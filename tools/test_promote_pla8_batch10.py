#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch10.py (THE BRASSICA FAMILY). Base 4725bcbb.

REPLAY-PINNED; the evidence is the mutation harness plus the refusal-spec drivers.
`VerifyPostIsDriven` is FIRST, ninth time this arc.

Frozen literals: the id convention, the new-id list, the mint's load-bearing fields, the copper
and timing tables and the per-crop counts are restated here, not derived from the promote.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch10 as P  # noqa: E402

POST_SHA = "be444e25a614e2a8ff95dae7aebaf6835277545e7d4b4e7905f1309355e57234"

CROPS = ("cabbage", "cauliflower", "kohlrabi", "collards", "kale")
COUNTS = {"cabbage": (10, 47), "cauliflower": (10, 52), "kohlrabi": (10, 52),
          "collards": (9, 43), "kale": (9, 43)}
NEW_IDS = ("bacterial-soft-rot", "blackleg", "fusarium-yellows")
TIMING_KEPT = (("kohlrabi", "flea-beetles"),)
HANDPICK_OK = ("cabbageworms", "harlequin-bug")


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

    def test_mint_verbatim_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        post["control_methods"][P.MINT_KEY]["tier"] = "conventional"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("did not land verbatim", problem)

    def test_pyrethroid_shipping_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "cabbage", "harlequin-bug")["control_ladder"].append(_rung("pyrethroid"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("synthetic pyrethroid", problem)

    def test_lost_pyrethrin_rung_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "kale", "harlequin-bug")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != P.MINT_KEY]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("lost its pyrethrin rung", problem)

    def test_regained_timing_rung_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "cabbage", "cabbage-root-maggot")["control_ladder"].insert(
            1, _rung("planting_time_avoidance"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("unearned timing rung", problem)

    def test_lost_scoped_timing_rung_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "kohlrabi", "flea-beetles")
        p["control_ladder"] = [r for r in p["control_ladder"]
                               if r["method"] != "planting_time_avoidance"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("prose DOES recommend", problem)

    def test_copper_on_black_rot_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "collards", "black-rot")["control_ladder"].append(_rung("copper_fungicide"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("does not recommend", problem)

    def test_lost_copper_where_recommended_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "kale", "downy-mildew")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "copper_fungicide"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("lost its copper rung", problem)

    def test_handpick_on_a_leaf_removal_target_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "cabbage", "downy-mildew")["control_ladder"].insert(1, _rung("handpick"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("leaf-removal target", problem)

    def test_unminted_method_in_a_note_is_caught(self):
        for word in ("diatomaceous earth", "trap crop"):
            pre, snap, post = self._staged()
            _prob(post, "kohlrabi", "clubroot")["control_ladder"][0]["note_seasoned"] += \
                f" Consider a {word}."
            problem = P.verify_post(snap, post)
            self.assertIsNotNone(problem, word)
            self.assertIn("unminted method reached a note", problem)

    def test_empty_post_ladder_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "cauliflower", "bacterial-soft-rot")["control_ladder"] = []
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

    def test_second_method_beyond_the_mint_is_caught(self):
        pre, snap, post = self._staged()
        post["control_methods"]["ghost"] = copy.deepcopy(post["control_methods"]["handpick"])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("other than the one mint", problem)

    def test_bystander_crop_edit_is_caught(self):
        pre, snap, post = self._staged()
        _crop(post, "broccoli")["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("touches only", problem)

    def test_bystander_method_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["control_methods"]["pyrethroid"]["tier"] = "soft_chemical"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("bystander method", problem)

    def test_source_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["source_catalog"]["npic_orst"]["tier"] = "T2"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("source_catalog changed", problem)

    def test_identical_ladder_content_is_caught(self):
        """ISOLATED. collards and kale carry the same 9 problems and the same method sequences
        (their source prose is byte-identical on several), so a wholesale note copy is otherwise
        well-formed and only the content-identity guard can object."""
        pre, snap, post = self._staged()
        # BY ID, not by index: the two crops order their problems differently, and an index-zip
        # lands collards' harlequin ladder on kale's aphids, tripping the handpick pin instead --
        # the driver would never reach the guard under test.
        src = {p["id"]: p["control_ladder"]
               for _, p in P.problems(_crop(post, "collards"))}
        for _, p in P.problems(_crop(post, "kale")):
            p["control_ladder"] = copy.deepcopy(src[p["id"]])
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
        self.assertEqual(len(post["control_methods"]), len(pre["control_methods"]) + 1)
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


class TheMint(unittest.TestCase):
    def test_mint_is_the_botanical_not_the_synthetic(self):
        """The whole reason this entry exists: `pyrethroid` is the synthetic analog at
        conventional tier, and the crops' prose names the organic-permitted botanical."""
        pre = _pre()
        self.assertEqual(pre["control_methods"]["pyrethroid"]["tier"], "conventional")
        self.assertEqual(P.MINT["tier"], "soft_chemical")
        self.assertIn("chrysanthemum", P.MINT["how_it_works_beginner"].lower())
        self.assertIn("Distinct from the synthetic pyrethroids", P.MINT["best_use"])

    def test_mint_states_the_strictest_bee_band(self):
        """The reading that changed what the entry had to say: organically acceptable, and in
        the SAME bee band as the conventional insecticides."""
        blob = " ".join(P.MINT["cautions"])
        self.assertIn("strictest honey bee band", blob)
        self.assertIn("does not soften", blob)
        self.assertNotIn("sunset", blob.lower())
        self.assertNotIn("dusk", blob.lower())

    def test_mint_states_the_mild_halves_too(self):
        blob = " ".join(P.MINT["cautions"]).lower()
        self.assertIn("acute toxicity to people and other mammals low", blob)
        self.assertIn("no known risk", blob)

    def test_mint_is_t1_anchored_twice(self):
        pre = _pre()
        self.assertEqual(P.MINT["sources"], ["ucipm_uaidb", "npic_orst"])
        for sid in P.MINT["sources"]:
            self.assertEqual(pre["source_catalog"][sid]["tier"], "T1", sid)
            self.assertIn(sid, P.MINT["anchoring_urls"])
        self.assertIn("uaiKey=53", P.MINT["anchoring_urls"]["ucipm_uaidb"]["url"])

    def test_every_harlequin_ladder_takes_the_mint_last(self):
        post = _post()
        for slug in CROPS:
            lad = [r["method"] for r in _prob(post, slug, "harlequin-bug")["control_ladder"]]
            self.assertEqual(lad[-1], P.MINT_KEY, slug)

    def test_no_pyrethroid_anywhere_in_the_batch(self):
        post = _post()
        for slug in CROPS:
            for _, p in P.problems(_crop(post, slug)):
                self.assertNotIn("pyrethroid",
                                 [r["method"] for r in p["control_ladder"]], f"{slug}/{p['id']}")

    def test_missing_pyrethroid_premise_is_refused(self):
        """The mint's whole justification is the contrast with the synthetic. If `pyrethroid`
        ever leaves the catalog the distinction is moot and this promote should say so; without
        this driver the premise check is unfalsifiable decoration."""
        pre = _pre()
        del pre["control_methods"]["pyrethroid"]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("moot", problem)

    def test_staged_spec_drift_is_refused(self):
        """MINT is a LITERAL; this proves the agreement check can actually fail."""
        spec = copy.deepcopy(P.staged_mint())
        spec["entry"]["cautions"] = spec["entry"]["cautions"][:1]
        with _Patch("staged_mint", lambda: spec):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("disagrees with this promote's literal", problem)

    def test_mint_already_present_is_refused(self):
        pre = _pre()
        pre["control_methods"][P.MINT_KEY] = copy.deepcopy(P.MINT)
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already run", problem)

    def test_bee_band_claim_removed_is_refused(self):
        bad = copy.deepcopy(P.MINT)
        bad["cautions"] = [c for c in bad["cautions"] if "strictest honey bee band" not in c]
        spec = copy.deepcopy(P.staged_mint()); spec["entry"] = bad
        with _Patch("MINT", bad), _Patch("staged_mint", lambda: spec):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("worth writing", problem)

    def test_wrong_tier_is_refused(self):
        bad = copy.deepcopy(P.MINT)
        bad["tier"] = "conventional"
        spec = copy.deepcopy(P.staged_mint()); spec["entry"] = bad
        with _Patch("MINT", bad), _Patch("staged_mint", lambda: spec):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("organic-permitted", problem)


class ReadFixes(unittest.TestCase):
    def _with(self, mutator):
        with _Patch("staged", _staged_with(mutator)):
            return P.check(_pre())

    def test_clean_staged_files_pass(self):
        self.assertIsNone(P.check_read_fixes(P.staged(),
                                             {c["slug"]: c for c in _pre()["crops"]}))

    def test_timing_rung_on_any_root_maggot_is_refused(self):
        for slug in CROPS:
            def m(batch, slug=slug):
                for _, p in P.problems(batch[slug]):
                    if p["id"] == "cabbage-root-maggot":
                        p["control_ladder"].insert(1, _rung("planting_time_avoidance"))
            problem = self._with(m)
            self.assertIsNotNone(problem, slug)
            self.assertIn("never recommends shifting the planting", problem)

    def test_kohlrabi_flea_timing_rung_is_required(self):
        def m(batch):
            for _, p in P.problems(batch["kohlrabi"]):
                if p["id"] == "flea-beetles":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "planting_time_avoidance"]
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("scoped rather than blanket", problem)

    def test_pyrethroid_substitution_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cauliflower"]):
                if p["id"] == "harlequin-bug":
                    p["control_ladder"].append(_rung("pyrethroid"))
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("swaps the material", problem)

    def test_missing_pyrethrin_rung_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["collards"]):
                if p["id"] == "harlequin-bug":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != P.MINT_KEY]
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("names botanical pyrethrins", problem)

    def test_copper_on_black_rot_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cabbage"]):
                if p["id"] == "black-rot":
                    p["control_ladder"].append(_rung("copper_fungicide"))
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("names no fungicide for black rot", problem)

    def test_lost_copper_where_recommended_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cauliflower"]):
                if p["id"] == "alternaria-leaf-spot":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "copper_fungicide"]
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("prose recommends copper", problem)

    def test_handpick_on_a_disease_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["kale"]):
                if p["id"] == "alternaria-leaf-spot":
                    p["control_ladder"].insert(1, _rung("handpick"))
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("free-living insects", problem)

    def test_unminted_methods_in_notes_are_refused(self):
        for word, msg in (("diatomaceous earth", "diatomaceous"), ("trap crop", "trap cropping")):
            def m(batch, word=word):
                P.problems(batch["cabbage"])[0][1]["control_ladder"][0]["note_beginner"] += \
                    f" Try a {word}."
            problem = self._with(m)
            self.assertIsNotNone(problem, word)
            self.assertIn(msg, problem)


