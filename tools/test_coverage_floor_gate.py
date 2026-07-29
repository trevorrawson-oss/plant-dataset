#!/usr/bin/env python3
"""Tests for the coverage-floor cert gates (whole_crop_gate A31 region roster + A32 calendar
presence; incognito-redteam C3 + C4). Run: python3 tools/test_coverage_floor_gate.py

C3 (A31 region_roster_violations): a non-indoor crop ships with regions:{} (zero coverage) or
a single region and PASSES -- "10 regions" was enforced nowhere. The 10-region roster is the
coverage floor; an indoor / zone_independent crop legitimately collapses regions to {}.

C4 (A32 calendar_presence_violations): delete calendar[] on every filled cell of a frost_anchored
annual (keep plantings + region_notes) and it certifies -- A5/A24/A28 all `continue` on an absent
calendar, A2 checks plantings not the calendar. A frost_anchored resolved cell must carry a
non-empty calendar (the page's core deliverable). Trees/indoor are out of scope (tree empty cells
are governed by A3; indoor has no cells).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coverage_floor_gate import (region_roster_violations, calendar_presence_violations,
                                  CANONICAL_REGIONS, CALENDAR_PRESENCE_BASES)
from zone_span_gate import EXPECTED_SPANS

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
_data = json.load(open(_path, encoding="utf-8")) if os.path.exists(_path) else {"crops": []}
_cert = [c for c in _data["crops"]
         if c.get("verification_status", {}).get("status") == "verified_gs_arc"]


def _full_regions():
    return {r: {"plantings": [{"track": "succession"}], "resolved_by_zone": {"8": {"calendar": ["growing"]}}}
            for r in CANONICAL_REGIONS}


# ============================== C3 -- region roster floor (A31) ==============================
# 0. the canonical roster is DERIVED from zone_span_gate.EXPECTED_SPANS (the single source of
#    truth for the region universe) -- never a hardcoded literal set, so this assertion can never
#    drift out of sync again when a future region (rgv, maritime-PNW, ...) is added there.
assert CANONICAL_REGIONS == set(EXPECTED_SPANS), sorted(CANONICAL_REGIONS)

# 1. a non-indoor crop with the full roster -> clean
ok = {"slug": "x", "calendar_basis": "frost_anchored", "regions": _full_regions()}
assert region_roster_violations(ok) == [], region_roster_violations(ok)

# 2. regions:{} on a non-indoor crop (the audit injection) -> violation
bad = {"slug": "x", "calendar_basis": "frost_anchored", "regions": {}}
assert region_roster_violations(bad), "empty regions on a non-indoor crop must be flagged"

# 3. a SINGLE region (partial roster) -> violation, names what's missing
one = {"slug": "x", "calendar_basis": "frost_anchored",
       "regions": {"se_gulf": {"plantings": [{"track": "succession"}]}}}
v = region_roster_violations(one)
assert v and "missing" in v[0].lower(), v

# 4. an UNKNOWN region key (typo) -> violation
typo = {"slug": "x", "calendar_basis": "frost_anchored", "regions": dict(_full_regions(), mars={})}
assert region_roster_violations(typo), "an unknown region key must be flagged"

# 5. indoor crop (non_seasonal_indoor) collapses regions to {} -> clean (legit N/A)
indoor = {"slug": "microgreens-mix", "calendar_basis": "non_seasonal_indoor", "regions": {}}
assert region_roster_violations(indoor) == [], region_roster_violations(indoor)
# re-audit #2 D1: indoor exemption is now keyed on calendar_basis ONLY -- the zone_independent flag
# alone (without the non_seasonal_indoor basis) does NOT exempt the floor (see 6b below).

# 6. an indoor crop that ANOMALOUSLY carries regions -> violation (off-model)
indoor_regions = {"slug": "x", "calendar_basis": "non_seasonal_indoor", "regions": _full_regions()}
assert region_roster_violations(indoor_regions), "indoor crop with non-empty regions is off-model"

# 6b. re-audit #2 D1: zone_independent:true on a NON-indoor basis must NOT exempt the roster floor
#     (the floor keys on calendar_basis now, not the unvalidated flag).
zi_kill = {"slug": "x", "calendar_basis": "frost_anchored", "zone_independent": True, "regions": {}}
assert region_roster_violations(zi_kill), "zone_independent must not be a backdoor out of the region floor"

# 7. REAL DATA: every certified anchor passes the roster floor (0 FP)
fp = [(c["slug"], region_roster_violations(c)) for c in _cert if region_roster_violations(c)]
assert fp == [], f"C3 region-roster FP on certified anchors: {fp}"

# ============================ C4 -- calendar presence floor (A32) ============================
def _annual():
    return {"slug": "x", "calendar_basis": "frost_anchored", "regions": {
        "se_gulf": {"plantings": [{"track": "succession"}], "resolved_by_zone": {
            "8": {"calendar": ["growing", "harvest"]}, "9": {"calendar": ["growing"]}}},
        "northern_tier": {"plantings": [{"track": "succession"}], "resolved_by_zone": {
            "3": {"calendar": ["cold_pause", "growing"]}}}}}


# 8. a frost_anchored crop with calendars on every cell -> clean
assert calendar_presence_violations(_annual()) == [], calendar_presence_violations(_annual())

# 9. the audit injection: a filled cell whose calendar[] is EMPTY -> violation
c = _annual(); c["regions"]["se_gulf"]["resolved_by_zone"]["8"]["calendar"] = []
assert any("se_gulf" in v and "8" in v for v in calendar_presence_violations(c)), calendar_presence_violations(c)

# 10. a filled cell whose calendar key is ABSENT entirely -> violation
c = _annual(); del c["regions"]["se_gulf"]["resolved_by_zone"]["9"]["calendar"]
assert any("se_gulf" in v and "9" in v for v in calendar_presence_violations(c)), calendar_presence_violations(c)

# 11. NON-frost_anchored is OUT OF SCOPE: a tree (perennial) with empty cells is NOT flagged here
#     (A3 governs tree empty cells -- unsuitable / chill-limited cells are legitimately empty).
tree = {"slug": "peach", "calendar_basis": "perennial_chill_gated", "regions": {
    "northern_tier": {"resolved_by_zone": {"3": {"suitability": "unsuitable", "calendar": []}}}}}
assert calendar_presence_violations(tree) == [], calendar_presence_violations(tree)

# 12. indoor crop (no regions) -> no-op
assert calendar_presence_violations({"slug": "x", "calendar_basis": "non_seasonal_indoor", "regions": {}}) == []

# 13. REAL DATA: every certified anchor passes the calendar-presence floor (0 FP)
fp = [(c["slug"], calendar_presence_violations(c)) for c in _cert if calendar_presence_violations(c)]
assert fp == [], f"C4 calendar-presence FP on certified anchors: {fp}"

# ===== re-audit #2 D2/D7: the zone layer below the region key was never validated =====
# 14. D2: a region with an EMPTY resolved_by_zone (hollow) -> violation (A31 checked region keys only)
hollow = {"slug": "x", "calendar_basis": "frost_anchored", "regions": _full_regions()}
hollow["regions"]["se_gulf"]["resolved_by_zone"] = {}
assert any("se_gulf" in v and "zone" in v.lower() for v in region_roster_violations(hollow)), \
    f"D2: hollow resolved_by_zone must flag: {region_roster_violations(hollow)}"

# 15. D7: a FICTITIOUS zone key -> violation (no zone roster existed)
fic = {"slug": "x", "calendar_basis": "frost_anchored", "regions": _full_regions()}
fic["regions"]["se_gulf"]["resolved_by_zone"] = {"banana_zone": {"calendar": ["growing"]}}
assert any("se_gulf" in v and "banana_zone" in v for v in region_roster_violations(fic)), \
    f"D7: fictitious zone key must flag: {region_roster_violations(fic)}"
# valid USDA zone keys (3-11) stay clean
ok_zones = {"slug": "x", "calendar_basis": "frost_anchored", "regions": _full_regions()}
ok_zones["regions"]["se_gulf"]["resolved_by_zone"] = {"9": {"calendar": ["growing"]}, "10": {"calendar": ["growing"]}}
assert region_roster_violations(ok_zones) == [], region_roster_violations(ok_zones)

# ===== re-audit #2 D3: calendar-presence floor extended to the 3 NON-TREE perennial archetypes =====
def _perennial(basis):
    return {"slug": "x", "calendar_basis": basis, "regions": {
        "se_gulf": {"resolved_by_zone": {"8": {"calendar": ["dormant", "growing", "harvest"]}}}}}


# 16. a non-tree perennial (herbaceous/woody/berries_woody) with an EMPTY cell calendar -> violation
for basis in ("perennial_herbaceous", "berries_woody", "perennial_woody_ornamental"):
    c = _perennial(basis); c["regions"]["se_gulf"]["resolved_by_zone"]["8"]["calendar"] = []
    assert any("se_gulf" in v and "8" in v for v in calendar_presence_violations(c)), \
        f"D3: empty calendar on {basis} must flag: {calendar_presence_violations(c)}"
    # a filled calendar on the same is clean
    assert calendar_presence_violations(_perennial(basis)) == [], basis

# 17. REGRESSION: a TREE (perennial_chill_gated/evergreen) with an empty cell is NOT flagged here
#     (A3 governs tree empty cells -- unsuitable/chill-limited cells are legitimately empty)
for basis in ("perennial_chill_gated", "perennial_evergreen"):
    c = _perennial(basis); c["regions"]["se_gulf"]["resolved_by_zone"]["8"]["calendar"] = []
    assert calendar_presence_violations(c) == [], f"tree {basis} empty cell is A3's job, not the floor"

# 18. REAL DATA: the calendar-presence floor (now incl. the 3 perennials) is still 0-FP on the 18
fp2 = [(c["slug"], calendar_presence_violations(c)) for c in _cert if calendar_presence_violations(c)]
assert fp2 == [], f"D3 calendar-presence FP on certified anchors: {fp2}"
if _cert:
    print(f"  real data: 0 FP across {len(_cert)} certified (region+zone+calendar floors): PASS")

print("coverage_floor_gate: all tests passed")

# ===== hardening item 4 (2026-07-29): `unsuitable` is EXEMPT from the calendar-presence floor =====
# The floor's message is a RENDERING CONTRACT, and no consumer renders an `unsuitable` cell
# (plant-astro builds no page for it; plant-app maps it to 'blocked'). Requiring content there
# could only be satisfied by inventing it -- which is what had happened on 11 real cells.

def _cell(basis, suit, cal):
    c = {"slug": "probe", "calendar_basis": basis, "regions": {
        "se_gulf": {"resolved_by_zone": {"9": {"calendar": cal}}}}}
    if suit is not None:
        c["regions"]["se_gulf"]["resolved_by_zone"]["9"]["suitability"] = suit
    return c


# 19. GREEN: an `unsuitable` cell with an EMPTY calendar is clean on every presence base.
#     Guard against a vacuous loop: assert each name really IS a presence base, or the
#     exemption assertion below would pass simply because the gate no-ops off the basis.
for basis in ("frost_anchored", "perennial_herbaceous", "berries_woody",
              "perennial_woody_ornamental"):
    assert basis in CALENDAR_PRESENCE_BASES, f"{basis!r} is not a presence base -- test is vacuous"
    c = _cell(basis, "unsuitable", [])
    assert calendar_presence_violations(c) == [], \
        f"unsuitable must be exempt on {basis}: {calendar_presence_violations(c)}"

# 20. ADVERSARIAL: the carve is NARROW. Every OTHER suitability value with an empty calendar
#     still bounces -- the exemption keys on the value, not on carrying a suitability key.
for suit in ("perennializes", "marginal", "annual_only", "survives_no_fruit", "fruits_reliably"):
    c = _cell("frost_anchored", suit, [])
    assert any("se_gulf" in v and "9" in v for v in calendar_presence_violations(c)), \
        f"{suit} with an empty calendar MUST still flag: {calendar_presence_violations(c)}"

# 21. ADVERSARIAL: a cell with NO suitability key at all (an ordinary annual) still bounces --
#     absence must not read as exemption.
c = _cell("frost_anchored", None, [])
assert any("se_gulf" in v for v in calendar_presence_violations(c)), \
    f"a suitability-less empty cell must still flag: {calendar_presence_violations(c)}"

# 22. ADVERSARIAL: near-miss spellings do NOT earn the exemption.
for bogus in ("Unsuitable", "UNSUITABLE", "unsuitable ", "un-suitable", "unsuited"):
    c = _cell("frost_anchored", bogus, [])
    assert any("se_gulf" in v for v in calendar_presence_violations(c)), \
        f"{bogus!r} must not be exempt: {calendar_presence_violations(c)}"

# 23. an `unsuitable` cell that DOES carry a calendar is still clean (the carve permits, never
#     requires, an empty calendar -- so this change cannot break existing filled data).
c = _cell("frost_anchored", "unsuitable", ["growing"] * 12)
assert calendar_presence_violations(c) == [], calendar_presence_violations(c)

print("coverage_floor_gate: unsuitable carve-out tests passed")
