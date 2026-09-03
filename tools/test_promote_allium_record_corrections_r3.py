#!/usr/bin/env python3
"""Guard suite for tools/promote_allium_record_corrections_r3.py. Base 50ffedb0 (r2's output).

REPLAY-PINNED via CHAIN until r2 commits. Evidence the guards are live: `MainWiringIsDriven` plus
tools/mutate_allium_record_corrections_r3_suite.py.

`PositiveControl` asserts every retired-claim LABEL is present on at least one target in the
pre-state, and PINS the (target, label) pairs that are refusal-spec, present on no target, so the
list of what is measured versus what is merely refused is written down rather than implied.
`MatcherBehaviour` asserts every predicate in both directions, including on the promote's own
replacements. Two checks in verify_post are FORWARD assertions (the rung count and the
duplicate-method scan cannot be reached past the key-set and rung-leaf-count checks); the suite
asserts that masking so a future edit that makes them reachable is noticed.
"""
import hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_allium_record_corrections_r3 as P  # noqa: E402

POST_SHA = "9d2031ff5ba3abd7a61fe6f0d02715b67d3d0f880cb9d89c0f1729e52df48e8b"
MAG, PINK, BOT = P.MAGGOT, P.PINK, "Botrytis (leaf blight and neck rot)"

# (crop, name, label) pairs whose retired claim is present on NO field of that target in the
# pre-state. The guard scanning them is a REFUSAL SPEC there, not a measurement. Pinned so a
# change in the pre-state (or in the table) shows up as a red test rather than a silent shift.
REFUSAL_SPEC = {
    ("chives", MAG, "the unsourced emergence timing"), ("garlic", MAG, "the unsourced emergence timing"),
    ("chives", MAG, "the debris carryover mechanism"),
    ("chives", MAG, "the false-attribution device"), ("leek", MAG, "the false-attribution device"),
    ("onion", MAG, "the false-attribution device"), ("shallot", MAG, "the false-attribution device"),
    ("garlic", MAG, "the false-attribution device"),
}


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
    def __init__(self, n, v):
        self.n, self.v = n, v

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)

    def __exit__(self, *e):
        setattr(P, self.n, self.old)
        return False


class CleanRun(unittest.TestCase):
    def test_pre_state_is_the_pinned_shape(self):
        self.assertEqual(hashlib.sha256(P.serialize(_pre())).hexdigest(), P.BASE_SHA)

    def test_apply_produces_the_pinned_post_sha(self):
        self.assertEqual(hashlib.sha256(P.serialize(_applied())).hexdigest(), POST_SHA)

    def test_counts_are_pinned(self):
        self.assertEqual((len(P.PROSE), len(P.RUNG_NOTES), len(P.SEVERITY), len(P.SOURCES)),
                         (42, 7, 1, 11))
        self.assertEqual((P.EXPECTED_PROSE, P.EXPECTED_RUNG_NOTES, P.EXPECTED_SEVERITY,
                          P.EXPECTED_SOURCE_SETS), (42, 7, 1, 11))
        self.assertEqual(len(P.TARGETS), 11)
        self.assertEqual(len(P.RETIRED), 30)
        self.assertEqual(sum(len(f) for _t, f, _p, _l in P.REQUIRED), 40)
        self.assertEqual(len(P.RETIRED_URLS), 5)

    def test_the_roster_shape_is_unchanged(self):
        a, b = _pre(), _applied()
        self.assertEqual(len(a["crops"]), 128)
        self.assertEqual(len(a["crops"]), len(b["crops"]))
        self.assertEqual(sum(len(P.problems(c)) for c in b["crops"]), 912)
        self.assertEqual(P.rung_count(a), 3243)
        self.assertEqual(P.rung_count(b), 3243)

    def test_shipped_ladders_keep_their_method_order(self):
        a, b = _pre(), _applied()
        for slug, name in P.SHIPPED:
            self.assertEqual([r["method"] for r in P.find_problem(a, slug, name)["control_ladder"]],
                             [r["method"] for r in P.find_problem(b, slug, name)["control_ladder"]])

    def test_unshipped_targets_stay_id_less_and_ladder_less(self):
        b = _applied()
        for slug, name in P.TARGETS:
            if (slug, name) in P.SHIPPED:
                continue
            p = P.find_problem(b, slug, name)
            self.assertIsNone(p.get("id"))
            self.assertIsNone(p.get("control_ladder"))

    def test_names_are_untouched(self):
        a, b = _pre(), _applied()
        for c in a["crops"]:
            self.assertEqual([p.get("name") for p in P.problems(c)],
                             [p.get("name") for p in P.problems(P.by_slug(b)[c["slug"]])])

    def test_only_leek_pink_root_severity_moves(self):
        a, b = _pre(), _applied()
        for c in a["crops"]:
            for pa, pb in zip(P.problems(c), P.problems(P.by_slug(b)[c["slug"]])):
                if (c["slug"], pa.get("name")) == ("leek", PINK):
                    self.assertEqual((pa.get("severity"), pb.get("severity")), ("medium", "low"))
                else:
                    self.assertEqual(pa.get("severity"), pb.get("severity"))


