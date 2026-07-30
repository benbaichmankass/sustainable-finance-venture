#!/usr/bin/env python3
"""RT-2 scaffold: rules-based underwriting scorecard over RT-1 data.

    python3 risk-tools/tools/generate_dataset.py --out /tmp/synth
    python3 risk-tools/tools/score_loans.py --data /tmp/synth

RULES-BASED ON PURPOSE, NOT AS A STEPPING STONE TO ML. There is no repayment
history to train or validate on. A model fitted on borrowed priors would be a
confident guess wearing the costume of a measurement, and it would be
impossible to explain to a borrower who was declined. When a real track record
exists, the honest upgrade path is to backtest THIS scorecard against it
first - a scorecard that beats chance is a baseline any model has to clear.

Every decision carries its reasons. That is not decoration: LIT-014 puts
consumer protection, not systemic risk, at the centre of savings-group
regulation, and "the model said no" is not a reason anyone can contest.

Python 3 stdlib only.
"""

import argparse
import csv
import os
import sys
from collections import Counter, defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_VERSION = "0.1"

# Each rule: (name, weight, test, human-readable reason when it FAILS).
# Weights are judgement, not estimates - they encode which signals the
# literature and the schema say should matter, in what rough order. They are
# the first thing that should be replaced by measurement.
BANDS = [
    ("approve", 70), ("approve_with_conditions", 55), ("refer", 40), ("decline", 0),
]


def load(data_dir):
    out = {}
    for name in ("group", "member", "loan"):
        with open(os.path.join(data_dir, name + ".csv"), newline="", encoding="utf-8") as fh:
            out[name] = list(csv.DictReader(fh))
    return out


def f(row, key, default=0.0):
    try:
        return float(row.get(key, "") or default)
    except ValueError:
        return default


