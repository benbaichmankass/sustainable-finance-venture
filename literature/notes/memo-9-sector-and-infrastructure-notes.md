# MEMO-9 — Sector and infrastructure notes

**Status:** Drafted (LC-24 section only) · **Covers:** LC-24 coffee-sector economics and cooperative finance · **Last updated:** 2026-10-08

This memo is the practical-rails memo: digital capture, PAYGO receivables, value-chain and warehouse finance, cost-to-serve, remittances, the coffee sector, and data governance. Only the **coffee section is written**. The rest is still outline.

The coffee section was written first, and out of order, because OQ-16 committed the field anchor to the coffee cooperative cluster on 2026-08-22 *before* this component was read. The read therefore audits a decision rather than informing one.

---

## 1\. What this section had to settle

The coffee scores (EXP-09 and EXP-10, both 3.60) rested on two untested assumptions:

1. **Partner reachability** — that producer cooperative federations and value-chain lenders are actually reachable, and that cooperatives intermediate *credit* rather than only marketing.  
2. **Data rails** — that certification and traceability records could carry underwriting, or at minimum supply a sampling frame.

Both now have evidence. Both survive. A third thing surfaced that nobody asked about, and it is the one that matters most.

---

## 2\. Cooperatives do intermediate credit — and the loan book is exactly the object of study

**LIT-031** settles assumption 1 in the affirmative, in the lender's own words. Root Capital lends to enterprises — producer organisations, private businesses, local financial institutions — and those enterprises

> "on-lend funds as smaller loans to individual producers and, in doing so, bear the risk of repayment. Enterprises manage all loan origination, disbursement, monitoring, and repayment internally through an **internal credit fund**."

That is not a marketing cooperative. That is a lender of record with a portfolio, and the internal credit fund is precisely the cash-flow object this project proposes to make investor-legible. The scale is real: more than USD 900m disbursed since 1999 across roughly 2,000 loans; under the Coffee Farmer Resilience Initiative, USD 9m in renovation loans to nine enterprises reaching 1,335 farmers over 3,500 hectares in two years.

**But the same report supplies the caveat that should govern the pilot design.** Root Capital describes internal credit funds as "often informal and unregulated", says weak internal controls and accounting are "the most commonly observed deficiencies among potential R\&R loan clients", and states that credit decisions "can be politically or personally motivated, rather than being based on established policies to determine financial need and creditworthiness."

This cuts both ways and the memo should be honest about which way is which:

- **For the thesis** — this is the "informally functional, not investor-legible" gap stated by a practitioner lender, unprompted. It is corroboration that the problem is real.  
- **Against the pilot as currently imagined** — if the origination records are informal, they cannot be assumed to support a data tape. Any coffee pilot has to budget for *building* the record, not extracting it.

One number is conspicuously absent and its absence is itself a finding: **the report discloses no repayment, default, delinquency or portfolio-at-risk figure** for either the R\&R portfolio or the enterprises' on-lending. It was published two years into a seven-year product with a two-year principal grace, so nothing had amortised. The lender-side loss data this project needs does not exist in the public record here.

---

## 3\. The sampling frame exists, and has been used

**LIT-033** settles assumption 2 for Ethiopia, concretely. The author compiled a comprehensive list of coffee cooperatives and their certification status by working with the regional Authority, the Cooperatives Agency and the Sidama cooperative unions, then drew a probability sample: 12 certified and 8 non-certified cooperatives selected at random from those lists, then 370 certified and 160 non-certified households drawn randomly *from the list of cooperative members in proportion to the size of each cooperative*.

Member registers exist. They are obtainable through the union and the government Cooperatives Agency. They have been used as a probability sampling frame in published work.

The universe is also large enough to matter: **about 57 primary cooperatives in Sidama alone, collectively involving around 85,000 smallholder farmers** across 8,000 hectares of Arabica. Forty-one are Fairtrade-certified, 32 of those also Organic.

**LIT-034** shows the same proportional-to-membership approach applied across Ethiopia, India and Nicaragua — so the method travels, at least to Latin America.

What is *not* established: whether member registers are equally obtainable in the Latin American belts where LIT-031's evidence sits. LIT-033 is Ethiopian. That gap is real.

---

## 4\. Certification organises the population; it does not deliver the outcome

This is where the coffee case gets weaker, and it needs saying plainly because a proposal built on certification-premium logic would be built on sand.

**LIT-032**, the Campbell/3ie systematic review, is the authority: 43 effectiveness studies drawn from 10,753 records, coffee 38% of them, published 1990–2016. Its headline methodological finding is that there are **no randomised controlled trials in this literature at all**, and "the proportion of quantitative studies with high risk of bias ratings was relatively large."

Its synthesised effects have a consistent shape:

| Outcome | Effect | Significant? |
| :---- | :---- | :---- |
| Price | \+14% (4 to 24%) | **Yes** |
| Income from sale of certified produce | \+11% (2 to 20%) | **Yes** |
| **Total household income** | **\+6% (−3 to 16%)** | **No** |
| Yields | −20% (−52 to 19%) | No |
| Assets / wealth | \+3% (−7 to 13%) | No |
| Wages (workers) | **−13% (−22 to −3%)** | **Yes — negative** |
| Schooling | \+6% (0 to 12%) | Yes |

