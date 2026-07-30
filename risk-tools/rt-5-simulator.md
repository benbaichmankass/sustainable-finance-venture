# RT-5 simulator — what it is, what it is not

**Status:** Scaffold built, running · **Model version:** 0.1 · **Calibration: none**
**Code:** `risk-tools/tools/simulate_portfolio.py` · **Config:** `risk-tools/tools/portfolio-config.csv` · **Scenarios:** `data/macro-scenarios.csv`

## What it is

A synthetic portfolio generator and a sequential waterfall, wired to the deterministic macro scenarios. It answers structural questions:

- How sensitive is the junior tranche to default correlation?
- At what pool size do fixed costs stop dominating? (**OQ-2**)
- Does a 15% first-loss layer survive a correlated food-price shock? (**OQ-6**)
- Which of those two questions is actually binding at a given scale?

```bash
python3 risk-tools/tools/simulate_portfolio.py              # all scenarios
python3 risk-tools/tools/simulate_portfolio.py --scenario SC-2
python3 risk-tools/tools/simulate_portfolio.py --sweep      # pool size vs fixed costs
python3 risk-tools/tools/simulate_portfolio.py --write-loans
```

Headline results are written to `data/rt5-scenario-results.csv` and surface on the dashboard. The loan-level tape is gitignored — it is regenerable from the seed, and committing 36,000 synthetic rows would bury the real data in the repo.

## What it is not

**It is not calibrated.** No field data exists. The default rate, recovery rate and correlation are placeholders chosen to be plausible. Any number this produces is a statement about the *model*, not about this asset class.

**It is not a forecast.** The scenarios are deterministic rule sets, not probability-weighted views. SC-5 is not a prediction that rates, food prices and FX will move together — it is a coherence test.

**It is not a rating model.** No agency methodology is implemented. Whether to target one is still open (Memo 3).

**Its outputs are not evidence.** They belong in a design conversation, not in a document that makes claims to an investor. Every output row carries `Basis: SYNTHETIC` for exactly this reason.

## What the scaffold has already shown

Two things worth recording, both of which are properties of the structure rather than of the placeholder parameters:

**1. The fixed-cost floor is real and steep.** From `--sweep`:

| Groups | Pool | Fixed cost as % of pool | Base junior loss | Stressed junior loss |
|---|---|---|---|---|
| 250 | $1.2m | 20.9% | 100% | 100% |
| 500 | $2.3m | 10.8% | 82% | 95% |
| 1,000 | $4.6m | 5.5% | 47% | 66% |
| 2,000 | $9.3m | 2.7% | 27% | 48% |
| 4,000 | $18.7m | 1.3% | 20% | 36% |
| 8,000 | $37.3m | 0.7% | 15% | 35% |
| 16,000 | $74.7m | 0.3% | 13% | 31% |

Below roughly $5m the junior tranche is destroyed by **costs, not credit**. The curve flattens around $20–40m, where credit loss takes over as the binding constraint. That is a derived answer to OQ-2 rather than a borrowed one — the existing working band came from central tendencies across deals that do not resemble this asset (LIT-011, LIT-012).

It also reframes the question. A pilot pool of 20–50 groups is not "too small to securitise" by a little; it is smaller than the fixed-cost floor by two orders of magnitude. The warehousing bridge is not an optimisation, it is the only path.

**2. Correlation matters more than the default rate.** SC-2 raises the default multiplier 2.2× *and* pushes correlation from 0.20 to 0.45. The mean loss rate roughly doubles, but the p95 loss nearly triples. A model assuming independence would look reassuring and size the junior layer far too thin — the failure mode Memo 3 warns about.

**Caveat on both:** these are relationships between the model's own parameters. They are believable as *shapes* and worthless as *levels*.

## Design choices worth knowing

**Single-factor Gaussian copula** for correlated default: each geography draws a systemic factor, each loan combines it with an idiosyncratic draw. Standard in structured credit, chosen here because it is inspectable — a reader can see exactly what the correlation parameter does. Anything more sophisticated would be harder to check and no better founded, given nothing is calibrated.

**Sequential waterfall** with an explicit conservation assertion: what goes in must equal what comes out, to the cent, on every path. A leak there would invalidate every number downstream, and it is the classic waterfall bug.

**Cost drag reported separately from credit loss.** Learned the hard way: the first run showed a 1.4% pool loss wiping out 48% of the junior tranche, which reads as a credit result and is not one. Splitting the two is what made the fixed-cost finding visible at all.

**Stdlib only.** Includes a hand-rolled inverse normal CDF rather than taking a numpy/scipy dependency, consistent with the rest of the toolchain. A researcher with Python and no install step must be able to run this in five years.

## Graduating from synthetic to calibrated

In order of how much each would improve the model:

1. **Observed default and recovery rates** from a real pilot cohort, by cycle. Replaces the two most load-bearing placeholders. Requires RT-1 to be in the field.
2. **An empirical correlation estimate** — needs several groups across several geographies observed through at least one common shock. This is the hardest input to get and the one that matters most, and it plausibly requires SAVIX historical data rather than our own pilot.
3. **Real cost quotes** — legal, rating, listing, servicing, from actual providers in the target jurisdiction (PT-09). The fixed-cost term drives the OQ-2 answer, and $250,000 is currently a guess.
4. **A structuring review** of the waterfall convention against what an investor would actually accept (PT-08).

Until (1) and (3), treat every level this produces as illustrative. The *shapes* — cost floor steepness, correlation sensitivity — are more robust than the levels and are what the tool is currently good for.

## Open questions

- What loss and correlation assumptions are defensible with no track record? The honest output is a range, not a number.
- Should the model target a rating-agency methodology, and if so which?
- What servicing cost is realistic for community-originated assets? Likely higher per dollar than any comparable deal, which pushes the minimum viable scale up.
- **OQ-8**: run a blended PL-1 / PL-2 pool through the same engine. Not yet implemented — PL-2 needs a PPA cash-flow generator, and the prior question of whether a utility PPA permits assignment at all is unresolved.
