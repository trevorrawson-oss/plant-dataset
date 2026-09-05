#!/usr/bin/env python3
"""Suite for promote_pla8_batch26 -- PLA-8 batch 26, the trees and shrubs.

BUILT TO THE PLA-215 BAR. Every guard family below is exercised by an injected defect that must
redden it, and the harness that drives those injections (`tools/mutate_pla8_batch26_suite.py`)
carries a MUTATION-APPLIED marker, a sentinel that must redden, and a positive control, or it exits
HARNESS DEAD.

THREE THINGS THIS SUITE DOES DELIBERATELY, EACH BECAUSE OF A PAST DEFECT.

1. **Every assertion names a message fragment unique to ONE guard.** A driver that asserts a SHARED
   fragment ("REFUSED") passes when the wrong guard fires, and the mutation survives while the test
   goes green.
2. **Clean input is asserted to PASS, not just defective input to fail.** A guard that refuses
   correct input is its own defect class and NO mutation finds it. The PLA-457 predicate in this
   batch is asserted both ways: an interval is refused, a bare co-mention is admitted.
3. **Counts are pinned to MEASURED values, never computed from the thing they validate.** The
   numbers below were read off a passing run and are re-measured, never retuned, if canonical moves.

NEW FAMILIES IN THIS BATCH: retirements-are-array-duplicates, the mixed type situation pinned per
row, the PLA-457 sulfur/oil hold, and pear template-twin divergence.
"""
import copy
import difflib
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import promote_fixture  # noqa: E402
import promote_pla8_batch26 as P  # noqa: E402

# ---- PINNED, MEASURED on the passing run. Re-measure on a canonical move; never retune to match.
BASE_SHA = "ce98b0a6f83cc04b380a6c3be3009709a7c6c3626b2611c88fafec1164997144"
N_CANONICAL_PROBLEMS = 39
N_TARGET_PROBLEMS = 38
N_RETIRED = 3
N_SPLIT_ROWS = 4
N_RENAMED = 1
N_UPGRADED = 28       # 26 coarse rows on four crops + the two `other` pear-decline rows
N_CARRIED = 10        # the pears' fine-typed rows
N_TWINS = 3           # pear entries with byte-identical canonical prose: Pear scab, Pear psylla, Pear decline
N_RUNGS = 115
N_CORRECTIONS = 210
N_SOURCE_KEYS = 125
N_HOUSE_SENTENCES = 761
CROPS = ("mulberry", "pawpaw", "pear-asian", "pear-european", "persimmon", "pomegranate")


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # REBUILD THE PRE-STATE FROM THE COMMITTED BASE, never from live canonical: the moment this
        # promote lands, a live read fails on a base mismatch and the suite goes permanently red.
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.pins, cls.batch = P.staged()
        cls.cm = cls.data["control_methods"]

    def fresh(self):
        return copy.deepcopy(self.batch)

    def fresh_pins(self):
        return copy.deepcopy(self.pins)

    def assertRefuses(self, fragment, fn, *a, **kw):
        """The fragment must be unique to ONE guard. A shared fragment lets a mutation survive."""
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg,
                      f"guard fired but with the wrong message.\n  wanted fragment: {fragment!r}\n"
                      f"  got: {msg!r}")

    def entry(self, crop, field, name):
        return next(e for e in self.batch[crop][field] if e["name"] == name)

    def multi_tier_rung_list(self, b):
        """First (crop, field, entry) whose ladder spans two tiers, so reversing it inverts."""
        for crop in CROPS:
            for field in ("pests", "diseases"):
                for e in b[crop][field]:
                    lad = e.get("control_ladder") or []
                    tiers = {P.TIER_RANK[self.cm[r["method"]]["tier"]] for r in lad}
                    if len(tiers) >= 2:
                        return crop, field, e
        self.fail("no ladder spans two tiers; the inversion test would be vacuous")


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(promote_fixture.pre_state(P.BASE_SHA)), BASE_SHA)

    def test_load_canonical_refuses_a_moved_base(self):
        """REACH THE ENTRY POINT: deleting the SHA check inside `load_canonical` must redden."""
        real = P.BASE_SHA
        try:
            P.BASE_SHA = "0" * 64
            self.assertRefuses("base SHA mismatch", P.load_canonical)
        finally:
            P.BASE_SHA = real

    def test_all_six_crops_are_staged(self):
        self.assertEqual(tuple(sorted(self.batch)), tuple(sorted(CROPS)))


