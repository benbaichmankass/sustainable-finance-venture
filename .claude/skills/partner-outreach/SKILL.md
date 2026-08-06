---
name: partner-outreach
description: Prepare and log outreach to partners, funders, or PhD supervisors. Use when the user asks to draft an intro email, prepare for a partner call, plan supervisor outreach, or update contact status in the partner/PhD trackers.
---

# Partner and supervisor outreach

Two trackers: `data/partner-tracker.csv` (originators, verification partners, funders, counsel) and `data/phd-programs.csv` (universities and supervisors). Both are contact records — the point is that nobody gets approached twice by accident, and that what came back is written down.

## Before drafting anything

1. **Check the tracker for prior contact.** `Contact_Status` and `Notes`. Duplicate cold approaches to the same organisation are the specific failure this tracker exists to prevent.
2. **Read what we'd be asking for.** For originators: `product-design/business-plan.md` §2 and §5. For funders: Memo 3's first-loss section. For supervisors: the PhD framing in `docs/research/working-doc.md`, plus that program's `Fit_Notes` and `Outreach_Plan`.
3. **Know the specific ask.** "Explore a partnership" wastes the first contact. "Would you be open to a 30-minute call about whether your VSLA cohort's existing MIS could support a standardized loan-level data capture pilot?" doesn't.

## Drafting

- Lead with what's in it for them, not with the venture's ambition.
- Be concrete about stage: this is pre-pilot research, not a funded programme. Overstating maturity is the fastest way to lose a serious partner.
- Cite the evidence base where it earns credibility — the literature review is a genuine asset in conversations with CGAP, J-PAL or a DFI desk.
- Keep a cold email under 200 words with one clear ask.
- **Never send anything without explicit approval.** Draft, show, wait. This applies to emails, LinkedIn messages and calendar invites alike.

## Logging

After any contact, update the tracker row in the same session:

- `Contact_Status`: `Not contacted` → `Contacted` → `In conversation` → `Committed` / `Declined`
- `Contact_Person`: name and role
- `Notes`: date, channel, what was asked, what came back, next step and when

File the actual correspondence in the Vault's `03-communications` (see `docs/ops/drive-vault.md`) — the tracker holds the summary, the Vault holds the thread.

## Follow-through

- A `Declined` row keeps its notes. Knowing who said no and why is worth as much as knowing who said yes.
- If a conversation surfaces a new constraint or opportunity, that's a row in `data/open-questions.csv` or a matrix entry — not just a line in the notes field.
- Update `data/milestones.csv` when outreach milestones (M-03, M-04, M-06, M-09) move.
- Regenerate the dashboard: `python3 dashboard/build.py`.
