#!/usr/bin/env python3
"""Unit tests for plants_per_pot_gate -- A60 (PLA-580 spec 2026-09-21, section 8; register row 31).

TDD: this file was written and run RED before plants_per_pot_gate.py existed.

THREE OUTCOMES, everywhere absence is possible. The field's value domain is enumerated once, here,
because `[]` is a CLAIM and a shape gate cannot see an absence:
  key ABSENT      -- an uncertified shell. A violation on a certified crop (presence floor).
  value null      -- "no T1 count read". The legitimate state of 114 certified crops.
  {readings:[..]} -- one or more readings, each a count at a stated pot size.
  {readings: []}  -- NOT a legitimate value. Absence is spelled null. The gate refuses it.
"""
import copy
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plants_per_pot_gate as G  # noqa: E402
import numeric_sanity_gate as NSG  # noqa: E402

CERT = {"status": "verified_gs_arc", "field_additions": [{"field": "plants_per_pot"}]}
SHELL = {"status": None, "field_additions": []}

READING = {
    "count": [4, 6],
    "at_gallons": [1, 1],
    "sources": ["uiuc_ext"],
    "anchoring_urls": {"uiuc_ext": {"url": "https://extension.illinois.edu/x", "verified": "2026-09-21"}},
}


def crop(value="__absent__", *, ok=True, cert=True, extra_cn=None, vs=None):
    cn = {"container_ok": ok, "min_pot_gallons": 1}
    if value != "__absent__":
        cn["plants_per_pot"] = value
    if extra_cn:
        cn.update(extra_cn)
    return {
        "slug": "testcrop",
        "container_notes": cn,
        "verification_status": copy.deepcopy(vs if vs is not None else (CERT if cert else SHELL)),
    }


def reading(**over):
    r = copy.deepcopy(READING)
    r.update(over)
    return r


def obj(*readings):
    return {"readings": [copy.deepcopy(r) for r in readings]}


class ThreeOutcomes(unittest.TestCase):
    def test_key_absent_is_silent_in_shape(self):
        """SHAPE fires only when the key is present, so the gate arms GREEN on a state
        that carries no values anywhere (079e3923 carries 0)."""
        self.assertEqual(G.shape_violations(crop()), [])

    def test_null_is_legitimate(self):
        self.assertEqual(G.shape_violations(crop(None)), [])

    def test_a_reading_is_legitimate(self):
        self.assertEqual(G.shape_violations(crop(obj(READING))), [])

    def test_empty_readings_list_is_refused(self):
        """`[]` would assert 'assessed, none found'. Absence is spelled null."""
        v = G.shape_violations(crop({"readings": []}))
        self.assertTrue(any("non-empty" in m for m in v), v)

    def test_a_refusal_spec_pass_is_not_vacuous(self):
        """The gate staying green on the 8 real readings is a REFUSAL-SPEC pass: assert the
        matcher BOTH ways, so a gate that refused good input could not read as coverage."""
        self.assertEqual(G.shape_violations(crop(obj(READING))), [])
        self.assertNotEqual(G.shape_violations(crop(obj(reading(count=[0, 6])))), [])


class ValueShape(unittest.TestCase):
    def test_refuses_a_bare_array(self):
        v = G.shape_violations(crop([4, 6]))
        self.assertTrue(any("readings" in m for m in v), v)

    def test_refuses_an_extra_top_key(self):
        v = G.shape_violations(crop({"readings": [READING], "note": "x"}))
        self.assertTrue(any("only key" in m or "readings" in m for m in v), v)

    def test_refuses_a_reading_with_wrong_keys(self):
        r = reading(); del r["sources"]
        v = G.shape_violations(crop(obj(r)))
        self.assertTrue(any("keys must be exactly" in m for m in v), v)

    def test_refuses_a_reading_with_an_extra_key(self):
        v = G.shape_violations(crop(obj(reading(note="x"))))
        self.assertTrue(any("keys must be exactly" in m for m in v), v)

    def test_a_count_without_its_pot_size_is_refused(self):
        """Spec section 8 states this rule by name: what the gate DOES check (having refused to
        compare at_gallons against min_pot_gallons) is that at_gallons is present whenever count
        is. It falls out of the exact-key-set rule, and is asserted here under its own name so a
        later relaxation of that rule cannot drop it silently."""
        r = reading(); del r["at_gallons"]
        v = G.shape_violations(crop(obj(r)))
        self.assertTrue(any("keys must be exactly" in m for m in v), v)
        self.assertIn("count", r)  # the count is still there: a count with no pot size


