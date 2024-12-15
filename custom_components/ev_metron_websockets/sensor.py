"""Contains the Entity classes."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfElectricCurrent, UnitOfTime
from homeassistant.util import dt as dt_util
from homeassistant.components.sensor import (
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)

from .const import DOMAIN
from .entity import MetronEVBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for setup hub object."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            MetronStatus(hub),
            MetronActive(hub),
            MetronName(hub),
            L1CurrentStation(hub),
            L2CurrentStation(hub),
            L3CurrentStation(hub),
            L1CurrentBuilding(hub),
            L2CurrentBuilding(hub),
            L3CurrentBuilding(hub),
            HouseEnergy(hub),
            L1CurrentSolar(hub),
            ButtonSetChargingCurrent(hub),
            MainFuseRating(hub),
            DinamicChargingCurrentLimit(hub),
            SolarChargingEnable(hub),
            SolarChargingEnableShort(hub),
            TotalChargingPower(hub),
            TotalHousePower(hub),
            TotalSolarPower(hub),
            ThisChargeEnergy(hub),
            ChargingTime(hub),
            PreviousChargeEnergy(hub),
            LifetimeEnergy(hub),
            SolarEnergy(hub),
            SolarSURPLUSPower(hub),
            LocalNetworkIPString(hub),
            TimerDelay(hub),
            SignalPresent(hub),
            CarConnected(hub),
            CarCharging(hub),
        ]
    )

class MetronStatus(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_station_status"
        self._attr_name = f"{hub._name} station status"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if int(self._hub.metron_ev_status) == 1 and int(self._hub._ESP32_timer_delay) == 0:
            return "Ready to charge"
        elif int(self._hub.metron_ev_status) == 1 and int(self._hub._ESP32_timer_delay) != 0:
            return "Charging start delayed"
        elif int(self._hub.metron_ev_status) == 2 and int(self._hub._TCA0_cmp2) != 8000:
            return "FULLY CHARGED or charging postponed"
        elif int(self._hub.metron_ev_status) == 2 and int(self._hub._TCA0_cmp2) == 8000 and int(self._hub._ESP32_timer_delay) == 0:
            return "Charging stopped"
        elif int(self._hub.metron_ev_status) == 2 and int(self._hub._TCA0_cmp2) == 8000 and int(self._hub._ESP32_timer_delay) != 0:
            return "Charging stopped"
        elif int(self._hub.metron_ev_status) == 3 and int(self._hub._TCA0_cmp2) != 8000:
            return "CHARGING"
        elif int(self._hub.metron_ev_status) == 3 and int(self._hub._TCA0_cmp2) == 8000 and int(self._hub._ESP32_timer_delay) == 0:
            return "Charging stopped"
        elif int(self._hub.metron_ev_status) == 3 and int(self._hub._TCA0_cmp2) == 8000 and int(self._hub._ESP32_timer_delay) != 0:
            return "Charging start delayed"
        elif int(self._hub.metron_ev_status) == 4:
            return "Room ventilation required by the vehicle, charging stopped"
        elif int(self._hub.metron_ev_status) == 5:
            return "STATION BOOTING"
        elif int(self._hub.metron_ev_status) == 6:
            return "Waiting for charging activation"
        elif int(self._hub.metron_ev_status) == 7:
            return "Waiting for charging activation"
        else:
            return "Station or vehicle error"

class MetronActive(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_station_active"
        self._attr_name = f"{hub._name} station active"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if self._hub.available is True:
            return "Connected"
        else:
            return "Disconnected"

class MetronName(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_station_name"
        self._attr_name = f"{hub._name} station name"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.metron_ev_name

class L1CurrentStation(MetronEVBaseEntity):
    """Metron station phase 1 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_L1_current_station"
        self._attr_name = f"{hub._name} L1 current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self):
        """Return the state of the sensor."""

        return self._hub.L1_current_station

class L2CurrentStation(MetronEVBaseEntity):
    """Metron station phase 2 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_L2_current_station"
        self._attr_name = f"{hub._name} L2 current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L2_current_station

class L3CurrentStation(MetronEVBaseEntity):
    """Metron station phase 3 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_L3_current_station"
        self._attr_name = f"{hub._name} L3 current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L1_current_station

class L1CurrentBuilding(MetronEVBaseEntity):
    """Metron station building phase 1 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_L1_current_building"
        self._attr_name = f"{hub._name} L1 building current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L1_current_building

class L2CurrentBuilding(MetronEVBaseEntity):
    """Metron station building phase 2 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_L2_current_building"
        self._attr_name = f"{hub._name} L2 building current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L2_current_building

