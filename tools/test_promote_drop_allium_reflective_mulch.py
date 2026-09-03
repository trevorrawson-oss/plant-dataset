#!/usr/bin/env python3
"""Guard suite for tools/promote_drop_allium_reflective_mulch.py. Base f851dc15.

REPLAY-PINNED; no RED phase is claimed. Evidence the guards are live: `MainWiringIsDriven` plus
tools/mutate_drop_allium_reflective_suite.py.

`PositiveControl` asserts the defect is actually PRESENT in the pre-state, at exactly the five
sites this promote clears, and that coverage fails there. A guard that only fires on an injected
defect proves nothing about whether it sees the real one.

`PeasAreProtected` is the reason this suite exists in the shape it does. Reflective mulch against
thrips is wrong for alliums and RIGHT for peas, where thrips act as virus vectors on a young crop
and the method's own best_use describes exactly that case. Blanketing one reason across crops is a
defect this repo has paid for; the promote must be provably incapable of it.
"""
import hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_drop_allium_reflective_mulch as P  # noqa: E402

POST_SHA = "3e408f5886f3f78dec3583bd0faa6c1f7c3b481c20039941112719193dc419ee"
PRE_DEFECT_SITES = sorted([
    "garlic/onion-thrips/management_seasoned", "garlic/onion-thrips/rung",
    "onion/None/management_seasoned", "shallot/None/management_seasoned",
])


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _applied():
    d = _pre()
    P.apply_to(d)
    return d


def _expect(case, sentence, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(sentence, str(cm.exception))


class _Patch:
    def __init__(self, n, v):
        self.n, self.v = n, v

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)

    def __exit__(self, *e):
        setattr(P, self.n, self.old)
        return False


class CleanRun(unittest.TestCase):
    def test_pre_state_is_the_pinned_shape(self):
        self.assertEqual(hashlib.sha256(P.serialize(_pre())).hexdigest(), P.BASE_SHA)

    def test_apply_produces_the_pinned_post_sha(self):
        self.assertEqual(hashlib.sha256(P.serialize(_applied())).hexdigest(), POST_SHA)

    def test_rung_counts_are_pinned(self):
        self.assertEqual(P.rung_count(_pre()), P.EXPECTED_RUNGS_BEFORE)
        self.assertEqual(P.rung_count(_applied()), P.EXPECTED_RUNGS_AFTER)
        self.assertEqual(P.EXPECTED_RUNGS_BEFORE - P.EXPECTED_RUNGS_AFTER, 1)

    def test_problem_count_is_unchanged(self):
        def n(d):
            return sum(len(P.problems(c)) for c in d["crops"])
        self.assertEqual(n(_pre()), n(_applied()))

    def test_the_replacement_reads_correctly(self):
        self.assertNotIn("reflective", P.AFTER.lower())
        self.assertIn("hose off light infestations, and rotate away from alliums", P.AFTER)
        self.assertEqual(len(P.BEFORE) - len(P.AFTER), len(", use reflective mulch"))


class PositiveControl(unittest.TestCase):
    """Does the guard see the REAL defect?"""

    def test_the_defect_is_present_in_the_pre_state_at_exactly_five_sites(self):
        d = _pre()
        found = []
        for slug in P.ALLIUM_THRIPS:
            c = P.by_slug(d).get(slug)
            if c is None:
                continue
            for p in P.problems(c):
                if "thrip" not in ((p.get("id") or "") + (p.get("name") or "")).lower():
                    continue
                for k, v in p.items():
                    if isinstance(v, str) and P.REFLECTIVE.search(v):
                        found.append("%s/%s/%s" % (slug, p.get("id"), k))
                for r in p.get("control_ladder") or []:
                    if r.get("method") == "reflective_mulch":
                        found.append("%s/%s/rung" % (slug, p.get("id")))
        self.assertEqual(sorted(found), PRE_DEFECT_SITES)

    def test_coverage_fails_on_the_untouched_pre_state(self):
        _expect(self, "allium thrips advice still names reflective mulch",
                lambda: P.check_coverage(_pre()))

    def test_coverage_passes_after_the_promote(self):
        self.assertEqual(P.check_coverage(_applied()), len(P.ALLIUM_THRIPS))

    def test_the_PROSE_branch_alone_is_enough_to_fail_coverage(self):
        """Driven on the APPLIED state, one branch at a time. Every earlier coverage test ran
        against the pre-state, where prose AND a rung are both present -- either branch alone
        raises, so none of them could tell the two apart and both mutations survived."""
        d = _applied()
        P.find_problem(d, "onion", "Onion thrips")["management_seasoned"] = (
            "Keep plants watered and use reflective mulch.")
        _expect(self, "onion/None/management_seasoned", lambda: P.check_coverage(d))

    def test_the_RUNG_branch_alone_is_enough_to_fail_coverage(self):
        d = _applied()
        P.find_problem(d, "garlic", "Onion thrips")["control_ladder"].append(
            {"method": "reflective_mulch", "note_beginner": "x", "note_seasoned": "y"})
        _expect(self, "garlic/onion-thrips/rung", lambda: P.check_coverage(d))

    def test_the_denominator_covers_alliums_this_promote_never_edits(self):
        """leek and spring-onion are in ALLIUM_THRIPS but not in PROSE_EDITS. If the denominator
        shrinks to the edited crops, a regression on either goes unseen."""
        d = _applied()
        P.find_problem(d, "leek", "Onion thrips")["management_seasoned"] = (
            "Lay reflective mulch against thrips.")
        _expect(self, "leek/None/management_seasoned", lambda: P.check_coverage(d))

    def test_leek_and_spring_onion_never_carried_it(self):
        """They are in the denominator so a later regression on them is caught, but they are not
        edited. Asserting that keeps the coverage number honest."""
        d = _pre()
        for slug in ("leek", "spring-onion"):
            for p in P.problems(P.by_slug(d)[slug]):
                for k, v in p.items():
                    if isinstance(v, str):
                        self.assertIsNone(P.REFLECTIVE.search(v), "%s/%s" % (slug, k))


