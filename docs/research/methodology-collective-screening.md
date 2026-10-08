# Methodology — screening collectives for risk intermediation

**Status:** v1, provisional cutoffs · **Last updated:** 2026-10-08 · **Applies to:** rows in `data/collective-market-map.csv` · **Script:** `scripts/score_collectives.py` · **Part of:** the business-research unit (`docs/venture/business-research.md`)

## What the score is for

The business-research plan asks which collective institutions can originate, monitor, aggregate, hedge and service member-level risk well enough to support external risk-sharing. The scorecard turns that question into ten dimensions a desk reviewer or a deep-dive visit can score 1 to 5, so that candidates across countries and collective types are compared on the same terms and the reason a candidate was dropped is recoverable later.

It is a screening tool, not a credit model. RT-7 is the quantitative companion: a collective that screens well is one whose parameters could be observed rather than assumed.

## The ten dimensions

| Dimension | A score of 5 means | A score of 1 means | Where RT-7 feels it |
|---|---|---|---|
| **Cash-flow observability** | Digitised sales, delivery, payment and repayment records | Paper, partial, or none | Every `observed` promotion in the parameter tracker |
| **Contractability** | Credible offtake, delivery, collateral and collection-account rights | Informal sales, no assignable receivable | `fwd_share`, `penalty_per_ton_short`, the delivery channel |
| **Diversification** | Many members, limited concentration, several micro-regions and buyers | Few members or one buyer | `member_yield_dispersion`, number of members, the regional factor's reach |
| **Governance** | Audited accounts, transparent leadership, reliable member records | Unaudited, contested, no register | `collective_fixed_cost_usd`, `reserve_share_of_margin` |
| **Loss-history availability** | Several cycles of repayment, sales and recovery data | None | `base_pd_*`, `lgd_*`, `pd_anchor_dscr` |
| **Climate measurability** | Clear crop calendar and usable weather or yield proxies | No usable index | `yield_vol` and the climate factor (DS-02, DS-03) |
| **Price-risk controllability** | Pricing formulas, buyer relationships, hedging or price-floor access | Spot sales only | `fwd_price_usd_per_t`, `basis_local` |
| **Servicing capacity** | Can originate, monitor, collect, reconcile and report regularly | Cannot | Whether RT-1 and RT-3 could run at all |
| **Regulatory feasibility** | Can lend, pledge receivables, insure and transfer risk | Cannot, or unclear | Whether a facility is legal (OQ-20 by market) |
| **Member alignment** | Clear member benefit; protections against exclusion and over-indebtedness | Unclear benefit, coercion risk | `household_floor_usd`: the model assumes consumption is senior to debt |

Each dimension is scored on the evidence in the row's `Evidence_Refs`. A score without a reference is a guess; leave it blank instead.

## Bands

| Total | Band | Means |
|---|---|---|
| 40–50 | Structured-pilot candidate | Design a facility with a defined risk layer |
| 30–39 | Limited pilot | A pilot with technical assistance, data improvement or guarantee support first |
| Below 30 | Research prospect | Technical-assistance or research relationship; not yet suitable for external risk transfer |

**The cutoffs are provisional.** They came in with the plan and have not been tested against a single scored partner. The first three deep dives should be used to check whether the bands separate anything, and the cutoffs moved if not. Record the change here with the date.

## Rules

- **Score only after a deep dive or a well-sourced desk review.** A longlist row has blank scores and a blank band. `scripts/score_collectives.py` refuses a partial scorecard.
- **Score organisations, not relationships.** The market map is public. Whether an organisation has replied to us, who the contact is, and what they said live in `private/partner-contacts.csv`, never in a score or a note.
- **One row per entity, stable ID.** `CMM-NN`, never reused. A dropped candidate stays with `Research_Status: Dropped` and the reason.
- **Research_Status vocabulary:** `Longlist` · `Desk reviewed` · `Deep dive` · `Scored` · `Dropped`.
- **Entity_Type vocabulary** (the typology in the plan): `Producer cooperative` · `Savings group network` · `SACCO` · `Farmer producer organisation` · `Cooperative union` · `Mutual guarantee association` · `Platform network` · `Specialist lender` · `Bank or MFI` · `Buyer or exporter` · `Insurer` · `Investor or fund` · `Government or DFI program`.

## Running it

```bash
python3 scripts/score_collectives.py          # recompute totals and bands in place
python3 scripts/score_collectives.py --check  # CI-style: exit 1 if the committed file is stale
python3 dashboard/build.py --public           # the Business research tab reads the result
```
