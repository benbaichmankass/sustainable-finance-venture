# Business research — collective finance, risk intermediation and securitisation readiness

**Status:** Live research unit · **Owner:** BB · **Opened:** 2026-10-08 · **Synced with Drive** (editable either side; see `docs/ops/drive-sync.md`) · **Trackers:** `data/collective-market-map.csv` (CMM), `data/collective-products.csv` (CPR), `data/risk-allocation.csv` (RA) · **Method:** `docs/research/methodology-collective-screening.md` · **Model:** RT-7 · **Dashboard:** the *Business research* tab

> **How this doc works.** It is the narrative home of the business-research unit and it has a Google Doc twin for working on a phone or with a collaborator. Write here or there. The three trackers are the structured record: a finding about an organisation, a product or a risk goes in a tracker row with an evidence reference, and this doc points at it. Under the repo's single-source rule the Master Reference Tracker Sheet mirrors the trackers; if they disagree, the repo wins.
>
> **Provenance.** This unit was opened from the research plan that came in with the RT-7 prototype on 2026-10-07 (`archive/prototype-2026-10/collective-finance-research-plan.md`). Three things changed in the move: the plan's three Sheet tabs became repo trackers; Vietnam is held as a modelling case rather than a pilot setting (decision 2026-10-08, with OQ-22 still open); and securitisation is treated as a design constraint on today's products rather than a pilot objective (decision register, 2026-09-09).

---

## 1. The question

**Which collective institutions can originate, monitor, aggregate, hedge and service member-level risks well enough to support external risk-sharing and, eventually, investable, securitisable cash-flow pools?**

Sub-questions, each with a home:

| # | Sub-question | Answered in |
|---|---|---|
| 1 | What collectives exist, in which sectors, geographies and legal forms? | Market map (CMM), `Entity_Type`, `Legal_Form` |
| 2 | What financial and non-financial services do they provide members? | Market map, `Services_Provided` |
| 3 | How do they finance those services today? | Market map, `Existing_Funders`; products (CPR), `Funding_Source` |
| 4 | Which lenders, insurers, buyers, exporters, fintechs, asset managers and DFIs support them? | Market map rows of those types |
| 5 | Which risks remain unpriced, unhedged, poorly monitored or inefficiently retained? | Risk allocation (RA) |
| 6 | Which risks can SFV measure, price, absorb, reduce or transfer uniquely? | Risk allocation, `Potential_SFV_Intervention`; RT-7 sensitivities |
| 7 | What data, governance, legal rights and servicing capacity make a collective securitisation-ready? | The screening scorecard |

## 2. Working hypothesis

Collectives reduce information asymmetry and servicing cost through local knowledge, peer monitoring, aggregation, recurring transactions, marketing relationships and payment control. Most external capital providers nonetheless underwrite them as opaque single borrowers rather than decomposing member, climate, price, delivery, liquidity, governance and collateral risk.

SFV's role is therefore not to supply lending capital. It is to build the **risk infrastructure** that makes collective cash flows measurable, comparable, hedgeable and financeable: the collective risk operating system, standardised risk-sharing contracts, and the readiness standard. This is Lane A, B and D of the practice in `docs/venture/solo-operator-track.md`, with the collective as the client type.

What the evidence already says about the hypothesis, from the literature matrix:

- The cooperative-as-lender-of-record structure exists at scale (Root Capital, LIT-031: more than USD 900m disbursed since 1999; enterprises on-lend and bear repayment risk). Its data quality is the known weak point: internal credit funds are "often informal and unregulated", and weak internal controls are the most common deficiency. **The thesis restated as a field risk.**
- Member registers are obtainable through unions and the government cooperatives agency, and have been used as a probability sampling frame (Sidama, LIT-033). **The longlist is buildable.**
- Coffee is close to a worst case for correlation: leaf rust across more than half of Central America's coffee area in one event (LIT-031); price flagged excessively variable on 45 of 260 days in 2019/20 (LIT-035). **Hardest case for poolability, best case for measuring correlation** (Memo 9).
- Certification does not reliably move household income (LIT-032, LIT-034). **Do not build a welfare claim on the certification premium**; use certification records as a data asset instead (EXP-11).

## 3. Collective typology

| Collective type | Core purpose | Member financial role | Relevance here |
|---|---|---|---|
| Producer or marketing cooperative | Aggregate output, quality, processing, sales | Harvest advances, input credit, payment on delivery, retained patronage | Strong fit for receivables and forward-sale structures |
| Savings group / VSLA | Savings, internal loans, emergency support | Member-funded short loans and a social fund | Strong local screening; small tickets; the PL-1 origin |
| SACCO / credit union | Member savings and credit | Deposits, working capital, asset loans, insurance links | Direct origination and servicing channel |
| Farmer producer organisation | Representation, extension, procurement, marketing | Often brokers finance | Distribution, data and aggregation layer |
| Cooperative union / federation | Aggregate primary cooperatives | Bulk purchasing, export and processing finance, guarantees | Regional pooling and structured-finance counterparty |
| Mutual guarantee association | Shared guarantee | Guarantees, reserves, peer screening | A natural first-loss or partial-guarantee mechanism |
| Platform-enabled network | Digital aggregation of farmers, buyers, lenders, insurers | Payments, scoring, embedded credit | Data and servicing partner; data rights need care |

