#!/usr/bin/env python3
"""Tests for the herbaceous_perennial structural cert branch (asparagus GS arc, 2026-07-23).
Run: python3 tools/test_herbaceous_perennial_gate.py

Invariants (docs/superpowers/specs/2026-07-23-asparagus-herbaceous-perennial-archetype-design.md):
  - fires ONLY for archetype == 'herbaceous_perennial' (no-op otherwise -- keeps the 119 certified,
    incl. the herbaceous herbs chives/mint on culinary_herb, untouched).
  - perennial true; lifecycle in {perennial, permanent}; succession_policy.suitable False + reason;
    establishment fields sane (years_to_first_harvest non-empty min>=1, years_to_full_production
    non-empty, productive_lifespan_years positive int); no succession/second_planting planting
    tracks; per filled cell: suitability in enum + a marginal/unsuitable cell carries a reason note
    + a non-empty calendar (A32 honesty floor); rotation present.
  - a cell with suitability null AND empty calendar is the admission state (skip).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from herbaceous_perennial_gate import herbaceous_perennial_violations, SUITABILITY_ENUM

def well_formed():
    """Minimal valid herbaceous_perennial crop: one thriving + one unsuitable region cell."""
    return {
        "slug": "asparagus-mini", "archetype": "herbaceous_perennial",
        "calendar_basis": "frost_anchored", "perennial": True, "lifecycle": "perennial",
        "succession_policy": {"suitable": False, "reason_seasoned": "A permanent 15-to-20-year bed is established once, never succession-planted."},
        "years_to_first_harvest": [2, 3], "years_to_full_production": [3, 4],
        "productive_lifespan_years": 18, "rotation": "Permanent bed; do not rotate. Choose the site for the long haul.",
        "regions": {
            "northern_tier": {"plantings": [{"track": "perennial", "label": "crowns"}],
                "resolved_by_zone": {"4": {"suitability": "perennializes",
                    "calendar": ["cold_pause","cold_pause","cold_pause","harvest","harvest","harvest",
                                 "growing","growing","growing","growing","cold_pause","cold_pause"]}}},
            "hawaii_tropical": {"plantings": [{"track": "perennial", "label": "crowns"}],
                "resolved_by_zone": {"12": {"suitability": "unsuitable",
                    "suitability_note_seasoned": "Asparagus needs a real winter dormancy it will not get here; it declines instead of perennializing.",
                    "calendar": ["growing","growing","growing","growing","growing","growing",
                                 "growing","growing","growing","growing","growing","growing"]}}}},
    }

# 0. well-formed -> clean
assert herbaceous_perennial_violations(well_formed()) == [], herbaceous_perennial_violations(well_formed())

# 1. off-archetype -> NO-OP even with garbage (chives-style herb stays untouched)
off = {"slug": "chives", "archetype": "culinary_herb", "calendar_basis": "frost_anchored",
       "perennial": True, "lifecycle": "perennial", "regions": {}}
assert herbaceous_perennial_violations(off) == [], "non-herbaceous_perennial crop must be a no-op"

# 2. ADMISSION STATE: unfilled shell cell (suitability null, calendar []) -> skipped
c = well_formed()
c["regions"]["northern_tier"]["resolved_by_zone"]["4"] = {"suitability": None, "calendar": []}
assert herbaceous_perennial_violations(c) == [], herbaceous_perennial_violations(c)

# 3. perennial not true -> violation
c = well_formed(); c["perennial"] = False
assert any("perennial" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 4. lifecycle annual -> violation
c = well_formed(); c["lifecycle"] = "annual"
assert any("lifecycle" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 5. succession suitable true -> violation
c = well_formed(); c["succession_policy"]["suitable"] = True
assert any("succession" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 5b. succession suppressed but no reason -> violation
c = well_formed(); c["succession_policy"]["reason_seasoned"] = None
assert any("reason_seasoned" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6. empty years_to_first_harvest -> violation
c = well_formed(); c["years_to_first_harvest"] = []
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6b. years_to_first_harvest min 0 (no real establishment lag) -> violation
c = well_formed(); c["years_to_first_harvest"] = [0]
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 6c. productive_lifespan_years null -> violation
c = well_formed(); c["productive_lifespan_years"] = None
assert any("productive_lifespan_years" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 7. a succession planting track -> violation
c = well_formed(); c["regions"]["northern_tier"]["plantings"].append({"track": "succession", "label": "fill"})
assert any("succession" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 8. bad suitability enum on a filled cell -> violation. This probe USED to be `annual_only`,
#    which the artichoke arc considered and declined (design-decisions B.6: a frontend-visible
#    vocabulary change with no renderer support). It became legal on 2026-07-28 by a ruling and a
#    renderer change, which is exactly the route the old comment demanded -- "if it ever becomes
#    legal it must be by a ruling, not by drift." Probe swapped to a value that is still illegal,
#    so the reject branch stays covered.
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = "grows_ok"
assert any("suitability" in v and "grows_ok" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 9. unsuitable cell missing the reason note -> violation
c = well_formed(); c["regions"]["hawaii_tropical"]["resolved_by_zone"]["12"].pop("suitability_note_seasoned")
assert any("hawaii_tropical" in v and "12" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 10. a suitability-marked cell with an EMPTY calendar (A32 honesty floor) -> violation
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["calendar"] = []
assert any("northern_tier" in v and "calendar" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 11. rotation missing -> violation
c = well_formed(); c["rotation"] = None
assert any("rotation" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 12. years_to_first_harvest = [True] -> violation (bool is an int subclass; guard must reject it)
c = well_formed(); c["years_to_first_harvest"] = [True]
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 13. productive_lifespan_years = True -> violation (bool is an int subclass; guard must reject it)
c = well_formed(); c["productive_lifespan_years"] = True
assert any("productive_lifespan_years" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 14. empty years_to_full_production -> violation
c = well_formed(); c["years_to_full_production"] = []
assert any("years_to_full_production" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 15. a second_planting planting track -> violation (sibling of succession, same enum)
c = well_formed(); c["regions"]["northern_tier"]["plantings"].append({"track": "second_planting", "label": "fill"})
assert any("second_planting" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# 16. lifecycle permanent -> VALID (proves the accepted-value branch, not just the reject branch)
c = well_formed(); c["lifecycle"] = "permanent"
assert herbaceous_perennial_violations(c) == [], herbaceous_perennial_violations(c)

# 17. non-list years_to_first_harvest (None) -> violation
c = well_formed(); c["years_to_first_harvest"] = None
assert any("years_to_first_harvest" in v for v in herbaceous_perennial_violations(c)), herbaceous_perennial_violations(c)

# ---------------------------------------------------------------------------------------------
# 18-22. THE ENUM IS THE ROSTER'S FIVE VALUES, not three (artichoke GS arc, 2026-07-28).
#
# WHY. This gate shipped with a three-value vocabulary because asparagus only ever needed three.
# The roster actually publishes FIVE, measured on canonical ea3636e7: fruits_reliably 292,
# marginal 180, unsuitable 165, survives_no_fruit 118, perennializes 25. The two the gate did not
# know about are not new -- `survives_no_fruit` is authored on 118 cells across 17 crops and has a
# RULED display behavior (flagged ornamental-only: "the plant lives and gives you no food, someone
# may still want it"). A crop joining this archetype could not reach for either one.
#
# Artichoke is the case that needed it. In the tropics UF/IFAS's mechanism is that plants STAY
# VEGETATIVE and never initiate buds -- the plant thrives and simply gives no artichokes, which is
# `survives_no_fruit` exactly. Rating it `unsuitable` would hide a cell about a plant that grows
# perfectly well there.
#
# This widens an enum, so the tests that matter are the ones proving it still REJECTS. #8 above
# (annual_only) and #21 below are those.
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"].update(
    {"suitability": "survives_no_fruit",
     "suitability_note_seasoned": "The plant grows well and never sets a bud, so it is foliage only."})
assert herbaceous_perennial_violations(c) == [], herbaceous_perennial_violations(c)

# 19. fruits_reliably accepted too -- admitted for symmetry so the archetype can express the whole
#     roster vocabulary rather than a subset that happens to fit one crop.
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = "fruits_reliably"
assert herbaceous_perennial_violations(c) == [], herbaceous_perennial_violations(c)

# 20. survives_no_fruit REQUIRES the seasoned note. "This plant will live and give you nothing to
#     eat" is a stronger claim than `marginal`, not a weaker one, so it joins the note-bearing set
#     rather than riding in as a free pass alongside the positive verdicts.
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = "survives_no_fruit"
v = herbaceous_perennial_violations(c)
assert any("northern_tier" in x and "suitability_note_seasoned" in x for x in v), v

# 21. ADVERSARIAL: the widened enum must still bite. A near-miss spelling of a LEGAL value is the
#     realistic defect (a typo in an authoring script, not an invented word), and it must bounce.
for bogus in ("survives_no_fruits", "SURVIVES_NO_FRUIT", "fruits_reliable", "no_fruit", ""):
    c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = bogus
    v = herbaceous_perennial_violations(c)
    assert any("suitability" in x and "not in" in x for x in v), (bogus, v)

# 22. fruits_reliably needs NO note -- it is a positive verdict, the parallel of perennializes.
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = "fruits_reliably"
assert not any("suitability_note_seasoned" in x for x in herbaceous_perennial_violations(c))

# 24-26. `annual_only` -- the SIXTH value (2026-07-28, Trevor's call).
#
# A perennial that is a dependable ANNUAL in this zone. `marginal` was carrying these
# cells and it undersells them: it answers "does the planting persist" with a shrug, when
# the honest answer is "no, and it crops well anyway, so replant". 22 of artichoke's cells
# are that, and the value was declined at cert ONLY because the renderers did not know it.
# plant-app now does (commit bc2c809: its own display state, its own "Replant each year"
# flag, and the zone now outranks the archetype for the grown-as pill), so the blocker is
# gone and the data can say what is true.
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"].update(
    {"suitability": "annual_only",
     "suitability_note_seasoned": "Grown as an annual here; the crown does not survive winter."})
assert herbaceous_perennial_violations(c) == [], herbaceous_perennial_violations(c)

# 25. it REQUIRES the seasoned note, and that is the entire point of the value. These cells
#     carry the one instruction a grower cannot infer -- replant each spring -- and a bare
#     downgrade with no reason would be worse than the `marginal` it replaces.
c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = "annual_only"
v = herbaceous_perennial_violations(c)
assert any("northern_tier" in x and "suitability_note_seasoned" in x for x in v), v

# 26. near-miss spellings still bounce -- widening the enum must not soften it.
for bogus in ("annual", "annual-only", "ANNUAL_ONLY", "annuals_only", "annual_culture"):
    c = well_formed(); c["regions"]["northern_tier"]["resolved_by_zone"]["4"]["suitability"] = bogus
    v = herbaceous_perennial_violations(c)
    assert any("suitability" in x and "not in" in x for x in v), (bogus, v)

assert SUITABILITY_ENUM == {"perennializes", "marginal", "unsuitable", "annual_only",
                            "survives_no_fruit", "fruits_reliably"}, SUITABILITY_ENUM

# 23. REAL-DATA REGRESSION: asparagus, the only crop on the archetype today, stays clean. Widening
#     an enum cannot break existing data, but the note requirement added in #20 could have, so this
#     is the check that earns the change rather than assuming it.
import json  # noqa: E402
_here = os.path.dirname(os.path.abspath(__file__))
_data = json.load(open(os.path.join(_here, "..", "crops_data_final.json"), encoding="utf-8"))
_seen = 0
for _c in _data["crops"]:
    if _c.get("archetype") == "herbaceous_perennial":
        _seen += 1
        assert herbaceous_perennial_violations(_c) == [], (_c.get("slug"), herbaceous_perennial_violations(_c))
assert _seen >= 1, "expected at least asparagus on the archetype"

print("herbaceous_perennial_gate: all tests passed")
