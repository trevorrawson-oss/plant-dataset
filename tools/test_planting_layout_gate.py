#!/usr/bin/env python3
"""Tests for planting_layout_gate (A44), rewritten for PLA-10 promote 1 (spec
docs/specs/pla10-field-shape.md §1.1, §1.2, §1.6, §2.4, §3). Run:
    python3 tools/test_planting_layout_gate.py        (also collected by pytest)

The field is a LIST of (arrangement, support) entries with one default, and the crop-root
`spacing_inches` / `row_spacing_inches` / `row_spacing_reason` are GATED MIRRORS of it.

Two states, both tested:
  * UNARMED (the tools commit, canonical c5fc3d13): the 6 legacy strings still validate under the old
    enum + block<->min_rows rule, absence is a no-op, and ANY crop already carrying a list is held to
    the full list rule. The live canonical stays green.
  * ARMED (flipped in promote 1's data commit): every certified crop carries a list, a string is
    refused, a microgreen must be [] with null mirrors, and the retired spacing anchor key is refused.

Every mutation the spec names in §1.6 check 7 has a driver here, and each driver asserts the violation
TEXT, not just "non-empty", so a defect caught for the wrong reason does not count (an earlier check
masking a later one: memory guard-tests-pass-because-an-earlier-check-fires).
"""
import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import planting_layout_gate as G  # noqa: E402

CERT = {"status": "verified_gs_arc"}
A = {"url": "https://extension.umn.edu/vegetables/growing-potatoes", "verified": "2026-10-01"}


def entry(eid="row-none", arr="row", sup="none", default=True, **kw):
    e = {"id": eid, "arrangement": arr, "support": sup, "default": default,
         "row_spacing_inches": [30, 36], "row_spacing_reason": None,
         "sources": ["umn_ext"], "anchoring_urls": {"umn_ext": dict(A)}}
    if arr in ("row", "block"):
        e["in_row_inches"] = [10, 12]
    if arr == "hill":
        e["hill_spacing_inches"] = [96, 96]
        e["plants_per_hill"] = [2, 2]
    e.update(kw)
    return e


def potato():
    """§1.4's single-entry common case."""
    return {"slug": "potato", "verification_status": dict(CERT),
            "planting_layout": [entry()],
            "spacing_inches": [10, 12], "row_spacing_inches": [30, 36], "row_spacing_reason": None}


def watermelon():
    """§1.4's hill default with a row entry behind it: the between-plants mirror falls back."""
    return {"slug": "watermelon", "verification_status": dict(CERT),
            "planting_layout": [
                entry("hill-none", "hill", row_spacing_inches=[96, 96]),
                entry("row-none", "row", default=False, in_row_inches=[60, 72],
                      row_spacing_inches=[72, 96])],
            "spacing_inches": [60, 72], "row_spacing_inches": [96, 96], "row_spacing_reason": None}


def butternut_see_layout():
    """A hill default with NO row figure and a row entry that has one: see_layout (§3)."""
    return {"slug": "butternut-squash", "verification_status": dict(CERT),
            "planting_layout": [
                entry("hill-none", "hill", hill_spacing_inches=[48, 72], plants_per_hill=[2, 3],
                      row_spacing_inches=None, row_spacing_reason="not_authored"),
                entry("row-none", "row", default=False, in_row_inches=[24, 36],
                      row_spacing_inches=[60, 72])],
            "spacing_inches": [24, 36], "row_spacing_inches": None, "row_spacing_reason": "see_layout"}


def sweet_corn():
    """§1.4's block default with a hill behind it; pollination_block_min_rows stays at the root."""
    return {"slug": "sweet-corn", "verification_status": dict(CERT),
            "planting_layout": [
                entry("block-none", "block", in_row_inches=[8, 12]),
                entry("hill-none", "hill", default=False, hill_spacing_inches=[30, 30],
                      plants_per_hill=[4, 5])],
            "pollination_block_min_rows": 4,
            "spacing_inches": [8, 12], "row_spacing_inches": [30, 36], "row_spacing_reason": None}