class IdConvention(unittest.TestCase):
    def test_every_staged_id_is_on_convention(self):
        batch, pre = P.staged(), _pre()
        for slug in CROPS:
            canon = P.problems(_crop(pre, slug))
            for idx, (_, p) in enumerate(P.problems(batch[slug])):
                self.assertEqual(p["id"], P.ID_CONVENTION[canon[idx][1].get("name")], slug)

    def test_both_cabbageworm_spellings_converge(self):
        self.assertEqual(P.ID_CONVENTION["Cabbageworms and cabbage loopers"], "cabbageworms")
        self.assertEqual(
            P.ID_CONVENTION["Cabbageworms, loopers, and diamondback moths"], "cabbageworms")

    def test_new_ids_are_genuinely_new(self):
        pre = _pre()
        existing = {p.get("id") for c in pre["crops"] for _, p in P.problems(c) if p.get("id")}
        for pid in NEW_IDS:
            self.assertNotIn(pid, existing, pid)
        self.assertEqual(tuple(P.NEW_IDS), NEW_IDS)

    def test_reused_ids_really_ship_already(self):
        pre = _pre()
        existing = {p.get("id") for c in pre["crops"] for _, p in P.problems(c) if p.get("id")}
        for pid in set(P.ID_CONVENTION.values()) - set(NEW_IDS):
            self.assertIn(pid, existing, pid)

    def test_specialist_vs_generic_aphid_split_is_prose_driven(self):
        """cabbage/cauliflower/kohlrabi name the Brevicoryne specialist; collards/kale are
        titled 'Aphids' and describe the complex."""
        batch = P.staged()
        for slug in ("cabbage", "cauliflower", "kohlrabi"):
            self.assertIn("cabbage-aphids", [p["id"] for _, p in P.problems(batch[slug])], slug)
        for slug in ("collards", "kale"):
            ids = [p["id"] for _, p in P.problems(batch[slug])]
            self.assertIn("aphids", ids, slug)
            self.assertNotIn("cabbage-aphids", ids, slug)

    def test_unknown_problem_name_is_refused(self):
        """Drives the `want is None` branch: without a driver the whole convention lookup can be
        disabled and every test stays green (the harness caught exactly that)."""
        pre = _pre()
        P.problems(_crop(pre, "cabbage"))[0][1]["name"] = "Mystery brassica pest"
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("id-convention table", problem)

    def test_divergent_id_is_refused(self):
        def m(batch):
            P.problems(batch["kale"])[0][1]["id"] = "cabbage-caterpillars"
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("join keys", problem)


