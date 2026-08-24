#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_slug_bait_safety.py. Base 75b3c0f0.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_sbs_suite.py.

THE LOAD-BEARING FAMILY IS `SafetyClaim`. This promote exists because consumer copy asserted a
pesticide IS SAFE, where the T1 source publishes only a COMPARATIVE ("safer ... than metaldehyde").
So the guards that matter assert two things at once, because either alone is vacuous:
  * the absolute is GONE, roster-wide, everywhere slug-bait prose appears; and
  * every rewritten field CARRIES the comparative that replaced it.
Absence alone would be satisfied by deleting the sentence. Presence alone would be satisfied by a
field that says both. The pair is the specification.

`ScopeDiscipline` is the second family and guards the opposite failure: this promote must NOT have
quietly swept in the Bt absolute that shares the phrase "which is safe" on nine other crops. That
class is real, recorded in the content module, and deliberately untouched. A guard that asserts we
did NOT change something is unusual; it is here because the roster-wide post-check found the Bt
class mid-build and the tempting move was to widen silently.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_slug_bait_safety as P  # noqa: E402
import build_slug_bait_safety_content as C  # noqa: E402

POST_SHA = "6b295d440a8d4bfbad240c0cbf1bfdc83ccad1059c2d615ac8f9f5765e9d69ca"
TOUCHED_CROPS = {"basil", "lettuce-leaf", "swiss-chard", "arugula", "bok-choy", "sage"}
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _leaves(data):
    """Every crop prose string, keyed by a stable path. The blast-radius unit is the LEAF."""
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
        """`post` is this promote's OWN replayed output, never live canonical."""
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)

    def test_nine_edits_on_six_crops(self):
        self.assertEqual(len(C.EDITS), 9)
        self.assertEqual({e[0] for e in C.EDITS}, TOUCHED_CROPS)


# --------------------------------------------------------------------------- reachability
class Reachability(unittest.TestCase):
    """Proves the guards below CAN fire: the base state really carried the defect."""

    def test_base_carried_an_absolute_in_every_edited_field(self):
        pre = _pre()
        for slug, pname, field, old, _new in C.EDITS:
            p = P._find(pre, slug, pname)
            self.assertIsNotNone(p, f"{slug}/{pname}")
            self.assertEqual(p[field], old, f"{slug}/{pname}/{field}")
            self.assertTrue(any(re.search(pat, old, re.I) for pat in C.BANNED),
                            f"{slug}/{pname}/{field} pre-text matched no banned pattern")

    def test_base_fails_the_post_check(self):
        """The refusal is reachable: run the POST assertions against the PRE state."""
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_passes_the_post_check(self):
        self.assertIsNone(P.verify_post(_post()))


# --------------------------------------------------------------------------- load-bearing
class SafetyClaim(unittest.TestCase):
    """Absence of the absolute AND presence of the comparative. Either alone is vacuous."""

    def test_no_absolute_survives_anywhere_in_slug_bait_prose(self):
        post = _post()
        for label, text in P.iter_prose(post):
            if not re.search(C.SCOPE, text, re.I):
                continue
            for pat in C.BANNED:
                self.assertIsNone(re.search(pat, text, re.I), f"{pat!r} survives at {label}")

    def test_every_rewritten_field_carries_the_comparative(self):
        post = _post()
        for slug, pname, field, _old, new in C.EDITS:
            got = P._find(post, slug, pname)[field]
            self.assertEqual(got, new, f"{slug}/{pname}/{field}")
            self.assertTrue(re.search(C.REQUIRED_COMPARATIVE, got, re.I),
                            f"{slug}/{pname}/{field} lost the comparative")

    def test_the_comparative_is_against_metaldehyde_not_a_bare_reassurance(self):
        """UC IPM's claim is comparative and the comparison is its whole content. A field that
        says 'lower risk' without naming what it is lower than has dropped the substance."""
        for slug, pname, field, _old, new in C.EDITS:
            self.assertIn("metaldehyde", new.lower(), f"{slug}/{pname}/{field}")

    def test_no_edited_field_still_calls_the_bait_plainly_safe(self):
        for _s, _p, _f, _o, new in C.EDITS:
            self.assertIsNone(re.search(r"\b(?:is|are)\s+safe\b", new, re.I), new[:80])

    def test_the_source_quote_is_comparative(self):
        """Guards the CONTENT module's record of what was read, not the data."""
        self.assertIn("safer", C.SOURCE_READ["quote"].lower())
        self.assertNotIn("is safe", C.SOURCE_READ["quote"].lower())