def cherry_tomato():
    """§1.4's support fork, with a height override on the staked entry."""
    return {"slug": "cherry-tomato", "verification_status": dict(CERT),
            "planting_layout": [
                entry("row-stake", "row", "stake", in_row_inches=[18, 24], row_spacing_inches=[36, 36],
                      mature_height_ft=[6, 8]),
                entry("row-cage", "row", "cage", default=False, in_row_inches=[24, 36],
                      row_spacing_inches=[48, 48]),
                entry("row-none", "row", default=False, in_row_inches=[36, 36],
                      row_spacing_inches=[48, 60])],
            "spacing_inches": [18, 24], "row_spacing_inches": [36, 36], "row_spacing_reason": None}


def apple_not_authored():
    return {"slug": "apple", "verification_status": dict(CERT),
            "planting_layout": [entry(in_row_inches=[144, 180], row_spacing_inches=None,
                                      row_spacing_reason="not_authored")],
            "spacing_inches": [144, 180], "row_spacing_inches": None, "row_spacing_reason": "not_authored"}


def microgreen():
    return {"slug": "wheatgrass", "verification_status": dict(CERT), "zone_independent": True,
            "planting_layout": [], "spacing_inches": None, "row_spacing_inches": None,
            "row_spacing_reason": "not_applicable"}


def strawberry_bed():
    """Two entries sharing a pair, told apart by a qualifier (promote 2's row-none-bed)."""
    return {"slug": "strawberry", "verification_status": dict(CERT),
            "planting_layout": [
                entry(in_row_inches=[15, 24], row_spacing_inches=[36, 48]),
                entry("row-none-bed", default=False, in_row_inches=[12, 12], rows_per_bed=2,
                      row_spacing_inches=[36, 36])],
            "spacing_inches": [15, 24], "row_spacing_inches": [36, 48], "row_spacing_reason": None}


CLEAN = (potato, watermelon, butternut_see_layout, sweet_corn, cherry_tomato, apple_not_authored,
         microgreen, strawberry_bed)


def legacy(pl, **kw):
    c = {"slug": "x", "verification_status": dict(CERT), "spacing_inches": [8, 12], "planting_layout": pl}
    c.update(kw)
    return c


def has(vs, *needles):
    return any(all(n in v for n in needles) for v in vs)


class PositiveControls(unittest.TestCase):
    def test_every_spec_example_passes_armed_and_unarmed(self):
        for f in CLEAN:
            for armed in (False, True):
                self.assertEqual(G.check_crop(f(), armed=armed), [], (f.__name__, armed))

    def test_mirror_helpers_read_the_spec_rules(self):
        self.assertEqual(G.expected_spacing(watermelon()["planting_layout"]), [60, 72])
        self.assertEqual(G.expected_spacing([]), None)
        self.assertEqual(G.expected_row_reason(butternut_see_layout()), "see_layout")
        self.assertEqual(G.expected_row_reason(apple_not_authored()), "not_authored")
        self.assertEqual(G.expected_row_reason(microgreen()), "not_applicable")
        self.assertEqual(G.expected_row_reason(potato()), None)


class Unarmed(unittest.TestCase):
    """The UNARMED path (the tools-commit state; armed since promote 1's data commit, so armed=False is
    passed explicitly): the legacy strings validate and their defects still bounce."""

    def test_legacy_strings_still_validate(self):
        self.assertEqual(G.check_crop(legacy("block", pollination_block_min_rows=4), armed=False), [])
        self.assertEqual(G.check_crop(legacy("row"), armed=False), [])
        self.assertEqual(G.check_crop({"slug": "x"}, armed=False), [])
        self.assertEqual(G.check_crop({"slug": "x", "planting_layout": None}, armed=False), [])

    def test_legacy_defects_still_bounce(self):
        self.assertTrue(has(G.check_crop(legacy("block"), armed=False), "pollination_block_min_rows missing"))
        self.assertTrue(has(G.check_crop(legacy("blocks"), armed=False), "not in"))
        self.assertTrue(has(G.check_crop(legacy("row", pollination_block_min_rows=4), armed=False), "not 'block'"))
        self.assertTrue(has(G.check_crop(legacy("block", pollination_block_min_rows=1), armed=False), "int >= 2"))
        self.assertTrue(has(G.check_crop(legacy("block", pollination_block_min_rows=True), armed=False), "int >= 2"))
        self.assertTrue(has(G.check_crop({"slug": "x", "pollination_block_min_rows": 4}, armed=False),
                            "planting_layout absent"))

    def test_grid_and_single_left_the_enum(self):
        """§ 'Decided in this spec': grid and single leave the arrangement enum (0 population)."""
        self.assertTrue(has(G.check_crop(legacy("grid"), armed=False), "not in"))
        self.assertTrue(has(G.check_crop(legacy("single"), armed=False), "not in"))

    def test_a_list_is_held_to_the_full_rule_even_unarmed(self):
        c = potato(); c["spacing_inches"] = [10, 14]
        self.assertTrue(has(G.check_crop(c, armed=False), "spacing_inches", "mirror"))

    def test_unarmed_does_not_demand_presence(self):
        c = {"slug": "x", "verification_status": dict(CERT), "spacing_inches": [8, 12]}
        self.assertEqual(G.check_crop(c, armed=False), [])


