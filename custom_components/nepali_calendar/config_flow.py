"""Config flow for Nepali Calendar."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class NepaliCalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nepali Calendar."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        # Only one instance allowed
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Nepali Calendar", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={
                "info": (
                    "Adds the Nepali (Bikram Sambat) calendar sensor, "
                    "calendar entity, and conversion services."
                )
            },
        )


# Compatibility shim for older Home Assistant versions using HANDLERS registry.
if hasattr(config_entries, "HANDLERS"):
    config_entries.HANDLERS.register(DOMAIN)(NepaliCalendarConfigFlow)
