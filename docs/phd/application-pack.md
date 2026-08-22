# The application pack

**Status:** v1 (2026-08-22) · **Owner:** BB
**Lives in:** the Drive Vault, `02-applications-phd/General Application`. The link is in `private/pointers.csv`, not here - see `docs/ops/drive-vault.md`.

## What it is

A general set of application documents built once, copied and customised per
advisor. It exists so that approaching a thirteenth programme costs an hour rather
than a weekend, and so that what each recipient was sent is a matter of record.

It lives in the **Vault**, not the synced workfolder, because it contains personal
documents - transcripts, certificates, a CV. `docs/ops/drive-vault.md` is explicit
that those never sit in the public-linked workfolder, and the repo holds the pointer
rather than the folder ID.

## The escalating-length principle

An application does not need one long document. It needs four documents of
increasing length, because different people at different moments read different
amounts:

| Length | Document | Read by | When |
|---|---|---|---|
| One line | Working title | Anyone, in a subject line | Always |
| One paragraph | Abstract | A supervisor deciding whether to open the attachment | Always |
| One page | One-pager | A supervisor deciding whether to reply | First contact |
| Two pages | Research statement | A supervisor deciding whether to meet | After interest |
| Eight to ten pages | Full proposal | An admissions committee, or a supervisor who is already interested | Formal application |

**The failure this prevents:** sending the full proposal as a first contact. It is
the most common mistake in cold supervisor outreach and it reliably produces no
reply, because it asks for forty minutes from someone who has not yet decided to
give you four.

## Contents

| # | Document | Source in repo | Customise per advisor? |
|---|---|---|---|
| 00 | README and customisation checklist | this document | No |
| 01 | Working title and abstract | `docs/phd/research-questions.md` | **Yes - lead strand** |
| 02 | One-pager | assembled | **Yes - lead strand** |
| 03 | Research statement (2 pages) | assembled | **Yes - lead strand, and programme fit** |
| 04 | Research proposal (full) | `docs/phd/phd-proposal-master.md` | Lightly - framing only |
| 05 | Research questions menu | `docs/phd/research-questions.md` | No - reference |
| 06 | Research framework summary | `docs/research/research-framework.md` | No - reference |
| 07 | Experiment menu | `data/experiments.csv` | Site and population per programme |
| 08 | Statement of purpose template | assembled | **Yes - heavily** |
| 09 | Supervisor outreach email templates | assembled | **Yes - every time** |
| 10 | Advisor customisation notes | this document, expanded | No |
| 11 | CV outline | BB to complete | Lightly |
| 12 | Reading list by component | `data/lit-components.csv` | No - reference |

Items 05, 06, 07 and 12 are generated from the repo and should be regenerated rather
than edited in Drive - the repo is the source of truth (CLAUDE.md §1).

## Outstanding: the misplaced credentials

**Action needed from the account that owns them.** Ten personal files — transcripts,
degree certificates, psychometric scores — sit in a folder called "Application Docs"
inside the **SFV workfolder**, which `docs/ops/drive-vault.md` documents as the
publicly-linked folder. They belong in this pack's `Credentials` subfolder, which
exists and is empty.

They could not be moved automatically: the files are owned by a different Google
account from the one the tooling is authenticated as, and Drive refuses the move with
a permission error. It is a two-minute drag from the owning account.

Drive currently reports the workfolder as owner-only, so nothing is exposed today. But
the repo's own documentation treats that folder as public, and the dashboard links to
it — so this is a live hazard rather than a theoretical one, and it should not wait.

## Customising for an advisor

Four moves, in order. The first is the only one that really matters.

1. **Pick the lead strand.** `docs/phd/research-questions.md` maps advisor profile to
   strand. This changes documents 01, 02 and 03, and it changes the first sentence -
   which is the sentence that decides whether the rest gets read.
2. **Name one reserve strand** as the co-supervision territory. No department has all
   four pillars this project needs, and proposing where the second supervisor would
   sit is a strength, not an admission.
3. **Set site and population** to what that programme can actually reach. Geography
   is deliberately open (decision of 2026-08-22): the design specifies what it needs
   *from* a site rather than naming one. A programme with an existing East Africa
   field presence gets East Africa; a programme with Latin America coffee links gets
   the coffee cluster.
4. **Say why them, specifically.** One sentence referencing their actual work. If
   that sentence cannot be written honestly, the programme is on the list for the
   wrong reason.

**Never present the menu.** One question, one reserve, one coherent programme. An
advisor who sees seven questions sees someone who has not chosen.

## Versioning

Each document carries a version tag and a one-line changelog in its header. When a
document changes materially, bump the version.

Then record, in `private/phd-applications.csv`, which pack version each recipient
received. A reply arriving six weeks later needs to be readable against what that
person actually saw - and after two or three revision rounds, it will not be
obvious from memory.

Contact status and named individuals live in `private/`, never in `data/`
(CLAUDE.md §8).

## BB's own shortlist, and where it disagrees with the rubric

Captured from the scratchpad, 2026-08-19, and worth keeping because it is a
preference signal the scoring does not contain:

| BB's list | ID | Rubric tier |
|---|---|---|
| HUJI Business School | PHD-10 | Priority (3.95) |
| Groningen | PHD-22 | Priority (3.80) |
| TAU Coller | PHD-02 | Consider (3.10) |
| Copenhagen | PHD-49 | Consider |
| Mannheim / ZEW | PHD-29 | Consider (3.40) |
| Bocconi | PHD-51 | Priority-adjacent |

**The disagreement is the interesting part.** The rubric's three top-ranked
programmes - UEA (PHD-15), CERMi (PHD-20) and IHEID Geneva (PHD-21), all at 4.05 -
are not on this list at all, and four of the six chosen are `Consider` rather than
`Priority`. That is not necessarily wrong: the rubric cannot see language, personal
ties, partner proximity or where someone actually wants to live, and those are real
inputs.

But it is worth being deliberate about. Either the rubric weights are off - in which
case change them in the workbook and let the field re-rank - or the shortlist is
being driven by something the rubric deliberately down-weighted, in which case name
it. Both are fine; drifting between them is not.

Two of the six also carry known funding caveats worth checking before investing
effort: the HUJI PBC/Rotenstreich fellowship is citizens and permanent residents
only, and German funding routes require a salaried TV-L position rather than a
development scholarship (`docs/phd/phd-funding-landscape.md`).

## Keeping the pack in step with the repo

The pack drifts the moment the repo moves. Regenerate documents 04, 05, 06, 07
and 12 whenever their sources change materially - in particular after the P1
literature phase (M-26), which will change the framework's power section and the
reading list, and after OQ-15 resolves, which will change the experiment menu.

The pack is **not** registered in `data/drive-links.csv`. That manifest is for the
public bidirectional workfolder; adding Vault content to it would publish the
folder ID.
