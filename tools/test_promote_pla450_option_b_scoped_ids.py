#!/usr/bin/env python3
"""Guard suite for promote_pla450_option_b_scoped_ids -- PLA-450 Option B (Trevor, 2026-09-05).

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (`promote_fixture.pre_state`), never read from live
canonical. SHIPS MUTATION-TESTED (PLA-215): `mutate_pla450_option_b_scoped_ids_suite.py` injects one
mutation per guard family with an anchor preflight, a MUTATION-APPLIED marker, a positive control
and a sentinel that must redden.

THE BASELINE REGISTRY IS PINNED TO A COMMIT. The promote repoints one registry entry, so the
working registry read against the PRE-state gives a transitional 36 / 21 / 15. The baseline the
prediction rests on (36 / 22 / 14) is measured with the registry as committed at 074f9e2, and the
suite asserts the promote reads it from THERE, not from HEAD (which will be the new registry once
this lands) and not from the working copy.

THE PREDICTION IS PINNED TWICE: the promote refuses any other post-state figure, and this suite
pins the same literals so a retuned constant reddens.
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
import promote_pla450_option_b_scoped_ids as P  # noqa: E402
import problem_id_collision_gate as G  # noqa: E402

# ---- PINNED, MEASURED on the passing run. Re-measure on a canonical move; never retune to match.
BASE_SHA = "36d6df6bf3bdd2cac37dc568742c37655d1a739b20c9991285bd9608463925fd"
OUTPUT_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"
ROSTER = 128
N_ROWS = 2
N_LEAVES = 2
N_VARIETY_REFS = 129
N_TOUCHED_IDS = 15
CROPS = ("cilantro-coriander", "edamame")
PREDICTED_BASELINE = {"raw": 36, "registered": 22, "actionable": 14}
PREDICTED = {"raw": 36, "registered": 24, "actionable": 12}
BASELINE_REGISTRY_COMMIT = "074f9e2"


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

    def row(self, spec, crop):
        return next(r for r in spec["rows"] if r["crop"] == crop)

    def entry(self, data, crop, field, name):
        return next(e for e in P.by_slug(data)[crop][field] if e.get("name") == name)

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
        rows = P.rows(self.spec)
        self.assertEqual(len(rows), N_ROWS)
        self.assertTrue(all(r["kind"] == "scope" for r in rows))
        self.assertEqual(tuple(sorted({r["crop"] for r in rows})), tuple(sorted(CROPS)))
        self.assertEqual(tuple(sorted(P.CROPS)), tuple(sorted(CROPS)))

    def test_prediction_constants_are_the_pinned_literals(self):
        self.assertEqual(P.PREDICTED, PREDICTED)
        self.assertEqual(P.PREDICTED_BASELINE, PREDICTED_BASELINE)

    def test_the_ruling_is_the_two_held_pairs(self):
        self.assertEqual(P.RULED, {"bacterial-leaf-spot": ("cilantro-coriander", "bacterial-spot"),
                                   "bacterial-blight": ("edamame", "bacterial-blights")})

    def test_baseline_registry_is_pinned_to_a_commit_not_head(self):
        """Once this promote lands, HEAD's registry is the NEW one and would give 36 / 21 / 15 on
        the pre-state. The pin must be the commit the baseline was measured at."""
        self.assertEqual(P.BASELINE_REGISTRY_COMMIT, BASELINE_REGISTRY_COMMIT)
        head = subprocess.run(["git", "-C", P.REPO, "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
        # allowed to EQUAL head before the commit lands; must never be the literal "HEAD"
        self.assertNotEqual(P.BASELINE_REGISTRY_COMMIT.upper(), "HEAD")
        self.assertTrue(len(head) >= 7)


class SpecShape(Base):
    def test_spec_shape_passes(self):
        self.assertEqual(P.check_spec_shape(self.spec), N_ROWS)

    def test_refuses_a_row_outside_the_ruling(self):
        s = self.fresh_spec()
        s["rows"].append({"kind": "scope", "crop": "dry-bean", "field": "diseases",
                          "name": "Bacterial blights (common and halo)", "from": "bacterial-blights",
                          "to": "dry-bacterial-blights", "diverges_from": "edamame-bacterial-blight"})
        self.assertRefuses("not in Trevor's ruling", P.check_spec_shape, s)

    def test_refuses_the_wrong_crop_for_a_ruled_id(self):
        s = self.fresh_spec()
        self.row(s, "edamame")["crop"] = "cilantro-coriander"
        s["rows"] = [r for r in s["rows"] if r["from"] != "bacterial-leaf-spot"] + \
                    [self.row(self.spec, "cilantro-coriander")]
        self.assertRefuses("is ruled on", P.check_spec_shape, s)

    def test_refuses_the_wrong_diverges_from(self):
        s = self.fresh_spec()
        self.row(s, "edamame")["diverges_from"] = "mulberry-bacterial-blight"
        self.assertRefuses("in the ruling, spec", P.check_spec_shape, s)

    def test_refuses_a_free_form_scoped_id(self):
        s = self.fresh_spec()
        self.row(s, "edamame")["to"] = "soybean-bacterial-blight"
        self.assertRefuses("the pattern is mechanical", P.check_spec_shape, s)

    def test_refuses_a_missing_ruled_row(self):
        s = self.fresh_spec()
        s["rows"] = [r for r in s["rows"] if r["crop"] != "edamame"]
        self.assertRefuses("the ruling covers", P.check_spec_shape, s)

    def test_refuses_a_kind_other_than_scope(self):
        s = self.fresh_spec()
        self.row(s, "edamame")["kind"] = "merge"
        self.assertRefuses("this promote only scopes", P.check_spec_shape, s)


class PreState(Base):
    def test_pre_state_passes(self):
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_ROWS)

    def test_refuses_a_missing_target(self):
        d = self.fresh_data()
        self.entry(d, "edamame", "diseases", "Bacterial blight")["name"] = "Bacterial leaf blight"
        self.assertRefuses("need exactly 1", P.check_pre_state, self.spec, d)

    def test_refuses_an_id_drift(self):
        d = self.fresh_data()
        self.entry(d, "edamame", "diseases", "Bacterial blight")["id"] = "already-moved"
        self.assertRefuses("has drifted", P.check_pre_state, self.spec, d)

    def test_refuses_a_target_with_no_ladder(self):
        d = self.fresh_data()
        self.entry(d, "edamame", "diseases", "Bacterial blight")["control_ladder"] = []
        self.assertRefuses("has no ladder in the pre-state", P.check_pre_state, self.spec, d)

    def test_refuses_a_generic_id_that_is_not_a_singleton(self):
        """THE VACATE PREMISE. If a second crop held the generic id, scoping cilantro's would leave
        it populated and the ruling's reuse argument would not hold."""
        d = self.fresh_data()
        P.by_slug(d)["dry-bean"]["diseases"][0]["id"] = "bacterial-blight"
        self.assertRefuses("the vacate premise is wrong", P.check_pre_state, self.spec, d)

    def test_refuses_a_scoped_id_that_already_exists(self):
        d = self.fresh_data()
        P.by_slug(d)["dry-bean"]["diseases"][0]["id"] = "edamame-bacterial-blight"
        self.assertRefuses("already exists on", P.check_pre_state, self.spec, d)

    def test_refuses_a_diverges_from_that_is_not_live(self):
        d = self.fresh_data()
        for c in d["crops"]:
            for _, e in P.problems(c):
                if e.get("id") == "bacterial-blights":
                    e["id"] = "bean-blights-renamed"
        self.assertRefuses("nothing to diverge from", P.check_pre_state, self.spec, d)


