#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch21.py. Base 5409c0ce (batch 20, a commit).

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are LIVE is `VerifyPostIsDriven`
plus tools/mutate_pla8_batch21_suite.py.

Every driver asserts the ONE message its branch emits.

WHAT IS NEW versus batches 17-20:

* `NoteSchemaPremise` drives a premise asserted in BOTH directions -- the note pair present AND the
  full-schema fields absent. Copying batch 20's promote would have refused this batch outright.
* `BtIsScoped` drives a CONTENT ruling: bt stays on nasturtium (the target is the pest butterfly's
  own larvae, and six brassicas ship the same rung) and was REMOVED from viola (a fritillary host,
  where Bt cannot sort the pest larvae from the desirable ones). Both halves are pinned.
* `ProseEcho` drives the guard this batch's measurement SELECTED. 9 of 20 reused-id instances match
  a shipped ladder method-for-method, which is correct convergence on generic pests, so shape
  comparison is meaningless here and prose copying is the real hazard.
* `SingularVariants` drives a guard whose premise is three live roster defects, and which refuses if
  they are ever repaired.
"""
import copy, hashlib, json, os, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch21 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

CROPS = ("nasturtium", "sunflower", "viola")
TOTAL_RUNGS = 64
TOTAL_PROBLEMS = 26
POST_SHA = "fabdaae1d3c35d54ccc49704253b5eb4e191700897786c1ec761e340166b5cb6"
BYSTANDER = "marigold"
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
    """Clean rung prose: no absolutes, no figures, no ladder vocabulary, no trap/decoy token, and
    long enough that the echo scan's 40-character sentence floor would see it if it were an echo."""
    _UNIQ[0] += 1
    return {"method": m,
            "note_beginner": "Injected beginner text number %d for this driver only." % _UNIQ[0],
            "note_seasoned": "Injected seasoned text number %d, which differs materially." % _UNIQ[0]}


def _expect(case, fragment, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(fragment, str(cm.exception))


def _run_main(path, apply_=False):
    argv = sys.argv
    sys.argv = ["promote_pla8_batch21.py", path] + (["--apply"] if apply_ else [])
    try:
        P.main()
    finally:
        sys.argv = argv


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    def test_bystander_edit_is_caught(self):
        """marigold is a note-schema sibling and the anchor for two reused ids."""
        pre = _pre()
        d = _post(pre)
        _crop(d, BYSTANDER)["pests"][0]["id"] = "mutated-bystander"
        _expect(self, "bystander crop", lambda: P.verify_post(P.snapshot(pre), d))

    def test_addition_is_caught_not_just_mutation(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "viola")["pests"].append({"name": "ghost-problem", "type": "insect"})
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_removal_is_caught(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "sunflower")["diseases"].pop()
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_undercount_is_caught(self):
        pre = _pre()
        d = _post(pre)
        for fam in ("pests", "diseases"):
            for s, t in zip(_crop(pre, "nasturtium").get(fam) or [],
                            _crop(d, "nasturtium").get(fam) or []):
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


class NoteSchemaPremise(unittest.TestCase):
    """Asserted in BOTH directions -- the half batches 17-20 could not have."""

    def test_the_records_really_are_note_shaped(self):
        pre = _pre()
        for c in CROPS:
            for _f, p in P.problems(_crop(pre, c)):
                self.assertTrue(str(p.get("note_beginner") or "").strip())
                self.assertTrue(str(p.get("note_seasoned") or "").strip())
                for f in P.FULL_SCHEMA_FIELDS:
                    self.assertNotIn(f, p)

    def test_missing_crop_refused(self):
        pre = _pre()
        by = P.by_slug(pre)
        del by["viola"]
        _expect(self, "not on the roster", lambda: P.check_note_schema_premise(by))

    def test_missing_note_refused(self):
        pre = _pre()
        _pre_prob(pre, "sunflower", "Rust")["note_seasoned"] = "  "
        _expect(self, "has no note_seasoned",
                lambda: P.check_note_schema_premise(P.by_slug(pre)))

    def test_full_schema_conversion_refused(self):
        """If these records are ever converted, the promote must refuse rather than validate prose
        it was not written against."""
        pre = _pre()
        _pre_prob(pre, "viola", "Gray mold (Botrytis blight)")["cause_seasoned"] = "converted"
        _expect(self, "were note-shaped when",
                lambda: P.check_note_schema_premise(P.by_slug(pre)))

    def test_already_laddered_refused(self):
        pre = _pre()
        _pre_prob(pre, "nasturtium", "Flea beetles")["control_ladder"] = [_rung("handpick")]
        _expect(self, "already laddered", lambda: P.check_note_schema_premise(P.by_slug(pre)))


class TypeSetFromNothing(unittest.TestCase):
    def test_all_26_pre_state_types_are_absent(self):
        pre = _pre()
        self.assertEqual({p.get("type") for c in CROPS
                          for _f, p in P.problems(_crop(pre, c))}, {None})

    def test_post_state_is_fine(self):
        d = _post()
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                self.assertIn(p.get("type"), FINE_TYPES)

    def test_pre_existing_type_breaks_the_premise(self):
        pre = _pre()
        _pre_prob(pre, "viola", "Spider mites")["type"] = "mite"
        _expect(self, "pre-state already has type",
                lambda: P.check_type_set_from_nothing(P.staged(), P.by_slug(pre)))

    def test_non_enum_post_type_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "viola", "gray-mold")["type"] = "oomycete"
        _expect(self, "is not a fine type",
                lambda: P.check_type_set_from_nothing(batch, P.by_slug(pre)))

    def test_coverage_count_is_pinned(self):
        pre = _pre()
        batch = P.staged()
        _crop(pre, "viola")["diseases"].pop()
        batch["viola"]["diseases"].pop()
        _expect(self, "type check covered",
                lambda: P.check_type_set_from_nothing(batch, P.by_slug(pre)))


