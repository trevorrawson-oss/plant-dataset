#!/usr/bin/env python3
"""Tests for the annual calendar deriver (Step 5.5). Run from repo root:
    python3 tools/test_annual_calendar.py

Ground truth = the certified annuals' resolved cells. The deriver must reproduce
a clean cold-cycle calendar (carrot northern_tier z5) EXACTLY from its windows,
and produce coherent calendars for basil's frost-anchored summer-season cells.

SCOPE (basil archetype + cold multi-cycle): frost-anchored annuals whose harvest
falls inside the frost-free season (summer-centered), explicit `plant_out` OR a
direct-sow first/last-plant envelope, cold_pause winters, year_round cells, and
honoring a DECLARED heat_pause. OUT OF SCOPE for now (documented, not basil):
winter-wrapping harvest (carrot se_gulf "Sep - May") + lettuce-style heat-inverted
two-cool-season cells -- those need the cycle-segmentation extension.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import annual_calendar as ac

# ---------- month parser ----------
assert ac.parse_months("Jun - Sep") == {6, 7, 8, 9}, ac.parse_months("Jun - Sep")
assert ac.parse_months("May - Aug, Oct - Nov") == {5, 6, 7, 8, 10, 11}
assert ac.parse_months("May 8 - May 22") == {5}
assert ac.parse_months("Mar 27 - Apr 10") == {3, 4}
assert ac.parse_months("Mar 15 - Apr 15; Aug 15 - Sep 15") == {3, 4, 8, 9}
assert ac.parse_months("Sep - May") == {9, 10, 11, 12, 1, 2, 3, 4, 5}   # wrap
assert ac.parse_months("Year round") == set(range(1, 13))
assert ac.parse_months(None) == set()
print("  month parser: PASS")

# ---------- GROUND TRUTH: carrot northern_tier z5 (direct-sow envelope, double cycle) ----------
# plant_out None -> plant inferred from first/last_plant envelope MINUS harvest months.
carrot_nt5 = {
    "plant_out": None, "start_indoors": None,
    "first_plant_date": "Mar 25", "last_plant_date": "Aug 17",
    "harvest": "May - Jun, Oct - Nov", "harvest_start": "May 24", "harvest_end": "Nov 14",
}
EXPECT_CARROT_NT5 = ["cold_pause", "cold_pause", "plant", "plant", "harvest", "harvest",
                     "plant", "plant", "growing", "harvest", "harvest", "cold_pause"]
got = ac.derive_annual_calendar(carrot_nt5, calendar_basis="frost_anchored")
assert got == EXPECT_CARROT_NT5, ("carrot NT z5 regression", got)
print("  carrot northern_tier z5 reproduced EXACTLY: PASS")

# ---------- basil northern_tier z5 (explicit plant_out + start_indoors, single summer) ----------
basil_nt5 = {
    "start_indoors": "Mar 27 - Apr 10", "plant_out": "May 8 - May 22",
    "harvest": "Jun - Sep", "harvest_start": "Jun 7", "harvest_end": "Sep 26",
    "first_plant_date": "May 8", "last_plant_date": "May 22",
}
EXPECT_BASIL_NT5 = ["cold_pause", "cold_pause", "indoors", "indoors", "plant", "harvest",
                    "harvest", "harvest", "harvest", "cold_pause", "cold_pause", "cold_pause"]
got = ac.derive_annual_calendar(basil_nt5, calendar_basis="frost_anchored")
assert got == EXPECT_BASIL_NT5, ("basil NT z5", got)
print("  basil northern_tier z5 (explicit plant_out + indoors): PASS")

# ---------- basil se_gulf z9 (double warm-season arm; plant overlaps harvest in Aug) ----------
# plant_out explicit -> authoritative; plant > harvest in the Aug overlap.
basil_seg9 = {
    "plant_out": "Mar 15 - Apr 15; Aug 15 - Sep 15", "start_indoors": None,
    "harvest": "May - Aug, Oct - Nov", "harvest_start": "May 1", "harvest_end": "Nov 15",
    "first_plant_date": "Mar 15", "last_plant_date": "Sep 15",
}
EXPECT_BASIL_SEG9 = ["cold_pause", "cold_pause", "plant", "plant", "harvest", "harvest",
                     "harvest", "plant", "plant", "harvest", "harvest", "cold_pause"]
got = ac.derive_annual_calendar(basil_seg9, calendar_basis="frost_anchored")
assert got == EXPECT_BASIL_SEG9, ("basil se_gulf z9", got)
print("  basil se_gulf z9 (double arm, plant>harvest overlap): PASS")

# ---------- near-year-round cell with a SUMMER lull (fl_peninsula z11): no cold_pause ----------
# harvest wraps Oct->Jan, so January is ACTIVE -> there is NO winter off-season. The Jul/Aug
# inactive gap is a SUMMER lull -> "growing", never "cold_pause" (a season-span model wrongly
# marks it cold_pause). cold_pause is anchored at deep winter (January), not a contiguous span.
fl_z11 = {
    "start_indoors": "Dec 15 - Feb 15", "plant_out": "Feb 1 - Apr 30; Sep 1 - Nov 15",
    "harvest": "Mar - Jun, Oct - Jan", "harvest_start": "Mar 15", "harvest_end": "Jan 15",
    "first_plant_date": "Feb 1", "last_plant_date": "Nov 15",
}
EXPECT_FL_Z11 = ["harvest", "plant", "plant", "plant", "harvest", "harvest",
                 "growing", "growing", "plant", "plant", "plant", "harvest"]
got = ac.derive_annual_calendar(fl_z11, calendar_basis="frost_anchored")
assert "cold_pause" not in got, ("no cold_pause in a January-active near-year-round cell", got)
assert got == EXPECT_FL_Z11, ("fl_peninsula z11 near-year-round", got)
print("  fl_peninsula z11 (near-year-round, summer lull -> growing): PASS")

# ---------- year_round cell (hawaii) -> continuous, no pause ----------
hawaii = {"plant_out": "Year round", "year_round": True,
          "harvest": "Year round", "harvest_start": None, "harvest_end": None}
got = ac.derive_annual_calendar(hawaii, calendar_basis="frost_anchored")
assert got == ["growing"] * 12, ("hawaii year_round", got)
print("  hawaii year_round (continuous): PASS")

# ---------- declared heat_pause overrides (general-case honoring; basil has none) ----------
hp = {"plant_out": "Mar - Apr", "start_indoors": None, "harvest": "May - Sep",
      "harvest_start": "May 1", "harvest_end": "Sep 30", "heat_pause_months": {7, 8}}
got = ac.derive_annual_calendar(hp, calendar_basis="frost_anchored")
assert got[6] == "heat_pause" and got[7] == "heat_pause", ("heat_pause override", got)
assert got[4] == "harvest", got            # May still harvest
print("  declared heat_pause override: PASS")

print("PASS annual_calendar deriver")

# ============ annual_coherence_violations (the always-on gate check) ============
# A coherent frost_anchored cell -> no hard violations, no notes.
clean = {"calendar_basis": "frost_anchored", "regions": {"se_gulf": {"resolved_by_zone": {"8": {
    "calendar": ["cold_pause", "indoors", "plant", "harvest", "harvest", "harvest",
                 "plant", "plant", "harvest", "harvest", "cold_pause", "cold_pause"]}}}}}
h, n = ac.annual_coherence_violations(clean)
assert h == [] and n == [], ("clean cell", h, n)

# A `start_indoors` token (the cherry/beefsteak drift; SuccessionCard reads 'indoors') -> HARD.
drift = {"calendar_basis": "frost_anchored", "regions": {"r": {"resolved_by_zone": {"8": {
    "calendar": ["cold_pause", "start_indoors", "plant", "harvest", "harvest", "harvest",
                 "harvest", "harvest", "harvest", "harvest", "cold_pause", "cold_pause"]}}}}}
h, n = ac.annual_coherence_violations(drift)
assert len(h) == 1 and "start_indoors" in h[0], ("start_indoors caught", h)

# heat_pause.months object disagreeing with the calendar's heat_pause tokens -> HARD.
mis = {"calendar_basis": "frost_anchored", "regions": {"r": {"resolved_by_zone": {"9": {
    "heat_pause": {"months": [7]},
    "calendar": ["plant", "plant", "harvest", "harvest", "harvest", "harvest",
                 "harvest", "heat_pause", "plant", "harvest", "cold_pause", "cold_pause"]}}}}}
h, n = ac.annual_coherence_violations(mis)
assert len(h) == 1 and "heat_pause" in h[0], ("heat_pause misalignment caught", h)

# A `wait` token -> NOTE (surfaced, non-blocking), not a hard violation.
w = {"calendar_basis": "frost_anchored", "regions": {"r": {"resolved_by_zone": {"10": {
    "calendar": ["cold_pause", "wait", "indoors", "plant", "harvest", "harvest",
                 "harvest", "harvest", "harvest", "harvest", "cold_pause", "cold_pause"]}}}}}
h, n = ac.annual_coherence_violations(w)
assert h == [] and len(n) == 1 and "wait" in n[0], ("wait is a note not hard", h, n)

# non-frost_anchored crop -> no-op.
assert ac.annual_coherence_violations({"calendar_basis": "perennial_chill_gated"}) == ([], [])
print("  annual_coherence_violations (always-on gate): PASS")
print("PASS annual_calendar (deriver + coherence gate)")

# ============ annual_calendar_violations (B1: token-PLACEMENT drift gate) ============
# NOT a full re-derive (the deriver cannot reproduce ~190/200 hand-authored cells:
# month-rounding + multi-cycle/winter-wrap/heat-inverted/year-round-with-plant shapes).
# This gates exactly the audit B1 defect classes with empirically zero FPs on all 10
# certified annuals: a PAUSE token must not displace an ACTIVE window.
#   - cold_pause / wait on ANY plant_out month (frost/dormancy cannot coincide with an
#     outdoor planting window at any granularity).
#   - heat_pause on a CORE plant_out or CORE harvest month NOT in declared
#     heat_pause.months (heat abuts planting/harvest at span boundaries via month-
#     rounding, so only a FULLY-covered "core" month is an unambiguous contradiction;
#     a declared heat month is excused -- that is the legitimate summer exclusion).
# Thermal BACKING of a self-consistent-but-unjustified heat_pause is B3, not B1.

def _crop(cell, basis="frost_anchored"):
    return {"calendar_basis": basis, "regions": {"r": {"resolved_by_zone": {"5": cell}}}}

# clean basil-shaped cell (reproduces exactly) -> no placement violations.
clean_cell = {"plant_out": "May 8 - May 22", "harvest": "Jun - Sep",
              "calendar": ["cold_pause", "cold_pause", "indoors", "indoors", "plant",
                           "harvest", "harvest", "harvest", "harvest", "cold_pause",
                           "cold_pause", "cold_pause"]}
assert ac.annual_calendar_violations(_crop(clean_cell)) == [], \
    ("clean cell flagged", ac.annual_calendar_violations(_crop(clean_cell)))

# DEFECT pause-on-plant (cold): cold_pause sitting on a plant_out month.
cold_on_plant = dict(clean_cell, plant_out="Apr 1 - May 31",
                     calendar=["cold_pause", "cold_pause", "indoors", "indoors", "cold_pause",
                               "harvest", "harvest", "harvest", "harvest", "cold_pause",
                               "cold_pause", "cold_pause"])
v = ac.annual_calendar_violations(_crop(cold_on_plant))
assert len(v) == 1 and "cold_pause" in v[0] and "plant" in v[0], ("cold-on-plant not caught", v)

# DEFECT pause-on-plant (wait): wait sitting on a plant_out month.
wait_on_plant = dict(clean_cell, plant_out="May 1 - May 31",
                     calendar=["cold_pause", "cold_pause", "indoors", "indoors", "wait",
                               "harvest", "harvest", "harvest", "harvest", "cold_pause",
                               "cold_pause", "cold_pause"])
v = ac.annual_calendar_violations(_crop(wait_on_plant))
assert len(v) == 1 and "wait" in v[0], ("wait-on-plant not caught", v)

# DEFECT pause-on-harvest (heat): heat_pause on a CORE harvest month, no declared months.
heat_on_harvest = {"plant_out": "Mar - Apr", "harvest": "Jun - Sep",
                   "calendar": ["cold_pause", "cold_pause", "plant", "plant", "growing",
                                "harvest", "heat_pause", "harvest", "harvest", "cold_pause",
                                "cold_pause", "cold_pause"]}
v = ac.annual_calendar_violations(_crop(heat_on_harvest))
assert len(v) == 1 and "heat_pause" in v[0] and "harvest" in v[0], ("heat-on-harvest not caught", v)

# DEFECT pause-on-plant (heat): heat_pause on a CORE plant_out month, no declared months.
heat_on_plant = {"plant_out": "Apr - Jun", "harvest": "Aug - Sep",
                 "calendar": ["cold_pause", "cold_pause", "plant", "plant", "heat_pause",
                              "plant", "growing", "harvest", "harvest", "cold_pause",
                              "cold_pause", "cold_pause"]}
v = ac.annual_calendar_violations(_crop(heat_on_plant))
assert len(v) == 1 and "heat_pause" in v[0] and "plant" in v[0], ("heat-on-plant not caught", v)

# LEGIT: heat_pause on a BOUNDARY harvest month, no object (zucchini se_gulf shape).
# harvest "May 25 - Jul 10" -> Jul only partly covered -> NOT core -> not flagged.
boundary_heat = {"plant_out": "Apr 1 - May 15, Aug 1 - Aug 20", "harvest": "May 25 - Jul 10, Sep 25 - Nov 5",
                 "calendar": ["cold_pause", "cold_pause", "indoors", "plant", "plant",
                              "harvest", "heat_pause", "plant", "harvest", "harvest",
                              "harvest", "cold_pause"]}
assert ac.annual_calendar_violations(_crop(boundary_heat)) == [], \
    ("boundary heat_pause false-positived", ac.annual_calendar_violations(_crop(boundary_heat)))

# LEGIT: heat_pause DECLARED on a core harvest month (desert tomato shape) -> excused.
declared_heat = {"plant_out": "Sep - Sep", "harvest": "Feb - Jun", "heat_pause": {"months": [6]},
                 "calendar": ["growing", "harvest", "harvest", "harvest", "harvest", "heat_pause",
                              "heat_pause", "heat_pause", "plant", "growing", "harvest", "plant"]}
declared_heat["heat_pause"]["months"] = [6, 7, 8]
assert ac.annual_calendar_violations(_crop(declared_heat)) == [], \
    ("declared heat_pause flagged", ac.annual_calendar_violations(_crop(declared_heat)))

# DEFECT (GATE-UNLOCK 2026-06-26): cold_pause on a CORE harvest month -- the old broccoli nt.z7
# over-stated-continuous-harvest shape (a 3-month summer cold_pause sitting inside an "Apr 26 - Dec 4"
# harvest display). Now that the certified data is corrected (the summer gap relabeled heat_pause +
# the harvest split), this contradiction is FLAGGED. Was deliberately tolerated before the fix.
cold_on_harvest = {"plant_out": "Feb 22 - Mar 15", "harvest": "Apr 26 - Dec 4",
                   "calendar": ["cold_pause", "plant", "plant", "harvest", "harvest", "cold_pause",
                                "cold_pause", "cold_pause", "plant", "growing", "harvest", "harvest"]}
v = ac.annual_calendar_violations(_crop(cold_on_harvest))
assert any("cold_pause" in x and "harvest" in x for x in v), ("cold-on-core-harvest not caught", v)

# LEGIT: cold_pause on a PARTIAL boundary harvest month (the frost tail clips in) -> NOT flagged.
# harvest "May 1 - Nov 5" -> Nov only partly covered -> NOT core -> the Nov cold_pause is month-rounding.
cold_boundary = {"plant_out": "Mar - Apr", "harvest": "May 1 - Nov 5",
                 "calendar": ["cold_pause", "cold_pause", "plant", "plant", "harvest", "harvest",
                              "harvest", "harvest", "harvest", "harvest", "cold_pause", "cold_pause"]}
assert ac.annual_calendar_violations(_crop(cold_boundary)) == [], \
    ("boundary cold_pause false-positived", ac.annual_calendar_violations(_crop(cold_boundary)))

# no-op for non-frost_anchored crops.
assert ac.annual_calendar_violations({"calendar_basis": "perennial_chill_gated"}) == []
print("  annual_calendar_violations (B1 placement gate, unit): PASS")

# REAL-DATA GUARD: zero false positives across every certified frost_anchored annual.
_path = os.path.join(HERE, "..", "crops_data_final.json")
if os.path.exists(_path):
    _data = json.load(open(_path))
    def _certified(c):
        v = c.get("verification_status") or {}
        return (v.get("status") == "verified_gs_arc"
                and v.get("launch_ready_core") and v.get("launch_ready_seasoned"))
    _annuals = [c for c in _data["crops"]
                if c.get("calendar_basis") == "frost_anchored" and _certified(c)]
    assert len(_annuals) >= 10, ("certified annuals unexpectedly few (>=10)", len(_annuals))
    for c in _annuals:
        fp = ac.annual_calendar_violations(c)
        assert fp == [], (f"FALSE POSITIVE on certified annual {c['slug']}", fp)
    print(f"  annual_calendar_violations: 0 FP across {len(_annuals)} certified annuals: PASS")
print("PASS annual_calendar (deriver + coherence gate + B1 placement gate)")

# ============ heat_pause_backing_violations (B3: thermal backing gate) ============
# Closes audit B3: a self-consistent heat_pause (calendar token + matching months) with
# ZERO climate justification ships clean. Heat tolerance is crop+region+zone physiology
# (same desert zone: carrot pauses Mar-Aug while zucchini pauses Jul-Aug), so a heat
# exclusion is backed AT THE CELL, not via a shared climate table. Wherever the calendar
# SHOWS a heat_pause token, the cell must carry a backed heat_pause object:
#   months (non-empty) + basis_seasoned prose + >=1 sources, each source anchored by a
#   URL in anchoring_urls. PRESENCE/SHAPE check only -- month<->calendar ALIGNMENT stays
#   in annual_coherence_violations (A5). No-op for non-frost_anchored crops.

_HP_CAL = ["cold_pause", "cold_pause", "plant", "plant", "harvest", "harvest",
           "heat_pause", "harvest", "harvest", "cold_pause", "cold_pause", "cold_pause"]

def _hp_obj(**over):
    o = {"months": [7], "classification": "heat_pause",
         "basis_seasoned": "Summer sowing gap is a heat exclusion: high night temps fail fruit set.",
         "sources": ["uga_ext"],
         "anchoring_urls": {"uga_ext": {"url": "https://x/c943", "verified": "2026-06-05"}}}
    o.update(over)
    return o

# CLEAN: heat_pause token backed by a full object -> [].
backed = {"harvest": "Jun - Sep", "heat_pause": _hp_obj(), "calendar": list(_HP_CAL)}
assert ac.heat_pause_backing_violations(_crop(backed)) == [], \
    ("backed heat_pause flagged", ac.heat_pause_backing_violations(_crop(backed)))

# DEFECT object-less: a heat_pause token but no heat_pause object (the zucchini/green-beans
# shape today, and the audit's injected token+no-backing) -> 1 violation.
objectless = {"harvest": "Jun - Sep", "calendar": list(_HP_CAL)}
v = ac.heat_pause_backing_violations(_crop(objectless))
assert len(v) == 1 and "heat_pause" in v[0] and "object" in v[0], ("object-less not caught", v)

# DEFECT months missing/empty.
no_months = {"harvest": "Jun - Sep", "heat_pause": _hp_obj(months=[]), "calendar": list(_HP_CAL)}
v = ac.heat_pause_backing_violations(_crop(no_months))
assert len(v) == 1 and "months" in v[0], ("empty months not caught", v)

# DEFECT basis_seasoned prose missing (token + months + source, but no stated reason).
no_basis = {"harvest": "Jun - Sep", "heat_pause": _hp_obj(basis_seasoned="  "), "calendar": list(_HP_CAL)}
v = ac.heat_pause_backing_violations(_crop(no_basis))
assert len(v) == 1 and "basis_seasoned" in v[0], ("missing basis not caught", v)

# DEFECT sources empty (a stated reason but no Tier-1 citation).
no_sources = {"harvest": "Jun - Sep", "heat_pause": _hp_obj(sources=[]), "calendar": list(_HP_CAL)}
v = ac.heat_pause_backing_violations(_crop(no_sources))
assert len(v) == 1 and "source" in v[0], ("empty sources not caught", v)

# DEFECT source key with no anchoring URL (a citation that points nowhere).
unanchored = {"harvest": "Jun - Sep",
              "heat_pause": _hp_obj(sources=["nmsu_ext"], anchoring_urls={}),
              "calendar": list(_HP_CAL)}
v = ac.heat_pause_backing_violations(_crop(unanchored))
assert len(v) == 1 and "nmsu_ext" in v[0] and "anchor" in v[0].lower(), ("unanchored source not caught", v)

# LEGIT: no heat_pause token in the calendar -> no claim shown -> [] (even with a stray object).
no_token = {"harvest": "Jun - Sep", "heat_pause": _hp_obj(),
            "calendar": ["cold_pause", "cold_pause", "plant", "plant", "harvest", "harvest",
                         "harvest", "harvest", "harvest", "cold_pause", "cold_pause", "cold_pause"]}
assert ac.heat_pause_backing_violations(_crop(no_token)) == [], \
    ("no-token cell flagged", ac.heat_pause_backing_violations(_crop(no_token)))

# no-op for non-frost_anchored crops.
assert ac.heat_pause_backing_violations({"calendar_basis": "perennial_chill_gated"}) == []
print("  heat_pause_backing_violations (B3 backing gate, unit): PASS")

# REAL-DATA guard: the Pass-1 heat_pause back-fill HAS LANDED (2026-06-26) -- every certified
# annual that SHOWS a heat_pause token now carries a backed object (months + basis_seasoned +
# anchored source), incl. the 13 formerly object-less zucchini/green-beans cells and broccoli's
# 3 northern_tier cells relabeled cold_pause->heat_pause. 0 = clean; the gate is WIRED.
if os.path.exists(_path):
    _total = sum(len(ac.heat_pause_backing_violations(c)) for c in _annuals)
    assert _total == 0, ("heat_pause backing regressed (was 0 after the Pass-1 back-fill)", _total)
    print(f"  heat_pause_backing_violations: {_total} unbacked across certified annuals (Pass-1 landed): PASS")
print("PASS annual_calendar (deriver + coherence + B1 placement + B3 backing)")
