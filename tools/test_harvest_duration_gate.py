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

from harvest_duration_gate import (  # noqa: E402
    duration_violations, ramp_violations, ramp_prose_violations, stop_rule_violations, STOP_SIGNALS,
    stated_duration, stated_end,
)

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


class ArtichokeProseIdiom(unittest.TestCase):
    """Verbatim staged artichoke prose. Artichoke is the SECOND crop this gate meets, and
    it broke the parser in two ways asparagus's shorter sentences never exposed:

      1. `harvest_clauses` split only on . and ; -- artichoke chains a planting window and a
         harvest window into one comma-separated sentence, so a PLANTING month or a seedling
         VERNALIZATION week count was attributed to harvest.
      2. `stated_end` took the FIRST `into|through <month>` match, so a start-of-harvest
         phrase beat the real end.

    All four of these were reported as violations against the staged cells and ALL FOUR were
    false positives. They are pinned here so the next crop's idiom cannot silently undo the fix.
    """

    def test_vernalization_week_count_is_not_a_harvest_duration(self):
        c = crop({("northern_tier", "5"): {
            "harvest": "Aug - Oct",
            "notes": ("This is the best-documented cold-region cycle: seed sown in the last "
                      "third of March, seedlings chilled about three weeks near 40°F at the "
                      "four to six leaf stage, transplanted late May to mid June, first buds "
                      "from mid August, and harvest continuing into early October until a "
                      "hard freeze."),
        }})
        self.assertEqual(duration_violations(c), [])

    def test_end_month_is_the_last_harvest_anchored_month_not_the_first(self):
        c = crop({("northern_tier", "6"): {
            "harvest": "Jul - Oct",
            "notes": ("Start seed indoors in February, chill the seedlings, and set them out "
                      "from late April. The longer season pulls first harvest forward into "
                      "July and lets picking run into October on secondary buds."),
        }})
        self.assertEqual(duration_violations(c), [])

    def test_transplanting_window_is_not_a_harvest_end(self):
        c = crop({("low_desert_az", "9"): {
            "harvest": "May - Jun",
            "notes": ("University of Arizona's Maricopa County calendar marks artichoke for "
                      "transplanting from mid January through March, with seed sown from early "
                      "November to mid December, and gives four to six months to harvest."),
        }})
        self.assertEqual(duration_violations(c), [])

    def test_planting_window_sharing_a_clause_with_harvest_is_not_a_harvest_end(self):
        c = crop({("low_desert_az", "10"): {
            "harvest": "May - Jun",
            "notes": ("University of Arizona's Yuma calendar puts artichoke in from September "
                      "through October and harvests it in May and June, running the plant "
                      "through the whole mild winter."),
        }})
        self.assertEqual(duration_violations(c), [])

    def test_a_duration_in_a_comma_continuation_still_belongs_to_its_harvest_clause(self):
        # asparagus warm_arid z8, verbatim. Splitting on commas severed "up to about ten
        # weeks" from the harvest clause it modifies, silently dropping REACH coverage on a
        # live cell. A segment inherits harvest-clause status from the preceding segment
        # within the same sentence; the inheritance resets at . and ;
        note = ("In the inland Southwest asparagus is winter hardy and tolerates the heat "
                "well; spears emerge in March as the soil warms, so harvest from March into "
                "mid May, up to about ten weeks once the bed is four years old, and stop "
                "when the spears thin toward a quarter inch. Then let the ferns grow through "
                "the long hot summer, kept watered, to recharge the crown before it goes "
                "dormant in winter.")
        self.assertEqual(stated_duration(note), (10, 10))
        self.assertEqual(stated_end(note), 5)  # "into mid May"

    def test_inheritance_does_not_leak_across_a_sentence_boundary(self):
        # the artichoke z5 shape: a vernalization week count in a sentence whose harvest
        # word appears only LATER must not be adopted
        note = ("Seedlings chilled about three weeks near 40°F, transplanted late May. "
                "Harvest runs into October.")
        self.assertIsNone(stated_duration(note))

    def test_a_real_end_disagreement_still_flags_in_artichoke_shaped_prose(self):
        # the fix must not buy its precision by going blind
        c = crop({("r", "7"): {
            "harvest": "Jul - Oct",
            "notes": ("Set them out from late April. The season pulls first harvest forward "
                      "into July and picking runs into August on secondary buds."),
        }})
        v = duration_violations(c)
        self.assertTrue(any("END" in x for x in v), v)


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


