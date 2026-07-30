#!/usr/bin/env python3
"""Generate a synthetic dataset that conforms to the RT-1 origination schema.

    python3 risk-tools/tools/generate_dataset.py --out /tmp/synth --groups 300

Emits five CSVs - originator, group, member, loan, event - with the exact
field names and domains declared in risk-tools/schema/rt-1-origination-schema.csv.

WHY THIS EXISTS, beyond feeding RT-2 and RT-3: its output is validated by
validate_schema.py --data. That turns the schema from a document into
something executable. If the schema and the generator drift apart, the check
fails - which is the only way to know a 57-field contract is still coherent
before anyone tries to collect against it in a village.

EVERYTHING IT PRODUCES IS SYNTHETIC. The behavioural assumptions (who repays,
who falls into arrears, when) are plausible-looking placeholders, not
estimates. See risk-tools/rt-5-simulator.md.

Python 3 stdlib only.
"""

import argparse
import csv
import math
import os
import random
import sys
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_VERSION = "0.1"

LIVELIHOODS = ["smallholder_farming", "livestock", "petty_trade", "wage_labour",
               "salaried", "artisan", "remittance_dependent", "mixed"]
PURPOSES = ["agriculture_input", "livestock", "trade_stock", "equipment", "education",
            "health", "housing", "emergency_consumption", "energy_asset"]
ROLES = ["member"] * 12 + ["chair", "secretary", "treasurer", "box_keeper", "key_holder"]
AGE_BANDS = ["under_25", "25_34", "35_44", "45_54", "55_plus"]
CLIMATE = ["arid", "semi_arid", "sub_humid", "humid", "highland"]


