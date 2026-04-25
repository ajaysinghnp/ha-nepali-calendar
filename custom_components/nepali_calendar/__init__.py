"""
Nepali (Bikram Sambat) Calendar – Home Assistant custom integration.

Registers:
  • sensor.nepali_date          – current BS date sensor
  • calendar.nepali_events      – calendar entity (shows events in the HA calendar card)
  • services: gregorian_to_nepali, nepali_to_gregorian, add_event, delete_event, list_events
  • Lovelace card auto-loaded from  /local/nepali-calendar-card/nepali-calendar-card.js
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    EVENTS_FILE,
    DATA_FILE,
    BS_YEAR_DATA,
    SERVICE_GREGORIAN_TO_NEPALI,
    SERVICE_NEPALI_TO_GREGORIAN,
    SERVICE_ADD_EVENT,
    SERVICE_DELETE_EVENT,
    SERVICE_LIST_EVENTS,
    NEPALI_MONTHS_ENG,
)
from .date_utils import (
    nepali_from_gregorian,
    gregorian_from_nepali,
    validate_bs_date,
)
from .event_store import EventStore

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "calendar"]

# ── Schema for services ────────────────────────────────────────────────────────

_GREG_TO_NEP_SCHEMA = vol.Schema(
    {
        vol.Required("year"): vol.All(int, vol.Range(min=1900, max=2200)),
        vol.Required("month"): vol.All(int, vol.Range(min=1, max=12)),
        vol.Required("day"): vol.All(int, vol.Range(min=1, max=31)),
    }
)

_NEP_TO_GREG_SCHEMA = vol.Schema(
    {
        vol.Required("bs_year"): vol.All(int, vol.Range(min=1900, max=2200)),
        vol.Required("bs_month"): vol.All(int, vol.Range(min=1, max=12)),
        vol.Required("bs_day"): vol.All(int, vol.Range(min=1, max=32)),
    }
)

_ADD_EVENT_SCHEMA = vol.Schema(
    {
        vol.Required("title"): cv.string,
        vol.Required("bs_year"): vol.All(int, vol.Range(min=1900, max=2200)),
        vol.Required("bs_month"): vol.All(int, vol.Range(min=1, max=12)),
        vol.Required("bs_day"): vol.All(int, vol.Range(min=1, max=32)),
        vol.Optional("description", default=""): cv.string,
        vol.Optional("annual", default=False): cv.boolean,
        vol.Optional("color", default=""): cv.string,
    }
)

_DELETE_EVENT_SCHEMA = vol.Schema(
    {
        vol.Required("event_id"): cv.string,
    }
)

_LIST_EVENTS_SCHEMA = vol.Schema(
    {
        vol.Optional("bs_year"): vol.All(int, vol.Range(min=1900, max=2200)),
        vol.Optional("bs_month"): vol.All(int, vol.Range(min=1, max=12)),
    }
)


# ── Setup ──────────────────────────────────────────────────────────────────────


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the nepali_calendar component (YAML configuration entry)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # ── Load optional user-supplied data override ──────────────────────────────
    data_path = hass.config.path(DATA_FILE)
    if os.path.exists(data_path):
        try:
            with open(data_path, encoding="utf-8") as fh:
                user_data = json.load(fh)
            BS_YEAR_DATA.update({int(k): v for k, v in user_data.items()})
            _LOGGER.info("Loaded %d BS year entries from %s", len(user_data), data_path)
        except (json.JSONDecodeError, OSError, ValueError) as err:
            _LOGGER.warning("Could not load %s: %s", data_path, err)

    # ── Event store ─────────────────────────────────────────────────────────────
    store = EventStore(hass.config.config_dir, EVENTS_FILE)
    await store.async_load()
    hass.data[DOMAIN]["store"] = store
    hass.data[DOMAIN]["entry"] = entry

    # ── Forward to platforms ────────────────────────────────────────────────────
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # ── Register services ───────────────────────────────────────────────────────
    _register_services(hass, store)

    # ── Auto-register Lovelace card resource ────────────────────────────────────
    await _async_register_lovelace_resource(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop("store", None)
        hass.data[DOMAIN].pop("entry", None)
        for svc in [
            SERVICE_GREGORIAN_TO_NEPALI,
            SERVICE_NEPALI_TO_GREGORIAN,
            SERVICE_ADD_EVENT,
            SERVICE_DELETE_EVENT,
            SERVICE_LIST_EVENTS,
        ]:
            hass.services.async_remove(DOMAIN, svc)
    return unload_ok


# ── Service registration ───────────────────────────────────────────────────────


def _register_services(hass: HomeAssistant, store: EventStore) -> None:

    async def svc_greg_to_nep(call: ServiceCall) -> None:
        year, month, day = call.data["year"], call.data["month"], call.data["day"]
        try:
            import datetime

            greg = datetime.date(year, month, day)
        except ValueError as err:
            _LOGGER.error("gregorian_to_nepali: invalid date – %s", err)
            return
        nep = nepali_from_gregorian(greg)
        hass.bus.async_fire(
            f"{DOMAIN}_conversion_result",
            {
                "direction": "gregorian_to_nepali",
                "input": {"year": year, "month": month, "day": day},
                "output": {
                    "bs_year": nep.year,
                    "bs_month": nep.month,
                    "bs_day": nep.day,
                    "month_name": nep.month_name_eng,
                    "month_name_np": nep.month_name_np,
                },
            },
        )
        _LOGGER.info(
            "gregorian_to_nepali: %04d-%02d-%02d → %s",
            year,
            month,
            day,
            nep,
        )

    async def svc_nep_to_greg(call: ServiceCall) -> None:
        bs_year = call.data["bs_year"]
        bs_month = call.data["bs_month"]
        bs_day = call.data["bs_day"]
        err = validate_bs_date(bs_year, bs_month, bs_day)
        if err:
            _LOGGER.error("nepali_to_gregorian: %s", err)
            return
        greg = gregorian_from_nepali(bs_year, bs_month, bs_day)
        hass.bus.async_fire(
            f"{DOMAIN}_conversion_result",
            {
                "direction": "nepali_to_gregorian",
                "input": {"bs_year": bs_year, "bs_month": bs_month, "bs_day": bs_day},
                "output": {"year": greg.year, "month": greg.month, "day": greg.day},
            },
        )
        _LOGGER.info(
            "nepali_to_gregorian: %04d-%02d-%02d → %s",
            bs_year,
            bs_month,
            bs_day,
            greg.isoformat(),
        )

    async def svc_add_event(call: ServiceCall) -> None:
        err = validate_bs_date(
            call.data["bs_year"], call.data["bs_month"], call.data["bs_day"]
        )
        if err:
            _LOGGER.error("add_event: %s", err)
            return
        event = await store.async_add_event(
            title=call.data["title"],
            bs_year=call.data["bs_year"],
            bs_month=call.data["bs_month"],
            bs_day=call.data["bs_day"],
            description=call.data.get("description", ""),
            annual=call.data.get("annual", False),
            color=call.data.get("color", ""),
        )
        hass.bus.async_fire(f"{DOMAIN}_event_added", event)
        _LOGGER.info("Event added: %s", event["title"])

    async def svc_delete_event(call: ServiceCall) -> None:
        ok = await store.async_delete_event(call.data["event_id"])
        if ok:
            hass.bus.async_fire(
                f"{DOMAIN}_event_deleted", {"event_id": call.data["event_id"]}
            )
            _LOGGER.info("Event deleted: %s", call.data["event_id"])
        else:
            _LOGGER.warning("delete_event: ID not found – %s", call.data["event_id"])

    async def svc_list_events(call: ServiceCall) -> None:
        bs_year = call.data.get("bs_year")
        bs_month = call.data.get("bs_month")
        if bs_year and bs_month:
            events = store.get_for_bs_month(bs_year, bs_month)
        else:
            events = store.get_all()
        hass.bus.async_fire(
            f"{DOMAIN}_events_list", {"events": events, "count": len(events)}
        )

    hass.services.async_register(
        DOMAIN, SERVICE_GREGORIAN_TO_NEPALI, svc_greg_to_nep, _GREG_TO_NEP_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_NEPALI_TO_GREGORIAN, svc_nep_to_greg, _NEP_TO_GREG_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_ADD_EVENT, svc_add_event, _ADD_EVENT_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_DELETE_EVENT, svc_delete_event, _DELETE_EVENT_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LIST_EVENTS, svc_list_events, _LIST_EVENTS_SCHEMA
    )


# ── Lovelace resource auto-registration ───────────────────────────────────────


async def _async_register_lovelace_resource(hass: HomeAssistant) -> None:
    """Attempt to register the Lovelace card JS as a frontend resource."""
    url = "/local/nepali-calendar-card/nepali-calendar-card.js"
    try:
        lovelace = hass.data.get("lovelace")
        if lovelace is None:
            return
        resources = lovelace.get("resources")
        if resources is None:
            return
        existing = [r.get("url") for r in await resources.async_get()]
        if url not in existing:
            await resources.async_create_item({"res_type": "module", "url": url})
            _LOGGER.info("Registered Lovelace resource: %s", url)
    except Exception:  # noqa: BLE001
        # Non-fatal – user can add the resource manually
        _LOGGER.debug(
            "Could not auto-register Lovelace resource. "
            "Add it manually via  Settings → Dashboards → Resources."
        )
