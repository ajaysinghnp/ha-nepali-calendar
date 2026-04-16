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

import datetime
from typing import NamedTuple

from .const import (
    BS_YEAR_DATA,
    BS_MIN_YEAR,
    BS_MAX_YEAR,
    NEPALI_MONTHS,
    NEPALI_MONTHS_NP,
    NEPALI_DAYS,
    NEPALI_DAYS_NP,
    REFERENCE_GREGORIAN,
    REFERENCE_BS,
)


class NepaliDate(NamedTuple):
    year: int
    month: int   # 1-indexed (1 = Baisakh … 12 = Chaitra)
    day: int

    # ── convenient string representations ──────────────────────────────────────
    @property
    def month_name(self) -> str:
        return NEPALI_MONTHS[self.month - 1]

    @property
    def month_name_np(self) -> str:
        return NEPALI_MONTHS_NP[self.month - 1]

    def __str__(self) -> str:
        return f"{self.year} {self.month_name} {self.day}"

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

    return _days_since_epoch(bs_year, bs_month, bs_day) - \
           _days_since_epoch(ref_year, ref_month, ref_day)


# ── Public API ──────────────────────────────────────────────────────────────────

def nepali_from_gregorian(greg_date: datetime.date) -> NepaliDate:
    """Convert a Gregorian date to its Bikram Sambat equivalent."""
    ref_greg = datetime.date(*REFERENCE_GREGORIAN)           # 2024-04-14
    delta = (greg_date - ref_greg).days                      # signed offset

    ref_year, ref_month, ref_day = REFERENCE_BS             # 2081, 1, 1

    bs_year  = ref_year
    bs_month = ref_month
    bs_day   = ref_day

    if delta >= 0:
        # walk forward
        remaining = delta
        while remaining > 0:
            days_this_month = _get_year_data(bs_year)[bs_month - 1]
            days_left_in_month = days_this_month - bs_day
            if remaining <= days_left_in_month:
                bs_day += remaining
                remaining = 0
            else:
                remaining -= (days_left_in_month + 1)
                bs_day = 1
                bs_month += 1
                if bs_month > 12:
                    bs_month = 1
                    bs_year += 1
    else:
        # walk backward
        remaining = -delta
        while remaining > 0:
            if remaining < bs_day:
                bs_day -= remaining
                remaining = 0
            else:
                remaining -= bs_day
                bs_month -= 1
                if bs_month < 1:
                    bs_month = 12
                    bs_year -= 1
                bs_day = _get_year_data(bs_year)[bs_month - 1]

    return NepaliDate(bs_year, bs_month, bs_day)


def gregorian_from_nepali(bs_year: int, bs_month: int, bs_day: int) -> datetime.date:
    """Convert a Bikram Sambat date to its Gregorian equivalent."""
    # validate
    if bs_year not in BS_YEAR_DATA:
        raise ValueError(f"BS year {bs_year} not in data table.")
    month_data = _get_year_data(bs_year)
    if not (1 <= bs_month <= 12):
        raise ValueError(f"BS month must be 1–12, got {bs_month}.")
    max_day = month_data[bs_month - 1]
    if not (1 <= bs_day <= max_day):
        raise ValueError(
            f"BS day {bs_day} is out of range for {NEPALI_MONTHS[bs_month-1]} "
            f"{bs_year} (1–{max_day})."
        )

    day_offset = _bs_days_from_reference(bs_year, bs_month, bs_day)
    ref_greg = datetime.date(*REFERENCE_GREGORIAN)
    return ref_greg + datetime.timedelta(days=day_offset)


def today_nepali() -> NepaliDate:
    """Return today's date as a NepaliDate."""
    return nepali_from_gregorian(datetime.date.today())


def days_in_bs_month(bs_year: int, bs_month: int) -> int:
    """Return how many days are in (bs_year, bs_month)."""
    return _get_year_data(bs_year)[bs_month - 1]


def bs_day_of_week(bs_year: int, bs_month: int, bs_day: int) -> int:
    """Return ISO weekday (1=Monday … 7=Sunday) for a BS date."""
    greg = gregorian_from_nepali(bs_year, bs_month, bs_day)
    return greg.isoweekday()


def bs_day_of_week_name(bs_year: int, bs_month: int, bs_day: int,
                         nepali: bool = False) -> str:
    """Return the day-of-week name for a BS date."""
    dow = bs_day_of_week(bs_year, bs_month, bs_day)  # 1=Mon … 7=Sun
    # Our NEPALI_DAYS list is Sun-first (index 0 = Sunday)
    # ISO: 1=Mon, 7=Sun  →  convert to 0=Sun
    idx = dow % 7   # Mon=1→1, …, Sat=6→6, Sun=7→0
    if nepali:
        return NEPALI_DAYS_NP[idx]
    return NEPALI_DAYS[idx]


def first_weekday_of_month(bs_year: int, bs_month: int) -> int:
    """Return the weekday index (0=Sun, 6=Sat) of the 1st day of a BS month."""
    dow = bs_day_of_week(bs_year, bs_month, 1)   # ISO 1-7
    return dow % 7  # 0=Sun … 6=Sat


def bs_month_calendar(bs_year: int, bs_month: int) -> list[list[int | None]]:
    """
    Return a list of weeks for a BS month.
    Each week is a 7-element list (Sun … Sat) of day numbers or None.
    """
    total_days    = days_in_bs_month(bs_year, bs_month)
    start_weekday = first_weekday_of_month(bs_year, bs_month)   # 0=Sun

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
        return f"Day {bs_day} out of range (1–{max_day}) for {NEPALI_MONTHS[bs_month-1]} {bs_year}."
    return None
