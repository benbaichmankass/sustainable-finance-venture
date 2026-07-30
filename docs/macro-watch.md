# Macro watch — live values, the watchlist, and the observation log

**Created:** 2026-07-30

## What this is

A standing watchlist of the macro conditions that bear on this project, each with why it matters *here* and a link to the authoritative source — plus a dated log of what was actually observed and what it changed.

Three files:

- `data/macro-indicators.csv` — the watchlist. Twelve indicators across cost of capital, risk appetite, market depth, borrower shocks, project economics and funding availability.
- `data/macro-snapshot.csv` — **generated**, refreshed daily by scheduled build. Current values for the indicators that have a keyless public API. Committed, so it accumulates into a record of conditions over the life of the project.
- `data/macro-log.csv` — dated observations you write by hand. What was seen, from where, and what it changes.

## Live values — what is fetched, and what isn't

Five of the twelve indicators carry a live value, refreshed daily by a scheduled build:

| | Indicator | Source | Frequency |
|---|---|---|---|
| MAC-01 | US federal funds target rate (upper) | FRED `DFEDTARU` | daily |
| MAC-02 | ECB main refinancing operations rate | ECB Data Portal | daily |
| MAC-04 | ICE BofA EM high-yield corporate OAS | FRED `BAMLEMHBHYCRPIOAS` | daily |
| MAC-07 | ENSO / Oceanic Nino Index | NOAA CPC | monthly |
| MAC-12 | EUR/ILS reference rate | ECB Data Portal | daily |

The other seven are **link-only** and the dashboard says so on each row. FAO's food price index, Bank of Israel, SIFMA/AFME issuance, KNOMAD remittances, OECD ODA and EIA energy either need an API key, publish only as spreadsheets, or have no stable machine-readable endpoint. Rather than scrape something fragile, those rows link to the source and you read the number there.

**Only keyless sources are used.** An API key would have to live in repository secrets, which makes the build unreproducible for anyone else who clones this and adds a rotation burden a research project does not need.

## How the refresh works

`.github/workflows/pages.yml` runs on a daily cron. On a scheduled or manual run it executes `dashboard/fetch_macro.py`, commits `data/macro-snapshot.csv` if it changed, rebuilds and deploys. On an ordinary push it skips the fetch — a push build must not commit back to `main`.

Run it locally any time:

```bash
python3 dashboard/fetch_macro.py
python3 dashboard/build.py
```

### The two rules the fetcher is built around

**1. It never breaks the build.** Any upstream can fail — APIs go down, formats drift, rate limits bite. A failed fetch keeps the previous value, marks the row `stale`, and exits 0. A flaky API cannot take the dashboard down with it. This is tested by simulating upstream failures.

**2. It never silently shows a stale number.** Every row carries `As_Of` (the observation date from the source) and `Fetched_At` (when we asked). The dashboard renders the observation date and its age next to every value, and flags it against that indicator's own cadence — 45 days is unremarkable for an annual series and alarming for a daily one.

That second rule is why the numbers are trustworthy. A dashboard that shows "3.75%" with no date is worse than one showing nothing, because it invites a decision on a figure that might be from last year. **The `As of` column is the one to trust.**

### Change columns

`1m`, `3m` and `12m` are differences in the series' own units, computed from observation counts appropriate to the series frequency — business-day offsets for daily series, month offsets for monthly ones. Getting this wrong is not cosmetic: applying business-day offsets to a monthly series reads 66 *months* back and labels it a 3-month change.

No colour is applied to direction. "Rates up" is not good or bad in itself, and colouring it would assert a view this project does not hold.

### Adding a live source

Add an entry to `SOURCES` in `dashboard/fetch_macro.py` with its `MAC-NN` id, a fetch function returning `[(date, value)]` ascending, and its `freq`. The three existing fetch helpers cover FRED CSV, ECB SDMX-JSON and NOAA fixed-width text. Keyless sources only.

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
