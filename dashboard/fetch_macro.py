#!/usr/bin/env python3
"""Fetch current values for the macro indicators that have a keyless public API.

Writes data/macro-snapshot.csv. Run on a schedule from .github/workflows/pages.yml;
the committed snapshot accumulates into a history of what the macro environment
looked like over the life of the project.

    python3 dashboard/fetch_macro.py

Design rules, in priority order:

1. NEVER break the build. Any fetch can fail - APIs go down, formats drift,
   rate limits bite. A failed fetch keeps the previous value and marks the row
   stale. The script exits 0 unless it cannot write the file at all.
2. NEVER silently show a stale number. Every row carries the observation date
   from the source (as_of) and when we fetched it (fetched_at), and the
   dashboard renders staleness as prominently as the value.
3. Only sources that need no API key. A key would have to live in repo secrets,
   which makes the build unreproducible for anyone else and adds a rotation
   burden to a research project.

Python 3 stdlib only, same as build.py.
"""

import csv
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "macro-snapshot.csv")
HISTORY = os.path.join(ROOT, "data", "macro-history.csv")

# Years of history kept for the charts. Also sets how far back sources are asked
# to go, so every series covers the same window.
HISTORY_YEARS = 12

TIMEOUT = 30
UA = "sustainable-finance-venture/1.0 (+https://github.com/benbaichmankass/sustainable-finance-venture)"

FIELDS = [
    "ID", "Label", "Value", "Unit", "As_Of",
    "Chg_1m", "Chg_3m", "Chg_12m", "Direction",
    "Fetched_At", "Status", "Source_URL", "Note",
]


# --- fetch helpers -----------------------------------------------------------

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fred_csv(series):
    """FRED's graph CSV endpoint is keyless. Returns [(date, float)] ascending.

    `cosd` is passed explicitly. Without it the endpoint serves whatever window
    that series' default graph happens to use - which is the full history for
    some series and about three years for others, silently. That produced a
    12-year chart for the fed funds rate next to a 3-year one for EM spreads,
    with nothing to indicate the axes weren't comparable.
    """
    start = date.today().year - HISTORY_YEARS - 1
    url = ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s&cosd=%d-01-01"
           % (series, start))
    rows = []
    for row in csv.DictReader(_get(url).splitlines()):
        # Not `date` - that shadows the imported date type used just above, and
        # because the name is assigned here Python treats it as local for the
        # whole function, so date.today() raises before the loop is ever reached.
        obs_date = row.get("observation_date") or row.get("DATE")
        raw = row.get(series, "")
        # FRED writes "." for a missing observation on a business-day series.
        if not obs_date or raw in (".", "", None):
            continue
        try:
            rows.append((obs_date, float(raw)))
        except ValueError:
            continue
    return rows, url


def ecb_sdmx(flow, key, n=5000):
    """ECB Data Portal SDMX-JSON, keyless. Returns [(date, float)] ascending.

    `n` counts raw observations, not months. These are daily series, so a few
    hundred buys barely a year of chart once downsampled to month-end - hence
    the deliberately large default.
    """
    url = ("https://data-api.ecb.europa.eu/service/data/%s/%s"
           "?lastNObservations=%d&format=jsondata" % (flow, key, n))
    doc = json.loads(_get(url))
    series = doc["dataSets"][0]["series"]
    obs = series[list(series.keys())[0]]["observations"]
    dates = [v["id"] for v in doc["structure"]["dimensions"]["observation"][0]["values"]]
    rows = []
    for idx_str, values in obs.items():
        idx = int(idx_str)
        if idx < len(dates) and values and values[0] is not None:
            rows.append((dates[idx], float(values[0])))
    rows.sort(key=lambda r: r[0])
    return rows, url


def noaa_oni():
    """NOAA Oceanic Nino Index, fixed-width text. Returns [(season-year, anomaly)]."""
    url = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
    rows = []
    for line in _get(url).splitlines()[1:]:
        parts = line.split()
        if len(parts) == 4:
            try:
                rows.append(("%s %s" % (parts[1], parts[0]), float(parts[3])))
            except ValueError:
                continue
    return rows, url


