# The PhD by Publication Route

**Status:** Explainer, no decision attached · **Owner:** BB · **Drafted:** 2026-09-08 · **Relates to:** OQ-19, OQ-21

`docs/venture/solo-operator-track.md` §7.3 recommends framing the PhD as *deferred*, not dropped,
partly because a publication-based route stays open and costs almost nothing to preserve. This
document explains what that route actually is, what it would require, and — the part that matters
operationally — **the one term that can close it accidentally in the first six months**.

Doctoral regulations vary enormously by country and institution. Everything below is the general
shape of the route; every specific has to be checked against the named institution's own
regulations, and §6 makes that a milestone rather than an assumption.

---

## 1. Three different things that get called the same name

They are routinely conflated and they have almost nothing in common operationally.

### (a) PhD by published work — *retrospective*

You have already published a body of peer-reviewed work, often over years, sometimes with no
institutional affiliation at the time. You then apply to a university, register for a short
period, and write a **critical integrative commentary** — typically 10,000–20,000 words — arguing
that the published works together constitute a coherent, original, doctoral-level contribution.
The commentary is the thesis; the papers are the evidence.

This is the route that is interesting here, because it is the only one where **the research
happens first and the enrolment happens afterwards**.

Where it exists: well established in the **UK**, Australia, New Zealand, Scandinavia, the
Netherlands, Ireland and South Africa. Largely **absent as a distinct route in the United States**,
where the traditional dissertation remains the norm. The current pipeline in
`data/phd-programs.csv` is 15 UK programmes plus Netherlands, Belgium, Sweden, Norway and Denmark,
and zero US programmes — so the geography happens to be favourable.

### (b) Thesis by publication — *prospective*

You enrol as a normal doctoral student, but your thesis is a set of papers with an introduction
and a synthesis chapter, rather than a monograph. This is now the **default format** in much of
Northern Europe, Scandinavia and Australia, and increasingly in economics everywhere.

This is a normal PhD with a different binding. It carries the usual full-time expectation, the
usual duration, and the usual opportunity cost. It does not solve the problem the venture has.

### (c) Higher doctorate (DSc, DLitt, LLD)

Awarded for a sustained career-level body of work, usually to established academics, often decades
in. Not a route to a first doctorate. Mentioned only so it is not mistaken for (a).

**And one adjacent option worth separating: the professional doctorate (DBA, DProf).** Part-time,
practitioner-oriented, and already in the tracker at PHD-37 (Heriot-Watt, fully online),
PHD-38 (IE) and PHD-39 (Reading/Henley). A DBA **is not a PhD**, and the tracker's own note on
PHD-37 flags "if a DBA's credibility tradeoff is acceptable" as the open question. For a venture
that intends to publish and partner with economics departments, that tradeoff is real: a DBA is
weaker currency with exactly the research institutions OQ-21 needs.

---

## 2. What route (a) typically requires

Common requirements, with the caveat in the header — these are patterns, not rules:

| Requirement | Typical shape |
| :---- | :---- |
| **Number of outputs** | Usually 3–8 peer-reviewed publications. Journal articles are the safe currency; book chapters and monographs sometimes count. |
| **Authorship** | You must be **sole, first, or demonstrably lead author** on most of them, with signed statements from co-authors attesting your contribution. **This is the binding constraint — see §4.** |
| **Coherence** | The works must form one argument, not a career's worth of unrelated papers. The commentary exists to make that case. |
| **Peer review** | Working papers, policy briefs, grey literature and reports usually **do not count**, however influential. Development finance produces a great deal of exactly this kind of output. |
| **Recency and eligibility** | Many institutions cap how old the work may be (often within ~10 years) and require it to post-date your last degree. |
| **Institutional link** | Many restrict the route to their own staff or alumni. Some open it to external applicants; fewer than you would hope. |
| **Registration period** | Typically 1–2 years part-time to write the commentary, with a supervisor assigned. |
| **Examination** | A normal viva, on the papers and the commentary together. |
| **Funding** | Effectively none. There is no stipend for this route — you are self-funding a short registration, which in this case the practice pays for. |

---

## 3. Why this route fits the venture's shape unusually well

Not a general argument — a specific one. The solo track generates the raw material almost as a
by-product, and the papers are genuinely publishable because the repo has already established
that the gaps are real:

| Paper | Comes from | Why it is publishable |
| :---- | :---- | :---- |
| **Default correlation in community-originated lending** | EXP-25 | LC-08's read established that nobody has estimated this at loan level for this asset class, while LIT-038's standard method takes the parameter as an *input by assumption*. A number that is currently assumed, estimated for the first time. |
| **The cost of securitisation-ready origination** | EXP-22 | `business-plan.md` §5: "Everyone in the sector repeats it; nobody has priced it." An activity-based costing of a claim the sector treats as settled. |
| **Penetration thresholds tested at loan level** | EXP-25 secondary outcome | LIT-037's market-penetration thresholds have not been tested on loan-level data. Listed in the EXP-25 spec as a secondary outcome already. |
| **An origination data standard for community assets** | RT-1 v1.0 plus its field-cost curve | A methods and standards contribution, strengthened rather than weakened by being field-tested commercially. |
| **The coffee anchor evaluation** | EXP-09 or EXP-10 | The field trial, co-authored with the research partner who holds the grant. |

