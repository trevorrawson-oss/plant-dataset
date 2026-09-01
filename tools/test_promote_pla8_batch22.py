#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch22.py. Base fabdaae1 (batch 21, a commit).

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are LIVE is `VerifyPostIsDriven`
plus tools/mutate_pla8_batch22_suite.py.

Every driver asserts the ONE message its branch emits, and every anti-vacuity branch has its own
driver -- batch 21's two harness survivors were both anti-vacuity branches with no driver, in a
suite that looked complete at 71 green tests.

WHAT IS NEW versus batches 17-21:

* `FullSchemaPremise` is the mirror of batch 21's note-schema premise, asserted in both directions,
  and it also pins the per-crop `severity` asymmetry that the handoff did not record.
* `TypeSplitByCrop` drives the first type rule that is TWO-SIDED WITHIN one batch: two crops set
  from nothing, one upgraded from coarse. Both sides, and both coverage counts, are driven.
* `TemplateSiblingDivergence` drives the guard this batch's measurement SELECTED, and it is the
  batch 3 defect made mechanical: where a batch problem's source prose is byte-identical to a
  shipped sibling's, the ladder must match, with one adjudicated exception pinned.
* `ScopeVariantIds` drives an id ruling batch 21's method could not have reached. Checking a mint
  BY ID passes an id that merely resembles a live one; a substring scan found two mints sitting
  beside a shorter roster id that names a WIDER problem.
"""
import copy, hashlib, json, os, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch22 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

CROPS = ("english-cucumber", "edamame", "pumpkin")
TOTAL_RUNGS = 135
TOTAL_PROBLEMS = 26
POST_SHA = "919eabc4d2dae936e3f5b876c52799f5a3a3e3d1983c2c8ac324384ab986c073"
BYSTANDER = "butternut-squash"     # the template sibling three of these guards lean on
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
    """Clean rung prose: no absolutes, no figures, no ladder vocabulary, and long enough that the
    echo scan's 40-character sentence floor would see it if it were an echo."""
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
    sys.argv = ["promote_pla8_batch22.py", path] + (["--apply"] if apply_ else [])
    try:
        P.main()
    finally:
        sys.argv = argv


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    def test_bystander_edit_is_caught(self):
        """butternut-squash is the template twin for three of pumpkin's problems and the anchor for
        six reused ids, so it is the bystander most likely to be touched by mistake."""
        pre = _pre()
        d = _post(pre)
        _crop(d, BYSTANDER)["pests"][0]["id"] = "mutated-bystander"
        _expect(self, "bystander crop", lambda: P.verify_post(P.snapshot(pre), d))

    def test_addition_is_caught_not_just_mutation(self):
        """set(pre) == set(post) BEFORE any value comparison; iterating pre alone makes every
        addition invisible, which was all four PLA-162 defects."""
        pre = _pre()
        d = _post(pre)
        _crop(d, "pumpkin")["pests"].append({"name": "ghost-problem", "type": "insect"})
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_removal_is_caught(self):
        pre = _pre()
        d = _post(pre)
        _crop(d, "edamame")["diseases"].pop()
        _expect(self, "problem set changed", lambda: P.verify_post(P.snapshot(pre), d))

    def test_undercount_is_caught(self):
        pre = _pre()
        d = _post(pre)
        for fam in ("pests", "diseases"):
            for s, t in zip(_crop(pre, "pumpkin").get(fam) or [],
                            _crop(d, "pumpkin").get(fam) or []):
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
        """Never live canonical: the post fixture is this promote's OWN replayed output."""
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

    def test_counts_are_pinned_and_agree_with_the_staged_files(self):
        batch = P.staged()
        self.assertEqual(sum(P.EXPECTED_PROBLEMS.values()), TOTAL_PROBLEMS)
        self.assertEqual(sum(P.EXPECTED_RUNGS.values()), TOTAL_RUNGS)
        for c in CROPS:
            self.assertEqual(len(P.problems(batch[c])), P.EXPECTED_PROBLEMS[c])
            self.assertEqual(sum(len(p["control_ladder"]) for _f, p in P.problems(batch[c])),
                             P.EXPECTED_RUNGS[c])


