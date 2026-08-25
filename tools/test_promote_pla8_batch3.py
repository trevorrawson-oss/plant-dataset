#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch3.py. Base c13ddea5.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_batch3_suite.py.

THE LOAD-BEARING FAMILY IS `DistinctnessPremise`, AND IT IS THE EXACT INVERSE OF BATCH 2'S.

`test_promote_pla8_batch2.py` carries `TwinGroupPremise`, which asserts the four corns are
BYTE-IDENTICAL at both ends, because that batch authored one crop and propagated the ladders. The
same tool told this session to do the same thing to the three cucumbers. It was wrong: the twin
signature in `ladder_batch.py` was `tuple(sorted(problem_name(p)))`, problem NAMES ONLY, and never
compared prose. The cucumbers share 72.2% of their problem fields, not 100%.

So this suite asserts the OPPOSITE at both ends: the staged files must be DISTINCT, the promoted
ladders must not all match, and the four crop-distinct claims must sit on exactly the crop whose
prose earns them. pickling-cucumber alone names wilt-tolerant County Fair and CMV-resistant
varieties; cucumber and slicing-cucumber name non-bitter varieties, which is a claim about the
VECTOR and therefore does NOT earn a resistant_varieties rung on the bacterial-wilt entry. A
propagation in either direction erases a sourced claim or invents one, and both are refused.

`RefusalReachability` carries forward the batch-1 harness lesson: proving that SOME check fires is
not proving that EACH check fires. Every check gets an otherwise-valid batch with exactly one defect
injected, plus a positive control.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch3 as P  # noqa: E402
import build_pla8_batch3_content as C  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

# Snapshot taken at IMPORT, before any test body runs. The write-back guard used to read its own
# "before" state inside the test, which meant an EARLIER test calling staged() could already have
# rewritten the files; the guard then compared a mutated file to itself and passed. That masking is
# why the harness reported it as a survivor. Same class as the ordering trap in
# `guard-tests-pass-because-an-earlier-check-fires`.
_PRISTINE_STAGED = {s: open(os.path.join(
    os.path.join(REPO, "tools", "staging", "pla8_ladder_batch3"), f"out_{s}.json"), "rb").read()
    for s in ("cucumber", "pickling-cucumber", "slicing-cucumber")}

POST_SHA = "decb944d51e591ef9c7b0f657a258a0a7690f2ad1aa8804dad4b83a235db90c0"
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
        """POST is the promote's OWN output replayed from the fixture, never live canonical."""
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)

    def test_roster_goes_16_to_19(self):
        self.assertEqual(len(_laddered(_pre())), 16)
        post = _laddered(_post())
        self.assertEqual(len(post), 19)
        for s in P.CROPS:
            self.assertIn(s, post)