class L3CurrentBuilding(MetronEVBaseEntity):
    """Metron station building phase 3 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_L3_current_building"
        self._attr_name = f"{hub._name} L3 building current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L3_current_building

class HouseEnergy(MetronEVBaseEntity):
    """Metron station building phase 3 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_house_energy"
        self._attr_name = f"{hub._name} house energy"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.House_energy

class L1CurrentSolar(MetronEVBaseEntity):
    """Metron solar current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_solar_current"
        self._attr_name = f"{hub._name} solar current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L1_current_solar

class ButtonSetChargingCurrent(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_button_set_current"
        self._attr_name = f"{hub._name} button set current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.button_set_charging_current

class MainFuseRating(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_main_fuse"
        self._attr_name = f"{hub._name} main fuse rating"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.main_fuse_rating

class DinamicChargingCurrentLimit(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_dinamic_charging_current_limit"
        self._attr_name = f"{hub._name} dinamic charging current limit"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.dinamic_charging_current_limit

class SolarChargingEnable(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_solar_charging_enable"
        self._attr_name = f"{hub._name} solar charging enable"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if int(self._hub.solar_charging_enable) == 1 and int(self._hub.solar_charging_enable_esp) == 1:
            return "Solar charging OFF"
        elif int(self._hub.solar_charging_enable) == 1 and int(self._hub.solar_charging_enable_esp) == 0:
            return "Solar charging activated"
        else:
            return "Solar charging activated by switch"

class SolarChargingEnableShort(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_solar_charging_enable_short"
        self._attr_name = f"{hub._name} solar charging state"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if int(self._hub.solar_charging_enable) == 1 and int(self._hub.solar_charging_enable_esp) == 1:
            return "OFF"
        elif int(self._hub.solar_charging_enable) == 1 and int(self._hub.solar_charging_enable_esp) == 0:
            return "ON"
        else:
            return "ON"

class TotalChargingPower(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_total_charging_power"
        self._attr_name = f"{hub._name} total charging power"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.total_charging_power

class TotalHousePower(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_total_house_power"
        self._attr_name = f"{hub._name} total house power"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.total_house_power

class TotalSolarPower(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_total_solar_power"
        self._attr_name = f"{hub._name} total solar power"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.total_solar_power

class ThisChargeEnergy(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_this_charge_energy"
        self._attr_name = f"{hub._name} this charge energy"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.this_charge_energy

class ChargingTime(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_charging_time"
        self._attr_name = f"{hub._name} charging time"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_device_class = SensorDeviceClass.DURATION

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        charging_time = (int(self._hub.hour_counter)*60)+int(self._hub.minute_counter)
        return charging_time

class PreviousChargeEnergy(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_previous_charge_energy"
        self._attr_name = f"{hub._name} previous charge energy"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.previous_charge_energy

class LifetimeEnergy(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_lifetime_energy"
        self._attr_name = f"{hub._name} lifetime_energy"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_last_reset = dt_util.utc_from_timestamp(0)

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.lifetime_energy

class SolarEnergy(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_solar_energy"
        self._attr_name = f"{hub._name}  solar energy"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.solar_energy

class SolarSURPLUSPower(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_solar_SURPLUS_power"
        self._attr_name = f"{hub._name} solar SURPLUS power"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.solar_SURPLUS_power

class LocalNetworkIPString(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_local_network_IP_string"
        self._attr_name = f"{hub._name} local network IP string"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.local_network_IP_string

class TimerDelay(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_ESP32_timer_delay"
        self._attr_name = f"{hub._name} timer delay"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_device_class = SensorDeviceClass.DURATION

    @property
    def state(self) -> int:
        """Return the state of the sensor."""

        return int(self._hub.ESP32_timer_delay)

class SignalPresent(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_HC12_Signal_Present"
        self._attr_name = f"{hub._name} Telemetry Signal Present"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if int(self._hub.HC12_Signal_Present) == 1:
            return "Good"
        else:
            return "No signal"

class CarConnected(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_car_connected"
        self._attr_name = f"{hub._name} car connected"
        self._attr_is_on = False
        self._attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""
        if int(self._hub.metron_ev_status) in [2, 3, 4, 7]:
            return True
        else:
            return False

class CarCharging(MetronEVBaseEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_charging"
        self._attr_name = f"{hub._name} charging"
        self._attr_is_on = False
        self._attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""
        if int(self._hub.metron_ev_status) == 3 and int(self._hub._TCA0_cmp2) != 8000:
            return True
        else:
            return False
