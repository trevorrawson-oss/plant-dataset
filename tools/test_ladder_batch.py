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
                "description_beginner", "description_seasoned")


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
        covered = set()
        for base in (classic, microgreen):
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


class ReportedTwinsAreRealOnCanonical(unittest.TestCase):
    """The live roster: anything the tool advertises as propagate-safe must survive the check."""

    @classmethod
    def setUpClass(cls):
        d = lb.load()
        cert = [c for c in d["crops"]
                if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
        cls.todo = [c for c in cert if not lb.laddered(c)]


    def test_reported_twin_groups_are_byte_identical_in_prose(self):
        twins, _singles = lb.family_cut(self.todo)
        by = {c["slug"]: c for c in self.todo}
        bad = []
        for g in twins:
            g = sorted(g)
            base = by[g[0]]
            for other in g[1:]:
                o = by[other]
                for f in ("pests", "diseases"):
                    for i, p in enumerate(base.get(f) or []):
                        q = (o.get(f) or [])[i] if i < len(o.get(f) or []) else {}
                        for k in PROSE_FIELDS:
                            if p.get(k) != q.get(k):
                                bad.append(f"{g[0]}/{other} {f}[{i}] {p.get('name')} :: {k}")
        self.assertEqual(bad, [], "reported twin groups differ in prose:\n  " + "\n  ".join(bad[:20]))

    def test_the_measurement_is_not_vacuous(self):
        """REACHABILITY. `test_reported_twin_groups_are_byte_identical_in_prose` passes trivially
        if `family_cut` reports NO groups at all -- the exact shape of a guard that reads as
        coverage while checking nothing. Assert the canonical roster actually produces one.

        If this ever fails because the roster genuinely ran out of true twins, DELETE the canonical
        assertion rather than leaving it green and empty.
        """
        twins, singles = lb.family_cut(self.todo)
        self.assertGreater(len(self.todo), 0, "no unladdered crops: the canonical check is vacuous")
        self.assertGreater(len(twins), 0,
                           "family_cut reported ZERO true twin groups on canonical, so the "
                           "byte-identity assertion above has an empty denominator")


if __name__ == "__main__":
    unittest.main(verbosity=2)
