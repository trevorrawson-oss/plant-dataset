#!/usr/bin/env python3
"""Tests for the pet_safe rollout coverage tool (post-114 §A rollout). Run:
    python3 tools/test_pet_safe_coverage.py

WHY: safe crops carry NO pet_safe field (warnings-only), so the log is the completeness record.
This asserts every certified crop was checked (is in the log) and that the log and dataset agree.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pet_safe_coverage import coverage_violations

def cert(slug, pet_safe=None):
    c = {"slug": slug, "verification_status": {"status": "verified_gs_arc"}}
    if pet_safe is not None:
        c["pet_safe"] = pet_safe
    return c

TOXIC = {"status": "toxic", "affects": ["cats"], "note": "x", "sources": ["aspca"],
         "anchoring_urls": {"aspca": {"url": "https://a/", "verified": "2026-07-06"}}}

# 1. clean: every cert crop logged; toxic crop has a block; safe crop is blank
crops = [cert("chives", TOXIC), cert("basil")]
log = {"chives": {"verdict": "toxic"}, "basil": {"verdict": "safe"}}
assert coverage_violations(log, crops) == [], coverage_violations(log, crops)

# 2. a certified crop NOT in the log -> violation (unchecked)
crops = [cert("chives", TOXIC), cert("basil")]
log = {"chives": {"verdict": "toxic"}}
assert any("basil" in v and "unchecked" in v for v in coverage_violations(log, crops)), coverage_violations(log, crops)

# 3. logged toxic but NO dataset block -> violation
crops = [cert("chives")]  # no pet_safe block
log = {"chives": {"verdict": "toxic"}}
assert any("chives" in v and "no pet_safe" in v for v in coverage_violations(log, crops)), coverage_violations(log, crops)

# 4. dataset block but crop NOT logged -> violation
crops = [cert("chives", TOXIC)]
log = {}
assert any("chives" in v for v in coverage_violations(log, crops)), coverage_violations(log, crops)

print("pet_safe_coverage tests: OK")
