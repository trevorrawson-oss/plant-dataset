#!/usr/bin/env python3
"""Guard suite for promote_pla465_null_rulings -- PLA-465 promote 2 (the twelve nulls, recorded).
THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla465_null_rulings_suite.py."""
import copy, json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla465_null_rulings as P  # noqa: E402

BASE_SHA = "a7f234ce449c6d74b4f1be2398bb808cfe29bebf9a1f7cc51efdcaea56246c93"
ROSTER = 128
N_APPENDS = 12
N_CROPS = 12
N_ADDENDA = 1
CROPS = ("apricot", "blackberry", "cherry-sour", "cherry-sweet", "grapefruit", "lime", "mandarin-clementine",
         "orange-navel", "pear-asian", "pear-european", "plum", "raspberry")


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.spec = P.staged()

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg, f"guard fired with the wrong message.\n  wanted: {fragment!r}\n  got: {msg!r}")

    def plum_finding(self, data):
        return next(x for x in P.by_slug(data)["plum"]["verification_status"]["open_findings"] if x["id"] == self.spec["addendum"]["id"])


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(promote_fixture.pre_state(P.BASE_SHA)), BASE_SHA)

    def test_refuses_a_canonical_that_is_not_the_base(self):
        with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as f:
            f.write(b'{"crops":[]}')
        try:
            self.assertRefuses("this promote is pinned to", P.load_canonical, f.name)
        finally:
            os.remove(f.name)

    def test_fixture_is_the_full_roster(self):
        self.assertEqual(len(self.data["crops"]), ROSTER)

    def test_pins_are_the_literals(self):
        self.assertEqual((P.EXPECTED_APPENDS, P.EXPECTED_CROPS, P.EXPECTED_ADDENDA), (N_APPENDS, N_CROPS, N_ADDENDA))

    def test_the_spec_is_the_shape_measured(self):
        self.assertEqual(len(self.spec["appends"]), N_APPENDS)
        self.assertEqual(tuple(sorted({r["crop"] for r in self.spec["appends"]} | {self.spec["addendum"]["crop"]})), CROPS)
        self.assertEqual(self.spec["expected"], {"appends": N_APPENDS, "crops": N_CROPS, "addenda": N_ADDENDA})

    def test_base_carries_no_ruling_and_the_addendum_target_is_original(self):
        idx = P.by_slug(self.data)
        for r in self.spec["appends"]:
            self.assertFalse(any(x.get("id") == r["entry"]["id"] for x in idx[r["crop"]]["verification_status"]["open_findings"]), r["entry"]["id"])
        self.assertEqual(self.plum_finding(self.data)["summary"], self.spec["addendum"]["original_summary"])
        for c in CROPS:
            self.assertTrue(all(idx[c].get(k) is None for k in P.PDG.FIELDS), c)


class SpecShape(Base):
    def test_refuses_a_spec_on_another_base(self):
        s = self.fresh_spec(); s["base_sha"] = "0" * 64
        self.assertRefuses("not the pinned base", P.check_spec_shape, s)

    def test_refuses_an_appends_count_drift(self):
        s = self.fresh_spec(); s["appends"].pop()
        self.assertRefuses("appends, pinned", P.check_spec_shape, s)

    def test_refuses_a_record_with_the_wrong_keys(self):
        s = self.fresh_spec(); del s["appends"][0]["entry"]["resolution_note"]
        self.assertRefuses("has keys", P.check_spec_shape, s)

    def test_refuses_a_duplicated_id(self):
        s = self.fresh_spec(); s["appends"][1]["entry"]["id"] = s["appends"][0]["entry"]["id"]
        self.assertRefuses("appears twice", P.check_spec_shape, s)

    def test_refuses_a_blocking_record(self):
        s = self.fresh_spec(); s["appends"][0]["entry"]["blocks_launch"] = True
        self.assertRefuses("must be non-blocking", P.check_spec_shape, s)

    def test_refuses_a_status_outside_the_vocabulary(self):
        s = self.fresh_spec(); s["appends"][0]["entry"]["status"] = "open"
        self.assertRefuses("not in", P.check_spec_shape, s)

    def test_refuses_deferred_without_a_route_and_accepted_with_one(self):
        s = self.fresh_spec(); r = next(x for x in s["appends"] if x["entry"]["status"] == "deferred"); r["entry"]["deferred_to"] = None
        self.assertRefuses("deferred_to must be set iff", P.check_spec_shape, s)
        s = self.fresh_spec(); r = next(x for x in s["appends"] if x["entry"]["status"] == "accepted"); r["entry"]["deferred_to"] = "PLA-1"
        self.assertRefuses("deferred_to must be set iff", P.check_spec_shape, s)

    def test_refuses_an_empty_summary(self):
        s = self.fresh_spec(); s["appends"][0]["entry"]["summary"] = "  "
        self.assertRefuses("empty summary", P.check_spec_shape, s)

    def test_refuses_an_em_dash_in_a_record(self):
        s = self.fresh_spec(); s["appends"][0]["entry"]["summary"] += " — no"
        self.assertRefuses("carries an em dash", P.check_spec_shape, s)

    def test_allows_a_double_dash_in_a_backend_record(self):
        """`--` is quoted page text in two records; a backend record is not consumer copy."""
        self.assertTrue(any("--" in r["entry"]["summary"] for r in self.spec["appends"]))
        self.assertEqual(P.check_spec_shape(self.spec), N_APPENDS)

    def test_refuses_an_addendum_shape(self):
        s = self.fresh_spec(); s["addendum"]["extra"] = 1
        self.assertRefuses("addendum has the wrong shape", P.check_spec_shape, s)

    def test_refuses_an_addendum_without_the_dated_marker(self):
        s = self.fresh_spec(); s["addendum"]["suffix"] = " more text]"
        self.assertRefuses("dated ADDENDUM marker", P.check_spec_shape, s)

    def test_refuses_an_em_dash_in_the_addendum(self):
        s = self.fresh_spec(); s["addendum"]["suffix"] = s["addendum"]["suffix"][:-1] + " — no]"
        self.assertRefuses("addendum carries an em dash", P.check_spec_shape, s)

    def test_refuses_a_crop_count_drift(self):
        """Move one of pear-asian's TWO records to apple: pear-asian stays, apple is added, the set grows to 13.
        (Moving the only record on a crop swaps a crop for a crop and leaves the count at 12.)"""
        s = self.fresh_spec()
        r = next(x for x in s["appends"] if x["crop"] == "pear-asian")
        r["crop"] = "apple"
        self.assertRefuses("crops, pinned", P.check_spec_shape, s)

    def test_refuses_an_expected_block_drift(self):
        s = self.fresh_spec(); s["expected"]["addenda"] = 2
        self.assertRefuses("expected block", P.check_spec_shape, s)


