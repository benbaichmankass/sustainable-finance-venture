# RT-7 — Collective facility risk model

**Status:** Built, running · **Version:** 0.2 · **Calibration: none** · **Product lines:** PL-1 · **Code:** `risk-tools/collective/` (Python reference) and `dashboard/rt7-model.js` (browser port) · **Parameters:** `data/rt7-parameters.csv` · **Scenarios:** `data/rt7-scenarios.csv` · **Results:** `data/rt7-region-results.csv`, `data/rt7-sensitivity.csv` · **Interactive:** the dashboard's *Collective model* tab

## Purpose

Answer the question a lender to a producer collective has to answer before it lends: **what loss distribution am I taking on, and what drives it?**

The collective is the borrower of record. It on-lends to members (seasonal OpEx loans and asset CapEx loans) and markets a share of their crop, part of it sold forward before the season. That is the structure OQ-13 asks about — securitisation attaching one level up, so the community's own risk management stays intact — and it is the structure LIT-031 shows already operates at scale (Root Capital's enterprises "on-lend funds as smaller loans to individual producers and, in doing so, bear the risk of repayment").

The model exists for three jobs, in order:

1. **Design.** Which structural choices (how much is sold forward, how delivery is enforced, how thick a collective reserve, what loan sizes against what farm) move the loss distribution, and in which direction. These answers are robust to calibration because they are about *shape*.
2. **Partner diagnostics.** When a real collective's data arrives, the same model with its parameters replaced is the readiness diagnostic the practice sells (Lane A in `docs/venture/solo-operator-track.md`).
3. **Securitisation readiness.** Not a pilot objective (decision register, 2026-09-09). But the facility's loss distribution is exactly what RT-5's waterfall consumes, and the illustrative tranche cut is kept so a product designed today can be pooled later without redesign.

## What it is not

**It is not calibrated.** All 105 rows of `data/rt7-parameters.csv` carry `Basis: assumption`. Two parameters cite literature as a *reference point* (LIT-035 for price variability, LIT-036 and LIT-037 for the residual correlation channel), not as an estimate. Every number this model produces is a statement about the model, not about any coffee collective.

**It is not a forecast.** The stress scenarios are deterministic shifts, chosen for coherence. RS-2 does not predict a leaf-rust year; it asks what one would do.

**It is not a rating model and the tranches are not a product.** The equity/mezz/senior cut is illustrative, carried so that a product designed now can be pooled later. Securitisation is not part of the business pilot.

**Its outputs are not evidence.** They belong in a design conversation and in the dashboard, where every panel says *synthetic*. They do not belong in a document that makes a claim to a partner or an investor.

## The risk chain

One crop season, one collective, many Monte Carlo paths. Per path:

| Step | What happens | Why it is modelled this way |
|---|---|---|
| **Factors** | A regional climate factor and a global price factor are drawn (optionally correlated). | These are the two covariate shocks Memo 9 says dominate coffee: biological (leaf rust across half of Central America's area, LIT-031) and price (45 of 260 days flagged excessively variable in 2019/20, LIT-035). |
| **Yield and price** | The regional yield and the international reference price are lognormal around their bases; the price can also jump. Local spot is the reference less a basis. | Mean-preserving lognormals keep the base case honest. Basis is applied because farm-gate is not the world price (LIT-035 leaves the gap unmeasured). |
| **Production** | Each member produces area × persistent productivity × regional year × own noise. | Members differ permanently (dispersion) and annually (idiosyncratic noise). The regional year is the correlated part. |
| **Forward book** | Before the season the collective sold forward a share of its *expected* deliveries at a fixed price. | A forward is contracted on expectations, not outcomes. That is why a short crop creates a shortfall. |
| **Side-selling** | If spot runs above the forward price by more than a threshold, members divert part of their committed crop to the spot market. | The delivery-risk channel the research plan names. The elasticity is an assumption and the model's most consequential one. |
| **Collective sales** | Deliveries fill the forward book first, the rest sells at spot. Undelivered forward volume costs the cover price (spot − forward, floored at zero) plus a contractual penalty. The collective keeps a margin and pays fixed costs. | The collective's net cash flow can now be negative, which v0.1 made impossible. |
| **Member cash flow** | Revenue (collective payout on delivered crop, spot on the rest, other income) less production cost and a household floor gives cash available for debt service; divided by debt service gives DSCR. | A DSCR on gross revenue is always comfortable and never moves. Cost and a consumption floor are what make cover bite. |
| **Conditional PD** | An anchored logistic: PD equals the base PD at the anchor DSCR (1.5), falls toward a floor as cover strengthens, rises toward `pd_max` as it collapses. | The base PD is a prior for a *normal* year. The curve says how fast it climbs when the year is not normal. Monotone by construction. |
| **Defaults** | A one-factor copula on top of the conditional PD, with `residual_correlation`. | Yield and price explain some co-movement; LIT-036 and LIT-037 say the historical crises ran through a market-level, institutional channel the factors above do not capture. Keeping it as a separate parameter is what lets EXP-25 estimate it. |
| **Losses and buffer** | Member losses are EAD × LGD on defaults. The collective's positive net cash flow (times a reserve share) absorbs them first; a negative net cash flow adds to them. The facility loss is the remainder, capped at the pool. | The buffer is OQ-13's mechanism in arithmetic. The cap is because a lender cannot lose more than it lent; the excess is reported separately as the collective's deficit. |
| **Summary** | EL, UL95, UL99, tranche metrics, the first-loss thickness at which a senior tranche meets an EL target, and a histogram. | The attachment search is a design yardstick, not a rating. |

Two correlation channels are therefore explicit and separable: **environmental** (through yield and price into DSCR) and **institutional** (`residual_correlation`). That separation is the point of EXP-25's respec, and it is why the correlation is not a single sweep parameter here as it is in RT-5.

## Decisions worth knowing, and why

**Attach one level up.** The borrower is the collective. Member loans matter because they are the collective's assets and the source of its repayment; the facility's loss is what the collective cannot cover. This keeps the community's screening and enforcement in the structure (OQ-12's residual) rather than replacing it.

**Loan sizes scale with the farm.** v0.1 drew loan sizes independently of farm size, which put a USD 2,500 asset loan on a 0.3 ha plot and made the leverage distribution meaningless. v0.2 scales sizes with area and keeps lognormal noise around that line. The *normal-year PD* output compares what the leverage distribution implies against the base-PD prior, so an inconsistency between loan sizes and income assumptions shows up as a number rather than hiding.

**Forward book on expected volume, deliveries on realised volume.** That asymmetry is the whole of forward-delivery risk and the reason the collective's cash flow can go negative in a short year.

**Shortfall cost is cover plus penalty.** Per undelivered tonne the collective pays the market difference (if spot is above forward) and the contractual penalty. This is the conservative reading of a buyer contract; a liquidated-damages-only contract would cap it. The parameter note says so.

**Side-selling is linear in the premium above a threshold.** Simple and inspectable: at threshold 0.10 and elasticity 1.0, a 30 percent spot premium diverts 20 percent of committed crop. A real estimate needs a partner's delivery records across a high-price season (DS-08).

**Residual correlation on top of a structural PD, not instead of it.** A pure copula with a single ρ hides the mechanism; a pure structural model claims the factors explain everything. Keeping both lets the data decide how much is left over.

**Facility loss is capped at the pool.** In a price spike the uncovered forward book can exceed the loan notional. The lender's loss stops at what it lent; the rest is the collective's and its buyer's problem, and `mean_collective_deficit_usd` reports it rather than dropping it.

**numpy, deliberately.** The rest of the toolchain is stdlib-only so a researcher with bare Python can run it in five years. RT-7 takes numpy because the model is vectorised over members and paths and the Colab workflow the prototype was built for assumes it. The JavaScript port has no dependencies at all and is what the dashboard runs, so the five-year property holds for the interactive version.

**One model, two implementations, one test.** Python is the reference and runs the pipeline and CI. The JavaScript port makes the dashboard interactive. `test_rt7.py` hands the same member set to both and requires everything deterministic (pool, forward book, normal-year PD, the PD curve, the inverse normal) to match exactly, and the Monte Carlo statistics to match within sampling error.

## What v0.1 got wrong

The prototype uploaded on 2026-10-07 (archived verbatim at `archive/prototype-2026-10/`) had the right structure and the wrong risk chain. Recorded here because the fixes are the content of v0.2:

| Defect | Effect | Fix |
|---|---|---|
| PD computed from revenue *averaged across scenarios* | The DSCR link was severed from the simulation; price and yield had no effect on defaults | PD per path from that path's DSCR |
| One yield draw shared by all paths | Climate risk absent from the loss distribution | Per-path regional yield from the climate factor, plus member noise |
| Defaults drawn independently | Tail far too thin; the senior tranche looked safe for the wrong reason | Residual-correlation copula on top of the factor-driven PD |
| `shortfall_cost = 0`; `basis_local` and `penalty_per_ton_short` never applied | Collective cash flow always positive; pool loss identical to loan loss | Expected-vs-realised deliveries, cover cost, penalty, basis, fixed cost |
| Member yields generated but a single district yield used for everyone | Dispersion parameter did nothing | Member productivity carried through production |
| Loan sizes independent of farm size | Over-levered small farms by construction | Sizes scale with area |
| `sigma = vol / sqrt(n_years)` in the price model | Wrong per-period volatility for multi-year horizons | Single-season model; volatility is per season |
| DSCR on gross revenue | Cover always comfortable; PD never moved | Production cost and household floor deducted first |
| Hedge-ratio sensitivity table | Nearly flat, because of all the above | Tornado over 16 parameters that now actually move the output |

The consequence of the first four together: v0.1's loss numbers did not respond to climate or price at all, while looking as if they did.

## What the model shows at v0.2 defaults

Shapes, not levels. From `data/rt7-region-results.csv` and `data/rt7-sensitivity.csv` (5,000 paths, seed 42; sensitivities at 3,000 paths):

**1. The tail is delivery risk, not credit risk.** In every region the top sensitivity for expected loss is `price_vol` or `side_sell_elasticity`, and the scenario that produces the largest tail loss is the *price spike* (RS-4), not the price crash. A forward book sized at half of expected deliveries, with members free to side-sell, turns a price rise into the largest loss the facility can take, because the collective must cover the shortfall at the very price that caused it. This is the research plan's "delivery and side-selling risk" row made quantitative, and it argues for delivery enforcement (collection-account control, buyer-paid premiums on delivery) ahead of any credit enhancement.

**2. A poor season roughly triples expected loss; a leaf-rust-scale year multiplies it by six.** Colombia: 3.3 percent base, 10.6 percent at RS-1, 20.3 percent at RS-2. The buffer is exhausted early in a bad year because the collective's own margin falls with volume at the same time as member defaults rise — the two are not independent, which is the covariate point in a single collective.

**3. The collective buffer is thin by construction.** At a 3 percent margin on sales the collective absorbs a few thousand dollars of member losses in a normal year and nothing in a bad one. Whether a real collective holds reserves of this order is a Gate-2 question in the business-research plan, and `reserve_share_of_margin` is where the answer goes.

**4. Normal-year PD exposes assumption drift.** For Ethiopia the leverage distribution implies a normal-year PD of about 10 percent against base priors of 4 and 8 percent — the loan-size and income assumptions do not agree with the PD prior. That is a defect in the assumptions, surfaced rather than hidden, and it is what calibration against DS-07 would settle.

**5. The senior target is unattainable where the tail reaches the pool.** With a 25 bp senior EL target, Colombia needs a first-loss layer of about half the pool and Vietnam cannot reach it at all, because 1 percent of base-case paths lose everything through the forward book. Compare RT-5's 10–20 percent first-loss working range (LIT-013, LIT-015): the gap is the delivery channel, and it is the design problem to solve before the structuring one.

Caveat on all five: these are relationships between the model's own parameters. They are believable as shapes and worthless as levels.

## Data source mapping

Every parameter in `data/rt7-parameters.csv` carries four provenance fields, which the dashboard renders as the *Data sources* table:

- `Basis` — `assumption` · `literature` · `observed`. Currently all assumption.
- `Source_Refs` — LIT IDs that bear on the value today (reference points, not estimates).
- `Target_Source` — where the number should come from, as a `DS-NN` row in `data/data-catalog.csv` or a partner data class.
- `Note` — the parameter's history (prototype placeholder, introduced in v0.2, hard-coded in v0.1).

The catalogue rows that calibrate this model, all `Proposed`: DS-01 (FAOSTAT yields), DS-02 and DS-03 (CHIRPS, NASA POWER for the climate factor), DS-04 (World Bank Pink Sheet Arabica and Robusta prices), DS-07 (partner loan book) and DS-08 (partner member register and delivery records). The first four are open data and are the Phase 3 work; the last two need a partner and a data-sharing agreement, and their row-level content never enters the repo (`docs/ops/data-provenance.md`).

