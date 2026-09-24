#!/usr/bin/env python3
"""Unit suite for critical_warnings_gate -- A61 (PLA-581 spec 2026-09-21, section 7; register row 32).

THE FIXTURE IS THE PINNED BASE 526788f2 rebuilt by promote_fixture, never live canonical, so this
suite does not move when the PLA-581 promote (or any later one) moves canonical.

THE FIVE POSITIVE CONTROLS the spec owes BY NAME (section 7.3) live in NamedControls. Under the
rulings every certified crop ships `null`, so the live data exercises NONE of the entry rules, the
`[]` branch, a non-null `stage`, a `harvest` entry or a second entry on one crop. Without these the
gate is coverage in name only. Each is a mutation driver in mutate_pla581_critical_warnings_suite.py.
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import critical_warnings_gate as G  # noqa: E402

FIXTURE_SHA = "526788f2c34a7fe1c59e9427271c1d1738c6b6cce2c1d0524df715e4fc359659"  # PLA-580, 2588678
CROP = "basil"          # certified, container_ok, carries a growth_stages ladder
SHELL = "avocado"       # an uncertified shell
URL = "https://extension.illinois.edu/container-gardens/container-size"


def entry(**kw):
    e = {"id": "a-full-pot-is-heavy", "class": "safety", "severity": "high", "stage": None,
         "title": "A full pot is heavy",
         "body_seasoned": "Wet potting mix is heavy; consult a building architect about load.",
         "body_beginner": "Wet soil is heavy, so ask the building owner before you set pots up.",
         "sources": ["uiuc_ext"],
         "anchoring_urls": {"uiuc_ext": {"url": URL, "verified": "2026-09-23"}}}
    e.update(kw)
    return e


def cs_warning(wid="balcony_load", **kw):
    e = entry(id=wid, **kw)
    return e


def cs_record(wid="balcony_load", src=("uiuc_ext",), url=URL):
    return {"field": f"container_safety.{wid}", "date": "2026-09-23", "sources": list(src),
            "note": f"PLA-581 container_safety.{wid}. {url} (raw read 2026-09-23, 1 bytes, sha256 "
                    f"{'0' * 64}); verbatim: \"x\"."}


def cw_record():
    return {"field": "critical_warnings", "date": "2026-09-23", "sources": ["uiuc_ext"],
            "note": "assessed"}


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(FIXTURE_SHA))
        cls.catalog = cls.data["source_catalog"]

    def crop(self, slug=CROP):
        return copy.deepcopy(next(c for c in self.data["crops"] if c["slug"] == slug))

    def put(self, value, record=True, slug=CROP):
        c = self.crop(slug)
        c[G.FIELD] = value
        if record:
            vs = c["verification_status"]
            vs["field_additions"] = list(vs.get("field_additions") or []) + [cw_record()]
        return c

    def shape(self, c):
        return G.shape_violations(c, self.catalog)

    def cs(self, value):
        d = {"source_catalog": self.catalog, G.DATASET_KEY: value}
        return G.dataset_violations(d)

    def good_cs(self):
        return {"warnings": [cs_warning()], "field_additions": [cs_record()]}

    def assertFires(self, V, fragment):
        self.assertTrue(V, f"expected a violation containing {fragment!r}, got none")
        self.assertTrue(any(fragment in v for v in V),
                        f"a violation fired, but not the one wanted.\n  wanted: {fragment!r}\n  got: {V}")


class Fixture(Base):
    def test_the_fixture_is_the_pinned_base(self):
        self.assertEqual(len(self.data["crops"]), 128)

    def test_the_base_carries_neither_key(self):
        """The shape rules arm GREEN on the base: neither key exists anywhere on 526788f2."""
        self.assertNotIn(G.DATASET_KEY, self.data)
        self.assertEqual(sum(1 for c in self.data["crops"] if G.FIELD in c), 0)
        self.assertEqual(G.all_violations(self.data, presence=False), [])

    def test_the_crop_fixture_is_certified_and_laddered(self):
        c = self.crop()
        self.assertTrue(G._certified(c))
        self.assertIn("harvest", G.ladder_ids(c))
        self.assertFalse(G._certified(self.crop(SHELL)))


class ThreeStates(Base):
    """Rule 1 (spec 5.2): null = not assessed, [] = assessed none found, [...] = authored."""

    def test_state_of_distinguishes_all_five(self):
        self.assertEqual(G.state_of(self.crop()), "absent")
        self.assertEqual(G.state_of(self.put(None, record=False)), "null")
        self.assertEqual(G.state_of(self.put([])), "empty")
        self.assertEqual(G.state_of(self.put([entry()])), "authored")
        self.assertEqual(G.state_of(self.put("none")), "invalid")

    def test_null_is_clean_and_needs_no_record(self):
        self.assertEqual(self.shape(self.put(None, record=False)), [])

    def test_empty_list_with_its_record_is_clean(self):
        self.assertEqual(self.shape(self.put([])), [])

    def test_empty_list_without_a_record_is_refused(self):
        """[] is a CLAIM ('assessed, none found'). A claim nobody can point at is the null->[]
        collapse the three-state rule exists to stop, so it refuses at the gate, not only in a
        promote that happens to be running."""
        self.assertFires(self.shape(self.put([], record=False)), "assessed, none found")

    def test_authored_list_without_a_record_is_refused(self):
        self.assertFires(self.shape(self.put([entry()], record=False)), "field_additions")

    def test_a_string_is_refused(self):
        self.assertFires(self.shape(self.put("none")), "null, [] or a non-empty list")

    def test_a_dict_is_refused(self):
        self.assertFires(self.shape(self.put({"entries": []})), "null, [] or a non-empty list")

    def test_a_number_is_refused(self):
        self.assertFires(self.shape(self.put(0)), "null, [] or a non-empty list")

    def test_false_is_refused(self):
        self.assertFires(self.shape(self.put(False)), "null, [] or a non-empty list")

    def test_the_key_on_an_uncertified_shell_is_refused_even_null(self):
        self.assertFires(self.shape(self.put(None, record=False, slug=SHELL)), "uncertified")

    def test_absent_key_is_not_a_shape_violation(self):
        self.assertEqual(self.shape(self.crop()), [])

    def test_presence_requires_the_key_on_a_certified_crop(self):
        self.assertFires(G.presence_violations(self.crop()), "missing")

    def test_presence_exempts_the_shells(self):
        self.assertEqual(G.presence_violations(self.crop(SHELL)), [])

    def test_presence_accepts_null(self):
        self.assertEqual(G.presence_violations(self.put(None, record=False)), [])

    def test_a_record_for_another_field_does_not_back_the_claim(self):
        c = self.put([], record=False)
        c["verification_status"]["field_additions"].append(dict(cw_record(), field="plants_per_pot"))
        self.assertFires(self.shape(c), "assessed, none found")


class EntryRules(Base):
    """Rules 2 to 8, on a crop entry."""

    def one(self, **kw):
        return self.shape(self.put([entry(**kw)]))

    def test_a_good_entry_is_clean(self):
        self.assertEqual(self.one(), [])

    def test_an_extra_key_is_refused(self):
        self.assertFires(self.shape(self.put([dict(entry(), extra=1)])), "keys must be exactly")

    def test_a_missing_key_is_refused(self):
        e = entry(); del e["severity"]
        self.assertFires(self.shape(self.put([e])), "keys must be exactly")

    def test_a_non_dict_entry_is_refused(self):
        self.assertFires(self.shape(self.put(["watch out"])), "keys must be exactly")

    def test_a_snake_case_id_is_refused_on_a_crop(self):
        self.assertFires(self.one(id="a_full_pot"), "id must be kebab-case")

    def test_an_uppercase_id_is_refused(self):
        self.assertFires(self.one(id="Heavy-Pot"), "id must be kebab-case")

    def test_an_unknown_class_is_refused(self):
        self.assertFires(self.one(**{"class": "comfort"}), "class must be one of")

    def test_an_unknown_severity_is_refused(self):
        self.assertFires(self.one(severity="medium"), "severity must be one of")

    def test_a_stage_off_the_ladder_is_refused(self):
        self.assertFires(self.one(stage="veraison"), "not a stage in this crop's own growth_stages")

    def test_a_non_string_stage_is_refused(self):
        self.assertFires(self.one(stage=3), "not a stage in this crop's own growth_stages")

    def test_an_empty_title_is_refused(self):
        self.assertFires(self.one(title="  "), "title must be a non-empty string")

    def test_a_missing_register_is_refused(self):
        self.assertFires(self.one(body_beginner=None), "body_beginner must be a non-empty string")

    def test_an_em_dash_is_refused(self):
        self.assertFires(self.one(body_seasoned="Heavy — very heavy."), "em or en dash")

    def test_an_en_dash_is_refused(self):
        self.assertFires(self.one(title="Heavy – pots"), "em or en dash")

    def test_a_double_hyphen_is_refused(self):
        self.assertFires(self.one(body_beginner="Heavy -- very."), "'--'")

    def test_empty_sources_are_refused(self):
        self.assertFires(self.one(sources=[], anchoring_urls={}), "sources must be a non-empty list")

    def test_a_sourceless_SAFETY_entry_is_refused_by_the_sources_rule(self):
        """Spec rule 9 ('a class: safety entry with an empty sources is a violation') is SUBSUMED
        by rule 8, which requires non-empty sources on EVERY entry. A separate rule-9 guard could
        never fire first, so it is not shipped; this driver proves the defect is still caught."""
        self.assertFires(self.one(**{"class": "safety", "sources": [], "anchoring_urls": {}}),
                         "sources must be a non-empty list")

    def test_a_source_not_in_the_catalog_is_refused(self):
        self.assertFires(self.one(sources=["nobody_ext"],
                                  anchoring_urls={"nobody_ext": {"url": URL, "verified": "2026-09-23"}}),
                         "not in source_catalog")

    def test_a_non_T1_source_is_refused(self):
        low = next(k for k, v in self.catalog.items() if v.get("tier") != "T1")
        self.assertFires(self.one(sources=[low],
                                  anchoring_urls={low: {"url": URL, "verified": "2026-09-23"}}),
                         "not T1")

    def test_a_source_without_an_anchor_is_refused(self):
        self.assertFires(self.one(anchoring_urls={}), "no anchoring_urls entry")

    def test_an_anchor_not_in_sources_is_refused(self):
        au = {"uiuc_ext": {"url": URL, "verified": "2026-09-23"},
              "csu_ext": {"url": URL, "verified": "2026-09-23"}}
        self.assertFires(self.one(anchoring_urls=au), "not in sources")

    def test_an_anchor_with_extra_keys_is_refused(self):
        au = {"uiuc_ext": {"url": URL, "verified": "2026-09-23", "note": "x"}}
        self.assertFires(self.one(anchoring_urls=au), "keys must be exactly")

    def test_a_non_url_is_refused(self):
        self.assertFires(self.one(anchoring_urls={"uiuc_ext": {"url": "illinois", "verified": "2026-09-23"}}),
                         "is not a url")

    def test_a_year_prefix_does_not_satisfy_the_date(self):
        """PLA-114: a guard passed on '202' matching a date. fullmatch, never search."""
        self.assertFires(self.one(anchoring_urls={"uiuc_ext": {"url": URL, "verified": "2026-09-23x"}}),
                         "not a YYYY-MM-DD date")


class NamedControls(Base):
    """The FIVE positive controls owed by name (spec 7.3). The live roster reaches none of them."""

    def test_control_1_a_stage_on_the_crops_own_ladder_is_accepted(self):
        self.assertEqual(self.shape(self.put([entry(stage="harvest")])), [])

    def test_control_1_a_stage_off_the_crops_own_ladder_is_refused(self):
        c = self.crop()
        missing = "bud-break"
        self.assertNotIn(missing, G.ladder_ids(c))
        self.assertFires(self.shape(self.put([entry(stage=missing)])),
                         "not a stage in this crop's own growth_stages")

    def test_control_1_a_stage_valid_on_another_crop_is_refused_here(self):
        """The rule is THIS crop's ladder, not the roster's 81-id union."""
        other = next(c for c in self.data["crops"]
                     if G._certified(c) and set(G.ladder_ids(c)) - set(G.ladder_ids(self.crop())))
        foreign = sorted(set(G.ladder_ids(other)) - set(G.ladder_ids(self.crop())))[0]
        self.assertFires(self.shape(self.put([entry(stage=foreign)])),
                         "not a stage in this crop's own growth_stages")

    def test_control_2_a_harvest_class_entry_is_accepted(self):
        self.assertEqual(self.shape(self.put([entry(**{"class": "harvest", "stage": "harvest"})])), [])

    def test_control_3_two_distinct_entries_on_one_crop_are_accepted(self):
        self.assertEqual(self.shape(self.put([entry(), entry(id="pick-before-frost",
                                                             **{"class": "harvest"})])), [])

    def test_control_3_two_entries_sharing_an_id_are_refused(self):
        self.assertFires(self.shape(self.put([entry(), entry(**{"class": "harvest"})])),
                         "appears twice")

    def test_control_4_empty_and_authored_both_pass_and_both_differ_from_null(self):
        empty, full, null = self.put([]), self.put([entry()]), self.put(None, record=False)
        self.assertEqual(self.shape(empty), [])
        self.assertEqual(self.shape(full), [])
        self.assertEqual({G.state_of(empty), G.state_of(full), G.state_of(null)},
                         {"empty", "authored", "null"})

    def test_control_5_the_reader_never_coerces_null_to_empty(self):
        """The `not (x or [])` idiom collapses null and [] on purpose elsewhere (PLA-533). Here it
        would make every crop read 'assessed, none' and still pass. state_of must keep them apart,
        and a [] with no record behind it must refuse."""
        self.assertNotEqual(G.state_of(self.put(None, record=False)), G.state_of(self.put([], record=False)))
        self.assertEqual(self.shape(self.put(None, record=False)), [])
        self.assertTrue(self.shape(self.put([], record=False)))


class ContainerSafety(Base):
    """Rule 10: the same entry rules on the top-level object, checked once, plus its own."""

    def test_a_good_object_is_clean(self):
        self.assertEqual(self.cs(self.good_cs()), [])

    def test_absent_is_clean_without_presence(self):
        self.assertEqual(G.dataset_violations({"source_catalog": self.catalog}), [])

    def test_absent_is_refused_with_presence(self):
        self.assertFires(G.dataset_violations({"source_catalog": self.catalog}, presence=True),
                         "missing")

    def test_null_is_refused(self):
        self.assertFires(self.cs(None), "must be an object")

    def test_wrong_top_keys_are_refused(self):
        self.assertFires(self.cs({"warnings": [cs_warning()]}), "must be an object")

    def test_empty_warnings_are_refused(self):
        self.assertFires(self.cs({"warnings": [], "field_additions": []}), "non-empty list")

    def test_a_kebab_id_is_refused_here(self):
        """container_safety ids are the spec's pinned names (balcony_load ...), snake_case."""
        v = self.good_cs()
        v["warnings"][0]["id"] = "balcony-load"
        v["field_additions"][0]["field"] = "container_safety.balcony-load"
        self.assertFires(self.cs(v), "id must be snake_case")

    def test_a_harvest_class_is_refused_here(self):
        v = self.good_cs(); v["warnings"][0]["class"] = "harvest"
        self.assertFires(self.cs(v), "class must be 'safety'")

    def test_a_non_null_stage_is_refused_here(self):
        """No crop, no ladder: the only legitimate stage is null ('a pot is heavy whenever')."""
        v = self.good_cs(); v["warnings"][0]["stage"] = "harvest"
        self.assertFires(self.cs(v), "not a stage")

    def test_a_duplicate_warning_id_is_refused(self):
        v = self.good_cs()
        v["warnings"].append(cs_warning())
        v["field_additions"].append(cs_record())
        self.assertFires(self.cs(v), "appears twice")

    def test_a_digit_is_refused(self):
        v = self.good_cs(); v["warnings"][0]["body_seasoned"] = "A pot can weigh 60 pounds wet."
        self.assertFires(self.cs(v), "states a figure")

    def test_a_spelled_number_is_refused(self):
        v = self.good_cs(); v["warnings"][0]["body_beginner"] = "Two big pots are too many."
        self.assertFires(self.cs(v), "states a figure")

    def test_a_teen_or_twenty_is_refused(self):
        for w in ("Twelve pots crowd a rail.", "Keep it under nineteen.", "Twenty is too many."):
            v = self.good_cs(); v["warnings"][0]["body_beginner"] = w
            self.assertFires(self.cs(v), "states a figure")

    def test_dozen_hundred_and_thousand_are_refused(self):
        for w in ("A dozen pots is a lot.", "A hundred pounds of mix.", "A thousand plants."):
            v = self.good_cs(); v["warnings"][0]["body_seasoned"] = w
            self.assertFires(self.cs(v), "states a figure")

    def test_thirty_through_ninety_are_refused(self):
        for w in ("Thirty pots is a lot.", "Keep it under fifty.", "Ninety is too many."):
            v = self.good_cs(); v["warnings"][0]["body_beginner"] = w
            self.assertFires(self.cs(v), "states a figure")

    def test_half_is_refused(self):
        v = self.good_cs(); v["warnings"][0]["body_seasoned"] = "Fill it only half way when wet."
        self.assertFires(self.cs(v), "states a figure")

    def test_the_ruled_word_list_is_exactly_the_ruling(self):
        """Trevor, 2026-09-23: one through twenty, thirty through ninety, half, dozen, hundred,
        thousand. Enumerated, not derived."""
        words = "|".join((G._SMALL, G._TEENS, G._TENS, G._HALF, G._LARGE)).split("|")
        self.assertEqual(len(words), 31)
        self.assertEqual(words[:10], ["one", "two", "three", "four", "five", "six", "seven", "eight",
                                      "nine", "ten"])
        self.assertEqual(words[19:27], ["twenty", "thirty", "forty", "fifty", "sixty", "seventy",
                                        "eighty", "ninety"])
        self.assertEqual(words[-4:], ["half", "dozen", "hundred", "thousand"])

    def test_a_number_with_a_unit_is_refused(self):
        v = self.good_cs(); v["warnings"][0]["title"] = "Keep it under 40 pounds"
        self.assertFires(self.cs(v), "states a figure")

    def test_the_approved_copy_that_denies_a_figure_is_accepted(self):
        """A GUARD CAN REFUSE GOOD INPUT. Spec 4.4's approved balcony copy says no source publishes
        a figure, and has to name the unit to say it. A first draft that refused bare unit words
        refused this sentence; a unit with no number states nothing."""
        v = self.good_cs()
        v["warnings"][0]["body_seasoned"] = ("No extension source publishes a pounds figure for this, "
                                             "so treat it as a question for whoever knows the structure, "
                                             "not a number you can look up.")
        self.assertEqual(self.cs(v), [])

    def test_someone_is_not_a_number(self):
        """Word boundaries: 'someone' must not read as 'one', or the rule refuses the real copy."""
        v = self.good_cs(); v["warnings"][0]["body_beginner"] = "Not over a spot where someone sits."
        self.assertEqual(self.cs(v), [])

    def test_a_missing_record_is_refused(self):
        v = self.good_cs(); v["field_additions"] = []
        self.assertFires(self.cs(v), "one field_additions record per warning")

    def test_an_extra_record_is_refused(self):
        v = self.good_cs(); v["field_additions"].append(cs_record("hanging_security"))
        self.assertFires(self.cs(v), "one field_additions record per warning")

    def test_a_record_with_the_wrong_shape_is_refused(self):
        v = self.good_cs(); v["field_additions"][0]["extra"] = 1
        self.assertFires(self.cs(v), "record keys must be exactly")

    def test_a_record_with_a_bad_date_is_refused(self):
        v = self.good_cs(); v["field_additions"][0]["date"] = "2026-09"
        self.assertFires(self.cs(v), "date is not a YYYY-MM-DD date")

    def test_a_record_with_an_em_dash_is_refused(self):
        v = self.good_cs(); v["field_additions"][0]["note"] += " — read twice."
        self.assertFires(self.cs(v), "record carries an em or en dash")

    def test_a_record_crediting_another_institution_is_refused(self):
        v = self.good_cs(); v["field_additions"][0]["sources"] = ["csu_ext"]
        self.assertFires(self.cs(v), "credits")

    def test_a_record_that_does_not_name_the_anchor_url_is_refused(self):
        v = self.good_cs(); v["field_additions"][0]["note"] = "sha256 x; verbatim: \"y\""
        self.assertFires(self.cs(v), "does not name")

    def test_a_record_that_quotes_no_digest_is_refused(self):
        v = self.good_cs(); v["field_additions"][0]["note"] = f"{URL} verbatim: \"y\""
        self.assertFires(self.cs(v), "quotes no sha256")

    def test_a_record_that_quotes_no_source_text_is_refused(self):
        v = self.good_cs(); v["field_additions"][0]["note"] = f"{URL} sha256 {'0' * 64}"
        self.assertFires(self.cs(v), "quotes no source text")

    def test_the_entry_rules_run_on_the_object(self):
        """Rule 10 is not a separate rule set: the SAME entry validator runs on these entries."""
        v = self.good_cs(); v["warnings"][0]["severity"] = "medium"
        self.assertFires(self.cs(v), "severity must be one of")
        v = self.good_cs(); v["warnings"][0]["sources"] = ["nobody_ext"]
        v["warnings"][0]["anchoring_urls"] = {"nobody_ext": {"url": URL, "verified": "2026-09-23"}}
        v["field_additions"][0]["sources"] = ["nobody_ext"]
        self.assertFires(self.cs(v), "not in source_catalog")


