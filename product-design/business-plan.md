# Business Plan — Working Draft

**Status:** Draft · **Last updated:** 2026-07-30 · **Owner:** BB

This is the venture-level plan. Individual product lines have their own documents in product-design/product-lines/.

It draws on three earlier framings, all archived for lineage:

- archive/google-drive/sds-work-plan.md (Nov 2024\) — sustainable development securities; the general thesis  
- archive/google-drive/bfav-business-plan.md (Apr 2024\) — agrivoltaic project finance; now Product Line 2  
- archive/google-drive/web3-vsla-business-plan.md (Feb 2025\) — Web3/DAO delivery; now Product Line 1

**What carried over, and what did not.** From the Web3 plan: the community-finance core, the pooled-liquidity/structured-product revenue model, the risk-layer positioning, and the insurance expansion path all survive; the blockchain/DAO delivery mechanism does not — smart-contract governance solved a trust problem VSLAs already solve socially, while adding crypto-regulatory and FX risk the venture has no reason to carry. From the SDS plan: the pooling logic (combine assets with uncorrelated idiosyncratic risk across timeline, type and geography), the "design the asset to capture induced growth" principle, and the public-markets distribution ambition carry directly into the securitization design. From BFAV: the whole thing, promoted from a standalone business to a product line.

---

## 1\. Concept

A structuring and verification layer that turns cash flows originated in underfunded sustainable-development sectors into standardized, verifiable, poolable assets that institutional capital can price.

The thesis is that some sustainable-development problems persist not because solutions are absent, but because the market lacks the right financial product design, underwriting logic, distribution mechanism and de-risking structure to channel capital toward them.

**The thesis is layer-agnostic.** It does not say anything about VSLAs specifically. It says that if an asset's cash flows are standardized, verifiable and legally transferable *at origination*, they can be pooled and sold; and that the reason they usually aren't is that nobody designed them that way. That claim applies equally to a community loan book and to a portfolio of solar PPAs — which is why the venture runs more than one product line.

## 2\. Product lines

Tracked in data/product-lines.csv.

|  | PL-1 — Community credit & insurance | PL-2 — Agrivoltaic project finance (BFAV) |
| :---- | :---- | :---- |
| Origination layer | VSLAs, MFIs, NGOs, employer networks | Farmers / landholders via our project vehicle |
| Underlying cash flow | Loan repayments, insurance premiums | PPA revenue from the utility |
| Tenor | Months | 15–25 years |
| Counterparty | Many small, socially enforced | One utility, monopsony |
| Hard part | Data capture and standardization | Permitting, offtake terms, concentration |
| Precedent | LIT-004, LIT-006 | LIT-008 |
| Evidence base | Strong (LIT-001/002/003/007) | Thin — no equivalent impact literature yet |
| Document | product-lines/community-credit-and-insurance.md | product-lines/agrivoltaic-project-finance.md |

**Why they belong together.** Beyond sharing the thesis, they share the *toolkit* — the data schema, underwriting engine, monitoring system and waterfall models in §5 are largely asset-agnostic. Building them twice would be waste.

And they are close to uncorrelated. A community loan book and a portfolio of utility PPAs have almost no shared risk driver: different obligors, different macro exposure, different failure modes. That is exactly the diversification the SDS plan argued for, and neither line achieves it alone — PL-2 in particular is only superficially diversified, since many small projects still face one offtaker and one regulator.

Whether that means they should share a *vehicle* is a separate question — investors and rating agencies generally prefer homogeneous pools, and mixing an unproven asset class with a legible one may contaminate the legible one. **Resolved (OQ-8, 2026-08-02): keep separate homogeneous pools**, and capture the PL-1/PL-2 diversification at the fund/investor level rather than inside one pool.

**Sequencing.** PL-1 leads, because it carries the research programme and the PhD, and because its evidence base is real. PL-2 is closer to revenue and has a cleaner asset, so it may well produce the first pooled structure. They are not competing for the same milestone.

## 3\. Three-layer structure

| Layer | Who | What they do |
| :---- | :---- | :---- |
| **Origination** | PL-1: VSLAs, NGOs, MFIs, employer networks · PL-2: farmers/landholders, EPC subcontractors | KYC, disbursement, collections, claims, construction, local compliance |
| **Risk (our layer)** | Us | Underwriting rules, monitoring dashboards, early-warning systems, risk-sharing/tranching design, first-loss structuring |
| **Product** | Joint | Loans, insurance, bundled products, project equity/debt — priced using origination data |

