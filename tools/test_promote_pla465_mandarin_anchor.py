#!/usr/bin/env python3
"""Guard suite for promote_pla465_mandarin_anchor -- PLA-465's owed repair of the crop's ucr_citrus anchor.
THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla465_mandarin_anchor_suite.py.

The defect class this suite exists for is OVER-REACH: the recorded reason ("the crop's cited UCR anchor is
a satsuma page, the wrong scion") is wider than the defect, and a promote that believed it would strip the
eight correct attributions. So the KEEP and HELD cells are pinned on BOTH sides, and the cell census is
compared against an ENUMERATED constant rather than derived from the walk it validates."""
import copy, json, os, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla465_mandarin_anchor as P  # noqa: E402

BASE_SHA = "892c76fb9e89fd9a242f682a7040a71886cb128ec899092a4f6414d2e0708edb"
ROSTER = 128
N_REPOINTS = 7
N_KEEPS = 8
N_HELD = 3
N_DROPPED = 1
N_CELLS = 19
N_CELLS_AFTER = 18
N_FINDINGS = 2
CROP = "mandarin-clementine"
OLD = "https://citrusvariety.ucr.edu/crc3178"


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.spec = P.staged()

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def crop(self, data):
        return P.by_slug(data)[CROP]

    def anchor(self, data, path):
        return P.resolve(self.crop(data), path)["anchoring_urls"][P.KEY]

    def finding(self, data):
        return next(x for x in self.crop(data)["verification_status"]["open_findings"] if x["id"] == P.FINDING_ID)

    def post(self):
        return P.apply_to(self.fresh_data(), self.spec)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg, f"guard fired with the wrong message.\n  wanted: {fragment!r}\n  got: {msg!r}")


# ----------------------------------------------------------------- preflight and pins
class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(promote_fixture.pre_state(P.BASE_SHA)), BASE_SHA)

    def test_refuses_a_canonical_that_is_not_the_base(self):
        with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as f:
            f.write(b'{"crops":[]}')
        try:
            self.assertRefuses("this promote is pinned to", P.load_canonical, f.name)
        finally:
            os.remove(f.name)

    def test_fixture_is_the_full_roster(self):
        self.assertEqual(len(self.data["crops"]), ROSTER)

    def test_pins_are_the_literals(self):
        self.assertEqual(P.EXPECTED["repoints"], N_REPOINTS)
        self.assertEqual(P.EXPECTED["keeps"], N_KEEPS)
        self.assertEqual(P.EXPECTED["held"], N_HELD)
        self.assertEqual(P.EXPECTED["dropped"], N_DROPPED)
        self.assertEqual(P.EXPECTED["findings"], N_FINDINGS)
        self.assertEqual((P.CELLS_BEFORE, P.CELLS_AFTER), (N_CELLS, N_CELLS_AFTER))

    def test_the_four_classes_are_disjoint_and_cover_nineteen(self):
        r, k, h, d = set(P.REPOINT_PATHS), set(P.KEEP_PATHS), set(P.HELD_PATHS), {P.DROP_PATH}
        self.assertEqual((len(r), len(k), len(h), len(d)), (N_REPOINTS, N_KEEPS, N_HELD, N_DROPPED))
        for a, b in ((r, k), (r, h), (r, d), (k, h), (k, d), (h, d)):
            self.assertEqual(a & b, set())
        self.assertEqual(len(r | k | h | d), N_CELLS)

    def test_the_census_of_the_base_is_exactly_the_enumeration(self):
        """COVERAGE, not overlap: the independent walk of the committed base must equal the constant."""
        self.assertEqual(P.census(self.crop(self.data)),
                         set(P.REPOINT_PATHS) | set(P.KEEP_PATHS) | set(P.HELD_PATHS) | {P.DROP_PATH})

    def test_the_census_shrinks_by_exactly_the_dropped_cell(self):
        self.assertEqual(len(P.census(self.crop(self.post()))), N_CELLS_AFTER)
        self.assertNotIn(P.DROP_PATH, P.census(self.crop(self.post())))

    def test_every_cell_on_the_base_is_the_defective_anchor(self):
        for p in set(P.REPOINT_PATHS) | set(P.KEEP_PATHS) | set(P.HELD_PATHS) | {P.DROP_PATH}:
            rec = self.anchor(self.data, p)
            self.assertEqual(rec["url"], OLD, p)
            self.assertEqual(rec["verified"], P.VERIFIED_BEFORE, p)

    def test_the_clean_spec_and_base_are_ACCEPTED(self):
        """A guard can refuse correct input. Assert the matcher both ways."""
        self.assertEqual(P.check_spec_shape(self.spec), N_REPOINTS)
        self.assertEqual(P.check_pre_state(self.spec, self.fresh_data()), N_CELLS)
        post = self.post()
        P.check_post(post, self.spec)
        self.assertEqual(P.verify_post(self.data, post, self.spec), (N_REPOINTS, 1))

    def test_every_quoted_sha256_is_a_measured_evidence_digest(self):
        """A fabricated digest is the defect this guards: the field's shape pulls a plausible 64-hex
        string out of you after only a prefix has actually been measured."""
        quoted = set(P.SHA256_RE.findall(json.dumps(self.spec, ensure_ascii=False)))
        self.assertTrue(quoted)
        self.assertEqual(quoted - P.EVIDENCE_HASHES - {P.BASE_SHA}, set())

    def test_the_dropped_cell_retains_a_source_on_the_base(self):
        """Trevor's stop condition, encoded: this promote may not leave a claim-bearing cell uncited."""
        srcs = P.resolve(self.crop(self.data), P.DROP_PATH)["sources"]
        self.assertIn(P.KEY, srcs)
        self.assertTrue([x for x in srcs if x != P.KEY])

    def test_height_stays_null_on_both_sides(self):
        for d in (self.data, self.post()):
            for k in P.PDG.FIELDS:
                self.assertIsNone(self.crop(d).get(k), k)


