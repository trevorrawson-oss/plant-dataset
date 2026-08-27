#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch8.py (THE LEAFY GREENS). Base f8678ade.

REPLAY-PINNED; the evidence is the mutation harness plus the refusal-spec drivers below.
`VerifyPostIsDriven` is FIRST, seventh time this arc: every post-state guard gets an input that
doctors the APPLIED post directly, since check() refuses everything upstream.

Staged-side refusal tests monkeypatch P.staged / P.staged_digests with doctored copies.

Frozen literals: the id-convention table, the copper-split sides, the two normalized orders, and
the per-crop counts are restated here as constants, not derived from the promote's tables.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch8 as P  # noqa: E402

POST_SHA = "043a7272e76d640f287df420d319f209de8bd4443ffa75d327175958bf3b76e0"

CROPS = ("spinach", "arugula", "lettuce-leaf", "bok-choy")
COUNTS = {"spinach": (8, 36), "arugula": (8, 40), "lettuce-leaf": (5, 20), "bok-choy": (11, 57)}
COPPER_YES = ("lettuce-leaf", "bok-choy")
COPPER_NO = ("spinach", "arugula")
WR_ORDER = ("resistant_varieties", "crop_rotation", "airflow_spacing", "water_at_the_base",
            "garden_sanitation")
DO_ORDER = ("sound_sowing_practice", "improve_drainage", "garden_sanitation")
REUSED_IDS = {"beet-spinach-leafminer": "swiss-chard", "cabbage-root-maggot": "broccoli",
              "clubroot": "broccoli", "black-rot": "broccoli", "cabbageworms": "broccoli"}


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _crop(data, slug):
    return next(c for c in data["crops"] if c.get("slug") == slug)


def _prob(data, slug, pid):
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("id") == pid:
                return p
    raise AssertionError(f"{slug}/{pid} not found")


class _Patch:
    def __init__(self, name, value):
        self.n, self.v = name, value

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(P, self.n, self.old)
        return False


def _staged_with(mutator):
    batch = P.staged()
    mutator(batch)
    return lambda: batch


