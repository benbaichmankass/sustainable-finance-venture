#!/usr/bin/env python3
"""RT-3 scaffold: portfolio monitoring and early warning over RT-1 events.

    python3 risk-tools/tools/generate_dataset.py --out /tmp/synth
    python3 risk-tools/tools/monitor_portfolio.py --data /tmp/synth
    python3 risk-tools/tools/monitor_portfolio.py --data /tmp/synth --as-of 2027-06-30

The point of this tool is to fire BEFORE a loss crystallises. A write-off is
not a warning, it is an outcome; by the time it lands the money is gone and
the only remaining question is how it is reported. What RT-3 watches is the
arrears that precede it.

That is also what makes the junior tranche fundable. LIT-013 is explicit that
a documented monitoring regime is part of what a first-loss provider is
buying - they are taking the risk, so they need to see it moving before it
arrives.

Alerts are thresholds, not predictions. Every one states the number that
tripped it so it can be argued with rather than believed.

Python 3 stdlib only.
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from datetime import date

MODEL_VERSION = "0.1"

# Thresholds. Judgement, not estimates - and deliberately visible at the top of
# the file rather than buried, because they are the first thing that should be
# argued about and the first thing real data should replace.
THRESHOLDS = {
    "par30_pct": 8.0,           # portfolio at risk > 30 days, % of outstanding
    "par90_pct": 4.0,
    "group_arrears_pct": 25.0,  # share of a group's loans in arrears
    "geo_arrears_pct": 15.0,    # share of a region's loans in arrears - correlation flag
    "originator_spread_pp": 10.0,   # gap between best and worst originator PAR30
    "arrears_trend_pp": 3.0,    # month-on-month rise in new arrears
}

ARREARS_EVENTS = {"missed_payment", "arrears_flagged"}
TERMINAL_EVENTS = {"write_off"}


def load(data_dir):
    out = {}
    for name in ("group", "loan", "event"):
        with open(os.path.join(data_dir, name + ".csv"), newline="", encoding="utf-8") as fh:
            out[name] = list(csv.DictReader(fh))
    return out


def num(row, key, default=0.0):
    try:
        return float(row.get(key, "") or default)
    except ValueError:
        return default


def analyse(data, as_of):
    loans = {l["loan_id"]: l for l in data["loan"]}
    groups = {g["group_id"]: g for g in data["group"]}

    # Walk the event stream in date order and keep the latest state per loan.
    # Ordering matters: a recovery after a write-off means something different
    # from the reverse, and an unsorted stream silently produces the wrong one.
    events = sorted((e for e in data["event"] if e["event_date"] <= as_of),
                    key=lambda e: (e["event_date"], e["event_id"]))

    state = {}
    new_arrears_by_month = defaultdict(int)
    for e in events:
        lid = e["event_loan_id"]
        s = state.setdefault(lid, {"dpd": 0, "balance": None, "status": "current",
                                   "last": None, "ever_arrears": False})
        s["dpd"] = int(num(e, "event_days_past_due"))
        s["balance"] = num(e, "event_balance_after")
        s["last"] = e["event_date"]
        if e["event_type"] in ARREARS_EVENTS:
            if not s["ever_arrears"]:
                new_arrears_by_month[e["event_date"][:7]] += 1
            s["ever_arrears"] = True
            s["status"] = "arrears"
        elif e["event_type"] in TERMINAL_EVENTS:
            s["status"] = "written_off"
        elif s["dpd"] == 0 and s["status"] != "written_off":
            s["status"] = "current"

    outstanding = par30 = par90 = written_off = 0.0
    by_group = defaultdict(lambda: {"n": 0, "arrears": 0})
    by_geo = defaultdict(lambda: {"n": 0, "arrears": 0})
    by_orig = defaultdict(lambda: {"outstanding": 0.0, "par30": 0.0})

    for lid, s in state.items():
        loan = loans.get(lid)
        if not loan:
            continue
        bal = s["balance"] or 0.0
        grp = groups.get(loan["loan_group_id"], {})
        geo = grp.get("group_admin1", "?")
        orig = grp.get("group_originator_id", "?")

        by_group[loan["loan_group_id"]]["n"] += 1
        by_geo[geo]["n"] += 1
        if s["status"] == "written_off":
            written_off += num(loan, "loan_principal")
            continue

        outstanding += bal
        by_orig[orig]["outstanding"] += bal
        if s["status"] == "arrears":
            by_group[loan["loan_group_id"]]["arrears"] += 1
            by_geo[geo]["arrears"] += 1
        if s["dpd"] >= 30:
            par30 += bal
            by_orig[orig]["par30"] += bal
        if s["dpd"] >= 90:
            par90 += bal

    pct = lambda a, b: (100 * a / b) if b else 0.0
    return {
        "as_of": as_of,
        "loans_tracked": len(state),
        "outstanding": outstanding,
        "written_off": written_off,
        "par30_pct": pct(par30, outstanding),
        "par90_pct": pct(par90, outstanding),
        "by_group": by_group, "by_geo": by_geo, "by_orig": by_orig,
        "new_arrears_by_month": dict(sorted(new_arrears_by_month.items())),
    }


def alerts(a):
    """Threshold breaches, most severe first. Each carries its own number."""
    out = []

    if a["par30_pct"] > THRESHOLDS["par30_pct"]:
        out.append(("critical", "PAR30 %.1f%% exceeds %.1f%% threshold"
                    % (a["par30_pct"], THRESHOLDS["par30_pct"])))
    if a["par90_pct"] > THRESHOLDS["par90_pct"]:
        out.append(("critical", "PAR90 %.1f%% exceeds %.1f%% threshold"
                    % (a["par90_pct"], THRESHOLDS["par90_pct"])))

    # Geographic concentration is the one that matters most for a pooled
    # structure: several regions deteriorating together is the correlated-loss
    # scenario RT-5 is most sensitive to, and it is visible here first.
    hot_geo = [(g, 100 * v["arrears"] / v["n"]) for g, v in a["by_geo"].items()
               if v["n"] >= 20 and 100 * v["arrears"] / v["n"] > THRESHOLDS["geo_arrears_pct"]]
    for g, p in sorted(hot_geo, key=lambda x: -x[1])[:5]:
        out.append(("serious", "region %s at %.1f%% arrears (threshold %.1f%%)"
                    % (g, p, THRESHOLDS["geo_arrears_pct"])))
    if len(hot_geo) >= 3:
        out.append(("critical", "%d regions above the arrears threshold simultaneously - "
                    "consistent with a correlated shock, not idiosyncratic default" % len(hot_geo)))

    hot_groups = [(g, 100 * v["arrears"] / v["n"]) for g, v in a["by_group"].items()
                  if v["n"] >= 4 and 100 * v["arrears"] / v["n"] > THRESHOLDS["group_arrears_pct"]]
    if hot_groups:
        out.append(("warning", "%d groups above %.0f%% arrears - worst %s at %.0f%%"
                    % (len(hot_groups), THRESHOLDS["group_arrears_pct"],
                       max(hot_groups, key=lambda x: x[1])[0],
                       max(p for _, p in hot_groups))))

    pars = [(o, 100 * v["par30"] / v["outstanding"]) for o, v in a["by_orig"].items()
            if v["outstanding"] > 0]
    if len(pars) >= 2:
        best, worst = min(pars, key=lambda x: x[1]), max(pars, key=lambda x: x[1])
        if worst[1] - best[1] > THRESHOLDS["originator_spread_pp"]:
            out.append(("warning", "originator PAR30 spread %.1fpp (%s %.1f%% vs %s %.1f%%) - "
                        "underwriting quality is not uniform across the pool"
                        % (worst[1] - best[1], worst[0], worst[1], best[0], best[1])))

    months = list(a["new_arrears_by_month"].items())
    if len(months) >= 2:
        prev, last = months[-2][1], months[-1][1]
        if prev and last > prev * 1.5:
            out.append(("serious", "new arrears rose from %d to %d month-on-month (+%.0f%%) - "
                        "leading indicator, before any write-off lands"
                        % (prev, last, 100 * (last - prev) / prev)))

    order = {"critical": 0, "serious": 1, "warning": 2}
    return sorted(out, key=lambda x: order[x[0]])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="directory of RT-1 entity CSVs")
    ap.add_argument("--as-of", default="2099-12-31", help="evaluate as at this date (ISO)")
    args = ap.parse_args()

    a = analyse(load(args.data), args.as_of)

    print("RT-3 MONITOR v%s - SYNTHETIC data, uncalibrated thresholds" % MODEL_VERSION)
    print("  as at %s, %d loans tracked\n" % (a["as_of"], a["loans_tracked"]))
    print("  outstanding      %12s" % format(round(a["outstanding"]), ","))
    print("  written off      %12s" % format(round(a["written_off"]), ","))
    print("  PAR30            %11.2f%%" % a["par30_pct"])
    print("  PAR90            %11.2f%%" % a["par90_pct"])

    if a["new_arrears_by_month"]:
        print("\n  New arrears by month (the leading signal):")
        peak = max(a["new_arrears_by_month"].values())
        for month, n in list(a["new_arrears_by_month"].items())[-9:]:
            print("    %s  %4d  %s" % (month, n, "#" * int(34 * n / peak)))

    fired = alerts(a)
    print("\n  ALERTS: %d\n" % len(fired))
    for level, msg in fired:
        print("    [%-8s] %s" % (level.upper(), msg))
    if not fired:
        print("    none - every monitored threshold is within tolerance")

    print("\n  Thresholds are judgement, not estimates. Each alert states the number that")
    print("  tripped it so it can be argued with. See risk-tools/rt-3-monitoring-early-warning.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
