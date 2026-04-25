"""sensor.py – sensor.nepali_date entity."""

from __future__ import annotations

import datetime as dt

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change

from .date_utils import (
    today_nepali,
    days_in_bs_month,
    bs_day_of_week_name,
    gregorian_from_nepali,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            NepaliDateSensor(hass),
            NepaliYearSensor(hass),
            NepaliMonthSensor(hass),
            NepaliDaySensor(hass),
            NepaliGregorianDateSensor(hass),
        ],
        update_before_add=True,
    )


def _to_nepali_digits(value: int | str, pad: bool | int = False) -> str:
    digits = "०१२३४५६७८९"
    trans = str.maketrans("0123456789", digits)
    if pad is True:
        pad = 2
    return str(value).zfill(pad).translate(trans)


def _gregorian_date_np(greg_date: dt.date) -> str:
    return (
        f"{_to_nepali_digits(greg_date.year, 4)}-"
        f"{_to_nepali_digits(f'{greg_date.month:02d}', 2)}-"
        f"{_to_nepali_digits(f'{greg_date.day:02d}', 2)}"
    )


class _BaseNepaliSensor(SensorEntity):
    """Shared behavior for Nepali date-derived sensors."""

    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._bs = today_nepali()
        self._unsub = None

    async def async_added_to_hass(self) -> None:
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

    async def _async_midnight_refresh(self, _now: dt.datetime) -> None:
        self._bs = today_nepali()
        self.async_write_ha_state()

    def update(self) -> None:
        self._bs = today_nepali()


class NepaliDateSensor(_BaseNepaliSensor):
    """Sensor showing the current Nepali (BS) date."""

    _attr_unique_id = "nepali_calendar_today"
    _attr_name = "Nepali Date"
    _attr_icon = "mdi:calendar-today"

    @property
    def native_value(self) -> str:
        return f"{self._bs.year_np} {self._bs.month_name_np} {_to_nepali_digits(self._bs.day)}"

    @property
    def extra_state_attributes(self) -> dict:
        tdt = dt.date.today()
        return {
            "bs_date_eng": f"{self._bs.year} {self._bs.month_name_eng} {self._bs.day}",
            "gregorian_date": f"{tdt.year}-{tdt.month:02d}-{tdt.day:02d}",
            "gregorian_date_np": _gregorian_date_np(tdt),
            "bs_date_short": f"{self._bs.year_np}-{_to_nepali_digits(self._bs.month, 2)}-{_to_nepali_digits(self._bs.day, 2)}",
            "gregorian_date_short": f"{tdt.month:02d} {tdt.day:02d} {tdt.year}",
        }


class NepaliYearSensor(_BaseNepaliSensor):
    _attr_unique_id = "nepali_calendar_year"
    _attr_name = "BS Year"
    _attr_icon = "mdi:numeric"

    @property
    def native_value(self) -> str:
        return self._bs.year_np

    @property
    def extra_state_attributes(self) -> dict:
        today = dt.date.today()
        return {
            "bs_year_eng": self._bs.year,
            "gregorian_year": today.year,
            "gregorian_year_np": _to_nepali_digits(today.year),
        }


class NepaliMonthSensor(_BaseNepaliSensor):
    _attr_unique_id = "nepali_calendar_month"
    _attr_name = "BS Month"
    _attr_icon = "mdi:calendar-month"

    @property
    def native_value(self) -> str:
        return self._bs.month_name_np

    @property
    def extra_state_attributes(self) -> dict:
        bs = self._bs
        dim = days_in_bs_month(bs.year, bs.month)
        start_greg = gregorian_from_nepali(bs.year, bs.month, 1)
        end_greg = gregorian_from_nepali(bs.year, bs.month, dim)
        if start_greg.month == end_greg.month:
            month_span = start_greg.strftime("%B")
        else:
            month_span = f"{start_greg.strftime('%B')}/{end_greg.strftime('%B')}"

        today = dt.date.today()
        return {
            "bs_month_eng": bs.month_name_eng,
            "bs_month_number": bs.month,
            "gregorian_months_span": month_span,
            "current_gregorian_month": today.strftime("%B"),
            "days_in_bs_month": dim,
            "starting_weekday": bs_day_of_week_name(bs.year, bs.month, 1),
            "starting_weekday_np": bs_day_of_week_name(bs.year, bs.month, 1, True),
        }


class NepaliDaySensor(_BaseNepaliSensor):
    _attr_unique_id = "nepali_calendar_day"
    _attr_name = "BS Day"
    _attr_icon = "mdi:calendar-today"

    @property
    def native_value(self) -> str:
        return _to_nepali_digits(self._bs.day)

    @property
    def extra_state_attributes(self) -> dict:
        bs = self._bs
        greg = dt.date.today()
        return {
            "bs_day_eng": bs.day,
            "weekday": bs_day_of_week_name(bs.year, bs.month, bs.day),
            "weekday_np": bs_day_of_week_name(bs.year, bs.month, bs.day, True),
            "gregorian_day": greg.day,
            "gregorian_day_np": _to_nepali_digits(greg.day),
        }


class NepaliGregorianDateSensor(_BaseNepaliSensor):
    _attr_unique_id = "nepali_calendar_gregorian_date"
    _attr_name = "Gregorian Date (NP)"
    _attr_icon = "mdi:calendar-clock"

    @property
    def native_value(self) -> str:
        return _gregorian_date_np(dt.date.today())

    @property
    def extra_state_attributes(self) -> dict:
        greg = dt.date.today()
        return {
            "gregorian_date_eng": greg.isoformat(),
            "gregorian_weekday": greg.strftime("%A"),
            "gregorian_month": greg.strftime("%B"),
        }
