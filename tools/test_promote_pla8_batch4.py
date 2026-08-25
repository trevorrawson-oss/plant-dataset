#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch4.py. Base e40cd8ec.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_batch4_suite.py.

THE LOAD-BEARING FAMILY IS `HybridGrouping`, and it is the first batch to need BOTH directions.
Batch 2's promote refuses if its four corns DIVERGE. Batch 3's refuses if its three cucumbers
CONVERGE. This batch is both at once: a verified 40/40 twin pair that was authored once and
propagated, and a trio at 73-80% that was authored three times. A promote that could not tell them
apart would ship one of the two defects those batches exist to prevent.

DISTINCTNESS HERE IS ABOUT PROSE, NOT METHOD KEYS. The trio converges on identical method sequences,
which is correct: same seven problems, mostly shared prose, and none of the crop-distinct variety
claims that made the cucumbers diverge. Comparing method keys alone refused this batch on its first
dry run. What must differ is the notes.

`ReadFixes` pins the three corrections, all of which were found ACROSS siblings rather than inside
one crop, and two of which the new cross-sibling check surfaced mechanically.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch4 as P  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

POST_SHA = "e794969f24a670e5c8573d27a66b6d9d7ad885b8637e1768227a643944d6fe71"
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")
_PRISTINE = {s: open(os.path.join(REPO, "tools", "staging", "pla8_ladder_batch4",
                                  f"out_{s}.json"), "rb").read() for s in P.CROPS}


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

    def test_roster_goes_19_to_24(self):
        self.assertEqual(len(_laddered(_pre())), 19)
        post = _laddered(_post())
        self.assertEqual(len(post), 24)
        for s in P.CROPS:
            self.assertIn(s, post)


