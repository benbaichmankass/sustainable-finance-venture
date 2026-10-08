#!/usr/bin/env python3
"""RT-7 portfolio layer: many collectives, several regions, one global price
factor and correlated regional climate factors, pooled.

    python3 risk-tools/collective/rt7_portfolio.py                 # all scenarios
    python3 risk-tools/collective/rt7_portfolio.py --paths 10000

Reads data/rt7-portfolio.csv (one row per synthetic collective: region, size
relative to the region's n_members, seed) and the parameter tracker, and
writes:

    data/rt7-portfolio-results.csv     one row per scenario x level (portfolio,
                                       each region sub-pool, each collective)
    data/rt7-portfolio-histogram.csv   the portfolio loss distribution per scenario

Factor structure (per path and season):

    world climate W ~ N(0,1)
    region climate R_r = sqrt(kappa) W + sqrt(1 - kappa) H_r        kappa = portfolio_climate_cross_corr
    with an empirical district history: R_r <- beta_r B_r + sqrt(1 - beta_r^2) R_r
    collective climate C_c = sqrt(1 - lambda) R_r(c) + sqrt(lambda) E_c   lambda = collective_climate_idio_share
    price factor: one AR(1) series shared by every collective (price_persistence),
    one jump series shared by every collective

Each collective is then rt7_model.simulate with those factors injected. The
portfolio loss is the sum of the facility losses; "standalone" is the sum of
each collective's own UL99 (no diversification credit at all); "independent"
is the pooled UL99 if the collectives' losses were independent (each
collective's paths permuted on their own), which shows what the shared factors
cost. Tails are reported both as UL99 (a quantile, which is not subadditive:
for losses as lumpy as a single collective's, the quantile of an independent
sum can exceed the sum of the quantiles) and as ES99, the mean loss beyond the
99th percentile, which is coherent and is the figure to compare across the
three. This is EXP-27's simulation and the loss distribution RT-5's waterfall
consumes (OQ-18: does pooling diversify on the right axis?).

Dependency: numpy.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import rt7_model as M  # noqa: E402
import rt7_params as P  # noqa: E402

SPEC_CSV = os.path.join(ROOT, "data", "rt7-portfolio.csv")
RESULTS_CSV = os.path.join(ROOT, "data", "rt7-portfolio-results.csv")
HIST_CSV = os.path.join(ROOT, "data", "rt7-portfolio-histogram.csv")
BASIS = "SYNTHETIC - illustrative portfolio of synthetic collectives"


def pct(x, nd=3):
    return "%.*f" % (nd, 100.0 * x)


def es99(x):
    """Expected shortfall at 99 percent: mean of the worst 1 percent of paths."""
    x = np.sort(np.asarray(x, dtype=float))
    k = max(1, int(math.ceil(0.01 * len(x))))
    return float(x[-k:].mean())


def load_spec():
    with open(SPEC_CSV, newline="", encoding="utf-8") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def shared_factors(regions, params_by_region, n_paths, T, seed, histories, p_all):
    """Draw the world, regional and price factors once per scenario run."""
    rng = np.random.default_rng(seed)
    kappa = float(p_all.get("portfolio_climate_cross_corr", 0.0))
    rho_p = float(p_all.get("price_persistence", 0.0))
    S = n_paths
    world = rng.standard_normal((T, S))
    region_c = {}
    for r in regions:
        eta = rng.standard_normal((T, S))
        R = math.sqrt(kappa) * world + math.sqrt(1 - kappa) * eta
        beta = float(params_by_region[r].get("climate_rain_beta", 0.0))
        h = histories.get(r)
        if beta > 0 and h is not None and len(h) >= 10:
            hz = np.asarray(h, dtype=float)
            hz = (hz - hz.mean()) / hz.std(ddof=1)
            bw = 0.9 * len(hz) ** (-0.2)
            B = (hz[rng.integers(0, len(hz), (T, S))] + bw * rng.standard_normal((T, S))) / math.sqrt(1 + bw * bw)
            beta = min(beta, 0.99)
            R = beta * B + math.sqrt(1 - beta * beta) * R
        region_c[r] = R
    innov = rng.standard_normal((T, S))
    z_p = np.empty((T, S))
    z_p[0] = innov[0]
    for t in range(1, T):
        z_p[t] = rho_p * z_p[t - 1] + math.sqrt(1 - rho_p * rho_p) * innov[t]
    # Jumps use the "all" row's jump parameters: one global event series.
    jump = (rng.uniform(size=(T, S)) < p_all["price_jump_prob"]) * rng.normal(p_all["price_jump_mean"], p_all["price_jump_sd"], (T, S))
    return {"world": world, "region": region_c, "z_p": z_p, "jump": jump, "rng": rng}


def run_portfolio(spec, scenario, n_paths, seed, histories):
    regions = sorted({c["Region"] for c in spec})
    pbr = {r: P.region_params(r) for r in regions}
    p_all = P.region_params(regions[0])          # shared rows are the same in every region
    T = max(1, int(p_all.get("horizon_seasons", 1)))
    lam = float(p_all.get("collective_climate_idio_share", 0.0))
    F = shared_factors(regions, pbr, n_paths, T, seed, histories, p_all)
    losses, pools, per_c = [], [], []
    for c in spec:
        p = dict(pbr[c["Region"]])
        p["n_members"] = max(5, int(round(p["n_members"] * float(c["Member_Scale"]))))
        eps = F["rng"].standard_normal((T, n_paths))
        z_c = math.sqrt(1 - lam) * F["region"][c["Region"]] + math.sqrt(lam) * eps
        r = M.simulate(p, n_paths, int(c["Seed"]), scenario, return_paths=True,
                       factors={"z_c": z_c, "z_p": F["z_p"], "jump": F["jump"]})
        losses.append(r["paths"]["facility_loss"]); pools.append(r["pool_notional_usd"])
        per_c.append((c, r))
    L = np.vstack(losses)                 # (collectives, paths)
    pool = float(sum(pools))
    port = L.sum(axis=0)
    lf = port / pool
    # Independent benchmark: permute each collective's paths separately.
    prng = np.random.default_rng(seed + 77)
    indep = np.zeros_like(port)
    for i in range(L.shape[0]):
        indep += L[i][prng.permutation(L.shape[1])]
    sum_standalone_ul99 = float(sum(np.percentile(l, 99) for l in losses)) / pool
    sum_standalone_ul95 = float(sum(np.percentile(l, 95) for l in losses)) / pool
    out = {
        "pool": pool, "n_collectives": len(spec), "T": T,
        "summary": M.summarise(port, L.sum(axis=0), pool, p_all),
        "indep_ul99": float(np.percentile(indep, 99)) / pool,
        "indep_ul95": float(np.percentile(indep, 95)) / pool,
        "es99": es99(port) / pool, "indep_es99": es99(indep) / pool,
        "sum_standalone_es99": float(sum(es99(l) for l in losses)) / pool,
        "sum_standalone_ul99": sum_standalone_ul99, "sum_standalone_ul95": sum_standalone_ul95,
        "regions": {}, "collectives": [], "histogram": M.histogram(lf),
    }
    for r in regions:
        idx = [i for i, c in enumerate(spec) if c["Region"] == r]
        sub = L[idx].sum(axis=0); sp = float(sum(pools[i] for i in idx))
        out["regions"][r] = {"pool": sp, "n": len(idx), "summary": M.summarise(sub, sub, sp, p_all), "es99": es99(sub) / sp,
                             "share_of_portfolio_el": float(sub.mean() / port.mean()) if port.mean() > 0 else 0.0,
                             "sum_standalone_ul99": float(sum(np.percentile(L[i], 99) for i in idx)) / sp}
    for (c, r), l, pl in zip(per_c, losses, pools):
        out["collectives"].append({"id": c["Collective_ID"], "region": c["Region"], "label": c["Label"], "pool": pl,
                                   "n_members": r["n_members"], "el_pct": r["el_pct"], "ul99_pct": r["ul99_pct"], "es99": es99(l) / pl,
                                   "share_of_portfolio_el": float(l.mean() / port.mean()) if port.mean() > 0 else 0.0})
    return out


def row(level, name, region, scen, o, s, pool, n, extra):
    t = s["tranches"]; att = s["attachment_for_senior_target"]
    d = {"Scenario_ID": scen["id"], "Scenario": scen["name"], "Level": level, "Name": name, "Region": region,
         "Pool_USD": "%.0f" % pool, "N_Collectives": str(n), "Horizon_Seasons": str(o["T"]),
         "EL_Pct": pct(s["el_pct"]), "UL95_Pct": pct(s["ul95_pct"]), "UL99_Pct": pct(s["ul99_pct"]),
         "ES99_Pct": "", "Sum_Standalone_UL99_Pct": "", "Independent_UL99_Pct": "", "Sum_Standalone_ES99_Pct": "", "Independent_ES99_Pct": "",
         "Share_Of_Portfolio_EL_Pct": "",
         "Equity_EL_Pct": pct(t["equity"]["el_pct"], 2), "Mezz_EL_Pct": pct(t["mezz"]["el_pct"], 2),
         "Senior_EL_Pct": pct(t["senior"]["el_pct"], 3), "Attachment_For_Senior_Target_Pct": "" if att >= 1 else pct(att, 1)}
    d.update(extra)
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paths", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    problems = P.validate()
    if problems:
        for pr in problems:
            print("  !", pr, file=sys.stderr)
        return 1
    spec = load_spec()
    histories = P.load_climate_history()
    scenarios = P.load_scenarios()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows, hrows = [], []
    for scen in scenarios:
        o = run_portfolio(spec, scen, args.paths, args.seed, histories)
        s = o["summary"]
        rows.append(row("portfolio", "Portfolio of %d collectives" % o["n_collectives"], "all", scen, o, s, o["pool"], o["n_collectives"],
                        {"ES99_Pct": pct(o["es99"]), "Sum_Standalone_UL99_Pct": pct(o["sum_standalone_ul99"]), "Independent_UL99_Pct": pct(o["indep_ul99"]),
                         "Sum_Standalone_ES99_Pct": pct(o["sum_standalone_es99"]), "Independent_ES99_Pct": pct(o["indep_es99"]),
                         "Share_Of_Portfolio_EL_Pct": "100.0"}))
        for r, d in o["regions"].items():
            rows.append(row("region", r, r, scen, o, d["summary"], d["pool"], d["n"],
                            {"ES99_Pct": pct(d["es99"]), "Sum_Standalone_UL99_Pct": pct(d["sum_standalone_ul99"]), "Share_Of_Portfolio_EL_Pct": pct(d["share_of_portfolio_el"], 1)}))
        for c in o["collectives"]:
            rows.append(row("collective", c["id"] + " " + c["label"], c["region"], scen, o,
                            {"el_pct": c["el_pct"], "ul95_pct": float("nan"), "ul99_pct": c["ul99_pct"],
                             "tranches": {"equity": {"el_pct": float("nan")}, "mezz": {"el_pct": float("nan")}, "senior": {"el_pct": float("nan")}},
                             "attachment_for_senior_target": 1.0},
                            c["pool"], 1, {"Share_Of_Portfolio_EL_Pct": pct(c["share_of_portfolio_el"], 1), "UL95_Pct": "", "ES99_Pct": pct(c["es99"]),
                                           "Equity_EL_Pct": "", "Mezz_EL_Pct": "", "Senior_EL_Pct": ""}))
        h = o["histogram"]
        for i, cnt in enumerate(h["counts"]):
            hrows.append({"Scenario_ID": scen["id"], "Bin_Low_Pct": pct(h["edges"][i], 2), "Bin_High_Pct": pct(h["edges"][i + 1], 2),
                          "Share_Of_Paths_Pct": pct(cnt / h["n"], 3)})
        print("   %-6s %-28s EL %6s%%  UL99 %6s%%  ES99 %6s%% (standalone sum %6s%%, independent %6s%%)" % (
            scen["id"], scen["name"], pct(s["el_pct"], 2), pct(s["ul99_pct"], 1), pct(o["es99"], 1), pct(o["sum_standalone_es99"], 1), pct(o["indep_es99"], 1)))
    for r in rows:
        r.update({"N_Paths": str(args.paths), "Seed": str(args.seed), "Model_Version": M.MODEL_VERSION, "Computed_At": stamp, "Basis": BASIS})
    for path, rs in ((RESULTS_CSV, rows), (HIST_CSV, hrows)):
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rs[0].keys()), quoting=csv.QUOTE_ALL, lineterminator="\n")
            w.writeheader(); w.writerows(rs)
        print("wrote %s (%d rows)" % (os.path.relpath(path, ROOT), len(rs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
