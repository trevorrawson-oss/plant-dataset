#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch18.py. Base 2cde361b (the ant_exclusion mint, a commit).

REPLAY-PINNED; no RED phase is claimed. A replay-pinned suite is green from birth, so the evidence
that these guards are LIVE is `VerifyPostIsDriven` plus the mutation harness
(tools/mutate_pla8_batch18_suite.py), NOT the fact that this file passes.

Every driver asserts the ONE message its branch emits. `assertRaises(SystemExit)` alone would let a
sabotage be caught by an EARLIER check and still report a pass for the wrong reason.

THREE THINGS THIS SUITE DOES THAT BATCH 17's DID NOT:

* `SootyMold` drives the guard the batch exists for. `sooty-mold` shipped `control_ladder: null` on
  base 2a9d3c85 and only became ladderable when `ant_exclusion` was minted; all four of its refusal
  branches plus its anti-vacuity branch are driven separately.
* `TypeTransition` drives a TWO-SIDED rule. Citrus `type` is MIXED (21 of 24 problems already carry
  a fine type, 3 are coarse), so the preservation half -- an already-fine type is never rewritten --
  needs its own driver, and the pinned-upgrade SET needs one that does not trip the per-problem
  loop on the way.
* `CatalogUntouchedInMain` reaches the two guards that live in `main()` rather than in `check()`.
  Comparing serializations from the suite, as batch 17 did, tests the OUTCOME without ever driving
  the promote's own refusal; those two branches were unreachable by that shape of test.
