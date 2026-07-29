#!/usr/bin/env python3
"""Behavior-level hardening tests for the inline whole_crop_gate.py checks that are NOT
importable `*_violations` functions (the §3 subset, the dispatch/floor branches). Each
test reproduces an incognito-redteam-audit (2026-06-27) injection in a SCRATCH copy of the
canonical and asserts the live gate now FAILS it (the hole is closed), with a negative
control proving the unmutated crop still PASSES (zero false positives on the certified 18).

Method mirrors the audit: deep-copy the canonical, mutate ONE crop, write a scratch JSON,
run `whole_crop_gate.py <slug> <scratch>` as a subprocess, read the exit code. READ-ONLY on
the canonical -- every mutation lands only in a tempfile.

Run: python3 tools/test_whole_crop_gate_hardening.py
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANONICAL = os.path.join(ROOT, "crops_data_final.json")
GATE = os.path.join(HERE, "whole_crop_gate.py")

_DATA = json.load(open(CANONICAL, encoding="utf-8"))


def _crop(slug):
    return copy.deepcopy(next(c for c in _DATA["crops"] if c["slug"] == slug))


def run_gate(mutated_crop):
    """Write a scratch dataset with `mutated_crop` swapped in for its slug, run the live
    gate on that slug, return (exit_code, combined_output)."""
    data = copy.deepcopy(_DATA)
    slug = mutated_crop["slug"]
    data["crops"] = [mutated_crop if c["slug"] == slug else c for c in data["crops"]]
    fd, path = tempfile.mkstemp(suffix=".json", prefix="gatehard_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
        p = subprocess.run([sys.executable, GATE, slug, path],
                           capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    finally:
        os.unlink(path)


def expect_fail(crop, needle, label):
    code, out = run_gate(crop)
    assert code != 0, f"{label}: expected gate FAIL, got PASS (exit 0)\n{out}"
    assert needle.lower() in out.lower(), f"{label}: FAIL but message missing {needle!r}\n{out}"
    print(f"  ok (caught): {label}")


def expect_pass(crop, label):
    code, out = run_gate(crop)
    assert code == 0, f"{label}: expected clean PASS, got FAIL (exit {code})\n{out}"
    print(f"  ok (clean):  {label}")


# ============================================================================
# C9 -- §3 pH nesting accepts an INVERTED preferred_range with tolerated present.
# The check guarded only nesting (tolerated[0]<=preferred[0] and preferred[1]<=
# tolerated[1]); preferred:[9,4] tolerated:[5.8,7.5] passed (Hero stat "9.0 to 4.0").
# ============================================================================
def test_c9_inverted_preferred_range():
    print("C9: §3 pH inverted preferred_range")
    # negative control: the unmutated certified crop passes
    expect_pass(_crop("carrot"), "C9 control: unmutated carrot")
    # the audit injection: preferred low/high inverted, still nested in tolerated
    bad = _crop("carrot")
    bad["ph"] = {**(bad.get("ph") or {}), "preferred_range": [9, 4],
                 "tolerated_range": [5.8, 7.5]}
    expect_fail(bad, "ph", "C9: inverted preferred_range [9,4]")
    # an inverted TOLERATED range is equally wrong
    bad2 = _crop("carrot")
    bad2["ph"] = {**(bad2.get("ph") or {}), "preferred_range": [6.0, 6.8],
                  "tolerated_range": [7.5, 5.8]}
    expect_fail(bad2, "ph", "C9: inverted tolerated_range [7.5,5.8]")


# ============================================================================
# re-audit #2 D9 (shape half) -- gate F must reject a truthy-placeholder anchoring URL.
# `url:"TODO"`/`"pending"` are truthy and passed the old `not au[s].get("url")` check; an
# anchoring URL must be a real http(s) URL. (The CONTENT half + `verified` honesty is the
# source-fidelity layer's job, not this gate -- `verified` is a date string here, not a bool.)
# ============================================================================
def _first_anchored_source(crop):
    """Find a (path-ish) anchoring_urls dict + a source id in it, to mutate its url."""
    found = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.endswith("anchoring_urls") and isinstance(v, dict):
                    for sid, entry in v.items():
                        if isinstance(entry, dict) and entry.get("url"):
                            found.append((v, sid))
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(crop)
    return found[0] if found else (None, None)


def test_d9_placeholder_url():
    print("D9: gate F rejects a truthy-placeholder anchoring url")
    expect_pass(_crop("carrot"), "D9 control: unmutated carrot (real http urls)")
    bad = _crop("carrot")
    au, sid = _first_anchored_source(bad)
    assert au is not None, "carrot should have an anchored source to mutate"
    au[sid]["url"] = "TODO"          # truthy placeholder -- passed the old `not url` check
    expect_fail(bad, "malformed", "D9: anchoring url 'TODO' (not an http URL)")


# ============================================================================
# re-audit #2 D16 -- the C/D dash/temp scan must check USER-FACING LIST elements, not just
# dict values. A novel list field laundering `--` / "degrees F" rendered to growers.
# ============================================================================
def test_d16_list_element_laundering():
    print("D16: C/D dash/temp scan reaches user-facing list elements")
    expect_pass(_crop("carrot"), "D16 control: unmutated carrot")
    bad = _crop("carrot")
    bad["care_bullets"] = ["Mulch deeply in spring.", "Water at 70 degrees F -- pinch the tips."]
    expect_fail(bad, "dash", "D16: em-dash laundered in a list element")
    bad2 = _crop("carrot")
    bad2["care_bullets"] = ["Keep soil at 70 degrees F."]
    expect_fail(bad2, "temp", "D16: 'degrees F' laundered in a list element")


# ============================================================================
# THE ARTICHOKE HARD-FLIPS (2026-07-28). Three checks shipped SOFT + standalone with the
# SAME stated trigger: artichoke's certification, because the herbaceous_perennial archetype
# had only one member and a one-member archetype cannot demonstrate that a floor is meetable.
# Artichoke certified as GS #121, so the trigger has fired and all three fold into the
# always-on suite. "Soft is a stage, not a resting state."
#
# These tests are what makes the flip real: a soft gate that nothing runs is indistinguishable
# from a gate that does not exist, which is the vacuity failure A47/A48 were written for.
# ============================================================================
def test_a49_zone_order_is_wired():
    """A49 -- zone_order_gate. Within one region, as the USDA zone RISES the ground gets
    warmer, so harvest should start EARLIER or equal. The defect it reproduces: asparagus
    ca_desert z9 (cooler) opened harvest a month AHEAD of z10 (warmer valley floor)."""
    print("A49: zone-order coherence wired into whole_crop_gate")
    expect_pass(_crop("artichoke"), "A49 control: unmutated artichoke")
    expect_pass(_crop("asparagus"), "A49 control: unmutated asparagus")
    # inject the ca_desert z9 defect shape: cooler zone leads the warmer one into harvest
    bad = _crop("artichoke")
    rbz = bad["regions"]["ca_desert"]["resolved_by_zone"]
    rbz["9"]["harvest"] = "Nov - Apr"     # cooler zone now starts a month AHEAD of z10
    rbz["10"]["harvest"] = "Dec - Apr"
    expect_fail(bad, "zone-order", "A49: cooler zone starts harvest before the warmer one")


def test_a50_harvest_duration_is_wired():
    """A50 -- harvest_duration_gate (STOP-SHAPE + RAMP-FIRST + RAMP-PROSE + REACH/END).
    Register row 27 phrased this flip as 'fold STOP-SHAPE into A39'; it lands as its own
    A-number instead, because the module carries four check families and splitting one gate
    across two A-numbers would leave three of them soft. STOP-SHAPE is inside it either way."""
    print("A50: harvest-duration coherence wired into whole_crop_gate")
    expect_pass(_crop("artichoke"), "A50 control: unmutated artichoke")
    expect_pass(_crop("asparagus"), "A50 control: unmutated asparagus")

    # STOP-SHAPE: an unknown stop signal. The app dispatches display on this value.
    bad = _crop("artichoke")
    bad["harvest_stop_rule"] = {**bad["harvest_stop_rule"], "signal": "vibes"}
    expect_fail(bad, "stop-shape", "A50: unknown harvest_stop_rule.signal")

    # STOP-SHAPE, the artichoke-specific half: inches attached to a NON-dimensional signal
    # assert a threshold no source published. Bract opening is a state, not a measurement.
    bad2 = _crop("artichoke")
    bad2["harvest_stop_rule"] = {**bad2["harvest_stop_rule"], "threshold_inches": [3.0, 4.0]}
    expect_fail(bad2, "threshold_inches", "A50: inches on a non-dimensional stop signal")

    # STOP-SHAPE, the asparagus half must stay strict: a DIMENSIONAL signal still needs its
    # number. Making the requirement conditional must not have made it optional.
    bad3 = _crop("asparagus")
    r = dict(bad3["harvest_stop_rule"]); r.pop("threshold_inches")
    bad3["harvest_stop_rule"] = r
    expect_fail(bad3, "threshold_inches", "A50: dimensional signal missing its threshold")

    # RAMP-FIRST: the [0,0] collapse -- a ramp that opens later than years_to_first_harvest
    # allows, presenting one end of a real source disagreement as certainty.
    bad4 = _crop("asparagus")
    bad4["harvest_ramp_weeks"] = [dict(e, weeks=[0, 0]) if e["bed_year"] == 2 else e
                                  for e in bad4["harvest_ramp_weeks"]]
    expect_fail(bad4, "ramp-first", "A50: ramp year 2 collapsed to [0,0]")


def test_a51_region_prose_is_wired():
    """A51 -- region_prose_gate, the R7 defect: region prose contradicting its own cell ratings.
    ROSTER-WIDE rather than archetype-scoped, because any crop with region prose can do this.
    The injection is the exact sentence found on certified asparagus."""
    print("A51: region-prose coherence wired into whole_crop_gate (roster-wide)")
    expect_pass(_crop("asparagus"), "A51 control: unmutated asparagus (repaired)")
    expect_pass(_crop("apple"), "A51 control: unmutated apple (a long-certified fruit tree)")

    # the live defect, reproduced: prose says a zone is unsuitable, the cell says marginal
    bad = _crop("asparagus")
    r = bad["regions"]["ca_south_coast"]
    r["region_notes_seasoned"] = r["region_notes_seasoned"] + " Frost-free zone 11 is unsuitable."
    expect_fail(bad, "region-prose", "A51: prose calls a marginal zone unsuitable")

    # and it must reach a fruit tree, since that is the half that was never audited
    bad2 = _crop("apple")
    r2 = bad2["regions"]["se_gulf"]
    r2["region_notes_beginner"] = "Zone 8 is unsuitable here."   # cell is fruits_reliably
    expect_fail(bad2, "region-prose", "A51: roster-wide reach onto a fruit tree")

    # NEGATIVE CONTROL that matters most: the comparative prose the first version flagged must
    # still pass. If this fails, the check has regressed to keyword matching.
    ok = _crop("asparagus")
    ok["regions"]["ca_south_coast"]["region_notes_seasoned"] = (
        "Zone 9 carries a productive bed, where a navel is only marginal and lime is unsuitable "
        "through most of Texas.")
    expect_pass(ok, "A51: comparative prose about other crops/regions stays clean")


def test_hard_flips_are_no_ops_off_scope():
    """Both flips are archetype-scoped, so a crop on another archetype must be untouched.
    If this ever fails, a flip has widened into a flood and the 38 open fruit-tree prose
    findings would start blocking unrelated certifications."""
    print("hard-flips: no-op off the herbaceous_perennial archetype")
    for slug in ("carrot", "apple", "peach", "strawberry", "thyme"):
        expect_pass(_crop(slug), f"off-scope control: {slug}")


if __name__ == "__main__":
    test_c9_inverted_preferred_range()
    test_d9_placeholder_url()
    test_d16_list_element_laundering()
    test_a49_zone_order_is_wired()
    test_a50_harvest_duration_is_wired()
    test_a51_region_prose_is_wired()
    test_hard_flips_are_no_ops_off_scope()
    print("\nALL HARDENING TESTS PASSED")
