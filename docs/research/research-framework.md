# Research framework

**Status:** v1 (2026-08-22) · **Owner:** BB
**Parent:** `docs/phd/research-questions.md` · **Detail layer:** `docs/research/methodology-impact-measurement.md`
**Implements:** RT-4 (impact evaluation module) · **Feeds:** RT-1 schema, RT-5 waterfall

## What this document is for

`docs/phd/research-questions.md` says what the project asks. This says how it would
answer it, in enough detail that a methods-minded supervisor can find the holes.

It is written to a specific standard: **a reader should be able to tell what would
have to happen for this project to fail.** Section 11 states that explicitly, and
the rest of the document is written so that section is answerable.

One framework covers all seven research-question strands because of the constraint
set out in the questions document: every strand is answerable from the same
fieldwork. What differs by strand is which estimand leads, not what gets collected.

---

## 1. Theory of change

The claim the project tests, stated as a chain so that each link can be attacked
separately:

```
  Community structure          ->  Low-cost screening, monitoring
  (repeat interaction,             and enforcement at small ticket
   local information)              sizes that formal lenders cannot match
            |
            v
  Standardised origination     ->  Cash flows that are recorded, verifiable
  (RT-1 schema, digital             and comparable across originators
   capture at point of sale)
            |
            v
  Bundled risk cover           ->  Fewer shock-driven defaults; lower
  (parametric or indemnity,         variance in the repayment stream;
   premium financed in)             better household outcomes in the tail
            |
            v
  Poolable asset               ->  Modelled loss distribution; credit
  (diversified across groups,       enhancement sized to it; institutional
   geographies, perils)             capital priced in
            |
            v
  Capital at scale             ->  More households reached than grant or
                                    DFI-only funding can reach
```

**Each arrow is a hypothesis, and each has a named threat:**

| Link | Hypothesis | The threat to it |
|---|---|---|
| 1 | Community structure produces genuine information rents | The rent may be in repeat interaction, not in the contract, and may not be transferable to an outside underwriter (LIT-020, LIT-021) |
| 2 | Standardisation is achievable at acceptable cost | Capture burden may exceed the value of the data; groups may refuse the intrusion (RQ-06, LC-19) |
| 3 | Bundling reduces default and stabilises cash flow | Basis risk may leave cover unfired when it is needed; financed premiums may worsen indebtedness (LC-03, LC-17) |
| 4 | Diversification makes the pool investable | Defaults may be covariate rather than idiosyncratic, in which case pooling buys much less than assumed (LC-08) |
| 5 | Capital arrives and is additional | Concessional capital may substitute rather than mobilise; the spread may not reach households (RQ-05, LC-12) |

**And one threat that runs across all of them:** the act of connecting the pool to
outside capital may destroy the mechanism in link 1. That is OQ-12 and OQ-13, and
this framework treats it as a primary hypothesis rather than a limitation - see §3.

---

## 2. Three estimands, three units of analysis

Most of the confusion in this project's earlier drafts came from sliding between
levels. The framework fixes three estimands and names the unit for each.

**Estimand A - household welfare.** Unit: the member household. The effect of
access to the product on resilience, consumption smoothing, asset retention and
adaptation behaviour. This is what a development-economics examiner reads first.

**Estimand B - contract performance.** Unit: the loan or policy. The effect of the
product design on default hazard, arrears trajectory, claims incidence and
prepayment. This is what a credit-risk examiner reads first, and it is measured on
the *same* contracts whose borrowers supply Estimand A.

**Estimand C - portfolio behaviour.** Unit: the simulated pool. The loss
distribution, correlation structure and enhancement requirement implied by
Estimand B, propagated through the RT-5 waterfall. This is not a field estimand -
it is an extrapolation, and §9 is explicit about how far it can be pushed.

The design's efficiency comes from A and B being measured on the same randomisation
at no extra allocation cost. The design's honesty comes from C being labelled a
model output rather than a finding.

---

## 3. The core design: two-layer randomisation

This is the design contribution, and it is what to put in front of an advisor.

**Layer 1 - product access.** Randomise at the group or village level: treatment
groups receive the credit product with cover bundled in; control groups receive the
credit product alone. Standard, well-precedented, identifies Estimands A and B.

**Layer 2 - funding source.** Within the treated arm, randomise whether the loan
fund is the group's own accumulated savings or externally supplied wholesale
capital, with contract terms held constant.

