#!/usr/bin/env python3
"""PLA-8: `bottom_watering` gains `bacterial` and `mollusk`. Base d04b868c.

TWO applies_to corrections on ONE existing method, plus one new T1 source. No new method, no crop
touched, nothing removed.

WHY THIS IS SMALL. The re-run of the 5-crop pilot surfaced NINE blocked controls, and an earlier
draft of this work proposed widening all nine on the grounds that they were "the same defect shape".
They are not, and blanket-widening would have been the never-blanket-a-reason error. Graded:

  SHIPPED HERE (2) -- the method's own mechanism genuinely covers the type, and a T1 document says so
    bottom_watering + bacterial   splash dispersal is how bacterial spot/speck moves
    bottom_watering + mollusk     irrigation practice is a named mollusk control

  NOT SHIPPED, UNSOURCED (2) -- plausible, no anchor found; the UC IPM blossom-end-rot page returns
    a stub, so straw_mulch + physiological and balance_nitrogen + physiological stay blocked until a
    document is read. Owed, not abandoned.

  REFUSED (5) -- these ask the ladder to say "keep the plant healthy" where a rung means "do this to
    the problem". even_watering + insect, straw_mulch + nematode, even_watering + nematode and
    airflow_spacing + insect are all TOLERANCE, not control. And beneficial_predators + viral is the
    map being RIGHT: predators control the vector, not the virus, and that rung belongs on the aphid
    entry, which is where the authoring pass had already put it.

SOURCES, fetched and read 2026-08-23:
  bacterial -- UC IPM, Bacterial Speck (Tomato): "The pathogen is spread by splashing rain or
    sprinkler irrigation." and "When the disease appears, change from overhead to furrow irrigation."
  mollusk   -- UC IPM Pest Notes 7427, Snails and Slugs (already catalogued as
    `ucanr_ext_snails_slugs` by the previous promote): "Switching from sprinkler irrigation to drip
    irrigation will reduce humidity and moist surfaces, making the habitat less favorable for these
    pests. Irrigating near sunrise will reduce the amount of time that foliage and ground are moist."

A WIDENING CANNOT REDDEN ANYTHING: it only enlarges the set of methods the gate ACCEPTS for a type.
The risk here is not breakage, it is authoring a rung the biology does not support, which is why the
grading above matters more than the diff.

Guard suite:      tools/test_promote_pla8_bottom_watering_targets.py
Mutation harness: tools/mutate_pla8_bw_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla8_bottom_watering_targets.py [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "d04b868c94e45aa7c08dd4de7768040c0462b268f2e9c99eddaf9e6e75beef17"
METHOD = "bottom_watering"
VERIFIED = "2026-08-23"

NEW_SOURCE = {
    "ucanr_ext_bacterial_speck": {
        "id": "ucanr_ext_bacterial_speck",
        "name": "UC IPM -- Bacterial Speck (Tomato)",
        "title": "Bacterial Speck / Tomato / Agriculture: Pest Management Guidelines / UC Statewide "
                 "IPM Program (UC IPM)",
        "publisher": "UC ANR",
        "url": "https://ipm.ucanr.edu/agriculture/tomato/bacterial-speck/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-08",
        "tier": "T1",
        "citable_for": (
            "UC IPM tomato bacterial speck guidelines. Cited for irrigation practice as a BACTERIAL "
            "disease control: 'The pathogen is spread by splashing rain or sprinkler irrigation' and "
            "'When the disease appears, change from overhead to furrow irrigation.'"
        ),
        "_admission_provenance": (
            "Minted 2026-08-23 (PLA-8). `bottom_watering` was fungal_soilborne/insect_general only, "
            "so a jalapeno authoring pass could not place 'water at the soil to keep foliage dry' on "
            "bacterial spot even though the crop's own prose names it a primary control. Two "
            "independent authoring passes reported the same block. Document fetched (31,788 bytes) "
            "and read before pinning."
        ),
    }
}

# target -> the source id that anchors it
ADD_TARGETS = {"bacterial": "ucanr_ext_bacterial_speck", "mollusk": "ucanr_ext_snails_slugs"}


def check(data):
    cm, sc = data["control_methods"], data["source_catalog"]
    if METHOD not in cm:
        return f"control_methods.{METHOD} missing; nothing to correct"
    for k, e in NEW_SOURCE.items():
        if k in sc:
            return f"source_catalog.{k} already exists"
        if e.get("tier") != "T1":
            return f"source_catalog.{k} is not T1"
    for target, src in ADD_TARGETS.items():
        if target in cm[METHOD]["applies_to"]:
            return (f"{METHOD} already carries {target!r}; the correction is a no-op and a no-op "
                    f"reads as coverage it does not provide")
        if src not in sc and src not in NEW_SOURCE:
            return f"anchor source {src!r} does not exist"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    data["source_catalog"].update(json.loads(json.dumps(NEW_SOURCE)))
    m = data["control_methods"][METHOD]
    for target, src in ADD_TARGETS.items():
        m["applies_to"].append(target)
        if src not in m["sources"]:
            m["sources"].append(src)
            m["anchoring_urls"][src] = {"url": data["source_catalog"][src]["url"],
                                        "verified": VERIFIED}
    return len(ADD_TARGETS)


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

    before = list(data["control_methods"][METHOD]["applies_to"])
    n = apply_to(data)
    print(f"PLA-8 -- {METHOD} applies_to correction")
    print(f"  {before}  ->  {data['control_methods'][METHOD]['applies_to']}")
    print(f"  source_catalog +1 ({', '.join(NEW_SOURCE)})")
    print(f"  targets added: {n}")

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
