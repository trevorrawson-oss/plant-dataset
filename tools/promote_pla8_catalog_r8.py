#!/usr/bin/env python3
"""PLA-8 catalog round 8: mint 2 methods, mint NO source, and DEFER one candidate. Base 919eabc4.

The content, the sourcing, the verbatim quotes and the adjudications: build_pla8_catalog_r8_content.

WHAT MOVES. `control_methods` 62 -> 64 (`cure_and_store`, `lower_soil_ph`). NO existing method is
touched, NO source is added or changed, NO crop, NO ladder.

WHY THIS ROUND RUNS BEFORE THE ROOTS BATCH. Both mints were found by measuring the roots crops'
prose against the catalog BEFORE authoring, which is the r5/r7 method. Batch 1's documented defect
was being authored against a 37-method catalog that grew to 43 underneath it, and `ladder_batch
prepare` regenerates its brief FROM CANONICAL, so minting mid-batch reproduces exactly that.

WHY A GUARD FOR A PAIR RATHER THAN FOR A REFUSAL. r7 guarded something it did NOT do. This round's
hazard is different and it is live in the catalog already: `raise_soil_ph` exists, is named "Raise
soil pH (liming)", is for clubroot, and points the OPPOSITE WAY from what potato scab needs. An
author reaching for the nearest-sounding key would encode advice that makes scab worse -- the
`bottom_watering` failure mode, except the wrong method is already sitting there.

So `opposed_pair_holds` asserts the two are and stay DISJOINT: no problem type may ever be legal on
both, and the new method's own prose must keep naming its opposite. If a later round widens either
one into the other's territory, this refuses rather than letting the catalog hold two methods that
tell the same problem to do contradictory things.

WHAT IS NOT GUARDED, DELIBERATELY. In-season mounding over stems and crowns was measured at 5
problems / 5 crops and DEFERRED, not refused, because reading splits it into three mechanisms and
one of the three has no supporting document. A guard asserting "no mounding method exists" would
have to be retired by the very round that adds it, and would read as a ruling against a method this
round thinks is probably admissible. The content module's record is the guard there.

THIS ROUND MINTS NO SOURCES, and that is asserted rather than assumed: all six anchors are already
T1 entries in `source_catalog`. `check` refuses if `NEW_SOURCES` is ever non-empty without the
source-mint validation being reached, so the empty case cannot go vacuous.

REFUSALS: base SHA mismatch; a mint key already present; a missing required field; an unknown tier;
an `applies_to` value outside the gate vocabulary; a source not in source_catalog or not T1; a
declared source with no anchoring_url; an anchoring_url that is not https or has no verified date;
an anchoring_url for an undeclared source; a dropped source hedge; the opposed pair sharing a
target or losing its cross-reference; copy hygiene; and post-state blast radius on methods, sources
and every crop.

Guard suite:      tools/test_promote_pla8_catalog_r8.py
Mutation harness: tools/mutate_pla8_catalog_r8_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_catalog_r8.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "919eabc4d2dae936e3f5b876c52799f5a3a3e3d1983c2c8ac324384ab986c073"

REQUIRED = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
            "best_use", "pros", "cons", "sources", "anchoring_urls")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")
EXPECTED_MINTS = 2
EXPECTED_NEW_SOURCES = 0


def content():
    import build_pla8_catalog_r8_content as C
    return C


def gate_vocabulary():
    from control_ladder_gate import TYPE_TARGETS, UNIVERSAL_TARGET
    v = {UNIVERSAL_TARGET}
    for targets in TYPE_TARGETS.values():
        v |= set(targets)
    return v


def hygiene(s):
    if re.search(r"[—–]", s):
        return "em or en dash"
    if "--" in s:
        return "double hyphen"
    if re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I):
        return "absolute claim"
    if re.search(r"\s°F", s):
        return "spaced degF"
    if re.search(r"\d+\s*F\b", s):
        return "bare F without a degree sign"
    if "**" in s or "__" in s:
        return "markdown emphasis"
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


def _check_sources(m, key, sc, new_sources):
    known = dict(sc)
    known.update(new_sources)
    for s in m["sources"]:
        if s not in known:
            return f"{key}: source {s!r} is not in source_catalog"
        if (known[s].get("tier") or "").upper() != "T1":
            return f"{key}: source {s!r} is not T1"
        if s not in m["anchoring_urls"]:
            return f"{key}: source {s!r} has no anchoring_url"
    for s, a in m["anchoring_urls"].items():
        if s not in m["sources"]:
            return f"{key}: anchoring_url {s!r} is not a declared source"
        if not str(a.get("url", "")).startswith("https://"):
            return f"{key}: anchoring_url {s!r} is not https"
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a.get("verified", ""))):
            return f"{key}: anchoring_url {s!r} has no valid verified date"
    return None


def opposed_pair_holds(cm):
    """THE HAZARD, ASSERTED. `lower_soil_ph` and `raise_soil_ph` are named alike and point in
    opposite directions: one holds a potato bed acid against common scab, the other limes a
    brassica bed against clubroot. They must never both be legal on one problem, and the new
    method's prose must keep saying so, or an author picking by name encodes the inverse advice."""
    C = content()
    new, old = C.OPPOSED_PAIR
    for k in (new, old):
        if k not in cm:
            return f"{k} is not in the catalog, so the opposed pair cannot be checked"
    a = set(cm[new].get("applies_to") or [])
    b = set(cm[old].get("applies_to") or [])
    if not a or not b:
        return f"the opposed pair has an empty applies_to ({new}={sorted(a)}, {old}={sorted(b)}), "\
               f"so disjointness would be vacuously true"
    shared = sorted(a & b)
    if shared:
        return (f"{new} and {old} now share the target(s) {shared}. They move soil pH in OPPOSITE "
                f"directions, so a problem legal on both would be told to do contradictory things; "
                f"widening either one into the other's territory needs a document and a ruling")
    blob = " ".join(prose_of(cm[new])).lower()
    if "opposite" not in blob:
        return (f"{new} no longer names its opposite in prose. The cross-reference is the guard "
                f"against an author picking the wrong one of two similarly named methods")
    return None


