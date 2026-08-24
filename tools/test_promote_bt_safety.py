#!/usr/bin/env python3
"""Guard suite for tools/promote_bt_safety.py. Base afe4d697.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_bt_safety_suite.py.

THE LOAD-BEARING FAMILY IS `SafetyClaim`, and it is a THREE-part specification, not two. The
sentence being replaced had two defects:
  * "which is SAFE"                 -- an unhedged absolute; NPIC says "low in toxicity", never "safe"
  * "targets ONLY caterpillars"     -- literally true and consumer-MISLEADING, because the non-target
                                       risk IS other caterpillars ("a few studies also found that
                                       non-target moths were harmed")
So the guards assert all three of: the absolute is GONE roster-wide in Bt prose; every rewritten
field CARRIES the qualified toxicity claim; and every rewritten field CARRIES the non-target caveat.
Drop any one and the promote can pass while leaving the reader worse informed than a blank field
would. Absence alone is satisfied by deleting the sentence, which is why it is never asserted alone.

`ScopeDiscipline` guards the opposite failure. Four corn crops say Bt "only works while they are
still out on the leaves" -- an EFFICACY limitation, correctly stated, that a naive "only" scan
flags. They must stay untouched. Three other crops (dill, viola, parsley) already carry the
butterfly nuance and are the model these nine were out of step with; they must stay untouched too.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_bt_safety as P  # noqa: E402
import build_bt_safety_content as C  # noqa: E402

POST_SHA = "0f911326d2f4ca20c4b92e199afca3c8e842eb8fa422b1b2a1d537a3d20ac093"
TOUCHED = {"kale", "collards", "spinach", "arugula", "bok-choy", "cauliflower",
           "cabbage", "brussels-sprouts", "kohlrabi"}
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _leaves(data):
    out = {}
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for i, p in enumerate(c.get(fam) or []):
                if not isinstance(p, dict):
                    continue
                for k, v in p.items():
                    if isinstance(v, str):
                        out[f"{c.get('slug')}|{fam}|{i}|{k}"] = v
    return out


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

    def test_nine_edits_on_nine_crops(self):
        self.assertEqual(len(C.EDITS), 9)
        self.assertEqual({e[0] for e in C.EDITS}, TOUCHED)
        self.assertEqual({e[2] for e in C.EDITS}, {"organic_treatment_beginner"})


# --------------------------------------------------------------------------- reachability
class Reachability(unittest.TestCase):
    def test_base_carried_the_absolute_in_every_edited_field(self):
        pre = _pre()
        for slug, pname, field, old, _new in C.EDITS:
            p = P._find(pre, slug, pname)
            self.assertIsNotNone(p, f"{slug}/{pname}")
            self.assertEqual(p[field], old)
            self.assertIn("which is safe and targets only caterpillars", old)

    def test_base_fails_the_post_check(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_passes_the_post_check(self):
        self.assertIsNone(P.verify_post(_post()))


# --------------------------------------------------------------------------- load-bearing
class SafetyClaim(unittest.TestCase):
    """Three parts. Any one alone is vacuous."""

    def test_1_no_absolute_survives_anywhere_in_Bt_prose(self):
        post = _post()
        for label, text in P.iter_prose(post):
            if not re.search(C.SCOPE, text, re.I):
                continue
            for pat in C.BANNED:
                self.assertIsNone(re.search(pat, text, re.I), f"{pat!r} survives at {label}")

    def test_2_every_rewritten_field_carries_the_qualified_toxicity_claim(self):
        post = _post()
        for slug, pname, field, _old, new in C.EDITS:
            got = P._find(post, slug, pname)[field]
            self.assertEqual(got, new)
            self.assertTrue(re.search(C.REQUIRED_QUALIFIER, got, re.I),
                            f"{slug} lost 'low in toxicity'")

    def test_3_every_rewritten_field_carries_the_NON_TARGET_caveat(self):
        """The half that matters. Without it the reader is still told Bt hits nothing they care
        about, which is the misleading part of the original sentence rather than the unhedged part."""
        post = _post()
        for slug, pname, field, _old, new in C.EDITS:
            got = P._find(post, slug, pname)[field]
            self.assertTrue(re.search(C.REQUIRED_NONTARGET, got, re.I),
                            f"{slug} lost the butterfly caveat")
            self.assertIn("cannot tell", got.lower(), slug)

    def test_the_replacement_never_says_bt_is_safe(self):
        for _s, _p, _f, _o, new in C.EDITS:
            self.assertIsNone(re.search(r"\bis\s+safe\b", new, re.I), new[:80])

    def test_the_replacement_scopes_treatment_to_affected_plants(self):
        """NPIC's practical consequence: spray only plants with a problem."""
        for slug, _p, _f, _o, new in C.EDITS:
            self.assertIn("only the plants that have a problem", new, slug)

    def test_the_source_record_names_the_nontarget_finding(self):
        joined = " ".join(C.SOURCE_READ["quotes"]).lower()
        self.assertIn("non-target moths were harmed", joined)
        self.assertEqual(C.SOURCE_READ["id"], "npic_orst")

    def test_no_recorded_quote_makes_a_bare_safety_claim(self):
        """COVERAGE, not overlap. The first version of this guard asserted 'low in toxicity'
        appeared SOMEWHERE in the joined quotes -- which a second, still-qualified quote satisfied
        even after the first was mutated to 'Bt is safe for people'. The mutation harness caught
        that as a survivor. Every quote is now checked individually."""
        for q in C.SOURCE_READ["quotes"]:
            self.assertIsNone(re.search(r"\b(?:is|are)\s+safe\b", q, re.I), q)
        self.assertEqual(C.SOURCE_READ["never_says"], "safe (unqualified)")

    def test_the_people_and_mammals_quote_is_itself_qualified(self):
        mammal = [q for q in C.SOURCE_READ["quotes"] if "mammals" in q.lower()]
        self.assertTrue(mammal, "the people/mammals quote is missing from the record")
        for q in mammal:
            self.assertIn("low in toxicity", q.lower(), q)

    def test_the_required_patterns_actually_reject_prose_that_lacks_the_concept(self):
        """A constant validated only against data the SAME module supplies is vacuous: weakening
        REQUIRED_NONTARGET to r'' matched everything and no test noticed, which the harness caught
        as a survivor. These are the constants' negative and positive controls."""
        blank = "Spray Bt on the leaves and repeat after rain."
        self.assertIsNone(re.search(C.REQUIRED_NONTARGET, blank, re.I),
                          "REQUIRED_NONTARGET matches prose with no caveat; it has been weakened")
        self.assertIsNone(re.search(C.REQUIRED_QUALIFIER, blank, re.I),
                          "REQUIRED_QUALIFIER matches prose with no toxicity claim")
        self.assertTrue(re.search(C.REQUIRED_NONTARGET, "from a butterfly one", re.I))
        self.assertTrue(re.search(C.REQUIRED_QUALIFIER, "low in toxicity to bees", re.I))

    def test_the_cited_source_is_catalogued_and_T1(self):
        sc = _post()["source_catalog"]
        self.assertIn(C.SOURCE_READ["id"], sc)
        self.assertEqual(sc[C.SOURCE_READ["id"]].get("tier"), "T1")


