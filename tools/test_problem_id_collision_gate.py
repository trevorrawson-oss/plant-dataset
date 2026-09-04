#!/usr/bin/env python3
"""Guard suite for tools/problem_id_collision_gate.py (PLA-449).

Pinned to canonical a9c84847 (PLA-8 batch 24, the alliums). The audit-mode fixture is an EXACT
pin, not a floor: PLA-449 rules that materially fewer findings means the check is too narrow and
materially more means it floods, so both directions have to fail loudly. A new batch that mints a
colliding id changes the count and reddens `test_audit_output_is_exactly_pinned`, which is the
whole point -- that is the guard telling the next arc to adjudicate.

WHAT EACH TEST IS FOR, and why the obvious version of it would be vacuous:

* `test_the_eight_pla449_pairs_are_all_flagged` asserts COMPLETENESS against a constant enumerated
  from the ticket, never from the scan. A test that collected the scan's own output and compared it
  to itself would pass on an empty guard ([[guard-derived-from-what-it-checks-is-vacuous]]).
* `test_the_nine_known_good_are_flagged_RAW_then_suppressed` asserts BOTH halves. Asserting only
  that they are absent from the actionable set passes on a guard that never found them at all,
  which is the difference between a registration path and a blind spot.
* `test_registry_does_not_suppress_a_target_pair` is the anti-vacuity direction: a registry wide
  enough to hide a real duplicate is worse than no registry.
* `test_edit_distance_is_symmetric_and_bounded` exists because difflib-style asymmetry has bitten
  this repo before ([[difflib-ratio-is-asymmetric]]); Levenshtein is symmetric and the test pins
  that rather than assuming it.
* `test_normalize_collapses_only_what_it_claims` pins the normalization's REACH in both directions.
  The audit's function deletes parentheticals entirely, which is what makes `gray-mold` reachable
  AND what makes the `botryti` false positive; both are asserted so neither can drift silently.
"""
import json, os, subprocess, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import problem_id_collision_gate as G  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
PINNED_SHA = "ce98b0a6f83cc04b380a6c3be3009709a7c6c3626b2611c88fafec1164997144"

# ---------------------------------------------------------------------------------------------
# The PLA-449 fixture, transcribed from the ticket. NEVER computed from a scan.
# ---------------------------------------------------------------------------------------------
# The eight duplicate-id decisions. Written as the ID SETS the ticket names, so the slug family's
# three ids stay one decision rather than becoming three unrelated rows.
THE_EIGHT = [
    ("cutworm", "cutworms"),
    ("flea-beetle", "flea-beetles"),
    ("japanese-beetle", "japanese-beetles"),
    ("bacterial-leaf-spot", "bacterial-spot"),
    ("gray-mold", "botrytis-gray-mold"),
    ("two-spotted-spider-mite", "twospotted-spider-mite"),
    ("bacterial-blight", "bacterial-blights"),
    ("slugs", "slugs-and-snails", "snails-and-slugs"),
]

# The nine deliberate host/pathogen scopings the guard must not leave in the actionable set.
THE_NINE_KNOWN_GOOD = [
    ("anthracnose", "cane-anthracnose"),
    ("aphids", "citrus-aphids", "apricot-aphids"),
    ("bacterial-spot", "bacterial-spot-pruni"),
    ("bacterial-wilt", "southern-bacterial-wilt"),
    ("black-rot", "sweet-potato-black-rot"),
    ("black-knot", "black-rot"),
    ("white-rot", "white-rust"),
    ("cane-blight", "late-blight"),
    ("phytophthora-foot-rot", "phytophthora-root-rot"),
]


def _pairs_of(group):
    out = set()
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            out.add(tuple(sorted((group[i], group[j]))))
    return out


def canon():
    with open(CANON) as f:
        return json.load(f)


class Preflight(unittest.TestCase):
    def test_canonical_is_the_pinned_sha(self):
        """Every count below is a snapshot of ONE dataset state. If the canonical has moved, the
        pins are stale and must be re-measured, not edited to match."""
        got = subprocess.run(["shasum", "-a", "256", CANON], capture_output=True, text=True,
                             check=True).stdout.split()[0]
        self.assertEqual(got, PINNED_SHA,
                         "canonical moved; re-measure the fixture, do not retune the pins")


