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

# ---- fixture 5: PERMANENT TREE author-fresh crop (peach-like) -> tree region model ----
# A permanent tree is planted ONCE, then lives for decades. The annual sowing-window
# model does not fit it; Step 3.5 builds the TREE region shape instead:
#   - crop calendar_basis flips frost_anchored (wipe default) -> perennial_chill_gated
#   - plantings[] = a SINGLE one-time establishment entry, track:"perennial" (no succession)
#   - chill-adequacy layer (chill_hours_delivered + chill_basis_*) per region
#   - resolved cells reshaped to the tree key-set: a per-zone `suitability` verdict
#     (survives != fruits is FIRST-CLASS), chill, bloom/harvest/prune render fields,
#     a tree `calendar[]`; the annual-only keys are stripped.
# Input mimics the live peach scaffold: annual-shaped region cells, empty/null, the
# frost_anchored wipe default still on the crop.
def tree_author_fresh_crop():
    def annual_cell(z):
        return {"plant_out": None, "start_indoors": None, "harvest": None,
                "harvest_start": None, "harvest_end": None,
                "first_plant_date": None, "last_plant_date": None, "calendar": [],
                "notes": None, "zone_notes": None, "planting_note": None,
                "sources": [], "anchoring_urls": {}, "plantings": [],
                "resolution_method": None, "lifted_from_zone": None}
    def shell(label, zones):
        return {"region_id": None, "region_label": label, "zone_span": [],
                "sources": [], "sources_pending_admission": [],  # vestigial scaffold residue
                "plantings": [], "plantings_provenance": None,
                "resolved_by_zone": {z: annual_cell(z) for z in zones},
                "region_notes_seasoned": None, "region_notes_beginner": None}
    regions = {rk: shell("California -- Interior Valleys" if rk == "ca_interior" else rk, ("9",))
               for rk in REGION_KEYS if rk != "northern_tier"}
    regions["northern_tier"] = shell("Northern Tier (Cold Zones)", ("3", "4", "5", "6", "7"))
    return {"slug": "peach", "lifecycle": "permanent",
            "archetype": "deciduous_fruit_tree", "calendar_basis": "frost_anchored",
            "start_method": {"start": "bare_root_dormant"},
            "zones": {}, "regions": regions}

c5 = build_region_shells(tree_author_fresh_crop(), session="peach_step3_5", date="2026-06-10")
# the crop-level marker that makes the Step 5.5 gate branch to the tree model
assert c5["calendar_basis"] == "perennial_chill_gated", f"calendar_basis not flipped: {c5.get('calendar_basis')!r}"
r5 = c5["regions"]
assert set(r5) == REGION_KEYS, f"fixture5 region set: {set(r5)}"
for rk, r in r5.items():
    # region-constant rule: exactly ONE perennial establishment entry, no succession
    assert len(r["plantings"]) == 1, f"{rk}: tree must have exactly one establishment entry, got {len(r['plantings'])}"
    p0 = r["plantings"][0]
    assert p0.get("track") == "perennial", f"{rk}: establishment track must be 'perennial', got {p0.get('track')!r}"
    assert p0.get("label") == "establishment", f"{rk}: establishment label"
    for w in ("plant_out", "bloom", "harvest_start", "harvest_end"):
        assert p0.get(w) == [], f"{rk}: {w} should be present-but-empty rule list, got {p0.get(w)!r}"
    # a tree is bare-root: no annual sowing keys on the rule entry
    assert "start_indoors" not in p0 and "direct_sow" not in p0, f"{rk}: annual sowing keys leaked onto a tree entry"
    # chill-adequacy layer present-but-empty at shell stage
    assert r.get("chill_hours_delivered") == [], f"{rk}: chill_hours_delivered should be present-but-empty"
    assert "chill_basis_seasoned" in r and "chill_basis_beginner" in r, f"{rk}: chill_basis keys missing"
    # region_notes + dash resolution (shared with the annual model)
    assert "region_notes_seasoned" in r and "region_notes_beginner" in r, f"{rk}: region_notes keys"
    assert " -- " not in (r.get("region_label") or ""), f"{rk}: region_label still has --"
    # vestigial empty scaffold residue swept (matches the carrot Step 3.5 release)
    assert "sources_pending_admission" not in r, f"{rk}: empty sources_pending_admission residue not swept"
    # resolved cells reshaped to the TREE key-set
    for z, cell in r["resolved_by_zone"].items():
        # survives != fruits is FIRST-CLASS: the per-zone suitability verdict slot exists
        assert "suitability" in cell, f"{rk}.{z}: tree cell missing the suitability verdict slot"
        assert "suitability_note_seasoned" in cell and "suitability_note_beginner" in cell, f"{rk}.{z}: suitability_note keys"
        assert cell.get("chill_hours_delivered") == [], f"{rk}.{z}: cell chill_hours_delivered"
        assert cell.get("calendar") == [], f"{rk}.{z}: tree cell calendar should be present-but-empty"
        # render fields reuse the annual resolved-cell keys (renderer reads them uniformly)
        for w in ("plant_out", "bloom", "harvest_start", "harvest_end"):
            assert w in cell, f"{rk}.{z}: tree render key {w} missing"
        # annual-only leftovers stripped (a tree has no second sowing / lifted zone / nested rules)
        for dead in ("start_indoors", "lifted_from_zone", "plantings", "notes",
                     "zone_notes", "planting_note", "first_plant_date", "last_plant_date"):
            assert dead not in cell, f"{rk}.{z}: annual-only key {dead!r} survived into a tree cell"