Certification moves the price line and the crop-revenue line. It does **not** demonstrably move total household income. And for hired workers the significant effect is *negative*.

**LIT-034** replicates the pattern across three continents: pooled, no significant yield effect and no household income effect, with net revenue up 445–593 PPP\$/ha. Country results scatter badly — Ethiopia negative throughout, India positive, Nicaragua positive only on net revenue.

**LIT-033 is the dissenting result** and should not be buried: in Sidama, nearest-neighbour matching gives positive significant effects on coffee income, household income *and* consumption expenditure. The author attributes the difference from western-Ethiopia studies to better-organised cooperatives in Sidama — which, read carefully, is an argument that the effect is a property of **strong cooperatives**, not of certification. That reading is more useful to this project than the headline, because cooperative strength is something a design can select on and measure.

**Design consequence.** Certification records are a *sampling and organising* asset. They are not an income mechanism, and the pilot's theory of change must not route benefit through the certification premium. Note also that in Sidama the premium reaches producers as **dividends** (first dividends 5–8 ETB/kg from the cooperative, second 5–6 ETB/kg from the union) and the USD 0.20/lb social premium goes to community projects, not households — so even where a premium exists, its incidence is at the cooperative, not the farm.

---

## 5\. The finding nobody asked for: coffee is close to a worst case for correlation

This is the most consequential thing in the read, and it did not come from the questions the component was written to answer.

**Coffee leaf rust is a textbook covariate shock**, and LIT-031 measures it:

- more than **half of Central America's total coffee-growing area** affected at once  
- analysts estimated up to a **40% reduction** in Central American annual output, roughly **USD 500m** in lost producer revenue and nearly **375,000 jobs** eliminated  
- **El Salvador production cut 60%** in 2013/14 against the prior year  
- **40% of Peru's total coffee-growing area** affected  
- some Root Capital-financed producer organisations in Selva Central experienced **80% production drops**

Governments of Costa Rica, Guatemala, Honduras, Nicaragua and Peru all declared national states of emergency.

Now add price. **LIT-035** records that in coffee year 2019/20 the ICO composite indicator was flagged by IFPRI's Excessive Food Price Variability system on **45 of 260 reporting days** as *excessively* variable, plus 48 days of moderate variability — roughly one trading day in six. Standard deviation of the composite around its annual average was 7.2 US cents/lb, and of futures 11 US cents/lb.

So a pool of smallholder coffee loans faces a **biological covariate shock and a price covariate shock, both regional or global in scope, both capable of moving the whole book at once**. That is the opposite of the idiosyncratic-risk profile that makes a portfolio poolable.

Two readings, and the honest answer is that both are true:

- **Against the anchor.** For a securitisation thesis, a monocrop export commodity with a regional pathogen and a world price is close to the hardest case you could pick. Diversifying across regions does not help much when leaf rust crossed from Mexico to Peru in a season.  
- **For the anchor.** If the project's real contribution is characterising and pricing correlation — which is what EXP-25 tests and RQ-03 asks — then coffee is where the correlation is large enough to *measure*. A setting with weak covariate structure would be a weaker test, not a stronger one.

Which reading wins depends on OQ-17, which is still open. It should be decided deliberately rather than inherited.

There is also a live comparator: **Colombia launched a Coffee Price Stabilization Fund in February 2020** specifically to protect farmers against price volatility (LIT-035). For EXP-09, whose whole premise is price stabilisation, that is simultaneously a partner opportunity and a displacement risk under OQ-11's logic — a state scheme already occupies the ground.

---

## 6\. Verdict on the coffee bet

**The bet survives, on both assumptions it was made on.** Cooperatives really do lend, and member registers really are obtainable and have been used as sampling frames. Nothing here forces the reversal that was the risk of deciding before reading.

**But the read moves the risk rather than removing it.** Three things changed:

1. The origination records inside cooperative internal credit funds are described by a practitioner lender as informal and unregulated. Budget for building the data rail, do not assume it.  
2. Certification cannot carry the welfare claim. It organises the population; the outcome has to come from somewhere else.  
3. Coffee's risk is dominated by two covariate shocks. This makes it the hardest case for poolability and the best case for measuring correlation — and which of those the project wants is an open decision, not a settled one.

**Still unread for this component:** the record of coffee price-risk instruments for smallholders as *evaluated* rather than announced; whether Latin American member registers are obtainable; and any published loss or default data on cooperative internal credit funds, which on this evidence may not exist publicly at all. Status is `Partially covered`, five anchors of eight.

---

## 7\. Cost and income anchors for the coffee model (added 2026-10-08)

RT-7 needed farm sizes, production costs, a household floor and loan terms for its three coffee regions, and the prototype had assumed all of them. The sources below were read for those numbers; the derivations are in `data/rt7-literature-inputs.csv` and the resulting parameter changes in `data/rt7-parameters.csv`. Three things are worth recording here rather than only there.