class Ids(unittest.TestCase):
    def test_arity_mismatch_refused(self):
        pre = _pre()
        batch = P.staged()
        batch["sunflower"]["pests"].pop()
        _expect(self, "arity", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_unknown_problem_name_refused(self):
        pre = _pre()
        _pre_prob(pre, "viola", "Gray mold (Botrytis blight)")["name"] = "Some Unlisted Disease"
        _expect(self, "not in ID_CONVENTION",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_off_convention_id_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "sunflower", "sunflower-rust")["id"] = "puccinia-helianthi"
        _expect(self, "!= convention", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_cucurbit_bacterial_wilt_id(self):
        """The batch's worst trap: same name, different organism, OPPOSITE management."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION,
                                          **{"Bacterial wilt": "bacterial-wilt"})):
            _sprob(batch, "nasturtium", "southern-bacterial-wilt")["id"] = "bacterial-wilt"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_crop_scoped_bee_balm_rust_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(P.ID_CONVENTION, **{"Rust": "bee-balm-rust"})):
            _sprob(batch, "sunflower", "sunflower-rust")["id"] = "bee-balm-rust"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_tomato_septoria_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", dict(
                P.ID_CONVENTION,
                **{"Septoria leaf spot and powdery mildew": "septoria-leaf-spot"})):
            _sprob(batch, "sunflower", "sunflower-foliar-diseases")["id"] = "septoria-leaf-spot"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_reuse_anchor_must_exist(self):
        pre = _pre()
        for c in pre["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") == "southern-bacterial-wilt":
                    p["id"] = "renamed-away"
        _expect(self, "resolves nowhere", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_reuse_id_present_but_anchor_lost(self):
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "fig")):
            if p.get("id") == "birds-and-squirrels":
                p["id"] = "moved-off-anchor"
        _crop(pre, "apple")["pests"].append(
            {"name": "Ghost", "type": "vertebrate", "id": "birds-and-squirrels"})
        _expect(self, "missing its anchor crop",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_new_id_already_taken_is_refused(self):
        pre = _pre()
        _crop(pre, "apple")["diseases"].append(
            {"name": "Ghost", "type": "fungal", "id": "sunflower-rust"})
        _expect(self, "already exists on", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))


class SingularVariants(unittest.TestCase):
    """Three live roster splits, each with exactly ONE crop on the singular."""

    def test_all_three_splits_are_live_in_the_base(self):
        pre = _pre()
        off = P.roster_ids(pre, exclude=CROPS)
        for sing, plur in (("cutworm", "cutworms"), ("flea-beetle", "flea-beetles"),
                           ("japanese-beetle", "japanese-beetles")):
            self.assertEqual(len(off.get(sing, ())), 1, sing)
            self.assertGreater(len(off.get(plur, ())), 1, plur)

    def test_taking_a_singular_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "sunflower", "cutworms")["id"] = "cutworm"
        _expect(self, "widening a known split",
                lambda: P.check_singular_variants_not_taken(batch, pre))

    def test_majority_flip_is_refused(self):
        """The batch takes the plural BECAUSE it is the majority. If that ever inverts, the guard
        must refuse rather than keep asserting a stale rule."""
        pre = _pre()
        for slug in ("cabbage", "broccoli", "kale", "collards", "bok-choy", "arugula",
                     "artichoke", "field-corn", "flint-corn", "popcorn", "cayenne-pepper",
                     "habanero"):
            for _f, p in P.problems(_crop(pre, slug)):
                if p.get("id") == "cutworms":
                    p["id"] = "cutworm"
        _expect(self, "holders against",
                lambda: P.check_singular_variants_not_taken(P.staged(), pre))

    def test_guard_refuses_if_every_split_is_repaired(self):
        pre = _pre()
        for c in pre["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") in ("cutworm", "flea-beetle", "japanese-beetle"):
                    p["id"] = p["id"] + "s"
        _expect(self, "is live any more",
                lambda: P.check_singular_variants_not_taken(P.staged(), pre))


class Inversion(unittest.TestCase):
    """Carried from batches 15 and 16; nasturtium is the roster's sharpest case."""

    def test_trap_cropping_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "nasturtium", "aphids")["control_ladder"].insert(0, _rung("trap_cropping"))
        _expect(self, "the companion inversion",
                lambda: P.check_inversion(batch, pre["control_methods"]))

    def test_trap_vocabulary_in_a_note_refused(self):
        pre = _pre()
        batch = P.staged()
        r = _sprob(batch, "nasturtium", "aphids")["control_ladder"][0]
        r["note_seasoned"] += " Keep this stand as a trap for the vegetable bed."
        _expect(self, "must not creep back through prose",
                lambda: P.check_inversion(batch, pre["control_methods"]))

    def test_decoy_vocabulary_in_a_note_refused(self):
        pre = _pre()
        batch = P.staged()
        r = _sprob(batch, "viola", "aphids")["control_ladder"][0]
        r["note_beginner"] += " Use it as a decoy planting."
        _expect(self, "must not creep back through prose",
                lambda: P.check_inversion(batch, pre["control_methods"]))

    def test_forbidding_an_absent_method_is_refused_as_vacuous(self):
        pre = _pre()
        cm = {k: v for k, v in pre["control_methods"].items() if k != "trap_cropping"}
        _expect(self, "forbidding it is vacuous", lambda: P.check_inversion(P.staged(), cm))

    def test_note_scan_anti_vacuity_is_driven(self):
        """The SECOND vacuity branch. `check_inversion` has two -- the catalog check above and this
        one -- and the harness found this one had no driver while the suite looked complete."""
        pre = _pre()
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                p["control_ladder"] = []
        _expect(self, "no rung notes scanned",
                lambda: P.check_inversion(batch, pre["control_methods"]))

    def test_shipped_batch_is_clean(self):
        P.check_inversion(P.staged(), _pre()["control_methods"])


class BtIsScoped(unittest.TestCase):
    """A CONTENT ruling, pinned in both directions."""

    def test_bt_on_the_butterfly_host_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "viola", "caterpillars")["control_ladder"].append(_rung("bt"))
        _expect(self, "a fritillary host", lambda: P.check_bt_is_scoped(batch))

    def test_bt_outside_its_pinned_home_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "nasturtium", "flea-beetles")["control_ladder"].append(_rung("bt"))
        _expect(self, "unpinned bt rung", lambda: P.check_bt_is_scoped(batch))

    def test_losing_the_permitted_bt_rung_is_refused(self):
        """The RETENTION is a ruling too. Six brassicas ship bt on this same id."""
        batch = P.staged()
        L = _sprob(batch, "nasturtium", "cabbageworms")["control_ladder"]
        _sprob(batch, "nasturtium", "cabbageworms")["control_ladder"] = [
            r for r in L if r["method"] != "bt"]
        _expect(self, "bt rungs are", lambda: P.check_bt_is_scoped(batch))

    def test_viola_ships_no_bt_after_apply(self):
        d = _post()
        for _f, p in P.problems(_crop(d, "viola")):
            self.assertNotIn("bt", [r["method"] for r in p["control_ladder"]])
        self.assertIn("bt", [r["method"]
                             for r in _prob(d, "nasturtium", "cabbageworms")["control_ladder"]])


