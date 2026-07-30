#!/usr/bin/env python3
"""Validate the RT-1 origination schema, and optionally a dataset against it.

Two modes:

    python3 risk-tools/tools/validate_schema.py
        Check the schema definition itself is well-formed and internally
        consistent. This runs in CI.

    python3 risk-tools/tools/validate_schema.py --data <dir>
        Check a directory of CSVs (originator.csv, group.csv, member.csv,
        loan.csv, event.csv) against the schema: required fields present,
        enums respected, referential integrity intact.

The schema is a data contract with people in the field. A contract nobody
checks is a suggestion, so this is deliberately strict about the schema file
itself - a malformed enum or a missing rationale fails the build.

Python 3 stdlib only, same as the rest of the toolchain.
"""

import argparse
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA = os.path.join(ROOT, "risk-tools", "schema", "rt-1-origination-schema.csv")

COLUMNS = [
    "Field_ID", "Label", "Entity", "Description", "Type", "Allowed_Values",
    "Required", "Capture", "Validation", "Privacy", "Critical_Path", "Why_It_Matters",
]
ENTITIES = {"originator", "group", "member", "loan", "event"}
TYPES = {"string", "integer", "decimal", "date", "boolean", "enum"}
REQUIREDNESS = {"required", "optional"}
CAPTURE = {"origination", "updated", "derived"}
PRIVACY = {"public", "private", "sensitive", "derived"}
YESNO = {"yes", "no"}

# Minimum length for the rationale column. A field that cannot justify itself in
# a sentence is a field somebody will have to collect in a meeting for no reason.
MIN_RATIONALE = 60


def load_schema():
    with open(SCHEMA, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != COLUMNS:
            raise SystemExit("Schema columns changed.\n  expected: %s\n  found:    %s"
                             % (COLUMNS, reader.fieldnames))
        return [dict(r) for r in reader]


def check_schema(rows):
    """Structural checks on the schema definition itself."""
    errors, warnings = [], []
    seen = set()

    for i, row in enumerate(rows, start=2):        # +2: header is line 1
        fid = row["Field_ID"]
        where = "%s (line %d)" % (fid or "<blank>", i)

        if not fid:
            errors.append("line %d: blank Field_ID" % i)
            continue
        if not re.match(r"^[a-z][a-z0-9_]*$", fid):
            errors.append("%s: Field_ID must be lower_snake_case" % where)
        if fid in seen:
            errors.append("%s: duplicate Field_ID" % where)
        seen.add(fid)

        for col, allowed in (("Entity", ENTITIES), ("Type", TYPES),
                             ("Required", REQUIREDNESS), ("Capture", CAPTURE),
                             ("Privacy", PRIVACY), ("Critical_Path", YESNO)):
            if row[col] not in allowed:
                errors.append("%s: %s=%r not in %s"
                              % (where, col, row[col], sorted(allowed)))

        if row["Type"] == "enum" and ";" not in row["Allowed_Values"]:
            errors.append("%s: type is enum but Allowed_Values has no ';' list" % where)

        if len(row["Why_It_Matters"]) < MIN_RATIONALE:
            errors.append("%s: Why_It_Matters is too short to be a real rationale" % where)

        if not row["Description"]:
            errors.append("%s: missing Description" % where)

        # Derived fields must say how they are computed, or they are just
        # untracked duplicates of something else.
        if row["Capture"] == "derived" and "=" not in row["Validation"]:
            warnings.append("%s: derived field has no formula in Validation" % where)

        # A sensitive field at row level is a privacy incident waiting to happen.
        if row["Privacy"] == "sensitive" and row["Required"] == "required":
            warnings.append("%s: sensitive AND required - is that intended?" % where)

    # Every entity needs a schema_version stamp; a mixed-vintage pool without one
    # cannot be interpreted, and it cannot be backfilled.
    for entity in ENTITIES:
        fields = [r["Field_ID"] for r in rows if r["Entity"] == entity]
        if not any(f.endswith("schema_version") for f in fields):
            if entity == "originator":
                continue                     # reference data, versioned with the group
            errors.append("entity %r has no schema_version field" % entity)

    return errors, warnings


# --- dataset validation ------------------------------------------------------

FK = {                       # child field -> (parent entity, parent field)
    "group_originator_id": ("originator", "originator_id"),
    "member_group_id": ("group", "group_id"),
    "loan_group_id": ("group", "group_id"),
    "loan_member_id": ("member", "member_id"),
    "event_loan_id": ("loan", "loan_id"),
}
PK = {"originator": "originator_id", "group": "group_id", "member": "member_id",
      "loan": "loan_id", "event": "event_id"}


def check_data(rows, data_dir):
    """Check a directory of entity CSVs against the schema."""
    errors = []
    by_entity = {}
    for entity in ENTITIES:
        by_entity[entity] = [r for r in rows if r["Entity"] == entity]

    loaded, keys = {}, {}
    for entity in ENTITIES:
        path = os.path.join(data_dir, entity + ".csv")
        if not os.path.exists(path):
            errors.append("missing %s.csv" % entity)
            continue
        with open(path, newline="", encoding="utf-8") as fh:
            loaded[entity] = list(csv.DictReader(fh))
        keys[entity] = {r.get(PK[entity]) for r in loaded[entity]}

    for entity, records in loaded.items():
        spec = {r["Field_ID"]: r for r in by_entity[entity]}
        required = [f for f, s in spec.items()
                    if s["Required"] == "required" and s["Capture"] != "derived"]
        for n, rec in enumerate(records, start=2):
            for field in required:
                if not rec.get(field, "").strip():
                    errors.append("%s.csv line %d: missing required %s" % (entity, n, field))
            for field, value in rec.items():
                s = spec.get(field)
                if not s or not value:
                    continue
                if s["Type"] == "enum":
                    allowed = {v.strip() for v in s["Allowed_Values"].split(";")}
                    if value not in allowed:
                        errors.append("%s.csv line %d: %s=%r not in enum"
                                      % (entity, n, field, value))
                if s["Type"] == "date" and not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
                    errors.append("%s.csv line %d: %s=%r is not ISO 8601"
                                  % (entity, n, field, value))
                if field in FK:
                    parent_entity, _ = FK[field]
                    if parent_entity in keys and value not in keys[parent_entity]:
                        errors.append("%s.csv line %d: %s=%r has no matching %s"
                                      % (entity, n, field, value, parent_entity))
            if len(errors) > 200:
                errors.append("... stopping after 200 errors")
                return errors
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", metavar="DIR",
                    help="also validate a directory of entity CSVs against the schema")
    args = ap.parse_args()

    rows = load_schema()
    print("Schema: %d fields across %d entities"
          % (len(rows), len({r["Entity"] for r in rows})))

    errors, warnings = check_schema(rows)
    for w in warnings:
        print("  warn  %s" % w)

    if args.data:
        errors += check_data(rows, args.data)

    if errors:
        print("\nFAILED - %d error(s):" % len(errors), file=sys.stderr)
        for e in errors:
            print("  %s" % e, file=sys.stderr)
        return 1

    critical = sum(1 for r in rows if r["Critical_Path"] == "yes")
    print("  %d required, %d critical-path, %d warnings" %
          (sum(1 for r in rows if r["Required"] == "required"), critical, len(warnings)))
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
