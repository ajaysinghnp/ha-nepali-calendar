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
  2000:[30,32,31,32,31,30,30,30,29,30,29,31],2001:[31,31,32,31,31,31,30,29,30,29,30,30],
  2002:[31,31,32,32,31,30,30,29,30,29,30,30],2003:[31,32,31,32,31,30,30,30,29,29,30,31],
  2004:[30,32,31,32,31,30,30,30,29,30,29,31],2005:[31,31,32,31,31,31,30,29,30,29,30,30],
  2006:[31,31,32,32,31,30,30,29,30,29,30,30],2007:[31,32,31,32,31,30,30,30,29,29,30,31],
  2008:[31,31,32,31,31,31,30,29,30,29,30,30],2009:[31,31,32,32,31,30,30,29,30,29,30,31],
  2010:[30,32,31,32,31,30,30,30,29,29,30,31],2011:[31,31,32,31,31,31,30,29,30,29,30,30],
  2012:[31,31,32,32,31,30,30,29,30,29,30,30],2013:[31,32,31,32,31,30,30,30,29,29,30,31],
  2014:[30,32,31,32,31,30,30,30,29,30,29,31],2015:[31,31,32,31,31,31,30,29,30,29,30,30],
  2016:[31,31,32,32,31,30,30,29,30,29,30,30],2017:[31,32,31,32,31,30,30,30,29,29,30,31],
  2018:[31,31,32,31,31,31,30,29,30,29,30,30],2019:[31,31,32,32,31,30,30,29,30,29,30,31],
  2020:[30,32,31,32,31,30,30,30,29,29,30,31],2021:[31,31,32,31,31,31,30,29,30,29,30,30],
  2022:[31,31,32,32,31,30,30,29,30,29,30,30],2023:[31,32,31,32,31,30,30,30,29,29,30,31],
  2024:[30,32,31,32,31,30,30,30,29,30,29,31],2025:[31,31,32,31,31,31,30,29,30,29,30,30],
  2026:[31,31,32,32,31,30,30,29,30,29,30,30],2027:[31,32,31,32,31,30,30,30,29,29,30,31],
  2028:[31,31,32,31,31,31,30,29,30,29,30,30],2029:[31,31,32,32,31,30,30,29,30,29,30,31],
  2030:[30,32,31,32,31,30,30,30,29,29,30,31],2031:[31,31,32,31,31,31,30,29,30,29,30,30],
  2032:[31,31,32,32,31,30,30,29,30,29,30,30],2033:[31,32,31,32,31,30,30,30,29,29,30,31],
  2034:[30,32,31,32,31,30,30,30,29,30,29,31],2035:[31,31,32,31,31,31,30,29,30,29,30,30],
  2036:[31,31,32,32,31,30,30,29,30,29,30,30],2037:[31,32,31,32,31,30,30,30,29,29,30,31],
  2038:[31,31,32,31,31,31,30,29,30,29,30,30],2039:[31,31,32,32,31,30,30,29,30,29,30,31],
  2040:[30,32,31,32,31,30,30,30,29,29,30,31],2041:[31,31,32,31,31,31,30,29,30,29,30,30],
  2042:[31,31,32,32,31,30,30,29,30,29,30,30],2043:[31,32,31,32,31,30,30,30,29,29,30,31],
  2044:[30,32,31,32,31,30,30,30,29,30,29,31],2045:[31,31,32,31,31,31,30,29,30,29,30,30],
  2046:[31,31,32,32,31,30,30,29,30,29,30,30],2047:[31,32,31,32,31,30,30,30,29,29,30,31],
  2048:[31,31,32,31,31,31,30,29,30,29,30,30],2049:[31,31,32,32,31,30,30,29,30,29,30,31],
  2050:[30,32,31,32,31,30,30,30,29,29,30,31],2051:[31,31,32,31,31,31,30,29,30,29,30,30],
  2052:[31,31,32,32,31,30,30,29,30,29,30,30],2053:[31,32,31,32,31,30,30,30,29,29,30,31],
  2054:[30,32,31,32,31,30,30,30,29,30,29,31],2055:[31,31,32,31,31,31,30,29,30,29,30,30],
  2056:[31,31,32,32,31,30,30,29,30,29,30,30],2057:[31,32,31,32,31,30,30,30,29,29,30,31],
  2058:[31,31,32,31,31,31,30,29,30,29,30,30],2059:[31,31,32,32,31,30,30,29,30,29,30,31],
  2060:[30,32,31,32,31,30,30,30,29,29,30,31],2061:[31,31,32,31,31,31,30,29,30,29,30,30],
  2062:[31,31,32,32,31,30,30,29,30,29,30,30],2063:[31,32,31,32,31,30,30,30,29,29,30,31],
  2064:[30,32,31,32,31,30,30,30,29,30,29,31],2065:[31,31,32,31,31,31,30,29,30,29,30,30],
  2066:[31,31,32,32,31,30,30,29,30,29,30,30],2067:[31,32,31,32,31,30,30,30,29,29,30,31],
  2068:[31,31,32,31,31,31,30,29,30,29,30,30],2069:[31,31,32,32,31,30,30,29,30,29,30,31],
  2070:[30,32,31,32,31,30,30,30,29,29,30,31],2071:[31,31,32,31,31,31,30,29,30,29,30,30],
  2072:[31,31,32,32,31,30,30,29,30,29,30,30],2073:[31,32,31,32,31,30,30,30,29,29,30,31],
  2074:[30,32,31,32,31,30,30,30,29,30,29,31],2075:[31,31,32,31,31,31,30,29,30,29,30,30],
  2076:[31,31,32,32,31,30,30,29,30,29,30,30],2077:[31,32,31,32,31,30,30,30,29,29,30,31],
  2078:[31,31,32,31,31,31,30,29,30,29,30,30],2079:[31,31,32,32,31,30,30,29,30,29,30,31],
  2080:[31,31,32,32,31,30,30,29,30,29,30,30],2081:[31,31,32,31,31,31,30,29,30,30,29,31],
  2082:[31,32,31,32,31,30,30,29,30,29,30,30],2083:[31,31,32,31,31,31,29,30,30,29,30,30],
  2084:[31,31,32,31,31,31,30,29,30,29,30,30],2085:[31,32,31,32,31,30,30,29,30,29,30,31],
  2086:[30,32,31,32,31,30,30,30,29,29,30,31],2087:[31,31,32,31,31,31,30,29,30,29,30,30],
  2088:[31,31,32,32,31,30,30,29,30,29,30,30],2089:[31,32,31,32,31,30,30,30,29,29,30,31],
  2090:[30,32,31,32,31,30,30,30,29,30,29,31],2091:[31,31,32,31,31,31,30,29,30,29,30,30],
  2092:[31,31,32,32,31,30,30,29,30,29,30,30],2093:[31,32,31,32,31,30,30,30,29,29,30,31],
  2094:[30,32,31,32,31,30,30,30,29,30,29,31],2095:[31,31,32,31,31,31,30,29,30,29,30,30],
  2096:[31,31,32,32,31,30,30,29,30,29,30,30],2097:[31,32,31,32,31,30,30,30,29,29,30,31],
  2098:[31,31,32,31,31,31,30,29,30,29,30,30],2099:[31,31,32,32,31,30,30,29,30,29,30,31],
  2100:[30,32,31,32,31,30,30,30,29,29,30,31],
};

