# Research Proposal Framework

**Status:** Scaffold (week of 2026-08-02) · **Owner:** BB

This is the spine of the research proposal. It holds the argument and links out to the pieces that live in their own files. It is deliberately a *framework* first: each section states what the finished proposal will contain and points at the artifact where that work is done, so the structure is fixed before the drafting.

**Scope decision (2026-08-02).** The proposal is anchored, for now, on goals related to **climate change** and **global poverty reduction**, with field sites in **Africa / MENA** first. Other SDG domains and geographies are deliberately out of the initial frame — not rejected, just not this proposal.

**How this maps to the deliverables:**

| Deliverable | Lives in | State |
| :---- | :---- | :---- |
| 1\. Literature review | §1 below \+ `literature/` (matrix \+ memos), decomposed into components in `data/lit-components.csv` and planned in `docs/research/research-agenda.md` v2 | 23 anchors, 3 memos; **9 P1 components identified, ~77 anchors outstanding** (M-26) |
| 2\. Opportunity-mapping methodology | `docs/research/methodology-opportunity-mapping.md` | Skeleton; weights resolved, first scoring pass run |
| 3\. Impact-measurement methodology | `docs/research/research-framework.md` (spine) \+ `docs/research/methodology-impact-measurement.md` (outcome metrics) | **Framework written 2026-08-22**; power parameters uncalibrated (M-28) |
| 4\. Experiment ideas | `data/experiments.csv` (EXP-01…EXP-30) \+ `docs/research/experiment-spec-template.md` | **Expanded to 30 and scored 2026-08-22**; portfolio unresolved (OQ-15) |
| 5\. Grant / funding plan | `docs/venture/funding-pipeline.md` \+ `data/funders.csv` | Plan \+ tracker; funder-research pass outstanding (M-19) |
| 6\. Research questions | `docs/phd/research-questions.md` \+ `data/research-questions.csv` | **Added 2026-08-22** - one core question, 7 strands, lead strand open (OQ-14) |
| 7\. Application pack | `docs/phd/application-pack.md` \+ the Drive Vault | **Added 2026-08-22**; CV and personal sections outstanding (M-29) |

**Sequencing across all of the above:** `docs/phd/proposal-workplan.md`.

**Direction decided (2026-08-02).** Working through OQ-9/10/11 landed four choices that shape the rest:

- **Win condition — research / evidence-first, with commercial viability an explicit co-goal.** The opportunity map is weighted toward impact and clean measurement (OQ-9, resolved), and the asset/structuring side is kept as a feasibility filter precisely so the flagship assets stay structurable. Commercial viability is to be *proven during the research stage, not after it* — which is why the blended-structure design (OQ-6, M-22) and the go/no-go economics (OQ-10) run in parallel with the pilots rather than waiting.  
- **Flagship portfolio — three uncorrelated experiments** (OQ-11, resolved): **EXP-01** crop drought-index (rural smallholders), **EXP-02** clean-energy PAYGO (energy / enterprise), **EXP-06** multi-peril parametric climate cover (urban informal settlements).  
- **Field design — 2–3 parallel, lean, pre-registered RCTs sharing one verification partner.** This makes the verification partner (OQ-7, PT-05) and an anchor evaluation grant (FUND-02/03) *gating prerequisites*, reordering the near-term critical path: lock the trio → verification partner co-designs the shared measurement → anchor grant application (M-20 → M-21).  
- **Go/no-go economics — a credible path to at-scale profitability is the gate**, with pilot-breakeven as a companion yardstick and no fixed-scale anchor (OQ-10, framing locked; numbers pending).

---

## 0\. Research question

> **Superseded as the canonical statement (2026-08-22).** The question is now held as
> an architecture rather than a sentence - one institution-neutral core question and
> seven strands, each framed for a different advisor profile and all answerable from
> the same fieldwork. See `docs/phd/research-questions.md` and `data/research-questions.csv`.
> The version below remains the climate-and-poverty framing of the RQ-02 strand and is
> retained because §1 to §5 of this document are written against it.
>
> The scope note above still holds as *a* framing, but geography and population are now
> deliberately open and adaptable to the programme (decision of 2026-08-22), which is why
> the experiment menu spans Africa, MENA, Latin America and South Asia rather than Africa/MENA alone.

Carried from `docs/research/working-doc.md`, narrowed to the climate \+ poverty frame:

> How can community-based lending and insurance arrangements in climate-exposed, low-income communities in Africa and MENA be structured into standardized, verifiable, poolable assets that mobilize private capital — and under what conditions do those structures measurably improve both climate resilience / poverty outcomes and risk-adjusted returns?

The proposal defends three claims in sequence:

