# Experiment specs: the scoring rubric and the write-up template

**Status:** v1 (2026-08-22) · **Owner:** BB
**Tracker:** `data/experiments.csv` (EXP-01 … EXP-30) · **Scorer:** `scripts/score_experiments.py`

Two things live here: how a candidate experiment gets scored, and what a shortlisted
one has to say for itself when it is written up properly.

---

## Part 1 - the scoring rubric

### Why score at all

Thirty candidates and room for three or four. Scoring does not make the choice, but
it makes the choice *arguable*: a reader can see which criterion drove a ranking and
disagree with the weight rather than with a hunch.

**These scores are our judgement, not findings.** Nothing in the score columns comes
from a source. They are recorded so they can be challenged, and re-running
`scripts/score_experiments.py` after changing one is a five-second operation.

### The five criteria

Each scored 1 to 5. The anchors matter more than the number.

**Research_Significance** - what the field learns if this works.

| | |
|---|---|
| 5 | Answers a question nobody has answered, and a null result is publishable too |
| 4 | Meaningful new evidence on a live debate |
| 3 | Solid contribution to an established literature |
| 2 | Replication in a new context of something already well established |
| 1 | Confirms what is already known |

**PhD_Feasibility** - can one candidate finish it inside three to four years.

| | |
|---|---|
| 5 | Desk-executable; no field site, no partner data dependency, no IRB beyond standard review |
| 4 | Needs a data-sharing agreement or short fieldwork, but no multi-year pilot |
| 3 | Fieldwork inside an existing programme; a single season or cycle |
| 2 | Multi-year field pilot requiring partner, grant, ethics approval and a full survey operation |
| 1 | Requires capital deployment or an institution that does not yet exist |

**Partner_Availability** - how likely a willing counterpart exists and can be reached.

| | |
|---|---|
| 5 | No partner required |
| 4 | Multiple identified candidate organisations with aligned incentives |
| 3 | Plausible candidates, but the ask is unusual and not obviously in their interest |
| 2 | Needs a partner to do something against their operating convention |
| 1 | No identified route |

**Implementation_Ease** - operational complexity once running.

| | |
|---|---|
| 5 | Runs from a laptop |
| 4 | Light field operation or a defined data pipeline |
| 3 | Standard survey operation |
| 2 | Multi-arm field operation with product delivery and shock-triggered rounds |
| 1 | Capital-intensive or infrastructure-dependent |

**Grant_Exposure** - fit with funders in `data/funders.csv`.

| | |
|---|---|
| 5 | Squarely inside a named funder's stated call |
| 4 | Clear fit with several funders |
| 3 | Fundable with framing work |
| 2 | Few obvious funders, though the study is cheap enough not to need one |
| 1 | No grant route |

### The weights

| Criterion | Weight |
|---|---|
| Research significance | 35% |
| PhD feasibility | 30% |
| Partner availability | 15% |
| Implementation ease | 10% |
| Grant exposure | 10% |

Significance leads because OQ-9 resolved this programme as research-first.
Feasibility sits close behind because the binding constraint is one person and four
years, and the earlier version of this tracker ignored that entirely.

Bands: `Flagship candidate` at 4.00 and above · `Strong` 3.40 to 3.99 ·
`Reserve` 2.80 to 3.39 · `Park` below 2.80.

### Two things the rubric does not do

**It does not decide.** `Priority_Band` is the rubric's view. `Status` is the
decision, and they are allowed to disagree. They did: the pass put the OQ-11 flagship
trio in the `Reserve` band while it still read `Selected`, and that disagreement is
what forced OQ-15.

**It systematically favours desk studies**, because feasibility at 30% rewards not
needing a field site. That is a real constraint, not a bug - but a portfolio built
only from the top of the ranking would be a thesis with no field component, and
several of the high scorers re-analyse data that only exists because somebody else
ran the field pilot.

