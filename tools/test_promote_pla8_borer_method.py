#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_borer_method.py. Base 5696aead.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_borer_method_suite.py.

THE LOAD-BEARING FAMILY IS `NarrowScope`. This method exists because `handpick` was the wrong key
for a larva inside a stem, and the whole value of minting it is that the gate can now tell those two
apart. If `applies_to` ever widens beyond `insect_boring`, the new method becomes a second handpick
and the gap it was minted to close reopens with an extra key in the catalog to show for it.

`HedgesSurvive` is the other half. BOTH sources qualify this method's success -- UMN "you may not be
able to save the plant", ISU "can sometimes be successfully removed ... during July or early
August". A dropped qualifier is a defect with no term to scan for, so the hedges and the seasonal
window are asserted explicitly rather than trusted to review.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_borer_method as P  # noqa: E402
import build_pla8_borer_method_content as C  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

POST_SHA = "e40cd8ecb612a292880fa4a75f62ebc14267123914fa16d023903c9e63aac9bd"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


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

    def test_catalog_goes_50_to_51(self):
        self.assertEqual(len(_pre()["control_methods"]), 50)
        self.assertEqual(len(_post()["control_methods"]), 51)


class NarrowScope(unittest.TestCase):
    """The scope is the point. Widening it recreates the confusion the method resolves."""

    def test_applies_to_is_exactly_insect_boring(self):
        self.assertEqual(_post()["control_methods"][C.KEY]["applies_to"], ["insect_boring"])

    def test_check_REFUSES_a_wider_scope(self):
        orig = list(C.METHOD["applies_to"])
        try:
            C.METHOD["applies_to"] = ["insect_boring", "insect_chewing"]
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("insect_boring", out)
        finally:
            C.METHOD["applies_to"] = orig

    def test_it_is_legal_on_an_insect_and_ILLEGAL_on_a_surface_only_type(self):
        """The gate contract: reachable for the borer, refused for a mollusk or a disease."""
        targets = set(_post()["control_methods"][C.KEY]["applies_to"])
        self.assertTrue(targets & set(TYPE_TARGETS["insect"]), "unreachable for insect problems")
        for t in ("mollusk", "fungal", "bacterial", "viral", "physiological", "nematode",
                  "vertebrate", "mite"):
            self.assertFalse(targets & set(TYPE_TARGETS[t]), f"wrongly legal on {t}")

    def test_it_does_not_duplicate_handpick(self):
        """If the two ever cover the same targets, one of them is redundant and the split that
        motivated this mint has collapsed."""
        post = _post()["control_methods"]
        self.assertNotEqual(set(post[C.KEY]["applies_to"]), set(post["handpick"]["applies_to"]))
        self.assertNotIn("insect_chewing", post[C.KEY]["applies_to"])


