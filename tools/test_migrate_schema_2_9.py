#!/usr/bin/env python3
"""TDD for migrate_schema_2_9 -- additive, idempotent, non-destructive null-scaffold.
Run from repo root: python3 tools/test_migrate_schema_2_9.py
"""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migrate_schema_2_9 as m


def tree():
    return {"slug": "peach", "archetype": "deciduous_fruit_tree", "perennial": True,
            "watering": {"frequency_seasoned": "weekly"}, "fertilizer": {"type": "x"},
            "container_notes": {"container_ok": True},
            "varieties": {"recommended": []}, "thinning": {}}


def evergreen():
    return {"slug": "lemon", "archetype": "evergreen_fruit_tree", "perennial": True,
            "watering": {}, "fertilizer": {}, "container_notes": {}, "varieties": {"recommended": []}}


def bramble():
    return {"slug": "raspberry", "archetype": "berries_woody", "perennial": True,
            "watering": {}, "fertilizer": {}, "container_notes": {}, "varieties": {"recommended": []}}


def strawberry():
    return {"slug": "strawberry", "archetype": "berries_herbaceous", "perennial": True,
            "watering": {}, "fertilizer": {}, "container_notes": {}, "varieties": {"recommended": []}}


def annual():
    return {"slug": "carrot", "archetype": "cool_season_annual", "perennial": False,
            "watering": {"frequency_seasoned": "twice weekly"}, "fertilizer": {},
            "container_notes": {}, "varieties": {"recommended": ["Nantes (sweet)"]}}


# 1. UNIVERSAL on every crop (annual included): watering ext + fertilizer how-much + container
a = m.migrate_crop(copy.deepcopy(annual()))
for k in ("watering_method", "schedule_by_stage", "drought_tolerance",
          "method_note_seasoned", "method_note_beginner",
          "critical_periods_seasoned", "critical_periods_beginner"):
    assert k in a["watering"], ("annual watering missing", k)
assert a["watering"]["schedule_by_stage"] == [], a["watering"]["schedule_by_stage"]
assert "amount_seasoned" in a["fertilizer"] and "amount_beginner" in a["fertilizer"]
assert "self_watering_ok" in a["container_notes"]
assert "self_watering_notes_seasoned" in a["container_notes"]

# 2. UNIVERSAL: C2 sources/anchoring plumbing on the four shells
assert a["watering"].get("sources", "MISS") is None
assert a["watering"].get("anchoring_urls", "MISS") is None
assert a["fertilizer"].get("sources", "MISS") is None
assert a["varieties"].get("sources", "MISS") is None

# 3. annual does NOT get perennial/tree groups
for k in ("chill_hours_required", "bloom_time_seasoned", "pollination",
          "recommended_rootstock", "rootstock_options", "dormancy_window",
          "establishment_years", "cane_type", "renovation_seasoned"):
    assert k not in a, ("annual wrongly got", k)

# 4. non-destructive: existing values + annual variety strings preserved
assert a["watering"]["frequency_seasoned"] == "twice weekly"
assert a["varieties"]["recommended"] == ["Nantes (sweet)"], "annual varieties must stay strings"

# 5. WOODY tree gets the full perennial surface
t = m.migrate_crop(copy.deepcopy(tree()))
assert t["chill_hours_required"] is None and t["chill_hours_range"] == []
assert "chill_hours_note_seasoned" in t and "chill_hours_note_beginner" in t
assert "bloom_time_seasoned" in t and t["bloom_duration_days"] is None
assert "pollinator_notes_seasoned" in t
poll = t["pollination"]
assert {"self_fertile", "needs_pollinizer", "pollinizer_distance_ft",
        "notes_seasoned", "notes_beginner"} <= set(poll)
assert "dormancy_window" in t and "pruning_window" in t
assert t["establishment_years"] is None and "establishment_note" in t
assert "container_overwintering_seasoned" in t["container_notes"]
# woody varieties.recommended stays a list, ready for objects
assert isinstance(t["varieties"]["recommended"], list)

# 6. GRAFTED tree gets rootstock; bramble does NOT
assert t["recommended_rootstock"] is None and t["rootstock_options"] == []
assert "recommended_rootstock_note" in t
b = m.migrate_crop(copy.deepcopy(bramble()))
assert "rootstock_options" not in b, "bramble should not get rootstock"
assert b["cane_type"] is None and "cane_management_seasoned" in b
assert "chill_hours_required" in b  # bramble is woody -> chill applies

# 7. evergreen gets rootstock (grafted) but is woody too
e = m.migrate_crop(copy.deepcopy(evergreen()))
assert "rootstock_options" in e and "chill_hours_required" in e
assert "cane_type" not in e  # not a bramble

# 8. strawberry (matted herbaceous): renovation + bloom + establishment, NO chill/rootstock
s = m.migrate_crop(copy.deepcopy(strawberry()))
assert "renovation_seasoned" in s and "renovation_beginner" in s
assert "bloom_time_seasoned" in s and "pollinator_notes_seasoned" in s
assert s["establishment_years"] is None
assert "chill_hours_required" not in s and "rootstock_options" not in s and "cane_type" not in s

# 9. idempotent: applying twice equals once (no double-append, no overwrite)
once = m.migrate_crop(copy.deepcopy(tree()))
twice = m.migrate_crop(m.migrate_crop(copy.deepcopy(tree())))
assert once == twice, "migration not idempotent"

# 10. dataset-level: schema_version bumped + versioning_note extended; crops migrated
d = {"schema_version": "2.8", "versioning_note": "base note.", "crops": [tree(), annual()]}
m.migrate_dataset(d)
assert d["schema_version"] == "2.9", d["schema_version"]
assert "2.9" in d["versioning_note"]
assert d["crops"][0]["chill_hours_required"] is None  # tree migrated
assert "watering_method" in d["crops"][1]["watering"]  # annual migrated

print("PASS migrate_schema_2_9")
