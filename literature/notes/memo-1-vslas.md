# Memo 1: VSLAs & Savings Groups — Synthesis for Product/Research Design

**Status:** Reviewed · **Covers axis:** 1-VSLA · **Last updated:** 2026-08-07

## Sources
- LIT-001: Ksoll et al. 2016, cluster RCT (46 villages, Malawi)
- LIT-002: Cross-country VSLA/savings-group evaluation synthesis (Brannen 2016)
- LIT-014: CGAP 2025, *Regulating Savings Groups: Only a Proportionate Approach Will Work*
- LIT-023: Tankha 2012, *Banking on Self-help Groups: Twenty Years On* (India's SHG-Bank Linkage Programme)

## Lending to the group rather than the member (added 2026-08-07, for OQ-13)

India's SHG-Bank Linkage Programme is the large-scale precedent for financing the collective and letting it carry the individual loans. Banks lend to self-help groups of typically 10–20 women; the group on-lends to members at rates it sets. Tankha (LIT-023) describes the SHG as "effectively a micro bank as it raises equity and deposits, as well as external funds, and on-lends them."

The record is instructive precisely because it is mixed:

- NPAs on the bank SHG portfolio were **steady at 2.9%** in March 2009 and March 2010, then rose to **4.72% by 31 March 2011** — commercial banks near 5%, cooperative banks near 7%. The subsidised SGSY component ran **consistently over 5%, above 7%** at March 2011.
- Deterioration tracks **target-driven group formation** and concerns about the quality of groups promoted, not the structure alone.
- The predecessor IRDP programme suffered "abysmally low recoveries... exacerbated by political decisions to waive loan repayments."

**The counterweight worth holding onto:** the longest-running successful joint-liability institution in the record — the 19th-century German rural credit cooperative (LIT-022) — "financed those loans from local deposits." It was self-funded. The structure with the best track record did not take external wholesale funding into the group layer, which is exactly what a group-level securitisation would do.

## Key Findings
- Cluster-randomized evidence shows consistent, positive intent-to-treat effects on savings behavior and consumption smoothing.
- Effects on business investment/income are present but smaller and more heterogeneous across contexts.
- Cross-country synthesis confirms the savings/resilience effect is the most replicable finding in this literature; income effects are context-dependent.

## Regulatory and data environment

Added from LIT-014 — this is the piece that connects the impact evidence to our data problem.

- Savings groups carry low systemic and AML/CFT risk, so the appropriate regulatory posture is **registration, not prudential regulation**. Bank-style prudential rules are disproportionate and tend to suppress group formation.
- The workable model delegates registration to local authorities, NGOs and group federations rather than centralising it in a financial supervisor.
- The same source argues for **digitising group-level records** — not as a compliance burden, but as the mechanism that makes groups visible to governments, donors and private providers, and therefore able to access external finance.

The practical consequence for us: the data spine we need for underwriting is the same data spine the sector is already being pushed toward for policy reasons. We are not asking groups to carry a novel reporting burden — we are asking them to adopt, slightly earlier and more rigorously, a record-keeping standard the regulatory direction of travel already favours.

## Limitations
- ITT estimates dilute true effect size due to partial compliance/take-up.
- Single-country RCT settings limit external validity; pooling across heterogeneous contexts is difficult.
- Publication bias may skew the literature toward positive results.
- LIT-014 is a policy synthesis rather than a formal evaluation; its claims about fraud and consumer risk are argued rather than quantified.

## Implications for Product Design
1. VSLA cycles already generate structured, periodic data (contributions, payouts, loan requests) — this is the natural first data source for underwriting.
2. Because the savings/resilience effect is the most robust finding, initial product framing (and impact claims to investors) should emphasize resilience/smoothing rather than income growth.
3. Recommend piloting in Israel (migrant worker groups) first to test data capture infrastructure and parametric trigger design in a controlled, well-resourced environment before scaling to Africa.
4. **Design the VSLA data standard so it can drop into a light-touch registration system** — an NGO-run registry or federation platform — without requiring bank-level reporting. A schema that only works inside a supervised financial institution will not reach the groups we need.
5. **Frame data capture as a benefit to the group** (visibility, access to support, eligibility for external finance) rather than as a condition of participation. Per LIT-014 this is also the framing that actually achieves adoption.

## Open Questions
- Does effect persistence extend beyond typical 1-2 year RCT windows?
- What governance/verification structure is needed to make VSLA cash-flow data audit-grade for external investors? (→ OQ-3)
- Which registration model in our target jurisdictions — statutory, delegated, or purely voluntary — is realistically available to a pilot cohort? (→ OQ-3, OQ-1)
- If we lend to the group rather than the member, what stops capital-deployment pressure from degrading group formation quality the way it did in India? This is the failure mode LIT-023 documents, and it is a governance question about our own origination incentives, not about the groups. (→ OQ-13)
- Does a group carrying external debt still behave like a mutual-risk pool, or does it become a leveraged intermediary whose members' incentives shift? No source logged here answers this. (→ OQ-13, OQ-12)
