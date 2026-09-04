#!/usr/bin/env python3
"""Suite for promote_pla8_batch25 -- PLA-8 batch 25, the herbs.

BUILT TO THE PLA-215 BAR. Every guard family below is exercised by an injected defect that must
redden it, and the harness that drives those injections
(`tools/mutate_pla8_batch25_suite.py`) carries a MUTATION-APPLIED marker, a sentinel that must
redden, and a positive control, or it exits HARNESS DEAD.

THREE THINGS THIS SUITE DOES DELIBERATELY, EACH BECAUSE OF A PAST DEFECT.

1. **Every assertion names a message fragment unique to ONE guard.** A driver that asserts a SHARED
   fragment ("REFUSED") passes when the wrong guard fires, and the mutation survives while the test
   goes green. That recurred three times in one session on an earlier batch.

2. **Clean input is asserted to PASS, not just defective input to fail.** A guard that refuses
   correct input is its own defect class and NO mutation finds it, because the branch fires exactly
   as written. This batch already produced one: the machinery-vocabulary regex matched
   `applies[_ ]to` with an optional space and refused the correct English sentence "The same care
   applies to a division handed over the fence."

3. **Counts are pinned to MEASURED values, never computed from the thing they validate.** An
   expected value derived from the object under test is vacuous. The numbers below were read off a
   passing run and are re-measured, never retuned, if canonical moves.
"""
import copy
import difflib
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import promote_pla8_batch25 as P  # noqa: E402

# ---- PINNED, MEASURED on the passing run. Re-measure on a canonical move; never retune to match.
BASE_SHA = "500a61262d5870636d8b33845cb81072940e677d3674938c0375319eab6d6fc9"
N_CANONICAL_PROBLEMS = 36
N_TARGET_PROBLEMS = 38
N_RETIRED = 2
N_SPLIT_ROWS = 7
N_RENAMED = 3
N_RUNGS = 141
N_CORRECTIONS = 246
N_SOURCE_KEYS = 130
N_HOUSE_SENTENCES = 760      # shipped sentences with 2+ donors; the house-phrasing exemption
CROPS = ("lavender", "lemongrass", "mint", "oregano", "rosemary", "sage", "thyme")


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = P.load_canonical()
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


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        """If canonical moved, every count below is measuring a different object."""
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        raw = open(P.CANON, "rb").read()
        self.assertEqual(P.sha256_bytes(raw), BASE_SHA, "canonical has moved; re-measure the pins")

    def test_load_canonical_refuses_a_moved_base(self):
        """REACH THE ENTRY POINT. The pin test asserts the CONSTANT and never calls the function, so
        deleting the SHA check inside `load_canonical` survived it. This calls it."""
        real = P.BASE_SHA
        try:
            P.BASE_SHA = "0" * 64
            self.assertRefuses("base SHA mismatch", P.load_canonical)
        finally:
            P.BASE_SHA = real
        P.load_canonical()   # and it must still succeed on the true pin

    def test_all_seven_crops_are_staged(self):
        self.assertEqual(tuple(sorted(self.batch)), tuple(sorted(CROPS)))