# --------------------------------------------------------------------------- load-bearing
class DistinctnessPremise(unittest.TestCase):
    """The inverse of batch 2's TwinGroupPremise. These crops are NOT twins."""

    def test_the_three_staged_files_are_all_distinct(self):
        d = P.staged_digests()
        self.assertEqual(len(set(d.values())), len(P.CROPS), {k: v[:12] for k, v in d.items()})

    def test_check_REFUSES_if_the_staged_files_collide(self):
        """Reachability for the premise guard itself: it must fire on a propagation."""
        import tempfile, shutil
        orig = P.STAGING
        tmp = tempfile.mkdtemp(prefix="distinct_")
        try:
            shutil.copytree(orig, os.path.join(tmp, "s"))
            P.STAGING = os.path.join(tmp, "s")
            src = open(os.path.join(P.STAGING, "out_cucumber.json"), "rb").read()
            open(os.path.join(P.STAGING, "out_slicing-cucumber.json"), "wb").write(src)
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("not all distinct", out)
        finally:
            P.STAGING = orig
            shutil.rmtree(tmp, ignore_errors=True)

    def test_the_three_promoted_crops_do_NOT_carry_identical_ladders(self):
        post = _post()
        sig = {}
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            sig[slug] = json.dumps([[r["method"] for r in p["control_ladder"]]
                                    for fam in ("pests", "diseases") for p in c.get(fam) or []],
                                   sort_keys=True)
        self.assertGreater(len(set(sig.values())), 1,
                           "identical ladders across all three means a propagation happened")

    def test_county_fair_belongs_to_pickling_cucumber_ALONE(self):
        post = _post()
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            blob = json.dumps([p.get("control_ladder") for fam in ("pests", "diseases")
                               for p in c.get(fam) or []], ensure_ascii=False)
            self.assertEqual("County Fair" in blob, slug == "pickling-cucumber", slug)

    def test_cmv_resistance_belongs_to_pickling_cucumber_ALONE(self):
        post = _post()
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            blob = json.dumps([p.get("control_ladder") for fam in ("pests", "diseases")
                               for p in c.get(fam) or []], ensure_ascii=False)
            self.assertEqual("CMV-resistant" in blob, slug == "pickling-cucumber", slug)

    def test_bacterial_wilt_resistance_is_pickling_only(self):
        """The Stewart's-wilt structural limit. cucumber and slicing claim only that non-bitter
        varieties attract fewer BEETLES, which is a vector claim, so neither earns the rung on the
        bacterial entry. pickling claims genuine wilt tolerance and does."""
        post = _post()
        for slug in P.CROPS:
            lad = _prob(post, slug, "bacterial-wilt")["control_ladder"]
            has = any(r["method"] == "resistant_varieties" for r in lad)
            self.assertEqual(has, slug == "pickling-cucumber", slug)

    def test_every_pinned_distinct_claim_is_exercised(self):
        """COVERAGE, not overlap: each DISTINCT_CLAIMS entry must be checkable against post, so a
        claim added to the constant without a real problem behind it fails here."""
        post = _post()
        for crop, pid, method, want in P.DISTINCT_CLAIMS:
            p = _prob(post, crop, pid)
            self.assertIsNotNone(p, f"{crop}/{pid} does not exist")
            self.assertEqual(any(r["method"] == method for r in p["control_ladder"]), want,
                             f"{crop}/{pid} {method}")
        self.assertEqual(len(P.DISTINCT_CLAIMS), 9)

    def test_the_staged_files_are_never_written_back(self):
        """Compared against the IMPORT-TIME snapshot, not a read taken inside this test.

        The in-test read was masked by ordering: any earlier test that called staged() would
        already have triggered the write-back, so `before` and `after` matched and the guard passed
        on mutated files. The harness caught it as a survivor.
        """
        _post()
        after = {s: open(os.path.join(P.STAGING, f"out_{s}.json"), "rb").read() for s in P.CROPS}
        self.assertEqual(after, _PRISTINE_STAGED,
                         "a staged file changed on disk; staged() must never write back")


