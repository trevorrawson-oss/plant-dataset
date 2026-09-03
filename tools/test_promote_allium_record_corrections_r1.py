#!/usr/bin/env python3
"""Guard suite for tools/promote_allium_record_corrections_r1.py. Base 3e408f58.

REPLAY-PINNED. Evidence the guards are live: `MainWiringIsDriven` plus
tools/mutate_allium_record_corrections_suite.py.

`PositiveControl` asserts each retired claim is actually PRESENT in the pre-state and that the
guard fails there. `VarietyCheckRecognisesNegation` exists because the first version of that guard
pattern-matched "tolerant variety" and refused this promote's OWN replacement text, which says
there is NO resistant variety -- the opposite claim. A guard that rejects correct input is as much
a defect as one that accepts bad input, and no mutation of its branches would have found it.
"""
import hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_allium_record_corrections_r1 as P  # noqa: E402

POST_SHA = "b89763b76e03584a270a569eb1ad0d5359a6a00d8ad217eb9493cf9eaa795a8f"


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

    def test_counts_are_pinned(self):
        self.assertEqual((len(P.PROSE), len(P.SEVERITY), len(P.SOURCES)),
                         (P.EXPECTED_PROSE, P.EXPECTED_SEVERITY, P.EXPECTED_SOURCE_SETS))
        self.assertEqual(len(P.TARGETS), 3)

    def test_the_roster_shape_is_unchanged(self):
        a, b = _pre(), _applied()
        self.assertEqual(len(a["crops"]), len(b["crops"]))
        self.assertEqual(sum(len(P.problems(c)) for c in a["crops"]),
                         sum(len(P.problems(c)) for c in b["crops"]))
        self.assertEqual(sum(len(p.get("control_ladder") or []) for c in b["crops"]
                             for p in P.problems(c)), 3243)


class PositiveControl(unittest.TestCase):
    def test_every_retired_claim_is_present_in_the_pre_state(self):
        d = _pre()
        for (slug, name), still_present, label in P.RETIRED:
            p = P.find_problem(d, slug, name)
            self.assertTrue(any(isinstance(v, str) and still_present(v) for v in p.values()),
                            "%s/%s: %s was not present to begin with" % (slug, name, label))

    def test_the_guard_fails_on_the_untouched_pre_state(self):
        _expect(self, "still carries", lambda: P.check_retired_claims(_pre()))

    def test_the_guard_passes_after_the_promote(self):
        self.assertEqual(P.check_retired_claims(_applied()), len(P.RETIRED))

    def test_leek_rust_still_cites_rhs_before_the_promote(self):
        self.assertIn("rhs", P.find_problem(_pre(), "leek", "Leek rust")["sources"])
        _expect(self, "leek/Leek rust still cites", lambda: P.check_sources_retired(_pre()))

    def test_leek_rust_cites_neither_stale_source_after(self):
        P.check_sources_retired(_applied())
        p = P.find_problem(_applied(), "leek", "Leek rust")
        self.assertEqual(p["sources"], ["uc_ipm", "osu_ext"])
        self.assertEqual(list(p["anchoring_urls"]), ["uc_ipm", "osu_ext"])


class VarietyCheckRecognisesNegation(unittest.TestCase):
    """The measurement, not the branch."""

    def test_a_recommendation_is_caught(self):
        for t in ("Pick tolerant varieties if this is a regular problem for you.",
                  "choose tolerant varieties where downy mildew is a recurring problem",
                  "Pick rust-tolerant varieties if you can.",
                  "choose more rust-tolerant varieties where available",
                  "Plant resistant varieties when possible."):
            self.assertTrue(P.recommends_a_variety(t), t)

    def test_saying_there_is_NONE_is_not_a_recommendation(self):
        for t in ("There is no resistant variety to fall back on.",
                  "No resistant variety is available, so every lever here is a "
                  "growing-conditions one.",
                  "There are no resistant varieties.",
                  "no rust-tolerant variety is offered to home gardeners"):
            self.assertFalse(P.recommends_a_variety(t), t)

    def test_the_promotes_own_replacements_pass_their_own_guard(self):
        for (_s, _n, _f), (_before, after) in P.PROSE.items():
            self.assertFalse(P.recommends_a_variety(after), after[:60])


