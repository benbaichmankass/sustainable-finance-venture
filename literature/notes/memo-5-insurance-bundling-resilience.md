# Memo 5: Insurance, bundling, and what resilience means

**Status:** Drafted (partial) · **Covers components:** LC-03 ✓, LC-04 ✓, LC-05 (unread) · **Last updated:** 2026-08-22

> **Scope warning.** **LC-04 (bundling)** and **LC-03 (index insurance demand and basis risk)**
> have each had a first pass. **LC-05 (resilience measurement)** is unread and its section is a
> placeholder. The memo exists because LC-04's findings contradict a live claim in the proposal
> and should not sit only in a CSV.
>
> All four sources were verified from **published abstracts and authoritative summary pages, not
> full texts**, so their matrix rows are `To read`. Everything below is quotable to that standard
> and no further.

## Sources

- **LIT-024** — Giné & Yang 2009, *Insurance, credit, and technology adoption: Field experimental evidence from Malawi*, J Dev Econ 89(1) 1–11. RCT, ~800 farmers.
- **LIT-025** — Banerjee, Duflo & Hornbeck 2014, *Bundling Health Insurance and Microfinance in India*, AER 104(5) 291–297. RCT, Karnataka.
- **LIT-026** — Karlan, Osei, Osei-Akoto & Udry 2014, *Agricultural Decisions after Relaxing Credit and Risk Constraints*, QJE 129(2) 597–652 (read as NBER WP 18463). RCT, northern Ghana.
- **LIT-027** — Carter, Cheng & Sarris 2016, *Where and how index insurance can boost the adoption of improved agricultural technologies*, J Dev Econ 118(C) 59–71. Theory.
- **LIT-028** — Clarke 2016, *A Theory of Rational Demand for Index Insurance*, AEJ: Micro 8(1) 283–306. Theory.
- **LIT-029** — Carter, de Janvry, Sadoulet & Sarris 2017, *Index Insurance for Developing Country Agriculture: A Reassessment*, Ann Rev Resource Econ 9 421–438. Review.
- **LIT-030** — Jensen, Mude & Barrett 2018, *How basis risk and spatiotemporal adverse selection influence demand for index insurance: Evidence from northern Kenya*, Food Policy 74(C) 172–198. Panel.

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

First pass done. It compounds §1–§3 rather than softening them, in three steps.

**The sector's own verdict is that demand is not there at unsubsidised prices.** LIT-029 — an
Annual Review stock-take, so about as authoritative as a summary gets — states that despite
extensive experimentation, **"take-up has been disappointingly low without large and sustained
subsidies."** Set that beside EXP-01, which finances the premium *into the amount owed*. That is
the opposite of a subsidy. The design is on the wrong side of the one variable this review
identifies as decisive.

**And the low demand may be correct, not mistaken.** LIT-028 is the theoretical result that should
change how we talk about this. Because an index pays on a proxy rather than on your actual loss,
rational demand behaves unlike indemnity demand: **optimal demand is zero for the infinitely
risk-averse, and nonmonotonic in risk aversion, wealth and price.** If low take-up is a rational
response to basis risk and deadweight cost, then compelling purchase does not correct an error —
it overrides a correct decision and pushes the cost onto the borrower. That is a plausible
mechanism for both LIT-024 and LIT-025, and it is a *do-no-harm* concern, not only a demand one.

**Basis risk is measurable and it bites.** LIT-030 is the first study to measure basis risk
directly and use it in a demand estimation: alongside price and the familiar non-price factors,
**basis risk and spatiotemporal adverse selection** materially drive IBLI demand in northern
Kenya.

That last finding has a second life on the structuring side, and it is the kind of thing that gets
missed when a source is filed under one component. Index products are usually *presumed* immune to
adverse selection. If clients time purchase on private seasonal information, the pool's loss
distribution is not what a naive actuarial model assumes — so LIT-030 is cross-referenced into
LC-08 (portfolio correlation) as well.

**For EXP-30** (satellite versus picture-based verification): LIT-028 and LIT-030 together make
its premise sound — basis risk is first-order for demand — while LIT-029 names measurement
technology as one of the levers that can partially overcome take-up constraints. What none of them
answers is EXP-30's actual question, whether better verification pays for what it costs.

## 5. LC-05 — resilience and consumption-smoothing measurement

*Not yet read.* The research framework's §5 depends on it — specifically on shock measurement and
on powering for the conditional effect. No findings to report yet.

## Limitations of this memo

- Seven sources, all verified from abstracts or publisher summary pages only. None of the four full texts has been read, so
  design detail, robustness and stated limitations are largely unknown to us.
- One unresolved discrepancy: LIT-024's published abstract says take-up was 13 points lower, while
  the J-PAL summary page states 33% versus 17.6% (a 15.4-point gap). Probably regression-adjusted
  versus raw, but that is our inference and neither source says so.
- Secondary summaries make two further claims we could **not** verify and which must not be cited:
  a 22-point fall in loan renewal in LIT-025, and a claim that LIT-027's model implies insurance
  *must* be bundled in low-collateral environments.
- LIT-029's canonical abstract could not be reached — Annual Reviews and SSRN both returned
  HTTP 403 — so it is quoted from the FERDI publication page and a search-result rendering.
- One of the three components this memo is scoped to cover (LC-05) is unread.

## Implications for product/research design

1. Treat compulsory, premium-financed cover as a **known-risky design**, not a neutral default.
2. Make the take-up-versus-protection separation an explicit design question in any bundled pilot.
3. Carry a **retention** outcome in every bundled design — LIT-025 shows the lender-side effect can
   dominate, and it is the one that reaches the securitisation model.
4. Read LIT-027's model next; it is the most likely route to reconciling LIT-024 with LIT-026.
5. **Treat basis risk as a priced design parameter, not a footnote.** LIT-028 makes it the thing
   that determines whether demand exists at all, and LIT-030 shows it is directly measurable.
6. **Carry the adverse-selection finding into the pool model.** If purchase timing responds to
   private seasonal information, RT-5's loss distribution needs to reflect that.