That is three to five coherent papers on one argument — **the poolability of community-originated
financial assets** — arriving on roughly the timeline Track C's Phases 1 and 2 produce them.
The coherence requirement in §2, which trips up most retrospective applicants, is satisfied by
construction here rather than by retrofitting.

---

## 4. The one thing that can close this route by accident

**Authorship position, agreed in the research MOU.**

`solo-operator-track.md` §7 argues that the academic partner should be principal investigator,
because that is what supplies grant eligibility and ethics approval. That is correct and it
should stand. But **PI on the grant and first author on the paper are separate things**, and if
they are allowed to travel together by default, route (a) is damaged before a single paper exists:
the requirement is lead authorship on most outputs, and a body of work where you are consistently
second or third author does not meet it.

So the MOU has to say, in writing and at the start:

1. **Who is first author on which paper**, mapped to who does which work. On EXP-25 and EXP-22 the
   data access, the instrument design and the costing method are yours; the econometrics and the
   ethics approval are theirs. First authorship on those two is a reasonable ask and a much easier
   one to make in month 2 than in year 3.
2. **That co-author contribution statements will be provided on request** — the signed attestations
   route (a) requires at application.
3. **That the partner holds PI status and ethics approval**, explicitly, so nothing above is read
   as claiming otherwise.

None of this is adversarial; it is the ordinary content of a research collaboration agreement, and
academics negotiate it routinely. It only becomes a problem when nobody raises it, which is the
default.

Two smaller things to preserve at the same near-zero cost:

- **Take the practitioner affiliation** (OQ-21 Form 3). Several institutions restrict route (a) to
  staff and alumni; an affiliate or visiting-fellow title can create the institutional link that
  makes an application admissible at all, years before it is submitted.
- **Publish in journals, not just as working papers.** The natural output of this venture is a
  policy brief or a DFI report. Those do not count. If a paper is worth writing, target a
  peer-reviewed journal even though it is slower.

---

## 5. The honest case against

Not reasons to rule it out, but the things that make it a by-product rather than a plan:

- **Publication is slow.** In economics, two to four years from first submission to print in a good
  journal is unremarkable. "Papers by year four" means *writing* by year two, and a first paper
  submitted at year three appears at year five or six.
- **The route is not equally regarded everywhere.** Some hiring committees and some funders treat
  it as a lesser doctorate. If the goal is a tenure-track academic career, the traditional route is
  still the safer currency. If the goal is credibility with DFIs, partners and research
  collaborators, the gap is much smaller and the published papers do most of the work anyway.
- **No training, no cohort, no supervision to speak of.** Route (a) assumes you already know how to
  do research to publishable standard. The methods scaffolding a normal PhD provides — and which
  `data/phd-programs.csv` scores several programmes highly for, PHD-01 among them — is
  simply absent. The research partner has to supply it instead, which is another reason §4's MOU
  matters.
- **It cannot be forced.** If the papers do not get accepted, there is no route. Enrolment is a
  commitment that produces a thesis; publication is an outcome that might not arrive.
- **Eligibility caps can bite quietly.** A ten-year recency window is generous now and is not
  generous if the first paper appears in year six and the application is made in year twelve.

---

## 6. What this means in practice

**Treat it as a by-product to keep available, not as a goal to organise around.** The asymmetry is
the whole argument: preserving the option costs an authorship clause and an affiliate title;
closing it accidentally costs the option entirely and cannot be undone once three papers carry the
wrong author order.

Three concrete actions, all cheap and all early:

1. **Put the authorship terms in the research MOU** (§4) — part of M-38's research outreach, not a
   later negotiation.
2. **Take the practitioner affiliation** — OQ-21 Form 3, same window.
3. **Score the existing pipeline for the route.** `data/phd-programs.csv` holds 52 scored
   programmes and, on a scan of the `Format`, `Advantages` and `Fit_Notes` columns, **exactly one
   row mentions a publication route at all** (PHD-08) — so the rubric never asked the question.
   Two candidates already stand out for a venture-parallel doctorate on the existing notes:
   **PHD-26 (UNU-MERIT / Maastricht)**, whose "Dual Career" track is described in the tracker as
   "purpose-built for professionals running parallel work", and the Tier-1 UK pair **PHD-14
   (Manchester)** and **PHD-15 (UEA)**, both "part-time available" and fieldwork-native. Logged as
   **M-43**: check each shortlisted institution's regulations for whether route (a) exists, whether
   external applicants are eligible, and what the recency cap is.

Then decide at year three or four, when there are actually papers — which is the only point at
which the question can be answered rather than guessed.
