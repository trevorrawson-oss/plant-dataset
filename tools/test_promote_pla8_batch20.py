#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch20.py. Base 50bc203f (batch 19, a commit).

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are LIVE is `VerifyPostIsDriven`
plus tools/mutate_pla8_batch20_suite.py, NOT the fact that this file passes.

Every driver asserts the ONE message its branch emits.

WHAT IS NEW versus batch 19's suite:

* `BroadGenericExemption` drives a guard that RE-MEASURES its own exemption list. `aphids` and
  `powdery-mildew` are exempt from shape comparison because they already carry 17 and 12 distinct
  shapes roster-wide; the guard refuses if an exempt id turns out not to be broad, so a narrow id
  cannot be smuggled onto the list to silence a real divergence.
* `CrossBatchDivergence` drives the narrow half, in three directions: an unpinned divergence, a pin
  the batch never compares, and a pin whose ladders have CONVERGED.
* `TypeSetFromNothing` drives the THIRD form of the type rule in four batches. All 39 problems carry
  no type at all, so every type is set rather than upgraded or preserved.
* `AnthracnoseTaxonSplit` drives a THREE-way split, and `JapaneseBeetleSplit` drives a guard whose
  premise is a pre-existing roster DEFECT.
"""
import copy, hashlib, json, os, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch20 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

CROPS = ("blackberry", "blueberry", "raspberry", "elderberry")
TOTAL_RUNGS = 140
TOTAL_PROBLEMS = 39
POST_SHA = "5409c0ce32a87c04d92724aedae17b902a572ab14c01847980078ac158521441"
BYSTANDER = "strawberry"
FINE_TYPES = ("insect", "mite", "mollusk", "fungal", "bacterial", "viral", "physiological",
              "nematode", "vertebrate")
NARROW_PINS = {"spotted-wing-drosophila", "birds", "japanese-beetles", "scale-insects",
               "stink-bugs"}


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
    _UNIQ[0] += 1
    return {"method": m, "note_beginner": "injected beginner %d" % _UNIQ[0],
            "note_seasoned": "injected seasoned %d and it differs" % _UNIQ[0]}


def _expect(case, fragment, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(fragment, str(cm.exception))


def _run_main(path, apply_=False):
    argv = sys.argv
    sys.argv = ["promote_pla8_batch20.py", path] + (["--apply"] if apply_ else [])
    try:
        P.main()
    finally:
        sys.argv = argv


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    def test_bystander_edit_is_caught(self):
        """The bystander is strawberry, the anchor for three of this batch's reused ids."""
        pre = _pre()
        d = _post(pre)
        _crop(d, BYSTANDER)["pests"][0]["id"] = "mutated-bystander"
        _expect(self, "bystander crop", lambda: P.verify_post(P.snapshot(pre), d))

    def test_addition_is_caught_not_just_mutation(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "blackberry")["pests"].append({"name": "ghost-problem", "type": "insect"})
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_removal_is_caught(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "raspberry")["diseases"].pop()
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_undercount_is_caught(self):
        pre = _pre()
        d = _post(pre)
        for fam in ("pests", "diseases"):
            for s, t in zip(_crop(pre, "elderberry").get(fam) or [],
                            _crop(d, "elderberry").get(fam) or []):
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


class SchemaPremise(unittest.TestCase):
    def test_missing_crop_refused(self):
        pre = _pre()
        by = P.by_slug(pre)
        del by["elderberry"]
        _expect(self, "not on the roster", lambda: P.check_schema_premise(by))

    def test_full_schema_required(self):
        pre = _pre()
        del _pre_prob(pre, "blueberry", "Mummy berry")["organic_treatment_beginner"]
        _expect(self, "missing organic_treatment_beginner",
                lambda: P.check_schema_premise(P.by_slug(pre)))

    def test_blank_premise_field_refused(self):
        pre = _pre()
        _pre_prob(pre, "raspberry", "Orange rust")["cause_seasoned"] = "  "
        _expect(self, "missing cause_seasoned", lambda: P.check_schema_premise(P.by_slug(pre)))

    def test_already_laddered_refused(self):
        pre = _pre()
        _pre_prob(pre, "blackberry", "Stink bugs")["control_ladder"] = [_rung("garden_sanitation")]
        _expect(self, "already laddered", lambda: P.check_schema_premise(P.by_slug(pre)))