class RegisterRuling(Base):
    """`class` is ruled path-scoped (register_completeness), and ONLY there; the rest of an entry's
    strings were already ruled. Asserted both ways: a ruling that also exempted `class` elsewhere
    would be a hole, and one that missed critical_warnings would flood PLA-142's first entry."""

    def test_an_authored_entry_raises_no_unruled_prose(self):
        import register_completeness_gate as R
        self.assertEqual(R.register_completeness_violations(self.put([entry()])), [])

    def test_class_is_ruled_only_under_critical_warnings(self):
        import register_completeness_gate as R
        self.assertTrue(R._is_ruled("critical_warnings[]", "class"))
        self.assertFalse(R._is_ruled("container_notes", "class"))
        self.assertFalse(R._is_ruled("tips_by_stage[]", "class"))


class Wholesale(Base):
    def test_all_violations_walks_the_shells(self):
        """gate_all iterates CERTIFIED crops only, so a key on a shell is invisible to it by
        construction. This entry point walks all 128 and must see it."""
        d = copy.deepcopy(self.data)
        next(c for c in d["crops"] if c["slug"] == SHELL)[G.FIELD] = None
        self.assertTrue(any("uncertified" in v for v in G.all_violations(d)))

    def test_all_violations_includes_the_dataset_object(self):
        d = copy.deepcopy(self.data)
        d[G.DATASET_KEY] = None
        self.assertTrue(any(G.DATASET_KEY in v for v in G.all_violations(d)))

    def test_population_reports_the_three_states(self):
        d = copy.deepcopy(self.data)
        for c in d["crops"]:
            if G._certified(c):
                c[G.FIELD] = None
        p = G.population(d)
        self.assertEqual((p["null"], p["empty"], p["authored"], p["absent_certified"]), (121, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
