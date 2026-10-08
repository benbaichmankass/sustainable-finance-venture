# SFV Coffee Collective Risk Models: User Guide

## Purpose

This prototype models a single coffee-grower collective as a standalone financing project. It combines:

- **Member lending:** CapEx loans for productive assets and OpEx loans for seasonal working capital.
- **Collective marketing:** A portion of coffee production is marketed collectively through a simple forward-price and spot-price split.
- **Credit risk:** Member-level probability of default (PD), loss given default (LGD), and exposure at default (EAD).
- **Pool risk:** Monte Carlo simulation of collective loan losses.
- **Illustrative structuring:** Equity, mezzanine, and senior loss tranches.

There are three independent regional prototypes:

- Colombia (LATAM)
- Ethiopia (Africa)
- Vietnam (SE Asia)

Run and validate each one separately before combining them into a multi-collective or multi-country portfolio.

---

## Package layout

```text
sfv_risk_models/
├─ README.md
├─ configs/
│  ├─ colombia_params.yaml
│  ├─ ethiopia_params.yaml
│  └─ vietnam_params.yaml
├─ data/
│  ├─ agri/
│  ├─ climate/
│  ├─ prices/
│  └─ solar/
├─ models/
│  ├─ yield_model.py
│  ├─ price_model.py
│  ├─ loan_book.py
│  ├─ marketing_module.py
│  ├─ credit_risk.py
│  └─ securitization.py
└─ notebooks/
   ├─ colombia_coffee_collective.py
   ├─ ethiopia_coffee_collective.py
   └─ vietnam_coffee_collective.py
```

---

## Requirements

