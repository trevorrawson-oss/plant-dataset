#!/usr/bin/env python3
"""Guard suite for promote_pla464_rootstock_array -- PLA-464 Option A.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla464_rootstock_array_suite.py.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla464_rootstock_array as P  # noqa: E402

BASE_SHA = "d7b33682f9926e3aef176ef8a1bb1f3191143957ca40c94e36433abd883a2798"
ROSTER = 128
N_RETIRE = 6
N_FOLDINS = 3
N_RR = 2
N_FA = 3
N_FINDINGS = 4
N_CROPS = 5
N_GALLONS = 15
N_CHANGES = 18
RETIRE_CROPS = ("cherry-sour", "fig", "mulberry", "pawpaw", "pomegranate")
RETIRED_NAMES = {
    ("fig", 0): "Own-root (from cuttings)",
    ("pomegranate", 0): "Own roots (cutting-grown)",
    ("mulberry", 0): "Own-root (from hardwood cutting)",
    ("mulberry", 2): "Genetic dwarf (e.g. Dwarf Everbearing)",
    ("pawpaw", 1): "Own-root seedling (ungrafted)",
    ("cherry-sour", 4): "Own-root / genetic dwarf (North Star, Meteor)",
}
SURVIVORS = {
    "fig": [], "pomegranate": [],
    "mulberry": ["Morus seedling (alba or rubra)"],
    "pawpaw": ["Pawpaw seedling (grafted)"],
    "cherry-sour": ["Mahaleb", "Mazzard", "Gisela 5", "Gisela 6"],
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

    def fold(self, spec, crop):
        return next(f for f in spec["note_foldins"] if f["crop"] == crop)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg, f"guard fired with the wrong message.\n  wanted: {fragment!r}\n  got: {msg!r}")


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(promote_fixture.pre_state(P.BASE_SHA)), BASE_SHA)

    def test_refuses_a_canonical_that_is_not_the_base(self):
        """load_canonical is the ENTRY POINT: bytes that do not hash to BASE_SHA are refused before any check runs."""
        with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as f:
            f.write(b'{"crops":[]}')
        try:
            self.assertRefuses("this promote is pinned to", P.load_canonical, f.name)
        finally:
            os.remove(f.name)

    def test_fixture_is_the_full_roster(self):
        self.assertEqual(len(self.data["crops"]), ROSTER)

    def test_pins_are_the_literals(self):
        self.assertEqual((P.EXPECTED_RETIRE, P.EXPECTED_FOLDINS, P.EXPECTED_RR, P.EXPECTED_FA, P.EXPECTED_FINDINGS,
                          P.EXPECTED_CROPS, P.MULBERRY_GALLONS, P.EXPECTED_CHANGES),
                         (N_RETIRE, N_FOLDINS, N_RR, N_FA, N_FINDINGS, N_CROPS, N_GALLONS, N_CHANGES))

    def test_the_spec_is_the_shape_measured(self):
        self.assertEqual(len(self.spec["retire"]), N_RETIRE)
        self.assertEqual(tuple(sorted({r["crop"] for r in self.spec["retire"]})), RETIRE_CROPS)
        self.assertEqual({(r["crop"], r["index"]): r["name"] for r in self.spec["retire"]}, RETIRED_NAMES)
        self.assertEqual(sorted(f["crop"] for f in self.spec["note_foldins"]), ["fig", "mulberry", "pawpaw"])
        self.assertEqual(sorted(r["crop"] for r in self.spec["recommended_rootstock"]), ["fig", "mulberry"])
        self.assertEqual(sorted(o["crop"] for o in self.spec["open_findings"]), ["cherry-sour", "fig", "mulberry", "pomegranate"])
        self.assertEqual(self.spec["expected"], {
            "retire": P.EXPECTED_RETIRE, "foldins": P.EXPECTED_FOLDINS, "recommended_rootstock": P.EXPECTED_RR,
            "field_additions": P.EXPECTED_FA, "open_findings": P.EXPECTED_FINDINGS, "crops": P.EXPECTED_CROPS,
            "mulberry_gallons": P.MULBERRY_GALLONS},
            "spec.json's expected block is enforced by nothing else; it must equal the promote's pins")

    def test_the_name_net_flags_exactly_the_six_on_the_base(self):
        """The independent net and the spec agree on the base; a real rootstock (Morus seedling, D. virginiana) is NOT flagged."""
        got = P.net_population(self.data)
        self.assertEqual({(c, i) for c, i, _ in got}, set(RETIRED_NAMES))
        self.assertFalse(P.NAME_NET.search("Morus seedling (alba or rubra)"))
        self.assertFalse(P.NAME_NET.search("Diospyros virginiana (American persimmon)"))
        self.assertFalse(P.NAME_NET.search("Pawpaw seedling (grafted)"))


class SpecShape(Base):
    def test_refuses_a_spec_on_another_base(self):
        s = self.fresh_spec(); s["base_sha"] = "0" * 64
        self.assertRefuses("not the pinned base", P.check_spec_shape, s)

    def test_refuses_a_retire_count_drift(self):
        s = self.fresh_spec(); s["retire"].pop()
        self.assertRefuses("retire rows, pinned", P.check_spec_shape, s)

    def test_refuses_a_duplicated_retire_row(self):
        s = self.fresh_spec(); s["retire"][1] = dict(s["retire"][0])
        self.assertRefuses("appears twice", P.check_spec_shape, s)

    def test_refuses_an_unknown_concept(self):
        s = self.fresh_spec(); s["retire"][0]["concept"] = "rootstock"
        self.assertRefuses("concept", P.check_spec_shape, s)

    def test_refuses_a_nameless_retire_row(self):
        s = self.fresh_spec(); s["retire"][0]["name"] = "  "
        self.assertRefuses("has no name", P.check_spec_shape, s)

    def test_refuses_a_retire_set_spanning_the_wrong_crop_count(self):
        """Move one of mulberry's TWO rows to apple: mulberry stays, apple is added, the set grows to 6.
        (Moving fig's only row would swap a crop for a crop and leave the count at 5, and the fold-in
        check would answer for the guard.)"""
        s = self.fresh_spec()
        row = next(r for r in s["retire"] if r["crop"] == "mulberry" and r["index"] == 2)
        row["crop"] = "apple"
        self.assertRefuses("crops, pinned", P.check_spec_shape, s)

    def test_refuses_a_foldin_count_drift(self):
        s = self.fresh_spec(); s["note_foldins"].pop()
        self.assertRefuses("fold-ins, pinned", P.check_spec_shape, s)

    def test_refuses_a_foldin_on_a_crop_with_no_retired_row(self):
        s = self.fresh_spec(); self.fold(s, "pawpaw")["crop"] = "apple"
        self.assertRefuses("distinct crops that carry a retired row", P.check_spec_shape, s)

    def test_refuses_a_foldin_without_a_period(self):
        s = self.fresh_spec(); self.fold(s, "fig")["sentence"] = "No period here"
        self.assertRefuses("does not end with a period", P.check_spec_shape, s)

    def test_refuses_a_foldin_with_an_em_dash(self):
        s = self.fresh_spec(); self.fold(s, "fig")["sentence"] = "A sentence — with an em dash."
        self.assertRefuses("em dash", P.check_spec_shape, s)

    def test_refuses_a_foldin_without_sources(self):
        s = self.fresh_spec(); self.fold(s, "fig")["sources"] = []
        self.assertRefuses("carries no sources", P.check_spec_shape, s)

    def test_refuses_a_recommended_rootstock_count_drift(self):
        s = self.fresh_spec(); s["recommended_rootstock"].pop()
        self.assertRefuses("recommended_rootstock rows, pinned", P.check_spec_shape, s)

    def test_refuses_a_recommended_rootstock_no_op(self):
        s = self.fresh_spec(); s["recommended_rootstock"][0]["to"] = s["recommended_rootstock"][0]["from"]
        self.assertRefuses("is not a change on a retire crop", P.check_spec_shape, s)

    def test_refuses_mulberry_gallons_not_kept(self):
        s = self.fresh_spec(); s["mulberry_gallons"]["kept"] = False
        self.assertRefuses("must be kept", P.check_spec_shape, s)

    def test_refuses_a_field_additions_count_drift(self):
        s = self.fresh_spec(); s["field_additions"].pop()
        self.assertRefuses("field_additions, pinned", P.check_spec_shape, s)

    def test_refuses_a_field_additions_shape(self):
        s = self.fresh_spec(); del s["field_additions"][0]["entry"]["note"]
        self.assertRefuses("wrong shape", P.check_spec_shape, s)

    def test_refuses_a_field_additions_whose_sources_differ_from_its_foldin(self):
        s = self.fresh_spec(); s["field_additions"][0]["entry"]["sources"] = ["ncsu_ext"]
        self.assertRefuses("does not carry its fold-in's sources", P.check_spec_shape, s)

    def test_refuses_a_findings_count_drift(self):
        s = self.fresh_spec(); s["open_findings"].pop()
        self.assertRefuses("open_findings, pinned", P.check_spec_shape, s)

    def test_refuses_a_finding_shape(self):
        s = self.fresh_spec(); s["open_findings"][0]["entry"]["extra"] = 1
        self.assertRefuses("wrong shape", P.check_spec_shape, s)

    def test_refuses_a_finding_that_blocks_launch(self):
        s = self.fresh_spec(); s["open_findings"][0]["entry"]["blocks_launch"] = True
        self.assertRefuses("must be deferred, non-blocking", P.check_spec_shape, s)

    def test_refuses_a_duplicated_finding_id(self):
        s = self.fresh_spec(); s["open_findings"][1]["entry"]["id"] = s["open_findings"][0]["entry"]["id"]
        self.assertRefuses("duplicated", P.check_spec_shape, s)

    def test_refuses_an_expected_block_drift(self):
        s = self.fresh_spec(); s["expected"]["retire"] = 7
        self.assertRefuses("expected block", P.check_spec_shape, s)


class PreState(Base):
    def test_pre_state_passes(self):
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_RETIRE)

    def test_refuses_a_roster_drift(self):
        d = self.fresh_data(); d["crops"].append(copy.deepcopy(P.by_slug(d)["lime"]))
        d["crops"][-1]["slug"] = "ghost-crop"
        self.assertRefuses("roster is 129", P.check_pre_state, self.spec, d)

    def test_refuses_a_retire_crop_off_the_roster(self):
        s = self.fresh_spec(); s["retire"][0]["crop"] = "ghost-crop"
        self.assertRefuses("is not on the roster", P.check_pre_state, s, self.data)

    def test_refuses_an_index_naming_another_row(self):
        s = self.fresh_spec()
        row = next(r for r in s["retire"] if r["crop"] == "mulberry" and r["index"] == 0)
        row["index"] = 1
        self.assertRefuses("is not 'Own-root (from hardwood cutting)' on the base", P.check_pre_state, s, self.data)

    def test_refuses_a_net_disagreement_missed_row(self):
        """A seventh flagged row on the base (apple) that the spec does not name."""
        d = self.fresh_data()
        P.by_slug(d)["apple"]["rootstock_options"].append({"name": "Own-root seedling (ungrafted)", "container_suitable": False})
        self.assertRefuses("name net flags", P.check_pre_state, self.spec, d)

    def test_refuses_a_net_disagreement_unflagged_spec_row(self):
        """The spec and the base agree on a name the net does NOT flag: the row is not retired on the spec's say-so."""
        s = self.fresh_spec(); d = self.fresh_data()
        row = next(r for r in s["retire"] if r["crop"] == "mulberry" and r["index"] == 0)
        row["name"] = "Morus cutting stock"
        P.by_slug(d)["mulberry"]["rootstock_options"][0]["name"] = "Morus cutting stock"
        self.assertRefuses("name net flags", P.check_pre_state, s, d)

    def test_refuses_a_crop_with_no_note(self):
        d = self.fresh_data(); P.by_slug(d)["fig"]["recommended_rootstock_note"] = None
        self.assertRefuses("no recommended_rootstock_note to fold into", P.check_pre_state, self.spec, d)

    def test_refuses_a_foldin_already_present(self):
        d = self.fresh_data(); c = P.by_slug(d)["fig"]
        c["recommended_rootstock_note"] += " " + self.fold(self.spec, "fig")["sentence"]
        self.assertRefuses("already carries the fold-in sentence", P.check_pre_state, self.spec, d)

    def test_refuses_a_foldin_source_not_in_catalog(self):
        s = self.fresh_spec()
        self.fold(s, "fig")["sources"] = ["nobody_ext"]
        s["field_additions"][0]["entry"]["sources"] = ["nobody_ext"]
        self.assertRefuses("is not in source_catalog", P.check_pre_state, s, self.data)

    def test_refuses_a_sibling_from_mismatch(self):
        d = self.fresh_data(); P.by_slug(d)["fig"]["recommended_rootstock"] = "Something else"
        self.assertRefuses("recommended_rootstock is not", P.check_pre_state, self.spec, d)

    def test_refuses_mulberry_gallons_not_pinned_on_base(self):
        d = self.fresh_data(); P.by_slug(d)["mulberry"]["container_notes"]["min_pot_gallons"] = 20
        self.assertRefuses("mulberry min_pot_gallons is not the pinned figure", P.check_pre_state, self.spec, d)

    def test_refuses_dwarf_everbearing_gallons_not_pinned_on_base(self):
        d = self.fresh_data()
        v = next(x for x in P._varieties(P.by_slug(d)["mulberry"]) if x["name"] == "Dwarf Everbearing")
        v["container_min_gallons"] = 20
        self.assertRefuses("Dwarf Everbearing container_min_gallons is not the pinned figure", P.check_pre_state, self.spec, d)

    def test_refuses_field_additions_not_a_list(self):
        d = self.fresh_data(); P.by_slug(d)["fig"]["verification_status"]["field_additions"] = None
        self.assertRefuses("field_additions is not a list", P.check_pre_state, self.spec, d)

    def test_refuses_a_recorded_note_addition_already_present(self):
        d = self.fresh_data()
        P.by_slug(d)["fig"]["verification_status"]["field_additions"].append({"field": "recommended_rootstock_note", "date": "2026-01-01", "sources": [], "note": "x"})
        self.assertRefuses("already records a recommended_rootstock_note addition", P.check_pre_state, self.spec, d)

    def test_refuses_open_findings_not_a_list(self):
        d = self.fresh_data(); P.by_slug(d)["fig"]["verification_status"]["open_findings"] = None
        self.assertRefuses("open_findings is not a list", P.check_pre_state, self.spec, d)

    def test_refuses_a_finding_id_already_present(self):
        d = self.fresh_data()
        P.by_slug(d)["fig"]["verification_status"]["open_findings"].append({"id": "fig_min_pot_gallons_unanchored_pla464"})
        self.assertRefuses("already carries finding", P.check_pre_state, self.spec, d)


