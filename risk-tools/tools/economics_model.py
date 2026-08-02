#!/usr/bin/env python3
"""RT-6 unit-economics model: does the structuring layer become a business?

    python3 risk-tools/tools/economics_model.py               # deal + venture summary
    python3 risk-tools/tools/economics_model.py --deal        # deal-level P&L only
    python3 risk-tools/tools/economics_model.py --venture      # venture ramp to break-even
    python3 risk-tools/tools/economics_model.py --pilot        # flagship pilot-breakeven yardstick
    python3 risk-tools/tools/economics_model.py --sensitivity  # loss-rate x fee-compression grids

WHAT THIS IS. A deterministic, closed-form economics model of the STRUCTURING
COMPANY - our own P&L - plus a check on whether the tranche stack clears the
returns investors require. It answers OQ-10: is there a credible path to
at-scale profitability at a scale we can realistically reach?

The split is deliberate and follows the OQ-10 framing locked 2026-08-02:

  - THE GATE is our own P&L. Structuring fee + servicing fee + return on the
    retained strip, less our fixed structuring cost and our servicing opex.
    "Is this a business for us" is judged here.
  - THE BINDING CONSTRAINT is the investor stack. If the pool's spread cannot
    pay the senior and mezzanine their required coupons after expected loss and
    the originator's share, there is no deal to structure - so we check it, but
    it is a gate on the deal existing, not on it being a business for us.

WHAT THIS IS NOT. It is not RT-5. RT-5 simulates the credit waterfall with a
correlated loss model and tells you how a tranche behaves under stress; it owns
the loss distribution and the fixed-cost floor (OQ-2). RT-6 takes a loss
ASSUMPTION (a point estimate, sweepable, and readable straight off an RT-5
scenario) and asks the economics question on top of it. RT-5 answers "does the
structure survive"; RT-6 answers "does the business pay".

CALIBRATION. Every driver in economics-config.csv carries a Basis tag:
SOURCED rows cite an open-access benchmark; ASSUMED rows are working values the
research phase exists to replace. The model prints the basis mix on every run,
and no output should be shown to an investor as a result while ASSUMED rows
carry the load. See risk-tools/rt-6-economics-model.md.

Reads:
  risk-tools/tools/economics-config.csv    drivers, each tagged SOURCED/ASSUMED
  risk-tools/tools/economics-assets.csv    flagship pilot profiles (EXP-01/02/06)

Writes:
  data/rt6-economics-results.csv           committed headline metrics

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


# --- config ------------------------------------------------------------------

def load_config():
    """Return (values, basis). values maps Parameter -> float; basis maps
    Parameter -> 'SOURCED'/'ASSUMED' so the model can report its own footing."""
    values, basis = {}, {}
    with open(CONFIG, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            values[row["Parameter"]] = float(row["Value"])
            basis[row["Parameter"]] = row["Basis"].split(" ")[0].upper()
    return values, basis


def load_assets():
    if not os.path.exists(ASSETS):
        return []
    with open(ASSETS, newline="", encoding="utf-8") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def basis_mix(basis):
    sourced = sum(1 for v in basis.values() if v == "SOURCED")
    return sourced, len(basis)


# --- the two computations ----------------------------------------------------

def structure_clears(cfg, notional, loss_pct=None):
    """The BINDING CONSTRAINT: does the pool's spread pay senior + mezz their
    required coupons, after expected loss, the originator's share and our fees,
    and what is left for the junior/first-loss layer?

    All flows are annualised on the pool notional and expressed as a rate on
    notional, so a reader can trace every term. Returns the residual return to
    the junior layer (a rate on the junior tranche) and the coverage checks.
    """
    el = cfg["expected_loss_pct"] if loss_pct is None else loss_pct

    # Gross spread available to the structure, per year, as a rate on notional.
    # Gross yield less what the origination layer keeps and less expected credit
    # loss. This is the pool of return every capital provider and fee is paid from.
    gross = cfg["gross_yield_pct"]
    originator = gross * cfg["originator_share_pct"]        # a share of gross yield
    net_spread = gross - originator - el

    # Our fee load is senior to the capital stack's returns in the waterfall
    # (fees come first). The servicing fee is annual; the structuring fee is
    # upfront and amortised over the pool's life for this rate comparison.
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
    """THE GATE: the structuring company's own P&L for one deal, over the pool's
    life. Returns absolute USD and margin as a % of notional.

    Revenue is ours to keep: the upfront structuring fee, the annual servicing
    fee over the pool's life, and the net return on the economic interest we are
    required to retain. Cost is ours to bear: the one-off fixed structuring cost
    (legal, SPV, rating, listing) and our own servicing/monitoring opex. The
    originator's economics and the investor coupons are NOT our cost - they live
    in structure_clears() as the constraint on the deal existing at all.
    """
    life = cfg["weighted_life_years"]

    rev_structuring = cfg["structuring_fee_pct"] * notional
    rev_servicing = cfg["servicing_fee_pct"] * notional * life

    # Return on the retained strip. We hold retained_interest_pct of notional;
    # its return is the junior residual (the strip is first-loss economic
    # interest), floored at zero - a wiped strip returns nothing, it does not
    # bill negatively here (the loss shows up as capital, tracked separately).
    sc = structure_clears(cfg, notional, loss_pct)
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
    in closed form. Above this size a deal pays for itself; below it, the fixed
    structuring cost is not covered by the variable margin - the same fixed-cost
    logic RT-5 finds for the junior tranche (OQ-2), here for our P&L.
    """
    life = cfg["weighted_life_years"]
    sc = structure_clears(cfg, 1.0, loss_pct)
    # Variable margin per $1 of notional over the pool life.
    per_dollar = (
        cfg["structuring_fee_pct"]
        + cfg["servicing_fee_pct"] * life
        + max(0.0, sc["junior_return"]) * cfg["retained_interest_pct"] * life
        - cfg["cost_to_serve_pct"] * life
    )
    if per_dollar <= 0:
        return None  # no pool size covers fixed cost; the deal never pays
    return cfg["fixed_structuring_cost_usd"] / per_dollar


