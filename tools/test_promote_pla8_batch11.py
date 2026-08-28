#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch11.py (ALLIUMS + FALL HERBS). Base 96cbc68c (re-pinned 2026-08-28 off the trap_cropping backfill).

REPLAY-PINNED; the evidence is the mutation harness plus the refusal-spec drivers.
`VerifyPostIsDriven` is FIRST, tenth time this arc.

`SchemaCoverage` is the novel family, and its rationale was CORRECTED by its own test. This is the
first MIXED-SCHEMA batch: garlic and spring-onion carry `identification_*`/`management_*` prose,
dill and cilantro the classic set. The first version of this guard claimed a classic-only
`PROSE_FIELDS` would make `prose_signature` all-None for the alliums -- it does not, because
`name` and `cause_*` exist in BOTH schemas, and the test proved it by refusing to fail. What a
classic-only list actually loses is the ADVICE half of each record, which is the half the ladders
are built from and the half where two crops of one family differ. The guard now requires per-crop
coverage of advice-bearing fields, and a second test pins the corrected reasoning so nobody
restores the wrong one.

Frozen literals: the id convention, the shared-allium ids, the widening's three parts and the
per-crop counts are restated here rather than derived from the promote's own tables.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch11 as P  # noqa: E402

POST_SHA = "1e4d0c06ad28ed28642f64a3ae15b537bb7d14367b73280489ebde3befd311ae"

CROPS = ("garlic", "spring-onion", "dill", "cilantro-coriander")
COUNTS = {"garlic": (7, 21), "spring-onion": (6, 16), "dill": (5, 19),
          "cilantro-coriander": (6, 25)}
SHARED_ALLIUM = ("onion-thrips", "onion-maggot", "white-rot", "fusarium-basal-rot",
                 "botrytis-neck-rot")
NEW_IDS = ("allium-leafminer", "bacterial-leaf-spot", "botrytis-neck-rot", "fusarium-basal-rot",
           "garlic-rust", "leafhoppers", "onion-maggot", "onion-thrips", "parsleyworm",
           "stem-and-bulb-nematode", "white-rot")
