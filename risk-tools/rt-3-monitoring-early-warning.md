# RT-3 — Monitoring and early-warning system

**Status:** Specified, not built · **Version:** 0.0 (draft spec) · **Product lines:** PL-1, PL-2 · **Blocked by:** RT-1

## Purpose

Track portfolio performance against expectation and raise alerts early enough to act.

Two audiences, and they need different things:

- **Operations** — which groups need attention this week.
- **The first-loss provider** — is the junior tranche performing as underwritten. LIT-013 makes documented monitoring part of what a DFI evaluates when deciding whether to fund a junior layer, so this tool is partly a fundraising instrument.

## Design

### Levels

| Level | Watching for |
|---|---|
| Loan | days past due, partial payment, restructure, claim |
| Group | arrears concentration, attendance decline, cycle disruption, savings falling off |
| Portfolio | vintage curves against expectation, geographic concentration, delinquency migration |
| Environment | shocks that move whole cohorts at once — see the macro watchlist |

**Group level is where the early signal lives.** By the time a loan is 30 days past due, the information is old. Attendance dropping or savings contributions thinning are visible earlier and are observable in data the group already produces.

### Alerts

Every alert carries: what fired, the threshold crossed, the trend that led to it, and a suggested action. An alert that only says "group 14 is deteriorating" transfers work rather than reducing it.

**Alert fatigue is the failure mode to design against.** A system that fires constantly gets ignored, and an ignored monitoring system is worse than none because it creates false confidence. Thresholds should start deliberately conservative and be tuned against observed false-positive rates.

### Environmental layer

Community portfolios fail in correlated ways. A drought, a price spike, a remittance disruption hits every group in a region simultaneously — which is exactly the risk that diversification within a single product line does not address. The monitoring system should ingest the indicators tracked in `data/macro-indicators.csv` so that a regional cluster of alerts is interpreted as one shock rather than fifteen unrelated problems.

## Versioning

| Bump | Means |
|---|---|
| Major | Alert definitions change so that historical alert rates are no longer comparable |
| Minor | New alert type, new data source |
| Patch | Threshold tuning within an existing definition |

Alert history retains the version that produced it, for the same reason RT-2 decisions do.

### History

| Date | Version | Change |
|---|---|---|
| 2026-07-30 | 0.0 | Initial specification. |

## Tests

Not yet written. Planned:

- **Synthetic-portfolio replay** — construct portfolios with known deterioration patterns and assert the right alerts fire at the right time. This is how the tool gets tested before a real portfolio exists.
- **Known-shock replay** — replay a historical shock (a drought season, a currency move) and check the environmental layer catches it.
- **False-positive rate** — measured against a stable synthetic portfolio; a healthy portfolio must stay quiet.
- **Lead-time measurement** — for each alert type, how far ahead of the loss does it fire? An alert with zero lead time is a report, not a warning.
- **Threshold-boundary tests** — no flapping when a metric sits on the line.

## Open questions

- What lead time is achievable? Unknown until there is real data. It determines whether the tool is genuinely preventive or merely diagnostic.
- Which group-level signals degrade first? Testable in the pilot and worth designing the pilot to answer.
- How do alerts reach the field — and who acts on them? A system that alerts head office about a group nobody visits changes nothing.
- What does the first-loss provider need to see, and how often? Worth asking PT-07 directly rather than guessing.
