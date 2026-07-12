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
    }
    return {"slug": slug, "regions": regions}

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

if fails:
    print(f"\n{len(fails)} test(s) FAILED"); sys.exit(1)
print("\nall build_zonespan_widen_patch tests passed")
