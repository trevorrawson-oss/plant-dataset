#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_disease_escape_backfill.py. Base 9f38bb00 (the mint's output,
rebuilt by CHAIN replay until the mint commits).

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.

`VerifyPostIsDriven` is FIRST, one driver per branch, each a plain post-state doctoring with no
module swap, and each asserting the ONE message its branch emits: a disjunction over two error
messages passes whether or not the branch under test is reachable (the trap-cropping harness caught
two of those hiding masked guards).

`Premise` verifies in CANONICAL that every target's prose states the escape and names its disease,
and that fava's root-rots entry really carries the cold-seedbed warning the fava rung attributes to
it. `Distinctness` pins the escape-sentence correspondence in both directions. `Placement` pins the
front-of-ladder positions. `Exclusions` pins the four scan matches, spinach's damping-off above
all: typed fungal, gate-legal, and the advice inverts there.
"""
import copy, hashlib, json, os, sys, unittest
from contextlib import contextmanager

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_disease_escape_backfill as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "ee0f54a35a4dd1eee0da6daa5992c636cc422f25796e46d4649fd3c9fcc07277"

# FROZEN LITERALS -- restated, never derived from P.
METHOD = "disease_escape_sowing"
TARGETS = (
    ("sweet-corn", "common-rust"),
    ("field-corn", "common-rust"),
    ("popcorn", "common-rust"),
    ("flint-corn", "common-rust"),
    ("sugar-snap-peas", "powdery-mildew"),
    ("snow-peas", "powdery-mildew"),
    ("broad-beans-fava", "broad-bean-rust"),
)
EXCLUDED = (
    ("spinach", "damping-off"),
    ("radish", "black-rot"),
    ("cilantro-coriander", "powdery-mildew"),
    ("jalapeno", "mosaic-viruses"),
)
ATTRIBUTION = "this crop's guidance"


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


def _prob(data, slug, pid):
    for c in data["crops"]:
        if c.get("slug") == slug:
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    if p.get("id") == pid or p.get("name") == pid:
                        return p
    return None


def _rung(method):
    return {"method": method, "note_beginner": "b", "note_seasoned": "s"}


class VerifyPostIsDriven(unittest.TestCase):
    """One driver per branch of verify_post. Written first, on purpose. Every assertion is a
    SINGLE message: a hedged OR over two messages is how a masked guard passes review."""

    def _staged(self):
        pre = _pre()
        return P.snapshot(pre), _post(pre)

    def test_a_duplicate_rung_is_caught(self):
        snap, post = self._staged()
        _prob(post, "sweet-corn", "common-rust")["control_ladder"].append(_rung(METHOD))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("expected 1", out)

    def test_a_rung_at_the_wrong_index_is_caught(self):
        snap, post = self._staged()
        lad = _prob(post, "sugar-snap-peas", "powdery-mildew")["control_ladder"]
        r = lad.pop(1)
        lad.append(r)
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("put the rung at index", out)

    def test_a_tier_decrease_elsewhere_in_the_ladder_is_caught(self):
        """Reachable on its own: the rung stays at its wanted index while two later rungs swap."""
        snap, post = self._staged()
        lad = _prob(post, "snow-peas", "powdery-mildew")["control_ladder"]
        lad[3], lad[5] = lad[5], lad[3]   # garden_sanitation (cultural) <-> sulfur (soft_chemical)
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_a_swapped_rung_text_is_caught(self):
        snap, post = self._staged()
        lad = _prob(post, "broad-beans-fava", "broad-bean-rust")["control_ladder"]
        lad[0]["note_beginner"] = P.RUNGS[("sweet-corn", "common-rust")]["note_beginner"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("did not get its own rung", out)

    def test_an_exclusion_that_stops_resolving_is_caught(self):
        snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "spinach"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("no longer resolves", out)

    def test_a_rung_on_the_DANGEROUS_exclusion_is_caught(self):
        """spinach/damping-off: gate-legal, and early sowing into cold soil CAUSES the problem."""
        snap, post = self._staged()
        _prob(post, "spinach", "damping-off")["control_ladder"].insert(0, _rung(METHOD))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("must never carry", out)
        self.assertIn("OPPOSITE DIRECTION", out)

    def test_a_rung_on_a_non_target_problem_is_caught(self):
        snap, post = self._staged()
        _prob(post, "kale", "downy-mildew")["control_ladder"].append(_rung(METHOD))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("landed on", out)

    def test_a_dropped_bystander_crop_is_caught(self):
        snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "tomatillo"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

    def test_an_edited_bystander_crop_is_caught(self):
        snap, post = self._staged()
        for c in post["crops"]:
            if c.get("slug") == "tomatillo":
                c["name"] = "MUTATED"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("touches only", out)

    def test_a_touched_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"][METHOD]["best_use"] += " x"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("mints nothing", out)

    def test_a_touched_source_is_caught(self):
        snap, post = self._staged()
        post["source_catalog"]["wsu_ext"]["accessed"] = "2099-01"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("source_catalog changed", out)

    def test_verify_post_is_clean_on_the_real_apply(self):
        snap, post = self._staged()
        self.assertIsNone(P.verify_post(snap, post))


class Fixture(unittest.TestCase):
    def test_base_reconstructs(self):
        self.assertEqual(
            hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(), P.BASE_SHA)

    def test_the_base_already_carries_the_mint(self):
        pre = _pre()
        self.assertIn(METHOD, pre["control_methods"])
        self.assertEqual(pre["control_methods"][METHOD]["tier"], "cultural")

    def test_post_sha_pinned(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)

    def test_check_passes_on_the_pinned_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_check_REFUSES_running_over_its_own_output(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already carries", out)


class Premise(unittest.TestCase):
    """The escape must be stated by each crop's OWN prose, in canonical, disease named."""

    def test_every_target_states_the_escape(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_escape_premise(by))

    def test_the_frozen_target_list_matches(self):
        self.assertEqual(tuple((s, p) for s, p, _a, _w in P.TARGETS), TARGETS)

    def test_check_REFUSES_a_target_whose_escape_sentence_is_gone(self):
        pre = _pre()
        p = _prob(pre, "sweet-corn", "common-rust")
        for f in ("prevention_beginner", "prevention_seasoned"):
            p[f] = p[f].replace("plant early", "keep watch")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("no longer states an early-sowing escape", out)

    def test_check_REFUSES_an_escape_sentence_that_stops_naming_the_disease(self):
        pre = _pre()
        p = _prob(pre, "snow-peas", "powdery-mildew")
        for f in ("prevention_beginner", "prevention_seasoned"):
            p[f] = p[f].replace("mildew weather", "bad weather")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("no longer names", out)

    def test_fava_premise_holds_in_canonical(self):
        """The fava rung attributes the cold-seedbed warning to the crop's own root-rots entry."""
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_fava_premise(by))

    def test_check_REFUSES_when_the_fava_counter_exposure_is_gone(self):
        pre = _pre()
        p = _prob(pre, "broad-beans-fava", "root-rots-damping-off")
        for f in P.PROSE_FIELDS:
            if p.get(f):
                p[f] = p[f].replace("cold", "poor").replace("Cold", "Poor")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("no longer carries the cold-seedbed", out)


