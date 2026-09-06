#!/usr/bin/env python3
"""Guard suite for promote_pla450_451_problem_ids -- PLA-450 merges + PLA-451 celery split.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE, never read from live canonical: the moment this
promote lands, a live read fails on a base mismatch and the suite goes permanently red (or, worse,
silently vacuous). `promote_fixture.pre_state` hash-verifies every reconstruction.

SHIPS MUTATION-TESTED (PLA-215). The companion `mutate_pla450_451_problem_ids_suite.py` injects one
mutation per guard family, carries a MUTATION-APPLIED marker, a sentinel that must redden, and a
positive control, or it exits HARNESS DEAD.

THE REFUSAL SPECS. Three guards here stay GREEN on the real spec because the spec does not contain
the thing they refuse: `check_held_pairs` (no row merges a taxon-refuted pair), the retired-id arm
of `check_variety_refs` (none of the 129 references sits on a merged id), and the stale-registry
arm of `check_registry`. Each one's green is a PASS only because the drivers below prove it reddens
under injection. Do not delete them for being quiet.

THE PREDICTION IS PINNED TWICE. The promote carries PREDICTED as a constant and refuses on any
other post-state figure; this suite pins the SAME literals independently, so retuning the promote's
constant to match a surprise reddens here. A number that matches a prediction is evidence; a
constant edited after the fact is not.
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
import promote_pla450_451_problem_ids as P  # noqa: E402
import problem_id_collision_gate as G  # noqa: E402

# ---- PINNED, MEASURED on the passing run. Re-measure on a canonical move; never retune to match.
BASE_SHA = "95e66f6d1a8ea8550b2df3825d3bcbb00d39056e106d037290737923f74d0879"
OUTPUT_SHA = "36d6df6bf3bdd2cac37dc568742c37655d1a739b20c9991285bd9608463925fd"
ROSTER = 128
N_ROWS = 9
N_MERGES = 7             # six decisions; the slug decision retires two minority ids
N_MINTS = 2
N_LEAVES = 9
N_VARIETY_REFS = 129     # apple 102, strawberry 22, asparagus 5 -- none on a touched id
N_HELD = 2
N_TOUCHED_IDS = 48       # distinct ids across the six touched crops after the rewrite
CROPS = ("artichoke", "asparagus", "basil", "celery", "strawberry", "swiss-chard")
PREDICTED_BASELINE = {"raw": 42, "registered": 20, "actionable": 22}
PREDICTED = {"raw": 36, "registered": 22, "actionable": 14}


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

    def row(self, spec, crop, name):
        return next(r for r in spec["rows"] if r["crop"] == crop and r["name"] == name)

    def entry(self, data, crop, field, name):
        return next(e for e in P.by_slug(data)[crop][field] if e.get("name") == name)

    def assertRefuses(self, fragment, fn, *a, **kw):
        """The fragment must be unique to ONE guard. Asserting a SHARED fragment lets a mutation
        survive by tripping a different guard."""
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
        rebuilt = promote_fixture.pre_state(P.BASE_SHA)
        self.assertEqual(P.sha256_bytes(rebuilt), BASE_SHA)
        self.assertEqual(len(json.loads(rebuilt)["crops"]), ROSTER)

    def test_the_spec_is_the_shape_measured(self):
        rows = P.rows(self.spec)
        self.assertEqual(len(rows), N_ROWS)
        self.assertEqual(sum(1 for r in rows if r["kind"] == "merge"), N_MERGES)
        self.assertEqual(sum(1 for r in rows if r["kind"] == "mint"), N_MINTS)
        self.assertEqual(tuple(sorted({r["crop"] for r in rows})), tuple(sorted(CROPS)))
        self.assertEqual(tuple(sorted(P.CROPS)), tuple(sorted(CROPS)))

    def test_prediction_constants_are_the_pinned_literals(self):
        """Pinned HERE as literals so a retune in the promote reddens. The promote refuses on a
        figure that differs from PREDICTED; this test refuses PREDICTED being edited to match."""
        self.assertEqual(P.PREDICTED, PREDICTED)
        self.assertEqual(P.PREDICTED_BASELINE, PREDICTED_BASELINE)

    def test_held_pairs_are_the_two_taxon_refuted_ones(self):
        self.assertEqual(len(P.HELD), N_HELD)
        self.assertIn(frozenset(("bacterial-leaf-spot", "bacterial-spot")), P.HELD)
        self.assertIn(frozenset(("bacterial-blight", "bacterial-blights")), P.HELD)
        for reason in P.HELD.values():
            self.assertIn("Pseudomonas", reason)
            self.assertIn("Xanthomonas", reason)


class SpecShape(Base):
    def test_spec_shape_passes(self):
        self.assertEqual(P.check_spec_shape(self.spec), N_ROWS)

    def test_refuses_a_self_rewrite(self):
        s = self.fresh_spec()
        self.row(s, "asparagus", "Cutworms")["to"] = "cutworm"
        self.assertRefuses("rewrites an id to itself", P.check_spec_shape, s)

    def test_refuses_the_same_entry_named_twice(self):
        s = self.fresh_spec()
        s["rows"].append(copy.deepcopy(self.row(s, "asparagus", "Cutworms")))
        self.assertRefuses("names the same entry twice", P.check_spec_shape, s)

    def test_refuses_an_undeclared_crop(self):
        s = self.fresh_spec()
        self.row(s, "asparagus", "Cutworms")["crop"] = "tomatillo"
        self.assertRefuses("which is not a declared crop", P.check_spec_shape, s)

    def test_refuses_a_declared_crop_with_no_row(self):
        s = self.fresh_spec()
        s["rows"] = [r for r in s["rows"] if r["crop"] != "basil"]
        self.assertRefuses("have no spec row", P.check_spec_shape, s)

    def test_refuses_a_mint_set_other_than_the_two_celery_ids(self):
        s = self.fresh_spec()
        self.row(s, "celery", "Early blight (Cercospora leaf spot)")["to"] = "apium-early-blight"
        self.assertRefuses("expected exactly", P.check_spec_shape, s)


class HeldPairs(Base):
    """Rule 1, a REFUSAL SPEC: green on the real spec, red under injection, in both directions."""

    def test_no_row_merges_a_held_pair(self):
        self.assertEqual(P.check_held_pairs(self.spec), N_HELD)

    def test_refuses_the_cilantro_pepper_merge(self):
        s = self.fresh_spec()
        s["rows"].append({"kind": "merge", "crop": "cilantro-coriander", "field": "diseases",
                          "name": "Bacterial leaf spot", "from": "bacterial-leaf-spot",
                          "to": "bacterial-spot"})
        self.assertRefuses("taxon-refuted pair", P.check_held_pairs, s)

    def test_refuses_the_bean_edamame_merge_in_either_direction(self):
        s = self.fresh_spec()
        s["rows"].append({"kind": "merge", "crop": "edamame", "field": "diseases",
                          "name": "Bacterial blight", "from": "bacterial-blight",
                          "to": "bacterial-blights"})
        self.assertRefuses("taxon-refuted pair", P.check_held_pairs, s)
        s = self.fresh_spec()
        s["rows"].append({"kind": "merge", "crop": "dry-bean", "field": "diseases",
                          "name": "Bacterial blights (common and halo)", "from": "bacterial-blights",
                          "to": "bacterial-blight"})
        self.assertRefuses("taxon-refuted pair", P.check_held_pairs, s)


class PreState(Base):
    def test_pre_state_passes(self):
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_ROWS)

    def test_refuses_a_missing_target(self):
        d = self.fresh_data()
        self.entry(d, "asparagus", "pests", "Cutworms")["name"] = "Cutworm larvae"
        self.assertRefuses("need exactly 1", P.check_pre_state, self.spec, d)

    def test_refuses_an_id_drift(self):
        d = self.fresh_data()
        self.entry(d, "asparagus", "pests", "Cutworms")["id"] = "already-moved"
        self.assertRefuses("the pre-state has drifted", P.check_pre_state, self.spec, d)

    def test_refuses_a_target_with_no_ladder(self):
        """A57's concern, pre-side: an id rewrite must not be how an unladdered entry gets past."""
        d = self.fresh_data()
        self.entry(d, "strawberry", "pests", "Slugs")["control_ladder"] = []
        self.assertRefuses("has no ladder in the pre-state", P.check_pre_state, self.spec, d)


