# RT-7 — Collective facility risk model

**Status:** Built, running · **Version:** 0.3 · **Calibration: partial** (world prices, national yields, district rainfall and the Colombian farm-gate basis observed; farm size, costs, household floor and Colombian loan size and arrears from literature and proxy data; the rest assumed) · **Product lines:** PL-1 · **Code:** `risk-tools/collective/` (Python reference) and `dashboard/rt7-model.js` (browser port) · **Parameters:** `data/rt7-parameters.csv` · **Scenarios:** `data/rt7-scenarios.csv` · **Results:** `data/rt7-region-results.csv`, `data/rt7-sensitivity.csv` · **Interactive:** the dashboard's *Collective model* tab

## Purpose

Answer the question a lender to a producer collective has to answer before it lends: **what loss distribution am I taking on, and what drives it?**

The collective is the borrower of record. It on-lends to members (seasonal OpEx loans and asset CapEx loans) and markets a share of their crop, part of it sold forward before the season. That is the structure OQ-13 asks about — securitisation attaching one level up, so the community's own risk management stays intact — and it is the structure LIT-031 shows already operates at scale (Root Capital's enterprises "on-lend funds as smaller loans to individual producers and, in doing so, bear the risk of repayment").

The model exists for three jobs, in order:

1. **Design.** Which structural choices (how much is sold forward, how delivery is enforced, how thick a collective reserve, what loan sizes against what farm) move the loss distribution, and in which direction. These answers are robust to calibration because they are about *shape*.
2. **Partner diagnostics.** When a real collective's data arrives, the same model with its parameters replaced is the readiness diagnostic the practice sells (Lane A in `docs/venture/solo-operator-track.md`).
3. **Securitisation readiness.** Not a pilot objective (decision register, 2026-09-09). But the facility's loss distribution is exactly what RT-5's waterfall consumes, and the illustrative tranche cut is kept so a product designed today can be pooled later without redesign.

## What it is not

**It is only partly calibrated.** Since 2026-10-08, 12 of the 105 rows of `data/rt7-parameters.csv` are `Basis: observed`: the reference price level and its volatility (DS-04, World Bank Pink Sheet) and the national yield level and its year-to-year variability (DS-01, FAOSTAT), per region. Every loan, cost, household, delivery, buffer and credit parameter is still an assumption, and two of those cite literature only as a *reference point* (LIT-035, LIT-036 and LIT-037). The observed inputs make the model's *scale* real; the assumed ones still decide its *losses*. Every number this model produces remains a statement about the model, not about any coffee collective.

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

**The forward-shortfall allocation is an input, not a conclusion (v0.3).** `fwd_shortfall_facility_share` says how much of the collective's uncovered forward obligation reaches the cash flow in front of the lender. v0.2 silently set it to all of it. The right value is whatever the buyer contract and the facility agreement say (RA-05), and the business-research plan's step 5 is to decide it; the model's job is to show what each answer costs, which it now does in one number.

**Seasons in a row, defaults absorbing (v0.3).** With `horizon_seasons` above one the same chain runs season after season: a member who defaults leaves the collective and takes their deliveries with them, CapEx balances amortise on their annuity schedule, OpEx renews for survivors, the forward book is re-contracted each season on the survivors' expected volume, the collective's unused reserve carries forward, and the price factor persists as an AR(1) (`price_persistence`). Losses are cumulative over the horizon as a share of the initial pool, so a multi-year facility's tranche cut is on the horizon loss. What it does not have: prepayment, restructuring or re-borrowing states (LIT-043's competing risks), a forward price that moves with the market, or any learning by the collective. A one-season horizon reproduces v0.2 to the last decimal, and the test suite checks that.

**The district's own weather enters the climate factor to the extent the yield record supports (v0.3).** The regional climate factor can be a mix of a bootstrapped district rainfall anomaly (DS-02, 1981 onward, inside a committed administrative polygon) and a normal residual, weighted by `climate_rain_beta`, the observed correlation between national yield residuals and that anomaly. The bootstrap keeps the district's real skew and the frequency of its deep deficit years; the residual keeps everything rainfall does not explain. With a weak correlation the factor is close to normal, which is honest: a national yield series against a district rain series cannot carry more. The sign is free, because for some origins the wet years are the bad ones.

