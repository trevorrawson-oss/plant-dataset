#!/usr/bin/env python3
"""Guard suite for tools/promote_allium_record_corrections_r4.py. Base 9d2031ff (r3's output).

REPLAY-PINNED via CHAIN until r3 commits. Evidence the guards are live: `MainWiringIsDriven` plus
tools/mutate_allium_record_corrections_r4_suite.py.

`PositiveControl` pins which (crop, label) pairs are refusal-spec: reflective mulch and the
false-attribution device are present on NO thrips target in the pre-state (the mulch was dropped
by 112a8f7), so those scans refuse-and-stay-green by contract. `MatcherBehaviour` asserts every
predicate in both directions, including that "rotate" is caught wherever it hides and that the
replacements pass every predicate of their own promote.
"""
import hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_allium_record_corrections_r4 as P  # noqa: E402

POST_SHA = "47e7b5c03cd91829a40279f319f11140de800a127aff2d277d1e977f95b6b143"
T = P.THRIPS
REFUSAL_SPEC = {(c, lab) for c in P.CROPS for lab in ("reflective mulch", "the false-attribution device")}


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
        self.assertEqual((len(P.PROSE), len(P.RUNG_REPLACE), len(P.SOURCES)), (10, 2, 5))
        self.assertEqual(len(P.TARGETS), 5)
        self.assertEqual(len(P.RETIRED), 20)
        self.assertEqual(sum(len(f) for _t, f, _p, _l in P.REQUIRED), 50)

    def test_the_roster_shape_is_unchanged(self):
        a, b = _pre(), _applied()
        self.assertEqual(len(a["crops"]), 128)
        self.assertEqual(sum(len(P.problems(c)) for c in b["crops"]), 912)
        self.assertEqual((P.rung_count(a), P.rung_count(b)), (3243, 3243))

    def test_shipped_ladders_keep_their_length_and_swap_only_position_zero(self):
        a, b = _pre(), _applied()
        for slug, name in P.SHIPPED:
            la = [r["method"] for r in P.find_problem(a, slug, name)["control_ladder"]]
            lb = [r["method"] for r in P.find_problem(b, slug, name)["control_ladder"]]
            self.assertEqual(la, ["crop_rotation", "water_spray"])
            self.assertEqual(lb, ["garden_sanitation", "water_spray"])
            self.assertEqual(P.find_problem(a, slug, name)["control_ladder"][1],
                             P.find_problem(b, slug, name)["control_ladder"][1])

    def test_unshipped_targets_stay_id_less(self):
        b = _applied()
        for slug in ("onion", "shallot", "leek"):
            p = P.find_problem(b, slug, T)
            self.assertIsNone(p.get("id"))
            self.assertIsNone(p.get("control_ladder"))

    def test_chives_is_byte_identical(self):
        a, b = _pre(), _applied()
        self.assertEqual(P.by_slug(a)["chives"], P.by_slug(b)["chives"])

    def test_severity_and_names_untouched(self):
        a, b = _pre(), _applied()
        for c in a["crops"]:
            self.assertEqual([(p.get("name"), p.get("severity")) for p in P.problems(c)],
                             [(p.get("name"), p.get("severity")) for p in P.problems(P.by_slug(b)[c["slug"]])])