class Primitives(unittest.TestCase):
    def test_edit_distance_is_symmetric_and_bounded(self):
        self.assertEqual(G.edit_distance("cutworm", "cutworms"), 1)
        self.assertEqual(G.edit_distance("cutworms", "cutworm"), 1)
        self.assertEqual(G.edit_distance("pink-root", "pink-rot"), 1)
        self.assertEqual(G.edit_distance("black-knot", "black-rot"), 2)
        # the cheap length prefilter must not report a real distance as huge
        self.assertEqual(G.edit_distance("a", "abc"), 2)
        self.assertGreater(G.edit_distance("gray-mold", "botrytis-gray-mold"), 2)

    def test_normalize_collapses_only_what_it_claims(self):
        n = G.normalize_name
        # case, plural, hyphen, ampersand, word order, parenthetical
        self.assertEqual(n("Flea beetle"), n("Flea beetles"))
        self.assertEqual(n("Slugs & snails"), n("Slugs and snails"))
        self.assertEqual(n("Snails and slugs (Cornu aspersum)"), n("Slugs and snails"))
        self.assertEqual(n("Gray mold (Botrytis cinerea)"), n("Gray mold"))
        # and what it must NOT collapse
        self.assertNotEqual(n("White rot"), n("White rust"))
        self.assertNotEqual(n("Black knot"), n("Black rot"))
        self.assertNotEqual(n("Two-spotted spider mite"), n("Twospotted spider mite"))


class Branches(unittest.TestCase):
    """Direct drivers for branches the roster does not exercise, or exercises without changing a
    finding. The mutation harness surfaced every one of these as a survivor: the guard behaved
    correctly and no test could tell. A branch nothing reaches is a latent defense
    ([[guard-reachability-must-be-measured]]), so it is pinned here rather than trusted."""

    def test_singular_keeps_double_s_words_whole(self):
        # unreachable from the current roster; pinned so it cannot rot before a crop needs it
        self.assertEqual(G.singular("grass"), "grass")
        self.assertEqual(G.singular("moss"), "moss")

    def test_singular_handles_the_ies_family(self):
        self.assertEqual(G.singular("whiteflies"), "whitefly")   # live on 5 crops
        self.assertEqual(G.singular("boxes"), "box")
        self.assertEqual(G.singular("ant"), "ant")               # <=3 chars untouched

    def test_conjuncts_of_a_name_with_no_conjunction_is_empty(self):
        self.assertEqual(G.conjuncts("Cutworms"), set())
        self.assertEqual(G.conjuncts("Slugs and snails"), {"slug", "snail"})

    def test_id_nesting_is_proper_not_reflexive(self):
        """Equal token sets are NOT nesting: `slugs-and-snails` and `snails-and-slugs` hold the
        same tokens, and check 3 must not claim one is a narrower member of the other."""
        self.assertFalse(G.id_tokens_nested("slugs-and-snails", "snails-and-slugs"))
        self.assertFalse(G.id_tokens_nested("cutworm", "cutworm"))
        self.assertTrue(G.id_tokens_nested("slugs", "slugs-and-snails"))

    def test_a_pair_found_by_two_checks_keeps_both_kinds(self):
        by = {}
        for x in G.scan(canon(), registry=None):
            by[x.pair] = x.kinds
        self.assertEqual(by[("cutworm", "cutworms")], {G.ID_NEAR_DUP, G.NAME_SHARED})