class VerifyPostIsDriven(unittest.TestCase):
    def _staged(self):
        pre = _pre()
        return pre, P.snapshot(pre), _post(pre)

    def test_copper_lost_where_required_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "lettuce-leaf", "downy-mildew")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "copper_fungicide"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("lost its copper rung", problem)

    def test_copper_gained_where_ruled_out_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "spinach", "downy-mildew")["control_ladder"].append(
            {"method": "copper_fungicide", "note_beginner": "x", "note_seasoned": "y"})
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("gained a copper rung the read ruled out", problem)

    def test_lettuce_rotation_gain_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "lettuce-leaf", "downy-mildew")["control_ladder"].insert(
            0, {"method": "crop_rotation", "note_beginner": "x", "note_seasoned": "y"})
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("prose contradicts", problem)

    def test_neem_regained_on_flea_beetles_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "bok-choy", "flea-beetles")["control_ladder"].append(
            {"method": "neem_oil", "note_beginner": "x", "note_seasoned": "y"})
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("regained neem_oil", problem)

    def test_de_mention_landing_is_caught(self):
        pre, snap, post = self._staged()
        r = _prob(post, "lettuce-leaf", "slugs-and-snails")["control_ladder"][2]
        r["note_seasoned"] += " A diatomaceous earth ring helps too."
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("diatomaceous", problem)

    def test_white_rust_order_drift_is_caught(self):
        pre, snap, post = self._staged()
        lad = _prob(post, "arugula", "white-rust")["control_ladder"]
        lad[0], lad[1] = lad[1], lad[0]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("drifted from the normalized order", problem)

    def test_empty_post_ladder_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "spinach", "fusarium-wilt")["control_ladder"] = []
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("no ladder after promote", problem)

    def test_added_crop_is_caught_set_equality_first(self):
        pre, snap, post = self._staged()
        ghost = copy.deepcopy(post["crops"][0])
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("crop set changed", problem)

    def test_bystander_crop_edit_is_caught(self):
        pre, snap, post = self._staged()
        _crop(post, "beefsteak-tomato")["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("touches only", problem)

    def test_any_method_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["control_methods"]["copper_fungicide"]["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("control_methods changed", problem)

    def test_source_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["source_catalog"]["umn_ext"]["tier"] = "T2"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("source_catalog changed", problem)

    def test_identical_ladder_content_is_caught(self):
        """spinach and arugula share problem count (8), so a full ladder copy is well-formed
        and only the content guard can object -- but the copy also flips the copper split, so
        the SPECIFIC message asserted is whichever substantive guard answers first."""
        pre, snap, post = self._staged()
        src, dst = _crop(post, "spinach"), _crop(post, "arugula")
        for fam in ("pests", "diseases"):
            for a, b in zip(src[fam], dst[fam]):
                b["control_ladder"] = copy.deepcopy(a["control_ladder"])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)

    def test_content_identity_guard_has_its_own_driver(self):
        """Drive ONLY the content guard: mirror one crop's ladders onto itself in pre-snapshot
        space is impossible, so instead copy arugula onto spinach AND fix up the copper/rotation
        pins so nothing else objects; what remains is the identity check."""
        pre, snap, post = self._staged()
        src, dst = _crop(post, "arugula"), _crop(post, "spinach")
        for fam in ("pests", "diseases"):
            for a, b in zip(src[fam], dst[fam]):
                b["control_ladder"] = copy.deepcopy(a["control_ladder"])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        # arugula's ladders satisfy every copper/rotation/DE pin for spinach's problem set too
        # (same ids, no copper on downy), so the identity guard is what fires.
        self.assertIn("identical ladder CONTENT", problem)


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

    def test_counts(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(len(post["crops"]), len(pre["crops"]))
        self.assertEqual(post["control_methods"], pre["control_methods"])
        self.assertEqual(post["source_catalog"], pre["source_catalog"])
        for slug, (n_prob, n_rungs) in COUNTS.items():
            probs = P.problems(_crop(post, slug))
            self.assertEqual(len(probs), n_prob, slug)
            self.assertEqual(sum(len(p["control_ladder"]) for _, p in probs), n_rungs, slug)

    def test_clean_promote_passes_both_phases(self):
        pre = _pre()
        self.assertIsNone(P.check(pre))
        p = copy.deepcopy(pre)
        P.apply_to(p)
        self.assertIsNone(P.verify_post(P.snapshot(pre), p))

    def test_expected_tables_match_the_frozen_counts(self):
        for slug, (n_prob, n_rungs) in COUNTS.items():
            self.assertEqual(P.EXPECTED_PROBLEMS[slug], n_prob)
            self.assertEqual(P.EXPECTED_RUNGS[slug], n_rungs)
        self.assertEqual(set(P.CROPS), set(CROPS))


class IdConvention(unittest.TestCase):
    def test_every_staged_id_is_on_convention(self):
        batch = P.staged()
        pre = _pre()
        for slug in CROPS:
            canon = P.problems(_crop(pre, slug))
            for idx, (_, p) in enumerate(P.problems(batch[slug])):
                name = canon[idx][1].get("name")
                self.assertEqual(p["id"], P.ID_CONVENTION[name], f"{slug}/{name}")

    def test_reused_ids_really_ship_on_their_precedent_crops(self):
        """The reuse claims are verified against the live roster, not asserted."""
        pre = _pre()
        for pid, precedent in REUSED_IDS.items():
            ids = [p.get("id") for _, p in P.problems(_crop(pre, precedent))]
            self.assertIn(pid, ids, f"{precedent} does not ship {pid}")

    def test_cabbage_aphids_is_distinct_from_aphids_by_design(self):
        """The Brevicoryne-specialist entry mints its own id (the two-spotted-spider-mite
        precedent); generic `aphids` ships on spinach, arugula and lettuce in this same batch."""
        batch = P.staged()
        bc = [p["id"] for _, p in P.problems(batch["bok-choy"])]
        self.assertIn("cabbage-aphids", bc)
        self.assertNotIn("aphids", bc)
        for slug in ("spinach", "arugula", "lettuce-leaf"):
            self.assertIn("aphids", [p["id"] for _, p in P.problems(batch[slug])])

    def test_divergent_id_is_refused_by_name(self):
        def mutate(batch):
            P.problems(batch["spinach"])[0][1]["id"] = "spinach-leafminer"
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("join keys", problem)

    def test_unknown_problem_name_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "spinach"))[0][1]["name"] = "Mystery pest"
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("id-convention table", problem)


