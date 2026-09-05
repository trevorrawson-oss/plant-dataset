#!/usr/bin/env python3
"""Guard suite for promote_pla8_batch27 -- PLA-8 batch 27, the microgreens.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE, never read from live canonical: the moment this
promote lands, a live read fails on a base mismatch and the suite goes permanently red (or, worse,
silently vacuous). `promote_fixture.pre_state` hash-verifies every reconstruction.

SHIPS MUTATION-TESTED (PLA-215). The companion `mutate_pla8_batch27_suite.py` injects one mutation
per guard family, carries a MUTATION-APPLIED marker, a sentinel that must redden, and a positive
control, or it exits HARNESS DEAD.

THE REFUSAL SPECS. Four guards here are expected to stay GREEN on the real batch, because the batch
does not contain the thing they refuse: `no_material_rungs`, `no_root_hair_claim`,
`no_sulfur_oil_interval`, and the `check_pre_state_schema` name-key clause. A refusal spec's green
is a PASS, not vacuity -- but only because the mutation suite proves each one reddens when the
refused thing is injected. Do not delete them for being quiet.
"""
import copy
import difflib
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import promote_fixture  # noqa: E402
import promote_pla8_batch27 as P  # noqa: E402

# ---- PINNED, MEASURED on the passing run. Re-measure on a canonical move; never retune to match.
BASE_SHA = "ba61762a21e52bad85ec1ddca98a92b34e6216d8258497325ec8b0630787beb3"
N_CROPS = 7
N_PROBLEMS = 14           # 7 crops x 2, and every one of them was unladdered before this batch
N_RUNGS = 43
N_REGISTER_STRINGS = 85   # 43 rungs, all but one carrying both notes
N_REGISTER_PAIRS = 42     # sunflower's airflow_spacing rung is beginner-only, as the precedent's is
N_IDS = 2                 # fungus-gnats, damping-off -- BOTH REUSED, zero minted
N_LEAVES = 42             # 14 entries x 3 added keys (id, type, control_ladder)
CROPS = ("arugula-microgreens", "broccoli-microgreens", "cilantro-microgreens", "pea-shoots",
         "radish-microgreens", "sunflower-sprouts", "wheatgrass")
# The one ladder that spans two tiers. Without it the tier-inversion test is vacuous, so it is
# pinned by name: cilantro is the only crop whose own prose asserts sticky cards.
MULTI_TIER = ("cilantro-microgreens", "pests", "fungus-gnats")

# PINNED, MEASURED literals: arugula's and broccoli's fungus-gnat management_seasoned. difflib's
# ratio reads 0.288 one way and 0.828 the other, a gap of 0.540. Pinned as literals rather than
# read from the fixture, because an expectation COMPUTED from the thing it validates is vacuous.
ASYM_A = ("Let the surface dry between waterings where the crop allows, bottom-water once greened, "
          "and keep airflow up. Because the arugula cycle is so short, most trays are harvested "
          "before gnats build to a real problem; sanitized trays and fresh medium between cycles "
          "break the cycle.")