"""
import copy, hashlib, json, os, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch18 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

# FROZEN LITERALS -- restated here, never imported from P. A suite that reads its expectations from
# the module under test grades that module against itself.
CROPS = ("lemon", "lime")
TOTAL_RUNGS = 78
TOTAL_PROBLEMS = 24
POST_SHA = "514903dbaa59fa66d550fc88525d56dcdfe7150398f6f639e5b5905f1ddf85e4"
REUSE_ANCHORS = {"mealybugs": "chamomile"}
REFUSED = ("aphids", "spider-mites", "anthracnose", "bacterial-spot")
FINE_TYPES = ("insect", "mite", "mollusk", "fungal", "bacterial", "viral", "physiological",
              "nematode", "vertebrate")
# The six ant_exclusion rungs, read one by one against the method's MEANS during the batch read.
ANT_EXCLUSION_RUNGS = {("lemon", "scale-insects"), ("lemon", "citrus-aphids"),
                       ("lemon", "mealybugs"), ("lemon", "sooty-mold"),
                       ("lime", "scale-insects"), ("lime", "mealybugs")}
MATERIAL_FREE_LADDERS = 8


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _crop(data, slug):
    return next(c for c in data["crops"] if c.get("slug") == slug)


def _prob(data, slug, pid):
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("id") == pid:
                return p
    raise AssertionError("%s/%s not found" % (slug, pid))


def _pre_prob(data, slug, name):
    """Pre-state problems carry no id yet, so they are addressed by NAME."""
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("name") == name:
                return p
    raise AssertionError("pre %s/%r not found" % (slug, name))


class _Patch:
    """Temporarily swap a module-level name on P, restoring it even on failure."""

    def __init__(self, name, value):
        self.n, self.v = name, value

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(P, self.n, self.old)
        return False


def _sprob(batch, slug, pid):
    for fam in ("pests", "diseases"):
        for p in batch[slug].get(fam) or []:
            if p.get("id") == pid:
                return p
    raise AssertionError("staged %s/%s not found" % (slug, pid))


_UNIQ = [0]


def _rung(m):
    """A syntactically clean rung. The notes carry no absolute, no temperature figure and no ladder
    vocabulary, so injecting one drives the branch under test rather than a hygiene branch."""
    _UNIQ[0] += 1
    return {"method": m, "note_beginner": "injected beginner %d" % _UNIQ[0],
            "note_seasoned": "injected seasoned %d and it differs" % _UNIQ[0]}


def _expect(case, fragment, fn):
    """Assert fn() exits with a message containing `fragment`. Asserting the MESSAGE, not merely
    that something refused, is what stops an earlier check from masking the branch under test."""
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(fragment, str(cm.exception))


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    """verify_post must actually FIRE. Without this the blast-radius guard can be vacuous and every
    other test still passes -- the defect that motivated putting this class first (batch 7)."""

    def test_bystander_edit_is_caught(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "orange-navel")["pests"][0]["id"] = "mutated-bystander"
        _expect(self, "bystander crop", lambda: P.verify_post(P.snapshot(pre), d))

    def test_addition_is_caught_not_just_mutation(self):
        """set(pre) == set(post) BEFORE value comparison. Iterating pre alone makes ADDITIONS
        invisible, which was all four PLA-162 defects."""
        pre = _pre()
        d = _post(pre)
        _crop(d, "lemon")["pests"].append({"name": "ghost-problem", "type": "insect"})
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_removal_is_caught(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "lime")["diseases"].pop()
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_undercount_is_caught(self):
        """If a crop ended up unladdered, the touched count must not still add up.

        Simulated by REVERTING one crop after a clean apply rather than by patching CROPS: patching
        it also narrows staged() and every pre-check, so the run would die upstream and never reach
        verify_post -- green for the wrong reason, the exact masking the assert-the-message rule
        exists to prevent.
        """
        pre = _pre()
        d = _post(pre)
        for fam in ("pests", "diseases"):
            src = _crop(pre, "lemon").get(fam) or []
            dst = _crop(d, "lemon").get(fam) or []
            for s, t in zip(src, dst):
                t["id"] = s.get("id")
                t["type"] = s.get("type")
                t.pop("control_ladder", None)
        _expect(self, "problems changed, expected", lambda: P.verify_post(P.snapshot(pre), d))

    def test_clean_apply_passes(self):
        """Positive control: without sabotage the guard returns the full count, so the RED results
        above are the guard firing rather than it refusing everything."""
        pre = _pre()
        self.assertEqual(P.verify_post(P.snapshot(pre), _post(pre)), TOTAL_PROBLEMS)


class Fixture(unittest.TestCase):
    def test_pre_state_matches_base_sha(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_post_is_this_promotes_own_output(self):
        """`post` is replayed from the promote, never read from live canonical -- otherwise the
        suite reddens on every future promote."""
        d = _post()
        self.assertEqual(hashlib.sha256(P.serialize(d)).hexdigest(), POST_SHA)
        self.assertEqual(P.rung_count(P.staged()), TOTAL_RUNGS)
        self.assertEqual(sum(1 for c in CROPS for _f, p in P.problems(_crop(d, c))
                             if p.get("control_ladder")), TOTAL_PROBLEMS)

    def test_base_sha_is_enforced(self):
        """The promote refuses a base it was not written against."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(b'{"crops":[]}')
            path = fh.name
        try:
            _expect(self, "base SHA", lambda: _run_main(path))
        finally:
            os.unlink(path)


# ---------------------------------------------------------------- premise
class SchemaPremise(unittest.TestCase):
    def test_missing_crop_refused(self):
        pre = _pre()
        by = P.by_slug(pre)
        del by["lime"]
        _expect(self, "not on the roster", lambda: P.check_schema_premise(by))

    def test_full_schema_required(self):
        pre = _pre()
        del _pre_prob(pre, "lemon", "Sooty mold")["organic_treatment_beginner"]
        _expect(self, "missing organic_treatment_beginner",
                lambda: P.check_schema_premise(P.by_slug(pre)))

    def test_blank_premise_field_refused(self):
        """Present-but-empty is the same defect as absent; the guard strips before testing."""
        pre = _pre()
        _pre_prob(pre, "lime", "Greasy spot")["cause_seasoned"] = "   "
        _expect(self, "missing cause_seasoned",
                lambda: P.check_schema_premise(P.by_slug(pre)))

    def test_already_laddered_refused(self):
        pre = _pre()
        _pre_prob(pre, "lemon", "Scale insects")["control_ladder"] = [_rung("garden_sanitation")]
        _expect(self, "already laddered", lambda: P.check_schema_premise(P.by_slug(pre)))