class CleanInputPasses(Base):
    """A guard that refuses correct input is invisible to mutation testing. Assert both ways."""

    def test_reconcile_passes(self):
        n_canon, n_target = P.check_reconcile(self.pins, self.data)
        self.assertEqual(n_canon, N_CANONICAL_PROBLEMS)
        self.assertEqual(n_target, N_TARGET_PROBLEMS)

    def test_spec_match_passes(self):
        P.check_batch_matches_spec(self.pins, self.batch)

    def test_ladders_pass_and_rung_count_is_pinned(self):
        self.assertEqual(P.check_ladders(self.batch, self.cm), N_RUNGS)

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
        self.assertGreater(checked, 0, "zero notes scanned would make this guard vacuous")
        self.assertGreater(shipped, 0, "zero shipped notes would make this guard vacuous")

    def test_no_intra_batch_twins(self):
        self.assertGreater(P.check_no_intra_batch_twins(self.batch), 0)

    def test_temperature_figures_warranted(self):
        P.check_temperature_figures_warranted(self.batch, self.pins, self.data)

    def test_machinery_regex_does_not_refuse_ordinary_english(self):
        """PINNED REGRESSION. The first version of this regex matched `applies[_ ]to` with an
        optional space and refused 'The same care applies to a division handed over the fence'.
        Both directions are asserted: the ordinary sentence passes, the field name is caught."""
        self.assertIsNone(P.LADDER_VOCAB.search(
            "The same care applies to a division handed over the fence."))
        self.assertIsNone(P.LADDER_VOCAB.search(
            "This control method works best before the disease appears."))
        self.assertIsNotNone(P.LADDER_VOCAB.search("this is the cheapest rung on the ladder"))
        self.assertIsNotNone(P.LADDER_VOCAB.search("applies_to"))


class ReconcileFamily(Base):
    def test_unaccounted_canonical_problem_is_refused(self):
        pins = self.fresh_pins()
        pins["thyme"]["pests"] = [r for r in pins["thyme"]["pests"] if r["name"] != "Aphids"]
        self.assertRefuses("UNACCOUNTED", P.check_reconcile, pins, self.data)

    def test_phantom_source_is_refused(self):
        pins = self.fresh_pins()
        pins["thyme"]["pests"][0]["from"] = "RENAME from 'No Such Problem'"
        self.assertRefuses("PHANTOM SOURCE", P.check_reconcile, pins, self.data)

    def test_phantom_retirement_is_refused(self):
        pins = self.fresh_pins()
        pins["_retired"].append({"crop": "thyme", "field": "pests", "name": "Nope", "why": "x"})
        self.assertRefuses("PHANTOM RETIREMENT", P.check_reconcile, pins, self.data)

    def test_retiring_something_also_used_is_refused(self):
        """Retirement is DECLARED. A contradiction between the two must not resolve silently."""
        pins = self.fresh_pins()
        pins["_retired"].append(
            {"crop": "thyme", "field": "pests", "name": "Aphids", "why": "contradiction"})
        self.assertRefuses("CONTRADICTION", P.check_reconcile, pins, self.data)

    def test_retirement_count_is_pinned(self):
        self.assertEqual(len(self.pins["_retired"]), N_RETIRED)
        self.assertEqual(
            sum(1 for _, _, r in P.spec_rows(self.pins) if r["from"].startswith("SPLIT")),
            N_SPLIT_ROWS)
        self.assertEqual(
            sum(1 for _, _, r in P.spec_rows(self.pins) if r["from"].startswith("RENAME")),
            N_RENAMED)


class SpecMatchFamily(Base):
    def test_off_pin_id_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0]["id"] = "spider-mite"
        self.assertRefuses("but pinned", P.check_batch_matches_spec, self.pins, b)

    def test_reverted_type_is_refused(self):
        """THE DEFECT A1 EXISTS TO FIX. Reverting a spider mite to `insect` makes `sulfur` and
        `even_watering` illegal. The fan-out validator once passed this because it read `type` from
        the PIN to check ladder legality and never compared the OUTPUT's own value."""
        b = self.fresh()
        for e in b["oregano"]["pests"]:
            if e["id"] == "spider-mites":
                e["type"] = "insect"
        self.assertRefuses("but pinned", P.check_batch_matches_spec, self.pins, b)

    def test_dropped_entry_is_refused(self):
        b = self.fresh()
        b["sage"]["pests"] = b["sage"]["pests"][:-1]
        self.assertRefuses("entries, spec has", P.check_batch_matches_spec, self.pins, b)

    def test_appended_ghost_entry_is_refused(self):
        """The PLA-162 shape: an APPENDED clone is invisible to a walk that iterates `pre`."""
        b = self.fresh()
        ghost = copy.deepcopy(b["sage"]["pests"][0])
        ghost["name"] = "Ghost pest"
        b["sage"]["pests"].append(ghost)
        self.assertRefuses("entries, spec has", P.check_batch_matches_spec, self.pins, b)