class AuditFixture(unittest.TestCase):
    """PLA-449's 'run against current data before trusting it forward'."""

    @classmethod
    def setUpClass(cls):
        cls.data = canon()
        cls.reg = G.load_registry()
        cls.findings = G.scan(cls.data, registry=cls.reg)
        cls.flagged = {f.pair for f in cls.findings}
        cls.actionable = {f.pair for f in cls.findings if not f.registered}

    def test_the_eight_pla449_pairs_are_all_flagged(self):
        missing = []
        for group in THE_EIGHT:
            want = _pairs_of(group)
            if not (want & self.actionable):
                missing.append(group)
        self.assertEqual(missing, [], "PLA-449 duplicate-id decisions the guard did not surface")

    def test_every_id_in_each_of_the_eight_is_reachable(self):
        """The slug decision names THREE ids. Surfacing two of them hands the reviewer a
        decision with a member missing."""
        for group in THE_EIGHT:
            reached = {i for p in self.actionable for i in p if i in group}
            self.assertEqual(reached, set(group),
                             "decision %r surfaced only %r" % (group, sorted(reached)))

    def test_the_nine_known_good_are_flagged_RAW_then_suppressed(self):
        raw = {f.pair for f in G.scan(self.data, registry=None)}
        for group in THE_NINE_KNOWN_GOOD:
            want = _pairs_of(group)
            self.assertTrue(want & raw,
                            "known-good %r is invisible to the raw checks, so the registration "
                            "path is not what is hiding it" % (group,))
            self.assertFalse(want & self.actionable,
                             "known-good %r survived registration" % (group,))

    def test_registry_does_not_suppress_a_target_pair(self):
        for group in THE_EIGHT:
            for p in _pairs_of(group):
                self.assertFalse(self.reg.registered(*p),
                                 "registry suppresses the real duplicate %r" % (p,))

    def test_audit_output_is_exactly_pinned(self):
        """Both directions of PLA-449's bar. Re-measure on a canonical move; never retune.

        RE-MEASURED 2026-09-04 for PLA-8 batch 25 (the herbs), 34 -> 37 raw. The delta is exactly
        the three pairs that batch introduced, all three adjudicated and REGISTERED, so registered
        went 12 -> 15 while ACTIONABLE DID NOT MOVE. That last part is the check that matters: a
        batch is allowed to add registered pairs and is not allowed to add open ones, and holding
        `actionable` at 22 across a 38-problem reshape is the assertion, not the raw total."""
        self.assertEqual(len(self.findings), 37, "raw finding count moved")
        self.assertEqual(len(self.actionable), 22, "actionable count moved")
        registered = [f for f in self.findings if f.registered]
        self.assertEqual(len(registered), 15, "registered count moved")
        for pair in (("carrot-leaf-blight", "lemongrass-leaf-blight"),
                     ("leafhoppers", "sage-leafhoppers"),
                     ("mint-rust", "oregano-rust")):
            self.assertIn(pair, self.flagged, "batch-25 pair %r stopped being flagged" % (pair,))
            self.assertTrue(self.reg.registered(*pair))
            self.assertNotIn(pair, self.actionable)

    def test_batch24_minted_the_ninth_pair(self):
        """Regression for the finding this build produced: `pink-rot` (celery) carried an id all
        along and `pink-root` was minted when batch 24 laddered the alliums, so the pair did not
        exist at the audit base 80519a28. Adjudicated distinct in PLA-448 s2, hence registered."""
        self.assertIn(("pink-root", "pink-rot"), self.flagged)
        self.assertTrue(self.reg.registered("pink-root", "pink-rot"))
        self.assertNotIn(("pink-root", "pink-rot"), self.actionable)


class BatchMode(unittest.TestCase):
    """The mode that actually runs at batch apply: only pairs touching a newly minted id."""

    def setUp(self):
        self.data = canon()

    def test_minted_mode_reports_only_pairs_touching_a_minted_id(self):
        f = G.scan(self.data, minted={"cutworm"}, registry=None)
        self.assertTrue(f)
        for x in f:
            self.assertIn("cutworm", x.pair)

    def test_minted_mode_is_a_filter_not_a_different_check(self):
        """A pair reported in minted mode must be reported in audit mode too."""
        audit = {x.pair for x in G.scan(self.data, registry=None)}
        for mid in ("cutworm", "flea-beetle", "pink-root"):
            for x in G.scan(self.data, minted={mid}, registry=None):
                self.assertIn(x.pair, audit)

    def test_a_clean_minted_id_reports_nothing(self):
        self.assertEqual(G.scan(self.data, minted={"quackgrass-rhizome-drift"}, registry=None), [])

    def test_minted_ids_absent_from_the_data_are_reported_as_check_1_ONLY(self):
        """A minted id with no record in `data` carries no display name, so checks 2 and 3 cannot
        run on it and the caller is getting a THIRD of the guard while the output looks complete.
        The gate must say so rather than return a quiet clean."""
        # FIND THE ABSENT ID BY THE PROPERTY UNDER TEST, NEVER BY NAME. This test used to hardcode
        # `mint-rust` as its example of an id not in the data. PLA-8 batch 25 minted `mint-rust`,
        # so the example silently stopped being absent and the test failed on a DATASET change
        # rather than a code change. plant-app hit the identical shape when a batch gave
        # cherry-tomato the ladder its fixture used it to lack. Any fixture naming a specific id to
        # mean "an id without X" is a tripwire waiting for the batch that gives it an X.
        live = {p.get("id") for c in self.data["crops"]
                for f in ("pests", "diseases") for p in (c.get(f) or []) if p.get("id")}
        absent = "no-such-problem-id-anywhere"
        self.assertNotIn(absent, live, "the chosen absent id is present; test would be vacuous")
        present = sorted(live)[0]
        partial = G.checks_unavailable_for(self.data, {absent, present})
        self.assertEqual(partial, [absent])
        self.assertEqual(G.checks_unavailable_for(self.data, {present}), [])

    def test_minted_mode_catches_an_id_not_yet_in_the_data(self):
        """The real batch case: the id is being MINTED, so it is absent from `data`."""
        f = G.scan(self.data, minted={"aphid"}, registry=None)
        self.assertIn(("aphid", "aphids"), {x.pair for x in f})