class TypeTransition(unittest.TestCase):
    """Citrus `type` is MIXED. 21 of 24 problems already carry a fine type and must be PRESERVED
    exactly; only 3 are coarse upgrades. Both halves get drivers."""

    def test_pre_state_is_mixed_not_uniformly_coarse(self):
        """The measurement the guard rests on. Batch 17 could assert a clean coarse -> fine upgrade
        because all six of its crops were coarse; this batch cannot, and asserting it would be
        false."""
        pre = _pre()
        coarse = {(c, p.get("name")) for c in CROPS for _f, p in P.problems(_crop(pre, c))
                  if p.get("type") not in FINE_TYPES}
        self.assertEqual(len(coarse), 3)
        self.assertEqual(coarse, set(P.EXPECTED_TYPE_UPGRADES))

    def test_post_state_is_fine(self):
        d = _post()
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                self.assertIn(p.get("type"), FINE_TYPES)

    def test_non_enum_type_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "greasy-spot")["type"] = "oomycete"
        _expect(self, "is not a fine type",
                lambda: P.check_type_transition(batch, P.by_slug(pre)))

    def test_silent_retype_of_an_already_fine_type_is_refused(self):
        """THE preservation half. An already-fine type rewritten changes which methods are legal on
        the problem, and no other guard would notice."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "scale-insects")["type"] = "mite"
        _expect(self, "SILENT RETYPE",
                lambda: P.check_type_transition(batch, P.by_slug(pre)))

    def test_unpinned_upgrade_is_refused(self):
        """A fourth coarse -> fine upgrade cannot ride along unnoticed."""
        pre = _pre()
        _pre_prob(pre, "lemon", "Scale insects")["type"] = "pest"
        _expect(self, "not a pinned upgrade",
                lambda: P.check_type_transition(P.staged(), P.by_slug(pre)))

    def test_pinned_upgrade_landing_elsewhere_is_refused(self):
        """The upgrade is pinned to its DESTINATION, not merely to the fact that one happened."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "citrus-mites")["type"] = "insect"
        _expect(self, "!= pinned",
                lambda: P.check_type_transition(batch, P.by_slug(pre)))

    def test_shrinking_the_coarse_set_is_refused(self):
        """Drives the SET assertion alone. Making a pinned problem's pre-state type already fine
        (and equal to its post) short-circuits the per-problem loop via `continue`, so the only
        branch left to fire is the closing set comparison. Without this driver that branch has no
        driver at all."""
        pre = _pre()
        _pre_prob(pre, "lemon", "Spider mites and citrus mites")["type"] = "mite"
        _expect(self, "the set of coarse-typed problems is",
                lambda: P.check_type_transition(P.staged(), P.by_slug(pre)))


