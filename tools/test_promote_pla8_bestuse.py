#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_bestuse.py. Base decb944d.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_bestuse_suite.py.

THE LOAD-BEARING FAMILIES ARE `LeftAlone` AND `ScopeIsExact`.

`best_use` is read on two surfaces: ladder_batch.py hands it to authoring agents as "what the method
MEANS", and MethodSheet.tsx renders it to users. So a bad edit here is simultaneously a content
defect and a defect in every future authoring pass, which is why this promote is narrow to the point
of pedantry -- exactly 10 strings, one field, zero crops.

`LeftAlone` guards the one method the detector flagged and the READ spared. `bottom_watering`'s
best_use already names both its shipped problems and correctly confines the method to indoor trays
and seedlings. That confinement is not narrowness to be fixed: `bottom_watering` MEANS water from
below in trays, and twelve authored rungs in batch 1 used it to mean water at the base outdoors.
Widening it would re-open the worst defect the rollout has produced. 11 flagged, 10 real.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_bestuse as P  # noqa: E402
import build_pla8_bestuse_content as C  # noqa: E402

POST_SHA = "3ec673a76717c0a9fbfe9861d6d63ee36e574d59a88b3e3b3b97cccb29253027"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


# --------------------------------------------------------------------------- fixture
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


# --------------------------------------------------------------------------- load-bearing
class LeftAlone(unittest.TestCase):
    """bottom_watering was flagged by the detector and spared by the read."""

    def test_bottom_watering_is_byte_identical(self):
        pre, post = _pre(), _post()
        self.assertEqual(pre["control_methods"]["bottom_watering"],
                         post["control_methods"]["bottom_watering"])

    def test_it_still_confines_itself_to_trays_and_seedlings(self):
        """The distinction batch 1 got wrong twelve times. If this wording ever loosens, the key
        stops meaning a different action from water_at_the_base."""
        s = _post()["control_methods"]["bottom_watering"]["best_use"]
        self.assertIn("trays", s.lower())
        self.assertIn("seedlings", s.lower())

    def test_water_at_the_base_still_disambiguates_itself_from_it(self):
        """The sibling half of the same distinction, untouched by this promote."""
        s = _post()["control_methods"]["water_at_the_base"]["best_use"]
        self.assertIn("bottom watering", s.lower())

    def test_the_promote_REFUSES_if_an_excluded_method_is_widened(self):
        """And the OVERLAP check must be the one that fires, identified by its message.

        Asserting only that check() returned something passed with the overlap guard deleted: the
        injected entry's bogus `old` then failed the drifted-text check further down and check()
        refused anyway, for a different reason. The harness scored it a survivor. Pin the guard to
        its own diagnosis, not to the bare fact of a refusal.
        """
        orig = dict(C.WIDENINGS)
        try:
            C.WIDENINGS["bottom_watering"] = {"why": "x", "old": "y", "new": "z"}
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("in BOTH", out,
                          f"the EXCLUDED/WIDENINGS overlap guard did not fire; got: {out}")
        finally:
            C.WIDENINGS.clear(); C.WIDENINGS.update(orig)
        self.assertEqual(len(C.WIDENINGS), 10, "WIDENINGS was not restored")

    def test_the_other_39_methods_are_untouched(self):
        pre, post = _pre(), _post()
        changed = [k for k in pre["control_methods"]
                   if pre["control_methods"][k] != post["control_methods"][k]]
        self.assertEqual(sorted(changed), sorted(C.WIDENINGS))


