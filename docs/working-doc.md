# Sustainable Finance Product Research and Venture Working Document

## Purpose

This document is a living planning artifact for a project focused on identifying sustainable-development solutions that remain underfunded because financing, insurance, and risk-management structures are missing or misaligned. The working hypothesis is that community-based financial structures such as Village Savings and Loan Associations (VSLAs) may help manage idiosyncratic risk well enough to support scalable lending and insurance products, which could later be aggregated into securitizable assets.

The project is being shaped around three explicit design constraints. First, product families should be designed with eventual pooling and securitization in mind. Second, the research program should be empirical and verification-heavy, using rigorous impact evaluation methods and external research partners. Third, the operating role should initially focus on analytics, structuring, and project management, while local partners manage regulated operations, customer relationships, and compliance.

## Current project thesis

The central thesis is that some sustainable-development problems persist not because solutions are absent, but because the market lacks the right financial product design, underwriting logic, distribution mechanisms, and de-risking structures to channel capital toward them.

Community-based finance is a promising starting point because VSLAs and related informal savings systems already create governance, monitoring, and social-enforcement mechanisms at the local level.

## Design principles

### 1. Securitization-readiness
Any pilot product should be designed as a future underlying asset for an asset-backed structure: standardized contracts, digital audit trails, consistent data fields, predictable cash flows, and legal transferability.

Two-layer architecture: local origination layer (VSLAs, NGOs, MFIs, worker networks) and an aggregation layer (liquidity pools, SPVs) that pools receivables for outside investors.

### 2. Verification-first research design
Treat product design, impact evaluation, and risk verification as one integrated system. Realistic standard: cluster-randomized rollout, blinded outcome assessment where feasible, and strong quasi-experimental methods when full randomization is not practical.

### 3. Role specialization
Initial role sits in the structuring layer, not the licensed operating layer: analytics, underwriting logic, monitoring systems, partner coordination, and risk-sharing/first-loss structure design. Regulated entities handle origination, claims, collections, compliance.

## Preliminary literature themes (see /literature/lit-matrix.csv for full detail)

### Well established
- Persistent sustainable-development financing gap (risk allocation & intermediation problem, not just capital shortage)
- Community-based savings/lending structures (VSLAs, susu, ekub) can work and are durable
- Microfinance impact evaluation methods are mature (RCTs, pipeline designs)
- Securitization and blended finance are established financial technologies

### Partially explored
- Microfinance securitization exists but is limited/uneven, especially in Africa
- Microfinance outcomes are mixed, not uniformly positive
- Insurance integration into group-based models is recognized but under-mapped

### Likely clearest gaps
1. From community trust to investor-grade data
2. Product design for securitization-readiness at origination (not retrofitted later)
3. Integrated causal testing across the full product lifecycle (origination -> repayment/claims -> structuring -> investor suitability)
4. A partner-based model for analytics-driven de-risking (asset-light intermediary layer)

## Candidate pilot directions

### Africa-focused pilots
Deep traditions of community-based finance, high financial exclusion, aligns with blended finance/SDG capital mobilization narrative. Securitization markets still nascent -> potential first-mover advantage in standard-setting.

### Israel migrant-worker pilot
Logistical proximity, easier hands-on PM, existing regulatory environment around foreign-worker insurance. Good controlled environment to develop research protocol and tooling before African expansion.

**Working decision:** Consider anchoring PhD/pilot methodology development in Israel (migrant worker communities) first, then replicate in an African country as a second field site once framework is proven.

## Working hypotheses

1. Community-based groups reduce screening/monitoring costs enough to improve economics of small-ticket lending/insurance vs. atomized individual underwriting.
2. The bottleneck is not raw demand for finance but the absence of standardized, verifiable, poolable product structures institutional capital can price.
3. Investment-grade structures are unlikely to emerge from raw community portfolios without credit enhancement, first-loss protection, and high-quality servicing data.
4. The most defensible business position is a structuring/verification layer, not a retail financial institution.

## PhD framing

**Candidate research question:** How can community-based lending and insurance arrangements be structured into standardized, securitizable assets that mobilize private capital for sustainable development, and under what conditions do these structures improve risk-adjusted returns and development impact?

**Design constraints:** empirical-heavy, RCT/quasi-experimental where possible, double-blind where feasible, academic/research institutions as formal "research and verification partners" alongside community and commercial partners.

**Candidate programs/supervisors to evaluate:**
- Israel: Hebrew University of Jerusalem (Economics; Business School finance/risk), Tel Aviv University (New Environmental School; Coller School), Ben-Gurion University (Public Policy and Management; Economics)
- International: Oxford (Smith School / Oxford Sustainable Finance Group), LSE (Finance / International Development), Cambridge (Judge Business School / CISL), Geneva Finance Research Institute, IESEG/Lille, Loughborough Business School

## Business model framing

Three-layer structure:
- **Origination layer:** VSLAs, NGOs, MFIs, community banks, employer networks -- handle KYC, disbursement, collections, claims, local compliance
- **Risk layer (my role):** underwriting rules, monitoring dashboards, early-warning systems, risk-sharing/tranching design, first-loss structuring
- **Product layer:** loans, insurance, bundled products, priced using group-behavior data

**Target end state:** investment-grade tranches sellable to institutional investors, with DFI/philanthropic capital absorbing first-loss/junior risk and private capital in mezzanine.

**My value-add / toolkit to build:**
1. Standardized data schema for loans/insurance (ABS-data-tape-ready)
2. Underwriting engine (rules-based + ML scoring incorporating community signals)
3. Monitoring & early-warning system (DPD tracking, delinquency/claim pattern alerts)
4. Impact evaluation module (randomization infrastructure, pre-registered designs with academic partners)
5. Securitization modeling (cash-flow waterfall models, loss/prepayment simulations)

## Open questions for next phase

- Which use cases have the best combination of social need, unit economics, and securitization potential?
- Which communities/partner types generate the most reliable screening and servicing signals?
- What data schema is required to make future pooling and rating feasible?
- Which impact metrics should be tracked alongside financial metrics from day one?
- What minimum credit enhancement is likely needed to approach investment-grade notes?
- Israel pilot vs. Africa pilot as the first site -- final decision pending contact/access assessment
- Loan vs. insurance vs. bundled product as the first instrument

## Change log

- Initial version drafted via research/planning conversation (pre-lit-review)
