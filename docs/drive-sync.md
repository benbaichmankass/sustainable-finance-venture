# Drive sync — bidirectional, automated, repo stays the source of truth

**Status:** v1 — narrative docs only · **Last updated:** 2026-08-05

## What this is, and what it isn't

The **Drive Vault** (`docs/drive-vault.md`) holds artifacts that don't belong in git at all — PDFs, correspondence, personal documents. This is a different thing: a set of repo documents that also have a live, editable copy in Google Drive, kept in sync automatically in both directions. Vault content is private and one-way (Direction 2 in the `sync-drive` skill). Workfolder content is public and bidirectional. Don't conflate the two folders.

The point is to let editing happen wherever's convenient — the repo directly, or a Google Doc on a phone on a train — without the repo ever losing its status as the record. That works because of one rule:

**Reconciliation is mechanical, not editorial.** A script compares hashes against the last-synced baseline and moves content in whichever direction actually changed. There is no model in this loop and no judgment call about which version is "better" — if both sides changed since the last sync, the script does not guess; it stops and flags it for a human.

## Architecture

```
data/drive-links.csv  ── manifest: one row per synced item ─┐
                                                              │
scripts/sync_drive.py ── the reconciliation engine ──────────┤
  (service-account auth, hash comparison, pull/push/conflict) │
                                                              │
.github/workflows/sync-drive.yml ── runs it on a timer ──────┘
  (every ~15 min + manual dispatch, commits straight to main)

dashboard/build.py reads data/drive-links.csv like any other tracker ─→
  Resources tab: master folder link + every item, each linking out to
  its Drive copy and its repo file.
```

Nothing here talks to Claude. The workflow, the script, and the credential all live in this repo and GitHub's infrastructure; an AI agent might *write* the manifest row for a new doc, same as any other repo edit, but the reconciliation itself runs unattended.

## The manifest — `data/drive-links.csv`

One row per synced item, plus one `folder`-type row for the master Drive folder itself (used only for navigation, never reconciled).

| Column | Meaning |
|---|---|
| `ID` | Stable ID, `DRV-NN`. Never reused, same rule as every other tracker. |
| `Drive_ID` | The Drive file/folder ID. Blank means "not created yet" — the next sync run creates it from the repo file. |
| `Repo_Path` | The repo file this row reconciles with. Blank for the folder row. |
| `Type` | `folder` (navigation only) · `doc` (Google Doc ↔ markdown) · `sheet` (Google Sheet ↔ CSV). |
| `Parent_ID` | The `ID` of the folder row a new file gets created inside. |
| `Title` | Display title — also the Doc/Sheet's name when it's first created. |
| `Category` | Groups items in the dashboard (`Planning`, `Synthesis memos`, `Product & business`, `Risk tools`). |
| `Baseline_Drive_Hash` / `Baseline_Repo_Hash` | SHA-256 of each side's content **as of the last successful sync**. This is what makes three-way comparison possible — see below. |
| `Last_Synced_At` | UTC timestamp of the last successful reconciliation. |
| `Status` | `Not synced` · `Synced` · `Conflict` · `Error`. |

## The reconciliation algorithm

Every run, for every non-folder row, the script computes the current hash of both sides and compares each against its stored baseline — not against each other directly:

| Drive vs. baseline | Repo vs. baseline | Result |
|---|---|---|
| unchanged | unchanged | nothing to do |
| changed | unchanged | **pull** — Drive was edited, overwrite the repo file |
| unchanged | changed | **push** — the repo was edited, overwrite the Drive file |
| changed | changed, but Drive now equals repo | not a real conflict — both sides independently landed on the same content; just re-baseline |
| changed | changed, and they disagree | **conflict** — open a GitHub issue, touch neither side, wait for a human |
| — (`Drive_ID` blank) | — | **create** — make a new Doc/Sheet under the parent folder from the current repo content, then baseline both sides to the post-creation export (Drive's own text, not the pre-upload source — a markdown → Google Doc → markdown round-trip isn't always byte-identical, and baselining to what Drive actually has avoids a spurious "changed" on the very next run) |

Why compare against a stored baseline instead of just "whichever timestamp is newer": a bare timestamp race can silently discard an edit — two people (or a person and an automated commit) touching both sides within the same 15-minute window, and whichever wrote last wins with no record of what was lost. The baseline comparison instead *detects* that both sides moved and refuses to pick a winner. See `scripts/sync_drive.py`'s `reconcile_row()` for the actual implementation — it's about 40 lines, worth reading before changing the merge rules.

## Resolving a conflict

The issue the script opens links both the Drive doc and the repo file, and says how to close it out: **edit one side to match the other, or merge by hand so both agree**, then let the next scheduled run pick it up — it re-baselines automatically once the two sides actually agree. The issue itself doesn't auto-close; close it once you've confirmed the next run synced cleanly.

## Auto-commit, not auto-merge

Reconciled changes are committed straight to `main` by the workflow — no PR, no review gate, for either direction. That's deliberately different from how a normal content change to this repo works (see `CLAUDE.md` §7, "ask before committing when the change is substantive"). It's safe here specifically because:

- The only things a sync run can touch are the markdown docs and Sheets explicitly listed in the manifest — nothing structural, nothing with an ID scheme to corrupt.
- Every commit is a plain content diff, fully revertable with `git revert`.
- The conflict path is the actual safety valve: anything ambiguous stops and asks, rather than getting silently auto-committed.

If a CSV tracker (one with the ID/status-vocabulary invariants) is ever added as a `sheet` row, that calculus changes — a bad Sheet paste can break those invariants in a way a markdown edit can't. Don't add a `data/*.csv` tracker to the manifest without adding a schema-validation step to the script first; right now it will accept anything a Sheet contains and write it straight to the CSV.

## Adding a new synced document

1. Add a row to `data/drive-links.csv`: a fresh `DRV-NN` ID, `Repo_Path` set, `Drive_ID` blank, `Parent_ID` set to the folder row's ID, `Type` set, `Status` set to `Not synced`.
2. Either wait for the next scheduled run, or trigger the workflow manually (Actions tab → Drive sync → Run workflow).
3. The row fills itself in — `Drive_ID`, both baseline hashes, `Last_Synced_At`, `Status: Synced`.

## Cadence and its tradeoff

The workflow polls every ~15 minutes rather than reacting to a Drive push notification. A true push (Drive API `watch` channels) would mean near-instant reconciliation, but it needs a permanently hosted webhook receiver and a subscription that expires and must be renewed at least every 24 hours — a second piece of infrastructure with its own upkeep. Fifteen-minute polling gets nearly all the same practical benefit (nobody is watching a doc update in real time) at zero hosting cost and nothing to renew. If that latency ever actually matters, revisiting this is a self-contained change — it doesn't require touching the reconciliation logic, only the trigger.

## One-time setup (already done for this repo)

1. A Google Cloud project with the Drive API (and Sheets API, for the `sheet` path) enabled — no billing account required.
2. A service account (`sfv-drive-sync-bot@sustainable-finance-venture.iam.gserviceaccount.com`) with a JSON key.
3. That service account invited as **Editor** on the master Drive folder — this is what actually grants access; the key alone gets nowhere without it.
4. The key stored as the `GDRIVE_SA_KEY` GitHub Actions secret on this repo.
5. Repo Settings → Actions → General → Workflow permissions set to **Read and write permissions**, so the workflow's `GITHUB_TOKEN` can push to `main` and open issues.

Setting this up again from scratch (a new project, a rotated key) is the same five steps.