class HedgesSurvive(unittest.TestCase):
    """Both sources qualify this method's success. A dropped qualifier has no term to scan for."""

    def _blob(self):
        m = _post()["control_methods"][C.KEY]
        return " ".join(P.prose_of(m)).lower()

    def test_the_failure_case_is_stated(self):
        self.assertRegex(self._blob(), r"may not|not work every time")

    def test_the_seasonal_window_survives(self):
        self.assertIn("july or early august", self._blob())

    def test_the_cons_carry_the_failure_not_just_the_prose(self):
        cons = " ".join(_post()["control_methods"][C.KEY]["cons"]).lower()
        self.assertIn("may not save the plant", cons)

    def test_check_REFUSES_prose_with_every_hedge_stripped(self):
        orig = C.METHOD["how_it_works_beginner"], C.METHOD["how_it_works_seasoned"], list(C.METHOD["cons"])
        try:
            C.METHOD["how_it_works_beginner"] = "Cut the stem, take out the grub, mound soil over it."
            C.METHOD["how_it_works_seasoned"] = "Extraction in July or early August; mound soil to re-root."
            C.METHOD["cons"] = ["Reaches only the larvae you find"]
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("hedge", out)
        finally:
            (C.METHOD["how_it_works_beginner"], C.METHOD["how_it_works_seasoned"],
             C.METHOD["cons"]) = orig[0], orig[1], orig[2]

    def test_check_REFUSES_a_dropped_seasonal_window(self):
        """Stripped from BOTH fields that carry it, which is the honest failure mode.

        The first version removed it from how_it_works_seasoned only and the check stayed silent,
        because best_use carries the window too and the guard scans the whole prose blob. That is
        the guard behaving correctly -- the window had not actually been dropped -- but the test was
        claiming to exercise something it was not. Two fields carry it, so a real loss removes both.
        """
        orig_s, orig_b = C.METHOD["how_it_works_seasoned"], C.METHOD["best_use"]
        try:
            C.METHOD["how_it_works_seasoned"] = orig_s.replace("July or early August", "midsummer")
            C.METHOD["best_use"] = orig_b.replace("July or early August", "midsummer")
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("window", out)
        finally:
            C.METHOD["how_it_works_seasoned"], C.METHOD["best_use"] = orig_s, orig_b

    def test_the_window_is_carried_in_BOTH_fields_that_should_have_it(self):
        """Pins why the test above must strip two fields, so a later edit that moves the window to
        one place does not quietly make that test vacuous again."""
        m = _post()["control_methods"][C.KEY]
        self.assertIn("July or early August", m["how_it_works_seasoned"])
        self.assertIn("July or early August", m["best_use"])


class SourcingIsReal(unittest.TestCase):
    def test_both_sources_are_T1_and_in_the_catalog(self):
        sc = _post()["source_catalog"]
        for s in C.METHOD["sources"]:
            self.assertIn(s, sc)
            self.assertEqual((sc[s].get("tier") or "").upper(), "T1", s)

    def test_every_source_has_an_https_anchor_with_a_verified_date(self):
        for s, a in C.METHOD["anchoring_urls"].items():
            self.assertIn(s, C.METHOD["sources"])
            self.assertTrue(a["url"].startswith("https://"), s)
            self.assertRegex(a["verified"], r"^\d{4}-\d{2}-\d{2}$")

    def test_the_ISU_anchor_is_the_LIVE_url_not_the_redirecting_one(self):
        """yellow-summer-squash and zucchini still cite hortnews.extension.iastate.edu, which now
        301-redirects. The document is alive; only the URL moved. This mint anchors the new one.
        The crop repoint is deliberately NOT part of this promote."""
        url = C.METHOD["anchoring_urls"]["iastate_ext"]["url"]
        self.assertIn("yardandgarden.extension.iastate.edu", url)
        self.assertNotIn("hortnews", url)

    def test_check_REFUSES_a_source_missing_its_anchor(self):
        orig = dict(C.METHOD["anchoring_urls"])
        try:
            C.METHOD["anchoring_urls"] = {"umn_ext": orig["umn_ext"]}
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("anchoring_url", out)
        finally:
            C.METHOD["anchoring_urls"] = orig


class BlastRadius(unittest.TestCase):
    def test_no_existing_method_changes(self):
        pre, post = _pre(), _post()
        self.assertEqual(set(post["control_methods"]) - set(pre["control_methods"]), {C.KEY})
        for k in pre["control_methods"]:
            self.assertEqual(pre["control_methods"][k], post["control_methods"][k], k)

    def test_zero_crops_change(self):
        pre = _pre()
        post = _post(pre)
        by = {c["slug"]: c for c in post["crops"]}
        self.assertEqual([c["slug"] for c in pre["crops"]], [c["slug"] for c in post["crops"]])
        self.assertEqual([c["slug"] for c in pre["crops"] if c != by[c["slug"]]], [])

    def test_no_source_catalog_change(self):
        pre = _pre()
        self.assertEqual(pre["source_catalog"], _post(pre)["source_catalog"])

    def test_no_ladder_points_at_it_yet(self):
        """This promote mints only. Batch 4's promote is what attaches rungs."""
        post = _post()
        for c in post["crops"]:
            for f in ("pests", "diseases"):
                for p in (c.get(f) or []):
                    if isinstance(p, dict):
                        for r in (p.get("control_ladder") or []):
                            self.assertNotEqual(r["method"], C.KEY)


