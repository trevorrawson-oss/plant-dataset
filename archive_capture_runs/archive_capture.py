#!/usr/bin/env python3
"""
archive_capture.py -- Cherry retro v1.2 archive snapshot tool

Reads a cherry-retro URL log markdown file with `<pending>` placeholders
in Archive URL and Captured fields. For each `<pending>` entry, attempts
to capture an archive.org snapshot of the live URL via Save Page Now
(https://web.archive.org/save/<URL>), then writes the resolved snapshot
URL and capture date back to the markdown file.

Idempotent and re-runnable: only `<pending>` entries are touched. Successful
captures replace the placeholder. Failures leave the placeholder and log
the reason. Safe to re-run as many times as needed.

Usage:
  python3 archive_capture.py <path-to-url-log.md>
  python3 archive_capture.py <path-to-url-log.md> --dry-run      # don't write back
  python3 archive_capture.py <path-to-url-log.md> --retries 3    # retry transient failures

Rate-limiting:
  archive.org Save Page Now is rate-limited. Default delay is 6 seconds
  between requests. Adjust with --delay if you hit rate limits.

Anonymous use (no API key) works but has lower priority than authenticated
requests. For large batches consider creating an archive.org account and
passing --access-key and --secret-key.

Output:
  - Updates the markdown file in place (unless --dry-run)
  - Prints a summary at the end: N captured, M failed, K already-recorded

Authored: Cherry retro Session 1A, 2026-05-14
"""

import argparse
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path


SAVE_PAGE_NOW_BASE = "https://web.archive.org/save/"
WAYBACK_AVAILABLE_BASE = "https://archive.org/wayback/available?url="
USER_AGENT = "plant-app-cherry-retro/1.0 (https://vegetables.garden; cherry-tomato verification audit trail)"
PENDING = "`<pending>`"


def parse_args():
    p = argparse.ArgumentParser(description="Capture archive.org snapshots for cherry retro URL log markdown.")
    p.add_argument("markdown_path", help="Path to URL log markdown file (e.g., cherry_retro_session_1a_anchor_claims_url_log.md)")
    p.add_argument("--dry-run", action="store_true", help="Don't write changes; just report what would be done")
    p.add_argument("--delay", type=float, default=6.0, help="Seconds between Save Page Now requests (default: 6.0)")
    p.add_argument("--retries", type=int, default=2, help="Retries per URL on transient failure (default: 2)")
    p.add_argument("--access-key", default=None, help="archive.org S3 access key (optional, for authenticated SPN)")
    p.add_argument("--secret-key", default=None, help="archive.org S3 secret key (optional)")
    p.add_argument("--prefer-existing", action="store_true",
                   help="Before SPN, check if an existing snapshot exists via Wayback Availability API and use that")
    return p.parse_args()


def extract_pending_entries(content):
    """
    Find all (anchoring_url, line_index_of_archive_pending, line_index_of_captured_pending) tuples
    in the markdown content where the Archive URL field is `<pending>`.

    The URL log format is:
        - **Anchoring URL:** <live URL>
        - **Anchoring quote:** "..."
        - **Archive URL:** `<pending>`
        - **Captured:** `<pending>`

    Returns a list of dicts: [{'url': str, 'archive_line': int, 'captured_line': int}, ...]
    """
    lines = content.split("\n")
    entries = []
    current_url = None
    current_archive_line = None

    url_pattern = re.compile(r"^\s*-\s*\*\*Anchoring URL:\*\*\s*(https?://\S+)\s*$")
    archive_pattern = re.compile(r"^\s*-\s*\*\*Archive URL:\*\*\s*`<pending>`\s*$")
    captured_pattern = re.compile(r"^\s*-\s*\*\*Captured:\*\*\s*`<pending>`\s*$")

    for i, line in enumerate(lines):
        m = url_pattern.match(line)
        if m:
            current_url = m.group(1).rstrip(".,;:")  # strip trailing punctuation defensively
            current_archive_line = None
            continue
        if archive_pattern.match(line) and current_url is not None:
            current_archive_line = i
            continue
        if captured_pattern.match(line) and current_url is not None and current_archive_line is not None:
            entries.append({
                "url": current_url,
                "archive_line": current_archive_line,
                "captured_line": i,
            })
            current_url = None
            current_archive_line = None

    return entries, lines


def check_existing_snapshot(url, timeout=15):
    """
    Query the Wayback Availability API for an existing snapshot.
    Returns the snapshot URL if one exists, else None.
    """
    api_url = WAYBACK_AVAILABLE_BASE + urllib.request.quote(url, safe="")
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            import json
            data = json.loads(resp.read().decode("utf-8"))
            closest = data.get("archived_snapshots", {}).get("closest", {})
            if closest.get("available") and closest.get("url"):
                return closest["url"]
    except Exception as e:
        sys.stderr.write(f"  Availability API check failed: {e}\n")
    return None


