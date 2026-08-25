#!/usr/bin/env python3
"""PLA-8: widen the 10 catalog `best_use` fields narrower than their own shipped usage. Base decb944d.

The content and the reasoning: tools/build_pla8_bestuse_content.py.

WHAT MOVES. Exactly 10 strings, all `control_methods.<key>.best_use`. NO crop is touched, NO other
field of any method, NO source, NO ladder, NO roster change. This is a pure catalog-prose promote.

WHY IT IS WORTH A PROMOTE. `best_use` is read on two surfaces at once: `ladder_batch.py prepare`
hands it to every authoring agent as "what the method MEANS", and `MethodSheet.tsx` renders it to
users under "When to reach for it". Measured during batch 3, 11 of 49 shipped methods carried a
best_use narrower than their real use, and in that one batch it produced four false gaps plus one
genuinely missing rung. With ~34 batches left it is a recurring tax on every authoring pass.

ONE OF THE ELEVEN IS CORRECT AS WRITTEN. `bottom_watering` names both its shipped problems and
correctly confines itself to indoor trays and seedlings; that confinement is the very distinction
twelve batch-1 rungs got wrong (`bottom_watering` MEANS water from below in trays, not water at the
base outdoors). check() REFUSES if it is edited. Read, do not count: 11 flagged, 10 real.

ONE OF THE TEN IS A FACTUAL CORRECTION, not a widening. `off_season_tillage` was minted in batch 2's
catalog round and glossed around the hornworms that motivated it, so it named a life stage European
corn borer does not have. The borer overwinters INSIDE THE STALK, per sweet-corn's own sourced prose
("the borer overwinters in old stalks; shred and turn under cornstalks after harvest"). The ACTION
was correct the whole time; only the stated mechanism was too narrow.

REFUSALS: base SHA mismatch; any crop changed; any method other than the 10 changed; any field other
than best_use changed on the 10; bottom_watering not byte-identical; a current best_use that is not
the expected text (someone else edited it); a copy-hygiene violation in the new prose.

Guard suite:      tools/test_promote_pla8_bestuse.py
Mutation harness: tools/mutate_pla8_bestuse_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_bestuse.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "decb944d51e591ef9c7b0f657a258a0a7690f2ad1aa8804dad4b83a235db90c0"

BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def content():
    import build_pla8_bestuse_content as C
    return C


def hygiene(s):
    """Consumer-copy rules; best_use renders in MethodSheet.tsx. Returns a reason or None."""
    if re.search(r"[—–]", s):
        return "em or en dash"
    if "--" in s:
        return "double hyphen"
    if re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I):
        return "absolute claim"
    if re.search(r"\s°F", s):
        return "spaced degF"
    for w in BRITISH:
        if re.search(rf"\b{w}\b", s, re.I):
            return f"British spelling {w!r}"
    if re.search(r"(?<![.!?]\s)(?<!^)\bPlant\b(?! Pro)", s):
        return "capital Plant mid-sentence"
    if re.search(r"\b(?:is|are)\s+safe\b", s, re.I):
        return "bare safety claim"
    return None


def check(data):
    C = content()
    cm = data.get("control_methods") or {}

    for key in C.EXCLUDED:
        if key in C.WIDENINGS:
            return f"{key} is in BOTH EXCLUDED and WIDENINGS"
        if key not in cm:
            return f"EXCLUDED method {key!r} is not in the catalog"

    for key, w in C.WIDENINGS.items():
        if key not in cm:
            return f"no catalog method {key!r}"
        cur = cm[key].get("best_use")
        if cur == w["new"]:
            return f"{key}: already widened"
        if cur != w["old"]:
            return (f"{key}: best_use is not the expected text, so it changed under this pass. "
                    f"expected {w['old'][:70]!r}, found {str(cur)[:70]!r}")
        bad = hygiene(w["new"])
        if bad:
            return f"{key}: new best_use fails copy hygiene ({bad})"
    if len(C.WIDENINGS) != 10:
        return f"expected 10 widenings, found {len(C.WIDENINGS)}"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    C = content()
    return C.apply_widenings(data["control_methods"])


def verify_post(data):
    C = content()
    cm = data.get("control_methods") or {}
    for key, w in C.WIDENINGS.items():
        if cm.get(key, {}).get("best_use") != w["new"]:
            return f"post: {key} does not carry the widened text"
    for key in C.EXCLUDED:
        if key not in cm:
            return f"post: EXCLUDED {key!r} vanished"
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

    C = content()
    print("PLA-8 -- best_use widened where it was narrower than its own shipped use")
    print(f"  methods widened : {n}")
    print(f"  left alone      : {len(C.EXCLUDED)} ({', '.join(C.EXCLUDED)}) -- correct as written")
    print(f"  crops touched   : 0")
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
