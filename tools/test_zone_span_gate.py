#!/usr/bin/env python3
"""Unit test for zone_span_gate (A45) -- expected-span + parity + donor integrity.
Run from repo root: python3 tools/test_zone_span_gate.py

Synthetic fixtures only (a live-crop fixture rots as the roster is authored).
Also carries the SWEEP ACCEPTANCE fixture: the Tier-1 gap table from
docs/2026-07-12-region-zonespan-gaps.md must be covered by EXPECTED_SPANS.
"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zone_span_gate import check_crop, EXPECTED_SPANS, DONORS

def make_crop():
    """A minimal crop whose regions exactly match EXPECTED_SPANS."""
    regions = {}
    for rid, span in EXPECTED_SPANS.items():
        regions[rid] = {
            "region_id": rid,
            "zone_span": list(span),
            "resolved_by_zone": {z: {"plant_out": "Mar 1 - Mar 21",
                                     "lifted_from_zone": None} for z in span},
        }
    return {"slug": "synthetic",
            "verification_status": {"status": "verified_gs_arc"},
            "regions": regions}

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

# 1. Conforming crop -> no violations.
check("conforming crop passes", check_crop(make_crop()) == [])

# 2. No regions dict -> no-op.
check("regionless crop passes", check_crop({"slug": "x"}) == [])

# 3. Divergent span value -> violation.
c = make_crop()
c["regions"]["low_desert_az"]["zone_span"] = ["9"]          # stale, pre-widen
check("stale span bounces", any("low_desert_az" in v for v in check_crop(c)))

# 4. Int-typed span -> violation (type is part of the contract).
c = make_crop()
c["regions"]["warm_arid"]["zone_span"] = [8]
check("int-typed span bounces", any("warm_arid" in v for v in check_crop(c)))

# 5. Empty span with populated rows -> violation.
c = make_crop()
c["regions"]["se_gulf"]["zone_span"] = []
check("empty span bounces", any("se_gulf" in v for v in check_crop(c)))

# 6. Span/key parity: span lists a zone with no resolved row -> violation.
c = make_crop()
del c["regions"]["hawaii_tropical"]["resolved_by_zone"]["12"]
check("missing resolved row bounces",
      any("hawaii_tropical" in v for v in check_crop(c)))

# 7. Parity the other way: an extra resolved row not in the span -> violation.
c = make_crop()
c["regions"]["ca_interior"]["resolved_by_zone"]["10"] = {"plant_out": "x",
                                                         "lifted_from_zone": None}
check("orphan resolved row bounces",
      any("ca_interior" in v for v in check_crop(c)))

# 8. Dangling lifted_from_zone -> violation.
c = make_crop()
c["regions"]["se_gulf"]["resolved_by_zone"]["10"]["lifted_from_zone"] = "77"
check("dangling lifted_from_zone bounces",
      any("se_gulf" in v for v in check_crop(c)))

# 9. Valid lifted_from_zone -> pass.
c = make_crop()
c["regions"]["se_gulf"]["resolved_by_zone"]["10"]["lifted_from_zone"] = "9"
check("valid lifted_from_zone passes", check_crop(c) == [])

# 10. Unknown region id -> violation.
c = make_crop()
c["regions"]["atlantis"] = {"region_id": "atlantis", "zone_span": ["1"],
                            "resolved_by_zone": {"1": {}}}
check("unknown region bounces", any("atlantis" in v for v in check_crop(c)))

# 11. Empty resolved_by_zone -> no-op (shell tolerance, must not crash).
c = make_crop()
c["regions"]["warm_arid"]["resolved_by_zone"] = {}
c["regions"]["warm_arid"]["zone_span"] = []
check("empty shell tolerated", not any("warm_arid" in v for v in check_crop(c)))

# 11b. Uncertified crop is EXEMPT: a shell with a stale/narrow span does not bounce
#      (enforced on the certified roster only, matching gate_all). It IS flagged once certified.
c = make_crop()
c["regions"]["low_desert_az"]["zone_span"] = ["9"]  # stale
c["verification_status"] = {"status": "shell"}
check("uncertified crop exempt from A45", check_crop(c) == [])
c.pop("verification_status")
check("missing verification_status exempt", check_crop(c) == [])

# 12. SWEEP ACCEPTANCE: every Tier-1 gap from the source report is covered.
TIER1 = [("AZ", "10", "low_desert_az"), ("HI", "12", "hawaii_tropical"),
         ("HI", "13", "hawaii_tropical"), ("HI", "10", "hawaii_tropical"),
         ("TX", "10", "se_gulf"),        # interim ruling, spec section 4
         ("CA", "11", "ca_south_coast"), ("CA", "11", "ca_desert"),
         ("LA", "10", "se_gulf")]
for state, zone, rid in TIER1:
    check(f"sweep {state} z{zone} -> {rid}", zone in EXPECTED_SPANS[rid])

# 13. DONORS sanity: every donor zone is inside its region's expected span,
#     and every donated zone is too.
for rid, m in DONORS.items():
    for new, donor in m.items():
        check(f"donor {rid} {new}<-{donor}",
              new in EXPECTED_SPANS[rid] and donor in EXPECTED_SPANS[rid])

if fails:
    print(f"\n{len(fails)} test(s) FAILED"); sys.exit(1)
print("\nall zone_span_gate tests passed")
