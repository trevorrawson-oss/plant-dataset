#!/usr/bin/env python3
"""Guard suite for tools/promote_row_cover_trap_precondition.py. Base c24d7754.

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are live is `MainWiringIsDriven`
plus tools/mutate_row_cover_trap_suite.py.

Every driver asserts the ONE message its branch emits. The colliding constants here are "expected"
(EDITS size AND crop count AND changed-leaf count) and "missing the precondition" (the clause guard
AND the coverage guard), so those are asserted as whole sentences.

THE CENTRAL TEST IS `PositiveControl`. A guard that merely fires when poked proves nothing about
whether it sees the real defect; today's batch-24 work turned up a copy detector that was
reachable, non-vacuous and 3/3 mutation-tested and still scored the real copy at 0.431. So this
suite asserts that on the UNMODIFIED pre-state the coverage guard fails for EXACTLY the ten
registers this promote fixes, named individually. If the real defect ever stops being detected,
that test goes red even though every branch still works.

`RegexBehaviour` exists because the first version of `PRIOR_CROP` used `brassica\\b`, which does not
match "brassicas", and it refused a clause that stated the condition perfectly well. A guard that
rejects correct input is as much a defect as one that accepts bad input, and neither a mutation nor
a branch driver would have caught it.
"""
import copy, difflib, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_row_cover_trap_precondition as P  # noqa: E402

POST_SHA = "f851dc15a75db4b08b6659e2a2ed06a628d2b34cf688b7a5965ad269ba0c6dab"
TOTAL_EDITS = 10
TOTAL_CROPS = 7
# The exact registers that are defective in the pre-state. Named individually, so a change in the
# defect population is a test failure rather than a silent drift.
PRE_STATE_DEFECTS = sorted([
    "kale/cabbage-root-maggot/note_beginner (needs condition AND consequence)",
    "broccoli/cabbage-root-maggot/note_beginner (needs condition AND consequence)",
    "broccoli/cabbage-root-maggot/note_seasoned (needs the prior-crop condition)",
    "bok-choy/cabbage-root-maggot/note_beginner (needs condition AND consequence)",
    "bok-choy/cabbage-root-maggot/note_seasoned (needs the prior-crop condition)",
    "cabbage/cabbage-root-maggot/note_beginner (needs condition AND consequence)",
    "kohlrabi/cabbage-root-maggot/note_beginner (needs condition AND consequence)",
    "kohlrabi/cabbage-root-maggot/note_seasoned (needs the prior-crop condition)",
    "brussels-sprouts/cabbage-root-maggot/note_beginner (needs condition AND consequence)",
    "collards/cabbage-root-maggot/note_beginner (needs condition AND consequence)",
])


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _applied():
    d = _pre()
    P.apply_to(d)
    return d