class PositiveControl(unittest.TestCase):
    def test_every_retired_label_is_present_on_some_target_in_the_pre_state(self):
        d = _pre()
        present = {}
        for (slug, name), fn, label in P.RETIRED:
            p = P.find_problem(d, slug, name)
            hit = any(fn(v) for _w, v in P.strings_of(p))
            present.setdefault(label, False)
            present[label] = present[label] or hit
            if not hit:
                self.assertIn((slug, name, label), REFUSAL_SPEC,
                              "%s/%s: %s is absent in the pre-state and not pinned as refusal-spec"
                              % (slug, name, label))
            else:
                self.assertNotIn((slug, name, label), REFUSAL_SPEC,
                                 "%s/%s: %s is pinned refusal-spec but IS present" % (slug, name, label))
        self.assertTrue(all(present.values()), present)
        self.assertEqual(len(REFUSAL_SPEC), 8)

    def test_every_required_claim_is_absent_from_every_declared_register_in_the_pre_state(self):
        d = _pre()
        for (slug, name), fields, pat, label in P.REQUIRED:
            p = P.find_problem(d, slug, name)
            for f in fields:
                self.assertIsNone(pat.search(p.get(f) or ""),
                                  "%s/%s/%s already carried %s" % (slug, name, f, label))

    def test_the_guards_fail_on_the_pre_state_and_pass_after(self):
        _expect(self, "still carries", lambda: P.check_retired_claims(_pre()))
        _expect(self, "lacks", lambda: P.check_required_claims(_pre()))
        _expect(self, "retired anchors survive", lambda: P.check_urls_retired(_pre()))
        _expect(self, "chives/Onion maggot anchors umn_ext at "
                      "'https://extension.umn.edu/vegetables/growing-onions'",
                lambda: P.check_maggot_anchors_uniform(_pre()))
        b = _applied()
        self.assertEqual(P.check_retired_claims(b), 30)
        self.assertEqual(P.check_required_claims(b), 40)
        self.assertEqual(P.check_urls_retired(b), 5)
        self.assertEqual(P.check_maggot_anchors_uniform(b), 12)

    def test_survivor_phrases_exist_before_and_after(self):
        self.assertEqual(P.check_survivors(_pre()), 3)
        self.assertEqual(P.check_survivors(_applied()), 3)

    def test_the_shipped_rung_notes_really_carry_the_defects(self):
        d = _pre()
        r = P.find_rung(d, "spring-onion", MAG, "floating_row_cover")
        self.assertIn("Cover at emergence, which is the window the guidance points at",
                      r["note_seasoned"])
        self.assertIn("rotation rung", r["note_seasoned"])
        self.assertIn("Residue is the carryover reservoir the guidance names",
                      P.find_rung(d, "spring-onion", MAG, "garden_sanitation")["note_seasoned"])
        self.assertIn("carry over in allium residue",
                      P.find_rung(d, "spring-onion", MAG, "crop_rotation")["note_seasoned"])
        self.assertIn("Removing crop residue and cull bulbs",
                      P.find_rung(d, "garlic", MAG, "garden_sanitation")["note_seasoned"])