Layer 2 is the unusual one, and it is the whole reason this is a thesis rather than
a product trial. The literature this repo has assembled establishes that the
joint-liability *contract* is not what drives repayment (LIT-020), and points
instead at repeated interaction and the informal risk-sharing it builds (LIT-021).
Ghatak and Guinnane (LIT-022) show information and sanction channels can trade
against each other. Tankha (LIT-023) records that the longest-running successful
joint-liability institution funded itself from local deposits.

Securitisation is exactly the substitution of outside money for community money.
**No study in the matrix randomises that substitution.** Layer 2 does, and it
converts the project's biggest vulnerability into its most publishable result:

- If repayment behaviour is unchanged under external funding, the pooling thesis
  clears its hardest obstacle and the finding is important on its own terms.
- If repayment degrades, the project has identified the binding constraint on an
  entire class of financial-inclusion structuring proposals - a more valuable
  contribution than a successful pilot, and one that would reorient the venture
  toward the group-level structure of OQ-13.

Either result is publishable. A design where only one outcome is interesting is a
design with a problem.

**Practical caveats, stated rather than hidden.** Layer 2 needs partner willingness
to vary funding source, which is a real negotiation and may fail; it needs enough
clusters to support a second factor, which pushes on power (§6); and it raises a
fairness question if externally funded groups can lend more, which is handled by
holding lending capacity constant by design rather than letting the funding source
change the loan volume.

---

## 4. Identification hierarchy

Per pilot, in strict order of preference. The condition that forces each fallback
is named, because "we will use quasi-experimental methods if necessary" is not a
plan.

1. **Cluster-randomised trial.** Randomise at group or village level. Preferred
   always. Requires: enough clusters for power, a partner willing to withhold, and
   ethics approval for withholding a product believed beneficial.
2. **Stepped wedge.** Every cluster is treated eventually; the order is randomised.
   Forced when a partner will not withhold but will sequence. Costs: exposure to
   secular time trends, and a stronger reliance on correct modelling of time effects.
3. **Matched difference-in-differences.** Forced when rollout order is determined by
   the partner rather than by us. Requires a credible parallel-trends argument with
   pre-period data, which means the partner's historical MIS becomes a precondition.
4. **Regression discontinuity.** Available only where a sharp eligibility threshold
   exists (a group age, size or savings-balance cut-off). Narrow external validity,
   but clean where it applies.

**Cross-cutting requirements, applying to all four:**

- **Pre-registration** of hypotheses, primary outcomes and the analysis plan before
  enrolment, on a public registry.
- **Blinded outcome assessment** where feasible: the verification partner collects
  outcomes without knowing treatment status (OQ-7).
- **A pre-specified primary outcome.** One. Everything else is secondary and
  labelled as such, with multiple-hypothesis correction across each outcome family.
- **Spillover measurement.** Savings groups in a village talk to each other.
  Randomising at group level within a village invites contamination; randomising at
  village level costs power. The design assumes village-level randomisation with
  group-level measurement, and measures spillovers to untreated groups in treated
  villages explicitly rather than assuming them away.

---

## 5. Outcomes and instruments

The full metric menu lives in `methodology-impact-measurement.md` §1 and is not
duplicated here. What this section adds is the discipline around it.

**One primary outcome per estimand.** Provisionally: for Estimand A, a
consumption-smoothing measure conditional on shock exposure; for Estimand B,
90-day-past-due incidence over the loan cycle. Both to be fixed with the
verification partner before pre-registration, not after seeing data.

**Output metrics are logged and never reported as impact.** Loans disbursed,
premiums collected and people reached are operational facts. The distinction is the
methodology's whole point.

**Shock measurement is the load-bearing instrument.** Every resilience claim is
conditional on a shock having occurred, which means the shock must be measured
independently of the outcome and of self-report where possible. Three sources,
triangulated: the parametric index itself (objective, but subject to basis risk),
administrative and remote-sensing data, and a household shock module with a fixed
recall period. Where the index says no shock and the household says shock, that
disagreement is *itself* a finding about basis risk (RQ-25) and is recorded as data
rather than resolved by preference.