class FullSchemaPremise(unittest.TestCase):
    """The mirror of batch 21's note-schema premise, asserted in BOTH directions."""

    def test_the_records_really_are_full_shaped(self):
        pre = _pre()
        for c in CROPS:
            for _f, p in P.problems(_crop(pre, c)):
                for f in P.FULL_SCHEMA_FIELDS:
                    self.assertTrue(str(p.get(f) or "").strip(), (c, p.get("name"), f))
                for f in P.NOTE_FIELDS:
                    self.assertNotIn(f, p)
                self.assertTrue(p.get("sources"))
                self.assertTrue(p.get("anchoring_urls"))

    def test_severity_asymmetry_is_real(self):
        """edamame's problems carry `severity`; the other two crops' do not. Measured, not in the
        handoff, and pinned so a drift on either side is visible."""
        pre = _pre()
        for c in CROPS:
            for _f, p in P.problems(_crop(pre, c)):
                self.assertEqual("severity" in p, c in P.SEVERITY_PRESENT, (c, p.get("name")))

    def test_missing_crop_refused(self):
        pre = _pre()
        by = P.by_slug(pre)
        del by["pumpkin"]
        _expect(self, "not on the roster", lambda: P.check_full_schema_premise(by))

    def test_missing_prose_field_refused(self):
        pre = _pre()
        _pre_prob(pre, "pumpkin", "Squash bug")["cause_seasoned"] = "  "
        _expect(self, "has no cause_seasoned",
                lambda: P.check_full_schema_premise(P.by_slug(pre)))

    def test_note_schema_conversion_refused(self):
        """The other direction: if these records are ever converted to the companion note shape,
        the promote must refuse rather than validate prose it was not written against."""
        pre = _pre()
        _pre_prob(pre, "edamame", "Stink bugs")["note_beginner"] = "converted"
        _expect(self, "were full-schema when",
                lambda: P.check_full_schema_premise(P.by_slug(pre)))

    def test_missing_sources_refused(self):
        pre = _pre()
        _pre_prob(pre, "english-cucumber", "Gray mold")["sources"] = []
        _expect(self, "has no sources", lambda: P.check_full_schema_premise(P.by_slug(pre)))

    def test_missing_anchoring_urls_refused(self):
        pre = _pre()
        _pre_prob(pre, "english-cucumber", "Gray mold")["anchoring_urls"] = {}
        _expect(self, "has no anchoring_urls",
                lambda: P.check_full_schema_premise(P.by_slug(pre)))

    def test_severity_appearing_on_a_crop_without_it_refused(self):
        pre = _pre()
        _pre_prob(pre, "pumpkin", "Squash bug")["severity"] = "high"
        _expect(self, "severity present", lambda: P.check_full_schema_premise(P.by_slug(pre)))

    def test_severity_vanishing_from_edamame_refused(self):
        pre = _pre()
        del _pre_prob(pre, "edamame", "Stink bugs")["severity"]
        _expect(self, "severity present", lambda: P.check_full_schema_premise(P.by_slug(pre)))

    def test_already_laddered_refused(self):
        pre = _pre()
        _pre_prob(pre, "pumpkin", "Squash bug")["control_ladder"] = [_rung("handpick")]
        _expect(self, "already laddered", lambda: P.check_full_schema_premise(P.by_slug(pre)))

    def test_coverage_count_is_pinned(self):
        pre = _pre()
        _crop(pre, "pumpkin")["diseases"].pop()
        _expect(self, "premise check covered",
                lambda: P.check_full_schema_premise(P.by_slug(pre)))


