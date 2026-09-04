#!/usr/bin/env python3
"""Suite for promote_rosemary_certlog_correction. Built to the PLA-215 bar.

The guard families here are few because the change is one appended string, but each one guards a
way this specific promote could silently do the wrong thing:

  PREFIX      the original prose must survive byte-for-byte; an APPEND-ONLY field that gets edited
              destroys the only evidence of what a pass actually concluded
  SCOPE       exactly one leaf on one crop may move
  PRECONDITION the claim being corrected must EXIST, or the promote appends a correction to nothing
  IDEMPOTENCE re-running must refuse rather than double-append
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_rosemary_certlog_correction as P  # noqa: E402

BASE_SHA = "132980d52dd2f4c7850729401fdcfde8b5485ab0eb03f734e9acf949755d27b4"


def canon():
    with open(P.CANON, encoding="utf-8") as f:
        return json.load(f)


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = canon()

    def fresh(self):
        return copy.deepcopy(self.data)

    def assertRefuses(self, fragment, fn, *a):
        with self.assertRaises(SystemExit) as cm:
            fn(*a)
        self.assertIn(fragment, str(cm.exception),
                      f"guard fired with the wrong message: {cm.exception}")


class Preflight(Base):
    def test_base_sha_is_pinned(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(open(P.CANON, "rb").read()), BASE_SHA,
                         "canonical moved; re-measure rather than retune")

    def test_the_stale_claim_is_actually_present(self):
        """POSITIVE CONTROL. If the claim were absent the promote would be correcting nothing and
        every test below would pass vacuously."""
        v = P.by_slug(self.data)["rosemary"]["verification_status"][P.FIELD]
        self.assertIn(P.STALE_CLAIM, v)

    def test_correction_matches_the_conventions_format(self):
        """docs/verification_log_ref_convention.md fixes the shape."""
        self.assertTrue(P.CORRECTION.lstrip().startswith("[CORRECTION 2026-09-04:"))
        self.assertTrue(P.CORRECTION.rstrip().endswith("]"))
        self.assertIn("--", P.CORRECTION, "the convention's ' -- see <finding>' pointer is missing")

    def test_correction_does_not_assert_the_genera_it_retracts_toward(self):
        """The caveat bounds the correction. A proxy retrieval justifies retracting an over-claim
        and does NOT license a new one, so the text must not present the three genera as rosemary's
        established pathogens."""
        self.assertIn("NOT a first-party read", P.CORRECTION)
        self.assertIn("UNRESOLVED", P.CORRECTION)


class CleanRun(Base):
    def test_apply_then_verify(self):
        post = P.apply_to(self.data)
        self.assertTrue(P.verify_post(self.data, post))

    def test_original_survives_as_an_exact_prefix(self):
        pre = P.by_slug(self.data)["rosemary"]["verification_status"][P.FIELD]
        post = P.apply_to(self.data)
        got = P.by_slug(post)["rosemary"]["verification_status"][P.FIELD]
        self.assertTrue(got.startswith(pre))
        self.assertEqual(got[:len(pre)], pre, "original prose must be byte-for-byte intact")
        self.assertGreater(len(got), len(pre))

    def test_only_rosemary_moves(self):
        post = P.apply_to(self.data)
        pre_i, post_i = P.by_slug(self.data), P.by_slug(post)
        moved = [s for s in pre_i
                 if json.dumps(pre_i[s], sort_keys=True) != json.dumps(post_i[s], sort_keys=True)]
        self.assertEqual(moved, ["rosemary"])


    def test_serialize_is_compact(self):
        """Reachable now. Canonical is compact: no indent, no trailing newline, unicode unescaped."""
        blob = P.serialize({"a": 1, "b": "caf\u00e9"})
        self.assertEqual(blob, '{"a":1,"b":"caf\u00e9"}'.encode("utf-8"))
        self.assertNotIn(b"\\u", blob)
        self.assertFalse(blob.endswith(b"\n"))
        self.assertNotIn(b"\n", blob)


class Guards(Base):
    def test_edited_rather_than_appended_is_refused(self):
        """THE CORE GUARD. Rewriting a stale log into current tense is the thing this field's
        convention exists to forbid."""
        post = P.apply_to(self.data)
        vs = P.by_slug(post)["rosemary"]["verification_status"]
        vs[P.FIELD] = vs[P.FIELD].replace(P.STALE_CLAIM, "root/crown rot taxon unresolved")
        self.assertRefuses("not an exact PREFIX", P.verify_post, self.data, post)

    def test_a_different_appended_text_is_refused(self):
        post = P.apply_to(self.data)
        vs = P.by_slug(post)["rosemary"]["verification_status"]
        vs[P.FIELD] = vs[P.FIELD] + " and something else"
        self.assertRefuses("not exactly the declared correction", P.verify_post, self.data, post)

    def test_a_second_field_moving_is_refused(self):
        post = P.apply_to(self.data)
        P.by_slug(post)["rosemary"]["verification_status"]["status"] = "tampered"
        self.assertRefuses("expected only", P.verify_post, self.data, post)

    def test_another_crop_moving_is_refused(self):
        post = P.apply_to(self.data)
        P.by_slug(post)["basil"]["name"] = "Tampered"
        self.assertRefuses("untouched crop", P.verify_post, self.data, post)

    def test_top_level_change_is_refused(self):
        post = P.apply_to(self.data)
        post["source_catalog"]["uc_ipm"]["tier"] = "T2"
        self.assertRefuses("top-level key", P.verify_post, self.data, post)

    def test_missing_stale_claim_is_refused(self):
        """PRECONDITION. Appending a correction to a field that no longer carries the claim would
        leave a correction pointing at nothing, which is worse than no correction."""
        d = self.fresh()
        vs = P.by_slug(d)["rosemary"]["verification_status"]
        vs[P.FIELD] = vs[P.FIELD].replace(P.STALE_CLAIM, "something else entirely")
        self.assertRefuses("ABSENT from the pre-state", P.check_pre, d)

    def test_double_append_is_refused(self):
        """IDEMPOTENCE, by refusal rather than by silence."""
        d = P.apply_to(self.data)
        self.assertRefuses("already present", P.check_pre, d)

    def test_empty_field_is_refused(self):
        d = self.fresh()
        P.by_slug(d)["rosemary"]["verification_status"][P.FIELD] = "   "
        self.assertRefuses("not a non-empty string", P.check_pre, d)


if __name__ == "__main__":
    unittest.main(verbosity=2)
