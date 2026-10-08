#!/usr/bin/env python3
"""export_staleness_gate -- how far behind is each consumer's dataset pin? INFORMATIONAL (PLA-713).

WHAT THIS IS NOW. Since the split (PLA-713, ruled 2026-10-07) both consumers build from a PINNED
dataset revision -- plant-astro by its `plant-dataset` submodule, plant-app by its
`vendor/plant-dataset` submodule -- and data bumps happen only on Trevor's call, both repos the same
day, through the PLA-712 template. A consumer sitting behind this repo's origin/main is therefore
the EXPECTED state, not a defect, and this tool only says how far behind each one is:

  E1 APP-PIN    plant-app's pinned dataset commit, read from plant-app's ORIGIN
  E3 ASTRO-PIN  plant-astro's pinned dataset commit, read from plant-astro's ORIGIN

For each: the pinned commit, how many dataset commits it is behind origin/main, and whether the
canonical at the pin is byte-identical to the canonical at origin/main (tooling-only commits put a
consumer "behind" without changing a byte it serves).

IT NEVER BLOCKS. The CLI exits 0 whatever it finds, and nothing in the commit or push path calls it
as a gate (the pre-commit hook no longer touches either consumer).

IT READS ORIGINS, NEVER A CHECKOUT. Each pin is the gitlink recorded in the consumer's branch on its
origin, fetched into a throwaway bare repo. A local `~/plant-app` or `~/plant-astro` checkout, its
working tree and its export are never opened: what ships is what the consumer's origin pins.

WHAT IT REPLACED. PLA-258 (2026-08-19) built E1/E2/E3 as a BLOCKING currency gate after both
consumers silently served a three-week-old canonical: E1 compared the app's export stamp in
`~/plant-app` to the live canonical, E2 hashed that checkout's artifacts, E3 required the astro pin
to carry the live canonical. The split makes "behind" deliberate, so blocking on it would be a check
that is always red. E2 is retired here: the app checks its own export against its own pin, inside
its repo (`src/lib/dataset-pin.test.ts`, PLA-713 [APP]). The PLA-258 lesson survives as the
UNMEASURED channel: a pin that cannot be read is reported as unmeasured, never as current.

Usage:
  export_staleness_gate.py [--no-fetch] [--json]
Exit 0 always (2 only on a usage error).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

DATASET_REF = "refs/remotes/origin/main"
CANONICAL = "crops_data_final.json"

# (check, label, origin url, branch the consumer ships from, gitlink path). The branches are the ones
# PLA-713 pinned: the app ships from feat/community-foundation, the site from main (Netlify).
CONSUMERS = (
    ("E1", "app", "https://github.com/trevorrawson-oss/plant-app.git",
     "feat/community-foundation", "vendor/plant-dataset"),
    ("E3", "astro", "https://github.com/trevorrawson-oss/plant-astro.git",
     "main", "plant-dataset"),
)


def _git(repo, *args):
    """stdout of a git command, or None if it failed. Never raises."""
    try:
        r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    except OSError:
        return None
    return r.stdout.decode("utf-8", "replace").strip() if r.returncode == 0 else None


def _git_bytes(repo, *args):
    try:
        r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def origin_gitlink(url, branch, path):
    """(pinned commit, None) or (None, why). Fetches the consumer branch's tip from its ORIGIN into a
    throwaway bare repo and reads the gitlink there. Trees only (blob:none): a gitlink is a tree entry."""
    tmp = tempfile.mkdtemp(prefix="consumer-pin-")
    try:
        if _git(tmp, "init", "--bare", "-q") is None:
            return None, "could not create a scratch repo"
        if _git(tmp, "fetch", "-q", "--depth=1", "--filter=blob:none", url,
                f"refs/heads/{branch}") is None:
            return None, f"could not fetch {branch} from {url}"
        entry = _git(tmp, "ls-tree", "FETCH_HEAD", path)
        if not entry:
            return None, f"{branch} on origin records no `{path}` entry"
        parts = entry.split()
        if len(parts) < 3 or parts[0] != "160000":
            return None, f"`{path}` on origin {branch} is not a submodule gitlink (mode {parts[0]})"
        return parts[2], None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def pin_status(check, label, url, branch, path, dataset_root=REPO, dataset_ref=DATASET_REF):
    """One consumer's row. `measured` is False when the pin, or its place in this repo's history,
    could not be established -- that row is UNMEASURED, never read as current."""
    row = {"check": check, "consumer": label, "origin": url, "branch": branch, "path": path,
           "pinned": None, "head": None, "behind": None, "ahead": None,
           "canonical_same": None, "measured": False, "note": None}
    head = _git(dataset_root, "rev-parse", "--verify", f"{dataset_ref}^{{commit}}")
    if head is None:
        row["note"] = f"this repo has no {dataset_ref}"
        return row
    row["head"] = head
    pinned, why = origin_gitlink(url, branch, path)
    if pinned is None:
        row["note"] = why
        return row
    row["pinned"] = pinned
    if _git(dataset_root, "cat-file", "-e", f"{pinned}^{{commit}}") is None:
        row["note"] = (f"pinned commit {pinned[:12]} is not in this repo's history "
                       f"(unpushed, rewritten, or unfetched)")
        return row
    behind = _git(dataset_root, "rev-list", "--count", f"{pinned}..{head}")
    ahead = _git(dataset_root, "rev-list", "--count", f"{head}..{pinned}")
    pin_canon = _git_bytes(dataset_root, "show", f"{pinned}:{CANONICAL}")
    head_canon = _git_bytes(dataset_root, "show", f"{head}:{CANONICAL}")
    if behind is None or ahead is None or pin_canon is None or head_canon is None:
        row["note"] = "could not count commits or read the canonical at the pin"
        return row
    row.update(behind=int(behind), ahead=int(ahead), measured=True,
               canonical_same=pin_canon == head_canon,
               pinned_canonical=hashlib.sha256(pin_canon).hexdigest(),
               head_canonical=hashlib.sha256(head_canon).hexdigest())
    if row["ahead"]:
        row["note"] = f"pin is NOT on {dataset_ref}: {row['ahead']} commit(s) only the pin has"
    return row


def report(consumers=None, dataset_root=None, dataset_ref=DATASET_REF, fetch=True):
    """Defaults resolve at CALL time, so a test can point main() at fixture origins."""
    consumers = CONSUMERS if consumers is None else consumers
    dataset_root = REPO if dataset_root is None else dataset_root
    if fetch:
        _git(dataset_root, "fetch", "-q", "origin")
    rows = [pin_status(*c, dataset_root=dataset_root, dataset_ref=dataset_ref) for c in consumers]
    return {"dataset_ref": dataset_ref,
            "head": _git(dataset_root, "rev-parse", "--verify", f"{dataset_ref}^{{commit}}"),
            "consumers": rows,
            "measured": sum(r["measured"] for r in rows),
            "unmeasured": sum(not r["measured"] for r in rows)}


def format_row(r):
    where = f"{r['consumer']} ({r['branch']}:{r['path']})"
    if not r["measured"]:
        return f"{r['check']} UNMEASURED {where}: {r['note']}"
    canon = (f"canonical identical ({r['pinned_canonical'][:8]})" if r["canonical_same"] else
             f"canonical differs (pin {r['pinned_canonical'][:8]}, origin/main {r['head_canonical'][:8]})")
    line = (f"{r['check']} {where}: pin {r['pinned'][:7]}, {r['behind']} dataset commit(s) behind "
            f"origin/main {r['head'][:7]}; {canon}")
    return line + (f"; {r['note']}" if r["note"] else "")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-fetch", action="store_true",
                    help="measure against this repo's existing origin/main ref without fetching it")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    r = report(fetch=not a.no_fetch)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        for row in r["consumers"]:
            print(format_row(row))
        print(f"export_staleness_gate: {len(r['consumers'])} consumer(s), {r['measured']} measured, "
              f"{r['unmeasured']} unmeasured. Informational only: consumers are pinned and data bumps "
              f"happen only on Trevor's call (PLA-713). Never blocks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