class PreState(Base):
    def test_pre_state_passes(self):
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_APPENDS)

    def test_refuses_a_roster_drift(self):
        d = self.fresh_data(); d["crops"].append(copy.deepcopy(P.by_slug(d)["lime"])); d["crops"][-1]["slug"] = "ghost-crop"
        self.assertRefuses("roster is 129", P.check_pre_state, self.spec, d)

    def test_refuses_a_crop_off_the_roster(self):
        s = self.fresh_spec(); s["appends"][0]["crop"] = "ghost-crop"
        self.assertRefuses("is not on the roster", P.check_pre_state, s, self.data)

    def test_refuses_an_uncertified_crop(self):
        s = self.fresh_spec(); s["appends"][0]["crop"] = "avocado"
        self.assertRefuses("is not certified", P.check_pre_state, s, self.data)

    def test_refuses_a_crop_that_carries_a_dimension(self):
        """The ruling is about nulls: mulberry carries an authored value on the base."""
        s = self.fresh_spec(); s["appends"][0]["crop"] = "mulberry"
        self.assertRefuses("the ruling is about nulls", P.check_pre_state, s, self.data)

    def test_refuses_open_findings_not_a_list(self):
        d = self.fresh_data(); P.by_slug(d)["apricot"]["verification_status"]["open_findings"] = None
        self.assertRefuses("open_findings is not a list", P.check_pre_state, self.spec, d)

    def test_refuses_an_id_already_present(self):
        d = self.fresh_data(); r = self.spec["appends"][0]
        P.by_slug(d)[r["crop"]]["verification_status"]["open_findings"].append({"id": r["entry"]["id"]})
        self.assertRefuses("already carries finding", P.check_pre_state, self.spec, d)

    def test_refuses_an_addendum_target_that_is_not_found_once(self):
        s = self.fresh_spec(); s["addendum"]["id"] = "plum_nobody"
        self.assertRefuses("matches 0 findings", P.check_pre_state, s, self.data)

    def test_refuses_an_addendum_target_whose_summary_moved(self):
        d = self.fresh_data(); self.plum_finding(d)["summary"] += " moved"
        self.assertRefuses("summary has moved", P.check_pre_state, self.spec, d)

    def test_refuses_an_addendum_already_applied(self):
        s = self.fresh_spec(); d = self.fresh_data()
        f = self.plum_finding(d); f["summary"] = f["summary"] + s["addendum"]["suffix"]; s["addendum"]["original_summary"] = f["summary"]
        self.assertRefuses("already carries this addendum", P.check_pre_state, s, d)


