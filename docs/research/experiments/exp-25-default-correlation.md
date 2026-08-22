# EXP-25 — Default correlation on partner management-information-system data

**Status:** Specified
**Serves:** RQ-03 (lead), RQ-13 (lead sub), RQ-28 (secondary) · **Composite:** 4.10 (Flagship candidate)
**Specced:** 2026-08-22 · **Supersedes** the tracker row's single-correlation framing — see §0.

---

## 0. What changed, and why this is a respec rather than a first spec

The tracker row asks whether defaults are "covariate rather than idiosyncratic" and proposes
to estimate "default correlation across groups, regions, time and agro-climatic zones."

**That framing is now known to be too coarse.** Three anchors read on 2026-08-22 say the
covariate component is real but arrives through **two separable channels**, and that
collapsing them into one number would hide the finding rather than produce it:

| Channel | Evidence | Behaves like |
|---|---|---|
| **Environmental** — weather, pathogen, commodity price | LIT-031 (leaf rust across >50% of Central America's coffee area at once; El Salvador −60%; 80% output drops at some financed producer organisations), LIT-035 (45 of 260 days excessively variable), LIT-030 (basis risk) | A geographic/agro-climatic factor. Diversifiable across regions, in principle. |
| **Institutional** — market saturation, multiple borrowing, contagion | LIT-036 (four national repayment crises; PAR>30 above 10% in three of four markets; the global recession **explicitly rejected** as primary cause), LIT-037 (individual MFI growth does *not* predict deterioration; **market-level** borrower growth >63%/yr and active loans >10% of population **do**) | A **market**-level factor. **Not** diversifiable by adding lenders within the same market. |

The second row is the one that matters and the one the original framing would have missed.
If the operative factor is market penetration rather than lender behaviour, then a pool
assembled from several MFIs in one country is **not** diversified against the thing that
historically predicts trouble — it may be concentrated in it. That is a direct challenge to
the pooling thesis and it is testable on data that already exists.

A single pooled correlation coefficient cannot distinguish those cases. A variance
decomposition can.

**The respec, in one line:** stop estimating *a* correlation; estimate *which levels* the
variance sits at, and report the parameter RT-5 and the Pluto-Tasche bound actually consume.

---

## 1. The question

At which levels — borrower, group, branch, agro-climatic zone, lender, market — does the
variance in community-originated loan default actually sit, and is the market level large
enough to defeat diversification within a country?

## 2. Hypotheses

**H1 (primary).** The market-level variance component is non-zero and material — operationally,
it accounts for at least as much of total default variance as the agro-climatic component.
*Rejected if* the market-level intra-class correlation is indistinguishable from zero once
agro-climatic zone and time are absorbed.

**H2.** Default correlation rises with market penetration. Portfolio segments in
market-years above LIT-037's thresholds (borrower growth >63% p.a.; active loans >10% of
population) show higher within-market default correlation than segments below them.
*Direction: positive.* This is the direct test of LIT-037 on loan-level rather than
market-aggregate data, which has not been done.

**H3.** The environmental and institutional components are **separable** — that is, a model
with both levels fits materially better than either alone, and the two do not simply proxy
each other. *Rejected if* including both leaves one indistinguishable from zero.

**H4 (secondary, serves RQ-28).** Some variance components are portable across sites and
some are not. Specifically, the borrower- and group-level components are more stable across
countries than the market-level component.

**Null-result value.** If H1 is rejected — market level near zero, variance concentrated at
borrower and group level — that is a *strong positive* for the pooling thesis and the single
most valuable result this project could produce cheaply. It is not a failed experiment.
This is stated deliberately: an experiment whose null is uninformative should not be run,
and this one's null is highly informative in both directions.

## 3. Why it matters

**If the market component is large:** geographic diversification across regions within a
country does not work, tranching has to be sized against a fatter tail than RT-5 currently
assumes, and the venture's structuring proposition needs a cross-*market* pool — which is
materially harder, slower and more expensive to assemble. Better to know before building.

