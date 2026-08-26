#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch5.py. Base acf33780.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_batch5_suite.py.

THE LOAD-BEARING FAMILY IS `TwinPremise`, and it is what this batch adds over batch 4. Copying one
crop's ladders onto another is licensed by one fact: their SOURCE prose is byte-identical in order.
Batch 4 asserted that by comparing the two STAGED files, which proves a propagation happened and
says nothing about whether it was allowed. The premise lives in canonical, so that is where it is
checked -- all eleven prose fields of all nine problems -- and it is checked in BOTH directions: the
twin must match, and the sibling must NOT, because a sibling that had quietly become identical would
mean the batch is authoring the same crop twice and calling it two passes.

`ReadFixes` is the second half. Four defects came out of reading, and a fix that is not pinned is a
fix that regresses on the next pass over these crops. The subtlest is FIX 1: `off_season_tillage`
and `garden_sanitation` are both cultural, both legal on an insect, and both plausible for "work
crop debris into the soil". Only the METHOD MEANING separates them, and no gate can see that, so the
guard names the key that may not appear rather than the shape that must.

`ReadFixes` also pins a divergence that is CORRECT, in both directions: `augmentative_release` on
the twin's Mexican bean beetle and NOT on the sibling's. The twin's prose names the wasp in both
registers; the sibling's names it in neither. Pinned both ways so a later pass can neither propagate
the claim across the family nor drop it from the crop that earns it.
"""
import copy, hashlib, json, os, sys, unittest
from contextlib import contextmanager

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch5 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "7c3e5d71ae875e013a20b77c3d8dd1f12960bfb8c413e7f8b728df79ef24d145"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _by(d):
    return {c.get("slug"): c for c in d["crops"]}


@contextmanager
def staged_as(batch, digests=None):
    """Run with a doctored staged batch, so refusal specs can drive the real check()."""
    real_s, real_d = P.staged, P.staged_digests
    P.staged = lambda: copy.deepcopy(batch)
    if digests is not None:
        P.staged_digests = lambda: digests
    try:
        yield
    finally:
        P.staged, P.staged_digests = real_s, real_d


def _batch():
    return P.staged()


def _digests():
    return P.staged_digests()


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

    def test_check_passes_on_the_pinned_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_counts(self):
        b = _batch()
        self.assertEqual(P.rung_count(b), 131)
        self.assertEqual(sum(len(P.problems(b[s])) for s in P.CROPS), 27)
        for s, n in P.EXPECTED_RUNGS.items():
            self.assertEqual(sum(len(p["control_ladder"]) for _, p in P.problems(b[s])), n, s)

    def test_the_three_crops_are_unladdered_at_base(self):
        """A batch promote is only meaningful over crops that have no ladder yet."""
        by = _by(_pre())
        for s in P.CROPS:
            for _, p in P.problems(by[s]):
                self.assertNotIn("control_ladder", p, f"{s} already laddered at base")

    def test_roster_laddered_goes_24_to_27(self):
        def laddered(d):
            return sum(1 for c in d["crops"]
                       if any(p.get("control_ladder") for _, p in P.problems(c)))
        pre = _pre()
        self.assertEqual(laddered(pre), 24)
        self.assertEqual(laddered(_post(pre)), 27)


class TwinPremise(unittest.TestCase):
    """What licenses the propagation, checked where the claim actually lives: canonical."""

    def test_the_twin_prose_really_is_identical_in_canonical(self):
        by = _by(_pre())
        self.assertEqual(P.prose_signature(by[P.TWIN[0]]), P.prose_signature(by[P.TWIN[1]]))

    def test_the_sibling_really_does_differ_in_canonical(self):
        by = _by(_pre())
        a = P.prose_signature(by[P.TWIN[0]])
        c = P.prose_signature(by[P.SIBLING])
        self.assertNotEqual(a, c)
        n = sum(1 for x, y in zip(a, c) for i, j in zip(x, y) if i != j)
        self.assertGreater(n, 0, "the sibling is a separate authoring pass only if its prose differs")

    def test_check_REFUSES_a_broken_twin_premise(self):
        pre = _pre()
        by = _by(pre)
        by[P.TWIN[0]]["pests"][0]["cause_beginner"] = "MUTATED"
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("twin premise FAILS", out)

    def test_check_REFUSES_a_sibling_that_became_identical(self):
        pre = _pre()
        by = _by(pre)
        for fam in ("pests", "diseases"):
            by[P.SIBLING][fam] = copy.deepcopy(by[P.TWIN[0]][fam])
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("byte-identical to the twin", out)

    def test_the_premise_does_not_include_the_field_the_promote_writes(self):
        """control_ladder must NOT be in PROSE_FIELDS: the premise would then be self-referential,
        true by construction after the promote and worthless before it."""
        self.assertNotIn("control_ladder", P.PROSE_FIELDS)
        self.assertNotIn("id", P.PROSE_FIELDS)
        self.assertNotIn("type", P.PROSE_FIELDS)


class Grouping(unittest.TestCase):
    def test_staged_twin_files_are_byte_identical(self):
        d = _digests()
        self.assertEqual(d[P.TWIN[0]], d[P.TWIN[1]])

    def test_staged_sibling_differs(self):
        d = _digests()
        self.assertNotEqual(d[P.SIBLING], d[P.TWIN[0]])

    def test_check_REFUSES_a_diverging_twin(self):
        d = dict(_digests())
        d[P.TWIN[0]] = "0" * 64
        with staged_as(_batch(), d):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("NOT byte-identical", out)

    def test_check_REFUSES_a_sibling_propagated_from_the_twin(self):
        b = _batch()
        b[P.SIBLING] = copy.deepcopy(b[P.TWIN[0]])
        d = dict(_digests())
        d[P.SIBLING] = d[P.TWIN[0]]
        with staged_as(b, d):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must be authored separately", out)


class ReadFixes(unittest.TestCase):
    """Four fixes the read applied, plus one divergence it ruled correct. Each pinned both ways."""

    def test_fix1_sibling_carries_sanitation_not_tillage(self):
        by = _by(_post())
        ms, _ = P.ladder_of(by[P.SIBLING], P.MBB)
        self.assertIn("garden_sanitation", ms)
        self.assertNotIn("off_season_tillage", ms)

    def test_check_REFUSES_the_tillage_key_returning(self):
        b = _batch()
        for _, p in P.problems(b[P.SIBLING]):
            if p["id"] == P.MBB:
                for r in p["control_ladder"]:
                    if r["method"] == "garden_sanitation":
                        r["method"] = "off_season_tillage"
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("soil-pupating", out)

    def test_check_REFUSES_the_sanitation_rung_simply_disappearing(self):
        """DELETES the rung rather than swapping it for tillage. The swap trips the
        off_season_tillage branch first, so the "is it still present" branch was never reached --
        the harness reported it as a surviving mutation."""
        b = _batch()
        for _, p in P.problems(b[P.SIBLING]):
            if p["id"] == P.MBB:
                p["control_ladder"] = [r for r in p["control_ladder"]
                                       if r["method"] != "garden_sanitation"]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("lost the garden_sanitation rung", out)

    def test_fix2_anthracnose_order(self):
        by = _by(_post())
        for s in P.TWIN:
            m, _ = P.ladder_of(by[s], "anthracnose")
            self.assertLess(m.index("garden_sanitation"), m.index("water_at_the_base"), s)

    def test_fix3_root_rot_order(self):
        by = _by(_post())
        for s in P.TWIN:
            m, _ = P.ladder_of(by[s], "bean-root-rots")
            self.assertLess(m.index("sound_sowing_practice"), m.index("improve_drainage"), s)

    def test_check_REFUSES_the_anthracnose_order_regressing(self):
        b = _batch()
        for s in P.TWIN:
            for _, p in P.problems(b[s]):
                if p["id"] == "anthracnose":
                    lad = p["control_ladder"]
                    i = [r["method"] for r in lad].index("garden_sanitation")
                    j = [r["method"] for r in lad].index("water_at_the_base")
                    lad[i], lad[j] = lad[j], lad[i]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must precede water_at_the_base", out)

    def test_check_REFUSES_the_root_rot_order_regressing(self):
        """The sibling test to the anthracnose one above. Without it, fix 3 had only a POST-state
        assertion -- which stays green with the guard disabled, because the staged data is already
        in the right order. The harness reported exactly that as a surviving mutation."""
        b = _batch()
        for s in P.TWIN:
            for _, p in P.problems(b[s]):
                if p["id"] == "bean-root-rots":
                    lad = p["control_ladder"]
                    ms = [r["method"] for r in lad]
                    i, j = ms.index("sound_sowing_practice"), ms.index("improve_drainage")
                    lad[i], lad[j] = lad[j], lad[i]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must precede improve_drainage", out)

    def test_fix4_root_injury_claim_is_gone(self):
        by = _by(_post())
        for s in P.TWIN:
            _, p = P.ladder_of(by[s], "bean-root-rots")
            for r in p["control_ladder"]:
                if r["method"] == "sound_sowing_practice":
                    blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                    for tok in P.ROOT_INJURY_TOKENS:
                        self.assertNotIn(tok, blob, s)

    def test_check_REFUSES_the_root_injury_claim_returning(self):
        b = _batch()
        for s in P.TWIN:
            for _, p in P.problems(b[s]):
                if p["id"] == "bean-root-rots":
                    for r in p["control_ladder"]:
                        if r["method"] == "sound_sowing_practice":
                            r["note_beginner"] += " Take care not to damage the roots as you plant."
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("outside its enumerated scope", out)

    def test_the_correct_divergence_holds_in_both_directions(self):
        by = _by(_post())
        for s in P.TWIN:
            m, _ = P.ladder_of(by[s], P.MBB)
            self.assertIn("augmentative_release", m, f"{s} lost the wasp its prose names")
        m, _ = P.ladder_of(by[P.SIBLING], P.MBB)
        self.assertNotIn("augmentative_release", m,
                         "the sibling's prose names no wasp in either register")

    def test_check_REFUSES_the_wasp_propagated_to_the_sibling(self):
        b = _batch()
        for _, p in P.problems(b[P.SIBLING]):
            if p["id"] == P.MBB:
                p["control_ladder"].insert(-1, {"method": "augmentative_release",
                                                "note_beginner": "A wasp is sold for this.",
                                                "note_seasoned": "A parasitoid is available."})
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("names no wasp", out)

    def test_check_REFUSES_the_wasp_dropped_from_the_twin(self):
        b = _batch()
        for s in P.TWIN:
            for _, p in P.problems(b[s]):
                if p["id"] == P.MBB:
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "augmentative_release"]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("lost augmentative_release", out)


class R5IsConsumed(unittest.TestCase):
    """The catalog round was justified by this batch's prose. Prove the batch actually uses it."""

    def test_each_r5_method_lands_on_every_crop(self):
        by = _by(_post())
        for pid, method in P.R5_USE.items():
            for s in P.CROPS:
                m, _ = P.ladder_of(by[s], pid)
                self.assertIn(method, m, f"{s}/{pid}")

    def test_check_REFUSES_a_batch_that_ignores_the_round(self):
        b = _batch()
        for _, p in P.problems(b[P.SIBLING]):
            if p["id"] == "bacterial-blights":
                p["control_ladder"] = [r for r in p["control_ladder"]
                                       if r["method"] != "wet_foliage_discipline"]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("wet_foliage_discipline", out)

    def test_check_REFUSES_when_an_r5_method_is_missing_from_the_catalog(self):
        pre = _pre()
        del pre["control_methods"]["wet_foliage_discipline"]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("r5 round must land first", out)


