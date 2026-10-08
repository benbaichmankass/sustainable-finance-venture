# DS-01 — coffee, green: national area, production and yield (FAOSTAT)

One row per country per year, 1961 to 2024 (160 rows). FAOSTAT domain QCL (Crops and livestock products), item Coffee, green (656), elements Area harvested, Production and Yield, for Colombia, Ethiopia and Viet Nam.

| Column | Meaning | Unit |
|---|---|---|
| `Region` | RT-7 region key (the country; FAOSTAT is national) | |
| `Year` | Calendar year as FAOSTAT reports it | |
| `Area_ha` | Area harvested | ha |
| `Production_t` | Production of green coffee | t |
| `Yield_t_ha` | Yield, converted from the publisher's kg/ha (or hg/ha in older vintages) | t / ha |
| `Flags` | FAOSTAT observation-status flags present in that year's rows (A official, E estimated, I imputed, T unofficial, blank official per the publisher's flag table) | |

**What it is.** National averages. A district (Huila, Jimma, Dak Lak) can sit well above or below its national figure, and a cooperative's members further still. RT-7 uses the national series for the year-to-year *variability* of the regional yield factor and as a first anchor for the level; the level should be replaced by district statistics or partner delivery records (DS-08) before it is believed.

**Validation (run 2026-10-08T07:25:28Z).** Schema: six columns. Coverage: continuous from 1961 for every country. Units: converted once, in the script, which refuses any unit it does not expect. Plausibility: production / area reproduces the published yield within 2 percent in every row.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-01` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-01/faostat-qcl-coffee-3-countries-20261008.csv` (gitignored; Vault copy under `05-raw-data/DS-01/`) |
| Raw SHA-256 | `cefd3fc37918ab58ac4b8b07e78797ae84b33565eaf2865596c12e8923e54dab` |
| Retrieved | 2026-10-08T07:25:28Z |
| Ingestion script | `scripts/ingest/ds01_faostat_yields.py` at commit `40d0220` |
| Processed | 2026-10-08T07:25:28Z |
| Bulk file | https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip |
| Bulk SHA-256 | c5835418c18f9322e7decbd6800f93a216eaae3cdfa31acb08f0518c0c6d6853 |
| Filter | Area in (Colombia, Ethiopia, Viet Nam) and Item startswith 'Coffee' and Element in (Area harvested, Production, Yield) |
