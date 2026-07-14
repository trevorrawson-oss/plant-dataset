#!/usr/bin/env python3
"""Tests for overwinter_hardiness_gate. Run: python3 tools/test_overwinter_hardiness_gate.py

SOFT + standalone (variety_detail_gate pattern): a crop opts in via `winter_hardiness` in gating_factors;
off-scope crops are silent. Violations = coverage (an opted-in overwintering crop must recommend >=2
hardiness classes). Warnings = window-fit (a very_hardy overwintering type should not be 'early'; a tender
summer type should not be 'late'). Shape (enum/min_temp_f/DTM) is variety_detail_gate's job, NOT re-checked.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overwinter_hardiness_gate import in_scope, hardiness_violations, hardiness_warnings, coverage_report


def hv(**over):
    v = {"id": "lancelot", "name": "Lancelot", "cold_hardiness_class": "hardy", "maturity_class": "mid"}
    v.update(over)
    return v


def crop(varieties, gating=("winter_hardiness",), slug="leek"):
    return {"slug": slug, "gating_factors": list(gating), "varieties": {"recommended": varieties}}


_tender = hv(id="king-richard", name="King Richard", cold_hardiness_class="tender", maturity_class="early")
_vhardy = hv(id="bandit", name="Bandit", cold_hardiness_class="very_hardy", maturity_class="late")

# in scope only when the token is present
assert in_scope(crop([hv()])) is True
assert in_scope(crop([hv()], gating=())) is False

# off-scope crop -> silent (no violations, no warnings)
assert hardiness_violations(crop([hv()], gating=())) == []
assert hardiness_warnings(crop([hv()], gating=())) == []

# clean: spans >=2 classes, coherent windows -> no violations, no warnings
CLEAN = crop([_tender, hv(), _vhardy])
assert hardiness_violations(CLEAN) == [], hardiness_violations(CLEAN)
assert hardiness_warnings(CLEAN) == [], hardiness_warnings(CLEAN)

# coverage gap: a single hardiness class on an opted-in crop -> violation
assert any("hardiness class" in v for v in hardiness_violations(crop([hv(), hv(id="a", name="A")])))

# window-fit WARNING: very_hardy labeled 'early'
assert any("very_hardy" in w for w in hardiness_warnings(crop([_tender, hv(id="x", name="X", cold_hardiness_class="very_hardy", maturity_class="early")])))

# window-fit WARNING: tender labeled 'late'
assert any("tender" in w for w in hardiness_warnings(crop([hv(), hv(id="y", name="Y", cold_hardiness_class="tender", maturity_class="late")])))

# coverage_report counts in-scope crops + objs
cov = coverage_report([CLEAN])
assert cov["in_scope_crops"] == 1 and cov["variety_objs"] == 3, cov

print("overwinter_hardiness_gate tests: OK")
