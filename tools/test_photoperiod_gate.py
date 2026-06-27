#!/usr/bin/env python3
"""Tests for the photoperiod (day-length) cert-gate branch -- the A9 invariants for a
photoperiod-gated crop (onion, anchor 12; the allium family inherits it). Run:
python3 tools/test_photoperiod_gate.py

Invariants (onion-photoperiod-model-design.md; gold-standard arc A9):
  - fires ONLY for a crop with "photoperiod" in gating_factors (no-op otherwise).
  - VARIETY TYPING: every varieties.recommended[] entry is an object with a valid
    day_length_type in {long_day, intermediate_day, short_day}.
  - CELL TYPING: every FILLED resolved cell's recommended_day_length_type is valid; a
    null cell is the Step-3.5 admission state (skipped -- A2 owns region-fill).
  - COVERAGE INVARIANT: every day-length type a region RESOLVES to has >=1 recommended
    variety carrying that type (no "grow short-day here" with zero short-day varieties).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from photoperiod_gate import photoperiod_violations, DAY_LENGTH_ENUM


def well_formed_photoperiod():
    """Minimal valid photoperiod crop: 3 typed varieties spanning the enum; filled cells
    resolving only to types that have a matching variety."""
    return {
        "slug": "onion-mini",
        "calendar_basis": "frost_anchored",
        "gating_factors": ["photoperiod"],
        "varieties": {"recommended": [
            {"name": "Walla Walla", "day_length_type": "long_day"},
            {"name": "Candy", "day_length_type": "intermediate_day"},
            {"name": "Texas 1015Y", "day_length_type": "short_day"}]},
        "regions": {
            "northern_tier": {"resolved_by_zone": {
                "3": {"recommended_day_length_type": "long_day"},
                "5": {"recommended_day_length_type": "long_day"}}},
            "se_gulf": {"resolved_by_zone": {
                "9": {"recommended_day_length_type": "short_day"}}},
            "ca_interior": {"resolved_by_zone": {
                "8": {"recommended_day_length_type": "intermediate_day"}}}},
    }


def shell_admission():
    """Step-3.5 admission state: varieties typed (from Steps 1-3), but every cell's
    recommended_day_length_type is still null (Step 4 fills it). Must be a no-op."""
    c = well_formed_photoperiod()
    for r in c["regions"].values():
        for cell in r["resolved_by_zone"].values():
            cell["recommended_day_length_type"] = None
    return c


# 0. the well-formed crop -> no violations
assert photoperiod_violations(well_formed_photoperiod()) == [], photoperiod_violations(well_formed_photoperiod())

# 1. a crop WITHOUT photoperiod in gating_factors AND WITHOUT day-length machinery -> NO-OP.
# (A real non-photoperiod crop -- carrot, tomato -- carries no day_length_type fields at all.
# Note: a non-photoperiod crop that DOES carry day-length machinery is the C5 token-drop attack
# below, no longer a no-op -- see tests 16-18.)
non_photo = {"slug": "carrot", "calendar_basis": "frost_anchored", "gating_factors": [],
             "varieties": {"recommended": ["Nantes types", "Danvers"]},
             "regions": {"se_gulf": {"resolved_by_zone": {"9": {"suitability": "good"}}}}}
assert photoperiod_violations(non_photo) == [], "non-photoperiod crop (no machinery) must be a no-op"
# also no-op when gating_factors is missing entirely (and no machinery)
assert photoperiod_violations({"slug": "x", "varieties": {"recommended": [123]}}) == [], "missing gating_factors -> no-op"

# 2. a variety with a bad day_length_type -> violation
c = well_formed_photoperiod()
c["varieties"]["recommended"][0]["day_length_type"] = "medium_day"
assert any("day_length_type" in v and "medium_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 3. a bare-string variety (not the object shape) -> violation
c = well_formed_photoperiod()
c["varieties"]["recommended"][1] = "Candy (intermediate)"
assert any("recommended[1]" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 4. a FILLED cell with a bad recommended_day_length_type -> violation
c = well_formed_photoperiod()
c["regions"]["se_gulf"]["resolved_by_zone"]["9"]["recommended_day_length_type"] = "winter_day"
assert any("se_gulf" in v and "9" in v and "winter_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 5. Step-3.5 ADMISSION STATE: all cells null -> NO-OP (the load-bearing mid-arc case)
assert photoperiod_violations(shell_admission()) == [], photoperiod_violations(shell_admission())

# 6. COVERAGE GAP: a cell resolves to short_day but no recommended variety is short_day -> violation
c = well_formed_photoperiod()
c["varieties"]["recommended"] = [v for v in c["varieties"]["recommended"] if v["day_length_type"] != "short_day"]
assert any("coverage" in v.lower() and "short_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 7. COVERAGE satisfied with EXTRA varieties (more varieties than resolved types) -> clean
c = well_formed_photoperiod()
c["varieties"]["recommended"].append({"name": "Red Burgundy", "day_length_type": "short_day"})
assert photoperiod_violations(c) == [], photoperiod_violations(c)

# 8. the enum is exactly the 3 classes (day-neutral folds into intermediate_day)
assert DAY_LENGTH_ENUM == {"long_day", "intermediate_day", "short_day"}, DAY_LENGTH_ENUM


# ============ B4: WINDOW FIT (day_length_type <-> planting-season shape) ============
# A9 typed + covered the day-length classes but never linked a cell's day_length_type to
# its PLANTING-WINDOW shape, so a short-day onion with a long-day-shaped (spring) schedule
# passed (audit B4). Onion's real cells are the 0-FP corpus:
#   long_day        -> SPRING-planted (Mar-Jun), NOT fall (bulbs in summer's long days).
#   short_day       -> FALL/WINTER-planted (Sep-Feb), NOT spring/summer (bulbs as short
#                      winter days lengthen).
#   intermediate_day-> fall-to-early-spring (Sep-Mar), NOT late-spring/summer.
# Keyed on plant_out only; harvest shape is intentionally NOT checked (overstated harvest
# displays would false-positive -- the broccoli/annual lesson). A cell with no parseable
# plant_out is skipped (the window-fit gate does not own "plant_out must exist").

def windows_crop():
    """Photoperiod crop with FILLED cells whose plant_out windows FIT their type; the
    intermediate cell exercises the 'early/mid/late <Month>' normalization."""
    return {
        "slug": "onion-win",
        "calendar_basis": "frost_anchored",
        "gating_factors": ["photoperiod"],
        "varieties": {"recommended": [
            {"name": "Walla Walla", "day_length_type": "long_day"},
            {"name": "Candy", "day_length_type": "intermediate_day"},
            {"name": "Texas 1015Y", "day_length_type": "short_day"}]},
        "regions": {
            "northern_tier": {"resolved_by_zone": {
                "5": {"recommended_day_length_type": "long_day", "plant_out": "Apr 1 - Apr 22"}}},
            "se_gulf": {"resolved_by_zone": {
                "9": {"recommended_day_length_type": "short_day", "plant_out": "Nov 1 - Feb 15"}}},
            "ca_interior": {"resolved_by_zone": {
                "8": {"recommended_day_length_type": "intermediate_day",
                      "plant_out": "Oct - Nov, Jan - early March"}}}},
    }

# 9. CLEAN window fit (incl. 'Jan - early March' normalization) -> no violations.
assert photoperiod_violations(windows_crop()) == [], photoperiod_violations(windows_crop())

# 10. DEFECT: long_day planted in FALL -> violation.
c = windows_crop()
c["regions"]["northern_tier"]["resolved_by_zone"]["5"]["plant_out"] = "Oct - Nov"
assert any("northern_tier" in v and "long_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 11. DEFECT: long_day with a winter-only (Jan) schedule, no spring -> violation (audit B4 injection).
c = windows_crop()
c["regions"]["northern_tier"]["resolved_by_zone"]["5"]["plant_out"] = "Jan 1 - Jan 15"
assert any("northern_tier" in v and "long_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 12. DEFECT: short_day planted in SPRING (long-day-shaped) -> violation.
c = windows_crop()
c["regions"]["se_gulf"]["resolved_by_zone"]["9"]["plant_out"] = "Apr - May"
assert any("se_gulf" in v and "short_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 13. DEFECT: intermediate_day planted in summer -> violation.
c = windows_crop()
c["regions"]["ca_interior"]["resolved_by_zone"]["8"]["plant_out"] = "Jun - Jul"
assert any("ca_interior" in v and "intermediate_day" in v for v in photoperiod_violations(c)), photoperiod_violations(c)

# 14. SKIP: a filled cell with no parseable plant_out -> no window-fit violation from it.
c = windows_crop()
del c["regions"]["se_gulf"]["resolved_by_zone"]["9"]["plant_out"]
assert photoperiod_violations(c) == [], ("missing plant_out should skip window-fit", photoperiod_violations(c))

# 15. REAL DATA: onion (the only photoperiod crop) has 0 window-fit violations.
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
if os.path.exists(_path):
    import json
    _data = json.load(open(_path))
    _onion = next((c for c in _data["crops"] if c["slug"] == "onion"), None)
    assert _onion is not None, "onion not found"
    assert photoperiod_violations(_onion) == [], ("onion window-fit FP", photoperiod_violations(_onion))
    print("  window-fit: 0 FP across onion's 20 real cells: PASS")

# ============ incognito-redteam C5: token-drop + null-cell-type evasions ============
# (a) Drop "photoperiod" from gating_factors and the WHOLE gate no-ops while the day_length
#     machinery (variety types, cell types) remains -> an invalid type ships. The gate must
#     require the token whenever NON-NULL day-length machinery is present.
# (b) Null a single FILLED cell's recommended_day_length_type to evade coverage + window-fit
#     while it still renders a calendar. The null-skip is only legitimate for an UNFILLED cell.

# 16. token-drop, variety machinery remains -> violation (the gate would otherwise no-op)
c = well_formed_photoperiod(); c["gating_factors"] = []
assert any("photoperiod" in v and "gating_factors" in v for v in photoperiod_violations(c)), \
    f"C5a: variety day_length_type present but token dropped must flag: {photoperiod_violations(c)}"

# 17. token-drop, CELL machinery remains (no variety types) -> violation
c = {"slug": "x", "gating_factors": ["cold_hardiness"],
     "varieties": {"recommended": [{"name": "v"}]},
     "regions": {"se_gulf": {"resolved_by_zone": {"9": {"recommended_day_length_type": "short_day"}}}}}
assert any("photoperiod" in v and "gating_factors" in v for v in photoperiod_violations(c)), \
    f"C5a: cell recommended_day_length_type present but token dropped must flag: {photoperiod_violations(c)}"

# 18. token dropped AND an invalid type would have shipped -> still flagged (the gate is not no-op'd)
c = well_formed_photoperiod(); c["gating_factors"] = []
c["varieties"]["recommended"][0]["day_length_type"] = "banana"
assert photoperiod_violations(c), "C5a: a token-dropped crop with a bogus type must not ship clean"

# 19. null type on a FILLED cell (carries a calendar) -> coverage evasion, violation
c = well_formed_photoperiod()
cell = c["regions"]["se_gulf"]["resolved_by_zone"]["9"]
cell["recommended_day_length_type"] = None
cell["calendar"] = ["growing", "growing", "harvest"]  # it still renders
assert any("se_gulf" in v and "9" in v and "null" in v.lower() for v in photoperiod_violations(c)), \
    f"C5b: null type on a calendar-bearing cell must flag: {photoperiod_violations(c)}"

# 20. REGRESSION: null type on an UNFILLED cell (no calendar) stays a no-op (Step-3.5 admission)
c = well_formed_photoperiod()
cell = c["regions"]["se_gulf"]["resolved_by_zone"]["9"]
cell["recommended_day_length_type"] = None  # no calendar key -> genuinely unfilled
# se_gulf no longer resolves short_day; remove the short_day variety so coverage stays satisfied
c["varieties"]["recommended"] = [v for v in c["varieties"]["recommended"]
                                 if v["day_length_type"] != "short_day"]
assert photoperiod_violations(c) == [], \
    f"C5b regression: null type on an UNFILLED cell must remain a no-op: {photoperiod_violations(c)}"

# 21. REGRESSION: real onion (token present, all 20 cells filled+typed) -> still 0 violations.
# (covered by test 15's real-data load above; re-assert here for the C5 changes.)
if os.path.exists(_path):
    assert photoperiod_violations(_onion) == [], ("C5: onion FP", photoperiod_violations(_onion))

print("photoperiod_gate: all tests passed")
