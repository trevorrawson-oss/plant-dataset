#!/usr/bin/env python3
"""Tests for control_ladder_gate. Run: python3 tools/test_control_ladder_gate.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from control_ladder_gate import catalog_violations

def data(methods, crops=None, srcs=None):
    return {
        "control_methods": methods,
        "source_catalog": srcs or {"umn_ext": {"tier": "T1"}, "seed_co": {"tier": "T2"}},
        "crops": crops or [],
    }

def method(**over):
    m = {"name": "Insecticidal soap", "tier": "soft_chemical", "applies_to": ["insect_soft_bodied"],
         "how_it_works_beginner": "x", "how_it_works_seasoned": "x", "best_use": "x",
         "pros": ["low tox"], "cons": ["contact only"], "sources": ["umn_ext"],
         "anchoring_urls": {"umn_ext": {"url": "u", "verified": "2026-07-22"}}}
    m.update(over); return m

# clean catalog -> no violations
assert catalog_violations(data({"insecticidal_soap": method()})) == []
# missing required key
assert any("missing/empty" in v for v in catalog_violations(data({"insecticidal_soap": method(pros=[])})))
# invalid tier
assert any("invalid tier" in v for v in catalog_violations(data({"insecticidal_soap": method(tier="nuke")})))
# NB: catalog method KEYS are snake_case (mirroring source_catalog keys) -- NOT format-checked here.
# The kebab ID_RE check applies only to per-crop pest/disease `id` (Task 3 identity).
# source not in catalog
assert any("not in source_catalog" in v for v in catalog_violations(data({"m": method(sources=["ghost"], anchoring_urls={"ghost": {}})})))
# source not T1
assert any("not T1" in v for v in catalog_violations(data({"m": method(sources=["seed_co"], anchoring_urls={"seed_co": {}})})))
# anchoring_urls mismatch
assert any("anchoring_urls" in v for v in catalog_violations(data({"m": method(anchoring_urls={})})))
print("catalog_violations tests: OK")
