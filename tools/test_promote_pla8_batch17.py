#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch17.py. Base 213cb110 (batch 16's output, a commit).

REPLAY-PINNED; no RED phase is claimed. A replay-pinned suite is green from birth, so the evidence
that these guards are LIVE is `VerifyPostIsDriven` plus the mutation harness
(tools/mutate_pla8_batch17_suite.py), NOT the fact that this file passes.

Every driver asserts the ONE message its branch emits. `assertRaises(SystemExit)` alone would let a
sabotage be caught by an EARLIER check and still report a pass for the wrong reason.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch17 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

# FROZEN LITERALS -- restated here, never imported from P. A suite that reads its expectations from
# the module under test grades that module against itself.
CROPS = ("apricot", "cherry-sour", "cherry-sweet", "nectarine", "peach", "plum")
TOTAL_RUNGS = 137
TOTAL_PROBLEMS = 49
REUSE_ANCHORS = {"plum-curculio": "apple", "spotted-wing-drosophila": "strawberry",
                 "birds": "strawberry"}
REFUSED = ("bacterial-spot", "aphids")
FINE_TYPES = ("insect", "mite", "mollusk", "fungal", "bacterial", "viral", "physiological",
              "nematode", "vertebrate")


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


def _staged_with(mutator):
    batch = P.staged()
    mutator(batch)
    return lambda: batch


def _sprob(batch, slug, pid):
    for fam in ("pests", "diseases"):
        for p in batch[slug].get(fam) or []:
            if p.get("id") == pid:
                return p
    raise AssertionError("staged %s/%s not found" % (slug, pid))


_UNIQ = [0]


def _rung(m):
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
        _crop(d, "apple")["pests"][0]["id"] = "mutated-bystander"
        _expect(self, "bystander crop", lambda: P.verify_post(P.snapshot(pre), d))

    def test_addition_is_caught_not_just_mutation(self):
        """set(pre) == set(post) BEFORE value comparison. Iterating pre alone makes ADDITIONS
        invisible, which was all four PLA-162 defects."""
        pre = _pre()
        d = _post(pre)
        _crop(d, "apricot")["pests"].append({"name": "ghost-problem", "type": "insect"})
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_removal_is_caught(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "plum")["diseases"].pop()
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_undercount_is_caught(self):
        """If a crop ended up unladdered, the touched count must not still add up.

        Simulated by REVERTING one crop after a clean apply rather than by patching CROPS: patching
        it also narrows staged() and check_splits(), so the run would die inside the pre-checks and
        never reach verify_post -- green for the wrong reason, the exact masking this suite's
        assert-the-message rule exists to prevent.
        """
        pre = _pre()
        d = _post(pre)
        for fam in ("pests", "diseases"):
            src = _crop(pre, "cherry-sour").get(fam) or []
            dst = _crop(d, "cherry-sour").get(fam) or []
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
        self.assertEqual(P.rung_count(P.staged()), TOTAL_RUNGS)
        self.assertEqual(sum(1 for c in CROPS for _f, p in P.problems(_crop(d, c))
                             if p.get("control_ladder")), TOTAL_PROBLEMS)


# ---------------------------------------------------------------- premise
class SchemaPremise(unittest.TestCase):
    def test_full_schema_required(self):
        pre = _pre()
        del _crop(pre, "peach")["pests"][0]["organic_treatment_beginner"]
        _expect(self, "missing organic_treatment_beginner", lambda: P.check_schema_premise(
            P.by_slug(pre)))

    def test_note_shaped_record_refused(self):
        """Batches 15/16 were note-shaped. If a stone fruit record is ever converted, this promote's
        premise no longer describes it and must refuse rather than validate the wrong prose."""
        pre = _pre()
        _crop(pre, "peach")["pests"][0]["note_beginner"] = "converted"
        _expect(self, "note-shaped", lambda: P.check_schema_premise(P.by_slug(pre)))

    def test_already_laddered_refused(self):
        pre = _pre()
        _crop(pre, "plum")["pests"][0]["control_ladder"] = [_rung("garden_sanitation")]
        _expect(self, "already laddered", lambda: P.check_schema_premise(P.by_slug(pre)))


