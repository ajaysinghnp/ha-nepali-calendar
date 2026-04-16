# 🇳🇵 Nepali Calendar – Home Assistant Custom Integration

A full-featured Bikram Sambat (BS/Nepali) calendar for Home Assistant.
Runs *alongside* the default Gregorian calendar — it does **not** replace it.

---

## Features

| Feature | Details |
|---|---|
| **Date sensor** | `sensor.nepali_date` – current BS date with rich attributes |
| **Calendar entity** | `calendar.nepali_events` – works with the default HA Calendar card |
| **Custom Lovelace card** | Monthly grid, Gregorian sub-dates, event dots, month nav, day-click dialog |
| **Event management** | Add / delete annual & one-off events via card UI or service calls |
| **Date conversion services** | `gregorian_to_nepali` and `nepali_to_gregorian` |
| **Embedded converter** | Optional converter panel right inside the Lovelace card |
| **Extensible data** | Override BS month-length data via a user-editable JSON file |

---

## Installation

### Method A – HACS (recommended)

1. Open HACS in your Home Assistant instance.
2. Click **Integrations → ⋮ → Custom repositories**.
3. Add `https://github.com/ajaysinghnp/ha-nepali-calendar` as an **Integration**.
4. Find "Nepali Calendar" and click **Download**.
5. Restart Home Assistant.
6. Go to **Settings → Devices & Services → Add Integration** and search for **Nepali Calendar**.

### Method B – Manual

```bash
# From your HA config directory:
mkdir -p custom_components/nepali_calendar
# Copy all files from custom_components/nepali_calendar/ here

mkdir -p www/nepali-calendar-card
# Copy www/nepali-calendar-card/nepali-calendar-card.js here
```

Restart Home Assistant, then add the integration via the UI.

---

## Lovelace Card Setup

### Automatic (preferred)
The integration tries to register the Lovelace resource automatically on startup.
If that succeeds, skip to "Adding the card".

### Manual resource registration
1. Go to **Settings → Dashboards → ⋮ → Resources**.
2. Click **+ Add resource**.
3. URL: `/local/nepali-calendar-card/nepali-calendar-card.js`
4. Type: **JavaScript module**
5. Click **Create**.
6. **Hard-refresh** your browser (Ctrl+Shift+R / Cmd+Shift+R).

### Adding the card
In any dashboard, click **+ Add card → Custom: Nepali Calendar Card**.

Or paste the YAML manually:

```yaml
type: custom:nepali-calendar-card
title: Nepali Calendar         # optional header override
show_gregorian: true           # show Gregorian day number below BS day
highlight_weekends: true       # colour Sunday/Saturday differently
language: en                   # "en" or "np" (Devanagari labels)
show_converter: true           # embed date-converter panel
primary_color: "#c0392b"       # header background
weekend_color: "#e74c3c"       # weekend text colour
today_color: "#ff9800"         # today cell background
event_color: "#27ae60"         # event dot colour
font_size: "14px"              # overall font size
```

---

## Sensor

`sensor.nepali_date` state: `"2081 Baisakh 15"`

### Attributes

| Attribute | Example |
|---|---|
| `bs_year` | `2081` |
| `bs_month` | `1` |
| `bs_day` | `15` |
| `bs_month_name` | `Baisakh` |
| `bs_month_name_np` | `बैशाख` |
| `bs_day_of_week` | `Sombar` |
| `gregorian_date` | `2024-04-28` |
| `days_in_month` | `31` |
| `isoformat` | `2081-01-15` |

### Template examples

```jinja2
{{ state_attr('sensor.nepali_date', 'bs_month_name') }} {{ state_attr('sensor.nepali_date', 'bs_day') }}, {{ state_attr('sensor.nepali_date', 'bs_year') }}
```

---

## Services

### `nepali_calendar.gregorian_to_nepali`

```yaml
service: nepali_calendar.gregorian_to_nepali
data:
  year: 2025
  month: 4
  day: 14
```

Fires event `nepali_calendar_conversion_result` on the HA event bus:
```json
{
  "direction": "gregorian_to_nepali",
  "input":  { "year": 2025, "month": 4, "day": 14 },
  "output": { "bs_year": 2082, "bs_month": 1, "bs_day": 1, "month_name": "Baisakh" }
}
```

---

### `nepali_calendar.nepali_to_gregorian`

```yaml
service: nepali_calendar.nepali_to_gregorian
data:
  bs_year: 2082
  bs_month: 1
  bs_day: 1
```

