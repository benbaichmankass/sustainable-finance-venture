# Publishing — what's public, what's private, and how the two connect

**Status:** policy in force; repo not yet flipped to public · **Last updated:** 2026-07-30

## The posture

This project is **open by default**. The repo holds the thinking, the methods, the evidence base and the tools — and there is no good reason for any of that to be secret. Community finance and blended finance are fields that advance by people publishing what they learned; a literature matrix and a data schema are more valuable shared than hoarded.

What stays private is a short list, and it's private for one reason: **it's about people.** Not because it's commercially precious.

## The line

| Public repo | Private Vault |
|---|---|
| Methods, schemas, code, models | Raw and row-level data, anything identifying a research participant |
| The literature matrix and memos | Copyrighted PDFs of the sources |
| Research agenda, working doc, business plan | Signed documents, term sheets, priced offers |
| Product-line specs and structuring logic | Named individuals and what they said |
| Open questions and reasoning | Relationship status — who was approached, who declined, who's warm |
| Organizations as research targets, and why | Personal documents — CVs, transcripts, applications |
| Milestones and progress | Correspondence threads |
| Aggregate findings | Vault links themselves |

**The test:** does it name a person and say something about them? Then it's private. Does it name an organization as a candidate partner and explain the reasoning? That's a research observation, and it's public.

"CARE's VSLA network is the largest established methodology network and a candidate origination partner" — public.
"Spoke to [name] on 12 March, lukewarm on the data standard, revisit after pilot" — private.

Commercial strategy is deliberately on the public side. The thesis isn't a secret worth keeping; execution and relationships are the moat, and those are exactly what stays in the Vault.

## How they connect

This is the part that makes it workable rather than annoying: **the private data overlays the public data, matched by ID.**

```
data/partner-tracker.csv        PT-01 … PT-10   who they are, why they matter        (public)
private/partner-contacts.csv    PT-01 … PT-10   status, contact person, notes        (gitignored)
                                      ↓ merged on ID by dashboard/build.py
                            the full picture, locally
```

So the repo carries the *structure* and the Vault carries the *instances*. Run the dashboard locally and you see everything. Publish it and you see the public tier. Nothing is duplicated, nothing has to be manually kept in sync, and the boundary is a property of where a file lives rather than a judgement call made repeatedly.

The same pattern works for the research use case you'd actually want: the analysis code, the schema and the methodology are in the repo; you point them at a dataset in the Vault's `05-raw-data`; the aggregate result comes back into the repo. The tooling is public, the inputs are private, the conclusions are publishable.

**Setting up the overlay, and adding new private fields:** `docs/private-overlay.md` — the operational how-to for this policy.

## Building each tier

```bash
python3 dashboard/build.py            # merges the private overlay if present
                                      # → dashboard/data.private.js (gitignored)

python3 dashboard/build.py --public   # public tier only
                                      # → dashboard/data.js (committed)
```

The dashboard loads `data.js`, then `data.private.js` on top if it exists. The header chip says **Private view** or **Public view** so there's no ambiguity about what's on screen — check it before screenshotting anything.

**Before pushing, always run `--public`.** Otherwise the committed `data.js` goes stale.

## Setting up on a new machine

The `private/` directory is gitignored, so a fresh clone doesn't have it. The canonical copies live in the Vault under `00-private-overlay`. Download them into `private/` and rebuild.

If you skip that step nothing breaks — you get the public view, with a banner on the Partners and PhD tabs explaining what's missing.

## Pre-publish checklist

Run through this before flipping the repo to public, and before enabling Pages.

- [ ] `grep -rn "drive.google.com\|docs.google.com" --include="*.md" --include="*.csv" .` returns nothing outside `private/` and `docs/publishing.md`
- [ ] No file in `data/` has a `Contact_Person`, `Contact_Status`, `Application_Status` or `Private_Notes` column
- [ ] `git ls-files private/` shows only `README.md` and the `.example.csv` templates
- [ ] `dashboard/data.js` was built with `--public` (check: `grep -c '"Private_Notes":' dashboard/data.js` returns 0)
- [ ] No personal data of any research participant anywhere in the tree
- [ ] `git log -p | grep -i` spot-check for anything sensitive in history — **history is public too**
- [ ] Named individuals appearing anywhere public would be comfortable seeing it there
- [ ] New files are covered by one of the two licences, and anything third-party is flagged in `NOTICE`