class MatcherBehaviour(unittest.TestCase):
    def _fn(self, label, crop="leek", name=MAG):
        hits = [fn for (s, n), fn, lab in P.RETIRED if lab == label and (s, n) == (crop, name)]
        self.assertEqual(len(hits), 1, label)
        return hits[0]

    def test_residue_pattern(self):
        fn = self._fn("the residue carryover mechanism")
        for t in ("remove cull bulbs and crop residue", "carry over in allium residue",
                  "Till under infested crop residues promptly"):
            self.assertTrue(fn(t), t)
        for t in ("the pupae overwinter in the soil around last season's alliums",
                  "residents of the bed", "old bulbs and rotting garden waste draw it in"):
            self.assertFalse(fn(t), t)

    def test_emergence_pattern(self):
        fn = self._fn("the unsourced emergence timing")
        for t in ("use floating row cover at emergence to block egg-laying",
                  "floating row cover at establishment to block", "Cover at emergence, which"):
            self.assertTrue(fn(t), t)
        for t in ("from planting day, before the spring flight", "before the moths emerge",
                  "as soon as you sow, so it is in place before the flies are out"):
            self.assertFalse(fn(t), t)

    def test_debris_carryover_pattern(self):
        fn = self._fn("the debris carryover mechanism", "garlic")
        for t in ("where allium debris carries the pest over",
                  "The problem carries over in old onion material", "carry over in leftover debris",
                  "populations carry over in allium residue", "carries over in old onion scraps"):
            self.assertTrue(fn(t), t)
        for t in ("on ground that carried alliums the year before",
                  "The fly spends the winter in the soil where onions grew",
                  # garlic's SHIPPED rotation note: the correct mechanism, must pass
                  "Populations carry over in allium ground, so rotating garlic off beds"):
            self.assertFalse(fn(t), t)

    def test_false_attribution_pattern(self):
        fn = self._fn("the false-attribution device", "spring-onion")
        for t in ("the window the guidance points at", "the reservoir the guidance names",
                  "onion's guidance asks for rotation"):
            self.assertTrue(fn(t), t)
        for t in ("treat persistent outbreaks per local extension guidance",
                  "ask your local extension office"):
            self.assertFalse(fn(t), t)

    def test_clean_stock_pattern(self):
        fn = self._fn("the clean-stock claim", "onion", PINK)
        for t in ("start with clean, disease-free transplants", "start with clean healthy transplants",
                  "clean sets"):
            self.assertTrue(fn(t), t)
        for t in ("clear out old bulbs", "cleanup at the end of the season",
                  "keep the plants well cared for"):
            self.assertFalse(fn(t), t)

    def test_botrytis_patterns(self):
        sen = self._fn("in-season senescing-leaf removal", "chives", BOT)
        gray = self._fn("the neck-rot gray-mold symptom", "chives", BOT)
        splash = self._fn("the splash-dispersal mechanism", "chives", BOT)
        self.assertTrue(sen("remove senescing debris"))
        self.assertFalse(sen("clear dead foliage and debris at the end of the season"))
        for t in ("sometimes with a gray fuzzy mold", "sometimes with gray sporulation",
                  "Botrytis is a gray-mold fungus"):
            self.assertTrue(gray(t), t)
        self.assertFalse(gray("small white sunken oval spots with a light green halo"))
        self.assertTrue(splash("splashing water and leaf wetness spread the spores"))
        self.assertFalse(splash("its spores are airborne"))

    def test_required_patterns_in_both_directions(self):
        pats = {}
        for _t, _f, pat, label in P.REQUIRED:
            pats.setdefault(label, pat)
        trap = pats["the row-cover trap precondition"]
        for t in ("Do not cover a bed that grew alliums last year, or you seal",
                  "Do not cover a bed that grew leeks or onions last year",
                  "but not over ground that grew onions or their relatives last year",
                  "from planting, on ground that did not carry alliums last year"):
            self.assertTrue(trap.search(t), t)
        for t in ("cover young plants with row-cover fabric so the fly cannot lay eggs",
                  "Do not plant onions in the same place each year"):
            self.assertIsNone(trap.search(t), t)
        cav = pats["the rotation caveat"]
        for t in ("knowing that rotation reduces the disease rather than clearing it",
                  "Rotation helps but does not clear the fungus"):
            self.assertTrue(cav.search(t), t)
        for t in ("Rotate away from alliums for several years", "rotation is not highly effective"):
            self.assertIsNone(cav.search(t), t)
        res = pats["resistant varieties as the lead onion control"]
        self.assertTrue(res.search("Resistant varieties are the best control"))
        self.assertTrue(res.search("a variety sold as resistant to pink root"))
        self.assertIsNone(res.search("keep the plants well cared for"))
        wet = pats["the 20-hour leaf-wetness figure"]
        self.assertTrue(wet.search("Leaves need 20 or more hours of wetness"))
        self.assertTrue(wet.search("leaf wetness lasts 20 hours or more"))
        self.assertIsNone(wet.search("20 minutes of wetness"))
        soil = pats["the soil overwintering mechanism"]
        self.assertTrue(soil.search("the pupae overwinter in the soil around"))
        self.assertIsNone(soil.search("populations carry over in allium residue"))
        org = pats["the organic-matter attraction"]
        self.assertTrue(org.search("keep spring manure and green manure out of the bed"))
        self.assertTrue(org.search("Rotting organic matter draws egg-laying"))
        self.assertIsNone(org.search("old plant debris"))

    def test_hygiene_catches_the_shipped_note_defects_and_passes_replacements(self):
        self.assertIn("ladder vocabulary", P.hygiene("Pair it with the rotation rung"))
        self.assertIn("false-attribution device", P.hygiene("the window the guidance points at"))
        self.assertIn("british:\\bautumn\\b", P.hygiene("in autumn"))
        self.assertIn("absolute:never", P.hygiene("never cover"))
        for table in (P.PROSE, P.RUNG_NOTES):
            for k, (_b, after) in table.items():
                self.assertEqual(P.hygiene(after), [], k)
        for (slug, name, *_rest), (_b, after) in list(P.PROSE.items()) + list(P.RUNG_NOTES.items()):
            for (ts, tn), fn, label in P.RETIRED:
                if (ts, tn) == (slug, name):
                    self.assertFalse(fn(after), "%s/%s trips %r: %s" % (slug, name, label, after[:60]))