# --------------------------------------------------------------------------- the read delta
class ReadFixDelta(unittest.TestCase):
    """The one fix the read found lives in a delta module, not edited into the staged files."""

    def test_exactly_one_read_fix(self):
        self.assertEqual(len(C.INSERTS), 1)

    def test_the_staged_file_does_NOT_already_contain_it(self):
        """If the fix were edited into staging, the delta would be a no-op that reads as coverage."""
        raw = json.load(open(os.path.join(P.STAGING, "out_cucumber.json")))
        lad = next(p for p in raw["pests"] if p["id"] == "cucumber-beetles")["control_ladder"]
        self.assertNotIn("resistant_varieties", [r["method"] for r in lad])

    def test_the_delta_puts_it_in(self):
        b = P.staged()
        lad = next(p for p in b["cucumber"]["pests"]
                   if p["id"] == "cucumber-beetles")["control_ladder"]
        self.assertEqual([r["method"] for r in lad], C.INSERTS[0]["expect_after"])

    def test_the_delta_REFUSES_a_stale_index(self):
        """And it must be the expect_BEFORE guard that fires, identified by its message.

        `expect_after` is `[method] + expect_before` for an index-0 insert, so it SUBSUMES the
        pre-check: any change to the staged ladder propagates into `after` and would be caught
        there anyway. Asserting only `AssertionError` therefore passes with the pre-check deleted,
        which is exactly how the harness scored it a survivor. The pre-check still earns its place
        because it refuses BEFORE mutating and names the real cause (the staged content moved), so
        the guard is pinned to its own diagnosis rather than to the bare exception type.
        """
        b = {s: json.load(open(os.path.join(P.STAGING, f"out_{s}.json"))) for s in P.CROPS}
        next(p for p in b["cucumber"]["pests"]
             if p["id"] == "cucumber-beetles")["control_ladder"].pop(0)
        with self.assertRaises(AssertionError) as cm:
            C.apply_read_fixes(b)
        self.assertIn("staged ladder is", str(cm.exception),
                      "the expect_before pre-check did not fire; expect_after caught it instead")

    def test_the_delta_leaves_the_ladder_UNTOUCHED_when_it_refuses(self):
        """A refusal that has already mutated is worse than no refusal: the caller sees an error
        and a half-applied ladder. This is what checking BEFORE the insert buys."""
        b = {s: json.load(open(os.path.join(P.STAGING, f"out_{s}.json"))) for s in P.CROPS}
        lad = next(p for p in b["cucumber"]["pests"]
                   if p["id"] == "cucumber-beetles")["control_ladder"]
        lad.pop(0)
        snapshot = [r["method"] for r in lad]
        with self.assertRaises(AssertionError):
            C.apply_read_fixes(b)
        self.assertEqual([r["method"] for r in lad], snapshot, "the ladder was mutated then refused")

    def test_the_delta_REFUSES_a_double_apply(self):
        b = P.staged()          # already delta'd
        with self.assertRaises(AssertionError):
            C.apply_read_fixes(b)

    def test_cucumber_and_slicing_agree_on_the_beetle_rung(self):
        """They carry BYTE-IDENTICAL prevention_seasoned there; the fix exists so they agree."""
        post = _post()
        for slug in ("cucumber", "slicing-cucumber"):
            lad = _prob(post, slug, "cucumber-beetles")["control_ladder"]
            self.assertEqual(lad[0]["method"], "resistant_varieties", slug)

    def test_promote_REFUSES_if_INSERTS_grows_without_bumping_the_constant(self):
        """The only way `n != EXPECTED_READ_FIXES` can fire.

        `apply_read_fixes` already asserts `applied == len(INSERTS)`, so the promote's count check
        is unreachable unless the two disagree -- i.e. someone adds a read-fix and forgets the
        constant. Without this the check was dead code that read as coverage, and the harness
        scored disabling it a survivor.
        """
        base = ["resistant_varieties", "crop_rotation", "garden_sanitation",
                "floating_row_cover", "handpick", "yellow_sticky_traps"]
        # The extra fix must APPLY CLEANLY, or an earlier guard inside apply_read_fixes fires and
        # the count check is never reached. The first version of this reused `crop_rotation`, which
        # slicing's beetle ladder already carries, so the "already present" refusal raised first:
        # the clean test passed for the wrong reason and the harness scored the mutation a survivor.
        # `insecticidal_soap` is absent from that ladder, and appending keeps expect_after honest.
        extra = copy.deepcopy(C.INSERTS[0])
        extra["crop"] = "slicing-cucumber"
        extra["index"] = len(base)
        extra["expect_before"] = base
        extra["expect_after"] = base + ["insecticidal_soap"]
        extra["rung"] = dict(extra["rung"], method="insecticidal_soap")
        orig = C.INSERTS
        try:
            C.INSERTS = orig + [extra]
            with self.assertRaises(AssertionError) as cm:
                P.staged()
            msg = str(cm.exception)
            self.assertIn("expected 1", msg,
                          f"the COUNT check did not fire; something else refused first: {msg}")
        finally:
            C.INSERTS = orig
        self.assertEqual(len(C.INSERTS), 1, "INSERTS was not restored")

    def test_not_applied_list_is_recorded(self):
        self.assertEqual(len(C.NOT_APPLIED), 2)
        for s in C.NOT_APPLIED:
            self.assertTrue(s.strip())


# --------------------------------------------------------------------------- reachability
class Reachability(unittest.TestCase):
    def test_base_has_no_cucumber_ladders(self):
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

    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))