const NEPALI_MONTHS    = ["Baisakh","Jestha","Ashadh","Shrawan","Bhadra","Ashwin","Kartik","Mangsir","Poush","Magh","Falgun","Chaitra"];
const NEPALI_MONTHS_NP = ["बैशाख","जेठ","असार","साउन","भदौ","आश्विन","कार्तिक","मंसिर","पौष","माघ","फाल्गुन","चैत"];
const WEEK_DAYS_EN     = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
const WEEK_DAYS_NP     = ["आइत","सोम","मंगल","बुध","बिही","शुक्र","शनि"];

// ── Reference: Gregorian 2024-04-14 = BS 2081-01-01 ──────────────────────────
const REF_GREG = new Date(2024, 3, 14); // month is 0-indexed
const REF_BS   = { year: 2081, month: 1, day: 1 };

// ── BS Math helpers ───────────────────────────────────────────────────────────
function daysInBsMonth(year, month) {
  const data = BS_YEAR_DATA[year];
  if (!data) return 30;
  return data[month - 1];
}

function gregToBS(date) {
  const msPerDay = 86400000;
  const delta    = Math.round((date - REF_GREG) / msPerDay);

  let { year, month, day } = REF_BS;
  let remaining = delta;

  if (remaining >= 0) {
    while (remaining > 0) {
      const dim  = daysInBsMonth(year, month);
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
  const refOffset  = daysSinceEpoch(REF_BS.year, REF_BS.month, REF_BS.day);
  const tgtOffset  = daysSinceEpoch(bsYear, bsMonth, bsDay);
  const delta      = tgtOffset - refOffset;
  const result     = new Date(REF_GREG);
  result.setDate(result.getDate() + delta);
  return result;
}

function todayBS() { return gregToBS(new Date()); }

function firstWeekdayOfBsMonth(year, month) {
  const g = bsToGreg(year, month, 1);
  return g.getDay(); // 0=Sun
}

// ══════════════════════════════════════════════════════════════════════════════
//  Custom Element
// ══════════════════════════════════════════════════════════════════════════════
class NepaliCalendarCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config   = {};
    this._hass     = null;
    this._today    = todayBS();
    this._viewYear  = this._today.year;
    this._viewMonth = this._today.month;
    this._events    = {};   // { "bsYear-bsMonth-bsDay": [eventObj, …] }
    this._dialog    = null;
  }

  // ── HA card protocol ────────────────────────────────────────────────────────
  static getConfigElement() { return document.createElement("nepali-calendar-card-editor"); }
  static getStubConfig()    { return { show_gregorian: true, highlight_weekends: true, language: "en" }; }

  setConfig(config) {
    this._config = {
      title:               config.title               ?? "Nepali Calendar",
      show_gregorian:      config.show_gregorian      ?? true,
      highlight_weekends:  config.highlight_weekends  ?? true,
      language:            config.language            ?? "en",
      primary_color:       config.primary_color       ?? "var(--primary-color)",
      weekend_color:       config.weekend_color       ?? "#e74c3c",
      today_color:         config.today_color         ?? "var(--accent-color, #ff9800)",
      event_color:         config.event_color         ?? "#27ae60",
      show_converter:      config.show_converter      ?? false,
      font_size:           config.font_size           ?? "14px",
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

  connectedCallback() {
    this._render();
    this._loadEventsFromApi();
    // Refresh at midnight
    const now = new Date();
    const msToMidnight = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1) - now;
    setTimeout(() => {
      this._today = todayBS();
      this._render();
      setInterval(() => { this._today = todayBS(); this._render(); }, 86400000);
    }, msToMidnight);
  }

  async _loadEventsFromApi() {
    if (!this._hass) return;
    try {
      // Fetch events via HA's calendar API endpoint
      const start = bsToGreg(this._viewYear, 1, 1);
      const end   = bsToGreg(this._viewYear, 12, 32 > daysInBsMonth(this._viewYear, 12)
        ? daysInBsMonth(this._viewYear, 12) : 31);
      const startStr = start.toISOString().slice(0, 10);
      const endStr   = end.toISOString().slice(0, 10);

      const resp = await this._hass.callApi(
        "GET",
        `calendars/calendar.nepali_events?start=${startStr}T00:00:00&end=${endStr}T23:59:59`
      );
      this._events = {};
      if (Array.isArray(resp)) {
        resp.forEach(ev => {
          const greg = new Date(ev.start.date || ev.start.dateTime);
          const bs   = gregToBS(greg);
          const key  = `${bs.year}-${bs.month}-${bs.day}`;
          (this._events[key] = this._events[key] || []).push({
            id:    ev.uid || "",
            title: ev.summary || "",
            desc:  ev.description || "",
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
    const c = this._config;
    const isNP = c.language === "np";
    const months   = isNP ? NEPALI_MONTHS_NP : NEPALI_MONTHS;
    const weekdays = isNP ? WEEK_DAYS_NP      : WEEK_DAYS_EN;

    const year  = this._viewYear;
    const month = this._viewMonth;
    const dim   = daysInBsMonth(year, month);
    const startWD = firstWeekdayOfBsMonth(year, month); // 0=Sun

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
          const isToday   = isCurrentMonth && day === td;
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
            } catch(_) {}
          }

          const dots = hasEvent
            ? `<span class="dots">${evts.slice(0,3).map(e =>
                `<span class="dot" title="${e.title}" style="background:${c.event_color}"></span>`
              ).join("")}</span>`
            : "";

          const cls = [
            "day-cell",
            isToday   ? "today"   : "",
            isWeekend ? "weekend" : "",
            hasEvent  ? "has-event" : "",
          ].filter(Boolean).join(" ");

          const style = isToday
            ? `background:${c.today_color};color:#fff;`
            : isWeekend
              ? `color:${c.weekend_color};`
              : "";

          return `<td class="${cls}" style="${style}" data-day="${day}">
            <span class="bs-day">${day}</span>
            ${gregLabel}
            ${dots}
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
          display: flex; align-items: center; justify-content: space-between;
          padding: 12px 16px;
          background: ${c.primary_color};
          color: #fff;
        }
        .card-header h2 { margin: 0; font-size: 1.1em; font-weight: 600; }
        .nav-btn {
          background: rgba(255,255,255,0.2); border: none; color: #fff;
          border-radius: 50%; width: 32px; height: 32px;
          cursor: pointer; font-size: 1.1em; display: flex; align-items: center; justify-content: center;
        }
        .nav-btn:hover { background: rgba(255,255,255,0.35); }
        .nav-center { text-align: center; }
        .nav-center .month-title { font-size: 1.2em; font-weight: 700; }
        .nav-center .year-title  { font-size: 0.85em; opacity: 0.85; }
        .today-btn {
          background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.4);
          color: #fff; border-radius: 12px; padding: 3px 10px; cursor: pointer; font-size: 0.8em;
        }
        table { width: 100%; border-collapse: collapse; }
        th { padding: 8px 4px; text-align: center; font-size: 0.78em; font-weight: 600;
             color: var(--secondary-text-color); }
        td { padding: 4px 2px; text-align: center; vertical-align: top;
             height: 48px; cursor: pointer; border-radius: 6px; transition: background 0.15s; }
        td:hover:not(:empty) { background: var(--secondary-background-color); }
        .day-cell { position: relative; }
        .bs-day { display: block; font-size: 1em; font-weight: 500; line-height: 1.4; }
        .greg { display: block; font-size: 0.65em; color: var(--secondary-text-color); line-height: 1; }
        .today .greg { color: rgba(255,255,255,0.75); }
        .dots { display: flex; justify-content: center; gap: 2px; margin-top: 2px; }
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
          <div class="nav-center">
            <div class="month-title">${months[month - 1]}</div>
            <div class="year-title">${year} BS</div>
          </div>
          <div style="display:flex;gap:6px;align-items:center;">
            <button class="today-btn" id="goto-today">${isNP ? "आज" : "Today"}</button>
            <button class="nav-btn" id="next-month">&#8250;</button>
          </div>
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
          <div class="conv-result" id="conv-g-result"></div>
        </div>
        <div>
          <label style="font-size:0.8em;color:var(--secondary-text-color);display:block;margin-bottom:4px;">BS → Gregorian</label>
          <div class="conv-row">
            <input id="conv-b-y" type="number" placeholder="Year" style="width:80px;" />
            <input id="conv-b-m" type="number" placeholder="Mo" style="width:60px;" min="1" max="12" />
            <input id="conv-b-d" type="number" placeholder="Day" style="width:60px;" min="1" max="32" />
            <button class="btn btn-primary" id="conv-b-btn">Convert</button>
          </div>
          <div class="conv-result" id="conv-b-result"></div>
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
      this._today = todayBS();
      this._viewYear  = this._today.year;
      this._viewMonth = this._today.month;
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

    // Converter
    root.getElementById("conv-g-btn")?.addEventListener("click", () => {
      const val = root.getElementById("conv-g-date")?.value;
      if (!val) return;
      const [y, m, d] = val.split("-").map(Number);
      const bs = gregToBS(new Date(y, m - 1, d));
      const mn = this._config.language === "np" ? NEPALI_MONTHS_NP[bs.month - 1] : NEPALI_MONTHS[bs.month - 1];
      root.getElementById("conv-g-result").innerHTML =
        `<strong>${bs.year} ${mn} ${bs.day}</strong>`;
    });
    root.getElementById("conv-b-btn")?.addEventListener("click", () => {
      const y = parseInt(root.getElementById("conv-b-y")?.value);
      const m = parseInt(root.getElementById("conv-b-m")?.value);
      const d = parseInt(root.getElementById("conv-b-d")?.value);
      if (!y || !m || !d) return;
      try {
        const g = bsToGreg(y, m, d);
        root.getElementById("conv-b-result").innerHTML =
          `<strong>${g.toISOString().slice(0,10)}</strong>`;
      } catch(e) {
        root.getElementById("conv-b-result").innerHTML = "Invalid date.";
      }
    });
  }

  // ── Day dialog ──────────────────────────────────────────────────────────────
  _openDayDialog(year, month, day) {
    const key  = `${year}-${month}-${day}`;
    const evts = this._events[key] || [];
    const isNP = this._config.language === "np";
    const mn   = isNP ? NEPALI_MONTHS_NP[month - 1] : NEPALI_MONTHS[month - 1];

    let gDateStr = "";
    try { gDateStr = bsToGreg(year, month, day).toISOString().slice(0, 10); } catch(_) {}

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
        <h3>${mn} ${day}, ${year} BS${gDateStr ? ` <span style="font-size:0.75em;font-weight:400;color:var(--secondary-text-color);">(${gDateStr})</span>` : ""}</h3>
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
      const title  = overlay.querySelector("#dlg-title").value.trim();
      if (!title) { overlay.querySelector("#dlg-title").focus(); return; }
      const desc   = overlay.querySelector("#dlg-desc").value.trim();
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
    } catch(e) {
      console.error("nepali-calendar-card: service call failed", e);
    }
  }
}

customElements.define("nepali-calendar-card", NepaliCalendarCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type:         "nepali-calendar-card",
  name:         "Nepali Calendar Card",
  description:  "A Bikram Sambat calendar with event management and date conversion.",
  preview:      true,
  documentationURL: "https://github.com/your-username/ha-nepali-calendar",
});

console.info(
  "%c NEPALI-CALENDAR-CARD %c v1.0.0 ",
  "background:#c0392b;color:#fff;font-weight:700;padding:2px 6px;border-radius:3px 0 0 3px;",
  "background:#222;color:#fff;padding:2px 6px;border-radius:0 3px 3px 0;"
);
