#!/usr/bin/env python3
"""Guard suite for promote_pla533_blockers -- PLA-533 2a, Trevor ruling 1 (2026-09-25).

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla533_blockers_suite.py.

Every refusal driver asserts the guard fired with ITS OWN message (assertRefuses), because a driver
that reddens on an earlier check grades its mutation caught for the wrong reason.
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla533_blockers as P  # noqa: E402

BASE_SHA = "83384c85d9daccc71b3d4a0da795872a761538b0e4d8e94b0d401a674a8a6cd6"
CROPS = ("orange-navel", "grapefruit", "mandarin-clementine")
N_FINDINGS = 7
HELD = ("orange_navel_mulched_basin_contradicted_pla533",
        "mandarin_clementine_npk_2_1_1_cites_hs132_pla533")


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(BASE_SHA))
        cls.spec = P.staged()
        cls.post = P.apply_to(copy.deepcopy(cls.data), cls.spec)

    def fresh(self):
        return copy.deepcopy(self.data)

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def assertRefuses(self, fn, needle):
        with self.assertRaises(SystemExit) as cm:
            fn()
        self.assertIn(needle, str(cm.exception), f"refused for the WRONG reason: {cm.exception}")

    def crop(self, data, slug):
        return next(c for c in data["crops"] if c["slug"] == slug)


class TestHappyPath(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)

    def test_spec_carries_exactly_seven_and_not_the_held_two(self):
        ids = [x["finding"]["id"] for x in self.spec["findings"]]
        self.assertEqual(len(ids), N_FINDINGS)
        self.assertEqual(len(set(ids)), N_FINDINGS)
        for h in HELD:
            self.assertNotIn(h, ids)

    def test_every_finding_blocks_and_carries_the_close_condition(self):
        for x in self.spec["findings"]:
            f = x["finding"]
            self.assertIs(f["blocks_launch"], True)
            self.assertEqual(f["status"], "open")
            self.assertIn("resolves ONLY when the named fields are re-authored", f["summary"])
            self.assertIn("Removing, emptying or repointing a citation NEVER resolves it", f["summary"])

    def test_post_appends_the_findings_after_the_existing_ones(self):
        for slug in CROPS:
            pre = self.crop(self.data, slug)["verification_status"]["open_findings"]
            post = self.crop(self.post, slug)["verification_status"]["open_findings"]
            self.assertEqual(post[:len(pre)], pre)
            added = [f["id"] for f in post[len(pre):]]
            want = [x["finding"]["id"] for x in self.spec["findings"] if x["crop"] == slug]
            self.assertEqual(added, want)

    def test_flags_go_false_and_status_does_not_move(self):
        for slug in CROPS:
            vs0 = self.crop(self.data, slug)["verification_status"]
            vs1 = self.crop(self.post, slug)["verification_status"]
            self.assertIs(vs0["launch_ready_core"], True)
            self.assertIs(vs0["launch_ready_seasoned"], True)
            self.assertIs(vs1["launch_ready_core"], False)
            self.assertIs(vs1["launch_ready_seasoned"], False)
            self.assertEqual(vs1["status"], vs0["status"])

    def test_launch_ready_count_goes_117_to_114(self):
        def lr(d):
            return sum(1 for c in d["crops"]
                       if c["verification_status"].get("status") == "verified_gs_arc"
                       and c["verification_status"].get("launch_ready_core")
                       and c["verification_status"].get("launch_ready_seasoned"))
        self.assertEqual(lr(self.data), 117)
        self.assertEqual(lr(self.post), 114)

    def test_nothing_else_moves(self):
        self.assertEqual({k for k in self.data if k != "crops"}, {k for k in self.post if k != "crops"})
        for k in self.data:
            if k != "crops":
                self.assertEqual(self.data[k], self.post[k], k)
        self.assertEqual([c["slug"] for c in self.data["crops"]], [c["slug"] for c in self.post["crops"]])
        for a, b in zip(self.data["crops"], self.post["crops"]):
            if a["slug"] not in CROPS:
                self.assertEqual(a, b, a["slug"])

    def test_output_is_compact(self):
        raw = P.serialize(self.post)
        self.assertFalse(raw.endswith(b"\n"))
        self.assertNotIn(b'": ', raw[:4000])


class TestPreStateRefusals(Base):
    def test_refuses_a_wrong_base(self):
        self.assertRefuses(lambda: P.check_base_sha(b"not the base"), "base sha mismatch")

    def test_refuses_a_flag_already_false(self):
        d = self.fresh()
        self.crop(d, "grapefruit")["verification_status"]["launch_ready_seasoned"] = False
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "launch_ready pre-state")

    def test_refuses_a_preexisting_live_blocker(self):
        d = self.fresh()
        self.crop(d, "mandarin-clementine")["verification_status"]["open_findings"].append(
            {"id": "x", "blocks_launch": True, "status": "open"})
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "already carries a live blocking finding")

    def test_refuses_an_id_collision(self):
        d = self.fresh()
        fid = self.spec["findings"][0]["finding"]["id"]
        self.crop(d, "lemon")["verification_status"]["open_findings"].append({"id": fid, "status": "resolved"})
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "id already exists")

    def test_refuses_a_quoted_field_string_that_is_not_there(self):
        d = self.fresh()
        self.crop(d, "orange-navel")["storage"]["freezer_seasoned"] = "rewritten"
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "quoted string not found")

    def test_refuses_a_quote_absent_from_the_cached_evidence(self):
        s = self.fresh_spec()
        s["findings"][1]["evidence"][0][1] = "a sentence the page never says"
        self.assertRefuses(lambda: P.check_evidence(s), "evidence quote not in cached bytes")

    def test_refuses_a_missing_cached_file(self):
        s = self.fresh_spec()
        s["findings"][0]["evidence"][0][0] = "0" * 64
        self.assertRefuses(lambda: P.check_evidence(s), "missing from")

    def test_refuses_a_cached_file_whose_bytes_drifted(self):
        # The file EXISTS under the right name but its bytes changed. The missing-file driver above
        # cannot reach this check (measured: the digest mutation survived it), so it gets its own.
        import tempfile
        from unittest import mock
        s = self.fresh_spec()
        sha = s["findings"][0]["evidence"][0][0]
        with tempfile.TemporaryDirectory() as d:
            src = open(os.path.join(P.CACHE, f"{sha}.html"), "rb").read()
            open(os.path.join(d, f"{sha}.html"), "wb").write(src + b" ")
            with mock.patch.object(P, "CACHE", d):
                self.assertRefuses(lambda: P.check_evidence(s), "does not hash to its name")


class TestSpecRefusals(Base):
    def test_refuses_a_non_blocking_finding(self):
        s = self.fresh_spec()
        s["findings"][2]["finding"]["blocks_launch"] = False
        self.assertRefuses(lambda: P.check_spec(s), "must block launch")

    def test_refuses_a_finding_without_the_close_condition(self):
        s = self.fresh_spec()
        s["findings"][3]["finding"]["summary"] = "BLOCKS LAUNCH. short."
        self.assertRefuses(lambda: P.check_spec(s), "close condition")

    def test_refuses_the_held_orange_mulch_finding(self):
        s = self.fresh_spec()
        # SUBSTITUTE, don't append: appending makes the count guard fire first (measured -- the
        # first draft of this driver was graded caught by "expected 7 findings", the wrong reason).
        s["findings"][0]["finding"]["id"] = HELD[0]
        self.assertRefuses(lambda: P.check_spec(s), "HELD")

    def test_refuses_the_wrong_finding_count(self):
        s = self.fresh_spec()
        s["findings"].pop()
        self.assertRefuses(lambda: P.check_spec(s), "expected 7 findings")

    def test_refuses_a_crop_outside_the_three(self):
        s = self.fresh_spec()
        s["findings"][0]["crop"] = "lemon"
        self.assertRefuses(lambda: P.check_spec(s), "crop set")


class TestPostStateRefusals(Base):
    def test_post_check_passes_on_the_real_post(self):
        P.check_post(self.data, self.post, self.spec)

    def test_refuses_a_crop_added_in_post(self):
        q = copy.deepcopy(self.post)
        clone = copy.deepcopy(self.crop(q, "lime"))
        clone["slug"] = "ghost-crop"
        q["crops"].append(clone)
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "crop set changed")

    def test_refuses_collateral_damage_on_another_crop(self):
        q = copy.deepcopy(self.post)
        self.crop(q, "lemon")["difficulty"] = "hard"
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "collateral change")

    def test_refuses_collateral_damage_inside_a_target_crop(self):
        q = copy.deepcopy(self.post)
        self.crop(q, "grapefruit")["storage"]["freezer_beginner"] = "x"
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "outside the declared keys")

    def test_refuses_a_status_move(self):
        q = copy.deepcopy(self.post)
        self.crop(q, "orange-navel")["verification_status"]["status"] = "draft"
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "outside the declared keys")

    def test_refuses_a_flag_left_true(self):
        q = copy.deepcopy(self.post)
        self.crop(q, "mandarin-clementine")["verification_status"]["launch_ready_core"] = True
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "flags must both be false")

    def test_refuses_a_top_level_key_change(self):
        q = copy.deepcopy(self.post)
        q["source_catalog"]["ufifas_ext"]["url"] = "x"
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "top-level")


if __name__ == "__main__":
    unittest.main()
