"""Constants for the Nepali Calendar integration."""

DOMAIN = "nepali_calendar"
PLATFORM_SENSOR = "sensor"
PLATFORM_CALENDAR = "calendar"

NEPALI_NUMERALS = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]


# --- Names ---
NEPALI_MONTHS_ENG = [
    "Baisakh",
    "Jestha",
    "Ashadh",
    "Shrawan",
    "Bhadra",
    "Ashwin",
    "Kartik",
    "Mangsir",
    "Poush",
    "Magh",
    "Falgun",
    "Chaitra",
]

NEPALI_MONTHS_NP = [
    "बैशाख",
    "जेठ",
    "असार",
    "साउन",
    "भदौ",
    "आश्विन",
    "कार्तिक",
    "मंसिर",
    "पौष",
    "माघ",
    "फाल्गुन",
    "चैत",
]

NEPALI_DAYS = [
    "Aaitabar",
    "Sombar",
    "Mangalbar",
    "Budhbar",
    "Bihibar",
    "Sukrabar",
    "Sanibar",
]

NEPALI_DAYS_NP = [
    "आइतबार",
    "सोमबार",
    "मंगलबार",
    "बुधबार",
    "बिहीबार",
    "शुक्रबार",
    "शनिबार",
]

# ── Reference date ─────────────────────────────────────────────────────────────
# Gregorian 1992-06-30  ↔  BS 2049-03-16  (Asar 16, 2049)

# Attribute names
ATTR_BS_YEAR_ENG = "bs_year_eng"
ATTR_BS_YEAR_NP = "bs_year_np"
ATTR_BS_MONTH = "bs_month"
ATTR_BS_DAY = "bs_day"
ATTR_BS_MONTH_NAME = "bs_month_name"
ATTR_BS_MONTH_NAME_NP = "bs_month_name_np"
ATTR_BS_DAY_OF_WEEK = "bs_day_of_week"
ATTR_BS_DAY_OF_WEEK_NP = "bs_day_of_week_np"
ATTR_GREGORIAN_DATE = "gregorian_date"
ATTR_DAYS_IN_MONTH = "days_in_month"

# Service names
SERVICE_GREGORIAN_TO_NEPALI = "gregorian_to_nepali"
SERVICE_NEPALI_TO_GREGORIAN = "nepali_to_gregorian"
SERVICE_ADD_EVENT = "add_event"
SERVICE_DELETE_EVENT = "delete_event"
SERVICE_LIST_EVENTS = "list_events"

# Storage
EVENTS_FILE = "nepali_events.json"

# Config keys
CONF_SHOW_GREGORIAN = "show_gregorian"
CONF_HIGHLIGHT_WEEKENDS = "highlight_weekends"
CONF_LANGUAGE = "language"
CONF_PRIMARY_COLOR = "primary_color"
CONF_WEEKEND_COLOR = "weekend_color"
CONF_TODAY_COLOR = "today_color"
CONF_EVENT_COLOR = "event_color"
