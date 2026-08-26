#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch6.py. Base 17d0eac7.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_batch6_suite.py.

THE LOAD-BEARING FAMILY IS `ReadFinding`, and what makes it worth reading is that the drop it pins
is SCOPED. `wet_foliage_discipline` leaves the powdery-mildew ladder because its mechanism is
free-water transport and powdery mildew does not travel that way, and it STAYS on the ascochyta
ladder on the same two crops, because that entry's own cause says splashing water spreads it. One
method, one crop, right use and wrong use side by side. A guard that only checked the removal would
be satisfied by deleting the method everywhere, which is the over-correction; both halves are
asserted, plus `airflow_spacing` surviving as the method that SHOULD carry the canopy case.

`NotTwins` is batch 5's premise inverted, and it needs asserting just as hard. Batch 5 propagated
one crop's ladders onto another and proved the licence in canonical. These two are a shared-name
family at 82.8%, so the claim is the opposite one: they are NOT the same crop and each needed its
own pass. Refused in both directions -- identical in canonical means propagation was available and
this batch did double work; identical as staged means one file was copied and the second pass never
happened.

`RoundsExercised` ties three catalog rounds to real data. r6 corrected this method's criterion, r7
refused to widen it to a disease, and both passes then hit exactly that wall and reported it. The
refusal is observable here as data rather than as a comment: `planting_time_avoidance` appears on an
insect problem and on no fungal one.
"""
import copy, hashlib, json, os, sys, unittest
from contextlib import contextmanager

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch6 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "3a87737a60c544453497f67bc3744d8534a400cbcba795b6e4b23fdcbabc3cb5"

# Problems covered by NO read-fix and NO round pin, so a shape refusal aimed here cannot be
# answered by an earlier guard. Batch 5 shipped a shape test that was masked exactly that way.
UNGUARDED = "armyworms-cutworms"


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


def _find(b, slug, pid):
    for _, p in P.problems(b[slug]):
        if p["id"] == pid:
            return p
    raise AssertionError(f"{slug}/{pid} not staged")


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
        self.assertEqual(P.rung_count(b), 84)
        self.assertEqual(sum(len(P.problems(b[s])) for s in P.CROPS), 16)

    def test_both_crops_are_unladdered_at_base(self):
        by = _by(_pre())
        for s in P.CROPS:
            for _, p in P.problems(by[s]):
                self.assertNotIn("control_ladder", p, f"{s} already laddered")

    def test_roster_laddered_goes_27_to_29(self):
        def laddered(d):
            return sum(1 for c in d["crops"]
                       if any(p.get("control_ladder") for _, p in P.problems(c)))
        pre = _pre()
        self.assertEqual(laddered(pre), 27)
        self.assertEqual(laddered(_post(pre)), 29)


class NotTwins(unittest.TestCase):
    """Batch 5's premise, inverted. The claim here is that these are NOT the same crop."""

    def test_canonical_prose_differs(self):
        by = _by(_pre())
        a = P.prose_signature(by[P.CROPS[0]])
        b = P.prose_signature(by[P.CROPS[1]])
        self.assertNotEqual(a, b)
        n = sum(1 for x, y in zip(a, b) for i, j in zip(x, y) if i != j)
        self.assertGreater(n, 0, "these were authored as two passes only if their prose differs")

    def test_check_REFUSES_crops_that_became_identical_in_canonical(self):
        pre = _pre()
        by = _by(pre)
        for fam in ("pests", "diseases"):
            by[P.CROPS[1]][fam] = copy.deepcopy(by[P.CROPS[0]][fam])
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("TRUE TWIN", out)

    def test_check_REFUSES_one_staged_file_copied_from_the_other(self):
        b = _batch()
        b[P.CROPS[1]] = copy.deepcopy(b[P.CROPS[0]])
        d = dict(P.staged_digests())
        d[P.CROPS[1]] = d[P.CROPS[0]]
        with staged_as(b, d):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copied from the other", out)

    def test_the_two_ladders_differ_in_content_after_apply(self):
        by = _by(_post())
        def sig(s):
            return json.dumps([[(r["method"], r["note_beginner"], r["note_seasoned"])
                                for r in p["control_ladder"]] for _, p in P.problems(by[s])],
                              sort_keys=True)
        self.assertNotEqual(sig(P.CROPS[0]), sig(P.CROPS[1]))