**That tension is now resolved, and the resolution is a sequence** (OQ-15, 2026-08-22).
The two desk-executable falsification tests run first, because either can kill the
thesis before field money is committed; one field anchor follows. So the ranking is
read as an ordering *within* type, and the portfolio takes from both ends of it.

---

## Part 2 - the write-up template

A tracker row says enough to compare candidates. It does not say enough to design
one, defend it to a supervisor, or drop it into a proposal. Any experiment that
reaches shortlist gets expanded against this shape, as
`docs/research/experiments/exp-NN-short-name.md`.

Fill it honestly. An empty section is information; a plausible-sounding guess is not.

```markdown
# EXP-NN — <short name>

**Status:** <Idea | Specified | Shortlisted | Pre-registered | Running | Complete>
**Serves:** RQ-NN (lead), RQ-NN (secondary) · **Composite:** N.NN (<band>)

## 1. The question
The one sentence this experiment answers. If it takes two, the design is not settled.

## 2. Hypotheses
H1, H2 … stated so each can be rejected. Include the direction, and say which is primary.

## 3. Why it matters
What changes if the answer is yes. What changes if it is no. If nothing changes on a
null result, say so — that is a reason to reconsider the experiment.

## 4. Design
Identification strategy, unit of randomisation, arms, and the assignment mechanism.
Name the fallback design and the condition that would force it
(`docs/research/research-framework.md` §4).

## 5. Population and setting
Who, where, how many, and how they are reached. Sites are adaptable — say what the
design needs from a site rather than naming one prematurely.

## 6. Intervention
What is actually delivered, by whom, on what schedule. Include what the control arm
gets, which is a design decision and not an absence.

## 7. Outcomes
Primary outcome — one. Secondary outcomes by family, with the correction method.
Instrument and timing for each. Shock measurement, where the outcome is conditional
on a shock.

## 8. Data
Sources, ownership, sharing agreement status, and what happens to row-level records
(Vault `05-raw-data`, never the repo — CLAUDE.md §8).

## 9. Power
ICC assumption and its source, cluster count, expected shock incidence, and the MDE
that follows. If the parameters are not yet known, say which literature component or
partner dataset supplies them rather than assuming a number.

## 10. Partners
Origination, verification, and any regulatory counterpart. Status of each. Named
individuals go in `private/partner-contacts.csv`, never here.

## 11. Timeline
Design, approval, enrolment, data collection, analysis. Mark the gating milestones —
ethics approval and data-sharing agreements are the two that slip.

## 12. Risks
What could make this fail, and the mitigation or fallback for each. Include the
ethical risks (`docs/research/research-framework.md` §10), not only the operational ones.

## 13. Cost and funding
Rough budget by line. Target funders from `data/funders.csv` with the specific call.

## 14. What it would take to abandon this
The result or blocker that means stopping. Deciding this in advance is what stops a
sunk-cost pilot from consuming a whole PhD.
```

### Which ones get specced

Three to five, no more. A proposal that specs everything reads as a candidate who
cannot prioritise. The rest stay as tracker rows, which is what the tracker is for.

Priority order for specs, settled by OQ-15:

1. **EXP-25** - default correlation on partner MIS. Tests whether the risk is
   covariate rather than idiosyncratic, which is the falsification test the whole
   pooling thesis turns on. `Selected`.
2. **EXP-22** - securitisation-ready origination protocol with activity-based costing.
   Tests whether investability costs more than it unlocks. `Selected`.
3. **The field anchor** - one of EXP-01, EXP-06, EXP-09 or EXP-10, once OQ-16 resolves.
   Cannot be specced until it is chosen, and it should carry the second randomisation
   layer from `docs/research/research-framework.md` §3.
4. Optionally, the investor-side study (EXP-23), which is unusual enough to be
   memorable in a proposal and costs almost nothing to run.

Specs 1 and 2 can be written now - neither is waiting on a decision, only on partner
data access (M-32).