class HybridGrouping(unittest.TestCase):
    """Both premises at once, asserted in opposite directions."""

    def test_the_twin_pair_is_byte_identical_on_disk(self):
        d = P.staged_digests()
        self.assertEqual(d[P.TWIN[0]], d[P.TWIN[1]])

    def test_the_trio_files_are_all_distinct_on_disk(self):
        d = {s: P.staged_digests()[s] for s in P.TRIO}
        self.assertEqual(len(set(d.values())), len(P.TRIO), d)

    def test_check_REFUSES_if_the_twin_pair_diverges(self):
        import tempfile, shutil
        orig = P.STAGING
        tmp = tempfile.mkdtemp(prefix="b4twin_")
        try:
            shutil.copytree(orig, os.path.join(tmp, "s"))
            P.STAGING = os.path.join(tmp, "s")
            o = json.load(open(os.path.join(P.STAGING, f"out_{P.TWIN[1]}.json")))
            o["pests"][0]["control_ladder"][0]["note_beginner"] += " Divergent."
            json.dump(o, open(os.path.join(P.STAGING, f"out_{P.TWIN[1]}.json"), "w"), indent=1)
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("NOT byte-identical", out)
        finally:
            P.STAGING = orig
            shutil.rmtree(tmp, ignore_errors=True)

    def test_check_REFUSES_if_two_of_the_trio_collide(self):
        import tempfile, shutil
        orig = P.STAGING
        tmp = tempfile.mkdtemp(prefix="b4trio_")
        try:
            shutil.copytree(orig, os.path.join(tmp, "s"))
            P.STAGING = os.path.join(tmp, "s")
            src = open(os.path.join(P.STAGING, "out_acorn-squash.json"), "rb").read()
            open(os.path.join(P.STAGING, "out_butternut-squash.json"), "wb").write(src)
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("byte-identical", out)
        finally:
            P.STAGING = orig
            shutil.rmtree(tmp, ignore_errors=True)

    def test_check_REFUSES_a_trio_file_that_equals_the_TWIN_file(self):
        """The cross-family collision, which the two earlier checks cannot see.

        If a trio crop's file is copied from the twin's, the trio files stay distinct FROM EACH
        OTHER and the twin pair stays identical, so both of the preceding guards pass. Only the
        cross-family check can object, and nothing exercised that state until this test -- the
        harness scored disabling it a survivor.
        """
        import tempfile, shutil
        orig = P.STAGING
        tmp = tempfile.mkdtemp(prefix="b4xf_")
        try:
            shutil.copytree(orig, os.path.join(tmp, "s"))
            P.STAGING = os.path.join(tmp, "s")
            src = open(os.path.join(P.STAGING, f"out_{P.TWIN[0]}.json"), "rb").read()
            open(os.path.join(P.STAGING, "out_acorn-squash.json"), "wb").write(src)
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("propagation across a family", out,
                          f"the cross-family guard did not fire; got: {out}")
        finally:
            P.STAGING = orig
            shutil.rmtree(tmp, ignore_errors=True)

    def test_the_twin_pair_carries_identical_ladders_after_promote(self):
        post = _post()
        def blob(s):
            c = next(x for x in post["crops"] if x["slug"] == s)
            return json.dumps([p["control_ladder"] for fam in ("pests", "diseases")
                               for p in c.get(fam) or []], sort_keys=True)
        self.assertEqual(blob(P.TWIN[0]), blob(P.TWIN[1]))

    def test_the_trio_prose_is_distinct_after_promote(self):
        post = _post()
        def blob(s):
            c = next(x for x in post["crops"] if x["slug"] == s)
            return json.dumps([[(r["note_beginner"], r["note_seasoned"]) for r in p["control_ladder"]]
                               for fam in ("pests", "diseases") for p in c.get(fam) or []],
                              sort_keys=True)
        self.assertEqual(len({blob(s) for s in P.TRIO}), len(P.TRIO))

    def test_the_trio_METHOD_sequences_converging_is_ACCEPTED(self):
        """Pins the ruling that refused this batch on its first dry run.

        Identical method keys across a shared-name family is the correct outcome when the crops
        carry the same problems and mostly the same prose. If a future edit re-tightens the
        distinctness check onto method keys, this fails and says why.
        """
        post = _post()
        def methods(s):
            c = next(x for x in post["crops"] if x["slug"] == s)
            return json.dumps([[r["method"] for r in p["control_ladder"]]
                               for fam in ("pests", "diseases") for p in c.get(fam) or []],
                              sort_keys=True)
        self.assertEqual(len({methods(s) for s in P.TRIO}), 1,
                         "the trio no longer converges on methods; if that is intended, this "
                         "test should be updated rather than deleted")
        self.assertIsNone(P.verify_post(post), "convergent methods must not be refused")

    def test_the_staged_files_are_never_written_back(self):
        _post()
        after = {s: open(os.path.join(P.STAGING, f"out_{s}.json"), "rb").read() for s in P.CROPS}
        self.assertEqual(after, _PRISTINE)