class TypeSetFromNothing(unittest.TestCase):
    """The THIRD form of the type rule in four batches, and it was measured, not inherited."""

    def test_all_39_pre_state_types_are_absent(self):
        pre = _pre()
        got = {p.get("type") for c in CROPS for _f, p in P.problems(_crop(pre, c))}
        self.assertEqual(got, {None})

    def test_post_state_is_fine(self):
        d = _post()
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                self.assertIn(p.get("type"), FINE_TYPES)

    def test_pre_existing_type_breaks_the_premise(self):
        """If a pre-state type ever appears, the set-from-nothing rule is the wrong rule and the
        promote must refuse rather than silently apply it."""
        pre = _pre()
        _pre_prob(pre, "blueberry", "Mummy berry")["type"] = "fungal"
        _expect(self, "pre-state already has type",
                lambda: P.check_type_is_set_from_nothing(P.staged(), P.by_slug(pre)))

    def test_non_enum_post_type_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blueberry", "mummy-berry")["type"] = "oomycete"
        _expect(self, "is not a fine type",
                lambda: P.check_type_is_set_from_nothing(batch, P.by_slug(pre)))

    def test_coverage_count_is_pinned(self):
        pre = _pre()
        batch = P.staged()
        _crop(pre, "blackberry")["diseases"].pop()
        batch["blackberry"]["diseases"].pop()
        _expect(self, "type check covered",
                lambda: P.check_type_is_set_from_nothing(batch, P.by_slug(pre)))


class Ids(unittest.TestCase):
    def test_arity_mismatch_refused(self):
        pre = _pre()
        batch = P.staged()
        batch["raspberry"]["pests"].pop()
        _expect(self, "arity", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_unknown_problem_name_refused(self):
        pre = _pre()
        _pre_prob(pre, "blueberry", "Mummy berry")["name"] = "Some Unlisted Disease"
        _expect(self, "not in ID_CONVENTION",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_off_convention_id_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blueberry", "mummy-berry")["id"] = "monilinia-vaccinii"
        _expect(self, "!= convention", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_generic_anthracnose_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{"Anthracnose": "anthracnose"})):
            for c in ("blackberry", "raspberry"):
                _sprob(batch, c, "cane-anthracnose")["id"] = "anthracnose"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_singular_japanese_beetle_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION,
                                          **{"Japanese beetle": "japanese-beetle"})):
            for c in ("blackberry", "raspberry"):
                _sprob(batch, c, "japanese-beetles")["id"] = "japanese-beetle"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_citrus_phytophthora_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION,
                                          **{"Phytophthora root rot": "phytophthora-foot-rot"})):
            for c in ("blackberry", "blueberry", "raspberry"):
                _sprob(batch, c, "phytophthora-root-rot")["id"] = "phytophthora-foot-rot"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_reuse_anchor_must_exist(self):
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "strawberry")):
            if p.get("id") == "spotted-wing-drosophila":
                p["id"] = "renamed-away"
        for _f, p in P.problems(_crop(pre, "cherry-sour")):
            if p.get("id") == "spotted-wing-drosophila":
                p["id"] = "renamed-away"
        for _f, p in P.problems(_crop(pre, "cherry-sweet")):
            if p.get("id") == "spotted-wing-drosophila":
                p["id"] = "renamed-away"
        _expect(self, "resolves nowhere", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_reuse_id_present_but_anchor_lost(self):
        """The id survives elsewhere off-batch while leaving its anchor, so the anchor branch is the
        one that fires rather than `resolves nowhere`."""
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "strawberry")):
            if p.get("id") == "spotted-wing-drosophila":
                p["id"] = "moved-off-anchor"
        _expect(self, "missing its anchor crop",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_new_id_already_taken_is_refused(self):
        pre = _pre()
        _crop(pre, "apple")["diseases"].append(
            {"name": "Ghost disease", "type": "fungal", "id": "mummy-berry"})
        _expect(self, "already exists on", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))


