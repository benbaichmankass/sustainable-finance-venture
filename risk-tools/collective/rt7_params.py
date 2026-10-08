#!/usr/bin/env python3
"""RT-7 parameter loading.

The parameters live in data/rt7-parameters.csv - one row per parameter with
its unit, provenance (Basis: assumption / literature / observed), the source it
currently rests on and the source it should eventually come from. Region "all"
holds the shared defaults; a region row overrides it.

The CSV is the record. This module only reads it. Python 3 stdlib.
"""

from __future__ import annotations

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PARAMS_CSV = os.path.join(ROOT, "data", "rt7-parameters.csv")
REGIONS_CSV = os.path.join(ROOT, "data", "rt7-regions.csv")
SCENARIOS_CSV = os.path.join(ROOT, "data", "rt7-scenarios.csv")

BASIS_VOCAB = ("assumption", "literature", "observed")

INTEGER_PARAMS = {"n_members", "capex_tenor_years", "opex_tenor_years"}


def _read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def load_rows(path=PARAMS_CSV):
    return _read(path)


def load_regions(path=REGIONS_CSV):
    return _read(path)


def load_scenarios(path=SCENARIOS_CSV):
    out = []
    for r in _read(path):
        out.append({
            "id": r["ID"],
            "name": r["Scenario"],
            "climate_shift": float(r["Climate_Factor_Shift"] or 0),
            "price_shift": float(r["Price_Shift_Pct"] or 0) / 100.0,
            "description": r["Description"],
            "rationale": r["Rationale"],
            "refs": r["Refs"],
        })
    return out


def region_params(region, rows=None):
    """Merged {parameter: value} for a region, with region rows overriding
    the shared "all" rows. Values are floats except the integer parameters."""
    rows = rows if rows is not None else load_rows()
    merged = {}
    for r in rows:
        if r["Region"] == "all":
            merged[r["Parameter"]] = r["Value"]
    seen = False
    for r in rows:
        if r["Region"] == region:
            merged[r["Parameter"]] = r["Value"]
            seen = True
    if not seen:
        raise KeyError("no parameter rows for region %r" % region)
    out = {}
    for k, v in merged.items():
        out[k] = int(float(v)) if k in INTEGER_PARAMS else float(v)
    return out


def provenance(region, rows=None):
    """Full rows (with provenance columns) for a region, shared rows included,
    region rows winning. Used by the data-source mapping and the run manifest."""
    rows = rows if rows is not None else load_rows()
    by_param = {}
    for r in rows:
        if r["Region"] == "all":
            by_param[r["Parameter"]] = r
    for r in rows:
        if r["Region"] == region:
            by_param[r["Parameter"]] = r
    return list(by_param.values())


REQUIRED = [
    "n_members", "avg_area_ha", "area_sd", "base_yield_t_ha", "yield_vol",
    "member_yield_dispersion", "member_yield_idio_vol", "production_cost_per_ha",
    "household_floor_usd", "other_income_mean", "other_income_sd",
    "capex_share", "opex_share", "avg_capex_size", "avg_opex_size", "loan_size_sigma",
    "capex_rate", "opex_rate", "capex_tenor_years", "opex_tenor_years",
    "hedge_ratio_mean", "hedge_ratio_sd", "fwd_share", "fwd_price_usd_per_t",
    "basis_local", "penalty_per_ton_short", "collective_margin_rate",
    "collective_fixed_cost_usd", "reserve_share_of_margin", "side_sell_threshold",
    "side_sell_elasticity",
    "price_base_usd_per_t", "price_vol", "price_jump_prob", "price_jump_mean",
    "price_jump_sd", "climate_price_correlation",
    "base_pd_capex", "base_pd_opex", "pd_anchor_dscr", "pd_dscr_sensitivity",
    "pd_max", "pd_floor_share", "lgd_capex", "lgd_opex", "residual_correlation",
    "tranche_equity_detach", "tranche_mezz_detach", "senior_el_target_bp",
]


def validate(rows=None):
    """Schema check on the parameter tracker. Returns a list of problems;
    empty means clean. Run by the test suite and by the pipeline before a run."""
    rows = rows if rows is not None else load_rows()
    problems = []
    regions = sorted({r["Region"] for r in rows} - {"all"})
    for r in rows:
        if r["Basis"] not in BASIS_VOCAB:
            problems.append("%s/%s: Basis %r not in %s" % (r["Region"], r["Parameter"], r["Basis"], BASIS_VOCAB))
        try:
            float(r["Value"])
        except ValueError:
            problems.append("%s/%s: Value %r is not numeric" % (r["Region"], r["Parameter"], r["Value"]))
        if not r["Target_Source"].strip():
            problems.append("%s/%s: Target_Source is blank - every parameter must say where it should come from"
                            % (r["Region"], r["Parameter"]))
    for region in regions:
        try:
            p = region_params(region, rows)
        except KeyError as e:
            problems.append(str(e))
            continue
        missing = [k for k in REQUIRED if k not in p]
        if missing:
            problems.append("%s: missing %s" % (region, ", ".join(missing)))
        for k in ("capex_share", "opex_share", "fwd_share", "hedge_ratio_mean", "basis_local",
                  "collective_margin_rate", "reserve_share_of_margin", "base_pd_capex",
                  "base_pd_opex", "pd_max", "pd_floor_share", "lgd_capex", "lgd_opex",
                  "residual_correlation", "tranche_equity_detach", "tranche_mezz_detach"):
            if k in p and not (0.0 <= p[k] <= 1.0):
                problems.append("%s/%s: %s outside [0, 1]" % (region, k, p[k]))
        if "tranche_equity_detach" in p and "tranche_mezz_detach" in p and \
                not (p["tranche_equity_detach"] < p["tranche_mezz_detach"] < 1.0):
            problems.append("%s: tranche detachments must satisfy equity < mezz < 1" % region)
        if "climate_price_correlation" in p and not (-1.0 < p["climate_price_correlation"] < 1.0):
            problems.append("%s: climate_price_correlation outside (-1, 1)" % region)
    return problems


if __name__ == "__main__":
    probs = validate()
    for p in probs:
        print("  !", p)
    print("%d problem(s)" % len(probs))
    raise SystemExit(1 if probs else 0)
