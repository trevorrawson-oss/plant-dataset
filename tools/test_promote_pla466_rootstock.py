#!/usr/bin/env python3
"""Guard suite for promote_pla466_rootstock, pinned to base 1721208e.

The fixture is REBUILT from the pinned base via promote_fixture, never read from live canonical.
A suite that reads live canonical goes silently vacuous the moment canonical moves, reporting
green while running zero checks (PLA-215). pre_state() raises rather than skipping if the base
cannot be rebuilt.

Every guard family below has at least one test that injects the defect and asserts the promote
REFUSES. The happy path is also asserted, so a promote that refuses EVERYTHING cannot pass by
looking strict: that is the positive control this suite carries internally, alongside the whole
suite serving as the harness's control.
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import promote_pla466_rootstock as P  # noqa: E402
import promote_fixture as FIX  # noqa: E402


def fresh():
    return json.loads(FIX.pre_state(P.BASE_SHA))


class Base(unittest.TestCase):
    def assertRefuses(self, needle, data):
        with self.assertRaises(SystemExit) as cm:
            P.run(data)
        self.assertIn(needle, str(cm.exception))

    def crop(self, data, slug):
        return P.by_slug(data)[slug]


class TestFixture(Base):
    def test_fixture_is_the_pinned_base(self):
        raw = FIX.pre_state(P.BASE_SHA)
        self.assertEqual(P.sha256_bytes(raw), P.BASE_SHA)

    def test_fixture_is_not_live_canonical_by_accident(self):
        """If canonical ever equals the base the suite is still reading the REBUILT bytes."""
        d = fresh()
        self.assertEqual(len(d["crops"]), P.ROSTER)


class TestHappyPath(Base):
    """The positive control. If these fail, every refusal below is meaningless."""

    def setUp(self):
        self.pre = fresh()
        self.post = P.run(copy.deepcopy(self.pre))

    def test_it_runs_and_is_deterministic(self):
        again = P.run(copy.deepcopy(self.pre))
        self.assertEqual(P.serialize(self.post), P.serialize(again))

    def test_exactly_seven_crops_change(self):
        a, b = P.by_slug(self.pre), P.by_slug(self.post)
        self.assertEqual(set(a), set(b))  # SET before VALUE
        self.assertEqual(sorted(s for s in a if a[s] != b[s]), P.EXPECTED_CHANGED_CROPS)

    def test_st_julien_is_gone_and_citation_is_in(self):
        rows = [e["name"] for e in self.crop(self.post, "plum")["rootstock_options"]]
        self.assertEqual(rows, P.PLUM_POST_NAMES)
        self.assertNotIn(P.DROP_ROW, rows)

    def test_citation_row_is_byte_equal_to_spec(self):
        r = P.row_of(self.crop(self.post, "plum"), P.CITATION_ROW["name"])
        self.assertEqual(r, P.CITATION_ROW)

    def test_the_48_region_cells_keep_the_dead_credit(self):
        """Values are NOT nulled and the credit is NOT dropped: the T1 re-source comes first."""
        self.assertEqual(P._count_url(self.crop(self.post, "plum"), P.DEAD_PLUM_URL), 48)

    def test_status_never_moves_on_any_crop(self):
        a, b = P.by_slug(self.pre), P.by_slug(self.post)
        for s in a:
            self.assertEqual(a[s]["verification_status"].get("status"),
                             b[s]["verification_status"].get("status"), s)

    def test_basis_is_held_on_lemon_and_lime(self):
        a, b = P.by_slug(self.pre), P.by_slug(self.post)
        for s in ("lemon", "lime"):
            self.assertEqual(a[s]["rootstock_selection_basis"], b[s]["rootstock_selection_basis"])

    def test_four_crops_carry_a_live_blocker_and_launch_false(self):
        n = 0
        for c in self.post["crops"]:
            vs = c["verification_status"]
            live = [f for f in (vs.get("open_findings") or [])
                    if isinstance(f, dict) and f.get("blocks_launch") and f.get("status") != "resolved"]
            if live:
                n += 1
                self.assertIs(vs["launch_ready_core"], False, c["slug"])
                self.assertIs(vs["launch_ready_seasoned"], False, c["slug"])
        self.assertEqual(n, P.EXPECTED_BLOCKERS_AFTER)

    def test_the_exclusion_sentence_is_in_citable_for(self):
        t = self.post["source_catalog"]["ucd_fruitnut"]["citable_for"]
        self.assertIn("NOT citable for per-region planting, bloom or harvest timing.", t)

    def test_every_repointed_anchor_carries_the_fragility_note(self):
        """The generic path is fragile; the note records why AND gives PLA-568 a title to assert."""
        plum = self.crop(self.post, "plum")
        for nm in (P.MYROBALAN_NEW_NAME, "Marianna 2624", P.CITATION_ROW["name"]):
            note = P.row_of(plum, nm)["anchoring_urls"]["ucd_fruitnut"]["note"]
            self.assertIn(P.EXPECTED_PLUM_TITLE, note, nm)
            self.assertIn("GENERIC", note, nm)
            self.assertIn("/node/4506", note, nm)

    def test_the_rooststock_slug_is_recorded_as_uc_davis_own(self):
        ids = [f["id"] for f in self.crop(self.post, "persimmon")["verification_status"]["open_findings"]
               if isinstance(f, dict)]
        self.assertIn("persimmon_rooststock_slug_is_uc_davis_own", ids)
        f = next(x for x in self.crop(self.post, "persimmon")["verification_status"]["open_findings"]
                 if isinstance(x, dict) and x["id"] == "persimmon_rooststock_slug_is_uc_davis_own")
        self.assertIn("DO NOT 'FIX' THIS URL", f["summary"])
        self.assertIn("would produce a 404", f["summary"])

    def test_the_chill_candidate_is_recorded_as_read_and_rejected(self):
        for slug in ("apple", "pear-european", "pear-asian"):
            blob = json.dumps(self.crop(self.post, slug)["verification_status"]["open_findings"])
            self.assertIn("READ AND REJECTED", blob, slug)
            self.assertIn(P.CHILL_CANDIDATE_SHA, blob, slug)

    def test_lemon_and_lime_record_the_narrow_scope(self):
        for slug in ("lemon", "lime"):
            blob = json.dumps(self.crop(self.post, slug)["verification_status"]["open_findings"])
            self.assertIn("only the tristeza claim is corrected", blob, slug)

    def test_the_repointed_url_is_the_pages_own_canonical(self):
        self.assertEqual(P.NEW_PLUM_URL, "https://fruitsandnuts.ucdavis.edu/rootstock-selection")

    def test_no_em_dashes_in_any_new_user_facing_string(self):
        rows = self.crop(self.post, "plum")["rootstock_options"]
        strings = [P.MYROBALAN_PROSE[k] for k in P.MYROBALAN_PROSE]
        strings += [P.CITATION_ROW[k] for k in ("traits_seasoned", "traits_beginner", "what_to_ask_nursery")]
        strings += [P.LEMON_NOTE_NEW, P.LEMON_TRAITS_NEW, P.LIME_NOTE_NEW, P.LIME_TRAITS_NEW]
        strings += [self.crop(self.post, "lemon")["recommended_rootstock_note"],
                    self.crop(self.post, "lime")["recommended_rootstock_note"]]
        strings += [r["traits_seasoned"] for r in rows] + [r["traits_beginner"] for r in rows]
        for s in strings:
            self.assertNotIn("—", s)
            self.assertNotIn("–", s)


class TestCatalogGuards(Base):
    def test_refuses_a_missing_ucd_fruitnut(self):
        d = fresh(); del d["source_catalog"]["ucd_fruitnut"]
        self.assertRefuses("ucd_fruitnut absent", d)

    def test_refuses_a_drifted_citable_for(self):
        d = fresh(); d["source_catalog"]["ucd_fruitnut"]["citable_for"] = "something else"
        self.assertRefuses("not the pinned pre-state text", d)

    def test_refuses_a_non_t1_catalog_entry(self):
        d = fresh(); d["source_catalog"]["ucd_fruitnut"]["tier"] = "T2"
        self.assertRefuses("expected T1", d)

    def test_refuses_collateral_damage_to_another_catalog_entry(self):
        d = fresh()
        orig = P.apply
        def sabotage(data):
            out = orig(data)
            out["source_catalog"]["ucanr_ext"]["citable_for"] = "tampered"
            return out
        P.apply = sabotage
        try:
            self.assertRefuses("source_catalog entry other than ucd_fruitnut changed", d)
        finally:
            P.apply = orig


class TestPlumPreState(Base):
    def test_refuses_a_rootstock_name_drift(self):
        d = fresh(); self.crop(d, "plum")["rootstock_options"][0]["name"] = "Myrobalan"
        self.assertRefuses("plum rootstock names drifted", d)

    def test_refuses_if_st_julien_is_already_absent(self):
        d = fresh()
        p = self.crop(d, "plum")
        p["rootstock_options"] = [e for e in p["rootstock_options"] if e["name"] != P.DROP_ROW]
        self.assertRefuses("names drifted", d)

    def test_refuses_a_marianna_container_drift(self):
        d = fresh(); P.row_of(self.crop(d, "plum"), "Marianna 2624")["container_size_gallons"] = 20
        self.assertRefuses("Marianna container pre-state", d)

    def test_refuses_a_marianna_size_drift(self):
        d = fresh(); P.row_of(self.crop(d, "plum"), "Marianna 2624")["mature_height_ft"] = [10, 16]
        self.assertRefuses("Marianna size pre-state drifted", d)

    def test_refuses_if_myrobalan_is_not_on_the_dead_url(self):
        d = fresh()
        P.row_of(self.crop(d, "plum"), P.PLUM_PRE_NAMES[0])["anchoring_urls"]["ucanr_ext"]["url"] = "https://x"
        self.assertRefuses("not on the dead ucanr_ext URL", d)

    def test_refuses_a_myrobalan_sources_drift(self):
        d = fresh(); P.row_of(self.crop(d, "plum"), P.PLUM_PRE_NAMES[0])["sources"] = ["ucanr_ext"]
        self.assertRefuses("Myrobalan sources", d)

    def test_refuses_if_varieties_credit_is_already_gone(self):
        d = fresh(); v = self.crop(d, "plum")["varieties"]
        v["sources"] = [s for s in v["sources"] if s != "ucanr_ext"]
        self.assertRefuses("does not carry the ucanr_ext credit", d)


class TestLaunchPreState(Base):
    def test_refuses_a_crop_not_launch_ready(self):
        d = fresh(); self.crop(d, "apple")["verification_status"]["launch_ready_core"] = False
        self.assertRefuses("launch_ready is not true/true", d)

    def test_refuses_a_crop_whose_status_is_not_verified(self):
        d = fresh(); self.crop(d, "plum")["verification_status"]["status"] = "shell"
        self.assertRefuses("expected verified_gs_arc", d)

    def test_refuses_a_pre_existing_live_blocker(self):
        d = fresh()
        self.crop(d, "apple")["verification_status"]["open_findings"].append(
            {"id": "x", "blocks_launch": True, "status": "open"})
        self.assertRefuses("already carries a live blocking finding", d)

    def test_refuses_a_chill_cell_count_drift(self):
        """Walk to a real chill-anchored cell and remove the credit, so the pinned count moves."""
        d = fresh()
        removed = []

        def walk(o):
            if removed:
                return
            if isinstance(o, dict):
                for k, v in list(o.items()):
                    if removed:
                        return
                    if k == "anchoring_urls" and isinstance(v, dict):
                        for kk, e in list(v.items()):
                            if isinstance(e, dict) and e.get("url") == P.DEAD_CHILL_URL:
                                del v[kk]
                                removed.append(kk)
                                return
                    elif v is not None:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    if v is not None:
                        walk(v)

        walk(self.crop(d, "apple"))
        self.assertTrue(removed, "fixture carried no chill-anchored cell to mutate")
        self.assertRefuses("chill cells", d)


class TestProseGuards(Base):
    def test_refuses_a_missing_lemon_note_target(self):
        d = fresh(); self.crop(d, "lemon")["recommended_rootstock_note"] = "no target here."
        self.assertRefuses("lemon note target not found exactly once", d)

    def test_refuses_a_doubled_lemon_note_target(self):
        d = fresh(); c = self.crop(d, "lemon")
        c["recommended_rootstock_note"] += " " + P.LEMON_NOTE_OLD
        self.assertRefuses("not found exactly once", d)

    def test_refuses_a_missing_lime_note_target(self):
        d = fresh(); self.crop(d, "lime")["recommended_rootstock_note"] = "no target."
        self.assertRefuses("lime note target not found exactly once", d)

    def test_refuses_when_the_traits_target_is_not_the_last_sentence(self):
        d = fresh(); r = P.row_of(self.crop(d, "lemon"), P.SOUR_ORANGE)
        r["traits_seasoned"] = r["traits_seasoned"] + " Trailing sentence."
        self.assertRefuses("is not the last sentence", d)

    def test_refuses_if_lime_already_has_the_new_source(self):
        d = fresh(); P.row_of(self.crop(d, "lime"), P.SOUR_ORANGE)["sources"].append("uf_ifas_edis")
        self.assertRefuses("already carries uf_ifas_edis", d)

    def test_refuses_a_size_row_that_is_not_semi_dwarf(self):
        d = fresh(); P.row_of(self.crop(d, "lemon"), P.NULL_SIZE_ROWS[0][1])["size_class"] = "standard"
        self.assertRefuses("expected semi_dwarf", d)

    def test_refuses_a_pre_existing_container_null(self):
        d = fresh(); self.crop(d, "apple")["rootstock_options"][0]["container_suitable"] = None
        self.assertRefuses("already null", d)


class TestPostStateGuards(Base):
    """Each injects a defect INTO the applied state, so the post-state guards must catch it."""

    def _post_with(self, sabotage, needle):
        d = fresh()
        orig = P.apply
        def wrapped(data):
            out = orig(data)
            sabotage(P.by_slug(out), out)
            return out
        P.apply = wrapped
        try:
            self.assertRefuses(needle, d)
        finally:
            P.apply = orig

    def test_catches_an_appended_crop(self):
        self._post_with(lambda S, d: d["crops"].append({"slug": "ghost-crop"}),
                        "crop set changed")

    def test_catches_an_unexpected_crop_change(self):
        self._post_with(lambda S, d: S["fig"].__setitem__("name", "Figg"),
                        "changed crops")

    def test_catches_a_failed_repoint(self):
        self._post_with(
            lambda S, d: P.row_of(S["plum"], P.MYROBALAN_NEW_NAME)["anchoring_urls"]["ucd_fruitnut"].__setitem__("url", P.DEAD_PLUM_URL),
            "url did not repoint")

    def test_catches_a_stale_verified_date_carried_onto_the_new_url(self):
        self._post_with(
            lambda S, d: P.row_of(S["plum"], "Marianna 2624")["anchoring_urls"]["ucd_fruitnut"].__setitem__("verified", "2026-06-30"),
            "verified date did not move with the url")

    def test_catches_a_tampered_citation_row(self):
        self._post_with(
            lambda S, d: P.row_of(S["plum"], P.CITATION_ROW["name"]).__setitem__("size_class", "semi_dwarf"),
            "not byte-equal to its spec")

    def test_catches_a_surviving_varieties_credit(self):
        self._post_with(lambda S, d: S["plum"]["varieties"]["sources"].append("ucanr_ext"),
                        "still credits ucanr_ext")

    def test_catches_a_region_credit_dropped_by_mistake(self):
        def nuke(S, d):
            for r in S["plum"]["regions"].values():
                for pl in r.get("plantings") or []:
                    au = pl.get("anchoring_urls") or {}
                    au.pop("ucanr_ext", None)
        self._post_with(nuke, "dead plum URL appears")

    def test_catches_a_moved_status(self):
        self._post_with(lambda S, d: S["plum"]["verification_status"].__setitem__("status", "shell"),
                        "status moved")

    def test_catches_a_blocker_without_the_launch_flip(self):
        self._post_with(
            lambda S, d: S["plum"]["verification_status"].__setitem__("launch_ready_core", True),
            "live blocker but launch_ready is not false")

    def test_catches_a_moved_basis(self):
        self._post_with(lambda S, d: S["lemon"].__setitem__("rootstock_selection_basis", "size_control"),
                        "basis moved")

    def test_catches_a_moved_container_path(self):
        self._post_with(lambda S, d: S["lime"]["container_notes"].__setitem__("container_path", "rootstock"),
                        "container_path/container_ok moved")

    def test_catches_a_lost_finding_id(self):
        self._post_with(lambda S, d: S["plum"]["verification_status"]["open_findings"].pop(0),
                        "lost an existing finding id")

    def test_catches_a_finding_count_drift(self):
        self._post_with(
            lambda S, d: S["plum"]["verification_status"]["open_findings"].append(
                {"id": "extra", "blocks_launch": False, "status": "open"}),
            "new findings, pinned")


class TestSurvivorsFromTheHarness(Base):
    """One test per mutation that SURVIVED the first harness run.

    Each of these existed as a guard in the promote but had no test exercising it, so disabling
    the guard left the suite green. A survivor is an unguarded defect class, not a pass.
    """

    def test_refuses_a_roster_count_drift(self):
        d = fresh(); d["crops"].append(dict(d["crops"][0], slug="ghost-crop"))
        self.assertRefuses("roster", d)

    def test_refuses_a_non_unique_traits_target(self):
        """Reaches replace_once: the pre-state endswith check passes, uniqueness does not."""
        d = fresh(); r = P.row_of(self.crop(d, "lemon"), P.SOUR_ORANGE)
        r["traits_seasoned"] = P.SOUR_ORANGE_TRAITS_OLD + " " + r["traits_seasoned"]
        self.assertRefuses("expected exactly 1", d)

    def _post_sabotage(self, sabotage, needle):
        d = fresh()
        orig = P.apply
        def wrapped(data):
            out = orig(data)
            sabotage(P.by_slug(out), out)
            return out
        P.apply = wrapped
        try:
            self.assertRefuses(needle, d)
        finally:
            P.apply = orig

    def test_catches_a_null_container_count_drift(self):
        self._post_sabotage(
            lambda S, d: P.row_of(S["plum"], "Marianna 2624").__setitem__("container_suitable", False),
            "null container rows, pinned")

    def test_catches_a_null_size_count_drift(self):
        self._post_sabotage(
            lambda S, d: P.row_of(S["lime"], P.NULL_SIZE_ROWS[2][1]).__setitem__("size_class", "standard"),
            "null size_class rows, pinned")

    def test_catches_a_dropped_lime_source(self):
        def strip(S, d):
            r = P.row_of(S["lime"], P.SOUR_ORANGE)
            r["sources"] = [s for s in r["sources"] if s != "uf_ifas_edis"]
        self._post_sabotage(strip, "did not gain uf_ifas_edis")

    def test_catches_a_blocker_count_drift(self):
        """Flip an EXISTING finding rather than adding one: adding would trip the
        findings-count guard first and mask the blocker-count guard this test exists for."""
        def extra(S, d):
            vs = S["lemon"]["verification_status"]
            f = next(x for x in vs["open_findings"] if isinstance(x, dict))
            f["blocks_launch"] = True
            f["status"] = "open"
            vs["launch_ready_core"] = False
            vs["launch_ready_seasoned"] = False
        self._post_sabotage(extra, "carry a live blocker, pinned")


class TestGateOnPostState(Base):
    def test_container_shape_gate_is_clean_on_the_post_state(self):
        import container_path_gate as G
        post = P.run(fresh())
        V = [v for c in post["crops"] for v in G.shape_violations(c)]
        self.assertEqual(V, [])

    def test_container_shape_gate_bounces_a_bad_rootstock_value(self):
        """REFUSAL-SPEC: the new 1(b) rule must redden, or its green above is vacuous."""
        import container_path_gate as G
        post = P.run(fresh())
        plum = P.by_slug(post)["plum"]
        plum["rootstock_options"][0]["container_suitable"] = "yes"
        self.assertTrue(any("must be true, false or null" in v for v in G.shape_violations(plum)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
