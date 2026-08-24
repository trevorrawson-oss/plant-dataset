#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch1.py. Base 0f911326.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_batch1_suite.py.

THE LOAD-BEARING FAMILY IS `ReadFixes`, and its hardest guard is `MergeEvidence`. Eight of the
eighteen fixes MERGE two rungs into one, and a merge is the easiest fix to fake: dropping the
`prune_out_infection` rung alone satisfies "no prune_out_infection survives" while silently deleting
half the advice. So each merged rung is checked to carry a distinctive phrase from BOTH original
rungs. Absence of the wrong key is never asserted on its own.

`StillOpen` is the second family and guards the opposite temptation. Four rungs are deliberately NOT
fixed, each because the method they need cannot be honestly minted yet. A promote that quietly
"closed" them by repointing to a near-miss method would look like a better result and be a worse
one, so the suite asserts they remain exactly as authored.

`StagingIntegrity` asserts the authored files on disk are never written back. The fixes are a delta
applied in memory; if the staging were mutated, the record of what the bots actually produced would
be gone and the fixes would no longer be reviewable against it.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch1 as P  # noqa: E402
import build_pla8_batch1_content as C  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

POST_SHA = "76c7048803a0c68d0924b062a40cfb3d8ffdbaf9a12e316a851f40c9b2255bd4"
STAGED_RUNGS = 165
PROMOTED_RUNGS = 159
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")

# For each merge: a phrase that can only have come from the garden_sanitation rung, and one that
# can only have come from the prune_out_infection rung. Both must survive in the merged note.
MERGE_EVIDENCE = {
    ("basil", "downy-mildew"): ("shedding spores onto its neighbors", "heavily infected stems"),
    ("swiss-chard", "cercospora-leaf-spot"): ("rake up", "worst-spotted leaves"),
    ("swiss-chard", "downy-mildew"): ("crop leftovers", "twisted, thickened"),
    ("heirloom-tomato", "early-blight"): ("compost pile", "spotted lower leaves"),
    ("heirloom-tomato", "septoria-leaf-spot"): ("compost pile", "spotted lower leaves"),
    ("heirloom-tomato", "late-blight"): ("before winter", "whole plant out"),
    ("jalapeno", "bacterial-spot"): ("hands and tools", "badly spotted"),
    ("jalapeno", "mosaic-viruses"): ("wash your hands", "stunted with mottled"),
}


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _prob(data, slug, pid):
    for c in data["crops"]:
        if c.get("slug") != slug:
            continue
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if isinstance(p, dict) and p.get("id") == pid:
                    return p
    return None


def _laddered(data):
    out = []
    for c in data["crops"]:
        if (c.get("verification_status") or {}).get("status") != "verified_gs_arc":
            continue
        if any("control_ladder" in p for fam in ("pests", "diseases")
               for p in (c.get(fam) or []) if isinstance(p, dict)):
            out.append(c["slug"])
    return sorted(out)


# --------------------------------------------------------------------------- fixture
class Fixture(unittest.TestCase):
    def test_base_reconstructs(self):
        self.assertEqual(
            hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(), P.BASE_SHA)

    def test_post_sha_pinned(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)

    def test_roster_goes_7_to_12(self):
        self.assertEqual(len(_laddered(_pre())), 7)
        post = _laddered(_post())
        self.assertEqual(len(post), 12)
        for s in P.CROPS:
            self.assertIn(s, post)


# --------------------------------------------------------------------------- staging
class StagingIntegrity(unittest.TestCase):
    def test_the_authored_files_are_never_written_back(self):
        before = {s: open(os.path.join(P.STAGING, f"out_{s}.json"), "rb").read() for s in P.CROPS}
        P.fixed_batch()
        _post()
        after = {s: open(os.path.join(P.STAGING, f"out_{s}.json"), "rb").read() for s in P.CROPS}
        self.assertEqual(before, after, "the staged batch was mutated on disk")

    def test_staged_rung_count(self):
        self.assertEqual(P.rung_count(P.staged()), STAGED_RUNGS)

    def test_fixed_batch_is_a_pure_function_of_staging(self):
        a = json.dumps(P.fixed_batch(), sort_keys=True)
        b = json.dumps(P.fixed_batch(), sort_keys=True)
        self.assertEqual(a, b)

    def test_rung_arithmetic(self):
        """165 - 8 merges - 1 merge-to + 3 splits = 159. Stated, not assumed."""
        self.assertEqual(
            STAGED_RUNGS - len(C.MERGES) - len(C.MERGE_TO) + len(C.SPLITS), PROMOTED_RUNGS)
        self.assertEqual(P.rung_count(P.fixed_batch()), PROMOTED_RUNGS)