The market map's `Entity_Type` uses this list, plus the provider types (specialist lender, bank or MFI, buyer or exporter, insurer, investor or fund, government or DFI program), so a longlist can hold the whole ecosystem of a region in one table.

## 4. Products and cash flows

Every product row in `data/collective-products.csv` maps to a cash-flow chain and, where RT-7 models it, to the parameters it would calibrate (`RT7_Mapping`):

| Product | Borrower | Repayment source | Main risks | RT-7 leg |
|---|---|---|---|---|
| Seasonal input credit | Member | Harvest proceeds | Yield, price, timing, side-selling | OpEx loan; DSCR; side-selling |
| Harvest procurement finance | Cooperative | Buyer or export receivables | Buyer delay, volume, quality, FX | Forward book; shortfall cost; (buyer delay and FX not yet modelled: RA-07, RA-08) |
| Asset finance | Member or cooperative | Incremental revenue or cost savings | Utilisation, asset performance, collateral recovery | CapEx loan; `lgd_capex` |
| Processing or storage CapEx | Cooperative | Processing or export margin | Throughput, energy, demand, operations | Not modelled |
| Warehouse or inventory finance | Cooperative or trader | Sale of stored commodity | Warehouse integrity, title, quality, price | Not modelled |
| Marketing advance | Member | Delivery to the collective | Delivery, quality, side-selling | Side-selling channel |
| Savings or social-fund loan | Member | Household or business cash flow | Idiosyncratic shocks, group liquidity | The PL-1 toolchain (RT-2, RT-3) |
| Insurance premium finance | Member or cooperative | Harvest or recurring cash flow | Climate event, basis risk, premium non-payment | Not modelled until OQ-25 settles insurance scope |

## 5. Where the market fails

**Fragmented underwriting.** Lenders assess a collective as one borrower. The risk-allocation tracker records, per risk, who holds it today, through what mechanism, who is left with the residual, and how observable and well priced it is. The ten RA rows seeded on 2026-10-08 are RT-7's own allocation: what the *model* assumes about who holds each risk. They are marked `Basis: RT-7 v0.2 assumption` and exist to be contradicted by the first partner deep dive.

**Seasonal liquidity mismatch.** Collectives need cash at harvest to buy members' crop and receive export proceeds later. The timing gap, its bridge finance today and its cost are deep-dive fields.

**Credit and risk transfer are structured separately.** Operating loans, climate triggers, price floors, delivery commitments, collection-account control, buyer receivables and group reserves are rarely designed together. RT-7 is the first place in this repo where they sit in one loss chain, and its first finding is that the delivery channel, not credit, drives the tail.

**Data not translated into underwriting.** Repayment history, delivery data, quality scores, savings records, attendance and agronomic data exist inside collectives and are not auditable risk features. The data-availability fields and the `data-catalog.csv` rows DS-07 and DS-08 are where that mapping goes.

**No standardisation.** Definitions, eligibility, reporting, loss waterfalls, reserve policy, audit trails. RT-1 is the origination half of that standard; the readiness scorecard is the institutional half.

## 6. Value hypotheses to test

| # | Hypothesis | Test | Where it lives |
|---|---|---|---|
| 1 | **Collective risk operating system**: member PD/LGD/EAD, crop-calendar repayment design, asset and collateral monitoring, climate and price stress tests, delivery-risk model, governance scorecard | Does it reduce external capital providers' uncertainty enough to improve tenor, pricing, collateral or approval? | RT-1, RT-2, RT-3, RT-7; Lane A diagnostics |
| 2 | **Parametric resilience layer**: index cover for systemic climate events over a collective reserve, with an excess-of-loss layer and reinsurance for the remote tail | Does structured protection lower expected tail loss and improve bankability? | RT-7 climate factor (one-line addition); gated on OQ-25 |
| 3 | **Forward-sale and receivables structure**: validated offtake, modelled volume and basis, buyer payments into controlled collection accounts, advances against eligible receivables | Can verified contracts and cash-flow control replace hard collateral? | RT-7 forward book and side-selling; CPR-02 |
| 4 | **Standardised risk-sharing contracts**: partial guarantees, portfolio excess-of-loss, first-loss reserve facilities, mezzanine notes, collateral-value protection, servicing-performance incentives | Which layer do originators and funders want, while preserving collective incentives? | RT-7 tranche cut and attachment search; Lane B design mandates |
| 5 | **Securitisation-readiness service**: tape standards, eligibility, data-quality tests, concentration and correlation limits, reserve and waterfall rules, stress packs, investor reporting, audit trail | Which collective types can meet the minimum thresholds? | The screening scorecard; RT-1; Lane D |

