#!/usr/bin/env python3
"""PLA-8 catalog round: mint `borer_stem_surgery`. Base 5696aead.

The content, the sourcing and the reasoning: tools/build_pla8_borer_method_content.py.

WHAT MOVES. One new key in `control_methods`, 50 -> 51. NO existing method is touched, NO crop, NO
source_catalog entry, NO ladder. Nothing points at the new method yet; batch 4's promote does that.

WHY IT IS A SEPARATE PROMOTE. Catalog rounds have been separate from batch promotes since batch 1
(b51bdbc, 0a89792, 49d6182), and a mint deserves its own guards: the method has to be sourced and
shaped correctly whether or not the batch that motivated it ever lands.

WHY THE METHOD EXISTS. Three authoring agents in batch 4 independently reported the squash vine
borer's stem surgery as unplaceable, two of them rejecting `handpick` by name and citing that
method's own con -- "Misses hidden eggs and tiny larvae". A larva inside a stem is the case
handpicking is documented to miss. It is the crop's only in-season remedy, so five ladders otherwise
carry no action for the treatment their own prose leads with.

REFUSALS: base SHA mismatch; the key already present; a missing required field; `applies_to` not
exactly ['insect_boring']; a source not in source_catalog or not T1; an anchoring_url missing for a
declared source; any existing method changed; any crop changed; a dropped source hedge; copy
hygiene.

Guard suite:      tools/test_promote_pla8_borer_method.py
Mutation harness: tools/mutate_pla8_borer_method_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_borer_method.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "5696aead08e2e197c06cec78824acf97feac8d8ff67043e82594b4b440b7f71e"

REQUIRED = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
            "best_use", "pros", "cons", "sources", "anchoring_urls")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def content():
    import build_pla8_borer_method_content as C
    return C


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
    if re.search(r"\b(?:is|are)\s+safe\b", s, re.I):
        return "bare safety claim"
    return None


def prose_of(m):
    out = []
    for f, v in m.items():
        if f in ("anchoring_urls", "sources", "applies_to", "tier"):
            continue
        out.extend(v if isinstance(v, list) else [v])
    return [s for s in out if isinstance(s, str)]


def check(data):
    C = content()
    cm = data.get("control_methods") or {}
    if C.KEY in cm:
        return f"{C.KEY} is already in the catalog"

    m = C.METHOD
    for f in REQUIRED:
        if f not in m or not m[f]:
            return f"mint is missing required field {f!r}"
    if m["tier"] not in TIERS:
        return f"tier {m['tier']!r} is not one of {TIERS}"

    # NARROW ON PURPOSE. Widening this is what would turn it into a second handpick.
    if m["applies_to"] != ["insect_boring"]:
        return (f"applies_to must be exactly ['insect_boring']; a wider scope lets this method "
                f"attach to surface pests, which is the confusion it exists to resolve")

    sc = data.get("source_catalog") or {}
    for s in m["sources"]:
        if s not in sc:
            return f"source {s!r} is not in source_catalog"
        if (sc[s].get("tier") or "").upper() != "T1":
            return f"source {s!r} is not T1"
        if s not in m["anchoring_urls"]:
            return f"source {s!r} has no anchoring_url"
    for s, a in m["anchoring_urls"].items():
        if s not in m["sources"]:
            return f"anchoring_url {s!r} is not a declared source"
        if not str(a.get("url", "")).startswith("https://"):
            return f"anchoring_url {s!r} is not https"
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a.get("verified", ""))):
            return f"anchoring_url {s!r} has no valid verified date"

    blob = " ".join(prose_of(m)).lower()
    for hedge in ("may not", "not always", "sometimes"):
        if hedge in blob:
            break
    else:
        return "the prose carries no hedge, but BOTH sources qualify this method's success"
    if "july or early august" not in blob:
        return "the stated seasonal window from the ISU source is missing from the prose"
    for s in prose_of(m):
        bad = hygiene(s)
        if bad:
            return f"prose fails copy hygiene ({bad}): {s[:60]!r}"
    return None


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    return content().apply_mint(data["control_methods"])


def verify_post(data):
    C = content()
    cm = data["control_methods"]
    if C.KEY not in cm:
        return "post: the method was not minted"
    if cm[C.KEY]["applies_to"] != ["insect_boring"]:
        return "post: applies_to is not the narrow scope"
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
    before = len(data["control_methods"])
    apply_to(data)
    problem = verify_post(data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    C = content()
    print("PLA-8 catalog round -- mint borer_stem_surgery")
    print(f"  catalog      : {before} -> {len(data['control_methods'])}")
    print(f"  applies_to   : {C.METHOD['applies_to']}  (narrow on purpose)")
    print(f"  sources      : {', '.join(C.METHOD['sources'])}  (both T1, both fetched and read)")
    print(f"  crops touched: 0   existing methods touched: 0")
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