def check(data):
    C = content()
    cm = data.get("control_methods") or {}
    sc = data.get("source_catalog") or {}
    vocab = gate_vocabulary()

    if len(C.MINTS) != EXPECTED_MINTS:
        return f"this round mints {len(C.MINTS)} methods, expected {EXPECTED_MINTS}"
    if len(C.NEW_SOURCES) != EXPECTED_NEW_SOURCES:
        return (f"this round mints {len(C.NEW_SOURCES)} sources, expected {EXPECTED_NEW_SOURCES}; "
                f"if that is intended, the source-mint validation below must be extended rather "
                f"than left to pass on an empty dict")

    for key, m in C.MINTS.items():
        if key in cm:
            return f"{key} is already in the catalog"
        for f in REQUIRED:
            if f not in m or not m[f]:
                return f"{key}: mint is missing required field {f!r}"
        if m["tier"] not in TIERS:
            return f"{key}: tier {m['tier']!r} is not one of {TIERS}"
        bad = [t for t in m["applies_to"] if t not in vocab]
        if bad:
            return (f"{key}: applies_to {bad} is outside the gate vocabulary, so no problem could "
                    f"ever reach this method")
        err = _check_sources(m, key, sc, C.NEW_SOURCES)
        if err:
            return err

    from source_catalog_title_gate import LEGACY_UNFILLED, _doc_scoped
    for sid, entry in C.NEW_SOURCES.items():
        if sid in sc:
            return f"source id {sid!r} is already in source_catalog"
        if (entry.get("tier") or "").upper() != "T1":
            return f"source {sid!r} is not T1"
        if sid in LEGACY_UNFILLED:
            return (f"source {sid!r} claims the frozen A54 exemption; that list is shrink-only and "
                    f"a new mint is never exempt")
        if _doc_scoped(entry) and not str(entry.get("title") or "").strip():
            return f"source {sid!r} is document-scoped and carries no title (A54)"
        if not _doc_scoped(entry) and entry.get("title"):
            return f"source {sid!r} is an institution root and must not carry a title (A54)"

    for key, hedges in C.REQUIRED_HEDGES.items():
        if key not in C.MINTS:
            return f"REQUIRED_HEDGES names {key!r}, which this round does not mint"
        blob = " ".join(prose_of(C.MINTS[key])).lower()
        for h in hedges:
            if h.lower() not in blob:
                return f"{key}: the source qualifier {h!r} is missing from the prose"

    for key, m in C.MINTS.items():
        for s in prose_of(m):
            bad = hygiene(s)
            if bad:
                return f"{key}: prose fails copy hygiene ({bad}): {s[:70]!r}"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"methods": {k: dump(v) for k, v in data["control_methods"].items()},
            "sources": {k: dump(v) for k, v in data["source_catalog"].items()},
            "crops": dump(data["crops"])}


