#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_catalog_r5.py. Base e794969f.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_catalog_r5_suite.py.

THE LOAD-BEARING FAMILY IS `WideningCarriesItsEvidence`. Two of the four changes here are WIDENINGS
of methods that already ship, and a widening is the one catalog operation that can be wrong while
every structural gate stays green. `balance_nitrogen` reaching a fungal disease while every sentence
of its prose is about aphids is exactly the `bottom_watering` defect -- right key, wrong meaning,
twelve rungs deep before anybody read it. So the suite asserts the prose moved WITH the target, in
both directions: the new evidence is present, and the old case was not thrown away to make room.

`ScopeDiscipline` is the second half. Both mints were deliberately scoped NARROWER than the nearest
plausible reading: `wet_foliage_discipline` is bacterial + fungal_foliar and NOT `disease_general`,
because handling does move some viruses but nothing was read for it; `planting_time_avoidance` is
insects only, because both documented cases are insects with a defined emergence window. A target
added on plausibility rather than on a document is the shape this arc keeps having to undo.

`HedgesSurvive` carries a NEGATIVE guard the others do not have. UMN states the squash outcome as
"will not suffer any damage" while Clemson hedges the same mechanism with "may escape damage". The
weaker source governs, so the suite asserts the hedge is present AND that UMN's absolute never
reaches consumer prose.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_catalog_r5 as P  # noqa: E402
import build_pla8_catalog_r5_content as C  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402
from source_catalog_title_gate import title_violations  # noqa: E402

POST_SHA = "48478cb5f62edd284674be3f16a7a08c2537d7d510c19c5e3d89517748c973b1"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Swap:
    """Temporarily replace a value inside the content module, restoring it however the test ends."""

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
        """The post is this promote's OWN replayed output, never live canonical."""
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)

    def test_counts_move_exactly_as_declared(self):
        pre, post = _pre(), None
        post = _post(pre)
        self.assertEqual(len(pre["control_methods"]), 51)
        self.assertEqual(len(post["control_methods"]), 53)
        self.assertEqual(len(pre["source_catalog"]), 212)
        self.assertEqual(len(post["source_catalog"]), 213)

    def test_check_passes_on_the_pinned_base(self):
        self.assertIsNone(P.check(_pre()))