class Count(unittest.TestCase):
    def test_refuses_a_scalar_count(self):
        v = G.shape_violations(crop(obj(reading(count=4))))
        self.assertTrue(any("two integers" in m for m in v), v)

    def test_refuses_a_one_element_count(self):
        v = G.shape_violations(crop(obj(reading(count=[4]))))
        self.assertTrue(any("two integers" in m for m in v), v)

    def test_refuses_a_float_count(self):
        v = G.shape_violations(crop(obj(reading(count=[1.5, 2]))))
        self.assertTrue(any("two integers" in m for m in v), v)

    def test_refuses_a_bool_count(self):
        """True is an int in Python. A count of `true` must not pass as 1."""
        v = G.shape_violations(crop(obj(reading(count=[True, 2]))))
        self.assertTrue(any("two integers" in m for m in v), v)

    def test_refuses_a_zero_minimum(self):
        v = G.shape_violations(crop(obj(reading(count=[0, 6]))))
        self.assertTrue(any("at least 1" in m for m in v), v)

    def test_refuses_an_inverted_count(self):
        v = G.shape_violations(crop(obj(reading(count=[6, 4]))))
        self.assertTrue(any("min <= max" in m for m in v), v)

    def test_accepts_a_point_count(self):
        self.assertEqual(G.shape_violations(crop(obj(reading(count=[1, 1])))), [])


class AtGallons(unittest.TestCase):
    def test_refuses_a_scalar_at_gallons(self):
        """Amendment 3: one type per field. A scalar is a violation, not a shorthand."""
        v = G.shape_violations(crop(obj(reading(at_gallons=1))))
        self.assertTrue(any("two-element list" in m for m in v), v)

    def test_refuses_a_one_element_at_gallons(self):
        v = G.shape_violations(crop(obj(reading(at_gallons=[8]))))
        self.assertTrue(any("two-element list" in m for m in v), v)

    def test_refuses_a_zero_at_gallons(self):
        v = G.shape_violations(crop(obj(reading(at_gallons=[0, 1]))))
        self.assertTrue(any("positive" in m for m in v), v)

    def test_refuses_an_inverted_at_gallons(self):
        v = G.shape_violations(crop(obj(reading(at_gallons=[10, 8]))))
        self.assertTrue(any("lo <= hi" in m for m in v), v)

    def test_accepts_a_half_gallon(self):
        """Illinois publishes a half-gallon row; the field must carry it."""
        self.assertEqual(G.shape_violations(crop(obj(reading(at_gallons=[0.5, 0.5])))), [])

    def test_accepts_a_band(self):
        """UMD's 'Minimum 8-10 gallons' is the only genuine band in either source."""
        self.assertEqual(G.shape_violations(crop(obj(reading(at_gallons=[8, 10])))), [])

    def test_does_not_require_at_gallons_to_reach_min_pot_gallons(self):
        """MEASURED: that assertion fails on 9 of 10 authored rows. It is the confusion the
        spec exists to prevent, and the gate must NOT make it (spec section 8)."""
        c = crop(obj(reading(at_gallons=[1, 1])), extra_cn={"min_pot_gallons": 15})
        self.assertEqual(G.shape_violations(c), [])


