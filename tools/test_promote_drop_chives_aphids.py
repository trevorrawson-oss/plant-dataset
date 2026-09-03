#!/usr/bin/env python3
"""Guard suite for tools/promote_drop_chives_aphids.py. Base b89763b7.

REPLAY-PINNED. Evidence the guards are live: `MainWiringIsDriven` plus
tools/mutate_drop_chives_aphids_suite.py.

Two classes of test carry most of the weight here, because this promote DELETES consumer content:

`NothingIsLost` asserts the entry's one valuable claim -- that chives repel aphids from neighbours
-- survives the removal, in six places under `companions`, hedged better there than in the pest
entry. Deleting content without proving what it carried is recorded elsewhere is how a cleanup
becomes a regression.

`TheFindingIsAmendedNotInvalidated` asserts the append-only convention. chives' open finding
enumerates the modeled pest set INCLUDING aphids and says it was "flagged for the source-truth
sample". That sample has now run, so the finding's prose goes stale the moment the entry leaves.
The promote appends a dated CORRECTION and the original wording must survive byte-for-byte as an
exact prefix.
"""
import hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_drop_chives_aphids as P  # noqa: E402

POST_SHA = "80519a28548586aedd9754a664f1618b722fb55976d8eb6c3314891ddc5c328f"


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
        self.assertEqual(P.problem_count(_pre()), P.EXPECTED_PROBLEMS_BEFORE)
        self.assertEqual(P.problem_count(_applied()), P.EXPECTED_PROBLEMS_AFTER)
        self.assertEqual(P.EXPECTED_PROBLEMS_BEFORE - P.EXPECTED_PROBLEMS_AFTER, 1)

    def test_only_chives_loses_a_problem(self):
        a, b = _pre(), _applied()
        for slug in {c["slug"] for c in a["crops"]}:
            na = len(P.problems(P.by_slug(a)[slug]))
            nb = len(P.problems(P.by_slug(b)[slug]))
            self.assertEqual(na - nb, 1 if slug == "chives" else 0, slug)

    def test_the_other_seven_chives_entries_survive_untouched(self):
        a, b = _pre(), _applied()
        before = {p["name"]: json.dumps(p, sort_keys=True)
                  for p in P.problems(P.by_slug(a)["chives"]) if p["name"] != "Aphids"}
        after = {p["name"]: json.dumps(p, sort_keys=True)
                 for p in P.problems(P.by_slug(b)["chives"])}
        self.assertEqual(before, after)
        self.assertEqual(len(after), 7)


class PositiveControl(unittest.TestCase):
    def test_the_entry_is_present_in_the_pre_state_where_the_promote_expects_it(self):
        d = _pre()
        lst = P.by_slug(d)["chives"][P.TARGET_FAMILY]
        self.assertEqual(len(lst), P.EXPECTED_PESTS_BEFORE)
        self.assertEqual(lst[P.TARGET_INDEX]["name"], P.TARGET_NAME)

    def test_the_finding_enumerates_the_entry_being_removed(self):
        """If the finding stopped naming aphids, the correction this promote appends would be
        answering a claim the record no longer makes."""
        self.assertIn("aphids", (P.finding(_pre()).get("summary") or "").lower())

    def test_the_entry_is_gone_afterward(self):
        self.assertFalse(any(p.get("name") == P.TARGET_NAME
                             for p in P.problems(P.by_slug(_applied())["chives"])))


class NothingIsLost(unittest.TestCase):
    def test_the_companion_claim_survives_in_six_places(self):
        self.assertEqual(P.check_companion_claim_survives(_applied()), 6)

    def test_the_guard_refuses_if_the_companion_claim_were_lost(self):
        d = _applied()
        P.by_slug(d)["chives"]["companions"] = {}
        _expect(self, "the aphid-repelling companion claim survives in only 0 places",
                lambda: P.check_companion_claim_survives(d))

    def test_the_floor_is_pinned_not_derived(self):
        d = _applied()
        with _Patch("MIN_COMPANION_SITES", 99):
            _expect(self, "expected at least 99", lambda: P.check_companion_claim_survives(d))

    def test_the_surviving_wording_is_the_better_hedged_one(self):
        """The pest entry stated the repelling claim as fact; the companions text calls it
        tradition. Losing the unhedged version is an improvement, not a loss."""
        sites = P.companion_sites(_applied())
        blob = " ".join(json.dumps(P.by_slug(_applied())["chives"]["companions"], ensure_ascii=False)
                        for _ in [0])
        self.assertGreaterEqual(len(sites), 5)
        self.assertIn("not a measured trial", blob)


