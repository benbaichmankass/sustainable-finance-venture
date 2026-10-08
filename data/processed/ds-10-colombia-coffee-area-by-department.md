# DS-10 — Colombian coffee area by department (FNC / SICA)

One row per department per year, 2002 to 2025 (516 rows). Thousand hectares cultivated with coffee; source SICA (Sistema de Informacion Cafetera) as reproduced in the FNC workbook. Years marked with an asterisk in the source are cut at December; `n/d` cells are omitted. The source's `TOTAL` row is kept as a department named `TOTAL` so shares can be computed without re-summing.

| Column | Meaning | Unit |
|---|---|---|
| `Department` | Department name as the FNC writes it (accents as in source) | |
| `Year` | Calendar year | |
| `Area_kha` | Cultivated coffee area | thousand ha |

Used for the share of the national area in Huila and Cauca (the RT-7 Colombia districts). No department-level production is in the workbook, so department yields cannot be derived from it.

**Validation (run 2026-10-08T08:50:01Z).** Schema: three columns; department names deduplicated as written; numeric values only.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-10` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-10/fnc-precios-area-produccion-20261008.xlsx` (gitignored; Vault copy under `05-raw-data/DS-10/`) |
| Raw SHA-256 | `d5d023a76856abe5802b85d2400b9f42f496b96560d9435bec13d9e6b8dc0563` |
| Retrieved | 2026-10-08T08:49:32Z |
| Ingestion script | `scripts/ingest/ds10_fnc_colombia.py` at commit `1905e3f` |
| Processed | 2026-10-08T08:50:01Z |
| Workbook URL | https://federaciondecafeteros.org/wp-content/uploads/2026/09/Precios-area-y-produccion-de-cafe-Septiembre-2026.xlsx |