class Sources(unittest.TestCase):
    def test_refuses_empty_sources(self):
        v = G.shape_violations(crop(obj(reading(sources=[]))))
        self.assertTrue(any("non-empty list of source keys" in m for m in v), v)

    def test_refuses_a_source_with_no_anchor(self):
        v = G.shape_violations(crop(obj(reading(sources=["uiuc_ext", "umd_ext"]))))
        self.assertTrue(any("no anchoring_urls entry" in m for m in v), v)

    def test_refuses_an_anchor_with_wrong_keys(self):
        r = reading(anchoring_urls={"uiuc_ext": {"url": "https://x/y"}})
        v = G.shape_violations(crop(obj(r)))
        self.assertTrue(any("keys must be exactly" in m for m in v), v)

    def test_refuses_a_non_url(self):
        r = reading(anchoring_urls={"uiuc_ext": {"url": "see the page", "verified": "2026-09-21"}})
        v = G.shape_violations(crop(obj(r)))
        self.assertTrue(any("is not a url" in m for m in v), v)

    def test_refuses_a_verified_that_is_not_a_date(self):
        r = reading(anchoring_urls={"uiuc_ext": {"url": "https://x/y", "verified": "2026"}})
        v = G.shape_violations(crop(obj(r)))
        self.assertTrue(any("YYYY-MM-DD" in m for m in v), v)

    def test_a_year_prefix_does_not_satisfy_the_date(self):
        """PLA-114: a guard passed on '202' matching an accessed date. Match the WHOLE date."""
        r = reading(anchoring_urls={"uiuc_ext": {"url": "https://x/y", "verified": "2026-09-21-extra"}})
        v = G.shape_violations(crop(obj(r)))
        self.assertTrue(any("YYYY-MM-DD" in m for m in v), v)

    def test_refuses_an_anchor_for_a_source_not_claimed(self):
        r = reading(anchoring_urls={
            "uiuc_ext": {"url": "https://x/y", "verified": "2026-09-21"},
            "stray_ext": {"url": "https://x/z", "verified": "2026-09-21"}})
        v = G.shape_violations(crop(obj(r)))
        self.assertTrue(any("not in sources" in m for m in v), v)

    def test_refuses_two_readings_sharing_a_source(self):
        """Two readings from one institution are one institution disagreeing with itself."""
        v = G.shape_violations(crop(obj(READING, reading(count=[1, 1], at_gallons=[8, 10]))))
        self.assertTrue(any("two readings" in m for m in v), v)

    def test_accepts_two_readings_from_different_sources(self):
        second = reading(count=[1, 1], at_gallons=[8, 10], sources=["umd_ext"],
                         anchoring_urls={"umd_ext": {"url": "https://extension.umd.edu/x",
                                                     "verified": "2026-09-21"}})
        self.assertEqual(G.shape_violations(crop(obj(READING, second))), [])


class Coupling(unittest.TestCase):
    def test_refuses_a_reading_on_a_crop_that_cannot_go_in_a_pot(self):
        v = G.shape_violations(crop(obj(READING), ok=False))
        self.assertTrue(any("container_ok" in m for m in v), v)

    def test_refuses_a_reading_where_container_ok_is_null(self):
        v = G.shape_violations(crop(obj(READING), ok=None))
        self.assertTrue(any("container_ok" in m for m in v), v)

    def test_null_is_fine_on_a_crop_that_cannot_go_in_a_pot(self):
        self.assertEqual(G.shape_violations(crop(None, ok=False)), [])

    def test_refuses_an_authored_value_with_no_provenance_record(self):
        c = crop(obj(READING), vs={"status": "verified_gs_arc", "field_additions": []})
        v = G.shape_violations(c)
        self.assertTrue(any("field_additions" in m for m in v), v)

    def test_a_record_for_another_field_is_not_provenance(self):
        c = crop(obj(READING), vs={"status": "verified_gs_arc",
                                   "field_additions": [{"field": "plant_dimensions"}]})
        v = G.shape_violations(c)
        self.assertTrue(any("field_additions" in m for m in v), v)

    def test_null_needs_no_provenance_record(self):
        c = crop(None, vs={"status": "verified_gs_arc", "field_additions": []})
        self.assertEqual(G.shape_violations(c), [])