class Armed(unittest.TestCase):
    def test_presence_on_a_certified_crop(self):
        c = {"slug": "x", "verification_status": dict(CERT), "spacing_inches": [8, 12]}
        self.assertTrue(has(G.check_crop(c, armed=True), "planting_layout", "absent"))

    def test_presence_not_demanded_of_a_shell(self):
        c = {"slug": "olive", "verification_status": {"status": "shell"}, "spacing_inches": []}
        self.assertEqual(G.check_crop(c, armed=True), [])

    def test_the_string_form_is_retired(self):
        self.assertTrue(has(G.check_crop(legacy("block", pollination_block_min_rows=4), armed=True),
                            "string form", "retired"))

    def test_mirror_keys_must_be_present(self):
        for k in ("spacing_inches", "row_spacing_inches", "row_spacing_reason"):
            c = potato(); del c[k]
            self.assertTrue(has(G.check_crop(c, armed=True), k, "absent"), k)


class ListShape(unittest.TestCase):
    """§1.6 checks 1-6."""

    def v(self, c):
        return G.check_crop(c, armed=True)

    def test_1_not_a_list(self):
        c = potato(); c["planting_layout"] = {"id": "row-none"}
        self.assertTrue(has(self.v(c), "not a list"))

    def test_1_empty_list_off_zone_independent(self):
        c = potato(); c["planting_layout"] = []; c["spacing_inches"] = None
        self.assertTrue(has(self.v(c), "[] only on a zone_independent crop"))

    def test_1_zone_independent_with_entries(self):
        c = microgreen(); c["planting_layout"] = [entry()]
        self.assertTrue(has(self.v(c), "zone_independent", "must be []"))

    def test_2_unknown_key(self):
        c = potato(); c["planting_layout"][0]["method"] = "row"
        self.assertTrue(has(self.v(c), "unknown key", "method"))

    def test_2_missing_required_key(self):
        for k in ("id", "arrangement", "support", "default", "in_row_inches", "row_spacing_inches",
                  "row_spacing_reason", "sources", "anchoring_urls"):
            c = potato(); del c["planting_layout"][0][k]
            self.assertTrue(has(self.v(c), "missing", k), k)

    def test_2_closed_enums(self):
        c = potato(); c["planting_layout"][0]["arrangement"] = "grid"
        self.assertTrue(has(self.v(c), "arrangement", "grid"))
        c = potato(); c["planting_layout"][0]["support"] = "vertical"
        self.assertTrue(has(self.v(c), "support", "vertical"))

    def test_2_id_must_match_its_pair(self):
        c = potato(); c["planting_layout"][0]["id"] = "hill-none"
        self.assertTrue(has(self.v(c), "id", "does not match its pair"))
        c = potato(); c["planting_layout"][0]["id"] = "Row-None"
        self.assertTrue(has(self.v(c), "id", "pattern"))

    def test_2_duplicate_id(self):
        c = strawberry_bed(); c["planting_layout"][1]["id"] = "row-none"
        self.assertTrue(has(self.v(c), "duplicate id"))

    def test_2_shared_pair_without_a_qualifier(self):
        c = cherry_tomato(); c["planting_layout"][1]["support"] = "stake"; c["planting_layout"][1]["id"] = "row-stake"
        self.assertTrue(has(self.v(c), "duplicate id") or has(self.v(c), "pair"))

    def test_2_qualifier_without_a_shared_pair(self):
        c = potato(); c["planting_layout"][0]["id"] = "row-none-bed"
        self.assertTrue(has(self.v(c), "qualifier"))

    def test_2_sources_and_anchors(self):
        c = potato(); c["planting_layout"][0]["sources"] = []
        self.assertTrue(has(self.v(c), "sources"))
        c = potato(); c["planting_layout"][0]["anchoring_urls"] = {}
        self.assertTrue(has(self.v(c), "anchoring_urls", "umn_ext"))
        c = potato(); c["planting_layout"][0]["anchoring_urls"]["umn_ext"] = {"url": "", "verified": "2026-10-01"}
        self.assertTrue(has(self.v(c), "anchoring_urls", "url"))

    def test_3_exactly_one_default(self):
        c = watermelon(); c["planting_layout"][1]["default"] = True
        self.assertTrue(has(self.v(c), "exactly one default", "2"))
        c = potato(); c["planting_layout"][0]["default"] = False
        self.assertTrue(has(self.v(c), "exactly one default", "0"))
        c = potato(); c["planting_layout"][0]["default"] = 1
        self.assertTrue(has(self.v(c), "default", "bool"))

    def test_4_hill_needs_its_keys_and_row_needs_in_row(self):
        c = watermelon(); del c["planting_layout"][0]["plants_per_hill"]
        self.assertTrue(has(self.v(c), "missing", "plants_per_hill"))
        c = potato(); c["planting_layout"][0]["plants_per_hill"] = [2, 2]
        self.assertTrue(has(self.v(c), "unknown key", "plants_per_hill"))
        c = potato(); c["planting_layout"][0]["hill_spacing_inches"] = [30, 30]
        self.assertTrue(has(self.v(c), "unknown key", "hill_spacing_inches"))

    def test_4_block_iff_min_rows(self):
        c = sweet_corn(); del c["pollination_block_min_rows"]
        self.assertTrue(has(self.v(c), "block entry", "pollination_block_min_rows"))
        c = potato(); c["pollination_block_min_rows"] = 4
        self.assertTrue(has(self.v(c), "pollination_block_min_rows", "no block entry"))
        c = sweet_corn(); c["pollination_block_min_rows"] = 1
        self.assertTrue(has(self.v(c), "pollination_block_min_rows", "int >= 2"))

    def test_5_pairs(self):
        for bad in ([12, 10], [0, 4], [10], [10, "12"], [True, 2], None):
            c = potato(); c["planting_layout"][0]["in_row_inches"] = bad
            c["spacing_inches"] = bad
            self.assertTrue(has(self.v(c), "in_row_inches", "[lo, hi]"), bad)
        c = watermelon(); c["planting_layout"][0]["plants_per_hill"] = [1.5, 2]
        self.assertTrue(has(self.v(c), "plants_per_hill", "whole"))

    def test_5_entry_row_null_iff_not_authored(self):
        c = potato(); c["planting_layout"][0]["row_spacing_reason"] = "not_authored"
        self.assertTrue(has(self.v(c), "row_spacing_reason", "row_spacing_inches"))
        c = apple_not_authored(); c["planting_layout"][0]["row_spacing_reason"] = None
        self.assertTrue(has(self.v(c), "row_spacing_reason", "row_spacing_inches"))

    def test_5_entry_reason_is_never_see_layout_or_not_applicable(self):
        for r in ("see_layout", "not_applicable"):
            c = apple_not_authored(); c["planting_layout"][0]["row_spacing_reason"] = r
            self.assertTrue(has(self.v(c), "row_spacing_reason", "crop-root"), r)

    def test_5_rows_per_bed(self):
        c = strawberry_bed(); c["planting_layout"][1]["rows_per_bed"] = 1
        self.assertTrue(has(self.v(c), "rows_per_bed"))
        c = watermelon(); c["planting_layout"][0]["rows_per_bed"] = 2
        self.assertTrue(has(self.v(c), "unknown key", "rows_per_bed"))

    def test_6_height_override_only_on_support(self):
        c = potato(); c["planting_layout"][0]["mature_height_ft"] = [2, 3]
        self.assertTrue(has(self.v(c), "mature_height_ft", "support"))
        c = cherry_tomato(); c["planting_layout"][0]["mature_height_ft"] = [8, 6]
        self.assertTrue(has(self.v(c), "mature_height_ft", "[lo, hi]"))


