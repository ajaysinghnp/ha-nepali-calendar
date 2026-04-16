"""calendar.py – calendar.nepali_events entity."""

from __future__ import annotations

import datetime
import logging
from typing import Any

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, NEPALI_MONTHS
from .date_utils import gregorian_from_nepali, nepali_from_gregorian
from .event_store import EventStore

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    store: EventStore = hass.data[DOMAIN]["store"]
    async_add_entities([NepaliCalendarEntity(store)], update_before_add=True)


class NepaliCalendarEntity(CalendarEntity):
    """Calendar entity exposing Nepali events."""

    _attr_unique_id   = "nepali_calendar_events"
    _attr_name        = "Nepali Events"
    _attr_icon        = "mdi:calendar-heart"
    _attr_has_entity_name = True

    def __init__(self, store: EventStore) -> None:
        self._store = store

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event (if any)."""
        today_bs = nepali_from_gregorian(datetime.date.today())
        today_greg = datetime.date.today()

        # look 365 days ahead
        for offset in range(365):
            check_greg = today_greg + datetime.timedelta(days=offset)
            check_bs   = nepali_from_gregorian(check_greg)
            evts = self._store.get_for_bs_date(
                check_bs.year, check_bs.month, check_bs.day
            )
            if evts:
                ev = evts[0]
                return self._to_calendar_event(ev, check_greg)
        return None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[CalendarEvent]:
        """Return events in the Gregorian range requested by HA."""
        results: list[CalendarEvent] = []
        current = start_date.date()
        end     = end_date.date()

        while current <= end:
            bs = nepali_from_gregorian(current)
            evts = self._store.get_for_bs_date(bs.year, bs.month, bs.day)
            for ev in evts:
                results.append(self._to_calendar_event(ev, current))
            current += datetime.timedelta(days=1)

        return results

    @staticmethod
    def _to_calendar_event(ev: dict, greg_date: datetime.date) -> CalendarEvent:
        month_name = NEPALI_MONTHS[ev["bs_month"] - 1]
        description = (
            f"BS: {ev['bs_year']} {month_name} {ev['bs_day']}"
            + (f"\n{ev['description']}" if ev.get("description") else "")
            + ("\n(Annual)" if ev.get("annual") else "")
        )
        return CalendarEvent(
            start       = greg_date,
            end         = greg_date + datetime.timedelta(days=1),
            summary     = ev["title"],
            description = description,
            uid         = ev["id"],
        )
