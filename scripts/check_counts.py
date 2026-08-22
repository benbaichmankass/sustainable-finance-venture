#!/usr/bin/env python3
"""Assert that hand-written counts in the prose match what the trackers contain.

The previous pass shipped three wrong figures in docs/research/research-agenda.md -
tier totals that had been typed rather than computed. Prose and CSVs drift the moment
one of them is edited alone, and nothing else in the repo notices. This does.

    python3 scripts/check_counts.py          # report, non-zero exit on mismatch

Add a claim here whenever a document states a number that a tracker also knows.
Python 3 stdlib only.
"""

import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel):
    with open(os.path.join(ROOT, rel), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def refs(value):
    return [x.strip() for x in (value or "").split(";") if x.strip()]


def text(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def main():
    lc = load("data/lit-components.csv")
    rq = load("data/research-questions.csv")
    exp = load("data/experiments.csv")
    lit = load("literature/lit-matrix.csv")

    tiers = {}
    for tier in ("P1", "P2", "P3"):
        sel = [r for r in lc if r["Priority"] == tier]
        tiers[tier] = {
            "components": len(sel),
            "target": sum(int(r["Target_Anchors"]) for r in sel),
            "filled": sum(len(refs(r["Current_Anchors"])) for r in sel),
        }
    total_target = sum(int(r["Target_Anchors"]) for r in lc)
    total_filled = sum(len(refs(r["Current_Anchors"])) for r in lc)
    distinct = len({x for r in lc for x in refs(r["Current_Anchors"])})
    p1_new = tiers["P1"]["target"] - tiers["P1"]["filled"]

    strands = len([r for r in rq if r["Tier"] == "Strand"])
    subs = len([r for r in rq if r["Tier"] == "Sub"])

    # (file, regex that must match, what it should say, actual value)
    claims = [
        ("docs/research/research-agenda.md",
         r"P1 - needed before the proposal goes out \((\d+) components, (\d+) anchors",
         (tiers["P1"]["components"], tiers["P1"]["target"])),
        ("docs/research/research-agenda.md",
         r"P2 - needed for the thesis, not for the first email \((\d+) components, (\d+) anchors\)",
         (tiers["P2"]["components"], tiers["P2"]["target"])),
        ("docs/research/research-agenda.md",
         r"P3 - context \((\d+) components, (\d+) anchors\)",
         (tiers["P3"]["components"], tiers["P3"]["target"])),
        ("docs/research/research-agenda.md",
         r"(\d+) cumulative target anchors\. Of those, (\d+) slots are already filled, by (\d+) distinct",
         (total_target, total_filled, distinct)),
        ("docs/research/research-agenda.md",
         r"P1: (\d+) targets, (\d+) filled, so (\d+) new rows",
         (tiers["P1"]["target"], tiers["P1"]["filled"], p1_new)),
        ("docs/research/research-agenda.md",
         r"P1 components read \(0 of (\d+) complete\)",
         (tiers["P1"]["components"],)),
        ("README.md",
         r"\| Research questions \| 1 core, (\d+) strands, (\d+) sub-questions",
         (strands, subs)),
        ("README.md",
         r"\| Literature components \| (\d+) . (\d+) are P1",
         (len(lc), tiers["P1"]["components"])),
        ("README.md",
         r"\| Literature anchors \| (\d+), all reviewed . against a P1 target of ~(\d+)",
         (len(lit), tiers["P1"]["target"])),
        ("README.md",
         r"\| Experiments \| (\d+) candidates",
         (len(exp),)),
    ]

    failures = []
    for rel, pattern, expected in claims:
        body = text(rel)
        m = re.search(pattern, body)
        if not m:
            failures.append("%s: no text matched /%s/ - the sentence was reworded, "
                            "so this check needs updating too" % (rel, pattern))
            continue
        got = tuple(int(g) for g in m.groups())
        if got != tuple(expected):
            failures.append("%s: says %s, trackers say %s  (/%s/)"
                            % (rel, got, tuple(expected), pattern))

    print("Tracker truth:")
    for tier in ("P1", "P2", "P3"):
        t = tiers[tier]
        print("  %-3s %2d components  %3d target  %2d filled"
              % (tier, t["components"], t["target"], t["filled"]))
    print("  total %d target, %d filled slots, %d distinct sources"
          % (total_target, total_filled, distinct))
    print("  %d RQ strands, %d sub-questions, %d experiments, %d literature anchors"
          % (strands, subs, len(exp), len(lit)))
    print()

    if failures:
        print("COUNT MISMATCH in %d claim(s):" % len(failures), file=sys.stderr)
        for f in failures:
            print("  " + f, file=sys.stderr)
        return 1
    print("All %d prose claims agree with the trackers." % len(claims))
    return 0


if __name__ == "__main__":
    sys.exit(main())
