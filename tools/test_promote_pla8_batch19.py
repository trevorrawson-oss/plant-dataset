#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch19.py. Base 514903db (batch 18, a commit).

REPLAY-PINNED; no RED phase is claimed. A replay-pinned suite is green from birth, so the evidence
that these guards are LIVE is `VerifyPostIsDriven` plus the mutation harness
(tools/mutate_pla8_batch19_suite.py), NOT the fact that this file passes.

Every driver asserts the ONE message its branch emits. `assertRaises(SystemExit)` alone would let a
sabotage be caught by an EARLIER check and still report a pass for the wrong reason.

WHAT IS NEW HERE versus batch 18's suite:

* `CrossBatchDivergence` drives a guard that reads CANONICAL, not just the staging directory. Nine
  of this batch's ids already live on lemon or lime, so a within-batch check would pass three crops
  that silently contradict two shipped ones.
* `TypePreservation` drives the STRONG form of the type rule. All 32 problems already carry a fine
  type, so no change of any kind is permitted, and the guard also refuses if that premise breaks.
* `BrownRotTaxonSplit` and `MiteSplit` drive the two id rulings in BOTH directions, so a later pass
  cannot tidy the model by collapsing them.
* `CankerIsNotCurative` drives a STANDING ruling from batch 18, enforced roster-wide including on
  the already-shipped acid citrus.
"""
import copy, hashlib, json, os, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch19 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

# FROZEN LITERALS -- restated here, never imported from P.
CROPS = ("grapefruit", "mandarin-clementine", "orange-navel")
TOTAL_RUNGS = 108
TOTAL_PROBLEMS = 32
POST_SHA = "50bc203faddfb10f2fddb56bc0361c107efc8e3d0095b3a740c34b24d7b78ba8"
BYSTANDER = "lemon"
FINE_TYPES = ("insect", "mite", "mollusk", "fungal", "bacterial", "viral", "physiological",
              "nematode", "vertebrate")
# The four shared ids adjudicated as legitimately divergent, by reading all five records.
DIVERGENT = {"citrus-aphids", "greasy-spot", "asian-citrus-psyllid", "citrus-canker"}


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
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("name") == name:
                return p
    raise AssertionError("pre %s/%r not found" % (slug, name))


class _Patch:
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
    """A syntactically clean rung: no absolute, no temperature figure, no ladder vocabulary, so an
    injection drives the branch under test rather than a hygiene branch."""
    _UNIQ[0] += 1
    return {"method": m, "note_beginner": "injected beginner %d" % _UNIQ[0],
            "note_seasoned": "injected seasoned %d and it differs" % _UNIQ[0]}


def _expect(case, fragment, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(fragment, str(cm.exception))


def _run_main(path, apply_=False):
    argv = sys.argv
    sys.argv = ["promote_pla8_batch19.py", path] + (["--apply"] if apply_ else [])
    try:
        P.main()
    finally:
        sys.argv = argv


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    def test_bystander_edit_is_caught(self):
        """The bystander here is an ACID citrus, the crop this batch shares nine ids with. If the
        promote reached back into lemon the blast-radius guard is the only thing that would see it."""
        pre = _pre()
        d = _post(pre)
        _crop(d, BYSTANDER)["pests"][0]["id"] = "mutated-bystander"
        _expect(self, "bystander crop", lambda: P.verify_post(P.snapshot(pre), d))

    def test_addition_is_caught_not_just_mutation(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "grapefruit")["pests"].append({"name": "ghost-problem", "type": "insect"})
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_removal_is_caught(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "orange-navel")["diseases"].pop()
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_undercount_is_caught(self):
        pre = _pre()
        d = _post(pre)
        for fam in ("pests", "diseases"):
            for s, t in zip(_crop(pre, "mandarin-clementine").get(fam) or [],
                            _crop(d, "mandarin-clementine").get(fam) or []):
                t["id"] = s.get("id")
                t["type"] = s.get("type")
                t.pop("control_ladder", None)
        _expect(self, "problems changed, expected", lambda: P.verify_post(P.snapshot(pre), d))

    def test_clean_apply_passes(self):
        pre = _pre()
        self.assertEqual(P.verify_post(P.snapshot(pre), _post(pre)), TOTAL_PROBLEMS)


class Fixture(unittest.TestCase):
    def test_pre_state_matches_base_sha(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_post_is_this_promotes_own_output(self):
        d = _post()
        self.assertEqual(hashlib.sha256(P.serialize(d)).hexdigest(), POST_SHA)
        self.assertEqual(P.rung_count(P.staged()), TOTAL_RUNGS)

    def test_base_sha_is_enforced(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(b'{"crops":[]}')
        try:
            _expect(self, "base SHA", lambda: _run_main(path))
        finally:
            os.unlink(path)


# ---------------------------------------------------------------- premise
class SchemaPremise(unittest.TestCase):
    def test_missing_crop_refused(self):
        pre = _pre()
        by = P.by_slug(pre)
        del by["orange-navel"]
        _expect(self, "not on the roster", lambda: P.check_schema_premise(by))

    def test_full_schema_required(self):
        pre = _pre()
        del _pre_prob(pre, "grapefruit", "Melanose")["organic_treatment_beginner"]
        _expect(self, "missing organic_treatment_beginner",
                lambda: P.check_schema_premise(P.by_slug(pre)))

    def test_blank_premise_field_refused(self):
        pre = _pre()
        _pre_prob(pre, "orange-navel", "Brown rot of fruit")["cause_seasoned"] = "  "
        _expect(self, "missing cause_seasoned",
                lambda: P.check_schema_premise(P.by_slug(pre)))

    def test_already_laddered_refused(self):
        pre = _pre()
        _pre_prob(pre, "grapefruit", "Melanose")["control_ladder"] = [_rung("garden_sanitation")]
        _expect(self, "already laddered", lambda: P.check_schema_premise(P.by_slug(pre)))


class TypePreservation(unittest.TestCase):
    """The STRONG form. All 32 already carry a fine type, so nothing may change."""

    def test_all_32_pre_state_types_are_already_fine(self):
        """The measurement the strong rule rests on. If this ever fails, the guard below is the
        wrong guard and batch 18's two-sided version is the right one."""
        pre = _pre()
        coarse = [(c, p.get("name")) for c in CROPS for _f, p in P.problems(_crop(pre, c))
                  if p.get("type") not in FINE_TYPES]
        self.assertEqual(coarse, [])

    def test_any_type_change_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "scale-insects")["type"] = "mite"
        _expect(self, "type changed", lambda: P.check_type_preservation(batch, P.by_slug(pre)))

    def test_broken_premise_is_refused(self):
        """If a pre-state type is ever coarse, the promote must refuse rather than silently apply a
        preservation rule that was only correct for the state it was measured against."""
        pre = _pre()
        _pre_prob(pre, "orange-navel", "Katydids and fruit-surface chewers")["type"] = "pest"
        _expect(self, "is COARSE", lambda: P.check_type_preservation(P.staged(), P.by_slug(pre)))

    def test_coverage_count_is_pinned(self):
        """A guard that silently checks fewer problems than the batch contains is half a guard."""
        pre = _pre()
        batch = P.staged()
        _crop(pre, "grapefruit")["diseases"].pop()
        batch["grapefruit"]["diseases"].pop()
        _expect(self, "type check covered",
                lambda: P.check_type_preservation(batch, P.by_slug(pre)))