class Direction(Base):
    def test_direction_passes(self):
        self.assertEqual(P.check_direction(self.spec, self.data), N_ROWS)

    def test_refuses_a_merge_pointing_at_the_minority(self):
        s = self.fresh_spec()
        r = self.row(s, "asparagus", "Cutworms")
        r["from"], r["to"] = r["to"], r["from"]
        self.assertRefuses("points at the minority", P.check_direction, s, self.data)

    def test_refuses_a_merge_onto_an_id_the_crop_already_holds(self):
        s = self.fresh_spec()
        self.row(s, "artichoke", "Gray mold (Botrytis cinerea)")["to"] = "cutworms"
        self.assertRefuses("would create a within-crop duplicate id", P.check_direction, s, self.data)

    def test_refuses_a_mint_that_already_exists(self):
        s = self.fresh_spec()
        self.row(s, "celery", "Early blight (Cercospora leaf spot)")["to"] = "gray-mold"
        self.assertRefuses("a mint must be new", P.check_direction, s, self.data)

    def test_refuses_a_mint_that_would_empty_the_generic_id(self):
        s = self.fresh_spec()
        self.row(s, "celery", "Early blight (Cercospora leaf spot)")["from"] = "celery-leafminer"
        self.assertRefuses("that is a rename, not a split", P.check_direction, s, self.data)


