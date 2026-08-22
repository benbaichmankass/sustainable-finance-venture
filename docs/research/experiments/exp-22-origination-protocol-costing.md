# EXP-22 — Securitisation-ready origination protocol: randomised comparison with activity-based costing

**Status:** Specified
**Serves:** RQ-06 (lead), RQ-22 (lead sub), RQ-21 (secondary), RQ-01 (contributes) · **Composite:** 4.00 (Flagship candidate)
**Specced:** 2026-08-22

---

## 0. What writing this up changed

Two defects in the tracker row, both worth naming because they would have propagated into a proposal.

**The row names two primary outcomes.** "Marginal operational cost per household of the
fuller protocol; marginal gain in default predictability." The template allows one, for good
reason — two primaries is two experiments sharing a budget. Worse, the two run on
*incompatible clocks*: cost is observable within weeks of protocol launch, while default
predictability requires the loans to season. On a 6–12 month product that is a year or more
before the second outcome exists at all.

**Resolved:** cost is the primary outcome and the thing this experiment is *for*.
Predictability becomes a pre-registered follow-on measured on the same cohort once it
seasons — specified here in §7 so the data is captured from day one, but not gating.
Critically, **RQ-21 (which fields are load-bearing) can be answered earlier and more cheaply
on EXP-25's retrospective panels** than by waiting for this cohort to mature. That
reallocation is the single most useful thing this spec does.

**The row also assumes the control arm is a coherent protocol.** LIT-031 found that
cooperative internal credit funds are "often informal and unregulated", that weak internal
controls and accounting are "the most commonly observed deficiencies", and that credit
decisions "can be politically or personally motivated". Where the counterfactual is *that*,
the treatment is not "richer data capture" — it is "having a protocol at all", and the
measured cost is the cost of building basic accounting, which is a different and much larger
number. §5 makes originator type a design parameter rather than an afterthought.

---

## 1. The question

What does it cost, per household, to originate a community loan to a
securitisation-ready standard rather than to the originator's own standard — and does that
cost fall with portfolio size fast enough to be worth paying?

## 2. Hypotheses

**H1 (primary).** The marginal operational cost per household of the RT-1 protocol is
positive but bounded — small enough that it is plausibly recovered by improved funding terms
at realistic portfolio sizes. *Direction: positive cost.* *Rejected if* the marginal cost is
statistically indistinguishable from zero (implausible, and would suggest the protocols are
not actually different) **or** if it is so large that no realistic funding-cost saving
recovers it.

**H2.** Marginal cost per household **declines with cumulative volume** — a learning curve.
*Direction: negative slope on cumulative loans originated per officer.* This is the
hypothesis that determines whether the answer to H1 is a fixed tax or a start-up cost, and
they have opposite implications.

**H3.** The cost is concentrated in a **minority of the 57 fields**. *Rejected if* per-field
time is roughly uniform. If H3 holds, the deliverable is not a yes/no on the full schema but
a ranked cost curve, which is far more useful to an originator deciding what to adopt.

**H4 (secondary, deliberately not gating).** Loans originated under the fuller protocol
support materially better default prediction than those under the standard protocol.
Measured on the same cohort after seasoning. See §7 and §11.

**Null-result value.** A null on H1 in the *low* direction — the fuller protocol costs
essentially nothing extra — is the best possible result for the venture and would be a
genuinely surprising, publishable finding given how universally the cost is assumed to be
prohibitive. A very large cost is equally decision-useful: it kills the "design for
investability from day one" claim and redirects the thesis toward retrofit. **Both tails
change what we do**, which is the test for whether an experiment is worth running.

## 3. Why it matters

RQ-06 and the venture both rest on an untested assertion: that building for investability at
origination beats retrofitting it. Everyone in the sector repeats it. Nobody has priced it.

**If cost is low or falls quickly:** the origination schema (RT-1) stops being a design
document and becomes a costed proposition an originator can be asked to adopt. It also
unblocks the structuring thesis, because a pool built to a known standard is what makes
RT-5's output mean anything.

**If cost is high and flat:** the honest conclusion is that investability has to be
retrofitted from whatever the originator already collects, which changes RT-1 from a
specification into a mapping exercise and changes the venture's proposition substantially.