**Portfolio: one price, correlated regions, local noise (v0.3).** `rt7_portfolio.py` runs many collectives through the same chain with shared systematic draws: one global price factor and jump series, one climate factor per region (tied across regions by `portfolio_climate_cross_corr` through a world factor), and a collective-level share of climate variance that is its own (`collective_climate_idio_share`). Residual correlation stays inside each collective. The pooled distribution is compared with two benchmarks, the sum of standalone tails (no diversification credit) and the pool with the shared factors switched off (independent collectives), so the cost of the shared factors is a number rather than an argument. That is EXP-27's simulation and OQ-18's test.

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

## What the model shows

Shapes first, levels with a stated caveat. From `data/rt7-region-results.csv` and `data/rt7-sensitivity.csv` (5,000 paths, seed 42; sensitivities at 3,000 paths), after the 2026-10-08 calibration and the same day's re-anchoring of the cost base on literature and proxy data.

**0. Re-anchoring the cost base put the base case back on a credible level.** The first calibration moved the reference price to its observed level (Arabica 7,750 USD/t over the twelve months to September 2026, Robusta 4,046) while costs, floors and loan sizes stayed at the prototype's levels, and the Colombian base-case expected loss collapsed to 0.35 percent of pool with a normal-year PD of 1.1 percent. Phase 3b replaced the assumed farm size, production cost, household floor and (for Colombia) loan size, arrears rate and farm-gate basis with values derived from published sources and a proxy loan book (`data/rt7-literature-inputs.csv`, DS-09 to DS-11). The Colombian base case is now 1.5 percent expected loss with a normal-year PD of 5.7 percent, against a Kiva-partner arrears proxy of 7.7 percent; Ethiopia 1.1 percent. Vietnam is unchanged at 0.2 percent because Robusta revenue per hectare (3.1 t at 4,046 USD/t) dwarfs its costs and floor at any plausible level, which says the Vietnamese case is a price-and-delivery case, not a credit one.

**1. The household floor is now the binding constraint for the smallest farms, and that is a finding about the floor, not an artefact.** With a subsistence floor of 3,440 USD (DANE 2024 rural poverty line for a household of four) and a mean farm of 1.28 ha, 27 percent of Colombian members have debt-service cover below 1 in a normal year: the sub-half-hectare tail of the farm-size distribution cannot carry a household of four on coffee alone. In reality those households live on off-farm income, and `other_income_mean` is still an assumption (500 USD) in Colombia and Vietnam; Ethiopia's is observed (553 USD, LIT-033). The parameter the floor makes decisive is other income, which is the first thing a partner survey should measure.

**2. The tail is still delivery risk, but the cost base now matters too.** The price spike (RS-4) remains the only scenario that wipes the pool in every region, through side-selling against the forward book; delivery enforcement still comes before credit enhancement. But in Colombia the top of the tornado is now `collective_fixed_cost_usd` (expected loss 1.0 to 4.1 percent across its range), then `hedge_ratio_mean`, `price_vol` and `household_floor_usd`; in Ethiopia `hedge_ratio_mean`, `price_vol` and the floor. The collective's fixed cost is the one assumption left with no source at all, and it is the first thing to ask a cooperative for.

**3. The forward book makes the facility's exposure asymmetric, and re-anchoring reversed one half of it.** A price crash (RS-3) raises member losses (Colombia 3.3 to 7.5 percent of pool) and, now that costs and floors are at realistic levels, raises the facility's expected loss too (1.5 to 5.4 percent): the forward book no longer insulates the collective enough to cover the members. The spike still cuts member losses while it breaks the collective. Members and lender hold opposite halves of the price distribution at the collective level; at the facility level the crash now bites through the buffer.

**4. A leaf-rust-scale year breaks Colombia (15.5 percent expected loss, shortfall in 46 percent of paths) and touches Ethiopia (5.5 percent).** The difference is still the observed national yield CV (0.16 against 0.10), and a national series smooths over districts: it is a floor on the regional factor the model wants. DS-02 with a district boundary is the next calibration step for this reason, and LI-17 (Dak Lak yield 13 percent below the national trend) shows the direction of the bias.

