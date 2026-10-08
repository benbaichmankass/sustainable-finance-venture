#!/usr/bin/env python3
"""Turn the processed open-data series into observed RT-7 parameters.

    python3 scripts/ingest/calibrate_rt7.py           # compute -> data/rt7-calibration.csv
    python3 scripts/ingest/calibrate_rt7.py --apply   # also write the values into data/rt7-parameters.csv

What is calibrated, and from what:

  price_vol             DS-04  annualised sd of monthly log returns over the window
  price_base_usd_per_t  DS-04  mean of the last 12 months of the reference series
  fwd_price_usd_per_t   DS-04  derived: price_base x (1 - FWD_DISCOUNT); the discount is an
                               assumption, so the row stays Basis assumption with the derivation noted
  yield_vol             DS-01  sd of residuals from a linear trend on log national yield
  base_yield_t_ha       DS-01  trend value in the last year (national, see caveat)

What is observed but NOT written into the model, because the model has no
parameter for it yet or the estimate is too weak to carry - reported in the
calibration file so the next modelling step starts from numbers:

  price_12m_change_p05/p50/p95   DS-04  distribution of rolling 12-month log changes
  price_jump_share               DS-04  share of 12-month windows with |log change| > 0.40
  yield_rain_corr                DS-01 x DS-03  correlation of yield residuals with the
                                  standardised annual rainfall anomaly (district mean)
  yield_price_corr               DS-01 x DS-04  correlation of yield residuals with the
                                  annual log change of the region's reference price

Phase 3b added two more sources of values:

  basis_local (Colombia)  DS-10 x DS-09 x DS-04  mean discount of the FNC internal price,
                          converted to USD per tonne of green coffee at the TRM, to the
                          Pink Sheet Arabica price, months from 2024-04 (factor 94 documented)
  avg_opex_size, base_pd_opex (Colombia)  DS-11  Kiva coffee-loan mean size and the
                          loans-posted-weighted arrears rate of the Colombian partners;
                          Basis proxy. Viet Nam's Kiva coffee loans all sit with one
                          distressed partner and are reported as observations only
  literature inputs       data/rt7-literature-inputs.csv  values derived by stated
                          arithmetic from published figures (Fairtrade, DANE, LIT-033 ...);
                          rows with Apply = yes are applied with their Basis, the rest are
                          carried as observations

Phase 4 (model v0.3) added the climate and persistence parameters:

  climate_rain_beta       DS-01 x DS-02  correlation of national yield trend residuals with the
                          region's district rainfall anomaly (data/rt7-climate-history.csv),
                          signed; applied as observed with its standard error in the note
  portfolio_climate_cross_corr  DS-02  mean pairwise correlation of the three regions' rainfall
                          anomalies (floored at 0), for the portfolio layer's shared climate factor
  collective_climate_idio_share  DS-02  1 - correlation of the two districts' anomalies within
                          a region: the share of a district's climate year not shared with its region
  price_persistence       DS-04  lag-1 autocorrelation of detrended annual log price, 20-year window

Arabica is the reference for Colombia and Ethiopia, Robusta for Viet Nam
(data/rt7-regions.csv). Python 3 stdlib.
"""

from __future__ import annotations

import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

PRICE_WINDOW_YEARS = 20
YIELD_WINDOW_YEARS = 25
FWD_DISCOUNT = 0.025          # assumption: forward price 2.5% under the reference, as in the prototype (3900/4000)
JUMP_THRESHOLD = 0.40
OUT = os.path.join(C.ROOT, "data", "rt7-calibration.csv")
PARAMS = os.path.join(C.ROOT, "data", "rt7-parameters.csv")
REGIONS = os.path.join(C.ROOT, "data", "rt7-regions.csv")
LIT_INPUTS = os.path.join(C.ROOT, "data", "rt7-literature-inputs.csv")
KG_EXCELSO_PER_CARGA = 93.09   # FNC: a carga of 125 kg parchment at factor 94 yields 93.09 kg excelso (RES-33)
LB_PER_T = 2204.62
KIVA_COUNTRY = {"colombia": "CO", "vietnam": "VN"}


def mean(x): return sum(x) / len(x)
def sd(x):
    m = mean(x); return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1)) if len(x) > 1 else 0.0
