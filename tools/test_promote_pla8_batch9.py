#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch9.py (THE ROOTS). Base 043a7272.

REPLAY-PINNED; the evidence is the mutation harness plus the refusal-spec drivers below.
`VerifyPostIsDriven` is FIRST, eighth time this arc.

Frozen literals: the id convention, the five divergence side-tables, the prompt_harvest uses and
the per-crop counts are restated here rather than derived from the promote's own tables.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch9 as P  # noqa: E402

POST_SHA = "4725bcbbe0cc78046b718c40bb5f97bdcd6638f7f55bec83e1ab465e1a5846f4"

CROPS = ("turnip", "radish", "carrot", "beet")
COUNTS = {"turnip": (9, 49), "radish": (7, 29), "carrot": (6, 24), "beet": (7, 32)}
PROMPT_USES = (("radish", "wireworms"), ("carrot", "carrot-rust-fly"), ("carrot", "cavity-spot"))
DAMPING = {"radish": 2, "carrot": 3, "beet": 3}


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


def _rung(m):
    return {"method": m, "note_beginner": "x", "note_seasoned": "y"}


class VerifyPostIsDriven(unittest.TestCase):
    def _staged(self):
        pre = _pre()
        return pre, P.snapshot(pre), _post(pre)

    def test_handpick_regained_on_leafminer_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "beet", "beet-spinach-leafminer")["control_ladder"].insert(3, _rung("handpick"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("wrong-meaning handpick", problem)

    def test_handpick_lost_where_it_belongs_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "turnip", "harlequin-bug")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "handpick"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("the drop was scoped", problem)

    def test_copper_lost_on_downy_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "beet", "downy-mildew")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "copper_fungicide"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("lost its copper rung", problem)

    def test_copper_gained_on_radish_alternaria_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "radish", "alternaria-leaf-spot")["control_ladder"].append(
            _rung("copper_fungicide"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("its prose refuses", problem)

    def test_spinosad_gained_on_beet_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "beet", "flea-beetles")["control_ladder"].append(_rung("spinosad"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("does not name", problem)

    def test_prompt_harvest_lost_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "carrot", "cavity-spot")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "prompt_harvest"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("lost prompt_harvest", problem)

    def test_singular_id_landing_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "beet", "flea-beetles")["id"] = "flea-beetle"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("singular flea-beetle", problem)

    def test_de_mention_landing_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "turnip", "clubroot")["control_ladder"][0]["note_seasoned"] += \
            " Ring with diatomaceous earth."
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("diatomaceous", problem)

    def test_empty_post_ladder_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "carrot", "aster-yellows")["control_ladder"] = []
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
        _crop(post, "spinach")["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("touches only", problem)

    def test_any_method_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["control_methods"]["prompt_harvest"]["best_use"] = "MUTATED"
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
        """ISOLATED. radish and beet both carry 7 problems, so a wholesale copy is well-formed,
        and every other post-side pin still passes under it EXCEPT the copper-on-downy pin (beet's
        downy slot inherits radish's damping-off ladder). That one is disabled for the duration so
        the content-identity guard is the one that must answer -- otherwise this driver never
        reaches it and the guard tests vacuously."""
        pre, snap, post = self._staged()
        src, dst = _crop(post, "radish"), _crop(post, "beet")
        for fam in ("pests", "diseases"):
            for a, b in zip(src[fam], dst[fam]):
                b["control_ladder"] = copy.deepcopy(a["control_ladder"])
        with _Patch("COPPER_DOWNY_YES", ()):
            problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
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
        batch, pre = P.staged(), _pre()
        for slug in CROPS:
            canon = P.problems(_crop(pre, slug))
            for idx, (_, p) in enumerate(P.problems(batch[slug])):
                self.assertEqual(p["id"], P.ID_CONVENTION[canon[idx][1].get("name")], slug)

    def test_beet_converged_to_the_plural(self):
        """Beet's problem NAME is singular; the roster id is the 14-crop plural."""
        pre = _pre()
        name = [p.get("name") for _, p in P.problems(_crop(pre, "beet"))
                if "lea" in (p.get("name") or "")]
        self.assertIn("Flea beetle", name)
        self.assertEqual(P.ID_CONVENTION["Flea beetle"], "flea-beetles")
        self.assertIn("flea-beetles", [p["id"] for _, p in P.problems(P.staged()["beet"])])

    def test_the_plural_is_the_roster_majority_and_swiss_chard_is_untouched(self):
        pre = _pre()
        plural = singular = 0
        for c in pre["crops"]:
            for _, p in P.problems(c):
                if p.get("id") == "flea-beetles":
                    plural += 1
                elif p.get("id") == "flea-beetle":
                    singular += 1
        self.assertGreaterEqual(plural, 14)
        self.assertEqual(singular, 1)
        post = _post()
        sc = [p.get("id") for _, p in P.problems(_crop(post, "swiss-chard"))]
        self.assertIn("flea-beetle", sc, "swiss-chard's shipped join key must not be re-derived")

    def test_singular_anywhere_in_the_batch_is_refused(self):
        def mutate(batch):
            for _, p in P.problems(batch["beet"]):
                if p["id"] == "flea-beetles":
                    p["id"] = "flea-beetle"
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        # the ID_CONVENTION loop owns this refusal; a second singular-specific check in check()
        # would be dead code below it, so the promote deliberately has none.
        self.assertIn("join keys", problem)

    def test_unknown_problem_name_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "carrot"))[0][1]["name"] = "Mystery pest"
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

    def test_handpick_on_leafminer_is_refused(self):
        def add(batch):
            for _, p in P.problems(batch["beet"]):
                if p["id"] == "beet-spinach-leafminer":
                    p["control_ladder"].insert(3, _rung("handpick"))
        problem = self._with(add)
        self.assertIsNotNone(problem)
        self.assertIn("not handpickable", problem)

    def test_leafminer_losing_sanitation_is_refused(self):
        def drop(batch):
            for _, p in P.problems(batch["beet"]):
                if p["id"] == "beet-spinach-leafminer":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "garden_sanitation"]
        problem = self._with(drop)
        self.assertIsNotNone(problem)
        self.assertIn("where removing mined leaves belongs", problem)

    def test_handpick_dropped_from_harlequin_bug_is_refused(self):
        def drop(batch):
            for _, p in P.problems(batch["turnip"]):
                if p["id"] == "harlequin-bug":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "handpick"]
        problem = self._with(drop)
        self.assertIsNotNone(problem)
        self.assertIn("not a blanket removal", problem)

    def test_each_divergence_is_refused_in_both_directions(self):
        cases = [
            ("turnip", "alternaria-leaf-spot", "copper_fungicide", "drop", "its prose names copper"),
            ("radish", "alternaria-leaf-spot", "copper_fungicide", "add", "grow faster"),
            ("turnip", "downy-mildew", "copper_fungicide", "drop", "last "),
            ("beet", "downy-mildew", "copper_fungicide", "drop", "last "),
            ("turnip", "flea-beetles", "spinosad", "drop", "prose names it"),
            ("radish", "flea-beetles", "spinosad", "drop", "prose names it"),
            ("beet", "flea-beetles", "spinosad", "add", "stops at kaolin clay"),
            ("turnip", "aphids", "garden_sanitation", "drop", "own prose supports"),
            ("beet", "aphids", "garden_sanitation", "add", "does not carry it"),
        ]
        for slug, pid, method, op, msg in cases:
            def mutate(batch, slug=slug, pid=pid, method=method, op=op):
                for _, p in P.problems(batch[slug]):
                    if p["id"] == pid:
                        if op == "drop":
                            p["control_ladder"] = [r for r in p["control_ladder"]
                                                   if r["method"] != method]
                        else:
                            p["control_ladder"].append(_rung(method))
            problem = self._with(mutate)
            self.assertIsNotNone(problem, f"{slug}/{pid} {op} {method} passed")
            self.assertIn(msg, problem, f"{slug}/{pid}: wrong refusal -- {problem}")

    def test_damping_off_rung_counts_are_pinned(self):
        for slug in DAMPING:
            def mutate(batch, slug=slug):
                for _, p in P.problems(batch[slug]):
                    if p["id"] == "damping-off":
                        p["control_ladder"].append(_rung("crop_rotation"))
            problem = self._with(mutate)
            self.assertIsNotNone(problem, slug)
            self.assertIn("re-sows bare spots", problem)

    def test_each_prompt_harvest_use_is_pinned(self):
        for slug, pid in PROMPT_USES:
            def mutate(batch, slug=slug, pid=pid):
                for _, p in P.problems(batch[slug]):
                    if p["id"] == pid:
                        p["control_ladder"] = [r for r in p["control_ladder"]
                                               if r["method"] != "prompt_harvest"]
            problem = self._with(mutate)
            self.assertIsNotNone(problem, f"{slug}/{pid}")
            self.assertIn("harvest promptly", problem)

    def test_prompt_harvest_uses_match_the_frozen_list(self):
        self.assertEqual(tuple(P.PROMPT_HARVEST_USES), PROMPT_USES)
        batch = P.staged()
        for slug, pid in PROMPT_USES:
            ms, _ = P.ladder_of(batch[slug], pid)
            self.assertIn("prompt_harvest", ms, f"{slug}/{pid}")

    def test_neem_or_soap_on_flea_beetles_is_refused(self):
        for m in ("neem_oil", "insecticidal_soap"):
            def mutate(batch, m=m):
                for _, p in P.problems(batch["turnip"]):
                    if p["id"] == "flea-beetles":
                        p["control_ladder"].append(_rung(m))
            problem = self._with(mutate)
            self.assertIsNotNone(problem, m)
            self.assertIn("bottom_watering shape", problem)

    def test_de_mention_is_refused(self):
        def add(batch):
            P.problems(batch["carrot"])[0][1]["control_ladder"][0]["note_beginner"] += \
                " Dust with diatomaceous earth."
        problem = self._with(add)
        self.assertIsNotNone(problem)
        self.assertIn("deliberately-unminted", problem)