Use Python 3.10 or later. Create an isolated environment if possible.

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install numpy pandas pyyaml scipy matplotlib
```

---

## Running a regional model

From the root of the `sfv_risk_models` directory, run a region script as a module or run it from its folder.

### Recommended approach

```bash
cd sfv_risk_models/notebooks
python colombia_coffee_collective.py
```

Replace `colombia` with `ethiopia` or `vietnam` to run the other regional prototypes.

Expected output includes:

- The loaded region configuration
- Number of synthetic members created
- Simulated yield and price summary statistics
- Collective marketing-margin summary
- Average and maximum member PD
- Aggregate EAD and LGD summary
- Expected and 95th-percentile loan loss
- Equity, mezzanine, and senior tranche loss metrics
- For Colombia, a hedge-ratio sensitivity table

---

## Workflow inside each model

Each regional script executes the following sequence.

### 1. Load the regional configuration

The script reads `configs/<region>_params.yaml`. The configuration controls all region-specific assumptions, including farm size, yield, loan characteristics, price assumptions, marketing structure, and initial PD/LGD assumptions.

### 2. Generate a synthetic collective

`models/loan_book.py` creates a heterogeneous group of farmers. Each member may receive:

- A **CapEx loan**, such as for solar equipment, irrigation, processing, drying, storage, or other productive assets.
- An **OpEx loan**, such as for fertilizer, labor, seedlings, transport, inventory, or seasonal working capital.

Farm area, yield, loan amounts, non-coffee income, and collective-marketing participation vary across members.

### 3. Simulate yield and coffee prices

- `models/yield_model.py` produces coffee yield scenarios in tonnes per hectare.
- `models/price_model.py` produces stochastic coffee-price scenarios in USD per tonne.

The present prototype is deliberately simple. Its parameters should be replaced or calibrated using open-source historical data before using results for any real underwriting decision.

### 4. Model collective marketing

`models/marketing_module.py` divides a member's coffee output between:

- A forward-marketed portion at the configured forward price.
- A remaining portion sold at a simulated spot price.

The collective retains a configurable marketing margin. This module is intended to represent the initial version of a collective sales platform, not a legally complete futures, warehouse receipt, or commodity-trading system.

### 5. Calculate member credit risk

`models/credit_risk.py` calculates:

- **PD:** based on regional product priors and debt-service coverage.
- **LGD:** based initially on CapEx and OpEx assumptions.
- **EAD:** based on the outstanding CapEx and OpEx principal balances.

The model then runs Monte Carlo default simulations to create a distribution of total loan losses for the collective.

### 6. Analyse illustrative tranches

`models/securitization.py` applies a basic loss waterfall to the simulated pool:

| Tranche | Attachment | Detachment | Intended role |
|---|---:|---:|---|
| Equity | 0% | 7% | First-loss/risk-retention layer |
| Mezzanine | 7% | 15% | Intermediate loss-bearing layer |
| Senior | 15% | 100% | Residual senior claim |

These attachment/detachment points are **illustrative only**. They are not a proposed investment product, rating outcome, or legally executable security.

---

## Editing assumptions

Edit only the relevant YAML configuration file at first. This keeps the shared model logic consistent across countries.

For example, edit:

```text
configs/colombia_params.yaml
```

Key fields are below.

### Collective composition

```yaml
n_farmers: 100
avg_area_ha: 2.0
area_sd: 0.8
base_yield_t_ha: 1.0
yield_vol: 0.15
```

- `n_farmers`: number of members in the synthetic collective.
- `avg_area_ha`, `area_sd`: average and dispersion of farm size.
- `base_yield_t_ha`: long-run yield assumption.
- `yield_vol`: coefficient of variation for production shocks.

### Loan mix and terms

```yaml
capex_share: 0.4
opex_share: 0.9
avg_capex_size: 2500
avg_opex_size: 800
capex_rate: 0.12
opex_rate: 0.15
capex_tenor_years: 5
opex_tenor_years: 1
```

- `capex_share`, `opex_share`: shares of members receiving each product.
- `avg_capex_size`, `avg_opex_size`: average loan sizes in USD.
- Rates are annual decimal rates: `0.12` means 12%.
- The CapEx product is amortizing; the OpEx product is currently modelled as a one-year bullet loan.

### Collective marketing

```yaml
hedge_ratio_mean: 0.5
hedge_ratio_sd: 0.15
price_base_usd_per_t: 4000
price_vol: 0.25
fwd_price_usd_per_t: 3900
fwd_share: 0.5
basis_local: 0.05
collective_margin_rate: 0.03
```

- `hedge_ratio_mean`: average member share of crop participating in collective marketing.
- `fwd_share`: share of the participating crop treated as forward sold.
- `price_base_usd_per_t`: initial coffee-price level.
- `price_vol`: annualized stylized price volatility.
- `fwd_price_usd_per_t`: agreed forward price.
- `basis_local`: local discount from the reference market price.
- `collective_margin_rate`: share of sales retained by the collective for aggregation/marketing services.

### Credit assumptions

```yaml
base_pd_capex: 0.03
base_pd_opex: 0.06
lgd_capex: 0.30
lgd_opex: 0.50
```

- PDs are one-period default priors and should be calibrated later from actual collective, MFI, cooperative, or lender data.
- CapEx LGD should eventually depend on collateral type, depreciation, repossession cost, legal enforceability, and secondary-market value.
- OpEx LGD should eventually depend on social fund coverage, repayment enforcement, receivables, crop liens, and recovery processes.

---

## Suggested first experiments

Change one assumption at a time and save the run output with the configuration version/date.

1. **Hedge participation:** Test `hedge_ratio_mean` at 0.20, 0.40, 0.60, and 0.80.
2. **Forward commitment:** Test `fwd_share` from 0.25 to 0.75.
3. **Climate stress:** Increase `yield_vol`, or use a negative `climate_shock_factor` in the yield module.
4. **Price stress:** Increase `price_vol`; test a forward price materially below spot expectations.
5. **Loan stress:** Increase OpEx loan sizes or decrease farm yields to identify debt-service thresholds.
6. **Collateral:** Reduce/increase `lgd_capex` to represent weaker/stronger asset resale and recovery conditions.
7. **Collective strength:** Vary the collective margin and, in later versions, model group recovery and side-selling explicitly.

A useful starting stress case is: a 25% yield decline, 25% price decline, higher OpEx defaults, and lower CapEx collateral recoveries.

---

## What to add next

### Priority 1: Replace synthetic drivers with open data

Add raw data under `data/` and create an ingestion/cleaning notebook or script for each region.

- `data/agri/`: FAOSTAT, national statistics, regional coffee yield/area data
- `data/climate/`: CHIRPS rainfall, NASA POWER temperature/solar variables, drought indicators
- `data/prices/`: ICO, FAO, World Bank, or exchange-linked coffee price series
- `data/solar/`: PVGIS or NASA POWER irradiance for solar CapEx asset cases

### Priority 2: Correct key prototype limitations

Before interpreting structured-finance results, add:

- Scenario-specific yield rather than one shared yield draw.
- Correlated member defaults driven by common climate, price, and local-economy factors.
- Actual expected-versus-realized production tracking.
- Forward-delivery shortfall cost when actual coffee supply is below the contracted volume.
- Side-selling/delivery-default behaviour when spot price materially exceeds the forward price.
- FX mismatch between export revenues and local-currency debt/costs.
- Buyer/exporter counterparty risk and payment delays.
- Separate asset-level cash-flow and collateral models for solar, irrigation, dryers, pulpers, and processing equipment.

### Priority 3: Build the portfolio model

Only after each regional model is reviewed and calibrated:

1. Create a reusable `CollectiveResult` output object/data schema.
2. Simulate many collectives per country rather than one example group.
3. Model global coffee-price correlation and partially independent regional climate factors.
4. Aggregate all collective loss distributions.
5. Re-run the capital structure and tranche analysis at portfolio level.

---

## Interpretation and governance

This is a research prototype, not a credit-decision engine. Its results are highly sensitive to assumptions and synthetic-data generation.

Before any real lending, insurance, hedging, or securitization deployment, establish:

- Data provenance and versioning
- Borrower and group-consent/privacy controls
- Model documentation and validation
- Independent review of PD/LGD, correlation, and stress assumptions
- Legal review of collateral, collective sale commitments, warehouse receipts, derivatives, FX, and securities regulation
- Clear risk-retention, reserve-account, servicing, and investor-disclosure arrangements

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'models'`

Run the script from inside `sfv_risk_models/notebooks/`:

```bash
cd sfv_risk_models/notebooks
python colombia_coffee_collective.py
```

Alternatively, install the package or set `PYTHONPATH` to the `sfv_risk_models` directory.

### YAML configuration errors

Check indentation and use spaces—not tabs. Numeric rates should be decimals, such as `0.12`, not `12`.

### Results change between runs

Random seeds are included to make the baseline prototype reproducible. If you change seed values or remove them, simulations will differ. For production research, record the random seed, configuration version, code commit, and input-data version for every run.

### Price-unit mismatch

All current config files use **USD per tonne of green coffee**. Do not mix this with USD per pound without conversion. One metric tonne equals approximately 2,204.62 pounds.
