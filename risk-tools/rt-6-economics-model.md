# RT-6 — Unit-economics model

**Status:** In development · **Version:** 0.1 · **Product lines:** PL-1, PL-2 · **Blocked by:** nothing to run against synthetic assumptions; calibration blocked on partner/counsel data **Code:** risk-tools/tools/economics\_model.py · **Config:** risk-tools/tools/economics-config.csv (drivers × 3 scenarios) · **Assets:** risk-tools/tools/economics-assets.csv

## Purpose

Answer OQ-10: *is there a credible path to at-scale profitability for the structuring layer, at a scale we can realistically reach?* RT-6 is a deterministic, closed-form model of the **structuring company's own P\&L**, run across three scenarios, with a check on whether the tranche stack clears the returns investors require.

It is the model the business-economics plan (product-design/business-economics.md) specified in §3 and now builds.

## What it is

A pair of computations, kept deliberately separate because they answer different questions and because the OQ-10 framing (locked 2026-08-02) turns on the distinction:

| Computation | Question | Role |
| :---- | :---- | :---- |
| deal\_pnl / venture\_ramp | Does the structuring company make money — per deal, and as a venture? | **The gate and the KPIs** |
| structure\_clears | Does the pool's spread pay the investor tranches after loss and fees? | **The binding constraint** |

**The gate (go/no-go), set by BB 2026-08-02:** a credible path to the structuring layer **covering its own costs at a reachable scale, within gate\_horizon\_years (3)**. This is a venture-level break-even test. It is *not* the pilot-breakeven yardstick — that asks the same of a single pilot pool, is expected to fail, and rides alongside as a companion.

**The KPIs we track (not the gate):** (1) steady-state **operating margin** (target 30%) and (2) **return on capital-at-risk** (target 15%, on the retained first-loss strip). The model reports each against its target, per scenario.

**The binding constraint:** if the pool's spread cannot pay senior and mezzanine their coupons after expected loss and the originator's share, there is no deal to structure. Our fees sit ahead of the tranches in the waterfall, so our fee income is insulated from credit loss *while the deal clears* — and vanishes entirely when it does not. The model shows both.

## What it is not

**It is not RT-5.** RT-5 simulates the credit waterfall with a correlated Monte-Carlo loss model; it owns the loss distribution and the fixed-cost floor (OQ-2). RT-6 takes a loss *assumption* — a point estimate, sweepable, and readable straight off an RT-5 scenario — and asks the economics question on top of it. RT-5 answers "does the structure survive"; RT-6 answers "does the business pay". They share the fixed-cost logic and reach the same shape of OQ-2 answer from opposite sides.

**It is not calibrated.** 5 of 23 drivers are SOURCED against open-access benchmarks; the other 18 are ASSUMED. Every output describes the *model*, not this asset class, while the assumed rows carry the load. No number here should be shown to an investor as a result.

**It is not a forecast.** The three scenarios are coherent assumption sets, not probability-weighted views.

## The three scenarios

economics-config.csv carries Worst, Likely and Best value columns. **Sourced anchors are held fixed across all three** (a benchmark does not get more optimistic because we want it to); the scenarios flex only the assumed judgment calls — expected loss, the origination share, our fees and cost-to-serve, the fixed cost, deal size, ramp and overhead.

### Sourced anchors (held fixed)

| Driver | Value | Source |
| :---- | :---- | :---- |
| Portfolio gross yield | 20% | MFI portfolio yield, Africa \~20% / global 19.2%, MIX 2017-18 (LIT-016) |
| Senior coupon | 7% | near MIV wholesale yield 7.6%, Symbiotics 2019 (LIT-017) |
| Junior/first-loss tranche | 15% | 10–20% range, LIT-013 / LIT-015 |
| Retained economic interest | 5% | EU/UK risk-retention minimum, Memo 3 |
| DFI mobilisation ratio | 1.8× private | Convergence (LIT-018); guarantees lead (LIT-019) |

The expected-loss and cost-to-serve **anchors** are also sourced (global PAR30 6.0% and OER 10.6% / Africa 14.5%, MIX 2017-18, LIT-016; MIV TER 2.4% / fee 1.2%, LIT-017), but the values the scenarios *use* are assumptions informed by them, so they sit in the flexed set.

### What the model currently says (synthetic, illustrative)

Running economics\_model.py on the committed config:

