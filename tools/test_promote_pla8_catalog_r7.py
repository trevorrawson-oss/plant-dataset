#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_catalog_r7.py. Base 7c3e5d71.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_catalog_r7_suite.py.

THE LOAD-BEARING FAMILY IS `RefusedWidening`, and it guards something the round did NOT do. Both
peas assert in consumer prose, on their highest-severity problem, that planting early prevents
powdery mildew. r5 had already flagged that timing a sowing against a DISEASE was a real practice
awaiting evidence, so this was where it should have arrived. Six T1 documents were read and none
makes the causal claim: they support "plant early because peas are a cool-season crop" and "powdery
mildew comes in the later weather" as separate statements. Assembling a recommendation out of two
true sentences is precisely how this method acquired a wrong criterion at r5.

**A refusal that leaves no trace is indistinguishable from an oversight.** So the refusal is a
guard, asserted in `check` AND `verify_post`, and a test drives it against a doctored catalog where
the target IS present -- because a negative guard that has never seen the thing it forbids has not
been shown to work.

`TierConsistency` is the second half. `biofungicide` is `biological` rather than `soft_chemical`, to
match `bt`: both are living organisms applied as a spray. That is not cosmetic. Tier decides ladder
ORDER, and the whole point of this method is that it sits BELOW sulfur, which is where UC IPM's
"research has not shown these products to be as effective as oils or sulfur" places it. Put it at
`soft_chemical` and it collides with sulfur; put it above and the ladder recommends the weaker
option after the stronger one.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_catalog_r7 as P  # noqa: E402
import build_pla8_catalog_r7_content as C  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402
from source_catalog_title_gate import title_violations  # noqa: E402

