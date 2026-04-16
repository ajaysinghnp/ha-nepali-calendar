"""
event_store.py – Persistent JSON-backed event storage for Nepali Calendar.

Events are stored in  <config_dir>/nepali_events.json.
Each event is a dict:
{
    "id":         <uuid string>,
    "title":      <str>,
    "bs_year":    <int>,
    "bs_month":   <int>,
    "bs_day":     <int>,
    "description":<str>,
    "annual":     <bool>,   # if True, repeats every BS year
    "color":      <str>,    # optional hex colour
    "created":    <ISO-8601 UTC timestamp>
}
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any

_LOGGER = logging.getLogger(__name__)


class EventStore:
    """Manages reading and writing Nepali calendar events."""

    def __init__(self, hass_config_dir: str, filename: str = "nepali_events.json") -> None:
        self._path = os.path.join(hass_config_dir, filename)
        self._events: list[dict[str, Any]] = []
        self._lock = asyncio.Lock()

    # ── I/O ────────────────────────────────────────────────────────────────────

    async def async_load(self) -> None:
        """Load events from disk (non-blocking)."""
        async with self._lock:
            await asyncio.get_event_loop().run_in_executor(None, self._load_sync)

    def _load_sync(self) -> None:
        if not os.path.exists(self._path):
            self._events = []
            return
        try:
            with open(self._path, encoding="utf-8") as fh:
                data = json.load(fh)
            if not isinstance(data, list):
                _LOGGER.warning("nepali_events.json is malformed – resetting.")
                self._events = []
            else:
                self._events = data
        except (json.JSONDecodeError, OSError) as err:
            _LOGGER.error("Cannot read %s: %s", self._path, err)
            self._events = []

    async def async_save(self) -> None:
        """Persist events to disk (non-blocking)."""
        async with self._lock:
            await asyncio.get_event_loop().run_in_executor(None, self._save_sync)

    def _save_sync(self) -> None:
        try:
            with open(self._path, "w", encoding="utf-8") as fh:
                json.dump(self._events, fh, ensure_ascii=False, indent=2)
        except OSError as err:
            _LOGGER.error("Cannot write %s: %s", self._path, err)

    # ── CRUD ───────────────────────────────────────────────────────────────────

    def get_all(self) -> list[dict[str, Any]]:
        """Return a shallow copy of all events."""
        return list(self._events)

    def get_by_id(self, event_id: str) -> dict[str, Any] | None:
        for ev in self._events:
            if ev.get("id") == event_id:
                return dict(ev)
        return None

    def get_for_bs_date(self, bs_year: int, bs_month: int, bs_day: int,
                         include_annual: bool = True) -> list[dict[str, Any]]:
        """Return events matching a specific BS date.
        Annual events match on month+day regardless of year.
        """
        result = []
        for ev in self._events:
            if ev["bs_month"] == bs_month and ev["bs_day"] == bs_day:
                if ev["bs_year"] == bs_year:
                    result.append(dict(ev))
                elif include_annual and ev.get("annual", False):
                    result.append(dict(ev))
        return result

    def get_for_bs_month(self, bs_year: int, bs_month: int) -> list[dict[str, Any]]:
        """Return all events visible in a given BS month (exact + annual)."""
        result = []
        for ev in self._events:
            if ev["bs_month"] == bs_month:
                if ev["bs_year"] == bs_year or ev.get("annual", False):
                    result.append(dict(ev))
        return result

    async def async_add_event(
        self,
        title: str,
        bs_year: int,
        bs_month: int,
        bs_day: int,
        description: str = "",
        annual: bool = False,
        color: str = "",
    ) -> dict[str, Any]:
        """Create and persist a new event. Returns the created event dict."""
        event: dict[str, Any] = {
            "id":          str(uuid.uuid4()),
            "title":       title,
            "bs_year":     bs_year,
            "bs_month":    bs_month,
            "bs_day":      bs_day,
            "description": description,
            "annual":      annual,
            "color":       color,
            "created":     datetime.now(timezone.utc).isoformat(),
        }
        self._events.append(event)
        await self.async_save()
        return dict(event)

    async def async_update_event(self, event_id: str, **kwargs: Any) -> bool:
        """Update fields on an existing event. Returns True on success."""
        ALLOWED = {"title", "bs_year", "bs_month", "bs_day",
                   "description", "annual", "color"}
        for i, ev in enumerate(self._events):
            if ev.get("id") == event_id:
                for k, v in kwargs.items():
                    if k in ALLOWED:
                        self._events[i][k] = v
                await self.async_save()
                return True
        return False

    async def async_delete_event(self, event_id: str) -> bool:
        """Delete an event by ID. Returns True if it was found and removed."""
        before = len(self._events)
        self._events = [ev for ev in self._events if ev.get("id") != event_id]
        if len(self._events) < before:
            await self.async_save()
            return True
        return False

    # ── Helpers ────────────────────────────────────────────────────────────────

    @property
    def count(self) -> int:
        return len(self._events)

    def events_indexed_by_day(self, bs_year: int, bs_month: int) -> dict[int, list[dict]]:
        """Return {day: [events…]} for the given month (for calendar rendering)."""
        by_day: dict[int, list[dict]] = {}
        for ev in self.get_for_bs_month(bs_year, bs_month):
            day = ev["bs_day"]
            by_day.setdefault(day, []).append(ev)
        return by_day