class Ids(unittest.TestCase):
    def test_ids_match_the_rosters_shipped_spelling(self):
        by = _by(_post())
        for s in P.CROPS:
            for _, p in P.problems(by[s]):
                want = P.ID_CONVENTION.get(p.get("name") or "")
                if want:
                    self.assertEqual(p["id"], want, f"{s}/{p.get('name')}")

    def test_check_REFUSES_an_id_disagreeing_with_the_roster(self):
        b = _batch()
        for _, p in P.problems(b[P.SIBLING]):
            if p["id"] == "aphids":
                p["id"] = "bean-aphids"
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("join keys", out)

    def test_every_id_is_kebab_and_unique_within_its_crop(self):
        import re
        by = _by(_post())
        for s in P.CROPS:
            ids = [p["id"] for _, p in P.problems(by[s])]
            self.assertEqual(len(ids), len(set(ids)), s)
            for i in ids:
                self.assertRegex(i, r"^[a-z0-9]+(?:-[a-z0-9]+)*$", f"{s}/{i}")


class Shape(unittest.TestCase):
    def test_check_REFUSES_an_unknown_method(self):
        b = _batch()
        P.problems(b[P.SIBLING])[0][1]["control_ladder"][0]["method"] = "not_a_method"
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not in catalog", out)

    def test_check_REFUSES_a_tier_decrease(self):
        b = _batch()
        for _, p in P.problems(b[P.SIBLING]):
            if p["id"] == "aphids":
                p["control_ladder"].reverse()
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_check_REFUSES_an_empty_ladder(self):
        """`[]` is not None, and a shape gate cannot see absence unless absence is spelled out.

        TARGETS `bean-leaf-beetle` DELIBERATELY. The first version emptied the sibling's problem 0,
        which is Mexican bean beetle, and `check_read_fixes` runs before `validate_batch` -- so the
        read-fix guard answered and this test passed green while proving nothing about the EMPTY
        check. bean-leaf-beetle is covered by no read fix and no r5 guard, so only the shape check
        can object to it."""
        b = _batch()
        target = next(p for _, p in P.problems(b[P.SIBLING]) if p["id"] == "bean-leaf-beetle")
        target["control_ladder"] = []
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("EMPTY", out)

    def test_check_REFUSES_identical_registers(self):
        b = _batch()
        r = P.problems(b[P.SIBLING])[0][1]["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_check_REFUSES_a_duplicate_method_in_one_ladder(self):
        b = _batch()
        p = P.problems(b[P.SIBLING])[0][1]
        p["control_ladder"].append(copy.deepcopy(p["control_ladder"][-1]))
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("appears twice", out)

    def test_check_REFUSES_an_applies_to_incoherence(self):
        b = _batch()
        for _, p in P.problems(b[P.SIBLING]):
            if p["id"] == "bacterial-blights":
                p["control_ladder"][0]["method"] = "handpick"
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cannot reach type", out)

    def test_check_REFUSES_a_rung_count_drift(self):
        b = _batch()
        P.problems(b[P.SIBLING])[0][1]["control_ladder"].pop()
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("rungs, expected", out)


class BlastRadius(unittest.TestCase):
    def test_no_crop_outside_the_three_changes(self):
        pre = _pre()
        post = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(post)
        self.assertEqual(set(a["crops"]), set(b["crops"]))
        for slug in a["crops"]:
            if slug in P.CROPS:
                continue
            self.assertEqual(b["crops"][slug], a["crops"][slug], slug)

    def test_no_method_or_source_changes(self):
        pre = _pre()
        post = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(post)
        self.assertEqual(b["methods"], a["methods"])
        self.assertEqual(b["sources"], a["sources"])

    def test_verify_post_CATCHES_a_bystander_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        _by(d)["tomatillo"]["name"] = "MUTATED"
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_touched_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["handpick"]["best_use"] += " Extra."
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_touched_source(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["source_catalog"]["umn_ext"]["accessed"] = "2099-01"
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_twin_that_diverged_at_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        _by(d)[P.TWIN[0]]["pests"][0]["control_ladder"][0]["note_beginner"] = "MUTATED"
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("twin pair", out)

    def test_verify_post_CATCHES_a_sibling_propagated_at_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        by = _by(d)
        for fam in ("pests", "diseases"):
            for i, p in enumerate(by[P.SIBLING][fam]):
                p["control_ladder"] = copy.deepcopy(by[P.TWIN[0]][fam][i]["control_ladder"])
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("identical to the twin", out)

    def test_verify_post_CATCHES_a_dropped_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["crops"] = [c for c in d["crops"] if c.get("slug") != "tomatillo"]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

    def test_verify_post_CATCHES_the_tillage_key_returning_after_apply(self):
        """check() sees only the staged batch; these guards are verify_post's own, and nothing
        reached them until a post state was doctored directly."""
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        for _, p in P.problems(_by(d)[P.SIBLING]):
            if p["id"] == P.MBB:
                for r in p["control_ladder"]:
                    if r["method"] == "garden_sanitation":
                        r["method"] = "off_season_tillage"
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("regained off_season_tillage", out)

    def test_verify_post_CATCHES_the_wasp_appearing_on_the_sibling(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        for _, p in P.problems(_by(d)[P.SIBLING]):
            if p["id"] == P.MBB:
                p["control_ladder"].insert(-1, {"method": "augmentative_release",
                                                "note_beginner": "b", "note_seasoned": "s"})
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("gained augmentative_release", out)

    def test_verify_post_CATCHES_the_wasp_dropped_from_BOTH_twins(self):
        """Dropped from BOTH deliberately. Removing it from one member breaks twin identity, and
        that check fires first, so the readfix guard would never be reached."""
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        by = _by(d)
        for s in P.TWIN:
            for _, p in P.problems(by[s]):
                if p["id"] == P.MBB:
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "augmentative_release"]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("lost augmentative_release", out)

    def test_verify_post_is_clean_on_the_real_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(P.snapshot(pre), d))


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_is_clean_on_the_post_state(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_every_new_ladder_is_softest_first(self):
        order = {t: i for i, t in enumerate(P.TIERS)}
        post = _post()
        cm = post["control_methods"]
        by = _by(post)
        for s in P.CROPS:
            for _, p in P.problems(by[s]):
                ranks = [order[cm[r["method"]]["tier"]] for r in p["control_ladder"]]
                self.assertEqual(ranks, sorted(ranks), f"{s}/{p['id']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
