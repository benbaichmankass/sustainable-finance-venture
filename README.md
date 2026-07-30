# Sustainable Finance Venture

Research and venture-building project exploring how financing and risk-management tools can unlock capital for proven, economically viable sustainable-development solutions that remain underfunded due to structural gaps (not technical ones).

**Core hypothesis:** Community-based financial structures (e.g., VSLAs) manage idiosyncratic risk well enough to support scalable lending/insurance products, and these products can be designed from origination to be standardized, verifiable, and eventually pooled into securitizable, investment-grade assets.

**Project stage:** research framing + literature review (pre-pilot).

---

## Start here

**Open `dashboard/index.html` in a browser.** It's a self-contained page — no server, no build step, no dependencies — showing project status, the full document library, the literature matrix, the milestone tracker and every tracker in this repo. Everything on it is generated from the files below, so it can't drift out of date.

Rebuild it after changing anything:

```bash
python3 dashboard/build.py
```

Working here with an AI agent? Read `CLAUDE.md` first — it holds the conventions, and `.claude/skills/` holds the procedures for recurring tasks.

## This repo is the source of truth

If it isn't in the repo, it isn't real. Google Docs and Sheets are inputs; this repo is the record. Two deliberate exceptions:

- **The Drive Vault** holds artifacts that shouldn't be in git — PDFs, personal documents, correspondence, raw data. The repo always holds the pointer. See `docs/drive-vault.md`.
- **The Master Reference Tracker Sheet** still exists for collaborator access, but it's now a mirror. If it disagrees with the repo, the repo wins.

## Structure

```
CLAUDE.md                  How to work in this repo — conventions, standards, where things go
dashboard/                 Generated status dashboard (open index.html)
docs/
  working-doc.md           Thesis, design principles, working hypotheses, PhD framing
  research-agenda.md       Literature review plan, reading lists, workflow
  milestone-plan.md        60/90-day plan narrative
  dashboard-design.md      Dashboard design decisions
  drive-vault.md           What lives in Drive instead of git, and why
literature/
  lit-matrix.csv           15 anchors (LIT-001 … LIT-015)
  notes/memo-*.md          3 synthesis memos, all Reviewed
product-design/
  business-plan.md         Current business plan, structuring assumptions, risks
data/                      Structured trackers — the dashboard reads these
  milestones.csv           M-NN    60/90-day milestones
  open-questions.csv       OQ-N    unresolved decisions
  partner-tracker.csv      PT-NN   candidate partners
  phd-programs.csv         PHD-NN  target programs
  synthesis-memos.csv      MEMO-N  memo status index
  resources.csv            RES-NN  external links and Vault folders
archive/google-drive/      Verbatim exports of superseded source docs
.claude/skills/            Task procedures for AI agents
```

Every record has a stable ID. IDs are never reused or renumbered — cross-references depend on them.

## Where things stand

| | |
|---|---|
| Literature anchors | 15, all reviewed |
| Synthesis memos | 3, all reviewed |
| Open questions | 7 — 4 partially answered, 3 open |
| Milestones | 2 done, 1 in progress, 8 not started |
| Partners | 10 tracked, 0 contacted |
| PhD programs | 9 shortlisted, 0 applications started |

**The critical path:**

1. Draft the canonical data schema (OQ-3) — blocks the underwriting engine, pilot design and ABS data tape.
2. Jurisdiction scan with counsel (OQ-1) — blocks pilot site selection. The literature has taken this as far as it can.
3. Begin partner outreach (M-03) — 10 candidates logged, none contacted. Longest-lead item.
4. Choose the first instrument — loan, insurance, or bundled.

## Related resources

- **Drive Vault:** https://drive.google.com/drive/folders/1OteXpvFVKBrk-SH1QKGYzpv50JhoHI9r
- **Master Reference Tracker (Sheet, now mirrored):** https://docs.google.com/spreadsheets/d/1Q8m8MaQ_wUzpjABRYTvIqeFTrgkDGskBJ-RGBOky2DY/edit

## Resuming a session

1. Open the dashboard for current state.
2. Check the Open Questions tab for what's undecided and why.
3. Check Partners and PhD pipeline before any new outreach — avoiding duplicate contact is the point of those trackers.