class VarietyRefs(Base):
    def setUp(self):
        self.touched = {r["from"] for r in P.rows(self.spec)} | {r["to"] for r in P.rows(self.spec)}

    def test_all_refs_resolve_pre_and_post(self):
        self.assertEqual(P.check_variety_refs(self.data, self.touched), N_VARIETY_REFS)
        self.assertEqual(P.check_variety_refs(self.post(), self.touched), N_VARIETY_REFS)

    def test_the_129_refs_sit_on_ids_this_promote_never_touches(self):
        hit = [(s, v, jf, pid) for s, v, jf, pid in P.variety_refs(self.data) if pid in self.touched]
        self.assertEqual(hit, [])

    def test_refuses_a_dangling_reference(self):
        d = self.fresh_data()
        v = P.by_slug(d)["apple"]["varieties"]["recommended"][0]
        v["resistance"]["nonexistent-problem"] = "resistant"
        self.assertRefuses("a dangling variety join", P.check_variety_refs, d, self.touched)

    def test_refuses_a_reference_on_a_touched_id(self):
        """REFUSAL SPEC. Resolves on the pre-state (edamame holds bacterial-blight), so only the
        touched-id arm can see it."""
        d = self.fresh_data()
        c = P.by_slug(d)["edamame"]
        if not isinstance(c.get("varieties"), dict):
            c["varieties"] = {"recommended": []}
        c["varieties"].setdefault("recommended", []).append(
            {"id": "probe", "name": "Probe", "resistance": {"bacterial-blight": "resistant"}})
        self.assertRefuses("an id this promote touches", P.check_variety_refs, d, self.touched)

    def test_refuses_a_vanished_join_surface(self):
        d = self.fresh_data()
        for c in d["crops"]:
            if isinstance(c.get("varieties"), dict):
                for x in c["varieties"].get("recommended") or []:
                    if isinstance(x, dict):
                        x.pop("resistance", None)
                        x.pop("ladder_delta", None)
        self.assertRefuses("found zero variety references", P.check_variety_refs, d, self.touched)