ASYM_B = ("Let the surface dry between waterings where the crop allows, bottom-water, and keep "
          "airflow up. Because broccoli finishes in about 8 to 12 days, most trays are cut before "
          "gnats build to a real problem; sanitized trays and fresh medium between cycles break "
          "the cycle.")


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.pins, cls.batch = P.staged()
        cls.cm = cls.data["control_methods"]

    def fresh(self):
        return copy.deepcopy(self.batch)

    def fresh_pins(self):
        return copy.deepcopy(self.pins)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def assertRefuses(self, fragment, fn, *a, **kw):
        """The fragment must be unique to ONE guard. Asserting a SHARED fragment lets a mutation
        survive by tripping a different guard, which happened three times in one session."""
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg,
                      f"guard fired but with the wrong message.\n  wanted fragment: {fragment!r}\n"
                      f"  got: {msg!r}")

    def a_rung(self, b, crop=None):
        """First rung of the first entry, for mutating."""
        crop = crop or CROPS[0]
        return b[crop]["diseases"][0]["control_ladder"][0]


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(promote_fixture.pre_state(P.BASE_SHA)), BASE_SHA)

    def test_fixture_is_not_live_canonical_by_accident(self):
        """If canonical still happens to equal the base, a live read would pass and hide the bug
        this fixture exists to prevent. Assert the fixture came from the FIXTURE."""
        rebuilt = promote_fixture.pre_state(P.BASE_SHA)
        self.assertEqual(P.sha256_bytes(rebuilt), BASE_SHA)
        self.assertEqual(len(json.loads(rebuilt)["crops"]), 128)

    def test_the_batch_is_the_shape_measured(self):
        self.assertEqual(len(self.batch), N_CROPS)
        self.assertEqual(tuple(sorted(self.batch)), tuple(sorted(CROPS)))
        n_probs = sum(len(self.batch[c][f]) for c in CROPS for f in ("pests", "diseases"))
        self.assertEqual(n_probs, N_PROBLEMS)
        n_rungs = sum(len(e["control_ladder"]) for c in CROPS for f in ("pests", "diseases")
                      for e in self.batch[c][f])
        self.assertEqual(n_rungs, N_RUNGS)
        self.assertEqual(sum(1 for _ in P.notes(self.batch)), N_REGISTER_STRINGS)

    def test_multi_tier_ladder_exists_so_inversion_is_not_vacuous(self):
        crop, field, pid = MULTI_TIER
        e = next(x for x in self.batch[crop][field] if x["id"] == pid)
        tiers = {P.TIER_RANK[self.cm[r["method"]]["tier"]] for r in e["control_ladder"]}
        self.assertGreaterEqual(len(tiers), 2,
                                "the only two-tier ladder lost its second tier; the inversion "
                                "test below would silently stop testing anything")


class PreStateSchema(Base):
    """Rule 1. The schema this promote joins on is PINNED, not assumed."""

    def test_pre_state_is_the_microgreens_schema(self):
        self.assertEqual(P.check_pre_state_schema(self.pins, self.data), N_PROBLEMS)

    def test_every_target_entry_really_lacks_the_keys_we_add(self):
        """The batch's premise. If any entry already carried an id, the promote would overwrite a
        join key -- the single worst thing a ladder batch can do."""
        idx = P.by_slug(self.data)
        for crop in CROPS:
            for field in ("pests", "diseases"):
                for e in idx[crop][field]:
                    self.assertNotIn("name", e)
                    self.assertNotIn("id", e)
                    self.assertNotIn("type", e)
                    self.assertNotIn("control_ladder", e)
                    self.assertTrue(e["name_seasoned"])

    def test_refuses_when_a_name_key_appears(self):
        """REFUSAL SPEC. If PLA-452 normalizes the schema, this promote must refuse rather than
        join on a key that no longer carries the identity."""
        d = self.fresh_data()
        P.by_slug(d)["wheatgrass"]["diseases"][0]["name"] = "Mold and damping-off"
        self.assertRefuses("the schema has changed", P.check_pre_state_schema, self.pins, d)

    def test_refuses_when_an_entry_already_has_an_id(self):
        d = self.fresh_data()
        P.by_slug(d)["wheatgrass"]["diseases"][0]["id"] = "already-here"
        self.assertRefuses("would overwrite it", P.check_pre_state_schema, self.pins, d)

    def test_refuses_a_name_seasoned_drift(self):
        d = self.fresh_data()
        P.by_slug(d)["wheatgrass"]["diseases"][0]["name_seasoned"] = "Something else"
        self.assertRefuses("!= pinned", P.check_pre_state_schema, self.pins, d)