class ApplyAndPost(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_apply_changes_exactly_the_declared_changes(self):
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec), N_CHANGES)

    def test_the_six_rows_are_gone_and_survivors_intact(self):
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for slug, names in SURVIVORS.items():
            self.assertEqual([e["name"] for e in post[slug]["rootstock_options"]], names, slug)
            kept = [e for e in pre[slug]["rootstock_options"] if e["name"] in names]
            self.assertEqual(kept, post[slug]["rootstock_options"], slug)
        self.assertEqual(P.net_population(self.post()), set())

    def test_the_three_notes_end_with_their_foldin(self):
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for f in self.spec["note_foldins"]:
            self.assertEqual(post[f["crop"]]["recommended_rootstock_note"],
                             pre[f["crop"]]["recommended_rootstock_note"] + " " + f["sentence"])
        for slug in ("pomegranate", "cherry-sour"):
            self.assertEqual(pre[slug]["recommended_rootstock_note"], post[slug]["recommended_rootstock_note"])

    def test_fig_recommended_rootstock_is_null_and_mulberrys_names_the_survivor(self):
        post = P.by_slug(self.post())
        self.assertIsNone(post["fig"]["recommended_rootstock"])
        self.assertEqual(post["mulberry"]["recommended_rootstock"], "Morus seedling (alba or rubra)")
        self.assertEqual(post["mulberry"]["recommended_rootstock"], post["mulberry"]["rootstock_options"][0]["name"])

    def test_mulberry_gallons_unchanged_at_the_pin(self):
        post = P.by_slug(self.post())["mulberry"]
        self.assertEqual(post["container_notes"]["min_pot_gallons"], N_GALLONS)
        v = next(x for x in P._varieties(post) if x["name"] == "Dwarf Everbearing")
        self.assertEqual((v["container_suitable"], v["container_min_gallons"]), (True, N_GALLONS))
        self.assertEqual(post["container_notes"]["container_ok"], True)
        self.assertEqual(post["container_notes"]["container_path"], "cultivar")

    def test_records_appended_once_each(self):
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for fa in self.spec["field_additions"]:
            a, b = pre[fa["crop"]]["verification_status"]["field_additions"], post[fa["crop"]]["verification_status"]["field_additions"]
            self.assertEqual(b, a + [fa["entry"]])
        for of in self.spec["open_findings"]:
            a, b = pre[of["crop"]]["verification_status"]["open_findings"], post[of["crop"]]["verification_status"]["open_findings"]
            self.assertEqual(b, a + [of["entry"]])
        self.assertEqual(pre["pawpaw"]["verification_status"]["open_findings"], post["pawpaw"]["verification_status"]["open_findings"])

    def test_no_other_crop_changes(self):
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for slug in pre:
            if slug not in RETIRE_CROPS:
                self.assertEqual(pre[slug], post[slug], slug)

    def test_post_gate_is_clean_with_presence_on(self):
        self.assertEqual(P.CPG.all_violations(self.post(), presence=True), [])

    def test_refuses_a_post_state_that_fails_the_gate(self):
        post = self.post(); P.by_slug(post)["basil"]["container_notes"]["container_path"] = None
        self.assertRefuses("container_path_gate on the post-state", P.check_post, post, self.spec)

    def test_refuses_a_touched_crop_that_fails_display_readiness(self):
        """D5 measured: a null pot figure on a container_ok crop is what display_readiness refuses."""
        post = self.post(); P.by_slug(post)["mulberry"]["container_notes"]["min_pot_gallons"] = None
        self.assertRefuses("display_readiness on mulberry", P.check_post, post, self.spec)

    def test_refuses_a_touched_crop_that_fails_numeric_sanity(self):
        post = self.post(); P.by_slug(post)["fig"]["container_notes"]["min_pot_gallons"] = 500
        self.assertRefuses("numeric_sanity on fig", P.check_post, post, self.spec)


