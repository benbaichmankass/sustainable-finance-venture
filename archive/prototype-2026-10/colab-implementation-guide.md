# Colab Implementation and Deliverables Guide

## Objective

Move the SFV coffee-collective risk models from local notebooks to reproducible Colab workflows that produce decision-ready outputs for each pilot region.

---

## 1. Model structure for easy Colab transfer

Keep the **models** package environment-agnostic:

- No hard-coded absolute paths.
- Use relative imports from `models/`.
- Configuration via YAML/JSON.
- All I/O paths passed as arguments or read from environment variables.

Recommended structure:

```text
sfv_risk_models/
├─ models/                 # Pure Python, no environment-specific code
│  ├─ yield_model.py
│  ├─ price_model.py
│  ├─ loan_book.py
│  ├─ marketing_module.py
│  ├─ credit_risk.py
│  └─ securitization.py
├─ configs/                # Region YAML files
├─ src/
│  ├─ data_ingestion/     # Data fetchers and catalog updater
│  └─ pipelines/          # End-to-end pipeline scripts
├─ notebooks/              # Local dev notebooks
├─ colab/                  # Colab-focused notebooks
│  ├─ 00_setup_and_data.ipynb
│  ├─ 01_run_colombia.ipynb
│  ├─ 01_run_ethiopia.ipynb
│  ├─ 01_run_vietnam.ipynb
│  └─ 02_compare_regions.ipynb
└─ outputs/
   ├─ colombia/
   ├─ ethiopia/
   └─ vietnam/
```

Key principles:

- **`models/`**: pure functions and classes; no file I/O except what is explicitly passed in.
- **`src/pipelines/`**: scripts that wire models, data, and outputs together.
- **`colab/`**: thin notebooks that:
  - Mount Google Drive or set up the working directory.
  - Install dependencies.
  - Call pipeline functions.
  - Save outputs to `outputs/`.

---

## 2. Colab notebook pattern

Each regional Colab notebook should follow this pattern:

### 2.1 Setup cell

```python
# Mount Drive (optional)
from google.colab import drive
drive.mount("/content/drive")

# Install dependencies
!pip install numpy pandas pyyaml scipy matplotlib

# Clone or upload the repo
# Option A: clone from GitHub
!git clone https://github.com/benbaichmankass/sustainable-finance-venture.git
%cd sustainable-finance-venture/sfv_risk_models

# Option B: upload zip and unzip in /content

import sys
from pathlib import Path
project_root = Path.cwd()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
```

### 2.2 Configuration cell

```python
REGION = "colombia"  # or "ethiopia", "vietnam"
CONFIG_PATH = project_root / "configs" / f"{REGION}_params.yaml"
OUTPUT_DIR = project_root / "outputs" / REGION
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

### 2.3 Data-loading cell

- Check for processed data in `data/processed/{region}/`.
- If missing, run ingestion scripts from `src/data_ingestion/`.
- Log dataset IDs from `data/data_catalog.csv`.

### 2.4 Model-run cell

Call a pipeline function, e.g.:

```python
from src.pipelines.run_region import run_region_pipeline

results = run_region_pipeline(
    config_path=CONFIG_PATH,
    output_dir=OUTPUT_DIR,
    n_sims=5000,
    seed=42,
)
```

### 2.5 Outputs cell

Save:

- Summary metrics (EL, UL, tranche metrics) as CSV/JSON.
- Key plots (loss distribution, tranche EL, sensitivity charts).
- A short Markdown/HTML summary for stakeholders.

---

## 3. From models to decision-ready deliverables

Design outputs around concrete decisions.

### 3.1 Core decision questions

For each collective and region:

1. **Feasibility:** Is the expected loss and capital requirement within acceptable bounds?
2. **Structure:** What hedge ratio, forward share, and tranche structure are acceptable?
3. **Pricing:** What premium/interest margin is needed to hit target risk-adjusted returns?
4. **Risk management:** Which stresses (drought, price crash, side-selling) drive tail losses?
5. **Data gaps:** Which assumptions most affect outcomes, and what data would reduce uncertainty?

### 3.2 Standard outputs per run

For each region, produce:

1. **Executive summary (1 page)**  
   - Context (region, collective size, loan mix).  
   - Key metrics: portfolio EL/UL, tranche EL, approximate cost of risk.  
   - Main sensitivities (hedge ratio, yield shock, price shock).  
   - Go / no-go or “proceed with conditions” recommendation.

2. **Metrics tables**  
   - Portfolio-level: EAD, EL, UL95, UL99.  
   - Tranche-level: attachment/detachment, EL%, UL95, approximate yield needed.  
   - Sensitivity tables: how EL/UL change with key parameters.

3. **Charts**  
   - Loss distribution histogram with EL and UL markers.  
   - Tranche EL bar chart.  
   - Tornado chart of parameter sensitivities.  
   - (Optional) time-series of yields/prices with stress scenarios highlighted.

4. **Assumption register**  
   - YAML or JSON file capturing all key assumptions (PD/LGD, hedge ratios, forward prices, correlation).  
   - Clear separation between data-driven and expert-judgment inputs.

5. **Data lineage report**  
   - List of dataset IDs used (from `data_catalog.csv`).  
   - Retrieval dates and code versions.  
   - Known limitations.

### 3.3 Example deliverable set (per region)

In `outputs/{region}/`:

```text
outputs/colombia/
├─ summary_executive.md
├─ metrics_portfolio.csv
├─ metrics_tranches.csv
├─ sensitivity_analysis.csv
├─ plots/
│  ├─ loss_distribution.png
│  ├─ tranche_el.png
│  └─ tornado_sensitivity.png
├─ assumptions_run_20261007.yaml
└─ data_lineage_run_20261007.md
```

---

## 4. Pipeline design

Create a reusable pipeline function in `src/pipelines/run_region.py`:

```python
def run_region_pipeline(
    config_path: Path,
    output_dir: Path,
    n_sims: int = 5000,
    seed: int | None = None,
) -> dict:
    ...
```

Responsibilities:

1. Load config and data.
2. Generate or load the synthetic collective.
3. Run yield/price simulations.
4. Run marketing and credit-risk modules.
5. Compute tranche metrics.
6. Run sensitivity analyses.
7. Save all outputs and a run manifest.

This keeps Colab notebooks thin and portable.

---

## 5. Colab-specific considerations

- **Reproducibility:**  
  - Pin dependency versions in a `requirements-colab.txt`.  
  - Record Git commit hash and config hashes in each run manifest.

- **Storage:**  
  - Use Google Drive for persistent storage of `outputs/` and `data/processed/`.  
  - Keep `data/raw/` either in Drive or re-downloadable via scripts.

- **Collaboration:**  
  - Share Colab notebooks with partners; they can re-run with updated configs.  
  - Export final outputs as PDFs/Markdown for non-technical stakeholders.

- **Security:**  
  - Do not store sensitive member-level data in Colab unless properly anonymized and access-controlled.  
  - Keep synthetic data as the default for shared notebooks.

---

## 6. Next implementation steps

1. Create `src/pipelines/run_region.py` with a minimal end-to-end flow.
2. Create `colab/00_setup_and_data.ipynb` as a shared setup notebook.
3. Create `colab/01_run_colombia.ipynb` as the first regional Colab.
4. Define output templates:
   - `summary_executive.md` template.
   - CSV schemas for metrics and sensitivities.
5. Wire the data catalog so each run logs which datasets were used.
