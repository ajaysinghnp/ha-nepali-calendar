/**
 * nepali-calendar-card.js
 * Lovelace custom card for the Nepali (Bikram Sambat) Calendar integration.
 *
 * Features:
 *  • Monthly grid with BS day numbers
 *  • Optional Gregorian sub-dates
 *  • Today highlight, weekend highlight
 *  • Event dots with tooltip
 *  • Month navigation (prev/next/today)
 *  • Click on a day → event management dialog (add / view / delete)
 *  • Date converter panel embedded in the card
 *  • Nepali & English month/day names
 *  • Fully customisable via card YAML config
 */

// ══════════════════════════════════════════════════════════════════════════════
//  BS Calendar Data (mirrors const.py — must be kept in sync)
// ══════════════════════════════════════════════════════════════════════════════
const BS_YEAR_DATA = {
  2000: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2001: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2002: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2003: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2004: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2005: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2006: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2007: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2008: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2009: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2010: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2011: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2012: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2013: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2014: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2015: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2016: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2017: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2018: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2019: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2020: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2021: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2022: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2023: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2024: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2025: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2026: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2027: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2028: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2029: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2030: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2031: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2032: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2033: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2034: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2035: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2036: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2037: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2038: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2039: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2040: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2041: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2042: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2043: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2044: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2045: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2046: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2047: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2048: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2049: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2050: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2051: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2052: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2053: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2054: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2055: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2056: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2057: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2058: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2059: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2060: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2061: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2062: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2063: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2064: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2065: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2066: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2067: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2068: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2069: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2070: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2071: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2072: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2073: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2074: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2075: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2076: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2077: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2078: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2079: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2080: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2081: [31, 31, 32, 31, 31, 31, 30, 29, 30, 30, 29, 31],
  2082: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2083: [31, 31, 32, 31, 31, 31, 29, 30, 30, 29, 30, 30],
  2084: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2085: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2086: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2087: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2088: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2089: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2090: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2091: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2092: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2093: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2094: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2095: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
  2096: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2097: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
  2098: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2099: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 31],
  2100: [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
};

const NEPALI_MONTHS = ["Baisakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin", "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"];
const NEPALI_MONTHS_NP = ["बैशाख", "जेठ", "असार", "साउन", "भदौ", "आश्विन", "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुन", "चैत"];
const ENGLISH_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const ENGLISH_MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const ENGLISH_MONTHS_NP = ["जनवरी", "फरवरी", "मार्च", "अप्रिल", "मई", "जून", "जुलाई", "अगस्त", "सितम्बर", "अक्टूबर", "नवम्बर", "दिसम्बर"];
const WEEK_DAYS_EN = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const WEEK_DAYS_EN_FULL = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const WEEK_DAYS_NP = ["आइत", "सोम", "मंगल", "बुध", "बिही", "शुक्र", "शनि"];
const WEEK_DAYS_NP_FULL = ["आइतबार", "सोमबार", "मंगलबार", "बुधबार", "बिहीबार", "शुक्रबार", "शनिबार"];
const NEPALI_DIGITS = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"];

// ── Reference: Gregorian 2024-04-14 = BS 2081-01-01 ──────────────────────────
const REF_GREG = new Date(1992, 6, 30); // month is 0-indexed
const REF_BS = { year: 2049, month: 6, day: 30 };

// ── BS Math helpers ───────────────────────────────────────────────────────────
function daysInBsMonth(year, month) {
  const data = BS_YEAR_DATA[year];
  if (!data) return 30;
  return data[month - 1];
}

function gregToBS(date) {
  const msPerDay = 86400000;
  const delta = Math.round((date - REF_GREG) / msPerDay);

  let { year, month, day } = REF_BS;
  let remaining = delta;

  if (remaining >= 0) {
    while (remaining > 0) {
      const dim = daysInBsMonth(year, month);
      const left = dim - day;
      if (remaining <= left) { day += remaining; remaining = 0; }
      else { remaining -= left + 1; day = 1; month++; if (month > 12) { month = 1; year++; } }
    }
  } else {
    remaining = -remaining;
    while (remaining > 0) {
      if (remaining < day) { day -= remaining; remaining = 0; }
      else { remaining -= day; month--; if (month < 1) { month = 12; year--; } day = daysInBsMonth(year, month); }
    }
  }
  return { year, month, day };
}

