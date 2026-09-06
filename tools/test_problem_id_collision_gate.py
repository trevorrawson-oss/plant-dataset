#!/usr/bin/env python3
"""Guard suite for tools/problem_id_collision_gate.py (PLA-449).

Pinned to canonical 72371c02 (PLA-450 Option B: the two held pairs scoped, both generic ids vacated). The
audit-mode fixture is an EXACT
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
PINNED_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"

# ---------------------------------------------------------------------------------------------
# The PLA-449 fixture, transcribed from the ticket. NEVER computed from a scan.
# ---------------------------------------------------------------------------------------------
# The eight duplicate-id decisions PLA-449 was built to surface, as they stand after PLA-450/451
# (2026-09-05). SIX were merged: the minority id no longer exists anywhere, so the pair is gone
# from the scan for the right reason, and the test proves the ABSENCE of the minority id rather
# than the absence of the pair. TWO were HELD, not merged, because the entries' own cause prose
# names different pathogens (cilantro Pseudomonas syringae pv. coriandricola vs pepper
# Xanthomonas; edamame P. savastanoi pv. glycinea vs bean X. campestris pv. phaseoli + P. syringae
# pv. phaseolicola), and then RULED (Trevor, PLA-450 Option B, 2026-09-05): the generic id was
# scoped to its single holder and VACATED, and the scoped id registered against the id it diverges
# from. Written as (minority ids..., majority id) / (vacated generic, scoped id, diverges from).
THE_SIX_MERGED = [
    (("cutworm",), "cutworms"),
    (("flea-beetle",), "flea-beetles"),
    (("japanese-beetle",), "japanese-beetles"),
    (("botrytis-gray-mold",), "gray-mold"),
    (("twospotted-spider-mite",), "two-spotted-spider-mite"),
    (("slugs", "snails-and-slugs"), "slugs-and-snails"),
]
THE_TWO_SCOPED = [
    ("bacterial-leaf-spot", "cilantro-bacterial-leaf-spot", "cilantro-coriander", "bacterial-spot"),
    ("bacterial-blight", "edamame-bacterial-blight", "edamame", "bacterial-blights"),
]
# The celery split (PLA-451): two minted ids that collide on NAME_SHARED with the generic id they
# left, adjudicated in the registry. Flagged RAW then suppressed, exactly like the nine known-good.
THE_CELERY_SPLIT = [
    ("celery-early-blight", "early-blight"),
    ("celery-late-blight", "late-blight"),
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


def live_ids(data):
    return {p.get("id") for c in data["crops"] for f in ("pests", "diseases")
            for p in (c.get(f) or []) if p.get("id")}


def with_slug_family_restored(data):
    """The pre-PLA-450 slug family, rebuilt by two id writes on a scratch copy: strawberry back on
    `slugs`, artichoke back on `snails-and-slugs`. Check 3 (FAMILY_MEMBER) has no live exercise
    left on canonical since the merge retired both minority ids, and a branch nothing reaches is a
    latent defense, so the family is reconstructed here rather than trusted."""
    for c in data["crops"]:
        if c["slug"] == "strawberry":
            for e in c["pests"]:
                if e.get("name") == "Slugs":
                    e["id"] = "slugs"
        if c["slug"] == "artichoke":
            for e in c["pests"]:
                if e.get("id") == "slugs-and-snails":
                    e["id"] = "snails-and-slugs"
    return data


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
        # the birds family: found by check 3 AND check 2, both kinds kept. (The earlier example,
        # bacterial-blight / bacterial-blights, was resolved by PLA-450 Option B.)
        self.assertEqual(by[("birds", "birds-and-squirrels")], {G.FAMILY_MEMBER, G.NAME_SHARED})


class AuditFixture(unittest.TestCase):
    """PLA-449's 'run against current data before trusting it forward'."""

    @classmethod
    def setUpClass(cls):
        cls.data = canon()
        cls.reg = G.load_registry()
        cls.findings = G.scan(cls.data, registry=cls.reg)
        cls.flagged = {f.pair for f in cls.findings}
        cls.actionable = {f.pair for f in cls.findings if not f.registered}

    def test_the_six_merged_decisions_are_resolved_for_the_right_reason(self):
        """A pair can vanish from the scan because the duplicate was merged OR because the guard
        went blind. Only the first is a pass, so this asserts the MINORITY ID IS GONE from the
        dataset and the majority id is still there -- never merely that the pair is absent."""
        live = live_ids(self.data)
        for minority, majority in THE_SIX_MERGED:
            for m in minority:
                self.assertNotIn(m, live, "retired id %r is still carried somewhere" % m)
                self.assertFalse(any(m in p for p in self.actionable),
                                 "retired id %r still appears in an OPEN pair" % m)
            self.assertIn(majority, live)

    def test_the_two_scoped_decisions_vacated_the_generic_and_registered_the_scoped(self):
        """Option B, both halves. The generic id must be GONE from the dataset (not merely absent
        from a pair), the scoped id must live on exactly its crop, and the scoped id's collision
        with the id it diverges from must be flagged RAW and then suppressed by the registry."""
        live = live_ids(self.data)
        raw = {f.pair: f for f in G.scan(self.data, registry=None)}
        holders = G.index(self.data)[0]
        for generic, scoped, crop, diverges in THE_TWO_SCOPED:
            self.assertNotIn(generic, live, "vacated generic %r is still carried" % generic)
            self.assertEqual(holders[scoped], {crop})
            key = tuple(sorted((scoped, diverges)))
            self.assertIn(key, raw, "scoped pair %r is invisible to the raw checks" % (key,))
            self.assertEqual(raw[key].kinds, {G.NAME_SHARED})
            self.assertNotIn(key, self.actionable, "scoped pair %r survived registration" % (key,))
            self.assertTrue(self.reg.registered(scoped, diverges))

    def test_the_celery_split_is_flagged_RAW_then_suppressed(self):
        raw = {f.pair: f for f in G.scan(self.data, registry=None)}
        for pair in THE_CELERY_SPLIT:
            key = tuple(sorted(pair))
            self.assertIn(key, raw, "celery pair %r is invisible to the raw checks" % (pair,))
            self.assertIn(G.NAME_SHARED, raw[key].kinds)
            self.assertNotIn(key, self.actionable, "celery pair %r survived registration" % (pair,))
            self.assertTrue(self.reg.registered(*pair))

    def test_the_nine_known_good_are_flagged_RAW_then_suppressed(self):
        raw = {f.pair for f in G.scan(self.data, registry=None)}
        for group in THE_NINE_KNOWN_GOOD:
            want = _pairs_of(group)
            self.assertTrue(want & raw,
                            "known-good %r is invisible to the raw checks, so the registration "
                            "path is not what is hiding it" % (group,))
            self.assertFalse(want & self.actionable,
                             "known-good %r survived registration" % (group,))

    def test_registry_names_no_vacated_id(self):
        """A registry naming a dead id is a stale record. The batch-26 mulberry entry that named
        edamame's old generic id was repointed to the scoped id, and that moved pair must still
        be registered."""
        for generic, scoped, _, _ in THE_TWO_SCOPED:
            for e in self.reg.entries:
                self.assertNotIn(generic, e["ids"], "registry entry %r names vacated %r" % (e["ids"], generic))
        self.assertTrue(self.reg.registered("edamame-bacterial-blight", "mulberry-bacterial-blight"))

    def test_audit_output_is_exactly_pinned(self):
        """Both directions of PLA-449's bar. Re-measure on a canonical move; never retune.

        RE-MEASURED 2026-09-05, ce98b0a6 -> 95e66f6d, 37 -> 42 raw. The delta is exactly the five
        pairs PLA-8 batch 26 (the trees and shrubs) introduced, every one adjudicated in
        problem_id_registry.json with a documented reason ruled "PLA-8 batch 26 (2026-09-04)", so
        registered went 15 -> 20 while ACTIONABLE DID NOT MOVE. Batch 27 (the microgreens) minted
        ZERO ids and contributed ZERO pairs: measured at ba61762a, raw was already 42.

        That last part is the check that matters: a batch is allowed to add registered pairs and is
        not allowed to add open ones, and holding `actionable` at 22 across batches 25, 26 and 27 is
        the assertion, not the raw total.

        The suite reddened at batch 26 and stayed red through batch 27 because those batches
        registered their pairs without re-measuring here. That is the pin working -- it refuses to
        certify a count it did not measure -- but it is also two revisions of the guard not running.
        RE-MEASURE THIS WHENEVER CANONICAL MOVES; never retune a count to make it green.

        RE-MEASURED 2026-09-05, 95e66f6d -> 36d6df6b, 42 -> 36 raw. THE FIRST MOVE OF `actionable`,
        and the first one PREDICTED BEFORE THE RUN (PLA-450's addendum): the promote pinned
        36 / 22 / 14 from the 42-pair list before it was first executed and refuses any other
        figure. Eight OPEN pairs retired because their minority id ceased to exist (five two-id
        merges plus the three-pair slug family); the two celery mints each added one NAME_SHARED
        pair, both registered. Net raw -8 +2, registered +2, actionable -8. The two HELD pairs
        (cilantro/pepper, edamame/bean) are still in the 14 on purpose.

        RE-MEASURED 2026-09-05, 36d6df6b -> 72371c02, raw 36 -> 36, registered 22 -> 24,
        actionable 14 -> 12. PLA-450 Option B (Trevor's ruling): the two held pairs resolved by
        SCOPING the generic id to its single holder, so `bacterial-leaf-spot` and
        `bacterial-blight` exist nowhere. Predicted before the run and matched: each scoped id
        retires its OPEN pair and adds one registered NAME_SHARED pair against the id it diverges
        from; the edamame id also retires the registered mulberry pair with the dead id, re-creates
        it under the new id via the repointed registry entry, and adds a second NAME_SHARED pair
        with mulberry because 'bacterial blight' now has three owners. Raw does not move at all.
        The 12 that remain are the residue decisions of the PLA-449 handoff, section 4."""
        self.assertEqual(len(self.findings), 36, "raw finding count moved")
        self.assertEqual(len(self.actionable), 12, "actionable count moved")
        registered = [f for f in self.findings if f.registered]
        self.assertEqual(len(registered), 24, "registered count moved")
        # batch 25's three, batch 26's five, PLA-451's two, then Option B's three: FLAGGED,
        # REGISTERED, not open.
        for pair in (("bacterial-spot", "cilantro-bacterial-leaf-spot"),
                     ("bacterial-blights", "edamame-bacterial-blight"),
                     ("edamame-bacterial-blight", "mulberry-bacterial-blight"),
                     ("celery-early-blight", "early-blight"),
                     ("celery-late-blight", "late-blight"),
                     ("carrot-leaf-blight", "lemongrass-leaf-blight"),
                     ("leafhoppers", "sage-leafhoppers"),
                     ("mint-rust", "oregano-rust"),
                     ("bacterial-blights", "mulberry-bacterial-blight"),
                     ("cherry-borers", "mulberry-borers"),
                     ("lavender-leaf-spot", "persimmon-leaf-spot"),
                     ("lavender-root-crown-rot", "phytophthora-root-rot")):
            self.assertIn(pair, self.flagged, "registered pair %r stopped being flagged" % (pair,))
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
        # `cutworm` was RETIRED by PLA-450, so this is now a re-mint probe: an id absent from the
        # data, reached by check 1 alone -- exactly the batch-apply case.
        f = G.scan(self.data, minted={"cutworm"}, registry=None)
        self.assertTrue(f)
        for x in f:
            self.assertIn("cutworm", x.pair)

    def test_minted_mode_is_a_filter_not_a_different_check(self):
        """A pair reported in minted mode must be reported in audit mode too."""
        audit = {x.pair for x in G.scan(self.data, registry=None)}
        for mid in ("pink-root", "chives-rust", "plum-aphids"):   # all still live after PLA-450
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
        """The celery split is the live example: edit distance 7, one normalized name."""
        self.assertIn(G.NAME_SHARED, self.by[("celery-early-blight", "early-blight")])
        self.assertNotIn(G.ID_NEAR_DUP, self.by[("celery-early-blight", "early-blight")])

    def test_family_member_completes_the_slug_decision(self):
        """Reconstructed: PLA-450 retired both slug minority ids, so check 3 has no live exercise
        on canonical. The pre-merge family is rebuilt on a scratch copy and must still surface all
        three members."""
        by = {}
        for x in G.scan(with_slug_family_restored(canon()), registry=None):
            by.setdefault(x.pair, set()).update(x.kinds)
        self.assertIn(G.FAMILY_MEMBER, by[("slugs", "slugs-and-snails")])
        self.assertIn(G.FAMILY_MEMBER, by[("slugs", "snails-and-slugs")])
        self.assertIn(G.NAME_SHARED, by[("slugs-and-snails", "snails-and-slugs")])

    def test_family_member_never_opens_a_family_on_its_own(self):
        """Scoped by construction to ids already implicated by check 1 or check 2, so it cannot
        flood. Measured on 36d6df6b: it contributes NOTHING on its own (the slug family is merged);
        with the family restored it contributes exactly the two slug pairs, and nothing else."""
        only = [p for p, k in self.by.items() if k == {G.FAMILY_MEMBER}]
        self.assertEqual(only, [])
        by = {}
        for x in G.scan(with_slug_family_restored(canon()), registry=None):
            by.setdefault(x.pair, set()).update(x.kinds)
        only = [p for p, k in by.items() if k == {G.FAMILY_MEMBER}]
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
        f = [x for x in G.scan(canon(), registry=None)
             if x.pair == ("celery-early-blight", "early-blight")][0]
        self.assertEqual(f.crops["celery-early-blight"], ["celery"])
        self.assertIn("potato", f.crops["early-blight"])
        self.assertIn("Early blight (Cercospora leaf spot)", f.names["celery-early-blight"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
