#!/usr/bin/env python3
"""Guard suite for promote_pla580_plants_per_pot -- PLA-580 plants_per_pot, register row 31.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical:
a suite pinned to live canonical goes silently vacuous the moment canonical moves on.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla580_plants_per_pot_suite.py.

TWO POSITIVE CONTROLS ARE OWED BY NAME (spec section 8), because no authored crop exercises either
path: the two-reading conservative maximum, and a [2, 6] count that distinguishes count[0] from
count[1]. They live in NamedControls, below, and each is a mutation driver.
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
import promote_pla580_plants_per_pot as P  # noqa: E402

BASE_SHA = "079e3923660a53189bcf5e0bee0506e78225e473b2dadcba54cbfb3045337696"
ROSTER = 128
N_KEYS = 121
N_SHELLS = 7
N_AUTHORED = P.EXPECTED_AUTHORED_CROPS
N_READINGS = P.EXPECTED_READINGS_TOTAL

# A certified, container_ok crop this pass leaves NULL -- the fixture for every "a value appeared
# where no row authorized it" driver. Asserted against the base in Preflight, never assumed.
NULL_CROP = "basil"


def a_reading(count=(2, 3), gallons=(1, 1), src="uiuc_ext"):
    return {"count": list(count), "at_gallons": list(gallons), "sources": [src],
            "anchoring_urls": {src: {"url": "https://extension.illinois.edu/x",
                                     "verified": "2026-09-21"}}}


def a_record(src="uiuc_ext"):
    return {"field": "plants_per_pot", "date": "2026-09-21", "sources": [src],
            "note": "driver fixture"}


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.spec = P.staged()

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def row(self, spec, crop):
        return next(r for r in spec["authored"] if r["crop"] == crop)

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

    def test_fixture_is_the_full_roster(self):
        self.assertEqual(len(self.data["crops"]), ROSTER)

    def test_pins_are_the_literals(self):
        self.assertEqual(
            (P.EXPECTED_KEYS, P.EXPECTED_SHELLS, P.EXPECTED_AUTHORED_CROPS, P.EXPECTED_READINGS_TOTAL),
            (N_KEYS, N_SHELLS, N_AUTHORED, N_READINGS))

    def test_the_ruling_is_enumerated_not_derived(self):
        """EXPECTED_READINGS is the RULING, written as literals. An expectation computed from the
        spec it validates is vacuous, so assert the constant's own content, crop by crop."""
        self.assertEqual(sorted(P.EXPECTED_READINGS), [
            "cabbage", "cherry-tomato", "eggplant", "green-beans-bush",
            "lettuce-leaf", "parsley", "swiss-chard"])
        self.assertEqual(P.EXPECTED_READINGS["lettuce-leaf"], [("uiuc_ext", [4, 6], [1, 1])])
        self.assertEqual(P.EXPECTED_READINGS["green-beans-bush"], [("uiuc_ext", [2, 3], [1, 1])])
        self.assertEqual(P.EXPECTED_READINGS["parsley"], [("uiuc_ext", [1, 1], [0.5, 0.5])])
        self.assertEqual(P.EXPECTED_READINGS["eggplant"],
                         [("uiuc_ext", [1, 1], [2, 2]), ("umd_ext", [1, 1], [8, 10])])
        self.assertEqual(sum(len(v) for v in P.EXPECTED_READINGS.values()), N_READINGS)

    def test_the_planner_effect_is_the_approved_two(self):
        self.assertEqual(sorted(P.PLANNER_EFFECT), ["green-beans-bush", "lettuce-leaf"])
        self.assertEqual(P.PLANNER_EFFECT["green-beans-bush"],
                         {"before_min_pot_gallons": 5, "after_gallons_per_plant": 0.5})
        self.assertEqual(P.PLANNER_EFFECT["lettuce-leaf"],
                         {"before_min_pot_gallons": 1, "after_gallons_per_plant": 0.25})

    def test_base_carries_no_key_and_no_record_anywhere(self):
        self.assertEqual(sum(1 for c in self.data["crops"]
                             if "plants_per_pot" in (c.get("container_notes") or {})), 0)
        self.assertEqual(sum(1 for c in self.data["crops"]
                             for x in ((c.get("verification_status") or {}).get("field_additions") or [])
                             if isinstance(x, dict) and x.get("field") == "plants_per_pot"), 0)

    def test_the_null_crop_fixture_is_clean(self):
        c = P.by_slug(self.data)[NULL_CROP]
        self.assertIs(c["container_notes"].get("container_ok"), True)
        self.assertNotIn(NULL_CROP, P.EXPECTED_READINGS)

    def test_every_authored_crop_is_certified_and_container_ok_on_the_base(self):
        idx = P.by_slug(self.data)
        for slug in P.EXPECTED_READINGS:
            self.assertTrue(P._certified(idx[slug]), slug)
            self.assertIs(idx[slug]["container_notes"].get("container_ok"), True, slug)

    def test_the_base_has_no_uiuc_anchor_on_the_table_page(self):
        """Spec 3, property 3: the Illinois TABLE page anchors nothing in container_notes today,
        which is why the reading carries its own source instead of joining the block's."""
        table = "https://extension.illinois.edu/container-gardens/growing-vegetables-containers"
        hits = [c["slug"] for c in self.data["crops"]
                for v in ((c.get("container_notes") or {}).get("anchoring_urls") or {}).values()
                if isinstance(v, dict) and v.get("url") == table]
        self.assertEqual(hits, [])

    def test_lettuce_leaf_already_anchors_uiuc_at_a_different_page(self):
        """The concrete reason the sources are PER READING: a block-level uiuc_ext entry would
        OVERWRITE this one. If that stops being true, the argument needs re-reading."""
        au = P.by_slug(self.data)["lettuce-leaf"]["container_notes"]["anchoring_urls"]
        self.assertIn("uiuc_ext", au)
        self.assertIn("container-drainage-options", au["uiuc_ext"]["url"])


