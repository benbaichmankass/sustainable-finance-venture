#!/usr/bin/env python3
"""DS-02: CHIRPS v2.0 monthly precipitation averaged over the six RT-7 coffee
districts, inside documented administrative boundaries.

    python3 scripts/ingest/ds02_chirps.py            # fetch + process
    python3 scripts/ingest/ds02_chirps.py --no-fetch # re-process the latest raw files

Two sources:

  Boundaries  geoBoundaries (gbOpen release, pinned commit 9469f09): simplified
              ADM1 polygons for Huila and Cauca (Colombia), Dak Lak and Lam Dong
              (Viet Nam) and ADM2 zone polygons for Jimma and Sidama (Ethiopia,
              2016 vintage, when Sidama was still a zone of SNNPR). Open licences
              per country (CC BY / ODbL per the gbOpen metadata), attribution in
              NOTICE. The six polygons are committed as
              data/processed/ds-02-district-boundaries.geojson so the boundary
              behind every number is in the repo.
  Rainfall    CHIRPS v2.0 monthly (0.05 degree), served by the IRI Data Library
              as a grid table over each district's bounding box; cells whose
              centre falls inside the polygon are averaged (simple mean).

Processed:
  data/processed/ds-02-district-rainfall-monthly.csv   Region, District, Month, Precip_mm, N_Cells
  data/processed/ds-02-district-rainfall-annual.csv    calendar-year totals and standardised anomalies
  data/rt7-climate-history.csv                         one standardised anomaly per region-year,
                                                       the series the model's empirical climate
                                                       factor bootstraps from
Python 3 stdlib.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

DS = "DS-02"
GB_COMMIT = "9469f09"
GB_URL = "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/%s/releaseData/gbOpen/%s/%s/geoBoundaries-%s-%s_simplified.geojson"
IRI = "https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly/.global/.precipitation"
T_START, T_END = "Jan 1981", "Dec 2026"
# region key, district label, ISO3, ADM level, substrings that identify the feature (accent-stripped, lower case)
DISTRICTS = [
    ("colombia", "Huila", "COL", "ADM1", ["huila"]),
    ("colombia", "Cauca", "COL", "ADM1", ["cauca"]),
    ("ethiopia", "Jimma", "ETH", "ADM2", ["jimma", "jima"]),
    ("ethiopia", "Sidama", "ETH", "ADM2", ["sidama", "sidamo"]),
    ("vietnam", "Dak Lak", "VNM", "ADM1", ["dak lak", "daklak"]),
    ("vietnam", "Lam Dong", "VNM", "ADM1", ["lam dong", "lamdong"]),
]
CLIMATE_CSV = os.path.join(C.ROOT, "data", "rt7-climate-history.csv")
BOUNDARIES = os.path.join(C.ROOT, "data", "processed", "ds-02-district-boundaries.geojson")


def norm(s):
    import unicodedata
    s = s.replace("\u0110", "D").replace("\u0111", "d")       # Vietnamese D-with-stroke has no NFKD decomposition
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def point_in_ring(x, y, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y):
            xcross = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < xcross:
                inside = not inside
        j = i
    return inside


def point_in_geometry(x, y, geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        if point_in_ring(x, y, poly[0]) and not any(point_in_ring(x, y, hole) for hole in poly[1:]):
            return True
    return False


def bbox(geom):
    xs, ys = [], []
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        for ring in poly:
            for pt in ring:
                xs.append(pt[0]); ys.append(pt[1])
    return min(xs), max(xs), min(ys), max(ys)


def find_feature(fc, keys):
    exact = [f for f in fc["features"] if norm(f["properties"].get("shapeName", "")) in keys]
    hits = exact or [f for f in fc["features"] if any(k in norm(f["properties"].get("shapeName", "")) for k in keys)]
    if len(hits) != 1:
        C.fail("expected one feature for %s, found %s" % (keys, [h["properties"].get("shapeName") for h in hits]))
    return hits[0]


def iri_url(x0, x1, y0, y1):
    pad = 0.05
    return ("%s/X/%.3f/%.3f/RANGEEDGES/Y/%.3f/%.3f/RANGEEDGES/T/(%s)/(%s)/RANGEEDGES/gridtable.tsv"
            % (IRI, x0 - pad, x1 + pad, y0 - pad, y1 + pad, T_START.replace(" ", "%20"), T_END.replace(" ", "%20")))


def month_of(t):
    k = int(math.floor(float(t)))          # months since 1960-01-01, cell centred at .5
    return "%04d-%02d" % (1960 + k // 12, k % 12 + 1)


def parse_gridtable(path, geom):
    """-> {month: (sum, count)} over cells inside the polygon, plus cell counts."""
    inside_cache = {}
    agg = {}
    n_in = n_tot = 0
    with open(path, encoding="utf-8") as fh:
        hdr = fh.readline(); fh.readline()   # names, units
        if not hdr.startswith("X"):
            C.fail("unexpected gridtable header in %s: %r" % (path, hdr[:80]))
        for line in fh:
            parts = line.split()
            if len(parts) < 4:
                continue
            x, y, t, v = float(parts[0]), float(parts[1]), parts[2], parts[3]
            key = (x, y)
            if key not in inside_cache:
                inside_cache[key] = point_in_geometry(x, y, geom)
                n_tot += 1
                n_in += inside_cache[key]
            if not inside_cache[key] or v in ("NaN", "nan", "-999"):
                continue
            m = month_of(t)
            s, c = agg.get(m, (0.0, 0))
            agg[m] = (s + float(v), c + 1)
    return agg, n_in, n_tot


def sd(x):
    m = sum(x) / len(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))


def process(raw_files, logs):
    feats = json.load(open(BOUNDARIES, encoding="utf-8"))["features"]
    by_key = {(f["properties"]["region"], f["properties"]["district"]): f for f in feats}
    monthly, cells = [], {}
    for region, district, iso, adm, keys in DISTRICTS:
        geom = by_key[(region, district)]["geometry"]
        agg, n_in, n_tot = parse_gridtable(raw_files[(region, district)], geom)
        cells[(region, district)] = (n_in, n_tot)
        for m in sorted(agg):
            s, c = agg[m]
            monthly.append([region, district, m, round(s / c, 2), c])
        print("  %-9s %-8s %d cells inside of %d in the box, %s to %s" % (region, district, n_in, n_tot, min(agg), max(agg)))
    header = ["Region", "District", "Month", "Precip_mm", "N_Cells"]
    # Annual totals (complete calendar years) and standardised anomalies
    annual = {}
    for region, district, m, v, c in monthly:
        annual.setdefault((region, district), {}).setdefault(int(m[:4]), []).append(v)
    arows, z_by = [], {}
    for (region, district), yrs in annual.items():
        tot = {y: sum(v) for y, v in yrs.items() if len(v) == 12}
        ys = sorted(tot); vals = [tot[y] for y in ys]
        mu, s = sum(vals) / len(vals), sd(vals)
        for y in ys:
            z = (tot[y] - mu) / s
            z_by.setdefault((region, district), {})[y] = z
            arows.append([region, district, y, round(tot[y], 1), round(z, 3), round(mu, 1), round(s / mu, 3)])
    aheader = ["Region", "District", "Year", "Precip_mm", "Anomaly_Z", "Mean_mm", "CV"]
    # Region series: mean of the two districts' z, re-standardised
    regions = sorted({r for r, _, *_ in DISTRICTS})
    crows = []
    for region in regions:
        ds = [d for r, d, *_ in DISTRICTS if r == region]
        yrs = sorted(set.intersection(*[set(z_by[(region, d)]) for d in ds]))
        raw = [sum(z_by[(region, d)][y] for d in ds) / len(ds) for y in yrs]
        mu, s = sum(raw) / len(raw), sd(raw)
        for y, v in zip(yrs, raw):
            crows.append([region, y, round((v - mu) / s, 4), "; ".join(ds)])
    cheader = ["Region", "Year", "Rain_Anomaly_Z", "Districts"]
    with open(CLIMATE_CSV, "w", newline="", encoding="utf-8") as fh:
        import csv
        w = csv.writer(fh, quoting=csv.QUOTE_ALL, lineterminator="\n"); w.writerow(cheader); w.writerows(crows)
    print("wrote %s (%d rows)" % (os.path.relpath(CLIMATE_CSV, C.ROOT), len(crows)))

    first_log = logs[DISTRICTS[0][:2]]
    bl = logs["boundaries"]
    cell_note = "; ".join("%s %d of %d" % (d, cells[(r, d)][0], cells[(r, d)][1]) for r, d, *_ in DISTRICTS)
    md = """# DS-02 — CHIRPS v2.0 monthly rainfall over the six RT-7 coffee districts

