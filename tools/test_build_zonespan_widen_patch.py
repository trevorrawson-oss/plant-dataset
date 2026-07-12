#!/usr/bin/env python3
"""Unit test for build_zonespan_widen_patch -- op emission on synthetic fixtures.
Run from repo root: python3 tools/test_build_zonespan_widen_patch.py
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_zonespan_widen_patch import build_widen_ops
from zone_span_gate import EXPECTED_SPANS, DONORS, check_crop

DONOR_ROW = {"plant_out": "Mar 1 - Mar 21", "calendar": ["plant"] * 12,
             "zone_notes": None, "lifted_from_zone": None,
             "sources": ["uariz_ext"]}

def stale_crop(slug="alpha"):
    """Pre-widen shapes: stale spans, one int-typed, one empty."""
    regions = {
        "low_desert_az": {"zone_span": ["9"],
                          "resolved_by_zone": {"9": copy.deepcopy(DONOR_ROW)}},
        "warm_arid":     {"zone_span": [8],      # int-typed
                          "resolved_by_zone": {"8": copy.deepcopy(DONOR_ROW)}},
        "fl_peninsula":  {"zone_span": [],       # empty but populated
                          "resolved_by_zone": {"10": copy.deepcopy(DONOR_ROW),
                                                "11": copy.deepcopy(DONOR_ROW)}},
        "ca_interior":   {"zone_span": ["8", "9"],   # already correct -> no op
                          "resolved_by_zone": {"8": copy.deepcopy(DONOR_ROW),
                                                "9": copy.deepcopy(DONOR_ROW)}},
        "hawaii_tropical": {"zone_span": ["11"],     # multi-donor: z10/z12/z13 all <- z11
                            "resolved_by_zone": {"11": copy.deepcopy(DONOR_ROW)}},
    }
    return {"slug": slug, "verification_status": {"status": "verified_gs_arc"},
            "regions": regions}

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

data = {"crops": [stale_crop()]}
ops = build_widen_ops(data)
by_path = {o["json_path"]: o for o in ops}

# 1. Clone op for az z10, donor row copied with lifted_from_zone set.
p = "$.crops[?(@.slug=='alpha')].regions.low_desert_az.resolved_by_zone.10"
check("az z10 clone emitted", p in by_path and by_path[p]["op"] == "add")
row = by_path[p]["value"]
check("clone marked lifted_from_zone=9", row["lifted_from_zone"] == "9")
check("clone copies donor content", row["plant_out"] == DONOR_ROW["plant_out"])
check("clone is a COPY not a reference",
      row is not data["crops"][0]["regions"]["low_desert_az"]["resolved_by_zone"]["9"])

# 1b. Multi-donor region: hawaii z10/z12/z13 all clone from the single donor z11.
for nz in ("10", "12", "13"):
    hp = f"$.crops[?(@.slug=='alpha')].regions.hawaii_tropical.resolved_by_zone.{nz}"
    check(f"hawaii z{nz} clone emitted from z11",
          hp in by_path and by_path[hp]["op"] == "add"
          and by_path[hp]["value"]["lifted_from_zone"] == "11")
check("hawaii span widened 11 -> 10,11,12,13",
      by_path["$.crops[?(@.slug=='alpha')].regions.hawaii_tropical.zone_span"]["value"]
      == ["10", "11", "12", "13"])

# 2. Span replaces: stale, int-typed, empty all normalized; correct one skipped.
sp = lambda rid: f"$.crops[?(@.slug=='alpha')].regions.{rid}.zone_span"
check("stale az span replaced", by_path[sp("low_desert_az")]["value"] == ["9", "10"])
check("stale az from-guard verbatim", by_path[sp("low_desert_az")]["from"] == ["9"])
check("int span normalized", by_path[sp("warm_arid")]["value"] == ["8"]
      and by_path[sp("warm_arid")]["from"] == [8])
check("empty span filled", by_path[sp("fl_peninsula")]["value"] == ["10", "11"])
check("correct span skipped (no-op)", sp("ca_interior") not in by_path)

# 3. Non-widened regions get NO clone ops.
check("no clone into fl_peninsula",
      not any("fl_peninsula.resolved_by_zone" in q for q in by_path))

# 4. Idempotency: applying the ops mentally then re-building emits zero ops.
widened = copy.deepcopy(data)
for rid, cell in widened["crops"][0]["regions"].items():
    for new, donor in (DONORS.get(rid) or {}).items():
        r = copy.deepcopy(cell["resolved_by_zone"][donor]); r["lifted_from_zone"] = donor
        cell["resolved_by_zone"][new] = r
    cell["zone_span"] = list(EXPECTED_SPANS[rid])
check("idempotent (widened input -> zero ops)", build_widen_ops(widened) == [])

# 5. The widened synthetic crop passes the A45 gate (builder and gate agree).
check("widened crop passes A45", check_crop(widened["crops"][0]) == [])

# 6. Crop without regions -> zero ops, no crash.
check("regionless crop no-ops", build_widen_ops({"crops": [{"slug": "x"}]}) == [])

# 7. Chill-table clone ops: donor band copied to each new zone; already-present skipped;
#    value is a fresh copy (not a reference to the donor list).
data2 = {"crops": [], "region_chill_delivered": {
    "low_desert_az": {"9": [100, 400]},
    "se_gulf": {"8": [650, 1000], "9": [350, 650]},
    "hawaii_tropical": {"11": [0, 150]},
    "ca_south_coast": {"9": [200, 550], "10": [50, 350], "11": [0, 99]},  # 11 present -> skip
}}
cops = {o["json_path"]: o for o in build_widen_ops(data2)}
check("az chill z10 cloned from z9",
      cops.get("$.region_chill_delivered.low_desert_az.10", {}).get("value") == [100, 400])
check("se_gulf chill z10 cloned from z9",
      cops.get("$.region_chill_delivered.se_gulf.10", {}).get("value") == [350, 650])
check("hawaii chill z12 cloned from z11",
      cops.get("$.region_chill_delivered.hawaii_tropical.12", {}).get("value") == [0, 150])
check("hawaii chill z13 cloned from z11",
      cops.get("$.region_chill_delivered.hawaii_tropical.13", {}).get("value") == [0, 150])
check("present chill band skipped (ca_south_coast z11)",
      "$.region_chill_delivered.ca_south_coast.11" not in cops)
check("chill clone is a copy not a reference",
      cops["$.region_chill_delivered.low_desert_az.10"]["value"]
      is not data2["region_chill_delivered"]["low_desert_az"]["9"])

# 8. Uncertified crop is SKIPPED entirely (no span/row ops) -- shells carry empty-calendar
#    cells that would trip A32 if cloned; they are widened only when authored + certified.
shell = stale_crop("shell")
shell["verification_status"] = {"status": "shell"}  # not verified_gs_arc
check("uncertified crop emits no ops",
      build_widen_ops({"crops": [shell]}) == [])
# a certified crop in the SAME batch still gets widened (skip is per-crop, not all-or-nothing).
mixed = {"crops": [shell, stale_crop("cert")]}
mixed_paths = {o["json_path"] for o in build_widen_ops(mixed)}
check("certified crop in mixed batch still widened",
      any(".slug=='cert'" in p for p in mixed_paths))
check("uncertified crop in mixed batch untouched",
      not any(".slug=='shell'" in p for p in mixed_paths))
# a crop with NO verification_status key is treated as uncertified (skipped).
noskey = stale_crop("nostatus"); noskey.pop("verification_status")
check("missing verification_status -> skipped",
      build_widen_ops({"crops": [noskey]}) == [])

if fails:
    print(f"\n{len(fails)} test(s) FAILED"); sys.exit(1)
print("\nall build_zonespan_widen_patch tests passed")