class R5Migration(unittest.TestCase):
    """R5: an entry may ship UNCITED only as the (crop, entry id) an R5 migration waiver names. A44
    permits the empty citation slots there and nowhere else; byte-equality to the pre-promote spacing
    is A62's check (sourced_block_ratchet_gate.migration_verdict), never retyped here."""

    def bok(self):
        c = potato(); c["slug"] = "bok-choy"
        c["planting_layout"][0].update(sources=[], anchoring_urls={})
        return c

    def waive(self, slug, eid):
        import planting_layout_migration_known as M
        saved = dict(M.WAIVERS)
        M.WAIVERS.clear(); M.WAIVERS[slug] = {"entry_id": eid, "in_row_inches": [10, 12], "hunt": "t"}
        self.addCleanup(lambda: (M.WAIVERS.clear(), M.WAIVERS.update(saved)))

    def test_an_uncited_entry_fails_without_a_waiver(self):
        self.assertTrue(has(G.check_crop(self.bok(), armed=True), "sources"))

    def test_the_waived_entry_may_be_uncited(self):
        self.waive("bok-choy", "row-none")
        self.assertEqual(G.check_crop(self.bok(), armed=True), [])

    def test_the_waiver_covers_only_its_entry(self):
        self.waive("bok-choy", "row-stake")
        self.assertTrue(has(G.check_crop(self.bok(), armed=True), "sources"))

    def test_a_waived_entry_still_needs_both_slots_empty_not_half(self):
        self.waive("bok-choy", "row-none")
        c = self.bok(); c["planting_layout"][0]["anchoring_urls"] = {"umn_ext": dict(A)}
        self.assertTrue(has(G.check_crop(c, armed=True), "anchoring_urls"))