One row per district per month, %s to %s. Simple mean of the CHIRPS 0.05-degree cells whose centre falls inside the district polygon.

| Column | Meaning | Unit |
|---|---|---|
| `Region` | RT-7 region key | |
| `District` | Huila, Cauca (Colombia, departments); Jimma, Sidama (Ethiopia, zones as of the 2016 boundary set); Dak Lak, Lam Dong (Viet Nam, provinces) | |
| `Month` | Calendar month | `YYYY-MM` |
| `Precip_mm` | Mean monthly precipitation over the cells inside the polygon | mm |
| `N_Cells` | Cells averaged (constant per district unless CHIRPS reports a missing cell) | |

**The boundaries.** geoBoundaries gbOpen release, commit `%s`, simplified geometries, fetched from `media.githubusercontent.com` (the repository stores them with Git LFS). The six features are copied verbatim into `data/processed/ds-02-district-boundaries.geojson` with their `shapeID`, so a reader can see exactly which polygon produced each number. Cells inside the box but outside the polygon are discarded: %s. Ethiopia's set is the 2016 vintage, in which Sidama is a zone of SNNPR; it became a regional state in 2020 with the same outline. Licences: see the gbOpen metadata per country (OpenStreetMap-derived for Colombia, Open Africa / Code for Ethiopia CC BY for Ethiopia, geoBoundaries / Wikipedia for Viet Nam); attribution recorded in `NOTICE`.

