# Drive sync — bidirectional, automated, repo stays the source of truth

**Status:** v1 — narrative docs only · **Last updated:** 2026-08-05

## What this is, and what it isn't

The **Drive Vault** (`docs/ops/drive-vault.md`) holds artifacts that don't belong in git at all — PDFs, correspondence, personal documents. This is a different thing: a set of repo documents that also have a live, editable copy in Google Drive, kept in sync automatically in both directions. Vault content is private and one-way (Direction 2 in the `sync-drive` skill). Workfolder content is public and bidirectional. Don't conflate the two folders.

The point is to let editing happen wherever's convenient — the repo directly, or a Google Doc on a phone on a train — without the repo ever losing its status as the record. That works because of one rule:

**Reconciliation is mechanical, not editorial.** A script compares hashes against the last-synced baseline and moves content in whichever direction actually changed. There is no model in this loop and no judgment call about which version is "better" — if both sides changed since the last sync, the script does not guess; it stops and flags it for a human.

## Architecture

```
data/drive-links.csv  ── manifest: one row per synced item ─┐
                                                              │
scripts/sync_drive.py ── the reconciliation engine ──────────┤
  (service-account auth, hash comparison, pull/push/conflict) │
                                                              │
.github/workflows/sync-drive.yml ── runs it ─────────────────┘
  (on push to a synced path + hourly poll + manual dispatch;
   commits straight to main. See "Cadence" - the poll is
   best-effort and routinely much slower than hourly.)

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

Why compare against a stored baseline instead of just "whichever timestamp is newer": a bare timestamp race can silently discard an edit — two people (or a person and an automated commit) touching both sides within the same polling window — and that window is hours wide, not minutes, so the odds of it happening are not academic — with whichever wrote last winning and no record of what was lost. The baseline comparison instead *detects* that both sides moved and refuses to pick a winner. See `scripts/sync_drive.py`'s `reconcile_row()` for the actual implementation — it's about 40 lines, worth reading before changing the merge rules.

## Resolving a conflict

The issue the script opens links both the Drive doc and the repo file, and says how to close it out: **edit one side to match the other, or merge by hand so both agree**, then let the next scheduled run pick it up — but first check the conflict is really about *content*. If the repo file carries a BOM or CRLF endings, the mismatch may be structural rather than editorial, in which case no amount of editing either side will clear it; see the normalisation rule above — it re-baselines automatically once the two sides actually agree. The issue itself doesn't auto-close; close it once you've confirmed the next run synced cleanly.

## Auto-commit, not auto-merge

Reconciled changes are committed straight to `main` by the workflow — no PR, no review gate, for either direction. That's deliberately different from how a normal content change to this repo works (see `CLAUDE.md` §7, "ask before committing when the change is substantive"). It's safe here specifically because:

- The only things a sync run can touch are the markdown docs and Sheets explicitly listed in the manifest — nothing structural, nothing with an ID scheme to corrupt.
- Every commit is a plain content diff, fully revertable with `git revert`.
- The conflict path is the actual safety valve: anything ambiguous stops and asks, rather than getting silently auto-committed.

If a CSV tracker (one with the ID/status-vocabulary invariants) is ever added as a `sheet` row, that calculus changes — a bad Sheet paste can break those invariants in a way a markdown edit can't. Don't add a `data/*.csv` tracker to the manifest without adding a schema-validation step to the script first; right now it will accept anything a Sheet contains and write it straight to the CSV.

## Text is normalised at both ends, and markdown export never degrades

Two rules the engine enforces on every byte crossing the boundary. Both were added on
2026-08-22 after one document was silently corrupted and then wedged for a day.

**1. Normalise before hashing and before writing.** A UTF-8 BOM is stripped and CRLF/CR
is folded to LF, in `read_repo_file()`, `export_doc_text()` and `write_repo_file()`.

This is not tidiness. `write_repo_file()` opens with `newline="\n"`, which does *not*
strip a `\r` already inside the string, while `read_repo_file()` opens with universal
newlines, which does. So a CRLF-bearing export written to disk and read back is a
**different string** — its hash can never match the baseline recorded at write time, and
`repo_changed` is therefore `True` on every run, for ever. The row cannot converge, and
because the documented "edit one side to match the other" fix operates on *content*, it
cannot clear a mismatch that is structural. Normalising both ends is what makes the
round-trip stable.

**2. A Doc that will not export as markdown is an error, not a plain-text pull.**
`export_doc_text()` used to fall back to `text/plain` on any `HttpError`. That looks
defensive and is the opposite: Google's plain-text export drops every heading marker,
every bold marker and every table pipe, and adds a BOM and CRLF endings. A transient API
error on one run would therefore overwrite a good markdown file with a formatting-stripped
rendering, commit it to `main`, and report success.

It now raises `MarkdownExportUnavailable`; `main()` catches it, marks the row `Error` and
moves on. Losing a cycle on one document beats losing the document.

### The incident these came from

`DRV-11` (`docs/phd/phd-scoring-rubric.md`), 2026-08-21T07:13Z. The markdown export
failed, the fallback pulled plain text, and the repo copy lost 8 headings, 4 tables and
all bold, gaining 212 tab characters, a BOM and CRLF endings. Both baselines were then
set to that degraded text, so the corruption became the recorded truth. From the next run
onward the repo hash could never match its baseline, Drive was exporting proper markdown
again, both sides read as changed, they disagreed — permanent `Conflict`.

Recovering it needed the normalisation fix *plus* a deliberate re-baseline of both hashes
to the normalised repo hash, which makes the engine see repo-unchanged / Drive-changed and
take the pull branch. Note that re-baselining this way needs only a locally computable
value — it is the one manoeuvre that does not require predicting Drive's export hash.

Regression cover: `scripts/test_sync_drive.py` (stdlib only, no Drive credentials needed).

## Known constraint: the service account can't create new files

A standalone Google service account — one not backed by a Google Workspace organization with a **Shared Drive** — has **zero Drive storage quota of its own**. Editing a file it doesn't own costs it nothing (the file's storage counts against whoever owns it), but *creating* a new file makes the service account the owner by default, and Google rejects that with `storageQuotaExceeded` even though it has full Editor access to the folder. This isn't a permissions bug; it surfaced on the very first live run of this system (every one of the 32 initial docs failed to create, cleanly, with that exact error, while everything else — auth, the commit, the push — worked).

Shared Drives fix this properly (files there are owned by the Shared Drive, not any one account), but Shared Drives are a Workspace-only feature, unavailable on a plain Google account. So for a plain account, the practical rule is:

**New files must be created by a real account with its own quota, then the service account only ever edits what already exists.** The initial 32 docs were seeded this way (via an authenticated Drive connection to the folder owner's real account) rather than through the automated workflow.

## The manifest is the whole world — nothing is auto-discovered

The script iterates over the rows in `data/drive-links.csv` and nothing else. It never lists the workfolder's contents, so:

- **A Doc you create by hand in the Drive workfolder will not appear in the repo.** It sits there, unseen, until someone adds a `DRV-NN` row pointing at it. There is no scan step that would notice it.
- **A markdown file you add to the repo will not appear in Drive**, for the same reason.

Sync is bidirectional *per registered pair*, not per folder. Registration is the manual half, and it's manual on purpose — it's what keeps an arbitrary Drive upload from landing in a public repo without anyone deciding it should.

## Adding a new synced document

Because of the quota constraint above, adding a new synced doc is a three-step:

1. **Create the Doc first, from an account with storage quota** — directly in Drive (File → New → Google Doc, inside the workfolder), or via an agent holding a real Drive connection rather than the service-account key. Note the file ID from its URL (`docs.google.com/document/d/<ID>/edit`). Seed it with the repo file's content in the same move, so the two sides start out saying the same thing.
2. **Baseline both sides before the first run.** Add the row with `Drive_ID` filled in, a fresh `DRV-NN`, `Repo_Path`, `Parent_ID` pointing at the folder row, `Type`, and — this is the part that matters — **both baseline hashes already populated**, `Status: Synced`.

   Leaving the baselines blank does *not* produce a clean first sync. Blank baselines make both sides read as changed, and since a markdown → Google Doc → markdown round-trip is never quite byte-identical, the two hashes won't match either — which is precisely the conflict signature. The very first scheduled run would open a conflict issue on a document nobody had edited yet.

   So compute them by hand: `Baseline_Repo_Hash` is the SHA-256 of the repo file's bytes; `Baseline_Drive_Hash` is the SHA-256 of the Doc **exported as `text/markdown`** — Drive's own rendering, not the content you uploaded. Getting one slightly wrong is survivable (the next run just pulls or pushes, and re-baselines itself); leaving both blank is the case that actually jams.
3. **Trigger the workflow** (scheduled, or Actions tab → Drive sync → Run workflow) and confirm the row comes back clean. With correct baselines this run is a no-op, which is the point — the row is already reconciled and the automation takes over from there.

Leaving `Drive_ID` blank and letting the workflow create the file will fail with the quota error above unless the service account has since been moved to a Workspace Shared Drive. The `create` branch in `reconcile_row()` is still correct code — it just can't run on this account.

## Cadence — and why the two directions are not symmetric

The two directions have different trigger mechanics, and conflating them is what produced the wrong latency figure this section used to quote.

**Repo → Drive is push-triggered and effectively immediate.** A commit to `main` touching `docs/`, `literature/notes/`, `product-design/`, `risk-tools/` or the manifest runs the workflow directly. No scheduler involved, so no scheduler to be let down by. (The job's own commit can't loop back: pushes authenticated with `GITHUB_TOKEN` don't retrigger workflows.)

**Drive → repo has to be polled**, because there's no signal to react to. A true push (Drive API `watch` channels) would mean near-instant reconciliation, but it needs a permanently hosted webhook receiver and a subscription that expires and must be renewed at least every 24 hours — a second piece of infrastructure with its own upkeep, to speed up the direction that's used less. Not worth it yet.

### What the cron actually delivers

The poll is **hourly**, and that number is deliberately modest, because a more aggressive one was measured and found to be fiction. The schedule used to read `7,22,37,52 * * * *` — four times an hour. Measured over 18.7 hours on 2026-08-06:

| | |
|---|---|
| Scheduled runs in the window | 74 |
| Runs that actually fired | 10 |
| **Dropped** | **87%** |
| Claimed gap | 15 min |
| Observed gap | 60–205 min, mean 124 |

The runs that did fire didn't land on the cron minutes either. This is documented GitHub behaviour, not a repo bug: `schedule` is best-effort, it's deprioritised under load, and high-frequency crons are dropped hardest. Asking for four runs an hour bought nothing but scheduler pressure and a latency figure in this document that was never true.

So: **assume up to a couple of hours for a Drive-side edit to reach the repo**, and don't design anything around a tighter bound. If you need it now, run the workflow by hand — Actions tab → Drive sync → Run workflow. A repo-side edit, by contrast, syncs on the push.

### When Actions is down

Both triggers are dead during a GitHub Actions outage, and a run queued when the incident starts may be cancelled rather than eventually run. Nothing is lost when this happens — reconciliation is a pure function of current state against the stored baselines, so a skipped run is simply caught by the next one. Check <https://www.githubstatus.com> before debugging a sync that appears stuck; on 2026-08-06 an Actions/Pages major outage from 15:22Z stalled both this workflow and the Pages deploy for hours, and it looked exactly like a broken workflow from inside the repo.

## One-time setup (already done for this repo)

1. A Google Cloud project with the Drive API (and Sheets API, for the `sheet` path) enabled — no billing account required.
2. A service account (`sfv-drive-sync-bot@sustainable-finance-venture.iam.gserviceaccount.com`) with a JSON key.
3. That service account invited as **Editor** on the master Drive folder — this is what actually grants access; the key alone gets nowhere without it.
4. The key stored as the `GDRIVE_SA_KEY` GitHub Actions secret on this repo.
5. Repo Settings → Actions → General → Workflow permissions set to **Read and write permissions**, so the workflow's `GITHUB_TOKEN` can push to `main` and open issues.

Setting this up again from scratch (a new project, a rotated key) is the same five steps.
