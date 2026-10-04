#!/usr/bin/env python3
"""The WIDE restatement scanner and the restatement-support guard (PLA-655; housekeeping kickoff 60, B3, 2026-10-03).

SCANNER (cited_promote_common.spacing_strings / height_strings, wide by default):
  - ARMING: exactly the three landed PLA-10 promotes opt out with wide=False (their replays must reproduce the
    canonicals they landed), and every scanner call in them carries it. Any other promote gets the wide scanner.
  - POSITIVE CONTROL: PLA-655's named misses, on promote 3's pre-state (31b766e8), are flagged WIDE and not
    NARROW (so each arm is needed): dill, lemongrass x3, echinacea description (feet beside a growth word);
    edamame x2, green-beans-bush x2 (word numbers); sunflower "12+ ft" (the + figure); echinacea 'Magnus'
    "about 30 to 36 in" (the variety-leaf arm); and on promote 1's pre-state (c5fc3d13), artichoke
    soil_prep_beginner "a foot and a half between plants and two to three feet between rows" (spacing).
  - REFUSAL SPEC: the feet-only rule. An inch figure beside a growth word outside a variety leaf is NOT a height
    restatement (watering, soil depth: 88 of 89 sampled); a spacing sentence is not a height either.
  - POPULATION, measured before arming, after the precision exclusions: wide height hits over promote 3's fixed list (pre) 209
    (narrow 113); wide spacing hits over promote 1's 113 staged crops (pre-state) 793 (narrow 762).
SUPPORT GUARD (check_restatement_support): promote 3's 12 real rows pass; each mechanical check refuses its own
defect injected into a copy of one real row (meaning is never checked here; it stays with review).
Run: python3 -m pytest tools/test_restatement_scanner_wide.py -q
SHIPS MUTATION-TESTED via mutate_cited_promote_common.py.
"""
import copy, glob, json, os, re, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cited_promote_common as C  # noqa: E402
import promote_fixture  # noqa: E402
import promote_pla10_planting_layout as P1  # noqa: E402
import promote_pla10_promote3 as P3  # noqa: E402

LANDED = {"promote_pla10_planting_layout.py", "promote_pla10_promote2.py", "promote_pla10_promote3.py"}
PRE3 = {c["slug"]: c for c in json.loads(promote_fixture.pre_state(P3.BASE_SHA))["crops"]}
PRE1 = {c["slug"]: c for c in json.loads(promote_fixture.pre_state(P1.BASE_SHA))["crops"]}
POST3 = {c["slug"]: c for c in json.loads(promote_fixture.pre_state(
    "b331e5f2c99378526c3ac8f2f870232953b318c994b7dc3d8c54938f2b62c38d"))["crops"]}

# (slug, leaf, spread authored on promote 3's stage)
HEIGHT_CONTROL = (
    ("dill", "container_notes.notes_seasoned", False),
    ("lemongrass", "companions.note_seasoned", False),
    ("lemongrass", "tips_by_stage.vegetative[0].text_seasoned", False),
    ("lemongrass", "regions.northern_tier.region_notes_seasoned", False),
    ("echinacea", "description_seasoned", True),
    ("edamame", "growth_stages[2].what_to_look_for_beginner", False),
    ("edamame", "growth_stages[2].what_to_look_for_seasoned", False),
    ("green-beans-bush", "growth_stages[2].what_to_look_for_beginner", False),
    ("green-beans-bush", "growth_stages[2].what_to_look_for_seasoned", False),
    ("sunflower", "varieties.recommended[1]", False),
    ("echinacea", "varieties.recommended[0]", False),
)