def write(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def generate(n_groups, seed, out_dir):
    rng = random.Random(seed)
    os.makedirs(out_dir, exist_ok=True)
    base = date(2027, 1, 1)

    n_orig = max(1, n_groups // 80)
    originators = [{
        "originator_id": "ORG-%04d" % i,
        "originator_type": rng.choice(["ngo", "mfi", "savings_group_federation", "cooperative"]),
        "originator_country": rng.choice(["KE", "TZ", "UG", "RW", "IL"]),
        "originator_regulated": rng.choice(["true", "false"]),
    } for i in range(n_orig)]

    groups, members, loans, events = [], [], [], []

    for g in range(n_groups):
        cycle_len = rng.choice([9, 12, 12, 12, 15])
        formation = base - timedelta(days=rng.randrange(200, 3000))
        n_members = rng.randrange(12, 31)
        gid = "GRP-%06d" % g
        # Cycle start anchors the share-out date, which is the liquidity event a
        # loan maturing past it has to survive. RT-2 keys off exactly this.
        cycle_start = base + timedelta(days=rng.randrange(0, 90))
        groups.append({
            "group_id": gid,
            "group_originator_id": rng.choice(originators)["originator_id"],
            "group_formation_date": formation.isoformat(),
            "group_cycle_number": max(1, (base - formation).days // (cycle_len * 30) + 1),
            "group_cycle_length_months": cycle_len,
            "group_member_count": n_members,
            "group_governance_model": rng.choice(
                ["standard_vsla", "standard_vsla", "standard_vsla", "federated", "ngo_managed"]),
            "group_meeting_frequency": rng.choice(["weekly", "weekly", "fortnightly", "monthly"]),
            "group_savings_balance": round(rng.uniform(400, 6000), 2),
            "group_currency_code": "USD",
            "group_admin1": "REG-%02d" % rng.randrange(12),
            "group_admin2": "",
            "group_climate_zone": rng.choice(CLIMATE),
            "group_savix_id": "",
            "group_schema_version": SCHEMA_VERSION,
            "_cycle_start": cycle_start.isoformat(),        # internal, stripped on write
        })

        for m in range(n_members):
            members.append({
                "member_id": "MEM-%08d" % len(members),
                "member_group_id": gid,
                "member_join_date": (formation + timedelta(days=rng.randrange(0, 400))).isoformat(),
                "member_role": rng.choice(ROLES),
                "member_sex": rng.choice(["female", "female", "male", "undisclosed"]),
                "member_age_band": rng.choice(AGE_BANDS),
                "member_primary_livelihood": rng.choice(LIVELIHOODS),
                "member_prior_cycles": rng.randrange(0, 6),
                "member_schema_version": SCHEMA_VERSION,
            })

    members_by_group = {}
    for m in members:
        members_by_group.setdefault(m["member_group_id"], []).append(m)

    for grp in groups:
        borrowers = rng.sample(members_by_group[grp["group_id"]],
                               k=max(1, int(grp["group_member_count"] * rng.uniform(0.25, 0.55))))
        cycle_start = date.fromisoformat(grp["_cycle_start"])
        for mem in borrowers:
            savings = round(rng.uniform(20, 600), 2)
            principal = round(min(savings * rng.uniform(0.8, 3.5), 3000), 2)
            if principal < 20:
                continue
            disb = cycle_start + timedelta(days=rng.randrange(0, 120))
            term = rng.choice([90, 120, 150, 180, 210])
            freq = grp["group_meeting_frequency"]
            step = {"weekly": 7, "fortnightly": 14, "monthly": 30}.get(freq, 30)
            instalments = max(1, term // step)
            lid = "LN-%010d" % len(loans)
            loans.append({
                "loan_id": lid,
                "loan_group_id": grp["group_id"],
                "loan_member_id": mem["member_id"],
                "loan_disbursement_date": disb.isoformat(),
                "loan_principal": principal,
                "loan_currency_code": "USD",
                "loan_term_days": term,
                "loan_repayment_frequency": freq if freq != "irregular" else "monthly",
                "loan_scheduled_instalments": instalments,
                "loan_charge_rate_pct": rng.choice([5.0, 10.0, 10.0, 15.0]),
                "loan_charge_basis": "flat_per_cycle",
                "loan_purpose_code": rng.choice(PURPOSES),
                "loan_guarantee_type": rng.choice(
                    ["group_joint_liability", "group_joint_liability", "cash_savings_pledge",
                     "social_collateral"]),
                "loan_guarantee_coverage_pct": round(rng.uniform(40, 100), 1),
                "loan_borrower_savings_at_disbursement": savings,
                "loan_to_savings_ratio": round(principal / savings, 3) if savings else 0,
                "loan_prior_loans_count": rng.randrange(0, 8),
                "loan_first_loss_provider_id": "",
                "loan_schema_version": SCHEMA_VERSION,
                "_cycle_start": grp["_cycle_start"],
                "_cycle_length_months": grp["group_cycle_length_months"],
            })

    # --- event stream --------------------------------------------------------
    # The part RT-3 consumes. Behaviour is deliberately not uniform: a minority
    # of loans slip into arrears and a smaller subset default, with arrears
    # arriving before default so an early-warning system has something real to
    # detect rather than a step change at write-off.
    for loan in loans:
        step = {"weekly": 7, "fortnightly": 14, "monthly": 30}[loan["loan_repayment_frequency"]]
        n = loan["loan_scheduled_instalments"]
        principal = loan["loan_principal"]
        charge = principal * loan["loan_charge_rate_pct"] / 100.0
        per = (principal + charge) / n
        disb = date.fromisoformat(loan["loan_disbursement_date"])

        trouble = rng.random() < 0.14                # falls behind at some point
        defaults = trouble and rng.random() < 0.35   # and a minority never recover
        stumble_at = rng.randrange(1, n) if trouble and n > 1 else n

        balance = principal
        dpd = 0
        for i in range(1, n + 1):
            due = disb + timedelta(days=step * i)
            if defaults and i > stumble_at:
                if i == stumble_at + 1:
                    events.append(_event(loan, due, "missed_payment", 0.0, balance, dpd))
                    dpd = step
                elif i == stumble_at + 2:
                    dpd += step
                    events.append(_event(loan, due, "arrears_flagged", 0.0, balance, dpd))
                elif i == n:
                    recovered = round(balance * rng.uniform(0.2, 0.7), 2)
                    events.append(_event(loan, due, "recovery", recovered,
                                         round(balance - recovered, 2), dpd))
                    events.append(_event(loan, due + timedelta(days=30), "write_off", 0.0,
                                         0.0, dpd + 30))
                else:
                    dpd += step
                    events.append(_event(loan, due, "missed_payment", 0.0, balance, dpd))
                continue

            late = trouble and i >= stumble_at and rng.random() < 0.5
            if late:
                dpd = step
                events.append(_event(loan, due, "missed_payment", 0.0, balance, dpd))
                paid = round(min(per * 2, balance + charge / n), 2)
                balance = max(0.0, round(balance - paid * 0.8, 2))
                events.append(_event(loan, due + timedelta(days=step), "partial_repayment",
                                     paid, balance, dpd))
                dpd = 0
            else:
                paid = round(min(per, balance + charge / n), 2)
                balance = max(0.0, round(balance - paid * 0.85, 2))
                events.append(_event(loan, due, "scheduled_repayment", paid, balance, 0))

    for g in groups:
        g.pop("_cycle_start", None)
    loan_out = [{k: v for k, v in l.items() if not k.startswith("_")} for l in loans]

    write(os.path.join(out_dir, "originator.csv"), originators, list(originators[0].keys()))
    write(os.path.join(out_dir, "group.csv"), groups, list(groups[0].keys()))
    write(os.path.join(out_dir, "member.csv"), members, list(members[0].keys()))
    write(os.path.join(out_dir, "loan.csv"), loan_out, list(loan_out[0].keys()))
    write(os.path.join(out_dir, "event.csv"), events, list(events[0].keys()))

    return {"originators": len(originators), "groups": len(groups), "members": len(members),
            "loans": len(loan_out), "events": len(events)}


_EVENT_N = [0]


def _event(loan, when, kind, amount, balance, dpd):
    _EVENT_N[0] += 1
    return {
        "event_id": "EV-%012d" % _EVENT_N[0],
        "event_loan_id": loan["loan_id"],
        "event_date": when.isoformat(),
        "event_type": kind,
        "event_amount": round(amount, 2),
        "event_principal_component": "",
        "event_balance_after": round(balance, 2),
        "event_days_past_due": dpd,
        "event_recorded_by_role": "secretary",
        "event_schema_version": SCHEMA_VERSION,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="/tmp/sfv-synthetic", help="output directory")
    ap.add_argument("--groups", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20260730)
    args = ap.parse_args()

    print("SYNTHETIC DATASET - illustrative only, conforms to RT-1 v%s" % SCHEMA_VERSION)
    counts = generate(args.groups, args.seed, args.out)
    for k, v in counts.items():
        print("  %-12s %6d" % (k, v))
    print("Wrote %s" % args.out)
    print("\nValidate it against the schema with:")
    print("  python3 risk-tools/tools/validate_schema.py --data %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
