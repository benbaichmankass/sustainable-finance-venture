# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "pandas",
#     "pyyaml",
#     "scipy",
#     "matplotlib",
# ]
# ///

"""
Vietnam Coffee Collective – SFV Risk Model Prototype

This notebook mirrors the Colombia prototype but uses vietnam-specific parameters.
"""

import numpy as np
import pandas as pd
import yaml
import sys
from pathlib import Path

this_file = Path(__file__).resolve()
project_root = this_file.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from models.yield_model import simulate_yield_series
from models.price_model import simulate_price_paths
from models.loan_book import generate_collective_members, annual_debt_service
from models.marketing_module import MarketingConfig, compute_member_revenues
from models.credit_risk import compute_pd, compute_lgd, simulate_defaults
from models.securitization import Tranche, compute_tranche_losses

# -------------------------
# 1. Load configuration
# -------------------------

config_path = project_root / "configs" / "vietnam_params.yaml"
with open(config_path) as f:
    cfg = yaml.safe_load(f)

print("Loaded config for region:", cfg["region"])

# -------------------------
# 2. Generate synthetic collective
# -------------------------

members = generate_collective_members(
    n_farmers=cfg["n_farmers"],
    avg_area_ha=cfg["avg_area_ha"],
    area_sd=cfg["area_sd"],
    base_yield_t_ha=cfg["base_yield_t_ha"],
    yield_vol=cfg["yield_vol"],
    capex_share=cfg["capex_share"],
    opex_share=cfg["opex_share"],
    avg_capex_size=cfg["avg_capex_size"],
    avg_opex_size=cfg["avg_opex_size"],
    capex_rate=cfg["capex_rate"],
    opex_rate=cfg["opex_rate"],
    capex_tenor_years=cfg["capex_tenor_years"],
    opex_tenor_years=cfg["opex_tenor_years"],
    hedge_ratio_mean=cfg["hedge_ratio_mean"],
    hedge_ratio_sd=cfg["hedge_ratio_sd"],
    other_income_mean=cfg["other_income_mean"],
    other_income_sd=cfg["other_income_sd"],
    seed=42,
)

print(f"Generated {len(members)} members.")

# -------------------------
# 3. Simulate yield & price scenarios
# -------------------------

n_sims = 5000
n_years = 1

yields = simulate_yield_series(
    n_years=n_years,
    base_yield_t_ha=cfg["base_yield_t_ha"],
    yield_vol=cfg["yield_vol"],
    seed=123,
)

prices = simulate_price_paths(
    n_sims=n_sims,
    n_years=n_years,
    base_price=cfg["price_base_usd_per_t"],
    vol=cfg["price_vol"],
    seed=124,
)

yield_scenario = yields[0]
price_scenarios = prices[:, 0]

print(f"Yield scenario (t/ha): {yield_scenario:.3f}")
print(f"Price scenarios: mean={price_scenarios.mean():.1f}, sd={price_scenarios.std():.1f}")

# -------------------------
# 4. Marketing & revenue simulation
# -------------------------

mkt_cfg = MarketingConfig(
    fwd_price_usd_per_t=cfg["fwd_price_usd_per_t"],
    fwd_share=cfg["fwd_share"],
    basis_local=cfg["basis_local"],
    penalty_per_ton_short=cfg["penalty_per_ton_short"],
    collective_margin_rate=cfg["collective_margin_rate"],
)

n_members = len(members)
revenue_total_matrix = np.zeros((n_sims, n_members))
collective_margins = np.zeros(n_sims)
shortfall_costs = np.zeros(n_sims)

for s in range(n_sims):
    spot_price = price_scenarios[s]
    res = compute_member_revenues(
        members=members,
        realized_yield_t_ha=yield_scenario,
        spot_price_usd_per_t=spot_price,
        cfg=mkt_cfg,
    )
    revenue_total_matrix[s, :] = res["revenue_total"]
    collective_margins[s] = res["collective_margin"]
    shortfall_costs[s] = res["shortfall_cost"]

print("Revenue simulation complete.")
print("Collective margin: mean={:.1f}, sd={:.1f}".format(
    collective_margins.mean(), collective_margins.std()
))

# -------------------------
# 5. Credit risk: PD, LGD, EAD, loss simulation
# -------------------------

avg_revenue_per_member = revenue_total_matrix.mean(axis=0)

pds = np.zeros(n_members)
lgds = np.zeros(n_members)
eads = np.zeros(n_members)

for i, m in enumerate(members):
    pds[i] = compute_pd(
        member=m,
        revenue_total=avg_revenue_per_member[i],
        region=cfg["region"],
        product="portfolio",
        base_pd_capex=cfg["base_pd_capex"],
        base_pd_opex=cfg["base_pd_opex"],
    )
    lgds[i] = compute_lgd(
        member=m,
        region=cfg["region"],
        lgd_capex=cfg["lgd_capex"],
        lgd_opex=cfg["lgd_opex"],
    )
    ead = 0.0
    if m.capex_loan is not None:
        ead += m.capex_loan
    if m.opex_loan is not None:
        ead += m.opex_loan
    eads[i] = ead

print(f"PD: mean={pds.mean():.4f}, max={pds.max():.4f}")
print(f"LGD: mean={lgds.mean():.3f}")
print(f"EAD: total={eads.sum():.0f}, mean={eads.mean():.0f}")

loan_losses = simulate_defaults(
    members=members,
    pd_array=pds,
    lgd_array=lgds,
    ead_array=eads,
    n_sims=n_sims,
    seed=125,
)

print(f"Loan losses: mean={loan_losses.mean():.0f}, 95th={np.percentile(loan_losses, 95):.0f}")

# -------------------------
# 6. Combine loan losses + collective cash flow risk
# -------------------------

pool_notional = eads.sum()
net_collective_cf = collective_margins - shortfall_costs
collective_loss = np.maximum(0, -net_collective_cf)
pool_losses = loan_losses + collective_loss

print(f"Pool losses: mean={pool_losses.mean():.0f}, 95th={np.percentile(pool_losses, 95):.0f}")

# -------------------------
# 7. Tranche analysis
# -------------------------

tranches = [
    Tranche("equity", 0.0, 0.07),
    Tranche("mezz", 0.07, 0.15),
    Tranche("senior", 0.15, 1.0),
]

tranche_metrics = compute_tranche_losses(
    loss_distribution=pool_losses,
    pool_notional=pool_notional,
    tranches=tranches,
)

print("\nTranche metrics (as % of tranche notional):")
for name, metrics in tranche_metrics.items():
    print(f"{name}: EL={metrics['expected_loss_pct']:.2%}, UL95={metrics['ul_95_usd']:.0f} USD")