class TwinsAndPremises(unittest.TestCase):
    def test_identical_canonical_prose_is_refused(self):
        pre = _pre()
        a, b = _crop(pre, "radish"), _crop(pre, "beet")
        for fam in ("pests", "diseases"):
            for pa, pb in zip(a[fam], b[fam]):
                for f in P.PROSE_FIELDS:
                    pb[f] = copy.deepcopy(pa.get(f))
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("TRUE TWIN", problem)

    def test_identical_staged_bytes_are_refused(self):
        dg = P.staged_digests()
        dg["beet"] = dg["radish"]
        with _Patch("staged_digests", lambda: dg):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("copied", problem)

    def test_all_pairs_have_distinct_staged_bytes(self):
        dg = list(P.staged_digests().values())
        self.assertEqual(len(dg), len(set(dg)))

    def test_prompt_harvest_premise_is_refused_when_the_meaning_moves(self):
        pre = _pre()
        pre["control_methods"]["prompt_harvest"]["best_use"] = "Fruit crops only."
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("harvest-sooner action", problem)

    def test_spinosad_premise_is_refused(self):
        pre = _pre()
        cm = pre["control_methods"]["spinosad"]
        cm["cautions"] = [c.replace("dusk", "dawn") for c in cm["cautions"]]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("dusk caution", problem)

    def test_pre_state_carries_both_premises(self):
        cm = _pre()["control_methods"]
        self.assertIn("dusk", " ".join(cm["spinosad"]["cautions"]))
        self.assertIn("sooner", cm["prompt_harvest"]["best_use"])

    def test_already_laddered_crop_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "carrot"))[0][1]["control_ladder"] = []
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already laddered", problem)


