# Data Provenance and Catalog Standard

## Purpose

This document defines how SFV records, versions, and governs all external and internal data used in the coffee-collective risk models. Every file that enters `data/` must be traceable to its source, retrieval time, query parameters, transformations, and code version.

---

## Scope

Applies to:

- **External data:** FAOSTAT/OWID coffee statistics, CHIRPS rainfall, NASA POWER meteorology/solar, World Bank and ICO coffee prices, administrative boundaries, and national statistics.
- **Internal data:** synthetic loan books, assumption registries, processed features, and scenario outputs.
- **All environments:** local development, Colab, and any future production pipelines.

---

## Directory layout

```text
sfv_risk_models/
├─ data/
│  ├─ DATA_CATALOG.md
│  ├─ data_catalog.csv
│  ├─ raw/
│  │  ├─ colombia_huila/
│  │  ├─ ethiopia_jimma/
│  │  └─ vietnam_dak_lak/
│  ├─ interim/
│  ├─ processed/
│  └─ boundaries/
├─ src/
│  └─ data_ingestion/
│     ├─ fetch_chirps.py
│     ├─ fetch_nasa_power.py
│     ├─ fetch_faostat.py
│     ├─ fetch_prices.py
│     └─ update_catalog.py
└─ docs/
   └─ DATA_PROVENANCE_STANDARD.md
```

- `raw/`: immutable, never edited manually.
- `interim/`: temporary joins and reshapes.
- `processed/`: model-ready datasets with documented transformations.
- `boundaries/`: versioned administrative or catchment polygons.

---

## Catalog schema

Maintain a machine-readable CSV (`data/data_catalog.csv`) and a human-readable Markdown (`data/DATA_CATALOG.md`).

Required columns:

| Column | Description |
|---|---|
| `dataset_id` | Stable internal identifier (e.g. `chirps_v3_huila_monthly_20261007`) |
| `dataset_name` | Human-readable source/product name |
| `domain` | `agri`, `climate`, `price`, `solar`, `credit`, `geography` |
| `region` | `Colombia-Huila`, `Ethiopia-Jimma`, `Vietnam-Dak Lak` |
| `source_organization` | FAO, CHC/UCSB, NASA, World Bank, ICO, etc. |
| `source_url` | Landing page or API endpoint |
| `access_method` | API, CSV download, manual download, Earth Engine |
| `query_parameters` | Coordinates, date range, variables, filters, units |
| `raw_file` | Exact local raw-file path |
| `retrieved_at_utc` | ISO timestamp (e.g. `2026-10-07T08:55:00Z`) |
| `source_last_updated` | Date/version reported by the publisher (if available) |
| `temporal_coverage` | e.g. `1981-01 to 2026-09` |
| `spatial_coverage` | Point, polygon, district, country; include coordinates/boundary version |
| `frequency` | Daily, monthly, annual |
| `variables` | Variables retained in the raw extract |
| `raw_units` | Original publisher units |
| `output_file` | Cleaned/model-ready file path |
| `transformations` | Resampling, unit conversions, imputation, lagging |
| `license_or_terms` | License, attribution, redistribution constraints |
| `checksum_sha256` | File-integrity hash |
| `code_version` | Git commit hash or release tag of ingestion script |
| `status` | Proposed, downloaded, cleaned, validated, deprecated |
| `notes` | Caveats, known gaps, calibration usage |

---

## Collection rules

1. **Never overwrite raw files.** Add a retrieval date/version to filenames.
2. **Save the exact API response or downloaded original** before any cleaning.
3. **Log query payloads.** For an API, save URL parameters or a JSON request beside the returned file.
4. **Hash raw and processed outputs** with SHA-256.
5. **Version transformations in Git.** Each processed file should reference its ingestion script and Git commit.
6. **Store data dictionaries.** For every processed CSV/Parquet file, add a matching Markdown or YAML file that explains columns, units, aggregation, and missing-value codes.
7. **Use UTC for retrieval timestamps** and ISO 8601 dates.
8. **Record unit conversions explicitly.** Coffee prices may be USD/kg, USD/lb, USD/tonne, local currency/kg, or farm-gate vs export values.
9. **Keep model assumptions distinct from external data.** YAML parameters such as baseline PD, collateral recovery, and delivery-default probabilities must be tagged `assumption`, not `observed_data`.

---

## Data lineage

```text
Raw source extract
    ↓
Validation: schema, date range, units, missingness, checksum
    ↓
Standardization: dates, geography, units, crop/price definitions
    ↓
Feature creation: seasonal rainfall, yield anomaly, price volatility,
                  forward/spot basis, solar generation
    ↓
Region-specific model inputs
    ↓
Scenario simulations and risk outputs
```

---

## Initial catalog priorities

For each pilot region (Huila, Jimma, Dak Lak), start with:

1. FAOSTAT/OWID coffee production, area, and yield.
2. CHIRPS v3 rainfall.
3. NASA POWER daily weather and solar variables.
4. World Bank Pink Sheet Arabica or Robusta monthly prices.
5. A documented administrative/catchment boundary.
6. A project-assumptions registry for synthetic loan-book and PD/LGD inputs.

Use **Arabica** for Huila and Jimma, and **Robusta** for Dak Lak. World Bank price data distinguish Arabica and Robusta series; the ICO also provides coffee-specific indicator-price data.

---

## Governance

- The catalog is the operational source of truth. The Markdown file should be updated alongside it.
- Any change to a processed dataset requires updating `data_catalog.csv`, including a new `code_version` and `retrieved_at_utc`.
- Private or sensitive data (e.g., cooperative member-level records) must be stored separately with explicit access controls and consent documentation.