# --------------------------------------------------------------------------- scope discipline
class ScopeDiscipline(unittest.TestCase):
    def test_the_corn_efficacy_only_is_left_exactly_as_found(self):
        """'Bt only works while they are still out on the leaves' is a correctly-stated LIMITATION,
        not a safety claim. A naive 'only' scan flags it; this promote must not touch it."""
        pre = _pre()
        post = _post(pre)
        for slug in C.CORN_EFFICACY_ONLY:
            self.assertEqual(P._crop_of(pre, slug), P._crop_of(post, slug), slug)

    def test_the_corn_efficacy_sentences_still_exist(self):
        """If this goes green by the sentences vanishing, the guard above is measuring nothing."""
        post = _post()
        hits = [lab for lab, t in P.iter_prose(post)
                if "only works while they are still out on the leaves" in t]
        self.assertEqual(len(hits), len(C.CORN_EFFICACY_ONLY), hits)

    def test_the_crops_that_already_had_it_right_are_untouched(self):
        pre = _pre()
        post = _post(pre)
        for slug in C.ALREADY_CORRECT:
            self.assertEqual(P._crop_of(pre, slug), P._crop_of(post, slug), slug)

    def test_the_seasoned_spare_beneficials_claim_is_NOT_swept_in(self):
        """A different claim, deliberately out of scope and recorded in NOT_FIXED."""
        post = _post()
        hits = [lab for lab, t in P.iter_prose(post) if "spare beneficials" in t]
        self.assertTrue(hits, "the out-of-scope claim vanished; scope was silently widened")
        self.assertTrue(C.NOT_FIXED)


