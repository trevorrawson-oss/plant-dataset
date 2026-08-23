#!/usr/bin/env python3
"""PLA-8: split `bottom_watering`; mint `water_at_the_base`; revert a mis-attached widening. Base 208e213c.

Rationale, sources and the full defect account: tools/build_water_at_base_content.py

WHAT MOVES. control_methods 42 -> 43. `water_at_the_base` is created carrying the `bacterial` and
`mollusk` targets plus the two sources that d19abe60 wrongly attached to `bottom_watering`, and
`bottom_watering` reverts to its pre-d19abe60 applies_to and sources. NO crop is touched, NO source
is minted or removed from the catalog, and the two shipped microgreens rungs that legitimately use
bottom_watering are unaffected.

THIS PROMOTE PARTIALLY REVERTS AN EARLIER ONE, ON PURPOSE. The sourcing in d19abe60 was sound; the
entry it was attached to was not. Reverting the attachment while keeping the sources is the honest
shape, and it is why `ucanr_ext_bacterial_speck` moves rather than being deleted.

REFUSALS: base SHA mismatch; the method already exists; bottom_watering missing; a source that does
not resolve or is not T1; a revert that would orphan a source still used elsewhere.

Guard suite:      tools/test_promote_pla8_water_at_base.py
Mutation harness: tools/mutate_pla8_wab_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_water_at_base.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "208e213cb14dce4e2df6b0a48ad49f7e6818337dcd4ce5b1b52691954af542ce"
TIERS = ("cultural","physical","biological","soft_chemical","conventional")
REQ = ("name","tier","applies_to","how_it_works_beginner","how_it_works_seasoned","best_use",
       "pros","cons","sources","anchoring_urls")

def content():
    import build_water_at_base_content as B
    return B.NEW_METHOD, B.REVERT

def check(data):
    cm, sc = data["control_methods"], data["source_catalog"]
    new, rev = content()
    for k, m in new.items():
        if k in cm:
            return f"control_methods.{k} already exists; this promote creates it"
        if m["tier"] not in TIERS:
            return f"{k}: bad tier {m['tier']!r}"
        for f in REQ:
            if not m.get(f):
                return f"{k}: missing/empty {f!r}"
        for s in m["sources"]:
            if s not in sc:
                return f"{k}: source {s!r} not in source_catalog"
            if sc[s].get("tier") != "T1":
                return f"{k}: source {s!r} is not T1"
        if set(m["anchoring_urls"]) != set(m["sources"]):
            return f"{k}: anchoring_urls keys do not match sources"
    if "bottom_watering" not in cm:
        return "bottom_watering missing; nothing to revert"
    bw = cm["bottom_watering"]
    for t in ("bacterial", "mollusk"):
        if t not in bw["applies_to"]:
            return f"bottom_watering does not carry {t!r}; the revert is a no-op"
    # a source dropped from bottom_watering must survive elsewhere, or move to the new method
    for s in rev["drop_anchors"]:
        others = [k for k, v in cm.items() if k != "bottom_watering" and s in v.get("sources", [])]
        moving = any(s in m["sources"] for m in new.values())
        if not others and not moving:
            return f"dropping {s!r} from bottom_watering would orphan it"
    return None

def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def apply_to(data):
    new, rev = content()
    data["control_methods"].update(json.loads(json.dumps(new)))
    bw = data["control_methods"]["bottom_watering"]
    bw["applies_to"] = list(rev["applies_to"])
    bw["sources"] = list(rev["sources"])
    for s in rev["drop_anchors"]:
        bw["anchoring_urls"].pop(s, None)
    return len(new)

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
    bw_before = list(data["control_methods"]["bottom_watering"]["applies_to"])
    n = apply_to(data)
    print("PLA-8 -- water_at_the_base split")
    print(f"  control_methods {before} -> {len(data['control_methods'])}  (+{n})")
    print(f"  bottom_watering applies_to {bw_before} -> {data['control_methods']['bottom_watering']['applies_to']}")
    out = serialize(data); new_sha = hashlib.sha256(out).hexdigest()
    if a.dry_run or not a.apply:
        print(f"DRY RUN -- would write {len(out)} bytes, sha {new_sha}"); return 0
    open(a.canonical, "wb").write(out)
    print(f"wrote {len(out)} bytes\nnew canonical SHA: {new_sha}"); return 0

if __name__ == "__main__":
    sys.exit(main())
