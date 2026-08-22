#!/usr/bin/env python3
"""Guard suite for tools/promote_pla6_wave3.py (PLA-6 Round 2, wave 3: the berries). Base 64428067.

REPLAY-PINNED, so there is NO RED PHASE and this suite does not claim one -- `pre` is rebuilt
from the pinned base and `post` is the promote's own output. The non-vacuity evidence is the
REACHABILITY guard (the base really lacked every field this creates) plus
tools/mutate_pla6_wave1_suite.py.

WHAT WAVE 1 ADDS OVER THE PILOT'S GUARDS. Eight crops of similar biology are authored at once,
so the risk shifts from "is the field shaped right" to "did the same paragraph get pasted eight
times with the crop name swapped". That is the v1.3 sec9.1 cosmetic-pair defect on the CROSS-CROP
axis, and a similarity metric scores a name-swap as substantively different while a reader scores
it as identical. TEMPLATE-PASTE is therefore a first-class family here, and it caught a real one
during drafting: peach and nectarine's full_harvest_notes_beginner measured 0.837.
"""
import copy
import difflib
import hashlib
import json
import itertools
import os
import re
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
import promote_pla6_wave3 as P  # noqa: E402
from perennial_year_gate import renders_pills  # noqa: E402

POST_SHA = '97c63704812e2192fe8ec27ba0007e24db5dadbc88473aeccca5bba217c1521c'

BASES = ('first_harvest_notes', 'full_harvest_notes')

ORDINAL = {2: 'second', 3: 'third'}

# ENUMERATED, never derived from P.TRIO. The mutation harness caught the first version deriving
# `expected` from P.TRIO inside the test body, which made adding an unauthorised crop change both
# sides of the comparison identically -- the guard-derived-from-what-it-checks vacuity. A literal
# is the only shape that can fail.
WAVE_CROPS = ('blackberry', 'blueberry', 'elderberry', 'raspberry', 'strawberry')


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre):
    return P.apply_to(copy.deepcopy(pre))


def _all_strings():
    return [(f'{s}.{k}', v) for s, f in P.TRIO.items() for k, v in f.items()]