class ReadFixes(unittest.TestCase):
    """The three corrections, all found ACROSS siblings rather than inside one crop."""

    def test_no_downy_mildew_ladder_carries_copper(self):
        """These crops' prose says only 'a labeled fungicide' and names no material."""
        post = _post()
        for slug in P.CROPS:
            p = _prob(post, slug, "downy-mildew")
            if p:
                self.assertNotIn("copper_fungicide", [r["method"] for r in p["control_ladder"]], slug)

    def test_certified_cucumber_KEEPS_its_copper_rung(self):
        """The contrast that justifies the removal: cucumber's prose NAMES copper, so its rung is
        correct and must not be swept up by a blanket rule."""
        p = _prob(_post(), "cucumber", "downy-mildew")
        self.assertIn("copper_fungicide", [r["method"] for r in p["control_ladder"]])

    def test_every_borer_ladder_carries_the_new_method(self):
        post = _post()
        for slug in P.CROPS:
            p = _prob(post, slug, "squash-vine-borer")
            self.assertIsNotNone(p, slug)
            self.assertIn(P.BORER_METHOD, [r["method"] for r in p["control_ladder"]], slug)

    def test_no_borer_ladder_still_uses_handpick(self):
        """handpick's own con is 'Misses hidden eggs and tiny larvae'; a larva inside a stem is
        exactly that case."""
        post = _post()
        for slug in P.CROPS:
            p = _prob(post, slug, "squash-vine-borer")
            self.assertNotIn("handpick", [r["method"] for r in p["control_ladder"]], slug)

    def test_the_borer_method_is_legal_for_the_type_it_landed_on(self):
        post = _post()
        cm = post["control_methods"]
        for slug in P.CROPS:
            p = _prob(post, slug, "squash-vine-borer")
            targets = TYPE_TARGETS.get(p["type"]) or set()
            self.assertTrue(set(cm[P.BORER_METHOD]["applies_to"]) & targets, slug)

    def test_problem_ids_match_the_roster_convention(self):
        post = _post()
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    want = P.ID_CONVENTION.get(p.get("name") or "")
                    if want:
                        self.assertEqual(p["id"], want, f"{slug}/{p.get('name')}")

    def test_the_singular_id_is_gone_everywhere(self):
        """The summer-squash pair minted `cucumber-beetle`; the roster ships the plural."""
        post = _post()
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            ids = [p.get("id") for fam in ("pests", "diseases") for p in c.get(fam) or []]
            self.assertNotIn("cucumber-beetle", ids, slug)

    def test_verify_post_CATCHES_copper_that_slipped_past_check(self):
        """Isolates verify_post's copper guard.

        check() refuses a copper rung before apply ever runs, so nothing a normal test does can make
        verify_post's copy of that assertion speak. Disabling it changed nothing observable and the
        harness scored it a survivor. Kept rather than deleted as redundant: check() reads the
        STAGED batch, verify_post reads what actually landed in canonical, and those are different
        questions the day someone edits apply_to.
        """
        d = _post()
        p = _prob(d, "acorn-squash", "downy-mildew")
        p["control_ladder"].append({"method": "copper_fungicide",
                                    "note_beginner": "x", "note_seasoned": "y"})
        out = P.verify_post(d)
        self.assertIsNotNone(out)
        self.assertIn("regained copper_fungicide", out)

    def test_check_REFUSES_a_reintroduced_copper_rung(self):
        import tempfile, shutil
        orig = P.STAGING
        tmp = tempfile.mkdtemp(prefix="b4cu_")
        try:
            shutil.copytree(orig, os.path.join(tmp, "s"))
            P.STAGING = os.path.join(tmp, "s")
            f = os.path.join(P.STAGING, "out_acorn-squash.json")
            o = json.load(open(f))
            for p in o["diseases"]:
                if p["id"] == "downy-mildew":
                    p["control_ladder"].append({"method": "copper_fungicide",
                                                "note_beginner": "x", "note_seasoned": "y"})
            json.dump(o, open(f, "w"), indent=1)
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("copper_fungicide", out)
        finally:
            P.STAGING = orig
            shutil.rmtree(tmp, ignore_errors=True)

    def test_check_REFUSES_a_divergent_problem_id(self):
        import tempfile, shutil
        orig = P.STAGING
        tmp = tempfile.mkdtemp(prefix="b4id_")
        try:
            shutil.copytree(orig, os.path.join(tmp, "s"))
            P.STAGING = os.path.join(tmp, "s")
            f = os.path.join(P.STAGING, "out_acorn-squash.json")
            o = json.load(open(f))
            for p in o["pests"]:
                if p["id"] == "cucumber-beetles":
                    p["id"] = "cucumber-beetle"
            json.dump(o, open(f, "w"), indent=1)
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn("join keys", out)
        finally:
            P.STAGING = orig
            shutil.rmtree(tmp, ignore_errors=True)

    def test_check_REFUSES_a_borer_ladder_without_the_method(self):
        import tempfile, shutil
        orig = P.STAGING
        tmp = tempfile.mkdtemp(prefix="b4bo_")
        try:
            shutil.copytree(orig, os.path.join(tmp, "s"))
            P.STAGING = os.path.join(tmp, "s")
            f = os.path.join(P.STAGING, "out_acorn-squash.json")
            o = json.load(open(f))
            for p in o["pests"]:
                if p["id"] == "squash-vine-borer":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != P.BORER_METHOD]
            json.dump(o, open(f, "w"), indent=1)
            out = P.check(_pre())
            self.assertIsNotNone(out)
            self.assertIn(P.BORER_METHOD, out)
        finally:
            P.STAGING = orig
            shutil.rmtree(tmp, ignore_errors=True)

    def test_check_REFUSES_if_the_mint_round_has_not_landed(self):
        d = _pre()
        del d["control_methods"][P.BORER_METHOD]
        out = P.check(d)
        self.assertIsNotNone(out)
        self.assertIn("mint round", out)


