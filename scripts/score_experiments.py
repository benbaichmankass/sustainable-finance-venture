#!/usr/bin/env python3
"""Recompute the Composite score and Priority_Band in data/experiments.csv.

The composite is a weighted mean of five 1-5 judgement scores. Keeping it in a
script rather than a spreadsheet formula means the weights are reviewable, the
ranking is reproducible, and reweighting is one edit instead of a manual re-rank.

    python3 scripts/score_experiments.py            # rewrite Composite + Priority_Band
    python3 scripts/score_experiments.py --check    # verify, non-zero exit on drift
    python3 scripts/score_experiments.py --rank     # print the ranking

The weights follow the research-first resolution of OQ-9: evidence value leads,
and the asset/structuring side acts as a filter rather than a driver. The rubric
behind each 1-5 anchor is in docs/research/experiment-spec-template.md.

Python 3 stdlib only - no install step, matching risk-tools/tools/.
"""

import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "experiments.csv")

WEIGHTS = {
    "Research_Significance": 0.35,
    "PhD_Feasibility": 0.30,
    "Partner_Availability": 0.15,
    "Implementation_Ease": 0.10,
    "Grant_Exposure": 0.10,
}

# Composite lower bound -> band. Checked high to low.
BANDS = [
    (4.00, "Flagship candidate"),
    (3.40, "Strong"),
    (2.80, "Reserve"),
    (0.00, "Park"),
]


def band_for(score):
    for floor, label in BANDS:
        if score >= floor:
            return label
    return BANDS[-1][1]


def composite(row):
    total = 0.0
    for field, weight in WEIGHTS.items():
        raw = (row.get(field) or "").strip()
        if not raw:
            raise ValueError("%s: %s is empty" % (row["ID"], field))
        value = int(raw)
        if not 1 <= value <= 5:
            raise ValueError("%s: %s = %d is outside 1-5" % (row["ID"], field, value))
        total += value * weight
    return round(total, 2)


def load():
    raw = open(PATH, "rb").read()
    term = "\r\n" if b"\r\n" in raw else "\n"
    with open(PATH, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return rows, list(rows[0].keys()), term


def save(rows, cols, term):
    with open(PATH, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, quoting=csv.QUOTE_ALL,
                                lineterminator=term)
        writer.writeheader()
        writer.writerows(rows)


def main():
    check = "--check" in sys.argv
    rank = "--rank" in sys.argv
    rows, cols, term = load()

    drift = []
    for row in rows:
        want = composite(row)
        want_band = band_for(want)
        have = (row.get("Composite") or "").strip()
        have_band = (row.get("Priority_Band") or "").strip()
        if have != ("%.2f" % want) or have_band != want_band:
            drift.append((row["ID"], have, "%.2f" % want, have_band, want_band))
        row["Composite"] = "%.2f" % want
        row["Priority_Band"] = want_band

    if check:
        if drift:
            print("Composite drift in %d row(s):" % len(drift), file=sys.stderr)
            for rid, have, want, hband, wband in drift:
                print("  %-8s %s -> %s   %s -> %s"
                      % (rid, have or "(blank)", want, hband or "(blank)", wband),
                      file=sys.stderr)
            return 1
        print("All %d composites agree with their component scores." % len(rows))
        return 0

    save(rows, cols, term)
    print("Scored %d experiments (weights: %s)"
          % (len(rows), ", ".join("%s %.0f%%" % (k.split("_")[0], v * 100)
                                  for k, v in WEIGHTS.items())))
    if drift:
        print("  updated %d row(s)" % len(drift))

    if rank:
        print()
        ordered = sorted(rows, key=lambda r: -float(r["Composite"]))
        print("  %-8s %-6s %-19s %-26s %s" % ("ID", "Score", "Band", "Type", "Theme"))
        for row in ordered:
            print("  %-8s %-6s %-19s %-26s %s"
                  % (row["ID"], row["Composite"], row["Priority_Band"],
                     row["Type"][:26], row["Theme"][:40]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