CLASSIC_ONLY = ("name", "symptoms_beginner", "symptoms_seasoned", "cause_beginner",
                "cause_seasoned", "organic_treatment_beginner", "organic_treatment_seasoned",
                "prevention_beginner", "prevention_seasoned", "severity", "sources")


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

    def test_widening_applies_to_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        m = post["control_methods"][P.WIDEN_KEY]
        m["applies_to"] = [a for a in m["applies_to"] if a != P.WIDEN_ADD]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("does not reach", problem)

    def test_widening_best_use_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        post["control_methods"][P.WIDEN_KEY]["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("best_use did not take the widened prose", problem)

    def test_widening_seasoned_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        m = post["control_methods"][P.WIDEN_KEY]
        m["how_it_works_seasoned"] = m["how_it_works_seasoned"][:-40]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("how_it_works_seasoned did not take", problem)

    def test_garlic_clean_stock_rung_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        p = _prob(post, "garlic", P.NEMATODE)
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != P.WIDEN_KEY]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("lost its leading", problem)

    def test_cilantro_copper_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "cilantro-coriander", "bacterial-leaf-spot")["control_ladder"].append(
            _rung("copper_fungicide"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("the read ruled out", problem)

    def test_split_allium_id_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "spring-onion", "onion-thrips")["id"] = "thrips-onion"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("split id", problem)

    def test_timing_rung_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "spring-onion", "allium-leafminer")["control_ladder"].insert(
            0, _rung("planting_time_avoidance"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("unearned timing rung", problem)

    def test_handpick_scoping_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "garlic", "garlic-rust")["control_ladder"].insert(0, _rung("handpick"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("leaf-removal target", problem)

    def test_unminted_method_in_a_note_guard_runs_on_the_post(self):
        for word in ("diatomaceous earth", "trap crop"):
            pre, snap, post = self._staged()
            _prob(post, "dill", "aphids")["control_ladder"][0]["note_seasoned"] += f" Use a {word}."
            problem = P.verify_post(snap, post)
            self.assertIsNotNone(problem, word)
            self.assertIn("unminted method reached a note", problem)

    def test_empty_post_ladder_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "garlic", "botrytis-neck-rot")["control_ladder"] = []
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

    def test_added_method_is_caught(self):
        pre, snap, post = self._staged()
        post["control_methods"]["ghost"] = copy.deepcopy(post["control_methods"]["handpick"])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("gained or lost a key", problem)

    def test_bystander_crop_edit_is_caught(self):
        pre, snap, post = self._staged()
        _crop(post, "cabbage")["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("touches only", problem)

    def test_bystander_method_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["control_methods"]["crop_rotation"]["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("bystander method", problem)

    def test_source_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["source_catalog"]["umn_ext"]["tier"] = "T2"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("source_catalog changed", problem)


class SchemaCoverage(unittest.TestCase):
    """The first mixed-schema batch. Without this the twins check silently compares nothing."""

    def test_the_two_alliums_use_the_newer_schema(self):
        pre = _pre()
        for slug in ("garlic", "spring-onion"):
            fields = set()
            for _, p in P.problems(_crop(pre, slug)):
                fields |= set(p.keys())
            self.assertIn("management_seasoned", fields, slug)
            self.assertNotIn("organic_treatment_seasoned", fields, slug)

    def test_the_two_herbs_use_the_classic_schema(self):
        pre = _pre()
        for slug in ("dill", "cilantro-coriander"):
            fields = set()
            for _, p in P.problems(_crop(pre, slug)):
                fields |= set(p.keys())
            self.assertIn("organic_treatment_seasoned", fields, slug)
            self.assertNotIn("management_seasoned", fields, slug)

    def test_prose_fields_spans_both_schemas(self):
        self.assertIn("management_seasoned", P.PROSE_FIELDS)
        self.assertIn("organic_treatment_seasoned", P.PROSE_FIELDS)

    def test_a_classic_only_field_list_is_refused(self):
        """THE POINT, corrected. `cause_*` and `name` exist in BOTH schemas, so a classic-only
        list does not go silently vacuous -- it keeps comparing those. What it stops comparing is
        the ADVICE half the ladders are built from, which is where two crops of one family
        differ. The guard requires per-crop coverage of advice-bearing fields."""
        with _Patch("PROSE_FIELDS", CLASSIC_ONLY):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("advice-bearing fields", problem)

    def test_a_classic_only_list_is_NOT_silently_vacuous(self):
        """Pins the corrected reasoning: the shared fields still produce a signature, which is
        why the guard checks advice coverage rather than emptiness."""
        pre = _pre()
        with _Patch("PROSE_FIELDS", CLASSIC_ONLY):
            sig = P.prose_signature(_crop(pre, "garlic"))
        self.assertTrue(any(v not in (None, "null") for row in sig for v in row))

    def test_a_record_with_no_advice_field_is_refused(self):
        """Drives the `not own_advice` branch, which real data never reaches."""
        pre = _pre()
        for _, p in P.problems(_crop(pre, "garlic")):
            for f in P.ADVICE_FIELDS:
                p.pop(f, None)
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("record shape is unexpected", problem)

    def test_an_allium_losing_the_new_schema_is_refused(self):
        """Drives the NEW_SCHEMA_CROPS expectation, also unreachable on real data."""
        pre = _pre()
        for _, p in P.problems(_crop(pre, "spring-onion")):
            p["organic_treatment_seasoned"] = p.pop("management_seasoned", "x")
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("identification_/management_ schema", problem)

    def test_signatures_are_non_empty_for_every_crop(self):
        pre = _pre()
        for slug in CROPS:
            sig = P.prose_signature(_crop(pre, slug))
            self.assertTrue(sig, slug)
            for row in sig:
                self.assertTrue(any(v not in (None, "null") for v in row), slug)


class TheWidening(unittest.TestCase):
    def test_premise_the_method_did_not_reach_nematode(self):
        """RED on the shipped canonical: garlic's primary control was unplaceable."""
        cm = _pre()["control_methods"][P.WIDEN_KEY]
        self.assertNotIn("nematode", cm["applies_to"])
        self.assertNotIn("nematode", cm["best_use"].lower())

    def test_only_five_methods_reached_nematode_before(self):
        from control_ladder_gate import TYPE_TARGETS
        cm = _pre()["control_methods"]
        legal = [k for k, v in cm.items()
                 if "any" in v["applies_to"]
                 or set(v["applies_to"]) & set(TYPE_TARGETS.get("nematode", []))]
        self.assertEqual(len(legal), 5)
        self.assertNotIn(P.WIDEN_KEY, legal)

    def test_post_state_reaches_nematode_with_its_prose(self):
        m = _post()["control_methods"][P.WIDEN_KEY]
        self.assertIn("nematode", m["applies_to"])
        self.assertIn("nematodes that ride inside seed cloves", m["best_use"])
        self.assertIn("stem and bulb nematode arrives inside infected garlic cloves",
                      m["how_it_works_seasoned"])

    def test_garlic_takes_the_rung_and_it_leads(self):
        lad = [r["method"] for r in _prob(_post(), "garlic", P.NEMATODE)["control_ladder"]]
        self.assertEqual(lad[0], P.WIDEN_KEY)

    def test_the_rung_keeps_the_retired_practice_retired(self):
        """The prose withdraws hot-water dips; a rung must not resurrect them."""
        p = _prob(_post(), "garlic", P.NEMATODE)
        blob = " ".join(r["note_beginner"] + " " + r["note_seasoned"]
                        for r in p["control_ladder"]).lower()
        self.assertIn("hot-water", blob)
        self.assertIn("no longer", blob)

    def test_a_note_resurrecting_hot_water_dips_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["garlic"]):
                if p["id"] == P.NEMATODE:
                    for r in p["control_ladder"]:
                        if r["method"] == P.WIDEN_KEY:
                            r["note_beginner"] = "Dip the cloves in hot water before planting."
                            r["note_seasoned"] = "A hot water dip treats the seed stock."
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("retirement", problem)

    def test_missing_rung_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["garlic"]):
                if p["id"] == P.NEMATODE:
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != P.WIDEN_KEY]
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("single most important practice", problem)

    def test_rung_not_leading_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["garlic"]):
                if p["id"] == P.NEMATODE:
                    lad = p["control_ladder"]
                    lad.append(lad.pop(0))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("must lead the ladder", problem)

    def test_already_widened_is_refused(self):
        pre = _pre()
        pre["control_methods"][P.WIDEN_KEY]["applies_to"].append("nematode")
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already run", problem)

    def test_staged_spec_drift_is_refused(self):
        spec = copy.deepcopy(P.staged_widening())
        spec["best_use"] = "MUTATED"
        with _Patch("staged_widening", lambda: spec):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("disagrees with this promote's literals", problem)


