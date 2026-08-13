# RT-2 and RT-3 scaffolds — scorecard and monitor

**Status:** Scaffolds built, running against synthetic data · **Version:** 0.1 · **Calibration: none** **Code:** tools/score\_loans.py, tools/monitor\_portfolio.py · **Data:** tools/generate\_dataset.py

## The chain now runs end to end

RT-1 schema  ──►  generate\_dataset.py  ──►  validate\_schema.py \--data   (schema is executable)

                          │

                          ├──►  score\_loans.py       RT-2: decision \+ reasons \+ limit

                          ├──►  monitor\_portfolio.py RT-3: PAR, arrears, alerts

                          └──►  simulate\_portfolio.py RT-5: waterfall, tranches, stress

python3 risk-tools/tools/generate\_dataset.py \--out /tmp/synth \--groups 300

python3 risk-tools/tools/validate\_schema.py \--data /tmp/synth

python3 risk-tools/tools/score\_loans.py \--data /tmp/synth

python3 risk-tools/tools/monitor\_portfolio.py \--data /tmp/synth \--as-of 2027-05-31

**The validation step is the point.** The generator writes data claiming to conform to the 57-field schema; the validator checks it does. That makes RT-1 executable rather than a document, and it is the only way to know a field contract is still coherent before anyone tries to collect against it in a village. Corrupting the generated data — a bad enum, a missing required field, a dangling foreign key, a non-ISO date — fails the check, so it has teeth.

---

## RT-2 — rules-based scorecard

Takes a loan plus its member and group from RT-1, returns a **score, a band, a limit, and the reasons in both directions**.

### Rules-based on purpose, not as a stepping stone to ML

There is no repayment history to train or validate on. A model fitted on borrowed priors would be a confident guess wearing the costume of a measurement — and impossible to explain to a borrower who was declined. LIT-014 puts consumer protection, not systemic risk, at the centre of savings-group regulation, and *"the model said no"* is not a reason anyone can contest.

When a real track record exists, the honest upgrade is to **backtest this scorecard against it first**. A scorecard that beats chance is the baseline any model has to clear.

### Two rules that only exist because of the schema

Most of the scorecard is unsurprising — track record, leverage, group maturity, guarantee. Two rules are worth calling out because a generic credit scorecard could not express them:

**The share-out constraint.** A loan maturing at or past the end of the savings cycle has to survive the moment the group empties its box. The joint-liability backing is at its weakest exactly when the loan falls due. This is only visible because RT-1 captures group\_cycle\_length\_months alongside loan\_term\_days — and it is a concrete argument for keeping that field required.

**Correlated exposure.** An agriculture\_input loan to a smallholder\_farming borrower is repaid from the same harvest it funds. That is correlated risk hiding inside an apparently diversified pool, and it is exactly the parameter RT-5 shows the junior tranche is most sensitive to. Two fields the schema already has, combined.

### Output on synthetic data

| Band | Share |
| :---- | :---- |
| approve | 78.7% |
| approve with conditions | 17.0% |
| refer | 4.0% |
| decline | 0.3% |

**That distribution is a property of the generator, not a finding.** The generator draws borrower attributes roughly uniformly, so the population is healthier than any real cohort. The useful output is the *reason distribution* — "no completed savings cycles" and "first loan for this borrower" dominate, which is what you would expect from a synthetic population with no history, and is a sanity check that the rules fire on the inputs they claim to.

Every decision is explainable:

$ score\_loans.py \--data /tmp/synth \--explain LN-0000000003

Loan LN-0000000003 \- score 93.0 \-\> approve

  in favour:

    \+ member has completed 2 prior cycle(s)

    \+ 3 prior loans in this group

    \+ loan is 1.3x savings \- conservative

    \+ group is in cycle 6 \- has survived 5 share-outs

---

## RT-3 — monitoring and early warning

Walks the event stream in date order, tracks per-loan state, and reports portfolio at risk, arrears concentration by group / region / originator, and threshold breaches. Supports \--as-of for point-in-time evaluation.

### It fires before the loss lands

This is the whole claim, and it is testable. Running the same dataset at successive dates:

| As at | PAR30 | Written off | Alerts |
| :---- | :---- | :---- | :---- |
| 2027-05-31 | 1.66% | **0** | **2** |
| 2027-07-31 | 3.49% | 4,814 | 1 |
| 2027-09-30 | 5.73% | 23,291 | 1 |
| 2027-12-31 | 1.88% | 51,325 | 1 |
| 2028-06-30 | 0.82% | 54,788 | 1 |

At the end of May in this run (300 groups, seed 20260730), **nothing has been written off at all** — and the monitor is already flagging:

\[SERIOUS \] new arrears rose from 30 to 52 month-on-month (+73%) \- leading indicator,

           before any write-off lands

\[WARNING \] 3 groups above 25% arrears \- worst GRP-000010 at 29%

By the time write-offs reach $51k, PAR30 has already peaked and started falling. The arrears signal leads the realised loss by roughly four to seven months here.

Whether write-offs are *exactly* zero at a given date depends on the seed and the sample size, so test\_toolchain.py asserts the durable property instead: at the early date, arrears are already accumulating while under 20% of eventual write-offs have been booked. A write-off is not a warning — it is an outcome, and by then the only remaining question is how to report it.

That lead time is also what makes the junior tranche fundable. LIT-013 is explicit that a documented monitoring regime is part of what a first-loss provider is buying: they are taking the risk, so they need to see it moving before it arrives.

### The alert that matters most for a pooled structure

Several regions deteriorating *simultaneously* escalates to critical, with an explicit note that this is consistent with a correlated shock rather than idiosyncratic default. That is the scenario RT-5 shows the junior tranche is most sensitive to, and RT-3 is where it becomes visible first.

### Thresholds are judgement

All six live at the top of the file rather than buried, because they are the first thing that should be argued about and the first thing real data should replace. Every alert states the number that tripped it, so it can be contested rather than believed.

---

## What would move these from scaffold to usable

**RT-2**, in order of impact:

1. **Observed repayment outcomes** to backtest the scorecard against. Until then the weights encode which signals the literature says should matter, in what rough order — not what does.  
2. **A field review of the reason strings.** They are consumer-facing, and phrasing that reads as reasonable in English may not survive translation or the relationship it lands in.  
3. **A limit policy conversation with originators.** The limit-as-multiple-of-savings convention is inherited from savings-group practice, not derived.

**RT-3**:

1. **Threshold calibration** against an observed delinquency distribution. Six numbers currently doing a lot of work.  
2. **Vintage curves** — arrears by months-on-book across disbursement cohorts. Implementable now, and the standard view an investor asks for.  
3. **A false-positive review.** An alert nobody acts on is worse than no alert, because it trains people to ignore the panel.

Both remain **uncalibrated**. Every output is labelled synthetic. Neither should be shown to a partner or an investor as a result.  
