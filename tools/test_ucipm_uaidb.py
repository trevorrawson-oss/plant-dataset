#!/usr/bin/env python3
"""The positive control for the UC IPM hazard-grid parser. OFFLINE: parses a cached page.

This is deliberately not a network test. Its job is to pin the PARSE against a document whose
rendered values are independently known -- Trevor's screenshot of the chlorothalonil page on
2026-08-26 -- so that a future edit to the parser cannot silently reintroduce the column shift that
reported Acute L where the page says Acute H.
"""
import os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import ucipm_uaidb as U  # noqa: E402

FIXTURE = os.path.join(REPO, "tools", "fixtures", "ucipm_uaidb_115_chlorothalonil.html")


class PositiveControl(unittest.TestCase):
    def setUp(self):
        self.html = open(FIXTURE).read()

    def _parse(self):
        orig = U.fetch
        U.fetch = lambda key, cache=True: self.html
        try:
            return U.parse("115")
        finally:
            U.fetch = orig

    def test_the_five_hazard_columns_match_the_rendered_page(self):
        r = self._parse()
        self.assertEqual(r["water_quality"], "H")
        self.assertEqual(r["natural_enemies"], "L")
        self.assertEqual(r["honey_bees"], "bee:medium")
        self.assertEqual(r["acute"], "H")
        self.assertIn("Prop 65", r["chronic"])
        self.assertIn("US EPA", r["chronic"])

    def test_acute_is_not_the_shifted_value(self):
        """The exact defect: a markdown parse of this page reported Acute L. L is CAUTION, H is
        DANGER, and the difference decides how the caution is written."""
        self.assertNotEqual(self._parse()["acute"], "L")

    def test_footnote_text_is_not_mistaken_for_data(self):
        """Every <th> ends its sr-only footnote with 'Information to be added.'"""
        self.assertIn("Information to be added", self.html)
        for v in self._parse().values():
            self.assertNotIn("Information to be added", str(v))

    def test_the_bee_cell_has_no_text_at_all(self):
        """It is an empty span; the value lives in the CSS class, which is why a text scrape loses
        it and the next cell slides left."""
        self.assertIn("bee-precaution-rating-medium", self.html)
        self.assertIn("<span class='bee-precaution-rating-medium'></span>", self.html)

    def test_name_and_sections_parse(self):
        r = self._parse()
        self.assertEqual(r["name"], "chlorothalonil")
        self.assertIn("Fungicide", r["type"])
        self.assertIn("gloves", r["safety"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