---

### `nepali_calendar.add_event`

```yaml
service: nepali_calendar.add_event
data:
  title: "Ram's Birthday"
  bs_year: 2081
  bs_month: 1
  bs_day: 10
  description: "Family gathering at home"
  annual: true          # repeat every year on Baisakh 10
  color: "#3498db"      # optional event colour
```

---

### `nepali_calendar.delete_event`

```yaml
service: nepali_calendar.delete_event
data:
  event_id: "550e8400-e29b-41d4-a716-446655440000"
```

Get event IDs by calling `nepali_calendar.list_events` and watching the `nepali_calendar_events_list` event in the HA event monitor (**Developer Tools → Events**).

---

### `nepali_calendar.list_events`

```yaml
service: nepali_calendar.list_events
data:
  bs_year: 2081    # optional
  bs_month: 1      # optional
```

---

## Automation Examples

### Morning greeting with BS date

```yaml
automation:
  alias: "Good morning – Nepali date"
  trigger:
    - platform: time
      at: "06:00:00"
  action:
    - service: notify.mobile_app_my_phone
      data:
        title: "Subha Prabhat! 🙏"
        message: >
          आज {{ state_attr('sensor.nepali_date', 'bs_month_name_np') }}
          {{ state_attr('sensor.nepali_date', 'bs_day') }},
          {{ state_attr('sensor.nepali_date', 'bs_year') }} हो।
```

### Birthday reminder

```yaml
automation:
  alias: "Nepali birthday reminder"
  trigger:
    - platform: time
      at: "07:00:00"
  condition:
    - condition: template
      value_template: >
        {{ state_attr('sensor.nepali_date', 'bs_month') == 1 and
           state_attr('sensor.nepali_date', 'bs_day') == 10 }}
  action:
    - service: notify.notify
      data:
        message: "Today is Ram's birthday! 🎂"
```

---

## Updating the BS Calendar Data

The integration ships with data from **BS 2000 to BS 2100**.

To override or extend (e.g. after Nepal's official calendar publishes new month lengths):

1. Create `<HA config dir>/nepali_calendar_data.json`:

```json
{
  "2101": [31, 31, 32, 31, 31, 30, 30, 29, 30, 29, 30, 30],
  "2102": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]
}
```

Each key is a BS year (string); each value is a 12-element array of day counts for Baisakh through Chaitra.

2. Restart Home Assistant.

The integration merges your JSON on top of the built-in table at startup.

---

## Event Storage

Events are stored in `<HA config dir>/nepali_events.json`.
You can back this file up or edit it manually (restart HA after manual edits).

```json
[
  {
    "id": "550e8400-...",
    "title": "Ram's Birthday",
    "bs_year": 2081,
    "bs_month": 1,
    "bs_day": 10,
    "description": "Family gathering",
    "annual": true,
    "color": "#3498db",
    "created": "2024-04-28T10:00:00+00:00"
  }
]
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Card not found | Add the JS resource manually (see above) and hard-refresh |
| "Year not in data table" | Your date is beyond the built-in range – add it via `nepali_calendar_data.json` |
| Events not showing | Check logs for errors; verify `nepali_events.json` is writable |
| Wrong BS date | The reference date is **Gregorian 2024-04-14 = BS 2081-01-01**. If you believe there is a data error, update `nepali_calendar_data.json` |

---

## File Structure

```
custom_components/nepali_calendar/
├── __init__.py          – integration setup, service registration
├── calendar.py          – calendar.nepali_events entity
├── config_flow.py       – UI config flow
├── const.py             – constants, BS year data table
├── date_utils.py        – BS ↔ Gregorian conversion engine
├── event_store.py       – JSON event persistence
├── manifest.json        – HACS/HA manifest
├── sensor.py            – sensor.nepali_date entity
├── services.yaml        – service schema definitions
└── strings.json         – UI strings

www/nepali-calendar-card/
└── nepali-calendar-card.js   – Lovelace custom card

hacs.json                – HACS metadata
README.md
```

---

## Accuracy Note

The BS calendar is astronomical and managed by the Government of Nepal's Department of Calendar, Astrology and Forecasting.
Month lengths can be adjusted by official decree.
This integration uses a well-established reference table; for critical applications always verify against [www.ashesh.com.np](https://www.ashesh.com.np) or official Nepali government publications.

---

## License

MIT © ajaysinghnp