**Timing follows the shock, not the calendar.** Standard baseline / midline /
endline rounds can miss the event the whole design is about. The framework adds a
trigger-activated round: when the index fires or a shock is otherwise recorded, a
short survey goes out within a defined window. This is an operational commitment
with cost implications, and it needs to be in the grant budget from the start.

---

## 6. Power, and what is not yet known

The method, stated honestly, with parameters marked as to be calibrated. **No
minimum detectable effect is asserted in this document, because the inputs are not
yet in the repo.**

Sizing proceeds in this order:

1. **Intra-cluster correlation** for each primary outcome, taken from the
   savings-group RCT literature (LC-01, LC-26) - not assumed. This is the single
   parameter that most determines whether the study is feasible, and it is
   currently unknown to this project.
2. **Number of clusters, then households per cluster.** For clustered designs,
   cluster count dominates; adding households inside a fixed number of groups buys
   very little. This constrains partner selection more than budget does.
3. **Power for the conditional effect, not the mean effect.** The interesting
   outcome is what happens to households that get hit by a shock. If shock incidence
   in the study period is materially below one, the effective sample for the primary
   analysis is a fraction of the enrolled sample, and the study must be sized for
   that fraction. This is the most common way a resilience study fails.
4. **The second factor.** Layer 2 splits the treated arm. Either the design accepts
   lower power on the interaction, or it powers the main effect and treats Layer 2
   as exploratory and clearly pre-labelled as such.
5. **Simulation-based power.** Given the clustering, the conditional structure and
   the second factor, closed-form formulas will mislead. Power is computed by
   simulation against the actual planned analysis - which is also a check that the
   analysis code exists before enrolment starts.

**Open until calibrated:** ICCs, expected shock incidence, take-up under automatic
versus opt-in cover, and baseline default rates. Each traces to a literature
component or to partner MIS access. Until they are in hand, any MDE this project
quotes would be decoration.

---

## 7. Verification and pre-registration

Impact the venture measures on its own products is not evidence. The design
separates the party that structures from the party that measures:

- An **independent verification partner** runs outcome measurement (OQ-7, currently
  gating; PT-05 is the standing candidate).
- **Pre-registration** before enrolment, with the analysis plan attached.
- **IRB / ethics approval** and a **data-sharing agreement** are preconditions, not
  parallel tasks.
- **Row-level participant data never enters this repo** - Vault `05-raw-data` only,
  aggregate results back (CLAUDE.md §8).

The reason to accept the cost and delay: the project's commercial thesis depends on
an investor believing the impact claim. A claim the venture verified itself is worth
approximately nothing to that reader, so the independence is a commercial asset and
not only an academic nicety.

---

## 8. Data architecture

The RT-1 origination schema does double duty, and that is a design decision rather
than a convenience: the same record that makes a receivable poolable also carries
the baseline covariates the causal design needs.

| Field group | Serves securitisation | Serves identification |
|---|---|---|
| Contract terms, disbursement, schedule | Cash-flow modelling, data tape | Treatment definition |
| Repayment events, arrears, restructuring | Default hazard, loss curves | Estimand B outcomes |
| Group identity, meeting frequency, attendance | Originator quality signal | Mechanism covariates (LIT-021) |
| Geospatial and agro-climate tags | Correlation and concentration analysis | Shock exposure, clustering |
| Claims and trigger events | Actuarial pricing | Treatment intensity, basis-risk analysis |
| Baseline household characteristics | Underwriting inputs | Covariate adjustment, heterogeneity |

**The deadline that is easy to miss:** fields can be added freely until collection
starts, and cannot be backfilled afterwards for loans already originated. OQ-3 and
OQ-12 have to be settled *before* first deployment, not during. Meeting frequency
and attendance are candidate first-class fields on the strength of LIT-021, and if
they are not in v1 of the schema the mechanism analysis is unavailable for the first
cohort.

---

## 9. The risk-modelling layer, and its limits

The bridge from field evidence to structuring, and the part most likely to be
overclaimed:

1. Estimand B outputs become the inputs to survival and hazard models for
   time-to-default and time-to-claim (LC-07).
2. Loss given default is estimated from observed recoveries - with the caveat that
   few will be observed in a short pilot, which is a known weak point rather than a
   detail.
3. Correlation across groups, geographies and time is estimated where the design
   spans enough units, and bounded by assumption where it does not (LC-08).