class IdsAreReused(Base):
    """Rule 2. This batch mints NOTHING, and that claim is guarded."""

    def test_both_ids_already_exist_outside_the_batch(self):
        ids, outside = P.check_ids_are_reused(self.pins, self.data)
        self.assertEqual(len(ids), N_IDS)
        self.assertEqual(ids, {"fungus-gnats", "damping-off"})
        for pid in ids:
            self.assertIn(P.PRECEDENT, outside[pid])

    def test_damping_off_is_the_roster_wide_id_not_a_microgreen_one(self):
        """A crop-scoped mint would have been the wrong call: 14 crops already carry this id for
        the same seedling complex."""
        _, outside = P.check_ids_are_reused(self.pins, self.data)
        self.assertGreaterEqual(len(outside["damping-off"]), 10)

    def test_refuses_a_minted_id(self):
        """REFUSAL SPEC, and the whole reason PLA-449 exists. A crop-scoped mint that no other crop
        carries must be refused here, because the collision guard runs at pinning time and this is
        the belt to its braces."""
        pins = self.fresh_pins()
        pins["wheatgrass"]["diseases"][0]["id"] = "damping-off-microgreens"
        self.assertRefuses("does not exist outside this batch",
                           P.check_ids_are_reused, pins, self.data)

    def test_refuses_an_id_the_precedent_does_not_carry(self):
        pins = self.fresh_pins()
        pins["wheatgrass"]["diseases"][0]["id"] = "gray-mold"   # real elsewhere, not on the precedent
        self.assertRefuses("is not carried by the precedent",
                           P.check_ids_are_reused, pins, self.data)


class Ladders(Base):
    def test_ladders_are_valid(self):
        self.assertEqual(P.check_ladders(self.batch, self.cm), N_RUNGS)

    def test_refuses_an_unknown_method(self):
        b = self.fresh()
        self.a_rung(b)["method"] = "tray_sanitation"   # the key the bots wished existed
        self.assertRefuses("names unknown method", P.check_ladders, b, self.cm)

    def test_refuses_a_tier_inversion(self):
        b = self.fresh()
        crop, field, pid = MULTI_TIER
        e = next(x for x in b[crop][field] if x["id"] == pid)
        e["control_ladder"].reverse()
        self.assertRefuses("is not softest-first", P.check_ladders, b, self.cm)

    def test_refuses_an_applies_to_mismatch(self):
        """airflow_spacing on an insect is the DELIBERATE refusal this arc already ruled."""
        b = self.fresh()
        b["wheatgrass"]["pests"][0]["control_ladder"].append(
            {"method": "airflow_spacing", "note_beginner": "x", "note_seasoned": "y"})
        self.assertRefuses("does not fit", P.check_ladders, b, self.cm)

    def test_refuses_an_empty_ladder(self):
        """`[]` is not `None`. An empty ladder passed every gate once."""
        b = self.fresh()
        b["wheatgrass"]["pests"][0]["control_ladder"] = []
        self.assertRefuses("empty or missing ladder", P.check_ladders, b, self.cm)

    def test_refuses_a_repeated_method(self):
        b = self.fresh()
        lad = b["wheatgrass"]["pests"][0]["control_ladder"]
        lad.append(copy.deepcopy(lad[0]))
        self.assertRefuses("repeats method", P.check_ladders, b, self.cm)


