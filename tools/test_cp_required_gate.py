#!/usr/bin/env python3
"""Tests for the CP-required (dual-register) gate (whole_crop_gate A36; incognito-redteam C16,
Trevor ruling 2026-06-27). Run: python3 tools/test_cp_required_gate.py

C16: deleting a `_beginner` sibling makes gate B count the field SP (no violation) -- a bot can
downgrade a should-be-dual consumer field to seasoned-only by simply not writing the sibling. This
gate closes that: every base-name in the ESTABLISHED dual-register consumer set (the 74 the 18
already carry both registers for) PLUS the newly-ruled soil-texture fields must carry BOTH a
`_seasoned` AND a `_beginner` sibling.

GATE-UNLOCK (Trevor): the soil-texture fields (preferred/problematic/tolerated_texture) were ruled
CP while the 7 crops carrying them had no `_beginner` yet -> the gate went RED on those 21 cells
until a claude.ai back-fill landed (gate-as-worklist, like the register passes). That back-fill
LANDED 2026-06-28, so the live 18 are now 0-FP on this gate (established set + soil texture both
dual-complete). SP-ruled fields (why_seasoned, reason_seasoned, the backend *_note/*_basis) are NOT
in the CP set. The synthetic omission tests below still prove the gate fires on a deleted sibling.
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

# 4. re-audit #2 D21: the soil-texture trio is CATEGORICAL (rendered as chips), NOT CP prose -- the
#    real soil prose is preferred_description. So a texture _seasoned with no _beginner does NOT flag.
for tex in ("preferred_texture", "problematic_texture", "tolerated_texture"):
    assert tex not in CP_BASE_NAMES, f"{tex} is categorical (chips), must NOT be in the CP set"
assert cp_required_violations({"slug": "x", "soil": {"preferred_texture_seasoned": "Fertile loam."}}) == [], \
    "soil texture is categorical, not a CP-prose field"
# the real soil prose IS CP:
assert "preferred_description" in CP_BASE_NAMES
assert any("preferred_description" in m for m in cp_required_violations(
    {"slug": "x", "soil": {"preferred_description_seasoned": "Deep loose loam."}})), \
    "preferred_description (the real soil prose) IS CP"

# 5. a whitespace/empty _seasoned -> not a populated field, not flagged here (A29 owns emptiness)
assert cp_required_violations({"slug": "x", "description_seasoned": "   "}) == []

# 6. REAL DATA: the GATE-UNLOCK is RESOLVED -- the soil-texture beginner back-fill landed
#    (2026-06-28), so all 18 certified crops are now 0-FP on A36 (the established 74-name consumer
#    set AND the soil-texture trio are both dual-complete). Originally this asserted the 21-item
#    worklist; that worklist is cleared.
if _cert:
    fp = [(c["slug"], m) for c in _cert for m in cp_required_violations(c)]
    assert fp == [], f"cp_required FALSE POSITIVES on the 18 (GATE-UNLOCK should be cleared): {fp}"
    print(f"  real data: 0 cp_required violations across {len(_cert)} certified "
          f"(GATE-UNLOCK cleared by the soil-texture back-fill): PASS")

print("cp_required_gate: all tests passed")
