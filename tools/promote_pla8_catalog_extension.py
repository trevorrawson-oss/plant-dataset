#!/usr/bin/env python3
"""PLA-8: extend the control-method catalog ahead of the ladder rollout. Base 98ea96c4.

SPEC + FULL PROVENANCE: docs/2026-08-22-control-method-catalog-extension-spec.md.
CONTENT: tools/build_catalog_extension_content.py (the authored entries and their anchors).

WHAT THIS CHANGES, AND WHAT IT POINTEDLY DOES NOT. Two TOP-LEVEL tables grow: `control_methods`
37 -> 40 and `source_catalog` 209 -> 211, plus `applies_to` widens on four existing methods. **NO
CROP IS TOUCHED.** That is the inverse of this arc's previous promote, so the blast-radius guards run
the other way: they prove every crop leaf is byte-identical and that the only movement is inside the
two tables.

WHY. Measured against `TYPE_TARGETS`, `nematode` and `viral` are declared problem types that ZERO of
the 37 methods target, so a problem typed either way can only ever reach the four methods marked
`any`. That is not an abstraction: plant-app renders a ladder from whatever methods a problem
resolves to, so those types bottom out at four generic rungs and read to a grower as "we have almost
nothing to say about this." Five independent authoring bots hit the wall on five unrelated crops in
one afternoon, each reporting it unprompted:

  heirloom-tomato/spider mites  the crop's own prose names a water blast and consistent watering as
                                its PRIMARY controls; the catalog made both unauthorable.
  swiss-chard/slugs             night hand-picking, the entry's first-line treatment, was blocked.
  swiss-chard + fig/root-knot   the whole organic-matter and vigor program had no legal home.
  basil, jalapeno, tomato       soil drainage, named the core control in all three, had no method.

AFTER: nematode 4 -> 5, viral 10 -> 13, mite 22 -> 25, fungal 12 -> 14, bacterial 10 -> 12,
mollusk 6 -> 7.

SOURCING. Every claim is quoted from a document fetched and READ 2026-08-22. The three new methods
follow the house pattern verified against the existing 37 (bare `ucanr_ext`, already T1, with a
DOCUMENT-SPECIFIC `anchoring_urls` entry -- 30 of 37 do exactly this). The corrections ADD a
document-scoped sibling id rather than overwrite the existing URL, because `anchoring_urls` allows
one URL per source id and a widened method rests on a SECOND document; that is the PLA-253 rule,
add a source, never replace one. Both new ids are titled FROM the document per A54.

SOLARIZATION SHIPS CARRYING ITS OWN LIMITS. Two independent UC IPM notes bound it, and both bounds
are in `cons` rather than compressed away: it is "not always as effective against nematodes as it is
against fungal disease and weeds" because "nematodes are relatively mobile and can move deeper in
the soil profile to escape the heat", and the effect reaches "primarily in the top foot or so of the
soil, so they are effective only for about a year."

ONE SPEC'D CORRECTION WAS DROPPED AFTER CHECKING: `horticultural_oil` already carries `mite`. The
claim was true and the correction a no-op, and a no-op row in a corrections table reads as coverage
it does not provide.

REFUSALS (each a live path, exercised by the suite): base SHA mismatch; a method that already
exists; a source id that already exists; a correction naming a method that is absent; a correction
whose target is already present; an unknown tier; a source that is not T1.

Guard suite:      tools/test_promote_pla8_catalog_extension.py
Mutation harness: tools/mutate_pla8_catalog_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla8_catalog_extension.py [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")

BASE_SHA = "98ea96c446cbeed858efa56bbf5324a7dc2edd3e21bbe26bdaf4c51b90ac6aef"
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
VERIFIED = "2026-08-22"


def content():
    import build_catalog_extension_content as B
    return B.NEW_SOURCES, B.NEW_METHODS, B.CORRECTIONS


def check(data):
    """Every refusal, before a byte moves."""
    cm, sc = data["control_methods"], data["source_catalog"]
    new_sources, new_methods, corrections = content()
    for k in new_sources:
        if k in sc:
            return f"source_catalog.{k} already exists"
        if new_sources[k].get("tier") != "T1":
            return f"source_catalog.{k} is not T1"
    for k, m in new_methods.items():
        if k in cm:
            return f"control_methods.{k} already exists; this promote creates it"
        if m.get("tier") not in TIERS:
            return f"control_methods.{k}: tier {m.get('tier')!r} not in {list(TIERS)}"
        for s in m.get("sources", []):
            if s not in sc and s not in new_sources:
                return f"control_methods.{k}: source {s!r} not in source_catalog"
        if set(m.get("anchoring_urls") or {}) != set(m.get("sources") or []):
            return f"control_methods.{k}: anchoring_urls keys do not match sources"
    for k, (target, src) in corrections.items():
        if k not in cm:
            return f"control_methods.{k} missing; nothing to correct"
        if target in cm[k]["applies_to"]:
            return (f"control_methods.{k} already carries {target!r}; the correction is a no-op "
                    f"and a no-op reads as coverage it does not provide")
        if src not in new_sources and src not in sc:
            return f"control_methods.{k}: correction source {src!r} does not exist"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    new_sources, new_methods, corrections = content()
    data["source_catalog"].update(json.loads(json.dumps(new_sources)))
    data["control_methods"].update(json.loads(json.dumps(new_methods)))
    for k, (target, src) in corrections.items():
        m = data["control_methods"][k]
        m["applies_to"].append(target)
        if src not in m["sources"]:
            m["sources"].append(src)
            m["anchoring_urls"][src] = {"url": data["source_catalog"][src]["url"],
                                        "verified": VERIFIED}
    return len(new_methods), len(corrections)


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

    before_m, before_s = len(data["control_methods"]), len(data["source_catalog"])
    nm, nc = apply_to(data)
    print("PLA-8 -- control-method catalog extension")
    print(f"  control_methods {before_m} -> {len(data['control_methods'])}  (+{nm})")
    print(f"  source_catalog  {before_s} -> {len(data['source_catalog'])}  (+2)")
    print(f"  applies_to corrections: {nc}")

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