class AnthracnoseTaxonSplit(unittest.TestCase):
    """One common name, THREE organisms."""

    def test_generic_taken_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blackberry", "cane-anthracnose")["id"] = "anthracnose"
        _expect(self, "took the vegetable generic",
                lambda: P.check_anthracnose_taxon_split(batch, pre))

    def test_missing_split_id_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blueberry", "blueberry-ripe-rot")["id"] = "something-else"
        _expect(self, "missing; the three-way anthracnose split",
                lambda: P.check_anthracnose_taxon_split(batch, pre))

    def test_split_landing_on_the_wrong_crops_refused(self):
        """The split is pinned to its CROPS, not merely to the ids existing somewhere."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blueberry", "blueberry-ripe-rot")["id"] = "cane-anthracnose"
        _expect(self, "sits on", lambda: P.check_anthracnose_taxon_split(batch, pre))

    def test_guard_refuses_if_the_generic_is_gone(self):
        pre = _pre()
        for c in pre["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") == "anthracnose":
                    p["id"] = "gone"
        _expect(self, "exists nowhere off-batch",
                lambda: P.check_anthracnose_taxon_split(P.staged(), pre))

    def test_three_ids_hold_after_apply(self):
        d = _post()
        holders = {}
        for c in d["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") in ("anthracnose", "cane-anthracnose", "blueberry-ripe-rot"):
                    holders.setdefault(p["id"], set()).add(c["slug"])
        self.assertFalse(holders["anthracnose"] & set(CROPS))
        self.assertEqual(holders["cane-anthracnose"], {"blackberry", "raspberry"})
        self.assertEqual(holders["blueberry-ripe-rot"], {"blueberry"})


class JapaneseBeetleSplit(unittest.TestCase):
    """This guard's PREMISE is a pre-existing roster defect."""

    def test_the_split_really_exists_in_the_base(self):
        pre = _pre()
        off = P.roster_ids(pre, exclude=CROPS)
        self.assertEqual(off.get("japanese-beetle"), {"basil"})
        self.assertEqual(off.get("japanese-beetles"), {"marigold", "zinnia", "echinacea"})

    def test_taking_the_singular_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blackberry", "japanese-beetles")["id"] = "japanese-beetle"
        _expect(self, "widening a known roster split",
                lambda: P.check_japanese_beetle_split_not_widened(batch, pre))

    def test_guard_refuses_if_the_split_is_repaired(self):
        """If basil is ever repointed, this guard must be RETIRED deliberately rather than quietly
        passing on a premise that no longer holds."""
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "basil")):
            if p.get("id") == "japanese-beetle":
                p["id"] = "japanese-beetles"
        _expect(self, "not in the state this guard was written against",
                lambda: P.check_japanese_beetle_split_not_widened(P.staged(), pre))

    def test_guard_is_not_vacuous(self):
        pre = _pre()
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                if p["id"] == "japanese-beetles":
                    p["id"] = "renamed"
        _expect(self, "would be vacuous",
                lambda: P.check_japanese_beetle_split_not_widened(batch, pre))


class BroadGenericExemption(unittest.TestCase):
    """The exemption is RE-MEASURED. Without this a narrow id could be added to BROAD_GENERIC to
    silence a real divergence and every other test would still pass."""

    def test_the_exempt_ids_really_are_broad(self):
        pre = _pre()
        for pid in P.BROAD_GENERIC:
            sh = P.shapes_off_batch(pre, pid)
            self.assertGreaterEqual(len(sh), P.BROAD_MIN_HOLDERS)
            self.assertGreaterEqual(len(set(sh.values())), P.BROAD_MIN_SHAPES)

    def test_smuggling_a_narrow_id_onto_the_list_is_refused(self):
        pre = _pre()
        with _Patch("BROAD_GENERIC", tuple(P.BROAD_GENERIC) + ("scale-insects",)):
            _expect(self, "is exempt from shape comparison but is not broad",
                    lambda: P.check_broad_generic_exemption_is_earned(pre))

    def test_exemption_passes_as_shipped(self):
        P.check_broad_generic_exemption_is_earned(_pre())


