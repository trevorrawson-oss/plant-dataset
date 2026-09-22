#!/usr/bin/env python3
"""Tests for container_citation_floor_gate -- the PLA-533 RATCHET (Trevor, 2026-09-22).

TDD: written and run RED before the module existed.

THE RULING: "the count of certified crops with a non-null container_notes.min_pot_gallons and no
sources or no anchoring URL may go DOWN, never UP. Armed at 4 today it is green and it stops the
population growing while the audit runs. Prove it by mutation: adding a fifth must fail; closing
one must pass at the lower count."

WHY THIS GATE EXISTS AT ALL, and why it is not section F. Section F asks "did you anchor what you
CITED?" -- it fires only on a NON-EMPTY sources list, so emptying `sources` makes it QUIETER, not
louder (measured: cabbage's claim-bearing leaf count drops 147 -> 146 and the gate still PASSES).
A gate that gets greener as you cite less cannot floor coverage. This one asks the other question:
"should this number have been cited?" It is a COVERAGE FLOOR, in the A57 / A59 pattern, and it is
roster-level rather than per-crop because a ratchet is a property of a COUNT.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import container_citation_floor_gate as G  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
KNOWN = ("dry-bean", "grapefruit", "green-beans-bush", "orange-navel")
# A properly cited crop, used as the donor for "break a fifth one".
CITED_VICTIM = "cabbage"


def canon():
    with open(CANON, encoding="utf-8") as f:
        return json.load(f)


def by(data):
    return {c["slug"]: c for c in data["crops"]}


class PinsAreTheRuling(unittest.TestCase):
    def test_ceiling_and_known_set_are_the_measured_four(self):
        """Enumerated as literals, never computed from the scan they bound. A ceiling derived from
        the thing it limits is vacuous -- it would 'hold' at any value."""
        self.assertEqual(G.CEILING, 4)
        self.assertEqual(tuple(sorted(G.KNOWN)), tuple(sorted(KNOWN)))
        self.assertEqual(len(G.KNOWN), G.CEILING)


class MeasuresTheLivePopulation(unittest.TestCase):
    def test_live_canonical_is_exactly_the_known_four(self):
        self.assertEqual(sorted(G.uncited(canon())), sorted(KNOWN))

    def test_live_canonical_passes(self):
        self.assertEqual(G.violations(canon()), [])

    def test_the_four_really_are_uncited_and_really_do_carry_a_figure(self):
        """Refusal-spec both ways: assert the population is what the gate says it is, from the
        data, so a gate that simply returned its own KNOWN tuple could not pass this."""
        idx = by(canon())
        for slug in KNOWN:
            cn = idx[slug]["container_notes"]
            self.assertIsNotNone(cn.get("min_pot_gallons"), slug)
            self.assertFalse(cn.get("sources") or [], slug)
            self.assertFalse(cn.get("anchoring_urls") or {}, slug)

    def test_a_cited_crop_is_not_in_the_population(self):
        idx = by(canon())
        cn = idx[CITED_VICTIM]["container_notes"]
        self.assertTrue(cn.get("sources"))
        self.assertTrue(cn.get("anchoring_urls"))
        self.assertNotIn(CITED_VICTIM, G.uncited(canon()))


class TheRatchet(unittest.TestCase):
    """Trevor's two proofs, by name."""

    def test_PROOF_adding_a_fifth_FAILS(self):
        d = canon()
        by(d)[CITED_VICTIM]["container_notes"].update({"sources": [], "anchoring_urls": {}})
        self.assertEqual(len(G.uncited(d)), 5)
        v = G.violations(d)
        self.assertTrue(v, "a fifth uncited crop must FAIL the ratchet")
        self.assertTrue(any(CITED_VICTIM in m for m in v), v)

    def test_PROOF_closing_one_PASSES_at_the_lower_count(self):
        d = canon()
        by(d)["dry-bean"]["container_notes"].update({
            "sources": ["umn_ext"],
            "anchoring_urls": {"umn_ext": {"url": "https://extension.umn.edu/x",
                                           "verified": "2026-09-22"}}})
        self.assertEqual(sorted(G.uncited(d)), sorted(s for s in KNOWN if s != "dry-bean"))
        self.assertEqual(G.violations(d), [],
                         "shrinking the population must PASS without editing the pin")

    def test_closing_ALL_FOUR_passes(self):
        d = canon()
        for slug in KNOWN:
            by(d)[slug]["container_notes"].update({
                "sources": ["umn_ext"],
                "anchoring_urls": {"umn_ext": {"url": "https://extension.umn.edu/x",
                                               "verified": "2026-09-22"}}})
        self.assertEqual(G.uncited(d), [])
        self.assertEqual(G.violations(d), [])