class SafetyRefusals(Base):
    """Rule 4 and rule 5. Both are REFUSAL SPECS: green on the real batch, red under injection."""

    def test_no_material_rungs_in_the_batch(self):
        self.assertEqual(P.check_no_material_rungs(self.batch, self.cm), N_RUNGS)

    def test_refuses_a_soft_chemical_rung(self):
        """The batch's central safety claim: nothing above physical ships on a crop cut at
        cotyledon stage and eaten raw, because no PHI has been ruled for a 7 to 28 day crop."""
        b = self.fresh()
        soft = next(k for k, m in self.cm.items()
                    if P.TIER_RANK[m["tier"]] > P.TIER_RANK["physical"]
                    and ("any" in (m.get("applies_to") or [])
                         or set(m.get("applies_to") or []) & P.TYPE_TARGETS["fungal"]))
        b["wheatgrass"]["diseases"][0]["control_ladder"].append(
            {"method": soft, "note_beginner": "x", "note_seasoned": "y"})
        self.assertRefuses("needs a pre-harvest-interval ruling",
                           P.check_no_material_rungs, b, self.cm)

    def test_no_root_hair_claim_in_the_batch(self):
        self.assertTrue(P.check_no_root_hair_claim(self.batch))

    def test_refuses_the_root_hair_claim(self):
        """Unsourced against psu_microgreens, which is these entries' only cited source."""
        b = self.fresh()
        self.a_rung(b)["note_beginner"] = (
            "The white fuzz at the base is usually root hairs rather than mold.")
        self.assertRefuses("states the root-hair claim", P.check_no_root_hair_claim, b)

    def test_pla457_is_held(self):
        self.assertGreater(P.check_no_sulfur_oil_interval(self.batch), 0)

    def test_refuses_a_sulfur_oil_interval(self):
        b = self.fresh()
        self.a_rung(b)["note_seasoned"] = (
            "Keep sulfur and oil sprays two weeks apart on this crop.")
        self.assertRefuses("states a sulfur/oil interval", P.check_no_sulfur_oil_interval, b)


class CopyGuards(Base):
    def test_nothing_is_lifted(self):
        self.assertEqual(P.check_no_precedent_copy(self.batch, self.data), N_REGISTER_STRINGS)

    def test_refuses_a_short_run_lifted_from_the_crops_own_prose(self):
        """THE N-GRAM ARM, isolated. A short borrowed run buried in otherwise original text keeps
        the ratio far below threshold, so only the run check can see it. That is the case a ratio
        check alone missed once: a 72-char lift scored 0.59."""
        b = self.fresh()
        src = P.by_slug(self.data)["wheatgrass"]["diseases"][0]["management_beginner"]
        run = " ".join(src.split()[:8])
        note = ("Cut the tray early if you must, but " + run +
                " when judging how the crop is coming along day to day.")
        r = self.a_rung(b, "wheatgrass")
        r["note_beginner"] = note
        self.assertLess(max(P._sym(note, d) for _, d in P._donor_prose(self.data)),
                        P.COPY_THRESHOLD,
                        "this injection must NOT trip the ratio arm, or it stops isolating the "
                        "n-gram arm and the mutation below would be graded by the wrong guard")
        self.assertRefuses("shares a", P.check_no_precedent_copy, b, self.data)

    def test_refuses_a_lift_from_the_precedent_ladder(self):
        """THE RATIO ARM, isolated. microgreens-mix is a SHAPE exemplar, not a donor: three notes
        had to be rewritten for exactly this in the authoring pass, and a fourth was a 0.776
        recombination of TWO precedent rungs with no shared run at all."""
        b = self.fresh()
        donor = P.by_slug(self.data)[P.PRECEDENT]["diseases"][0]["control_ladder"][0]["note_beginner"]
        self.a_rung(b)["note_beginner"] = donor
        self.assertRefuses("similar to", P.check_no_precedent_copy, b, self.data)

    def test_figure_runs_are_exempt(self):
        """A guard can refuse CORRECT input. A number has no honest paraphrase, so a shared run
        carrying one is exempt -- and the exemption must be narrow enough that prose still fails."""
        self.assertTrue(P._is_figure_run("7 to 10 day grow out"))
        self.assertFalse(P._is_figure_run("let the surface dry between waterings"))

    def test_similarity_takes_the_max_of_both_orders(self):
        """difflib's ratio is ASYMMETRIC, and on this pair the gap is 0.54.

        THE FIRST VERSION OF THIS TEST WAS VACUOUS: it used a synthetic pair that happened to be
        symmetric, so dropping the max() changed nothing and the mutation SURVIVED. The harness
        caught it, which is the entire reason the harness exists. The pair below is the real
        arugula/broccoli gnat prose, and it is chosen because a one-order check would MISS it:
        one direction reads 0.29 and sails under the 0.70 threshold while the reverse reads 0.83
        and is plainly a near-copy."""
        lo = difflib.SequenceMatcher(None, ASYM_A, ASYM_B).ratio()
        hi = difflib.SequenceMatcher(None, ASYM_B, ASYM_A).ratio()
        self.assertGreater(abs(hi - lo), 0.4,
                           "the pinned pair stopped being asymmetric, so this test can no longer "
                           "tell a both-orders guard from a one-order one")
        self.assertLess(lo, P.COPY_THRESHOLD,
                        "a one-order guard must MISS this pair, or the mutation is undetectable")
        self.assertGreater(hi, P.COPY_THRESHOLD)
        self.assertAlmostEqual(P._sym(ASYM_A, ASYM_B), hi)
        self.assertAlmostEqual(P._sym(ASYM_B, ASYM_A), hi)

    def test_no_intra_batch_twins(self):
        self.assertEqual(P.check_no_intra_batch_twins(self.batch), N_REGISTER_STRINGS)

    def test_refuses_a_propagated_note(self):
        """Seven crops with 0% identical source prose must not emerge with one crop's sentence."""
        b = self.fresh()
        donor = b["arugula-microgreens"]["diseases"][0]["control_ladder"][0]["note_beginner"]
        b["wheatgrass"]["diseases"][0]["control_ladder"][0]["note_beginner"] = donor
        self.assertRefuses("these are separate authoring passes", P.check_no_intra_batch_twins, b)


