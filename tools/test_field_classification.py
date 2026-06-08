#!/usr/bin/env python3
"""Unit test for the ONE canonical backend/user-facing predicate.
Run from repo root: python3 tools/test_field_classification.py

Pins the disputed-field rulings from TOOLING_HARDENING_spec FIX 1 + the
register-bearing-field inventory, so the three gates can never drift again.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field_classification import is_backend

# --- BACKEND (verbatim/dash/spelled-degrees tolerated; not temp/dash-scanned) ---
BACKEND_CASES = [
    # (key, path)
    ("source_quote", "regions.warm_arid.plantings[0].source_quote"),
    ("source_quote_seasoned", "x.source_quote_seasoned"),
    ("basis_seasoned", "regions.warm_arid.resolved_by_zone.8.heat_pause.basis_seasoned"),
    ("basis", "regions.warm_arid.resolved_by_zone.8.heat_pause.basis"),
    ("synthesis_note_seasoned", "zones.8.plantings[0].synthesis_note_seasoned"),
    ("design_note", "regions.x.plantings[0].design_note"),
    ("note", "verification_status.open_findings[0].note"),       # under verification_status subtree
    ("note", "zones.9.anchoring_urls.uc_mg.note"),               # anchoring_urls subtree
    ("zone_8_presence", "regions.ca_north_coast.zone_8_presence"),
    ("zone_10_desert_fold", "regions.ca_desert.zone_10_desert_fold"),
    ("calendar_basis", "regions.x.resolved_by_zone.9.calendar_basis"),
    ("sources_summary", "sources_summary"),
    ("plantings_provenance", "regions.x.plantings_provenance"),
    ("uscrn_validation", "regions.x.uscrn_validation"),
    ("description_sources", "description_sources"),
    ("notes_internal", "x.notes_internal"),
    ("note_internal", "x.note_internal"),
]
for k, p in BACKEND_CASES:
    assert is_backend(k, p), f"expected BACKEND: key={k!r} path={p!r}"

# --- USER-FACING (must be temp/dash-scanned; NOT backend) ---
USER_FACING_CASES = [
    ("region_notes_seasoned", "regions.warm_arid.region_notes_seasoned"),
    ("region_notes_beginner", "regions.warm_arid.region_notes_beginner"),
    ("region_label", "regions.warm_arid.region_label"),
    ("description_seasoned", "description_seasoned"),
    ("harvest_ready_seasoned", "harvest_ready_seasoned"),
    ("plant_out", "regions.warm_arid.resolved_by_zone.9.plant_out"),
    ("text", "tips_by_stage[0].text"),
    ("cause_seasoned", "pests[0].cause_seasoned"),
]
for k, p in USER_FACING_CASES:
    assert not is_backend(k, p), f"expected USER-FACING: key={k!r} path={p!r}"

print("PASS field_classification")