class ScopeDiscipline(unittest.TestCase):
    """Each mint is scoped to what was READ, not to what is plausible."""

    def test_wet_foliage_is_not_disease_general(self):
        """disease_general would reach viral problems. Handling does move some viruses; nothing
        was read for it here, so the method does not claim it."""
        targets = set(_post()["control_methods"]["wet_foliage_discipline"]["applies_to"])
        self.assertNotIn("disease_general", targets)
        self.assertNotIn("any", targets)
        self.assertFalse(targets & set(TYPE_TARGETS["viral"]),
                         "wet_foliage_discipline is reachable by a viral problem, unsourced")

    def test_wet_foliage_reaches_exactly_bacterial_and_fungal(self):
        targets = set(_post()["control_methods"]["wet_foliage_discipline"]["applies_to"])
        for t in ("bacterial", "fungal"):
            self.assertTrue(targets & set(TYPE_TARGETS[t]), f"unreachable for {t}")
        for t in ("insect", "mite", "mollusk", "physiological", "nematode", "vertebrate", "viral"):
            self.assertFalse(targets & set(TYPE_TARGETS[t]), f"wrongly legal on {t}")

    def test_planting_time_reaches_insects_only(self):
        targets = set(_post()["control_methods"]["planting_time_avoidance"]["applies_to"])
        self.assertTrue(targets & set(TYPE_TARGETS["insect"]))
        for t in ("fungal", "bacterial", "viral", "mollusk", "physiological", "nematode",
                  "vertebrate", "mite"):
            self.assertFalse(targets & set(TYPE_TARGETS[t]), f"wrongly legal on {t}")

    def test_no_mint_uses_the_universal_target(self):
        """`any` is what a method reaches for when its scope was never decided."""
        for key, m in C.MINTS.items():
            self.assertNotIn(CLG.UNIVERSAL_TARGET, m["applies_to"], key)

    def test_every_target_is_in_the_gate_vocabulary(self):
        """A target the gate does not know is a target no problem can reach: a dead method."""
        vocab = P.gate_vocabulary()
        for key, m in _post()["control_methods"].items():
            for t in m.get("applies_to") or []:
                self.assertIn(t, vocab, f"{key} declares unknown target {t!r}")

    def test_check_REFUSES_a_target_outside_the_vocabulary(self):
        m = copy.deepcopy(C.MINTS["wet_foliage_discipline"])
        m["applies_to"] = ["fungal_leafy"]
        with _Swap(C.MINTS, "wet_foliage_discipline", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("vocabulary", out)

    def test_planting_time_is_not_a_second_crop_rotation(self):
        """Both move the planting. One moves it in space, one in time; if they ever cover the same
        ground the distinction that justifies the mint has collapsed."""
        post = _post()["control_methods"]
        self.assertNotEqual(set(post["planting_time_avoidance"]["applies_to"]),
                            set(post["crop_rotation"]["applies_to"]))
        self.assertIn("in time", post["planting_time_avoidance"]["best_use"])

    def test_wet_foliage_states_its_split_from_water_at_the_base(self):
        """The nearest neighbour. One changes where the water goes, the other where you go."""
        bu = _post()["control_methods"]["wet_foliage_discipline"]["best_use"]
        self.assertIn("watering at the base", bu)
        self.assertIn("where you go", bu)


class WideningCarriesItsEvidence(unittest.TestCase):
    """A widened target over unwidened prose is the bottom_watering defect. Both must move."""

    def test_balance_nitrogen_prose_reaches_the_disease_side(self):
        m = _post()["control_methods"]["balance_nitrogen"]
        blob = " ".join(P.prose_of(m)).lower()
        self.assertIn("canopy", blob)
        self.assertIn("white mold", blob)

    def test_balance_nitrogen_still_covers_aphids(self):
        """The widening must not throw away the case the method was built for."""
        m = _post()["control_methods"]["balance_nitrogen"]
        blob = " ".join(P.prose_of(m)).lower()
        self.assertIn("aphid", blob)
        self.assertIn("insect_soft_bodied", m["applies_to"])

    def test_augmentative_release_prose_reaches_the_parasitoid_case(self):
        m = _post()["control_methods"]["augmentative_release"]
        blob = " ".join(P.prose_of(m)).lower()
        self.assertIn("pediobius", blob)
        self.assertIn("beetle", blob)

    def test_augmentative_release_still_covers_the_mite_predators(self):
        m = _post()["control_methods"]["augmentative_release"]
        blob = " ".join(P.prose_of(m)).lower()
        self.assertIn("phytoseiulus", blob)
        self.assertIn("mite", m["applies_to"])

    def test_check_REFUSES_a_widening_whose_prose_does_not_mention_its_evidence(self):
        """THE STRIPPED PROSE KEEPS THE HEDGE ON PURPOSE, and the assertion names G5's own words.

        The first version of this test dropped the hedge along with the evidence, so the HEDGE
        check fired first and the test passed green with G5 disabled -- three mutations survived
        behind it. The evidence tokens are 'canopy' and 'white mold'; the hedge is 'can produce
        excessive canopies', which contains neither ('canopy' is not a substring of 'canopies').
        So this input is refusable by G5 and by nothing else."""
        w = copy.deepcopy(C.WIDENINGS["balance_nitrogen"])
        w["prose"]["how_it_works_beginner"] = "Avoid overfeeding with high-nitrogen fertilizer."
        w["prose"]["how_it_works_seasoned"] = (
            "Excess nitrogen drives flushes of tender growth aphids feed on. UC IPM's dry bean "
            "guidance is to avoid heavy applications of nitrogen, which can produce excessive "
            "canopies.")
        w["prose"]["best_use"] = "A preventive feeding habit anywhere aphids turn up most years."
        w["prose"]["pros"] = ["Costs nothing; it is simply not overfeeding",
                              "Improves plant health and lowers aphid pressure"]
        w["prose"]["cons"] = ["Preventive only; it will not clear an established colony",
                              "Underfeeding hurts yield, so it is a balance, not a cut"]
        with _Swap(C.WIDENINGS, "balance_nitrogen", w):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("never mentions", out)
        self.assertIn("balance_nitrogen", out)

    def test_every_widening_declares_nonempty_evidence_tokens(self):
        """A COVERAGE assertion, not an overlap one: every widened method must be listed in
        WIDENING_EVIDENCE with at least one real token, so a third widening added later cannot
        arrive with G5 silently switched off for it. An empty tuple makes G5 a no-op for that
        key while the loop still runs and the suite still passes."""
        for key in C.WIDENINGS:
            self.assertIn(key, P.WIDENING_EVIDENCE, f"{key} has no G5 evidence tokens")
            tokens = P.WIDENING_EVIDENCE[key]
            self.assertTrue(tokens, f"{key} declares an EMPTY evidence tuple, so G5 cannot fire")
            for t in tokens:
                self.assertTrue(str(t).strip(), f"{key} declares a blank evidence token")
        self.assertEqual(set(P.WIDENING_EVIDENCE), set(C.WIDENINGS))

    def test_check_REFUSES_an_augmentative_release_widening_without_its_evidence(self):
        """The symmetric case to balance_nitrogen above. Reachability has to be shown per key:
        one key's refusal test says nothing about the other key's tokens. The stripped prose keeps
        UMD's scale hedge, which contains neither evidence token, so only G5 can object."""
        w = copy.deepcopy(C.WIDENINGS["augmentative_release"])
        w["prose"]["how_it_works_beginner"] = (
            "You can buy predatory insects and mites and release them onto an active infestation. "
            "It can help, but the predators need prey already present or they starve or move on.")
        w["prose"]["how_it_works_seasoned"] = (
            "Augmentative release supplements resident natural enemies rather than substituting "
            "for them. Released predators starve or migrate elsewhere if prey is not available "
            "when they arrive. UMD calls it most practical in large plantings or community "
            "gardens, which is the scale limit worth carrying into any home-garden decision.")
        with _Swap(C.WIDENINGS, "augmentative_release", w):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("never mentions", out)
        self.assertIn("augmentative_release", out)

    def test_check_REFUSES_a_widening_target_outside_the_vocabulary(self):
        """G1's vocabulary check covers mints. This is the widening branch, which nothing else
        drives: a target the gate does not know makes the WIDENING dead, not the mint."""
        w = copy.deepcopy(C.WIDENINGS["augmentative_release"])
        w["add_applies_to"] = ["insect_leaf_eating"]
        with _Swap(C.WIDENINGS, "augmentative_release", w):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("vocabulary", out)

    def test_apply_RAISES_on_an_anchor_collision(self):
        """check() refuses this first, so the apply-side raise is unreachable through the promote.
        Drive it directly: it is the last line of defense if check is ever reordered or relaxed."""
        w = copy.deepcopy(C.WIDENINGS["balance_nitrogen"])
        w["add_sources"] = ["ucanr_ext"]
        w["add_anchoring_urls"] = {"ucanr_ext": {"url": "https://example.edu/x",
                                                 "verified": C.VERIFIED}}
        with _Swap(C.WIDENINGS, "balance_nitrogen", w):
            with self.assertRaises(AssertionError) as cm:
                P.apply_to(copy.deepcopy(_pre()))
        self.assertIn("never overwrite", str(cm.exception))

    def test_check_REFUSES_a_widening_that_adds_no_target(self):
        w = copy.deepcopy(C.WIDENINGS["augmentative_release"])
        w["add_applies_to"] = []
        with _Swap(C.WIDENINGS, "augmentative_release", w):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("no target", out)

    def test_check_REFUSES_a_target_the_method_already_has(self):
        w = copy.deepcopy(C.WIDENINGS["augmentative_release"])
        w["add_applies_to"] = ["mite"]
        with _Swap(C.WIDENINGS, "augmentative_release", w):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("already applies", out)

    def test_widening_never_overwrites_an_existing_anchor(self):
        """anchoring_urls allows one URL per source id. Clobbering the existing anchor silently
        drops the document the method was originally built on. (PLA-253 rule.)"""
        pre, post = _pre(), None
        post = _post(pre)
        for key in C.WIDENINGS:
            before = pre["control_methods"][key]["anchoring_urls"]
            after = post["control_methods"][key]["anchoring_urls"]
            for sid, a in before.items():
                self.assertEqual(after.get(sid), a, f"{key} overwrote the anchor for {sid}")

    def test_check_REFUSES_an_anchor_overwrite(self):
        w = copy.deepcopy(C.WIDENINGS["balance_nitrogen"])
        w["add_anchoring_urls"] = {"ucanr_ext": {"url": "https://example.edu/x",
                                                 "verified": C.VERIFIED}}
        w["add_sources"] = ["ucanr_ext"]
        with _Swap(C.WIDENINGS, "balance_nitrogen", w):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("never overwrite", out)


class HedgesSurvive(unittest.TestCase):
    """Every qualifier these four documents attach, and the one absolute that must not travel."""

    def test_each_required_hedge_is_present(self):
        post = _post()["control_methods"]
        for key, hedges in C.REQUIRED_HEDGES.items():
            blob = " ".join(P.prose_of(post[key])).lower()
            for h in hedges:
                self.assertIn(h.lower(), blob, f"{key} dropped the qualifier {h!r}")

    def test_umn_absolute_never_reaches_consumer_prose(self):
        """UMN: 'will not suffer any damage'. Clemson hedges the same mechanism. Weaker governs."""
        for m in _post()["control_methods"].values():
            for s in P.prose_of(m):
                self.assertNotIn(C.FORBIDDEN_ABSOLUTE.lower(), s.lower())

    def test_check_REFUSES_a_dropped_hedge(self):
        m = copy.deepcopy(C.MINTS["planting_time_avoidance"])
        m["how_it_works_seasoned"] = m["how_it_works_seasoned"].replace(
            "may escape damage", "escape damage")
        with _Swap(C.MINTS, "planting_time_avoidance", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("may escape", out)

    def test_check_REFUSES_the_absolute_entering_the_prose(self):
        m = copy.deepcopy(C.MINTS["planting_time_avoidance"])
        m["pros"] = list(m["pros"]) + [f"A later sowing {C.FORBIDDEN_ABSOLUTE}"]
        with _Swap(C.MINTS, "planting_time_avoidance", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("absolute", out.lower())

    def test_the_scale_limit_on_bought_releases_is_carried(self):
        """UMD calls a release 'most practical in large plantings or community gardens'. On a
        home-garden dataset that qualifier is the whole practical content of the recommendation."""
        m = _post()["control_methods"]["augmentative_release"]
        blob = " ".join(P.prose_of(m)).lower()
        self.assertIn("large planting", blob)


class Sourcing(unittest.TestCase):
    def test_every_new_source_is_T1_and_anchored(self):
        post = _post()
        for key in list(C.MINTS) + list(C.WIDENINGS):
            m = post["control_methods"][key]
            for s in m["sources"]:
                self.assertIn(s, post["source_catalog"], f"{key}: {s} not in source_catalog")
                self.assertEqual(post["source_catalog"][s]["tier"], "T1", f"{key}: {s}")
                self.assertIn(s, m["anchoring_urls"], f"{key}: {s} has no anchor")

    def test_anchors_are_https_with_a_verified_date(self):
        post = _post()
        for key in list(C.MINTS) + list(C.WIDENINGS):
            for sid, a in post["control_methods"][key]["anchoring_urls"].items():
                self.assertTrue(a["url"].startswith("https://"), f"{key}/{sid}")
                self.assertRegex(a["verified"], r"^\d{4}-\d{2}-\d{2}$", f"{key}/{sid}")

    def test_the_new_source_passes_A54(self):
        """A document-scoped mint carries a title read OFF the document, and is never exempt."""
        self.assertEqual(title_violations(_post()["source_catalog"]), [])

    def test_check_REFUSES_a_document_scoped_source_without_a_title(self):
        e = copy.deepcopy(C.NEW_SOURCES["ucanr_ext_dry_bean_white_mold"])
        e.pop("title")
        with _Swap(C.NEW_SOURCES, "ucanr_ext_dry_bean_white_mold", e):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("title", out)

    def test_check_REFUSES_a_non_T1_source(self):
        e = copy.deepcopy(C.NEW_SOURCES["ucanr_ext_dry_bean_white_mold"])
        e["tier"] = "T2"
        with _Swap(C.NEW_SOURCES, "ucanr_ext_dry_bean_white_mold", e):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("T1", out)

    def test_check_REFUSES_a_source_that_does_not_exist(self):
        m = copy.deepcopy(C.MINTS["wet_foliage_discipline"])
        m["sources"] = ["clemson_hgic", "not_a_real_source"]
        m["anchoring_urls"] = dict(m["anchoring_urls"])
        m["anchoring_urls"]["not_a_real_source"] = {"url": "https://example.edu/",
                                                    "verified": C.VERIFIED}
        with _Swap(C.MINTS, "wet_foliage_discipline", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("source_catalog", out)

    def test_check_REFUSES_a_mint_declaring_a_non_T1_catalog_source(self):
        """`almanac` is a real T2 entry. This drives the T1 branch inside _check_sources, which
        the new-source T1 check in G2 was silently standing in for."""
        m = copy.deepcopy(C.MINTS["planting_time_avoidance"])
        m["sources"] = ["umn_ext", "almanac"]
        m["anchoring_urls"] = dict(m["anchoring_urls"])
        m["anchoring_urls"].pop("clemson_hgic")
        m["anchoring_urls"]["almanac"] = {"url": "https://example.edu/", "verified": C.VERIFIED}
        with _Swap(C.MINTS, "planting_time_avoidance", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not T1", out)

    def test_check_REFUSES_a_declared_source_with_no_anchoring_url(self):
        """A source with no anchor is a credit with no document behind it."""
        m = copy.deepcopy(C.MINTS["wet_foliage_discipline"])
        m["anchoring_urls"] = {k: v for k, v in m["anchoring_urls"].items() if k != "umn_ext"}
        with _Swap(C.MINTS, "wet_foliage_discipline", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("no anchoring_url", out)

    def test_the_new_source_is_not_claiming_the_frozen_exemption(self):
        from source_catalog_title_gate import LEGACY_UNFILLED
        for sid in C.NEW_SOURCES:
            self.assertNotIn(sid, LEGACY_UNFILLED)


class MintShape(unittest.TestCase):
    def test_mints_carry_every_required_field(self):
        post = _post()["control_methods"]
        for key in C.MINTS:
            for f in P.REQUIRED:
                self.assertIn(f, post[key], f"{key} missing {f}")
                self.assertTrue(post[key][f], f"{key}: {f} is empty")

    def test_mints_match_the_catalog_shape_the_gate_requires(self):
        from control_ladder_gate import _REQ_METHOD
        post = _post()["control_methods"]
        for key in C.MINTS:
            for f in _REQ_METHOD:
                self.assertIn(f, post[key], f"{key} missing gate-required {f}")

    def test_tiers_are_valid(self):
        post = _post()["control_methods"]
        for key in C.MINTS:
            self.assertIn(post[key]["tier"], P.TIERS)

    def test_check_REFUSES_an_invalid_tier(self):
        m = copy.deepcopy(C.MINTS["wet_foliage_discipline"])
        m["tier"] = "behavioral"
        with _Swap(C.MINTS, "wet_foliage_discipline", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tier", out)

    def test_check_REFUSES_a_missing_required_field(self):
        m = copy.deepcopy(C.MINTS["planting_time_avoidance"])
        m.pop("best_use")
        with _Swap(C.MINTS, "planting_time_avoidance", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("best_use", out)

    def test_check_REFUSES_a_mint_that_already_exists(self):
        """Re-running this promote over its own output must abort, not double-apply.

        THE ASSERTION NAMES G1's OWN MESSAGE. Asserting only `is not None` passed green with the
        already-in-catalog refusal disabled, because the WIDENING check further down objects to
        the same input for a different reason and returns a message of its own."""
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already in the catalog", out)


class Hygiene(unittest.TestCase):
    def test_every_authored_string_passes_copy_hygiene(self):
        post = _post()["control_methods"]
        for key in list(C.MINTS) + list(C.WIDENINGS):
            for s in P.prose_of(post[key]):
                self.assertIsNone(P.hygiene(s), f"{key}: {s[:70]!r}")

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        """Drives check()'s hygiene SWEEP, not the hygiene function. The two tests below prove the
        function works; only this one proves the promote actually runs it over the authored prose.

        The violation is a British spelling rather than an absolute: the forbidden-absolute check
        runs earlier and would have caught an absolute first, masking this branch."""
        m = copy.deepcopy(C.MINTS["wet_foliage_discipline"])
        m["pros"] = list(m["pros"]) + ["Keeps the colour of the foliage even"]
        with _Swap(C.MINTS, "wet_foliage_discipline", m):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_the_hygiene_check_is_not_vacuous(self):
        """Drive the function, not a constant: each family it claims to catch must actually trip."""
        self.assertIsNotNone(P.hygiene("a — dash"))
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("it is completely harmless"))
        self.assertIsNotNone(P.hygiene("the colour of the leaf"))
        self.assertIsNotNone(P.hygiene("warm to 70 °F"))
        self.assertIsNotNone(P.hygiene("a double -- hyphen"))
        self.assertIsNone(P.hygiene("Wait until the leaves have dried before going in to pick."))


class BlastRadius(unittest.TestCase):
    """SET EQUALITY BEFORE VALUE COMPARISON, both dicts, both directions (PLA-162)."""

    def test_exactly_the_declared_methods_are_added_and_none_dropped(self):
        pre, post = _pre(), None
        post = _post(pre)
        self.assertEqual(set(post["control_methods"]) - set(pre["control_methods"]), set(C.MINTS))
        self.assertEqual(set(pre["control_methods"]) - set(post["control_methods"]), set())

    def test_exactly_the_declared_sources_are_added_and_none_dropped(self):
        pre, post = _pre(), None
        post = _post(pre)
        self.assertEqual(set(post["source_catalog"]) - set(pre["source_catalog"]),
                         set(C.NEW_SOURCES))
        self.assertEqual(set(pre["source_catalog"]) - set(post["source_catalog"]), set())

    def test_no_untouched_method_changes(self):
        pre, post = _pre(), None
        post = _post(pre)
        touched = set(C.MINTS) | set(C.WIDENINGS)
        for k, before in pre["control_methods"].items():
            if k in touched:
                continue
            self.assertEqual(post["control_methods"][k], before, f"{k} changed")

    def test_no_existing_source_changes(self):
        pre, post = _pre(), None
        post = _post(pre)
        for k, before in pre["source_catalog"].items():
            self.assertEqual(post["source_catalog"][k], before, f"{k} changed")

    def test_no_crop_is_touched(self):
        pre, post = _pre(), None
        post = _post(pre)
        self.assertEqual(json.dumps(post["crops"], sort_keys=True),
                         json.dumps(pre["crops"], sort_keys=True))

    def test_no_ladder_gains_a_rung(self):
        """This promote mints keys; nothing points at them until batch 5 does."""
        pre, post = _pre(), None
        post = _post(pre)
        def rungs(d):
            n = 0
            for c in d["crops"]:
                for p in (c.get("pests") or []) + (c.get("diseases") or []):
                    n += len(p.get("control_ladder") or [])
            return n
        self.assertEqual(rungs(post), rungs(pre))

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

    def test_verify_post_CATCHES_an_extra_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["smuggled_method"] = dict(C.MINTS["wet_foliage_discipline"])
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_an_edited_bystander(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["handpick"]["best_use"] += " Also works on stem borers."
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_lost_target_on_a_widened_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["balance_nitrogen"]["applies_to"].remove("insect_soft_bodied")
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_CATCHES_a_dropped_source_on_a_widened_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["augmentative_release"]["sources"].remove("ucanr_ext")
        self.assertIsNotNone(P.verify_post(P.snapshot(pre), d))

    def test_verify_post_is_clean_on_the_real_apply(self):
        """The refusal specs above are only meaningful if the honest path passes."""
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(P.snapshot(pre), d))


class GateContract(unittest.TestCase):
    """The post state has to survive the gates this catalog is graded by."""

    def test_control_ladder_gate_is_clean_on_the_post_state(self):
        post = _post()
        self.assertEqual(CLG.catalog_violations(CLG.catalog(post)), [])

    def test_all_violations_is_clean_on_the_post_state(self):
        post = _post()
        self.assertEqual(CLG.all_violations(post), [])


class AdjudicationsHold(unittest.TestCase):
    """Three controls were adjudicated as ALREADY HOMED rather than minted. Pin the reasoning so a
    later session does not re-mint what already exists, and so the claim stays checkable."""

    def test_soil_warmth_at_sowing_is_still_sound_sowing_practice(self):
        m = _post()["control_methods"]["sound_sowing_practice"]
        self.assertIn("soil to warm", m["how_it_works_beginner"])
        self.assertTrue(set(m["applies_to"]) & set(TYPE_TARGETS["fungal"]),
                        "sound_sowing_practice cannot reach a fungal root rot, so the adjudication "
                        "that bean root rots need no new method is wrong")

    def test_weed_hosts_are_still_named_by_garden_sanitation(self):
        m = _post()["control_methods"]["garden_sanitation"]
        self.assertTrue(any("weed" in s.lower() for s in P.prose_of(m)),
                        "garden_sanitation no longer names weed hosts, so the adjudication that "
                        "aphid weed-host advice needs no new method is wrong")

    def test_no_method_was_minted_for_an_already_homed_control(self):
        post = _post()["control_methods"]
        for ghost in ("weed_host_control", "tool_and_hand_hygiene", "sow_into_warm_soil"):
            self.assertNotIn(ghost, post)


if __name__ == "__main__":
    unittest.main(verbosity=2)
