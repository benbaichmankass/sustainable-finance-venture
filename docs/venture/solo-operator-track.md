# Solo Operator Track — Product Design and Arranging, Without the PhD

**Status:** Option under evaluation, not a decision · **Owner:** BB · **Drafted:** 2026-09-08 · **Decision:** OQ-19

> **Scope correction, 2026-09-09.** This document was written with the repo's research apparatus attached. The business scoping — where to play, who it reaches, and what the first pilots are — is now in [market-scan-and-pilots.md](http://market-scan-and-pilots.md). What survives here: the revenue lanes, the data-rights clause, and the blocking decisions. What is parked: the experimental designs. Read the market scan first.

This document answers a specific question put to the project on 2026-09-08:

> If the PhD track is dropped for now, and the business focuses on **designing financial products and building the partnerships between investors and the organisations that distribute them** — non-capital-intensive, solo, no hiring — what does the business plan, the work plan, the partnership map, the pilot portfolio and the research collaboration look like?

It is written as a **live alternative** to the configuration in product-design/business-plan.md, not as a replacement for it. The thesis does not change. The *layer we occupy*, the *revenue sequencing* and the *role in the research* all do. Nothing in business-plan.md has been edited; §10 of this document lists exactly what would change there if OQ-19 resolves this way.

---

## 1\. The short version

The existing plan puts us in the **structuring layer** with an end state of investment-grade tranches (business-plan.md §3). That is a capital-markets business. It needs a pool, an SPV, counsel, a rating conversation, and — because EU/UK risk-retention rules bite on a sponsor — a retained economic interest, which is balance sheet (business-plan.md §4.2, MEMO-3).

The solo track puts us one step earlier, in the **design and arranging layer**: we design the product, we specify how it is originated and monitored, we assemble the counterparties, and somebody else carries it. That is a services business. It has no pool, no SPV of our own, no retention requirement, and it can bill in month three.

**The key finding of this document is that this is not a downgrade of the thesis. It is the subset of the thesis a solo operator can actually own.** §2 shows why, using the project's own analysis.

---

## 2\. What survives the move, and what does not

business-plan.md §5 sets out seven theories of a pricing edge and concludes the stack should be **7 → 3 → 5, with 2 as the research engine underneath**. Re-read that table against a one-person, no-balance-sheet practice:

| \# | Theory | Survives solo? | Why |
| :---- | :---- | :---- | :---- |
| **7** | **Instrumentation** — cause the data to exist by supplying the origination protocol | **Yes, fully** | This *is* a services business already. RT-1 is the product; EXP-22 is the engagement. No capital required. |
| **3** | **Standard-setting** — define the format the asset is described in | **Yes, fully** | Adoption is the moat, and adoption is won by publishing and being early, not by deploying capital. Being small is not a disadvantage here; being late is. |
| **6** | **Verification** — be the party investors trust to attest the data | **Yes** | business-plan.md already notes this "needs no new capability" and requires no balance sheet. Recurring revenue. |
| **2** | **Parameter monopoly** — know the correlation structure | **Partly — only through a research partner** | The estimate itself (EXP-25) needs econometric capacity, data access and publication credibility. See §7: this is exactly what the PhD was buying, and it has to be re-bought some other way. |
| **5** | **Tranching precision** — size first-loss tightly | **No** | You have to be structuring the pool to monetise this. It comes back at deal 3–4 (§4), not at the start. |
| 1 | Borrower-level information | Already dropped | business-plan.md §5 drops it on LIT-037. |
| 4 | Correlation arbitrage | Already dropped | Same. |

So the solo track keeps **7, 3 and 6** — the three legs that are services, standards and trust — and defers **5** while making **2** conditional on a research partnership. The project's own reading already concluded that 7 is "the theory this project's evidence most supports" and that 6 needs no new capability. The solo configuration is therefore aligned with the evidence, not a compromise against it.

**Two concrete consequences worth stating plainly:**

