#!/usr/bin/env python3
"""T4 reads fraction figures (PLA-659; housekeeping kickoff 60, B4, 2026-10-03).

MEASURED ON THE HASHED BYTES. The two trigger pages carry U+00BD VULGAR FRACTION ONE HALF ("3½", "1½"), not
U+2044: norm_text's NFKC turns "3½" into "31⁄2" and "1½" into "11⁄2", so the boundary between the whole number and
the fraction is lost after normalization. Before this fix T4 read "2 to 31⁄2 feet tall and 11⁄2 feet wide" as
2 ft tall and 2 ft WIDE (the denominator taken as the figure), a FALSE read that would state a 2-ft spread.
No landed EVIDENCE row depended on it (measured: no promote 3 quote carries a fraction).

THE READ. A single-digit numerator, U+2044, and a denominator of 2, 3, 4 or 8 is a fraction. Glued to a whole
number ("31⁄2", the NFKC form of "3½") or spaced from it ("3 1⁄2") it is whole + fraction; alone ("1⁄2") it is the
fraction. A glued figure is never read as a 31/2: a vulgar fraction's numerator is one digit.

FIXTURES are sentences located in the HASHED bytes at test time (Clemson HGIC echinacea dd5acdb3..., UW-Madison
cilantro 341f18e3...), never retyped. No hashed page carries the spaced form (both pages are glued, measured), so
the spaced case is synthetic and says so. POSITIVE CONTROL on a plain decimal: UMaine kale (42285ee9...), "2.5-3
feet tall".
Run: python3 -m pytest tools/test_t4_fractions.py -q
SHIPS MUTATION-TESTED via mutate_cited_promote_common.py.
"""
import glob, hashlib, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cited_promote_common as C  # noqa: E402

EVIDENCE = os.path.join(HERE, ".evidence_cache")
CLEMSON = "dd5acdb3add04ba8d84e4a5b8f4d6e17b3fa7676e0176c8dfb9b687aa62d1837"
UW = "341f18e3fac1"
UMAINE = "42285ee921b8"
H, S = "mature_height_ft", "mature_spread_ft"


def page(sha_prefix):
    files = glob.glob(os.path.join(EVIDENCE, sha_prefix + "*"))
    assert len(files) == 1, f"EVIDENCE CACHE: {len(files)} files for {sha_prefix} (the bytes must be local)"
    raw = open(files[0], "rb").read()
    assert hashlib.sha256(raw).hexdigest().startswith(sha_prefix), "the cached bytes do not hash to their name"
    return C.norm_text(raw.decode("utf-8", "replace"))


def sentence(sha_prefix, fragment):
    text = page(sha_prefix)
    assert text.count(fragment) >= 1, f"{fragment!r} is not in the hashed page {sha_prefix}"
    return fragment


class HashedFractions(unittest.TestCase):
    def test_clemson_height_2_to_3_and_a_half(self):
        q = sentence(CLEMSON, "grows up to 2 to 31⁄2 feet tall and 11⁄2 feet wide")
        self.assertEqual(C.ft_endpoints_stated(H, [2, 3.5], q), {2, 3.5})

    def test_clemson_spread_1_and_a_half(self):
        q = sentence(CLEMSON, "grows up to 2 to 31⁄2 feet tall and 11⁄2 feet wide")
        self.assertEqual(C.ft_endpoints_stated(S, [1.5, 1.5], q), {1.5})

    def test_the_false_read_is_gone(self):
        q = sentence(CLEMSON, "grows up to 2 to 31⁄2 feet tall and 11⁄2 feet wide")
        self.assertEqual(C.ft_endpoints_stated(S, [2, 2], q), set(), "the denominator read as a 2-ft spread")
        self.assertEqual(C.ft_endpoints_stated(H, [31, 31], q), set(), "a glued figure read as 31 ft")

    def test_clemson_yellow_coneflower_2_and_a_half_to_3(self):
        q = sentence(CLEMSON, "reaches 21⁄2 to 3 feet tall")
        self.assertEqual(C.ft_endpoints_stated(H, [2.5, 3], q), {2.5, 3})

    def test_clemson_inches_wide(self):
        q = sentence(CLEMSON, "a rose-pink flower measuring 41⁄2 inches wide")
        self.assertEqual(C._ft_groups(q), [("W", [4.5 / 12])])

    def test_uw_cilantro_1_to_1_and_a_half(self):
        q = sentence(UW, "the foliage grows 1 to 11⁄2 feet high")
        self.assertEqual(C.ft_endpoints_stated(H, [1, 1.5], q), {1, 1.5})
        self.assertEqual(C.ft_endpoints_stated(H, [2, 2], q), set())

    def test_a_bare_fraction_is_the_fraction(self):
        q = sentence(UW, "plant seed 1⁄4 to 1⁄2 inch deep")
        self.assertEqual(C._ft_groups(q), [("", [0.25 / 12, 0.5 / 12])])


class SpacedForm(unittest.TestCase):
    # SYNTHETIC: no hashed page carries "3 1⁄2" spaced (both trigger pages are glued, measured 2026-10-03).
    def test_spaced_whole_and_fraction(self):
        self.assertEqual(C.ft_endpoints_stated(H, [3.5, 3.5], "it grows 3 1⁄2 feet tall."), {3.5})
        self.assertEqual(C.ft_endpoints_stated(H, [12.5, 12.5], "it grows 12 1⁄2 feet tall."), {12.5})


class PlainDecimal(unittest.TestCase):
    def test_umaine_kale_2_point_5_to_3(self):
        q = sentence(UMAINE, "kale is a large plant, often growing to 2.5-3 feet tall")
        self.assertEqual(C.ft_endpoints_stated(H, [2.5, 3], q), {2.5, 3})


if __name__ == "__main__":
    unittest.main()
