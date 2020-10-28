"""支持小米米家蓝牙温湿度计2"""
import logging
import threading
import time
from datetime import timedelta

from homeassistant import config_entries
from homeassistant.helpers import device_registry as dr
from homeassistant.util import Throttle
from homeassistant.const import (
    CONF_MAC,
    CONF_MODE
)

from .const import (
    DOMAIN,
    ATTR_CONFIG,
    CONF_DISCOVERY,
    UPDATE_TOPIC,
    ERROR_TOPIC
)
from .common import (
    get_static_devices,
    async_discover_devices
)
from .sensor import SingletonBLEScanner

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)
ERROR_SLEEP_TIME = timedelta(minutes=5)

async def async_setup(hass, config):
    """Do not allow config via configuration.yaml"""
    conf = config.get("sensor")
    _LOGGER.debug("async_setup sensor %s", conf)
    conf2 = config.get(DOMAIN)
    _LOGGER.debug("async_setup %s %s", DOMAIN, conf2)

    if not hasattr(hass.data, DOMAIN):
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN][ATTR_CONFIG] = conf

    if conf is not None:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": config_entries.SOURCE_IMPORT}
            )
        )

    return True

async def async_setup_entry(hass, entry):
    """Set up a config entry."""
    _LOGGER.debug("async_setup_entry %s", entry.data)
    config_data = hass.data[DOMAIN].get(ATTR_CONFIG)
    _LOGGER.debug("async_setup_entry %s", config_data)

    sensors = hass.data[DOMAIN]["sensor"] = []

    # Add static devices
    static_devices = []
    if config_data is not None:
        static_devices = get_static_devices(config_data)

        # sensors.extend(static_devices)

    # Add discovered devices
    if config_data is None or True: # config_data[CONF_DISCOVERY]
        discovered_devices = await async_discover_devices(hass, static_devices)

        sensors.extend(discovered_devices)

    if sensors:
        _LOGGER.debug(
            "Got %s sensors: %s", len(sensors), ", ".join([d.mac for d in sensors])
        )
        hass.async_create_task(
          hass.config_entries.async_forward_entry_setup(
            entry, "sensor"
          )
        )

        device_registry = await dr.async_get_registry(hass)

        for device in sensors:
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, device.id)},
                model=device.mode,
                manufacturer="小米 米家",
                name=device.friendly_name,
            )

    if len(sensors) > 0:
        hass.data[DOMAIN]["hub"] = MiTempBT2Hub(SingletonBLEScanner(), hass, sensors)

    return True

async def async_unload_entry(hass, config_entry):
    """Unload flood monitoring sensors."""
    return await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")

class MiTempBT2Hub(threading.Thread):
    """蓝牙设备数据扫描"""

    def __init__(self, instance, hass, sensors):
        """Init MiTempBT2 Hub"""
        super().__init__()
        self.instance = instance
        self.hass = hass
        self.sensors = sensors

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update sensors from Bluetooth devices."""
        for sensor in self.sensors:
            try:
                data = self.instance.get_info(sensor.mac, mode=sensor.mode)

                if data:
                    self.hass.helpers.dispatcher.dispatcher_send(UPDATE_TOPIC.format(sensor.id), data)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(
                    "Error updating mitemp_bt2 data. "
                    "This probably means the devices is not ready now"
                )
                self.hass.helpers.dispatcher.dispatcher_send(ERROR_TOPIC.format(sensor.id))
                time.sleep(ERROR_SLEEP_TIME.seconds)

    def run(self):
        """Thread run loop."""
        while True:
            _LOGGER.debug("Starting mitemp_bt2 loop")
            self.update()
            time.sleep(MIN_TIME_BETWEEN_UPDATES.seconds)
