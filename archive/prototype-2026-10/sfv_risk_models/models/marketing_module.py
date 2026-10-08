"""Collective marketing & forward sales module.

Models revenue sharing between members and the collective, forward contracts,
and shortfall costs when production < contracted volumes.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .loan_book import Member


@dataclass
class MarketingConfig:
    """Configuration for collective marketing."""
    fwd_price_usd_per_t: float  # forward price (USD per tonne green coffee)
    fwd_share: float  # fraction of expected crop sold forward
    basis_local: float  # local basis vs contract/futures (e.g. 0.05 = 5% below)
    penalty_per_ton_short: float  # penalty for non-delivery (USD/tonne)
    collective_margin_rate: float = 0.03  # margin retained by collective on sales


def compute_member_revenues(
    members: list[Member],
    realized_yield_t_ha: float,
    spot_price_usd_per_t: float,
    cfg: MarketingConfig,
) -> dict[str, np.ndarray]:
    """
    Compute farm-gate revenues and collective cash flows for one yield/price realization.

    Parameters
    ----------
    members : list[Member]
        List of members.
    realized_yield_t_ha : float
        Realized district yield (t/ha) for this scenario.
    spot_price_usd_per_t : float
        Local spot price (USD/tonne).
    cfg : MarketingConfig
        Marketing parameters.

    Returns
    -------
    dict
        - revenue_fwd: forward revenue per member (USD)
        - revenue_spot: spot revenue per member (USD)
        - revenue_total: total farm revenue (USD)
        - collective_margin: net margin for the collective (USD)
        - shortfall_cost: cost to cover volume shortfall (USD, >=0)
        - production_t: production tonnes per member
    """
    n = len(members)
    areas = np.array([m.area_ha for m in members])
    hedge_ratios = np.array([m.hedge_ratio for m in members])

    # Production per member (using realized district yield as proxy)
    production_t = areas * realized_yield_t_ha

    # Volume each member commits to collective forward pool
    # We assume: forward volume = hedge_ratio * fwd_share of expected production
    fwd_volume_t = production_t * hedge_ratios * cfg.fwd_share

    # Total forward volume contracted by collective
    total_fwd_t = fwd_volume_t.sum()

    # Forward revenue at contracted price
    revenue_fwd = fwd_volume_t * cfg.fwd_price_usd_per_t

    # Remaining volume sold at spot by farmer (or via collective at spot)
    spot_volume_t = production_t * (1 - hedge_ratios * cfg.fwd_share)
    revenue_spot = spot_volume_t * spot_price_usd_per_t

    revenue_total = revenue_fwd + revenue_spot + np.array([m.other_income_usd for m in members])

    # Collective cash flow:
    # - Receives coffee from members (we assume pass-through pricing at fwd & spot)
    # - Sells at fwd_price and spot_price
    # - Retains a margin on total sales
    total_sales_usd = (fwd_volume_t * cfg.fwd_price_usd_per_t +
                       spot_volume_t * spot_price_usd_per_t)
    collective_margin = total_sales_usd * cfg.collective_margin_rate

    # Shortfall cost: if actual production < expected, collective may need to buy coffee
    # to fulfill forward contracts. For simplicity, we model expected production as
    # base yield * area, and compare to realized.
    # Here we just approximate: if total_fwd_t > some threshold of expected, incur penalty.
    # A more refined version would track expected vs realized separately.
    # For now, set shortfall_cost = 0 in this simple version; can be extended later.
    shortfall_cost = 0.0

    return {
        "revenue_fwd": revenue_fwd,
        "revenue_spot": revenue_spot,
        "revenue_total": revenue_total,
        "collective_margin": collective_margin,
        "shortfall_cost": shortfall_cost,
        "production_t": production_t,
    }