class TwinsAndValidate(unittest.TestCase):
    def _with(self, mutator):
        with _Patch("staged", _staged_with(mutator)):
            return P.check(_pre())

    def test_identical_staged_bytes_are_refused(self):
        dg = P.staged_digests()
        dg["kale"] = dg["collards"]
        with _Patch("staged_digests", lambda: dg):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("copied", problem)

    def test_all_pairs_have_distinct_staged_bytes(self):
        dg = list(P.staged_digests().values())
        self.assertEqual(len(dg), len(set(dg)))

    def test_collards_and_kale_share_methods_but_not_notes(self):
        """Their source prose is byte-identical on several problems, so the METHOD sequences
        legitimately converge; the notes must still be independently authored."""
        batch = P.staged()
        a = {p["id"]: [r["method"] for r in p["control_ladder"]]
             for _, p in P.problems(batch["collards"])}
        b = {p["id"]: [r["method"] for r in p["control_ladder"]]
             for _, p in P.problems(batch["kale"])}
        self.assertEqual(a, b, "the shared-name family converged on methods, as expected")
        na = {(p["id"], r["method"]): (r["note_beginner"], r["note_seasoned"])
              for _, p in P.problems(batch["collards"]) for r in p["control_ladder"]}
        nb = {(p["id"], r["method"]): (r["note_beginner"], r["note_seasoned"])
              for _, p in P.problems(batch["kale"]) for r in p["control_ladder"]}
        shared = set(na) & set(nb)
        self.assertGreater(len(shared), 30)
        for k in shared:
            self.assertNotEqual(na[k], nb[k], f"{k} was copied rather than authored")

    def test_identical_canonical_prose_is_refused(self):
        pre = _pre()
        a, b = _crop(pre, "collards"), _crop(pre, "kale")
        for fam in ("pests", "diseases"):
            for pa, pb in zip(a[fam], b[fam]):
                for f in P.PROSE_FIELDS:
                    pb[f] = copy.deepcopy(pa.get(f))
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("TRUE TWIN", problem)

    def test_unknown_method_is_refused(self):
        def m(batch):
            P.problems(batch["cabbage"])[0][1]["control_ladder"][0]["method"] = "ghost"
        self.assertIn("not in catalog", self._with(m))

    def test_tier_decrease_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cabbage"]):
                if p["id"] == "cabbage-aphids":
                    lad = p["control_ladder"]
                    lad.insert(0, lad.pop())
        self.assertIn("tiers decrease", self._with(m))

    def test_applies_to_incoherence_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cabbage"]):
                if p["id"] == "clubroot":
                    p["control_ladder"].append(_rung("bt"))
        self.assertIn("cannot reach type", self._with(m))

    def test_identical_registers_are_refused(self):
        def m(batch):
            r = P.problems(batch["cabbage"])[0][1]["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        self.assertIn("registers are identical", self._with(m))

    def test_empty_ladder_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cabbage"]):
                if p["id"] == "fusarium-yellows":
                    p["control_ladder"] = []
        self.assertIn("EMPTY", self._with(m))

    def test_duplicate_method_is_refused(self):
        def m(batch):
            lad = P.problems(batch["cabbage"])[0][1]["control_ladder"]
            lad.append(copy.deepcopy(lad[-1]))
        self.assertIn("appears twice", self._with(m))

    def test_rung_count_drift_is_refused(self):
        """On cabbage/blackleg, an all-cultural ladder no read pin covers."""
        def m(batch):
            for _, p in P.problems(batch["cabbage"]):
                if p["id"] == "blackleg":
                    p["control_ladder"].append(_rung("resistant_varieties"))
        self.assertIn("rungs, expected", self._with(m))

    def test_already_laddered_crop_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "cabbage"))[0][1]["control_ladder"] = []
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already laddered", problem)


