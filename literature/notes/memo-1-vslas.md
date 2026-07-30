# Memo 1: VSLAs & Savings Groups — Synthesis for Product/Research Design

**Status:** Reviewed · **Covers axis:** 1-VSLA · **Last updated:** 2026-07-30

## Sources
- LIT-001: Ksoll et al. 2016, cluster RCT (46 villages, Malawi)
- LIT-002: Cross-country VSLA/savings-group evaluation synthesis (Brannen 2016)
- LIT-014: CGAP 2025, *Regulating Savings Groups: Only a Proportionate Approach Will Work*

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
