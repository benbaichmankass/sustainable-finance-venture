---
name: add-literature
description: Add one or more sources to the literature matrix. Use when the user shares a paper, report, PDF or link to be logged; asks to "add this to the lit review", "find anchors for X gap", or expand the evidence base on a research axis. Covers the field-by-field standard, the ID scheme, and the no-fabrication rule.
---

# Adding a source to the literature matrix

The matrix (`literature/lit-matrix.csv`) is the project's evidence base. A weak row is worse than no row, because it will be cited later as if it were solid.

## Before you add anything

1. **Read `literature/lit-matrix.csv`** — check the source isn't already there under a different citation string. Duplicates across LIT-004/LIT-011 style overlaps are the common failure.
2. **Read `docs/research/research-agenda.md`** — the four review axes and the identified gaps. A new anchor should close a named gap, not just be interesting.
3. **Actually read the source.** Abstract, introduction, methods, limitations, conclusion at minimum. If you can only reach a landing page or an abstract, the row's `Status` is `To read` and `Key_Findings` says what you could and couldn't verify.

## The ID scheme

Sequential, never reused: the next row after `LIT-015` is `LIT-016`. If a source is later superseded, set `Status: Superseded` and note the replacement in `Open_Questions` — don't renumber.

## Filling the columns

| Column | Standard |
|---|---|
| `Axis` | One of: `1-VSLA`, `2-Microfinance`, `3-Securitization`, `4-Blended finance`, `5-Insurance`. New axes need a corresponding update to `docs/research/research-agenda.md`. |
| `Geography` | Where the *evidence* comes from, not where the publisher sits. |
| `Method` | RCT / systematic review / evaluation review / case study / legal review / policy report / survey. Be precise — this is how a reader weights the finding. |
| `Key_Findings` | What the source actually establishes. Include sample size, country and design where stated. Never a number the source doesn't state. |
| `Limitations` | Where the evidence is thin, what it doesn't cover, what has dated. Mandatory — a row with an empty limitations field hasn't been read properly. |
| `Relevance_Product` / `_Risk` / `_Impact` | `High` / `Medium` / `Low`. Relevance to *our* design decisions, not general importance. |
| `Open_Questions` | What this source makes answerable next, ideally naming an `OQ-N`. |
| `Link_Citation` | `Author/Org Year - Title`. |
| `URL` | Direct link where one exists. **Leave blank rather than guessing** — the dashboard generates a Scholar search link for blank URLs. |
| `Status` | `To read` / `Reading` / `Reviewed` / `Superseded`. |

## After adding rows

1. **Update the memo** that covers the axis (`literature/notes/memo-*.md`) — add the source to its `## Sources` list and work the finding into the body. A matrix row that no memo references is orphaned evidence.
2. **Update `data/synthesis-memos.csv`** if the memo's takeaway changed.
3. **Check `data/open-questions.csv`** — if the new source moves a question, update its `Status`, `Notes` and `Evidence_Refs`. Questions go `Open` → `Partially answered` → `Answered`; say explicitly what remains.
4. **Regenerate the dashboard**: `python3 dashboard/build.py`.
5. **Offer to file the PDF** in the Vault's `01-literature-pdfs` as `LIT-0NN — short-title.pdf` (see `docs/ops/drive-vault.md`).

## The hard rule

Never fabricate a citation, URL, author, year, sample size or finding. If a source can't be verified, the honest row — `Status: To read`, with a note on what blocked verification — is the correct output. Everything downstream in this project cites this file.