class Pins(unittest.TestCase):
    def test_stale_prose_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "leek", "Leek rust")["cause_beginner"] = "moved on"
        _expect(self, "does not match its pinned text; the record moved", lambda: P.check_pins(d))

    def test_a_target_outside_the_declared_set_refuses(self):
        d = _pre()
        pr = dict(P.PROSE)
        pr[("garlic", "Onion thrips", "cause_beginner")] = ("x", "y")
        with _Patch("PROSE", pr), _Patch("EXPECTED_PROSE", len(pr)):
            _expect(self, "garlic/Onion thrips is not a declared target", lambda: P.check_pins(d))

    def test_table_sizes_are_asserted(self):
        d = _pre()
        with _Patch("EXPECTED_PROSE", 8):
            _expect(self, "edit tables hold 9/1/3, expected 8/1/3", lambda: P.check_pins(d))

    def test_an_identical_replacement_refuses(self):
        d = _pre()
        k = ("leek", "Leek rust", "cause_beginner")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][0])
        with _Patch("PROSE", pr):
            _expect(self, "replacement is identical", lambda: P.check_pins(d))

    def test_hygiene_on_the_replacement_refuses(self):
        d = _pre()
        k = ("leek", "Leek rust", "cause_beginner")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][1] + " It completely stops the rust.")
        with _Patch("PROSE", pr):
            _expect(self, "absolute:completely", lambda: P.check_pins(d))

    def test_a_british_replacement_refuses(self):
        d = _pre()
        k = ("leek", "Leek rust", "cause_beginner")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][1] + " Worst in autumn.")
        with _Patch("PROSE", pr):
            _expect(self, "british:", lambda: P.check_pins(d))

    def test_a_stale_severity_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "leek", "Leek rust")["severity"] = "medium"
        _expect(self, "severity is 'medium', pinned 'high'", lambda: P.check_pins(d))

    def test_an_unknown_new_severity_refuses(self):
        d = _pre()
        with _Patch("SEVERITY", {("leek", "Leek rust"): ("high", "trivial")}):
            _expect(self, "new severity 'trivial' is not a known value", lambda: P.check_pins(d))

    def test_a_stale_source_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "shallot", "White rot")["sources"] = ["umd_ext"]
        _expect(self, "sources are ['umd_ext'], pinned", lambda: P.check_pins(d))

    def test_citing_an_id_not_in_the_catalog_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("shallot", "White rot")] = (["umass_ext", "umd_ext"],
                                         ["umass_ext", "umd_ext", "invented_ext"],
                                         {"invented_ext": "https://example.edu/x"})
        with _Patch("SOURCES", src):
            _expect(self, "cites 'invented_ext', which is not in source_catalog",
                    lambda: P.check_pins(d))

    def test_an_anchor_outside_the_new_source_list_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("shallot", "White rot")] = (["umass_ext", "umd_ext"], ["umass_ext", "umd_ext"],
                                         {"uc_ipm": "https://ipm.ucanr.edu/x"})
        with _Patch("SOURCES", src):
            _expect(self, "anchors 'uc_ipm' which is not in its new source list",
                    lambda: P.check_pins(d))

    def test_an_ambiguous_problem_name_refuses(self):
        d = _pre()
        P.by_slug(d)["leek"]["diseases"].append({"name": "Leek rust"})
        _expect(self, "has 2 problems named 'Leek rust', expected exactly 1",
                lambda: P.check_pins(d))


class RetiredClaimsPerBranch(unittest.TestCase):
    """One driver per retired claim, on the APPLIED state, so each isolates its own branch."""

    def _reintroduce(self, slug, name, field, text):
        d = _applied()
        P.find_problem(d, slug, name)[field] = text
        return d

    def test_a_variety_recommendation_coming_back_on_shallot(self):
        d = self._reintroduce("shallot", "Downy mildew", "management_beginner",
                              "Pick tolerant varieties if you can.")
        _expect(self, "shallot/Downy mildew/management_beginner still carries",
                lambda: P.check_retired_claims(d))

    def test_the_fabricated_figure_coming_back(self):
        d = self._reintroduce("shallot", "White rot", "cause_beginner",
                              "Sclerotia last 20 to 30 years in the soil.")
        _expect(self, "still carries the fabricated 20-to-30-year figure",
                lambda: P.check_retired_claims(d))

    def test_the_british_verb_coming_back(self):
        d = self._reintroduce("leek", "Leek rust", "management_beginner",
                              "Pull off and bin the worst leaves.")
        _expect(self, "still carries the British verb 'bin'", lambda: P.check_retired_claims(d))

    def test_the_variety_recommendation_coming_back_on_leek(self):
        d = self._reintroduce("leek", "Leek rust", "management_seasoned",
                              "Choose more rust-tolerant varieties where available.")
        _expect(self, "still carries the variety recommendation RHS never made",
                lambda: P.check_retired_claims(d))

    def test_the_uk_seasonal_framing_coming_back(self):
        d = self._reintroduce("leek", "Leek rust", "identification_beginner",
                              "Orange pustules from mid-summer into late autumn.")
        _expect(self, "still carries the UK seasonal framing", lambda: P.check_retired_claims(d))

    def test_a_claim_surviving_in_a_SIBLING_field_is_caught(self):
        """The whole point of scanning the problem rather than the edited field."""
        d = self._reintroduce("leek", "Leek rust", "cause_seasoned",
                              "Worse in humid weather from mid-summer into late autumn.")
        _expect(self, "cause_seasoned still carries", lambda: P.check_retired_claims(d))

    def test_a_stale_source_surviving_only_in_anchoring_urls_is_caught(self):
        d = _applied()
        P.find_problem(d, "leek", "Leek rust")["anchoring_urls"]["rhs"] = {
            "url": "https://www.rhs.org.uk/disease/leek-rust", "verified": "2026-06-29"}
        _expect(self, "leek/Leek rust still cites ['rhs']",
                lambda: P.check_sources_retired(d))