class Mirrors(unittest.TestCase):
    """§1.6 check 7: every mutation the spec names, by name."""

    def v(self, c):
        return G.check_crop(c, armed=True)

    def test_mirror_taken_from_the_second_carrier_while_the_default_carries_one(self):
        c = cherry_tomato(); c["spacing_inches"] = [24, 36]   # the caged figure, today's live value
        self.assertTrue(has(self.v(c), "spacing_inches", "mirror", "[18, 24]"))

    def test_the_default_wins_even_when_declared_second(self):
        """Positive control for an otherwise invisible mutation: every other fixture declares its
        default first, so a mirror that ignored `default` and took declared order would pass them."""
        c = cherry_tomato(); c["planting_layout"] = [c["planting_layout"][1], c["planting_layout"][0],
                                                     c["planting_layout"][2]]
        self.assertEqual(self.v(c), [])
        self.assertEqual(G.expected_spacing(c["planting_layout"]), [18, 24])
        c["spacing_inches"] = [24, 36]
        self.assertTrue(has(self.v(c), "spacing_inches", "mirror"))

    def test_mirror_follows_declared_order_after_the_default(self):
        c = watermelon()
        c["planting_layout"].append(entry("row-trellis", "row", "trellis", default=False,
                                          in_row_inches=[24, 24], row_spacing_inches=None,
                                          row_spacing_reason="not_authored"))
        self.assertEqual(self.v(c), [])
        c["spacing_inches"] = [24, 24]
        self.assertTrue(has(self.v(c), "spacing_inches", "mirror"))

    def test_mirror_non_null_when_no_entry_carries_one(self):
        c = watermelon(); del c["planting_layout"][1]
        c["row_spacing_reason"] = None
        self.assertTrue(has(self.v(c), "spacing_inches", "null"))

    def test_mirror_null_when_an_entry_carries_one(self):
        c = potato(); c["spacing_inches"] = None
        self.assertTrue(has(self.v(c), "spacing_inches", "mirror"))

    def test_an_empty_list_mirror_surviving_on_a_zone_independent_crop(self):
        c = microgreen(); c["spacing_inches"] = []
        self.assertTrue(has(self.v(c), "spacing_inches", "null"))

    def test_zone_independent_rows_and_reason(self):
        c = microgreen(); c["row_spacing_reason"] = "not_authored"
        self.assertTrue(has(self.v(c), "row_spacing_reason", "not_applicable"))
        c = microgreen(); c["row_spacing_inches"] = [12, 12]
        self.assertTrue(has(self.v(c), "row_spacing_inches"))

    def test_not_applicable_off_zone_independent(self):
        c = apple_not_authored(); c["row_spacing_reason"] = "not_applicable"
        self.assertTrue(has(self.v(c), "row_spacing_reason", "not_authored"))

    def test_crop_root_row_borrowed_from_a_non_default_entry(self):
        c = butternut_see_layout(); c["row_spacing_inches"] = [60, 72]; c["row_spacing_reason"] = None
        self.assertTrue(has(self.v(c), "row_spacing_inches", "default"))

    def test_crop_root_row_differs_from_the_default(self):
        c = potato(); c["row_spacing_inches"] = [30, 40]
        self.assertTrue(has(self.v(c), "row_spacing_inches", "default"))

    def test_see_layout_on_a_row_default(self):
        c = apple_not_authored()
        c["planting_layout"].append(entry("row-stake", "row", "stake", default=False,
                                          in_row_inches=[72, 96], row_spacing_inches=[120, 120]))
        self.assertEqual(self.v(c), [])
        c["row_spacing_reason"] = "see_layout"
        self.assertTrue(has(self.v(c), "row_spacing_reason", "not_authored"))

    def test_see_layout_on_a_block_default(self):
        c = sweet_corn(); c["planting_layout"][0]["row_spacing_inches"] = None
        c["planting_layout"][0]["row_spacing_reason"] = "not_authored"
        c["planting_layout"][1]["row_spacing_inches"] = [30, 36]
        c["row_spacing_inches"] = None; c["row_spacing_reason"] = "see_layout"
        self.assertTrue(has(self.v(c), "row_spacing_reason", "not_authored"))

    def test_see_layout_with_no_entry_carrying_a_row_figure(self):
        c = butternut_see_layout(); c["planting_layout"][1]["row_spacing_inches"] = None
        c["planting_layout"][1]["row_spacing_reason"] = "not_authored"
        self.assertTrue(has(self.v(c), "row_spacing_reason", "not_authored"))

    def test_not_authored_where_see_layout_holds(self):
        c = butternut_see_layout(); c["row_spacing_reason"] = "not_authored"
        self.assertTrue(has(self.v(c), "row_spacing_reason", "see_layout"))

    def test_reason_non_null_while_row_present(self):
        c = potato(); c["row_spacing_reason"] = "not_authored"
        self.assertTrue(has(self.v(c), "row_spacing_reason", "null"))


