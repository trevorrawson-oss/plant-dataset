#!/usr/bin/env python3
"""Tests for the berries_herbaceous calendar FILL pass (strawberry, anchor 13).
Run: python3 tools/test_derive_berry_calendars.py

The release-lane step that GENERATES each cell's calendar[] from its grown_as + window
dates via berry_calendar.derive_berry_calendar (the tree-calendar discipline: author the
dates, derive the array). A cell whose windows are not yet authored (deriver -> None) is
left [] (admission). No-op off perennial_herbaceous.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from derive_berry_calendars import fill_berry_calendars

# 1. a perennial cell with windows -> filled with the perennial cycle
crop = {"calendar_basis": "perennial_herbaceous", "regions": {"northern_tier": {"resolved_by_zone": {
    "5": {"grown_as": "perennial", "bloom": "May", "harvest": "June",
          "resolved_from": {"last_frost": "April", "first_frost": "October"}, "calendar": []}}}}}
filled, skipped = fill_berry_calendars(crop)
assert filled == ["northern_tier.5"], filled
assert crop["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"] == \
    ["dormant", "dormant", "dormant", "growing", "bloom", "harvest", "renovation",
     "growing", "growing", "growing", "dormant", "dormant"], \
    crop["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"]

# 2. an annual cell -> the season_over shape
crop3 = {"calendar_basis": "perennial_herbaceous", "regions": {"ca_interior": {"resolved_by_zone": {
    "9": {"grown_as": "annual", "plant_out": "October", "bloom": "February",
          "harvest": "March-June", "calendar": []}}}}}
fill_berry_calendars(crop3)
assert crop3["regions"]["ca_interior"]["resolved_by_zone"]["9"]["calendar"] == \
    ["growing", "bloom", "harvest", "harvest", "harvest", "harvest",
     "season_over", "season_over", "season_over", "plant", "growing", "growing"]

# 3. an admission cell (grown_as null, no windows) -> skipped, stays []
crop2 = {"calendar_basis": "perennial_herbaceous", "regions": {"se_gulf": {"resolved_by_zone": {
    "9": {"grown_as": None, "calendar": []}}}}}
filled2, skipped2 = fill_berry_calendars(crop2)
assert filled2 == [] and skipped2 == ["se_gulf.9"], (filled2, skipped2)
assert crop2["regions"]["se_gulf"]["resolved_by_zone"]["9"]["calendar"] == []

# 4. off-basis -> no-op
assert fill_berry_calendars({"calendar_basis": "frost_anchored", "regions": {}}) == ([], [])

# 5. idempotent: re-running reproduces the same calendar
before = list(crop["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"])
fill_berry_calendars(crop)
assert crop["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"] == before

print("derive_berry_calendars: all tests passed")
