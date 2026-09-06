#!/usr/bin/env python3
"""Tests for container_path_gate (PLA-7 spec section 2 rules 1-4, section 7).
Run: python3 -m pytest tools/test_container_path_gate.py -q"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from container_path_gate import shape_violations, presence_violations, all_violations, VALUES


def crop(path, ok=True, archetype="warm_season_fruiting", depth=None, rootstocks=None, varieties=None,
         axis=None, certified=True, key=True):
    cn = {"container_ok": ok, "min_pot_gallons": 5, "depth_inches_min": depth}
    if key:
        cn["container_path"] = path
    c = {"slug": "x", "archetype": archetype, "container_notes": cn,
         "verification_status": {"status": "verified_gs_arc" if certified else None}}
    if rootstocks is not None:
        c["rootstock_options"] = rootstocks
    if varieties is not None:
        c["varieties"] = {"recommended": varieties}
    if axis is not None:
        c["rootstock_selection_axis"] = axis
    return c


class Rule1(unittest.TestCase):
    def test_direct_on_ok_true_is_clean(self):
        self.assertEqual(shape_violations(crop("direct")), [])
    def test_null_on_ok_false_is_clean(self):
        self.assertEqual(shape_violations(crop(None, ok=False)), [])
    def test_null_on_ok_null_is_clean(self):
        self.assertEqual(shape_violations(crop(None, ok=None)), [])
    def test_refuses_null_path_on_ok_true(self):
        self.assertTrue(any("rule 1" in v for v in shape_violations(crop(None))))
    def test_refuses_a_path_on_ok_false(self):
        self.assertTrue(any("rule 1" in v for v in shape_violations(crop("direct", ok=False))))
    def test_refuses_an_unknown_value(self):
        self.assertTrue(any("not in" in v for v in shape_violations(crop("dwarf_rootstock"))))
    def test_absent_key_is_not_a_shape_violation(self):
        self.assertEqual(shape_violations(crop(None, key=False)), [])


class Rule2(unittest.TestCase):
    def test_rootstock_with_a_suitable_entry_is_clean(self):
        self.assertEqual(shape_violations(crop("rootstock", rootstocks=[{"name": "M9", "container_suitable": True}])), [])
    def test_refuses_rootstock_with_no_suitable_entry(self):
        v = shape_violations(crop("rootstock", rootstocks=[{"name": "seedling", "container_suitable": False}]))
        self.assertTrue(any("rule 2" in x for x in v))
    def test_refuses_rootstock_with_no_rootstock_array(self):
        self.assertTrue(any("rule 2" in x for x in shape_violations(crop("rootstock"))))
    def test_axis_permits_size_control_and_combined(self):
        for ax in ("size_control", "combined"):
            self.assertEqual(shape_violations(crop("rootstock", rootstocks=[{"container_suitable": True}], axis=ax)), [])
    def test_refuses_rootstock_when_the_axis_forbids_it(self):
        v = shape_violations(crop("rootstock", rootstocks=[{"container_suitable": True}], axis="soil_and_pest"))
        self.assertTrue(any("PLA-463" in x for x in v))


class Rule3(unittest.TestCase):
    def test_cultivar_with_a_flagged_variety_is_clean(self):
        self.assertEqual(shape_violations(crop("cultivar", varieties=[{"name": "Astia", "container_suitable": True}])), [])
    def test_refuses_cultivar_with_no_flagged_variety(self):
        v = shape_violations(crop("cultivar", varieties=[{"name": "Costata", "container_suitable": False}]))
        self.assertTrue(any("rule 3" in x for x in v))
    def test_refuses_cultivar_with_string_varieties(self):
        self.assertTrue(any("rule 3" in x for x in shape_violations(crop("cultivar", varieties=["Astia"]))))


class Rule4(unittest.TestCase):
    def test_tray_on_microgreen_with_depth_is_clean(self):
        self.assertEqual(shape_violations(crop("tray", archetype="microgreen", depth=1)), [])
    def test_refuses_tray_without_depth(self):
        self.assertTrue(any("rule 4" in x for x in shape_violations(crop("tray", archetype="microgreen"))))
    def test_refuses_tray_off_the_microgreen_archetype(self):
        self.assertTrue(any("rule 4" in x for x in shape_violations(crop("tray", depth=1))))
    def test_refuses_direct_on_a_microgreen(self):
        self.assertTrue(any("rule 4" in x for x in shape_violations(crop("direct", archetype="microgreen", depth=1))))


class VarietyFlag(unittest.TestCase):
    def test_min_gallons_on_a_flagged_variety_is_clean(self):
        self.assertEqual(shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": True, "container_min_gallons": 15}])), [])
    def test_refuses_min_gallons_on_an_unflagged_variety(self):
        v = shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": False, "container_min_gallons": 15}]))
        self.assertTrue(any("container_min_gallons" in x for x in v))
    def test_refuses_min_gallons_out_of_bounds(self):
        v = shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": True, "container_min_gallons": 0}]))
        self.assertTrue(any("[1, 100]" in x for x in v))
    def test_refuses_a_non_boolean_flag(self):
        v = shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": "yes"}]))
        self.assertTrue(any("container_suitable" in x for x in v))
    def test_null_flag_is_clean(self):
        self.assertEqual(shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": None}])), [])


class Presence(unittest.TestCase):
    def test_certified_crop_missing_the_key_is_a_presence_violation(self):
        self.assertEqual(len(presence_violations(crop(None, key=False))), 1)
    def test_certified_crop_with_null_key_is_clean(self):
        self.assertEqual(presence_violations(crop(None, ok=False)), [])
    def test_uncertified_shell_is_exempt(self):
        self.assertEqual(presence_violations(crop(None, key=False, certified=False)), [])
    def test_all_violations_presence_off_by_default(self):
        data = {"crops": [crop(None, key=False)]}
        self.assertEqual(all_violations(data), [])
        self.assertEqual(len(all_violations(data, presence=True)), 1)


class Values(unittest.TestCase):
    def test_the_enum_is_the_spec_enum(self):
        self.assertEqual(VALUES, ("direct", "rootstock", "cultivar", "tray"))


if __name__ == "__main__":
    unittest.main()
