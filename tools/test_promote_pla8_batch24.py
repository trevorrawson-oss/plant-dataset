#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch24.py. Base c24d7754 (catalog r10).

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are LIVE is `MainWiringIsDriven`
plus tools/mutate_pla8_batch24_suite.py.

Every driver asserts the ONE message its branch emits. Batch 23 lost time three separate times to
drivers asserting a fragment that also occurs in a SIBLING guard's message, so either branch could
be disabled with the suite still green. The colliding constants in THIS promote are "problems,
expected" (schema premise AND blast radius), "expected 27" (pin-table size, schema coverage and
type coverage, all three), "is vacuous" (precedent pass A AND pass B), "this guard would be
vacuous" (echo corpus AND echo coverage), and "not in the batch" (scope, spelling AND taxon-reuse
pins). Every anti-vacuity branch has its own driver.

WHAT IS NEW versus batches 17-23, and why the inherited drivers do NOT cover it:

* `SchemaPremise` drives a SPLIT premise, both directions per crop, and the severity split BOTH
  WAYS -- a one-directional severity driver passes on a crop that is simply missing the field.
* `TypeSetFromNothing` drives `type` as an ABSENT key. Batch 23's coarse->fine drivers assert
  messages this promote never emits.
* `TemplateTwinsPremise` carries a POSITIVE CONTROL BUILT FROM THE REAL DEFECT: the historical
  scan matched `None` to `None` on 6 of 8 fields and reported 3 twins where there are zero. The
  control asserts the naive comparison STILL reports identity on this fixture and that the
  schema-aware guard is not fooled by it. A driver that only fires the guard on a real twin would
  have passed against the broken version too.
* `MetricDiscriminates` asserts THE METRIC, which is the part a mutation harness cannot reach.
  Batch 23's copy guard was reachable, non-vacuous and mutation-tested 3/3 -- every property the
  PLA-215 bar checks -- and it scored the batch's only real copy at 0.431 and passed it. Three
  separate dilutions have now been found in this one metric and a harness reddens on none of them,
  because the branch fires correctly every time and only the NUMBER handed to it is wrong.
* `ShippedProseEcho` drives the DECLARED-IDENTITY EXEMPTION. Without it two guards contradict each
  other, one requiring byte-identity and the other forbidding it, and the batch cannot pass either
  way while the failure reads as bad data.
* `IdAdjudications` drives BOTH HALVES of the scope split. The own half was an unused tuple element
  until this suite was written -- unpacked from the pin, never read, reading as coverage.

COST. `check_no_precedent_copy` makes 18575 comparisons over 82 rungs and takes ~55s, so the suite
runs the full-corpus path EXACTLY ONCE, as a subprocess of the module under test, and every other
driver works from the cached result or from a THIN fixture. The subprocess runs `P.__file__`, not
the repo path: under the mutation harness the imported module is the MUTATED copy in a sandbox, and
a hard-coded repo path would run the clean promote and report every mutation as caught.
"""
import copy, difflib, hashlib, json, os, subprocess, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch24 as P  # noqa: E402

CROPS = ("chives", "leek", "onion", "shallot")
TOTAL_RUNGS = 95
TOTAL_PROBLEMS = 26
POST_SHA = "a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7"
PRECEDENT = "garlic"          # the real management relative; NOT spring-onion
SIBLING = "spring-onion"      # holds the declared identity and the resembled scope id
# The thin fixture keeps every crop any guard reaches for, and nothing else.
THIN_KEEP = set(CROPS) | {PRECEDENT, SIBLING, "carrot", "parsley", "apple", "potato"}
EXPECTED_CMP_A = 260
EXPECTED_CMP_B = 20904
EXPECTED_WORST = 0.612
EXPECTED_WORST_PAIR = "B:chives/downy-mildew/airflow_spacing vs cherry-tomato/early-blight"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


_RUN = {}


def _run_promote():
    """THE ONE full-corpus execution, through the real entry point, cached for the whole suite.

    Runs the module under test as a SUBPROCESS of `P.__file__` so the mutation harness's sandbox
    copy is what executes, and applies to a temp file so the post-state bytes come back as the
    promote's own output rather than being rebuilt here."""
    if _RUN:
        return _RUN
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        fh.write(promote_fixture.pre_state(P.BASE_SHA))
        path = fh.name
    try:
        r = subprocess.run([sys.executable, P.__file__, path, "--apply"],
                           capture_output=True, text=True)
        _RUN["rc"] = r.returncode
        _RUN["out"] = r.stdout + r.stderr
        if r.returncode == 0:
            with open(path, "rb") as fh:
                _RUN["post"] = fh.read()
        else:
            _RUN["post"] = b""
    finally:
        os.unlink(path)
    return _RUN


def _post():
    run = _run_promote()
    assert run["rc"] == 0, "the clean promote must succeed:\n" + run["out"]
    return json.loads(run["post"].decode("utf-8"))


_SNAP = {}


def _pre_snap():
    if not _SNAP:
        _SNAP["v"] = P.snapshot(_pre())
    return _SNAP["v"]


def _staged():
    return copy.deepcopy(P.staged())


def _thin():
    """The fixture the precedent drivers use. Same shape, ~6 crops, so the guard's LOGIC can be
    driven without paying the full 18575-comparison scan on every driver."""
    d = _pre()
    d["crops"] = [c for c in d["crops"] if c.get("slug") in THIN_KEEP]
    return d


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


def _live_prob(data, slug, pid):
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("id") == pid:
                return p
    raise AssertionError("live %s/%s not found" % (slug, pid))


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


def _with_batch(batch):
    return _Patch("staged", lambda: batch)


_UNIQ = [0]


def _rung(m):
    _UNIQ[0] += 1
    return {"method": m,
            "note_beginner": "Injected beginner text number %d written for this driver only, and "
                             "long enough to clear the sentence floor." % _UNIQ[0],
            "note_seasoned": "Injected seasoned wording number %d, which differs materially from "
                             "its own beginner register." % _UNIQ[0]}


