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

ENGLISH_MONTHS_NP = [
    "जनवरी",
    "फेब्रुअरी",
    "मार्च",
    "अप्रिल",
    "मई",
    "जून",
    "जुलाई",
    "अगस्त",
    "सितम्बर",
    "अक्टूबर",
    "नवम्बर",
    "दिसम्बर",
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

DAYS_ENG = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

# ── Reference date ─────────────────────────────────────────────────────────────
# Gregorian 1992-06-30  ↔  BS 2049-03-16  (Asar 16, 2049)

# Attribute names
ATTR_BS_DATE_ENG = "bs_date_eng"
ATTR_GREGORIAN_DATE = "gregorian_date"
ATTR_GREGORIAN_DATE_NP = "gregorian_date_np"
ATTR_BS_DATE_SHORT = "bs_date_short"
ATTR_GREGORIAN_DATE_SHORT = "gregorian_date_short"

# Year-related attributes
ATTR_BS_YEAR_ENG = "bs_year_eng"
ATTR_GREGORIAN_YEAR = "gregorian_year"
ATTR_GREGORIAN_YEAR_NP = "gregorian_year_np"

# Month-related attributes
ATTR_BS_MONTH_ENG = "bs_month_eng"
ATTR_BS_MONTH_NUMBER = "bs_month_number"
ATTR_GREGORIAN_MONTHS_SPAN = "gregorian_months_span"
ATTR_GREGORIAN_MONTHS_SPAN_NP = "gregorian_months_span_np"
ATTR_CURRENT_GREGORIAN_MONTH = "current_gregorian_month"
ATTR_CURRENT_GREGORIAN_MONTH_NP = "current_gregorian_month_np"
ATTR_DAYS_IN_BS_MONTH = "days_in_bs_month"
ATTR_STARTING_WEEKDAY = "starting_weekday"
ATTR_STARTING_WEEKDAY_NP = "starting_weekday_np"
ATTR_STARTING_WEEKDAY_ENG = "starting_weekday_eng"

# Day-related attributes
ATTR_BS_DAY_ENG = "bs_day_eng"
ATTR_WEEKDAY = "weekday"
ATTR_WEEKDAY_NP = "weekday_np"
ATTR_WEEKDAY_ENG = "weekday_eng"
ATTR_GREGORIAN_DAY = "gregorian_day"
ATTR_GREGORIAN_DAY_NP = "gregorian_day_np"

# Gregorian Week and Month attributes
ATTR_GREGORIAN_DATE_ENG = "gregorian_date_eng"
ATTR_GREGORIAN_WEEKDAY = "gregorian_weekday"
ATTR_GREGORIAN_WEEKDAY_NP = "gregorian_weekday_np"
ATTR_GREGORIAN_MONTH = "gregorian_month"
ATTR_GREGORIAN_MONTH_NP = "gregorian_month_np"

# Service names
SERVICE_GREGORIAN_TO_NEPALI = "ad2bs"
SERVICE_NEPALI_TO_GREGORIAN = "bs2ad"
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