class CleanInputPasses(Base):
    """A guard that refuses correct input is invisible to mutation testing. Assert both ways."""

    def test_reconcile_passes(self):
        n_canon, n_target = P.check_reconcile(self.pins, self.data)
        self.assertEqual(n_canon, N_CANONICAL_PROBLEMS)
        self.assertEqual(n_target, N_TARGET_PROBLEMS)

    def test_retirements_pass_and_count_is_pinned(self):
        self.assertEqual(P.check_retirements_are_array_duplicates(self.pins, self.data), N_RETIRED)

    def test_types_pass_and_split_is_pinned(self):
        self.assertEqual(P.check_type_upgrade(self.pins, self.data), (N_UPGRADED, N_CARRIED))

    def test_spec_match_passes(self):
        P.check_batch_matches_spec(self.pins, self.batch)

    def test_ladders_pass_and_rung_count_is_pinned(self):
        self.assertEqual(P.check_ladders(self.batch, self.cm), N_RUNGS)

    def test_hold_passes_on_clean_input(self):
        self.assertGreater(P.check_no_sulfur_oil_interval(self.batch), 0)

    def test_split_limbs_pass(self):
        P.check_split_rows_author_full_prose(self.pins, self.batch)

    def test_corrections_pass_and_count_is_pinned(self):
        self.assertEqual(P.check_corrections_anchored(self.batch, self.pins), N_CORRECTIONS)

    def test_sources_pass_and_count_is_pinned(self):
        self.assertEqual(P.check_sources_admitted(self.batch, self.data), N_SOURCE_KEYS)

    def test_no_precedent_copy(self):
        worst, at, comparisons = P.check_no_precedent_copy(self.batch, self.data)
        self.assertGreater(comparisons, 0, "zero comparisons would make this guard vacuous")
        self.assertLess(worst, P.COPY_THRESHOLD, f"worst copy score {worst:.3f} at {at}")

    def test_no_shipped_echo(self):
        checked, house = P.check_no_shipped_prose_echo(self.batch, self.data)
        self.assertGreater(checked, 0)
        self.assertEqual(house, N_HOUSE_SENTENCES)

    def test_no_multi_donor_recombination(self):
        checked, shipped = P.check_no_multi_donor_recombination(self.batch, self.data)
        self.assertGreater(checked, 0)
        self.assertGreater(shipped, 0)

    def test_no_intra_batch_twins(self):
        self.assertGreater(P.check_no_intra_batch_twins(self.batch), 0)

    def test_pear_twins_pass_and_count_is_pinned(self):
        twins, _div = P.check_pear_twin_divergence(self.pins, self.batch, self.data)
        self.assertEqual(twins, N_TWINS)

    def test_temperature_figures_warranted(self):
        P.check_temperature_figures_warranted(self.batch, self.pins, self.data)

    def test_machinery_regex_does_not_refuse_ordinary_english(self):
        self.assertIsNone(P.LADDER_VOCAB.search(
            "The same care applies to a division handed over the fence."))
        self.assertIsNone(P.LADDER_VOCAB.search(
            "This control method works best before the disease appears."))
        self.assertIsNotNone(P.LADDER_VOCAB.search("this is the cheapest rung on the ladder"))
        self.assertIsNotNone(P.LADDER_VOCAB.search("applies_to"))

    def test_hold_predicate_admits_a_bare_co_mention(self):
        """POSITIVE CONTROL for the PLA-457 predicate: sulfur and oil in one sentence with no
        duration is the legitimate 'never mix them' sentence and must pass."""
        self.assertFalse(P.states_sulfur_oil_interval("Never mix oil with sulfur in the same tank."))
        self.assertFalse(P.states_sulfur_oil_interval(
            "Spray oil in the dormant season. Sulfur goes on at green tip two weeks later."))


class ReconcileFamily(Base):
    def test_unaccounted_canonical_problem_is_refused(self):
        pins = self.fresh_pins()
        pins["mulberry"]["pests"] = [r for r in pins["mulberry"]["pests"] if r["name"] != "Birds"]
        self.assertRefuses("UNACCOUNTED", P.check_reconcile, pins, self.data)

    def test_phantom_source_is_refused(self):
        pins = self.fresh_pins()
        pins["mulberry"]["pests"][0]["from"] = "RENAME from 'No Such Problem'"
        self.assertRefuses("PHANTOM SOURCE", P.check_reconcile, pins, self.data)

    def test_phantom_retirement_is_refused(self):
        pins = self.fresh_pins()
        pins["_retired"].append({"crop": "mulberry", "field": "pests", "name": "Nope", "why": "x",
                                 "duplicate_of": {"field": "diseases", "name": "Nope"}})
        self.assertRefuses("PHANTOM RETIREMENT", P.check_reconcile, pins, self.data)

    def test_retiring_something_also_used_is_refused(self):
        pins = self.fresh_pins()
        pins["_retired"].append({"crop": "mulberry", "field": "pests", "name": "Birds", "why": "x",
                                 "duplicate_of": {"field": "diseases", "name": "Birds"}})
        self.assertRefuses("CONTRADICTION", P.check_reconcile, pins, self.data)

    def test_retirement_count_is_pinned(self):
        self.assertEqual(len(self.pins["_retired"]), N_RETIRED)
        self.assertEqual(
            sum(1 for _, _, r in P.spec_rows(self.pins) if r["from"].startswith("SPLIT")),
            N_SPLIT_ROWS)
        self.assertEqual(
            sum(1 for _, _, r in P.spec_rows(self.pins) if r["from"].startswith("RENAME")),
            N_RENAMED)