**5. Price volatility was assumed slightly high; price jumps were assumed far too timid.** Observed annualised log volatility is 0.21 for Arabica and 0.19 for Robusta over 2005 to 2026, against the prototype's 0.25 to 0.30. But 14 percent of rolling twelve-month windows moved by more than 40 percent in log terms, where the model's jump assumption implies far fewer. The jump parameters stay assumptions, with the observed distribution recorded next to them in `data/rt7-calibration.csv`.

**6. The farm-gate basis in Colombia is about 10 percent, twice the assumption.** Thirty months of the FNC internal base price, converted to green terms at factor 94 and to dollars at the TRM, sit on average 9.6 percent below the Pink Sheet Arabica series (sd 2.8 points) and 10.8 percent below the ICO Colombian milds indicator. The assumed 5 percent understated what a cooperative loses to the chain before it buys. Ethiopia's implied farm-gate from LIT-033 is not usable at the official 2023 exchange rate (it equals the world price), and Vietnam's single-month observation sits above the reference in a spike; both stay assumptions.

**7. The senior target is attainable in a normal year and not in a stressed one.** Colombia needs an 8.5 percent first-loss layer for a 25 bp senior expected loss in the base case, 20 percent in a poor season, 37 percent in a leaf-rust year, and cannot reach it at all under a price spike. The base-case figure now sits inside RT-5's 10 to 20 percent working range (LIT-013, LIT-015); the stressed figures are the delivery channel again.

**8. Who carries an undelivered forward tonne decides the tail (v0.3, RA-05).** With the collective's uncovered forward shortfall charged to the cash flow in front of the lender, as v0.2 assumed, the price spike (RS-4) gives Colombia 6.7 percent expected loss and wipes the pool in the tail. With the same shortfall carried by the buyer or the collective's equity (`fwd_shortfall_facility_share` 0) the same scenario gives 0.7 percent and a 6 percent UL99; Ethiopia 3.4 to 0.5, Vietnam 10.1 to 0.2. Half-and-half still leaves Colombia at 4.1 percent. In the base case the parameter barely registers (shortfalls are rare), which is the point: it is a tail allocation, and it is written in a contract, not estimated from data. Business-research step 5.

**9. Over several seasons the loss front-loads, and the model is optimistic about why (v0.3).** Over three seasons Colombia's cumulative expected loss is 2.9 percent of the initial pool (1.54, 0.83, 0.54 by season), over five 3.5 percent, 0.7 a season; Ethiopia 2.0 and 2.2; Vietnam 0.5 and 0.7. Losses fall season by season because members who default leave, CapEx balances amortise, and the collective's reserve accumulates (Colombia carries about 9,000 USD after five seasons). All three are survivorship effects, and the model has no new members, no re-borrowing after default and no restructuring, so the decline is an upper bound on how benign later seasons are. The first-loss layer a 25 bp senior target needs over five seasons is 38 percent in Colombia, against 7.7 for one.

**10. The district's rainfall history changes the shape of the climate factor, and in Colombia it says wet years are the bad years (v0.3, DS-02).** Over 1981 to 2024 the correlation between national yield residuals and the district rainfall anomaly is -0.43 in Colombia (standard error about 0.16), 0.03 in Ethiopia and -0.07 in Vietnam. Colombia's sign fits the leaf-rust years coinciding with the La Nina rains; the other two are indistinguishable from zero, so their factor stays normal in all but name. Applied, the Colombian base case is unchanged (1.51 percent) and the leaf-rust scenario's UL99 moves from 36.8 to 38.3 percent. The district rainfall records themselves are close to normal in annual totals (tenth percentile -1.2 to -1.3 standard deviations, skew near zero), so rainfall totals are not where a fatter yield tail would come from; pests, disease and intra-season timing are, and those need a district yield series, not more rainfall.