class RefusalReachability(unittest.TestCase):
    """EVERY check inside validate_batch shown to fire ON ITS OWN."""

    def setUp(self):
        self.cm = _pre()["control_methods"]

    def _lad(self, batch, slug="acorn-squash"):
        for fam in ("pests", "diseases"):
            for p in batch[slug].get(fam, []):
                if len(p["control_ladder"]) >= 2:
                    return p
        raise AssertionError("no multi-rung ladder")

    def test_a_clean_batch_is_accepted(self):
        self.assertIsNone(P.validate_batch(P.staged(), self.cm))

    def test_empty_ladder_fires(self):
        b = P.staged(); self._lad(b)["control_ladder"] = []
        self.assertIn("EMPTY", P.validate_batch(b, self.cm) or "")

    def test_missing_ladder_fires(self):
        b = P.staged(); del self._lad(b)["control_ladder"]
        self.assertIn("no control_ladder", P.validate_batch(b, self.cm) or "")

    def test_unknown_method_fires(self):
        b = P.staged(); self._lad(b)["control_ladder"][0]["method"] = "not_a_method"
        self.assertIn("not in catalog", P.validate_batch(b, self.cm) or "")

    def test_tier_order_fires(self):
        b = P.staged()
        lad = self._lad(b)["control_ladder"]
        lad.reverse()
        if len({self.cm[r["method"]]["tier"] for r in lad}) == 1:
            lad.insert(0, {"method": "spinosad", "note_beginner": "x", "note_seasoned": "y"})
        self.assertIn("tiers decrease", P.validate_batch(b, self.cm) or "")

    def test_empty_register_fires(self):
        b = P.staged(); self._lad(b)["control_ladder"][0]["note_beginner"] = "  "
        self.assertIn("note_beginner", P.validate_batch(b, self.cm) or "")

    def test_identical_registers_fire(self):
        b = P.staged()
        r = self._lad(b)["control_ladder"][0]
        r["note_seasoned"] = r["note_beginner"]
        self.assertIn("identical", P.validate_batch(b, self.cm) or "")

    def test_applies_to_fires(self):
        b = P.staged()
        for fam in ("pests", "diseases"):
            for p in b["acorn-squash"].get(fam, []):
                if p.get("type") == "bacterial":
                    p["control_ladder"][0]["method"] = "spinosad"
                    self.assertIn("cannot reach type", P.validate_batch(b, self.cm) or "")
                    return
        self.fail("no bacterial problem")

    def test_prune_out_infection_fires(self):
        b = P.staged(); self._lad(b)["control_ladder"][0]["method"] = "prune_out_infection"
        self.assertIn("prune_out_infection", P.validate_batch(b, self.cm) or "")

    def test_missing_id_or_type_fires(self):
        b = P.staged(); del self._lad(b)["type"]
        self.assertIn("missing id or type", P.validate_batch(b, self.cm) or "")

    def test_problem_count_fires(self):
        b = P.staged(); b["acorn-squash"]["pests"] = b["acorn-squash"]["pests"][:-1]
        self.assertIn("expected 7", P.validate_batch(b, self.cm) or "")

    def test_per_crop_rung_count_fires_with_the_total_unchanged(self):
        import promote_pla8_batch4 as M
        real = M.staged
        def moved():
            b = real()
            src = next(p for p in b["acorn-squash"]["pests"] if len(p["control_ladder"]) > 1)
            src["control_ladder"].pop()
            dst = next(p for p in b["butternut-squash"]["pests"] if p["id"] == "squash-bug")
            tail = copy.deepcopy(dst["control_ladder"][-1])
            tail["note_beginner"] += " Duplicate."
            dst["control_ladder"].append(tail)
            return b
        try:
            M.staged = moved
            out = M.check(_pre())
        finally:
            M.staged = real
        self.assertIsNotNone(out)
        self.assertIn("rungs, expected", out)