**If it is small:** the pooling thesis survives its sharpest available falsification test,
and RT-5 gets a defensible correlation input instead of a sweep. That is the single result
that most improves the proposal's credibility with a finance-side supervisor.

**Either way it supplies a missing parameter, not just a finding.** LIT-038 shows the
standard method for estimating a default probability in a portfolio with no observed
defaults — Pluto–Tasche — returns the PD as an upper confidence bound that is *a function of
an asset correlation supplied by assumption*. RT-5's own documentation says correlation "is
the parameter that matters most" and currently handles it with a sweep from independence to
near-perfect correlation. This experiment is what converts that sweep into a range with
evidence behind it.

## 4. Design

**Not a trial.** This is a retrospective multi-level variance-components study on
administrative panels. The identification hierarchy in `research-framework.md` §4 governs the
field pilots and does not apply here; there is no assignment mechanism and no causal claim
about an intervention. The claim is descriptive and structural, and should be presented that way.

**Estimand.** A variance decomposition of the loan-level default indicator across a nested
and partially crossed hierarchy:

```
borrower  ⊂  group  ⊂  branch  ⊂  agro-climatic zone  ⊂  lender  ⊂  market(country)
                                     ×  time (origination cohort × calendar period)
```

Lender and agro-climatic zone are **crossed**, not nested — several lenders operate in the
same zone, and one lender spans several zones. That crossing is exactly what identifies the
institutional channel separately from the environmental one, and it is the reason the study
needs **more than one lender per market**. A single-lender dataset cannot answer H1 and
should not be presented as if it could.

**Specification.** A hierarchical generalised linear mixed model with a binary default
outcome and random intercepts at each level, reporting intra-class correlations by level and
their uncertainty. A discrete-time survival specification with the same random-effects
structure is the preferred form where origination dates and censoring are recorded, because
it handles loans still outstanding correctly rather than dropping them.

**Translating to the parameter the tools need.** The mixed-model ICCs are not directly the
asset correlation that RT-5 and Pluto–Tasche consume. The spec therefore includes an explicit
mapping step: fit a single-factor Vasicek-style latent-variable model to the same data to
recover an asset correlation ϱ per level, and report *both* — the ICC decomposition, which is
the research finding, and ϱ, which is the engineering input. Reporting only the first would
leave the tools uncalibrated; reporting only the second would hide the decomposition.

**Fallbacks, with the condition that forces each:**

1. **Preferred — multi-lender, multi-market loan-level panel.** Answers H1–H4.
2. **Multi-lender, single-market.** Forced when only one country's originators share.
   Market level is no longer identified; H1 and H2 drop, H3 partially survives via
   branch × zone crossing. **Say so explicitly rather than reporting a market ICC of zero.**
3. **Single-lender, multi-branch panel.** Forced when only one originator shares. This
   identifies borrower, group, branch and zone components only. It cannot address the
   institutional channel at all and should be published as a component study, not as a test
   of the pooling thesis.
4. **Aggregate market-level panel** (MIX / Atlas-style institution-year data). Forced when no
   loan-level data is obtainable. This replicates LIT-037's level of analysis rather than
   improving on it, so it is a literature contribution at best. Treat as the floor, not a plan.

**Pre-specification.** Even though this is observational, the level structure, the primary
estimand (the market-level ICC), the penetration thresholds for H2, and the model
specification are registered before the data is received. A variance decomposition has a
great many defensible specifications, and choosing among them after seeing the data is how
this kind of study loses its credibility.

## 5. Population and setting

Existing loan portfolios of savings-group networks, MFIs and cooperative internal credit
funds. Sites are not named prematurely; what the design **needs** is:

- **at least two lenders per market**, otherwise the institutional channel is unidentified;
- **at least two markets**, otherwise H1's comparison has no contrast;
- **loan-level records with a group or branch identifier and a location** precise enough to
  join to an agro-climatic zone;
- **a panel long enough to contain at least one covariate shock** — a drought, a price
  collapse, a pathogen outbreak, or a repayment crisis. A quiet period estimates the
  idiosyncratic component well and the covariate component not at all, which is the failure
  mode most likely to produce a falsely reassuring answer.

