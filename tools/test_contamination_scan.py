#!/usr/bin/env python3
"""Sneak the defect at contamination_scan and confirm it BOUNCES (CLAUDE.md TDD rule).

The defect class (PLA-160 item 4): 0/0 rendered as 0%. The scan printed "Mean overall
contamination across the 7 non-walked crops: 0%" where all 7 were empty shells with ZERO
leaves passing classify() -- measured-clean and measured-nothing rendered identically, and
it printed the reassuring one (`x/0` guarded to `0.0` on line 126).

Contract under test: a crop with an empty denominator renders `n/a (0 leaves measured)`,
never a percentage; the mean is taken over MEASURABLE crops only, with the excluded count
stated; and when every member has an empty denominator the scan refuses the mean outright,
in its own name.

Runs under both pytest and `python3 tools/test_contamination_scan.py`.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "contamination_scan.py")

PROSE = ("This sturdy plant thrives in loose fertile soil with steady moisture and "
         "benefits from a thick straw mulch through the hottest weeks of summer.")


def _crop(slug, prose=None):
    c = {"slug": slug}
    if prose:
        c["description_beginner"] = prose
    return c


def _run(crops):
    d = tempfile.mkdtemp()
    p = os.path.join(d, "c.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"crops": crops}, fh, ensure_ascii=False, separators=(",", ":"))
    return subprocess.run([sys.executable, SCRIPT, p], capture_output=True, text=True)


def test_empty_denominator_renders_na_not_zero_percent():
    """THE DEFECT: an all-shell roster used to print 'Mean overall contamination ... 0%'."""
    r = _run([_crop("shell-a"), _crop("shell-b")])
    assert "n/a" in r.stdout, r.stdout[-600:]
    mean_lines = [ln for ln in r.stdout.splitlines() if "Mean overall contamination" in ln]
    assert mean_lines, r.stdout[-600:]
    assert not re.search(r"Mean overall contamination[^\n]*\b0%", mean_lines[0]), \
        "measured-nothing rendered as measured-clean: %s" % mean_lines[0]
    assert "0 leaves measured" in r.stdout or "empty denominator" in r.stdout, r.stdout[-600:]
    print("PASS all-shell roster refuses the 0% mean, renders n/a")


def test_per_crop_row_shows_na_for_unmeasured():
    r = _run([_crop("shell-a"), _crop("real-b", PROSE)])
    row = next(ln for ln in r.stdout.splitlines() if ln.startswith("| shell-a"))
    assert "n/a" in row, row
    assert "0%" not in row, "an unmeasured crop's row shows a percentage: %s" % row
    print("PASS unmeasured crop's row renders n/a, not 0%")


def test_mean_is_over_measurable_crops_only_with_exclusion_stated():
    """Two contaminated measurable crops + one shell: the mean must be 100% over 2, with
    the shell excluded and the exclusion stated -- never 67% over 3."""
    r = _run([_crop("real-a", PROSE), _crop("real-b", PROSE), _crop("shell-c")])
    mean_line = next(ln for ln in r.stdout.splitlines()
                     if "Mean overall contamination" in ln)
    assert "100%" in mean_line, mean_line
    assert "1" in mean_line and ("unmeasured" in mean_line or "excluded" in mean_line), \
        "the excluded shell is not stated on the mean line: %s" % mean_line
    print("PASS mean over measurable crops only, exclusion stated")


def test_high_contamination_denominator_is_measurable_count():
    r = _run([_crop("real-a", PROSE), _crop("real-b", PROSE), _crop("shell-c")])
    line = next(ln for ln in r.stdout.splitlines() if ">=60% contaminated" in ln)
    assert "of 2" in line, "the >=60%% denominator must be measurable crops, not all: %s" % line
    print("PASS >=60% line uses the measurable denominator")


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    for t in TESTS:
        t()
    print("ALL contamination_scan TESTS PASSED (%d)" % len(TESTS))
