# Memo 7: Can these cash flows be modelled?

**Status:** Drafted · **Covers:** LC-07 (credit-risk modelling in thin-data settings), LC-08 (portfolio correlation and covariate risk), LC-09 (securitisation eligibility, data tapes and rating criteria) · **Last updated:** 2026-08-22

## Sources

- **LIT-038** — Grigutis 2023, probabilistic overview of Pluto–Tasche for low default portfolios
- **LIT-041** — Basel Committee 2005, *Studies on the Validation of Internal Rating Systems* (WP14)
- **LIT-042** — Federal Reserve & OCC 2011, *Supervisory Guidance on Model Risk Management* (SR 11-7)
- **LIT-043** — Botha & Verster 2025, discrete-time survival analysis for IFRS 9 term-structure PD
- **LIT-044** — DAI/USAID 2006, *A Handbook for Developing Credit Scoring Systems in a Microfinance Context*
- **LIT-036** — Chen, Rasmussen & Reille 2010, *Growth and Vulnerabilities in Microfinance* (CGAP Focus Note 61)
- **LIT-037** — Schicks & Rosenberg 2011, *Too Much Microcredit?* (CGAP Occasional Paper 19)
- **LIT-031** — Root Capital 2016, Coffee Farmer Resilience Initiative learning report
- **LIT-030** — basis risk and spatiotemporal adverse selection in index insurance
- **LIT-016** — MIX / CFI 2019, global microfinance benchmark
- **LIT-004**, **LIT-006**, **LIT-011** — microfinance securitisation precedent and African market depth

---

## 1. The answer, up front

**Yes, but the binding constraint is not the modelling.** Three separate constraints
sit in front of it, in this order:

1. **The data does not exist** in most originators (LIT-031, LIT-044).
2. **The correlation parameter is unknown**, and it is the input that does most of
   the work in every method available (LIT-038, LIT-041).
3. **Validation cannot rescue you** from (2), because correlation defeats the
   statistical tests that would otherwise catch a bad calibration (LIT-041).

The specification question — which hazard model, which link function — turns out to
be the easy part, and is essentially settled (LIT-043). This memo is mostly about
why that is not the reassuring finding it sounds like.

---

## 2. Specification is settled

**LIT-043** does the job LC-07 was written to close. Discrete-time hazard within a
generalised linear model, with the baseline hazard entered explicitly as an input —
the paper flags models that omit it as questionable survival models at all. Logit
and probit are the practical choices; complementary log-log underperforms slightly.
A public R codebase is contributed, and the three credit-specific complications are
handled by name:

- **Competing risks** — a loan may prepay, be written off or restructured, each of
  which precludes default *and* shrinks the risk set.
- **Left-truncation** — described as extensive, especially for longer-dated products.
- **Recurrent default events** — a loan that cures and re-defaults.

The rationale transfers cleanly to our asset class, and it is worth stating exactly
why: *"the underlying data-generating mechanism of credit data is typically discrete
in nature; i.e., interval-censored monthly observations."* A VSLA or cooperative
repayment book **is** a discrete-time process — weekly or monthly instalments — so
discrete-time survival is not an approximation here, it is the natural form.

**What follows for RT-1.** The specification imposes field requirements. A single
default flag is insufficient; the schema needs an **event type** distinguishing
default, prepayment, write-off and restructure, plus origination date and censoring
status. That has been recorded against RT-1 and belongs in EXP-22's protocol.

**What LIT-043 does not give us.** It is a 90,000-account mortgage panel at a large
bank. Long-dated, collateralised, individually underwritten, rich MIS — almost every
property is the opposite of ours. The method transfers; the parameters and the
diagnostic experience do not. It offers no small-sample corrections, which is
precisely LC-07's third question.

---

## 3. The correlation parameter is where the uncertainty concentrates

This is the memo's central finding, and it arrived by three independent routes that
did not start out looking related.

**Route one — the method takes it as an input.** For a portfolio with zero or very
few observed defaults, the standard approach is Pluto–Tasche (LIT-038): estimate the
probability of default as an *upper confidence bound*. Two estimators are available,
one assuming obligor independence, one assuming conditional independence given a
systematic factor. In the second, the default event is a threshold crossing of
`√ϱ·S + √(1−ϱ)·ξ`, the loss distribution is Vasicek, and **ϱ — the asset correlation
— is supplied by assumption, not estimated from the data.** In a thin-data portfolio
that assumption is doing most of the work.

