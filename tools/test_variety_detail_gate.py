#!/usr/bin/env python3
"""Tests for variety_detail_gate. Run: python3 tools/test_variety_detail_gate.py

Each assert sneaks ONE defect at the gate and confirms it bounces. The gate is SOFT: off-scope crops
(no maturity_class) are silent; in-scope shape/enum errors are HARD (exit 1); band-coherence and
class/DTM ordering are advisory WARNINGS (a sourced value never warns). Absence of the schema on the
un-migrated roster is never a violation.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from variety_detail_gate import (in_scope, variety_violations, variety_warnings, coverage_report)

REQUIRED = ("id", "name", "maturity_class", "seed_type", "seed_color", "seed_size",
            "plant_habit", "primary_use", "confidence_tier", "note_beginner", "note_seasoned", "sources")


def variety(**over):
    v = {"id": "black-turtle", "name": "Black Turtle", "days_to_maturity": 100,
         "maturity_class": "late", "seed_type": "open_pollinated", "seed_color": "black",
         "seed_size": "small", "plant_habit": "bush", "primary_use": "soup",
         "is_reference": True, "confidence_tier": "T1",
         "note_beginner": "b", "note_seasoned": "s", "sources": ["ucanr_ext"]}
    v.update(over)
    return v


def crop(varieties, dtm=[90, 100], slug="dry-bean"):
    return {"slug": slug, "days_to_maturity": dtm, "varieties": {"recommended": varieties}}


_navy = variety(id="navy", name="Navy", days_to_maturity=85, maturity_class="early",
                seed_color="white", primary_use="baked", is_reference=False)

# clean pilot crop (flagship + one non-flagship) -> no violations, no warnings (Navy@85 is sourced)
CLEAN = crop([variety(), _navy])
assert variety_violations(CLEAN) == [], variety_violations(CLEAN)
assert variety_warnings(CLEAN) == [], variety_warnings(CLEAN)

from variety_detail_gate import archetype

def tvar(**over):
    v = {"id": "golden-delicious", "name": "Golden Delicious", "maturity_class": "mid",
         "is_reference": True, "confidence_tier": "T1", "note_beginner": "b", "note_seasoned": "s",
         "sources": ["umn_ext"], "bloom_group": "mid", "bloom_window_relative": [0.42, 0.6],
         "bloom_duration_days": 10, "chill_hours_required": 700, "use": "fresh eating", "triploid": False}
    v.update(over)
    return v

def tcrop(varieties, slug="apple"):
    return {"slug": slug, "variety_archetype": "tree_fruit", "days_to_maturity": [],
            "varieties": {"recommended": varieties}}

_mcintosh = tvar(id="mcintosh", name="McIntosh", bloom_group="early",
                 bloom_window_relative=[0.2, 0.36], chill_hours_required=900,
                 use="fresh eating, sauce", is_reference=False)

# archetype dispatch
assert archetype(tcrop([tvar()])) == "tree_fruit"
assert archetype(CLEAN) == "annual_dtm"          # no variety_archetype key -> default
assert archetype({"slug": "x", "variety_archetype": "bogus", "varieties": {"recommended": []}}) == "annual_dtm"

# a clean tree crop -> no violations
TREE_CLEAN = tcrop([tvar(), _mcintosh])
assert variety_violations(TREE_CLEAN) == [], variety_violations(TREE_CLEAN)

# a tree crop is NOT required to carry the bean traits (they are annual-only now)
assert not any("seed_type" in v or "plant_habit" in v for v in variety_violations(TREE_CLEAN)), variety_violations(TREE_CLEAN)

# a tree crop MISSING a tree-required field -> violation
notree = tvar(); del notree["bloom_group"]
assert any("bloom_group" in v for v in variety_violations(tcrop([notree, _mcintosh])))

# a tree variety does NOT need days_to_maturity (grafted / season-only)
assert not any("days_to_maturity" in v for v in variety_violations(TREE_CLEAN)), variety_violations(TREE_CLEAN)

# 0. off-scope crop (no maturity_class anywhere) -> silent, even with junk
off = {"slug": "bell-pepper", "days_to_maturity": [60, 90],
       "varieties": {"recommended": [{"name": "X", "days_to_maturity": 999}]}}
assert not in_scope(off)
assert variety_violations(off) == [], variety_violations(off)

# 1. bad enum on each enum field -> violation
for f, bad in [("maturity_class", "very_late"), ("seed_type", "gmo"), ("seed_size", "huge"),
               ("plant_habit", "vine"), ("primary_use", "dessert"), ("confidence_tier", "T5")]:
    c = crop([variety(**{f: bad}), _navy])
    assert any(f in v for v in variety_violations(c)), (f, variety_violations(c))

# 2. missing a required field -> violation
for f in REQUIRED:
    v = variety()
    del v[f]
    c = crop([v, _navy])
    assert any(f in x for x in variety_violations(c)), (f, variety_violations(c))

# 3. NOT exactly one flagship -> violation (zero, and two)
assert any("is_reference" in v or "flagship" in v.lower()
           for v in variety_violations(crop([variety(is_reference=False), _navy])))
assert any("is_reference" in v or "flagship" in v.lower()
           for v in variety_violations(crop([variety(), variety(id="pinto", name="Pinto", is_reference=True)])))

# 4. is_reference not a real bool -> violation
assert any("is_reference" in v for v in variety_violations(crop([variety(is_reference=1), _navy])))

# 5. id not slug-shaped / duplicate id -> violation
assert any("slug" in v.lower() or "id" in v for v in variety_violations(crop([variety(id="Black Turtle!"), _navy])))
assert any("duplicate" in v.lower()
           for v in variety_violations(crop([variety(), variety(id="black-turtle", name="Dup", is_reference=False)])))

# 6. DTM absurd (violates [7,400]) / non-int -> violation
assert any("days_to_maturity" in v for v in variety_violations(crop([variety(days_to_maturity=850), _navy])))
assert any("days_to_maturity" in v for v in variety_violations(crop([variety(days_to_maturity="100"), _navy])))

# 7. DTM missing on a DTM-based crop -> violation; but OK on a season-only crop (empty crop DTM)
v = variety()
del v["days_to_maturity"]
assert any("days_to_maturity" in x for x in variety_violations(crop([v, _navy])))
so_v = variety(id="redhaven", name="Redhaven")
del so_v["days_to_maturity"]
season_only = {"slug": "peach", "days_to_maturity": [], "varieties": {"recommended": [so_v]}}
assert not any("days_to_maturity" in x for x in variety_violations(season_only)), variety_violations(season_only)

# 8. WARNING: sourced out-of-band DTM -> SILENT (source wins); unsourced out-of-band -> advisory.
#    Test the band check SOLO so the separate class/DTM ordering check (needs >=2 varieties) can't interfere.
solo_oob = crop([variety(id="longbean", name="Longbean", days_to_maturity=200)])  # sourced (default), out of band
assert variety_warnings(solo_oob) == [], variety_warnings(solo_oob)
uns = variety(id="weird", name="Weird", days_to_maturity=200, is_reference=False, sources=[])
assert any("UNSOURCED" in w for w in variety_warnings(crop([variety(), uns]))), variety_warnings(crop([variety(), uns]))

# 9. WARNING: class/DTM ordering -- fastest labeled 'late' -> advisory (not a violation)
fast_late = variety(id="quick", name="Quick", days_to_maturity=80, maturity_class="late", is_reference=False)
c = crop([variety(), fast_late])
assert variety_violations(c) == [], variety_violations(c)
assert any("late" in w for w in variety_warnings(c)), variety_warnings(c)

# coverage
cov = coverage_report([CLEAN, off])
assert cov["in_scope_crops"] == 1, cov
assert cov["variety_objs"] == 2, cov

# CLI exit codes (subprocess)
import json as _json
import subprocess
import tempfile

_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "variety_detail_gate.py")


def _run(fixture, extra=None):
    fd, p = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(p, "w", encoding="utf-8") as fh:
        _json.dump(fixture, fh)
    try:
        r = subprocess.run([sys.executable, _GATE, p] + (extra or []), capture_output=True, text=True)
        return r.returncode
    finally:
        os.unlink(p)


assert _run({"crops": [CLEAN]}) == 0, "clean in-scope crop exits 0"
assert _run({"crops": [crop([variety(maturity_class="very_late"), _navy])]}) == 1, "bad enum exits 1"
assert _run({"crops": [off]}) == 0, "off-scope crop exits 0"

print("variety_detail_gate tests: OK")
