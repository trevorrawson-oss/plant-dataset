#!/usr/bin/env python3
"""PLA-8: hedge the Bt safety absolute in CROP prose. Base afe4d697.

Rationale, the source read, and every edit: tools/build_bt_safety_content.py

WHAT MOVES. Nine `organic_treatment_beginner` strings on nine crops (kale, collards, spinach,
arugula, bok-choy, cauliflower, cabbage, brussels-sprouts, kohlrabi). NO control_method, NO source,
NO ladder, id, type or problem is touched, and no crop outside those nine.

THE SENTENCE HAS TWO DEFECTS AND THE SECOND IS THE WORSE ONE. "which is SAFE" is an unhedged
absolute; NPIC says "low in toxicity", "practically nontoxic", and never "safe" unqualified. But
"targets ONLY caterpillars" is literally true and consumer-MISLEADING: it reads as harmless to
everything you care about, when the non-target risk IS other caterpillars. NPIC: "a few studies
also found that non-target moths were harmed." So the replacement must carry BOTH the qualified
toxicity claim and the non-target caveat; either alone leaves the reader worse informed.

THE CATALOG ALREADY HAD IT RIGHT, for the third time this arc: `control_methods.bt` carries the
swallowtail-and-monarch caution and "it does not tell good caterpillars from bad". PLA-253 fixed the
METHOD and the remediation never reached the crops.

REFUSALS: base SHA mismatch; a crop or problem not found; a field missing; an `old` text that does
not match EXACTLY; a replacement that still matches a banned construction, or that drops the
qualified toxicity claim or the non-target caveat; a banned construction surviving anywhere in Bt
prose after the edit; any leaf changed outside the nine; a dash form barred in copy.

Guard suite:      tools/test_promote_bt_safety.py
Mutation harness: tools/mutate_bt_safety_suite.py (PLA-215)

Usage: python3 tools/promote_bt_safety.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "afe4d6978aa76ea3a0b8213f8c7f5e57e2dd373292ee20fd14e3f9e04de2fa6e"

PROSE_FIELDS = ("organic_treatment_beginner", "organic_treatment_seasoned",
                "prevention_beginner", "prevention_seasoned",
                "symptoms_beginner", "symptoms_seasoned",
                "cause_beginner", "cause_seasoned",
                "note_beginner", "note_seasoned")


def content():
    import build_bt_safety_content as B
    return B


def _crop_of(data, slug):
    for c in data["crops"]:
        if c.get("slug") == slug:
            return c
    return None


def _find(data, slug, problem_name):
    for c in data["crops"]:
        if c.get("slug") != slug:
            continue
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if isinstance(p, dict) and p.get("name") == problem_name:
                    return p
    return None


def iter_prose(data):
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if not isinstance(p, dict):
                    continue
                for f in PROSE_FIELDS:
                    v = p.get(f)
                    if isinstance(v, str):
                        yield (f"{c.get('slug')}/{p.get('name')}/{f}", v)


def check(data):
    B = content()
    seen = set()
    for slug, pname, field, old, new in B.EDITS:
        key = (slug, pname, field)
        if key in seen:
            return f"duplicate edit target {key}"
        seen.add(key)
        p = _find(data, slug, pname)
        if p is None:
            return f"{slug}: problem {pname!r} not found"
        if field not in p:
            return f"{slug}/{pname}: field {field!r} missing"
        if p[field] != old:
            return (f"{slug}/{pname}/{field}: text does not match exactly; already applied, or the "
                    f"prose changed under this promote")
        if old == new:
            return f"{slug}/{pname}/{field}: edit is a no-op"
        for pat in B.BANNED:
            if re.search(pat, new, re.I):
                return f"{slug}/{pname}/{field}: replacement still matches banned {pat!r}"
        if not re.search(B.REQUIRED_QUALIFIER, new, re.I):
            return f"{slug}/{pname}/{field}: replacement drops the qualified toxicity claim"
        if not re.search(B.REQUIRED_NONTARGET, new, re.I):
            return (f"{slug}/{pname}/{field}: replacement drops the non-target caveat; without it "
                    f"the reader is still told Bt hits nothing they care about")
        if re.search(r"[—–]", new) or "--" in new:
            return f"{slug}/{pname}/{field}: replacement introduces a dash form barred in copy"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    B = content()
    n = 0
    for slug, pname, field, old, new in B.EDITS:
        p = _find(data, slug, pname)
        assert p is not None and p[field] == old, "check() must run before apply_to()"
        p[field] = new
        n += 1
    return n


def verify_post(data):
    B = content()
    for label, text in iter_prose(data):
        if not re.search(B.SCOPE, text, re.I):
            continue
        for pat in B.BANNED:
            if re.search(pat, text, re.I):
                return f"banned construction {pat!r} survives at {label}"
    for slug, pname, field, _old, new in B.EDITS:
        p = _find(data, slug, pname)
        if p is None or p.get(field) != new:
            return f"{slug}/{pname}/{field}: post-state text is not the intended replacement"
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
    print("PLA-8 -- Bt safety absolute, crop prose")
    print(f"  fields rewritten : {n} across {len({e[0] for e in B.EDITS})} crops")
    for slug, _p, field, _o, _n in B.EDITS:
        print(f"    {slug:18s} {field}")
    print(f"  untouched, correctly-stated efficacy 'only': {', '.join(B.CORN_EFFICACY_ONLY)}")
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
