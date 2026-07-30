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

# --- structured trackers -----------------------------------------------------
# key -> path relative to repo root
TABLES = {
    "literature": "literature/lit-matrix.csv",
    "openQuestions": "data/open-questions.csv",
    "partners": "data/partner-tracker.csv",
    "phdPrograms": "data/phd-programs.csv",
    "milestones": "data/milestones.csv",
    "memos": "data/synthesis-memos.csv",
    "resources": "data/resources.csv",
}

# --- document library --------------------------------------------------------
# directory -> display category. Files are picked up recursively.
DOC_DIRS = [
    (".", "Project", False),
    ("docs", "Planning", True),
    ("literature/notes", "Synthesis memos", True),
    ("product-design", "Product & business", True),
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


def counts(rows, field):
    out = {}
    for row in rows:
        value = row.get(field) or "Unspecified"
        out[value] = out.get(value, 0) + 1
    return out


def main():
    print("Building dashboard data...")
    data = {}
    for key, relpath in TABLES.items():
        rows = read_table(relpath)
        data[key] = rows
        print("  %-14s %3d rows  (%s)" % (key, len(rows), relpath))

    docs = collect_docs()
    data["docs"] = docs
    print("  %-14s %3d files" % ("docs", len(docs)))

    data["meta"] = {
        "generated": date.today().isoformat(),
        "repo": "benbaichmankass/sustainable-finance-venture",
        "vaultUrl": "https://drive.google.com/drive/folders/1OteXpvFVKBrk-SH1QKGYzpv50JhoHI9r",
        "counts": {
            "literatureByAxis": counts(data["literature"], "Axis"),
            "literatureByStatus": counts(data["literature"], "Status"),
            "questionsByStatus": counts(data["openQuestions"], "Status"),
            "milestonesByStatus": counts(data["milestones"], "Status"),
            "partnersByStatus": counts(data["partners"], "Contact_Status"),
            "totalWords": sum(d["words"] for d in docs),
        },
    }

    payload = json.dumps(data, indent=1, ensure_ascii=False)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("// GENERATED FILE - do not edit by hand.\n")
        fh.write("// Regenerate with: python3 dashboard/build.py\n")
        fh.write("window.SFV_DATA = %s;\n" % payload)

    size = os.path.getsize(OUT)
    print("Wrote %s (%.1f KB)" % (os.path.relpath(OUT, ROOT), size / 1024.0))


if __name__ == "__main__":
    main()