class CrossBatchDivergence(unittest.TestCase):
    def test_unpinned_divergence_is_refused(self):
        """Every narrow id in this batch IS pinned, so the pin is removed to reach the branch."""
        pre = _pre()
        pins = {k: v for k, v in P.NARROW_DIVERGENCE.items() if k != "scale-insects"}
        with _Patch("NARROW_DIVERGENCE", pins):
            _expect(self, "is not a pinned divergence",
                    lambda: P.check_cross_batch_divergence(P.staged(), pre))

    def test_pin_the_batch_never_compares_is_refused(self):
        pre = _pre()
        pins = dict(P.NARROW_DIVERGENCE, **{"ghost-id": "not in this batch"})
        with _Patch("NARROW_DIVERGENCE", pins):
            _expect(self, "never compared it",
                    lambda: P.check_cross_batch_divergence(P.staged(), pre))

    def test_converged_pin_is_refused(self):
        """A pin whose ladders now MATCH a shipped one is false documentation. Blueberry's
        scale-insects ladder is made identical to the shipped citrus one, so nothing diverges."""
        pre = _pre()
        batch = P.staged()
        shipped = _prob(pre, "lemon", "scale-insects")["control_ladder"]
        _sprob(batch, "blueberry", "scale-insects")["control_ladder"] = copy.deepcopy(shipped)
        _expect(self, "now MATCHES a shipped one",
                lambda: P.check_cross_batch_divergence(batch, pre))

    def test_guard_is_not_vacuous(self):
        pre = _pre()
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                p["id"] = "%s-only-%s" % (c, p["id"])
        with _Patch("NARROW_DIVERGENCE", {}):
            _expect(self, "no narrow shared ids compared",
                    lambda: P.check_cross_batch_divergence(batch, pre))

    def test_broad_generics_are_not_shape_compared(self):
        """Positive control for the exemption: aphids diverges from all 17 shipped shapes on every
        berry, and the guard passes anyway because it is exempt."""
        pre = _pre()
        P.check_cross_batch_divergence(P.staged(), pre)
        sh = P.shapes_off_batch(pre, "aphids")
        mine = tuple(r["method"] for r in _sprob(P.staged(), "blackberry", "aphids")["control_ladder"])
        self.assertNotIn(mine, set(sh.values()))


class TemperatureAndVocabulary(unittest.TestCase):
    def test_degree_figure_refused(self):
        batch = P.staged()
        r = _sprob(batch, "blueberry", "scale-insects")["control_ladder"][-1]
        r["note_seasoned"] += " Do not spray above 90°F."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_spelled_degrees_refused(self):
        batch = P.staged()
        r = _sprob(batch, "blackberry", "aphids")["control_ladder"][-1]
        r["note_beginner"] += " Hold off when it is over 90 degrees out."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_ladder_vocabulary_refused(self):
        batch = P.staged()
        r = _sprob(batch, "raspberry", "orange-rust")["control_ladder"][0]
        r["note_beginner"] += " Work down this ladder in order."
        _expect(self, "uses internal vocabulary", lambda: P.check_no_ladder_vocabulary(batch))

    def test_shipped_batch_is_clean(self):
        P.check_no_temperature_figures(P.staged())
        P.check_no_ladder_vocabulary(P.staged())


