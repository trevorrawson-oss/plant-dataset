#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_chlorothalonil.py. Base 3a87737a.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + the mutation harness.

THE LOAD-BEARING FAMILY IS `Disclosures`, and it is the reason this method is safe to ship at all.
Everything else in this catalog can be wrong and cost a reader a crop. This one can be wrong and
cost them something else: it is a synthetic on the DANGER signal-word band, rated High for water
quality and High for acute toxicity, and carried on both the California Prop 65 list and the US EPA
list, where an active ingredient appears only as a likely or confirmed carcinogen.

Trevor's ruling (2026-08-26) is that a product people can buy off a shelf gets named, with the
profile stated. That ruling only holds if the profile is ACTUALLY stated, so each hazard axis is
asserted individually and each has its own refusal test. Removing any single one must be refused BY
NAME -- a guard that only counted the cautions, or checked that "some" hazard language was present,
would let the carcinogen line quietly disappear while staying green.

`ScopeAndTier` is the second half. `conventional` is not a label here, it is what puts this at the
END of an escalation and keeps it out of the first thing a reader sees; and `applies_to` is exactly
`fungal_foliar` because every one of the eleven problems naming this material is a foliar fungal
disease. A wider scope would put a DANGER-band synthetic in front of readers whose own sources never
mention it.