**Either way it is a number nobody has.** That is the whole case for running it, and it is
why this experiment survives the objection that it is operational rather than academic:
activity-based costing of a data-capture protocol, randomised, is a methods contribution to
a literature that currently argues about this from anecdote.

## 4. Design

**Identification.** Cluster-randomised comparison of two origination protocols, per
`research-framework.md` §4 rung 1. Unit of randomisation is the **branch** where branch
counts allow, otherwise the **loan officer**.

| | Treatment | Control |
|---|---|---|
| Protocol | Full RT-1 field set — 57 fields, 5 entities, 48 required, 45 critical-path | The originator's existing origination process, unchanged |
| Everything else | Identical — same products, pricing, approval authority, targets | |

**The cluster-count problem, stated plainly.** A mid-size originator has perhaps 10–40
branches. That is few clusters, and few clusters is the binding constraint on this design,
not sample size in households. Three responses, in order:

1. **Officer-level randomisation within branch** multiplies units, at the cost of
   contamination — officers in one branch share a supervisor, a workspace and habits, and
   the fuller protocol is learnable by observation. Contamination biases toward the null,
   so a positive H1 under officer randomisation is credible while a null is not.
2. **Stratify on branch size and portfolio maturity** before assignment; with few clusters,
   stratification does more for precision than anything else available.
3. **Multi-originator recruitment** to raise the cluster count, which also improves external
   validity. Costly in agreements, so it is the fallback rather than the plan.

**Fallbacks, with the condition that forces each:**

1. **Preferred — cluster-randomised branch assignment.** Requires ≥ ~20 branches at one
   originator, or pooling across two.
2. **Officer-level randomisation within branch.** Forced when branch count is too low.
   Report contamination risk and the resulting one-sided interpretation.
3. **Stepped wedge across branches** (framework §4 rung 2). Forced when the originator will
   not run two protocols concurrently but will sequence adoption. Costs: secular trends
   confounded with rollout, and the learning curve (H2) becomes hard to separate from
   calendar time.
4. **Time-and-motion study without randomisation.** Forced when no originator will vary
   protocol at all. This measures cost but cannot attribute it, and cannot address H2's
   learning curve credibly. It is a costing exercise, not an experiment — label it as such.

**Pre-registration** of H1, the cost definition, the field-level time allocation method and
the analysis plan, before enrolment.

## 5. Population and setting

Loan officers and originating groups at an originator willing to run two protocols side by
side. Sites are adaptable; what the design **needs**:

- **Enough clusters** — see §4. This is the first screening question for any partner, before
  enthusiasm.
- **An existing, documented standard protocol** so the control arm is a real counterfactual
  rather than an absence.
- **Branch-level operational accounting** good enough to support activity-based costing at
  all — staff time, supervision, rework.
- **A live origination pipeline** during the study window, at volume.

**Originator type is a design parameter, not a detail.** The treatment effect is defined
against whatever the control arm actually is, and LIT-031 shows that varies enormously:

| Control arm | What the treatment effect then measures |
|---|---|
| A professionalised MFI with a working MIS | The **marginal** cost of additional fields. The clean, intended estimand. |
| A cooperative internal credit fund with informal records | The cost of **building a protocol from near-zero**. Much larger, and not the same quantity. |

Both are worth knowing and they are different experiments. **Do not pool them into one
average.** If both originator types are available, treat type as a pre-specified moderator
and power for the MFI stratum as primary — the cooperative stratum will be underpowered but
descriptively valuable, and that asymmetry should be declared in advance rather than
discovered.

## 6. Intervention

**Treatment arm.** Officers originate using the full RT-1 field set, with:
- the RT-1 field definitions, enumerations and validation rules (no free text where a
  category is meant; ISO 8601 dates; money with currency and date; nulls distinguishable
  from zeros; `schema_version` on every row);
- whatever capture tool the originator already uses, extended — **not** a new app. A new tool
  would confound protocol cost with tool-adoption cost, which is the most likely way to get
  a large and meaningless answer;
- training, delivered once, with the hours logged as a study cost.

**Control arm.** The originator's existing process, entirely unchanged. This is a design
decision and not an absence: the control arm's protocol is *documented in detail at baseline*,
because the estimand is meaningless without knowing what it is measured against.