# ----------------------------------------------------------------- spec shape
class SpecShape(Base):
    def test_refuses_a_spec_on_another_base(self):
        s = self.fresh_spec(); s["base_sha"] = "0" * 64
        self.assertRefuses("spec base_sha is not the pinned base", P.check_spec_shape, s)

    def test_refuses_a_spec_targeting_another_crop_or_key(self):
        s = self.fresh_spec(); s["crop"] = "lemon"
        self.assertRefuses("does not target the pinned crop and source key", P.check_spec_shape, s)

    def test_refuses_a_spec_that_does_not_pin_the_prior_anchor(self):
        s = self.fresh_spec(); s["verified_before"] = "2026-01-01"
        self.assertRefuses("does not pin the prior url and verified date", P.check_spec_shape, s)

    def test_refuses_a_repoint_count_drift(self):
        s = self.fresh_spec(); s["repoints"] = s["repoints"][:-1]
        self.assertRefuses("repoints, pinned", P.check_spec_shape, s)

    def test_refuses_repoint_paths_that_are_not_the_pinned_set(self):
        s = self.fresh_spec(); s["repoints"][0]["path"] = "storage"
        self.assertRefuses("not the pinned REPOINT set", P.check_spec_shape, s)

    def test_refuses_a_repoint_row_with_the_wrong_keys(self):
        s = self.fresh_spec(); s["repoints"][0]["extra"] = 1
        self.assertRefuses("has keys", P.check_spec_shape, s)

    def test_refuses_a_duplicated_repoint_path(self):
        """Reached by defeating the ordered-path pin, which fires first on a plain duplicate."""
        s = self.fresh_spec()
        s["repoints"][1] = copy.deepcopy(s["repoints"][0])
        P.REPOINT_PATHS_SAVED = P.REPOINT_PATHS
        try:
            P.REPOINT_PATHS = tuple([s["repoints"][0]["path"]] + [r["path"] for r in s["repoints"][1:]])
            self.assertRefuses("appears twice", P.check_spec_shape, s)
        finally:
            P.REPOINT_PATHS = P.REPOINT_PATHS_SAVED

    def test_refuses_a_repoint_that_does_not_move_off_the_defective_anchor(self):
        s = self.fresh_spec(); s["repoints"][0]["from"] = P.CRC0279
        self.assertRefuses("does not move off the pinned old url", P.check_spec_shape, s)

    def test_refuses_a_repoint_to_an_unadjudicated_accession(self):
        s = self.fresh_spec(); s["repoints"][0]["to"] = "https://citrusvariety.ucr.edu/crc9999"
        self.assertRefuses("not an adjudicated accession", P.check_spec_shape, s)

    def test_refuses_a_repoint_carrying_a_stale_verified_date(self):
        s = self.fresh_spec(); s["repoints"][0]["verified"] = P.VERIFIED_BEFORE
        self.assertRefuses("must carry the date the new url was verified", P.check_spec_shape, s)

    def test_refuses_an_empty_or_em_dashed_rationale(self):
        s = self.fresh_spec(); s["repoints"][0]["why"] = "  "
        self.assertRefuses("empty or em-dashed rationale", P.check_spec_shape, s)
        s = self.fresh_spec(); s["repoints"][0]["why"] = "an em—dash"
        self.assertRefuses("empty or em-dashed rationale", P.check_spec_shape, s)

    def test_refuses_a_target_split_drift(self):
        s = self.fresh_spec(); s["repoints"][0]["to"] = P.CRC3913
        self.assertRefuses("target split is", P.check_spec_shape, s)

    def test_refuses_a_field_addition_with_the_wrong_keys(self):
        s = self.fresh_spec(); del s["field_addition"]["sources"]
        self.assertRefuses("field_addition has keys", P.check_spec_shape, s)

    def test_refuses_a_field_addition_that_does_not_name_the_field(self):
        s = self.fresh_spec(); s["field_addition"]["field"] = "plant_dimensions"
        self.assertRefuses("must name the field and carry the pass date", P.check_spec_shape, s)

    def test_refuses_a_field_addition_crediting_the_wrong_source(self):
        s = self.fresh_spec(); s["field_addition"]["sources"] = ["uf_ifas_edis"]
        self.assertRefuses("must credit the source key it repairs", P.check_spec_shape, s)

    def test_refuses_an_em_dashed_provenance_note(self):
        s = self.fresh_spec(); s["field_addition"]["note"] = "a note with an em—dash"
        self.assertRefuses("note is empty or carries an em dash", P.check_spec_shape, s)

    def test_refuses_a_provenance_note_that_does_not_name_the_urls(self):
        s = self.fresh_spec(); s["field_addition"]["note"] = s["field_addition"]["note"].replace(P.CRC3913, "a page")
        self.assertRefuses("does not name", P.check_spec_shape, s)

    def test_refuses_an_addendum_shape(self):
        s = self.fresh_spec(); s["addendum"]["extra"] = 1
        self.assertRefuses("addendum has the wrong shape", P.check_spec_shape, s)

    def test_refuses_an_addendum_targeting_another_finding(self):
        s = self.fresh_spec(); s["addendum"]["id"] = "some_other_finding"
        self.assertRefuses("does not target the pinned finding", P.check_spec_shape, s)

    def test_refuses_an_addendum_without_the_dated_marker(self):
        s = self.fresh_spec(); s["addendum"]["suffix"] = " a bare sentence]"
        self.assertRefuses("must open with the dated marker", P.check_spec_shape, s)

    def test_refuses_an_em_dash_in_the_addendum(self):
        s = self.fresh_spec(); s["addendum"]["suffix"] = P.ADDENDUM_MARK + " an em—dash]"
        self.assertRefuses("addendum carries an em dash", P.check_spec_shape, s)

    def test_refuses_an_expected_block_drift(self):
        s = self.fresh_spec(); s["expected"] = dict(s["expected"], keeps=99)
        self.assertRefuses("expected block is not the promote's pins", P.check_spec_shape, s)