# --------------------------------------------------------------------------- load-bearing 1
class ReadFixes(unittest.TestCase):
    def test_eighteen_fixes_are_declared(self):
        n = (len(C.MERGES) + len(C.MERGE_TO) + len(C.REPOINTS)
             + len(C.REPOINT_REWRITES) * 1 + len(C.SPLITS) + len(C.EDIT_NOTES))
        # merges 8 + merge_to 1(x2 rungs) + repoints 3 + rewrites 1 + splits 3 + edit 1 = 17 ops,
        # 18 RUNGS because the merge_to collapses two mismatched rungs at once.
        self.assertEqual(n, 17)
        self.assertEqual(C.EXPECTED_FIX_COUNT, 18)

    def test_no_prune_out_infection_survives_in_the_batch(self):
        b = P.fixed_batch()
        for crop in P.CROPS:
            for fam in ("pests", "diseases"):
                for p in b[crop].get(fam, []):
                    for r in p["control_ladder"]:
                        self.assertNotEqual(r["method"], "prune_out_infection",
                                            f"{crop}/{p['id']}")

    def test_prune_out_infection_stays_reachable_only_from_the_two_genuine_rungs(self):
        post = _post()
        left = {(c.get("slug"), p.get("id")) for c in post["crops"]
                for fam in ("pests", "diseases") for p in (c.get(fam) or [])
                if isinstance(p, dict)
                for r in (p.get("control_ladder") or []) if r.get("method") == "prune_out_infection"}
        self.assertEqual(left, {("apple", "fire-blight"), ("artichoke", "botrytis-gray-mold")})

    def test_every_repoint_landed(self):
        post = _post()
        for r in C.REPOINTS + C.REPOINT_REWRITES:
            methods = [x["method"] for x in _prob(post, r["crop"], r["pid"])["control_ladder"]]
            self.assertIn(r["to"], methods, f"{r['crop']}/{r['pid']}")
            self.assertNotIn(r["from"], methods[r["rung"]:r["rung"] + 1])

    def test_the_merge_to_collapsed_both_mismatched_rungs(self):
        post = _post()
        for m in C.MERGE_TO:
            methods = [x["method"] for x in _prob(post, m["crop"], m["pid"])["control_ladder"]]
            self.assertIn(m["to"], methods)
            self.assertNotIn("sensible_seeding_rate", methods)
            self.assertNotIn("water_at_the_base", methods)

    def test_every_split_produced_two_rungs(self):
        post = _post()
        for s in C.SPLITS:
            methods = [x["method"] for x in _prob(post, s["crop"], s["pid"])["control_ladder"]]
            self.assertIn(s["keep_method"], methods, f"{s['crop']}/{s['pid']}")
            self.assertIn(s["new_method"], methods, f"{s['crop']}/{s['pid']}")

    def test_the_jalapeno_lure_clause_is_gone_and_the_key_is_unchanged(self):
        """The hunt CORRECTED the read here: yellow_sticky_traps was right, the lure clause was the
        unsourced part. So the key must NOT have moved and the clause must be gone."""
        post = _post()
        lad = _prob(post, "jalapeno", "pepper-weevil")["control_ladder"]
        self.assertEqual(lad[2]["method"], "yellow_sticky_traps")
        joined = " ".join(lad[2][k] for k in ("note_beginner", "note_seasoned")).lower()
        self.assertNotIn("scent lure", joined)
        self.assertNotIn("pheromone", joined)
        self.assertIn("yellow sticky traps", joined)


class MergeEvidence(unittest.TestCase):
    """A merge is the easiest fix to fake: dropping one rung satisfies 'no prune_out_infection
    survives' while deleting half the advice. Both halves must be present in the merged note."""

    def test_every_merged_rung_carries_content_from_BOTH_original_rungs(self):
        post = _post()
        for (crop, pid), (from_gs, from_prune) in MERGE_EVIDENCE.items():
            m = next(x for x in C.MERGES if x["crop"] == crop and x["pid"] == pid)
            lad = _prob(post, crop, pid)["control_ladder"]
            note = " ".join(lad[m["keep"]][k] for k in ("note_beginner", "note_seasoned")).lower()
            self.assertIn(from_gs.lower(), note, f"{crop}/{pid}: lost the sanitation half")
            self.assertIn(from_prune.lower(), note, f"{crop}/{pid}: lost the removal half")

    def test_the_merge_evidence_table_covers_every_merge(self):
        self.assertEqual(set(MERGE_EVIDENCE), {(m["crop"], m["pid"]) for m in C.MERGES})

    def test_each_ladder_lost_exactly_one_rung_per_merge(self):
        pre_b, post_b = P.staged(), P.fixed_batch()
        def n(b, crop, pid):
            for fam in ("pests", "diseases"):
                for p in b[crop].get(fam, []):
                    if p["id"] == pid:
                        return len(p["control_ladder"])
        for m in C.MERGES:
            self.assertEqual(n(post_b, m["crop"], m["pid"]), n(pre_b, m["crop"], m["pid"]) - 1,
                             f"{m['crop']}/{m['pid']}")


