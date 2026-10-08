"""Regional risk-model pipeline.

End-to-end runner for a single coffee-collective region.
"""

from __future__ import annotations

from pathlib import Path
import yaml
import numpy as np
import pandas as pd

from models.yield_model import simulate_yield_series
from models.price_model import simulate_price_paths
from models.loan_book import generate_collective_members, annual_debt_service
from models.marketing_module import MarketingConfig, compute_member_revenues
from models.credit_risk import compute_pd, compute_lgd, simulate_defaults
from models.securitization import Tranche, compute_tranche_losses


def run_region_pipeline(
    config_path: Path,
    output_dir: Path,
    n_sims: int = 5000,
    seed: int | None = None,
) -> dict:
    """
    Run the full risk pipeline for one region.

    Parameters
    ----------
    config_path : Path
        Path to region YAML config.
    output_dir : Path
        Directory to save outputs (metrics, plots, summaries).
    n_sims : int
        Number of Monte Carlo simulations.
    seed : int | None
        Random seed.

    Returns
    -------
    dict
        Summary results and paths to key output files.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load config
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    region = cfg["region"]

    # -------------------------
    # 1. Generate collective
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
        seed=seed,
    )

    # -------------------------
    # 2. Simulate yield & price
    # -------------------------
    n_years = 1
    yields = simulate_yield_series(
        n_years=n_years,
        base_yield_t_ha=cfg["base_yield_t_ha"],
        yield_vol=cfg["yield_vol"],
        seed=seed,
    )
    prices = simulate_price_paths(
        n_sims=n_sims,
        n_years=n_years,
        base_price=cfg["price_base_usd_per_t"],
        vol=cfg["price_vol"],
        seed=seed,
    )

    yield_scenario = yields[0]
    price_scenarios = prices[:, 0]

    # -------------------------
    # 3. Marketing & revenues
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

    # -------------------------
    # 4. Credit risk
    # -------------------------
    avg_revenue_per_member = revenue_total_matrix.mean(axis=0)

    pds = np.zeros(n_members)
    lgds = np.zeros(n_members)
    eads = np.zeros(n_members)

    for i, m in enumerate(members):
        pds[i] = compute_pd(
            member=m,
            revenue_total=avg_revenue_per_member[i],
            region=region,
            product="portfolio",
            base_pd_capex=cfg["base_pd_capex"],
            base_pd_opex=cfg["base_pd_opex"],
        )
        lgds[i] = compute_lgd(
            member=m,
            region=region,
            lgd_capex=cfg["lgd_capex"],
            lgd_opex=cfg["lgd_opex"],
        )
        ead = 0.0
        if m.capex_loan is not None:
            ead += m.capex_loan
        if m.opex_loan is not None:
            ead += m.opex_loan
        eads[i] = ead

    loan_losses = simulate_defaults(
        members=members,
        pd_array=pds,
        lgd_array=lgds,
        ead_array=eads,
        n_sims=n_sims,
        seed=seed,
    )

    # -------------------------
    # 5. Pool losses & tranches
    # -------------------------
    pool_notional = eads.sum()
    net_collective_cf = collective_margins - shortfall_costs
    collective_loss = np.maximum(0, -net_collective_cf)
    pool_losses = loan_losses + collective_loss

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

    # -------------------------
    # 6. Save outputs
    # -------------------------
    (output_dir / "plots").mkdir(exist_ok=True)

    # Metrics
    portfolio_metrics = {
        "region": region,
        "n_sims": n_sims,
        "pool_notional_usd": pool_notional,
        "el_usd": float(pool_losses.mean()),
        "el_pct": float(pool_losses.mean() / pool_notional),
        "ul_95_usd": float(np.percentile(pool_losses, 95)),
        "ul_95_pct": float(np.percentile(pool_losses, 95) / pool_notional),
        "ul_99_usd": float(np.percentile(pool_losses, 99)),
        "ul_99_pct": float(np.percentile(pool_losses, 99) / pool_notional),
    }

    pd_metrics = {
        "mean_pd": float(pds.mean()),
        "max_pd": float(pds.max()),
        "mean_lgd": float(lgds.mean()),
        "total_ead_usd": float(eads.sum()),
    }

    # Save CSVs
    pd.DataFrame([portfolio_metrics]).to_csv(
        output_dir / "metrics_portfolio.csv", index=False
    )

    tranche_rows = []
    for name, m in tranche_metrics.items():
        row = {"tranche": name}
        row.update(m)
        tranche_rows.append(row)
    pd.DataFrame(tranche_rows).to_csv(
        output_dir / "metrics_tranches.csv", index=False
    )

    pd.DataFrame([pd_metrics]).to_csv(
        output_dir / "metrics_credit.csv", index=False
    )

    # Simple executive summary Markdown
    summary_md = f"""# Executive Summary – {region.capitalize()} Coffee Collective

## Context

- Region: {region}
- Number of farmers: {cfg['n_farmers']}
- Average farm size: {cfg['avg_area_ha']} ha
- Loan mix: {cfg['capex_share']*100:.0f}% CapEx, {cfg['opex_share']*100:.0f}% OpEx
- Hedge ratio (mean): {cfg['hedge_ratio_mean']*100:.0f}%

## Key risk metrics

- Portfolio notional: ${portfolio_metrics['pool_notional_usd']:,.0f}
- Expected loss (EL): ${portfolio_metrics['el_usd']:,.0f} ({portfolio_metrics['el_pct']:.2%})
- Unexpected loss (95th percentile): ${portfolio_metrics['ul_95_usd']:,.0f} ({portfolio_metrics['ul_95_pct']:.2%})
- Unexpected loss (99th percentile): ${portfolio_metrics['ul_99_usd']:,.0f} ({portfolio_metrics['ul_99_pct']:.2%})

## Tranche metrics (illustrative)

| Tranche | Attachment | Detachment | EL (%) | UL95 (USD) |
|---------|------------|------------|--------|------------|
"""

    for name, m in tranche_metrics.items():
        attach = next(t.attachment for t in tranches if t.name == name)
        detach = next(t.detachment for t in tranches if t.name == name)
        summary_md += (
            f"| {name} | {attach:.0%} | {detach:.0%} | "
            f"{m['expected_loss_pct']:.2%} | {m['ul_95_usd']:,.0f} |\n"
        )

    summary_md += f"""
## Sensitivities (to be extended)

- Increase yield volatility or introduce climate shocks.
- Vary hedge ratio and forward share.
- Stress price volatility and forward/spot basis.
- Adjust PD/LGD assumptions.

## Data & assumptions

- All data currently synthetic or based on literature priors.
- See `assumptions_run.yaml` and `data_lineage_run.md` (to be added) for details.

## Interpretation

This is a research prototype. Results are highly sensitive to assumptions and should not be used for real underwriting without further validation, data integration, and legal review.
"""

    (output_dir / "summary_executive.md").write_text(summary_md, encoding="utf-8")

    # Save assumptions snapshot
    assumptions_snapshot = {
        "config_file": str(config_path),
        "config": cfg,
        "n_sims": n_sims,
        "seed": seed,
    }
    import yaml
    with open(output_dir / "assumptions_run.yaml", "w") as f:
        yaml.dump(assumptions_snapshot, f, allow_unicode=True)

    return {
        "region": region,
        "portfolio_metrics": portfolio_metrics,
        "tranche_metrics": tranche_metrics,
        "output_dir": str(output_dir),
    }