class RefusalReachability(unittest.TestCase):
    """EVERY check inside validate_batch must be shown to fire ON ITS OWN."""

    def setUp(self):
        self.cm = _pre()["control_methods"]

    def _lad(self, batch, slug="cucumber"):
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
            for p in b["cucumber"].get(fam, []):
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
        b["cucumber"]["pests"] = b["cucumber"]["pests"][:-1]
        out = P.validate_batch(b, self.cm)
        self.assertIsNotNone(out)
        self.assertIn("expected 9", out)

    def test_distinctness_check_fires_on_a_wrong_claim(self):
        b = P.staged()
        lad = next(p for p in b["cucumber"]["diseases"]
                   if p["id"] == "bacterial-wilt")["control_ladder"]
        lad.insert(0, {"method": "resistant_varieties", "note_beginner": "x", "note_seasoned": "y"})
        out = P.check_distinctness(b)
        self.assertIsNotNone(out)
        self.assertIn("must NOT carry", out)

    def test_distinctness_check_fires_on_a_stolen_prose_claim(self):
        b = P.staged()
        next(p for p in b["cucumber"]["diseases"]
             if p["id"] == "downy-mildew")["control_ladder"][0]["note_beginner"] += " County Fair."
        out = P.check_distinctness(b)
        self.assertIsNotNone(out)
        self.assertIn("belongs only to", out)

    def test_distinctness_check_fires_when_the_owner_LOSES_its_claim(self):
        b = P.staged()
        for p in b["pickling-cucumber"]["pests"] + b["pickling-cucumber"]["diseases"]:
            for r in p["control_ladder"]:
                r["note_beginner"] = r["note_beginner"].replace("County Fair", "a variety")
                r["note_seasoned"] = r["note_seasoned"].replace("County Fair", "a variety")
        out = P.check_distinctness(b)
        self.assertIsNotNone(out)
        self.assertIn("lost its", out)

    def test_per_crop_rung_count_fires_when_the_TOTAL_is_unchanged(self):
        """Isolates the per-crop check from the total check.

        `rung_count(batch) != sum(EXPECTED_RUNGS.values())` catches a changed total, so moving a
        rung BETWEEN crops leaves the total right and only the per-crop check can see it. Without
        this, disabling the per-crop check survived the harness.
        """
        import promote_pla8_batch3 as M
        d = _pre()
        real = M.staged

        def moved():
            """The move must be TIER-NEUTRAL and legality-neutral, or an earlier check fires first.

            The first version of this appended pickling's popped rung onto a cucumber ladder and
            tripped `tiers decrease` instead -- masking the very check it was written to isolate.
            Removing from the END of a ladder cannot break a non-decreasing sequence, and appending
            a DUPLICATE of a ladder's own last rung keeps both its tier and its applies_to legality.
            Only the per-crop count moves.
            """
            b = real()
            src = next(p for p in b["pickling-cucumber"]["pests"] if len(p["control_ladder"]) > 1)
            src["control_ladder"].pop()
            dst = next(p for p in b["cucumber"]["pests"] if p["id"] == "squash-bug")
            tail = copy.deepcopy(dst["control_ladder"][-1])
            tail["note_beginner"] = tail["note_beginner"] + " Duplicate rung."
            dst["control_ladder"].append(tail)
            return b

        try:
            M.staged = moved
            out = M.check(d)
        finally:
            M.staged = real
        self.assertIsNotNone(out, "a rung moved between crops was not caught")
        self.assertIn("rungs, expected", out)

    def test_distinctness_accepts_the_clean_batch(self):
        self.assertIsNone(P.check_distinctness(P.staged()))


# --------------------------------------------------------------------------- ladder integrity
class LadderIntegrity(unittest.TestCase):
    def test_one_hundred_thirty_seven_rungs(self):
        self.assertEqual(P.rung_count(P.staged()), 137)

    def test_per_crop_rung_counts(self):
        b = P.staged()
        for slug, want in P.EXPECTED_RUNGS.items():
            n = sum(len(p["control_ladder"]) for fam in ("pests", "diseases")
                    for p in b[slug].get(fam, []))
            self.assertEqual(n, want, slug)

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
        post = _post()
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    self.assertTrue(p.get("control_ladder"), f"{slug}/{p.get('id')}")

    def test_registers_present_and_different(self):
        for slug, pid, i, r in _all_rungs(_post()):
            for k in ("note_beginner", "note_seasoned"):
                self.assertTrue(str(r.get(k) or "").strip(), f"{slug}/{pid}#{i}/{k}")
            self.assertNotEqual(r["note_beginner"], r["note_seasoned"], f"{slug}/{pid}#{i}")

    def test_anthracnose_stays_cultural_only_on_all_three(self):
        """Its only named fungicide is chlorothalonil, which has no catalog key. A conventional
        rung appearing here would mean a material was invented to fill the ladder out."""
        post = _post()
        cm = post["control_methods"]
        for slug in P.CROPS:
            lad = _prob(post, slug, "anthracnose")["control_ladder"]
            tiers = {cm[r["method"]]["tier"] for r in lad}
            self.assertNotIn("conventional", tiers, slug)
            self.assertNotIn("soft_chemical", tiers, slug)


