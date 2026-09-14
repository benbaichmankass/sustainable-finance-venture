# Risk management tools

The toolkit that makes community-originated cash flows underwritable. Registry: data/risk-tools.csv; one document per tool in this directory.

**Nothing here is built yet.** Every tool is at specification stage. That's stated honestly in the registry rather than dressed up as "in progress" — the specs exist so that when data arrives the build is a matter of execution, not design.

## The tools

| ID | Tool | Consumes | Blocked by |
| :---- | :---- | :---- | :---- |
| RT-1 | Origination data schema | — | OQ-3 |
| RT-2 | Underwriting engine | RT-1 | RT-1, pilot data |
| RT-3 | Monitoring & early-warning | RT-1 | RT-1 |
| RT-4 | Impact evaluation module | RT-1 | OQ-4/5/7 |
| RT-5 | Securitisation cash-flow model | RT-1 | RT-1 |
| RT-6 | Unit-economics model | benchmarks; RT-5 loss shape | partner/counsel data for calibration |

**RT-1 is the critical path.** Everything consumes its output. Get the field list wrong and every downstream tool inherits the error — and unlike code, an origination schema cannot be fixed retroactively, because the data you failed to capture is simply gone.

## Why these five

They map to the venture's position in the stack. We sit in the risk layer (product-design/business-plan.md §3): origination partners handle disbursement and collection, we handle underwriting rules, monitoring, tranching and evidence. These five are that layer made concrete.

RT-5 is the one that can be built first with no real data — waterfall mechanics can be exercised against synthetic portfolios, and it answers OQ-2 and OQ-6, which are currently blocking decisions. RT-6 sits on top of the same fixed-cost logic from the P\&L side: it takes a loss assumption and asks whether the *structuring company* makes money (OQ-10), where RT-5 asks whether the *structure* survives.

## Conventions

**Versioning.** Semantic, per tool, recorded in the tool's document and in data/risk-tools.csv:

- **Major** — a change that invalidates comparison with prior output. A removed schema field, a changed scoring scale, a different waterfall convention. Requires a migration note.  
- **Minor** — additive and backward-compatible. A new optional field, a new alert type.  
- **Patch** — fixes that don't change the interface.

Every tool document carries a version history table with date, version, change and rationale. 0.x means specification only, nothing implemented.

**Schema changes are special.** RT-1 is a data contract with origination partners in the field. A major version bump means retraining people and possibly reprinting forms. Batch changes; don't drip them.

**Tests.** Each tool states its test strategy in its own document. The standing requirements:

- Deterministic golden cases for anything doing arithmetic on money.  
- Property-based tests for invariants (a waterfall must distribute exactly what it receives; a score must stay in range).  
- Backtests against held-out data for anything predictive — and no predictive model ships without one.  
- Synthetic-data tests so tools are testable before real portfolios exist.

**No model without a backtest** is the rule that matters most. The temptation with thin data is to ship a plausible-looking scorecard. A model that has never been validated out-of-sample is a guess wearing a number, and it would be used to price other people's risk.

## Adding a tool

1. Add a row to data/risk-tools.csv with the next RT-N.  
2. Add risk-tools/rt-N-slug.md following the structure of the existing docs: purpose, design, inputs/outputs, versioning, tests, open questions.  
3. Rebuild the dashboard.

## Built so far

|  | What exists | Where |
| :---- | :---- | :---- |
| RT-1 | 57-field origination schema (v0.1) \+ validator | [schema/](http://schema/), [tools/validate\_schema.py](http://tools/validate_schema.py) |
| RT-2 | Rules-based scorecard: band, limit, reasons both ways | [tools/score\_loans.py](http://tools/score_loans.py), [rt-2-rt-3-scaffolds.md](http://rt-2-rt-3-scaffolds.md) |
| RT-3 | Portfolio monitor: PAR, arrears concentration, alerts | [tools/monitor\_portfolio.py](http://tools/monitor_portfolio.py), [rt-2-rt-3-scaffolds.md](http://rt-2-rt-3-scaffolds.md) |
| RT-5 | Synthetic portfolio simulator \+ waterfall \+ 6 stress scenarios | [tools/simulate\_portfolio.py](http://tools/simulate_portfolio.py), [rt-5-simulator.md](http://rt-5-simulator.md) |
| RT-6 | Three-scenario unit-economics P\&L \+ pilot yardstick \+ sensitivity | [tools/economics\_model.py](http://tools/economics_model.py), [rt-6-economics-model.md](http://rt-6-economics-model.md) |

RT-4 remains at specification stage — it is gated on a pre-registered design with an academic partner, not on code.

## Running the chain

python3 risk-tools/tools/generate\_dataset.py \--out /tmp/synth   \# RT-1-conformant synthetic data

python3 risk-tools/tools/validate\_schema.py \--data /tmp/synth   \# proves schema and generator agree

python3 risk-tools/tools/score\_loans.py     \--data /tmp/synth   \# RT-2

python3 risk-tools/tools/monitor\_portfolio.py \--data /tmp/synth \# RT-3

python3 risk-tools/tools/simulate\_portfolio.py                  \# RT-5

python3 risk-tools/tools/economics\_model.py                     \# RT-6

python3 risk-tools/tools/test\_toolchain.py                      \# end-to-end checks (CI)

**Nothing here is calibrated and nothing is field-tested.** Every tool says so in its own output and its own doc, rather than relying on the reader to infer it. None of these outputs should be shown to a partner or an investor as a result.  
