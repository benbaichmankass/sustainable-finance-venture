#!/usr/bin/env python3
"""RT-7 collective facility risk model - reference implementation.

One coffee collective, one crop season, many Monte Carlo paths. The collective
on-lends to members (CapEx and OpEx loans) and markets a share of their crop,
part of it sold forward. The question the model answers is: what loss
distribution does a lender to the collective face, and what drives it?

The risk chain, per path s:

  climate factor Z_c, price factor Z_p          (regional, global; optionally correlated)
    -> regional yield Y_s, reference price P_s  (lognormal; jumps on price)
    -> member production, local spot price      (member dispersion + idiosyncratic noise; basis)
    -> side-selling when spot >> forward        (committed crop diverted to spot)
    -> collective deliveries vs forward book    (forward sales, spot sales, shortfall cost)
    -> member revenue, cost, household floor    -> CFADS -> DSCR
    -> conditional PD from DSCR                 (anchored logistic; base PD at anchor DSCR)
    -> defaults with residual correlation       (one-factor copula for the channel the
                                                 factors above do not capture: LIT-036/037)
    -> member losses (EAD x LGD)
    -> collective net cash flow as first-loss buffer
    -> facility loss                            -> EL, UL, illustrative tranches

Two correlation channels are therefore explicit and separable, which is what
EXP-25 says the evidence requires: an ENVIRONMENTAL channel (yield and price,
through DSCR) and an INSTITUTIONAL channel (residual_correlation).

Everything is uncalibrated. See risk-tools/rt-7-collective-facility-model.md.

Dependency: numpy. The JavaScript port in dashboard/rt7-model.js implements
the same model for the interactive tab; test_rt7.py checks the two agree.
"""

from __future__ import annotations

import math

import numpy as np

MODEL_VERSION = "0.2"


# --- small numerics ----------------------------------------------------------