class VarietyRefs(Base):
    """Rule 3. The join surface, on both states."""

    def setUp(self):
        self.retired = {r["from"] for r in P.rows(self.spec) if r["kind"] == "merge"}

    def test_all_refs_resolve_pre_and_post(self):
        self.assertEqual(P.check_variety_refs(self.data, self.retired), N_VARIETY_REFS)
        self.assertEqual(P.check_variety_refs(self.post(), self.retired), N_VARIETY_REFS)

    def test_the_129_refs_sit_on_ids_this_promote_never_touches(self):
        touched = {r["from"] for r in P.rows(self.spec)} | {r["to"] for r in P.rows(self.spec)}
        hit = [(s, v, jf, pid) for s, v, jf, pid in P.variety_refs(self.data) if pid in touched]
        self.assertEqual(hit, [])

    def test_refuses_a_dangling_reference(self):
        d = self.fresh_data()
        v = P.by_slug(d)["apple"]["varieties"]["recommended"][0]
        v["resistance"]["nonexistent-problem"] = "resistant"
        self.assertRefuses("a dangling variety join", P.check_variety_refs, d, self.retired)

    def test_refuses_a_reference_on_a_retired_id(self):
        """REFUSAL SPEC. The reference resolves on the pre-state, so the resolve arm is silent
        and only the retired-id arm can see it."""
        d = self.fresh_data()
        v = P.by_slug(d)["strawberry"]["varieties"]["recommended"][0]
        v.setdefault("resistance", {})["slugs"] = "tolerant"
        self.assertRefuses("an id this promote retires", P.check_variety_refs, d, self.retired)

    def test_refuses_a_vanished_join_surface(self):
        d = self.fresh_data()
        for c in d["crops"]:
            if isinstance(c.get("varieties"), dict):
                for x in c["varieties"].get("recommended") or []:
                    if isinstance(x, dict):
                        x.pop("resistance", None)
                        x.pop("ladder_delta", None)
        self.assertRefuses("found zero variety references", P.check_variety_refs, d, self.retired)


class PinnedRegistry(Base):
    def test_figures_are_read_from_the_pinned_commit_not_the_working_copy(self):
        """ADDED 2026-09-06 after PLA-450 Option B repointed a registry entry and this suite went red
        in four places while replaying unchanged states. The pin must be a commit, never HEAD."""
        self.assertEqual(P.REGISTRY_COMMIT, "c189d65")
        self.assertNotEqual(P.REGISTRY_COMMIT.upper(), "HEAD")
        self.assertEqual(P.collision_figures(self.data), PREDICTED_BASELINE)


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
        self.assertEqual(P.check_registry(self.spec), N_MINTS)

    def test_refuses_a_missing_adjudication(self):
        path = self._with_registry(lambda entries: entries[:] and entries.__setitem__(
            slice(None), [e for e in entries if "celery-late-blight" not in e["ids"]]))
        self.assertRefuses("is not adjudicated where the gate reads it", self._run_with, path)

    def test_refuses_a_reason_that_does_not_name_both_organisms(self):
        def mutate(entries):
            for e in entries:
                if "celery-early-blight" in e["ids"]:
                    e["reason"] = e["reason"].replace("Alternaria", "another fungus")
        self.assertRefuses("an adjudication names both organisms",
                           self._run_with, self._with_registry(mutate))

    def test_refuses_an_entry_naming_a_retired_id(self):
        """REFUSAL SPEC: the live registry names none of the seven retired ids."""
        def mutate(entries):
            entries.append({"ids": ["slugs", "slugs-and-snails"], "reason": "x", "ruled": "x"})
        self.assertRefuses("a stale record", self._run_with, self._with_registry(mutate))


