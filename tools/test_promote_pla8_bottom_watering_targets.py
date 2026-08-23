#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_bottom_watering_targets.py. Base d04b868c.

REPLAY-PINNED: `pre` is rebuilt from the pinned base, `post` is the promote's OWN output. No RED
phase is claimed; the evidence is Reachability plus tools/mutate_pla8_bw_suite.py.

THE RISK HERE IS NOT BREAKAGE. A widening only enlarges what the gate ACCEPTS, so it cannot redden
anything. The risk is authoring a rung the biology does not support, so the load-bearing guards are
the SCOPE ones: exactly two targets, exactly the two that were graded and sourced, and NONE of the
five that were refused as tolerance-not-control. Those refusals are pinned as literals because they
are a judgment that a later pass could quietly reverse by "finishing the job".
"""
import copy
import hashlib
import json
import os
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

import promote_fixture  # noqa: E402
import promote_pla8_bottom_watering_targets as P  # noqa: E402

POST_SHA = "d19abe601ab6c67dbf4037f982307ec26a73f921f70334187dc1ed7fd97954f8"

ADDED = {"bacterial", "mollusk"}
NEW_SOURCE = "ucanr_ext_bacterial_speck"
# The five graded REFUSALS. Each is tolerance-or-wrong-target, not a control this method delivers.
# Pinned so a later pass cannot quietly "finish the job" without re-arguing the biology.
REFUSED = [("even_watering", "insect"), ("even_watering", "nematode"),
           ("straw_mulch", "nematode"), ("airflow_spacing", "insect"),
           ("beneficial_predators", "viral")]


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class Fixture(unittest.TestCase):
    def test_base_reconstructs(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_post_sha_is_pinned(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_output_is_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)


class Reachability(unittest.TestCase):
    def test_the_base_lacked_both_targets(self):
        a = _pre()["control_methods"][P.METHOD]["applies_to"]
        for t in ADDED:
            self.assertNotIn(t, a, f"base already had {t}")

    def test_the_base_lacked_the_new_source(self):
        self.assertNotIn(NEW_SOURCE, _pre()["source_catalog"])

    def test_both_targets_land(self):
        a = _post()["control_methods"][P.METHOD]["applies_to"]
        for t in ADDED:
            self.assertIn(t, a)


class Scope(unittest.TestCase):
    def test_exactly_two_targets_added_and_nothing_removed(self):
        a = _pre()["control_methods"][P.METHOD]["applies_to"]
        b = _post()["control_methods"][P.METHOD]["applies_to"]
        self.assertEqual(set(b) - set(a), ADDED)
        self.assertEqual(set(a) - set(b), set(), "an existing target was removed")

    def test_the_five_refused_widenings_did_NOT_happen(self):
        """Tolerance is not control. If a later pass wants these, it must re-argue the biology."""
        cm = _post()["control_methods"]
        for method, target in REFUSED:
            self.assertNotIn(target, cm[method]["applies_to"],
                             f"{method} gained {target}, which was graded REFUSED")

    def test_only_bottom_watering_changed(self):
        a, b = _pre(), None
        b = _post(a)
        changed = {k for k in a["control_methods"]
                   if a["control_methods"][k] != b["control_methods"][k]}
        self.assertEqual(changed, {P.METHOD})

    def test_no_crop_is_touched(self):
        a = _pre()
        b = _post(a)
        self.assertEqual(a["crops"], b["crops"])

    def test_every_other_top_level_key_untouched(self):
        a = _pre()
        b = _post(a)
        self.assertEqual(set(a), set(b))
        for k in a:
            if k not in ("control_methods", "source_catalog"):
                self.assertEqual(a[k], b[k], k)

    def test_no_existing_source_entry_changed(self):
        a = _pre()
        b = _post(a)
        for k in a["source_catalog"]:
            self.assertEqual(a["source_catalog"][k], b["source_catalog"][k], k)


class Sourcing(unittest.TestCase):
    def test_each_added_target_has_its_own_anchor(self):
        m = _post()["control_methods"][P.METHOD]
        for target, src in P.ADD_TARGETS.items():
            self.assertIn(src, m["sources"], f"{target} has no anchor source")
            self.assertIn(src, m["anchoring_urls"])

    def test_the_correction_ADDS_sources_and_never_replaces(self):
        a = _pre()["control_methods"][P.METHOD]["sources"]
        b = _post()["control_methods"][P.METHOD]["sources"]
        self.assertEqual(b[:len(a)], a, "an existing source was displaced")
        self.assertGreater(len(b), len(a))

    def test_new_source_is_T1_and_titled_from_the_document(self):
        e = _post()["source_catalog"][NEW_SOURCE]
        self.assertEqual(e["tier"], "T1")
        self.assertTrue(e.get("title"))
        self.assertIn("Bacterial Speck", e["title"])
        self.assertTrue(e.get("_admission_provenance"))

    def test_the_mollusk_anchor_reuses_the_already_catalogued_source(self):
        """The snails note was minted by the previous promote; re-minting it would duplicate."""
        self.assertEqual(P.ADD_TARGETS["mollusk"], "ucanr_ext_snails_slugs")
        self.assertIn("ucanr_ext_snails_slugs", _pre()["source_catalog"])

    def test_anchoring_urls_match_sources_exactly(self):
        m = _post()["control_methods"][P.METHOD]
        self.assertEqual(set(m["anchoring_urls"]), set(m["sources"]))


class Refusals(unittest.TestCase):
    def test_refuses_a_no_op_target(self):
        pre = _pre()
        pre["control_methods"][P.METHOD]["applies_to"].append("bacterial")
        self.assertIn("no-op", P.check(pre))

    def test_refuses_when_the_source_already_exists(self):
        pre = _pre()
        pre["source_catalog"][NEW_SOURCE] = {"tier": "T1"}
        self.assertIn("already exists", P.check(pre))

    def test_refuses_a_missing_method(self):
        pre = _pre()
        del pre["control_methods"][P.METHOD]
        self.assertIn("nothing to correct", P.check(pre))

    def test_clean_base_is_accepted(self):
        self.assertIsNone(P.check(_pre()))


class GateEffect(unittest.TestCase):
    def test_the_widening_makes_the_blocked_pairings_legal(self):
        """The whole point: two controls the crops' own prose names become authorable."""
        sys.path.insert(0, os.path.join(REPO, "tools"))
        from control_ladder_gate import TYPE_TARGETS
        post = _post()
        a = set(post["control_methods"][P.METHOD]["applies_to"])
        for t in ("bacterial", "mollusk"):
            self.assertTrue(a & TYPE_TARGETS[t], f"{P.METHOD} still illegal on {t}")

    def test_it_was_illegal_before(self):
        from control_ladder_gate import TYPE_TARGETS
        pre = _pre()
        a = set(pre["control_methods"][P.METHOD]["applies_to"])
        for t in ("bacterial", "mollusk"):
            self.assertFalse(a & TYPE_TARGETS[t], f"{P.METHOD} was already legal on {t}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
