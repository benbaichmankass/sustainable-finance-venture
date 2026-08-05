# Dashboard — design plan

**Status:** v1 implemented · **Last updated:** 2026-08-04

## The problem

Project state was spread across a Google Sheet, several Google Docs, a repo, and conversation history. Answering "what's the current status of X" meant checking three places and hoping they agreed. The dashboard exists so there is one place to look — and, more importantly, so that place can't drift from the underlying record.

## The core decision: generated, not authored

The dashboard has **no state of its own**. Every number, row and document on it is read out of the repo's source files at build time. You cannot update the dashboard directly; you update the CSV or the markdown and rebuild.

This is the whole design. It means:

- The dashboard can never disagree with the repo — the failure mode that made the Sheet unreliable.
- Status changes happen in one place, in a diffable file, under version control.
- Anyone can reconstruct the dashboard from the repo alone. No database, no hosted service, nothing to expire.

The cost is a build step. It's a 200-line Python script with no dependencies, which seemed a fair trade.

## Architecture

```
data/*.csv  ─┐
literature/  ├─→  dashboard/build.py  ─→  dashboard/data.js  ─→  dashboard/index.html
docs/*.md    │                                                    (opened in a browser)
product-design/
archive/     ─┘
```

- **`build.py`** — Python 3 stdlib only. Reads seven CSVs and every markdown file in the tracked directories, and emits a single JSON blob assigned to `window.SFV_DATA`.
- **`data.js`** — generated, committed, never hand-edited. Committing it means the dashboard works from a fresh clone with no build step for a reader.
- **`index.html`** — one self-contained file: CSS, a small markdown renderer, and the view code. No npm, no bundler, no CDN.

### Why no framework

The whole point is longevity. This project will be picked up intermittently over years. A React build with pinned dependencies would be unbuildable in three years; a single HTML file opened with `file://` will not be.

## Tabs

| Tab | Answers |
|---|---|
| **Overview** | Where does the project stand, and what's next? KPI tiles, milestone and question status, evidence base by axis, and the current critical path. |
| **Library** | Where's that thing I wrote? Every markdown document in the repo, in full, rendered inline. Search runs over complete document text, not just titles. Each document also has one-click download as Markdown, DOCX or PDF (see "Document export" below). |
| **Research plan** | What does the evidence say? The full literature matrix with per-source findings, limitations, relevance ratings and links, plus the synthesis memos built on it. |
| **Business plan** | What are we building, and are we on schedule? The plan itself plus the 60/90-day milestone tracker broken out by phase. |
| **Open questions** | What can't we decide yet? Each question's status, what the evidence establishes, and explicitly what remains. |
| **Partners** | Who have we approached? Contact status across originators, funders, verification partners and counsel. |
| **PhD pipeline** | Where are the applications? Programs, supervisors, fit notes and next steps. |
| **Resources** | Where's everything else? External libraries, the Master Tracker Sheet, and the Drive vault folders. |

## Navigation

The tab list is a **left sidebar**, not a top bar — with 13 tabs a horizontal strip was starting to require scrolling to find the later ones, and a sidebar scales to more tabs without that. It sticks just below the header (`--header-h`, measured from the header's real rendered height in JS since the header wraps at some widths — see `syncHeaderHeight()`), with its own scroll region so a long tab list never pushes the page taller than the viewport.

Below 900px wide, the sidebar becomes a **slide-in drawer** instead of staying on-screen: off-canvas by default, opened by a hamburger button in the header (`#nav-toggle`, itself hidden above 900px), dismissed by tapping the backdrop, picking a tab, pressing Escape, or resizing back past the breakpoint. This was a horizontal scrolling tab bar in an earlier version, but that doesn't scale any better than the old top bar did once there are enough tabs to require scrolling to find one — a drawer keeps the same full vertical list mobile gets on desktop, just off-screen until asked for.

## Document export

Every document in the Library can be downloaded as Markdown, DOCX or PDF, generated **client-side, on click, with no server and no external library** — consistent with the "no framework" decision above. MD is just the document's own source text. DOCX and PDF share a plain-text block parser (`mdToBlocks`) that walks the same markdown grammar as the inline renderer but emits plain text instead of HTML. From there:

- **DOCX** is built as a minimal but spec-valid OPC package — `[Content_Types].xml`, `_rels/.rels`, `word/document.xml` — zipped with a hand-rolled STORE-only writer (no DEFLATE implementation needed for a handful of small XML parts).
- **PDF** is assembled object-by-object (catalog, pages, four Base-14 fonts, one content stream per page) with a hand-rolled writer that computes its own xref table. Word-wrap uses the standard Helvetica AFM width metrics rather than a guess, and text is restricted to Latin-1/WinAnsi before layout, since the writer emits single-byte string literals rather than carrying a Unicode CMap.

Both are deliberately plain — headings and emphasis carry through, tables collapse to pipe-separated text, but there is no attempt to reproduce the dashboard's visual styling. The goal is a portable, readable copy of the document, not a design export.

## Visual design rules

The dashboard follows the data-visualisation conventions the project uses everywhere:

- **Colour is assigned by identity, never by rank.** Filtering the literature matrix doesn't repaint the rows that survive.
- **Magnitude comparisons use one hue** (the blue ramp), not a categorical rainbow. The "sources by axis" bars compare quantities, so they're a sequential encoding.
- **Status colour never carries meaning alone.** Every status pill shows a coloured dot *and* its text label — required for colourblind readers, and it also survives being printed.
- **Both colour schemes are designed, not flipped.** Dark mode uses its own colour steps chosen against the dark surface. The page follows the OS setting; the in-page toggle overrides it in both directions.
- **Wide content scrolls inside its own container.** The page body never scrolls horizontally.
- **Recessive chrome.** Hairline borders, muted axis text, no shadows or gradients competing with content.

## Extending it

Adding a tracker:

1. Add the CSV to `data/` following the conventions in `CLAUDE.md` §4.
2. Register it in `build.py`'s `TABLES` dict.
3. Add a `TABS` entry and a `render*()` function in `index.html`.
4. Rebuild, open, check both colour schemes.

The `buildTable(rows, cols, detailFn)` helper handles the common case — a compact table with expandable detail rows. Most trackers need nothing more than a column config.

**Columns are click-to-sort.** Any column with a `key`, `sortKey`, or `sortVal(row)` sorts on click (first click ascending, second descending); blanks always fall to the bottom and comparison is numeric-aware, so `PHD-2` precedes `PHD-10` and tier `1` precedes `2`. A render-only column (one drawing a pill or link with no underlying field) becomes sortable by giving it a `sortKey` — e.g. the PhD "Fit" column renders a tier pill but sorts on `Tier`. Sorting and row-expansion run off one delegated listener, so a sort re-renders in place without re-wiring. Pass `{sortIdx, sortDir}` in `opts` to set a default sort.

## Deliberately not built

- **No hosting.** Open the file locally. If it's ever wanted on the web, GitHub Pages would serve `dashboard/` as-is, but the repo is private and the content includes partner names — that's a decision to make explicitly, not to drift into.
- **No editing from the browser.** Writes would need a backend, and the repo would stop being the source of truth.
- **No live Drive/Sheet reads.** They'd break the offline-from-a-clone property, and they'd reintroduce the drift problem the whole design exists to solve. Sync is a deliberate act — see the `sync-drive` skill.
- **No time-series charts yet.** There's no time-series data. When pilot data exists, that's the moment to add them.
