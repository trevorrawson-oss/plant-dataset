#!/usr/bin/env python3
"""Tests for tools/harvest_duration_gate.py (the asparagus harvest-duration pass, 2026-07-27).

Run: python3 tools/test_harvest_duration_gate.py

RED-proof: the historical-reproduction test runs the gate against the PRE-FIX canonical extracted
from git (commit 7870051, canonical 02fbb5e8) and must find exactly the six defective cells the
pass repaired. The live-canonical test asserts 0 findings and stays RED until the promote lands.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

from harvest_duration_gate import duration_violations, ramp_violations  # noqa: E402

PRE_FIX_COMMIT = "7870051"  # canonical 02fbb5e8, before the duration-pass repairs


def crop(cells):
    """Minimal synthetic crop: {(region, zone): {harvest, notes}}."""
    regions = {}
    for (rk, z), cell in cells.items():
        regions.setdefault(rk, {"resolved_by_zone": {}})["resolved_by_zone"][z] = cell
    return {"slug": "synthetic", "regions": regions}


RAMP_OK = [
    {"bed_year": 1, "weeks": [0, 0]}, {"bed_year": 2, "weeks": [0, 2]},
    {"bed_year": 3, "weeks": [2, 4]}, {"bed_year": 4, "weeks": [6, 8]},
    {"bed_year": 5, "weeks": [8, 10]},
]
RAMP_HISTORICAL_DEFECT = [
    {"bed_year": 1, "weeks": [0, 0]}, {"bed_year": 2, "weeks": [0, 0]},
    {"bed_year": 3, "weeks": [2, 3]}, {"bed_year": 4, "weeks": [6, 8]},
    {"bed_year": 5, "weeks": [8, 10]},
]


class RampFirstCheck(unittest.TestCase):
    def test_ramp_opening_later_than_the_earliest_possible_year_flags(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_HISTORICAL_DEFECT,
                "years_to_first_harvest": [2, 3]}
        v = ramp_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-FIRST", v[0])

    def test_ramp_opening_in_the_earliest_possible_year_passes(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "years_to_first_harvest": [2, 3]}
        self.assertEqual(ramp_violations(crop), [])

    def test_crop_without_a_ramp_is_skipped(self):
        self.assertEqual(ramp_violations({"slug": "c"}), [])

    def test_ramp_with_no_nonzero_year_flags(self):
        crop = {"slug": "c",
                "harvest_ramp_weeks": [{"bed_year": 1, "weeks": [0, 0]}],
                "years_to_first_harvest": [2, 3]}
        v = ramp_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-FIRST", v[0])


class ReachCheck(unittest.TestCase):
    def test_duration_too_short_to_touch_last_month_flags(self):
        c = crop({("r", "7"): {
            "harvest": "Apr - Jun",
            "notes": "Spears emerge in April; harvest for four to six weeks into June.",
        }})
        v = duration_violations(c)
        self.assertEqual(len(v), 1, v)
        self.assertIn("REACH", v[0])

    def test_duration_that_reaches_last_month_passes(self):
        c = crop({("r", "8"): {
            "harvest": "Apr - Jun",
            "notes": "Spears emerge in April; harvest for six to eight weeks into June.",
        }})
        self.assertEqual(duration_violations(c), [])


class EndCheck(unittest.TestCase):
    def test_note_end_month_disagreeing_with_field_flags(self):
        c = crop({("r", "6"): {
            "harvest": "Apr - Jun",
            "notes": "Spears start in April; cut for six to eight weeks into May.",
        }})
        v = duration_violations(c)
        self.assertEqual(len(v), 1, v)
        self.assertIn("END", v[0])

    def test_through_a_and_b_uses_the_later_month(self):
        c = crop({("r", "8"): {
            "harvest": "Mar - May",
            "notes": "Harvest through March and April for six to eight weeks.",
        }})
        v = duration_violations(c)
        self.assertEqual(len(v), 1, v)
        self.assertIn("END", v[0])
        self.assertIn("April", v[0])

    def test_mid_month_modifier_still_matches_field_end(self):
        c = crop({("r", "9"): {
            "harvest": "Apr - Jun",
            "notes": "Spears start in April; harvest into mid June.",
        }})
        self.assertEqual(duration_violations(c), [])

    def test_fern_and_irrigation_housekeeping_is_not_a_harvest_clause(self):
        # the ca_desert z10 false-positive shape: "Cut irrigation ... cut them to the
        # ground ... set crowns from November into early February" must not be read
        # as a harvest end
        c = crop({("r", "10"): {
            "harvest": "Mar - Apr",
            "notes": ("Spears follow in March and April. Cut irrigation in September or "
                      "October and let the ferns dry down, then cut them to the ground, "
                      "and set crowns any time from November into early February."),
        }})
        self.assertEqual(duration_violations(c), [])


class StartCheck(unittest.TestCase):
    def test_note_emergence_month_disagreeing_with_field_flags(self):
        c = crop({("r", "5"): {
            "harvest": "Apr - Jun",
            "notes": "Spears break ground in early to mid May; harvest for six to eight weeks into June.",
        }})
        v = duration_violations(c)
        self.assertEqual(len(v), 1, v)
        self.assertIn("START", v[0])


class Scope(unittest.TestCase):
    def test_day_granular_windows_are_skipped(self):
        c = crop({("r", "7"): {
            "harvest": "Mar 20 - Apr 15",
            "notes": "Harvest for four weeks into June.",
        }})
        self.assertEqual(duration_violations(c), [])

    def test_two_cycle_comma_windows_are_skipped(self):
        c = crop({("r", "7"): {
            "harvest": "Apr - Jun, Sep - Oct",
            "notes": "Harvest for four weeks into June.",
        }})
        self.assertEqual(duration_violations(c), [])

    def test_noteless_cells_are_skipped(self):
        c = crop({("r", "7"): {"harvest": "Apr - Jun"}})
        self.assertEqual(duration_violations(c), [])


class HistoricalReproduction(unittest.TestCase):
    """The gate must reproduce the shipped defect exactly on the pre-fix canonical."""

    EXPECTED_CELLS = {
        ("asparagus", "mid_south", "7"),
        ("asparagus", "mid_atlantic", "7"),
        ("asparagus", "northern_tier", "5"),
        ("asparagus", "northern_tier", "6"),
        ("asparagus", "northern_tier", "7"),
        ("asparagus", "utah_dixie", "8"),
    }

    def test_pre_fix_canonical_flags_exactly_the_six_repaired_cells(self):
        raw = subprocess.run(
            ["git", "show", f"{PRE_FIX_COMMIT}:crops_data_final.json"],
            cwd=REPO, capture_output=True, check=True,
        ).stdout
        data = json.loads(raw)
        hit = set()
        n = 0
        for cr in data["crops"]:
            for v in duration_violations(cr):
                # violation strings are "region z<zone>: KIND: ..."
                rk, rest = v.split(" z", 1)
                z = rest.split(":", 1)[0]
                hit.add((cr["slug"], rk, z))
                n += 1
        self.assertEqual(hit, self.EXPECTED_CELLS)
        self.assertEqual(n, 8)  # mid_south z7 + mid_atlantic z7 each carry REACH and END


class LiveCanonicalClean(unittest.TestCase):
    """Done is a check that returns zero. RED until the promote lands."""

    def test_live_canonical_has_zero_findings(self):
        data = json.loads((REPO / "crops_data_final.json").read_text(encoding="utf-8"))
        findings = []
        for cr in data["crops"]:
            findings += [f"{cr['slug']} {v}" for v in duration_violations(cr)]
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
