"""Synthetic loan book generation for coffee collectives.

Generates heterogeneous smallholder members with CapEx and OpEx loans.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass


@dataclass
class Member:
    """A single smallholder member of a collective."""
    id: int
    area_ha: float
    yield_t_ha: float
    capex_loan: float | None  # outstanding principal
    opex_loan: float | None
    capex_tenor_years: int | None
    opex_tenor_years: int | None
    capex_rate: float | None
    opex_rate: float | None
    hedge_ratio: float  # share of crop marketed collectively
    other_income_usd: float  # non-coffee income


def generate_collective_members(
    n_farmers: int,
    avg_area_ha: float,
    area_sd: float,
    base_yield_t_ha: float,
    yield_vol: float,
    capex_share: float,
    opex_share: float,
    avg_capex_size: float,
    avg_opex_size: float,
    capex_rate: float,
    opex_rate: float,
    capex_tenor_years: int,
    opex_tenor_years: int,
    hedge_ratio_mean: float,
    hedge_ratio_sd: float,
    other_income_mean: float = 0.0,
    other_income_sd: float = 0.0,
    seed: int | None = None,
) -> list[Member]:
    """
    Generate a synthetic collective of smallholder members.

    Parameters
    ----------
    n_farmers : int
        Number of farmers.
    avg_area_ha : float
        Average farm size (ha).
    area_sd : float
        Std dev of farm size.
    base_yield_t_ha : float
        Average yield (t/ha).
    yield_vol : float
        Yield CV across farmers.
    capex_share : float
        Fraction of farmers with CapEx loans.
    opex_share : float
        Fraction of farmers with OpEx loans.
    avg_capex_size : float
        Average CapEx loan size (USD).
    avg_opex_size : float
        Average OpEx loan size (USD).
    capex_rate : float
        Interest rate on CapEx loans.
    opex_rate : float
        Interest rate on OpEx loans.
    capex_tenor_years : int
        CapEx loan tenor (years).
    opex_tenor_years : int
        OpEx loan tenor (years).
    hedge_ratio_mean : float
        Mean fraction of crop marketed collectively.
    hedge_ratio_sd : float
        Std dev of hedge ratio.
    other_income_mean : float
        Mean non-coffee income (USD/year).
    other_income_sd : float
        Std dev of non-coffee income.
    seed : int | None
        Random seed.

    Returns
    -------
    list[Member]
        List of Member objects.
    """
    rng = np.random.default_rng(seed)

    # Farm sizes (lognormal-ish, truncated at 0)
    areas = rng.normal(avg_area_ha, area_sd, size=n_farmers)
    areas = np.clip(areas, 0.2, None)

    # Yields (lognormal around base_yield)
    sigma = np.sqrt(np.log(1 + yield_vol**2))
    mu = np.log(base_yield_t_ha) - 0.5 * sigma**2
    yields = rng.lognormal(mean=mu, sigma=sigma, size=n_farmers)

    # Hedge ratios (beta-like, truncated [0,1])
    hedge_ratios = rng.normal(hedge_ratio_mean, hedge_ratio_sd, size=n_farmers)
    hedge_ratios = np.clip(hedge_ratios, 0.0, 1.0)

    # Other income
    other_incomes = rng.normal(other_income_mean, other_income_sd, size=n_farmers)
    other_incomes = np.clip(other_incomes, 0, None)

    # Loan flags
    has_capex = rng.uniform(size=n_farmers) < capex_share
    has_opex = rng.uniform(size=n_farmers) < opex_share

    # Loan sizes (lognormal around averages)
    capex_sizes = rng.lognormal(
        mean=np.log(avg_capex_size),
        sigma=0.5,
        size=n_farmers,
    )
    opex_sizes = rng.lognormal(
        mean=np.log(avg_opex_size),
        sigma=0.5,
        size=n_farmers,
    )

    members = []
    for i in range(n_farmers):
        capex_loan = float(capex_sizes[i]) if has_capex[i] else None
        opex_loan = float(opex_sizes[i]) if has_opex[i] else None

        members.append(
            Member(
                id=i,
                area_ha=float(areas[i]),
                yield_t_ha=float(yields[i]),
                capex_loan=capex_loan,
                opex_loan=opex_loan,
                capex_tenor_years=capex_tenor_years if has_capex[i] else None,
                opex_tenor_years=opex_tenor_years if has_opex[i] else None,
                capex_rate=capex_rate if has_capex[i] else None,
                opex_rate=opex_rate if has_opex[i] else None,
                hedge_ratio=float(hedge_ratios[i]),
                other_income_usd=float(other_incomes[i]),
            )
        )

    return members


def annual_debt_service(member: Member) -> float:
    """
    Approximate annual debt service for a member (CapEx + OpEx).

    For simplicity:
    - CapEx: level amortization over tenor.
    - OpEx: bullet repayment after 1 year (so full principal + interest in year 1).
    """
    ds = 0.0
    if member.capex_loan is not None and member.capex_tenor_years:
        n = member.capex_tenor_years
        r = member.capex_rate or 0.0
        # Level payment: P * r / (1 - (1+r)**-n)
        if r > 0:
            pmt = member.capex_loan * r / (1 - (1 + r) ** (-n))
        else:
            pmt = member.capex_loan / n
        ds += pmt
    if member.opex_loan is not None and member.opex_tenor_years:
        # Assume 1-year bullet for OpEx
        r = member.opex_rate or 0.0
        ds += member.opex_loan * (1 + r)
    return ds