class Pins(unittest.TestCase):
    def test_stale_prose_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "onion", PINK)["cause_seasoned"] = "moved on"
        _expect(self, "onion/Pink root/cause_seasoned does not match its pinned text; the record moved",
                lambda: P.check_pins(d))

    def test_stale_rung_note_pin_refuses(self):
        d = _pre()
        P.find_rung(d, "garlic", MAG, "garden_sanitation")["note_seasoned"] = "moved on"
        _expect(self, "garlic/Onion maggot/garden_sanitation/note_seasoned does not match its pinned "
                      "note; the rung moved", lambda: P.check_pins(d))

    def test_a_rung_note_on_an_unshipped_target_refuses(self):
        d = _pre()
        rn = dict(P.RUNG_NOTES)
        rn[("leek", MAG, "crop_rotation", "note_beginner")] = ("x", "y")
        with _Patch("RUNG_NOTES", rn), _Patch("EXPECTED_RUNG_NOTES", len(rn)):
            _expect(self, "leek/Onion maggot is not a shipped target; it has no rungs to edit",
                    lambda: P.check_pins(d))

    def test_a_missing_rung_method_refuses(self):
        d = _pre()
        rn = dict(P.RUNG_NOTES)
        rn[("garlic", MAG, "handpick", "note_beginner")] = ("x", "y")
        with _Patch("RUNG_NOTES", rn), _Patch("EXPECTED_RUNG_NOTES", len(rn)):
            _expect(self, "garlic/Onion maggot carries 0 rungs for 'handpick', expected exactly 1",
                    lambda: P.check_pins(d))

    def test_an_unshipped_target_that_already_carries_an_id_refuses(self):
        """batch 24 must land AFTER this promote, never before."""
        d = _pre()
        P.find_problem(d, "leek", PINK)["id"] = "pink-root"
        _expect(self, "leek/Pink root already carries a ladder or id; this promote must land BEFORE "
                      "batch 24", lambda: P.check_pins(d))

    def test_a_shipped_target_without_a_ladder_refuses(self):
        d = _pre()
        P.find_problem(d, "garlic", MAG)["control_ladder"] = []
        _expect(self, "garlic/Onion maggot is declared shipped but carries no ladder or id",
                lambda: P.check_pins(d))

    def test_a_target_outside_the_declared_set_refuses(self):
        d = _pre()
        pr = dict(P.PROSE)
        pr[("leek", "Leek rust", "cause_beginner")] = ("x", "y")
        with _Patch("PROSE", pr), _Patch("EXPECTED_PROSE", len(pr)):
            _expect(self, "leek/Leek rust is not a declared target", lambda: P.check_pins(d))

    def test_table_sizes_are_asserted(self):
        d = _pre()
        with _Patch("EXPECTED_PROSE", 35):
            _expect(self, "edit tables hold 42/7/1/11, expected 35/7/1/11", lambda: P.check_pins(d))

    def test_an_identical_replacement_refuses(self):
        d = _pre()
        k = ("onion", PINK, "cause_seasoned")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][0])
        with _Patch("PROSE", pr):
            _expect(self, "onion/Pink root/cause_seasoned replacement is identical",
                    lambda: P.check_pins(d))

    def test_hygiene_on_a_replacement_refuses(self):
        d = _pre()
        k = ("onion", PINK, "cause_seasoned")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][1] + " Rotation completely clears it.")
        with _Patch("PROSE", pr):
            _expect(self, "onion/Pink root/cause_seasoned replacement: absolute:completely",
                    lambda: P.check_pins(d))

    def test_ladder_vocabulary_in_a_rung_note_replacement_refuses(self):
        d = _pre()
        k = ("spring-onion", MAG, "crop_rotation", "note_seasoned")
        rn = dict(P.RUNG_NOTES)
        rn[k] = (P.RUNG_NOTES[k][0], P.RUNG_NOTES[k][1] + " Pair it with the sanitation rung.")
        with _Patch("RUNG_NOTES", rn):
            _expect(self, "spring-onion/Onion maggot/crop_rotation/note_seasoned replacement: ladder "
                          "vocabulary", lambda: P.check_pins(d))

    def test_a_stale_severity_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "leek", PINK)["severity"] = "high"
        _expect(self, "leek/Pink root severity is 'high', pinned 'medium'", lambda: P.check_pins(d))

    def test_an_unknown_new_severity_refuses(self):
        d = _pre()
        with _Patch("SEVERITY", {("leek", PINK): ("medium", "none")}):
            _expect(self, "leek/Pink root new severity 'none' is not a known value",
                    lambda: P.check_pins(d))

    def test_a_stale_source_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "onion", PINK)["sources"] = ["uc_ipm"]
        _expect(self, "onion/Pink root sources are ['uc_ipm'], pinned ['tamu_agrilife']",
                lambda: P.check_pins(d))

    def test_citing_an_id_not_in_the_catalog_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("onion", PINK)] = (["tamu_agrilife"], ["uc_ipm", "nmsu_pinkroot"],
                                {"uc_ipm": "https://x", "nmsu_pinkroot": "https://y"})
        with _Patch("SOURCES", src):
            _expect(self, "onion/Pink root cites 'nmsu_pinkroot', which is not in source_catalog",
                    lambda: P.check_pins(d))

    def test_an_anchor_outside_the_new_source_list_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("onion", PINK)] = (["tamu_agrilife"], ["uc_ipm", "usu_ext"],
                                {"uc_ipm": "https://x", "usu_ext": "https://y", "nmsu_ext": "https://z"})
        with _Patch("SOURCES", src):
            _expect(self, "onion/Pink root anchors 'nmsu_ext' which is not in its new source list",
                    lambda: P.check_pins(d))

    def test_a_cited_id_without_any_anchor_refuses(self):
        """garlic keeps usu_ext's EXISTING anchor; strip it from the pre-state and the kept id has
        nothing to point at."""
        d = _pre()
        P.find_problem(d, "garlic", MAG)["anchoring_urls"].pop("usu_ext")
        _expect(self, "garlic/Onion maggot cites 'usu_ext' without a document anchor",
                lambda: P.check_pins(d))

    def test_a_declared_target_with_no_edit_refuses(self):
        d = _pre()
        src = {k: v for k, v in P.SOURCES.items() if k != ("chives", "Rust")}
        with _Patch("SOURCES", src), _Patch("EXPECTED_SOURCE_SETS", len(src)):
            _expect(self, "chives/Rust is declared but receives no edit", lambda: P.check_pins(d))

    def test_an_ambiguous_problem_name_refuses(self):
        d = _pre()
        P.by_slug(d)["onion"]["diseases"].append({"name": "Pink root"})
        _expect(self, "onion has 2 problems named 'Pink root', expected exactly 1",
                lambda: P.check_pins(d))


