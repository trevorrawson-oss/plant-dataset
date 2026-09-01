#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_catalog_r8.py. Base 919eabc4 (batch 22, a commit).

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are LIVE is `VerifyPostIsDriven`
plus tools/mutate_pla8_catalog_r8_suite.py.

`check` and `verify_post` RETURN a message rather than raising, matching r5/r7, so every driver
asserts on the returned string and a `None` return is the pass.

WHAT IS NEW versus r5 and r7:

* `OpposedPair` drives a guard against a hazard that is ALREADY LIVE in the catalog, rather than
  against something this round declined to do. `raise_soil_ph` is named alike, is for clubroot, and
  moves soil pH the opposite way from what potato scab needs; the two must never both be legal on
  one problem. Its vacuity branch (an empty `applies_to` makes disjointness trivially true) has its
  own driver, because that is the branch that would quietly hollow the guard out.
* `MintsNoSources` drives the count assertion that keeps an EMPTY `NEW_SOURCES` from making the
  whole source-mint validation block vacuous. r7 minted a source and its checks ran; r8 mints none,
  so the guard is that the emptiness is DECLARED rather than merely happening.
"""
import copy, hashlib, json, os, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_catalog_r8 as P  # noqa: E402
import build_pla8_catalog_r8_content as C  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "6a67a677960afcf3a0a85069c73737243d8117869232ec66ce8b79e99bdc8797"
MINTS = ("cure_and_store", "lower_soil_ph")
OPPOSITE = "raise_soil_ph"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Patch:
    """Patch an attribute on the CONTENT module, which is what the promote reads through."""

    def __init__(self, name, value, mod=C):
        self.n, self.v, self.m = name, value, mod

    def __enter__(self):
        self.old = getattr(self.m, self.n)
        setattr(self.m, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(self.m, self.n, self.old)
        return False


def _mints(**over):
    """A deep copy of MINTS with one method's field overridden."""
    m = copy.deepcopy(C.MINTS)
    for key, (field, value) in over.items():
        if value is _DROP:
            m[key].pop(field, None)
        else:
            m[key][field] = value
    return m


class _Drop:
    pass


_DROP = _Drop()


def _run_main(path, apply_=False):
    argv = sys.argv
    sys.argv = ["promote_pla8_catalog_r8.py", path] + (["--apply"] if apply_ else [])
    try:
        P.main()
    finally:
        sys.argv = argv


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    def test_clean_apply_passes(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        snap = P.snapshot(d)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(snap, d))

    def test_a_crop_change_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["crops"][0]["slug"] = "mutated-crop"
        self.assertIn("a crop changed", P.verify_post(snap, d))

    def test_an_existing_method_change_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["control_methods"]["garden_sanitation"]["tier"] = "physical"
        self.assertIn("existing method", P.verify_post(snap, d))

    def test_an_existing_source_change_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["source_catalog"]["umn_ext"]["tier"] = "T2"
        self.assertIn("existing source", P.verify_post(snap, d))

    def test_an_extra_method_is_caught_not_just_a_changed_one(self):
        """set equality BEFORE value comparison; iterating pre alone makes additions invisible."""
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["control_methods"]["ghost_method"] = {"name": "Ghost"}
        self.assertIn("methods added", P.verify_post(snap, d))

    def test_a_dropped_method_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        del d["control_methods"]["garden_sanitation"]
        self.assertIn("methods dropped", P.verify_post(snap, d))

    def test_an_added_source_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["source_catalog"]["ghost_src"] = {"name": "G", "tier": "T1"}
        self.assertIn("sources added", P.verify_post(snap, d))

    def test_a_dropped_source_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        del d["source_catalog"]["umn_ext"]
        self.assertIn("sources dropped", P.verify_post(snap, d))


