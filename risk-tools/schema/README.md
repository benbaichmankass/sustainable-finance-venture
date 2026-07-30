# Minimum viable origination schema for future poolability

**Schema:** `rt-1-origination-schema.csv` · **Version 0.1** · **Status: v0, not yet field-tested**

## The philosophy

This schema exists to answer one question: **what must be captured at origination so that a pool of these assets is legible to an investor later, without retrofitting?**

Everything follows from a single asymmetry. Most mistakes in this project are recoverable — a wrong assumption in the business plan gets revised, a bad literature summary gets corrected. **A field not captured at origination is gone forever.** You cannot go back to a village in 2029 and ask what a borrower's savings balance was on the day of a 2027 disbursement. A field added in year two produces a portfolio with two years of nulls, which to a rating agency is a portfolio with no history.

So the design rule is not "capture everything useful." It is **capture everything irreplaceable, and nothing else.**

## Three constraints, one of them binding

**1. ABS legibility.** The end state is a loan-level data tape an investor will accept. The benchmark is the European DataWarehouse loan-level templates (RES-28) — not because we will report to them, but because they are a settled answer to "what does an investor need to know about each loan."

**2. Field-workability.** Per LIT-014, savings-group regulation is heading toward light-touch registration with digitised records, delegated to local authorities and NGOs. Every required field must be capturable by a group secretary with a phone, in a meeting, without training beyond what the group already gets.

**3. Privacy.** Personal data lives in the Vault, never the repo. The schema separates a stable pseudonymous ID from the identifying record, so analysis and pooling run on the pseudonymous layer alone.

**Constraint 2 is binding.** It is easy to design a schema that satisfies 1 and 3 and is unusable in a village meeting. Every field here was tested against the question "could a group secretary record this, in a meeting, without a laptop?" Fields that failed are not in the schema, however useful they would have been.

That is why there is no GPS coordinate, no exact date of birth, no itemised household income, and no free-text notes field.

## What "minimum viable" cost us

Deliberate omissions, recorded so they are choices rather than oversights:

| Not captured | Why not |
|---|---|
| Exact location (GPS/village) | Identifies a group. `admin1` is required and `admin2` optional; that is enough to model a regional drought without exposing anyone. |
| Exact date of birth | Age bands give the cohort analysis its value with none of the identifiability. |
| Household income | Not reliably measurable in a meeting. A number that is collected but wrong is worse than a gap, because it gets modelled. |
| Free-text notes | Unpoolable. Anything worth analysing gets an enum or it does not get captured. |
| Detailed impact outcomes | Belongs to RT-4 under a pre-registered design, not to origination. Collecting outcome data casually is how impact claims lose credibility. |

## The two things that carry the most weight

**The `event` table.** Static loan attributes are cheap and largely reconstructible from a contract. The payment-behaviour time series is not, and it is what an underwriting model learns from and an investor prices. If only one table survives contact with the field, this is the one that matters.

**`schema_version` on every row.** Unglamorous and non-negotiable. A mixed-vintage portfolio without version stamps cannot be interpreted, and the stamp cannot be backfilled — by then nobody knows which rules a given record was captured under.

## Reading the schema file

| Column | |
|---|---|
| `Entity` | Which table: `originator`, `group`, `member`, `loan`, `event` |
| `Required` | `required` fields block a record; `optional` fields are collected where cheap |
| `Capture` | `origination` (fixed at disbursement), `updated` (changes over time), `derived` (computed, never entered) |
| `Privacy` | `public` · `private` (pseudonymous, repo-safe) · `sensitive` (aggregate only, never row-level) · `derived` |
| `Critical_Path` | `yes` = cannot be reconstructed later. **These are the fields worth arguing about.** |
| `Validation` | The rule `validate_schema.py` enforces |
| `Why_It_Matters` | Why the field earns its place. A field that cannot fill this column should not exist. |

45 of 57 fields are critical path. That ratio is high on purpose: a field that *can* be reconstructed later is a field that does not need to be in a v0 schema.

## Status and what would change it

This is **v0**. It has been designed against the literature and validated for internal consistency — it has **not** been tested with a real group, and no field data has been collected against it.

What would move it to v1:

1. A group secretary completing a full cycle of records with it, and telling us which fields they skipped.
2. A SAVIX mapping exercise — if existing MIS data maps in cleanly, the pilot cohort could be hundreds of groups rather than twenty.
3. A structuring conversation confirming these fields are what an investor would actually want (PT-08).

Until then, treat the field list as a serious proposal, not a settled contract.
