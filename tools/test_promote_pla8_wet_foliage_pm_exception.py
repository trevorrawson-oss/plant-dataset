#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_wet_foliage_pm_exception.py. Base 4a239eef.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + the mutation harness.

TWO FAMILIES CARRY THIS SUITE, AND THEY PULL IN OPPOSITE DIRECTIONS ON PURPOSE.

`ExceptionIsStated` checks the fix landed and says something specific enough to act on: it must name
the pathogen it excepts, the mechanism that does not apply (free water), and what does the work
instead (airflow). A vaguer sentence would pass an "is it there" check and leave the next authoring
pass exactly where it was.

`NotOverCorrected` checks the fix did NOT go further than the evidence. The tempting stronger move
is to drop `fungal_foliar` from `applies_to`, which would "fix" powdery mildew by breaking ascochyta
blight and anthracnose -- the splash-dispersed foliar fungi this method was minted for, and the use
it correctly keeps on the same two pea crops. `applies_to` is frozen in both `check` and
`verify_post`.

`ReachesTheAuthoringBrief` is the one that would have caught the version of this fix I nearly
shipped. Until `603f4f8` the brief emitted only `applies_to` and a 150-character slice of
`best_use`; 41 caution strings across 29 methods reached it nowhere. **A caution added before that
commit would have read as protection while doing nothing.** So this suite does not trust that the
field is consumed -- it generates a real brief and looks for the sentence.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_wet_foliage_pm_exception as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "17d0eac762fc22b07fb5ec6a83c9f08471202e3c5ddf9bb7010fc861af5f0688"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Swap:
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

    def test_the_base_really_lacks_the_exception(self):
        """A correction is only meaningful if the gap was actually there."""
        m = _pre()["control_methods"][P.KEY]
        blob = " ".join(m.get("cautions") or []).lower()
        self.assertNotIn("powdery mildew", blob)


class ExceptionIsStated(unittest.TestCase):
    def test_the_caution_lands(self):
        self.assertIn(P.CAUTION, _post()["control_methods"][P.KEY]["cautions"])

    def test_it_names_the_pathogen_the_mechanism_and_the_alternative(self):
        low = P.CAUTION.lower()
        for need in P.MUST_CARRY:
            self.assertIn(need, low)

    def test_check_REFUSES_a_vaguer_replacement(self):
        with _Swap("CAUTION", "This does not suit every foliar disease."):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must name the pathogen", out)

    def test_check_REFUSES_a_caution_that_is_already_present(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already carries this caution", out)

    def test_the_existing_caution_survives(self):
        pre = _pre()
        post = _post(pre)
        for c in pre["control_methods"][P.KEY]["cautions"]:
            self.assertIn(c, post["control_methods"][P.KEY]["cautions"])

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        with _Swap("CAUTION", P.CAUTION + " This never applies."):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("hygiene", out)

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("a — dash"))
        self.assertIsNone(P.hygiene(P.CAUTION))