`NothingUsesItYet` pins the deliberate split: this promote mints the key and touches no ladder. The
nine shipped ladders that name chlorothalonil in their prose are amended by a SEPARATE promote, so
that adding a conventional rung to certified crops is its own reviewable act.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_chlorothalonil as P  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "93e32e2b49d9e064b0d687dd5814260186fb71341f072a27b8eec36fa0d578ed"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Swap:
    def __init__(self, name, value):
        self.n, self.v = name, value

    def __enter__(self):
        self.old = copy.deepcopy(getattr(P, self.n))
        setattr(P, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(P, self.n, self.old)
        return False


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

    def test_catalog_goes_55_to_56(self):
        pre = _pre()
        self.assertEqual(len(pre["control_methods"]), 55)
        self.assertEqual(len(_post(pre)["control_methods"]), 56)

    def test_check_passes_on_the_pinned_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_the_gap_it_closes_is_real(self):
        """Before this mint, NOTHING conventional could reach a fungal problem."""
        cm = _pre()["control_methods"]
        conv = [k for k, v in cm.items() if v["tier"] == "conventional"]
        self.assertEqual(sorted(conv), ["carbaryl", "pyrethroid"])
        for k in conv:
            self.assertFalse(set(cm[k]["applies_to"]) & set(TYPE_TARGETS["fungal"]),
                             f"{k} already reaches a fungal problem, so the gap is not what is claimed")


class Disclosures(unittest.TestCase):
    """Every hazard axis, asserted individually and refusable individually."""

    def test_all_axes_are_stated_in_the_shipped_cautions(self):
        m = _post()["control_methods"][P.KEY]
        self.assertEqual(P.missing_disclosures(m), [])

    def test_the_axis_list_is_not_empty(self):
        """A COVERAGE assertion: an emptied table makes missing_disclosures() return [] for any
        input at all, which is the vacuous-pass shape."""
        self.assertGreaterEqual(len(P.REQUIRED_DISCLOSURES), 6)
        for k, toks in P.REQUIRED_DISCLOSURES.items():
            self.assertTrue(toks, f"{k} declares no tokens, so it can never fail")

    def test_the_carcinogen_line_is_present_and_specific(self):
        """The disclosure this catalog has never carried before. It must name both lists rather
        than gesturing at 'health concerns'."""
        blob = " ".join(_post()["control_methods"][P.KEY]["cautions"]).lower()
        self.assertIn("prop 65", blob)
        self.assertIn("epa", blob)
        self.assertIn("carcinogen", blob)

    def test_the_acute_line_names_the_signal_word_band(self):
        blob = " ".join(_post()["control_methods"][P.KEY]["cautions"]).lower()
        self.assertIn("danger", blob)
        self.assertIn("acute toxicity", blob)

    def test_removing_ANY_single_axis_is_refused_by_name(self):
        """Each axis drives its own refusal. A guard that only counted cautions, or looked for
        'some' hazard language, would let the carcinogen line vanish while staying green."""
        for axis, tokens in P.REQUIRED_DISCLOSURES.items():
            m = copy.deepcopy(P.METHOD)
            m["cautions"] = [c for c in m["cautions"]
                             if not all(t in c.lower() for t in tokens)]
            with _Swap("METHOD", m):
                out = P.check(_pre())
            self.assertIsNotNone(out, f"dropping the {axis} disclosure was not refused")
            self.assertIn(axis, out, f"the refusal for {axis} does not name it")

    def test_check_REFUSES_a_caution_that_states_HALF_an_axis(self):
        """ALL tokens, not ANY. A caution naming acute toxicity while dropping the DANGER band
        understates the material, and an ANY test would accept it. The harness caught that the
        per-axis deletion tests above cannot tell ALL from ANY, because deleting a whole caution
        removes every token at once."""
        m = copy.deepcopy(P.METHOD)
        m["cautions"] = [c for c in m["cautions"] if "danger" not in c.lower()]
        m["cautions"].append("UC IPM rates its acute toxicity to people and other mammals as high.")
        with _Swap("METHOD", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("acute", out)

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        """Drives check()'s hygiene SWEEP. The post-state assertion below proves the FUNCTION works;
        only this proves the promote actually runs it over the authored prose."""
        m = copy.deepcopy(P.METHOD)
        m["pros"] = list(m["pros"]) + ["Keeps the colour of the leaf even"]
        with _Swap("METHOD", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_verify_post_REFUSES_a_stripped_caution_after_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"][P.KEY]["cautions"] = ["Read the label."]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("do not state", out)

    def test_the_beginner_register_does_not_undersell_it(self):
        """A beginner who reads only the plain half must still learn this is the heavy end."""
        b = _post()["control_methods"][P.KEY]["how_it_works_beginner"].lower()
        self.assertIn("heaviest warnings", b)
        self.assertIn("end of the list", b)

    def test_no_absolute_safety_language_anywhere(self):
        """The PLA-253 class. On a DANGER-band synthetic it would be the worst possible place."""
        for s in P.prose_of(_post()["control_methods"][P.KEY]):
            self.assertIsNone(P.hygiene(s), s[:70])


class ScopeAndTier(unittest.TestCase):
    def test_tier_is_conventional(self):
        self.assertEqual(_post()["control_methods"][P.KEY]["tier"], "conventional")

    def test_check_REFUSES_a_softer_tier(self):
        m = copy.deepcopy(P.METHOD)
        m["tier"] = "soft_chemical"
        with _Swap("METHOD", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("understates", out)

    def test_it_sits_ABOVE_copper_and_sulfur(self):
        """Tier decides ladder order, and the whole editorial point is that the softer options are
        exhausted first."""
        post = _post()["control_methods"]
        order = {t: i for i, t in enumerate(P.TIERS)}
        for softer in ("copper_fungicide", "sulfur", "biofungicide"):
            self.assertLess(order[post[softer]["tier"]], order[post[P.KEY]["tier"]], softer)

    def test_applies_to_is_exactly_fungal_foliar(self):
        self.assertEqual(_post()["control_methods"][P.KEY]["applies_to"], ["fungal_foliar"])

    def test_it_is_unreachable_from_every_non_fungal_type(self):
        targets = set(_post()["control_methods"][P.KEY]["applies_to"])
        self.assertTrue(targets & set(TYPE_TARGETS["fungal"]))
        for t in ("insect", "mite", "mollusk", "bacterial", "viral", "physiological", "nematode",
                  "vertebrate"):
            self.assertFalse(targets & set(TYPE_TARGETS[t]), f"wrongly legal on {t}")

    def test_check_REFUSES_a_wider_scope(self):
        m = copy.deepcopy(P.METHOD)
        m["applies_to"] = ["fungal_foliar", "disease_general"]
        with _Swap("METHOD", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("fungal_foliar", out)

    def test_best_use_frames_it_as_a_last_resort_and_says_declining_is_fine(self):
        bu = _post()["control_methods"][P.KEY]["best_use"].lower()
        self.assertIn("last resort", bu)
        self.assertIn("declines", bu)


class Sourcing(unittest.TestCase):
    def test_sources_are_T1_and_anchored(self):
        post = _post()
        m = post["control_methods"][P.KEY]
        for s in m["sources"]:
            self.assertIn(s, post["source_catalog"])
            self.assertEqual(post["source_catalog"][s]["tier"], "T1", s)
            self.assertIn(s, m["anchoring_urls"], s)

    def test_the_uc_ipm_anchor_is_the_active_ingredient_page(self):
        """Not the database index. The index was what a fetch resolved to, and it carries no
        hazard content at all."""
        u = _post()["control_methods"][P.KEY]["anchoring_urls"]["ucanr_ext"]["url"]
        self.assertIn("active-ingredient-details", u)
        self.assertIn("uaiKey", u)

    def test_check_REFUSES_a_non_T1_source(self):
        m = copy.deepcopy(P.METHOD)
        m["sources"] = ["ucanr_ext", "almanac"]
        m["anchoring_urls"] = dict(m["anchoring_urls"])
        m["anchoring_urls"].pop("clemson_hgic")
        m["anchoring_urls"]["almanac"] = {"url": "https://example.edu/", "verified": P.VERIFIED}
        with _Swap("METHOD", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not T1", out)

    def test_check_REFUSES_a_source_with_no_anchor(self):
        m = copy.deepcopy(P.METHOD)
        m["anchoring_urls"] = {k: v for k, v in m["anchoring_urls"].items() if k != "clemson_hgic"}
        with _Swap("METHOD", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("no anchoring_url", out)


class MintShape(unittest.TestCase):
    def test_every_required_field_present(self):
        post = _post()["control_methods"][P.KEY]
        for f in P.REQUIRED:
            self.assertIn(f, post)
            self.assertTrue(post[f], f)

    def test_gate_required_shape(self):
        from control_ladder_gate import _REQ_METHOD
        post = _post()["control_methods"][P.KEY]
        for f in _REQ_METHOD:
            self.assertIn(f, post, f)

    def test_check_REFUSES_a_missing_field(self):
        m = copy.deepcopy(P.METHOD)
        m.pop("best_use")
        with _Swap("METHOD", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("best_use", out)

    def test_check_REFUSES_running_over_its_own_output(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already in the catalog", out)

    def test_find_it_beginner_names_the_shelf_products(self):
        """The evidence that decided this: it is on the shelf."""
        f = _post()["control_methods"][P.KEY]["find_it_beginner"]
        self.assertIn("Daconil", f)
        self.assertIn("chlorothalonil", f)


class NothingUsesItYet(unittest.TestCase):
    """The mint and the rungs are deliberately separate promotes."""

    def test_no_ladder_references_it(self):
        for c in _post()["crops"]:
            for p in (c.get("pests") or []) + (c.get("diseases") or []):
                if not isinstance(p, dict):
                    continue
                for r in p.get("control_ladder") or []:
                    self.assertNotEqual(r.get("method"), P.KEY)

    def test_the_nine_ladders_it_will_amend_are_unchanged_here(self):
        pre = _pre()
        post = _post(pre)
        pb = {c["slug"]: c for c in pre["crops"]}
        qb = {c["slug"]: c for c in post["crops"]}
        for slug in ("cucumber", "slicing-cucumber", "pickling-cucumber",
                     "green-beans-bush", "pole-beans", "dry-bean"):
            self.assertEqual(json.dumps(qb[slug], sort_keys=True),
                             json.dumps(pb[slug], sort_keys=True), slug)

    def test_the_population_awaiting_the_backfill_is_what_was_measured(self):
        """Nine laddered problems name this material in their prose. If that count moves, the
        backfill promote's scope moves with it."""
        n = 0
        for c in _post()["crops"]:
            for p in (c.get("pests") or []) + (c.get("diseases") or []):
                if not isinstance(p, dict) or not p.get("control_ladder"):
                    continue
                blob = " ".join(str(v) for k, v in p.items() if isinstance(v, str)).lower()
                if "chlorothalonil" in blob:
                    n += 1
        self.assertEqual(n, 9)


class BlastRadius(unittest.TestCase):
    def test_only_the_new_key_is_added(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(set(post["control_methods"]) - set(pre["control_methods"]), {P.KEY})
        self.assertEqual(set(pre["control_methods"]) - set(post["control_methods"]), set())

    def test_no_existing_method_changes(self):
        pre = _pre()
        post = _post(pre)
        for k, v in pre["control_methods"].items():
            self.assertEqual(post["control_methods"][k], v, k)

    def test_sources_and_crops_untouched(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(json.dumps(post["source_catalog"], sort_keys=True),
                         json.dumps(pre["source_catalog"], sort_keys=True))
        self.assertEqual(json.dumps(post["crops"], sort_keys=True),
                         json.dumps(pre["crops"], sort_keys=True))

    def test_verify_post_CATCHES_a_widened_scope_after_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"][P.KEY]["applies_to"] = ["fungal_foliar", "disease_general"]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("narrow scope", out)

    def test_verify_post_CATCHES_a_softened_tier_after_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"][P.KEY]["tier"] = "soft_chemical"
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("not conventional", out)

    def test_verify_post_CATCHES_an_extra_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["smuggled"] = copy.deepcopy(P.METHOD)
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("expected exactly", out)

    def test_verify_post_CATCHES_a_touched_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["crops"][0]["name"] = "MUTATED"
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("separate promote", out)

    def test_verify_post_CATCHES_an_edited_bystander(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["sulfur"]["best_use"] += " Extra."
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("existing method", out)

    def test_verify_post_CATCHES_a_touched_source(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["source_catalog"]["clemson_hgic"]["accessed"] = "2099-01"
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_dropped_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        del d["control_methods"]["kaolin_clay"]
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_is_clean_on_the_real_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(P.snapshot(pre), d))


class GateContract(unittest.TestCase):
    def test_gates_clean_on_the_post_state(self):
        post = _post()
        self.assertEqual(CLG.catalog_violations(CLG.catalog(post)), [])
        self.assertEqual(CLG.all_violations(post), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