class Fixture(unittest.TestCase):
    def test_pre_state_matches_base_sha(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_post_is_this_promotes_own_output(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_base_sha_is_enforced(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(b'{"crops":[]}')
        try:
            with self.assertRaises(SystemExit) as cm:
                _run_main(path)
            self.assertIn("base SHA", str(cm.exception))
        finally:
            os.unlink(path)

    def test_catalog_grows_by_exactly_two_and_sources_not_at_all(self):
        pre, post = _pre(), _post()
        self.assertEqual(len(post["control_methods"]) - len(pre["control_methods"]), 2)
        self.assertEqual(len(post["source_catalog"]), len(pre["source_catalog"]))
        self.assertEqual(sorted(set(post["control_methods"]) - set(pre["control_methods"])),
                         sorted(MINTS))

    def test_clean_check_passes(self):
        self.assertIsNone(P.check(_pre()))


class MintsNoSources(unittest.TestCase):
    """r8 mints no sources. The risk is that an empty NEW_SOURCES makes the whole source-mint
    validation block vacuous without anyone noticing, so the emptiness is DECLARED."""

    def test_new_sources_really_is_empty(self):
        self.assertEqual(C.NEW_SOURCES, {})

    def test_every_anchor_is_an_existing_t1_catalog_entry(self):
        sc = _pre()["source_catalog"]
        for key in MINTS:
            for s in C.MINTS[key]["sources"]:
                self.assertIn(s, sc, f"{key}/{s}")
                self.assertEqual((sc[s].get("tier") or "").upper(), "T1", f"{key}/{s}")

    def test_an_undeclared_source_mint_is_refused(self):
        with _Patch("NEW_SOURCES", {"ghost_src": {"tier": "T1"}}):
            self.assertIn("expected 0", P.check(_pre()))

    def test_a_changed_mint_count_is_refused(self):
        with _Patch("MINTS", {k: v for k, v in C.MINTS.items() if k == "lower_soil_ph"}):
            self.assertIn("expected 2", P.check(_pre()))


class OpposedPair(unittest.TestCase):
    """The hazard this round exists to disarm, and it is ALREADY LIVE in the catalog."""

    def test_the_opposite_method_really_is_opposite_in_the_base(self):
        cm = _pre()["control_methods"]
        self.assertIn(OPPOSITE, cm)
        self.assertIn("lim", cm[OPPOSITE]["name"].lower())
        self.assertEqual(cm[OPPOSITE]["applies_to"], ["fungal_soilborne"])

    def test_the_pair_is_disjoint_after_apply(self):
        cm = _post()["control_methods"]
        self.assertEqual(set(cm["lower_soil_ph"]["applies_to"])
                         & set(cm[OPPOSITE]["applies_to"]), set())
        self.assertIsNone(P.opposed_pair_holds(cm))

    def test_a_shared_target_is_refused(self):
        cm = _post()["control_methods"]
        cm[OPPOSITE]["applies_to"] = ["fungal_soilborne", "bacterial"]
        self.assertIn("opposite", P.opposed_pair_holds(cm).lower())

    def test_a_shared_target_from_the_new_side_is_refused(self):
        """Either side widening is the same defect; both directions are driven."""
        cm = _post()["control_methods"]
        cm["lower_soil_ph"]["applies_to"] = ["bacterial", "fungal_soilborne"]
        self.assertIn("contradictory", P.opposed_pair_holds(cm))

    def test_an_empty_applies_to_is_caught_as_vacuous(self):
        """THE ANTI-VACUITY BRANCH. Disjointness against an empty set is trivially true, so the
        guard would report success while checking nothing."""
        cm = _post()["control_methods"]
        cm[OPPOSITE]["applies_to"] = []
        self.assertIn("vacuously", P.opposed_pair_holds(cm))

    def test_losing_the_cross_reference_is_refused(self):
        cm = _post()["control_methods"]
        cm["lower_soil_ph"]["best_use"] = "A bed with a scab history, decided before planting."
        cm["lower_soil_ph"]["cautions"] = ["Test the soil before changing it"]
        cm["lower_soil_ph"]["how_it_works_seasoned"] = "Hold the pH down where scab has a history."
        self.assertIn("names its opposite", P.opposed_pair_holds(cm))

    def test_a_missing_pair_member_is_refused(self):
        cm = _post()["control_methods"]
        del cm[OPPOSITE]
        self.assertIn("cannot be checked", P.opposed_pair_holds(cm))

    def test_verify_post_runs_the_pair_check_before_the_bystander_loop(self):
        """ORDERING IS LOAD-BEARING. Widening `raise_soil_ph` IS a change to an existing method, so
        if the bystander comparison ran first this guard could never fire on that half."""
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["control_methods"][OPPOSITE]["applies_to"] = ["fungal_soilborne", "bacterial"]
        msg = P.verify_post(snap, d)
        self.assertIn("opposite", msg.lower())
        self.assertNotIn("existing method", msg)


class MintShape(unittest.TestCase):
    def test_required_fields_present_on_both(self):
        for key in MINTS:
            for f in P.REQUIRED:
                self.assertTrue(C.MINTS[key].get(f), f"{key}.{f}")

    def test_missing_required_field_refused(self):
        with _Patch("MINTS", _mints(cure_and_store=("best_use", _DROP))):
            self.assertIn("missing required field", P.check(_pre()))

    def test_empty_required_field_refused(self):
        with _Patch("MINTS", _mints(lower_soil_ph=("pros", []))):
            self.assertIn("missing required field", P.check(_pre()))

    def test_unknown_tier_refused(self):
        with _Patch("MINTS", _mints(cure_and_store=("tier", "magical"))):
            self.assertIn("is not one of", P.check(_pre()))

    def test_applies_to_outside_the_gate_vocabulary_refused(self):
        with _Patch("MINTS", _mints(lower_soil_ph=("applies_to", ["storage_rot"]))):
            self.assertIn("outside the gate vocabulary", P.check(_pre()))

    def test_a_key_already_in_the_catalog_refused(self):
        pre = _pre()
        pre["control_methods"]["cure_and_store"] = {"name": "squatter"}
        self.assertIn("already in the catalog", P.check(pre))

    def test_applies_to_actually_reaches_the_target_problems(self):
        """A method no problem can legally reach is a dead entry. Both mints are checked against
        the REAL types of the problems they were minted for."""
        from control_ladder_gate import TYPE_TARGETS
        post = _post()
        cm = post["control_methods"]

        def legal(method, ptype):
            return bool(set(TYPE_TARGETS[ptype]) & set(cm[method]["applies_to"]))
        # garlic neck rot is `fungal`; potato blackleg will be `bacterial`
        self.assertTrue(legal("cure_and_store", "fungal"))
        self.assertTrue(legal("cure_and_store", "bacterial"))
        # beet/scab is already typed `bacterial` on the roster
        self.assertTrue(legal("lower_soil_ph", "bacterial"))
        self.assertFalse(legal("lower_soil_ph", "fungal"))

    def test_beet_scab_is_really_typed_bacterial(self):
        """The datum `lower_soil_ph`'s applies_to was read off, not assumed."""
        pre = _pre()
        beet = next(c for c in pre["crops"] if c["slug"] == "beet")
        scab = next(p for p in beet["diseases"] if p.get("name") == "Scab")
        self.assertEqual(scab.get("type"), "bacterial")


class Sourcing(unittest.TestCase):
    def test_unknown_source_refused(self):
        with _Patch("MINTS", _mints(cure_and_store=("sources", ["umass_ext", "ghost_ext"]))):
            self.assertIn("is not in source_catalog", P.check(_pre()))

    def test_non_t1_source_refused(self):
        pre = _pre()
        pre["source_catalog"]["umass_ext"] = dict(pre["source_catalog"]["umass_ext"], tier="T2")
        self.assertIn("is not T1", P.check(pre))

    def test_source_without_an_anchor_refused(self):
        m = copy.deepcopy(C.MINTS)
        m["lower_soil_ph"]["sources"] = ["clemson_hgic", "osu_ext", "umn_ext"]
        with _Patch("MINTS", m):
            self.assertIn("has no anchoring_url", P.check(_pre()))

    def test_anchor_for_an_undeclared_source_refused(self):
        m = copy.deepcopy(C.MINTS)
        m["lower_soil_ph"]["anchoring_urls"]["umn_ext"] = {
            "url": "https://extension.umn.edu/x", "verified": "2026-09-01"}
        with _Patch("MINTS", m):
            self.assertIn("is not a declared source", P.check(_pre()))

    def test_non_https_anchor_refused(self):
        m = copy.deepcopy(C.MINTS)
        m["lower_soil_ph"]["anchoring_urls"]["osu_ext"]["url"] = "http://pnwhandbooks.org/x"
        with _Patch("MINTS", m):
            self.assertIn("is not https", P.check(_pre()))

    def test_anchor_without_a_verified_date_refused(self):
        m = copy.deepcopy(C.MINTS)
        m["lower_soil_ph"]["anchoring_urls"]["osu_ext"]["verified"] = "2026"
        with _Patch("MINTS", m):
            self.assertIn("no valid verified date", P.check(_pre()))

    def test_every_anchor_is_https_and_dated(self):
        import re
        for key in MINTS:
            for s, a in C.MINTS[key]["anchoring_urls"].items():
                self.assertTrue(a["url"].startswith("https://"), f"{key}/{s}")
                self.assertRegex(a["verified"], r"^\d{4}-\d{2}-\d{2}$", f"{key}/{s}")


class Hedges(unittest.TestCase):
    """Each hedge is a sentence a later editor would plausibly trim as waffle when it is in fact
    the finding. The crop-specific one is the whole reason this method is safe to ship."""

    def test_all_hedges_present(self):
        self.assertIsNone(P.check(_pre()))
        for key, hedges in C.REQUIRED_HEDGES.items():
            blob = " ".join(P.prose_of(C.MINTS[key])).lower()
            for h in hedges:
                self.assertIn(h.lower(), blob, f"{key}: {h}")

    def test_dropping_the_crop_specific_hedge_is_refused(self):
        m = copy.deepcopy(C.MINTS)
        m["cure_and_store"]["how_it_works_seasoned"] = \
            "Curing heals wounds and sets skins; store the cured crop cool and dry."
        m["cure_and_store"]["cautions"] = ["Set aside bruised produce to use first"]
        m["cure_and_store"]["how_it_works_beginner"] = "Hold the crop a while before storing it."
        with _Patch("MINTS", m):
            self.assertIn("crop-specific", P.check(_pre()))

    def test_dropping_the_chilling_injury_hedge_is_refused(self):
        m = copy.deepcopy(C.MINTS)
        m["cure_and_store"]["cautions"] = [
            "The curing and storage conditions are crop-specific, so take the figures from the "
            "crop's own guidance"]
        with _Patch("MINTS", m):
            self.assertIn("chilling injury", P.check(_pre()))

    def test_hedges_may_not_name_an_unminted_method(self):
        with _Patch("REQUIRED_HEDGES", dict(C.REQUIRED_HEDGES, ghost_method=("x",))):
            self.assertIn("does not mint", P.check(_pre()))


class CopyHygiene(unittest.TestCase):
    def test_shipped_prose_is_clean(self):
        for key in MINTS:
            for s in P.prose_of(C.MINTS[key]):
                self.assertIsNone(P.hygiene(s), f"{key}: {s[:60]}")

    def test_each_banned_shape_is_caught(self):
        for bad, frag in (("It never fails on a cured crop.", "absolute"),
                          ("Hold it at 55 °F for a week.", "spaced degF"),
                          ("Hold it at 55 F for a week.", "bare F"),
                          ("Cure it well -- then store it.", "double hyphen"),
                          ("A dash — here.", "em or en dash"),
                          ("Store in the **cold**.", "markdown"),
                          ("The colour of the skin sets.", "British"),
                          ("Cured roots are safe.", "bare safety claim")):
            self.assertIsNotNone(P.hygiene(bad), bad)
            self.assertIn(frag.split()[0].lower(), str(P.hygiene(bad)).lower(), bad)

    def test_clean_prose_passes(self):
        self.assertIsNone(P.hygiene("Cure the crop at the warmth its own guidance names."))

    def test_a_hygiene_violation_in_a_mint_is_refused(self):
        """Injected into `pros`, which carries no REQUIRED_HEDGES text. Sabotaging `best_use`
        instead trips the earlier hedge check and never reaches this branch."""
        with _Patch("MINTS", _mints(
                cure_and_store=("pros", ["Curing never fails to stop a storage rot."]))):
            self.assertIn("copy hygiene", P.check(_pre()))


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_post(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_no_crop_gains_or_loses_a_rung(self):
        pre, post = _pre(), _post()
        def rungs(d):
            return sum(len(p.get("control_ladder") or [])
                       for c in d["crops"] for f in ("pests", "diseases")
                       for p in c.get(f) or [] if isinstance(p, dict))
        self.assertEqual(rungs(pre), rungs(post))

    def test_one_serializer(self):
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


class MainIsWiredToTheGuards(unittest.TestCase):
    """Every other driver calls `check` and `verify_post` DIRECTLY, which proves the functions work
    and proves nothing about whether `main` runs them. The harness found exactly that hole: cutting
    the `check(data)` call out of `main` left the whole suite green. Reach the guard through the
    entry point."""

    def _fixture(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(promote_fixture.pre_state(P.BASE_SHA))
        return path

    def test_main_refuses_what_check_refuses(self):
        path = self._fixture()
        try:
            with _Patch("MINTS", _mints(cure_and_store=("tier", "magical"))):
                with self.assertRaises(SystemExit) as cm:
                    _run_main(path)
            self.assertIn("REFUSED", str(cm.exception))
            self.assertIn("is not one of", str(cm.exception))
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)

    def test_main_refuses_what_verify_post_refuses(self):
        """Sabotage AFTER apply, so only the post-state check can see it."""
        path = self._fixture()
        real = P.apply_to

        def wrapped(data):
            out = real(data)
            data["crops"][0]["slug"] = "mutated-by-the-driver"
            return out
        try:
            with _Patch("apply_to", wrapped, mod=P):
                with self.assertRaises(SystemExit) as cm:
                    _run_main(path)
            self.assertIn("a crop changed", str(cm.exception))
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)

    def test_main_applies_the_pinned_post_sha(self):
        path = self._fixture()
        try:
            _run_main(path, apply_=True)
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), POST_SHA)
        finally:
            os.unlink(path)

    def test_a_clean_dry_run_writes_nothing(self):
        path = self._fixture()
        try:
            _run_main(path)
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)


class DeferralIsRecorded(unittest.TestCase):
    """Deliberately NOT a guard on the catalog: a check asserting no mounding method exists would
    have to be retired by the round that adds it. The record is what carries forward."""

    def test_the_deferral_is_written_down_with_its_measurement(self):
        self.assertIn("in_season_mounding", C.DEFERRED)
        d = C.DEFERRED["in_season_mounding"]
        self.assertIn("5 problems", d["measured"])
        self.assertIn("three mechanisms", d["why_not_yet"])

    def test_no_mounding_method_was_actually_minted(self):
        for key in C.MINTS:
            self.assertNotIn("mound", key)
            self.assertNotIn("hill", key)


if __name__ == "__main__":
    unittest.main(verbosity=2)
