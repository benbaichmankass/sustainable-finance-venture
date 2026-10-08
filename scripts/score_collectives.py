#!/usr/bin/env python3
"""Score the collective market map on the readiness scorecard.

    python3 scripts/score_collectives.py            # recompute Score_Total and Readiness_Band in place
    python3 scripts/score_collectives.py --check    # report only, exit 1 if the file is stale

Reads data/collective-market-map.csv. A row is scored only when all ten
Score_* columns carry an integer 1..5; otherwise Score_Total and
Readiness_Band are left blank, which is the honest state for a longlist row.
Bands follow docs/research/methodology-collective-screening.md:
40-50 structured-pilot candidate, 30-39 limited pilot, below 30 research
prospect. The cutoffs are provisional and the doc says so.

Python 3 stdlib only.
"""

from __future__ import annotations

import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "collective-market-map.csv")

DIMENSIONS = [
    "Score_Observability", "Score_Contractability", "Score_Diversification", "Score_Governance",
    "Score_Loss_History", "Score_Climate_Measurability", "Score_Price_Control", "Score_Servicing",
    "Score_Regulatory", "Score_Member_Alignment",
]
BANDS = [(40, "Structured-pilot candidate"), (30, "Limited pilot"), (0, "Research prospect")]


def score(row):
    vals = []
    for d in DIMENSIONS:
        v = (row.get(d) or "").strip()
        if not v:
            return "", ""
        try:
            n = int(v)
        except ValueError:
            raise ValueError("%s: %s is %r, not an integer" % (row["ID"], d, v))
        if not 1 <= n <= 5:
            raise ValueError("%s: %s is %d, outside 1..5" % (row["ID"], d, n))
        vals.append(n)
    total = sum(vals)
    band = next(b for cutoff, b in BANDS if total >= cutoff)
    return str(total), band


def main():
    check = "--check" in sys.argv
    with open(PATH, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fields = reader.fieldnames
    stale = 0
    for r in rows:
        total, band = score(r)
        if r.get("Score_Total", "") != total or r.get("Readiness_Band", "") != band:
            stale += 1
            print("  %s: %s -> total %s, band %s" % (r["ID"], r["Entity_Name"][:40], total or "-", band or "-"))
        r["Score_Total"], r["Readiness_Band"] = total, band
    scored = sum(1 for r in rows if r["Score_Total"])
    print("%d rows, %d scored, %d %s" % (len(rows), scored, stale, "stale" if check else "updated"))
    if check:
        return 1 if stale else 0
    with open(PATH, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