class Shells(unittest.TestCase):
    def test_refuses_the_key_on_an_uncertified_shell(self):
        """The 7 shells carry NO key; that is how A39 exempts them by status."""
        v = G.shape_violations(crop(None, cert=False))
        self.assertTrue(any("uncertified" in m for m in v), v)

    def test_an_uncertified_crop_with_no_key_is_clean(self):
        self.assertEqual(G.shape_violations(crop(cert=False)), [])

    def test_presence_exempts_an_uncertified_crop(self):
        self.assertEqual(G.presence_violations(crop(cert=False)), [])

    def test_presence_requires_the_key_on_a_certified_crop(self):
        v = G.presence_violations(crop())
        self.assertTrue(any("missing" in m for m in v), v)

    def test_presence_is_satisfied_by_null(self):
        self.assertEqual(G.presence_violations(crop(None)), [])


class ConsumerContract(unittest.TestCase):
    """The RULED formula (spec 4.2 / 4.3 / 5.2), as the oracle PLA-539 and PLA-586 implement."""

    def test_no_reading_means_fall_back(self):
        """5.2's ruling: one plant per min_pot_gallons pot. None is how the oracle says so."""
        self.assertIsNone(G.planner_gallons_per_plant(crop(None)))
        self.assertIsNone(G.planner_gallons_per_plant(crop()))

    def test_count_one_readings_do_not_switch(self):
        """Ruling 3. eggplant's shape exactly: two readings, both count-1."""
        second = reading(count=[1, 1], at_gallons=[8, 10], sources=["umd_ext"],
                         anchoring_urls={"umd_ext": {"url": "https://extension.umd.edu/x",
                                                     "verified": "2026-09-21"}})
        c = crop(obj(reading(count=[1, 1], at_gallons=[2, 2]), second))
        self.assertIsNone(G.planner_gallons_per_plant(c))

    def test_a_one_to_two_reading_does_switch(self):
        """Spec 4.2: 'A reading of [1, 2] is not a count-1 row and does switch.'"""
        c = crop(obj(reading(count=[1, 2], at_gallons=[1, 1])))
        self.assertEqual(G.planner_gallons_per_plant(c), 1.0)

    # ---- NAMED POSITIVE CONTROL 1 (spec section 8): the count[min] divisor -------------------
    def test_control_count_min_is_the_divisor_measured_on_a_2_6_reading(self):
        """A [2, 6] count DISTINGUISHES count[0] from count[1]: 1/2 = 0.5 vs 1/6 = 0.167.
        A [4, 4] fixture would pass under either end and is NOT a control (amendment 4)."""
        c = crop(obj(reading(count=[2, 6], at_gallons=[1, 1])))
        self.assertEqual(G.conservative_gallons_per_plant(c["container_notes"]["plants_per_pot"]["readings"][0]), 0.5)
        self.assertEqual(G.planner_gallons_per_plant(c), 0.5)
        # and the control is a real discriminator, asserted rather than assumed:
        self.assertNotEqual(1 / 2, 1 / 6)

    def test_a_4_4_count_would_not_have_been_a_control(self):
        """Stated as a test so the reason the fixture is [2,6] cannot be lost: on [4,4] the
        two candidate divisors AGREE, so a [4,4] fixture proves nothing about which end is used."""
        r = reading(count=[4, 4], at_gallons=[1, 1])
        self.assertEqual(r["at_gallons"][1] / r["count"][0], r["at_gallons"][1] / r["count"][1])

    # ---- NAMED POSITIVE CONTROL 2 (spec section 8): the two-reading maximum -------------------
    def test_control_two_reading_conservative_maximum_takes_the_larger(self):
        """Ruling 2, on a SYNTHETIC fixture: no authored crop exercises it (eggplant is the only
        two-reading crop and both its readings are count-1, so ruling 3 keeps min_pot_gallons).

        One count>1 reading (0.5 gal/plant) triggers the switch; one cautious count-1 reading
        (10 gal/plant) then RESTRAINS it. The maximum must win, or UMD's caution is ignored."""
        loose = reading(count=[2, 3], at_gallons=[1, 1])                     # 1 / 2  = 0.5
        cautious = reading(count=[1, 1], at_gallons=[8, 10], sources=["umd_ext"],
                           anchoring_urls={"umd_ext": {"url": "https://extension.umd.edu/x",
                                                       "verified": "2026-09-21"}})   # 10 / 1 = 10.0
        c = crop(obj(loose, cautious))
        self.assertEqual(G.conservative_gallons_per_plant(loose), 0.5)
        self.assertEqual(G.conservative_gallons_per_plant(cautious), 10.0)
        self.assertEqual(G.planner_gallons_per_plant(c), 10.0)
        # the fixture must actually discriminate max from min, or the control is vacuous:
        self.assertNotEqual(0.5, 10.0)

    def test_at_gallons_hi_is_the_numerator(self):
        """The band's roomier end (spec 4.2). [8,10] must give 10, not 8."""
        c = crop(obj(reading(count=[1, 2], at_gallons=[8, 10])))
        self.assertEqual(G.planner_gallons_per_plant(c), 10.0)

    def test_readings_of_treats_absent_null_and_empty_alike(self):
        """The consumer contract (7.2 step 1, 7.3): all three mean 'no readings'."""
        self.assertEqual(G.readings_of(crop()), [])
        self.assertEqual(G.readings_of(crop(None)), [])
        self.assertEqual(G.readings_of(crop({"readings": []})), [])


