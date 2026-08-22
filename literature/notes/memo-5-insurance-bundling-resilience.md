# Memo 5: Insurance, bundling, and what resilience means

**Status:** Drafted (partial) · **Covers components:** LC-03, LC-04, LC-05 · **Last updated:** 2026-08-22

> **Scope warning.** Only **LC-04 (bundled credit and insurance)** has had a first pass. LC-03
> (index insurance demand, basis risk, impact) and LC-05 (resilience measurement) are unread, and
> their sections below are placeholders. The memo exists now rather than later because LC-04's
> findings contradict a live claim in the proposal and should not sit only in a CSV.
>
> All four sources were verified from **published abstracts and authoritative summary pages, not
> full texts**, so their matrix rows are `To read`. Everything below is quotable to that standard
> and no further.

## Sources

- **LIT-024** — Giné & Yang 2009, *Insurance, credit, and technology adoption: Field experimental evidence from Malawi*, J Dev Econ 89(1) 1–11. RCT, ~800 farmers.
- **LIT-025** — Banerjee, Duflo & Hornbeck 2014, *Bundling Health Insurance and Microfinance in India*, AER 104(5) 291–297. RCT, Karnataka.
- **LIT-026** — Karlan, Osei, Osei-Akoto & Udry 2014, *Agricultural Decisions after Relaxing Credit and Risk Constraints*, QJE 129(2) 597–652 (read as NBER WP 18463). RCT, northern Ghana.
- **LIT-027** — Carter, Cheng & Sarris 2016, *Where and how index insurance can boost the adoption of improved agricultural technologies*, J Dev Econ 118(C) 59–71. Theory.

---

## 1. The finding that changes the proposal

The master proposal claims bundling is "a design question the existing literature raises but
rarely tests directly." **That is false.** It has been tested experimentally at least twice, and
in both cases compulsory bundling suppressed demand:

| | Setting | Product | Result |
|---|---|---|---|
| **LIT-024** | Malawi, ~800 farmers | Rainfall index cover *required* with a seed loan, actuarially fair | Take-up **13 points lower**, against a 33.0% uninsured base |
| **LIT-025** | Karnataka, MFI clients | Health cover *mandated* on loan renewal, actuarially fair | **16-point (23%) rise in drop-out** from microfinance |

Giné and Yang's own suggested explanation is the interesting part: farmers were **already
implicitly insured by the limited-liability clause in the loan contract**, so adding a priced
policy read as an interest-rate rise rather than as protection. Banerjee, Duflo and Hornbeck
found demand so close to absent that there was no adverse selection to be had.

**LIT-025 also answers a question we had listed as open.** LC-04 asked whether anyone had measured
bundling's effect on the *lender's* book rather than borrower welfare. Someone has, and the answer
was strongly negative.

## 2. The counterweight, and why this is a tension rather than a verdict

LIT-026 points the other way, and it is not a weaker study. In northern Ghana, **uninsured risk —
not capital — is the binding constraint** on farm investment: insured farmers "find resources to
increase expenditure on their farms," take on riskier, higher-return production, and demand for
index insurance is *strong*. Demand rises with one's own payouts, with payouts to others in one's
social network, and after recent poor rain.

The reconciliation is a design distinction, and it is the single most useful thing in this memo:

> **Insurance offered separately, often subsidised → strong demand and real investment effects.
> Insurance compulsorily priced into a loan → demand collapses.**

LIT-027 is the theory that asks precisely this — standalone versus explicitly interlinked with
credit — and conditions its answer on the structure of risk and on the **collateral environment**.
That last term matters, because Giné and Yang's limited-liability explanation *is* a
collateral-environment argument. Reading that model may reconcile the two empirical results
directly, which makes it the highest-value next read in this component.

## 3. Implications for this project

**Do not put EXP-01 in front of an advisor as written.** Its design — "premium financed into the
loan principal so cover is automatic rather than opt-in" — is exactly the intervention that failed
twice. It is not novel, and worse, its expected sign is now negative on take-up.

**EXP-17 is promoted from add-on to centrepiece.** It offers the same actuarial product three
ways: financed into principal, opt-in at the same price, and opt-in with a subsidy that equalises
take-up. That is the direct experimental separation of the take-up effect from the protection
effect, and the literature above makes it the live question rather than a robustness check.

**The novelty claim has to move.** Candidates, none chosen — this is OQ-17 and it is BB's call:

1. **The funding-source layer** (RQ-04, EXP-13). Nothing in the matrix randomises community
   capital against external wholesale capital. Untouched by any of these papers.
2. **Lender-side cash-flow characterisation.** LIT-025 measured drop-out. It did not produce loss
   curves, correlation estimates or anything resembling a data tape. That gap looks real and is
   ours.
3. **The design question itself** — whether compulsory bundling can be structured so it does not
   destroy demand, which is EXP-17.

**One assumption in RT-6 is now unsupported.** Any cash-flow model treating bundling as
retention-neutral contradicts LIT-025. Retention is a modelled driver, not a constant.

## 4. LC-03 — index insurance: demand, basis risk, impact

*Not yet read.* LIT-026 and LIT-027 already gesture at the two themes that will dominate it:
**basis risk** and **imperfect trust that payouts will arrive**, both named in LIT-026's abstract
as consistent with observed demand patterns. Note for when this is read: our EXP-30 (satellite
versus picture-based verification) is a basis-risk experiment and should be re-read against
whatever this component turns up.

## 5. LC-05 — resilience and consumption-smoothing measurement

*Not yet read.* The research framework's §5 depends on it — specifically on shock measurement and
on powering for the conditional effect. No findings to report yet.

## Limitations of this memo

- Four sources, all verified from abstracts only. None of the four full texts has been read, so
  design detail, robustness and stated limitations are largely unknown to us.
- One unresolved discrepancy: LIT-024's published abstract says take-up was 13 points lower, while
  the J-PAL summary page states 33% versus 17.6% (a 15.4-point gap). Probably regression-adjusted
  versus raw, but that is our inference and neither source says so.
- Secondary summaries make two further claims we could **not** verify and which must not be cited:
  a 22-point fall in loan renewal in LIT-025, and a claim that LIT-027's model implies insurance
  *must* be bundled in low-collateral environments.
- Two of the three components this memo is scoped to cover are unread.

## Implications for product/research design

1. Treat compulsory, premium-financed cover as a **known-risky design**, not a neutral default.
2. Make the take-up-versus-protection separation an explicit design question in any bundled pilot.
3. Carry a **retention** outcome in every bundled design — LIT-025 shows the lender-side effect can
   dominate, and it is the one that reaches the securitisation model.
4. Read LIT-027's model next; it is the most likely route to reconciling LIT-024 with LIT-026.
