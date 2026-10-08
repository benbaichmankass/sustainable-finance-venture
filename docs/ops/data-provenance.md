# Data provenance — where every number comes from

**Status:** v1 · **Last updated:** 2026-10-08 · **Catalogue:** `data/data-catalog.csv` (DS-NN) · **Applies to:** every external or partner dataset that feeds a model, a tracker or a claim in this repo

## Why this exists

RT-7 has 105 parameters and every one of them is currently an assumption. The model is only as useful as the path from each assumption to the observation that should replace it, and that path has to be recorded before the data arrives, not reconstructed afterwards. This document fixes the rules; the catalogue is the record.

It adapts the data-provenance standard that came in with the RT-7 prototype (`archive/prototype-2026-10/data-provenance-standard.md`) to this repo's conventions: the catalogue is a tracker with stable IDs, raw data lives in the Vault, and the Master Reference Tracker Sheet is a mirror.

## The three-tier basis

Every parameter in a model tracker carries a `Basis`:

| Basis | Means | What has to be true |
|---|---|---|
| `assumption` | A number someone chose | The row says why, and names the `Target_Source` that would replace it |
| `literature` | Taken or derived from a source in the literature matrix | `Source_Refs` names the LIT IDs; the matrix row states the number |
| `observed` | Computed from a catalogued dataset | `Source_Refs` names the `DS-NN` row and the processed file; the catalogue row is `Validated` |

A literature *reference point* that bears on a value without estimating it (LIT-035's price range next to `price_vol`) stays `assumption` with the LIT ID in `Source_Refs`. Promotion to `literature` requires the source to state the number.

## The catalogue — `data/data-catalog.csv`

One row per dataset, `DS-NN`, never reused. Columns:

| Column | Meaning |
|---|---|
| `ID` | `DS-NN` |
| `Dataset` | Publisher's own name for the product, with the variables in brackets where the name is generic |
| `Domain` | `agri` · `climate` · `price` · `solar` · `credit` · `geography` (semicolon-separated if several) |
| `Regions` | Which pilot regions it covers, or `Global` |
| `Source_Organization` | Publisher |
| `URL` | Landing page or API root. **Verified or absent**, as in every tracker |
| `Access_Method` | API, download, Earth Engine, data-sharing agreement |
| `Variables` | What is retained |
| `Frequency` | Daily, monthly, annual, per loan |
| `Temporal_Coverage` | Start and end as published |
| `License_Or_Terms` | Licence or the words "confidential" |
| `Status` | `Proposed` · `Downloaded` · `Cleaned` · `Validated` · `Deprecated` |
| `Used_By` | Which tool parameters or trackers consume it |
| `Notes` | Caveats, unit conversions, known gaps |

A dataset moves `Proposed → Downloaded` when a raw extract exists in the Vault, `→ Cleaned` when a processed file exists in the repo with its data dictionary, `→ Validated` when the checks below have run and the result is recorded, `→ Deprecated` when a newer extract or publisher version replaces it (the row stays; the replacement gets a new ID).

## Where the bytes live

| Tier | Where | Why |
|---|---|---|
| **Raw extracts** | Vault `05-raw-data/<DS-NN>/`, never edited, filename carries the retrieval date | Large, sometimes licence-restricted, and the thing that must never be silently altered |
| **Query logs** | Beside the raw file in the Vault: the exact URL or request parameters, retrieval timestamp (UTC), publisher version, SHA-256 of the file | Reproducibility without re-downloading |
| **Processed, model-ready files** | `data/processed/<DS-NN>-<slug>.csv` in the repo, small, every field quoted, with a `.md` data dictionary beside it | The repo holds what a model reads |
| **Ingestion code** | `scripts/ingest/<DS-NN>_<slug>.py` | A processed file names the script and the commit that made it |

**Partner data (DS-07, DS-08 and any future member-level dataset) never enters the repo at any tier.** Row-level records stay in the Vault under the data-sharing agreement; only aggregates come back, and only aggregates that cannot identify a member (`CLAUDE.md` §8, `docs/ops/publishing.md`).

## Validation before a dataset is `Validated`

1. **Schema** — columns, types and units match the data dictionary.
2. **Coverage** — the date range and geography are what the catalogue row claims; gaps are listed.
3. **Units** — converted once, explicitly, in the ingestion script, and recorded in the dictionary (coffee prices arrive as USD/kg, US cents/lb and USD/t; the model uses USD/t green).
4. **Checksum** — SHA-256 of the raw and processed files recorded in the query log.
5. **Plausibility** — a one-paragraph note of what the series looks like against what the literature says it should look like (LIT-035 for prices, LIT-031 for the leaf-rust years in Central American yields).

## Lineage, in one line per model parameter

A parameter's lineage is readable from its row in the model tracker without opening anything else: `Basis` says what kind of number it is, `Source_Refs` says what it rests on today, `Target_Source` says what should replace it, `Note` says how it got here. The dashboard renders this as the *Data sources* table on each model tab. If a row cannot be filled in, the parameter is not ready to be in the model.

## What this does not yet do

- No ingestion scripts exist. The eight catalogue rows are all `Proposed`; writing the fetchers for DS-01 to DS-04 is Phase 3 of the RT-7 plan.
- No automated checksum or dictionary tooling. The rules above are followed by hand until there is a second dataset to justify a script.
- The Vault folder `05-raw-data/<DS-NN>/` convention is new and not yet reflected in `docs/ops/drive-vault.md`; update that doc with the first real extract.