class NothingReferencesIt(unittest.TestCase):
    def test_a_problem_id_on_the_target_refuses(self):
        """A problem id is a JOIN KEY -- `varieties[].resistance` and `ladder_delta` point at one."""
        d = _pre()
        P.by_slug(d)["chives"][P.TARGET_FAMILY][P.TARGET_INDEX]["id"] = "aphids"
        _expect(self, "the target carries id 'aphids'", lambda: P.check_nothing_references_it(d))

    def test_a_shipped_ladder_on_the_target_refuses(self):
        d = _pre()
        P.by_slug(d)["chives"][P.TARGET_FAMILY][P.TARGET_INDEX]["control_ladder"] = [
            {"method": "water_spray", "note_beginner": "x", "note_seasoned": "y"}]
        _expect(self, "carries a shipped control_ladder", lambda: P.check_nothing_references_it(d))

    def test_a_resistance_key_anywhere_on_the_crop_refuses(self):
        d = _pre()
        P.by_slug(d)["chives"]["varieties"]["resistance"] = {}
        _expect(self, 'carries "resistance" somewhere', lambda: P.check_nothing_references_it(d))

    def test_the_real_crop_carries_no_join_keys(self):
        P.check_nothing_references_it(_pre())


class TheFindingIsAmendedNotInvalidated(unittest.TestCase):
    def test_the_original_wording_survives_as_an_exact_prefix(self):
        original = P.finding(_pre())["summary"]
        self.assertTrue(P.finding(_applied())["summary"].startswith(original))

    def test_the_appended_text_is_a_dated_correction(self):
        original = P.finding(_pre())["summary"]
        appended = P.finding(_applied())["summary"][len(original):]
        self.assertIn("[CORRECTION 2026-09-03:", appended)
        self.assertIn("APHIDS entry has been REMOVED", appended)

    def test_the_correction_records_what_is_no_longer_true_and_why(self):
        appended = P.CORRECTION
        for frag in ("no aphid page at all", "Wisconsin", "companions", "Neotoxoptera formosana"):
            self.assertIn(frag, appended)

    def test_rewriting_the_original_refuses(self):
        original = P.finding(_pre())["summary"]
        d = _applied()
        P.finding(d)["summary"] = "Rewritten from scratch." + P.CORRECTION
        _expect(self, "original wording was not preserved byte-for-byte",
                lambda: P.check_finding_amended(d, original))

    def test_leaving_the_finding_untouched_refuses(self):
        original = P.finding(_pre())["summary"]
        d = _applied()
        P.finding(d)["summary"] = original
        _expect(self, "the finding was not amended", lambda: P.check_finding_amended(d, original))

    def test_appending_something_that_is_not_a_correction_refuses(self):
        original = P.finding(_pre())["summary"]
        d = _applied()
        P.finding(d)["summary"] = original + " Also some other note."
        _expect(self, "appended text is not a dated CORRECTION",
                lambda: P.check_finding_amended(d, original))

    def test_a_missing_finding_refuses(self):
        d = _pre()
        vs = P.by_slug(d)["chives"]["verification_status"]
        vs["open_findings"] = [f for f in vs["open_findings"] if f.get("id") != P.FINDING_ID]
        _expect(self, "has no open finding", lambda: P.finding(d))


class TargetPins(unittest.TestCase):
    def test_a_wrong_pest_count_refuses(self):
        d = _pre()
        P.by_slug(d)["chives"]["pests"].append({"name": "Slugs"})
        _expect(self, "chives has 5 pests, expected 4", lambda: P.check_target(d))

    def test_a_wrong_index_refuses(self):
        d = _pre()
        lst = P.by_slug(d)["chives"]["pests"]
        lst[0], lst[3] = lst[3], lst[0]
        _expect(self, "chives/pests[3] is 'Onion thrips', expected 'Aphids'",
                lambda: P.check_target(d))

    def test_a_duplicate_name_makes_the_removal_ambiguous(self):
        d = _pre()
        P.by_slug(d)["chives"]["diseases"].append({"name": "Aphids"})
        _expect(self, "carries 'Aphids' more than once; the removal is ambiguous",
                lambda: P.check_target(d))

    def test_a_wrong_roster_problem_count_refuses(self):
        d = _pre()
        P.by_slug(d)["beet"]["pests"].append({"name": "Extra"})
        _expect(self, "roster holds 914 problems, expected 913", lambda: P.check_target(d))

    def test_a_missing_crop_refuses(self):
        d = _pre()
        d["crops"] = [c for c in d["crops"] if c["slug"] != "chives"]
        _expect(self, "crop chives is not on the roster", lambda: P.check_target(d))