The coffee cooperative setting chosen under OQ-16 is a strong candidate source precisely
because LIT-031 documents a shock large enough to identify the environmental component
(2012–2015 leaf rust). Note the tension honestly: cooperative internal credit funds are
described by their own lender as "often informal and unregulated" with weak accounting
(LIT-031), so record quality is the binding constraint on whether they can supply usable data.

## 6. Intervention

None. Retrospective study on data that already exists. No control arm, no delivery, no
participant burden.

## 7. Outcomes

**Primary.** The market-level intra-class correlation of loan default, with its confidence
interval.

**Secondary, by family, with Benjamini–Hochberg correction within each family:**

- *Decomposition family* — ICC at each of borrower, group, branch, zone and lender levels.
- *Penetration family* — the H2 interaction between market-penetration indicators and
  within-market correlation.
- *Portability family* — cross-market stability of each component (H4, RQ-28).
- *Engineering family* — the recovered asset correlation ϱ by level, and the implied
  first-loss thickness when fed to RT-5.

**Definition discipline.** Default is defined once, in advance, as a specified days-past-due
threshold, and every lender's data is mapped onto it. LIT-036 is explicit that write-off
policy is at each board's discretion and that PAR comparisons across institutions are soft
for exactly this reason — so the study reports results on a harmonised definition **and**
on each lender's native definition, and shows whether the conclusion survives the choice.

## 8. Data

- **Sources.** Partner management-information-system extracts; agro-climatic zone from public
  gridded climate data joined on location; market penetration from public sector statistics.
- **Ownership.** The partner's. Governed by a data-sharing agreement per originator.
- **Row-level records** stay in the Vault's `05-raw-data` and never enter the repo — not as a
  CSV, not as a summary table, not in the dashboard (CLAUDE.md §8). What returns to the repo
  is estimated parameters and their uncertainty.
- **Minimum fields:** loan identifier, group/branch identifier, origination date, maturity,
  amount, repayment or arrears history sufficient to construct the default indicator,
  censoring status, and a location at least as fine as district.
- **Personal identifiers are neither needed nor requested.** The ask is pseudonymised. This
  is worth stating in the first email — it materially lowers the barrier to a yes.

## 9. Power

**Not yet computable, and the reason is specific rather than a placeholder.** The quantity
that determines precision here is the number of **level-5 and level-6 units** — lenders and
markets — not the number of loans. A million loans across one lender in one market gives a
market-level ICC with no precision at all.

What is missing and where it comes from:

| Parameter | Supplied by |
|---|---|
| Prior on group- and branch-level ICC | LC-01 and LC-26; not yet read |
| Prior on market-level ICC | **Nothing in the literature — this is the gap the study fills.** LIT-037 is the closest and is measured at market aggregate, not loan level |
| Shock incidence in the panel window | The partner data itself, once obtained |
| Number of lenders and markets available | M-32 / M-03 outreach |

A precision analysis — what interval width is achievable for a given number of lenders and
markets — is written **before** the data arrives and is the deliverable that tells us whether
a given partner combination is worth the effort. Quoting an MDE now would be decoration.

## 10. Partners

- **Origination data:** MFI networks, savings-group networks, cooperative unions and
  value-chain lenders. All `Not contacted` (M-03). **Two per market is the design minimum.**
- **Sector repositories:** as a fallback source of aggregate panels, and as a route to
  introductions.
- **No regulatory counterpart required** for pseudonymised retrospective data in most
  jurisdictions, but confirm per market — this is a question for OQ-1's counsel scan.
- Named individuals go in `private/partner-contacts.csv`, never here.

**The ask, sharpened by this respec.** The request is no longer "share your portfolio data".
It is: *pseudonymised loan-level records covering a period that includes a shock, from two
lenders in the same market*. That is a more specific request, which is usually easier to
grant, and it comes with something to offer in return — every participating lender gets its
own decomposition back, which is a number none of them currently has about their own book.

## 11. Timeline

