#!/usr/bin/env python3
"""Integration test: whole_crop_gate A59 (plant dimensions) fires on a scratch fixture and is a
no-op on a canonical carrying no values. Run: python3 tools/test_gate_plant_dimensions_a59.py"""
import copy, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json")))
FA = {"field": "plant_dimensions", "date": "2026-09-16", "sources": ["umd_ext"], "note": "test"}


def gate(slug, mutate):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == slug)
    mutate(c)
    tmp = os.path.join(HERE, "_tmp_a59_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        return subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
                              capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)


def with_fa(c):
    c["verification_status"]["field_additions"] = list(c["verification_status"].get("field_additions") or []) + [FA]


def with_sibling(c):
    c["mature_dimensions_sources"] = ["umd_ext"]
    c["mature_dimensions_anchoring_urls"] = {"umd_ext": {"url": "https://extension.umd.edu/resource/growing-peppers-home-garden",
                                                         "verified": "2026-10-02"}}


# The fixture crop is a CERTIFIED crop carrying no authored value and no plant_dimensions record on the
# canonical (a null row after the 2026-09-16 write), so every injection below is the ONLY value on it.
# apple is authored on the live canonical and would carry its own record, which answered for the
# "no provenance" case once the write landed. Re-homed basil -> carrot 2026-10-03 (PLA-10 promote 3 gives
# basil a height; carrot is a NONE row in docs/kickoffs/59 and stays null).
NULL_CROP = "carrot"
nc = next(c for c in base["crops"] if c["slug"] == NULL_CROP)
assert nc.get("mature_height_ft") is None and not any(x.get("field") == "plant_dimensions" for x in nc["verification_status"].get("field_additions") or []), \
    f"{NULL_CROP} is no longer a clean fixture for this test; pick a certified crop with no plant_dimensions value or record"
# The block is present and announced, and a null row is clean.
out = gate(NULL_CROP, lambda c: None)
assert "A59. plant dimensions" in out, "A59 block missing from whole_crop_gate"
assert "plant-dimensions:" not in out, out
# A malformed pair on a scratch copy bounces.
out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [4, 1]), with_fa(c)))
assert "plant-dimensions:" in out and "lo <= hi" in out, out
# A footprint at or above the minimum spacing bounces.
out = gate(NULL_CROP, lambda c: c.__setitem__("footprint_inches", c["spacing_inches"][0]))
assert "plant-dimensions:" in out and "below spacing_inches[0]" in out, out
# An authored value with no provenance record bounces.
out = gate(NULL_CROP, lambda c: c.__setitem__("mature_height_ft", [1, 2]))
assert "plant-dimensions:" in out and "field_additions" in out, out
# A good pair with its record (and, once the sibling rule arms, its sibling) is clean, and A33 accepts it on a
# non-tree base.
out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [1, 2]), c.__setitem__("mature_spread_ft", [1, 2]), with_fa(c), with_sibling(c)))
assert "plant-dimensions:" not in out and "mature_height_ft" not in out, out
# A33 bounds: a 60 ft carrot is absurd on a non-tree base.
out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [1, 60]), with_fa(c), with_sibling(c)))
assert "mature_height_ft" in out, out
# An authored crop on the live canonical carries its record and is clean.
out = gate("apple", lambda c: None)
assert "plant-dimensions:" not in out, out
# Presence arms in the same commit that writes the keys, never before: the flag must match the data.
src = open(os.path.join(HERE, "whole_crop_gate.py")).read()
assert ("A59_PRESENCE_ARMED = True" in src) == any("mature_height_ft" in c for c in base["crops"]), \
    "presence floor must arm in the same commit that writes the keys, never before"
# With presence ARMED, a certified crop missing a key bounces.
if "A59_PRESENCE_ARMED = True" in src:
    out = gate(NULL_CROP, lambda c: c.pop("footprint_inches"))
    assert "plant-dimensions:" in out and "missing" in out, out
# With coverage ARMED, a WOODY crop whose null loses its explaining record bounces, and the message names
# the field. plum's ruling lives as an addendum on its pollination finding, so this drives the real shape.
if "A59_COVERAGE_ARMED = True" in src:
    def de_name(c):
        for f in c["verification_status"]["open_findings"]:
            f["summary"] = f["summary"].replace("mature_height_ft", "HEIGHT")
    out = gate("plum", de_name)
    assert "plant-dimensions:" in out and "no record names the field" in out, out
    # and an authored woody crop is clean under coverage
    out = gate("apple", lambda c: None)
    assert "plant-dimensions:" not in out, out
    # a cane fruit is exempt by the predicate even with its record de-named (the branch, in isolation)
    out = gate("raspberry", de_name)
    assert "plant-dimensions:" not in out, out
# PLA-10 promote 3 (T5): the SIBLING rule arms in the data commit that writes the siblings, never before
# (armed on today's canonical, the 16 PLA-465 heights carry no sibling and would each fail).
assert ("A59_SIBLING_ARMED = True" in src) == any("mature_dimensions_sources" in c for c in base["crops"]), \
    "the sibling rule must arm in the same commit that writes mature_dimensions_sources, never before"
assert "A59_SIBLING_ARMED" in src, "whole_crop_gate carries no A59_SIBLING_ARMED flag"
if "A59_SIBLING_ARMED = True" in src:
    def strip_sibling(c):
        c.pop("mature_dimensions_sources", None)
        c.pop("mature_dimensions_anchoring_urls", None)
    out = gate("apple", strip_sibling)
    assert "plant-dimensions:" in out and "mature_dimensions_sources" in out, out
    # (2026-10-03, the data commit: the armed branch's first run.) Proved at the whole_crop_gate entry point
    # on a NEW authored crop, not only a backfilled one: an uncited pair with its record bounces ...
    out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [1, 2]), with_fa(c)))
    assert "plant-dimensions:" in out and "no mature_dimensions_sources" in out, out
    # ... a blank source id bounces ...
    out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [1, 2]), with_fa(c), with_sibling(c),
                                     c.__setitem__("mature_dimensions_sources", [" "])))
    assert "plant-dimensions:" in out and "no mature_dimensions_sources" in out, out
    # ... a listed source with no http(s) anchor bounces, naming the source ...
    out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [1, 2]), with_fa(c), with_sibling(c),
                                     c.__setitem__("mature_dimensions_anchoring_urls", {})))
    assert "plant-dimensions:" in out and "source 'umd_ext' has no http(s) anchor" in out, out
    # ... a spread alone (height null) is cited too ...
    out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_spread_ft", [1, 2]), with_fa(c)))
    assert "plant-dimensions:" in out and "no mature_dimensions_sources" in out, out
    # ... and every certified crop carrying a value on the live canonical is clean (positive control on the
    # real data, so a sibling the promote mis-wrote on any of them reddens here).
    authored = [c["slug"] for c in base["crops"] if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"
                and (c.get("mature_height_ft") is not None or c.get("mature_spread_ft") is not None)]
    assert len(authored) >= 59, f"positive-control population {len(authored)} < 59 (43 promote-3 + 16 PLA-465)"
    for slug in authored:
        out = gate(slug, lambda c: None)
        assert "plant-dimensions:" not in out, (slug, out)
    print(f"  A59 sibling armed: 4 refusals at the entry point; {len(authored)} authored certified crops clean")
else:
    # Unarmed, the block announces it and an uncited height is NOT failed for its sibling here.
    out = gate(NULL_CROP, lambda c: (c.__setitem__("mature_height_ft", [1, 2]), with_fa(c)))
    assert "sibling off" in out and "plant-dimensions:" not in out, out
print("PASS gate A59 plant dimensions")