def score_loan(loan, member, group):
    """Return (score 0-100, band, reasons, limit_multiple).

    Reasons are recorded for BOTH directions - what helped and what hurt - so
    a marginal decision can be explained and argued with.
    """
    score = 50.0
    plus, minus = [], []

    # --- borrower track record (the strongest signal available pre-data) -----
    prior_cycles = f(member, "member_prior_cycles")
    if prior_cycles >= 3:
        score += 12; plus.append("member has completed %d prior cycles" % prior_cycles)
    elif prior_cycles >= 1:
        score += 6; plus.append("member has completed %d prior cycle(s)" % prior_cycles)
    else:
        score -= 8; minus.append("no completed savings cycles - no track record")

    prior_loans = f(loan, "loan_prior_loans_count")
    if prior_loans >= 3:
        score += 10; plus.append("%d prior loans in this group" % prior_loans)
    elif prior_loans >= 1:
        score += 5; plus.append("%d prior loan(s) in this group" % prior_loans)
    else:
        minus.append("first loan for this borrower")

    # --- leverage: the classic savings-group underwriting ratio ---------------
    ltsr = f(loan, "loan_to_savings_ratio")
    if ltsr <= 1.5:
        score += 12; plus.append("loan is %.1fx savings - conservative" % ltsr)
    elif ltsr <= 2.5:
        score += 4; plus.append("loan is %.1fx savings - within norm" % ltsr)
    elif ltsr <= 3.5:
        score -= 6; minus.append("loan is %.1fx savings - above typical limit" % ltsr)
    else:
        score -= 18; minus.append("loan is %.1fx savings - highly leveraged" % ltsr)

    # --- group maturity ------------------------------------------------------
    cycle_no = f(group, "group_cycle_number")
    if cycle_no >= 4:
        score += 10; plus.append("group is in cycle %d - has survived %d share-outs"
                                 % (cycle_no, cycle_no - 1))
    elif cycle_no >= 2:
        score += 5; plus.append("group is in cycle %d" % cycle_no)
    else:
        score -= 10; minus.append("group is in its first cycle - unproven")

    members = f(group, "group_member_count")
    if members >= 20:
        score += 5; plus.append("%d members - broad joint-liability base" % members)
    elif members < 12:
        score -= 8; minus.append("only %d members - thin joint-liability base" % members)

    # --- guarantee -----------------------------------------------------------
    gtype = loan.get("loan_guarantee_type", "")
    coverage = f(loan, "loan_guarantee_coverage_pct")
    if gtype == "cash_savings_pledge":
        score += 8; plus.append("cash savings pledged")
    elif gtype == "group_joint_liability" and coverage >= 80:
        score += 6; plus.append("joint liability at %.0f%% coverage" % coverage)
    elif gtype == "none":
        score -= 15; minus.append("no guarantee structure")
    elif coverage < 50:
        score -= 6; minus.append("guarantee covers only %.0f%%" % coverage)

    # --- the share-out constraint -------------------------------------------
    # This one only exists because the RT-1 schema captures cycle length. A loan
    # maturing after share-out has to survive the moment the group empties its
    # box - the joint-liability backing is at its weakest exactly when the loan
    # is due. A generic scorecard has no way to see this.
    term = f(loan, "loan_term_days")
    cycle_days = f(group, "group_cycle_length_months") * 30
    if cycle_days and term > cycle_days * 0.85:
        score -= 12
        minus.append("term (%dd) runs close to or past share-out (%dd cycle)"
                     % (term, cycle_days))

    # --- correlated exposure -------------------------------------------------
    # An agricultural-input loan repaid from the same harvest it funds is
    # correlated risk hiding inside an apparently diversified pool.
    if (loan.get("loan_purpose_code") == "agriculture_input"
            and member.get("member_primary_livelihood") == "smallholder_farming"):
        score -= 7
        minus.append("agricultural input loan repaid from the harvest it funds")

    if loan.get("loan_purpose_code") == "emergency_consumption":
        score -= 5; minus.append("emergency consumption - no income from proceeds")

    score = max(0.0, min(100.0, score))
    band = next(b for b, floor in BANDS if score >= floor)

    # Limit as a multiple of savings, tightened by band. Deliberately expressed
    # as a multiple rather than an amount: it must hold across currencies.
    limit_multiple = {"approve": 3.0, "approve_with_conditions": 2.0,
                      "refer": 1.5, "decline": 0.0}[band]
    return round(score, 1), band, plus, minus, limit_multiple


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="directory of RT-1 entity CSVs")
    ap.add_argument("--out", help="write scored loans to this CSV")
    ap.add_argument("--explain", metavar="LOAN_ID", help="print the full reasoning for one loan")
    args = ap.parse_args()

    d = load(args.data)
    groups = {g["group_id"]: g for g in d["group"]}
    members = {m["member_id"]: m for m in d["member"]}

    scored, bands = [], Counter()
    for loan in d["loan"]:
        m = members.get(loan["loan_member_id"], {})
        g = groups.get(loan["loan_group_id"], {})
        score, band, plus, minus, mult = score_loan(loan, m, g)
        bands[band] += 1
        savings = f(loan, "loan_borrower_savings_at_disbursement")
        scored.append({
            "loan_id": loan["loan_id"],
            "score": score,
            "band": band,
            "requested": f(loan, "loan_principal"),
            "limit": round(savings * mult, 2),
            "reasons_for": " | ".join(plus),
            "reasons_against": " | ".join(minus),
            "model_version": MODEL_VERSION,
            "basis": "SYNTHETIC - uncalibrated rules-based scorecard",
        })

    if args.explain:
        row = next((r for r in scored if r["loan_id"] == args.explain), None)
        if not row:
            raise SystemExit("no such loan: %s" % args.explain)
        print("Loan %s - score %.1f -> %s" % (row["loan_id"], row["score"], row["band"]))
        print("  requested %.2f, limit %.2f" % (row["requested"], row["limit"]))
        print("  in favour:")
        for r in row["reasons_for"].split(" | "):
            print("    + %s" % r)
        print("  against:")
        for r in (row["reasons_against"].split(" | ") if row["reasons_against"] else ["(none)"]):
            print("    - %s" % r)
        return 0

    print("RT-2 SCORECARD v%s - SYNTHETIC, uncalibrated" % MODEL_VERSION)
    print("  %d loans scored\n" % len(scored))
    total = len(scored)
    for band, _ in BANDS:
        n = bands[band]
        bar = "#" * int(40 * n / total) if total else ""
        print("  %-24s %5d  %5.1f%%  %s" % (band, n, 100 * n / total if total else 0, bar))

    over = [s for s in scored if s["limit"] and s["requested"] > s["limit"]]
    declined = [s for s in scored if s["band"] == "decline"]
    print("\n  %d loans (%.1f%%) exceed the limit the scorecard would set"
          % (len(over), 100 * len(over) / total if total else 0))
    print("  %d loans (%.1f%%) would be declined outright"
          % (len(declined), 100 * len(declined) / total if total else 0))

    reasons = Counter()
    for s in scored:
        for r in s["reasons_against"].split(" | "):
            if r:
                reasons[r.split(" - ")[0].split(" (")[0]] += 1
    print("\n  Most common reasons against:")
    for r, n in reasons.most_common(6):
        print("    %5d  %s" % (n, r[:70]))

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(scored[0].keys()),
                               quoting=csv.QUOTE_ALL, lineterminator="\n")
            w.writeheader()
            for s in scored:
                w.writerow(s)
        print("\nWrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