class Registers(Base):
    def test_registers_diverge(self):
        self.assertGreater(P.check_registers_diverge(self.batch), 0)

    def test_refuses_identical_registers(self):
        b = self.fresh()
        r = self.a_rung(b)
        r["note_seasoned"] = r["note_beginner"]
        self.assertRefuses("registers are identical", P.check_registers_diverge, b)

    def test_refuses_a_reworded_register(self):
        b = self.fresh()
        r = self.a_rung(b)
        r["note_seasoned"] = r["note_beginner"].replace("the", "a", 1) + " "
        self.assertRefuses("that is a reword", P.check_registers_diverge, b)


class Hygiene(Base):
    def test_copy_hygiene(self):
        self.assertTrue(P.check_copy_hygiene(self.batch))

    def test_refuses_an_em_dash(self):
        b = self.fresh()
        self.a_rung(b)["note_beginner"] = "Keep the tray damp — not soggy."
        self.assertRefuses("em or en dash", P.check_copy_hygiene, b)

    def test_refuses_an_absolute(self):
        b = self.fresh()
        self.a_rung(b)["note_beginner"] = "Clean trays will always stop this problem."
        self.assertRefuses("contains an absolute", P.check_copy_hygiene, b)

    def test_refuses_ladder_vocabulary(self):
        b = self.fresh()
        self.a_rung(b)["note_beginner"] = "Move to the next rung when this stops working."
        self.assertRefuses("names the ladder machinery", P.check_copy_hygiene, b)

    def test_refuses_a_spaced_degree(self):
        b = self.fresh()
        self.a_rung(b)["note_beginner"] = "Hold the room near 70 °F for even germination."
        self.assertRefuses("spaced degree symbol", P.check_copy_hygiene, b)