class ReadFinding(unittest.TestCase):
    """The drop is SCOPED. Both halves asserted, or deleting the method everywhere would pass."""

    def test_powdery_mildew_does_not_carry_the_method(self):
        by = _by(_post())
        for s in P.CROPS:
            m, _ = P.ladder_of(by[s], P.PM)
            self.assertNotIn(P.WFD, m, s)

    def test_ascochyta_STILL_carries_it(self):
        """The half that stops this being a blanket removal."""
        by = _by(_post())
        for s in P.CROPS:
            m, _ = P.ladder_of(by[s], P.ASC)
            self.assertIn(P.WFD, m, f"{s}: the drop was scoped to powdery mildew, not global")

    def test_airflow_spacing_survives_on_powdery_mildew(self):
        by = _by(_post())
        for s in P.CROPS:
            m, _ = P.ladder_of(by[s], P.PM)
            self.assertIn("airflow_spacing", m, s)

    def test_check_REFUSES_the_method_returning_to_powdery_mildew(self):
        b = _batch()
        p = _find(b, P.CROPS[0], P.PM)
        p["control_ladder"].insert(2, {"method": P.WFD, "note_beginner": "b", "note_seasoned": "s"})
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("do not spread in rain or free water", out)

    def test_check_REFUSES_a_blanket_removal_that_also_strips_ascochyta(self):
        b = _batch()
        p = _find(b, P.CROPS[0], P.ASC)
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != P.WFD]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("blanket removal", out)

    def test_check_REFUSES_airflow_spacing_being_dropped_too(self):
        b = _batch()
        p = _find(b, P.CROPS[0], P.PM)
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "airflow_spacing"]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("SHOULD carry the canopy case", out)

    def test_check_REFUSES_running_without_the_catalog_caution(self):
        """The exception must be on the sheet before these ladders ship, or the trap stays in place
        for the 21 other crops whose powdery mildew carries wet-handling advice."""
        pre = _pre()
        pre["control_methods"][P.WFD]["cautions"] = ["something else entirely"]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("powdery-mildew exception", out)

    def test_the_orderings_normalized_on_both_crops(self):
        by = _by(_post())
        for s in P.CROPS:
            m, _ = P.ladder_of(by[s], "root-rots-damping-off")
            self.assertLess(m.index("improve_drainage"), m.index("sound_sowing_practice"), s)
            self.assertEqual(m[-1], "resistant_varieties", s)
            a, _ = P.ladder_of(by[s], P.ASC)
            self.assertLess(a.index("garden_sanitation"), a.index("crop_rotation"), s)

    def test_check_REFUSES_the_tolerance_rung_moving_off_the_end(self):
        """Was a POST-state assertion only, which stays green with its guard disabled because the
        staged data is already correct. Same defect batch 5 shipped on fix 3."""
        b = _batch()
        p = _find(b, P.CROPS[0], "root-rots-damping-off")
        lad = p["control_ladder"]
        rv = next(i for i, r in enumerate(lad) if r["method"] == "resistant_varieties")
        lad.insert(0, lad.pop(rv))
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("belongs last", out)

    def test_check_REFUSES_the_root_rot_order_regressing(self):
        b = _batch()
        p = _find(b, P.CROPS[0], "root-rots-damping-off")
        lad = p["control_ladder"]
        ms = [r["method"] for r in lad]
        i, j = ms.index("improve_drainage"), ms.index("sound_sowing_practice")
        lad[i], lad[j] = lad[j], lad[i]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must precede sound_sowing_practice", out)

    def test_check_REFUSES_the_ascochyta_order_regressing(self):
        b = _batch()
        p = _find(b, P.CROPS[0], P.ASC)
        lad = p["control_ladder"]
        ms = [r["method"] for r in lad]
        i, j = ms.index("garden_sanitation"), ms.index("crop_rotation")
        lad[i], lad[j] = lad[j], lad[i]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must precede crop_rotation", out)