class RetiredClaimsPerBranch(unittest.TestCase):
    def _re(self, slug, name, field, text):
        d = _applied()
        P.find_problem(d, slug, name)[field] = text
        return d

    def test_residue_coming_back(self):
        d = self._re("onion", MAG, "cause_beginner", "They survive in crop residue.")
        _expect(self, "onion/Onion maggot/cause_beginner still carries the residue carryover mechanism",
                lambda: P.check_retired_claims(d))

    def test_emergence_timing_coming_back(self):
        d = self._re("shallot", MAG, "management_beginner", "Cover at emergence.")
        _expect(self, "shallot/Onion maggot/management_beginner still carries the unsourced emergence "
                      "timing", lambda: P.check_retired_claims(d))

    def test_debris_carryover_coming_back(self):
        d = self._re("garlic", MAG, "identification_beginner", "Where allium debris carries the pest over.")
        _expect(self, "garlic/Onion maggot/identification_beginner still carries the debris carryover "
                      "mechanism", lambda: P.check_retired_claims(d))

    def test_the_device_coming_back_in_a_RUNG_NOTE(self):
        d = _applied()
        P.find_rung(d, "spring-onion", MAG, "crop_rotation")["note_beginner"] = \
            "Rotate, as the guidance names."
        _expect(self, "spring-onion/Onion maggot/crop_rotation/note_beginner still carries the "
                      "false-attribution device", lambda: P.check_retired_claims(d))

    def test_clean_stock_coming_back(self):
        d = self._re("leek", PINK, "management_beginner", "Start with clean transplants.")
        _expect(self, "leek/Pink root/management_beginner still carries the clean-stock claim",
                lambda: P.check_retired_claims(d))

    def test_senescing_coming_back(self):
        d = self._re("chives", BOT, "prevention_beginner", "Remove senescing leaves.")
        _expect(self, "still carries in-season senescing-leaf removal", lambda: P.check_retired_claims(d))

    def test_gray_mold_coming_back(self):
        d = self._re("chives", BOT, "symptoms_beginner", "Look for gray fuzzy mold.")
        _expect(self, "still carries the neck-rot gray-mold symptom", lambda: P.check_retired_claims(d))

    def test_splash_coming_back(self):
        d = self._re("chives", BOT, "cause_beginner", "Spread by splashing water.")
        _expect(self, "still carries the splash-dispersal mechanism", lambda: P.check_retired_claims(d))

    def test_a_claim_surviving_in_an_UNEDITED_sibling_field_is_caught(self):
        d = self._re("leek", MAG, "identification_beginner", "Worst where residue is left.")
        _expect(self, "leek/Onion maggot/identification_beginner still carries",
                lambda: P.check_retired_claims(d))