**11. Pooling twelve collectives across three regions diversifies the climate and not the price (v0.3, EXP-27, OQ-18).** In the base case the portfolio's expected shortfall beyond the 99th percentile is 17.8 percent of the pool, against 19.8 with no diversification credit at all and 10.0 if the collectives were independent: pooling recovers about a fifth of what independence would give. The reason is in the loss correlations, 0.7 to 1.0 between collectives in one region and 0.65 across regions even though the regions' rainfall anomalies are uncorrelated (mean pairwise 0): the shared axis is the global price factor, and every collective side-sells against the same spike. In the price spike the portfolio's tail equals the standalone sum (97.6 percent); in a leaf-rust year it is 44.7 against 47.5. Colombia carries 64 percent of the portfolio's expected loss. For OQ-18 that is a modelling answer on the environmental channel: a multi-region pool diversifies weather and not price, so the price channel needs hedging, delivery enforcement or buyer-borne cover, not a wider pool; the institutional channel (LIT-036, LIT-037) is not in the model and is EXP-25's job.

Caveat on all of it: these are relationships between the model's own parameters. Per region, 5 to 6 are observed, 2 to 5 come from literature arithmetic, 2 (Colombia) from a proxy loan book, and about 40 remain assumptions. The level is now defensible as an order of magnitude; the loan mix, rates, tenors, LGDs and the collective's own costs still rest on the prototype's choices.

## Data source mapping

Every parameter in `data/rt7-parameters.csv` carries four provenance fields, which the dashboard renders as the *Data sources* table:

- `Basis` — `assumption` · `literature` · `proxy` · `observed` (`docs/ops/data-provenance.md`). Observed: price level, volatility and persistence, yield level and variability, the district rain weight in the climate factor, the Colombian basis, and the portfolio layer's climate correlations. Literature: farm size (Colombia, Ethiopia), production cost and household floor (all three), Ethiopian other income. Proxy: Colombian seasonal loan size and normal-year PD from a Kiva partner book. The rest assumption.
- `Source_Refs` — DS, LIT and LI IDs the value rests on today.
- `Target_Source` — where the number should come from, as a `DS-NN` row in `data/data-catalog.csv` or a partner data class.
- `Note` — the parameter's history (prototype placeholder, introduced in v0.2, calibrated on which date from what).

**Literature inputs.** A value derived from a published figure by arithmetic (a per-household cost divided by a coffee area, a poverty line times a household size, a peso cost converted at a dated exchange rate) is written out in `data/rt7-literature-inputs.csv`, one row per derivation with the source figures, the arithmetic, the reference year and whether it is applied. `calibrate_rt7.py` reads that file: applied rows go into the tracker with `Basis: literature`, the rest (living-income benchmarks, the FNC productivity figure, the Dak Lak yield, farm-gate observations) ride along as observations in `data/rt7-calibration.csv`. Sources: Fairtrade's living income reference price notes for Colombia and Ethiopia (LIT-045, LIT-046, LIT-047), the Sidama household survey (LIT-033), Global Living Wage Coalition benchmarks (LIT-048, LIT-049), FNC and StoneX sector figures (LIT-050, LIT-051), the DANE poverty line (LIT-052), Vietnam's Decree 07/2021 poverty standard (LIT-053) and three Dak Lak sources (LIT-054 to LIT-056).

**The design choice behind the floor.** `household_floor_usd` is a subsistence threshold (a poverty line, or observed consumption where a survey gives one), not a living income. The living-income benchmarks are recorded beside it (LI-04, LI-11, LI-15) and roughly double it; a living-income floor is a scenario to run, not the base case, because the model's question is whether debt gets serviced, not whether the household lives decently.

The catalogue rows that calibrate this model: DS-01 (FAOSTAT national yields), DS-02 (CHIRPS district rainfall inside committed geoBoundaries polygons), DS-03 (NASA POWER district climate), DS-04 (World Bank Pink Sheet Arabica and Robusta prices), DS-09 (exchange rates), DS-10 (FNC internal and ex-dock prices, area by department) and DS-11 (Kiva agriculture loans and partner metrics, a proxy population) are `Validated` and pulled by `scripts/ingest/`; `scripts/ingest/calibrate_rt7.py` turns them and the literature inputs into `data/rt7-calibration.csv` and, with `--apply`, into the parameter tracker. `data/rt7-climate-history.csv` carries the per-region rainfall anomaly series the climate factor bootstraps from. DS-07 (partner loan book) and DS-08 (partner member register and delivery records) need a partner and a data-sharing agreement, and their row-level content never enters the repo.