def _expect(case, sentence, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(sentence, str(cm.exception))


# ---------------------------------------------------------------- the happy path
class CleanRun(unittest.TestCase):
    def test_the_clean_promote_succeeds_through_its_own_entry_point(self):
        run = _run_promote()
        self.assertEqual(run["rc"], 0, run["out"])

    def test_apply_produces_the_pinned_post_sha(self):
        self.assertEqual(hashlib.sha256(_run_promote()["post"]).hexdigest(), POST_SHA)

    def test_the_pre_state_is_the_pinned_shape(self):
        self.assertEqual(hashlib.sha256(P.serialize(_pre())).hexdigest(), P.BASE_SHA)

    def test_serialize_is_compact_and_unescaped(self):
        self.assertEqual(P.serialize({"a": "café", "b": [1, 2]}),
                         '{"a":"café","b":[1,2]}'.encode("utf-8"))

    def test_counts_are_pinned_not_derived(self):
        self.assertEqual(sum(P.EXPECTED_PROBLEMS.values()), TOTAL_PROBLEMS)
        self.assertEqual(sum(P.EXPECTED_RUNGS.values()), P.TOTAL_RUNGS)
        self.assertEqual(P.TOTAL_RUNGS, TOTAL_RUNGS)

    def test_the_batch_holds_the_pinned_number_of_problems(self):
        b = _staged()
        self.assertEqual(sum(len(b[c].get(f) or []) for c in CROPS
                             for f in ("pests", "diseases")), TOTAL_PROBLEMS)

    def test_the_schema_split_is_asserted_here_not_only_inside_the_guard(self):
        """The premise the whole batch rests on, stated independently of the code enforcing it."""
        self.assertIs(P.SCHEMA_FOR["chives"], P.FULL_SCHEMA_FIELDS)
        for c in ("leek", "onion", "shallot"):
            self.assertIs(P.SCHEMA_FOR[c], P.ALLIUM_SCHEMA_FIELDS)
        self.assertEqual(P.SEVERITY_EXPECTED,
                         {"chives": False, "leek": True, "onion": True, "shallot": True})
        d = _pre()
        for c in CROPS:
            self.assertEqual({bool(p.get("severity")) for _f, p in P.problems(_crop(d, c))},
                             {P.SEVERITY_EXPECTED[c]}, c)


# ---------------------------------------------------------------- pre-state premise
class SchemaPremise(unittest.TestCase):
    def test_missing_full_schema_field_on_chives_refuses(self):
        d = _pre()
        del _pre_prob(d, "chives", "Downy mildew")["cause_seasoned"]
        _expect(self, "missing cause_seasoned, required by its schema",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_missing_allium_schema_field_on_leek_refuses(self):
        d = _pre()
        del _pre_prob(d, "leek", "Leek moth")["management_seasoned"]
        _expect(self, "missing management_seasoned, required by its schema",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_full_schema_field_appearing_on_an_allium_crop_refuses(self):
        """DIRECTION ONE. A FULL field on onion means the crop is not the shape the brief
        described, and its authoring agent was pointed at fields the record does not carry."""
        d = _pre()
        _pre_prob(d, "onion", "Onion maggot")["symptoms_beginner"] = "x"
        _expect(self, "carries symptoms_beginner from the OTHER schema",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_allium_schema_field_appearing_on_chives_refuses(self):
        """DIRECTION TWO, driven separately: a single-direction guard passes on the crop it was
        not written for."""
        d = _pre()
        _pre_prob(d, "chives", "Rust")["identification_beginner"] = "x"
        _expect(self, "carries identification_beginner from the OTHER schema",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_shared_cause_fields_are_not_treated_as_the_other_schema(self):
        """cause_beginner/cause_seasoned are in BOTH sets. Without the `f not in fields` clause
        the guard refuses every crop in the batch on its first problem."""
        self.assertIn("cause_beginner", P.FULL_SCHEMA_FIELDS)
        self.assertIn("cause_beginner", P.ALLIUM_SCHEMA_FIELDS)
        P.check_schema_premise(P.by_slug(_pre()))

    def test_note_schema_field_present_refuses(self):
        d = _pre()
        _pre_prob(d, "shallot", "White rot")["note"] = "x"
        _expect(self, "carries note-schema field note",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_severity_appearing_on_chives_refuses(self):
        """The severity split runs the OPPOSITE way to the schema split, and only measuring found
        it. This half is 'present where none is pinned'."""
        d = _pre()
        _pre_prob(d, "chives", "Rust")["severity"] = "moderate"
        _expect(self, "severity present=True, pinned False",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_severity_missing_on_an_allium_crop_refuses(self):
        d = _pre()
        del _pre_prob(d, "shallot", "Pink root")["severity"]
        _expect(self, "severity present=False, pinned True",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_already_laddered_target_refuses(self):
        d = _pre()
        _pre_prob(d, "onion", "Pink root")["control_ladder"] = [_rung("crop_rotation")]
        _expect(self, "is ALREADY laddered", lambda: P.check_schema_premise(P.by_slug(d)))

    def test_pre_existing_id_refuses(self):
        d = _pre()
        _pre_prob(d, "leek", "Leek rust")["id"] = "leek-rust"
        _expect(self, "already carries id 'leek-rust'",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_missing_sources_refuses(self):
        d = _pre()
        _pre_prob(d, "chives", "White rot")["sources"] = []
        _expect(self, "missing sources/anchoring_urls",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_problem_count_drift_refuses(self):
        """WHOLE SENTENCE: "problems, expected" also occurs in the blast-radius message."""
        d = _pre()
        _crop(d, "onion")["pests"].pop()
        _expect(self, "onion has 4 problems, expected 5",
                lambda: P.check_schema_premise(P.by_slug(d)))

    def test_schema_coverage_count_is_pinned(self):
        """ANTI-VACUITY: if the crop loop never runs, nothing was scanned and the premise is
        unproven while the guard reports green."""
        d = _pre()
        with _Patch("CROPS", ()):
            _expect(self, "schema premise scanned 0 problems, expected 26",
                    lambda: P.check_schema_premise(P.by_slug(d)))

    def test_crop_absent_refuses(self):
        d = _pre()
        d["crops"] = [c for c in d["crops"] if c.get("slug") != "chives"]
        _expect(self, "crop chives not on the roster",
                lambda: P.check_schema_premise(P.by_slug(d)))


class TypeSetFromNothing(unittest.TestCase):
    def test_pre_state_type_present_at_all_refuses(self):
        """Batch 23's crops carried a COARSE type and its guard checked the upgrade. Here the key
        does not exist, so ANY pre-state type is the refusal."""
        d, b = _pre(), _staged()
        _pre_prob(d, "leek", "Onion thrips")["type"] = "insect"
        _expect(self, "already carries type 'insect'; this batch SETS the type from nothing",
                lambda: P.check_type_set_from_nothing(b, P.by_slug(d)))

    def test_staged_type_off_the_pin_refuses(self):
        d, b = _pre(), _staged()
        _sprob(b, "leek", "pink-root")["type"] = "bacterial"
        _expect(self, "staged type 'bacterial', pinned 'fungal'",
                lambda: P.check_type_set_from_nothing(b, P.by_slug(d)))

    def test_staged_type_outside_the_gate_type_map_refuses(self):
        """Reachable only with the pin moved too, since the off-the-pin branch fires first.
        Driving it through the pin proves the branch is not dead code."""
        d, b = _pre(), _staged()
        conv = dict(P.ID_CONVENTION)
        name, pid, _t, dec = conv[("onion", "diseases", 2)]
        conv[("onion", "diseases", 2)] = (name, pid, "mycoplasma", dec)
        _sprob(b, "onion", "pink-root")["type"] = "mycoplasma"
        with _Patch("ID_CONVENTION", conv):
            _expect(self, "type 'mycoplasma' is not in the gate's type map",
                    lambda: P.check_type_set_from_nothing(b, P.by_slug(d)))

    def test_length_mismatch_refuses(self):
        d, b = _pre(), _staged()
        b["shallot"]["pests"].pop()
        _expect(self, "shallot/pests length 2 staged vs 3 canonical",
                lambda: P.check_type_set_from_nothing(b, P.by_slug(d)))

    def test_type_coverage_count_is_pinned(self):
        d, b = _pre(), _staged()
        with _Patch("CROPS", ()):
            _expect(self, "type set scanned 0, expected 26",
                    lambda: P.check_type_set_from_nothing(b, P.by_slug(d)))


class Ids(unittest.TestCase):
    def test_pin_table_size_is_asserted(self):
        d, b = _pre(), _staged()
        conv = dict(P.ID_CONVENTION)
        conv.pop(("shallot", "diseases", 3))
        with _Patch("ID_CONVENTION", conv):
            _expect(self, "pin table holds 25 entries, expected 26",
                    lambda: P.check_ids(b, P.by_slug(d)))

    def test_canonical_name_drift_refuses(self):
        d, b = _pre(), _staged()
        _pre_prob(d, "leek", "Leek moth")["name"] = "Leek moths"
        _expect(self, "canonical name 'Leek moths', pinned 'Leek moth'",
                lambda: P.check_ids(b, P.by_slug(d)))

    def test_staged_id_off_the_pin_refuses(self):
        d, b = _pre(), _staged()
        _sprob(b, "chives", "chives-rust")["id"] = "rust"
        _expect(self, "staged id 'rust', pinned 'chives-rust'",
                lambda: P.check_ids(b, P.by_slug(d)))

    def test_pin_coverage_is_a_coverage_assertion_not_a_restatement(self):
        """The first version filled `seen` by iterating ID_CONVENTION and compared it to
        ID_CONVENTION, so it could never fail. It must be measured against the BATCH's positions."""
        d, b = _pre(), _staged()
        conv = {k: v for k, v in P.ID_CONVENTION.items() if k != ("chives", "pests", 2)}
        with _Patch("ID_CONVENTION", conv), \
                _Patch("EXPECTED_PROBLEMS", dict(P.EXPECTED_PROBLEMS, chives=6)):
            _expect(self, "the pin table covers 25 positions but the batch holds 26",
                    lambda: P.check_ids(b, P.by_slug(d)))

    def test_out_of_range_position_refuses(self):
        d, b = _pre(), _staged()
        conv = dict(P.ID_CONVENTION)
        conv[("onion", "pests", 7)] = ("Onion thrips", "onion-thrips", "insect", "REUSE")
        with _Patch("ID_CONVENTION", conv), \
                _Patch("EXPECTED_PROBLEMS", dict(P.EXPECTED_PROBLEMS, onion=6)):
            _expect(self, "onion/pests[7] out of range", lambda: P.check_ids(b, P.by_slug(d)))

    def test_duplicate_id_within_a_crop_refuses(self):
        d, b = _pre(), _staged()
        conv = dict(P.ID_CONVENTION)
        name, _pid, t, dec = conv[("shallot", "diseases", 3)]
        conv[("shallot", "diseases", 3)] = (name, "white-rot", t, dec)
        _sprob(b, "shallot", "pink-root")["id"] = "white-rot"
        with _Patch("ID_CONVENTION", conv):
            _expect(self, "shallot has duplicate problem ids",
                    lambda: P.check_ids(b, P.by_slug(d)))


class IdAdjudications(unittest.TestCase):
    # ---- scope variant, BOTH halves
    def test_scope_pin_missing_from_the_batch_refuses(self):
        d, b = _thin(), _staged()
        b["chives"] = {"pests": [], "diseases": []}
        _expect(self, "scope pin 'botrytis-leaf-blight-neck-rot' is not in the batch; the pin is "
                      "stale",
                lambda: P.check_id_adjudications(b, d))

    def test_scope_minted_id_already_live_refuses(self):
        d, b = _thin(), _staged()
        _live_prob(d, PRECEDENT, "botrytis-neck-rot")["id"] = "botrytis-leaf-blight-neck-rot"
        _expect(self, "'botrytis-leaf-blight-neck-rot' was minted as distinct but already exists",
                lambda: P.check_id_adjudications(b, d))

    def test_resembled_id_vanishing_refuses(self):
        d, b = _thin(), _staged()
        for c in d["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                if p.get("id") == "botrytis-neck-rot":
                    p["id"] = "gray-mold"
        _expect(self, "'botrytis-neck-rot' no longer exists, so the reason to keep "
                      "'botrytis-leaf-blight-neck-rot' separate cannot be checked",
                lambda: P.check_id_adjudications(b, d))

    def test_other_half_of_the_scope_split_vanishing_refuses(self):
        """The live id is the STORAGE rot. If no holder still says so, the split is unproven."""
        d, b = _thin(), _staged()
        for c in d["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                if p.get("id") != "botrytis-neck-rot":
                    continue
                for f in P.SCHEMA_FOR.get(c["slug"], P.FULL_SCHEMA_FIELDS):
                    if p.get(f):
                        p[f] = p[f].replace("curing", "drying down")
        _expect(self, "'botrytis-neck-rot' no longer says 'curing', so the scope split that "
                      "justified 'botrytis-leaf-blight-neck-rot' is unproven",
                lambda: P.check_id_adjudications(b, d))

    def test_own_half_of_the_scope_split_vanishing_refuses(self):
        """THE HALF THAT WAS NOT CHECKED. `own_phrase` was unpacked from the pin and never read,
        so chives' entry could have stopped describing a FOLIAR blight -- the reason it is a
        distinct id at all -- and the guard would have gone on reporting green."""
        d, b = _thin(), _staged()
        p = _pre_prob(d, "chives", "Botrytis (leaf blight and neck rot)")
        for f in P.FULL_SCHEMA_FIELDS:
            if p.get(f):
                p[f] = p[f].replace("dense canopies", "thick stands")
        _expect(self, "no longer says 'dense canopies', so the half of the scope split that makes "
                      "'botrytis-leaf-blight-neck-rot' a DISTINCT entry is unproven",
                lambda: P.check_id_adjudications(b, d))

    def test_own_half_anchor_must_map_to_exactly_one_pinned_position(self):
        d, b = _thin(), _staged()
        conv = dict(P.ID_CONVENTION)
        name, _pid, t, dec = conv[("chives", "diseases", 1)]
        conv[("chives", "diseases", 1)] = (name, "botrytis-leaf-blight-neck-rot", t, dec)
        with _Patch("ID_CONVENTION", conv):
            _expect(self, "maps to 2 pinned positions, expected exactly 1; the own side cannot be "
                          "anchored",
                    lambda: P.check_id_adjudications(b, d))

    # ---- spelling variant
    def test_spelling_pin_missing_from_the_batch_refuses(self):
        d, b = _thin(), _staged()
        _sprob(b, "leek", "allium-leafminer")["id"] = "allium-leaf-miner"
        _expect(self, "spelling pin leek/allium-leafminer is not in the batch",
                lambda: P.check_id_adjudications(b, d))

    def test_spelling_pin_display_name_vanishing_refuses(self):
        d, b = _thin(), _staged()
        _pre_prob(d, "leek", "Allium leaf miner")["name"] = "Allium leafminer"
        _expect(self, "leek no longer names a problem 'Allium leaf miner'; the spelling pin is "
                      "stale",
                lambda: P.check_id_adjudications(b, d))

    def test_spelling_pin_organism_vanishing_refuses(self):
        """Anchored on the ORGANISM both records name, never on the id string, so it fails loudly
        if the reason to reuse across a spelling difference stops being true."""
        d, b = _thin(), _staged()
        p = _pre_prob(d, "leek", "Allium leaf miner")
        for f in P.ALLIUM_SCHEMA_FIELDS:
            if p.get(f):
                p[f] = p[f].replace("Phytomyza gymnostoma", "the fly")
        _expect(self, "no longer names 'Phytomyza gymnostoma', so reusing 'allium-leafminer' "
                      "across the spelling difference is unproven",
                lambda: P.check_id_adjudications(b, d))

    # ---- taxon reuse
    def test_taxon_reuse_pin_missing_from_the_batch_refuses(self):
        d, b = _thin(), _staged()
        pins = {("chives", "ghost-id"): P.TAXON_REUSE_PINS[("chives", "white-rot")]}
        with _Patch("TAXON_REUSE_PINS", pins):
            _expect(self, "taxon-reuse pin 'ghost-id' not in the batch",
                    lambda: P.check_id_adjudications(b, d))

    def test_precedent_crop_losing_the_reused_id_refuses(self):
        d, b = _thin(), _staged()
        _live_prob(d, PRECEDENT, "white-rot")["id"] = "allium-white-rot"
        _expect(self, "'garlic' no longer holds 'white-rot', so the reuse is unproven",
                lambda: P.check_id_adjudications(b, d))

    def test_taxon_phrase_vanishing_refuses(self):
        d, b = _thin(), _staged()
        p = _live_prob(d, PRECEDENT, "white-rot")
        for f in P.SCHEMA_FOR.get(PRECEDENT, P.ALLIUM_SCHEMA_FIELDS):
            if p.get(f):
                p[f] = p[f].replace("Sclerotium cepivorum", "the fungus")
        _expect(self, "no longer says 'Sclerotium cepivorum'; the taxon check that justified this "
                      "reuse has stopped being true",
                lambda: P.check_id_adjudications(b, d))

    # ---- stem variant
    def test_unadjudicated_stem_variant_refuses(self):
        """A REFUSAL SPEC at zero: no minted id in this batch is stem-equal to a live one, so
        staying green IS the pass. This proves the branch would fire if one appeared."""
        d, b = _thin(), _staged()
        conv = dict(P.ID_CONVENTION)
        name, _pid, t, dec = conv[("leek", "diseases", 2)]
        conv[("leek", "diseases", 2)] = (name, "wireworm", t, dec)
        _sprob(b, "leek", "pink-root")["id"] = "wireworm"
        with _Patch("ID_CONVENTION", conv):
            _expect(self, "leek MINTS 'wireworm' while the roster holds the stem-equal 'wireworms'",
                    lambda: P.check_id_adjudications(b, d))

    def test_adjudicated_stem_pair_count_is_pinned(self):
        d, b = _thin(), _staged()
        conv = dict(P.ID_CONVENTION)
        name, _pid, t, dec = conv[("leek", "diseases", 2)]
        conv[("leek", "diseases", 2)] = (name, "wireworm", t, dec)
        _sprob(b, "leek", "pink-root")["id"] = "wireworm"
        with _Patch("ID_CONVENTION", conv), \
                _Patch("STEM_VARIANT_PINS", {("wireworm", "wireworms"): ("x", "y")}):
            _expect(self, "1 stem-variant pairs adjudicated, pinned 0",
                    lambda: P.check_id_adjudications(b, d))

    def test_the_stemmer_is_not_plural_blind(self):
        """THE ORIGINAL BUG: an `es`-stripping version turned `beetles` into `beetl` while
        `beetle` stayed `beetle`, so the pair never compared equal and the guard silently skipped
        the exact class it exists for."""
        self.assertEqual(P._stem_key("wireworm"), P._stem_key("wireworms"))
        self.assertEqual(P._stem_key("flea-beetle"), P._stem_key("flea-beetles"))
        self.assertEqual(P._stem_key("aphid"), P._stem_key("aphids"))
        self.assertNotEqual(P._stem_key("white-rot"), P._stem_key("pink-root"))

    def test_the_real_batch_passes_every_adjudication(self):
        P.check_id_adjudications(_staged(), _pre())


class TemplateTwinsPremise(unittest.TestCase):
    def test_a_real_twin_on_the_carried_fields_refuses(self):
        d = _thin()
        src = _pre_prob(d, "chives", "Downy mildew")
        host = None
        for c in d["crops"]:
            if c["slug"] in CROPS:
                continue
            if not any(x.get("control_ladder") for _f, x in P.problems(c)):
                continue
            for _f, p in P.problems(c):
                if all(p.get(k) for k in P.FULL_SCHEMA_FIELDS):
                    host = p
                    break
            if host:
                break
        self.assertIsNotNone(host, "no laddered FULL-schema host in the thin fixture")
        for k in P.FULL_SCHEMA_FIELDS:
            host[k] = src[k]
        _expect(self, "is a TEMPLATE TWIN of",
                lambda: P.check_no_template_twins_premise(P.by_slug(d), d))

    def test_positive_control_the_naive_scan_still_reports_identity_on_absence(self):
        """THE REAL DEFECT, REPRODUCED. The historical scan compared the 8 FULL-schema fields on
        crops carrying identification_*/management_*, so 6 of 8 were None on BOTH sides and the
        tuples matched on ABSENCE. It reported 3 twins where there are zero, and two authoring
        agents were told to copy a sibling's ladder on the strength of it.

        A driver that only fires the guard on a REAL twin would have passed against the broken
        version too. This asserts BOTH halves: that the naive tuple comparison STILL matches on
        this fixture, and that the schema-aware guard is not fooled by it."""
        d = _pre()
        naive = []
        for c in CROPS:
            for _f, p in P.problems(_crop(d, c)):
                key = tuple(p.get(k) for k in P.FULL_SCHEMA_FIELDS)
                for cc in d["crops"]:
                    if cc["slug"] in CROPS:
                        continue
                    if not any(x.get("control_ladder") for _ff, x in P.problems(cc)):
                        continue
                    for _ff, pp in P.problems(cc):
                        if tuple(pp.get(k) for k in P.FULL_SCHEMA_FIELDS) == key:
                            naive.append((c, p.get("name"), cc["slug"], pp.get("name"),
                                          sum(1 for k in P.FULL_SCHEMA_FIELDS
                                              if p.get(k) is None and pp.get(k) is None)))
        # EXACTLY the 3 the broken scan reported, all against the sibling, all matching on ABSENCE
        self.assertEqual(len(naive), 3,
                         "the historical false-identity shape has changed; this control no longer "
                         "reproduces the defect it exists for: %r" % (naive,))
        self.assertEqual({row[2] for row in naive}, {SIBLING})
        for row in naive:
            self.assertEqual(row[4], 6, "matched on %d absent fields, expected 6: %r" % (row[4], row))
        self.assertEqual(sorted((row[0], row[1]) for row in naive),
                         [("onion", "Fusarium basal rot"), ("onion", "Onion thrips"),
                          ("shallot", "Onion thrips")])
        # ...and the schema-aware guard reports ZERO on the same fixture.
        P.check_no_template_twins_premise(P.by_slug(d), d)

    def test_a_comparison_is_only_counted_where_both_sides_carry_the_fields(self):
        """The `all(...)` presence filters ARE the fix. Remove either and the guard counts
        absence as data."""
        leek = _pre_prob(_pre(), "leek", "Leek rust")
        self.assertFalse(all(leek.get(k) for k in P.FULL_SCHEMA_FIELDS))
        self.assertTrue(all(leek.get(k) for k in P.ALLIUM_SCHEMA_FIELDS))

    def test_anti_vacuity_branch_refuses_when_nothing_was_compared(self):
        d = _thin()
        with _Patch("CROPS", ()):
            _expect(self, "no schema-compatible shipped problem was compared; the twin premise is "
                          "unproven and this guard is vacuous",
                    lambda: P.check_no_template_twins_premise(P.by_slug(d), d))

    # -- THE THREE DRIVERS THE RE-AUTHORED BATCH'S HARNESS SHOWED WERE MISSING (2026-09-03).
    # On the corrected records the "historical bug" mutation (FULL fields imposed on every crop)
    # no longer reports a false twin: the presence filters skip every allium-schema problem
    # instead, so the mutation's effect is SILENT non-coverage, and the two filter mutations are
    # no-ops on real data because every real problem carries its schema. Each is driven below
    # through the one observable that separates "compared and found nothing" from "never
    # compared": the anti-vacuity branch on a single-crop batch.

    def _shipped_allium_host(self, d):
        for c in d["crops"]:
            if c["slug"] in CROPS or not any(x.get("control_ladder") for _f, x in P.problems(c)):
                continue
            for _f, p in P.problems(c):
                if all(p.get(k) for k in P.ALLIUM_SCHEMA_FIELDS):
                    return p
        self.fail("no laddered allium-schema host in the thin fixture")

    def test_the_field_set_follows_the_crop_schema_or_the_crop_is_never_compared(self):
        """With FULL fields imposed on leek, the batch-side filter skips all seven leek problems
        and a leek-only batch is vacuous. The correct guard compares leek on ITS fields."""
        d = _thin()
        self._shipped_allium_host(d)
        with _Patch("CROPS", ("leek",)):
            P.check_no_template_twins_premise(P.by_slug(d), d)

    def test_the_batch_side_presence_filter_is_load_bearing(self):
        """A batch problem missing one of its fields must not be compared at all. With the
        shipped-side filter intact no shared-None twin can form, so the batch-side filter's only
        observable is the comparison count: blank a field on EVERY leek problem and a leek-only
        batch is vacuous under the correct guard, and silently 'compared' without the filter."""
        d = _thin()
        self._shipped_allium_host(d)
        for _f, p in P.problems(_crop(d, "leek")):
            p["identification_beginner"] = None
        with _Patch("CROPS", ("leek",)):
            _expect(self, "no schema-compatible shipped problem was compared; the twin premise is "
                          "unproven and this guard is vacuous",
                    lambda: P.check_no_template_twins_premise(P.by_slug(d), d))

    def test_the_shipped_side_presence_filter_is_load_bearing(self):
        """Every shipped allium-schema problem blanked on one field: the correct guard has nothing
        it may compare a leek problem against and refuses as vacuous; without the shipped-side
        filter it compares against absence and passes."""
        d = _thin()
        self._shipped_allium_host(d)
        for c in d["crops"]:
            if c["slug"] in CROPS or not any(x.get("control_ladder") for _f, x in P.problems(c)):
                continue
            for _f, p in P.problems(c):
                if all(p.get(k) for k in P.ALLIUM_SCHEMA_FIELDS):
                    p["identification_beginner"] = None
        with _Patch("CROPS", ("leek",)):
            _expect(self, "no schema-compatible shipped problem was compared; the twin premise is "
                          "unproven and this guard is vacuous",
                    lambda: P.check_no_template_twins_premise(P.by_slug(d), d))

    def test_the_real_batch_has_zero_twins_roster_wide(self):
        d = _pre()
        P.check_no_template_twins_premise(P.by_slug(d), d)


class NoPrecedentCopy(unittest.TestCase):
    def test_both_passes_make_comparisons_on_the_thin_fixture(self):
        cmp_a, cmp_b, worst = P.check_no_precedent_copy(_staged(), _thin())
        self.assertGreater(cmp_a, 0)
        self.assertGreater(cmp_b, 0)
        self.assertLess(worst[0], P.PRECEDENT_COPY_THRESHOLD)

    def test_pass_a_refuses_a_rung_copied_from_the_same_problem_and_method(self):
        d, b = _thin(), _staged()
        donor = (_live_prob(d, PRECEDENT, "onion-thrips").get("control_ladder") or [])[0]
        tgt = _sprob(b, "leek", "onion-thrips")
        tgt["control_ladder"][0] = {"method": donor["method"],
                                    "note_beginner": donor["note_beginner"],
                                    "note_seasoned": donor["note_seasoned"]}
        _expect(self, "similar to garlic's rung for the same problem and method",
                lambda: P.check_no_precedent_copy(b, d))

    def test_pass_b_refuses_a_rung_lifted_onto_a_DIFFERENT_problem(self):
        """The pass an authoring agent found missing. Phrasing lifted from a sibling's DIFFERENT
        problem scores 0.000 under pass A, and two real cases landed on `pink-root`, which no
        shipped crop carries -- pass A had nothing to compare against at all."""
        d, b = _thin(), _staged()
        donor = None
        for _f, p in P.problems(_crop(d, PRECEDENT)):
            for r in p.get("control_ladder") or []:
                if r["method"] == "crop_rotation":
                    donor = r
        self.assertIsNotNone(donor)
        tgt = _sprob(b, "leek", "pink-root")
        tgt["control_ladder"][0] = {"method": "crop_rotation",
                                    "note_beginner": donor["note_beginner"],
                                    "note_seasoned": donor["note_seasoned"]}
        _expect(self, "using the SAME METHOD on a DIFFERENT problem",
                lambda: P.check_no_precedent_copy(b, d))

    def test_declared_identity_must_be_byte_identical(self):
        d, b = _thin(), _staged()
        r = [x for x in _sprob(b, "onion", "onion-thrips")["control_ladder"]
             if x["method"] == "water_spray"][0]
        r["note_seasoned"] = r["note_seasoned"] + " One more clause."
        _expect(self, "is DECLARED byte-identical to spring-onion's rung and is not. "
                      "Near-identical is neither a declared propagation nor independent authoring.",
                lambda: P.check_no_precedent_copy(b, d))

    def test_declared_identity_naming_a_crop_with_no_such_rung_refuses(self):
        d, b = _thin(), _staged()
        with _Patch("DECLARED_IDENTITIES",
                    {("onion", "onion-thrips", "water_spray"): ("carrot", "why")}):
            _expect(self, "names carrot, which has no rung for this problem and method",
                    lambda: P.check_no_precedent_copy(b, d))

    def test_declared_identity_missing_from_the_batch_refuses(self):
        d, b = _thin(), _staged()
        decl = dict(P.DECLARED_IDENTITIES)
        decl[("leek", "white-rot", "crop_rotation")] = (PRECEDENT, "invented for this driver")
        with _Patch("DECLARED_IDENTITIES", decl):
            _expect(self, "declared identities [('leek', 'white-rot', 'crop_rotation')] were not "
                          "found in the batch",
                    lambda: P.check_no_precedent_copy(b, d))

    def test_pass_a_anti_vacuity_branch(self):
        """cmp_a == 0 while cmp_b > 0: the SUBSET is empty and the superset is not. Reaching this
        at all requires stripping the shipped ids, which is why the branch order matters."""
        d, b = _thin(), _staged()
        for c in d["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                p["id"] = None
        lad = _sprob(b, "onion", "onion-thrips")["control_ladder"]
        lad[:] = [r for r in lad if r["method"] != "water_spray"]
        with _Patch("DECLARED_IDENTITIES", {}):
            _expect(self, "precedent pass A made 0 comparisons; it is vacuous",
                    lambda: P.check_no_precedent_copy(b, d))

    def test_pass_b_anti_vacuity_branch(self):
        """THIS BRANCH WAS UNREACHABLE UNTIL THIS SUITE WAS WRITTEN. `by_m` is a superset of
        `by_idm`, so cmp_b == 0 implies cmp_a == 0; with pass A checked first the pass-B branch
        could never fire. An anti-vacuity branch that is itself vacuous is the batch-21 class."""
        d, b = _thin(), _staged()
        for c in d["crops"]:
            if c["slug"] in CROPS:
                continue
            for _f, p in P.problems(c):
                p["control_ladder"] = None
        with _Patch("DECLARED_IDENTITIES", {}):
            _expect(self, "precedent pass B made 0 comparisons; it is vacuous",
                    lambda: P.check_no_precedent_copy(b, d))

    def test_the_superset_branch_is_checked_first(self):
        """The ordering IS the fix, asserted so a refactor cannot quietly restore the dead
        branch."""
        import inspect
        src = inspect.getsource(P.check_no_precedent_copy)
        self.assertLess(src.index("pass B made 0 comparisons"),
                        src.index("pass A made 0 comparisons"))


class MetricDiscriminates(unittest.TestCase):
    """THE PART A MUTATION HARNESS CANNOT REACH.

    Batch 23's copy guard was reachable (243 comparisons), non-vacuous and mutation-tested 3/3 --
    every property the PLA-215 bar checks -- and it scored the batch's only real copy at 0.431 and
    passed it. The branch fired correctly; the NUMBER handed to it was wrong. A harness proves a
    guard FIRES, never that it MEASURES the right thing, so the metric needs assertions of its own.

    THREE dilutions have now been found in this one metric:
      1. `autojunk` engages at 200 characters and junks any character in over 1% of the sequence,
         which describes every seasoned register.  (found batch 23)
      2. a MEAN of the two registers dilutes one copied register against one independent one.
         (found batch 23)
      3. difflib's matcher is GREEDY, so `ratio(a, b) != ratio(b, a)` -- by up to 0.271 on this
         corpus, and the batch-first order under-scores in 607 of 1200 sampled pairs.  (found here)
    """

    LONG_A = ("Work a shallow cultivation through the bed as soon as the last harvest is off, "
              "turning under the trimmings and the papery skins so the overwintering stages lose "
              "the shelter they need, and follow it with a second pass once the surface has "
              "dried enough to crumble rather than smear.")
    LONG_B = ("Lift the spent plants whole and compost them well away from the bed, then rake the "
              "surface clean so nothing is left standing to carry the problem into the following "
              "season, and give the ground a fortnight to settle before anything else goes in.")
    LONG_C = ("Clear the bed down to bare soil after the last pull, taking the debris right out "
              "of the garden, because anything left lying is somewhere the trouble can sit out "
              "the winter in comfort and start again the next season.")

    def _pair(self):
        """One register copied VERBATIM, one written independently: the real defect's shape."""
        return ({"note_beginner": self.LONG_A, "note_seasoned": self.LONG_B},
                {"note_beginner": self.LONG_A, "note_seasoned": self.LONG_C})

    # ---- dilution 1
    SHARED_RUN = ("turning under the trimmings and the papery skins so the overwintering stages "
                  "lose the shelter they need before the ground cools")
    DEFLATE_A = ("Work a shallow cultivation through the bed as soon as the last harvest is off, "
                 + SHARED_RUN + ", and go over it twice.")
    DEFLATE_B = ("Rake the surface clean once the crop is lifted, " + SHARED_RUN
                 + ", then leave the ground bare.")

    def test_autojunk_default_deflates_a_verbatim_run_ACROSS_the_threshold(self):
        """Not a cosmetic difference: autojunk engages at 200 characters and junks any character
        appearing in more than 1% of the sequence, which in a 200-character English sentence is
        very nearly every letter. Two notes sharing a 127-character VERBATIM run score 0.637 with
        it on -- under the threshold, shipped -- and 0.744 with it off. The defect is not that the
        number is lower; it is that the number lands on the other side of the line."""
        self.assertGreater(len(self.DEFLATE_A), 200)
        self.assertEqual(len(self.SHARED_RUN), 127)
        on = difflib.SequenceMatcher(None, self.DEFLATE_A, self.DEFLATE_B).ratio()
        off = difflib.SequenceMatcher(None, self.DEFLATE_A, self.DEFLATE_B,
                                      autojunk=False).ratio()
        self.assertLess(on, P.PRECEDENT_COPY_THRESHOLD, "the deflated score must PASS")
        self.assertGreaterEqual(off, P.PRECEDENT_COPY_THRESHOLD, "the true score must REFUSE")

    # ---- dilution 2
    def test_a_mean_of_two_registers_hides_one_copied_register(self):
        shipped, copied = self._pair()
        nb = difflib.SequenceMatcher(None, shipped["note_beginner"], copied["note_beginner"],
                                     autojunk=False).ratio()
        ns = difflib.SequenceMatcher(None, shipped["note_seasoned"], copied["note_seasoned"],
                                     autojunk=False).ratio()
        self.assertGreaterEqual(max(nb, ns), P.PRECEDENT_COPY_THRESHOLD)
        self.assertLess((nb + ns) / 2.0, P.PRECEDENT_COPY_THRESHOLD)

    # ---- dilution 3
    def test_difflib_is_asymmetric_so_argument_order_alone_moves_a_score(self):
        """Verified by an independent walk over the matching blocks: 52 characters matched one
        way, 11 the other, on the same two strings."""
        u = ("Pick off and get rid of the leaves that have gone pale and fuzzy, and clear sick "
             "foliage out of the bed instead of leaving it lying there.")
        v = ("Liming toward a neutral pH suppresses the pathogen; wet, acidic conditions are what "
             "favor infection, so this pairs with the drainage work rather than standing alone.")
        fwd = difflib.SequenceMatcher(None, u, v, autojunk=False)
        rev = difflib.SequenceMatcher(None, v, u, autojunk=False)
        self.assertNotAlmostEqual(fwd.ratio(), rev.ratio(), places=2)
        self.assertGreater(abs(fwd.ratio() - rev.ratio()), 0.20)
        self.assertEqual(sum(bl.size for bl in fwd.get_matching_blocks()), 52)
        self.assertEqual(sum(bl.size for bl in rev.get_matching_blocks()), 11)

    def test_the_shipped_metric_takes_the_max_of_both_orders(self):
        """Reads the guard's own scorer rather than trusting its comment."""
        import inspect
        src = inspect.getsource(P.check_no_precedent_copy)
        body = src[src.index("def score("):]
        code = "\n".join(l for l in body.splitlines() if "difflib.SequenceMatcher" in l)
        self.assertEqual(code.count("autojunk=False"), 2,
                         "both SequenceMatcher calls must disable autojunk")
        self.assertIn("difflib.SequenceMatcher(None, u, v, autojunk=False).ratio()", code)
        self.assertIn("difflib.SequenceMatcher(None, v, u, autojunk=False).ratio()", code)
        self.assertIn("max(difflib.SequenceMatcher", code)

    # ---- end to end, through the real guard
    def test_the_guard_refuses_the_pair_a_mean_would_have_passed(self):
        """The assertion that would have caught batch 23's copy."""
        d, b = _thin(), _staged()
        shipped, copied = self._pair()
        g = _live_prob(d, PRECEDENT, "onion-thrips")
        g["control_ladder"] = [dict(shipped, method="garden_sanitation")]
        _sprob(b, "shallot", "onion-thrips")["control_ladder"][0] = dict(
            copied, method="garden_sanitation")
        _expect(self, "similar to garlic's rung for the same problem and method",
                lambda: P.check_no_precedent_copy(b, d))

    def test_the_length_prune_never_hides_a_pair_the_exact_walk_would_catch(self):
        """The prune is an O(1) RIGOROUS bound (ratio is 2M/T and M cannot exceed the shorter
        length), not an approximation. Asserted against an unpruned walk on the thin fixture:
        same comparison counts, same worst, same value."""
        d, b = _thin(), _staged()
        pruned = P.check_no_precedent_copy(b, d)
        exact = _unpruned_precedent(b, d)
        self.assertEqual((pruned[0], pruned[1]), (exact[0], exact[1]))
        self.assertAlmostEqual(pruned[2][0], exact[2][0], places=9)
        self.assertEqual(pruned[2][1], exact[2][1])

    def test_the_measured_ceiling_is_reported_by_the_promote_and_still_holds(self):
        """The batch's real worst pair sits at 0.693 against a 0.70 threshold: 0.007 of headroom,
        taken from the promote's OWN printed output over all 18575 comparisons, so a later edit
        that pushes a rung over the line fails as a measurement change, not as a mystery."""
        out = _run_promote()["out"]
        self.assertIn("precedent scan    : %d + %d comparisons, worst %.3f"
                      % (EXPECTED_CMP_A, EXPECTED_CMP_B, EXPECTED_WORST), out)
        self.assertIn(EXPECTED_WORST_PAIR, out)


def _unpruned_precedent(batch, data):
    """An INDEPENDENT walk of the precedent scan with no pruning and no shared code, used only to
    prove the shipped guard's O(1) bound changes nothing. Deliberately re-derived rather than
    imported: a check that reuses the implementation it validates is vacuous."""
    by_idm, by_m = {}, {}
    for c in data["crops"]:
        if c["slug"] in P.CROPS:
            continue
        for _f, p in P.problems(c):
            for r in p.get("control_ladder") or []:
                rec = (c["slug"], p.get("id"), r.get("note_beginner") or "",
                       r.get("note_seasoned") or "")
                by_m.setdefault(r["method"], []).append(rec)
                if p.get("id"):
                    by_idm.setdefault((p["id"], r["method"]), []).append(rec)

    def sym(u, v):
        return max(difflib.SequenceMatcher(None, u, v, autojunk=False).ratio(),
                   difflib.SequenceMatcher(None, v, u, autojunk=False).ratio())

    cmp_a = cmp_b = 0
    worst = (0.0, None)
    for c in P.CROPS:
        for _f, p in P.problems(batch[c]):
            for r in p.get("control_ladder") or []:
                if (c, p["id"], r["method"]) in P.DECLARED_IDENTITIES:
                    continue
                rb, rs = r.get("note_beginner") or "", r.get("note_seasoned") or ""
                for lst, tag in ((by_idm.get((p["id"], r["method"]), []), "A"),
                                 (by_m.get(r["method"], []), "B")):
                    for _sl, _pid, nb, ns in lst:
                        if tag == "A":
                            cmp_a += 1
                            label = "A:%s/%s/%s vs %s" % (c, p["id"], r["method"], _sl)
                        else:
                            cmp_b += 1
                            label = "B:%s/%s/%s vs %s/%s" % (c, p["id"], r["method"], _sl, _pid)
                        s = max(sym(rb, nb), sym(rs, ns))
                        if s > worst[0]:
                            worst = (s, label)
    return cmp_a, cmp_b, worst


class ShippedProseEcho(unittest.TestCase):
    def test_whole_note_echo_refuses(self):
        d, b = _thin(), _staged()
        donor = (_live_prob(d, PRECEDENT, "white-rot").get("control_ladder") or [])[0]
        tgt = _sprob(b, "chives", "chives-rust")
        tgt["control_ladder"][0] = {"method": tgt["control_ladder"][0]["method"],
                                    "note_beginner": donor["note_beginner"],
                                    "note_seasoned": "Independently written seasoned register for "
                                                     "this driver, materially different."}
        _expect(self, "note_beginner is a verbatim echo of",
                lambda: P.check_no_shipped_prose_echo(b, d))

    def test_sentence_echo_refuses(self):
        d, b = _thin(), _staged()
        donor = (_live_prob(d, PRECEDENT, "white-rot").get("control_ladder") or [])[0]
        raw = None
        for s in (donor["note_seasoned"], donor["note_beginner"]):
            for piece in s.split(". "):
                if len(piece.strip()) > 40:
                    raw = piece.strip().rstrip(".") + "."
                    break
            if raw:
                break
        self.assertIsNotNone(raw, "no donor sentence clears the 40-character floor")
        tgt = _sprob(b, "chives", "chives-rust")
        tgt["control_ladder"][0] = {
            "method": tgt["control_ladder"][0]["method"],
            "note_beginner": "A fresh opening clause of my own. " + raw,
            "note_seasoned": "Independently written seasoned register, materially different."}
        _expect(self, "echoes a shipped sentence from",
                lambda: P.check_no_shipped_prose_echo(b, d))

    def test_declared_identity_is_EXEMPT_from_the_echo_scan(self):
        """WITHOUT THIS EXEMPTION TWO GUARDS CONTRADICT EACH OTHER. check_no_precedent_copy
        REQUIRES the declared rung to be byte-identical to spring-onion's; the echo scan forbids
        exactly that. The batch cannot pass either way, and the failure reads as bad data rather
        than as a guard conflict."""
        d, b = _thin(), _staged()
        P.check_no_shipped_prose_echo(b, d)          # green WITH the exemption
        with _Patch("DECLARED_IDENTITIES", {}):      # ...and RED without it
            _expect(self, "is a verbatim echo of",
                    lambda: P.check_no_shipped_prose_echo(b, d))

    def test_empty_corpus_anti_vacuity_branch(self):
        d, b = _thin(), _staged()
        for c in d["crops"]:
            for _f, p in P.problems(c):
                p["control_ladder"] = None
        _expect(self, "no shipped rung prose found; this guard would be vacuous",
                lambda: P.check_no_shipped_prose_echo(b, d))

    def test_no_notes_scanned_anti_vacuity_branch(self):
        _expect(self, "no batch notes scanned; this guard would be vacuous",
                lambda: P.check_no_shipped_prose_echo(
                    {c: {"pests": [], "diseases": []} for c in CROPS}, _thin()))

    def test_the_real_batch_echoes_nothing_roster_wide(self):
        P.check_no_shipped_prose_echo(_staged(), _pre())


class TemperatureWarranted(unittest.TestCase):
    def test_unwarranted_temperature_figure_refuses(self):
        d, b = _pre(), _staged()
        r = _sprob(b, "leek", "leek-rust")["control_ladder"][0]
        r["note_seasoned"] = r["note_seasoned"] + " Hold off above 118°F."
        _expect(self, "appears neither in the problem's own prose nor in the method's catalog "
                      "text",
                lambda: P.check_temperature_figures_warranted(b, P.by_slug(d),
                                                              d["control_methods"]))

    def test_pinned_figure_count_catches_a_REMOVED_figure(self):
        """The count is what makes a vanished figure as visible as an added one."""
        d, b = _pre(), _staged()
        r = [x for x in _sprob(b, "chives", "onion-thrips")["control_ladder"]
             if x["method"] == "insecticidal_soap"][0]
        r["note_seasoned"] = r["note_seasoned"].replace("90°F", "the heat of the day")
        _expect(self, "found 9 temperature figures, pinned 10",
                lambda: P.check_temperature_figures_warranted(b, P.by_slug(d),
                                                              d["control_methods"]))

    def test_the_three_warranted_figures_are_where_the_promote_says_they_are(self):
        b = _staged()
        found = [(c, p["id"], r["method"], hit)
                 for c in CROPS for _f, p in P.problems(b[c]) for r in p["control_ladder"]
                 for k in P.ADVICE_FIELDS for hit in P.TEMP_FIGURE.findall(r.get(k) or "")]
        self.assertEqual(len(found), P.EXPECTED_TEMP_FIGURES)
        self.assertEqual({f[0] for f in found}, {"chives", "leek", "onion", "shallot"})
        self.assertEqual(sorted(f[3] for f in found), ["50°F", "50°F", "50°F", "50°F", "59°F", "75°F", "75°F", "85°F", "85°F", "90°F"])


class LadderVocabulary(unittest.TestCase):
    def test_internal_vocabulary_refuses(self):
        b = _staged()
        _sprob(b, "onion", "pink-root")["control_ladder"][0]["note_beginner"] = \
            "Start with the first rung and work down."
        _expect(self, "uses internal vocabulary", lambda: P.check_no_ladder_vocabulary(b))

    def test_anti_vacuity_branch(self):
        _expect(self, "no notes scanned for vocabulary; this guard would be vacuous",
                lambda: P.check_no_ladder_vocabulary(
                    {c: {"pests": [], "diseases": []} for c in CROPS}))

    def test_the_real_batch_carries_none(self):
        P.check_no_ladder_vocabulary(_staged())


class ValidateBatch(unittest.TestCase):
    def setUp(self):
        self.cm = _pre()["control_methods"]

    def test_empty_ladder_refuses(self):
        b = _staged()
        _sprob(b, "leek", "pink-root")["control_ladder"] = []
        _expect(self, "has an empty ladder", lambda: P.validate_batch(b, self.cm))

    def test_unknown_method_refuses(self):
        b = _staged()
        _sprob(b, "leek", "pink-root")["control_ladder"][0]["method"] = "moon_phase_planting"
        _expect(self, "names unknown method 'moon_phase_planting'",
                lambda: P.validate_batch(b, self.cm))

    def test_duplicate_method_in_one_ladder_refuses(self):
        b = _staged()
        lad = _sprob(b, "shallot", "pink-root")["control_ladder"]
        lad.append(copy.deepcopy(lad[0]))
        _expect(self, "repeats method", lambda: P.validate_batch(b, self.cm))

    def test_tier_inversion_refuses(self):
        b = _staged()
        _sprob(b, "shallot", "onion-thrips")["control_ladder"].reverse()
        _expect(self, "tier decreases at", lambda: P.validate_batch(b, self.cm))

    def test_unknown_tier_refuses(self):
        b, cm = _staged(), copy.deepcopy(self.cm)
        cm[_sprob(b, "leek", "pink-root")["control_ladder"][0]["method"]]["tier"] = "folkloric"
        _expect(self, "has unknown tier 'folkloric'", lambda: P.validate_batch(b, cm))

    def test_applies_to_incoherence_refuses(self):
        b, cm = _staged(), copy.deepcopy(self.cm)
        cm[_sprob(b, "leek", "pink-root")["control_ladder"][0]["method"]]["applies_to"] = ["mite"]
        _expect(self, "does not reach it", lambda: P.validate_batch(b, cm))

    def test_missing_register_refuses(self):
        b = _staged()
        _sprob(b, "onion", "pink-root")["control_ladder"][0]["note_seasoned"] = ""
        _expect(self, "missing a register", lambda: P.validate_batch(b, self.cm))

    def test_identical_registers_refuse(self):
        b = _staged()
        r = _sprob(b, "onion", "pink-root")["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        _expect(self, "registers are identical", lambda: P.validate_batch(b, self.cm))

    def test_unexpected_rung_key_refuses(self):
        b = _staged()
        _sprob(b, "onion", "pink-root")["control_ladder"][0]["severity"] = "high"
        _expect(self, "has unexpected rung keys ['severity']",
                lambda: P.validate_batch(b, self.cm))

    def test_hygiene_absolute_refuses(self):
        b = _staged()
        _sprob(b, "chives", "chives-rust")["control_ladder"][0]["note_beginner"] = \
            "This will completely stop the problem."
        _expect(self, "note_beginner: absolute:completely", lambda: P.validate_batch(b, self.cm))

    def test_hygiene_em_dash_refuses(self):
        b = _staged()
        _sprob(b, "chives", "chives-rust")["control_ladder"][0]["note_beginner"] = \
            "Cut the clump back — then water it in."
        _expect(self, "note_beginner: em/en dash", lambda: P.validate_batch(b, self.cm))

    def test_per_crop_rung_count_is_pinned(self):
        b = _staged()
        _sprob(b, "chives", "chives-rust")["control_ladder"].pop()
        _expect(self, "chives has 26 rungs, expected 27", lambda: P.validate_batch(b, self.cm))

    def test_the_absolute_vocabulary_is_not_empty(self):
        """A word list that can be emptied without a test noticing is a zero with extra steps.
        Enumerated by value rather than derived from the list it validates."""
        for w in ("always", "never", "completely", "totally", "harmless", "guaranteed",
                  "eliminate", "eliminates"):
            self.assertEqual(P.hygiene("It will %s." % w), ["absolute:%s" % w])
        self.assertEqual(P.hygiene("Water it in well."), [])

    def test_the_real_batch_validates(self):
        P.validate_batch(_staged(), self.cm)


class BlastRadius(unittest.TestCase):
    def test_clean_apply_touches_exactly_the_batch(self):
        self.assertEqual(P.verify_post(_pre_snap(), _post()), TOTAL_PROBLEMS)

    def test_snapshot_is_leaf_level_and_covers_the_whole_roster(self):
        d = _pre()
        self.assertEqual(len({k[0] for k in P.snapshot(d)}), len(d["crops"]))

    def test_unexpected_added_leaf_key_refuses(self):
        d = _post()
        _pre_prob(d, "leek", "Leek moth")["ladder_delta"] = {}
        _expect(self, "unexpected leaf keys added", lambda: P.verify_post(_pre_snap(), d))

    def test_dropped_leaf_key_refuses(self):
        d = _post()
        del _pre_prob(d, "onion", "Pink root")["severity"]
        _expect(self, "leaf keys dropped", lambda: P.verify_post(_pre_snap(), d))

    def test_added_key_count_is_pinned_at_three_per_problem(self):
        """`type` is an ADDED key here, not a changed value. Batch 23's 2-per-problem count
        refuses this batch outright, which is why the inherited driver does not transfer."""
        d = _post()
        del _pre_prob(d, "onion", "Pink root")["type"]
        _expect(self, "77 leaf keys added, expected 78", lambda: P.verify_post(_pre_snap(), d))

    def test_a_pre_existing_leaf_changing_refuses(self):
        d = _post()
        _pre_prob(d, "shallot", "White rot")["severity"] = "catastrophic"
        _expect(self, "changed pre-existing leaf", lambda: P.verify_post(_pre_snap(), d))

    def test_a_bystander_crop_changing_refuses(self):
        d = _post()
        _crop(d, PRECEDENT)["name"] = "Garlick"
        _expect(self, "changed pre-existing leaf", lambda: P.verify_post(_pre_snap(), d))

    def test_the_touched_and_per_crop_counts_are_FORWARD_assertions(self):
        """Both are verified UNREACHABLE and are withdrawn from the mutation harness rather than
        reported as permanent survivors. The arithmetic is asserted here so the withdrawal is a
        measured claim and not a note in a docstring:

        every added key is (batch crop, one of exactly 3 field names), so a touched triple can
        carry at most 3 keys and 81 added keys force exactly 27 triples; and each batch crop's
        pinned problem count IS its full problem count, so the per-crop split of 27 is forced too.
        An attempt to move a problem between two batch crops DROPS a leaf key and is refused three
        branches earlier."""
        self.assertEqual(sum(P.EXPECTED_PROBLEMS.values()) * 3,
                         3 * TOTAL_PROBLEMS, "the added-key count no longer forces the triples")
        d = _pre()
        for c in CROPS:
            self.assertEqual(len(P.problems(_crop(d, c))), P.EXPECTED_PROBLEMS[c],
                             "%s's pinned count is no longer its full problem count, so the "
                             "per-crop tally has become reachable and needs a driver" % c)
        # the nearest reachable attempt is refused earlier, by the DROPPED-key branch
        post = _post()
        moved = _crop(post, "onion")["diseases"].pop()
        _crop(post, "shallot")["diseases"].append(moved)
        _expect(self, "leaf keys dropped", lambda: P.verify_post(_pre_snap(), post))

    def test_set_equality_is_compared_before_any_value(self):
        """PLA-162's shape: iterating `pre` alone makes every ADDITION invisible. Asserted on the
        source so a refactor cannot quietly reorder it."""
        import inspect
        src = inspect.getsource(P.verify_post)
        self.assertLess(src.index("added, dropped = set(post) - set(pre)"),
                        src.index("if pre[k] != post[k]:"))


class CatalogUntouched(unittest.TestCase):
    def setUp(self):
        d = _pre()
        self.cm = P.serialize(d["control_methods"])
        self.sc = P.serialize(d["source_catalog"])

    def test_control_methods_change_refuses(self):
        d = _pre()
        d["control_methods"]["crop_rotation"]["tier"] = "physical"
        _expect(self, "control_methods changed; this batch mints nothing",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_source_catalog_change_refuses(self):
        d = _pre()
        d["source_catalog"][sorted(d["source_catalog"])[0]]["name"] = "changed"
        _expect(self, "source_catalog changed",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_the_real_batch_touches_neither(self):
        P.check_catalog_untouched(self.cm, self.sc, _post())

    def test_the_catalog_is_byte_identical_across_the_promote(self):
        post = _post()
        self.assertEqual(P.serialize(post["control_methods"]), self.cm)
        self.assertEqual(P.serialize(post["source_catalog"]), self.sc)


class MainWiringIsDriven(unittest.TestCase):
    """RECURRED at catalog r8: 53 green tests and `main()` never called `check()`. Every guard
    must be reachable from the ENTRY POINT, not only from the suite."""

    def test_apply_to_routes_through_check(self):
        calls = []

        def spy(_data):
            calls.append(1)
            raise SystemExit("SPY REACHED CHECK")
        with _Patch("check", spy):
            with self.assertRaises(SystemExit):
                P.apply_to(_pre())
        self.assertEqual(calls, [1], "apply_to did not route through check()")

    def test_check_calls_every_guard_this_suite_drives(self):
        import inspect
        src = inspect.getsource(P.check)
        for g in ("check_schema_premise", "check_type_set_from_nothing", "check_ids",
                  "check_id_adjudications", "check_no_template_twins_premise",
                  "check_no_precedent_copy", "check_no_shipped_prose_echo",
                  "check_temperature_figures_warranted", "check_no_ladder_vocabulary",
                  "validate_batch"):
            self.assertIn(g + "(", src, "%s is never reached from check()" % g)

    def test_main_runs_verify_post_and_the_catalog_check(self):
        import inspect
        src = inspect.getsource(P.main)
        self.assertIn("verify_post(pre, data)", src)
        self.assertIn("check_catalog_untouched(before_cm, before_sc, data)", src)
        self.assertIn("if sha != expect:", src)

    def test_end_to_end_through_main_reports_the_pinned_counts(self):
        out = _run_promote()["out"]
        self.assertIn("problems laddered : 26", out)
        self.assertIn("rungs             : 95", out)
        self.assertIn("post  SHA         : " + POST_SHA, out)

    def test_a_wrong_base_sha_is_refused_by_main(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(P.serialize({"crops": [], "control_methods": {}, "source_catalog": {}}))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, path],
                               capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("REFUSED: base SHA", r.stdout + r.stderr)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main(verbosity=1)
