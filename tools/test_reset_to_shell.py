#!/usr/bin/env python3
"""Unit tests for reset_to_shell (the author-fresh wipe). Run from repo root:
    python3 tools/test_reset_to_shell.py
TDD: written BEFORE the implementation. Pins docs/reset_to_shell_policy_v1_0.md.
"""
import os, sys, json, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reset_to_shell import (reset_crop, reset_dataset, assert_blanked,
                            KEEP_TOP, PRE_ARC_VSTATUS, GS_KEEP)

def sample_crop():
    return {
        "slug": "test-crop", "name": "Test Crop", "botanical_name": "Testus cropus",
        "family": "Testaceae", "category": "Root Vegetables", "type": "crop",
        "archetype": "cool_season_annual", "calendar_basis": "frost_anchored",
        "lifecycle": "annual", "perennial": False, "difficulty": "medium",
        "sources_summary": {"primary": [{"id": "umn_ext", "name": "UMN"}], "frost_data": []},
        "verification_status": {"launch_ready_core": True, "launch_ready_seasoned": True,
                                "status": "verified_complete", "source_set": ["umn_ext"],
                                "open_findings": [{"id": "x"}], "last_audited": "2026-01-01",
                                "phase": "phase_3"},
        "days_to_maturity": [70, 80], "spacing_inches": [2, 4],
        "soil": {"preferred_texture_core": "sandy loam",
                 "preferred_description_seasoned": "Deep loose -- bucket",
                 "sources": ["umn_ext"], "anchoring_urls": {}},
        "ph": {"preferred_range": [6.0, 6.8], "note_seasoned": "bucket note",
               "tolerated_range": None},
        "pests": [{"name": "Carrot rust fly", "cause_seasoned": "Psila rosae"}],
        "growth_stages": [{"name": "Germination", "what_to_look_for_seasoned": "shoots"}],
        "regions": {"northern_tier": {"region_label": "Northern Tier (Cold Zones)",
                    "plantings": [{"track": None, "direct_sow": [{"from": "soil_temp_40f"}]}],
                    "resolved_by_zone": {"3": {"calendar": ["plant"],
                                               "plantings": [{"direct_sow": []}]}},
                    "region_notes_seasoned": "bucket", "region_notes_beginner": None,
                    "sources": ["umn_ext"], "anchoring_urls": {}}},
        "succession_policy": {"suitable": True, "interval_weeks": 3, "successions": 4,
                              "tip_seasoned": "bucket tip", "tip_beginner": None},
        "start_method": {"start": "direct", "weeks_before": 0, "notes_seasoned": "always direct"},
        "zones": {"3": {"plantings": [{"x": 1}]}},
    }

def gs_crop():
    return {"slug": "cherry-tomato", "name": "Cherry",
            "pests": [{"name": "Hornworm", "cause_seasoned": "moth"}],
            "verification_status": {"status": "verified_gs_arc", "launch_ready_core": True}}

# 1. identity/classification kept verbatim
r = reset_crop(sample_crop())
for k in ["slug", "name", "botanical_name", "family", "category", "type",
          "archetype", "calendar_basis", "lifecycle", "perennial", "difficulty"]:
    assert r[k] == sample_crop()[k], f"identity {k} changed: {r[k]!r}"

# 2. sources_summary kept verbatim (candidate pool)
assert r["sources_summary"] == sample_crop()["sources_summary"], "sources_summary changed"

# 3. verification_status reset to pre-arc shell exactly
assert r["verification_status"] == PRE_ARC_VSTATUS, f"vstatus not reset: {r['verification_status']}"
assert "source_set" not in r["verification_status"], "source_set survived"
assert "open_findings" not in r["verification_status"], "open_findings survived"

# 4. scalar/string content nulled
assert r["soil"]["preferred_texture_core"] is None
assert r["soil"]["preferred_description_seasoned"] is None
assert r["ph"]["note_seasoned"] is None

# 5. content lists emptied
assert r["days_to_maturity"] == []
assert r["spacing_inches"] == []
assert r["ph"]["preferred_range"] == []
assert r["pests"] == []
assert r["growth_stages"] == []
assert r["soil"]["sources"] == []

# 6. nested dict KEYS preserved (shape intact)
assert set(r["soil"].keys()) == {"preferred_texture_core", "preferred_description_seasoned",
                                 "sources", "anchoring_urls"}
assert set(r["ph"].keys()) == {"preferred_range", "note_seasoned", "tolerated_range"}

# 7. regions: structure kept, content gone
assert "northern_tier" in r["regions"]
nt = r["regions"]["northern_tier"]
assert set(nt.keys()) == set(sample_crop()["regions"]["northern_tier"].keys())
assert nt["plantings"] == []
assert "3" in nt["resolved_by_zone"]
assert nt["resolved_by_zone"]["3"]["calendar"] == []
assert nt["resolved_by_zone"]["3"]["plantings"] == []
assert nt["region_notes_seasoned"] is None
assert nt["region_label"] is None  # uniform null; rebuilt by Step 3.5

# 8. succession_policy + start_method: keys kept, values null (re-authored Step 2)
assert set(r["succession_policy"].keys()) == set(sample_crop()["succession_policy"].keys())
assert all(v is None for v in r["succession_policy"].values()), "succession value survived"
assert all(v is None for v in r["start_method"].values()), "start_method value survived"

# 9. legacy zones blanked
assert r["zones"]["3"]["plantings"] == []

# 10. GS crops untouched by reset_dataset
data = {"crops": [sample_crop(), gs_crop()], "source_catalog": {"umn_ext": {"url": "x"}}}
before_gs = json.dumps(gs_crop(), sort_keys=True)
before_catalog = json.dumps(data["source_catalog"], sort_keys=True)
new_data, stats = reset_dataset(copy.deepcopy(data))
gs_after = next(c for c in new_data["crops"] if c["slug"] == "cherry-tomato")
assert json.dumps(gs_after, sort_keys=True) == before_gs, "GS crop mutated"
assert json.dumps(new_data["source_catalog"], sort_keys=True) == before_catalog, "catalog mutated"
assert stats["wiped"] == 1 and stats["kept_gs"] == 1, f"stats wrong: {stats}"

# 11. safety invariant helper: no content leaf survives outside keep-set
assert_blanked(r)  # must not raise
# and it MUST raise if a content leaf is non-null
bad = reset_crop(sample_crop())
bad["pests"] = [{"name": "x"}]  # smuggle content back
raised = False
try:
    assert_blanked(bad)
except AssertionError:
    raised = True
assert raised, "assert_blanked failed to catch a surviving content leaf"

# 12. reset is idempotent (re-running changes nothing)
assert reset_crop(r) == r, "reset not idempotent"

print("PASS reset_to_shell (12 checks)")