class TypeTransition(unittest.TestCase):
    def test_pre_state_is_coarse(self):
        pre = _pre()
        for c in CROPS:
            for p in _crop(pre, c).get("pests") or []:
                self.assertEqual(p.get("type"), "pest")
            for p in _crop(pre, c).get("diseases") or []:
                self.assertEqual(p.get("type"), "disease")

    def test_post_state_is_fine(self):
        d = _post()
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                self.assertIn(p.get("type"), FINE_TYPES)

    def test_coarse_type_surviving_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "peach", "brown-rot")["type"] = "disease"
        with _Patch("staged", lambda: batch):
            _expect(self, "kept the coarse type",
                    lambda: P.check_type_transition(batch, P.by_slug(pre)))

    def test_non_enum_type_is_refused(self):
        """The fine-type branch, reachable now that coarse-equality is checked before it."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "peach", "brown-rot")["type"] = "oomycete"
        _expect(self, "not a fine type",
                lambda: P.check_type_transition(batch, P.by_slug(pre)))

    def test_pre_state_already_fine_is_refused(self):
        pre = _pre()
        _crop(pre, "peach")["pests"][0]["type"] = "insect"
        _expect(self, "pre-state type", lambda: P.check_type_transition(P.staged(),
                                                                       P.by_slug(pre)))


# ---------------------------------------------------------------- ids
class Ids(unittest.TestCase):
    def test_off_convention_id_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "apricot", "shot-hole")["id"] = "coryneum-blight"
        _expect(self, "convention", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_bacterial_spot_id(self):
        """The peppers' generic Xanthomonas id must never reach a stone fruit."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{"Bacterial spot": "bacterial-spot"})):
            # "Bacterial spot" is the name on all FOUR crops, so every one must move or the
            # convention check fires first and masks the refusal branch under test.
            for c in ("apricot", "nectarine", "peach", "plum"):
                _sprob(batch, c, "bacterial-spot-pruni")["id"] = "bacterial-spot"
            _expect(self, "refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_generic_aphids_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{"Aphids": "aphids"})):
            _sprob(batch, "apricot", "apricot-aphids")["id"] = "aphids"
            _expect(self, "refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_unknown_problem_name_refused(self):
        """Driver for the `not in ID_CONVENTION` branch. It is MASKED by the `i != want` check
        below it whenever a real id is present, so without a staged id of None the mutation
        harness reports this branch as surviving."""
        pre = _pre()
        batch = P.staged()
        _crop(pre, "plum")["diseases"][0]["name"] = "Some Unlisted Disease"
        _sprob(batch, "plum", "black-knot")["id"] = None
        _expect(self, "not in ID_CONVENTION", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_reuse_id_present_but_anchor_lost(self):
        """Driver for the anchor branch specifically. Renaming apple's id trips `resolves nowhere`
        instead, so the id must survive ELSEWHERE off-batch while leaving the anchor."""
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "apple")):
            if p.get("id") == "plum-curculio":
                p["id"] = "moved-off-anchor"
        # Park the id on a different non-batch crop so `i not in existing` cannot fire.
        _crop(pre, "strawberry")["pests"][0]["id"] = "plum-curculio"
        _expect(self, "missing its anchor crop",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_reuse_anchor_must_exist(self):
        """A reused id whose anchor crop lost it means the join now resolves nowhere."""
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "apple")):
            if p.get("id") == "plum-curculio":
                p["id"] = "renamed-away"
        _expect(self, "resolves nowhere", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_new_id_already_taken_is_refused(self):
        pre = _pre()
        _crop(pre, "apple")["diseases"][0]["id"] = "brown-rot"
        _expect(self, "already exists", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_reuses_actually_land_on_the_anchor(self):
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
                             "%s reached a stone fruit: %s" % (pid, holders & set(CROPS)))


class Splits(unittest.TestCase):
    def test_cherry_fruit_flies_do_not_merge(self):
        """The forbidden id ADDED alongside the required one. Renaming instead would trip the
        lost-required branch below and never reach this one."""
        batch = P.staged()
        batch["cherry-sweet"]["pests"].append(
            {"id": "cherry-fruit-fly", "type": "insect",
             "control_ladder": [_rung("garden_sanitation")]})
        _expect(self, "belongs to the other split", lambda: P.check_splits(batch))

    def test_required_split_id_cannot_vanish(self):
        batch = P.staged()
        _sprob(batch, "cherry-sour", "cherry-fruit-fly")["id"] = "something-else"
        _expect(self, "lost required id", lambda: P.check_splits(batch))

    def test_cherry_borers_do_not_collapse_into_peachtree_borer(self):
        batch = P.staged()
        batch["cherry-sweet"]["pests"].append(
            {"id": "peachtree-borer", "type": "insect",
             "control_ladder": [_rung("garden_sanitation")]})
        _expect(self, "belongs to the other split", lambda: P.check_splits(batch))

    def test_renaming_a_split_id_trips_the_lost_branch(self):
        """Both branches of check_splits are driven; assertTrue(A or B) would let either rot."""
        batch = P.staged()
        _sprob(batch, "cherry-sweet", "cherry-borers")["id"] = "peachtree-borer"
        _expect(self, "lost required id", lambda: P.check_splits(batch))


class CurculioShape(unittest.TestCase):
    def test_handpick_rung_refused_on_staged_crop(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "peach", "plum-curculio")["control_ladder"].insert(1, _rung("handpick"))
        _expect(self, "handpick", lambda: P.check_curculio_shape(batch, pre))

    def test_anchor_apple_is_guarded_too(self):
        """The anchor cannot drift either, or the batch ends up consistent with nothing."""
        pre = _pre()
        _prob(pre, "apple", "plum-curculio")["control_ladder"].insert(1, _rung("handpick"))
        _expect(self, "apple/plum-curculio", lambda: P.check_curculio_shape(P.staged(), pre))

    def test_guard_is_not_vacuous(self):
        """If no shipped plum-curculio ladder exists the check would pass trivially, so it refuses."""
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "apple")):
            if p.get("id") == "plum-curculio":
                p["control_ladder"] = []
        _expect(self, "would be vacuous", lambda: P.check_curculio_shape(P.staged(), pre))