class RequiredClaimsPerBranch(unittest.TestCase):
    def test_each_required_claim_is_checked_in_each_declared_register(self):
        for (slug, name), fields, pat, label in P.REQUIRED:
            for f in fields:
                d = _applied()
                p = P.find_problem(d, slug, name)
                p[f] = pat.sub("later", p[f])
                _expect(self, "%s/%s/%s lacks %s" % (slug, name, f, label),
                        lambda d=d: P.check_required_claims(d))


class SurvivorsUrlsUniform(unittest.TestCase):
    def test_dropping_dense_canopies_refuses(self):
        """batch 24's scope pin for the chives Botrytis id anchors on this phrase."""
        d = _applied()
        p = P.find_problem(d, "chives", BOT)
        p["cause_seasoned"] = p["cause_seasoned"].replace("dense canopies", "crowding")
        _expect(self, "chives/Botrytis (leaf blight and neck rot) no longer says 'dense canopies'",
                lambda: P.check_survivors(d))

    def test_a_retired_url_surviving_under_the_kept_id_refuses(self):
        d = _applied()
        P.find_problem(d, "onion", MAG)["anchoring_urls"]["umn_ext"]["url"] = \
            "https://extension.umn.edu/vegetables/growing-onions"
        _expect(self, "retired anchors survive: ['onion/Onion maggot/umn_ext -> "
                      "extension.umn.edu/vegetables/growing-onions']", lambda: P.check_urls_retired(d))

    def test_a_maggot_crop_drifting_to_a_different_url_refuses(self):
        d = _applied()
        P.find_problem(d, "garlic", MAG)["anchoring_urls"]["uc_ipm"]["url"] = \
            "https://ipm.ucanr.edu/agriculture/onion-and-garlic/"
        _expect(self, "garlic/Onion maggot anchors uc_ipm at 'https://ipm.ucanr.edu/agriculture/"
                      "onion-and-garlic/', expected", lambda: P.check_maggot_anchors_uniform(d))


