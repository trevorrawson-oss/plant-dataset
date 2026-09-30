#!/usr/bin/env python3
"""Guard suite for promote_pla533_subtractive -- PLA-533 subtractive pass (Trevor rulings 2026-09-29).

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla533_subtractive_suite.py.

Every refusal driver asserts the guard fired with ITS OWN message (assertRefuses): a driver that
reddens on an earlier check grades its mutation caught for the wrong reason (measured twice in the
PLA-533 blockers suite).
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla533_subtractive as P  # noqa: E402

BASE_SHA = "edcd9bf95ad7e3a90ada7c522db23e00172d1f57d74ff33da219908d7a266229"
CHANGED = {"orange-navel", "grapefruit", "mandarin-clementine", "lemon", "lime"}
N_EDITS = 31


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

    def fresh_post(self):
        return copy.deepcopy(self.post)

    def crop(self, d, slug):
        return next(c for c in d["crops"] if c["slug"] == slug)

    def assertRefuses(self, fn, needle):
        with self.assertRaises(SystemExit) as cm:
            fn()
        self.assertIn(needle, str(cm.exception), f"refused for the WRONG reason: {cm.exception}")


class TestHappyPath(Base):
    def test_base_sha_pinned(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)

    def test_edit_count(self):
        self.assertEqual(len(self.spec["edits"]), N_EDITS)

    def test_every_before_is_gone_and_every_after_present(self):
        for e in self.spec["edits"]:
            v = P.at(self.crop(self.post, e["crop"]), e["path"]) if e["crop"] != "lime" or not e["path"].startswith("/rootstock_options") else None
            if v is None:
                continue
            self.assertNotIn(e["before"], v, e)
            if e["after"]:
                self.assertIn(e["after"], v, e)

    def test_no_sulfur_acidification_survives_on_the_three_crops(self):
        for slug in ("orange-navel", "grapefruit", "mandarin-clementine"):
            c = self.crop(self.post, slug)
            for p in ("/soil/preferred_description_seasoned", "/ph/note_seasoned", "/ph/note_beginner"):
                self.assertNotRegex(P.at(c, p).lower(), r"sulfur|acidif")

    def test_lime_row_removed_and_others_byte_equal(self):
        pre = self.crop(self.data, "lime")["rootstock_options"]
        post = self.crop(self.post, "lime")["rootstock_options"]
        self.assertEqual(pre[0]["name"], "sour orange (Citrus aurantium)")
        self.assertEqual(len(post), len(pre) - 1)
        # byte-equal to the surviving pre rows EXCEPT row 1's traits_seasoned (ruling 1, third batch),
        # which test_row1_comparison_sentence_deleted pins to its exact text
        want = copy.deepcopy(pre[1:])
        want[0]["traits_seasoned"] = post[0]["traits_seasoned"]
        self.assertEqual(post, want)

    def test_lime_note_exact(self):
        self.assertEqual(self.crop(self.post, "lime")["recommended_rootstock_note"],
            "At a retail nursery you usually take whatever industry-standard rootstock the tree is grafted on; it is "
            "rarely a choice. Key limes are susceptible to tristeza whatever the rootstock, and Tahiti limes may be "
            "susceptible to severe strains whatever the rootstock. On the deep sands and calcareous rocklands where "
            "limes are often grown, UF/IFAS favors rough lemon, Volkamer lemon, alemow, or Rangpur lime; on "
            "neutral-to-low-pH soils, Swingle citrumelo adds foot-rot and tristeza resistance and some cold tolerance. "
            "Key lime is often grown on its own roots from seed, cuttings, or air-layers rather than grafted. Note that "
            "scion choice matters less for a lime's cold hardiness than simply avoiding frost.")

    def test_lime_recommended_rootstock_null(self):
        self.assertIsNone(self.crop(self.post, "lime")["recommended_rootstock"])

    def test_row1_comparison_sentence_deleted(self):
        t = self.crop(self.post, "lime")["rootstock_options"][0]["traits_seasoned"]
        self.assertNotIn("sour orange", t)
        self.assertEqual(t, "Vigorous, drought- and sand-tolerant rootstocks that UF/IFAS recommends for the deep "
                            "sands and high-pH calcareous soils of Florida; they crop heavily and tolerate alkaline ground.")

    def test_flying_dragon_shape_b(self):
        for slug in ("orange-navel", "grapefruit"):
            fd = self.crop(self.post, slug)["rootstock_options"][2]
            self.assertEqual(fd["name"], "Flying Dragon trifoliate")
            self.assertIsNone(fd["container_size_gallons"])
            self.assertIs(fd["container_suitable"], True)

    def test_findings_and_flags_untouched(self):
        for slug in CHANGED:
            a, b = self.crop(self.data, slug)["verification_status"], self.crop(self.post, slug)["verification_status"]
            self.assertEqual(a, b, slug)

    def test_other_crops_and_top_level_untouched(self):
        for a, b in zip(self.data["crops"], self.post["crops"]):
            if a["slug"] not in CHANGED:
                self.assertEqual(a, b, a["slug"])
        for k in self.data:
            if k != "crops":
                self.assertEqual(self.data[k], self.post[k], k)

    def test_post_check_passes(self):
        P.check_post(self.data, self.post, self.spec)

    def test_compact_output(self):
        raw = P.serialize(self.post)
        self.assertFalse(raw.endswith(b"\n"))
        self.assertNotIn(b'": ', raw[:4000])


class TestPreRefusals(Base):
    def test_refuses_wrong_base(self):
        self.assertRefuses(lambda: P.check_base_sha(b"x"), "base sha mismatch")

    def test_refuses_a_target_not_found(self):
        d = self.fresh()
        self.crop(d, "orange-navel")["ph"]["note_seasoned"] = "rewritten"
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "found 0 times")

    def test_refuses_a_target_found_twice(self):
        d = self.fresh()
        c = self.crop(d, "grapefruit")["ph"]
        c["note_beginner"] = c["note_beginner"] + " " + c["note_beginner"]
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "found 2 times")

    def test_refuses_an_added_number(self):
        s = self.fresh_spec()
        e = next(x for x in s["edits"] if x["path"] == "/yield_expectations/per_plant_seasoned")
        e["after"] = "A mature navel yields 150 pounds."
        self.assertRefuses(lambda: P.check_spec(s), "adds a number or citation")

    def test_refuses_an_added_citation_token(self):
        s = self.fresh_spec()
        e = next(x for x in s["edits"] if x["path"] == "/ph/note_seasoned" and x["crop"] == "lime") \
            if any(x["crop"] == "lime" and x["path"] == "/ph/note_seasoned" for x in s["edits"]) else s["edits"][10]
        e["after"] = e["after"] + " See https://example.org."
        self.assertRefuses(lambda: P.check_spec(s), "adds a number or citation")

    def test_refuses_wrong_lime_row(self):
        d = self.fresh()
        self.crop(d, "lime")["rootstock_options"][0]["name"] = "something else"
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "sour orange row")

    def test_refuses_wrong_lime_recommended_prestate(self):
        d = self.fresh()
        self.crop(d, "lime")["recommended_rootstock"] = "rough lemon"
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "recommended_rootstock pre-state")

    def test_refuses_wrong_flying_dragon_prestate(self):
        d = self.fresh()
        self.crop(d, "grapefruit")["rootstock_options"][2]["container_size_gallons"] = 20
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "container_size_gallons pre-state")

    def test_refuses_a_crop_outside_the_set(self):
        s = self.fresh_spec()
        s["edits"][0]["crop"] = "apple"
        self.assertRefuses(lambda: P.check_spec(s), "outside the change set")


class TestPostRefusals(Base):
    def test_refuses_a_crop_added(self):
        q = self.fresh_post()
        g = copy.deepcopy(self.crop(q, "apple")); g["slug"] = "ghost-crop"; q["crops"].append(g)
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "crop set changed")

    def test_refuses_collateral_on_another_crop(self):
        q = self.fresh_post()
        self.crop(q, "apple")["difficulty"] = "x"
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "collateral change on apple")

    def test_refuses_an_undeclared_change_inside_a_changed_crop(self):
        q = self.fresh_post()
        self.crop(q, "lemon")["difficulty"] = "x"
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "undeclared change inside lemon")

    def test_refuses_a_finding_resolved_by_the_pass(self):
        q = self.fresh_post()
        f = self.crop(q, "orange-navel")["verification_status"]["open_findings"]
        next(x for x in f if x.get("blocks_launch"))["status"] = "resolved"
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "undeclared change inside orange-navel")

    def test_refuses_the_container_flag_moving(self):
        q = self.fresh_post()
        self.crop(q, "orange-navel")["rootstock_options"][2]["container_suitable"] = None
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "undeclared change inside orange-navel")

    def test_refuses_a_top_level_change(self):
        q = self.fresh_post()
        q["source_catalog"]["uf_ifas"]["url"] = "x"
        self.assertRefuses(lambda: P.check_post(self.data, q, self.spec), "top-level")


if __name__ == "__main__":
    unittest.main()