class RampProseCheck(unittest.TestCase):
    def test_prose_week_count_disagreeing_with_mature_ramp_flags(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_beginner": "Keep harvesting for about six to eight weeks, then stop."}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-PROSE", v[0])

    def test_prose_matching_mature_ramp_passes(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_beginner": "Keep harvesting for eight to ten weeks, then stop."}
        self.assertEqual(ramp_prose_violations(crop), [])

    def test_prose_stating_no_week_count_is_silent(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_beginner": "Harvest until the spears thin to pencil width."}
        self.assertEqual(ramp_prose_violations(crop), [])

    def test_hyphenated_compound_week_count_is_parsed(self):
        # the harvest_ready_seasoned shape: "a roughly six-to-eight-week spring window"
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_seasoned": "Harvest through a roughly six-to-eight-week spring window."}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-PROSE", v[0])

    # --- RAMP NARRATIVE (added 2026-08-22, PLA-6 Round 2) ---
    # A string that enumerates the ramp YEAR BY YEAR is the opposite of the defect this check
    # exists to catch. RAMP-PROSE was written against a stale FLAT week count contradicting the
    # ramp; a faithful per-bed-year narrative states several ranges, and the first-match parser
    # compared only the first of them to the MATURE entry and flagged correct prose. Register
    # row 26 has carried this as a known parser gap ("cannot parse ramp-narrative phrasing such
    # as 'lengthening to four and then six weeks'") that was previously worked around by hand,
    # by never naming the week numbers at all -- which is why the numbers a grower actually
    # wants were missing from the prose.

    def test_a_faithful_ramp_narrative_passes(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "full_harvest_notes_beginner": (
                    "About two to four weeks in year three, six to eight in year four, and "
                    "eight to ten weeks from year five onward.")}
        self.assertEqual(ramp_prose_violations(crop), [])

    def test_a_narrative_with_ONE_wrong_year_still_flags(self):
        # The whole point: enumerating several ranges must not become a way to smuggle a wrong
        # one past the check.
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "full_harvest_notes_beginner": (
                    "About two to four weeks in year three, nine to eleven in year four, and "
                    "eight to ten weeks from year five onward.")}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-NARRATIVE", v[0])
        self.assertIn("9 to 11", v[0])

    def test_a_single_range_is_still_measured_against_the_MATURE_entry(self):
        # Unchanged behavior for the one-figure case, which is the original defect class.
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_beginner": "Cut for two to four weeks."}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("RAMP-PROSE", v[0])

    def test_two_ranges_that_are_both_the_mature_entry_is_not_a_narrative(self):
        # Repeating the mature figure twice is not an enumeration; it must still pass, and for
        # the ordinary reason rather than by being mistaken for a narrative.
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "harvest_ready_beginner": "Eight to ten weeks, and eight to ten weeks again."}
        self.assertEqual(ramp_prose_violations(crop), [])

    # --- the check reads EVERY crop-level consumer string, not just harvest_ready_* ---
    # Narrowing it to harvest_ready_* is what let nine other asparagus strings keep
    # asserting a superseded figure while the gate reported clean.

    def test_disagreeing_count_in_description_flags(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "description_beginner": "After about six to eight weeks of cutting you stop."}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("description_beginner", v[0])

    def test_disagreeing_count_in_a_nested_list_of_objects_flags(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "growth_stages": [{"id": "x"},
                                  {"user_action_seasoned": "Cut through the roughly six-to-eight-week window."}]}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("growth_stages[1].user_action_seasoned", v[0])

    def test_count_in_a_sentence_with_no_harvest_verb_still_flags(self):
        # the notifications[].body_seasoned shape. The per-CELL checks filter to harvest
        # clauses to dodge fern/irrigation housekeeping, but at CROP level a week count is
        # about this crop's harvest even with no harvest verb in the sentence.
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "notifications": [{"body_seasoned": "You are near the end of the roughly "
                                                    "six-to-eight-week window."}]}
        v = ramp_prose_violations(crop)
        self.assertEqual(len(v), 1, v)
        self.assertIn("notifications[0].body_seasoned", v[0])

    def test_region_cells_are_not_scanned_by_the_crop_level_check(self):
        # per-cell prose is duration_violations' job, with its own clause filtering
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "regions": {"r": {"resolved_by_zone": {"7": {
                    "harvest": "Apr - May",
                    "notes": "Spears emerge in April; harvest for four to six weeks into May."}}}}}
        self.assertEqual(ramp_prose_violations(crop), [])

    def test_audit_record_and_citation_machinery_are_not_scanned(self):
        crop = {"slug": "c", "harvest_ramp_weeks": RAMP_OK,
                "verification_status": {"open_findings": [
                    {"finding": "was six to eight weeks before the widening"}]},
                "sources_summary": {"primary": [{"note": "cited six to eight weeks"}]}}
        self.assertEqual(ramp_prose_violations(crop), [])

    def test_crop_without_a_ramp_is_skipped_even_with_week_counts(self):
        crop = {"slug": "c", "description_beginner": "Harvest for six to eight weeks."}
        self.assertEqual(ramp_prose_violations(crop), [])