# --------------------------------------------------------------------------- load-bearing 2
class StillOpen(unittest.TestCase):
    """Four rungs are deliberately NOT fixed. Closing them with a near-miss method would look like
    a better result and be a worse one."""

    def test_the_exact_four_are_recorded_with_reasons(self):
        """ENUMERATE the keys, do not count them. Checking only len()==4 and value lengths let a
        mutation RENAME a key -- the record kept its shape while no longer naming the rung it is
        supposed to hold open, and the harness caught it as a survivor."""
        self.assertEqual(set(C.STILL_OPEN), {
            "fig/root-knot-nematode",
            "swiss-chard/root-knot-nematode",
            "jalapeno/pepper-maggot",
            "heirloom-tomato/fruit-cracking",
        })
        for k, v in C.STILL_OPEN.items():
            self.assertGreater(len(v), 40, k)

    def test_the_two_nematode_rungs_keep_their_original_keys(self):
        post = _post()
        self.assertEqual(_prob(post, "fig", "root-knot-nematode")["control_ladder"][0]["method"],
                         "garden_sanitation")
        self.assertEqual(
            _prob(post, "swiss-chard", "root-knot-nematode")["control_ladder"][0]["method"],
            "crop_rotation")

    def test_container_culture_was_not_minted_to_close_them(self):
        self.assertNotIn("container_culture", _post()["control_methods"])

    def test_the_padded_pepper_maggot_ladder_is_left_at_its_authored_length(self):
        pre_b = P.staged()
        n = next(len(p["control_ladder"]) for p in pre_b["jalapeno"]["pests"]
                 if p["id"] == "pepper-maggot")
        self.assertEqual(len(_prob(_post(), "jalapeno", "pepper-maggot")["control_ladder"]), n)

    def test_fruit_cracking_still_uses_even_watering(self):
        methods = [r["method"] for r in
                   _prob(_post(), "heirloom-tomato", "fruit-cracking")["control_ladder"]]
        self.assertIn("even_watering", methods)


# --------------------------------------------------------------------------- ids
class IdStability(unittest.TestCase):
    def test_thirty_eight_ids_minted_none_reused(self):
        d = _pre()
        minted, reused, rungs = P.apply_to(d)
        self.assertEqual((minted, reused, rungs), (38, 0, PROMOTED_RUNGS))

    def test_promoted_ids_match_the_authored_ids_exactly(self):
        b, post = P.staged(), _post()
        for crop in P.CROPS:
            for fam in ("pests", "diseases"):
                for i, p in enumerate(b[crop].get(fam, [])):
                    tgt = next(c for c in post["crops"] if c["slug"] == crop)[fam][i]
                    self.assertEqual(tgt["id"], p["id"], f"{crop}/{fam}/{i}")

    def test_an_existing_canonical_id_WINS_over_the_staged_one(self):
        """Ids are join keys for varieties[].resistance and ladder_delta. Canonical must win."""
        d = _pre()
        crop = next(c for c in d["crops"] if c["slug"] == "fig")
        crop["pests"][0]["id"] = "already-shipped-id"
        P.apply_to(d)
        self.assertEqual(crop["pests"][0]["id"], "already-shipped-id")

    def test_every_problem_gains_a_type(self):
        post = _post()
        for crop in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == crop)
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    self.assertTrue(p.get("type"), f"{crop}/{p.get('id')}")


# --------------------------------------------------------------------------- ladder integrity
class LadderIntegrity(unittest.TestCase):
    def test_validate_batch_passes_on_the_fixed_batch(self):
        self.assertIsNone(P.validate_batch(P.fixed_batch(), _pre()["control_methods"]))

    def test_validate_batch_REJECTS_the_unfixed_staged_batch(self):
        """Reachability: the validator must fail on what the bots actually authored, or it is
        asserting nothing about the fixes. NOTE this proves only that SOME check fires -- see
        RefusalReachability for why that was not enough."""
        self.assertIsNotNone(P.validate_batch(P.staged(), _pre()["control_methods"]))


