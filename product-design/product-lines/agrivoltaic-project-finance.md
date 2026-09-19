# Product Line 2 — Agrivoltaic Project Finance (BFAV)

**Status:** Concept, partially specified · **Origination layer:** farmers / landholders · **Asset:** PPA-backed project cash flows **Lineage:** `archive/google-drive/bfav-business-plan.md` (Apr 2024\) · **Last updated:** 2026-07-30

## Why this belongs in the same venture

BFAV looks like a different business from the VSLA line — solar developers and utilities rather than savings groups and microloans. It is the same thesis with a different origination layer.

The venture's claim is that certain sustainable-development assets are underfunded because nobody designed them at origination to be poolable. That claim is layer-agnostic. What matters is whether the origination layer produces cash flows that are **standardized, verifiable, and legally transferable**. Agrivoltaic projects do — arguably more cleanly than community loans:

|  | Community credit line | Agrivoltaic line |
| :---- | :---- | :---- |
| Originator | VSLAs, MFIs, NGOs | Farmers / landholders, via our project vehicle |
| Underlying cash flow | Loan repayments, insurance premiums | PPA revenue from the utility |
| Counterparty credit | Many small, socially enforced | One utility, monopsony |
| Standardization difficulty | High — data capture is the hard part | Low — PPAs are already standard contracts |
| Tenor | Months | 15–25 years |
| Precedent | LIT-004, LIT-006 | **LIT-008** (Rwanda distributed solar ABS) |

**LIT-008 is a direct precedent for this line, not an analogy.** It pools many small, geographically dispersed solar receivables from multiple originators into one tradable ABS. That is structurally what a portfolio of agrivoltaic projects is. The requirement it identifies — a standardized origination protocol across developers plus a donor/DFI anchor — is the same requirement here.

The predecessor `sds-work-plan.md` is the bridge document: it argued for combining projects with uncorrelated idiosyncratic risk (by timeline, type and geography) into pooled securities. A portfolio containing both community receivables and agrivoltaic PPAs is a concrete instance of exactly that.

## Concept

A project finance and management firm that adds bifacial agrivoltaic solar capacity to working farmland, sells the electricity to the utility under a PPA, and manages the project through its life.

The differentiator is risk allocation: **the investment is de-risked for the landholder**. The farmer contributes land use without carrying development or capital risk, which is what makes projects actually move. Crop rotations are selected to be compatible with the array rather than displaced by it, so the land keeps producing.

Unit economics reduce to: `(Solar Area Coverage) × (Solar Productivity in Watts) × (Price per Watt)`.

## Market structure

The end customer is the electric utility buying the power. But revenue comes through relatively rigid PPAs in a monopsony market — the price is not negotiable in any meaningful sense, and there is only one buyer.

That has a consequence worth stating plainly: **growth is constrained by partner acquisition, not by sales.** The real customers are the farmers and investors whose participation creates projects. Marketing effort belongs there, not at the utility.

The monopsony also cuts the other way, and favourably for securitization: a single, regulated, creditworthy offtaker on a long-dated standard contract is a far more legible cash flow to an investor than thousands of small borrowers. The credit analysis largely collapses to the utility's credit plus operational/production risk.

## Products and services

1. **Capital investment and project management** — the core service.  
2. **Partnership models** — yield modelling across PV and crop to design the most appropriate and profitable configuration for a given plot.  
3. **Asset securitization** — the layer this venture exists to build. Present in the original 2024 plan as a line item; here it is the point.  
4. **O\&M** — operations and maintenance over project life.

## Risks

| Category | Risk | Note |
| :---- | :---- | :---- |
| Production | Solar yield below model | Bifacial gain on agricultural ground cover is site-specific; needs measured validation, not datasheet assumptions |
| Agricultural | Crop yield loss under array, rotation incompatibility | The value proposition to the farmer fails if this isn't managed |
| Offtake | PPA terms set by a monopsony buyer; tariff or policy revision | The single largest exposure — concentrated counterparty and regulatory risk in one place |
| Political / regulatory | Land-use permitting, agricultural land protection rules, grid connection queues | Jurisdiction-specific; blocks projects rather than degrading them |
| Financial | Interest-rate and construction-cost exposure on long-dated assets | Match funding tenor to asset tenor |
| Concentration | Many projects, one offtaker | Undermines the "uncorrelated idiosyncratic risk" pooling logic if the whole portfolio faces one utility — see below |

## The concentration problem — and why the two lines need each other

A pure agrivoltaic portfolio is only superficially diversified. Many small projects, but one offtaker, one regulator, one tariff regime. Idiosyncratic risk is diversified; systematic risk is not. That is precisely the failure mode the SDS work plan warned about.

This is the strongest structural argument for running both product lines: community receivables and PPA-backed project cash flows have close to no shared risk driver. A blended pool is genuinely diversified in a way that either line alone is not.

Whether a **blended vehicle** is desirable is a live question. Rating agencies and investors generally prefer homogeneous pools, and mixing an unproven asset class with a legible one may contaminate the legible one rather than lifting the other. Recorded as OQ-8.

## Not yet specified

Carried forward from the 2024 plan and still open:

- Financial plan — capex per MW, project IRR, revenue projections, the funding ask  
- Competitive analysis — who else is doing agrivoltaic project finance in this market  
- Team and organizational structure  
- Legal structure of the project vehicle, and whether it can be the same entity as the community line  
- Which jurisdiction — the original plan implies Israel, which would align with the community line's pilot site

## Open questions

- **OQ-8** — should agrivoltaic and community receivables be pooled in one vehicle, or kept in separate homogeneous pools?  
- Does the LIT-008 origination-protocol standard transfer directly to agrivoltaic projects, or does long-tenor PPA paper need a different template?  
- What does a utility's PPA actually allow in terms of assignment of receivables? This is the LIT-009 true-sale checklist applied to this asset — and it may be the binding constraint.