1. **There is a mappable set of climate-and-poverty problems** where the binding constraint is financial-product design, not the absence of a solution (→ §2, opportunity mapping).  
2. **A specific toolkit can convert some of those into investable assets** (→ the venture's risk-tools RT-1…RT-5 and the business-economics analysis).  
3. **The impact of those products on the underlying SDG outcomes is measurable** with credible causal methods (→ §3, impact measurement).

## 1\. Literature review

The evidence base already exists in this repo and does not need rebuilding — it needs *framing* for a proposal. The proposal's literature review is assembled from:

- **`literature/lit-matrix.csv`** — 23 reviewed anchors across four axes (community finance / VSLAs; microfinance impact & RCT methods; microfinance securitization & ABS; blended finance & SDG capital).  
- **The three synthesis memos** in `literature/notes/` (all Reviewed):  
  - Memo 1 — what VSLAs and savings groups actually achieve, and where they fail.  
  - Memo 2 — what microfinance RCTs and reviews say about impact and design.  
  - Memo 3 — how securitization / blended finance has been applied to microfinance, and the structural constraints that remain.

**What the proposal adds on top:** a single narrative that walks from "the financing gap is a risk-allocation problem, not a capital shortage" to "here is the specific gap this research fills." That narrative is the connective tissue between the four axes, and it is drafted in the proposal document itself (not in the matrix).

**Gaps that need new anchors before the proposal is submission-ready** (each becomes a row via the `add-literature` skill; none fabricated here):

- **Climate-risk / index-insurance evidence** — the current matrix is thin on parametric and index-based insurance outcomes (e.g. index-based livestock insurance, weather-index crop cover). This axis underpins EXP-01, EXP-05, EXP-06.  
- **SDG / climate financing-gap sizing** — authoritative gap estimates (adaptation finance gap, energy-access financing gap) to ground the opportunity map's "gap size" axis.  
- **Impact-measurement methods for climate resilience** — outcome-metric literature specific to resilience and consumption-smoothing, beyond the general microfinance-RCT canon.

These three gaps were decomposed on 2026-08-22 into named literature components with anchor targets and search terms: index insurance and basis risk is **LC-03**, financing-gap sizing is **LC-06**, and resilience measurement is **LC-05**. All three are P1. The full breakdown is `data/lit-components.csv` and the plan is `docs/research/research-agenda.md` v2.

A fourth gap surfaced in that pass and is more serious than the original three: **LC-04, bundled credit and insurance**, has zero anchors. It is the component the proposal's central novelty claim rests on, and it is the first thing to read (M-26).

These are logged as gaps, not filled with guesses — see the milestone tracker.

## 2\. Opportunity-mapping methodology (skeleton)

Full skeleton in **`docs/research/methodology-opportunity-mapping.md`**.

In one line: a two-axis prioritization that scores candidate climate-and-poverty problems by **(a) the size / potential of the unmet-financing gap** against **(b) our toolkit's capacity to turn that problem into a feasible investment**. The output is a ranked shortlist that tells the research program *where to point first*. The experiment ideas in `data/experiments.csv` are the raw candidates this methodology is designed to score.

## 3\. Impact-measurement methodology (skeleton)

**Superseded 2026-08-22 by `docs/research/research-framework.md`**, which is the full framework rather than a skeleton: estimands, the two-layer randomisation design, the identification hierarchy, the power method, verification, the risk-modelling bridge and the falsification conditions. `docs/research/methodology-impact-measurement.md` remains the outcome-metric layer it points back to.

In one line: how the research measures whether the financial products actually move the SDG outcomes they target — the causal-identification strategy (building on OQ-4 / OQ-5), the outcome metrics tied to specific climate and poverty goals, and the verification arrangement (OQ-7) that keeps the measurement independent.

## 4\. Experiment ideas

Held as a tracker: **`data/experiments.csv`** (EXP-01 … EXP-08). Each row is a community with a specified climate-or-poverty problem and a candidate financial product to address it, plus how the venture's toolkit fits. These are the inputs to §2 and the seedbed for the pilot / PhD field design. See §2 of the mapping methodology for how they get narrowed to a flagship shortlist.

## 5\. Grant / funding plan

Full plan in **`docs/venture/funding-pipeline.md`**, tracker in **`data/funders.csv`** (FUND-01…). Covers the grantmaker landscape for climate-and-poverty research experiments (impact-evaluation funders, climate funds, foundations, DFI research windows) and a sequenced ask strategy that fits the research timeline.

## Open questions this framework raises

Logged in `data/open-questions.csv`: OQ-9 (mapping-score criteria and weights), OQ-10 (the internal go/no-go economics threshold), OQ-11 (which experiments become the flagship pilots), OQ-14 (which research-question strand leads the primary proposal), OQ-15 (whether the 2026-08-22 scoring pass changes the flagship set).  