class Kinds(unittest.TestCase):
    def setUp(self):
        self.data = canon()
        self.by = {}
        for x in G.scan(self.data, registry=None):
            self.by.setdefault(x.pair, set()).update(x.kinds)

    def test_id_near_dup_fires_on_edit_distance_only(self):
        self.assertIn(G.ID_NEAR_DUP, self.by[("black-knot", "black-rot")])
        self.assertNotIn(G.NAME_SHARED, self.by[("black-knot", "black-rot")])

    def test_name_shared_fires_across_a_wide_id_distance(self):
        self.assertIn(G.NAME_SHARED, self.by[("botrytis-gray-mold", "gray-mold")])
        self.assertNotIn(G.ID_NEAR_DUP, self.by[("botrytis-gray-mold", "gray-mold")])

    def test_family_member_completes_the_slug_decision(self):
        self.assertIn(G.FAMILY_MEMBER, self.by[("slugs", "slugs-and-snails")])

    def test_family_member_never_opens_a_family_on_its_own(self):
        """Scoped by construction to ids already implicated by check 1 or check 2, so it cannot
        flood. Measured: it contributes exactly the two slug pairs on this canonical."""
        only = [p for p, k in self.by.items() if k == {G.FAMILY_MEMBER}]
        self.assertEqual(sorted(only), [("slugs", "slugs-and-snails"), ("slugs", "snails-and-slugs")])


class MicrogreenSchema(unittest.TestCase):
    """The seven microgreen crops and `microgreens-mix` carry `name_seasoned` / `name_beginner`
    and NO `name` key, so a name-keyed check is blind to them unless taught the schema. Seven of
    them are still unladdered and are a remaining PLA-8 family: when they ladder, an id like
    `damping-off-microgreens` sits edit distance 11 from `damping-off`, so check 1 would not see it
    either. Closing this before the batch, not after."""

    def setUp(self):
        self.data = canon()

    def test_display_name_falls_back_to_name_seasoned(self):
        got = G.index(self.data)[1]
        self.assertIn("Fungus gnats", got["fungus-gnats"])

    def test_a_minted_microgreen_id_reusing_a_live_name_is_caught(self):
        """The exact defect the microgreen batch would otherwise mint silently."""
        for c in self.data["crops"]:
            if c["slug"] == "arugula-microgreens":
                for e in c["diseases"]:
                    e["id"] = "damping-off-microgreens"
                    e["name_seasoned"] = "Damping-off"
        f = G.scan(self.data, minted={"damping-off-microgreens"}, registry=None)
        self.assertIn(("damping-off", "damping-off-microgreens"), {x.pair for x in f})


class Evidence(unittest.TestCase):
    def test_a_finding_carries_the_crops_that_hold_each_id(self):
        f = [x for x in G.scan(canon(), registry=None) if x.pair == ("cutworm", "cutworms")][0]
        self.assertEqual(f.crops["cutworm"], ["asparagus"])
        self.assertIn("sweet-corn", f.crops["cutworms"])
        self.assertIn("Cutworms", f.names["cutworm"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
