# Macro watch — how this tab works, and why it has no live numbers

**Created:** 2026-07-30

## What this is

A standing watchlist of the macro conditions that bear on this project, each with why it matters *here* and a link to the authoritative source — plus a dated log of what was actually observed and what it changed.

Two files:

- `data/macro-indicators.csv` — the watchlist. Twelve indicators across cost of capital, risk appetite, market depth, borrower shocks, project economics and funding availability.
- `data/macro-log.csv` — dated observations. What was seen, from where, and what it changes.

## Why there are no live numbers on the page

This was a deliberate choice and it is worth being explicit about, because "what are rates doing right now" is the obvious thing to want.

The dashboard is a static page generated from the repo. To show a current interest rate it would have to either (a) fetch from an API in the browser, or (b) bake a snapshot in at build time. Both are worse than they look:

- **Client-side fetching** breaks the property that makes this dashboard durable — it opens from `file://`, works offline, and will still work in five years with no dependency on anyone's API still existing at the same URL with the same auth model.
- **Build-time snapshots go stale silently.** A page showing "Fed funds 4.25%" with no visible staleness is worse than a page showing nothing, because it invites decisions on a number that may be months old. And this repo's own standard is that we never state a number the source doesn't currently state (`CLAUDE.md` §6).

So the tab gives you the **fastest possible path to the real number** — one click to the authoritative source — rather than a copy of it that rots.

**If you want live numbers, that is buildable** and the honest way to do it is a scheduled build: a cron trigger on the Pages workflow fetches a handful of open APIs (ECB and FRED both serve JSON without a key), writes a snapshot with an explicit "as of" timestamp, and the page renders the timestamp as prominently as the value. That is a real piece of work — error handling, rate limits, a stale-data indicator — and it should be a deliberate decision rather than something bolted on. Say the word.

## What the log is for

The watchlist tells you where to look. The log is the part that compounds.

A research project makes decisions over years, and the reasoning behind a decision is only recoverable if you wrote down what the world looked like at the time. "We sized the first-loss layer at 15% in Q3 2026 when EM spreads were wide and aid budgets were contracting" is a defensible record. "We sized it at 15%" is not — and in two years nobody, including you, will remember which it was.

Log an entry when something moves that would change a decision. Skip the rest — a log of everything is a log nobody reads.

Each entry records:

| Field | |
|---|---|
| `Date` | when observed |
| `Indicator_Refs` | which `MAC-NN` it relates to |
| `Observation` | what the source actually said, with no embellishment |
| `So_What` | what it changes — the reason the entry exists |
| `Source_Checked` | where it came from |

## The discipline

The same rule as the literature matrix applies: **never state a number the source doesn't state.** If a figure is an inference or a recollection, mark it as such. The value of this log is that it can be trusted later; a single made-up number destroys that for every entry.

## Adding an indicator

1. Add a row to `data/macro-indicators.csv` with the next `MAC-NN`.
2. Fill in `Why_It_Matters_Here` properly — not what the indicator is, but what it changes for *this* project. If you can't write that sentence, the indicator probably doesn't belong on the list.
3. Verify the URL resolves.
4. Rebuild the dashboard.
