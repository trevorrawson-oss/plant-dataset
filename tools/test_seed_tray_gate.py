#!/usr/bin/env python3
"""Tests for the seed-tray cell-protocol gate (register #9). Run:
    python3 tools/test_seed_tray_gate.py

WHY: `tray_sowing` (multi_sow_thin_to_one/single_sow/multisow_clump/na) is a default + typed exceptions
for the sow-a-few-per-cell -> thin-to-strongest protocol; `pot_up` is the enum companion (does the
seedling need an intermediate pot-up before hardening off: recommended/optional/not_needed), present iff
`tray_sowing` is a REAL tray value. The `na` <-> seedling_light coherence reuses register #6's validated
signal: a real tray value requires seedling_light=='bright_default' (started from seed in an indoor cell
tray); 'na' requires seedling_light in {'na','blackout_then_bright'} (direct-sown, nursery/vegetative, or
microgreen broadcast mat). Each assertion below sneaks ONE defect class at the gate and confirms it
bounces. Checks fire ONLY when a field is present -- ABSENCE is a coverage TODO, never a shape violation,
so the un-authored roster stays green. `multisow_clump` is RESERVED (0 live members in the roster, like
#6's photoperiod_capped) and proven live only by the synthetic fixture here. See
docs/seed_tray_protocol_contract.md.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed_tray_gate import check_crop, coverage


# ---------------------------------------------------------------- clean fixtures (-> no violations)
def tray_default_recommended():   # cherry-tomato: default sow, pot-up recommended (Solanaceae)
    return {"slug": "cherry-tomato", "seedling_light": "bright_default",
            "tray_sowing": "multi_sow_thin_to_one", "pot_up": "recommended"}

def tray_default_optional():      # broccoli: default sow, pot-up optional (fast brassica)
    return {"slug": "broccoli", "seedling_light": "bright_default",
            "tray_sowing": "multi_sow_thin_to_one", "pot_up": "optional"}

def tray_single_notneeded():      # cucumber: large seed, pot-up not needed (resents disturbance)
    return {"slug": "cucumber", "seedling_light": "bright_default",
            "tray_sowing": "single_sow", "pot_up": "not_needed"}

def tray_clump_reserved():        # RESERVED value proof: multisow_clump (no live crop carries it)
    return {"slug": "synthetic-clump", "seedling_light": "bright_default",
            "tray_sowing": "multisow_clump", "pot_up": "not_needed"}

def na_direct():                  # carrot: direct-sown -> no cell-tray phase, no pot_up
    return {"slug": "carrot", "seedling_light": "na", "tray_sowing": "na"}

def na_nursery():                 # apple: bare-root nursery stock
    return {"slug": "apple", "seedling_light": "na", "tray_sowing": "na"}

def na_microgreen():              # microgreens: broadcast mat, seedling_light == blackout_then_bright
    return {"slug": "microgreens-mix", "seedling_light": "blackout_then_bright", "tray_sowing": "na"}

CLEAN = (tray_default_recommended, tray_default_optional, tray_single_notneeded, tray_clump_reserved,
         na_direct, na_nursery, na_microgreen)
for f in CLEAN:
    assert check_crop(f()) == [], (f.__name__, check_crop(f()))

# 0. an un-authored crop (no #9 fields) -> no violations (coverage owns presence, not this gate)
assert check_crop({"slug": "x", "seedling_light": "bright_default"}) == [], \
    check_crop({"slug": "x", "seedling_light": "bright_default"})
# fully-bare crop likewise green
assert check_crop({"slug": "y"}) == []
# a na crop with pot_up correctly ABSENT stays green (companion not required for na)
assert check_crop(na_direct()) == []

# ---------------------------------------------------------------- defect injections (-> violation)
# 1. tray_sowing bad enum
c = tray_default_optional(); c["tray_sowing"] = "sow_one"
assert any("tray_sowing" in v for v in check_crop(c)), check_crop(c)

# 2. coherence: a REAL tray value but seedling_light == 'na' (crop has no indoor cell-tray phase)
c = tray_default_optional(); c["seedling_light"] = "na"
assert any("tray_sowing" in v and ("seedling_light" in v or "bright_default" in v) for v in check_crop(c)), check_crop(c)

# 2b. coherence the other way: tray_sowing == 'na' but seedling_light == 'bright_default'
c = na_direct(); c["seedling_light"] = "bright_default"
assert any("tray_sowing" in v and "seedling_light" in v for v in check_crop(c)), check_crop(c)

# 2c. na with seedling_light == 'blackout_then_bright' (microgreen) is VALID -> no violation
assert check_crop(na_microgreen()) == [], check_crop(na_microgreen())

# 3. pot_up bad enum (not in recommended/optional/not_needed)
c = tray_default_optional(); c["pot_up"] = "yes"
assert any("pot_up" in v for v in check_crop(c)), check_crop(c)

# 3b. pot_up must not be a bool (the old shape -- guard against regression to true/false)
c = tray_default_optional(); c["pot_up"] = True
assert any("pot_up" in v for v in check_crop(c)), check_crop(c)

# 4. pot_up orphan: present but tray_sowing == 'na'
c = na_direct(); c["pot_up"] = "optional"
assert any("pot_up" in v for v in check_crop(c)), check_crop(c)

# 4b. pot_up orphan: present but tray_sowing ABSENT entirely
c = {"slug": "z", "seedling_light": "bright_default", "pot_up": "recommended"}
assert any("pot_up" in v for v in check_crop(c)), check_crop(c)

# 5. missing companion: a REAL tray value but pot_up absent
c = tray_default_optional(); del c["pot_up"]
assert any("pot_up" in v and "missing" in v.lower() for v in check_crop(c)), check_crop(c)

# ---------------------------------------------------------------- coverage
crops = [tray_default_recommended(), tray_default_optional(), tray_single_notneeded(),
         tray_clump_reserved(), na_direct(), na_microgreen(),
         {"slug": "unauthored", "seedling_light": "bright_default"}]
tray, pot = coverage(crops)
assert set(tray["multi_sow_thin_to_one"]) == {"cherry-tomato", "broccoli"}, tray
assert tray["single_sow"] == ["cucumber"], tray
assert tray["multisow_clump"] == ["synthetic-clump"], tray
assert set(tray["na"]) == {"carrot", "microgreens-mix"}, tray
assert tray["TODO"] == ["unauthored"], tray
assert pot["recommended"] == ["cherry-tomato"], pot
assert pot["optional"] == ["broccoli"], pot
assert set(pot["not_needed"]) == {"cucumber", "synthetic-clump"}, pot
assert set(pot["absent"]) == {"carrot", "microgreens-mix", "unauthored"}, pot

# ---------------------------------------------------------------- CLI exit codes (subprocess)
import json as _json
import subprocess
import tempfile

_GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_tray_gate.py")


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


_clean = {"crops": [tray_default_recommended(), tray_single_notneeded(), na_direct(), na_microgreen()]}
_bad = {"crops": [dict(tray_default_optional(), tray_sowing="sow_one")]}
assert _run(_clean)[0] == 0, "clean fixture should exit 0"
assert _run(_bad)[0] == 1, "bad-enum fixture should exit 1"
rc, out = _run(_clean, ["--coverage"])
assert rc == 0 and "COVERAGE" in out, ("coverage run", rc, out)

print("seed_tray_gate tests: OK")
