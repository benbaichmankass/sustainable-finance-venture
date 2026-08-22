# Research Agenda: the literature review plan

**Status:** v2 (2026-08-22) · **Owner:** BB · **Tracker:** `data/lit-components.csv` (LC-01 … LC-26)
**Supersedes:** v1 (four-axis plan, 2026-07). The axes are kept as a classification; they are no longer the unit of work.

## Objective

Build a literature base that supports three different consumers: a PhD proposal a
supervisor will take seriously, product and pilot design decisions, and an
investor-grade thesis. Those are not the same reading list, but they overlap enough
to be built once.

## What changed from v1, and why

v1 organised the review into four broad axes - community finance, microfinance
impact, securitisation, blended finance. That was the right shape for a first pass
and it worked: 23 anchors and three reviewed memos came out of it.

It has stopped being useful for one specific reason: **an axis does not tell you
what to read next.** "Securitisation" spans rating criteria, true-sale law, African
market depth and portfolio correlation - four bodies of work with different
questions, different sources and very different urgency. Meanwhile three gaps
flagged in `docs/phd/research-proposal.md` §1 sat unaddressed for weeks precisely
because no axis owned them.

v2 replaces the axis with the **component** as the unit of work. A component is
scoped so that reading it produces a working command of one identifiable body of
knowledge, and so that its completion is a checkable event rather than a feeling.

Each component carries: why it matters to *this* project, which research-question
strands it serves, the specific questions it must answer, search terms, its current
anchors, a target, and the memo it feeds.

## The components

Full detail in `data/lit-components.csv`. Summary:

### P1 - needed before the proposal goes out (10 components, 96 anchors cumulative)

| ID | Component | Have | Target |
|---|---|---|---|
| LC-01 | Savings groups and community finance institutions | 4 | 10 |
| LC-02 | Group-lending mechanisms: information, sanction, repeat interaction | 4 | 12 |
| LC-03 | Index and parametric insurance: demand, basis risk, impact | 4 | 12 |
| LC-04 | Bundled credit and insurance: theory and evidence | 4 | 10 |
| LC-05 | Resilience and consumption-smoothing outcome measurement | 0 | 8 |
| LC-06 | Climate and adaptation finance: gap sizing and instruments | 0 | 8 |
| LC-07 | Credit-risk modelling in thin-data settings | 0 | 10 |
| LC-08 | Portfolio correlation and covariate risk in microfinance | 2 | 8 |
| LC-09 | Securitisation eligibility, data tapes and rating criteria | 3 | 10 |
| LC-24 | Coffee-sector economics and cooperative finance | 0 | 8 |