class NotOverCorrected(unittest.TestCase):
    """The fix must not go further than the evidence."""

    def test_applies_to_is_unchanged(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(post["control_methods"][P.KEY]["applies_to"],
                         pre["control_methods"][P.KEY]["applies_to"])
        self.assertEqual(post["control_methods"][P.KEY]["applies_to"], P.FROZEN_APPLIES_TO)

    def test_check_REFUSES_narrowing_the_target(self):
        """Dropping fungal_foliar would break ascochyta and anthracnose to fix powdery mildew."""
        pre = _pre()
        pre["control_methods"][P.KEY]["applies_to"] = ["bacterial"]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("must not narrow the target", out)

    def test_verify_post_REFUSES_narrowing_after_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"][P.KEY]["applies_to"] = ["bacterial"]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("must not narrow", out)

    def test_the_method_is_still_reachable_from_a_fungal_problem(self):
        from control_ladder_gate import TYPE_TARGETS
        targets = set(_post()["control_methods"][P.KEY]["applies_to"])
        self.assertTrue(targets & set(TYPE_TARGETS["fungal"]),
                        "ascochyta and anthracnose can no longer reach this method")
        self.assertTrue(targets & set(TYPE_TARGETS["bacterial"]))


class ReachesTheAuthoringBrief(unittest.TestCase):
    """A caution the brief does not emit is protection that cannot be read.

    Before `603f4f8`, `cmd_prepare` emitted only applies_to and `best_use[:150]`, so every one of
    the catalog's 41 caution strings was invisible at authoring time. This test refuses to assume
    the field is consumed: it generates a real brief from a post-promote catalog and looks for the
    sentence."""

    def test_the_new_caution_appears_in_a_generated_brief(self):
        import argparse, shutil, tempfile
        # DO NOT re-insert the tools dir here. The module-level sys.path already covers it, and a
        # local insert puts the REAL tools directory ahead of whatever the mutation harness staged,
        # so this test would import an unmutated ladder_batch and pass while the emission it checks
        # was broken. Both `brief` mutations survived exactly that way on the first harness run.
        import ladder_batch as lb
        post = _post()
        tmp = tempfile.mkdtemp(prefix="pmbrief_")
        real_load = lb.load
        try:
            lb.load = lambda *a, **k: post
            target = next(c["slug"] for c in post["crops"]
                          if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"
                          and not lb.laddered(c))
            lb.cmd_prepare(argparse.Namespace(crops=target, out=tmp))
            brief = open(os.path.join(tmp, "brief_catalog.md")).read()
        finally:
            lb.load = real_load
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertIn(P.CAUTION, brief,
                      "the caution does not reach the authoring brief, so it protects nothing")
        self.assertIn("powdery mildew", brief.lower())
        # The caution is only half the protection on this method. The other half is best_use's
        # trailing "Distinct from watering at the base ... this one changes where you go" clause,
        # which the brief truncated away until 603f4f8. Assert it survives too, or a reinstated
        # `[:150]` slice would leave this test green while gutting the sheet it protects.
        self.assertIn(post["control_methods"][P.KEY]["best_use"], brief,
                      "best_use is truncated in the brief, so the Distinct-from clause that keeps "
                      "this method apart from watering at the base is invisible again")


class BlastRadius(unittest.TestCase):
    def test_only_this_method_changes(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(set(post["control_methods"]), set(pre["control_methods"]))
        for k in pre["control_methods"]:
            if k == P.KEY:
                continue
            self.assertEqual(post["control_methods"][k], pre["control_methods"][k], k)

    def test_only_three_fields_move_on_it(self):
        pre = _pre()
        post = _post(pre)
        a, b = pre["control_methods"][P.KEY], post["control_methods"][P.KEY]
        self.assertEqual(set(a), set(b))
        self.assertEqual(sorted(f for f in a if a[f] != b[f]),
                         ["anchoring_urls", "cautions", "sources"])

    def test_source_catalog_and_crops_are_untouched(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(json.dumps(post["source_catalog"], sort_keys=True),
                         json.dumps(pre["source_catalog"], sort_keys=True))
        self.assertEqual(json.dumps(post["crops"], sort_keys=True),
                         json.dumps(pre["crops"], sort_keys=True))

    def test_existing_anchors_are_not_overwritten(self):
        pre = _pre()
        post = _post(pre)
        for sid, a in pre["control_methods"][P.KEY]["anchoring_urls"].items():
            self.assertEqual(post["control_methods"][P.KEY]["anchoring_urls"][sid], a)
        self.assertEqual(post["control_methods"][P.KEY]["anchoring_urls"][P.SOURCE]["url"],
                         P.SOURCE_URL)

    def test_apply_RAISES_on_an_anchor_collision(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        d["control_methods"][P.KEY]["anchoring_urls"][P.SOURCE] = {"url": "https://x.edu/",
                                                                   "verified": "2026-01-01"}
        with self.assertRaises(AssertionError):
            P.apply_to(d)

    def test_verify_post_CATCHES_a_dropped_existing_caution(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"][P.KEY]["cautions"] = [P.CAUTION]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("existing caution was dropped", out)

    def test_verify_post_CATCHES_a_touched_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["crops"][0]["name"] = "MUTATED"
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_an_edited_bystander(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["airflow_spacing"]["best_use"] += " Extra."
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("untouched method", out)

    def test_verify_post_CATCHES_another_field_moving(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"][P.KEY]["how_it_works_beginner"] += " Extra."
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("only cautions/sources/anchoring_urls", out)

    def test_verify_post_is_clean_on_the_real_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(P.snapshot(pre), d))


class GateContract(unittest.TestCase):
    def test_gates_are_clean_on_the_post_state(self):
        post = _post()
        self.assertEqual(CLG.catalog_violations(CLG.catalog(post)), [])
        self.assertEqual(CLG.all_violations(post), [])

    def test_the_three_shipped_uses_are_all_bacterial_and_survive(self):
        """The method is live on exactly three problems today, all bacterial blights on the beans,
        all correct. This correction must not disturb them."""
        post = _post()
        uses = [(c["slug"], p["id"], p["type"])
                for c in post["crops"]
                for p in (c.get("pests") or []) + (c.get("diseases") or [])
                if isinstance(p, dict)
                for r in (p.get("control_ladder") or []) if r["method"] == P.KEY]
        self.assertEqual(len(uses), 3)
        for _slug, _pid, ptype in uses:
            self.assertEqual(ptype, "bacterial")


if __name__ == "__main__":
    unittest.main(verbosity=2)