class Shape(unittest.TestCase):
    def test_every_required_field_present(self):
        m = _post()["control_methods"][C.KEY]
        for f in P.REQUIRED:
            self.assertIn(f, m)
            self.assertTrue(m[f], f)

    def test_it_matches_the_shape_of_the_other_50(self):
        post = _post()["control_methods"]
        common = set.intersection(*(set(v) for k, v in post.items() if k != C.KEY))
        self.assertTrue(common <= set(post[C.KEY]), sorted(common - set(post[C.KEY])))

    def test_tier_is_valid(self):
        self.assertIn(_post()["control_methods"][C.KEY]["tier"], P.TIERS)

    def test_copy_hygiene_on_all_prose(self):
        for s in P.prose_of(_post()["control_methods"][C.KEY]):
            self.assertIsNone(P.hygiene(s), s[:70])

    def test_hygiene_is_not_vacuous(self):
        for bad in ("an em dash — here", "it is completely safe", "the colour", "this is safe to eat"):
            self.assertIsNotNone(P.hygiene(bad), bad)


class Reachability(unittest.TestCase):
    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_refuses_when_already_minted(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already in the catalog", out)

    def test_apply_raises_on_double_mint(self):
        d = _post()
        with self.assertRaises(AssertionError):
            P.apply_to(d)

    def test_post_check_fails_on_the_base(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_check_CATCHES_a_widened_scope_that_slipped_past_check(self):
        """Isolates verify_post's scope guard.

        check() refuses a wide scope before apply ever runs, so nothing a normal test does can make
        verify_post's copy of that assertion speak -- it is the second line of a defense whose first
        line always fires. Disabling it therefore changed nothing observable. Driving verify_post
        directly with a doctored post-state is the only way it can be reached, and it is worth
        keeping: check() reads the CONSTANT, verify_post reads what actually landed in the data.
        """
        d = _post()
        d["control_methods"][C.KEY]["applies_to"] = ["insect_boring", "insect_chewing"]
        out = P.verify_post(d)
        self.assertIsNotNone(out)
        self.assertIn("narrow scope", out)

    def test_refuses_a_missing_required_field(self):
        orig = C.METHOD.pop("best_use")
        try:
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("best_use", out)
        finally:
            C.METHOD["best_use"] = orig

    def test_refuses_a_source_missing_from_the_catalog(self):
        orig, oa = list(C.METHOD["sources"]), dict(C.METHOD["anchoring_urls"])
        try:
            C.METHOD["sources"] = orig + ["not_a_real_source"]
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("source_catalog", out)
        finally:
            C.METHOD["sources"], C.METHOD["anchoring_urls"] = orig, oa

    def test_refuses_a_source_that_is_IN_the_catalog_but_NOT_T1(self):
        """Isolates the tier check from the membership check that runs before it.

        The first version added a source that did not exist at all, so the earlier
        "not in source_catalog" branch fired and the tier check was never reached -- disabling it
        changed nothing and the harness scored it a survivor. `almanac` is a real T2 entry, so
        membership passes and only the tier check can object.
        """
        orig, oa = list(C.METHOD["sources"]), dict(C.METHOD["anchoring_urls"])
        try:
            C.METHOD["sources"] = orig + ["almanac"]
            C.METHOD["anchoring_urls"] = dict(oa, almanac={"url": "https://www.almanac.com/x",
                                                           "verified": "2026-08-25"})
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("not T1", out, f"the tier check did not fire; got: {out}")
        finally:
            C.METHOD["sources"], C.METHOD["anchoring_urls"] = orig, oa


if __name__ == "__main__":
    unittest.main(verbosity=2)