class Registry(Base):
    def _with_registry(self, mutate):
        reg = json.load(open(G.REGISTRY_PATH, encoding="utf-8"))
        mutate(reg["deliberately_distinct"])
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(reg, f)
        return path

    def _run_with(self, path):
        orig = G.REGISTRY_PATH
        G.REGISTRY_PATH = path
        try:
            return P.check_registry(self.spec)
        finally:
            G.REGISTRY_PATH = orig
            os.unlink(path)

    def test_registry_passes(self):
        self.assertEqual(P.check_registry(self.spec), 2)

    def test_refuses_a_missing_adjudication(self):
        def mutate(entries):
            entries[:] = [e for e in entries if "cilantro-bacterial-leaf-spot" not in e["ids"]]
        self.assertRefuses("is not adjudicated where the gate reads it",
                           self._run_with, self._with_registry(mutate))

    def test_refuses_a_reason_that_does_not_name_both_organisms(self):
        def mutate(entries):
            for e in entries:
                if "cilantro-bacterial-leaf-spot" in e["ids"]:
                    e["reason"] = e["reason"].replace("Xanthomonas", "another bacterium")
        self.assertRefuses("names both organisms", self._run_with, self._with_registry(mutate))

    def test_refuses_a_reason_that_does_not_cite_its_anchor(self):
        """The ruling: carry the anchors into the registry so the adjudication is sourced where it
        sits. A reason with the organisms but no source is not that."""
        def mutate(entries):
            for e in entries:
                if "edamame-bacterial-blight" in e["ids"] and "bacterial-blights" in e["ids"]:
                    e["reason"] = e["reason"].replace("Clemson", "a bean fact sheet")
        self.assertRefuses("sourced where it sits", self._run_with, self._with_registry(mutate))

    def test_refuses_an_entry_naming_a_vacated_id(self):
        def mutate(entries):
            entries.append({"ids": ["bacterial-blight", "bacterial-blights"], "reason": "x", "ruled": "x"})
        self.assertRefuses("a stale record", self._run_with, self._with_registry(mutate))

    def test_refuses_a_lost_moved_pair(self):
        """The batch-26 mulberry adjudication must survive the repoint under the new id."""
        def mutate(entries):
            entries[:] = [e for e in entries
                          if set(e["ids"]) != {"mulberry-bacterial-blight", "edamame-bacterial-blight"}]
        self.assertRefuses("lost in the repoint", self._run_with, self._with_registry(mutate))


class ApplyAndVacate(Base):
    def test_both_generic_ids_vacate(self):
        self.assertEqual(P.check_vacated(self.post(), self.spec), N_ROWS)
        idx = P.id_index(self.post())
        self.assertNotIn("bacterial-leaf-spot", idx)
        self.assertNotIn("bacterial-blight", idx)
        self.assertEqual(idx["cilantro-bacterial-leaf-spot"], {"cilantro-coriander"})
        self.assertEqual(idx["edamame-bacterial-blight"], {"edamame"})

    def test_refuses_a_generic_id_that_survives(self):
        post = self.post()
        self.entry(post, "edamame", "diseases", "Bacterial blight")["id"] = "bacterial-blight"
        self.assertRefuses("supposed to vacate", P.check_vacated, post, self.spec)

    def test_refuses_a_scoped_id_that_lands_elsewhere(self):
        post = self.post()
        P.by_slug(post)["dry-bean"]["diseases"][0]["id"] = "edamame-bacterial-blight"
        self.assertRefuses("expected exactly", P.check_vacated, post, self.spec)

    def test_within_crop_unique_passes(self):
        self.assertEqual(P.check_within_crop_unique(self.post()), N_TOUCHED_IDS)

    def test_refuses_a_within_crop_duplicate(self):
        post = self.post()
        P.by_slug(post)["edamame"]["pests"][0]["id"] = "edamame-bacterial-blight"
        self.assertRefuses("carries duplicate id(s)", P.check_within_crop_unique, post)