# ----------------------------------------------------------------- the drop and the findings (spec)
class DropAndFindingsSpec(Base):
    def test_refuses_a_drop_block_with_the_wrong_shape(self):
        s = self.fresh_spec(); s["drop"]["extra"] = 1
        self.assertRefuses("drop block has the wrong shape", P.check_spec_shape, s)

    def test_refuses_a_drop_targeting_another_cell_or_key(self):
        s = self.fresh_spec(); s["drop"]["source_key"] = "uhawaii_ctahr"
        self.assertRefuses("does not target the pinned cell, key and url", P.check_spec_shape, s)

    def test_refuses_a_drop_of_a_cell_another_class_claims(self):
        """A path cannot be both dropped and kept. Reached by pointing the drop at a KEEP cell."""
        s = self.fresh_spec(); s["drop"]["path"] = "storage"
        saved = P.DROP_PATH
        try:
            P.DROP_PATH = "storage"
            self.assertRefuses("also claimed by another class", P.check_spec_shape, s)
        finally:
            P.DROP_PATH = saved

    def test_refuses_a_drop_that_names_no_retained_source(self):
        s = self.fresh_spec(); s["drop"]["must_retain"] = []
        self.assertRefuses("a drop that leaves a claim-bearing cell uncited", P.check_spec_shape, s)

    def test_refuses_an_empty_or_em_dashed_drop_rationale(self):
        s = self.fresh_spec(); s["drop"]["why"] = "an em—dash"
        self.assertRefuses("drop rationale is empty or carries an em dash", P.check_spec_shape, s)

    def test_refuses_a_findings_count_drift(self):
        s = self.fresh_spec(); s["findings"] = s["findings"][:1]
        self.assertRefuses("findings, pinned", P.check_spec_shape, s)

    def test_refuses_finding_ids_that_are_not_the_pinned_ids(self):
        s = self.fresh_spec(); s["findings"][0]["entry"]["id"] = "something_else"
        self.assertRefuses("not the pinned ids, in order", P.check_spec_shape, s)

    def test_refuses_a_finding_on_another_crop(self):
        s = self.fresh_spec(); s["findings"][0]["crop"] = "lemon"
        self.assertRefuses("a finding targets another crop", P.check_spec_shape, s)

    def test_refuses_a_finding_with_the_wrong_keys(self):
        s = self.fresh_spec(); del s["findings"][0]["entry"]["deferred_to"]
        self.assertRefuses("has keys", P.check_spec_shape, s)

    def test_refuses_a_blocking_finding(self):
        s = self.fresh_spec(); s["findings"][0]["entry"]["blocks_launch"] = True
        self.assertRefuses("must be non-blocking and filed in", P.check_spec_shape, s)

    def test_refuses_a_finding_status_outside_the_vocabulary(self):
        s = self.fresh_spec(); s["findings"][0]["entry"]["status"] = "resolved"
        self.assertRefuses("not in", P.check_spec_shape, s)

    def test_refuses_a_deferred_finding_with_no_route(self):
        """The span finding is routed to PLA-559; stripping the route must refuse."""
        s = self.fresh_spec(); s["findings"][1]["entry"]["deferred_to"] = None
        self.assertRefuses("deferred_to must be set iff status is deferred", P.check_spec_shape, s)

    def test_refuses_an_empty_finding_summary(self):
        s = self.fresh_spec(); s["findings"][0]["entry"]["summary"] = "  "
        self.assertRefuses("has an empty summary or resolution_note", P.check_spec_shape, s)

    def test_refuses_an_em_dash_in_a_finding(self):
        s = self.fresh_spec(); s["findings"][0]["entry"]["resolution_note"] = "an em—dash"
        self.assertRefuses("carries an em dash", P.check_spec_shape, s)

    def test_refuses_a_fabricated_sha256_anywhere_in_the_spec(self):
        """THE NEAR-MISS THIS GUARD EXISTS FOR: on the re-stage a plausible 64-hex digest was written
        into a finding after only its first 16 characters had actually been measured."""
        s = self.fresh_spec()
        e = s["findings"][0]["entry"]
        real = sorted(P.EVIDENCE_HASHES)[0]
        e["summary"] = e["summary"] + " sha256 " + ("a" * 64)
        self.assertRefuses("is not a measured evidence digest", P.check_spec_shape, s)
        # and the matcher the other way: a MEASURED digest in the same position is accepted
        e["summary"] = e["summary"].replace("a" * 64, real)
        self.assertEqual(P.check_spec_shape(s), N_REPOINTS)