**Both arms** get identical supervision, targets and incentives. If the originator's
performance incentives reward speed, the fuller protocol is fighting them, and that has to be
recorded rather than neutralised — it is part of the real cost.

## 7. Outcomes

**Primary — one.** Marginal operational cost per household originated, treatment minus
control, in local currency and PPP, built by activity-based costing:

- officer time per origination (the dominant line), measured by timestamped capture logs
  where the tool supports it and by structured time-and-motion sampling where it does not;
- supervisory and quality-assurance time;
- rework and error-correction time, including records rejected by validation;
- training, amortised over the study cohort and reported separately so it can be
  re-amortised over a realistic horizon;
- any equipment or connectivity delta.

**Why timestamped logs matter:** self-reported time is the standard weakness of ABC studies
and is systematically biased. Where the capture tool can emit per-screen timestamps, that is
the measurement; where it cannot, time-and-motion sampling is second best and the
self-report is a validity check only, never the estimate.

**Secondary, by family, Benjamini–Hochberg within family:**

- *Cost-structure family* — the H2 learning curve (cost against cumulative originations per
  officer); the H3 per-field cost distribution and the resulting ranked cost curve.
- *Quality family* — completeness, validation pass rate, and rate of critical-path fields
  missing. A cheaper protocol that produces unusable records is not cheaper.
- *Burden family* — officer-reported burden and time-to-decision for the borrower. The
  borrower's time is a real cost that ABC on the originator's books will miss entirely.
- *Predictability family (H4, deferred)* — discrimination of a default model fitted on the
  treatment field set versus the control field set, on the same cohort after seasoning.

**On H4's clock.** Default outcomes are not available for a year or more. The spec's position
is: **capture the data from day one, commit to the analysis in the pre-registration, and do
not let it gate the primary result.** And note the cheaper substitute — **RQ-21's
load-bearing-fields question is better answered on EXP-25's retrospective panels**, which
already contain seasoned defaults. Sequencing those two experiments this way removes a year
from the critical path.

## 8. Data

- **Sources.** Origination records from both arms; timestamped capture logs; time-and-motion
  observation sheets; the originator's payroll and operational cost lines; a baseline
  document of the control protocol.
- **Ownership.** The originator's, under a data-sharing agreement.
- **Row-level borrower records** stay in the Vault's `05-raw-data` and never enter the repo,
  in any form (CLAUDE.md §8). What returns is cost parameters, distributions and model
  performance statistics.
- **Officer-level data is personal data.** Time-and-motion measurement of named staff is
  employment-sensitive and needs explicit consent and pseudonymisation at collection, not
  after. It also needs the originator's HR sign-off, which is a distinct approval from the
  data-sharing agreement and is easy to forget until it blocks the study.
- The **RT-1 validator** (`risk-tools/tools/validate_schema.py`) runs on the treatment arm's
  output as a quality measure and, usefully, as a live test of the schema itself — a field
  the validator constantly rejects is a schema defect, not an officer error.

## 9. Power

**Computable in structure, not in value.** Precision is driven by the **number of clusters**,
not households — see §4. Two parameters are missing:

| Parameter | Supplied by |
|---|---|
| ICC of origination time within branch/officer | Not in the literature for this setting. **A two-week time-and-motion pilot at one branch gives it directly**, and is the cheapest de-risking step available |
| Baseline mean and variance of origination time | Same pilot |

A precision analysis — achievable interval width on marginal cost per household, as a
function of cluster count — is produced from that pilot and **before** committing to a design.
Where it lands determines whether one originator suffices or a second is required. Quoting an
MDE now would be decoration.

Note the asymmetry: H1 needs only enough precision to distinguish "small" from "prohibitive",
which is a coarse question and therefore cheaper than a typical impact study. H2's learning
curve needs a longer panel per officer, and is the outcome most likely to be underpowered.

## 10. Partners

- **Originator:** an MFI or savings-group network with branch-level operations, or a
  cooperative union with an internal credit fund (§5 — different estimand). All `Not
  contacted` (M-03).
- **HR / staff representation** at the originator, for the officer-time measurement. Distinct
  approval; start it early.
- **No regulatory counterpart** expected for a protocol comparison, but confirm — OQ-1.
- Named individuals go in `private/partner-contacts.csv`, never here.