class ApplyAndPost(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_apply_changes_exactly_the_declared_records(self):
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec), (N_APPENDS, N_ADDENDA))

    def test_records_land_and_the_addendum_is_the_original_plus_suffix(self):
        post = self.post(); idx = P.by_slug(post)
        for r in self.spec["appends"]:
            self.assertEqual(idx[r["crop"]]["verification_status"]["open_findings"][-1] if r["crop"] != "pear-asian" else None,
                             r["entry"] if r["crop"] != "pear-asian" else None)
        pa = idx["pear-asian"]["verification_status"]["open_findings"]
        self.assertEqual([x["id"] for x in pa[-2:]], [r["entry"]["id"] for r in self.spec["appends"] if r["crop"] == "pear-asian"])
        self.assertEqual(self.plum_finding(post)["summary"], self.spec["addendum"]["original_summary"] + self.spec["addendum"]["suffix"])

    def test_no_dimension_value_moves(self):
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for s in pre:
            for k in P.PDG.FIELDS:
                self.assertEqual(pre[s].get(k), post[s].get(k), (s, k))

    def test_no_other_crop_changes(self):
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for s in pre:
            if s not in CROPS:
                self.assertEqual(pre[s], post[s], s)

    def test_refuses_a_post_state_that_fails_the_gate(self):
        post = self.post(); P.by_slug(post)["apricot"]["mature_height_ft"] = [4, 1]
        self.assertRefuses("plant_dimensions_gate on the post-state", P.check_post, post, self.spec)

    def test_refuses_a_launch_blocker_after_the_write(self):
        post = self.post(); e = P.by_slug(post)["apricot"]["verification_status"]["open_findings"][-1]
        e["blocks_launch"] = True; e["status"] = "open"
        self.assertRefuses("carries a launch blocker", P.check_post, post, self.spec)


class BlastRadius(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_refuses_a_top_level_key_addition(self):
        post = self.post(); post["injected_top_key"] = 1
        self.assertRefuses("top-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_top_level_change(self):
        post = self.post(); post["control_methods"] = {}
        self.assertRefuses("top-level key 'control_methods' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_roster_change(self):
        post = self.post(); post["crops"].pop()
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_untouched_crop_change(self):
        post = self.post(); P.by_slug(post)["apple"]["verification_status"]["open_findings"].append({"id": "stray"})
        self.assertRefuses("untouched crop apple changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_crop_level_key_addition(self):
        post = self.post(); P.by_slug(post)["apricot"]["injected"] = 1
        self.assertRefuses("crop-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_change_outside_verification_status(self):
        post = self.post(); self.assertIn("propagule", P.by_slug(post)["apricot"]); P.by_slug(post)["apricot"]["propagule"] = "seed"
        self.assertRefuses("changed outside verification_status", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_key_addition(self):
        post = self.post(); P.by_slug(post)["apricot"]["verification_status"]["injected"] = 1
        self.assertRefuses("verification_status key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_value_change(self):
        post = self.post(); P.by_slug(post)["apricot"]["verification_status"]["phase"] = "changed"
        self.assertRefuses("verification_status.phase changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_shrunk_list(self):
        post = self.post(); P.by_slug(post)["apricot"]["verification_status"]["open_findings"] = []
        self.assertRefuses("open_findings shrank", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_rewritten_prefix(self):
        post = self.post(); P.by_slug(post)["apricot"]["verification_status"]["open_findings"][0]["summary"] = "rewritten"
        self.assertRefuses("prefix entry 0 is not byte-identical", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_addendum_target_key_addition(self):
        post = self.post(); self.plum_finding(post)["injected"] = 1
        self.assertRefuses("addendum target key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_addendum_summary_other_than_original_plus_suffix(self):
        post = self.post(); self.plum_finding(post)["summary"] = self.spec["addendum"]["suffix"]
        self.assertRefuses("is not the original plus the suffix", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_addendum_target_field_change(self):
        post = self.post(); self.plum_finding(post)["status"] = "resolved"
        self.assertRefuses("addendum target field 'status' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_tail_other_than_the_spec(self):
        post = self.post(); P.by_slug(post)["apricot"]["verification_status"]["open_findings"][-1]["resolution_note"] = "changed"
        self.assertRefuses("appended 1 entries, expected 1 matching the spec", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_appended_record(self):
        post = self.post(); P.by_slug(post)["plum"]["verification_status"]["open_findings"].append({"id": "stray"})
        self.assertRefuses("appended 1 entries, expected 0", P.verify_post, self.data, post, self.spec)


class Serializer(Base):
    def test_compact_no_trailing_newline(self):
        self.assertEqual(P.serialize({"a": [1, 2], "b": "eé"}), b'{"a":[1,2],"b":"e\xc3\xa9"}')

    def test_output_sha_is_stable(self):
        self.assertEqual(P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec))), P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec))))


class WriteGuards(Base):
    def _copy(self):
        d = tempfile.mkdtemp(prefix="pla465b_wg_"); p = os.path.join(d, "crops_data_final.json")
        with open(p, "wb") as f:
            f.write(promote_fixture.pre_state(P.BASE_SHA))
        return d, p

    def _run(self, *args):
        r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla465_null_rulings.py"), *args], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def test_refuses_to_write_without_expect_sha(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p); self.assertNotEqual(rc, 0); self.assertIn("requires --expect-sha", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)

    def test_refuses_out_that_targets_the_canonical(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p, "--out", p); self.assertNotEqual(rc, 0); self.assertIn("may not target the canonical", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)

    def test_refuses_a_wrong_expect_sha_and_leaves_the_copy_untouched(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p, "--expect-sha", "0" * 64); self.assertNotEqual(rc, 0); self.assertIn("REFUSED: expected", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