# ----------------------------------------------------------------- pre-state
class PreState(Base):
    def test_refuses_a_roster_drift(self):
        d = self.fresh_data(); d["crops"] = d["crops"][:-1]
        self.assertRefuses("roster is", P.check_pre_state, self.spec, d)

    def test_refuses_a_crop_off_the_roster(self):
        d = self.fresh_data(); d["crops"] = [c for c in d["crops"] if c["slug"] != CROP]
        d["crops"].append(copy.deepcopy(d["crops"][0])); d["crops"][-1]["slug"] = "ghost-crop"
        self.assertRefuses("is not on the roster", P.check_pre_state, self.spec, d)

    def test_refuses_an_uncertified_crop(self):
        d = self.fresh_data(); self.crop(d)["verification_status"]["status"] = "shell"
        self.assertRefuses("is not certified", P.check_pre_state, self.spec, d)

    def test_refuses_a_class_enumeration_that_does_not_cover_nineteen(self):
        """The three class tuples ARE the expectation. If one loses a path, the union stops being the
        census and the promote must refuse rather than silently validate against a smaller constant."""
        saved = P.HELD_PATHS
        try:
            P.HELD_PATHS = P.HELD_PATHS[:-1]
            self.assertRefuses("distinct cells, pinned", P.check_pre_state, self.spec, self.fresh_data())
        finally:
            P.HELD_PATHS = saved

    def test_refuses_a_census_with_an_unaccounted_cell(self):
        """A ucr_citrus cell appearing where the enumeration does not expect one."""
        d = self.fresh_data()
        self.crop(d)["pollination"] = {"anchoring_urls": {P.KEY: {"url": OLD, "verified": P.VERIFIED_BEFORE}}}
        self.assertRefuses("cell census moved", P.check_pre_state, self.spec, d)

    def test_refuses_a_census_that_lost_a_cell(self):
        d = self.fresh_data()
        del P.resolve(self.crop(d), "storage")["anchoring_urls"][P.KEY]
        self.assertRefuses("cell census moved", P.check_pre_state, self.spec, d)

    def test_refuses_an_anchor_record_with_the_wrong_keys(self):
        d = self.fresh_data(); self.anchor(d, "storage")["note"] = "x"
        self.assertRefuses("record is missing or has keys", P.check_pre_state, self.spec, d)

    def test_refuses_a_cell_not_on_the_defective_anchor(self):
        d = self.fresh_data(); self.anchor(d, "storage")["url"] = P.CRC0279
        self.assertRefuses("not the defective anchor this promote repairs", P.check_pre_state, self.spec, d)

    def test_refuses_a_cell_at_another_verified_date(self):
        d = self.fresh_data(); self.anchor(d, "storage")["verified"] = "2025-01-01"
        self.assertRefuses("not the pinned prior date", P.check_pre_state, self.spec, d)

    def test_refuses_field_additions_not_a_list(self):
        d = self.fresh_data(); self.crop(d)["verification_status"]["field_additions"] = {}
        self.assertRefuses("are not lists", P.check_pre_state, self.spec, d)

    def test_refuses_a_provenance_record_already_present(self):
        d = self.fresh_data()
        self.crop(d)["verification_status"]["field_additions"].append({"field": P.FA_FIELD, "date": "x", "sources": [], "note": "n"})
        self.assertRefuses("already carries a", P.check_pre_state, self.spec, d)

    def test_refuses_an_addendum_target_not_found_once(self):
        d = self.fresh_data()
        of = self.crop(d)["verification_status"]["open_findings"]
        of[:] = [x for x in of if x.get("id") != P.FINDING_ID]
        self.assertRefuses("matches 0 findings", P.check_pre_state, self.spec, d)

    def test_refuses_an_addendum_already_applied(self):
        d = self.fresh_data(); self.finding(d)["summary"] += P.ADDENDUM_MARK + " already]"
        self.assertRefuses("already carries this addendum", P.check_pre_state, self.spec, d)

    def test_refuses_a_drop_when_the_cell_does_not_cite_the_key(self):
        d = self.fresh_data()
        node = P.resolve(self.crop(d), P.DROP_PATH)
        node["sources"] = [x for x in node["sources"] if x != P.KEY]
        self.assertRefuses("there is nothing to drop", P.check_pre_state, self.spec, d)

    def test_refuses_a_drop_that_would_leave_the_cell_uncited(self):
        """Trevor's stop condition as a REFUSAL, not a workaround: if the credit is the cell's only
        source, the targeted T1 read has to come first and this promote must decline."""
        d = self.fresh_data()
        P.resolve(self.crop(d), P.DROP_PATH)["sources"] = [P.KEY]
        self.assertRefuses("may not be left uncited by this promote", P.check_pre_state, self.spec, d)

    def test_refuses_a_retained_source_set_that_moved_since_staging(self):
        d = self.fresh_data()
        P.resolve(self.crop(d), P.DROP_PATH)["sources"] = [P.KEY, "uf_ifas_edis"]
        self.assertRefuses("not the staged", P.check_pre_state, self.spec, d)

    def test_refuses_a_finding_already_present(self):
        d = self.fresh_data()
        self.crop(d)["verification_status"]["open_findings"].append(
            {"id": P.FINDING_IDS[0], "severity": "low", "status": "accepted", "blocks_launch": False,
             "filed_in_session": P.SESSION, "summary": "s", "resolution_note": "r", "deferred_to": None})
        self.assertRefuses("already carries finding", P.check_pre_state, self.spec, d)

    def test_refuses_a_crop_that_carries_a_dimension(self):
        d = self.fresh_data(); self.crop(d)[P.PDG.FIELDS[0]] = [8, 12]
        self.assertRefuses("height stays null", P.check_pre_state, self.spec, d)


