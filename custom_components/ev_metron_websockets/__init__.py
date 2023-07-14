"""The Metron EV integration."""
from __future__ import annotations


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform,
    CONF_PORT,
    CONF_HOST,
    CONF_FRIENDLY_NAME,
)

from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .hub import MetronEVHub


PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Metron EV from a config entry."""

    hub = MetronEVHub(
        hass,
        entry.data[CONF_FRIENDLY_NAME],
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
    )

    entry.async_create_background_task(hass, hub.update(), "ev_metron_update")
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
