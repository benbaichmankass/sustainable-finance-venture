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

Builds directly on the open questions already logged (OQ-4, OQ-5). **Direction set (2026-08-02): the
flagship portfolio is 2–3 parallel, lean, pre-registered RCTs sharing a single verification
partner** — so the partner (OQ-7, PT-05) and an anchor evaluation grant become gating prerequisites,
not parallel nice-to-haves. Sharing one partner favors experiments with a *common measurement
architecture*, which is one reason two of the three flagships are parametric (see the portfolio
note below). The proposal still commits to a *hierarchy of preference* per pilot:

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

**The flagship portfolio (OQ-11):** EXP-01 crop drought-index (rural smallholders), EXP-02
clean-energy PAYGO (energy / enterprise), EXP-06 multi-peril parametric climate cover (urban
informal settlements). The two parametric lines (EXP-01, EXP-06) share a trigger → payout →
loss-avoided measurement design, which is what makes running them in parallel under one partner
affordable. EXP-06 spans several perils (flood, drought/heat, storm), but that raises *product*
complexity, not *identification* complexity: access to the cover is randomized and resilience
outcomes are measured whatever peril actually strikes.

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
