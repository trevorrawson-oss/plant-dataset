#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_chlorothalonil_backfill.py. Base 93e32e2b.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + the mutation harness.

THIS PROMOTE AMENDS NINE LADDERS ON SIX CERTIFIED CROPS, which is the heaviest thing this arc does,
and two families carry it.

`SharedSentence` is the premise. A rung restates a sentence, and three crops share a rung only
because they share the sentence. That is checked in CANONICAL, per group, and a crop whose source
has drifted is refused rather than given somebody else's words. It is batch 5's twin premise applied
at the level of one sentence instead of a whole record.

`JumpShape` is the part a reader would notice. The three cucurbit anthracnose ladders currently END
at `garden_sanitation`, which is cultural, because their prose names no softer spray at all. Adding
this rung makes them run cultural -> conventional, skipping three tiers. That is legal and honest,
and it is also the kind of thing that looks like three forgotten rungs, so the prose says so and the
guard pins that the shape appears in exactly those three and NOWHERE ELSE. A guard that only checked
monotonicity would let the jump spread silently to the other six.

`RungContent` carries group C's three hedges. Its source says the material "can suppress" the
disease "when started early" and that "cultural control is the mainstay for a home crop" -- a rung
promising a cure from that sentence would be this arc's most-repeated defect, on its most dangerous
method.
"""
import copy, hashlib, json, os, sys, unittest
from contextlib import contextmanager

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_chlorothalonil_backfill as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "1330fe5d7b1533eaa165b0a48ddad1c8c9ef0335aa3db74f2c545bc447046781"


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

    def test_nine_targets_across_six_crops(self):
        t = P.targets()
        self.assertEqual(len(t), 9)
        self.assertEqual(len({s for _, s, _ in t}), 6)

    def test_exactly_nine_rungs_are_added(self):
        pre = _pre()
        def count(d):
            return sum(1 for c in d["crops"]
                       for fam in ("pests", "diseases")
                       for p in (c.get(fam) or []) if isinstance(p, dict)
                       for r in (p.get("control_ladder") or []) if r["method"] == P.METHOD)
        self.assertEqual(count(pre), 0)
        self.assertEqual(count(_post(pre)), 9)

    def test_check_REFUSES_when_the_mint_has_not_landed(self):
        pre = _pre()
        del pre["control_methods"][P.METHOD]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("mint must land first", out)

    def test_check_REFUSES_a_non_conventional_method_tier(self):
        pre = _pre()
        pre["control_methods"][P.METHOD]["tier"] = "soft_chemical"
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("conventional tier", out)

    def test_check_REFUSES_running_over_its_own_output(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already carries", out)


class SharedSentence(unittest.TestCase):
    """Three crops share a rung only because they share the sentence it restates."""

    def test_every_group_really_shares_its_phrase_in_canonical(self):
        by = _by(_pre())
        self.assertIsNone(P.check_shared_sentence(by))

    def test_the_group_table_covers_all_nine_and_no_more(self):
        """COVERAGE. An emptied or trimmed table makes the premise check pass over nothing."""
        self.assertEqual(len(P.GROUPS), 3)
        for g, (slugs, pid, phrase) in P.GROUPS.items():
            self.assertEqual(len(slugs), 3, g)
            self.assertTrue(phrase.strip(), g)
            self.assertIn(g, P.RUNGS)
        self.assertEqual(set(P.RUNGS), set(P.GROUPS))

    def test_check_REFUSES_a_crop_whose_sentence_has_drifted(self):
        pre = _pre()
        by = _by(pre)
        p = P.problem(by, "pickling-cucumber", "downy-mildew")
        p["organic_treatment_seasoned"] = "Improve airflow and remove affected leaves."
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("needs its own", out)

    def test_every_phrase_is_specific_enough_to_be_load_bearing(self):
        """The premise is only worth anything if the phrase actually identifies the sentence.

        The first version of this test asserted only that each group's phrase was absent from the
        OTHER group's prose, and the harness showed that passes for a phrase as weak as "the" --
        which happens not to occur in the cucurbit anthracnose sentence. A phrase must name the
        material and carry enough of the claim to be the thing the rung restates."""
        for g, (_slugs, _pid, phrase) in P.GROUPS.items():
            self.assertIn("chlorothalonil", phrase, f"group {g}'s phrase does not name the material")
            self.assertGreaterEqual(len(phrase), 20,
                                    f"group {g}'s phrase is too short to identify a sentence")
        by = _by(_pre())
        a = P.problem(by, "cucumber", "downy-mildew")["organic_treatment_seasoned"].lower()
        self.assertNotIn(P.GROUPS["B"][2], a)
        b = P.problem(by, "cucumber", "anthracnose")["organic_treatment_seasoned"].lower()
        self.assertNotIn(P.GROUPS["A"][2], b)

    def test_group_C_anchors_on_the_hedged_clause_not_the_bare_word(self):
        """Group C's whole reason for its own rung is that its sentence hedges. Anchoring on the
        bare material name would let a differently-hedged sibling into the group."""
        self.assertIn("can suppress", P.GROUPS["C"][2])
        self.assertIn("started early", P.GROUPS["C"][2])


class JumpShape(unittest.TestCase):
    """cultural -> conventional, in exactly three ladders, deliberately."""

    def _jumps(self, d):
        cm = d["control_methods"]
        out = []
        for c in d["crops"]:
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    if not isinstance(p, dict) or not p.get("control_ladder"):
                        continue
                    ms = [r["method"] for r in p["control_ladder"]]
                    if P.METHOD not in ms:
                        continue
                    below = [cm[m]["tier"] for m in ms[:-1]]
                    if below and set(below) == {"cultural"}:
                        out.append((c["slug"], p["id"]))
        return sorted(out)

    def test_the_jump_exists_in_exactly_the_three_cucurbit_anthracnose_ladders(self):
        self.assertEqual(self._jumps(_post()),
                         sorted((s, "anthracnose") for s in P.CUCURBITS))

    def test_the_other_six_step_past_a_soft_chemical_instead(self):
        post = _post()
        cm = post["control_methods"]
        by = _by(post)
        for g, slug, pid in P.targets():
            if g == P.JUMP_GROUP:
                continue
            ms = [r["method"] for r in P.problem(by, slug, pid)["control_ladder"]]
            self.assertEqual(cm[ms[-2]]["tier"], "soft_chemical", f"{slug}/{pid}")

    def test_the_jump_rung_prose_SAYS_it_is_a_jump(self):
        """Otherwise it reads as three rungs somebody forgot."""
        blob = (P.RUNGS[P.JUMP_GROUP]["note_beginner"] + " " +
                P.RUNGS[P.JUMP_GROUP]["note_seasoned"]).lower()
        self.assertIn("gap below it", blob)
        self.assertIn("straight from sanitation", blob)

    def test_check_REFUSES_a_jump_group_target_that_no_longer_tops_out_cultural(self):
        pre = _pre()
        by = _by(pre)
        p = P.problem(by, "cucumber", "anthracnose")
        p["control_ladder"].append({"method": "copper_fungicide",
                                    "note_beginner": "b", "note_seasoned": "s"})
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("no longer describes it", out)

    def test_check_REFUSES_a_non_jump_target_that_became_cultural_topped(self):
        pre = _pre()
        by = _by(pre)
        p = P.problem(by, "dry-bean", "anthracnose")
        p["control_ladder"] = [r for r in p["control_ladder"]
                               if r["method"] != "copper_fungicide"]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("undocumented three-tier jump", out)

    def test_verify_post_CATCHES_the_jump_spreading(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        p = P.problem(_by(d), "dry-bean", "anthracnose")
        p["control_ladder"] = [r for r in p["control_ladder"]
                               if r["method"] != "copper_fungicide"]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("jump appears on", out)


class RungContent(unittest.TestCase):
    def test_the_hedge_table_names_what_each_source_qualifies(self):
        """COVERAGE. The test below iterates REQUIRED_HEDGES, so trimming an entry makes it check
        less and still pass -- the harness caught exactly that on group C's 'suppress'."""
        self.assertEqual(set(P.REQUIRED_HEDGES), set(P.GROUPS))
        self.assertEqual(tuple(P.REQUIRED_HEDGES["C"]), ("suppress", "started early", "mainstay"))
        for g, hedges in P.REQUIRED_HEDGES.items():
            self.assertTrue(hedges, f"group {g} requires no hedge at all")

    def test_every_group_carries_its_source_hedges(self):
        for g, hedges in P.REQUIRED_HEDGES.items():
            blob = (P.RUNGS[g]["note_beginner"] + " " + P.RUNGS[g]["note_seasoned"]).lower()
            for h in hedges:
                self.assertIn(h, blob, f"group {g} dropped {h!r}")

    def test_the_bean_group_states_suppression_not_cure(self):
        blob = (P.RUNGS["C"]["note_beginner"] + " " + P.RUNGS["C"]["note_seasoned"]).lower()
        self.assertIn("suppress", blob)
        self.assertNotIn("cure", blob.replace("cures", ""))
        self.assertIn("mainstay", blob)

    def test_check_REFUSES_a_dropped_hedge(self):
        r = copy.deepcopy(P.RUNGS)
        r["C"]["note_beginner"] = r["C"]["note_beginner"].replace("started early", "used")
        r["C"]["note_seasoned"] = r["C"]["note_seasoned"].replace("starts\nearly", "starts").replace(
            "where treatment starts early", "where treatment is used")
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("started early", out)

    def test_check_REFUSES_identical_registers(self):
        """Uses group B deliberately. Copying group A's beginner over its seasoned also DROPS
        'protectant only', so the hedge check fired first and this test passed for the wrong
        reason. Group B's hedge ('preventiv') is present in both registers, so the copy leaves the
        hedges intact and only the identical-registers check can object."""
        r = copy.deepcopy(P.RUNGS)
        r["B"]["note_seasoned"] = r["B"]["note_beginner"]
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        r = copy.deepcopy(P.RUNGS)
        r["B"]["note_beginner"] += " The colour will recover."
        with swap("RUNGS", r):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_hygiene_is_not_vacuous_and_catches_favour(self):
        self.assertIsNotNone(P.hygiene("conditions that favour it"))
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNone(P.hygiene(P.RUNGS["A"]["note_seasoned"]))

    def test_every_rung_points_at_the_methods_own_cautions(self):
        """The sheet carries the Prop 65 and EPA listing; the rung must send the reader there
        rather than restating a partial version of it."""
        for g in P.RUNGS:
            blob = (P.RUNGS[g]["note_beginner"] + " " + P.RUNGS[g]["note_seasoned"]).lower()
            self.assertTrue("warning" in blob or "caution" in blob,
                            f"group {g} never points the reader at the method's cautions")