# ---------------------------------------------------------------- ids
class Ids(unittest.TestCase):
    def test_arity_mismatch_refused(self):
        pre = _pre()
        batch = P.staged()
        batch["orange-navel"]["pests"].pop()
        _expect(self, "arity", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_unknown_problem_name_refused(self):
        pre = _pre()
        _pre_prob(pre, "grapefruit", "Melanose")["name"] = "Some Unlisted Disease"
        _expect(self, "not in ID_CONVENTION",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_off_convention_id_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "melanose")["id"] = "diaporthe-citri"
        _expect(self, "!= convention", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_brown_rot_id(self):
        """The taxon trap, at the id layer."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{"Brown rot of fruit": "brown-rot"})):
            _sprob(batch, "orange-navel", "citrus-brown-rot")["id"] = "brown-rot"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_composite_citrus_mites_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{"Citrus rust mite": "citrus-mites"})):
            _sprob(batch, "grapefruit", "citrus-rust-mite")["id"] = "citrus-mites"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_generic_aphids_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{"Aphids": "aphids"})):
            for c in CROPS:
                _sprob(batch, c, "citrus-aphids")["id"] = "aphids"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_reuse_anchor_must_exist(self):
        """Nine ids are reused from acid citrus. If the anchor loses one the join resolves nowhere."""
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "lemon")):
            if p.get("id") == "sooty-mold":
                p["id"] = "renamed-away"
        _expect(self, "resolves nowhere", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_reuse_id_present_but_anchor_lost(self):
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "lemon")):
            if p.get("id") == "greasy-spot":
                p["id"] = "moved-off-anchor"
        _expect(self, "missing its anchor crop",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_new_id_already_taken_is_refused(self):
        """The id is APPENDED to a bystander rather than written over an existing one. Overwriting
        lemon's first disease took out `phytophthora-foot-rot`, a reuse ANCHOR, so the anchor branch
        fired first and this branch was never reached -- green for the wrong reason."""
        pre = _pre()
        _crop(pre, "apple")["diseases"].append(
            {"name": "Ghost disease", "type": "fungal", "id": "melanose"})
        _expect(self, "already exists on", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))


# ---------------------------------------------------------------- the two id rulings
class BrownRotTaxonSplit(unittest.TestCase):
    """`brown-rot` is Monilinia fructicola on six stone fruit; citrus brown rot is soil-borne
    Phytophthora. Same common name, unrelated organisms."""

    def test_citrus_taking_brown_rot_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "orange-navel", "citrus-brown-rot")["id"] = "brown-rot"
        _expect(self, "which is Monilinia on stone fruit",
                lambda: P.check_brown_rot_taxon_split(batch, pre))

    def test_guard_is_not_vacuous(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "orange-navel", "citrus-brown-rot")["id"] = "something-else"
        _expect(self, "would be vacuous", lambda: P.check_brown_rot_taxon_split(batch, pre))

    def test_guard_refuses_if_the_id_it_protects_against_is_gone(self):
        """If `brown-rot` no longer exists off-batch there is no collision to avoid, and the split
        this promote asserts is unmotivated. Refusing beats passing for the wrong reason."""
        pre = _pre()
        for c in pre["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") == "brown-rot":
                    p["id"] = "gone"
        _expect(self, "exists nowhere off-batch",
                lambda: P.check_brown_rot_taxon_split(P.staged(), pre))

    def test_brown_rot_leaking_onto_acid_citrus_is_refused(self):
        """The reachable form of the contamination check. The first cut tested
        `holders & set(CROPS)`, which could never fire because `holders` excludes CROPS by
        construction -- a dead branch that read as coverage."""
        pre = _pre()
        _prob(pre, "lemon", "greasy-spot")["id"] = "brown-rot"
        _expect(self, "already reaches an acid citrus",
                lambda: P.check_brown_rot_taxon_split(P.staged(), pre))

    def test_stone_fruit_keeps_brown_rot_after_apply(self):
        d = _post()
        holders = {c["slug"] for c in d["crops"]
                   for _f, p in P.problems(c) if p.get("id") == "brown-rot"}
        self.assertIn("peach", holders)
        self.assertFalse(holders & set(CROPS))
        self.assertEqual(_prob(d, "orange-navel", "citrus-brown-rot")["type"], "fungal")


class MiteSplit(unittest.TestCase):
    """Asserted in BOTH directions: the new species ids exist, and the acid-citrus composite
    survives untouched."""

    def test_missing_split_id_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "citrus-rust-mite")["id"] = "citrus-red-mite"
        _expect(self, "missing; the mite split", lambda: P.check_mite_split(batch, pre))

    def test_composite_reused_by_sweet_citrus_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "orange-navel", "citrus-red-mite")["id"] = "citrus-mites"
        _expect(self, "took the COMPOSITE", lambda: P.check_mite_split(batch, pre))

    def test_retro_splitting_the_composite_is_refused(self):
        """The other direction. A later pass must not tidy lemon and lime into species ids: those
        records genuinely say 'several mite species', and the id was pinned one commit ago."""
        pre = _pre()
        for s in ("lemon", "lime"):
            for _f, p in P.problems(_crop(pre, s)):
                if p.get("id") == "citrus-mites":
                    p["id"] = "citrus-red-mite"
        _expect(self, "NOT retro-split", lambda: P.check_mite_split(P.staged(), pre))


class CankerIsNotCurative(unittest.TestCase):
    """A STANDING RULING from batch 18, enforced roster-wide."""

    def test_curative_key_on_a_staged_crop_refused(self):
        pre = _pre()
        batch = P.staged()
        L = _sprob(batch, "grapefruit", "citrus-canker")["control_ladder"]
        L.insert(3, _rung("prune_out_infection"))
        _expect(self, "carries prune_out_infection",
                lambda: P.check_canker_is_not_curative(batch, pre))

    def test_shipped_acid_citrus_is_guarded_too(self):
        """The ruling can also be undone from the other side, on a crop this batch does not touch."""
        pre = _pre()
        _prob(pre, "lemon", "citrus-canker")["control_ladder"].append(_rung("prune_out_infection"))
        _expect(self, "the batch 18 ruling has been undone",
                lambda: P.check_canker_is_not_curative(P.staged(), pre))

    def test_guard_is_not_vacuous(self):
        pre = _pre()
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                if p["id"] == "citrus-canker":
                    p["id"] = "renamed"
        for s in ("lemon", "lime"):
            for _f, p in P.problems(_crop(pre, s)):
                if p.get("id") == "citrus-canker":
                    p["id"] = "renamed"
        _expect(self, "would be vacuous", lambda: P.check_canker_is_not_curative(batch, pre))


class CrossBatchDivergence(unittest.TestCase):
    """THE guard this batch exists for: it reads CANONICAL, not just the staging directory."""

    def test_unpinned_divergence_from_a_SHIPPED_crop_is_refused(self):
        """`scale-insects` is byte-identical on all five citrus. Diverging from the shipped acid
        citrus without a pin is exactly what a within-batch guard could not see."""
        batch = P.staged()
        _sprob(batch, "grapefruit", "scale-insects")["control_ladder"].append(
            _rung("insecticidal_soap"))
        _expect(self, "is not a pinned divergence",
                lambda: P.check_cross_batch_divergence(batch, _pre()))

    def test_dead_exception_refused(self):
        """If a pinned divergence CONVERGES the pin is false documentation and must be removed."""
        pre = _pre()
        batch = P.staged()
        src = [r for r in _prob(pre, "lemon", "greasy-spot")["control_ladder"]
               if r["method"] == "water_at_the_base"]
        for c in CROPS:
            _sprob(batch, c, "greasy-spot")["control_ladder"].insert(2, copy.deepcopy(src[0]))
        _expect(self, "pinned as a permitted divergence",
                lambda: P.check_cross_batch_divergence(batch, pre))

    def test_shared_id_set_is_pinned(self):
        """Driver for the SET assertion. `citrus-red-mite` is shared by two crops IN the batch, so
        the pinned set is not simply the reused-from-acid-citrus set -- the first cut of this guard
        asserted that and refused the correct batch."""
        batch = P.staged()
        _sprob(batch, "mandarin-clementine", "citrus-red-mite")["id"] = "mandarin-only-mite"
        _expect(self, "the set of multi-crop ids is",
                lambda: P.check_cross_batch_divergence(batch, _pre()))

    def test_guard_is_not_vacuous(self):
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                p["id"] = "%s-only-%s" % (c, p["id"])
        _expect(self, "no shared ids found",
                lambda: P.check_cross_batch_divergence(batch, _pre()))

    def test_exactly_the_four_adjudicated_ids_diverge_after_apply(self):
        """The rulings as data. Each of these four was settled by reading all five records."""
        d = _post()
        lad = {}
        for c in d["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") and p.get("control_ladder"):
                    lad.setdefault(p["id"], set()).add(
                        tuple(r["method"] for r in p["control_ladder"]))
        batch_ids = {p["id"] for c in CROPS for _f, p in P.problems(_crop(d, c))}
        multi = {i for i in batch_ids if len(lad.get(i, ())) > 1}
        self.assertEqual(multi, DIVERGENT)


# ---------------------------------------------------------------- copy
class TemperatureFigures(unittest.TestCase):
    def test_degree_figure_refused(self):
        batch = P.staged()
        r = _sprob(batch, "grapefruit", "scale-insects")["control_ladder"][-1]
        r["note_seasoned"] += " Do not spray above 95°F."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_spelled_degrees_refused(self):
        batch = P.staged()
        r = _sprob(batch, "orange-navel", "citrus-red-mite")["control_ladder"][-1]
        r["note_beginner"] += " Hold off when it is over 90 degrees out."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_shipped_batch_carries_no_figure(self):
        P.check_no_temperature_figures(P.staged())


class LadderVocabulary(unittest.TestCase):
    def test_rung_word_refused(self):
        batch = P.staged()
        r = _sprob(batch, "mandarin-clementine", "greasy-spot")["control_ladder"][0]
        r["note_beginner"] += " Use the same limits as the scale rung."
        _expect(self, "uses internal vocabulary", lambda: P.check_no_ladder_vocabulary(batch))

    def test_shipped_batch_is_clean(self):
        P.check_no_ladder_vocabulary(P.staged())


# ---------------------------------------------------------------- shape
class Materials(unittest.TestCase):
    def test_material_outside_allowlist_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "scale-insects")["control_ladder"].append(
            _rung("insecticidal_soap"))
        _expect(self, "outside MATERIAL_OK",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_material_free_ladders_stay_material_free(self):
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
        self.assertEqual(free, TOTAL_PROBLEMS - len(P.MATERIAL_OK))


class Shape(unittest.TestCase):
    def test_unknown_method_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "melanose")["control_ladder"][0]["method"] = "not_a_method"
        _expect(self, "unknown method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_forbidden_method_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "citrus-leafminer")["control_ladder"].insert(
            0, _rung("trap_cropping"))
        _expect(self, "forbidden method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_duplicate_method_refused(self):
        pre = _pre()
        batch = P.staged()
        L = _sprob(batch, "grapefruit", "melanose")["control_ladder"]
        L.append(_rung(L[-1]["method"]))
        _expect(self, "duplicate method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_tier_decrease_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "citrus-leafminer")["control_ladder"].append(
            _rung("garden_sanitation"))
        _expect(self, "tier decrease", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_applies_to_incoherence_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "orange-navel", "citrus-red-mite")["control_ladder"].append(
            _rung("copper_fungicide"))
        _expect(self, "illegal for type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_predatory_mites_stay_legal_on_a_mite(self):
        """The positive half of the imported table, and why it is imported rather than retyped: a
        copy with `mite: {"mite"}` would reject content control_ladder_gate passes."""
        pre = _pre()
        P.validate_batch(P.staged(), pre["control_methods"])
        self.assertIn("insect_general", CLG.TYPE_TARGETS["mite"])

    def test_identical_registers_refused(self):
        pre = _pre()
        batch = P.staged()
        r = _sprob(batch, "grapefruit", "melanose")["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        _expect(self, "identical registers",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_missing_note_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "huanglongbing")["control_ladder"][0]["note_beginner"] = " "
        _expect(self, "missing note_beginner",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_empty_ladder_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "sooty-mold")["control_ladder"] = []
        _expect(self, "empty ladder", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_missing_type_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "orange-navel", "katydids")["type"] = None
        _expect(self, "missing type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_problem_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        batch["grapefruit"]["diseases"].pop()
        _expect(self, "problems, expected",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_per_crop_rung_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "huanglongbing")["control_ladder"].pop()
        _expect(self, "rungs, expected", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_total_rung_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "huanglongbing")["control_ladder"].pop()
        with _Patch("EXPECTED_RUNGS", dict(P.EXPECTED_RUNGS, grapefruit=34)):
            _expect(self, "rungs total, expected",
                    lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_em_dash_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "melanose")["control_ladder"][0]["note_beginner"] += " a — b"
        _expect(self, "em/en dash", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_absolute_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "grapefruit", "melanose")["control_ladder"][0]["note_beginner"] += \
            " This never fails."
        _expect(self, "absolute", lambda: P.validate_batch(batch, pre["control_methods"]))


# ---------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_only_batch_crops_changed(self):
        pre = _pre()
        d = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(d)
        self.assertEqual({k[0] for k in a if a[k] != b[k]}, set(CROPS))

    def test_acid_citrus_is_byte_identical(self):
        """The two crops sharing nine ids with this batch must not move at all."""
        pre = _pre()
        d = _post(pre)
        for slug in ("lemon", "lime"):
            self.assertEqual(P.serialize(_crop(d, slug)), P.serialize(_crop(pre, slug)))

    def test_one_serializer(self):
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


class CatalogUntouchedInMain(unittest.TestCase):
    """These two refusals live in main(), not check(). Comparing serializations from the suite
    asserts the OUTCOME without ever driving the promote's own guard."""

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
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)

    def test_control_methods_mutation_refused(self):
        self._on_a_fixture(
            lambda d: d["control_methods"]["horticultural_oil"].__setitem__("tier", "cultural"),
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

    def test_citrus_is_fully_laddered_after_apply(self):
        """Citrus closes here: all five crops carry a ladder on every problem."""
        d = _post()
        for slug in ("lemon", "lime") + CROPS:
            for _f, p in P.problems(_crop(d, slug)):
                self.assertTrue(p.get("control_ladder"), "%s/%s unladdered" % (slug, p.get("name")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
