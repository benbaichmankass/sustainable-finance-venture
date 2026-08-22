# Literature review

> **This file is generated.** Do not edit it. It is assembled from
> `literature/lit-matrix.csv`, `data/lit-components.csv` and
> `data/synthesis-memos.csv` by `scripts/build_lit_review.py`.
> Change a tracker and regenerate; editing here would create a second
> source of truth, which is the thing this repo exists to avoid.

It exists because the review is correctly stored in four places and
readable in none of them. Gaps are shown as gaps: a component with no
anchors says so, and a memo that has not been written says so. How much
of the review is *not* done is the most useful thing this document says.

## Where the review stands

| | |
|---|---|
| Anchors logged | **44** (37 reviewed, 7 to read) |
| Components | 26, covering 206 target anchor slots, 55 filled |
| Component status | In progress 2 · Not started 9 · Partially covered 15 |
| Synthesis memos | Reviewed 3 · Drafted 3 · Outline 3 |

## What is still unread

Ordered by priority, then by how empty the component is. This is the
reading list; everything below it is what has been read so far.

| Component | Priority | Status | Filled | Target | Memo |
|---|---|---|---|---|---|
| **LC-02** Group-lending mechanisms: information, sanction, repeat interaction | P1 | Partially covered | 4 | 12 | MEMO-4 |
| **LC-03** Index and parametric insurance: demand, basis risk, impact | P1 | Partially covered | 4 | 12 | MEMO-5 |
| **LC-05** Resilience and consumption-smoothing outcome measurement | P1 | In progress | 1 | 8 | MEMO-5 |
| **LC-06** Climate and adaptation finance: gap sizing and instruments | P1 | In progress | 1 | 8 | MEMO-6 |
| **LC-09** Securitisation eligibility, data tapes and rating criteria | P1 | Partially covered | 3 | 10 | MEMO-7 |
| **LC-01** Savings groups and community finance institutions | P1 | Partially covered | 4 | 10 | MEMO-1 (extend) |
| **LC-04** Bundled credit and insurance: theory and evidence | P1 | Partially covered | 4 | 10 | MEMO-5 |
| **LC-07** Credit-risk modelling in thin-data settings | P1 | Partially covered | 5 | 10 | MEMO-7 |
| **LC-24** Coffee-sector economics and cooperative finance | P1 | Partially covered | 5 | 8 | MEMO-9 |
| **LC-08** Portfolio correlation and covariate risk in microfinance | P1 | Partially covered | 6 | 8 | MEMO-7 |
| **LC-13** Microcredit impact evidence and the meta-analytic record | P2 | Partially covered | 1 | 10 | MEMO-4 |
| **LC-14** Digital financial rails and origination data capture | P2 | Not started | 0 | 8 | MEMO-9 |
| **LC-16** Agricultural value chains, warehouse receipts and price risk | P2 | Not started | 0 | 8 | MEMO-9 |
| **LC-18** Financialisation of community institutions | P2 | Partially covered | 1 | 8 | MEMO-4 |
| **LC-10** Securitisation law, true sale and SPV domicile | P2 | Partially covered | 2 | 8 | MEMO-8 |
| **LC-17** Over-indebtedness, consumer protection and credit ethics | P2 | Not started | 0 | 6 | MEMO-4 |
| **LC-11** African and emerging-market capital-market depth | P2 | Partially covered | 3 | 8 | MEMO-8 |
| **LC-15** PAYGO and energy-access receivables finance | P2 | Not started | 1 | 6 | MEMO-9 |
| **LC-19** Regulation of savings groups and microinsurance | P2 | Partially covered | 1 | 6 | MEMO-8 |
| **LC-20** Microfinance cost-to-serve and unit economics | P2 | Partially covered | 2 | 6 | MEMO-9 |
| **LC-26** Impact-evaluation method advances | P3 | Not started | 0 | 8 | MEMO-6 |
| **LC-21** Microsavings and household financial behaviour | P3 | Not started | 0 | 6 | MEMO-4 |
| **LC-23** Gender, group composition and intra-household allocation | P3 | Not started | 0 | 6 | MEMO-4 |
| **LC-22** Remittances and migrant financial arrangements | P3 | Not started | 0 | 5 | MEMO-9 |
| **LC-25** Data governance, consent and privacy in field research | P3 | Not started | 0 | 5 | MEMO-9 |

## Synthesis memos

The memos are where anchors become an argument. A component with anchors
but no memo prose is evidence that has not been synthesised yet.

### MEMO-1 — What VSLAs and similar structures actually achieve

**Status:** Reviewed · **Fed by:** LC-01 (4 anchor slots) · [`literature/notes/memo-1-vslas.md`](../../literature/notes/memo-1-vslas.md)

The VSLA/savings-group model is empirically the most de-risked starting point: cluster-RCT evidence (Ksoll et al. 2016) and cross-country synthesis show consistent, replicable gains in savings and resilience. Group cycles already generate structured, periodic data - the natural first data source for underwriting and eventual securitization. CGAP's proportionate-regulation guidance (LIT-014) means the data spine we need aligns with where savings-group policy is already heading: light-touch registration plus digitised group records. Recommend an Israel migrant-worker pilot to test data capture and parametric triggers before Africa scale-up. Extended 2026-08-07 with the group-level lending precedent for OQ-13: India's SHG-Bank Linkage Programme has financed collectives that on-lend to members since 1992, so the structure is proven at scale - but NPAs on the bank SHG portfolio rose from a steady 2.9% (March 2009 and 2010) to 4.72% by March 2011, worse in the subsidised SGSY component, with deterioration tracking target-driven group formation rather than the structure itself (LIT-023). Counterweight: the longest-running successful joint-liability institution, the 19th-century German rural credit cooperative, financed its loans from local deposits rather than external wholesale funding (LIT-022).

### MEMO-2 — What microfinance RCTs and reviews say about impact and design

**Status:** Reviewed · **Fed by:** — (0 anchor slots) · [`literature/notes/memo-2-microfinance-impact.md`](../../literature/notes/memo-2-microfinance-impact.md)

Microfinance systematic reviews show average income/poverty effects are small and heterogeneous, but effects on consumption smoothing and female empowerment are more robust. Implication: do not oversell income/business growth claims to investors; frame the product around resilience/smoothing outcomes, which have the strongest evidence base and are easiest to verify for impact reporting and securitization covenants. This is an alignment rather than a concession - investors underwrite cash-flow regularity, which is exactly what the resilience evidence speaks to. Extended 2026-08-07 with the repayment-MECHANISM evidence for OQ-12: the joint-liability contract is not the active ingredient (LIT-020 found no repayment effect when 169 Philippine centres were converted to individual liability), while repeat interaction is a strong candidate for what is (LIT-021: randomised first-cycle meeting frequency, later equalised, left monthly-meeting clients four times more likely to default on the second loan, via informal risk-sharing, in individual-liability groups). LIT-022 supplies the screening/monitoring/enforcement/audit taxonomy and shows information and sanction channels can trade off. Implication: underwrite the group's social structure, not its liability terms - and note that no study here tests the case where the creditor is an outside investor rather than the community, which is precisely what securitisation creates.

### MEMO-3 — How securitization/blended finance has been applied to microfinance

**Status:** Reviewed · **Fed by:** — (0 anchor slots) · [`literature/notes/memo-3-securitization-blended-finance.md`](../../literature/notes/memo-3-securitization-blended-finance.md)

Securitization of community/microfinance assets is feasible but nascent: existing models all required a standardization layer, credit enhancement/first-loss, and an anchor investor before market-rate tranches were sellable. New anchors add three concrete design parameters: a six-point legal checklist for cross-border true sale (LIT-009/010); a size band of tens of millions warehoused scaling to >=USD 100m for issuance (LIT-011/012); and a first-loss tranche in the 10-20% range with a documented additionality and tapering story (LIT-013/015). Design the data schema and underwriting rules from day one to match ABS eligibility criteria. Economics anchors added 2026-08-02 for RT-6/OQ-10: MIV total expense ratio ~2.4% and Fixed-Income fund fee 1.2% with a 7.6% senior yield (LIT-017), and a concessional-to-private mobilisation ratio of ~1.8x with guarantees the strongest lever (LIT-018/019).

### MEMO-4 — The repayment mechanism and its critics

**Status:** Outline · **Fed by:** LC-02, LC-13, LC-17, LC-18, LC-21, LC-23 (6 anchor slots) · [`literature/notes/memo-4-the-repayment-mechanism-and-its-critics.md`](../../literature/notes/memo-4-the-repayment-mechanism-and-its-critics.md)

Scope: what actually drives repayment in community lending, and what the critical literature says happens when external capital enters member-owned institutions. Carries OQ-12 and OQ-13. Not yet drafted.

### MEMO-5 — Insurance, bundling, and what resilience means

**Status:** Drafted · **Fed by:** LC-03, LC-04, LC-05 (9 anchor slots) · [`literature/notes/memo-5-insurance-bundling-resilience.md`](../../literature/notes/memo-5-insurance-bundling-resilience.md)

PARTIAL - LC-04 and LC-03 read, LC-05 outstanding; all seven sources verified from abstracts or publisher summary pages, not full texts. BUNDLING (LC-04): not untested. Compulsory bundling suppressed demand in two RCTs - Gine & Yang 2009 Malawi (take-up 13 points lower off a 33.0% base) and Banerjee, Duflo & Hornbeck 2014 India (16 point, 23 percent rise in drop-out, measured on the lender's book). Karlan et al. 2014 Ghana is the counterweight: uninsured risk rather than capital binds, and demand for SEPARATELY offered cover is strong. The reconciling distinction is offered-separately versus compulsorily-priced-into-the-loan. INDEX INSURANCE (LC-03) compounds it: Carter et al. 2017 report take-up disappointingly low WITHOUT LARGE AND SUSTAINED SUBSIDIES; Clarke 2016 shows low demand can be RATIONAL under basis risk (optimal demand zero for the infinitely risk-averse, nonmonotonic in risk aversion, wealth and price); Jensen et al. 2018 measures basis risk directly and finds it and spatiotemporal adverse selection drive demand - the latter also a warning for the pool's loss distribution, so cross-referenced to LC-08. CONSEQUENCES: the proposal's novelty claim is false as written (OQ-17), EXP-01 is on the wrong side of the subsidy variable, EXP-17 becomes the centrepiece with its subsidised arm carrying the strongest prior, EXP-30's basis-risk premise is supported, and RT-6 cannot treat bundling as retention-neutral.

### MEMO-6 — The climate financing gap and how to measure a response

**Status:** Outline · **Fed by:** LC-06, LC-26 (1 anchor slot) · [`literature/notes/memo-6-the-climate-financing-gap-and-how-to-measure-a-response.md`](../../literature/notes/memo-6-the-climate-financing-gap-and-how-to-measure-a-response.md)

Scope: authoritative adaptation and energy-access gap estimates, and the impact-evaluation methods needed to credibly measure a response. P1. Not yet drafted.

### MEMO-7 — Can these cash flows be modelled

**Status:** Drafted · **Fed by:** LC-07, LC-08, LC-09 (14 anchor slots) · [`literature/notes/memo-7-can-these-cash-flows-be-modelled.md`](../../literature/notes/memo-7-can-these-cash-flows-be-modelled.md)

Drafted 2026-08-22, covering LC-07, LC-08 and LC-09. THE ANSWER: yes these cash flows can be modelled, but the binding constraint is not the modelling. Three constraints sit in front of it - the data does not exist in most originators (LIT-031, LIT-044); the correlation parameter is unknown and is the input doing most of the work in every available method (LIT-038, LIT-041); and validation cannot rescue you from that, because correlation defeats the tests (LIT-041). SPECIFICATION IS SETTLED (LIT-043): discrete-time hazard with an explicit baseline, competing risks, left-truncation, public R codebase - and the rationale transfers exactly, because a community repayment book IS a discrete-time process, so this is the natural form rather than an approximation. CORRELATION REACHED BY THREE INDEPENDENT ROUTES: the method takes it as an assumed input; the crisis record says it is large and institutional rather than macro (LIT-036 rejects the global recession outright, LIT-037 finds market-level penetration predicts trouble while individual lender growth does not); and Basel says tests built on independence are so conservative that well-calibrated systems fail them while correlation-aware tests catch only obvious miscalibration. LGD: four routes, of which implied historical is the only retail one, and its validation 'relies essentially on the validation of the PDs used' - it inherits the whole problem. MODEL RISK: SR 11-7 warns that an extreme point on a misspecified distribution is not conservative, which is the Pluto-Tasche bound exactly, so RT-5's sweep stays and no point estimate is published. PRACTITIONER CONSTRAINT: a judgmental scorecard RANKS risk; only a statistical model PRICES it, so closing the rank-to-price gap is the work. FOUR NAMED GAPS remain: small-sample corrections, LGD with few recoveries, rating-agency correlation assumptions for EM consumer pools, and any published loss data on cooperative internal credit funds - which may not exist publicly at all.

### MEMO-8 — Legal and market preconditions

**Status:** Outline · **Fed by:** LC-10, LC-11, LC-12, LC-19 (13 anchor slots) · [`literature/notes/memo-8-legal-and-market-preconditions.md`](../../literature/notes/memo-8-legal-and-market-preconditions.md)

Scope: true sale and SPV structuring across candidate jurisdictions, African and EM capital-market depth, and the regulation of savings groups and microinsurance. Not yet drafted.

### MEMO-9 — Sector and infrastructure notes

**Status:** Drafted · **Fed by:** LC-14, LC-15, LC-16, LC-20, LC-22, LC-24, LC-25 (8 anchor slots) · [`literature/notes/memo-9-sector-and-infrastructure-notes.md`](../../literature/notes/memo-9-sector-and-infrastructure-notes.md)

LC-24 section written 2026-08-22; the rest still outline. VERDICT ON THE COFFEE BET: it survives on both assumptions it was made on, but the risk moves rather than disappearing. (1) Cooperatives DO intermediate credit - LIT-031 has Root Capital stating that borrower enterprises on-lend to individual producers, bear the repayment risk, and run origination, disbursement, monitoring and repayment through an internal credit fund. That fund is the cash-flow object this project exists to make legible. (2) Member registers DO work as a sampling frame - LIT-033 compiled the cooperative and certification map from the Cooperatives Agency and the union, then sampled 20 cooperatives and 530 households proportional to membership; Sidama alone holds about 57 primary cooperatives and 85,000 farmers. (3) BUT certification cannot carry the welfare claim: LIT-032 (43 studies, no RCTs anywhere in the literature) finds price +14% and produce income +11% significant, while TOTAL household income is +6% and NOT significant, and worker wages are -13% and significant; LIT-034 replicates the null on household income across three continents. (4) THE UNASKED FINDING: coffee is close to a worst case for correlation. Leaf rust hit more than half of Central America's coffee area at once, cut El Salvador production 60%, and drove 80% output drops at some financed producer organisations; LIT-035 adds price, with 45 of 260 days flagged excessively variable in 2019/20. Two covariate shocks, both regional or global. That is the hardest case for poolability and the best case for MEASURING correlation - which of those the project wants is OQ-17's business, not an inheritance. Colombia's Coffee Price Stabilization Fund (Feb 2020) is a live sovereign comparator for EXP-09 and a displacement risk under OQ-11. Also notable for underwriting: LIT-031 discloses NO repayment, default or portfolio-at-risk figure, and public loss data on cooperative internal credit funds may simply not exist.

## The evidence, by axis

---

## Axis 1-VSLA

### LC-01 — Savings groups and community finance institutions

**P1** · **Partially covered** · 4 of 10 anchors · feeds MEMO-1 (extend)

**Why it matters.** The origination layer itself. Everything downstream assumes these institutions are durable and that their behaviour is characterisable; the matrix supports the first claim better than the second.

**Questions.** How durable are savings groups over multiple cycles? What is the institutional taxonomy (VSLA, ROSCA, ASCA, SHG, cooperative) and how do the forms differ in governance and cash-flow behaviour? What are the documented failure modes?

#### LIT-001 — Ksoll et al. 2016 - Impact of Village Savings and Loan Associations

**Reviewed** · RCT · Sub-Saharan Africa

*Rural households in VSLA programs*

**Findings.** Cluster RCT (46 villages, Malawi); positive intent-to-treat effects on savings and consumption smoothing; modest effects on business investment/income

**Limitations.** ITT dilutes true effect due to partial compliance; single-country context limits external validity

**What it opens.** Does the effect persist beyond the 1-2 year RCT window, and does it survive withdrawal of NGO support?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=Ksoll+et+al.+2016+-+Impact+of+Village+Savings+and+Loan+Associations) · relevance — product High, risk Medium, impact High

#### LIT-002 — Brannen 2016 - Evaluation of the impact of VSLAs

**Reviewed** · Evaluation review · Multi-country

*VSLA program participants*

**Findings.** Synthesis of VSLA/savings-group RCTs across countries; savings & resilience effects consistently positive; income/business effects mixed and smaller

**Limitations.** Heterogeneity across contexts complicates pooling; publication bias toward positive results

**What it opens.** What governance features drive the best outcomes, and which of them generalise across contexts?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=Brannen+2016+-+Evaluation+of+the+impact+of+VSLAs) · relevance — product Medium, risk Medium, impact High

#### LIT-014 — [CGAP 2025 - Regulating Savings Groups: Only a Proportionate Approach Will Work](https://www.cgap.org/blog/regulating-savings-groups-only-proportionate-approach-will-work)

**Reviewed** · Policy synthesis · East Africa (Tanzania, Uganda, Rwanda; generalisable)

*Savings-group regulators, NGOs and VSLA members*

