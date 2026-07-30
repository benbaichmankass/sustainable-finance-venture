# The private overlay

> **Full onboarding guide: [`docs/private-overlay.md`](../docs/private-overlay.md)** — setup, what happens when the overlay is absent, and a worked example of adding a private field. This file is the quick reference.

This directory is **gitignored**. Nothing in it except this file and the `*.example.csv` templates is ever committed.

It exists so the repo can be public without losing the private half of the picture. The public CSVs in `data/` hold the parts of each tracker that are safe to publish — organizations, categories, criteria, research reasoning. The files here hold the parts that aren't: named individuals, relationship status, negotiation notes, deal terms, and links into the Drive Vault.

`dashboard/build.py` merges the two by ID when these files are present. Locally you see the whole picture; a public build shows only the public tier.

## Files

| File | Overlays | Adds |
|---|---|---|
| `partner-contacts.csv` | `data/partner-tracker.csv` on `ID` | `Contact_Status`, `Contact_Person`, `Private_Notes` |
| `phd-applications.csv` | `data/phd-programs.csv` on `ID` | `Candidate_Supervisors`, `Application_Status`, `Outreach_Plan`, `Private_Notes` |
| `pointers.csv` | `data/resources.csv` on `ID` | `URL` for the Vault and tracker rows |

All three are ID-keyed overlays — they fill in columns on rows that already exist publicly, they don't add rows. That matters for `pointers.csv`: the public tier keeps the Vault row and its description, so a reader can see the Vault exists and what it holds, and only the link itself is withheld. `pointers.csv` is therefore just two columns, `ID` and `URL`.

Each has a committed `.example.csv` showing the schema with dummy rows.

## Where the real copies live

**The Drive Vault is canonical for these files.** This directory is a working copy. If you're setting up on a new machine, download them from the Vault's `00-private-overlay` folder rather than reconstructing them.

When you change one locally, upload it back. There is no sync automation — it's a deliberate act, which is the point.

## The rule for what goes here

Anything that names a person and says something about them — their status, what they said, whether they declined — belongs here, not in `data/`.

Organizations are usually fine in public. "CARE's VSLA network is a candidate origination partner" is a research observation. "Spoke to [name] on 12 March, lukewarm, revisit after pilot" is not.

If you're unsure, it goes here. Moving something from private to public later is easy; the reverse is not, because git history is forever.