class PositiveControl(unittest.TestCase):
    def test_retired_labels_present_or_pinned_refusal_spec(self):
        d = _pre()
        for (slug, name), fn, label in P.RETIRED:
            hit = any(fn(v) for _w, v in P.strings_of(P.find_problem(d, slug, name)))
            if hit:
                self.assertNotIn((slug, label), REFUSAL_SPEC, (slug, label))
            else:
                self.assertIn((slug, label), REFUSAL_SPEC, (slug, label))
        self.assertEqual(len(REFUSAL_SPEC), 10)

    def test_the_rotation_claim_is_on_every_crop_in_the_pre_state(self):
        d = _pre()
        for slug in P.CROPS:
            p = P.find_problem(d, slug, T)
            self.assertIn("rotate away from alliums", p["management_seasoned"])

    def test_the_shipped_rotation_rungs_exist_in_the_pre_state(self):
        d = _pre()
        for slug, name in P.SHIPPED:
            self.assertEqual(P.find_problem(d, slug, name)["control_ladder"][0]["method"], "crop_rotation")

    def test_every_required_claim_is_absent_in_the_pre_state(self):
        d = _pre()
        for (slug, name), fields, pat, label in P.REQUIRED:
            p = P.find_problem(d, slug, name)
            for f in fields:
                self.assertIsNone(pat.search(p.get(f) or ""), "%s/%s already carried %s" % (slug, f, label))

    def test_the_guards_fail_on_pre_and_pass_after(self):
        _expect(self, "still carries the rotation claim", lambda: P.check_retired_claims(_pre()))
        _expect(self, "garlic/Onion thrips still carries a crop_rotation rung",
                lambda: P.check_no_rotation_rung(_pre()))
        _expect(self, "lacks", lambda: P.check_required_claims(_pre()))
        b = _applied()
        self.assertEqual(P.check_retired_claims(b), 20)
        self.assertEqual(P.check_no_rotation_rung(b), 2)
        self.assertEqual(P.check_required_claims(b), 50)
        self.assertEqual(P.check_survivors(b), 5)


class MatcherBehaviour(unittest.TestCase):
    def _fn(self, label, crop="onion"):
        hits = [fn for (s, n), fn, lab in P.RETIRED if lab == label and s == crop]
        self.assertEqual(len(hits), 1)
        return hits[0]

    def test_rotation_pattern(self):
        fn = self._fn("the rotation claim")
        for t in ("rotate away from alliums", "Rotating off last season's allium ground",
                  "crop rotation is the foundation", "Rotation and cleanup are the pair"):
            self.assertTrue(fn(t), t)
        for t in ("Clear volunteer onions and crop debris", "keep the bed away from small grains",
                  "rogue out volunteer alliums"):
            self.assertFalse(fn(t), t)

    def test_same_spot_pattern(self):
        fn = self._fn("the same-spot rotation instruction")
        for t in ("do not plant garlic where onions or garlic grew last year",
                  "do not plant onions in the same spot every year",
                  "Do not plant alliums in the same place each year",
                  "do not plant leeks where you grew onions or leeks last year"):
            self.assertTrue(fn(t), t)
        for t in ("do not put onions right beside a grain, alfalfa or clover patch",
                  "Do not cover a bed that grew alliums last year"):
            self.assertFalse(fn(t), t)

    def test_required_patterns(self):
        pats = {lab: pat for _t, _f, pat, lab in P.REQUIRED}
        self.assertTrue(pats["vigor as TOLERANCE"].search("vigor buys tolerance of the feeding"))
        self.assertIsNone(pats["vigor as TOLERANCE"].search("keep plants vigorous and watered"))
        self.assertTrue(pats["the grain, alfalfa or clover neighbor"].search("small grains, alfalfa or clover"))
        self.assertIsNone(pats["the grain, alfalfa or clover neighbor"].search("grainy soil"))
        self.assertTrue(pats["volunteer and debris sanitation"].search("Clear volunteer onions"))
        self.assertTrue(pats["volunteer and debris sanitation"].search("rogue out volunteer alliums"))
        self.assertIsNone(pats["volunteer and debris sanitation"].search("clean up old onion scraps"))
        self.assertTrue(pats["straw mulch"].search("straw mulch on the bed deters thrips"))
        self.assertIsNone(pats["straw mulch"].search("use mulches"))

    def test_replacements_pass_every_predicate_of_their_own_promote(self):
        for (slug, name, _f), (_b, after) in P.PROSE.items():
            self.assertEqual(P.hygiene(after), [], after[:50])
            for (ts, tn), fn, label in P.RETIRED:
                if (ts, tn) == (slug, name):
                    self.assertFalse(fn(after), "%s trips %r" % (slug, label))
        for (slug, name, _i, _o), (_m, nb, ns) in P.RUNG_REPLACE.items():
            for note in (nb, ns):
                self.assertEqual(P.hygiene(note), [], note[:50])
                for (ts, tn), fn, label in P.RETIRED:
                    if (ts, tn) == (slug, name):
                        self.assertFalse(fn(note), "%s rung trips %r" % (slug, label))


