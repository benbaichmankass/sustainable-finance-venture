# The Drive Vault — where non-repo artifacts live

**Created:** 2026-07-30

Some project material should not live in git: copyrighted PDFs, large binaries, personal application documents, and correspondence with named individuals. Those live in a single Google Drive folder — the **Vault** — which is indexed from this repo so nothing gets lost.

This matters more than it would in a private repo, because **this repo is intended to be public** — see `docs/publishing.md`. The Vault is the private half of the system.

**Vault links live in `private/pointers.csv`**, which is gitignored. They're deliberately not in this file: publishing a folder ID invites access requests and serves no purpose.

**Not to be confused with the Drive workfolder.** A separate Drive folder holds live, editable copies of this repo's *public* narrative docs, synced automatically in both directions — see `docs/drive-sync.md`. That folder's link is public on purpose (it's linked from the dashboard); this Vault's is not. Same underlying platform, opposite privacy posture — don't point one skill's logic at the other's folder.

## The rule

| Put it in the **repo** | Put it in the **Vault** |
|---|---|
| Anything you wrote: notes, memos, plans, schemas | Anything someone else wrote and holds copyright over |
| Structured trackers (CSV) | PDFs of papers and reports |
| Anything you want diffed, reviewed, or versioned | Large binaries (>5 MB), media, scans |
| Anything an AI agent needs to read to do its job | Personal documents — CVs, transcripts, application drafts |
| Public-facing text | Correspondence with named individuals |
| Links and citations | Signed documents, term sheets, legal drafts |

**The repo always holds the pointer.** A PDF in the Vault is only findable if something in the repo references it — `literature/lit-matrix.csv` for a paper, `data/resources.csv` for everything else. Where the pointer would itself be a private link, it goes in `private/pointers.csv`.

**How research actually works across the boundary.** The tooling is public and the inputs are private: the schema, analysis code and methodology live in the repo, you point them at a dataset in `05-raw-data`, and the aggregate result comes back into the repo. Nothing about the boundary prevents doing the work — it just decides where each piece rests.

## Folder structure

| Folder | Holds |
|---|---|
| `00-private-overlay` | Canonical copies of the gitignored CSVs in `private/` — contact status, application status, Vault pointers. Download these into `private/` when setting up on a new machine. |
| `01-literature-pdfs` | Full-text PDFs of matrix entries. Name files `LIT-0NN — short-title.pdf` so they sort alongside the matrix. |
| `02-applications-phd` | PhD applications, CVs, statements of purpose, transcripts, supervisor correspondence drafts. |
| `03-communications` | Partner and funder correspondence, meeting notes, call recordings/transcripts. |
| `04-partner-materials` | Materials received from partners: NGO reports, MFI portfolio data summaries, pitch decks. |
| `05-raw-data` | Raw pilot data, exports, anything with personal data in it. **Never** commit this to the repo. |
| `06-legal-and-regulatory` | Counsel memos, jurisdiction scans, draft term sheets, regulatory filings. |

Links in `private/pointers.csv`.

## Naming convention

`YYYY-MM-DD — <subject> — <source or counterparty>.<ext>`

For literature, prefix with the matrix ID instead: `LIT-011 — FSD Africa securitisation Africa.pdf`.

## Working with an AI agent

An agent with Drive access can read from the Vault and write back to it. Two standing rules:

1. **Read freely, write deliberately.** Fetching a paper from `01-literature-pdfs` to summarise it needs no permission. Adding, moving or overwriting a file does — say what you are about to do first.
2. **Personal data stays in `05-raw-data`.** Never copy its contents into the repo, into a summary that will be committed, or into a dashboard. If a pilot dataset needs analysis, the aggregate result comes back to the repo; the row-level data does not.

## Anything with personal data

`05-raw-data` is the only place row-level pilot data belongs. Before any of it is collected, the pilot design doc needs to state the consent basis, the retention period, and who has access — that work is tracked as M-08.
