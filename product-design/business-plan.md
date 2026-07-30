# Business Plan — Working Draft

**Status:** Draft · **Last updated:** 2026-07-30 · **Owner:** BB

This is the current, canonical business plan. It supersedes two earlier framings, both archived for lineage:

- `archive/google-drive/web3-vsla-business-plan.md` (Feb 2025) — Web3/DAO delivery mechanism
- `archive/google-drive/sds-work-plan.md` (Nov 2024) — infrastructure/energy project securities

**What carried over, and what did not.** The community-finance core, the liquidity-pool/structured-product revenue model, the risk-layer positioning, and the insurance expansion path all survive from the Web3 plan; the blockchain/DAO delivery mechanism does not — smart-contract governance solved a trust problem that VSLAs already solve socially, while adding regulatory and FX risk the venture does not need to carry. From the SDS plan, the pooling logic (combine assets with uncorrelated idiosyncratic risk across timeline, type and geography), the "design the asset to capture induced growth" principle, and the public-markets distribution ambition all carry directly into the securitization design.

---

## 1. Concept

A structuring and verification layer that turns community-originated loan and insurance receivables into standardized, verifiable, poolable assets that institutional capital can price.

The thesis is that some sustainable-development problems persist not because solutions are absent, but because the market lacks the right financial product design, underwriting logic, distribution mechanism and de-risking structure to channel capital toward them.

## 2. Three-layer structure

| Layer | Who | What they do |
|---|---|---|
| **Origination** | VSLAs, NGOs, MFIs, community banks, employer networks | KYC, disbursement, collections, claims, local compliance |
| **Risk (our layer)** | Us | Underwriting rules, monitoring dashboards, early-warning systems, risk-sharing/tranching design, first-loss structuring |
| **Product** | Joint | Loans, insurance, bundled products — priced using group-behaviour data |

We sit in the structuring layer deliberately. Regulated entities handle origination, claims, collections and compliance; we are asset-light and do not seek a licence in the first phase.

**Target end state:** investment-grade tranches sellable to institutional investors, with DFI/philanthropic capital absorbing first-loss/junior risk and private capital in mezzanine and senior.

## 3. Revenue model

1. **Structuring and servicing fees** on pools we assemble and monitor.
2. **Retained economic interest** in the pools — which is not optional: EU/UK risk-retention rules require the originator/sponsor to hold a minimum economic interest if senior notes are placed with those investors (see `literature/notes/memo-3-securitization-blended-finance.md`).
3. **Data/analytics licensing** to originators and funders once the underwriting engine has a track record.

The earlier Web3 plan's "non-voting investor in the VSLA" model is preserved in substance by (2): we take return on capital without taking governance control of the group.

## 4. Toolkit to build

1. Standardized data schema for loans/insurance — ABS-data-tape-ready (→ OQ-3)
2. Underwriting engine — rules-based plus ML scoring incorporating community signals
3. Monitoring & early-warning system — DPD tracking, delinquency/claim pattern alerts
4. Impact evaluation module — randomization infrastructure, pre-registered designs with academic partners
5. Securitization modelling — cash-flow waterfall models, loss/prepayment simulations

## 5. Market and pilot direction

**Two candidate first sites.**

- **Israel (migrant-worker communities)** — logistical proximity, easier hands-on project management, existing regulatory environment around foreign-worker insurance. A controlled environment in which to develop the research protocol and tooling.
- **Africa (multi-country VSLA networks)** — deep traditions of community-based finance, high financial exclusion, alignment with blended-finance/SDG capital mobilization narratives, and a nascent securitization market that offers first-mover advantage in standard-setting.

**Working decision:** anchor methodology development in Israel first, then replicate in an African country as a second field site once the framework is proven. Final decision pending contact/access assessment.

## 6. Structuring assumptions (evidence-backed)

Derived from the literature review; see Memo 3 for sources.

| Assumption | Working value | Basis |
|---|---|---|
| First-loss / junior tranche size | 10–20% of structure | LIT-013, LIT-015 |
| Pilot warehouse size | Tens of millions USD, DFI-anchored | LIT-011, LIT-012 |
| Public issuance threshold | ≥ USD 100m | LIT-012 |
| Originator structure | Multi-originator, plausibly regional | LIT-008, LIT-011 |
| Track record before first tranche | 2–3 years of clean repayment data | LIT-004, LIT-006 |

These are starting ranges to be tested, not targets. Each is an observed central tendency across deals that do not closely resemble our asset class.

## 7. Risks

| Category | Risk | Mitigation |
|---|---|---|
| Market | No investor appetite for a novel asset class at pilot scale | Anchor investor secured before structuring; frame first vehicle as a blended fund, not a public ABS |
| Financial | FX exposure between local-currency receivables and hard-currency notes | Hedging or local-currency tranches; DFI guarantees for FX risk |
| Financial | Interest-rate mismatch across the waterfall | Match funding tenor to asset tenor at structuring |
| Credit | Community portfolios underperform relative to modelled loss curves | First-loss layer; conservative advance rates; early-warning monitoring |
| Legal | Cross-border transfer fails a true-sale test in one jurisdiction | Run the LIT-009 six-point checklist with local counsel **before** committing to a geography (→ OQ-1) |
| Regulatory | Origination partner loses licence or falls foul of local rules | Partner diligence; multi-originator structure limits single-partner exposure |
| Operational | Origination data quality too poor to underwrite | Schema and data capture designed at origination, not retrofitted (→ OQ-3) |
| Reputational | Impact claims outrun the evidence base | Frame around resilience/smoothing, which the evidence supports (Memo 2) |

## 8. Open work

Tracked in `data/milestones.csv` and `data/open-questions.csv`. The near-term critical path:

1. Draft the canonical data schema (OQ-3) — blocks everything downstream.
2. Jurisdiction scan with counsel (OQ-1) — blocks pilot site selection.
3. First originator and verification partner conversations (M-03, M-04).
4. Choose the first instrument: loan vs insurance vs bundled.

## 9. Not yet drafted

Sections carried forward from the earlier plans that still need work, listed so the gaps stay visible:

- Financial plan — cost structure, revenue projections, funding ask
- Organization & management — team structure, hiring sequence
- Competitive analysis — who else is structuring community-originated assets
- Marketing/BD strategy — how originator partners are actually reached
- Legal structure of the operating company itself
