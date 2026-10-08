# SFV Risk Models – Coffee Collective Prototypes

This package contains prototype risk models for SFV’s pilot coffee collectives in:

- Colombia (LATAM)
- Ethiopia (Africa)
- Vietnam (SE Asia)

Each region has:

- A parameter file (`configs/<region>_params.yaml`)
- A standalone notebook (`notebooks/<region>_coffee_collective.py`)
- Shared model code in `models/`

## Directory structure

```text
sfv_risk_models/
├─ README.md
├─ models/
│  ├─ __init__.py
│  ├─ yield_model.py
│  ├─ price_model.py
│  ├─ loan_book.py
│  ├─ marketing_module.py
│  ├─ credit_risk.py
│  └─ securitization.py
├─ configs/
│  ├─ colombia_params.yaml
│  ├─ ethiopia_params.yaml
│  └─ vietnam_params.yaml
├─ notebooks/
│  ├─ colombia_coffee_collective.py
│  ├─ ethiopia_coffee_collective.py
│  └─ vietnam_coffee_collective.py
└─ data/
   ├─ climate/
   ├─ agri/
   ├─ prices/
   └─ solar/
```

## How to run a notebook

From the `notebooks/` directory (with Python ≥3.10 and dependencies installed):

```bash
cd notebooks
python colombia_coffee_collective.py
```

Dependencies (install in your environment):

```bash
pip install numpy pandas pyyaml scipy matplotlib
```

## What each notebook does

For its region, each notebook:

1. Loads region-specific parameters (farm sizes, yields, loan terms, hedge ratios, etc.).
2. Generates a synthetic collective of ~100 smallholder coffee farmers.
3. Simulates yield and price scenarios.
4. Computes member revenues under a collective marketing model:
   - A share of expected crop sold forward at a fixed price.
   - Remainder sold at spot.
   - Collective retains a small margin on sales.
5. Calculates PD/LGD for each member and simulates loan losses.
6. Combines loan losses with collective cash-flow risk.
7. Runs a simple tranche analysis (equity/mezz/senior) on the pooled loss distribution.
8. Performs a sensitivity analysis on the hedge ratio (share of crop marketed collectively).

## Extending the models

Next steps (in priority order):

1. **Add real data**:
   - District-level coffee yields (FAOSTAT, national stats).
   - Rainfall/temperature series (CHIRPS, NASA POWER).
   - Coffee price histories (ICO, FAO, USDA).
   - Solar irradiance for CapEx assets (PVGIS, NASA POWER).

2. **Refine credit risk**:
   - Add climate shock factors to PD (drought/flood scenarios).
   - Incorporate side-selling incentives when spot >> forward price.
   - Calibrate PD/LGD to observed smallholder/cooperative data.

3. **Enhance marketing module**:
   - Add volume shortfall logic (production < forward commitments).
   - Support minimum-price guarantees + upside participation.
   - Integrate warehouse receipt financing (inventory credit).

4. **Portfolio-level model**:
   - Combine many collectives across regions.
   - Model correlation (climate within region, global price across regions).
   - Re-run tranche analysis on the multi-region pool.

## Integration with SFV repo

Move this `sfv_risk_models/` folder into your main `sustainable-finance-venture` repo, e.g.:

```text
sustainable-finance-venture/
├─ sfv_risk_models/
├─ docs/
├─ literature/
└─ ...
```

Update the master tracker (Google Sheet) with:

- Links to these notebooks.
- Key outputs (EL/UL, tranche metrics) per region.
- Open questions & calibration notes.

## Notes

- All data currently synthetic; replace with open-source data as available.
- Models are intentionally simple for prototyping; complexity can be added iteratively.
- Price units: USD per tonne (green coffee). Adjust configs if you prefer USD/lb.