class Distinctness(unittest.TestCase):
    """Identical escape sentences <-> identical rungs, pinned in both directions."""

    def test_the_correspondence_holds_on_the_pinned_base(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_rung_distinctness(by))

    def test_the_corns_share_one_text_and_the_peas_another(self):
        corn = P.RUNGS[("sweet-corn", "common-rust")]
        for slug in ("field-corn", "popcorn", "flint-corn"):
            self.assertEqual(P.RUNGS[(slug, "common-rust")], corn, slug)
        pea = P.RUNGS[("sugar-snap-peas", "powdery-mildew")]
        self.assertEqual(P.RUNGS[("snow-peas", "powdery-mildew")], pea)
        self.assertNotEqual(corn, pea)
        self.assertNotEqual(P.RUNGS[("broad-beans-fava", "broad-bean-rust")], corn)
        self.assertNotEqual(P.RUNGS[("broad-beans-fava", "broad-bean-rust")], pea)

    def test_the_peas_share_the_escape_byte_for_byte_but_not_their_whole_prose(self):
        """WHY the correspondence keys on escape sentences: whole-field bytes would force a fork
        the sources do not carry (the peas differ only in their variety-name sentences)."""
        pre = _pre()
        a = _prob(pre, "sugar-snap-peas", "powdery-mildew")
        b = _prob(pre, "snow-peas", "powdery-mildew")
        self.assertEqual(P.escape_key(a), P.escape_key(b))
        self.assertNotEqual([a.get(f) for f in P.PROSE_FIELDS],
                            [b.get(f) for f in P.PROSE_FIELDS])

    def test_check_REFUSES_a_forked_rung_on_identical_escapes(self):
        bad = copy.deepcopy(P.RUNGS)
        bad[("snow-peas", "powdery-mildew")] = dict(
            bad[("snow-peas", "powdery-mildew")],
            note_beginner=bad[("snow-peas", "powdery-mildew")]["note_beginner"] + " More.")
        with swap("RUNGS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("byte-identical escape sentences but different rungs", out)

    def test_check_REFUSES_a_copied_rung_across_differing_escapes(self):
        bad = copy.deepcopy(P.RUNGS)
        bad[("broad-beans-fava", "broad-bean-rust")] = copy.deepcopy(
            bad[("sweet-corn", "common-rust")])
        with swap("RUNGS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("share a rung but their escape sentences differ", out)


class Placement(unittest.TestCase):
    def test_the_six_land_after_resistant_varieties_and_fava_at_the_front(self):
        post = _post()
        for slug, pid, after, _w in P.TARGETS:
            ms = [r["method"] for r in _prob(post, slug, pid)["control_ladder"]]
            if after is None:
                self.assertEqual(ms.index(METHOD), 0, slug)
            else:
                self.assertEqual(ms.index(METHOD), ms.index("resistant_varieties") + 1, slug)

    def test_tier_monotonicity_holds_on_every_target_after_the_insert(self):
        post = _post()
        cm = post["control_methods"]
        rank = {t: i for i, t in enumerate(("cultural", "physical", "biological",
                                            "soft_chemical", "conventional"))}
        for slug, pid in TARGETS:
            ranks = [rank[cm[r["method"]]["tier"]]
                     for r in _prob(post, slug, pid)["control_ladder"]]
            self.assertEqual(ranks, sorted(ranks), slug)

    def test_check_REFUSES_when_resistant_varieties_is_not_the_opening_rung(self):
        """The placement premise: the rung sits beside the other before-anything-is-in-the-ground
        decision. If a ladder reorders, the premise has drifted and the promote must say so."""
        pre = _pre()
        lad = _prob(pre, "popcorn", "common-rust")["control_ladder"]
        lad[0], lad[1] = lad[1], lad[0]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("not the ladder's opening rung", out)

    def test_check_REFUSES_a_target_already_carrying_the_rung(self):
        pre = _pre()
        _prob(pre, "flint-corn", "common-rust")["control_ladder"].append(_rung(METHOD))
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("already carries", out)


class Contract(unittest.TestCase):
    """Every rung attributes the escape to the crop and routes the trade through the cautions."""

    def test_every_rung_carries_the_attribution_and_the_pointer(self):
        for key, rung in P.RUNGS.items():
            blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
            self.assertIn(ATTRIBUTION, blob, key)
            self.assertIn("cautions", blob, key)

    def test_check_REFUSES_a_rung_without_the_attribution(self):
        bad = copy.deepcopy(P.RUNGS)
        for f in ("note_beginner", "note_seasoned"):
            bad[("popcorn", "common-rust")][f] = \
                bad[("popcorn", "common-rust")][f].replace(ATTRIBUTION, "sound practice")
        with swap("RUNGS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("does not attribute the escape", out)

    def test_check_REFUSES_a_rung_without_the_cautions_pointer(self):
        bad = copy.deepcopy(P.RUNGS)
        for f in ("note_beginner", "note_seasoned"):
            bad[("sweet-corn", "common-rust")][f] = \
                bad[("sweet-corn", "common-rust")][f].replace("cautions", "notes")
        with swap("RUNGS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("never points the reader", out)

    def test_check_REFUSES_identical_registers(self):
        bad = copy.deepcopy(P.RUNGS)
        bad[("snow-peas", "powdery-mildew")]["note_seasoned"] = \
            bad[("snow-peas", "powdery-mildew")]["note_beginner"]
        bad[("sugar-snap-peas", "powdery-mildew")]["note_seasoned"] = \
            bad[("sugar-snap-peas", "powdery-mildew")]["note_beginner"]
        with swap("RUNGS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_every_rung_names_the_cold_trade(self):
        """The rung must not sell the escape without its cost; each text says cold in some form."""
        for key, rung in P.RUNGS.items():
            blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
            self.assertIn("cold", blob, key)


class Exclusions(unittest.TestCase):
    def test_the_exclusion_list_is_the_frozen_four(self):
        self.assertEqual(tuple((s, p) for s, p, _r in P.EXCLUSIONS), EXCLUDED)

    def test_every_exclusion_RESOLVES_and_carries_a_reason(self):
        pre = _pre()
        for slug, ident, reason in P.EXCLUSIONS:
            self.assertIsNotNone(P.find_problem(pre, slug, ident), f"{slug}/{ident}")
            self.assertTrue(reason.strip(), f"{slug}/{ident}")

    def test_none_of_the_four_gains_the_rung(self):
        post = _post()
        for slug, ident in EXCLUDED:
            p = P.find_problem(post, slug, ident)
            self.assertFalse(any(r.get("method") == METHOD
                                 for r in p.get("control_ladder") or []), f"{slug}/{ident}")

    def test_the_dangerous_exclusion_is_gate_legal_so_only_this_list_protects_it(self):
        from control_ladder_gate import TYPE_TARGETS
        pre = _pre()
        p = P.find_problem(pre, "spinach", "damping-off")
        self.assertEqual(p.get("type"), "fungal")
        self.assertIn("fungal_foliar", TYPE_TARGETS["fungal"])

    def test_check_REFUSES_an_exclusion_that_does_not_resolve(self):
        bad = tuple(P.EXCLUSIONS) + (("spinach", "no-such-problem", "reason"),)
        with swap("EXCLUSIONS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("would protect nothing", out)

    def test_check_REFUSES_an_exclusion_that_is_also_a_target(self):
        bad = tuple(P.EXCLUSIONS) + (("sweet-corn", "common-rust", "reason"),)
        with swap("EXCLUSIONS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cannot both be true", out)


class Hygiene(unittest.TestCase):
    def test_all_shipped_rung_prose_passes(self):
        for key, rung in P.RUNGS.items():
            for f in ("note_beginner", "note_seasoned"):
                self.assertIsNone(P.hygiene(rung[f]), (key, f))

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("an em dash — here"))
        self.assertIsNotNone(P.hygiene("mid-sentence Plant capital"))

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        bad = copy.deepcopy(P.RUNGS)
        bad[("popcorn", "common-rust")]["note_beginner"] += " This never fails."
        with swap("RUNGS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)


class BlastRadius(unittest.TestCase):
    def test_key_sets_are_compared_before_values(self):
        """set(pre) == set(post) FIRST. Iterating pre alone makes every addition invisible."""
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(set(b["crops"]), set(a["crops"]))
        changed = sorted(s for s in a["crops"] if a["crops"][s] != b["crops"][s])
        self.assertEqual(changed, sorted(P.CROPS))

    def test_methods_and_sources_are_byte_identical(self):
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(b["methods"], a["methods"])
        self.assertEqual(b["sources"], a["sources"])

    def test_each_target_gains_exactly_one_ladder_entry_and_nothing_else_changes_there(self):
        pre = _pre()
        post = _post(pre)
        for slug, pid in TARGETS:
            before = _prob(pre, slug, pid)
            after = _prob(post, slug, pid)
            self.assertEqual(len(after["control_ladder"]), len(before["control_ladder"]) + 1, slug)
            for f in P.PROSE_FIELDS:
                self.assertEqual(after.get(f), before.get(f), (slug, f))


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_the_post_state(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_the_new_rungs_are_applies_to_coherent(self):
        """Every target is typed fungal and the method reaches fungal_foliar; the gate agrees."""
        post = _post()
        for slug, pid in TARGETS:
            self.assertEqual(_prob(post, slug, pid).get("type"), "fungal", slug)


if __name__ == "__main__":
    unittest.main(verbosity=2)