class BlastRadius(unittest.TestCase):
    def test_clean_apply_changes_the_expected_leaves(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        self.assertEqual(P.verify_post(pre, d), 12)

    def test_a_key_added_outside_sources_or_anchors_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "leek", "Leek rust")["note"] = "x"
        _expect(self, "added or dropped outside sources/anchoring_urls",
                lambda: P.verify_post(pre, d))

    def test_a_source_added_on_a_NON_target_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "garlic", "Onion thrips")["sources"].append("uc_ipm")
        _expect(self, "added or dropped outside the declared targets",
                lambda: P.verify_post(pre, d))

    def test_an_extra_prose_change_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "leek", "Leek rust")["identification_beginner"] += " Extra."
        _expect(self, "did not receive its replacement", lambda: P.verify_post(pre, d))

    def test_a_change_on_a_bystander_crop_refuses(self):
        """Driven on a NON-prose field. A bystander change in one of the nine pinned prose fields
        trips the prose-count check first and never reaches this branch -- the guard-tests-pass-
        because-an-earlier-check-fires shape. Both paths are covered: the count catches a prose
        change, this catches everything else."""
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "garlic", "Onion thrips")["severity"] = "low"
        _expect(self, "leaves changed outside the declared targets", lambda: P.verify_post(pre, d))

    def test_a_bystander_change_in_a_PROSE_field_is_caught_by_the_count(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "garlic", "Onion thrips")["cause_beginner"] = "changed"
        _expect(self, "10 prose leaves changed, expected 9", lambda: P.verify_post(pre, d))

    def test_severity_not_applied_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "leek", "Leek rust")["severity"] = "high"
        _expect(self, "severity was not set to 'low'", lambda: P.verify_post(pre, d))

    def test_the_source_list_ORDER_is_pinned_not_just_the_set(self):
        """Nothing drove this branch until the harness said so: apply_to always writes the right
        list, so only a post-apply perturbation reaches it. Order is load-bearing here -- it is
        part of the serialized output and therefore part of the pinned SHA."""
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        p = P.find_problem(d, "leek", "Leek rust")
        p["sources"] = list(reversed(p["sources"]))
        _expect(self, "sources are ['osu_ext', 'uc_ipm'], expected ['uc_ipm', 'osu_ext']",
                lambda: P.verify_post(pre, d))

    def test_a_source_swapped_for_a_different_id_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        p = P.find_problem(d, "shallot", "White rot")
        p["sources"] = ["umass_ext", "umd_ext", "usu_ext"]
        _expect(self, "sources are ['umass_ext', 'umd_ext', 'usu_ext'], expected",
                lambda: P.verify_post(pre, d))

    def test_anchor_keys_must_match_the_source_list(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "leek", "Leek rust")["anchoring_urls"].pop("osu_ext")
        _expect(self, "anchoring_urls keys", lambda: P.verify_post(pre, d))

    def test_the_prose_change_count_is_pinned(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        k = ("shallot", "White rot", "cause_seasoned")
        P.find_problem(d, *k[:2])[k[2]] = P.PROSE[k][0]
        _expect(self, "8 prose leaves changed, expected 9", lambda: P.verify_post(pre, d))


class CatalogUntouched(unittest.TestCase):
    def setUp(self):
        d = _pre()
        self.cm, self.sc = P.serialize(d["control_methods"]), P.serialize(d["source_catalog"])

    def test_control_methods_change_refuses(self):
        d = _pre()
        d["control_methods"]["crop_rotation"]["tier"] = "physical"
        _expect(self, "control_methods changed; this promote mints nothing",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_source_catalog_change_refuses(self):
        d = _pre()
        d["source_catalog"]["osu_ext"]["name"] = "x"
        _expect(self, "source_catalog changed; every id cited here already exists",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_every_id_this_promote_cites_already_exists(self):
        sc = _pre()["source_catalog"]
        for (_s, _n), (_b, after, _a) in P.SOURCES.items():
            for sid in after:
                self.assertIn(sid, sc)

    def test_the_real_promote_touches_neither(self):
        P.check_catalog_untouched(self.cm, self.sc, _applied())


class MainWiringIsDriven(unittest.TestCase):
    def test_apply_to_routes_through_check_pins(self):
        import inspect
        self.assertIn("check_pins(", inspect.getsource(P.apply_to))

    def test_main_runs_every_post_check(self):
        import inspect
        src = inspect.getsource(P.main)
        for frag in ("verify_post(pre, data)", "check_catalog_untouched(",
                     "check_retired_claims(data)", "check_sources_retired(data)",
                     "if sha != expect:"):
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
            self.assertIn("retired claims gone : 5/5", r.stdout)
            self.assertIn("leek rust severity  : high -> low", r.stdout)
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