class BlastRadius(unittest.TestCase):
    def test_clean_apply_drops_exactly_the_entry(self):
        d = _pre()
        pre = P.snapshot(d)
        original = P.finding(d)["summary"]
        P.apply_to(d)
        self.assertEqual(P.verify_post(pre, d, original), 12)

    def test_the_snapshot_keys_problems_by_NAME_so_the_tail_does_not_shift(self):
        pre, post = P.snapshot(_pre()), P.snapshot(_applied())
        dropped = set(pre) - set(post)
        self.assertEqual({k[:4] for k in dropped}, {("PROB", "chives", "pests", "Aphids")})
        self.assertEqual(set(post) - set(pre), set())

    def test_dropping_a_second_entry_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        original = P.finding(d)["summary"]
        P.apply_to(d)
        P.by_slug(d)["chives"]["diseases"].pop()
        _expect(self, "keys dropped outside the target entry",
                lambda: P.verify_post(pre, d, original))

    def test_an_added_key_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        original = P.finding(d)["summary"]
        P.apply_to(d)
        P.by_slug(d)["chives"]["pests"][0]["note"] = "x"
        _expect(self, "keys added", lambda: P.verify_post(pre, d, original))

    def test_a_change_outside_the_finding_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        original = P.finding(d)["summary"]
        P.apply_to(d)
        P.by_slug(d)["beet"]["name"] = "Beetroot"
        _expect(self, "a leaf changed outside the chives finding",
                lambda: P.verify_post(pre, d, original))

    def test_a_SECOND_finding_also_changing_refuses(self):
        """The only way to reach the changed-count check: every changed leaf is inside
        open_findings, so the per-key scope check passes, but two findings moved instead of one.
        Nothing drove this until the harness said so."""
        d = _pre()
        pre = P.snapshot(d)
        original = P.finding(d)["summary"]
        P.apply_to(d)
        others = [f for f in P.by_slug(d)["chives"]["verification_status"]["open_findings"]
                  if f.get("id") != P.FINDING_ID]
        others[0]["summary"] = (others[0].get("summary") or "") + " Edited too."
        _expect(self, "2 leaves changed, expected exactly the finding summary",
                lambda: P.verify_post(pre, d, original))

    def test_the_post_problem_count_is_pinned(self):
        d = _pre()
        pre = P.snapshot(d)
        original = P.finding(d)["summary"]
        P.apply_to(d)
        with _Patch("EXPECTED_PROBLEMS_AFTER", 911):
            _expect(self, "roster holds 912 problems after, expected 911",
                    lambda: P.verify_post(pre, d, original))


class CatalogUntouched(unittest.TestCase):
    def setUp(self):
        d = _pre()
        self.cm, self.sc = P.serialize(d["control_methods"]), P.serialize(d["source_catalog"])

    def test_control_methods_change_refuses(self):
        d = _pre()
        d["control_methods"]["crop_rotation"]["tier"] = "physical"
        _expect(self, "control_methods changed",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_source_catalog_change_refuses(self):
        d = _pre()
        d["source_catalog"]["uwi_hort"]["name"] = "x"
        _expect(self, "source_catalog changed; this promote retires no source id",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_the_orphaned_source_ids_are_deliberately_left_in_the_catalog(self):
        """uwi_hort and umn_ext were this entry's citations. Both are institution-level ids used by
        other crops, so the removal retires no catalog row."""
        d = _applied()
        for sid in ("uwi_hort", "umn_ext"):
            self.assertIn(sid, d["source_catalog"])
        P.check_catalog_untouched(self.cm, self.sc, d)


class MainWiringIsDriven(unittest.TestCase):
    def test_apply_to_routes_through_both_pre_checks(self):
        import inspect
        src = inspect.getsource(P.apply_to)
        self.assertIn("check_target(", src)
        self.assertIn("check_nothing_references_it(", src)

    def test_main_runs_every_post_check(self):
        import inspect
        src = inspect.getsource(P.main)
        for frag in ("verify_post(pre, data, original)", "check_catalog_untouched(",
                     "check_companion_claim_survives(data)", "if sha != expect:"):
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
            self.assertIn("roster problems     : 913 -> 912", r.stdout)
            self.assertIn("companion claim     : survives in 6 places", r.stdout)
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