**Normative and observed costs differ by an order of magnitude, and the difference is family labour.** Fairtrade's living income reference price models (LIT-045 Colombia, LIT-046 Ethiopia) cost all labour at a living wage: 108,030 Birr per hectare of garden coffee in Ethiopia. The Sidama household survey (LIT-033) reports what households actually paid: 7,655 Birr per household, about 12,350 per hectare, of which hired labour is under half. A credit model that deducts a household floor before debt service should use the cash figure and let the floor carry family labour; using the normative figure would double-count. The same split exists in Colombia, where LIT-045's 2022 per-farm costs (7.77 million pesos of inputs on 2.8 ha after a 122 percent fertiliser-price rise) are those of an intensive farm and the harvest labour scales with yield.

**A subsistence floor and a living income are different questions, and the model asks the first.** DANE's 2024 rural poverty line (LIT-052; 291,998 pesos per person per month) and Vietnam's Decree 07/2021 income criterion (LIT-053; 1.5 million dong per person per month) give subsistence floors of about 3,400 and 3,000 dollars a year for a household of four; the living-income benchmarks for the same households (LIT-045, LIT-049, LIT-048 for Sidama) are roughly double. Even at the subsistence floor, a quarter of the Colombian members in the model cannot cover debt from coffee alone, because the farm-size mean is 1.28 ha (LIT-050, LIT-051) with a long small tail. What makes those households creditworthy in practice is off-farm income, which no open source quantifies for Colombian or Vietnamese coffee households and which LIT-033 puts at about 550 dollars cash for Sidama.

**Open proxies for repayment exist for Colombia and not for the other two.** Kiva's Colombian agriculture partners (DS-11) show a loans-posted-weighted arrears rate of 7.7 percent and a default rate of 3 percent on Kiva-funded books, with coffee-purpose loans of about 760 dollars over 18 months. That is a microfinance book, not a cooperative's, and it is the closest open number to the normal-year PD the model needs. Ethiopia has no Kiva presence; Vietnam's coffee loans all sit with one paused partner in arrears on two thirds of its book and were not applied. LIT-031's point stands: cooperative on-lending repayment data is not published anywhere, and a pilot has to collect it.

Vietnam remains the thinnest case: its cost figure is a 2021 press report of farmer statements (LIT-055), its only yield and farm-gate numbers are from a 2024 newspaper article (LIT-054), and the provincial economic-technical norms that would give a proper cost basis (Decision 25/2021, replacing LIT-056) were not retrieved. That is consistent with Vietnam's role as a modelling comparator rather than a market candidate.

---

## Sources

- **LIT-031** — Root Capital 2016, *Financing Farm Renovation: How to Build Resilience Using a Blend of Capital* (Coffee Farmer Resilience Initiative learning report)  
- **LIT-032** — Oya, Schaefer, Skalidou, McCosker & Langer 2017, *Effects of certification schemes for agricultural production on socio-economic outcomes in low- and middle-income countries: a systematic review* (3ie Systematic Review 34 / Campbell Systematic Reviews 13\)  
- **LIT-033** — Berihun 2024, *The Economic Impact of Sustainability Standards on Smallholder Coffee Producers: Evidence from Sidama Region, Ethiopia* (IGC Working Paper ETH-22247)  
- **LIT-034** — Jena & Grote 2022, *Do Certification Schemes Enhance Coffee Yields and Household Income? Lessons Learned Across Continents* (Frontiers in Sustainable Food Systems)  
- **LIT-035** — International Coffee Organization 2020, *Coffee Development Report 2020: The Value of Coffee*
- **LIT-045** — Fairtrade International 2022, *Living Income Reference Price for Coffee from Colombia: Update December 2022*
- **LIT-046** — Fairtrade International 2023, *Living Income Reference Price for Coffee from Ethiopia: Explanatory Note*
- **LIT-047** — Fairtrade International 2025, *Living Income Reference Price update, forest coffee, Ethiopia*
- **LIT-048** — Global Living Wage Coalition 2025, *Living Income Report for Rural Sidama, Ethiopia* (landing page figures)
- **LIT-049** — Global Living Wage Coalition 2025, *Living Wage Report for Minimum Wage Region 4, Vietnam* (landing page figures)
- **LIT-050** — Federacion Nacional de Cafeteros (Uribe) 2025, *Extension y asistencia tecnica para la productividad sostenible* (presentation)
- **LIT-051** — StoneX 2023, *Coffee study maps structural shifts in Colombia's coffee sector*
- **LIT-052** — DANE 2025, *Pobreza monetaria y pobreza monetaria extrema 2024*
- **LIT-053** — Government of Viet Nam 2021, *Decree 07/2021/ND-CP on the multidimensional poverty standard for 2021-2025*
- **LIT-054** — Nhan Dan 2024, *Dak Lak thuc day cac giai phap phat trien ben vung nganh hang ca phe*
- **LIT-055** — VietnamNet 2021, *Coffee farmers suffer poor crop, low price*
- **LIT-056** — Dak Lak Provincial People's Committee 2013, *Decision 38/2013/QD-UBND on economic-technical norms for main crops and livestock*
