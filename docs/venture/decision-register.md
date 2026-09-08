# Decision Register — What Has To Be Settled, and When

**Status:** Live register · **Owner:** BB · **Drafted:** 2026-09-08

Every decision the work plan needs, sequenced by **when it binds** rather than by importance.
Companion to `docs/venture/track-c-plan.md`; open questions carrying the substance live in
`data/open-questions.csv`.

---

## 0. The frame this is written under

**Phase 2 is the base case. Phase 3 is an option, not the goal.** A design, standard-setting and
verification practice that never sponsors a securitisation is the plan, and it has to stand on its
own economics. Phase 3 stays available only where keeping it available is free.

Four things change once that is the frame, and they change the decision list rather than merely
its tone:

**1. The business has no capital requirement at all.** Gate 6 of `track-c-plan.md` §4 — identify
and commit the retention strip — was the single line where the model stopped being capital-light.
Under a Phase-2-terminal plan that line never arrives. The venture is funded by fees from end to
end.

**2. Lane D stops being a "year 2+" afterthought and becomes the strategic core.** This is the most
important consequence and it reorders the register. `solo-operator-track.md` §3.2 lists four
revenue lanes; A (diagnostics), B (design mandates) and C (arranging) are all **linear in your
calendar**. At two to three concurrent engagements, that is a well-paid job with a hard ceiling.
Lane D — the published standard, the tooling, verification and attestation subscriptions — is the
only leg that earns without consuming a day. Under Phase 3, Lane D was a bonus. Under Phase 2 as
the end state, **Lane D is the difference between a business and a job**, and the decisions that
shape it (D-16, D-17) move from month 18 to month 6.

**3. Some carry-forward items get more important, not less.** Re-derived in `track-c-plan.md` §5.

**4. Two gates stop being gates.** The correlation estimate and OQ-18 mattered because they sized
tranches. They are now research and credibility assets — valuable, not load-bearing.

---

## 1. Decisions versus questions

Worth separating, because confusing the two is how a plan stalls:

- **A question is settled by evidence.** Someone else can answer it — counsel, a partner's MIS, a
  dataset. OQ-1 (jurisdiction), OQ-3 (schema), OQ-18 (diversification axis) are questions. You
  commission them.
- **A decision is settled by you.** No amount of research closes it, because it is a choice about
  what kind of business this is. Market, pricing, what you refuse, what you give away.

This register lists **decisions**. Where one waits on a question, the question is named as its
input — but "I am still researching it" is only a valid answer for as long as the research is
actually commissioned and running.

---

## 2. Gate 0 — Before you can sell anything (Days 1–30)

| ID | Decision | Reversible? | Input |
| :---- | :---- | :---- | :---- |
| **D-01** | Operating model, and **how much you will pay to keep Phase 3 open** | Yes | OQ-19 |
| **D-02** | First market | Costly to reverse | **OQ-22** |
| **D-03** | Your own entity: legal form and jurisdiction | Costly | D-04 |
| **D-04** | Regulatory posture: advisory-only, appointed representative, or licensed | Yes | OQ-20, counsel |
| **D-05** | Offer design and pricing | Yes, but resets positioning | **OQ-23** |
| **D-06** | Data-rights clause scope | **No — irreversible per client** | M-42, counsel |
| **D-07** | Adopt the prohibition list | Yes | `track-c-plan.md` §6 |
| **D-08** | Runway: how much cash, over how long, before D1 can stop it | — | — |

### D-01 · How much to pay for the Phase 3 option

The recommendation is narrow and it follows directly from your steer: **keep only the free
options.** The data-rights clause, the refinancing right of first refusal and originating to RT-1
from day one all cost nothing and are good practice for a Phase-2-only business anyway. Do not
spend real money on Phase 3 — no SPV counsel, no rating conversations, no retention-capital
raise — until gate 1 (a ≥ USD 20m contractible pipeline) is met on its own.

### D-02 · First market — the biggest single decision

Everything downstream sits on it: travel cost is your main variable expense, and it is also the
one decision that quietly re-opens the research site choice.

**The commercial criteria are not the research criteria.** The coffee cooperative cluster was
chosen (OQ-16, M-33) partly because LIT-031 makes it *the hardest case for poolability* — a
research virtue that is close to irrelevant if you never assemble a pool. Re-take it on:

- originators with **10–40 branches** (the EXP-22 cluster-count constraint, and a proxy for "big
  enough to pay, small enough to decide quickly");
- a live TA facility in-market that funds design work (Lane B);
- a regulatory perimeter you can operate in unlicensed (D-04);
- travel cost and time-zone you can sustain solo;
- and — only if you still want the research paper — two lenders in one market.

Israel's original justification in `business-plan.md` §7 was logistical proximity for a
research-first configuration. That justification is weaker for a fee-earning practice and stronger
for cash-flow reasons. It deserves a fresh look rather than inheritance. **Logged as OQ-22.**

### D-05 · Offer design and pricing

Two sub-decisions, both yours alone, and neither has a benchmark anywhere in this repo:

- **Fee basis** — day rate, fixed fee per deliverable, or retainer. Fixed fee per deliverable is
  usually right for a diagnostic: it prices the outcome rather than your hours, and it stops a
  solo operator's utilisation problem from becoming the client's discount.
- **The number.** Together with utilisation this decides Phase 1, and M-41's model cannot be run
  until you set both. Mark them `ASSUMED` and move.

**Logged as OQ-23**, together with D-10.

### D-06 · Data-rights clause scope — the only irreversible one at Gate 0

The clause itself is settled (`track-c-plan.md` §5.1, M-42). What is a decision is **how far it
reaches**, and there is a real tradeoff: a broad grant covering pooling and third-party
structuring is what Lane D needs, and it is also the clause most likely to get escalated to a
client's board or data-protection officer and slow a first sale.

Under a Phase-2-terminal frame the answer gets *easier*, not harder: you no longer need rights
broad enough to securitise. You need rights broad enough to **benchmark across clients and publish
aggregates** — which is a materially smaller ask, easier to grant, and is exactly what Lane D
sells. Draft to that scope, not the maximal one.

Irreversible because it is per client and cannot be retrofitted. Decide before client one, not
during.

### D-08 · Runway

Not a strategy question, but it sets D1's date and is the constraint every other decision runs
into. Write down the number and the date. A plan whose stopping rule is undefined does not have a
stopping rule.

---

## 3. Gate 1 — Before outreach (Days 31–60)

| ID | Decision | Reversible? | Input |
| :---- | :---- | :---- | :---- |
| **D-09** | Which originator segment leads | Yes | OQ-12, OQ-13 |
| **D-10** | Entry product: full EXP-22, or a lighter readiness assessment | Yes | **OQ-23** |
| **D-11** | First engagement: full fee, discounted, or free for the case study | Yes, once | — |
| **D-12** | Product lines in scope: credit only, credit + insurance, and does PL-2 survive | Yes | **OQ-25** |
| **D-13** | Research partner: which form, which institution first | Yes | OQ-21 |
| **D-14** | Authorship terms to ask for in the MOU | **No, once papers exist** | OQ-21 |
| **D-15** | PhD application track: park it or run it in parallel | Yes | **OQ-26** |

### D-09 · Originator segment

Four are now tracked and they behave very differently as buyers: VSLA networks (PT-03, PT-11),
MFIs (PT-01), cooperative unions (PT-12) and SME/business membership associations (PT-13). They
differ in budget, data maturity, decision speed and — per OQ-12 — in whether repayment runs on
information or on social enforcement. **Pick one to lead.** A solo practice cannot learn four
buying processes at once, and the diagnostic's framing has to be written for a specific reader.

### D-10 · Entry product — the one I would most encourage you to re-examine

`solo-operator-track.md` §5.1 proposes selling EXP-22 as the first paid engagement. Worth
being honest about the risk in that: **EXP-22 is a cluster-randomised experiment with
activity-based costing.** It requires branch-level randomisation, timestamped capture logs, and
HR or staff-representation approval for officer time measurement. That is a research design, and
asking a first-time client to host one is a heavy first sale.

The alternative is a **lighter readiness assessment** — the RT-1 field list scored against their
current capture, a gap list, a costed remediation plan — sold in two to three weeks, with EXP-22
positioned as the upsell for a client who wants the number rather than the direction.

Lighter is easier to sell, produces a case study sooner, and still field-tests the schema. It does
*not* produce the per-field cost curve, which is what makes the standard adoptable incrementally
(§5.4 / Lane D). So the decision is real: **speed to first revenue against the depth that Lane D
needs.** Running the light version two or three times and the full EXP-22 once, with a funder
paying for the full one under Lane B, is the obvious hybrid and probably the answer.

### D-12 · Product lines under the solo constraint

Insurance requires a licensed risk carrier (PT-17 and that whole partner class). That is an extra
relationship, an extra regulatory surface, and an extra sales cycle. **PL-2 (agrivoltaic project
finance) is a further question again** — different buyer, 15–25 year tenor, permitting-heavy, and
essentially unrelated to the practice's day-to-day work. `business-plan.md` keeps it because the
toolkit is shared and the two lines are uncorrelated; under a solo services practice that argument
is much weaker, since the shared toolkit does not reduce the sales effort.

Deciding to park PL-2 for the practice's first two years is legitimate and should be explicit
rather than by neglect. **Logged as OQ-25.**

### D-15 · The PhD application track

M-06, M-11 and M-29 (supervisor outreach, applications, the application pack) are live milestones
competing for the same calendar as outreach wave 1. Running both halves both. The decision is to
**park them explicitly** — status `Blocked`, not deleted, with the publication route preserved via
D-14 — or to keep one narrow thread alive. **Logged as OQ-26.**

---

## 4. Gate 2 — Once there is revenue (Days 61–150)

| ID | Decision | Reversible? | Input |
| :---- | :---- | :---- | :---- |
| **D-16** | RT-1: publish openly, licence it, or open core plus paid tooling | **Hard to reverse once published** | **OQ-24** |
| **D-17** | Which Lane D product comes first | Yes | **OQ-24** |
| **D-18** | Whether to pursue arranging (Lane C) at all | Yes | D-05, M-41 |
| **D-19** | Subcontractor bench: who, and engaged how | Yes | — |

### D-16 and D-17 · The two decisions that decide whether this is a business or a job

Under a Phase-2-terminal plan these are the most consequential decisions in the register, which is
why the frame in §0 matters so much. They are in tension:

- **Theory 3 (standard-setting) says publish.** Adoption is the moat, adoption requires
  giving it away, and `business-plan.md` §5 names the falsifier as someone else publishing a
  competing standard first — adoption is winner-take-most, so being early beats being complete.
- **Revenue says licence.** A published standard earns nothing directly.

The resolution most standards businesses reach is **open core**: the *schema* is published free
and unencumbered, because adoption is the whole point; the *tooling* (RT-2 scorecard, RT-3
monitor), the **certification** that an originator's book conforms, and the **verification
attestation** that investors rely on are the paid layer. Theory 6 (verification) is what monetises
theory 3, and `business-plan.md` already notes it needs no new capability.

**D-17 then asks which paid layer comes first.** Certification is the cheapest to stand up and the
closest to what a diagnostic already produces — arguably it is just the diagnostic, repeated
annually, under a name that makes the recurrence obvious. **Logged as OQ-24.**

### D-18 · Whether to arrange at all

Worth holding open rather than assuming. Lane C is the highest regulatory exposure (D-04), the
longest cycle, and the lumpiest revenue. A practice that does A, B and D and simply *refers*
originators to capital partners without taking a fee from the transaction is simpler, cleaner and
possibly more profitable per hour. Decide it against M-41's model once there is real utilisation
data, not now.

---

## 5. Reviews, not decisions — hold these as dates

| | When | Question | Options |
| :---- | :---- | :---- | :---- |
| **D1** | Month 12 | Do Lanes A and B clear the cash floor? | Continue · restructure the offer · stop |
| **D2** | Month 30–36 | Is Phase 3 worth opening? | Open it · **formally close it and reinvest in Lane D** |

**D2's default is now "close it and reinvest".** Given your steer, Phase 3 should only be opened if
gate 1 (a ≥ USD 20m contractible pipeline) and gate 7 (an anchor investor) have arrived
*unprompted* out of Phase 2 — that is, if the market is pulling you into structuring rather than
you pushing toward it. Anything less and the right answer is to put the same effort into Lane D,
which compounds without capital and without headcount.

---

## 6. What actually blocks you right now

Of the twenty-one decisions above, **five block everything else.** The rest can wait, and treating
them as though they cannot is the main way this stalls before it starts:

1. **D-02 — the market.** Everything is downstream.
2. **D-04 — the regulatory posture.** Determines how every engagement letter is written.
3. **D-05 — the offer and its price.** Nothing can be sold until it exists as a signable scope.
4. **D-06 — data-rights scope.** The only irreversible one, and it must precede client one.
5. **D-08 — runway.** Sets D1's date and bounds every other choice.

D-04 and D-06 are the same counsel conversation. D-02 and D-05 are yours and need no external
input. D-08 is arithmetic you already have.

**Everything else in this register can be decided after you have talked to ten people** — and
several of them will be decided *by* those conversations, which is a better way to settle them
than deciding in advance.
