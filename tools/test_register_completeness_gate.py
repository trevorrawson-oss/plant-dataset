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
from register_completeness_gate import (register_completeness_violations,
                                         backend_key_laundering_violations)

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

# ---- incognito-redteam C11 (Trevor ruling 2026-06-27): tighten A25 to flag ANY unruled STRING ----
# regardless of length (the <25-char evasion), now that the 49 legit short-string keys are ruled.

# 6. a novel SHORT-string field (the audit injection) -> flagged (was missed at <25 chars)
short_novel = {"slug": "x", "mystery_advice": "Water it lots"}
assert any("mystery_advice" in p for p in register_completeness_violations(short_novel)), \
    f"C11(a): a short novel string must now flag: {register_completeness_violations(short_novel)}"

# 7. a novel NON-STRING field -> NOT flagged (A25 polices PROSE/strings only; A33/A34 + shape
#    gates own non-string novelty -- the accepted blanket ruling).
nonstr_novel = {"slug": "x", "mystery_count": 42, "mystery_list": ["a", "b"]}
assert register_completeness_violations(nonstr_novel) == [], \
    f"C11(b): non-string novelty is out of A25's scope: {register_completeness_violations(nonstr_novel)}"

# 8. an empty / whitespace-only unruled string -> NOT flagged (not a novel field)
assert register_completeness_violations({"slug": "x", "blank": "", "ws": "   "}) == []

# 9. the RULED short-string keys (Part 1) stay clean -- a crop carrying them is not flagged
ruled_short = {"slug": "x",
               "soil": {"drainage_requirement": "well_draining", "organic_matter_preference": "high",
                        "preferred_texture_core": "loam"},
               "harvest_urgency": "daily", "hardiness_zone_min": "8b",
               "diseases": [{"audience": "core", "cause": "too much nitrogen"}],
               "notifications": [{"offset_from": "last_frost", "trigger": "days_after_sow", "stage": "germination"}],
               "regions": {"ca_desert": {"resolved_by_zone": {"10": {
                   "resolved_from": {"first_frost": "Sep 15", "last_frost": "May 15"}}}}},
               "varieties": {"recommended": [{"species": "Lavandula angustifolia", "bloom_group": "very_early"}]}}
assert register_completeness_violations(ruled_short) == [], \
    f"ruled short-string keys must stay clean: {register_completeness_violations(ruled_short)}"

# ---- incognito-redteam C11 (c) (Trevor: pursue): backend-key dash-laundering ----
# summary/claim/note are backend keys exempt from the dash/temp scan + A25. A user-facing string
# under one OUTSIDE a known-backend subtree launders past those scans (incl. a forbidden `--`).

# 10. claim at the crop root -> flagged (claim is in BACKEND_KEYS, so the check must be PATH-based)
assert any("claim" in v for v in backend_key_laundering_violations(
    {"slug": "x", "claim": "Tomatoes love full sun -- plant early."})), "root-level claim must flag"

# 11. note / summary at a user-facing position -> flagged
assert any("note" in v for v in backend_key_laundering_violations(
    {"slug": "x", "soil": {"note": "Work in compost -- it helps."}})), "user-facing note must flag"
assert any("summary" in v for v in backend_key_laundering_violations(
    {"slug": "x", "summary": "A grower-facing summary that should be a ruled field."})), "root summary must flag"

# 12. note INSIDE a known-backend subtree -> NOT flagged (legit machinery)
assert backend_key_laundering_violations(
    {"slug": "x", "regions": {"ca_desert": {"plantings_provenance": {"note": "deriver note -- ok"}}}}) == [], \
    "note under plantings_provenance is legit backend"
assert backend_key_laundering_violations(
    {"slug": "x", "verification_status": {"open_findings": [{"summary": "audit -- ok", "note": "x"}]}}) == [], \
    "summary/note under verification_status is legit backend"

# 13. the ruled-categorical varieties.recommended[].note -> NOT flagged (Trevor's per-variety note)
assert backend_key_laundering_violations(
    {"slug": "x", "varieties": {"recommended": [{"name": "v", "note": "Fast brassica, 8 to 12 days; spicy."}]}}) == [], \
    "varieties.recommended[].note is ruled categorical, exempt"

# 14. REAL DATA: 0 FP across the 18 (summary/claim/note all live in backend subtrees or the ruled note)
if os.path.exists(_path):
    fp = [(c["slug"], backend_key_laundering_violations(c)) for c in cert if backend_key_laundering_violations(c)]
    assert fp == [], f"C11(c) laundering FP on certified anchors: {fp}"
    print(f"  backend_key_laundering: 0 FP across {len(cert)} certified: PASS")

print("PASS register_completeness_gate (per-crop function)")
