#!/usr/bin/env python3
"""Assemble docs/research/literature-review.md from the trackers.

The literature review lives in four places by design: lit-matrix.csv holds the
anchors, lit-components.csv holds the coverage plan, synthesis-memos.csv indexes
the memos, and the memo files hold the prose. Each is the right shape for its
job and none of them is readable end to end.

This script produces the readable end-to-end view WITHOUT creating a second
source of truth: every fact in the output is copied from a tracker, and the file
is regenerated rather than edited. Same discipline as dashboard/data.js.

Gaps are rendered as gaps. A component with no anchors says so; a memo that does
not exist says so. That is the point - the document should be honest about how
much of the review is done, not paper over it.

    python3 scripts/build_lit_review.py

Run it after any change to literature/lit-matrix.csv, data/lit-components.csv or
data/synthesis-memos.csv, and commit the output alongside the source change.
"""

import csv
import io
import os
import sys
from urllib.parse import quote_plus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "research", "literature-review.md")

MATRIX = "literature/lit-matrix.csv"
COMPONENTS = "data/lit-components.csv"
MEMOS = "data/synthesis-memos.csv"

# Rendered in this order; anything else falls to the end alphabetically.
AXIS_ORDER = [
    "1-VSLA",
    "2-Microfinance",
    "3-Securitization",
    "4-Blended finance",
    "5-Insurance",
]

PRIORITY_ORDER = ["P1", "P2", "P3"]


def read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def refs(value):
    """Split a semicolon-separated ref cell into a clean list."""
    return [x.strip() for x in (value or "").split(";") if x.strip()]


def lit_sort_key(row):
    """Sort LIT-007 before LIT-030 - numerically, not as strings."""
    try:
        return int(row["ID"].split("-")[1])
    except (IndexError, ValueError):
        return 10**6


