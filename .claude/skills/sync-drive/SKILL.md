---
name: sync-drive
description: Move content between Google Drive and this repo. Use when the user says "save this doc to the repo", "make sure the repo has everything from Drive", shares a Google Doc/Sheet link, wants a PDF filed in the Vault, or asks whether the repo and Drive are in sync.
---

# Syncing Drive and the repo

The repo is the source of truth; Drive holds inputs and artifacts that shouldn't be versioned. See `docs/drive-vault.md` for the boundary.

**This skill covers manual, one-off sync** — migrating a Doc's content into the repo, filing a PDF in the Vault. A separate, automated mechanism keeps a defined set of public narrative docs continuously synced with live Drive copies in both directions, no agent involved in the reconciliation itself — see `docs/drive-sync.md`. Use that system (edit `data/drive-links.csv`), not this skill, for anything that should stay permanently mirrored rather than migrated once.

## Direction 1 — Drive content into the repo

For a Doc or Sheet whose *content* belongs in the repo:

1. **Read the whole thing** before writing anything. Sheets have multiple tabs; read them all.
2. **Archive it verbatim** at `archive/google-drive/<slug>.md` with a provenance header: source title, URL, created/modified dates, capture date, and a status line saying whether it's live, superseded, or predecessor thinking.
3. **Split the live content into its proper homes** per the table in `CLAUDE.md` §3. Trackers become CSVs in `data/`; narrative becomes markdown in `docs/`; evidence becomes matrix rows.
4. **Add a mapping table** to the archive file — "Where this content now lives" — so a reader who finds the archive knows to edit elsewhere.
5. **Note anything you had to fix** during migration (mangled cells, pasted-in stray text, inconsistent IDs) in the archive file. Silent cleanup makes later discrepancies unexplainable.
6. **Add a `data/resources.csv` row** pointing back at the original if collaborators still use it.

## Direction 2 — artifacts into the Vault

Files that shouldn't be in git — PDFs, CVs, correspondence, raw data:

1. Pick the right folder (`01-literature-pdfs` … `06-legal-and-regulatory`).
2. Name it per convention: `YYYY-MM-DD — subject — counterparty.ext`, or `LIT-0NN — short-title.pdf` for papers.
3. **Add the pointer to the repo** — a matrix `URL`, or a `data/resources.csv` row. An unreferenced Vault file is a lost Vault file.

## Permissions

- **Reading from Drive: go ahead.** Fetching a doc to summarise or file needs no check-in.
- **Writing to Drive: say what you're about to do first.** Creating folders, uploading, moving or overwriting are all visible to collaborators and some are hard to undo.
- **Never overwrite a Drive file without reading it first.**

## Checking sync status

To answer "is the repo current?":

1. List recent Drive activity in the project folders.
2. Compare against `archive/google-drive/` capture dates and `data/resources.csv`.
3. Report what's missing rather than assuming it's covered — and don't claim a doc is synced without having read it.

## Privacy boundary

Content from the Vault's `05-raw-data` never moves into the repo. Aggregate analysis results can; row-level records with personal data cannot — not in a CSV, a memo, or the dashboard.