class RetirementFamily(Base):
    """A retirement must be a pests[] copy of a SURVIVING diseases[] entry."""

    def test_retirement_not_declared_as_duplicate_is_refused(self):
        pins = self.fresh_pins()
        pins["_retired"][0].pop("duplicate_of")
        self.assertRefuses("is not declared as a pests[] duplicate",
                           P.check_retirements_are_array_duplicates, pins, self.data)

    def test_retirement_with_no_diseases_twin_is_refused(self):
        """Retire a pests[] entry that has NO same-named diseases[] twin: a real pest, not a copy.
        The shape check passes (it is declared as a duplicate); the existence check must fire."""
        pins = self.fresh_pins()
        # mulberry's pests[] 'Birds' has no diseases[] twin; remove its pin row so reconcile is
        # not the guard under test, and declare it retired as a 'duplicate'.
        pins["mulberry"]["pests"] = [r for r in pins["mulberry"]["pests"] if r["name"] != "Birds"]
        pins["_retired"].append({"crop": "mulberry", "field": "pests", "name": "Birds", "why": "x",
                                 "duplicate_of": {"field": "diseases", "name": "Birds"}})
        self.assertRefuses("names a diseases[] twin that does not exist",
                           P.check_retirements_are_array_duplicates, pins, self.data)

    def test_retirement_whose_twin_is_not_carried_is_refused(self):
        pins = self.fresh_pins()
        pins["pear-asian"]["diseases"] = [r for r in pins["pear-asian"]["diseases"]
                                          if r["name"] != "Pear scab"]
        self.assertRefuses("is not carried by the pin table",
                           P.check_retirements_are_array_duplicates, pins, self.data)

    def test_retirement_of_a_real_pest_is_refused(self):
        """The pests[] copy must be TYPED as a disease. Build a fixture where a same-named
        diseases[] twin exists and is carried, but the pests[] entry is an insect."""
        pins = self.fresh_pins()
        data = copy.deepcopy(self.data)
        idx = P.by_slug(data)
        ghost = copy.deepcopy(idx["mulberry"]["diseases"][0])
        ghost["name"] = "Birds"
        idx["mulberry"]["diseases"].append(ghost)            # a diseases[] 'Birds' twin
        pins["mulberry"]["diseases"].append(dict(pins["mulberry"]["pests"][0], name="Birds"))
        pins["mulberry"]["pests"] = [r for r in pins["mulberry"]["pests"] if r["name"] != "Birds"]
        pins["_retired"].append({"crop": "mulberry", "field": "pests", "name": "Birds", "why": "x",
                                 "duplicate_of": {"field": "diseases", "name": "Birds"}})
        self.assertRefuses("not a disease sitting in the wrong array",
                           P.check_retirements_are_array_duplicates, pins, data)

    def test_zero_retirements_is_refused(self):
        pins = self.fresh_pins()
        pins["_retired"] = []
        self.assertRefuses("no retirements declared",
                           P.check_retirements_are_array_duplicates, pins, self.data)


class TypeFamily(Base):
    """The type situation is MIXED and pinned per row."""

    def test_pre_type_mismatch_is_refused(self):
        pins = self.fresh_pins()
        pins["mulberry"]["pests"][0]["pre_type"] = "insect"      # canonical says `pest`
        self.assertRefuses("re-measure, never retune", P.check_type_upgrade, pins, self.data)

    def test_coarse_type_not_upgraded_is_refused(self):
        """A coarse row whose post type equals its pre type must be refused. The branch is only
        reachable when the post value is ALSO a recognized gate type (an unrecognized one is
        refused a line earlier), and no such value is coarse on the real table. So the coarse
        table is widened to include `insect` for the duration, which makes pear-asian's codling
        moth (insect -> insect) read as 'coarse and not upgraded'. The mutation that disables the
        branch lets that fixture pass, which is exactly what this driver must catch."""
        pins = self.fresh_pins()
        real = P.COARSE_TYPES
        try:
            P.COARSE_TYPES = ("pest", "disease", "other", "insect")
            # pear-asian codling moth: canonical insect, pinned insect -> under the patched table
            # that is 'coarse and not upgraded' and must be refused.
            self.assertRefuses("was not upgraded off", P.check_type_upgrade, pins, self.data)
        finally:
            P.COARSE_TYPES = real

    def test_unrecognized_post_type_is_refused(self):
        pins = self.fresh_pins()
        pins["pear-asian"]["diseases"][-1]["type"] = "other"      # pear decline left as other
        self.assertRefuses("is not a recognized gate type", P.check_type_upgrade, pins, self.data)

    def test_fine_type_retyped_without_reason_is_refused(self):
        pins = self.fresh_pins()
        for r in pins["pear-european"]["diseases"]:
            if r["name"] == "Fire blight":
                r["type"] = "fungal"                              # bacterial -> fungal, no reason
        self.assertRefuses("with no retype_reason", P.check_type_upgrade, pins, self.data)

    def test_type_situation_must_be_mixed(self):
        """Drop every fine-typed crop from the pin table: the guard must refuse a table that is no
        longer mixed rather than report a clean upgrade."""
        pins = self.fresh_pins()
        for c in ("pear-asian", "pear-european"):
            pins[c] = {"pests": [], "diseases": []}
        self.assertRefuses("was measured MIXED", P.check_type_upgrade, pins, self.data)


