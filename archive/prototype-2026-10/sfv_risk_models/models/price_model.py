"""Coffee price simulation.

Simple AR(1) + jumps model for international coffee prices.
"""

from __future__ import annotations

import numpy as np


def simulate_price_paths(
    n_sims: int,
    n_years: int,
    base_price: float,
    vol: float,
    ar1_phi: float = 0.3,
    jump_prob: float = 0.05,
    jump_mean: float = 0.15,
    jump_sd: float = 0.10,
    seed: int | None = None,
) -> np.ndarray:
    """
    Simulate price paths with AR(1) log-returns and occasional jumps.

    Parameters
    ----------
    n_sims : int
        Number of simulation paths.
    n_years : int
        Number of years per path.
    base_price : float
        Starting price level.
    vol : float
        Annual volatility of log-returns.
    ar1_phi : float
        AR(1) persistence for log-returns.
    jump_prob : float
        Probability of a jump in a given year.
    jump_mean : float
        Mean jump size (as fraction, e.g. 0.15 = +15%).
    jump_sd : float
        Std dev of jump size.
    seed : int | None
        Random seed.

    Returns
    -------
    np.ndarray
        Array of shape (n_sims, n_years) with simulated prices.
    """
    rng = np.random.default_rng(seed)
    sigma = vol / np.sqrt(n_years)  # approximate per-period vol
    # Simulate log-returns
    eps = rng.normal(0, sigma, size=(n_sims, n_years))
    # AR(1) structure on returns
    log_ret = np.zeros_like(eps)
    log_ret[:, 0] = eps[:, 0]
    for t in range(1, n_years):
        log_ret[:, t] = ar1_phi * log_ret[:, t - 1] + eps[:, t]
    # Add jumps
    jump_mask = rng.uniform(size=(n_sims, n_years)) < jump_prob
    jumps = rng.normal(jump_mean, jump_sd, size=(n_sims, n_years))
    log_ret[jump_mask] += jumps[jump_mask]
    # Convert to price levels
    log_prices = np.log(base_price) + np.cumsum(log_ret, axis=1)
    prices = np.exp(log_prices)
    return prices


def local_spot_price(
    intl_price: np.ndarray,
    basis_local: float,
    quality_adj: float = 1.0,
) -> np.ndarray:
    """
    Convert international price to local spot price with basis and quality adjustment.

    Parameters
    ----------
    intl_price : np.ndarray
        International price array (any shape).
    basis_local : float
        Local basis (e.g. 0.05 means local price is 5% below intl).
    quality_adj : float
        Quality adjustment factor (1.0 = parity).

    Returns
    -------
    np.ndarray
        Local spot prices.
    """
    return intl_price * (1 - basis_local) * quality_adj