def venture_ramp(cfg, loss_pct=None):
    """Venture level: cumulative net margin from a realistic deal ramp against
    the structuring company's own annual overhead. Returns the year and deal
    count at which the venture turns cumulatively profitable, and the steady-
    state annual margin once the book is built - the at-scale profitability the
    OQ-10 gate asks for.
    """
    per_year = cfg["deals_per_year"]
    size = cfg["avg_deal_notional"]
    overhead = cfg["annual_overhead_usd"]
    horizon = int(cfg["target_horizon_years"])

    rows = []
    cumulative = 0.0
    active_book = 0.0            # notional under management earning servicing fees
    life = cfg["weighted_life_years"]
    be_year = be_deals = None
    total_deals = 0

    # Per-deal upfront take is identical across deals of the same size, so
    # compute it once: the structuring fee plus one year's worth of the strip's
    # return (the retained return is booked over the pool's life, so 1/life here).
    d1 = deal_pnl(cfg, size, loss_pct)
    upfront_per_deal = d1["rev_structuring"] + d1["rev_retained"] / life

    for year in range(1, horizon + 1):
        new_deals = per_year
        total_deals += new_deals
        upfront = upfront_per_deal * new_deals
        # Servicing fee accrues on the active book. Pools roll off after `life`
        # years; approximate the book as the last `life` cohorts.
        active_book = min(year, life) * per_year * size
        servicing = cfg["servicing_fee_pct"] * active_book
        our_serving_cost = cfg["cost_to_serve_pct"] * active_book
        year_margin = upfront + servicing - our_serving_cost - overhead
        cumulative += year_margin
        if be_year is None and cumulative >= 0:
            be_year, be_deals = year, total_deals
        rows.append({
            "year": year, "deals_cumulative": total_deals,
            "active_book_usd": active_book, "year_margin_usd": year_margin,
            "cumulative_usd": cumulative,
        })

    steady = rows[-1]["year_margin_usd"]
    steady_book = rows[-1]["active_book_usd"]
    return {
        "rows": rows,
        "break_even_year": be_year,
        "break_even_deals": be_deals,
        "steady_state_margin_usd": steady,
        "steady_state_book_usd": steady_book,
        "steady_state_return_pct": steady / steady_book if steady_book else 0.0,
    }


# --- reporting ---------------------------------------------------------------

def money(x):
    return "$%s" % format(int(round(x)), ",")


def pct(x):
    return "%.2f%%" % (100 * x)


