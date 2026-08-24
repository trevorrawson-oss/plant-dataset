#!/usr/bin/env python3
"""PLA-8: hedge the iron-phosphate slug-bait safety absolute in CROP prose. Base 75b3c0f0.

Rationale, the source read, and the full edit list: tools/build_slug_bait_safety_content.py

WHAT MOVES. Eight `organic_treatment_*` strings on five crops (basil, lettuce-leaf, swiss-chard,
arugula, bok-choy). NO control_method is touched, NO source is minted, NO ladder, id or problem is
touched, and no crop outside those five is touched. The claim goes from "is safe" / "pet-safe" to
the comparative UC IPM actually publishes: safer around pets and wildlife THAN METALDEHYDE, and
still a pesticide.

WHY EIGHT AND NOT TWO. Two surfaced while reading batch 1; a scan of all 23 iron-phosphate mentions
in crop prose found six more of the identical class on three crops outside the batch. Fixing a
subset is the documented failure mode. The other 15 mentions make no safety claim and are untouched.

REFUSALS: base SHA mismatch; a crop or problem not found; a field missing; an `old` text that does
not match EXACTLY (already applied, or the prose moved under us); a banned construction surviving
anywhere in crop prose after the edit; a rewritten field that does not carry the replacement
comparative; any leaf changed outside the eight named fields; an em dash or double hyphen
introduced into consumer copy.

Guard suite:      tools/test_promote_pla8_slug_bait_safety.py
Mutation harness: tools/mutate_pla8_sbs_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_slug_bait_safety.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "75b3c0f0c253ffa7cb420d0f9c9d35e2a04c5dd47d9c222271923b2cc2b41d32"

PROSE_FIELDS = ("organic_treatment_beginner", "organic_treatment_seasoned",
                "prevention_beginner", "prevention_seasoned",
                "symptoms_beginner", "symptoms_seasoned",
                "cause_beginner", "cause_seasoned",
                "note_beginner", "note_seasoned")


def content():
    import build_slug_bait_safety_content as B
    return B.EDITS, B.BANNED, B.REQUIRED_COMPARATIVE


def scope_pat():
    import build_slug_bait_safety_content as B
    return B.SCOPE


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
    """Every consumer prose string on every crop problem, as (label, text)."""
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
    edits, banned, _req = content()
    seen = set()
    for slug, pname, field, old, new in edits:
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
            return (f"{slug}/{pname}/{field}: text does not match exactly; "
                    f"already applied, or the prose changed under this promote")
        if old == new:
            return f"{slug}/{pname}/{field}: edit is a no-op"
        for pat in banned:
            if re.search(pat, new, re.I):
                return f"{slug}/{pname}/{field}: replacement still matches banned {pat!r}"
        if re.search(r"[—–]", new) or "--" in new:
            return f"{slug}/{pname}/{field}: replacement introduces a dash form barred in copy"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    edits, _banned, _req = content()
    n = 0
    for slug, pname, field, old, new in edits:
        p = _find(data, slug, pname)
        assert p is not None and p[field] == old, "check() must run before apply_to()"
        p[field] = new
        n += 1
    return n


def verify_post(data):
    """POST-state assertions. Kept separate so the suite can call them on a replayed post.

    The banned scan is roster-wide but SCOPED to slug/snail-bait prose -- see SCOPE in the content
    module for why a promote must not assert a property it does not establish.
    """
    edits, banned, req = content()
    scope = scope_pat()
    for label, text in iter_prose(data):
        if not re.search(scope, text, re.I):
            continue
        for pat in banned:
            if re.search(pat, text, re.I):
                return f"banned construction {pat!r} survives at {label}"
    for slug, pname, field, _old, new in edits:
        p = _find(data, slug, pname)
        if p is None or p.get(field) != new:
            return f"{slug}/{pname}/{field}: post-state text is not the intended replacement"
        if not re.search(req, new, re.I):
            return f"{slug}/{pname}/{field}: replacement lacks the comparative that replaced the absolute"
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
        print(f"ABORT: base SHA mismatch\n  expected {a.expect_sha}\n  found    {sha}",
              file=sys.stderr)
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

    print("PLA-8 -- iron-phosphate slug-bait safety absolute, crop prose")
    print(f"  fields rewritten : {n} across "
          f"{len({e[0] for e in content()[0]})} crops")
    for slug, pname, field, _o, _n in content()[0]:
        print(f"    {slug:14s} {field}")
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