# northern_tier is from-scratch (a tree cell, NOT zone-promoted)
nt5 = r5["northern_tier"]
assert nt5["plantings"][0].get("track") == "perennial", "NT not built as a tree establishment entry"
assert "Zone-promoted" not in (nt5.get("plantings_provenance") or ""), "tree NT was wrongly promoted-from-zones"
assert set(nt5["resolved_by_zone"]) == {"3", "4", "5", "6", "7"}, "NT zone keys not preserved (suitability carries the verdict, not zone-trimming)"

# ---- fixture 6: tree idempotency + no-clobber of a FILLED cell ----
built = build_region_shells(tree_author_fresh_crop(), session="peach_step3_5", date="2026-06-10")
before6 = copy.deepcopy(built["regions"])
build_region_shells(built)  # re-run must be a no-op on an already-built tree
assert built["regions"] == before6, "tree transform not idempotent on an already-built crop"
# a re-run must NOT wipe a cell Step 4 has already authored
filled = build_region_shells(tree_author_fresh_crop())
filled["regions"]["se_gulf"]["resolved_by_zone"]["9"].update(
    {"suitability": "fruits_reliably", "chill_hours_delivered": [700, 900],
     "bloom": "Mar 1 - Mar 20", "resolution_method": "perennial_precompute"})
filled["regions"]["se_gulf"]["chill_hours_delivered"] = [650, 950]
keep = copy.deepcopy(filled["regions"]["se_gulf"])
build_region_shells(filled)
assert filled["regions"]["se_gulf"] == keep, "tree build clobbered an already-authored cell"

# ---- fixture 7: EVERGREEN permanent tree (lemon-like) -> the evergreen tree model ----
# An evergreen fruit tree (citrus/avocado/olive) shares the tree two-layer cut but
# differs on TWO axes (tree_region_model_evergreen_amendment_v1_0): the calendar SHAPE
# (calendar_basis -> perennial_evergreen, no dormancy) and the suitability GATE (a
# crop-level gating_factors list). For a cold-only evergreen the region CLIMATE layer is
# min_winter_temp_f (the frost-risk datum), NOT chill_hours_delivered (chill ~ 0).
def evergreen_author_fresh_crop():
    base = tree_author_fresh_crop()
    base["slug"] = "lemon"
    base["archetype"] = "evergreen_fruit_tree"
    base["gating_factors"] = ["cold_hardiness"]
    return base

c7 = build_region_shells(evergreen_author_fresh_crop(), session="lemon_step3_5", date="2026-06-12")
# Axis 1: the calendar_basis SHAPE marker flips to perennial_evergreen (NOT chill_gated)
assert c7["calendar_basis"] == "perennial_evergreen", f"evergreen calendar_basis not set: {c7.get('calendar_basis')!r}"
r7 = c7["regions"]
assert set(r7) == REGION_KEYS, f"fixture7 region set: {set(r7)}"
for rk, r in r7.items():
    # the perennial establishment entry is shared with the deciduous tree
    assert len(r["plantings"]) == 1 and r["plantings"][0].get("track") == "perennial", f"{rk}: evergreen establishment entry"
    # region CLIMATE layer is gating-keyed: cold_hardiness -> min_winter_temp_f + cold_basis_*
    assert r.get("min_winter_temp_f") == [], f"{rk}: min_winter_temp_f should be present-but-empty, got {r.get('min_winter_temp_f')!r}"
    assert "cold_basis_seasoned" in r and "cold_basis_beginner" in r, f"{rk}: cold_basis keys missing"
    # an evergreen is NOT chill-gated: no chill climate fields
    assert "chill_hours_delivered" not in r, f"{rk}: chill_hours_delivered leaked onto an evergreen region"
    assert "chill_basis_seasoned" not in r, f"{rk}: chill_basis leaked onto an evergreen region"
    for z, cell in r["resolved_by_zone"].items():
        # shared tree cell shape: suitability verdict + reused render keys + empty calendar
        assert "suitability" in cell, f"{rk}.{z}: evergreen cell missing suitability verdict"
        assert cell.get("calendar") == [], f"{rk}.{z}: evergreen cell calendar should be present-but-empty"
        for w in ("plant_out", "bloom", "harvest_start", "harvest_end"):
            assert w in cell, f"{rk}.{z}: evergreen render key {w} missing"
        # cell climate is min_winter_temp_f, not chill
        assert cell.get("min_winter_temp_f") == [], f"{rk}.{z}: cell min_winter_temp_f should be present-but-empty"
        assert "chill_hours_delivered" not in cell, f"{rk}.{z}: chill_hours_delivered leaked onto an evergreen cell"
        for dead in ("start_indoors", "lifted_from_zone", "plantings", "notes"):
            assert dead not in cell, f"{rk}.{z}: annual-only key {dead!r} survived into an evergreen cell"