|  | Worst | Likely | Best |
| :---- | :---- | :---- | :---- |
| Deal net margin (% of notional) | −0.95% | \+1.9% | \+4.1% |
| Break-even pool size | \~$38m | \~$8.6m | \~$3.2m |
| Gate (cover costs within 3y) | **fail** | **pass** (yr 1\) | **pass** (yr 1\) |
| KPI1 operating margin (t. 30%) | −101% | 34% | 69% |
| KPI2 return on capital-at-risk (t. 15%) | −30% | 16% | 44% |
| Junior residual vs 10% hurdle | −21% (no deal) | 8.7% (short) | 18% (clears) |

**The reading.** Under the most-likely assumptions the gate passes and both KPIs are met — but the junior tranche returns 8.7% against a 10% hurdle, so **the deal exists only with concessional first-loss**. That is the blended-finance story stated as arithmetic, not asserted. The worst case is not a rounding-down of the likely case: it fails the clearing test outright (senior+mezz uncovered), which means no deal, not a thin one. The sensitivity grid shows why — our fee margin survives fee compression far better than it survives loss, because the real cliff is the pool ceasing to clear at \~6% loss, not our margin thinning.

**The companion yardstick.** On the flagship trio at pilot scale (EXP-01/02/06, economics-assets.csv), pilots sit **14–50× below break-even**. That is expected and is the same finding RT-5 reaches for the junior tranche: the warehousing bridge to scale is not an optimisation, it is the only path (OQ-2).

## Running it

python3 risk-tools/tools/economics\_model.py               \# all scenarios \+ pilot, writes results CSV

python3 risk-tools/tools/economics\_model.py \--scenario Likely

python3 risk-tools/tools/economics\_model.py \--deal        \# deal-level P\&L per scenario

python3 risk-tools/tools/economics\_model.py \--venture     \# venture ramp per scenario

python3 risk-tools/tools/economics\_model.py \--pilot       \# flagship pilot-breakeven yardstick

python3 risk-tools/tools/economics\_model.py \--sensitivity \# loss × fee grid (Likely)

Headline metrics per scenario are written to data/rt6-economics-results.csv (committed) and surface on the dashboard's Business tab. Every row carries the basis mix (SOURCED 5/23 drivers; remainder ASSUMED).

## Versioning

| Bump | Means |
| :---- | :---- |
| Major | A change to the P\&L definition or the gate/KPI methodology — prior outputs are not comparable |
| Minor | A new driver, a new scenario column, an added output metric |
| Patch | A numerical fix with no methodology change |

Every run prints its model version and the basis mix. **A margin without its assumptions is not a result** — this is the tool most likely to be quoted back in a conversation with an investor.

### History

| Date | Version | Change |
| :---- | :---- | :---- |
| 2026-08-02 | 0.1 | Initial build. Three-scenario deal \+ venture P\&L; gate \= cover-costs-within-3y; KPIs \= operating margin and return on capital-at-risk; pilot yardstick on the flagship trio; loss × fee sensitivity. Benchmarks sourced against MIX 2017-18, Symbiotics 2019, Convergence and OECD (LIT-016..019). |

## Tests

Wired into risk-tools/tools/test\_toolchain.py (CI):

- **P\&L identity** — revenue − cost \= net margin, to the cent, every scenario.  
- **Economies of scale** — a larger pool never earns a smaller net margin (fixed cost is diluted, everything else scales linearly).  
- **Scenario ordering** — Best ≥ Likely ≥ Worst on deal net margin as a share of notional.  
- **Gate consistency** — the gate flag matches the break-even year against the horizon.

## Open questions

- **The five sourced anchors are the floor, not the ceiling.** 18 drivers remain assumed. The two that swing the answer most and are hardest to source: the **origination-layer share of the spread** (needs partner MIS, PT-03/PT-04) and the **fixed structuring cost per deal** (needs counsel, PT-09 — no open-access benchmark exists for this, so it stays a we-assume). See business-economics.md §4.  
- **The junior hurdle is the whole blended-finance question.** At 10% the Likely deal is short; at a commercial 15%+ it is far short. What return the DFI/first-loss layer will actually accept (OQ-6) decides whether the deal clears.  
- **Should the loss assumption be driven off RT-5 directly?** Today it is a config value informed by PAR benchmarks. Wiring RT-6 to read an RT-5 scenario's mean/p95 loss would tie the two tools together — a candidate for v0.2.  
- **Weighted life and revolving pools.** The model treats the pool as a single-life structure; a revolving warehouse that recycles principal several times per year would change the fee base materially. Worth modelling once the warehouse design (M-22) firms up.

