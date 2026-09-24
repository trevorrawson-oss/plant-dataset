#!/usr/bin/env python3
"""Guard suite for promote_pla581_critical_warnings -- PLA-581, register row 32.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical:
a suite pinned to live canonical goes silently vacuous the moment canonical moves on.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla581_critical_warnings_suite.py.

Every driver asserts the guard fired with ITS OWN message (assertRefuses), because a driver that
reddens on an earlier check grades its mutation caught for the wrong reason.

THE null -> [] CONTROL, by name: test_refuses_an_empty_list_where_the_ruling_writes_null. The
PLA-533 ratchet collapses null and [] on purpose (`not (x or [])`); in this promote that idiom would
let a crop read "assessed, none found" and pass, so null is checked by identity and this driver
proves the check can tell them apart.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla581_critical_warnings as P  # noqa: E402

BASE_SHA = "526788f2c34a7fe1c59e9427271c1d1738c6b6cce2c1d0524df715e4fc359659"
ROSTER = 128
N_CERT = 121
N_SHELLS = 7
N_WARNINGS = P.EXPECTED_WARNINGS
NULL_CROP = "basil"
SHELL = "avocado"
MAT = "container_material"   # the two-source warning


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.spec = P.staged()
        cls.post = P.apply_to(cls.data, cls.spec)

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def fresh_post(self):
        return copy.deepcopy(self.post)

    def w(self, spec, wid):
        return next(x for x in spec["container_safety"]["warnings"] if x["id"] == wid)

    def rec(self, spec, wid):
        return next(r for r in spec["container_safety"]["field_additions"]
                    if r["field"] == f"container_safety.{wid}")

    def crop(self, data, slug):
        return next(c for c in data["crops"] if c["slug"] == slug)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg,
                      f"guard fired with the wrong message.\n  wanted: {fragment!r}\n  got: {msg!r}")


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

    def test_pins_are_the_literals(self):
        self.assertEqual((P.EXPECTED_CERTIFIED, P.EXPECTED_SHELLS, P.EXPECTED_WARNINGS, ROSTER),
                         (N_CERT, N_SHELLS, N_WARNINGS, P.ROSTER))

    def test_the_ruling_is_enumerated_not_derived(self):
        """The ruled ids, severity, sources and titles, asserted as their own content."""
        self.assertEqual(P.EXPECTED_IDS, ["balcony_load", "container_material", "hanging_security"])
        self.assertEqual(P.EXPECTED_SEVERITY, "high")
        self.assertEqual(sorted(P.EXPECTED_SOURCES[MAT]), ["csu_ext", "uiuc_ext"])
        self.assertEqual(P.EXPECTED_CUT, {"mosquito", "lifting", "pounds_figure"})
        self.assertEqual({w: len(v) for w, v in P.EVIDENCE.items()},
                         {"balcony_load": 1, "container_material": 4, "hanging_security": 4})
        # every measured page is used as evidence, and no evidence page is unmeasured
        self.assertEqual(sorted({u for v in P.EVIDENCE.values() for u, _ in v}), sorted(P.EVIDENCE_HASHES))
        # the wood sentence was DROPPED (it sits under the rot question); the drip-to-placement one is in
        hs = [t for _, t in P.EVIDENCE["hanging_security"]]
        self.assertNotIn("Consider safety issues if wood containers are hanging.", hs)
        self.assertIn("Consider this when determining placement of a hanging container.", hs)
        self.assertIn("Exercise caution with treated lumber when growing food, or where toddlers are "
                      "concerned.", [t for _, t in P.EVIDENCE["container_material"]])

    def test_the_base_carries_neither_key_nor_any_record(self):
        self.assertNotIn("container_safety", self.data)
        self.assertEqual(sum(1 for c in self.data["crops"] if "critical_warnings" in c), 0)
        self.assertEqual(sum(1 for c in self.data["crops"]
                             for x in ((c.get("verification_status") or {}).get("field_additions") or [])
                             if str(x.get("field", "")).startswith(("critical_warnings", "container_safety"))), 0)

    def test_the_approved_copy_is_read_from_the_spec_document(self):
        """Section 14 is the oracle, all three warnings read, INCLUDING container_material, whose
        header wraps onto a second line (a one-line pattern silently read 2 of 3, caught only by the
        id-set refusal)."""
        ok = P.approved_copy()
        self.assertEqual(sorted(ok), sorted(P.EXPECTED_IDS))
        self.assertEqual(ok["container_material"][0], P.EXPECTED_TITLES["container_material"])
        self.assertTrue(ok["balcony_load"][2].endswith("It gives no weight figure."))
        self.assertTrue(ok["container_material"][1].startswith("Many kinds of containers can be used."))

    def test_section_4_4_is_byte_for_byte_the_approved_text(self):
        """Ruling: section 14 supersedes 4.4's bodies, and 4.4 STAYS as first approved. Pinned against
        the approval commit f1c29e3, so 4.4 cannot be edited into agreement with anything."""
        cut = lambda t: t.split("### 4.4 ", 1)[1].split("### 4.5 ", 1)[0]
        approved = subprocess.run(["git", "-C", os.path.dirname(HERE), "show",
                                   "f1c29e3:docs/superpowers/specs/2026-09-21-pla581-critical-warnings-field-shape.md"],
                                  capture_output=True, text=True, check=True).stdout
        self.assertEqual(cut(open(P.SPEC_DOC, encoding="utf-8").read()), cut(approved))

    def test_no_title_or_body_states_a_figure(self):
        import critical_warnings_gate as G
        for w in self.spec["container_safety"]["warnings"]:
            for k in ("title", "body_seasoned", "body_beginner"):
                self.assertIsNone(G._FIGURE.search(w[k]), f"{w['id']}.{k}")


class Pipeline(Base):
    def test_the_whole_pipeline_passes_and_writes_null_everywhere(self):
        P.check_spec_shape(self.fresh_spec())
        self.assertEqual(P.check_pre_state(self.fresh_spec(), self.fresh_data()), N_CERT)
        post = P.apply_to(self.fresh_data(), self.fresh_spec())
        self.assertEqual(P.check_post(post)["null"], N_CERT)
        self.assertEqual(P.verify_post(self.fresh_data(), post, self.fresh_spec()), N_CERT)
        self.assertTrue(all(c["critical_warnings"] is None for c in post["crops"] if P._certified(c)))
        self.assertEqual(sum(1 for c in post["crops"] if "critical_warnings" in c), N_CERT)

    def test_compact_no_trailing_newline(self):
        blob = P.serialize(self.post)
        self.assertFalse(blob.endswith(b"\n"))
        self.assertNotIn(b'": ', blob[:4000])
        self.assertNotIn(b"\n", blob)


class SpecShape(Base):
    def test_refuses_when_no_digest_is_measured(self):
        with mock.patch.dict(P.EVIDENCE_HASHES, clear=True):
            self.assertRefuses("no digest has been measured", P.check_spec_shape, self.fresh_spec())

    def test_refuses_a_spec_on_another_base(self):
        s = self.fresh_spec(); s["base_sha"] = "0" * 64
        self.assertRefuses("base_sha is not the pinned base", P.check_spec_shape, s)

    def test_refuses_a_fetch_date_drift(self):
        s = self.fresh_spec(); s["fetch_date"] = "2026-09-21"
        self.assertRefuses("fetch_date", P.check_spec_shape, s)

    def test_refuses_an_expected_block_drift(self):
        s = self.fresh_spec(); s["expected"]["warnings"] = 4
        self.assertRefuses("expected block", P.check_spec_shape, s)

    def test_refuses_a_page_set_other_than_the_measured_one(self):
        s = self.fresh_spec(); s["pages"].pop("uiuc_material")
        self.assertRefuses("spec pages are", P.check_spec_shape, s)

    def test_refuses_digests_swapped_between_two_pages(self):
        """Both halves of a swap are measured digests, so the blanket scan cannot see it."""
        s = self.fresh_spec()
        a, b = s["pages"]["uiuc_size"], s["pages"]["uiuc_material"]
        a["sha256"], b["sha256"] = b["sha256"], a["sha256"]
        self.assertRefuses("measured", P.check_spec_shape, s)
        self.assertRefuses("for that page", P.check_spec_shape, s)

    def test_refuses_evidence_other_than_the_ruled_sentences(self):
        s = self.fresh_spec(); s["evidence"]["balcony_load"][0]["sentence"] = "Pots are heavy."
        self.assertRefuses("evidence is not the ruled sentences", P.check_spec_shape, s)

    def test_refuses_evidence_for_a_missing_warning(self):
        s = self.fresh_spec(); s["evidence"].pop("hanging_security")
        self.assertRefuses("spec evidence covers", P.check_spec_shape, s)

    def test_refuses_a_fabricated_digest(self):
        s = self.fresh_spec(); s["cut"][0]["why"] += " sha256 " + "ab" * 32
        self.assertRefuses("not a measured evidence digest", P.check_spec_shape, s)

    def test_refuses_a_cut_ledger_missing_the_mosquito(self):
        s = self.fresh_spec(); s["cut"] = [c for c in s["cut"] if c["candidate"] != "mosquito"]
        self.assertRefuses("cut ledger is", P.check_spec_shape, s)

    def test_refuses_a_cut_with_no_reason(self):
        s = self.fresh_spec(); s["cut"][1]["why"] = " "
        self.assertRefuses("records no reason", P.check_spec_shape, s)

    def test_refuses_an_extra_key_in_container_safety(self):
        s = self.fresh_spec(); s["container_safety"]["applies_to"] = "container_ok"
        self.assertRefuses("container_safety has keys", P.check_spec_shape, s)

    def test_refuses_a_warning_order_swap(self):
        s = self.fresh_spec(); ws = s["container_safety"]["warnings"]; ws[0], ws[1] = ws[1], ws[0]
        self.assertRefuses("warning ids are", P.check_spec_shape, s)

    def test_refuses_a_fourth_warning(self):
        s = self.fresh_spec()
        s["container_safety"]["warnings"].append(dict(self.w(s, "balcony_load"), id="lifting"))
        self.assertRefuses("warning ids are", P.check_spec_shape, s)

    def test_refuses_a_non_null_stage(self):
        s = self.fresh_spec(); self.w(s, "balcony_load")["stage"] = "harvest"
        self.assertRefuses("class safety with stage null", P.check_spec_shape, s)

    def test_refuses_a_critical_severity(self):
        """Uniform `high` is the ruling; `critical` on one would claim a ranking no source makes."""
        s = self.fresh_spec(); self.w(s, "balcony_load")["severity"] = "critical"
        self.assertRefuses("uniform, modeled", P.check_spec_shape, s)

    def test_refuses_a_title_the_spec_doc_does_not_carry(self):
        """The literal and the document are BOTH oracles: a title matching a changed literal but not
        section 14 must still refuse."""
        s = self.fresh_spec(); self.w(s, "hanging_security")["title"] = "Hang it well"
        with mock.patch.dict(P.EXPECTED_TITLES, {"hanging_security": "Hang it well"}):
            self.assertRefuses("title is not the pinned one", P.check_spec_shape, s)

    def test_refuses_an_edited_title(self):
        s = self.fresh_spec(); self.w(s, "hanging_security")["title"] = "Hang it well"
        self.assertRefuses("title is not the pinned one", P.check_spec_shape, s)

    def test_refuses_body_copy_not_in_the_approved_spec(self):
        s = self.fresh_spec(); self.w(s, "balcony_load")["body_beginner"] += " Most decks hold plenty."
        self.assertRefuses("not the approved spec's section 14", P.check_spec_shape, s)

    def test_refuses_a_dropped_second_source(self):
        s = self.fresh_spec(); w = self.w(s, MAT)
        w["sources"] = ["uiuc_ext"]; w["anchoring_urls"].pop("csu_ext")
        self.assertRefuses("cites", P.check_spec_shape, s)

    def test_refuses_an_anchor_at_another_url(self):
        s = self.fresh_spec()
        self.w(s, "balcony_load")["anchoring_urls"]["uiuc_ext"]["url"] = "https://extension.illinois.edu/gardening"
        self.assertRefuses("anchor for uiuc_ext is not", P.check_spec_shape, s)

    def test_refuses_an_anchor_verified_on_another_date(self):
        """Carrying an old date onto a fresh read would fabricate the attribution (PLA-466)."""
        s = self.fresh_spec(); self.w(s, "balcony_load")["anchoring_urls"]["uiuc_ext"]["verified"] = "2026-09-21"
        self.assertRefuses("anchor for uiuc_ext is not", P.check_spec_shape, s)

    def test_refuses_a_missing_record(self):
        s = self.fresh_spec(); s["container_safety"]["field_additions"].pop()
        self.assertRefuses("one per ruled warning", P.check_spec_shape, s)

    def test_refuses_a_record_date_drift(self):
        s = self.fresh_spec(); self.rec(s, "balcony_load")["date"] = "2026-09-21"
        self.assertRefuses("is dated", P.check_spec_shape, s)

    def test_refuses_a_record_quoting_another_pages_digest(self):
        s = self.fresh_spec(); r = self.rec(s, "balcony_load")
        mine = P.EVIDENCE_HASHES[P.EXPECTED_SOURCES["balcony_load"]["uiuc_ext"]]
        other = P.EVIDENCE_HASHES[P.EXPECTED_SOURCES["hanging_security"]["uiuc_ext"]]
        r["note"] = r["note"].replace(mine, other)
        self.assertRefuses("does not quote that page's measured digest", P.check_spec_shape, s)

    def test_refuses_a_two_source_record_missing_one_digest(self):
        """container_material credits two pages; quoting one digest must not satisfy both."""
        s = self.fresh_spec(); r = self.rec(s, MAT)
        csu = P.EVIDENCE_HASHES[P.EXPECTED_SOURCES[MAT]["csu_ext"]]
        r["note"] = r["note"].replace(csu, "")
        self.assertRefuses("does not quote that page's measured digest", P.check_spec_shape, s)

    def test_refuses_a_record_without_its_sentence(self):
        s = self.fresh_spec(); r = self.rec(s, "hanging_security")
        r["note"] = r["note"].replace(P.EVIDENCE["hanging_security"][2][1], "")
        self.assertRefuses("does not quote the sentence it rests on", P.check_spec_shape, s)

    def test_refuses_a_record_missing_the_unanchored_pages_digest(self):
        """container_material rests on container-material-choices (treated lumber) WITHOUT anchoring
        it, so only the evidence walk can demand that page's digest in the record."""
        s = self.fresh_spec(); r = self.rec(s, MAT)
        r["note"] = r["note"].replace(P.EVIDENCE_HASHES[P._MAT], "")
        self.assertRefuses("does not quote that page's measured digest", P.check_spec_shape, s)

    def test_refuses_a_spec_doc_without_section_14(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# nothing here\n")
        try:
            self.assertRefuses("cannot locate section 14", P.check_spec_shape, self.fresh_spec(), f.name)
        finally:
            os.remove(f.name)

    def test_refuses_a_spec_doc_yielding_other_ids(self):
        doc = open(P.SPEC_DOC, encoding="utf-8").read()
        i = doc.index("\n## 14. ")  # rename the id inside SECTION 14, the oracle, not in 4.4
        doc = doc[:i] + doc[i:].replace("**`hanging_security`**", "**`hanging`**", 1)
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(doc)
        try:
            self.assertRefuses("section 14 yields copy for", P.check_spec_shape, self.fresh_spec(), f.name)
        finally:
            os.remove(f.name)


class PreState(Base):
    def test_refuses_a_roster_drift(self):
        d = self.fresh_data(); d["crops"].append(copy.deepcopy(self.crop(d, NULL_CROP)))
        self.assertRefuses("roster is", P.check_pre_state, self.fresh_spec(), d)

    def test_refuses_a_certified_count_drift(self):
        d = self.fresh_data(); self.crop(d, NULL_CROP)["verification_status"]["status"] = None
        self.assertRefuses("certified crops, pinned", P.check_pre_state, self.fresh_spec(), d)

    def test_refuses_a_dataset_already_carrying_container_safety(self):
        d = self.fresh_data(); d["container_safety"] = None
        self.assertRefuses("already carries container_safety", P.check_pre_state, self.fresh_spec(), d)

    def test_refuses_a_crop_already_carrying_the_key(self):
        d = self.fresh_data(); self.crop(d, NULL_CROP)["critical_warnings"] = None
        self.assertRefuses("already carries critical_warnings", P.check_pre_state, self.fresh_spec(), d)

    def test_refuses_a_prior_record(self):
        d = self.fresh_data()
        self.crop(d, NULL_CROP)["verification_status"]["field_additions"].append(
            {"field": "critical_warnings", "date": "2026-09-01", "sources": [], "note": "x"})
        self.assertRefuses("already records", P.check_pre_state, self.fresh_spec(), d)

    def test_refuses_a_staged_object_the_gate_rejects(self):
        s = self.fresh_spec(); self.w(s, "balcony_load")["body_beginner"] = "Two pots is the limit."
        self.assertRefuses("fails critical_warnings_gate", P.check_pre_state, s, self.fresh_data())


class Post(Base):
    def test_refuses_a_post_state_that_fails_the_gate(self):
        p = self.fresh_post(); self.crop(p, SHELL)["critical_warnings"] = None
        self.assertRefuses("critical_warnings_gate on the post-state", P.check_post, p)

    def test_refuses_an_inspected_population_other_than_pinned(self):
        """A GATE-CLEAN post-state that is still not what was ruled: one crop moved to [] WITH a
        record. The gate accepts it (it is a legitimate state); the pinned population does not."""
        p = self.fresh_post(); c = self.crop(p, NULL_CROP)
        c["critical_warnings"] = []
        c["verification_status"]["field_additions"].append(
            {"field": "critical_warnings", "date": "2026-09-23", "sources": ["uiuc_ext"], "note": "x"})
        self.assertRefuses("the gate inspected", P.check_post, p)


class BlastRadius(Base):
    def verify(self, post):
        return P.verify_post(self.fresh_data(), post, self.fresh_spec())

    def test_refuses_an_empty_list_where_the_ruling_writes_null(self):
        """THE null -> [] CONTROL. A crop's null turned into [] must redden: [] asserts 'assessed,
        none found' on a crop nobody assessed. A truthiness check would pass it."""
        p = self.fresh_post(); self.crop(p, NULL_CROP)["critical_warnings"] = []
        self.assertRefuses("the ruling writes null", self.verify, p)

    def test_refuses_a_false_where_the_ruling_writes_null(self):
        p = self.fresh_post(); self.crop(p, NULL_CROP)["critical_warnings"] = False
        self.assertRefuses("the ruling writes null", self.verify, p)

    def test_refuses_a_top_level_key_addition(self):
        p = self.fresh_post(); p["critical_warnings_schema"] = 1
        self.assertRefuses("top-level key set", self.verify, p)

    def test_refuses_a_top_level_key_removal(self):
        p = self.fresh_post(); p.pop("uscrn_soil_temp")
        self.assertRefuses("top-level key set", self.verify, p)

    def test_refuses_a_source_catalog_change(self):
        p = self.fresh_post(); p["source_catalog"]["uiuc_ext"]["accessed"] = "2026-09"
        self.assertRefuses("top-level key 'source_catalog' changed", self.verify, p)

    def test_refuses_a_written_object_other_than_the_staged_one(self):
        p = self.fresh_post(); p["container_safety"]["warnings"][0]["title"] = "Heavy"
        self.assertRefuses("is not the staged one", self.verify, p)

    def test_refuses_an_appended_crop(self):
        p = self.fresh_post(); p["crops"].append(dict(copy.deepcopy(self.crop(p, "lime")), slug="ghost-crop"))
        self.assertRefuses("crop roster changed", self.verify, p)

    def test_refuses_a_shell_change(self):
        p = self.fresh_post(); self.crop(p, SHELL)["name"] = "Avocado!"
        self.assertRefuses("shell avocado changed", self.verify, p)

    def test_refuses_a_crop_level_key_addition(self):
        p = self.fresh_post(); self.crop(p, NULL_CROP)["container_safety"] = None
        self.assertRefuses("crop key set", self.verify, p)

    def test_refuses_a_certified_crop_missing_the_key(self):
        p = self.fresh_post(); self.crop(p, NULL_CROP).pop("critical_warnings")
        self.assertRefuses("crop key set", self.verify, p)

    def test_refuses_a_change_outside_the_new_key(self):
        p = self.fresh_post()
        self.crop(p, NULL_CROP)["verification_status"]["field_additions"].append({"field": "x"})
        self.assertRefuses("field 'verification_status' changed", self.verify, p)


class Cli(Base):
    def run_main(self, *args):
        with tempfile.TemporaryDirectory() as d:
            base = os.path.join(d, "base.json")
            with open(base, "wb") as f:
                f.write(promote_fixture.pre_state(P.BASE_SHA))
            argv = [a.replace("{BASE}", base).replace("{DIR}", d) for a in args]
            r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla581_critical_warnings.py"),
                                "--canonical", base] + argv, capture_output=True, text=True)
            written = open(base, "rb").read()
            return r, written

    def test_check_writes_nothing(self):
        r, written = self.run_main("--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(P.sha256_bytes(written), BASE_SHA)

    def test_a_write_requires_expect_sha(self):
        r, written = self.run_main()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("requires --expect-sha", r.stderr)
        self.assertEqual(P.sha256_bytes(written), BASE_SHA)

    def test_a_wrong_expect_sha_refuses_and_writes_nothing(self):
        r, written = self.run_main("--expect-sha", "0" * 64)
        self.assertIn("REFUSED: expected", r.stderr)
        self.assertEqual(P.sha256_bytes(written), BASE_SHA)

    def _spec_with_titles(self, titles):
        s = self.fresh_spec()
        for w in s["container_safety"]["warnings"]:
            w["title"] = titles[w["id"]]
        return s

    def test_pending_titles_names_every_placeholder_and_only_those(self):
        """Both ways, and independent of whatever titles are staged today."""
        pend = {i: f"[TITLE PENDING: {i}]" for i in P.EXPECTED_IDS}
        self.assertEqual(P.pending_titles(self._spec_with_titles(pend)), P.EXPECTED_IDS)
        final = {i: f"A plain title for {i.replace('_', ' ')}" for i in P.EXPECTED_IDS}
        self.assertEqual(P.pending_titles(self._spec_with_titles(final)), [])
        mixed = dict(final, hanging_security="[TITLE PENDING: hanging_security]")
        self.assertEqual(P.pending_titles(self._spec_with_titles(mixed)), ["hanging_security"])

    def test_a_write_refuses_while_titles_are_pending(self):
        """Titles are authored in the claude.ai lane; nothing ships with placeholder wording. Run in
        process against a synthetic pending spec with the CORRECT --expect-sha, so the refusal can
        only come from the title guard, and assert the canonical bytes are untouched."""
        pend = {i: f"[TITLE PENDING: {i}]" for i in P.EXPECTED_IDS}
        spec = self._spec_with_titles(pend)
        good = P.sha256_bytes(P.serialize(P.apply_to(self.fresh_data(), spec)))
        with tempfile.TemporaryDirectory() as d:
            base = os.path.join(d, "base.json")
            with open(base, "wb") as f:
                f.write(promote_fixture.pre_state(P.BASE_SHA))
            argv = ["promote", "--canonical", base, "--expect-sha", good]
            # Both title oracles (the literal AND section 14) must agree with the synthetic titles,
            # or check_spec_shape refuses first and the driver never reaches the write guard.
            doc = {i: (pend[i],) + v[1:] for i, v in P.approved_copy().items()}
            with mock.patch.object(P, "staged", return_value=spec), \
                 mock.patch.object(P, "approved_copy", return_value=doc), \
                 mock.patch.dict(P.EXPECTED_TITLES, pend), mock.patch.object(sys, "argv", argv):
                self.assertRefuses("titles still pending", P.main)
            self.assertEqual(P.sha256_bytes(open(base, "rb").read()), BASE_SHA)

    def test_out_may_not_target_the_canonical(self):
        r, written = self.run_main("--out", "{BASE}")
        self.assertIn("--out may not target the canonical", r.stderr)
        self.assertEqual(P.sha256_bytes(written), BASE_SHA)


if __name__ == "__main__":
    unittest.main()
