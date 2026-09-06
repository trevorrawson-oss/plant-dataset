#!/usr/bin/env python3
"""Guard suite for promote_pla457_sulfur_oil_interval -- PLA-457, the sulfur/oil interval.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (`promote_fixture.pre_state`), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via `mutate_pla457_sulfur_oil_interval_suite.py`.

THE INSTRUMENT IS PINNED, NOT JUST THE OUTPUT. The ticket said 15 notes; the strict scan finds 15;
the pronoun-aware net finds 20. `test_the_net_finds_the_five_pronoun_statements` names the five the
strict scan misses, so a net that narrows back reddens here before it can under-count the fix.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import promote_fixture  # noqa: E402
import promote_pla457_sulfur_oil_interval as P  # noqa: E402

BASE_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"
OUTPUT_SHA = "e4e55a14be8c4f32dca69e6ab23b742c31d2236dd742f5230ae425835ff260aa"
ROSTER = 128
N_NOTES = 20
N_CROPS = 10
N_PRE = 22
N_POST = 22
N_NEW_SOURCES = 1
N_LEAVES = 20
CROPS = ("apple", "apricot", "cherry-sour", "cherry-sweet", "grape-tomato", "lemongrass", "oregano",
         "plum", "sage", "strawberry")
# The five statements the strict (sulfur AND oil in one sentence) scan cannot see: the rung's own
# material is "it". Named as literals, never derived from the scan.
PRONOUN_FIVE = {
    ("apple", "apple-scab", "sulfur"),
    ("oregano", "powdery-mildew", "sulfur"),
    ("sage", "powdery-mildew", "sulfur"),
    ("strawberry", "two-spotted-spider-mite", "horticultural_oil"),
    ("cherry-sweet", "black-cherry-aphid", "horticultural_oil"),
}


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.spec = P.staged()

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def post(self):
        return P.apply_to(self.data, self.spec)

    def row(self, spec, crop, pid, register=None):
        return next(r for r in spec["notes"] if r["crop"] == crop and r["id"] == pid
                    and (register is None or r["register"] == register))

    def rung(self, data, crop, field, pid, method):
        ent = next(p for p in P.by_slug(data)[crop][field] if p.get("id") == pid)
        return next(x for x in ent["control_ladder"] if x.get("method") == method)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg,
                      f"guard fired but with the wrong message.\n  wanted fragment: {fragment!r}\n"
                      f"  got: {msg!r}")


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(promote_fixture.pre_state(P.BASE_SHA)), BASE_SHA)

    def test_fixture_is_not_live_canonical_by_accident(self):
        self.assertEqual(len(json.loads(promote_fixture.pre_state(P.BASE_SHA))["crops"]), ROSTER)

    def test_the_spec_is_the_shape_measured(self):
        rows = P.note_rows(self.spec)
        self.assertEqual(len(rows), N_NOTES)
        self.assertEqual(tuple(sorted({r["crop"] for r in rows})), CROPS)
        self.assertEqual(sorted(self.spec["control_methods"]), sorted(P.METHODS))
        self.assertEqual(list(self.spec["catalog_new"]), ["purdue_ext_bp69w"])

    def test_pins_are_the_literals(self):
        self.assertEqual((P.EXPECTED_NOTES, P.EXPECTED_CROPS, P.EXPECTED_PRE_STATEMENTS,
                          P.EXPECTED_POST_STATEMENTS, P.EXPECTED_NEW_SOURCES),
                         (N_NOTES, N_CROPS, N_PRE, N_POST, N_NEW_SOURCES))


class TheNet(Base):
    """Guard 1. The instrument the promote pins itself to."""

    def test_pre_net_finds_exactly_the_pinned_count(self):
        self.assertEqual(len(P.interval_sentences(self.data)), N_PRE)

    def test_the_net_finds_the_five_pronoun_statements(self):
        found = {tuple(w.split("/")[i] for i in (0, 2, 3)) for w, s in P.interval_sentences(self.data)
                 if not w.startswith("control_methods")}
        self.assertTrue(PRONOUN_FIVE <= found, f"missing {PRONOUN_FIVE - found}")

    def test_the_net_excludes_mints_harvest_phi(self):
        self.assertFalse(any(w.startswith("mint/") for w, s in P.interval_sentences(self.data)))

    def test_pre_statements_pass(self):
        self.assertEqual(P.check_pre_statements(self.spec, self.data), N_PRE)

    def test_refuses_a_pre_count_drift(self):
        d = self.fresh_data()
        r = self.rung(d, "basil", "pests", "aphids", "insecticidal_soap") if False else None
        # inject a fresh interval statement on a rung the spec does not name
        ent = P.by_slug(d)["mint"]["diseases"]
        e = next(p for p in ent if p.get("id") == "powdery-mildew")
        sr = next(x for x in e["control_ladder"] if x.get("method") == "sulfur")
        sr["note_beginner"] = (sr.get("note_beginner") or "") + " Keep sulfur two weeks from any oil spray."
        self.assertRefuses("re-measure before running", P.check_pre_statements, self.spec, d)

    def test_refuses_a_statement_the_spec_does_not_rewrite(self):
        s = self.fresh_spec()
        self.row(s, "apple", "apple-scab")["old"] = "Some other sentence."
        self.assertRefuses("the spec does not rewrite", P.check_pre_statements, s, self.data)

    def test_post_statements_pass(self):
        self.assertEqual(P.check_post_statements(self.post()), N_POST)

    def test_refuses_a_surviving_sub_thirty_statement(self):
        post = self.post()
        r = self.row(self.spec, "plum", "san-jose-scale", "note_beginner")
        rg = self.rung(post, "plum", "pests", "san-jose-scale", "horticultural_oil")
        rg["note_beginner"] = rg["note_beginner"].replace(r["new"], r["old"])
        self.assertRefuses("survive without the scoped 30-day claim", P.check_post_statements, post)

    def test_refuses_a_post_count_change(self):
        post = self.post()
        rg = self.rung(post, "sage", "pests", "spider-mites", "horticultural_oil")
        rg["note_beginner"] = (rg.get("note_beginner") or "") + " Keep sulfur 30 days from oil while in leaf; check the label."
        self.assertRefuses("expected 22", P.check_post_statements, post)


class SpecShape(Base):
    def test_spec_shape_passes(self):
        self.assertEqual(P.check_spec_shape(self.spec), N_NOTES)

    def test_refuses_a_bare_interval(self):
        s = self.fresh_spec()
        self.row(s, "apple", "apple-scab")["new"] = "Avoid it above 90°F and within 30 days of an oil spray while the tree is in leaf."
        self.assertRefuses("not a scoped 30-day claim", P.check_spec_shape, s)

    def test_refuses_a_missing_scope(self):
        s = self.fresh_spec()
        self.row(s, "apple", "apple-scab")["new"] = "Avoid it above 90°F and within 30 days of an oil spray; check the oil label, since some specify longer."
        self.assertRefuses("not a scoped 30-day claim", P.check_spec_shape, s)

    def test_refuses_a_sub_thirty_interval(self):
        s = self.fresh_spec()
        self.row(s, "apple", "apple-scab")["new"] = "Avoid it within 30 days of an oil spray while the tree is in leaf, or 2 weeks if the oil label allows it."
        self.assertRefuses("not a scoped 30-day claim", P.check_spec_shape, s)

    def test_refuses_a_claim_without_the_figure(self):
        s = self.fresh_spec()
        self.row(s, "apple", "apple-scab")["new"] = "Avoid it within a month of an oil spray while the tree is in leaf; check the oil label, since some specify longer."
        self.assertRefuses("not a scoped 30-day claim", P.check_spec_shape, s)

    def test_scoped_thirty_with_label_directly(self):
        f = P.scoped_thirty_with_label
        self.assertTrue(f("Keep sulfur 30 days from oil while the plant is in leaf; check the label."))
        self.assertFalse(f("Keep sulfur 30 days from oil while the plant is in leaf."))
        self.assertFalse(f("Keep sulfur 30 days from oil; check the label."))
        self.assertFalse(f("Keep sulfur 2 weeks from oil while in leaf; check the label; or 30 days."))
        self.assertFalse(f("Keep sulfur a month from oil while in leaf; check the label."))

    def test_refuses_an_em_dash(self):
        s = self.fresh_spec()
        self.row(s, "apple", "apple-scab")["new"] = "Avoid it within 30 days of an oil spray while the tree is in leaf — check the oil label, since some specify longer."
        self.assertRefuses("fails copy hygiene", P.check_spec_shape, s)

    def test_refuses_a_verbatim_lift_from_an_anchor(self):
        s = self.fresh_spec()
        self.row(s, "apple", "apple-scab")["new"] = "Do not use sulfur if you have applied an oil spray within the last month, or 30 days, while the tree is in leaf; check the oil label, since some specify longer."
        self.assertRefuses("lifts a verbatim run", P.check_spec_shape, s)

    def test_figure_runs_are_exempt_but_prose_runs_are_not(self):
        self.assertTrue(P._is_figure_run("30 days of an oil spray"))
        self.assertFalse(P._is_figure_run("if you have applied an oil spray"))
        self.assertIsNone(P.lifted_from_anchor("Keep sulfur at least 30 days of an oil spray apart."))
        self.assertIsNotNone(P.lifted_from_anchor("Remember: if you have applied an oil spray within the last month, wait."))

    def test_refuses_a_row_count_other_than_twenty(self):
        s = self.fresh_spec()
        s["notes"] = s["notes"][:-1]
        self.assertRefuses("expected 20", P.check_spec_shape, s)

    def test_refuses_a_duplicated_row(self):
        s = self.fresh_spec()
        s["notes"][-1] = copy.deepcopy(s["notes"][0])
        self.assertRefuses("names the same note twice", P.check_spec_shape, s)

    def test_refuses_a_self_rewrite(self):
        s = self.fresh_spec()
        r = self.row(s, "apple", "apple-scab")
        r["new"] = r["old"]
        self.assertRefuses("rewrites a sentence to itself", P.check_spec_shape, s)

    def test_refuses_a_second_catalog_id(self):
        s = self.fresh_spec()
        s["catalog_new"]["ghost_source"] = dict(s["catalog_new"]["purdue_ext_bp69w"], id="ghost_source")
        self.assertRefuses("admits 2 catalog ids", P.check_spec_shape, s)

    def test_refuses_anchors_that_do_not_match_sources(self):
        s = self.fresh_spec()
        s["control_methods"]["sulfur"]["add_anchors"].pop("ucanr_ext_spider_mites")
        self.assertRefuses("add_anchors keys != add_sources", P.check_spec_shape, s)


class PreState(Base):
    def test_pre_state_passes(self):
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_NOTES)

    def test_refuses_a_drifted_old_sentence(self):
        d = self.fresh_data()
        rg = self.rung(d, "apple", "diseases", "apple-scab", "sulfur")
        rg["note_seasoned"] = rg["note_seasoned"].replace("2 weeks", "10 days")
        self.assertRefuses("found 0 times", P.check_pre_state, self.spec, d)

    def test_refuses_a_missing_caution(self):
        d = self.fresh_data()
        d["control_methods"]["sulfur"]["cautions"] = [c for c in d["control_methods"]["sulfur"]["cautions"] if "2 weeks" not in c]
        self.assertRefuses("caution found 0 times", P.check_pre_state, self.spec, d)

    def test_refuses_a_catalog_id_that_already_exists(self):
        d = self.fresh_data()
        d["source_catalog"]["purdue_ext_bp69w"] = dict(self.spec["catalog_new"]["purdue_ext_bp69w"])
        self.assertRefuses("already exists; this would overwrite", P.check_pre_state, self.spec, d)

    def test_refuses_a_non_t1_source_on_a_caution(self):
        s = self.fresh_spec()
        s["catalog_new"]["purdue_ext_bp69w"]["tier"] = "T2"
        self.assertRefuses("which is not T1", P.check_pre_state, s, self.data)

    def test_refuses_an_anchor_url_that_differs_from_the_catalog(self):
        s = self.fresh_spec()
        s["control_methods"]["sulfur"]["add_anchors"]["ucanr_ext_spider_mites"]["url"] = "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7406.html"
        self.assertRefuses("does not match the catalog url", P.check_pre_state, s, self.data)

    def test_refuses_a_bare_host_url(self):
        s = self.fresh_spec()
        s["catalog_new"]["purdue_ext_bp69w"]["url"] = "https://extension.purdue.edu"
        for m in s["control_methods"].values():
            if "purdue_ext_bp69w" in m["add_anchors"]:
                m["add_anchors"]["purdue_ext_bp69w"]["url"] = "https://extension.purdue.edu"
        self.assertRefuses("not a pathed https document", P.check_pre_state, s, self.data)

    def test_refuses_a_document_id_without_a_title_A54(self):
        s = self.fresh_spec()
        s["catalog_new"]["purdue_ext_bp69w"].pop("title")
        self.assertRefuses("would fail A54", P.check_pre_state, s, self.data)


class OreganoAndRegisters(Base):
    def test_oregano_agrees(self):
        self.assertTrue(P.check_oregano_agrees(self.post()))

    def test_refuses_oregano_with_one_rung_reverted(self):
        post = self.post()
        r = self.row(self.spec, "oregano", "powdery-mildew")
        rg = self.rung(post, "oregano", "diseases", "powdery-mildew", "sulfur")
        rg["note_seasoned"] = rg["note_seasoned"].replace(r["new"], r["old"])
        self.assertRefuses("do not both say 30 days", P.check_oregano_agrees, post)

    def test_registers_diverge(self):
        self.assertEqual(P.check_registers_diverge(self.post(), self.spec), N_NOTES)

    def test_refuses_identical_registers(self):
        post = self.post()
        rg = self.rung(post, "plum", "pests", "plum-aphids", "horticultural_oil")
        rg["note_seasoned"] = rg["note_beginner"]
        self.assertRefuses("registers are identical", P.check_registers_diverge, post, self.spec)

    def test_refuses_a_reworded_register(self):
        post = self.post()
        rg = self.rung(post, "plum", "pests", "plum-aphids", "horticultural_oil")
        rg["note_seasoned"] = rg["note_beginner"].replace("the", "a", 1) + " "
        self.assertRefuses("that is a reword", P.check_registers_diverge, post, self.spec)


class CatalogGates(Base):
    def test_catalog_gates_pass_on_the_post_state(self):
        self.assertTrue(P.check_catalog_gates(self.post()))

    def test_refuses_a54_on_the_post_state(self):
        post = self.post()
        post["source_catalog"]["purdue_ext_bp69w"].pop("title")
        self.assertRefuses("A54 on the post-state", P.check_catalog_gates, post)

    def test_refuses_control_ladder_gate_on_the_post_state(self):
        post = self.post()
        post["control_methods"]["sulfur"]["sources"].append("not-a-catalog-id")
        self.assertRefuses("control_ladder_gate on the post-state", P.check_catalog_gates, post)


class VerifyPost(Base):
    def test_apply_changes_exactly_the_declared_leaves(self):
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec), N_LEAVES)

    def test_set_comparison_runs_before_value_comparison(self):
        post = self.post()
        next(p for p in P.by_slug(post)["plum"]["pests"] if p["id"] == "plum-aphids")["ghost"] = 1
        self.assertRefuses("entry key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_crop_level_addition(self):
        post = self.post()
        P.by_slug(post)["plum"]["ghost_field"] = 1
        self.assertRefuses("crop-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_untouched_crop_change(self):
        post = self.post()
        P.by_slug(post)["tomatillo"]["diseases"][0]["id"] = "tampered"
        self.assertRefuses("untouched crop", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_prose_field_change_on_a_touched_crop(self):
        post = self.post()
        next(p for p in P.by_slug(post)["plum"]["pests"] if p["id"] == "plum-aphids")["symptoms_beginner"] = "rewritten"
        self.assertRefuses("rewrites rung notes and nothing else on a crop", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_rung_key_set_change(self):
        post = self.post()
        self.rung(post, "plum", "pests", "plum-aphids", "horticultural_oil")["ghost"] = 1
        self.assertRefuses("rung key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_ladder_length_change(self):
        post = self.post()
        next(p for p in P.by_slug(post)["plum"]["pests"] if p["id"] == "plum-aphids")["control_ladder"].pop()
        self.assertRefuses("ladder length changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_note_change_without_a_row(self):
        post = self.post()
        self.rung(post, "plum", "pests", "plum-aphids", "horticultural_oil")["note_seasoned"] += " Extra."
        self.assertRefuses("not exactly the one-sentence replacement", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_note_change_on_an_unnamed_rung(self):
        """The first draft named a rung plum's aphid ladder does not have and errored before the
        guard ran; the harness then counted its mutation as caught for the wrong reason. Pick the
        rung by the property under test: any rung on the entry that is NOT horticultural_oil."""
        post = self.post()
        ent = next(p for p in P.by_slug(post)["plum"]["pests"] if p["id"] == "plum-aphids")
        other = next(x for x in ent["control_ladder"] if x.get("method") != "horticultural_oil")
        other["note_beginner"] = "changed"
        self.assertRefuses("without a spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_fewer_leaves_than_rows(self):
        post = self.post()
        r = self.row(self.spec, "plum", "san-jose-scale", "note_beginner")
        rg = self.rung(post, "plum", "pests", "san-jose-scale", "horticultural_oil")
        rg["note_beginner"] = rg["note_beginner"].replace(r["new"], r["old"])
        self.assertRefuses("note leaves changed, spec has", P.verify_post, self.data, post, self.spec)

    def test_refuses_another_method_changing(self):
        post = self.post()
        post["control_methods"]["garden_sanitation"]["tier"] = "physical"
        self.assertRefuses("may change", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_non_caution_field_on_a_declared_method(self):
        post = self.post()
        post["control_methods"]["sulfur"]["best_use"] = "rewritten"
        self.assertRefuses("only cautions, sources and", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_cautions_count_change(self):
        post = self.post()
        post["control_methods"]["sulfur"]["cautions"].append("Another caution.")
        self.assertRefuses("cautions count changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_second_caution_changing(self):
        post = self.post()
        post["control_methods"]["sulfur"]["cautions"][0] = "rewritten"
        self.assertRefuses("cautions changed other than the declared one", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_undeclared_source_addition(self):
        post = self.post()
        post["control_methods"]["sulfur"]["sources"].append("uc_ipm")
        self.assertRefuses("sources changed other than by the declared additions", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_modified_existing_anchor(self):
        post = self.post()
        post["control_methods"]["sulfur"]["anchoring_urls"]["ucanr_ext"]["verified"] = "2030-01-01"
        self.assertRefuses("was modified", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_dropped_catalog_entry(self):
        post = self.post()
        post["source_catalog"].pop("uc_ipm")
        self.assertRefuses("source_catalog DROPPED", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_catalog_entry(self):
        post = self.post()
        post["source_catalog"]["ghost_source"] = dict(post["source_catalog"]["purdue_ext_bp69w"], id="ghost_source")
        self.assertRefuses("expected exactly", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_modified_existing_catalog_entry(self):
        post = self.post()
        post["source_catalog"]["uc_ipm"]["accessed"] = "2030-01"
        self.assertRefuses("was MODIFIED", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_roster_change(self):
        post = self.post()
        ghost = copy.deepcopy(P.by_slug(post)["plum"])
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_touched_top_level_key(self):
        post = self.post()
        post["version"] = "tampered"
        self.assertRefuses("top-level key", P.verify_post, self.data, post, self.spec)


class Serializer(Base):
    def test_one_serializer_shared_with_the_suite(self):
        blob = P.serialize({"a": "é", "b": 1})
        self.assertEqual(blob, b'{"a":"\xc3\xa9","b":1}')
        self.assertNotIn(b"\n", blob)

    def test_promote_output_is_the_pinned_sha(self):
        self.assertEqual(P.sha256_bytes(P.serialize(self.post())), OUTPUT_SHA)


class EntryPoint(Base):
    def _run(self, blob, *extra):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "canonical.json")
            with open(path, "wb") as f:
                f.write(blob)
            r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla457_sulfur_oil_interval.py"),
                                *extra, path], capture_output=True, text=True)
            after = open(path, "rb").read()
            out_path = os.path.join(td, "post.json")
            post_bytes = open(out_path, "rb").read() if os.path.exists(out_path) else None
            return r, after, post_bytes

    def test_main_runs_the_whole_promote_against_the_fixture(self):
        r, after, _ = self._run(promote_fixture.pre_state(P.BASE_SHA), "--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for expected in ("spec shape", "pre-state", "widened net (pre)", "widened net (post)", "oregano",
                         "registers diverge", "catalog gates", "verify post", OUTPUT_SHA, "nothing written"):
            self.assertIn(expected, r.stdout)
        self.assertEqual(P.sha256_bytes(after), BASE_SHA, "--check wrote the canonical")

    def test_out_writes_the_post_state_elsewhere_and_leaves_canonical_alone(self):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "canonical.json")
            out = os.path.join(td, "post.json")
            with open(path, "wb") as f:
                f.write(promote_fixture.pre_state(P.BASE_SHA))
            r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla457_sulfur_oil_interval.py"),
                                "--out", out, path], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(P.sha256_bytes(open(path, "rb").read()), BASE_SHA)
            self.assertEqual(P.sha256_bytes(open(out, "rb").read()), OUTPUT_SHA)

    def test_main_refuses_a_moved_base(self):
        d = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        d["version"] = "tampered"
        r, _, _ = self._run(P.serialize(d), "--check")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("base SHA mismatch", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