class IdConvention(unittest.TestCase):
    def test_every_staged_id_is_on_convention(self):
        batch, pre = P.staged(), _pre()
        for slug in CROPS:
            canon = P.problems(_crop(pre, slug))
            for idx, (_, p) in enumerate(P.problems(batch[slug])):
                self.assertEqual(p["id"], P.ID_CONVENTION[canon[idx][1].get("name")], slug)

    def test_the_alliums_agree_on_every_shared_id(self):
        batch = P.staged()
        g = {p["id"] for _, p in P.problems(batch["garlic"])}
        s = {p["id"] for _, p in P.problems(batch["spring-onion"])}
        for pid in SHARED_ALLIUM:
            self.assertIn(pid, g, pid)
            self.assertIn(pid, s, pid)

    def test_a_divergent_id_on_a_non_shared_problem_is_refused(self):
        """ISOLATED. dill's parsleyworm is on no other crop, so only the convention loop can
        object -- the allium-agreement check cannot shadow it here."""
        def m(batch):
            for _, p in P.problems(batch["dill"]):
                if p["id"] == "parsleyworm":
                    p["id"] = "swallowtail-caterpillar"
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("join keys", problem)

    def test_a_split_allium_id_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["spring-onion"]):
                if p["id"] == "white-rot":
                    p["id"] = "allium-white-rot"
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        # NOT a hedged OR. The allium-agreement check is a documented forward assertion (one
        # ID_CONVENTION entry serves both crops, so it cannot answer first), which means the
        # convention loop is the only guard that can refuse this.
        self.assertIn("join keys", problem)

    def test_new_ids_are_genuinely_new(self):
        pre = _pre()
        existing = {p.get("id") for c in pre["crops"] for _, p in P.problems(c) if p.get("id")}
        for pid in NEW_IDS:
            self.assertNotIn(pid, existing, pid)
        self.assertEqual(tuple(P.NEW_IDS), NEW_IDS)

    def test_leafhoppers_is_minted_not_aster_yellows_reused(self):
        """carrot's aster-yellows is a DISEASE entry; cilantro's is the insect VECTOR."""
        pre = _pre()
        carrot = _prob(pre, "carrot", "aster-yellows")
        self.assertIn(carrot, _crop(pre, "carrot")["diseases"])
        batch = P.staged()
        ids = [p["id"] for fam, p in P.problems(batch["cilantro-coriander"]) if fam == "pests"]
        self.assertIn("leafhoppers", ids)
        self.assertNotIn("aster-yellows",
                         [p["id"] for _, p in P.problems(batch["cilantro-coriander"])])

    def test_soft_rot_reuses_the_cauliflower_id(self):
        pre = _pre()
        self.assertTrue(_prob(pre, "cauliflower", "bacterial-soft-rot"))
        self.assertIn("bacterial-soft-rot",
                      [p["id"] for _, p in P.problems(P.staged()["cilantro-coriander"])])

    def test_unknown_problem_name_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "dill"))[0][1]["name"] = "Mystery herb pest"
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

    def test_copper_on_cilantro_bacterial_leaf_spot_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cilantro-coriander"]):
                if p["id"] == "bacterial-leaf-spot":
                    p["control_ladder"].append(_rung("copper_fungicide"))
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("a limitation is not a recommendation", problem)

    def test_no_copper_shipped_on_that_ladder(self):
        lad = [r["method"] for r in
               _prob(_post(), "cilantro-coriander", "bacterial-leaf-spot")["control_ladder"]]
        self.assertNotIn("copper_fungicide", lad)

    def test_trap_cropping_is_refused_batch_wide(self):
        """The parallel round makes this a legal key; dill's parsleyworm is
        relocation-for-conservation, whose intent is the opposite of the method's."""
        for slug in CROPS:
            def m(batch, slug=slug):
                P.problems(batch[slug])[0][1]["control_ladder"].insert(0, _rung("trap_cropping"))
            problem = self._with(m)
            self.assertIsNotNone(problem, slug)
            self.assertIn("relocation-for-conservation", problem)

    def test_planting_time_avoidance_is_refused_batch_wide(self):
        for slug in CROPS:
            def m(batch, slug=slug):
                P.problems(batch[slug])[0][1]["control_ladder"].insert(
                    0, _rung("planting_time_avoidance"))
            problem = self._with(m)
            self.assertIsNotNone(problem, slug)
            self.assertIn("risk description is not a recommendation", problem)

    def test_handpick_off_leaf_removal_targets(self):
        def m(batch):
            for _, p in P.problems(batch["cilantro-coriander"]):
                if p["id"] == "powdery-mildew":
                    p["control_ladder"].insert(0, _rung("handpick"))
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("free-living insects", problem)

    def test_handpick_is_allowed_on_parsleyworm(self):
        lad = [r["method"] for r in _prob(_post(), "dill", "parsleyworm")["control_ladder"]]
        self.assertIn("handpick", lad)

    def test_unminted_method_in_a_note_is_refused_by_check(self):
        """The post-side sweep had a driver; this one drives the check-side scan, which the
        harness showed was untested."""
        for word, msg in (("diatomaceous earth", "diatomaceous"), ("trap crop", "trap crop")):
            def m(batch, word=word):
                P.problems(batch["garlic"])[0][1]["control_ladder"][0]["note_beginner"] += \
                    f" Try {word}."
            problem = self._with(m)
            self.assertIsNotNone(problem, word)
            self.assertIn(msg, problem)

    def test_pyrethroid_is_refused(self):
        def m(batch):
            P.problems(batch["dill"])[0][1]["control_ladder"].append(_rung("pyrethroid"))
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("synthetic pyrethroid", problem)


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
        self.assertEqual(len(post["control_methods"]), len(pre["control_methods"]))
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
        self.assertEqual(tuple(P.SHARED_ALLIUM_IDS), SHARED_ALLIUM)


