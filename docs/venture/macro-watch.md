# Macro watch — live values, the watchlist, and the observation log

**Created:** 2026-07-30

## What this is

A standing watchlist of the macro conditions that bear on this project, each with why it matters *here* and a link to the authoritative source — plus a dated log of what was actually observed and what it changed.

Three files:

- `data/macro-indicators.csv` — the watchlist. Sixteen indicators across cost of capital, risk appetite, market depth, borrower shocks, project economics and funding availability.  
- `data/macro-snapshot.csv` — **generated**, refreshed daily by scheduled build. Current values for the indicators that have a keyless public API. Committed, so it accumulates into a record of conditions over the life of the project.  
- `data/macro-history.csv` — **generated**. Up to twelve years of monthly observations per live series. This is what the charts read.  
- `data/macro-log.csv` — dated observations you write by hand. What was seen, from where, and what it changes.

## Live values — what is fetched, and what isn't

Eleven of the sixteen indicators carry a live value and a charted history, refreshed daily by a scheduled build:

|  | Indicator | Source | Frequency |
| :---- | :---- | :---- | :---- |
| MAC-01 | US federal funds target rate (upper) | FRED `DFEDTARU` | daily |
| MAC-02 | ECB main refinancing operations rate | ECB Data Portal | daily |
| MAC-03 | Bank of Israel policy rate | BOI SDMX `BR` / `MNT_RIB_BOI_D` | daily |
| MAC-04 | ICE BofA EM high-yield corporate OAS | FRED `BAMLEMHBHYCRPIOAS` | daily |
| MAC-06 | FAO Food Price Index | FAO monthly CSV | monthly |
| MAC-07 | ENSO / Oceanic Nino Index | NOAA CPC | monthly |
| MAC-12 | EUR/ILS reference rate | ECB Data Portal | daily |
| MAC-13 | USD/ILS representative rate | BOI SDMX `EXR` / `RER_USD_ILS` | daily |
| MAC-14 | FAO Cereals Price Index | FAO monthly CSV | monthly |
| MAC-15 | US 10-year Treasury yield | FRED `DGS10` | daily |
| MAC-16 | Brent crude oil price | FRED `DCOILBRENTEU` | daily |

The remaining five are **link-only** and the dashboard says so on each row. SIFMA/AFME issuance volumes, FEWS NET food-security outlooks, EIA energy demand, KNOMAD remittances and OECD ODA either need an API key, publish only as PDFs or spreadsheets, or have no stable machine-readable endpoint. Rather than scrape something fragile, those rows link to the source and you read the number there.

**Only keyless sources are used.** An API key would have to live in repository secrets, which makes the build unreproducible for anyone else who clones this and adds a rotation burden a research project does not need.

## Charts

Every live series gets a panel on the Macro watch tab and a sparkline in its watchlist row. Three rules govern them:

- **One series per chart, never a shared axis.** These are percentages, index points, exchange rates and dollars a barrel. Putting two of them on one frame would imply a comparison that does not exist — the most misleading thing a chart can do.  
- **Each panel states its own date range and point count.** Sources do not all offer the same history: FRED serves the EM spread series from 2023 only, whatever start date is requested, so that panel is a three-year window sitting beside twelve-year ones. The footer is how you tell.  
- **Monthly resolution, twelve years.** Daily series are downsampled to the last observation of each month. A daily point is below one pixel at this width, and keeping them would make the committed file large and its diffs unreadable — which would defeat the reason for committing it.

## How the refresh works

`.github/workflows/pages.yml` runs on a daily cron. On a scheduled or manual run it executes `dashboard/fetch_macro.py`, commits `data/macro-snapshot.csv` and `data/macro-history.csv` if they changed, rebuilds and deploys. On an ordinary push it skips the fetch — a push build must not commit back to `main`.

Run it locally any time:

python3 dashboard/fetch\_macro.py

python3 dashboard/build.py

### The two rules the fetcher is built around

**1\. It never breaks the build.** Any upstream can fail — APIs go down, formats drift, rate limits bite. A failed fetch keeps the previous value, marks the row `stale`, and exits 0\. A flaky API cannot take the dashboard down with it. This is tested by simulating upstream failures.

**2\. It never silently shows a stale number.** Every row carries `As_Of` (the observation date from the source) and `Fetched_At` (when we asked). The dashboard renders the observation date and its age next to every value, and flags it against that indicator's own cadence — 45 days is unremarkable for an annual series and alarming for a daily one.

