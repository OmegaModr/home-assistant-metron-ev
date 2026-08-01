"""Config flow for Metron EV charger integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PORT, CONF_HOST, CONF_FRIENDLY_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN
from .hub import MetronEVHub

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_FRIENDLY_NAME, default="Home Charger"): str,
        vol.Required(CONF_HOST, default="localhost"): str,
        vol.Required(CONF_PORT, default="80"): str,
    }
)


def _reconfigure_schema(host: str, port: str) -> vol.Schema:
    """Return schema for editing the connection details of an existing entry."""
    return vol.Schema(
        {
            vol.Required(CONF_HOST, default=host): str,
            vol.Required(CONF_PORT, default=port): str,
        }
    )


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    metron_ev_hub = MetronEVHub(
        hass,
        data[CONF_FRIENDLY_NAME],
        data[CONF_HOST],
        data[CONF_PORT],
    )

    if not await metron_ev_hub.test_endpoint():
        raise InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": data[CONF_FRIENDLY_NAME]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Metron EV charger."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle changing the host/port of an already configured charger.

        The friendly name is kept unchanged because every entity's unique_id is
        derived from it; only the connection details are editable here so the
        existing entities, automations and dashboards are preserved.
        """
        entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )

        errors: dict[str, str] = {}
        if user_input is not None:
            new_data = {**entry.data, **user_input}
            try:
                await validate_input(self.hass, new_data)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                self._migrate_device_identifier(
                    entry, entry.data[CONF_HOST], new_data[CONF_HOST]
                )
                return self.async_update_reload_and_abort(
                    entry, data=new_data, reason="reconfigure_successful"
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_reconfigure_schema(
                entry.data[CONF_HOST], entry.data[CONF_PORT]
            ),
            errors=errors,
        )

    def _migrate_device_identifier(
        self, entry: config_entries.ConfigEntry, old_host: str, new_host: str
    ) -> None:
        """Move the device registry entry to the new host-based identifier.

        The device is identified by ``(DOMAIN, host.lower())``; without this the
        old device would be orphaned and a new one created, losing its area and
        name customisations.
        """
        if old_host.lower() == new_host.lower():
            return

        device_reg = dr.async_get(self.hass)
        device = device_reg.async_get_device(
            identifiers={(DOMAIN, old_host.lower())}
        )
        if device is not None:
            device_reg.async_update_device(
                device.id,
                new_identifiers={(DOMAIN, new_host.lower())},
            )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
