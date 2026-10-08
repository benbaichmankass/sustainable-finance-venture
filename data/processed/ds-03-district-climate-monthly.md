# DS-03 — district climate, monthly (NASA POWER)

One row per district per month, 1981-01 to 2025-12 (3240 rows across 6 points). Source: NASA POWER monthly point API, agroclimatology community, parameters `PRECTOTCORR`, `T2M`, `T2M_MAX`.

| Column | Meaning | Unit |
|---|---|---|
| `Region` | RT-7 region key | |
| `District` | Coffee district the point represents | |
| `Lat`, `Lon` | Request coordinates (district centroid, by judgement) | decimal degrees |
| `Elev_m` | Elevation POWER reports for the grid cell | m |
| `Month` | Calendar month | `YYYY-MM` |
| `Precip_mm` | Monthly precipitation: POWER's `PRECTOTCORR` (mm/day, bias-corrected) x days in month | mm |
| `T2M_C` | Mean 2 m air temperature | deg C |
| `T2M_Max_C` | Mean daily maximum 2 m temperature | deg C |

**What it is.** A reanalysis-based grid product at 0.5 x 0.625 degrees: a regional climate signal, not a station and not a plot. Good enough to build a seasonal rainfall anomaly for the RT-7 climate factor; not good enough to settle an index-insurance trigger (that is DS-02, CHIRPS, with a documented boundary).

**Validation (run 2026-10-08T07:25:12Z).** Schema: nine columns. Coverage: every point returns every month from 1981-01; POWER's own annual aggregate (month code 13) is dropped and recomputed downstream. Units: mm/day converted to monthly mm using the calendar month length. Fill values (-999) are skipped, none were present in this pull unless noted in the query log.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-03` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-03/nasa-power-monthly-20261008.json` (gitignored; Vault copy under `05-raw-data/DS-03/`) |
| Raw SHA-256 | `68998bdd0e849275f079a8024c7c495b7b24ddc5da701a600a3c57a498108925` |
| Retrieved | 2026-10-08T07:25:12Z |
| Ingestion script | `scripts/ingest/ds03_nasa_power.py` at commit `40d0220` |
| Processed | 2026-10-08T07:25:12Z |
| Points | colombia/Huila (2.45, -75.65); colombia/Cauca (2.45, -76.6); ethiopia/Jimma (7.67, 36.83); ethiopia/Sidama (6.8, 38.4); vietnam/Dak Lak (12.67, 108.05); vietnam/Lam Dong (11.95, 108.44) |
| API | https://power.larc.nasa.gov/api/temporal/monthly/point |