def norm_ppf(p):
    """Inverse standard normal CDF, Acklam's rational approximation, vectorised.
    Same algorithm as RT-5's _norm_ppf and the JS port, so thresholds agree
    across implementations to ~1e-9."""
    p = np.clip(np.asarray(p, dtype=float), 1e-300, 1.0 - 1e-16)
    out = np.empty_like(p)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    lo = p < plow
    hi = p > phigh
    mid = ~(lo | hi)
    q = np.sqrt(-2 * np.log(np.where(lo, p, 0.5)))
    out[lo] = ((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1))[lo]
    q = np.sqrt(-2 * np.log(np.where(hi, 1 - p, 0.5)))
    out[hi] = (-((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
                 ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)))[hi]
    qm = p - 0.5
    r = qm * qm
    out[mid] = ((((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*qm /
                (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1))[mid]
    return np.clip(out, -8.0, 8.0)


def lognormal_sigma(cv):
    """Log-sd that gives a lognormal with mean 1 and the given coefficient of variation."""
    return math.sqrt(math.log(1.0 + cv * cv))


def annuity_payment(principal, rate, years):
    if years <= 0:
        return 0.0
    if rate <= 0:
        return principal / years
    return principal * rate / (1.0 - (1.0 + rate) ** (-years))


def pd_curve(dscr, base_pd, p):
    """Conditional PD as a function of debt-service cover.

    Anchored logistic: PD equals base_pd exactly at pd_anchor_dscr, falls toward
    pd_floor_share x base_pd as cover strengthens, and rises toward pd_max as
    cover collapses. pd_dscr_sensitivity sets the steepness. Monotone
    decreasing in DSCR by construction.
    """
    pd_min = p["pd_floor_share"] * base_pd
    pd_max = p["pd_max"]
    base = np.clip(base_pd, pd_min + 1e-12, pd_max - 1e-12)
    frac = (base - pd_min) / (pd_max - pd_min)
    c = np.log(frac / (1.0 - frac))                       # logit of the anchor position
    z = p["pd_dscr_sensitivity"] * (p["pd_anchor_dscr"] - np.asarray(dscr, dtype=float)) + c
    z = np.clip(z, -40.0, 40.0)                             # inf DSCR (no debt) and collapsed cover
    sig = 1.0 / (1.0 + np.exp(-z))
    return pd_min + (pd_max - pd_min) * sig


# --- members -----------------------------------------------------------------

def generate_members(p, seed):
    """Synthetic collective. Returns a dict of member-level arrays.

    Member yields (relative productivity) ARE used downstream - the v0.1
    prototype generated them and then applied a single district yield to
    everyone. Loan flags, sizes, hedge ratios and other income follow the
    prototype's distributions with the hard-coded 0.5 log-sd exposed.
    """
    rng = np.random.default_rng(seed)
    n = int(p["n_members"])

    area = np.clip(rng.normal(p["avg_area_ha"], p["area_sd"], n), 0.2, None)
    s = lognormal_sigma(p["member_yield_dispersion"])
    productivity = rng.lognormal(-0.5 * s * s, s, n)        # mean 1
    hedge = np.clip(rng.normal(p["hedge_ratio_mean"], p["hedge_ratio_sd"], n), 0.0, 1.0)
    other_income = np.clip(rng.normal(p["other_income_mean"], p["other_income_sd"], n), 0.0, None)

    has_capex = rng.uniform(size=n) < p["capex_share"]
    has_opex = rng.uniform(size=n) < p["opex_share"]
    # Loan sizes scale with farm area, with lognormal noise around that line.
    # v0.1 drew them independently of the farm, which put a 2,500 USD asset
    # loan on a 0.3 ha plot and made the leverage distribution meaningless.
    scale = area / p["avg_area_ha"]
    s_l = p["loan_size_sigma"]
    capex = np.where(has_capex, p["avg_capex_size"] * scale * rng.lognormal(-0.5 * s_l * s_l, s_l, n), 0.0)
    opex = np.where(has_opex, p["avg_opex_size"] * scale * rng.lognormal(-0.5 * s_l * s_l, s_l, n), 0.0)

    ds_capex = np.array([annuity_payment(c, p["capex_rate"], int(p["capex_tenor_years"])) if c > 0 else 0.0
                         for c in capex])
    ds_opex = opex * (1.0 + p["opex_rate"])                 # one-season bullet
    debt_service = ds_capex + ds_opex
    ead = capex + opex

    # EAD-weighted blends of the product-level priors.
    with np.errstate(invalid="ignore", divide="ignore"):
        w_capex = np.where(ead > 0, capex / np.where(ead > 0, ead, 1.0), 0.0)
    base_pd = w_capex * p["base_pd_capex"] + (1 - w_capex) * p["base_pd_opex"]
    lgd = w_capex * p["lgd_capex"] + (1 - w_capex) * p["lgd_opex"]

    return {
        "n": n,
        "area": area,
        "productivity": productivity,
        "hedge": hedge,
        "other_income": other_income,
        "capex": capex,
        "opex": opex,
        "debt_service": debt_service,
        "ead": ead,
        "base_pd": base_pd,
        "lgd": lgd,
        "has_loan": ead > 0,
    }


# --- the simulation ----------------------------------------------------------

def simulate(p, n_paths=5000, seed=42, scenario=None, members=None, return_paths=False):
    """Run the model. Returns a results dict (see summarise). The member set is
    generated from `seed` unless passed in, so a sensitivity sweep can hold the
    collective fixed while a parameter moves."""
    scenario = scenario or {"climate_shift": 0.0, "price_shift": 0.0}
    m = members if members is not None else generate_members(p, seed)
    rng = np.random.default_rng(seed + 1_000_003)
    n, S = m["n"], int(n_paths)

    # 1. Systematic factors. One climate factor (regional) and one price factor
    #    (global) per path, optionally correlated.
    z_c = rng.standard_normal(S) + scenario["climate_shift"]
    rho_cp = p["climate_price_correlation"]
    z_p = rho_cp * (z_c - scenario["climate_shift"]) + math.sqrt(1 - rho_cp * rho_cp) * rng.standard_normal(S)

    # 2. Regional yield and reference price (lognormal, mean-preserving).
    s_y = lognormal_sigma(p["yield_vol"])
    regional_yield = p["base_yield_t_ha"] * np.exp(s_y * z_c - 0.5 * s_y * s_y)
    s_p = p["price_vol"]
    jump = (rng.uniform(size=S) < p["price_jump_prob"]) * rng.normal(p["price_jump_mean"], p["price_jump_sd"], S)
    ref_price = p["price_base_usd_per_t"] * (1 + scenario["price_shift"]) * np.exp(s_p * z_p - 0.5 * s_p * s_p + jump)
    spot = ref_price * (1 - p["basis_local"])               # local farm-gate spot

    # 3. Member production: area x persistent productivity x regional year x own noise.
    s_i = lognormal_sigma(p["member_yield_idio_vol"])
    idio = rng.lognormal(-0.5 * s_i * s_i, s_i, (S, n))
    production = m["area"][None, :] * m["productivity"][None, :] * regional_yield[:, None] * idio

    # 4. Forward book, contracted on EXPECTED deliveries before the season.
    expected_prod = m["area"] * m["productivity"] * p["base_yield_t_ha"]
    fwd_book = p["fwd_share"] * float(np.sum(m["hedge"] * expected_prod))   # tonnes
    fwd_price = p["fwd_price_usd_per_t"]

    # 5. Side-selling: when spot runs above forward by more than the threshold,
    #    members divert part of their committed crop to the spot market.
    premium = spot / fwd_price - 1.0
    diverted = np.clip(p["side_sell_elasticity"] * (premium - p["side_sell_threshold"]), 0.0, 1.0)   # (S,)
    committed = m["hedge"][None, :] * production                                 # tonnes a member owes the collective
    delivered_i = committed * (1 - diverted[:, None])
    sidesold_i = committed * diverted[:, None]
    own_spot_i = (1 - m["hedge"][None, :]) * production
    delivered = delivered_i.sum(axis=1)                                          # (S,)

    # 6. Collective sales, shortfall and margin.
    fwd_sold = np.minimum(delivered, fwd_book)
    spot_sold = np.maximum(delivered - fwd_book, 0.0)
    shortfall_t = np.maximum(fwd_book - delivered, 0.0)
    shortfall_cost = shortfall_t * (np.maximum(spot - fwd_price, 0.0) + p["penalty_per_ton_short"])
    gross_sales = fwd_sold * fwd_price + spot_sold * spot
    margin = p["collective_margin_rate"] * gross_sales
    payout_per_t = np.where(delivered > 0, (gross_sales - margin) / np.where(delivered > 0, delivered, 1.0), 0.0)
    net_cf = margin - shortfall_cost - p["collective_fixed_cost_usd"]

    # 7. Member cash flow available for debt service.
    revenue = (delivered_i * payout_per_t[:, None] + (sidesold_i + own_spot_i) * spot[:, None]
               + m["other_income"][None, :])
    cfads = revenue - m["area"][None, :] * p["production_cost_per_ha"] - p["household_floor_usd"]
    ds = m["debt_service"][None, :]
    # Members without debt get a large finite cover rather than inf, so the PD
    # curve never multiplies 0 x inf; their PD is masked to zero below anyway.
    dscr = np.where(ds > 0, cfads / np.where(ds > 0, ds, 1.0), 1e9)

    # 8. Conditional PD and correlated defaults.
    pd = np.where(m["has_loan"][None, :], pd_curve(dscr, m["base_pd"][None, :], p), 0.0)
    rho = p["residual_correlation"]
    z_r = rng.standard_normal(S)
    latent = math.sqrt(rho) * z_r[:, None] + math.sqrt(1 - rho) * rng.standard_normal((S, n))
    defaults = (latent < norm_ppf(pd)) & m["has_loan"][None, :]

    # 9. Losses and the collective buffer.
    member_loss = (defaults * m["ead"][None, :] * m["lgd"][None, :]).sum(axis=1)
    buffer = p["reserve_share_of_margin"] * np.maximum(net_cf, 0.0) - np.maximum(-net_cf, 0.0)
    pool = float(m["ead"].sum())
    # The facility cannot lose more than it lent. The collective's deficit beyond
    # that (an uncovered forward book in a price spike) falls on the collective
    # and its buyer, and is reported separately rather than silently dropped.
    uncapped = np.maximum(member_loss - buffer, 0.0)
    facility_loss = np.minimum(uncapped, pool)
    absorbed = np.minimum(member_loss, np.maximum(buffer, 0.0))

    # Normal-year reference: factors at zero, no noise - what the PD prior
    # implies for THIS collective's leverage. Exposes inconsistency between the
    # base PD and the loan-size / cost assumptions.
    ref = _normal_year(p, m)

    res = summarise(facility_loss, member_loss, pool, p)
    res.update({
        "model_version": MODEL_VERSION,
        "n_paths": S,
        "n_members": n,
        "n_borrowers": int(m["has_loan"].sum()),
        "pool_notional_usd": pool,
        "fwd_book_t": fwd_book,
        "expected_delivered_t": float(np.sum(m["hedge"] * expected_prod)),
        "mean_default_rate": float(defaults.sum(axis=1).mean() / max(1, m["has_loan"].sum())),
        "mean_pd": float(pd[:, m["has_loan"]].mean()) if m["has_loan"].any() else 0.0,
        "normal_year_pd": ref["pd"],
        "normal_year_median_dscr": ref["median_dscr"],
        "share_dscr_below_1": float((dscr[:, m["has_loan"]] < 1.0).mean()) if m["has_loan"].any() else 0.0,
        "p_shortfall": float((shortfall_t > 0).mean()),
        "mean_shortfall_cost_usd": float(shortfall_cost.mean()),
        "mean_diverted_share": float(diverted.mean()),
        "p_side_selling": float((diverted > 0).mean()),
        "mean_collective_net_cf_usd": float(net_cf.mean()),
        "p_collective_deficit": float((net_cf < 0).mean()),
        "mean_collective_deficit_usd": float(np.maximum(-net_cf, 0.0).mean()),
        "p_loss_capped_at_pool": float((uncapped > pool).mean()),
        "mean_buffer_absorbed_usd": float(absorbed.mean()),
        "mean_member_loss_usd": float(member_loss.mean()),
        "member_el_pct": float(member_loss.mean() / pool) if pool else 0.0,
        "mean_regional_yield_t_ha": float(regional_yield.mean()),
        "mean_spot_usd_per_t": float(spot.mean()),
        "loss_histogram": histogram(facility_loss / pool if pool else facility_loss),
    })
    if return_paths:
        res["paths"] = {
            "facility_loss": facility_loss, "member_loss": member_loss, "net_cf": net_cf,
            "regional_yield": regional_yield, "spot": spot, "dscr": dscr, "pd": pd,
            "defaults": defaults, "shortfall_t": shortfall_t, "diverted": diverted,
        }
        res["members"] = m
    return res


def _normal_year(p, m):
    """Deterministic pass with every factor at its mean and no noise."""
    expected_prod = m["area"] * m["productivity"] * p["base_yield_t_ha"]
    spot = p["price_base_usd_per_t"] * (1 - p["basis_local"])
    fwd_book = p["fwd_share"] * float(np.sum(m["hedge"] * expected_prod))
    delivered = float(np.sum(m["hedge"] * expected_prod))
    fwd_sold = min(delivered, fwd_book)
    gross = fwd_sold * p["fwd_price_usd_per_t"] + max(delivered - fwd_book, 0.0) * spot
    payout = (gross * (1 - p["collective_margin_rate"]) / delivered) if delivered > 0 else 0.0
    revenue = m["hedge"] * expected_prod * payout + (1 - m["hedge"]) * expected_prod * spot + m["other_income"]
    cfads = revenue - m["area"] * p["production_cost_per_ha"] - p["household_floor_usd"]
    loans = m["has_loan"]
    if not loans.any():
        return {"pd": 0.0, "median_dscr": float("nan")}
    dscr = cfads[loans] / m["debt_service"][loans]
    pd = pd_curve(dscr, m["base_pd"][loans], p)
    w = m["ead"][loans]
    return {"pd": float(np.sum(pd * w) / np.sum(w)), "median_dscr": float(np.median(dscr))}


# --- summaries ---------------------------------------------------------------

def tranche_metrics(loss_frac, attach, detach):
    width = detach - attach
    tl = np.clip(loss_frac - attach, 0.0, width) / width       # loss as share of tranche notional
    return {
        "attach": attach, "detach": detach,
        "el_pct": float(tl.mean()),
        "ul95_pct": float(np.percentile(tl, 95)),
        "ul99_pct": float(np.percentile(tl, 99)),
        "p_any_loss": float((tl > 0).mean()),
        "p_wipeout": float((tl >= 1.0 - 1e-12).mean()),
    }


def attachment_for_target(loss_frac, target_el):
    """Smallest first-loss thickness (as a share of pool) at which a senior
    tranche attaching there has expected loss <= target_el (share of senior
    notional). Bisection on a monotone function; returns 1.0 if unattainable."""
    def senior_el(a):
        if a >= 1.0:
            return 0.0
        return float(np.mean(np.clip(loss_frac - a, 0.0, 1.0 - a)) / (1.0 - a))
    if senior_el(0.0) <= target_el:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if senior_el(mid) <= target_el:
            hi = mid
        else:
            lo = mid
    return hi


def histogram(loss_frac, n_bins=40, cap=None):
    """Fixed-width bins on loss as a share of pool, for the dashboard chart.
    The cap is the p99 rounded up to a clean step, so a long tail does not
    squash the body into one bar; everything above the cap lands in the last bin."""
    x = np.asarray(loss_frac, dtype=float)
    if cap is None:
        hi = float(np.percentile(x, 99.0)) if len(x) else 0.0
        cap = max(0.02, math.ceil(hi * 100 / 2) * 2 / 100)   # steps of 2 percentage points
    edges = np.linspace(0.0, cap, n_bins + 1)
    counts, _ = np.histogram(np.minimum(x, cap - 1e-12), bins=edges)
    return {"edges": [float(e) for e in edges], "counts": [int(c) for c in counts], "n": int(len(x))}


def summarise(facility_loss, member_loss, pool, p):
    lf = facility_loss / pool if pool > 0 else np.zeros_like(facility_loss)
    eq, mz = p["tranche_equity_detach"], p["tranche_mezz_detach"]
    return {
        "el_usd": float(facility_loss.mean()),
        "el_pct": float(lf.mean()),
        "ul95_pct": float(np.percentile(lf, 95)),
        "ul99_pct": float(np.percentile(lf, 99)),
        "ul95_usd": float(np.percentile(facility_loss, 95)),
        "ul99_usd": float(np.percentile(facility_loss, 99)),
        "sd_pct": float(lf.std()),
        "p_no_loss": float((facility_loss <= 1e-9).mean()),
        "tranches": {
            "equity": tranche_metrics(lf, 0.0, eq),
            "mezz": tranche_metrics(lf, eq, mz),
            "senior": tranche_metrics(lf, mz, 1.0),
        },
        "attachment_for_senior_target": attachment_for_target(lf, p["senior_el_target_bp"] / 10000.0),
    }


# --- sensitivity -------------------------------------------------------------

# (parameter, how, low, high). "abs" shifts the value; "mul" scales it; "set" replaces it.
TORNADO = [
    ("hedge_ratio_mean", "abs", -0.20, 0.20),
    ("fwd_share", "abs", -0.25, 0.25),
    ("fwd_price_usd_per_t", "mul", 0.90, 1.10),
    ("yield_vol", "mul", 0.50, 1.50),
    ("price_vol", "mul", 0.50, 1.50),
    ("basis_local", "abs", -0.05, 0.05),
    ("base_pd_opex", "mul", 0.50, 1.50),
    ("base_pd_capex", "mul", 0.50, 1.50),
    ("lgd_opex", "abs", -0.15, 0.15),
    ("lgd_capex", "abs", -0.15, 0.15),
    ("residual_correlation", "set", 0.0, 0.30),
    ("household_floor_usd", "mul", 0.75, 1.25),
    ("production_cost_per_ha", "mul", 0.75, 1.25),
    ("side_sell_elasticity", "set", 0.0, 2.0),
    ("collective_fixed_cost_usd", "mul", 0.5, 2.0),
    ("pd_dscr_sensitivity", "mul", 0.5, 1.5),
]

CLAMP_01 = {"hedge_ratio_mean", "fwd_share", "basis_local", "base_pd_opex", "base_pd_capex",
            "lgd_opex", "lgd_capex", "residual_correlation"}


def shocked(p, name, how, v):
    q = dict(p)
    base = p[name]
    val = base + v if how == "abs" else base * v if how == "mul" else v
    if name in CLAMP_01:
        val = min(max(val, 0.0), 0.95 if name == "residual_correlation" else 1.0)
    if name in ("yield_vol", "price_vol"):
        val = max(val, 0.0)
    q[name] = val
    return q


def tornado(p, n_paths=3000, seed=42, scenario=None):
    """One-at-a-time sensitivity of EL and UL99 to each entry in TORNADO.

    The member set is regenerated from the same seed on every run rather than
    held fixed: generation is deterministic in the seed, so the collective is
    the same set of draws, and a parameter that acts at generation (hedge
    ratio, base PD, LGD, loan size) moves the attribute it should move instead
    of being silently frozen. Returns rows sorted by swing in EL."""
    base = simulate(p, n_paths, seed, scenario)
    rows = []
    for name, how, lo, hi in TORNADO:
        if name not in p:
            continue
        r_lo = simulate(shocked(p, name, how, lo), n_paths, seed, scenario)
        r_hi = simulate(shocked(p, name, how, hi), n_paths, seed, scenario)
        rows.append({
            "parameter": name, "how": how, "low": lo, "high": hi,
            "value_low": shocked(p, name, how, lo)[name], "value_high": shocked(p, name, how, hi)[name],
            "el_low": r_lo["el_pct"], "el_high": r_hi["el_pct"], "el_base": base["el_pct"],
            "ul99_low": r_lo["ul99_pct"], "ul99_high": r_hi["ul99_pct"], "ul99_base": base["ul99_pct"],
            "swing_el": abs(r_hi["el_pct"] - r_lo["el_pct"]),
        })
    rows.sort(key=lambda r: -r["swing_el"])
    return base, rows
