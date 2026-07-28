#!/usr/bin/env python3
"""RED-before-GREEN battery for zone_order_gate (the ca_desert z9 defect class).

THE DEFECT THIS GUARDS. asparagus `ca_desert` z9 (cooler) carried harvest "Feb - Apr" while
z10 (warmer, Imperial/Coachella) carried "Mar - Apr" -- the cooler zone led the warmer zone
into harvest by a month. Root cause was a wrong-sentence citation off UC ANR Pub 7234, but
NO GATE COMPARED NEIGHBORING ZONES, so nothing caught it; it was found by reading the cells.

Run: python3 tools/test_zone_order_gate.py
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zone_order_gate import zone_order_violations  # noqa: E402

CANON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
PASS, FAIL = [], []


def check(name, cond):
    (PASS if cond else FAIL).append(name)
    print(f"  {'ok  ' if cond else 'FAIL'} {name}")


def mk(archetype="herbaceous_perennial", zones=None):
    """Minimal crop with one region; zones = {zone: (suitability, harvest)}."""
    zones = zones or {}
    return {
        "slug": "test-crop",
        "archetype": archetype,
        "regions": {"test_region": {"resolved_by_zone": {
            z: {"suitability": s, "harvest": h, "calendar": ["growing"] * 12}
            for z, (s, h) in zones.items()}}},
    }


print("=== A. the real defect, from the real pre-fix canonical ===")
data = json.load(open(CANON, encoding="utf-8"))
asp = [c for c in data["crops"] if c.get("slug", "").startswith("asparagus")][0]

# Reconstruct the shipped defect on a SCRATCH COPY of the real crop.
red = copy.deepcopy(asp)
red["regions"]["ca_desert"]["resolved_by_zone"]["9"]["harvest"] = "Feb - Apr"
v = zone_order_violations(red)
check("RED: pre-fix ca_desert z9 'Feb - Apr' vs z10 'Mar - Apr' is flagged", len(v) == 1)
check("RED: message names both zones", bool(v) and "9" in v[0] and "10" in v[0])

check("GREEN: the real shipped asparagus is clean", zone_order_violations(asp) == [])

print("\n=== B. roster-wide: the gate must be silent on canonical ===")
total = sum(len(zone_order_violations(c)) for c in data["crops"])
check(f"GREEN: 0 violations across all {len(data['crops'])} crops (got {total})", total == 0)

print("\n=== C. adversarial -- defects that MUST bounce ===")
check("cooler zone leads warmer by one month",
      len(zone_order_violations(mk(zones={
          "9": ("perennializes", "Feb - Apr"), "10": ("perennializes", "Mar - May")}))) == 1)
check("cooler zone leads warmer by several months",
      len(zone_order_violations(mk(zones={
          "5": ("perennializes", "Mar - May"), "6": ("perennializes", "Jun - Jul")}))) == 1)
check("non-adjacent chain: each bad step flagged",
      len(zone_order_violations(mk(zones={
          "3": ("perennializes", "Jan - Mar"),
          "4": ("perennializes", "Feb - Apr"),
          "5": ("perennializes", "Mar - May")}))) == 2)
check("marginal cells are in scope too (not just perennializes)",
      len(zone_order_violations(mk(zones={
          "9": ("marginal", "Feb - Apr"), "10": ("perennializes", "Mar - May")}))) == 1)

print("\n=== D. legitimate shapes that must NOT bounce (flood control) ===")
check("warmer starts earlier = correct gradient",
      zone_order_violations(mk(zones={
          "9": ("perennializes", "Apr - Jun"), "10": ("perennializes", "Mar - May")})) == [])
check("equal starts are fine",
      zone_order_violations(mk(zones={
          "9": ("perennializes", "Mar - May"), "10": ("perennializes", "Mar - Apr")})) == [])
check("unsuitable cells are skipped",
      zone_order_violations(mk(zones={
          "9": ("unsuitable", "Feb - Apr"), "10": ("perennializes", "Mar - May")})) == [])
check("two-cycle comma windows are skipped (not comparable)",
      zone_order_violations(mk(zones={
          "8": ("perennializes", "Apr - May, Nov - Jan"),
          "9": ("perennializes", "Dec - May")})) == [])
check("missing harvest is skipped (A48's job, not this gate's)",
      zone_order_violations(mk(zones={
          "9": ("perennializes", None), "10": ("perennializes", "Mar - May")})) == [])
check("unparseable harvest is skipped, not crashed",
      zone_order_violations(mk(zones={
          "9": ("perennializes", "whenever spears appear"),
          "10": ("perennializes", "Mar - May")})) == [])

print("\n=== E. scope -- the measured reason this is archetype-scoped ===")
# Measured on canonical 9fe9e33e: all-crops 51 violations / 37 crops, perennial-is-True 11 / 8,
# herbaceous_perennial 0. The broad scopes are dominated by LEGITIMATE shapes: USDA zone is a
# WINTER-MINIMUM metric and a poor spring proxy in maritime PNW, and frost-free subtropics
# deliberately delay the warmest zone's fall planting.
check("a cool_season_annual with the SAME defect does NOT bounce (archetype-scoped)",
      zone_order_violations(mk(archetype="cool_season_annual", zones={
          "9": ("perennializes", "Feb - Apr"), "10": ("perennializes", "Mar - May")})) == [])
check("a crop with no archetype does NOT bounce",
      zone_order_violations(mk(archetype=None, zones={
          "9": ("perennializes", "Feb - Apr"), "10": ("perennializes", "Mar - May")})) == [])

print(f"\n{'='*62}\n{len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    for f in FAIL:
        print(f"  FAILED: {f}")
    sys.exit(1)
print("ALL GREEN")
