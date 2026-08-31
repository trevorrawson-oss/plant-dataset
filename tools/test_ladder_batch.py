#!/usr/bin/env python3
"""Guards on the batch runner's FAMILY CUT.

WHY THIS EXISTS. `cmd_families` prints "TWIN GROUPS ... one read covers the group" and closes with
"identical prose means the read is one problem set plus a mechanical equality check on its
siblings". That instruction sends a session into a mechanical propagation: author ONE crop, copy the
ladders onto its siblings, and have the promote assert the copies are byte-identical (see
`tools/promote_pla8_batch2.py`).

The signature it grouped on was `tuple(sorted(problem_name(p)))` -- NAMES ONLY. It never compared a
single character of prose. Two crops naming the same nine problems grouped as "twins" no matter how
far apart their sourced prose had drifted.

Measured against canonical `c13ddea5`, NOT ONE of the ten reported twin groups was a true twin:
collards/kale shared 28.7% of their problem fields, beefsteak/cherry-tomato 55.4%, the three
cucumbers 72.7%. The corns (batch 2, already shipped) measured 96.2% with all twelve differences on
one problem, so that propagation was in fact sound -- which is exactly the danger. The tool selected
that group for the wrong reason and the result happened to be right, so the method looked proven.

On the cucumbers the same propagation would have been a content defect in both directions:
pickling-cucumber's prose names wilt-tolerant County Fair and CMV-resistant varieties, where
cucumber's and slicing-cucumber's name non-bitter varieties and claim no resistance at all. Copying
either way erases a sourced claim or invents one.

A percentage is not the bar. The bar is that a group ADVERTISED as safe to propagate mechanically
must actually be byte-identical in the prose a rung is built from.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ladder_batch as lb

# the fields a rung is RESTATED FROM. anchoring_urls/sources are provenance, not rung content;
# they are checked separately because a divergence there is a sourcing defect, not a ladder one.
PROSE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "prevention_beginner", "prevention_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned",
                "management_beginner", "management_seasoned",
                "description_beginner", "description_seasoned",
                "note_beginner", "note_seasoned")


def crop(slug, problems):
    return {"slug": slug, "name": slug, "category": "Test",
            "verification_status": {"status": "verified_gs_arc"},
            "pests": problems, "diseases": []}


class TwinGroupsShareProse(unittest.TestCase):
    """A reported twin group must share PROSE, not merely problem names."""

    def test_same_names_different_prose_is_not_a_twin_group(self):
        """THE DEFECT. Two crops naming the same problem with different advice are NOT twins.

        This is the cucumber case reduced to its bones: same problem name, and a `prevention_*`
        that names a DIFFERENT control. Propagating a ladder across this pair swaps one sourced
        control for another.
        """
        a = crop("crop-a", [{"name": "Cucumber beetles",
                             "prevention_seasoned": "choose non-bitter varieties that attract fewer beetles",
                             "organic_treatment_beginner": "cover young plants with row cover"}])
        b = crop("crop-b", [{"name": "Cucumber beetles",
                             "prevention_seasoned": "choose wilt-tolerant varieties such as County Fair",
                             "organic_treatment_beginner": "cover young plants with row cover"}])
        twins, _singles = lb.family_cut([a, b])
        self.assertEqual(twins, [],
                         "crops whose prose names DIFFERENT controls were reported as a twin group; "
                         "a mechanical propagation across them swaps a sourced control")

    def test_identical_prose_is_a_twin_group(self):
        """POSITIVE CONTROL. Without this the fix could be 'return [] always' and still pass."""
        p = {"name": "Aphids", "prevention_seasoned": "avoid excess nitrogen",
             "organic_treatment_beginner": "knock them off with water"}
        twins, _singles = lb.family_cut([crop("crop-a", [dict(p)]), crop("crop-b", [dict(p)])])
        self.assertEqual([sorted(g) for g in twins], [["crop-a", "crop-b"]],
                         "crops with byte-identical prose must still group as twins")

    def test_differing_field_absence_is_not_identical(self):
        """A field present on one crop and absent on the other is a difference, not a match.

        Guards the `.get(k)` -> None -> None collision that made all eight microgreens crops
        collide on a signature of empties (see problem_name's docstring for the same class of bug).
        """
        a = crop("crop-a", [{"name": "Aphids", "prevention_seasoned": "avoid excess nitrogen"}])
        b = crop("crop-b", [{"name": "Aphids"}])
        twins, _singles = lb.family_cut([a, b])
        self.assertEqual(twins, [], "absent prose must not collide with present prose")

    def test_every_prose_field_is_load_bearing(self):
        """EACH field must break the tie, not just whichever one the implementation happens to read.

        BOTH SCHEMAS. The first version of this test built its fixture from the classic
        `organic_treatment_*`/`prevention_*` shape only, so dropping the microgreens half of
        PROSE_FIELDS survived the mutation harness -- the identical blind spot `prose_key`'s
        docstring already records ("Reading only the classic pair silently EXCLUDED the
        microgreens"). A test that reproduces the bug it is guarding against is not coverage.
        """
        classic = {"name": "Aphids", "symptoms_beginner": "s1", "symptoms_seasoned": "s2",
                   "cause_beginner": "c1", "cause_seasoned": "c2",
                   "prevention_beginner": "p1", "prevention_seasoned": "p2",
                   "organic_treatment_beginner": "o1", "organic_treatment_seasoned": "o2"}
        microgreen = {"name_beginner": "Damping-off and mold",
                      "name_seasoned": "Damping-off (and surface mold)",
                      "description_beginner": "d1", "description_seasoned": "d2",
                      "management_beginner": "m1", "management_seasoned": "m2"}
        # THIRD SCHEMA (2026-08-30): the Companion & Pollinator crops carry note_* only.
        companion = {"name": "Aphids", "note_beginner": "n1", "note_seasoned": "n2"}
        covered = set()
        for base in (classic, microgreen, companion):
            for field in [f for f in PROSE_FIELDS if f in base]:
                covered.add(field)
                with self.subTest(field=field):
                    b = dict(base)
                    b[field] = "CHANGED"
                    twins, _s = lb.family_cut([crop("crop-a", [dict(base)]), crop("crop-b", [b])])
                    self.assertEqual(twins, [],
                                     f"a difference in {field} did not break the twin group")
        # COVERAGE, not overlap: every field the module declares must have been exercised above,
        # so adding a field to PROSE_FIELDS without a fixture for it fails here rather than
        # silently going untested.
        self.assertEqual(sorted(covered), sorted(lb.PROSE_FIELDS),
                         "PROSE_FIELDS contains fields no fixture exercises: "
                         f"{sorted(set(lb.PROSE_FIELDS) - covered)}")

    def test_note_shaped_crops_with_different_notes_are_not_twins(self):
        """THE COMPANION SCHEMA. The 10 Companion & Pollinator crops carry their prose in
        note_beginner/note_seasoned ONLY (no prevention_*, no management_*). Before the note
        fallback, prose_key reduced every such problem to (name, None, None), so two companion
        crops naming the same problem with DIFFERENT advice collided as a false twin, the exact
        shape that excluded the microgreens once and the nasturtium/zinnia records from the
        trap-cropping scan."""
        a = crop("crop-a", [{"name": "Aphids",
                             "note_beginner": "hose them off and let the ladybugs work",
                             "note_seasoned": "conserve natural enemies; a water jet clears colonies"}])
        b = crop("crop-b", [{"name": "Aphids",
                             "note_beginner": "pinch out the worst shoot tips and discard them",
                             "note_seasoned": "tip removal takes the colony with it on this crop"}])
        twins, _singles = lb.family_cut([a, b])
        self.assertEqual(twins, [],
                         "note-shaped problems with different advice collided as a twin group; "
                         "the note schema is invisible to prose_key")

    def test_note_shaped_identical_prose_is_a_twin_group(self):
        """POSITIVE CONTROL for the note schema, so the fix cannot be 'never group note crops'."""
        p = {"name": "Aphids",
             "note_beginner": "hose them off and let the ladybugs work",
             "note_seasoned": "conserve natural enemies; a water jet clears colonies"}
        twins, _singles = lb.family_cut([crop("crop-a", [dict(p)]), crop("crop-b", [dict(p)])])
        self.assertEqual([sorted(g) for g in twins], [["crop-a", "crop-b"]],
                         "byte-identical note-shaped prose must group as twins")

    def test_problem_ORDER_is_part_of_the_identity(self):
        """Propagation is INDEX-WISE (`promote_pla8_batch2.py` copies ladders by position), so two
        crops carrying the same problems in a different order are not propagate-safe even though
        their prose SETS match. Sorting the signature would report them as twins and hand the next
        session an index-shifted copy: every ladder attached to the wrong problem."""
        a = {"name": "Aphids", "prevention_seasoned": "avoid excess nitrogen"}
        b = {"name": "Spider mites", "prevention_seasoned": "keep plants well watered"}
        twins, _singles = lb.family_cut([crop("crop-a", [dict(a), dict(b)]),
                                         crop("crop-b", [dict(b), dict(a)])])
        self.assertEqual(twins, [],
                         "same problems in a DIFFERENT ORDER were reported as propagate-safe twins")

    def test_explicit_null_is_not_the_same_as_an_absent_field(self):
        """A key present with a null value is a DIFFERENT record shape from a missing key.

        Both mean "no prose", so this looks like a distinction without a difference. It is not:
        the batch promote asserts the STAGED FILES are byte-identical
        (`promote_pla8_batch2.py:check()`), and a null-vs-absent divergence breaks that assertion
        late and confusingly, after the authoring is done. Refuse it here instead.
        """
        a = crop("crop-a", [{"name": "Aphids", "prevention_seasoned": None}])
        b = crop("crop-b", [{"name": "Aphids"}])
        twins, _singles = lb.family_cut([a, b])
        self.assertEqual(twins, [], "an explicit null collided with an absent field")

    def test_name_beginner_divergence_breaks_a_twin(self):
        """problem_name() falls back name -> name_seasoned -> name_beginner and returns the FIRST
        one set. Two crops agreeing on name_seasoned while differing on name_beginner must not be
        declared propagate-safe."""
        base = {"name_seasoned": "Damping-off (and surface mold)",
                "name_beginner": "Damping-off and mold",
                "management_beginner": "keep the mix just damp"}
        b = dict(base, name_beginner="Seedling rot")
        twins, _singles = lb.family_cut([crop("crop-a", [dict(base)]), crop("crop-b", [b])])
        self.assertEqual(twins, [], "a name_beginner divergence did not break the twin group")


class CrossSiblingLadderConflicts(unittest.TestCase):
    """Siblings that share source prose but got DIFFERENT ladders.

    WHY THIS EXISTS. Batch 3's one real defect was found by hand. cucumber and slicing-cucumber
    carry BYTE-IDENTICAL `prevention_seasoned` on Cucumber beetles ("choose non-bitter varieties
    that attract fewer beetles"), and slicing's authoring agent keyed it to `resistant_varieties`
    while cucumber's refused. Same input, different output; one of them had to be wrong.

    No gate can see that, because each ladder is independently valid. It is a CROSS-CROP question
    that exists only because a family batch authors siblings separately. Finding it took a manual
    side-by-side, and with ~34 batches left that read is the bottleneck. This makes the mechanical
    half mechanical, so the human read spends itself on what actually needs judgment.

    IT REPORTS, IT DOES NOT REFUSE. A divergence can be correct: pickling-cucumber legitimately
    carries `resistant_varieties` on bacterial-wilt where its siblings do not, because its prose
    claims wilt tolerance and theirs claim only reduced beetle attraction. The output is a read
    list with the evidence attached, not a verdict.
    """

    def test_identical_prose_with_differing_ladders_is_reported(self):
        src = {"a": [{"name": "Cucumber beetles", "prevention_seasoned": "choose non-bitter varieties"}],
               "b": [{"name": "Cucumber beetles", "prevention_seasoned": "choose non-bitter varieties"}]}
        out = {"a": [["crop_rotation"]], "b": [["resistant_varieties", "crop_rotation"]]}
        rows = lb.cross_sibling_conflicts(src, out)
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["problem"], "Cucumber beetles")
        self.assertEqual(rows[0]["only_in_b"], ["resistant_varieties"])
        self.assertEqual(rows[0]["only_in_a"], [])
        self.assertIn("prevention_seasoned", rows[0]["identical_fields"])

    def test_identical_prose_and_identical_ladders_is_silent(self):
        """POSITIVE CONTROL: without it, `return []` passes every other test in this class."""
        src = {"a": [{"name": "Aphids", "prevention_seasoned": "avoid excess nitrogen"}],
               "b": [{"name": "Aphids", "prevention_seasoned": "avoid excess nitrogen"}]}
        out = {"a": [["balance_nitrogen"]], "b": [["balance_nitrogen"]]}
        self.assertEqual(lb.cross_sibling_conflicts(src, out), [])

    def test_reported_even_when_only_SOME_fields_match(self):
        """The real cucumber case: prevention_seasoned matched while organic_treatment_* differed.
        Requiring EVERY field to match would have missed the actual defect."""
        src = {"a": [{"name": "Cucumber beetles", "prevention_seasoned": "same",
                      "organic_treatment_beginner": "cover them"}],
               "b": [{"name": "Cucumber beetles", "prevention_seasoned": "same",
                      "organic_treatment_beginner": "cover the plants"}]}
        out = {"a": [["crop_rotation"]], "b": [["resistant_varieties"]]}
        rows = lb.cross_sibling_conflicts(src, out)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["identical_fields"], ["prevention_seasoned"])
        self.assertIn("organic_treatment_beginner", rows[0]["differing_fields"])

    def test_no_shared_prose_at_all_is_NOT_reported(self):
        """If siblings share nothing on this problem, differing ladders are expected and the row
        would be noise. The signal is identical INPUT with different OUTPUT."""
        src = {"a": [{"name": "Aphids", "prevention_seasoned": "one thing"}],
               "b": [{"name": "Aphids", "prevention_seasoned": "a completely different thing"}]}
        out = {"a": [["balance_nitrogen"]], "b": [["water_spray"]]}
        self.assertEqual(lb.cross_sibling_conflicts(src, out), [])

    def test_three_crops_report_each_conflicting_PAIR(self):
        src = {c: [{"name": "Aphids", "prevention_seasoned": "same"}] for c in ("a", "b", "c")}
        out = {"a": [["x"]], "b": [["x"]], "c": [["y"]]}
        rows = lb.cross_sibling_conflicts(src, out)
        self.assertEqual(sorted((r["a"], r["b"]) for r in rows), [("a", "c"), ("b", "c")])

    def test_it_would_have_caught_the_batch_3_defect(self):
        """The regression case, in the shape it actually occurred."""
        shared = ("Exclude beetles from seedlings with row cover, keep young plants vigorous so "
                  "they grow past the vulnerable stage, choose non-bitter varieties that attract "
                  "fewer beetles, clear weeds and debris, and rotate away from where cucurbits grew.")
        src = {"cucumber": [{"name": "Cucumber beetles", "prevention_seasoned": shared}],
               "slicing-cucumber": [{"name": "Cucumber beetles", "prevention_seasoned": shared}]}
        out = {"cucumber": [["crop_rotation", "garden_sanitation", "floating_row_cover",
                             "handpick", "yellow_sticky_traps"]],
               "slicing-cucumber": [["resistant_varieties", "crop_rotation", "garden_sanitation",
                                     "floating_row_cover", "handpick", "yellow_sticky_traps"]]}
        rows = lb.cross_sibling_conflicts(src, out)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["only_in_b"], ["resistant_varieties"])


class TheRosterHasRunOutOfTrueTwins(unittest.TestCase):
    """RETIRED AND REPLACED, on the instruction the retired test left behind.

    This class used to be `ReportedTwinsAreRealOnCanonical`: it walked every twin group
    `family_cut` reported on the live roster and asserted the members were byte-identical in prose.
    Its own reachability guard said, in as many words, "If this ever fails because the roster
    genuinely ran out of true twins, DELETE the canonical assertion rather than leaving it green
    and empty."

    That is what happened. Batch 5 laddered `dry-bean` + `green-beans-bush`, the last true twin on
    the roster, and the reachability guard went red the moment the denominator emptied -- which is
    the guard doing its job rather than the suite breaking. The byte-identity PROPERTY is still
    fully covered, synthetically and with a real denominator, by `TwinGroupsShareProse` above.

    What replaces it is the fact that emptying created, which is worth asserting because the whole
    rollout plan depends on it: **there is no propagation available any more.** Every remaining
    batch costs one authoring pass per crop, so any estimate built on the old twin-group numbers is
    wrong by roughly 3x. If a twin ever reappears -- a new crop, or an edit that makes two records
    identical -- this test fails and the propagation path becomes available again, which is
    information the next session wants either way.
    """

    @classmethod
    def setUpClass(cls):
        d = lb.load()
        cert = [c for c in d["crops"]
                if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
        cls.todo = [c for c in cert if not lb.laddered(c)]

    def test_there_are_unladdered_crops_left_to_measure(self):
        self.assertGreater(len(self.todo), 0)

    def test_no_true_twin_group_remains_on_the_roster(self):
        twins, _singles = lb.family_cut(self.todo)
        self.assertEqual(
            [sorted(g) for g in twins], [],
            "a true twin group has REAPPEARED on the roster. That is not a failure -- it means a "
            "propagate-safe pair exists again and the next batch can author one crop instead of "
            "two. Verify the pair really is byte-identical in prose, then take it as the next "
            "batch and update this test.")


class ReadBriefCarriesTheWholeMeaning(unittest.TestCase):
    """THE SECOND INSTANCE OF THE SAME DEFECT, in the CHECKING tool rather than the authoring one.

    `603f4f8` fixed `cmd_prepare`, which builds the authoring brief. `cmd_verify` builds the READ
    brief -- the pass that holds each shipped rung against what its method actually means -- and it
    was still cutting `best_use` at 104 characters. Measured against canonical 04b5aa69: 53 of 56
    methods run past that cut and 13 lose their trailing "Distinct from <neighbour>" clause
    outright, including `off_season_tillage` and `planting_time_avoidance`, two of the methods this
    arc has actually confused. **The tool that checks for method-meaning mismatches was comparing
    rungs against truncated meanings**, which is the failure it exists to catch.

    The gates are stubbed here because they are slow subprocesses and are not what is under test;
    the real `cmd_verify` print path is exercised."""

    @classmethod
    def setUpClass(cls):
        import tempfile, argparse, io, contextlib, copy, subprocess as sp
        cls.tmp = tempfile.mkdtemp(prefix="readbrieftest_")
        d = lb.load()
        cls.cm = d["control_methods"]
        # one laddered crop, minimally altered so `changed` is non-empty and the pairs print
        scratch = copy.deepcopy(d)
        target = next(c for c in scratch["crops"] if lb.laddered(c))
        cls.target = target["slug"]
        for _f, prob in lb.problems(target):
            if prob.get("control_ladder"):
                prob["control_ladder"][0]["note_beginner"] += " (test edit)"
                break
        path = os.path.join(cls.tmp, "scratch_canonical.json")
        json.dump(scratch, open(path, "w"))

        class _Stub:
            returncode = 0
            stdout = "STUBBED: 0 violation(s)"
            stderr = ""

        real = lb.subprocess.run
        lb.subprocess.run = lambda *a, **k: _Stub()
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                lb.cmd_verify(argparse.Namespace(out=cls.tmp))
        finally:
            lb.subprocess.run = real
        cls.out = buf.getvalue()

    @classmethod
    def tearDownClass(cls):
        import shutil
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_read_brief_actually_ran(self):
        """Liveness: if cmd_verify printed no method/rung pairs, every assertion below is vacuous."""
        self.assertIn("METHOD MEANS:", self.out)
        self.assertIn(self.target, self.out)

    def test_every_method_meaning_it_prints_appears_in_full(self):
        n = 0
        for line in self.out.splitlines():
            i = line.find("METHOD MEANS: ")
            if i < 0:
                continue
            n += 1
            shown = line[i + len("METHOD MEANS: "):]
            match = [k for k, v in self.cm.items() if v["best_use"] == shown]
            self.assertTrue(match, "a printed method meaning is truncated or altered: "
                                   f"{shown[-60:]!r}")
        self.assertGreater(n, 0, "no method meanings printed, so this guard has no denominator")

    def test_the_population_this_protects_is_not_empty(self):
        """Coverage. If nothing exceeded the old 104-char cut the guard would prove nothing."""
        over = [k for k, v in self.cm.items() if len(v["best_use"]) > 104]
        self.assertGreater(len(over), 40,
                           "fewer than 40 methods exceed 104 chars, so the truncation this forbids "
                           "would be nearly invisible")

    def test_the_distinct_from_clauses_that_the_cut_removed(self):
        """13 methods lost their disambiguation to the 104-char cut. Name the population."""
        lost = [k for k, v in self.cm.items()
                if "Distinct from" in v["best_use"] and "Distinct from" not in v["best_use"][:104]]
        self.assertGreater(len(lost), 8, "too few cut clauses to be measuring anything")
        for k in lost:
            bu = self.cm[k]["best_use"]
            if bu in self.out:
                self.assertIn(bu[bu.find("Distinct from"):], self.out,
                              f"{k}'s Distinct-from clause is missing from the read brief")


class BriefCarriesTheWholeMeaning(unittest.TestCase):
    """THE BRIEF IS THE ONLY THING AN AUTHORING PASS READS ABOUT A METHOD, so anything cut from it
    is a constraint that cannot be honored.

    `cmd_prepare` used to emit `best_use[:150]`. The house pattern writes a method's disambiguation
    as a TRAILING clause -- "Distinct from <the confusable neighbour>, which ..." -- so the slice
    removed exactly the sentence that keeps two similar methods apart. Measured against canonical
    4a239eef: 37 of 55 best_use fields ran past 150 characters and SIX lost their Distinct-from
    clause outright, with `weed_host_control` cut mid-word at "Disti|nct from garden sanitation".

    The methods the authoring passes have actually confused across batches 1, 3, 4 and 5 --
    off_season_tillage, prompt_harvest, sound_sowing_practice, wet_foliage_discipline -- are the
    truncated ones. This suite exists so that slice cannot come back.

    `cautions` reached the brief nowhere at all: 41 strings across 29 methods, including sulfur's
    90degF limit, copper's aquatic toxicity, Bt killing all lepidoptera, and spinosad's bee
    toxicity. Batch 5's read recorded those cautions missing from crop prose without knowing why.
    An author cannot carry a caution they were never shown."""

    @classmethod
    def setUpClass(cls):
        import tempfile, argparse
        cls.tmp = tempfile.mkdtemp(prefix="brieftest_")
        d = lb.load()
        cls.cm = d["control_methods"]
        target = next(c["slug"] for c in d["crops"]
                      if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"
                      and not lb.laddered(c))
        lb.cmd_prepare(argparse.Namespace(crops=target, out=cls.tmp))
        cls.brief = open(os.path.join(cls.tmp, "brief_catalog.md")).read()

    @classmethod
    def tearDownClass(cls):
        import shutil
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_every_best_use_appears_in_full(self):
        for k, v in self.cm.items():
            self.assertIn(v["best_use"], self.brief,
                          f"{k}'s best_use is truncated or altered in the brief")

    def test_the_population_this_protects_is_not_empty(self):
        """A coverage assertion. If no best_use exceeded the old cut, the test above would pass on
        a truncating brief and prove nothing."""
        over = [k for k, v in self.cm.items() if len(v["best_use"]) > 150]
        self.assertGreater(len(over), 20,
                           "fewer than 20 methods exceed 150 chars, so this guard has almost no "
                           "denominator and the truncation it forbids would be nearly invisible")

    def test_every_distinct_from_clause_survives(self):
        """The clause that keeps two confusable methods apart. Six of these were being cut."""
        n = 0
        for k, v in self.cm.items():
            bu = v["best_use"]
            i = bu.find("Distinct from")
            if i < 0:
                continue
            n += 1
            self.assertIn(bu[i:], self.brief, f"{k}'s Distinct-from clause is missing from the brief")
        self.assertGreater(n, 5, "too few Distinct-from clauses to be measuring anything")

    def test_every_caution_reaches_the_brief(self):
        n = 0
        for k, v in self.cm.items():
            for c in (v.get("cautions") or []):
                n += 1
                self.assertIn(c, self.brief, f"{k}: a caution is missing from the brief")
        self.assertGreater(n, 30, "too few cautions to be measuring anything")

    def test_the_safety_cautions_specifically_are_present(self):
        """Named rather than counted. These four are the ones a wrong ladder can actually hurt
        somebody with, and all four were invisible before."""
        for key, token in (("sulfur", "90"), ("copper_fungicide", "aquatic"),
                           ("bt", "butterfl"), ("spinosad", "bees")):
            cautions = " ".join(self.cm[key].get("cautions") or [])
            self.assertIn(token, cautions, f"{key}'s caution no longer mentions {token!r}")
            self.assertIn(cautions.split(";")[0][:60], self.brief,
                          f"{key}'s safety caution does not reach the brief")

    def test_the_brief_still_names_every_method_and_its_targets(self):
        for k, v in self.cm.items():
            self.assertIn(k, self.brief, f"{k} is missing from the brief entirely")
            self.assertIn(f"applies_to={sorted(v['applies_to'])}", self.brief, k)


if __name__ == "__main__":
    unittest.main(verbosity=2)
