# Research questions: one project, seven ways to ask about it

**Status:** v1 (2026-08-22) · **Owner:** BB · **Tracker:** `data/research-questions.csv` (RQ-01 … RQ-29)

## Why this document exists

Three documents in this repo state the project's research question, and they do not
quite agree. `docs/research/working-doc.md` asks how community arrangements can be
*structured into securitizable assets*. `docs/phd/phd-proposal-master.md` asks how
they should be *structured and modelled at origination*. `docs/phd/research-proposal.md`
narrows both to climate and poverty in Africa and MENA.

None of those is wrong. The problem is that a supervisor in an actuarial-science
department and a supervisor in a development-economics RCT lab will not respond to
the same sentence, and sending both the same paragraph guarantees that at least one
of them reads it as somebody else's project.

So the question is held as **an architecture, not a sentence**: one core question,
seven strands, and a rule for which strand leads a given approach.

## The constraint that makes this honest

Adaptable research questions are usually a warning sign. They suggest a candidate
who will say whatever gets them admitted.

The thing that makes this architecture defensible instead is a hard constraint:

> **Every strand must be answerable from the same fieldwork.**

One pilot - a community-originated credit product with cover bundled in, captured
under a securitisation-ready schema, randomised at group level - generates the
household outcomes RQ-02 needs, the loan-level performance data RQ-03 needs, the
mechanism variation RQ-04 needs, the cost data RQ-06 needs, and the trigger series
RQ-07 needs. The strands are different *questions about one body of evidence*, not
different projects.

Where a strand needs something the core pilot does not produce, that is stated in
its row rather than glossed. RQ-05 needs investor-side data the pilot cannot
generate; RQ-08 needs a second site.

## The core question

> **RQ-01.** Can the credit and insurance cash flows originated by community
> financial structures be made investor-legible - standardised, verifiable,
> poolable - without degrading the social mechanisms that make them perform, and
> what does that trade-off cost in risk terms and in welfare terms?

Two things about this phrasing are deliberate.

**It contains a tension, not a task.** "How do we securitise VSLA loans" is an
engineering problem and reads like consultancy. The version above carries the
possibility that the answer is *no* - and that possibility is grounded in this
repo's own evidence, not manufactured for effect. Memo 2 establishes that the
joint-liability contract is not the active ingredient in repayment (LIT-020); what
seems to matter is repeated interaction and the informal risk-sharing it builds
(LIT-021). Ghatak and Guinnane (LIT-022) show the information and sanction channels
can trade against each other. Tankha (LIT-023) records that the longest-running
successful joint-liability institution in the record funded itself from local
deposits and did not take external wholesale money into the group layer.

Securitisation is precisely the act of replacing community money with outside
money. Whether the mechanism survives that substitution is an open empirical
question - logged here as OQ-12 and OQ-13 - and it is the intellectual core of the
thesis rather than a caveat at the end of it.

**It is institution-neutral.** It names no country, no crop, no product and no
discipline. Every strand below is a narrowing of it, and the geography, population
and instrument are all adaptable to the programme (decision of 2026-08-22).

## The seven strands

| ID | Strand | The question, short | Method backbone |
|---|---|---|---|
| RQ-02 | Impact evaluation | Does bundling cover into group credit improve resilience and repayment stability? | Cluster RCT, pre-registered |
| RQ-03 | Credit risk | Can these cash flows be modelled and enhanced to investment grade? | Hazard models, LGD, Monte Carlo waterfall |
| RQ-04 | Mechanism | What drives repayment, and does it survive external capital? | Lab-in-field plus randomised funding source |
| RQ-05 | Capital mobilisation | When does first-loss capital mobilise rather than substitute, and who captures the gain? | Deal-level panel, investor elicitation |
| RQ-06 | Data architecture | What must be captured at origination, and what does it cost? | Design science, randomised protocol comparison |
| RQ-07 | Adaptation finance | Can pooling household climate risk make adaptation finance work at household scale? | Spatial correlation, capital simulation |
| RQ-08 | Transferability | What travels across institutional forms and sites, and what must be re-estimated? | Multi-site replication, hierarchical pooling |