What the calibration file also records without writing into the model: the long-window price mean, the distribution of twelve-month price changes and the share of large moves, the annual rainfall CV at the district centroids, the correlations of national yield residuals with rainfall anomalies and with price changes, the Colombian basis against the ICO Colombian milds indicator, Kiva loan terms and default rates, and the Vietnamese Kiva figures that were judged too distorted to apply (one paused partner holding every coffee loan).

The order in which further calibration would improve the model most: (1) DS-08 delivery records across at least one high-price season, which is the only way to put a number on side-selling; (2) a cooperative's accounts for `collective_fixed_cost_usd` and margin, now the top of the Colombian tornado; (3) DS-07 repayment history, for the PD anchor and curve and the loan mix; (4) other income for Colombian and Vietnamese households, which the floor makes decisive; (5) a district-level yield factor from DS-02 with a boundary; (6) a farm-gate series for Ethiopia and Vietnam.

## Running it

The portfolio layer: `python3 risk-tools/collective/rt7_portfolio.py` reads `data/rt7-portfolio.csv` and writes `data/rt7-portfolio-results.csv` and `-histogram.csv`. DS-02 is refreshed with `python3 scripts/ingest/ds02_chirps.py` (six grid tables of 25 to 85 MB each from the IRI Data Library; a few minutes).


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
| 2026-10-08 | 0.2 (calibrated) | Phase 3: DS-01, DS-03 and DS-04 ingested with provenance; price level and volatility and national yield level and variability set to observed values per region via `scripts/ingest/calibrate_rt7.py`. No change to the model; the base case moved because the price level did. |
| 2026-10-08 | 0.3 | Phase 4: `horizon_seasons` and `price_persistence` (multi-season chain with absorbing defaults, amortising CapEx, carried reserve); `fwd_shortfall_facility_share` (RA-05 as an input); `climate_rain_beta` with a bootstrapped district rainfall history (DS-02 ingested inside committed geoBoundaries polygons); external factor injection and `rt7_portfolio.py` (twelve synthetic collectives, shared price factor, correlated regional climate; EXP-27, OQ-18). Every default reproduces v0.2, and the test suite checks the one-season case against the committed results. |
| 2026-10-08 | 0.2 (re-anchored) | Phase 3b: `proxy` added to the basis vocabulary; DS-09 (exchange rates), DS-10 (FNC prices and area) and DS-11 (Kiva loans, proxy) ingested; `data/rt7-literature-inputs.csv` introduced for values derived by arithmetic from LIT-033 and LIT-045 to LIT-056. Farm size, production cost, household floor, Ethiopian other income, Colombian basis, seasonal loan size and normal-year PD re-anchored. No change to the model code. |

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

- **Whose loss is the forward book?** Now an input (`fwd_shortfall_facility_share`, RA-05) rather than a hidden assumption, and the model prices each answer. The open part is the contract: which allocation a buyer will sign, and what a delivery-enforcement mechanism costs. A Gate-2 question in the business-research plan.
- **Multi-season, properly.** The horizon exists, but without prepayment, restructuring or re-borrowing states (LIT-043's competing risks, recorded against RT-1), a forward price that follows the market, or a collective that changes its forward share after a bad year. Each of those is a behavioural assumption a partner's history would have to supply.
- **Portfolio calibration.** The layer exists (`rt7_portfolio.py`, EXP-27) and OQ-18 has a first modelling answer. What it rests on is the cross-region climate correlation and the local share, both observed from rainfall rather than from losses, and a residual correlation that stays within each collective. The institutional channel across collectives in one market (LIT-036, LIT-037) is not in it; EXP-25 is the way to put it there.
- **District yields.** The climate factor now carries the district's rainfall history, but its weight is set against national yields. A district yield series (DS-08 delivery records, or a national statistics office's department-level production) would let the weight and the yield CV both be set at the district.
- **Insurance layer.** A parametric trigger on the climate factor is a one-line addition to the loss chain and the obvious next product question (research plan hypothesis 2). Not added until PL-1's insurance scope is settled under OQ-25.
