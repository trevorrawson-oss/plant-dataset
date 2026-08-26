#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_planting_time_bestuse.py. Base 48478cb5.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + the mutation harness.

THE LOAD-BEARING FAMILY IS `SheetDoesNotContradictItself`, and it is the family that would have
caught this defect at r5 if it had existed. The shipped `best_use` demanded "one main generation"
in the same sentence pair that named Mexican bean beetle as a documented case. Clemson, the
document the method cites for that case, says the beetle has "usually three generations per year".
The criterion excluded one of its own examples.

Nothing structural could see it. `control_ladder_gate` validates shape; the r5 suite asserted the
prose contained the tokens I said it should; the r5 harness proved those assertions were reachable.
All three were green on a self-contradicting sentence, because every one of them checks that the
prose says what the AUTHOR intended rather than whether the intentions cohere. The guard here is
the coherence itself: **if the sheet names a multi-generation pest as a case, it may not demand a
single generation as the criterion.** That is checkable, and it is checked over the WHOLE sheet
rather than the one field, because a criterion deleted from `best_use` while it survives in
`how_it_works_seasoned` leaves the contradiction live.

`FixIsNotDeletion` is the other half. The cheap way to satisfy a "remove the wrong criterion" bug is
to remove the criterion and say nothing, which passes any absence check and leaves the field vaguer
than it was. So the replacement must positively carry what the mechanism really requires: the single
flight, the several generations, and the July-August damage window that makes the beetle case work.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_planting_time_bestuse as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "acf337809d9085f748bc45b6dfc38dd9c7e88fb92b1408f53879c6bdc0f970a7"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Swap:
    """Temporarily replace a module-level constant, restoring it however the test ends."""

    def __init__(self, name, value):
        self.n, self.v = name, value

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(P, self.n, self.old)
        return False


