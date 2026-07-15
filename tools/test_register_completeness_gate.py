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

# 4b. pet_safe.note + pet_safe.toxic_parts are RULED USER-FACING-CATEGORICAL (single-form icon
#     copy, Trevor 2026-07-06). `note` is a laundering key, so BOTH checks must pass clean.
pet = {"slug": "x", "pet_safe": {
    "status": "caution",
    "note": "Ripe tomatoes are fine, but the leaves and unripe fruit are toxic to cats and dogs.",
    "toxic_parts": "green foliage and unripe fruit"}}
assert register_completeness_violations(pet) == [], register_completeness_violations(pet)
assert backend_key_laundering_violations(pet) == [], backend_key_laundering_violations(pet)

# 5. REAL DATA: all 18 certified crops are 0-FP (so the gate can wire green into whole_crop_gate).
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
if os.path.exists(_path):
    data = json.load(open(_path))
    cert = [c for c in data["crops"]
            if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
    assert len(cert) >= 18, ("certified set unexpectedly small (>=18)", len(cert))
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

# 9b. TIMING-SPINE ENUMS (Plan 3, 2026-07-07): propagule + dtm_anchor are RULED backend enums
#     (structured tokens the app's crop-timing.ts consumes + maps, siblings of `start`); a crop
#     carrying them must stay clean. The other timing-spine fields are numeric arrays (out of the
#     C11 string check by shape).
timing_enums = {"slug": "x", "propagule": "clove", "dtm_anchor": "from_planting"}
assert register_completeness_violations(timing_enums) == [], \
    f"timing-spine enums propagule/dtm_anchor must be ruled: {register_completeness_violations(timing_enums)}"

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

# ---- dry-bean variety pilot (2026-07-11): the new flat per-variety string keys are RULED ----
_pilot_variety_crop = {
    "slug": "dry-bean",
    "varieties": {"recommended": [{
        "id": "black-turtle", "name": "Black Turtle",
        "maturity_class": "late", "seed_type": "open_pollinated",
        "seed_color": "black", "seed_size": "small", "plant_habit": "bush",
        "primary_use": "soup", "confidence_tier": "T1",
        "disease_notes": "some white mold pressure in humidity",
        "regional_fit": "long warm seasons",
        "note_beginner": "x", "note_seasoned": "y",
    }]},
}
_unruled = register_completeness_violations(_pilot_variety_crop)
assert _unruled == [], ("pilot variety keys must be ruled, got:", _unruled)

# a genuinely novel unruled variety key still flags (the ruling is scoped, not a blanket pass)
_novel = {"slug": "x", "varieties": {"recommended": [{"mystery_field": "Water it a whole lot, friend."}]}}
assert any("mystery_field" in p for p in register_completeness_violations(_novel)), \
    register_completeness_violations(_novel)

# ---- apple variety pilot (2026-07-11): the new tree-archetype string keys are RULED ----
# Test through the COMPOSED gate predicate _is_ruled(pat, key), not ruled_categorical alone --
# bloom_group is already globally excluded via EXCLUDED_KEYS (line 82, June-2026 C11 ruling),
# and _is_ruled checks EXCLUDED_KEYS BEFORE calling ruled_categorical, so a bloom_group clause
# inside ruled_categorical would be dead code / never reached for that key. Asserting through
# _is_ruled reflects how the real gate resolves both keys.
from register_completeness_gate import ruled_categorical, _is_ruled

P_rec = "$.crops[?(@.slug=='apple')].varieties.recommended[0]"
P_other = "$.crops[?(@.slug=='apple')]"

# bloom_group is ruled at ANY path -- it's globally excluded via EXCLUDED_KEYS, not path-scoped.
# (Do NOT assert bloom_group is False at any path -- that would contradict the June-2026 ruling.)
assert _is_ruled(P_rec, "bloom_group"), "bloom_group must be ruled (globally, via EXCLUDED_KEYS)"

# self_fruitful is ruled ONLY when path-scoped to varieties.recommended (the new Task-4 clause).
assert _is_ruled(P_rec, "self_fruitful"), "self_fruitful must be ruled under varieties.recommended"
assert not _is_ruled(P_other, "self_fruitful"), "self_fruitful path guard: unruled outside varieties.recommended"

# apple tree-variety pilot: variety_archetype (crop-level schema-dispatch enum) is ruled globally
# via EXCLUDED_KEYS -- it's a structural token, never user-facing prose
assert _is_ruled(P_other, "variety_archetype"), "variety_archetype must be ruled (EXCLUDED_KEYS)"

# leek variety pilot (hardiness_annual archetype, 2026-07-14): cold_hardiness_class (per-variety
# overwintering-viability enum: tender|hardy|very_hardy) is ruled globally via EXCLUDED_KEYS -- a
# structural token read by variety_detail_gate + overwinter_hardiness_gate, sibling of day_length_type.
assert _is_ruled(P_rec, "cold_hardiness_class"), "cold_hardiness_class must be ruled (EXCLUDED_KEYS, hardiness_annual archetype)"

# guard against over-broad rulings: an unrelated string key stays UNRULED
assert not _is_ruled(P_rec, "totally_new_prose_key"), "unrelated key must stay unruled"

# pin the ruled_categorical helper's own path-scoping directly (self_fruitful only; bloom_group
# is intentionally NOT in ruled_categorical -- it's handled upstream by EXCLUDED_KEYS)
assert ruled_categorical(P_rec, "self_fruitful"), "self_fruitful must be ruled_categorical-scoped"
assert not ruled_categorical(P_other, "self_fruitful"), "self_fruitful ruled_categorical path guard holds"

# ---- berry variety pilot (2026-07-15): bearing_habit, berry_group ruled globally; hero_description path-scoped ----
# berry enum tokens ruled globally (siblings of cold_hardiness_class / day_length_type / variety_archetype)
assert _is_ruled("$.crops[?(@.slug=='strawberry')].varieties.recommended[0].bearing_habit", "bearing_habit")
assert _is_ruled("$.crops[?(@.slug=='strawberry')].berry_group", "berry_group")
# hero_description ruled path-scoped to varieties.recommended (single-register marquee, analog of pet_safe.note)
assert _is_ruled("$.crops[?(@.slug=='strawberry')].varieties.recommended[0].hero_description", "hero_description")
# NOT ruled elsewhere (guard the path scope)
assert not _is_ruled("$.crops[?(@.slug=='strawberry')].hero_description", "hero_description")

print("PASS register_completeness_gate (per-crop function)")