class ReadRecord(unittest.TestCase):
    def test_tables_are_the_frozen_literals(self):
        self.assertEqual(tuple(P.TIMING_KEPT), TIMING_KEPT)
        self.assertEqual(tuple(P.HANDPICK_OK), HANDPICK_OK)
        self.assertEqual(len(P.COPPER_ON), 9)

    def test_no_root_maggot_ladder_carries_the_timing_rung(self):
        batch = P.staged()
        for slug in CROPS:
            ms, _ = P.ladder_of(batch[slug], "cabbage-root-maggot")
            self.assertNotIn("planting_time_avoidance", ms, slug)

    def test_no_black_rot_ladder_carries_copper(self):
        batch = P.staged()
        for slug in CROPS:
            ms, _ = P.ladder_of(batch[slug], "black-rot")
            self.assertNotIn("copper_fungicide", ms, slug)

    def test_every_pyrethrin_rung_states_the_bee_band(self):
        """The rungs restate the mint's load-bearing caution rather than borrowing a dusk
        window from the softer materials."""
        batch = P.staged()
        for slug in CROPS:
            _, p = P.ladder_of(batch[slug], "harlequin-bug")
            r = [x for x in p["control_ladder"] if x["method"] == P.MINT_KEY][0]
            blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
            self.assertIn("strictest", blob, slug)
            self.assertNotIn("at dusk", blob, slug)

    def test_no_conventional_rung_anywhere_in_the_batch(self):
        cm = _pre()["control_methods"]
        cm_post = dict(cm)
        cm_post[P.MINT_KEY] = P.MINT
        batch = P.staged()
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                for r in p["control_ladder"]:
                    self.assertNotEqual(cm_post[r["method"]]["tier"], "conventional",
                                        f"{slug}/{p['id']}/{r['method']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
