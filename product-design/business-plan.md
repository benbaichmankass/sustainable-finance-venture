# Business Plan — Working Draft

**Status:** Draft · **Last updated:** 2026-08-22 · **Owner:** BB

This is the venture-level plan. Individual product lines have their own documents in `product-design/product-lines/`.

It draws on three earlier framings, all archived for lineage:

- `archive/google-drive/sds-work-plan.md` (Nov 2024\) — sustainable development securities; the general thesis  
- `archive/google-drive/bfav-business-plan.md` (Apr 2024\) — agrivoltaic project finance; now Product Line 2  
- `archive/google-drive/web3-vsla-business-plan.md` (Feb 2025\) — Web3/DAO delivery; now Product Line 1

**What carried over, and what did not.** From the Web3 plan: the community-finance core, the pooled-liquidity/structured-product revenue model, the risk-layer positioning, and the insurance expansion path all survive; the blockchain/DAO delivery mechanism does not — smart-contract governance solved a trust problem VSLAs already solve socially, while adding crypto-regulatory and FX risk the venture has no reason to carry. From the SDS plan: the pooling logic (combine assets with uncorrelated idiosyncratic risk across timeline, type and geography), the "design the asset to capture induced growth" principle, and the public-markets distribution ambition carry directly into the securitization design. From BFAV: the whole thing, promoted from a standalone business to a product line.

---

## 1\. Concept

A structuring and verification layer that turns cash flows originated in underfunded sustainable-development sectors into standardized, verifiable, poolable assets that institutional capital can price.

The thesis is that some sustainable-development problems persist not because solutions are absent, but because the market lacks the right financial product design, underwriting logic, distribution mechanism and de-risking structure to channel capital toward them.

**The thesis is layer-agnostic.** It does not say anything about VSLAs specifically. It says that if an asset's cash flows are standardized, verifiable and legally transferable *at origination*, they can be pooled and sold; and that the reason they usually aren't is that nobody designed them that way. That claim applies equally to a community loan book and to a portfolio of solar PPAs — which is why the venture runs more than one product line.

## 2\. Product lines

Tracked in `data/product-lines.csv`.

|  | PL-1 — Community credit & insurance | PL-2 — Agrivoltaic project finance (BFAV) |
| :---- | :---- | :---- |
| Origination layer | VSLAs, MFIs, NGOs, employer networks | Farmers / landholders via our project vehicle |
| Underlying cash flow | Loan repayments, insurance premiums | PPA revenue from the utility |
| Tenor | Months | 15–25 years |
| Counterparty | Many small, socially enforced | One utility, monopsony |
| Hard part | Data capture and standardization | Permitting, offtake terms, concentration |
| Precedent | LIT-004, LIT-006 | LIT-008 |
| Evidence base | Strong (LIT-001/002/003/007) | Thin — no equivalent impact literature yet |
| Document | `product-lines/community-credit-and-insurance.md` | `product-lines/agrivoltaic-project-finance.md` |

**Why they belong together.** Beyond sharing the thesis, they share the *toolkit* — the data schema, underwriting engine, monitoring system and waterfall models in §5 are largely asset-agnostic. Building them twice would be waste.

And they are close to uncorrelated. A community loan book and a portfolio of utility PPAs have almost no shared risk driver: different obligors, different macro exposure, different failure modes. That is exactly the diversification the SDS plan argued for, and neither line achieves it alone — PL-2 in particular is only superficially diversified, since many small projects still face one offtaker and one regulator.

Whether that means they should share a *vehicle* is a separate question — investors and rating agencies generally prefer homogeneous pools, and mixing an unproven asset class with a legible one may contaminate the legible one. **Resolved (OQ-8, 2026-08-02): keep separate homogeneous pools**, and capture the PL-1/PL-2 diversification at the fund/investor level rather than inside one pool.

**Sequencing.** PL-1 leads, because it carries the research programme and the PhD, and because its evidence base is real. PL-2 is closer to revenue and has a cleaner asset, so it may well produce the first pooled structure. They are not competing for the same milestone.

## 3\. Three-layer structure

| Layer | Who | What they do |
| :---- | :---- | :---- |
| **Origination** | PL-1: VSLAs, NGOs, MFIs, employer networks · PL-2: farmers/landholders, EPC subcontractors | KYC, disbursement, collections, claims, construction, local compliance |
| **Risk (our layer)** | Us | Underwriting rules, monitoring dashboards, early-warning systems, risk-sharing/tranching design, first-loss structuring |
| **Product** | Joint | Loans, insurance, bundled products, project equity/debt — priced using origination data |