def _expect(case, sentence, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(sentence, str(cm.exception))


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


# ---------------------------------------------------------------- happy path
class CleanRun(unittest.TestCase):
    def test_pre_state_is_the_pinned_shape(self):
        self.assertEqual(hashlib.sha256(P.serialize(_pre())).hexdigest(), P.BASE_SHA)

    def test_apply_produces_the_pinned_post_sha(self):
        self.assertEqual(hashlib.sha256(P.serialize(_applied())).hexdigest(), POST_SHA)

    def test_counts_are_pinned_not_derived(self):
        self.assertEqual(len(P.EDITS), TOTAL_EDITS)
        self.assertEqual(len({k[0] for k in P.EDITS}), TOTAL_CROPS)
        self.assertEqual(P.EXPECTED_EDITS, TOTAL_EDITS)

    def test_serialize_is_compact_and_unescaped(self):
        self.assertEqual(P.serialize({"a": "café", "b": [1, 2]}),
                         '{"a":"café","b":[1,2]}'.encode("utf-8"))

    def test_every_edit_targets_a_known_row_cover_rung(self):
        for slug, pid, _f in P.EDITS:
            self.assertIn((slug, pid), P.ALL_ROW_COVER_RUNGS)

    def test_no_edit_touches_a_crop_that_was_already_correct(self):
        for slug, pid, _f in P.EDITS:
            self.assertNotIn((slug, pid), P.ALREADY_CORRECT)


# ---------------------------------------------------------------- THE CENTRAL TEST
class PositiveControl(unittest.TestCase):
    """Does the guard see the REAL defect, not just an injected one?"""

    def test_coverage_fails_on_the_untouched_pre_state(self):
        _expect(self, "still missing the precondition", lambda: P.check_coverage(_pre()))

    def test_it_names_exactly_the_ten_defective_registers(self):
        """If the defect population changes, this is a test failure rather than silent drift."""
        with self.assertRaises(SystemExit) as cm:
            P.check_coverage(_pre())
        msg = str(cm.exception)
        listed = sorted(json.loads(msg[msg.index("["):].replace("'", '"')))
        self.assertEqual(listed, PRE_STATE_DEFECTS)

    def test_coverage_passes_after_the_promote(self):
        self.assertEqual(P.check_coverage(_applied()), len(P.ALL_ROW_COVER_RUNGS))

    def test_the_four_correct_crops_already_pass_before_the_promote(self):
        """They are the reason the house pattern is known to be writable, and they must not be
        counted as defects."""
        d = _pre()
        for slug, pid in P.ALREADY_CORRECT:
            r = P.find_rung(d, slug, pid)
            self.assertTrue(P.has_precondition(r["note_beginner"]),
                            "%s beginner should already carry it" % slug)
            self.assertTrue(P.PRIOR_CROP.search(r["note_seasoned"]),
                            "%s seasoned should already name the condition" % slug)


class RegexBehaviour(unittest.TestCase):
    """The matcher is the measurement. It was wrong once and no branch driver would have shown it."""

    def test_prior_crop_matches_plural_forms(self):
        for t in ("a bed that carried brassicas last season",
                  "ground that grew cabbage-family crops last year",
                  "a previous crucifer crop", "an earlier cabbage-family crop",
                  "where alliums grew last year", "onions planted the previous year"):
            self.assertTrue(P.PRIOR_CROP.search(t), t)

    def test_prior_crop_matches_in_both_orders(self):
        self.assertTrue(P.PRIOR_CROP.search("carried brassicas last season"))
        self.assertTrue(P.PRIOR_CROP.search("last season's crucifer bed"))

    def test_prior_crop_does_not_match_a_bare_rotation_instruction(self):
        """"Rotate your beds" is not the warning: without naming the prior crop it gives the
        reader no way to tell whether this bed is the dangerous one."""
        self.assertFalse(P.PRIOR_CROP.search("Pair it with the rotation above."))
        self.assertFalse(P.PRIOR_CROP.search("ground that already carries the pest"))

    def test_enclosure_matches_the_house_phrasings(self):
        for t in ("flies can end up trapped under the cover", "it can seal emerging flies in",
                  "you seal them in with your turnips", "holds the emerging flies in with the crop",
                  "are caught inside the cover", "the fabric encloses the emerging adults",
                  "finish up inside the cover with the crop"):
            self.assertTrue(P.ENCLOSURE.search(t), t)

    def test_enclosure_does_not_match_a_bare_exclusion_claim(self):
        self.assertFalse(P.ENCLOSURE.search("keeps the fly from reaching the plants"))

    def test_has_precondition_requires_BOTH_halves(self):
        self.assertFalse(P.has_precondition("avoid ground that grew brassicas last year"))
        self.assertFalse(P.has_precondition("the cover can trap flies underneath it"))
        self.assertTrue(P.has_precondition(
            "avoid ground that grew brassicas last year, or the cover traps them with the crop"))


# ---------------------------------------------------------------- targets
class Targets(unittest.TestCase):
    def test_stale_pin_refuses(self):
        d = _pre()
        P.find_rung(d, "kale", "cabbage-root-maggot")["note_beginner"] = "something else entirely"
        _expect(self, "current text does not match its pin", lambda: P.check_targets(d))

    def test_edit_table_size_is_asserted(self):
        d = _pre()
        e = dict(P.EDITS)
        e.pop(("collards", "cabbage-root-maggot", "note_beginner"))
        with _Patch("EDITS", e):
            _expect(self, "EDITS holds 9 entries, expected 10", lambda: P.check_targets(d))

    def test_crop_count_is_asserted(self):
        d = _pre()
        e = {k: v for k, v in P.EDITS.items() if k[0] != "collards"}
        with _Patch("EDITS", e), _Patch("EXPECTED_EDITS", len(e)):
            _expect(self, "EDITS touches 6 crops, expected 7", lambda: P.check_targets(d))

    def test_a_target_outside_the_known_rungs_refuses(self):
        d = _pre()
        e = dict(P.EDITS)
        e[("beet", "aphids", "note_beginner")] = ("x", "xy")
        with _Patch("EDITS", e), _Patch("EXPECTED_EDITS", len(e)), \
                _Patch("EXPECTED_CROPS", 8):
            _expect(self, "is not a known row-cover rung", lambda: P.check_targets(d))

    def test_editing_an_already_correct_crop_refuses(self):
        d = _pre()
        r = P.find_rung(d, "radish", "cabbage-root-maggot")
        e = dict(P.EDITS)
        e[("radish", "cabbage-root-maggot", "note_beginner")] = (r["note_beginner"],
                                                                 r["note_beginner"] + " More.")
        with _Patch("EDITS", e), _Patch("EXPECTED_EDITS", len(e)), _Patch("EXPECTED_CROPS", 8):
            _expect(self, "already carries the precondition and must not be edited",
                    lambda: P.check_targets(d))

    def test_missing_crop_refuses(self):
        d = _pre()
        d["crops"] = [c for c in d["crops"] if c.get("slug") != "kale"]
        _expect(self, "crop kale is not on the roster", lambda: P.check_targets(d))

    def test_missing_rung_refuses(self):
        d = _pre()
        for fam in ("pests", "diseases"):
            for p in P.by_slug(d)["kale"].get(fam) or []:
                if p.get("id") == "cabbage-root-maggot":
                    p["control_ladder"] = [r for r in p["control_ladder"]
                                           if r["method"] != "floating_row_cover"]
        _expect(self, "has no floating_row_cover rung", lambda: P.check_targets(d))


class OnlyAdds(unittest.TestCase):
    """The promote is structurally incapable of rewriting shipped prose."""

    def test_a_replacement_that_does_not_extend_the_original_refuses(self):
        d = _pre()
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        before, after = P.EDITS[k]
        e = dict(P.EDITS)
        e[k] = (before, "A completely rewritten note that grew brassicas last year and traps them.")
        with _Patch("EDITS", e):
            _expect(self, "may only APPEND a clause", lambda: P.check_only_adds(d))

    def test_a_replacement_that_adds_nothing_refuses(self):
        d = _pre()
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        before, _after = P.EDITS[k]
        e = dict(P.EDITS)
        e[k] = (before, before)
        with _Patch("EDITS", e):
            _expect(self, "replacement adds nothing", lambda: P.check_only_adds(d))

    def test_every_shipped_original_survives_verbatim_as_a_prefix(self):
        d = _applied()
        for (slug, pid, field), (before, _after) in P.EDITS.items():
            self.assertTrue(P.find_rung(d, slug, pid)[field].startswith(before))


class Clauses(unittest.TestCase):
    def test_a_clause_missing_the_precondition_refuses(self):
        d = _pre()
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        before, _a = P.EDITS[k]
        e = dict(P.EDITS)
        e[k] = (before, before + " Seal the edges well.")
        with _Patch("EDITS", e):
            _expect(self, "does not state BOTH the prior-crop condition and the enclosure "
                          "consequence", lambda: P.check_clauses(d))

    def test_a_clause_with_only_the_condition_refuses(self):
        d = _pre()
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        before, _a = P.EDITS[k]
        e = dict(P.EDITS)
        e[k] = (before, before + " Avoid ground that grew brassicas last year.")
        with _Patch("EDITS", e):
            _expect(self, "does not state BOTH the prior-crop condition and the enclosure "
                          "consequence", lambda: P.check_clauses(d))

    def test_an_em_dash_refuses(self):
        d = _pre()
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        before, _a = P.EDITS[k]
        e = dict(P.EDITS)
        e[k] = (before, before + " Avoid brassica ground from last year — it traps them in.")
        with _Patch("EDITS", e):
            _expect(self, "em/en dash", lambda: P.check_clauses(d))

    def test_an_absolute_refuses(self):
        d = _pre()
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        before, _a = P.EDITS[k]
        e = dict(P.EDITS)
        e[k] = (before, before + " This completely stops them; brassicas last year trap them in.")
        with _Patch("EDITS", e):
            _expect(self, "absolute:completely", lambda: P.check_clauses(d))

    def test_british_usage_refuses(self):
        d = _pre()
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        before, _a = P.EDITS[k]
        e = dict(P.EDITS)
        e[k] = (before, before + " Bin the cover where brassicas grew last year or it traps them.")
        with _Patch("EDITS", e):
            _expect(self, "british:bin", lambda: P.check_clauses(d))

    def test_ladder_vocabulary_refuses(self):
        d = _pre()
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        before, _a = P.EDITS[k]
        e = dict(P.EDITS)
        e[k] = (before, before + " Pair it with the rotation rung; brassicas last year trap them.")
        with _Patch("EDITS", e):
            _expect(self, "ladder vocabulary", lambda: P.check_clauses(d))

    def test_two_near_identical_clauses_refuse(self):
        d = _pre()
        ka = ("kale", "cabbage-root-maggot", "note_beginner")
        cb = ("cabbage", "cabbage-root-maggot", "note_beginner")
        e = dict(P.EDITS)
        shared = (" Lay it on a bed that did not grow cabbage-family crops last year, or the "
                  "emerging flies are held in with the crop.")
        e[ka] = (P.EDITS[ka][0], P.EDITS[ka][0] + shared)
        e[cb] = (P.EDITS[cb][0], P.EDITS[cb][0] + shared)
        with _Patch("EDITS", e):
            _expect(self, "similar; write them independently", lambda: P.check_clauses(d))

    def test_anti_vacuity_branch(self):
        d = _pre()
        with _Patch("EDITS", {}):
            _expect(self, "no clauses were compared; this guard is vacuous",
                    lambda: P.check_clauses(d))

    def test_the_similarity_ceiling_is_pinned(self):
        """The threshold is a DECISION, not an implementation detail. Loosening it silently is
        indistinguishable from removing the guard, and asserting only that the real clauses sit
        under it cannot notice: they sit under a loosened one too."""
        self.assertEqual(P.CLAUSE_SIMILARITY_CEILING, 0.70)

    def test_a_realistic_paraphrase_is_refused_not_just_an_exact_copy(self):
        """The duplicate driver injected two IDENTICAL clauses, which score 1.000 and are refused
        by any ceiling short of 1. That is why loosening the ceiling to 0.99 survived the harness.
        A paraphrase at 0.859 is the shape a real template twin takes, and it separates a 0.70
        ceiling from a 0.99 one."""
        d = _pre()
        ka = ("kale", "cabbage-root-maggot", "note_beginner")
        cb = ("cabbage", "cabbage-root-maggot", "note_beginner")
        e = dict(P.EDITS)
        e[ka] = (P.EDITS[ka][0], P.EDITS[ka][0] + " Lay it on a bed that did not grow "
                 "cabbage-family crops last year, since the flies emerging from that soil are held "
                 "in under the cover with the crop.")
        e[cb] = (P.EDITS[cb][0], P.EDITS[cb][0] + " Lay it on a bed that has not grown "
                 "cabbage-family crops recently, since the flies coming out of that soil are held "
                 "in beneath the cover with the crop.")
        with _Patch("EDITS", e):
            _expect(self, "similar; write them independently", lambda: P.check_clauses(d))

    def test_the_metric_disables_autojunk(self):
        """difflib's autojunk engages at 200 characters and deflates any long pair. The shipped
        clauses are 141 to 162 characters, so the current data cannot exercise it and removing
        `autojunk=False` changes nothing -- which is exactly why the mutation survived. This pair
        is 226 and 244 characters and scores 0.494 with autojunk on, 0.834 with it off. Only the
        corrected metric refuses it."""
        d = _pre()
        shared = ("the overwintering pupae are already sitting in that soil, and a sealed cover "
                  "then holds the flies that emerge from them in with the crop instead of keeping "
                  "them off it")
        ka = ("kale", "cabbage-root-maggot", "note_beginner")
        cb = ("cabbage", "cabbage-root-maggot", "note_beginner")
        e = dict(P.EDITS)
        e[ka] = (P.EDITS[ka][0], P.EDITS[ka][0] + " Use it only on ground rotated off "
                 "cabbage-family crops last season, because " + shared + ".")
        e[cb] = (P.EDITS[cb][0], P.EDITS[cb][0] + " Leave the cover off where brassicas grew last "
                 "year, since " + shared + ".")
        with _Patch("EDITS", e):
            _expect(self, "similar; write them independently", lambda: P.check_clauses(d))

    def test_the_real_clauses_clear_the_ceiling_with_headroom(self):
        """Recorded so a later edit that crowds the ceiling fails as a measurement change."""
        worst = P.check_clauses(_pre())
        self.assertLess(worst[0], P.CLAUSE_SIMILARITY_CEILING)
        self.assertAlmostEqual(worst[0], 0.657, places=3)


class Coverage(unittest.TestCase):
    def test_a_beginner_register_missing_the_consequence_refuses(self):
        d = _applied()
        r = P.find_rung(d, "collards", "cabbage-root-maggot")
        r["note_beginner"] = "Cover the bed. Avoid ground that grew brassicas last year."
        _expect(self, "collards/cabbage-root-maggot/note_beginner (needs condition AND "
                      "consequence)", lambda: P.check_coverage(d))

    def test_a_seasoned_register_missing_the_condition_refuses(self):
        d = _applied()
        P.find_rung(d, "cabbage", "cabbage-root-maggot")["note_seasoned"] = "Seal the edges."
        _expect(self, "cabbage/cabbage-root-maggot/note_seasoned (needs the prior-crop condition)",
                lambda: P.check_coverage(d))

    def test_an_already_correct_crop_regressing_is_caught(self):
        """The four crops this promote does not touch are still in the denominator."""
        d = _applied()
        P.find_rung(d, "radish", "cabbage-root-maggot")["note_beginner"] = "Cover the bed."
        _expect(self, "radish/cabbage-root-maggot/note_beginner", lambda: P.check_coverage(d))

    def test_the_denominator_is_all_eleven_rungs(self):
        self.assertEqual(len(P.ALL_ROW_COVER_RUNGS), 11)
        self.assertEqual(len(set(P.ALL_ROW_COVER_RUNGS)), 11)


class BlastRadius(unittest.TestCase):
    def test_clean_apply_changes_exactly_ten_leaves(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        self.assertEqual(P.verify_post(pre, d), TOTAL_EDITS)

    def test_an_added_key_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_rung(d, "kale", "cabbage-root-maggot")["extra"] = "x"
        _expect(self, "leaf keys added", lambda: P.verify_post(pre, d))

    def test_a_dropped_key_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        del P.find_rung(d, "kale", "cabbage-root-maggot")["method"]
        _expect(self, "leaf keys dropped", lambda: P.verify_post(pre, d))

    def test_an_extra_changed_leaf_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.by_slug(d)["beet"]["name"] = "Beetroot"
        _expect(self, "11 leaves changed, expected 10", lambda: P.verify_post(pre, d))

    def test_a_changed_leaf_outside_a_register_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        # revert one edit and change a non-register leaf instead, keeping the count at 10
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        P.find_rung(d, *k[:2])[k[2]] = P.EDITS[k][0]
        P.by_slug(d)["beet"]["name"] = "Beetroot"
        _expect(self, "changed a leaf outside a rung register", lambda: P.verify_post(pre, d))

    def test_a_replacement_not_actually_applied_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        P.find_rung(d, *k[:2])[k[2]] = P.EDITS[k][0] + " Different brassicas last year text traps."
        _expect(self, "did not receive its replacement", lambda: P.verify_post(pre, d))

    def test_the_right_count_on_the_WRONG_crops_refuses(self):
        """The distinct failure the crop-set check exists for: ten registers changed, but not the
        ten this promote pins. It is only reachable because the check sits ahead of the per-edit
        application check; behind it, the substitution fires first and this branch is dead."""
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        k = ("kale", "cabbage-root-maggot", "note_beginner")
        P.find_rung(d, *k[:2])[k[2]] = P.EDITS[k][0]          # revert kale
        r = P.find_rung(d, "radish", "cabbage-root-maggot")   # ...and touch a crop not in EDITS
        r["note_beginner"] = r["note_beginner"] + " An extra sentence."
        _expect(self, "touched crops", lambda: P.verify_post(pre, d))

    def test_set_equality_is_compared_before_any_value(self):
        import inspect
        src = inspect.getsource(P.verify_post)
        self.assertLess(src.index("added, dropped = set(post) - set(pre)"),
                        src.index("changed = sorted"))

    def test_snapshot_covers_the_catalogs_too(self):
        snap = P.snapshot(_pre())
        self.assertTrue(any(k[0] == "control_methods" for k in snap))
        self.assertTrue(any(k[0] == "source_catalog" for k in snap))


class CatalogUntouched(unittest.TestCase):
    def setUp(self):
        d = _pre()
        self.cm = P.serialize(d["control_methods"])
        self.sc = P.serialize(d["source_catalog"])

    def test_control_methods_change_refuses(self):
        d = _pre()
        d["control_methods"]["crop_rotation"]["tier"] = "physical"
        _expect(self, "control_methods changed; this promote mints nothing",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_source_catalog_change_refuses(self):
        d = _pre()
        d["source_catalog"][sorted(d["source_catalog"])[0]]["name"] = "changed"
        _expect(self, "source_catalog changed; this promote adds no source",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_the_real_promote_touches_neither(self):
        P.check_catalog_untouched(self.cm, self.sc, _applied())


class MainWiringIsDriven(unittest.TestCase):
    """RECURRED at catalog r8: 53 green tests and main() never called check()."""

    def test_apply_to_routes_through_every_pre_check(self):
        import inspect
        src = inspect.getsource(P.apply_to)
        for g in ("check_targets", "check_only_adds", "check_clauses"):
            self.assertIn(g + "(", src, "%s is never reached from apply_to()" % g)

    def test_main_runs_verify_post_coverage_and_the_catalog_check(self):
        import inspect
        src = inspect.getsource(P.main)
        for frag in ("verify_post(pre, data)", "check_catalog_untouched(before_cm, before_sc, data)",
                     "check_coverage(data)", "if sha != expect:"):
            self.assertIn(frag, src)

    def test_end_to_end_through_main(self):
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(promote_fixture.pre_state(P.BASE_SHA))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, path], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("post  SHA           : " + POST_SHA, r.stdout)
            self.assertIn("registers corrected : 10 across 7 crops", r.stdout)
            self.assertIn("11/11 row-cover rungs", r.stdout)
        finally:
            os.unlink(path)

    def test_a_wrong_base_sha_is_refused(self):
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(P.serialize({"crops": [], "control_methods": {}, "source_catalog": {}}))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, path], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("REFUSED: base SHA", r.stdout + r.stderr)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main(verbosity=1)
