#!/usr/bin/env python3
"""RT-7 checks. Runs in CI.

    python3 risk-tools/collective/test_rt7.py

Proportionate rather than exhaustive, in the same spirit as the toolchain
check: the properties that would silently corrupt every downstream number if
they broke.

  1. The parameter tracker is well-formed (vocabulary, numeric, every row
     says where its number should come from).
  2. The PD curve hits the base PD exactly at the anchor and is monotone.
  3. With no volatility and comfortable cover, losses equal PD x EAD x LGD
     (the golden case the whole chain reduces to).
  4. Losses respond in the right direction to the shocks that should move
     them: a poor season and a price crash never lower EL; residual
     correlation fattens the tail without moving the mean.
  5. Side-selling fires when spot runs far above forward, and never when the
     forward price is above spot.
  6. Tranche losses conserve: the three tranches add up to the pool loss on
     every path, and the attachment search delivers the target it claims.
  7. The facility never loses more than it lent, and the member set is
     reproducible from the seed.
  8. The JavaScript port agrees with this implementation: exactly on the
     deterministic pieces, within Monte Carlo error on the simulation. Skipped
     with a notice if node is not installed.
  9. v0.3 additions: a one-season horizon reproduces the committed v0.2 results
     exactly; a multi-season run is cumulative and never below the first
     season; the forward-shortfall share moves the facility's loss and the
     amount carried outside the facility in the right directions; the
     empirical climate factor keeps unit variance and reproduces the history's
     skew; the JS port agrees on a three-season run with shared members.

Dependencies: numpy; node optional for check 8.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rt7_model as M  # noqa: E402
import rt7_params as P  # noqa: E402

PASS, FAIL, SKIP = [], [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("  %s  %s%s" % ("PASS" if cond else "FAIL", name, ("  - " + detail) if detail else ""))


def skip(name, why):
    SKIP.append(name)
    print("  SKIP  %s  - %s" % (name, why))


def main():
    print("RT-7 collective facility model checks\n")

    # --- 1. tracker --------------------------------------------------------------
    probs = P.validate()
    check("parameter tracker is well-formed", not probs, "; ".join(probs[:3]))
    regions = [r["Region"] for r in P.load_regions()]
    check("every region in rt7-regions.csv has parameters",
          all(any(True for _ in [P.region_params(r)]) for r in regions), ", ".join(regions))
    scen = {s["id"]: s for s in P.load_scenarios()}
    check("scenario table has a base case RS-0 with no shift",
          "RS-0" in scen and scen["RS-0"]["climate_shift"] == 0 and scen["RS-0"]["price_shift"] == 0)

    p = P.region_params("colombia")

    # --- 2. PD curve ----------------------------------------------------------------
    at_anchor = float(M.pd_curve(p["pd_anchor_dscr"], 0.05, p))
    check("PD curve equals the base PD at the anchor DSCR", abs(at_anchor - 0.05) < 1e-9, "%.6f" % at_anchor)
    grid = np.linspace(-2, 10, 200)
    pds = M.pd_curve(grid, 0.05, p)
    check("PD curve is monotone decreasing in DSCR", bool(np.all(np.diff(pds) <= 1e-12)))
    check("PD curve stays inside [floor, pd_max]",
          bool(pds.min() >= p["pd_floor_share"] * 0.05 - 1e-12 and pds.max() <= p["pd_max"] + 1e-12))

    # --- 3. golden case ---------------------------------------------------------------
    q = dict(p, yield_vol=0.0, member_yield_idio_vol=0.0, price_vol=0.0, price_jump_prob=0.0,
             residual_correlation=0.0, collective_fixed_cost_usd=0.0, reserve_share_of_margin=0.0,
             household_floor_usd=0.0, production_cost_per_ha=0.0, pd_dscr_sensitivity=0.0)
    # With sensitivity 0 the PD is the base PD for every borrower regardless of
    # DSCR, so the expected loss is exactly sum(pd_i x EAD_i x LGD_i).
    m = M.generate_members(q, 7)
    r = M.simulate(q, 40000, 7, scen["RS-0"], members=m)
    expected = float(np.sum(m["base_pd"] * m["ead"] * m["lgd"]))
    se = float(np.sqrt(np.sum(m["base_pd"] * (1 - m["base_pd"]) * (m["ead"] * m["lgd"]) ** 2) / 40000))
    check("golden case: EL equals sum(PD x EAD x LGD) within 4 standard errors",
          abs(r["el_usd"] - expected) < 4 * se + 1e-6,
          "EL %.0f vs %.0f (se %.0f)" % (r["el_usd"], expected, se))

    # --- 4. direction of response -----------------------------------------------------------
    base = M.simulate(p, 6000, 42, scen["RS-0"])
    poor = M.simulate(p, 6000, 42, scen["RS-1"])
    crash = M.simulate(p, 6000, 42, scen["RS-3"])
    check("a poor season does not lower EL", poor["el_pct"] >= base["el_pct"] - 1e-9,
          "%.2f%% -> %.2f%%" % (100 * base["el_pct"], 100 * poor["el_pct"]))
    # A price crash raises MEMBER losses (less spot revenue, lower cover) but can
    # LOWER the facility's loss: it removes side-selling, and the forward book
    # protects the collective. So the property that holds by construction is on
    # member loss, not on EL. Observed at the 2026-10 calibration: Colombia EL
    # 0.42% -> 0.23% under RS-3 while member loss rose.
    check("a price crash does not lower expected member loss",
          crash["mean_member_loss_usd"] >= base["mean_member_loss_usd"] * (1 - 0.02),
          "member loss %.0f -> %.0f; facility EL %.2f%% -> %.2f%%" % (
              base["mean_member_loss_usd"], crash["mean_member_loss_usd"], 100 * base["el_pct"], 100 * crash["el_pct"]))
    lo = M.simulate(dict(p, residual_correlation=0.0), 20000, 42, scen["RS-0"])
    hi = M.simulate(dict(p, residual_correlation=0.5), 20000, 42, scen["RS-0"])
    check("residual correlation fattens the tail (UL99 up)", hi["ul99_pct"] > lo["ul99_pct"],
          "UL99 %.1f%% -> %.1f%%" % (100 * lo["ul99_pct"], 100 * hi["ul99_pct"]))
    # Per-path conditional defaults are Bernoulli(pd) either way, so the mean member loss is the same in expectation.
    se_m = max(lo["mean_member_loss_usd"], 1.0) * 0.08
    check("residual correlation leaves expected member loss roughly unchanged",
          abs(hi["mean_member_loss_usd"] - lo["mean_member_loss_usd"]) < se_m,
          "%.0f vs %.0f" % (lo["mean_member_loss_usd"], hi["mean_member_loss_usd"]))

    # --- 5. side-selling ----------------------------------------------------------------------
    # At +90% the premium over forward is about 80%, so roughly 70% of committed
    # crop diverts and deliveries fall below a forward book sized at half of
    # expected deliveries on every path.
    spike = M.simulate(dict(p, price_vol=0.0, price_jump_prob=0.0), 500, 42, {"climate_shift": 0.0, "price_shift": 0.90})
    check("side-selling fires and the forward book is short when spot runs 90% above forward",
          spike["p_side_selling"] > 0.99 and spike["p_shortfall"] > 0.99 and spike["mean_diverted_share"] > 0.5,
          "P(side-sell) %.0f%%, P(shortfall) %.0f%%, diverted %.0f%%" % (
              100 * spike["p_side_selling"], 100 * spike["p_shortfall"], 100 * spike["mean_diverted_share"]))
    below = M.simulate(dict(p, price_vol=0.0, price_jump_prob=0.0, fwd_price_usd_per_t=p["price_base_usd_per_t"] * 1.5),
                       500, 42, scen["RS-0"])
    check("no side-selling when the forward price is above spot", below["p_side_selling"] == 0.0)

    # --- 6. tranches conserve -----------------------------------------------------------------------
    rp = M.simulate(p, 3000, 42, scen["RS-0"], return_paths=True)
    lf = rp["paths"]["facility_loss"] / rp["pool_notional_usd"]
    eq, mz = p["tranche_equity_detach"], p["tranche_mezz_detach"]
    parts = (np.clip(lf, 0, eq) + np.clip(lf - eq, 0, mz - eq) + np.clip(lf - mz, 0, 1 - mz))
    check("tranche losses add up to the pool loss on every path", bool(np.allclose(parts, np.minimum(lf, 1.0), atol=1e-12)))
    att = rp["attachment_for_senior_target"]
    target = p["senior_el_target_bp"] / 10000.0
    if att < 1.0:
        sen = float(np.mean(np.clip(lf - att, 0, 1 - att)) / (1 - att))
        check("attachment search delivers the senior EL target", sen <= target + 1e-9,
              "attach %.1f%% gives senior EL %.1f bp vs target %d bp" % (100 * att, 10000 * sen, p["senior_el_target_bp"]))
    else:
        sen0 = float(np.mean(np.clip(lf - 0.999, 0, 0.001)) / 0.001)
        check("attachment search reports unattainable only when the tail reaches the pool", sen0 > target,
              "senior EL at 99.9%% attachment is %.1f bp" % (10000 * sen0))

    # --- 7. bounds and reproducibility ---------------------------------------------------------------
    check("facility loss never exceeds the pool", bool(np.all(rp["paths"]["facility_loss"] <= rp["pool_notional_usd"] + 1e-6)))
    check("facility loss is never negative", bool(np.all(rp["paths"]["facility_loss"] >= 0)))
    m1, m2 = M.generate_members(p, 42), M.generate_members(p, 42)
    check("member set is reproducible from the seed", bool(np.array_equal(m1["ead"], m2["ead"])))
    r1, r2 = M.simulate(p, 500, 42), M.simulate(p, 500, 42)
    check("simulation is reproducible from the seed", r1["el_pct"] == r2["el_pct"])

    # --- 8. JS parity ---------------------------------------------------------------------------------
    node = shutil.which("node")
    if not node:
        skip("JS port agrees with the Python reference", "node not installed")
    else:
        probes_d = [-1.0, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0, 50.0]
        probes_p = [1e-6, 0.001, 0.02, 0.1, 0.5, 0.9, 0.99, 0.999999]
        probes_a = [[2500, 0.12, 5], [1500, 0.14, 4], [1000, 0.0, 3]]
        n_par = 20000
        # Hand the JS the SAME member set, so everything deterministic in the
        # members (pool, forward book, normal-year PD) must match exactly and
        # only the Monte Carlo paths differ.
        mem = M.generate_members(p, 42)
        mem_json = {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in mem.items()}
        payload = {"params": p, "nPaths": n_par, "seed": 42, "scenario": scen["RS-0"], "members": mem_json,
                   "pd_probe": probes_d, "pd_probe_base": 0.04, "ppf_probe": probes_p, "annuity_probe": probes_a}
        proc = subprocess.run([node, os.path.join(HERE, "parity_runner.js")], input=json.dumps(payload),
                              capture_output=True, text=True)
        if proc.returncode != 0:
            check("JS parity runner executes", False, proc.stderr.strip()[-200:])
        else:
            out = json.loads(proc.stdout)
            check("JS parity runner executes", True, "node " + subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip())
            py_pd = [float(x) for x in M.pd_curve(np.array(probes_d), 0.04, p)]
            check("PD curve identical in JS and Python", all(abs(a - b) < 1e-9 for a, b in zip(py_pd, out["pd_probe"])))
            py_ppf = [float(x) for x in M.norm_ppf(np.array(probes_p))]
            check("inverse normal identical in JS and Python", all(abs(a - b) < 1e-9 for a, b in zip(py_ppf, out["ppf_probe"])))
            py_ann = [M.annuity_payment(*a) for a in probes_a]
            check("annuity payment identical in JS and Python", all(abs(a - b) < 1e-9 for a, b in zip(py_ann, out["annuity_probe"])))
            check("JS and Python report the same model version", out["version"] == M.MODEL_VERSION)

            py = M.simulate(p, n_par, 42, scen["RS-0"], members=mem)
            js = out["result"]
            check("pool notional identical on the shared member set",
                  abs(py["pool_notional_usd"] - js["pool_notional_usd"]) < 1e-6,
                  "py %.2f vs js %.2f" % (py["pool_notional_usd"], js["pool_notional_usd"]))
            check("forward book identical on the shared member set",
                  abs(py["fwd_book_t"] - js["fwd_book_t"]) < 1e-9)
            check("normal-year PD and median DSCR identical on the shared member set",
                  abs(py["normal_year_pd"] - js["normal_year_pd"]) < 1e-9
                  and abs(py["normal_year_median_dscr"] - js["normal_year_median_dscr"]) < 1e-9,
                  "PD %.4f%% vs %.4f%%" % (100 * py["normal_year_pd"], 100 * js["normal_year_pd"]))
            # Mean loss rate: the two sides use different random streams, so the
            # tolerance is a multiple of the combined Monte Carlo standard error.
            se_el = math.sqrt(2) * py["sd_pct"] / math.sqrt(n_par)
            tol_el = 5 * se_el + 0.002
            check("EL agrees within Monte Carlo error",
                  abs(py["el_pct"] - js["el_pct"]) < tol_el,
                  "py %.2f%% vs js %.2f%% (tol %.2f pp)" % (100 * py["el_pct"], 100 * js["el_pct"], 100 * tol_el))
            check("UL95 agrees within 2 percentage points",
                  abs(py["ul95_pct"] - js["ul95_pct"]) < 0.02,
                  "py %.1f%% vs js %.1f%%" % (100 * py["ul95_pct"], 100 * js["ul95_pct"]))
            check("mean PD agrees within half a percentage point",
                  abs(py["mean_pd"] - js["mean_pd"]) < 0.005,
                  "py %.2f%% vs js %.2f%%" % (100 * py["mean_pd"], 100 * js["mean_pd"]))
            check("side-selling and shortfall frequencies agree within 2 points",
                  abs(py["p_side_selling"] - js["p_side_selling"]) < 0.02 and abs(py["p_shortfall"] - js["p_shortfall"]) < 0.02,
                  "side-sell py %.1f%% js %.1f%%; shortfall py %.1f%% js %.1f%%" % (
                      100 * py["p_side_selling"], 100 * js["p_side_selling"], 100 * py["p_shortfall"], 100 * js["p_shortfall"]))

    # --- 9. v0.3: horizon, shortfall share, empirical climate --------------------------------------
    import csv as _csv
    committed = {(r["Region"], r["Scenario_ID"]): r for r in _csv.DictReader(
        open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "data", "rt7-region-results.csv"), newline="", encoding="utf-8"))}
    one = dict(p, horizon_seasons=1)
    r1 = M.simulate(one, 5000, 42, scen["RS-0"])
    cm = committed.get(("colombia", "RS-0"))
    if cm and cm["N_Paths"] == "5000" and cm["Seed"] == "42":
        check("one-season horizon reproduces the committed Colombia base case to 3 decimals",
              abs(100 * r1["el_pct"] - float(cm["EL_Pct"])) < 0.0015 and abs(100 * r1["ul99_pct"] - float(cm["UL99_Pct"])) < 0.0015,
              "EL %.3f vs %s, UL99 %.3f vs %s" % (100 * r1["el_pct"], cm["EL_Pct"], 100 * r1["ul99_pct"], cm["UL99_Pct"]))
    else:
        skip("one-season horizon reproduces the committed base case", "committed row not at 5000 paths / seed 42")
    r3 = M.simulate(dict(p, horizon_seasons=3, price_persistence=0.5), 3000, 42, scen["RS-0"])
    check("three-season loss is cumulative: not below season one, and the seasons add up",
          r3["el_pct"] >= r3["el_per_season_pct"][0] - 1e-12 and abs(sum(r3["el_per_season_pct"]) - r3["el_pct"]) < 1e-9
          and len(r3["el_per_season_pct"]) == 3,
          "cumulative %.2f%%, seasons %s" % (100 * r3["el_pct"], ["%.2f" % (100 * x) for x in r3["el_per_season_pct"]]))
    check("members who default leave: cumulative member loss is below three times a single season",
          r3["member_el_pct"] < 3 * r1["member_el_pct"],
          "%.2f%% vs 3 x %.2f%%" % (100 * r3["member_el_pct"], 100 * r1["member_el_pct"]))
    sp_all = M.simulate(dict(p, fwd_shortfall_facility_share=1.0), 4000, 42, scen["RS-4"])
    sp_none = M.simulate(dict(p, fwd_shortfall_facility_share=0.0), 4000, 42, scen["RS-4"])
    check("moving the forward shortfall off the facility lowers its loss in a price spike",
          sp_none["el_pct"] < sp_all["el_pct"] and sp_all["mean_shortfall_outside_facility_usd"] == 0.0
          and abs(sp_none["mean_shortfall_outside_facility_usd"] - sp_none["mean_shortfall_cost_usd"]) < 1e-6,
          "EL %.2f%% -> %.2f%%; outside %.0f" % (100 * sp_all["el_pct"], 100 * sp_none["el_pct"], sp_none["mean_shortfall_outside_facility_usd"]))
    rng = np.random.default_rng(3)
    hist = np.concatenate([rng.normal(0.3, 0.6, 40), [-2.5, -2.2, -1.9, -2.8, -2.1]])   # skewed: a few deep deficits
    draws = M.climate_factor(np.random.default_rng(5), 200000, dict(p, climate_rain_beta=0.9), hist)
    hz = (hist - hist.mean()) / hist.std(ddof=1)
    skew_h = float(np.mean(hz ** 3)); skew_d = float(np.mean(((draws - draws.mean()) / draws.std()) ** 3))
    check("empirical climate factor keeps unit variance and the history's skew",
          abs(draws.std() - 1.0) < 0.02 and abs(draws.mean()) < 0.02 and skew_d < -0.3 and abs(skew_d - 0.9 ** 3 * skew_h) < 0.25,
          "sd %.3f, mean %.3f, skew %.2f (history %.2f)" % (draws.std(), draws.mean(), skew_d, skew_h))
    check("with beta 0 the climate factor is the plain normal draw",
          bool(np.array_equal(M.climate_factor(np.random.default_rng(9), 100, p, hist),
                              np.random.default_rng(9).standard_normal(100))))
    if node:
        p3 = dict(p, horizon_seasons=3, price_persistence=0.5, fwd_shortfall_facility_share=0.5, climate_rain_beta=0.4)
        mem3 = M.generate_members(p3, 42)
        payload = {"params": p3, "nPaths": 20000, "seed": 42, "scenario": scen["RS-0"],
                   "members": {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in mem3.items()},
                   "climate_history": hist.tolist()}
        proc = subprocess.run([node, os.path.join(HERE, "parity_runner.js")], input=json.dumps(payload),
                              capture_output=True, text=True)
        if proc.returncode != 0:
            check("JS parity on a three-season run executes", False, proc.stderr.strip()[-200:])
        else:
            js3 = json.loads(proc.stdout)["result"]
            py3 = M.simulate(p3, 20000, 42, scen["RS-0"], members=mem3, climate_history=hist)
            se3 = math.sqrt(2) * py3["sd_pct"] / math.sqrt(20000)
            check("JS agrees on a three-season run with shortfall share and empirical climate (EL within MC error)",
                  abs(py3["el_pct"] - js3["el_pct"]) < 5 * se3 + 0.002 and js3["horizon_seasons"] == 3,
                  "py %.2f%% vs js %.2f%% (tol %.2f pp); seasons py %s js %s" % (
                      100 * py3["el_pct"], 100 * js3["el_pct"], 100 * (5 * se3 + 0.002),
                      ["%.2f" % (100 * x) for x in py3["el_per_season_pct"]], ["%.2f" % (100 * x) for x in js3["el_per_season_pct"]]))
            # The reserve is a mean over every path (tight); the shortfall carried
            # outside is driven by the few spike paths, so its tolerance is wider.
            check("JS agrees on the carried reserve (10 percent) and the shortfall carried outside the facility (30 percent)",
                  abs(py3["mean_reserve_end_usd"] - js3["mean_reserve_end_usd"]) < 0.1 * max(py3["mean_reserve_end_usd"], 1)
                  and abs(py3["mean_shortfall_outside_facility_usd"] - js3["mean_shortfall_outside_facility_usd"]) < 0.3 * max(py3["mean_shortfall_outside_facility_usd"], 1) + 20,
                  "reserve py %.0f js %.0f; outside py %.0f js %.0f" % (
                      py3["mean_reserve_end_usd"], js3["mean_reserve_end_usd"],
                      py3["mean_shortfall_outside_facility_usd"], js3["mean_shortfall_outside_facility_usd"]))

    print("\n%d passed, %d failed, %d skipped" % (len(PASS), len(FAIL), len(SKIP)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
