# DS-11 — Kiva field partners behind the sampled loans

One row per field partner appearing in `ds-11-kiva-agriculture-loans.csv`, with Kiva's published portfolio metrics at retrieval.

| Column | Meaning (Kiva's definitions) |
|---|---|
| `Default_Rate_Pct` | Amount of ended loans defaulted as a share of the amount of ended loans, Kiva-funded portfolio |
| `Arrears_Rate_Pct` | Amount in arrears as a share of the outstanding Kiva-funded portfolio |
| `Loans_At_Risk_Rate_Pct` | Share of outstanding portfolio with any payment overdue |
| `Average_Loan_Size_USD`, `Average_Loan_Term_Months` | Across the partner's Kiva loans |
| `Loans_Posted` | Count of loans the partner has posted on Kiva |
| `Risk_Rating` | Kiva's internal rating (0.5 to 5 stars) |

**Reading the rates.** These describe each partner's Kiva-funded book, not coffee loans specifically and not the partner's whole portfolio. The default rate is a loss-of-amount measure over the partner's history; the arrears rate is a portfolio-at-risk measure at a point in time. For the RT-7 proxy the arrears rate stands in for the normal-year probability of a payment problem and the default rate is recorded as an observation. One Vietnamese partner shows an arrears rate above 60 percent and nearly all of its book at risk: a partner in distress, which the loans-posted weighting limits but does not remove.

**Validation (run 2026-10-08T08:51:46Z).** Partner ids unique; rates numeric; countries as published.

## Provenance

| | |
|---|---|
| Catalogue row | `DS-11` in `data/data-catalog.csv` |
| Raw extract | `data/raw/DS-11/kiva-agri-loans-20261008.json` (gitignored; Vault copy under `05-raw-data/DS-11/`) |
| Raw SHA-256 | `2fb6a77aded0d97116bfaa69c09c9f3e44d603d06e872fae022bc0d9969c7bbc` |
| Retrieved | 2026-10-08T08:51:46Z |
| Ingestion script | `scripts/ingest/ds11_kiva_loans.py` at commit `1905e3f` |
| Processed | 2026-10-08T08:51:46Z |
| API | https://api.kivaws.org/graphql |
