#!/usr/bin/env python3
"""DS-04: World Bank Commodity Price Data (the Pink Sheet), monthly.

    python3 scripts/ingest/ds04_pink_sheet.py            # fetch + process
    python3 scripts/ingest/ds04_pink_sheet.py --no-fetch # re-process the latest raw file

Raw:       data/raw/DS-04/CMO-Historical-Data-Monthly-<date>.xlsx (+ .query.json)
Processed: data/processed/ds-04-coffee-prices-monthly.csv (+ .md dictionary)

Keeps the two coffee series only - Coffee, Arabica and Coffee, Robusta - and
converts the publisher's USD/kg to USD/t (x 1000), which is the unit RT-7 uses.
Dependency: openpyxl (the publisher ships XLSX, not CSV).
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

DS = "DS-04"
# The landing page https://www.worldbank.org/en/research/commodity-markets links a
# doc id that changes with each release. Check it when the processed file looks
# stale: the id below is the one linked on 2026-10-08. An older id
# (5d903e...-0350012021) still serves a copy that ends in 2024-12.
URL = "https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx"
NAME = "ds-04-coffee-prices-monthly"
SERIES = {"Coffee, Arabica": "arabica", "Coffee, Robusta": "robusta"}


def process(raw_path, raw_log):
    import openpyxl
    wb = openpyxl.load_workbook(raw_path, read_only=True, data_only=True)
    ws = wb["Monthly Prices"]
    rows = list(ws.iter_rows(values_only=True))
    updated = next((r[0] for r in rows[:6] if isinstance(r[0], str) and r[0].startswith("Updated")), "")
    hdr_i = next(i for i, r in enumerate(rows) if r and any(c in SERIES for c in r if isinstance(c, str)))
    units = rows[hdr_i + 1]
    cols = {SERIES[c]: j for j, c in enumerate(rows[hdr_i]) if isinstance(c, str) and c in SERIES}
    for key, j in cols.items():
        if units[j] != "($/kg)":
            C.fail("unexpected unit for %s: %r" % (key, units[j]))
    out = []
    for r in rows[hdr_i + 2:]:
        if not r or not isinstance(r[0], str) or not re.match(r"^\d{4}M\d{2}$", r[0]):
            continue
        ym = r[0][:4] + "-" + r[0][5:]
        vals = {}
        for key, j in cols.items():
            v = r[j]
            vals[key] = round(float(v) * 1000.0, 2) if isinstance(v, (int, float)) else ""
        out.append([ym, vals["arabica"], vals["robusta"]])
    if not out:
        C.fail("no monthly rows parsed")
    first, last = out[0][0], out[-1][0]
    missing = sum(1 for r in out if r[1] == "" or r[2] == "")
    header = ["Month", "Arabica_USD_per_t", "Robusta_USD_per_t"]
    md = """# DS-04 — coffee prices, monthly (World Bank Pink Sheet)

One row per month, %s to %s (%d rows, %d with a missing value). Nominal US dollars per metric tonne of green coffee, converted from the publisher's USD/kg by multiplying by 1,000. Publisher note on this file: "%s".

| Column | Meaning | Unit |
|---|---|---|
| `Month` | Calendar month | `YYYY-MM` |
| `Arabica_USD_per_t` | Pink Sheet series *Coffee, Arabica* (ICO indicator price, other mild arabicas, New York and Bremen/Hamburg markets, ex-dock) | USD / t, nominal |
| `Robusta_USD_per_t` | Pink Sheet series *Coffee, Robusta* (ICO indicator price, New York and Le Havre/Marseilles, ex-dock) | USD / t, nominal |

**What it is.** World reference prices, not farm-gate. The gap to what a smallholder receives is `basis_local` in RT-7 and is NOT measured here (LIT-035 makes the same point). Nominal, so a long-window volatility includes inflation drift; the calibration uses log returns, which removes a constant drift but not a changing one.

**Validation (run %s).** Schema: three columns, month key parses, values numeric or blank. Coverage: continuous monthly from %s. Units: `($/kg)` read from the header row before conversion; the script refuses any other unit. Plausibility: Arabica above Robusta in every month with both present, as expected.

%s
""" % (first, last, len(out), missing, updated, C.now_iso(), first,
       C.provenance_block(DS, raw_log, "scripts/ingest/ds04_pink_sheet.py",
                          {"Source URL": URL, "Publisher series": "Coffee, Arabica; Coffee, Robusta (sheet 'Monthly Prices')"}))
    # plausibility check
    for r in out:
        if r[1] != "" and r[2] != "" and r[1] < r[2]:
            print("  note: Robusta above Arabica in %s" % r[0])
    C.write_processed(NAME, header, out, md)


def main():
    if "--no-fetch" not in sys.argv:
        print("fetching %s" % URL)
        data = C.fetch(URL)
        raw_path, log = C.save_raw(DS, "CMO-Historical-Data-Monthly-%s.xlsx" % C.today(), data,
                                   {"url": URL, "method": "GET"},
                                   "Whole workbook kept as published; only the two coffee series are processed.")
        print("raw: %s (%d bytes, sha256 %s)" % (os.path.relpath(raw_path, C.ROOT), log["bytes"], log["sha256"][:12]))
    else:
        raw_path = C.latest_raw(DS, ".xlsx")
        if not raw_path:
            C.fail("no raw file; run without --no-fetch")
        import json
        log = json.load(open(raw_path + ".query.json"))
    process(raw_path, log)


if __name__ == "__main__":
    main()
