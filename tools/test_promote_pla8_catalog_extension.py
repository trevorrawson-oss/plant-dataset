#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_catalog_extension.py. Base 98ea96c4.

REPLAY-PINNED, so there is NO RED PHASE and this suite does not claim one: `pre` is rebuilt from the
pinned base via promote_fixture and `post` is the promote's OWN output, never live canonical. The
non-vacuity evidence is the REACHABILITY family plus tools/mutate_pla8_catalog_suite.py.

WHAT IS DIFFERENT ABOUT THIS PROMOTE'S RISK. It changes only TOP-LEVEL tables, so the blast radius
runs the opposite way from the ladder-delta promote: the thing to prove is that **no crop moved at
all**. A guard that only diffed the two tables would be blind to a crop edit, which is precisely the
direction a catalog change could go wrong (a method rename silently orphaning a rung).

The sourcing claims are also load-bearing here in a way shape checks cannot see: an anchor URL that
does not match the document the prose was read from is invisible to every structural gate. So the
suite pins the URL per method and the substantive claim per source, enumerated as literals.
"""
import copy
import hashlib
import json
import os
import re
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

import promote_fixture  # noqa: E402
import promote_pla8_catalog_extension as P  # noqa: E402

POST_SHA = "d04b868c94e45aa7c08dd4de7768040c0462b268f2e9c99eddaf9e6e75beef17"

# ENUMERATED, never derived from the content module -- a guard that recomputes its expectation from
# the thing under test cannot fail.
NEW_METHODS = ("soil_solarization", "improve_drainage", "reflective_mulch")
NEW_SOURCES = ("ucanr_ext_spider_mites", "ucanr_ext_snails_slugs")
CORRECTIONS = {"water_spray": "mite", "insecticidal_soap": "mite",
               "even_watering": "mite", "handpick": "mollusk"}
# The document each method's prose was actually read from. A wrong URL here is invisible to
# every structural gate in the repo.
ANCHOR = {
    "soil_solarization": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn74145.html",
    "improve_drainage": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn74133.html",
    "reflective_mulch": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html",
}
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
REQ = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
       "best_use", "pros", "cons", "sources", "anchoring_urls")


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _leaves(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _leaves(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _leaves(v, f"{path}[{i}]")
    else:
        yield path, o


def _new_strings():
    _, nm, _ = P.content()
    out = []
    for k, m in nm.items():
        for f, v in m.items():
            if f == "name":
                continue
            for t in (v if isinstance(v, list) else [v] if isinstance(v, str) else []):
                out.append((f"{k}.{f}", t))
    return out


class Fixture(unittest.TestCase):
    def test_base_reconstructs_to_the_pinned_sha(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_post_serializes_to_the_pinned_post_sha(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_output_is_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)


class Reachability(unittest.TestCase):
    def test_the_base_lacked_every_method_and_source_this_creates(self):
        pre = _pre()
        for k in NEW_METHODS:
            self.assertNotIn(k, pre["control_methods"], k)
        for k in NEW_SOURCES:
            self.assertNotIn(k, pre["source_catalog"], k)

    def test_the_base_lacked_every_correction_target(self):
        pre = _pre()
        for m, t in CORRECTIONS.items():
            self.assertNotIn(t, pre["control_methods"][m]["applies_to"], f"{m} already had {t}")

    def test_scope_is_exactly_the_enumerated_three_and_two(self):
        ns, nm, corr = P.content()
        self.assertEqual(sorted(nm), sorted(NEW_METHODS))
        self.assertEqual(sorted(ns), sorted(NEW_SOURCES))
        self.assertEqual({k: v[0] for k, v in corr.items()}, CORRECTIONS)

    def test_horticultural_oil_is_NOT_a_correction(self):
        """It already carries `mite`. A no-op correction reads as coverage it does not provide."""
        _, _, corr = P.content()
        self.assertNotIn("horticultural_oil", corr)
        self.assertIn("mite", _pre()["control_methods"]["horticultural_oil"]["applies_to"])


class BlastRadius(unittest.TestCase):
    def test_NO_CROP_IS_TOUCHED(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(pre["crops"], post["crops"], "a crop changed; this promote touches none")

    def test_leaf_additions_are_confined_to_the_two_tables(self):
        pre = _pre()
        post = _post(pre)
        a = {p for p, _ in _leaves(pre)}
        b = {p for p, _ in _leaves(post)}
        self.assertEqual(a - b, set(), "leaf paths were DROPPED")
        stray = [p for p in (b - a)
                 if not (p.startswith(".control_methods.") or p.startswith(".source_catalog."))]
        self.assertEqual(stray, [], f"added leaves outside the two tables: {stray[:5]}")

    def test_only_the_four_corrected_methods_changed_value(self):
        pre = _pre()
        post = _post(pre)
        changed = {k for k in pre["control_methods"]
                   if pre["control_methods"][k] != post["control_methods"][k]}
        self.assertEqual(changed, set(CORRECTIONS))

    def test_every_other_top_level_key_is_untouched(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(set(pre), set(post))
        for k in pre:
            if k not in ("control_methods", "source_catalog"):
                self.assertEqual(pre[k], post[k], f"top-level {k} changed")

    def test_no_existing_source_catalog_entry_changed(self):
        pre = _pre()
        post = _post(pre)
        for k in pre["source_catalog"]:
            self.assertEqual(pre["source_catalog"][k], post["source_catalog"][k], k)


class CatalogShape(unittest.TestCase):
    def test_new_methods_carry_every_required_key(self):
        post = _post()
        for k in NEW_METHODS:
            for f in REQ:
                self.assertIn(f, post["control_methods"][k], f"{k}.{f}")
                self.assertTrue(post["control_methods"][k][f], f"{k}.{f} is empty")

    def test_new_methods_use_an_existing_tier(self):
        post = _post()
        for k in NEW_METHODS:
            self.assertIn(post["control_methods"][k]["tier"], TIERS)

    def test_every_source_resolves_at_T1(self):
        post = _post()
        for k in NEW_METHODS + tuple(CORRECTIONS):
            for s in post["control_methods"][k]["sources"]:
                self.assertIn(s, post["source_catalog"], f"{k} -> {s}")
                self.assertEqual(post["source_catalog"][s]["tier"], "T1", s)

    def test_anchoring_urls_match_sources_exactly(self):
        post = _post()
        for k in NEW_METHODS + tuple(CORRECTIONS):
            m = post["control_methods"][k]
            self.assertEqual(set(m["anchoring_urls"]), set(m["sources"]), k)

    def test_each_new_method_points_at_the_document_it_was_read_from(self):
        """A wrong anchor URL is invisible to every structural gate in this repo."""
        post = _post()
        for k, url in ANCHOR.items():
            self.assertEqual(post["control_methods"][k]["anchoring_urls"]["ucanr_ext"]["url"], url)

    def test_new_sources_are_titled_from_the_document(self):
        """A54: a document-scoped id must carry a title read off the document, not inferred."""
        post = _post()
        for k in NEW_SOURCES:
            e = post["source_catalog"][k]
            self.assertTrue(e.get("title"), f"{k} has no title")
            self.assertIn("UC IPM", e["title"], k)
            self.assertTrue(e.get("_admission_provenance"), f"{k} has no admission provenance")

    def test_a_correction_ADDS_a_source_and_never_replaces_one(self):
        pre, post = _pre(), None
        post = _post(pre)
        for k in CORRECTIONS:
            before = pre["control_methods"][k]["sources"]
            after = post["control_methods"][k]["sources"]
            self.assertEqual(after[:len(before)], before, f"{k}: an existing source was displaced")
            self.assertGreater(len(after), len(before), f"{k}: no source was added")


class Sourcing(unittest.TestCase):
    def test_the_solarization_nematode_hedge_survives_into_cons(self):
        """Two UC IPM notes bound this claim. A hedge dropped in compression has no term to scan
        for, so it is pinned here explicitly."""
        cons = " ".join(_post()["control_methods"]["soil_solarization"]["cons"]).lower()
        self.assertIn("less effective on nematodes", cons)
        self.assertIn("deeper", cons)
        self.assertTrue("about a year" in cons or "top foot" in cons)

    def test_reflective_mulch_keeps_the_small_plant_scope(self):
        """The source's benefit is documented on seedlings and small plants; the prose must not
        imply it protects a mature planting."""
        m = _post()["control_methods"]["reflective_mulch"]
        blob = (m["how_it_works_beginner"] + " " + m["how_it_works_seasoned"] + " "
                + " ".join(m["cons"])).lower()
        self.assertTrue("small plant" in blob or "seedling" in blob or "while plants are small"
                        in blob)

    def test_solarization_is_the_first_method_to_target_nematode(self):
        pre, post = _pre(), _post()
        self.assertEqual([k for k, v in pre["control_methods"].items()
                          if "nematode" in v["applies_to"]], [])
        self.assertIn("soil_solarization",
                      [k for k, v in post["control_methods"].items()
                       if "nematode" in v["applies_to"]])

    def test_reflective_mulch_is_the_first_method_to_target_viral(self):
        pre, post = _pre(), _post()
        self.assertEqual([k for k, v in pre["control_methods"].items()
                          if "viral" in v["applies_to"]], [])
        self.assertIn("reflective_mulch",
                      [k for k, v in post["control_methods"].items()
                       if "viral" in v["applies_to"]])


class Refusals(unittest.TestCase):
    def test_refuses_a_method_that_already_exists(self):
        """ISOLATED. The first version ran a full apply_to then asserted the substring
        "already exists" -- which the SOURCE already-exists check also produces, so the guard
        passed while the method check was disabled. The mutation harness caught it. Adding only
        the method leaves the source checks satisfied, so the method check is what fires."""
        pre = _pre()
        _, nm, _ = P.content()
        pre["control_methods"]["soil_solarization"] = copy.deepcopy(nm["soil_solarization"])
        msg = P.check(pre)
        self.assertIn("control_methods.soil_solarization already exists", msg)
        self.assertNotIn("source_catalog", msg, "an earlier check fired; the guard is masked")

    def test_refuses_a_no_op_correction(self):
        pre = _pre()
        pre["control_methods"]["water_spray"]["applies_to"].append("mite")
        self.assertIn("no-op", P.check(pre))

    def test_refuses_a_missing_correction_target(self):
        pre = _pre()
        del pre["control_methods"]["handpick"]
        self.assertIn("nothing to correct", P.check(pre))

    def test_clean_base_is_accepted(self):
        self.assertIsNone(P.check(_pre()))


class Mechanics(unittest.TestCase):
    def test_no_em_dash_en_dash_or_double_hyphen(self):
        for where, t in _new_strings():
            for bad in ("—", "–", "--"):
                self.assertNotIn(bad, t, where)

    def test_american_english(self):
        bad = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
               "mould", "grey", "labour", "practise")
        for where, t in _new_strings():
            for w in bad:
                self.assertIsNone(re.search(rf"\b{w}\b", t, re.I), f"{where}: {w}")

    def test_temperatures_are_unspaced_degF(self):
        for where, t in _new_strings():
            self.assertIsNone(re.search(r"\s°F", t), where)
            self.assertIsNone(re.search(r"\b\d{2,3}\s*degrees\b", t, re.I), where)

    def test_registers_are_materially_different(self):
        import difflib
        post = _post()
        for k in NEW_METHODS:
            m = post["control_methods"][k]
            r = difflib.SequenceMatcher(None, m["how_it_works_beginner"].lower(),
                                        m["how_it_works_seasoned"].lower()).ratio()
            self.assertLess(r, 0.85, f"{k}: registers are near-verbatim ({r:.3f})")


if __name__ == "__main__":
    unittest.main(verbosity=2)