class BlastRadius(unittest.TestCase):
    def _post(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        return pre, d

    def test_clean_apply_changes_the_expected_leaves(self):
        pre, d = self._post()
        self.assertEqual(P.verify_post(pre, d), 71)

    def test_a_key_added_outside_sources_or_anchors_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "onion", PINK)["note"] = "x"
        _expect(self, "added or dropped outside sources/anchoring_urls", lambda: P.verify_post(pre, d))

    def test_a_source_added_on_a_NON_target_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "leek", "Leek rust")["sources"].append("umd_ext")
        _expect(self, "added or dropped outside the declared targets", lambda: P.verify_post(pre, d))

    def test_an_UNPINNED_field_on_a_target_changing_refuses(self):
        """The gap r4's suite found: the owner IS a target and the counts only count pinned
        fields, so a target's unpinned field moving was invisible."""
        pre, d = self._post()
        P.find_problem(d, "onion", PINK)["cause_beginner"] += " Extra."
        _expect(self, "onion/Pink root/cause_beginner is not a pinned field of this promote",
                lambda: P.verify_post(pre, d))

    def test_an_UNPINNED_rung_note_on_a_shipped_target_changing_refuses(self):
        pre, d = self._post()
        P.find_rung(d, "garlic", MAG, "crop_rotation")["note_beginner"] += " Extra."
        _expect(self, "garlic/Onion maggot/crop_rotation/note_beginner is not a pinned rung note of "
                      "this promote", lambda: P.verify_post(pre, d))

    def test_a_rung_note_silently_reverted_is_caught_by_the_count(self):
        pre, d = self._post()
        k = ("garlic", MAG, "garden_sanitation", "note_seasoned")
        P.find_rung(d, *k[:3])[k[3]] = P.RUNG_NOTES[k][0]
        _expect(self, "6 rung leaves changed, expected 7", lambda: P.verify_post(pre, d))

    def test_a_replacement_silently_reverted_refuses(self):
        pre, d = self._post()
        k = ("onion", PINK, "cause_seasoned")
        P.find_problem(d, *k[:2])[k[2]] = P.PROSE[k][0]
        _expect(self, "41 prose leaves changed, expected 42", lambda: P.verify_post(pre, d))

    def test_a_prose_leaf_changed_to_the_wrong_text_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "onion", PINK)["cause_seasoned"] = "wrong"
        _expect(self, "onion/Pink root/cause_seasoned did not receive its replacement",
                lambda: P.verify_post(pre, d))

    def test_a_rung_note_with_the_wrong_text_refuses(self):
        pre, d = self._post()
        P.find_rung(d, "garlic", MAG, "garden_sanitation")["note_seasoned"] = "wrong"
        _expect(self, "garlic/Onion maggot/garden_sanitation/note_seasoned did not receive its "
                      "replacement", lambda: P.verify_post(pre, d))

    def test_a_bystander_severity_change_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "leek", "Leek rust")["severity"] = "high"
        _expect(self, "2 severity leaves changed, expected 1", lambda: P.verify_post(pre, d))

    def test_severity_not_applied_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "leek", PINK)["severity"] = "medium"
        _expect(self, "0 severity leaves changed, expected 1", lambda: P.verify_post(pre, d))

    def test_a_bystander_change_on_a_non_counted_field_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "leek", "Leek rust")["identification_beginner"] = "changed"
        _expect(self, "leaves changed outside the declared targets: [('leek', 'Leek rust')]",
                lambda: P.verify_post(pre, d))

    def test_the_source_list_ORDER_is_pinned(self):
        pre, d = self._post()
        p = P.find_problem(d, "leek", PINK)
        p["sources"] = list(reversed(p["sources"]))
        _expect(self, "leek/Pink root sources are ['uf_ifas', 'usu_ext', 'uc_ipm'], expected "
                      "['uc_ipm', 'usu_ext', 'uf_ifas']", lambda: P.verify_post(pre, d))

    def test_anchor_keys_must_match_the_source_list(self):
        pre, d = self._post()
        P.find_problem(d, "leek", PINK)["anchoring_urls"].pop("usu_ext")
        _expect(self, "leek/Pink root anchoring_urls keys ['uc_ipm', 'uf_ifas'] do not match",
                lambda: P.verify_post(pre, d))

    def test_a_wrong_anchor_url_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "chives", "Rust")["anchoring_urls"]["osu_ext"]["url"] = "https://x"
        _expect(self, "chives/Rust anchor osu_ext is", lambda: P.verify_post(pre, d))

    def test_the_kept_garlic_usu_anchor_is_byte_identical(self):
        a, b = _pre(), _applied()
        self.assertEqual(P.find_problem(a, "garlic", MAG)["anchoring_urls"]["usu_ext"],
                         P.find_problem(b, "garlic", MAG)["anchoring_urls"]["usu_ext"])

    def test_rung_shape_checks_are_FORWARD_assertions(self):
        """A rung removed or added changes the key set and is refused before the rung-count check;
        a method duplicated is a changed control_ladder leaf and is refused by the rung-leaf count.
        Both are WITHDRAWN from the harness rather than reported as survivors; this test pins the
        masking so an edit that makes either reachable is noticed."""
        pre, d = self._post()
        P.find_problem(d, "garlic", MAG)["control_ladder"].pop()
        _expect(self, "added or dropped outside sources/anchoring_urls", lambda: P.verify_post(pre, d))
        pre, d = self._post()
        P.find_rung(d, "spring-onion", MAG, "floating_row_cover")["method"] = "crop_rotation"
        _expect(self, "spring-onion/Onion maggot/crop_rotation/method is not a pinned rung note of "
                      "this promote", lambda: P.verify_post(pre, d))


