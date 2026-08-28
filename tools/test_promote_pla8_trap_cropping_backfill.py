#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_trap_cropping_backfill.py. Base 86c5396a.

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.

THIS PROMOTE AMENDS TEN LADDERS ON NINE CERTIFIED CROPS, which is the heaviest thing this arc does.
Four families carry it.

`GroupPremise` is the premise, verified IN CANONICAL and IN BOTH DIRECTIONS. The seven harlequin bug
entries carry the removal step in their own prose ("then destroy it before the main crop is set
out"), so their rungs may restate it and attribute it. The three flea beetle entries stop at the
diversion ("divert beetles from the main crop"), so their rungs route the timing through the METHOD's
cautions and are FORBIDDEN the attribution phrase. Saying "this crop's guidance" about a removal step
the source never states is authoring a recommendation, which is the batch-10 planting_time_avoidance
ruling in a different field.

`Species` is what stops a propagation defect. The ten name different trap plants, and jalapeno's is
NASTURTIUM while most of the rest are mustard. Every species a rung names is checked against THAT
crop's own prose, so a rung copied off a sibling is refused.

`Distinctness` pins the prose/rung correspondence BOTH WAYS: byte-identical prose must yield an
identical rung (cabbage and cauliflower, the only such pair), and differing prose must yield
differing rungs. One direction catches a copied rung, the other a needlessly forked one. Batch 3's
cucumbers are why: propagation there would have erased a sourced control in both directions.

`Exclusions` pins the six that must never carry the rung, in both directions, each with its own
reason. nasturtium is the most dangerous of them: its own text describes pulling a loaded trap stand,
which READS exactly like this method's action, but this dataset carries nasturtium as an ornamental
and edible crop, so a rung tells the reader to destroy the crop they are growing.

Frozen literals: the target list, the group split, the exclusion six, the species vocabulary and the
attribution phrase are restated here, NOT derived from the promote.
"""
import copy, hashlib, json, os, sys, unittest
from contextlib import contextmanager

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_trap_cropping_backfill as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "96cbc68c7f8a1509bf922e85ad424d6a55a3f1c2a45d6288bfa5ba16a2bec67a"

# FROZEN LITERALS -- restated, never derived from P.
METHOD = "trap_cropping"
DIVERT = (("arugula", "flea-beetles"), ("bok-choy", "flea-beetles"), ("jalapeno", "flea-beetles"))
DESTROY = (("bok-choy", "harlequin-bug"), ("cabbage", "harlequin-bug"),
           ("cauliflower", "harlequin-bug"), ("collards", "harlequin-bug"),
           ("kale", "harlequin-bug"), ("kohlrabi", "harlequin-bug"), ("turnip", "harlequin-bug"))
ALL_TARGETS = DIVERT + DESTROY
CROPS = ("arugula", "bok-choy", "jalapeno", "cabbage", "cauliflower", "collards", "kale",
         "kohlrabi", "turnip")
EXCLUDED = (
    ("radish", "flea-beetles"),
    ("radish", "cabbage-root-maggot"),
    ("dill", "Parsleyworm (black swallowtail caterpillar)"),
    ("parsley", "Parsleyworm (black swallowtail caterpillar)"),
    ("nasturtium", "Aphids"),
    ("zinnia", "Japanese beetles"),
)
ATTRIBUTION = "this crop's guidance"
# The only pair whose prose is byte-identical over the four fields, so the only pair licensed to
# share a rung text.
TWINS = (("cabbage", "harlequin-bug"), ("cauliflower", "harlequin-bug"))


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _by(d):
    return {c.get("slug"): c for c in d["crops"]}


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
        return pre, P.snapshot(pre), _post(pre)

    def test_a_duplicated_rung_is_caught(self):
        _pre_, snap, post = self._staged()
        lad = P.problem(_by(post), "cabbage", "harlequin-bug")["control_ladder"]
        lad.insert(1, copy.deepcopy(lad[1]))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("expected 1", out)

    def test_a_rung_placed_inside_the_cultural_run_is_caught(self):
        """turnip has two cultural rungs, so the new one can be moved earlier while staying in the
        run. Only the end-of-run branch can object."""
        _pre_, snap, post = self._staged()
        lad = P.problem(_by(post), "turnip", "harlequin-bug")["control_ladder"]
        i = next(k for k, r in enumerate(lad) if r["method"] == METHOD)
        lad.insert(0, lad.pop(i))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("inside the cultural run", out)

    def test_a_rung_moved_to_the_END_of_the_ladder_is_caught(self):
        """Caught by MONOTONICITY, and the assertion says so rather than hedging.

        This began as a driver for a dedicated "sits after a non-cultural rung" branch, asserting
        `"after a non-cultural rung" in out or "tiers decrease" in out`. The harness showed the
        branch survived being disabled: a cultural rung after a non-cultural one always breaks tier
        order, so monotonicity answered every time and the branch was unreachable. The disjunction
        is what let that pass unnoticed -- the second time in these two suites that a hedged OR hid
        a masked guard. The branch is now deleted and this asserts the one check that really fires."""
        _pre_, snap, post = self._staged()
        lad = P.problem(_by(post), "cabbage", "harlequin-bug")["control_ladder"]
        i = next(k for k, r in enumerate(lad) if r["method"] == METHOD)
        lad.append(lad.pop(i))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_a_tier_decrease_elsewhere_in_the_ladder_is_caught(self):
        """The new rung stays where it belongs, so only the monotonicity branch can object."""
        _pre_, snap, post = self._staged()
        lad = P.problem(_by(post), "cabbage", "harlequin-bug")["control_ladder"]
        j = next(k for k, r in enumerate(lad) if r["method"] == "neem_oil")
        lad.insert(len(lad) - 1, lad.pop(j)) if j != len(lad) - 1 else None
        lad.append(lad.pop(next(k for k, r in enumerate(lad) if r["method"] == "handpick")))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_the_wrong_crops_rung_text_is_caught(self):
        _pre_, snap, post = self._staged()
        lad = P.problem(_by(post), "kale", "harlequin-bug")["control_ladder"]
        i = next(k for k, r in enumerate(lad) if r["method"] == METHOD)
        lad[i]["note_beginner"] = P.RUNGS[("collards", "harlequin-bug")]["note_beginner"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("did not get its own rung", out)

    def test_a_rung_on_an_EXCLUDED_problem_is_caught_with_its_own_reason(self):
        """The refusal-spec driver, and the reason the exclusion loop runs before the landed-set
        check: the message has to say WHY radish is forbidden, not print a diff of ten pairs."""
        _pre_, snap, post = self._staged()
        P.problem(_by(post), "radish", "flea-beetles")["control_ladder"].insert(0, _rung(METHOD))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("must never carry", out)
        self.assertIn("INVERTED", out)

    def test_a_rung_on_the_NASTURTIUM_exclusion_is_caught(self):
        """The most dangerous of the six. It is unladdered, so the rung has to bring a ladder with
        it, which is exactly what a later pass laddering the ornamentals would do."""
        _pre_, snap, post = self._staged()
        p = P.find_problem(post, "nasturtium", "Aphids")
        p["control_ladder"] = [_rung(METHOD)]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("must never carry", out)
        self.assertIn("MOST DANGEROUS", out)

    def test_a_rung_on_a_bystander_problem_is_caught(self):
        _pre_, snap, post = self._staged()
        P.problem(_by(post), "cabbage", "cabbage-root-maggot")["control_ladder"].insert(
            0, _rung(METHOD))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("the rung landed on", out)

    def test_a_dropped_crop_is_caught(self):
        _pre_, snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "tomatillo"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

    def test_a_bystander_crop_is_caught(self):
        _pre_, snap, post = self._staged()
        _by(post)["tomatillo"]["name"] = "MUTATED"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("touches only", out)

    def test_a_touched_method_is_caught(self):
        _pre_, snap, post = self._staged()
        post["control_methods"]["garden_sanitation"]["best_use"] += " x"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("mints nothing", out)

    def test_a_touched_source_is_caught(self):
        _pre_, snap, post = self._staged()
        post["source_catalog"]["uga_ext"]["accessed"] = "2099-01"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("source_catalog changed", out)

    def test_verify_post_is_clean_on_the_real_apply(self):
        _pre_, snap, post = self._staged()
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

    def test_ten_targets_across_nine_crops(self):
        self.assertEqual(tuple((s, p) for s, p, _g in P.TARGETS), ALL_TARGETS)
        self.assertEqual(len(P.TARGETS), 10)
        self.assertEqual(len({s for s, _p, _g in P.TARGETS}), 9)
        self.assertEqual(tuple(sorted(P.CROPS)), tuple(sorted(CROPS)))

    def test_exactly_ten_rungs_are_added(self):
        pre = _pre()

        def count(d):
            return sum(1 for c in d["crops"]
                       for fam in ("pests", "diseases")
                       for p in (c.get(fam) or []) if isinstance(p, dict)
                       for r in (p.get("control_ladder") or []) if r["method"] == METHOD)
        self.assertEqual(count(pre), 0)
        self.assertEqual(count(_post(pre)), 10)

    def test_check_REFUSES_when_the_mint_has_not_landed(self):
        pre = _pre()
        del pre["control_methods"][METHOD]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("mint must land first", out)

    def test_check_REFUSES_a_non_cultural_method_tier(self):
        pre = _pre()
        pre["control_methods"][METHOD]["tier"] = "soft_chemical"
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("cultural tier", out)

    def test_check_REFUSES_running_over_its_own_output(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already carries", out)


class GroupPremise(unittest.TestCase):
    """Which crops' prose actually states the removal step, verified in canonical, both ways."""

    def test_the_split_is_the_frozen_one(self):
        got_d = tuple((s, p) for s, p, g in P.TARGETS if g == P.DESTROY_STATED)
        got_v = tuple((s, p) for s, p, g in P.TARGETS if g == P.DIVERT_ONLY)
        self.assertEqual(got_d, DESTROY)
        self.assertEqual(got_v, DIVERT)
        self.assertEqual(len(got_d), 7)
        self.assertEqual(len(got_v), 3)

    def test_the_premise_holds_on_the_pinned_base(self):
        self.assertIsNone(P.check_group_premise(_by(_pre())))

    def test_each_DESTROY_target_really_states_a_removal_in_canonical(self):
        by = _by(_pre())
        for slug, pid in DESTROY:
            blob = " ".join(P.trap_sentences(P.problem(by, slug, pid))).lower()
            self.assertTrue(any(w in blob for w in P.REMOVAL_WORDS), f"{slug}/{pid}")

    def test_each_DIVERT_target_really_does_NOT(self):
        """The half that licenses routing the timing through the method instead of the crop."""
        by = _by(_pre())
        for slug, pid in DIVERT:
            blob = " ".join(P.trap_sentences(P.problem(by, slug, pid))).lower()
            self.assertFalse(any(w in blob for w in P.REMOVAL_WORDS), f"{slug}/{pid}")

    def test_check_REFUSES_a_DESTROY_target_whose_prose_lost_its_removal_step(self):
        pre = _pre()
        p = P.problem(_by(pre), "kohlrabi", "harlequin-bug")
        p["prevention_beginner"] = p["prevention_beginner"].replace(", then destroy it", "")
        p["prevention_seasoned"] = p["prevention_seasoned"].replace(
            ", then destroy it before the main crop is set out", "")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("no longer states a removal step", out)

    def test_check_REFUSES_a_DIVERT_target_whose_prose_GAINED_one(self):
        """The other direction. A crop that starts recommending removal should carry the
        DESTROY_STATED contract, not keep routing the timing through the method."""
        pre = _pre()
        p = P.problem(_by(pre), "jalapeno", "flea-beetles")
        p["prevention_seasoned"] += " Destroy the trap planting once it fills."
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("now states a removal step", out)

    def test_check_REFUSES_a_target_that_stopped_mentioning_a_trap_crop(self):
        pre = _pre()
        p = P.problem(_by(pre), "arugula", "flea-beetles")
        for f in P.PROSE_FIELDS:
            if p.get(f):
                p[f] = p[f].replace("sacrificial", "spare").replace("trap", "spare")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("nothing to restate", out)

    def test_trap_sentences_is_not_vacuous(self):
        by = _by(_pre())
        self.assertTrue(P.trap_sentences(P.problem(by, "jalapeno", "flea-beetles")))
        self.assertEqual(P.trap_sentences(P.problem(by, "cabbage", "cabbage-root-maggot")), [])


class Species(unittest.TestCase):
    """Every trap plant a rung names must be named by that crop's own prose."""

    def test_the_species_vocabulary_covers_what_the_prose_uses(self):
        self.assertIn("nasturtium", P.SPECIES)
        self.assertIn("mustard", P.SPECIES)
        self.assertIn("rapeseed", P.SPECIES)

    def test_every_rung_names_only_species_its_own_crop_names(self):
        self.assertIsNone(P.check_species(_by(_pre())))

    def test_jalapeno_names_nasturtium_and_no_brassica(self):
        """The propagation tripwire. jalapeno is not a brassica and its prose names nasturtium; a
        rung copied off a sibling would put mustard here."""
        blob = (P.RUNGS[("jalapeno", "flea-beetles")]["note_beginner"] + " " +
                P.RUNGS[("jalapeno", "flea-beetles")]["note_seasoned"]).lower()
        self.assertIn("nasturtium", blob)
        self.assertNotIn("mustard", blob)
        self.assertNotIn("rapeseed", blob)

    def test_nasturtium_appears_in_NO_other_crops_rung(self):
        for (slug, pid), rung in P.RUNGS.items():
            if slug == "jalapeno":
                continue
            blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
            self.assertNotIn("nasturtium", blob, f"{slug}/{pid}")

    def test_rapeseed_appears_only_where_the_prose_names_it(self):
        for (slug, pid), rung in P.RUNGS.items():
            blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
            if "rapeseed" in blob:
                self.assertIn(slug, ("collards", "kale"), f"{slug}/{pid}")

    def test_check_REFUSES_a_rung_naming_a_plant_its_crop_does_not(self):
        r = copy.deepcopy(P.RUNGS)
        r[("jalapeno", "flea-beetles")]["note_beginner"] = (
            r[("jalapeno", "flea-beetles")]["note_beginner"].replace("nasturtium", "mustard"))
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("which this crop's own prose does not", out)

    def test_check_REFUSES_a_rung_naming_no_trap_plant_at_all(self):
        r = copy.deepcopy(P.RUNGS)
        for k in ("note_beginner", "note_seasoned"):
            for sp in P.SPECIES:
                r[("kohlrabi", "harlequin-bug")][k] = (
                    r[("kohlrabi", "harlequin-bug")][k].replace(sp, "a patch"))
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("names no trap plant", out)


class Distinctness(unittest.TestCase):
    """Identical prose -> identical rung; differing prose -> differing rung. Both directions."""

    def test_the_correspondence_holds_on_the_pinned_base(self):
        self.assertIsNone(P.check_rung_distinctness(_by(_pre())))

    def test_cabbage_and_cauliflower_are_the_only_byte_identical_pair(self):
        by = _by(_pre())
        same = []
        for i, (s1, p1) in enumerate(ALL_TARGETS):
            for s2, p2 in ALL_TARGETS[i + 1:]:
                if P.prose_key(P.problem(by, s1, p1)) == P.prose_key(P.problem(by, s2, p2)):
                    same.append(((s1, p1), (s2, p2)))
        self.assertEqual(same, [TWINS])

    def test_the_twins_share_one_rung_object(self):
        self.assertEqual(P.RUNGS[TWINS[0]], P.RUNGS[TWINS[1]])

    def test_the_other_eight_rungs_are_all_distinct(self):
        seen = {}
        for (slug, pid), rung in P.RUNGS.items():
            if (slug, pid) in TWINS:
                continue
            key = rung["note_beginner"]
            self.assertNotIn(key, seen, f"{slug}/{pid} duplicates {seen.get(key)}")
            seen[key] = (slug, pid)

    def test_check_REFUSES_a_rung_copied_onto_a_crop_whose_prose_differs(self):
        r = copy.deepcopy(P.RUNGS)
        r[("kale", "harlequin-bug")] = copy.deepcopy(r[("kohlrabi", "harlequin-bug")])
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertTrue("share a rung but their prose differs" in out
                        or "which this crop's own prose does not" in out)

    def test_check_REFUSES_the_twins_being_needlessly_forked(self):
        r = copy.deepcopy(P.RUNGS)
        r[("cauliflower", "harlequin-bug")] = copy.deepcopy(r[("cauliflower", "harlequin-bug")])
        r[("cauliflower", "harlequin-bug")]["note_beginner"] += " An extra sentence."
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("byte-identical prose but different rungs", out)


class RungContent(unittest.TestCase):
    def test_every_rung_points_at_the_methods_cautions(self):
        """That sheet is where the UMass before-eggs-hatch deadline lives."""
        for (slug, pid), rung in P.RUNGS.items():
            blob = (rung["note_beginner"] + " " + rung["note_seasoned"]).lower()
            self.assertIn(P.CAUTIONS_POINTER, blob, f"{slug}/{pid}")

    def test_the_attribution_phrase_is_reserved_for_the_DESTROY_group(self):
        for slug, pid in DESTROY:
            blob = (P.RUNGS[(slug, pid)]["note_beginner"] + " " +
                    P.RUNGS[(slug, pid)]["note_seasoned"]).lower()
            self.assertIn(ATTRIBUTION, blob, f"{slug}/{pid}")
        for slug, pid in DIVERT:
            blob = (P.RUNGS[(slug, pid)]["note_beginner"] + " " +
                    P.RUNGS[(slug, pid)]["note_seasoned"]).lower()
            self.assertNotIn(ATTRIBUTION, blob, f"{slug}/{pid}")

    def test_check_REFUSES_a_DIVERT_rung_that_attributes_a_removal_to_the_crop(self):
        """The content defect this split exists to prevent: crediting a source with advice it does
        not give."""
        r = copy.deepcopy(P.RUNGS)
        r[("arugula", "flea-beetles")]["note_seasoned"] += (
            " Removing it is what this crop's guidance calls for.")
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("would credit the crop with a removal step", out)

    def test_check_REFUSES_a_DESTROY_rung_that_drops_the_attribution(self):
        """Replaced case-INSENSITIVELY on purpose. The first version of this test used a lowercase
        str.replace and silently missed turnip's sentence-initial "This crop's guidance", so the
        mutation was inert and the test passed against an unmodified rung. The check lowercases its
        blob, so the injection has to as well or it grades nothing."""
        import re as _re
        r = copy.deepcopy(P.RUNGS)
        for k in ("note_beginner", "note_seasoned"):
            r[("turnip", "harlequin-bug")][k] = _re.sub(
                ATTRIBUTION, "common practice", r[("turnip", "harlequin-bug")][k], flags=_re.I)
        blob = (r[("turnip", "harlequin-bug")]["note_beginner"] + " " +
                r[("turnip", "harlequin-bug")]["note_seasoned"]).lower()
        self.assertNotIn(ATTRIBUTION, blob, "the injection did not actually remove the phrase")
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("does not attribute the removal", out)

    def test_check_REFUSES_a_rung_that_never_points_at_the_cautions(self):
        r = copy.deepcopy(P.RUNGS)
        for k in ("note_beginner", "note_seasoned"):
            r[("kale", "harlequin-bug")][k] = (
                r[("kale", "harlequin-bug")][k].replace("cautions", "notes"))
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("never points the reader at the method's cautions", out)

    def test_check_REFUSES_identical_registers(self):
        """Uses arugula deliberately. Copying kohlrabi's beginner over its seasoned also drops the
        only "cautions" pointer in that pair, so the cautions check fired first and the test passed
        for the wrong reason. arugula is DIVERT_ONLY and carries the pointer in BOTH registers, so
        the copy leaves the pointer intact, adds no attribution phrase, and only the
        identical-registers check can object."""
        r = copy.deepcopy(P.RUNGS)
        r[("arugula", "flea-beetles")] = {
            "note_beginner": P.RUNGS[("arugula", "flea-beetles")]["note_beginner"],
            "note_seasoned": P.RUNGS[("arugula", "flea-beetles")]["note_beginner"],
        }
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        r = copy.deepcopy(P.RUNGS)
        r[("collards", "harlequin-bug")]["note_beginner"] += " The colour will recover."
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("conditions that favour it"))
        self.assertIsNone(P.hygiene(P.RUNGS[("turnip", "harlequin-bug")]["note_seasoned"]))

    def test_no_rung_copies_a_sentence_verbatim_from_its_crops_prose(self):
        by = _by(_pre())
        for (slug, pid), rung in P.RUNGS.items():
            said = P.prose_blob(P.problem(by, slug, pid))
            for reg in ("note_beginner", "note_seasoned"):
                for sent in rung[reg].split(". "):
                    s = sent.strip().rstrip(".")
                    if len(s) > 40:
                        self.assertNotIn(s, said, f"{slug}/{pid} {reg}")

    def test_the_rung_table_and_target_list_agree(self):
        self.assertEqual(set(P.RUNGS), {(s, p) for s, p, _g in P.TARGETS})