class RefusalReachability(unittest.TestCase):
    """EVERY check inside validate_batch must be shown to fire ON ITS OWN.

    The first version of this suite proved reachability by feeding validate_batch the unfixed staged
    batch. That trips the `prune_out_infection` check FIRST and returns immediately, so the
    tier-order and empty-register checks were never shown to fire at all -- and the harness caught
    both as survivors when they were disabled. Each check now gets an otherwise-valid batch with
    exactly one defect injected, which is the only way a per-check refusal is non-vacuous.
    """

    def setUp(self):
        self.cm = _pre()["control_methods"]

    def _one_ladder(self, batch):
        for fam in ("pests", "diseases"):
            for p in batch["basil"].get(fam, []):
                if len(p["control_ladder"]) >= 2:
                    return p
        raise AssertionError("no multi-rung ladder to break")

    def test_a_clean_batch_is_accepted(self):
        """Positive control: the injections below must not be passing for an unrelated reason."""
        self.assertIsNone(P.validate_batch(P.fixed_batch(), self.cm))

    def test_tier_order_check_fires_in_isolation(self):
        b = P.fixed_batch()
        p = self._one_ladder(b)
        lad = p["control_ladder"]
        lad.reverse()  # a non-decreasing ladder reversed decreases, unless it is all one tier
        tiers = [self.cm[r["method"]]["tier"] for r in lad]
        if len(set(tiers)) == 1:
            lad.insert(0, {"method": "copper_fungicide", "note_beginner": "x", "note_seasoned": "y"})
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_empty_register_check_fires_in_isolation(self):
        b = P.fixed_batch()
        self._one_ladder(b)["control_ladder"][0]["note_beginner"] = "   "
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("note_beginner", out)

    def test_identical_register_check_fires_in_isolation(self):
        b = P.fixed_batch()
        r = self._one_ladder(b)["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("identical", out)

    def test_unknown_method_check_fires_in_isolation(self):
        b = P.fixed_batch()
        self._one_ladder(b)["control_ladder"][0]["method"] = "not_a_real_method"
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("not in catalog", out)

    def test_applies_to_check_fires_in_isolation(self):
        """A method legal in the catalog but unreachable from this problem's TYPE."""
        b = P.fixed_batch()
        for fam in ("pests", "diseases"):
            for p in b["jalapeno"].get(fam, []):
                if p.get("type") == "viral":
                    p["control_ladder"][0]["method"] = "balance_nitrogen"
                    out = P.validate_batch(b, self.cm)
                    self.assertIsNotNone(out)
                    self.assertIn("cannot reach type", out)
                    return
        self.fail("no viral problem to inject into")

    def test_prune_check_fires_in_isolation(self):
        b = P.fixed_batch()
        self._one_ladder(b)["control_ladder"][0]["method"] = "prune_out_infection"
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("prune_out_infection survives", out)

    def test_empty_ladder_check_fires_in_isolation(self):
        b = P.fixed_batch()
        self._one_ladder(b)["control_ladder"] = []
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("empty ladder", out)

    def test_tiers_never_decrease_in_any_promoted_ladder(self):
        post = _post()
        cm = post["control_methods"]
        order = {t: i for i, t in enumerate(P.TIERS)}
        for crop in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == crop)
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    tiers = [order[cm[r["method"]]["tier"]] for r in p["control_ladder"]]
                    self.assertEqual(tiers, sorted(tiers), f"{crop}/{p['id']}")

    def test_every_method_is_legal_for_its_problem_type(self):
        post = _post()
        cm = post["control_methods"]
        for crop in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == crop)
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    targets = TYPE_TARGETS.get(p["type"]) or set()
                    for r in p["control_ladder"]:
                        ok = ("any" in cm[r["method"]]["applies_to"]
                              or set(cm[r["method"]]["applies_to"]) & targets)
                        self.assertTrue(ok, f"{crop}/{p['id']}: {r['method']} vs {p['type']}")

    def test_both_registers_present_and_materially_different(self):
        post = _post()
        for crop in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == crop)
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    for i, r in enumerate(p["control_ladder"]):
                        for k in ("note_beginner", "note_seasoned"):
                            self.assertTrue(str(r.get(k) or "").strip(), f"{crop}/{p['id']}#{i}/{k}")
                        self.assertNotEqual(r["note_beginner"], r["note_seasoned"])