class SpecShape(Base):
    def test_the_spec_passes(self):
        self.assertEqual(P.check_spec_shape(self.spec, N_AUTHORED), N_AUTHORED)

    def test_refuses_a_spec_on_another_base(self):
        s = self.fresh_spec(); s["base_sha"] = "0" * 64
        self.assertRefuses("not the pinned base", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_fetch_date_drift(self):
        s = self.fresh_spec(); s["fetch_date"] = "2026-01-01"
        self.assertRefuses("is not 2026-09-21", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_an_authored_count_drift(self):
        s = self.fresh_spec(); s["authored"].pop()
        self.assertRefuses("authored crops, pinned", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_crop_not_in_the_ruling(self):
        s = self.fresh_spec(); self.row(s, "cabbage")["crop"] = NULL_CROP
        self.assertRefuses("authored crop set is not the ruled one", P.check_spec_shape, s, N_AUTHORED)

    def test_a_duplicated_crop_is_caught_by_the_set_comparison(self):
        """There is deliberately NO duplicate-crop guard: with the row count pinned at 7 and the
        crop SET compared to the 7 ruled crops, a duplicate necessarily shrinks the set. The PLA-465
        pattern's dedicated guard would be unreachable here, so it was removed rather than shipped
        as coverage. This test records that the defect is still CAUGHT, by the earlier check."""
        s = self.fresh_spec(); s["authored"][1] = copy.deepcopy(s["authored"][0])
        self.assertRefuses("authored crop set is not the ruled one", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_row_with_the_wrong_keys(self):
        s = self.fresh_spec(); s["authored"][0]["extra"] = 1
        self.assertRefuses("has keys", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_count_other_than_the_ruled_one(self):
        s = self.fresh_spec(); self.row(s, "lettuce-leaf")["readings"][0]["count"] = [4, 5]
        self.assertRefuses("readings are", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_an_at_gallons_other_than_the_ruled_one(self):
        s = self.fresh_spec(); self.row(s, "parsley")["readings"][0]["at_gallons"] = [1, 1]
        self.assertRefuses("readings are", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_reading_order_swap_on_the_two_reading_crop(self):
        """eggplant's two readings are ordered uiuc then umd; the card renders in the order
        authored (7.1), so the order is part of the ruling, not an implementation detail."""
        s = self.fresh_spec(); r = self.row(s, "eggplant")
        r["readings"].reverse(); r["field_additions"].reverse()
        self.assertRefuses("readings are", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_missing_provenance_record(self):
        s = self.fresh_spec(); self.row(s, "eggplant")["field_additions"].pop()
        self.assertRefuses("one per reading", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_readings_total_drift(self):
        """A crop could carry the ruled readings and the TOTAL still be wrong if the ruling itself
        were edited, so the total is pinned separately from the per-crop comparison."""
        s = self.fresh_spec()
        r = self.row(s, "eggplant")
        saved = copy.deepcopy(P.EXPECTED_READINGS["eggplant"])
        P.EXPECTED_READINGS["eggplant"] = saved[:1]
        r["readings"] = r["readings"][:1]; r["field_additions"] = r["field_additions"][:1]
        try:
            self.assertRefuses("readings, pinned", P.check_spec_shape, s, N_AUTHORED)
        finally:
            P.EXPECTED_READINGS["eggplant"] = saved

    def test_refuses_a_field_addition_shape(self):
        s = self.fresh_spec(); del s["authored"][0]["field_additions"][0]["note"]
        self.assertRefuses("wrong shape", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_field_addition_date(self):
        s = self.fresh_spec(); s["authored"][0]["field_additions"][0]["date"] = "2026-01-01"
        self.assertRefuses("field_addition date", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_field_addition_without_sources(self):
        s = self.fresh_spec(); s["authored"][0]["field_additions"][0]["sources"] = []
        self.assertRefuses("carries no sources", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_note_that_names_no_page(self):
        s = self.fresh_spec(); s["authored"][0]["field_additions"][0]["note"] = "read it, trust me"
        self.assertRefuses("does not name its page", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_note_that_quotes_no_digest(self):
        s = self.fresh_spec(); fa = s["authored"][0]["field_additions"][0]
        fa["note"] = fa["note"].replace("sha256", "checksum")
        self.assertRefuses("quotes no digest", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_note_that_quotes_no_source_text(self):
        s = self.fresh_spec(); fa = s["authored"][0]["field_additions"][0]
        fa["note"] = fa["note"].replace("verbatim:", "roughly:")
        self.assertRefuses("quotes no source text", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_an_em_dash_in_a_record(self):
        s = self.fresh_spec(); fa = s["authored"][0]["field_additions"][0]
        fa["note"] = fa["note"].replace(". ", "— ", 1)
        self.assertRefuses("em or en dash", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_record_crediting_another_institution(self):
        """Correct EVERY field carrying an attribution: a record that credits a page its reading
        does not cite is a fabricated credit, even when both pages are real and admitted.

        The driver ADDS a second credit and also adds that page's digest to the note, so the
        per-record digest guard is satisfied and this reaches the credit guard itself. Replacing
        the credit outright is caught one guard later, on the digest, which is a different defect
        and would have graded this mutation caught for the wrong reason (measured: it did)."""
        s = self.fresh_spec(); fa = self.row(s, "cabbage")["field_additions"][0]
        fa["sources"] = ["uiuc_ext", "umd_ext"]
        fa["note"] = fa["note"] + " " + P.EVIDENCE_HASHES["umd_ext"]
        self.assertRefuses("but its record credits", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_record_that_does_not_name_its_url(self):
        s = self.fresh_spec(); r = self.row(s, "cabbage")
        r["readings"][0]["anchoring_urls"]["uiuc_ext"]["url"] = "https://extension.illinois.edu/other"
        self.assertRefuses("does not name the url", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_spec_with_no_source_ledger(self):
        s = self.fresh_spec(); s["source_ledger"] = []
        self.assertRefuses("no source_ledger", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_ledger_entry_with_wrong_keys(self):
        s = self.fresh_spec(); s["source_ledger"][0]["extra"] = 1
        self.assertRefuses("source_ledger entry has keys", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_an_unrecognised_ledger_outcome(self):
        s = self.fresh_spec(); s["source_ledger"][0]["outcome"] = "SKIPPED"
        self.assertRefuses("is not one of", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_ledger_entry_with_no_reason(self):
        """A hold is a DECISION. A held row with no recorded reason is an omission wearing a label."""
        s = self.fresh_spec()
        held = next(e for e in s["source_ledger"] if e["outcome"].startswith("HELD"))
        held["why"] = "  "
        self.assertRefuses("records no reason", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_ledger_that_authors_a_different_set(self):
        s = self.fresh_spec()
        e = next(x for x in s["source_ledger"] if x["outcome"].startswith("AUTHORED"))
        e["outcome"] = "AUTHORED -> ghost-crop"
        self.assertRefuses("source_ledger authors", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_fabricated_digest(self):
        s = self.fresh_spec()
        fa = s["authored"][0]["field_additions"][0]
        fa["note"] = fa["note"] + " " + ("a" * 64)
        self.assertRefuses("not a measured", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_source_set_other_than_the_measured_one(self):
        s = self.fresh_spec(); s["sources"]["extra_ext"] = dict(s["sources"]["uiuc_ext"])
        self.assertRefuses("spec sources are", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_digests_swapped_between_the_two_sources(self):
        """The blanket scan CANNOT see this: after a swap both digests are still measured ones.
        Measured, a bare membership check here was redundant and its mutation SURVIVED, caught by
        the scan firing first. Keyed per source, it catches the swap."""
        s = self.fresh_spec()
        s["sources"]["uiuc_ext"]["sha256"], s["sources"]["umd_ext"]["sha256"] = (
            s["sources"]["umd_ext"]["sha256"], s["sources"]["uiuc_ext"]["sha256"])
        self.assertRefuses("for that page", P.check_spec_shape, s, N_AUTHORED)

    def test_refuses_a_record_quoting_the_other_pages_digest(self):
        """Correct EVERY field carrying an attribution. A record may name the right institution and
        still quote the wrong page's bytes, and that digest is legitimately 'measured'."""
        s = self.fresh_spec(); fa = self.row(s, "cabbage")["field_additions"][0]
        fa["note"] = fa["note"].replace(P.EVIDENCE_HASHES["uiuc_ext"], P.EVIDENCE_HASHES["umd_ext"])
        self.assertRefuses("quotes another page's digest", P.check_spec_shape, s, N_AUTHORED)

    def test_the_digest_guard_accepts_the_real_digests(self):
        """Refusal-spec both ways: a guard that rejected the REAL digests would also be 'green'
        on the fabricated one, so assert the matcher in both directions."""
        self.assertEqual(sorted(P.EVIDENCE_HASHES), ["uiuc_ext", "umd_ext"])
        self.assertEqual(len(P.MEASURED_DIGESTS), 2)
        for d in P.MEASURED_DIGESTS:
            s = self.fresh_spec()
            fa = s["authored"][0]["field_additions"][0]
            fa["note"] = fa["note"] + " " + d
            self.assertEqual(P.check_spec_shape(s, N_AUTHORED), N_AUTHORED)

    def test_refuses_an_expected_block_drift(self):
        s = self.fresh_spec(); s["expected"]["null"] = 0
        self.assertRefuses("expected block", P.check_spec_shape, s, N_AUTHORED)


class PreState(Base):
    def test_pre_state_passes(self):
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_AUTHORED)

    def test_refuses_a_roster_drift(self):
        d = self.fresh_data()
        d["crops"].append(copy.deepcopy(P.by_slug(d)["lime"])); d["crops"][-1]["slug"] = "ghost-crop"
        self.assertRefuses("roster is 129", P.check_pre_state, self.spec, d)

    def test_refuses_a_certified_count_drift(self):
        d = self.fresh_data()
        P.by_slug(d)["avocado"]["verification_status"]["status"] = "verified_gs_arc"
        self.assertRefuses("certified crops, pinned", P.check_pre_state, self.spec, d)

    def test_refuses_a_crop_already_carrying_the_key(self):
        d = self.fresh_data()
        P.by_slug(d)[NULL_CROP]["container_notes"]["plants_per_pot"] = None
        self.assertRefuses("already carries container_notes.plants_per_pot", P.check_pre_state, self.spec, d)

    def test_refuses_field_additions_not_a_list(self):
        d = self.fresh_data()
        P.by_slug(d)[NULL_CROP]["verification_status"]["field_additions"] = None
        self.assertRefuses("field_additions is not a list", P.check_pre_state, self.spec, d)

    def test_refuses_a_prior_plants_per_pot_record(self):
        d = self.fresh_data()
        P.by_slug(d)[NULL_CROP]["verification_status"]["field_additions"].append(a_record())
        self.assertRefuses("already records a plants_per_pot addition", P.check_pre_state, self.spec, d)

    def test_refuses_an_authored_crop_off_the_roster(self):
        s = self.fresh_spec(); self.row(s, "cabbage")["crop"] = "ghost-crop"
        self.assertRefuses("is not on the roster", P.check_pre_state, s, self.data)

    def test_refuses_an_authored_shell(self):
        s = self.fresh_spec(); self.row(s, "cabbage")["crop"] = "avocado"
        self.assertRefuses("is not certified", P.check_pre_state, s, self.data)

    def test_refuses_an_authored_crop_that_cannot_go_in_a_pot(self):
        """plum is certified and NOT container_ok on 079e3923: a per-pot count needs a pot."""
        self.assertIsNot(
            P.by_slug(self.data)["plum"]["container_notes"].get("container_ok"), True)
        s = self.fresh_spec(); self.row(s, "cabbage")["crop"] = "plum"
        self.assertRefuses("is not container_ok", P.check_pre_state, s, self.data)

    def test_refuses_a_source_not_in_catalog(self):
        s = self.fresh_spec(); s["authored"][0]["field_additions"][0]["sources"] = ["nobody_ext"]
        self.assertRefuses("is not in source_catalog", P.check_pre_state, s, self.data)

    def test_refuses_a_row_the_gate_rejects(self):
        s = self.fresh_spec(); self.row(s, "lettuce-leaf")["readings"][0]["count"] = [6, 4]
        self.assertRefuses("fails plants_per_pot_gate", P.check_pre_state, s, self.data)

    def test_refuses_a_row_the_bounds_reject(self):
        s = self.fresh_spec(); self.row(s, "lettuce-leaf")["readings"][0]["count"] = [4, 99]
        self.assertRefuses("fails numeric_sanity", P.check_pre_state, s, self.data)


class ApplyAndPost(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_apply_changes_exactly_the_declared_split(self):
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec),
                         (N_KEYS, N_AUTHORED, N_KEYS - N_AUTHORED, N_READINGS))

    def test_every_certified_crop_carries_the_key_and_no_shell_does(self):
        post = self.post()
        carrying = {c["slug"] for c in post["crops"]
                    if "plants_per_pot" in (c.get("container_notes") or {})}
        certified = {c["slug"] for c in post["crops"] if P._certified(c)}
        self.assertEqual(carrying, certified)
        self.assertEqual(len(certified), N_KEYS)

    def test_authored_values_are_the_spec_rows(self):
        idx = P.by_slug(self.post())
        for r in self.spec["authored"]:
            self.assertEqual(idx[r["crop"]]["container_notes"]["plants_per_pot"],
                             {"readings": r["readings"]})

    def test_the_other_certified_crops_are_null(self):
        idx = P.by_slug(self.post())
        authored = set(P.EXPECTED_READINGS)
        nulls = [s for s, c in idx.items()
                 if P._certified(c) and c["container_notes"]["plants_per_pot"] is None]
        self.assertEqual(len(nulls), N_KEYS - N_AUTHORED)
        self.assertEqual(set(nulls) & authored, set())

    def test_no_shell_changes(self):
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for s in pre:
            if not P._certified(pre[s]):
                self.assertEqual(pre[s], post[s], s)

    def test_post_gate_is_clean_with_presence_on(self):
        self.assertEqual(P.PPG.all_violations(self.post(), presence=True), [])

    def test_check_post_passes_and_returns_the_effect(self):
        self.assertEqual(P.check_post(self.post(), self.spec),
                         {"green-beans-bush": 0.5, "lettuce-leaf": 0.25})

    def test_refuses_a_post_state_that_fails_the_gate(self):
        post = self.post()
        P.by_slug(post)["lettuce-leaf"]["container_notes"]["plants_per_pot"]["readings"][0]["count"] = [6, 4]
        self.assertRefuses("plants_per_pot_gate on the post-state", P.check_post, post, self.spec)

    def test_refuses_an_authored_crop_that_fails_the_bounds(self):
        """The bounds guard must be reached, so the injection has to be one the SHAPE gate lets
        through: [4, 30] is well-shaped and inside the gate's rules, and only A33 bounds it."""
        post = self.post()
        P.by_slug(post)["lettuce-leaf"]["container_notes"]["plants_per_pot"]["readings"][0]["at_gallons"] = [1, 400]
        self.assertRefuses("numeric_sanity on", P.check_post, post, self.spec)

    def test_refuses_an_authored_crop_that_fails_display_readiness(self):
        post = self.post()
        cn = P.by_slug(post)["lettuce-leaf"]["container_notes"]
        cn["min_pot_gallons"] = None
        cn["depth_inches_min"] = None
        self.assertRefuses("display_readiness on", P.check_post, post, self.spec)

    def test_refuses_a_third_crop_switching(self):
        """A crop gaining the switch is a PRODUCT change. The driver adds both the value and its
        provenance record, so the gate does not answer first and mask the planner guard."""
        post = self.post()
        c = P.by_slug(post)[NULL_CROP]
        c["container_notes"]["plants_per_pot"] = {"readings": [a_reading(count=(2, 3))]}
        c["verification_status"]["field_additions"].append(a_record())
        self.assertRefuses("the planner switches on", P.check_post, post, self.spec)

    def test_refuses_a_crop_losing_the_switch(self):
        post = self.post()
        P.by_slug(post)["lettuce-leaf"]["container_notes"]["plants_per_pot"]["readings"][0]["count"] = [1, 1]
        self.assertRefuses("the planner switches on", P.check_post, post, self.spec)

    def test_refuses_a_planner_figure_other_than_approved(self):
        """The switch SET is unchanged and only the figure moves, so this reaches the second
        guard rather than the set comparison."""
        post = self.post()
        P.by_slug(post)["lettuce-leaf"]["container_notes"]["plants_per_pot"]["readings"][0]["at_gallons"] = [2, 2]
        self.assertRefuses("gal/plant, approved", P.check_post, post, self.spec)

    def test_refuses_a_moved_min_pot_gallons_basis(self):
        """PLANNER_EFFECT records what the switch is measured AGAINST. If PLA-533 moves a
        min_pot_gallons under this pass, the recorded 10x and 4x stop being true and the promote
        must refuse rather than carry a stale comparison into a landing record."""
        post = self.post()
        P.by_slug(post)["lettuce-leaf"]["container_notes"]["min_pot_gallons"] = 2
        self.assertRefuses("approved against", P.check_post, post, self.spec)


class NamedControls(Base):
    """THE TWO CONTROLS OWED BY NAME (spec section 8). Neither path is exercised by any authored
    crop, so both run on SYNTHETIC readings injected into the post-state and driven through
    check_post's planner guard -- the real entry point, not the formula in isolation."""

    def post(self):
        return P.apply_to(self.data, self.spec)

    def _inject(self, post, slug, readings):
        c = P.by_slug(post)[slug]
        c["container_notes"]["plants_per_pot"] = {"readings": readings}
        c["verification_status"]["field_additions"].append(a_record())
        return c

    def test_control_the_two_reading_conservative_maximum(self):
        """RULING 2, on a synthetic fixture. eggplant is the only two-reading crop on real data and
        BOTH its readings are count-1, so ruling 3 keeps min_pot_gallons and the maximum is never
        taken. Here one count>1 reading (1 / 2 = 0.5 gal/plant) triggers the switch and one
        cautious count-1 reading (10 / 1 = 10.0) restrains it. The MAXIMUM must win, or UMD's
        caution is silently discarded -- which is the whole point of ruling 2.

        The fixture discriminates: max gives 10.0, min would give 0.5, and the two differ."""
        loose = a_reading(count=(2, 3), gallons=(1, 1), src="uiuc_ext")
        cautious = a_reading(count=(1, 1), gallons=(8, 10), src="umd_ext")
        self.assertEqual(P.PPG.conservative_gallons_per_plant(loose), 0.5)
        self.assertEqual(P.PPG.conservative_gallons_per_plant(cautious), 10.0)
        self.assertNotEqual(0.5, 10.0)

        post = self.post()
        self._inject(post, NULL_CROP, [loose, cautious])
        self.assertEqual(P.PPG.all_violations(post, presence=True), [],
                          "the control fixture must be gate-legal, or the gate answers first")
        self.assertEqual(P.planner_effect(post)[NULL_CROP], 10.0)
        # and it reaches the real guard: the switch set now has a third crop
        self.assertRefuses("the planner switches on", P.check_post, post, self.spec)

    def test_control_the_count_min_divisor_on_a_2_6_reading(self):
        """AMENDMENT 4, on a synthetic fixture. A [2, 6] count DISTINGUISHES count[0] from
        count[1]: at 1 gallon it prices at 1/2 = 0.5, where count[1] would give 1/6 = 0.167.

        A [4, 4] FIXTURE WOULD PASS UNDER EITHER END and is not a control. That is asserted
        below, so the reason this fixture is [2, 6] cannot be lost to a later simplification."""
        r = a_reading(count=(2, 6), gallons=(1, 1))
        self.assertEqual(P.PPG.conservative_gallons_per_plant(r), 0.5)
        self.assertNotEqual(1 / 2, 1 / 6)
        flat = a_reading(count=(4, 4), gallons=(1, 1))
        self.assertEqual(flat["at_gallons"][1] / flat["count"][0],
                         flat["at_gallons"][1] / flat["count"][1],
                         "a [4,4] fixture cannot tell the two divisors apart; keep [2,6]")

        post = self.post()
        self._inject(post, NULL_CROP, [r])
        self.assertEqual(P.PPG.all_violations(post, presence=True), [])
        self.assertEqual(P.planner_effect(post)[NULL_CROP], 0.5)
        self.assertRefuses("the planner switches on", P.check_post, post, self.spec)

    def test_control_at_gallons_hi_is_the_numerator(self):
        """The band's roomier end (spec 4.2). [8, 10] must price at 10, not 8; a [n, n] fixture
        could not tell those apart, which is why the control uses UMD's real band."""
        self.assertEqual(P.PPG.conservative_gallons_per_plant(a_reading(count=(1, 2), gallons=(8, 10))), 10.0)
        self.assertNotEqual(10 / 1, 8 / 1)


class BlastRadius(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_set_equality_holds_before_any_value_comparison(self):
        """Iterating `pre` alone makes everything ADDED in `post` invisible, which was all four
        PLA-162 defects. Assert the roster sets are equal, both directions."""
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        self.assertEqual(set(pre), set(post))
        self.assertEqual(len(pre), len(post))

    def test_refuses_a_top_level_key_addition(self):
        post = self.post(); post["injected_top_key"] = 1
        self.assertRefuses("top-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_top_level_change(self):
        post = self.post(); post["control_methods"] = {}
        self.assertRefuses("top-level key 'control_methods' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_source_catalog_change(self):
        """This pass admits no source; both are already in the catalog."""
        post = self.post(); post["source_catalog"]["uiuc_ext"]["name"] = "changed"
        self.assertRefuses("top-level key 'source_catalog' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_roster_change(self):
        post = self.post(); post["crops"].pop()
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_appended_crop(self):
        """A CLONE APPENDED TO THE ROSTER is the PLA-162 defect all four guards missed."""
        post = self.post()
        ghost = copy.deepcopy(P.by_slug(post)["lime"]); ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_shell_change(self):
        post = self.post()
        P.by_slug(post)["avocado"]["container_notes"]["plants_per_pot"] = None
        self.assertRefuses("shell avocado changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_crop_level_key_set_drift(self):
        post = self.post(); P.by_slug(post)[NULL_CROP]["injected"] = 1
        self.assertRefuses("crop-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_change_outside_container_notes(self):
        post = self.post()
        self.assertIn("propagule", P.by_slug(post)[NULL_CROP])
        P.by_slug(post)[NULL_CROP]["propagule"] = "cutting"
        self.assertRefuses("changed outside container_notes", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_container_notes_key_set_drift(self):
        post = self.post()
        del P.by_slug(post)[NULL_CROP]["container_notes"]["plants_per_pot"]
        self.assertRefuses("is not the base's plus plants_per_pot", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_container_notes_key_addition(self):
        post = self.post()
        P.by_slug(post)[NULL_CROP]["container_notes"]["injected"] = 1
        self.assertRefuses("is not the base's plus plants_per_pot", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_change_to_another_container_notes_field(self):
        """min_pot_gallons is explicitly NOT touched by this pass (spec section 1)."""
        post = self.post()
        P.by_slug(post)["lettuce-leaf"]["container_notes"]["min_pot_gallons"] = 2
        self.assertRefuses("container_notes.min_pot_gallons changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_prose_change_in_container_notes(self):
        post = self.post()
        P.by_slug(post)["lettuce-leaf"]["container_notes"]["notes_seasoned"] = "rewritten"
        self.assertRefuses("container_notes.notes_seasoned changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_written_value_other_than_the_spec_row(self):
        post = self.post()
        P.by_slug(post)["lettuce-leaf"]["container_notes"]["plants_per_pot"]["readings"][0]["count"] = [4, 7]
        self.assertRefuses("written plants_per_pot is not the spec row's", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_reading_on_an_authored_crop(self):
        post = self.post()
        P.by_slug(post)["cabbage"]["container_notes"]["plants_per_pot"]["readings"].append(a_reading(src="umd_ext"))
        self.assertRefuses("written plants_per_pot is not the spec row's", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_value_on_a_crop_with_no_row(self):
        post = self.post()
        P.by_slug(post)[NULL_CROP]["container_notes"]["plants_per_pot"] = {"readings": [a_reading()]}
        self.assertRefuses("carries a plants_per_pot value with no authored row", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_empty_readings_list_on_a_null_crop(self):
        """`{readings: []}` is not the same as null, and would assert 'assessed, none found'."""
        post = self.post()
        P.by_slug(post)[NULL_CROP]["container_notes"]["plants_per_pot"] = {"readings": []}
        self.assertRefuses("carries a plants_per_pot value with no authored row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_readings_count_drift_in_the_written_state(self):
        """A spec row could carry fewer readings and still match ITSELF, so the TOTAL is pinned
        in verify_post as well as in check_spec_shape."""
        spec = self.fresh_spec(); r = self.row(spec, "eggplant")
        r["readings"] = r["readings"][:1]; r["field_additions"] = r["field_additions"][:1]
        post = P.apply_to(self.data, spec)
        self.assertRefuses("readings written, pinned", P.verify_post, self.data, post, spec)

    def test_refuses_a_verification_status_key_addition(self):
        post = self.post(); P.by_slug(post)[NULL_CROP]["verification_status"]["injected"] = 1
        self.assertRefuses("verification_status key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_verification_status_value_change(self):
        post = self.post(); P.by_slug(post)[NULL_CROP]["verification_status"]["phase"] = "changed"
        self.assertRefuses("verification_status.phase changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_status_flip(self):
        """This pass touches no status and no launch_ready flag."""
        post = self.post(); P.by_slug(post)[NULL_CROP]["verification_status"]["launch_ready_core"] = False
        self.assertRefuses("verification_status.launch_ready_core changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_rewritten_field_additions_prefix(self):
        post = self.post()
        fa = P.by_slug(post)["lettuce-leaf"]["verification_status"]["field_additions"]
        self.assertGreater(len(fa), 1, "driver needs a crop with a pre-existing field_additions entry")
        fa[0]["note"] = "rewritten"
        self.assertRefuses("prefix is not byte-identical", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_record_other_than_the_spec(self):
        post = self.post()
        P.by_slug(post)["cabbage"]["verification_status"]["field_additions"][-1]["sources"] = ["other"]
        self.assertRefuses("appended 1 entries, expected 1 matching the spec", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_appended_record(self):
        post = self.post()
        P.by_slug(post)[NULL_CROP]["verification_status"]["field_additions"].append({"field": "stray"})
        self.assertRefuses("appended 1 entries, expected 0", P.verify_post, self.data, post, self.spec)

    def test_the_two_reading_crop_takes_two_records(self):
        post = self.post()
        pre_fa = P.by_slug(self.data)["eggplant"]["verification_status"]["field_additions"]
        post_fa = P.by_slug(post)["eggplant"]["verification_status"]["field_additions"]
        self.assertEqual(len(post_fa) - len(pre_fa), 2)
        self.assertEqual([x["sources"] for x in post_fa[len(pre_fa):]], [["uiuc_ext"], ["umd_ext"]])


class Serializer(Base):
    def test_compact_no_trailing_newline(self):
        self.assertEqual(P.serialize({"a": [1, 2], "b": "eé"}), b'{"a":[1,2],"b":"e\xc3\xa9"}')

    def test_output_sha_is_stable(self):
        a = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        b = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        self.assertEqual(a, b)


class WriteGuards(Base):
    def _copy(self):
        d = tempfile.mkdtemp(prefix="pla580_wg_")
        p = os.path.join(d, "crops_data_final.json")
        with open(p, "wb") as f:
            f.write(promote_fixture.pre_state(P.BASE_SHA))
        return d, p

    def _run(self, *args):
        r = subprocess.run(
            [sys.executable, os.path.join(HERE, "promote_pla580_plants_per_pot.py"), *args],
            capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def test_refuses_to_write_without_expect_sha(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p)
            self.assertNotEqual(rc, 0); self.assertIn("requires --expect-sha", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)

    def test_refuses_out_that_targets_the_canonical(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p, "--out", p)
            self.assertNotEqual(rc, 0); self.assertIn("may not target the canonical", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)

    def test_refuses_a_wrong_expect_sha_and_leaves_the_copy_untouched(self):
        d, p = self._copy()
        try:
            rc, out = self._run(p, "--expect-sha", "0" * 64)
            self.assertNotEqual(rc, 0); self.assertIn("REFUSED: expected", out)
            self.assertEqual(P.sha256_bytes(open(p, "rb").read()), BASE_SHA)
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
