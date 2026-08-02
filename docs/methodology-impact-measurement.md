# Methodology: Measuring the SDG Impact of the Financial Products

**Status:** Skeleton (week of 2026-08-02) · **Owner:** BB · **Parent:** `docs/research-proposal.md` §3

## Purpose

The venture's credibility rests on a claim it must be able to *prove*: that the financial
products it structures actually improve the climate-resilience and poverty outcomes they target —
not just that loans were disbursed or premiums collected. This document is the skeleton of the
research methodology for measuring that impact, so it is designed *before* any product is in the
field, not reconstructed afterward.

It answers three questions: **impact on what**, **identified how**, and **verified by whom**.

## 1. Impact on what — outcome metrics

Metrics are chosen to map onto the two SDG frames the proposal commits to. Each candidate product
in `data/experiments.csv` will select from this menu; the menu is deliberately outcome-side, not
output-side.

| Frame | Primary outcomes | Notes |
|---|---|---|
| **Poverty reduction** | Consumption / consumption smoothing; asset retention through shocks; income stability; food security | Memo 2 is clear the defensible microfinance claim is *resilience and smoothing*, not income transformation — metrics reflect that |
| **Climate resilience** | Losses avoided in a climate shock; speed of recovery; adoption of climate-smart inputs / assets; reduced distress sales | For parametric products (EXP-01/05/06) the mechanism is payout-on-trigger; measure whether payouts actually protect assets |
| **Climate mitigation (where relevant)** | Clean-energy adoption; biomass / emissions displaced | Applies to the energy-access experiments (EXP-02, EXP-08) |
| **Financial (paired)** | Repayment / loss curves, claims ratios, cost-to-serve | Paired with impact so the analysis can speak to *both* SDG and investor theses at once |

**Discipline:** output metrics (loans made, people reached) are logged but never reported *as*
impact. The distinction is the whole point of the methodology.

## 2. Identified how — causal design

Builds directly on the open questions already logged (OQ-4, OQ-5). The proposal does not commit to
a single design across all sites; it commits to a *hierarchy of preference* and picks per pilot.

1. **Cluster-randomized rollout** — preferred where ethically and operationally feasible
   (randomize at the savings-group / village level). Cleanest identification. OQ-4 notes this is
   likely most feasible in a smaller, controlled site.
2. **Stepped-wedge** — where partners resist withholding treatment; every cluster is eventually
   treated, order randomized. Often more acceptable to NGO partners (OQ-4).
3. **Strong quasi-experimental** — matched difference-in-differences, regression discontinuity on
   an eligibility threshold — where randomization is impossible.

Cross-cutting design requirements:
- **Pre-registration** of hypotheses and analysis plan before rollout.
- **Blinded outcome assessment** where feasible (the verification partner collects outcomes
  without knowing treatment status).
- **Powered for the resilience effect**, not just the mean effect — the interesting outcomes are
  in the tails (what happens in a shock), which drives sample size.

## 3. Verified by whom — independence

Impact the venture measures on its own products is not credible. The design separates the party
that *structures* from the party that *measures*:

- An **independent verification partner** (academic field team / RCT lab) runs outcome
  measurement — this is OQ-7, and PT-05 (J-PAL) is the standing candidate.
- **IRB / ethics approval** and a **data-sharing agreement** are preconditions, not afterthoughts.
- Row-level participant data stays in the Vault (`05-raw-data`), never in the repo — only
  aggregate results come back (CLAUDE.md §8).

## 4. Integration with the toolkit

The impact module is one of the five risk-tools, not a bolt-on. The same RT-1 origination schema
that makes receivables poolable also carries the baseline covariates the causal design needs;
the RT-3 monitor timestamps the shocks the resilience metrics are measured against. Designing
impact measurement and securitization-readiness together is design principle 2 of the venture
(`docs/working-doc.md`).

## Deliverable state

Skeleton only. Remaining work: pick the outcome metrics per flagship experiment (after OQ-11),
resolve OQ-4/OQ-5 with a prospective supervisor and verification partner, and draft the
pre-registration template. Feeds milestone M-08 (pilot design doc).
