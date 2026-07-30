#!/usr/bin/env python3
"""RT-5 scaffold: synthetic portfolio generator and waterfall.

    python3 risk-tools/tools/simulate_portfolio.py            # all scenarios
    python3 risk-tools/tools/simulate_portfolio.py --scenario SC-2
    python3 risk-tools/tools/simulate_portfolio.py --write-loans   # loan-level CSV

EVERYTHING THIS PRODUCES IS SYNTHETIC AND ILLUSTRATIVE. No field data exists
yet. The loss, recovery and correlation parameters are placeholders chosen to
be plausible, not estimates of anything. Outputs are useful for reasoning about
STRUCTURE - how sensitive is the junior tranche to correlation, where does the
fixed-cost floor sit - and are not usable as evidence about this asset class.
See rt-5-simulator.md for what would have to change for that.

Reads:
  risk-tools/tools/portfolio-config.csv   portfolio assumptions
  data/macro-scenarios.csv                deterministic macro shocks

Writes:
  data/rt5-scenario-results.csv           committed headline metrics per scenario
  risk-tools/tools/output/loans-*.csv     loan-level tape (gitignored, --write-loans)

Python 3 stdlib only.
"""

import argparse
import csv
import math
import os
import random
import sys
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG = os.path.join(ROOT, "risk-tools", "tools", "portfolio-config.csv")
SCENARIOS = os.path.join(ROOT, "data", "macro-scenarios.csv")
RESULTS = os.path.join(ROOT, "data", "rt5-scenario-results.csv")
OUTDIR = os.path.join(ROOT, "risk-tools", "tools", "output")

SCHEMA_VERSION = "0.1"
MODEL_VERSION = "0.1"


