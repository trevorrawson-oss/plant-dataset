#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch23.py. Base b118f19d (the thin-ladder backfill).

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are LIVE is `MainWiringIsDriven`
plus tools/mutate_pla8_batch23_suite.py.

Every driver asserts the ONE message its branch emits -- not a shared fragment. The backfill lost
time to three drivers all asserting "expected 7", a constant that appears in two different guards'
messages, so either guard could have been disabled with the suite still green.

Every anti-vacuity branch has its own driver. Batch 21's two harness survivors were both
anti-vacuity branches with no driver, in a suite that looked complete at 71 green tests.

WHAT IS NEW versus batches 17-22:

* `NoPrecedentCopy` drives the guard this batch's measurement SELECTED. Batch 22's
  `check_template_sibling_divergence` is dropped because roots has ZERO template twins; the guard
  that replaces it protects the risk this session created by pointing every authoring agent at a
  precedent crop for 13 reused ids.
* `TemplateTwinPremise` drives the ASSERTED vacuity of the dropped guard. Dropping a guard silently
  is how a premise stops being checked.
* `TemperatureWarranted` drives a BAN converted into a PROVENANCE check. Batch 22 refused any
  temperature figure and its crops contained none, so the ban was a refusal-spec pass; roots
  contains five, all sourced, so the ban would have refused verified content.
* `StemmedIdScan` drives the singular/plural class that an exact-id check cannot see -- the miss
  that let two ids through in batch 22.
"""
import copy, difflib, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch23 as P  # noqa: E402

CROPS = ("parsnip", "potato", "sweet-potato")
TOTAL_RUNGS = 87
TOTAL_PROBLEMS = 22
POST_SHA = "e6c986e38e15a0219d64c805cfc11a8786e974320f915e1dd35e6031422f0419"
BYSTANDER = "carrot"      # parsnip's nearest laddered relative; 3 shared ids


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _staged():
    return copy.deepcopy(P.staged())


def _crop(data, slug):
    return next(c for c in data["crops"] if c.get("slug") == slug)


def _sprob(batch, slug, pid):
    for fam in ("pests", "diseases"):
        for p in batch[slug].get(fam) or []:
            if p.get("id") == pid:
                return p
    raise AssertionError("staged %s/%s not found" % (slug, pid))


def _pre_prob(data, slug, name):
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("name") == name:
                return p
    raise AssertionError("pre %s/%r not found" % (slug, name))


class _Patch:
    """Patch a module attribute for the duration of a driver."""
    def __init__(self, name, value):
        self.n, self.v = name, value

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(P, self.n, self.old)
        return False


def _with_batch(batch):
    return _Patch("staged", lambda: batch)


_UNIQ = [0]


def _rung(m):
    """Clean rung prose: no absolutes, no temperature figures, no ladder vocabulary, and long
    enough that the echo scan's 40-character sentence floor would see it if it were an echo."""
    _UNIQ[0] += 1
    return {"method": m,
            "note_beginner": "Injected beginner text number %d for this driver only." % _UNIQ[0],
            "note_seasoned": "Injected seasoned wording number %d, which differs materially."
                             % _UNIQ[0]}