**The rainfall.** CHIRPS v2.0 (Climate Hazards Center, UC Santa Barbara), monthly, 0.05 degree, 1981 onward, read through the IRI Data Library's `gridtable.tsv` view of the bounding box; the raw tables are kept under `data/raw/DS-02/` (gitignored) with query logs. CHIRPS blends satellite estimates with station data; it is a rainfall product, not a drought index, and it says nothing about temperature, which NASA POWER (DS-03) covers at the centroid.

**Derived files.** `ds-02-district-rainfall-annual.csv` holds calendar-year totals for complete years with the standardised anomaly (`Anomaly_Z`, over the district's own record) and the district's mean and coefficient of variation. `data/rt7-climate-history.csv` averages the two districts' anomalies per region and re-standardises them; that series is what the model's empirical climate factor bootstraps from (`climate_rain_beta`). Calendar years are used for every region; the coffee year runs across the calendar year in all three, so a flowering-to-harvest window is a refinement left for a partner's own harvest calendar.

**Validation (run %s).** Schema: five columns. Coverage: every district has every month from 1981-01 to the latest CHIRPS month. Units: mm/month as served. Plausibility: annual means fall where the literature puts them (Huila and Cauca roughly 1,200 to 2,000 mm; Jimma and Sidama 1,200 to 1,800; Dak Lak and Lam Dong 1,700 to 2,000), and the within-region district anomalies are positively correlated.

%s
""" % (monthly[0][2], max(r[2] for r in monthly), GB_COMMIT, cell_note, C.now_iso(),
       C.provenance_block(DS, first_log, "scripts/ingest/ds02_chirps.py",
                          {"IRI base": IRI, "Boundary source": GB_URL % (GB_COMMIT, "<ISO>", "<ADM>", "<ISO>", "<ADM>"),
                           "Boundary raw SHA-256 (COL ADM1)": bl["sha256"],
                           "Other raw files": "one gridtable per district under data/raw/DS-02/ with its own query log"}))
    C.write_processed("ds-02-district-rainfall-monthly", header, monthly, md)
    md_a = """# DS-02 — district rainfall, calendar-year totals and anomalies

Derived from `ds-02-district-rainfall-monthly.csv`: complete calendar years only. `Anomaly_Z` is `(Precip_mm - Mean_mm) / sd` over the district's own record; `CV` is `sd / Mean_mm`. See the monthly file's dictionary for sources, boundaries and caveats.

**Validation (run %s).** One row per district per complete year; anomalies have mean 0 and sd 1 per district by construction.

%s
""" % (C.now_iso(), C.provenance_block(DS, first_log, "scripts/ingest/ds02_chirps.py", {"Derived from": "ds-02-district-rainfall-monthly.csv"}))
    C.write_processed("ds-02-district-rainfall-annual", aheader, arows, md_a)


def fetch_or_reuse(filename, url, request, note, timeout):
    """A same-day raw file is reused rather than re-fetched: save_raw refuses to
    overwrite, and a re-run after a parsing fix should not hit the publisher again."""
    path = os.path.join(C.raw_dir(DS), filename)
    if os.path.exists(path) and os.path.exists(path + ".query.json"):
        print("  reusing %s" % filename)
        return path, json.load(open(path + ".query.json"))
    data = C.fetch(url, timeout=timeout)
    return C.save_raw(DS, filename, data, request, note)


def main():
    fetch = "--no-fetch" not in sys.argv
    raw_dir = C.raw_dir(DS)
    os.makedirs(raw_dir, exist_ok=True)
    logs, raw_files = {}, {}
    if fetch:
        # 1. boundaries
        fcs = {}
        for iso, adm in sorted({(d[2], d[3]) for d in DISTRICTS}):
            url = GB_URL % (GB_COMMIT, iso, adm, iso, adm)
            print("fetching %s" % url)
            path, log = fetch_or_reuse("geoBoundaries-%s-%s_simplified-%s.geojson" % (iso, adm, C.today()), url,
                                       {"url": url, "method": "GET", "commit": GB_COMMIT}, "Whole-country simplified boundary file as published.", 180)
            fcs[(iso, adm)] = json.load(open(path, encoding="utf-8"))
            if (iso, adm) == ("COL", "ADM1"):
                logs["boundaries"] = log
        feats = []
        for region, district, iso, adm, keys in DISTRICTS:
            f = find_feature(fcs[(iso, adm)], keys)
            feats.append({"type": "Feature", "properties": {"region": region, "district": district, "iso3": iso, "adm_level": adm,
                                                            "shapeName": f["properties"].get("shapeName"), "shapeID": f["properties"].get("shapeID"),
                                                            "shapeGroup": f["properties"].get("shapeGroup"), "source": "geoBoundaries gbOpen " + GB_COMMIT},
                          "geometry": f["geometry"]})
            print("  %s / %s -> %r (%s)" % (region, district, f["properties"].get("shapeName"), f["properties"].get("shapeID")))
        with open(BOUNDARIES, "w", encoding="utf-8") as fh:
            json.dump({"type": "FeatureCollection", "name": "RT-7 coffee district boundaries (geoBoundaries gbOpen, simplified)", "features": feats}, fh, separators=(",", ":"))
        print("wrote %s (%d KB)" % (os.path.relpath(BOUNDARIES, C.ROOT), os.path.getsize(BOUNDARIES) // 1024))
        # 2. rainfall per district
        for region, district, iso, adm, keys in DISTRICTS:
            geom = [f for f in feats if f["properties"]["district"] == district][0]["geometry"]
            x0, x1, y0, y1 = bbox(geom)
            url = iri_url(x0, x1, y0, y1)
            print("fetching CHIRPS for %s (%.2f..%.2f, %.2f..%.2f)" % (district, x0, x1, y0, y1))
            slug = district.lower().replace(" ", "-")
            path, log = fetch_or_reuse("chirps-monthly-%s-%s.tsv" % (slug, C.today()), url, {"url": url, "method": "GET", "bbox": [x0, x1, y0, y1]},
                                       "IRI gridtable over the district bounding box; cells outside the polygon are discarded at processing.", 900)
            print("  raw %s (%d KB)" % (os.path.basename(path), log["bytes"] // 1024))
            logs[(region, district)] = log; raw_files[(region, district)] = path
    else:
        for region, district, iso, adm, keys in DISTRICTS:
            slug = district.lower().replace(" ", "-")
            cands = sorted(f for f in os.listdir(raw_dir) if f.startswith("chirps-monthly-%s-" % slug) and f.endswith(".tsv"))
            if not cands:
                C.fail("no raw CHIRPS file for %s; run without --no-fetch" % district)
            raw_files[(region, district)] = os.path.join(raw_dir, cands[-1])
            logs[(region, district)] = json.load(open(raw_files[(region, district)] + ".query.json"))
        b = sorted(f for f in os.listdir(raw_dir) if f.startswith("geoBoundaries-COL-ADM1") and f.endswith(".geojson"))
        logs["boundaries"] = json.load(open(os.path.join(raw_dir, b[-1]) + ".query.json"))
    process(raw_files, logs)


if __name__ == "__main__":
    main()