class Pins(unittest.TestCase):
    def test_stale_prose_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "onion", T)["management_seasoned"] = "moved"
        _expect(self, "onion/Onion thrips/management_seasoned does not match its pinned text; the record "
                      "moved", lambda: P.check_pins(d))

    def test_table_sizes_are_asserted(self):
        d = _pre()
        with _Patch("EXPECTED_PROSE", 9):
            _expect(self, "edit tables hold 10/2/5, expected 9/2/5", lambda: P.check_pins(d))

    def test_an_undeclared_target_refuses(self):
        d = _pre()
        pr = dict(P.PROSE)
        pr[("chives", T, "prevention_beginner")] = ("x", "y")
        with _Patch("PROSE", pr), _Patch("EXPECTED_PROSE", len(pr)):
            _expect(self, "chives/Onion thrips is not a declared target", lambda: P.check_pins(d))

    def test_an_identical_replacement_refuses(self):
        d = _pre()
        k = ("onion", T, "management_seasoned")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][0])
        with _Patch("PROSE", pr):
            _expect(self, "onion/Onion thrips/management_seasoned replacement is identical",
                    lambda: P.check_pins(d))

    def test_hygiene_on_a_replacement_refuses(self):
        d = _pre()
        k = ("onion", T, "management_beginner")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][1] + " This never fails.")
        with _Patch("PROSE", pr):
            _expect(self, "onion/Onion thrips/management_beginner replacement: absolute:never",
                    lambda: P.check_pins(d))

    def test_a_rung_replace_on_an_unshipped_target_refuses(self):
        d = _pre()
        rr = dict(P.RUNG_REPLACE)
        rr[("leek", T, 0, "crop_rotation")] = ("garden_sanitation", "a", "b")
        with _Patch("RUNG_REPLACE", rr), _Patch("SHIPPED", P.SHIPPED + (("leek", T),)):
            _expect(self, "leek/Onion thrips is declared shipped but carries no ladder or id",
                    lambda: P.check_pins(d))

    def test_a_rung_at_the_wrong_position_refuses(self):
        d = _pre()
        rr = {("garlic", T, 1, "crop_rotation"): P.RUNG_REPLACE[("garlic", T, 0, "crop_rotation")],
              ("spring-onion", T, 0, "crop_rotation"): P.RUNG_REPLACE[("spring-onion", T, 0, "crop_rotation")]}
        with _Patch("RUNG_REPLACE", rr):
            _expect(self, "garlic/Onion thrips rung 1 is 'water_spray', expected 'crop_rotation'",
                    lambda: P.check_pins(d))

    def test_an_unknown_replacement_method_refuses(self):
        d = _pre()
        rr = dict(P.RUNG_REPLACE)
        rr[("garlic", T, 0, "crop_rotation")] = ("bed_hygiene", "a", "b")
        with _Patch("RUNG_REPLACE", rr):
            _expect(self, "garlic/Onion thrips replacement method 'bed_hygiene' is not in control_methods",
                    lambda: P.check_pins(d))

    def test_a_replacement_already_on_the_ladder_refuses(self):
        d = _pre()
        rr = dict(P.RUNG_REPLACE)
        rr[("garlic", T, 0, "crop_rotation")] = ("water_spray", "a", "b")
        with _Patch("RUNG_REPLACE", rr):
            _expect(self, "garlic/Onion thrips already carries 'water_spray'; the replacement would "
                          "duplicate it", lambda: P.check_pins(d))

    def test_a_replacement_that_changes_the_tier_refuses(self):
        d = _pre()
        rr = dict(P.RUNG_REPLACE)
        rr[("garlic", T, 0, "crop_rotation")] = ("floating_row_cover", "a", "b")
        with _Patch("RUNG_REPLACE", rr):
            _expect(self, "replacing 'crop_rotation' (cultural) with 'floating_row_cover' (physical) "
                          "changes the tier at that position", lambda: P.check_pins(d))

    def test_a_replacement_not_reaching_the_type_refuses(self):
        d = _pre()
        rr = dict(P.RUNG_REPLACE)
        rr[("garlic", T, 0, "crop_rotation")] = ("airflow_spacing", "a", "b")
        with _Patch("RUNG_REPLACE", rr):
            _expect(self, "garlic/Onion thrips replacement 'airflow_spacing' does not carry applies_to any",
                    lambda: P.check_pins(d))

    def test_identical_rung_registers_refuse(self):
        d = _pre()
        rr = dict(P.RUNG_REPLACE)
        rr[("garlic", T, 0, "crop_rotation")] = ("garden_sanitation", "same text", "same text")
        with _Patch("RUNG_REPLACE", rr):
            _expect(self, "garlic/Onion thrips/garden_sanitation registers are identical",
                    lambda: P.check_pins(d))

    def test_ladder_vocabulary_in_a_rung_note_refuses(self):
        d = _pre()
        rr = dict(P.RUNG_REPLACE)
        nb, ns = P.RUNG_REPLACE[("garlic", T, 0, "crop_rotation")][1:]
        rr[("garlic", T, 0, "crop_rotation")] = ("garden_sanitation", nb + " See the next rung.", ns)
        with _Patch("RUNG_REPLACE", rr):
            _expect(self, "garlic/Onion thrips/garden_sanitation note_beginner: ladder vocabulary",
                    lambda: P.check_pins(d))

    def test_an_unshipped_target_carrying_an_id_refuses(self):
        d = _pre()
        P.find_problem(d, "onion", T)["id"] = "onion-thrips"
        _expect(self, "onion/Onion thrips already carries a ladder or id; this promote must land BEFORE "
                      "batch 24", lambda: P.check_pins(d))

    def test_a_stale_source_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "onion", T)["sources"] = ["usu_ext"]
        _expect(self, "onion/Onion thrips sources are ['usu_ext'], pinned ['umn_ext']",
                lambda: P.check_pins(d))

    def test_a_cited_id_without_an_anchor_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("onion", T)] = (["umn_ext"], ["usu_ext", "umass_ext"], {"usu_ext": "https://x"})
        with _Patch("SOURCES", src):
            _expect(self, "onion/Onion thrips cites 'umass_ext' without a document anchor",
                    lambda: P.check_pins(d))

    def test_an_id_absent_from_the_catalog_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("onion", T)] = (["umn_ext"], ["usu_ext", "wisc_hort"], {"usu_ext": "https://x", "wisc_hort": "https://y"})
        with _Patch("SOURCES", src):
            _expect(self, "onion/Onion thrips cites 'wisc_hort', which is not in source_catalog",
                    lambda: P.check_pins(d))

    def test_a_target_with_prose_but_no_sources_refuses(self):
        d = _pre()
        src = {k: v for k, v in P.SOURCES.items() if k != ("leek", T)}
        with _Patch("SOURCES", src), _Patch("EXPECTED_SOURCE_SETS", 4):
            _expect(self, "leek/Onion thrips is declared but not fully edited", lambda: P.check_pins(d))