class RetiredAnchors(unittest.TestCase):
    """§1.6 check 8: a second authored copy of the in-row figure cannot reappear."""

    def test_spacing_inches_anchoring_urls_refused_by_name(self):
        c = potato(); c["spacing_inches_anchoring_urls"] = {"umn_ext": dict(A)}
        self.assertTrue(has(G.check_crop(c, armed=True), "spacing_inches_anchoring_urls", "retired"))
        self.assertTrue(has(G.check_crop(c, armed=False), "spacing_inches_anchoring_urls", "retired"))

    def test_spacing_inches_sources_refused_by_name(self):
        c = potato(); c["spacing_inches_sources"] = ["umn_ext"]
        self.assertTrue(has(G.check_crop(c, armed=True), "spacing_inches_sources"))

    def test_a_legacy_crop_may_keep_its_anchor_until_armed(self):
        c = legacy("row"); c["spacing_inches_anchoring_urls"] = {"umn_ext": dict(A)}
        self.assertEqual(G.check_crop(c, armed=False), [])
        self.assertTrue(has(G.check_crop(c, armed=True), "spacing_inches_anchoring_urls"))


class Roster(unittest.TestCase):
    """§1.6 check 9: the population is reported and a short one REFUSES."""

    def data(self, n_extra=0):
        crops = [f() for f in CLEAN]
        for i in range(n_extra):
            c = potato(); c["slug"] = f"p{i}"; crops.append(c)
        return {"crops": crops}

    def test_reports_crops_and_entries(self):
        r = G.roster(self.data(), armed=True)
        self.assertEqual(r["certified"], len(CLEAN))
        self.assertEqual(r["entries"], 1 + 2 + 2 + 2 + 3 + 1 + 0 + 2)
        self.assertEqual(r["list_shaped"], len(CLEAN))
        self.assertEqual(r["violations"], [])

    def test_refuses_below_the_crop_floor(self):
        r = G.roster(self.data(), armed=True)
        self.assertIn("below the declared floor", G.refusal(r, armed=True))
        self.assertIn("below the declared floor", G.refusal(r, armed=False))

    def test_refuses_an_empty_roster(self):
        r = G.roster({"crops": []}, armed=False)
        self.assertIn("0 certified", G.refusal(r, armed=False))

    def test_entry_floor_applies_only_armed(self):
        r = G.roster(self.data(n_extra=G.CERT_FLOOR), armed=True)
        self.assertIsNone(G.refusal(dict(r, entries=G.ENTRY_FLOOR), armed=True))
        self.assertIn("entries", G.refusal(dict(r, entries=G.ENTRY_FLOOR - 1), armed=True))
        self.assertIsNone(G.refusal(dict(r, entries=0), armed=False))

    def test_floors_are_literals(self):
        """Never derived from the walk (memory computed-guard-expectations-are-vacuous)."""
        self.assertEqual((G.CERT_FLOOR, G.ENTRY_FLOOR), (121, 113))

    def test_the_data_commit_ships_armed(self):
        """Armed in promote 1's data commit (gates arm off the data), together with this assertion,
        which read `PRESENCE_ARMED is False` in the tools commit (f6de39a)."""
        self.assertIs(G.PRESENCE_ARMED, True)


