#!/usr/bin/env python3
"""Guard suite for promote_pla465_plant_dimensions -- PLA-465 plant dimensions, register row 30.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla465_plant_dimensions_suite.py.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla465_plant_dimensions as P  # noqa: E402

BASE_SHA = "a98b6cfdfd7c5ffdcccdb222ceaa141fdca79e0ed674f991c0dcb396c2534412"
ROSTER = 128
N_KEYS = 121
N_SHELLS = 7
N_AUTHORED = P.EXPECTED_AUTHORED  # pinned in the promote from the staged reads before the first run
WOODY = ("deciduous_fruit_tree", "evergreen_fruit_tree", "berries_woody", "woody_ornamental")


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.spec = P.staged()

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def row(self, spec, crop):
        return next(r for r in spec["authored"] if r["crop"] == crop)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg, f"guard fired with the wrong message.\n  wanted: {fragment!r}\n  got: {msg!r}")


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
        self.assertIsNotNone(N_AUTHORED, "EXPECTED_AUTHORED must be pinned before the first run")
        self.assertEqual((P.EXPECTED_KEYS, P.EXPECTED_SHELLS, P.EXPECTED_AUTHORED), (N_KEYS, N_SHELLS, N_AUTHORED))

    def test_the_spec_is_the_shape_measured(self):
        idx = P.by_slug(self.data)
        self.assertEqual(len(self.spec["authored"]), N_AUTHORED)
        for r in self.spec["authored"]:
            self.assertIn(idx[r["crop"]]["archetype"], WOODY, r["crop"])
        self.assertEqual(self.spec["expected"], {"keys": N_KEYS, "authored": N_AUTHORED, "null": N_KEYS - N_AUTHORED, "shells": N_SHELLS})

    def test_base_carries_no_key_anywhere(self):
        self.assertEqual(sum(1 for c in self.data["crops"] for f in P.FIELDS if f in c), 0)


class SpecShape(Base):
    def test_refuses_a_spec_on_another_base(self):
        s = self.fresh_spec(); s["base_sha"] = "0" * 64
        self.assertRefuses("not the pinned base", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_an_authored_count_drift(self):
        s = self.fresh_spec(); s["authored"].pop()
        self.assertRefuses("authored rows, pinned", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_duplicated_crop(self):
        s = self.fresh_spec(); s["authored"][1] = copy.deepcopy(s["authored"][0])
        self.assertRefuses("appears twice", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_row_with_the_wrong_keys(self):
        s = self.fresh_spec(); s["authored"][0]["extra"] = 1
        self.assertRefuses("has keys", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_an_authored_row_with_no_height(self):
        s = self.fresh_spec(); s["authored"][0]["mature_height_ft"] = None
        self.assertRefuses("no mature_height_ft", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_field_addition_shape(self):
        s = self.fresh_spec(); del s["authored"][0]["field_addition"]["note"]
        self.assertRefuses("wrong shape", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_field_addition_date(self):
        s = self.fresh_spec(); s["authored"][0]["field_addition"]["date"] = "2026-01-01"
        self.assertRefuses("date", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_field_addition_without_sources(self):
        s = self.fresh_spec(); s["authored"][0]["field_addition"]["sources"] = []
        self.assertRefuses("carries no sources", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_note_that_names_no_page(self):
        s = self.fresh_spec(); s["authored"][0]["field_addition"]["note"] = "read it, trust me"
        self.assertRefuses("does not name its page", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_an_expected_block_drift(self):
        s = self.fresh_spec(); s["expected"]["null"] = 0
        self.assertRefuses("expected block", P.check_spec_shape, s, N_AUTHORED)


class PreState(Base):
    def test_pre_state_passes(self):
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_AUTHORED)

    def test_refuses_a_roster_drift(self):
        d = self.fresh_data(); d["crops"].append(copy.deepcopy(P.by_slug(d)["lime"])); d["crops"][-1]["slug"] = "ghost-crop"
        self.assertRefuses("roster is 129", P.check_pre_state, self.spec, d)

    def test_refuses_a_certified_count_drift(self):
        d = self.fresh_data(); P.by_slug(d)["avocado"]["verification_status"] = {"status": "verified_gs_arc", "field_additions": []}
        self.assertRefuses("certified crops, pinned", P.check_pre_state, self.spec, d)

    def test_refuses_a_crop_already_carrying_a_key(self):
        d = self.fresh_data(); P.by_slug(d)["basil"]["mature_height_ft"] = [1, 2]
        self.assertRefuses("already carries mature_height_ft", P.check_pre_state, self.spec, d)

    def test_refuses_field_additions_not_a_list(self):
        d = self.fresh_data(); P.by_slug(d)["basil"]["verification_status"]["field_additions"] = None
        self.assertRefuses("field_additions is not a list", P.check_pre_state, self.spec, d)

    def test_refuses_a_prior_plant_dimensions_record(self):
        d = self.fresh_data()
        P.by_slug(d)["basil"]["verification_status"]["field_additions"].append({"field": "plant_dimensions", "date": "x", "sources": [], "note": "x"})
        self.assertRefuses("already records a plant_dimensions addition", P.check_pre_state, self.spec, d)

    def test_refuses_an_authored_crop_off_the_roster(self):
        s = self.fresh_spec(); s["authored"][0]["crop"] = "ghost-crop"
        self.assertRefuses("is not on the roster", P.check_pre_state, s, self.data)

    def test_refuses_an_authored_shell(self):
        """avocado is woody and uncertified: the certified check answers before the archetype check."""
        s = self.fresh_spec(); s["authored"][0]["crop"] = "avocado"
        self.assertRefuses("is not certified", P.check_pre_state, s, self.data)

    def test_refuses_an_authored_herbaceous_crop(self):
        """R1: define for 121, author the woody 30. basil is certified and not woody."""
        s = self.fresh_spec(); s["authored"][0]["crop"] = "basil"
        self.assertRefuses("is not tree or woody (R1)", P.check_pre_state, s, self.data)

    def test_refuses_a_source_not_in_catalog(self):
        s = self.fresh_spec(); s["authored"][0]["field_addition"]["sources"] = ["nobody_ext"]
        self.assertRefuses("is not in source_catalog", P.check_pre_state, s, self.data)

    def test_refuses_a_row_the_gate_rejects(self):
        s = self.fresh_spec(); s["authored"][0]["mature_height_ft"] = [14, 10]
        self.assertRefuses("fails plant_dimensions_gate", P.check_pre_state, s, self.data)

    def test_refuses_a_row_the_bounds_reject(self):
        s = self.fresh_spec(); s["authored"][0]["mature_height_ft"] = [1, 500]
        self.assertRefuses("fails numeric_sanity", P.check_pre_state, s, self.data)


class ApplyAndPost(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_apply_changes_exactly_the_declared_split(self):
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec), (N_KEYS, N_AUTHORED, N_KEYS - N_AUTHORED))

    def test_every_certified_crop_carries_the_keys_and_no_shell_does(self):
        post = self.post()
        carrying = {c["slug"] for c in post["crops"] if all(f in c for f in P.FIELDS)}
        certified = {c["slug"] for c in post["crops"] if P._certified(c)}
        self.assertEqual(carrying, certified)
        self.assertEqual(len(certified), N_KEYS)

    def test_authored_values_are_the_spec_rows_and_footprint_is_null_everywhere(self):
        idx = P.by_slug(self.post())
        for r in self.spec["authored"]:
            self.assertEqual(idx[r["crop"]]["mature_height_ft"], r["mature_height_ft"])
            self.assertEqual(idx[r["crop"]]["mature_spread_ft"], r["mature_spread_ft"])
        self.assertTrue(all(c.get("footprint_inches") is None for c in self.post()["crops"]))

    def test_no_shell_changes(self):
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for s in pre:
            if not P._certified(pre[s]):
                self.assertEqual(pre[s], post[s], s)

    def test_post_gate_is_clean_with_presence_on(self):
        self.assertEqual(P.PDG.all_violations(self.post(), presence=True), [])

    def test_refuses_a_post_state_that_fails_the_gate(self):
        post = self.post(); P.by_slug(post)[self.spec["authored"][0]["crop"]]["mature_height_ft"] = [14, 10]
        self.assertRefuses("plant_dimensions_gate on the post-state", P.check_post, post, self.spec)

    def test_refuses_an_authored_crop_that_fails_the_bounds(self):
        post = self.post(); P.by_slug(post)[self.spec["authored"][0]["crop"]]["mature_height_ft"] = [1, 500]
        self.assertRefuses("numeric_sanity on", P.check_post, post, self.spec)

    def test_refuses_an_authored_crop_that_fails_display_readiness(self):
        post = self.post()
        slug = next(r["crop"] for r in self.spec["authored"] if (P.by_slug(post)[r["crop"]].get("container_notes") or {}).get("container_ok") is True)
        # display_readiness accepts EITHER a pot figure OR a tray depth on a container_ok crop (apple carries
        # both), so the driver must remove both; nulling the gallons alone leaves the crop readable.
        P.by_slug(post)[slug]["container_notes"]["min_pot_gallons"] = None
        P.by_slug(post)[slug]["container_notes"]["depth_inches_min"] = None
        self.assertRefuses("display_readiness on", P.check_post, post, self.spec)


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

    def test_refuses_a_shell_change(self):
        post = self.post(); P.by_slug(post)["avocado"]["mature_height_ft"] = None
        self.assertRefuses("shell avocado changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_crop_level_key_set_drift(self):
        post = self.post(); del P.by_slug(post)["basil"]["footprint_inches"]
        self.assertRefuses("is not the base's plus the three keys", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_change_outside_the_declared_keys(self):
        post = self.post()
        self.assertIn("propagule", P.by_slug(post)["basil"])
        P.by_slug(post)["basil"]["propagule"] = "cutting"
        self.assertRefuses("changed outside the declared keys", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_non_null_footprint(self):
        post = self.post(); P.by_slug(post)["basil"]["footprint_inches"] = 4
        self.assertRefuses("footprint_inches is not null", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_written_value_other_than_the_spec_row(self):
        post = self.post(); r = self.spec["authored"][0]
        P.by_slug(post)[r["crop"]]["mature_height_ft"] = [r["mature_height_ft"][0], r["mature_height_ft"][1] + 1]
        self.assertRefuses("written dimensions are not the spec row's", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_dimension_on_a_crop_with_no_row(self):
        post = self.post(); P.by_slug(post)["basil"]["mature_height_ft"] = [1, 2]
        self.assertRefuses("carries a dimension with no authored row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_key_addition(self):
        post = self.post(); P.by_slug(post)["basil"]["verification_status"]["injected"] = 1
        self.assertRefuses("verification_status key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_value_change(self):
        post = self.post(); P.by_slug(post)["basil"]["verification_status"]["phase"] = "changed"
        self.assertRefuses("verification_status.phase changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_rewritten_field_additions_prefix(self):
        post = self.post(); r = self.spec["authored"][0]
        fa = P.by_slug(post)[r["crop"]]["verification_status"]["field_additions"]
        self.assertGreater(len(fa), 1, "driver needs a crop with a pre-existing field_additions entry")
        fa[0]["note"] = "rewritten"
        self.assertRefuses("prefix is not byte-identical", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_record_other_than_the_spec(self):
        post = self.post(); r = self.spec["authored"][0]
        P.by_slug(post)[r["crop"]]["verification_status"]["field_additions"][-1]["sources"] = ["other"]
        self.assertRefuses("appended 1 entries, expected 1 matching the spec", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_appended_record(self):
        post = self.post(); P.by_slug(post)["basil"]["verification_status"]["field_additions"].append({"field": "stray"})
        self.assertRefuses("appended 1 entries, expected 0", P.verify_post, self.data, post, self.spec)


class Serializer(Base):
    def test_compact_no_trailing_newline(self):
        self.assertEqual(P.serialize({"a": [1, 2], "b": "eé"}), b'{"a":[1,2],"b":"e\xc3\xa9"}')

    def test_output_sha_is_stable(self):
        a = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        b = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        self.assertEqual(a, b)


class WriteGuards(Base):
    def _copy(self):
        d = tempfile.mkdtemp(prefix="pla465_wg_")
        p = os.path.join(d, "crops_data_final.json")
        with open(p, "wb") as f:
            f.write(promote_fixture.pre_state(P.BASE_SHA))
        return d, p

    def _run(self, *args):
        r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla465_plant_dimensions.py"), *args], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def test_refuses_to_write_without_expect_sha(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p)
            self.assertNotEqual(rc, 0); self.assertIn("requires --expect-sha", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)

    def test_refuses_out_that_targets_the_canonical(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p, "--out", p)
            self.assertNotEqual(rc, 0); self.assertIn("may not target the canonical", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)

    def test_refuses_a_wrong_expect_sha_and_leaves_the_copy_untouched(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p, "--expect-sha", "0" * 64)
            self.assertNotEqual(rc, 0); self.assertIn("REFUSED: expected", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
