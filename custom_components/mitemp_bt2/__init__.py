"""支持小米米家蓝牙温湿度计2"""
import logging
import threading
import time
from datetime import timedelta
from homeassistant.helpers import device_registry as dr
from homeassistant.util import Throttle
from homeassistant.const import (
    CONF_MAC,
    CONF_MODE
)

from .const import (
    DOMAIN,
    UPDATE_TOPIC,
    ERROR_TOPIC
)
from .sensor import SingletonBLEScanner

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)
ERROR_SLEEP_TIME = timedelta(minutes=5)

async def async_setup(hass, config):
    """Do not allow config via configuration.yaml"""
    # hass.data[DOMAIN] = {}

    return True

async def async_setup_entry(hass, entry):
    """Set up a config entry."""
    _LOGGER.debug(entry)
    hass.async_create_task(
      hass.config_entries.async_forward_entry_setup(
        entry, "sensor"
      )
    )

    device_registry = await dr.async_get_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        manufacturer="Xiaomi Mijia",
        name="Hygrometer",
    )

    hass.data[DOMAIN] = MiTempBT2Hub(SingletonBLEScanner(), hass, entry.data)
    hass.data[DOMAIN].start()

    return True

async def async_unload_entry(hass, config_entry):
    """Unload flood monitoring sensors."""
    return await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")

class MiTempBT2Hub(threading.Thread):
    """蓝牙设备数据扫描"""

    def __init__(self, instance, hass, hass_config):
        """Init MiTempBT2 Hub"""
        super().__init__()
        self.instance = instance
        self.hass = hass
        self.hass_config = hass_config

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update sensors from Bluetooth devices."""
        data = self.instance.get_info(self.hass_config[CONF_MAC], mode=self.hass_config[CONF_MODE])

        if data:
            self.hass.helpers.dispatcher.dispatcher_send(UPDATE_TOPIC.format(self.hass_config[CONF_MAC].replace(":", "").lower()), data)

    def run(self):
        """Thread run loop."""
        while True:
            try:
                _LOGGER.debug("Starting mitemp_bt2 loop")
                self.update()
                time.sleep(MIN_TIME_BETWEEN_UPDATES.seconds)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(
                    "Error updating mitemp_bt2 data. "
                    "This probably means the devices is not ready now"
                )
                self.hass.helpers.dispatcher.dispatcher_send(ERROR_TOPIC.format(self.hass_config[CONF_MAC].replace(":", "").lower()))
                time.sleep(ERROR_SLEEP_TIME.seconds)