class ApplyAndRetirement(Base):
    def test_retirement_is_complete(self):
        self.assertEqual(P.check_retirement_complete(self.post(), self.spec), N_MERGES)

    def test_refuses_a_straggler(self):
        post = self.post()
        self.entry(post, "strawberry", "pests", "Slugs")["id"] = "slugs"
        self.assertRefuses("left a straggler", P.check_retirement_complete, post, self.spec)

    def test_refuses_a_split_that_emptied_the_generic_id(self):
        post = self.post()
        for c in post["crops"]:
            for _, e in P.problems(c):
                if e.get("id") == "early-blight":
                    e["id"] = "early-blight-renamed"
        self.assertRefuses("vanished after the split", P.check_retirement_complete, post, self.spec)

    def test_refuses_a_crop_still_on_the_generic_id_after_minting(self):
        post = self.post()
        self.entry(post, "celery", "diseases", "Early blight (Cercospora leaf spot)")["id"] = "early-blight"
        self.assertRefuses("after minting", P.check_retirement_complete, post, self.spec)

    def test_within_crop_unique_passes(self):
        self.assertEqual(P.check_within_crop_unique(self.post()), N_TOUCHED_IDS)

    def test_refuses_a_within_crop_duplicate(self):
        post = self.post()
        self.entry(post, "artichoke", "pests", "Cutworms")["id"] = "gray-mold"
        self.assertRefuses("carries duplicate id(s)", P.check_within_crop_unique, post)


class CollisionPrediction(Base):
    """Rule 4. The real gate, the real registry, a pinned prediction."""

    def test_baseline_is_what_the_prediction_rests_on(self):
        self.assertEqual(P.collision_figures(self.data), PREDICTED_BASELINE)

    def test_post_state_matches_the_prediction(self):
        self.assertEqual(P.check_collision_prediction(self.data, self.post()), PREDICTED)

    def test_the_eight_open_pairs_retire_and_the_two_celery_pairs_arrive_registered(self):
        """The prediction's mechanism, asserted pair by pair rather than as a total."""
        pre = {f.pair: f for f in G.scan(self.data, registry=P.pinned_registry())}
        post = {f.pair: f for f in G.scan(self.post(), registry=P.pinned_registry())}
        gone = set(pre) - set(post)
        new = set(post) - set(pre)
        self.assertEqual(gone, {
            ("cutworm", "cutworms"), ("flea-beetle", "flea-beetles"),
            ("japanese-beetle", "japanese-beetles"), ("botrytis-gray-mold", "gray-mold"),
            ("two-spotted-spider-mite", "twospotted-spider-mite"),
            ("slugs", "slugs-and-snails"), ("slugs", "snails-and-slugs"),
            ("slugs-and-snails", "snails-and-slugs")})
        self.assertTrue(all(not pre[p].registered for p in gone), "a retired pair was registered")
        self.assertEqual(new, {("celery-early-blight", "early-blight"),
                               ("celery-late-blight", "late-blight")})
        self.assertTrue(all(post[p].registered for p in new), "a celery pair arrived OPEN")
        self.assertTrue(all(G.NAME_SHARED in post[p].kinds for p in new))

    def test_the_two_held_pairs_stay_open(self):
        post = {f.pair: f for f in G.scan(self.post(), registry=P.pinned_registry())}
        for pair in (("bacterial-leaf-spot", "bacterial-spot"), ("bacterial-blight", "bacterial-blights")):
            self.assertIn(pair, post)
            self.assertFalse(post[pair].registered, f"{pair} was quietly registered")

    def test_refuses_a_baseline_drift(self):
        pre = self.fresh_data()
        self.entry(pre, "tomatillo", "diseases", "Early blight")["id"] = "early-blight-x"
        self.assertRefuses("re-derive the prediction before running",
                           P.check_collision_prediction, pre, self.post())

    def test_refuses_a_post_state_whose_figures_differ(self):
        post = self.post()
        self.entry(post, "asparagus", "pests", "Cutworms")["id"] = "cutworm"
        self.assertRefuses("!= PREDICTED", P.check_collision_prediction, self.data, post)


