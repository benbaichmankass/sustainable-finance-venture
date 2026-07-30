# Archive — Master Reference Tracker (Google Sheet)

> **Provenance.** Verbatim export of the Google Sheet *"Sustainable Finance Venture — Master Reference Tracker"*, captured 2026-07-30.
> Source: Google Drive — link in `private/pointers.csv` (kept out of the public repo; the archive below is the content)
>
> **This file is an archive, not the source of truth.** The live content has been split into the repo files listed under "Where this content now lives". Edit those; this file exists so the original wording is recoverable.

## Where this content now lives

| Sheet tab | Now maintained in |
|---|---|
| README / index | `README.md` |
| 60/90-Day Milestone Plan | `data/milestones.csv`, `docs/milestone-plan.md` |
| Open Questions | `data/open-questions.csv` |
| Lit Matrix | `literature/lit-matrix.csv` |
| Synthesis Memos | `data/synthesis-memos.csv` + `literature/notes/*.md` |
| Partner Tracker | `data/partner-tracker.csv` (public tier) + `private/partner-contacts.csv` (contact status) |
| PhD Programs | `data/phd-programs.csv` (public tier) + `private/phd-applications.csv` (supervisors, status) |

The partner and PhD tabs were split when the repo was made publishable: who an organization is and why it matters is public; a named individual and our relationship status with them is not. See `docs/publishing.md`.

---

## Tab: README

**Sustainable Finance Venture — Master Reference Tracker**

This workbook is the collaborative literature/reference hub for the project. See the GitHub repo (sustainable-finance-venture) for docs, working notes, and versioned files. This Sheet is canonical for: Lit Matrix, Partner Tracker, PhD Programs, Open Questions.

Tabs:
- Lit Matrix: one row per source, tagged by axis, with findings/relevance/status
- Synthesis Memos: links + summaries of the 3 planned synthesis memos
- Partner Tracker: candidate NGOs / VSLA networks / academics / commercial partners
- PhD Programs: target universities/supervisors, fit notes, application status
- Open Questions: running log of unresolved decisions

Related: GitHub repo (private) - benbaichmankass/sustainable-finance-venture

### 60/90-Day Milestone Plan (updated)

- **Days 1-30:** Finalize lit-matrix anchors (target 10-15, currently 8); complete 3 synthesis memos (done, draft stage - move to Reviewed); identify 3-5 concrete market gaps via partner outreach (Partner Tracker now has 10 candidates - begin contact).
- **Days 31-60:** Screen and interview 3-5 candidate originator/verification partners; select Israel pilot use-case and draft product/operating model; begin PhD supervisor outreach (see PhD Programs Outreach Plan column); resolve Open Questions #1-3 (legal, pool size, data schema) with counsel/CGAP input.
- **Days 61-90:** Draft pilot design doc (20-50 VSLA or Israel equivalent cohort, RCT/quasi-experimental design per Open Question #4); secure at least 1 anchor originator + 1 verification partner commitment; outline first-loss/blended-finance structure with 1-2 DFI/impact fund contacts; submit first PhD applications where cycles allow.
- **Owners:** Founder (BB) owns all workstreams currently; assign partner outreach and legal/regulatory research to first hire or advisor as team grows.

### GitHub file index (as recorded in the Sheet)

GitHub repo (canonical code/docs): https://github.com/benbaichmankass/sustainable-finance-venture

- `/docs/working-doc.md` - main working/planning doc
- `/docs/research-agenda.md` - research agenda + open questions (research side)
- `/literature/lit-matrix.csv` - literature matrix (synced with Lit Matrix tab, 8 anchors LIT-001-008)
- `/literature/notes/memo-1-vslas.md` - Synthesis Memo 1: VSLAs and savings groups
- `/literature/notes/memo-2-microfinance-impact.md` - Synthesis Memo 2: Microfinance impact evidence
- `/literature/notes/memo-3-securitization-blended-finance.md` - Synthesis Memo 3: Securitization & blended finance
- `/product-design/` - placeholder, product specs/term sheets to be added
- `/data/` - placeholder, pilot data schemas to be added

**How to resume a session:** 1) Start at this README tab. 2) Check Open Questions tab for unresolved decisions. 3) Check GitHub `/docs/research-agenda.md` for research-side status. 4) Cross-reference Partner Tracker and PhD Programs tabs before new outreach.

---

## Tab: Open Questions

