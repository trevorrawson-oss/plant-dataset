#!/usr/bin/env python3
"""promote_pla626_delete_first -- PLA-626 delete-first on apricot and plum. Base d8906b43 (PLA-457 landed).

Trevor rulings 2026-09-29, from the chat review at _handoff/pla626_delete_first_review.md.
Spec: tools/staging/pla626_delete_first/spec.json.

WHAT MOVES (the PLA-533 subtractive pattern: remove what is wrong, add nothing, cite nothing new):
  apricot  recommended_rootstock "Myrobalan 29C" -> null. FNRIC confines Myrobalan to very heavy or wet
           soils (graft-union breakage in wind); UC IPM's apricot PMG calls plum-parentage stocks highly
           susceptible to bacterial canker. Nothing is promoted into it (a new pick is PLA-566's).
  apricot  rootstock_options[2] (Marianna 2624) traits_seasoned: the wrong-crop "prune brownline" cut.
  plum     recommended_rootstock_note: St. Julien (row dropped, attribution retracted by PLA-466) and
           "and containers" (Marianna's container flag is null, not assessed) cut; the Myrobalan
           heavier/wetter-soils clause STAYS by ruling (FNRIC supports it).
  plum     container_notes notes_beginner + notes_seasoned: St. Julien cut.

KEPT BY RULING (re-verification narrowed the ticket): apricot's Myrobalan-canker, Lovell-canker and Marianna
nematode/oak-root text is supported by UC IPM's apricot Pest Management Guidelines, so it is an attribution
defect for PLA-566's final pass, not wrong text; plum soil "or Myrobalan"; plum Guardian "Lovell, Halford".

WHY EACH GUARD EXISTS.
 1. PINNED BASE: the canonical must hash to BASE_SHA.
 2. CHANGE SET: every edit is on apricot or plum.
 3. EXACT-ONCE: every edit's before-text occurs exactly once in its field.
 4. NOTHING ADDED: an after-text may repair grammar, but a digit, URL or citation token refuses.
 5. PINNED RETRACTION: only apricot /recommended_rootstock may be retracted, and only from "Myrobalan 29C".
 6. PINNED ROW: apricot rootstock_options[2] must be Marianna 2624, so a reordered list cannot aim the cut
    at another row.
 7. SET BEFORE VALUE: crop set and order equal before any comparison; top-level keys byte-equal.
 8. BLAST RADIUS BY REVERSAL: the declared changes are undone on a copy of each changed post crop and the
    result must equal the pre crop exactly; every other crop byte-equal.
 9. PURPOSE: no consumer string on plum names St. Julien and none on apricot names prune brownline after the
    pass (verification_status is history and exempt). Guard 8 cannot see an edit the SPEC forgot; this can.

Usage:
    promote_pla626_delete_first.py --check [canonical]
    promote_pla626_delete_first.py --out /path/scratch.json [canonical]
    promote_pla626_delete_first.py --expect-sha <sha> [canonical]     # writes canonical, on approval
"""
import argparse
import copy
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
SPEC = os.path.join(HERE, "staging", "pla626_delete_first", "spec.json")

BASE_SHA = "d8906b4313864161c361534cde1b8404c93a81ce44cc5640bf5f51f624b23ce9"
CHANGED = ("apricot", "plum")
RETRACTION = ("apricot", "/recommended_rootstock", "Myrobalan 29C")
MARIANNA = "Marianna 2624 (plum)"
ST_JULIEN = re.compile(r"st\.?\s*julien", re.I)
BROWNLINE = re.compile(r"brownline", re.I)


