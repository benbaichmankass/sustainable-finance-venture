# Methodology: Measuring the SDG Impact of the Financial Products

**Status:** Outcome-metric layer (week of 2026-08-02; re-scoped 2026-08-22) · **Owner:** BB **Parent:** `docs/phd/research-proposal.md` §3 · **Spine:** `docs/research/research-framework.md`

> **Read the framework first.** As of 2026-08-22 the identification strategy, estimands, power method, two-layer randomisation design, verification arrangement, data architecture and falsification conditions live in `docs/research/research-framework.md`. This document is no longer the whole methodology \- it is the **outcome-metric layer**: what gets measured, against which SDG frame, with what discipline. Sections 2 and 3 below are retained because the framework refers back to them, and are summarised there rather than duplicated.

## Purpose

The venture's credibility rests on a claim it must be able to *prove*: that the financial products it structures actually improve the climate-resilience and poverty outcomes they target — not just that loans were disbursed or premiums collected. This document specifies what gets measured to prove it, designed *before* any product is in the field rather than reconstructed afterward. How that measurement is identified, powered and verified is the framework's job (`docs/research/research-framework.md`).

It answers three questions: **impact on what**, **identified how**, and **verified by whom**.

## 1\. Impact on what — outcome metrics

Metrics are chosen to map onto the two SDG frames the proposal commits to. Each candidate product in `data/experiments.csv` will select from this menu; the menu is deliberately outcome-side, not output-side.

| Frame | Primary outcomes | Notes |
| :---- | :---- | :---- |
| **Poverty reduction** | Consumption / consumption smoothing; asset retention through shocks; income stability; food security | Memo 2 is clear the defensible microfinance claim is *resilience and smoothing*, not income transformation — metrics reflect that |
| **Climate resilience** | Losses avoided in a climate shock; speed of recovery; adoption of climate-smart inputs / assets; reduced distress sales | For parametric products (EXP-01/05/06) the mechanism is payout-on-trigger; measure whether payouts actually protect assets |
| **Climate mitigation (where relevant)** | Clean-energy adoption; biomass / emissions displaced | Applies to the energy-access experiments (EXP-02, EXP-08) |
| **Financial (paired)** | Repayment / loss curves, claims ratios, cost-to-serve | Paired with impact so the analysis can speak to *both* SDG and investor theses at once |

**Discipline:** output metrics (loans made, people reached) are logged but never reported *as* impact. The distinction is the whole point of the methodology.

## 2\. Identified how — causal design

Builds directly on the open questions already logged (OQ-4, OQ-5). **Direction set (2026-08-02): the flagship portfolio is 2–3 parallel, lean, pre-registered RCTs sharing a single verification partner** — so the partner (OQ-7, PT-05) and an anchor evaluation grant become gating prerequisites, not parallel nice-to-haves. Sharing one partner favors experiments with a *common measurement architecture*, which is one reason two of the three flagships are parametric (see the portfolio note below). The proposal still commits to a *hierarchy of preference* per pilot:

1. **Cluster-randomized rollout** — preferred where ethically and operationally feasible (randomize at the savings-group / village level). Cleanest identification. OQ-4 notes this is likely most feasible in a smaller, controlled site.  
2. **Stepped-wedge** — where partners resist withholding treatment; every cluster is eventually treated, order randomized. Often more acceptable to NGO partners (OQ-4).  
3. **Strong quasi-experimental** — matched difference-in-differences, regression discontinuity on an eligibility threshold — where randomization is impossible.

Cross-cutting design requirements:

- **Pre-registration** of hypotheses and analysis plan before rollout.  
- **Blinded outcome assessment** where feasible (the verification partner collects outcomes without knowing treatment status).  
- **Powered for the resilience effect**, not just the mean effect — the interesting outcomes are in the tails (what happens in a shock), which drives sample size.

**The flagship portfolio (OQ-11):** EXP-01 crop drought-index (rural smallholders), EXP-02 clean-energy PAYGO (energy / enterprise), EXP-06 multi-peril parametric climate cover (urban informal settlements). The two parametric lines (EXP-01, EXP-06) share a trigger → payout → loss-avoided measurement design, which is what makes running them in parallel under one partner affordable. EXP-06 spans several perils (flood, drought/heat, storm), but that raises *product* complexity, not *identification* complexity: access to the cover is randomized and resilience outcomes are measured whatever peril actually strikes.

## 3\. Verified by whom — independence

Impact the venture measures on its own products is not credible. The design separates the party that *structures* from the party that *measures*:

- An **independent verification partner** (academic field team / RCT lab) runs outcome measurement — this is OQ-7, and PT-05 (J-PAL) is the standing candidate.  
- **IRB / ethics approval** and a **data-sharing agreement** are preconditions, not afterthoughts.  
- Row-level participant data stays in the Vault (`05-raw-data`), never in the repo — only aggregate results come back (CLAUDE.md §8).

## 4\. Integration with the toolkit

The impact module is one of the five risk-tools, not a bolt-on. The same RT-1 origination schema that makes receivables poolable also carries the baseline covariates the causal design needs; the RT-3 monitor timestamps the shocks the resilience metrics are measured against. Designing impact measurement and securitization-readiness together is design principle 2 of the venture (`docs/research/working-doc.md`).

## Deliverable state

**Re-scoped 2026-08-22.** The methodology this document was a skeleton of is now written in `docs/research/research-framework.md`, which supersedes the sketch versions of identification, verification and integration held here. What remains live in *this* document is the outcome-metric menu in §1 \- the part the framework points back to.

Remaining work on the metric layer specifically:

- Fix **one primary outcome per estimand** with the verification partner before pre-registration (framework §5). Section 1 above is a menu; a pre-registered study needs a choice.  
- Pin the **shock-measurement instrument** and its recall period \- the load-bearing measurement, since every resilience claim is conditional on a shock having been observed.  
- Settle **comprehension** as a first-class measured outcome, not a fieldwork detail (framework §10).  
- Add outcome definitions for the experiment types the 2026-08-22 menu introduced that are not household-level at all: administrative-data studies, investor elicitation, and simulation (`data/experiments.csv`, `docs/research/experiment-spec-template.md`).

Still gated on OQ-7 (verification partner) and OQ-4. Feeds milestone M-08 (pilot design doc).  