def main():
    matrix = sorted(read(MATRIX), key=lit_sort_key)
    components = read(COMPONENTS)
    memos = read(MEMOS)

    by_id = {r["ID"]: r for r in matrix}
    memo_by_id = {r["ID"]: r for r in memos}

    # --- which anchors does each component claim, and are they real? --------
    claimed = {}
    dangling = []
    for c in components:
        ids = refs(c["Current_Anchors"])
        claimed[c["ID"]] = ids
        for i in ids:
            if i not in by_id:
                dangling.append((c["ID"], i))

    # An anchor can serve more than one component; count distinct.
    anchored = set()
    for ids in claimed.values():
        anchored.update(i for i in ids if i in by_id)
    orphans = [r for r in matrix if r["ID"] not in anchored]

    out = []
    w = out.append

    # ---------------------------------------------------------------- header
    w("# Literature review")
    w("")
    w("> **This file is generated.** Do not edit it. It is assembled from")
    w("> `literature/lit-matrix.csv`, `data/lit-components.csv` and")
    w("> `data/synthesis-memos.csv` by `scripts/build_lit_review.py`.")
    w("> Change a tracker and regenerate; editing here would create a second")
    w("> source of truth, which is the thing this repo exists to avoid.")
    w("")
    w("It exists because the review is correctly stored in four places and")
    w("readable in none of them. Gaps are shown as gaps: a component with no")
    w("anchors says so, and a memo that has not been written says so. How much")
    w("of the review is *not* done is the most useful thing this document says.")
    w("")

    # ------------------------------------------------------------- the state
    total_target = sum(int(c["Target_Anchors"] or 0) for c in components)
    total_filled = sum(len(v) for v in claimed.values())
    statuses = {}
    for c in components:
        statuses[c["Status"]] = statuses.get(c["Status"], 0) + 1

    w("## Where the review stands")
    w("")
    w("| | |")
    w("|---|---|")
    w("| Anchors logged | **%d** (%d reviewed, %d to read) |"
      % (len(matrix),
         sum(1 for r in matrix if r["Status"] == "Reviewed"),
         sum(1 for r in matrix if r["Status"] == "To read")))
    w("| Components | %d, covering %d target anchor slots, %d filled |"
      % (len(components), total_target, total_filled))
    w("| Component status | %s |"
      % " · ".join("%s %d" % (k, v) for k, v in sorted(statuses.items())))
    w("| Synthesis memos | %s |"
      % " · ".join("%s %d" % (k, sum(1 for m in memos if m["Status"] == k))
                   for k in ("Reviewed", "Drafted", "Outline")))
    w("")

    if dangling:
        w("> ⚠️ **%d component(s) reference an anchor that is not in the matrix:** %s"
          % (len(dangling),
             ", ".join("%s → %s" % (c, i) for c, i in dangling)))
        w("")

    missing_memo_files = [
        m for m in memos
        if m.get("Path") and not os.path.exists(os.path.join(ROOT, m["Path"]))
    ]
    if missing_memo_files:
        w("> ⚠️ **%d memo(s) have a `Path` pointing at a file that does not exist:** %s"
          % (len(missing_memo_files),
             ", ".join("%s (%s)" % (m["ID"], m["Path"]) for m in missing_memo_files)))
        w("")

    # -------------------------------------------------------- reading agenda
    w("## What is still unread")
    w("")
    w("Ordered by priority, then by how empty the component is. This is the")
    w("reading list; everything below it is what has been read so far.")
    w("")
    w("| Component | Priority | Status | Filled | Target | Memo |")
    w("|---|---|---|---|---|---|")

    def gap_key(c):
        pri = PRIORITY_ORDER.index(c["Priority"]) if c["Priority"] in PRIORITY_ORDER else 9
        target = int(c["Target_Anchors"] or 0)
        return (pri, -(target - len(claimed[c["ID"]])))

    for c in sorted(components, key=gap_key):
        filled = len(claimed[c["ID"]])
        target = int(c["Target_Anchors"] or 0)
        if filled >= target:
            continue
        w("| **%s** %s | %s | %s | %d | %d | %s |"
          % (c["ID"], c["Component"], c["Priority"], c["Status"],
             filled, target, c["Output_Memo"]))
    w("")

    # ---------------------------------------------------------------- memos
    w("## Synthesis memos")
    w("")
    w("The memos are where anchors become an argument. A component with anchors")
    w("but no memo prose is evidence that has not been synthesised yet.")
    w("")
    for m in sorted(memos, key=lambda r: r["ID"]):
        path = m.get("Path", "")
        exists = path and os.path.exists(os.path.join(ROOT, path))
        feeds = [c for c in components if c["Output_Memo"].startswith(m["ID"])]
        feed_ids = ", ".join(c["ID"] for c in feeds) or "—"
        n = sum(len(claimed[c["ID"]]) for c in feeds)
        link = "[`%s`](../../%s)" % (path, path) if exists else "*(file not written)*"
        w("### %s — %s" % (m["ID"], m["Title"]))
        w("")
        w("**Status:** %s · **Fed by:** %s (%d anchor slot%s) · %s"
          % (m["Status"], feed_ids, n, "" if n == 1 else "s", link))
        w("")
        if m.get("Key_Takeaways"):
            w(m["Key_Takeaways"])
            w("")

    # ------------------------------------------------- components by axis
    w("## The evidence, by axis")
    w("")

    axes = sorted(
        {c["Axis"] for c in components},
        key=lambda a: (AXIS_ORDER.index(a) if a in AXIS_ORDER else 99, a),
    )

    for axis in axes:
        w("---")
        w("")
        w("## Axis %s" % axis)
        w("")
        axis_components = [c for c in components if c["Axis"] == axis]
        axis_components.sort(
            key=lambda c: (PRIORITY_ORDER.index(c["Priority"])
                           if c["Priority"] in PRIORITY_ORDER else 9, c["ID"]))

        for c in axis_components:
            ids = claimed[c["ID"]]
            target = int(c["Target_Anchors"] or 0)
            w("### %s — %s" % (c["ID"], c["Component"]))
            w("")
            w("**%s** · **%s** · %d of %d anchors · feeds %s"
              % (c["Priority"], c["Status"], len(ids), target, c["Output_Memo"]))
            w("")
            if c.get("Why_It_Matters"):
                w("**Why it matters.** " + c["Why_It_Matters"])
                w("")
            if c.get("Questions_To_Answer"):
                w("**Questions.** " + c["Questions_To_Answer"])
                w("")
            if not ids:
                w("> **No anchors yet.** Search terms on file: %s"
                  % (c.get("Search_Terms") or "none recorded"))
                w("")
                continue

            for i in ids:
                r = by_id.get(i)
                if r is None:
                    w("> ⚠️ `%s` is referenced here but is not in the matrix." % i)
                    w("")
                    continue
                # The citation itself is the link to the article where we have a
                # verified URL. Renders as a link on GitHub and in the dashboard,
                # and the bare LIT-0NN token stays in the text so the dashboard
                # also turns it into a citation chip.
                if r.get("URL"):
                    w("#### %s — [%s](%s)" % (r["ID"], r["Link_Citation"], r["URL"]))
                else:
                    w("#### %s — %s" % (r["ID"], r["Link_Citation"]))
                w("")
                meta = ["**%s**" % r["Status"], r["Method"], r["Geography"]]
                w(" · ".join(x for x in meta if x))
                w("")
                if r.get("Population_Context"):
                    w("*%s*" % r["Population_Context"])
                    w("")
                if r.get("Key_Findings"):
                    w("**Findings.** " + r["Key_Findings"])
                    w("")
                if r.get("Limitations"):
                    w("**Limitations.** " + r["Limitations"])
                    w("")
                if r.get("Open_Questions"):
                    w("**What it opens.** " + r["Open_Questions"])
                    w("")
                tail = []
                if r.get("URL"):
                    tail.append("[open source](%s)" % r["URL"])
                else:
                    # CLAUDE.md: a URL is verified or absent, never guessed. Give
                    # the reader a search instead of a dead link.
                    tail.append(
                        "*no verified URL on file* — "
                        "[search Scholar](https://scholar.google.com/scholar?q=%s)"
                        % quote_plus(r["Link_Citation"]))
                tail.append("relevance — product %s, risk %s, impact %s"
                            % (r.get("Relevance_Product", "?"),
                               r.get("Relevance_Risk", "?"),
                               r.get("Relevance_Impact", "?")))
                w(" · ".join(tail))
                w("")

    # -------------------------------------------------------------- orphans
    if orphans:
        w("---")
        w("")
        w("## Anchors not claimed by any component")
        w("")
        w("These are in the matrix but no component lists them, so they appear")
        w("nowhere above. Either a component should claim them or they are")
        w("evidence nobody is using.")
        w("")
        for r in orphans:
            w("- **%s** — %s (%s)" % (r["ID"], r["Link_Citation"], r["Status"]))
        w("")

    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")

    print("Wrote %s" % os.path.relpath(OUT, ROOT))
    print("  %d anchors, %d components, %d memos" % (len(matrix), len(components), len(memos)))
    print("  %d anchor slots filled of %d target" % (total_filled, total_target))
    if orphans:
        print("  %d anchor(s) claimed by no component: %s"
              % (len(orphans), ", ".join(r["ID"] for r in orphans)))
    if dangling:
        print("  %d dangling anchor reference(s)" % len(dangling))
        return 1
    if missing_memo_files:
        print("  %d memo path(s) point at a missing file: %s"
              % (len(missing_memo_files), ", ".join(m["ID"] for m in missing_memo_files)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
