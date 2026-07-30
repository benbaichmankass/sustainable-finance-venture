# Sustainable Finance Venture

Research and venture-building project exploring how financing and risk-management tools can unlock capital for proven, economically viable sustainable-development solutions that remain underfunded due to structural gaps (not technical ones).

**Core hypothesis:** Community-based financial structures (e.g., VSLAs) manage idiosyncratic risk well enough to support scalable lending/insurance products, and these products can be designed from origination to be standardized, verifiable, and eventually pooled into securitizable, investment-grade assets.

**Project stage:** research framing + literature review (pre-pilot).

---

## Start here

**Open `dashboard/index.html` in a browser.** It's a self-contained page — no server, no build step, no dependencies — showing project status, the full document library, the literature matrix, the milestone tracker and every tracker in this repo. Everything on it is generated from the files below, so it can't drift out of date.

Rebuild it after changing anything:

```bash
python3 dashboard/build.py            # local view, merges the private overlay
python3 dashboard/build.py --public   # public tier — run this before pushing
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
  publishing.md            Public/private boundary and pre-publish checklist
literature/
  lit-matrix.csv           15 anchors (LIT-001 … LIT-015)
  notes/memo-*.md          3 synthesis memos, all Reviewed
product-design/
  business-plan.md         Venture-level plan, structuring assumptions, risks
  product-lines/           One doc per product line (PL-1 community, PL-2 agrivoltaic)
data/                      Structured trackers — the dashboard reads these
  milestones.csv           M-NN    60/90-day milestones
  open-questions.csv       OQ-N    unresolved decisions
  product-lines.csv        PL-N    product lines
  partner-tracker.csv      PT-NN   candidate partners (public tier)
  phd-programs.csv         PHD-NN  target programs (public tier)
  synthesis-memos.csv      MEMO-N  memo status index
  resources.csv            RES-NN  external links
private/                   GITIGNORED private overlay — see docs/publishing.md
archive/google-drive/      Verbatim exports of superseded source docs
.claude/skills/            Task procedures for AI agents
```

Every record has a stable ID. IDs are never reused or renumbered — cross-references depend on them.

## Where things stand

| | |
|---|---|
| Literature anchors | 15, all reviewed |
| Synthesis memos | 3, all reviewed |
| Open questions | 8 — 4 partially answered, 4 open |
| Milestones | 2 done, 1 in progress, 8 not started |
| Product lines | 2 — community credit/insurance, agrivoltaic project finance |
| Partners | 10 tracked (contact status in the private overlay) |
| PhD programs | 9 shortlisted |

**The critical path:**

1. Draft the canonical data schema (OQ-3) — blocks the underwriting engine, pilot design and ABS data tape.
2. Jurisdiction scan with counsel (OQ-1) — blocks pilot site selection. The literature has taken this as far as it can.
3. Begin partner outreach (M-03) — 10 candidates logged, none contacted. Longest-lead item.
4. Choose the first instrument — loan, insurance, or bundled.

## Open by default

This repo is meant to be public. It holds the thinking, the methods, the evidence base and the tools — none of which is better for being secret. A short private tier stays out of git, and it's private because it's about **people**, not because it's commercially precious.

The test: does it name a person and say something about them? Private. Does it name an organization and explain why it's relevant? Public.

The two connect by ID at build time — `data/partner-tracker.csv` holds who a partner is and why they matter; `private/partner-contacts.csv` (gitignored) holds status and contact person. Locally you see both; a published build shows the public tier. Same pattern for research: public tooling, private inputs, publishable conclusions.

Full policy and the pre-publish checklist: `docs/publishing.md`.

## Resuming a session

1. Open the dashboard for current state.
2. Check the Open Questions tab for what's undecided and why.
3. Check Partners and PhD pipeline before any new outreach — avoiding duplicate contact is the point of those trackers.
