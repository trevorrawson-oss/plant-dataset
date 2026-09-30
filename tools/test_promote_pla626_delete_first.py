#!/usr/bin/env python3
"""Guard suite for promote_pla626_delete_first -- PLA-626 delete-first on apricot and plum
(Trevor rulings 2026-09-29).

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla626_delete_first_suite.py.

Every refusal driver asserts the guard fired with ITS OWN message (assertRefuses): a driver that
reddens on an earlier check grades its mutation caught for the wrong reason.

REACHABILITY: the two purpose guards (St. Julien, prune brownline) are asserted to find their text in
the PRE-state, so "absent from post" cannot be green because the text was never there.

KEPT BY RULING, asserted byte-identical: apricot's Myrobalan / Lovell rows and Marianna's canker
sentence (UC IPM-supported; attribution work for PLA-566), plum's Myrobalan heavier/wetter-soils clause,
plum soil prose, plum's Guardian row. A delete-first pass that takes true text off the site is the
failure this ticket's re-verification caught; these tests keep it caught.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla626_delete_first as P  # noqa: E402

BASE_SHA = "d8906b4313864161c361534cde1b8404c93a81ce44cc5640bf5f51f624b23ce9"
OUTPUT_SHA = "00dda31cc6616b9ea865f04fe0ce97fb1fb5d821f0c94724d3a03dbad8c8dd8e"
CHANGED = {"apricot", "plum"}
N_EDITS = 4
N_RETRACTIONS = 1

PLUM_NOTE_AFTER = ("Pick a rootstock for your soil, pests, and desired tree size: Myrobalan is the vigorous, widely "
                   "adaptable default that tolerates heavier and wetter soils, while Marianna is a size-limiting "
                   "choice for smaller trees.")
MARIANNA_AFTER = ("Plum-hybrid rootstock tolerant of heavy, wet soils with resistance to root-knot nematode and oak "
                  "root fungus. Like Myrobalan it is more susceptible to bacterial canker than the seedling stocks, "
                  "and some apricot cultivars are incompatible on it, so match the variety carefully.")


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = promote_fixture.pre_state(BASE_SHA)
        cls.data = json.loads(cls.raw)
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
        self.assertEqual(P.sha256(self.raw), BASE_SHA)

    def test_spec_counts(self):
        self.assertEqual(len(self.spec["edits"]), N_EDITS)
        self.assertEqual(len(self.spec["retractions"]), N_RETRACTIONS)
        self.assertEqual({e["crop"] for e in self.spec["edits"]}, CHANGED)

    def test_output_sha_pinned(self):
        # equals the independently staged scratch (_handoff/pla626_stage_delete_first.py) reviewed in chat
        self.assertEqual(P.sha256(P.serialize(self.post)), OUTPUT_SHA)

    def test_apricot_recommended_rootstock_retracted(self):
        self.assertEqual(self.crop(self.data, "apricot")["recommended_rootstock"], "Myrobalan 29C")
        self.assertIsNone(self.crop(self.post, "apricot")["recommended_rootstock"])

    def test_marianna_exact(self):
        self.assertEqual(self.crop(self.post, "apricot")["rootstock_options"][2]["traits_seasoned"], MARIANNA_AFTER)

    def test_plum_note_exact_and_myrobalan_clause_kept(self):
        note = self.crop(self.post, "plum")["recommended_rootstock_note"]
        self.assertEqual(note, PLUM_NOTE_AFTER)
        self.assertIn("tolerates heavier and wetter soils", note)

    def test_plum_container_notes_drop_st_julien_only(self):
        pre = self.crop(self.data, "plum")["container_notes"]
        post = self.crop(self.post, "plum")["container_notes"]
        for k in ("notes_beginner", "notes_seasoned"):
            self.assertIn("St. Julien or Marianna", pre[k])
            self.assertEqual(post[k], pre[k].replace("St. Julien or Marianna", "Marianna"))

    def test_purpose_guards_are_reachable_on_pre(self):
        self.assertTrue(P.consumer_hits(self.crop(self.data, "plum"), P.ST_JULIEN))
        self.assertTrue(P.consumer_hits(self.crop(self.data, "apricot"), P.BROWNLINE))

    def test_purpose_guards_clean_on_post(self):
        self.assertEqual(P.consumer_hits(self.crop(self.post, "plum"), P.ST_JULIEN), [])
        self.assertEqual(P.consumer_hits(self.crop(self.post, "apricot"), P.BROWNLINE), [])

    def test_kept_by_ruling(self):
        a0, a1 = self.crop(self.data, "apricot"), self.crop(self.post, "apricot")
        for i in (0, 1, 3):   # apricot seedling, Myrobalan, Lovell rows: byte-identical
            self.assertEqual(a0["rootstock_options"][i], a1["rootstock_options"][i], i)
        self.assertEqual(a0["recommended_rootstock_note"], a1["recommended_rootstock_note"])
        self.assertEqual(a0["diseases"], a1["diseases"])
        p0, p1 = self.crop(self.data, "plum"), self.crop(self.post, "plum")
        self.assertEqual(p0["soil"], p1["soil"])
        self.assertEqual(p0["rootstock_options"], p1["rootstock_options"])
        self.assertIn("Lovell, Halford, or Guardian", p1["rootstock_options"][3]["traits_seasoned"])

    def test_findings_and_flags_untouched(self):
        for slug in CHANGED:
            self.assertEqual(self.crop(self.data, slug)["verification_status"],
                             self.crop(self.post, slug)["verification_status"], slug)

    def test_other_crops_and_top_level_untouched(self):
        self.assertEqual([c["slug"] for c in self.data["crops"]], [c["slug"] for c in self.post["crops"]])
        for a, b in zip(self.data["crops"], self.post["crops"]):
            if a["slug"] not in CHANGED:
                self.assertEqual(a, b, a["slug"])
        for k in self.data:
            if k != "crops":
                self.assertEqual(self.data[k], self.post[k], k)

    def test_check_post_passes(self):
        P.check_post(self.data, self.post, self.spec)

    def test_serializer_is_compact(self):
        self.assertEqual(P.serialize({"a": "é", "b": 1}), b'{"a":"\xc3\xa9","b":1}')


class TestRefusals(Base):
    def test_refuses_moved_base(self):
        self.assertRefuses(lambda: P.check_base_sha(self.raw + b" "), "base sha mismatch")

    def test_refuses_target_absent(self):
        s = self.fresh_spec()
        s["edits"][0]["before"] = "a sentence that is not there"
        self.assertRefuses(lambda: P.apply_to(self.fresh(), s), "found 0 times")

    def test_refuses_target_twice(self):
        d = self.fresh()
        c = self.crop(d, "plum")
        c["recommended_rootstock_note"] += " " + self.spec["edits"][1]["before"]
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "found 2 times")

    def test_refuses_edit_outside_change_set(self):
        s = self.fresh_spec()
        s["edits"][0]["crop"] = "peach"
        self.assertRefuses(lambda: P.apply_to(self.fresh(), s), "outside the change set")

    def test_refuses_added_number(self):
        s = self.fresh_spec()
        s["edits"][1]["after"] = "while Marianna is a size-limiting choice for trees of 10 feet."
        self.assertRefuses(lambda: P.apply_to(self.fresh(), s), "adds a number or citation token")

    def test_refuses_added_citation(self):
        s = self.fresh_spec()
        s["edits"][1]["after"] = "while Marianna is a size-limiting choice for smaller trees (see https://example.org/x)."
        self.assertRefuses(lambda: P.apply_to(self.fresh(), s), "adds a number or citation token")

    def test_refuses_retraction_outside_pinned_field(self):
        s = self.fresh_spec()
        s["retractions"][0]["crop"] = "plum"
        self.assertRefuses(lambda: P.apply_to(self.fresh(), s), "retraction outside")

    def test_refuses_recommended_rootstock_pre_state(self):
        d = self.fresh()
        self.crop(d, "apricot")["recommended_rootstock"] = "Nemaguard"
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "recommended_rootstock pre-state")

    def test_refuses_marianna_row_moved(self):
        d = self.fresh()
        rows = self.crop(d, "apricot")["rootstock_options"]
        rows[1], rows[2] = rows[2], rows[1]
        self.assertRefuses(lambda: P.apply_to(d, self.spec), "is not Marianna 2624")

    def test_refuses_crop_set_change(self):
        post = self.fresh_post()
        ghost = copy.deepcopy(self.crop(post, "plum"))
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        self.assertRefuses(lambda: P.check_post(self.data, post, self.spec), "crop set changed")

    def test_refuses_top_level_change(self):
        post = self.fresh_post()
        post["version"] = "tampered"
        self.assertRefuses(lambda: P.check_post(self.data, post, self.spec), "top-level key changed")

    def test_refuses_collateral_change(self):
        post = self.fresh_post()
        self.crop(post, "peach")["name"] = "Peach!"
        self.assertRefuses(lambda: P.check_post(self.data, post, self.spec), "collateral change on peach")

    def test_refuses_undeclared_change_inside_a_changed_crop(self):
        post = self.fresh_post()
        self.crop(post, "apricot")["verification_status"]["launch_ready_core"] = False
        self.assertRefuses(lambda: P.check_post(self.data, post, self.spec), "undeclared change inside apricot")

    def test_refuses_st_julien_surviving(self):
        # a spec that drops the two container_notes edits applies cleanly and passes the reversal check,
        # so ONLY the purpose guard can stop it
        s = self.fresh_spec()
        s["edits"] = [e for e in s["edits"] if not e["path"].startswith("/container_notes")]
        post = P.apply_to(self.fresh(), s)
        self.assertRefuses(lambda: P.check_post(self.data, post, s), "St. Julien survives")

    def test_refuses_brownline_surviving(self):
        s = self.fresh_spec()
        s["edits"] = [e for e in s["edits"] if e["crop"] != "apricot"]
        post = P.apply_to(self.fresh(), s)
        self.assertRefuses(lambda: P.check_post(self.data, post, s), "brownline survives")


class TestEntryPoint(Base):
    def _run(self, blob, *args):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "canonical.json")
            out = os.path.join(td, "post.json")
            with open(path, "wb") as f:
                f.write(blob)
            argv = [a.replace("{OUT}", out) for a in args]
            r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla626_delete_first.py"), *argv, path],
                               capture_output=True, text=True)
            after = open(path, "rb").read()
            post = open(out, "rb").read() if os.path.exists(out) else None
            return r, after, post

    def test_check_writes_nothing(self):
        r, after, _ = self._run(self.raw, "--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(OUTPUT_SHA, r.stdout)
        self.assertEqual(P.sha256(after), BASE_SHA)

    def test_out_writes_elsewhere(self):
        r, after, post = self._run(self.raw, "--out", "{OUT}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(P.sha256(after), BASE_SHA)
        self.assertEqual(P.sha256(post), OUTPUT_SHA)

    def test_expect_sha_mismatch_refuses_and_writes_nothing(self):
        r, after, _ = self._run(self.raw, "--expect-sha", "0" * 64)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--expect-sha", r.stdout + r.stderr)
        self.assertEqual(P.sha256(after), BASE_SHA)

    def test_main_refuses_a_moved_base(self):
        d = json.loads(self.raw)
        d["version"] = "tampered"
        r, _, _ = self._run(P.serialize(d), "--check")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("base sha mismatch", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