class BacterialSpotCopper(unittest.TestCase):
    def test_missing_terminal_copper_refused(self):
        batch = P.staged()
        _sprob(batch, "plum", "bacterial-spot-pruni")["control_ladder"].pop()
        _expect(self, "does not end on copper_fungicide",
                lambda: P.check_bacterial_spot_copper(batch))

    def test_dropped_preventive_hedge_refused(self):
        batch = P.staged()
        L = _sprob(batch, "plum", "bacterial-spot-pruni")["control_ladder"]
        for f in ("note_beginner", "note_seasoned"):
            L[-1][f] = re.sub(r"preventive|prevention", "useful", L[-1][f], flags=re.I)
        _expect(self, "preventive-not-curative", lambda: P.check_bacterial_spot_copper(batch))

    def test_dropped_injury_hedge_refused(self):
        batch = P.staged()
        L = _sprob(batch, "nectarine", "bacterial-spot-pruni")["control_ladder"]
        for f in ("note_beginner", "note_seasoned"):
            L[-1][f] = re.sub(r"injur\w*|harm\w*|damag\w*|hurt\w*", "affect", L[-1][f], flags=re.I)
        _expect(self, "tree-injury", lambda: P.check_bacterial_spot_copper(batch))

    def test_count_is_pinned(self):
        """Four crops carry this id; if one silently loses it the guard must not go quiet."""
        batch = P.staged()
        _sprob(batch, "apricot", "bacterial-spot-pruni")["id"] = "moved-away"
        _expect(self, "expected 4", lambda: P.check_bacterial_spot_copper(batch))


class SelfDenial(unittest.TestCase):
    """The guard that caught a live defect twice. See the promote's module docstring."""

    def test_ladder_terminality_claim_refused(self):
        batch = P.staged()
        r = _sprob(batch, "peach", "brown-rot")["control_ladder"][0]
        r["note_seasoned"] += " This ladder carries no conventional rung."
        _expect(self, "asserts the ladder ends", lambda: P.check_no_self_denial(batch))

    def test_top_of_ladder_claim_refused(self):
        batch = P.staged()
        r = _sprob(batch, "plum", "brown-rot")["control_ladder"][0]
        r["note_beginner"] += " Copper sits at the top of this ladder."
        _expect(self, "asserts the ladder ends", lambda: P.check_no_self_denial(batch))

    def test_no_rung_claim_refused(self):
        batch = P.staged()
        r = _sprob(batch, "apricot", "brown-rot")["control_ladder"][0]
        r["note_seasoned"] += " There is no reliable rung above this one."
        _expect(self, "asserts the ladder ends", lambda: P.check_no_self_denial(batch))

    def test_structural_rule_catches_what_the_phrase_list_misses(self):
        """Driver for the STRUCTURAL rule alone. Every other self-denial test uses a phrase the
        enumerated list already catches, so without this the structural half is never the branch
        that fires and the harness reports it as surviving. This sentence is the shape a real
        author produced and the enumeration missed."""
        batch = P.staged()
        r = _sprob(batch, "apricot", "shot-hole")["control_ladder"][0]
        r["note_seasoned"] += " Clearing them is the base the rest of this ladder sits on."
        for pat in P.SELF_DENIAL_PATTERNS:
            self.assertIsNone(re.search(pat, r["note_seasoned"].lower()),
                              "the enumerated list already catches this; it no longer isolates "
                              "the structural rule")
        _expect(self, "structural claim", lambda: P.check_no_self_denial(batch))

    def test_positive_control_fires_on_an_over_wide_phrase(self):
        """DRIVES the promote's positive control rather than re-implementing it.

        The first version of this test re-ran the same regex comparison itself and merely called
        the promote's function for show. Disabling that function therefore SURVIVED the mutation
        harness: the test never depended on it. A test that duplicates the logic it is supposed to
        be checking is vacuous no matter how green it looks.
        """
        with _Patch("SELF_DENIAL_PATTERNS", tuple(P.SELF_DENIAL_PATTERNS) + (r"no cure",)):
            _expect(self, "over-widened", P.check_self_denial_positive_control)

    def test_positive_control_fires_on_an_over_wide_structural_rule(self):
        """The structural half of the positive control, driven separately."""
        with _Patch("LADDER_VOCAB", re.compile(r"\bcure\b", re.I)):
            _expect(self, "over-widened", P.check_self_denial_positive_control)

    def test_positive_control_requires_both_halves(self):
        """If STRUCTURAL_CLAIM stops matching a plain hedge, the conjunction carries no weight and
        the rule has quietly become a one-word vocabulary ban."""
        with _Patch("STRUCTURAL_CLAIM", re.compile(r"zzz-never-matches")):
            _expect(self, "carrying no weight", P.check_self_denial_positive_control)

    def test_positive_control_passes_as_shipped(self):
        P.check_self_denial_positive_control()

    def test_shipped_batch_is_clean(self):
        P.check_no_self_denial(P.staged())


