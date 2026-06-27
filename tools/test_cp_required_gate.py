#!/usr/bin/env python3
"""Tests for the CP-required (dual-register) gate (whole_crop_gate A36; incognito-redteam C16,
Trevor ruling 2026-06-27). Run: python3 tools/test_cp_required_gate.py

C16: deleting a `_beginner` sibling makes gate B count the field SP (no violation) -- a bot can
downgrade a should-be-dual consumer field to seasoned-only by simply not writing the sibling. This
gate closes that: every base-name in the ESTABLISHED dual-register consumer set (the 74 the 18
already carry both registers for) PLUS the newly-ruled soil-texture fields must carry BOTH a
`_seasoned` AND a `_beginner` sibling.

GATE-UNLOCK (Trevor): the soil-texture fields (preferred/problematic/tolerated_texture) are ruled
CP but the 7 crops carrying them have no `_beginner` yet -> the gate goes RED on those 21 cells
until a claude.ai back-fill lands (gate-as-worklist, like the register passes). So on the live 18
this gate returns EXACTLY the 21 soil-texture worklist items and ZERO established-set violations.
SP-ruled fields (why_seasoned, reason_seasoned, the backend *_note/*_basis) are NOT in the CP set.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cp_required_gate import cp_required_violations, CP_BASE_NAMES

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
_data = json.load(open(_path, encoding="utf-8")) if os.path.exists(_path) else {"crops": []}
_cert = [c for c in _data["crops"]
         if c.get("verification_status", {}).get("status") == "verified_gs_arc"]

# 0. a CP field carrying BOTH registers -> clean
assert cp_required_violations(
    {"slug": "x", "description_seasoned": "S.", "description_beginner": "B."}) == [], "both present -> clean"

# 1. the C16 omission: a CP field with _seasoned but NO _beginner sibling -> violation
v = cp_required_violations({"slug": "x", "description_seasoned": "Only seasoned, beginner deleted."})
assert any("description" in m for m in v), f"missing _beginner on a CP field must flag: {v}"

# 2. a nested CP field (region_notes) missing its beginner -> violation, path named
v = cp_required_violations({"slug": "x", "regions": {"se_gulf": {"region_notes_seasoned": "S."}}})
assert any("region_notes" in m and "se_gulf" in m for m in v), v

# 3. an SP-ruled field is NOT in the CP set -> NOT flagged (why/reason/backend notes)
for sp in ("why_seasoned", "reason_seasoned", "frost_risk_note_seasoned", "synthesis_note_seasoned",
           "design_note_seasoned", "basis_seasoned", "source_note_seasoned"):
    assert cp_required_violations({"slug": "x", sp: "Seasoned-only, legitimately SP."}) == [], \
        f"{sp} is SP-ruled, must NOT be flagged"
    assert sp[:-9] not in CP_BASE_NAMES, f"{sp[:-9]} must not be in the CP set"

# 4. the soil-texture GATE-UNLOCK: ruled CP, so a _seasoned with no _beginner -> violation (worklist)
v = cp_required_violations({"slug": "x", "soil": {"preferred_texture_seasoned": "Fertile loam."}})
assert any("preferred_texture" in m for m in v), f"soil texture is ruled CP -> flag until back-fill: {v}"
for tex in ("preferred_texture", "problematic_texture", "tolerated_texture"):
    assert tex in CP_BASE_NAMES, f"{tex} must be in the CP set (Trevor C16 ruling)"

# 5. a whitespace/empty _seasoned -> not a populated field, not flagged here (A29 owns emptiness)
assert cp_required_violations({"slug": "x", "description_seasoned": "   "}) == []

# 6. REAL DATA: the ONLY violations across the 18 are the 21 soil-texture worklist items;
#    the established 74-name consumer set is 0-FP (every _seasoned has its _beginner).
if _cert:
    all_v = [(c["slug"], m) for c in _cert for m in cp_required_violations(c)]
    non_texture = [(s, m) for s, m in all_v if "_texture" not in m]
    assert non_texture == [], f"established-set CP FALSE POSITIVES (should be 0): {non_texture}"
    texture = [(s, m) for s, m in all_v if "_texture" in m]
    assert len(texture) == 21, f"expected 21 soil-texture GATE-UNLOCK items (7 crops x 3), got {len(texture)}"
    worklist_crops = sorted({s for s, _ in texture})
    assert worklist_crops == ["blueberry", "broccoli", "green-beans-bush", "lavender",
                              "microgreens-mix", "onion", "orange-navel"], worklist_crops
    print(f"  real data: established set 0-FP; {len(texture)} soil-texture GATE-UNLOCK items "
          f"across {len(worklist_crops)} crops (the claude.ai back-fill worklist): PASS")

print("cp_required_gate: all tests passed")