**Findings.** Savings groups pose low systemic and AML/CFT risk but face consumer-protection and linkage challenges; argues for proportionate regulation built on voluntary or light-touch registration rather than full prudential rules; recommends delegating registration to local authorities, NGOs and federations and digitising group-level records to increase visibility and enable linkages to banks/MFIs and government support

**Limitations.** Blog-format synthesis rather than a formal evaluation; focuses on regulatory design rather than quantitative impact; evidence on fraud and consumer risk is anecdotal rather than systematically quantified

**What it opens.** What registration and data-collection model would both protect members and generate the digital, auditable data streams needed to underwrite VSLA-linked credit/insurance and eventual securitisation?

[open source](https://www.cgap.org/blog/regulating-savings-groups-only-proportionate-approach-will-work) · relevance — product High, risk Medium, impact High

#### LIT-023 — [Tankha 2012 - Banking on Self-help Groups: Twenty Years On (ACCESS Development Services / SAGE)](https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-paper-banking-on-self-help-groups-twenty-years-on-2012.pdf)

**Reviewed** · Programme review with portfolio data · India

*The SHG-Bank Linkage Programme (SBLP), begun by NABARD in 1992: banks lend to self-help groups of typically 10-20 women, which on-lend to their own members at rates the group sets*

**Findings.** The closest real-world precedent for lending to the collective rather than the individual, at national scale and over twenty years. Tankha describes the Indian SHG as 'effectively a micro bank as it raises equity and deposits, as well as external funds, and on-lends them' - the same one-level-up abstraction we are considering. Crucially the record is mixed rather than a clean success. NPAs on the bank SHG portfolio were 'steady at 2.9% in March 2009 and March 2010' but 'gone up substantially to 4.72% as on 31 March 2011', with commercial banks near 5% and cooperative banks near 7% at that date. The government-subsidised SGSY component performed worse, 'consistently over 5% in all the years and over 7% as on 31 March 2011', with commercial banks at 7.4%. The book links deterioration to target-driven growth and to concerns about the quality of groups promoted, and records that the predecessor IRDP programme suffered 'abysmally low recoveries over the years, being exacerbated by political decisions to waive loan repayments', leaving banks with unpaid loans.

**Limitations.** A programme review and secondary compilation, not an impact evaluation; no counterfactual, so deterioration cannot be causally attributed to the linkage structure itself rather than to the subsidy programmes running alongside it. Portfolio data ends at 31 March 2011, so it predates the 2010 Andhra Pradesh microfinance crisis aftermath and everything since; current NABARD figures were not verified here because the NABARD site returned HTTP 503 to automated retrieval. Indian SHGs are promoted, trained and often subsidised by NGOs and government in ways VSLAs typically are not, so the transfer to a VSLA setting is not one-to-one. Book-length source: the structure, NPA tables and waiver history were read; the majority of the volume was not.

**What it opens.** Anchors OQ-13. Shows the group-as-intermediary model is viable at scale but that its credit quality is not self-sustaining: it degraded when group formation was driven by capital deployment targets, and it is exposed to political waiver risk that is systemic rather than idiosyncratic and therefore not diversifiable by pooling within one country. Also implies the underwriting unit becomes the GROUP as an intermediary - its governance, vintage and record-keeping - which is an RT-1 and RT-2 consequence.

[open source](https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-paper-banking-on-self-help-groups-twenty-years-on-2012.pdf) · relevance — product High, risk High, impact Medium

### LC-18 — Financialisation of community institutions

**P2** · **Partially covered** · 1 of 8 anchors · feeds MEMO-4

**Why it matters.** The intellectual counterweight to the thesis. A proposal that does not engage the critique that external capital corrodes community institutions will be read as naive, and RQ-04 is built on taking it seriously.

**Questions.** What does the critical literature say about formalising informal finance? What is the record of external capital entering member-owned institutions? What happened to the SHG-Bank Linkage Programme and to microfinance commercialisation?

#### LIT-023 — [Tankha 2012 - Banking on Self-help Groups: Twenty Years On (ACCESS Development Services / SAGE)](https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-paper-banking-on-self-help-groups-twenty-years-on-2012.pdf)

**Reviewed** · Programme review with portfolio data · India

*The SHG-Bank Linkage Programme (SBLP), begun by NABARD in 1992: banks lend to self-help groups of typically 10-20 women, which on-lend to their own members at rates the group sets*

**Findings.** The closest real-world precedent for lending to the collective rather than the individual, at national scale and over twenty years. Tankha describes the Indian SHG as 'effectively a micro bank as it raises equity and deposits, as well as external funds, and on-lends them' - the same one-level-up abstraction we are considering. Crucially the record is mixed rather than a clean success. NPAs on the bank SHG portfolio were 'steady at 2.9% in March 2009 and March 2010' but 'gone up substantially to 4.72% as on 31 March 2011', with commercial banks near 5% and cooperative banks near 7% at that date. The government-subsidised SGSY component performed worse, 'consistently over 5% in all the years and over 7% as on 31 March 2011', with commercial banks at 7.4%. The book links deterioration to target-driven growth and to concerns about the quality of groups promoted, and records that the predecessor IRDP programme suffered 'abysmally low recoveries over the years, being exacerbated by political decisions to waive loan repayments', leaving banks with unpaid loans.

**Limitations.** A programme review and secondary compilation, not an impact evaluation; no counterfactual, so deterioration cannot be causally attributed to the linkage structure itself rather than to the subsidy programmes running alongside it. Portfolio data ends at 31 March 2011, so it predates the 2010 Andhra Pradesh microfinance crisis aftermath and everything since; current NABARD figures were not verified here because the NABARD site returned HTTP 503 to automated retrieval. Indian SHGs are promoted, trained and often subsidised by NGOs and government in ways VSLAs typically are not, so the transfer to a VSLA setting is not one-to-one. Book-length source: the structure, NPA tables and waiver history were read; the majority of the volume was not.

**What it opens.** Anchors OQ-13. Shows the group-as-intermediary model is viable at scale but that its credit quality is not self-sustaining: it degraded when group formation was driven by capital deployment targets, and it is exposed to political waiver risk that is systemic rather than idiosyncratic and therefore not diversifiable by pooling within one country. Also implies the underwriting unit becomes the GROUP as an intermediary - its governance, vintage and record-keeping - which is an RT-1 and RT-2 consequence.

[open source](https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-paper-banking-on-self-help-groups-twenty-years-on-2012.pdf) · relevance — product High, risk High, impact Medium

### LC-19 — Regulation of savings groups and microinsurance

**P2** · **Partially covered** · 1 of 6 anchors · feeds MEMO-8

**Why it matters.** Determines whether a product is legal before it is desirable, and sets the ceiling on what data can be demanded at origination.

**Questions.** How are savings groups regulated across candidate jurisdictions? What licensing does a microinsurance product require? Who may lawfully hold and share member data?

#### LIT-014 — [CGAP 2025 - Regulating Savings Groups: Only a Proportionate Approach Will Work](https://www.cgap.org/blog/regulating-savings-groups-only-proportionate-approach-will-work)

**Reviewed** · Policy synthesis · East Africa (Tanzania, Uganda, Rwanda; generalisable)

*Savings-group regulators, NGOs and VSLA members*

**Findings.** Savings groups pose low systemic and AML/CFT risk but face consumer-protection and linkage challenges; argues for proportionate regulation built on voluntary or light-touch registration rather than full prudential rules; recommends delegating registration to local authorities, NGOs and federations and digitising group-level records to increase visibility and enable linkages to banks/MFIs and government support

**Limitations.** Blog-format synthesis rather than a formal evaluation; focuses on regulatory design rather than quantitative impact; evidence on fraud and consumer risk is anecdotal rather than systematically quantified

**What it opens.** What registration and data-collection model would both protect members and generate the digital, auditable data streams needed to underwrite VSLA-linked credit/insurance and eventual securitisation?

[open source](https://www.cgap.org/blog/regulating-savings-groups-only-proportionate-approach-will-work) · relevance — product High, risk Medium, impact High

### LC-23 — Gender, group composition and intra-household allocation

**P3** · **Not started** · 0 of 6 anchors · feeds MEMO-4

**Why it matters.** Savings groups are predominantly women's institutions; a design that ignores intra-household bargaining will mis-measure its own outcomes.

**Questions.** How does group composition affect performance? What is the evidence on women's economic empowerment through group finance? How does intra-household allocation mediate measured effects?

> **No anchors yet.** Search terms on file: women's savings groups; gender microfinance empowerment; intra-household bargaining credit; group composition homogeneity; female borrower repayment

---

## Axis 2-Microfinance

### LC-02 — Group-lending mechanisms: information, sanction, repeat interaction

**P1** · **Partially covered** · 4 of 12 anchors · feeds MEMO-4

**Why it matters.** This is the mechanism the whole thesis turns on. OQ-12 is partially answered and OQ-13 is fully open; both need this component deeper than four anchors.

**Questions.** Which channel actually drives repayment, and how were the channels separated empirically? What evidence exists on what happens when the funding source changes? Is there any prior work on group-level versus member-level lending?

#### LIT-020 — [Gine & Karlan 2009 - Group versus Individual Liability: Long Term Evidence from Philippine Microcredit Lending Groups (Yale EGC WP 970; earlier trial as World Bank WPS4008, 2006; published Journal of Development Economics, 2014)](https://ideas.repec.org/p/egc/wpaper/970.html)

**Reviewed** · RCT · Philippines

*Female microcredit clients of a Philippine rural bank organised into group-liability 'centers' of approximately twenty women*

**Findings.** Two randomised trials testing whether the joint-liability CONTRACT is what produces repayment. Trial 1 (World Bank WPS4008, Sept 2006) randomly converted half of 169 pre-existing group-liability centers of approximately twenty women to individual liability, keeping the rest as group liability: 'the conversion to individual liability does not affect the repayment rate, and leads to higher growth in centre size by attracting new clients.' Trial 2 randomly assigned villages to group or individual liability. In both, groups continued to hold weekly meetings. Long-term result: no increase in default and larger groups after three years in the pre-existing areas, and no change in default but fewer groups created after two years in the expansion areas. The direct implication for OQ-12 is that joint liability as a contract term is separable from, and apparently not the source of, the repayment performance.

**Limitations.** Single lender in a single country, and clients kept meeting weekly under both arms, so the design holds meeting structure fixed and cannot separate the contract from the social interaction it sits inside - which is precisely what LIT-021 varies. Centre-level randomisation with approximately twenty women per centre. Sample sizes beyond the 169 centers of trial 1 not verified here. Read: WPS4008 full text and the Yale EGC WP 970 abstract; the published version (Journal of Development Economics, 2014) has not been read directly.

**What it opens.** Bears directly on OQ-12: if the joint-liability contract is not doing the work, then the underwriting features for RT-2 should describe the group's social structure rather than its liability terms. Raises whether weekly meetings, held constant here, are the actual active ingredient.

[open source](https://ideas.repec.org/p/egc/wpaper/970.html) · relevance — product High, risk High, impact Medium

#### LIT-021 — [Feigenberg, Field & Pande 2010 - Building Social Capital through Microfinance (NBER WP 16018; published as 'The Economic Returns to Social Interaction', Review of Economic Studies 80(4), 2013, 1459-1483)](https://ideas.repec.org/p/nbr/nberwo/16018.html)

**Reviewed** · RCT · India (West Bengal)

*Female clients of Village Welfare Society, an MFI operating in impoverished urban and peri-urban West Bengal; at the start of the experiments it held USD 6.75 million outstanding to over 56,000 female clients*

**Findings.** Isolates social interaction from the loan contract. First-loan-cycle groups were randomly assigned to meet weekly or monthly; all clients then converged to the same (fortnightly) frequency for the second loan, so any later difference reflects social ties formed earlier rather than ongoing treatment. Clients assigned to monthly meetings in the first cycle were four times (7.8%) more likely to default on the SECOND loan than weekly clients. Survey data and a follow-up lottery-based public-goods experiment attribute the effect to improved informal risk-sharing from greater social contact. Critically for OQ-12, these were INDIVIDUAL-liability lending groups: social ties reduced default with no joint-liability contract present, which the authors offer as an alternative explanation for the success of group lending.

**Limitations.** Authors' own caveats: default was extremely low among first-time borrowers (1.8% among monthly clients), so no effect appears in the first cycle and the result rests on the second; and 'bringing people together to interact in a financial setting such as microfinance groups may have a particularly strong effect on economic cooperation relative to other forms of interaction', limiting transfer to non-financial settings. Single MFI, single Indian state, female clients only. IMPORTANT VERSION NOTE: this row was read from the working-paper text (NBER WP 16018 / conference version, 2010), which states the four-times figure. The published version (Review of Economic Studies 80(4), 2013, 1459-1483, retitled 'The Economic Returns to Social Interaction: Experimental Evidence from Microfinance') reports a three-times figure in its abstract. The published text has not been read directly - use the published version's numbers before citing externally.

**What it opens.** Bears directly on OQ-12 and supplies a candidate causal channel: repayment via informal risk-sharing built by repeat interaction. Suggests RT-1 should capture meeting frequency and attendance as origination variables. Raises whether the effect survives when the creditor is an outside investor rather than the MFI the clients meet through.

[open source](https://ideas.repec.org/p/nbr/nberwo/16018.html) · relevance — product High, risk High, impact Medium

#### LIT-022 — [Ghatak & Guinnane 1999 - The economics of lending with joint liability: theory and practice (Journal of Development Economics 60(1), 195-228)](https://personal.lse.ac.uk/ghatak/jde2.pdf)

**Reviewed** · Theory with case-study review · Cross-country (theory plus case studies: Bangladesh, Germany, Ireland, Guatemala, USA, Malaysia, Burkina Faso)

*Joint-liability lending institutions, from 19th-century German and Irish credit cooperatives to Grameen-style microlenders and their transplants to wealthy countries*

**Findings.** The reference taxonomy for OQ-12. Joint liability is shown to work through four distinct mechanisms: better SCREENING against adverse selection, peer MONITORING to reduce moral hazard, incentives to ENFORCE repayment, and reduced lender AUDIT COSTS via costly state verification. The information channels (screening, monitoring) and the sanction channel (enforcement) are separable and can trade off against each other. The paper's Irish case makes the trade-off concrete: 19th-century Irish credit cooperatives modelled on successful German ones largely failed because members would not sanction defaulting neighbours, and a contemporary reform proposal to enlarge each cooperative's area so that outsiders could bear the blame 'amounts to throwing away all the information local people have on one another'. The paper also treats social ties as a precondition rather than a given - transplants to rural Arkansas struggled with low population density and heterogeneity, and Wydick (1999) is cited showing Guatemalan groups whose businesses are close together repay better.

**Limitations.** Theory paper with illustrative case studies, not an impact evaluation; no effect sizes. The authors are explicit about the gap this project is now facing: 'Given the underdeveloped state of the empirical literature, we do not claim that joint-liability lending is the most important feature of successful micro-lenders... There is clear evidence that joint-liability improves repayment, but these institutions use other instruments as well, and no study yet tries to apportion the reasons for success.' Written in 1999, so it predates the experimental work in LIT-020 and LIT-021 that partly answers it. Case studies are selected to illustrate, not sampled.

**What it opens.** Supplies the mechanism vocabulary OQ-12 needs and names the failure mode that matters most to this project: the authors note that when a group is denied future loans, 'bitterness and recrimination among group members may have far-reaching consequences for village life. This risk is inherent in the system and needs to be viewed as a potential cost.' That is a social-cost consideration for the impact methodology, not just a credit one.

[open source](https://personal.lse.ac.uk/ghatak/jde2.pdf) · relevance — product High, risk High, impact Medium

#### LIT-023 — [Tankha 2012 - Banking on Self-help Groups: Twenty Years On (ACCESS Development Services / SAGE)](https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-paper-banking-on-self-help-groups-twenty-years-on-2012.pdf)

**Reviewed** · Programme review with portfolio data · India

*The SHG-Bank Linkage Programme (SBLP), begun by NABARD in 1992: banks lend to self-help groups of typically 10-20 women, which on-lend to their own members at rates the group sets*

**Findings.** The closest real-world precedent for lending to the collective rather than the individual, at national scale and over twenty years. Tankha describes the Indian SHG as 'effectively a micro bank as it raises equity and deposits, as well as external funds, and on-lends them' - the same one-level-up abstraction we are considering. Crucially the record is mixed rather than a clean success. NPAs on the bank SHG portfolio were 'steady at 2.9% in March 2009 and March 2010' but 'gone up substantially to 4.72% as on 31 March 2011', with commercial banks near 5% and cooperative banks near 7% at that date. The government-subsidised SGSY component performed worse, 'consistently over 5% in all the years and over 7% as on 31 March 2011', with commercial banks at 7.4%. The book links deterioration to target-driven growth and to concerns about the quality of groups promoted, and records that the predecessor IRDP programme suffered 'abysmally low recoveries over the years, being exacerbated by political decisions to waive loan repayments', leaving banks with unpaid loans.

**Limitations.** A programme review and secondary compilation, not an impact evaluation; no counterfactual, so deterioration cannot be causally attributed to the linkage structure itself rather than to the subsidy programmes running alongside it. Portfolio data ends at 31 March 2011, so it predates the 2010 Andhra Pradesh microfinance crisis aftermath and everything since; current NABARD figures were not verified here because the NABARD site returned HTTP 503 to automated retrieval. Indian SHGs are promoted, trained and often subsidised by NGOs and government in ways VSLAs typically are not, so the transfer to a VSLA setting is not one-to-one. Book-length source: the structure, NPA tables and waiver history were read; the majority of the volume was not.

**What it opens.** Anchors OQ-13. Shows the group-as-intermediary model is viable at scale but that its credit quality is not self-sustaining: it degraded when group formation was driven by capital deployment targets, and it is exposed to political waiver risk that is systemic rather than idiosyncratic and therefore not diversifiable by pooling within one country. Also implies the underwriting unit becomes the GROUP as an intermediary - its governance, vintage and record-keeping - which is an RT-1 and RT-2 consequence.

[open source](https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-paper-banking-on-self-help-groups-twenty-years-on-2012.pdf) · relevance — product High, risk High, impact Medium

### LC-05 — Resilience and consumption-smoothing outcome measurement

**P1** · **In progress** · 1 of 8 anchors · feeds MEMO-5

**Why it matters.** Flagged as a gap in research-proposal.md. Memo 2 concludes the defensible claim is resilience and smoothing rather than income, which makes the measurement of resilience the load-bearing methodological choice. OPENED 2026-08-22, one anchor of eight. LIT-039 (FAO RIMA short questionnaire) supplies a citable, CC-licensed instrument and answers the operationalisation and survey-instrument questions: a latent-variable Resilience Capacity Index over four pillars, 41 questions in short form, with a shocks module. It does NOT answer the hardest question in this component - distinguishing consumption SMOOTHING from consumption LEVEL - and it measures resilience to food insecurity specifically, which is not the same estimand as a credit-and-insurance outcome.

**Questions.** How is household resilience operationalised and which indices are defensible? How are shocks timed and verified? What recall periods and survey instruments are standard? How is consumption smoothing distinguished from consumption level?

#### LIT-039 — [FAO 2020 - Resilience Index Measurement and Analysis: Short Questionnaire (RIMA-II)](https://openknowledge.fao.org/server/api/core/bitstreams/381c85aa-9de1-434b-8928-f6c92ee633b0/content)

**Reviewed** · Measurement methodology and survey instrument (latent variable model) · Global - designed for fragile and conflict-affected contexts

*Households, for resilience-to-food-insecurity measurement in programme monitoring and impact evaluation*

**Findings.** Answers LC-05's first and third questions with an off-the-shelf, citable instrument. RIMA estimates household resilience to food insecurity through a latent-variable model producing a Resilience Capacity Index, and FAO states it is context- and shock-specific and 'can be adopted for impact evaluation, reflecting the Theory of Change and Logframe of interventions'. The RCI is built from four pillars - Access to Basic Services, Assets, Social Safety Nets and Adaptive Capacity - plus food security and shocks modules; household demographics are mandatory alongside them, and optional modules cover subjective resilience and conflict. The short form is 41 questions, chosen from experience with the full RIMA by isolating the critical variables, plus literature review and technical consultation. It is explicitly designed for mobile-device collection and high-frequency monitoring, and FAO notes it also serves as 'a benchmark to assess whether already existing monitoring and evaluation frameworks are suitable for resilience analysis'. Individual items are binary or minutes-to-service and are meant to be contextualised before use. Published under CC BY-NC-SA 3.0 IGO, so it can be reproduced and adapted.

**Limitations.** This is the SHORT questionnaire, a deliberate reduction of the full RIMA for settings where full data collection is not feasible, so it trades measurement precision for field practicality and FAO says so. It measures resilience to FOOD INSECURITY specifically - it is not a general welfare or income instrument, and mapping it onto a financial-product outcome is an additional step the document does not take. RIMA is a descriptive and targeting tool; the RCI is a latent construct whose comparability across contexts depends on the contextualisation the user performs, which weakens cross-site pooling. There is no validation evidence in this document itself, only pointers to the RIMA-II methodology paper. It says nothing about how to distinguish consumption SMOOTHING from consumption LEVEL, which is LC-05's fourth and hardest question.

**What it opens.** Gives the research framework a concrete, defensible resilience instrument to name instead of gesturing at 'resilience', and its shocks module is a ready answer to how shocks get timed and verified. Still open for LC-05: whether the RCI is the right primary outcome for a credit-and-insurance intervention or whether consumption smoothing measured directly is better, and the smoothing-versus-level distinction, which nothing here addresses. Bears on OQ-4 and on framework section 6, since the estimand determines the power calculation.

[open source](https://openknowledge.fao.org/server/api/core/bitstreams/381c85aa-9de1-434b-8928-f6c92ee633b0/content) · relevance — product Low, risk Low, impact High

### LC-13 — Microcredit impact evidence and the meta-analytic record

**P2** · **Partially covered** · 1 of 10 anchors · feeds MEMO-4

**Why it matters.** The canonical evidence base a development-economics examiner will expect the candidate to know cold. Currently one anchor for an entire literature.

**Questions.** What do the seven coordinated microcredit RCTs find and how does the Bayesian hierarchical re-analysis change the reading? Where is treatment-effect heterogeneity real rather than noise? What are the standard critiques of the RCT canon?

#### LIT-003 — Duvendack et al. - What is the evidence of microfinance impact

**Reviewed** · Systematic review · Global

*Microfinance borrowers*

**Findings.** Systematic review of microfinance impact studies; average effects on poverty/income are small; strongest evidence for consumption smoothing and female empowerment

**Limitations.** Many underlying studies non-experimental; selection bias in who takes loans

**What it opens.** Which subpopulations see the largest effects, and can we screen for them at intake?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=Duvendack+et+al.+-+What+is+the+evidence+of+microfinance+impact) · relevance — product Low, risk Medium, impact High

### LC-17 — Over-indebtedness, consumer protection and credit ethics

**P2** · **Not started** · 0 of 6 anchors · feeds MEMO-4

**Why it matters.** The do-no-harm section of the framework needs an evidence base, and bundling a financed premium into a loan raises exactly the concern this literature documents.

**Questions.** What drives over-indebtedness in microcredit markets? What consumer-protection standards apply to bundled and financed insurance? What does the mis-selling record in microinsurance look like?

> **No anchors yet.** Search terms on file: microfinance over-indebtedness; client protection principles; microinsurance mis-selling; consumer protection financial inclusion; multiple borrowing microfinance; responsible finance

### LC-20 — Microfinance cost-to-serve and unit economics

**P2** · **Partially covered** · 2 of 6 anchors · feeds MEMO-9

**Why it matters.** RT-6 runs on assumptions the repo labels stubborn. RQ-06 and RQ-20 need real operating-cost benchmarks.

**Questions.** What are benchmark operating expense ratios by institution type and loan size? How does cost-to-serve scale with portfolio size? What does group methodology cost per member relative to individual lending?

#### LIT-016 — [MIX Market / Center for Financial Inclusion 2019 - Global Outreach and Financial Performance Benchmark Report 2017-2018](https://www.findevgateway.org/sites/default/files/publications/files/mix_market_global_outreach_financial_benchmark_report_2017-2018_1.pdf)

**Reviewed** · Industry benchmark report · Global (regional breakdowns incl. Africa/MENA)

*762 financial service providers, ~120m borrowers, USD 112bn gross loan portfolio (FY2017)*

**Findings.** Global yield on gross loan portfolio 19.2% (FY2017); operating expense / loan portfolio ratio (OER) 10.6%, down from 11.1% in FY2016; PAR30 6.0%, down from 7.1%; cost per borrower ~USD 87. Regional: Africa OER 14.5%, MENA yield 15.3% and OER 15.6%. This is the last comprehensive MIX benchmark edition.

**Limitations.** FY2017 data - predates COVID and the current rate cycle; self-reported by FSPs; MIX ceased regular reporting after this edition, so there is no newer equivalent; several regional figures are read from tables rather than stated in prose.

**What it opens.** Supplies the gross-yield, expected-loss (PAR) and cost-to-serve anchors for the RT-6 unit-economics model (OQ-10). Open: how do community/VSLA-level economics compare with these formal-MFI averages?

[open source](https://www.findevgateway.org/sites/default/files/publications/files/mix_market_global_outreach_financial_benchmark_report_2017-2018_1.pdf) · relevance — product Medium, risk High, impact Low

#### LIT-017 — [Symbiotics 2020 - 2019 Symbiotics MIV Survey (13th edition)](https://symbioticsgroup.com/wp-content/uploads/2020/02/symbiotics-symbiotics-2019-miv-survey.pdf)

**Reviewed** · Industry survey · Global

*87 microfinance investment vehicles (MIVs), USD 15.3bn assets under management (Dec 2018)*

**Findings.** MIV total expense ratio (TER) 2.4% of average assets in 2018, down from 2.9% in 2017; all-MIV management fee ~1.5%; Fixed-Income Funds (the debt vehicles closest to a securitisation) TER 2.2% and management fee 1.2%; weighted-average yield on the direct microfinance debt portfolio 7.6%; portfolio write-offs 0.2% and loan-loss-provision ratio 3.7%. Latest publicly available edition.

**Limitations.** 2018 data - predates COVID and current rates; self-reported; equity-fund TER excludes carried interest per the report's own footnote; MIV-level economics (a fund lending senior debt to MFIs) sit above the community/VSLA level this venture originates at.

**What it opens.** Supplies the structuring/servicing-fee and senior-coupon anchors for RT-6 (OQ-10). Open: how does a VSLA-linked vehicle's cost structure compare with an established MIV's?

[open source](https://symbioticsgroup.com/wp-content/uploads/2020/02/symbiotics-symbiotics-2019-miv-survey.pdf) · relevance — product Medium, risk High, impact Low

### LC-21 — Microsavings and household financial behaviour

**P3** · **Not started** · 0 of 6 anchors · feeds MEMO-4

**Why it matters.** The savings side of the group is the part with the most robust evidence, and it is the mechanism behind the resilience effects the framework measures.

**Questions.** What is the causal evidence on savings access and household outcomes? What role do commitment devices and mental accounting play? How does saving interact with borrowing in the same group?

> **No anchors yet.** Search terms on file: microsavings randomized; commitment savings; savings constraints poor; mental accounting savings; behavioural barriers saving

### LC-22 — Remittances and migrant financial arrangements

**P3** · **Not started** · 0 of 5 anchors · feeds MEMO-9

**Why it matters.** Underpins EXP-07 and the Israel migrant-worker track (EXP-29).

**Questions.** How do remittance flows interact with household risk management? What products link remittances to savings or insurance? What is documented about migrant-worker financial arrangements in destination countries?

> **No anchors yet.** Search terms on file: remittances risk sharing; remittance linked savings; migrant worker financial inclusion; diaspora finance; remittance cost corridor

### LC-26 — Impact-evaluation method advances

**P3** · **Not started** · 0 of 8 anchors · feeds MEMO-6

**Why it matters.** The framework makes design choices - clustering, stepped wedge, tail-powered outcomes, multiple hypotheses - that each have a methods literature a methods examiner will know.

**Questions.** How is power computed for cluster designs with realistic ICCs? What are the current standards on multiple-hypothesis correction and pre-analysis plans? How are spillovers handled? When is a stepped wedge identified?

> **No anchors yet.** Search terms on file: cluster randomized trial power; intracluster correlation development; pre-analysis plan; multiple hypothesis testing experiments; stepped wedge design; spillover effects experiments; randomization inference

---

## Axis 3-Securitization

### LC-07 — Credit-risk modelling in thin-data settings

**P1** · **Partially covered** · 5 of 10 anchors · feeds MEMO-7

**Why it matters.** RQ-03 is a whole strand and has no methodological anchors at all. The technical claim that these cash flows can be modelled needs the modelling literature behind it. OPENED 2026-08-22, one anchor of ten. LIT-038 gives RQ-03 the method it lacked - Pluto-Tasche upper confidence bounds for a portfolio with zero or near-zero observed defaults - and, more usefully, locates where the modelling is load-bearing: the PD bound is a function of an ASSET CORRELATION that is assumed, not estimated. That is the same parameter LC-08 says nobody has measured for this asset class, so LC-07 and LC-08 are one problem, not two. Still unanchored here: loss given default with few recoveries, competing risks of default and prepayment, short-panel corrections, and model-risk disclosure. READ 2026-08-22, five anchors of ten, and three of the component's four questions now have answers. SPECIFICATION (LIT-043): discrete-time hazard with an explicit baseline, competing risks for prepayment and write-off, left-truncation handling - and the justification transfers exactly, because credit data is interval-censored on a monthly cycle, which is the shape of a savings-group repayment book. Public R codebase. LGD (LIT-041): four named routes, of which IMPLIED HISTORICAL LGD - derived from total loss experience plus PD estimates - is the retail-portfolio case, and its validation 'relies essentially on the validation of the PDs used', so it inherits all the PD uncertainty. MODEL RISK (LIT-042): effective challenge as the organising principle, plus a warning aimed squarely at our own method - picking an extreme point on a modelled distribution is NOT conservative if the distribution was misspecified, which is exactly the Pluto-Tasche bound resting on an assumed asset correlation. THE CROSS-CUTTING FINDING: LIT-041 shows correlation does not merely widen the PD estimate, it BREAKS THE VALIDATION - tests assuming independence are so conservative that well-behaved systems fail them, while tests that model correlation detect only obvious miscalibration. So LC-07 and LC-08 are one problem from the regulator's side too. STILL OPEN: small-sample and short-panel corrections, and loss given default with few observed recoveries - the two questions where the thin-data literature is thinnest.

**Questions.** Which hazard and survival specifications are standard for small-ticket unsecured credit? How is loss-given-default estimated with few observed recoveries? What are the small-sample and short-panel corrections? How is model risk disclosed?

#### LIT-038 — [Grigutis 2023 - Probabilistic Overview of Probabilities of Default for Low Default Portfolios by K. Pluto and D. Tasche (arXiv:2303.06148)](https://arxiv.org/pdf/2303.06148)

**Reviewed** · Methodological / probabilistic exposition · Not applicable - methodological

*Credit portfolios with zero or very few observed defaults - the low default portfolio problem*

**Findings.** The method anchor RQ-03 was missing, and it turns out to be the bridge between LC-07 and LC-08. The paper is a probabilistic exposition of the Pluto-Tasche approach to estimating a probability of default when the observed default count is zero or near zero, which is exactly the position a new community-originated portfolio starts from. It sets out two estimators: one treating obligors as INDEPENDENT Bernoulli trials, and one treating them as CONDITIONALLY independent given a systematic factor. In the second, the default event is written as a threshold crossing of sqrt(rho)*S + sqrt(1-rho)*xi where S is the systematic factor and rho is the ASSET CORRELATION, defined in the paper as corr(r_log, S) = sqrt(rho); the resulting loss distribution is the Vasicek distribution, and the estimator is a mixture of binomial and Vasicek. The practical consequence, and the reason this matters here: the PD estimate is produced as an upper confidence bound, and that bound is a function of an asset correlation that is ASSUMED rather than estimated from the data. In a thin-data portfolio the correlation parameter is therefore doing much of the work, and it is precisely the parameter LC-08 says nobody has measured for this asset class.

**Limitations.** An expository article aimed at clarifying assumptions for early-career analysts, not new empirical or theoretical work, and the author states it is a survey of two models. It is a preprint. There is no application to microfinance, community finance or any real portfolio - no worked example on real data at all. It does not address loss given default, competing risks, prepayment, or short-panel corrections, all of which LC-07 also asks about, so it closes only one of that component's four questions. The choice of confidence level is acknowledged in the wider literature as unresolved and is not resolved here.

**What it opens.** Gives RQ-03 a defensible starting method and, more usefully, identifies WHERE the modelling is load-bearing: the asset correlation input. That converts a vague 'we will model the cash flows' claim into a specific, falsifiable one - the PD bound is only as good as the correlation assumption, and EXP-25 is the experiment that would supply it. Still open for LC-07: loss-given-default with few recoveries, competing risks of default and prepayment, small-sample and short-panel corrections, and how model risk gets disclosed to an investor.

[open source](https://arxiv.org/pdf/2303.06148) · relevance — product Low, risk High, impact Low

#### LIT-041 — [Basel Committee on Banking Supervision 2005 - Studies on the Validation of Internal Rating Systems (Working Paper No. 14, revised)](https://www.bis.org/publ/bcbs_wp14.pdf)

**Reviewed** · Regulatory working paper (collected technical studies by supervisory experts) · Not applicable - regulatory and methodological

*Internal rating systems under Basel II; PD, LGD and EAD estimation and validation*

**Findings.** The authoritative statement of why thin-data credit modelling is hard, and it says something sharper than 'not enough data'. On PD it separates two stages - discriminatory power (cumulative accuracy profile, accuracy ratio) versus calibration accuracy - and states that methods for validating CALIBRATION are 'at a much earlier stage'. Then the finding that matters most here: 'A major obstacle to backtesting of PDs is the scarcity of data, caused by the infrequency of default events AND THE IMPACT OF DEFAULT CORRELATION. Even if the final minimum requirements of the revised Framework for the length of time series for PDs (five years) are met, the explanatory power of statistical tests will still be limited.' It spells out the bind precisely: because defaults are correlated, observed default rates can systematically exceed critical values computed under independence, so tests assuming independence are conservative and even well-behaved rating systems fail them; while tests that DO account for correlation 'will only allow the detection of relatively obvious cases of miscalibration'. Its conclusion is that statistical tests alone are insufficient to validate a rating system, and that benchmarking against alternative sources is a necessary complement - though 'a complement to, not a substitute for' statistical methods. On LGD it is candid that 'much less is known about what drives LGD' and that a QUALITATIVE assessment of the estimation process may be more meaningful than quantitative validation. It sets out four estimation routes: workout LGD from discounted post-default cash flows; market LGD from traded defaulted loan prices; implied market LGD from non-defaulted bond prices via an asset-pricing model; and - explicitly flagged as the retail-portfolio case - IMPLIED HISTORICAL LGD, derived from total loss experience together with PD estimates. It also notes that validating implied historical LGD 'relies essentially on the validation of the PDs used in this method'. On incomplete workouts: facilities still in recovery are frequently excluded from the reference data set, banks use a recovery threshold (the example given is remaining non-recovered value below 5 per cent of EAD) or a time threshold such as one year from default, and 'if the definition results in the exclusion of many defaulted facilities from the LGD estimates, the treatment of incomplete workouts must be revised'. Finally, and directly relevant to this project's structure: it points to data POOLING initiatives by banking associations as an important step forward for building consistent data sets, 'especially for smaller banks'.

**Limitations.** Written for Basel II internal-ratings-based banks with five-year time series and formal supervisory oversight - a very different institution from a savings-group network or a cooperative internal credit fund, and the paper never contemplates that setting. It is 2005 and predates IFRS 9 lifetime expected credit loss, machine-learning scorecards and the current validation literature. It is a collection of expert studies rather than a single coherent method, and the Committee is explicit that the views are the authors' and not official. Retail portfolios get comparatively little attention; the implied historical LGD route relevant to us is named but not developed. No empirical results on a portfolio resembling ours.

**What it opens.** Answers LC-07's LGD question with a named menu and identifies which route fits a retail-shaped book, while making clear the retail route inherits all the PD uncertainty. More importantly it joins LC-07 to LC-08 from the regulator's side: correlation does not merely widen the PD estimate, it BREAKS THE VALIDATION - you cannot backtest your way out of a correlated portfolio. That is a second, independent reason the correlation parameter EXP-25 targets is load-bearing. The pooling remark also cuts both ways for this project and is worth taking seriously: pooling data across small lenders is endorsed as the fix for thin data, which is structurally the same move as pooling their loans, and the same concentration question applies.

[open source](https://www.bis.org/publ/bcbs_wp14.pdf) · relevance — product Low, risk High, impact Low

#### LIT-042 — [Board of Governors of the Federal Reserve System & Office of the Comptroller of the Currency 2011 - Supervisory Guidance on Model Risk Management (SR 11-7 / OCC Bulletin 2011-12)](https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107a1.pdf)

**Reviewed** · Supervisory guidance · United States - regulatory guidance, internationally influential

*Quantitative models used in bank decision-making; development, implementation, use, validation and governance*

**Findings.** The canonical answer to LC-07's fourth question - how model risk gets disclosed - and it contains one paragraph that lands directly on this project's method. Model risk is defined as 'the potential for adverse consequences from decisions based on incorrect or misused model outputs and reports', arising for two reasons: fundamental errors in the model, and correct models used incorrectly or outside the environment they were designed for. Risk is stated to increase with 'greater model complexity, higher uncertainty about inputs and assumptions, broader use, and larger potential impact', and aggregate model risk is affected by 'reliance on common assumptions, data, or methodologies' across models. The organising principle is EFFECTIVE CHALLENGE - 'critical analysis by objective, informed parties who can identify model limitations and assumptions and produce appropriate changes' - which depends on incentives, competence and influence, and is stronger the more separated the challenger is from the developer. THE PARAGRAPH THAT MATTERS HERE, on conservatism: 'banks should be careful in applying conservatism broadly or claiming to make conservative adjustments... Model aspects that appear conservative in one model may not be truly conservative compared with alternative methods. For example, simply picking an extreme point on a given modeled distribution may not be conservative if the distribution was misestimated or misspecified in the first place. Furthermore, initially conservative assumptions may not remain conservative over time.' Banks are told to 'justify and substantiate claims that model outputs are conservative'. The guidance also states plainly that model risk cannot be eliminated even with skilled modelling and robust validation, so limits on model use, performance monitoring and supplementary analysis are required alongside.

**Limitations.** Principles-based supervisory guidance, not a method - it says what a sound program contains and explicitly leaves the how to each institution's size, nature and complexity. It is addressed to supervised US banking organisations; a research project or an early-stage venture has no supervisor and therefore none of the governance machinery (independent validation function, model inventory, board reporting) the guidance assumes. It says nothing about thin-data estimation specifically, nothing about microfinance or community finance, and gives no worked examples. 2011, so it predates the machine-learning model governance debate it is now routinely applied to.

**What it opens.** Gives RT-5 and any published risk model a disclosure standard to be held to, and gives the proposal a defensible answer to a finance-side supervisor asking how model risk is handled. The conservatism paragraph is a direct warning to this project's own method: LIT-038's Pluto-Tasche upper confidence bound LOOKS conservative, but it is an extreme point on a distribution whose asset correlation is assumed rather than estimated - which is precisely the case the guidance says is not necessarily conservative at all. That should be stated explicitly wherever the bound is used, and it is a further argument for EXP-25. Effective challenge is also a structural point for the venture: a model built and validated by the same party that originates the assets is exactly the arrangement the guidance is written against.

[open source](https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107a1.pdf) · relevance — product Low, risk High, impact Low

#### LIT-043 — [Botha & Verster 2025 - Approaches for modelling the term-structure of default risk under IFRS 9: A tutorial using discrete-time survival analysis (arXiv:2507.15441v3)](https://arxiv.org/pdf/2507.15441)

**Reviewed** · Methodological tutorial with empirical demonstration; public R codebase · South Africa

*90,000 randomly subsampled residential mortgage accounts from a large South African bank*

**Findings.** Answers LC-07's first question - which hazard and survival specifications are standard - with a worked, reproducible example rather than a survey. The paper reviews classes of technique for lifetime probability of default under IFRS 9 and then develops an in-depth tutorial in DISCRETE-TIME survival analysis, with a set of reusable diagnostics and a public R codebase. Its central justification is directly transferable: 'the underlying data-generating mechanism of credit data is typically discrete in nature; i.e., interval-censored monthly observations' - which is exactly the shape of a savings-group repayment book, where instalments fall on a weekly or monthly cycle rather than in continuous time. It sets discrete-time hazard models within a generalised linear model framework differentiated by link function (logit, probit, complementary log-log), notes that logit and probit are more popular in practice with cloglog slightly underperforming both, and flags a specific pitfall: models that do not embed the baseline hazard as an explicit input are questionable as survival models at all. It covers the three credit-relevant complications by name - COMPETING RISKS (a loan may prepay, be written off or restructured, which precludes default and shrinks the risk set), LEFT-TRUNCATION (described as extensive, especially for longer-dated products), and RECURRENT DEFAULT EVENTS. Continuous-time alternatives are reviewed for contrast: Kaplan-Meier, Cox proportional hazards, and accelerated failure time models, with diagnostics including Cox-Snell and Schoenfeld residuals and time-dependent ROC analysis.

**Limitations.** Residential mortgages at a large bank in an upper-middle-income country - long-dated, collateralised, individually underwritten, with a rich MIS. Almost every one of those properties is the opposite of a VSLA or cooperative loan, so the METHOD transfers but the parameters and much of the diagnostic experience do not. 90,000 accounts is a large-data setting; the paper is not about thin data and offers no small-sample corrections, which is LC-07's third question and remains unanswered here. It is framed around IFRS 9 accounting requirements rather than securitisation. A preprint tutorial rather than a new empirical result, and its own contribution is pedagogical.

**What it opens.** Settles the specification question for RQ-03: discrete-time hazard with an explicit baseline, competing risks for prepayment and write-off, and left-truncation handling, with public code to start from rather than build. It also names the exact features a partner MIS must record for any of this to be possible - origination date, censoring status, and an event type that distinguishes default from prepayment and restructure - which should feed straight into RT-1's field list and EXP-22's protocol. Still open for LC-07: small-sample and short-panel corrections, and loss given default with few observed recoveries.

[open source](https://arxiv.org/pdf/2507.15441) · relevance — product Low, risk High, impact Low

#### LIT-044 — [DAI Washington for USAID 2006 - A Handbook for Developing Credit Scoring Systems in a Microfinance Context (microREPORT #66, AMAP)](https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-toolkit-a-handbook-for-developing-credit-scoring-systems-in-a-microfinance-context-feb-2006_0.pdf)

**Reviewed** · Practitioner handbook with institutional case studies · Multi-country practitioner cases - includes Bolivia, South Africa, Latvia, Bulgaria

*Microfinance institutions and banks building credit scorecards; cases span purely judgmental to statistical scorecards*

**Findings.** The practitioner answer to what an originator with thin data actually does, and it is not what the modelling literature assumes. Scorecards are classified as statistical, judgmental, or hybrid, and the handbook is direct about the trade-off: only a statistical model 'predicts the probability of default for an individual borrower', and 'this degree of precision makes it the most powerful scorecard type for risk management, pricing and provisioning', while judgmental and hybrid scores only RANK relative risk. That distinction is the crux for a securitisation thesis, because ranking does not price. It then states that 'the quality and quantity of historical data available are the most important factors to determining what type of scorecard should be developed', with the second factor being how far future business is expected to resemble past business. Its practical recommendation for institutions without data is a PHASED progression - the Credit Indemnity case runs paper-based judgmental application scorecard, then system-driven judgmental, then statistically developed behavioural, then collections, then fraud - and it makes the point that matters most for this project: 'Use of scorecards can be a stimulus for improving data collection and data management. More and better data open opportunities for developing more powerful scorecards over time.' It also insists that even judgmental models be back-tested on historic cases wherever possible to attach a historic probability of default to score bands, and records that BancoSol hired dedicated staff to key in historical data over a two-month period in order to develop a statistical model at all.

**Limitations.** 2006, and a USAID-commissioned practitioner toolkit rather than research - no effect estimates, no validation results, no comparison of scorecard performance across the cases it describes. Its cases are banks and larger MFIs with individual lending, not savings groups or cooperative internal credit funds, and group-guarantee structures barely feature. The 'Big Data Rule' and similar guidance are heuristics offered for ease of memory, not findings. It gives no minimum sample size for statistical scoring, which is the number a thin-data project most wants. Predates mobile and alternative-data scoring entirely.

**What it opens.** Reframes the thin-data problem as a sequence rather than a barrier, which fits this project's own logic: the origination protocol comes first and the model becomes possible later. That is EXP-22's argument arriving from the practitioner side, and it is worth citing there. But it also sharpens a constraint the venture has not fully confronted - a judgmental scorecard cannot price a pool, only rank it, so an originator running one is not investment-ready no matter how well it performs, and the gap between ranking and pricing is the gap this project has to close. Leaves open the minimum data volume at which statistical scoring becomes defensible in a group-lending book, which is a question EXP-25's panels could answer directly.

[open source](https://www.findevgateway.org/sites/default/files/publications/files/mfg-en-toolkit-a-handbook-for-developing-credit-scoring-systems-in-a-microfinance-context-feb-2006_0.pdf) · relevance — product Medium, risk Medium, impact Low

### LC-08 — Portfolio correlation and covariate risk in microfinance

**P1** · **Partially covered** · 6 of 8 anchors · feeds MEMO-7

**Why it matters.** Diversification is the whole argument for pooling. If defaults are covariate rather than idiosyncratic, the pooling thesis weakens sharply, and the repo currently has no evidence either way. CROSS-REFERENCE ADDED 2026-08-22: LIT-030 finds spatiotemporal adverse selection in index insurance - clients timing purchase on private seasonal information. Index products are usually presumed immune to it. If it holds in a pool we structure, the loss distribution is not what a naive actuarial model assumes, which is a correlation-structure problem and belongs here as well as in LC-03. READ 2026-08-22, six anchors of eight, and the component's own framing needed correcting. The question was posed as whether defaults are covariate or idiosyncratic. The historical record says covariate, but the dominant channel is not the one assumed: LIT-036 finds four national repayment crises driven by concentrated competition, multiple borrowing and social-network contagion, with the global recession explicitly rejected as the primary cause, and LIT-037 reports that individual MFI growth does NOT predict portfolio deterioration while MARKET-level penetration does. So the correlation is institutional and market-level, which geographic diversification does not fix and which pooling across lenders in one market may worsen. Against that, LIT-031 shows the environmental channel is real and severe in the chosen coffee setting. Both channels are live and they are separable, which is what EXP-25 should be designed to do.

**Questions.** How correlated are microfinance defaults across groups, regions and time? What drives the covariate component? How did microfinance portfolios behave in crises and droughts? What correlation assumptions do rating agencies apply to EM consumer pools?

#### LIT-016 — [MIX Market / Center for Financial Inclusion 2019 - Global Outreach and Financial Performance Benchmark Report 2017-2018](https://www.findevgateway.org/sites/default/files/publications/files/mix_market_global_outreach_financial_benchmark_report_2017-2018_1.pdf)

**Reviewed** · Industry benchmark report · Global (regional breakdowns incl. Africa/MENA)

*762 financial service providers, ~120m borrowers, USD 112bn gross loan portfolio (FY2017)*

**Findings.** Global yield on gross loan portfolio 19.2% (FY2017); operating expense / loan portfolio ratio (OER) 10.6%, down from 11.1% in FY2016; PAR30 6.0%, down from 7.1%; cost per borrower ~USD 87. Regional: Africa OER 14.5%, MENA yield 15.3% and OER 15.6%. This is the last comprehensive MIX benchmark edition.

**Limitations.** FY2017 data - predates COVID and the current rate cycle; self-reported by FSPs; MIX ceased regular reporting after this edition, so there is no newer equivalent; several regional figures are read from tables rather than stated in prose.

**What it opens.** Supplies the gross-yield, expected-loss (PAR) and cost-to-serve anchors for the RT-6 unit-economics model (OQ-10). Open: how do community/VSLA-level economics compare with these formal-MFI averages?

[open source](https://www.findevgateway.org/sites/default/files/publications/files/mix_market_global_outreach_financial_benchmark_report_2017-2018_1.pdf) · relevance — product Medium, risk High, impact Low

#### LIT-030 — [Jensen, Mude & Barrett 2018 - How basis risk and spatiotemporal adverse selection influence demand for index insurance: Evidence from northern Kenya (Food Policy 74(C) 172-198)](https://ideas.repec.org/a/eee/jfpoli/v74y2018icp172-198.html)

**To read** · Longitudinal household panel analysis · Kenya (northern, arid and semi-arid)

*Pastoralist households offered index-based livestock insurance (IBLI)*

**Findings.** The first study to measure basis risk DIRECTLY and put it into a demand estimation, which is why it matters more than its modest framing suggests. The abstract states that basis risk - the risk remaining to an insured individual - is widely acknowledged as the Achilles heel of index insurance, yet direct measurements of it had never been used to study its role in demand. Using longitudinal household data the authors find that, while price and the non-price factors studied previously are indeed important, BASIS RISK AND SPATIOTEMPORAL ADVERSE SELECTION also play a major role in determining IBLI demand. The adverse-selection finding is notable because index products are usually presumed immune to it - client knowledge of season-specific environmental conditions and spatial variation in basis risk reintroduce it.

**Limitations.** VERIFIED FROM THE PUBLISHED ABSTRACT ONLY (IDEAS/RePEc) - full text not read, hence Status To read. The abstract reports directions and importance but no effect sizes, so nothing quantitative can be cited from this row yet. Single product (livestock), single region, pastoralist population - transfer to crop or multi-peril cover is an argument, not a given. Observational panel rather than experimental.

**What it opens.** Two things for us. (1) It is the empirical counterpart to LIT-028's theory and supports treating basis risk as a first-order design parameter, which is EXP-30's premise. (2) The spatiotemporal adverse-selection finding is a warning for the securitisation side: if clients time purchase on private seasonal information, the pool's loss distribution is not what a naive actuarial model assumes. That belongs in LC-08 and RT-5, not only in LC-03.

[open source](https://ideas.repec.org/a/eee/jfpoli/v74y2018icp172-198.html) · relevance — product High, risk High, impact Medium

#### LIT-031 — [Root Capital 2016 - Financing Farm Renovation: How to Build Resilience Using a Blend of Capital (Learning Report: The Coffee Farmer Resilience Initiative)](https://rootcapital.org/wp-content/uploads/2018/01/Root-Capital-CFRI-Learning-Report-Full-Report.pdf)

**Reviewed** · Practitioner learning report (lender self-report, non-experimental) · Guatemala; Honduras; Mexico; Nicaragua; Peru

*Smallholder coffee producers reached through producer organisations, private mills and local financial institutions financed by Root Capital under the Coffee Farmer Resilience Initiative*

**Findings.** Answers the LC-24 credit-intermediation question directly and affirmatively. Root Capital lends to enterprises - producer organisations, private businesses or local financial institutions that aggregate individual farmers - and states those enterprises 'on-lend funds as smaller loans to individual producers and, in doing so, bear the risk of repayment. Enterprises manage all loan origination, disbursement, monitoring, and repayment internally through an internal credit fund.' So the co-operative IS the lender of record to the farmer. Scale stated: more than USD 900 million disbursed since 1999 across roughly 2,000 loans, of which 80 per cent had tenors under 12 months; under CFRI, USD 9 million in long-term renovation loans approved to nine enterprises in the first two years, helping 1,335 smallholder coffee farmers renovate 3,500 hectares. R&R loan parameters: USD 100,000 to USD 2 million, up to seven years with a two-year grace period on principal, collateral at 100 per cent loan-to-value on a fully discounted basis, monitoring by three visits per year to the enterprise plus the farms of 20 per cent of participating producers randomly selected by a Root Capital agronomist. Short-term lending uses a 'triangulation model' against forward purchase agreements with buyers, which the report says avoids the need for fixed-asset collateral. Blended structure stated precisely: Ford Foundation, IDB-MIF and Starbucks invested USD 12.5 million (seven to ten year); Keurig Green Mountain provided USD 400,000 first-loss, described as just under 3 per cent of target credit disbursements; USAID provided a 50 per cent pari passu guarantee up to USD 15 million taking effect after the first loss is exhausted; USAID also committed USD 2 million in grant funding. Leaf rust as a covariate shock: more than half of Central America's total coffee-growing area affected; analysts at the height of the outbreak estimated up to 40 per cent reduction in Central American annual output, approximately USD 500 million in lost producer revenue and nearly 375,000 jobs eliminated; El Salvador production cut 60 per cent in 2013/2014 against the prior year; 40 per cent of Peru's total coffee-growing area affected, and some Root Capital-financed producer organisations in Selva Central experienced 80 per cent production drops.

**Limitations.** A self-published learning report by the lender, not an independent evaluation, and explicitly written for practitioners: there is no counterfactual, no comparison group and no attribution claim. Critically for underwriting, NO repayment, default, delinquency or portfolio-at-risk figures are disclosed for the R&R portfolio or for the enterprises' own on-lending - the report is two years into a seven-year product with a two-year principal grace, so no loan had yet amortised. The report is candid that co-operative internal credit funds are 'often informal and unregulated', that weak internal controls and accounting are 'the most commonly observed deficiencies among potential R&R loan clients', and that credit decisions 'can be politically or personally motivated, rather than being based on established policies' - which means the intermediation rail exists but its record-keeping quality cannot be assumed. Nine enterprises is a small base. Latin America only; says nothing about East African co-operative lending.

**What it opens.** Bears directly on OQ-16: the co-operative credit rail the coffee anchor assumes does exist, but its data quality is the known weak point, which is the project's own thesis restated as a field risk. Feeds OQ-3 (canonical data schema) - an internal credit fund with informal records is precisely what a schema has to formalise. Feeds LC-08 and EXP-25: leaf rust is a textbook covariate shock and these figures are the correlation problem in its sharpest form.

[open source](https://rootcapital.org/wp-content/uploads/2018/01/Root-Capital-CFRI-Learning-Report-Full-Report.pdf) · relevance — product High, risk High, impact Medium

#### LIT-036 — [Chen, Rasmussen & Reille 2010 - Growth and Vulnerabilities in Microfinance (CGAP Focus Note 61)](https://www.cgap.org/sites/default/files/CGAP-Focus-Note-Growth-and-Vulnerabilities-in-Microfinance-Feb-2010.pdf)

**Reviewed** · Comparative case study (four national markets) with MIX and supervisory data plus practitioner interviews · Nicaragua; Morocco; Bosnia and Herzegovina; Pakistan

*National microfinance markets that each suffered a repayment crisis after a period of rapid growth, 2004-2009*

**Findings.** The central LC-08 anchor, and it reframes the correlation question. All four markets went into repayment crisis: portfolio-at-risk over 30 days exceeded 10 per cent in three of the four by June 2009, with Bosnia below 10 per cent only 'on account of aggressive loan write-offs'. June 2009 write-off ratios: BiH 4.1 per cent, Pakistan 3.66 per cent, Morocco 2.90 per cent, Nicaragua 1.84 per cent. Nicaragua's delinquency crisis 'affected all 22 major MFIs'; in BiH 'nearly all the 12 largest MFIs experienced a sharp rise in PAR, reaching 7 percent in June 2009'. Sector context: 2004-2008 average annual asset growth of 39 per cent to over USD 60 billion by December 2008, cross-border investment stock reaching USD 10 billion, and the four focal markets compounding at 33 to 67 per cent a year. CRITICALLY, the report rejects the macroeconomy as the cause: the MIX median PAR rose to nearly 3 per cent by December 2008 and the Symbiotics SYM 50 median to over 4.5 per cent by June 2009, but 'these increases were mild compared to the delinquency crises in our four countries', and most MFI managers interviewed did not name the global crisis as the primary cause. The three vulnerabilities it identifies are internal to the industry: concentrated market competition and multiple borrowing; overstretched MFI systems and controls; erosion of MFI lending discipline. Morocco's central bank estimated 40 per cent of borrowers held loans from more than one MFI as the crisis began. Contagion is named as a distinct mechanism with a stated boundary: in Pakistan 'social networks aided by mobile telephone connections rapidly escalated a small local problem into a wider regional crisis across semi-urban, Punjabi-speaking, low-income communities', and the report observes that 'these social networks can also set the boundaries beyond which a crisis is unlikely to spread' - the refusal to repay did not spread to rural areas.

**Limitations.** Four countries selected precisely because they had crises, so this is a sample on the dependent variable and says nothing about the base rate of correlated default in markets that did not blow up. Case-study method with interviews, not an identified estimate - no correlation coefficient, no asset correlation, no default correlation is reported anywhere, so it establishes that defaults cluster without quantifying how much. PAR and write-off figures come from mixed sources across the four countries (network data, MIX, JAIDA) and are not on a common basis; the report itself notes write-off policy is at each board's discretion, which makes PAR comparisons soft. Data ends 2009 and predates the Andhra Pradesh crisis of 2010, mobile lending, and every subsequent market cycle.

**What it opens.** Directly answers part of LC-08 and shifts it: the dominant correlation channel in the historical record is INSTITUTIONAL - concentration, multiple borrowing and social-network contagion - not weather or macro. That matters for the pooling thesis because geographic diversification does not diversify away a channel created by the lending structure itself, and because a pool assembled from several MFIs in one market may be more correlated, not less. Feeds EXP-25 directly: any correlation estimate should decompose institutional from environmental drivers, not lump them. Leaves open what the base rate is outside crisis markets, and what correlation assumption a rating agency would actually apply.

[open source](https://www.cgap.org/sites/default/files/CGAP-Focus-Note-Growth-and-Vulnerabilities-in-Microfinance-Feb-2010.pdf) · relevance — product Medium, risk High, impact Low

#### LIT-037 — [Schicks & Rosenberg 2011 - Too Much Microcredit? A Survey of the Evidence on Over-Indebtedness (CGAP Occasional Paper 19)](https://www.cgap.org/sites/default/files/CGAP-Occasional-Paper-Too-Much-Microcredit-A-Survey-of-the-Evidence-on-Overindebtedness-Sep-2011.pdf)

**Reviewed** · Evidence survey (narrative review of the over-indebtedness literature) · Cross-country; evidence base skewed to a small set of markets

*Microcredit borrowers and lenders; market-level and institution-level growth as predictors of repayment problems*

**Findings.** Supplies the finding that most sharpens LC-08 for a securitisation reader, and it is a level-of-analysis result. Citing Gonzalez's analysis of MIX data, the survey reports NO correlation between individual MFI growth rates and portfolio deterioration except at extreme and very unusual levels; it adds that intensive growth (adding borrowers to existing branches) is more dangerous than expansive growth (new branches), but that neither correlates with collection problems at growth rates large MFIs actually reach. 'The picture is different, however, when one looks at aggregate market-level growth rates': high aggregate growth in a country's number of microfinance borrowers, above 63 per cent per year, and an active-loans-to-total-population rate above 10 per cent, are significantly related to repayment problems. So the predictor of trouble is a MARKET-level variable, not a lender-level one. The survey is also explicit about the state of the evidence, saying there 'isn't enough evidence yet to make strong assertions about how prevalent most of them are or how heavily they contribute to over-indebtedness', and that multiple borrowing correlates with over-indebtedness in some studies but not all.

**Limitations.** A narrative survey, not a meta-analysis: no pooled effect sizes and no risk-of-bias appraisal of the studies it draws on. The Gonzalez results are reported second-hand from a 2010 analysis of MIX data, and MIX coverage is self-reported and skewed toward larger, better-governed institutions, which is exactly the wrong sample for measuring tail behaviour. The 63 per cent and 10 per cent figures are thresholds from one cross-country analysis, not validated parameters. It is a 2011 paper and the market-penetration measure predates digital and nano-lending, which change the denominator. It says nothing about how correlated losses would behave inside a structured pool.

**What it opens.** This is the sharpest available statement of the pooling problem: if the risk factor is market penetration rather than lender behaviour, then a pool diversified ACROSS LENDERS WITHIN A MARKET is not diversified against the thing that predicts trouble. Any tranching assumption in the risk tools should be tested against that. Feeds RT-1 and RT-5 and gives EXP-25 a concrete hypothesis to test rather than an open-ended correlation hunt.

[open source](https://www.cgap.org/sites/default/files/CGAP-Occasional-Paper-Too-Much-Microcredit-A-Survey-of-the-Evidence-on-Overindebtedness-Sep-2011.pdf) · relevance — product Low, risk High, impact Medium

#### LIT-038 — [Grigutis 2023 - Probabilistic Overview of Probabilities of Default for Low Default Portfolios by K. Pluto and D. Tasche (arXiv:2303.06148)](https://arxiv.org/pdf/2303.06148)

**Reviewed** · Methodological / probabilistic exposition · Not applicable - methodological

*Credit portfolios with zero or very few observed defaults - the low default portfolio problem*

**Findings.** The method anchor RQ-03 was missing, and it turns out to be the bridge between LC-07 and LC-08. The paper is a probabilistic exposition of the Pluto-Tasche approach to estimating a probability of default when the observed default count is zero or near zero, which is exactly the position a new community-originated portfolio starts from. It sets out two estimators: one treating obligors as INDEPENDENT Bernoulli trials, and one treating them as CONDITIONALLY independent given a systematic factor. In the second, the default event is written as a threshold crossing of sqrt(rho)*S + sqrt(1-rho)*xi where S is the systematic factor and rho is the ASSET CORRELATION, defined in the paper as corr(r_log, S) = sqrt(rho); the resulting loss distribution is the Vasicek distribution, and the estimator is a mixture of binomial and Vasicek. The practical consequence, and the reason this matters here: the PD estimate is produced as an upper confidence bound, and that bound is a function of an asset correlation that is ASSUMED rather than estimated from the data. In a thin-data portfolio the correlation parameter is therefore doing much of the work, and it is precisely the parameter LC-08 says nobody has measured for this asset class.

**Limitations.** An expository article aimed at clarifying assumptions for early-career analysts, not new empirical or theoretical work, and the author states it is a survey of two models. It is a preprint. There is no application to microfinance, community finance or any real portfolio - no worked example on real data at all. It does not address loss given default, competing risks, prepayment, or short-panel corrections, all of which LC-07 also asks about, so it closes only one of that component's four questions. The choice of confidence level is acknowledged in the wider literature as unresolved and is not resolved here.

**What it opens.** Gives RQ-03 a defensible starting method and, more usefully, identifies WHERE the modelling is load-bearing: the asset correlation input. That converts a vague 'we will model the cash flows' claim into a specific, falsifiable one - the PD bound is only as good as the correlation assumption, and EXP-25 is the experiment that would supply it. Still open for LC-07: loss-given-default with few recoveries, competing risks of default and prepayment, small-sample and short-panel corrections, and how model risk gets disclosed to an investor.

[open source](https://arxiv.org/pdf/2303.06148) · relevance — product Low, risk High, impact Low

### LC-09 — Securitisation eligibility, data tapes and rating criteria

**P1** · **Partially covered** · 3 of 10 anchors · feeds MEMO-7

**Why it matters.** OQ-3 and RQ-06 both need the target specification: what a data tape must contain before anyone will price it. The matrix has the deal-level view but not the field-level requirement.

**Questions.** What loan-level fields do standard reporting templates require? What eligibility criteria are typical for EM consumer and microfinance ABS? What do rating methodologies require of originator track record and servicing? Will an agency engage pre-track-record?

#### LIT-004 — FSD Africa / BII - microfinance securitization report

**Reviewed** · Case study / industry report · Africa

*MFI loan portfolios*

**Findings.** Case studies of MFI loan securitization/ABS in Africa (incl. NSIA Cote d'Ivoire, solar securitization Rwanda); shows feasibility but requires scale, standardized data, legal/ratings infrastructure

**Limitations.** Small sample of deals; mostly larger MFIs, not yet community-group (VSLA) level assets

**What it opens.** What legal/regulatory barriers block ABS issuance at community-group level?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=FSD+Africa+%2F+BII+-+microfinance+securitization+report) · relevance — product High, risk High, impact Low

#### LIT-006 — La Torre - Microcredit Securitization

**Reviewed** · Conceptual/legal review · Global

*MFI loan portfolios*

**Findings.** Indirect Microcredit-Backed Securitization (IMBS) model: SPV buys receivables from MFI, tranches by risk; senior/junior structure improves rating for senior notes

**Limitations.** Requires standardized loan data, legal transferability of receivables, and credit enhancement/first-loss layer to be investable

**What it opens.** What minimum pool size/data standardization is needed for VSLA-level receivables to be tranche-able?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=La+Torre+-+Microcredit+Securitization) · relevance — product High, risk Low, impact Low

#### LIT-011 — [FSD Africa & BII 2025 - The role of securitisation in developing capital markets in Africa](https://fsdafrica.org/wp-content/uploads/2025/10/The-role-of-securitisation-in-developing-capital-markets-in-Africa-BII-and-FSD-Africa.pdf)

**Reviewed** · Policy/market report with case studies · Africa

*Capital markets authorities, DFIs, banks and MFIs in African countries*

**Findings.** A number of African countries have introduced securitisation regulatory frameworks, but deal flow remains thin; closed deals have tended to involve relatively large, standardised portfolios with strong sponsor/DFI involvement; constraints are a shallow institutional investor base, limited rating-agency coverage, and few originators at sufficient scale

**Limitations.** Evidence base is mostly descriptive and drawn from a small number of transactions; not focused on VSLA-level assets; pool-size guidance is implicit in the examples rather than stated as thresholds

**What it opens.** What transaction sizes and structures (single-country vs regional, single- vs multi-originator) have actually closed in Africa, and what does that imply for minimum viable pool size and aggregation strategy?

[open source](https://fsdafrica.org/wp-content/uploads/2025/10/The-role-of-securitisation-in-developing-capital-markets-in-Africa-BII-and-FSD-Africa.pdf) · relevance — product High, risk High, impact Medium

### LC-10 — Securitisation law, true sale and SPV domicile

**P2** · **Partially covered** · 2 of 8 anchors · feeds MEMO-8

**Why it matters.** OQ-1 is blocked on counsel, not literature, but the thesis still needs the doctrinal frame written up rather than a checklist.

**Questions.** What makes an assignment a true sale across candidate jurisdictions? How is insolvency remoteness achieved where local trust law is thin? What changed with the EU Securitisation Regulation and Basel III/IV since LIT-009?

#### LIT-009 — [World Bank / IFC 2004 - Securitization: Key Legal and Regulatory Issues](https://documents1.worldbank.org/curated/en/747401468092077080/pdf/395540Securitization.pdf)

**Reviewed** · Legal/technical review · Global / Europe

*Legal frameworks and capital markets in Europe and Russia*

**Findings.** Sets out core legal preconditions for securitization: true sale that survives originator insolvency, transferability of receivables, efficient perfection/registration, enforceable security over receivables and collection accounts, tax neutrality, and an insolvency-remote limited-purpose SPV; summarises how several European laws (France, Italy, Spain, Portugal, Greece) addressed these obstacles

**Limitations.** Older (pre-CRR/CRD, EU Securitisation Regulation, Basel III/IV); focused on Russia and Europe rather than Israel/Africa; does not cover microfinance or VSLA assets specifically

**What it opens.** Use its legal checklist to assess whether Israel and target African jurisdictions can support true-sale transfers of VSLA-linked receivables, and whether local or offshore SPVs are feasible.

[open source](https://documents1.worldbank.org/curated/en/747401468092077080/pdf/395540Securitization.pdf) · relevance — product High, risk High, impact Low

#### LIT-010 — [Baker McKenzie 2020 - A Global Guide to Legal Issues in Securitisation](https://www.bakermckenzie.com/-/media/files/insight/publications/2020/09/global-securitisation-guide-2020-final_030920.pdf)

**Reviewed** · Comparative legal guide · Multi-country (incl. Africa / Europe / Middle East)

*Securitisation originators and investors across jurisdictions*

**Findings.** Country-by-country summaries of securitisation rules: SPV requirements, true-sale standards, risk-retention obligations, offering and qualified-investor restrictions, and tax/regulatory constraints; identifies where offshore SPVs are permitted and on what conditions

**Limitations.** Commercial law-firm guide rather than peer-reviewed; depth varies by jurisdiction; goes out of date as regulation changes; not specific to development or microfinance assets

**What it opens.** Which SPV domiciles and cross-border structures could hold pooled VSLA/community receivables while remaining compliant with local securitisation and investor-protection rules?

[open source](https://www.bakermckenzie.com/-/media/files/insight/publications/2020/09/global-securitisation-guide-2020-final_030920.pdf) · relevance — product High, risk High, impact Low

### LC-11 — African and emerging-market capital-market depth

**P2** · **Partially covered** · 3 of 8 anchors · feeds MEMO-8

**Why it matters.** OQ-2's pool-size answer depends on who could actually buy the paper, in what currency, under what mandate.

**Questions.** Which African markets have functioning securitisation frameworks and completed deals? Who are the domestic institutional buyers? How is currency risk handled in local-currency structures? What did the deals that closed have in common?

#### LIT-008 — Climate Finance Lab - Solar Securitization Rwanda

**Reviewed** · Instrument design / case study · Rwanda / Africa

*Distributed solar developers/off-grid households*

**Findings.** Pools many small distributed-asset loans (solar) from multiple originators into one tradable ABS; template for aggregating small, geographically dispersed receivables

**Limitations.** Required donor/DFI anchor investment and standardized origination protocol across developers to make the pool credible

**What it opens.** Direct analogue for pooling VSLA/community loans across multiple NGOs into one aggregation vehicle - what standardization is required?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=Climate+Finance+Lab+-+Solar+Securitization+Rwanda) · relevance — product High, risk Medium, impact Medium

#### LIT-011 — [FSD Africa & BII 2025 - The role of securitisation in developing capital markets in Africa](https://fsdafrica.org/wp-content/uploads/2025/10/The-role-of-securitisation-in-developing-capital-markets-in-Africa-BII-and-FSD-Africa.pdf)

**Reviewed** · Policy/market report with case studies · Africa

*Capital markets authorities, DFIs, banks and MFIs in African countries*

**Findings.** A number of African countries have introduced securitisation regulatory frameworks, but deal flow remains thin; closed deals have tended to involve relatively large, standardised portfolios with strong sponsor/DFI involvement; constraints are a shallow institutional investor base, limited rating-agency coverage, and few originators at sufficient scale

**Limitations.** Evidence base is mostly descriptive and drawn from a small number of transactions; not focused on VSLA-level assets; pool-size guidance is implicit in the examples rather than stated as thresholds

**What it opens.** What transaction sizes and structures (single-country vs regional, single- vs multi-originator) have actually closed in Africa, and what does that imply for minimum viable pool size and aggregation strategy?

[open source](https://fsdafrica.org/wp-content/uploads/2025/10/The-role-of-securitisation-in-developing-capital-markets-in-Africa-BII-and-FSD-Africa.pdf) · relevance — product High, risk High, impact Medium

#### LIT-012 — [OECD 2019 - Blended Finance Funds and Facilities: 2018 Survey Results (Working Paper 59)](https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/08/blended-finance-funds-and-facilities_14900999/806991a2-en.pdf)

**Reviewed** · Quantitative survey (180 funds/facilities) · Global

*Blended finance funds and facilities (DFI- and asset-manager-led)*

**Findings.** Survey of 180 blended vehicles with USD 60.2bn AUM; structured funds with layered junior/senior capital are common; average facility size ~USD 483m and average fund size ~USD 250m; structured funds are more likely to reach >=USD 100m than flat funds; OECD mobilisation methodology attributes 50% of mobilised private capital to official investors in the riskiest tranche

**Limitations.** Self-reported survey data with some double-counting across vehicles; aggregates many sectors and geographies rather than microfinance/VSLA specifically; does not evaluate the impact of each structure

**What it opens.** What does existing practice imply about sizing the junior/first-loss tranche and the overall vehicle if a VSLA-linked structured product is to attract DFIs and institutional investors?

[open source](https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/08/blended-finance-funds-and-facilities_14900999/806991a2-en.pdf) · relevance — product Medium, risk High, impact Medium

### LC-15 — PAYGO and energy-access receivables finance

**P2** · **Not started** · 1 of 6 anchors · feeds MEMO-9

**Why it matters.** EXP-02 and EXP-08 depend on it and it is the closest existing analogue to what this project proposes: small-ticket receivables already being pooled.

**Questions.** How are PAYGO solar receivables financed and securitised today? What default and repossession behaviour is documented? What data standards has the sector converged on?

#### LIT-008 — Climate Finance Lab - Solar Securitization Rwanda

**Reviewed** · Instrument design / case study · Rwanda / Africa

*Distributed solar developers/off-grid households*

**Findings.** Pools many small distributed-asset loans (solar) from multiple originators into one tradable ABS; template for aggregating small, geographically dispersed receivables

**Limitations.** Required donor/DFI anchor investment and standardized origination protocol across developers to make the pool credible

**What it opens.** Direct analogue for pooling VSLA/community loans across multiple NGOs into one aggregation vehicle - what standardization is required?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=Climate+Finance+Lab+-+Solar+Securitization+Rwanda) · relevance — product High, risk Medium, impact Medium

---

## Axis 4-Blended finance

### LC-06 — Climate and adaptation finance: gap sizing and instruments

**P1** · **In progress** · 1 of 8 anchors · feeds MEMO-6

**Why it matters.** Flagged as a gap. The opportunity-mapping methodology has a gap-magnitude axis with no evidence behind it, and a proposal that asserts a financing gap without an authoritative number is easy to dismiss. OPENED 2026-08-22, one anchor of eight. LIT-040 (CPI Global Landscape of Climate Finance 2024) closes the gap-magnitude axis with a citable number: adaptation finance reached USD 76 billion in 2022 against modelled needs of USD 212 billion a year for 2024-2030, so flows run at about a third of requirement in EMDEs alone. It also turns this component's third question into a documented data gap rather than an open one - flows are tracked at commitment level by intermediary, private and domestic-budget adaptation finance is described as opaque, and 92 per cent of tracked adaptation finance is public, so NOBODY can currently say what share reaches households. That absence is itself the argument for a private poolable instrument, and it is a stronger framing than the assertion it replaces.

**Questions.** What are the authoritative adaptation-finance and energy-access gap estimates and how are they constructed? Which instruments are actually deployed at household scale? What share of adaptation finance reaches households at all?

#### LIT-040 — [Climate Policy Initiative 2024 - Global Landscape of Climate Finance 2024: Insights for COP29](https://www.climatepolicyinitiative.org/wp-content/uploads/2024/10/Global-Landscape-of-Climate-Finance-2024.pdf)

**Reviewed** · Financial flow tracking and gap analysis · Global, with emerging market and developing economy breakdown

*Global climate finance flows by use, sector, instrument and destination; adaptation finance versus estimated adaptation needs*

**Findings.** Supplies LC-06 with the authoritative gap number the opportunity-mapping methodology was asserting without evidence. Adaptation finance more than doubled between 2018 and 2022, reaching USD 76 billion in 2022, on a path of USD 35 billion (2018), 42 (2019), 56 (2020), 61 (2021), 76 (2022). Against that, estimated adaptation needs are USD 212 billion a year on average for 2024-2030 and USD 239 billion a year for 2031-2050 - so current flows run at roughly a third of what is required to 2030 in EMDEs alone, which the report states directly. Total climate finance across all uses more than doubled from USD 674 billion in 2018 to USD 1.46 trillion in 2022. Distribution is heavily skewed: 19 per cent of adaptation finance (USD 14.5 billion) went to least developed countries and 2 per cent (USD 1.5 billion) to small island developing states in 2022. The public sector provided 92 per cent of adaptation flows in 2022, rising to 99 per cent for cross-sectoral adaptation, 88 per cent for water and wastewater and 87 per cent for agriculture, forestry and land use.

**Limitations.** The report is unusually direct about its own weakness, and the caveat is the finding for our purposes: 'Measuring the adaptation gap is challenging both conceptually and quantitatively. These figures are likely underestimates as they only account for EMDEs' needs, and many adaptation investment needs cannot be accurately measured.' It also states that 'information on climate adaptation finance from public domestic budgets and the private sector remains opaque' - CPI tracked only USD 4.7 billion of additional adaptation-relevant private finance across 2019-2022 through enhanced collection. Flows are tracked at commitment level by intermediary, not by ultimate recipient, so the report CANNOT answer what share of adaptation finance reaches households, which is LC-06's third question. Needs estimates are modelled and inherit the assumptions of the underlying studies. Coverage runs to 2022 with some 2023 indicators.

**What it opens.** Closes the gap-magnitude axis of the opportunity-mapping methodology with a citable number and a defensible range. It also converts LC-06's household question into a documented data gap rather than an unanswered one - nobody tracks adaptation finance to the household, and 92 per cent of what is tracked is public, which is itself the argument for a private, poolable instrument. Leaves open which instruments are actually deployed at household scale, LC-06's second question, which needs a different source.

[open source](https://www.climatepolicyinitiative.org/wp-content/uploads/2024/10/Global-Landscape-of-Climate-Finance-2024.pdf) · relevance — product Medium, risk Low, impact Medium

### LC-12 — Blended finance, first-loss and guarantees

**P2** · **Partially covered** · 7 of 6 anchors · feeds MEMO-8

**Why it matters.** Well covered for structuring mechanics; thin on whether mobilisation claims survive scrutiny, which is exactly what RQ-05 asks.

**Questions.** What counterfactual evidence exists that concessional capital mobilises rather than substitutes? How are mobilisation ratios computed and how contested are they? What does the additionality critique say?

#### LIT-005 — OECD - Scaling up blended finance in developing countries

**Reviewed** · Policy report · Global

*DFIs and private investors*

**Findings.** G20/OECD review of blended finance de-risking; guarantees and concessional capital mobilize private investment but effectiveness/mobilization ratios vary widely; risk of subsidizing bankable deals

**Limitations.** Limited rigorous counterfactual evaluation of blended finance outcomes; mostly descriptive/case-based

**What it opens.** What blended structures have proven replicable at scale, and which fit our risk profile?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=OECD+-+Scaling+up+blended+finance+in+developing+countries) · relevance — product Medium, risk High, impact Medium

#### LIT-012 — [OECD 2019 - Blended Finance Funds and Facilities: 2018 Survey Results (Working Paper 59)](https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/08/blended-finance-funds-and-facilities_14900999/806991a2-en.pdf)

**Reviewed** · Quantitative survey (180 funds/facilities) · Global

*Blended finance funds and facilities (DFI- and asset-manager-led)*

**Findings.** Survey of 180 blended vehicles with USD 60.2bn AUM; structured funds with layered junior/senior capital are common; average facility size ~USD 483m and average fund size ~USD 250m; structured funds are more likely to reach >=USD 100m than flat funds; OECD mobilisation methodology attributes 50% of mobilised private capital to official investors in the riskiest tranche

**Limitations.** Self-reported survey data with some double-counting across vehicles; aggregates many sectors and geographies rather than microfinance/VSLA specifically; does not evaluate the impact of each structure

**What it opens.** What does existing practice imply about sizing the junior/first-loss tranche and the overall vehicle if a VSLA-linked structured product is to attract DFIs and institutional investors?

[open source](https://www.oecd.org/content/dam/oecd/en/publications/reports/2019/08/blended-finance-funds-and-facilities_14900999/806991a2-en.pdf) · relevance — product Medium, risk High, impact Medium

#### LIT-013 — [OECD 2021 - Evaluating blended finance instruments and mechanisms](https://www.oecd.org/content/dam/oecd/en/publications/reports/2021/08/evaluating-blended-finance-instruments-and-mechanisms_c995f112/f1574c10-en.pdf)

**Reviewed** · Conceptual / evaluation guidance · Global

*Blended finance instruments and mechanisms (DFIs, donors, evaluators)*

**Findings.** Typology and evaluation approaches for blended instruments (equity, debt, first-loss capital, guarantees, structured funds, securitisations); first-loss guarantees and junior capital are the key tools in structured funds and securitisations; recommends assessing additionality, mobilisation, financial sustainability and risk; documents the practice of attributing 50% of mobilised private capital to official investors in the riskiest tranche

**Limitations.** Focuses on evaluation and measurement rather than concrete transaction design; examples are mostly at fund/facility scale; no sector-specific guidance for VSLAs or microfinance

**What it opens.** How should a first-loss tranche or pooled guarantee in a VSLA-linked vehicle be designed and documented so DFIs and donors can evaluate additionality and mobilisation against emerging OECD norms?

[open source](https://www.oecd.org/content/dam/oecd/en/publications/reports/2021/08/evaluating-blended-finance-instruments-and-mechanisms_c995f112/f1574c10-en.pdf) · relevance — product Medium, risk High, impact Medium

#### LIT-015 — [IFC 2025 - The Role of Blended Finance in an Evolving Global Context](https://www.ifc.org/content/dam/ifc/doc/2025/role-of-blended-finance-in-an-evolving-global-context.pdf)

**Reviewed** · Policy note · Global

*DFIs, donors and private investors in blended structures*

**Findings.** Sets out the current menu of first-loss instruments - junior equity, subordinated debt and pooled first-loss guarantees that cover default losses on a first-come, first-served basis - and stresses that concessional instruments are often recyclable or returnable rather than pure grant; frames minimum-concessionality and time-bound support as design norms

**Limitations.** Institutional policy note rather than independent evaluation; examples are illustrative and skew toward IFC's own transactions; limited quantitative benchmarking of tranche sizing

**What it opens.** Which first-loss instrument (junior equity, subordinated debt or pooled guarantee) is the most realistic ask for a first VSLA-linked pilot vehicle, and what tapering plan makes it acceptable to a donor?

[open source](https://www.ifc.org/content/dam/ifc/doc/2025/role-of-blended-finance-in-an-evolving-global-context.pdf) · relevance — product Medium, risk High, impact Medium

#### LIT-017 — [Symbiotics 2020 - 2019 Symbiotics MIV Survey (13th edition)](https://symbioticsgroup.com/wp-content/uploads/2020/02/symbiotics-symbiotics-2019-miv-survey.pdf)

**Reviewed** · Industry survey · Global

*87 microfinance investment vehicles (MIVs), USD 15.3bn assets under management (Dec 2018)*

**Findings.** MIV total expense ratio (TER) 2.4% of average assets in 2018, down from 2.9% in 2017; all-MIV management fee ~1.5%; Fixed-Income Funds (the debt vehicles closest to a securitisation) TER 2.2% and management fee 1.2%; weighted-average yield on the direct microfinance debt portfolio 7.6%; portfolio write-offs 0.2% and loan-loss-provision ratio 3.7%. Latest publicly available edition.

**Limitations.** 2018 data - predates COVID and current rates; self-reported; equity-fund TER excludes carried interest per the report's own footnote; MIV-level economics (a fund lending senior debt to MFIs) sit above the community/VSLA level this venture originates at.

**What it opens.** Supplies the structuring/servicing-fee and senior-coupon anchors for RT-6 (OQ-10). Open: how does a VSLA-linked vehicle's cost structure compare with an established MIV's?

[open source](https://symbioticsgroup.com/wp-content/uploads/2020/02/symbiotics-symbiotics-2019-miv-survey.pdf) · relevance — product Medium, risk High, impact Low

#### LIT-018 — [Convergence - How much commercial capital does concessional capital leverage? (State of Blended Finance data)](https://www.convergence.finance/news/4cC8kVJXvOFZDVxGQ6HLNH/view)

**Reviewed** · Transaction-database analysis · Global

*Blended finance funds and transactions in Convergence's deal database*

**Findings.** On average USD 1 of concessional capital mobilises ~USD 4.1 of commercial capital, of which ~USD 1.8 is private-sector (just under half), across 340 transactions (2023 data). An earlier brief reported ~4.0x average, median 2.7x and a range of 0.3x-22x (2018, 72 funds). Dispersion is wide and mobilisation skews toward middle-income countries.

**Limitations.** The leverage ratio is a contested metric that OECD warns can create perverse incentives; the deal database is self-reported; ratios skew to middle-income countries, so Sub-Saharan Africa / LDC figures are typically lower; it is a mobilisation, not an additionality or impact, measure.

**What it opens.** Provides the DFI mobilisation-ratio context for RT-6 and OQ-6 (how much private capital a first-loss layer can unlock). Open: what ratio is realistic for a VSLA-linked vehicle in Sub-Saharan Africa?

[open source](https://www.convergence.finance/news/4cC8kVJXvOFZDVxGQ6HLNH/view) · relevance — product Low, risk High, impact Medium

#### LIT-019 — [OECD 2021 - The Role of Guarantees in Blended Finance](https://www.oecd.org/content/dam/oecd/en/publications/reports/2021/06/the-role-of-guarantees-in-blended-finance_cef700a2/730e1498-en.pdf)

**Reviewed** · Policy report / mobilisation-data analysis · Global

*DFIs, donors and private investors using guarantees and other blended instruments*

**Findings.** Guarantees mobilised more private finance than any other instrument - 39% of all private capital mobilised over 2012-2018 - and were the most effective tool in every year of that period. OECD 2012-2023 instrument shares are roughly direct investment 29%, guarantees 23% and syndicated loans 19% (~70% combined). Total private finance mobilised exceeded USD 500bn over 2012-2023.

**Limitations.** OECD cautions that the leverage ratio is not its official metric; the instrument mix aggregates all sectors and geographies rather than microfinance/VSLA specifically; the analysis is descriptive rather than causal.

**What it opens.** Informs OQ-6 first-loss instrument choice (a pooled guarantee may mobilise more than junior equity) and the RT-6 mobilisation driver. Open: which first-loss instrument fits a first VSLA-linked pilot vehicle?

[open source](https://www.oecd.org/content/dam/oecd/en/publications/reports/2021/06/the-role-of-guarantees-in-blended-finance_cef700a2/730e1498-en.pdf) · relevance — product Low, risk High, impact Medium

---

## Axis 5-Insurance

### LC-03 — Index and parametric insurance: demand, basis risk, impact

**P1** · **Partially covered** · 4 of 12 anchors · feeds MEMO-5

**Why it matters.** FIRST PASS DONE 2026-08-22, and it compounds the LC-04 finding rather than softening it. Three things now stand on the record. (1) LIT-029, the authoritative review, states take-up has been DISAPPOINTINGLY LOW WITHOUT LARGE AND SUSTAINED SUBSIDIES - and our EXP-01 design does the opposite of subsidising, it adds the premium to the amount owed. (2) LIT-028 shows low demand may be RATIONAL rather than a behavioural failure: with basis risk, optimal demand for an index product is zero for the infinitely risk-averse and nonmonotonic in risk aversion, wealth and price. If that is right, compelling purchase overrides a correct decision instead of correcting a mistake. (3) LIT-030 measures basis risk directly and finds it, plus spatiotemporal adverse selection, materially drives demand - and the adverse-selection half is a warning for the pool's loss distribution, not just for take-up. Remaining: the empirical demand literature proper (Cole et al. on barriers to household risk management is the obvious next read), the impact side, and index-based livestock insurance outcomes.

**Questions.** What does the RCT evidence say about take-up and welfare effects of index insurance? How large is basis risk in practice and what reduces it? Why is demand persistently low at actuarially fair prices? What does the index-based livestock insurance record show?

#### LIT-007 — Kousky 2021 - Parametric Microinsurance review

**Reviewed** · Evidence review · Global (incl. Africa)

*Low-income households/farmers*

**Findings.** Parametric microinsurance can improve financial resilience and speed of payout vs indemnity insurance, but take-up remains low without subsidy/bundling

**Limitations.** Basis risk (payout doesn't match actual loss) undermines trust and renewal rates

**What it opens.** Can parametric triggers be designed around VSLA/group-level shocks (e.g., migrant remittance disruption) rather than only weather?

*no verified URL on file* — [search Scholar](https://scholar.google.com/scholar?q=Kousky+2021+-+Parametric+Microinsurance+review) · relevance — product High, risk High, impact Medium

#### LIT-028 — [Clarke 2016 - A Theory of Rational Demand for Index Insurance (American Economic Journal: Microeconomics 8(1) 283-306)](https://www.aeaweb.org/articles?id=10.1257%2Fmic.20140103)

**To read** · Theoretical model · Theoretical (no single geography)

*A risk-averse agent choosing how much index insurance to buy when the index imperfectly tracks their own loss*

**Findings.** The theory that reframes low take-up from a puzzle into a rational response, and it bites directly on our design. The abstract states that rational demand for index products is FUNDAMENTALLY DIFFERENT from demand for indemnity products because of basis risk: optimal demand is ZERO for infinitely risk-averse individuals, and is NONMONOTONIC in risk aversion, wealth and price. The paper derives upper bounds on optimal demand and gives a simple ratio for monitoring basis risk, using it to explain limited consumer interest in hedging instruments as a rational response to deadweight costs and basis risk.

**Limitations.** VERIFIED FROM THE PUBLISHED ABSTRACT ONLY (AEA page) - full text and model not read, hence Status To read. Theoretical: it constrains how we may reason about demand, it does not measure any population. The upper bounds and the basis-risk ratio are the operationally useful parts and neither has been extracted here.

**What it opens.** Sharpens OQ-17 considerably. If low demand for index cover is a RATIONAL response to basis risk rather than a behavioural failure, then compelling purchase by financing the premium into loan principal does not fix the problem - it overrides a correct decision and transfers the deadweight cost to the borrower, which is a plausible mechanism behind LIT-024 and LIT-025. Also bears on EXP-30 (does reducing basis risk pay for itself) and on the do-no-harm section of the research framework.

[open source](https://www.aeaweb.org/articles?id=10.1257%2Fmic.20140103) · relevance — product High, risk Medium, impact Medium

#### LIT-029 — [Carter, de Janvry, Sadoulet & Sarris 2017 - Index Insurance for Developing Country Agriculture: A Reassessment (Annual Review of Resource Economics 9 421-438)](https://ferdi.fr/en/publications/index-insurance-for-developing-country-agriculture-a-reassessment)

**To read** · Review article · Developing-country smallholder agriculture (review)

*The accumulated index-insurance experimentation record in smallholder agriculture*

**Findings.** The authoritative stock-take, and its headline is not encouraging for anyone assuming demand exists. The abstract states that uninsured risk is a major hurdle to investment, productivity growth and poverty reduction in developing-country smallholder agriculture, and that index-based insurance promised to overcome the hurdles of indemnity insurance in that setting - but that IN SPITE OF EXTENSIVE EXPERIMENTATION, TAKE-UP HAS BEEN DISAPPOINTINGLY LOW WITHOUT LARGE AND SUSTAINED SUBSIDIES. The authors argue existing take-up constraints can be partially overcome through revised contract design, better measurement technology, improved marketing and better policy support, and propose pairing improved index insurance with stress-tolerant seed varieties and new risk-oriented savings and credit products.

**Limitations.** VERIFIED FROM AN ABSTRACT RENDERING ON THE FERDI PUBLICATION PAGE plus a search-result quotation - the Annual Reviews page returned HTTP 403 and SSRN 403, so the canonical abstract could not be read directly and the full text certainly was not. Status To read. A review, so it summarises others' evidence rather than supplying its own; the specific studies behind 'disappointingly low' are not enumerated in what we read.

**What it opens.** The phrase that matters for us is 'without large and sustained subsidies'. Our EXP-01 design does the opposite of subsidising - it adds the premium to the amount owed. Feeds OQ-17 directly, and makes the subsidised-opt-in arm of EXP-17 the arm with the strongest prior. Also names contract redesign and measurement technology as the levers, which is where EXP-30 sits.

[open source](https://ferdi.fr/en/publications/index-insurance-for-developing-country-agriculture-a-reassessment) · relevance — product High, risk Medium, impact High

#### LIT-030 — [Jensen, Mude & Barrett 2018 - How basis risk and spatiotemporal adverse selection influence demand for index insurance: Evidence from northern Kenya (Food Policy 74(C) 172-198)](https://ideas.repec.org/a/eee/jfpoli/v74y2018icp172-198.html)

**To read** · Longitudinal household panel analysis · Kenya (northern, arid and semi-arid)

*Pastoralist households offered index-based livestock insurance (IBLI)*

**Findings.** The first study to measure basis risk DIRECTLY and put it into a demand estimation, which is why it matters more than its modest framing suggests. The abstract states that basis risk - the risk remaining to an insured individual - is widely acknowledged as the Achilles heel of index insurance, yet direct measurements of it had never been used to study its role in demand. Using longitudinal household data the authors find that, while price and the non-price factors studied previously are indeed important, BASIS RISK AND SPATIOTEMPORAL ADVERSE SELECTION also play a major role in determining IBLI demand. The adverse-selection finding is notable because index products are usually presumed immune to it - client knowledge of season-specific environmental conditions and spatial variation in basis risk reintroduce it.

**Limitations.** VERIFIED FROM THE PUBLISHED ABSTRACT ONLY (IDEAS/RePEc) - full text not read, hence Status To read. The abstract reports directions and importance but no effect sizes, so nothing quantitative can be cited from this row yet. Single product (livestock), single region, pastoralist population - transfer to crop or multi-peril cover is an argument, not a given. Observational panel rather than experimental.

**What it opens.** Two things for us. (1) It is the empirical counterpart to LIT-028's theory and supports treating basis risk as a first-order design parameter, which is EXP-30's premise. (2) The spatiotemporal adverse-selection finding is a warning for the securitisation side: if clients time purchase on private seasonal information, the pool's loss distribution is not what a naive actuarial model assumes. That belongs in LC-08 and RT-5, not only in LC-03.

[open source](https://ideas.repec.org/a/eee/jfpoli/v74y2018icp172-198.html) · relevance — product High, risk High, impact Medium

### LC-04 — Bundled credit and insurance: theory and evidence

**P1** · **Partially covered** · 4 of 10 anchors · feeds MEMO-5

**Why it matters.** FIRST PASS DONE 2026-08-22, and it changed the proposal. This was the most important empty cell in the repo because the master proposal asserts the literature raises but rarely tests loan-insurance bundling. That assertion is FALSE. Bundling has been tested experimentally at least twice, and both times it suppressed demand: Gine and Yang 2009 in Malawi (LIT-024, compulsory rainfall cover priced into a seed loan, take-up 13 points lower off a 33.0% base) and Banerjee, Duflo and Hornbeck 2014 in India (LIT-025, mandatory health cover, 16 point / 23 percent rise in drop-out - and that one measures the lender's own book, which we had assumed nobody had done). Against them sits Karlan et al. 2014 in Ghana (LIT-026): risk, not capital, is the binding constraint and demand for index insurance offered SEPARATELY is strong. Carter, Cheng and Sarris 2016 (LIT-027) is the theory that asks standalone-versus-interlinked directly. The live question is therefore not whether bundling has been tried but whether compulsory, premium-financed bundling can be designed so it does not destroy demand - which is what EXP-17 tests. Remaining: read all four full texts, then extend toward the lender-side and risk-contingent-credit literature (Mishra on insured loans and credit access is the obvious next lead).

**Questions.** What is the theoretical case that insurance relieves a credit constraint? What field evidence exists on interlinked credit-insurance contracts? Has anyone measured the effect of bundling on lender-side portfolio performance rather than borrower welfare?

#### LIT-024 — [Gine & Yang 2009 - Insurance, credit, and technology adoption: Field experimental evidence from Malawi (Journal of Development Economics 89(1) 1-11)](https://www.povertyactionlab.org/evaluation/insurance-credit-and-technology-adoption-malawi)

**To read** · RCT (field experiment) · Malawi

*About 800 maize and groundnut farmers offered credit for hybrid seed, 2006 crop season*

**Findings.** THE DIRECT TEST OF MANDATORY BUNDLING, and it went the wrong way. Half the farmers were offered credit alone; half were offered the same credit but REQUIRED to buy a rainfall index policy at actuarially fair rates that partially or fully forgave the loan on poor rainfall. The published abstract states take-up of 33.0% for the uninsured loan and take-up 13 percentage points LOWER among those offered insurance with the loan. The authors' suggested explanation is that farmers were already implicitly insured by the limited-liability clause in the loan contract, so adding a priced policy effectively raised the interest rate. Insured-loan take-up correlated with education, income and wealth; uninsured-loan take-up did not.

**Limitations.** VERIFIED FROM THE ABSTRACT AND THE J-PAL SUMMARY PAGE ONLY - full text not read, hence Status To read. Two figures do not agree across those sources and we could not reconcile them without the full text: the published abstract says take-up was lower by 13 percentage points, while the J-PAL evaluation page states 33% versus 17.6%, a 15.4 point gap. Most likely a regression-adjusted versus raw difference, but that is an inference, not something either source states. Single country, single season, one crop system, and the product was compulsory rather than offered at a choice - so it speaks to mandatory bundling specifically.

**What it opens.** Directly undercuts the novelty claim in docs/phd/phd-proposal-master.md that the literature raises but rarely tests loan-insurance bundling - it has been tested, experimentally, and mandatory bundling reduced take-up. Bears on OQ-16 (field anchor) and on EXP-01, whose design is precisely premium-financed-into-principal compulsory cover. Makes EXP-17 (separating the take-up effect from the protection effect) the live question rather than an add-on. See OQ-17.

[open source](https://www.povertyactionlab.org/evaluation/insurance-credit-and-technology-adoption-malawi) · relevance — product High, risk High, impact High

#### LIT-025 — [Banerjee, Duflo & Hornbeck 2014 - Bundling Health Insurance and Microfinance in India: There Cannot Be Adverse Selection If There Is No Demand (American Economic Review 104(5) 291-297)](https://www.aeaweb.org/articles?id=10.1257/aer.104.5.291)

**To read** · RCT (field experiment) · India (Karnataka)

*Existing microfinance clients of a large MFI, randomised at village level*

**Findings.** The second direct test of mandatory bundling, and the one that measures the LENDER side rather than borrower welfare - which is exactly the question LC-04 asks and the one we assumed was unanswered. Loan renewal was evaluated after mandating purchase of actuarially fair health insurance covering hospitalisation and maternity. The abstract states bundling led to a 16 percentage point (23 percent) increase in drop-out from microfinance, with many clients preferring to give up microfinance rather than pay a higher effective rate and receive insurance. Demand was so close to absent that there was no adverse selection to speak of.

**Limitations.** VERIFIED FROM THE PUBLISHED ABSTRACT ONLY (AEA page) - full text not read, hence Status To read. A short AER Papers and Proceedings piece (7 pages), so design detail and robustness are not in what we have read. Health insurance rather than climate cover, and an urban-adjacent Indian MFI rather than a savings group, so transfer to our setting is an argument, not a given. Secondary summaries cite a 22 percentage point fall in renewal against a 75 percent control renewal rate; that figure is NOT in the abstract and is unverified here.

**What it opens.** Answers LC-04's third question - yes, someone has measured bundling's effect on the lender's own book, and it was strongly negative. Any cash-flow model that assumes bundling is retention-neutral is unsupported. Feeds OQ-17 and the RT-6 assumptions.

[open source](https://www.aeaweb.org/articles?id=10.1257/aer.104.5.291) · relevance — product High, risk High, impact Medium

#### LIT-026 — [Karlan, Osei, Osei-Akoto & Udry 2014 - Agricultural Decisions after Relaxing Credit and Risk Constraints (Quarterly Journal of Economics 129(2) 597-652; NBER WP 18463)](https://www.nber.org/papers/w18463)

**To read** · RCT (field experiment, multiple arms and years) · Ghana (northern)

*Small-scale farmers randomised to cash grants, rainfall index insurance (granted or offered for purchase), or both*

**Findings.** The counterweight, and the reason the picture is a tension rather than a verdict. The abstract states that demand for index insurance is strong and that insurance leads to significantly larger agricultural investment and riskier production choices; the binding constraint to farmer investment is uninsured risk, not capital - when insured against the primary catastrophic risk, farmers find resources to increase farm spending. Subsequent-year demand rises with the farmer's own payouts, with payouts to others in their social network, and after recent poor rain. Patterns are consistent with meaningful basis risk, imperfect trust that payouts will arrive, and overweighting of recent events.

**Limitations.** VERIFIED FROM THE NBER WORKING PAPER ABSTRACT (w18463) - the published QJE version (2014, 129(2) 597-652) was not reachable and the full text is unread, hence Status To read. Insurance here was largely granted or offered as a separate product, often subsidised - which is materially different from financing a premium into loan principal, and is the most likely reason its demand finding points the opposite way to LIT-024 and LIT-025. No lender-side outcomes.

**What it opens.** Supplies the case FOR insurance in a credit-constrained setting and the mechanism our theory of change link 3 assumes. The contrast with LIT-024/LIT-025 - strong demand when offered separately, collapsed demand when compulsorily priced into a loan - is the sharpest single finding for our product design, and it is what EXP-17 is built to test. Feeds OQ-17.

[open source](https://www.nber.org/papers/w18463) · relevance — product High, risk Medium, impact High

#### LIT-027 — [Carter, Cheng & Sarris 2016 - Where and how index insurance can boost the adoption of improved agricultural technologies (Journal of Development Economics 118(C) 59-71)](https://ideas.repec.org/a/eee/deveco/v118y2016icp59-71.html)

**To read** · Theoretical model · Theoretical (no single geography)

*Small farm households choosing between a capital-intensive risky technology and traditional self-insurance*

**Findings.** The theory that asks our exact design question. The abstract states the paper steps back from a mixed empirical record and considers theoretically where index insurance is most effective, and specifically WHETHER IT SHOULD BE OFFERED AS A STANDALONE CONTRACT OR EXPLICITLY INTERLINKED WITH CREDIT. It reports a set of nuanced recommendations conditioned on the structure of risk and on the property rights or collateral environment. So the standalone-versus-interlinked question is not only tested empirically (LIT-024, LIT-025) but framed theoretically.

**Limitations.** VERIFIED FROM THE PUBLISHED ABSTRACT ONLY (IDEAS/RePEc) - full text not read, hence Status To read. The abstract does NOT state what the nuanced recommendations are; secondary summaries claim the model implies insurance must be bundled with loans in low-collateral environments, and that claim is NOT verified here and must not be cited until the model is read. Theoretical, so it constrains design reasoning rather than supplying evidence.

**What it opens.** Reading the model is now a priority because it may reconcile LIT-024 with LIT-026: Gine and Yang attribute low insured-loan take-up to implicit insurance from limited liability, which is a collateral-environment argument of exactly the kind this paper formalises. Feeds LC-04 and OQ-17.

[open source](https://ideas.repec.org/a/eee/deveco/v118y2016icp59-71.html) · relevance — product High, risk Medium, impact Low

### LC-24 — Coffee-sector economics and cooperative finance

**P1** · **Partially covered** · 5 of 8 anchors · feeds MEMO-9

**Why it matters.** PROMOTED TO P1 2026-08-22, and the reason matters: not because coffee has been chosen, but because it has not. The coffee cluster (EXP-09, EXP-10, EXP-11) scores above every other field candidate - 3.90, 3.60, 3.60 - and those scores rest on two assumptions nobody has tested: that producer cooperative federations and value-chain lenders are actually reachable as partners, and that existing certification and traceability records could carry underwriting rather than just provenance claims. Reading this component is the cheap way to test both before committing a field programme to them. If the assumptions hold, the cluster is the leading field anchor under OQ-16; if they do not, the scores were wrong and the anchor is EXP-01 or EXP-06. Either way the read pays for itself, which is what makes it P1 rather than context. PROMOTED, THEN OVERTAKEN: this component was raised to P1 to inform OQ-16, and on 2026-08-22 OQ-16 was decided in coffee's favour ahead of it. The read therefore now VERIFIES a live commitment rather than informing an open choice - if partner reachability or the certification data rails turn out not to exist, the finding forces a reversal, not a redirection. First in the P1 queue for that reason. READ 2026-08-22, five anchors of eight: the audit came back clean on both assumptions - cooperatives do lend (LIT-031) and member registers do serve as a sampling frame (LIT-033) - so no reversal is forced. The read instead relocated the risk: origination records inside cooperative internal credit funds are described by the lender itself as informal and unregulated, certification does not move total household income (LIT-032, LIT-034), and coffee carries two covariate shocks - leaf rust and world price - that make it the hardest case for poolability and the best case for measuring correlation. Written up in MEMO-9 section 5.

**Questions.** How is smallholder coffee financed today and by whom? What climate exposures dominate (leaf rust, drought, temperature) and are they indexable? What traceability and certification data already exists and could it serve as an origination schema? What is the record of coffee price-risk instruments for smallholders? Do cooperatives in the target belts actually intermediate credit, or only marketing? Is certification (Fairtrade, Rainforest Alliance, organic) audit data obtainable at member level, and does it constitute a usable sampling frame? What is the realistic membership size of a single cooperative, and how many cooperatives would a powered design need?

#### LIT-031 — [Root Capital 2016 - Financing Farm Renovation: How to Build Resilience Using a Blend of Capital (Learning Report: The Coffee Farmer Resilience Initiative)](https://rootcapital.org/wp-content/uploads/2018/01/Root-Capital-CFRI-Learning-Report-Full-Report.pdf)

**Reviewed** · Practitioner learning report (lender self-report, non-experimental) · Guatemala; Honduras; Mexico; Nicaragua; Peru

*Smallholder coffee producers reached through producer organisations, private mills and local financial institutions financed by Root Capital under the Coffee Farmer Resilience Initiative*

**Findings.** Answers the LC-24 credit-intermediation question directly and affirmatively. Root Capital lends to enterprises - producer organisations, private businesses or local financial institutions that aggregate individual farmers - and states those enterprises 'on-lend funds as smaller loans to individual producers and, in doing so, bear the risk of repayment. Enterprises manage all loan origination, disbursement, monitoring, and repayment internally through an internal credit fund.' So the co-operative IS the lender of record to the farmer. Scale stated: more than USD 900 million disbursed since 1999 across roughly 2,000 loans, of which 80 per cent had tenors under 12 months; under CFRI, USD 9 million in long-term renovation loans approved to nine enterprises in the first two years, helping 1,335 smallholder coffee farmers renovate 3,500 hectares. R&R loan parameters: USD 100,000 to USD 2 million, up to seven years with a two-year grace period on principal, collateral at 100 per cent loan-to-value on a fully discounted basis, monitoring by three visits per year to the enterprise plus the farms of 20 per cent of participating producers randomly selected by a Root Capital agronomist. Short-term lending uses a 'triangulation model' against forward purchase agreements with buyers, which the report says avoids the need for fixed-asset collateral. Blended structure stated precisely: Ford Foundation, IDB-MIF and Starbucks invested USD 12.5 million (seven to ten year); Keurig Green Mountain provided USD 400,000 first-loss, described as just under 3 per cent of target credit disbursements; USAID provided a 50 per cent pari passu guarantee up to USD 15 million taking effect after the first loss is exhausted; USAID also committed USD 2 million in grant funding. Leaf rust as a covariate shock: more than half of Central America's total coffee-growing area affected; analysts at the height of the outbreak estimated up to 40 per cent reduction in Central American annual output, approximately USD 500 million in lost producer revenue and nearly 375,000 jobs eliminated; El Salvador production cut 60 per cent in 2013/2014 against the prior year; 40 per cent of Peru's total coffee-growing area affected, and some Root Capital-financed producer organisations in Selva Central experienced 80 per cent production drops.

**Limitations.** A self-published learning report by the lender, not an independent evaluation, and explicitly written for practitioners: there is no counterfactual, no comparison group and no attribution claim. Critically for underwriting, NO repayment, default, delinquency or portfolio-at-risk figures are disclosed for the R&R portfolio or for the enterprises' own on-lending - the report is two years into a seven-year product with a two-year principal grace, so no loan had yet amortised. The report is candid that co-operative internal credit funds are 'often informal and unregulated', that weak internal controls and accounting are 'the most commonly observed deficiencies among potential R&R loan clients', and that credit decisions 'can be politically or personally motivated, rather than being based on established policies' - which means the intermediation rail exists but its record-keeping quality cannot be assumed. Nine enterprises is a small base. Latin America only; says nothing about East African co-operative lending.

**What it opens.** Bears directly on OQ-16: the co-operative credit rail the coffee anchor assumes does exist, but its data quality is the known weak point, which is the project's own thesis restated as a field risk. Feeds OQ-3 (canonical data schema) - an internal credit fund with informal records is precisely what a schema has to formalise. Feeds LC-08 and EXP-25: leaf rust is a textbook covariate shock and these figures are the correlation problem in its sharpest form.

[open source](https://rootcapital.org/wp-content/uploads/2018/01/Root-Capital-CFRI-Learning-Report-Full-Report.pdf) · relevance — product High, risk High, impact Medium

#### LIT-032 — [Oya, Schaefer, Skalidou, McCosker & Langer 2017 - Effects of certification schemes for agricultural production on socio-economic outcomes in low- and middle-income countries: a systematic review (3ie Systematic Review 34; Campbell Systematic Reviews 13)](https://www.3ieimpact.org/sites/default/files/2019-01/sr34-certification-schemes-agricultural-production_0.pdf)

**Reviewed** · Systematic review with meta-analysis (Campbell/3ie Systematic Review 34) · Low- and middle-income countries; Latin America dominant in the included studies

*Agricultural producers and wage workers under 12 certification schemes; coffee is 38 per cent of included studies and fruits 17 per cent; Fairtrade appears in over half*

**Findings.** The evidence-quality anchor for the certification leg of the coffee bet, and it is sobering. From 10,753 records the review included 43 studies from 44 papers for effectiveness and 136 studies from 114 papers for the qualitative question, published 1990 to 2016. It states plainly that there are NO randomised controlled trials in this literature, only quasi-experimental designs, and that 'the proportion of quantitative studies with high risk of bias ratings was relatively large'. Synthesised effects, certified versus control, with the review's own central estimates and ranges: prices 14 per cent higher (4 to 24 per cent; SMD 0.28, 95% CI 0.09 to 0.49), statistically significant; income from sale of certified produce 11 per cent higher (2 to 20 per cent; SMD 0.22, 95% CI 0.03 to 0.41), significant; TOTAL household income 6 per cent higher but NOT statistically significant (-3 to 16 per cent; SMD 0.13, 95% CI -0.06 to 0.32); yields 20 per cent lower and not significant (-52 to 19 per cent; SMD -0.42, 95% CI -1.23 to 0.39); assets/wealth 3 per cent higher, not significant; wages for workers in certified production 13 per cent LOWER and statistically significant (-22 to -3 per cent; SMD -0.26, 95% CI -0.46 to -0.06); schooling 6 per cent higher, significant; illness 7 per cent lower, not significant. The pattern is consistent: certification moves prices and crop-sale revenue but does not demonstrably move total household income.

**Limitations.** The review's own stated limits are severe and it says so: very few studies with low or moderate risk of bias per outcome, meta-analysis hampered by the paucity of calculable effect sizes and heterogeneous methods, several outcomes synthesised from only two studies. The standardised percentages are described by the authors as statistical constructs resting on assumptions, presented for intuition rather than as measured effects. Evidence is skewed to Latin America and to Fairtrade. It ends in 2016 and predates the certification landscape changes since. It says nothing about credit, insurance or lending - it is about certification's welfare effects, not about certification records as a data asset.

**What it opens.** Bears on OQ-16: certification is a usable organising structure but is NOT an income mechanism to build a welfare claim on - the total-household-income effect is not distinguishable from zero across the whole literature. Any coffee design that leans on the certification premium as the counterfactual improvement needs to say why it expects better than this. Also a methodological warning for the project's own design: a field of 43 studies with no RCT is a field where a well-powered randomised design is itself a contribution.

[open source](https://www.3ieimpact.org/sites/default/files/2019-01/sr34-certification-schemes-agricultural-production_0.pdf) · relevance — product Medium, risk Medium, impact High

#### LIT-033 — [Berihun 2024 - The Economic Impact of Sustainability Standards on Smallholder Coffee Producers: Evidence from Sidama Region, Ethiopia (IGC Working Paper ETH-22247)](https://www.theigc.org/sites/default/files/2024-06/Berihun%20Working%20paper%20March%202024.pdf)

**Reviewed** · Cross-sectional household survey with propensity score matching and nearest-neighbour matching · Ethiopia (Sidama Region)

*530 smallholder coffee households - 370 certified, 160 non-certified - drawn from 20 primary co-operatives (12 certified, 8 non-certified) across six woredas*

**Findings.** Answers the LC-24 sampling-frame question affirmatively and shows exactly how it is done. The author 'compiled a comprehensive list of coffee cooperatives, their participation in VSS certifications' working with the regional Authority, the Cooperatives Agency and the Sidama coffee farmers' co-operative unions, then randomly selected 12 certified and 8 non-certified co-operatives from those lists, then drew 370 certified and 160 non-certified households 'randomly from the list of cooperative members in proportion to the size of each cooperative'. So co-operative member registers exist, are obtainable through the union and the government Cooperatives Agency, and have been used as a probability sampling frame in practice. Structural figures for the region as stated: about 57 primary coffee co-operatives in Sidama, collectively involving around 85,000 smallholder farmers cultivating 8,000 hectares of Arabica; currently 41 Fairtrade-certified co-operatives of which 32 are also Organic certified, so 32 double-certified in total; Rainforest Alliance and UTZ certifications observed to be no longer in operation in the region despite Minten et al. 2015 recording them at 6.4 and 10.6 per cent of 47 union co-operatives at that time. On transmission: primary co-operatives can only trade internationally through their union (SCFU), and the certification premium reaches producers as dividends - the 2023 union report is cited for first dividends of 5 to 8 ETB/kg from co-operatives and second dividends of 5 to 6 ETB/kg from the union, with a social premium of USD 0.20/lb going to community projects rather than to households. Estimated price effect on red cherry is about 0.8 ETB more per kg, around 1.6 per cent above the non-certified mean, which the author notes understates the total effect because the premium arrives as dividend. Findings are positive: significantly higher red-cherry yields, prices and dividends, and under nearest-neighbour matching a positive significant effect on coffee income, household income and consumption expenditure; certification also raises production costs, mainly labour. The study also finds a co-operative effect - members of better-performing co-operatives benefit more in yield and dividends - with the VSS effect surviving controls for co-operative performance.

**Limitations.** Author-stated: measurements rest on individual recall, and certification is at group level so individual assignment is not clean. Cross-sectional and observational - PSM cannot rule out unmeasured confounding, which the paper acknowledges directly. Single region of a single country, chosen because certification is dense there, so it is close to a best case rather than a representative one. The positive income result is explicitly noted to differ from studies in western Ethiopia (Mitiku et al. 2017 found no living-standard effect) and the author attributes the difference to better-organised co-operatives in Sidama - which is an argument that the result is a property of strong co-operatives, not of certification. A working paper: supervised student research, not stated as peer-reviewed. Says nothing about co-operative lending to members, internal credit funds or default.

**What it opens.** Bears on OQ-16 and directly on power: 57 co-operatives and 85,000 farmers in one Ethiopian region is a large enough universe for a clustered design, and a 20-co-operative, 530-household study has already been executed there. Feeds the framework section 6 power calculation once an ICC is available. Leaves open whether member registers are equally obtainable in Latin American coffee belts, where the Root Capital evidence (LIT-031) sits.

[open source](https://www.theigc.org/sites/default/files/2024-06/Berihun%20Working%20paper%20March%202024.pdf) · relevance — product High, risk Low, impact Medium

#### LIT-034 — [Jena & Grote 2022 - Do Certification Schemes Enhance Coffee Yields and Household Income? Lessons Learned Across Continents (Frontiers in Sustainable Food Systems)](https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2021.716904/full)

**Reviewed** · Cross-sectional household survey with propensity score matching (radius, kernel and 5-nearest-neighbour), Rosenbaum bounds sensitivity analysis · Ethiopia; India; Nicaragua

*738 smallholder coffee farmers - Ethiopia 249 (166 certified, 83 not) across 6 primary co-operatives; India 256 (155, 101) across 6 villages; Nicaragua 233 (163, 70) across 4 co-operative unions*

**Findings.** A three-continent replication that lands close to the systematic review. Pooled across all three countries there is no statistically significant yield effect and no household income effect, with a net revenue effect of 445 to 593 PPP dollars per hectare. Country results diverge sharply: Ethiopia negative and not significant on yield (-127 to -165 kg/ha), net revenue (-171 to -242 PPP$/ha) and household income (1 to 6 PPP$); India positive and significant on yield (+215 to +281 kg/ha) and net revenue (+19 to +24 PPP$/ha) with mixed significance on household income (+273 to +486 PPP$); Nicaragua positive and significant on net revenue (+1,288 to +1,482 PPP$/ha) but not significant on yield (+95 to +209 kg/ha) or household income (-207 to +976 PPP$). On sampling, co-operatives were selected by stratified sampling with certification status as the strata, and farmers were then 'chosen randomly but drawn on the basis of fixed proportions to the membership population of the selected cooperatives' - the same member-register-proportional approach as LIT-033, though this paper does not state what enumeration list supplied the members.

**Limitations.** Authors state the country case studies are not representative of their continents. Cross-sectional data rules out instrumental-variable approaches; selection on unobservables remains possible despite the Rosenbaum bounds. Sample sizes are small - roughly 250 households and 6 co-operatives per country - which is a plausible explanation for the number of null results rather than evidence of no effect, and the paper does not report power. The authors note a general paucity of robust studies in this literature. Nothing on credit, insurance, or co-operative lending.

**What it opens.** Reinforces LIT-032 for OQ-16: certification does not reliably move total household income, and the effect that does appear is at the crop-revenue line. The Ethiopia result here is negative where LIT-033's Ethiopia result is positive - the two differ in region, sample size and year, and reconciling them is a real question for any Ethiopian siting decision. Also a caution on scale: 6 co-operatives and 250 households produced mostly nulls, which is the design the coffee anchor should NOT copy.

[open source](https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2021.716904/full) · relevance — product Medium, risk Low, impact Medium

#### LIT-035 — [International Coffee Organization 2020 - Coffee Development Report 2020: The Value of Coffee - Sustainability, Inclusiveness, and Resilience of the Coffee Global Value Chain](https://icocoffee.org/wp-content/uploads/2022/11/CDR2020.pdf)

**Reviewed** · Flagship sector report (descriptive market and price statistics) · Global; Colombia detail

*The global coffee value chain; producing-country market structure and price formation*

**Findings.** Establishes the price-risk premise behind EXP-09 with measured numbers rather than assertion. For coffee year 2019/20 the ICO composite indicator ranged between 93.60 and 124.49 US cents/lb day to day and Arabica futures between 92.90 and 139.97 US cents/lb, both hitting their low on 17 October 2019. The standard deviation of the composite indicator around its annual average was 7.2 US cents/lb, up from 5.9 the previous coffee year; for futures it was 11 US cents/lb, up from 7.8. Against IFPRI's Excessive Food Price Variability Early Warning System, spot prices recorded 48 days of moderate and 45 days of EXCESSIVE variability out of 260 reporting days between 1 October 2019 and 14 August 2020 - so roughly one trading day in six was flagged as excessively variable. Three distinct episodes are named: December 2019 to January 2020, March to May 2020, and August to September 2020. The report also records that Colombia's government launched a Coffee Price Stabilization Fund in February 2020 explicitly to protect farmers against price volatility, which is a live public-sector comparator for the price-stabilisation leg of EXP-09. Composite indicator group weights are given as Colombian Milds 12 per cent, Other Milds 21 per cent, Brazilian Naturals 30 per cent, Robusta 37 per cent.

**Limitations.** Descriptive market statistics, not an evaluation - there is no causal claim and no household-level evidence. The volatility window is dominated by the onset of covid-19, so 2019/20 is not a normal year and the report says as much. It documents that a price stabilisation fund exists in Colombia but provides no assessment of whether it worked, what it cost or who it reached. Prices are world-market indicators, not farmgate, and the gap between the two is exactly where a smallholder price instrument would have to operate.

**What it opens.** Bears on EXP-09: price risk is real and measurable, and a sovereign comparator already exists in Colombia, which is both a partner opportunity and a displacement risk under OQ-11's logic. Leaves open the farmgate-versus-world-price basis question, which is the price analogue of the basis risk LIT-030 measures for weather indices - and which would have to be settled before a price-stabilisation instrument could be indexed at all.

[open source](https://icocoffee.org/wp-content/uploads/2022/11/CDR2020.pdf) · relevance — product High, risk High, impact Low

### LC-16 — Agricultural value chains, warehouse receipts and price risk

**P2** · **Not started** · 0 of 8 anchors · feeds MEMO-9

**Why it matters.** EXP-04, EXP-09 and EXP-11 all sit here, and the coffee cluster cannot be assessed without it.

**Questions.** What is the evidence on warehouse receipt finance and post-harvest lending? How do price-stabilisation instruments perform for smallholders? How does value-chain finance interact with group structures?

> **No anchors yet.** Search terms on file: warehouse receipt finance; inventory credit smallholder; value chain finance agriculture; price risk management smallholder; commodity price hedging cooperatives; post harvest loss lending

---

## Axis 6-Data and technology

### LC-14 — Digital financial rails and origination data capture

**P2** · **Not started** · 0 of 8 anchors · feeds MEMO-9

**Why it matters.** RQ-06 asks what data capture costs. The answer depends on the rails available, which is a literature the repo has not touched at all.

**Questions.** What does the evidence say about digitising savings-group records? How do mobile money rails change transaction cost and data availability? What are the documented failure modes of MIS deployments in low-connectivity settings?

> **No anchors yet.** Search terms on file: digital savings groups; mobile money savings group; e-recording VSLA; digital financial services evidence; MIS microfinance implementation; digitisation informal finance

### LC-25 — Data governance, consent and privacy in field research

**P3** · **Not started** · 0 of 5 anchors · feeds MEMO-9

**Why it matters.** CLAUDE.md section 8 and the ethics section of the framework both depend on it, and IRB approval will require it in writing.

**Questions.** What consent standards apply in low-literacy multilingual settings? How is participant data governed when a commercial partner co-holds it? What are the norms on data sharing and retention in development field research?

> **No anchors yet.** Search terms on file: informed consent low literacy; research ethics development economics; data protection field research; participant data governance; IRB international field research

