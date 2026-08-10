#!/usr/bin/env python3
"""Sneak the defect at soil_temp_floor_scan and confirm it BOUNCES (CLAUDE.md TDD rule).

A gate isn't done until a defect has been injected into a SCRATCH COPY and caught. This
injects each variant of the class the scan exists to catch, plus the near-misses it must NOT
flag, so the check is proven tight rather than merely quiet on today's data.

PLA-160 additions -- the three false-zero shapes measured in
docs/2026-08-06-pla138-phase1-instrument-audit.md:
  * a cell whose `resolved_from.last_frost` is nulled must move to UNDETERMINED and keep the
    exit non-zero, never silently exit enforcement ("the escape hatch is a data field the
    defect controls");
  * the RULED suppression key must be scoped to the CELLS a human read (slug, region, zone),
    not the whole (region, zone) -- the utah_dixie ruling read 6 cucurbit cells and its old
    key covered every cell in the zone;
  * the warm-soil predicate is frost_effect == 'killed' AND germination floor >= 60F -- the
    old bare `g[0] >= 70` excluded all four corns and four beans, the exact protected class
    (germination-temp-is-optimal-not-minimum).

Runs under both pytest and `python3 tools/test_soil_temp_floor_scan.py` -- the guard lives in
the test body, never under __main__, because pytest never runs __main__ (that gap is exactly
what let test_build_corn_family_patch fail under one runner and skip under the other).
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

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
    return [h for h in S.scan(data) if (h[0], h[2], h[3]) not in S.RULED]


def _synth(plant_out, first_plant, last_frost):
    """A one-crop dataset passing the full predicate, for deterministic exit-code tests."""
    node = {"plant_out": plant_out, "first_plant_date": first_plant,
            "resolved_from": {"last_frost": last_frost} if last_frost else {}}
    return {"crops": [{"slug": "synthcrop", "germination_temp_f": [70, 95],
                       "frost_effect": "killed", "propagule": "seed",
                       "regions": {"r1": {"resolved_by_zone": {"7": node}}}}]}


def _run_file(data):
    d = tempfile.mkdtemp()
    p = os.path.join(d, "c.json")
    with open(p, "wb") as fh:
        fh.write(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode())
    r = subprocess.run([sys.executable, os.path.join(HERE, "soil_temp_floor_scan.py"), p],
                       capture_output=True, text=True)
    return r


# --------------------------------------------------------------------------
# PLA-160: the nulled-anchor escape hatch. THE mutation from the audit --
# "inject the defect, then null resolved_from.last_frost: the injected defect
# vanishes while the gate stays green."
# --------------------------------------------------------------------------

def test_nulled_anchor_is_undetermined_not_clean():
    data = _synth("Jan 15 - Feb 15", "Jan 15", "Jan 15")   # sown ON frost: a hit
    assert len(S.scan(data)) == 1, "premise: the injected defect is caught"
    data["crops"][0]["regions"]["r1"]["resolved_by_zone"]["7"]["resolved_from"] = {}
    assert not S.scan(data), "premise: nulling the anchor removes the hit"
    und = S.undetermined(data)
    assert len(und) == 1 and und[0][0] == "synthcrop", \
        "nulled anchor must surface as UNDETERMINED, not silently exit enforcement"
    print("PASS nulled anchor surfaces as UNDETERMINED")


def test_exit_codes_hit_undetermined_clean():
    """1 = defect, 3 = zero-hits-but-unevaluable (not flip-safe), 0 = honest clean."""
    r = _run_file(_synth("Jan 15 - Feb 15", "Jan 15", "Jan 15"))
    assert r.returncode == 1, (r.returncode, r.stdout)
    r = _run_file(_synth("Jan 15 - Feb 15", "Jan 15", None))
    assert r.returncode == 3, \
        "nulled anchor must exit 3 (UNDETERMINED), got %d\n%s" % (r.returncode, r.stdout)
    assert "soil_temp_floor_scan UNDETERMINED" in r.stdout, r.stdout
    r = _run_file(_synth("Apr 1 - May 1", "Apr 1", "Mar 1"))   # sown 31 days after frost
    assert r.returncode == 0, (r.returncode, r.stdout)
    print("PASS exit 1 on defect, 3 on unevaluable, 0 on honest clean")


def test_live_canonical_undetermined_population_is_reported():
    """The measured blind spot: cells lacking resolved_from.last_frost (the frost-free
    regions). They must be counted, never folded into a green."""
    und = S.undetermined(_base())
    assert und, "the frost-free regions lost their UNDETERMINED accounting"
    regions = {u[2] for u in und}
    assert "hawaii_tropical" in regions, regions
    print("PASS live canonical reports %d UNDETERMINED cells across %s"
          % (len(und), sorted(regions)))


# --------------------------------------------------------------------------
# PLA-160: the RULED key is scoped to the cells the ruling actually read.
# --------------------------------------------------------------------------

def test_ruled_key_is_cell_scoped_not_zone_scoped():
    """A NEW crop hitting in utah_dixie z8 must be REPORTED -- the 2026-07-29 ruling read
    six cucurbit cells, not the zone."""
    data = _base()
    cell = _cell(data, "okra", "utah_dixie", "8")
    cell["plant_out"] = "Mar 15 - Mar 29"
    cell["first_plant_date"] = "Mar 15"
    hits = [h for h in _unruled(data)
            if h[0] == "okra" and h[2] == "utah_dixie" and h[3] == "8"]
    assert hits, ("okra injected into utah_dixie z8 was absorbed by the ruling -- "
                  "the suppression key is coarser than its evidence")
    print("PASS a new utah_dixie z8 hit is reported, not absorbed by the ruling")


def test_ruled_exception_is_suppressed_but_still_visible():
    """The six cucurbit cells the ruling read must not be reported, must still be returned
    by the raw scan, and each ruling must carry a reason."""
    data = _base()
    raw = S.scan(data)
    ud = [h for h in raw if h[2] == "utah_dixie" and h[3] == "8"
          and (h[0], h[2], h[3]) in S.RULED]
    assert len(ud) == 6, "the six ruled cucurbit cells no longer match the raw scan: %s" % ud
    assert not [h for h in _unruled(data)
                if (h[0], h[2], h[3]) in S.RULED], "ruled exception leaked into the report"
    for key, reason in S.RULED.items():
        assert len(key) == 3, "RULED keys must be (slug, region, zone): %r" % (key,)
        assert reason and len(reason) > 40 and "USU" in reason, \
            "a RULED entry must carry a substantive sourced reason"
    print("PASS ruled cells suppressed, still visible, cell-scoped, and carry reasons")


# --------------------------------------------------------------------------
# PLA-160: the predicate covers the protected class and does not flood.
# --------------------------------------------------------------------------

def test_frost_killed_corn_is_in_scope():
    """sweet-corn (germ floor 60, frost_effect killed) was invisible under g[0] >= 70."""
    data = _base()
    cell = _cell(data, "sweet-corn", "ca_desert", "10") if \
        "ca_desert" in _crop(data, "sweet-corn").get("regions", {}) else None
    if cell is None:
        region = next(iter(_crop(data, "sweet-corn")["regions"]))
        zone = next(iter(_crop(data, "sweet-corn")["regions"][region]["resolved_by_zone"]))
        cell = _cell(data, "sweet-corn", region, zone)
    lf = (cell.get("resolved_from") or {}).get("last_frost")
    if not lf:
        cell["resolved_from"] = {"last_frost": "Apr 15"}
        lf = "Apr 15"
    cell["plant_out"] = "%s - May 30" % lf
    cell["first_plant_date"] = lf
    assert any(h[0] == "sweet-corn" for h in S.scan(data)), \
        "a frost-killed corn sown ON last frost is invisible -- the 70F floor is back"
    print("PASS frost-killed corn with germ floor 60 is in scope")


def test_hardy_annual_is_not_flooded():
    """dill / calendula (frost_effect foliage_damaged) legitimately open before last frost;
    they must stay OUT of scope even though their germination floor is 60."""
    data = _base()
    flagged = {h[0] for h in S.scan(data)}
    for slug in ("dill", "calendula", "borage", "sweet-alyssum"):
        assert slug not in flagged, \
            "%s (hardy, foliage_damaged) flagged -- the predicate lost the frost filter" % slug
    # prove frost_effect is what excludes it, not luck
    _crop(data, "dill")["frost_effect"] = "killed"
    assert any(h[0] == "dill" for h in S.scan(data)), \
        "frost_effect is not what was excluding dill -- check the predicate"
    print("PASS hardy annuals excluded, and frost_effect is provably the reason")


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
    crop["frost_effect"] = "killed"
    assert any(h[0] == "rosemary" for h in _unruled(data)), \
        "propagule filter is not what was excluding rosemary -- check the scan"
    print("PASS ignores transplanted crops, and propagule is provably the reason")


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


def test_ignores_cool_season_crop():
    """A crop that does not need warm soil may be sown at frost."""
    data = _base()
    flagged = {h[0] for h in _unruled(data)}
    for c in data["crops"]:
        g = c.get("germination_temp_f")
        if isinstance(g, list) and len(g) == 2 and isinstance(g[0], (int, float)):
            assert not (g[0] < S.WARM_SOIL_F and c["slug"] in flagged), \
                "cool-soil crop %s flagged" % c["slug"]
    print("PASS ignores crops that do not require warm soil")


# --------------------------------------------------------------------------
# The live-canonical lead population. NOT a cleanliness assertion any more:
# the corrected predicate surfaces real unread leads (that is the finding, per
# PLA-160 -- do not "fix" the rise by loosening the predicate). The set is
# pinned as a CEILING: shrinking means a lead was adjudicated (fine); a hit
# outside the pinned set means new data arrived and must be read.
# --------------------------------------------------------------------------

OPEN_LEAD_CROPS = {
    "dry-bean", "edamame", "field-corn", "flint-corn", "popcorn", "sweet-corn",
    "green-beans-bush", "pole-beans",
}


def test_live_canonical_leads_are_the_measured_population():
    hits = _unruled(_base())
    crops = {h[0] for h in hits}
    assert crops <= OPEN_LEAD_CROPS, \
        ("unruled hits outside the 2026-08-10 measured lead population -- new data or a "
         "regression, read them: %s" % sorted(crops - OPEN_LEAD_CROPS))
    print("PASS live canonical: %d unruled lead cells, all within the measured corn/bean "
          "population (%s)" % (len(hits), sorted(crops)))


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    for t in TESTS:
        t()
    print("ALL soil_temp_floor_scan TESTS PASSED (%d)" % len(TESTS))