**The ask, and why this one is easier than EXP-25's.** This experiment gives the originator
something immediately usable: a costed answer to "what would it take for our book to be
investable", plus a validated field list, plus a time-and-motion baseline of their own
origination process that most originators do not have. Unlike EXP-25 it requires no
historical data disclosure — only permission to vary a process and to observe it. **That
makes it the better first ask of a new partner**, and the relationship it builds is what
makes the EXP-25 data request plausible later. Sequence outreach accordingly.

## 11. Timeline

| Stage | Gating |
|---|---|
| Time-and-motion pilot at one branch (§9) | **Not blocked.** Cheapest first move |
| Precision analysis and design choice | Follows the pilot |
| Pre-registration | Before enrolment |
| Data-sharing agreement + HR approval | **Gating, both.** HR is the one that gets forgotten |
| Ethics approval | Officer observation makes this non-trivial; allow real time |
| Protocol training and launch | |
| Origination window and ABC measurement | Primary outcome available here |
| **Seasoning gap** | A year or more before H4 is measurable |
| H4 predictability analysis | Deferred; pre-registered, not gating |

## 12. Risks

| Risk | Mitigation / fallback |
|---|---|
| **Too few clusters.** The main threat to this design. | Screen for cluster count before anything else. Officer-level fallback with one-sided interpretation; multi-originator recruitment. |
| **Contamination** under officer-level randomisation — the fuller protocol is learnable by watching. | Biases toward the null, so a positive H1 stays credible. Measure control-arm field completeness over time as a contamination indicator. |
| **Tool confound** — building a new capture app would measure tool adoption, not protocol cost. | Extend the existing tool. If that is impossible, say the estimate is an upper bound. |
| **Hawthorne effects** on observed officers. | Timestamped logs over observation where possible; run observation in both arms symmetrically; discard a lead-in period. |
| **Incentive conflict** — speed-based officer incentives penalise the fuller protocol. | Record it as part of true cost rather than neutralising it. Report cost with and without the incentive penalty. |
| **Control arm is not a protocol** (LIT-031). | Pre-specify originator type as a moderator; do not pool MFI and informal-cooperative strata. |
| **H4 never happens** because the study ends before seasoning. | Accept explicitly. RQ-21 is reallocated to EXP-25 for this reason. |
| **Ethical.** Officers may perceive time measurement as performance surveillance, and the data could be used that way. | Consent, pseudonymisation at collection, aggregate-only reporting back to management, and an explicit written commitment that individual data is not shared with supervisors. This is a condition of running the study, not a nicety. |

## 13. Cost and funding

Moderate — more expensive than EXP-25, cheaper than any field pilot. The dominant line is
observer time.

| Line | Note |
|---|---|
| Time-and-motion pilot | Small, and buys the power parameters |
| Enumerator / observer time | The largest line |
| Protocol training delivery | Also a measured outcome |
| Tool extension | Small if extending; large if building — avoid building (§12) |
| Data-sharing and HR legal review | Per originator |

**Target funders** (`data/funders.csv`): **FUND-04 FSD Africa** is the strongest fit —
financial-market and capital-market development is precisely the framing, and the deliverable
(a costed origination standard) is the kind of market infrastructure they fund. **FUND-01
IDRC** for the research and methods component. Both `Not researched`; specific calls not yet
identified, and that is a gap.

## 14. What it would take to abandon this

**Abandon if** no originator will vary its origination protocol *and* none will permit
observation, leaving only §4 rung 4 — which is not an experiment. At that point the honest
move is to publish the field-level cost model as a costed proposal with transparent
assumptions, and say the empirical test was not obtainable.

**Do not abandon** because H4 cannot be reached within the PhD. H1 alone answers RQ-22, is
publishable, and is the number the venture actually needs.

**Do not abandon** on a low-cost null. That is the best available result, not a failure.

---

## Provenance

Specced 2026-08-22, second entry in `docs/research/experiments/`. Anchors that shaped it:
**LIT-031** (Root Capital CFRI — informal internal credit funds, which redefines the control
arm). Depends on **RT-1** v0.1 (57 fields, 5 entities, 45 critical path) and on **OQ-3**,
`Partially answered`. Sequencing note recorded against **EXP-25**: RQ-21 moves there.
Template: `docs/research/experiment-spec-template.md`.