def print_deal(cfg, basis):
    n = cfg["avg_deal_notional"]
    d = deal_pnl(cfg, n)
    sc = d["structure"]
    print("DEAL-LEVEL P&L  (pool notional %s, life %.1fy)" % (money(n), cfg["weighted_life_years"]))
    print("  Our revenue")
    print("    structuring fee    %12s" % money(d["rev_structuring"]))
    print("    servicing fee      %12s" % money(d["rev_servicing"]))
    print("    retained interest  %12s" % money(d["rev_retained"]))
    print("    total revenue      %12s" % money(d["revenue"]))
    print("  Our cost")
    print("    fixed structuring  %12s" % money(d["cost_fixed"]))
    print("    servicing opex     %12s" % money(d["cost_serving"]))
    print("    total cost         %12s" % money(d["cost"]))
    print("  NET MARGIN           %12s   (%s of notional)"
          % (money(d["net_margin_usd"]), pct(d["net_margin_pct"])))
    be = break_even_pool(cfg)
    print("  Break-even pool size %12s" % (money(be) if be else "never (variable margin <= 0)"))
    print()
    print("  BINDING CONSTRAINT - does the investor stack clear?")
    print("    net spread to structure   %s" % pct(sc["net_spread"]))
    print("    less our fee load         %s" % pct(sc["fee_load"]))
    print("    senior+mezz coupon cost   %s" % pct(sc["senior_cost"] + sc["mezz_cost"]))
    print("    senior+mezz covered:      %s" % ("YES" if sc["senior_mezz_covered"] else "NO"))
    print("    residual junior return    %s  (hurdle %s -> %s)"
          % (pct(sc["junior_return"]), pct(cfg["junior_hurdle_pct"]),
             "clears" if sc["junior_clears_hurdle"] else "SHORT, needs concessional pricing"))
    print()


def print_venture(cfg, basis):
    v = venture_ramp(cfg)
    print("VENTURE RAMP  (%.0f deals/yr x %s, overhead %s/yr, horizon %.0fy)"
          % (cfg["deals_per_year"], money(cfg["avg_deal_notional"]),
             money(cfg["annual_overhead_usd"]), cfg["target_horizon_years"]))
    print("  %-6s %-8s %-16s %-16s %s" % ("year", "deals", "active book", "year margin", "cumulative"))
    for r in v["rows"]:
        print("  %-6d %-8d %-16s %-16s %s"
              % (r["year"], r["deals_cumulative"], money(r["active_book_usd"]),
                 money(r["year_margin_usd"]), money(r["cumulative_usd"])))
    if v["break_even_year"]:
        print("  BREAK-EVEN: year %d, after %d deals" % (v["break_even_year"], v["break_even_deals"]))
    else:
        print("  BREAK-EVEN: not reached within the horizon")
    print("  Steady-state annual margin %s on a %s book  (%s return on book)"
          % (money(v["steady_state_margin_usd"]), money(v["steady_state_book_usd"]),
             pct(v["steady_state_return_pct"])))
    tgt = cfg["target_margin_pct"]
    print("  OQ-10 gate: target %s return on book -> %s"
          % (pct(tgt),
             "MET" if v["steady_state_return_pct"] >= tgt else "not met at this ramp"))
    print()


def print_pilot(cfg, basis):
    assets = load_assets()
    if not assets:
        print("PILOT YARDSTICK: no economics-assets.csv found.")
        return
    print("PILOT-BREAKEVEN YARDSTICK  (companion to the gate, not the gate)")
    print("  A pilot pool is expected to be below break-even. The question is how")
    print("  far, and what closes the gap - scale, fee, or grant subsidy.\n")
    print("  %-8s %-26s %-14s %-14s %s" % ("asset", "pilot pool", "net margin", "% of notional", "x to break-even"))
    for a in assets:
        local = dict(cfg)
        for k in ("gross_yield_pct", "expected_loss_pct", "weighted_life_years"):
            if a.get(k):
                local[k] = float(a[k])
        n = float(a["pilot_notional_usd"])
        d = deal_pnl(local, n)
        be = break_even_pool(local)
        mult = ("%.1fx" % (be / n)) if be and n else "n/a"
        print("  %-8s %-26s %-14s %-14s %s"
              % (a["Asset_ID"], "%s (%s loans)" % (money(n), a.get("pilot_loans", "?")),
                 money(d["net_margin_usd"]), pct(d["net_margin_pct"]), mult))
    print()


