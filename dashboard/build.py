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
    "researchQuestions": "data/research-questions.csv",
    "litComponents": "data/lit-components.csv",
    "openQuestions": "data/open-questions.csv",
    "productLines": "data/product-lines.csv",
    "riskTools": "data/risk-tools.csv",
    "macroIndicators": "data/macro-indicators.csv",
    "macroSnapshot": "data/macro-snapshot.csv",
    "macroHistory": "data/macro-history.csv",
    "macroLog": "data/macro-log.csv",
    "macroScenarios": "data/macro-scenarios.csv",
    "rt5Results": "data/rt5-scenario-results.csv",
    "rt6Results": "data/rt6-economics-results.csv",
    "partners": "data/partner-tracker.csv",
    "phdPrograms": "data/phd-programs.csv",
    "milestones": "data/milestones.csv",
    "memos": "data/synthesis-memos.csv",
    "resources": "data/resources.csv",
    "experiments": "data/experiments.csv",
    "funders": "data/funders.csv",
    "driveLinks": "data/drive-links.csv",
}

# --- private overlay ---------------------------------------------------------
# Gitignored files that add the columns a public repo must not carry: named
# individuals, relationship status, Vault links. Merged by ID when present, so
# a local build shows the whole picture and a public build shows only the
# public tier. See docs/ops/publishing.md.
OVERLAYS = {
    "partners": "private/partner-contacts.csv",
    "phdPrograms": "private/phd-applications.csv",
    # Fills in the blank URL on the Vault/tracker rows of data/resources.csv.
    # Keyed by ID like the others, so the public tier keeps the row and its
    # description and only the link is withheld.
    "resources": "private/pointers.csv",
}

# --- document library --------------------------------------------------------
# Where to look for documents: (directory, recursive). This is discovery only -
# what a document is grouped UNDER comes from DOC_TREE below, not from where it
# happens to sit on disk.
DOC_DIRS = [
    (".", False),
    ("docs", True),
    ("literature/notes", True),
    ("product-design", True),
    ("risk-tools", True),
    ("archive/google-drive", True),
    (".claude/skills", True),
]

SKIP_FILES = {"data.js"}

# Generated docs whose whole content is already in this payload as structured rows.
# docs/research/literature-review.md is assembled from the literature matrix and the
# component tracker by scripts/build_lit_review.py, so embedding it here would ship
# every anchor twice - once as a literature row the dashboard renders, once as prose
# nobody reads in the doc viewer. The duplication grows linearly with the matrix.
# Read it in the repo or on GitHub; the dashboard has its own literature view.
SKIP_PATHS = {"docs/research/literature-review.md"}

# The library's two-level tree: (path prefix, group, section). Grouping is by
# what a document is FOR, which is why the PhD track is its own group rather
# than a corner of Research - writing the enquiry and applying to programmes are
# different jobs with different deadlines, and burying one inside the other is
# what made the old flat "Planning" bucket unusable at 17 files.
#
# First match wins, so exact paths come before the directories they sit in.
# Order here is the order the tree renders in - deliberately the order the work
# actually flows, not alphabetical.
DOC_TREE = [
    ("docs/research/",                  "Research",    "Programme & method"),
    ("literature/notes/",               "Research",    "Evidence synthesis"),

    ("docs/phd/phd-proposal-master.md", "PhD track",   "Proposal & positioning"),
    ("docs/phd/research-proposal.md",   "PhD track",   "Proposal & positioning"),
    ("docs/phd/",                       "PhD track",   "Applications & funding"),

    ("product-design/product-lines/",   "Venture",     "Product lines"),
    ("product-design/",                 "Venture",     "Plan & economics"),
    ("docs/venture/",                   "Venture",     "Delivery & funding"),

    ("risk-tools/README.md",            "Risk tools",  "Overview & schema"),
    ("risk-tools/schema/",              "Risk tools",  "Overview & schema"),
    ("risk-tools/",                     "Risk tools",  "Tool specs"),

    ("docs/ops/publishing.md",          "Operations",  "Publishing & privacy"),
    ("docs/ops/private-overlay.md",     "Operations",  "Publishing & privacy"),
    ("docs/ops/drive-sync.md",          "Operations",  "Drive & sync"),
    ("docs/ops/drive-vault.md",         "Operations",  "Drive & sync"),
    ("docs/ops/",                       "Operations",  "Dashboard & capture"),
    ("CLAUDE.md",                       "Operations",  "Repo conventions"),
    ("README.md",                       "Operations",  "Repo conventions"),
    ("LICENSE-CONTENT.md",              "Operations",  "Repo conventions"),

    (".claude/skills/",                 "AI skills",   "Working procedures"),
    ("archive/google-drive/",           "Archive",     "Superseded source docs"),
]