class Exclusions(unittest.TestCase):
    def test_the_exclusion_list_is_the_frozen_six(self):
        self.assertEqual(tuple((s, i) for s, i, _r in P.EXCLUSIONS), EXCLUDED)

    def test_every_exclusion_RESOLVES_in_canonical(self):
        pre = _pre()
        for slug, ident in EXCLUDED:
            self.assertIsNotNone(P.find_problem(pre, slug, ident), f"{slug}/{ident}")

    def test_every_exclusion_carries_a_reason(self):
        """A shared message would under-explain nasturtium, which is the one a later pass is most
        likely to talk itself into."""
        for slug, ident, reason in P.EXCLUSIONS:
            self.assertTrue(reason.strip(), f"{slug}/{ident}")
            self.assertGreater(len(reason), 40, f"{slug}/{ident}")

    def test_no_exclusion_is_also_a_target(self):
        self.assertEqual(set(EXCLUDED) & set(ALL_TARGETS), set())

    def test_none_of_the_six_carries_the_rung_after_the_promote(self):
        post = _post()
        for slug, ident in EXCLUDED:
            p = P.find_problem(post, slug, ident)
            self.assertFalse(any(r.get("method") == METHOD
                                 for r in p.get("control_ladder") or []), f"{slug}/{ident}")

    def test_the_four_laddered_exclusions_keep_their_ladders_unchanged(self):
        pre, post = _pre(), None
        post = _post(pre)
        for slug, ident in EXCLUDED:
            a = P.find_problem(pre, slug, ident).get("control_ladder")
            b = P.find_problem(post, slug, ident).get("control_ladder")
            self.assertEqual(b, a, f"{slug}/{ident}")

    def test_check_REFUSES_an_exclusion_that_does_not_resolve(self):
        bad = tuple(P.EXCLUSIONS) + (("radish", "no-such-problem", "typo"),)
        with swap("EXCLUSIONS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("would protect nothing", out)

    def test_check_REFUSES_an_exclusion_that_is_also_a_target(self):
        bad = tuple(P.EXCLUSIONS) + (("cabbage", "harlequin-bug", "contradiction"),)
        with swap("EXCLUSIONS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cannot both be true", out)

    def test_check_REFUSES_an_exclusion_with_no_reason(self):
        bad = tuple(P.EXCLUSIONS[:-1]) + (("zinnia", "Japanese beetles", "   "),)
        with swap("EXCLUSIONS", bad):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("carries no reason", out)


class Placement(unittest.TestCase):
    def test_the_rung_lands_at_the_end_of_the_cultural_run_on_all_ten(self):
        post = _post()
        cm = post["control_methods"]
        by = _by(post)
        for slug, pid in ALL_TARGETS:
            ms = [r["method"] for r in P.problem(by, slug, pid)["control_ladder"]]
            i = ms.index(METHOD)
            self.assertTrue(all(cm[m]["tier"] == "cultural" for m in ms[:i]), f"{slug}/{pid}")
            self.assertTrue(all(cm[m]["tier"] != "cultural" for m in ms[i + 1:]), f"{slug}/{pid}")

    def test_it_is_never_appended_last(self):
        """Appending would break monotonicity: every one of the ten ends above cultural."""
        post = _post()
        by = _by(post)
        for slug, pid in ALL_TARGETS:
            ms = [r["method"] for r in P.problem(by, slug, pid)["control_ladder"]]
            self.assertNotEqual(ms[-1], METHOD, f"{slug}/{pid}")

    def test_all_ten_stay_softest_first(self):
        post = _post()
        cm = post["control_methods"]
        order = {t: i for i, t in enumerate(P.TIERS)}
        by = _by(post)
        for slug, pid in ALL_TARGETS:
            ms = [r["method"] for r in P.problem(by, slug, pid)["control_ladder"]]
            ranks = [order[cm[m]["tier"]] for m in ms]
            self.assertEqual(ranks, sorted(ranks), f"{slug}/{pid}")

    def test_each_ladder_grows_by_exactly_one(self):
        pre = _pre()
        post = _post(pre)
        for slug, pid in ALL_TARGETS:
            a = len(P.problem(_by(pre), slug, pid)["control_ladder"])
            b = len(P.problem(_by(post), slug, pid)["control_ladder"])
            self.assertEqual(b, a + 1, f"{slug}/{pid}")

    def test_cultural_end_is_not_vacuous(self):
        pre = _pre()
        cm = pre["control_methods"]
        lad = P.problem(_by(pre), "arugula", "flea-beetles")["control_ladder"]
        i, bad = P.cultural_end(lad, cm)
        self.assertIsNone(bad)
        self.assertEqual(i, 3)
        scrambled = [lad[-1]] + lad[:-1]
        _i, bad = P.cultural_end(scrambled, cm)
        self.assertIsNotNone(bad)


class BlastRadius(unittest.TestCase):
    def test_no_crop_outside_the_nine_changes(self):
        pre = _pre()
        post = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(post)
        self.assertEqual(set(a["crops"]), set(b["crops"]))
        for slug in a["crops"]:
            if slug in CROPS:
                continue
            self.assertEqual(b["crops"][slug], a["crops"][slug], slug)

    def test_no_other_problem_on_the_nine_changes(self):
        pre = _pre()
        post = _post(pre)
        touched = set(ALL_TARGETS)
        for slug in CROPS:
            for fam in ("pests", "diseases"):
                a = {p["id"]: json.dumps(p, sort_keys=True)
                     for p in (_by(pre)[slug].get(fam) or []) if isinstance(p, dict) and "id" in p}
                b = {p["id"]: json.dumps(p, sort_keys=True)
                     for p in (_by(post)[slug].get(fam) or []) if isinstance(p, dict) and "id" in p}
                self.assertEqual(set(a), set(b), slug)
                for pid in a:
                    if (slug, pid) in touched:
                        continue
                    self.assertEqual(b[pid], a[pid], f"{slug}/{pid}")

    def test_methods_and_sources_untouched(self):
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(b["methods"], a["methods"])
        self.assertEqual(b["sources"], a["sources"])

    def test_key_sets_are_compared_before_values(self):
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(set(a["crops"]), set(b["crops"]))


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_the_post_state(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_the_method_can_legally_reach_every_target_problem_type(self):
        post = _post()
        cm = post["control_methods"]
        by = _by(post)
        from control_ladder_gate import TYPE_TARGETS
        for slug, pid in ALL_TARGETS:
            p = P.problem(by, slug, pid)
            targets = TYPE_TARGETS.get(p["type"]) or set()
            m = cm[METHOD]
            self.assertTrue("any" in m["applies_to"] or set(m["applies_to"]) & targets,
                            f"{slug}/{pid}: {METHOD} cannot reach {p['type']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