class CatalogUntouched(unittest.TestCase):
    def setUp(self):
        d = _pre()
        self.cm, self.sc = P.serialize(d["control_methods"]), P.serialize(d["source_catalog"])

    def test_control_methods_change_refuses(self):
        d = _pre()
        d["control_methods"]["crop_rotation"]["tier"] = "physical"
        _expect(self, "control_methods changed; this promote mints nothing",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_source_catalog_change_refuses(self):
        d = _pre()
        d["source_catalog"]["osu_ext"]["name"] = "x"
        _expect(self, "source_catalog changed; every id cited here already exists",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_every_id_this_promote_cites_already_exists(self):
        sc = _pre()["source_catalog"]
        for (_s, _n), (_b, after, _a) in P.SOURCES.items():
            for sid in after:
                self.assertIn(sid, sc)

    def test_the_real_promote_touches_neither(self):
        P.check_catalog_untouched(self.cm, self.sc, _applied())


class MainWiringIsDriven(unittest.TestCase):
    def test_apply_to_routes_through_check_pins(self):
        import inspect
        self.assertIn("check_pins(", inspect.getsource(P.apply_to))

    def test_main_runs_every_post_check(self):
        import inspect
        src = inspect.getsource(P.main)
        for frag in ("verify_post(pre, data)", "check_catalog_untouched(before_cm, before_sc, data)",
                     "check_retired_claims(data)", "check_required_claims(data)",
                     "check_survivors(data)", "check_urls_retired(data)",
                     "check_maggot_anchors_uniform(data)", "if sha != expect:"):
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
            self.assertIn("retired claims gone : 30/30", r.stdout)
            self.assertIn("required claims in  : 40 registers", r.stdout)
            self.assertIn("maggot anchors      : 12 uniform across 6 crops", r.stdout)
            self.assertIn("leek pink root      : severity medium -> low", r.stdout)
            self.assertIn("dry run; pass --apply to write", r.stdout)
        finally:
            os.unlink(path)

    def test_the_canonical_flag_form_is_accepted(self):
        """promote_fixture's CHAIN replay passes `--canonical PATH`. Driven with a file whose SHA
        differs from live canonical, so ignoring the flag (silently reading the default path) is
        refused by the base-SHA check wherever live canonical happens to sit. The first version
        passed the pinned pre-state, byte-identical to live canonical whenever this promote is the
        next to land, and the harness mutation survived by that accident."""
        import subprocess, tempfile
        d = _pre()
        d["_probe"] = "canonical-flag driver"
        raw = P.serialize(d)
        sha = hashlib.sha256(raw).hexdigest()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(raw)
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, "--canonical", path, "--expect-sha", sha],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("base  SHA           : " + sha, r.stdout)
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