class PeasAreProtected(unittest.TestCase):
    def test_the_peas_keep_all_four_rungs(self):
        d = _applied()
        n = sum(1 for c in d["crops"] if c["slug"] in P.PROTECTED
                for p in P.problems(c) for r in p.get("control_ladder") or []
                if r.get("method") == "reflective_mulch")
        self.assertEqual(n, P.EXPECTED_PROTECTED_RUNGS)
        self.assertEqual(n, 4)

    def test_the_peas_prose_is_byte_identical_after(self):
        a, b = _pre(), _applied()
        for slug in P.PROTECTED:
            self.assertEqual(json.dumps(P.by_slug(a)[slug], sort_keys=True),
                             json.dumps(P.by_slug(b)[slug], sort_keys=True), slug)

    def test_a_pea_change_is_refused(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        for p in P.problems(P.by_slug(d)["snow-peas"]):
            if p.get("id") == "thrips":
                p["control_ladder"] = [r for r in p["control_ladder"]
                                       if r["method"] != "reflective_mulch"]
        _expect(self, "a protected pea entry changed",
                lambda: P.check_protected_untouched(pre, d))

    def test_the_protected_count_is_pinned_not_derived(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        with _Patch("EXPECTED_PROTECTED_RUNGS", 3):
            _expect(self, "the peas hold 4 reflective_mulch rungs, expected 3",
                    lambda: P.check_protected_untouched(pre, d))


class Pins(unittest.TestCase):
    def test_stale_prose_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "onion", "Onion thrips")["management_seasoned"] = "moved on"
        _expect(self, "does not match its pinned text; the record moved", lambda: P.check_pins(d))

    def test_a_non_allium_target_refuses(self):
        d = _pre()
        with _Patch("PROSE_EDITS", P.PROSE_EDITS + (("snow-peas", "Thrips", "prevention_seasoned"),)), \
                _Patch("EXPECTED_PROSE_EDITS", 4):
            _expect(self, "snow-peas is not an allium thrips crop", lambda: P.check_pins(d))

    def test_edit_count_is_asserted(self):
        d = _pre()
        with _Patch("PROSE_EDITS", P.PROSE_EDITS[:2]):
            _expect(self, "PROSE_EDITS holds 2 entries, expected 3", lambda: P.check_pins(d))

    def test_a_replacement_that_still_names_reflective_mulch_refuses(self):
        d = _pre()
        with _Patch("AFTER", P.BEFORE.replace("use reflective mulch", "use a reflective mulch")):
            _expect(self, "the replacement still names reflective mulch", lambda: P.check_pins(d))

    def test_wrong_ladder_length_refuses(self):
        d = _pre()
        P.find_problem(d, "garlic", "Onion thrips")["control_ladder"].append(
            {"method": "handpick", "note_beginner": "x", "note_seasoned": "y"})
        _expect(self, "ladder holds 4 rungs, expected 3", lambda: P.check_pins(d))

    def test_wrong_rung_position_refuses(self):
        d = _pre()
        lad = P.find_problem(d, "garlic", "Onion thrips")["control_ladder"]
        lad[0], lad[1] = lad[1], lad[0]
        _expect(self, "rung 1 is 'crop_rotation', expected 'reflective_mulch'",
                lambda: P.check_pins(d))

    def test_a_duplicate_method_makes_the_removal_ambiguous(self):
        d = _pre()
        lad = P.find_problem(d, "garlic", "Onion thrips")["control_ladder"]
        lad.append(dict(lad[1]))
        with _Patch("RUNG_REMOVAL", ("garlic", "Onion thrips", "reflective_mulch", 1, 4)):
            _expect(self, "carries 'reflective_mulch' more than once; the removal is ambiguous",
                    lambda: P.check_pins(d))

    def test_an_ambiguous_problem_name_refuses(self):
        d = _pre()
        P.by_slug(d)["onion"]["pests"].append({"name": "Onion thrips"})
        _expect(self, "has 2 problems named 'Onion thrips', expected exactly 1",
                lambda: P.check_pins(d))

    def test_pinning_by_name_is_required_because_two_crops_have_no_id(self):
        """onion and shallot carry no `id` on their problems yet; an id-keyed lookup would find
        nothing on two of the three crops this promote edits."""
        d = _pre()
        for slug in ("onion", "shallot"):
            self.assertIsNone(P.find_problem(d, slug, "Onion thrips").get("id"), slug)
        self.assertEqual(P.find_problem(d, "garlic", "Onion thrips").get("id"), "onion-thrips")


class BlastRadius(unittest.TestCase):
    def test_clean_apply_changes_exactly_three_leaves(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        self.assertEqual(P.verify_post(pre, d), P.EXPECTED_PROSE_EDITS)

    def test_the_snapshot_is_content_keyed_so_a_removal_does_not_shift_the_tail(self):
        """A path-keyed snapshot reports every rung after the removed one as dropped-and-re-added,
        drowning the one real removal. Keying rungs by METHOD makes the diff exact."""
        pre, post = P.snapshot(_pre()), P.snapshot(_applied())
        dropped = set(pre) - set(post)
        self.assertEqual(len(dropped), 3)
        self.assertEqual({k[3] for k in dropped}, {"reflective_mulch"})
        self.assertEqual(set(post) - set(pre), set())

    def test_an_added_key_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "garlic", "Onion thrips")["control_ladder"].append(
            {"method": "handpick", "note_beginner": "x", "note_seasoned": "y"})
        _expect(self, "keys added", lambda: P.verify_post(pre, d))

    def test_removing_a_second_rung_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "garlic", "Onion thrips")["control_ladder"].pop()
        _expect(self, "expected exactly the reflective_mulch rung's leaves",
                lambda: P.verify_post(pre, d))

    def test_an_extra_changed_leaf_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.by_slug(d)["beet"]["name"] = "Beetroot"
        _expect(self, "4 leaves changed, expected 3", lambda: P.verify_post(pre, d))

    def test_a_change_on_the_wrong_crop_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "onion", "Onion thrips")["management_seasoned"] = P.BEFORE
        P.by_slug(d)["beet"]["name"] = "Beetroot"
        _expect(self, "changed", lambda: P.verify_post(pre, d))

    def test_the_post_rung_total_is_pinned(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        with _Patch("EXPECTED_RUNGS_AFTER", 3242):
            _expect(self, "3243 rungs after, expected 3242", lambda: P.verify_post(pre, d))


class CatalogUntouched(unittest.TestCase):
    def setUp(self):
        d = _pre()
        self.cm, self.sc = P.serialize(d["control_methods"]), P.serialize(d["source_catalog"])

    def test_control_methods_change_refuses(self):
        d = _pre()
        d["control_methods"]["reflective_mulch"]["applies_to"] = ["viral"]
        _expect(self, "control_methods changed; this promote retires no method",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_source_catalog_change_refuses(self):
        d = _pre()
        d["source_catalog"][sorted(d["source_catalog"])[0]]["name"] = "x"
        _expect(self, "source_catalog changed",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_the_method_itself_survives_because_the_peas_still_use_it(self):
        d = _applied()
        self.assertIn("reflective_mulch", d["control_methods"])
        P.check_catalog_untouched(self.cm, self.sc, d)


class MainWiringIsDriven(unittest.TestCase):
    def test_apply_to_routes_through_check_pins(self):
        import inspect
        self.assertIn("check_pins(", inspect.getsource(P.apply_to))

    def test_main_runs_every_post_check(self):
        import inspect
        src = inspect.getsource(P.main)
        for frag in ("verify_post(pre, data)", "check_catalog_untouched(",
                     "check_protected_untouched(pre, data)", "check_coverage(data)",
                     "if sha != expect:", "if rung_count(data) != EXPECTED_RUNGS_BEFORE:"):
            self.assertIn(frag, src)

    def test_end_to_end_through_main(self):
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(promote_fixture.pre_state(P.BASE_SHA))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, path], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("post  SHA           : " + POST_SHA, r.stdout)
            self.assertIn("rungs               : 3244 -> 3243", r.stdout)
            self.assertIn("peas untouched      : 4", r.stdout)
        finally:
            os.unlink(path)

    def test_a_wrong_base_sha_is_refused(self):
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(P.serialize({"crops": [], "control_methods": {}, "source_catalog": {}}))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, path], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("REFUSED: base SHA", r.stdout + r.stderr)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main(verbosity=1)
