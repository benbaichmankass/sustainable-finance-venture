# Business Economics — Benchmarks & Unit-Economics Model

**Status:** Model built (RT-6 v0.1) · **Owner:** BB · **Updated:** 2026-08-02

This fills the "Financial plan — cost structure, revenue projections, funding ask" gap flagged in
`business-plan.md §10`. It began as a plan for the analysis plus a benchmark skeleton; it now carries
a **working unit-economics model (RT-6)** and a first, defensible answer to OQ-10. Its job is to tell
us — with benchmarks, not vibes — whether and how this becomes a profitable business.

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

## 3. The unit-economics model (built — RT-6)

Built as **RT-6** (`risk-tools/tools/economics_model.py`, doc `risk-tools/rt-6-economics-model.md`),
a stdlib-only tool alongside RT-1…RT-5. It takes pool-level drivers and returns deal- and
venture-level economics across **three scenarios** (Worst / Likely / Best).

**Inputs (drivers):** pool notional; average ticket; weighted life; gross yield; expected loss;
origination share of the spread; our cost-to-serve; fixed structuring cost; structuring and servicing
fee %; retained-interest %; tranche sizes and coupons; junior hurdle; ramp (deals per year); overhead.
Each driver is tagged `SOURCED` or `ASSUMED` in `economics-config.csv`.

**Outputs:** net margin per deal; break-even pool size; deals- and years-to-breakeven; operating
margin and return on capital-at-risk; the junior residual return against its hurdle; and a loss ×
fee-compression sensitivity grid.

**Two levels, plus a companion:**
- **Deal level** — is one pool profitable, and above what size?
- **Venture level** — given fixed overhead and a realistic ramp, does the structuring layer cover its
  own costs, and at what margin? This is the go/no-go test (OQ-10).
- **Pilot yardstick** — how far a pilot-scale pool on each flagship asset is from covering itself.

**The design choice that matters:** RT-6 keeps *our P&L* (the gate) separate from *the investor
stack* (the binding constraint), and it is **not** RT-5. RT-5 owns the correlated loss distribution
and the fixed-cost floor; RT-6 takes a loss assumption and asks whether the business pays.

## 4. Benchmarks

Starting values to *test*, not targets. The 2026-08-02 benchmark-research pass replaced most of the
original **[assumed]** shopping list with open-access **[sourced]** anchors; what remains assumed is
flagged honestly. Nothing here is stated as fact, and every figure feeds RT-6's `economics-config.csv`.

| Benchmark | Working value | Basis |
|---|---|---|
| First-loss / junior tranche | 10–20% of structure | **[sourced]** LIT-013, LIT-015 |
| Pilot warehouse size | Tens of millions USD, DFI-anchored | **[sourced]** LIT-011, LIT-012 |
| Public issuance threshold | ≥ USD 100m | **[sourced]** LIT-012 |
| Track record before first tranche | 2–3 years clean repayment data | **[sourced]** LIT-004, LIT-006 |
| Portfolio gross yield (MFI to borrower) | ~20% Africa / 19.2% global | **[sourced]** LIT-016 (MIX 2017-18) |
| Expected loss / PAR | PAR30 6.0% global → ~5% net loss modelled | **[sourced]** LIT-016; net-loss value **[assumed]** |
| Cost-to-serve (operating expense ratio) | 10.6% global / 14.5% Africa; ~$87/borrower | **[sourced]** LIT-016 |
| Structuring / servicing fee | MIV TER 2.4%; Fixed-Income fund fee 1.2% | **[sourced]** LIT-017 (Symbiotics 2019) |
| Senior coupon | ~7% (MIV wholesale yield 7.6%) | **[sourced]** LIT-017 |
| DFI mobilization ratio (private $ per DFI $) | ~1.8× private / 4.1× commercial; guarantees lead | **[sourced]** LIT-018, LIT-019 |
| Fixed legal / SPV set-up cost | ~$250k/deal (working) | **[assumed]** — no open-access benchmark exists; get from counsel (PT-09) alongside OQ-1 |
| Origination share of the spread | ~5% of the ~20% yield | **[assumed]** — informed by OER; get from partner MIS (PT-03, PT-04) |

**Two rows resisted sourcing and remain the priority shopping list:** the **fixed structuring cost per
deal** (genuinely absent from open-access literature — a we-assume, not a the-literature-says) and the
**origination layer's share of the spread** (needs real partner MIS). These are also the two drivers
RT-6's sensitivity flags as most load-bearing. The vintage caveat matters: the MIX and Symbiotics
anchors are 2017-18 data — the last comprehensive public editions — so they predate the current rate
cycle.

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

**The concrete threshold (decided 2026-08-02, BB).** The go/no-go **gate** is a credible path to the
structuring layer **covering its own costs at a reachable scale, within 3 years**. Two figures ride
alongside as **KPIs we steer by, not gates**: steady-state **operating margin** (target 30%) and
**return on capital-at-risk** on the retained first-loss strip (target 15%). RT-6 evaluates all three,
per scenario.

### What the model says (RT-6 v0.1, synthetic)

| | Worst | Likely | Best |
|---|---|---|---|
| Deal net margin (% of notional) | −0.95% | **+1.9%** | +4.1% |
| Break-even pool size | ~$38m | **~$8.6m** | ~$3.2m |
| Gate — cover costs within 3y | fail | **pass (yr 1)** | pass (yr 1) |
| KPI1 operating margin (t. 30%) | −101% | **34%** | 69% |
| KPI2 return on capital-at-risk (t. 15%) | −30% | **16%** | 44% |
| Junior residual vs 10% hurdle | −21% (no deal) | **8.7% (short)** | 18% (clears) |

**A first, defensible answer to OQ-10: a conditional GO.** Under the most-likely assumptions the gate
passes and both KPIs are met — the structuring layer is a business at a reachable scale (roughly four
$25m warehouse-scale deals a year). But the answer rests on two conditions the model makes explicit:
(1) it holds only above ~$8.6m per deal — pilots sit 14–50× below that (the warehousing bridge is the
only path, per OQ-2); and (2) the junior tranche returns 8.7% against a 10% hurdle, so **the deal exists
only with concessional first-loss** — the blended-finance case stated as arithmetic. The worst case does
not merely thin the margin; it fails the clearing test, so there is no deal at all. This is a first
answer to calibrate, not a verdict — 18 of 23 drivers are still assumed.

What remains is calibration: replace the two stubborn **[assumed]** rows in §4 (fixed structuring cost;
origination share) with partner and counsel numbers, and tie the loss assumption to RT-5 directly.

## 6. Sequence

1. ~~Confirm the cost-stack and revenue-line taxonomy~~ (this doc). **Done.**
2. ~~Define the go/no-go threshold (OQ-10).~~ **Done** — gate + KPIs, §5.
3. ~~Build the deal- and venture-level model; expose the sensitivities.~~ **Done** — RT-6, three scenarios.
4. ~~Source the benchmarks.~~ **Mostly done** — LIT-016..019; two rows resist sourcing (§4).
5. Replace the two remaining **[assumed]** rows with partner/counsel numbers (M-04, OQ-1, PT-03/04/09).
6. Wire RT-6's loss assumption to an RT-5 scenario directly (RT-6 v0.2).

## Deliverable state

**Model built (RT-6 v0.1).** Benchmarks sourced where open-access data exists; go/no-go threshold
decided; a three-scenario model produces a first, defensible answer to OQ-10 (conditional GO, §5).
Feeds `business-plan.md §10` (financial plan) and connects to OQ-2 and OQ-6. Remaining work is
calibration: the two stubborn assumed drivers, and tying the loss assumption to RT-5.