# ---------------------------------------------------------------- ids
class Ids(unittest.TestCase):
    def test_arity_mismatch_refused(self):
        pre = _pre()
        batch = P.staged()
        batch["lime"]["diseases"].pop()
        _expect(self, "arity", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_unknown_problem_name_refused(self):
        pre = _pre()
        _pre_prob(pre, "lime", "Postbloom fruit drop")["name"] = "Some Unlisted Disease"
        _expect(self, "not in ID_CONVENTION",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_off_convention_id_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "greasy-spot")["id"] = "citrus-greasy-spot"
        _expect(self, "!= convention", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_generic_aphids_id(self):
        """The 50-crop vegetable aphid must never reach citrus: these entries name a CTV-vectoring
        complex. The convention table is patched too, or `!= convention` fires first and masks the
        refusal branch under test."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{
                "Aphids": "aphids", "Brown citrus aphid and other aphids": "aphids"})):
            _sprob(batch, "lemon", "citrus-aphids")["id"] = "aphids"
            _sprob(batch, "lime", "citrus-aphids")["id"] = "aphids"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_generic_spider_mites_id(self):
        """lemon's record names citrus red mite AND twospotted with different monitoring seasons;
        the twospotted-focused generic would lose the red mite half outright."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{
                "Spider mites and citrus mites": "spider-mites",
                "Citrus red mite and rust mites": "spider-mites"})):
            _sprob(batch, "lemon", "citrus-mites")["id"] = "spider-mites"
            _sprob(batch, "lime", "citrus-mites")["id"] = "spider-mites"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_generic_anthracnose_id(self):
        """lime carries C. gloeosporioides AND C. acutatum as separate problems; the generic id
        would merge two Colletotrichum species on one crop."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{
                "Lime anthracnose (withertip)": "anthracnose"})):
            _sprob(batch, "lime", "lime-anthracnose")["id"] = "anthracnose"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_bacterial_spot_id(self):
        """Citrus canker is Xanthomonas citri, not the peppers' Xanthomonas leaf spot."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION,
                                          **{"Citrus canker": "bacterial-spot"})):
            for c in CROPS:
                _sprob(batch, c, "citrus-canker")["id"] = "bacterial-spot"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_reuse_anchor_must_exist(self):
        """A reused id whose anchor crop lost it means the join now resolves nowhere. chamomile is
        the ONLY off-batch holder of `mealybugs`, so renaming it trips this branch."""
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "chamomile")):
            if p.get("id") == "mealybugs":
                p["id"] = "renamed-away"
        _expect(self, "resolves nowhere",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_reuse_id_present_but_anchor_lost(self):
        """Driver for the anchor branch specifically. The id must survive ELSEWHERE off-batch while
        leaving the anchor, or `resolves nowhere` fires instead and this branch is never reached."""
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "chamomile")):
            if p.get("id") == "mealybugs":
                p["id"] = "moved-off-anchor"
        _crop(pre, "strawberry")["pests"][0]["id"] = "mealybugs"
        _expect(self, "missing its anchor crop",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_new_id_already_taken_is_refused(self):
        pre = _pre()
        _crop(pre, "orange-navel")["diseases"][0]["id"] = "sooty-mold"
        _expect(self, "already exists on",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_reuse_actually_lands_on_the_anchor(self):
        d = _post()
        for pid, anchor in REUSE_ANCHORS.items():
            holders = {c["slug"] for c in d["crops"]
                       for _f, p in P.problems(c) if p.get("id") == pid}
            self.assertIn(anchor, holders, "%s lost its anchor" % pid)

    def test_refused_ids_hold_after_apply(self):
        d = _post()
        for pid in REFUSED:
            holders = {c["slug"] for c in d["crops"]
                       for _f, p in P.problems(c) if p.get("id") == pid}
            self.assertFalse(holders & set(CROPS),
                             "%s reached a citrus: %s" % (pid, holders & set(CROPS)))


# ---------------------------------------------------------------- the batch's headline guard
class SootyMold(unittest.TestCase):
    """THE guard this batch exists for. `sooty-mold` shipped `control_ladder: null` on base
    2a9d3c85 because a fungal type could name no insect method. If it is unladdered again, or has
    lost its ant_exclusion rung, the ant_exclusion mint accomplished nothing."""

    def test_unladdered_again_is_refused(self):
        batch = P.staged()
        cm = _pre()["control_methods"]
        _sprob(batch, "lemon", "sooty-mold")["control_ladder"] = []
        _expect(self, "is unladdered again",
                lambda: P.check_sooty_mold_is_laddered(batch, cm))

    def test_losing_the_ant_exclusion_rung_is_refused(self):
        """Nothing else in the catalog reaches a fungal type with an insect control, so a
        substitution here is the mint being silently undone."""
        batch = P.staged()
        cm = _pre()["control_methods"]
        _sprob(batch, "lemon", "sooty-mold")["control_ladder"][0]["method"] = "garden_sanitation"
        _expect(self, "lost its ant_exclusion rung",
                lambda: P.check_sooty_mold_is_laddered(batch, cm))

    def test_retyping_away_from_fungal_is_refused(self):
        """The mint's `disease_general` scope is what carries this rung. Retyped, the rung might
        still be legal but for a different reason than the one that was sourced."""
        batch = P.staged()
        cm = _pre()["control_methods"]
        _sprob(batch, "lemon", "sooty-mold")["type"] = "bacterial"
        _expect(self, "retyped to", lambda: P.check_sooty_mold_is_laddered(batch, cm))

    def test_guard_is_not_vacuous(self):
        """If no sooty-mold problem is in the batch the check would pass trivially, so it refuses."""
        batch = P.staged()
        cm = _pre()["control_methods"]
        _sprob(batch, "lemon", "sooty-mold")["id"] = "renamed-away"
        _expect(self, "no sooty-mold problem in the batch",
                lambda: P.check_sooty_mold_is_laddered(batch, cm))

    def test_base_without_the_mint_is_refused(self):
        """Running this batch on a base predating the mint must refuse, not emit a dangling rung."""
        batch = P.staged()
        cm = {k: v for k, v in _pre()["control_methods"].items() if k != "ant_exclusion"}
        _expect(self, "ant_exclusion is not in the catalog",
                lambda: P.check_sooty_mold_is_laddered(batch, cm))

    def test_sooty_mold_is_laddered_after_apply(self):
        """The defect this batch closes, asserted on the OUTPUT rather than on the staged file."""
        p = _prob(_post(), "lemon", "sooty-mold")
        self.assertTrue(p["control_ladder"])
        self.assertIn("ant_exclusion", [r["method"] for r in p["control_ladder"]])
        self.assertEqual(p["type"], "fungal")


class AntExclusionOrdering(unittest.TestCase):
    """The mechanism claim, asserted on the DATA. The sources say exclude ants SO THAT natural
    enemies can work, so wherever both rungs appear the exclusion must come first."""

    def test_ordering_violation_refused(self):
        batch = P.staged()
        cm = _pre()["control_methods"]
        L = _sprob(batch, "lemon", "scale-insects")["control_ladder"]
        L[0], L[1] = L[1], L[0]
        _expect(self, "puts ant_exclusion AFTER beneficial_predators",
                lambda: P.check_ant_exclusion_precedes_predators(batch, cm))

    def test_tier_change_breaking_the_ordering_is_refused(self):
        """The ordering is delivered by physical < biological, not by a hand-written string. If the
        method is ever re-tiered the guarantee is gone, so the guard asserts the tier too."""
        batch = P.staged()
        cm = copy.deepcopy(_pre()["control_methods"])
        cm["ant_exclusion"]["tier"] = "biological"
        _expect(self, "no longer physical",
                lambda: P.check_ant_exclusion_precedes_predators(batch, cm))

    def test_guard_is_not_vacuous(self):
        batch = P.staged()
        cm = _pre()["control_methods"]
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                p["control_ladder"] = [r for r in p["control_ladder"]
                                       if r["method"] != "ant_exclusion"]
        _expect(self, "no ant_exclusion rung in the batch",
                lambda: P.check_ant_exclusion_precedes_predators(batch, cm))

    def test_the_six_rungs_are_exactly_the_ones_read(self):
        """Pinned by name. Every one of these was read against the method's MEANS during the batch
        read; a seventh appearing later has not been."""
        d = _post()
        got = {(c, p["id"]) for c in CROPS for _f, p in P.problems(_crop(d, c))
               if "ant_exclusion" in [r["method"] for r in p["control_ladder"]]}
        self.assertEqual(got, ANT_EXCLUSION_RUNGS)

    def test_ordering_holds_after_apply(self):
        d = _post()
        both = 0
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                ms = [r["method"] for r in p["control_ladder"]]
                if "ant_exclusion" in ms and "beneficial_predators" in ms:
                    both += 1
                    self.assertLess(ms.index("ant_exclusion"), ms.index("beneficial_predators"),
                                    "%s/%s inverts the mechanism" % (c, p["id"]))
        self.assertEqual(both, 5)


class SharedIdDivergence(unittest.TestCase):
    """A shared id MAY carry different ladders where the RECORDS differ (this batch's ruling), but
    every such divergence is pinned by name and by the exact rung that differs. Anything else is
    the batch-17 `plum-curculio` defect: one join key carrying two shapes for the same content."""

    def test_unpermitted_divergence_refused(self):
        batch = P.staged()
        _sprob(batch, "lemon", "scale-insects")["control_ladder"].append(
            _rung("insecticidal_soap"))
        _expect(self, "diverges and is not permitted to",
                lambda: P.check_shared_id_divergence(batch))

    def test_divergence_beyond_the_permitted_rung_refused(self):
        """citrus-aphids may differ by ant_exclusion and by NOTHING ELSE."""
        batch = P.staged()
        _sprob(batch, "lemon", "citrus-aphids")["control_ladder"].insert(
            0, _rung("garden_sanitation"))
        _expect(self, "diverges by more than the permitted",
                lambda: P.check_shared_id_divergence(batch))

    def test_dead_exception_refused(self):
        """If the two ladders converge, the pin is a dead exception and must be removed rather than
        left standing as false documentation of a divergence that no longer exists."""
        batch = P.staged()
        L = _sprob(batch, "lime", "citrus-aphids")["control_ladder"]
        src = [r for r in _sprob(batch, "lemon", "citrus-aphids")["control_ladder"]
               if r["method"] == "ant_exclusion"]
        L.insert(2, copy.deepcopy(src[0]))
        _expect(self, "pinned as a PERMITTED divergence but its ladders",
                lambda: P.check_shared_id_divergence(batch))

    def test_guard_is_not_vacuous(self):
        batch = P.staged()
        for _f, p in P.problems(batch["lime"]):
            p["id"] = "lime-only-" + p["id"]
        _expect(self, "no shared ids found",
                lambda: P.check_shared_id_divergence(batch))

    def test_ten_shared_ids_and_exactly_one_diverges(self):
        """The ruling as data: ten ids are shared, nine match method-for-method, one differs."""
        d = _post()
        per = {}
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                per.setdefault(p["id"], {})[c] = [r["method"] for r in p["control_ladder"]]
        shared = {k: v for k, v in per.items() if len(v) == 2}
        self.assertEqual(len(shared), 10)
        differ = {k for k, v in shared.items() if v["lemon"] != v["lime"]}
        self.assertEqual(differ, set(P.PERMITTED_DIVERGENCE))


class TemperatureFigures(unittest.TestCase):
    """Ruled this batch: the crops say oil is unsafe above 95°F, the catalog caution says 90°F, and
    the mite entries carry no figure at all yet their rungs had imported one. No rung asserts a
    temperature, so the method's caution carries it and the stricter figure governs."""

    def test_degree_figure_refused(self):
        batch = P.staged()
        r = _sprob(batch, "lemon", "scale-insects")["control_ladder"][-1]
        r["note_seasoned"] += " Do not spray above 95°F."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_spelled_degrees_refused(self):
        """The figure carried in words rather than in the degree sign, which a °F-only scan misses.
        A handed-out RULE beats a handed-out regex; this is the pattern-evading form."""
        batch = P.staged()
        r = _sprob(batch, "lime", "citrus-mites")["control_ladder"][-1]
        r["note_beginner"] += " Hold off when it is over 90 degrees out."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_shipped_batch_carries_no_figure(self):
        P.check_no_temperature_figures(P.staged())


class LadderVocabulary(unittest.TestCase):
    """Internal vocabulary in grower-facing copy. In this batch it also took the form of
    cross-problem pointers, which is why a bare word list is the right shape here."""

    def test_rung_word_refused(self):
        batch = P.staged()
        r = _sprob(batch, "lemon", "citrus-mites")["control_ladder"][0]
        r["note_beginner"] += " Use the same limits as the scale rung."
        _expect(self, "uses internal vocabulary", lambda: P.check_no_ladder_vocabulary(batch))

    def test_ladder_word_refused(self):
        batch = P.staged()
        r = _sprob(batch, "lime", "greasy-spot")["control_ladder"][0]
        r["note_seasoned"] += " Work down this ladder in order."
        _expect(self, "uses internal vocabulary", lambda: P.check_no_ladder_vocabulary(batch))

    def test_shipped_batch_is_clean(self):
        P.check_no_ladder_vocabulary(P.staged())


# ---------------------------------------------------------------- shape
class Materials(unittest.TestCase):
    def test_material_outside_allowlist_refused(self):
        pre = _pre()
        batch = P.staged()
        # Legal for the type and no tier decrease, so the MATERIAL_OK branch is the one that fires
        # rather than an earlier check.
        _sprob(batch, "lemon", "scale-insects")["control_ladder"].append(
            _rung("insecticidal_soap"))
        _expect(self, "outside MATERIAL_OK",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_cultural_only_ladders_stay_material_free(self):
        """8 of 24 ladders carry no material rung at all; that is the short-ladder guard as data."""
        d = _post()
        free = 0
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                if not P.MATERIAL_OK.get((c, p["id"])):
                    for r in p["control_ladder"]:
                        self.assertNotIn(d["control_methods"][r["method"]]["tier"],
                                         P.MATERIAL_TIERS,
                                         "%s/%s took an unlisted material" % (c, p["id"]))
                    free += 1
        self.assertEqual(free, MATERIAL_FREE_LADDERS)


class Shape(unittest.TestCase):
    def test_unknown_method_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lime", "greasy-spot")["control_ladder"][0]["method"] = "not_a_method"
        _expect(self, "unknown method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_forbidden_method_refused(self):
        """trap_cropping IS in the catalog, so `unknown method` cannot mask this branch."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "citrus-leafminer")["control_ladder"].insert(
            0, _rung("trap_cropping"))
        _expect(self, "forbidden method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_duplicate_method_refused(self):
        pre = _pre()
        batch = P.staged()
        L = _sprob(batch, "lime", "greasy-spot")["control_ladder"]
        L.append(_rung(L[-1]["method"]))
        _expect(self, "duplicate method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_tier_decrease_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "citrus-leafminer")["control_ladder"].append(
            _rung("garden_sanitation"))
        _expect(self, "tier decrease", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_applies_to_incoherence_refused(self):
        """copper_fungicide on a MITE. The imported TYPE_TARGETS is what makes this the right
        verdict: hand-copied, `mite` lost `insect_general` and the table refused correct content
        instead."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "citrus-mites")["control_ladder"].append(_rung("copper_fungicide"))
        _expect(self, "illegal for type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_predatory_mites_stay_legal_on_a_mite(self):
        """The positive half of the same table, and the reason it is IMPORTED rather than retyped.
        Predatory mites are the natural enemy on citrus-mites; a copy with `mite: {"mite"}` would
        reject this rung, which control_ladder_gate passes."""
        pre = _pre()
        P.validate_batch(P.staged(), pre["control_methods"])
        self.assertIn("insect_general", CLG.TYPE_TARGETS["mite"])

    def test_identical_registers_refused(self):
        pre = _pre()
        batch = P.staged()
        r = _sprob(batch, "lemon", "greasy-spot")["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        _expect(self, "identical registers",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_missing_note_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lime", "huanglongbing")["control_ladder"][0]["note_beginner"] = "  "
        _expect(self, "missing note_beginner",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_empty_ladder_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "sooty-mold")["control_ladder"] = []
        _expect(self, "empty ladder", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_missing_type_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lime", "postbloom-fruit-drop")["type"] = None
        _expect(self, "missing type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_problem_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        batch["lemon"]["diseases"].pop()
        _expect(self, "problems, expected",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_per_crop_rung_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        # Removing the LAST rung avoids the duplicate-method and tier-decrease branches, so the
        # count branch is the one that actually fires.
        _sprob(batch, "lemon", "huanglongbing")["control_ladder"].pop()
        _expect(self, "rungs, expected", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_total_rung_count_pinned(self):
        """The TOTAL is a separate branch from the per-crop counts, and the per-crop check would
        mask it, so EXPECTED_RUNGS is relaxed to let the run reach it."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "huanglongbing")["control_ladder"].pop()
        with _Patch("EXPECTED_RUNGS", dict(P.EXPECTED_RUNGS, lemon=35)):
            _expect(self, "rungs total, expected",
                    lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_em_dash_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "greasy-spot")["control_ladder"][0]["note_beginner"] += " a — b"
        _expect(self, "em/en dash", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_absolute_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "lemon", "greasy-spot")["control_ladder"][0]["note_beginner"] += \
            " This never fails."
        _expect(self, "absolute", lambda: P.validate_batch(batch, pre["control_methods"]))


# ---------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_only_batch_crops_changed(self):
        pre = _pre()
        d = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(d)
        changed = {k[0] for k in a if a[k] != b[k]}
        self.assertEqual(changed, set(CROPS))

    def test_sweet_citrus_is_untouched(self):
        """Citrus was SPLIT on size. The other half must not move, or the split was not real."""
        pre = _pre()
        d = _post(pre)
        for slug in ("grapefruit", "mandarin-clementine", "orange-navel"):
            self.assertEqual(P.serialize(_crop(d, slug)), P.serialize(_crop(pre, slug)))

    def test_one_serializer(self):
        """The promote and this suite must use the SAME serializer, or an indent mutation survives
        because the suite quietly re-encodes with its own settings."""
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def _run_main(path, apply_=False):
    argv = sys.argv
    sys.argv = ["promote_pla8_batch18.py", path] + (["--apply"] if apply_ else [])
    try:
        P.main()
    finally:
        sys.argv = argv


class CatalogUntouchedInMain(unittest.TestCase):
    """Batch 18 USES the 62nd method; it does not extend the catalog. Those two refusals live in
    main() rather than in check(), so comparing serializations from the suite -- what batch 17 did
    -- asserts the OUTCOME without ever driving the promote's own guard. These reach it.
    """

    def _on_a_fixture(self, sabotage, fragment):
        raw = promote_fixture.pre_state(P.BASE_SHA)
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(raw)
        real = P.apply_to

        def wrapped(data):
            out = real(data)
            sabotage(out)
            return out
        try:
            with _Patch("apply_to", wrapped):
                _expect(self, fragment, lambda: _run_main(path))
            # The promote must not have written: this run never passed --apply.
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)

    def test_control_methods_mutation_refused(self):
        self._on_a_fixture(
            lambda d: d["control_methods"]["ant_exclusion"].__setitem__("tier", "cultural"),
            "control_methods changed")

    def test_control_methods_addition_refused(self):
        self._on_a_fixture(
            lambda d: d["control_methods"].__setitem__(
                "ghost_method", {"tier": "cultural", "applies_to": ["any"]}),
            "control_methods changed")

    def test_source_catalog_mutation_refused(self):
        self._on_a_fixture(
            lambda d: d["source_catalog"].__setitem__(
                "ghost_source", {"name": "Ghost", "title": "Ghost", "url": "https://example.edu/"}),
            "source_catalog changed")

    def test_clean_run_passes_and_writes_nothing(self):
        """Positive control. Without sabotage main() completes, so the three RED results above are
        the guards firing rather than main() refusing everything."""
        raw = promote_fixture.pre_state(P.BASE_SHA)
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(raw)
        try:
            _run_main(path)
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_post(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_gate_would_have_flagged_the_pre_state_sooty_mold(self):
        """The pre-state is clean too -- an unladdered problem is legal. That is precisely why this
        batch needed its OWN sooty-mold guard: control_ladder_gate cannot see the defect the mint
        was minted to fix."""
        self.assertEqual(CLG.all_violations(_pre()), [])
        self.assertIsNone(_pre_prob(_pre(), "lemon", "Sooty mold").get("control_ladder"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
