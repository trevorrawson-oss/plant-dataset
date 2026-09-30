#!/usr/bin/env python3
"""promote_pla533_subtractive -- PLA-533 subtractive pass. Base edcd9bf9.

Trevor rulings 2026-09-29 (two batches), from the chat review at _handoff/pla533_subtractive_review.md.
Spec: tools/staging/pla533_subtractive/spec.json.

WHAT MOVES, on five crops (orange-navel, grapefruit, mandarin-clementine, lemon, lime):
  1. 29 string edits inside named fields: 11 whole-sentence deletes and 18 rewrites that remove a
     contradicted clause and repair the grammar left behind (sulfur acidification, navel juice freezing,
     "best fruit tree in a pot", the 100-200+ lb yield, the leaked kickoff note, two dangling "See the
     ... note" references, lemon's "not a reason to choose against this one", grapefruit's wrong-crop
     Flying Dragon clause, lime's sour orange note sentence, and orange-navel's beginner pot sentence
     replaced with Trevor's text).
  2. Flying Dragon container_size_gallons 25 -> null on orange-navel and grapefruit (shape B);
     container_suitable stays true, unsourced (PLA-612).
  3. lime: the sour orange rootstock row is REMOVED and recommended_rootstock is RETRACTED to null
     (PLA-466 shape; rough lemon is NOT promoted into it).
Nothing adds a claim, a number or a citation. NONE of this resolves a PLA-533 blocking finding: the
seven findings and all launch flags are byte-identical after the pass (only a clause-checked re-author
closes a finding).

Third batch (2026-09-29): lime row 1's comparison sentence "...than sour orange." is DELETED with the
row it compared against (it had been held, shown, then approved).

WHY EACH GUARD EXISTS.
 1. PINNED BASE: the canonical must hash to BASE_SHA.
 2. EXACT-ONCE: every edit's before-text must occur exactly once in its field (0 or 2+ refuses).
 3. NOTHING ADDED: an after-text may repair grammar, but a digit, URL or citation token refuses.
 4. PINNED STRUCTURE: lime's row 0 must be the sour orange row, recommended_rootstock its exact
    pre-state, and Flying Dragon's gallons 25 with container_suitable true, or the promote refuses.
 6. SET BEFORE VALUE: set(pre crops) == set(post crops) and order unchanged before any comparison.
 7. BLAST RADIUS BY REVERSAL: for each changed crop, the declared changes are reverted on a copy of
    the post and the result must equal the pre crop EXACTLY. Anything else that moved -- a resolved
    finding, a flipped flag, a container flag, any stray key -- is an undeclared change and refuses.
    Every other crop and every top-level key must be byte-equal.

Usage:
    promote_pla533_subtractive.py --check
    promote_pla533_subtractive.py --out /path/scratch.json
    promote_pla533_subtractive.py --expect-sha <sha>      # writes canonical, on approval
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
SPEC = os.path.join(HERE, "staging", "pla533_subtractive", "spec.json")

BASE_SHA = "edcd9bf95ad7e3a90ada7c522db23e00172d1f57d74ff33da219908d7a266229"
CHANGED = ("orange-navel", "grapefruit", "mandarin-clementine", "lemon", "lime")
LIME_ROW = "sour orange (Citrus aurantium)"
LIME_REC = "sour orange (Citrus aurantium), or rough lemon on sandy and calcareous soils"
FD_NAME = "Flying Dragon trifoliate"


def refuse(msg):
    raise SystemExit(f"REFUSED: {msg}")


def staged(path=None):
    with open(path or SPEC, encoding="utf-8") as f:
        return json.load(f)


def check_base_sha(raw):
    got = hashlib.sha256(raw).hexdigest()
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


def check_spec(spec):
    for e in spec["edits"]:
        if e["crop"] not in CHANGED:
            refuse(f"edit on {e['crop']} is outside the change set {CHANGED}")
        added = [w for w in _words(e["after"]) if w not in set(_words(e["before"]))]
        if any(re.search(r"\d", w) for w in added) or re.search(r"https?://|_ext\b|uf_ifas|\bsources?\b", e["after"]):
            refuse(f"{e['crop']}{e['path']}: after-text adds a number or citation token: {added}")


def apply_to(data, spec):
    check_spec(spec)
    C = {c["slug"]: c for c in data["crops"]}
    for e in spec["edits"]:
        crop = C[e["crop"]]
        cur = at(crop, e["path"])
        n = cur.count(e["before"]) if isinstance(cur, str) else 0
        if n != 1:
            refuse(f"{e['crop']}{e['path']}: target found {n} times, expected exactly 1: {e['before'][:60]!r}")
        # a whole-sentence delete removes the sentence and the single space that joined it
        if not e["after"] and (" " + e["before"]) in cur:
            new = cur.replace(" " + e["before"], "", 1)
        else:
            new = cur.replace(e["before"], e["after"], 1)
        _set(crop, e["path"], new.strip())
    for r in spec["retractions"]:
        crop = C[r["crop"]]
        row = at(crop, "/rootstock_options/2")
        if row.get("name") != FD_NAME or row.get("container_size_gallons") != r["before"] or row.get("container_suitable") is not True:
            refuse(f"{r['crop']}: Flying Dragon container_size_gallons pre-state is not 25 with container_suitable true")
        row["container_size_gallons"] = None
    lime = C["lime"]
    rows = lime["rootstock_options"]
    if not rows or rows[0].get("name") != LIME_ROW or sum(1 for x in rows if x.get("name") == LIME_ROW) != 1:
        refuse("lime: the sour orange row is not exactly once at index 0")
    if lime.get("recommended_rootstock") != LIME_REC:
        refuse(f"lime: recommended_rootstock pre-state is not the pinned value: {lime.get('recommended_rootstock')!r}")
    rows.pop(0)
    lime["recommended_rootstock"] = None
    return data


def _revert(pre_crop, post_crop, spec):
    """Undo every DECLARED change on a copy of the post crop; the result must equal the pre crop."""
    q = copy.deepcopy(post_crop)
    slug = pre_crop["slug"]
    if slug == "lime":
        q["rootstock_options"].insert(0, copy.deepcopy(pre_crop["rootstock_options"][0]))
        q["recommended_rootstock"] = pre_crop["recommended_rootstock"]
    for e in spec["edits"]:
        if e["crop"] == slug:
            _set(q, e["path"], at(pre_crop, e["path"]))
    for r in spec["retractions"]:
        if r["crop"] == slug:
            q["rootstock_options"][2]["container_size_gallons"] = pre_crop["rootstock_options"][2]["container_size_gallons"]
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


def serialize(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--out")
    g.add_argument("--expect-sha")
    args = ap.parse_args()
    raw = open(CANON, "rb").read()
    check_base_sha(raw)
    spec = staged()
    pre = json.loads(raw)
    post = apply_to(copy.deepcopy(pre), spec)
    check_post(pre, post, spec)
    out = serialize(post)
    sha = hashlib.sha256(out).hexdigest()
    print(f"promote_pla533_subtractive: {len(spec['edits'])} edits, {len(spec['retractions'])} retractions, "
          f"lime row removed + recommended_rootstock retracted; post sha {sha}")
    if args.check:
        return
    if args.out:
        with open(args.out, "wb") as f:
            f.write(out)
        print(f"wrote {args.out}")
        return
    if sha != args.expect_sha:
        refuse(f"post sha {sha} != --expect-sha {args.expect_sha}")
    with open(CANON, "wb") as f:
        f.write(out)
    print(f"wrote {CANON}")


if __name__ == "__main__":
    main()
