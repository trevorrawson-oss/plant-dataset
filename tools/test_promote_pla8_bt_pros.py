#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_bt_pros.py. Base 3ec673a7.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_bt_pros_suite.py.

THE LOAD-BEARING FAMILY IS `SheetDoesNotContradictItself`. This defect was never structural. Every
gate passed the record; `pros` and `cautions` are both well-formed and both individually true-ish.
What was wrong is that MethodSheet.tsx renders them on the SAME sheet, pros first, and a reader
scrolling meets "sparing most beneficial insects" seventeen lines before "kills ... swallowtails and
monarchs". So the guards assert a RELATIONSHIP between two fields, which is the only level at which
the defect exists.

`LeftAlone` is the other half. The sweep that found this returned 40 selectivity sentences and one
defect; five adjudicated entries are pinned byte-for-byte so a later pass cannot "finish the job"
by scrubbing correct hedges. neem_oil's claim is qualified ("once it dries"), iron phosphate's is
comparative ("safer THAN metaldehyde"), insecticidal_soap's is an admission of harm, and bt's own
pros[0] is NPIC's term of art.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_bt_pros as P  # noqa: E402

POST_SHA = "5696aead08e2e197c06cec78824acf97feac8d8ff67043e82594b4b440b7f71e"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


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


class SheetDoesNotContradictItself(unittest.TestCase):
    """The defect existed only in the relationship between two fields on one rendered sheet."""

    def test_the_base_DOES_contradict_itself(self):
        """REACHABILITY for the whole promote: if this ever passes on the base, there was nothing
        to fix and every assertion below is decoration."""
        bt = _pre()["control_methods"]["bt"]
        pro = bt["pros"][1].lower()
        caution = bt["cautions"][0].lower()
        self.assertIn("only", pro)
        self.assertIn("sparing most beneficial insects", pro)
        self.assertIn("swallowtails and monarchs", caution)

    def test_NO_pro_in_the_catalog_carries_the_banned_construction(self):
        """The general form, over all 50 methods, so the next method to acquire this shape fails
        here instead of shipping.

        AN EARLIER VERSION OF THIS TEST WAS A FUZZY CONTRADICTION DETECTOR -- "does any pros entry
        claim sparing while its cautions admit harm to a beneficial" -- and it flagged the APPROVED
        replacement. That was the test being wrong, not the copy: the new text hedges with "most
        other beneficials", but so did the old one ("sparing most beneficial insects"), so a hedge
        detector cannot tell them apart. The word doing the damage was "only", which reads as "only
        pests" rather than "only caterpillars".

        So this asserts the construction, not the contradiction. Whether two fields contradict each
        other needs READING; a heuristic that stands in for it would flood on correct copy later,
        and this repo has already paid for gates that flood.
        """
        cm = _post()["control_methods"]
        bad = [f"{k}.pros[{i}]: {p}" for k, m in cm.items()
               for i, p in enumerate(m.get("pros") or []) if P.BANNED.search(p)]
        self.assertEqual(bad, [])

    def test_the_construction_is_gone_from_EVERY_field_of_bt(self):
        """Not just pros. The whole point of this promote is that the claim lives in FIELDS, and
        23b4539 fixed one of them while `pros` kept it."""
        bt = _post()["control_methods"]["bt"]
        for f, v in bt.items():
            for s in (v if isinstance(v, list) else [v]):
                if isinstance(s, str):
                    with self.subTest(field=f):
                        self.assertIsNone(P.BANNED.search(s), f"{f}: {s[:80]}")

    def test_the_banned_construction_is_gone_from_bt(self):
        for s in _post()["control_methods"]["bt"]["pros"]:
            self.assertIsNone(P.BANNED.search(s), s)

    def test_check_REFUSES_if_BANNED_stops_matching_the_text_it_removes(self):
        """Exercises the runtime self-check, not just the constants.

        `test_the_banned_pattern_actually_matches_the_OLD_text` reads P.BANNED and P.OLD directly,
        so it says nothing about the guard inside check() that asserts the same thing at promote
        time. Disabling that guard therefore changed nothing observable and the harness scored it a
        survivor. This drives check() with a weakened pattern, which is the only state in which the
        guard can speak.

        It is worth keeping rather than deleting as redundant: it is the promote's own answer to
        "is the pattern I am verifying my work with still able to see the defect?", and someone can
        edit BANNED and re-run the promote without ever running this suite.
        """
        orig = P.BANNED
        try:
            P.BANNED = re.compile(r"(?!x)x")      # matches nothing
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("does not match the text this promote exists to remove", out)
        finally:
            P.BANNED = orig
        self.assertIsNotNone(P.BANNED.search(P.OLD), "BANNED was not restored")

    def test_the_banned_pattern_actually_matches_the_OLD_text(self):
        """A pattern that matches nothing is a guard that reports success without checking. This is
        the vacuity the c13ddea5 sweep hit from the other side: it read this very field and asked it
        the wrong question, because its vocabulary was safe/non-toxic/completely."""
        self.assertIsNotNone(P.BANNED.search(P.OLD))
        self.assertIsNone(P.BANNED.search(P.NEW))

    def test_the_true_selectivity_claim_SURVIVES(self):
        """Deleting the pro would satisfy a naive 'banned construction gone' check while leaving the
        reader worse off. Btk's selectivity is the reason to choose it."""
        pro = _post()["control_methods"]["bt"]["pros"][1].lower()
        self.assertIn("caterpillars", pro)
        self.assertIn("spar", pro)
        self.assertIn("bees", pro)

    def test_it_does_NOT_repeat_the_instruction_a_fourth_time(self):
        """how_it_works_beginner, best_use and cautions each already tell the reader to keep it off
        butterfly plants. A fourth on the same sheet, inside a benefits list, is noise."""
        bt = _post()["control_methods"]["bt"]
        self.assertNotIn("growing for butterflies", bt["pros"][1])
        for f in ("how_it_works_beginner", "best_use"):
            self.assertIn("butterflies", bt[f], f"{f} should still carry it")
        self.assertIn("butterfly host plants", bt["cautions"][0])

    def test_the_voice_matches_the_rest_of_the_sheet(self):
        """'as a group' is the phrasing how_it_works_beginner and best_use already use."""
        bt = _post()["control_methods"]["bt"]
        self.assertIn("as a group", bt["pros"][1])
        self.assertIn("as a group", bt["best_use"])


