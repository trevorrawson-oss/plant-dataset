#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_thin_ladder_backfill.py. Base 4f33522c (catalog r9).

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are LIVE is `VerifyPostIsDriven`
plus tools/mutate_pla8_thin_ladder_backfill_suite.py.

WHAT IS NEW versus every PLA-8 batch so far:

* Every batch treated "already laddered" as a REFUSAL. Here it is the PRECONDITION, so
  `AddsWithoutRewriting` drives the inverted protection: the exact prior sequence is pinned, every
  pre-existing rung must be byte-identical after, and the record prose must not move at all.
* `Warrants` drives the guard that would have caught the thin-ladder scan's four FALSE POSITIVES.
  Each of those named a control only to DISCOUNT it ("Research into tolerant varieties is ongoing
  but there is no home cure"), and none could have produced a warrant phrase that survived reading.
"""
import copy, hashlib, json, os, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_thin_ladder_backfill as P  # noqa: E402
import build_pla8_thin_ladder_backfill_content as C  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "b118f19d36d021db95d755225e566843676fe3fa393299f250a8d34bb9605710"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Patch:
    def __init__(self, name, value, mod=C):
        self.n, self.v, self.m = name, value, mod

    def __enter__(self):
        self.old = getattr(self.m, self.n)
        setattr(self.m, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(self.m, self.n, self.old)
        return False


def _bf(key, field, value):
    b = copy.deepcopy(C.BACKFILL)
    b[key][field] = value
    return b


def _run_main(path, apply_=False):
    argv = sys.argv
    sys.argv = ["promote_pla8_thin_ladder_backfill.py", path] + (["--apply"] if apply_ else [])
    try:
        P.main()
    finally:
        sys.argv = argv


FIG = ("fig", "dried-fruit-beetle-souring")
BEET = ("beet", "common-scab")
STRAW = ("strawberry", "red-stele")


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    def test_clean_apply_passes(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        snap = P.snapshot(d)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(snap, d))

    def test_a_bystander_problem_change_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        tom = next(c for c in d["crops"] if c["slug"] == "beefsteak-tomato")
        tom["diseases"][0]["control_ladder"].append(
            {"method": "crop_rotation", "note_beginner": "x", "note_seasoned": "y"})
        self.assertIn("bystander problem", P.verify_post(snap, d))

    def test_an_added_problem_is_caught_not_just_a_changed_one(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        next(c for c in d["crops"] if c["slug"] == "fig")["pests"].append(
            {"name": "ghost-problem", "type": "insect"})
        self.assertIn("problem SET changed", P.verify_post(snap, d))

    def test_a_removed_problem_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        next(c for c in d["crops"] if c["slug"] == "fig")["diseases"].pop()
        self.assertIn("problem SET changed", P.verify_post(snap, d))

    def test_a_control_methods_change_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["control_methods"]["prompt_harvest"]["tier"] = "physical"
        self.assertIn("control_methods changed", P.verify_post(snap, d))

    def test_a_source_catalog_change_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["source_catalog"]["ghost"] = {"name": "G", "tier": "T1"}
        self.assertIn("source_catalog changed", P.verify_post(snap, d))


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

    def test_clean_check_passes(self):
        self.assertIsNone(P.check(_pre()))

    def test_counts_are_pinned(self):
        self.assertEqual(len(C.BACKFILL), C.EXPECTED_PROBLEMS)
        added = sum(len([m for m in s["expect_after"] if m not in s["expect_before"]])
                    for s in C.BACKFILL.values())
        self.assertEqual(added, C.EXPECTED_NEW_RUNGS)
        self.assertEqual(tuple(sorted({s for s, _ in C.BACKFILL})), tuple(sorted(C.EXPECTED_CROPS)))

    def test_exactly_eight_rungs_land(self):
        pre, post = _pre(), _post()

        def rungs(d):
            return sum(len(p.get("control_ladder") or [])
                       for c in d["crops"] for f in ("pests", "diseases")
                       for p in c.get(f) or [] if isinstance(p, dict))
        self.assertEqual(rungs(post) - rungs(pre), 8)


class AddsWithoutRewriting(unittest.TestCase):
    """Every batch so far refused an already-laddered problem. Here it is the precondition."""

    def test_every_target_is_already_laddered(self):
        pre = _pre()
        for (slug, pid) in C.BACKFILL:
            p = P.find_problem(pre, slug, pid)
            self.assertTrue(p.get("control_ladder"), f"{slug}/{pid}")

    def test_existing_rungs_are_byte_identical_after(self):
        pre, post = _pre(), _post()
        for (slug, pid), spec in C.BACKFILL.items():
            before = {r["method"]: r for r in P.find_problem(pre, slug, pid)["control_ladder"]}
            for r in P.find_problem(post, slug, pid)["control_ladder"]:
                if r["method"] in before:
                    self.assertEqual(r, before[r["method"]], f"{slug}/{pid}/{r['method']}")

    def test_rewriting_an_existing_rung_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        p = P.find_problem(d, *STRAW)
        for r in p["control_ladder"]:
            if r["method"] == "crop_rotation":
                r["note_beginner"] = "rewritten by the driver"
        self.assertIn("rewrites none", P.verify_post(snap, d))

    def test_touching_the_record_prose_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        P.find_problem(d, *BEET)["prevention_beginner"] = "rewritten by the driver"
        self.assertIn("record prose field", P.verify_post(snap, d))

    def test_apply_to_itself_refuses_a_drifted_ladder(self):
        """The CONTENT module carries its own expect_before assertion. `apply_to` is called
        directly by the suite and by nothing that ran check() first, so it needs its own driver."""
        pre = _pre()
        P.find_problem(pre, *FIG)["control_ladder"].append(
            {"method": "crop_rotation", "note_beginner": "x", "note_seasoned": "y"})
        with self.assertRaises(AssertionError) as cm:
            P.apply_to(pre)
        self.assertIn("expected", str(cm.exception))

    def test_a_drifted_ladder_refuses(self):
        pre = _pre()
        P.find_problem(pre, *FIG)["control_ladder"].append(
            {"method": "crop_rotation", "note_beginner": "x", "note_seasoned": "y"})
        self.assertIn("it has drifted", P.check(pre))

    def test_dropping_a_rung_is_refused(self):
        with _Patch("BACKFILL", _bf(BEET, "expect_after", ["even_watering", "lower_soil_ph"])):
            self.assertIn("would DROP", P.check(_pre()))

    def test_declared_prose_must_match_the_rungs_added(self):
        with _Patch("BACKFILL", _bf(BEET, "expect_after",
                                    ["even_watering", "lower_soil_ph", "crop_rotation",
                                     "garden_sanitation"])):
            self.assertIn("declares prose for", P.check(_pre()))

    def test_a_wrong_post_ladder_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        P.find_problem(d, *BEET)["control_ladder"].reverse()
        self.assertIn("expected", P.verify_post(snap, d))

    def test_a_missing_target_problem_refuses(self):
        """Keep all six entries and rename ONE problem id. Shrinking the table instead trips the
        problem-COUNT check first and never reaches this branch."""
        b = {(k if k != FIG else ("fig", "no-such-problem")): v
             for k, v in copy.deepcopy(C.BACKFILL).items()}
        with _Patch("BACKFILL", b):
            self.assertIn("not on the roster", P.check(_pre()))

    def test_the_problem_count_is_pinned(self):
        with _Patch("BACKFILL", {FIG: C.BACKFILL[FIG]}):
            self.assertIn("expected 6", P.check(_pre()))

    def test_the_changed_problem_count_is_pinned(self):
        """verify_post counts what actually moved. Reached by calling it directly, since check()
        refuses a shrunk table before main would ever get here."""
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        with _Patch("EXPECTED_PROBLEMS", 5):
            self.assertIn("6 problems changed, expected 5", P.verify_post(snap, d))

    def test_the_crop_set_is_pinned(self):
        with _Patch("EXPECTED_CROPS", ("beet", "fig", "garlic")):
            self.assertIn("expected", P.check(_pre()))


class Warrants(unittest.TestCase):
    """The guard that would have caught the scan's four false positives."""

    def test_every_warrant_is_really_in_its_record(self):
        pre = _pre()
        for (slug, pid, m), phrase in C.WARRANTS.items():
            blob = P.record_prose(P.find_problem(pre, slug, pid)).lower()
            self.assertIn(phrase.lower(), blob, f"{slug}/{pid}/{m}")

    def test_a_missing_warrant_refuses(self):
        w = {k: v for k, v in C.WARRANTS.items() if k != ("beet", "common-scab", "lower_soil_ph")}
        with _Patch("WARRANTS", w):
            self.assertIn("has no declared warrant", P.check(_pre()))

    def test_a_warrant_absent_from_the_record_refuses(self):
        """The false-positive shape: a plausible-sounding rung whose phrase is not in the prose."""
        w = dict(C.WARRANTS)
        w[("beet", "common-scab", "lower_soil_ph")] = "apply elemental sulfur each spring"
        with _Patch("WARRANTS", w):
            self.assertIn("is NOT in the record", P.check(_pre()))

    def test_the_warrant_table_must_cover_exactly_the_added_rungs(self):
        w = dict(C.WARRANTS)
        w[("fig", "fig-endosepsis", "garden_sanitation")] = "clean"
        with _Patch("WARRANTS", w):
            self.assertIn("does not exactly cover", P.check(_pre()))

    def test_the_check_level_rung_count_is_pinned(self):
        """Assert the SPECIFIC message. `expected 7` appears in check()'s message AND in
        check_warrants', so a hedged assertion lets either branch be disabled."""
        with _Patch("EXPECTED_NEW_RUNGS", 7):
            self.assertIn("backfill adds 8 rungs, expected 7", P.check(_pre()))

    def test_the_warrant_coverage_count_is_pinned(self):
        """Reach check_warrants' own count branch by calling it directly, past the earlier check."""
        with _Patch("EXPECTED_NEW_RUNGS", 7):
            self.assertIn("warrant check covered 8 rungs, expected 7", P.check_warrants(_pre()))


class RungShape(unittest.TestCase):
    def test_unknown_method_refused(self):
        b = copy.deepcopy(C.BACKFILL)
        b[BEET]["expect_after"] = ["even_watering", "lower_soil_ph", "crop_rotation", "no_such"]
        b[BEET]["add"]["no_such"] = {"note_beginner": "a", "note_seasoned": "b"}
        with _Patch("BACKFILL", b):
            self.assertIn("unknown method", P.check(_pre()))

    def test_duplicate_method_refused(self):
        """Duplicate a rung that is ALREADY in expect_before, so the added-set comparison still
        matches and the duplicate check is the branch that fires."""
        with _Patch("BACKFILL", _bf(BEET, "expect_after",
                                    ["even_watering", "lower_soil_ph", "crop_rotation",
                                     "crop_rotation"])):
            self.assertIn("duplicate method", P.check(_pre()))

    def test_tier_decrease_refused(self):
        b = copy.deepcopy(C.BACKFILL)
        b[FIG]["expect_after"] = ["prompt_harvest", "resistant_varieties", "garden_sanitation",
                                  "pyrethrin", "crop_rotation"]
        b[FIG]["add"]["pyrethrin"] = {"note_beginner": "a spray", "note_seasoned": "a knockdown"}
        b[FIG]["add"]["crop_rotation"] = {"note_beginner": "move it", "note_seasoned": "site it"}
        with _Patch("BACKFILL", b):
            self.assertIn("tier decrease", P.check(_pre()))

    def test_illegal_method_for_the_type_refused(self):
        """`bt` is caterpillar-scoped and beet/common-scab is bacterial."""
        b = copy.deepcopy(C.BACKFILL)
        b[BEET]["expect_after"] = ["even_watering", "lower_soil_ph", "crop_rotation", "bt"]
        b[BEET]["add"]["bt"] = {"note_beginner": "a", "note_seasoned": "b"}
        with _Patch("BACKFILL", b):
            self.assertIn("illegal for type", P.check(_pre()))

    def test_extra_rung_key_refused(self):
        b = copy.deepcopy(C.BACKFILL)
        b[FIG]["add"]["prompt_harvest"]["severity"] = "high"
        with _Patch("BACKFILL", b):
            self.assertIn("expected the note pair", P.check(_pre()))

    def test_identical_registers_refused(self):
        b = copy.deepcopy(C.BACKFILL)
        b[FIG]["add"]["prompt_harvest"]["note_seasoned"] = \
            b[FIG]["add"]["prompt_harvest"]["note_beginner"]
        with _Patch("BACKFILL", b):
            self.assertIn("identical registers", P.check(_pre()))

    def test_missing_note_refused(self):
        b = copy.deepcopy(C.BACKFILL)
        b[FIG]["add"]["prompt_harvest"]["note_seasoned"] = "   "
        with _Patch("BACKFILL", b):
            self.assertIn("missing note_seasoned", P.check(_pre()))

    def test_hygiene_violation_refused(self):
        b = copy.deepcopy(C.BACKFILL)
        b[FIG]["add"]["prompt_harvest"]["note_beginner"] = \
            "Picking promptly never lets the beetles in."
        with _Patch("BACKFILL", b):
            self.assertIn("copy hygiene", P.check(_pre()))

    def test_each_banned_shape_is_caught(self):
        for bad, frag in (("It never sours.", "absolute"),
                          ("Hold at 55 °F.", "spaced degF"),
                          ("Pick it -- then store it.", "double hyphen"),
                          ("A dash — here.", "em or en dash"),
                          ("Keep it **dry**.", "markdown"),
                          ("The colour is off.", "British"),
                          ("Cured bulbs are safe.", "bare safety claim")):
            got = P.hygiene(bad)
            self.assertIsNotNone(got, bad)
            self.assertIn(frag.split()[0].lower(), str(got).lower(), bad)

    def test_shipped_rung_prose_is_clean(self):
        for (slug, pid), spec in C.BACKFILL.items():
            for m, rung in spec["add"].items():
                for f in P.ADVICE_FIELDS:
                    self.assertIsNone(P.hygiene(rung[f]), f"{slug}/{pid}/{m}/{f}")

    def test_the_garlic_temperature_uses_a_degree_sign(self):
        """91 shipped rung notes carry temperature figures, so a figure is allowed here; a BARE F
        is not, and this is the one rung in the set that states one."""
        s = C.BACKFILL[("garlic", "fusarium-basal-rot")]["add"]["cure_and_store"]["note_seasoned"]
        self.assertIn("39°F", s)
        self.assertIsNone(P.hygiene(s))


class MainIsWiredToTheGuards(unittest.TestCase):
    def _fixture(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(promote_fixture.pre_state(P.BASE_SHA))
        return path

    def test_main_refuses_what_check_refuses(self):
        """The sabotage must be one ONLY `check` can see. A wrong rung count is ALSO caught by
        verify_post, so a driver using it passes even with the check() call cut out of main -- the
        harness proved exactly that. A falsified warrant is invisible to verify_post."""
        path = self._fixture()
        w = dict(C.WARRANTS)
        w[("beet", "common-scab", "lower_soil_ph")] = "apply elemental sulfur each spring"
        try:
            with _Patch("WARRANTS", w):
                with self.assertRaises(SystemExit) as cm:
                    _run_main(path)
            self.assertIn("is NOT in the record", str(cm.exception))
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)

    def test_main_refuses_what_verify_post_refuses(self):
        path = self._fixture()
        real = P.apply_to

        def wrapped(data):
            out = real(data)
            data["control_methods"]["prompt_harvest"]["tier"] = "physical"
            return out
        try:
            with _Patch("apply_to", wrapped, mod=P):
                with self.assertRaises(SystemExit) as cm:
                    _run_main(path)
            self.assertIn("control_methods changed", str(cm.exception))
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


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_post(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_the_two_r8_r9_methods_are_actually_used_now(self):
        """r8 minted `lower_soil_ph` and `cure_and_store` and r9 made `even_watering` reach
        `bacterial`. Until this promote each was legal and unused on these problems."""
        post = _post()
        used = {r["method"] for c in post["crops"] for f in ("pests", "diseases")
                for p in c.get(f) or [] if isinstance(p, dict)
                for r in p.get("control_ladder") or []}
        for m in ("lower_soil_ph", "cure_and_store"):
            self.assertIn(m, used)
        beet = P.find_problem(post, *BEET)
        self.assertIn("even_watering", [r["method"] for r in beet["control_ladder"]])

    def test_one_serializer(self):
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
