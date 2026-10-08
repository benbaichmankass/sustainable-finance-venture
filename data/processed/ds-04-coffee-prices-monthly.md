# DS-04 — coffee prices, monthly (World Bank Pink Sheet)

One row per month, 1960-01 to 2026-09 (801 rows, 0 with a missing value). Nominal US dollars per metric tonne of green coffee, converted from the publisher's USD/kg by multiplying by 1,000. Publisher note on this file: "Updated on October 02, 2026".

| Column | Meaning | Unit |
|---|---|---|
| `Month` | Calendar month | `YYYY-MM` |
| `Arabica_USD_per_t` | Pink Sheet series *Coffee, Arabica* (ICO indicator price, other mild arabicas, New York and Bremen/Hamburg markets, ex-dock) | USD / t, nominal |
| `Robusta_USD_per_t` | Pink Sheet series *Coffee, Robusta* (ICO indicator price, New York and Le Havre/Marseilles, ex-dock) | USD / t, nominal |

**What it is.** World reference prices, not farm-gate. The gap to what a smallholder receives is `basis_local` in RT-7 and is NOT measured here (LIT-035 makes the same point). Nominal, so a long-window volatility includes inflation drift; the calibration uses log returns, which removes a constant drift but not a changing one.

**Validation (run 2026-10-08T07:26:56Z).** Schema: three columns, month key parses, values numeric or blank. Coverage: continuous monthly from 1960-01. Units: `($/kg)` read from the header row before conversion; the script refuses any other unit. Plausibility: Arabica above Robusta in every month with both present, as expected.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-04` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-04/CMO-Historical-Data-Monthly-20261008.xlsx` (gitignored; Vault copy under `05-raw-data/DS-04/`) |
| Raw SHA-256 | `ea1c350827878ea3bbe30e3cda16a13fd3bd5b409b8458940dc94a36b5a33154` |
| Retrieved | 2026-10-08T07:26:55Z |
| Ingestion script | `scripts/ingest/ds04_pink_sheet.py` at commit `40d0220` |
| Processed | 2026-10-08T07:26:56Z |
| Source URL | https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx |
| Publisher series | Coffee, Arabica; Coffee, Robusta (sheet 'Monthly Prices') |
