"""Constants for the Xiaomi Mijia Bluetooth Termometer."""
from homeassistant.const import (
    PERCENTAGE,
    TEMP_CELSIUS
)

DOMAIN = "mitemp_bt2"
DEFAULT_NAME = 'Mijia BLE Temperature Hygrometer 2'
ATTR_CONFIG = "config"

# Configuration options
CONF_PERIOD = "period"
CONF_USE_MEDIAN = "use_median"
CONF_ACTIVE_SCAN = "active_scan"
CONF_DISCOVERY = "discovery"

# Default values for configuration options
DEFAULT_PERIOD = 300
DEFAULT_USE_MEDIAN = False
DEFAULT_ACTIVE_SCAN = False
DEFAULT_MODE = "LYWSD03MMC" # "LYWSD03MMC", "LYWSDCGQ/01ZM" are available
DEFAULT_DISCOVERY = True

MODES = ["LYWSD03MMC", "LYWSDCGQ/01ZM"]
NAMES = ["米家蓝牙温湿度计2", "米家蓝牙温湿度计"]

SENSOR_TYPES = {
    'temperature': ['温度', TEMP_CELSIUS],
    'humidity': ['湿度', PERCENTAGE],
    'battery': ['电量', PERCENTAGE],
}

UPDATE_TOPIC = DOMAIN + ".sensor.{}"
ERROR_TOPIC = DOMAIN + ".sensor.{}_error"