class LadderIntegrity(unittest.TestCase):
    def test_one_hundred_thirty_nine_rungs(self):
        self.assertEqual(P.rung_count(P.staged()), 139)

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
        for slug, pid, i, r in _all_rungs(post):
            pass
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

    def test_anthracnose_style_restraint_no_conventional_rung_anywhere(self):
        """No crop in this batch names a conventional material; a carbaryl or pyrethroid rung would
        mean one was invented to fill a ladder out."""
        post = _post()
        cm = post["control_methods"]
        for slug, pid, i, r in _all_rungs(post):
            self.assertNotEqual(cm[r["method"]]["tier"], "conventional", f"{slug}/{pid}#{i}")


class IdStability(unittest.TestCase):
    def test_thirty_one_minted_none_reused(self):
        self.assertEqual(P.apply_to(_pre()), (31, 0, 139))

    def test_an_existing_canonical_id_WINS(self):
        d = _pre()
        crop = next(c for c in d["crops"] if c["slug"] == "acorn-squash")
        crop["pests"][0]["id"] = "already-shipped"
        P.apply_to(d)
        self.assertEqual(crop["pests"][0]["id"], "already-shipped")

    def test_ids_kebab_and_unique_per_crop(self):
        post = _post()
        for slug in P.CROPS:
            c = next(x for x in post["crops"] if x["slug"] == slug)
            ids = [p["id"] for fam in ("pests", "diseases") for p in c.get(fam) or []]
            self.assertEqual(len(ids), len(set(ids)), slug)
            for i in ids:
                self.assertRegex(i, r"^[a-z0-9]+(-[a-z0-9]+)*$", f"{slug}/{i}")


class BlastRadius(unittest.TestCase):
    def test_crop_set_identical_before_value_comparison(self):
        pre = _pre(); post = _post(pre)
        self.assertEqual([c["slug"] for c in pre["crops"]], [c["slug"] for c in post["crops"]])
        self.assertEqual(set(pre.keys()), set(post.keys()))

    def test_only_the_five_squashes_change(self):
        pre = _pre(); post = _post(pre)
        by = {c["slug"]: c for c in post["crops"]}
        changed = [c["slug"] for c in pre["crops"] if c != by[c["slug"]]]
        self.assertEqual(sorted(changed), sorted(P.CROPS))

    def test_pumpkin_is_NOT_touched(self):
        """A Squash-category singleton that also carries Squash vine borer. Easy to sweep in."""
        pre = _pre(); post = _post(pre)
        a = next(c for c in pre["crops"] if c["slug"] == "pumpkin")
        b = next(c for c in post["crops"] if c["slug"] == "pumpkin")
        self.assertEqual(a, b)

    def test_no_control_method_or_source_change(self):
        pre = _pre(); post = _post(pre)
        self.assertEqual(pre["control_methods"], post["control_methods"])
        self.assertEqual(pre["source_catalog"], post["source_catalog"])

    def test_earlier_batches_untouched(self):
        pre = _pre(); post = _post(pre)
        for slug in ("cucumber", "pickling-cucumber", "slicing-cucumber", "sweet-corn", "basil"):
            a = next(c for c in pre["crops"] if c["slug"] == slug)
            b = next(c for c in post["crops"] if c["slug"] == slug)
            self.assertEqual(a, b, slug)


class CopyHygiene(unittest.TestCase):
    def _strings(self):
        return [r[k] for _s, _p, _i, r in _all_rungs(_post())
                for k in ("note_beginner", "note_seasoned")]

    def test_there_are_strings_to_check(self):
        self.assertEqual(len(self._strings()), 139 * 2)

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
        for s in self._strings():
            self.assertIsNone(re.search(r"\b(?:is|are)\s+safe\b", s, re.I), s[:80])
            self.assertIsNone(re.search(r"\bpet-safe\b", s, re.I), s[:80])


class Reachability(unittest.TestCase):
    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_base_fails_the_post_check(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_passes_the_post_check(self):
        self.assertIsNone(P.verify_post(_post()))

    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_if_a_crop_is_already_laddered(self):
        d = _pre()
        c = next(x for x in d["crops"] if x["slug"] == "acorn-squash")
        c["pests"][0]["control_ladder"] = [{"method": "handpick", "note_beginner": "x",
                                            "note_seasoned": "y"}]
        self.assertIsNotNone(P.check(d))


if __name__ == "__main__":
    unittest.main(verbosity=2)
