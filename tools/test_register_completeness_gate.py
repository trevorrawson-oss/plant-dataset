#!/usr/bin/env python3
"""Tests for the per-crop register-completeness function (B5 wiring).

register_completeness_violations(crop) is the per-crop half of the roster-completeness
gate: every prose-shaped string must match a ruling class, else it is an UNRULED field
(the generalized bolting-class miss). This function is what wires into the always-on
whole_crop_gate; importing the module must NOT run the dataset-wide script (it is guarded
under __main__).

Run: python3 tools/test_register_completeness_gate.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from register_completeness_gate import register_completeness_violations

# 1. a crop whose prose is all register-suffixed / excluded -> clean.
clean = {"slug": "x", "description_seasoned": "A long enough seasoned sentence of prose.",
         "name": "Carrot", "soil": {"note_beginner": "Loamy, well drained; works for most beds."}}
assert register_completeness_violations(clean) == [], register_completeness_violations(clean)

# 2. an UNRULED prose field (novel key, sentence-shaped) -> flagged (stop-and-ask).
unruled = {"slug": "x", "gizmo": "A sufficiently long sentence of prose; clearly unruled here."}
v = register_completeness_violations(unruled)
assert any("gizmo" in p for p in v), v

# 3. the §5 companions `reason` is DEFERRED-by-design -> NOT flagged.
deferred_reason = {"slug": "x", "companions": {"good_seasoned": [
    {"name": "Radishes", "reason": "A long prose reason that would otherwise be unruled here."}]}}
assert register_completeness_violations(deferred_reason) == [], register_completeness_violations(deferred_reason)

# 4. short categorical strings are not prose -> not flagged.
categorical = {"slug": "x", "water": "High", "difficulty": "Easy"}
assert register_completeness_violations(categorical) == [], register_completeness_violations(categorical)

# 5. REAL DATA: all 18 certified crops are 0-FP (so the gate can wire green into whole_crop_gate).
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
if os.path.exists(_path):
    data = json.load(open(_path))
    cert = [c for c in data["crops"]
            if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
    assert len(cert) == 18, ("expected 18 certified", len(cert))
    for c in cert:
        fp = register_completeness_violations(c)
        assert fp == [], (f"register_completeness FALSE POSITIVE on certified {c['slug']}", fp)
    print(f"  register_completeness_violations: 0 unruled across {len(cert)} certified: PASS")

print("PASS register_completeness_gate (per-crop function)")