def _expect(case, fragment, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(fragment, str(cm.exception))


# ---------------------------------------------------------------- the happy path
class CleanRun(unittest.TestCase):
    def test_clean_pre_state_passes_and_is_the_pinned_shape(self):
        d = _pre()
        self.assertEqual(hashlib.sha256(P.serialize(d)).hexdigest(), P.BASE_SHA)
        batch = P.check(d)
        self.assertEqual(sum(len(batch[c].get(f) or []) for c in CROPS
                             for f in ("pests", "diseases")), TOTAL_PROBLEMS)

    def test_apply_produces_the_pinned_post_sha(self):
        d = _pre()
        P.apply_to(d)
        self.assertEqual(hashlib.sha256(P.serialize(d)).hexdigest(), POST_SHA)

    def test_serialize_is_compact_and_unescaped(self):
        blob = P.serialize({"a": "café", "b": [1, 2]})
        self.assertEqual(blob, '{"a":"café","b":[1,2]}'.encode("utf-8"))

    def test_counts_are_pinned_not_derived(self):
        self.assertEqual(sum(P.EXPECTED_PROBLEMS.values()), TOTAL_PROBLEMS)
        self.assertEqual(sum(P.EXPECTED_RUNGS.values()), P.TOTAL_RUNGS)
        self.assertEqual(P.TOTAL_RUNGS, TOTAL_RUNGS)


# ---------------------------------------------------------------- pre-state premise
class FullSchemaPremise(unittest.TestCase):
    def test_missing_full_schema_field_refuses(self):
        d = _pre()
        del _pre_prob(d, "potato", "Late blight")["cause_seasoned"]
        _expect(self, "missing full-schema field cause_seasoned", lambda: P.check(d))

    def test_note_schema_field_present_refuses(self):
        d = _pre()
        _pre_prob(d, "parsnip", "Damping-off")["note"] = "x"
        _expect(self, "carries note-schema field note", lambda: P.check(d))

    def test_missing_severity_refuses(self):
        d = _pre()
        del _pre_prob(d, "sweet-potato", "Black rot")["severity"]
        _expect(self, "has no severity", lambda: P.check(d))

    def test_already_laddered_target_refuses(self):
        d = _pre()
        _pre_prob(d, "potato", "Common scab")["control_ladder"] = [_rung("crop_rotation")]
        _expect(self, "is ALREADY laddered", lambda: P.check(d))

    def test_pre_existing_id_refuses(self):
        d = _pre()
        _pre_prob(d, "potato", "Wireworms")["id"] = "wireworms"
        _expect(self, "already carries id", lambda: P.check(d))

    def test_missing_sources_refuses(self):
        d = _pre()
        _pre_prob(d, "parsnip", "Aster yellows")["sources"] = []
        _expect(self, "missing sources/anchoring_urls", lambda: P.check(d))

    def test_problem_count_drift_refuses(self):
        """Asserts the WHOLE sentence. "problems, expected" also occurs in the coverage-count
        message, so the short fragment let either branch satisfy the other's driver and BOTH
        mutations survived."""
        d = _pre()
        _crop(d, "parsnip")["pests"].pop()
        _expect(self, "parsnip has 5 problems, expected 6", lambda: P.check(d))

    def test_schema_coverage_count_is_pinned(self):
        """The coverage count's own driver. It is the guard's ANTI-VACUITY branch: if the crop loop
        never runs, nothing was scanned and the premise is unproven."""
        d = _pre()
        with _Patch("CROPS", ()):
            _expect(self, "schema premise scanned 0 problems, expected 22",
                    lambda: P.check_full_schema_premise(P.by_slug(d)))

    def test_crop_absent_refuses(self):
        d = _pre()
        d["crops"] = [c for c in d["crops"] if c.get("slug") != "parsnip"]
        _expect(self, "not on the roster", lambda: P.check(d))


class UniformCoarseTypeUpgrade(unittest.TestCase):
    def test_pre_state_type_not_coarse_refuses(self):
        d = _pre()
        _pre_prob(d, "potato", "Flea beetles")["type"] = "insect"
        _expect(self, "expected coarse", lambda: P.check(d))

    def test_staged_type_off_the_pin_refuses(self):
        d, b = _pre(), _staged()
        _sprob(b, "parsnip", "aster-yellows")["type"] = "viral"
        with _with_batch(b):
            _expect(self, "staged type 'viral', pinned 'bacterial'", lambda: P.check(d))

    def test_staged_type_off_the_pin_is_caught_before_anything_else(self):
        d, b = _pre(), _staged()
        _sprob(b, "potato", "wireworms")["type"] = "pest"
        with _with_batch(b):
            _expect(self, "staged type 'pest', pinned 'insect'", lambda: P.check(d))

    def test_type_left_at_the_coarse_default_refuses(self):
        """Reachable only when the PIN ITSELF is coarse: otherwise the pin comparison fires first
        and this branch is dead. The mutation survived until this driver existed."""
        d, b = _pre(), _staged()
        _sprob(b, "potato", "wireworms")["type"] = "pest"
        pins = dict(P.ID_CONVENTION)
        name, pid, _t, dec = pins[("potato", "pests", 3)]
        pins[("potato", "pests", 3)] = (name, pid, "pest", dec)
        with _with_batch(b), _Patch("ID_CONVENTION", pins):
            _expect(self, "type was not upgraded off the coarse default", lambda: P.check(d))

    def test_type_upgrade_coverage_count_is_pinned(self):
        d, b = _pre(), _staged()
        with _Patch("CROPS", ()):
            _expect(self, "type upgrade scanned 0, expected 22",
                    lambda: P.check_uniform_coarse_type_upgrade(b, P.by_slug(d)))

    def test_length_mismatch_refuses(self):
        d, b = _pre(), _staged()
        b["parsnip"]["pests"].pop()
        with _with_batch(b):
            _expect(self, "staged vs", lambda: P.check(d))


# ---------------------------------------------------------------- ids
class Ids(unittest.TestCase):
    def test_id_drift_from_the_pin_refuses(self):
        d, b = _pre(), _staged()
        _sprob(b, "potato", "late-blight")["id"] = "potato-late-blight"
        with _with_batch(b):
            _expect(self, "pinned 'late-blight'", lambda: P.check(d))

    def test_canonical_name_drift_refuses(self):
        d = _pre()
        _pre_prob(d, "potato", "Early blight")["name"] = "Early Blight"
        _expect(self, "canonical name", lambda: P.check(d))

    def test_duplicate_id_within_a_crop_refuses(self):
        """The pin table is patched to expect the duplicate too, so the positional pin check passes
        and the WITHIN-CROP uniqueness branch is the one that fires."""
        d, b = _pre(), _staged()
        _sprob(b, "potato", "early-blight")["id"] = "late-blight"
        pins = dict(P.ID_CONVENTION)
        name, _pid, t, dec = pins[("potato", "diseases", 1)]
        pins[("potato", "diseases", 1)] = (name, "late-blight", t, dec)
        with _with_batch(b), _Patch("ID_CONVENTION", pins):
            _expect(self, "duplicate problem ids", lambda: P.check(d))

    def test_pin_coverage_against_the_batch_is_asserted(self):
        """The batch carrying a position the pin table does not cover must refuse. The old form of
        this assertion compared ID_CONVENTION to a set built by iterating ID_CONVENTION, so it
        could never fail; the mutation harness proved it by surviving."""
        d, b = _pre(), _staged()
        extra = copy.deepcopy(b["parsnip"]["pests"][0])
        extra["id"] = "extra-injected-problem"
        b["parsnip"]["pests"].append(extra)
        _expect(self, "the pin table covers 22 positions but the batch holds 23",
                lambda: P.check_ids(b, P.by_slug(d)))

    def test_pin_table_size_is_asserted(self):
        """Driven against check_ids directly: a short table raises a KeyError in the type-upgrade
        guard first, which would report the wrong thing."""
        d, b = _pre(), _staged()
        short = {k: v for i, (k, v) in enumerate(sorted(P.ID_CONVENTION.items())) if i}
        with _Patch("ID_CONVENTION", short):
            _expect(self, "pin table holds 21 entries, expected 22",
                    lambda: P.check_ids(b, P.by_slug(d)))


class StemmedIdScan(unittest.TestCase):
    """The singular/plural class. An exact-id check passes an id that merely RESEMBLES a live one,
    which is how two ids got through in batch 22."""

    def test_unpinned_stem_variant_refuses(self):
        """Where the roster holds two stem-equal variants of one name, which one the batch takes is
        a DECISION. An unadjudicated pick must refuse. The pin table is patched to match the id so
        the positional pin check passes and the stem scan is the branch under test."""
        d, b = _pre(), _staged()
        _sprob(b, "parsnip", "parsnip-leafminer")["id"] = "aphid"   # stem-equal to `aphids` (x59)
        pins = dict(P.ID_CONVENTION)
        name, _pid, t, dec = pins[("parsnip", "pests", 1)]
        pins[("parsnip", "pests", 1)] = (name, "aphid", t, dec)
        with _with_batch(b), _Patch("ID_CONVENTION", pins):
            _expect(self, "adjudicate which the batch takes and pin it", lambda: P.check(d))

    def test_the_real_flea_beetle_variant_is_adjudicated_not_ignored(self):
        """swiss-chard's singular `flea-beetle` is stem-equal to the x32 `flea-beetles` this batch
        takes on two crops. That is a real pair and it is PINNED, not skipped."""
        self.assertIn(("flea-beetles", "flea-beetle"), P.STEM_VARIANT_PINS)
        self.assertEqual(P.EXPECTED_STEM_VARIANT_HITS, 2)
        P.check(_pre())

    def test_stem_variant_hit_count_is_pinned(self):
        with _Patch("EXPECTED_STEM_VARIANT_HITS", 3):
            _expect(self, "stem-variant pairs adjudicated, pinned 3", lambda: P.check(_pre()))

    def test_removing_the_pin_refuses_the_shipped_batch(self):
        """The pin is load-bearing: without it the real batch stops passing."""
        with _Patch("STEM_VARIANT_PINS", {}):
            _expect(self, "Two variants of one name exist", lambda: P.check(_pre()))

    def test_stemmer_matches_singular_and_plural(self):
        """The first stemmer turned `beetles` into `beetl` while `beetle` stayed `beetle`, so the
        guard silently skipped the exact pair it exists for."""
        self.assertEqual(P._stem_key("flea-beetles"), P._stem_key("flea-beetle"))
        self.assertEqual(P._stem_key("carrot-rust-flies"), P._stem_key("carrot-rust-fly"))
        self.assertNotEqual(P._stem_key("aphids"), P._stem_key("aphids-virus-vectors"))

    def test_scope_pin_whose_id_is_already_live_refuses(self):
        """A scope pin claims an id was minted as DISTINCT. If that id is in fact live on the
        roster the claim is false, and the promote must say so rather than pass on a name match."""
        pins = dict(P.ID_SCOPE_PINS)
        pins["flea-beetles"] = ("aphids", "Flea beetles", None)
        with _Patch("ID_SCOPE_PINS", pins):
            _expect(self, "was minted as distinct but already exists on the roster",
                    lambda: P.check(_pre()))

    def test_stale_taxon_reuse_pin_refuses(self):
        """A TAXON_REUSE_PINS entry naming an id this batch does not take is a stale pin."""
        pins = dict(P.TAXON_REUSE_PINS)
        pins[("potato", "ghost-id")] = ("beet", "some phrase")
        with _Patch("TAXON_REUSE_PINS", pins):
            _expect(self, "taxon-reuse pin 'ghost-id' not in the batch",
                    lambda: P.check(_pre()))

    def test_precedent_crop_losing_the_reused_id_refuses(self):
        """common-scab is REUSED on the strength of beet holding it. If beet stops holding it, the
        reuse has no anchor left and the promote must refuse rather than assume."""
        d = _pre()
        for c in d["crops"]:
            if c["slug"] != "beet":
                continue
            for f in ("pests", "diseases"):
                for p in c.get(f) or []:
                    if p.get("id") == "common-scab":
                        p["id"] = "beet-scab-renamed"
        _expect(self, "no longer holds 'common-scab'", lambda: P.check(d))

    def test_scope_pin_not_in_the_batch_refuses(self):
        with _Patch("ID_SCOPE_PINS", dict(P.ID_SCOPE_PINS, **{"ghost-id": ("aphids", "x", None)})):
            _expect(self, "is not in the batch; the pin is stale", lambda: P.check(_pre()))

    def test_resembled_id_gone_from_the_roster_refuses(self):
        d = _pre()
        for c in d["crops"]:
            for f in ("pests", "diseases"):
                for p in c.get(f) or []:
                    if p.get("id") == "aphids":
                        p["id"] = "aphids-renamed"
        _expect(self, "can no longer be checked", lambda: P.check(d))

    def test_taxon_collision_reason_gone_refuses(self):
        """If the brassicas stop naming Xanthomonas, the reason to keep sweet-potato-black-rot
        separate is unproven and the promote must say so rather than pass on a name match."""
        d = _pre()
        for c in d["crops"]:
            for f in ("pests", "diseases"):
                for p in c.get(f) or []:
                    if p.get("id") == "black-rot":
                        for k in P.PROSE_FIELDS:
                            if p.get(k):
                                p[k] = p[k].replace("Xanthomonas", "REDACTED")
        _expect(self, "the taxon collision that justified", lambda: P.check(d))

    def test_own_scope_reason_gone_refuses(self):
        d = _pre()
        p = _pre_prob(d, "potato", "Aphids and the viruses they spread")
        p["cause_seasoned"] = p["cause_seasoned"].replace(
            "Virus pressure, not the feeding itself", "They feed on the foliage")
        _expect(self, "is not in its own", lambda: P.check(d))

    def test_taxon_reuse_phrase_gone_refuses(self):
        """common-scab is REUSED because beet's prose says it is the same organism. If beet stops
        saying so, the reuse is unproven."""
        d = _pre()
        for c in d["crops"]:
            for f in ("pests", "diseases"):
                for p in c.get(f) or []:
                    if p.get("id") == "common-scab" and c["slug"] == "beet":
                        p["cause_seasoned"] = p["cause_seasoned"].replace(
                            "the same organism that causes potato scab", "a soil organism")
        _expect(self, "has stopped being true", lambda: P.check(d))


# ---------------------------------------------------------------- the chosen guard
class NoPrecedentCopy(unittest.TestCase):
    """The guard this batch's measurement selected. Threshold 0.70 sits just above a measured
    independent-authoring ceiling of 0.644 over 207 singleton pairs."""

    def test_a_rung_copied_from_its_precedent_crop_refuses(self):
        d, b = _pre(), _staged()
        beet = None
        for c in d["crops"]:
            if c["slug"] != "beet":
                continue
            for p in c.get("diseases") or []:
                if p.get("id") == "common-scab":
                    beet = [r for r in p["control_ladder"] if r["method"] == "even_watering"][0]
        self.assertIsNotNone(beet, "beet/common-scab/even_watering is the precedent this leans on")
        rung = [r for r in _sprob(b, "potato", "common-scab")["control_ladder"]
                if r["method"] == "even_watering"][0]
        rung["note_beginner"] = beet["note_beginner"]
        rung["note_seasoned"] = beet["note_seasoned"]
        with _with_batch(b):
            _expect(self, "similar to beet's rung for the same problem", lambda: P.check(d))

    def test_the_shipped_batch_is_well_under_the_threshold(self):
        d = _pre()
        compared, worst = P.check_no_precedent_copy(P.staged(), d)
        self.assertGreaterEqual(compared, 200, "13 reused ids should reach hundreds of rungs")
        self.assertLess(worst[0], 0.684,
                        "the shipped batch must sit under the measured independent ceiling")

    def test_guard_is_not_vacuous_and_says_so(self):
        """If no reused id reaches a precedent, the guard is a zero with extra steps."""
        d = _pre()
        for c in d["crops"]:
            if c["slug"] in CROPS:
                continue
            for f in ("pests", "diseases"):
                for p in c.get(f) or []:
                    p["control_ladder"] = None
        _expect(self, "made 0 comparisons; it is vacuous",
                lambda: P.check_no_precedent_copy(P.staged(), d))

    def test_threshold_is_the_measured_value(self):
        self.assertEqual(P.PRECEDENT_COPY_THRESHOLD, 0.70)

    def test_metric_is_autojunk_free_and_per_register(self):
        """The regression this guard shipped with once. difflib's autojunk deflates sequences over
        200 characters, and averaging the registers dilutes a single copied one. A 300-character
        near-copy must score high, not average away."""
        a = ("Steady moisture through tuber formation, the 4 to 9 weeks after planting, is the "
             "in-season half of scab control and the half still available once the crop is in the "
             "ground; dry conditions while tubers size are what favor infection. The pH decision "
             "is settled before planting, this one is made every week.")
        b = ("Steady moisture through root sizing is the in-season half of scab control, and it is "
             "the half still available once the crop is in the ground. The pH decision is made "
             "before planting; this one is made every week.")
        self.assertLess(difflib.SequenceMatcher(None, a, b).ratio(), 0.40,
                        "default difflib hides this copy -- that is the bug")
        self.assertGreater(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(), 0.70,
                           "the corrected metric must see it")


class TemplateTwinPremise(unittest.TestCase):
    """Batch 22's divergence guard is DROPPED as vacuous. The vacuity is ASSERTED, not assumed."""

    def test_a_template_twin_appearing_refuses_and_names_the_dropped_guard(self):
        d = _pre()
        src = _pre_prob(d, "parsnip", "Damping-off")
        twin = _pre_prob(d, BYSTANDER, "Damping-off")
        for f in P.PROSE_FIELDS:
            twin[f] = src.get(f)
        _expect(self, "check_template_sibling_divergence", lambda: P.check(d))

    def test_premise_is_not_vacuous(self):
        d = _pre()
        d["crops"] = [c for c in d["crops"] if c.get("slug") in CROPS]
        _expect(self, "the twin premise is unproven",
                lambda: P.check_no_template_twins_premise(P.by_slug(d), d))


class NoShippedProseEcho(unittest.TestCase):
    def test_whole_note_echo_refuses(self):
        d, b = _pre(), _staged()
        echo = None
        for c in d["crops"]:
            if c["slug"] in CROPS:
                continue
            for f in ("pests", "diseases"):
                for p in c.get(f) or []:
                    for r in p.get("control_ladder") or []:
                        if echo is None and len(r.get("note_beginner") or "") > 60:
                            echo = r["note_beginner"]
        _sprob(b, "parsnip", "damping-off")["control_ladder"][0]["note_beginner"] = echo
        with _with_batch(b):
            _expect(self, "is a verbatim echo of", lambda: P.check(d))

    def test_sentence_echo_refuses(self):
        d, b = _pre(), _staged()
        sent = None
        for c in d["crops"]:
            if c["slug"] in CROPS:
                continue
            for f in ("pests", "diseases"):
                for p in c.get(f) or []:
                    for r in p.get("control_ladder") or []:
                        for s in P.sentences(r.get("note_seasoned") or ""):
                            if sent is None and len(s) > 60:
                                sent = r["note_seasoned"]
        rung = _sprob(b, "parsnip", "damping-off")["control_ladder"][0]
        rung["note_beginner"] = "A short unique lead for this driver. " + \
                                P.sentences(sent)[0].capitalize()
        with _with_batch(b):
            _expect(self, "echoes a shipped sentence from", lambda: P.check(d))

    def test_no_batch_notes_is_vacuous_and_refuses(self):
        d, b = _pre(), _staged()
        for c in CROPS:
            for f in ("pests", "diseases"):
                for p in b[c].get(f) or []:
                    p["control_ladder"] = []
        with _with_batch(b):
            _expect(self, "no batch notes scanned", lambda: P.check_no_shipped_prose_echo(b, d))

    def test_no_shipped_corpus_is_vacuous_and_refuses(self):
        d, b = _pre(), _staged()
        for c in d["crops"]:
            for f in ("pests", "diseases"):
                for p in c.get(f) or []:
                    p["control_ladder"] = None
        _expect(self, "no shipped rung prose found",
                lambda: P.check_no_shipped_prose_echo(b, d))


class TemperatureWarranted(unittest.TestCase):
    """Batch 22 BANNED temperature figures. Roots contains five, every one sourced, so the ban is
    converted into a provenance check."""

    def test_unwarranted_figure_refuses(self):
        d, b = _pre(), _staged()
        rung = _sprob(b, "parsnip", "damping-off")["control_ladder"][0]
        rung["note_beginner"] = rung["note_beginner"] + " Hold the bed at 137°F throughout."
        with _with_batch(b):
            _expect(self, "appears neither in the problem's own prose nor in the method's",
                    lambda: P.check(d))

    def test_a_figure_from_the_problems_own_prose_is_allowed(self):
        d = _pre()
        P.check_temperature_figures_warranted(P.staged(), P.by_slug(d), d["control_methods"])

    def test_removing_a_sourced_figure_refuses_on_the_pinned_count(self):
        d, b = _pre(), _staged()
        for r in _sprob(b, "parsnip", "damping-off")["control_ladder"]:
            for k in P.ADVICE_FIELDS:
                r[k] = r[k].replace("50°F", "warm enough")
        with _with_batch(b):
            _expect(self, "temperature figures, pinned 5", lambda: P.check(d))

    def test_expected_count_is_pinned(self):
        self.assertEqual(P.EXPECTED_TEMP_FIGURES, 5)


class LadderVocabulary(unittest.TestCase):
    def test_internal_vocabulary_refuses(self):
        d, b = _pre(), _staged()
        rung = _sprob(b, "potato", "wireworms")["control_ladder"][0]
        rung["note_seasoned"] = "This is the first rung of the sequence for this driver only."
        with _with_batch(b):
            _expect(self, "uses internal vocabulary", lambda: P.check(d))

    def test_guard_is_not_vacuous(self):
        b = _staged()
        for c in CROPS:
            for f in ("pests", "diseases"):
                for p in b[c].get(f) or []:
                    p["control_ladder"] = []
        _expect(self, "no notes scanned for vocabulary",
                lambda: P.check_no_ladder_vocabulary(b))


# ---------------------------------------------------------------- ladder validity
class ValidateBatch(unittest.TestCase):
    def test_unknown_method_refuses(self):
        d, b = _pre(), _staged()
        _sprob(b, "potato", "wireworms")["control_ladder"][0]["method"] = "not_a_method"
        with _with_batch(b):
            _expect(self, "names unknown method", lambda: P.check(d))

    def test_tier_inversion_refuses(self):
        d, b = _pre(), _staged()
        lad = _sprob(b, "potato", "aphids-virus-vectors")["control_ladder"]
        lad.insert(0, _rung("insecticidal_soap"))   # soft_chemical ahead of cultural
        _sprob(b, "potato", "aphids-virus-vectors")["control_ladder"] = lad
        with _with_batch(b):
            _expect(self, "tier decreases at", lambda: P.check(d))

    def test_applies_to_incoherence_refuses(self):
        d, b = _pre(), _staged()
        # certified_clean_stock cannot reach an insect-typed problem: the batch's own r10 finding
        lad = _sprob(b, "sweet-potato", "sweet-potato-weevil")["control_ladder"]
        lad.insert(0, _rung("certified_clean_stock"))
        with _with_batch(b):
            _expect(self, "does not reach it", lambda: P.check(d))

    def test_identical_registers_refuse(self):
        d, b = _pre(), _staged()
        r = _sprob(b, "parsnip", "aster-yellows")["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        with _with_batch(b):
            _expect(self, "registers are identical", lambda: P.check(d))

    def test_duplicate_method_in_one_ladder_refuses(self):
        d, b = _pre(), _staged()
        p = _sprob(b, "parsnip", "aster-yellows")
        p["control_ladder"] = p["control_ladder"] + [dict(p["control_ladder"][0])]
        with _with_batch(b):
            _expect(self, "repeats method", lambda: P.check(d))

    def test_empty_ladder_refuses(self):
        d, b = _pre(), _staged()
        # aster-yellows carries no temperature figure, so the pinned-count guard does not mask this
        _sprob(b, "parsnip", "aster-yellows")["control_ladder"] = []
        with _with_batch(b):
            _expect(self, "has an empty ladder", lambda: P.check(d))

    def test_missing_register_refuses(self):
        d, b = _pre(), _staged()
        del _sprob(b, "potato", "wireworms")["control_ladder"][0]["note_seasoned"]
        with _with_batch(b):
            _expect(self, "missing a register", lambda: P.check(d))

    def test_unexpected_rung_key_refuses(self):
        d, b = _pre(), _staged()
        _sprob(b, "potato", "wireworms")["control_ladder"][0]["severity"] = "high"
        with _with_batch(b):
            _expect(self, "unexpected rung keys", lambda: P.check(d))

    def test_absolute_claim_refuses(self):
        d, b = _pre(), _staged()
        r = _sprob(b, "potato", "wireworms")["control_ladder"][0]
        r["note_beginner"] = "This will completely clear the pest from the bed for good."
        with _with_batch(b):
            _expect(self, "absolute:completely", lambda: P.check(d))

    def test_em_dash_refuses(self):
        d, b = _pre(), _staged()
        r = _sprob(b, "potato", "wireworms")["control_ladder"][0]
        r["note_beginner"] = "Work the bed after harvest — it exposes the larvae to weather."
        with _with_batch(b):
            _expect(self, "em/en dash", lambda: P.check(d))

    def test_per_crop_rung_count_drift_refuses(self):
        d, b = _pre(), _staged()
        # airflow_spacing is cultural and legal for fungal, and is not already in this ladder, so
        # neither the tier check nor the duplicate-method check masks the count
        _sprob(b, "parsnip", "damping-off")["control_ladder"].append(_rung("airflow_spacing"))
        with _with_batch(b):
            _expect(self, "parsnip has 22 rungs, expected 21", lambda: P.check(d))

    def test_hygiene_covers_the_ladder_batch_absolute_vocabulary(self):
        """tools/test_ladder_batch_absolutes.py re-derives every promote's list; this asserts the
        COVERAGE rather than re-listing, so a word dropped here is visible."""
        import ladder_batch
        for w in ladder_batch.ABSOLUTE_WORDS:
            self.assertTrue(P.hygiene("this %s happens" % w),
                            "hygiene() must catch %r" % w)


# ---------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_set_comparison_happens_before_value_comparison(self):
        """Iterating `pre` alone makes ADDITIONS invisible; that was all four PLA-162 defects."""
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        post = P.snapshot(d)
        self.assertEqual(len(set(post) - set(pre)), 2 * TOTAL_PROBLEMS)
        self.assertEqual(set(pre) - set(post), set())

    def test_bystander_crop_change_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        _pre_prob(d, BYSTANDER, "Damping-off")["type"] = "bacterial"
        _expect(self, "bystander crop %s changed" % BYSTANDER, lambda: P.verify_post(pre, d))

    def test_unexpected_added_leaf_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        _pre_prob(d, "potato", "Wireworms")["new_field"] = "x"
        _expect(self, "unexpected leaf keys added", lambda: P.verify_post(pre, d))

    def test_dropped_leaf_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        del _pre_prob(d, "potato", "Wireworms")["severity"]
        _expect(self, "leaf keys dropped", lambda: P.verify_post(pre, d))

    def test_unexpected_field_change_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        _pre_prob(d, "potato", "Wireworms")["severity"] = "high"
        _expect(self, "changed an unexpected field", lambda: P.verify_post(pre, d))

    def test_added_leaf_count_is_pinned(self):
        """Reachable only when the RIGHT KINDS of key are added but not the right NUMBER: drop one
        attached ladder, so `unexpected_add` and `dropped` are both empty and only the count sees it."""
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        del _pre_prob(d, "potato", "Wireworms")["control_ladder"]
        _expect(self, "leaf keys added, expected", lambda: P.verify_post(pre, d))

    def test_per_crop_problem_counts_are_checked(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        # revert one crop's type upgrades so the per-crop tally goes wrong
        for f in ("pests", "diseases"):
            for p in _crop(d, "parsnip").get(f) or []:
                p["type"] = "pest" if f == "pests" else "disease"
        _expect(self, "problems had type upgraded", lambda: P.verify_post(pre, d))

    def test_snapshot_covers_every_roster_crop_not_just_the_batch(self):
        d = _pre()
        snap = P.snapshot(d)
        slugs = {k[0] for k in snap}
        self.assertEqual(len(slugs), len(d["crops"]))
        self.assertIn(BYSTANDER, slugs)


class CatalogUntouched(unittest.TestCase):
    def test_control_methods_and_source_catalog_are_byte_identical_after_apply(self):
        d = _pre()
        before_cm = P.serialize(d["control_methods"])
        before_sc = P.serialize(d["source_catalog"])
        P.apply_to(d)
        P.check_catalog_untouched(before_cm, before_sc, d)
        self.assertEqual(P.serialize(d["control_methods"]), before_cm)

    def test_a_control_methods_change_refuses(self):
        d = _pre()
        before_cm = P.serialize(d["control_methods"])
        before_sc = P.serialize(d["source_catalog"])
        d["control_methods"]["crop_rotation"]["tier"] = "physical"
        _expect(self, "control_methods changed",
                lambda: P.check_catalog_untouched(before_cm, before_sc, d))

    def test_a_source_catalog_change_refuses(self):
        d = _pre()
        before_cm = P.serialize(d["control_methods"])
        before_sc = P.serialize(d["source_catalog"])
        k = sorted(d["source_catalog"])[0]
        d["source_catalog"][k] = dict(d["source_catalog"][k] or {}, injected=True) \
            if isinstance(d["source_catalog"][k], dict) else "injected"
        _expect(self, "source_catalog changed",
                lambda: P.check_catalog_untouched(before_cm, before_sc, d))


class BaseShaRefusal(unittest.TestCase):
    def test_base_sha_is_the_pinned_backfill_output(self):
        self.assertEqual(P.BASE_SHA,
                         "b118f19d36d021db95d755225e566843676fe3fa393299f250a8d34bb9605710")
        self.assertIn(P.BASE_SHA, promote_fixture.COMMIT_FOR)

    def test_main_refuses_a_wrong_base_sha_end_to_end(self):
        """Drives main() itself, through the real entry point, in a subprocess."""
        import subprocess, tempfile
        d = _pre()
        d["crops"][0]["slug"] = d["crops"][0]["slug"]      # no-op; then perturb bytes
        blob = P.serialize(d) + b" "
        with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as fh:
            fh.write(blob)
            path = fh.name
        try:
            # P.__file__, NOT the repo path: under the mutation harness the suite imports a
            # MUTATED copy, and invoking the pristine repo file would exercise the wrong code.
            r = subprocess.run([sys.executable, P.__file__, path],
                               capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("base SHA", r.stdout + r.stderr)
        finally:
            os.unlink(path)

    def test_main_runs_clean_on_the_real_canonical(self):
        import subprocess
        r = subprocess.run([sys.executable, P.__file__],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(POST_SHA, r.stdout)


# ---------------------------------------------------------------- entry-point wiring
class MainWiringIsDriven(unittest.TestCase):
    """The r8 lesson and its second half, learned one round apart:
    (1) reach the guard through the ENTRY POINT, and
    (2) make the sabotage one that ONLY that guard can see.
    The backfill's replacement driver still passed with check() removed, because its sabotage
    (a wrong rung count) is ALSO caught by verify_post."""

    def test_apply_to_calls_check(self):
        called = []
        real = P.check

        def spy(data):
            called.append(True)
            return real(data)

        with _Patch("check", spy):
            P.apply_to(_pre())
        self.assertEqual(len(called), 1, "apply_to must reach check(); r8 found it did not")

    def test_the_sabotage_is_invisible_to_verify_post(self):
        """Proves the sabotage below is CHECK-ONLY. verify_post compares leaf keys and counts and
        cannot see prose content at all, so it cannot mask this guard."""
        d, b = _pre(), _staged()
        _sprob(b, "potato", "wireworms")["control_ladder"][0]["note_seasoned"] = \
            "This is the first rung of the sequence, invisible to a leaf-level diff."
        pre = P.snapshot(d)
        with _with_batch(b), _Patch("check", lambda data: b):
            P.apply_to(d)
            self.assertEqual(P.verify_post(pre, d), TOTAL_PROBLEMS)

    def test_with_check_live_the_same_sabotage_refuses_through_the_entry_point(self):
        d, b = _pre(), _staged()
        _sprob(b, "potato", "wireworms")["control_ladder"][0]["note_seasoned"] = \
            "This is the first rung of the sequence, invisible to a leaf-level diff."
        with _with_batch(b):
            _expect(self, "uses internal vocabulary", lambda: P.apply_to(d))


if __name__ == "__main__":
    unittest.main(verbosity=2)