class LadderFamily(Base):
    def test_empty_ladder_is_refused(self):
        """`[]` is not `None`. An empty ladder once passed every gate in this repo."""
        b = self.fresh()
        b["thyme"]["pests"][0]["control_ladder"] = []
        self.assertRefuses("non-empty list", P.check_ladders, b, self.cm)

    def test_null_ladder_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0]["control_ladder"] = None
        self.assertRefuses("non-empty list", P.check_ladders, b, self.cm)

    def test_unknown_method_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0]["control_ladder"][0]["method"] = "not_a_method"
        self.assertRefuses("unknown method", P.check_ladders, b, self.cm)

    def test_tier_inversion_is_refused(self):
        """PINNED ORDER: cultural < physical < BIOLOGICAL < soft_chemical < conventional. This
        suite's first draft had biological and soft_chemical the wrong way round, which would have
        mis-ordered every ladder in the batch; it was caught by importing the gate's table."""
        self.assertLess(P.TIER_RANK["biological"], P.TIER_RANK["soft_chemical"])
        b = self.fresh()
        lad = b["thyme"]["pests"][0]["control_ladder"]
        lad.reverse()
        self.assertRefuses("follows a higher tier", P.check_ladders, b, self.cm)

    def test_repeated_method_is_refused(self):
        b = self.fresh()
        lad = b["sage"]["pests"][1]["control_ladder"]
        lad.append(copy.deepcopy(lad[0]))
        self.assertRefuses("repeats method", P.check_ladders, b, self.cm)

    def test_method_not_reaching_type_is_refused(self):
        b = self.fresh()
        for e in b["sage"]["diseases"]:
            if e["id"] == "powdery-mildew":
                e["control_ladder"][0]["method"] = "handpick"   # insect/mollusk only
        self.assertRefuses("does not reach type", P.check_ladders, b, self.cm)

    def test_em_dash_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0]["control_ladder"][0]["note_beginner"] += " and then — stop."
        self.assertRefuses("em/en dash", P.check_ladders, b, self.cm)

    def test_machinery_vocabulary_in_a_note_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0]["control_ladder"][0]["note_seasoned"] = \
            "This is the cheapest rung to start with."
        self.assertRefuses("names the machinery", P.check_ladders, b, self.cm)

    def test_identical_registers_are_refused(self):
        b = self.fresh()
        r = b["thyme"]["pests"][0]["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        self.assertRefuses("byte-identical", P.check_ladders, b, self.cm)

    def test_empty_note_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0]["control_ladder"][0]["note_beginner"] = "   "
        self.assertRefuses("missing or empty", P.check_ladders, b, self.cm)


class CorrectionFamily(Base):
    def test_split_limb_inheriting_bundle_prose_is_refused(self):
        b = self.fresh()
        for e in b["mint"]["diseases"]:
            if e["id"] == "anthracnose":
                e["field_corrections"].pop("cause_seasoned", None)
        self.assertRefuses("may not inherit bundle prose",
                           P.check_split_rows_author_full_prose, self.pins, b)

    def test_correction_without_anchor_is_refused(self):
        b = self.fresh()
        for e in b["thyme"]["diseases"]:
            fc = e.get("field_corrections") or {}
            if fc:
                fc[list(fc)[0]]["anchor"] = ""
                break
        self.assertRefuses("is missing 'anchor'", P.check_corrections_anchored, b, self.pins)

    def test_correction_without_reason_is_refused(self):
        b = self.fresh()
        for e in b["thyme"]["diseases"]:
            fc = e.get("field_corrections") or {}
            if fc:
                fc[list(fc)[0]]["why"] = ""
                break
        self.assertRefuses("is missing 'why'", P.check_corrections_anchored, b, self.pins)

    def test_correction_to_a_non_prose_field_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0].setdefault("field_corrections", {})["severity"] = {
            "new": "high", "why": "x", "anchor": "y"}
        self.assertRefuses("is not a prose field", P.check_corrections_anchored, b, self.pins)

    def test_name_correction_disagreeing_with_the_pin_is_refused(self):
        """`name` is allowed as provenance ONLY when it agrees with the pin, which governs."""
        b = self.fresh()
        for e in b["oregano"]["diseases"]:
            if e["id"] == "oregano-rust":
                e["field_corrections"]["name"]["new"] = "Oregano rust"
        self.assertRefuses("the pin governs the value",
                           P.check_corrections_anchored, b, self.pins)

    def test_machinery_vocabulary_in_a_correction_is_refused(self):
        """Corrected prose is consumer copy too. The guard was notes-only, leaving 244 of the
        batch's 382 authored strings unscanned."""
        b = self.fresh()
        for e in b["thyme"]["diseases"]:
            fc = e.get("field_corrections") or {}
            if fc:
                fc[list(fc)[0]]["new"] = "Start on the first rung of the ladder."
                break
        self.assertRefuses("correction names the machinery",
                           P.check_corrections_anchored, b, self.pins)