class ProseEcho(unittest.TestCase):
    """The guard this batch's measurement selected."""

    def test_convergent_shapes_are_the_reason_this_guard_exists(self):
        """9 of 20 reused-id instances match a shipped ladder method-for-method. That is correct
        convergence on generic pests, which is why shape comparison is NOT used here."""
        pre = _pre()
        shipped = {}
        for c in pre["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                if p.get("id") and p.get("control_ladder"):
                    shipped.setdefault(p["id"], set()).add(
                        tuple(r["method"] for r in p["control_ladder"]))
        batch = P.staged()
        match = sum(1 for c in CROPS for _f, p in P.problems(batch[c])
                    if p["id"] in shipped
                    and tuple(r["method"] for r in p["control_ladder"]) in shipped[p["id"]])
        self.assertGreaterEqual(match, 5)

    def test_verbatim_whole_note_echo_refused(self):
        pre = _pre()
        batch = P.staged()
        src = _prob(pre, "marigold", "aphids")["control_ladder"][0]["note_beginner"]
        _sprob(batch, "viola", "aphids")["control_ladder"][0]["note_beginner"] = src
        _expect(self, "verbatim echo of", lambda: P.check_no_shipped_prose_echo(batch, pre))

    def test_sentence_level_echo_refused(self):
        """The subtler half: a rung that borrows one sentence rather than the whole note."""
        pre = _pre()
        batch = P.staged()
        src = _prob(pre, "marigold", "aphids")["control_ladder"][0]["note_seasoned"]
        sent = P.sentences(src)[0]
        r = _sprob(batch, "viola", "aphids")["control_ladder"][0]
        r["note_seasoned"] = "A fresh opening clause for this driver. " + sent[0].upper() + sent[1:]
        _expect(self, "echoes a shipped sentence", lambda: P.check_no_shipped_prose_echo(batch, pre))

    def test_guard_is_not_vacuous_without_shipped_prose(self):
        pre = _pre()
        with _Patch("shipped_rung_prose", lambda d: ({}, {})):
            _expect(self, "no shipped rung prose found",
                    lambda: P.check_no_shipped_prose_echo(P.staged(), pre))

    def test_batch_scan_anti_vacuity_is_driven(self):
        """The SECOND vacuity branch, likewise undriven until the harness said so. An empty batch
        must refuse rather than report a clean echo scan over nothing."""
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                p["control_ladder"] = []
        _expect(self, "no batch notes scanned",
                lambda: P.check_no_shipped_prose_echo(batch, _pre()))

    def test_shipped_batch_is_clean(self):
        P.check_no_shipped_prose_echo(P.staged(), _pre())


class TemperatureAndVocabulary(unittest.TestCase):
    def test_degree_figure_refused(self):
        batch = P.staged()
        r = _sprob(batch, "viola", "aphids")["control_ladder"][0]
        r["note_seasoned"] += " Hold off above 90°F."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_spelled_degrees_refused(self):
        batch = P.staged()
        r = _sprob(batch, "sunflower", "aphids")["control_ladder"][0]
        r["note_beginner"] += " Wait if it is over 90 degrees."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_ladder_vocabulary_refused(self):
        batch = P.staged()
        r = _sprob(batch, "sunflower", "white-mold")["control_ladder"][0]
        r["note_beginner"] += " Work down this ladder in order."
        _expect(self, "uses internal vocabulary", lambda: P.check_no_ladder_vocabulary(batch))

    def test_shipped_batch_is_clean(self):
        P.check_no_temperature_figures(P.staged())
        P.check_no_ladder_vocabulary(P.staged())


class Materials(unittest.TestCase):
    def test_material_outside_allowlist_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "sunflower", "aphids")["control_ladder"].append(_rung("neem_oil"))
        _expect(self, "scopes every material to the note that names it",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_most_ladders_are_material_free(self):
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
        _sprob(batch, "viola", "gray-mold")["control_ladder"][0]["method"] = "not_a_method"
        _expect(self, "unknown method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_duplicate_method_refused(self):
        pre = _pre()
        batch = P.staged()
        L = _sprob(batch, "viola", "gray-mold")["control_ladder"]
        L.append(_rung(L[-1]["method"]))
        _expect(self, "duplicate method", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_tier_decrease_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "nasturtium", "aphids")["control_ladder"].append(_rung("garden_sanitation"))
        _expect(self, "tier decrease", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_applies_to_incoherence_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "nasturtium", "aphid-borne-viruses")["control_ladder"].append(
            _rung("insecticidal_soap"))
        _expect(self, "illegal for type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_identical_registers_refused(self):
        pre = _pre()
        batch = P.staged()
        r = _sprob(batch, "viola", "gray-mold")["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        _expect(self, "identical registers",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_missing_note_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "sunflower", "sunflower-rust")["control_ladder"][0]["note_beginner"] = " "
        _expect(self, "missing note_beginner",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_empty_ladder_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "nasturtium", "flea-beetles")["control_ladder"] = []
        _expect(self, "empty ladder", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_missing_type_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "viola", "spider-mites")["type"] = None
        _expect(self, "missing type", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_problem_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        batch["viola"]["diseases"].pop()
        _expect(self, "problems, expected",
                lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_per_crop_rung_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "viola", "gray-mold")["control_ladder"].pop()
        _expect(self, "rungs, expected", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_total_rung_count_pinned(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "viola", "gray-mold")["control_ladder"].pop()
        with _Patch("EXPECTED_RUNGS", dict(P.EXPECTED_RUNGS, viola=22)):
            _expect(self, "rungs total, expected",
                    lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_em_dash_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "viola", "gray-mold")["control_ladder"][0]["note_beginner"] += " a — b"
        _expect(self, "em/en dash", lambda: P.validate_batch(batch, pre["control_methods"]))

    def test_hygiene_absolute_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "viola", "gray-mold")["control_ladder"][0]["note_beginner"] += \
            " This never fails."
        _expect(self, "absolute", lambda: P.validate_batch(batch, pre["control_methods"]))


class BlastRadius(unittest.TestCase):
    def test_only_batch_crops_changed(self):
        pre = _pre()
        d = _post(pre)
        a, b = P.snapshot(pre), P.snapshot(d)
        self.assertEqual({k[0] for k in a if a[k] != b[k]}, set(CROPS))

    def test_note_schema_siblings_are_byte_identical(self):
        """The shipped companion flowers anchor several reused ids and must not move."""
        pre = _pre()
        d = _post(pre)
        for slug in ("marigold", "calendula", "cosmos", "sweet-alyssum"):
            self.assertEqual(P.serialize(_crop(d, slug)), P.serialize(_crop(pre, slug)))

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
            lambda d: d["control_methods"]["bt"].__setitem__("tier", "cultural"),
            "control_methods changed")

    def test_source_catalog_mutation_refused(self):
        self._on_a_fixture(
            lambda d: d["source_catalog"].__setitem__(
                "ghost", {"name": "G", "title": "G", "url": "https://example.edu/"}),
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
