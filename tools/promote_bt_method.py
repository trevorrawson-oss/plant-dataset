#!/usr/bin/env python3
"""PLA-8: close the Bt safety absolute in the CATALOG method. Base 0e12689b.

Rationale, the source read, and the 13 correct-as-written hits left alone:
tools/build_bt_method_content.py

WHAT MOVES. ONE string: `control_methods.bt.how_it_works_beginner`. Nothing else in the whole
dataset. No crop, no other method, no source, no ladder.

This is the LAST of the class. `cffa4a7` closed the iron-phosphate absolute in crop prose (9 fields
/ 6 crops), `9116050` closed the Bt absolute in crop prose (9 fields / 9 crops), and this closes the
Bt absolute in the catalog method those crops point at.

WHY IT WAS LEFT UNTIL NOW rather than folded into 9116050: it is a different file and a different
claim, and folding it in would have been the scope creep this arc deliberately resisted three times.
The Bt sweep's own guard suite asserted `control_methods` was unchanged, so leaving it was explicit
rather than an oversight.

REFUSALS: base SHA mismatch; the method or field missing; `old` text not matching EXACTLY; a banned
construction surviving in the replacement; a required element missing from the replacement; any
other bt field changed; any other control_method changed; any crop changed; a dash form barred in
copy.

Guard suite:      tools/test_promote_bt_method.py
Mutation harness: tools/mutate_bt_method_suite.py (PLA-215)

Usage: python3 tools/promote_bt_method.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "0e12689ba616bca3316652c9064ca9cbce4aa0c4037b1b69589a1e397abb88a4"


def content():
    import build_bt_method_content as B
    return B


def check(data):
    B = content()
    cm = data["control_methods"]
    if B.METHOD not in cm:
        return f"control_methods.{B.METHOD} missing"
    m = cm[B.METHOD]
    if B.FIELD not in m:
        return f"{B.METHOD}.{B.FIELD} missing"
    if m[B.FIELD] != B.OLD:
        return (f"{B.METHOD}.{B.FIELD}: text does not match exactly; already applied, or the prose "
                f"changed under this promote")
    if B.OLD == B.NEW:
        return "edit is a no-op"
    for pat in B.BANNED:
        if re.search(pat, B.NEW, re.I):
            return f"replacement still matches banned {pat!r}"
    for label, pat in B.REQUIRED.items():
        if not re.search(pat, B.NEW, re.I):
            return f"replacement is missing {label!r}"
    if re.search(r"[—–]", B.NEW) or "--" in B.NEW:
        return "replacement introduces a dash form barred in consumer copy"
    # the correct-as-written methods must still be there to be left alone
    for k in B.CORRECT_AS_WRITTEN:
        if k not in cm:
            return f"correct-as-written method {k!r} is not in the catalog"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    B = content()
    data["control_methods"][B.METHOD][B.FIELD] = B.NEW
    return 1


def verify_post(data):
    B = content()
    m = data["control_methods"][B.METHOD]
    if m[B.FIELD] != B.NEW:
        return "the replacement did not land"
    for pat in B.BANNED:
        if re.search(pat, m[B.FIELD], re.I):
            return f"banned construction {pat!r} survives"
    for label, pat in B.REQUIRED.items():
        if not re.search(pat, m[B.FIELD], re.I):
            return f"post-state is missing {label!r}"
    # the field must no longer contradict itself
    low = m[B.FIELD].lower()
    if "only affects caterpillars" in low and "cannot tell" in low:
        return "the field still says both 'only affects caterpillars' and 'cannot tell'"
    # NPIC's own term of art must survive in the seasoned register and pros
    if "practically nontoxic" not in m["how_it_works_seasoned"].lower():
        return ("how_it_works_seasoned lost 'practically nontoxic', which is NPIC's own phrasing "
                "and is already qualified; rewriting it would make the record less faithful")
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != a.expect_sha:
        print(f"ABORT: base SHA mismatch\n  expected {a.expect_sha}\n  found    {sha}", file=sys.stderr)
        return 1
    data = json.loads(raw.decode("utf-8"))

    problem = check(data)
    if problem:
        print("ABORT: " + problem, file=sys.stderr)
        return 1

    n = apply_to(data)

    problem = verify_post(data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    B = content()
    print("PLA-8 -- the Bt safety absolute, CATALOG method (the last of the class)")
    print(f"  rewritten    : control_methods.{B.METHOD}.{B.FIELD}  ({n} string)")
    print(f"  dropped      : 'only affects caterpillars', 'is safe to eat'")
    print(f"  kept         : the eye/skin caution, the non-target caveat, "
          f"NPIC's 'practically nontoxic' in the seasoned register")
    print(f"  left alone   : {len(B.CORRECT_AS_WRITTEN)} correct-as-written methods "
          f"(non-toxic on cardboard, glue and pheromone)")
    out = serialize(data)
    new_sha = hashlib.sha256(out).hexdigest()
    if a.dry_run or not a.apply:
        print(f"DRY RUN -- would write {len(out)} bytes, sha {new_sha}")
        return 0
    open(a.canonical, "wb").write(out)
    print(f"wrote {len(out)} bytes\nnew canonical SHA: {new_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
