#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch7.py (THE TOMATOES). Base 674fab25.

REPLAY-PINNED, so green from birth is expected and TDD RED is not claimed; the evidence is the
mutation harness plus the refusal-spec tests below, each of which drives a refusal branch with a
doctored input.

`VerifyPostIsDriven` is FIRST in this file by design, for the sixth time this arc: check()
refuses every malformed input upstream, so every post-state guard needs a driver that doctors the
APPLIED post directly or it sits untested while green. The chemical-cohort harness went 49/49 on
its first run because this class was written before the rest of the suite; same order here.

The staged out_*.json files are the authoring record and check() reads them from disk, so the
staged-side refusal tests monkeypatch P.staged / P.staged_digests / P.staged_mint with doctored
copies rather than touching the files.

Frozen literals (the computed-expected-value trap): the id-convention table, the mint's key
fields, and the per-crop problem/rung counts are restated here as constants, not derived from the
promote's own tables.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch7 as P  # noqa: E402

POST_SHA = "f8678adea533447445ee2679d7d333065763a7481c39371b98d0b39d55aeeec1"

CROPS = ("beefsteak-tomato", "cherry-tomato", "grape-tomato", "roma-tomato")
COUNTS = {"beefsteak-tomato": (8, 35), "cherry-tomato": (8, 35),
          "grape-tomato": (9, 42), "roma-tomato": (9, 42)}
CONVENTION = {
    "Aphids": "aphids", "Tomato hornworm": "tomato-hornworm", "Flea beetles": "flea-beetles",
    "Spider mites": "spider-mites", "Whiteflies": "whiteflies", "Early blight": "early-blight",
    "Blossom end rot": "blossom-end-rot", "Septoria leaf spot": "septoria-leaf-spot",
    "Late blight": "late-blight", "Fusarium and Verticillium wilt": "fusarium-verticillium-wilt"}


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
    """Monkeypatch a P.<name> callable (or constant), restoring on exit."""

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
    """A staged() replacement whose dict has been run through `mutator`."""
    batch = P.staged()
    mutator(batch)
    return lambda: batch


class VerifyPostIsDriven(unittest.TestCase):
    """Every post-state guard gets an input that reaches it, bypassing check()."""

    def _staged(self):
        pre = _pre()
        return pre, P.snapshot(pre), _post(pre)

    def test_mint_verbatim_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        post["control_methods"][P.MINT_KEY]["tier"] = "physical"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("did not land verbatim", problem)

    def test_neem_regained_on_flea_beetles_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "cherry-tomato", "flea-beetles")["control_ladder"].append(
            {"method": "neem_oil", "note_beginner": "x", "note_seasoned": "y"})
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("regained neem_oil", problem)

    def test_neem_lost_where_kept_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "roma-tomato", "aphids")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "neem_oil"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("scoped to flea-beetles", problem)

    def test_ber_culling_lost_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "beefsteak-tomato", "blossom-end-rot")
        p["control_ladder"] = [r for r in p["control_ladder"]
                               if r["method"] != "garden_sanitation"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("culling rung", problem)

    def test_splash_rung_lost_is_caught(self):
        pre, snap, post = self._staged()
        p = _prob(post, "grape-tomato", "early-blight")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != P.MINT_KEY]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn(P.MINT_KEY, problem)

    def test_whitefly_divergence_collapse_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "roma-tomato", "whiteflies")["control_ladder"].append(
            {"method": "horticultural_oil", "note_beginner": "x", "note_seasoned": "y"})
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("divergence collapsed", problem)

    def test_empty_ladder_after_promote_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "cherry-tomato", "late-blight")["control_ladder"] = []
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
        post["control_methods"]["ghost_method"] = copy.deepcopy(
            post["control_methods"]["water_spray"])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("other than the one mint", problem)

    def test_bystander_crop_edit_is_caught(self):
        pre, snap, post = self._staged()
        _crop(post, "strawberry")["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("touches only", problem)

    def test_bystander_method_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["control_methods"]["copper_fungicide"]["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("bystander method", problem)

    def test_source_catalog_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["source_catalog"]["umn_ext"]["tier"] = "T2"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("source_catalog changed", problem)

    def test_identical_ladder_content_alone_is_caught_by_its_own_guard(self):
        """Same-family pair with NO divergence pin (beefsteak/cherry), so only the content
        guard can object."""
        pre, snap, post = self._staged()
        src, dst = _crop(post, "beefsteak-tomato"), _crop(post, "cherry-tomato")
        for fam in ("pests", "diseases"):
            for a, b in zip(src[fam], dst[fam]):
                b["control_ladder"] = copy.deepcopy(a["control_ladder"])
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


class IdConvention(unittest.TestCase):
    def test_convention_table_is_the_frozen_literal(self):
        self.assertEqual(dict(P.ID_CONVENTION), CONVENTION)

    def test_every_staged_id_is_on_convention(self):
        batch = P.staged()
        pre = _pre()
        for slug in CROPS:
            canon = P.problems(_crop(pre, slug))
            for idx, (_, p) in enumerate(P.problems(batch[slug])):
                name = canon[idx][1].get("name")
                self.assertEqual(p["id"], CONVENTION[name], f"{slug}/{name}")

    def test_convention_matches_what_heirloom_tomato_already_ships(self):
        """The ids are join keys; the convention is the ROSTER's, not this batch's invention."""
        pre = _pre()
        h = _crop(pre, "heirloom-tomato")
        for fam in ("pests", "diseases"):
            for p in h.get(fam) or []:
                if p.get("name") in CONVENTION:
                    self.assertEqual(p.get("id"), CONVENTION[p["name"]], p.get("name"))

    def test_divergent_id_is_refused_by_name(self):
        def mutate(batch):
            P.problems(batch["cherry-tomato"])[0][1]["id"] = "green-peach-aphid"
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("join keys", problem)

    def test_unknown_problem_name_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "cherry-tomato"))[0][1]["name"] = "Mystery pest"
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("id-convention table", problem)


