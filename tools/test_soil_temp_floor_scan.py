#!/usr/bin/env python3
"""Sneak the defect at soil_temp_floor_scan and confirm it BOUNCES (CLAUDE.md TDD rule).

A gate isn't done until a defect has been injected into a SCRATCH COPY and caught. This
injects each variant of the class the scan exists to catch, plus the near-misses it must NOT
flag, so the check is proven tight rather than merely quiet on today's data.

Runs under both pytest and `python3 tools/test_soil_temp_floor_scan.py` -- the guard lives in
the test body, never under __main__, because pytest never runs __main__ (that gap is exactly
what let test_build_corn_family_patch fail under one runner and skip under the other).
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import soil_temp_floor_scan as S  # noqa: E402

CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")


def _base():
    with open(CANON, encoding="utf-8") as fh:
        return json.load(fh)


def _crop(data, slug):
    for c in data["crops"]:
        if c["slug"] == slug:
            return c
    raise AssertionError("crop %s absent" % slug)


def _cell(data, slug, region, zone):
    return _crop(data, slug)["regions"][region]["resolved_by_zone"][zone]


def _unruled(data):
    return [h for h in S.scan(data) if (h[2], h[3]) not in S.RULED]


def test_live_canonical_is_clean():
    """The shipped state: zero UNRULED hits, so the check is flip-eligible."""
    hits = _unruled(_base())
    assert not hits, "live canonical has %d unruled hit(s): %s" % (
        len(hits), [(h[0], h[2], h[3]) for h in hits[:5]])
    print("PASS live canonical: 0 unruled hits")


def test_catches_sown_on_last_frost():
    """The exact defect corrected 2026-07-29: plant_out opens ON the last-frost date."""
    data = _base()
    cell = _cell(data, "acorn-squash", "ca_desert", "10")
    assert cell["plant_out"] == "Feb 1 - Mar 1", cell["plant_out"]   # guard the premise
    cell["plant_out"] = "Jan 15 - Feb 15"
    cell["first_plant_date"] = "Jan 15"
    hits = _unruled(data)
    assert any(h[0] == "acorn-squash" and h[2] == "ca_desert" and h[3] == "10" for h in hits), \
        "injected sown-on-last-frost was NOT caught"
    print("PASS caught: sown exactly ON the last-frost date")


def test_catches_sown_before_last_frost():
    """The worse variant: opens strictly BEFORE last frost, with no sourced exception."""
    data = _base()
    cell = _cell(data, "pumpkin", "ca_desert", "10")
    cell["plant_out"] = "Jan 1 - Feb 15"
    cell["first_plant_date"] = "Jan 1"
    hits = _unruled(data)
    assert any(h[0] == "pumpkin" and h[3] == "10" and h[4] < 0 for h in hits), \
        "injected sown-before-last-frost was NOT caught"
    print("PASS caught: sown BEFORE the last-frost date")


def test_catches_the_two_cycle_spring_half():
    """A two-cycle 'spring, fall' string whose SPRING half is the offender."""
    data = _base()
    cell = _cell(data, "cucumber", "ca_desert", "10")
    assert cell["plant_out"].startswith("Feb 1"), cell["plant_out"]
    cell["plant_out"] = "Jan 15 - Mar 1, Sep 1 - Oct 1"
    cell["first_plant_date"] = "Jan 15"
    assert any(h[0] == "cucumber" and h[3] == "10" for h in _unruled(data)), \
        "injected two-cycle spring defect was NOT caught"
    print("PASS caught: two-cycle string with a bad spring half")


def test_ignores_transplanted_crop():
    """A nursery-transplant crop set out ON last frost is CORRECT -- its germination temp
    governs indoor sowing, not the transplant date. This is the filter that cut 27 false
    positives (thyme/rosemary/lavender)."""
    data = _base()
    crop = _crop(data, "rosemary")
    assert crop.get("propagule") == "transplant", crop.get("propagule")
    hits = [h for h in _unruled(data) if h[0] == "rosemary"]
    assert not hits, "transplanted crop wrongly flagged: %s" % hits[:3]
    # and prove the filter is what excludes it, not luck
    crop["propagule"] = "seed"
    assert any(h[0] == "rosemary" for h in _unruled(data)), \
        "propagule filter is not what was excluding rosemary -- check the scan"
    print("PASS ignores transplanted crops, and propagule is provably the reason")


def test_ignores_cool_season_crop():
    """A crop that does not need warm soil may be sown at frost."""
    data = _base()
    for c in data["crops"]:
        g = c.get("germination_temp_f")
        if isinstance(g, list) and len(g) == 2 and isinstance(g[0], (int, float)):
            assert not (g[0] < S.WARM_SOIL_F and any(
                h[0] == c["slug"] for h in _unruled(data))), \
                "cool-soil crop %s flagged" % c["slug"]
    print("PASS ignores crops that do not require warm soil")


def test_ruled_exception_is_suppressed_but_still_visible():
    """utah_dixie z8 must not be reported, must still be returned by the raw scan, and its
    ruling must carry a reason."""
    data = _base()
    raw = S.scan(data)
    ud = [h for h in raw if h[2] == "utah_dixie" and h[3] == "8"]
    assert ud, "utah_dixie z8 no longer matches the raw scan -- did the data change?"
    assert not [h for h in _unruled(data) if h[2] == "utah_dixie"], \
        "ruled exception leaked into the reported set"
    reason = S.RULED[("utah_dixie", "8")]
    assert reason and len(reason) > 40 and "USU" in reason, \
        "a RULED entry must carry a substantive sourced reason"
    print("PASS ruled exception suppressed, still visible, and carries its reason")


def test_exit_code_is_nonzero_on_defect(tmp_path=None):
    """The gate must actually FAIL, not just print."""
    import subprocess
    import tempfile
    data = _base()
    cell = _cell(data, "acorn-squash", "ca_desert", "10")
    cell["plant_out"] = "Jan 15 - Feb 15"
    cell["first_plant_date"] = "Jan 15"
    d = tempfile.mkdtemp()
    p = os.path.join(d, "c.json")
    with open(p, "wb") as fh:
        fh.write(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode())
    rc = subprocess.run([sys.executable, os.path.join(HERE, "soil_temp_floor_scan.py"), p],
                        capture_output=True, text=True).returncode
    assert rc == 1, "scan exited %d on injected defect, expected 1" % rc
    clean = subprocess.run([sys.executable, os.path.join(HERE, "soil_temp_floor_scan.py"), CANON],
                           capture_output=True, text=True).returncode
    assert clean == 0, "scan exited %d on the clean canonical, expected 0" % clean
    print("PASS exit 1 on injected defect, exit 0 on clean canonical")


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    for t in TESTS:
        t()
    print("ALL soil_temp_floor_scan TESTS PASSED (%d)" % len(TESTS))