class Validate(unittest.TestCase):
    def _with(self, mutator):
        with _Patch("staged", _staged_with(mutator)):
            return P.check(_pre())

    def test_unknown_method_is_refused(self):
        def m(batch):
            P.problems(batch["carrot"])[0][1]["control_ladder"][0]["method"] = "ghost"
        self.assertIn("not in catalog", self._with(m))

    def test_tier_decrease_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["turnip"]):
                if p["id"] == "aphids":
                    lad = p["control_ladder"]
                    lad.insert(0, lad.pop())
        self.assertIn("tiers decrease", self._with(m))

    def test_applies_to_incoherence_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["carrot"]):
                if p["id"] == "root-knot-nematode":
                    p["control_ladder"].append(_rung("bt"))
        self.assertIn("cannot reach type", self._with(m))

    def test_identical_registers_are_refused(self):
        def m(batch):
            r = P.problems(batch["carrot"])[0][1]["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        self.assertIn("registers are identical", self._with(m))

    def test_empty_ladder_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["carrot"]):
                if p["id"] == "aster-yellows":
                    p["control_ladder"] = []
        self.assertIn("EMPTY", self._with(m))

    def test_duplicate_method_is_refused(self):
        def m(batch):
            lad = P.problems(batch["carrot"])[0][1]["control_ladder"]
            lad.append(copy.deepcopy(lad[-1]))
        self.assertIn("appears twice", self._with(m))

    def test_missing_register_is_refused(self):
        def m(batch):
            P.problems(batch["carrot"])[0][1]["control_ladder"][0]["note_beginner"] = " "
        self.assertIn("missing or empty", self._with(m))

    def test_rung_count_drift_is_refused(self):
        """On turnip/clubroot, an all-cultural ladder: appending another cultural method keeps
        tiers non-decreasing and applies_to legal, so only the count check can object."""
        def m(batch):
            for _, p in P.problems(batch["turnip"]):
                if p["id"] == "clubroot":
                    p["control_ladder"].append(_rung("resistant_varieties"))
        self.assertIn("rungs, expected", self._with(m))