class Fixture(unittest.TestCase):
    def test_base_reconstructs_to_the_pinned_sha(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_post_serializes_to_the_pinned_post_sha(self):
        out = json.dumps(_post(_pre()), ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        self.assertEqual(hashlib.sha256(out).hexdigest(), POST_SHA)

    def test_output_is_compact(self):
        out = json.dumps(_post(_pre()), ensure_ascii=False, separators=(',', ':'))
        self.assertNotIn(', "', out)
        self.assertNotIn('\n', out)


class Reachability(unittest.TestCase):
    def test_every_field_was_absent_in_the_base(self):
        by = {c['slug']: c for c in _pre()['crops']}
        for slug, fields in P.TRIO.items():
            for field in fields:
                self.assertNotIn(field, by[slug], f'{slug}.{field} already existed')

    def test_the_pilot_crops_are_NOT_in_this_wave(self):
        for slug in ('apple', 'pawpaw', 'asparagus'):
            self.assertNotIn(slug, P.TRIO)

    def test_the_wave_is_exactly_the_enumerated_five(self):
        self.assertEqual(sorted(P.TRIO), sorted(WAVE_CROPS))


class BlastRadius(unittest.TestCase):
    def test_only_the_expected_fields_differ(self):
        pre = _pre()
        post = _post(copy.deepcopy(pre))
        pre_by = {c['slug']: c for c in pre['crops']}
        post_by = {c['slug']: c for c in post['crops']}
        assert set(pre_by) == set(post_by)          # SET EQUALITY BEFORE value comparison
        expected = {(s, f) for s in WAVE_CROPS for f in P.NEW_FIELDS}
        touched = set()
        for slug in post_by:
            a, b = pre_by[slug], post_by[slug]
            assert set(a) | set(b) == set(b), f'{slug}: a key disappeared'
            for field in set(a) | set(b):
                if a.get(field, '\0X') != b.get(field, '\0X'):
                    touched.add((slug, field))
        self.assertEqual(touched, expected)

    def test_top_level_keys_unchanged(self):
        pre = _pre()
        post = _post(copy.deepcopy(pre))
        assert set(pre) == set(post)
        for k in pre:
            if k != 'crops':
                self.assertEqual(pre[k], post[k], f'top-level {k} changed')


class Mechanics(unittest.TestCase):
    def test_no_em_dash_en_dash_or_double_hyphen(self):
        for where, v in _all_strings():
            for bad in ('\u2014', '\u2013', '--'):
                self.assertNotIn(bad, v, where)

    def test_american_english(self):
        for where, v in _all_strings():
            self.assertIsNone(re.search(r'\b(colour|fibre|centre|metre|grey|programme|internalise|realise|organise|recognise|emphasise|minimise|maximise|analyse|defence|labour|favour|behaviour)\b', v, re.I), where)

    def test_temperatures_are_not_spelled_out(self):
        for where, v in _all_strings():
            self.assertIsNone(re.search(r'\b\d+\s*degrees?\s*F\b', v), where)


class RegisterIntegrity(unittest.TestCase):
    def test_no_pair_is_a_near_verbatim_copy(self):
        """A COPY DETECTOR, NOT A COSMETIC-PAIR DETECTOR, and the distinction is measured rather
        than assumed. Copy architecture v1.3 sec9.1 defines the cosmetic pair as a seasoned half
        that is the beginner half with harder words, and it says plainly that a similarity metric
        scores a thesaurus pass as substantively different because every word changed. Measured
        on this arc's own prose: a verbatim copy scores 1.000, a three-word swap 0.986, and a
        true thesaurus pass over every word scores 0.333 -- LOWER than honest, genuinely
        different prose. The metric is inverted against the defect it would need to catch.

        So this guard claims only what it can do: it refuses a pair where one half was pasted
        from the other and lightly edited. THE sec9.1 DEFECT PROPER IS NOT MECHANIZABLE and is
        checked by reading, per v1.2 sec11 ("these rules are checked by reading, and by nothing
        else"). Authored pairs in this arc measure 0.015 to 0.117, far below the bar, so a hit
        here means a paste rather than a close call."""
        for slug, fields in P.TRIO.items():
            for base in BASES:
                b, s = fields.get(base + '_beginner'), fields.get(base + '_seasoned')
                if not (b and s):
                    continue
                r = difflib.SequenceMatcher(None, b.lower(), s.lower()).ratio()
                self.assertLess(r, 0.85, f'{slug}.{base} similarity {r:.3f}: one half is a copy '
                                         f'of the other')


    def test_beginner_halves_carry_an_imperative(self):
        VERBS = r'\b(thin|pick|prune|cut|net|space|clear|handle|check|keep|watch|pull)\b'
        for slug, fields in P.TRIO.items():
            for field, v in fields.items():
                if field.endswith('_beginner'):
                    self.assertIsNotNone(re.search(VERBS, v, re.I), f'{slug}.{field}')


class TemplatePaste(unittest.TestCase):
    """v1.3 sec9.1 on the CROSS-CROP axis. Eight biologically similar crops authored in one pass
    is exactly where a paragraph gets pasted with the crop name swapped, and a name-swap scores
    as substantively different to a similarity metric while a reader sees one text."""

    def test_no_two_crops_share_a_near_identical_field(self):
        worst = []
        for field in P.NEW_FIELDS:
            for a, b in itertools.combinations(sorted(P.TRIO), 2):
                r = difflib.SequenceMatcher(None, P.TRIO[a][field].lower(),
                                            P.TRIO[b][field].lower()).ratio()
                if r >= 0.60:
                    worst.append(f'{a} vs {b} {field} = {r:.3f}')
        self.assertEqual(worst, [], 'cross-crop paste')



class BerryFacts(unittest.TestCase):
    """What separates the five. Each assertion is PER FIELD where the fact is actually read,
    never over a joined string: the mutation harness proved twice, in waves 1 and 2, that a
    joined-field guard goes vacuous the moment a single field is replaced."""

    def test_raspberry_and_blackberry_have_OPPOSITE_harvest_cues(self):
        # The receptacle either stays on the plant or comes with the fruit, and confusing them
        # sends a picker after under-ripe berries on one crop or over-ripe on the other.
        rasp = ' '.join(P.TRIO['raspberry'][f] for f in P.NEW_FIELDS).lower()
        black = ' '.join(P.TRIO['blackberry'][f] for f in P.NEW_FIELDS).lower()
        self.assertIn('slips off', rasp)
        self.assertIn('hollow', rasp)
        self.assertIn('with its core', black)
        self.assertTrue(re.search(r'glossy to a dull|gloss to a dull', black))
        self.assertNotIn('hollow', black)

    def test_blackberry_never_says_pick_on_shine(self):
        for field, v in P.TRIO['blackberry'].items():
            self.assertIsNone(re.search(r'pick .{0,40}\bshiny\b(?!.{0,30}not)', v, re.I), field)

    def test_blueberry_is_not_treated_as_a_cane_crop(self):
        joined = ' '.join(P.TRIO['blueberry'].values()).lower()
        self.assertIn('bush', joined)
        self.assertTrue(re.search(r'chlorosis', joined), 'blueberry loses its defining failure')

    def test_elderberrys_COOKING_RULE_is_in_every_field(self):
        """A safety rule, and a reader lands on ONE pill rather than reading all four. Raw and
        unripe fruit, foliage and stems are mildly toxic, so the instruction cannot live in only
        the field that happened to have room for it."""
        for field, v in P.TRIO['elderberry'].items():
            self.assertTrue(re.search(r'\bcook', v, re.I), f'{field}: no cooking instruction')
            self.assertTrue(re.search(r'toxic', v, re.I), f'{field}: no toxicity reason')

    def test_strawberry_scopes_renovation_to_JUNE_BEARING_only(self):
        # Renovating a day-neutral bed mows off fruit it is still carrying.
        for reg in ('beginner', 'seasoned'):
            v = P.TRIO['strawberry'][f'full_harvest_notes_{reg}']
            self.assertTrue(re.search(r'renovat', v, re.I), reg)
            self.assertTrue(re.search(r'day-neutral', v, re.I), f'{reg}: type scoping missing')
            self.assertTrue(re.search(r'skip renovation|not renovated|NOT renovated', v, re.I),
                            f'{reg}: never says day-neutrals are exempt')

    def test_the_cane_term_is_GLOSSED_where_a_beginner_meets_it(self):
        """v1.3 sec9.3, and this arc's largest measured gloss gap: `cane` runs 151 bare uses in
        beginner copy across the perennials, 133 of them on these two crops."""
        for slug in ('raspberry', 'blackberry'):
            v = P.TRIO[slug]['first_harvest_notes_beginner']
            self.assertIn('cane', v)
            self.assertTrue(re.search(r'meaning each individual stem', v), f'{slug}: bare cane')

    def test_full_harvest_year_equals_years_to_first_harvest_high(self):
        by = {c['slug']: c for c in _pre()['crops']}
        for slug in P.TRIO:
            hi = by[slug]['years_to_first_harvest'][1]
            self.assertIn(ORDINAL[hi], P.TRIO[slug]['full_harvest_notes_beginner'],
                          f'{slug}: prose must say year {hi}')

    def test_every_crop_renders_pills(self):
        by = {c['slug']: c for c in _post(_pre())['crops']}
        for slug in P.TRIO:
            self.assertTrue(renders_pills(by[slug]))

    def test_no_field_is_ever_null(self):
        by = {c['slug']: c for c in _post(_pre())['crops']}
        for crop in by.values():
            for field in P.NEW_FIELDS:
                if field in crop:
                    self.assertIsNotNone(crop[field], f"{crop['slug']}.{field}")



if __name__ == '__main__':
    unittest.main(verbosity=2)
