#!/usr/bin/env python3
"""DS-03: NASA POWER monthly meteorology at the pilot districts.

    python3 scripts/ingest/ds03_nasa_power.py            # fetch + process
    python3 scripts/ingest/ds03_nasa_power.py --no-fetch # re-process the latest raw file

Raw:       data/raw/DS-03/nasa-power-monthly-<date>.json (+ .query.json)
           One file holding the verbatim API response for every point, keyed
           by the request URL, so a single raw file documents the whole pull.
Processed: data/processed/ds-03-district-climate-monthly.csv (+ .md)

Points are district centroids, recorded below and in the query log. NASA
POWER's grid is 0.5 x 0.625 degrees, so a point is a regional value, not a plot.
Python 3 stdlib.
"""

from __future__ import annotations

import calendar
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

DS = "DS-03"
NAME = "ds-03-district-climate-monthly"
API = "https://power.larc.nasa.gov/api/temporal/monthly/point"
PARAMS = "PRECTOTCORR,T2M,T2M_MAX"
START, END = 1981, 2025

# Region key (as in data/rt7-regions.csv), district, approximate centroid.
# Coordinates are judgement: a point inside each coffee-growing district,
# not a surveyed polygon. Replace with a documented boundary (DS-02 work).
POINTS = [
    ("colombia", "Huila", 2.45, -75.65),
    ("colombia", "Cauca", 2.45, -76.60),
    ("ethiopia", "Jimma", 7.67, 36.83),
    ("ethiopia", "Sidama", 6.80, 38.40),
    ("vietnam", "Dak Lak", 12.67, 108.05),
    ("vietnam", "Lam Dong", 11.95, 108.44),
]


def url_for(lat, lon):
    return ("%s?parameters=%s&community=AG&longitude=%s&latitude=%s&start=%d&end=%d&format=JSON"
            % (API, PARAMS, lon, lat, START, END))


def process(raw_path, raw_log):
    blob = json.load(open(raw_path, encoding="utf-8"))
    rows = []
    for region, district, lat, lon in POINTS:
        resp = blob["responses"].get(url_for(lat, lon))
        if not resp:
            C.fail("no response stored for %s" % district)
        par = resp["properties"]["parameter"]
        elev = resp["geometry"]["coordinates"][2] if len(resp["geometry"]["coordinates"]) > 2 else ""
        fill = resp.get("header", {}).get("fill_value", -999)
        for key in sorted(par["PRECTOTCORR"]):
            y, m = int(key[:4]), int(key[4:])
            if m == 13:                      # POWER's annual aggregate; derive our own instead
                continue
            days = calendar.monthrange(y, m)[1]
            p = par["PRECTOTCORR"][key]
            t = par["T2M"].get(key)
            tx = par["T2M_MAX"].get(key)
            if p == fill or p is None:
                continue
            rows.append([region, district, lat, lon, round(elev, 1) if elev != "" else "",
                         "%04d-%02d" % (y, m), round(p * days, 1), "" if t in (None, fill) else round(t, 2),
                         "" if tx in (None, fill) else round(tx, 2)])
    header = ["Region", "District", "Lat", "Lon", "Elev_m", "Month", "Precip_mm", "T2M_C", "T2M_Max_C"]
    months = sorted({r[5] for r in rows})
    md = """# DS-03 — district climate, monthly (NASA POWER)

One row per district per month, %s to %s (%d rows across %d points). Source: NASA POWER monthly point API, agroclimatology community, parameters `PRECTOTCORR`, `T2M`, `T2M_MAX`.

| Column | Meaning | Unit |
|---|---|---|
| `Region` | RT-7 region key | |
| `District` | Coffee district the point represents | |
| `Lat`, `Lon` | Request coordinates (district centroid, by judgement) | decimal degrees |
| `Elev_m` | Elevation POWER reports for the grid cell | m |
| `Month` | Calendar month | `YYYY-MM` |
| `Precip_mm` | Monthly precipitation: POWER's `PRECTOTCORR` (mm/day, bias-corrected) x days in month | mm |
| `T2M_C` | Mean 2 m air temperature | deg C |
| `T2M_Max_C` | Mean daily maximum 2 m temperature | deg C |

**What it is.** A reanalysis-based grid product at 0.5 x 0.625 degrees: a regional climate signal, not a station and not a plot. Good enough to build a seasonal rainfall anomaly for the RT-7 climate factor; not good enough to settle an index-insurance trigger (that is DS-02, CHIRPS, with a documented boundary).

**Validation (run %s).** Schema: nine columns. Coverage: every point returns every month from %s; POWER's own annual aggregate (month code 13) is dropped and recomputed downstream. Units: mm/day converted to monthly mm using the calendar month length. Fill values (%s) are skipped, none were present in this pull unless noted in the query log.

%s
""" % (months[0], months[-1], len(rows), len(POINTS), C.now_iso(), months[0], "-999",
       C.provenance_block(DS, raw_log, "scripts/ingest/ds03_nasa_power.py",
                          {"Points": "; ".join("%s/%s (%s, %s)" % (p[0], p[1], p[2], p[3]) for p in POINTS),
                           "API": API}))
    C.write_processed(NAME, header, rows, md)


def main():
    if "--no-fetch" not in sys.argv:
        responses = {}
        for region, district, lat, lon in POINTS:
            u = url_for(lat, lon)
            print("fetching %s / %s" % (region, district))
            responses[u] = json.loads(C.fetch(u, timeout=120).decode("utf-8"))
        blob = {"api": API, "parameters": PARAMS, "start": START, "end": END, "retrieved_at_utc": C.now_iso(),
                "points": [{"region": r, "district": d, "lat": la, "lon": lo} for r, d, la, lo in POINTS],
                "responses": responses}
        data = json.dumps(blob, indent=0).encode("utf-8")
        raw_path, log = C.save_raw(DS, "nasa-power-monthly-%s.json" % C.today(), data,
                                   {"urls": list(responses), "method": "GET"},
                                   "Verbatim API responses, one per point, keyed by request URL.")
        print("raw: %s (%d bytes)" % (os.path.relpath(raw_path, C.ROOT), log["bytes"]))
    else:
        raw_path = C.latest_raw(DS, ".json")
        if not raw_path:
            C.fail("no raw file; run without --no-fetch")
        log = json.load(open(raw_path + ".query.json"))
    process(raw_path, log)


if __name__ == "__main__":
    main()