# Which family a document belongs to, where it belongs to one. These are display
# labels for the library, NOT new record IDs - nothing cross-references them, and
# they are not subject to the never-renumber rule in CLAUDE.md section 3.
#
# RT-5 covers two documents and RT-2/3 covers one document spanning two tools;
# the a/b suffixes and the slash say so rather than leaving three files looking
# like collisions. Value is either an ID or (ID, display title override).
DOC_FAMILY = {
    "risk-tools/rt-1-origination-schema.md":            "RT-1",
    "risk-tools/rt-2-underwriting-engine.md":           "RT-2",
    "risk-tools/rt-3-monitoring-early-warning.md":      "RT-3",
    "risk-tools/rt-2-rt-3-scaffolds.md":                ("RT-2/3", "Scaffolds - scorecard and monitor"),
    "risk-tools/rt-4-impact-evaluation.md":             "RT-4",
    "risk-tools/rt-5-securitisation-model.md":          "RT-5a",
    "risk-tools/rt-5-simulator.md":                     ("RT-5b", "Simulator - what it is, what it is not"),
    "risk-tools/rt-6-economics-model.md":               "RT-6",
    "literature/notes/memo-1-vslas.md":                 "MEMO-1",
    "literature/notes/memo-2-microfinance-impact.md":   "MEMO-2",
    "literature/notes/memo-3-securitization-blended-finance.md": "MEMO-3",
    "product-design/product-lines/community-credit-and-insurance.md":  "PL-1",
    "product-design/product-lines/agrivoltaic-project-finance.md":     "PL-2",
}

# Strips a family label off the front of a title so the library does not render
# "RT-1 - RT-1 - Origination data schema". The separator is mandatory: without
# it "RT-2 and RT-3 scaffolds" would lose its "RT-2" and start with "and".
FAMILY_PREFIX = re.compile(
    r"^(?:RT-\d+[a-z]?|MEMO-\d+|Memo \d+|PL-\d+|Product Line \d+)\s*[-—:]\s*",
    re.IGNORECASE,
)


def classify(rel):
    """(group, section) for a repo-relative path. Unmatched files land in
    Unfiled rather than vanishing - a visible prompt to place them."""
    for prefix, group, section in DOC_TREE:
        if rel == prefix or rel.startswith(prefix):
            return group, section
    return "Unfiled", "Needs a home"


def family_of(rel, title):
    """(doc_id, display_title). Both fall back cleanly when there is no family."""
    entry = DOC_FAMILY.get(rel)
    if entry is None:
        return "", title
    if isinstance(entry, tuple):
        return entry[0], entry[1]
    return entry, FAMILY_PREFIX.sub("", title).strip() or title


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
    for reldir, recursive in DOC_DIRS:
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
                rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                if rel in seen or rel in SKIP_PATHS:
                    continue
                seen.add(rel)
                with open(full, encoding="utf-8") as fh:
                    text = fh.read()
                meta, body = split_frontmatter(text)
                fallback = meta.get("name") or prettify(filename[:-3])
                group, section = classify(rel)
                doc_id, title = family_of(rel, title_of(body, fallback))
                docs.append(
                    {
                        "path": rel,
                        "group": group,
                        "section": section,
                        "docId": doc_id,
                        "title": title,
                        "summary": meta.get("description", ""),
                        "words": len(body.split()),
                        "body": body,
                    }
                )
    # Sort within a section by family ID where there is one (so RT-1..RT-6 read
    # as a sequence), then by title. The group/section order itself comes from
    # DOC_TREE, applied in the dashboard.
    docs.sort(key=lambda d: (d["group"], d["section"], d["docId"] or "zz", d["title"]))
    return docs


def tree_order():
    """Group -> [section, ...] in DOC_TREE order, deduped. The dashboard renders
    the tree from this rather than re-deriving an order from the docs."""
    order = []
    for _, group, section in DOC_TREE:
        entry = next((e for e in order if e["group"] == group), None)
        if entry is None:
            entry = {"group": group, "sections": []}
            order.append(entry)
        if section not in entry["sections"]:
            entry["sections"].append(section)
    return order


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

    # Reshape the macro history from one row per observation into
    # {ID: [[date, value], ...]}. As flat dicts it is ~1200 records that repeat
    # the column names on every one; as arrays it is a third of the size and is
    # what the charting code wants anyway.
    series = {}
    for row in data.pop("macroHistory", []):
        try:
            value = float(row["Value"])
        except (KeyError, TypeError, ValueError):
            continue
        series.setdefault(row["ID"], []).append([row["Date"], value])
    data["macroSeries"] = series
    print("  %-14s %3d series, %d points"
          % ("macroSeries", len(series), sum(len(v) for v in series.values())))

    docs = collect_docs()
    data["docs"] = docs
    data["docTree"] = tree_order()
    print("  %-14s %3d files" % ("docs", len(docs)))
    for entry in data["docTree"]:
        total = sum(1 for d in docs if d["group"] == entry["group"])
        print("      %-13s %3d  (%s)" % (entry["group"], total, ", ".join(entry["sections"])))
    unfiled = [d["path"] for d in docs if d["group"] == "Unfiled"]
    if unfiled:
        print("  ! %d unfiled doc(s) - add them to DOC_TREE:" % len(unfiled), file=sys.stderr)
        for path in unfiled:
            print("      %s" % path, file=sys.stderr)

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
