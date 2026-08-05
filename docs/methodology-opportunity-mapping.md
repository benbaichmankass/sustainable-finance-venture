# Methodology: Mapping Underserved SDG Opportunities against Toolbox Capacity

**Status:** Skeleton (week of 2026-08-02) · **Owner:** BB · **Parent:** `docs/research-proposal.md` §2

## Purpose

Decide *where to point the research program first*. There are many climate-and-poverty problems where finance is the binding constraint; we can only pilot a few. This methodology is a repeatable way to rank candidate problems so the choice is defensible rather than intuitive.

It is a **two-axis** map:

- **Axis X — Opportunity size / potential.** How large and how unmet is the financing gap behind this problem, and how much climate-resilience / poverty-reduction impact would closing it unlock?  
- **Axis Y — Toolbox capacity.** How well can *our* toolkit (RT-1…RT-5, the structuring layer) actually turn this problem into a feasible, poolable investment?

A problem that is huge but that our tools cannot make investable is a policy question, not our question. A problem our tools fit perfectly but that barely moves any SDG outcome is a rounding error. The interesting shortlist sits high on **both** axes.

 Toolbox      high │  build the tools,        │  FLAGSHIP —

 capacity          │  small prize (park)      │  pilot these first

 (Axis Y)          │--------------------------+--------------------------

             low   │  not ours                │  big prize, wrong layer

                   │  (refer out)             │  (watch / partner)

                   └──────────────────────────┴──────────────────────────

                        low  ── Opportunity size / potential (Axis X) ──  high

## Axis X — scoring the opportunity

**Weighting resolved (OQ-9, 2026-08-02): research / evidence-first.** The score is dominated by how much credible impact evidence a pilot can produce, not by market size. Each sub-criterion is scored 1–5 and multiplied by the weight below.

| Sub-criterion | Weight | Question | Candidate source of evidence |
| :---- | :---- | :---- | :---- |
| Impact leverage | **High** | How much resilience / poverty reduction per dollar deployed? | Impact literature (Memo 2 \+ climate-resilience anchors) |
| Measurability / RCT-feasibility | **High** | Can the effect be identified cleanly with a lean randomized design? | Impact-measurement methodology; precedent studies |
| Depth of need | Medium | How concentrated is the problem among the poor / climate-exposed? | Poverty and vulnerability data |
| Precedent signal | Medium | Has *anything* like this worked — enough to be feasible, not so much it is already settled? | Experiment `Linked_Refs`, lit matrix |
| Gap magnitude / neglectedness | Low | How large / how capital-starved is the need? | Adaptation-finance-gap and energy-access-gap literature (to anchor — see proposal §1) |

*Measurability was promoted here from the toolbox axis (it was "verifiability"): under a research-first win condition it is the criterion that most reorders the ranking.*

## Axis Y — toolbox capacity (a filter, not a scored axis)

**Resolved (OQ-9): under research-first, the toolbox axis is a minimum-bar filter plus a light tie-breaker, not a heavily weighted score.** A candidate must clear a plausible-enough bar on the criteria below to stay in the running; among those that pass, toolbox fit only breaks ties. This keeps the poolable-asset thesis alive — nothing structurally hopeless can win — without letting asset economics override the cleanest study. (Verifiability has moved to Axis X as "measurability".)

| Sub-criterion (filter) | Question | Tie to the toolkit |
| :---- | :---- | :---- |
| Data capturability | Can the cash flows be standardized at origination? | RT-1 schema (OQ-3) |
| Underwritability | Do community signals let us price the risk? | Underwriting engine (RT-2) |
| Monitorability | Can we detect trouble early enough to act? | Monitoring / early-warning (RT-3) |
| Poolability | Are the receivables homogeneous and transferable enough to aggregate? | Securitization modelling (RT-5); OQ-2, OQ-8 |
| De-riskability | Is there a plausible first-loss / blended structure? | Blended-finance design; OQ-6 |

## Method

1. **Candidates in.** Start from `data/experiments.csv` (EXP-01…). Add others as they surface.  
2. **Score** each candidate on both axes using the sub-criteria above.  
3. **Weight and combine** — apply the resolved research-first weights (OQ-9): the Axis-X score leads, Axis-Y acts as a filter plus tie-breaker.  
4. **Plot** onto the 2x2 and read the top-right quadrant.  
5. **Shortlist** 2–3 flagship candidates → OQ-11 → feed the pilot / PhD field design.

## What this is not

- Not a claim that the un-shortlisted problems don't matter — only that they aren't the best fit for *this* toolkit *first*.  
- Not a finished evidence base. The weighting (OQ-9) is resolved, but several Axis-X evidence anchors (climate-financing-gap sizing, resilience-metric literature) are still gaps to fill.

## Deliverable state

Weighting resolved and a first scoring pass run (2026-08-02): flagship trio **EXP-01** (crop drought-index), **EXP-02** (clean-energy PAYGO), **EXP-06** (multi-peril parametric climate cover) — three uncorrelated risk drivers, recorded as OQ-11. Remaining work: fill the Axis-X evidence anchors (proposal §1 gaps) and firm the scores with the verification partner.  
