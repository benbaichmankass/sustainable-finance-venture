# DS-10 — Colombian coffee prices, monthly (FNC)

One row per month from 2000-01 to 2026-09. Source workbook: FNC, "Precios, area y produccion de cafe" (https://federaciondecafeteros.org/wp-content/uploads/2026/09/Precios-area-y-produccion-de-cafe-Septiembre-2026.xlsx).

| Column | Meaning | Unit |
|---|---|---|
| `Month` | Calendar month | `YYYY-MM` |
| `Internal_Price_COP_per_carga` | FNC base internal purchase price (precio interno base de compra), monthly average | COP per carga of 125 kg dry parchment |
| `Base_Yield_Factor_Assumed` | The FNC base yield factor the price is quoted at: 94 from 2024-04 (FNC committee decision of March 2024, effective 1 April 2024), 88 from 2019-09 to 2024-03 (the factor the 2024 decision replaced; the earlier start of 88 is not documented here, so months before 2019-09 are left blank) | kg parchment per 70 kg excelso |
| `ExDock_Price_USc_per_lb` | FNC external price of Colombian coffee, ex-dock | US cents / lb |
| `ICO_Composite_USc_per_lb` | ICO composite indicator, as reproduced by the FNC | US cents / lb |
| `ICO_Colombian_Milds_USc_per_lb` | ICO Colombian milds group indicator, weighted average | US cents / lb |
| `ICO_Other_Milds_USc_per_lb` | ICO other milds group indicator, weighted average (the series the World Bank Pink Sheet *Coffee, Arabica* follows) | US cents / lb |

**Converting the internal price to green coffee.** At factor 94 a carga of 125 kg parchment yields 93.09 kg of excelso (FNC daily price sheet, 2026-10-07; RES row). A per-kg-green internal price is `Internal_Price_COP_per_carga / 93.09` for months at factor 94. The calibration uses only those months. The FNC states that the 2024 factor change "does not affect what the producer receives", i.e. the carga price moved with the factor.

**Validation (run 2026-10-08T08:50:01Z).** Schema: seven columns. Coverage: internal price continuous monthly from 1944 in the source, kept from 2000; ICO columns from 2000-01. Units read from the sheet headers. Plausibility: the ex-dock price tracks the ICO Colombian milds indicator within a few cents in every month checked.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-10` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-10/fnc-precios-area-produccion-20261008.xlsx` (gitignored; Vault copy under `05-raw-data/DS-10/`) |
| Raw SHA-256 | `d5d023a76856abe5802b85d2400b9f42f496b96560d9435bec13d9e6b8dc0563` |
| Retrieved | 2026-10-08T08:49:32Z |
| Ingestion script | `scripts/ingest/ds10_fnc_colombia.py` at commit `1905e3f` |
| Processed | 2026-10-08T08:50:01Z |
| Source page | https://federaciondecafeteros.org/wp/estadisticas-cafeteras/ |
| Workbook URL | https://federaciondecafeteros.org/wp-content/uploads/2026/09/Precios-area-y-produccion-de-cafe-Septiembre-2026.xlsx |
