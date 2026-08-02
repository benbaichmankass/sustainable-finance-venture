# Memo 3: Securitization & Blended Finance — Synthesis for Product/Research Design

**Status:** Reviewed · **Covers axes:** 3-Securitization / 4-Blended finance · **Last updated:** 2026-08-02

## Sources
- LIT-004: Case studies of MFI loan securitization/ABS in Africa (FSD Africa/BII; NSIA Cote d'Ivoire; solar securitization Rwanda)
- LIT-005: G20/OECD review of blended finance de-risking instruments
- LIT-006: Microcredit Securitization — Indirect Microcredit-Backed Securitization (IMBS) model
- LIT-008: Solar securitization Rwanda — distributed asset aggregation template
- LIT-009: World Bank/IFC 2004 — *Securitization: Key Legal and Regulatory Issues*
- LIT-010: Baker McKenzie 2020 — *A Global Guide to Legal Issues in Securitisation*
- LIT-011: FSD Africa & BII 2025 — *The role of securitisation in developing capital markets in Africa*
- LIT-012: OECD 2019 — *Blended Finance Funds and Facilities: 2018 Survey Results*
- LIT-013: OECD 2021 — *Evaluating blended finance instruments and mechanisms*
- LIT-015: IFC 2025 — *The Role of Blended Finance in an Evolving Global Context*
- LIT-017: Symbiotics 2020 — *2019 Symbiotics MIV Survey* (MIV cost structure and yields)
- LIT-018: Convergence — *How much commercial capital does concessional capital leverage?* (mobilisation ratios)
- LIT-019: OECD 2021 — *The Role of Guarantees in Blended Finance*

## Key Findings
- Existing microfinance/community-asset securitization deals (IMBS tranching, Rwanda solar ABS, African bank SME ABS) required: (1) a standardization layer for loan-level data, (2) credit enhancement or a first-loss tranche, and (3) an anchor investor (often DFI or donor) before market-rate senior tranches were sellable to private investors.
- Blended finance instruments (guarantees, concessional capital) are the typical bridge used to de-risk the earliest tranches/deals in this space.
- The solar securitization template (pooling many small, geographically dispersed loans from multiple originators into one tradable vehicle) is a close structural analogue to pooling VSLA/community loans across NGOs.

## Legal and regulatory framework for cross-border SPVs

The legal question is not "onshore or offshore" — it is whether the originating jurisdiction recognises the transfer and the security. LIT-009 gives the checklist to run against each jurisdiction:

1. **True sale** that is not unwound in the originator's insolvency.
2. **Assignability of receivables** without prohibitive consent or notification requirements.
3. **Efficient perfection/registration** of the transfer.
4. **Enforceable security** over both the receivables and the collection accounts.
5. **Insolvency-remote, limited-purpose SPV.**
6. **Tax neutrality** — no punitive transfer, stamp or withholding tax on the structure.

LIT-010 adds the jurisdiction-by-jurisdiction layer. Practical constraints it surfaces that bear on our design:

- Many jurisdictions permit offshore SPVs with foreign-law documentation provided local assignment and tax rules are respected — so the SPV domicile is a cost/efficiency decision more than a feasibility one.
- If senior notes are to be sold to EU/UK investors, **risk-retention rules** apply (the originator must retain a minimum economic interest), alongside qualified-investor and private-placement restrictions.
- Some jurisdictions restrict SPV ownership by entities resident in particular offshore centres — worth checking before defaulting to a Cayman vehicle.

**Next step (OQ-1):** run the six-point checklist above against Israel and the shortlisted African jurisdiction with local counsel, and shortlist two candidate domiciles (one EEA, one African/regional). The literature has taken this as far as it can; the remainder is a counsel question.

## Pool size and aggregation strategy

- LIT-011 finds that several African countries have enacted securitisation frameworks without generating meaningful deal flow. The binding constraints are a shallow institutional investor base, limited rating-agency coverage, and too few originators holding portfolios large and standardised enough to securitise efficiently.
- LIT-012 gives the size benchmarks: 180 blended vehicles surveyed, USD 60.2bn AUM, average facility ~USD 483m and average fund ~USD 250m, with **structured funds materially more likely than flat funds to clear USD 100m**.
- Fixed costs — legal, rating, listing, structuring — set a minimum efficient scale that a single NGO's VSLA portfolio in a single country will not reach.

**Implication:** the first vehicle should be a **multi-originator, plausibly regional** aggregation rather than a single-partner pool, and it should be framed as a *blended fund with securitisation-ready mechanics* — private, DFI-anchored, in the tens of millions — with an explicit path to a public issuance at ≥ USD 100m once the track record exists. This is the warehousing/aggregation bridge referenced in OQ-2.

## First-loss and blended-finance structuring

- OECD mobilisation methodology attributes **50% of mobilised private capital to official investors in the riskiest tranche** (LIT-012, LIT-013). The junior tranche is the mobilisation lever, and it is measured as such — a strong argument for a clearly delineated junior layer rather than a pari-passu pool.
- Junior/first-loss capital in comparable structures commonly sits in the **10–20% of total structure** range, though it varies widely by sector and risk (LIT-013, LIT-015). Treat this as a starting range to be tested, not a target.
- LIT-015 sets out the instrument menu: junior equity, subordinated debt, and **pooled first-loss guarantees** that absorb default losses on a first-come, first-served basis. It also stresses that concessional instruments are frequently recyclable or returnable rather than pure grant — a material point when asking a donor to fund the junior layer.

Design guidance from LIT-013, which is written for evaluators and therefore tells us what we will be judged on:

- State **additionality** explicitly: why private capital would not enter without the first-loss layer.
- Instrument monitoring to track **both** mobilisation and the financial performance of the junior layer.
- Document a **tapering/exit plan** so concessional support is understood as time-bound from the outset.

## Fee benchmarks and mobilisation ratios (for the unit economics)

These anchors were added to calibrate the RT-6 unit-economics model (OQ-10); they price the structuring layer rather than the legal or credit structure.

- **What a fund earns and what it costs to run (LIT-017).** The 2019 Symbiotics MIV Survey (87 vehicles, USD 15.3bn AUM, 2018) reports an all-MIV total expense ratio of **2.4%** of average assets (management fee ~1.5%); for Fixed-Income Funds — the debt vehicles closest to a securitisation — TER is **2.2%** and the management fee **1.2%**. The weighted-average yield on the direct microfinance debt portfolio was **7.6%**, i.e. what senior capital lent into this market earned. These set our fee-load and senior-coupon anchors. The MIV write-off ratio was only 0.2% because the MFI, not the fund, absorbs first loss — a reminder that where you sit in the stack determines the loss you bear.
- **How much private capital a first-loss layer unlocks (LIT-018, LIT-019).** Convergence finds USD 1 of concessional capital mobilises ~USD 4.1 of commercial capital on average, of which ~USD 1.8 is private-sector — with wide dispersion (median 2.7x, range 0.3x–22x) and a skew toward middle-income countries, so Sub-Saharan Africa is likely at the lower end. OECD adds the instrument nuance: **guarantees mobilised more private finance than any other instrument** (39% of the 2012–2018 total, most effective in every year), which bears directly on the OQ-6 first-loss instrument choice — a pooled guarantee may out-mobilise junior equity.

The honest caveat: these are MIV- and fund-level figures. A VSLA-linked vehicle originates a layer below an established MIV, where the origination cost-to-serve is higher and the net spread thinner. The RT-6 model uses these as anchors, flags everything derived from them as a working assumption, and brackets the answer across worst/likely/best scenarios rather than asserting a point estimate.

## Limitations
- Sample of actual community-asset securitization deals is still small; most precedents are at MFI/bank scale, not yet at raw community-group (VSLA) level.
- Blended finance evaluation literature is largely descriptive/case-based; rigorous counterfactual evidence on mobilization effectiveness is limited.
- LIT-009 predates the EU Securitisation Regulation and Basel III/IV; its legal checklist remains sound but its regulatory context does not.
- The 10–20% first-loss range is an observed central tendency across heterogeneous deals, not a benchmark derived from anything resembling our asset class.

## Implications for Product/Research Design
1. Build the data schema and underwriting rules from day one to match ABS eligibility criteria: loan-level granularity, standardized covenants, verifiable repayment/claims history, and audit trails.
2. Plan for a 2-3 year pilot period generating a clean data/repayment track record sufficient to make a credible case to a DFI or anchor investor for a first credit-enhanced tranche.
3. Explore multi-originator aggregation (multiple NGO/VSLA networks feeding one SPV) using the solar securitization structure as a direct template — and size it against the ≥ USD 100m threshold where structured vehicles start to behave like the rest of the market.
4. Budget for a first-loss/guarantee layer (likely donor or DFI capital) at roughly 10–20% of the structure; do not assume market-rate capital will be available for the first securitized tranche.
5. Run the LIT-009 legal checklist as a formal jurisdiction scan before committing to a pilot geography — the legal precondition set is binary, and discovering a broken link late is expensive.

## Open Questions
- ~~What legal/regulatory framework applies to cross-border pooling of Israel + Africa-origin receivables into a single SPV?~~ → **partially answered**: checklist and candidate structures identified (LIT-009, LIT-010); jurisdiction-specific counsel review outstanding. (OQ-1)
- ~~What minimum pool size and data standardization threshold is required before a rating agency or anchor investor will engage?~~ → **partially answered**: target band established (tens of millions warehoused, ≥ USD 100m for issuance) (LIT-011, LIT-012). (OQ-2)
- ~~What blended-finance structure best fits our expected risk profile at pilot stage?~~ → **partially answered**: junior tranche at 10–20%, instrument menu identified, evaluation requirements known (LIT-012, LIT-013, LIT-015). (OQ-6)
- Still fully open: what does a rating agency actually require of VSLA-level receivables, and will any agency engage pre-track-record?