def boi_sdmx(flow, key, n=4000):
    """Bank of Israel SDMX-JSON via the Fusion Edge server, keyless.

    `key` filters on the first dimension (SERIES_CODE); a partial key is legal
    and is what we want, since the remaining dimensions are redundant for the
    single series we're after. Returns [(date, float)] ascending.
    """
    url = ("https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/"
           "BOI.STATISTICS/%s/1.0/%s/?format=sdmx-json&lastNObservations=%d"
           % (flow, key, n))
    doc = json.loads(_get(url))
    series = doc["data"]["dataSets"][0]["series"]
    if not series:
        raise ValueError("no series returned for %s/%s" % (flow, key))
    dates = [v["id"] for v in
             doc["data"]["structure"]["dimensions"]["observation"][0]["values"]]
    # A partial key can match more than one series; take the first deterministically.
    obs = series[sorted(series.keys())[0]]["observations"]
    rows = []
    for idx_str, values in obs.items():
        idx = int(idx_str)
        if idx < len(dates) and values and values[0] is not None:
            try:
                rows.append((dates[idx], float(values[0])))
            except (TypeError, ValueError):
                continue
    rows.sort(key=lambda r: r[0])
    return rows, url


def fao_fpi(column):
    """FAO Food Price Index monthly CSV, keyless. Returns [(YYYY-MM, float)].

    The link on FAO's index page carries an `sfvrsn` cache-buster that changes
    on every publication; the bare URL serves the same file and is stable, so
    we use that rather than re-scraping the page each run.

    Layout: two title lines, then a header row starting with "Date", then
    monthly rows. Trailing annual-average rows exist in some vintages, so we
    accept only YYYY-MM keys rather than trusting position.
    """
    url = ("https://www.fao.org/media/docs/worldfoodsituationlibraries/"
           "default-document-library/food_price_indices_data.csv")
    text = _get(url)
    reader = csv.reader(text.splitlines())
    header, rows = None, []
    for parts in reader:
        if not parts:
            continue
        first = parts[0].strip().lstrip("﻿")
        if header is None:
            if first.lower() == "date":
                header = [p.strip() for p in parts]
            continue
        if not re.match(r"^\d{4}-\d{2}$", first):
            continue
        try:
            value = parts[header.index(column)].strip()
        except (ValueError, IndexError):
            continue
        if not value:
            continue
        try:
            rows.append((first, float(value)))
        except ValueError:
            continue
    if header is None:
        raise ValueError("could not find the Date header row in the FAO CSV")
    rows.sort(key=lambda r: r[0])
    return rows, url


# --- indicator registry ------------------------------------------------------
# Keyed to the MAC-NN IDs in data/macro-indicators.csv. Only indicators with a
# keyless machine-readable source appear here; the rest stay link-only on the
# dashboard, which is honest about the difference.