# --------------------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_leaf_sets_identical_before_any_value_comparison(self):
        pre = _pre()
        post = _post(pre)
        a, b = _leaves(pre), _leaves(post)
        self.assertEqual(set(a), set(b))

    def test_exactly_nine_leaves_changed(self):
        pre = _pre()
        post = _post(pre)
        a, b = _leaves(pre), _leaves(post)
        self.assertEqual(set(a), set(b))
        changed = {k for k in a if a[k] != b[k]}
        self.assertEqual(len(changed), 9, sorted(changed))
        self.assertEqual({k.split("|")[0] for k in changed}, TOUCHED)

    def test_no_control_method_or_source_changes(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(pre["control_methods"], post["control_methods"])
        self.assertEqual(pre["source_catalog"], post["source_catalog"])

    def test_no_ladder_id_or_type_is_touched(self):
        pre = _pre()
        post = _post(pre)
        def skel(d):
            return [(c.get("slug"), fam, i, p.get("id"), p.get("type"),
                     json.dumps(p.get("control_ladder"), sort_keys=True))
                    for c in d["crops"] for fam in ("pests", "diseases")
                    for i, p in enumerate(c.get(fam) or []) if isinstance(p, dict)]
        self.assertEqual(skel(pre), skel(post))


# --------------------------------------------------------------------------- copy hygiene
class CopyHygiene(unittest.TestCase):
    def test_no_dash_forms_barred_in_copy(self):
        for _s, _p, _f, _o, new in C.EDITS:
            self.assertIsNone(re.search(r"[—–]", new), new[:60])
            self.assertNotIn("--", new)

    def test_american_english(self):
        for _s, _p, _f, _o, new in C.EDITS:
            for w in BRITISH:
                self.assertIsNone(re.search(rf"\b{w}\b", new, re.I), f"{w} in {new[:60]}")

    def test_no_absolute_claim_vocabulary(self):
        for _s, _p, _f, _o, new in C.EDITS:
            self.assertIsNone(re.search(
                r"\b(?:always|guaranteed|completely|totally|harmless)\b", new, re.I), new[:80])

    def test_the_rain_reapplication_advice_survives_every_rewrite(self):
        """Bt breaks down; losing 'spray again after rain' would trade a safety fix for an
        efficacy defect."""
        for slug, _p, _f, _o, new in C.EDITS:
            self.assertIn("Spray again after rain", new, slug)


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    """REFUSAL-SPEC: green here means check() REFUSED a bad input."""

    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_a_missing_crop(self):
        d = _pre()
        d["crops"] = [c for c in d["crops"] if c.get("slug") != "kohlrabi"]
        self.assertIsNotNone(P.check(d))

    def test_refuses_when_the_prose_moved_under_us(self):
        d = _pre()
        p = P._find(d, "spinach", "Caterpillars (loopers and armyworms)")
        p["organic_treatment_beginner"] = p["organic_treatment_beginner"].replace("Spray", "Apply")
        self.assertIsNotNone(P.check(d))

    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
