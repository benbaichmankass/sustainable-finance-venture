#!/usr/bin/env python3
"""DS-10: Federacion Nacional de Cafeteros (FNC) coffee statistics workbook.

    python3 scripts/ingest/ds10_fnc_colombia.py            # fetch + process
    python3 scripts/ingest/ds10_fnc_colombia.py --no-fetch

The FNC publishes one workbook, refreshed monthly, with the internal
(farm-gate) base purchase price, the external ex-dock price, ICO indicator
prices and the cultivated area by department. The file name carries the
month; the script reads the current link off the statistics page.

Raw:       data/raw/DS-10/fnc-precios-area-produccion-<date>.xlsx
Processed: data/processed/ds-10-colombia-coffee-prices-monthly.csv (+ .md)
           data/processed/ds-10-colombia-coffee-area-by-department.csv (+ .md)

Unit notes that matter: the internal price is Colombian pesos per carga of
125 kg of DRY PARCHMENT at the FNC's base yield factor (factor de
rendimiento). The factor was 88 kg of parchment per 70 kg sack of excelso
until 2024-03-31 and 94 from 2024-04-01; at 94 a carga yields 93.09 kg of
excelso (FNC daily price sheet, RES row in data/resources.csv). Converting
to a per-kg-green price therefore depends on the date, and the calibration
only uses months from 2024-04 onward, where the factor is documented.
Dependency: openpyxl.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

DS = "DS-10"
PAGE = "https://federaciondecafeteros.org/wp/estadisticas-cafeteras/"
NAME_PRICES = "ds-10-colombia-coffee-prices-monthly"
NAME_AREA = "ds-10-colombia-coffee-area-by-department"


def find_link():
    html = C.fetch(PAGE, timeout=120).decode("utf-8", "replace")
    links = sorted(set(re.findall(r'href="(https://federaciondecafeteros\.org/wp-content/uploads/[^"]*Precios-area-y-produccion[^"]*\.xlsx)"', html)))
    if not links:
        C.fail("no 'Precios-area-y-produccion' link on %s" % PAGE)
    return links[-1]


def header_row(rows, keys):
    for i, r in enumerate(rows):
        if r and any(isinstance(c, str) and c.strip() in keys for c in r):
            return i
    return None


def as_month(v):
    if isinstance(v, (datetime.datetime, datetime.date)):
        return "%04d-%02d" % (v.year, v.month)
    if isinstance(v, str) and re.match(r"^\d{4}-\d{2}", v):
        return v[:7]
    return None


def process(raw_path, raw_log, source_url):
    import openpyxl
    wb = openpyxl.load_workbook(raw_path, read_only=True, data_only=True)

    def sheet(name_part):
        n = [s for s in wb.sheetnames if name_part in s]
        if not n:
            C.fail("sheet containing %r not found; sheets: %s" % (name_part, wb.sheetnames))
        return list(wb[n[0]].iter_rows(values_only=True))

    # Internal price, monthly (COP per carga 125 kg dry parchment)
    rows = sheet("Precio Interno Mensual"); h = header_row(rows, {"Mes"}); hdr = rows[h]
    cm = next(j for j, c in enumerate(hdr) if c == "Mes"); cp = cm + 1
    internal = {}
    for r in rows[h + 1:]:
        m = as_month(r[cm]) if len(r) > cm else None
        if m and len(r) > cp and isinstance(r[cp], (int, float)):
            internal[m] = round(float(r[cp]), 0)
    # Ex-dock external price, monthly (US cents per lb)
    rows = sheet("Ex_Dock Mensual"); h = header_row(rows, {"Mes"}); hdr = rows[h]
    cm = next(j for j, c in enumerate(hdr) if c == "Mes"); cp = cm + 1
    exdock = {}
    for r in rows[h + 1:]:
        m = as_month(r[cm]) if len(r) > cm else None
        if m and len(r) > cp and isinstance(r[cp], (int, float)):
            exdock[m] = round(float(r[cp]), 2)
    # ICO indicators, monthly: composite, Colombian milds (NY, Europe, weighted), other milds (weighted)
    rows = sheet("Precio OIC"); h = header_row(rows, {"Mes"}); hdr = rows[h]
    cm = next(j for j, c in enumerate(hdr) if c == "Mes")
    oic = {}
    for r in rows[h + 1:]:
        m = as_month(r[cm]) if len(r) > cm else None
        if m:
            vals = [round(float(r[cm + k]), 2) if len(r) > cm + k and isinstance(r[cm + k], (int, float)) else "" for k in (1, 4, 7)]
            oic[m] = vals  # composite, Colombian milds weighted, other milds weighted
    months = sorted(set(internal) | set(exdock) | set(oic))
    out = []
    for m in months:
        y, mo = int(m[:4]), int(m[5:])
        fr = 94 if (y, mo) >= (2024, 4) else (88 if (y, mo) >= (2019, 9) else "")
        o = oic.get(m, ["", "", ""])
        out.append([m, internal.get(m, ""), fr, exdock.get(m, ""), o[0], o[1], o[2]])
    out = [r for r in out if r[0] >= "2000-01"]
    header = ["Month", "Internal_Price_COP_per_carga", "Base_Yield_Factor_Assumed", "ExDock_Price_USc_per_lb",
              "ICO_Composite_USc_per_lb", "ICO_Colombian_Milds_USc_per_lb", "ICO_Other_Milds_USc_per_lb"]
    last_int = max(k for k in internal)
    md = """# DS-10 — Colombian coffee prices, monthly (FNC)

