#!/usr/bin/env python3
"""Tests for the berries_woody calendar FILL pass (blueberry, anchor 18).
Run: python3 tools/test_derive_berry_woody_calendars.py

The release-lane step that GENERATES each cell's calendar[] from its leaf_habit + window dates
via berry_woody_calendar.derive_berry_woody_calendar (the tree-calendar discipline: claude.ai
authors the dates, Claude Code derives the array). A cell whose windows are not yet authored
(deriver -> None) is left [] (admission). No-op off berries_woody.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from derive_berry_woody_calendars import fill_berry_woody_calendars

D, G, B, H, C, P = "dormant", "growing", "bloom", "harvest", "care", "prune"

# 1. a deciduous cell with windows -> the tree dormant/prune/bloom/growing/harvest/care cycle
crop = {"calendar_basis": "berries_woody", "regions": {"northern_tier": {"resolved_by_zone": {
    "6": {"leaf_habit": "deciduous", "bloom": "Apr - May", "harvest": "Jul - Aug", "calendar": []}}}}}
filled, skipped = fill_berry_woody_calendars(crop)
assert filled == ["northern_tier.6"], filled
assert crop["regions"]["northern_tier"]["resolved_by_zone"]["6"]["calendar"] == \
    [D, D, P, B, G, G, H, H, C, D, D, D], \
    crop["regions"]["northern_tier"]["resolved_by_zone"]["6"]["calendar"]

# 2. an evergreen cell -> growing year-round with bloom/harvest/care (no dormant, no season_over)
crop3 = {"calendar_basis": "berries_woody", "regions": {"se_gulf": {"resolved_by_zone": {
    "9": {"leaf_habit": "evergreen", "bloom": "Mar", "harvest": "Jun - Jul", "calendar": []}}}}}
fill_berry_woody_calendars(crop3)
assert crop3["regions"]["se_gulf"]["resolved_by_zone"]["9"]["calendar"] == \
    [G, G, B, G, G, H, H, C, G, G, G, G]

# 3. an admission cell (leaf_habit null, no windows) -> skipped, stays []
crop2 = {"calendar_basis": "berries_woody", "regions": {"ca_interior": {"resolved_by_zone": {
    "9": {"leaf_habit": None, "calendar": []}}}}}
filled2, skipped2 = fill_berry_woody_calendars(crop2)
assert filled2 == [] and skipped2 == ["ca_interior.9"], (filled2, skipped2)
assert crop2["regions"]["ca_interior"]["resolved_by_zone"]["9"]["calendar"] == []

# 4. off-basis -> no-op
assert fill_berry_woody_calendars({"calendar_basis": "frost_anchored", "regions": {}}) == ([], [])

# 5. idempotent: re-running reproduces the same calendar
before = list(crop["regions"]["northern_tier"]["resolved_by_zone"]["6"]["calendar"])
fill_berry_woody_calendars(crop)
assert crop["regions"]["northern_tier"]["resolved_by_zone"]["6"]["calendar"] == before

print("derive_berry_woody_calendars: all tests passed")
