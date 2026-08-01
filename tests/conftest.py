"""Stub out homeassistant modules so tests run without a full HA install."""

import enum
import sys
import types


def _stub(name):
    """Ensure a dotted module path exists in sys.modules."""
    parts = name.split(".")
    for i in range(1, len(parts) + 1):
        key = ".".join(parts[:i])
        if key not in sys.modules:
            sys.modules[key] = types.ModuleType(key)


for _mod in [
    "homeassistant",
    "homeassistant.config_entries",
    "homeassistant.core",
    "homeassistant.helpers",
    "homeassistant.helpers.entity",
    "homeassistant.helpers.entity_platform",
    "homeassistant.components",
    "homeassistant.components.sensor",
    "homeassistant.components.binary_sensor",
    "homeassistant.const",
    "websockets",
    "websockets.protocol",
]:
    _stub(_mod)


# --- homeassistant.components.sensor ---

class SensorStateClass(str, enum.Enum):
    MEASUREMENT = "measurement"
    TOTAL = "total"
    TOTAL_INCREASING = "total_increasing"


class SensorDeviceClass(str, enum.Enum):
    CURRENT = "current"
    ENERGY = "energy"
    POWER = "power"
    DURATION = "duration"


_sensor = sys.modules["homeassistant.components.sensor"]
_sensor.SensorStateClass = SensorStateClass
_sensor.SensorDeviceClass = SensorDeviceClass

# --- homeassistant.components.binary_sensor ---

class BinarySensorDeviceClass(str, enum.Enum):
    PLUG = "plug"


sys.modules["homeassistant.components.binary_sensor"].BinarySensorDeviceClass = BinarySensorDeviceClass

# --- homeassistant.const ---

class EntityCategory(str, enum.Enum):
    DIAGNOSTIC = "diagnostic"


class Platform(str, enum.Enum):
    SENSOR = "sensor"
    BUTTON = "button"
    NUMBER = "number"
    SELECT = "select"


_const = sys.modules["homeassistant.const"]
_const.EntityCategory = EntityCategory
_const.Platform = Platform
_const.UnitOfEnergy = types.SimpleNamespace(WATT_HOUR="Wh", KILO_WATT_HOUR="kWh")
_const.UnitOfPower = types.SimpleNamespace(WATT="W")
_const.UnitOfElectricCurrent = types.SimpleNamespace(AMPERE="A")
_const.UnitOfTime = types.SimpleNamespace(MINUTES="min")
_const.CONF_HOST = "host"
_const.CONF_PORT = "port"
_const.CONF_FRIENDLY_NAME = "friendly_name"

# --- homeassistant.config_entries ---

class ConfigEntry:
    """Minimal stub for ConfigEntry."""


sys.modules["homeassistant.config_entries"].ConfigEntry = ConfigEntry

# --- homeassistant.core ---

class HomeAssistant:
    """Minimal stub for HomeAssistant."""


sys.modules["homeassistant.core"].HomeAssistant = HomeAssistant

# --- homeassistant.helpers.entity ---

sys.modules["homeassistant.helpers.entity"].Entity = object
sys.modules["homeassistant.helpers.entity"].DeviceInfo = dict

# --- homeassistant.helpers.entity_platform ---

sys.modules["homeassistant.helpers.entity_platform"].AddEntitiesCallback = object

# --- websockets ---

sys.modules["websockets.protocol"].State = types.SimpleNamespace(OPEN="OPEN")
sys.modules["websockets"].connect = None
sys.modules["websockets"].WebSocketException = Exception
