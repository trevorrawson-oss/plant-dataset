#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_mancozeb.py. Base b6d36611 (batch 13's output, a commit).

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.

`Disclosure` is the safety family: water H, the Prop 65 / EPA carcinogen listing, the PPE note,
the 5 day PHI, and the UNRATED natural-enemies axis. `InventedRating` is this mint's own family:
chlorothalonil earns a "natural enemies Low" pro and mancozeb does NOT (UC IPM shows no rating),
so any sentence claiming that advantage is the neem invented-rating shape and is refused.
"""
import copy, hashlib, json, os, sys, unittest
from contextlib import contextmanager

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_mancozeb as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "4c5a79d34a435117adee9723242d1846a04045eda739226e6b3419892644c739"

# FROZEN LITERALS -- restated, never derived from P.
KEY = "mancozeb"
TIER = "conventional"
APPLIES_TO = ["fungal_foliar"]
DISCLOSURE_AXES = ("aquatic", "carcinogen", "phi", "ppe", "unrated")
SOURCES = ["ucanr_ext", "clemson_hgic"]


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
    """One driver per branch of verify_post, each asserting its ONE message."""

    def _staged(self):
        pre = _pre()
        return P.snapshot(pre), _post(pre)

    def test_unminted_method_is_caught(self):
        snap, post = self._staged()
        del post["control_methods"][KEY]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("was not minted", out)

    def test_stripped_disclosure_is_caught(self):
        snap, post = self._staged()
        m = post["control_methods"][KEY]
        m["cautions"] = [c for c in m["cautions"] if "Prop 65" not in c]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("do not state", out)
        self.assertIn("carcinogen", out)

    def test_an_invented_enemy_rating_is_caught(self):
        """The neem shape: a sentence claiming the natural-enemies Low advantage the database
        does not carry for this ingredient."""
        snap, post = self._staged()
        m = post["control_methods"][KEY]
        m["pros"] = m["pros"] + ["Rated Low risk to natural enemies, so predators keep working"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("claims a natural-enemies rating", out)

    def test_widened_applies_to_is_caught(self):
        snap, post = self._staged()
        post["control_methods"][KEY]["applies_to"] = ["fungal_foliar", "fungal_soilborne"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("not the narrow scope", out)

    def test_wrong_tier_is_caught(self):
        snap, post = self._staged()
        post["control_methods"][KEY]["tier"] = "soft_chemical"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("tier is not conventional", out)

    def test_non_verbatim_landing_is_caught(self):
        snap, post = self._staged()
        post["control_methods"][KEY]["name"] = "Mancozeb fungicide"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("did not land verbatim", out)

    def test_a_rung_landing_here_is_caught(self):
        snap, post = self._staged()
        for c in post["crops"]:
            if c.get("slug") == "watermelon":
                for p in c.get("diseases") or []:
                    if p.get("name") == "Anthracnose":
                        p["control_ladder"] = [_rung(KEY)]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("mints only", out)

    def test_a_second_added_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"]["ghost_method"] = copy.deepcopy(P.METHOD)
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("methods added", out)

    def test_a_dropped_method_is_caught(self):
        snap, post = self._staged()
        del post["control_methods"]["chlorothalonil"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("was dropped", out)

    def test_an_edited_existing_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"]["chlorothalonil"]["best_use"] += " x"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("only mints", out)

    def test_a_touched_source_is_caught(self):
        snap, post = self._staged()
        post["source_catalog"]["clemson_hgic"]["accessed"] = "2099-01"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("source_catalog changed", out)

    def test_a_touched_crop_is_caught(self):
        snap, post = self._staged()
        for c in post["crops"]:
            if c.get("slug") == "okra":
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

    def test_it_is_legal_on_fungal_problems(self):
        from control_ladder_gate import TYPE_TARGETS
        self.assertTrue(set(P.METHOD["applies_to"]) & TYPE_TARGETS["fungal"])

    def test_check_REFUSES_a_softer_tier(self):
        bad = copy.deepcopy(P.METHOD)
        bad["tier"] = "soft_chemical"
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("understates what it is", out)

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

    def test_the_uc_ipm_anchor_is_the_ingredient_record(self):
        self.assertIn("uaiKey=30", P.METHOD["anchoring_urls"]["ucanr_ext"]["url"])

    def test_check_REFUSES_an_unanchored_source(self):
        bad = copy.deepcopy(P.METHOD)
        del bad["anchoring_urls"]["clemson_hgic"]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("has no anchoring_url", out)


class Disclosure(unittest.TestCase):
    def test_the_axis_table_is_the_frozen_one(self):
        self.assertEqual(tuple(sorted(P.REQUIRED_DISCLOSURES)), DISCLOSURE_AXES)
        for k, toks in P.REQUIRED_DISCLOSURES.items():
            self.assertTrue(toks, f"axis {k} requires no token at all")

    def test_all_axes_are_stated_in_the_shipped_cautions(self):
        self.assertEqual(P.missing_disclosures(P.METHOD), [])

    def test_the_profile_figures_are_stated_where_they_belong(self):
        """water H + Prop 65/EPA in the cautions; acute L/CAUTION and bees-low as honest pros."""
        cautions = " ".join(P.METHOD["cautions"])
        self.assertIn("High for water quality", cautions)
        self.assertIn("Prop 65", cautions)
        pros = " ".join(P.METHOD["pros"])
        self.assertIn("CAUTION signal-word band", pros)
        self.assertIn("low impact on honey bees", pros)

    def test_the_phi_names_five_days(self):
        blob = " ".join(P.METHOD["cautions"]).lower()
        self.assertIn("5 day pre-harvest interval", blob)

    def test_check_REFUSES_cautions_missing_the_unrated_axis(self):
        bad = copy.deepcopy(P.METHOD)
        bad["cautions"] = [c for c in bad["cautions"] if "Unrated is not the same" not in c]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("do not state", out)
        self.assertIn("unrated", out)

    def test_missing_disclosures_is_not_vacuous(self):
        empty = copy.deepcopy(P.METHOD)
        empty["cautions"] = []
        self.assertEqual(sorted(P.missing_disclosures(empty)), sorted(DISCLOSURE_AXES))


class InventedRating(unittest.TestCase):
    """UC IPM shows NO natural-enemies rating for mancozeb; claiming one is the neem shape."""

    def test_the_shipped_entry_makes_no_such_claim(self):
        self.assertIsNone(P.invented_enemy_rating(P.METHOD))

    def test_the_legitimate_unrated_sentences_pass(self):
        """The cons and cautions mention 'natural enemies ... low' only to say unrated != low;
        those must NOT trip the guard, or the honest disclosure becomes unwritable."""
        blob = " ".join(P.prose_of(P.METHOD)).lower()
        self.assertIn("unrated is not the same as low", blob)
        self.assertIsNone(P.invented_enemy_rating(P.METHOD))

    def test_check_REFUSES_the_sibling_pro_pasted_in(self):
        bad = copy.deepcopy(P.METHOD)
        bad["pros"] = bad["pros"] + [
            "Rated Low risk to natural enemies, so it does not strip out the predators"]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("natural-enemies rating the database does not carry", out)

    def test_the_detector_is_not_vacuous(self):
        fake = {"pros": ["natural enemies risk is Low here"]}
        self.assertIsNotNone(P.invented_enemy_rating(fake))


class Hygiene(unittest.TestCase):
    def test_all_shipped_prose_passes(self):
        for s in P.prose_of(P.METHOD):
            self.assertIsNone(P.hygiene(s), s[:60])

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("an em dash — here"))
        self.assertIsNotNone(P.hygiene("it is safe for pets"))

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
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(set(b["methods"]) - set(a["methods"]), {KEY})
        for k in a["methods"]:
            self.assertEqual(b["methods"][k], a["methods"][k], k)

    def test_no_ladder_anywhere_gains_the_rung(self):
        self.assertEqual(P.rungs_of(_post(), KEY), [])

    def test_rungs_of_is_not_vacuous(self):
        post = _post()
        for c in post["crops"]:
            if c.get("slug") == "watermelon":
                for p in c.get("diseases") or []:
                    if p.get("name") == "Anthracnose":
                        p["control_ladder"] = [_rung(KEY)]
        self.assertEqual(P.rungs_of(post, KEY), [("watermelon", "Anthracnose")])


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_the_post_state(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_the_catalog_half_of_the_gate_accepts_the_new_entry(self):
        post = _post()
        bad = [v for v in CLG.catalog_violations(post) if KEY in v]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
