#!/usr/bin/env python3
"""End-to-end check that the RT toolchain holds together.

    python3 risk-tools/tools/test_toolchain.py

Runs in CI. Proportionate rather than exhaustive - it checks the properties
that would silently corrupt every downstream number if they broke, and skips
the ones that would be obvious.

What it asserts:
  1. The generator's output validates against the RT-1 schema.
     (Otherwise the schema is a document, not a contract.)
  2. The validator actually rejects corrupt data.
     (A check that passes everything is worse than no check.)
  3. The scorecard is monotone in leverage - more debt against the same
     savings never scores better.
  4. Every declined loan carries at least one reason.
     (An unexplained decline is not defensible to a borrower or a regulator.)
  5. The RT-3 arrears signal leads realised write-offs.
     (The entire premise of an early-warning system.)
  6. The RT-5 waterfall conserves cash on every path.
     (A leak invalidates every tranche number.)

Python 3 stdlib only.
"""

import csv
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

PASS, FAIL = [], []


def check(name, condition, detail=""):
    (PASS if condition else FAIL).append((name, detail))
    print("  %s  %s%s" % ("PASS" if condition else "FAIL", name,
                          ("  — " + detail) if detail else ""))


def run(*args):
    return subprocess.run([sys.executable] + list(args), capture_output=True, text=True)


def main():
    print("RT toolchain end-to-end check\n")
    tmp = tempfile.mkdtemp(prefix="sfv-test-")
    try:
        # --- 1. generator output conforms to the schema ----------------------
        gen = run(os.path.join(HERE, "generate_dataset.py"), "--out", tmp, "--groups", "120")
        check("generator runs", gen.returncode == 0, gen.stderr.strip()[:120])

        val = run(os.path.join(HERE, "validate_schema.py"), "--data", tmp)
        check("generated data validates against RT-1 schema", val.returncode == 0,
              val.stderr.strip().splitlines()[-1] if val.returncode else "")

        # --- 2. the validator has teeth --------------------------------------
        bad = tempfile.mkdtemp(prefix="sfv-bad-")
        for f in os.listdir(tmp):
            shutil.copy(os.path.join(tmp, f), bad)
        path = os.path.join(bad, "loan.csv")
        rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
        fields = list(rows[0].keys())
        rows[0]["loan_purpose_code"] = "not_a_real_purpose"
        rows[1]["loan_group_id"] = "GRP-999999"
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
            w.writeheader()
            for r in rows:
                w.writerow(r)
        bad_run = run(os.path.join(HERE, "validate_schema.py"), "--data", bad)
        check("validator rejects a bad enum and a dangling foreign key",
              bad_run.returncode != 0)
        shutil.rmtree(bad, ignore_errors=True)

        # --- 3 & 4. scorecard properties -------------------------------------
        from score_loans import score_loan

        group = {"group_cycle_number": "4", "group_member_count": "22",
                 "group_cycle_length_months": "12"}
        member = {"member_prior_cycles": "2", "member_primary_livelihood": "petty_trade"}
        base = {"loan_prior_loans_count": "2", "loan_guarantee_type": "group_joint_liability",
                "loan_guarantee_coverage_pct": "90", "loan_term_days": "150",
                "loan_purpose_code": "trade_stock", "loan_principal": "500",
                "loan_borrower_savings_at_disbursement": "250"}
        scores = []
        for ratio in (1.0, 2.0, 3.0, 5.0):
            loan = dict(base, loan_to_savings_ratio=str(ratio))
            scores.append(score_loan(loan, member, group)[0])
        check("scorecard is monotone in leverage",
              all(a >= b for a, b in zip(scores, scores[1:])),
              "scores at 1x/2x/3x/5x savings: %s" % scores)

        with open(os.path.join(tmp, "loan.csv"), newline="", encoding="utf-8") as fh:
            loans = list(csv.DictReader(fh))
        with open(os.path.join(tmp, "member.csv"), newline="", encoding="utf-8") as fh:
            members = {m["member_id"]: m for m in csv.DictReader(fh)}
        with open(os.path.join(tmp, "group.csv"), newline="", encoding="utf-8") as fh:
            groups = {g["group_id"]: g for g in csv.DictReader(fh)}

        unexplained = 0
        for loan in loans:
            s, band, plus, minus, _ = score_loan(
                loan, members.get(loan["loan_member_id"], {}),
                groups.get(loan["loan_group_id"], {}))
            if band in ("decline", "refer") and not minus:
                unexplained += 1
        check("every declined or referred loan carries a reason", unexplained == 0,
              "%d unexplained" % unexplained if unexplained else "")

        # --- 5. arrears lead write-offs --------------------------------------
        # The property is that the arrears signal RUNS AHEAD of realised loss,
        # not that write-offs are literally zero on a given date - that depends
        # on the seed and the sample size, and asserting it made this test fail
        # for a reason that said nothing about the tool.
        from monitor_portfolio import analyse, load
        data = load(tmp)
        early = analyse(data, "2027-05-31")
        late = analyse(data, "2028-06-30")
        early_share = early["written_off"] / late["written_off"] if late["written_off"] else 1.0
        arrears_seen = sum(early["new_arrears_by_month"].values())
        check("arrears run ahead of realised loss",
              arrears_seen > 0 and early_share < 0.20,
              "at 2027-05-31: %d loans already in arrears, %.0f%% of eventual write-offs booked"
              % (arrears_seen, 100 * early_share))
        check("write-offs do eventually materialise", late["written_off"] > 0,
              "final written off %.0f" % late["written_off"])

        # --- 6. waterfall conserves cash -------------------------------------
        # The assertion lives inside waterfall(); exercising it across a wide
        # range of collection levels is what makes it a test rather than a hope.
        from simulate_portfolio import waterfall, load_config, parse_scenarios, load_scenarios
        cfg = load_config()
        scen = parse_scenarios(load_scenarios())
        leaked = False
        for s in scen:
            for collections in (0.0, 1_000.0, 5_000_000.0, 50_000_000.0):
                try:
                    waterfall(10_000_000.0, collections, cfg, s)
                except AssertionError:
                    leaked = True
        check("waterfall conserves cash across scenarios and collection levels", not leaked)

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