The order in which calibration would improve the model most: (1) DS-08 delivery records across at least one high-price season, which is the only way to put a number on side-selling; (2) DS-07 repayment history, for the PD anchor and curve; (3) DS-04 price history, for volatility and jumps, which is also the easiest; (4) DS-01 with DS-02/03 for the yield factor.

## Running it

```bash
pip install -r risk-tools/collective/requirements.txt       # numpy
python3 risk-tools/collective/rt7_params.py                  # validate the parameter tracker
python3 risk-tools/collective/run_region.py                  # all regions x scenarios + tornado -> data/rt7-*.csv
python3 risk-tools/collective/run_region.py --region ethiopia --paths 20000
python3 risk-tools/collective/test_rt7.py                    # checks, incl. JS parity when node is present
python3 dashboard/build.py --public                          # then rebuild the dashboard
```

Per-run manifests (every parameter with provenance, the seed, the commit) land under `risk-tools/collective/output/<region>/`, gitignored because they are regenerable. A tranche size without its assumptions is not a result; the manifest is the assumptions.

The interactive tab runs the JavaScript port on the committed parameter rows. Edits there are a scratchpad: nothing a user changes in the browser is written anywhere. To change a default, change the CSV.

## Versioning

| Bump | Means |
|---|---|
| Major | A change to the risk chain or the loss definition that makes prior output non-comparable |
| Minor | A new channel, scenario, output or parameter with a default that reproduces prior behaviour |
| Patch | Numerical fix, no methodology change |

| Date | Version | Change |
|---|---|---|
| 2026-10-07 | 0.1 | Prototype uploaded as `sfv_risk_models` (Colombia, Ethiopia, Vietnam notebooks). Archived at `archive/prototype-2026-10/`. |
| 2026-10-08 | 0.2 | Registered as RT-7. Risk chain repaired (see *What v0.1 got wrong*). Parameters moved to `data/rt7-parameters.csv` with per-parameter provenance. Scenarios RS-0..RS-5. Tornado over 16 parameters. JavaScript port and parity test. Dashboard tab. |

## Tests

`risk-tools/collective/test_rt7.py`, run in CI by `.github/workflows/pages.yml`:

- Parameter tracker well-formed: vocabulary, numeric values, every row names a target source.
- PD curve equals the base PD at the anchor, is monotone decreasing, stays inside its floor and ceiling.
- Golden case: with no volatility and a flat PD curve, EL equals Σ PD × EAD × LGD within sampling error.
- Direction: a poor season and a price crash never lower EL; residual correlation raises UL99 and leaves expected member loss unchanged.
- Side-selling fires and the forward book is short when spot runs far above forward; never when forward is above spot.
- Tranche losses sum to the pool loss on every path; the attachment search delivers the target it claims.
- Facility loss is in [0, pool]; members and simulation reproduce from the seed.
- JS parity: deterministic pieces identical to 1e-9 on a shared member set; Monte Carlo statistics within sampling error.

Not yet written, and should be before v0.3: a multi-season extension test (the OpEx bullet and CapEx amortisation currently live in one season), and a backtest harness that takes a partner loan panel in RT-1 form and reports the PD curve's calibration error. No predictive model ships without the second one (`risk-tools/README.md`).

## Open questions

- **Whose loss is the forward book?** The model charges the collective's uncovered forward obligation to the facility up to the pool. In a real structure the buyer, the collective and the lender share it by contract. Settling that allocation is a Gate-2 question in the business-research plan and would change the tail materially.
- **Multi-season.** CapEx loans amortise over four or five years; the model takes one season. A multi-season version needs a prepayment and restructure state (the competing-risks point from LIT-043 recorded against RT-1).
- **Portfolio.** Many collectives, several regions, a global price factor and regional climate factors, pooled and fed to RT-5's waterfall. That is EXP-27 and the Phase 4 of the plan this tool came in under; it also gives OQ-18 (does a multi-originator pool diversify on the right axis?) a modelling answer.
- **Insurance layer.** A parametric trigger on the climate factor is a one-line addition to the loss chain and the obvious next product question (research plan hypothesis 2). Not added until PL-1's insurance scope is settled under OQ-25.