Each strand carries roughly three sub-questions in the tracker (RQ-09 … RQ-29).
Those are the chapter-level questions - the thing a supervisor will actually ask you
to be specific about in a second meeting.

## Which strand leads which approach

Scored programmes come from `data/phd-programs.csv` and the rubric in
`docs/phd/phd-scoring-rubric.md`. The `Fits_Programs` column in the tracker holds
the full mapping; this is the summary.

| If the advisor is… | Lead with | Keep in reserve | Example programmes |
|---|---|---|---|
| A field-experiment / RCT economist | **RQ-02** | RQ-04, RQ-08 | UEA (PHD-15), Groningen (PHD-22), IHEID (PHD-21), Wageningen (PHD-27), Passau (PHD-44), NHH (PHD-48), Namur (PHD-52), Bocconi (PHD-51) |
| A structured-finance or actuarial researcher | **RQ-03** | RQ-07, RQ-06 | HUJI Business School (PHD-10), Bayes (PHD-18), Reading ICMA (PHD-17), Geneva GFRI (PHD-07), SMU (PHD-31) |
| A microfinance mechanism / contract theorist | **RQ-04** | RQ-02 | CERMi (PHD-20), Namur (PHD-52), KU Leuven (PHD-24), TSE/PSE (PHD-41) |
| A development-finance or policy scholar | **RQ-05** | RQ-08 | SOAS (PHD-13), Manchester GDI (PHD-14), Antwerp IOB (PHD-23), UNU-MERIT (PHD-26) |
| A data / decision-science or fintech researcher | **RQ-06** | RQ-03 | Technion FDDS (PHD-12), Krea/LEAD (PHD-30), Manchester (PHD-14) |
| A sustainable- or climate-finance centre | **RQ-07** | RQ-05 | Oxford Smith School (PHD-04), LSE (PHD-05), SOAS (PHD-13), NTU CSFI (PHD-33) |
| A development-studies / replication researcher | **RQ-08** | RQ-02 | Manchester GDI (PHD-14), UNU-MERIT (PHD-26), Bath CDS (PHD-16) |

**The rule for a specific approach:** lead with one strand, name one reserve, and
state RQ-01 once so the coherence is visible. Do not present the menu. An advisor
who sees seven questions sees a candidate who has not chosen; an advisor who sees
one question and a coherent programme behind it sees a candidate who has.

The exception is a second or third conversation, where showing the architecture is
an asset - it demonstrates the project has more than one chapter in it and that the
candidate has thought about where a co-supervisor would fit.

## Where the co-supervisor goes

The rubric already records that no single department combines all four pillars this
project needs. The strand structure is what makes that tractable: the lead strand
picks the primary supervisor, and the reserve strand names the co-supervisor's
territory. An RQ-02 primary at a development-economics department pairs naturally
with an RQ-03 co-supervisor in finance or actuarial science, and the pairing is
easier to propose when both halves are already written down as questions.

## What is not yet decided

**Which strand leads the primary proposal** is logged as **OQ-14** and is
deliberately open. It should be settled by which advisor engages first, not chosen
in advance - that is the whole point of building the architecture this way.

## Maintenance

- New sub-questions get the next free RQ number. IDs are never reused (CLAUDE.md §3).
- When a strand is dropped, mark its `Status` `Parked` with a reason; do not delete
  the row - the `Component_Refs` and `Experiment_Refs` on it are cross-referenced.
- `Status` vocabulary: `Active` · `Lead` · `Parked`. Exactly one row may be `Lead`.
- When a literature component (`data/lit-components.csv`) or experiment
  (`data/experiments.csv`) is added, check whether it belongs in a strand's refs.