class LiveCanonicalClean(unittest.TestCase):
    """Done is a check that returns zero. RED until the promote lands."""

    def test_live_canonical_has_zero_findings(self):
        data = json.loads((REPO / "crops_data_final.json").read_text(encoding="utf-8"))
        findings = []
        for cr in data["crops"]:
            findings += [f"{cr['slug']} {v}" for v in duration_violations(cr)]
        self.assertEqual(findings, [])


class LiveCanonicalRampProseClean(unittest.TestCase):
    """RAMP-PROSE findings on live canonical. GREEN since the 2026-07-28 reconciliation
    promote (canonical f37b228b) moved harvest_ramp_weeks bed year 5 to [6, 10] and
    rewrote both harvest_ready registers off their bare six-to-eight-week counts."""

    def test_live_canonical_has_zero_ramp_prose_findings(self):
        data = json.loads((REPO / "crops_data_final.json").read_text(encoding="utf-8"))
        findings = []
        for cr in data["crops"]:
            findings += [f"{cr['slug']} {v}" for v in ramp_prose_violations(cr)]
        self.assertEqual(findings, [])


STOP_OK = {
    "signal": "spear_diameter",
    "threshold_inches": [0.25, 0.5],
    "note_beginner": "Stop cutting when new spears come up about as thick as a pencil.",
    "note_seasoned": "End the season when most spears thin to about pencil diameter.",
    "sources": ["uada_ext"],
}


class StopShapeCheck(unittest.TestCase):
    def test_absent_stop_rule_is_silent(self):
        self.assertEqual(stop_rule_violations({"slug": "c"}), [])

    def test_wellformed_stop_rule_passes(self):
        self.assertEqual(stop_rule_violations({"slug": "c", "harvest_stop_rule": STOP_OK}), [])

    def test_unknown_signal_flags(self):
        r = dict(STOP_OK, signal="vibes")
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("STOP-SHAPE" in x and "signal" in x for x in v), v)

    def test_descending_threshold_flags(self):
        r = dict(STOP_OK, threshold_inches=[0.5, 0.25])
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("threshold_inches" in x for x in v), v)

    def test_missing_register_flags(self):
        r = dict(STOP_OK); del r["note_seasoned"]
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("note_seasoned" in x for x in v), v)

    def test_missing_sources_flags(self):
        r = dict(STOP_OK, sources=[])
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("sources" in x for x in v), v)


# --------------------------------------------------------------------------------------------
# A SECOND STOP SIGNAL (artichoke GS arc, 2026-07-28).
#
# STOP_SIGNALS shipped as a vocabulary of one because asparagus was the only crop with a stop
# rule. Artichoke's signal is not a different threshold on the same observable, it is a DIFFERENT
# OBSERVABLE: you watch the bud's bracts for the moment they loosen and begin to spread, and you
# cut before that happens. Three T1 sources state it independently and none of them states a size:
#
#   UC IPM  "harvested when the buds have grown to maximum size but before the bracts or leaves
#            on the bud begin to spread open" + "Buds left on the plant past their prime tend to
#            become woody and bitter."
#   USU     "Harvest buds when they reach full size but before the bracts (bud leaves) begin to open."
#   UF/IFAS "High temperatures above 86F reduce the tenderness and compactness of the 'heart' and
#            cause buds to open quickly."
#
# So `threshold_inches` becomes CONDITIONAL ON THE SIGNAL rather than universally required. The
# gate demanded it unconditionally, which for a non-dimensional signal would force the author to
# invent a diameter -- false precision manufactured to satisfy a shape, which is the defect class
# this whole gate was written for. Keyed to the signal it stays fully strict for asparagus.
STOP_BRACT = {
    "signal": "bract_opening",
    "note_beginner": "Cut each bud while it is still tight and the scales are closed flat.",
    "note_seasoned": "Cut on bract tightness rather than size; once the bracts loosen the bud is "
                     "woody and bitter and is past use.",
    "sources": ["uc_ipm"],
}


