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

from control_ladder_gate import ladder_violations

CAT = {
    "rotate_crops":     {"name": "Rotation", "tier": "cultural", "applies_to": ["any"]},
    "insecticidal_soap":{"name": "Soap", "tier": "soft_chemical", "applies_to": ["insect_soft_bodied"]},
    "copper":           {"name": "Copper", "tier": "soft_chemical", "applies_to": ["fungal_foliar"]},
    "pyrethrin":        {"name": "Pyrethrin", "tier": "conventional", "applies_to": ["insect_general"]},
}
def crop(problems, key="pests"):
    return {"slug": "broccoli", key: problems}
def prob(**over):
    p = {"id": "aphids", "name": "Aphids", "type": "insect",
         "control_ladder": [{"method": "rotate_crops"}, {"method": "insecticidal_soap"}]}
    p.update(over); return p
def D(crop_obj):  # gate expects (data, crop)
    return ({"control_methods": CAT}, crop_obj)

# clean softest-first ladder -> no violations
assert ladder_violations(*D(crop([prob()]))) == []
# absent ladder -> not a ladder violation (coverage handles it)
assert ladder_violations(*D(crop([prob(control_ladder=None)]))) == []
# dangling method reference
assert any("unknown method" in v for v in ladder_violations(*D(crop([prob(control_ladder=[{"method": "ghost"}])]))))
# NON-monotonic: conventional before cultural
bad = [{"method": "pyrethrin"}, {"method": "rotate_crops"}]
assert any("softest-first" in v for v in ladder_violations(*D(crop([prob(control_ladder=bad)]))))
# applies_to mismatch: insecticidal soap under a FUNGAL disease
fung = prob(id="downy-mildew", name="Downy mildew", type="fungal",
            control_ladder=[{"method": "rotate_crops"}, {"method": "insecticidal_soap"}])
assert any("does not fit problem type" in v for v in ladder_violations(*D(crop([fung], key="diseases"))))
# cultural-only SHORT ladder (clubroot) -> MUST PASS
club = prob(id="clubroot", name="Clubroot", type="fungal", control_ladder=[{"method": "rotate_crops"}])
assert ladder_violations(*D(crop([club], key="diseases"))) == []
# bad-tier catalog method in a ladder must NOT crash (catalog_violations reports the bad tier separately)
_badcat = {"broken": {"name": "Broken", "applies_to": ["any"]}}  # no tier key
assert ladder_violations({"control_methods": _badcat}, crop([prob(control_ladder=[{"method": "broken"}])])) == []
# unrecognized problem type -> flagged (applies_to coherence cannot be checked)
_unk = prob(id="mystery", type="fungusy", control_ladder=[{"method": "insecticidal_soap"}])
assert any("not a recognized type" in v for v in ladder_violations(*D(crop([_unk]))))
print("ladder_violations tests: OK")