**Route two — the historical record says the correlation is large, and not where
you would look for it.** LIT-036 studies four national repayment crises (Nicaragua,
Morocco, Bosnia, Pakistan). Portfolio-at-risk over 30 days exceeded 10% in three of
the four by June 2009; Nicaragua's crisis affected *all 22 major MFIs*; Bosnia's
nearly all 12 largest. And the report **explicitly rejects the macroeconomy** as the
cause — the MIX median PAR rose only to about 3%, "mild compared to the delinquency
crises in our four countries", and most managers interviewed did not name the global
crisis. The named drivers are concentrated market competition, multiple borrowing
and erosion of lending discipline. Contagion is a mechanism with a boundary: mobile
phones and social networks escalated a local Punjab problem into a regional one, and
the same networks stopped it reaching rural areas.

LIT-037 sharpens this into a level-of-analysis result that should change how a pool
is assembled: **individual MFI growth does not predict portfolio deterioration**
except at extreme levels, but **market-level** borrower growth above ~63% a year and
active loans above ~10% of population **do**.

So the correlation channel that matters historically is *institutional and
market-level*. Geographic diversification does not address it. Pooling several
lenders within one market may concentrate it.

**Route three — the regulator says you cannot backtest around it.** LIT-041 is the
sharpest statement of the bind, and it is the Basel Committee's own:

> "A major obstacle to backtesting of PDs is the scarcity of data, caused by the
> infrequency of default events and the impact of default correlation. Even if the
> final minimum requirements... for the length of time series for PDs (five years)
> are met, the explanatory power of statistical tests will still be limited."

The mechanism is spelt out. Because defaults are correlated, observed default rates
systematically exceed critical values computed under independence — so tests built
on independence are so conservative that **well-calibrated systems fail them**,
while tests that *do* model correlation "will only allow the detection of relatively
obvious cases of miscalibration." The conclusion: *"statistical tests alone will be
insufficient to adequately validate an internal rating system."* Benchmarking against
external estimates is a required complement, explicitly "a complement to, not a
substitute for" statistical methods.

**Correlation does not merely widen the estimate. It breaks the validation.**

Set against all of this, LIT-031 supplies the environmental channel in the setting
now chosen: leaf rust across more than half of Central America's coffee area at once,
El Salvador output down 60% in 2013/14, 80% production drops at some financed
producer organisations. LIT-030 adds basis risk and spatiotemporal adverse selection
on the insurance side.

**Two channels, both live, and separable.** That separation is what EXP-25 was
respecced to deliver, and it is why the design needs at least two lenders per market
and at least two markets — with one lender the institutional channel is unidentified
and a near-zero estimate would be an artefact of the design.

---

## 4. Loss given default: a named menu, and the retail route inherits everything

LIT-041 is candid that *"much less is known about what drives LGD"* than PD, and that
a **qualitative** assessment of the estimation process may be more meaningful than
quantitative validation. Four routes:

| Route | Basis | Applies to |
|---|---|---|
| Workout LGD | Discounted cash flows after default | The common IRB choice |
| Market LGD | Prices of traded defaulted loans | Large corporate |
| Implied market LGD | Non-defaulted bond prices via an asset-pricing model | Where a bond market exists |
| **Implied historical LGD** | **Total loss experience plus PD estimates** | **Retail portfolios — ours** |

The retail route is the only one available to us, and it comes with a catch stated
plainly: *"the validation of implied historical LGDs relies essentially on the
validation of the PDs used in this method."* It does not sidestep the PD uncertainty;
it inherits all of it. Given §3, that means LGD inherits the correlation problem too.

On incomplete workouts — loans still in recovery — LIT-041 notes they are frequently
excluded from the reference data set, that banks apply a recovery threshold (the
example given is remaining unrecovered value below 5% of exposure) or a time
threshold such as one year from default, and that *"if the definition results in the
exclusion of many defaulted facilities from the LGD estimates, the treatment of
incomplete workouts must be revised."* For a short-tenor community loan book with a
young panel, that exclusion could be most of the data.

**This remains LC-07's weakest area.** LGD with few observed recoveries is unresolved
here and is one of the two remaining gaps.

---

## 5. Model risk: a warning aimed at our own method

LIT-042 (SR 11-7) supplies the disclosure standard, and one paragraph lands directly
on the approach §3 describes:

> "simply picking an extreme point on a given modeled distribution may not be
> conservative if the distribution was misestimated or misspecified in the first
> place. Furthermore, initially conservative assumptions may not remain conservative
> over time."

