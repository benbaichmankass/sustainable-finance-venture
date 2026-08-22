#!/usr/bin/env python3
"""Tests for the Drive <-> repo text handling in sync_drive.py.

These exist because of one incident. On 2026-08-21 a transient Drive API error
made export_doc_text() fall back to text/plain; the engine pulled a
formatting-stripped rendering over docs/phd/phd-scoring-rubric.md, wrote it with
CRLF and a BOM, and baselined to it. From then on the repo-side hash could never
match its own baseline - write kept the CRLFs, read stripped them - so the row
sat in Conflict permanently and no hand-edit of either side could clear it.

Both halves of that are covered here: the round-trip must be hash-stable, and
the plain-text fallback must not exist.

    python3 scripts/test_sync_drive.py

Python 3 stdlib only, no install step, matching risk-tools/tools/.
"""

import os
import sys
import tempfile
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _import_sync_drive():
    """Import sync_drive without needing the Google client libraries.

    Everything under test here - normalise, sha, read_repo_file,
    write_repo_file - is pure stdlib, but sync_drive imports the Google client
    at module scope. In CI those are installed and the real import is used. On a
    machine without them (or with a broken cryptography backend) we stub just
    the four names it imports, so the tests still run rather than being quietly
    skipped. A test that only runs somewhere else is not a test.
    """
    try:
        import sync_drive  # noqa: F401
        return sync_drive
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException:  # noqa: BLE001
        # Deliberately BaseException, not Exception: a broken native extension
        # (here, cryptography's Rust binding without _cffi_backend) raises
        # pyo3_runtime.PanicException, which does NOT subclass Exception. An
        # `except Exception` guard here looks right and silently fails to catch.
        sys.modules.pop("sync_drive", None)

    class _HttpError(Exception):
        pass

    stubs = {
        "google": types.ModuleType("google"),
        "google.oauth2": types.ModuleType("google.oauth2"),
        "googleapiclient": types.ModuleType("googleapiclient"),
        "googleapiclient.discovery": types.ModuleType("googleapiclient.discovery"),
        "googleapiclient.errors": types.ModuleType("googleapiclient.errors"),
        "googleapiclient.http": types.ModuleType("googleapiclient.http"),
    }
    stubs["google.oauth2"].service_account = object()
    stubs["googleapiclient.discovery"].build = lambda *a, **k: None
    stubs["googleapiclient.errors"].HttpError = _HttpError
    stubs["googleapiclient.http"].MediaIoBaseUpload = object
    saved = {k: sys.modules.get(k) for k in stubs}
    sys.modules.update(stubs)
    try:
        import sync_drive  # noqa: F811
        return sync_drive
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v


sync_drive = _import_sync_drive()


PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("  %s  %s%s" % ("PASS" if cond else "FAIL", name, ("  - " + detail) if detail else ""))


def main():
    print("sync_drive text handling\n")

    # --- normalise ---------------------------------------------------------
    bom_crlf = "﻿# Title\r\n\r\nA line\r\nAnother\r\n"
    clean = sync_drive.normalise(bom_crlf)
    check("normalise strips the BOM", not clean.startswith("﻿"))
    check("normalise folds CRLF to LF", "\r" not in clean)
    check("normalise is idempotent", sync_drive.normalise(clean) == clean)
    check("normalise keeps content", clean == "# Title\n\nA line\nAnother\n")
    check("normalise folds a lone CR", sync_drive.normalise("a\rb") == "a\nb")
    check("normalise passes None through", sync_drive.normalise(None) is None)
    check("normalise leaves clean text alone", sync_drive.normalise(clean) == clean)

    # --- sha is computed on the canonical form ------------------------------
    check("sha ignores CRLF vs LF", sync_drive.sha(bom_crlf) == sync_drive.sha(clean))
    check("sha ignores a BOM", sync_drive.sha("﻿x") == sync_drive.sha("x"))
    check("sha still distinguishes real differences",
          sync_drive.sha("a\nb") != sync_drive.sha("a\nc"))

    # --- THE REGRESSION: write -> read must be hash-stable ------------------
    # This is the exact loop that wedged DRV-11. Before the fix, writing a
    # CRLF-bearing export and reading it back produced two different hashes,
    # so repo_changed was True on every run for ever.
    tmp = tempfile.mkdtemp()
    real_root = sync_drive.ROOT
    try:
        sync_drive.ROOT = tmp
        rel = "docs/round-trip.md"
        sync_drive.write_repo_file(rel, bom_crlf)
        back = sync_drive.read_repo_file(rel)
        check("round-trip is hash-stable (the DRV-11 defect)",
              sync_drive.sha(bom_crlf) == sync_drive.sha(back),
              "write(export) then read() must hash the same")
        raw = open(os.path.join(tmp, rel), "rb").read()
        check("nothing CRLF reaches disk", b"\r\n" not in raw)
        check("no BOM reaches disk", raw[:3] != b"\xef\xbb\xbf")
        check("read_repo_file returns None for a missing file",
              sync_drive.read_repo_file("docs/nope.md") is None)
    finally:
        sync_drive.ROOT = real_root

    # --- the fallback must be gone -----------------------------------------
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_drive.py")
    src = open(src_path, encoding="utf-8").read()
    body = src[src.index("def export_doc_text("):src.index("def create_doc(")]
    check("export_doc_text never exports the fallback mime",
          "export(fileId=file_id, mimeType=DOC_EXPORT_FALLBACK_MIME)" not in body
          and ".export(" in body,
          "a text/plain pull silently destroys headings, bold and tables")
    check("export_doc_text raises instead", "raise MarkdownExportUnavailable" in body)
    check("main() flags the row Error rather than dying",
          "except MarkdownExportUnavailable" in src and 'row["Status"] = "Error"' in src)

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
