#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch2.py. Base 0754031d.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_batch2_suite.py.

THE LOAD-BEARING FAMILY IS `TwinGroupPremise`. This is the first batch cut by FAMILY rather than by
size, and the whole justification is that the four corns share their prose: 276 of 288 source field
instances are byte-identical across the siblings, so ONE crop was authored and the ladders were
propagated. If the four ever diverge, either the propagation broke or they are not twins, and either
way the reason this batch was cut this way is gone. So the suite asserts identity at BOTH ends --
the staged files on disk and the promoted ladders in canonical.

`RefusalReachability` carries forward the batch-1 harness lesson: proving that SOME check fires is
not proving that EACH check fires. Batch 1's reachability test fed the validator a batch that
tripped an earlier check and returned, so two later checks were never shown to fire at all and the
harness caught both as survivors. Each check here gets an otherwise-valid batch with exactly one
defect injected, plus a positive control.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch2 as P  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

POST_SHA = "0e12689ba616bca3316652c9064ca9cbce4aa0c4037b1b69589a1e397abb88a4"
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


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
    return sorted(c["slug"] for c in data["crops"]
                  if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"
                  and any("control_ladder" in p for fam in ("pests", "diseases")
                          for p in (c.get(fam) or []) if isinstance(p, dict)))


def _all_rungs(data):
    for slug in P.CROPS:
        c = next(x for x in data["crops"] if x["slug"] == slug)
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                for i, r in enumerate(p.get("control_ladder") or []):
                    yield slug, p.get("id"), i, r


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

    def test_roster_goes_12_to_16(self):
        self.assertEqual(len(_laddered(_pre())), 12)
        post = _laddered(_post())
        self.assertEqual(len(post), 16)
        for s in P.CROPS:
            self.assertIn(s, post)


# --------------------------------------------------------------------------- load-bearing
class TwinGroupPremise(unittest.TestCase):
    """The family cut's justification, asserted at both ends."""

    def test_the_four_staged_files_are_byte_identical(self):
        d = P.staged_digests()
        self.assertEqual(len(set(d.values())), 1, {k: v[:12] for k, v in d.items()})

    def test_check_REFUSES_if_they_diverge(self):
        """Reachability for the premise guard itself: it must fire when the files differ."""
        import tempfile, shutil
        orig = P.STAGING
        tmp = tempfile.mkdtemp(prefix="twin_")
        try:
            shutil.copytree(orig, os.path.join(tmp, "s"))
            P.STAGING = os.path.join(tmp, "s")
            o = json.load(open(os.path.join(P.STAGING, "out_popcorn.json")))
            o["pests"][0]["control_ladder"][0]["note_beginner"] += " Divergent."
            json.dump(o, open(os.path.join(P.STAGING, "out_popcorn.json"), "w"), indent=1)
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("NOT identical", out)
        finally:
            P.STAGING = orig
            shutil.rmtree(tmp, ignore_errors=True)

    def test_the_four_promoted_crops_carry_identical_ladders(self):
        post = _post()
        sig = {}
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            sig[slug] = json.dumps([[r["method"] for r in p["control_ladder"]]
                                    for fam in ("pests", "diseases") for p in c.get(fam) or []],
                                   sort_keys=True)
        self.assertEqual(len(set(sig.values())), 1)

    def test_identical_prose_too_not_just_identical_method_keys(self):
        post = _post()
        blobs = set()
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            blobs.add(json.dumps([p["control_ladder"] for fam in ("pests", "diseases")
                                  for p in c.get(fam) or []], sort_keys=True))
        self.assertEqual(len(blobs), 1)

    def test_the_staged_files_are_never_written_back(self):
        before = {s: open(os.path.join(P.STAGING, f"out_{s}.json"), "rb").read() for s in P.CROPS}
        _post()
        after = {s: open(os.path.join(P.STAGING, f"out_{s}.json"), "rb").read() for s in P.CROPS}
        self.assertEqual(before, after)


