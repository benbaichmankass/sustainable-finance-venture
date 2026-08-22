# Proposal workplan: from here to a supervisor saying yes

**Status:** v1 (2026-08-22) · **Owner:** BB
**Provenance:** built from the repo's existing state, incorporating structure from an external planning draft (question families, governance-variation experiments, the experiment-spec template, and the escalating-length application bundle).

## What this is

The coordination backbone for the PhD track. Everything else added on 2026-08-22 is
a component this sequences:

| Deliverable | Lives in | State |
|---|---|---|
| Research questions | `docs/phd/research-questions.md` + `data/research-questions.csv` | Done |
| Literature decomposition | `docs/research/research-agenda.md` v2 + `data/lit-components.csv` | Done - reading not started |
| Research framework | `docs/research/research-framework.md` | Done - parameters uncalibrated |
| Experiment menu | `data/experiments.csv` + `docs/research/experiment-spec-template.md` | Done - portfolio unresolved (OQ-15) |
| Application pack | `docs/phd/application-pack.md` + the Vault folder | Done - CV and specifics outstanding |

## The honest state of things

Worth being direct about where this actually stands, because the artifacts can make
it look further along than it is.

**What is genuinely strong:** the evidence base, the structuring analysis, the
toolchain, and a research question with a real tension in it. A supervisor reading
the master proposal will not think this is a beginner.

**What is thin:** three of the nine P1 literature components have zero anchors,
including LC-04 (bundled credit and insurance), which is the component the
proposal's central novelty claim depends on. No power parameters exist. No partner
has been contacted. No verification partner is secured, and OQ-7 gates the entire
field programme.

**What that means for sequencing:** outreach does not have to wait for all of it,
but it does have to wait for LC-04. Approaching a microinsurance economist while
unable to say whether the bundling trial has already been run is the one avoidable
way to waste a first contact.

---

## Phase 1 - close the P1 literature gap

**Weeks 1 to 6. Gates: a credible proposal. Blocks: Phase 3.**

Nine components, roughly 77 new anchors. `docs/research/research-agenda.md` has the
pace argument and the two-pass method.

Order within the phase, which is not arbitrary:

1. **LC-04 first** (bundled credit and insurance). It can invalidate the novelty
   claim. Find out in week one, not week six.
2. **LC-03 and LC-05** (index insurance; resilience measurement). These make the
   flagship experiments describable in a supervisor's own vocabulary.
3. **LC-07 and LC-08** (credit-risk modelling; portfolio correlation). RQ-03 has no
   methodological anchors at all, and LC-08 underpins a falsification test.
4. **LC-09, LC-06, LC-02, LC-01** in whatever order access allows.

Output: memos 5, 6 and 7 drafted. Each memo ends with an implications section - that
section is what actually gets reused in the proposal.

**Done when:** the nine components are `Reviewed` and the three memos exist. Not when
the anchor count is hit.

## Phase 2 - harden the framework

**Weeks 4 to 9, overlapping Phase 1. Gates: pre-registration and grant applications.**

- **Calibrate power** (framework §6) once LC-01 and LC-26 supply ICCs. Until then no
  MDE is quotable, and quoting one would be decoration.
- **Draft the pre-registration template.** Feeds M-08.
- **Spec three to five experiments** against the template, once OQ-15 is decided.
- **Resolve OQ-15** - the portfolio sequence. This is a decision, not research, and
  it should not wait for the literature.

## Phase 3 - advisor outreach

**From week 6, continuous. Gated on LC-04 only, not on Phase 2.**

A first email does not need a finished power calculation. It needs a question the
recipient recognises as theirs, evidence that the sender knows their field, and a
specific reason for writing to *them*.

1. Pick the lead strand per target (`docs/phd/research-questions.md`), and resolve
   **OQ-14** by marking one RQ row `Lead` once a conversation is live.
2. Work the Priority tier from `docs/phd/phd-scoring-rubric.md` - 13 programmes.
   Verify the supervisor is active and taking students before writing; the rubric
   already caps unverified supervisor fits at 3 for exactly this reason.
3. Customise from the pack, log through the `partner-outreach` skill. Contact status
   goes to `private/phd-applications.csv`, never to `data/`.
4. Record which pack version each recipient received, so a reply six weeks later can
   be matched to what they actually read.

**Sequencing note:** do not send all thirteen at once. Send three, learn from the
replies, revise the pack, send the next three. The first three should be programmes
you would be happy with but are not your top choice.

## Phase 4 - partner and verification access

**From day one, continuous. Gates: everything downstream.**

This is the longest-lead item and the one most likely to determine the timeline, and
it has not started. OQ-7 (verification partner) is gating; M-03, M-04 and M-09 have
all been `Not started` for weeks.

- Approach verification candidates **in parallel**, not in sequence (the decision
  already recorded on OQ-7).
- Approach originator candidates in parallel with those.
- **Data-sharing conversations count as partner outreach**, and they are cheaper:
  EXP-25 and EXP-26 need historical MIS data, not a field programme. That is a much
  smaller ask for a first contact and it opens the relationship.

The last point is the most useful thing in this phase. Asking an MFI network for
five years of anonymised portfolio data is a request they can say yes to in a week.
Asking them to host a multi-year randomised pilot is a request that takes a year to
answer. Lead with the former.

## Phase 5 - grant applications

**From month 5. Gated on Phase 4.**

- **M-19** first: `data/funders.csv` has ten rows all marked `Not researched`, and
  no URLs. Deadlines and eligibility cannot be planned around until that is fixed.
- Anchor evaluation grant (M-21), gated on the verification partner.
- Note the eligibility traps already documented in
  `docs/phd/phd-funding-landscape.md` - several instruments that look open are not
  open to an Israeli applicant, and the same care is needed on the research-grant side.

---

## The critical path, in one line

**LC-04 → memos 5 to 7 → first three approaches → verification partner → anchor grant.**

Everything else is either parallel or downstream. The two things that can be done
this week and unblock the most are: read LC-04, and send a data-sharing request to
one MFI network.

## Gates, as milestones

| Milestone | Gate |
|---|---|
| M-26 | P1 literature components read; memos 5, 6, 7 drafted |
| M-27 | OQ-15 resolved - the experiment portfolio and its sequence |
| M-28 | Framework power parameters calibrated; pre-registration template drafted |
| M-29 | Application pack complete and used for a first wave of three approaches |
| M-30 | Three to five experiments specced against the template |

Existing milestones are not duplicated here: M-06 (supervisor outreach), M-11 (first
applications), M-20 (verification partners), M-21 (anchor grant), M-19 (funder
research) and M-08 (pilot design) all remain the operative rows for their work.

## How we work through this together

- One phase at a time, but Phase 4 runs continuously underneath the others.
- Literature goes in through the `add-literature` skill, one component per session -
  a component is a session-sized unit, which is why it is the unit of work.
- Outreach goes through the `partner-outreach` skill so nothing gets contacted twice.
- Every session that changes `data/`, `literature/` or the dashboard ends with a
  rebuild and `publish-check`.
- When a memo's conclusions change, the memo, its `synthesis-memos.csv` row and any
  open question citing it all move together. These three drift apart otherwise.