class RetiredAndRequiredPerBranch(unittest.TestCase):
    def test_rotation_coming_back_in_prose(self):
        d = _applied()
        P.find_problem(d, "leek", T)["management_beginner"] = "Rotate the bed."
        _expect(self, "leek/Onion thrips/management_beginner still carries the rotation claim",
                lambda: P.check_retired_claims(d))

    def test_same_spot_coming_back(self):
        d = _applied()
        P.find_problem(d, "shallot", T)["cause_beginner"] = "Do not plant shallots in the same spot every year."
        _expect(self, "shallot/Onion thrips/cause_beginner still carries the same-spot rotation instruction",
                lambda: P.check_retired_claims(d))

    def test_rotation_coming_back_in_a_RUNG_NOTE(self):
        d = _applied()
        P.find_problem(d, "garlic", T)["control_ladder"][1]["note_seasoned"] = "Rotation helps."
        _expect(self, "garlic/Onion thrips/water_spray/note_seasoned still carries the rotation claim",
                lambda: P.check_retired_claims(d))

    def test_reflective_mulch_coming_back(self):
        d = _applied()
        P.find_problem(d, "onion", T)["management_seasoned"] += " Use reflective mulch."
        _expect(self, "onion/Onion thrips/management_seasoned still carries reflective mulch",
                lambda: P.check_retired_claims(d))

    def test_a_rotation_rung_surviving_refuses(self):
        d = _applied()
        P.find_problem(d, "spring-onion", T)["control_ladder"].append(
            {"method": "crop_rotation", "note_beginner": "a", "note_seasoned": "b"})
        _expect(self, "spring-onion/Onion thrips still carries a crop_rotation rung",
                lambda: P.check_no_rotation_rung(d))

    def test_the_replacement_not_at_the_position_refuses(self):
        d = _applied()
        P.find_problem(d, "garlic", T)["control_ladder"][0]["method"] = "handpick"
        _expect(self, "garlic/Onion thrips rung 0 is 'handpick', expected 'garden_sanitation' after "
                      "replacement", lambda: P.check_no_rotation_rung(d))

    def test_each_required_claim_is_checked_in_each_register(self):
        for (slug, name), fields, pat, label in P.REQUIRED:
            for f in fields:
                d = _applied()
                p = P.find_problem(d, slug, name)
                p[f] = pat.sub("later", p[f])
                _expect(self, "%s/%s/%s lacks %s" % (slug, name, f, label),
                        lambda d=d: P.check_required_claims(d))

    def test_dropping_the_binomial_refuses(self):
        d = _applied()
        p = P.find_problem(d, "leek", T)
        p["cause_seasoned"] = p["cause_seasoned"].replace("Thrips tabaci", "a thrips")
        _expect(self, "leek/Onion thrips no longer says 'Thrips tabaci'", lambda: P.check_survivors(d))

    def test_a_chives_change_refuses(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        P.find_problem(d, "chives", T)["prevention_beginner"] = "changed"
        _expect(self, "chives changed", lambda: P.check_chives_untouched(pre, d))


class BlastRadius(unittest.TestCase):
    def _post(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        return pre, d

    def test_clean_apply_changes_the_expected_leaves(self):
        pre, d = self._post()
        self.assertEqual(P.verify_post(pre, d), 25)

    def test_a_key_added_outside_sources_or_anchors_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "onion", T)["note"] = "x"
        _expect(self, "added or dropped outside sources/anchoring_urls", lambda: P.verify_post(pre, d))

    def test_a_source_added_on_a_NON_target_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "chives", T)["sources"].append("uc_ipm")
        _expect(self, "added or dropped outside the declared targets", lambda: P.verify_post(pre, d))

    def test_an_extra_prose_change_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "chives", T)["organic_treatment_beginner"] = "changed"
        _expect(self, "leaves changed outside the declared targets: [('chives', 'Onion thrips')]",
                lambda: P.verify_post(pre, d))

    def test_a_target_management_change_beyond_the_pins_is_caught_by_the_count(self):
        pre, d = self._post()
        P.find_problem(d, "onion", T)["management_seasoned"] += " Extra."
        _expect(self, "onion/Onion thrips/management_seasoned did not receive its replacement",
                lambda: P.verify_post(pre, d))

    def test_an_UNPINNED_field_on_a_target_changing_refuses(self):
        """The first suite run found this gap: the owner IS a target and the counts only count the
        management fields, so a target's cause text moving was invisible."""
        pre, d = self._post()
        P.find_problem(d, "onion", T)["cause_beginner"] = "changed"
        _expect(self, "onion/Onion thrips/cause_beginner is not a pinned field of this promote",
                lambda: P.verify_post(pre, d))

    def test_a_leaf_of_the_UNREPLACED_rung_changing_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "garlic", T)["control_ladder"][1]["note_beginner"] = "changed"
        _expect(self, "garlic/Onion thrips rung [1]/note_beginner is not the replaced rung of this "
                      "promote", lambda: P.verify_post(pre, d))

    def test_a_pinned_field_silently_reverted_is_caught_by_the_count(self):
        """The harness found the count check undriven once the unpinned-field check landed: an
        EXTRA change is refused earlier, so only a REVERTED pinned field reaches the count."""
        pre, d = self._post()
        k = ("onion", T, "management_seasoned")
        P.find_problem(d, *k[:2])[k[2]] = P.PROSE[k][0]
        _expect(self, "9 prose leaves changed, expected 10", lambda: P.verify_post(pre, d))

    def test_rung_leaf_count_is_pinned(self):
        pre, d = self._post()
        P.find_problem(d, "garlic", T)["control_ladder"][0]["method"] = "crop_rotation"
        _expect(self, "5 rung leaves changed, expected 6", lambda: P.verify_post(pre, d))

    def test_a_rung_replacement_with_the_wrong_text_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "garlic", T)["control_ladder"][0]["note_seasoned"] = \
            P.RUNG_REPLACE[("garlic", T, 0, "crop_rotation")][2]
        P.find_problem(d, "garlic", T)["control_ladder"][0]["note_beginner"] = \
            P.RUNG_REPLACE[("spring-onion", T, 0, "crop_rotation")][1]
        _expect(self, "garlic/Onion thrips rung 0 did not receive its replacement",
                lambda: P.verify_post(pre, d))

    def test_the_source_order_is_pinned(self):
        pre, d = self._post()
        p = P.find_problem(d, "leek", T)
        p["sources"] = list(reversed(p["sources"]))
        _expect(self, "leek/Onion thrips sources are ['umd_ext', 'uc_ipm', 'umass_ext', 'osu_ext'], expected",
                lambda: P.verify_post(pre, d))

    def test_anchor_keys_must_match(self):
        pre, d = self._post()
        P.find_problem(d, "leek", T)["anchoring_urls"].pop("umd_ext")
        _expect(self, "leek/Onion thrips anchoring_urls keys", lambda: P.verify_post(pre, d))

    def test_a_wrong_anchor_url_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "onion", T)["anchoring_urls"]["usu_ext"]["url"] = \
            "https://extension.usu.edu/yardandgarden/research/onions-in-the-garden"
        _expect(self, "onion/Onion thrips anchor usu_ext is", lambda: P.verify_post(pre, d))

    def test_a_rung_added_is_refused_by_the_key_set(self):
        pre, d = self._post()
        P.find_problem(d, "garlic", T)["control_ladder"].append(
            {"method": "handpick", "note_beginner": "a", "note_seasoned": "b"})
        _expect(self, "added or dropped outside sources/anchoring_urls", lambda: P.verify_post(pre, d))