def save_page_now(url, retries, access_key=None, secret_key=None, timeout=60):
    """
    Hit the Save Page Now endpoint for <url>. Returns the snapshot URL on success, None on failure.
    Retries on transient failures. Authenticates with S3 keys if provided.
    """
    spn_url = SAVE_PAGE_NOW_BASE + url
    headers = {"User-Agent": USER_AGENT}
    if access_key and secret_key:
        headers["Authorization"] = f"LOW {access_key}:{secret_key}"

    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(spn_url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                # archive.org redirects to web.archive.org/web/<timestamp>/<url>
                final_url = resp.geturl()
                if "web.archive.org/web/" in final_url:
                    return final_url
                # Some responses don't redirect; read the headers for a Content-Location
                content_location = resp.headers.get("Content-Location")
                if content_location and content_location.startswith("/web/"):
                    return "https://web.archive.org" + content_location
                # Fallback: derive from the response URL with timestamp
                return final_url
        except urllib.error.HTTPError as e:
            if e.code in (429, 503, 504, 520, 523):
                # Transient: back off and retry
                if attempt < retries:
                    wait = (attempt + 1) * 30
                    sys.stderr.write(f"  HTTP {e.code}; backing off {wait}s and retrying...\n")
                    time.sleep(wait)
                    continue
            sys.stderr.write(f"  HTTPError {e.code}: {e.reason}\n")
            return None
        except urllib.error.URLError as e:
            sys.stderr.write(f"  URLError: {e.reason}\n")
            if attempt < retries:
                time.sleep(15)
                continue
            return None
        except Exception as e:
            sys.stderr.write(f"  Unexpected error: {e}\n")
            return None

    return None


def main():
    args = parse_args()
    md_path = Path(args.markdown_path)
    if not md_path.exists():
        sys.stderr.write(f"ERROR: file not found: {md_path}\n")
        sys.exit(1)

    content = md_path.read_text(encoding="utf-8")
    entries, lines = extract_pending_entries(content)

    if not entries:
        print("No <pending> archive entries found. Nothing to do.")
        sys.exit(0)

    print(f"Found {len(entries)} <pending> archive entries to capture.")
    print(f"Mode: {'DRY RUN (no writes)' if args.dry_run else 'WRITE BACK'}")
    print(f"Delay between requests: {args.delay}s; retries per URL: {args.retries}")
    if args.prefer_existing:
        print("Strategy: check Wayback Availability API first; use existing snapshot if found, else SPN.")
    else:
        print("Strategy: always Save Page Now (creates fresh snapshot).")
    print()

    today = date.today().isoformat()
    captured_count = 0
    failed_count = 0
    failed_urls = []

    for i, entry in enumerate(entries, start=1):
        url = entry["url"]
        print(f"[{i}/{len(entries)}] {url}")

        snapshot_url = None
        if args.prefer_existing:
            existing = check_existing_snapshot(url)
            if existing:
                print(f"  -> existing snapshot found: {existing}")
                snapshot_url = existing

        if snapshot_url is None:
            snapshot_url = save_page_now(url, args.retries, args.access_key, args.secret_key)
            if snapshot_url:
                print(f"  -> captured: {snapshot_url}")

        if snapshot_url:
            captured_count += 1
            # Update the markdown lines (preserving the indentation style)
            lines[entry["archive_line"]] = re.sub(
                r"`<pending>`",
                snapshot_url,
                lines[entry["archive_line"]],
            )
            lines[entry["captured_line"]] = re.sub(
                r"`<pending>`",
                today,
                lines[entry["captured_line"]],
            )
        else:
            failed_count += 1
            failed_urls.append(url)
            print(f"  -> FAILED; placeholder retained")

        # Rate-limit between requests (skip the wait after the last entry)
        if i < len(entries):
            time.sleep(args.delay)

    # Write back if not dry-run
    if not args.dry_run and captured_count > 0:
        md_path.write_text("\n".join(lines), encoding="utf-8")
        print()
        print(f"Wrote {captured_count} updates to {md_path}")

    print()
    print("=" * 60)
    print(f"SUMMARY")
    print("=" * 60)
    print(f"  Captured successfully: {captured_count}")
    print(f"  Failed (placeholder retained): {failed_count}")
    if failed_urls:
        print(f"  Failed URLs:")
        for u in failed_urls:
            print(f"    - {u}")
    print()
    print("Failures are typically transient (archive.org rate-limit, robots.txt, dead origin).")
    print("Re-run the script later; it will skip already-captured entries and retry pending ones.")


if __name__ == "__main__":
    main()