The `publish-check` skill runs most of this.

## Remaining steps to go public

1. ~~Add a licence~~ — done: Apache-2.0 + CC BY 4.0.
2. **Squash-merge the open PR** so `main` carries only the final tree. Git history is published too, and the Vault folder IDs appear in earlier commits on that branch.
3. **Flip repo visibility** to public. Owner action — irreversible in practice, since anything public may be cloned or indexed immediately.
4. **Enable Pages**: Settings → Pages → Source: GitHub Actions. `.github/workflows/pages.yml` takes over from there.

## About git history

Flipping a repo to public publishes **every commit ever made**, not just the current tree. Removing something in a new commit does not unpublish it.

For this repo that's been checked. The one item ever committed that shouldn't be public is the set of Drive Vault folder URLs, which are access-controlled anyway — someone with a link still has to request access and be refused. Untidy rather than dangerous.

PR #1 was squash-merged, so **`main` carries only the final tree** — a fresh clone contains no Vault IDs.

**But squash-merge does not erase the pull request.** GitHub keeps a merged PR's individual commits reachable under `refs/pull/1/*`, and those are visible to anyone who can see the repo. On a public repo, browsing PR #1's commit list still surfaces the Vault folder IDs. Squashing cleans the branch history, not the PR record.

Three ways to handle it, in ascending order of effort:

1. **Accept it.** The IDs are useless without Drive permissions. This is the proportionate response and the current position.
2. **Rotate the Vault.** Create new folders, move contents, update `private/pointers.csv`, delete the old folders. Cheapest to do while the Vault is nearly empty — the leaked IDs then point at nothing.
3. **Ask GitHub Support to purge the PR refs.** Only worth it if something genuinely sensitive is involved. Nothing here meets that bar.

## Enabling GitHub Pages

Once the repo is public, `.github/workflows/pages.yml` publishes `dashboard/` on every push to `main`. It's committed but **inert until Pages is enabled** in repo settings (Settings → Pages → Source: GitHub Actions).

The workflow builds with `--public`, so even if a private file were somehow present in CI it wouldn't be published. That's belt-and-braces; the real protection is that `private/` is never committed.

Published URL will be `https://benbaichmankass.github.io/sustainable-finance-venture/`.

## What flipping to public does not change

- The Vault stays exactly as private as it is now — it's a separate system with its own permissions.
- Nothing about how you work day to day; the local dashboard still shows everything.

## Licensing

Settled: **Apache-2.0 for code** (`LICENSE`), **CC BY 4.0 for writing and data** (`LICENSE-CONTENT.md`), with `NOTICE` carrying the copyright line and the third-party caveat.

Why this pair rather than the alternatives:

- **Apache-2.0 over MIT.** Almost identical in permissiveness, but Apache adds an express patent grant and patent-retaliation clause. Today the code is a dashboard; the toolkit this project intends to build — origination schema, underwriting engine, waterfall models — is exactly the kind of work where a patent question can surface later, from us or from a contributor. Apache settles it up front at no practical cost.
- **CC BY over CC BY-SA.** Share-alike would force anyone incorporating the data schema or matrix into their own materials to open-license those materials too. For a project whose whole strategy is getting NGOs, DFIs and regulators to adopt a standard, that's a barrier pointed the wrong way.
- **CC BY over CC0.** Attribution is worth keeping for a project with a PhD attached to it. CC0 gives up the citation.
- **CC BY specifically** also matches how this project's own sources publish — World Bank, OECD and CGAP all use it — so their material and ours are mutually compatible rather than in tension.

**What CC BY on the business plan actually means:** anyone may take the thesis, the product design and the structuring logic and build on them commercially, provided they credit the source. That is the intended consequence, not an oversight — the moat here is execution, relationships and field data, none of which is in this repo.

**What is not licensed by us:** cited sources. The matrix holds our summaries and analysis; the underlying papers remain their publishers' property and their full texts stay in the Vault. See `NOTICE`.