**LC-04 was the most important empty cell in this repo, and reading it first paid
off immediately.** The master proposal asserted that the literature raises but rarely
tests loan-insurance bundling. **That assertion is false.** Bundling has been tested
experimentally at least twice and compulsory bundling suppressed demand both times -
LIT-024 (Malawi, take-up 13 points lower off a 33.0% base) and LIT-025 (India, a
16-point rise in microfinance drop-out, measured on the lender's own book). LIT-026 is
the counterweight: risk rather than capital binds, and demand for *separately* offered
index insurance is strong. The distinction that reconciles them - offered separately
versus compulsorily priced into the loan - is the finding, and the proposal's novelty
claim has to move. Logged as **OQ-17**; synthesis in **MEMO-5**. Four anchors of ten,
all still `To read` because only abstracts were verified.

**LC-24 joined this tier on 2026-08-22, and the reason is worth stating.** It is here
because coffee has *not* been chosen, not because it has. The coffee cluster (EXP-09,
EXP-10, EXP-11) outscores every other field candidate, and those scores rest on two
assumptions nobody has tested: that producer cooperative federations and value-chain
lenders are reachable as partners, and that existing certification and traceability
records could carry underwriting rather than only provenance. Reading is the cheap way
to test both before a field programme commits to them. If the assumptions hold, the
cluster leads the field-anchor choice (OQ-16); if not, the scores were wrong.

**That framing is now out of date, and the change is worth recording honestly.** On
2026-08-22 OQ-16 was decided in coffee's favour *before* LC-24 was read. The component
is unchanged in content but has changed in function: it no longer tests an assumption
ahead of a decision, it audits one behind it. If the two assumptions above do not hold,
the finding forces the anchor decision to be reversed. That is a worse position than the
one this tier was designed to avoid, and it is why LC-24 now sits first in the P1 queue.

### P2 - needed for the thesis, not for the first email (11 components, 80 anchors)

LC-10 securitisation law and true sale · LC-11 African and EM capital-market depth ·
LC-12 blended finance and first-loss · LC-13 microcredit impact and the
meta-analytic record · LC-14 digital financial rails and data capture ·
LC-15 PAYGO and energy-access receivables · LC-16 agricultural value chains,
warehouse receipts and price risk · LC-17 over-indebtedness and consumer protection ·
LC-18 financialisation of community institutions · LC-19 regulation of savings
groups and microinsurance · LC-20 microfinance cost-to-serve and unit economics.

**LC-18 is the one to not skip.** It holds the critique that external capital
corrodes the institutions it enters. A proposal that does not engage it reads as
naive, and RQ-04 is built on taking it seriously rather than dismissing it.

### P3 - context (5 components, 30 anchors)

LC-21 microsavings and household financial behaviour · LC-22 remittances and migrant
financial arrangements · LC-23 gender and group composition · LC-25 data governance and
consent · LC-26 impact-evaluation method advances.

LC-26 is worth pulling forward despite the tier: it holds the power, clustering and
multiple-hypothesis material, and the research framework's section 6 cannot be
calibrated without it.

## Pace, and an honest word about the numbers

206 cumulative target anchors. Of those, 55 slots are already filled, by 44 distinct
sources - several sources serve more than one component, which is why the two numbers
differ. That is a full PhD-scale literature base and it is not a six-week job.

The near-term job is **P1: 96 targets, 37 filled, so 59 new rows.** At the 12 to 15
sources a week this repo's workflow has actually sustained, that is six to seven weeks
of reading. The two-pass structure from v1 still applies and is what makes the number
tractable:

- **Pass 1, breadth.** Abstract, introduction, conclusion, methods and limitations.
  Enough to write an honest matrix row and know whether the source matters. Most
  rows never get more than this, and that is fine - the row says so.
- **Pass 2, depth.** 15 to 20 anchors total across all components get a full read
  with detailed notes on design and assumptions. These are the sources the proposal
  argues *with* rather than merely cites.

Do not let the target numbers turn into a quota. A component with six honest rows
and a clearly stated gap is worth more than ten rows padded to hit a number, and
CLAUDE.md §6 is not negotiable: **nothing is logged that has not been read.**

## Workflow

**Adding a source** - use the `add-literature` skill. It enforces the field
standard, the ID scheme and the no-fabrication rule. Every row gets `Axis` (the v1
classification, retained) and should be cross-referenced from its component's row.

**Working a component** - read its `Questions_To_Answer` first; those are what the
component is *for*. Use `Search_Terms` as the starting query set, then forward and
backward citation search from whatever anchor turns out to be central. When the
component's questions can be answered without hedging, mark it `Reviewed`.

**Component status vocabulary:** `Not started` · `Partially covered` · `In progress`
· `Reviewed`.

## Synthesis memos

Memos 1 to 3 exist and are Reviewed. v2 maps every component to a memo, extending
the set to nine:

| Memo | Covers | State |
|---|---|---|
| MEMO-1 | LC-01 - what savings groups achieve and where they fail | Reviewed, extend with LC-01 |
| MEMO-2 | LC-13 - microfinance impact evidence | Reviewed, extend with LC-13 |
| MEMO-3 | LC-12 partial - securitisation and blended finance as applied | Reviewed |
| MEMO-4 | LC-02, LC-13, LC-17, LC-18, LC-21, LC-23 - the mechanism and its critics | To draft |
| MEMO-5 | LC-03, LC-04, LC-05 - insurance, bundling and what resilience means | **Drafted (partial)** - LC-04 read, LC-03 and LC-05 outstanding |
| MEMO-6 | LC-06, LC-26 - the climate financing gap and how to measure a response | To draft (P1) |
| MEMO-7 | LC-07, LC-08, LC-09 - can these cash flows be modelled | To draft (P1) |
| MEMO-8 | LC-10, LC-11, LC-19 - the legal and market preconditions | To draft |
| MEMO-9 | LC-14, LC-15, LC-16, LC-20, LC-22, LC-24, LC-25 - sector and infrastructure notes | To draft - its LC-24 section is P1 and lands earlier than the rest |

Every memo carries an explicit "implications for this project" section. When a
memo's conclusions change, update the memo, its `synthesis-memos.csv` row and any
open question that cited it - CLAUDE.md §7 flags these three as the ones that drift.

## Source access

- **Open access first**, and by preference: World Bank, OECD, IFC, CGAP, J-PAL,
  FinDev Gateway, IPA, 3ie, UNEP, IAIS. They are citable by anyone reading this repo
  later, which matters for a public repo.
- **Working-paper versions** (NBER, IZA, SSRN, RePEc, institutional repositories)
  are usually available where the journal version is not, and are acceptable as
  anchors provided the row records which version was read.
- **Paywalled** sources need institutional access. This is one of the concrete,
  unglamorous arguments for the PhD affiliation, and worth noting: LC-07 and LC-08
  in particular sit largely behind finance-journal paywalls.
- Track citations forward and backward from anchors rather than relying on search
  alone; the highest-value sources for LC-04 in particular are unlikely to surface
  from a keyword query.

## Status

- [x] v1 four-axis Tier-1 scan complete (23 anchors)
- [x] Memos 1 to 3 drafted and reviewed
- [x] Component breakdown defined (LC-01 … LC-26)
- [ ] P1 components read (0 of 10 complete; LC-04 and LC-03 partially covered)
- [ ] Memos 5, 6, 7 drafted - the P1 outputs
- [ ] Deep-read anchor set selected (target 15 to 20)
- [ ] P2 components read
- [ ] Memos 4, 8, 9 drafted
