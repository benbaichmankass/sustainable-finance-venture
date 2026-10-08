#!/usr/bin/env python3
"""RT-7 pipeline: run every region through every scenario, plus the
one-at-a-time sensitivity, and write the headline rows the dashboard reads.

    python3 risk-tools/collective/run_region.py                  # all regions
    python3 risk-tools/collective/run_region.py --region ethiopia
    python3 risk-tools/collective/run_region.py --paths 20000 --tornado-paths 5000

Writes (committed, read by dashboard/build.py):
    data/rt7-region-results.csv    one row per region x scenario
    data/rt7-sensitivity.csv       one row per region x tornado parameter

Writes (gitignored, regenerable):
    risk-tools/collective/output/<region>/run_manifest.json   every parameter with
        its provenance, the scenario results, seed, path count, model version and
        git commit - "a result without its assumptions is not a result"
    risk-tools/collective/output/<region>/summary.md          a short readable summary

Every output row carries Basis: SYNTHETIC. The parameters are partially
calibrated; the collective is synthetic. The empirical climate factor reads
data/rt7-climate-history.csv when it exists (DS-02).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import rt7_model as M  # noqa: E402
import rt7_params as P  # noqa: E402

BASIS = "SYNTHETIC - illustrative only, not calibrated to field data"
RESULTS_CSV = os.path.join(ROOT, "data", "rt7-region-results.csv")
SENS_CSV = os.path.join(ROOT, "data", "rt7-sensitivity.csv")
OUT_DIR = os.path.join(HERE, "output")


def pct(x, nd=3):
    return "%.*f" % (nd, 100.0 * x)


def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return ""


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def result_row(region, scen, r, seed):
    t = r["tranches"]
    att = r["attachment_for_senior_target"]
    return {
        "Region": region,
        "Scenario_ID": scen["id"],
        "Scenario": scen["name"],
        "Pool_Notional_USD": "%.2f" % r["pool_notional_usd"],
        "Borrowers": str(r["n_borrowers"]),
        "EL_Pct": pct(r["el_pct"]),
        "UL95_Pct": pct(r["ul95_pct"]),
        "UL99_Pct": pct(r["ul99_pct"]),
        "Member_EL_Pct": pct(r["member_el_pct"]),
        "Mean_PD_Pct": pct(r["mean_pd"], 2),
        "Normal_Year_PD_Pct": pct(r["normal_year_pd"], 2),
        "Share_DSCR_Below_1_Pct": pct(r["share_dscr_below_1"], 1),
        "P_Shortfall_Pct": pct(r["p_shortfall"], 1),
        "P_Side_Selling_Pct": pct(r["p_side_selling"], 1),
        "P_Collective_Deficit_Pct": pct(r["p_collective_deficit"], 1),
        "Mean_Buffer_Absorbed_USD": "%.0f" % r["mean_buffer_absorbed_usd"],
        "Equity_EL_Pct": pct(t["equity"]["el_pct"], 2),
        "Mezz_EL_Pct": pct(t["mezz"]["el_pct"], 2),
        "Senior_EL_Pct": pct(t["senior"]["el_pct"], 3),
        "Senior_UL99_Pct": pct(t["senior"]["ul99_pct"], 2),
        "Attachment_For_Senior_Target_Pct": "" if att >= 1.0 else pct(att, 1),
        "Horizon_Seasons": str(r.get("horizon_seasons", 1)),
        "EL_Annualised_Pct": pct(r.get("el_annualised_pct", r["el_pct"])),
        "EL_Per_Season_Pct": "; ".join(pct(x, 3) for x in r.get("el_per_season_pct", [r["el_pct"]])),
        "Shortfall_Outside_Facility_USD": "%.0f" % r.get("mean_shortfall_outside_facility_usd", 0.0),
        "N_Paths": str(r["n_paths"]),
        "Seed": str(seed),
        "Model_Version": r["model_version"],
        "Basis": BASIS,
    }


def summary_md(region, label, base, scen_rows, tornado_rows, p, n_paths, seed):
    lines = [
        "# RT-7 run summary: %s" % label,
        "",
        "**Basis: SYNTHETIC.** Every parameter is an assumption until the data catalogue says otherwise. "
        "These figures describe the model, not the collective.",
        "",
        "| | |",
        "|---|---|",
        "| Pool notional | USD %s across %d borrowers of %d members |" % (
            "{:,.0f}".format(base["pool_notional_usd"]), base["n_borrowers"], base["n_members"]),
        "| Expected loss | %s of pool |" % pct(base["el_pct"], 2),
        "| UL95 / UL99 | %s / %s |" % (pct(base["ul95_pct"], 1), pct(base["ul99_pct"], 1)),
        "| Normal-year PD implied by leverage | %s (base PD priors %s CapEx, %s OpEx) |" % (
            pct(base["normal_year_pd"], 1), pct(p["base_pd_capex"], 1), pct(p["base_pd_opex"], 1)),
        "| Paths with side-selling / forward shortfall | %s / %s |" % (
            pct(base["p_side_selling"], 0), pct(base["p_shortfall"], 0)),
        "| First-loss needed for a %d bp senior EL | %s |" % (
            int(p["senior_el_target_bp"]),
            "not attainable" if base["attachment_for_senior_target"] >= 1 else pct(base["attachment_for_senior_target"], 1)),
        "",
        "## Scenarios",
        "",
        "| Scenario | EL | UL99 | P(shortfall) | P(collective deficit) |",
        "|---|---|---|---|---|",
    ]
    for s, r in scen_rows:
        lines.append("| %s | %s | %s | %s | %s |" % (s["name"], pct(r["el_pct"], 2), pct(r["ul99_pct"], 1),
                                                   pct(r["p_shortfall"], 0), pct(r["p_collective_deficit"], 0)))
    lines += ["", "## Sensitivity (one at a time, EL in percent of pool)", "",
              "| Parameter | Low | High | EL at low | EL at high |", "|---|---|---|---|---|"]
    for t in tornado_rows:
        lines.append("| %s | %g | %g | %s | %s |" % (t["parameter"], round(t["value_low"], 4),
                                                   round(t["value_high"], 4), pct(t["el_low"], 2), pct(t["el_high"], 2)))
    lines += ["", "Run: %d paths, seed %d, model v%s, %s." % (
        n_paths, seed, M.MODEL_VERSION, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--region", default="all", help="region key from data/rt7-regions.csv, or all")
    ap.add_argument("--paths", type=int, default=5000)
    ap.add_argument("--tornado-paths", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--no-tornado", action="store_true")
    args = ap.parse_args()

    problems = P.validate()
    if problems:
        for pr in problems:
            print("  !", pr, file=sys.stderr)
        print("parameter tracker has %d problem(s); refusing to run" % len(problems), file=sys.stderr)
        return 1

    regions = P.load_regions()
    scenarios = P.load_scenarios()
    wanted = [r for r in regions if args.region == "all" or r["Region"] == args.region]
    if not wanted:
        print("unknown region %r" % args.region, file=sys.stderr)
        return 1

    # Keep rows for regions not being run, so a single-region run does not
    # drop the others from the committed table.
    existing = {}
    if os.path.exists(RESULTS_CSV):
        with open(RESULTS_CSV, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                existing.setdefault(r["Region"], []).append(r)
    existing_s = {}
    if os.path.exists(SENS_CSV):
        with open(SENS_CSV, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                existing_s.setdefault(r["Region"], []).append(r)

    commit = git_commit()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    histories = P.load_climate_history()

    for reg in wanted:
        region = reg["Region"]
        p = P.region_params(region)
        print("== %s" % reg["Label"])
        scen_rows = []
        hist = histories.get(region)
        for s in scenarios:
            r = M.simulate(p, args.paths, args.seed, s, climate_history=hist)
            scen_rows.append((s, r))
            print("   %-6s %-28s EL %6s%%  UL99 %6s%%  shortfall %4s%%" % (
                s["id"], s["name"], pct(r["el_pct"], 2), pct(r["ul99_pct"], 1), pct(r["p_shortfall"], 0)))
        base = scen_rows[0][1]
        existing[region] = [result_row(region, s, r, args.seed) for s, r in scen_rows]

        trows = []
        if not args.no_tornado:
            _, trows = M.tornado(p, args.tornado_paths, args.seed, scenarios[0], climate_history=hist)
            existing_s[region] = [{
                "Region": region, "Parameter": t["parameter"], "How": t["how"],
                "Value_Low": "%g" % t["value_low"], "Value_High": "%g" % t["value_high"],
                "EL_Base_Pct": pct(t["el_base"]), "EL_Low_Pct": pct(t["el_low"]), "EL_High_Pct": pct(t["el_high"]),
                "UL99_Base_Pct": pct(t["ul99_base"]), "UL99_Low_Pct": pct(t["ul99_low"]), "UL99_High_Pct": pct(t["ul99_high"]),
                "Swing_EL_Pct": pct(t["swing_el"]), "N_Paths": str(args.tornado_paths), "Basis": BASIS,
            } for t in trows]
            print("   tornado: top driver %s (EL %s%% .. %s%%)" % (
                trows[0]["parameter"], pct(trows[0]["el_low"], 2), pct(trows[0]["el_high"], 2)))

        out = os.path.join(OUT_DIR, region)
        os.makedirs(out, exist_ok=True)
        manifest = {
            "region": reg, "model_version": M.MODEL_VERSION, "git_commit": commit, "run_at_utc": stamp,
            "n_paths": args.paths, "tornado_paths": args.tornado_paths, "seed": args.seed, "basis": BASIS,
            "parameters": P.provenance(region),
            "climate_history_years": len(hist) if hist else 0,
            "scenarios": [{"scenario": s, "result": {k: v for k, v in r.items() if k != "loss_histogram"}}
                          for s, r in scen_rows],
            "sensitivity": trows,
        }
        with open(os.path.join(out, "run_manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=1, default=float)
        with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as fh:
            fh.write(summary_md(region, reg["Label"], base, scen_rows, trows, p, args.paths, args.seed))

    order = [r["Region"] for r in regions]
    rows = [row for region in order for row in existing.get(region, [])]
    write_csv(RESULTS_CSV, list(rows[0].keys()), rows)
    print("wrote %s (%d rows)" % (os.path.relpath(RESULTS_CSV, ROOT), len(rows)))
    srows = [row for region in order for row in existing_s.get(region, [])]
    if srows:
        write_csv(SENS_CSV, list(srows[0].keys()), srows)
        print("wrote %s (%d rows)" % (os.path.relpath(SENS_CSV, ROOT), len(srows)))
    print("manifests under %s" % os.path.relpath(OUT_DIR, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
