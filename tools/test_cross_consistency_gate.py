#!/usr/bin/env python3
"""Tests for the cross-consistency truth-layer gate (whole_crop_gate A34; incognito-redteam C7,
the deterministic cross-field layer). Run: python3 tools/test_cross_consistency_gate.py

WHY: the most likely bot failure (C7) is copy-nearest-template-don't-refit -- the crop contradicts
ITSELF. The canonical example: the fabricated crop's PROSE said pH 6.0-7.5 while the structured
`ph.preferred_range` was [3.0, 3.4]. No external truth needed -- the two fields disagree. This gate
cross-checks fields that must agree. RULE 1 (this increment): the pH range stated in
`ph.note_seasoned` / `ph.note_beginner` must match `ph.preferred_range` (every certified anchor
states it exactly; the gate tolerates 0.5 pH units of authoring drift, so it fires only on a real
contradiction). The decimal-required parse skips the "0 to 14 scale" boilerplate.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cross_consistency_gate import cross_consistency_violations

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
_data = json.load(open(_path, encoding="utf-8")) if os.path.exists(_path) else {"crops": []}
_cert = [c for c in _data["crops"]
         if c.get("verification_status", {}).get("status") == "verified_gs_arc"]


def clean():
    return {"slug": "carrot",
            "ph": {"preferred_range": [6.0, 6.8], "tolerated_range": [5.5, 7.0]},
            "ph_extra": None,
            }


def with_note(pref, note):
    return {"slug": "x", "ph": {"preferred_range": pref,
            "note_seasoned": note, "note_beginner": note}}


# 0. a crop with no ph note -> no violation (nothing to cross-check)
assert cross_consistency_violations(clean()) == [], cross_consistency_violations(clean())

# 1. note range matches preferred -> clean
assert cross_consistency_violations(with_note([6.0, 6.8], "Aim for pH 6.0 to 6.8.")) == [], "match -> clean"
assert cross_consistency_violations(with_note([4.5, 5.5], "Blueberries need pH 4.5 to 5.5.")) == [], "acid match -> clean"
assert cross_consistency_violations(with_note([6.0, 7.5], "tolerant across pH 6.0-7.5 range")) == [], "hyphen form -> clean"

# 2. THE C7 contradiction: prose says 6.0 to 7.5, structured is [3.0, 3.4] -> violation
c = with_note([3.0, 3.4], "Aim for a soil pH of 6.0 to 7.5 for best growth.")
v = cross_consistency_violations(c)
assert any("ph" in x.lower() and "note" in x.lower() for x in v), f"C7 pH contradiction must flag: {v}"

# 3. a single-endpoint drift beyond tolerance -> violation (prose 6.0-6.8 vs structured [6.0, 8.5])
c = with_note([6.0, 8.5], "around pH 6.0 to 6.8")
assert cross_consistency_violations(c), "high-end drift > 0.5 must flag"

# 4. within-tolerance drift -> clean (prose 6.0-6.8 vs structured [6.1, 6.9], <=0.5 each)
c = with_note([6.1, 6.9], "roughly pH 6.0 to 6.8")
assert cross_consistency_violations(c) == [], "small authoring drift stays clean"

# 5. the "0 to 14 scale" boilerplate must NOT be parsed as the pH range (no decimals -> skipped)
c = with_note([6.0, 6.8], "Soil pH runs on a scale from 0 to 14; aim for 6.0 to 6.8.")
assert cross_consistency_violations(c) == [], "scale boilerplate must be skipped, real range matches"

# 6. note present but NO parseable range -> skip (a single value 'around 6.5' is not a range)
c = with_note([6.0, 6.8], "Keep the soil slightly acidic, around pH 6.5.")
assert cross_consistency_violations(c) == [], "no parseable range -> no false contradiction"

# ---- re-audit #2 D12: the pH parse must catch INTEGER ranges, and still skip the 0/1-to-14 scale ----
# 6a. INTEGER prose contradiction: "pH 6 to 7" vs structured [3.0,3.4] -> violation (was evaded)
c = with_note([3.0, 3.4], "Aim for pH 6 to 7.")
assert cross_consistency_violations(c), "D12: integer-range prose contradiction must flag"
# 6b. integer prose that MATCHES (orange-navel ships "6 to 7" with [6.0,7.0]) -> clean
c = with_note([6.0, 7.0], "Navel oranges prefer roughly pH 6 to 7.")
assert cross_consistency_violations(c) == [], "matching integer range is clean"
# 6c. the "1 to 14" scale form (cherry-tomato/lettuce ship it) is skipped, real range still checked
c = with_note([6.0, 6.8], "pH runs on a scale of 1 to 14; aim for 6.0 to 6.8.")
assert cross_consistency_violations(c) == [], "the 1-to-14 scale must be skipped"
# 6d. a scale mention with NO real range -> no check (not a false contradiction)
c = with_note([6.0, 6.8], "Soil pH is measured from 0 to 14.")
assert cross_consistency_violations(c) == [], "scale-only note has no range to check"

# 7. preferred_range absent -> skip
assert cross_consistency_violations({"slug": "x", "ph": {"note_seasoned": "pH 6.0 to 6.8"}}) == []

# 8. REAL DATA: every certified anchor's pH prose matches its structured range (0 FP)
fp = [(c["slug"], cross_consistency_violations(c)) for c in _cert if cross_consistency_violations(c)]
assert fp == [], f"cross-consistency FP on certified anchors: {fp}"
if _cert:
    print(f"  real data: 0 FP across {len(_cert)} certified anchors: PASS")

# ---- increment 2, RULE 2 (Trevor: continue increment 2): harvest-requires-plant ----
# A frost_anchored cell that renders a `harvest` token must also carry a plant-class token
# (`plant`/`indoors`) -- you cannot harvest what was never planted. Catches the copy-paste that
# drops the planting tokens (a C7-class self-contradiction). Every frost_anchored cell in the 18
# that harvests also plants (0 FP). No-op off frost_anchored (trees/berries plant once at
# establishment, not in the annual strip).

def _annual_cell(cal):
    return {"slug": "x", "calendar_basis": "frost_anchored",
            "regions": {"se_gulf": {"resolved_by_zone": {"8": {"calendar": cal}}}}}


# 9. a cell with harvest AND plant -> clean
assert cross_consistency_violations(_annual_cell(
    ["cold_pause", "plant", "growing", "harvest", "harvest", "season_over"])) == [], "harvest+plant clean"
# indoors counts as a plant-class token
assert cross_consistency_violations(_annual_cell(
    ["indoors", "plant", "growing", "harvest"])) == [], "indoors+harvest clean"

# 10. a cell with harvest but NO plant-class token -> violation (the dropped-planting defect)
v = cross_consistency_violations(_annual_cell(["growing", "harvest", "harvest", "season_over"]))
assert any("harvest" in m.lower() and "plant" in m.lower() and "se_gulf" in m for m in v), \
    f"harvest with no plant must flag: {v}"

# 11. a cell with NO harvest -> no-op (nothing to check)
assert cross_consistency_violations(_annual_cell(["cold_pause", "growing", "growing"])) == []

# 12. NON-frost_anchored (a tree) with harvest but no plant -> NOT flagged (planted once at establishment)
tree = {"slug": "peach", "calendar_basis": "perennial_chill_gated",
        "regions": {"se_gulf": {"resolved_by_zone": {"8": {"calendar": ["bloom", "harvest", "dormant"]}}}}}
assert cross_consistency_violations(tree) == [], "tree harvest-without-annual-plant is legit"

# 13. REAL DATA still 0 FP after rule 2 (re-assert; the 18 frost_anchored cells all plant+harvest)
fp2 = [(c["slug"], cross_consistency_violations(c)) for c in _cert if cross_consistency_violations(c)]
assert fp2 == [], f"cross-consistency FP after rule 2: {fp2}"

# 14. herbaceous_perennial (asparagus) carve-out: an established permanent bed's steady-state
# calendar renders spring `harvest` + summer `growing` with NO annual plant token -- legit, must NOT
# fire Rule 2 (a permanent bed is planted once at establishment, like trees/berries off frost_anchored).
_hp = {"slug": "asparagus", "calendar_basis": "frost_anchored", "archetype": "herbaceous_perennial",
       "regions": {"northern_tier": {"resolved_by_zone": {"4": {"calendar":
           ["cold_pause","cold_pause","cold_pause","cold_pause","harvest","harvest",
            "growing","growing","growing","growing","cold_pause","cold_pause"]}}}}}
assert cross_consistency_violations(_hp) == [], cross_consistency_violations(_hp)
# 14b. REGRESSION: the SAME harvest-without-plant calendar on a NON-herbaceous_perennial frost_anchored
# crop STILL bounces (the carve-out must not weaken enforcement for annuals).
_ann = dict(_hp, archetype="cool_season_annual")
assert any("plant-class token" in v for v in cross_consistency_violations(_ann)), cross_consistency_violations(_ann)

print("cross_consistency_gate: all tests passed")
