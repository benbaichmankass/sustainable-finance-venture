# Business Economics — Analysis Plan & Benchmark Skeleton

**Status:** Plan (week of 2026-08-02) · **Owner:** BB

This fills the "Financial plan — cost structure, revenue projections, funding ask" gap flagged in
`business-plan.md §10`. It is the **plan for the analysis**, plus a first benchmark skeleton — not
a finished model. Its job is to state, precisely, the questions the economics must answer and the
numbers we need to pin down, so that during the research phase we can tell — with benchmarks, not
vibes — whether and how this becomes a profitable business.

The two questions the analysis exists to answer:

> **Do the unit economics of a single structured deal work — and how many deals, at what size, does
> the venture need before the structuring layer is self-sustaining?**

Everything below serves those two questions.

## 1. Deal anatomy and the cost stack

A "deal" is one pool of community-originated receivables that we structure, monitor and place. Its
economics decompose into a **fixed** cost stack (largely independent of pool size — this is what
makes small pools uneconomic, per OQ-2) and a **variable** stack (scales with the pool).

| Cost | Fixed / Variable | Notes |
|---|---|---|
| Legal & SPV set-up (true-sale opinions, domicile, counsel) | Fixed | The OQ-1 / LIT-009 checklist work; the main reason a pool must reach scale |
| Structuring & rating / analytics | Fixed | Our own labour early on; a rating cost later |
| Origination-partner economics | Variable | What the VSLA/MFI layer keeps; a revenue *share*, not our cost, but it sets the spread available |
| Servicing & monitoring | Variable | RT-3 monitor runs this; largely our cost |
| Credit enhancement / first-loss funding cost | Variable | The blended layer (OQ-6); DFI/philanthropic capital prices the junior risk |
| Impact measurement | Semi-fixed | Grant-funded where possible (see `funding-pipeline.md`), so kept off the commercial P&L |

**The key structural fact:** the fixed stack is why OQ-2's "tens of millions, scaling to ≥USD 100m"
band exists. The analysis has to locate the pool size at which fixed costs stop dominating.

## 2. Revenue lines

From `business-plan.md §4`, made quantifiable:

1. **Structuring & servicing fees** — as % of notional and/or bps on assets under management.
2. **Retained economic interest** — return on the strip we are required to hold (EU/UK
   risk-retention, Memo 3). Not optional; it is both a cost of capital and a return line.
3. **Data / analytics licensing** — later-stage, once the underwriting engine has a track record.

The analysis models each as a driver, so we can see which line actually carries the business at
each stage (early: fees; later: retained interest + data).

## 3. The unit-economics model (spec — to build)

A single spreadsheet / script that takes pool-level inputs and returns deal- and venture-level
economics. Candidate to become a new risk-tool alongside RT-1…RT-5.

**Inputs (drivers):** pool notional; # loans / # groups; average ticket; tenor; gross yield;
expected loss curve; cost-to-serve; fixed structuring cost; fee %; retained-interest %; first-loss
size and cost; ramp (deals per year).

**Outputs:** net margin per deal; break-even pool size; deals-to-breakeven for the venture;
blended return to each tranche; sensitivity to loss rate and fee compression.

**Two levels:**
- **Deal level** — is one pool profitable, and above what size?
- **Venture level** — given fixed overhead and a realistic ramp, how many deals of what size until
  the structuring layer covers its own costs? This is the go/no-go number (OQ-10).

## 4. Benchmark skeleton

Starting values to *test*, not targets. Some are already evidence-backed in `business-plan.md §7`;
those are marked **[sourced]**. The rest are marked **[assumed]** and are exactly what the research
phase exists to replace with real numbers. Nothing here is stated as fact.

| Benchmark | Working value | Basis |
|---|---|---|
| First-loss / junior tranche | 10–20% of structure | **[sourced]** LIT-013, LIT-015 |
| Pilot warehouse size | Tens of millions USD, DFI-anchored | **[sourced]** LIT-011, LIT-012 |
| Public issuance threshold | ≥ USD 100m | **[sourced]** LIT-012 |
| Track record before first tranche | 2–3 years clean repayment data | **[sourced]** LIT-004, LIT-006 |
| Structuring / servicing fee | To source | **[assumed]** benchmark vs responsAbility / BlueOrchard-type managers (PT-08) |
| Fixed legal / SPV set-up cost | To source | **[assumed]** get from counsel (PT-09) alongside OQ-1 |
| Portfolio gross yield (community loans) | To source | **[assumed]** from MFI/VSLA partner data (PT-03, PT-04) |
| Expected loss / PAR | To source | **[assumed]** from partner MIS + Memo 1/2 |
| Cost-to-serve per loan | To source | **[assumed]** from origination-partner economics |
| DFI mobilization ratio (private $ per DFI $) | To source | **[assumed]** OECD/IFC blended-finance data (Memo 3) |

The **[assumed]** rows are the shopping list. Each maps to a partner or source that can replace the
guess with a number — which is precisely how the research phase produces the benchmarks the user
asked for.

## 5. What "profitable business" means here (decided)

**Locked 2026-08-02 (OQ-10).** The go/no-go **gate** is a *credible path to at-scale profitability* — do
the unit economics show a defensible route to the structuring layer covering its costs plus a target
margin, at a scale we can realistically reach, with the key assumptions named and testable? Three
deliberate choices around it:

- **Pilot-breakeven is a companion yardstick, not the gate.** We compute how far a pilot-scale deal is
  from covering itself and what would close the gap — but a pilot failing to break even is expected and
  is not a "no".
- **No single fixed-scale target.** Rather than assume one target notional, the model brackets the
  question between the pilot floor and the path to scale.
- **Gate on our own P&L; investor returns are a constraint.** "Is this a business for us" is judged on the
  structuring company's economics; the tranche returns to junior / senior investors are a binding
  constraint (if they do not clear, there is no deal to structure), not the primary gate.

What remains is calibration: the concrete benchmark numbers (the **[assumed]** rows in §4), now anchored
on the flagship assets chosen in OQ-11.

## 6. Sequence

1. Confirm the cost-stack and revenue-line taxonomy above (this doc).
2. Define the go/no-go threshold (OQ-10).
3. Build the deal-level model with **[assumed]** benchmarks; expose the sensitivities.
4. Replace **[assumed]** with **[sourced]** as partner/counsel conversations land (M-04, OQ-1).
5. Extend to the venture level and read off the deals-to-breakeven number.

## Deliverable state

Plan + benchmark skeleton; OQ-10 framing now locked (§5). Remaining work: calibrate the [assumed]
benchmark rows against the flagship assets (OQ-11), then build the model (candidate new risk-tool).
Feeds `business-plan.md §10` (financial plan) and connects to OQ-2 and OQ-6.
