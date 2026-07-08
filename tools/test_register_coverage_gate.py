#!/usr/bin/env python3
"""Tests for the register-coverage HARD gate (register #8). Run:
    python3 tools/test_register_coverage_gate.py

WHY: the register fields (#4 timing spine, #5 watering.schedule_by_stage, #6 germination/seedling
light, #7 climate thresholds) were guarded only SOFTLY -- each field's standalone gate validates shape
WHEN PRESENT, so a newly-certified crop could silently OMIT a whole register set (the backfill-treadmill
the field-register warns about). This gate is the present-or-explicit-null coverage floor (the A17 npk /
A20 display-readiness pattern extended to the register fields): every certified crop
(verification_status.status == 'verified_gs_arc') must carry each shipped register field OR its defined
null/N-A. Uncertified §E shells are exempt; the per-field N-A predicates are REUSED from the standalone
gates (timing_spine_gate.dtm_empty / is_microgreen / SEED_LIKE, climate_threshold_gate.INDOOR_SLUGS).

Each assertion sneaks ONE defect class at the gate -- a certified crop MISSING a required field (not its
null/N-A) -- and confirms it bounces; the field-or-null case and the legit-N/A archetypes stay green; an
uncertified shell is exempt. The final block injects the defect into a SCRATCH COPY of the REAL canonical
and confirms the CLI bounces, and confirms the clean canonical is GREEN (all 114 carry all four sets).
See docs/kickoffs/13-register-coverage-gate.md, docs/field_addition_register.md #8.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from register_coverage_gate import register_coverage_violations, is_certified


# ---------------------------------------------------------------- clean / N-A fixtures (-> no violations)
def full_annual():
    """A fully-covered certified annual (tomato-like): every register field or its value present."""
    return {
        "slug": "cherry-tomato",
        "verification_status": {"status": "verified_gs_arc"},
        "propagule": "seed",
        "days_to_maturity": [60, 80],
        "spacing_inches": [18, 24],
        "dtm_anchor": "from_transplant",
        "sow_depth_inches": [0.25, 0.5],
        "watering": {"schedule_by_stage": [{"stage": "seedling"}]},
        "germination_light": "neutral",
        "seedling_light": "bright_default",
        "heat_threshold_f": 92,
        "frost_tolerance_f": 32,
        "chilling_sensitivity_f": 50,
        "tray_sowing": "multi_sow_thin_to_one",   # #9: present-or-na (na is a present value)
        "pot_up": "recommended",
    }


def transplant_annual():
    """pepper-like: transplant propagule (NOT seed-like) -> sow_depth is legitimately absent."""
    c = full_annual()
    c["slug"] = "bell-pepper"
    c["propagule"] = "transplant"
    del c["sow_depth_inches"]        # N-A: only seed-like propagules require a sowing depth
    return c


def empty_dtm_perennial():
    """apple-like: empty DTM -> no dtm_anchor + no ladder (N-A); non-seed-like -> no sow_depth;
    germination_light null (no home-from-seed path) + chilling null (cold-adapted) are PRESENT values."""
    return {
        "slug": "apple",
        "verification_status": {"status": "verified_gs_arc"},
        "propagule": "bare_root",
        "days_to_maturity": [],          # empty -> dtm_anchor N-A
        "spacing_inches": [15, 20],
        # no dtm_anchor, no sow_depth -- both legitimately N-A for this archetype
        "watering": {"schedule_by_stage": [{"stage": "establishment"}]},
        "germination_light": None,       # N-A: null is a PRESENT value (key exists)
        "seedling_light": "na",
        "heat_threshold_f": 95,
        "frost_tolerance_f": 28,
        "chilling_sensitivity_f": None,  # N-A: null is a PRESENT value
        "tray_sowing": "na",             # #9: 'na' is a present value (nursery stock, no tray phase)
    }


def microgreen():
    """microgreens-mix: INDOOR_SLUGS -> climate thresholds N-A; spacing==[] -> sow_depth N-A."""
    return {
        "slug": "microgreens-mix",
        "verification_status": {"status": "verified_gs_arc"},
        "propagule": "seed",
        "days_to_maturity": [10, 14],    # non-empty -> dtm_anchor required (present below)
        "spacing_inches": [],            # microgreen -> sow_depth N-A
        "dtm_anchor": "from_sow",
        "watering": {"schedule_by_stage": [{"stage": "germination"}]},
        "germination_light": "neutral",
        "seedling_light": "blackout_then_bright",
        "tray_sowing": "na",             # #9: microgreens are 'na' (broadcast mat, no cells)
        # no climate fields -- INDOOR_SLUGS are N-A-indoor
    }


def heat_lover():
    """okra-like: heat_threshold_f null (heat-lover, present value) -- still green."""
    c = full_annual()
    c["slug"] = "okra"
    c["heat_threshold_f"] = None         # N-A: null present value
    return c


def uncertified_shell():
    """An uncertified §E shell (olive-like) carrying NONE of the register fields -> exempt (green)."""
    return {"slug": "olive", "verification_status": {"status": None}, "propagule": None}


CLEAN = (full_annual, transplant_annual, empty_dtm_perennial, microgreen, heat_lover, uncertified_shell)
for f in CLEAN:
    assert register_coverage_violations(f()) == [], (f.__name__, register_coverage_violations(f()))

# a crop with NO verification_status at all is not certified -> exempt
assert register_coverage_violations({"slug": "bare"}) == []
assert is_certified(full_annual()) and not is_certified(uncertified_shell())


# ---------------------------------------------------------------- defect injections (-> violation)
def _missing(field, sub=None):
    """full_annual with one required field removed (top-level, or watering.schedule_by_stage)."""
    c = full_annual()
    if sub is None:
        del c[field]
    else:
        del c[field][sub]
    return c


# #4 timing spine
c = _missing("propagule")
assert any("propagule" in v for v in register_coverage_violations(c)), register_coverage_violations(c)
c = _missing("dtm_anchor")   # non-empty DTM -> anchor IS required
assert any("dtm_anchor" in v for v in register_coverage_violations(c)), register_coverage_violations(c)
c = _missing("sow_depth_inches")   # seed propagule, not microgreen -> depth required
assert any("sow_depth" in v for v in register_coverage_violations(c)), register_coverage_violations(c)

# #5 watering
c = _missing("watering", "schedule_by_stage")
assert any("schedule_by_stage" in v for v in register_coverage_violations(c)), register_coverage_violations(c)
c = full_annual(); c["watering"]["schedule_by_stage"] = []   # present but EMPTY -> still a gap
assert any("schedule_by_stage" in v for v in register_coverage_violations(c)), register_coverage_violations(c)

# #6 germination / seedling light
c = _missing("germination_light")
assert any("germination_light" in v for v in register_coverage_violations(c)), register_coverage_violations(c)
c = _missing("seedling_light")
assert any("seedling_light" in v for v in register_coverage_violations(c)), register_coverage_violations(c)

# #7 climate thresholds (non-indoor)
for f in ("heat_threshold_f", "frost_tolerance_f", "chilling_sensitivity_f"):
    c = _missing(f)
    assert any(f in v for v in register_coverage_violations(c)), (f, register_coverage_violations(c))

# #9 seed-tray protocol (present-or-na; na is a present value, so require the KEY)
c = _missing("tray_sowing")
assert any("tray_sowing" in v for v in register_coverage_violations(c)), register_coverage_violations(c)
# a certified crop carrying tray_sowing == 'na' is CLEAN (na is a present value, like a null germination_light)
c = full_annual(); c["tray_sowing"] = "na"; c.pop("pot_up", None)
assert not any("tray_sowing" in v for v in register_coverage_violations(c)), register_coverage_violations(c)


# ---------------------------------------------------------------- N-A must NOT be forced (green)
# empty-DTM perennial missing dtm_anchor/sow_depth is CLEAN (already asserted above), but prove the
# gate does not blindly demand them: a perennial WITH a spurious removal of climate still only flags climate.
c = empty_dtm_perennial(); del c["heat_threshold_f"]
v = register_coverage_violations(c)
assert any("heat_threshold_f" in x for x in v) and not any("dtm_anchor" in x for x in v), v

# a microgreen is NOT asked for climate fields even though it is certified
c = microgreen()
assert register_coverage_violations(c) == [], register_coverage_violations(c)
# ...but a microgreen missing seedling_light IS flagged (#6 is in-scope for indoor crops)
c = microgreen(); del c["seedling_light"]
assert any("seedling_light" in x for x in register_coverage_violations(c)), register_coverage_violations(c)

# an UNCERTIFIED crop missing everything is never flagged (exempt)
c = full_annual(); c["verification_status"]["status"] = None
for k in ("propagule", "dtm_anchor", "germination_light", "heat_threshold_f"):
    c.pop(k, None)
assert register_coverage_violations(c) == [], register_coverage_violations(c)


# ---------------------------------------------------------------- REAL canonical (SCRATCH-COPY defect + green)
_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "register_coverage_gate.py")
_WHOLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whole_crop_gate.py")
_CANON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "crops_data_final.json")


def _run(argv):
    r = subprocess.run([sys.executable] + argv, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


# clean canonical -> GREEN (every one of the 114 certified carries all four register sets)
rc, out = _run([_GATE, _CANON])
assert rc == 0, ("clean canonical should be GREEN\n" + out)

# scratch copy: delete a required register field from a REAL certified crop -> must bounce (exit 1)
_data = json.load(open(_CANON, encoding="utf-8"))
_target = next(c for c in _data["crops"]
               if c.get("verification_status", {}).get("status") == "verified_gs_arc"
               and c.get("slug") == "cherry-tomato")
for field in ("germination_light", "heat_threshold_f", "propagule", "tray_sowing"):
    scratch = copy.deepcopy(_data)
    tc = next(c for c in scratch["crops"] if c.get("slug") == "cherry-tomato")
    tc.pop(field, None)
    fd, p = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(scratch, fh)
    try:
        rc, out = _run([_GATE, p])
        assert rc == 1 and field in out, (f"standalone gate should bounce on missing {field}", rc, out)
        # and the always-on suite (A39) fires too -- check the VIOLATION line, not the A39 header
        rc2, out2 = _run([_WHOLE, "cherry-tomato", p])
        assert rc2 == 1 and "VIOLATION: register-coverage" in out2, (f"A39 should fire on missing {field}", rc2, out2)
    finally:
        os.unlink(p)

# and an uncertified §E shell in the REAL canonical raises NO register-coverage VIOLATION (exempt).
# (whole_crop_gate legitimately fails olive on OTHER gates -- unfilled shell -- but A39 must no-op.)
rc, out = _run([_WHOLE, "olive", _CANON])
assert "VIOLATION: register-coverage" not in out, ("uncertified shell must not raise register-coverage", out)
assert "register-coverage violations: 0" in out, ("A39 must run and report 0 on the shell", out)

print("register_coverage_gate tests: OK")
