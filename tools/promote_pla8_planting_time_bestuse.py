#!/usr/bin/env python3
"""PLA-8: close the single-generation criterion in planting_time_avoidance's best_use. Base 48478cb5.

ONE FIELD ON ONE METHOD. `control_methods.planting_time_avoidance.best_use`. No other field, no
other method, no source, no crop, no ladder. Catalog counts do not move.

THE METHOD SHEET CONTRADICTED ITSELF, AND IT SHIPPED THAT WAY THIS MORNING. `best_use` opened

    "A pest with one main generation and a published local emergence window..."

and closed, in the same sentence pair,

    "Squash vine borer and Mexican bean beetle are the documented cases."

Clemson's bean and southern pea insect factsheet -- the document this method cites for the Mexican
bean beetle case -- states: "From egg to adult requires about one month, and there are usually three
generations per year. During some years, there may be a partial fourth generation." So the criterion
excludes one of the two examples the same field names, and the document that would have settled it
was open when the field was written.

HOW IT WAS CAUGHT, AND BY WHAT. Not by a gate, not by the 67-test guard suite, and not by the
43-injection mutation harness -- all of them were green on that string, because every one of them
checks structure or checks that prose contains what the author said it should. It was caught by the
FIRST AUTHORING PASS TO USE THE METHOD. Reading `best_use` against the pest in front of it, the
green-beans-bush pass reported the key as a loose fit, "the generation-count half of the key's
definition does not describe this pest". The pole-beans pass reported the OPPOSITE, that the fit was
fine, citing the same sheet's `how_it_works_seasoned`, which names the beetle without any
generation claim. Two independent readers disagreeing about one method sheet, each correctly quoting
a different half of it, is the signature of a sheet that says two things.

WHAT THE MECHANISM ACTUALLY REQUIRES. Not one generation: a PREDICTABLE DAMAGE WINDOW. UMN's squash
vine borer has a single flight to get behind. Clemson's Mexican bean beetle has several generations
whose damage still concentrates in July and August, which is what makes an early or late sowing work.
The corrected field states both shapes rather than generalizing from the borer, which is what the
original did.

NO SOURCING CHANGES. Both anchors already on the method are the documents quoted here; this promote
adds no source and re-verifies no URL. `sources` and `anchoring_urls` are asserted byte-identical.

REFUSALS: base SHA mismatch; the old text absent (already corrected, or a different base); the new
text already present; any single-generation criterion surviving anywhere in the method's prose; the
corrected field failing to carry the multi-generation case; any other field of this method changed;
any other method changed; any source or crop changed; copy hygiene.

Guard suite:      tools/test_promote_pla8_planting_time_bestuse.py
Mutation harness: tools/mutate_pla8_planting_time_bestuse_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_planting_time_bestuse.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "48478cb5f62edd284674be3f16a7a08c2537d7d510c19c5e3d89517748c973b1"

KEY = "planting_time_avoidance"
FIELD = "best_use"

OLD = ("A pest with one main generation and a published local emergence window, on a crop quick "
       "enough to finish before it or start after it. Squash vine borer and Mexican bean beetle "
       "are the documented cases. Distinct from crop rotation, which moves the planting in space; "
       "this one moves it in time.")

NEW = ("A pest whose damage falls in a predictable, locally published stretch of the season, on a "
       "crop quick enough to finish before it or start after it. The two documented cases differ "
       "in shape: the squash vine borer has a single flight to get behind, while the Mexican bean "
       "beetle runs several generations a year whose damage still concentrates in July and August. "
       "Distinct from crop rotation, which moves the planting in space; this one moves it in time.")

# The defect class, stated as text this method's prose may never carry again. A criterion of this
# shape excludes one of the two cases the sheet itself names.
SINGLE_GEN_CRITERIA = (
    "one main generation",
    "a single generation",
    "one generation a year",
    "only one generation",
    "a single main generation",
)

# What the corrected field must actually say, so the fix cannot be satisfied by deletion alone.
MUST_CARRY = ("several generations", "july and august", "single flight")

BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def hygiene(s):
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
    return None


def prose_of(m):
    out = []
    for f, v in m.items():
        if f in ("anchoring_urls", "sources", "applies_to", "tier"):
            continue
        out.extend(v if isinstance(v, list) else [v])
    return [s for s in out if isinstance(s, str)]


def check(data):
    cm = data.get("control_methods") or {}
    if KEY not in cm:
        return f"{KEY} is not in the catalog"
    m = cm[KEY]
    if m.get(FIELD) != OLD:
        return (f"{KEY}.{FIELD} is not the text this correction was written against; the base is "
                f"not what it should be, or the field was already corrected")
    if NEW == OLD:
        return "the correction is a no-op"
    # NOTE: there is deliberately NO "already corrected" branch here. It would be unreachable --
    # a field equal to NEW is not equal to OLD, so the check above returns first. The mutation
    # harness proved it dead (the injection survived), and an unreachable guard reads as coverage
    # it does not provide, so it is removed rather than tested. Re-running this promote over its
    # own output is still refused, by the OLD check, and a test pins that.

    # The correction has to remove the criterion AND say the true thing, not just delete.
    low = NEW.lower()
    for bad in SINGLE_GEN_CRITERIA:
        if bad in low:
            return f"the replacement still carries a single-generation criterion ({bad!r})"
    for need in MUST_CARRY:
        if need not in low:
            return (f"the replacement drops {need!r}; the fix must state what the mechanism really "
                    f"requires, not merely delete the wrong criterion")
    bad = hygiene(NEW)
    if bad:
        return f"the replacement fails copy hygiene ({bad})"

    # Nothing ELSE on this sheet may carry the criterion either -- deleting it from one field while
    # it survives in another leaves the contradiction live.
    others = " ".join(s for f, v in m.items() if f != FIELD
                      for s in (v if isinstance(v, list) else [v]) if isinstance(s, str)).lower()
    for bad in SINGLE_GEN_CRITERIA:
        if bad in others:
            return f"another field of {KEY} still carries {bad!r}"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"methods": {k: dump(v) for k, v in data["control_methods"].items()},
            "sources": dump(data["source_catalog"]),
            "crops": dump(data["crops"])}


def apply_to(data):
    data["control_methods"][KEY][FIELD] = NEW
    return 1


def verify_post(pre, data):
    post = snapshot(data)
    # Set equality before value comparison, both directions (PLA-162).
    if set(post["methods"]) != set(pre["methods"]):
        return (f"post: the method set changed "
                f"(+{sorted(set(post['methods']) - set(pre['methods']))} "
                f"-{sorted(set(pre['methods']) - set(post['methods']))})")
    for k, before in pre["methods"].items():
        if k == KEY:
            continue
        if post["methods"][k] != before:
            return f"post: untouched method {k!r} changed"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote touches no source"
    if post["crops"] != pre["crops"]:
        return "post: a crop changed, and this promote touches no crop"

    m = data["control_methods"][KEY]
    before = json.loads(pre["methods"][KEY])

    # THE SUBSTANTIVE INVARIANT RUNS FIRST, and that ordering is load-bearing. Below the per-field
    # comparison this scan was unreachable -- every post state that could carry a criterion also
    # trips a field comparison, so the harness reported it as a surviving mutation. First line, not
    # second line: it now answers for the contradiction before blast radius answers for anything.
    low = " ".join(prose_of(m)).lower()
    for bad in SINGLE_GEN_CRITERIA:
        if bad in low:
            return f"post: {KEY} still carries {bad!r}"

    if m[FIELD] != NEW:
        return f"post: {FIELD} did not land"
    for f, v in before.items():
        if f == FIELD:
            continue
        if m.get(f) != v:
            return f"post: {KEY}.{f!r} changed, and only {FIELD} may move"
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

    pre = snapshot(data)
    apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print("PLA-8 -- close the single-generation criterion in planting_time_avoidance.best_use")
    print(f"  method   : {KEY}.{FIELD}   (1 field, 1 method)")
    print(f"  catalog  : {len(data['control_methods'])} methods, unchanged")
    print(f"  crops    : 0 touched   sources: 0 touched   other methods: 0 touched")
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
