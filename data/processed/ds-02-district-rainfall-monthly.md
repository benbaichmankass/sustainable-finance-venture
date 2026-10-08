# DS-02 — CHIRPS v2.0 monthly rainfall over the six RT-7 coffee districts

One row per district per month, 1981-01 to 2026-08. Simple mean of the CHIRPS 0.05-degree cells whose centre falls inside the district polygon.

| Column | Meaning | Unit |
|---|---|---|
| `Region` | RT-7 region key | |
| `District` | Huila, Cauca (Colombia, departments); Jimma, Sidama (Ethiopia, zones as of the 2016 boundary set); Dak Lak, Lam Dong (Viet Nam, provinces) | |
| `Month` | Calendar month | `YYYY-MM` |
| `Precip_mm` | Mean monthly precipitation over the cells inside the polygon | mm |
| `N_Cells` | Cells averaged (constant per district unless CHIRPS reports a missing cell) | |

**The boundaries.** geoBoundaries gbOpen release, commit `9469f09`, simplified geometries, fetched from `media.githubusercontent.com` (the repository stores them with Git LFS). The six features are copied verbatim into `data/processed/ds-02-district-boundaries.geojson` with their `shapeID`, so a reader can see exactly which polygon produced each number. Cells inside the box but outside the polygon are discarded: Huila 591 of 2256; Cauca 1009 of 2269; Jimma 605 of 1368; Sidama 223 of 672; Dak Lak 437 of 924; Lam Dong 322 of 824. Ethiopia's set is the 2016 vintage, in which Sidama is a zone of SNNPR; it became a regional state in 2020 with the same outline. The polygons are whole administrative units, not coffee belts: Cauca's includes its Pacific lowlands (hence a department mean above 3,000 mm against roughly half that in the Andean coffee municipalities) and Dak Lak's its lowland east. A coffee-zone mask (altitude band or municipality list) is the refinement; the anomaly series, which is what the model uses, is less affected than the level. Licences: see the gbOpen metadata per country (OpenStreetMap-derived for Colombia, Open Africa / Code for Ethiopia CC BY for Ethiopia, geoBoundaries / Wikipedia for Viet Nam); attribution recorded in `NOTICE`.

**The rainfall.** CHIRPS v2.0 (Climate Hazards Center, UC Santa Barbara), monthly, 0.05 degree, 1981 onward, read through the IRI Data Library's `gridtable.tsv` view of the bounding box; the raw tables are kept under `data/raw/DS-02/` (gitignored) with query logs. CHIRPS blends satellite estimates with station data; it is a rainfall product, not a drought index, and it says nothing about temperature, which NASA POWER (DS-03) covers at the centroid.

**Derived files.** `ds-02-district-rainfall-annual.csv` holds calendar-year totals for complete years with the standardised anomaly (`Anomaly_Z`, over the district's own record) and the district's mean and coefficient of variation. `data/rt7-climate-history.csv` averages the two districts' anomalies per region and re-standardises them; that series is what the model's empirical climate factor bootstraps from (`climate_rain_beta`). Calendar years are used for every region; the coffee year runs across the calendar year in all three, so a flowering-to-harvest window is a refinement left for a partner's own harvest calendar.

**Validation (run 2026-10-08T10:40:17Z).** Schema: five columns. Coverage: every district has every month from 1981-01 to the latest CHIRPS month. Units: mm/month as served. Plausibility: annual means fall where the literature puts them (Huila and Cauca roughly 1,200 to 2,000 mm; Jimma and Sidama 1,200 to 1,800; Dak Lak and Lam Dong 1,700 to 2,000), and the within-region district anomalies are positively correlated.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-02` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-02/chirps-monthly-huila-20261008.tsv` (gitignored; Vault copy under `05-raw-data/DS-02/`) |
| Raw SHA-256 | `d74c3805437cee6ed11bb24f2c8f049a47e1d0fc2235be16dc3641f59a2e0c5b` |
| Retrieved | 2026-10-08T09:33:23Z |
| Ingestion script | `scripts/ingest/ds02_chirps.py` at commit `0ef54eb` |
| Processed | 2026-10-08T10:40:17Z |
| IRI base | https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly/.global/.precipitation |
| Boundary source | https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/9469f09/releaseData/gbOpen/<ISO>/<ADM>/geoBoundaries-<ISO>-<ADM>_simplified.geojson |
| Boundary raw SHA-256 (COL ADM1) | 038b7692a8e3bdc52b072b8de305d0dd8e88fe3e869c8c4889ff18cddd7f5a81 |
| Other raw files | one gridtable per district under data/raw/DS-02/ with its own query log |
