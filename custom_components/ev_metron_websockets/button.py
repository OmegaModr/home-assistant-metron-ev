"""Buttons to perform Metron EV Station actions."""

from dataclasses import dataclass

from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from . import const
from .entity import MetronEVBaseEntity
from .hub import MetronEVHub


@dataclass
class MetronEVButtonDescriptionMixin:
    """Mixin to add action_data to ButtonEntityDescription class."""

    action_data: dict


@dataclass
class MetronEVButtonDescription(ButtonEntityDescription, MetronEVButtonDescriptionMixin):
    """Class for adding Mixin class to base ButtonEntityDescription."""


BUTTONS: tuple[MetronEVButtonDescription] = (
    MetronEVButtonDescription(
        name="Solar ON",
        key="solar_on",
        translation_key="solar_on",
        action_data=const.ACTION_SOLAR_ON,
    ),
    MetronEVButtonDescription(
        name="Solar OFF",
        key="solar_off",
        translation_key="solar_off",
        action_data=const.ACTION_SOLAR_OFF,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add buttons for setup hub object."""

    hub = hass.data[const.DOMAIN][config_entry.entry_id]

    async_add_entities(MetronButton(hub, description) for description in BUTTONS)

    async def toggle_solar(call: ServiceCall):
        """Toggle solar charging."""
        if int(hub.solar_charging_enable) == 1 and int(hub.solar_charging_enable_esp) == 1:
            await hub.perform_action("solON0")
        else:
            await hub.perform_action("solOF1")

    async def send_dynamic_limit(call: ServiceCall):
        """Send the current change to station."""
        integer_value = int(call.data.get("current"))
        payload = "SLIDE" + str(integer_value)
        await hub.perform_action(payload)

    async def send_charge_delay(call: ServiceCall):
        """Send the time delay to station."""
        integer_value = int(call.data.get("time"))
        payload = "TIMER" + str(integer_value)
        await hub.perform_action(payload)


    hass.services.async_register(const.DOMAIN, 'set_dynamic_limit', send_dynamic_limit)
    hass.services.async_register(const.DOMAIN, 'set_charger_delay', send_charge_delay)
    hass.services.async_register(const.DOMAIN, 'toggle_solar', toggle_solar)


class MetronButton(MetronEVBaseEntity, ButtonEntity):
    """Button class which will run the hub.perform_action method with configured description action_data."""

    def __init__(
        self,
        hub: MetronEVHub,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub._name}_{description.key}"
        self.entity_description = description

    async def async_press(self) -> None:
        """Trigger the button action."""
        await self._hub.perform_action(self.entity_description.action_data)
