#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_disease_escape_sowing.py. Base 7f5079aa.

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.

`VerifyPostIsDriven` is FIRST. Every branch of `verify_post` gets a driver that reaches it, because
a post-state guard with no driver is the failure mode this arc keeps rediscovering.

`Disclosure` is the safety family. The escape is a race the grower can lose: early sowing trades
late-season disease for a cold, wet seedbed, and NC State quantifies the floor (seed in moist soil
below 50°F will often rot, 60°F for the high-sugar corn genetics). A sheet recommending early
sowing without that trade can cost a reader their stand, so the promote refuses it.

`Contrast` is why this is a NEW KEY rather than a widening of `planting_time_avoidance`. That
method dodges a pest's flight window, which extension services publish as local calendar or
degree-day dates; this races a weather-driven epidemic with no published start date. And it is not
`resistant_varieties`, which changes WHAT you plant rather than WHEN.

`Exclusions` pins that all four excluded problems RESOLVE. spinach/damping-off is the dangerous
one: typed `fungal`, so a rung there is LEGAL per TYPE_TARGETS while advising the exact harm
(early sowing into cold soil is what CAUSES damping-off).

Frozen literals: the key, tier, applies_to, the disclosure axes, the contrast tokens and the
exclusion list are restated here as literals, NOT derived from the promote.
"""
import copy, hashlib, json, os, sys, unittest
from contextlib import contextmanager

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_disease_escape_sowing as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "9f38bb007d3abd5b1cfc970178b9a4405088b0a9de46ff27eaba5163bef7b575"

# FROZEN LITERALS -- restated, never derived from P.
KEY = "disease_escape_sowing"
TIER = "cultural"
APPLIES_TO = ["fungal_foliar"]
DISCLOSURE_AXES = ("late_build", "not_a_cure", "resistance", "seed_rot", "threshold")
CONTRAST_TOKENS = ("flight window", "published", "weather-driven", "what you plant")
SOURCES = ["wsu_ext", "cornell_ext", "ncsu_ext"]
EXCLUDED = (
    ("spinach", "damping-off"),
    ("radish", "black-rot"),
    ("cilantro-coriander", "powdery-mildew"),
    ("jalapeno", "mosaic-viruses"),
)


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


@contextmanager
def swap(name, value):
    old = copy.deepcopy(getattr(P, name))
    setattr(P, name, value)
    try:
        yield
    finally:
        setattr(P, name, old)


def _rung(method):
    return {"method": method, "note_beginner": "b", "note_seasoned": "s"}


class VerifyPostIsDriven(unittest.TestCase):
    """One driver per branch of verify_post. Written first, on purpose."""

    def _staged(self):
        pre = _pre()
        return P.snapshot(pre), _post(pre)

    def test_unminted_method_is_caught(self):
        snap, post = self._staged()
        del post["control_methods"][KEY]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("was not minted", out)

    def test_non_verbatim_landing_is_caught(self):
        snap, post = self._staged()
        post["control_methods"][KEY]["name"] = "Escape sowing"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("did not land verbatim", out)

    def test_stripped_disclosure_is_caught(self):
        """The safety branch. Drop the cold-soil caution and the post guard must object."""
        snap, post = self._staged()
        m = post["control_methods"][KEY]
        m["cautions"] = [c for c in m["cautions"] if "50°F" not in c]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("do not state", out)
        self.assertIn("threshold", out)

    def test_stripped_contrast_is_caught(self):
        snap, post = self._staged()
        m = post["control_methods"][KEY]
        m["best_use"] = m["best_use"].replace("flight window", "schedule")
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("does not distinguish", out)

    def test_widened_applies_to_is_caught(self):
        """Fires on a plain post-state mutation with no swap of P.METHOD; the branch ordering in
        verify_post is what keeps it reachable under the verbatim catch-all."""
        snap, post = self._staged()
        post["control_methods"][KEY]["applies_to"] = ["fungal_foliar", "fungal_soilborne"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("not the narrow scope", out)

    def test_wrong_tier_is_caught(self):
        snap, post = self._staged()
        post["control_methods"][KEY]["tier"] = "physical"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("tier is not cultural", out)

    def test_a_rung_landing_here_is_caught(self):
        """This promote MINTS ONLY. A ladder gaining the rung belongs to the backfill."""
        snap, post = self._staged()
        for c in post["crops"]:
            if c.get("slug") == "sweet-corn":
                for p in c.get("diseases") or []:
                    if p.get("id") == "common-rust":
                        p["control_ladder"].insert(1, _rung(KEY))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("mints only", out)

    def test_a_rung_on_an_EXCLUDED_problem_is_caught(self):
        """The refusal-spec driver, on the dangerous exclusion: early sowing into cold soil is
        what CAUSES spinach damping-off, and the type gate would accept the rung."""
        snap, post = self._staged()
        for c in post["crops"]:
            if c.get("slug") == "spinach":
                for p in c.get("diseases") or []:
                    if p.get("id") == "damping-off":
                        p["control_ladder"].insert(1, _rung(KEY))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("must never get one", out)

    def test_an_exclusion_that_stops_resolving_is_caught(self):
        snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "radish"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("no longer resolves", out)

    def test_a_second_added_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"]["ghost_method"] = copy.deepcopy(P.METHOD)
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("methods added", out)

    def test_a_dropped_method_is_caught(self):
        snap, post = self._staged()
        del post["control_methods"]["planting_time_avoidance"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("was dropped", out)

    def test_an_edited_existing_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"]["planting_time_avoidance"]["best_use"] += " x"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("only mints", out)

    def test_a_touched_source_is_caught(self):
        snap, post = self._staged()
        post["source_catalog"]["wsu_ext"]["accessed"] = "2099-01"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("source_catalog changed", out)

    def test_a_touched_crop_is_caught(self):
        snap, post = self._staged()
        for c in post["crops"]:
            if c.get("slug") == "tomatillo":
                c["name"] = "MUTATED"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("a crop changed", out)

    def test_verify_post_is_clean_on_the_real_apply(self):
        snap, post = self._staged()
        self.assertIsNone(P.verify_post(snap, post))


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

    def test_catalog_grows_by_exactly_one(self):
        pre = _pre()
        self.assertNotIn(KEY, pre["control_methods"])
        post = _post(pre)
        self.assertEqual(len(post["control_methods"]), len(pre["control_methods"]) + 1)
        self.assertIn(KEY, post["control_methods"])

    def test_check_REFUSES_running_over_its_own_output(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already in the catalog", out)

    def test_apply_to_REFUSES_a_second_run(self):
        with self.assertRaises(AssertionError):
            P.apply_to(_post())


class MintShape(unittest.TestCase):
    def test_the_frozen_identity_holds(self):
        self.assertEqual(P.KEY, KEY)
        self.assertEqual(P.METHOD["tier"], TIER)
        self.assertEqual(P.METHOD["applies_to"], APPLIES_TO)
        self.assertEqual(P.METHOD["sources"], SOURCES)

    def test_applies_to_is_foliar_fungal_and_no_more(self):
        """All seven measured instances are foliar fungal (two rusts, a powdery mildew).
        fungal_soilborne and disease_general are deliberately absent: nothing was read for a
        soilborne or bacterial escape, and declaring them would make the method legal on problems
        no source covers -- including damping-off, where the advice inverts."""
        self.assertEqual(P.METHOD["applies_to"], ["fungal_foliar"])
        self.assertNotIn("disease_general", P.METHOD["applies_to"])
        self.assertNotIn("any", P.METHOD["applies_to"])

    def test_it_is_legal_on_every_target_problem_type(self):
        from control_ladder_gate import TYPE_TARGETS
        post = _post()
        m = post["control_methods"][KEY]
        self.assertTrue(set(m["applies_to"]) & TYPE_TARGETS["fungal"])

    def test_it_is_NOT_legal_on_the_bacterial_and_viral_exclusions(self):
        """radish/black-rot is bacterial and jalapeno/mosaic-viruses is viral: the gate refuses
        those two on type alone. spinach and cilantro are fungal, which is why the exclusion list
        exists at all -- the gate cannot catch them."""
        from control_ladder_gate import TYPE_TARGETS
        m = _post()["control_methods"][KEY]
        self.assertFalse(set(m["applies_to"]) & TYPE_TARGETS["bacterial"])
        self.assertFalse(set(m["applies_to"]) & TYPE_TARGETS["viral"])

    def test_check_REFUSES_a_non_cultural_tier(self):
        bad = copy.deepcopy(P.METHOD)
        bad["tier"] = "physical"
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cultural practice", out)

    def test_check_REFUSES_a_widened_applies_to(self):
        bad = copy.deepcopy(P.METHOD)
        bad["applies_to"] = ["fungal_foliar", "disease_general"]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("applies_to must be exactly", out)

    def test_check_REFUSES_a_missing_required_field(self):
        bad = copy.deepcopy(P.METHOD)
        bad["best_use"] = ""
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("missing required field", out)

    def test_every_declared_source_is_T1_and_anchored(self):
        pre = _pre()
        sc = pre["source_catalog"]
        for s in P.METHOD["sources"]:
            self.assertIn(s, sc, s)
            self.assertEqual((sc[s].get("tier") or "").upper(), "T1", s)
            self.assertIn(s, P.METHOD["anchoring_urls"], s)
            self.assertTrue(P.METHOD["anchoring_urls"][s]["url"].startswith("https://"), s)

    def test_the_anchors_are_document_specific_not_bare_domains(self):
        """The house pattern: bare source id, document-scoped URL. A bare-domain anchor is the
        catalog-divergence shape in embryo."""
        for s, a in P.METHOD["anchoring_urls"].items():
            from urllib.parse import urlparse
            self.assertTrue(urlparse(a["url"]).path.strip("/"), s)

    def test_check_REFUSES_a_source_missing_from_the_catalog(self):
        bad = copy.deepcopy(P.METHOD)
        bad["sources"] = bad["sources"] + ["not_a_real_source"]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not in source_catalog", out)

    def test_check_REFUSES_an_unanchored_source(self):
        bad = copy.deepcopy(P.METHOD)
        del bad["anchoring_urls"]["ncsu_ext"]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("has no anchoring_url", out)


class Disclosure(unittest.TestCase):
    """The safety family. The escape is a race the grower can lose at the cold end."""

    def test_the_axis_table_is_the_frozen_one(self):
        """COVERAGE. The checks below iterate REQUIRED_DISCLOSURES, so trimming an entry makes
        them check less and still pass. Pinned against a restated literal."""
        self.assertEqual(tuple(sorted(P.REQUIRED_DISCLOSURES)), DISCLOSURE_AXES)
        for k, toks in P.REQUIRED_DISCLOSURES.items():
            self.assertTrue(toks, f"axis {k} requires no token at all")

    def test_all_axes_are_stated_in_the_shipped_cautions(self):
        self.assertEqual(P.missing_disclosures(P.METHOD), [])

    def test_the_cold_soil_floor_is_quoted_with_its_figures(self):
        blob = " ".join(P.METHOD["cautions"])
        self.assertIn("50°F", blob)
        self.assertIn("60°F", blob)
        self.assertIn("NC State", blob)

    def test_the_trade_is_stated_not_implied(self):
        """The sentence a reader can be harmed by: seed sown into cold, wet soil rots."""
        blob = " ".join(P.METHOD["cautions"]).lower()
        self.assertIn("cold", blob)
        self.assertIn("rot", blob)

    def test_the_seasoned_register_carries_the_trade_too(self):
        s = P.METHOD["how_it_works_seasoned"]
        self.assertIn("50°F", s)
        self.assertIn("rot", s.lower())

    def test_check_REFUSES_cautions_missing_the_cold_soil_trade(self):
        bad = copy.deepcopy(P.METHOD)
        bad["cautions"] = [c for c in bad["cautions"] if "50°F" not in c]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("do not state", out)

    def test_check_REFUSES_cautions_missing_the_not_a_cure_axis(self):
        bad = copy.deepcopy(P.METHOD)
        bad["cautions"] = [c.replace("rather than preventing", "and stops")
                           for c in bad["cautions"]]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not_a_cure", out)

    def test_missing_disclosures_is_not_vacuous(self):
        empty = copy.deepcopy(P.METHOD)
        empty["cautions"] = []
        self.assertEqual(sorted(P.missing_disclosures(empty)), sorted(DISCLOSURE_AXES))


class Contrast(unittest.TestCase):
    """Why this is a new key and not a widening of planting_time_avoidance."""

    def test_the_contrast_table_is_the_frozen_one(self):
        self.assertEqual(tuple(P.REQUIRED_CONTRASTS), CONTRAST_TOKENS)

    def test_best_use_holds_it_apart_from_both_near_misses(self):
        self.assertEqual(P.missing_contrasts(P.METHOD), [])

    def test_the_distinction_is_stated_in_the_right_DIRECTION(self):
        """The widen refusal's substance: the flight window is PUBLISHED, the epidemic is not.
        A best_use that reversed that would pass a token check, so the pairing is asserted."""
        b = P.METHOD["best_use"].lower()
        self.assertIn("no published start date", b)
        self.assertIn("what you plant rather than when", b)

    def test_check_REFUSES_a_best_use_that_drops_a_contrast(self):
        bad = copy.deepcopy(P.METHOD)
        bad["best_use"] = bad["best_use"].replace("weather-driven", "seasonal")
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("does not distinguish", out)

    def test_missing_contrasts_is_not_vacuous(self):
        empty = copy.deepcopy(P.METHOD)
        empty["best_use"] = "A crop with a disease."
        self.assertEqual(sorted(P.missing_contrasts(empty)), sorted(CONTRAST_TOKENS))


class Exclusions(unittest.TestCase):
    """Four problems matched the scan and must never carry the rung."""

    def test_the_exclusion_list_is_the_frozen_four(self):
        self.assertEqual(tuple(P.EXCLUSIONS), EXCLUDED)

    def test_every_exclusion_RESOLVES_in_canonical(self):
        pre = _pre()
        for slug, ident in EXCLUDED:
            self.assertIsNotNone(P.find_problem(pre, slug, ident), f"{slug}/{ident}")

    def test_the_dangerous_exclusion_is_gate_legal(self):
        """spinach/damping-off is typed fungal, so TYPE_TARGETS would ACCEPT the rung there. The
        exclusion list is the only thing standing between this method and advice that causes the
        problem it claims to escape. If this type ever changes, the exclusion may be reviewed."""
        from control_ladder_gate import TYPE_TARGETS
        pre = _pre()
        p = P.find_problem(pre, "spinach", "damping-off")
        self.assertEqual(p.get("type"), "fungal")
        self.assertIn("fungal_foliar", TYPE_TARGETS["fungal"])

    def test_none_of_the_four_is_laddered_with_the_new_key(self):
        post = _post()
        for slug, ident in EXCLUDED:
            p = P.find_problem(post, slug, ident)
            self.assertFalse(any(r.get("method") == KEY
                                 for r in p.get("control_ladder") or []), f"{slug}/{ident}")

    def test_check_REFUSES_an_exclusion_that_does_not_resolve(self):
        bad = tuple(P.EXCLUSIONS) + (("spinach", "no-such-problem"),)
        with swap("EXCLUSIONS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("would protect nothing", out)

    def test_find_problem_matches_by_id_AND_by_name(self):
        pre = _pre()
        self.assertIsNotNone(P.find_problem(pre, "spinach", "damping-off"))       # by id
        self.assertIsNotNone(P.find_problem(pre, "jalapeno", "Mosaic viruses"))   # by name
        self.assertIsNone(P.find_problem(pre, "spinach", "black-rot"))


class Hygiene(unittest.TestCase):
    def test_all_shipped_prose_passes(self):
        for s in P.prose_of(P.METHOD):
            self.assertIsNone(P.hygiene(s), s[:60])

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("the colour will recover"))
        self.assertIsNotNone(P.hygiene("an em dash — here"))
        self.assertIsNotNone(P.hygiene("it is safe for pets"))
        self.assertIsNone(P.hygiene(P.METHOD["best_use"]))

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        bad = copy.deepcopy(P.METHOD)
        bad["pros"] = bad["pros"] + ["This never fails."]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_the_registers_are_materially_different(self):
        self.assertNotEqual(P.METHOD["how_it_works_beginner"], P.METHOD["how_it_works_seasoned"])


class BlastRadius(unittest.TestCase):
    def test_no_crop_changes_at_all(self):
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(b["crops"], a["crops"])

    def test_no_source_changes(self):
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(b["sources"], a["sources"])

    def test_key_sets_are_compared_before_values(self):
        """set(pre) == set(post) FIRST. Iterating pre alone makes every addition invisible."""
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(set(b["methods"]) - set(a["methods"]), {KEY})
        for k in a["methods"]:
            self.assertEqual(b["methods"][k], a["methods"][k], k)

    def test_no_ladder_anywhere_gains_the_rung(self):
        self.assertEqual(P.rungs_of(_post(), KEY), [])

    def test_rungs_of_is_not_vacuous(self):
        """It returns [] on the real post state, so prove it can see a rung at all."""
        post = _post()
        for c in post["crops"]:
            if c.get("slug") == "sweet-corn":
                for p in c.get("diseases") or []:
                    if p.get("id") == "common-rust":
                        p["control_ladder"].append(_rung(KEY))
        self.assertEqual(P.rungs_of(post, KEY), [("sweet-corn", "common-rust")])


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_the_post_state(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_the_catalog_half_of_the_gate_accepts_the_new_entry(self):
        post = _post()
        bad = [v for v in CLG.catalog_violations(post) if KEY in v]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