class ReadFixes(unittest.TestCase):
    def _with(self, mutator):
        with _Patch("staged", _staged_with(mutator)):
            return P.check(_pre())

    def test_clean_staged_files_pass(self):
        self.assertIsNone(P.check_read_fixes(P.staged(),
                                             {c["slug"]: c for c in _pre()["crops"]}))

    def test_copper_split_is_refused_in_both_directions(self):
        def drop(batch):
            for _, p in P.problems(batch["bok-choy"]):
                if p["id"] == "downy-mildew":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "copper_fungicide"]
        problem = self._with(drop)
        self.assertIsNotNone(problem)
        self.assertIn("recommends preventive copper", problem)

        def add(batch):
            for _, p in P.problems(batch["arugula"]):
                if p["id"] == "downy-mildew":
                    p["control_ladder"].append({"method": "copper_fungicide",
                                                "note_beginner": "x", "note_seasoned": "y"})
        problem = self._with(add)
        self.assertIsNotNone(problem)
        self.assertIn("the read dropped it", problem)

    def test_lettuce_rotation_is_refused(self):
        def add(batch):
            for _, p in P.problems(batch["lettuce-leaf"]):
                if p["id"] == "downy-mildew":
                    p["control_ladder"].insert(0, {"method": "crop_rotation",
                                                   "note_beginner": "x", "note_seasoned": "y"})
        problem = self._with(add)
        self.assertIsNotNone(problem)
        self.assertIn("does not survive in the soil", problem)

    def test_spinach_losing_rotation_is_refused(self):
        def drop(batch):
            for _, p in P.problems(batch["spinach"]):
                if p["id"] == "downy-mildew":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "crop_rotation"]
        problem = self._with(drop)
        self.assertIsNotNone(problem)
        self.assertIn("oospores", problem)

    def test_de_mention_is_refused(self):
        def add(batch):
            r = P.problems(batch["arugula"])[0][1]["control_ladder"][0]
            r["note_beginner"] += " Ring the plants with diatomaceous earth."
        problem = self._with(add)
        self.assertIsNotNone(problem)
        self.assertIn("deliberately-unminted", problem)

    def test_neem_on_flea_beetles_is_refused(self):
        def add(batch):
            for _, p in P.problems(batch["spinach"]):
                if p["id"] == "flea-beetles":
                    p["control_ladder"].append({"method": "neem_oil",
                                                "note_beginner": "x", "note_seasoned": "y"})
        problem = self._with(add)
        self.assertIsNotNone(problem)
        self.assertIn("bottom_watering shape", problem)

    def test_flea_beetles_losing_row_cover_is_refused(self):
        def drop(batch):
            for _, p in P.problems(batch["bok-choy"]):
                if p["id"] == "flea-beetles":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "floating_row_cover"]
        problem = self._with(drop)
        self.assertIsNotNone(problem)
        self.assertIn("best single defense", problem)

    def test_white_rust_order_is_refused_when_scrambled(self):
        def scramble(batch):
            for _, p in P.problems(batch["spinach"]):
                if p["id"] == "white-rust":
                    p["control_ladder"] = list(reversed(p["control_ladder"]))
        problem = self._with(scramble)
        self.assertIsNotNone(problem)
        self.assertIn("normalized shared order", problem)

    def test_damping_off_order_is_refused_when_scrambled(self):
        def scramble(batch):
            for _, p in P.problems(batch["arugula"]):
                if p["id"] == "damping-off":
                    lad = p["control_ladder"]
                    lad[0], lad[1] = lad[1], lad[0]
        problem = self._with(scramble)
        self.assertIsNotNone(problem)
        self.assertIn("sowing-first order", problem)

    def test_bok_choy_losing_hort_oil_is_refused(self):
        def drop(batch):
            for _, p in P.problems(batch["bok-choy"]):
                if p["id"] == "cabbage-aphids":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "horticultural_oil"]
        problem = self._with(drop)
        self.assertIsNotNone(problem)
        self.assertIn("its own prose names", problem)


class TwinsAndPremises(unittest.TestCase):
    def test_identical_canonical_prose_is_refused(self):
        pre = _pre()
        a, b = _crop(pre, "spinach"), _crop(pre, "arugula")
        for fam in ("pests", "diseases"):
            for pa, pb in zip(a[fam], b[fam]):
                for f in P.PROSE_FIELDS:
                    pb[f] = copy.deepcopy(pa.get(f))
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("TRUE TWIN", problem)

    def test_identical_staged_bytes_are_refused(self):
        dg = P.staged_digests()
        dg["arugula"] = dg["spinach"]
        with _Patch("staged_digests", lambda: dg):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("copied", problem)

    def test_all_six_pairs_have_distinct_staged_bytes(self):
        dg = list(P.staged_digests().values())
        self.assertEqual(len(dg), len(set(dg)))

    def test_missing_spinosad_premise_is_refused(self):
        pre = _pre()
        cm = pre["control_methods"]["spinosad"]
        cm["cautions"] = [c.replace("dusk", "dawn") for c in cm["cautions"]]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("dusk caution", problem)

    def test_missing_neem_band_premise_is_refused(self):
        pre = _pre()
        cm = pre["control_methods"]["neem_oil"]
        cm["cautions"] = [c.replace("sunset", "dawn") for c in cm["cautions"]]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("medium-band bee caution", problem)

    def test_pre_state_actually_carries_both_premises(self):
        cm = _pre()["control_methods"]
        self.assertIn("dusk", " ".join(cm["spinosad"]["cautions"]))
        blob = " ".join(cm["neem_oil"]["cautions"])
        self.assertIn("sunset", blob)
        self.assertIn("midnight", blob)

    def test_already_laddered_crop_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "spinach"))[0][1]["control_ladder"] = []
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already laddered", problem)