function bsToGreg(bsYear, bsMonth, bsDay) {
  // compute day offset from reference BS date
  const MIN_YEAR = 2000;
  function daysSinceEpoch(y, m, d) {
    let total = 0;
    for (let yr = MIN_YEAR; yr < y; yr++) {
      if (BS_YEAR_DATA[yr]) BS_YEAR_DATA[yr].forEach(v => total += v);
    }
    const months = BS_YEAR_DATA[y] || [];
    for (let mo = 1; mo < m; mo++) total += months[mo - 1] || 30;
    return total + d - 1;
  }
  const refOffset = daysSinceEpoch(REF_BS.year, REF_BS.month, REF_BS.day);
  const tgtOffset = daysSinceEpoch(bsYear, bsMonth, bsDay);
  const delta = tgtOffset - refOffset;
  const result = new Date(REF_GREG);
  result.setDate(result.getDate() + delta);
  return result;
}

function firstWeekdayOfBsMonth(year, month) {
  const g = bsToGreg(year, month, 1);
  return g.getDay(); // 0=Sun
}

function formatNumber(value, useNepaliDigits) {
  if (!value) return "";
  const text = String(value);
  if (!useNepaliDigits) return text;
  let res = text.replace(/\d/g, (digit) => NEPALI_DIGITS[Number(digit)]);
  return res;
}