We sit in the structuring layer deliberately. Regulated entities handle origination, claims, collections and compliance; we are asset-light and do not seek a licence in the first phase.

**Target end state:** investment-grade tranches sellable to institutional investors, with DFI/philanthropic capital absorbing first-loss/junior risk and private capital in mezzanine and senior.

## 4\. Revenue model

1. **Structuring and servicing fees** on pools we assemble and monitor.  
2. **Retained economic interest** in the pools — which is not optional: EU/UK risk-retention rules require the originator/sponsor to hold a minimum economic interest if senior notes are placed with those investors (see `literature/notes/memo-3-securitization-blended-finance.md`).  
3. **Data/analytics licensing** to originators and funders once the underwriting engine has a track record.

The earlier Web3 plan's "non-voting investor in the VSLA" model is preserved in substance by (2): we take return on capital without taking governance control of the group.

## 5\. Theory of the edge

A revenue model says how money arrives. It does not say why anyone cannot simply do
the same thing. This section is the second question, and it is written after the LC-07
and LC-08 literature passes of 2026-08-22, which changed which answers are defensible.

Seven distinct theories of a pricing edge are available. They are not variants of one
idea — they have different mechanisms, different moats, different buyers, and different
things that would kill them.

| # | Theory | The mechanism | What makes it durable |
| :---- | :---- | :---- | :---- |
| 1 | **Borrower-level information** | See data others cannot, select better, compound | Data network effects |
| 2 | **Parameter monopoly** | Know the *correlation structure* of the asset class when nobody else does | The estimation pipeline, not the number |
| 3 | **Standard-setting** | Define the format the asset is described in | Adoption |
| 4 | **Correlation arbitrage** | Buy risk the market haircuts for unknown correlation | Nothing — it is a one-time repricing |
| 5 | **Tranching precision** | Size first-loss tightly, so more of the pool clears as senior | Modelling capability plus track record |
| 6 | **Verification** | Be the party investors trust to attest the data | Institutional trust |
| 7 | **Instrumentation** | Cause the data to exist by supplying the origination protocol | Embeddedness |

### What the evidence says about each

**1. Borrower-level information is the wrong axis.** This is the credit-bureau and
big-tech-lender story and it is the intuitive one. It is also the one this project's own
reading most directly undercuts. **LIT-037** finds that individual lender growth does
*not* predict portfolio deterioration, while **market-level** penetration does — above
roughly 63% annual borrower growth, or active loans above 10% of population. Knowing more
about each borrower does not protect a pool against a market-level factor. An edge built
here would be an edge on the wrong variable.

**2. Parameter monopoly is real but its moat is misidentified.** The standard method for
a portfolio with no observed defaults returns the probability of default as an upper
confidence bound that is *a function of an asset correlation supplied by assumption*
(**LIT-038**). Nobody has estimated that parameter at loan level for this asset class,
and **LIT-041** — the Basel Committee's own validation studies — says you cannot backtest
your way to it either, because correlation defeats the tests. Whoever can defend a number
is the only party who can price a *pool* rather than a loan, which is the difference
between originating and structuring.

The moat, though, is not the number. A PhD publishes it. What is scarce is the **pipeline
that keeps producing it** as markets shift, and the partner relationships that supply the
data. Treat the estimate as a product with a shelf life, not an asset.

**3. Standard-setting is the strongest structural position.** You do not outprice anyone;
you define the format. Whoever writes the data tape becomes the toll booth — the European
DataWarehouse for European ABS, ISDA for derivatives. RT-1 already is this in draft.
Revenue is licensing, certification and verification rather than spread, and the moat is
adoption, not information. Two independent pointers: **LIT-041** endorses data pooling
among small lenders as the fix for thin data, and **LIT-044** observes that adopting a
scorecard is itself the stimulus for better data collection.

**4. Correlation arbitrage probably runs the wrong way.** The trade is: the market applies
a conservative haircut because the correlation is unknown, the truth is lower, you buy
cheap. But the evidence points the other direction at least as often. **LIT-031** shows
the chosen coffee setting is close to a worst case — leaf rust across more than half of
Central America's coffee area at once — and **LIT-036/LIT-037** say pools assembled the
obvious way are *more* correlated than assumed, not less. This theory is listed for
completeness and should not be relied on.