class TypeSplitByCrop(unittest.TestCase):
    """The fifth type rule in six batches, and the first two-sided WITHIN a batch."""

    def test_the_split_is_real_in_the_base(self):
        pre = _pre()
        for c in P.SET_FROM_NOTHING:
            self.assertEqual({p.get("type") for _f, p in P.problems(_crop(pre, c))}, {None}, c)
        for c in P.UPGRADE_FROM_COARSE:
            self.assertEqual({p.get("type") for _f, p in P.problems(_crop(pre, c))},
                             {"pest", "disease"}, c)

    def test_post_state_is_fine_everywhere(self):
        d = _post()
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                self.assertIn(p.get("type"), FINE_TYPES)

    def test_rule_must_cover_every_crop(self):
        with _Patch("SET_FROM_NOTHING", ("english-cucumber",)):
            _expect(self, "does not cover every crop",
                    lambda: P.check_type_split_by_crop(P.staged(), P.by_slug(_pre())))

    def test_pre_existing_type_on_the_set_side_refused(self):
        pre = _pre()
        _pre_prob(pre, "pumpkin", "Squash bug")["type"] = "insect"
        _expect(self, "set-from-nothing side",
                lambda: P.check_type_split_by_crop(P.staged(), P.by_slug(pre)))

    def test_missing_coarse_type_on_the_upgrade_side_refused(self):
        pre = _pre()
        _pre_prob(pre, "edamame", "Stink bugs")["type"] = None
        _expect(self, "is not coarse; this crop",
                lambda: P.check_type_split_by_crop(P.staged(), P.by_slug(pre)))

    def test_wrong_coarse_value_for_the_family_refused(self):
        """A `disease` sitting in pests[] is a coarse value that is still wrong."""
        pre = _pre()
        _pre_prob(pre, "edamame", "Stink bugs")["type"] = "disease"
        _expect(self, "carries coarse type",
                lambda: P.check_type_split_by_crop(P.staged(), P.by_slug(pre)))

    def test_non_enum_post_type_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "pumpkin", "downy-mildew")["type"] = "oomycete"
        _expect(self, "is not a fine type",
                lambda: P.check_type_split_by_crop(batch, P.by_slug(pre)))

    def test_post_type_off_the_pinned_table_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "edamame", "soybean-cyst-nematode")["type"] = "insect"
        _expect(self, "!= pinned", lambda: P.check_type_split_by_crop(batch, P.by_slug(pre)))

    def test_unlisted_id_refused(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("EXPECTED_TYPES", {k: v for k, v in P.EXPECTED_TYPES.items()
                                       if k != ("pumpkin", "squash-bug")}):
            _expect(self, "not in EXPECTED_TYPES",
                    lambda: P.check_type_split_by_crop(batch, P.by_slug(pre)))

    def test_coverage_counts_are_pinned(self):
        pre = _pre()
        batch = P.staged()
        _crop(pre, "pumpkin")["diseases"].pop()
        batch["pumpkin"]["diseases"].pop()
        _expect(self, "type split covered",
                lambda: P.check_type_split_by_crop(batch, P.by_slug(pre)))


class Ids(unittest.TestCase):
    def test_convention_is_keyed_by_crop_and_name(self):
        """Three crops share the name "Downy mildew"; two share "Aphids" and "Cucumber beetles".
        A name-only table cannot express this batch."""
        names = [k[1] for k in P.ID_CONVENTION]
        self.assertGreater(len(names), len(set(names)))

    def test_arity_mismatch_refused(self):
        pre = _pre()
        batch = P.staged()
        batch["edamame"]["pests"].pop()
        _expect(self, "arity", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_unknown_problem_name_refused(self):
        pre = _pre()
        _pre_prob(pre, "pumpkin", "Squash bug")["name"] = "Some Unlisted Pest"
        _expect(self, "not in ID_CONVENTION",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_off_convention_id_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "edamame", "soybean-aphid")["id"] = "aphis-glycines"
        _expect(self, "!= convention", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_ralstonia_id_on_the_cucurbit_wilt(self):
        """Batch 21's trap, mirrored. pumpkin's wilt IS the beetle-gut Erwinia the roster id was
        minted for, so `bacterial-wilt` is right here and `southern-bacterial-wilt` is not."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", {**P.ID_CONVENTION,
                                      ("pumpkin", "Bacterial wilt"): "southern-bacterial-wilt"}):
            _sprob(batch, "pumpkin", "bacterial-wilt")["id"] = "southern-bacterial-wilt"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_generic_spider_mites_id(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", {**P.ID_CONVENTION,
                                      ("edamame", "Two-spotted spider mite"): "spider-mites"}):
            _sprob(batch, "edamame", "two-spotted-spider-mite")["id"] = "spider-mites"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_refused_artichoke_minority_gray_mold_id(self):
        """artichoke sits alone on `botrytis-gray-mold` for the same organism the majority id
        `gray-mold` names on five crops. english-cucumber takes the majority."""
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", {**P.ID_CONVENTION,
                                      ("english-cucumber", "Gray mold"): "botrytis-gray-mold"}):
            _sprob(batch, "english-cucumber", "gray-mold")["id"] = "botrytis-gray-mold"
            _expect(self, "took refused id", lambda: P.check_ids(batch, P.by_slug(pre), pre))

    def test_reuse_anchor_must_exist(self):
        pre = _pre()
        for c in pre["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") == "gummy-stem-blight":
                    p["id"] = "renamed-away"
        _expect(self, "resolves nowhere", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_reuse_id_present_but_anchor_lost(self):
        pre = _pre()
        for _f, p in P.problems(_crop(pre, "cantaloupe")):
            if p.get("id") == "gummy-stem-blight":
                p["id"] = "moved-off-anchor"
        _expect(self, "missing its anchor crop",
                lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_new_id_already_taken_is_refused(self):
        pre = _pre()
        _crop(pre, "apple")["diseases"].append(
            {"name": "Ghost", "type": "fungal", "id": "soybean-cyst-nematode"})
        _expect(self, "already exists on", lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))

    def test_id_set_coverage_is_asserted_not_just_membership(self):
        """A COVERAGE assertion, not an overlap one: the batch must take exactly the pinned set."""
        with _Patch("REUSED_IDS", dict(P.REUSED_IDS, **{"ghost-id": "apple"})):
            pre = _pre()
            _crop(pre, "apple")["pests"].append(
                {"name": "Ghost", "type": "insect", "id": "ghost-id"})
            _expect(self, "the batch takes",
                    lambda: P.check_ids(P.staged(), P.by_slug(pre), pre))


class SingularVariants(unittest.TestCase):
    """Carried from batch 21: three live roster splits, each with ONE crop on the singular."""

    def test_all_three_splits_are_live_in_the_base(self):
        pre = _pre()
        off = P.roster_ids(pre, exclude=CROPS)
        for sing, plur in P.SINGULAR_PLURAL_PAIRS:
            self.assertEqual(len(off.get(sing, ())), 1, sing)
            self.assertGreater(len(off.get(plur, ())), 1, plur)

    def test_taking_a_singular_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "edamame", "japanese-beetles")["id"] = "japanese-beetle"
        _expect(self, "widening a known split",
                lambda: P.check_singular_variants_not_taken(batch, pre))

    def test_majority_flip_is_refused(self):
        pre = _pre()
        holders = [c["slug"] for c in pre["crops"] if c["slug"] not in CROPS
                   for _f, p in P.problems(c) if p.get("id") == "japanese-beetles"]
        self.assertGreater(len(holders), 2)
        keep = holders[0]          # the pair must stay LIVE, or the partial-repair branch fires
        moved = 0
        for c in pre["crops"]:
            if c["slug"] in CROPS or c["slug"] == keep:
                continue
            for _f, p in P.problems(c):
                if p.get("id") == "japanese-beetles":
                    p["id"] = "japanese-beetle"
                    moved += 1
        self.assertGreater(moved, 1)
        _expect(self, "holders against",
                lambda: P.check_singular_variants_not_taken(P.staged(), pre))

    def test_partial_repair_is_refused(self):
        """Stricter than batch 21, which tolerated a partial repair. A repair changes the fact base
        this guard encodes, so it must be re-measured rather than silently absorbed."""
        pre = _pre()
        for c in pre["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") == "cutworm":
                    p["id"] = "cutworms"
        _expect(self, "singular/plural splits are still live",
                lambda: P.check_singular_variants_not_taken(P.staged(), pre))

    def test_full_repair_is_refused(self):
        pre = _pre()
        for c in pre["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") in ("cutworm", "flea-beetle", "japanese-beetle"):
                    p["id"] = p["id"] + "s"
        _expect(self, "singular/plural splits are still live",
                lambda: P.check_singular_variants_not_taken(P.staged(), pre))


class ScopeVariantIds(unittest.TestCase):
    """Two mints sit beside a SHORTER roster id naming a WIDER problem. Checking a mint BY ID -- the
    fix batch 21's failure earned -- passes an id that merely RESEMBLES a live one."""

    def test_the_wider_ids_really_are_wider_in_the_base(self):
        pre = _pre()
        for mint, shorter, holders, wider, batch_key, own in P.SCOPE_VARIANTS:
            off = P.roster_ids(pre, exclude=CROPS)
            self.assertEqual(set(off[shorter]), set(holders), shorter)
            self.assertNotIn(mint, off, mint)
            src = P.find_problem(pre, batch_key[0], batch_key[1])
            blob = " ".join(str(src.get(k) or "") for k in P.FULL_SCHEMA_FIELDS).lower()
            self.assertIn(own.lower(), blob)
            self.assertNotIn(wider.lower(), blob)

    def test_taking_the_wider_bean_blight_id_is_refused(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", {**P.ID_CONVENTION,
                                      ("edamame", "Bacterial blight"): "bacterial-blights"}):
            _sprob(batch, "edamame", "bacterial-blight")["id"] = "bacterial-blights"
            _expect(self, "merging a single-pathogen problem",
                    lambda: P.check_scope_variant_ids_not_merged(batch, pre))

    def test_taking_the_compound_calendula_id_is_refused(self):
        pre = _pre()
        batch = P.staged()
        with _Patch("ID_CONVENTION", {**P.ID_CONVENTION,
                                      ("english-cucumber", "Cucumber mosaic virus"):
                                          "cucumber-mosaic"}):
            _sprob(batch, "english-cucumber", "cucumber-mosaic-virus")["id"] = "cucumber-mosaic"
            _expect(self, "merging a single-pathogen problem",
                    lambda: P.check_scope_variant_ids_not_merged(batch, pre))

    def test_dropping_the_mint_is_refused(self):
        batch = P.staged()
        _sprob(batch, "edamame", "bacterial-blight")["id"] = "something-else"
        _expect(self, "no longer mints",
                lambda: P.check_scope_variant_ids_not_merged(batch, _pre()))

    def test_wider_id_vanishing_from_the_roster_is_refused(self):
        """If the id this mint was distinguished FROM is gone, the ruling must be re-made, not
        assumed still right."""
        pre = _pre()
        for c in pre["crops"]:
            for _f, p in P.problems(c):
                if p.get("id") == "cucumber-mosaic":
                    p["id"] = "gone"
        _expect(self, "It was the WIDER-scope id",
                lambda: P.check_scope_variant_ids_not_merged(P.staged(), pre))

    def test_holder_set_change_is_refused(self):
        pre = _pre()
        _crop(pre, "apple")["diseases"].append(
            {"name": "Ghost", "type": "bacterial", "id": "bacterial-blights"})
        _expect(self, "Its scope may have changed",
                lambda: P.check_scope_variant_ids_not_merged(P.staged(), pre))

    def test_wider_marker_lost_from_a_holder_is_refused(self):
        """`phaseolicola` is WHY the plural is a different disease. Lose it and the ruling is
        unsupported."""
        pre = _pre()
        p = _prob(pre, "pole-beans", "bacterial-blights")
        p["cause_seasoned"] = p["cause_seasoned"].replace("phaseolicola", "redacted")
        _expect(self, "That extra pathogen is WHY",
                lambda: P.check_scope_variant_ids_not_merged(P.staged(), pre))

    def test_own_marker_lost_from_the_batch_record_is_refused(self):
        pre = _pre()
        p = P.find_problem(pre, "edamame", "Bacterial blight")
        p["cause_seasoned"] = p["cause_seasoned"].replace("glycinea", "redacted")
        _expect(self, "which is the ground for minting",
                lambda: P.check_scope_variant_ids_not_merged(P.staged(), pre))

    def test_batch_record_growing_into_the_wider_scope_is_refused(self):
        """The scope difference is the whole ruling. If edamame's record starts naming the bean
        pathogen too, the two ids can no longer be told apart."""
        pre = _pre()
        p = P.find_problem(pre, "edamame", "Bacterial blight")
        p["cause_seasoned"] += " It is also caused by Pseudomonas syringae pv. phaseolicola."
        _expect(self, "can no longer be told apart by scope",
                lambda: P.check_scope_variant_ids_not_merged(P.staged(), pre))

    def test_missing_batch_record_is_refused(self):
        pre = _pre()
        d = _crop(pre, "edamame")
        d["diseases"] = [p for p in d["diseases"] if p.get("name") != "Bacterial blight"]
        _expect(self, "has no record to justify it",
                lambda: P.check_scope_variant_ids_not_merged(P.staged(), pre))

    def test_coverage_count_is_pinned(self):
        """The anti-vacuity branch: every pinned adjudication must actually be reached."""
        with _Patch("SCOPE_VARIANTS", ()):
            _expect(self, "scope-variant check covered",
                    lambda: P.check_scope_variant_ids_not_merged(P.staged(), _pre()))


class TemplateSiblingDivergence(unittest.TestCase):
    """The guard this batch's measurement SELECTED, and the batch 3 defect made mechanical."""

    def test_the_template_twins_are_real_and_counted(self):
        """9 twins measured: pumpkin's squash-bug, aphids and downy-mildew each against butternut,
        acorn and spaghetti squash."""
        pre = _pre()
        batch = P.staged()
        shipped = {}
        for c in pre["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                if p.get("control_ladder"):
                    shipped.setdefault(p["id"], []).append((c["slug"], p))
        twins = 0
        by = P.by_slug(pre)
        for c in CROPS:
            for fam in ("pests", "diseases"):
                for src, out in zip(by[c].get(fam) or [], batch[c].get(fam) or []):
                    for _s, q in shipped.get(out["id"], []):
                        if P.prose_key(src) == P.prose_key(q):
                            twins += 1
        self.assertEqual(twins, 9)

    def test_an_unpinned_divergence_on_identical_prose_is_refused(self):
        """pumpkin/squash-bug is a twin whose ladder currently MATCHES. Change it and the guard
        must refuse: identical prose cannot support two different ladders."""
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "pumpkin", "squash-bug")["control_ladder"].append(_rung("pyrethrin"))
        _expect(self, "shares byte-identical source prose",
                lambda: P.check_template_sibling_divergence(batch, pre))

    def test_a_pinned_divergence_of_the_wrong_shape_is_refused(self):
        pre = _pre()
        batch = P.staged()
        L = _sprob(batch, "pumpkin", "downy-mildew")["control_ladder"]
        _sprob(batch, "pumpkin", "downy-mildew")["control_ladder"] = [
            r for r in L if r["method"] != "wet_foliage_discipline"]
        _expect(self, "the pinned divergence never fired",
                lambda: P.check_template_sibling_divergence(batch, pre))

    def test_a_pinned_divergence_that_grows_is_refused(self):
        pre = _pre()
        batch = P.staged()
        _sprob(batch, "pumpkin", "downy-mildew")["control_ladder"].append(_rung("copper_fungicide"))
        _expect(self, "pinned +", lambda: P.check_template_sibling_divergence(batch, pre))

    def test_the_pin_is_the_wet_foliage_rung_and_the_siblings_are_the_ones_with_the_gap(self):
        """The shared prose says "avoid working among wet vines"; the method is exactly that action.
        Pumpkin carries the rung and the three squashes do not."""
        pre = _pre()
        d = _post(pre)
        self.assertIn("wet_foliage_discipline",
                      [r["method"] for r in _prob(d, "pumpkin", "downy-mildew")["control_ladder"]])
        for s in ("butternut-squash", "acorn-squash", "spaghetti-squash"):
            sib = _prob(pre, s, "downy-mildew")
            self.assertIn("working among wet vines", sib["prevention_seasoned"])
            self.assertNotIn("wet_foliage_discipline",
                             [r["method"] for r in sib["control_ladder"]])

    def test_vacuous_when_no_twins_exist(self):
        """ANTI-VACUITY BRANCH 1. Break every twin's prose and the guard must say so rather than
        pass on an empty comparison."""
        pre = _pre()
        for s in ("butternut-squash", "acorn-squash", "spaghetti-squash"):
            for _f, p in P.problems(_crop(pre, s)):
                p["cause_seasoned"] = "divergent text so no twin is detected"
        _expect(self, "no template twins found",
                lambda: P.check_template_sibling_divergence(P.staged(), pre))

    def test_vacuous_when_the_pin_is_unreachable(self):
        """ANTI-VACUITY BRANCH 2, and the one batch 21's harness would have caught. Leave the twins
        intact but make the PINNED problem's prose diverge, and the pin stops firing."""
        pre = _pre()
        for s in ("butternut-squash", "acorn-squash", "spaghetti-squash"):
            _prob(pre, s, "downy-mildew")["cause_seasoned"] = "divergent text for this driver"
        _expect(self, "the pinned divergence never fired",
                lambda: P.check_template_sibling_divergence(P.staged(), pre))

    def test_shipped_batch_is_clean(self):
        P.check_template_sibling_divergence(P.staged(), _pre())


class ProseEcho(unittest.TestCase):
    """Carried from batch 21 and re-measured before adoption: 0 hits over 270 notes against a
    5,351-note corpus. A REFUSAL-SPEC pass, and worth most where ladders converge."""

    def test_convergent_shapes_are_why_this_guard_still_earns_its_place(self):
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
        src = _prob(pre, "butternut-squash", "squash-bug")["control_ladder"][0]["note_beginner"]
        _sprob(batch, "pumpkin", "squash-vine-borer")["control_ladder"][0]["note_beginner"] = src
        _expect(self, "verbatim echo of", lambda: P.check_no_shipped_prose_echo(batch, pre))

    def test_sentence_level_echo_refused(self):
        pre = _pre()
        batch = P.staged()
        src = _prob(pre, "butternut-squash", "squash-bug")["control_ladder"][0]["note_seasoned"]
        sent = P.sentences(src)[0]
        r = _sprob(batch, "pumpkin", "squash-vine-borer")["control_ladder"][0]
        r["note_seasoned"] = "A fresh opening clause for this driver. " + sent[0].upper() + sent[1:]
        _expect(self, "echoes a shipped sentence", lambda: P.check_no_shipped_prose_echo(batch, pre))

    def test_vacuous_without_a_shipped_corpus(self):
        """ANTI-VACUITY BRANCH 1."""
        pre = _pre()
        for c in pre["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                p.pop("control_ladder", None)
        _expect(self, "no shipped rung prose",
                lambda: P.check_no_shipped_prose_echo(P.staged(), pre))

    def test_vacuous_without_batch_notes(self):
        """ANTI-VACUITY BRANCH 2 -- the shape that had no driver in batch 21."""
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                p["control_ladder"] = []
        _expect(self, "no batch notes scanned",
                lambda: P.check_no_shipped_prose_echo(batch, _pre()))

    def test_shipped_batch_is_clean(self):
        P.check_no_shipped_prose_echo(P.staged(), _pre())


class ProseDiscipline(unittest.TestCase):
    def test_temperature_figure_refused(self):
        batch = P.staged()
        _sprob(batch, "pumpkin", "powdery-mildew")["control_ladder"][0]["note_beginner"] += \
            " Apply below 90°F."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_degrees_word_refused(self):
        batch = P.staged()
        _sprob(batch, "pumpkin", "powdery-mildew")["control_ladder"][0]["note_seasoned"] += \
            " Hold off above 90 degrees."
        _expect(self, "states a temperature", lambda: P.check_no_temperature_figures(batch))

    def test_temperature_guard_vacuity_is_driven(self):
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                p["control_ladder"] = []
        _expect(self, "no notes scanned for temperatures",
                lambda: P.check_no_temperature_figures(batch))

    def test_ladder_vocabulary_refused(self):
        batch = P.staged()
        _sprob(batch, "edamame", "white-mold")["control_ladder"][0]["note_beginner"] += \
            " This rung comes first."
        _expect(self, "uses internal vocabulary", lambda: P.check_no_ladder_vocabulary(batch))

    def test_vocabulary_guard_vacuity_is_driven(self):
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                p["control_ladder"] = []
        _expect(self, "no notes scanned for vocabulary",
                lambda: P.check_no_ladder_vocabulary(batch))

    def test_shipped_batch_is_clean(self):
        P.check_no_temperature_figures(P.staged())
        P.check_no_ladder_vocabulary(P.staged())

    def test_hygiene_catches_each_banned_token(self):
        for bad, frag in (("It is completely safe.", "absolute:completely"),
                          ("Always spray weekly.", "absolute:always"),
                          ("Never water overhead.", "absolute:never"),
                          ("It is harmless to bees.", "absolute:harmless"),
                          ("Results are guaranteed.", "absolute:guaranteed"),
                          ("Use an em dash — here.", "em/en dash")):
            self.assertIn(frag, P.hygiene(bad), bad)
        self.assertEqual(P.hygiene("A clean sentence about coverage and timing."), [])

    def test_shipped_notes_pass_hygiene(self):
        batch = P.staged()
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                for r in p["control_ladder"]:
                    for f in P.ADVICE_FIELDS:
                        self.assertEqual(P.hygiene(r[f]), [], (c, p["id"], r["method"], f))


class ValidateBatch(unittest.TestCase):
    def _cm(self):
        return _pre()["control_methods"]

    def test_unknown_method_refused(self):
        batch = P.staged()
        _sprob(batch, "pumpkin", "squash-bug")["control_ladder"][0]["method"] = "no_such_method"
        _expect(self, "unknown method", lambda: P.validate_batch(batch, self._cm()))

    def test_duplicate_method_refused(self):
        batch = P.staged()
        L = _sprob(batch, "pumpkin", "squash-bug")["control_ladder"]
        L.append(_rung(L[0]["method"]))
        _expect(self, "duplicate method", lambda: P.validate_batch(batch, self._cm()))

    def test_tier_decrease_refused(self):
        batch = P.staged()
        p = _sprob(batch, "english-cucumber", "powdery-mildew")
        p["control_ladder"] = list(reversed(p["control_ladder"]))
        _expect(self, "tier decrease", lambda: P.validate_batch(batch, self._cm()))

    def test_applies_to_incoherence_refused(self):
        """`weed_host_control` cannot reach `viral`, which is exactly why CMV's weed-reservoir
        advice had to be placed elsewhere."""
        batch = P.staged()
        _sprob(batch, "english-cucumber", "cucumber-mosaic-virus")["control_ladder"].insert(
            0, _rung("weed_host_control"))
        _expect(self, "illegal for type", lambda: P.validate_batch(batch, self._cm()))

    def test_identical_registers_refused(self):
        batch = P.staged()
        r = _sprob(batch, "edamame", "white-mold")["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        _expect(self, "identical registers", lambda: P.validate_batch(batch, self._cm()))

    def test_missing_note_refused(self):
        batch = P.staged()
        _sprob(batch, "edamame", "white-mold")["control_ladder"][0]["note_seasoned"] = "   "
        _expect(self, "missing note_seasoned", lambda: P.validate_batch(batch, self._cm()))

    def test_hygiene_violation_refused(self):
        batch = P.staged()
        _sprob(batch, "edamame", "white-mold")["control_ladder"][0]["note_beginner"] = \
            "This approach is completely reliable in every season and needs no checking."
        _expect(self, "absolute:completely", lambda: P.validate_batch(batch, self._cm()))

    def test_extra_rung_key_refused(self):
        batch = P.staged()
        _sprob(batch, "edamame", "white-mold")["control_ladder"][0]["severity"] = "high"
        _expect(self, "rung carries", lambda: P.validate_batch(batch, self._cm()))

    def test_material_outside_the_pinned_set_refused(self):
        batch = P.staged()
        _sprob(batch, "pumpkin", "squash-bug")["control_ladder"].append(_rung("pyrethrin"))
        _expect(self, "outside MATERIAL_OK", lambda: P.validate_batch(batch, self._cm()))

    def test_material_on_a_problem_with_none_refused(self):
        batch = P.staged()
        _sprob(batch, "pumpkin", "bacterial-wilt")["control_ladder"].append(_rung("copper_fungicide"))
        _expect(self, "outside MATERIAL_OK", lambda: P.validate_batch(batch, self._cm()))

    def test_empty_ladder_refused(self):
        batch = P.staged()
        _sprob(batch, "pumpkin", "squash-bug")["control_ladder"] = []
        _expect(self, "empty ladder", lambda: P.validate_batch(batch, self._cm()))

    def test_missing_type_refused(self):
        batch = P.staged()
        _sprob(batch, "pumpkin", "squash-bug")["type"] = None
        _expect(self, "missing type", lambda: P.validate_batch(batch, self._cm()))

    def test_problem_count_refused(self):
        batch = P.staged()
        batch["pumpkin"]["pests"].pop()
        _expect(self, "problems, expected", lambda: P.validate_batch(batch, self._cm()))

    def test_per_crop_rung_count_refused(self):
        """Driven by moving the PIN, not by mutating a ladder: appending a rung trips the earlier
        duplicate-method or MATERIAL_OK check first and never reaches this branch."""
        with _Patch("EXPECTED_RUNGS", dict(P.EXPECTED_RUNGS, pumpkin=41)):
            _expect(self, "rungs, expected", lambda: P.validate_batch(P.staged(), self._cm()))

    def test_total_rung_count_refused(self):
        """Per-crop counts all agree; only the total is wrong, so this reaches the last branch."""
        with _Patch("TOTAL_RUNGS", TOTAL_RUNGS - 1):
            _expect(self, "rungs total, expected",
                    lambda: P.validate_batch(P.staged(), self._cm()))

    def test_shipped_batch_is_clean(self):
        P.validate_batch(P.staged(), self._cm())

    def test_material_table_is_exactly_the_material_rungs(self):
        """A COVERAGE assertion: every material rung is in the table and the table has no entry
        that no rung reaches."""
        batch = P.staged()
        cm = self._cm()
        seen = {}
        for c in CROPS:
            for _f, p in P.problems(batch[c]):
                mats = tuple(r["method"] for r in p["control_ladder"]
                             if cm[r["method"]]["tier"] in P.MATERIAL_TIERS)
                if mats:
                    seen[(c, p["id"])] = mats
        self.assertEqual(seen, dict(P.MATERIAL_OK))


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
            lambda d: d["control_methods"]["sulfur"].__setitem__("tier", "cultural"),
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

    def test_apply_writes_the_pinned_post_sha(self):
        raw = promote_fixture.pre_state(P.BASE_SHA)
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(raw)
        try:
            _run_main(path, apply_=True)
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), POST_SHA)
        finally:
            os.unlink(path)

    def test_one_serializer(self):
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_post(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_roster_grows_by_three(self):
        pre, post = _pre(), None
        post = _post(pre)

        def laddered(d):
            return sum(1 for c in d["crops"]
                       if any("control_ladder" in p for _f, p in P.problems(c)))
        self.assertEqual(laddered(post) - laddered(pre), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
