# RT-1 — Origination data schema

**Status:** v0 built, not field-tested · **Version:** 0.1 · **Product lines:** PL-1, PL-2 · **Resolves:** OQ-3
**Schema:** [`schema/rt-1-origination-schema.csv`](schema/rt-1-origination-schema.csv) — 57 fields, 5 entities · **Philosophy:** [`schema/README.md`](schema/README.md) · **Validator:** `risk-tools/tools/validate_schema.py`

## Purpose

Define every field captured at the moment a loan is disbursed or a policy is written, so that a pool of these assets is legible to a rating agency and an investor without retrofitting.

This is the tool that decides whether the venture works. The securitisation literature is unanimous that a standardisation layer is a precondition, not a nice-to-have (LIT-004, LIT-006, LIT-008). And unlike every other tool here, **a schema failure cannot be repaired later** — data not captured at origination is gone. A field added in year two produces a portfolio with two years of nulls, which for a rating agency is a portfolio with no history.

## Design constraints

Three constraints pull in different directions, and the schema has to satisfy all three.

**1. ABS legibility.** The end state is a loan-level data tape a rating agency will accept. The benchmark is the European DataWarehouse loan-level templates (RES-28) — not because we will report to them, but because they represent a settled answer to "what does an investor need to know about each loan."

**2. Field-workability.** Per LIT-014, savings-group regulation is heading toward light-touch registration with digitised group records, delegated to local authorities, NGOs and federations. A schema that only works inside a supervised financial institution will not reach the groups we need. Every required field must be capturable by a group secretary with a phone, in a meeting, without training beyond what the group already receives.

**3. Privacy.** Personal data lives in the Vault's `05-raw-data`, never the repo (`CLAUDE.md` §8). The schema must therefore separate a **stable pseudonymous ID** from the identifying record, so analysis and pooling can run on the pseudonymous layer alone.

Constraint 2 is the binding one. It is easy to design a schema that satisfies 1 and 3 and is unusable in a village meeting.

## Structure

Five tables, joined on IDs. Field counts are as built in v0.1.

| Table | Fields | Grain | Holds |
|---|---|---|---|
| `originator` | 4 | one row per originating institution | type, country, regulated status |
| `group` | 15 | one row per VSLA / originating unit | formation date, cycle number and length, size, governance, meeting cadence, savings balance, coarse geography, SAVIX link |
| `member` | 9 | one row per member | pseudonymous ID, join date, role, banded demographics, livelihood, prior cycles; **no name, no contact, no exact DOB** |
| `loan` | 19 | one row per loan | principal, disbursement date, term, charge rate and basis, purpose, guarantee structure, borrower savings, prior-loan count |
| `event` | 10 | one row per repayment, arrears, restructure, write-off, claim | loan ID, date, type, amount, balance after, DPD, who recorded it |

**48 of 57 fields are required; 45 are critical path** — meaning they cannot be reconstructed after origination. That ratio is high deliberately: a field that *can* be rebuilt later does not belong in a v0 schema.

The `event` table is where the value is. Static loan attributes are cheap; the payment-behaviour time series is what an underwriting model learns from and what an investor prices.

For PL-2 the same shape applies with `project` replacing `group` and PPA settlement events replacing repayments — the structural analogy is deliberate and is what lets one toolkit serve both lines.

## Field-level rules

- **Every field has a defined domain.** Enumerations, not free text, wherever a category is meant. Free text is unpoolable.
- **Money carries a currency code and a date.** No bare amounts.
- **Dates are ISO 8601.** No local formats.
- **Nulls are distinguishable from zeros.** "No repayment recorded" and "repayment of zero" are different facts.
- **Every row carries `schema_version`.** Without it a mixed-vintage portfolio is uninterpretable.

## Versioning

`data/risk-tools.csv` holds the current version. This schema is a **data contract with people in the field**, so version changes are more expensive than code changes:

| Bump | Means | Cost |
|---|---|---|
| Major | Field removed, domain changed, meaning changed | Retraining, possibly reprinted forms, migration note required |
| Minor | Optional field added | New field is null for prior vintages — acceptable, must be documented |
| Patch | Clarified description, corrected typo | None |

**Batch changes.** A major bump every quarter destroys field trust. Accumulate and release deliberately.

Every version records: what changed, why, which vintages are affected, and how to interpret the join across the boundary.

### History

| Date | Version | Change |
|---|---|---|
| 2026-07-30 | 0.0 | Initial specification. Structure and constraints only. |
| 2026-07-30 | 0.1 | First concrete field list: 57 fields across 5 entities, with validator. Not yet field-tested — see `schema/README.md` for what would move it to v1. |

## Tests

**Built** (`risk-tools/tools/validate_schema.py`, runs in CI):

- **Schema self-check** — field IDs are unique lower_snake_case; every entity, type, requiredness, capture mode and privacy class is in its allowed set; enums actually declare values; derived fields carry a formula; every entity has a `schema_version` field. It also enforces that every field explains why it exists — a rationale under 60 characters fails the build, which caught five lazy entries on the first run.
- **Dataset validation** (`--data <dir>`) — required fields present, enums respected, ISO dates, referential integrity across all five tables.

Still planned:

- **Round-trip** — export to the ABS tape format and back without loss.
- **Adversarial field data** — the suite must include the messy cases that actually occur: a member leaving mid-cycle, a loan repaid by someone else, a group splitting, a cycle ending early.
- **Cross-version join** — records at two schema versions must be joinable, or the migration note is wrong.

## Open questions

- Which fields are genuinely required versus nice-to-have? Every required field is a tax on the group secretary, and the schema fails if the tax is too high. v0.1 puts 48 fields in the required column; that number is a proposal and should be argued down, not up, once a real secretary has used it.
- Can we align with SAVIX (RES-31) so existing savings-group MIS data maps in without re-collection? This could be the difference between a pilot cohort of 20 and a pool of hundreds.
- What does a rating agency actually require of VSLA-level receivables, and will any agency engage pre-track-record? (Open in Memo 3.)
- PL-2: does a utility PPA permit assignment of receivables at all? That is the LIT-009 true-sale checklist applied to this asset, and it may be the binding constraint on the whole product line.