class NumericSanityAgreement(unittest.TestCase):
    """numeric_sanity_gate is deliberately dependency-free (five modules import it and it has no
    module-level imports at all), so it navigates to the readings with its own four-line reader
    instead of importing this gate's. That retype is the risk 'import a gate's table' warns about,
    so the agreement is MEASURED here rather than assumed."""

    SHAPES = [
        "__absent__", None, {"readings": []}, [4, 6], {"readings": "x"},
        {"readings": [READING]},
        {"readings": [READING, {"count": [1, 1], "at_gallons": [8, 10], "sources": ["umd_ext"],
                                "anchoring_urls": {}}]},
        {"readings": [{"count": None, "at_gallons": None, "sources": [], "anchoring_urls": {}}]},
    ]

    def test_the_two_readers_agree_on_every_shape(self):
        for shape in self.SHAPES:
            c = crop(shape)
            self.assertEqual(
                G.readings_of(c), NSG._plants_per_pot_readings(c.get("container_notes") or {}),
                f"readers disagree on {shape!r}")

    def test_the_bounds_actually_fire(self):
        """Not a vacuous agreement: numeric_sanity must REJECT an absurd count and an absurd pot."""
        self.assertNotEqual(NSG.numeric_sanity_violations(crop(obj(reading(count=[1, 99])))), [])
        self.assertNotEqual(NSG.numeric_sanity_violations(crop(obj(reading(at_gallons=[1, 400])))), [])

    def test_the_half_gallon_floor_is_accepted(self):
        """The 0.5 floor differs from min_pot_gallons' 1..100 ON PURPOSE (Illinois' half-gallon
        row). If a later reader 'fixes' it to 1, this test is what says no."""
        self.assertEqual(NSG.numeric_sanity_violations(crop(obj(reading(at_gallons=[0.5, 0.5])))), [])

    def test_a_quarter_gallon_is_below_the_floor(self):
        self.assertNotEqual(NSG.numeric_sanity_violations(crop(obj(reading(at_gallons=[0.25, 0.25])))), [])

    def test_min_pot_gallons_keeps_its_own_floor_of_one(self):
        """The two bounds are DIFFERENT; assert both, so neither drifts onto the other."""
        c = crop(None, extra_cn={"min_pot_gallons": 0.5})
        self.assertNotEqual(NSG.numeric_sanity_violations(c), [])


class RosterSweep(unittest.TestCase):
    """all_violations walks the roster and keeps presence OFF by default, for the same reason
    A60_PRESENCE_ARMED starts False: a caller replaying a historical state must stay green."""

    def test_presence_is_off_by_default(self):
        data = {"crops": [crop(), crop()]}
        self.assertEqual(G.all_violations(data), [])
        self.assertEqual(len(G.all_violations(data, presence=True)), 2)


if __name__ == "__main__":
    unittest.main()