**5. Tranching precision is the direct monetisation of (2).** You price the risk not to
hold it but to cut the waterfall. If sharper correlation knowledge sizes first-loss at 3%
where a conservative assumption says 8%, materially more of the pool clears as senior,
which is where cheap money is. RT-5 exists to do exactly this, and its current honest
output is a sweep rather than a point estimate.

**6. Verification is a services business, and a real one.** The asset is unverifiable to
investors, so pricing requires trust in the data before it requires a model. **LIT-033**
shows the institutional rails already exist in at least one setting — cooperative member
registers obtainable through the union and the government Cooperatives Agency, already
used as a probability sampling frame. Recurring revenue, trust-based moat, no balance
sheet required.

**7. Instrumentation is the theory this project's evidence most supports.** The reason
nobody prices this risk is not that the mathematics is hard. It is that **the data does
not exist**. **LIT-031** describes cooperative internal credit funds as "often informal
and unregulated", names weak accounting as the most commonly observed deficiency, and
discloses no portfolio-at-risk figure anywhere. **LIT-044** adds the sharp version of the
constraint: a judgmental scorecard only *ranks* risk, while only a statistical model
*prices* it — so an originator running the former is not investment-ready however well it
performs.

So the edge is not modelling existing data better. It is being the party that **causes the
data to exist**, by supplying the origination protocol and tooling, and taking data rights
and the structuring mandate in exchange. That is EXP-22 as a business rather than as an
experiment. The analogue is Plaid or a telematics insurer: the moat is embeddedness, not
analytics.

### The stack we should build on

**7 → 3 → 5, with 2 as the research engine underneath.** Cause the data to exist; define
its format; monetise by structuring pools whose senior tranche can be defended. Three
revenue models that reinforce each other, so the business is not a single bet on being
cleverer than the market. Theory 6 is a plausible fourth leg and needs no new capability.
Theories 1 and 4 should be dropped from the pitch.

### Frame the sale as subsidy efficiency, not returns

The buyers who exist today are development-finance institutions and foundations, and they
do not buy "we will beat the market". They buy leverage on scarce concessional capital.

**LIT-031** supplies the template with real numbers: the Coffee Farmer Resilience
Initiative ran USD 400,000 of first-loss capital, described as just under 3% of target
credit disbursements, alongside a 50% pari passu guarantee up to USD 15 million. If
sharper correlation knowledge lets a guarantor cover the same portfolio with materially
less first-loss, the leverage on that concessional dollar rises proportionately.

That proposition is measurable, it is denominated in the units the buyer already uses, and
it does not require anyone to believe a return forecast. It is the strongest available
framing of the edge and it should lead.

### Two things that cut against all of this

**At scale in one market, we become the correlation.** **LIT-037**'s threshold is active
loans above roughly 10% of population. A growth model of "reach scale in a market" would
manufacture the exact risk factor the business claims to price. This is a hard constraint
on the expansion path, not a caveat — it argues for breadth across markets before depth
within one, which is slower and more expensive than the reverse.

**The multi-originator assumption may be diversifying on the wrong axis.** Section 8 of
this plan records "Originator structure: multi-originator, plausibly regional". On
**LIT-036** and **LIT-037**, several lenders inside one market share the factor that
actually causes losses, so a regional multi-originator pool may concentrate risk rather
than spread it. The alternative — genuinely multi-market — is materially harder and slower
to assemble. Logged as **OQ-18** and not resolved here.

### What would falsify the stack

| Theory | Killed by |
| :---- | :---- | 
| 7 Instrumentation | Originators adopt the protocol and then decline to grant data rights, or a funder pays for the tooling directly and commoditises it |
| 3 Standard-setting | A DFI, network body or ratings agency publishes a competing standard first; adoption is winner-take-most |
| 5 Tranching precision | EXP-25 returns a correlation so high, or an interval so wide, that no defensible first-loss saving exists |
| 2 Parameter monopoly | The parameter turns out to be unstable across sites (RQ-28), so no estimate travels and each deal re-estimates from scratch |

EXP-25 is the test that bears on three of the four. That is a further argument for running
it early, and for the respec that separates the institutional correlation channel from the
environmental one — because the two have opposite implications for whether a multi-lender
pool works at all.

## 6\. Toolkit to build

1. Standardized data schema for loans/insurance — ABS-data-tape-ready (→ OQ-3)  
2. Underwriting engine — rules-based plus ML scoring incorporating community signals  
3. Monitoring & early-warning system — DPD tracking, delinquency/claim pattern alerts  
4. Impact evaluation module — randomization infrastructure, pre-registered designs with academic partners  
5. Securitization modelling — cash-flow waterfall models, loss/prepayment simulations

