#!/usr/bin/env python3
"""Tests for the cross-consistency truth-layer gate (whole_crop_gate A34; incognito-redteam C7,
the deterministic cross-field layer). Run: python3 tools/test_cross_consistency_gate.py

WHY: the most likely bot failure (C7) is copy-nearest-template-don't-refit -- the crop contradicts
ITSELF. The canonical example: the fabricated crop's PROSE said pH 6.0-7.5 while the structured
`ph.preferred_range` was [3.0, 3.4]. No external truth needed -- the two fields disagree. This gate
cross-checks fields that must agree. RULE 1 (this increment): the pH range stated in
`ph.note_seasoned` / `ph.note_beginner` must match `ph.preferred_range` (every certified anchor
states it exactly; the gate tolerates 0.5 pH units of authoring drift, so it fires only on a real
contradiction). The decimal-required parse skips the "0 to 14 scale" boilerplate.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cross_consistency_gate import cross_consistency_violations

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
_data = json.load(open(_path, encoding="utf-8")) if os.path.exists(_path) else {"crops": []}
_cert = [c for c in _data["crops"]
         if c.get("verification_status", {}).get("status") == "verified_gs_arc"]


def clean():
    return {"slug": "carrot",
            "ph": {"preferred_range": [6.0, 6.8], "tolerated_range": [5.5, 7.0]},
            "ph_extra": None,
            }


def with_note(pref, note):
    return {"slug": "x", "ph": {"preferred_range": pref,
            "note_seasoned": note, "note_beginner": note}}


# 0. a crop with no ph note -> no violation (nothing to cross-check)
assert cross_consistency_violations(clean()) == [], cross_consistency_violations(clean())

# 1. note range matches preferred -> clean
assert cross_consistency_violations(with_note([6.0, 6.8], "Aim for pH 6.0 to 6.8.")) == [], "match -> clean"
assert cross_consistency_violations(with_note([4.5, 5.5], "Blueberries need pH 4.5 to 5.5.")) == [], "acid match -> clean"
assert cross_consistency_violations(with_note([6.0, 7.5], "tolerant across pH 6.0-7.5 range")) == [], "hyphen form -> clean"

# 2. THE C7 contradiction: prose says 6.0 to 7.5, structured is [3.0, 3.4] -> violation
c = with_note([3.0, 3.4], "Aim for a soil pH of 6.0 to 7.5 for best growth.")
v = cross_consistency_violations(c)
assert any("ph" in x.lower() and "note" in x.lower() for x in v), f"C7 pH contradiction must flag: {v}"

# 3. a single-endpoint drift beyond tolerance -> violation (prose 6.0-6.8 vs structured [6.0, 8.5])
c = with_note([6.0, 8.5], "around pH 6.0 to 6.8")
assert cross_consistency_violations(c), "high-end drift > 0.5 must flag"

# 4. within-tolerance drift -> clean (prose 6.0-6.8 vs structured [6.1, 6.9], <=0.5 each)
c = with_note([6.1, 6.9], "roughly pH 6.0 to 6.8")
assert cross_consistency_violations(c) == [], "small authoring drift stays clean"

# 5. the "0 to 14 scale" boilerplate must NOT be parsed as the pH range (no decimals -> skipped)
c = with_note([6.0, 6.8], "Soil pH runs on a scale from 0 to 14; aim for 6.0 to 6.8.")
assert cross_consistency_violations(c) == [], "scale boilerplate must be skipped, real range matches"

# 6. note present but NO parseable decimal pH range -> skip (a single value 'around 6.5' is not a range)
c = with_note([6.0, 6.8], "Keep the soil slightly acidic, around pH 6.5.")
assert cross_consistency_violations(c) == [], "no parseable range -> no false contradiction"

# 7. preferred_range absent -> skip
assert cross_consistency_violations({"slug": "x", "ph": {"note_seasoned": "pH 6.0 to 6.8"}}) == []

# 8. REAL DATA: every certified anchor's pH prose matches its structured range (0 FP)
fp = [(c["slug"], cross_consistency_violations(c)) for c in _cert if cross_consistency_violations(c)]
assert fp == [], f"cross-consistency FP on certified anchors: {fp}"
if _cert:
    print(f"  real data: 0 FP across {len(_cert)} certified anchors: PASS")

print("cross_consistency_gate: all tests passed")
