"""Constants for the Xiaomi Mijia Bluetooth Termometer."""
from homeassistant.const import (
    PERCENTAGE,
    TEMP_CELSIUS
)

DOMAIN = "mitemp_bt2"
DEFAULT_NAME = 'Mijia BLE Temperature Hygrometer 2'

# Configuration options
CONF_PERIOD = "period"
CONF_USE_MEDIAN = "use_median"
CONF_ACTIVE_SCAN = "active_scan"

# Default values for configuration options
DEFAULT_PERIOD = 300
DEFAULT_USE_MEDIAN = False
DEFAULT_ACTIVE_SCAN = False
DEFAULT_MODE = "LYWSD03MMC" # "LYWSD03MMC", "LYWSDCGQ/01ZM" are available

MODES = ["LYWSD03MMC", "LYWSDCGQ/01ZM"]

SENSOR_TYPES = {
    'temperature': ['温度', TEMP_CELSIUS],
    'humidity': ['湿度', PERCENTAGE],
    'battery': ['电量', PERCENTAGE],
}
