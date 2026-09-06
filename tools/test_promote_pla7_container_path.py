#!/usr/bin/env python3
"""Guard suite for promote_pla7_container_path -- PLA-7 promote A1.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla7_container_path_suite.py.
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla7_container_path as P  # noqa: E402

BASE_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"
ROSTER = 128
N_ROWS = 121
N_NON_NULL = 110
N_NULL = 11
N_TRAY = 8
N_ROOTSTOCK = 8
N_CULTIVAR = 1
N_FLIPS = 3
N_FLAGS = 134
N_GRAVEL = 16
N_APPLICABLE = 12
N_LEAVES = 294
FLIP_CROPS = ("cherry-sour", "cherry-sweet", "mulberry")
TRAY_CROPS = ("arugula-microgreens", "broccoli-microgreens", "cilantro-microgreens", "microgreens-mix",
              "pea-shoots", "radish-microgreens", "sunflower-sprouts", "wheatgrass")


def evidence_filled(spec):
    return all((r.get("evidence") or "").strip() for r in spec["paths"] if r["container_path"] in P.EVIDENCE_VALUES)


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.spec = P.staged()

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def need_evidence(self):
        if not evidence_filled(self.spec):
            self.skipTest("evidence slots not yet filled (Task 7); this test is the last to go green")

    def row(self, spec, crop):
        return next(r for r in spec["paths"] if r["crop"] == crop)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg, f"guard fired with the wrong message.\n  wanted: {fragment!r}\n  got: {msg!r}")


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(promote_fixture.pre_state(P.BASE_SHA)), BASE_SHA)

    def test_fixture_is_the_full_roster(self):
        self.assertEqual(len(self.data["crops"]), ROSTER)

    def test_pins_are_the_literals(self):
        self.assertEqual((P.EXPECTED_ROWS, P.EXPECTED_NON_NULL, P.EXPECTED_NULL, P.EXPECTED_TRAY,
                          P.EXPECTED_ROOTSTOCK, P.EXPECTED_CULTIVAR, P.EXPECTED_FLIPS,
                          P.EXPECTED_FLAGS_MECHANICAL, P.EXPECTED_GRAVEL, P.EXPECTED_APPLICABLE, P.EXPECTED_LEAVES),
                         (N_ROWS, N_NON_NULL, N_NULL, N_TRAY, N_ROOTSTOCK, N_CULTIVAR, N_FLIPS,
                          N_FLAGS, N_GRAVEL, N_APPLICABLE, N_LEAVES))

    def test_the_spec_is_the_shape_measured(self):
        self.assertEqual(len(self.spec["paths"]), N_ROWS)
        self.assertEqual(tuple(sorted(f["crop"] for f in self.spec["flips"])), FLIP_CROPS)
        self.assertEqual(tuple(sorted(r["crop"] for r in self.spec["paths"] if r["container_path"] == "tray")), TRAY_CROPS)
        self.assertEqual(len(self.spec["gravel_normalize"]), N_GRAVEL)
        self.assertEqual(len(self.spec["overwinter_applicable_true"]), N_APPLICABLE)

    def test_base_has_no_key_anywhere(self):
        self.assertEqual(sum(1 for c in self.data["crops"] if "container_path" in c["container_notes"]), 0)

    def test_mechanical_matches_are_the_pinned_count(self):
        self.assertEqual(len(P.mechanical_flags(self.data)), N_FLAGS)


class SpecShape(Base):
    def test_refuses_a_missing_crop(self):
        s = self.fresh_spec(); s["paths"].pop()
        self.assertRefuses("path rows, pinned", P.check_spec_shape, s)

    def test_refuses_a_duplicated_crop(self):
        self.need_evidence()
        s = self.fresh_spec(); s["paths"][1] = dict(s["paths"][0])
        self.assertRefuses("appears twice", P.check_spec_shape, s)

    def test_refuses_an_unknown_value(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "basil")["container_path"] = "dwarf_rootstock"
        self.assertRefuses("not in", P.check_spec_shape, s)

    def test_refuses_rootstock_without_evidence(self):
        s = self.fresh_spec(); self.row(s, "apple")["evidence"] = ""
        self.assertRefuses("without evidence", P.check_spec_shape, s)

    def test_refuses_evidence_on_a_direct_row(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "basil")["evidence"] = "Basil does well in pots."
        self.assertRefuses("carries evidence on a", P.check_spec_shape, s)

    def test_refuses_a_count_drift(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "basil")["container_path"] = None
        self.assertRefuses("non_null rows", P.check_spec_shape, s)

    def test_refuses_a_fourth_flip(self):
        self.need_evidence()
        s = self.fresh_spec()
        s["flips"].append({"crop": "plum", "container_ok": True, "min_pot_gallons": 25, "container_recommended": False})
        self.assertRefuses("flips, pinned", P.check_spec_shape, s)

    def test_refuses_a_flip_that_recommends(self):
        self.need_evidence()
        s = self.fresh_spec(); s["flips"][0]["container_recommended"] = True
        self.assertRefuses("container_recommended false", P.check_spec_shape, s)

    def test_refuses_a_flip_with_an_absurd_pot(self):
        self.need_evidence()
        s = self.fresh_spec(); s["flips"][0]["min_pot_gallons"] = 500
        self.assertRefuses("min_pot_gallons", P.check_spec_shape, s)

    def test_refuses_a_gravel_row_count_drift(self):
        self.need_evidence()
        s = self.fresh_spec(); s["gravel_normalize"].append("basil")
        self.assertRefuses("gravel rows", P.check_spec_shape, s)


class PreState(Base):
    def test_pre_state_passes(self):
        self.need_evidence()
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_ROWS)

    def test_refuses_a_crop_already_carrying_the_key(self):
        self.need_evidence()
        d = self.fresh_data(); P.by_slug(d)["basil"]["container_notes"]["container_path"] = "direct"
        self.assertRefuses("already carries container_path", P.check_pre_state, self.spec, d)

    def test_refuses_a_variety_already_flagged(self):
        self.need_evidence()
        d = self.fresh_data(); P._varieties(P.by_slug(d)["apple"])[0]["container_suitable"] = True
        self.assertRefuses("already carries a variety container key", P.check_pre_state, self.spec, d)

    def test_refuses_evidence_that_does_not_match_the_crop(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "apple")["evidence"] = "This sentence is in no crop."
        self.assertRefuses("evidence found 0 times", P.check_pre_state, s, self.data)

    def test_refuses_evidence_that_matches_twice(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "apple")["evidence"] = "pot"
        self.assertRefuses("needs exactly 1", P.check_pre_state, s, self.data)

    def test_refuses_a_row_whose_null_disagrees_with_container_ok(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "peach")["container_path"] = "direct"
        d = self.fresh_data()
        self.assertRefuses("container_ok will be False", P.check_pre_state, s, d)

    def test_refuses_rootstock_with_no_suitable_entry(self):
        self.need_evidence()
        d = self.fresh_data()
        for r in P.by_slug(d)["apple"]["rootstock_options"]:
            r["container_suitable"] = False
        self.assertRefuses("no container_suitable rootstock entry", P.check_pre_state, self.spec, d)

    def test_refuses_a_flip_on_a_crop_already_true(self):
        self.need_evidence()
        d = self.fresh_data(); P.by_slug(d)["cherry-sweet"]["container_notes"]["container_ok"] = True
        self.assertRefuses("is not container_ok false", P.check_pre_state, self.spec, d)

    def test_refuses_a_missed_gravel_crop(self):
        self.need_evidence()
        d = self.fresh_data(); P.by_slug(d)["basil"]["container_notes"]["drainage"]["gravel_layer"] = "not_required"
        self.assertRefuses("gravel rows differ", P.check_pre_state, self.spec, d)

    def test_refuses_a_missed_applicable_crop(self):
        self.need_evidence()
        d = self.fresh_data(); P.by_slug(d)["basil"]["container_notes"]["overwintering"]["applicable"] = None
        self.assertRefuses("applicable rows differ", P.check_pre_state, self.spec, d)

    def test_refuses_applicable_with_no_prose(self):
        self.need_evidence()
        d = self.fresh_data(); cn = P.by_slug(d)["apple"]["container_notes"]
        cn["overwintering"]["approach_seasoned"] = None; cn["container_overwintering_seasoned"] = None
        self.assertRefuses("no overwintering prose", P.check_pre_state, self.spec, d)

    def test_refuses_a_mechanical_count_drift(self):
        self.need_evidence()
        d = self.fresh_data()
        for c in d["crops"]:
            c["container_notes"]["container_suitable_varieties"] = []
        self.assertRefuses("exact-name variety matches, pinned", P.check_pre_state, self.spec, d)

    def test_refuses_an_explicit_flag_naming_no_entry(self):
        self.need_evidence()
        s = self.fresh_spec(); s["variety_flags"][0]["name"] = "Dwarf Nobody"
        self.assertRefuses("matches 0 entries", P.check_pre_state, s, self.data)


class ApplyAndPost(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_apply_changes_exactly_the_declared_leaves(self):
        self.need_evidence()
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec), N_LEAVES)

    def test_every_certified_crop_carries_the_key_and_no_shell_does(self):
        self.need_evidence()
        post = self.post()
        carrying = {c["slug"] for c in post["crops"] if "container_path" in c["container_notes"]}
        certified = {c["slug"] for c in post["crops"] if (c.get("verification_status") or {}).get("status")}
        self.assertEqual(carrying, certified)
        self.assertEqual(len(certified), N_ROWS)

    def test_the_flips_are_true_with_their_pot(self):
        self.need_evidence()
        idx = P.by_slug(self.post())
        self.assertEqual((idx["cherry-sweet"]["container_notes"]["container_ok"], idx["cherry-sweet"]["container_notes"]["min_pot_gallons"]), (True, 25))
        self.assertEqual((idx["mulberry"]["container_notes"]["container_ok"], idx["mulberry"]["container_notes"]["min_pot_gallons"]), (True, 15))
        self.assertEqual(idx["mulberry"]["container_notes"]["container_path"], "cultivar")

    def test_mulberry_dwarf_everbearing_is_flagged_with_gallons(self):
        self.need_evidence()
        v = next(x for x in P._varieties(P.by_slug(self.post())["mulberry"]) if x["name"] == "Dwarf Everbearing")
        self.assertEqual((v["container_suitable"], v["container_min_gallons"]), (True, 15))

    def test_plum_is_untouched(self):
        self.need_evidence()
        pre, post = P.by_slug(self.data)["plum"], P.by_slug(self.post())["plum"]
        self.assertEqual(post["container_notes"]["container_ok"], False)
        self.assertIsNone(post["container_notes"]["container_path"])
        self.assertEqual(pre["rootstock_options"], post["rootstock_options"])

    def test_no_rootstock_entry_changes_anywhere(self):
        self.need_evidence()
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for s in pre:
            self.assertEqual(pre[s].get("rootstock_options"), post[s].get("rootstock_options"), s)

    def test_gravel_has_one_encoding_afterwards(self):
        self.need_evidence()
        vals = {(c["container_notes"].get("drainage") or {}).get("gravel_layer") for c in self.post()["crops"]}
        self.assertNotIn("not_required", vals)

    def test_post_gate_is_clean_with_presence_on(self):
        self.need_evidence()
        self.assertEqual(P.CPG.all_violations(self.post(), presence=True), [])

    def test_refuses_a_post_state_that_fails_the_gate(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["basil"]["container_notes"]["container_path"] = None
        self.assertRefuses("container_path_gate on the post-state", P.check_post, post, self.spec)

    def test_refuses_a_flip_that_fails_display_readiness(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["cherry-sweet"]["container_notes"]["min_pot_gallons"] = None
        self.assertRefuses("display_readiness on flipped", P.check_post, post, self.spec)


class BlastRadius(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_refuses_a_top_level_change(self):
        self.need_evidence()
        post = self.post(); post["control_methods"] = {}
        self.assertRefuses("top-level key 'control_methods' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_roster_change(self):
        self.need_evidence()
        post = self.post(); post["crops"].pop()
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_shell_change(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["avocado"]["container_notes"]["container_path"] = None
        self.assertRefuses("shell avocado changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_change_outside_the_two_blocks(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["basil"]["description"] = "changed"
        self.assertRefuses("changed outside container_notes/varieties", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_container_notes_key(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["basil"]["container_notes"]["plants_per_pot"] = [1, 2]
        self.assertRefuses("key set changed other than by adding container_path", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_undeclared_container_notes_change(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["basil"]["container_notes"]["min_pot_gallons"] = 99
        self.assertRefuses("changed without a spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_flip_value_other_than_declared(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["cherry-sweet"]["container_notes"]["min_pot_gallons"] = 30
        self.assertRefuses("changed without a spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_variety_flag_without_a_match(self):
        self.need_evidence()
        post = self.post(); P._varieties(P.by_slug(post)["apple"])[0]["container_suitable"] = True
        self.assertRefuses("without a match or a row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_variety_prose_change(self):
        self.need_evidence()
        post = self.post(); P._varieties(P.by_slug(post)["kale"])[0]["name"] = "Renamed"
        self.assertRefuses("variety field 'name' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_leaf_count_drift(self):
        self.need_evidence()
        post = self.post()
        idx = P.by_slug(post)
        slug = next(s for s in self.spec["gravel_normalize"])
        idx[slug]["container_notes"]["drainage"]["gravel_layer"] = "not_required"
        self.assertRefuses("leaves changed, pinned", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_drainage_key_addition(self):
        self.need_evidence()
        post = self.post()
        slug = next(s for s in self.spec["gravel_normalize"])
        P.by_slug(post)[slug]["container_notes"]["drainage"]["injected_key"] = 1
        self.assertRefuses("drainage key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_overwintering_key_addition(self):
        self.need_evidence()
        post = self.post()
        P.by_slug(post)["apple"]["container_notes"]["overwintering"]["injected_key"] = 1
        self.assertRefuses("overwintering key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_variety_min_gallons_other_than_declared(self):
        self.need_evidence()
        post = self.post()
        v = next(x for x in P._varieties(P.by_slug(post)["mulberry"]) if x["name"] == "Dwarf Everbearing")
        v["container_min_gallons"] = 99
        self.assertRefuses("is not the spec's", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_helper_that_flags_the_wrong_variety(self):
        """A count-preserving swap INSIDE the helper: the transform flags Table Queen instead of Honey Bear.
        The old allowed_flags check cannot see it (same helper); the raw-list re-derivation must."""
        self.need_evidence()
        real = P.mechanical_flags

        def swapped(data):
            s = set(real(data))
            s.discard(("acorn-squash", "Honey Bear"))
            s.add(("acorn-squash", "Table Queen"))
            return s
        P.mechanical_flags = swapped
        try:
            post = P.apply_to(self.data, self.spec)
            self.assertRefuses("not in the pre-state container_suitable_varieties list", P.verify_post, self.data, post, self.spec)
        finally:
            P.mechanical_flags = real

    def test_refuses_a_matching_variety_left_unflagged(self):
        self.need_evidence()
        post = self.post()
        v = next(x for x in P._varieties(P.by_slug(post)["acorn-squash"]) if x["name"] == "Honey Bear")
        del v["container_suitable"]
        self.assertRefuses("was not flagged", P.verify_post, self.data, post, self.spec)


class Serializer(Base):
    def test_compact_no_trailing_newline(self):
        b = P.serialize({"a": [1, 2], "b": "eé"})
        self.assertEqual(b, b'{"a":[1,2],"b":"e\xc3\xa9"}')

    def test_output_sha_is_stable(self):
        self.need_evidence()
        a = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        b = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