One row per month from 2000-01 to %s. Source workbook: FNC, "Precios, area y produccion de cafe" (%s).

| Column | Meaning | Unit |
|---|---|---|
| `Month` | Calendar month | `YYYY-MM` |
| `Internal_Price_COP_per_carga` | FNC base internal purchase price (precio interno base de compra), monthly average | COP per carga of 125 kg dry parchment |
| `Base_Yield_Factor_Assumed` | The FNC base yield factor the price is quoted at: 94 from 2024-04 (FNC committee decision of March 2024, effective 1 April 2024), 88 from 2019-09 to 2024-03 (the factor the 2024 decision replaced; the earlier start of 88 is not documented here, so months before 2019-09 are left blank) | kg parchment per 70 kg excelso |
| `ExDock_Price_USc_per_lb` | FNC external price of Colombian coffee, ex-dock | US cents / lb |
| `ICO_Composite_USc_per_lb` | ICO composite indicator, as reproduced by the FNC | US cents / lb |
| `ICO_Colombian_Milds_USc_per_lb` | ICO Colombian milds group indicator, weighted average | US cents / lb |
| `ICO_Other_Milds_USc_per_lb` | ICO other milds group indicator, weighted average (the series the World Bank Pink Sheet *Coffee, Arabica* follows) | US cents / lb |

**Converting the internal price to green coffee.** At factor 94 a carga of 125 kg parchment yields 93.09 kg of excelso (FNC daily price sheet, 2026-10-07; RES row). A per-kg-green internal price is `Internal_Price_COP_per_carga / 93.09` for months at factor 94. The calibration uses only those months. The FNC states that the 2024 factor change "does not affect what the producer receives", i.e. the carga price moved with the factor.

**Validation (run %s).** Schema: seven columns. Coverage: internal price continuous monthly from 1944 in the source, kept from 2000; ICO columns from 2000-01. Units read from the sheet headers. Plausibility: the ex-dock price tracks the ICO Colombian milds indicator within a few cents in every month checked.

%s
""" % (months[-1], source_url, C.now_iso(),
       C.provenance_block(DS, raw_log, "scripts/ingest/ds10_fnc_colombia.py", {"Source page": PAGE, "Workbook URL": source_url}))
    C.write_processed(NAME_PRICES, header, out, md)

    # Area by department (thousand ha)
    rows = sheet("rea cult. dep"); h = header_row(rows, {"Departamento"}); hdr = rows[h]
    cd = next(j for j, c in enumerate(hdr) if c == "Departamento")
    years = [(j, int(str(c)[:4])) for j, c in enumerate(hdr) if j > cd and c is not None and str(c)[:4].isdigit()]
    area = []
    for r in rows[h + 1:]:
        if not r or len(r) <= cd or not isinstance(r[cd], str) or r[cd].startswith("*"):
            continue
        dep = r[cd].strip()
        for j, y in years:
            v = r[j] if len(r) > j else None
            if isinstance(v, (int, float)):
                area.append([dep, y, round(float(v), 3)])
    header_a = ["Department", "Year", "Area_kha"]
    md_a = """# DS-10 — Colombian coffee area by department (FNC / SICA)

One row per department per year, %d to %d (%d rows). Thousand hectares cultivated with coffee; source SICA (Sistema de Informacion Cafetera) as reproduced in the FNC workbook. Years marked with an asterisk in the source are cut at December; `n/d` cells are omitted. The source's `TOTAL` row is kept as a department named `TOTAL` so shares can be computed without re-summing.

| Column | Meaning | Unit |
|---|---|---|
| `Department` | Department name as the FNC writes it (accents as in source) | |
| `Year` | Calendar year | |
| `Area_kha` | Cultivated coffee area | thousand ha |

Used for the share of the national area in Huila and Cauca (the RT-7 Colombia districts). No department-level production is in the workbook, so department yields cannot be derived from it.

**Validation (run %s).** Schema: three columns; department names deduplicated as written; numeric values only.

%s
""" % (min(a[1] for a in area), max(a[1] for a in area), len(area), C.now_iso(),
       C.provenance_block(DS, raw_log, "scripts/ingest/ds10_fnc_colombia.py", {"Workbook URL": source_url}))
    C.write_processed(NAME_AREA, header_a, area, md_a)


def main():
    if "--no-fetch" not in sys.argv:
        url = find_link()
        print("fetching %s" % url)
        data = C.fetch(url, timeout=180)
        raw_path, log = C.save_raw(DS, "fnc-precios-area-produccion-%s.xlsx" % C.today(), data,
                                   {"url": url, "method": "GET", "found_on": PAGE},
                                   "Whole workbook as published by the FNC.")
        print("raw: %s (%d bytes)" % (os.path.relpath(raw_path, C.ROOT), log["bytes"]))
    else:
        raw_path = C.latest_raw(DS, ".xlsx")
        if not raw_path:
            C.fail("no raw file; run without --no-fetch")
        log = json.load(open(raw_path + ".query.json")); url = log["request"]["url"]
    process(raw_path, log, url)


if __name__ == "__main__":
    main()