POST_SHA = "4a239eefe1d8627b029dc93e9cc5a990078e377eea0a4c8457dcbafe560002a4"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Swap:
    def __init__(self, container, key, value):
        self.c, self.k, self.v = container, key, value

    def __enter__(self):
        self.old = copy.deepcopy(self.c[self.k])
        self.c[self.k] = self.v
        return self

    def __exit__(self, *exc):
        self.c[self.k] = self.old
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

    def test_counts_move_exactly_as_declared(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(len(pre["control_methods"]), 53)
        self.assertEqual(len(post["control_methods"]), 55)
        self.assertEqual(len(pre["source_catalog"]), 213)
        self.assertEqual(len(post["source_catalog"]), 214)

    def test_check_passes_on_the_pinned_base(self):
        self.assertIsNone(P.check(_pre()))


class RefusedWidening(unittest.TestCase):
    """The guard for what this round deliberately did NOT do."""

    def test_planting_time_avoidance_gains_no_disease_target(self):
        key, forbidden = C.REFUSED_WIDENING
        targets = set(_post()["control_methods"][key]["applies_to"])
        self.assertEqual(targets & set(forbidden), set())
        self.assertEqual(sorted(targets), ["insect_boring", "insect_chewing"])

    def test_it_is_still_unreachable_from_every_disease_type(self):
        key, _ = C.REFUSED_WIDENING
        targets = set(_post()["control_methods"][key]["applies_to"])
        for t in ("fungal", "bacterial", "viral"):
            self.assertFalse(targets & set(TYPE_TARGETS[t]),
                             f"{key} became reachable from a {t} problem without a document")

    def test_check_REFUSES_the_target_being_added(self):
        """A negative guard that has never seen the thing it forbids has not been shown to work."""
        pre = _pre()
        pre["control_methods"]["planting_time_avoidance"]["applies_to"].append("fungal_foliar")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("deliberately REFUSED", out)

    def test_verify_post_REFUSES_the_target_being_added_after_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["planting_time_avoidance"]["applies_to"].append("disease_general")
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("REFUSED", out)

    def test_the_refusal_list_is_not_empty(self):
        """An empty forbidden set makes the guard a no-op that still reads as coverage."""
        key, forbidden = C.REFUSED_WIDENING
        self.assertTrue(forbidden)
        self.assertIn("fungal_foliar", forbidden)
        self.assertIn("disease_general", forbidden)


class TierConsistency(unittest.TestCase):
    """Tier decides ladder ORDER, so it is a content decision, not a label."""

    def test_biofungicide_is_biological_like_bt(self):
        post = _post()["control_methods"]
        self.assertEqual(post["biofungicide"]["tier"], "biological")
        self.assertEqual(post["biofungicide"]["tier"], post["bt"]["tier"],
                         "both are living organisms applied as a spray and must share a tier")

    def test_it_sits_BELOW_sulfur_in_the_escalation(self):
        """UC IPM: research has not shown these as effective as oils or sulfur. A ladder must be
        able to put the weaker option first and step past it, which needs the softer tier."""
        post = _post()["control_methods"]
        order = {t: i for i, t in enumerate(P.TIERS)}
        self.assertLess(order[post["biofungicide"]["tier"]], order[post["sulfur"]["tier"]])

    def test_weed_host_control_is_cultural(self):
        self.assertEqual(_post()["control_methods"]["weed_host_control"]["tier"], "cultural")


class ScopeDiscipline(unittest.TestCase):
    def test_weed_host_control_is_not_reachable_by_a_mite(self):
        """`insect_general` was rejected precisely because TYPE_TARGETS maps `mite` to
        {mite, insect_general}. Nothing read here is about mites."""
        targets = set(_post()["control_methods"]["weed_host_control"]["applies_to"])
        self.assertNotIn("insect_general", targets)
        self.assertFalse(targets & set(TYPE_TARGETS["mite"]))

    def test_weed_host_control_reaches_insects_and_fungal_only(self):
        targets = set(_post()["control_methods"]["weed_host_control"]["applies_to"])
        for t in ("insect", "fungal"):
            self.assertTrue(targets & set(TYPE_TARGETS[t]), f"unreachable for {t}")
        for t in ("mite", "mollusk", "bacterial", "viral", "physiological", "nematode", "vertebrate"):
            self.assertFalse(targets & set(TYPE_TARGETS[t]), f"wrongly legal on {t}")

    def test_biofungicide_reaches_fungal_only(self):
        targets = set(_post()["control_methods"]["biofungicide"]["applies_to"])
        self.assertTrue(targets & set(TYPE_TARGETS["fungal"]))
        for t in ("insect", "mite", "mollusk", "bacterial", "viral", "physiological", "nematode",
                  "vertebrate"):
            self.assertFalse(targets & set(TYPE_TARGETS[t]), f"wrongly legal on {t}")

    def test_no_mint_uses_the_universal_target(self):
        for key, m in C.MINTS.items():
            self.assertNotIn(CLG.UNIVERSAL_TARGET, m["applies_to"], key)

    def test_check_REFUSES_a_target_outside_the_vocabulary(self):
        m = copy.deepcopy(C.MINTS["biofungicide"])
        m["applies_to"] = ["fungal_leafy"]
        with _Swap(C.MINTS, "biofungicide", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("vocabulary", out)

    def test_weed_host_control_states_its_split_from_garden_sanitation(self):
        """The nearest neighbour, and the one both bean passes refused to fold it into."""
        bu = _post()["control_methods"]["weed_host_control"]["best_use"]
        self.assertIn("garden", bu.lower())
        self.assertIn("OTHER plants", bu)

    def test_biofungicide_states_its_split_from_sulfur(self):
        bu = _post()["control_methods"]["biofungicide"]["best_use"]
        self.assertIn("sulfur", bu.lower())


class HedgesSurvive(unittest.TestCase):
    def test_each_required_hedge_is_present(self):
        post = _post()["control_methods"]
        for key, hedges in C.REQUIRED_HEDGES.items():
            blob = " ".join(P.prose_of(post[key])).lower()
            for h in hedges:
                self.assertIn(h.lower(), blob, f"{key} dropped the qualifier {h!r}")

    def test_the_efficacy_limit_is_carried_not_softened(self):
        """UC IPM's sentence is the most important one on this sheet: recommending a biofungicide
        without it sells the gentler option as an equal one."""
        m = _post()["control_methods"]["biofungicide"]
        blob = " ".join(P.prose_of(m)).lower()
        self.assertIn("as effective as oils or sulfur", blob)
        self.assertIn("research has not shown", blob)

    def test_check_REFUSES_a_dropped_hedge(self):
        m = copy.deepcopy(C.MINTS["biofungicide"])
        m["how_it_works_seasoned"] = m["how_it_works_seasoned"].replace(
            "as effective as oils or sulfur", "a strong option")
        m["cons"] = [c.replace("as effective as oils or sulfur", "a strong option") for c in m["cons"]]
        with _Swap(C.MINTS, "biofungicide", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("qualifier", out)


class Sourcing(unittest.TestCase):
    def test_every_source_is_T1_and_anchored(self):
        post = _post()
        for key in C.MINTS:
            m = post["control_methods"][key]
            for s in m["sources"]:
                self.assertIn(s, post["source_catalog"], f"{key}: {s}")
                self.assertEqual(post["source_catalog"][s]["tier"], "T1", f"{key}: {s}")
                self.assertIn(s, m["anchoring_urls"], f"{key}: {s}")

    def test_anchors_are_https_with_a_verified_date(self):
        post = _post()
        for key in C.MINTS:
            for sid, a in post["control_methods"][key]["anchoring_urls"].items():
                self.assertTrue(a["url"].startswith("https://"), f"{key}/{sid}")
                self.assertRegex(a["verified"], r"^\d{4}-\d{2}-\d{2}$", f"{key}/{sid}")

    def test_the_two_UC_documents_are_distinct_ids(self):
        """anchoring_urls allows one URL per source id, so a method resting on two UC documents
        needs a document-scoped sibling rather than an overwrite."""
        m = _post()["control_methods"]["weed_host_control"]
        urls = [a["url"] for a in m["anchoring_urls"].values()]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertIn("ucanr_ext", m["sources"])
        self.assertIn("ucanr_ext_thrips", m["sources"])

    def test_the_new_source_passes_A54(self):
        self.assertEqual(title_violations(_post()["source_catalog"]), [])

    def test_check_REFUSES_a_document_scoped_source_without_a_title(self):
        e = copy.deepcopy(C.NEW_SOURCES["ucanr_ext_thrips"])
        e.pop("title")
        with _Swap(C.NEW_SOURCES, "ucanr_ext_thrips", e):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("title", out)

    def test_check_REFUSES_a_mint_declaring_a_non_T1_catalog_source(self):
        m = copy.deepcopy(C.MINTS["biofungicide"])
        m["sources"] = ["ucanr_ext", "almanac"]
        m["anchoring_urls"] = dict(m["anchoring_urls"])
        m["anchoring_urls"].pop("clemson_hgic")
        m["anchoring_urls"]["almanac"] = {"url": "https://example.edu/", "verified": C.VERIFIED}
        with _Swap(C.MINTS, "biofungicide", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not T1", out)

    def test_check_REFUSES_a_declared_source_with_no_anchoring_url(self):
        m = copy.deepcopy(C.MINTS["weed_host_control"])
        m["anchoring_urls"] = {k: v for k, v in m["anchoring_urls"].items() if k != "usu_ext"}
        with _Swap(C.MINTS, "weed_host_control", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("no anchoring_url", out)


class MintShape(unittest.TestCase):
    def test_mints_carry_every_required_field(self):
        post = _post()["control_methods"]
        for key in C.MINTS:
            for f in P.REQUIRED:
                self.assertIn(f, post[key], f"{key} missing {f}")
                self.assertTrue(post[key][f], f"{key}: {f} is empty")

    def test_mints_match_the_gate_required_shape(self):
        from control_ladder_gate import _REQ_METHOD
        post = _post()["control_methods"]
        for key in C.MINTS:
            for f in _REQ_METHOD:
                self.assertIn(f, post[key], f"{key} missing gate-required {f}")

    def test_check_REFUSES_an_invalid_tier(self):
        m = copy.deepcopy(C.MINTS["biofungicide"])
        m["tier"] = "microbial"
        with _Swap(C.MINTS, "biofungicide", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tier", out)

    def test_check_REFUSES_a_missing_required_field(self):
        m = copy.deepcopy(C.MINTS["weed_host_control"])
        m.pop("best_use")
        with _Swap(C.MINTS, "weed_host_control", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("best_use", out)

    def test_check_REFUSES_a_mint_that_already_exists(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already in the catalog", out)


class Hygiene(unittest.TestCase):
    def test_every_authored_string_passes(self):
        post = _post()["control_methods"]
        for key in C.MINTS:
            for s in P.prose_of(post[key]):
                self.assertIsNone(P.hygiene(s), f"{key}: {s[:70]!r}")

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        """A British spelling, not an absolute: there is no earlier absolute check to mask it."""
        m = copy.deepcopy(C.MINTS["weed_host_control"])
        m["pros"] = list(m["pros"]) + ["Keeps the colour of the bed even"]
        with _Swap(C.MINTS, "weed_host_control", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_the_hygiene_function_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("a — dash"))
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("the colour of it"))
        self.assertIsNotNone(P.hygiene("warm to 70 °F"))
        self.assertIsNone(P.hygiene(C.MINTS["biofungicide"]["best_use"]))


class BlastRadius(unittest.TestCase):
    def test_exactly_the_declared_methods_and_sources_are_added(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(set(post["control_methods"]) - set(pre["control_methods"]), set(C.MINTS))
        self.assertEqual(set(pre["control_methods"]) - set(post["control_methods"]), set())
        self.assertEqual(set(post["source_catalog"]) - set(pre["source_catalog"]),
                         set(C.NEW_SOURCES))
        self.assertEqual(set(pre["source_catalog"]) - set(post["source_catalog"]), set())

    def test_no_existing_method_or_source_changes(self):
        pre = _pre()
        post = _post(pre)
        for k, before in pre["control_methods"].items():
            self.assertEqual(post["control_methods"][k], before, k)
        for k, before in pre["source_catalog"].items():
            self.assertEqual(post["source_catalog"][k], before, k)

    def test_no_crop_is_touched(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(json.dumps(post["crops"], sort_keys=True),
                         json.dumps(pre["crops"], sort_keys=True))

    def test_nothing_references_the_new_methods_yet(self):
        post = _post()
        for c in post["crops"]:
            for p in (c.get("pests") or []) + (c.get("diseases") or []):
                for r in p.get("control_ladder") or []:
                    self.assertNotIn(r.get("method"), C.MINTS)

    def test_verify_post_CATCHES_a_touched_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["crops"][0]["name"] = "MUTATED"
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_an_edited_bystander_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["sulfur"]["best_use"] += " Extra."
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("existing method", out)

    def test_verify_post_CATCHES_an_edited_bystander_source(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["source_catalog"]["usu_ext"]["accessed"] = "2099-01"
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("existing source", out)

    def test_verify_post_CATCHES_an_extra_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["smuggled"] = dict(C.MINTS["biofungicide"])
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
    def test_gates_are_clean_on_the_post_state(self):
        post = _post()
        self.assertEqual(CLG.catalog_violations(CLG.catalog(post)), [])
        self.assertEqual(CLG.all_violations(post), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