SOURCES = [
    {"id": "MAC-01", "label": "US federal funds target rate (upper)", "unit": "%",
     "freq": "daily", "fn": lambda: fred_csv("DFEDTARU"),
     "note": "FRED series DFEDTARU."},
    {"id": "MAC-02", "label": "ECB main refinancing operations rate", "unit": "%",
     "freq": "daily", "fn": lambda: ecb_sdmx("FM", "D.U2.EUR.4F.KR.MRR_FR.LEV"),
     "note": "ECB Data Portal, daily level."},
    {"id": "MAC-04", "label": "ICE BofA EM high-yield corporate OAS", "unit": "pp",
     "freq": "daily", "fn": lambda: fred_csv("BAMLEMHBHYCRPIOAS"),
     "note": "Option-adjusted spread. Wider = investors demanding more to hold EM credit risk. FRED serves this series from 2023-07 only, whatever start date is requested - so its chart is a shorter window than the others. The footer on each chart states its own range."},
    {"id": "MAC-07", "label": "ENSO / Oceanic Nino Index", "unit": "degC anomaly",
     "freq": "monthly", "fn": noaa_oni,
     "note": "3-month running mean anomaly, one observation per overlapping season. Above +0.5 El Nino, below -0.5 La Nina."},
    {"id": "MAC-12", "label": "EUR/ILS reference rate", "unit": "ILS per EUR",
     "freq": "daily", "fn": lambda: ecb_sdmx("EXR", "D.ILS.EUR.SP00.A"),
     "note": "ECB daily reference rate. Relevant to a euro-denominated tranche placed with EU investors."},

    {"id": "MAC-03", "label": "Bank of Israel policy rate", "unit": "%",
     "freq": "daily", "fn": lambda: boi_sdmx("BR", "MNT_RIB_BOI_D"),
     "note": "BOI nominal interest rate, series MNT_RIB_BOI_D. The local funding cost for the Israel pilot and the discount rate on any shekel structure."},
    {"id": "MAC-06", "label": "FAO Food Price Index", "unit": "index 2014-2016=100",
     "freq": "monthly", "fn": lambda: fao_fpi("Food Price Index"),
     "note": "Nominal headline index. Monthly back to 1990 - the longest history in this set, and the most direct macro link to PL-1 repayment stress."},
    {"id": "MAC-13", "label": "USD/ILS representative rate", "unit": "ILS per USD",
     "freq": "daily", "fn": lambda: boi_sdmx("EXR", "RER_USD_ILS"),
     "note": "BOI representative rate. The dominant pair for the Israel pilot - most hard-currency tranching would be dollar-denominated."},
    {"id": "MAC-14", "label": "FAO Cereals Price Index", "unit": "index 2014-2016=100",
     "freq": "monthly", "fn": lambda: fao_fpi("Cereals"),
     "note": "The sub-index that tracks staple grains specifically. Moves ahead of and more sharply than the headline for the households in the PL-1 cohort."},
    {"id": "MAC-15", "label": "US 10-year Treasury yield", "unit": "%",
     "freq": "daily", "fn": lambda: fred_csv("DGS10"),
     "note": "The long-rate anchor. Fed funds prices the short end; a 15-25 year PL-2 PPA asset is discounted off something much closer to this."},
    {"id": "MAC-16", "label": "Brent crude oil price", "unit": "USD/barrel",
     "freq": "daily", "fn": lambda: fred_csv("DCOILBRENTEU"),
     "note": "Europe Brent spot, FRED DCOILBRENTEU. Sits behind both the tariff environment for PL-2 and the fuel and fertiliser costs feeding into MAC-06."},
]


# --- change computation ------------------------------------------------------

def _value_near(rows, back):
    """Value roughly `back` observations ago, tolerating short histories."""
    if len(rows) <= back:
        return None
    return rows[-1 - back][1]


# Observations per 1m / 3m / 12m, by series frequency. Getting this wrong is not
# a cosmetic issue: applying business-day offsets to a monthly series reads 66
# MONTHS back and reports it as a 3-month change.
LOOKBACK = {
    "daily": (22, 66, 260),     # business days
    "monthly": (1, 3, 12),
}


def changes(rows, freq):
    """Change over ~1m / ~3m / ~12m, using observation counts appropriate to the
    series frequency. Counts rather than calendar dates, so a source changing its
    date format can't silently corrupt the arithmetic."""
    if len(rows) < 2:
        return "", "", "", ""
    latest = rows[-1][1]
    out = []
    for back in LOOKBACK[freq]:
        prev = _value_near(rows, back)
        out.append("" if prev is None else round(latest - prev, 4))
    prev_any = next((c for c in out if c != ""), "")
    if prev_any == "":
        direction = ""
    elif prev_any > 0:
        direction = "up"
    elif prev_any < 0:
        direction = "down"
    else:
        direction = "flat"
    return out[0], out[1], out[2], direction


def load_previous():
    if not os.path.exists(OUT):
        return {}
    with open(OUT, newline="", encoding="utf-8") as fh:
        return {r["ID"]: r for r in csv.DictReader(fh)}


# --- history ----------------------------------------------------------------
# The snapshot answers "what is it now"; the history answers "what has it been
# doing", which is what a chart needs. Kept as a separate file so the snapshot
# stays small and diffable - the whole point of committing it is that a human
# can read the change in a PR.

