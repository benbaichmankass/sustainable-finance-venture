# DS-09 — exchange rates to the US dollar

Two series in one file, distinguished by `Frequency` and `Source`.

| Column | Meaning |
|---|---|
| `Currency` | `COP`, `ETB`, `VND` |
| `Period` | `YYYY-MM` for monthly rows, `YYYY` for annual rows |
| `Frequency` | `monthly` or `annual` |
| `LCU_per_USD` | Local currency units per US dollar |
| `N_Daily_Obs` | For COP months, the number of daily TRM values averaged |
| `Source` | Which series the row came from |

**COP.** Banco de la Republica's TRM, daily, 2003-01 to 2026-10 (286 months), via Colombia's open-data portal. Monthly rows are the simple mean of the daily values in the month.

**ETB and VND.** World Bank WDI official exchange rate (period average), annual, 2000 onward where published. Annual rows also exist for COP as a cross-check. Caveat: Ethiopia moved to a market-determined rate in July 2024, so the 2024 annual average (about 83) sits between the pre-float level (about 57) and the post-float level (above 110); use it for 2024 figures with care, and prefer a source's own stated rate where a document gives one.

**Validation (run 2026-10-08T08:49:23Z).** Schema: six columns. Coverage: every complete month from the first TRM month has at least 15 daily observations (the TRM is published for business days, about 20 a month); the current month is partial and its N_Daily_Obs says so. Units: local currency per USD in both sources, no conversion applied.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-09` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-09/trm-daily-20261008.json` (gitignored; Vault copy under `05-raw-data/DS-09/`) |
| Raw SHA-256 | `f39b814c93fd47b6b6f77d2437e78a1107ae94f86b805c37f177ae78992ba475` |
| Retrieved | 2026-10-08T08:48:53Z |
| Ingestion script | `scripts/ingest/ds09_exchange_rates.py` at commit `1905e3f` |
| Processed | 2026-10-08T08:49:23Z |
| TRM request | https://www.datos.gov.co/resource/32sa-8pi3.json?$limit=20000&$order=vigenciadesde%20ASC&$where=vigenciadesde%20%3E%3D%20%272003-01-01%27 |
| WDI request | https://api.worldbank.org/v2/country/COL;ETH;VNM/indicator/PA.NUS.FCRF?format=json&per_page=200&date=2000:2025 |
| WDI raw SHA-256 | b15e2e8cb6efff98ad24d0829d8cb3ba74d1f67172665428fdfcfe02d28bccd8 |