Banks are required to *"justify and substantiate claims that model outputs are
conservative."*

The Pluto–Tasche upper confidence bound is exactly an extreme point on a distribution
whose correlation parameter is assumed. **It looks conservative and may not be.**
Wherever this project uses that bound it has to say so.

This is why RT-5's correlation sweep — from independence to near-perfect correlation,
reporting the range — is the honest output rather than a placeholder. It claims no
conservative point estimate, so it makes no claim it cannot substantiate. Keep it
that way until EXP-25 supplies a measured range.

The guidance's other structural point deserves attention for the venture, not just
the model: **effective challenge** requires critical analysis by parties separated
from the developer. A model built and validated by the same entity that originates
the assets is precisely the arrangement SR 11-7 is written against. That is a
governance question for the business, and it argues for external validation as a
design feature rather than a later concession.

---

## 6. The practitioner constraint: ranking is not pricing

LIT-044 supplies the distinction that most sharpens the venture's problem, and it is
not a modelling point at all:

> A statistical model "predicts the probability of default for an individual
> borrower... this degree of precision makes it the most powerful scorecard type for
> risk management, pricing and provisioning." Judgmental and hybrid scorecards only
> **rank** relative risk.

An originator running a judgmental scorecard is not investment-ready however well it
performs, because a ranking cannot price a pool. **Closing the gap between ranking
and pricing is the work.**

The handbook's practical route is a phased progression — the Credit Indemnity case
runs paper-based judgmental, then system-driven judgmental, then statistical
behavioural, then collections — with the observation that matters here: *"Use of
scorecards can be a stimulus for improving data collection and data management."*
BancoSol hired dedicated staff to key in historical data over two months in order to
develop a statistical model at all.

That is EXP-22's argument arriving from practice: the protocol comes first and the
model becomes possible later.

---

## 7. What the securitisation side requires (LC-09, thin)

LC-09 is at three anchors of ten and this section is correspondingly provisional.

LIT-006 supplies the structural template — an SPV buys receivables from the MFI and
tranches by risk, with the senior/junior split improving the senior rating. LIT-004
shows African precedent exists but "requires scale, standardized data, legal and
ratings infrastructure." LIT-011 is the sober one: several African countries have
securitisation frameworks, but deal flow is thin, and closed deals have involved
*relatively large, standardised portfolios with strong sponsor or DFI involvement*
against a shallow institutional investor base and limited rating-agency coverage.

LIT-016 gives the only sector-wide performance baseline on file: global yield on
gross loan portfolio 19.2%, operating expense ratio 10.6%, PAR30 6.0%, cost per
borrower about USD 87 (FY2017) — and it is the last comprehensive MIX benchmark
edition, so it is both the best available reference and an ageing one.

**Unanswered and important:** what correlation assumption a rating agency actually
applies to an emerging-market consumer pool. That is LC-08's fourth question, it is
unanswered, and it determines whether a measured correlation would even change the
tranching outcome.

---

## 8. What this memo cannot yet say

Stated as gaps rather than hedged prose, because the design decisions downstream
depend on knowing where the evidence is thin:

1. **Small-sample and short-panel corrections.** LC-07's third question. Nothing on
   file addresses it. LIT-043 is a large-data setting; LIT-038 gives a bound but not
   a correction.
2. **LGD with few observed recoveries.** §4. The retail route is named and its
   dependency exposed, but no method for estimating it on a young book is anchored.
3. **Rating-agency correlation assumptions** for EM consumer pools. §7.
4. **Any published loss data on cooperative internal credit funds.** LIT-031
   discloses none, and on that evidence it may not exist publicly at all — which is
   itself a finding, and part of the argument for EXP-25.

LC-07 stands at five anchors of ten, LC-08 at six of eight, LC-09 at three of ten.

---

## 9. Consequences already recorded elsewhere

So this memo does not become the only place these live:

- **EXP-25** respecced to a variance decomposition separating the institutional from
  the environmental channel, needing two lenders per market and two markets
  (`docs/research/experiments/exp-25-default-correlation.md`).
- **RT-1** gains the event-type field requirement from §2.
- **RT-5** keeps the correlation sweep and the no-point-estimate discipline from §5.
- **OQ-17** — §3 strengthens candidate relocation (b), now with regulatory backing.
- **OQ-18** — §3's market-level finding is what puts the business plan's
  "multi-originator, plausibly regional" assumption in question.