class SpecMatchFamily(Base):
    def test_off_pin_id_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["id"] = "bird"
        self.assertRefuses("but pinned", P.check_batch_matches_spec, self.pins, b)

    def test_reverted_type_is_refused(self):
        b = self.fresh()
        for e in b["persimmon"]["pests"]:
            if e["id"] == "persimmon-psyllid":
                e["type"] = "pest"
        self.assertRefuses("but pinned", P.check_batch_matches_spec, self.pins, b)

    def test_dropped_entry_is_refused(self):
        b = self.fresh()
        b["pomegranate"]["pests"] = b["pomegranate"]["pests"][:-1]
        self.assertRefuses("entries, spec has", P.check_batch_matches_spec, self.pins, b)

    def test_appended_ghost_entry_is_refused(self):
        b = self.fresh()
        ghost = copy.deepcopy(b["pomegranate"]["pests"][0])
        ghost["name"] = "Ghost pest"
        b["pomegranate"]["pests"].append(ghost)
        self.assertRefuses("entries, spec has", P.check_batch_matches_spec, self.pins, b)


class LadderFamily(Base):
    def test_empty_ladder_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"] = []
        self.assertRefuses("non-empty list", P.check_ladders, b, self.cm)

    def test_null_ladder_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"] = None
        self.assertRefuses("non-empty list", P.check_ladders, b, self.cm)

    def test_unknown_method_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["method"] = "not_a_method"
        self.assertRefuses("unknown method", P.check_ladders, b, self.cm)

    def test_tier_inversion_is_refused(self):
        self.assertLess(P.TIER_RANK["biological"], P.TIER_RANK["soft_chemical"])
        b = self.fresh()
        _c, _f, e = self.multi_tier_rung_list(b)
        e["control_ladder"].reverse()
        self.assertRefuses("follows a higher tier", P.check_ladders, b, self.cm)

    def test_repeated_method_is_refused(self):
        b = self.fresh()
        lad = b["mulberry"]["pests"][0]["control_ladder"]
        lad.append(copy.deepcopy(lad[0]))
        self.assertRefuses("repeats method", P.check_ladders, b, self.cm)

    def test_method_not_reaching_type_is_refused(self):
        b = self.fresh()
        for e in b["mulberry"]["diseases"]:
            if e["id"] == "popcorn-disease":
                e["control_ladder"][0]["method"] = "handpick"   # insect/mollusk only
        self.assertRefuses("does not reach type", P.check_ladders, b, self.cm)

    def test_em_dash_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_beginner"] += " and then — stop."
        self.assertRefuses("em/en dash", P.check_ladders, b, self.cm)

    def test_machinery_vocabulary_in_a_note_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_seasoned"] = \
            "This is the cheapest rung to start with."
        self.assertRefuses("names the machinery", P.check_ladders, b, self.cm)

    def test_identical_registers_are_refused(self):
        b = self.fresh()
        r = b["mulberry"]["pests"][0]["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        self.assertRefuses("byte-identical", P.check_ladders, b, self.cm)

    def test_empty_note_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_beginner"] = "   "
        self.assertRefuses("missing or empty", P.check_ladders, b, self.cm)


class HoldFamily(Base):
    """PLA-457: no sulfur/oil interval may be stated, in a note or a correction."""

    def test_sulfur_oil_interval_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_seasoned"] += \
            " Do not apply sulfur within two weeks of an oil spray."
        self.assertRefuses("states a sulfur/oil interval", P.check_no_sulfur_oil_interval, b)

    def test_interval_in_a_correction_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0].setdefault("field_corrections", {})["prevention_seasoned"] = {
            "new": "Keep oil and sulfur 30 days apart.", "why": "x", "anchor": "y"}
        self.assertRefuses("states a sulfur/oil interval", P.check_no_sulfur_oil_interval, b)

    def test_predicate_both_ways(self):
        self.assertTrue(P.states_sulfur_oil_interval(
            "Wait 3 weeks after a sulfur application before spraying horticultural oil."))
        self.assertTrue(P.states_sulfur_oil_interval("Keep sulphur and oil a month apart."))
        self.assertFalse(P.states_sulfur_oil_interval("Sulfur and oil react on the leaf, so never combine them."))
        self.assertFalse(P.states_sulfur_oil_interval("Two weeks after the oil, check the leaves again."))