U = {"url": "https://extension.umd.edu/sites/extension.umd.edu/files/publications/AllAboutAppleRootStocks.pdf",
     "verified": "2026-06-11"}
N = {"url": "https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts",
     "verified": "2026-10-02"}


def rs_row(name, override="absent", cited=True):
    """A rootstock_options row as apple carries it; `override` "absent" leaves the key off."""
    r = {"name": name, "size_class": "dwarf", "mature_height_ft": [8, 12], "spread_ft": 8,
         "sources": ["umd_ext"], "anchoring_urls": {"umd_ext": dict(U)}}
    if override != "absent":
        r["spacing_inches"] = override
        if override is not None and cited:
            r["sources"] = ["umd_ext", "ncsu_ext_handbook_tree_fruit"]
            r["anchoring_urls"]["ncsu_ext_handbook_tree_fruit"] = dict(N)
    return r


def apple_overrides():
    """Promote 2's apple: every row carries the key (M26 null = the crop basis), each override cited."""
    c = apple_not_authored()
    c["rootstock_options"] = [rs_row("M9", [48, 96]), rs_row("M26", None), rs_row("MM106", [144, 192]),
                              rs_row("MM111", [168, 216]), rs_row("seedling", [216, 300])]
    return c


def apple_no_overrides():
    c = apple_not_authored()
    c["rootstock_options"] = [rs_row("M9"), rs_row("M26")]
    return c