class BlastRadius(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_refuses_a_top_level_key_addition(self):
        post = self.post(); post["injected_top_key"] = 1
        self.assertRefuses("top-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_top_level_change(self):
        post = self.post(); post["control_methods"] = {}
        self.assertRefuses("top-level key 'control_methods' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_roster_change(self):
        post = self.post(); post["crops"].pop()
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_untouched_crop_change(self):
        post = self.post(); P.by_slug(post)["apple"]["recommended_rootstock_note"] = "changed"
        self.assertRefuses("untouched crop apple changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_crop_level_key_addition(self):
        post = self.post(); P.by_slug(post)["fig"]["injected_key"] = 1
        self.assertRefuses("crop-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_change_outside_the_declared_keys(self):
        """The mutated field must ALREADY EXIST on the crop, or the key-set check one line earlier answers for it."""
        post = self.post()
        self.assertIn("propagule", P.by_slug(post)["fig"])
        P.by_slug(post)["fig"]["propagule"] = "seed"
        self.assertRefuses("changed outside the declared keys", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_gallons_move_on_mulberry(self):
        """D5 as amended: container_notes is outside the declared keys, so a moved pot figure is refused there."""
        post = self.post(); P.by_slug(post)["mulberry"]["container_notes"]["min_pot_gallons"] = 20
        self.assertRefuses("field 'container_notes' changed outside", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_gallons_move_on_dwarf_everbearing(self):
        """THE PAIR. mulberry's crop-level min_pot_gallons and Dwarf Everbearing's container_min_gallons were
        inherited together from the retired row and are handed to PLA-533 together. The whole risk there is
        that one gets re-derived and the other does not. This driver and the one above are the pair made
        visible: a move on EITHER side alone is refused. After this promote no standing gate ties the two;
        the mulberry open_findings entry naming both paths is what carries the tie."""
        post = self.post()
        v = next(x for x in P._varieties(P.by_slug(post)["mulberry"]) if x["name"] == "Dwarf Everbearing")
        v["container_min_gallons"] = 20
        self.assertRefuses("field 'varieties' changed outside", P.verify_post, self.data, post, self.spec)
        post = self.post()
        v = next(x for x in P._varieties(P.by_slug(post)["mulberry"]) if x["name"] == "Dwarf Everbearing")
        del v["container_min_gallons"]
        self.assertRefuses("field 'varieties' changed outside", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_entry_count_drift(self):
        post = self.post(); P.by_slug(post)["cherry-sour"]["rootstock_options"].pop()
        self.assertRefuses("rootstock_options has 3 entries, expected 4", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_surviving_entry_change(self):
        post = self.post(); P.by_slug(post)["mulberry"]["rootstock_options"][0]["size_class"] = "dwarf"
        self.assertRefuses("surviving rootstock entry 'Morus seedling (alba or rubra)' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_note_other_than_pre_plus_foldin(self):
        post = self.post(); P.by_slug(post)["fig"]["recommended_rootstock_note"] = self.fold(self.spec, "fig")["sentence"]
        self.assertRefuses("is not the pre note plus the fold-in", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_note_change_without_a_foldin(self):
        post = self.post(); P.by_slug(post)["pomegranate"]["recommended_rootstock_note"] += " Extra."
        self.assertRefuses("recommended_rootstock_note changed without a fold-in row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_sibling_value_other_than_declared(self):
        post = self.post(); P.by_slug(post)["fig"]["recommended_rootstock"] = "Own-root"
        self.assertRefuses("recommended_rootstock is not the spec's", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_sibling_change_without_a_row(self):
        post = self.post(); P.by_slug(post)["pawpaw"]["recommended_rootstock"] = None
        self.assertRefuses("recommended_rootstock changed without a spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_key_addition(self):
        post = self.post(); P.by_slug(post)["fig"]["verification_status"]["injected"] = 1
        self.assertRefuses("verification_status key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_value_change(self):
        post = self.post(); P.by_slug(post)["fig"]["verification_status"]["status"] = "changed"
        self.assertRefuses("verification_status.status changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_list_that_is_not_a_list(self):
        post = self.post(); P.by_slug(post)["fig"]["verification_status"]["field_additions"] = {}
        self.assertRefuses("is not a list on both sides", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_rewritten_prefix(self):
        post = self.post(); P.by_slug(post)["fig"]["verification_status"]["open_findings"][0]["summary"] = "rewritten"
        self.assertRefuses("prefix is not byte-identical", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_record_other_than_the_spec(self):
        post = self.post(); P.by_slug(post)["fig"]["verification_status"]["open_findings"][-1]["deferred_to"] = "nowhere"
        self.assertRefuses("appended 1 entries, expected 1 matching the spec", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_appended_record(self):
        post = self.post(); P.by_slug(post)["pawpaw"]["verification_status"]["open_findings"].append({"id": "stray"})
        self.assertRefuses("appended 1 entries, expected 0", P.verify_post, self.data, post, self.spec)


class Serializer(Base):
    def test_compact_no_trailing_newline(self):
        b = P.serialize({"a": [1, 2], "b": "eé"})
        self.assertEqual(b, b'{"a":[1,2],"b":"e\xc3\xa9"}')

    def test_output_sha_is_stable(self):
        a = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        b = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        self.assertEqual(a, b)


class WriteGuards(Base):
    """main()'s write guards, exercised through the CLI against a COPY of the base bytes (never the live file)."""
    def _copy(self):
        d = tempfile.mkdtemp(prefix="pla464_wg_")
        p = os.path.join(d, "crops_data_final.json")
        with open(p, "wb") as f:
            f.write(promote_fixture.pre_state(P.BASE_SHA))
        return d, p

    def _run(self, *args):
        r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla464_rootstock_array.py"), *args],
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def test_refuses_to_write_without_expect_sha(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p)
            self.assertNotEqual(rc, 0)
            self.assertIn("requires --expect-sha", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)

    def test_refuses_out_that_targets_the_canonical(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p, "--out", p)
            self.assertNotEqual(rc, 0)
            self.assertIn("may not target the canonical", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)

    def test_refuses_a_wrong_expect_sha_and_leaves_the_copy_untouched(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p, "--expect-sha", "0" * 64)
            self.assertNotEqual(rc, 0)
            self.assertIn("REFUSED: expected", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