class CorrectionFamily(Base):
    def test_split_limb_inheriting_bundle_prose_is_refused(self):
        b = self.fresh()
        for e in b["pomegranate"]["pests"]:
            if e["id"] == "scale-insects":
                e["field_corrections"].pop("cause_seasoned", None)
        self.assertRefuses("may not inherit bundle prose",
                           P.check_split_rows_author_full_prose, self.pins, b)

    def _first_correction(self, b):
        for crop in CROPS:
            for field in ("pests", "diseases"):
                for e in b[crop][field]:
                    fc = e.get("field_corrections") or {}
                    for k in fc:
                        if k != "name":
                            return e, fc, k
        self.fail("no correction to mutate; this test would be vacuous")

    def test_correction_without_anchor_is_refused(self):
        b = self.fresh()
        _e, fc, k = self._first_correction(b)
        fc[k]["anchor"] = ""
        self.assertRefuses("is missing 'anchor'", P.check_corrections_anchored, b, self.pins)

    def test_correction_without_reason_is_refused(self):
        b = self.fresh()
        _e, fc, k = self._first_correction(b)
        fc[k]["why"] = ""
        self.assertRefuses("is missing 'why'", P.check_corrections_anchored, b, self.pins)

    def test_correction_to_a_non_prose_field_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0].setdefault("field_corrections", {})["severity"] = {
            "new": "high", "why": "x", "anchor": "y"}
        self.assertRefuses("is not a prose field", P.check_corrections_anchored, b, self.pins)

    def test_name_correction_disagreeing_with_the_pin_is_refused(self):
        b = self.fresh()
        e = self.entry("persimmon", "diseases", "Phytophthora root and crown rot")
        e = next(x for x in b["persimmon"]["diseases"] if x["name"] == e["name"])
        e.setdefault("field_corrections", {})["name"] = {
            "new": "Root and crown rot", "why": "x", "anchor": "y"}
        self.assertRefuses("the pin governs the value",
                           P.check_corrections_anchored, b, self.pins)

    def test_machinery_vocabulary_in_a_correction_is_refused(self):
        b = self.fresh()
        _e, fc, k = self._first_correction(b)
        fc[k]["new"] = "Start on the first rung of the ladder."
        self.assertRefuses("correction names the machinery",
                           P.check_corrections_anchored, b, self.pins)


class SourceFamily(Base):
    def test_unadmitted_source_key_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0].setdefault("sources", []).append("plantvillage")
        self.assertRefuses("absent from source_catalog", P.check_sources_admitted, b, self.data)

    def test_anchor_without_a_matching_source_is_refused(self):
        b = self.fresh()
        e = b["mulberry"]["pests"][0]
        e.setdefault("anchoring_urls", {})["umn_ext"] = {"url": "https://x", "verified": "2026-09-04"}
        self.assertRefuses("does not list it in sources", P.check_sources_admitted, b, self.data)


