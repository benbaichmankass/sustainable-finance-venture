#!/usr/bin/env python3
"""RT-6 unit-economics model: does the structuring layer become a business?

    python3 risk-tools/tools/economics_model.py               # all scenarios, full report
    python3 risk-tools/tools/economics_model.py --scenario Likely
    python3 risk-tools/tools/economics_model.py --deal        # deal-level P&L
    python3 risk-tools/tools/economics_model.py --venture     # venture ramp to break-even
    python3 risk-tools/tools/economics_model.py --pilot       # flagship pilot-breakeven yardstick
    python3 risk-tools/tools/economics_model.py --sensitivity # loss x fee grid (Likely case)

WHAT THIS IS. A deterministic, closed-form economics model of the STRUCTURING
COMPANY - our own P&L - run across three scenarios (Worst / Likely / Best),
plus a check on whether the tranche stack clears the returns investors require.
It answers OQ-10.

THE OQ-10 THRESHOLD (set 2026-08-02, gate + KPIs decided by BB):

  - THE GATE (go/no-go) is a credible path to the structuring layer COVERING
    ITS OWN COSTS at a reachable scale, within gate_horizon_years. This is a
    venture-level break-even test - distinct from the pilot-breakeven companion
    yardstick, which asks the same of a single pilot pool and is expected to
    fail. The gate passes for a scenario if the venture turns cumulatively
    positive on or before the gate horizon.
  - THE KPIs we track (not the gate) are (1) steady-state operating margin and
    (2) return on capital-at-risk. Targets live in the config; the model reports
    each against its target per scenario.
  - THE BINDING CONSTRAINT is the investor stack. If the pool's spread cannot
    pay senior and mezzanine their coupons after expected loss and the
    originator's share, there is no deal to structure. Checked per scenario.

WHAT THIS IS NOT. It is not RT-5. RT-5 simulates the credit waterfall with a
correlated loss model and owns the loss distribution and the fixed-cost floor
(OQ-2). RT-6 takes a loss ASSUMPTION - a point estimate, sweepable, readable
off an RT-5 scenario - and asks the economics question on top of it. RT-5:
"does the structure survive". RT-6: "does the business pay".

CALIBRATION. economics-config.csv carries three value columns (Worst/Likely/
Best) and a Basis tag per driver. SOURCED drivers cite an open-access benchmark
and are held FIXED across scenarios; ASSUMED drivers are the judgment calls the
scenarios flex. The model prints the basis mix on every run. No output should
be shown to an investor as a result while ASSUMED rows carry the load. See
risk-tools/rt-6-economics-model.md.

Reads:
  risk-tools/tools/economics-config.csv    drivers x 3 scenarios, each tagged
  risk-tools/tools/economics-assets.csv    flagship pilot profiles (EXP-01/02/06)

Writes:
  data/rt6-economics-results.csv           committed headline metrics per scenario

Python 3 stdlib only.
"""

import argparse
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG = os.path.join(ROOT, "risk-tools", "tools", "economics-config.csv")
ASSETS = os.path.join(ROOT, "risk-tools", "tools", "economics-assets.csv")
RESULTS = os.path.join(ROOT, "data", "rt6-economics-results.csv")

MODEL_VERSION = "0.1"
SCENARIOS = ("Worst", "Likely", "Best")


# --- config ------------------------------------------------------------------