class Materials(unittest.TestCase):
    def test_material_outside_allowlist_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "peach", "brown-rot")["control_ladder"].append(_rung("copper_fungicide"))
        _expect(self, "outside MATERIAL_OK",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_cultural_only_ladders_stay_material_free(self):
        """29 of 49 ladders carry no material rung at all; that is the short-ladder guard as data."""
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
        self.assertEqual(free, 29)


class Shape(unittest.TestCase):
    def test_unknown_method_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "plum", "black-knot")["control_ladder"][0]["method"] = "not_a_method"
        _expect(self, "unknown method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_tier_decrease_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "plum", "plum-aphids")["control_ladder"].append(_rung("garden_sanitation"))
        _expect(self, "tier decrease", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_applies_to_incoherence_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "cherry-sour", "birds")["control_ladder"].append(_rung("copper_fungicide"))
        _expect(self, "illegal for type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_identical_registers_refused(self):
        pre = _pre()
        batch = P.staged()
        r = _sprob(batch, "apricot", "brown-rot")["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        _expect(self, "identical registers", lambda: P.validate_batch(batch,
                                                                      pre["control_methods"]))

    def test_duplicate_method_refused(self):
        pre = _pre()
        batch = P.staged()
        L = _sprob(batch, "cherry-sweet", "brown-rot")["control_ladder"]
        L.append(_rung(L[-1]["method"]))
        _expect(self, "duplicate method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_empty_ladder_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "peach", "brown-rot")["control_ladder"] = []
        _expect(self, "empty ladder", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_forbidden_method_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "apricot", "catfacing-insects")["control_ladder"].insert(
            0, _rung("trap_cropping"))
        cm = dict(pre["control_methods"])
        cm["trap_cropping"] = {"tier": "cultural", "applies_to": ["any"]}
        _expect(self, "forbidden method", lambda: P.validate_batch(batch, cm))

    def test_rung_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        # Removing avoids the duplicate-method and tier-decrease branches, so the count branch is
        # the one that actually fires.
        _sprob(batch, "plum", "brown-rot")["control_ladder"].pop()
        _expect(self, "rungs, expected", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_em_dash_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "apricot", "brown-rot")["control_ladder"][0]["note_beginner"] += " a — b"
        _expect(self, "em/en dash", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_absolute_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "apricot", "brown-rot")["control_ladder"][0]["note_beginner"] += \
            " This never fails."
        _expect(self, "absolute", lambda: P.validate_batch(batch, pre["control_methods"]))


class BlastRadius(unittest.TestCase):
    def test_catalog_untouched(self):
        pre = _pre()
        self.assertEqual(P.serialize(_post(pre)["control_methods"]),
                         P.serialize(pre["control_methods"]))

    def test_source_catalog_untouched(self):
        pre = _pre()
        self.assertEqual(P.serialize(_post(pre)["source_catalog"]),
                         P.serialize(pre["source_catalog"]))

    def test_only_batch_crops_changed(self):
        pre = _pre()
        d = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(d)
        changed = {k[0] for k in a if a[k] != b[k]}
        self.assertEqual(changed, set(CROPS))

    def test_one_serializer(self):
        """The promote and this suite must use the SAME serializer, or an indent mutation survives
        because the suite quietly re-encodes with its own settings."""
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_post(self):
        self.assertEqual(CLG.all_violations(_post()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
