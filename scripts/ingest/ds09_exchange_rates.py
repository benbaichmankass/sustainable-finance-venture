#!/usr/bin/env python3
"""DS-09: exchange rates to US dollars for the three RT-7 currencies.

    python3 scripts/ingest/ds09_exchange_rates.py            # fetch + process
    python3 scripts/ingest/ds09_exchange_rates.py --no-fetch

Two sources, kept in one processed file with a Source column:

  COP  Banco de la Republica's TRM (tasa representativa del mercado), daily,
       served by Colombia's open-data portal (datos.gov.co, Socrata API), and
       averaged to months here.
  ETB, VND  World Bank WDI PA.NUS.FCRF, official exchange rate, period
       average, annual. (Ethiopia floated the birr in July 2024; an annual
       average straddling that is a poor guide to either half of the year,
       and the dictionary says so.)

Raw:       data/raw/DS-09/trm-daily-<date>.json, data/raw/DS-09/wdi-fcrf-<date>.json
Processed: data/processed/ds-09-exchange-rates.csv (+ .md)
Python 3 stdlib.
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

DS = "DS-09"
NAME = "ds-09-exchange-rates"
TRM_URL = ("https://www.datos.gov.co/resource/32sa-8pi3.json?$limit=20000&$order=vigenciadesde%20ASC"
           "&$where=vigenciadesde%20%3E%3D%20%272003-01-01%27")
WDI_URL = "https://api.worldbank.org/v2/country/COL;ETH;VNM/indicator/PA.NUS.FCRF?format=json&per_page=200&date=2000:2025"


def process(trm_path, trm_log, wdi_path, wdi_log):
    trm = json.load(open(trm_path, encoding="utf-8"))
    by_month = defaultdict(list)
    for r in trm:
        by_month[r["vigenciadesde"][:7]].append(float(r["valor"]))
    rows = [["COP", m, "monthly", round(sum(v) / len(v), 4), len(v), "DS-09 TRM daily (datos.gov.co 32sa-8pi3), simple mean of daily values"]
            for m, v in sorted(by_month.items())]
    wdi = json.load(open(wdi_path, encoding="utf-8"))[1]
    iso = {"COL": "COP", "ETH": "ETB", "VNM": "VND"}
    for r in sorted(wdi, key=lambda x: (x["countryiso3code"], x["date"])):
        if r["value"] is None:
            continue
        rows.append([iso[r["countryiso3code"]], r["date"], "annual", round(float(r["value"]), 4), "",
                     "DS-09 WDI PA.NUS.FCRF official rate, period average"])
    header = ["Currency", "Period", "Frequency", "LCU_per_USD", "N_Daily_Obs", "Source"]
    cop = [r for r in rows if r[0] == "COP" and r[2] == "monthly"]
    md = """# DS-09 — exchange rates to the US dollar

Two series in one file, distinguished by `Frequency` and `Source`.

| Column | Meaning |
|---|---|
| `Currency` | `COP`, `ETB`, `VND` |
| `Period` | `YYYY-MM` for monthly rows, `YYYY` for annual rows |
| `Frequency` | `monthly` or `annual` |
| `LCU_per_USD` | Local currency units per US dollar |
| `N_Daily_Obs` | For COP months, the number of daily TRM values averaged |
| `Source` | Which series the row came from |

**COP.** Banco de la Republica's TRM, daily, %s to %s (%d months), via Colombia's open-data portal. Monthly rows are the simple mean of the daily values in the month.

**ETB and VND.** World Bank WDI official exchange rate (period average), annual, 2000 onward where published. Annual rows also exist for COP as a cross-check. Caveat: Ethiopia moved to a market-determined rate in July 2024, so the 2024 annual average (about 83) sits between the pre-float level (about 57) and the post-float level (above 110); use it for 2024 figures with care, and prefer a source's own stated rate where a document gives one.

**Validation (run %s).** Schema: six columns. Coverage: every complete month from the first TRM month has at least 15 daily observations (the TRM is published for business days, about 20 a month); the current month is partial and its N_Daily_Obs says so. Units: local currency per USD in both sources, no conversion applied.

%s
""" % (cop[0][1], cop[-1][1], len(cop), C.now_iso(),
       C.provenance_block(DS, trm_log, "scripts/ingest/ds09_exchange_rates.py",
                          {"TRM request": TRM_URL, "WDI request": WDI_URL, "WDI raw SHA-256": wdi_log["sha256"]}))
    thin = [r for r in cop if r[4] < 15]
    if thin:
        print("  note: %d COP months with fewer than 15 daily observations: %s" % (len(thin), [r[1] for r in thin][:6]))
    C.write_processed(NAME, header, rows, md)


def main():
    if "--no-fetch" not in sys.argv:
        print("fetching TRM daily (datos.gov.co)")
        trm = C.fetch(TRM_URL, timeout=180)
        trm_path, trm_log = C.save_raw(DS, "trm-daily-%s.json" % C.today(), trm, {"url": TRM_URL, "method": "GET"},
                                       "Verbatim Socrata JSON response; TRM is published by Banco de la Republica.")
        print("fetching WDI official exchange rates")
        wdi = C.fetch(WDI_URL, timeout=180)
        wdi_path, wdi_log = C.save_raw(DS, "wdi-fcrf-%s.json" % C.today(), wdi, {"url": WDI_URL, "method": "GET"},
                                       "Verbatim World Bank API JSON response.")
    else:
        trm_path, wdi_path = C.latest_raw(DS, ".json"), None
        for f in sorted(os.listdir(C.raw_dir(DS))):
            if f.endswith(".query.json"):
                continue
            if f.startswith("trm-daily") and f.endswith(".json"): trm_path = os.path.join(C.raw_dir(DS), f)
            if f.startswith("wdi-fcrf") and f.endswith(".json"): wdi_path = os.path.join(C.raw_dir(DS), f)
        if not (trm_path and wdi_path):
            C.fail("raw files missing; run without --no-fetch")
        trm_log = json.load(open(trm_path + ".query.json")); wdi_log = json.load(open(wdi_path + ".query.json"))
    process(trm_path, trm_log, wdi_path, wdi_log)


if __name__ == "__main__":
    main()