def corr(x, y):
    mx, my = mean(x), mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else float("nan")
def pct(x, q):
    s = sorted(x); i = (len(s) - 1) * q; lo, hi = int(math.floor(i)), int(math.ceil(i))
    return s[lo] + (s[hi] - s[lo]) * (i - lo)
def linfit(xs, ys):
    mx, my = mean(xs), mean(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return my - b * mx, b


def price_stats(series_key):
    rows = [r for r in C.read_processed("ds-04-coffee-prices-monthly") if r[series_key]]
    last_year = int(rows[-1]["Month"][:4])
    win = [r for r in rows if int(r["Month"][:4]) > last_year - PRICE_WINDOW_YEARS]
    p = [float(r[series_key]) for r in win]
    lr = [math.log(b / a) for a, b in zip(p, p[1:])]
    ch12 = [math.log(p[i] / p[i - 12]) for i in range(12, len(p))]
    annual = {}
    for r in rows:
        annual.setdefault(int(r["Month"][:4]), []).append(float(r[series_key]))
    annual_mean = {y: mean(v) for y, v in annual.items() if len(v) == 12}
    years = sorted(annual_mean)
    annual_logchg = {y: math.log(annual_mean[y] / annual_mean[y - 1]) for y in years if y - 1 in annual_mean}
    return {
        "window": "%s to %s" % (win[0]["Month"], win[-1]["Month"]),
        "vol": sd(lr) * math.sqrt(12),
        "base": mean(p[-12:]),
        "window_mean": mean(p),
        "last_month": rows[-1]["Month"],
        "p05": pct(ch12, 0.05), "p50": pct(ch12, 0.5), "p95": pct(ch12, 0.95),
        "jump_share": sum(1 for c in ch12 if abs(c) > JUMP_THRESHOLD) / len(ch12),
        "annual_logchg": annual_logchg,
    }


def yield_stats(region):
    rows = [r for r in C.read_processed("ds-01-coffee-national-yields") if r["Region"] == region and r["Yield_t_ha"]]
    last_year = int(rows[-1]["Year"])
    win = [r for r in rows if int(r["Year"]) > last_year - YIELD_WINDOW_YEARS]
    xs = [int(r["Year"]) for r in win]; ys = [math.log(float(r["Yield_t_ha"])) for r in win]
    a, b = linfit(xs, ys)
    resid = {x: y - (a + b * x) for x, y in zip(xs, ys)}
    return {
        "window": "%d to %d" % (xs[0], xs[-1]),
        "cv": sd(list(resid.values())),
        "trend_last": math.exp(a + b * xs[-1]),
        "actual_last": float(win[-1]["Yield_t_ha"]),
        "trend_pct_per_year": (math.exp(b) - 1) * 100,
        "resid": resid,
    }


def rain_anomaly(region):
    rows = [r for r in C.read_processed("ds-03-district-climate-monthly") if r["Region"] == region]
    by_year = {}
    for r in rows:
        by_year.setdefault((r["District"], int(r["Month"][:4])), []).append(float(r["Precip_mm"]))
    annual = {}
    for (d, y), v in by_year.items():
        if len(v) == 12:
            annual.setdefault(y, []).append(sum(v))
    annual = {y: mean(v) for y, v in annual.items()}
    ys = sorted(annual); vals = [annual[y] for y in ys]
    m, s = mean(vals), sd(vals)
    return {y: (annual[y] - m) / s for y in ys}, {"mean_mm": m, "cv": s / m, "window": "%d to %d" % (ys[0], ys[-1])}


def colombia_basis():
    """Discount of the Colombian farm-gate (FNC internal base price) to the world reference,
    month by month, for months where the base yield factor is 94 and all three series exist."""
    p10 = {r["Month"]: r for r in C.read_processed("ds-10-colombia-coffee-prices-monthly")}
    fx = {r["Period"]: float(r["LCU_per_USD"]) for r in C.read_processed("ds-09-exchange-rates")
          if r["Currency"] == "COP" and r["Frequency"] == "monthly"}
    p4 = {r["Month"]: r for r in C.read_processed("ds-04-coffee-prices-monthly")}
    vs_ref, vs_milds, months = [], [], []
    for m in sorted(p10):
        r = p10[m]
        if r["Base_Yield_Factor_Assumed"] != "94" or not r["Internal_Price_COP_per_carga"] or m not in fx or m not in p4 \
                or not p4[m]["Arabica_USD_per_t"] or not r["ICO_Colombian_Milds_USc_per_lb"]:
            continue
        usd_t = float(r["Internal_Price_COP_per_carga"]) / KG_EXCELSO_PER_CARGA * 1000 / fx[m]
        vs_ref.append(1 - usd_t / float(p4[m]["Arabica_USD_per_t"]))
        vs_milds.append(1 - usd_t / (float(r["ICO_Colombian_Milds_USc_per_lb"]) / 100 * LB_PER_T))
        months.append(m)
    return {"n": len(months), "window": "%s to %s" % (months[0], months[-1]),
            "vs_ref": mean(vs_ref), "vs_ref_sd": sd(vs_ref), "vs_milds": mean(vs_milds), "vs_milds_sd": sd(vs_milds)}


def kiva_stats(country):
    loans = [r for r in C.read_processed("ds-11-kiva-agriculture-loans") if r["Country"] == country]
    partners = [r for r in C.read_processed("ds-11-kiva-partners") if country in r["Countries"].split(";")]
    coffee = [r for r in loans if r["Coffee_Mention"] == "yes"]
    amt = [float(r["Amount_USD"]) for r in coffee]
    term = [float(r["Term_Months"]) for r in coffee if r["Term_Months"]]
    posted = {p["Partner_ID"]: float(p["Loans_Posted"] or 0) for p in partners}
    tot = sum(posted.values())
    w_arr = sum(posted[p["Partner_ID"]] * float(p["Arrears_Rate_Pct"]) for p in partners) / tot / 100
    w_def = sum(posted[p["Partner_ID"]] * float(p["Default_Rate_Pct"]) for p in partners) / tot / 100
    dates = sorted(r["Raised_Date"] for r in coffee if r["Raised_Date"])
    return {"n_loans": len(loans), "n_coffee": len(coffee), "window": "%s to %s" % (dates[0], dates[-1]),
            "amt_mean": mean(amt), "amt_median": pct(amt, 0.5), "amt_logsd": sd([math.log(a) for a in amt]),
            "term_median": pct(term, 0.5), "w_arrears": w_arr, "w_default": w_def, "n_partners": len(partners),
            "group_share": sum(1 for r in coffee if r["Borrower_Count"] not in ("", "1")) / len(coffee),
            "partners": partners}


def climate_history():
    path = os.path.join(C.ROOT, "data", "rt7-climate-history.csv")
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.setdefault(r["Region"], {})[int(r["Year"])] = float(r["Rain_Anomaly_Z"])
    return out


def district_annual():
    try:
        rows = C.read_processed("ds-02-district-rainfall-annual")
    except FileNotFoundError:
        return {}
    out = {}
    for r in rows:
        out.setdefault((r["Region"], r["District"]), {})[int(r["Year"])] = float(r["Anomaly_Z"])
    return out


def price_persistence(series_key):
    """Lag-1 autocorrelation of annual mean log price around a linear trend."""
    rows = [r for r in C.read_processed("ds-04-coffee-prices-monthly") if r[series_key]]
    annual = {}
    for r in rows:
        annual.setdefault(int(r["Month"][:4]), []).append(float(r[series_key]))
    last = max(y for y, v in annual.items() if len(v) == 12)
    ys = [y for y in sorted(annual) if len(annual[y]) == 12 and y > last - PRICE_WINDOW_YEARS]
    lp = [math.log(mean(annual[y])) for y in ys]
    a, b = linfit(ys, lp)
    res = [v - (a + b * y) for y, v in zip(ys, lp)]
    return corr(res[:-1], res[1:]), "%d to %d" % (ys[0], ys[-1]), len(ys)


def literature_inputs():
    with open(LIT_INPUTS, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    apply = "--apply" in sys.argv
    regions = list(csv.DictReader(open(REGIONS, newline="", encoding="utf-8")))
    series_for = {r["Region"]: ("arabica" if "Arabica" in r["Price_Series"] else "robusta") for r in regions}
    prices = {k: price_stats("Arabica_USD_per_t" if k == "arabica" else "Robusta_USD_per_t") for k in ("arabica", "robusta")}
    out = []
    stamp = C.now_iso()

    def add(region, param, value, unit, method, window, ds, note, apply_as=None):
        out.append({"Region": region, "Parameter": param, "Observed_Value": ("%.6g" % value) if isinstance(value, float) else str(value),
                    "Unit": unit, "Method": method, "Window": window, "Dataset": ds, "Computed_At": stamp,
                    "Apply_As": apply_as or "", "Note": note})

    for reg in regions:
        region, sk = reg["Region"], series_for[reg["Region"]]
        ps = prices[sk]
        label = "Arabica" if sk == "arabica" else "Robusta"
        add(region, "price_vol", ps["vol"], "annual log volatility",
            "sd of monthly log returns x sqrt(12), %s reference series" % label, ps["window"], "DS-04",
            "World reference price, not farm-gate; nominal series, drift removed by differencing.", "observed")
        add(region, "price_base_usd_per_t", ps["base"], "USD / t",
            "mean of the last 12 months of the %s reference series" % label, "12 months to %s" % ps["last_month"], "DS-04",
            "Season-start level. The file ends %s; refresh DS-04 before any run that is meant to be current." % ps["last_month"], "observed")
        add(region, "fwd_price_usd_per_t", ps["base"] * (1 - FWD_DISCOUNT), "USD / t",
            "derived: price_base_usd_per_t x (1 - %.3f)" % FWD_DISCOUNT, "12 months to %s" % ps["last_month"], "DS-04",
            "The %.1f percent forward discount is an assumption carried from the prototype (3900/4000); only the base is observed." % (100 * FWD_DISCOUNT), "assumption")
        add(region, "price_mean_window_usd_per_t", ps["window_mean"], "USD / t",
            "mean of the %s reference series over the window (nominal)" % label, ps["window"], "DS-04",
            "Observation only. The applied base is the last 12 months; this is the long-window level for a reader who wants a structural rather than a current run. Nominal, so it understates today's dollars.")
        add(region, "price_12m_change_p05", ps["p05"], "log change", "5th percentile of rolling 12-month log changes", ps["window"], "DS-04",
            "Observation only. For comparison with the model's price_vol and jump parameters.")
        add(region, "price_12m_change_p50", ps["p50"], "log change", "median rolling 12-month log change", ps["window"], "DS-04", "Observation only.")
        add(region, "price_12m_change_p95", ps["p95"], "log change", "95th percentile of rolling 12-month log changes", ps["window"], "DS-04", "Observation only.")
        add(region, "price_jump_share", ps["jump_share"], "share of 12-month windows",
            "share of rolling 12-month windows with |log change| > %.2f" % JUMP_THRESHOLD, ps["window"], "DS-04",
            "Observation only; the model's price_jump_prob is per season and remains an assumption.")

        ys = yield_stats(region)
        add(region, "yield_vol", ys["cv"], "CV (year to year, national)",
            "sd of residuals from a linear trend on log national yield", ys["window"], "DS-01",
            "National series. District and member variability are larger; this is a floor, not an estimate of the regional factor the model needs.", "observed")
        add(region, "base_yield_t_ha", ys["trend_last"], "t green coffee / ha",
            "trend value in the last year (actual %.3f; trend %+.2f percent a year)" % (ys["actual_last"], ys["trend_pct_per_year"]), ys["window"], "DS-01",
            "NATIONAL average. A coffee district or a cooperative can sit well above or below it. Replace with district statistics or DS-08 before believing the level.", "observed")

        try:
            ra, rs = rain_anomaly(region)
            yrs = [y for y in ys["resid"] if y in ra]
            r_ry = corr([ys["resid"][y] for y in yrs], [ra[y] for y in yrs])
            add(region, "annual_rain_cv", rs["cv"], "CV", "sd / mean of district-mean annual precipitation (two districts averaged)", rs["window"], "DS-03",
                "Observation only; mean %.0f mm a year." % rs["mean_mm"])
            add(region, "yield_rain_corr", r_ry, "correlation", "corr(yield trend residual, standardised annual rainfall anomaly), same calendar year, %d years" % len(yrs),
                "%d to %d" % (yrs[0], yrs[-1]), "DS-01; DS-03",
                "Observation only. National yield against a two-point district rainfall index; a weak number is expected and says little either way.")
        except FileNotFoundError:
            pass
        alc = ps["annual_logchg"]
        yrs = [y for y in ys["resid"] if y in alc]
        add(region, "yield_price_corr", corr([ys["resid"][y] for y in yrs], [alc[y] for y in yrs]), "correlation",
            "corr(yield trend residual, annual log change of the %s reference), same year, %d years" % (label, len(yrs)),
            "%d to %d" % (yrs[0], yrs[-1]), "DS-01; DS-04",
            "Observation only, bearing on climate_price_correlation (assumed 0). A small origin's bad year barely moves the world price; a large one's can.")

        # --- Phase 3b: farm-gate basis, Kiva proxies, literature inputs ---
        if region == "colombia":
            cb = colombia_basis()
            add(region, "basis_local", cb["vs_ref"], "share below reference price",
                "mean over %d months of 1 - (FNC internal price / %.2f kg excelso per carga x 1000 / TRM) / Pink Sheet Arabica" % (cb["n"], KG_EXCELSO_PER_CARGA),
                cb["window"], "DS-10; DS-09; DS-04",
                "Month-to-month sd %.3f. The internal price is the FNC base purchase price at factor 94, i.e. what a grower is paid for standard parchment; premia for quality or certification sit on top, and a cooperative's own margin comes off. Nominal, so no inflation adjustment is needed." % cb["vs_ref_sd"], "observed")
            add(region, "basis_vs_ico_colombian_milds", cb["vs_milds"], "share below ICO Colombian milds",
                "same conversion against the ICO Colombian milds indicator (DS-10)", cb["window"], "DS-10; DS-09",
                "Observation only (sd %.3f): the discount to the group the coffee actually belongs to. The model prices off the Pink Sheet Arabica series, which follows other milds, hence the applied basis above." % cb["vs_milds_sd"])
        if region in KIVA_COUNTRY:
            ks = kiva_stats(KIVA_COUNTRY[region])
            applied = region == "colombia"
            why = ("Kiva borrowers of microfinance partners, not cooperative members; %d coffee-purpose loans among the %d newest agriculture loans."
                   % (ks["n_coffee"], ks["n_loans"]))
            if not applied:
                why += " NOT applied: every Vietnamese coffee loan sits with one partner that Kiva lists as paused with 68 percent of its book in arrears, and 91 percent are group loans, so neither size nor repayment is a fair proxy for a Dak Lak collective."
            add(region, "avg_opex_size", ks["amt_mean"], "USD",
                "mean amount of Kiva loans whose use text mentions coffee (median %.0f, log sd %.2f)" % (ks["amt_median"], ks["amt_logsd"]),
                ks["window"], "DS-11", why, "proxy" if applied else None)
            add(region, "opex_term_months", ks["term_median"], "months",
                "median lender repayment term of the coffee-purpose loans", ks["window"], "DS-11",
                "Observation only. The model treats the OpEx loan as a one-season bullet; these loans amortise monthly over about a year and a half, which lowers exposure at any one point and spreads the repayment test across more than one harvest. Group loans: %.0f percent." % (100 * ks["group_share"]))
            add(region, "base_pd_opex", ks["w_arrears"], "probability per year",
                "arrears rate of the %d Kiva partners in the country, weighted by loans posted" % ks["n_partners"], "snapshot at retrieval", "DS-11",
                ("Portfolio-at-risk stands in for a normal-year PD: some arrears cure, so this overstates loss events, while the partners' default rate (%.1f percent of ended amounts, same weighting) understates them because write-offs lag. Kiva-funded books only. "
                 % (100 * ks["w_default"])) + ("" if applied else why), "proxy" if applied else None)
            add(region, "kiva_default_rate", ks["w_default"], "share of ended loan amount",
                "default rate of the same partners, weighted by loans posted", "partner history to retrieval", "DS-11",
                "Observation only; the lower bound to base_pd_opex above.")
        if region == "vietnam":
            p4 = {r["Month"]: r for r in C.read_processed("ds-04-coffee-prices-monthly")}
            li = [r for r in literature_inputs() if r["ID"] == "LI-18"]
            if li and p4.get("2024-11", {}).get("Robusta_USD_per_t"):
                fg = float(li[0]["Value"]); ref = float(p4["2024-11"]["Robusta_USD_per_t"])
                add(region, "basis_check_nov_2024", 1 - fg / ref, "share below reference price",
                    "1 - LI-18 farm-gate (%.0f USD/t) / Pink Sheet Robusta 2024-11 (%.0f USD/t)" % (fg, ref), "2024-11", "LIT-054; DS-09; DS-04",
                    "Observation only: a single month in a spike, when the Dak Lak farm-gate reportedly exceeded the monthly reference average. Says the assumed basis of 0.06 is not large, not what it is. A monthly farm-gate series is needed.")
        # --- Phase 4: district climate factor and persistence ---
        ch = climate_history().get(region)
        if ch:
            # Residuals from a trend fitted over the whole overlap with the rainfall record
            # (1981 onward), not the 25-year calibration window: the correlation needs every year it can get.
            yrows = [r for r in C.read_processed("ds-01-coffee-national-yields") if r["Region"] == region and r["Yield_t_ha"] and int(r["Year"]) in ch]
            xs_ = [int(r["Year"]) for r in yrows]; ly = [math.log(float(r["Yield_t_ha"])) for r in yrows]
            a_, b_ = linfit(xs_, ly)
            resid_full = {x: y - (a_ + b_ * x) for x, y in zip(xs_, ly)}
            yrs = sorted(resid_full)
            if len(yrs) >= 15:
                b = corr([resid_full[y] for y in yrs], [ch[y] for y in yrs])
                se = 1.0 / math.sqrt(len(yrs) - 3)
                add(region, "climate_rain_beta", b, "correlation",
                    "corr(national yield residual from a log-linear trend over the overlap, district rainfall anomaly averaged over the region's two districts), same calendar year, %d years" % len(yrs),
                    "%d to %d" % (yrs[0], yrs[-1]), "DS-01; DS-02",
                    "Signed. Standard error about %.2f, so a value inside that band is not distinguishable from zero and the empirical factor then barely differs from the normal one; the sign says whether wet or dry years are the bad years for this origin. National yield against district rain: a district yield series would sharpen it." % se, "observed")
                zs = [ch[y] for y in sorted(ch)]
                add(region, "district_rain_anomaly_p10", pct(zs, 0.10), "standard deviations",
                    "10th percentile of the region's standardised annual rainfall anomaly (%d years)" % len(zs), "%d to %d" % (min(ch), max(ch)), "DS-02",
                    "Observation: how deep a one-in-ten dry year is at the district (a normal factor puts it at -1.28); the gap is what the empirical factor carries.")
                add(region, "district_rain_anomaly_skew", mean([z ** 3 for z in zs]) / (sd(zs) ** 3), "skewness",
                    "skewness of the region's standardised annual rainfall anomaly", "%d to %d" % (min(ch), max(ch)), "DS-02",
                    "Observation only; negative means the dry tail is the long one.")
            da = district_annual()
            pair = [k for k in da if k[0] == region]
            if len(pair) == 2:
                yy = sorted(set(da[pair[0]]) & set(da[pair[1]]))
                r_dd = corr([da[pair[0]][y] for y in yy], [da[pair[1]][y] for y in yy])
                add(region, "collective_climate_idio_share", max(0.0, min(1.0, 1 - r_dd)), "share of climate-factor variance",
                    "1 - corr(%s anomaly, %s anomaly), %d years" % (pair[0][1], pair[1][1], len(yy)), "%d to %d" % (yy[0], yy[-1]), "DS-02",
                    "Share of one district's rainfall year not shared with the other district of the region: the stand-in for how much two collectives in a region differ. The parameter is a shared default; the regional values are averaged into it.", None)
        pp, pw, pn = price_persistence("Arabica_USD_per_t" if sk == "arabica" else "Robusta_USD_per_t")
        add(region, "price_persistence", pp, "AR(1) coefficient",
            "lag-1 autocorrelation of annual mean log %s price around a linear trend, %d years" % (label, pn), pw, "DS-04",
            "Observation for this region's reference series; the shared parameter is applied from the Arabica estimate (see the 'all' row).")
        for li in literature_inputs():
            if li["Region"] != region:
                continue
            add(region, li["Parameter"], float(li["Value"]), li["Unit"],
                "%s (data/rt7-literature-inputs.csv): %s" % (li["ID"], li["Arithmetic"]), li["Reference_Year"], li["Source_Refs"],
                li["Note"], li["Basis"] if li["Apply"] == "yes" else None)

    # Shared (Region "all") parameters: price persistence from the Arabica series, climate from DS-02
    pp, pw, pn = price_persistence("Arabica_USD_per_t")
    add("all", "price_persistence", pp, "AR(1) coefficient",
        "lag-1 autocorrelation of annual mean log Arabica price around a linear trend, %d years" % pn, pw, "DS-04",
        "Season-to-season persistence of the price factor for the multi-season horizon. Arabica is the reference for two of three regions; the Robusta estimate is recorded on the Vietnam row. About 20 annual observations, so the figure is indicative.", "observed")
    chh = climate_history()
    if len(chh) >= 2:
        regs = sorted(chh); pairs = []
        for i in range(len(regs)):
            for j in range(i + 1, len(regs)):
                yy = sorted(set(chh[regs[i]]) & set(chh[regs[j]]))
                pairs.append((regs[i], regs[j], corr([chh[regs[i]][y] for y in yy], [chh[regs[j]][y] for y in yy]), len(yy)))
        add("all", "portfolio_climate_cross_corr", max(0.0, mean([c for _, _, c, _ in pairs])), "correlation",
            "mean pairwise correlation of the regions' annual rainfall anomalies, floored at 0 (%s)" % "; ".join("%s-%s %.2f" % (a, b, c) for a, b, c, _ in pairs),
            "%d years" % min(n for _, _, _, n in pairs), "DS-02",
            "Rainfall anomalies, not yield anomalies: the climate factors' shared component in the portfolio layer. Pairwise values are in the method; a negative mean is floored because the model's construction needs a non-negative shared share.", "observed")
        idio = [r for r in out if r["Parameter"] == "collective_climate_idio_share"]
        if idio:
            add("all", "collective_climate_idio_share", mean([float(r["Observed_Value"]) for r in idio]), "share of climate-factor variance",
                "mean over regions of 1 - corr(district A, district B) annual rainfall anomalies", "see region rows", "DS-02",
                "Shared parameter applied as the regional mean; the region rows above are the observations it rests on.", "observed")
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader(); w.writerows(out)
    print("wrote %s (%d rows)" % (os.path.relpath(OUT, C.ROOT), len(out)))
    for r in out:
        if r["Apply_As"]:
            print("  %-9s %-22s %12s  %s" % (r["Region"], r["Parameter"], r["Observed_Value"], r["Apply_As"]))

    if not apply:
        return
    rows = list(csv.DictReader(open(PARAMS, newline="", encoding="utf-8")))
    fields = list(rows[0].keys())
    by = {(r["Region"], r["Parameter"]): r for r in rows}
    changed = 0
    for c in out:
        if not c["Apply_As"]:
            continue
        key = (c["Region"], c["Parameter"])
        if key not in by:
            print("  ! no region row for %s/%s - the parameter is a shared default; add a region row first" % key)
            continue
        r = by[key]
        v = float(c["Observed_Value"])
        r["Value"] = ("%.4f" % v).rstrip("0").rstrip(".") if v < 100 else "%.0f" % v
        r["Basis"] = c["Apply_As"]
        refs = [s.strip() for s in r["Source_Refs"].split(";") if s.strip()]
        for d in c["Dataset"].split(";"):
            if d.strip() and d.strip() not in refs:
                refs.append(d.strip())
        r["Source_Refs"] = "; ".join(refs)
        r["Note"] = (r["Note"].split(" CALIBRATED ")[0].rstrip(".") + ". CALIBRATED %s from %s: %s (%s). %s"
                     % (stamp[:10], c["Dataset"], c["Method"], c["Window"], c["Note"]))
        changed += 1
    with open(PARAMS, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    print("applied %d values to %s" % (changed, os.path.relpath(PARAMS, C.ROOT)))


if __name__ == "__main__":
    main()
