"""sensor.py – sensor.nepali_date entity."""

from __future__ import annotations

import datetime as dt

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change

from .date_utils import (
    bs_day_of_week,
    today_nepali,
    days_in_bs_month,
    bs_day_of_week_name,
    gregorian_from_nepali,
)

from .const import (
    ATTR_BS_DATE_ENG,
    ATTR_BS_DAY_ENG,
    ATTR_BS_YEAR_ENG,
    ATTR_CURRENT_GREGORIAN_MONTH_NP,
    ATTR_GREGORIAN_DATE,
    ATTR_GREGORIAN_DATE_ENG,
    ATTR_GREGORIAN_DATE_NP,
    ATTR_BS_DATE_SHORT,
    ATTR_GREGORIAN_DATE_SHORT,
    ATTR_GREGORIAN_DAY,
    ATTR_GREGORIAN_DAY_NP,
    ATTR_GREGORIAN_MONTH,
    ATTR_GREGORIAN_MONTH_NP,
    ATTR_GREGORIAN_MONTHS_SPAN_NP,
    ATTR_GREGORIAN_WEEKDAY,
    ATTR_GREGORIAN_WEEKDAY_NP,
    ATTR_GREGORIAN_YEAR,
    ATTR_GREGORIAN_YEAR_NP,
    ATTR_BS_MONTH_ENG,
    ATTR_BS_MONTH_NUMBER,
    ATTR_GREGORIAN_MONTHS_SPAN,
    ATTR_CURRENT_GREGORIAN_MONTH,
    ATTR_DAYS_IN_BS_MONTH,
    ATTR_STARTING_WEEKDAY,
    ATTR_STARTING_WEEKDAY_NP,
    ATTR_STARTING_WEEKDAY_ENG,
    ATTR_WEEKDAY,
    ATTR_WEEKDAY_ENG,
    ATTR_WEEKDAY_NP,
    DAYS_ENG,
    ENGLISH_MONTHS_NP,
    NEPALI_DAYS_NP,
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
            ATTR_BS_DATE_ENG: f"{self._bs.year} {self._bs.month_name_eng} {self._bs.day}",
            ATTR_GREGORIAN_DATE: f"{tdt.year}-{tdt.month:02d}-{tdt.day:02d}",
            ATTR_GREGORIAN_DATE_NP: _gregorian_date_np(tdt),
            ATTR_BS_DATE_SHORT: f"{self._bs.year_np}-{_to_nepali_digits(self._bs.month, 2)}-{_to_nepali_digits(self._bs.day, 2)}",
            ATTR_GREGORIAN_DATE_SHORT: f"{tdt.month:02d} {tdt.day:02d} {tdt.year}",
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
            ATTR_BS_YEAR_ENG: self._bs.year,
            ATTR_GREGORIAN_YEAR: today.year,
            ATTR_GREGORIAN_YEAR_NP: _to_nepali_digits(today.year),
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

        return {
            ATTR_BS_MONTH_ENG: bs.month_name_eng,
            ATTR_BS_MONTH_NUMBER: bs.month,
            ATTR_GREGORIAN_MONTHS_SPAN: month_span,
            ATTR_GREGORIAN_MONTHS_SPAN_NP: f"{ENGLISH_MONTHS_NP[start_greg.month - 1]}/{ENGLISH_MONTHS_NP[end_greg.month - 1]}",
            ATTR_CURRENT_GREGORIAN_MONTH: dt.date.today().strftime("%B"),
            ATTR_CURRENT_GREGORIAN_MONTH_NP: ENGLISH_MONTHS_NP[
                dt.date.today().month - 1
            ],
            ATTR_DAYS_IN_BS_MONTH: dim,
            ATTR_STARTING_WEEKDAY: bs_day_of_week_name(bs.year, bs.month, 1),
            ATTR_STARTING_WEEKDAY_NP: bs_day_of_week_name(bs.year, bs.month, 1, True),
            ATTR_STARTING_WEEKDAY_ENG: DAYS_ENG[bs_day_of_week(bs.year, bs.month, 1)],
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
            ATTR_BS_DAY_ENG: bs.day,
            ATTR_WEEKDAY: bs_day_of_week_name(bs.year, bs.month, bs.day),
            ATTR_WEEKDAY_NP: bs_day_of_week_name(bs.year, bs.month, bs.day, True),
            ATTR_WEEKDAY_ENG: DAYS_ENG[bs_day_of_week(bs.year, bs.month, bs.day)],
            ATTR_GREGORIAN_DAY: greg.day,
            ATTR_GREGORIAN_DAY_NP: _to_nepali_digits(greg.day),
        }


class NepaliGregorianDateSensor(_BaseNepaliSensor):
    _attr_unique_id = "nepali_calendar_gregorian_date"
    _attr_name = "Gregorian Date"
    _attr_icon = "mdi:calendar-clock"

    @property
    def native_value(self) -> str:
        return _gregorian_date_np(dt.date.today())

    @property
    def extra_state_attributes(self) -> dict:
        greg = dt.date.today()
        return {
            ATTR_GREGORIAN_DATE_ENG: greg.isoformat(),
            ATTR_GREGORIAN_WEEKDAY: greg.strftime("%A"),
            ATTR_GREGORIAN_WEEKDAY_NP: NEPALI_DAYS_NP[(greg.weekday() + 1) % 7],  # noqa: F821
            ATTR_GREGORIAN_MONTH: greg.strftime("%B"),
            ATTR_GREGORIAN_MONTH_NP: ENGLISH_MONTHS_NP[greg.month - 1],
        }
