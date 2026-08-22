#!/usr/bin/env python3
"""Reconcile data/drive-links.csv against Google Drive.

No model in the loop: this is a deterministic hash comparison against the
last-synced baseline recorded in the manifest, run unattended by
.github/workflows/sync-drive.yml. Full design in docs/ops/drive-sync.md.

For every non-folder row in the manifest:

  - Drive_ID blank            -> create the Drive file from the repo content,
                                  read the post-conversion text back, and
                                  baseline both sides to that.
  - only Drive changed        -> pull: overwrite the repo file.
  - only the repo changed     -> push: overwrite the Drive file.
  - both changed, now equal   -> both sides independently converged; just
                                  re-baseline (not a conflict).
  - both changed, now differ  -> conflict: open a GitHub issue, touch nothing.
  - neither changed           -> skip.

Auth: a service-account JSON key in the GDRIVE_SA_KEY env var. The service
account needs Editor access on the target Drive folder (granted by sharing
the folder with its email) - see docs/ops/drive-sync.md for one-time setup.
"""
import csv
import hashlib
import io
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "data", "drive-links.csv")
FIELDNAMES = [
    "ID", "Drive_ID", "Repo_Path", "Type", "Parent_ID", "Title", "Category",
    "Baseline_Drive_Hash", "Baseline_Repo_Hash", "Last_Synced_At", "Status",
]

SCOPES = ["https://www.googleapis.com/auth/drive"]
DOC_MIME = "application/vnd.google-apps.document"
SHEET_MIME = "application/vnd.google-apps.spreadsheet"
DOC_EXPORT_MIME = "text/markdown"
DOC_EXPORT_FALLBACK_MIME = "text/plain"


def log(msg):
    print(msg, flush=True)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalise(text):
    """Canonical form for any text crossing the Drive <-> repo boundary.

    Strips a UTF-8 BOM and folds CRLF/CR to LF. Both matter, and the second one
    is not cosmetic: write_repo_file() opens with newline="\n", which does NOT
    strip a \r already inside the string, while read_repo_file() opens with
    universal newlines, which does. So a CRLF-bearing export written to disk and
    read back is a DIFFERENT string, its hash never matches the baseline that was
    recorded at write time, and repo_changed is True on every run forever.

    That is what wedged DRV-11 (docs/phd/phd-scoring-rubric.md) in Conflict from
    2026-08-21: the recorded baseline hashes the bytes as written, the engine
    hashes them as read, and no amount of hand-editing either side can reconcile
    the two. Normalising both ends of the round-trip is the fix.
    """
    if text is None:
        return None
    if text.startswith("\ufeff"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sha(text):
    return hashlib.sha256(normalise(text).encode("utf-8")).hexdigest()


# --- manifest I/O -------------------------------------------------------

def read_manifest():
    with open(MANIFEST, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_manifest(rows):
    with open(MANIFEST, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDNAMES, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in FIELDNAMES})


def by_id(rows):
    return {r["ID"]: r for r in rows}


# --- Google auth ---------------------------------------------------------

def load_creds():
    key = os.environ.get("GDRIVE_SA_KEY")
    if not key:
        sys.exit("GDRIVE_SA_KEY is not set - nothing to authenticate with.")
    info = json.loads(key)
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


# --- Drive: docs -----------------------------------------------------------

class MarkdownExportUnavailable(Exception):
    """Drive would not give us markdown for a Doc we sync as markdown."""


def export_doc_text(drive, file_id):
    """Export a Doc as markdown. Never silently substitute plain text.

    There used to be a fallback here: on any HttpError it re-exported as
    text/plain and returned that. It looks harmless and is not. Google's
    text/plain export drops every heading marker, every bold marker and every
    table pipe, and adds a BOM and CRLF endings - so a transient API error on
    one run would overwrite a perfectly good markdown file in the repo with a
    formatting-stripped rendering, commit it to main, and report success.

    That is exactly what happened to docs/phd/phd-scoring-rubric.md on
    2026-08-21: 8 headings, 4 tables and all bold gone, replaced by 212 tabs.
    A pull that destroys formatting is a data-loss event, not a sync, so it now
    raises and the caller marks the row Error and moves on. Losing a cycle on
    one document is strictly better than losing the document.
    """
    try:
        data = drive.files().export(fileId=file_id, mimeType=DOC_EXPORT_MIME).execute()
    except HttpError as exc:
        raise MarkdownExportUnavailable(
            "markdown export unavailable for %s (%s); refusing to fall back to "
            "%s, which would strip all formatting" % (file_id, exc, DOC_EXPORT_FALLBACK_MIME)
        )
    text = data.decode("utf-8") if isinstance(data, (bytes, bytearray)) else data
    return normalise(text)


def create_doc(drive, parent_id, title, content):
    meta = {"name": title, "mimeType": DOC_MIME, "parents": [parent_id]}
    media = MediaIoBaseUpload(io.BytesIO(content.encode("utf-8")), mimetype=DOC_EXPORT_MIME)
    return drive.files().create(body=meta, media_body=media, fields="id").execute()


def update_doc(drive, file_id, content):
    media = MediaIoBaseUpload(io.BytesIO(content.encode("utf-8")), mimetype=DOC_EXPORT_MIME)
    drive.files().update(fileId=file_id, media_body=media).execute()


# --- Drive: sheets -----------------------------------------------------

def export_sheet_text(sheets, spreadsheet_id, tab="Sheet1"):
    result = sheets.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=tab).execute()
    values = result.get("values", [])
    buf = io.StringIO()
    w = csv.writer(buf, quoting=csv.QUOTE_ALL, lineterminator="\n")
    for r in values:
        w.writerow(r)
    return buf.getvalue()


