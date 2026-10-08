# DS-02 — district rainfall, calendar-year totals and anomalies

Derived from `ds-02-district-rainfall-monthly.csv`: complete calendar years only. `Anomaly_Z` is `(Precip_mm - Mean_mm) / sd` over the district's own record; `CV` is `sd / Mean_mm`. See the monthly file's dictionary for sources, boundaries and caveats.

**Validation (run 2026-10-08T10:40:17Z).** One row per district per complete year; anomalies have mean 0 and sd 1 per district by construction.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-02` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-02/chirps-monthly-huila-20261008.tsv` (gitignored; Vault copy under `05-raw-data/DS-02/`) |
| Raw SHA-256 | `d74c3805437cee6ed11bb24f2c8f049a47e1d0fc2235be16dc3641f59a2e0c5b` |
| Retrieved | 2026-10-08T09:33:23Z |
| Ingestion script | `scripts/ingest/ds02_chirps.py` at commit `0ef54eb` |
| Processed | 2026-10-08T10:40:17Z |
| Derived from | ds-02-district-rainfall-monthly.csv |
