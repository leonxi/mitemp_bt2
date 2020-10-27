"""mitemp_bt2 common functions."""
import logging
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError
import asyncio

from homeassistant.const import (
    CONF_MAC,
    CONF_MODE
)

from .const import (
    CONF_PERIOD,
    DEFAULT_PERIOD,
    MODES,
    NAMES
)

_LOGGER = logging.getLogger(__name__)

class MiTemperatureDevice():
    def __init__(self, mac, mode, period, static = False):
        self._mac = mac.lower()
        self._mode = mode
        self._period = period
        self._static = static

    @property
    def id(self):
        return self._mac.replace(":", "").lower()

    @property
    def mac(self):
        return self._mac

    @property
    def mode(self):
        return self._mode

    @property
    def period(self):
        return self._period

    @property
    def name(self):
        return f"sensor.{self.id}"

    @property
    def friendly_name(self):
        if self.mode == MODES[0]:
            return NAMES[0]
        else:
            return NAMES[1]

    def is_static(self):
        return _static

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            _LOGGER.debug("Discovered device", dev.addr)
        elif isNewData:
            _LOGGER.debug("Received new data from", dev.addr)

async def _async_has_devices(hass) -> bool:
    """Return if there are devices that can be discovered."""
    # TODO Check if there are any devices that can be discovered in the network.
    def discover():
        scanner = Scanner().withDelegate(ScanDelegate())
        scanentries = None

        cnt = 0
        while scanentries is None and cnt < 3:
            cnt += 1

            try:
                scanentries = scanner.scan(10.0)
            except BTLEDisconnectError as e:
                _LOGGER.debug("Bluetooth device scanner exception.")
                asyncio.sleep(5)

        for dev in scanentries:
            _LOGGER.debug("Device %s (%s), RSSI=%d dB", dev.addr, dev.addrType, dev.rssi)
            for (adtype, desc, value) in dev.getScanData():
                _LOGGER.debug("  %s = %s", desc, value)

        return scanentries

    devices = await hass.async_add_executor_job(discover)
    return len(devices) > 0

async def async_get_discoverable_devices(hass):

    def discover():
        scanner = Scanner().withDelegate(ScanDelegate())
        scanentries = None

        cnt = 0
        while scanentries is None and cnt < 3:
            cnt += 1

            try:
                scanentries = scanner.scan(10.0)
            except BTLEDisconnectError as e:
                _LOGGER.debug("Bluetooth device scanner exception.")
                asyncio.sleep(5)

        devices = []

        for dev in scanentries:
            _LOGGER.debug("Device %s (%s), RSSI=%d dB", dev.addr, dev.addrType, dev.rssi)
            mac = dev.addr
            mode = None

            for (adtype, desc, value) in dev.getScanData():
                _LOGGER.debug("  %s = %s", desc, value)
                if desc == "Complete Local Name":
                    mode = value

            if mode is None or not mode in MODES:
                continue

            devices.append(MiTemperatureDevice(mac, mode, DEFAULT_PERIOD))

        return devices

    return await hass.async_add_executor_job(discover)

async def async_discover_devices(hass, existing_devices):
    """Get devices through discovery."""
    _LOGGER.debug("Discovering devices")
    devices = await async_get_discoverable_devices(hass)
    _LOGGER.info("Discovered %s mijia device(s)", len(devices))

    existing_devices_macs = [d.mac for d in existing_devices]
    sensors = []

    def process_devices():
        for dev in devices:
            # If this device already exists, ignore dynamic setup.
            if dev.mac in existing_devices_macs:
                continue

            sensors.append(dev)

    await hass.async_add_executor_job(process_devices)

    return sensors

def get_static_devices(config_data):
    """Get statically defined devices in the config."""
    _LOGGER.debug("Getting static devices")
    sensors = []

    for entry in config_data:
        mac = entry[CONF_MAC]
        mode = entry.get(CONF_MODE)
        period = entry.get(CONF_PERIOD)

        sensors.append(MiTemperatureDevice(mac, mode, period, True))

    return sensors