class CollisionPrediction(Base):
    def test_baseline_is_what_the_prediction_rests_on(self):
        self.assertEqual(P.collision_figures(self.data, P.baseline_registry()), PREDICTED_BASELINE)

    def test_the_post_registry_gives_a_transitional_figure_on_the_pre_state(self):
        """Documents WHY the baseline is pinned to a commit: the repointed mulberry entry makes the
        post registry read one registration short on the pre-state."""
        got = P.collision_figures(self.data, P.post_registry())
        self.assertEqual(got, {"raw": 36, "registered": 21, "actionable": 15})

    def test_the_post_registry_is_a_staged_snapshot_carrying_the_ruling(self):
        """The snapshot is what the suite replays forever, so it must carry the adjudications and
        must not name a vacated id. (Equality with the working registry is a WRITE-PATH guard, not
        a suite assertion: the working registry is allowed to move on after this lands.)"""
        r = P.post_registry()
        self.assertTrue(r.registered("cilantro-bacterial-leaf-spot", "bacterial-spot"))
        self.assertTrue(r.registered("edamame-bacterial-blight", "bacterial-blights"))
        self.assertTrue(r.registered("edamame-bacterial-blight", "mulberry-bacterial-blight"))
        self.assertFalse(r.registered("bacterial-blight", "mulberry-bacterial-blight"))
        self.assertTrue(P.check_registry_snapshot_is_current())

    def test_refuses_to_write_when_the_snapshot_is_stale(self):
        """THE WRITE-PATH GUARD, driven by a DIFFERENCE. The first driver only asserted the guard
        returned True while the snapshot already matched, so disabling the guard changed nothing
        and the mutation SURVIVED (harness, 2026-09-06). A guard is tested by the input it refuses."""
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(open(P.REGISTRY_POST, encoding="utf-8").read().replace("PLA-450 Option B", "stale"))
        orig = P.REGISTRY_POST
        P.REGISTRY_POST = path
        try:
            self.assertRefuses("staged registry snapshot differs", P.check_registry_snapshot_is_current)
        finally:
            P.REGISTRY_POST = orig
            os.unlink(path)

    def test_post_state_matches_the_prediction(self):
        self.assertEqual(P.check_collision_prediction(self.data, self.post()), PREDICTED)

    def test_the_pairs_that_retire_and_the_pairs_that_arrive(self):
        pre = {f.pair: f for f in G.scan(self.data, registry=P.baseline_registry())}
        post = {f.pair: f for f in G.scan(self.post(), registry=P.post_registry())}
        gone, new = set(pre) - set(post), set(post) - set(pre)
        self.assertEqual(gone, {("bacterial-blight", "bacterial-blights"),
                                ("bacterial-leaf-spot", "bacterial-spot"),
                                ("bacterial-blight", "mulberry-bacterial-blight")})
        self.assertEqual(new, {("bacterial-spot", "cilantro-bacterial-leaf-spot"),
                               ("bacterial-blights", "edamame-bacterial-blight"),
                               ("edamame-bacterial-blight", "mulberry-bacterial-blight")})
        self.assertTrue(all(post[p].registered for p in new), "a new pair arrived OPEN")
        self.assertTrue(all(post[p].kinds == {G.NAME_SHARED} for p in new),
                        "a new pair fired on more than NAME_SHARED; the prediction assumed no "
                        "ID_NEAR_DUP and no FAMILY_MEMBER")

    def test_refuses_a_baseline_drift(self):
        pre = self.fresh_data()
        self.entry(pre, "tomatillo", "diseases", "Early blight")["id"] = "early-blight-x"
        self.assertRefuses("re-derive the prediction before running",
                           P.check_collision_prediction, pre, self.post())

    def test_refuses_a_post_state_whose_figures_differ(self):
        post = self.post()
        self.entry(post, "cilantro-coriander", "diseases", "Bacterial leaf spot")["id"] = "bacterial-leaf-spot"
        self.assertRefuses("!= PREDICTED", P.check_collision_prediction, self.data, post)


