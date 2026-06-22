#!/usr/bin/env python3
"""Tests for the woody-ornamental calendar FILL pass (lavender, anchor 14).
Run: python3 tools/test_derive_woody_ornamental_calendars.py

The release-lane step that GENERATES each cell's calendar[] from its grown_as + window dates
via woody_ornamental_calendar.derive_woody_ornamental_calendar (the tree-calendar discipline:
author the dates, derive the array). A cell whose windows are not yet authored (deriver -> None)
is left [] (admission). No-op off perennial_woody_ornamental. Mirrors fill_berry_calendars'
(filled, skipped) return shape (the global "mirror the berry tooling's shapes" constraint).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from derive_woody_ornamental_calendars import fill_woody_ornamental_calendars

# 1. a perennial cell with windows -> filled with the perennial subshrub cycle
crop = {"calendar_basis": "perennial_woody_ornamental", "regions": {"northern_tier": {"resolved_by_zone": {
    "5": {"grown_as": "perennial", "bloom": "May",
          "resolved_from": {"last_frost": "April", "first_frost": "October"}, "calendar": []}}}}}
filled, skipped = fill_woody_ornamental_calendars(crop)
assert filled == ["northern_tier.5"], filled
assert crop["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"] == \
    ["dormant", "dormant", "dormant", "growing", "bloom", "prune", "growing",
     "growing", "growing", "growing", "dormant", "dormant"], \
    crop["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"]

# 2. an annual cell -> the season_over shape (no prune)
crop3 = {"calendar_basis": "perennial_woody_ornamental", "regions": {"ca_interior": {"resolved_by_zone": {
    "9": {"grown_as": "annual", "plant_out": "October", "bloom": "April - May", "calendar": []}}}}}
fill_woody_ornamental_calendars(crop3)
assert crop3["regions"]["ca_interior"]["resolved_by_zone"]["9"]["calendar"] == \
    ["growing", "growing", "growing", "bloom", "bloom", "season_over", "season_over",
     "season_over", "season_over", "plant", "growing", "growing"]

# 3. an admission cell (grown_as null, no windows) -> skipped, stays []
crop2 = {"calendar_basis": "perennial_woody_ornamental", "regions": {"se_gulf": {"resolved_by_zone": {
    "9": {"grown_as": None, "calendar": []}}}}}
filled2, skipped2 = fill_woody_ornamental_calendars(crop2)
assert filled2 == [] and skipped2 == ["se_gulf.9"], (filled2, skipped2)
assert crop2["regions"]["se_gulf"]["resolved_by_zone"]["9"]["calendar"] == []

# 4. off-basis -> no-op
assert fill_woody_ornamental_calendars({"calendar_basis": "frost_anchored", "regions": {}}) == ([], [])

# 5. idempotent: re-running reproduces the same calendar
before = list(crop["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"])
fill_woody_ornamental_calendars(crop)
assert crop["regions"]["northern_tier"]["resolved_by_zone"]["5"]["calendar"] == before

print("derive_woody_ornamental_calendars: all tests passed")
