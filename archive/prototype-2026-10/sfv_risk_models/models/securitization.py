"""Securitization & tranche analysis module.

Takes a pool loss distribution and carves into tranches.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class Tranche:
    """A tranche of a securitized pool."""
    name: str
    attachment: float  # e.g. 0.07 (7% of pool notional)
    detachment: float  # e.g. 0.15


def compute_tranche_losses(
    loss_distribution: np.ndarray,
    pool_notional: float,
    tranches: list[Tranche],
) -> dict[str, dict[str, float]]:
    """
    Compute tranche-level loss metrics from a pool loss distribution.

    Parameters
    ----------
    loss_distribution : np.ndarray
        Array of simulated pool losses (USD).
    pool_notional : float
        Total notional of the pool.
    tranches : list[Tranche]
        List of tranches with attachment/detachment points (as fractions of notional).

    Returns
    -------
    dict
        Nested dict: {tranche_name: {metric: value, ...}, ...}
        Metrics: expected_loss, el_pct, ul_95, ul_99, el_tranche_pct.
    """
    if pool_notional <= 0:
        raise ValueError("pool_notional must be positive")

    # Convert absolute losses to fractions of notional
    loss_frac = loss_distribution / pool_notional

    results = {}
    for tr in tranches:
        # Tranche loss fraction for each scenario:
        # L_tranche = min(detachment, max(0, loss_frac - attachment)) / (detachment - attachment)
        denom = tr.detachment - tr.attachment
        if denom <= 0:
            raise ValueError(f"Tranche {tr.name} has non-positive width")

        tranche_loss_frac = np.clip(loss_frac - tr.attachment, 0, denom) / denom
        tranche_loss_usd = tranche_loss_frac * (denom * pool_notional)

        el = float(np.mean(tranche_loss_usd))
        el_pct = float(np.mean(tranche_loss_frac))
        ul_95 = float(np.percentile(tranche_loss_usd, 95))
        ul_99 = float(np.percentile(tranche_loss_usd, 99))

        results[tr.name] = {
            "expected_loss_usd": el,
            "expected_loss_pct": el_pct,
            "ul_95_usd": ul_95,
            "ul_99_usd": ul_99,
        }

    return results