class Arming(unittest.TestCase):
    def test_exactly_the_three_landed_promotes_opt_out(self):
        opted = {os.path.basename(p) for p in glob.glob(os.path.join(HERE, "promote_*.py"))
                 if "wide=False" in open(p, encoding="utf-8").read()}
        self.assertEqual(opted, LANDED)

    def test_every_scanner_call_in_a_landed_promote_opts_out(self):
        for name in sorted(LANDED):
            src = open(os.path.join(HERE, name), encoding="utf-8").read()
            calls = re.findall(r"\b(?:spacing|height)_strings\((?:[^()]|\([^()]*\))*\)", src)
            with self.subTest(promote=name):
                self.assertEqual(len(calls), 1, calls)
                self.assertTrue(all("wide=False" in c for c in calls), calls)

    def test_the_default_is_wide(self):
        crop = PRE3["dill"]
        self.assertEqual(C.height_strings(crop, False), C.height_strings(crop, False, wide=True))
        self.assertNotEqual(C.height_strings(crop, False), C.height_strings(crop, False, wide=False))


class PositiveControl(unittest.TestCase):
    def test_pla655s_height_misses_are_flagged_wide_and_not_narrow(self):
        for slug, leaf, sp in HEIGHT_CONTROL:
            with self.subTest(crop=slug, leaf=leaf):
                self.assertNotIn(leaf, C.height_strings(PRE3[slug], sp, wide=False))
                self.assertIn(leaf, C.height_strings(PRE3[slug], sp))

    def test_artichokes_word_number_spacing_is_flagged_wide_and_not_narrow(self):
        self.assertNotIn("soil_prep_beginner", C.spacing_strings(PRE1["artichoke"], wide=False))
        self.assertIn("soil_prep_beginner", C.spacing_strings(PRE1["artichoke"]))


class Idiom(unittest.TestCase):
    def test_a_foot_is_read_as_a_distance(self):
        self.assertEqual(C.spacing_strings({"tips": ["Allow a foot between plants."]}), ["tips[0]"])
        self.assertEqual(C.spacing_strings({"tips": ["Allow a foot between plants."]}, wide=False), [])
        self.assertEqual(C.height_strings({"tips": ["It grows about a foot tall."]}, False), ["tips[0]"])


class RefusalSpec(unittest.TestCase):
    def test_an_inch_figure_beside_a_growth_word_is_not_a_height(self):
        crop = {"watering": {"amount_seasoned": "Aim for roughly 1 inch of water per week during active growth."}}
        self.assertEqual(C.height_strings(crop, False), [])

    def test_a_feet_spacing_sentence_is_not_a_height(self):
        crop = {"tips": ["Space plants 3 feet apart so the vines can grow."]}
        self.assertEqual(C.height_strings(crop, False), [])

    def test_a_bare_variety_figure_about_a_pot_is_not_a_height(self):
        crop = {"varieties": {"recommended": ["Patio Gem (compact, fits a 5-gallon pot about 12 inches across)"]}}
        self.assertEqual(C.height_strings(crop, False), [])

    def test_a_bare_figure_outside_a_variety_leaf_is_not_a_height(self):
        crop = {"description_seasoned": "A standard, about 30 to 36 in."}
        self.assertEqual(C.height_strings(crop, False), [])


class Exclusions(unittest.TestCase):
    """The two precision exclusions on the WIDE arms (ruled 2026-10-03 from the live read of b331e5f2)."""

    def test_in_before_a_sentence_word_is_not_an_inch(self):
        self.assertEqual(C.spacing_strings({"tips": ["Sow two in warm weather, thinning between plants."]}), [])
        self.assertEqual(C.height_strings({"varieties": {"recommended": ["'Zone Hardy' (survives zone 5 in good years)"]}},
                                          False), [])
        self.assertEqual(C.spacing_strings({"tips": ["Space plants 12 in apart."]}), ["tips[0]"])

    def test_feet_beside_an_elevation_word_is_not_a_height(self):
        self.assertEqual(C.height_strings({"tips": ["It grows best at 800 feet elevation."]}, False), [])

    def test_a_thousand_feet_without_a_comma_is_not_a_height(self):
        self.assertEqual(C.height_strings({"tips": ["It grows well below 3000 feet."]}, False), [])

    def test_a_comma_thousands_figure_is_not_a_height(self):
        self.assertEqual(C.height_strings({"tips": ["It grows well below 3,000 feet."]}, False), [])

    def test_at_2_feet_is_a_height(self):
        self.assertEqual(C.height_strings({"tips": ["Pinch back the stems at 2 feet."]}, False), ["tips[0]"])
        self.assertEqual(C.height_strings({"tips": ["It grows to 6 feet tall above the fence."]}, False), ["tips[0]"])


