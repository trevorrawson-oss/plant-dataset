#!/usr/bin/env python3
"""Tests for the register-FILL cert gate (tools/register_fill_gate.py).

Distinct from register_completeness_gate.py (which checks every prose field is
RULED). This checks every ruled `_seasoned`/`_beginner` register field is AUTHORED
(not null/empty) before a crop can flip -- the gap that let apple ship 30 null
register fields and certified peach ship 46. It is a CERT gate (Step 11 / on-demand),
NOT part of the always-on whole_crop_gate, so an in-progress crop is not red-flagged.

Allowlist (legitimately null): `frost_risk_note_*` (seasoned-only, authored per-cell
only where late frost is a risk) and the legacy `zones{}` layer (deprecated). Empty
arrays (companions array-split) are not strings, so never counted. Everything else
null at cert is a violation -- author it (an N/A field is authored as N/A prose, not
left null).

Run: python3 tools/test_register_fill_gate.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from register_fill_gate import register_fill_violations

# 1. all register fields filled -> no violation
clean = {"slug": "x", "description_seasoned": "A.", "description_beginner": "B.",
         "soil": {"note_seasoned": "loamy", "note_beginner": "loamy"}}
assert register_fill_violations(clean) == [], register_fill_violations(clean)

# 2. a null core register field -> violation naming the path
bad = {"slug": "x", "description_seasoned": None, "description_beginner": "B."}
v = register_fill_violations(bad)
assert any("description_seasoned" in x for x in v), v

# 3. empty-string register field -> violation
bad2 = {"slug": "x", "container_notes": {"notes_seasoned": "", "notes_beginner": "y"}}
assert any("container_notes" in x and "notes_seasoned" in x for x in register_fill_violations(bad2)), register_fill_violations(bad2)

# 4. ALLOWLIST -- null frost_risk_note in a region cell is NOT a violation
frost = {"slug": "x", "regions": {"hawaii": {"resolved_by_zone": {"11": {"frost_risk_note_seasoned": None}}}}}
assert register_fill_violations(frost) == [], register_fill_violations(frost)

# 5. ALLOWLIST -- legacy zones{} suitability_reason null is NOT a violation
legacy = {"slug": "x", "zones": {"3": {"suitability_reason_seasoned": None, "suitability_reason_beginner": None}}}
assert register_fill_violations(legacy) == [], register_fill_violations(legacy)

# 6. empty ARRAY (companions split) -> NOT counted (only None / "" strings count)
arr = {"slug": "x", "companions": {"good_seasoned": [], "bad_seasoned": []}}
assert register_fill_violations(arr) == [], register_fill_violations(arr)

# 7. a real null region note (NOT frost) IS a violation (region_notes must be authored)
rn = {"slug": "x", "regions": {"se_gulf": {"region_notes_seasoned": None}}}
assert any("region_notes_seasoned" in x for x in register_fill_violations(rn)), register_fill_violations(rn)

# 8. N/A is authored as prose, not left null -> a null "not applicable" field still violates
na = {"slug": "x", "succession_policy": {"reason_seasoned": None}}
assert any("reason_seasoned" in x for x in register_fill_violations(na)), register_fill_violations(na)

# 9. STRUCTURED N/A: an {applicable: false} object IS the authored N/A, so its null
# approach_*/note_* register children are NOT violations (the overwintering N/A on
# cherry/beefsteak/carrot). The flag is the authored form -- do not demand prose too.
struct_na = {"slug": "x", "container_notes": {"overwintering": {
    "applicable": False, "approach_seasoned": None, "approach_beginner": None}}}
assert register_fill_violations(struct_na) == [], register_fill_violations(struct_na)

# 10. applicable: null is UNDECIDED, not authored -> its null register children STILL violate
# (lettuce overwintering: someone must decide applicability + author or set applicable:false).
undecided = {"slug": "x", "container_notes": {"overwintering": {
    "applicable": None, "approach_seasoned": None, "approach_beginner": None}}}
assert any("approach_seasoned" in x for x in register_fill_violations(undecided)), register_fill_violations(undecided)

# 11. applicable: true means the feature APPLIES -> null prose is still a violation.
applies = {"slug": "x", "container_notes": {"overwintering": {
    "applicable": True, "approach_seasoned": None}}}
assert any("approach_seasoned" in x for x in register_fill_violations(applies)), register_fill_violations(applies)

print("PASS register_fill_gate")