| Question | Category | Linked area | Status | Notes |
|---|---|---|---|---|
| Should PhD field research (Israel first, Africa second) use cluster randomization or a stepped-wedge design? | PhD/Research Design | PhD Programs | Open | To discuss with prospective supervisors |
| What cross-border legal/regulatory framework (jurisdiction, SPV domicile) will govern pooling Israeli and African-originated receivables into a single securitization vehicle? | Securitization Structure | Partner Tracker / Product Design | Open | Need input from securities counsel in Israel + target African jurisdiction; determine if a single offshore SPV (e.g., Cayman/Luxembourg) or parallel local SPVs feed a master trust. |
| What is the minimum viable receivables pool size (number of VSLAs / loan count / $ notional) needed to make a securitization economically viable given fixed legal/structuring costs? | Securitization Structure | Product Design / Pilot Design | Open | Rule-of-thumb ABS deals need $20-50M+ notional to justify costs; pilot-stage pools (20-50 VSLAs) will be far below this - need a warehousing/aggregation bridge strategy until scale is reached. |
| What standardized data schema and underwriting variables must be captured at origination to make VSLA-level receivables poolable and ratings-agency legible later? | Data Architecture | Data / Product Design | Open | Draft a canonical schema (borrower ID, loan terms, repayment history, group guarantee structure, geospatial/agro-climate tags) benchmarked against existing microfinance MIS + ABS reporting templates (e.g., European DataWarehouse loan-level data templates). |
| What is the best blended-finance / first-loss structure for the initial pilot (Israel and Africa) to attract anchor investors before a full public securitization is feasible? | Securitization Structure | Partner Tracker / Pilot Design | Open | Explore donor/DFI first-loss tranches (e.g., USAID, IFC, FMO) layered with local bank senior debt; benchmark against existing blended-finance microfinance funds (responsAbility, BlueOrchard). |
| Which RCT design (cluster randomization vs. stepped-wedge) is most feasible given VSLA group structures and ethical/operational constraints in Israel vs. Africa pilots? | Research Design | PhD Programs / Pilot Design | Open | Cluster randomization likely cleaner for Israel (smaller, controlled pilot); stepped-wedge may be more acceptable to African NGO partners who resist withholding treatment - confirm with prospective supervisors and verification partners. |
| Which verification partners (local NGOs, auditors, academic field teams) can provide independent, ideally double-blind, data verification for pilot outcomes? | Partnerships / Verification | Partner Tracker | Open | Shortlist candidates from J-PAL affiliated field offices, CGAP, and local university research centers in Israel and target African country; confirm data-sharing and IRB requirements. |

---

## Tab: Synthesis Memos

| Memo # | Title | Covers Axis | Status | Link | Key Takeaways |
|---|---|---|---|---|---|
| 1 | What VSLAs and similar structures actually achieve | 1-VSLA | Drafted | /literature/notes/memo-1-vslas.md | VSLA/savings-group model is empirically the most de-risked starting point: cluster-RCT evidence (Ksoll et al. 2016) and cross-country synthesis show consistent, replicable gains in savings and resilience. Group cycles already generate structured, periodic data (contributions, payouts, loan requests) - this is the natural first data source for underwriting and eventual securitization. Recommend Israel migrant-worker pilot to test data capture + parametric triggers before Africa scale-up. |
| 2 | What microfinance RCTs and reviews say about impact and design | 2-Microfinance | Drafted | /literature/notes/memo-2-microfinance-impact.md | Microfinance systematic reviews show average income/poverty effects are small and heterogeneous, but effects on consumption smoothing and female empowerment are more robust. Implication: don't oversell income/business growth claims to investors; frame product around resilience/smoothing outcomes which have the strongest evidence base and are easiest to verify for impact reporting and securitization covenants. |
| 3 | How securitization/blended finance has been applied to microfinance | 3-Securitization / 4-Blended finance | Drafted | /literature/notes/memo-3-securitization-blended-finance.md | Securitization of community/microfinance assets is feasible but nascent: existing models (IMBS tranching, Rwanda solar ABS, African bank SME securitizations) all required a standardization layer + credit enhancement/first-loss + anchor investor before market-rate tranches were sellable. Blended finance literature confirms guarantees/concessional capital are the typical bridge. Implication for our venture: design the data schema and underwriting rules from day one to match ABS eligibility criteria (loan-level granularity, standardized covenants, verifiable repayment/claims history) so that a 2-3 year pilot pool can credibly attract a DFI/anchor investor for a first securitized tranche. |

---

## Tab: Lit Matrix

Archived at 8 rows (LIT-001 to LIT-008). Live version — now 15 rows — is `literature/lit-matrix.csv`. The original 8 rows are preserved verbatim there; only the `Open_Questions` and `Link_Citation` columns were reconciled between the Sheet and the repo copy, and a `URL` column was added.

---

## Tab: Partner Tracker

Archived content migrated verbatim to `data/partner-tracker.csv` (10 rows, PT-01 to PT-10). No content was dropped; an `ID` column was added and free-text notes were extended with cross-references to the relevant open questions.

---

## Tab: PhD Programs

Archived content migrated to `data/phd-programs.csv` (9 rows, PHD-01 to PHD-09). Note: the Sheet's "Candidate Supervisors" column contained two cells where text from an adjacent row had been pasted in mid-string (LSE and Hebrew University rows). Those were untangled during migration — the LSE row's stray Cambridge text and the Hebrew University row's stray Tel Aviv text were removed, and the intended content preserved in the correct rows.