def downsample(rows):
    """One observation per calendar month - the last in that month - trimmed to
    the last HISTORY_YEARS.

    Daily series would otherwise contribute ~260 rows a year each, which makes
    the committed file enormous and the git diff useless, and buys nothing: at
    dashboard width a monthly point is already below one pixel of resolution.
    Monthly and seasonal series pass through unchanged.
    """
    monthly = {}
    for date, value in rows:
        # ISO dates bucket by prefix; NOAA's "AMJ 2026" seasons have no month to
        # extract, so they key on themselves and pass through untouched.
        key = date[:7] if re.match(r"^\d{4}-\d{2}", date) else date
        monthly[key] = (date, value)          # later obs overwrite earlier
    out = [monthly[k] for k in sorted(monthly)]
    if len(out) > HISTORY_YEARS * 12:
        out = out[-(HISTORY_YEARS * 12):]
    return out


def load_history():
    if not os.path.exists(HISTORY):
        return {}
    by_id = {}
    with open(HISTORY, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            by_id.setdefault(row["ID"], []).append((row["Date"], row["Value"]))
    return by_id


def write_history(series_by_id):
    with open(HISTORY, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow(["ID", "Date", "Value"])
        for pid in sorted(series_by_id):
            for date, value in series_by_id[pid]:
                writer.writerow([pid, date, value])


def main():
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    previous = load_previous()
    history = load_history()
    rows, failures = [], []

    for src in SOURCES:
        try:
            series, url = src["fn"]()
            if not series:
                raise ValueError("source returned no usable observations")
            history[src["id"]] = downsample(series)
            c1, c3, c12, direction = changes(series, src.get("freq", "daily"))
            rows.append({
                "ID": src["id"], "Label": src["label"],
                "Value": series[-1][1], "Unit": src["unit"], "As_Of": series[-1][0],
                "Chg_1m": c1, "Chg_3m": c3, "Chg_12m": c12, "Direction": direction,
                "Fetched_At": now, "Status": "ok",
                "Source_URL": url, "Note": src["note"],
            })
            print("  ok      %-8s %-42s %s (as of %s)"
                  % (src["id"], src["label"][:42], series[-1][1], series[-1][0]))
        except Exception as exc:                      # noqa: BLE001 - never fatal
            failures.append("%s: %s" % (src["id"], exc))
            old = previous.get(src["id"])
            if old:
                # Keep the last good value and its original as_of. Status flips to
                # stale so the dashboard can say so rather than implying currency.
                old = dict(old)
                old["Status"] = "stale"
                old["Note"] = "%s | last refresh failed: %s" % (src["note"], exc)
                rows.append(old)
                print("  STALE   %-8s kept previous value (%s)" % (src["id"], exc),
                      file=sys.stderr)
            else:
                rows.append({
                    "ID": src["id"], "Label": src["label"], "Value": "",
                    "Unit": src["unit"], "As_Of": "", "Chg_1m": "", "Chg_3m": "",
                    "Chg_12m": "", "Direction": "", "Fetched_At": now,
                    "Status": "failed", "Source_URL": "", "Note": str(exc),
                })
                print("  FAILED  %-8s no previous value (%s)" % (src["id"], exc),
                      file=sys.stderr)

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, quoting=csv.QUOTE_ALL,
                                lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})

    # A failed fetch leaves that indicator's existing history in place rather
    # than dropping it - same rule as the snapshot, for the same reason.
    write_history(history)

    ok = sum(1 for r in rows if r["Status"] == "ok")
    points = sum(len(v) for v in history.values())
    print("Wrote %s - %d/%d refreshed" % (os.path.relpath(OUT, ROOT), ok, len(SOURCES)))
    print("Wrote %s - %d points across %d series"
          % (os.path.relpath(HISTORY, ROOT), points, len(history)))
    if failures:
        print("Failures (non-fatal): %s" % "; ".join(failures), file=sys.stderr)
    # Deliberately exit 0 even on partial failure: a flaky upstream API must not
    # take down the dashboard deploy.
    return 0


if __name__ == "__main__":
    sys.exit(main())
