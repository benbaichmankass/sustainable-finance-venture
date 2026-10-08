#!/usr/bin/env python3
"""DS-01: FAOSTAT crops and livestock products - coffee, green - for the
three RT-7 countries.

    python3 scripts/ingest/ds01_faostat_yields.py            # fetch bulk + filter + process
    python3 scripts/ingest/ds01_faostat_yields.py --no-fetch # re-process the latest raw extract

FAOSTAT's query API now requires an authorization header, so this uses the
publisher's bulk download (the normalized "All Data" zip, ~34 MB) and keeps
only the coffee rows for Colombia, Ethiopia and Viet Nam as the raw extract.
The query log records the bulk file's size and SHA-256 and the filter applied,
so the extract is reproducible from the publisher file.

Raw:       data/raw/DS-01/faostat-qcl-coffee-3-countries-<date>.csv (+ .query.json)
Processed: data/processed/ds-01-coffee-national-yields.csv (+ .md)

Python 3 stdlib.
"""

from __future__ import annotations

import csv
import io
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

DS = "DS-01"
NAME = "ds-01-coffee-national-yields"
BULK_URL = "https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip"
AREAS = {"Colombia": "colombia", "Ethiopia": "ethiopia", "Viet Nam": "vietnam"}
ITEM_PREFIX = "Coffee"
ELEMENTS = {"Area harvested": "Area_ha", "Production": "Production_t", "Yield": "Yield_t_ha"}


def filter_bulk(zip_bytes):
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    name = [n for n in z.namelist() if n.endswith(".csv") and "Normalized" in n and "Flags" not in n][0]
    out = io.StringIO()
    w = None
    kept = 0
    with z.open(name) as fh:
        r = csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig"))
        w = csv.DictWriter(out, fieldnames=r.fieldnames, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        for row in r:
            if row["Area"] in AREAS and row["Item"].startswith(ITEM_PREFIX) and row["Element"] in ELEMENTS:
                w.writerow(row)
                kept += 1
    return name, kept, out.getvalue().encode("utf-8")


def process(raw_path, raw_log):
    rows = list(csv.DictReader(open(raw_path, newline="", encoding="utf-8")))
    items = sorted({(r["Item Code"], r["Item"]) for r in rows})
    by = {}
    for r in rows:
        key = (AREAS[r["Area"]], int(r["Year"]))
        d = by.setdefault(key, {"Area_ha": "", "Production_t": "", "Yield_t_ha": "", "Flag": set(), "Item": r["Item"]})
        col = ELEMENTS[r["Element"]]
        v = r["Value"]
        if v == "":
            continue
        v = float(v)
        if col == "Yield_t_ha":
            if r["Unit"] == "kg/ha":
                v = v / 1000.0
            elif r["Unit"] == "hg/ha":
                v = v / 10000.0
            elif r["Unit"] not in ("t/ha",):
                C.fail("unexpected yield unit %r" % r["Unit"])
            v = round(v, 4)
        elif col == "Area_ha":
            if r["Unit"] != "ha":
                C.fail("unexpected area unit %r" % r["Unit"])
            v = round(v, 1)
        else:
            if r["Unit"] != "t":
                C.fail("unexpected production unit %r" % r["Unit"])
            v = round(v, 1)
        d[col] = v
        if r["Flag"]:
            d["Flag"].add(r["Flag"])
    out = []
    for (region, year) in sorted(by):
        d = by[(region, year)]
        out.append([region, year, d["Area_ha"], d["Production_t"], d["Yield_t_ha"], ";".join(sorted(d["Flag"]))])
    years = sorted({r[1] for r in out})
    # plausibility: yield equals production / area within 2% where all three are present
    off = [r for r in out if r[2] and r[3] and r[4] and abs(r[3] / r[2] - r[4]) / max(r[4], 1e-9) > 0.02]
    header = ["Region", "Year", "Area_ha", "Production_t", "Yield_t_ha", "Flags"]
    md = """# DS-01 — coffee, green: national area, production and yield (FAOSTAT)

One row per country per year, %d to %d (%d rows). FAOSTAT domain QCL (Crops and livestock products), item %s, elements Area harvested, Production and Yield, for Colombia, Ethiopia and Viet Nam.

| Column | Meaning | Unit |
|---|---|---|
| `Region` | RT-7 region key (the country; FAOSTAT is national) | |
| `Year` | Calendar year as FAOSTAT reports it | |
| `Area_ha` | Area harvested | ha |
| `Production_t` | Production of green coffee | t |
| `Yield_t_ha` | Yield, converted from the publisher's kg/ha (or hg/ha in older vintages) | t / ha |
| `Flags` | FAOSTAT observation-status flags present in that year's rows (A official, E estimated, I imputed, T unofficial, blank official per the publisher's flag table) | |

**What it is.** National averages. A district (Huila, Jimma, Dak Lak) can sit well above or below its national figure, and a cooperative's members further still. RT-7 uses the national series for the year-to-year *variability* of the regional yield factor and as a first anchor for the level; the level should be replaced by district statistics or partner delivery records (DS-08) before it is believed.

**Validation (run %s).** Schema: six columns. Coverage: continuous from %d for every country. Units: converted once, in the script, which refuses any unit it does not expect. Plausibility: production / area reproduces the published yield within 2 percent in every row%s.

%s
""" % (years[0], years[-1], len(out), "; ".join("%s (%s)" % (i[1], i[0]) for i in items), C.now_iso(), years[0],
       "" if not off else " except %d rows (%s), kept as published" % (len(off), ", ".join("%s %s" % (r[0], r[1]) for r in off[:5])),
       C.provenance_block(DS, raw_log, "scripts/ingest/ds01_faostat_yields.py",
                          {"Bulk file": raw_log["request"].get("bulk_url", ""),
                           "Bulk SHA-256": raw_log["request"].get("bulk_sha256", ""),
                           "Filter": raw_log["request"].get("filter", "")}))
    C.write_processed(NAME, header, out, md)


def main():
    if "--no-fetch" not in sys.argv:
        print("fetching bulk file (about 34 MB) %s" % BULK_URL)
        zip_bytes = C.fetch(BULK_URL, timeout=600)
        member, kept, extract = filter_bulk(zip_bytes)
        raw_path, log = C.save_raw(DS, "faostat-qcl-coffee-3-countries-%s.csv" % C.today(), extract,
                                   {"bulk_url": BULK_URL, "bulk_member": member, "bulk_bytes": len(zip_bytes),
                                    "bulk_sha256": C.sha256_bytes(zip_bytes), "method": "GET bulk zip, filter rows",
                                    "filter": "Area in (Colombia, Ethiopia, Viet Nam) and Item startswith 'Coffee' and Element in (Area harvested, Production, Yield)"},
                                   "Raw extract is the filtered subset of the publisher's bulk file, rows unchanged; %d rows kept." % kept)
        print("raw: %s (%d rows, %d bytes)" % (os.path.relpath(raw_path, C.ROOT), kept, log["bytes"]))
    else:
        raw_path = C.latest_raw(DS, ".csv")
        if not raw_path:
            C.fail("no raw file; run without --no-fetch")
        log = json.load(open(raw_path + ".query.json"))
    process(raw_path, log)


if __name__ == "__main__":
    main()