We sit in the structuring layer deliberately. Regulated entities handle origination, claims, collections and compliance; we are asset-light and do not seek a licence in the first phase.

**Target end state:** investment-grade tranches sellable to institutional investors, with DFI/philanthropic capital absorbing first-loss/junior risk and private capital in mezzanine and senior.

## 4\. Revenue model

1. **Structuring and servicing fees** on pools we assemble and monitor.  
2. **Retained economic interest** in the pools — which is not optional: EU/UK risk-retention rules require the originator/sponsor to hold a minimum economic interest if senior notes are placed with those investors (see literature/notes/memo-3-securitization-blended-finance.md).  
3. **Data/analytics licensing** to originators and funders once the underwriting engine has a track record.

The earlier Web3 plan's "non-voting investor in the VSLA" model is preserved in substance by (2): we take return on capital without taking governance control of the group.

## 5\. Toolkit to build

1. Standardized data schema for loans/insurance — ABS-data-tape-ready (→ OQ-3)  
2. Underwriting engine — rules-based plus ML scoring incorporating community signals  
3. Monitoring & early-warning system — DPD tracking, delinquency/claim pattern alerts  
4. Impact evaluation module — randomization infrastructure, pre-registered designs with academic partners  
5. Securitization modelling — cash-flow waterfall models, loss/prepayment simulations

## 6\. Market and pilot direction

**Two candidate first sites.**

- **Israel (migrant-worker communities)** — logistical proximity, easier hands-on project management, existing regulatory environment around foreign-worker insurance. A controlled environment in which to develop the research protocol and tooling.  
- **Africa (multi-country VSLA networks)** — deep traditions of community-based finance, high financial exclusion, alignment with blended-finance/SDG capital mobilization narratives, and a nascent securitization market that offers first-mover advantage in standard-setting.

**Working decision:** anchor methodology development in Israel first, then replicate in an African country as a second field site once the framework is proven. Final decision pending contact/access assessment.

## 7\. Structuring assumptions (evidence-backed)

Derived from the literature review; see Memo 3 for sources.

| Assumption | Working value | Basis |
| :---- | :---- | :---- |
| First-loss / junior tranche size | 10–20% of structure | LIT-013, LIT-015 |
| Pilot warehouse size | Tens of millions USD, DFI-anchored | LIT-011, LIT-012 |
| Public issuance threshold | ≥ USD 100m | LIT-012 |
| Originator structure | Multi-originator, plausibly regional | LIT-008, LIT-011 |
| Track record before first tranche | 2–3 years of clean repayment data | LIT-004, LIT-006 |

These are starting ranges to be tested, not targets. Each is an observed central tendency across deals that do not closely resemble our asset class.

## 8\. Risks

| Category | Risk | Mitigation |
| :---- | :---- | :---- |
| Market | No investor appetite for a novel asset class at pilot scale | Anchor investor secured before structuring; frame first vehicle as a blended fund, not a public ABS |
| Financial | FX exposure between local-currency receivables and hard-currency notes | Hedging or local-currency tranches; DFI guarantees for FX risk |
| Financial | Interest-rate mismatch across the waterfall | Match funding tenor to asset tenor at structuring |
| Credit | Community portfolios underperform relative to modelled loss curves | First-loss layer; conservative advance rates; early-warning monitoring |
| Legal | Cross-border transfer fails a true-sale test in one jurisdiction | Run the LIT-009 six-point checklist with local counsel **before** committing to a geography (→ OQ-1) |
| Regulatory | Origination partner loses licence or falls foul of local rules | Partner diligence; multi-originator structure limits single-partner exposure |
| Operational | Origination data quality too poor to underwrite | Schema and data capture designed at origination, not retrofitted (→ OQ-3) |
| Reputational | Impact claims outrun the evidence base | Frame around resilience/smoothing, which the evidence supports (Memo 2\) |

## 9\. Open work

Tracked in data/milestones.csv and data/open-questions.csv. The near-term critical path:

1. Draft the canonical data schema (OQ-3) — blocks everything downstream.  
2. Jurisdiction scan with counsel (OQ-1) — blocks pilot site selection.  
3. First originator and verification partner conversations (M-03, M-04).  
4. Choose the first instrument: loan vs insurance vs bundled.

## 10\. Not yet drafted

Sections carried forward from the earlier plans that still need work, listed so the gaps stay visible:

- Financial plan — cost structure, revenue projections, funding ask  
- Organization & management — team structure, hiring sequence  
- Competitive analysis — who else is structuring community-originated assets  
- Marketing/BD strategy — how originator partners are actually reached  
- Legal structure of the operating company itself