class ApplyAndVerify(Base):
    def test_apply_is_purely_additive(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        self.assertEqual(P.verify_post(self.data, post, self.pins, self.batch), N_LEAVES)

    def test_set_comparison_runs_before_value_comparison(self):
        """PLA-162: iterating `pre` alone makes everything ADDED in `post` invisible."""
        post = P.apply_to(self.data, self.pins, self.batch)
        P.by_slug(post)["wheatgrass"]["diseases"][0]["severity"] = "high"
        self.assertRefuses("added", P.verify_post, self.data, post, self.pins, self.batch)

    def test_refuses_a_touched_prose_field(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        P.by_slug(post)["wheatgrass"]["diseases"][0]["description_beginner"] = "rewritten"
        self.assertRefuses("carried field", P.verify_post, self.data, post, self.pins, self.batch)

    def test_refuses_a_touched_untouched_crop(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        P.by_slug(post)["tomatillo"]["diseases"][0]["id"] = "tampered"
        self.assertRefuses("untouched crop", P.verify_post, self.data, post, self.pins, self.batch)

    def test_refuses_a_touched_top_level_key(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        post["control_methods"]["garden_sanitation"]["tier"] = "physical"
        self.assertRefuses("top-level key", P.verify_post, self.data, post, self.pins, self.batch)

    def test_refuses_a_roster_change(self):
        """PLA-162 shipped a clone of `lime` appended as `ghost-crop` past four green guards."""
        post = P.apply_to(self.data, self.pins, self.batch)
        ghost = copy.deepcopy(P.by_slug(post)["wheatgrass"])
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        self.assertRefuses("roster changed", P.verify_post, self.data, post, self.pins, self.batch)

    def test_refuses_a_ladder_that_does_not_match_the_authored_output(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        P.by_slug(post)["wheatgrass"]["diseases"][0]["control_ladder"][0]["note_beginner"] = "x"
        self.assertRefuses("does not match the", P.verify_post,
                           self.data, post, self.pins, self.batch)

    def test_untouched_crops_are_byte_identical(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        pre_i, post_i = P.by_slug(self.data), P.by_slug(post)
        n = 0
        for slug in pre_i:
            if slug in CROPS:
                continue
            self.assertEqual(json.dumps(pre_i[slug], sort_keys=True),
                             json.dumps(post_i[slug], sort_keys=True))
            n += 1
        self.assertEqual(n, 128 - N_CROPS)

    def test_the_seven_gain_exactly_three_keys_each(self):
        post = P.apply_to(self.data, self.pins, self.batch)
        pre_i, post_i = P.by_slug(self.data), P.by_slug(post)
        for crop in CROPS:
            for field in ("pests", "diseases"):
                for s, g in zip(pre_i[crop][field], post_i[crop][field]):
                    self.assertEqual(set(g) - set(s), set(P.PINNED_FIELDS))
                    self.assertEqual(set(s) - set(g), set())


class Serializer(Base):
    def test_one_serializer_shared_with_the_suite(self):
        """A suite doing its own json.dumps grades itself and an indent mutation survives."""
        blob = P.serialize({"a": "é", "b": 1})
        self.assertEqual(blob, b'{"a":"\xc3\xa9","b":1}')
        self.assertNotIn(b"\n", blob)
        self.assertNotIn(b", ", blob)

    def test_promote_output_is_deterministic(self):
        a = P.serialize(P.apply_to(self.data, self.pins, self.batch))
        b = P.serialize(P.apply_to(self.data, self.pins, self.batch))
        self.assertEqual(P.sha256_bytes(a), P.sha256_bytes(b))


class EntryPoint(Base):
    """REACH THE ENTRY POINT. Batch 23 shipped 53 green tests while main() never called check()."""

    def test_main_runs_the_whole_promote_against_the_fixture(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "canonical.json")
            with open(path, "wb") as f:
                f.write(promote_fixture.pre_state(P.BASE_SHA))
            r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla8_batch27.py"),
                                "--check", path],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            for expected in ("pre-state schema", "ids reused", "ladders", "no material rungs",
                             "no root-hair claim", "PLA-457 held", "verify post"):
                self.assertIn(expected, r.stdout)
            self.assertIn("nothing written", r.stdout)

    def test_main_refuses_a_moved_base(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "canonical.json")
            d = json.loads(promote_fixture.pre_state(P.BASE_SHA))
            d["version"] = "tampered"
            with open(path, "wb") as f:
                f.write(P.serialize(d))
            r = subprocess.run([sys.executable, os.path.join(HERE, "promote_pla8_batch27.py"),
                                "--check", path],
                               capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("base SHA mismatch", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