// ══════════════════════════════════════════════════════════════════════════════
//  Custom Element
// ══════════════════════════════════════════════════════════════════════════════
class NepaliCalendarCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
    this._hass = null;
    this._today = this._getTodayBSFromHA();
    this._viewYear = this._today?.year;
    this._viewMonth = this._today?.month;
    this._events = {};   // { "bsYear-bsMonth-bsDay": [eventObj, …] }
    this._dialog = null;
    this._resizeObserver = null;
  }

  // ── HA card protocol ────────────────────────────────────────────────────────
  static getConfigElement() { return document.createElement("nepali-calendar-card-editor"); }
  static getStubConfig() { return { show_gregorian: true, highlight_weekends: true, language: "np" }; }

  setConfig(config) {
    this._config = {
      title: config.title ?? "Nepali Calendar",
      show_gregorian: config.show_gregorian ?? true,
      highlight_weekends: config.highlight_weekends ?? true,
      language: config.language ?? "np",
      primary_color: config.primary_color ?? "var(--primary-color)",
      weekend_color: config.weekend_color ?? "#e74c3c",
      today_color: config.today_color ?? "var(--accent-color, #08ff0073)",
      event_color: config.event_color ?? "#27ae60",
      show_converter: config.show_converter ?? false,
      font_size: config.font_size ?? "14px",
      ...config,
    };
  }

  set hass(hass) {
    this._hass = hass;
    // pull events from HA calendar entity state attributes (if exposed)
    this._syncEventsFromHass(hass);
    if (!this.shadowRoot.innerHTML) this._render();
  }

  getCardSize() { return 6; }

  // ── Event sync ─────────────────────────────────────────────────────────────
  _syncEventsFromHass(hass) {
    // Events come from HA as calendar events; we rebuild our lookup map
    // by listening to "nepali_calendar_event_added/deleted" bus events
    // (the card uses fetch against HA API to load events once)
  }

  _getWeekdayLabels(isNP) {
    const useFullNames = this._getAvailableWidth() >= 430;
    if (isNP) {
      return useFullNames ? WEEK_DAYS_NP_FULL : WEEK_DAYS_NP;
    }
    return useFullNames ? WEEK_DAYS_EN_FULL : WEEK_DAYS_EN;
  }

  _getAvailableWidth() {
    return this.getBoundingClientRect().width || this.clientWidth || 0;
  }

  async _convertUsingService(serviceName, payload) {
    if (!this._hass) throw new Error("Home Assistant is not connected");

    const result = await this._hass.connection.sendMessagePromise({
      type: "call_service",
      domain: "nepali_calendar",
      service: serviceName,
      service_data: payload,
      return_response: true,
    });

    const response = result?.response ?? result?.service_response ?? null;
    if (!response) {
      throw new Error(`No response from service nepali_calendar.${serviceName}`);
    }

    return response.output ?? response;
  }

  //update the date components when ha dates updated
  _updateTodayFromHass() {
    if (!this._hass) return;
    this._viewYear = this._today?.year;
    this._viewMonth = this._today?.month;
  }

  // Get today's BS date from Home Assistant sensor instead of calculating locally
  _getTodayBSFromHA() {
    if (!this._hass) {
      console.warn("NepaliCalendarCard: Home Assistant not connected, cannot get today's date from sensor");
      return null;
    }
    const year = this._hass.states['sensor.bs_year'];
    const month = this._hass.states['sensor.bs_month'];
    const day = this._hass.states['sensor.bs_day'];

    return {
      year: year?.attributes?.bs_year_eng,
      month: month?.attributes?.bs_month_number,
      day: day?.attributes?.bs_day_eng,
    };
  }

  connectedCallback() {
    this._today = this._getTodayBSFromHA();
    this._updateTodayFromHass();
    console.debug("NepaliCalendarCard connected, today's BS date:", this._today);
    this._loadEventsFromApi();
    this._render();

    if (!this._resizeObserver && typeof ResizeObserver !== "undefined") {
      this._resizeObserver = new ResizeObserver(() => {
        this._render();
      });
      this._resizeObserver.observe(this);
    }

    // Listen to sensor.nepali_date state changes instead of calculating at midnight
    if (this._hass) {
      this._hass.connection.subscribeMessage(
        (msg) => {
          if (msg.type === 'state_changed' &&
            msg.data?.entity_id === 'sensor.nepali_date') {
            this._today = this._getTodayBSFromHA();
            this._updateTodayFromHass();
            this._render();
          }
        },
        { type: 'subscribe_events', event_type: 'state_changed' }
      );
    }
  }

  disconnectedCallback() {
    if (this._resizeObserver) {
      this._resizeObserver.disconnect();
      this._resizeObserver = null;
    }
  }

  async _loadEventsFromApi() {
    if (!this._hass) return;
    try {
      // Fetch events via HA's calendar API endpoint
      const start = bsToGreg(this._viewYear, 1, 1);
      const end = bsToGreg(this._viewYear, 12, 32 > daysInBsMonth(this._viewYear, 12)
        ? daysInBsMonth(this._viewYear, 12) : 31);
      const startStr = start.toISOString().slice(0, 10);
      const endStr = end.toISOString().slice(0, 10);

      const resp = await this._hass.callApi(
        "GET",
        `calendars/calendar.nepali_events?start=${startStr}T00:00:00&end=${endStr}T23:59:59`
      );

      this._events = {};
      if (Array.isArray(resp)) {
        resp.forEach(ev => {
          const greg = new Date(ev.start.date || ev.start.dateTime);
          const bs = gregToBS(greg);
          const key = `${bs.year}-${bs.month}-${bs.day}`;
          (this._events[key] = this._events[key] || []).push({
            id: ev.uid || "",
            title: ev.summary || "",
            desc: ev.description || "",
          });
        });
      }
      this._render();
    } catch (e) {
      console.warn("nepali-calendar-card: could not load events", e);
    }
  }

  // ── Rendering ───────────────────────────────────────────────────────────────
  _render() {
    if (!this._today) {
      this.shadowRoot.innerHTML = `<ha-card><div style="padding:16px;">Unable to determine today's date. Please ensure the "sensor.nepali_date" sensor is available and configured correctly.</div></ha-card>`;
      return;
    }
    const c = this._config;
    const isNP = c.language === "np";
    const months = isNP ? NEPALI_MONTHS_NP : NEPALI_MONTHS;
    const weekdays = this._getWeekdayLabels(isNP);

    const year = this._viewYear;
    const month = this._viewMonth;
    const dim = daysInBsMonth(year, month);
    const startWD = firstWeekdayOfBsMonth(year, month) - 1; // 0=Sun

    const { year: ty, month: tm, day: td } = this._today;
    const isCurrentMonth = (year === ty && month === tm);

    // Build grid rows
    let cells = [];
    for (let i = 0; i < startWD; i++) cells.push(null);
    for (let d = 1; d <= dim; d++) cells.push(d);
    while (cells.length % 7 !== 0) cells.push(null);

    const rows = [];
    for (let i = 0; i < cells.length; i += 7) rows.push(cells.slice(i, i + 7));

    const gridHTML = rows.map(row => `
      <tr>
        ${row.map((day, col) => {
      if (!day) return "<td></td>";
      const isToday = isCurrentMonth && day === td;
      const isWeekend = (col === 0 || col === 6) && c.highlight_weekends;
      const key = `${year}-${month}-${day}`;
      const evts = this._events[key] || [];
      const hasEvent = evts.length > 0;

      // Compute Gregorian date
      let gregLabel = "";
      if (c.show_gregorian) {
        try {
          const g = bsToGreg(year, month, day);
          gregLabel = `<span class="greg">${g.getDate()}</span>`;
        } catch (_) { }
      }

      const dots = hasEvent
        ? `<span class="dots">${evts.slice(0, 3).map(e =>
          `<span class="dot" title="${e.title}" style="background:${c.event_color}"></span>`
        ).join("")}</span>`
        : "";

      const cls = [
        "day-cell",
        isToday ? "today" : "",
        isWeekend ? "weekend" : "",
        hasEvent ? "has-event" : "",
      ].filter(Boolean).join(" ");

      const style = isToday
        ? `background:${c.today_color};color:#fff;`
        : isWeekend
          ? `color:${c.weekend_color};`
          : "";

      return `<td class="${cls}" style="${style}" data-day="${day}">
            <div class="day-content">
              <span class="bs-day">${formatNumber(day, isNP)}</span>
              <div class="day-footer">
                ${dots}
                ${gregLabel}
              </div>
            </div>
          </td>`;
    }).join("")}
      </tr>
    `).join("");

    const weekdayHeaders = weekdays.map((wd, i) => {
      const isWE = (i === 0 || i === 6) && c.highlight_weekends;
      return `<th style="${isWE ? `color:${c.weekend_color};` : ""}">${wd}</th>`;
    }).join("");

    const converterHTML = c.show_converter ? this._converterHTML() : "";

    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; font-size: ${c.font_size}; }
        ha-card { padding: 0; overflow: hidden; }
        .card-header {
          display: grid;
          grid-template-columns: auto minmax(0, 1fr) auto;
          align-items: center;
          justify-items: center;
          gap: 10px;
          padding: 8px 10px;
          background: ${c.primary_color};
          color: #fff;
        }
        .nav-btn {
          background: rgba(255,255,255,0.2); border: none; color: #fff;
          border-radius: 50%; width: 30px; height: 30px;
          cursor: pointer; font-size: 1.05em; display: flex; align-items: center; justify-content: center;
        }
        .nav-btn:hover { background: rgba(255,255,255,0.35); }
        .header-center {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 10px;
          min-width: 0;
          white-space: nowrap;
        }
        .month-title { font-size: 1.02em; font-weight: 700; text-align: center; white-space: nowrap; }
        .year-title  { font-size: 0.92em; font-weight: 600; opacity: 0.9; text-align: center; white-space: nowrap; }
        .today-btn {
          background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.4);
          color: #fff; border-radius: 12px; padding: 3px 9px; cursor: pointer; font-size: 0.8em;
          white-space: nowrap;
        }
        table { width: 100%; border-collapse: collapse; }
        th { padding: 8px 4px; text-align: center; font-size: 0.78em; font-weight: 600;
             color: var(--secondary-text-color); }
        td { padding: 6px 4px; text-align: center; vertical-align: top;
             height: 48px; cursor: pointer; border-radius: 6px; transition: background 0.15s; }
        td:hover:not(:empty) { background: var(--secondary-background-color); }
        .day-cell { position: relative; }
        .day-content {
          height: 100%;
          min-height: 42px;
          display: grid;
          grid-template-rows: 1fr auto;
        }
        .bs-day {
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 1.44em;
          font-weight: 600;
          line-height: 1;
          align-self: center;
        }
        .day-footer {
          display: flex;
          align-items: flex-end;
          justify-content: space-between;
          min-height: 14px;
          gap: 4px;
          padding-top: 1px;
        }
        .greg {
          display: block;
          margin-left: auto;
          font-size: 0.72em;
          color: var(--secondary-text-color);
          line-height: 1;
          text-align: right;
        }
        .today .greg { color: rgba(255,255,255,0.75); }
        .dots { display: flex; justify-content: flex-start; gap: 2px; }
        .dot { width: 5px; height: 5px; border-radius: 50%; }
        .has-event .bs-day::after { content: ""; display: inline-block;
          width: 4px; height: 4px; border-radius: 50%;
          background: ${c.event_color}; margin-left: 3px; vertical-align: middle; }
        /* Dialog */
        .dialog-overlay {
          position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 9000;
          display: flex; align-items: center; justify-content: center;
        }
        .dialog {
          background: var(--card-background-color);
          border-radius: 12px; padding: 24px; min-width: 320px; max-width: 400px;
          box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .dialog h3 { margin: 0 0 16px; font-size: 1.1em; }
        .dialog input, .dialog textarea, .dialog select {
          width: 100%; box-sizing: border-box; margin-bottom: 10px;
          padding: 8px 10px; border-radius: 6px; border: 1px solid var(--divider-color);
          background: var(--secondary-background-color);
          color: var(--primary-text-color); font-size: 0.9em;
        }
        .dialog textarea { height: 64px; resize: vertical; }
        .dialog label { font-size: 0.8em; color: var(--secondary-text-color); display: block; margin-bottom: 2px; }
        .dialog-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 8px; }
        .btn { padding: 8px 18px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.9em; }
        .btn-primary { background: ${c.primary_color}; color: #fff; }
        .btn-danger  { background: #e74c3c; color: #fff; }
        .btn-cancel  { background: var(--secondary-background-color);
                       color: var(--primary-text-color); }
        .event-list { margin: 8px 0 12px; }
        .event-item { display: flex; align-items: center; gap: 8px;
                      padding: 6px 8px; background: var(--secondary-background-color);
                      border-radius: 6px; margin-bottom: 4px; }
        .event-item .ev-title { flex: 1; font-size: 0.9em; }
        .event-item .del-btn { background: none; border: none; cursor: pointer;
                               color: #e74c3c; font-size: 1.1em; }
        /* Converter */
        .converter { padding: 16px; border-top: 1px solid var(--divider-color); }
        .converter h3 { margin: 0 0 12px; font-size: 1em; font-weight: 600;
                        color: var(--primary-text-color); }
        .conv-row { display: flex; gap: 8px; align-items: flex-end; }
        .conv-row input { flex: 1; padding: 7px 8px; border-radius: 6px;
                          border: 1px solid var(--divider-color);
                          background: var(--secondary-background-color);
                          color: var(--primary-text-color); font-size: 0.9em; }
        .conv-result { margin-top: 8px; font-size: 0.9em; color: var(--secondary-text-color); }
        .conv-result strong { color: var(--primary-text-color); }
      </style>

      <ha-card>
        <div class="card-header">
          <button class="nav-btn" id="prev-month">&#8249;</button>
          <div class="header-center">
            ${isNP ? `<div class="year-title">बिक्रम संवत् ${formatNumber(year, isNP)}</div>` : `<div class="year-title">${formatNumber(year, isNP)} A.D.</div>`}
            <div class="month-title">${months[month - 1]}</div>
            <button class="today-btn" id="goto-today">${isNP ? "आज" : "Today"}</button>
          </div>
          <button class="nav-btn" id="next-month">&#8250;</button>
        </div>

        <div style="padding:8px 12px 12px;">
          <table>
            <thead><tr>${weekdayHeaders}</tr></thead>
            <tbody id="cal-body">${gridHTML}</tbody>
          </table>
        </div>

        ${converterHTML}
      </ha-card>
    `;

    this._attachListeners();
  }

  _converterHTML() {
    return `
      <div class="converter">
        <h3>📅 Date Converter</h3>
        <div style="margin-bottom:10px;">
          <label style="font-size:0.8em;color:var(--secondary-text-color);display:block;margin-bottom:4px;">Gregorian → BS</label>
          <div class="conv-row">
            <input id="conv-g-date" type="date" placeholder="YYYY-MM-DD" />
            <button class="btn btn-primary" id="conv-g-btn" style="white-space:nowrap;">Convert</button>
          </div>
          <div class="conv-result">${this._config.language === "np" ? "बिक्रम संवत्" : "Bikram Sambat"}: <span id="conv-g-result"></span></div>
        </div>
        <div>
          <label style="font-size:0.8em;color:var(--secondary-text-color);display:block;margin-bottom:4px;">BS → Gregorian</label>
          <div class="conv-row">
            <input id="conv-b-y" type="number" placeholder="Year" style="width:80px;" />
            <input id="conv-b-m" type="number" placeholder="Mo" style="width:60px;" min="1" max="12" />
            <input id="conv-b-d" type="number" placeholder="Day" style="width:60px;" min="1" max="32" />
            <button class="btn btn-primary" id="conv-b-btn">Convert</button>
          </div>
          <div class="conv-result">${this._config.language === "np" ? "ईश्वी" : "Ishwi Sambat"}: <span id="conv-b-result"></span></div>
        </div>
      </div>`;
  }

  _attachListeners() {
    const root = this.shadowRoot;

    // Navigation
    root.getElementById("prev-month")?.addEventListener("click", () => {
      if (this._viewMonth === 1) { this._viewMonth = 12; this._viewYear--; }
      else this._viewMonth--;
      this._render();
      this._loadEventsFromApi();
    });
    root.getElementById("next-month")?.addEventListener("click", () => {
      if (this._viewMonth === 12) { this._viewMonth = 1; this._viewYear++; }
      else this._viewMonth++;
      this._render();
      this._loadEventsFromApi();
    });
    root.getElementById("goto-today")?.addEventListener("click", () => {
      this._today = this._getTodayBSFromHA();
      this._updateTodayFromHass();
      this._render();
      this._loadEventsFromApi();
    });

    // Day click
    root.querySelectorAll("td.day-cell").forEach(td => {
      td.addEventListener("click", () => {
        const day = parseInt(td.dataset.day);
        if (!isNaN(day)) this._openDayDialog(this._viewYear, this._viewMonth, day);
      });
    });

    // Converter ad2bs
    root.getElementById("conv-g-btn")?.addEventListener("click", async () => {
      const val = root.getElementById("conv-g-date")?.value;
      if (!val) return;
      const [y, m, d] = val.split("-").map(Number);
      const isNP = this._config.language === "np";
      try {
        const out = await this._convertUsingService("ad2bs", {
          year: y,
          month: m,
          day: d,
        });

        if (!out) throw new Error("No conversion output");

        const monthIndex = Number(out.bs_month) - 1;
        const mn = this._config.language === "np"
          ? (NEPALI_MONTHS_NP[monthIndex] || out.month_name_np || "")
          : (NEPALI_MONTHS[monthIndex] || out.month_name || "");

        root.getElementById("conv-g-result").innerHTML = `<strong>${formatNumber(out.bs_year, isNP)} ${mn} ${formatNumber(out.bs_day, isNP)}</strong>`;
      } catch (e) {
        root.getElementById("conv-g-result").innerHTML = "Conversion failed.";
      }
    });

    // Converter bs2ad
    root.getElementById("conv-b-btn")?.addEventListener("click", async () => {
      const y = parseInt(root.getElementById("conv-b-y")?.value);
      const m = parseInt(root.getElementById("conv-b-m")?.value);
      const d = parseInt(root.getElementById("conv-b-d")?.value);
      if (!y || !m || !d) return;
      try {
        const out = await this._convertUsingService("bs2ad", {
          bs_year: y,
          bs_month: m,
          bs_day: d,
        });

        if (!out) throw new Error("No conversion output");

        root.getElementById("conv-b-result").innerHTML = this._config.language === "np"
          ? `<strong>${ENGLISH_MONTHS_NP[out.month - 1] || ""} ${formatNumber(out.day, true)}, ${formatNumber(out.year, true)}</strong>`
          : `<strong>${ENGLISH_MONTHS[out.month - 1] || ""} ${formatNumber(out.day)}, ${formatNumber(out.year)}</strong>`;
      } catch (e) {
        root.getElementById("conv-b-result").innerHTML = "Conversion failed.";
      }
    });
  }

  // ── Day dialog ──────────────────────────────────────────────────────────────
  _openDayDialog(year, month, day) {
    const key = `${year}-${month}-${day}`;
    const evts = this._events[key] || [];
    const isNP = this._config.language === "np";
    const mn = isNP ? NEPALI_MONTHS_NP[month - 1] : NEPALI_MONTHS[month - 1];

    let gDateStr = "";
    try { gDateStr = bsToGreg(year, month, day).toISOString().slice(0, 10); } catch (_) { }

    const eventListHTML = evts.length
      ? `<div class="event-list">${evts.map(e => `
          <div class="event-item">
            <span class="ev-title">🗓 ${e.title}</span>
            <button class="del-btn" data-id="${e.id}" title="Delete">✕</button>
          </div>`).join("")}</div>`
      : `<p style="font-size:0.85em;color:var(--secondary-text-color);margin:4px 0 12px;">No events on this day.</p>`;

    const overlay = document.createElement("div");
    overlay.className = "dialog-overlay";
    overlay.innerHTML = `
      <div class="dialog">
        <h3>${mn} ${formatNumber(day, isNP)}, ${formatNumber(year, isNP)} BS${gDateStr ? ` <span style="font-size:0.75em;font-weight:400;color:var(--secondary-text-color);">(${gDateStr})</span>` : ""}</h3>
        ${eventListHTML}
        <hr style="border:none;border-top:1px solid var(--divider-color);margin:12px 0;">
        <label>Add Event</label>
        <input id="dlg-title" placeholder="Event title" />
        <textarea id="dlg-desc" placeholder="Description (optional)"></textarea>
        <label style="display:flex;align-items:center;gap:6px;margin-bottom:10px;cursor:pointer;">
          <input type="checkbox" id="dlg-annual" style="width:auto;margin:0;">
          <span style="font-size:0.85em;">Repeat annually</span>
        </label>
        <div class="dialog-actions">
          <button class="btn btn-cancel" id="dlg-cancel">Cancel</button>
          <button class="btn btn-primary" id="dlg-save">Add Event</button>
        </div>
      </div>`;

    this.shadowRoot.appendChild(overlay);

    overlay.querySelector("#dlg-cancel").onclick = () => overlay.remove();
    overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };

    overlay.querySelector("#dlg-save").onclick = async () => {
      const title = overlay.querySelector("#dlg-title").value.trim();
      if (!title) { overlay.querySelector("#dlg-title").focus(); return; }
      const desc = overlay.querySelector("#dlg-desc").value.trim();
      const annual = overlay.querySelector("#dlg-annual").checked;
      await this._callService("add_event", {
        title, bs_year: year, bs_month: month, bs_day: day,
        description: desc, annual,
      });
      overlay.remove();
      await this._loadEventsFromApi();
    };

    overlay.querySelectorAll(".del-btn").forEach(btn => {
      btn.onclick = async () => {
        const id = btn.dataset.id;
        if (!id) return;
        await this._callService("delete_event", { event_id: id });
        overlay.remove();
        await this._loadEventsFromApi();
      };
    });
  }

  async _callService(service, data) {
    if (!this._hass) return;
    try {
      await this._hass.callService("nepali_calendar", service, data);
    } catch (e) {
      console.error("nepali-calendar-card: service call failed", e);
    }
  }
}

customElements.define("nepali-calendar-card", NepaliCalendarCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "nepali-calendar-card",
  name: "Nepali Calendar Card",
  description: "A Bikram Sambat calendar with event management and date conversion.",
  preview: true,
  documentationURL: "https://github.com/ajaysinghnp/ha-nepali-calendar",
});

console.info(
  "%c NEPALI-CALENDAR-CARD %c v0.2.3",
  "background:#c0392b;color:#fff;font-weight:700;padding:2px 6px;border-radius:3px 0 0 3px;",
  "background:#222;color:#fff;padding:2px 6px;border-radius:0 3px 3px 0;"
);


// End of nepali-calendar-card.js