class VerifyPost(Base):
    def test_apply_changes_exactly_the_two_id_leaves(self):
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec), N_LEAVES)

    def test_set_comparison_runs_before_value_comparison(self):
        post = self.post()
        self.entry(post, "edamame", "diseases", "Bacterial blight")["severity_note"] = "added"
        self.assertRefuses("entry key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_crop_level_addition(self):
        post = self.post()
        P.by_slug(post)["edamame"]["ghost_field"] = 1
        self.assertRefuses("crop-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_touched_prose_field(self):
        post = self.post()
        self.entry(post, "edamame", "diseases", "Bacterial blight")["symptoms_beginner"] = "rewritten"
        self.assertRefuses("rewrites ids and nothing else", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_lost_ladder(self):
        post = self.post()
        self.entry(post, "cilantro-coriander", "diseases", "Bacterial leaf spot")["control_ladder"] = []
        self.assertRefuses("lost its ladder", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_dropped_entry(self):
        post = self.post()
        P.by_slug(post)["edamame"]["diseases"] = [
            e for e in P.by_slug(post)["edamame"]["diseases"] if e["name"] != "Bacterial blight"]
        self.assertRefuses("entry count", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_entry_reorder(self):
        post = self.post()
        P.by_slug(post)["edamame"]["diseases"].reverse()
        self.assertRefuses("entry order or name changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_id_change_without_a_spec_row(self):
        post = self.post()
        P.by_slug(post)["edamame"]["pests"][0]["id"] = "edamame-something"
        self.assertRefuses("without a spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_rewrite_not_matching_its_row(self):
        post = self.post()
        self.entry(post, "edamame", "diseases", "Bacterial blight")["id"] = "edamame-bacterial-blightz"
        self.assertRefuses("does not match its spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_fewer_leaves_than_rows(self):
        pre, post = self.fresh_data(), self.post()
        self.entry(pre, "edamame", "diseases", "Bacterial blight")["name"] = "Bacterial leaf blight"
        e = self.entry(post, "edamame", "diseases", "Bacterial blight")
        e["name"], e["id"] = "Bacterial leaf blight", "bacterial-blight"
        self.assertRefuses("id leaves changed, spec has", P.verify_post, pre, post, self.spec)

    def test_refuses_a_touched_untouched_crop(self):
        post = self.post()
        P.by_slug(post)["tomatillo"]["diseases"][0]["id"] = "tampered"
        self.assertRefuses("untouched crop", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_touched_top_level_key(self):
        post = self.post()
        post["control_methods"]["garden_sanitation"]["tier"] = "physical"
        self.assertRefuses("top-level key", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_roster_change(self):
        post = self.post()
        ghost = copy.deepcopy(P.by_slug(post)["edamame"])
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_untouched_crops_are_byte_identical(self):
        pre_i, post_i = P.by_slug(self.data), P.by_slug(self.post())
        n = 0
        for slug in pre_i:
            if slug in CROPS:
                continue
            self.assertEqual(json.dumps(pre_i[slug], sort_keys=True), json.dumps(post_i[slug], sort_keys=True))
            n += 1
        self.assertEqual(n, ROSTER - len(CROPS))

    def test_every_rewritten_entry_keeps_its_ladder_byte_for_byte(self):
        pre_i, post_i = P.by_slug(self.data), P.by_slug(self.post())
        for r in P.rows(self.spec):
            s = next(e for e in pre_i[r["crop"]][r["field"]] if e["name"] == r["name"])
            g = next(e for e in post_i[r["crop"]][r["field"]] if e["name"] == r["name"])
            self.assertEqual(s["control_ladder"], g["control_ladder"])
            self.assertTrue(g["control_ladder"])
            self.assertEqual({k for k in s if s[k] != g[k]}, {"id"})


class Serializer(Base):
    def test_one_serializer_shared_with_the_suite(self):
        blob = P.serialize({"a": "é", "b": 1})
        self.assertEqual(blob, b'{"a":"\xc3\xa9","b":1}')
        self.assertNotIn(b"\n", blob)
        self.assertNotIn(b", ", blob)

    def test_promote_output_is_the_pinned_sha(self):
        self.assertEqual(P.sha256_bytes(P.serialize(self.post())), OUTPUT_SHA)


class EntryPoint(Base):
    def _run(self, blob):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "canonical.json")
            with open(path, "wb") as f:
                f.write(blob)
            return subprocess.run([sys.executable, os.path.join(HERE, "promote_pla450_option_b_scoped_ids.py"),
                                   "--check", path], capture_output=True, text=True)

    def test_main_runs_the_whole_promote_against_the_fixture(self):
        r = self._run(promote_fixture.pre_state(P.BASE_SHA))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for expected in ("spec shape", "pre-state", "variety refs (pre)", "registry", "vacated",
                         "within-crop unique", "variety refs (post)", "collision prediction",
                         "verify post", OUTPUT_SHA, "nothing written"):
            self.assertIn(expected, r.stdout)

    def test_main_refuses_a_moved_base(self):
        d = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        d["version"] = "tampered"
        r = self._run(P.serialize(d))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("base SHA mismatch", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