class CatalogUntouched(unittest.TestCase):
    def setUp(self):
        d = _pre()
        self.cm, self.sc = P.serialize(d["control_methods"]), P.serialize(d["source_catalog"])

    def test_control_methods_change_refuses(self):
        d = _pre()
        d["control_methods"]["straw_mulch"]["applies_to"].append("insect")
        _expect(self, "control_methods changed; this promote mints nothing",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_source_catalog_change_refuses(self):
        d = _pre()
        d["source_catalog"]["umd_ext"]["name"] = "x"
        _expect(self, "source_catalog changed", lambda: P.check_catalog_untouched(self.cm, self.sc, d))

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
                     "check_retired_claims(data)", "check_no_rotation_rung(data)",
                     "check_required_claims(data)", "check_survivors(data)",
                     "check_chives_untouched(pre, data)", "if sha != expect:"):
            self.assertIn(frag, src)

    def test_end_to_end_through_main(self):
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(promote_fixture.pre_state(P.BASE_SHA))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, "--canonical", path], capture_output=True,
                               text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("post  SHA           : " + POST_SHA, r.stdout)
            self.assertIn("retired claims gone : 20/20", r.stdout)
            self.assertIn("rungs replaced      : 2 crop_rotation -> garden_sanitation; rungs 3243 -> 3243",
                          r.stdout)
            self.assertIn("required claims in  : 50 registers", r.stdout)
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
