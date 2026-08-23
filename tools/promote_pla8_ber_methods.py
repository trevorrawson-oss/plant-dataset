#!/usr/bin/env python3
"""PLA-8: two new methods for calcium-movement disorders. Base d19abe60.

Adds `moisture_buffering_mulch` and `avoid_ammoniacal_nitrogen` (both cultural, both
`physiological`), anchored to Clemson HGIC's Blossom End Rot section -- already catalogued T1,
already anchoring 5 methods, so NO new source id is minted.

WHY NEW METHODS RATHER THAN WIDENING TWO EXISTING ONES. Ruled with Trevor 2026-08-23. The controls
were first proposed as `applies_to` widenings on `balance_nitrogen` and `straw_mulch`. The biology
checked out and the widening was still wrong: `applies_to` governs what the GATE accepts and does
nothing to the PROSE. balance_nitrogen's copy is about sappy growth and aphids; BER's mechanism is
ammonium COMPETING WITH CALCIUM UPTAKE. straw_mulch's copy is about keeping strawberries off wet
soil. Either would have produced a rung that gates clean and reads as a non-sequitur -- the same
class of defect as prose that passes every structural check and is still false.

Rationale, sources and the not-duplicating-even_watering argument: tools/build_ber_methods_content.py

Guard suite:      tools/test_promote_pla8_ber_methods.py
Mutation harness: tools/mutate_pla8_ber_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_ber_methods.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "d19abe601ab6c67dbf4037f982307ec26a73f921f70334187dc1ed7fd97954f8"
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
REQ = ("name","tier","applies_to","how_it_works_beginner","how_it_works_seasoned","best_use",
       "pros","cons","sources","anchoring_urls")

def content():
    import build_ber_methods_content as B
    return B.NEW_METHODS

def check(data):
    cm, sc = data["control_methods"], data["source_catalog"]
    for k, m in content().items():
        if k in cm:
            return f"control_methods.{k} already exists; this promote creates it"
        if m.get("tier") not in TIERS:
            return f"{k}: tier {m.get('tier')!r} not in {list(TIERS)}"
        for f in REQ:
            if not m.get(f):
                return f"{k}: missing/empty required key {f!r}"
        for s in m["sources"]:
            if s not in sc:
                return f"{k}: source {s!r} not in source_catalog"
            if sc[s].get("tier") != "T1":
                return f"{k}: source {s!r} is not T1"
        if set(m["anchoring_urls"]) != set(m["sources"]):
            return f"{k}: anchoring_urls keys do not match sources"
    return None

def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def apply_to(data):
    data["control_methods"].update(json.loads(json.dumps(content())))
    return len(content())

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
        print(f"ABORT: base SHA mismatch\n  expected {a.expect_sha}\n  found    {sha}", file=sys.stderr); return 1
    data = json.loads(raw.decode("utf-8"))
    p = check(data)
    if p:
        print("ABORT: " + p, file=sys.stderr); return 1
    before = len(data["control_methods"])
    n = apply_to(data)
    print(f"PLA-8 -- calcium-disorder methods\n  control_methods {before} -> {len(data['control_methods'])}  (+{n})")
    for k in content(): print(f"    {k}")
    out = serialize(data); new_sha = hashlib.sha256(out).hexdigest()
    if a.dry_run or not a.apply:
        print(f"DRY RUN -- would write {len(out)} bytes, sha {new_sha}"); return 0
    open(a.canonical, "wb").write(out)
    print(f"wrote {len(out)} bytes\nnew canonical SHA: {new_sha}"); return 0

if __name__ == "__main__":
    sys.exit(main())
