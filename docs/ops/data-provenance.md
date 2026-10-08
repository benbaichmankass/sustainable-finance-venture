# Data provenance — where every number comes from

**Status:** v1 · **Last updated:** 2026-10-08 · **Catalogue:** `data/data-catalog.csv` (DS-NN) · **Applies to:** every external or partner dataset that feeds a model, a tracker or a claim in this repo

## Why this exists

RT-7 has 105 parameters and every one of them is currently an assumption. The model is only as useful as the path from each assumption to the observation that should replace it, and that path has to be recorded before the data arrives, not reconstructed afterwards. This document fixes the rules; the catalogue is the record.

It adapts the data-provenance standard that came in with the RT-7 prototype (`archive/prototype-2026-10/data-provenance-standard.md`) to this repo's conventions: the catalogue is a tracker with stable IDs, raw data lives in the Vault, and the Master Reference Tracker Sheet is a mirror.

## The four-tier basis

Every parameter in a model tracker carries a `Basis`:

| Basis | Means | What has to be true |
|---|---|---|
| `assumption` | A number someone chose | The row says why, and names the `Target_Source` that would replace it |
| `literature` | Taken or derived from a source in the literature matrix | `Source_Refs` names the LIT IDs; the matrix row states the figures, and any arithmetic from them is written out in `data/rt7-literature-inputs.csv` |
| `proxy` | Computed from a catalogued dataset about a *similar* population, not the one modelled (a Kiva loan book for the loan-size distribution, a household survey from the same region for farm sizes and incomes) | `Source_Refs` names the `DS-NN` or LIT row; the `Note` says what population it is and why it stands in |
| `observed` | Computed from a catalogued dataset about the thing modelled (the reference price series, the national yield series, the collective's own records when they arrive) | `Source_Refs` names the `DS-NN` row and the processed file; the catalogue row is `Validated` |

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

## The ingestion scripts

`scripts/ingest/` holds one script per dataset plus the shared plumbing in `_common.py`, which enforces the rules above: a raw file is never overwritten (the filename carries the retrieval date), a query log with the request, timestamp and SHA-256 is written beside it, and every processed file gets a dictionary with a provenance block naming the raw hash and the commit.

| Script | Dataset | Route | Processed file |
|---|---|---|---|
| `ds01_faostat_yields.py` | DS-01 FAOSTAT coffee, green | Publisher bulk zip, filtered to the three countries (the query API now needs an authorization header) | `data/processed/ds-01-coffee-national-yields.csv` |
| `ds03_nasa_power.py` | DS-03 NASA POWER monthly | Point API at six district centroids, one raw file of verbatim responses | `data/processed/ds-03-district-climate-monthly.csv` |
| `ds04_pink_sheet.py` | DS-04 World Bank Pink Sheet | XLSX; the doc id changes per release and is read off the landing page | `data/processed/ds-04-coffee-prices-monthly.csv` |
| `ds09_exchange_rates.py` | DS-09 exchange rates | Banco de la Republica TRM daily (Socrata API, averaged to months) and World Bank WDI official rates, annual | `data/processed/ds-09-exchange-rates.csv` |
| `ds10_fnc_colombia.py` | DS-10 FNC coffee statistics | Monthly workbook; the file name carries the month and is read off the statistics page; sheets parsed by header detection | `data/processed/ds-10-colombia-coffee-prices-monthly.csv`, `ds-10-colombia-coffee-area-by-department.csv` |
| `ds11_kiva_loans.py` | DS-11 Kiva loans (proxy) | GraphQL, 3,000 newest Agriculture loans per country with partner metrics; names and towns stay in the raw file | `data/processed/ds-11-kiva-agriculture-loans.csv`, `ds-11-kiva-partners.csv` |
| `calibrate_rt7.py` | all of the above plus `data/rt7-literature-inputs.csv` | Turns the series into observed and proxy RT-7 parameters, applies the literature inputs marked for application, and records observation-only statistics | `data/rt7-calibration.csv`, and with `--apply` the parameter tracker |

**Literature inputs.** A `literature` value that needs arithmetic (a per-household cost over a coffee area, a poverty line times a household size, a currency conversion at a dated rate) gets a row in `data/rt7-literature-inputs.csv`: ID (`LI-NN`), region, parameter, value, unit, basis, the LIT and DS IDs it rests on, the source figures as stated, the arithmetic written out, the reference year, whether it is applied, and a note on what the number is and is not. The source figures must be in the literature matrix row; the arithmetic must be reproducible from the row alone. `calibrate_rt7.py` applies the rows marked `Apply: yes` and carries the rest as observations.

Run order: the fetchers, then `calibrate_rt7.py --apply`, then `risk-tools/collective/run_region.py`, then the dashboard build.

**The query logs are committed; the raw bytes are not.** `data/raw/*/*.query.json` is tracked, everything else under `data/raw/` is gitignored. The log is the record of what was fetched; the bytes are reproducible from it.

**Vault copies of public datasets.** The rule is raw bytes in the Vault, and for partner data that is absolute. For a public, re-fetchable publisher file the query log's URL and SHA-256 already make the extract reproducible, and an agent pushing hundreds of kilobytes through a Drive connector is a poor use of anyone's time. So: the agent uploads a Vault copy when the file is small, records in the query log's `vault_copy` field when it has not, and a human with Drive access drops the larger files into `05-raw-data/<DS-NN>-<slug>/` when convenient. The folders exist for DS-01, DS-03 and DS-04; DS-09 to DS-11 are re-fetchable from their query logs and their raw files are not yet in the Vault.

## What this does not yet do

- DS-02 (CHIRPS) needs a documented district boundary before an extraction means anything; it stays `Proposed`. DS-05 (ICO) and DS-06 (Our World in Data) are cross-checks, not yet pulled.
- No automated checksum verification on re-run: a second fetch on a later date lands as a new raw file and the two hashes are compared by eye.
- The Vault folder `05-raw-data/<DS-NN>-<slug>/` convention is not yet reflected in `docs/ops/drive-vault.md`.
