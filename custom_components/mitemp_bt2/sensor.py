"""使用单例对象控制蓝牙接口连接多个设备，获取数据"""
import logging
import threading
import voluptuous as vol
from typing import Optional
import asyncio
from dataclasses import dataclass
from bluepy import btle
import time
import traceback
from datetime import timedelta

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_BATTERY,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
    CONF_MAC,
    CONF_MODE,
    ATTR_ATTRIBUTION,
    ATTR_FRIENDLY_NAME,
    PERCENTAGE,
    TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_point_in_utc_time
import homeassistant.util.dt as dt_util

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_MODE,
    DEFAULT_PERIOD,
    DEFAULT_USE_MEDIAN,
    DEFAULT_ACTIVE_SCAN,
    CONF_PERIOD,
    CONF_USE_MEDIAN,
    CONF_ACTIVE_SCAN
)

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION_1 = "米家蓝牙温湿度计"
ATTRIBUTION = "米家蓝牙温湿度计 2"

SENSOR_TYPES = {
    'temperature': ['温度', TEMP_CELSIUS],
    'humidity': ['湿度', PERCENTAGE],
    'battery': ['电量', PERCENTAGE],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC): cv.string,
    vol.Optional(CONF_MODE, default=DEFAULT_MODE): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_PERIOD, default=DEFAULT_PERIOD): cv.positive_int,
    vol.Optional(CONF_USE_MEDIAN, default=DEFAULT_USE_MEDIAN): cv.boolean,
    vol.Optional(CONF_ACTIVE_SCAN, default=DEFAULT_ACTIVE_SCAN): cv.boolean,
    vol.Optional(CONF_MONITORED_CONDITIONS, default=list(SENSOR_TYPES)):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
})

@dataclass
class Measurement:
    temperature: float
    humidity: int
    voltage: float
    calibratedHumidity: int = 0
    battery: int = 0
    timestamp: int = 0

    def __eq__(self, other):
        if self.temperature == other.temperature and self.humidity == other.humidity and self.calibratedHumidity == other.calibratedHumidity and self.battery == other.battery and self.voltage == other.voltage:
            return  True
        else:
            return False

mode="round"
class MyDelegate(btle.DefaultDelegate):

    def __init__(self, mac, future):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here
        self._mac = mac
        self._future = future
        self._cnt = 0

    def handleNotification(self, cHandle, data):

        self._cnt += 1
        try:
            measurement = Measurement(0,0,0,0,0,0)
            measurement.timestamp = int(time.time())

            temp=round(int.from_bytes(data[0:2],byteorder='little',signed=True)/100, 1)
            humidity=int.from_bytes(data[2:3],byteorder='little')
            voltage=int.from_bytes(data[3:5],byteorder='little') / 1000.
            _LOGGER.debug("Temperature: " + str(temp))
            _LOGGER.debug("Humidity: " + str(humidity))
            _LOGGER.debug("Battery voltage:",voltage)

            measurement.temperature = temp
            measurement.humidity = humidity
            measurement.voltage = voltage

            batteryLevel = min(int(round((voltage - 2.1),2) * 100), 100) #3.1 or above --> 100% 2.1 --> 0 %
            measurement.battery = batteryLevel

            if self._cnt <= 1:
                self._future.set_result(measurement)
                self._future.done()

        except Exception as e:
            _LOGGER.error(traceback.format_exc())

class SingletonBLEScanner(object):
    """单例对象实现同步获取蓝牙数据, 确保多个设备同时访问不会产生蓝牙接口竞争"""
    _instance_lock = threading.Lock()
    _event_loop = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SingletonBLEScanner, "_instance"):
            with SingletonBLEScanner._instance_lock:
                if not hasattr(SingletonBLEScanner, "_instance"):
                    SingletonBLEScanner._instance = object.__new__(cls)
        return SingletonBLEScanner._instance

    def get_info(self, mac, mode = DEFAULT_MODE, interface = 0):
        with self._instance_lock:
            self._event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._event_loop)

            retries = 0
            success = False

            while not success and retries < 3:
                retries += 1

                if reties > 1:
                    self._event_loop.sleep(5)
                    _LOGGER.error("Waiting ...")

                try:
                    p = btle.Peripheral(mac, iface=interface)
                except btle.BTLEDisconnectError as e:
                    _LOGGER.error("%s Connection lost, Retrying ... %d" % (mac, retries))
                    _LOGGER.debug(traceback.format_exc())
                else:
                    success = True

            if not success:
                return

            future = asyncio.Future()

            val=b'\x01\x00'
            p.writeCharacteristic(0x0038,val,True) # enable notifications of Temperature, Humidity and Battery voltage

            if mode == DEFAULT_MODE:
                p.writeCharacteristic(0x0046,b'\xf4\x01\x00',True)

            p.withDelegate(MyDelegate(mac, future))

            cnt = 0
            while cnt < 1:
                cnt += 1

                if p.waitForNotifications(2000):
                    continue
            self._event_loop.run_until_complete(future)

            p.disconnect()

            result = future.result()
            self._event_loop.close()

            return result

    def shutdown_handler(self, event):
        """Run homeassistant_stop event handler."""
        _LOGGER.debug("Running homeassistant_stop event handler: %s", event)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    devs = []

    mac = config[CONF_MAC]
    mode = config[CONF_MODE]
    instance = SingletonBLEScanner()
    hass.bus.listen("homeassistant_stop", instance.shutdown_handler)

    for parameter in config[CONF_MONITORED_CONDITIONS]:
        name = SENSOR_TYPES[parameter][0]
        unit = SENSOR_TYPES[parameter][1]

        prefix = config.get(CONF_NAME)
        if prefix:
            name = "{} {}".format(prefix, name)

        devs.append(MiTemperatureSensor(mac, mode, parameter, name, unit))

    add_entities(devs, True)

    def discover_ble_device(config):

        data = instance.get_info(config[CONF_MAC], mode=config[CONF_MODE])

        if data:
            for dev in devs:
                device_class = dev.device_class

                if device_class == DEVICE_CLASS_TEMPERATURE:
                    setattr(dev, "_state", data.temperature)
                elif device_class == DEVICE_CLASS_HUMIDITY:
                    setattr(dev, "_state", data.humidity)
                else:
                    setattr(dev, "_state", data.battery)

                dev.schedule_update_ha_state()

                _LOGGER.debug("important %s %s state updated.", config[CONF_MAC], device_class)

    def update_ble(now):
        period = config[CONF_PERIOD]

        try:
            discover_ble_device(config)
        except RuntimeError as error:
            _LOGGER.error("Error during Bluetooth LE scan: %s", error)

        track_point_in_utc_time(
            hass, update_ble, dt_util.utcnow() + timedelta(seconds=period)
        )

    update_ble(dt_util.utcnow())

    # Return successful setup
    return True

class MiTemperatureSensor(Entity):

    def __init__(self, mac, mode, parameter, name, unit):
        self._mac = mac
        self._mode = mode
        self.parameter = parameter
        self._unique_id = "{}_{}".format(parameter, mac.replace(":", "").lower())
        self._unit = unit
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def available(self):
        """Return true if device is available."""
        return not self._state is None

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def device_class(self):
        return self.parameter

    @property
    def device_state_attributes(self):
        if self._state is not None:
            if self._mode == DEFAULT_MODE:
                return {
                    ATTR_ATTRIBUTION: ATTRIBUTION,
                }
            else:
                return {
                    ATTR_ATTRIBUTION: ATTRIBUTION_1,
                }

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""

        return self._unique_id

    @property
    def force_update(self):
        """Force update."""
        return True
