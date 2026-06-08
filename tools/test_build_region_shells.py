#!/usr/bin/env python3
"""Unit test for build_region_shells -- asserts the post-transform shape.
Run from repo root: python3 tools/test_build_region_shells.py

Two fixtures, deliberately decoupled from canonical fill-state:
  1. a SYNTHETIC stub crop -- exercises the build-from-stub path (warm skeleton,
     northern_tier promote-from-zones, dash resolution, parameterized provenance).
     It does NOT read any live crop, because a live-crop fixture rots as crops are
     authored through the arc: cherry's warm cells were empty `[]` skeletons at its
     Step 3.5 and are fully filled now, so asserting "warm windows are empty" against
     cherry silently breaks the moment cherry is sourced (it did).
  2. cherry-tomato (already built) -- an idempotency smoke test: re-running the
     transform on a fully-built real crop must be a no-op, never a corruption.
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_region_shells import build_region_shells

REGION_KEYS = {"northern_tier", "se_gulf", "ca_interior", "ca_north_coast",
               "ca_south_coast", "ca_desert", "warm_arid", "low_desert_az",
               "fl_peninsula", "hawaii_tropical"}


def synthetic_stub_crop():
    """A minimal pre-build crop: stub warm regions + a stale-shape north."""
    def warm(label):
        return {
            "region_label": label,
            "plantings": ["PENDING CORRECTION PHASE -- windows not yet pulled."],
            "resolved_by_zone": {"9": {"plant_out": "PENDING",
                                       "resolution_method": "static_precompute"}},
        }
    regions = {rk: warm("California -- Interior Valleys" if rk == "ca_interior" else rk)
               for rk in REGION_KEYS if rk != "northern_tier"}
    regions["northern_tier"] = {
        "region_label": "Northern Tier (Cold Zones)",
        "plantings": [{"succession_id": 1, "label": "main",
                       "start_indoors": [], "plant_out": [],
                       "harvest_start": [], "harvest_end": []}],  # NOTE: no track
        "resolved_by_zone": {
            z: {"plant_out": "May", "resolution_method": "static_precompute",
                "lifted_from_zone": z,                       # tautological in the north
                "plantings": [{"succession_id": 1, "label": "main"}]}  # forbidden nested
            for z in ("3", "4", "5", "6", "7")
        },
        "plantings_provenance": "LIFTED VERBATIM from zone 5.",
    }
    return {"slug": "synthetic", "regions": regions}


# ---- fixture 1: synthetic stub (the build-from-stub path) ----
crop = build_region_shells(synthetic_stub_crop(), session="m16_unit_test", date="2026-06-07")
regions = crop["regions"]
assert set(regions) == REGION_KEYS, f"region set: {set(regions)}"

# warm shells: dict plantings, valid track, present-but-empty window arrays
for rk in REGION_KEYS - {"northern_tier"}:
    p0 = regions[rk]["plantings"][0]
    assert isinstance(p0, dict) and p0["track"] == "beginner", f"{rk}: warm track"
    for w in ["start_indoors", "plant_out", "harvest_start", "harvest_end"]:
        assert p0.get(w) == [], f"{rk}: {w} should be present-but-empty, got {p0.get(w)!r}"

# every plantings entry is a dict with a valid track; no nested plantings survive
for rk, r in regions.items():
    for p in r["plantings"]:
        assert p.get("track") in {"beginner", "second_planting", "succession"}, f"{rk}: bad track {p.get('track')!r}"
    for z, cell in (r.get("resolved_by_zone") or {}).items():
        assert "plantings" not in cell, f"{rk}.{z}: nested plantings survived"

# northern_tier promoted from zones: restamped, lifted_from_zone stripped, provenance set
nt = regions["northern_tier"]
for z, cell in nt["resolved_by_zone"].items():
    assert cell.get("resolution_method") == "zone_promoted_verified", f"nt.{z}: not restamped"
    assert "lifted_from_zone" not in cell, f"nt.{z}: tautological lifted_from_zone not stripped"
prov = nt["plantings_provenance"]
assert "Zone-promoted" in prov, f"provenance lost its promotion marker: {prov!r}"
assert "m16_unit_test" in prov and "2026-06-07" in prov, f"provenance not parameterized: {prov!r}"

# region_label em-dashes resolved
for rk, r in regions.items():
    assert " -- " not in (r.get("region_label") or ""), f"{rk}: region_label still has --"

# region_notes keys present on every region (value may be null at shell stage)
for rk, r in regions.items():
    assert "region_notes_seasoned" in r and "region_notes_beginner" in r, f"{rk}: missing region_notes keys"

# defaults preserved (backward-compatible): a no-kwargs call keeps the cherry-era constant
default_built = build_region_shells(synthetic_stub_crop())
assert "m16_cherry_step3_5_region_shells" in default_built["regions"]["northern_tier"]["plantings_provenance"]

# ---- fixture 2: cherry-tomato idempotency smoke (already built; re-run must be a no-op) ----
data = json.load(open("crops_data_final.json"))
cherry = copy.deepcopy(next(c for c in data["crops"] if c["slug"] == "cherry-tomato"))
before = copy.deepcopy(cherry["regions"])
build_region_shells(cherry)  # default kwargs == the constants cherry was built with
assert cherry["regions"] == before, "transform not idempotent on an already-built crop"

# ---- fixture 3: author-fresh DIRECT-SOW crop (carrot-like) ----
# Wiped-shell crop: empty regions, no zones{} data, NT resolved cells emptied with
# null resolution_method (nothing to promote). Direct-sown (start_method.start=="direct").
# Expect: every region (incl. NT) gets a from-scratch beginner skeleton with the
# DIRECT-SOW window shape (direct_sow, NOT start_indoors/plant_out); NT is NOT promoted.
def direct_sow_author_fresh_crop():
    def shell(label):
        return {
            "region_label": label,
            "plantings": [],
            "region_notes_seasoned": None, "region_notes_beginner": None,
            "resolved_by_zone": {"9": {"calendar": [], "plant_out": None,
                                       "resolution_method": None}},
        }
    regions = {rk: shell(rk) for rk in REGION_KEYS if rk != "northern_tier"}
    regions["northern_tier"] = {
        "region_label": "Northern Tier (Cold Zones)",
        "plantings": [],
        "region_notes_seasoned": None, "region_notes_beginner": None,
        "resolved_by_zone": {z: {"calendar": [], "plantings": [],
                                 "resolution_method": None}
                             for z in ("3", "4", "5", "6", "7")},
    }
    return {"slug": "carrot-like", "start_method": {"start": "direct"},
            "succession_policy": {"suitable": True, "successions": 3},
            "zones": {}, "regions": regions}

c3 = build_region_shells(direct_sow_author_fresh_crop(), session="carrot_step3_5", date="2026-06-08")
r3 = c3["regions"]
assert set(r3) == REGION_KEYS, f"fixture3 region set: {set(r3)}"
for rk, r in r3.items():
    p0 = r["plantings"][0]
    assert isinstance(p0, dict) and p0["track"] == "beginner", f"{rk}: track"
    # DIRECT-SOW shape: direct_sow present-empty; transplant keys absent
    assert p0.get("direct_sow") == [], f"{rk}: direct_sow should be present-but-empty, got {p0.get('direct_sow')!r}"
    assert "start_indoors" not in p0 and "plant_out" not in p0, f"{rk}: transplant keys leaked into a direct-sow shell"
    assert p0.get("harvest_start") == [] and p0.get("harvest_end") == [], f"{rk}: harvest windows"
    for z, cell in (r.get("resolved_by_zone") or {}).items():
        assert "plantings" not in cell, f"{rk}.{z}: nested plantings survived"
    assert "region_notes_seasoned" in r and "region_notes_beginner" in r, f"{rk}: region_notes keys"
# NT is FROM-SCRATCH (not promoted): direct-sow skeleton, no promotion provenance
nt3 = r3["northern_tier"]
assert nt3["plantings"][0].get("direct_sow") == [], "NT not built as a direct-sow from-scratch shell"
assert "Zone-promoted" not in (nt3.get("plantings_provenance") or ""), "from-scratch NT was wrongly promoted-from-zones"

# ---- fixture 4: transplant author-fresh crop -> transplant shape, from-scratch NT ----
def transplant_author_fresh_crop():
    c = direct_sow_author_fresh_crop()
    c["slug"] = "pepper-like"
    c["start_method"] = {"start": "transplant"}
    return c

c4 = build_region_shells(transplant_author_fresh_crop())
p4 = c4["regions"]["se_gulf"]["plantings"][0]
assert p4.get("start_indoors") == [] and p4.get("plant_out") == [], "transplant author-fresh: missing transplant windows"
assert "direct_sow" not in p4, "transplant shell should not carry direct_sow"

print("PASS build_region_shells")