# ----------------------------------------------------------------- post gates
class PostGates(Base):
    def test_refuses_a_census_change_across_the_write(self):
        post = self.post()
        self.crop(post)["pollination"] = {"anchoring_urls": {P.KEY: {"url": OLD, "verified": P.VERIFIED_BEFORE}}}
        self.assertRefuses("census changed across the write", P.check_post, post, self.spec)

    def test_refuses_a_keep_cell_that_moved(self):
        post = self.post(); self.anchor(post, "storage")["url"] = P.CRC0279
        self.assertRefuses("must not move", P.check_post, post, self.spec)

    def test_refuses_a_held_cell_that_moved(self):
        post = self.post(); self.anchor(post, P.HELD_PATHS[0])["url"] = P.CRC0279
        self.assertRefuses("must not move", P.check_post, post, self.spec)

    def test_refuses_a_repoint_that_did_not_land(self):
        post = self.post(); self.anchor(post, P.REPOINT_PATHS[0])["url"] = OLD
        self.assertRefuses("did not land on its adjudicated accession", P.check_post, post, self.spec)

    def test_a_drop_left_in_anchoring_urls_refuses_on_the_census_not_a_separate_check(self):
        """Pins WHICH guard catches this, so a separate (and unreachable) anchoring_urls check is not
        re-added later as phantom coverage: census() is the predicate `anchoring_urls carries KEY`."""
        post = self.post()
        P.resolve(self.crop(post), P.DROP_PATH)["anchoring_urls"][P.KEY] = {"url": OLD, "verified": P.VERIFIED_BEFORE}
        self.assertRefuses("census changed across the write", P.check_post, post, self.spec)

    def test_refuses_a_drop_left_in_sources(self):
        """A drop must clear BOTH halves; clearing only anchoring_urls leaves a dangling credit."""
        post = self.post()
        P.resolve(self.crop(post), P.DROP_PATH)["sources"].append(P.KEY)
        self.assertRefuses("a drop must clear BOTH", P.check_post, post, self.spec)

    def test_refuses_a_dropped_cell_left_uncited_in_the_post_state(self):
        post = self.post()
        P.resolve(self.crop(post), P.DROP_PATH)["sources"] = []
        self.assertRefuses("retains", P.check_post, post, self.spec)

    def test_the_post_census_set_implies_its_count(self):
        """Pins that CELLS_AFTER is checked by the SET comparison, not by a separate count: the three
        classes that survive the write have exactly CELLS_AFTER members, so a count guard in check_post
        could never fail on its own and is deliberately absent."""
        self.assertEqual(len(set(P.REPOINT_PATHS) | set(P.KEEP_PATHS) | set(P.HELD_PATHS)), P.CELLS_AFTER)
        self.assertEqual(len(P.census(self.crop(self.post()))), P.CELLS_AFTER)

    def test_refuses_a_post_state_that_fails_url_health(self):
        """Emptied on a NON-ucr anchor deliberately: every ucr_citrus url is pinned to a literal by the
        KEEP/HELD and repoint loops above, which fire first, so blanking one of those would grade this
        guard caught for the wrong reason. url_health walks every source on the crop, which is the
        reachable path."""
        post = self.post()
        P.resolve(self.crop(post), "varieties")["anchoring_urls"]["uf_ifas_edis"]["url"] = ""
        self.assertRefuses("url_health_gate on the post-state", P.check_post, post, self.spec)

    def test_refuses_a_post_state_that_fails_the_dimensions_gate(self):
        post = self.post(); self.crop(post)[P.PDG.FIELDS[0]] = "tall"
        self.assertRefuses("plant_dimensions_gate on the post-state", P.check_post, post, self.spec)

    def test_refuses_a_launch_blocker_after_the_write(self):
        post = self.post()
        self.crop(post)["verification_status"]["open_findings"].append(
            {"id": "x", "severity": "high", "status": "accepted", "blocks_launch": True,
             "filed_in_session": P.SESSION, "summary": "s", "resolution_note": "r", "deferred_to": None})
        self.assertRefuses("carries a launch blocker after the write", P.check_post, post, self.spec)


