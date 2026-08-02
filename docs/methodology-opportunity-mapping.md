# Methodology: Mapping Underserved SDG Opportunities against Toolbox Capacity

**Status:** Skeleton (week of 2026-08-02) · **Owner:** BB · **Parent:** `docs/research-proposal.md` §2

## Purpose

Decide *where to point the research program first*. There are many climate-and-poverty problems
where finance is the binding constraint; we can only pilot a few. This methodology is a
repeatable way to rank candidate problems so the choice is defensible rather than intuitive.

It is a **two-axis** map:

- **Axis X — Opportunity size / potential.** How large and how unmet is the financing gap behind
  this problem, and how much climate-resilience / poverty-reduction impact would closing it
  unlock?
- **Axis Y — Toolbox capacity.** How well can *our* toolkit (RT-1…RT-5, the structuring layer)
  actually turn this problem into a feasible, poolable investment?

A problem that is huge but that our tools cannot make investable is a policy question, not our
question. A problem our tools fit perfectly but that barely moves any SDG outcome is a rounding
error. The interesting shortlist sits high on **both** axes.

```
 Toolbox      high │  build the tools,        │  FLAGSHIP —
 capacity          │  small prize (park)      │  pilot these first
 (Axis Y)          │--------------------------+--------------------------
             low   │  not ours                │  big prize, wrong layer
                   │  (refer out)             │  (watch / partner)
                   └──────────────────────────┴──────────────────────────
                        low  ── Opportunity size / potential (Axis X) ──  high
```

## Axis X — scoring the opportunity (skeleton)

Each sub-criterion scored 1–5; weights are **provisional and are OQ-9**.

| Sub-criterion | Question | Candidate source of evidence |
|---|---|---|
| Gap magnitude | How large is the unmet financing need (USD, # people)? | Adaptation-finance-gap and energy-access-gap literature (to anchor — see proposal §1) |
| Depth of need | How concentrated is the problem among the poor / climate-exposed? | Poverty and vulnerability data |
| Impact leverage | How much resilience / poverty reduction per dollar deployed? | Impact literature (Memo 2 + climate-resilience anchors) |
| Neglectedness | Is capital genuinely absent, or just cautious? | Blended-finance / mobilization literature (Memo 3) |
| Precedent signal | Has *anything* like this worked at pilot scale? | Experiment `Linked_Refs`, lit matrix |

## Axis Y — scoring toolbox capacity (skeleton)

Scored against the venture's actual toolkit, so the map stays honest about what we can build.

| Sub-criterion | Question | Tie to the toolkit |
|---|---|---|
| Data capturability | Can the cash flows be standardized at origination? | RT-1 schema (OQ-3) |
| Underwritability | Do community signals let us price the risk? | Underwriting engine (RT-2) |
| Monitorability | Can we detect trouble early enough to act? | Monitoring / early-warning (RT-3) |
| Poolability | Are the receivables homogeneous and transferable enough to aggregate? | Securitization modelling (RT-5); OQ-2, OQ-8 |
| De-riskability | Is there a plausible first-loss / blended structure? | Blended-finance design; OQ-6 |
| Verifiability | Can impact be measured credibly (for the impact thesis)? | Impact module; `methodology-impact-measurement.md` |

## Method

1. **Candidates in.** Start from `data/experiments.csv` (EXP-01…). Add others as they surface.
2. **Score** each candidate on both axes using the sub-criteria above.
3. **Weight and combine** — weights are OQ-9; until resolved, use equal weights and report the
   sensitivity, so no ranking depends on an unstated judgement call.
4. **Plot** onto the 2x2 and read the top-right quadrant.
5. **Shortlist** 2–3 flagship candidates → OQ-11 → feed the pilot / PhD field design.

## What this is not

- Not a claim that the un-shortlisted problems don't matter — only that they aren't the best fit
  for *this* toolkit *first*.
- Not a finished scoring model. Weights (OQ-9), and several Axis-X evidence anchors, are open.
  This skeleton fixes the structure; the calibration is the next milestone.

## Deliverable state

Skeleton only. Remaining work: resolve OQ-9 (criteria/weights), fill the Axis-X evidence anchors
(proposal §1 gaps), and run the first scoring pass over `data/experiments.csv`.
