#!/usr/bin/env python3
"""PLA-8 catalog r3: mint prompt_harvest, sound_sowing_practice, augmentative_release,
resistant_rootstock. Base 6876840e.

Rationale, the source reads, and what was deliberately NOT minted:
tools/build_pla8_catalog_r3_content.py

WHAT MOVES. `control_methods` 45 -> 49. Nothing else: no existing method is edited, no crop is
touched, no source is minted. Every anchor is an already-catalogued T1 id.

EVERY ONE OF THESE FOUR WAS FIRST RECORDED AS "UNSOURCED" AND THEN FOUND AT T1. The crops were
citing the wrong documents. A fifth candidate, `pheromone_trap`, DISSOLVED under the same hunt: the
existing `yellow_sticky_traps` key turned out to be correct and the rung's pheromone clause is the
unsourced part.

REFUSALS: base SHA mismatch; a mint that already exists; a missing/empty required field; a bad tier;
a source absent from source_catalog or not T1; anchoring_urls not matching sources; a `best_use`
that does not name the neighbouring method it must be distinguished from; a mint whose applies_to
names a target no TYPE_TARGETS entry can reach.

Guard suite:      tools/test_promote_pla8_catalog_r3.py
Mutation harness: tools/mutate_pla8_cr3_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_catalog_r3.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "6876840ed629ca5a86f4052697426120b2c245d5895c1663e9b8722112f8e670"

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
REQ = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
       "best_use", "pros", "cons", "sources", "anchoring_urls")


def content():
    import build_pla8_catalog_r3_content as B
    return B


def check(data):
    B = content()
    cm, sc = data["control_methods"], data["source_catalog"]
    from control_ladder_gate import TYPE_TARGETS
    reachable = set().union(*TYPE_TARGETS.values())

    for k, m in B.NEW_METHODS.items():
        if k in cm:
            return f"control_methods.{k} already exists; this promote creates it"
        if m["tier"] not in TIERS:
            return f"{k}: bad tier {m['tier']!r}"
        for f in REQ:
            if not m.get(f):
                return f"{k}: missing/empty {f!r}"
        for t in m["applies_to"]:
            if t != "any" and t not in reachable:
                return f"{k}: applies_to {t!r} is not reachable from any problem type"
        for s in m["sources"]:
            if s not in sc:
                return f"{k}: source {s!r} not in source_catalog"
            if sc[s].get("tier") != "T1":
                return f"{k}: source {s!r} is not T1"
        if set(m["anchoring_urls"]) != set(m["sources"]):
            return f"{k}: anchoring_urls keys do not match sources"
        neighbour = B.DISAMBIGUATION.get(k)
        if not neighbour:
            return f"{k}: no disambiguation neighbour recorded"
        if neighbour.lower() not in m["best_use"].lower():
            return (f"{k}: best_use does not name {neighbour!r}; this catalog's defect class is a "
                    f"method meaning almost-but-not-quite what its neighbour means")
        key = neighbour.replace(" ", "_")
        if key not in cm:
            return f"{k}: disambiguation neighbour {key!r} is not in the catalog"

    covered = {r["for"] for r in B.SOURCE_READS}
    if covered != set(B.NEW_METHODS):
        return f"SOURCE_READS covers {sorted(covered)}, expected {sorted(B.NEW_METHODS)}"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    B = content()
    data["control_methods"].update(json.loads(json.dumps(B.NEW_METHODS)))
    return len(B.NEW_METHODS)


def verify_post(data):
    B = content()
    cm = data["control_methods"]
    for k in B.NEW_METHODS:
        if k not in cm:
            return f"{k} did not land"
    # the four neighbours must survive untouched -- this promote adds, it does not edit
    for neighbour in set(B.DISAMBIGUATION.values()):
        if neighbour.replace(" ", "_") not in cm:
            return f"neighbour {neighbour!r} vanished"
    if "starve or migrate" not in cm["augmentative_release"]["how_it_works_seasoned"].lower():
        return ("augmentative_release dropped UC IPM's caveat that released predators starve or "
                "migrate elsewhere without prey; without it the method oversells a bought control")
    if "density" not in cm["sound_sowing_practice"]["best_use"].lower():
        return "sound_sowing_practice does not distinguish itself from seeding DENSITY"
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
    n = apply_to(data)

    problem = verify_post(data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    B = content()
    print("PLA-8 catalog r3 -- four mints, each anchored to a T1 document fetched and read")
    print(f"  control_methods {before} -> {len(data['control_methods'])}  (+{n})")
    for k in B.NEW_METHODS:
        print(f"    {k:24s} tier={B.NEW_METHODS[k]['tier']:11s} "
              f"vs {B.DISAMBIGUATION[k]}")
    print(f"  NOT minted: {', '.join(sorted(B.NOT_MINTED))}")
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
