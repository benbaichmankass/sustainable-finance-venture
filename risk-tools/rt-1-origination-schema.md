# RT-1 — Origination data schema

**Status:** Specified, not built · **Version:** 0.0 (draft spec) · **Product lines:** PL-1, PL-2 · **Resolves:** OQ-3

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

Four tables, joined on IDs.

| Table | Grain | Holds |
|---|---|---|
| `group` | one row per VSLA / originating unit | formation date, size, cycle length, governance model, location tag, federation |
| `member` | one row per member | pseudonymous ID, join date, role, coarse demographics; **no name, no contact** |
| `loan` | one row per loan | amount, disbursement date, term, rate/fee, purpose code, guarantee structure, schedule |
| `event` | one row per repayment, arrears, claim, restructure, write-off | loan ID, date, type, amount, balance after |

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
| 2026-07-30 | 0.0 | Initial specification. No fields fixed yet — structure and constraints only. |

## Tests

Not yet written. Planned:

- **Validation suite** — every field checked against its domain; a malformed record is rejected at entry, not at analysis time.
- **Referential integrity** — no orphan loans, no events without loans, no members without groups.
- **Round-trip** — export to the ABS tape format and back without loss.
- **Adversarial field data** — the suite must include the messy cases that actually occur: a member leaving mid-cycle, a loan repaid by someone else, a group splitting, a cycle ending early.
- **Cross-version join** — records at two schema versions must be joinable, or the migration note is wrong.

## Open questions

- Which fields are genuinely required versus nice-to-have? Every required field is a tax on the group secretary, and the schema fails if the tax is too high.
- Can we align with SAVIX (RES-31) so existing savings-group MIS data maps in without re-collection? This could be the difference between a pilot cohort of 20 and a pool of hundreds.
- What does a rating agency actually require of VSLA-level receivables, and will any agency engage pre-track-record? (Open in Memo 3.)
- PL-2: does a utility PPA permit assignment of receivables at all? That is the LIT-009 true-sale checklist applied to this asset, and it may be the binding constraint on the whole product line.
