#!/usr/bin/env python3
"""Generate dashboard/data.js from the repo's source files.

The dashboard has no state of its own: everything it displays is read out of
the CSVs in data/, the literature matrix, and the markdown docs. Run this
after changing any of those, and commit the regenerated data.js alongside.

    python3 dashboard/build.py

Python 3 stdlib only - no install step, no toolchain.
"""

import csv
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dashboard", "data.js")
OUT_PRIVATE = os.path.join(ROOT, "dashboard", "data.private.js")

# --- structured trackers -----------------------------------------------------
# key -> path relative to repo root
TABLES = {
    "literature": "literature/lit-matrix.csv",
    "openQuestions": "data/open-questions.csv",
    "productLines": "data/product-lines.csv",
    "riskTools": "data/risk-tools.csv",
    "macroIndicators": "data/macro-indicators.csv",
    "macroLog": "data/macro-log.csv",
    "partners": "data/partner-tracker.csv",
    "phdPrograms": "data/phd-programs.csv",
    "milestones": "data/milestones.csv",
    "memos": "data/synthesis-memos.csv",
    "resources": "data/resources.csv",
}

# --- private overlay ---------------------------------------------------------
# Gitignored files that add the columns a public repo must not carry: named
# individuals, relationship status, Vault links. Merged by ID when present, so
# a local build shows the whole picture and a public build shows only the
# public tier. See docs/publishing.md.
OVERLAYS = {
    "partners": "private/partner-contacts.csv",
    "phdPrograms": "private/phd-applications.csv",
    # Fills in the blank URL on the Vault/tracker rows of data/resources.csv.
    # Keyed by ID like the others, so the public tier keeps the row and its
    # description and only the link is withheld.
    "resources": "private/pointers.csv",
}

# --- document library --------------------------------------------------------
# directory -> display category. Files are picked up recursively.
DOC_DIRS = [
    (".", "Project", False),
    ("docs", "Planning", True),
    ("literature/notes", "Synthesis memos", True),
    ("product-design", "Product & business", True),
    ("risk-tools", "Risk tools", True),
    ("archive/google-drive", "Archive", True),
    (".claude/skills", "AI skills", True),
]

SKIP_FILES = {"data.js"}


def read_table(relpath):
    path = os.path.join(ROOT, relpath)
    if not os.path.exists(path):
        print("  ! missing: %s" % relpath, file=sys.stderr)
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        rows = [dict(r) for r in csv.DictReader(fh)]
    # strip whitespace-only values to empty string for consistent rendering
    for row in rows:
        for key in list(row):
            row[key] = (row[key] or "").strip()
    return rows


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def split_frontmatter(text):
    """Return (meta_dict, body). Skill files carry YAML frontmatter that should be
    surfaced as metadata rather than rendered as document text."""
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def title_of(text, fallback):
    """First markdown H1, else the filename."""
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def prettify(name):
    return name.replace("-", " ").replace("_", " ").strip().capitalize()


def collect_docs():
    docs = []
    seen = set()
    for reldir, category, recursive in DOC_DIRS:
        base = os.path.join(ROOT, reldir)
        if not os.path.isdir(base):
            continue
        walker = os.walk(base) if recursive else [(base, [], os.listdir(base))]
        for dirpath, dirnames, filenames in walker:
            dirnames[:] = [d for d in dirnames if d != ".git"]
            for filename in sorted(filenames):
                if not filename.endswith(".md") or filename in SKIP_FILES:
                    continue
                full = os.path.join(dirpath, filename)
                rel = os.path.relpath(full, ROOT)
                if rel in seen:
                    continue
                seen.add(rel)
                with open(full, encoding="utf-8") as fh:
                    text = fh.read()
                meta, body = split_frontmatter(text)
                fallback = meta.get("name") or prettify(filename[:-3])
                docs.append(
                    {
                        "path": rel,
                        "category": category,
                        "title": title_of(body, fallback),
                        "summary": meta.get("description", ""),
                        "words": len(body.split()),
                        "body": body,
                    }
                )
    docs.sort(key=lambda d: (d["category"], d["path"]))
    return docs


def merge_overlay(rows, relpath):
    """Merge a private overlay onto public rows, matching on ID.

    Returns (rows, applied). Missing overlay is the normal case for a public
    build - not an error. Overlay rows whose ID isn't in the public table are
    reported, since that usually means an ID was renamed on one side only.
    """
    path = os.path.join(ROOT, relpath)
    if not os.path.exists(path):
        return rows, False
    overlay = {r["ID"]: r for r in read_table(relpath) if r.get("ID")}
    seen = set()
    for row in rows:
        extra = overlay.get(row.get("ID"))
        if extra:
            seen.add(row["ID"])
            for key, value in extra.items():
                if key != "ID":
                    row[key] = value
    orphans = set(overlay) - seen
    if orphans:
        print("  ! overlay %s has IDs not in the public table: %s"
              % (relpath, ", ".join(sorted(orphans))), file=sys.stderr)
    return rows, True


def counts(rows, field):
    out = {}
    for row in rows:
        value = row.get(field) or "Unspecified"
        out[value] = out.get(value, 0) + 1
    return out


def main():
    private = "--public" not in sys.argv
    print("Building dashboard data%s..." % ("" if private else " (public tier only)"))
    data = {}
    applied = []
    for key, relpath in TABLES.items():
        rows = read_table(relpath)
        if private and key in OVERLAYS:
            rows, did = merge_overlay(rows, OVERLAYS[key])
            if did:
                applied.append(OVERLAYS[key])
        data[key] = rows
        print("  %-14s %3d rows  (%s)" % (key, len(rows), relpath))

    docs = collect_docs()
    data["docs"] = docs
    print("  %-14s %3d files" % ("docs", len(docs)))

    data["meta"] = {
        "generated": date.today().isoformat(),
        "repo": "benbaichmankass/sustainable-finance-venture",
        "private": bool(applied),
        "overlays": applied,
        "counts": {
            "literatureByAxis": counts(data["literature"], "Axis"),
            "literatureByStatus": counts(data["literature"], "Status"),
            "questionsByStatus": counts(data["openQuestions"], "Status"),
            "milestonesByStatus": counts(data["milestones"], "Status"),
            "partnersByStatus": counts(data["partners"], "Contact_Status"),
            "totalWords": sum(d["words"] for d in docs),
        },
    }

    out = OUT_PRIVATE if applied else OUT
    payload = json.dumps(data, indent=1, ensure_ascii=False)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("// GENERATED FILE - do not edit by hand.\n")
        fh.write("// Regenerate with: python3 dashboard/build.py\n")
        if applied:
            fh.write("// Contains private overlay data. Gitignored - never commit.\n")
        fh.write("window.SFV_DATA = %s;\n" % payload)

    size = os.path.getsize(out)
    print("Wrote %s (%.1f KB)" % (os.path.relpath(out, ROOT), size / 1024.0))
    if applied:
        print("  merged private overlay: %s" % ", ".join(applied))
        print("  NOTE: this file is gitignored. Run with --public to refresh the")
        print("        committed dashboard/data.js before pushing.")
    else:
        print("  public tier only - safe to commit.")


if __name__ == "__main__":
    main()