class Materials(unittest.TestCase):
    def test_material_outside_allowlist_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blackberry", "aphids")["control_ladder"].append(_rung("horticultural_oil"))
        _expect(self, "outside MATERIAL_OK",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_most_ladders_are_material_free(self):
        """34 of 39 carry no material rung at all. Berry records are markedly more cultural than
        citrus's, and that is the source, not the authoring."""
        d = _post()
        free = 0
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                if not P.MATERIAL_OK.get((c, p["id"])):
                    for r in p["control_ladder"]:
                        self.assertNotIn(d["control_methods"][r["method"]]["tier"],
                                         P.MATERIAL_TIERS)
                    free += 1
        self.assertEqual(free, TOTAL_PROBLEMS - len(P.MATERIAL_OK))


class Shape(unittest.TestCase):
    def test_unknown_method_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "raspberry", "orange-rust")["control_ladder"][0]["method"] = "not_a_method"
        _expect(self, "unknown method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_forbidden_method_refused(self):
        """`bt` is forbidden here: it is caterpillar-specific and the katydid/beetle records would
        make it a wrong-organism rung."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blackberry", "japanese-beetles")["control_ladder"].insert(0, _rung("bt"))
        _expect(self, "forbidden method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_duplicate_method_refused(self):
        pre = _pre()
        batch = P.staged()
        L = _sprob(batch, "raspberry", "orange-rust")["control_ladder"]
        L.append(_rung(L[-1]["method"]))
        _expect(self, "duplicate method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_tier_decrease_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blackberry", "aphids")["control_ladder"].append(_rung("garden_sanitation"))
        _expect(self, "tier decrease", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_applies_to_incoherence_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "raspberry", "raspberry-mosaic-virus")["control_ladder"].append(
            _rung("insecticidal_soap"))
        _expect(self, "illegal for type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_identical_registers_refused(self):
        pre = _pre()
        batch = P.staged()
        r = _sprob(batch, "raspberry", "orange-rust")["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        _expect(self, "identical registers",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_missing_note_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "elderberry", "elder-borers")["control_ladder"][0]["note_beginner"] = " "
        _expect(self, "missing note_beginner",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_empty_ladder_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "elderberry", "elder-borers")["control_ladder"] = []
        _expect(self, "empty ladder", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_missing_type_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "blueberry", "birds")["type"] = None
        _expect(self, "missing type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_problem_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        batch["blueberry"]["diseases"].pop()
        _expect(self, "problems, expected",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_per_crop_rung_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "elderberry", "powdery-mildew")["control_ladder"].pop()
        _expect(self, "rungs, expected", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_total_rung_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "elderberry", "powdery-mildew")["control_ladder"].pop()
        with _Patch("EXPECTED_RUNGS", dict(P.EXPECTED_RUNGS, elderberry=20)):
            _expect(self, "rungs total, expected",
                    lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_em_dash_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "raspberry", "orange-rust")["control_ladder"][0]["note_beginner"] += " a — b"
        _expect(self, "em/en dash", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_absolute_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "raspberry", "orange-rust")["control_ladder"][0]["note_beginner"] += \
            " This never fails."
        _expect(self, "absolute", lambda: P.validate_batch(batch, pre["control_methods"]))


class BlastRadius(unittest.TestCase):
    def test_only_batch_crops_changed(self):
        pre = _pre()
        d = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(d)
        self.assertEqual({k[0] for k in a if a[k] != b[k]}, set(CROPS))

    def test_strawberry_is_byte_identical(self):
        """Strawberry anchors three reused ids and is the only other berry. It must not move."""
        pre = _pre()
        d = _post(pre)
        self.assertEqual(P.serialize(_crop(d, "strawberry")),
                         P.serialize(_crop(pre, "strawberry")))

    def test_one_serializer(self):
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


class CatalogUntouchedInMain(unittest.TestCase):
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
            lambda d: d["control_methods"]["garden_sanitation"].__setitem__("tier", "physical"),
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

    def test_berry_category_is_fully_laddered_after_apply(self):
        d = _post()
        for slug in CROPS + ("strawberry",):
            for _f, p in P.problems(_crop(d, slug)):
                self.assertTrue(p.get("control_ladder"), "%s/%s unladdered" % (slug, p.get("name")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