| Stage | Gating |
|---|---|
| Pre-specification and precision analysis | None — can start now |
| Data-sharing agreements | **Gating, and the one that slips.** Allow far longer than feels reasonable |
| Ethics review | Light for pseudonymised secondary data, but not zero; institution-dependent |
| Data receipt, harmonisation, default-definition mapping | Gating on the above |
| Estimation and the ϱ mapping step | Short once data is in hand |
| Feed to RT-5, re-run the first-loss sizing | Short |

Stages 1 and the precision analysis are **not blocked by anything** and are the honest
starting point.

## 12. Risks

| Risk | Mitigation / fallback |
|---|---|
| **No partner shares loan-level data.** The single most likely failure. | Fallback ladder in §4. Lead with the sharpened, pseudonymised, two-lender ask; offer the decomposition back. |
| **Quiet panel** — no covariate shock in the window, so the covariate component is near-zero by construction and reads as a reassuring result. | Screen the window for a shock *before* accepting a dataset. Report shock incidence alongside every estimate. This is the most dangerous failure because it looks like success. |
| **Single lender per market** — institutional channel unidentified. | Report it as unidentified. Do not present a near-zero market ICC that the design could not have detected. |
| **Definition heterogeneity** across lenders (LIT-036's write-off-discretion point). | Harmonised definition plus native-definition robustness, both reported. |
| **Survivorship** — lenders that failed in a crisis do not survive to share data, which biases the covariate component *downward*. | Acknowledge as a signed bias. Seek at least one dataset from a market that had a documented crisis (LIT-036 names four). Bound the bias rather than ignoring it. |
| **Selection into sharing** — better-governed lenders share, and they are exactly the ones with lower institutional correlation. | Same direction as survivorship: the estimate is a **lower bound** on the institutional component. State that in the abstract, not the appendix. |
| Model misspecification across many defensible hierarchies. | Pre-specification; report specification-curve style sensitivity. |
| **Ethical.** Re-identification risk from fine location joined to loan records. | Coarsen location to the level the agro-climatic join actually needs. Vault-only row-level storage. No individual records leave the partner's definition of acceptable. |

## 13. Cost and funding

Cheap by design — the dominant costs are legal and human, not fieldwork.

| Line | Note |
|---|---|
| Data-sharing agreement legal review | Per originator; the real cost |
| Data engineering and harmonisation | The bulk of the analyst time |
| Compute | Negligible |
| Travel for partner relationship-building | Modest, but probably decisive for getting a yes |

**Target funders** (`data/funders.csv`): **FUND-04 FSD Africa** — financial-sector development
is exactly this, and they have convening power with African originators, which is worth more
than the money here. **FUND-02 3ie** and **FUND-01 IDRC** for the research component.
**FUND-03 J-PAL K-CAI** is a weaker fit for a non-experimental study and should not be led
with. Specific calls to be identified — none logged yet.

## 14. What it would take to abandon this

**Abandon if:** after a genuine outreach effort across at least two markets, no originator
will share loan-level data under any terms, *and* the aggregate fallback (§4.4) would only
replicate LIT-037. At that point the parameter cannot be obtained and the honest move is to
say so in the proposal — an identified, documented, unfillable data gap is itself a
contribution, and it is a better one than a study run on data that cannot answer the question.

**Do not abandon if** the first estimate is imprecise. A wide interval on the market-level ICC
is still the first loan-level estimate of that parameter for this asset class, and RT-5 can
consume a range.

**Do not treat a null on H1 as failure.** See §2.

---

## Provenance

Respecced 2026-08-22 following the LC-08 first pass. Anchors that changed the design:
**LIT-036** (CGAP Focus Note 61), **LIT-037** (CGAP over-indebtedness survey), **LIT-038**
(Pluto–Tasche for low-default portfolios), **LIT-031** (Root Capital CFRI), **LIT-035** (ICO),
**LIT-030** (basis risk). Bears on **OQ-17** candidate relocation (b), **OQ-2**, and **RT-5**'s
correlation input. Template: `docs/research/experiment-spec-template.md`.
