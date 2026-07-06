#!/usr/bin/env python3
"""Tests for the pet_safe schema gate (post-114 backlog §A). Run:
    python3 tools/test_pet_safe_gate.py

WHY: pet_safe is a consumer-facing icon field; a mis-shaped block (bad enum, missing note on a
toxic crop, an uncatalogued/non-T1 source, a null anchoring url, a missing field_additions
provenance entry, or a coverage gap) must bounce BEFORE promote. Each assertion below sneaks one
defect class at the gate and confirms it is caught. The affirmative-non-toxic requirement for
`safe` is review-enforced (the offline gate cannot read the source page), so it is NOT tested here.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pet_safe_gate import pet_safe_violations, coverage_report

CATALOG = {
    "aspca": {"id": "aspca", "tier": "T1"},
    "ncsu_ext": {"id": "ncsu_ext", "tier": "T1"},
    "rhs": {"id": "rhs", "tier": "T1"},
    "some_blog": {"id": "some_blog", "tier": "T2"},
}


def safe_crop():
    return {"slug": "rosemary", "pet_safe": {
        "status": "safe",
        "note": "A culinary herb, not toxic to cats, dogs, or horses.",
        "sources": ["aspca", "ncsu_ext"],
        "anchoring_urls": {
            "aspca": {"url": "https://www.aspca.org/...", "verified": "2026-07-06"},
            "ncsu_ext": {"url": "https://plants.ces.ncsu.edu/...", "verified": "2026-07-06"},
        }}}


def toxic_crop():
    return {"slug": "chives", "pet_safe": {
        "status": "toxic",
        "affects": ["cats", "dogs", "horses"],
        "note": "In the allium family; toxic to cats, dogs, and horses.",
        "sources": ["aspca", "ncsu_ext"],
        "anchoring_urls": {
            "aspca": {"url": "https://www.aspca.org/...", "verified": "2026-07-06"},
            "ncsu_ext": {"url": "https://plants.ces.ncsu.edu/...", "verified": "2026-07-06"},
        }}}


# 0. clean safe + clean toxic -> no violations
assert pet_safe_violations(safe_crop(), CATALOG) == [], pet_safe_violations(safe_crop(), CATALOG)
assert pet_safe_violations(toxic_crop(), CATALOG) == [], pet_safe_violations(toxic_crop(), CATALOG)

# 1. absent pet_safe -> NOT this function's concern (coverage handles it)
assert pet_safe_violations({"slug": "x"}, CATALOG) == []

# 2. bad enum value -> violation
c = safe_crop(); c["pet_safe"]["status"] = "pet-friendly"
assert any("status" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 3. missing note on a toxic crop -> violation
c = toxic_crop(); del c["pet_safe"]["note"]
assert any("note" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 4. empty affects on a toxic crop -> violation
c = toxic_crop(); c["pet_safe"]["affects"] = []
assert any("affects" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 5. affects not a subset of {cats,dogs,horses} -> violation
c = toxic_crop(); c["pet_safe"]["affects"] = ["cats", "birds"]
assert any("affects" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 6. uncatalogued source -> violation
c = safe_crop(); c["pet_safe"]["sources"] = ["not_a_source"]
assert any("not_a_source" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 7. catalogued but non-T1 source -> violation
c = safe_crop(); c["pet_safe"]["sources"] = ["some_blog"]; c["pet_safe"]["anchoring_urls"] = {"some_blog": {"url": "http://x", "verified": "2026-07-06"}}
assert any("T1" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 8. empty sources -> violation
c = safe_crop(); c["pet_safe"]["sources"] = []
assert any("sources" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 9. anchoring url null / missing for a listed source -> violation
c = safe_crop(); c["pet_safe"]["anchoring_urls"]["aspca"] = {"url": None, "verified": "2026-07-06"}
assert any("aspca" in v and "url" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 10. CERTIFIED crop carrying pet_safe but NO field_additions entry -> violation (amend-not-recert)
c = safe_crop(); c["verification_status"] = {"status": "verified_gs_arc"}
assert any("field_additions" in v for v in pet_safe_violations(c, CATALOG)), pet_safe_violations(c, CATALOG)

# 11. same certified crop WITH the field_additions entry -> clean
c["verification_status"]["field_additions"] = [
    {"field": "pet_safe", "date": "2026-07-06", "sources": ["aspca", "ncsu_ext"], "note": "column pass"}]
assert pet_safe_violations(c, CATALOG) == [], pet_safe_violations(c, CATALOG)

# --- coverage_report ---
crops = [safe_crop(), toxic_crop(), {"slug": "borage"}]  # borage lacks pet_safe

# 12. required slug missing pet_safe -> appears in unset
counts, unset = coverage_report(crops, {"rosemary", "chives", "borage"})
assert unset == ["borage"], unset
assert counts == {"safe": 1, "toxic": 1, "caution": 0}, counts

# 13. all required present -> unset empty
counts, unset = coverage_report(crops, {"rosemary", "chives"})
assert unset == [], unset

print("pet_safe_gate tests: OK")