class RootstockOverride(unittest.TestCase):
    """PLA-10 promote 2, T2 (plan 58 §4): rootstock_options[].spacing_inches is all-or-none on a crop,
    each null or [lo, hi], and a non-null override is cited AND anchored on its own row. Unarmed until
    the data; armed, the literal crop list must carry it."""

    def test_clean_overrides_and_no_overrides_pass_in_every_state(self):
        for f in (apple_overrides, apple_no_overrides, potato):
            for armed in (False, True):
                self.assertEqual(G.check_crop(f(), armed=armed, rootstock_armed=False), [], f.__name__)
        self.assertEqual(G.check_crop(apple_overrides(), rootstock_armed=True), [])

    def test_all_or_none_on_a_crop(self):
        c = apple_overrides(); del c["rootstock_options"][3]["spacing_inches"]
        self.assertTrue(has(G.check_crop(c), "apple: rootstock_options spacing_inches is on 4 of 5 rows",
                            "all-or-none", "missing on ['MM111']"))

    def test_a_single_carrier_is_held_too(self):
        c = apple_no_overrides(); c["rootstock_options"][0]["spacing_inches"] = None
        self.assertTrue(has(G.check_crop(c), "spacing_inches is on 1 of 2 rows", "missing on ['M26']"))

    def test_each_value_is_null_or_a_pair(self):
        for bad in ([96, 48], [48], "4-8 ft", 48, [0, 48], [True, 48]):
            c = apple_overrides(); c["rootstock_options"][0]["spacing_inches"] = bad
            self.assertTrue(has(G.check_crop(c), "apple: rootstock_options[0] (M9): spacing_inches",
                                "is not null or a [lo, hi] pair"), bad)

    def test_a_non_null_override_with_no_source(self):
        c = apple_overrides(); r = c["rootstock_options"][2]
        r["sources"], r["anchoring_urls"] = [], {}
        self.assertTrue(has(G.check_crop(c), "apple: rootstock_options[2] (MM106): spacing_inches [144, 192]",
                            "the row cites no source"))

    def test_a_non_null_override_whose_source_is_not_anchored(self):
        c = apple_overrides(); del c["rootstock_options"][2]["anchoring_urls"]["ncsu_ext_handbook_tree_fruit"]
        self.assertTrue(has(G.check_crop(c), "rootstock_options[2] (MM106)",
                            "source 'ncsu_ext_handbook_tree_fruit' has no http(s) anchoring url"))
        c = apple_overrides(); c["rootstock_options"][2]["anchoring_urls"]["ncsu_ext_handbook_tree_fruit"]["url"] = "n/a"
        self.assertTrue(has(G.check_crop(c), "source 'ncsu_ext_handbook_tree_fruit' has no http(s) anchoring url"))

    def test_a_null_override_needs_no_new_source(self):
        c = apple_overrides()
        self.assertEqual(c["rootstock_options"][1]["sources"], ["umd_ext"])
        self.assertEqual(G.check_crop(c, rootstock_armed=True), [])

    def test_armed_the_literal_list_must_carry_it(self):
        self.assertTrue(has(G.check_crop(apple_no_overrides(), rootstock_armed=True),
                            "apple: no rootstock_options[].spacing_inches", "armed for ['apple']"))
        self.assertEqual(G.check_crop(apple_no_overrides(), rootstock_armed=False), [])
        c = apple_no_overrides(); c["verification_status"] = {"status": "shell"}
        self.assertEqual(G.check_crop(c, rootstock_armed=True), [])

    def test_violations_reach_every_layout_path(self):
        """The rootstock check is not behind the list path's early returns: a legacy string, an absent
        layout and a list each carry it."""
        for pl in ("row", None):
            c = apple_overrides(); c["planting_layout"] = pl
            c["rootstock_options"][0]["spacing_inches"] = [96, 48]
            self.assertTrue(has(G.check_crop(c, armed=False), "rootstock_options[0] (M9)"), pl)

    def test_roster_reports_the_rows_it_inspected(self):
        r = G.roster({"crops": [apple_overrides(), potato()]}, armed=True)
        self.assertEqual((r["rootstock_crops"], r["rootstock_rows"]), (1, 5))
        self.assertIn("rootstock overrides on 1 crop(s), 5 row(s)", G.summary(r, armed=True))

    def test_armed_refuses_below_the_row_floor(self):
        r = G.roster({"crops": [apple_overrides()] + [potato() for _ in range(G.CERT_FLOOR)]}, armed=True)
        r = dict(r, entries=G.ENTRY_FLOOR)
        self.assertIsNone(G.refusal(r, armed=True, rootstock_armed=True))
        self.assertIn("rootstock override row", G.refusal(dict(r, rootstock_rows=4), armed=True,
                                                           rootstock_armed=True))
        self.assertIsNone(G.refusal(dict(r, rootstock_rows=0), armed=True, rootstock_armed=False))

    def test_the_literals(self):
        self.assertEqual((G.ROOTSTOCK_OVERRIDE_CROPS, G.ROOTSTOCK_ROW_FLOOR), (("apple",), 5))

    def test_the_tools_commit_ships_unarmed(self):
        """Arms in promote 2's DATA commit with the overrides (gates arm off the data)."""
        self.assertIs(G.ROOTSTOCK_OVERRIDE_ARMED, False)


if __name__ == "__main__":
    import io
    stream = io.StringIO()
    res = unittest.TextTestRunner(stream=stream, verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    print(stream.getvalue())
    if not res.wasSuccessful():
        raise SystemExit(1)
    print(f"PASS test_planting_layout_gate ({res.testsRun} tests)")