class VerifyPost(Base):
    def test_apply_changes_exactly_the_nine_id_leaves(self):
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec), N_LEAVES)

    def test_set_comparison_runs_before_value_comparison(self):
        """PLA-162: iterating `pre` alone makes everything ADDED in `post` invisible."""
        post = self.post()
        self.entry(post, "strawberry", "pests", "Slugs")["severity_note"] = "added"
        self.assertRefuses("entry key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_crop_level_addition(self):
        post = self.post()
        P.by_slug(post)["strawberry"]["ghost_field"] = 1
        self.assertRefuses("crop-level key set changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_touched_prose_field(self):
        post = self.post()
        self.entry(post, "strawberry", "pests", "Slugs")["symptoms_beginner"] = "rewritten"
        self.assertRefuses("rewrites ids and nothing else", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_lost_ladder(self):
        """A57's concern, post-side: a merge that drops a ladder."""
        post = self.post()
        self.entry(post, "artichoke", "diseases", "Gray mold (Botrytis cinerea)")["control_ladder"] = []
        self.assertRefuses("lost its ladder", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_dropped_entry(self):
        post = self.post()
        P.by_slug(post)["strawberry"]["pests"] = [
            e for e in P.by_slug(post)["strawberry"]["pests"] if e["name"] != "Slugs"]
        self.assertRefuses("entry count", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_entry_reorder(self):
        post = self.post()
        P.by_slug(post)["celery"]["diseases"].reverse()
        self.assertRefuses("entry order or name changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_id_change_without_a_spec_row(self):
        post = self.post()
        self.entry(post, "celery", "diseases", "Pink rot")["id"] = "celery-pink-rot"
        self.assertRefuses("without a spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_rewrite_not_matching_its_row(self):
        post = self.post()
        self.entry(post, "asparagus", "pests", "Cutworms")["id"] = "cutwormz"
        self.assertRefuses("does not match its spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_fewer_leaves_than_rows(self):
        """A target renamed identically in both states drops out of the row join; the count
        check is the only guard that can see it."""
        pre, post = self.fresh_data(), self.post()
        self.entry(pre, "asparagus", "pests", "Cutworms")["name"] = "Cutworm larvae"
        e = self.entry(post, "asparagus", "pests", "Cutworms")
        e["name"], e["id"] = "Cutworm larvae", "cutworm"
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
        """PLA-162 shipped a clone of `lime` appended as `ghost-crop` past four green guards."""
        post = self.post()
        ghost = copy.deepcopy(P.by_slug(post)["celery"])
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_untouched_crops_are_byte_identical(self):
        pre_i, post_i = P.by_slug(self.data), P.by_slug(self.post())
        n = 0
        for slug in pre_i:
            if slug in CROPS:
                continue
            self.assertEqual(json.dumps(pre_i[slug], sort_keys=True),
                             json.dumps(post_i[slug], sort_keys=True))
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
        """`post` is the promote's OWN output, replayed from the pinned base, never live canonical."""
        self.assertEqual(P.sha256_bytes(P.serialize(self.post())), OUTPUT_SHA)


class EntryPoint(Base):
    """REACH THE ENTRY POINT. Batch 23 shipped 53 green tests while main() never called check()."""

    def _run(self, blob):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "canonical.json")
            with open(path, "wb") as f:
                f.write(blob)
            return subprocess.run([sys.executable, os.path.join(HERE, "promote_pla450_451_problem_ids.py"),
                                   "--check", path], capture_output=True, text=True)

    def test_main_runs_the_whole_promote_against_the_fixture(self):
        r = self._run(promote_fixture.pre_state(P.BASE_SHA))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for expected in ("spec shape", "held pairs", "pre-state", "direction", "variety refs (pre)",
                         "registry", "retirement", "within-crop unique", "variety refs (post)",
                         "collision prediction", "verify post", OUTPUT_SHA, "nothing written"):
            self.assertIn(expected, r.stdout)

    def test_main_refuses_a_moved_base(self):
        d = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        d["version"] = "tampered"
        r = self._run(P.serialize(d))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("base SHA mismatch", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
