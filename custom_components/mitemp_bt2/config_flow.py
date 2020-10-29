"""Adds config flow for mitemp_bt2."""
import logging
from collections import OrderedDict

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_entry_flow
from homeassistant.core import callback
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
    TEMP_CELSIUS
)

from .common import async_get_discoverable_devices
from .const import (
    DOMAIN,
    MODES,
    CONF_DISCOVERY,
    DEFAULT_DISCOVERY,
    DEFAULT_NAME,
    DEFAULT_MODE,
    DEFAULT_PERIOD,
    DEFAULT_USE_MEDIAN,
    DEFAULT_ACTIVE_SCAN,
    CONF_PERIOD,
    SENSOR_TYPES
)

_LOGGER = logging.getLogger(__name__)

class ConfigFlowHanlder(config_entries.ConfigFlow, domain=DOMAIN):
    """config flow for mitemp_bt2."""
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}
        _LOGGER.debug("Step user")

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="米家温湿度计", data=user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit the data."""
        data_schema = OrderedDict()

        data_schema[vol.Required(CONF_DISCOVERY, default=DEFAULT_DISCOVERY)] = bool
        data_schema[vol.Required(CONF_PERIOD, default=DEFAULT_PERIOD)] = int

        _LOGGER.debug("config form")

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Options callback for MiTempBT2."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize UniFi options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, _user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="选项", data=user_input)

        discovery = self.config_entry.options.get(CONF_DISCOVERY)
        period = self.config_entry.options.get(CONF_PERIOD)

        if discovery is None:
            discovery = self.config_entry.data.get(CONF_DISCOVERY)

        if period is None:
            period = self.config_entry.data.get(CONF_PERIOD)

        data_schema = OrderedDict()
        data_schema[
            vol.Required(CONF_DISCOVERY, default=discovery)
        ] = bool
        data_schema[
            vol.Required(CONF_PERIOD, default=period)
        ] = int

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema)
        )

# config_entry_flow.register_discovery_flow(
#     DOMAIN, "米家温湿度计", async_get_discoverable_devices, config_entries.CONN_CLASS_LOCAL_POLL
# )
