---
name: publish-check
description: Audit the repo before making it public, enabling GitHub Pages, or sharing a dashboard screenshot. Use when the user asks "is this safe to publish", wants to flip the repo public, mentions open-sourcing, or is about to share project material externally. Also run it before any commit that touches data/, private/ or the dashboard build.
---

# Pre-publish audit

This repo is intended to be public. That only works if the private tier stays private — see `docs/ops/publishing.md` for the policy and the reasoning.

## The line, in one sentence

**Does it name a person and say something about them? Private. Does it name an organization and explain why it's relevant? Public.**

Commercial strategy is deliberately public here. The thesis isn't the moat; relationships and execution are, and those live in the Vault.

## Run these

```bash
# 1. No Drive/Sheet links outside the private overlay and the policy doc
grep -rn "drive.google.com\|docs.google.com" --include="*.md" --include="*.csv" . \
  | grep -v "^./private/" | grep -v "^./docs/ops/publishing.md"

# 2. No private columns in the public trackers
grep -l "Contact_Person\|Contact_Status\|Application_Status\|Private_Notes" data/*.csv

# 3. Nothing under private/ is tracked except the README and templates
git ls-files private/

# 4. The committed dashboard payload is the public tier.
#    Match the JSON KEY form, with the colon. A bare column name also matches
#    this very file once its text is baked into data.js, so the loose pattern
#    reports a hit against itself and the check becomes meaningless.
grep -c '"Private_Notes":' dashboard/data.js     # expect 0
git ls-files dashboard/data.private.js           # expect empty

# 5. Rebuild the public tier so it isn't stale
python3 dashboard/build.py --public
```

Each should come back empty or zero. Anything else is a finding — report it rather than silently fixing, because the fix depends on whether the content should move to `private/` or just be deleted.

## Then check by reading, not grepping

Greps catch structure. These need judgement:

- **Free-text notes fields.** `Why_This_Partner`, `Notes`, memo bodies, open-question notes. A name or a "they said" can end up in prose that no column filter catches.
- **Named individuals anywhere public.** Public academics listed with their research interests are fine — that's what a research proposal contains. The same name attached to *our* outreach status is not.
- **Raw or participant data.** Should never be in the repo at all, in any form, aggregate or otherwise, if it derives from identifiable individuals.
- **Anything under `archive/`.** Imported docs can carry contact details, pricing, or personal material that wasn't obvious when they were archived.

## Licence coverage

Apache-2.0 for code (`LICENSE`), CC BY 4.0 for writing and data (`LICENSE-CONTENT.md`), `NOTICE` for the copyright line and third-party caveat.

New files fall under one or the other by kind and need no per-file header. Two things do need a check:

- **Third-party material.** Never commit the full text of a copyrighted source — PDFs go in the Vault, and the matrix holds our summary plus a link. If you add anything authored elsewhere, flag it in `NOTICE`.
- **Vendored code or data.** Anything copied in from another project carries its own licence; record it in `NOTICE` rather than silently absorbing it.

## Git history

Flipping a repo public publishes **every commit**, not the current tree. Removing something in a new commit does not unpublish it.

If a finding is already committed, say so explicitly and offer the options: squash-merge the open PR so `main` never carries it, rewrite the branch if it's unmerged, or accept it if the exposure is genuinely trivial. Do not rewrite published history without asking.

## Before flipping the repo to public

Work the checklist in `docs/ops/publishing.md`, then confirm with the user. Changing repo visibility is theirs to do and effectively irreversible — anything public may already be cloned or indexed. Never flip it unprompted.

## Before sharing a dashboard screenshot

Check the header chip. **Private view** means the overlay is loaded and the screenshot will contain contact status and names. Rebuild with `--public` and reload before capturing anything for external use.