# --------------------------------------------------------------------------- ids
class IdStability(unittest.TestCase):
    def test_twenty_seven_minted_none_reused(self):
        d = _pre()
        self.assertEqual(P.apply_to(d), (27, 0, 137))

    def test_an_existing_canonical_id_WINS(self):
        d = _pre()
        crop = next(c for c in d["crops"] if c["slug"] == "pickling-cucumber")
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
    def test_crop_set_identical_before_value_comparison(self):
        """set(pre) == set(post) FIRST. Iterating pre alone makes ADDITIONS invisible, which was
        all four PLA-162 defects."""
        pre = _pre()
        post = _post(pre)
        self.assertEqual([c["slug"] for c in pre["crops"]], [c["slug"] for c in post["crops"]])
        self.assertEqual(set(pre.keys()), set(post.keys()))

    def test_only_the_three_cucumbers_change(self):
        pre = _pre()
        post = _post(pre)
        by_post = {c["slug"]: c for c in post["crops"]}
        changed = [c["slug"] for c in pre["crops"] if c != by_post[c["slug"]]]
        self.assertEqual(sorted(changed), sorted(P.CROPS))

    def test_no_control_method_or_source_change(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(pre["control_methods"], post["control_methods"])
        self.assertEqual(pre["source_catalog"], post["source_catalog"])

    def test_english_cucumber_is_NOT_touched(self):
        """It is a Cucumbers-category SINGLETON, not part of this family. Easy to sweep in."""
        pre = _pre()
        post = _post(pre)
        a = next(c for c in pre["crops"] if c["slug"] == "english-cucumber")
        b = next(c for c in post["crops"] if c["slug"] == "english-cucumber")
        self.assertEqual(a, b)

    def test_earlier_batch_crops_untouched(self):
        pre = _pre()
        post = _post(pre)
        for slug in ("basil", "fig", "heirloom-tomato", "jalapeno", "swiss-chard",
                     "sweet-corn", "field-corn", "popcorn", "flint-corn"):
            a = next(c for c in pre["crops"] if c["slug"] == slug)
            b = next(c for c in post["crops"] if c["slug"] == slug)
            self.assertEqual(a, b, slug)


# --------------------------------------------------------------------------- copy hygiene
class CopyHygiene(unittest.TestCase):
    def _strings(self):
        return [r[k] for _s, _p, _i, r in _all_rungs(_post())
                for k in ("note_beginner", "note_seasoned")]

    def test_there_are_strings_to_check(self):
        """Without this the whole family passes vacuously if _all_rungs ever yields nothing."""
        self.assertEqual(len(self._strings()), 137 * 2)

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
        """The class swept in cffa4a7, 9116050 and 23b4539 must not re-enter through new content."""
        for s in self._strings():
            self.assertIsNone(re.search(r"\b(?:is|are)\s+safe\b", s, re.I), s[:80])
            self.assertIsNone(re.search(r"\bpet-safe\b", s, re.I), s[:80])

    def test_plant_is_lowercase_mid_sentence(self):
        for s in self._strings():
            self.assertIsNone(re.search(r"(?<![.!?]\s)(?<!^)\bPlant\b(?! Pro)", s), s[:80])


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_if_a_crop_is_already_laddered(self):
        d = _pre()
        c = next(x for x in d["crops"] if x["slug"] == "pickling-cucumber")
        c["pests"][0]["control_ladder"] = [{"method": "handpick", "note_beginner": "x",
                                            "note_seasoned": "y"}]
        self.assertIsNotNone(P.check(d))

    def test_refuses_a_problem_count_mismatch(self):
        d = _pre()
        next(x for x in d["crops"] if x["slug"] == "slicing-cucumber")["pests"].append(
            {"name": "Extra"})
        self.assertIsNotNone(P.check(d))


if __name__ == "__main__":
    unittest.main(verbosity=2)