class Population(unittest.TestCase):
    def test_wide_height_population_on_promote_3s_fixed_list(self):
        stage, _ = P3.load_stage(P3.STAGE)
        fixed = P3.NEW_CROPS + P3.BACKFILL_CROPS
        narrow = sum(len(C.height_strings(PRE3[s], stage[s].get(P3.S) is not None, wide=False)) for s in fixed)
        wide = sum(len(C.height_strings(PRE3[s], stage[s].get(P3.S) is not None)) for s in fixed)
        self.assertEqual((len(fixed), narrow, wide), (62, 113, 209))

    def test_wide_spacing_population_on_promote_1s_staged_crops(self):
        stage, _ = P1.load_stage(P1.STAGE)
        narrow = sum(len(C.spacing_strings(PRE1[s], wide=False)) for s in stage)
        wide = sum(len(C.spacing_strings(PRE1[s])) for s in stage)
        self.assertEqual((len(stage), narrow, wide), (113, 762, 793))


class SupportGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stage, _ = P3.load_stage(P3.STAGE)
        cls.adj = {slug: {C.fmt(C.resolve(PRE3[slug], r["path"])): r["verdict"]
                          for r in s.get("restatements") or []} for slug, s in cls.stage.items()}
        cls.man = C.manifest(P3.EVIDENCE)

    def check(self, rows):
        st = C.Stage(dict(self.stage), rows)
        return C.check_restatement_support(st, POST3, self.adj, self.man, P3.EVIDENCE)

    def refuses(self, mutate, text):
        rows = copy.deepcopy(self.stage.support)
        mutate(rows)
        with self.assertRaises(C.Refused) as cm:
            self.check(rows)
        self.assertIn(text, str(cm.exception))

    def test_promote_3s_real_rows_pass(self):
        self.assertEqual(self.check(copy.deepcopy(self.stage.support)), 12)

    def test_promote_3_runs_the_guard_on_its_real_stage(self):
        stage, ev = P3.load_stage(P3.STAGE)
        stage.support[0]["quote"] = "this sentence appears on no extension page at all"
        pre = json.loads(promote_fixture.pre_state(P3.BASE_SHA))
        with self.assertRaises(C.Refused) as cm:
            P3.run(pre, stage, ev, P3.EVIDENCE)
        self.assertIn(C.SUPPORT_FILE, str(cm.exception))

    def test_a_plain_dict_stage_is_refused_not_read_as_none(self):
        with self.assertRaises(C.Refused):
            C.check_restatement_support(dict(self.stage), POST3, self.adj, self.man, P3.EVIDENCE)

    def test_a_duplicate_row_REFUSES(self):
        self.refuses(lambda rows: rows.append(dict(rows[0])), "a duplicate row")

    def test_a_wrong_entry_id_REFUSES(self):
        self.refuses(lambda rows: rows[0].update(entry_id="mature_dimensions"), "is not 'restatement-support'")

    def test_an_unstaged_crop_REFUSES(self):
        self.refuses(lambda rows: rows[0].update(crop="carrot"), "is not a staged crop")

    def test_a_leaf_not_adjudicated_agrees_REFUSES(self):
        self.refuses(lambda rows: rows[0].update(field="description_seasoned"), "does not adjudicate")

    def test_a_url_not_cited_on_the_crop_REFUSES(self):
        self.refuses(lambda rows: rows[0].update(url="https://extension.example.edu/not-cited-on-this-crop"),
                     "url is not cited anywhere")

    def test_a_manifest_mismatch_REFUSES(self):
        self.refuses(lambda rows: rows[0].update(sha256=rows[1]["sha256"] if rows[1]["sha256"] != rows[0]["sha256"]
                                                  else rows[3]["sha256"]), "is not in")

    def test_a_quote_not_in_the_bytes_REFUSES(self):
        self.refuses(lambda rows: rows[0].update(quote="this sentence appears on no extension page at all"),
                     "the quote is not in the cached bytes")


if __name__ == "__main__":
    unittest.main()
