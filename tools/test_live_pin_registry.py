#!/usr/bin/env python3
"""The live-pin registry is COMPLETE: every test pinned to the live canonical is registered (kickoff 60, ruling 3).

  1. COMPLETENESS: every file live_pin_registry.detect() flags is in LIVE_PINS or EXEMPT; a new pin fails by name.
  2. HONESTY: every registered file exists; no file is both live and exempt; every exemption gives a reason.
  3. THE RULED ENTRIES are live: PLA-544's group A and B, the A44 pin it missed, and the five suites never named
     in a data commit (annual_calendar, perennial_year_gate, hunt28, campaign_c, campaign_d).
  4. POSITIVE CONTROL (the detector can see each pin shape): A44's population string, the collision gate's
     canonical SHA, doc_roster's integer equality, gate_all's floor.
  5. POPULATION: 60 files detected (incl. this one; 62 before B5's two replays), 25 live-pin files carrying 60
     pins, 42 exempt (measured 2026-10-04 on
     b331e5f2). A deliberate change re-measures these with the files read.
Run: python3 -m pytest tools/test_live_pin_registry.py -q
SHIPS MUTATION-TESTED via mutate_live_pin_registry.py.
"""
import os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import live_pin_registry as R  # noqa: E402

DETECTED = R.detect()
RULED_LIVE = (
    "test_problem_id_collision_gate.py",            # PLA-544 group A
    "test_sourced_block_ratchet_gate.py", "test_bare_host_gate.py", "test_bare_host_scan.py",
    "test_annual_calendar.py", "test_perennial_year_gate.py", "test_gate_plants_per_pot_a60.py",   # group B
    "test_doc_roster_claim_gate.py",               # PLA-544 borderline
    "test_gate_planting_layout_a44.py",            # the pin PLA-544 missed
    "test_promote_pla161_hunt28_declaration.py", "test_campaign_c_reprice.py", "test_campaign_d_reprice.py",
)


class Completeness(unittest.TestCase):
    def test_every_detected_file_is_registered(self):
        missing = sorted(set(DETECTED) - set(R.LIVE_PINS) - set(R.EXEMPT))
        self.assertEqual(missing, [], "tests pinned to the live canonical but not in live_pin_registry")


class Honesty(unittest.TestCase):
    def test_every_registered_file_exists(self):
        gone = sorted(f for f in set(R.LIVE_PINS) | set(R.EXEMPT) if not os.path.exists(os.path.join(HERE, f)))
        self.assertEqual(gone, [])

    def test_no_file_is_both_live_and_exempt(self):
        self.assertEqual(sorted(set(R.LIVE_PINS) & set(R.EXEMPT)), [])

    def test_every_exemption_says_why_and_every_live_file_names_a_pin(self):
        self.assertEqual(sorted(f for f, why in R.EXEMPT.items() if not why.strip()), [])
        self.assertEqual(sorted(f for f, pins in R.LIVE_PINS.items() if not pins), [])


class RuledEntries(unittest.TestCase):
    def test_the_ruled_files_are_live_pins(self):
        self.assertEqual(sorted(f for f in RULED_LIVE if f not in R.LIVE_PINS), [])


class PositiveControl(unittest.TestCase):
    def test_the_detector_sees_each_pin_shape(self):
        sha, eq, fl, ps = DETECTED["test_problem_id_collision_gate.py"]
        self.assertIn("b331e5f2", sha)
        self.assertGreater(DETECTED["test_gate_planting_layout_a44.py"][3], 0, "A44's population string")
        self.assertGreater(DETECTED["test_doc_roster_claim_gate.py"][1], 0, "doc_roster's integer equality")
        self.assertGreater(DETECTED["test_gate_all.py"][2], 0, "gate_all's floor")


class Population(unittest.TestCase):
    def test_the_registry_population(self):
        self.assertEqual((len(DETECTED), len(R.LIVE_PINS), len(R.reverify_list()), len(R.EXEMPT)), (61, 25, 60, 43))


if __name__ == "__main__":
    unittest.main()