class Monotonic(unittest.TestCase):
    def test_all_nine_stay_softest_first(self):
        post = _post()
        cm = post["control_methods"]
        order = {t: i for i, t in enumerate(P.TIERS)}
        by = _by(post)
        for _g, slug, pid in P.targets():
            ms = [r["method"] for r in P.problem(by, slug, pid)["control_ladder"]]
            ranks = [order[cm[m]["tier"]] for m in ms]
            self.assertEqual(ranks, sorted(ranks), f"{slug}/{pid}")

    def test_the_rung_is_appended_LAST_everywhere(self):
        by = _by(_post())
        for _g, slug, pid in P.targets():
            ms = [r["method"] for r in P.problem(by, slug, pid)["control_ladder"]]
            self.assertEqual(ms[-1], P.METHOD, f"{slug}/{pid}")

    def test_verify_post_CATCHES_a_rung_that_is_not_last(self):
        """APPENDS A SECOND CONVENTIONAL rather than moving this one to the front. Moving it forward
        also decreases the tiers, so the monotonicity check answered and the last-rung guard was
        never reached -- the harness reported it as a surviving mutation. A second conventional
        keeps the ranks sorted, so only the last-rung check can object."""
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        lad = P.problem(_by(d), "cucumber", "downy-mildew")["control_ladder"]
        lad.append({"method": "carbaryl", "note_beginner": "b", "note_seasoned": "s"})
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("does not end with", out)

    def test_verify_post_CATCHES_a_tier_decrease_EARLIER_in_the_ladder(self):
        """The rung stays last and unique, so only the monotonicity check can object."""
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        lad = P.problem(_by(d), "dry-bean", "anthracnose")["control_ladder"]
        soft = next(i for i, r in enumerate(lad) if r["method"] == "copper_fungicide")
        lad.insert(0, lad.pop(soft))
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_verify_post_CATCHES_a_duplicated_rung(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        lad = P.problem(_by(d), "dry-bean", "anthracnose")["control_ladder"]
        lad.append(copy.deepcopy(lad[-1]))
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("expected 1", out)

    def test_verify_post_CATCHES_the_wrong_groups_rung(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        lad = P.problem(_by(d), "cucumber", "downy-mildew")["control_ladder"]
        lad[-1]["note_beginner"] = P.RUNGS["C"]["note_beginner"]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("did not get group", out)


class BlastRadius(unittest.TestCase):
    def test_no_crop_outside_the_six_changes(self):
        pre = _pre()
        post = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(post)
        self.assertEqual(set(a["crops"]), set(b["crops"]))
        for slug in a["crops"]:
            if slug in P.CROPS:
                continue
            self.assertEqual(b["crops"][slug], a["crops"][slug], slug)

    def test_no_other_problem_on_the_six_changes(self):
        pre = _pre()
        post = _post(pre)
        touched = {(s, pid) for _g, s, pid in P.targets()}
        for slug in P.CROPS:
            for fam in ("pests", "diseases"):
                a = {p["id"]: json.dumps(p, sort_keys=True)
                     for p in (_by(pre)[slug].get(fam) or []) if isinstance(p, dict)}
                b = {p["id"]: json.dumps(p, sort_keys=True)
                     for p in (_by(post)[slug].get(fam) or []) if isinstance(p, dict)}
                self.assertEqual(set(a), set(b), slug)
                for pid in a:
                    if (slug, pid) in touched:
                        continue
                    self.assertEqual(b[pid], a[pid], f"{slug}/{pid}")

    def test_methods_and_sources_untouched(self):
        pre = _pre()
        post = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(post)
        self.assertEqual(b["methods"], a["methods"])
        self.assertEqual(b["sources"], a["sources"])

    def test_verify_post_CATCHES_a_bystander_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        _by(d)["tomatillo"]["name"] = "MUTATED"
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("touches only", out)

    def test_verify_post_CATCHES_a_dropped_crop(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["crops"] = [c for c in d["crops"] if c.get("slug") != "tomatillo"]
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

    def test_verify_post_CATCHES_a_touched_method(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["control_methods"]["sulfur"]["best_use"] += " x"
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("mints nothing", out)

    def test_verify_post_CATCHES_a_touched_source(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        d["source_catalog"]["clemson_hgic"]["accessed"] = "2099-01"
        out = P.verify_post(P.snapshot(pre), d)
        self.assertIsNotNone(out)
        self.assertIn("source_catalog changed", out)

    def test_verify_post_is_clean_on_the_real_apply(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(P.snapshot(pre), d))


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_the_post_state(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_the_six_crops_still_pass_their_own_gate_shape(self):
        post = _post()
        cm = post["control_methods"]
        by = _by(post)
        from control_ladder_gate import TYPE_TARGETS
        for _g, slug, pid in P.targets():
            p = P.problem(by, slug, pid)
            targets = TYPE_TARGETS.get(p["type"]) or set()
            for r in p["control_ladder"]:
                m = cm[r["method"]]
                self.assertTrue("any" in m["applies_to"] or set(m["applies_to"]) & targets,
                                f"{slug}/{pid}: {r['method']} cannot reach {p['type']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
