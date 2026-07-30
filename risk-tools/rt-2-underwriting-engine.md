# RT-2 — Underwriting engine

**Status:** Specified, not built · **Version:** 0.0 (draft spec) · **Product lines:** PL-1 · **Blocked by:** RT-1, pilot data

## Purpose

Turn origination data plus community signals into a decision, a limit and a price.

## Design

**Rules first, model later.** The engine ships as a deterministic rule set. It does not ship a learned scorecard until there is repayment history to fit and — critically — to validate against out-of-sample.

This is not conservatism for its own sake. A scorecard fitted on borrowed priors or on a few hundred loans produces confident numbers with no evidential basis, and those numbers would be used to price other people's risk and to size a first-loss tranche someone else funds. **No model ships without a backtest** is the hard rule.

### What the rules operate on

The distinctive signal here is that the group has already done the underwriting. VSLAs screen, monitor and enforce socially, which is precisely why small-ticket lending works there and fails under atomised individual assessment (Memo 1). The engine's job is to read that, not to replace it.

| Layer | Examples |
|---|---|
| Group-level | cycle completion history, attendance regularity, savings consistency, internal loan performance, governance stability, size and tenure |
| Member-level | tenure in group, internal borrowing and repayment record, role |
| Loan-level | size relative to member's savings, size relative to group fund, purpose, term against cycle timing |
| Context | seasonality, local shock indicators (see the macro watchlist) |

Group-level signals are likely to carry more weight than member-level ones, because the group's track record is longer and harder to game than any individual's. That is a hypothesis to test, not an assumption to build in permanently.

### Output

A decision, a limit, a price, and — non-negotiably — **a reason**. Every decision records which rules fired. An unexplainable decline is unacceptable both ethically and practically: origination partners have to be able to explain it to a member, and the reason codes are the raw material for improving the rules.

## Versioning

| Bump | Means |
|---|---|
| Major | Scoring scale changes, a factor is removed, decision boundaries move materially — prior decisions are no longer comparable |
| Minor | New factor added, threshold tuned within the existing scale |
| Patch | Bug fix with no decision-boundary movement |

**Every decision persists the engine version that produced it.** Without that, portfolio performance analysis silently mixes vintages scored on different logic and the resulting loss curves are meaningless.

### History

| Date | Version | Change |
|---|---|---|
| 2026-07-30 | 0.0 | Initial specification. Rules-first architecture; no model until backtest is possible. |

## Tests

Not yet written. Planned:

- **Golden cases** — a fixed set of applications with expected decisions; any change to output is deliberate or it is a bug.
- **Boundary tests** — applicants sitting exactly on each threshold.
- **Monotonicity properties** — improving a good-direction factor must never worsen a decision. Violations are almost always rule-interaction bugs and are invisible without property testing.
- **Backtest harness** — required before any learned component. Train on early vintages, test on later ones, report discrimination and calibration. A model that discriminates well but is miscalibrated will misprice the whole pool.
- **Fairness review** — check decision rates across groups where the data permits. This lends to poor people, largely women; a rule that proxies for something it shouldn't is a real risk and needs looking for deliberately.
- **Reason-code coverage** — no decision path may terminate without a reason.

## Open questions

- Which group-level signals actually predict repayment? Unknown until pilot data exists. The pilot should be designed to answer it — see RT-4.
- How much weight should group history carry relative to member history?
- Can the engine price, or only decide? Pricing needs a loss curve, which needs a track record.
- What happens when the group's own judgement and the engine disagree? The group is usually better informed. An override path with recorded reasons is probably right, and is itself a valuable data source.
