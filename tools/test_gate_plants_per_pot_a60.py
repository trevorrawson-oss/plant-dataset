#!/usr/bin/env python3
"""Integration test: whole_crop_gate A60 (plants_per_pot) fires on a scratch fixture and is a
no-op on a canonical carrying no values. Run: python3 tools/test_gate_plants_per_pot_a60.py

This is the A59 pattern: drive the gate through the REAL ENTRY POINT (whole_crop_gate as a
subprocess), not through the gate function, because a driver that never reaches the guarded call
site is vacuous and that has recurred three times in this repo.
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json")))
FA = {"field": "plants_per_pot", "date": "2026-09-21", "sources": ["uiuc_ext"], "note": "test"}
URL = "https://extension.illinois.edu/container-gardens/growing-vegetables-containers"


def reading(count=(4, 6), gallons=(1, 1), src="uiuc_ext", url=URL, verified="2026-09-21"):
    return {"count": list(count), "at_gallons": list(gallons), "sources": [src],
            "anchoring_urls": {src: {"url": url, "verified": verified}}}


def gate(slug, mutate):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == slug)
    mutate(c)
    tmp = os.path.join(HERE, "_tmp_a60_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        return subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
                              capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)


def with_fa(c):
    vs = c["verification_status"]
    vs["field_additions"] = list(vs.get("field_additions") or []) + [FA]


def put(c, value, fa=True):
    c["container_notes"]["plants_per_pot"] = value
    if fa:
        with_fa(c)


# The fixture crop must be CERTIFIED, container_ok, and carry no value and no record, so every
# injection below is the only thing on it. lettuce-leaf is an AUTHORED crop after the write and
# would carry its own record, which is why the fixture is a crop this pass leaves null.
NULL_CROP = "basil"
nc = next(c for c in base["crops"] if c["slug"] == NULL_CROP)
assert (nc["container_notes"].get("container_ok") is True
        and nc["container_notes"].get("plants_per_pot") is None
        and not any(x.get("field") == "plants_per_pot"
                    for x in nc["verification_status"].get("field_additions") or [])), \
    f"{NULL_CROP} is no longer a clean fixture; pick a certified container_ok crop with no value or record"

# The block is present and announced, and a crop with no value is clean.
out = gate(NULL_CROP, lambda c: None)
assert "A60. plants_per_pot" in out, "A60 block missing from whole_crop_gate"
assert "plants-per-pot:" not in out, out

# A legitimate reading with its record is clean, and A33 accepts the figures.
out = gate(NULL_CROP, lambda c: put(c, {"readings": [reading()]}))
assert "plants-per-pot:" not in out, out
assert "plants_per_pot" not in out.split("A60.")[0], out   # A33 said nothing either

# null is a legitimate value and needs no record.
out = gate(NULL_CROP, lambda c: put(c, None, fa=False))
assert "plants-per-pot:" not in out, out

# A BARE ARRAY -- the shape this spec rejected, and the one the deployed app would have divided by.
out = gate(NULL_CROP, lambda c: put(c, [4, 6]))
assert "plants-per-pot:" in out and "only key is 'readings'" in out, out

# An EMPTY readings list: absence is spelled null, never [].
out = gate(NULL_CROP, lambda c: put(c, {"readings": []}))
assert "plants-per-pot:" in out and "non-empty" in out, out

# A SCALAR at_gallons -- one type per field (amendment 3).
out = gate(NULL_CROP, lambda c: put(c, {"readings": [dict(reading(), at_gallons=1)]}))
assert "plants-per-pot:" in out and "two-element list" in out, out

# An inverted count.
out = gate(NULL_CROP, lambda c: put(c, {"readings": [reading(count=(6, 4))]}))
assert "plants-per-pot:" in out and "min <= max" in out, out

# A reading whose source has no anchor.
out = gate(NULL_CROP, lambda c: put(c, {"readings": [dict(reading(), anchoring_urls={})]}))
assert "plants-per-pot:" in out and "no anchoring_urls entry" in out, out

# Two readings from the SAME institution.
out = gate(NULL_CROP, lambda c: put(c, {"readings": [reading(), reading(count=(1, 1), gallons=(8, 10))]}))
assert "plants-per-pot:" in out and "two readings" in out, out

# An authored value with no provenance record bounces.
out = gate(NULL_CROP, lambda c: put(c, {"readings": [reading()]}, fa=False))
assert "plants-per-pot:" in out and "field_additions" in out, out

# A count on a crop the dataset says cannot go in a pot bounces. plum is certified and not
# container_ok, measured on 079e3923.
notpot = next(c for c in base["crops"] if c["slug"] == "plum")
assert notpot["container_notes"].get("container_ok") is not True, "plum is container_ok now; pick another"
out = gate("plum", lambda c: put(c, {"readings": [reading()]}))
assert "plants-per-pot:" in out and "container_ok" in out, out

# The key on an UNCERTIFIED SHELL bounces, even carrying null.
out = gate("avocado", lambda c: put(c, None, fa=False))
assert "plants-per-pot:" in out and "uncertified" in out, out

# A33 BOUNDS, through the same entry point: an absurd count and an absurd pot.
out = gate(NULL_CROP, lambda c: put(c, {"readings": [reading(count=(1, 99))]}))
assert "plants_per_pot" in out and "outside the physical bound" in out, out
out = gate(NULL_CROP, lambda c: put(c, {"readings": [reading(gallons=(1, 400))]}))
assert "plants_per_pot" in out and "outside the physical bound" in out, out
# and the HALF-GALLON row -- the reason the floor is 0.5 and not 1 -- is accepted.
out = gate(NULL_CROP, lambda c: put(c, {"readings": [reading(count=(1, 1), gallons=(0.5, 0.5))]}))
assert "plants-per-pot:" not in out and "outside the physical bound" not in out, out

# Presence arms in the same commit that writes the keys, never before: the flag must match the data.
src = open(os.path.join(HERE, "whole_crop_gate.py")).read()
carrying = any("plants_per_pot" in (c.get("container_notes") or {}) for c in base["crops"])
assert ("A60_PRESENCE_ARMED = True" in src) == carrying, \
    "presence floor must arm in the same commit that writes the keys, never before"

# With presence ARMED, a certified crop missing the key bounces.
if "A60_PRESENCE_ARMED = True" in src:
    out = gate(NULL_CROP, lambda c: c["container_notes"].pop("plants_per_pot"))
    assert "plants-per-pot:" in out and "missing" in out, out
    # and the 7 shells stay exempt by status
    out = gate("avocado", lambda c: None)
    assert "plants-per-pot:" not in out, out

print("PASS gate A60 plants_per_pot")
