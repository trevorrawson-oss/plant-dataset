#!/usr/bin/env python3
"""Tests for the seedling/germination-light gate (register #6). Run:
    python3 tools/test_seedling_light_gate.py

WHY: `germination_light` (light_required/dark_preferring/neutral, or null=no-home-seed-path) is the
genuinely per-crop fact; `seedling_light` (bright_default/na/blackout_then_bright/photoperiod_capped) is
a default + typed exceptions; `seedling_light_cap_hours` is the numeric companion for photoperiod_capped.
Each assertion below sneaks ONE defect class at the gate and confirms it bounces. Checks fire ONLY when a
field is present -- ABSENCE is a coverage TODO, never a shape violation, so the un-authored roster stays
green. The one cross-field coherence check is present-only: a seed crop may not be germination_light null
(a seed crop germinates from seed, so 'no-home-seed-path' N/A is contradictory). See
docs/seedling_light_contract.md.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedling_light_gate import check_crop, coverage


# ---------------------------------------------------------------- clean fixtures (-> no violations)
def seed_neutral():          # tomato-like
    return {"slug": "cherry-tomato", "propagule": "seed",
            "germination_light": "neutral", "seedling_light": "bright_default"}

def seed_light():            # lettuce-like (surface-sown, light aids germination)
    return {"slug": "lettuce-leaf", "propagule": "seed",
            "germination_light": "light_required", "seedling_light": "bright_default"}

def seed_dark():             # viola-like (cover to exclude light)
    return {"slug": "viola", "propagule": "seed",
            "germination_light": "dark_preferring", "seedling_light": "bright_default"}

def seed_direct_na():        # carrot-like: seed, but direct-sown -> no indoor seedling phase
    return {"slug": "carrot", "propagule": "seed",
            "germination_light": "neutral", "seedling_light": "na"}

def herb_seedstartable():    # lavender-like: transplant propagule, still SET (seed is a real home option)
    return {"slug": "lavender", "propagule": "transplant",
            "germination_light": "light_required", "seedling_light": "na"}

def tree_na():               # apple-like: no realistic home-from-seed path -> germination_light null
    return {"slug": "apple", "propagule": "bare_root",
            "germination_light": None, "seedling_light": "na"}

def microgreen():            # in-scope for #6 (opposite of #7): neutral + blackout_then_bright
    return {"slug": "microgreens-mix", "propagule": "seed",
            "germination_light": "neutral", "seedling_light": "blackout_then_bright"}

def capped():                # synthetic RESERVED value proof: photoperiod_capped + a valid cap
    return {"slug": "synthetic-longday", "propagule": "seed",
            "germination_light": "neutral", "seedling_light": "photoperiod_capped",
            "seedling_light_cap_hours": 11}

CLEAN = (seed_neutral, seed_light, seed_dark, seed_direct_na, herb_seedstartable,
         tree_na, microgreen, capped)
for f in CLEAN:
    assert check_crop(f()) == [], (f.__name__, check_crop(f()))

# 0. an un-authored crop (no #6 fields) -> no violations (coverage owns presence, not this gate)
assert check_crop({"slug": "x", "propagule": "seed"}) == [], check_crop({"slug": "x", "propagule": "seed"})
# non-seed unauthored likewise green
assert check_crop({"slug": "apple2", "propagule": "bare_root"}) == []

# ---------------------------------------------------------------- defect injections (-> violation)
# 1. germination_light bad enum
c = seed_neutral(); c["germination_light"] = "bright"
assert any("germination_light" in v for v in check_crop(c)), check_crop(c)

# 2. cross-field coherence: a SEED crop marked null (no-home-seed-path) is contradictory
c = seed_neutral(); c["germination_light"] = None
assert any("germination_light" in v and ("seed" in v.lower() or "null" in v.lower()) for v in check_crop(c)), check_crop(c)

# 2b. but a NON-seed crop marked null is VALID (the apple/tree N-A case) -> no violation
c = tree_na()
assert check_crop(c) == [], check_crop(c)

# 2c. and a NON-seed crop SET (seed-startable herb) is VALID -> no violation
c = herb_seedstartable()
assert check_crop(c) == [], check_crop(c)

# 3. seedling_light bad enum
c = seed_neutral(); c["seedling_light"] = "full_sun"
assert any("seedling_light" in v for v in check_crop(c)), check_crop(c)

# 4. orphan cap_hours: present but seedling_light != photoperiod_capped
c = seed_neutral(); c["seedling_light_cap_hours"] = 11   # seedling_light is bright_default
assert any("cap_hours" in v for v in check_crop(c)), check_crop(c)

# 4b. orphan cap_hours with seedling_light ABSENT entirely
c = {"slug": "y", "propagule": "seed", "seedling_light_cap_hours": 11}
assert any("cap_hours" in v for v in check_crop(c)), check_crop(c)

# 5. photoperiod_capped MISSING cap_hours
c = seed_neutral(); c["seedling_light"] = "photoperiod_capped"   # no cap_hours
assert any("cap_hours" in v and ("missing" in v.lower() or "photoperiod" in v.lower()) for v in check_crop(c)), check_crop(c)

# 6. cap_hours out of range
c = capped(); c["seedling_light_cap_hours"] = 30
assert any("cap_hours" in v and "range" in v.lower() for v in check_crop(c)), check_crop(c)

# 7. cap_hours not an int
c = capped(); c["seedling_light_cap_hours"] = "11"
assert any("cap_hours" in v and "int" in v.lower() for v in check_crop(c)), check_crop(c)

# 7b. cap_hours must not be a bool (bool is an int subclass -- guard it)
c = capped(); c["seedling_light_cap_hours"] = True
assert any("cap_hours" in v for v in check_crop(c)), check_crop(c)

# ---------------------------------------------------------------- coverage
crops = [seed_neutral(), seed_light(), tree_na(), microgreen(), capped(),
         {"slug": "unauthored", "propagule": "seed"}]
germ, seed = coverage(crops)
assert set(germ["SET"]) == {"cherry-tomato", "lettuce-leaf", "microgreens-mix", "synthetic-longday"}, germ
assert germ["NA"] == ["apple"], germ
assert germ["TODO"] == ["unauthored"], germ
assert seed["bright_default"] == ["cherry-tomato", "lettuce-leaf"], seed
assert seed["blackout_then_bright"] == ["microgreens-mix"], seed
assert seed["na"] == ["apple"], seed
assert seed["photoperiod_capped"] == ["synthetic-longday"], seed
assert seed["TODO"] == ["unauthored"], seed
# microgreens are IN-scope for #6 -> they COUNT (not skipped like #7's INDOOR_SLUGS)
assert "microgreens-mix" in germ["SET"] and "microgreens-mix" in seed["blackout_then_bright"]

# ---------------------------------------------------------------- CLI exit codes (subprocess)
import json as _json
import subprocess
import tempfile

_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seedling_light_gate.py")


def _run(fixture, extra=None):
    fd, p = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(p, "w", encoding="utf-8") as fh:
        _json.dump(fixture, fh)
    try:
        r = subprocess.run([sys.executable, _GATE, p] + (extra or []),
                           capture_output=True, text=True)
        return r.returncode, r.stdout
    finally:
        os.unlink(p)


_clean = {"crops": [seed_neutral(), capped(), tree_na(), microgreen()]}
_bad = {"crops": [dict(seed_neutral(), germination_light="bright")]}
assert _run(_clean)[0] == 0, "clean fixture should exit 0"
assert _run(_bad)[0] == 1, "bad-enum fixture should exit 1"
rc, out = _run(_clean, ["--coverage"])
assert rc == 0 and "COVERAGE" in out, ("coverage run", rc, out)

print("seedling_light_gate tests: OK")
