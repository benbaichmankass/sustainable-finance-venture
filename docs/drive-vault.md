# The Drive Vault — where non-repo artifacts live

**Created:** 2026-07-30

Some project material should not live in git: copyrighted PDFs, large binaries, personal application documents, and correspondence with named individuals. Those live in a single Google Drive folder — the **Vault** — which is indexed from this repo so nothing gets lost.

**Vault root:** https://drive.google.com/drive/folders/1OteXpvFVKBrk-SH1QKGYzpv50JhoHI9r

## The rule

| Put it in the **repo** | Put it in the **Vault** |
|---|---|
| Anything you wrote: notes, memos, plans, schemas | Anything someone else wrote and holds copyright over |
| Structured trackers (CSV) | PDFs of papers and reports |
| Anything you want diffed, reviewed, or versioned | Large binaries (>5 MB), media, scans |
| Anything an AI agent needs to read to do its job | Personal documents — CVs, transcripts, application drafts |
| Public-facing text | Correspondence with named individuals |
| Links and citations | Signed documents, term sheets, legal drafts |

**The repo always holds the pointer.** A PDF in the Vault is only findable if something in the repo references it — `literature/lit-matrix.csv` for a paper, `data/resources.csv` for everything else.

## Folder structure

| Folder | Holds | Link |
|---|---|---|
| `01-literature-pdfs` | Full-text PDFs of matrix entries. Name files `LIT-0NN — short-title.pdf` so they sort alongside the matrix. | [open](https://drive.google.com/drive/folders/1xRfUEqDAyPbXgQVMhE8iPASwV6F5QHHr) |
| `02-applications-phd` | PhD applications, CVs, statements of purpose, transcripts, supervisor correspondence drafts. | [open](https://drive.google.com/drive/folders/1Qy73klJhfFCzkkygBBCXv00dtrC-OUn4) |
| `03-communications` | Partner and funder correspondence, meeting notes, call recordings/transcripts. | [open](https://drive.google.com/drive/folders/1Tuu2fAujmfgtjMElXrFsfBqqSqvASCgv) |
| `04-partner-materials` | Materials received from partners: NGO reports, MFI portfolio data summaries, pitch decks. | [open](https://drive.google.com/drive/folders/1w12EUceIKvkaWMJ-QOg82fSCllUnqvLN) |
| `05-raw-data` | Raw pilot data, exports, anything with personal data in it. **Never** commit this to the repo. | [open](https://drive.google.com/drive/folders/1cMeHmNottCBvJC5xKDJ7fC4SNTR92k7x) |
| `06-legal-and-regulatory` | Counsel memos, jurisdiction scans, draft term sheets, regulatory filings. | [open](https://drive.google.com/drive/folders/1dKCr1UEm4aLpzfDsW5ij06dQapePxCyy) |

## Naming convention

`YYYY-MM-DD — <subject> — <source or counterparty>.<ext>`

For literature, prefix with the matrix ID instead: `LIT-011 — FSD Africa securitisation Africa.pdf`.

## Working with an AI agent

An agent with Drive access can read from the Vault and write back to it. Two standing rules:

1. **Read freely, write deliberately.** Fetching a paper from `01-literature-pdfs` to summarise it needs no permission. Adding, moving or overwriting a file does — say what you are about to do first.
2. **Personal data stays in `05-raw-data`.** Never copy its contents into the repo, into a summary that will be committed, or into a dashboard. If a pilot dataset needs analysis, the aggregate result comes back to the repo; the row-level data does not.

## Anything with personal data

`05-raw-data` is the only place row-level pilot data belongs. Before any of it is collected, the pilot design doc needs to state the consent basis, the retention period, and who has access — that work is tracked as M-08.
