"""
date_utils.py – Nepali (BS/Bikram Sambat) ↔ Gregorian conversion.

Algorithm
---------
1.  A reference date anchors the two calendars:
        Gregorian 2024-04-14  =  BS 2081-Baisakh-1
2.  Any Gregorian date is converted by computing its day-offset from the
    reference, then walking forwards/backwards through the BS month-length
    table to land on the correct BS date.
3.  The reverse (BS → Gregorian) computes the day-offset from BS 2081-01-01
    and adds it to 2024-04-14.
"""

from __future__ import annotations

import datetime as dt
import nepali_datetime as ndt
from typing import NamedTuple

from .const import (
    BS_YEAR_DATA,
    BS_MIN_YEAR,
    BS_MAX_YEAR,
    NEPALI_MONTHS_ENG,
    NEPALI_MONTHS_NP,
    NEPALI_DAYS,
    NEPALI_DAYS_NP,
    NEPALI_NUMERALS,
    REFERENCE_GREGORIAN,
    REFERENCE_BS,
)


class NepaliDate(NamedTuple):
    year: int
    month: int  # 1-indexed (1 = Baisakh … 12 = Chaitra)
    day: int

    # ── convenient string representations ──────────────────────────────────────
    @property
    def month_name_eng(self) -> str:
        return NEPALI_MONTHS_ENG[self.month - 1]

    @property
    def month_name_np(self) -> str:
        return NEPALI_MONTHS_NP[self.month - 1]

    @property
    def year_np(self) -> str:
        year = str(self.year)  # e.g. "2081"
        return "".join(NEPALI_NUMERALS[int(digit)] for digit in year)

    def __str__(self) -> str:
        return f"{self.year_np} {self.month_name_np} {self.day}"

    def isoformat(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

    # ── factory from isoformat string ──────────────────────────────────────────
    @classmethod
    def fromisoformat(cls, s: str) -> "NepaliDate":
        parts = s.split("-")
        if len(parts) != 3:
            raise ValueError(f"Invalid BS date string: {s!r}")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))


# ── Internal helpers ────────────────────────────────────────────────────────────


def _days_in_bs_year(bs_year: int) -> int:
    """Total days in a BS year (sum of all 12 months)."""
    data = _get_year_data(bs_year)
    return sum(data)


def _get_year_data(bs_year: int) -> list[int]:
    """Return the 12-element month-length list for *bs_year*.
    Raises ValueError if year is out of range.
    """
    if bs_year not in BS_YEAR_DATA:
        raise ValueError(
            f"BS year {bs_year} is outside the supported range "
            f"({BS_MIN_YEAR}–{BS_MAX_YEAR}).  "
            f"Update  nepali_calendar_data.json  to extend coverage."
        )
    return BS_YEAR_DATA[bs_year]


def _bs_days_from_reference(bs_year: int, bs_month: int, bs_day: int) -> int:
    """Return the signed day-count from REFERENCE_BS to (bs_year, bs_month, bs_day).
    Positive = after reference, negative = before reference.
    """
    ref_year, ref_month, ref_day = REFERENCE_BS  # 2081, 1, 1

    # --- build total days from BS epoch (2000-01-01) for both dates -----------
    def _days_since_epoch(y: int, m: int, d: int) -> int:
        total = 0
        for yr in range(BS_MIN_YEAR, y):
            if yr in BS_YEAR_DATA:
                total += _days_in_bs_year(yr)
        months = _get_year_data(y)
        for mo in range(1, m):
            total += months[mo - 1]
        total += d - 1
        return total

    return _days_since_epoch(bs_year, bs_month, bs_day) - _days_since_epoch(
        ref_year, ref_month, ref_day
    )


# ── Public API ──────────────────────────────────────────────────────────────────


def nepali_from_gregorian(greg_date: dt.date) -> NepaliDate:
    """Convert a Gregorian date to its Bikram Sambat equivalent."""
    tndt = ndt.datetime.from_datetime_date(greg_date)
    return NepaliDate(tndt.date().year, tndt.date().month, tndt.date().day)


def gregorian_from_nepali(bs_year: int, bs_month: int, bs_day: int) -> dt.date:
    """Convert a Bikram Sambat date to its Gregorian equivalent."""
    return ndt.date(bs_year, bs_month, bs_day).to_datetime_date()


def today_nepali() -> NepaliDate:
    """Return today's date as a NepaliDate."""
    today = ndt.date.today()
    return NepaliDate(today.year, today.month, today.day)


def days_in_bs_month(bs_year: int, bs_month: int) -> int:
    """Return how many days are in (bs_year, bs_month)."""
    return _get_year_data(bs_year)[bs_month - 1]


def bs_day_of_week(bs_year: int, bs_month: int, bs_day: int) -> int:
    """Return ISO weekday (1=Monday … 7=Sunday) for a BS date."""
    greg = gregorian_from_nepali(bs_year, bs_month, bs_day)
    return greg.isoweekday()


def bs_day_of_week_name(
    bs_year: int, bs_month: int, bs_day: int, nepali: bool = False
) -> str:
    """Return the day-of-week name for a BS date."""
    dow = bs_day_of_week(bs_year, bs_month, bs_day)  # 1=Mon … 7=Sun
    # Our NEPALI_DAYS list is Sun-first (index 0 = Sunday)
    # ISO: 1=Mon, 7=Sun  →  convert to 0=Sun
    idx = dow % 7  # Mon=1→1, …, Sat=6→6, Sun=7→0
    if nepali:
        return NEPALI_DAYS_NP[idx]
    return NEPALI_DAYS[idx]


def first_weekday_of_month(bs_year: int, bs_month: int) -> int:
    """Return the weekday index (0=Sun, 6=Sat) of the 1st day of a BS month."""
    dow = ndt.date(bs_year, bs_month, 1).weekday()  # ISO 1-7
    return dow % 7  # 0=Sun … 6=Sat


def bs_month_calendar(bs_year: int, bs_month: int) -> list[list[int | None]]:
    """
    Return a list of weeks for a BS month.
    Each week is a 7-element list (Sun … Sat) of day numbers or None.
    """
    total_days = days_in_bs_month(bs_year, bs_month)
    start_weekday = first_weekday_of_month(bs_year, bs_month)  # 0=Sun

    weeks: list[list[int | None]] = []
    week: list[int | None] = [None] * start_weekday
    for day in range(1, total_days + 1):
        week.append(day)
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        while len(week) < 7:
            week.append(None)
        weeks.append(week)
    return weeks


def prev_bs_month(bs_year: int, bs_month: int) -> tuple[int, int]:
    if bs_month == 1:
        return bs_year - 1, 12
    return bs_year, bs_month - 1


def next_bs_month(bs_year: int, bs_month: int) -> tuple[int, int]:
    if bs_month == 12:
        return bs_year + 1, 1
    return bs_year, bs_month + 1


def validate_bs_date(bs_year: int, bs_month: int, bs_day: int) -> str | None:
    """Return an error string or None if the date is valid."""
    if bs_year not in BS_YEAR_DATA:
        return f"Year {bs_year} not in data table ({BS_MIN_YEAR}–{BS_MAX_YEAR})."
    if not (1 <= bs_month <= 12):
        return f"Month must be 1–12."
    max_day = BS_YEAR_DATA[bs_year][bs_month - 1]
    if not (1 <= bs_day <= max_day):
        return f"Day {bs_day} out of range (1–{max_day}) for {NEPALI_MONTHS_ENG[bs_month - 1]} {bs_year}."
    return None