## 7. Research sequence

| Phase | Does | Output |
|---|---|---|
| **1. Desk mapping** | Longlist collective types and providers in the pilot settings; one source-backed row per entity and product; 3–5 priority organisations per country | Market map and product rows at `Longlist` or `Desk reviewed` |
| **2. Organisational deep dives** | Legal form, governance, members, services, the full cash-flow cycle from input purchase to member settlement, funding, performance history, buyer contracts, warehouse arrangements, price-risk management | Rows at `Deep dive`; new literature rows where a document is public |
| **3. Risk and data audit** | Every material risk in the member-to-buyer chain, its owner and residual holder, what data exist and under what consent; score the scorecard; find the smallest intervention that materially improves underwriting | RA rows per partner; scored CMM rows |
| **4. Product design** | One narrow, testable risk layer per partner: trigger, attachment, pricing logic, exclusions, data requirements, servicing duties, alignment mechanisms | A product-line doc or a new PL row; RT-7 run on the partner's parameters |
| **5. Pilot-partnership design** | The minimum partner configuration: collective + local originator + buyer where relevant + insurer or risk-capital provider + SFV's risk, data and structuring layer; who originates, services, controls collections, bears first loss, reports | Partner rows; milestones |
| **6. Portfolio transition** | Only after single-collective structures are validated: standardise fields, simulate many collectives per region, model within-region climate and cross-region price correlation, pool, test reserve and tranche structures, pick the first external-capital structure | RT-7 Phase 4 (EXP-27); RT-5 waterfall; OQ-18 |

**Pilot settings.** Colombia (Huila/Cauca) and Ethiopia (Jimma/Sidama) are the two settings with literature anchors and a regional case for the market scan's East Africa recommendation. Vietnam (Dak Lak/Lam Dong) is carried in RT-7 as a modelling case, because a Robusta origin gives the cross-region price factor a genuinely different series; it is not a market candidate until OQ-22 says so.

**The first prototype is narrow by design:** seasonal operating and harvest-procurement finance, supported by verifiable buyer contracts and controlled payment flows, with a defined climate-linked or portfolio-loss risk layer. Not a securitisation. Begin by validating that the collective can generate reliable data, service the facility, control key cash flows, manage delivery incentives and sustain acceptable loss performance.

## 8. Decision gates

| Gate | Question | Minimum evidence |
|---|---|---|
| **1** | Is the collective a viable operating partner? | Legitimate organisation and governance; member and product relevance; sufficient scale; willingness and capacity to share anonymised performance data; clear member benefit and safeguards |
| **2** | Is there a financeable cash-flow structure? | Identifiable repayment or buyer-payment source; credible servicing and collection; defined collateral, receivables, delivery or payment-control rights; manageable seasonal liquidity mismatch |
| **3** | Is there a priceable risk layer? | Observable exposure and loss trigger; a plausible historical proxy or scenario calibration; a willing risk holder or transfer counterparty; a premium compatible with the underlying economics |
| **4** | Is the collective portfolio-ready? | Standard data tape and reporting; reliable eligibility rules; servicing controls; understood correlation and concentration; a clear legal and regulatory path for the structure |

Gates 2 and 3 are what RT-7's outputs are organised around: EL, UL and the stress table for Gate 2, the sensitivities and the attachment search for Gate 3. Gate 4 is the securitisation-design constraint kept on today's products without being a pilot objective.

## 9. Governance principles

- Separate **observed data** from assumptions, expert judgement and scenario parameters (`docs/ops/data-provenance.md`).
- Participation in a collective is not proof of creditworthiness.
- Evaluate member impact: affordability, coercion, exclusion, asset repossession, debt stress. RT-7 treats household consumption as senior to debt service for this reason.
- Consent and data rights before any member-level information is used; row-level data never enters the repo.
- Originator, collective and external capital each bear the risks they can influence.
- Securitisation is a possible later-stage financing tool, not an end in itself.

## 10. Immediate next actions

1. Country longlists for Colombia and Ethiopia: one market-map row per organisation, with a source. The four rows seeded from the matrix are the start, not the longlist.
2. Select 3–5 deep-dive targets per country and set `Research_Status` accordingly.
3. Score nothing until a deep dive; then score, and check whether the band cutoffs separate anything.
4. Translate the first deep dive into RT-7 parameters and record each promotion from `assumption` in the parameter tracker.
5. Decide the allocation of forward-book risk between buyer, collective and lender (RA-05); it is the model's largest open question and a contract-drafting question, not a modelling one.

## Open questions this unit feeds

OQ-13 (attach one level up), OQ-18 (does a multi-originator pool diversify on the right axis), OQ-22 (first market), OQ-25 (product lines in scope, insurance), OQ-7 (verification partners), OQ-3 (origination schema against cooperative records).
