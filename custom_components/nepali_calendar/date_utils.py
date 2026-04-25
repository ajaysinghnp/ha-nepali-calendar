"""
date_utils.py – Nepali (BS/Bikram Sambat) ↔ Gregorian conversion.

This module intentionally delegates calendar math to `nepali_datetime` so the
library remains the single source of truth for BS/Gregorian conversion and BS
date validation.
"""

from __future__ import annotations

import datetime as dt
import nepali_datetime as ndt
from typing import NamedTuple

from .const import (
    NEPALI_MONTHS_ENG,
    NEPALI_MONTHS_NP,
    NEPALI_DAYS,
    NEPALI_DAYS_NP,
    NEPALI_NUMERALS,
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


# ── Public API ──────────────────────────────────────────────────────────────────


def nepali_from_gregorian(greg_date: dt.date) -> NepaliDate:
    """Convert a Gregorian date to its Bikram Sambat equivalent."""
    tndt = ndt.date.from_datetime_date(greg_date)
    return NepaliDate(tndt.year, tndt.month, tndt.day)


def gregorian_from_nepali(bs_year: int, bs_month: int, bs_day: int) -> dt.date:
    """Convert a Bikram Sambat date to its Gregorian equivalent."""
    return ndt.date(bs_year, bs_month, bs_day).to_datetime_date()


def today_nepali() -> NepaliDate:
    """Return today's date as a NepaliDate."""
    today = ndt.date.today()
    return NepaliDate(today.year, today.month, today.day)


def days_in_bs_month(bs_year: int, bs_month: int) -> int:
    """Return how many days are in (bs_year, bs_month)."""
    start = ndt.date(bs_year, bs_month, 1).to_datetime_date()
    if bs_year == ndt.date.max.year and bs_month == ndt.date.max.month:
        return ndt.date.max.day
    if bs_month == 12:
        next_month = ndt.date(bs_year + 1, 1, 1).to_datetime_date()
    else:
        next_month = ndt.date(bs_year, bs_month + 1, 1).to_datetime_date()
    return (next_month - start).days


def bs_day_of_week(bs_year: int, bs_month: int, bs_day: int) -> int:
    """Return weekday index (0=Sun … 6=Sat) for a BS date."""
    return (ndt.date(bs_year, bs_month, bs_day).weekday() + 1) % 7


def bs_day_of_week_name(
    bs_year: int, bs_month: int, bs_day: int, nepali: bool = False
) -> str:
    """Return the day-of-week name for a BS date."""
    idx = bs_day_of_week(bs_year, bs_month, bs_day)
    if nepali:
        return NEPALI_DAYS_NP[idx]
    return NEPALI_DAYS[idx]


def first_weekday_of_month(bs_year: int, bs_month: int) -> int:
    """Return the weekday index (0=Sun, 6=Sat) of the 1st day of a BS month."""
    return bs_day_of_week(bs_year, bs_month, 1)


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
    try:
        ndt.date(bs_year, bs_month, bs_day)
    except ValueError as err:
        if not (1 <= bs_month <= 12):
            return "Month must be 1–12."
        if not (1 <= bs_day <= 32):
            return f"Day {bs_day} is out of range for {NEPALI_MONTHS_ENG[bs_month - 1]} {bs_year}."
        return str(err.args[0]) if err.args else str(err)
    return None
