# DS-11 — Kiva agriculture loans, Colombia and Viet Nam (proxy population)

One row per loan: the 3000 newest loans in Kiva's Agriculture sector per country at retrieval, all statuses. Colombia 3000 loans (603 mention coffee in the use text), Viet Nam 3000 loans (81 mention coffee). Ethiopia has no Kiva agriculture loans.

| Column | Meaning |
|---|---|
| `Country` | ISO code |
| `Loan_ID` | Kiva loan id (public) |
| `Amount_USD` | Loan amount posted on Kiva, USD |
| `Term_Months` | Lender repayment term in months (Kiva's `lenderRepaymentTerm`) |
| `Status` | Kiva status at retrieval (fundraising, funded, expired, refunded) |
| `Raised_Date`, `Disbursal_Date`, `Defaulted_Date`, `Ended_Date` | As published; blank when not set |
| `Delinquent` | Kiva's delinquency flag at retrieval |
| `Borrower_Count` | 1 for individual loans, more for groups |
| `Activity` | Kiva activity (Agriculture, Farming, Pigs, ...); there is no coffee activity, hence the text flag |
| `Coffee_Mention` | `yes` if the use-of-funds text mentions coffee |
| `Local_Currency`, `Disbursal_Amount_LCU` | Disbursal terms where published |
| `Partner_ID` | Field partner; metrics in `ds-11-kiva-partners.csv` |

**What it is.** A proxy for smallholder agricultural borrowers in two of the three RT-7 countries: real loans to real farmers, including hundreds whose stated purpose is coffee (fertiliser, planting, a wet mill), with their sizes and terms. It is not a cooperative's book: Kiva's partners are microfinance institutions and social enterprises, the loans are those partners chose to list, and Kiva's status fields on recent loans say nothing about repayment (no loan in this pull is past its term). Repayment behaviour comes only from the partner-level rates.

**Validation (run 2026-10-08T08:51:46Z).** Schema: sixteen columns. Coverage: newest-first, so the date range is whatever the last 3000 loans span per country. Units: USD as posted. Names and towns were dropped from the processed file.

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
| Filters | country in ['CO', 'VN']; sector 1 Agriculture; status all; sortBy newest; 3000 newest per country |
