#!/usr/bin/env python3
"""Tests for the display-readiness cert-gate branch (Phase B, audit F5, 2026-06-24).
Run: python3 tools/test_display_readiness_gate.py

Cert validates BIOLOGY + sources; it does NOT guarantee the fields each guide CARD needs
are present, so a crop can be cert-clean and render BLANK hero/feeding cards. The audit
found this concentrated in the two citrus:
  lemon       -- sunlight, sunlight_hours, water, and the whole fertilizer grid (type/
                 timing/frequency) null -> blank Hero sun stat + blank Feeding card.
  orange-navel -- ph.preferred_range [], container_ok None (no decision), fertilizer grid
                 null -> blank pH hero stat + blank container line + blank Feeding card.

The gate is ARCHETYPE-AWARE so it never cries wolf on a legitimate N/A:
  - indoor (non_seasonal_indoor / microgreens): no sunlight_hours / ph / spacing / container
    / fertilizer-grid demanded -- its surface is the IndoorCycleCard, not Hero/Feeding/Ph.
  - in-ground trees (peach): container_ok == False is a VALID decision; no pot value demanded.

Contract (display_readiness_violations):
  Universal (every crop, incl. indoor): sunlight, water.
  Non-indoor: sunlight_hours, ph.preferred_range, spacing_inches (all non-empty lists);
              fertilizer.type / .timing / .frequency (non-empty); container_ok must be a real
              boolean decision, and if True must carry a pot (min_pot_gallons) or tray
              (depth_inches_min) dimension.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from display_readiness_gate import display_readiness_violations


def clean_outdoor():
    return {
        "slug": "carrot", "calendar_basis": "frost_anchored",
        "sunlight": "full_sun", "sunlight_hours": [6, 8], "water": "moderate",
        "ph": {"preferred_range": [6.0, 6.8]},
        "spacing_inches": [2, 3],
        "container_notes": {"container_ok": True, "min_pot_gallons": 5},
        "fertilizer": {"type": "balanced", "timing": "at planting", "frequency": "monthly"},
    }


def clean_indoor():
    """microgreens: indoor surface; sunlight_hours/ph/spacing/container all legitimately N/A."""
    return {
        "slug": "microgreens-mix", "calendar_basis": "non_seasonal_indoor",
        "sunlight": "bright indirect", "water": "keep evenly moist",
        "sunlight_hours": [], "ph": {"preferred_range": []}, "spacing_inches": [],
        "container_notes": {"container_ok": True, "depth_inches_min": 1},
        "fertilizer": {"type": None, "timing": None, "frequency": None},
    }


def clean_inground_tree():
    """peach: in-ground; container_ok == False is a valid decision, no pot demanded."""
    c = clean_outdoor()
    c["slug"] = "peach"
    c["container_notes"] = {"container_ok": False}
    return c


# 0. clean outdoor / indoor / in-ground tree -> no violations
assert display_readiness_violations(clean_outdoor()) == [], display_readiness_violations(clean_outdoor())
assert display_readiness_violations(clean_indoor()) == [], display_readiness_violations(clean_indoor())
assert display_readiness_violations(clean_inground_tree()) == [], display_readiness_violations(clean_inground_tree())

# 1. lemon: sunlight null -> violation
c = clean_outdoor(); c["sunlight"] = None
assert any("sunlight" in x and "hours" not in x for x in display_readiness_violations(c)), display_readiness_violations(c)

# 2. lemon: water null -> violation
c = clean_outdoor(); c["water"] = None
assert any(x.startswith("water") or "water" in x.split(":")[0] for x in display_readiness_violations(c)), display_readiness_violations(c)

# 3. lemon: sunlight_hours [] -> violation
c = clean_outdoor(); c["sunlight_hours"] = []
assert any("sunlight_hours" in x for x in display_readiness_violations(c)), display_readiness_violations(c)

# 4. lemon: fertilizer grid all null -> 3 violations (type/timing/frequency)
c = clean_outdoor(); c["fertilizer"] = {"type": None, "timing": None, "frequency": None}
v = display_readiness_violations(c)
assert any("fertilizer.type" in x for x in v) and any("fertilizer.timing" in x for x in v) and any("fertilizer.frequency" in x for x in v), v

# 5. orange: ph.preferred_range [] -> violation
c = clean_outdoor(); c["ph"] = {"preferred_range": []}
assert any("preferred_range" in x for x in display_readiness_violations(c)), display_readiness_violations(c)

# 6. orange: container_ok None (no decision) -> violation
c = clean_outdoor(); c["container_notes"] = {"container_ok": None}
assert any("container_ok" in x for x in display_readiness_violations(c)), display_readiness_violations(c)

# 7. spacing_inches [] (non-indoor) -> violation
c = clean_outdoor(); c["spacing_inches"] = []
assert any("spacing_inches" in x for x in display_readiness_violations(c)), display_readiness_violations(c)

# 8. container_ok True but NO pot/tray dimension -> violation
c = clean_outdoor(); c["container_notes"] = {"container_ok": True}
assert any("container_ok" in x and ("pot" in x or "dimension" in x) for x in display_readiness_violations(c)), display_readiness_violations(c)

# 9. indoor exemption is real: an indoor crop with empty sunlight_hours/ph/spacing is clean,
#    but a MISSING universal (water) is still flagged even indoors
c = clean_indoor(); c["water"] = None
assert any("water" in x.split(":")[0] for x in display_readiness_violations(c)), display_readiness_violations(c)

print("display_readiness_gate: all tests passed")
