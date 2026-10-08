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

    print("\n%d passed, %d failed, %d skipped" % (len(PASS), len(FAIL), len(SKIP)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