class ScopeIsExact(unittest.TestCase):
    """Exactly 10 strings, one field, zero crops."""

    def test_only_best_use_changes_on_the_widened_methods(self):
        pre, post = _pre(), _post()
        for k in C.WIDENINGS:
            a, b = dict(pre["control_methods"][k]), dict(post["control_methods"][k])
            self.assertNotEqual(a.pop("best_use"), b.pop("best_use"), k)
            self.assertEqual(a, b, f"{k}: a field other than best_use moved")

    def test_method_key_set_identical_before_value_comparison(self):
        """set(pre) == set(post) FIRST. Iterating pre alone makes ADDITIONS invisible."""
        pre, post = _pre(), _post()
        self.assertEqual(set(pre["control_methods"]), set(post["control_methods"]))
        self.assertEqual(set(pre.keys()), set(post.keys()))

    def test_zero_crops_change(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual([c["slug"] for c in pre["crops"]], [c["slug"] for c in post["crops"]])
        by = {c["slug"]: c for c in post["crops"]}
        changed = [c["slug"] for c in pre["crops"] if c != by[c["slug"]]]
        self.assertEqual(changed, [])

    def test_no_source_catalog_change(self):
        pre = _pre()
        self.assertEqual(pre["source_catalog"], _post(pre)["source_catalog"])

    def test_no_ladder_anywhere_changes(self):
        """The 19 laddered crops point AT these methods; a promote that moved a rung would be
        changing content this one has no business touching."""
        pre = _pre()
        post = _post(pre)
        def ladders(d):
            return [(c["slug"], p.get("id"), [r["method"] for r in p.get("control_ladder") or []])
                    for c in d["crops"] for f in ("pests", "diseases")
                    for p in (c.get(f) or []) if isinstance(p, dict) and p.get("control_ladder")]
        self.assertEqual(ladders(pre), ladders(post))
        self.assertEqual(len(ladders(post)), 149,
                         "19 laddered crops carry 149 laddered problems at decb944d")


# --------------------------------------------------------------------------- the content
class WidenedContent(unittest.TestCase):
    def test_ten_widenings(self):
        self.assertEqual(len(C.WIDENINGS), 10)
        self.assertEqual(len(C.EXCLUDED), 1)

    def test_promote_REFUSES_if_the_widening_COUNT_drifts_from_the_constant(self):
        """The only way `len(C.WIDENINGS) != 10` can fire.

        Asserting the constant equals 10 tests the CONSTANT, not the check that reads it. Nothing
        made check() ever see a different count, so disabling it changed nothing observable and the
        harness scored it a survivor -- the same unreachable-guard shape as batch 3's read-fix
        count. Dropping an entry keeps every per-method check passing, so the count guard is the
        only one left that can object.
        """
        orig = dict(C.WIDENINGS)
        try:
            C.WIDENINGS.pop("handpick")
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("expected 10 widenings", out,
                          f"the COUNT guard did not fire; got: {out}")
        finally:
            C.WIDENINGS.clear(); C.WIDENINGS.update(orig)
        self.assertEqual(len(C.WIDENINGS), 10, "WIDENINGS was not restored")

    def test_every_new_string_passes_copy_hygiene(self):
        for k, w in C.WIDENINGS.items():
            with self.subTest(method=k):
                self.assertIsNone(P.hygiene(w["new"]), f"{k}: {P.hygiene(w['new'])}")

    def test_hygiene_is_not_vacuous(self):
        """COVERAGE of the rule set: each check must reject something, or a typo in a pattern
        silently turns that rule off and every string 'passes'."""
        # "Plant it deep" is deliberately NOT here: sentence-initial Plant is ALLOWED, and using
        # it as a negative fixture would have asserted the opposite of the house rule.
        for bad in ("an em dash — here", "a double -- hyphen", "it is completely safe",
                    "at 85 °F", "the colour of it", "you should Plant it deep",
                    "this is safe to eat"):
            with self.subTest(bad=bad):
                self.assertIsNotNone(P.hygiene(bad), f"hygiene accepted {bad!r}")

    def test_every_widening_actually_widens(self):
        """A 'widening' that shortens or merely reflows is not what this promote claims to do."""
        for k, w in C.WIDENINGS.items():
            with self.subTest(method=k):
                self.assertGreater(len(w["new"]), len(w["old"]), k)
                self.assertNotEqual(w["new"], w["old"], k)

    def test_off_season_tillage_drops_the_wrong_mechanism(self):
        """The factual correction. It named a life stage European corn borer does not have."""
        s = _post()["control_methods"]["off_season_tillage"]["best_use"]
        self.assertNotIn("soil-pupating", s)
        self.assertIn("stalks", s.lower())
        self.assertIn("corn borer", s.lower())

    def test_off_season_tillage_keeps_its_disambiguation(self):
        """It exists partly to NOT be garden_sanitation; losing that line re-opens a merge."""
        s = _post()["control_methods"]["off_season_tillage"]["best_use"]
        self.assertIn("garden sanitation", s.lower())

    def test_resistant_varieties_now_admits_non_disease_traits(self):
        """The batch-3 case: an agent read the old text as disease-only and refused a rung its
        crop's own prose earned, against eight shipped insect uses across six crops."""
        s = _post()["control_methods"]["resistant_varieties"]["best_use"].lower()
        self.assertTrue("less drawn to" in s or "husk" in s, s)

    def test_floating_row_cover_now_admits_vector_exclusion(self):
        """Seven of its shipped rungs are bacterial: keeping the carrier off the plant."""
        s = _post()["control_methods"]["floating_row_cover"]["best_use"].lower()
        self.assertIn("bacterial wilt", s)

    def test_even_watering_now_admits_the_mite_case(self):
        """Half its shipped rungs are spider mites; the field was entirely calcium-framed."""
        s = _post()["control_methods"]["even_watering"]["best_use"].lower()
        self.assertIn("mite", s)

    def test_balance_nitrogen_drops_the_crop_restriction(self):
        """It ships on tomato, strawberry, pepper and the cucumbers, none of them leafy or cole."""
        s = _post()["control_methods"]["balance_nitrogen"]["best_use"].lower()
        self.assertNotIn("cole", s)

    def test_bt_keeps_the_non_target_caveat(self):
        """The corrected register and cautions both carry it; the surface a reader consults when
        DECIDING to use it should not be the one place that omits it."""
        s = _post()["control_methods"]["bt"]["best_use"].lower()
        self.assertIn("butterflies", s)
        self.assertNotIn("only affects caterpillars", s)

    def test_lengths_stay_in_the_existing_band(self):
        """best_use renders as a paragraph. Doubling every string would be a UI change smuggled in
        as a content fix."""
        post = _post()
        longest = max(len(m.get("best_use") or "") for m in post["control_methods"].values())
        self.assertLessEqual(longest, 420, "a best_use grew well past the existing distribution")


# --------------------------------------------------------------------------- reachability
class Reachability(unittest.TestCase):
    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_base_fails_the_post_check(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_passes_the_post_check(self):
        self.assertIsNone(P.verify_post(_post()))

    def test_refuses_when_already_applied(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already widened", out)

    def test_refuses_if_a_current_best_use_was_edited_by_someone_else(self):
        d = _pre()
        d["control_methods"]["handpick"]["best_use"] = "Something else entirely."
        out = P.check(d)
        self.assertIsNotNone(out)
        self.assertIn("changed under this pass", out)

    def test_refuses_a_missing_method(self):
        d = _pre()
        del d["control_methods"]["handpick"]
        self.assertIsNotNone(P.check(d))

    def test_refuses_new_prose_that_fails_hygiene(self):
        orig = C.WIDENINGS["handpick"]["new"]
        try:
            C.WIDENINGS["handpick"]["new"] = "This is completely harmless to everything."
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("copy hygiene", out)
        finally:
            C.WIDENINGS["handpick"]["new"] = orig

    def test_apply_raises_on_a_mismatch_rather_than_overwriting(self):
        d = _pre()
        d["control_methods"]["bt"]["best_use"] = "drifted"
        with self.assertRaises(AssertionError):
            P.apply_to(d)


if __name__ == "__main__":
    unittest.main(verbosity=2)
