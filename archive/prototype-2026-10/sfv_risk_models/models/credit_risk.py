"""Credit risk module: PD/LGD calculation and loss simulation.

Simple structural-style PD based on DSCR, with region/product priors.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm

from .loan_book import Member, annual_debt_service


def compute_pd(
    member: Member,
    revenue_total: float,
    region: str,
    product: str,
    base_pd_capex: float,
    base_pd_opex: float,
    ds_crash_multiplier: float = 2.5,
    side_sell_penalty: float = 0.0,
) -> float:
    """
    Compute probability of default for a member.

    Simplified approach:
    - Compute DSCR = revenue_total / debt_service.
    - Map DSCR to PD using a logistic-like function calibrated to base_pd.
    - Apply side-sell penalty if spot prices are much higher than forward (not used here directly).

    Parameters
    ----------
    member : Member
        Member data.
    revenue_total : float
        Total farm revenue (USD).
    region : str
        Region identifier (for future extensions).
    product : {"capex", "opex", "portfolio"}
        Which product to assess. For "portfolio", we blend capex/opex base PDs.
    base_pd_capex : float
        Baseline PD for CapEx loans in this region.
    base_pd_opex : float
        Baseline PD for OpEx loans in this region.
    ds_crash_multiplier : float
        How much PD increases when DSCR < 1 (calibration parameter).
    side_sell_penalty : float
        Additional PD increment for high hedge_ratio when spot >> fwd (optional).

    Returns
    -------
    float
        PD in [0,1].
    """
    ds = annual_debt_service(member)
    if ds <= 0:
        # No debt -> PD ~ 0 for credit model purposes
        return 0.0

    dscr = revenue_total / ds

    # Base PD: blend capex/opex by loan presence
    if product == "capex":
        base_pd = base_pd_capex
    elif product == "opex":
        base_pd = base_pd_opex
    else:
        # Portfolio: weighted by debt service composition
        ds_capex = 0.0
        ds_opex = 0.0
        if member.capex_loan is not None and member.capex_tenor_years:
            r = member.capex_rate or 0.0
            n = member.capex_tenor_years
            if r > 0:
                ds_capex = member.capex_loan * r / (1 - (1 + r) ** (-n))
            else:
                ds_capex = member.capex_loan / n
        if member.opex_loan is not None and member.opex_tenor_years:
            r = member.opex_rate or 0.0
            ds_opex = member.opex_loan * (1 + r)
        total_ds = ds_capex + ds_opex
        if total_ds <= 0:
            return 0.0
        w_capex = ds_capex / total_ds
        base_pd = w_capex * base_pd_capex + (1 - w_capex) * base_pd_opex

    # Map DSCR to PD:
    # Use a simple function: PD = base_pd * (1 + k * max(0, 1 - DSCR))
    # where k = ds_crash_multiplier - 1
    if dscr >= 1:
        pd = base_pd * (0.5 + 0.5 * (1 / (1 + (dscr - 1))))  # gentle decline as DSCR rises
    else:
        k = ds_crash_multiplier - 1
        pd = base_pd * (1 + k * (1 - dscr))

    pd = np.clip(pd, 0, 1)
    pd += side_sell_penalty
    pd = np.clip(pd, 0, 1)
    return float(pd)


def compute_lgd(
    member: Member,
    region: str,
    lgd_capex: float,
    lgd_opex: float,
) -> float:
    """
    Compute loss given default for a member.

    Simple version: use region/product LGD priors, optionally adjusted by collateral.
    """
    # For now, just blend by loan presence
    if member.capex_loan is not None and member.opex_loan is not None:
        # Simple average; could be weighted by EAD
        return 0.5 * lgd_capex + 0.5 * lgd_opex
    elif member.capex_loan is not None:
        return lgd_capex
    elif member.opex_loan is not None:
        return lgd_opex
    else:
        return 0.0


def simulate_defaults(
    members: list[Member],
    pd_array: np.ndarray,
    lgd_array: np.ndarray,
    ead_array: np.ndarray,
    n_sims: int,
    seed: int | None = None,
) -> np.ndarray:
    """
    Simulate aggregate loss distributions.

    Parameters
    ----------
    members : list[Member]
        List of members.
    pd_array : np.ndarray
        PD for each member (length n_members).
    lgd_array : np.ndarray
        LGD for each member.
    ead_array : np.ndarray
        Exposure at default for each member.
    n_sims : int
        Number of Monte Carlo simulations.
    seed : int | None
        Random seed.

    Returns
    -------
    np.ndarray
        Array of aggregate losses (USD) for each simulation (length n_sims).
    """
    rng = np.random.default_rng(seed)
    n_members = len(members)
    losses = np.zeros(n_sims)

    for s in range(n_sims):
        defaults = rng.uniform(size=n_members) < pd_array
        loss_s = (defaults * ead_array * lgd_array).sum()
        losses[s] = loss_s

    return losses