class Validate(unittest.TestCase):
    def _with(self, mutator):
        with _Patch("staged", _staged_with(mutator)):
            return P.check(_pre())

    def test_unknown_method_is_refused(self):
        def m(batch):
            P.problems(batch["dill"])[0][1]["control_ladder"][0]["method"] = "ghost"
        self.assertIn("not in catalog", self._with(m))

    def test_tier_decrease_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cilantro-coriander"]):
                if p["id"] == "aphids":
                    lad = p["control_ladder"]
                    lad.insert(0, lad.pop())
        self.assertIn("tiers decrease", self._with(m))

    def test_applies_to_incoherence_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["garlic"]):
                if p["id"] == "garlic-rust":
                    p["control_ladder"].append(_rung("bt"))
        self.assertIn("cannot reach type", self._with(m))

    def test_identical_registers_are_refused(self):
        def m(batch):
            r = P.problems(batch["dill"])[0][1]["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        self.assertIn("registers are identical", self._with(m))

    def test_empty_ladder_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["garlic"]):
                if p["id"] == "garlic-rust":
                    p["control_ladder"] = []
        self.assertIn("EMPTY", self._with(m))

    def test_duplicate_method_is_refused(self):
        def m(batch):
            lad = P.problems(batch["dill"])[0][1]["control_ladder"]
            lad.append(copy.deepcopy(lad[-1]))
        self.assertIn("appears twice", self._with(m))

    def test_rung_count_drift_is_refused(self):
        """On garlic-rust, an all-cultural ladder no read pin covers."""
        def m(batch):
            for _, p in P.problems(batch["garlic"]):
                if p["id"] == "garlic-rust":
                    p["control_ladder"].append(_rung("resistant_varieties"))
        self.assertIn("rungs, expected", self._with(m))

    def test_already_laddered_crop_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "dill"))[0][1]["control_ladder"] = []
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already laddered", problem)

    def test_identical_canonical_prose_is_refused(self):
        pre = _pre()
        a, b = _crop(pre, "garlic"), _crop(pre, "spring-onion")
        n = min(len(a["pests"]), len(b["pests"]))
        for pa, pb in list(zip(a["pests"], b["pests"]))[:n]:
            for f in P.PROSE_FIELDS:
                if f in pa:
                    pb[f] = copy.deepcopy(pa[f])
                else:
                    pb.pop(f, None)
        a["diseases"] = copy.deepcopy(b["diseases"])
        a["pests"] = copy.deepcopy(b["pests"])
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("TRUE TWIN", problem)

    def test_content_identity_cannot_fire_in_this_batch(self):
        """Pins the forward-assertion status. `ladder_signature` is keyed by problem id and no two
        crops here share an id set, so the guard is unreachable in THIS batch however the ladders
        are doctored. It was load-bearing in batch 10 (collards/kale shared an id set), which is
        why it is kept rather than deleted."""
        post = _post()
        sets = {s: frozenset(p["id"] for _, p in P.problems(_crop(post, s))) for s in CROPS}
        for i, a in enumerate(CROPS):
            for b in CROPS[i + 1:]:
                self.assertNotEqual(sets[a], sets[b], f"{a}/{b} now share an id set: the guard is "
                                                      f"reachable again and needs a real driver")

    def test_identical_staged_bytes_are_refused(self):
        dg = P.staged_digests()
        dg["dill"] = dg["cilantro-coriander"]
        with _Patch("staged_digests", lambda: dg):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("copied", problem)


if __name__ == "__main__":
    unittest.main(verbosity=2)
