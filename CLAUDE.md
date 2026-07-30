# Working in this repo

This repository is the **single source of truth** for the Sustainable Finance Venture project — a research and venture-building effort on structuring community-originated financial assets (VSLA loans, microinsurance) into standardized, verifiable, poolable instruments.

Read this file before making changes. It is short on purpose.

---

## 1. The SSOT rule

**If it isn't in the repo, it isn't real.** Google Docs, Sheets, chat threads and notebooks are inputs; the repo is the record. When you learn something from an external source, write it into the repo in the same session — don't leave it in the conversation.

Two exceptions, both deliberate:

- **The Vault** (`docs/drive-vault.md`) holds artifacts that shouldn't be in git — PDFs, personal documents, correspondence, raw data. The repo always holds the *pointer* to them.
- **The Master Reference Tracker Sheet** still exists for collaborator access. It is now a *mirror*, not a source. If the Sheet and the repo disagree, the repo wins.

## 2. Repo structure

```
README.md                        Project index and status — start here
CLAUDE.md                        This file
docs/
  working-doc.md                 Main planning doc — thesis, design principles, hypotheses
  research-agenda.md             Literature review plan, reading lists, workflow
  milestone-plan.md              60/90-day plan narrative
  dashboard-design.md            Dashboard design decisions and how to extend it
  drive-vault.md                 What lives in Drive instead of git, and why
literature/
  lit-matrix.csv                 THE literature matrix — one row per source
  notes/memo-*.md                Synthesis memos
product-design/
  business-plan.md               Current business plan
data/                            Structured trackers — the dashboard reads these
  milestones.csv                 M-NN   60/90-day milestones
  open-questions.csv             OQ-N   unresolved decisions
  partner-tracker.csv            PT-NN  candidate partners
  phd-programs.csv               PHD-NN target programs
  synthesis-memos.csv            MEMO-N memo status index
  resources.csv                  RES-NN external links and Vault folders
archive/google-drive/            Verbatim exports of superseded source docs
dashboard/                       Static dashboard — see §5
.claude/skills/                  Task-specific working procedures
```

## 3. Where things go

| You have… | It goes in… |
|---|---|
| A paper, report, or evidence source | a new row in `literature/lit-matrix.csv` |
| A conclusion drawn across several sources | a synthesis memo in `literature/notes/` |
| An unresolved decision | a row in `data/open-questions.csv` |
| A person or org to talk to | a row in `data/partner-tracker.csv` |
| A dated commitment | a row in `data/milestones.csv` |
| A link worth keeping | a row in `data/resources.csv` |
| A PDF, CV, or email thread | the Vault (`docs/drive-vault.md`), then a pointer row |
| Narrative reasoning or a plan | a markdown doc in `docs/` |

**Every record gets a stable ID** (`LIT-009`, `OQ-3`, `PT-04`, `M-07`). IDs are never reused or renumbered — cross-references depend on them. When something is superseded, mark it, don't delete it.

## 4. Data file conventions

- All CSVs: **every field quoted**, header row required, UTF-8, LF line endings.
- No commas-as-decimals, no smart quotes, no em-dashes inside CSV fields (they survive but make diffs noisy).
- Cross-references go in dedicated columns (`Evidence_Refs`, `Linked_Refs`) as semicolon-separated IDs: `"LIT-009; LIT-010"`.
- Status vocabularies are fixed. Use exactly these:
  - Literature `Status`: `To read` · `Reading` · `Reviewed` · `Superseded`
  - Open question `Status`: `Open` · `Partially answered` · `Answered` · `Dropped`
  - Milestone `Status`: `Not started` · `In progress` · `Done` · `Blocked`
  - Partner `Contact_Status`: `Not contacted` · `Contacted` · `In conversation` · `Committed` · `Declined`
  - Memo `Status`: `Outline` · `Drafted` · `Reviewed`

## 5. The dashboard

`dashboard/index.html` is a static, dependency-free page. It reads `dashboard/data.js`, which is **generated** — never hand-edit it.

After changing anything in `data/`, `literature/`, `docs/` or `product-design/`:

```bash
python3 dashboard/build.py
```

Then commit both the source change and the regenerated `dashboard/data.js`. Details in `docs/dashboard-design.md`.

## 6. Research standards

This project's credibility rests on the literature matrix being trustworthy. Accordingly:

- **Never invent a citation, URL, author, year, or finding.** If you haven't read the source, say so. A row with `Status: To read` and an honest gap is worth more than a plausible-sounding summary.
- **Never state a number the source doesn't state.** If a figure is your inference, mark it as such in the text.
- **Record limitations as carefully as findings.** The `Limitations` column is not a formality — the design decisions downstream depend on knowing where the evidence is thin.
- **Distinguish "the literature says" from "we assume."** Working assumptions in `product-design/business-plan.md` carry a source column for this reason.
- Prefer open-access sources (World Bank, CGAP, J-PAL, FinDev Gateway, OECD, IFC, FSD Africa). They're citable by anyone reading this repo later.

## 7. Working style

- **Ask before committing** when the change is substantive (new literature anchors, a changed conclusion, a restructure). Mechanical changes — regenerating the dashboard, fixing a typo, adding a pointer row — don't need a check-in.
- **Small commits with real messages.** `literature: add LIT-009..LIT-015 (SPV law, ABS scale, first-loss)` beats `update files`.
- **Update the dashboard in the same commit** as the data change that requires it.
- **Don't silently narrow scope.** If part of a task is blocked, do the rest and say what you skipped.
- When a memo's conclusions change, update the memo, the `synthesis-memos.csv` row, and any open question that cited it. These three drift apart easily.

## 8. Privacy

Row-level pilot data and anything identifying a research participant lives in the Vault's `05-raw-data`, never in the repo — not in a CSV, not in a summary, not in the dashboard. Aggregate results come back; individual records don't. Partner and supervisor names in trackers are professional contacts and are fine to keep in git.