def load_config():
    """Return (scenarios, basis).

    scenarios maps 'Worst'/'Likely'/'Best' -> {parameter: float}.
    basis maps parameter -> 'SOURCED' or 'ASSUMED', taken from the Basis tag,
    so the model can report its own footing.
    """
    scenarios = {s: {} for s in SCENARIOS}
    basis = {}
    with open(CONFIG, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            p = row["Parameter"]
            for s in SCENARIOS:
                scenarios[s][p] = float(row[s])
            basis[p] = row["Basis"].split(" ")[0].upper()
    return scenarios, basis


def load_assets():
    if not os.path.exists(ASSETS):
        return []
    with open(ASSETS, newline="", encoding="utf-8") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def basis_mix(basis):
    sourced = sum(1 for v in basis.values() if v == "SOURCED")
    return sourced, len(basis)


# --- the two computations ----------------------------------------------------

def structure_clears(cfg, loss_pct=None):
    """BINDING CONSTRAINT: does the pool's spread pay senior + mezz their
    required coupons, after expected loss, the originator's share and our fees,
    and what is left for the junior/first-loss layer?

    Everything is annualised and expressed as a rate on notional so a reader can
    trace each term. Returns the residual return to the junior layer (a rate on
    the junior tranche) and the coverage checks.
    """
    el = cfg["expected_loss_pct"] if loss_pct is None else loss_pct

    gross = cfg["gross_yield_pct"]
    originator = gross * cfg["originator_share_pct"]        # a share of gross yield
    net_spread = gross - originator - el

    # Our fee load sits ahead of the capital stack (fees come first in the
    # waterfall). Servicing fee is annual; the upfront structuring fee is
    # amortised over the pool's life for this rate comparison.
    fee_load = cfg["servicing_fee_pct"] + cfg["structuring_fee_pct"] / cfg["weighted_life_years"]
    available_to_capital = net_spread - fee_load

    senior_cost = cfg["senior_pct"] * cfg["senior_coupon_pct"]
    mezz_cost = cfg["mezz_pct"] * cfg["mezz_coupon_pct"]

    residual = available_to_capital - senior_cost - mezz_cost   # rate on notional
    junior_notional_rate = cfg["junior_pct"]
    junior_return = residual / junior_notional_rate if junior_notional_rate else 0.0

    return {
        "gross_yield": gross,
        "originator_share": originator,
        "expected_loss": el,
        "net_spread": net_spread,
        "fee_load": fee_load,
        "available_to_capital": available_to_capital,
        "senior_cost": senior_cost,
        "mezz_cost": mezz_cost,
        "residual_on_notional": residual,
        "junior_return": junior_return,
        "senior_mezz_covered": available_to_capital >= senior_cost + mezz_cost,
        "junior_clears_hurdle": junior_return >= cfg["junior_hurdle_pct"],
    }


def deal_pnl(cfg, notional, loss_pct=None):
    """THE STRUCTURING COMPANY'S OWN P&L for one deal, over the pool's life.

    Revenue is ours to keep: the upfront structuring fee, the annual servicing
    fee over the pool's life, and the net return on the economic interest we are
    required to retain. Cost is ours to bear: the one-off fixed structuring cost
    and our own servicing/monitoring opex. The originator's economics and the
    investor coupons are NOT our cost - they live in structure_clears() as the
    constraint on the deal existing at all.
    """
    life = cfg["weighted_life_years"]

    rev_structuring = cfg["structuring_fee_pct"] * notional
    rev_servicing = cfg["servicing_fee_pct"] * notional * life

    # Return on the retained strip. We hold retained_interest_pct of notional;
    # its return is the junior residual (the strip is first-loss economic
    # interest), floored at zero - a wiped strip returns nothing, it does not
    # bill negatively here.
    sc = structure_clears(cfg, loss_pct)
    strip = cfg["retained_interest_pct"] * notional
    rev_retained = max(0.0, sc["junior_return"]) * strip * life

    cost_fixed = cfg["fixed_structuring_cost_usd"]
    cost_serving = cfg["cost_to_serve_pct"] * notional * life

    revenue = rev_structuring + rev_servicing + rev_retained
    cost = cost_fixed + cost_serving
    net = revenue - cost

    return {
        "notional": notional,
        "rev_structuring": rev_structuring,
        "rev_servicing": rev_servicing,
        "rev_retained": rev_retained,
        "revenue": revenue,
        "cost_fixed": cost_fixed,
        "cost_serving": cost_serving,
        "cost": cost,
        "net_margin_usd": net,
        "net_margin_pct": net / notional if notional else 0.0,
        "structure": sc,
    }


def break_even_pool(cfg, loss_pct=None):
    """Deal-level break-even: the notional at which our net margin per deal = 0.

    Net margin is linear in notional except for the fixed cost, so this solves
    in closed form. Above this size a deal covers its fixed structuring cost;
    below it, it does not - the same fixed-cost logic RT-5 finds for the junior
    tranche (OQ-2), here for our P&L.
    """
    life = cfg["weighted_life_years"]
    sc = structure_clears(cfg, loss_pct)
    per_dollar = (
        cfg["structuring_fee_pct"]
        + cfg["servicing_fee_pct"] * life
        + max(0.0, sc["junior_return"]) * cfg["retained_interest_pct"] * life
        - cfg["cost_to_serve_pct"] * life
    )
    if per_dollar <= 0:
        return None  # no pool size covers the fixed cost; the deal never pays
    return cfg["fixed_structuring_cost_usd"] / per_dollar


def venture_ramp(cfg, loss_pct=None):
    """Venture level: cumulative net margin from a realistic deal ramp against
    the structuring company's own annual overhead.

    Returns the year and deal count at which the venture turns cumulatively
    positive (the GATE test), the steady-state annual margin, the operating
    margin (KPI 1) and the return on capital-at-risk (KPI 2).
    """
    per_year = cfg["deals_per_year"]
    size = cfg["avg_deal_notional"]
    overhead = cfg["annual_overhead_usd"]
    horizon = int(cfg["ramp_horizon_years"])
    life = cfg["weighted_life_years"]

    # Per-deal upfront take is identical across deals of the same size: the
    # structuring fee plus one year's amortised slice of the strip's return.
    d1 = deal_pnl(cfg, size, loss_pct)
    upfront_per_deal = d1["rev_structuring"] + d1["rev_retained"] / life

    rows = []
    cumulative = 0.0
    be_year = be_deals = None
    total_deals = 0
    for year in range(1, horizon + 1):
        total_deals += per_year
        upfront = upfront_per_deal * per_year
        # Servicing fee accrues on the active book. Pools roll off after `life`
        # years; approximate the book as the last `life` cohorts.
        active_book = min(year, life) * per_year * size
        servicing = cfg["servicing_fee_pct"] * active_book
        our_serving_cost = cfg["cost_to_serve_pct"] * active_book
        revenue = upfront + servicing
        cost = our_serving_cost + overhead
        margin = revenue - cost
        cumulative += margin
        if be_year is None and cumulative >= 0:
            be_year, be_deals = year, total_deals
        rows.append({
            "year": year, "deals_cumulative": total_deals,
            "active_book_usd": active_book, "revenue_usd": revenue,
            "cost_usd": cost, "year_margin_usd": margin, "cumulative_usd": cumulative,
        })

    last = rows[-1]
    steady_revenue = last["revenue_usd"]
    steady_margin = last["year_margin_usd"]
    steady_book = last["active_book_usd"]
    # Capital-at-risk = the first-loss economic interest we hold across the book.
    capital_at_risk = cfg["retained_interest_pct"] * steady_book
    return {
        "rows": rows,
        "break_even_year": be_year,
        "break_even_deals": be_deals,
        "steady_state_margin_usd": steady_margin,
        "steady_state_revenue_usd": steady_revenue,
        "steady_state_book_usd": steady_book,
        "operating_margin_pct": steady_margin / steady_revenue if steady_revenue else 0.0,
        "capital_at_risk_usd": capital_at_risk,
        "rocar_pct": steady_margin / capital_at_risk if capital_at_risk else 0.0,
    }


def evaluate(cfg):
    """Roll up the gate and the two KPIs for one scenario."""
    v = venture_ramp(cfg)
    gate_horizon = cfg["gate_horizon_years"]
    gate_pass = v["break_even_year"] is not None and v["break_even_year"] <= gate_horizon
    return {
        "venture": v,
        "gate_pass": gate_pass,
        "gate_horizon": gate_horizon,
        "kpi1_op_margin": v["operating_margin_pct"],
        "kpi1_target": cfg["kpi_operating_margin_target"],
        "kpi1_met": v["operating_margin_pct"] >= cfg["kpi_operating_margin_target"],
        "kpi2_rocar": v["rocar_pct"],
        "kpi2_target": cfg["kpi_rocar_target"],
        "kpi2_met": v["rocar_pct"] >= cfg["kpi_rocar_target"],
    }


# --- reporting ---------------------------------------------------------------

def money(x):
    return "$%s" % format(int(round(x)), ",")


def pct(x):
    return "%.2f%%" % (100 * x)


def print_deal(name, cfg):
    n = cfg["avg_deal_notional"]
    d = deal_pnl(cfg, n)
    sc = d["structure"]
    be = break_even_pool(cfg)
    print("[%s] DEAL-LEVEL P&L  (pool %s, life %.1fy)" % (name, money(n), cfg["weighted_life_years"]))
    print("    revenue  struct %s + servicing %s + retained %s = %s"
          % (money(d["rev_structuring"]), money(d["rev_servicing"]),
             money(d["rev_retained"]), money(d["revenue"])))
    print("    cost     fixed %s + servicing opex %s = %s"
          % (money(d["cost_fixed"]), money(d["cost_serving"]), money(d["cost"])))
    print("    NET MARGIN %s  (%s of notional)   break-even pool %s"
          % (money(d["net_margin_usd"]), pct(d["net_margin_pct"]),
             money(be) if be else "never"))
    print("    constraint: senior+mezz %s | junior return %s vs %s hurdle -> %s"
          % ("covered" if sc["senior_mezz_covered"] else "NOT COVERED",
             pct(sc["junior_return"]), pct(cfg["junior_hurdle_pct"]),
             "clears" if sc["junior_clears_hurdle"] else "SHORT, needs concessional first-loss"))


def print_venture(name, cfg):
    e = evaluate(cfg)
    v = e["venture"]
    print("[%s] VENTURE RAMP  (%.0f deals/yr x %s, overhead %s/yr)"
          % (name, cfg["deals_per_year"], money(cfg["avg_deal_notional"]),
             money(cfg["annual_overhead_usd"])))
    for r in v["rows"]:
        print("    y%d  deals %-3d  book %-14s margin %-14s cum %s"
              % (r["year"], r["deals_cumulative"], money(r["active_book_usd"]),
                 money(r["year_margin_usd"]), money(r["cumulative_usd"])))
    be = ("year %d (%d deals)" % (v["break_even_year"], v["break_even_deals"])
          if v["break_even_year"] else "not within horizon")
    print("    GATE (cover costs within %.0fy): break-even %s -> %s"
          % (e["gate_horizon"], be, "PASS" if e["gate_pass"] else "FAIL"))
    print("    KPI1 operating margin %s (target %s) -> %s"
          % (pct(e["kpi1_op_margin"]), pct(e["kpi1_target"]),
             "met" if e["kpi1_met"] else "below"))
    print("    KPI2 return on capital-at-risk %s on %s strip (target %s) -> %s"
          % (pct(e["kpi2_rocar"]), money(v["capital_at_risk_usd"]), pct(e["kpi2_target"]),
             "met" if e["kpi2_met"] else "below"))


def print_pilot(scenarios):
    """Pilot yardstick under the Likely scenario - the companion to the gate."""
    assets = load_assets()
    if not assets:
        print("PILOT YARDSTICK: no economics-assets.csv found.")
        return
    cfg = scenarios["Likely"]
    print("PILOT-BREAKEVEN YARDSTICK (Likely assumptions) - companion, not the gate")
    print("  A pilot pool is expected to be below break-even. The question is how")
    print("  far, and what closes the gap - scale, fee, or grant subsidy.")
    print("  %-8s %-24s %-14s %-13s %s" % ("asset", "pilot pool", "net margin", "% notional", "x to break-even"))
    for a in assets:
        local = dict(cfg)
        for k in ("gross_yield_pct", "expected_loss_pct", "weighted_life_years"):
            if a.get(k):
                local[k] = float(a[k])
        n = float(a["pilot_notional_usd"])
        d = deal_pnl(local, n)
        be = break_even_pool(local)
        mult = ("%.0fx" % (be / n)) if be and n else "n/a"
        print("  %-8s %-24s %-14s %-13s %s"
              % (a["Asset_ID"], "%s (%s loans)" % (money(n), a.get("pilot_loans", "?")),
                 money(d["net_margin_usd"]), pct(d["net_margin_pct"]), mult))
    print("  Read: pilots sit tens of times below break-even. The warehousing")
    print("  bridge to scale is not an optimisation - it is the only path (OQ-2).")


def print_sensitivity(scenarios):
    """Loss x fee grid under the Likely scenario."""
    cfg = scenarios["Likely"]
    n = cfg["avg_deal_notional"]
    base_el = cfg["expected_loss_pct"]
    base_fee = cfg["structuring_fee_pct"]
    loss_grid = [base_el * m for m in (0.5, 1.0, 1.5, 2.0, 3.0)]
    fee_grid = [base_fee * m for m in (1.0, 0.75, 0.5, 0.25)]
    print("SENSITIVITY (Likely) - deal net margin on a %s pool" % money(n))
    print("  Our fees are senior to credit losses in the waterfall, so margin is")
    print("  flat as loss rises WHILE the deal clears - then the pool stops paying")
    print("  senior+mezz and there is no deal to earn on ('no deal' below).")
    print("  rows: expected loss   cols: structuring fee (base -> compressed)")
    print("  %-12s %s" % ("", "  ".join("%9s" % pct(f) for f in fee_grid)))
    for el in loss_grid:
        cells = []
        for f in fee_grid:
            local = dict(cfg)
            local["structuring_fee_pct"] = f
            d = deal_pnl(local, n, loss_pct=el)
            cell = money(d["net_margin_usd"]) if d["structure"]["senior_mezz_covered"] else "no deal"
            cells.append("%9s" % cell)
        print("  %-12s %s" % (pct(el), "  ".join(cells)))
    print("  Read: the deal survives fee compression far better than loss - the")
    print("  cliff is the pool ceasing to clear, not our fee margin thinning.")


def write_results(scenarios, basis):
    """One row per (scenario, metric) to a committed CSV the dashboard reads.
    Every row carries the basis mix so the dashboard states plainly how sourced
    the model is."""
    sourced, total = basis_mix(basis)
    basis_note = ("SOURCED %d/%d drivers; remainder ASSUMED - not calibrated to field data"
                  % (sourced, total))
    rows = []
    for name in SCENARIOS:
        cfg = scenarios[name]
        n = cfg["avg_deal_notional"]
        d = deal_pnl(cfg, n)
        be = break_even_pool(cfg)
        e = evaluate(cfg)
        v = e["venture"]
        sc = d["structure"]
        def add(metric, value, unit, detail):
            rows.append({"Scenario": name, "Metric": metric, "Value": value,
                         "Unit": unit, "Detail": detail,
                         "Model_Version": MODEL_VERSION, "Basis": basis_note})
        add("Deal net margin", round(d["net_margin_usd"], 0), "USD",
            "on a %s pool over %.1fy" % (money(n), cfg["weighted_life_years"]))
        add("Deal net margin", round(100 * d["net_margin_pct"], 2), "% of notional",
            "structuring-company margin")
        add("Break-even pool size", round(be, 0) if be else "", "USD",
            "notional at which our net margin = 0")
        add("Gate: cover costs", "pass" if e["gate_pass"] else "fail", "bool",
            "venture break-even within %.0fy" % e["gate_horizon"])
        add("Years to break-even", v["break_even_year"] or "", "years",
            "venture-level, incl. %s/yr overhead" % money(cfg["annual_overhead_usd"]))
        add("Deals to break-even", v["break_even_deals"] or "", "deals",
            "cumulative, at %.0f deals/yr" % cfg["deals_per_year"])
        add("KPI1 operating margin", round(100 * e["kpi1_op_margin"], 2), "%",
            "steady-state; target %s" % pct(e["kpi1_target"]))
        add("KPI2 return on capital-at-risk", round(100 * e["kpi2_rocar"], 2), "%",
            "on %s strip; target %s" % (money(v["capital_at_risk_usd"]), pct(e["kpi2_target"])))
        add("Steady-state margin", round(v["steady_state_margin_usd"], 0), "USD/yr",
            "on a %s book" % money(v["steady_state_book_usd"]))
        add("Junior residual return", round(100 * sc["junior_return"], 2), "%",
            "binding constraint; hurdle %s" % pct(cfg["junior_hurdle_pct"]))
        add("Senior+mezz covered", "yes" if sc["senior_mezz_covered"] else "no", "bool",
            "does pool spread pay senior+mezz coupons")
    with open(RESULTS, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()),
                           quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("Wrote %s" % os.path.relpath(RESULTS, ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenario", choices=SCENARIOS, help="run a single scenario")
    ap.add_argument("--deal", action="store_true", help="deal-level P&L only")
    ap.add_argument("--venture", action="store_true", help="venture ramp only")
    ap.add_argument("--pilot", action="store_true", help="pilot-breakeven yardstick")
    ap.add_argument("--sensitivity", action="store_true", help="loss x fee grid (Likely)")
    ap.add_argument("--no-write", action="store_true", help="do not rewrite the results CSV")
    args = ap.parse_args()

    scenarios, basis = load_config()
    sourced, total = basis_mix(basis)
    names = [args.scenario] if args.scenario else list(SCENARIOS)

    print("RT-6 UNIT-ECONOMICS MODEL  v%s" % MODEL_VERSION)
    print("Basis: %d/%d drivers SOURCED, %d ASSUMED. Outputs describe the MODEL,"
          % (sourced, total, total - sourced))
    print("not this asset class, while ASSUMED rows carry the load.\n")

    want_deal = args.deal or not (args.deal or args.venture or args.pilot or args.sensitivity)
    want_venture = args.venture or not (args.deal or args.venture or args.pilot or args.sensitivity)

    for name in names:
        cfg = scenarios[name]
        if want_deal:
            print_deal(name, cfg)
        if want_venture:
            print_venture(name, cfg)
        if want_deal or want_venture:
            print()

    if args.pilot or not (args.deal or args.venture or args.sensitivity):
        print_pilot(scenarios)
        print()
    if args.sensitivity:
        print_sensitivity(scenarios)
        print()

    full_run = not (args.scenario or args.deal or args.venture or args.pilot or args.sensitivity)
    if full_run and not args.no_write:
        write_results(scenarios, basis)
    return 0


if __name__ == "__main__":
    sys.exit(main())
