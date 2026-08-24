#!/usr/bin/env python3
"""Guard suite for tools/promote_bt_method.py. Base 0e12689b.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_bt_method_suite.py.

THE LOAD-BEARING FAMILY IS `SafetyClaim`, and it is a SIX-part specification because this field was
wrong in two ways at once and self-contradictory besides. The old text said "It ONLY AFFECTS
CATERPILLARS" in sentence three and "it does not tell good caterpillars from bad" in sentence six.
Both were reaching for the same true thing -- Bt is selective to Lepidoptera as a group -- but the
first phrasing is the one that misleads, because the non-target risk IS other caterpillars.

So absence of the banned constructions is never asserted alone: deleting the sentence would satisfy
it while leaving the reader with less than they started with. Every required element must also be
PRESENT, including the actionable consequence ("never a plant you are growing for butterflies")
that turns the caveat into something a gardener can act on.

`LeftAlone` is the second family and guards the opposite failure. A roster-wide scan of all 50
catalog methods returned 15 safety-construction hits and THIRTEEN ARE CORRECT AS WRITTEN --
"non-toxic" on a cardboard collar, a glue card and a pheromone lure is literally accurate, and
"practically nontoxic" in bt's own seasoned register is NPIC's term of art. A sweep that flattened
those would make the record less faithful to its sources, not more.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_bt_method as P  # noqa: E402
import build_bt_method_content as C  # noqa: E402

POST_SHA = "c13ddea5f1320d766847b707d3795c8cc81251d71ed864f61260f9eeb12e73f5"
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _bt(data):
    return data["control_methods"]["bt"]


# --------------------------------------------------------------------------- fixture
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


# --------------------------------------------------------------------------- reachability
class Reachability(unittest.TestCase):
    def test_base_carried_BOTH_constructions(self):
        old = _bt(_pre())["how_it_works_beginner"]
        self.assertEqual(old, C.OLD)
        self.assertIn("only affects caterpillars", old.lower())
        self.assertIn("is safe to eat", old.lower())

    def test_base_contradicted_itself(self):
        """The field said 'only affects caterpillars' AND 'does not tell good caterpillars from
        bad'. That contradiction is the reason this is a rewrite and not a deletion."""
        old = _bt(_pre())["how_it_works_beginner"].lower()
        self.assertIn("only affects caterpillars", old)
        self.assertIn("does not tell good caterpillars from bad", old)

    def test_base_fails_the_post_check(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_passes_the_post_check(self):
        self.assertIsNone(P.verify_post(_post()))


# --------------------------------------------------------------------------- load-bearing 1
class SafetyClaim(unittest.TestCase):
    """Six parts. Absence is never asserted alone."""

    def test_1_no_banned_construction_survives(self):
        got = _bt(_post())["how_it_works_beginner"]
        for pat in C.BANNED:
            self.assertIsNone(re.search(pat, got, re.I), f"{pat!r} survives")

    def test_2_every_required_element_is_present(self):
        got = _bt(_post())["how_it_works_beginner"]
        for label, pat in C.REQUIRED.items():
            self.assertTrue(re.search(pat, got, re.I), f"missing {label}")

    def test_3_the_field_no_longer_contradicts_itself(self):
        got = _bt(_post())["how_it_works_beginner"].lower()
        self.assertNotIn("only affects", got)
        self.assertIn("cannot tell a pest caterpillar from a butterfly one", got)

    def test_4_the_caveat_carries_an_ACTIONABLE_consequence(self):
        """'It cannot tell them apart' is a fact. 'Never spray a plant you grow for butterflies' is
        what a gardener can do about it. The cautions entry has always said this; the beginner
        register now does too."""
        got = _bt(_post())["how_it_works_beginner"].lower()
        self.assertIn("never a plant you are growing for butterflies", got)

    def test_5_the_irritation_warning_is_not_lost_in_the_rewrite(self):
        got = _bt(_post())["how_it_works_beginner"].lower()
        self.assertIn("irritate eyes and skin", got)
        self.assertIn("wear gloves", got)

    def test_6_the_low_toxicity_claim_keeps_its_MECHANISM(self):
        """NPIC's 'low in toxicity ... when eaten' is true BECAUSE mammals cannot activate the
        proteins. Dropping the mechanism would leave a bare reassurance."""
        got = _bt(_post())["how_it_works_beginner"].lower()
        self.assertIn("low in toxicity", got)
        self.assertIn("cannot activate the proteins", got)

    def test_the_required_patterns_reject_prose_that_lacks_them(self):
        """Negative control: constants validated only against the data they guard are vacuous."""
        blank = "Bt is a soil bacterium. Spray it on the leaves."
        for label, pat in C.REQUIRED.items():
            self.assertIsNone(re.search(pat, blank, re.I), f"{label} matches unrelated prose")

    def test_the_source_record_is_qualified_throughout(self):
        for q in C.SOURCE_READ["quotes"]:
            self.assertIsNone(re.search(r"\b(?:is|are)\s+safe\b", q, re.I), q)
        joined = " ".join(C.SOURCE_READ["quotes"]).lower()
        self.assertIn("low in toxicity", joined)
        self.assertIn("non-target moths were harmed", joined)
        self.assertEqual(C.SOURCE_READ["never_says"], "safe (unqualified)")


# --------------------------------------------------------------------------- load-bearing 2
class LeftAlone(unittest.TestCase):
    """13 of 15 roster-wide hits are correct as written. Flattening them would be a regression."""

    def test_npics_own_term_of_art_survives_in_the_seasoned_register(self):
        m = _bt(_post())
        self.assertIn("practically nontoxic", m["how_it_works_seasoned"].lower())
        self.assertTrue(any("practically nontoxic" in p.lower() for p in m["pros"]))

    def test_every_other_bt_field_is_byte_identical(self):
        pre, post = _bt(_pre()), _bt(_post())
        for f in C.UNTOUCHED_BT_FIELDS:
            self.assertEqual(pre.get(f), post.get(f), f"bt.{f} changed")

    def test_the_cautions_entry_still_names_swallowtails_and_monarchs(self):
        joined = " ".join(_bt(_post()).get("cautions") or []).lower()
        self.assertIn("swallowtails", joined)
        self.assertIn("monarchs", joined)

    def test_the_correct_as_written_methods_are_untouched(self):
        pre, post = _pre(), None
        post = _post(pre)
        for k in C.CORRECT_AS_WRITTEN:
            self.assertEqual(pre["control_methods"][k], post["control_methods"][k], k)

    def test_their_accurate_language_still_reads_as_written(self):
        """If these go green by the words vanishing, the guard above measures nothing."""
        cm = _post()["control_methods"]
        self.assertTrue(any("non-toxic" in p.lower() for p in cm["stem_collars"]["pros"]))
        self.assertTrue(any("completely selective" in p.lower() for p in cm["handpick"]["pros"]))
        self.assertTrue(any("non-toxic" in p.lower() for p in cm["yellow_sticky_traps"]["pros"]))

    def test_the_correct_as_written_record_is_enumerated_not_counted(self):
        """A renamed key kept the shape once and the harness caught it. Enumerate."""
        self.assertEqual(set(C.CORRECT_AS_WRITTEN), {
            "stem_collars", "yellow_sticky_traps", "red_sphere_trap", "slug_traps_barriers",
            "swd_monitoring_traps", "codling_moth_pheromone_trap", "handpick",
            "swd_exclusion_netting"})


# --------------------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_exactly_one_string_changes_in_the_whole_dataset(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(pre["crops"], post["crops"])
        self.assertEqual(pre["source_catalog"], post["source_catalog"])
        a, b = pre["control_methods"], post["control_methods"]
        self.assertEqual(set(a), set(b))
        changed = {k for k in a if a[k] != b[k]}
        self.assertEqual(changed, {"bt"})
        diff = {f for f in a["bt"] if a["bt"][f] != b["bt"][f]}
        self.assertEqual(diff, {"how_it_works_beginner"})

    def test_no_crop_prose_is_touched(self):
        """cffa4a7 and 9116050 fixed the crops; this fixes the catalog. They must not overlap."""
        pre = _pre()
        post = _post(pre)
        for a, b in zip(pre["crops"], post["crops"]):
            self.assertEqual(a, b, a.get("slug"))

    def test_method_count_unchanged(self):
        self.assertEqual(len(_pre()["control_methods"]), len(_post()["control_methods"]))


# --------------------------------------------------------------------------- copy hygiene
class CopyHygiene(unittest.TestCase):
    def test_no_dash_forms(self):
        self.assertIsNone(re.search(r"[—–]", C.NEW))
        self.assertNotIn("--", C.NEW)

    def test_american_english(self):
        for w in BRITISH:
            self.assertIsNone(re.search(rf"\b{w}\b", C.NEW, re.I), w)

    def test_no_absolute_claim_vocabulary(self):
        self.assertIsNone(re.search(
            r"\b(?:always|guaranteed|completely|totally|harmless)\b", C.NEW, re.I), C.NEW[:80])

    def test_registers_stay_materially_different(self):
        m = _bt(_post())
        self.assertNotEqual(m["how_it_works_beginner"], m["how_it_works_seasoned"])

    def test_the_beginner_register_stays_common_tongue(self):
        """Lepidoptera and kurstaki belong in the seasoned half, not here."""
        got = _bt(_post())["how_it_works_beginner"].lower()
        for jargon in ("lepidoptera", "kurstaki", "crystal protein", "alkaline"):
            self.assertNotIn(jargon, got)


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_when_the_prose_moved_under_us(self):
        d = _pre()
        _bt(d)["how_it_works_beginner"] = C.OLD.replace("Bt is a natural", "Bt is a common")
        self.assertIsNotNone(P.check(d))

    def test_refuses_if_the_method_is_missing(self):
        d = _pre()
        d["control_methods"].pop("bt")
        self.assertIsNotNone(P.check(d))

    def test_refuses_if_a_correct_as_written_method_vanished(self):
        d = _pre()
        d["control_methods"].pop("stem_collars")
        self.assertIsNotNone(P.check(d))

    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
