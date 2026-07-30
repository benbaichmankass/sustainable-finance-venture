---
name: resolve-open-question
description: Move an open question forward with evidence. Use when the user asks to "answer OQ-N", "resolve the legal question", research a specific unresolved decision, or when new literature bears on a question already logged in data/open-questions.csv.
---

# Resolving an open question

`data/open-questions.csv` is the list of decisions the project can't yet make. Each one either blocks a milestone or shapes the product. The job is to move a question along the ladder — and to be honest about where it actually landed.

## The status ladder

| Status | Means |
|---|---|
| `Open` | No evidence gathered yet |
| `Partially answered` | Evidence narrows the range, but a decision still needs an input we don't have |
| `Answered` | The decision can now be made, and the notes say what it is |
| `Dropped` | No longer relevant — say why |

**`Partially answered` is the honest destination for most literature work.** A question like "what SPV domicile do we use" cannot be closed by reading; it closes when counsel answers. Marking it `Answered` because the reading is done is the failure mode to avoid.

## Procedure

1. **Read the question and its `Notes` field in full.** The notes usually already contain a working hypothesis and the specific unknown.
2. **Check `Evidence_Refs`** — what's already been brought to bear.
3. **Search the literature matrix first** before going external. The answer is often already in a row nobody connected to the question.
4. **If new sources are needed**, follow the `add-literature` skill — the source goes in the matrix, not just in the question's notes.
5. **Update the row:**
   - `Status` — per the ladder above
   - `Notes` — append what the evidence establishes, and state explicitly *what remains* and *who can supply it* ("remaining work is jurisdiction-specific counsel review, not literature")
   - `Evidence_Refs` — semicolon-separated `LIT-` IDs
6. **Propagate.** A resolved question usually touches:
   - the memo covering that axis (`literature/notes/memo-*.md`)
   - `data/milestones.csv` if a milestone was gated on it
   - `product-design/business-plan.md` §6 if it changes a structuring assumption
7. **Regenerate the dashboard**: `python3 dashboard/build.py`.

## Quality bar

State the *working value* and its *basis* separately. "First-loss tranche at 10–20%, based on observed central tendency in OECD/IFC-documented structures that do not closely resemble our asset class" is useful. "First-loss tranche: 10–20%" is a number someone will later treat as a benchmark.

Where the evidence gives a range rather than an answer, give the range and say what would narrow it.