class Validate(unittest.TestCase):
    def _with(self, mutator):
        with _Patch("staged", _staged_with(mutator)):
            return P.check(_pre())

    def test_unknown_method_is_refused(self):
        def m(batch):
            P.problems(batch["spinach"])[0][1]["control_ladder"][0]["method"] = "ghost"
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("not in catalog", problem)

    def test_tier_decrease_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["spinach"]):
                if p["id"] == "aphids":
                    lad = p["control_ladder"]
                    lad.insert(0, lad.pop())
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("tiers decrease", problem)

    def test_applies_to_incoherence_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["lettuce-leaf"]):
                if p["id"] == "tipburn":
                    p["control_ladder"].append({"method": "bt",
                                                "note_beginner": "x", "note_seasoned": "y"})
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("cannot reach type", problem)

    def test_identical_registers_are_refused(self):
        def m(batch):
            r = P.problems(batch["spinach"])[0][1]["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("registers are identical", problem)

    def test_empty_ladder_is_refused(self):
        """On fusarium-wilt, a problem no read pin covers, so only the EMPTY check can object."""
        def m(batch):
            for _, p in P.problems(batch["spinach"]):
                if p["id"] == "fusarium-wilt":
                    p["control_ladder"] = []
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("EMPTY", problem)

    def test_duplicate_method_is_refused(self):
        def m(batch):
            lad = P.problems(batch["spinach"])[0][1]["control_ladder"]
            lad.append(copy.deepcopy(lad[-1]))
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("appears twice", problem)

    def test_missing_register_is_refused(self):
        def m(batch):
            P.problems(batch["spinach"])[0][1]["control_ladder"][0]["note_beginner"] = " "
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("missing or empty", problem)

    def test_rung_count_drift_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["spinach"]):
                if p["id"] == "fusarium-wilt":
                    p["control_ladder"].append({"method": "improve_drainage",
                                                "note_beginner": "x", "note_seasoned": "y"})
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("rungs, expected", problem)


class ReadRecord(unittest.TestCase):
    """Pins that record what the read verified, so a later pass cannot quietly drift it."""

    def test_copper_split_tables_are_the_frozen_literals(self):
        self.assertEqual(tuple(P.COPPER_ON_DM), COPPER_YES)
        self.assertEqual(tuple(P.NO_COPPER_ON_DM), COPPER_NO)
        self.assertEqual(tuple(P.WHITE_RUST_ORDER), WR_ORDER)
        self.assertEqual(tuple(P.DAMPING_OFF_ORDER), DO_ORDER)

    def test_iron_phosphate_rungs_stay_comparative(self):
        """Every iron-phosphate rung hedges relative to metaldehyde, never absolutely."""
        batch = P.staged()
        found = 0
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                for r in p.get("control_ladder") or []:
                    if r["method"] == "iron_phosphate_slug_bait":
                        found += 1
                        blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                        self.assertIn("metaldehyde", blob, f"{slug}/{p['id']}")
                        self.assertIn("pesticide", blob, f"{slug}/{p['id']}")
                        self.assertNotIn("pet-safe", blob)
                        self.assertNotIn("safe around pets", blob)
        self.assertEqual(found, 3, "expected the three slug-carrying crops to bait")

    def test_spinosad_rungs_carry_the_dusk_timing(self):
        """The medium-band allowance the chemical-cohort round validated."""
        batch = P.staged()
        found = 0
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                for r in p.get("control_ladder") or []:
                    if r["method"] == "spinosad":
                        found += 1
                        blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                        self.assertIn("dusk", blob, f"{slug}/{p['id']}")
        self.assertGreaterEqual(found, 5)

    def test_lettuce_has_no_flea_beetles_and_thats_the_source(self):
        """The FB loop's `continue` branch is real: lettuce carries no flea-beetles problem."""
        self.assertIsNone(P.ladder_of(P.staged()["lettuce-leaf"], "flea-beetles")[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