# --------------------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_only_the_five_batch_crops_change(self):
        pre = _pre()
        post = _post(pre)
        changed = [c["slug"] for c in pre["crops"]
                   if c != next(x for x in post["crops"] if x["slug"] == c["slug"])]
        self.assertEqual(sorted(changed), sorted(P.CROPS))

    def test_crop_set_is_identical_before_any_value_comparison(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual([c["slug"] for c in pre["crops"]], [c["slug"] for c in post["crops"]])

    def test_no_control_method_or_source_catalog_change(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(pre["control_methods"], post["control_methods"])
        self.assertEqual(pre["source_catalog"], post["source_catalog"])

    def test_problem_counts_unchanged(self):
        pre = _pre()
        post = _post(pre)
        for crop in P.CROPS:
            a = next(c for c in pre["crops"] if c["slug"] == crop)
            b = next(c for c in post["crops"] if c["slug"] == crop)
            for fam in ("pests", "diseases"):
                self.assertEqual(len(a.get(fam) or []), len(b.get(fam) or []), f"{crop}/{fam}")


# --------------------------------------------------------------------------- sourcing
class Sourcing(unittest.TestCase):
    def test_the_mis_anchored_trap_claim_gains_the_document_it_comes_from(self):
        post = _post()
        p = _prob(post, "jalapeno", "pepper-weevil")
        self.assertIn("uf_ifas_edis", p["sources"])
        self.assertEqual(p["anchoring_urls"]["uf_ifas_edis"]["url"],
                         "https://ask.ifas.ufl.edu/publication/IN555")

    def test_the_added_source_is_catalogued_and_T1(self):
        sc = _post()["source_catalog"]
        for s in C.ADD_SOURCES:
            self.assertIn(s["source"], sc)
            self.assertEqual(sc[s["source"]].get("tier"), "T1")

    def test_the_original_anchors_are_not_dropped(self):
        pre, post = _pre(), _post()
        a = _prob(pre, "jalapeno", "pepper-weevil") or {}
        # pre has no ids yet, so locate by name instead
        src_pre = None
        for c in pre["crops"]:
            if c["slug"] != "jalapeno":
                continue
            for p in c.get("pests") or []:
                if p.get("name") == "Pepper weevil":
                    src_pre = p
        self.assertIsNotNone(src_pre)
        for s in src_pre.get("sources") or []:
            self.assertIn(s, _prob(post, "jalapeno", "pepper-weevil")["sources"])


# --------------------------------------------------------------------------- copy hygiene
class CopyHygiene(unittest.TestCase):
    def _authored(self):
        out = []
        for m in C.MERGES + C.MERGE_TO:
            out += [m["note_beginner"], m["note_seasoned"]]
        for r in C.REPOINT_REWRITES + C.EDIT_NOTES:
            out += [r["note_beginner"], r["note_seasoned"]]
        for s in C.SPLITS:
            out += [s["keep_beginner"], s["keep_seasoned"], s["new_beginner"], s["new_seasoned"]]
        return out

    def test_no_dash_forms_barred_in_copy(self):
        for s in self._authored():
            self.assertIsNone(re.search(r"[—–]", s), s[:60])
            self.assertNotIn("--", s)

    def test_american_english(self):
        for s in self._authored():
            for w in BRITISH:
                self.assertIsNone(re.search(rf"\b{w}\b", s, re.I), f"{w} in {s[:60]}")

    def test_no_absolute_claims(self):
        for s in self._authored():
            self.assertIsNone(re.search(
                r"\b(?:always|guaranteed|completely|totally|harmless)\b", s, re.I), s[:80])

    def test_degrees_unspaced(self):
        for s in self._authored():
            self.assertIsNone(re.search(r"\s°F", s), s[:80])

    def test_every_authored_note_is_substantive(self):
        for s in self._authored():
            self.assertGreater(len(s), 60, s)


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_if_a_crop_is_already_laddered(self):
        d = _pre()
        c = next(x for x in d["crops"] if x["slug"] == "basil")
        c["pests"][0]["control_ladder"] = [{"method": "handpick", "note_beginner": "x",
                                            "note_seasoned": "y"}]
        self.assertIsNotNone(P.check(d))

    def test_refuses_a_problem_count_mismatch(self):
        d = _pre()
        c = next(x for x in d["crops"] if x["slug"] == "fig")
        c["pests"].append({"name": "Extra"})
        self.assertIsNotNone(P.check(d))

    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