class LeftAlone(unittest.TestCase):
    """40 selectivity sentences, 1 defect. The correct hedges must not be scrubbed later."""

    def test_every_adjudicated_entry_survives_byte_for_byte(self):
        post = _post()
        for path, text in P.LEFT_ALONE.items():
            with self.subTest(path=path):
                self.assertEqual(P._at(post, path), text)

    def test_the_left_alone_list_is_not_empty_or_trivial(self):
        self.assertGreaterEqual(len(P.LEFT_ALONE), 5)

    def test_bt_pros_0_keeps_NPIC_term_of_art(self):
        """'practically nontoxic' is NPIC's own wording and is already qualified. Rewriting it
        would make the record LESS faithful to the source, not more."""
        self.assertEqual(_post()["control_methods"]["bt"]["pros"][0],
                         "Practically nontoxic to people, pets, bees, and wildlife")

    def test_only_ONE_string_changes_in_the_whole_file(self):
        pre, post = _pre(), _post()
        self.assertEqual(set(pre["control_methods"]), set(post["control_methods"]))
        changed = [k for k in pre["control_methods"]
                   if pre["control_methods"][k] != post["control_methods"][k]]
        self.assertEqual(changed, ["bt"])
        a, b = dict(pre["control_methods"]["bt"]), dict(post["control_methods"]["bt"])
        self.assertNotEqual(a.pop("pros"), b.pop("pros"))
        self.assertEqual(a, b, "a field of bt other than pros moved")
        self.assertEqual(pre["control_methods"]["bt"]["pros"][0],
                         post["control_methods"]["bt"]["pros"][0])

    def test_zero_crops_change(self):
        pre = _pre()
        post = _post(pre)
        by = {c["slug"]: c for c in post["crops"]}
        self.assertEqual([c["slug"] for c in pre["crops"]], [c["slug"] for c in post["crops"]])
        self.assertEqual([c["slug"] for c in pre["crops"] if c != by[c["slug"]]], [])

    def test_no_ladder_changes(self):
        pre = _pre()
        post = _post(pre)
        def lad(d):
            return [(c["slug"], p.get("id"), [r["method"] for r in p.get("control_ladder") or []])
                    for c in d["crops"] for f in ("pests", "diseases")
                    for p in (c.get(f) or []) if isinstance(p, dict) and p.get("control_ladder")]
        self.assertEqual(lad(pre), lad(post))
        self.assertEqual(len(lad(post)), 149)


class Reachability(unittest.TestCase):
    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_refuses_when_already_applied(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already applied", out)

    def test_refuses_if_the_text_drifted(self):
        d = _pre()
        d["control_methods"]["bt"]["pros"][1] = "Something else."
        out = P.check(d)
        self.assertIsNotNone(out)
        self.assertIn("not the expected text", out)

    def test_refuses_if_a_left_alone_entry_moved(self):
        d = _pre()
        d["control_methods"]["neem_oil"]["best_use"] = "Scrubbed."
        out = P.check(d)
        self.assertIsNotNone(out)
        self.assertIn("left-alone", out)

    def test_apply_raises_rather_than_overwriting_drift(self):
        d = _pre()
        d["control_methods"]["bt"]["pros"][1] = "drifted"
        with self.assertRaises(AssertionError):
            P.apply_to(d)

    def test_post_check_fails_on_the_base(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_hygiene_rejects_things(self):
        for bad in ("an em dash — here", "it is completely safe", "the colour of it",
                    "this is safe to use"):
            self.assertIsNotNone(P.hygiene(bad), bad)
        self.assertIsNone(P.hygiene(P.NEW))


if __name__ == "__main__":
    unittest.main(verbosity=2)