class SecondStopSignalCheck(unittest.TestCase):
    def test_bract_opening_is_a_known_signal(self):
        self.assertIn("bract_opening", STOP_SIGNALS)

    def test_bract_opening_without_threshold_passes(self):
        """The whole point: a non-dimensional signal must not be forced to carry a diameter."""
        self.assertEqual(stop_rule_violations({"slug": "c", "harvest_stop_rule": STOP_BRACT}), [])

    def test_bract_opening_WITH_threshold_flags(self):
        """And the exemption is not a free pass. Attaching inches to a signal that is not a
        measurement asserts a precision no source published, so it is a defect in its own right."""
        r = dict(STOP_BRACT, threshold_inches=[3.0, 4.0])
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("threshold_inches" in x for x in v), v)

    def test_spear_diameter_still_requires_threshold(self):
        """ASPARAGUS REGRESSION. Making the requirement conditional must not make it optional."""
        r = dict(STOP_OK); del r["threshold_inches"]
        v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
        self.assertTrue(any("threshold_inches" in x for x in v), v)

    def test_bract_opening_still_needs_both_registers_and_sources(self):
        for kill in ("note_beginner", "note_seasoned"):
            r = dict(STOP_BRACT); del r[kill]
            v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
            self.assertTrue(any(kill in x for x in v), (kill, v))
        r = dict(STOP_BRACT, sources=[])
        self.assertTrue(any("sources" in x for x in
                            stop_rule_violations({"slug": "c", "harvest_stop_rule": r})))

    def test_near_miss_signal_still_bounces(self):
        for bogus in ("bract_open", "bracts_opening", "BRACT_OPENING", "bud_size"):
            r = dict(STOP_BRACT, signal=bogus)
            v = stop_rule_violations({"slug": "c", "harvest_stop_rule": r})
            self.assertTrue(any("signal" in x for x in v), (bogus, v))


class OverrideCheck(unittest.TestCase):
    def test_override_unreachable_within_band_flags(self):
        c = crop({("r", "7"): {
            "harvest": "Apr - Jun",
            "harvest_duration_weeks": [4, 6],
            "notes": "Spears emerge in April.",
        }})
        v = duration_violations(c)
        self.assertTrue(any("REACH" in x for x in v), v)

    def test_override_disagreeing_with_note_flags(self):
        c = crop({("r", "7"): {
            "harvest": "Apr - May",
            "harvest_duration_weeks": [4, 6],
            "notes": "Spears emerge in April; harvest for six to eight weeks into May.",
        }})
        v = duration_violations(c)
        self.assertTrue(any("OVERRIDE-PROSE" in x for x in v), v)

    def test_override_agreeing_with_note_and_band_passes(self):
        c = crop({("r", "7"): {
            "harvest": "Apr - May",
            "harvest_duration_weeks": [4, 6],
            "notes": "Spears emerge in April; harvest for four to six weeks into May.",
        }})
        self.assertEqual(duration_violations(c), [])


class LiveCanonicalAllClean(unittest.TestCase):
    """Done is a check that returns zero -- the aggregate this file's own main() reports:
    the union of ramp_violations, ramp_prose_violations, stop_rule_violations (crop-level)
    and duration_violations (per-cell) across every crop in the real canonical.

    GREEN since the 2026-07-28 reconciliation promote (canonical f37b228b) closed the
    2 asparagus RAMP-PROSE findings; STOP-SHAPE also became live rather than vacuous on
    that promote, which added the crop's first harvest_stop_rule.
    """

    def test_live_canonical_has_zero_aggregate_findings(self):
        data = json.loads((REPO / "crops_data_final.json").read_text(encoding="utf-8"))
        findings = []
        for cr in data["crops"]:
            crop_level = (ramp_violations(cr) + ramp_prose_violations(cr)
                          + stop_rule_violations(cr))
            findings += [f"{cr['slug']} {v}" for v in crop_level + duration_violations(cr)]
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
