#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_ant_exclusion.py. Base 2a9d3c85 (batch 17's output, commit b196251).

REPLAY-PINNED; no RED phase claimed. Evidence that these guards are LIVE is `VerifyPostIsDriven`
plus tools/mutate_pla8_ant_exclusion_suite.py, NOT that this file passes.

Every driver asserts its branch's ONE message.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_ant_exclusion as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

# FROZEN LITERALS -- restated, never imported from P.
KEY = "ant_exclusion"
TIER = "physical"
APPLIES = ["insect_soft_bodied", "insect_general", "disease_general"]
SOURCE_IDS = {"ucanr_ext_ants", "ucanr_ext_sooty_mold", "uc_ipm_citrus_ants"}
METHODS_BEFORE, SOURCES_BEFORE = 61, 215
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Patch:
    def __init__(self, name, value):
        self.n, self.v = name, value

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(P, self.n, self.old)
        return False


def _expect(case, fragment, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(fragment, str(cm.exception))


def _mutated(**over):
    m = copy.deepcopy(P.ANT_EXCLUSION)
    m.update(over)
    return m


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    """A catalog revision's whole safety claim is 'no crop moved'. If verify_post is vacuous,
    nothing else in this file notices."""

    def _args(self, pre):
        return (P.crop_fingerprint(pre), copy.deepcopy(pre["control_methods"]),
                copy.deepcopy(pre["source_catalog"]))

    def test_a_changed_crop_is_caught(self):
        pre = _pre()
        a = self._args(pre)
        d = _post(pre)
        d["crops"][0]["pests"] = []
        _expect(self, "changed; this promote touches no crop", lambda: P.verify_post(*a, d))

    def test_a_dropped_crop_is_caught(self):
        pre = _pre()
        a = self._args(pre)
        d = _post(pre)
        d["crops"].pop()
        _expect(self, "crop roster changed", lambda: P.verify_post(*a, d))

    def test_an_edited_existing_method_is_caught(self):
        pre = _pre()
        a = self._args(pre)
        d = _post(pre)
        d["control_methods"]["garden_sanitation"]["tier"] = "physical"
        _expect(self, "existing method", lambda: P.verify_post(*a, d))

    def test_an_edited_existing_source_is_caught(self):
        pre = _pre()
        a = self._args(pre)
        d = _post(pre)
        k = next(iter(d["source_catalog"]))
        d["source_catalog"][k] = {"name": "tampered"}
        _expect(self, "existing source", lambda: P.verify_post(*a, d))

    def test_an_extra_method_is_caught(self):
        """RENAMES an existing method in post, so the count still reads 62 and the set-difference
        branch fires rather than the count branch. This is the addition-invisibility shape:
        comparing only counts would call a rename clean."""
        pre = _pre()
        a = self._args(pre)
        d = _post(pre)
        d["control_methods"]["stowaway"] = d["control_methods"].pop("garden_sanitation")
        _expect(self, "methods added", lambda: P.verify_post(*a, d))

    def test_an_extra_source_is_caught(self):
        """The source-side twin of test_an_extra_method_is_caught. Its absence let the
        added-sources branch SURVIVE the mutation harness: no test exercised it at all, so the
        method-side coverage created a false impression that both halves were guarded."""
        pre = _pre()
        a = self._args(pre)
        d = _post(pre)
        victim = next(iter(pre["source_catalog"]))
        d["source_catalog"]["stowaway"] = d["source_catalog"].pop(victim)
        _expect(self, "sources added", lambda: P.verify_post(*a, d))

    def test_clean_apply_passes(self):
        """Positive control: the RED results above are the guard firing, not blanket refusal."""
        pre = _pre()
        a = self._args(pre)
        self.assertEqual(P.verify_post(*a, _post(pre)), (METHODS_BEFORE + 1, SOURCES_BEFORE + 3))


class Fixture(unittest.TestCase):
    def test_pre_state_matches_base_sha(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_base_is_batch_17_output(self):
        pre = _pre()
        self.assertEqual(len(pre["control_methods"]), METHODS_BEFORE)
        self.assertNotIn(KEY, pre["control_methods"])


# ---------------------------------------------------------------- the mint
class Mint(unittest.TestCase):
    def test_method_lands_with_pinned_shape(self):
        m = _post()["control_methods"][KEY]
        self.assertEqual(m["tier"], TIER)
        self.assertEqual(m["applies_to"], APPLIES)
        for f in ("name", "how_it_works_beginner", "how_it_works_seasoned", "best_use",
                  "pros", "cons", "sources", "anchoring_urls"):
            self.assertTrue(m.get(f), "missing %s" % f)

    def test_sources_land(self):
        sc = _post()["source_catalog"]
        for sid in SOURCE_IDS:
            self.assertIn(sid, sc)
            self.assertEqual(sc[sid]["tier"], "T1")

    def test_remint_refused(self):
        """SWAPS a key rather than adding one, so the method COUNT premise stays satisfied and this
        branch is the one that fires. Adding would trip the count check first and pass for the
        wrong reason."""
        pre = _pre()
        pre["control_methods"][KEY] = pre["control_methods"].pop("garden_sanitation")
        _expect(self, "already exists in the catalog", lambda: P.check(pre))

    def test_existing_source_id_refused(self):
        """Swaps rather than adds, for the same reason as test_remint_refused."""
        pre = _pre()
        victim = next(iter(pre["source_catalog"]))
        pre["source_catalog"]["ucanr_ext_ants"] = pre["source_catalog"].pop(victim)
        _expect(self, "source id", lambda: P.check(pre))

    def test_missing_required_field_refused(self):
        pre = _pre()
        with _Patch("ANT_EXCLUSION", {k: v for k, v in P.ANT_EXCLUSION.items() if k != "pros"}):
            _expect(self, "missing required field", lambda: P.check(pre))

    def test_method_count_premise_refused(self):
        pre = _pre()
        pre["control_methods"]["extra"] = {"tier": "cultural"}
        _expect(self, "methods, expected", lambda: P.check(pre))

    def test_source_count_premise_refused(self):
        pre = _pre()
        pre["source_catalog"]["extra"] = {"name": "x"}
        _expect(self, "entries, expected", lambda: P.check(pre))


class TierAndScope(unittest.TestCase):
    def test_tier_is_pinned_to_physical(self):
        pre = _pre()
        with _Patch("ANT_EXCLUSION", _mutated(tier="cultural")):
            _expect(self, "every exclusion/barrier method in the catalog is", lambda: P.check(pre))

    def test_disease_general_cannot_be_dropped(self):
        """Without it, sooty mold stays unladderable and the mint accomplishes nothing."""
        pre = _pre()
        with _Patch("ANT_EXCLUSION", _mutated(applies_to=["insect_soft_bodied",
                                                          "insect_general"])):
            _expect(self, "disease_general", lambda: P.check(pre))

    def test_sorts_below_beneficial_predators(self):
        """The mechanism claim, asserted structurally: the sources say exclude ants SO THAT natural
        enemies can work, so this rung must be able to precede the biological rung in a ladder."""
        cm = _post()["control_methods"]
        self.assertLess(TIERS.index(cm[KEY]["tier"]),
                        TIERS.index(cm["beneficial_predators"]["tier"]))

    def test_reaches_a_fungal_typed_problem(self):
        """The end-to-end point of the mint: `fungal` resolves via `disease_general`."""
        cm = _post()["control_methods"]
        fungal_targets = {"fungal_foliar", "fungal_soilborne", "disease_general"}
        self.assertTrue(fungal_targets & set(cm[KEY]["applies_to"]),
                        "a fungal-typed problem still cannot name ant_exclusion")

    def test_reaches_an_insect_typed_problem(self):
        cm = _post()["control_methods"]
        insect_targets = {"insect_general", "insect_chewing", "insect_boring", "insect_soft_bodied"}
        self.assertTrue(insect_targets & set(cm[KEY]["applies_to"]))


class Anchors(unittest.TestCase):
    def test_anchoring_url_must_be_its_own_catalog_url(self):
        """The mis-pointed-key defect class: a real document filed under a sibling's id."""
        pre = _pre()
        bad = copy.deepcopy(P.ANT_EXCLUSION)
        bad["anchoring_urls"]["ucanr_ext_ants"] = {
            "url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn74108.html", "verified": "2026-08-31"}
        with _Patch("ANT_EXCLUSION", bad):
            _expect(self, "not its catalog url", lambda: P.check(pre))

    def test_sources_and_anchors_must_agree(self):
        pre = _pre()
        bad = copy.deepcopy(P.ANT_EXCLUSION)
        bad["anchoring_urls"].pop("uc_ipm_citrus_ants")
        with _Patch("ANT_EXCLUSION", bad):
            _expect(self, "disagree", lambda: P.check(pre))

    def test_unadmitted_source_refused(self):
        pre = _pre()
        with _Patch("ANT_EXCLUSION", _mutated(sources=list(P.ANT_EXCLUSION["sources"]) + ["nope"])):
            _expect(self, "unadmitted source", lambda: P.check(pre))

    def test_every_anchor_is_t1(self):
        sc = _post()["source_catalog"]
        for sid in _post()["control_methods"][KEY]["sources"]:
            self.assertEqual(sc[sid]["tier"], "T1", "%s is not T1" % sid)


class A54Titles(unittest.TestCase):
    """A54 is why the first cut of this mint took gate_all to 121/121 FAILED: the source entries
    carried `name` but no `title`. The promote now calls A54's OWN checker rather than
    re-implementing its rule, so these drive the real gate."""

    def test_missing_title_refused_at_check(self):
        pre = _pre()
        stripped = {k: {kk: vv for kk, vv in v.items() if kk != "title"}
                    for k, v in P.NEW_SOURCES.items()}
        with _Patch("NEW_SOURCES", stripped):
            _expect(self, "missing 'title'", lambda: P.check(pre))

    def test_a54_gate_runs_in_verify_post(self):
        """A bare institution-root carrying a title is A54's D2 fabrication check. It passes
        SOURCE_REQUIRED (every field present), so only the real gate catches it -- which is what
        makes this a driver for the A54 call rather than for the field loop above."""
        pre = _pre()
        extra = copy.deepcopy(P.NEW_SOURCES)
        extra["bogus_root"] = {
            "id": "bogus_root", "name": "Bogus Root", "title": "A Title A Bare Root Should Not Have",
            "publisher": "X", "url": "https://example.edu", "source_class": "university_extension",
            "trust_tier": "high", "accessed": "2026-08", "tier": "T1", "citable_for": "x",
        }
        with _Patch("NEW_SOURCES", extra):
            a = (P.crop_fingerprint(pre), copy.deepcopy(pre["control_methods"]),
                 copy.deepcopy(pre["source_catalog"]))
            d = _post(pre)
            _expect(self, "A54", lambda: P.verify_post(*a, d))

    def test_shipped_sources_carry_document_titles(self):
        sc = _post()["source_catalog"]
        for sid in SOURCE_IDS:
            t = sc[sid].get("title")
            self.assertTrue(isinstance(t, str) and t.strip(), "%s has no title" % sid)
            self.assertIn("UC Statewide IPM Program", t)
            # Read off the document, so it must not be a restatement of the id or the pub number.
            self.assertNotIn(sid, t)

    def test_post_state_passes_the_real_a54_gate(self):
        from source_catalog_title_gate import title_violations
        self.assertEqual(title_violations(_post()["source_catalog"]), [])


class Hygiene(unittest.TestCase):
    def test_em_dash_refused(self):
        pre = _pre()
        with _Patch("ANT_EXCLUSION", _mutated(best_use="a — b")):
            _expect(self, "em/en dash", lambda: P.check(pre))

    def test_absolute_refused(self):
        pre = _pre()
        with _Patch("ANT_EXCLUSION", _mutated(best_use="This never fails.")):
            _expect(self, "absolute", lambda: P.check(pre))

    def test_absolute_in_a_list_entry_refused(self):
        pre = _pre()
        with _Patch("ANT_EXCLUSION", _mutated(cons=["completely stops the pest"])):
            _expect(self, "cons entry", lambda: P.check(pre))

    def test_identical_registers_refused(self):
        pre = _pre()
        same = P.ANT_EXCLUSION["how_it_works_beginner"]
        with _Patch("ANT_EXCLUSION", _mutated(how_it_works_seasoned=same)):
            _expect(self, "identical registers", lambda: P.check(pre))

    def test_shipped_prose_is_clean(self):
        for f in ("how_it_works_beginner", "how_it_works_seasoned", "best_use",
                  "find_it_beginner"):
            self.assertEqual(P.hygiene(P.ANT_EXCLUSION[f]), [], f)
        for lst in ("pros", "cons", "cautions"):
            for item in P.ANT_EXCLUSION[lst]:
                self.assertEqual(P.hygiene(item), [], item[:40])

    def test_registers_are_materially_different(self):
        b = P.ANT_EXCLUSION["how_it_works_beginner"].lower().split()
        s = P.ANT_EXCLUSION["how_it_works_seasoned"].lower().split()
        overlap = len(set(b) & set(s)) / len(set(b) | set(s))
        self.assertLess(overlap, 0.5, "registers are too similar (jaccard %.2f)" % overlap)


class Mechanics(unittest.TestCase):
    def test_one_serializer(self):
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))

    def test_no_crop_moves_end_to_end(self):
        pre = _pre()
        self.assertEqual(P.crop_fingerprint(pre), P.crop_fingerprint(_post(pre)))


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_post(self):
        self.assertEqual(CLG.all_violations(_post()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
