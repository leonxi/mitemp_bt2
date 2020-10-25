"""支持小米米家蓝牙温湿度计2"""
import logging
from datetime import timedelta
from homeassistant.helpers import device_registry as dr

from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

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

    return True

async def async_unload_entry(hass, config_entry):
    """Unload flood monitoring sensors."""
    return await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