def print_sensitivity(cfg, basis):
    print("SENSITIVITY - net margin per deal (%s notional)\n" % money(cfg["avg_deal_notional"]))
    n = cfg["avg_deal_notional"]
    base_el = cfg["expected_loss_pct"]
    base_fee = cfg["structuring_fee_pct"]

    loss_grid = [base_el * m for m in (0.5, 1.0, 1.5, 2.0, 3.0)]
    fee_grid = [base_fee * m for m in (1.0, 0.75, 0.5, 0.25)]

    print("  rows: expected loss   cols: structuring fee (base -> compressed)")
    print("  %-14s %s" % ("", "  ".join("%7s" % pct(f) for f in fee_grid)))
    for el in loss_grid:
        cells = []
        for f in fee_grid:
            local = dict(cfg)
            local["structuring_fee_pct"] = f
            cells.append("%7s" % money(deal_pnl(local, n, loss_pct=el)["net_margin_usd"]))
        print("  %-14s %s" % (pct(el), "  ".join(cells)))
    print("\n  Read: where does net margin cross zero as loss rises and fees compress?")
    print()


def write_results(cfg, basis):
    """Headline metrics to a committed CSV the dashboard reads. Every row carries
    the basis mix so the dashboard can state plainly how sourced the model is."""
    sourced, total = basis_mix(basis)
    n = cfg["avg_deal_notional"]
    d = deal_pnl(cfg, n)
    be = break_even_pool(cfg)
    v = venture_ramp(cfg)
    sc = d["structure"]
    basis_note = ("SOURCED %d/%d drivers; remainder ASSUMED - not calibrated to field data"
                  % (sourced, total))
    rows = [
        {"Metric": "Deal net margin", "Value": round(d["net_margin_usd"], 0),
         "Unit": "USD", "Detail": "on a %s pool over %.1fy" % (money(n), cfg["weighted_life_years"]),
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
        {"Metric": "Deal net margin", "Value": round(100 * d["net_margin_pct"], 2),
         "Unit": "% of notional", "Detail": "structuring-company margin",
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
        {"Metric": "Break-even pool size", "Value": round(be, 0) if be else "",
         "Unit": "USD", "Detail": "notional at which our net margin = 0",
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
        {"Metric": "Deals to break-even", "Value": v["break_even_deals"] or "",
         "Unit": "deals", "Detail": "cumulative, at %.0f deals/yr" % cfg["deals_per_year"],
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
        {"Metric": "Years to break-even", "Value": v["break_even_year"] or "",
         "Unit": "years", "Detail": "venture-level, incl. %s/yr overhead" % money(cfg["annual_overhead_usd"]),
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
        {"Metric": "Steady-state margin", "Value": round(v["steady_state_margin_usd"], 0),
         "Unit": "USD/yr", "Detail": "on a %s book" % money(v["steady_state_book_usd"]),
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
        {"Metric": "Steady-state return on book", "Value": round(100 * v["steady_state_return_pct"], 2),
         "Unit": "%", "Detail": "vs OQ-10 gate of %s" % pct(cfg["target_margin_pct"]),
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
        {"Metric": "Junior residual return", "Value": round(100 * sc["junior_return"], 2),
         "Unit": "%", "Detail": "binding constraint; hurdle %s" % pct(cfg["junior_hurdle_pct"]),
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
        {"Metric": "Senior+mezz covered", "Value": "yes" if sc["senior_mezz_covered"] else "no",
         "Unit": "bool", "Detail": "does pool spread pay senior+mezz coupons",
         "Model_Version": MODEL_VERSION, "Basis": basis_note},
    ]
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
    ap.add_argument("--deal", action="store_true", help="deal-level P&L only")
    ap.add_argument("--venture", action="store_true", help="venture ramp to break-even")
    ap.add_argument("--pilot", action="store_true", help="flagship pilot-breakeven yardstick")
    ap.add_argument("--sensitivity", action="store_true", help="loss x fee sensitivity grid")
    ap.add_argument("--no-write", action="store_true", help="do not rewrite the results CSV")
    args = ap.parse_args()

    cfg, basis = load_config()
    sourced, total = basis_mix(basis)
    print("RT-6 UNIT-ECONOMICS MODEL  v%s" % MODEL_VERSION)
    print("Basis: %d/%d drivers SOURCED, %d ASSUMED. Outputs describe the MODEL,"
          % (sourced, total, total - sourced))
    print("not this asset class, while ASSUMED rows carry the load.\n")

    any_flag = args.deal or args.venture or args.pilot or args.sensitivity
    if args.deal or not any_flag:
        print_deal(cfg, basis)
    if args.venture or not any_flag:
        print_venture(cfg, basis)
    if args.pilot or not any_flag:
        print_pilot(cfg, basis)
    if args.sensitivity:
        print_sensitivity(cfg, basis)

    if not any_flag and not args.no_write:
        write_results(cfg, basis)
    return 0


if __name__ == "__main__":
    sys.exit(main())