1. **Risk retention stops being mandatory.** business-plan.md §4 says retained economic interest "is not optional" because EU/UK rules require a sponsor/originator to hold a minimum economic interest when senior notes are placed with those investors. That obligation attaches to *being the sponsor of a securitisation*. A design-and-arranging practice that stops short of sponsoring one does not trigger it. This removes the only balance-sheet requirement in the current plan — which is precisely the "not capital intensive" constraint being asked for. *(This is a structural reading of the rule as recorded in MEMO-3, not counsel's advice. Confirm with PT-09 alongside OQ-1 before relying on it.)*  
     
2. **The research question stops being ours to answer alone.** EXP-25 does not disappear; the PI does. §7 deals with this.

---

## 3\. The business model

### 3.1 What is actually sold

Three sellable things, all already built or half-built in this repo:

| Sold thing | Repo asset it is made of | Buyer |
| :---- | :---- | :---- |
| **Investment-readiness diagnostic** — "here is what it would cost your book to become investable, field by field" | RT-1 schema \+ validate\_schema.py \+ EXP-22's activity-based costing method | Originators (MFIs, co-op unions, VSLA networks) and the funders who want their grantees investable |
| **Product design mandate** — design a credit / insurance / bundled product and the facility that funds it | product-lines/, RT-2 underwriting engine, RT-3 monitor, RT-5 waterfall, RT-6 economics | DFIs, foundations, TA facilities, insurers entering a segment |
| **Arranging** — assemble originator \+ capital \+ risk carrier \+ verification into a closed facility | The whole toolkit plus relationships | The originator or the funder (see §3.3 on who may pay) |

The distinctive claim is narrow and defensible: **most parties in this market can tell an originator that it is not investable. Very few can tell it what specifically to change, price the change, and then bring the money that is unlocked by making it.** That is the offer.

### 3.2 Revenue lanes and their sequencing

The classic failure of an arranging practice is that arrangement fees only land when a deal closes, and these deals take 18–36 months. The plan must therefore front-load fee-for-service.

| Lane | What | When it pays | Notes |
| :---- | :---- | :---- | :---- |
| **A — Diagnostics** | Fixed-fee readiness assessments and schema/data-tape work | Months 3–6 onward | Small tickets, fast, repeatable. This is the cash floor. It is also how RT-1 gets field-tested for free. |
| **B — Funder-paid design mandates** | A DFI, foundation or TA facility pays to design a product or facility it intends to fund | Months 4–12 onward | Highest value early revenue. Facilities of exactly this shape exist (FSD Africa, ILO Impact Insurance Facility, Convergence design funding, Aceli Africa). |
| **C — Arranging / success fees** | Retainer plus success fee on a closed facility | Months 12–36 | The real business. Retainer matters: it converts an 18-month sales cycle into billable months. |
| **D — Licensing and certification** | RT-1 as a published standard; RT-2/RT-3 as tooling; verification/attestation subscriptions | Year 2+ | This is theory 3 and theory 6 monetised. Requires the standard to have been adopted first, which requires it to have been given away first. |

**Sequence: A funds B, B funds the wait for C, C funds D.** Do not attempt C first; it is the lane with the longest cycle and the highest regulatory exposure.

### 3.3 The regulatory perimeter — the one thing that can bite

**Introducing investors to issuers for a fee is a regulated activity in most jurisdictions** (arranging, or broker-dealer activity, depending on where). A solo unlicensed operator taking a placement fee from the capital side is the configuration most likely to be a problem.

Three ways to stay clear, in order of preference:

1. **Bill the originator or the funder for design and advisory work, not the investor for placement.** The economic result is similar; the characterisation is different.  
2. **Take success fees as an uplift on an advisory mandate** with the client who engaged you, not as a commission on capital raised.  
3. **Work as an appointed representative of, or in a co-mandate with, a licensed arranger** for any transaction where fee 1 and 2 do not work.

This is **OQ-20**, and it is a first-30-days question because it determines how every engagement letter is written. It is cheap to answer — it is a scoping call with the same counsel already needed for OQ-1 (PT-09).

### 3.4 Cost base — testing the "not capital intensive" claim

| Cost | Nature |
| :---- | :---- |
| Entity, accounting, professional indemnity insurance | Fixed, small. **PI insurance is not optional** for a practice giving financial product design advice — it is the one line people forget. |
| Counsel — perimeter (OQ-20) and jurisdiction scan (OQ-1) | Lumpy, project-triggered. Recoverable from Lane B mandates. |
| Travel to originator sites | The real variable cost, and the reason for one-market focus (§6.1). |
| Subcontractors — local counsel, field enumerators, a statistician for EXP-25 | Engagement-funded, never on payroll. |
| Toolkit maintenance | Already sunk. RT-1…RT-6 exist. |

The RT-6 model carries an **\[assumed\]** \~USD 250k fixed structuring cost per deal. That is the cost of standing up a *securitisation SPV*, and in the solo track **it is the client's cost, not ours** — or it does not arise at all, because deal 1 is not a securitisation (§4). Removing that line is most of what makes the solo configuration light.

### 3.5 What "solo" actually constrains

Not money — **calendar**. One person can hold roughly two to three concurrent client engagements plus one live pilot, and no more. Every decision below is downstream of that number. Two implications:

- **The toolkit is the leverage.** RT-1…RT-6 exist precisely so one person can deliver what would otherwise take an analyst team. Any engagement that cannot be run through the toolkit should be declined, not accepted and improvised.  
- **Subcontract, don't hire.** Local counsel, enumerators, an econometrician: engaged per project, paid from the engagement. This keeps the fixed cost base near zero and is what "no hiring" should mean in practice.

---

## 4\. The first deal must not be a securitisation

This follows from the project's own model and is the most load-bearing structural conclusion here.

**RT-5's sweep already found that fixed costs dominate the junior tranche below roughly USD 5m of pool and flatten only around USD 20–40m** (data/risk-tools.csv, RT-5; this is the derived answer to OQ-2). A solo operator will not assemble a USD 20–40m pool as a first transaction. So a securitisation as deal 1 is arithmetically the wrong instrument, independent of skill or effort.

The smallest structure that proves the same capability, without the fixed-cost floor:

> **A guarantee-wrapped or first-loss-wrapped bilateral lending facility.** One investor lends to one originator against a portfolio that is originated to our schema and monitored with our tools, with a concessional guarantee or first-loss layer sized against RT-5's output.

It carries the same design work, the same data rails, and the same verification role. It has no SPV, no true-sale opinion, no rating, no risk retention, and no minimum pool size. LIT-031's Coffee Farmer Resilience Initiative is exactly this shape at real scale — USD 400,000 of first-loss described as just under 3% of target credit disbursements, alongside a 50% pari passu guarantee up to USD 15m — which means the template is not hypothetical.

**Progression:** bilateral guaranteed facility (deal 1\) → club facility with two or three lenders (deal 2\) → warehouse (deal 3\) → securitisation (deal 4+, and only once there is the 2–3 years of clean repayment data that LIT-004/LIT-006 say is the precondition anyway). Theory 5 comes back at deal 3\.

---

## 5\. Pilots

Three tiers, distinguished by **who pays** — which is the only distinction that matters at solo scale.

### 5.1 Tier 1 — the commercial pilot (self-funding): EXP-22

**Run EXP-22 as a paid engagement, not as a research experiment.** It is already specified (docs/research/experiments/exp-22-\*.md) and it is a near-perfect fit for Lane A:

- The ask of the partner is minimal — permission to vary a process and observe it. No historical data disclosure. M-32 already identified this as the right opening ask.  
- The deliverable is immediately useful to the originator: a costed answer to what it would take for their book to be investable, a validated field list, and a time-and-motion baseline of their own origination that most originators do not have.  
- It field-tests RT-1 and moves the schema from v0.1 to v1.0 (data/risk-tools.csv, RT-1).  
- It produces the **ranked per-field cost curve**, which is what lets originators adopt the standard incrementally — the adoption mechanism for theory 3\.

Screen candidates for **cluster count before enthusiasm** (10–40 branches; it is the binding design constraint, per the EXP-22 spec) and remember it needs HR or staff-representation approval for officer time measurement.

Target: **one paid EXP-22 engagement closed by month 6, two more by month 12\.** Three of these is a body of comparative evidence nobody else has.

### 5.2 Tier 2 — the structuring pilot (fee-earning): the first guaranteed facility

Per §4. Target: **term sheet by month 12, close by month 18–24.** The originator should ideally be one whose book you already diagnosed under Tier 1 — because the diagnostic is what makes the facility financeable, and the sequence originator-diagnostic-then-facility is the practice's whole value proposition demonstrated end to end.

### 5.3 Tier 3 — the impact pilot (grant-funded, partner-run): the coffee anchor

EXP-09 (pre-harvest credit with a climate trigger and price floor) or EXP-10 (an index calibrated to leaf rust and heat stress) — the instrument choice is still open as OQ-16 / M-33.

**Change the role, not the experiment.** In the PhD configuration you were the principal investigator. In the solo configuration you are the **product designer and the data-rails partner on someone else's trial**: an academic partner is PI, holds the grant, holds ethics approval and publishes; you design the instrument, supply RT-1/RT-2/RT-3, and co-author. You are not paying for a multi-year randomised trial out of an advisory practice's cash flow, and you should not try.

**EXP-25 sits across tiers 1 and 3\.** It needs no field money at all — it needs pseudonymised loan-level panels from **two lenders in the same market, covering a window that contains a shock** (M-32). Tier 1 relationships are how you get that data; a Tier 3 research partner is how you analyse and publish it. Screen any offered dataset for a shock in the window *before* accepting it: a quiet panel produces a falsely reassuring near-zero covariate component, which is the most dangerous failure mode here because it looks like success.

---

## 6\. Partnerships

### 6.1 The shape of the map: depth in one market first

business-plan.md §9 records a real constraint — at scale in one market you *become* the correlation, because LIT-037 finds market penetration above roughly 10% of population predicts repayment problems. That argues for breadth across markets before depth within one.

**At solo scale that constraint does not bind for years.** A one-person practice will not approach 10% of any market's population. Meanwhile three things all argue for concentrating on one market first: travel cost is the main variable expense; EXP-25 *requires* two lenders in the same market; and a club facility (§4, deal 2\) needs several originators who share a jurisdiction and a legal opinion. So: **depth in one market now, breadth later, with own-market share tracked as a risk limit rather than a growth metric** — which is what §9 asks for anyway. The switch point is when the practice's aggregate originator book approaches a material share of the market, and it should be written into the plan as a limit before it is ever approached.

### 6.2 Four classes of partner

**Class 1 — Origination / distribution.** The organisations that actually manage distribution. Existing rows: PT-01, PT-02, PT-03. Added for this track: SEEP Network (PT-11) as the savings-group standards and practitioner network; coffee cooperative unions and producer federations (PT-12), which is the anchor setting and had no tracker row; and SME / business membership associations (PT-13), which the brief explicitly names and which are a genuinely distinct origination channel from VSLAs — larger tickets, existing member registers, weaker social enforcement.

*Target: 3–5 in one market, not 1 in each of 5 markets.*

**Class 2 — Capital.** The half of the map the tracker was thinnest on. Existing: PT-07 (DFI blended desks), PT-08 (impact asset managers). Added: Aceli Africa (PT-14), which pays origination incentives on small agricultural loans and therefore directly changes whether the originator economics clear at all; Convergence (PT-15) for blended design funding and precedent deal data; Incofin (PT-16) as a plausible first-facility lender in agri and cooperative finance.

**Class 3 — Risk carriers.** *Structurally required and previously absent.* A design practice cannot underwrite insurance; any insurance product line needs a licensed paper provider or a parametric underwriter. Added: Pula (PT-17) as an agricultural parametric underwriter/distributor. Without a Class 3 partner, PL-1's insurance half is undeliverable regardless of design quality.

**Class 4 — Standards, TA and mandate sources.** These are simultaneously the theory-3 adoption allies and the source of Lane B revenue. Existing: PT-04 (CGAP), PT-10 (FinDev/World Bank). Added: ILO Impact Insurance Facility (PT-18) and Microinsurance Network (PT-19). FSD Africa is already tracked as FUND-04 and belongs in both roles.

**Class 5 — Research.** Section 7\.

### 6.3 The order of approach

1. **Class 4 first.** They cost nothing to talk to, they give you the market map, they make introductions, and they are where Lane B money is. They are also the cheapest place to test whether the offer in §3.1 lands.  
2. **Class 1 second**, led with EXP-22 (the small ask), never with a pilot proposal or a data request. This is M-32's own sequencing finding and it holds exactly as well in the solo track.  
3. **Class 5 in parallel** with 1 — because the research MOU takes months and gates nothing else.  
4. **Class 2 and 3 last**, once there is a diagnosed originator and a designed product to bring them. Approaching capital before there is an asset to point at spends the relationship.

---

## 7\. Research collaborations — what the PhD was buying, and how to re-buy it

Be precise about what is actually lost. The PhD was buying five things:

| What the PhD supplied | Available without it? |
| :---- | :---- |
| A funded 3–4 year runway to produce the correlation estimate (theory 2\) | No — replaced by partner-funded research |
| **Principal-investigator eligibility on most research grants** | **No** — must come from an academic partner |
| **Ethics / IRB approval for evaluations involving human subjects** | **No** — a solo company cannot self-approve; must come from an institution |
| Credibility with DFIs and academic collaborators | Partly — replaceable by published work plus a track record, more slowly |
| A structural obligation to finish the correlation work | No — this is the one that quietly disappears, and it is the one to be honest about |

The middle two are not preferences. **If independent impact validation is part of the value proposition — and §3.1 says verification is one of three revenue legs — then an institutional research relationship is structurally required, not a nice-to-have.** That is the strongest single argument for taking §7 seriously rather than treating it as an afterthought. Logged as **OQ-21**.

### 7.1 Three workable forms

**Form 1 — Data-brokerage partnership (start here; this is EXP-25).** The trade is clean and it is genuinely two-sided: **academics struggle to get lender data; you will have it.** You broker pseudonymised loan-level access from Tier 1 relationships; they bring the econometrics, the ethics approval and the publication. Output is a joint working paper, and the paper *is* the marketing for theories 2 and 3\. Note the offer already built into the EXP-25 ask — every participating lender gets its own variance decomposition back, a number none of them currently has about their own book.

*Best fits:* credit-risk and development-economics groups. IPA (PT-20) and CEGA (PT-21) both run exactly this kind of administrative-data partnership; the World Bank's DIME (PT-23) does it at scale and publishes openly; J-PAL (PT-05) is already tracked.

**Form 2 — Embedded evaluation on a live product (this is Tier 3).** A pre-registered evaluation running alongside a real facility, funded by a research grant rather than by the practice. The IGC (PT-22 / FUND-11) is the most solo-compatible entry point in this class: small, fast-turnaround, country-office-based, explicitly for policy-relevant work with local partners, and it does not require the applicant to be a tenured PI in the way a large trial grant does. 3ie (FUND-02) and J-PAL K-CAI (FUND-03) are the larger, slower versions.

**Form 3 — Practitioner affiliation.** A research-affiliate, practitioner-fellow or visiting-practitioner arrangement with one department. This is the cheapest route to IRB access, library access and co-author standing, and it does not require enrolment. It is also the honest bridge back: it keeps a **part-time or industrial PhD, or a later PhD by publication built on the EXP-25 paper**, available as an option rather than a door closed. Recommendation: **do not frame this as dropping the PhD. Frame it as deferring enrolment while keeping the research relationship** — it costs nothing to keep open and it changes how academics respond to a first approach.

### 7.2 What to offer a research partner

Lead with what is scarce on their side, not what is impressive on yours:

1. **Data access they cannot get** — administrative loan panels via originator relationships.  
2. **A live product to evaluate**, with real allocation decisions to randomise around, rather than a hypothetical.  
3. **Instrumentation already built** — RT-1 capture, RT-3 monitoring, RT-4's pre-registration design. Most field partners cannot supply clean measurement infrastructure; you can.  
4. **A pre-registered design**, offered up front. Offering to pre-register before anyone asks is the single strongest credibility signal a commercial party can send an academic, because the default assumption is that you will want to choose the estimator after seeing the outcomes.

---

## 8\. Work plan

### Days 1–30 — decide, define, and clear the legal question

1. **Resolve OQ-20 (regulatory perimeter)** with counsel — one scoping call, bundled with the OQ-1 jurisdiction scan (PT-09). Everything about how engagements are papered depends on it.  
2. **Choose the market** (OQ-19's sub-decision). The Israel-vs-Africa working decision in business-plan.md §7 was made for a research-first configuration and should be re-taken on commercial criteria: where are there originators with 10–40 branches, two lenders in one market for EXP-25, and a live TA facility paying for design work?  
3. **Write the offer.** Two pages per Lane A and Lane B service: scope, deliverable, timeline, fee basis. Not a pitch deck — a scope of work a buyer can sign.  
4. **Package the toolkit as a client deliverable.** RT-1 \+ validate\_schema.py \+ the RT-2 scorecard, presented as a readiness assessment output rather than as a repo.  
5. **Set up:** entity, PI insurance, engagement-letter template.

### Days 31–60 — outreach wave 1

6. **Class 4 (standards / TA), 6–8 approaches.** Ask for the market map and for whether they fund design work. Do not pitch.  
7. **Class 1 (originators), 12–15 approaches**, led with the EXP-22 diagnostic as a paid or part-funded engagement. Screen for cluster count first.  
8. **Class 5 (research), 4–5 approaches**, offering §7.2's four things. Ask for Form 1 or Form 3; do not open with a grant proposal.  
9. Log every contact through the partner-outreach skill into private/partner-contacts.csv.

### Days 61–90 — convert

10. **Close one paid Tier 1 engagement.** This is the single hard success criterion for the quarter.  
11. **One Lane B mandate conversation** at proposal stage.  
12. **One research MOU or affiliation conversation** at term-sheet stage.  
13. **Re-run RT-6** with the two stubborn drivers replaced by real numbers from the engagement and from counsel (M-24) — fixed structuring cost, and the origination layer's share of the spread.

### Months 4–9 — deliver and publish

14. Run engagement 1; produce the per-field cost curve; **move RT-1 to v1.0**.  
15. **Publish RT-1 v1.0 openly**, with the cost curve. This is the theory-3 move and it only works if given away. Being first matters more than being complete.  
16. Begin design of the first guaranteed facility (§4) with the diagnosed originator.  
17. With the research partner, negotiate loan-level data access for EXP-25 — two lenders, one market, shock in the window.

### Months 10–18 — the first structure and the first paper

18. Term sheet on the guaranteed facility; Class 2 and 3 partners engaged.  
19. Submit an IGC or 3ie application **with the academic partner as PI**.  
20. EXP-25 analysis; working paper drafted.  
21. Engagements 2 and 3 running; Lane A now recurring.

**The two things that indicate this is working at month 12:** someone has paid a real fee for a diagnostic, and a research institution has signed something. If neither has happened, the model is wrong, not merely slow.

---

## 9\. Risks, and what would kill it

| Risk | Why it bites here specifically | Mitigation |
| :---- | :---- | :---- |
| **Revenue arrives later than the cash floor** | Lane C is 18–36 months; Lane A tickets are small | Retainers on Lane B mandates; do not start Lane C first |
| **Regulatory perimeter breach on arranging fees** | A solo unlicensed operator taking placement fees from the capital side | OQ-20 in the first 30 days; bill the originator/funder side |
| **The single-person bottleneck** | Two to three concurrent engagements is a hard ceiling | Toolkit leverage; decline non-toolkit work; subcontract |
| **Key-person risk is the whole business** | Investors will not commit to a facility whose arranger is one person with no succession | Publish the standard and the tools openly, so the method outlives the person — which also happens to be theory 3 |
| **Standards race lost** | business-plan.md §5: a DFI or ratings agency publishes a competing standard first; adoption is winner-take-most | Publish RT-1 early and openly; this is the argument for step 15 |
| **Research partner never materialises** | Without one there is no IRB, no PI, no impact validation — one of three revenue legs fails | Approach 4–5 in parallel from day 31; Form 3 affiliation is the low-cost fallback |
| **Concessional capital contraction** | Lane B and the first-loss layer both depend on DFI and philanthropic budgets | Track against data/macro-indicators.csv; keep Lane A (originator-paid) as the lane that does not depend on aid budgets |
| **Impact claims outrun the evidence** | Sharper here than in the PhD track — a commercial party making impact claims without an independent evaluator is the classic failure | Frame around resilience and smoothing, which MEMO-2 supports; never claim what the evaluation has not returned |

**What would falsify this configuration specifically** (distinct from the thesis falsifiers in business-plan.md §5):

- **No originator will pay for a diagnostic.** If readiness assessment is valued at zero, Lane A does not exist and the cash floor collapses. This is testable in 90 days and cheaply — which is the main argument for running the outreach wave before committing to anything else.  
- **Funders want implementation, not design.** If TA facilities only fund parties who deliver, an arranging-only practice has no Lane B.  
- **Arranging requires a licence in every market that matters.** Then the model is advisory-only, and Lane C never opens.

---

## 10\. What would change in the repo if OQ-19 resolves this way

Nothing has been edited yet. If this track is chosen:

| File | Change |
| :---- | :---- |
| product-design/business-plan.md §3 | Three-layer table: our layer becomes "design and arranging", not "risk/structuring". Structuring returns at deal 3\. |
| product-design/business-plan.md §4 | Retained economic interest moves from "not optional" to "not applicable until we sponsor a securitisation". Advisory and design fees become revenue line 1\. |
| product-design/business-plan.md §5 | The stack becomes **7 → 3 → 6, with 5 deferred and 2 outsourced to a research partner**. |
| product-design/business-plan.md §7 | Site decision re-taken on commercial criteria (§8.2 above). |
| product-design/business-plan.md §11 | Financial plan, org/management and BD strategy are substantially answered by §3 and §8 here; competitive analysis and operating-company legal structure remain genuinely open. |
| product-design/business-economics.md | RT-6 is modelling the wrong entity for deal 1\. Needs a services-P\&L variant: utilisation, day rate, engagement mix, and no per-deal SPV cost. |
| data/milestones.csv | M-06, M-11, M-29 (PhD outreach and applications) go to Blocked or Dropped, not deleted. M-36…M-40 activate. |
| data/open-questions.csv | OQ-14 (which RQ strand leads the proposal) and OQ-17 (the novelty claim) stop being critical-path; they become research-partner questions. |
| docs/phd/ | Retained intact. Nothing here forecloses re-entry, and §7.3 argues actively for keeping it open. |

---

## 11\. The decision this document asks for

**OQ-19 — operating model.** Three options, not two:

- **(a) Structurer** — the current business-plan.md. Highest ceiling, needs capital and a team, slowest to first revenue.  
- **(b) Designer-arranger** — this document. Fastest to revenue, solo-compatible, gives up theory 5 until deal 3, and requires a research partner to keep theory 2 alive.  
- **(c) Designer-arranger now, structurer later** — run (b), and let deal 3–4 convert the practice into (a) once there is a track record and a pool worth an SPV.

**(c) is the recommendation**, and it is not a fudge: §4's deal progression is a genuine path from one to the other, and nothing in (b) forecloses (a). The material question OQ-19 actually has to settle is not which end state but **whether to stop paying the PhD's opportunity cost now** — three to four years, against revenue starting in month 3 and a research relationship that supplies the PI and the ethics approval the PhD would have supplied.

Two subsidiary decisions travel with it: **OQ-20** (regulatory perimeter — must be answered in the first 30 days either way) and **OQ-21** (the academic affiliation route, which is required for impact validation under (b) and (c) alike).  