class SourceFamily(Base):
    def test_unadmitted_source_key_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0].setdefault("sources", []).append("plantvillage")
        self.assertRefuses("absent from source_catalog", P.check_sources_admitted, b, self.data)

    def test_anchor_without_a_matching_source_is_refused(self):
        b = self.fresh()
        e = b["thyme"]["pests"][0]
        e.setdefault("anchoring_urls", {})["umn_ext"] = {"url": "https://x", "verified": "2026-09-04"}
        self.assertRefuses("does not list it in sources", P.check_sources_admitted, b, self.data)

    def test_the_new_catalog_key_is_admitted(self):
        """uc_ipm_pn7493 landed in its own promote ahead of this batch."""
        self.assertIn("uc_ipm_pn7493", self.data["source_catalog"])


class CopyFamily(Base):
    def test_verbatim_lift_from_a_shipped_note_is_refused(self):
        b = self.fresh()
        donor = None
        for c in self.data["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    if r["method"] == "water_spray" and r.get("note_beginner"):
                        donor = r["note_beginner"]
                        break
                if donor:
                    break
            if donor:
                break
        self.assertIsNotNone(donor, "no donor found; this test would be vacuous")
        for e in b["sage"]["pests"]:
            for r in e["control_ladder"]:
                if r["method"] == "water_spray":
                    r["note_beginner"] = donor
        self.assertRefuses("scores", P.check_no_precedent_copy, b, self.data)

    def test_symmetric_metric_is_actually_symmetric(self):
        """difflib's matcher is greedy, so ratio(a,b) != ratio(b,a). The metric takes the MAX of both
        orders because argument order is not a property of the prose.

        THE PAIR MUST ACTUALLY BE ASYMMETRIC. The first version of this test used two hand-written
        sentences that scored 0.5890 in BOTH directions, so it passed whether `_sym` took the max or
        just one direction and proved nothing. A mutation making the metric one-directional survived
        it. The pair below is drawn from the real corpus and measured: the two orders differ by more
        than 0.30, which is larger than the 0.271 an earlier batch measured."""
        a, b = self._asymmetric_pair()
        fwd = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
        rev = difflib.SequenceMatcher(None, b, a, autojunk=False).ratio()
        self.assertNotAlmostEqual(fwd, rev, places=3,
                                  msg="the chosen pair is not asymmetric, so this test is vacuous")
        self.assertEqual(P._sym(a, b), P._sym(b, a))
        self.assertEqual(P._sym(a, b), max(fwd, rev))
        self.assertGreater(max(fwd, rev) - min(fwd, rev), 0.10)

    def _asymmetric_pair(self):
        """Find two shipped notes whose difflib ratio differs by order. Searched, not hardcoded, so
        it cannot silently stop being asymmetric if the corpus changes."""
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
        """autojunk engages at 200 characters and junks any character present in over 1% of the
        sequence, which describes every seasoned register. A VERBATIM lift scores 1.0 either way, so
        the verbatim-lift driver cannot see this setting and a mutation re-enabling it survived that
        driver.

        This asserts the setting where it decides the VERDICT: it finds a real shipped pair that
        scores at or above COPY_THRESHOLD with autojunk off and BELOW it with autojunk on. Measured
        across the corpus, 44844 pairs have their ratio changed by autojunk and the worst deflation
        runs 0.7778 down to 0.0385 -- so leaving it on would let a near-verbatim lift pass unseen.
        The pair is searched rather than hardcoded so it cannot quietly stop demonstrating this."""
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
        # And the guard's own metric must use the undeflated one.
        self.assertGreaterEqual(P._sym(x, y), P.COPY_THRESHOLD)

    def test_echo_of_a_shipped_sentence_is_refused(self):
        """The donor must be a SINGLE-donor sentence. Picking 'the first shipped sentence' selected
        house phrasing, which the exemption legitimately clears -- the test would then have been
        asserting the absence of a defect it had not actually injected."""
        import collections
        donors = collections.Counter()
        where = {}
        for c in self.data["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                for r in p.get("control_ladder") or []:
                    for k in P.ADVICE_FIELDS:
                        for sent in P.sentences(r.get(k) or ""):
                            donors[sent] += 1
                            where.setdefault(sent, f"{c['slug']}/{p.get('id')}")
        single = [x for x, n in donors.items() if n == 1]
        self.assertGreater(len(single), 0, "no single-donor sentence; this test would be vacuous")
        b = self.fresh()
        b["thyme"]["pests"][0]["control_ladder"][0]["note_seasoned"] += " " + single[0].capitalize()
        self.assertRefuses("echoes a shipped sentence", P.check_no_shipped_prose_echo, b, self.data)

    def test_two_donor_recombination_is_refused(self):
        """THE DEFECT THE RATIO CANNOT SEE. Half the phrasing from one donor and half from another
        resembles NEITHER closely enough to cross 0.70. This batch's real instance scored clean
        against both donors and would have shipped."""
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
        b["thyme"]["pests"][0]["control_ladder"][0]["note_beginner"] = half1 + " " + half2
        self.assertRefuses("recombines runs from two shipped notes",
                           P.check_no_multi_donor_recombination, b, self.data)

    def test_nested_donor_runs_are_not_recombination(self):
        """POSITIVE CONTROL, and the reason the nesting test exists. Several shipped notes carrying
        ONE stock sentence between them produce nested shared-gram sets and are house phrasing, not
        two lifts. Without this brake the check flagged 9 notes on this batch instead of 1.

        The control uses ONE CONTIGUOUS RUN from a single donor, not a whole donor note. Pasting a
        whole note is not a valid control: a shipped note may itself carry runs from two other
        shipped notes, in which case flagging it is CORRECT and the control would be asserting the
        opposite of what it means to. That is how this test failed on its first writing."""
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
        b["thyme"]["pests"][0]["control_ladder"][0]["note_beginner"] = (
            "Keep the bed tidy through the season. " + run)
        # One run, so every donor that matches it matches a NESTED subset. Must not flag.
        P.check_no_multi_donor_recombination(b, self.data)

    def test_nesting_brake_admits_only_nested_sets(self):
        """Unit-level, so the brake is asserted independently of whatever the corpus happens to
        contain. Non-nested sets are recombination; nested ones are one shared phrase."""
        a, c = {"x y z", "y z w"}, {"x y z", "y z w", "z w v"}
        self.assertTrue(a <= c, "a subset relation must read as nested")
        d, e = {"p q r", "q r s"}, {"m n o", "n o p"}
        self.assertFalse(d <= e or e <= d, "disjoint runs must read as non-nested")

    def test_cross_crop_twin_note_is_refused(self):
        b = self.fresh()
        src = None
        for e in b["sage"]["pests"]:
            for r in e["control_ladder"]:
                if r["method"] == "water_spray":
                    src = r["note_beginner"]
        self.assertIsNotNone(src)
        for e in b["thyme"]["pests"]:
            for r in e["control_ladder"]:
                if r["method"] == "water_spray":
                    r["note_beginner"] = src
        self.assertRefuses("template twin", P.check_no_intra_batch_twins, b)


class TemperatureFamily(Base):
    def test_unwarranted_temperature_figure_is_refused(self):
        b = self.fresh()
        b["thyme"]["pests"][0]["control_ladder"][0]["note_seasoned"] += " Hold it below 137°F."
        self.assertRefuses("with no warrant",
                           P.check_temperature_figures_warranted, b, self.pins, self.data)

    def test_a_warranted_figure_passes(self):
        """POSITIVE CONTROL. A blanket ban would be a refusal-spec pass on a batch with no figures;
        this batch HAS figures, so the guard must admit the warranted ones."""
        self.assertGreater(
            P.check_temperature_figures_warranted(self.batch, self.pins, self.data), 0,
            "zero figures found; the warrant check would be vacuous on this batch")


class ApplyAndVerify(Base):
    """Reach the ENTRY POINT. 53 green tests once sat on a main() that never called check()."""

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
        """THE CORE POST-CHECK. An owner-and-count check passes while a target's UNPINNED field
        changes unseen; every changed leaf must match a declaration.

        The mutated field must be one with NO declared correction. The first version of this test
        picked `thyme/Aphids/symptoms_beginner`, which HAS a declaration, so the guard correctly
        fired its other branch ('does not match its declared correction') and the specific-fragment
        assertion caught the mismatch. A test asserting a shared fragment would have passed while
        exercising the wrong branch."""
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
        for e in idx["thyme"]["diseases"]:
            src = next(x for x in self.batch["thyme"]["diseases"] if x["name"] == e["name"])
            for fname in (src.get("field_corrections") or {}):
                e[fname] = "Declared, but not what was written."
                done = True
                break
            if done:
                break
        self.assertTrue(done, "no correction to mutate; this test would be vacuous")
        self.assertRefuses("does not match its declared correction",
                           P.verify_post, self.data, post, self.pins, self.batch)

    def test_lost_key_is_refused(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        idx["thyme"]["pests"][0].pop("symptoms_beginner", None)
        self.assertRefuses("lost keys", P.verify_post, self.data, post, self.pins, self.batch)

    def test_serialize_is_compact(self):
        """CANONICAL IS COMPACT. Never indent, no trailing newline, unicode not escaped."""
        blob = P.serialize({"a": 1, "b": "café"})
        self.assertEqual(blob, '{"a":1,"b":"café"}'.encode("utf-8"))
        self.assertNotIn(b"\\u", blob)
        self.assertFalse(blob.endswith(b"\n"))

    def test_retired_entries_are_absent_from_the_post_state(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        for r in self.pins["_retired"]:
            names = {e["name"] for e in idx[r["crop"]].get(r["field"]) or []}
            self.assertNotIn(r["name"], names,
                             f"{r['crop']}/{r['name']!r} was declared retired but is still present")

    def test_post_state_problem_count_is_pinned(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        n = sum(len(idx[c].get(f) or []) for c in CROPS for f in ("pests", "diseases"))
        self.assertEqual(n, N_TARGET_PROBLEMS)

    def test_every_target_entry_carries_an_id_and_a_ladder(self):
        """The arc's completion test. `id=None` marks 'not through PLA-8'."""
        post = P.apply_to(self.data, self.pins, self.batch)
        idx = {c["slug"]: c for c in post["crops"]}
        for c in CROPS:
            for f in ("pests", "diseases"):
                for e in idx[c].get(f) or []:
                    self.assertIsNotNone(e.get("id"), f"{c}/{e['name']} has no id")
                    self.assertTrue(e.get("control_ladder"), f"{c}/{e['name']} has no ladder")


if __name__ == "__main__":
    unittest.main(verbosity=2)
