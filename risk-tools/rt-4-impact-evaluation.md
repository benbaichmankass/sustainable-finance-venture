# RT-4 — Impact evaluation module

**Status:** Specified, not built · **Version:** 0.0 (draft spec) · **Product lines:** PL-1 · **Blocked by:** OQ-4, OQ-5, OQ-7

## Purpose

Randomisation infrastructure and pre-registered analysis, so that impact claims about the pilot are credible to an academic supervisor, a DFI and a sceptical reader.

## Why this is a tool and not a report

The project's credibility rests on the evidence being trustworthy (`CLAUDE.md` §6). The literature is full of microfinance impact claims that did not survive scrutiny — Memo 2 exists because average effects on income turn out small and heterogeneous while the marketing rarely says so.

The way to not repeat that is procedural, and the procedure has to be built before enrolment starts:

1. **Design fixed and pre-registered before anyone is enrolled.** Choosing an estimator after seeing outcomes is the single most common way impact claims lose credibility.  
2. **Randomisation mechanised, not manual.** A documented, reproducible, seeded assignment. Hand-assignment invites well-meaning interference — the field officer who moves a struggling group into treatment destroys the comparison.  
3. **Analysis code written against simulated data first.** If the analysis only gets written after outcomes are visible, every specification choice is contaminated.

## Design

| Component | Does |
| :---- | :---- |
| Assignment | Seeded, reproducible randomisation at the level OQ-4 settles on; records the seed, the strata and the assignment log |
| Balance checks | Automatic covariate balance report post-assignment |
| Power analysis | Simulation-based, run *before* enrolment to state the minimum detectable effect |
| Pre-registration artefact | Generated from the design config, timestamped, committed, filed publicly |
| Analysis | Pre-specified primary and secondary outcomes, estimator, and multiple-comparison handling |

**Outcomes follow the evidence, not the pitch.** Per Memo 2, the primary outcomes should be resilience and consumption smoothing — where the evidence base is strongest and the measurement most defensible — with income and business investment as secondary and clearly labelled as such.

### Design choice still open

OQ-4 and OQ-5 both ask cluster randomisation versus stepped-wedge. They interact with partner acceptability: NGO partners often resist withholding treatment, which pushes toward stepped-wedge, while cluster randomisation gives a cleaner comparison. This must be settled with the verification partner (OQ-7) before the module is built, because it determines the assignment component's entire shape.

## Ethics

- Consent basis, retention period and access must be stated before any participant data is collected. Tracked as part of M-08.  
- Row-level participant data lives in the Vault's `05-raw-data` and never enters the repo — not as a CSV, a summary, or a dashboard row.  
- IRB or equivalent review via the academic partner (PT-05, PT-06).  
- Aggregate results come back to the repo. Individual records do not.

## Versioning

| Bump | Means |
| :---- | :---- |
| Major | Design or primary outcome changes — **requires an amended pre-registration with the change and its rationale stated** |
| Minor | Additional secondary outcome or robustness check added |
| Patch | Code fix with no change to specification |

A major bump after enrolment begins is a serious event and must be visible as one. The version history is part of the evidentiary record, not just changelog hygiene.

### History

| Date | Version | Change |
| :---- | :---- | :---- |
| 2026-07-30 | 0.0 | Initial specification. Design pending OQ-4/OQ-5 resolution with the verification partner. |

## Tests

Not yet written. Planned:

- **Assignment reproducibility** — same seed and inputs produce identical assignment, always.  
- **Randomisation quality** — many simulated assignments; check balance holds on average and the procedure is unbiased.  
- **Power simulation** — recover a known injected effect at the stated power; confirms the analysis code can find what it claims to be able to find.  
- **Null test** — run the full pipeline on data with no true effect. It must not produce a significant result more often than chance. This is the test that catches an analysis pipeline that manufactures findings.  
- **Pre-registration diff** — assert the executed analysis matches the registered specification, and flag every deviation.

## Open questions

- Cluster randomisation or stepped-wedge? (OQ-4, OQ-5)  
- Which verification partner, and what are their data-sharing and IRB requirements? (OQ-7)  
- What is the minimum detectable effect at realistic pilot scale — and if the honest answer is "larger than the effect we expect," what does the pilot actually establish? Better to know that before enrolling than after.