class ReadFixes(unittest.TestCase):
    def test_clean_staged_files_pass(self):
        self.assertIsNone(P.check_read_fixes(P.staged(),
                                             {c["slug"]: c for c in _pre()["crops"]}))

    def test_neem_on_any_flea_beetles_ladder_is_refused(self):
        for slug in CROPS:
            def mutate(batch, s=slug):
                for _, p in P.problems(batch[s]):
                    if p["id"] == "flea-beetles":
                        p["control_ladder"].append(
                            {"method": "neem_oil", "note_beginner": "x", "note_seasoned": "y"})
            with _Patch("staged", _staged_with(mutate)):
                problem = P.check(_pre())
            self.assertIsNotNone(problem, slug)
            self.assertIn("bottom_watering shape", problem)

    def test_flea_beetles_losing_row_cover_is_refused(self):
        """The one prose-supported exclusion rung; without it the drop adjudication would leave
        the ladder empty of the control every crop's prose leads with."""
        def mutate(batch):
            for _, p in P.problems(batch["cherry-tomato"]):
                if p["id"] == "flea-beetles":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "floating_row_cover"]
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("prose-supported exclusion rung", problem)

    def test_neem_dropped_where_it_was_kept_is_refused(self):
        def mutate(batch):
            for _, p in P.problems(batch["beefsteak-tomato"]):
                if p["id"] == "spider-mites":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "neem_oil"]
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("not a blanket removal", problem)

    def test_ber_without_the_culling_rung_is_refused(self):
        def mutate(batch):
            for _, p in P.problems(batch["roma-tomato"]):
                if p["id"] == "blossom-end-rot":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "garden_sanitation"]
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("first affected fruit", problem)

    def test_missing_splash_rung_is_refused(self):
        def mutate(batch):
            for _, p in P.problems(batch["cherry-tomato"]):
                if p["id"] == "septoria-leaf-spot":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != P.MINT_KEY]
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("splash mulching", problem)

    def test_misplaced_splash_rung_is_refused(self):
        def mutate(batch):
            for _, p in P.problems(batch["cherry-tomato"]):
                if p["id"] == "early-blight":
                    lad = p["control_ladder"]
                    i = next(k for k, r in enumerate(lad) if r["method"] == P.MINT_KEY)
                    lad.append(lad.pop(i))
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("directly after water_at_the_base", problem)

    def test_whitefly_divergence_is_pinned_both_directions(self):
        def add_to_roma(batch):
            for _, p in P.problems(batch["roma-tomato"]):
                if p["id"] == "whiteflies":
                    p["control_ladder"].append({"method": "weed_host_control",
                                                "note_beginner": "x", "note_seasoned": "y"})
        with _Patch("staged", _staged_with(add_to_roma)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("must not be leveled", problem)

        def drop_from_grape(batch):
            for _, p in P.problems(batch["grape-tomato"]):
                if p["id"] == "whiteflies":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "horticultural_oil"]
        with _Patch("staged", _staged_with(drop_from_grape)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("its own prose supports", problem)

    def test_roma_whiteflies_must_keep_neem(self):
        """Roma's whiteflies neem rung is protected by NEEM_KEPT, the same pin as the aphid
        rungs; this drives that pin on the whitefly slot specifically."""
        def mutate(batch):
            for _, p in P.problems(batch["roma-tomato"]):
                if p["id"] == "whiteflies":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "neem_oil"]
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("not a blanket removal", problem)

    def test_a_small_tomato_gaining_whiteflies_is_refused(self):
        def mutate(batch):
            src = next(p for _, p in P.problems(batch["grape-tomato"])
                       if p["id"] == "whiteflies")
            batch["beefsteak-tomato"]["pests"].append(copy.deepcopy(src))
        with _Patch("staged", _staged_with(mutate)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("does not carry", problem)


class Twins(unittest.TestCase):
    def test_clean_state_is_not_twins(self):
        self.assertIsNone(P.check_not_twins({c["slug"]: c for c in _pre()["crops"]}))

    def test_identical_canonical_prose_is_refused(self):
        pre = _pre()
        a, b = _crop(pre, "beefsteak-tomato"), _crop(pre, "cherry-tomato")
        for fam in ("pests", "diseases"):
            for pa, pb in zip(a[fam], b[fam]):
                for f in P.PROSE_FIELDS:
                    pb[f] = copy.deepcopy(pa.get(f))
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("TRUE TWIN", problem)

    def test_identical_staged_bytes_are_refused(self):
        dg = P.staged_digests()
        dg["roma-tomato"] = dg["grape-tomato"]
        with _Patch("staged_digests", lambda: dg):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("copied", problem)

    def test_all_six_pairs_have_distinct_staged_bytes(self):
        dg = list(P.staged_digests().values())
        self.assertEqual(len(dg), len(set(dg)))


class CatalogPremises(unittest.TestCase):
    def test_mint_already_present_is_refused(self):
        pre = _pre()
        pre["control_methods"][P.MINT_KEY] = copy.deepcopy(P.MINT)
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already run", problem)

    def test_staged_mint_disagreement_is_refused(self):
        bad = copy.deepcopy(P.staged_mint())
        bad["entry"]["tier"] = "physical"
        with _Patch("staged_mint", lambda: bad):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("drift apart", problem)

    def test_missing_copper_split_caution_is_refused(self):
        pre = _pre()
        cm = pre["control_methods"]["copper_fungicide"]
        cm["cautions"] = [c for c in cm["cautions"] if "copper hydroxide" not in c]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("chemical-cohort round must land", problem)

    def test_missing_neem_band_caution_is_refused(self):
        pre = _pre()
        cm = pre["control_methods"]["neem_oil"]
        cm["cautions"] = [c.replace("sunset", "dawn") for c in cm["cautions"]]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("medium-band bee caution", problem)

    def test_pre_state_actually_carries_both_premises(self):
        """The premises are real facts about 674fab25, the canonical the chemical round built."""
        cm = _pre()["control_methods"]
        self.assertTrue(any("copper hydroxide" in c for c in cm["copper_fungicide"]["cautions"]))
        blob = " ".join(cm["neem_oil"]["cautions"])
        self.assertIn("sunset", blob)
        self.assertIn("midnight", blob)

    def test_mint_literal_key_fields_are_frozen(self):
        self.assertEqual(P.MINT["tier"], "cultural")
        self.assertEqual(P.MINT["applies_to"], ["fungal_foliar", "bacterial", "disease_general"])
        self.assertEqual(P.MINT["sources"], ["umn_ext"])
        self.assertIn("tomato-leaf-spot-diseases", P.MINT["anchoring_urls"]["umn_ext"]["url"])
        self.assertEqual(P.MINT["anchoring_urls"]["umn_ext"]["verified"], "2026-08-26")
        self.assertIn("herbicide", P.MINT["cautions"][0])
        self.assertIn("Distinct from", P.MINT["best_use"])


class Validate(unittest.TestCase):
    def _with(self, mutator):
        with _Patch("staged", _staged_with(mutator)):
            return P.check(_pre())

    def test_unknown_method_is_refused(self):
        def m(batch):
            P.problems(batch["cherry-tomato"])[0][1]["control_ladder"][0]["method"] = "ghost"
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("not in catalog", problem)

    def test_tier_decrease_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cherry-tomato"]):
                if p["id"] == "aphids":
                    lad = p["control_ladder"]
                    lad.insert(0, lad.pop())          # soap/neem to the front
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("tiers decrease", problem)

    def test_identical_registers_are_refused(self):
        def m(batch):
            r = P.problems(batch["cherry-tomato"])[0][1]["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("registers are identical", problem)

    def test_empty_ladder_is_refused(self):
        """On late-blight, a problem no read pin covers, so only the EMPTY check can object."""
        def m(batch):
            for _, p in P.problems(batch["cherry-tomato"]):
                if p["id"] == "late-blight":
                    p["control_ladder"] = []
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("EMPTY", problem)

    def test_duplicate_method_is_refused(self):
        def m(batch):
            lad = P.problems(batch["cherry-tomato"])[0][1]["control_ladder"]
            lad.append(copy.deepcopy(lad[-1]))
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("appears twice", problem)

    def test_missing_register_is_refused(self):
        def m(batch):
            P.problems(batch["cherry-tomato"])[0][1]["control_ladder"][0]["note_beginner"] = " "
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("missing or empty", problem)

    def test_rung_count_drift_is_refused(self):
        def m(batch):
            for _, p in P.problems(batch["cherry-tomato"]):
                if p["id"] == "late-blight":
                    p["control_ladder"].append({"method": "garden_sanitation",
                                                "note_beginner": "x", "note_seasoned": "y"})
        problem = self._with(m)
        self.assertIsNotNone(problem)
        # the duplicate-method guard fires first on this ladder; inject on a ladder without it
        def m2(batch):
            for _, p in P.problems(batch["cherry-tomato"]):
                if p["id"] == "flea-beetles":
                    p["control_ladder"].append({"method": "yellow_sticky_traps",
                                                "note_beginner": "x", "note_seasoned": "y"})
        problem = self._with(m2)
        self.assertIsNotNone(problem)
        self.assertIn("rungs, expected", problem)

    def test_applies_to_incoherence_is_refused(self):
        """bt reaches only insect_chewing; appended to a fungal ladder it must bounce, and the
        applies_to check sits inside the rung loop so it answers before the tier check."""
        def m(batch):
            for _, p in P.problems(batch["cherry-tomato"]):
                if p["id"] == "early-blight":
                    p["control_ladder"].append({"method": "bt",
                                                "note_beginner": "x", "note_seasoned": "y"})
        problem = self._with(m)
        self.assertIsNotNone(problem)
        self.assertIn("cannot reach type", problem)

    def test_already_laddered_crop_is_refused(self):
        pre = _pre()
        P.problems(_crop(pre, "cherry-tomato"))[0][1]["control_ladder"] = []
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already laddered", problem)

    def test_splash_rungs_are_only_legal_because_of_the_mint(self):
        """The staged ladders are ILLEGAL against the pre-catalog: validate_batch without the
        mint must refuse them. This is the reachability proof for validating against cm_post."""
        pre = _pre()
        problem = P.validate_batch(P.staged(), pre["control_methods"])
        self.assertIsNotNone(problem)
        self.assertIn(P.MINT_KEY, problem)
        cm_post = dict(pre["control_methods"])
        cm_post[P.MINT_KEY] = P.MINT
        self.assertIsNone(P.validate_batch(P.staged(), cm_post))


if __name__ == "__main__":
    unittest.main(verbosity=2)