class Fixture(unittest.TestCase):
    def test_base_reconstructs(self):
        self.assertEqual(
            hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(), P.BASE_SHA)

    def test_post_sha_pinned(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)

    def test_catalog_counts_do_not_move(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(len(post["control_methods"]), len(pre["control_methods"]))
        self.assertEqual(len(post["source_catalog"]), len(pre["source_catalog"]))

    def test_check_passes_on_the_pinned_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_the_base_really_does_carry_the_defect(self):
        """A correction promote is only meaningful if the thing it corrects was actually there.
        Otherwise this whole suite is green over a no-op."""
        m = _pre()["control_methods"][P.KEY]
        self.assertIn("one main generation", m[P.FIELD].lower())
        self.assertIn("mexican bean beetle", m[P.FIELD].lower())


class SheetDoesNotContradictItself(unittest.TestCase):
    """The invariant this defect violated, checked over the whole method sheet."""

    def test_no_single_generation_criterion_survives_anywhere(self):
        m = _post()["control_methods"][P.KEY]
        blob = " ".join(P.prose_of(m)).lower()
        for bad in P.SINGLE_GEN_CRITERIA:
            self.assertNotIn(bad, blob, f"{P.KEY} still demands {bad!r}")

    def test_a_multigeneration_case_and_a_single_generation_criterion_cannot_coexist(self):
        """The general form. Naming a pest that runs several generations while demanding one is the
        contradiction, whichever field each half lives in."""
        m = _post()["control_methods"][P.KEY]
        blob = " ".join(P.prose_of(m)).lower()
        if "mexican bean beetle" in blob:
            for bad in P.SINGLE_GEN_CRITERIA:
                self.assertNotIn(
                    bad, blob,
                    "the sheet names a pest its own source puts at three generations a year while "
                    "demanding a single generation as the criterion")

    def test_the_guard_would_have_caught_the_shipped_defect(self):
        """Run the same invariant against the PRE state. It must FAIL there, or the guard is
        decorative: a check that passes on the known-bad input proves nothing."""
        m = _pre()["control_methods"][P.KEY]
        blob = " ".join(P.prose_of(m)).lower()
        self.assertIn("mexican bean beetle", blob)
        self.assertTrue(any(bad in blob for bad in P.SINGLE_GEN_CRITERIA),
                        "the pre state does not carry the criterion, so this guard is not "
                        "demonstrated to catch anything")

    def test_both_documented_cases_survive_the_rewrite(self):
        bu = _post()["control_methods"][P.KEY][P.FIELD].lower()
        self.assertIn("squash vine borer", bu)
        self.assertIn("mexican bean beetle", bu)


class FixIsNotDeletion(unittest.TestCase):
    """Removing the wrong criterion without stating the right one makes the field vaguer."""

    def test_the_replacement_states_what_the_mechanism_requires(self):
        bu = _post()["control_methods"][P.KEY][P.FIELD].lower()
        for need in P.MUST_CARRY:
            self.assertIn(need, bu)

    def test_check_REFUSES_a_replacement_that_only_deletes(self):
        thin = ("A pest whose damage falls in a predictable, locally published stretch of the "
                "season. Distinct from crop rotation, which moves the planting in space; this one "
                "moves it in time.")
        with _Swap("NEW", thin):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("merely delete", out)

    def test_check_REFUSES_a_replacement_that_keeps_the_criterion(self):
        still_bad = P.NEW.replace("a predictable, locally published stretch of the season",
                                  "one main generation and a published local emergence window")
        with _Swap("NEW", still_bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("single-generation criterion", out)

    def test_check_REFUSES_a_no_op(self):
        with _Swap("NEW", P.OLD):
            out = P.check(_pre())
        self.assertIsNotNone(out)

    def test_check_REFUSES_running_over_its_own_output(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("not the text this correction was written against", out)

    def test_check_REFUSES_a_criterion_surviving_in_another_field(self):
        """Deleting it from best_use while it lives on in how_it_works is not a fix."""
        pre = _pre()
        pre["control_methods"][P.KEY]["how_it_works_seasoned"] += (
            " This suits a pest with one main generation.")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("another field", out)

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        with _Swap("NEW", P.NEW + " It always works."):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("hygiene", out)

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("a — dash"))
        self.assertIsNotNone(P.hygiene("the colour of it"))
        self.assertIsNone(P.hygiene(P.NEW))


class BlastRadius(unittest.TestCase):
    def test_only_one_field_of_one_method_changes(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(set(post["control_methods"]), set(pre["control_methods"]))
        for k in pre["control_methods"]:
            if k == P.KEY:
                continue
            self.assertEqual(post["control_methods"][k], pre["control_methods"][k], k)
        a, b = pre["control_methods"][P.KEY], post["control_methods"][P.KEY]
        self.assertEqual(set(a), set(b))
        self.assertEqual([f for f in a if a[f] != b[f]], [P.FIELD])

    def test_sourcing_is_untouched(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(post["control_methods"][P.KEY]["sources"],
                         pre["control_methods"][P.KEY]["sources"])
        self.assertEqual(post["control_methods"][P.KEY]["anchoring_urls"],
                         pre["control_methods"][P.KEY]["anchoring_urls"])
        self.assertEqual(post["source_catalog"], pre["source_catalog"])

    def test_no_crop_is_touched(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(json.dumps(post["crops"], sort_keys=True),
                         json.dumps(pre["crops"], sort_keys=True))

    def test_verify_post_CATCHES_a_touched_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["crops"][0]["name"] = "MUTATED"
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_second_field_moving(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"][P.KEY]["how_it_works_beginner"] += " Extra."
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_an_edited_bystander(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["crop_rotation"]["best_use"] += " Also moves it in time."
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_dropped_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        del d["control_methods"]["kaolin_clay"]
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_criterion_surviving_in_the_post_state(self):
        """Reachable only because the criterion scan is verify_post's FIRST line. Below the
        per-field comparison this was dead: every post state carrying a criterion also trips a
        field comparison, and the harness reported it as a surviving mutation."""
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"][P.KEY]["how_it_works_seasoned"] += (
            " Best on a pest with one main generation.")
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("still carries", out)

    def test_verify_post_CATCHES_a_changed_source_catalog(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["source_catalog"]["umn_ext"]["accessed"] = "2099-01"
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_running_over_its_own_output_is_refused_by_the_base_check(self):
        """The dead "already corrected" branch was removed; this pins that the refusal still
        happens, and names which check does it."""
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("not the text this correction was written against", out)

    def test_verify_post_is_clean_on_the_real_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(P.snapshot(pre), d))


class GateContract(unittest.TestCase):
    def test_the_gates_stay_clean_on_the_post_state(self):
        post = _post()
        self.assertEqual(CLG.catalog_violations(CLG.catalog(post)), [])
        self.assertEqual(CLG.all_violations(post), [])

    def test_applies_to_is_untouched_by_a_prose_correction(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(post["control_methods"][P.KEY]["applies_to"],
                         pre["control_methods"][P.KEY]["applies_to"])
        self.assertEqual(post["control_methods"][P.KEY]["applies_to"],
                         ["insect_chewing", "insect_boring"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
