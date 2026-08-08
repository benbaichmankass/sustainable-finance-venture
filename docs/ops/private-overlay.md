# The private overlay — collaborator onboarding

**Audience:** anyone working in this repo, human or agent · **Last updated:** 2026-07-30

This repo is public. A short private tier is not, and it is not private because it is commercially precious — it is private because **it is about people**. This document explains how the two fit together and how to work with both without leaking one into the other.

Policy and reasoning: docs/ops/publishing.md. This is the operational how-to.

## The one-sentence rule

**Does it name a person and say something about them? Private. Does it name an organization and explain why it is relevant? Public.**

> "CARE's VSLA network is the largest established methodology network and a candidate origination partner" — **public**. It is a research observation.  
>   
> "Spoke to \[name\] on 12 March, lukewarm on the data standard, revisit after pilot" — **private**. It is a fact about our relationship with a person.

## What goes where

| Public repo | private/ (gitignored) | Drive Vault |
| :---- | :---- | :---- |
| Organizations, and why they matter | A named individual's status | PDFs of copyrighted sources |
| Methods, schemas, code, models | Who was approached, who declined | CVs, transcripts, applications |
| Literature matrix and memos | Contact people and roles | Correspondence threads |
| Open questions and reasoning | Application status | Signed documents, term sheets |
| Aggregate findings | Vault and tracker links | **Row-level participant data** |

**Never committed, under any circumstance:** row-level pilot data, anything identifying a research participant, credentials or tokens, Drive folder IDs, or a person's name attached to our outreach status.

Row-level participant data does not belong in private/ either — it lives only in the Vault's 05-raw-data. private/ is for the working overlay, not for personal data.

## How the overlay works

The two tiers are joined **by ID at build time**, not duplicated:

data/partner-tracker.csv        PT-01 … PT-10   who they are, why they matter   (public, committed)

private/partner-contacts.csv    PT-01 … PT-10   status, contact person, notes   (gitignored)

                                       │

                                       └── dashboard/build.py merges on ID

                                              ↓

                                    the full picture, locally only

Three overlays exist today:

| Overlay file | Extends | Adds |
| :---- | :---- | :---- |
| private/partner-contacts.csv | data/partner-tracker.csv | Contact\_Status, Contact\_Person, Private\_Notes |
| private/phd-applications.csv | data/phd-programs.csv | Candidate\_Supervisors, Application\_Status, Outreach\_Plan, Private\_Notes |
| private/pointers.csv | data/resources.csv | URL for Vault and tracker rows |

**Overlays fill in columns on rows that already exist publicly. They never add rows.** That is deliberate: the public tier keeps the row and its description, so a reader can see that a partner or a Vault folder exists and what it is for. Only the private column is withheld. An overlay that added rows would let the public tier silently under-report what the project is doing.

## Setting up locally

A fresh clone has no private/ contents — only this repo's README.md and the .example.csv templates.

git clone https://github.com/benbaichmankass/sustainable-finance-venture

cd sustainable-finance-venture

\# 1\. Get the overlay files from the Vault's 00-private-overlay folder

\#    and put them in private/. The Vault is canonical for these.

\# 2\. Build. With the overlay present this writes data.private.js:

python3 dashboard/build.py

\# 3\. Open dashboard/index.html. The header chip should read "Private view".

Without step 1 nothing breaks — you get the public view, and the Partners and PhD tabs show a banner explaining what is missing.

## What happens when private data is absent

By design, gracefully and visibly:

|  | With overlay | Without |
| :---- | :---- | :---- |
| Build output | dashboard/data.private.js (gitignored) | dashboard/data.js (committed) |
| Header chip | **Private view**, amber border | **Public view** |
| Partners tab | Contact column \+ status breakdown | Banner: "Contact status is in the private overlay" |
| PhD tab | Supervisors, status, outreach plan | Banner explaining the same |
| Resources tab | Vault links resolve | Rows present, links blank |

The header chip is the thing to check before screenshotting or sharing anything. **Private view means the screenshot contains names and relationship status.**

## Before pushing

Always rebuild the public tier, or the committed data.js goes stale:

python3 dashboard/build.py \--public

Then run the audit — the publish-check skill automates most of it:

grep \-rn "drive\\.google\\.com\\|docs\\.google\\.com" \--include="\*.md" \--include="\*.csv" . | grep \-v "^./private/"

grep \-l "Contact\_Person\\|Private\_Notes\\|Application\_Status" data/\*.csv

git ls-files private/          \# expect only README.md and \*.example.csv

CI enforces the same checks in .github/workflows/pages.yml and fails the deploy if a private file or column ever reaches it. That is a backstop, not the first line of defence — private/ being gitignored is.

## Adding a new private-only field

Worked example. Say partner rows need a Last\_Contact\_Date.

**1\. Decide the tier.** Does it name a person or describe our relationship with one? A contact date is relationship status → private.

**2\. Add it to the overlay file only.**

"ID","Contact\_Status","Contact\_Person","Private\_Notes","Last\_Contact\_Date"

"PT-03","In conversation","A. Example, Programme Director","Warm on the data standard.","2026-08-14"

**3\. Update the template** private/partner-contacts.example.csv with the same column and **fake data only**, so a new collaborator sees the schema without seeing anyone's details.

**4\. Nothing in build.py needs changing.** The merge copies every non-ID column from the overlay, so new fields flow through automatically.

**5\. Render it if useful** — add it to the relevant detail panel in dashboard/index.html, and guard on presence so the public build degrades cleanly:

\["Last contact", esc(r.Last\_Contact\_Date)\]   // fields() drops empty values

**6\. Document it** in the overlay table above and in private/README.md.

**7\. Upload the changed overlay to the Vault**, which is canonical. There is no sync automation — it is a deliberate act, which is the point.

## Adding a whole new overlay

If a public tracker needs a private companion:

1. Create private/\<name\>.csv keyed by the public tracker's ID.  
2. Commit private/\<name\>.example.csv with fake rows.  
3. Register it in OVERLAYS in dashboard/build.py.  
4. Confirm .gitignore still excludes the real file — private/\* with negations for README.md and \*.example.csv already covers it.  
5. Run python3 dashboard/build.py \--public and confirm the new columns do **not** appear in dashboard/data.js.

## If something private is committed by accident

1. **Do not just delete it in a new commit.** Git history is public; removing it later does not unpublish it.  
2. Assess what it actually was. A Drive folder ID is untidy; a person's contact details or participant data is an incident.  
3. For anything genuinely sensitive: rotate first (move the Vault folder, revoke the credential) so the exposed value stops being useful, then decide about history rewriting.  
4. Tell the repo owner. Do not quietly rewrite published history.