def refuse(msg):
    raise SystemExit(f"REFUSED: {msg}")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    """CANONICAL IS COMPACT."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def staged(path=None):
    with open(path or SPEC, encoding="utf-8") as f:
        return json.load(f)


def check_base_sha(raw):
    got = sha256(raw)
    if got != BASE_SHA:
        refuse(f"base sha mismatch: {got[:16]} != {BASE_SHA[:16]}")


def _split(ptr):
    return ptr.strip("/").split("/")


def at(crop, ptr):
    n = crop
    for p in _split(ptr):
        n = n[int(p)] if isinstance(n, list) else n[p]
    return n


def _set(crop, ptr, value):
    parts = _split(ptr)
    n = crop
    for p in parts[:-1]:
        n = n[int(p)] if isinstance(n, list) else n[p]
    k = parts[-1]
    if isinstance(n, list):
        n[int(k)] = value
    else:
        n[k] = value


def _words(s):
    return re.findall(r"[A-Za-z0-9'-]+", s.lower())


def consumer_hits(crop, pattern):
    """Paths of consumer strings on a crop matching pattern; verification_status is append-only history."""
    out = []

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                if p == "" and k == "verification_status":
                    continue
                walk(v, f"{p}/{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{p}/{i}")
        elif isinstance(o, str) and pattern.search(o):
            out.append(p)
    walk(crop, "")
    return out


def check_spec(spec):
    for e in spec["edits"]:
        if e["crop"] not in CHANGED:
            refuse(f"edit on {e['crop']} is outside the change set {CHANGED}")
        added = [w for w in _words(e["after"]) if w not in set(_words(e["before"]))]
        if any(re.search(r"\d", w) for w in added) or re.search(r"https?://|www\.|_ext\b|\bsources?\b", e["after"]):
            refuse(f"{e['crop']}{e['path']}: after-text adds a number or citation token: {added}")
    for r in spec["retractions"]:
        if (r["crop"], r["path"], r["before"]) != RETRACTION or r["after"] is not None:
            refuse(f"retraction outside the pinned field: {r['crop']}{r['path']} {r['before']!r}")


def apply_to(data, spec):
    check_spec(spec)
    C = {c["slug"]: c for c in data["crops"]}
    apricot = C["apricot"]
    if at(apricot, "/rootstock_options/2").get("name") != MARIANNA:
        refuse(f"apricot rootstock_options[2] is not Marianna 2624: {at(apricot, '/rootstock_options/2').get('name')!r}")
    for e in spec["edits"]:
        crop = C[e["crop"]]
        cur = at(crop, e["path"])
        n = cur.count(e["before"]) if isinstance(cur, str) else 0
        if n != 1:
            refuse(f"{e['crop']}{e['path']}: target found {n} times, expected exactly 1: {e['before'][:60]!r}")
        _set(crop, e["path"], cur.replace(e["before"], e["after"], 1))
    for r in spec["retractions"]:
        crop = C[r["crop"]]
        if at(crop, r["path"]) != r["before"]:
            refuse(f"{r['crop']}: recommended_rootstock pre-state is not the pinned value: {at(crop, r['path'])!r}")
        _set(crop, r["path"], None)
    return data


def _revert(pre_crop, post_crop, spec):
    """Undo every DECLARED change on a copy of the post crop; the result must equal the pre crop."""
    q = copy.deepcopy(post_crop)
    slug = pre_crop["slug"]
    for e in spec["edits"]:
        if e["crop"] == slug:
            _set(q, e["path"], at(pre_crop, e["path"]))
    for r in spec["retractions"]:
        if r["crop"] == slug:
            _set(q, r["path"], at(pre_crop, r["path"]))
    return q


def check_post(pre, post, spec):
    P = [c["slug"] for c in pre["crops"]]
    Q = [c["slug"] for c in post["crops"]]
    if set(P) != set(Q) or P != Q:
        refuse("crop set changed between pre and post")
    if set(pre) != set(post) or any(pre[k] != post[k] for k in pre if k != "crops"):
        refuse("a top-level key changed")
    for a, b in zip(pre["crops"], post["crops"]):
        slug = a["slug"]
        if slug not in CHANGED:
            if a != b:
                refuse(f"collateral change on {slug}")
            continue
        if _revert(a, b, spec) != a:
            refuse(f"undeclared change inside {slug}")
    Q = {c["slug"]: c for c in post["crops"]}
    left = consumer_hits(Q["plum"], ST_JULIEN)
    if left:
        refuse(f"St. Julien survives in plum consumer text: {left}")
    left = consumer_hits(Q["apricot"], BROWNLINE)
    if left:
        refuse(f"prune brownline survives in apricot consumer text: {left}")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--out")
    g.add_argument("--expect-sha")
    ap.add_argument("canonical", nargs="?", default=None)
    args = ap.parse_args()
    path = args.canonical or CANON
    raw = open(path, "rb").read()
    check_base_sha(raw)
    spec = staged()
    pre = json.loads(raw)
    post = apply_to(copy.deepcopy(pre), spec)
    check_post(pre, post, spec)
    out = serialize(post)
    sha = sha256(out)
    print(f"promote_pla626_delete_first: {len(spec['edits'])} edits, {len(spec['retractions'])} retraction; "
          f"post sha {sha}")
    if args.check:
        print("--check: nothing written")
        return
    if args.out:
        with open(args.out, "wb") as f:
            f.write(out)
        print(f"wrote {args.out} (canonical untouched)")
        return
    if sha != args.expect_sha:
        refuse(f"post sha {sha} != --expect-sha {args.expect_sha}")
    with open(path, "wb") as f:
        f.write(out)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