# ----------------------------------------------------------------- blast radius
class BlastRadius(Base):
    def test_refuses_a_top_level_key_addition(self):
        post = self.post(); post["new_key"] = 1
        self.assertRefuses("top-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_top_level_change(self):
        post = self.post(); post["total_crops"] = 999
        self.assertRefuses("top-level key", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_roster_change(self):
        post = self.post()
        ghost = copy.deepcopy(post["crops"][0]); ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_untouched_crop_change(self):
        post = self.post(); P.by_slug(post)["lemon"]["name"] = "Lemon!"
        self.assertRefuses("untouched crop lemon changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_crop_level_key_addition(self):
        post = self.post(); self.crop(post)["new_key"] = 1
        self.assertRefuses("crop-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_anchor_record_key_addition(self):
        post = self.post(); self.anchor(post, P.REPOINT_PATHS[0])["note"] = "x"
        self.assertRefuses("anchor record key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_change_beyond_the_seven_anchor_records(self):
        post = self.post(); self.anchor(post, "storage")["verified"] = "2026-09-18"
        self.assertRefuses("changed beyond the seven anchor records", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_prose_change_on_the_repaired_crop(self):
        post = self.post(); self.crop(post)["storage"]["room_temp_beginner"] = "rewritten"
        self.assertRefuses("changed beyond the seven anchor records", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_key_addition(self):
        post = self.post(); self.crop(post)["verification_status"]["new_key"] = 1
        self.assertRefuses("verification_status key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_value_change(self):
        post = self.post(); self.crop(post)["verification_status"]["last_audited"] = "2099-01-01"
        self.assertRefuses("verification_status.last_audited changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_more_than_one_field_addition_append(self):
        post = self.post()
        self.crop(post)["verification_status"]["field_additions"].append({"field": "z", "date": "d", "sources": [], "note": "n"})
        self.assertRefuses("expected exactly one append", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_rewritten_field_additions_prefix(self):
        post = self.post(); self.crop(post)["verification_status"]["field_additions"][0]["note"] = "rewritten"
        self.assertRefuses("field_additions prefix is not byte-identical", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_appended_field_addition_other_than_the_spec(self):
        post = self.post(); self.crop(post)["verification_status"]["field_additions"][-1]["note"] += " extra"
        self.assertRefuses("appended field_addition is not the spec's record", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_open_findings_append(self):
        post = self.post()
        self.crop(post)["verification_status"]["open_findings"].append(
            {"id": "y", "severity": "low", "status": "accepted", "blocks_launch": False,
             "filed_in_session": P.SESSION, "summary": "s", "resolution_note": "r", "deferred_to": None})
        self.assertRefuses("expected exactly", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_appended_finding_other_than_the_spec(self):
        post = self.post()
        self.crop(post)["verification_status"]["open_findings"][-1]["summary"] += " extra"
        self.assertRefuses("appended findings are not the spec's records", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_drop_that_did_not_happen(self):
        post = self.post()
        node = P.resolve(self.crop(post), P.DROP_PATH)
        node["sources"] = [P.KEY] + node["sources"]
        node["anchoring_urls"][P.KEY] = {"url": OLD, "verified": P.VERIFIED_BEFORE}
        self.assertRefuses("was not actually dropped", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_addendum_target_key_addition(self):
        post = self.post(); self.finding(post)["new_key"] = 1
        self.assertRefuses("addendum target key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_addendum_summary_other_than_original_plus_suffix(self):
        post = self.post(); self.finding(post)["summary"] += " tacked on"
        self.assertRefuses("not the original plus the suffix", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_addendum_target_field_change(self):
        post = self.post(); self.finding(post)["severity"] = "high"
        self.assertRefuses("addendum target field", P.verify_post, self.data, post, self.spec)

    def test_refuses_another_open_finding_change(self):
        post = self.post()
        other = next(x for x in self.crop(post)["verification_status"]["open_findings"] if x.get("id") != P.FINDING_ID)
        other["summary"] = "rewritten"
        self.assertRefuses("other than the addendum target changed", P.verify_post, self.data, post, self.spec)

    def test_an_unapplied_addendum_refuses_on_the_summary_not_the_count(self):
        """The addenda COUNT is not separately guarded, and cannot be: an unapplied addendum refuses on the
        per-entry summary comparison, and a renamed target refuses as a changed non-target finding. This
        driver pins WHICH guard catches it, so the count check is not re-added later as phantom coverage."""
        post = self.fresh_data()
        c = self.crop(post)
        for r in self.spec["repoints"]:
            rec = P.resolve(c, r["path"])["anchoring_urls"][P.KEY]
            rec["url"], rec["verified"] = r["to"], r["verified"]
        node = P.resolve(c, P.DROP_PATH)
        node["sources"] = [x for x in node["sources"] if x != P.KEY]
        del node["anchoring_urls"][P.KEY]
        for f in self.spec["findings"]:
            c["verification_status"]["open_findings"].append(copy.deepcopy(f["entry"]))
        c["verification_status"]["field_additions"].append(copy.deepcopy(self.spec["field_addition"]))
        self.assertRefuses("not the original plus the suffix", P.verify_post, self.data, post, self.spec)


# ----------------------------------------------------------------- serialization
class Serialization(Base):
    def test_compact_no_trailing_newline(self):
        blob = P.serialize(self.post())
        self.assertNotIn(b"\n", blob)
        self.assertFalse(blob.endswith(b"\n"))
        self.assertIn(b'","', blob)

    def test_non_ascii_survives_unescaped(self):
        self.assertIn("°F".encode("utf-8"), P.serialize(self.post()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
