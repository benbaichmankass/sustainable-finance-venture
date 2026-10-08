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
