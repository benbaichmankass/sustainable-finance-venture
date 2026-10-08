#!/usr/bin/env python3
"""Shared plumbing for the ingestion scripts. Python 3 stdlib.

The rules these enforce are in docs/ops/data-provenance.md:

- raw extracts land in data/raw/<DS-NN>/ (gitignored), named with the
  retrieval date, never edited, and a query log sits beside each one with
  the exact request, the UTC timestamp and the SHA-256 of the bytes;
- processed, model-ready files land in data/processed/ (committed), small,
  every field quoted, with a data dictionary beside them;
- every processed file records the script and git commit that made it.

The raw files are then copied to the Vault's 05-raw-data/<DS-NN>/ folder by
hand or by an agent with Drive access; the query log records when that was done.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "data", "raw")
PROCESSED = os.path.join(ROOT, "data", "processed")
USER_AGENT = "sustainable-finance-venture ingestion (https://github.com/benbaichmankass/sustainable-finance-venture)"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today():
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return ""


def fetch(url, timeout=300):
    """GET a URL and return the bytes. One place to set the user agent and timeout."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def raw_dir(ds_id):
    d = os.path.join(RAW, ds_id)
    os.makedirs(d, exist_ok=True)
    return d


def save_raw(ds_id, filename, data, request, notes=""):
    """Write a raw extract and its query log side by side. Never overwrites:
    the filename carries the retrieval date, and a second run on the same day
    refuses rather than silently replacing bytes."""
    d = raw_dir(ds_id)
    path = os.path.join(d, filename)
    if os.path.exists(path):
        raise FileExistsError("%s exists; raw files are never overwritten (rename with a new date)" % path)
    with open(path, "wb") as fh:
        fh.write(data)
    log = {
        "dataset_id": ds_id,
        "raw_file": os.path.relpath(path, ROOT),
        "retrieved_at_utc": now_iso(),
        "request": request,
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "code_version": git_commit(),
        "vault_copy": "",
        "notes": notes,
    }
    with open(path + ".query.json", "w", encoding="utf-8") as fh:
        json.dump(log, fh, indent=1)
    return path, log


def latest_raw(ds_id, suffix):
    """Most recent raw file for a dataset with the given suffix, or None."""
    d = raw_dir(ds_id)
    cands = sorted(f for f in os.listdir(d) if f.endswith(suffix) and not f.endswith(".query.json"))
    return os.path.join(d, cands[-1]) if cands else None


def write_processed(name, header, rows, dictionary_md):
    """Write data/processed/<name>.csv (every field quoted, LF) and its
    data dictionary data/processed/<name>.md. Returns the CSV path."""
    os.makedirs(PROCESSED, exist_ok=True)
    path = os.path.join(PROCESSED, name + ".csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_ALL, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else str(v) for v in r])
    with open(os.path.join(PROCESSED, name + ".md"), "w", encoding="utf-8") as fh:
        fh.write(dictionary_md.rstrip() + "\n")
    print("wrote %s (%d rows) and its dictionary" % (os.path.relpath(path, ROOT), len(rows)))
    return path


def read_processed(name):
    path = os.path.join(PROCESSED, name + ".csv")
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def provenance_block(ds_id, raw_log, script, extra=None):
    """The standard footer every data dictionary carries."""
    lines = [
        "## Provenance",
        "",
        "| | |",
        "|---|---|",
        "| Catalogue row | `%s` in `data/data-catalog.csv` |" % ds_id,
        "| Raw extract | `%s` (gitignored; Vault copy under `05-raw-data/%s/`) |" % (raw_log["raw_file"], ds_id),
        "| Raw SHA-256 | `%s` |" % raw_log["sha256"],
        "| Retrieved | %s |" % raw_log["retrieved_at_utc"],
        "| Ingestion script | `%s` at commit `%s` |" % (script, git_commit() or "uncommitted"),
        "| Processed | %s |" % now_iso(),
    ]
    for k, v in (extra or {}).items():
        lines.append("| %s | %s |" % (k, v))
    return "\n".join(lines)


def fail(msg):
    print("  ! " + msg, file=sys.stderr)
    sys.exit(1)