class CopyFamily(Base):
    def _shared_method_and_donor(self):
        """A method used by BOTH a batch rung and a shipped rung, with the shipped note."""
        shipped = {}
        for c in self.data["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    if r.get("note_beginner"):
                        shipped.setdefault(r["method"], r["note_beginner"])
        for crop in CROPS:
            for _f, p in P.problems(self.batch[crop]):
                for r in p["control_ladder"]:
                    if r["method"] in shipped:
                        return crop, p["name"], r["method"], shipped[r["method"]]
        self.fail("no method shared with the shipped corpus; this test would be vacuous")

    def test_verbatim_lift_from_a_shipped_note_is_refused(self):
        b = self.fresh()
        crop, name, method, donor = self._shared_method_and_donor()
        for _f, p in P.problems(b[crop]):
            if p["name"] == name:
                for r in p["control_ladder"]:
                    if r["method"] == method:
                        r["note_beginner"] = donor
        self.assertRefuses("scores", P.check_no_precedent_copy, b, self.data)

    def test_symmetric_metric_is_actually_symmetric(self):
        a, b = self._asymmetric_pair()
        fwd = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
        rev = difflib.SequenceMatcher(None, b, a, autojunk=False).ratio()
        self.assertNotAlmostEqual(fwd, rev, places=3,
                                  msg="the chosen pair is not asymmetric, so this test is vacuous")
        self.assertEqual(P._sym(a, b), P._sym(b, a))
        self.assertEqual(P._sym(a, b), max(fwd, rev))
        self.assertGreater(max(fwd, rev) - min(fwd, rev), 0.10)

    def _asymmetric_pair(self):
        notes = []
        for c in self.data["crops"]:
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    v = r.get("note_seasoned")
                    if v and 120 < len(v) < 260:
                        notes.append(v)
        best = None
        for i in range(min(200, len(notes))):
            for j in range(i + 1, min(200, len(notes))):
                x, y = notes[i], notes[j]
                d = abs(difflib.SequenceMatcher(None, x, y, autojunk=False).ratio()
                        - difflib.SequenceMatcher(None, y, x, autojunk=False).ratio())
                if best is None or d > best[0]:
                    best = (d, x, y)
        self.assertIsNotNone(best)
        return best[1], best[2]

    def test_autojunk_is_disabled_and_it_matters(self):
        notes = []
        for c in self.data["crops"]:
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    for k in P.ADVICE_FIELDS:
                        v = r.get(k)
                        if v and len(v) > 200:
                            notes.append(v)
        self.assertGreater(len(notes), 50, "too few long notes; this test would be vacuous")
        found = None
        for i in range(min(300, len(notes))):
            if found:
                break
            for j in range(i + 1, min(300, len(notes))):
                x, y = notes[i], notes[j]
                off = difflib.SequenceMatcher(None, x, y, autojunk=False).ratio()
                if off < P.COPY_THRESHOLD:
                    continue
                on = difflib.SequenceMatcher(None, x, y).ratio()
                if on < P.COPY_THRESHOLD:
                    found = (x, y, off, on)
                    break
        self.assertIsNotNone(
            found, "no pair where autojunk changes the verdict; this test would be vacuous")
        x, y, off, on = found
        self.assertGreaterEqual(off, P.COPY_THRESHOLD)
        self.assertLess(on, P.COPY_THRESHOLD)
        self.assertGreaterEqual(P._sym(x, y), P.COPY_THRESHOLD)

    def test_echo_of_a_shipped_sentence_is_refused(self):
        import collections
        donors = collections.Counter()
        for c in self.data["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    for k in P.ADVICE_FIELDS:
                        for sent in P.sentences(r.get(k) or ""):
                            donors[sent] += 1
        single = [x for x, n in donors.items() if n == 1]
        self.assertGreater(len(single), 0, "no single-donor sentence; this test would be vacuous")
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_seasoned"] += " " + single[0].capitalize()
        self.assertRefuses("echoes a shipped sentence", P.check_no_shipped_prose_echo, b, self.data)

    def test_house_phrasing_is_exempt_but_a_single_donor_lift_is_not(self):
        """Both directions of the exemption. A sentence with 2+ donors must pass; the mutation
        that makes EVERY sentence 'house' is caught by the single-donor half."""
        import collections
        donors = collections.Counter()
        for c in self.data["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    for k in P.ADVICE_FIELDS:
                        for sent in P.sentences(r.get(k) or ""):
                            donors[sent] += 1
        house = [x for x, n in donors.items() if n > 1]
        single = [x for x, n in donors.items() if n == 1]
        self.assertTrue(house and single, "need both classes; this test would be vacuous")
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_seasoned"] += " " + house[0].capitalize()
        P.check_no_shipped_prose_echo(b, self.data)          # house phrasing passes
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_seasoned"] += " " + single[0].capitalize()
        self.assertRefuses("echoes a shipped sentence", P.check_no_shipped_prose_echo, b, self.data)

    def test_whole_note_echo_is_never_exempt(self):
        whole = None
        for c in self.data["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    if r.get("note_beginner"):
                        whole = r["note_beginner"]
                        break
                if whole:
                    break
            if whole:
                break
        self.assertIsNotNone(whole)
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_beginner"] = whole
        self.assertRefuses("verbatim echo", P.check_no_shipped_prose_echo, b, self.data)

    def test_two_donor_recombination_is_refused(self):
        b = self.fresh()
        d1 = d2 = None
        for c in self.data["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    v = r.get("note_beginner") or ""
                    if len(v.split()) > 20:
                        if d1 is None:
                            d1 = v
                        elif d2 is None and v != d1:
                            d2 = v
        self.assertIsNotNone(d2, "need two donors; this test would be vacuous")
        half1 = " ".join(d1.split()[:12])
        half2 = " ".join(d2.split()[:12])
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_beginner"] = half1 + " " + half2
        self.assertRefuses("recombines runs from two shipped notes",
                           P.check_no_multi_donor_recombination, b, self.data)

    def test_nested_donor_runs_are_not_recombination(self):
        """POSITIVE CONTROL: one contiguous run from a single donor is house phrasing, not two
        lifts, and must not be flagged by the positional-overlap brake."""
        b = self.fresh()
        donor = None
        for c in self.data["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    v = r.get("note_beginner") or ""
                    if len(v.split()) > 25 and donor is None:
                        donor = v
        self.assertIsNotNone(donor, "no donor long enough; this test would be vacuous")
        run = " ".join(donor.split()[:14])
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_beginner"] = (
            "Keep the ground under the tree tidy through the season. " + run)
        P.check_no_multi_donor_recombination(b, self.data)

    def test_cross_crop_twin_note_is_refused(self):
        """Two crops in this batch sharing a method: copy one's note onto the other's rung."""
        b = self.fresh()
        by_method = {}
        for crop in CROPS:
            for _f, p in P.problems(b[crop]):
                for r in p["control_ladder"]:
                    by_method.setdefault(r["method"], []).append((crop, r))
        pair = next((v for v in by_method.values() if len({c for c, _ in v}) >= 2), None)
        self.assertIsNotNone(pair, "no method shared across two batch crops; test would be vacuous")
        (c1, r1), (c2, r2) = next((a, b_) for a in pair for b_ in pair if a[0] != b_[0])
        r2["note_beginner"] = r1["note_beginner"]
        self.assertRefuses("template twin", P.check_no_intra_batch_twins, b)


class PearTwinFamily(Base):
    """Byte-identical canonical prose across the pears: shared id, pinned divergence only."""

    def test_pear_twin_id_mismatch_is_refused(self):
        b = self.fresh()
        for e in b["pear-european"]["diseases"]:
            if e["name"] == "Pear scab":
                e["id"] = "pear-scab-eu"
        self.assertRefuses("shares its join key", P.check_pear_twin_divergence, self.pins, b, self.data)

    def test_unpinned_pear_divergence_is_refused(self):
        b = self.fresh()
        real = P.TWIN_DIVERGENCE_PINS
        try:
            P.TWIN_DIVERGENCE_PINS = {}
            for e in b["pear-asian"]["diseases"]:
                if e["name"] == "Pear decline":
                    e["control_ladder"] = e["control_ladder"] + [
                        {"method": "garden_sanitation", "note_beginner": "x", "note_seasoned": "y"}]
            # make the OTHER pear's ladder certainly different
            for e in b["pear-european"]["diseases"]:
                if e["name"] == "Pear decline":
                    e["control_ladder"] = [r for r in e["control_ladder"]
                                           if r["method"] != "garden_sanitation"]
            self.assertRefuses("cannot support two ladders unless the divergence is pinned",
                               P.check_pear_twin_divergence, self.pins, b, self.data)
        finally:
            P.TWIN_DIVERGENCE_PINS = real

    def test_mispinned_pear_divergence_is_refused(self):
        b = self.fresh()
        real = P.TWIN_DIVERGENCE_PINS
        try:
            P.TWIN_DIVERGENCE_PINS = dict(real, **{"Pear decline": (("no_such_method",), ())})
            for e in b["pear-asian"]["diseases"]:
                if e["name"] == "Pear decline":
                    e["control_ladder"] = e["control_ladder"] + [
                        {"method": "garden_sanitation", "note_beginner": "x", "note_seasoned": "y"}]
            for e in b["pear-european"]["diseases"]:
                if e["name"] == "Pear decline":
                    e["control_ladder"] = [r for r in e["control_ladder"]
                                           if r["method"] != "garden_sanitation"]
            self.assertRefuses("pinned +", P.check_pear_twin_divergence, self.pins, b, self.data)
        finally:
            P.TWIN_DIVERGENCE_PINS = real

    def test_pear_twin_guard_refuses_when_no_twins_reach_it(self):
        """Vacuity brake: if the twins stop reaching the guard it must say so, not report clean."""
        b = self.fresh()
        for crop in ("pear-asian", "pear-european"):
            for _f, p in P.problems(b[crop]):
                p["name"] = p["name"] + " (renamed)"
        self.assertRefuses("no pear template twins found",
                           P.check_pear_twin_divergence, self.pins, b, self.data)


class TemperatureFamily(Base):
    def test_unwarranted_temperature_figure_is_refused(self):
        b = self.fresh()
        b["mulberry"]["pests"][0]["control_ladder"][0]["note_seasoned"] += " Hold it below 137°F."
        self.assertRefuses("with no warrant",
                           P.check_temperature_figures_warranted, b, self.pins, self.data)

    def test_a_warranted_figure_passes(self):
        """POSITIVE CONTROL, constructed so it does not depend on whether the batch happens to
        carry a figure: the figure is placed in the note AND in a declared correction's anchor."""
        b = self.fresh()
        e = b["mulberry"]["pests"][0]
        e["control_ladder"][0]["note_seasoned"] += " Soaps and oils go on below 90°F."
        e.setdefault("field_corrections", {})["prevention_seasoned"] = {
            "new": "Spray only in cool weather.", "why": "x",
            "anchor": "uc_ipm: apply soaps or oils under 90°F"}
        self.assertGreaterEqual(
            P.check_temperature_figures_warranted(b, self.pins, self.data), 1)


class ApplyAndVerify(Base):
    """Reach the ENTRY POINT."""

    def test_apply_then_verify_round_trips(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        changed = P.verify_post(self.data, post, self.pins, self.batch)
        self.assertGreater(changed, 0)

    def test_untouched_crop_mutation_is_refused(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        idx["basil"]["pests"][0]["name"] = "Tampered"
        self.assertRefuses("untouched crop", P.verify_post, self.data, post, self.pins, self.batch)

    def test_top_level_key_mutation_is_refused(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        post["control_methods"]["water_spray"]["tier"] = "conventional"
        self.assertRefuses("top-level key", P.verify_post, self.data, post, self.pins, self.batch)

    def test_undeclared_prose_change_is_refused(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        target = None
        for crop in CROPS:
            for field in ("pests", "diseases"):
                for e in idx[crop].get(field) or []:
                    src = next(x for x in self.batch[crop][field] if x["name"] == e["name"])
                    declared = set(src.get("field_corrections") or {})
                    for fname in P.PROSE_FIELDS:
                        if fname in e and fname not in declared:
                            target = (crop, e, fname)
                            break
                    if target:
                        break
                if target:
                    break
            if target:
                break
        self.assertIsNotNone(target, "every prose field is declared; this test would be vacuous")
        _crop, entry, fname = target
        entry[fname] = "Silently rewritten with no declaration."
        self.assertRefuses("no correction was declared",
                           P.verify_post, self.data, post, self.pins, self.batch)

    def test_correction_not_matching_its_declaration_is_refused(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        done = False
        for crop in CROPS:
            for field in ("pests", "diseases"):
                for e in idx[crop][field]:
                    src = next(x for x in self.batch[crop][field] if x["name"] == e["name"])
                    for fname in (src.get("field_corrections") or {}):
                        if fname in P.PROSE_FIELDS:
                            e[fname] = "Declared, but not what was written."
                            done = True
                            break
                    if done:
                        break
                if done:
                    break
            if done:
                break
        self.assertTrue(done, "no correction to mutate; this test would be vacuous")
        self.assertRefuses("does not match its declared correction",
                           P.verify_post, self.data, post, self.pins, self.batch)

    def test_lost_key_is_refused(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        idx["mulberry"]["pests"][0].pop("symptoms_beginner", None)
        self.assertRefuses("lost keys", P.verify_post, self.data, post, self.pins, self.batch)

    def test_serialize_is_compact(self):
        blob = P.serialize({"a": 1, "b": "café"})
        self.assertEqual(blob, '{"a":1,"b":"café"}'.encode("utf-8"))
        self.assertNotIn(b"\\u", blob)
        self.assertFalse(blob.endswith(b"\n"))

    def test_retired_entries_are_absent_from_the_post_state(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        for r in self.pins["_retired"]:
            names = {e["name"] for e in idx[r["crop"]].get(r["field"]) or []}
            self.assertNotIn(r["name"], names)
            # ...and the diseases[] twin SURVIVES with a ladder
            twin = next(e for e in idx[r["crop"]]["diseases"] if e["name"] == r["name"])
            self.assertTrue(twin.get("control_ladder"))

    def test_no_disease_typed_entry_remains_in_pests(self):
        """The array/type mismatch this batch retires must be gone on these six crops."""
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        for c in CROPS:
            for e in idx[c]["pests"]:
                self.assertNotIn(e["type"], ("fungal", "bacterial", "viral", "disease"),
                                 f"{c}/{e['name']} is a disease still sitting in pests[]")

    def test_post_state_problem_count_is_pinned(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        n = sum(len(idx[c].get(f) or []) for c in CROPS for f in ("pests", "diseases"))
        self.assertEqual(n, N_TARGET_PROBLEMS)

    def test_every_target_entry_carries_an_id_a_fine_type_and_a_ladder(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        for c in CROPS:
            for f in ("pests", "diseases"):
                for e in idx[c].get(f) or []:
                    self.assertIsNotNone(e.get("id"), f"{c}/{e['name']} has no id")
                    self.assertIn(e.get("type"), P.TYPE_TARGETS, f"{c}/{e['name']} type")
                    self.assertTrue(e.get("control_ladder"), f"{c}/{e['name']} has no ladder")


if __name__ == "__main__":
    unittest.main(verbosity=2)
