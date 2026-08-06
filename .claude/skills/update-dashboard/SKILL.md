---
name: update-dashboard
description: Regenerate or extend the project dashboard. Use after changing anything in data/, literature/, docs/ or product-design/; when the user asks to "update the dashboard", add a tab, add a chart, or reports that the dashboard is showing stale content.
---

# Working on the dashboard

`dashboard/index.html` is a single, dependency-free static page. `dashboard/data.js` is **generated** — editing it by hand is always wrong, because the next build silently discards the edit.

## Regenerating

```bash
python3 dashboard/build.py
```

Runs on Python 3 stdlib only, no install step. It reads `data/*.csv`, `literature/lit-matrix.csv`, and the full text of every markdown file in `docs/`, `literature/notes/`, `product-design/` and `archive/`, then writes `dashboard/data.js`.

Commit the regenerated `data.js` alongside the source change. A commit that changes a CSV without the rebuilt `data.js` leaves the dashboard lying.

## Viewing it

Open `dashboard/index.html` directly in a browser — it works from `file://`, no server needed.

## Adding a new tracker

1. Add the CSV to `data/` following the conventions in `CLAUDE.md` §4.
2. Register it in `build.py`'s `TABLES` list.
3. Add a tab entry in `index.html`'s `TABS` array with its render config.
4. Rebuild and open the page to check it.

## Adding a new document

Markdown files under the indexed directories are picked up automatically, but a new one still needs a home in the Library's tree:

1. Put the file in the right `docs/` subfolder — `research/`, `phd/`, `venture/` or `ops/`. Never loose in `docs/`.
2. If no existing `DOC_TREE` prefix in `build.py` already covers it, add one. Rows are `(path prefix, group, section)`, first match wins, and list order is render order.
3. Rebuild. **Check stderr** — a document matching no prefix is reported there and shows up on the page under `Unfiled / Needs a home`. That's the taxonomy telling you it has a gap, not a cosmetic warning.
4. If it belongs to a numbered family (RT, MEMO, PL), add it to `DOC_FAMILY` so it renders with its ID chip and sorts in sequence.

Full reasoning in `docs/ops/dashboard-design.md`, "How the Library is organised".

## Design constraints

Documented in `docs/ops/dashboard-design.md`. The ones that are easy to break:

- **No external requests.** No CDN scripts, no web fonts, no remote images. Everything inline.
- **No build toolchain.** No npm, no bundler. A contributor with Python and a browser must be able to run this in five years.
- **Both colour schemes.** The page follows the OS setting and the in-page toggle; check any new colour in both.
- **Palette slots are fixed.** Colours are assigned by identity, never cycled by rank — a filter that changes the row count must not repaint the categories. Use the CSS custom properties already defined; don't introduce new hues.
- **Tables scroll inside their own container.** The page body must never scroll horizontally.

## After changing content

If the change alters project *status* — a milestone completed, an open question answered, a memo reviewed — update the source CSV rather than the dashboard. The dashboard has no state of its own, which is the point.