# evergreen idempotency: a re-run is a no-op (and re-detects via the perennial_evergreen basis)
built7 = build_region_shells(evergreen_author_fresh_crop(), session="lemon_step3_5", date="2026-06-12")
before7 = copy.deepcopy(built7["regions"])
build_region_shells(built7)
assert built7["regions"] == before7, "evergreen transform not idempotent on an already-built crop"

# the DECIDUOUS path stays exactly as before (peach/apple byte-identical regression)
assert c5["calendar_basis"] == "perennial_chill_gated", "deciduous basis changed -- regression"
assert r5["se_gulf"].get("chill_hours_delivered") == [], "deciduous chill layer changed -- regression"
assert "min_winter_temp_f" not in r5["se_gulf"], "deciduous region wrongly got an evergreen climate field"

# ---- fixture 8: HEAT-gated evergreen (orange-navel-like) -> +heat climate layer ----
# An evergreen whose gating_factors include heat_accumulation (orange, grapefruit) banks a
# SECOND climate datum beyond cold: heat_summer_basis (the qualitative summer-heat-adequacy
# verdict) + heat_basis_* prose, ALONGSIDE the cold min_winter_temp_f. Cool-summer cells are
# frost-safe but cannot sweeten fruit -- the heat floor, enforced at fill-time by perennial_gate.
def heat_evergreen_author_fresh_crop():
    base = evergreen_author_fresh_crop()
    base["slug"] = "orange-navel"
    base["gating_factors"] = ["cold_hardiness", "heat_accumulation"]
    return base

c8 = build_region_shells(heat_evergreen_author_fresh_crop(), session="orange_step3_5", date="2026-06-12")
assert c8["calendar_basis"] == "perennial_evergreen", f"heat-evergreen calendar_basis: {c8.get('calendar_basis')!r}"
r8 = c8["regions"]
assert set(r8) == REGION_KEYS, f"fixture8 region set: {set(r8)}"
for rk, r in r8.items():
    # cold datum still present (cold_hardiness is also in gating_factors)
    assert r.get("min_winter_temp_f") == [], f"{rk}: cold datum missing on a heat-gated evergreen"
    assert "cold_basis_seasoned" in r and "cold_basis_beginner" in r, f"{rk}: cold_basis keys missing"
    # NEW heat climate layer present-but-empty (enum verdict = None at shell stage; prose = None)
    assert "heat_summer_basis" in r and r.get("heat_summer_basis") is None, f"{rk}: heat_summer_basis region slot missing or non-null"
    assert "heat_basis_seasoned" in r and "heat_basis_beginner" in r, f"{rk}: heat_basis prose keys missing"
    # still NOT chill-gated (chill ~ 0 for citrus)
    assert "chill_hours_delivered" not in r, f"{rk}: chill leaked onto a heat-gated evergreen"
    for z, cell in r["resolved_by_zone"].items():
        assert cell.get("min_winter_temp_f") == [], f"{rk}.{z}: cell cold datum missing"
        assert "heat_summer_basis" in cell and cell.get("heat_summer_basis") is None, f"{rk}.{z}: cell heat_summer_basis slot missing or non-null"
        assert "chill_hours_delivered" not in cell, f"{rk}.{z}: chill leaked onto a heat-gated evergreen cell"

# heat-evergreen idempotency: a re-run is a no-op
built8 = build_region_shells(heat_evergreen_author_fresh_crop(), session="orange_step3_5", date="2026-06-12")
before8 = copy.deepcopy(built8["regions"])
build_region_shells(built8)
assert built8["regions"] == before8, "heat-evergreen transform not idempotent on an already-built crop"

# REGRESSION: a COLD-ONLY evergreen (lemon, fixture 7) gets NO heat scaffolding -- the heat
# layer is gating_factor-keyed, so lemon stays byte-identical to its pre-heat build.
for rk, r in r7.items():
    assert "heat_summer_basis" not in r, f"{rk}: heat_summer_basis leaked onto a cold-only evergreen region"
    assert "heat_basis_seasoned" not in r and "heat_basis_beginner" not in r, f"{rk}: heat_basis leaked onto a cold-only evergreen region"
    for z, cell in r["resolved_by_zone"].items():
        assert "heat_summer_basis" not in cell, f"{rk}.{z}: heat_summer_basis leaked onto a cold-only evergreen cell"

print("PASS build_region_shells")
