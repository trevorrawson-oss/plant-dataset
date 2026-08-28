#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_trap_cropping.py. Base be444e25.

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.

`VerifyPostIsDriven` is FIRST. Every branch of `verify_post` gets a driver that reaches it, because
a post-state guard with no driver is the failure mode this arc keeps rediscovering: eight of the
twelve survivors in the batch-8 harness were exactly that.

`Disclosure` is the safety family and the reason this method could be minted at all. Trap cropping
without the removal step raises the local pest population and parks it beside the crop, so the
cautions have to carry the deadline. UMass states it ("must receive an insecticide application or be
mechanically destroyed before eggs hatch") and UF/IFAS states the dispersal half ("you must eradicate
them to prevent them from moving on to the main crop"). A sheet recommending the practice without
that is worse than no sheet, so the promote refuses it.

`Contrast` is why this is a NEW KEY rather than a widening. `weed_host_control` REMOVES a host and
`crop_rotation` moves the crop; this ADDS a host and leaves the crop where it is. `best_use` has to
say so in as many words, which is the pyrethrin-against-pyrethroid pattern.

`Exclusions` pins that all six excluded problems RESOLVE. A typo in a slug or a problem name would
leave the backfill's refusal protecting nothing while still reporting green, which is the
derived-guard vacuity shape.

Frozen literals: the key, tier, applies_to, the disclosure axes, the contrast tokens and the
exclusion list are restated here as literals, NOT derived from the promote. Batch 10 shipped
`MINT = staged_mint()["entry"]` and made its own agreement check vacuous by construction.
"""
import copy, hashlib, json, os, sys, unittest
from contextlib import contextmanager

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_trap_cropping as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "86c5396a185e34a8b07271dc02794bbd54c7a6dba3367dde832e425c23e0bb2b"

# FROZEN LITERALS -- restated, never derived from P.
KEY = "trap_cropping"
TIER = "cultural"
APPLIES_TO = ["insect_chewing", "insect_general"]
DISCLOSURE_AXES = ("backfire", "deadline", "distance", "eradicate")
CONTRAST_TOKENS = ("weeds that host", "crop rotation", "removes", "adds")
SOURCES = ["uga_ext", "uf_ifas", "umass_ext"]
EXCLUDED = (
    ("radish", "flea-beetles"),
    ("radish", "cabbage-root-maggot"),
    ("dill", "Parsleyworm (black swallowtail caterpillar)"),
    ("parsley", "Parsleyworm (black swallowtail caterpillar)"),
    ("nasturtium", "Aphids"),
    ("zinnia", "Japanese beetles"),
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
        post["control_methods"][KEY]["name"] = "Trap crops"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("did not land verbatim", out)

    def test_stripped_disclosure_is_caught(self):
        """The safety branch. Drop the deadline sentence and the post guard must object."""
        snap, post = self._staged()
        m = post["control_methods"][KEY]
        m["cautions"] = [c for c in m["cautions"] if "before eggs hatch" not in c]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("do not state", out)
        self.assertIn("deadline", out)

    def test_stripped_contrast_is_caught(self):
        snap, post = self._staged()
        m = post["control_methods"][KEY]
        m["best_use"] = m["best_use"].replace("crop rotation", "moving things around")
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("does not distinguish", out)

    def test_widened_applies_to_is_caught(self):
        """Each of these fires on a plain post-state mutation, with no swap of P.METHOD. That is the
        point of the branch ordering in verify_post: the verbatim check subsumes all of them, so if
        it ran first these branches could never fire on their own and would be coverage in name
        only."""
        snap, post = self._staged()
        post["control_methods"][KEY]["applies_to"] = ["insect_chewing", "insect_general",
                                                      "insect_soft_bodied"]
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
            if c.get("slug") == "cabbage":
                for p in c.get("pests") or []:
                    if p.get("id") == "harlequin-bug":
                        p["control_ladder"].insert(1, _rung(KEY))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("mints only", out)

    def test_a_rung_on_an_EXCLUDED_problem_is_caught(self):
        """The refusal-spec driver. radish/flea-beetles is INVERTED: radish IS the trap crop."""
        snap, post = self._staged()
        for c in post["crops"]:
            if c.get("slug") == "radish":
                for p in c.get("pests") or []:
                    if p.get("id") == "flea-beetles":
                        p["control_ladder"].insert(1, _rung(KEY))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        # This asserted a DISJUNCTION at first ("mints only" OR "must never get one"), which hid
        # that the exclusion branch was unreachable: the mint-only sweep answered for it every
        # time. The harness caught it as a survivor. With the branches reordered the specific
        # message is the one that comes back, and a hedged assertion is no longer needed.
        self.assertIn("must never get one", out)

    def test_an_exclusion_that_stops_resolving_is_caught(self):
        snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "zinnia"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertTrue("no longer resolves" in out or "crop changed" in out
                        or "crop set changed" in out)

    def test_a_second_added_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"]["ghost_method"] = copy.deepcopy(P.METHOD)
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("methods added", out)

    def test_a_dropped_method_is_caught(self):
        snap, post = self._staged()
        del post["control_methods"]["crop_rotation"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("was dropped", out)

    def test_an_edited_existing_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"]["weed_host_control"]["best_use"] += " x"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("only mints", out)

    def test_a_touched_source_is_caught(self):
        snap, post = self._staged()
        post["source_catalog"]["uga_ext"]["accessed"] = "2099-01"
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

    def test_applies_to_reaches_both_measured_pest_families_and_no_more(self):
        """flea beetles are chewing; harlequin and stink bugs are general. insect_soft_bodied is
        deliberately absent: nothing was read for aphids or thrips, and declaring it would make the
        method legal on them. Same restraint weed_host_control used against mite."""
        self.assertIn("insect_chewing", P.METHOD["applies_to"])
        self.assertIn("insect_general", P.METHOD["applies_to"])
        self.assertNotIn("insect_soft_bodied", P.METHOD["applies_to"])
        self.assertNotIn("any", P.METHOD["applies_to"])

    def test_it_is_legal_on_every_target_problem_type(self):
        from control_ladder_gate import TYPE_TARGETS
        post = _post()
        m = post["control_methods"][KEY]
        self.assertTrue(set(m["applies_to"]) & TYPE_TARGETS["insect"])

    def test_check_REFUSES_a_non_cultural_tier(self):
        bad = copy.deepcopy(P.METHOD)
        bad["tier"] = "soft_chemical"
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cultural practice", out)

    def test_check_REFUSES_a_widened_applies_to(self):
        bad = copy.deepcopy(P.METHOD)
        bad["applies_to"] = ["any"]
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

    def test_check_REFUSES_a_source_missing_from_the_catalog(self):
        bad = copy.deepcopy(P.METHOD)
        bad["sources"] = bad["sources"] + ["not_a_real_source"]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not in source_catalog", out)

    def test_check_REFUSES_an_unanchored_source(self):
        bad = copy.deepcopy(P.METHOD)
        del bad["anchoring_urls"]["umass_ext"]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("has no anchoring_url", out)


class Disclosure(unittest.TestCase):
    """The safety family. Without the removal deadline this sheet recommends building a nursery."""

    def test_the_axis_table_is_the_frozen_one(self):
        """COVERAGE. The checks below iterate REQUIRED_DISCLOSURES, so trimming an entry makes them
        check less and still pass. Pinned against a restated literal."""
        self.assertEqual(tuple(sorted(P.REQUIRED_DISCLOSURES)), DISCLOSURE_AXES)
        for k, toks in P.REQUIRED_DISCLOSURES.items():
            self.assertTrue(toks, f"axis {k} requires no token at all")

    def test_all_axes_are_stated_in_the_shipped_cautions(self):
        self.assertEqual(P.missing_disclosures(P.METHOD), [])

    def test_the_deadline_is_quoted_to_the_source_that_states_it(self):
        blob = " ".join(P.METHOD["cautions"]).lower()
        self.assertIn("before eggs hatch", blob)
        self.assertIn("umass", blob)
        self.assertIn("eradicate", blob)

    def test_the_backfire_is_stated_not_implied(self):
        """The sentence a reader can be harmed by. A trap left standing is a population increase."""
        blob = " ".join(P.METHOD["cautions"]).lower()
        self.assertIn("works in reverse", blob)
        self.assertIn("population", blob)

    def test_the_seasoned_register_carries_the_mechanism_too(self):
        s = P.METHOD["how_it_works_seasoned"].lower()
        self.assertIn("before eggs hatch", s)
        self.assertIn("reservoir", s)

    def test_check_REFUSES_cautions_missing_the_deadline(self):
        bad = copy.deepcopy(P.METHOD)
        bad["cautions"] = [c for c in bad["cautions"] if "before eggs hatch" not in c]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("do not state", out)

    def test_check_REFUSES_cautions_missing_the_backfire(self):
        bad = copy.deepcopy(P.METHOD)
        bad["cautions"] = [c for c in bad["cautions"] if "works in reverse" not in c]
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("backfire", out)

    def test_missing_disclosures_is_not_vacuous(self):
        empty = copy.deepcopy(P.METHOD)
        empty["cautions"] = []
        self.assertEqual(sorted(P.missing_disclosures(empty)), sorted(DISCLOSURE_AXES))


class Contrast(unittest.TestCase):
    """Why this is a new key and not a widening of something already in the catalog."""

    def test_the_contrast_table_is_the_frozen_one(self):
        self.assertEqual(tuple(P.REQUIRED_CONTRASTS), CONTRAST_TOKENS)

    def test_best_use_holds_it_apart_from_both_near_misses(self):
        self.assertEqual(P.missing_contrasts(P.METHOD), [])

    def test_the_distinction_is_stated_in_the_right_DIRECTION(self):
        """The whole point: weed_host_control REMOVES a host, this ADDS one. A best_use that got
        that backwards would pass a token check, so the ordering is asserted."""
        b = P.METHOD["best_use"]
        self.assertLess(b.index("REMOVES"), b.index("ADDS"))
        self.assertIn("weeds that host", b.lower())
        self.assertIn("deliberately ADDS", b)

    def test_check_REFUSES_a_best_use_that_drops_a_contrast(self):
        bad = copy.deepcopy(P.METHOD)
        bad["best_use"] = bad["best_use"].replace("crop rotation", "other approaches")
        with swap("METHOD", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("does not distinguish", out)

    def test_missing_contrasts_is_not_vacuous(self):
        empty = copy.deepcopy(P.METHOD)
        empty["best_use"] = "A bed with a pest."
        self.assertEqual(sorted(P.missing_contrasts(empty)), sorted(CONTRAST_TOKENS))


class Exclusions(unittest.TestCase):
    """Six problems mention trap cropping and must never carry the rung."""

    def test_the_exclusion_list_is_the_frozen_six(self):
        self.assertEqual(tuple(P.EXCLUSIONS), EXCLUDED)

    def test_every_exclusion_RESOLVES_in_canonical(self):
        """The one that stops the backfill's refusal going vacuous. A typo'd slug or problem name
        would protect nothing while reporting green."""
        pre = _pre()
        for slug, ident in EXCLUDED:
            self.assertIsNotNone(P.find_problem(pre, slug, ident), f"{slug}/{ident}")

    def test_the_two_the_handoff_missed_carry_their_prose_in_note_fields(self):
        """nasturtium and zinnia were absent from the brief's scan because it covered the eight
        standard prose fields and these carry theirs in note_beginner/note_seasoned."""
        pre = _pre()
        for slug, ident in (("nasturtium", "Aphids"), ("zinnia", "Japanese beetles")):
            p = P.find_problem(pre, slug, ident)
            self.assertIsNotNone(p, slug)
            self.assertIn("note_seasoned", p, slug)
            self.assertNotIn("prevention_seasoned", p, slug)

    def test_none_of_the_six_is_laddered_with_the_new_key(self):
        post = _post()
        for slug, ident in EXCLUDED:
            p = P.find_problem(post, slug, ident)
            self.assertFalse(any(r.get("method") == KEY
                                 for r in p.get("control_ladder") or []), f"{slug}/{ident}")

    def test_check_REFUSES_an_exclusion_that_does_not_resolve(self):
        bad = tuple(P.EXCLUSIONS) + (("radish", "no-such-problem"),)
        with swap("EXCLUSIONS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("would protect nothing", out)

    def test_find_problem_matches_by_id_AND_by_name(self):
        """The four laddered exclusions carry ids; the two unladdered ones have no id at all, so
        both keys have to work or half the list silently stops resolving."""
        pre = _pre()
        self.assertIsNotNone(P.find_problem(pre, "radish", "flea-beetles"))          # by id
        self.assertIsNotNone(P.find_problem(pre, "nasturtium", "Aphids"))            # by name
        self.assertIsNone(P.find_problem(pre, "radish", "Aphids"))


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
        pre, post = _pre(), None
        post = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(post)
        self.assertEqual(b["crops"], a["crops"])

    def test_no_source_changes(self):
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(b["sources"], a["sources"])

    def test_key_sets_are_compared_before_values(self):
        """set(pre) == set(post) FIRST. Iterating pre alone makes every addition invisible, which
        was all four PLA-162 defects."""
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
            if c.get("slug") == "cabbage":
                for p in c.get("pests") or []:
                    if p.get("id") == "harlequin-bug":
                        p["control_ladder"].append(_rung(KEY))
        self.assertEqual(P.rungs_of(post, KEY), [("cabbage", "harlequin-bug")])


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_the_post_state(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_the_catalog_half_of_the_gate_accepts_the_new_entry(self):
        post = _post()
        bad = [v for v in CLG.catalog_violations(post) if KEY in v]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