# --------------------------------------------------------------------------- reachability
class Reachability(unittest.TestCase):
    def test_base_has_no_corn_ladders(self):
        pre = _pre()
        for slug in P.CROPS:
            c = next(x for x in pre["crops"] if x["slug"] == slug)
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    self.assertNotIn("control_ladder", p, f"{slug}")

    def test_base_fails_the_post_check(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_passes_the_post_check(self):
        self.assertIsNone(P.verify_post(_post()))

    def test_exclusion_fencing_exists_in_the_base(self):
        """r4 minted it; without it raccoons cannot be laddered and this batch cannot promote."""
        self.assertIn("exclusion_fencing", _pre()["control_methods"])


class RefusalReachability(unittest.TestCase):
    """EVERY check inside validate_batch must be shown to fire ON ITS OWN. See the batch-1 harness
    survivors, where two checks were masked by an earlier one returning first."""

    def setUp(self):
        self.cm = _pre()["control_methods"]

    def _lad(self, batch, slug="sweet-corn"):
        for fam in ("pests", "diseases"):
            for p in batch[slug].get(fam, []):
                if len(p["control_ladder"]) >= 2:
                    return p
        raise AssertionError("no multi-rung ladder")

    def test_a_clean_batch_is_accepted(self):
        self.assertIsNone(P.validate_batch(P.staged(), self.cm))

    def test_empty_ladder_fires(self):
        b = P.staged()
        self._lad(b)["control_ladder"] = []
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("EMPTY", out)

    def test_missing_ladder_fires(self):
        b = P.staged()
        del self._lad(b)["control_ladder"]
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("no control_ladder", out)

    def test_unknown_method_fires(self):
        b = P.staged()
        self._lad(b)["control_ladder"][0]["method"] = "not_a_method"
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("not in catalog", out)

    def test_tier_order_fires(self):
        b = P.staged()
        lad = self._lad(b)["control_ladder"]
        lad.reverse()
        tiers = [self.cm[r["method"]]["tier"] for r in lad]
        if len(set(tiers)) == 1:
            lad.insert(0, {"method": "spinosad", "note_beginner": "x", "note_seasoned": "y"})
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_empty_register_fires(self):
        b = P.staged()
        self._lad(b)["control_ladder"][0]["note_beginner"] = "  "
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("note_beginner", out)

    def test_identical_registers_fire(self):
        b = P.staged()
        r = self._lad(b)["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("identical", out)

    def test_applies_to_fires(self):
        b = P.staged()
        for fam in ("pests", "diseases"):
            for p in b["sweet-corn"].get(fam, []):
                if p.get("type") == "bacterial":
                    p["control_ladder"][0]["method"] = "spinosad"
                    out = P.validate_batch(b, self.cm)
                    self.assertIsNotNone(out)
                    self.assertIn("cannot reach type", out)
                    return
        self.fail("no bacterial problem")

    def test_prune_out_infection_fires(self):
        b = P.staged()
        self._lad(b)["control_ladder"][0]["method"] = "prune_out_infection"
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("prune_out_infection", out)

    def test_missing_id_or_type_fires(self):
        b = P.staged()
        del self._lad(b)["type"]
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("missing id or type", out)

    def test_problem_count_fires(self):
        b = P.staged()
        b["sweet-corn"]["pests"] = b["sweet-corn"]["pests"][:-1]
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("expected 8", out)


# --------------------------------------------------------------------------- raccoons
class RaccoonsIsLaddered(unittest.TestCase):
    """Raccoons is why r4 and the empty-ladder gate fix exist. It must not regress to blank."""

    def test_raccoons_leads_with_exclusion_fencing(self):
        post = _post()
        for slug in P.CROPS:
            lad = _prob(post, slug, "raccoons")["control_ladder"]
            self.assertTrue(lad, f"{slug}/raccoons is empty")
            self.assertEqual(lad[0]["method"], "exclusion_fencing")

    def test_it_is_a_single_rung_and_that_is_correct(self):
        """The source names exactly one control and nothing else. Padding is what the playbook
        forbids, so a single rung here is the right answer, not a thin one."""
        self.assertEqual(len(_prob(_post(), "sweet-corn", "raccoons")["control_ladder"]), 1)

    def test_the_rung_restates_the_CROPS_figures_not_the_methods(self):
        """Restate from the crop's own prose: the crop says about 4 and 8 inches. The method carries
        Iowa State's 4-6 and 12; importing those would be introducing a fact the crop does not assert."""
        r = _prob(_post(), "sweet-corn", "raccoons")["control_ladder"][0]
        blob = r["note_beginner"] + " " + r["note_seasoned"]
        self.assertIn("4 and 8", blob)
        self.assertNotIn("4 to 6", blob)

    def test_the_timing_point_survives(self):
        r = _prob(_post(), "sweet-corn", "raccoons")["control_ladder"][0]
        self.assertIn("before", r["note_beginner"].lower())
        self.assertIn("milk stage", r["note_seasoned"].lower())


# --------------------------------------------------------------------------- ladder integrity
class LadderIntegrity(unittest.TestCase):
    def test_eighty_eight_rungs(self):
        self.assertEqual(P.rung_count(P.staged()), 88)

    def test_tiers_never_decrease(self):
        post = _post()
        cm = post["control_methods"]
        order = {t: i for i, t in enumerate(P.TIERS)}
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    tiers = [order[cm[r["method"]]["tier"]] for r in p["control_ladder"]]
                    self.assertEqual(tiers, sorted(tiers), f"{slug}/{p['id']}")

    def test_every_method_legal_for_its_type(self):
        post = _post()
        cm = post["control_methods"]
        for slug, pid, i, r in _all_rungs(post):
            p = _prob(post, slug, pid)
            targets = TYPE_TARGETS.get(p["type"]) or set()
            ok = "any" in cm[r["method"]]["applies_to"] or set(cm[r["method"]]["applies_to"]) & targets
            self.assertTrue(ok, f"{slug}/{pid}#{i}: {r['method']} vs {p['type']}")

    def test_no_ladder_is_empty(self):
        for slug, pid, _i, _r in _all_rungs(_post()):
            self.assertTrue(_prob(_post(), slug, pid)["control_ladder"])

    def test_registers_present_and_different(self):
        for slug, pid, i, r in _all_rungs(_post()):
            for k in ("note_beginner", "note_seasoned"):
                self.assertTrue(str(r.get(k) or "").strip(), f"{slug}/{pid}#{i}/{k}")
            self.assertNotEqual(r["note_beginner"], r["note_seasoned"], f"{slug}/{pid}#{i}")


# --------------------------------------------------------------------------- ids
class IdStability(unittest.TestCase):
    def test_thirty_two_minted_none_reused(self):
        d = _pre()
        self.assertEqual(P.apply_to(d), (32, 0, 88))

    def test_an_existing_canonical_id_WINS(self):
        d = _pre()
        crop = next(c for c in d["crops"] if c["slug"] == "popcorn")
        crop["pests"][0]["id"] = "already-shipped"
        P.apply_to(d)
        self.assertEqual(crop["pests"][0]["id"], "already-shipped")

    def test_ids_are_kebab_and_unique_per_crop(self):
        post = _post()
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            ids = [p["id"] for fam in ("pests", "diseases") for p in c.get(fam) or []]
            self.assertEqual(len(ids), len(set(ids)), slug)
            for i in ids:
                self.assertRegex(i, r"^[a-z0-9]+(-[a-z0-9]+)*$", f"{slug}/{i}")


# --------------------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_only_the_four_corns_change(self):
        pre = _pre()
        post = _post(pre)
        changed = [c["slug"] for c in pre["crops"]
                   if c != next(x for x in post["crops"] if x["slug"] == c["slug"])]
        self.assertEqual(sorted(changed), sorted(P.CROPS))

    def test_crop_set_identical_before_value_comparison(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual([c["slug"] for c in pre["crops"]], [c["slug"] for c in post["crops"]])

    def test_no_control_method_or_source_change(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(pre["control_methods"], post["control_methods"])
        self.assertEqual(pre["source_catalog"], post["source_catalog"])

    def test_batch_1_crops_untouched(self):
        pre = _pre()
        post = _post(pre)
        for slug in ("basil", "fig", "heirloom-tomato", "jalapeno", "swiss-chard"):
            a = next(c for c in pre["crops"] if c["slug"] == slug)
            b = next(c for c in post["crops"] if c["slug"] == slug)
            self.assertEqual(a, b, slug)


# --------------------------------------------------------------------------- copy hygiene
class CopyHygiene(unittest.TestCase):
    def _strings(self):
        return [r[k] for _s, _p, _i, r in _all_rungs(_post())
                for k in ("note_beginner", "note_seasoned")]

    def test_no_dash_forms(self):
        for s in self._strings():
            self.assertIsNone(re.search(r"[—–]", s), s[:60])
            self.assertNotIn("--", s)

    def test_american_english(self):
        for s in self._strings():
            for w in BRITISH:
                self.assertIsNone(re.search(rf"\b{w}\b", s, re.I), f"{w} in {s[:60]}")

    def test_no_absolute_claims(self):
        for s in self._strings():
            self.assertIsNone(re.search(
                r"\b(?:always|guaranteed|completely|totally|harmless)\b", s, re.I), s[:80])

    def test_degrees_unspaced(self):
        for s in self._strings():
            self.assertIsNone(re.search(r"\s°F", s), s[:80])

    def test_no_bare_safety_claim(self):
        """The class swept in cffa4a7 and 9116050 must not re-enter through new content."""
        for s in self._strings():
            self.assertIsNone(re.search(r"\b(?:is|are)\s+safe\b", s, re.I), s[:80])
            self.assertIsNone(re.search(r"\bpet-safe\b", s, re.I), s[:80])


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_if_a_crop_is_already_laddered(self):
        d = _pre()
        c = next(x for x in d["crops"] if x["slug"] == "popcorn")
        c["pests"][0]["control_ladder"] = [{"method": "handpick", "note_beginner": "x",
                                            "note_seasoned": "y"}]
        self.assertIsNotNone(P.check(d))

    def test_refuses_a_problem_count_mismatch(self):
        d = _pre()
        next(x for x in d["crops"] if x["slug"] == "flint-corn")["pests"].append({"name": "Extra"})
        self.assertIsNotNone(P.check(d))

    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