4. These feed the RT-5 waterfall to size tranches and first-loss requirements
   against investment-grade benchmarks.

**Three limits, stated up front rather than in a footnote:**

- **The panel is too short.** Credit-risk models calibrate against multi-year
  loss-emergence patterns. Three or four years of pilot data produces provisional
  parameters, and every downstream number inherits that. Findings are reported as
  bounded ranges under stated assumptions, never as point estimates.
- **Correlation is the parameter the pilot can least estimate and the structure most
  depends on.** A single-site pilot has almost no power to estimate cross-site
  correlation. This is the strongest argument for either a multi-site design (RQ-08)
  or access to historical partner MIS across regions (EXP-25).
- **Extrapolation to a rated structure is a model output.** No rating agency has
  engaged with this asset class at community level, and until one does, any
  investment-grade claim is a simulation result and is labelled as one.

---

## 10. Ethics and do-no-harm

Not a compliance section. Three design constraints follow from it:

- **Over-indebtedness.** Financing a premium into loan principal increases the
  amount owed. If cover fails to fire when a shock hits, the household is worse off
  than under a loan-only counterfactual. The design must measure that downside case
  explicitly and pre-specify it as a harm outcome, not discover it afterwards.
- **Mis-selling and comprehension.** A parametric product that pays on an index
  rather than on loss is genuinely hard to explain. Comprehension is measured at
  baseline and treated as a first-class outcome; a product participants do not
  understand has not been meaningfully consented to.
- **Consent and power asymmetry.** Consent appropriate to the local literacy and
  language environment, obtained by a party without a stake in take-up. Where the
  originating partner also sells the product, they cannot be the party taking
  consent for the research.

Withholding a product believed beneficial is the standard ethical objection to
arm 1. The honest answer is that the product is *not* known to be beneficial - that
is what the study is for - and that the stepped-wedge fallback exists precisely for
partners who do not accept that reasoning.

---

## 11. What would falsify this

The section that makes the rest of the document checkable. Any one of these results
would require abandoning or fundamentally restructuring the thesis, and each is
attached to the experiment that would produce it.

| Finding | Consequence | Where it comes from |
|---|---|---|
| Repayment degrades materially when external capital replaces community money, with no structural fix | The pooling thesis fails at the mechanism. Pivot to the group-level structure (OQ-13) or abandon | Layer 2 / EXP-13 |
| Default is dominated by covariate rather than idiosyncratic risk | Diversification buys little; enhancement costs swamp the spread; the asset is not poolable on these terms | EXP-25, RQ-13 |
| Marginal cost of securitisation-ready capture exceeds the value it unlocks at realistic pool sizes | The structuring layer has no business model. RT-6 already puts break-even far above pilot scale | EXP-22, OQ-2, RT-6 |
| Bundling shows no effect on either resilience or repayment stability | The flagship intervention is not the intervention. The question survives; the product does not | EXP-01, EXP-06 |
| No investor will price the asset at any disclosure level short of a track record no pilot can produce | The capital-mobilisation link is broken regardless of asset quality | EXP-23, EXP-24 |

Two of these - covariate dominance and the cost of capture - are testable **before**
any field pilot, on administrative data and a costing exercise. That ordering is
deliberate: the cheap experiments that could kill the thesis should run first.

**This is now the adopted work sequence, not a recommendation.** OQ-15 was resolved on
2026-08-22 in exactly these terms: EXP-25 (correlation) and EXP-22 (capture cost) are
`Selected` and run before any field commitment; a single field anchor follows. OQ-16
then fixed the anchor's **setting** on 2026-08-22 - the coffee cooperative cluster -
leaving only the instrument open between EXP-09 and EXP-10. Whichever is chosen carries
the second randomisation layer above, since that layer is the design contribution and it
needs a field setting to live in.

---

## 12. What this framework still needs

Honest state, so this document is not read as more finished than it is:

- **Power parameters** (§6) - blocked on LC-01, LC-26 and partner MIS access.
- **Primary outcome definitions fixed** - blocked on the verification partner (OQ-7).
- **The pre-registration template** - drafted next; feeds M-08.
- **Confirmation that Layer 2 is operationally acceptable to a partner** - the
  design's most novel element is also its most likely to be negotiated away.
- **Whether bundling has already been trialled this way** (LC-04). If it has, §3's
  novelty claim moves entirely onto Layer 2.
