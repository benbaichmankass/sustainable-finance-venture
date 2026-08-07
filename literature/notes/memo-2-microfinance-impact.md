# Memo 2: Microfinance Impact Evidence — Synthesis for Product/Research Design

**Status:** Reviewed · **Covers axis:** 2-Microfinance · **Last updated:** 2026-08-07

## Sources
- LIT-003: Systematic review of microfinance impact studies (global)
- LIT-013: OECD 2021, *Evaluating blended finance instruments and mechanisms* (for the evaluation-norms point below)
- LIT-020: Giné & Karlan 2009, group vs individual liability RCTs, Philippines (mechanism)
- LIT-021: Feigenberg, Field & Pande 2010, meeting-frequency RCT, West Bengal (mechanism)
- LIT-022: Ghatak & Guinnane 1999, theory of joint liability (mechanism)

## Key Findings
- Average effects of microcredit access on income/poverty are small in magnitude and heterogeneous across contexts and studies.
- Strongest, most consistent evidence is for consumption smoothing and female empowerment/decision-making outcomes.
- Business investment effects exist for a subset of borrowers (typically those with existing entrepreneurial capacity) but are not the modal outcome.

### On the mechanism of repayment (added 2026-08-07, for OQ-12)

The evidence above is about *outcomes*. A separate strand speaks to *why repayment happens*, which is what our underwriting model actually has to encode.

- **The joint-liability contract is not the active ingredient.** Giné & Karlan (LIT-020) converted half of 169 pre-existing group-liability centres in the Philippines to individual liability and found no effect on repayment, with faster growth in centre size. A second trial randomising villages to either regime reached the same conclusion over two to three years. Both arms kept weekly meetings.
- **Repeat interaction is a strong candidate for what is.** Feigenberg, Field & Pande (LIT-021) randomised first-cycle meeting frequency, then equalised it, so later differences reflect social ties already formed. Monthly-meeting clients were four times more likely to default on their *second* loan. The mechanism they evidence is improved informal risk-sharing — and it operated in **individual-liability** groups, with no joint liability present.
- **Ghatak & Guinnane (LIT-022)** supply the vocabulary: joint liability can act through screening, peer monitoring, enforcement, and reduced audit costs. Information channels and the sanction channel are separable and can trade against each other. Their Irish credit-cooperative case is the sharpest illustration: the cooperatives failed because members would not sanction neighbours, and the proposed remedy — enlarging each cooperative so outsiders could bear the blame — "amounts to throwing away all the information local people have on one another."

**Taken together:** the evidence points away from the contract and toward the social structure it sits in. That structure is what a securitisation removes the community's own money from, which is why OQ-12 treats it as a live risk rather than a settled design question.

## Limitations
- Many underlying studies are non-experimental; borrowers self-select into microcredit, creating potential upward or downward bias depending on context.
- Definitions of "impact" vary widely across studies (income vs. consumption vs. wellbeing), complicating direct comparison.

## Implications for Product Design
1. Do not lead investor/impact narratives with income or business-growth claims — the evidence base is weakest there and most vulnerable to scrutiny.
2. Frame the core value proposition around consumption smoothing, resilience to shocks, and female economic agency, where evidence is strongest and easiest to verify with claims/repayment data.
3. For securitization purposes, resilience/smoothing metrics (on-time repayment continuity, shock-coping claims) are more defensible underwriting signals than projected income growth.
4. This is not a concession — it is an alignment. The securitization and blended-finance literature is largely agnostic about the *mechanism* of impact and cares primarily about cash-flow regularity, default behaviour and data quality (LIT-013). The outcomes with the strongest evidence base are also the ones that map most directly onto what an investor underwrites.

## Open Questions
- **OQ-12, now partially answered.** The contract-versus-social-structure question has good evidence (LIT-020, LIT-021); the securitisation-specific part does not. Nothing in this literature tests what happens when the creditor stops being the community or the MFI the members meet through and becomes an outside investor. That is the part we would have to establish ourselves.
- Does meeting frequency belong in the RT-1 origination schema as a first-class variable? LIT-021 makes it a plausible predictor of default; RT-1 is still v0 and can absorb it.
- Which subpopulations (by geography, group size, existing capacity) show the strongest business-investment response, and can we screen for them at intake?
- How should impact-reporting covenants in a future securitized instrument be worded? Emerging DFI/OECD evaluation norms (LIT-013) reward defensible, measurable claims — resilience and repayment continuity — over broad poverty-reduction assertions, so covenants should be drafted to what we can actually verify.