class ReadRecord(unittest.TestCase):
    """Pins recording what the read verified, so a later pass cannot quietly drift it."""

    def test_divergence_tables_are_the_frozen_literals(self):
        self.assertEqual(tuple(P.COPPER_ALTERNARIA_YES), ("turnip",))
        self.assertEqual(tuple(P.COPPER_ALTERNARIA_NO), ("radish",))
        self.assertEqual(tuple(P.COPPER_DOWNY_YES), ("turnip", "beet"))
        self.assertEqual(tuple(P.SPINOSAD_FB_YES), ("turnip", "radish"))
        self.assertEqual(tuple(P.SPINOSAD_FB_NO), ("beet",))
        self.assertEqual(dict(P.DAMPING_OFF_RUNGS), DAMPING)

    def test_kaolin_is_beets_terminal_flea_rung(self):
        ms, _ = P.ladder_of(P.staged()["beet"], "flea-beetles")
        self.assertEqual(ms[-1], "kaolin_clay")

    def test_no_conventional_rung_anywhere_in_the_batch(self):
        """No root crop's prose names a conventional material; the ladders stop softer."""
        cm = _pre()["control_methods"]
        batch = P.staged()
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                for r in p["control_ladder"]:
                    self.assertNotEqual(cm[r["method"]]["tier"], "conventional",
                                        f"{slug}/{p['id']}/{r['method']}")

    def test_wireworms_and_scab_are_genuinely_new_ids(self):
        pre = _pre()
        existing = {p.get("id") for c in pre["crops"] for _, p in P.problems(c) if p.get("id")}
        for pid in ("wireworms", "common-scab", "aster-yellows", "cavity-spot",
                    "carrot-leaf-blight"):
            self.assertNotIn(pid, existing, f"{pid} was claimed new but ships already")


if __name__ == "__main__":
    unittest.main(verbosity=2)
