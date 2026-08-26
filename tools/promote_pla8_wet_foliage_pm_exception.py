#!/usr/bin/env python3
"""PLA-8: name the powdery-mildew exception on wet_foliage_discipline. Base 4a239eef.

ONE METHOD. `control_methods.wet_foliage_discipline` gains one `cautions` entry, one source and one
anchoring_url. No other method, no crop, no ladder. Catalog counts do not move.

WHY. The method's own mechanism is free-water transport: "Free moisture on the leaf surface is the
transport medium for splash-dispersed bacteria and for many foliar fungi." Powdery mildew is not one
of them, and USU states it directly:

    "In contrast to many fungi, powdery mildews do not spread in rain or free water. For infection,
     powdery mildews only need high humidity or dew for a few hours."

`applies_to` includes `fungal_foliar`, which is CORRECT for the splash-dispersed foliar fungi the
method exists for -- Ascochyta blight, anthracnose, the leaf spots. It cannot express "except
powdery mildew", so the exception has to be stated in prose the authoring pass reads.

HOW IT SURFACED, AND IT IS THE BATCH-1 DEFECT CLASS AGAIN. Both batch-6 authoring passes put a
`wet_foliage_discipline` rung on the peas' powdery mildew, and BOTH flagged the underlying record as
self-contradictory without being asked: `cause_seasoned` says the fungus is "favored by warm days,
cool nights, and dry foliage" and that "Spores spread on the wind", while `prevention_seasoned` says
to "avoid working among wet vines". Both wrote the rung with NO mechanism stated, because neither
could restate a mechanism the entry undercuts. That refusal to invent is what surfaced it. The rung
was dropped from both ladders in the batch-6 read.

THE CONTRAST THAT SETTLES THE SCOPE: `airflow_spacing` names powdery mildew in its own `best_use`
("the same room helps against gray mold, powdery mildew and damping-off"), and humidity rather than
free water is what it acts on. One method is sanctioned for this pathogen by its own sheet; this one
is not. `wet_foliage_discipline` KEEPS its ascochyta use on the same crops, where the entry's own
cause says "Cool, wet weather and splashing water spread them".

BLAST RADIUS TODAY IS ZERO AND THAT IS THE POINT OF DOING IT NOW. The method is used on exactly
three problems, all bacterial blights on the beans, all correct. But 37 crops carry a powdery mildew
entry and 21 of them carry wet-handling advice, so this is a trap sitting in front of every one of
the 19 remaining batches rather than a live defect.

IT GOES IN `cautions` BECAUSE `cautions` CAN NOW BE READ. Until `603f4f8` the authoring brief
emitted only `applies_to` and a 150-character slice of `best_use`; 41 caution strings across 29
methods reached the brief nowhere. A caution added before that commit would have read as protection
while doing nothing. A test here asserts this one actually reaches a generated brief.

OVER-CORRECTION IS GUARDED. The tempting stronger fix is to drop `fungal_foliar` from `applies_to`,
which would break the legitimate ascochyta and anthracnose uses this method was minted for. `check`
and `verify_post` both refuse any change to `applies_to`.

REFUSALS: base SHA mismatch; the caution already present; the exception failing to name powdery
mildew; the USU mechanism missing; `applies_to` changed in either direction; the existing caution
dropped; an overwritten anchor; a source not in source_catalog or not T1; any other field, method,
source or crop changed; copy hygiene.

Guard suite:      tools/test_promote_pla8_wet_foliage_pm_exception.py
Mutation harness: tools/mutate_pla8_wet_foliage_pm_exception_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_wet_foliage_pm_exception.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "4a239eefe1d8627b029dc93e9cc5a990078e377eea0a4c8457dcbafe560002a4"

KEY = "wet_foliage_discipline"
SOURCE = "usu_ext"
SOURCE_URL = "https://extension.usu.edu/vegetableguide/legumes/powdery-mildew"
VERIFIED = "2026-08-26"

CAUTION = ("Powdery mildew is the exception and this does not act on it: USU notes that powdery "
           "mildews do not spread in rain or free water, needing only high humidity or dew for a "
           "few hours, so on that one disease it is airflow and spacing that do the work here, not "
           "staying out of a wet planting.")

# What the caution must actually say, so it cannot be satisfied by a vaguer sentence.
MUST_CARRY = ("powdery mildew", "free water", "airflow")

# The over-correction this promote must not make. Narrowing applies_to would break the ascochyta and
# anthracnose uses the method was minted for.
FROZEN_APPLIES_TO = ["bacterial", "fungal_foliar"]

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


def applies_to_frozen(cm):
    """THE OVER-CORRECTION GUARD. Dropping fungal_foliar would 'fix' powdery mildew by breaking
    ascochyta and anthracnose, which is what this method exists for."""
    if KEY not in cm:
        return f"{KEY} is not in the catalog"
    if list(cm[KEY].get("applies_to") or []) != FROZEN_APPLIES_TO:
        return (f"{KEY}.applies_to is {cm[KEY].get('applies_to')}, expected {FROZEN_APPLIES_TO}. "
                f"This promote states an exception in PROSE and must not narrow the target: "
                f"fungal_foliar is correct for the splash-dispersed foliar fungi the method was "
                f"minted for, and removing it would break ascochyta and anthracnose")
    return None


def check(data):
    cm = data.get("control_methods") or {}
    sc = data.get("source_catalog") or {}
    if KEY not in cm:
        return f"{KEY} is not in the catalog"
    m = cm[KEY]

    problem = applies_to_frozen(cm)
    if problem:
        return problem

    existing = list(m.get("cautions") or [])
    if not existing:
        return f"{KEY} has no cautions to append to; the base is not what this was written against"
    if CAUTION in existing:
        return f"{KEY} already carries this caution"

    low = CAUTION.lower()
    for need in MUST_CARRY:
        if need not in low:
            return (f"the caution does not mention {need!r}; it must name the pathogen it excepts, "
                    f"the mechanism that does not apply, and what does the work instead")
    bad = hygiene(CAUTION)
    if bad:
        return f"the caution fails copy hygiene ({bad})"

    if SOURCE not in sc:
        return f"source {SOURCE!r} is not in source_catalog"
    if (sc[SOURCE].get("tier") or "").upper() != "T1":
        return f"source {SOURCE!r} is not T1"
    if SOURCE in (m.get("anchoring_urls") or {}):
        return (f"{KEY}.anchoring_urls already carries {SOURCE!r}; anchoring_urls allows one URL "
                f"per source id and this must ADD, never overwrite")
    if not SOURCE_URL.startswith("https://"):
        return "the anchoring url is not https"
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
    m = data["control_methods"][KEY]
    m["cautions"] = list(m["cautions"]) + [CAUTION]
    if SOURCE not in m["sources"]:
        m["sources"] = list(m["sources"]) + [SOURCE]
    anchors = dict(m["anchoring_urls"])
    if SOURCE in anchors:
        raise AssertionError(f"{KEY}: anchoring_urls already has {SOURCE}; this must ADD")
    anchors[SOURCE] = {"url": SOURCE_URL, "verified": VERIFIED}
    m["anchoring_urls"] = anchors
    return 1


def verify_post(pre, data):
    cm = data["control_methods"]
    post = snapshot(data)

    # THE SUBSTANTIVE INVARIANTS RUN FIRST. Below the bystander loop they would be unreachable,
    # because any change to this method IS a change to an existing method. Third time in this arc.
    problem = applies_to_frozen(cm)
    if problem:
        return "post: " + problem
    m = cm[KEY]
    if CAUTION not in (m.get("cautions") or []):
        return "post: the caution did not land"
    before = json.loads(pre["methods"][KEY])
    for c in before.get("cautions") or []:
        if c not in m["cautions"]:
            return "post: an existing caution was dropped; this promote APPENDS"
    for sid, a in (before.get("anchoring_urls") or {}).items():
        if m["anchoring_urls"].get(sid) != a:
            return f"post: an existing anchoring_url ({sid}) was overwritten"
    for f, v in before.items():
        if f in ("cautions", "sources", "anchoring_urls"):
            continue
        if m.get(f) != v:
            return f"post: {KEY}.{f!r} changed, and only cautions/sources/anchoring_urls may move"

    if set(post["methods"]) != set(pre["methods"]):
        return "post: the method set changed"
    for k, b in pre["methods"].items():
        if k == KEY:
            continue
        if post["methods"][k] != b:
            return f"post: untouched method {k!r} changed"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote mints no source"
    if post["crops"] != pre["crops"]:
        return "post: a crop changed, and this promote touches no crop"
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

    print(f"PLA-8 -- name the powdery-mildew exception on {KEY}")
    print(f"  method     : {KEY}   (+1 caution, +1 source, +1 anchor)")
    print(f"  applies_to : {FROZEN_APPLIES_TO}  (FROZEN; narrowing would break ascochyta)")
    print(f"  catalog    : {len(data['control_methods'])} methods, unchanged")
    print(f"  crops      : 0 touched   other methods: 0 touched   source_catalog: 0 touched")
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