That second rule is why the numbers are trustworthy. A dashboard that shows "3.75%" with no date is worse than one showing nothing, because it invites a decision on a figure that might be from last year. **The `As of` column is the one to trust.**

### Change columns

`1m`, `3m` and `12m` are differences in the series' own units, computed from observation counts appropriate to the series frequency — business-day offsets for daily series, month offsets for monthly ones. Getting this wrong is not cosmetic: applying business-day offsets to a monthly series reads 66 *months* back and labels it a 3-month change.

No colour is applied to direction. "Rates up" is not good or bad in itself, and colouring it would assert a view this project does not hold.

### Adding a live source

Add an entry to `SOURCES` in `dashboard/fetch_macro.py` with its `MAC-NN` id, a fetch function returning `[(date, value)]` ascending, and its `freq`. The existing fetch helpers cover FRED CSV, ECB SDMX-JSON, NOAA fixed-width text, Bank of Israel SDMX-JSON and the FAO monthly CSV. Keyless sources only.

## What the log is for

The watchlist tells you where to look. The log is the part that compounds.

A research project makes decisions over years, and the reasoning behind a decision is only recoverable if you wrote down what the world looked like at the time. "We sized the first-loss layer at 15% in Q3 2026 when EM spreads were wide and aid budgets were contracting" is a defensible record. "We sized it at 15%" is not — and in two years nobody, including you, will remember which it was.

Log an entry when something moves that would change a decision. Skip the rest — a log of everything is a log nobody reads.

Each entry records:

| Field |  |
| :---- | :---- |
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

## Stress scenarios

`data/macro-scenarios.csv` turns the watchlist from monitoring into something the venture can be reasoned about *under stress*. Six scenarios, each a small set of deterministic multipliers applied to the RT-5 portfolio model.

|  | Scenario | Drives |
| :---- | :---- | :---- |
| SC-0 | Base | No shock — the comparator |
| SC-1 | Rates up | Policy and long rates \+300bp |
| SC-2 | Food price shock | Staple prices spike, correlation raised to 0.45 |
| SC-3 | Energy shock | Sustained oil spike, hits both product lines |
| SC-4 | FX shock | Local currency −25% against the note currency |
| SC-5 | Combined stress | Rates, food and FX together — a coherence test |

### How a scenario transforms the model

Each row carries five levers, applied multiplicatively to the base portfolio assumptions in `risk-tools/tools/portfolio-config.csv`:

| Column | Effect |
| :---- | :---- |
| `Rate_Shock_Pp` | Added in percentage points to the senior and mezzanine coupons due |
| `Default_Multiplier` | Multiplies the baseline annual default probability |
| `Recovery_Multiplier` | Multiplies the recovery rate on defaulted principal |
| `Prepay_Multiplier` | Multiplies the annual prepayment rate |
| `Correlation_Override` | Replaces the base default correlation outright, where a shock is regional rather than idiosyncratic |

`Correlation_Override` is the one that matters. A food-price shock is not a higher independent default rate — it hits a whole region at once. SC-2 raises the default multiplier 2.2× *and* pushes correlation from 0.20 to 0.45, and it is the correlation term that drives the tail. A scenario that only raised the default rate would understate the damage and look reassuring while doing it.

### Deliberately simple

These are readable deterministic rules, not a model. A transparent multiplier that a reader can check beats a calibrated-looking transformation that nobody can audit — particularly when the underlying portfolio parameters are themselves placeholders.

They are **not forecasts** and not probability-weighted. SC-5 is not a prediction; it is a test of whether the structure survives correlated adversity, since rate-hiking cycles, commodity spikes and EM currency pressure have historically arrived together.

### Running them

python3 risk-tools/tools/simulate\_portfolio.py            \# all scenarios

python3 risk-tools/tools/simulate\_portfolio.py \--sweep    \# pool size vs fixed costs

Results land in `data/rt5-scenario-results.csv` and surface on the Risk tools tab. Every row is labelled `SYNTHETIC`. See `risk-tools/rt-5-simulator.md` for what the outputs are and are not good for.

### Adding a scenario

1. Add a row to `data/macro-scenarios.csv` with the next `SC-N`.  
2. Fill `Rationale` properly — why these multipliers, and which macro indicators justify them. A scenario without a stated rationale is a made-up number with a label.  
3. Reference the relevant `MAC-NN` IDs in `Macro_Refs` so the scenario is traceable to something observed.  
4. Re-run the simulator and rebuild the dashboard.