def update_sheet(sheets, spreadsheet_id, csv_text, tab="Sheet1"):
    rows = list(csv.reader(io.StringIO(csv_text)))
    sheets.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=tab, body={}).execute()
    if rows:
        sheets.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=tab, valueInputOption="RAW",
            body={"values": rows}).execute()


def create_sheet(drive, sheets, parent_id, title, csv_text):
    meta = {"name": title, "mimeType": SHEET_MIME, "parents": [parent_id]}
    created = drive.files().create(body=meta, fields="id").execute()
    update_sheet(sheets, created["id"], csv_text)
    return created


# --- repo file I/O -------------------------------------------------------

def read_repo_file(rel_path):
    full = os.path.join(ROOT, rel_path)
    if not os.path.exists(full):
        return None
    with open(full, encoding="utf-8") as fh:
        return normalise(fh.read())


def write_repo_file(rel_path, content):
    full = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(normalise(content))


# --- conflict reporting (plain GitHub REST call, no extra dependency) ------

def github_api(method, path, token, body=None):
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo or not token:
        return None
    req = urllib.request.Request(
        "https://api.github.com/repos/%s%s" % (repo, path),
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": "Bearer %s" % token,
            "Accept": "application/vnd.github+json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        log("  ! GitHub API %s %s failed: %s" % (method, path, e))
        return None


def flag_conflict(row):
    token = os.environ.get("GITHUB_TOKEN")
    if not token or not os.environ.get("GITHUB_REPOSITORY"):
        log("  ! conflict on %s but no GITHUB_TOKEN/GITHUB_REPOSITORY - not opening an issue"
            % row["ID"])
        return
    existing = github_api(
        "GET", "/issues?labels=drive-sync-conflict&state=open&per_page=50", token) or []
    marker = "[%s]" % row["ID"]
    if any(marker in (issue.get("title") or "") for issue in existing):
        log("  conflict issue already open for %s" % row["ID"])
        return
    title = "Drive sync conflict %s: %s" % (marker, row["Repo_Path"])
    body = (
        "`%s` (`%s`) changed on both sides since the last sync (%s). "
        "Not auto-resolving - a bad guess here could silently discard an edit.\n\n"
        "**To resolve:** edit one side to match the other (or merge by hand so both "
        "agree), then the next scheduled run picks it up cleanly and closes out on "
        "its own. This issue does not auto-close - close it once you've confirmed "
        "the next run synced successfully.\n\n"
        "- Drive: https://docs.google.com/document/d/%s/edit\n"
        "- Repo: `%s`\n"
    ) % (row["ID"], row["Repo_Path"], row["Last_Synced_At"] or "never", row["Drive_ID"], row["Repo_Path"])
    github_api("POST", "/issues", token,
               {"title": title, "body": body, "labels": ["drive-sync-conflict"]})
    log("  opened conflict issue for %s" % row["ID"])


# --- reconciliation --------------------------------------------------------

def reconcile_row(row, id_index, drive, sheets):
    repo_text = read_repo_file(row["Repo_Path"])
    repo_hash = sha(repo_text) if repo_text is not None else ""
    is_sheet = row["Type"] == "sheet"

    if not row["Drive_ID"]:
        if repo_text is None:
            log("  ! %s has no Drive_ID and no repo file at %s - skipping"
                % (row["ID"], row["Repo_Path"]))
            row["Status"] = "Error"
            return
        parent = id_index.get(row["Parent_ID"], {})
        parent_drive_id = parent.get("Drive_ID")
        if not parent_drive_id:
            log("  ! %s: parent %s has no Drive_ID yet - skipping" % (row["ID"], row["Parent_ID"]))
            return
        title = row["Title"] or os.path.basename(row["Repo_Path"])
        log("  creating %s (%s) in Drive..." % (row["ID"], row["Repo_Path"]))
        try:
            created = (create_sheet(drive, sheets, parent_drive_id, title, repo_text)
                       if is_sheet else create_doc(drive, parent_drive_id, title, repo_text))
        except HttpError as e:
            if "storageQuotaExceeded" in str(e):
                log("  ! %s: the service account has no Drive storage quota of its own "
                    "(expected for a standalone service account, not backed by a Workspace "
                    "Shared Drive) - it cannot create new files, only edit ones a real "
                    "account already owns. See docs/ops/drive-sync.md's 'known constraint' "
                    "section for how new docs actually get seeded." % row["ID"])
            raise
        row["Drive_ID"] = created["id"]
        drive_text = (export_sheet_text(sheets, created["id"])
                      if is_sheet else export_doc_text(drive, created["id"]))
        row["Baseline_Drive_Hash"] = sha(drive_text)
        row["Baseline_Repo_Hash"] = repo_hash
        row["Last_Synced_At"] = now_iso()
        row["Status"] = "Synced"
        log("    -> %s" % created["id"])
        return

    if repo_text is None:
        log("  ! %s: repo file %s is missing - skipping" % (row["ID"], row["Repo_Path"]))
        row["Status"] = "Error"
        return

    drive_text = (export_sheet_text(sheets, row["Drive_ID"])
                  if is_sheet else export_doc_text(drive, row["Drive_ID"]))
    drive_hash = sha(drive_text)

    drive_changed = drive_hash != row["Baseline_Drive_Hash"]
    repo_changed = repo_hash != row["Baseline_Repo_Hash"]

    if not drive_changed and not repo_changed:
        return

    if drive_changed and repo_changed:
        if drive_hash == repo_hash:
            # Both sides moved independently but landed in the same place -
            # not a real conflict, just re-baseline.
            row["Baseline_Drive_Hash"] = drive_hash
            row["Baseline_Repo_Hash"] = repo_hash
            row["Last_Synced_At"] = now_iso()
            row["Status"] = "Synced"
            log("  %s: both sides changed but now agree - re-baselined" % row["ID"])
        else:
            row["Status"] = "Conflict"
            flag_conflict(row)
        return

    if drive_changed:
        log("  %s: Drive changed - pulling into %s" % (row["ID"], row["Repo_Path"]))
        write_repo_file(row["Repo_Path"], drive_text)
        row["Baseline_Repo_Hash"] = sha(drive_text)
        row["Baseline_Drive_Hash"] = drive_hash
    else:
        log("  %s: repo changed - pushing to Drive" % row["ID"])
        if is_sheet:
            update_sheet(sheets, row["Drive_ID"], repo_text)
            confirm_text = export_sheet_text(sheets, row["Drive_ID"])
        else:
            update_doc(drive, row["Drive_ID"], repo_text)
            confirm_text = export_doc_text(drive, row["Drive_ID"])
        row["Baseline_Drive_Hash"] = sha(confirm_text)
        row["Baseline_Repo_Hash"] = repo_hash

    row["Last_Synced_At"] = now_iso()
    row["Status"] = "Synced"


def main():
    rows = read_manifest()
    id_index = by_id(rows)
    creds = load_creds()
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)

    errors = 0
    for row in rows:
        if row["Type"] == "folder":
            continue
        try:
            reconcile_row(row, id_index, drive, sheets)
        except MarkdownExportUnavailable as e:
            # Deliberately not fatal and deliberately not silent: the row is left
            # untouched on both sides and flagged for a human, rather than pulled
            # in a degraded form. See export_doc_text().
            log("  ! %s: %s" % (row["ID"], e))
            row["Status"] = "Error"
            errors += 1
        except HttpError as e:
            log("  ! %s: Drive API error: %s" % (row["ID"], e))
            row["Status"] = "Error"
            errors += 1
        except Exception as e:  # noqa: BLE001 - one bad row shouldn't kill the run
            log("  ! %s: unexpected error: %s" % (row["ID"], e))
            row["Status"] = "Error"
            errors += 1

    write_manifest(rows)
    log("Done. %d row(s) errored." % errors if errors else "Done, no errors.")


if __name__ == "__main__":
    main()