class SubstitutionCannotHide(unittest.TestCase):
    """A COUNT-ONLY ratchet is defeatable: close one, break another, the count is still 4 and a
    pure count check passes. The population is therefore pinned as a SET as well, so a swap is
    caught. This is a strengthening of the ruling, not a departure from it -- the ruled direction
    (down yes, up no) is preserved exactly."""

    def test_swapping_one_for_another_still_FAILS(self):
        d = canon()
        idx = by(d)
        idx["dry-bean"]["container_notes"].update({
            "sources": ["umn_ext"],
            "anchoring_urls": {"umn_ext": {"url": "https://extension.umn.edu/x",
                                           "verified": "2026-09-22"}}})
        idx[CITED_VICTIM]["container_notes"].update({"sources": [], "anchoring_urls": {}})
        self.assertEqual(len(G.uncited(d)), 4, "the driver must hold the COUNT at the ceiling")
        v = G.violations(d)
        self.assertTrue(v, "a substitution keeps the count at 4 and must still FAIL")
        self.assertTrue(any(CITED_VICTIM in m for m in v), v)


class TheCountCheckIsNarrowlyReachable(unittest.TestCase):
    """The `len(live) > CEILING` branch is NOT reachable by growth alone: with len(KNOWN) ==
    CEILING, any fifth uncited crop is necessarily outside KNOWN, so the SET check answers first.
    It is reachable on exactly one path -- a KNOWN/CEILING DESYNC, which is the editor error this
    gate's own instructions invite ("add it to KNOWN and raise CEILING in the same commit").

    Measured and driven here rather than assumed, because an unreachable guard reads as coverage
    and that is how PLA-580's duplicate-crop guard came to be removed."""

    def test_the_set_check_answers_first_on_plain_growth(self):
        d = canon()
        by(d)[CITED_VICTIM]["container_notes"].update({"sources": [], "anchoring_urls": {}})
        msgs = G.violations(d)
        self.assertTrue(any("is NOT one of" in m for m in msgs), msgs)

    def test_the_count_check_fires_on_a_KNOWN_CEILING_desync(self):
        d = canon()
        by(d)[CITED_VICTIM]["container_notes"].update({"sources": [], "anchoring_urls": {}})
        saved = G.KNOWN
        G.KNOWN = saved + (CITED_VICTIM,)          # added to KNOWN, CEILING left at 4
        try:
            msgs = G.violations(d)
            self.assertTrue(any("ratchet ceiling" in m for m in msgs), msgs)
        finally:
            G.KNOWN = saved

    def test_the_two_pins_are_in_sync_as_shipped(self):
        """The invariant that makes the above the ONLY path. If this breaks, the ceiling and the
        set are telling different stories and one of them is wrong."""
        self.assertEqual(len(G.KNOWN), G.CEILING)


class PartialCitationCounts(unittest.TestCase):
    """'no sources OR no anchoring URL' -- either half missing means uncited."""

    def test_sources_without_anchors_is_uncited(self):
        d = canon()
        by(d)[CITED_VICTIM]["container_notes"]["anchoring_urls"] = {}
        self.assertIn(CITED_VICTIM, G.uncited(d))

    def test_anchors_without_sources_is_uncited(self):
        d = canon()
        by(d)[CITED_VICTIM]["container_notes"]["sources"] = []
        self.assertIn(CITED_VICTIM, G.uncited(d))

    def test_missing_keys_entirely_is_uncited(self):
        d = canon()
        cn = by(d)[CITED_VICTIM]["container_notes"]
        cn.pop("sources", None)
        cn.pop("anchoring_urls", None)
        self.assertIn(CITED_VICTIM, G.uncited(d))


class ScopeIsNotWiderThanClaimed(unittest.TestCase):
    def test_a_null_min_pot_gallons_is_out_of_scope(self):
        """A crop that states no pot size makes no claim to cite. 8 certified crops carry an empty
        container_notes.sources with all-null numerics and are legitimately silent."""
        d = canon()
        cn = by(d)["plum"]["container_notes"]
        self.assertIsNone(cn.get("min_pot_gallons"))
        self.assertFalse(cn.get("sources") or [])
        self.assertNotIn("plum", G.uncited(d))

    def test_an_uncertified_shell_is_exempt(self):
        d = canon()
        cn = by(d)["avocado"]["container_notes"]
        cn["min_pot_gallons"] = 10
        cn["sources"] = []
        cn["anchoring_urls"] = {}
        self.assertNotIn("avocado", G.uncited(d))

    def test_giving_a_null_crop_a_figure_without_a_citation_FAILS(self):
        """The floor is live for NEW authoring, not only for today's four: a certified crop that
        gains a pot size without a citation is caught."""
        d = canon()
        by(d)["plum"]["container_notes"]["min_pot_gallons"] = 25
        self.assertIn("plum", G.uncited(d))
        self.assertTrue(G.violations(d))


class CLI(unittest.TestCase):
    def _run(self, path):
        r = subprocess.run([sys.executable, os.path.join(HERE, "container_citation_floor_gate.py"),
                            path], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def test_cli_passes_on_canonical_and_reports_the_count(self):
        rc, out = self._run(CANON)
        self.assertEqual(rc, 0, out)
        self.assertIn("4", out)
        for slug in KNOWN:
            self.assertIn(slug, out)

    def test_cli_fails_on_a_fifth(self):
        d = canon()
        by(d)[CITED_VICTIM]["container_notes"].update({"sources": [], "anchoring_urls": {}})
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(d, f, separators=(",", ":"))
        try:
            rc, out = self._run(f.name)
            self.assertNotEqual(rc, 0, out)
            self.assertIn(CITED_VICTIM, out)
        finally:
            os.remove(f.name)


if __name__ == "__main__":
    unittest.main()