class RoundsExercised(unittest.TestCase):
    def test_the_pin_tables_are_not_empty(self):
        """A COVERAGE assertion. `test_each_pinned_method_lands_on_both_crops` iterates the tables
        it is validating, so emptying one makes the loop check nothing and still pass -- the
        harness reported exactly that. Name the contents instead of trusting the count."""
        self.assertEqual(P.R6_USE, {"pea-weevil": "planting_time_avoidance"})
        self.assertIn("biofungicide", P.R7_USE.values())
        self.assertIn("weed_host_control", P.R7_USE.values())
        self.assertGreaterEqual(len(P.R7_USE), 3)

    def test_each_pinned_method_lands_on_both_crops(self):
        by = _by(_post())
        for pid, method in list(P.R7_USE.items()) + list(P.R6_USE.items()):
            for s in P.CROPS:
                m, _ = P.ladder_of(by[s], pid)
                self.assertIn(method, m, f"{s}/{pid}")

    def test_the_r7_refusal_is_observable_as_data(self):
        """planting_time_avoidance reaches an insect problem and no disease. That is the refusal,
        visible in the shipped ladders rather than only in a docstring."""
        by = _by(_post())
        insect = disease = 0
        for s in P.CROPS:
            for _, p in P.problems(by[s]):
                if "planting_time_avoidance" in [r["method"] for r in p["control_ladder"]]:
                    if p["type"] == "insect":
                        insect += 1
                    else:
                        disease += 1
        self.assertEqual(disease, 0, "a disease reached a method r7 refused to widen")
        self.assertGreater(insect, 0, "the pin has no denominator: nothing uses the method at all")

    def test_check_REFUSES_a_disease_reaching_the_refused_method(self):
        b = _batch()
        p = _find(b, P.CROPS[0], P.PM)
        p["control_ladder"].insert(1, {"method": "planting_time_avoidance",
                                       "note_beginner": "b", "note_seasoned": "s"})
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        # NAME THE GUARD. check_rounds_are_exercised runs BEFORE validate_batch, so the refusal
        # message is the one that must appear. Accepting "cannot reach type" as an alternative let
        # applies_to coherence answer for this guard and the mutation survived.
        self.assertIn("REFUSED", out)

    def test_check_REFUSES_a_batch_that_ignores_a_round(self):
        b = _batch()
        p = _find(b, P.CROPS[1], "thrips")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "weed_host_control"]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("weed_host_control", out)

    def test_check_REFUSES_when_a_round_has_not_landed(self):
        pre = _pre()
        del pre["control_methods"]["biofungicide"]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("catalog round must land first", out)


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
        _find(b, P.CROPS[0], "powdery-mildew")["id"] = "pea-powdery-mildew"
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
    """Refusals aimed at a problem NO read-fix and NO round pin covers, so an earlier guard cannot
    answer for them. Batch 5 shipped one of these masked."""

    def test_check_REFUSES_an_unknown_method(self):
        b = _batch()
        _find(b, P.CROPS[0], UNGUARDED)["control_ladder"][0]["method"] = "not_a_method"
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not in catalog", out)

    def test_check_REFUSES_a_tier_decrease(self):
        b = _batch()
        _find(b, P.CROPS[0], UNGUARDED)["control_ladder"].reverse()
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_check_REFUSES_an_empty_ladder(self):
        b = _batch()
        _find(b, P.CROPS[0], UNGUARDED)["control_ladder"] = []
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("EMPTY", out)

    def test_check_REFUSES_identical_registers(self):
        b = _batch()
        r = _find(b, P.CROPS[0], UNGUARDED)["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_check_REFUSES_a_duplicate_method(self):
        b = _batch()
        p = _find(b, P.CROPS[0], UNGUARDED)
        p["control_ladder"].append(copy.deepcopy(p["control_ladder"][-1]))
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("appears twice", out)

    def test_check_REFUSES_an_applies_to_incoherence(self):
        b = _batch()
        _find(b, P.CROPS[0], "fusarium-wilt")["control_ladder"][0]["method"] = "handpick"
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cannot reach type", out)

    def test_check_REFUSES_a_rung_count_drift(self):
        b = _batch()
        _find(b, P.CROPS[0], UNGUARDED)["control_ladder"].pop()
        with staged_as(b):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("rungs, expected", out)


class BlastRadius(unittest.TestCase):
    def test_no_crop_outside_the_two_changes(self):
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
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("touches only", out)

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
        d["source_catalog"]["usu_ext"]["accessed"] = "2099-01"
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_the_method_returning_after_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        for _, p in P.problems(_by(d)[P.CROPS[0]]):
            if p["id"] == P.PM:
                p["control_ladder"].append({"method": P.WFD, "note_beginner": "b",
                                            "note_seasoned": "s"})
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("regained", out)

    def test_verify_post_CATCHES_ascochyta_losing_it_after_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        for _, p in P.problems(_by(d)[P.CROPS[0]]):
            if p["id"] == P.ASC:
                p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != P.WFD]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("scoped to powdery mildew", out)

    def test_verify_post_CATCHES_two_crops_becoming_identical_at_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        by = _by(d)
        for fam in ("pests", "diseases"):
            for i, p in enumerate(by[P.CROPS[1]][fam]):
                p["control_ladder"] = copy.deepcopy(by[P.CROPS[0]][fam][i]["control_ladder"])
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("identical ladder CONTENT", out)

    def test_verify_post_CATCHES_a_dropped_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["crops"] = [c for c in d["crops"] if c.get("slug") != "tomatillo"]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

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

    def test_the_biofungicide_rung_sits_below_sulfur(self):
        """r7 chose `biological` over `soft_chemical` precisely so this ordering would hold."""
        by = _by(_post())
        for s in P.CROPS:
            m, _ = P.ladder_of(by[s], P.PM)
            self.assertIn("biofungicide", m)
            self.assertIn("sulfur", m)
            self.assertLess(m.index("biofungicide"), m.index("sulfur"), s)


if __name__ == "__main__":
    unittest.main(verbosity=2)