# --------------------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_leaf_sets_are_identical_before_any_value_comparison(self):
        """set(pre) == set(post) FIRST. Iterating pre alone makes additions in post invisible."""
        pre, post = _pre(), None
        post = _post(pre)
        a, b = _leaves(pre), _leaves(post)
        self.assertEqual(set(a), set(b))

    def test_exactly_the_nine_intended_leaves_changed(self):
        pre = _pre()
        post = _post(pre)
        a, b = _leaves(pre), _leaves(post)
        self.assertEqual(set(a), set(b))
        changed = {k for k in a if a[k] != b[k]}
        self.assertEqual(len(changed), 9, sorted(changed))
        self.assertEqual({k.split("|")[0] for k in changed}, TOUCHED_CROPS)
        self.assertEqual({k.split("|")[3] for k in changed},
                         {"organic_treatment_beginner", "organic_treatment_seasoned"})

    def test_no_control_method_is_touched(self):
        pre = _pre()
        self.assertEqual(pre["control_methods"], _post(pre)["control_methods"])

    def test_no_source_catalog_change(self):
        pre = _pre()
        self.assertEqual(pre["source_catalog"], _post(pre)["source_catalog"])

    def test_no_problem_id_type_or_ladder_is_touched(self):
        pre = _pre()
        post = _post(pre)
        def skel(d):
            return [(c.get("slug"), fam, i, p.get("id"), p.get("type"),
                     json.dumps(p.get("control_ladder"), sort_keys=True))
                    for c in d["crops"] for fam in ("pests", "diseases")
                    for i, p in enumerate(c.get(fam) or []) if isinstance(p, dict)]
        self.assertEqual(skel(pre), skel(post))

    def test_crop_and_problem_counts_unchanged(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(len(pre["crops"]), len(post["crops"]))
        self.assertEqual([c.get("slug") for c in pre["crops"]],
                         [c.get("slug") for c in post["crops"]])


# --------------------------------------------------------------------------- scope discipline
class ScopeDiscipline(unittest.TestCase):
    """This promote must NOT have swept in the Bt absolute. See BT_ABSOLUTE_CROPS."""

    def test_the_bt_absolute_is_left_exactly_as_found(self):
        pre = _pre()
        post = _post(pre)
        for slug in C.BT_ABSOLUTE_CROPS:
            a = [c for c in pre["crops"] if c.get("slug") == slug][0]
            b = [c for c in post["crops"] if c.get("slug") == slug][0]
            for fam in ("pests", "diseases"):
                for i, p in enumerate(a.get(fam) or []):
                    if not isinstance(p, dict):
                        continue
                    q = b[fam][i]
                    for k, v in p.items():
                        if isinstance(v, str) and "which is safe" in v.lower():
                            self.assertEqual(v, q[k], f"{slug}/{p.get('name')}/{k} was swept in")

    def test_the_bt_class_is_still_present_and_therefore_still_owed(self):
        """If this ever goes green-by-absence, the Bt class was fixed elsewhere and this guard
        plus the BT_ABSOLUTE_CROPS record should be retired deliberately, not silently."""
        post = _post()
        found = {c.get("slug") for c in post["crops"]
                 for fam in ("pests", "diseases") for p in (c.get(fam) or [])
                 if isinstance(p, dict)
                 for v in p.values()
                 if isinstance(v, str) and re.search(r"\bwhich\s+is\s+safe\b", v, re.I)}
        self.assertEqual(found, set(C.BT_ABSOLUTE_CROPS))

    def test_the_negated_and_damage_level_uses_are_untouched(self):
        """cayenne/habanero say 'not completely safe' (a hedge); persimmon/pawpaw say 'harmless'
        about a DAMAGE LEVEL. Neither is this class and neither may be rewritten."""
        pre = _pre()
        post = _post(pre)
        for slug in ("cayenne-pepper", "habanero", "persimmon", "pawpaw"):
            a = [c for c in pre["crops"] if c.get("slug") == slug]
            if not a:
                continue
            b = [c for c in post["crops"] if c.get("slug") == slug][0]
            self.assertEqual(a[0], b, slug)


# --------------------------------------------------------------------------- copy hygiene
class CopyHygiene(unittest.TestCase):
    def test_no_dash_forms_barred_in_consumer_copy(self):
        for _s, _p, _f, _o, new in C.EDITS:
            self.assertIsNone(re.search(r"[—–]", new), new[:60])
            self.assertNotIn("--", new)

    def test_american_english(self):
        for _s, _p, _f, _o, new in C.EDITS:
            for w in BRITISH:
                self.assertIsNone(re.search(rf"\b{w}\b", new, re.I), f"{w} in {new[:60]}")

    def test_no_absolute_claim_vocabulary(self):
        for _s, _p, _f, _o, new in C.EDITS:
            self.assertIsNone(
                re.search(r"\b(?:always|never|guaranteed|completely|totally|harmless)\b",
                          new, re.I), new[:80])

    def test_registers_stay_materially_different_where_both_were_rewritten(self):
        by = {}
        for slug, pname, field, _o, new in C.EDITS:
            by.setdefault((slug, pname), {})[field] = new
        pairs = [v for v in by.values() if len(v) == 2]
        self.assertTrue(pairs, "expected at least one crop with both registers rewritten")
        for v in pairs:
            self.assertNotEqual(v["organic_treatment_beginner"], v["organic_treatment_seasoned"])


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    """REFUSAL-SPEC: each asserts check() REFUSES a bad input. Green here IS the pass."""

    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_a_missing_crop(self):
        d = _pre()
        d["crops"] = [c for c in d["crops"] if c.get("slug") != "sage"]
        self.assertIsNotNone(P.check(d))

    def test_refuses_a_missing_field(self):
        d = _pre()
        P._find(d, "basil", "Slugs and snails").pop("organic_treatment_beginner")
        self.assertIsNotNone(P.check(d))

    def test_refuses_when_the_prose_moved_under_us(self):
        d = _pre()
        p = P._find(d, "arugula", "Slugs and snails")
        p["organic_treatment_beginner"] = p["organic_treatment_beginner"].replace(
            "Hand-pick", "Handpick")
        self.assertIsNotNone(P.check(d))

    def test_refuses_a_renamed_problem(self):
        d = _pre()
        P._find(d, "bok-choy", "Slugs and snails")["name"] = "Slugs & snails"
        self.assertIsNotNone(P.check(d))

    def test_check_passes_on_the_real_base(self):
        """Positive control: the refusals above must not be passing for an unrelated reason."""
        self.assertIsNone(P.check(_pre()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