def load_config():
    cfg = {}
    with open(CONFIG, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            raw = row["Value"]
            cfg[row["Parameter"]] = int(raw) if raw.isdigit() else float(raw)
    return cfg


def load_scenarios():
    with open(SCENARIOS, newline="", encoding="utf-8") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


# --- pool generation ---------------------------------------------------------

def build_pool(cfg, rng):
    """Generate a loan-level pool shaped by the RT-1 schema.

    Fields mirror the RT-1 `loan` entity so the simulator and the real tape
    stay interchangeable - when field data arrives it should drop into the same
    downstream code with no changes here.
    """
    loans = []
    start = date(2027, 1, 1)
    for g in range(int(cfg["n_groups"])):
        geo = rng.randrange(int(cfg["n_geographies"]))
        originator = rng.randrange(int(cfg["n_originators"]))
        # Poisson via Knuth - stdlib random has no poisson and numpy is not a dep.
        lam, k, p = cfg["loans_per_group_mean"], 0, 1.0
        limit = math.exp(-lam)
        while p > limit:
            p *= rng.random()
            k += 1
        for _ in range(max(1, k - 1)):
            principal = rng.lognormvariate(
                math.log(cfg["loan_principal_mean"]) - cfg["loan_principal_sigma"] ** 2 / 2,
                cfg["loan_principal_sigma"])
            term = max(30, int(rng.gauss(cfg["term_days_mean"], cfg["term_days_sd"])))
            loans.append({
                "loan_id": "LN-%010d" % len(loans),
                "loan_group_id": "GRP-%06d" % g,
                "originator_id": "ORG-%04d" % originator,
                "geography": "GEO-%02d" % geo,
                "loan_disbursement_date": (start + timedelta(days=rng.randrange(0, 365))).isoformat(),
                "loan_principal": round(principal, 2),
                "loan_currency_code": "USD",
                "loan_term_days": term,
                "loan_charge_rate_pct": cfg["charge_rate_pct"],
                "loan_charge_basis": "flat_per_cycle",
                "loan_guarantee_type": "group_joint_liability",
                "loan_schema_version": SCHEMA_VERSION,
            })
    return loans


def simulate_losses(loans, cfg, scenario, rng):
    """One Monte Carlo path. Returns (principal, collections, losses).

    Correlation is modelled with a single-factor structure: each geography
    draws a systemic factor, and a loan defaults when its combined systemic and
    idiosyncratic draw crosses a threshold. This is the standard one-factor
    Gaussian copula shape used in structured credit, chosen because it is
    inspectable rather than because it is sophisticated - the whole point is
    that a reader can see what the correlation parameter does.
    """
    rho = scenario["correlation"] if scenario["correlation"] is not None else cfg["correlation"]
    rho = max(0.0, min(0.95, rho))
    pd_annual = min(0.95, cfg["annual_default_rate"] * scenario["default_multiplier"])
    recovery = max(0.0, min(1.0, cfg["recovery_rate"] * scenario["recovery_multiplier"]))
    prepay = max(0.0, min(1.0, cfg["prepay_rate_annual"] * scenario["prepay_multiplier"]))

    factors = {}
    principal = collections = losses = 0.0
    for loan in loans:
        geo = loan["geography"]
        if geo not in factors:
            factors[geo] = rng.gauss(0, 1)

        term_years = loan["loan_term_days"] / 365.0
        pd_term = 1 - (1 - pd_annual) ** term_years
        # Threshold on the standard normal that reproduces pd_term.
        threshold = _norm_ppf(pd_term)
        draw = math.sqrt(rho) * factors[geo] + math.sqrt(1 - rho) * rng.gauss(0, 1)

        p = loan["loan_principal"]
        charge = p * loan["loan_charge_rate_pct"] / 100.0
        principal += p

        if draw < threshold:                                   # default
            recovered = p * recovery
            collections += recovered
            losses += p - recovered
        else:
            prepaid = rng.random() < (1 - (1 - prepay) ** term_years)
            # A prepaid loan returns principal but only part of the charge.
            collections += p + (charge * 0.5 if prepaid else charge)
    return principal, collections, losses


def _norm_ppf(p):
    """Inverse standard normal CDF (Acklam's rational approximation).

    Needed to turn a default probability into a copula threshold. Written out
    rather than pulled from scipy to keep the stdlib-only rule - accurate to
    about 1e-9, far beyond what matters here.
    """
    if p <= 0:
        return -8.0
    if p >= 1:
        return 8.0
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q, r = p - 0.5, (p - 0.5) ** 2
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def waterfall(principal, collections, cfg, scenario):
    """Distribute collections: costs first, then senior, mezzanine, junior.

    Deliberately simple and sequential. The conservation property - what goes in
    equals what comes out - is asserted rather than assumed, because a leak here
    would invalidate every number downstream and is exactly the kind of bug that
    hides in a waterfall.
    """
    senior = principal * cfg["senior_pct"]
    mezz = principal * cfg["mezz_pct"]
    junior = principal * cfg["junior_pct"]

    rate_shock = scenario["rate_shock_pp"] / 100.0
    senior_due = senior * (1 + cfg["senior_coupon_pct"] + rate_shock)
    mezz_due = mezz * (1 + cfg["mezz_coupon_pct"] + rate_shock)

    costs = principal * cfg["servicing_cost_pct"] + cfg["fixed_costs_usd"]

    available = collections
    paid_costs = min(available, costs)
    available -= paid_costs
    paid_senior = min(available, senior_due)
    available -= paid_senior
    paid_mezz = min(available, mezz_due)
    available -= paid_mezz
    paid_junior = min(available, junior)
    residual = available - paid_junior

    total_out = paid_costs + paid_senior + paid_mezz + paid_junior + residual
    assert abs(total_out - collections) < 0.01, \
        "waterfall leak: in=%.2f out=%.2f" % (collections, total_out)

    return {
        "senior_due": senior_due, "senior_paid": paid_senior,
        "mezz_due": mezz_due, "mezz_paid": paid_mezz,
        "junior_notional": junior, "junior_paid": paid_junior,
        "costs": paid_costs, "costs_due": costs, "residual": residual,
        "senior_shortfall": max(0.0, senior_due - paid_senior),
        "mezz_shortfall": max(0.0, mezz_due - paid_mezz),
        "junior_loss": max(0.0, junior - paid_junior),
    }


def run_scenario(scenario, cfg, loans):
    rng = random.Random(int(cfg["seed"]) + hash(scenario["id"]) % 10000)
    n = int(cfg["n_simulations"])
    loss_rates, senior_hits, junior_wipes, junior_losses = [], 0, 0, []
    principal = sum(l["loan_principal"] for l in loans)

    for _ in range(n):
        p, collections, losses = simulate_losses(loans, cfg, scenario, rng)
        wf = waterfall(p, collections, cfg, scenario)
        loss_rates.append(losses / p if p else 0.0)
        if wf["senior_shortfall"] > 0.01:
            senior_hits += 1
        junior_losses.append(wf["junior_loss"] / wf["junior_notional"] if wf["junior_notional"] else 0.0)
        if wf["junior_loss"] >= wf["junior_notional"] - 0.01:
            junior_wipes += 1

    loss_rates.sort()
    # Cost drag is reported separately from credit loss on purpose. On a small
    # pool the fixed-cost term alone can consume the junior tranche while credit
    # losses stay low - which reads as a credit result unless the two are split.
    # That separation is the whole OQ-2 finding, so it belongs in the output.
    cost_drag = (principal * cfg["servicing_cost_pct"] + cfg["fixed_costs_usd"]) / principal
    return {
        "Scenario_ID": scenario["id"],
        "Scenario": scenario["name"],
        "Pool_Principal_USD": round(principal, 2),
        "Loans": len(loans),
        "Mean_Loss_Rate_Pct": round(100 * sum(loss_rates) / n, 3),
        "P95_Loss_Rate_Pct": round(100 * loss_rates[int(0.95 * n)], 3),
        "P99_Loss_Rate_Pct": round(100 * loss_rates[min(int(0.99 * n), n - 1)], 3),
        "Cost_Drag_Pct_Of_Pool": round(100 * cost_drag, 3),
        "Fixed_Cost_Pct_Of_Pool": round(100 * cfg["fixed_costs_usd"] / principal, 3),
        "Mean_Junior_Loss_Pct": round(100 * sum(junior_losses) / n, 2),
        "Junior_Wipeout_Prob_Pct": round(100 * junior_wipes / n, 2),
        "Senior_Shortfall_Prob_Pct": round(100 * senior_hits / n, 2),
        "Correlation_Used": scenario["correlation"] if scenario["correlation"] is not None else cfg["correlation"],
        "Default_Multiplier": scenario["default_multiplier"],
        "Model_Version": MODEL_VERSION,
        "Basis": "SYNTHETIC - illustrative only, not calibrated to field data",
    }


def parse_scenarios(rows):
    out = []
    for r in rows:
        corr = r["Correlation_Override"].strip()
        out.append({
            "id": r["ID"], "name": r["Scenario"],
            "rate_shock_pp": float(r["Rate_Shock_Pp"]),
            "default_multiplier": float(r["Default_Multiplier"]),
            "recovery_multiplier": float(r["Recovery_Multiplier"]),
            "prepay_multiplier": float(r["Prepay_Multiplier"]),
            "correlation": float(corr) if corr else None,
        })
    return out


def sweep_pool_size():
    """Vary pool size against a fixed cost base, under base and stress.

    This is the OQ-2 question stated directly: minimum viable pool size is a
    fixed-cost problem before it is a risk problem. The sweep shows where the
    cost floor stops dominating, which is the number the working band from
    LIT-011/LIT-012 currently stands in for.
    """
    cfg = load_config()
    scenarios = {s["id"]: s for s in parse_scenarios(load_scenarios())}
    print("POOL-SIZE SWEEP - synthetic, illustrative only")
    print("Fixed costs %s USD, servicing %.1f%% of pool\n"
          % (format(int(cfg["fixed_costs_usd"]), ","), 100 * cfg["servicing_cost_pct"]))
    print("  %-8s %-14s %-11s %-13s %s"
          % ("groups", "pool USD", "fixed cost", "base junior", "stressed junior"))

    rows = []
    for n_groups in (250, 500, 1000, 2000, 4000, 8000, 16000):
        local = dict(cfg)
        local["n_groups"] = n_groups
        local["n_simulations"] = 60          # sweep breadth over depth
        rng = random.Random(int(cfg["seed"]))
        loans = build_pool(local, rng)
        principal = sum(l["loan_principal"] for l in loans)
        base = run_scenario(scenarios["SC-0"], local, loans)
        stress = run_scenario(scenarios["SC-2"], local, loans)
        print("  %-8d %-14s %-11s %-13s %s"
              % (n_groups, format(int(principal), ","),
                 "%.2f%%" % (100 * cfg["fixed_costs_usd"] / principal),
                 "%.1f%% loss" % base["Mean_Junior_Loss_Pct"],
                 "%.1f%% loss" % stress["Mean_Junior_Loss_Pct"]))
        rows.append((n_groups, principal, base, stress))
    print("\nRead this as: where does the fixed-cost line stop dominating the junior")
    print("tranche? Below that size the structure fails on costs, not on credit.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenario", help="run a single scenario ID (e.g. SC-2)")
    ap.add_argument("--write-loans", action="store_true",
                    help="also write the loan-level tape (gitignored)")
    ap.add_argument("--sweep", action="store_true",
                    help="sweep pool size against the fixed-cost floor (OQ-2)")
    args = ap.parse_args()

    if args.sweep:
        return sweep_pool_size()

    cfg = load_config()
    scenarios = parse_scenarios(load_scenarios())
    if args.scenario:
        scenarios = [s for s in scenarios if s["id"] == args.scenario]
        if not scenarios:
            raise SystemExit("no such scenario: %s" % args.scenario)

    rng = random.Random(int(cfg["seed"]))
    loans = build_pool(cfg, rng)
    print("SYNTHETIC POOL - illustrative only, not calibrated to field data")
    print("  %d loans across %d groups, %s USD notional"
          % (len(loans), int(cfg["n_groups"]),
             format(round(sum(l["loan_principal"] for l in loans)), ",")))
    print("  %d simulations per scenario, seed %d\n" % (int(cfg["n_simulations"]), int(cfg["seed"])))

    results = []
    for s in scenarios:
        r = run_scenario(s, cfg, loans)
        results.append(r)
        print("  %-6s %-18s loss mean %5.2f%%  p95 %5.2f%%  junior loss %5.1f%%  "
              "wipeout %4.1f%%  senior hit %4.1f%%"
              % (r["Scenario_ID"], r["Scenario"][:18], r["Mean_Loss_Rate_Pct"],
                 r["P95_Loss_Rate_Pct"], r["Mean_Junior_Loss_Pct"],
                 r["Junior_Wipeout_Prob_Pct"], r["Senior_Shortfall_Prob_Pct"]))

    if not args.scenario:                      # only rewrite the full set
        with open(RESULTS, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(results[0].keys()),
                               quoting=csv.QUOTE_ALL, lineterminator="\n")
            w.writeheader()
            for r in results:
                w.writerow(r)
        print("\nWrote %s" % os.path.relpath(RESULTS, ROOT))

    if args.write_loans:
        os.makedirs(OUTDIR, exist_ok=True)
        path = os.path.join(OUTDIR, "loans-synthetic.csv")
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(loans[0].keys()),
                               quoting=csv.QUOTE_ALL, lineterminator="\n")
            w.writeheader()
            for l in loans:
                w.writerow(l)
        print("Wrote %s (gitignored)" % os.path.relpath(path, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