def apply_to(data):
    return content().apply_round(data)


def verify_post(pre, data):
    C = content()
    cm = data["control_methods"]
    post = snapshot(data)

    # SET EQUALITY BEFORE VALUE COMPARISON (PLA-162), both dicts, both directions.
    added_m = set(post["methods"]) - set(pre["methods"])
    if added_m != set(C.MINTS):
        return f"post: methods added {sorted(added_m)}, expected exactly {sorted(C.MINTS)}"
    if set(pre["methods"]) - set(post["methods"]):
        return f"post: methods dropped {sorted(set(pre['methods']) - set(post['methods']))}"
    added_s = set(post["sources"]) - set(pre["sources"])
    if added_s != set(C.NEW_SOURCES):
        return f"post: sources added {sorted(added_s)}, expected exactly {sorted(C.NEW_SOURCES)}"
    if set(pre["sources"]) - set(post["sources"]):
        return f"post: sources dropped {sorted(set(pre['sources']) - set(post['sources']))}"

    # THE SUBSTANTIVE INVARIANT RUNS BEFORE THE BLAST-RADIUS COMPARISON, and the ordering is
    # load-bearing, exactly as in r7: widening `raise_soil_ph` into `bacterial` IS a change to an
    # existing method, so below the bystander loop this guard could never fire on that half of the
    # pair. The opposition is the claim; blast radius is bookkeeping.
    problem = opposed_pair_holds(cm)
    if problem:
        return "post: " + problem

    for k, before in pre["methods"].items():
        if post["methods"][k] != before:
            return f"post: existing method {k!r} changed, and this round mints only"
    for k, before in pre["sources"].items():
        if post["sources"][k] != before:
            return f"post: existing source {k!r} changed"
    if post["crops"] != pre["crops"]:
        return "post: a crop changed, and this promote touches no crop"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    expect = a.expect_sha or BASE_SHA
    if sha != expect:
        raise SystemExit("REFUSED: base SHA %s != expected %s" % (sha[:16], expect[:16]))

    data = json.loads(raw.decode("utf-8"))
    problem = check(data)
    if problem:
        raise SystemExit("REFUSED: " + problem)

    pre = snapshot(data)
    before_cm, before_sc = len(data["control_methods"]), len(data["source_catalog"])
    summary = apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        raise SystemExit("REFUSED: " + problem)

    blob = serialize(data)
    print("minted methods    : %s" % ", ".join(summary["minted"]))
    print("minted sources    : %s" % (", ".join(summary["sources"]) or "(none)"))
    print("control_methods   : %d -> %d" % (before_cm, len(data["control_methods"])))
    print("source_catalog    : %d -> %d" % (before_sc, len(data["source_catalog"])))
    print("base  SHA         : %s" % sha)
    print("post  SHA         : %s" % hashlib.sha256(blob).hexdigest())
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