## 7\. Market and pilot direction

**Two candidate first sites.**

- **Israel (migrant-worker communities)** — logistical proximity, easier hands-on project management, existing regulatory environment around foreign-worker insurance. A controlled environment in which to develop the research protocol and tooling.  
- **Africa (multi-country VSLA networks)** — deep traditions of community-based finance, high financial exclusion, alignment with blended-finance/SDG capital mobilization narratives, and a nascent securitization market that offers first-mover advantage in standard-setting.

**Working decision:** anchor methodology development in Israel first, then replicate in an African country as a second field site once the framework is proven. Final decision pending contact/access assessment.

## 8\. Structuring assumptions (evidence-backed)

Derived from the literature review; see Memo 3 for sources.

| Assumption | Working value | Basis |
| :---- | :---- | :---- |
| First-loss / junior tranche size | 10–20% of structure | LIT-013, LIT-015 |
| Pilot warehouse size | Tens of millions USD, DFI-anchored | LIT-011, LIT-012 |
| Public issuance threshold | ≥ USD 100m | LIT-012 |
| Originator structure | Multi-originator, plausibly regional — **contested, see OQ-18** | LIT-008, LIT-011; challenged by LIT-036, LIT-037 |
| Track record before first tranche | 2–3 years of clean repayment data | LIT-004, LIT-006 |

These are starting ranges to be tested, not targets. Each is an observed central tendency across deals that do not closely resemble our asset class.

## 9\. Risks

| Category | Risk | Mitigation |
| :---- | :---- | :---- |
| Market | No investor appetite for a novel asset class at pilot scale | Anchor investor secured before structuring; frame first vehicle as a blended fund, not a public ABS |
| Financial | FX exposure between local-currency receivables and hard-currency notes | Hedging or local-currency tranches; DFI guarantees for FX risk |
| Financial | Interest-rate mismatch across the waterfall | Match funding tenor to asset tenor at structuring |
| Credit | Community portfolios underperform relative to modelled loss curves | First-loss layer; conservative advance rates; early-warning monitoring |
| Credit | **At scale in one market we become the correlation.** LIT-037 finds market penetration above ~10% of population predicts repayment problems, so growth manufactures the risk factor we claim to price | Breadth across markets before depth within one; monitor own share of each market as a risk limit, not a growth metric (→ OQ-18) |
| Model | Claimed conservatism is not actually conservative. SR 11-7 (LIT-042): an extreme point on a misspecified distribution is not a safe estimate, which is exactly the Pluto-Tasche bound on an assumed correlation (LIT-038) | Publish a correlation sweep, never a single conservative point estimate; substantiate any conservatism claim (RT-5) |
| Legal | Cross-border transfer fails a true-sale test in one jurisdiction | Run the LIT-009 six-point checklist with local counsel **before** committing to a geography (→ OQ-1) |
| Regulatory | Origination partner loses licence or falls foul of local rules | Partner diligence; multi-originator structure limits single-partner exposure |
| Operational | Origination data quality too poor to underwrite | Schema and data capture designed at origination, not retrofitted (→ OQ-3) |
| Reputational | Impact claims outrun the evidence base | Frame around resilience/smoothing, which the evidence supports (Memo 2\) |

## 10\. Open work

Tracked in `data/milestones.csv` and `data/open-questions.csv`. The near-term critical path:

1. Draft the canonical data schema (OQ-3) — blocks everything downstream.  
2. Jurisdiction scan with counsel (OQ-1) — blocks pilot site selection.  
3. First originator and verification partner conversations (M-03, M-04). Lead with **EXP-22**, not EXP-25: it asks only for permission to vary a process and observe it, and hands back a costed answer plus a time-and-motion baseline. EXP-25's loan-level data request is a much larger trust ask and should follow the relationship, not open it (M-32).  
4. Choose the first instrument: loan vs insurance vs bundled.  
5. Resolve **OQ-18** — whether the multi-originator structure diversifies on the right axis. It changes how hard the first pool is to assemble.

## 11\. Not yet drafted

Sections carried forward from the earlier plans that still need work, listed so the gaps stay visible:

- Financial plan — cost structure, revenue projections, funding ask  
- Organization & management — team structure, hiring sequence  
- Competitive analysis — who else is structuring community-originated assets  
- Marketing/BD strategy — how originator partners are actually reached  
- Legal structure of the operating company itself

