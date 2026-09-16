#!/usr/bin/env python3
"""Unit tests for plant_dimensions_gate (A59) -- PLA-465 plant-dimensions field shape.
RED before GREEN: written before the gate module existed."""
import copy
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from plant_dimensions_gate import shape_violations, presence_violations, all_violations, FIELDS  # noqa: E402

FA = {"field": "plant_dimensions", "date": "2026-09-16", "sources": ["ucanr_ext"], "note": "x"}


def crop(height=None, spread=None, footprint=None, spacing=(60, 120), certified=True, fa=True, keys=True):
    c = {"slug": "t", "spacing_inches": list(spacing) if spacing else None,
         "verification_status": {"status": "verified_gs_arc" if certified else None,
                                 "field_additions": [FA] if fa else []}}
    if keys:
        c["mature_height_ft"] = height
        c["mature_spread_ft"] = spread
        c["footprint_inches"] = footprint
    return c


class Shape(unittest.TestCase):
    def test_fields_are_the_three(self):
        self.assertEqual(FIELDS, ("mature_height_ft", "mature_spread_ft", "footprint_inches"))

    def test_all_null_is_clean(self):
        self.assertEqual(shape_violations(crop()), [])

    def test_a_well_formed_pair_is_clean(self):
        self.assertEqual(shape_violations(crop(height=[10, 14], spread=[8, 12], footprint=4)), [])

    def test_refuses_a_scalar_height(self):
        v = shape_violations(crop(height=12))
        self.assertTrue(any("mature_height_ft" in x and "two numbers" in x for x in v), v)

    def test_refuses_a_three_element_spread(self):
        v = shape_violations(crop(spread=[1, 2, 3]))
        self.assertTrue(any("mature_spread_ft" in x and "two numbers" in x for x in v), v)

    def test_refuses_lo_above_hi(self):
        v = shape_violations(crop(height=[14, 10]))
        self.assertTrue(any("mature_height_ft" in x and "lo <= hi" in x for x in v), v)

    def test_refuses_a_zero_or_negative_bound(self):
        v = shape_violations(crop(height=[0, 10]))
        self.assertTrue(any("mature_height_ft" in x and "positive" in x for x in v), v)

    def test_refuses_a_string_number(self):
        v = shape_violations(crop(spread=["8", 12]))
        self.assertTrue(any("mature_spread_ft" in x and "two numbers" in x for x in v), v)

    def test_refuses_a_bool_footprint(self):
        v = shape_violations(crop(footprint=True))
        self.assertTrue(any("footprint_inches" in x and "positive number" in x for x in v), v)

    def test_refuses_a_non_positive_footprint(self):
        v = shape_violations(crop(footprint=0))
        self.assertTrue(any("footprint_inches" in x and "positive number" in x for x in v), v)

    def test_refuses_a_footprint_at_or_above_min_spacing(self):
        v = shape_violations(crop(footprint=60, spacing=(60, 120)))
        self.assertTrue(any("footprint_inches" in x and "below spacing_inches[0]" in x for x in v), v)
        self.assertEqual(shape_violations(crop(footprint=59.5, spacing=(60, 120))), [])

    def test_footprint_with_no_spacing_is_shape_only(self):
        self.assertEqual(shape_violations(crop(footprint=6, spacing=None)), [])

    def test_refuses_an_authored_value_with_no_provenance_record(self):
        v = shape_violations(crop(height=[10, 14], fa=False))
        self.assertTrue(any("field_additions" in x and "plant_dimensions" in x for x in v), v)

    def test_provenance_is_not_required_on_a_null(self):
        self.assertEqual(shape_violations(crop(fa=False)), [])

    def test_provenance_is_not_required_off_certified(self):
        self.assertEqual(shape_violations(crop(height=[10, 14], fa=False, certified=False)), [])


class Presence(unittest.TestCase):
    def test_certified_crop_must_carry_all_three_keys(self):
        v = presence_violations(crop(keys=False))
        self.assertEqual(len(v), 3, v)
        for f in FIELDS:
            self.assertTrue(any(f in x and "missing" in x for x in v), (f, v))

    def test_null_is_a_present_value(self):
        self.assertEqual(presence_violations(crop()), [])

    def test_a_shell_is_exempt(self):
        self.assertEqual(presence_violations(crop(keys=False, certified=False)), [])

    def test_one_missing_key_is_one_violation(self):
        c = crop(); del c["footprint_inches"]
        v = presence_violations(c)
        self.assertEqual(len(v), 1, v)
        self.assertIn("footprint_inches", v[0])


class AllViolations(unittest.TestCase):
    def test_presence_is_off_by_default(self):
        self.assertEqual(all_violations({"crops": [crop(keys=False)]}), [])
        self.assertEqual(len(all_violations({"crops": [crop(keys=False)]}, presence=True)), 3)

    def test_shape_and_presence_add(self):
        c = crop(height=[14, 10]); del c["footprint_inches"]
        v = all_violations({"crops": [c]}, presence=True)
        self.assertEqual(len(v), 2, v)


if __name__ == "__main__":
    unittest.main()
