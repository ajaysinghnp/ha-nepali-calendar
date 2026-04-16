"""sensor.py – sensor.nepali_date entity."""

from __future__ import annotations

import datetime
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change

from .const import (
    DOMAIN,
    ATTR_BS_YEAR,
    ATTR_BS_MONTH,
    ATTR_BS_DAY,
    ATTR_BS_MONTH_NAME,
    ATTR_BS_MONTH_NAME_NP,
    ATTR_BS_DAY_OF_WEEK,
    ATTR_GREGORIAN_DATE,
    ATTR_DAYS_IN_MONTH,
    NEPALI_DAYS,
)
from .date_utils import (
    today_nepali,
    days_in_bs_month,
    bs_day_of_week,
    bs_day_of_week_name,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([NepaliDateSensor(hass)], update_before_add=True)


class NepaliDateSensor(SensorEntity):
    """Sensor showing the current Nepali (BS) date."""

    _attr_unique_id     = "nepali_calendar_today"
    _attr_name          = "Nepali Date"
    _attr_icon          = "mdi:calendar-today"
    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._bs   = today_nepali()
        self._unsub = None

    async def async_added_to_hass(self) -> None:
        """Register midnight refresh."""
        self._unsub = async_track_time_change(
            self._hass,
            self._async_midnight_refresh,
            hour=0,
            minute=0,
            second=5,
        )

    async def async_will_remove_from_hass(self) -> None:
        if self._unsub:
            self._unsub()

    async def _async_midnight_refresh(self, _now: datetime.datetime) -> None:
        self._bs = today_nepali()
        self.async_write_ha_state()

    def update(self) -> None:
        self._bs = today_nepali()

    @property
    def state(self) -> str:
        return str(self._bs)   # e.g. "2081 Baisakh 15"

    @property
    def extra_state_attributes(self) -> dict:
        bs = self._bs
        greg = datetime.date.today()
        dow = bs_day_of_week(bs.year, bs.month, bs.day)
        return {
            ATTR_BS_YEAR:         bs.year,
            ATTR_BS_MONTH:        bs.month,
            ATTR_BS_DAY:          bs.day,
            ATTR_BS_MONTH_NAME:   bs.month_name,
            ATTR_BS_MONTH_NAME_NP: bs.month_name_np,
            ATTR_BS_DAY_OF_WEEK:  bs_day_of_week_name(bs.year, bs.month, bs.day),
            ATTR_GREGORIAN_DATE:  greg.isoformat(),
            ATTR_DAYS_IN_MONTH:   days_in_bs_month(bs.year, bs.month),
            "isoformat":          bs.isoformat(),
        }
