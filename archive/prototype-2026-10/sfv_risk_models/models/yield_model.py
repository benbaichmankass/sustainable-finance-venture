"""Yield simulation for coffee districts.

Simple stochastic yield model with climate shock overlays.
"""

from __future__ import annotations

import numpy as np


def simulate_yield_series(
    n_years: int,
    base_yield_t_ha: float,
    yield_vol: float,
    climate_shock_factor: float = 0.0,
    seed: int | None = None,
) -> np.ndarray:
    """
    Simulate annual yield (t/ha) with lognormal noise and optional climate shock.

    Parameters
    ----------
    n_years : int
        Number of years to simulate.
    base_yield_t_ha : float
        Long-run average yield (tonnes per hectare).
    yield_vol : float
        Coefficient of variation (std / mean) for yield shocks.
    climate_shock_factor : float
        Multiplicative shock for bad climate years (e.g. -0.2 for 20% downside).
        0.0 = no systematic climate shock.
    seed : int | None
        Random seed.

    Returns
    -------
    np.ndarray
        Array of simulated yields (length n_years).
    """
    rng = np.random.default_rng(seed)
    # Lognormal shocks: mean 1, CV = yield_vol
    sigma = np.sqrt(np.log(1 + yield_vol**2))
    mu = -0.5 * sigma**2
    shocks = rng.lognormal(mean=mu, sigma=sigma, size=n_years)
    yields = base_yield_t_ha * shocks * (1 + climate_shock_factor)
    return yields


def yield_from_climate_index(
    base_yield_t_ha: float,
    rainfall_index: np.ndarray,
    beta_rain: float = 0.5,
    residual_vol: float = 0.1,
    seed: int | None = None,
) -> np.ndarray:
    """
    Generate yields as a function of a rainfall index (e.g. standardized anomaly).

    yield_t = base_yield * (1 + beta_rain * rainfall_index_t + eps_t)

    Parameters
    ----------
    base_yield_t_ha : float
        Long-run average yield.
    rainfall_index : np.ndarray
        Array of standardized rainfall anomalies (mean 0, std ~1).
    beta_rain : float
        Sensitivity of yield to rainfall anomalies.
    residual_vol : float
        Residual yield volatility not explained by rainfall.
    seed : int | None
        Random seed.

    Returns
    -------
    np.ndarray
        Simulated yields (same length as rainfall_index).
    """
    rng = np.random.default_rng(seed)
    eps = rng.normal(0, residual_vol, size=len(rainfall_index))
    yields = base_yield_t_ha * (1 + beta_rain * rainfall_index + eps)
    yields = np.clip(yields, 0, None)
    return yields
