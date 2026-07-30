# RT-5 — Securitisation cash-flow model

**Status:** Specified, not built · **Version:** 0.0 (draft spec) · **Product lines:** PL-1, PL-2 · **Blocked by:** RT-1 (for real data; buildable now against synthetic portfolios)

## Purpose

Model the waterfall: take a pool of receivables, apply loss and prepayment assumptions, and distribute cash through the tranche structure. Size the tranches. Test whether the first-loss layer is adequate.

## Build this one first

RT-5 is the only tool here that does not need real data to be useful. Waterfall mechanics can be exercised against synthetic portfolios today, and doing so answers two questions that are currently blocking decisions:

- **OQ-2** — minimum viable pool size. The current working band (tens of millions warehoused, ≥USD 100m for issuance) comes from observed central tendencies across deals that do not resemble our asset class (LIT-011, LIT-012). A model with our own cost assumptions would replace a borrowed benchmark with a derived one.
- **OQ-6** — first-loss sizing. The 10–20% working range comes from the same borrowed source (LIT-013, LIT-015). Modelling it against plausible loss distributions would tell us what *our* structure needs.

Both numbers are currently placeholders taken from other people's deals. That is honest but weak, and this tool is how it gets fixed.

## Design

| Component | Does |
|---|---|
| Pool generator | Builds synthetic portfolios with controllable size, tenor, loss and correlation characteristics |
| Loss model | Applies default timing and severity; **correlation is the parameter that matters most** |
| Prepayment model | Early repayment behaviour — significant for short-tenor PL-1 assets |
| Waterfall | Distributes collections through fees, senior, mezzanine, junior per the structure |
| Tranche sizer | Given a target rating or loss coverage, sizes the layers |
| Cost model | Legal, rating, listing, structuring, servicing — fixed and variable |

**Correlation is the crux.** Community loan portfolios do not default independently: a drought or a price shock moves a whole region together. A model assuming independence will size the first-loss tranche far too thin and will look reassuring while doing it. Correlation assumptions must be explicit inputs, stress-tested across a wide range, and reported alongside every result.

The cost model is what actually answers OQ-2 — minimum viable pool size is a fixed-cost problem, not a risk problem.

### Both product lines

The same engine serves PL-1 and PL-2 with different parameters: short-tenor, many-obligor, socially-enforced versus long-tenor, single-offtaker, contracted. Running a blended pool through it is the concrete way to test OQ-8 — whether combining the lines improves the structure or contaminates the legible asset with the unproven one.

## Versioning

| Bump | Means |
|---|---|
| Major | Waterfall convention or loss-model methodology changes — prior outputs are not comparable |
| Minor | New tranche type, new stress scenario, additional cost component |
| Patch | Numerical fix with no methodology change |

Every model run persists its version, inputs and assumptions alongside its outputs. **A tranche size without its assumptions is not a result** — and this is the tool whose outputs are most likely to be quoted in a conversation with an investor months later.

### History

| Date | Version | Change |
|---|---|---|
| 2026-07-30 | 0.0 | Initial specification. |

## Tests

Not yet written. Planned:

- **Conservation property** — the waterfall must distribute exactly what it receives, to the cent, under every scenario. This is the single most important test; a leak here invalidates everything.
- **Ordering property** — senior is never paid after junior in the same period; subordination must hold by construction.
- **Golden cases** — hand-calculated small structures with known correct answers.
- **Degenerate cases** — zero losses, total losses, single-loan pool, all prepaid at once. These are where waterfall code breaks.
- **Monotonicity** — more losses must never improve a senior tranche's outcome.
- **Correlation sweep** — run the same pool from independence to near-perfect correlation and report the range. If the recommended first-loss size is not robust across that sweep, the recommendation is not usable.
- **Cost-model sensitivity** — vary fixed costs and report how the minimum viable pool size moves.

## Open questions

- What loss and correlation assumptions are defensible with no track record? Probably a wide sensitivity range rather than a point estimate — and the honest output is a range, not a number.
- Should the model target a rating-agency methodology, and if so which? Depends on whether an agency will engage pre-track-record, which is still open in Memo 3.
- For PL-2, does a utility PPA permit assignment of receivables at all? If it does not, there is no waterfall to model on that line.
- What servicing cost is realistic for community-originated assets? Likely higher per dollar than any comparable deal, and that goes straight into the minimum-viable-scale answer.
