#!/usr/bin/env python3
"""Guard suite for tools/promote_pla6_wave2.py (PLA-6 Round 2, wave 2: citrus). Base 647fe432.

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
import promote_pla6_wave2 as P  # noqa: E402
from perennial_year_gate import renders_pills  # noqa: E402

POST_SHA = '64428067a44b369b550b6d11d8287e7578afbadf022b14e2fe7c8238e0ebc393'

BASES = ('year_one_notes', 'first_harvest_notes', 'full_harvest_notes')

ORDINAL = {3: 'third', 4: 'fourth'}

# ENUMERATED, never derived from P.TRIO. The mutation harness caught the first version deriving
# `expected` from P.TRIO inside the test body, which made adding an unauthorised crop change both
# sides of the comparison identically -- the guard-derived-from-what-it-checks vacuity. A literal
# is the only shape that can fail.
WAVE_CROPS = ('grapefruit', 'lemon', 'lime', 'mandarin-clementine', 'orange-navel')


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
        VERBS = (r'\b(thin|pick|prune|cut|net|space|clear|handle|check|keep|watch|pull|hold|'
                 r'water|feed|plant|set|strip|scout|protect|allow|leave|taste|use)\b')
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



class CitrusFacts(unittest.TestCase):
    """The five diverge in ways a paste would erase, and each divergence is the thing that
    decides whether the grower gets fruit or ruins it. Pinned by name."""

    def test_lemon_is_picked_on_taste_not_color(self):
        joined = ' '.join(P.TRIO['lemon'].values()).lower()
        self.assertTrue(re.search(r'not by color|rather than (?:by )?rind color|not.*rind color', joined))

    def test_lime_is_picked_GREEN_in_BOTH_full_harvest_registers(self):
        """PER-FIELD, not joined. The mutation harness caught the joined version: replacing one
        whole field with pick-it-yellow advice fired NOTHING, because the phrase survived in the
        other five. A joined-field guard goes vacuous under a single-field mutation, which is
        the same defect wave 1's spur and pear guards had.

        This is the wave's highest-consequence fact. Lime's own record calls picking yellow the
        most common lime-harvest mistake, and the rule is the exact inverse of lemon's, so the
        failure mode is a crop quietly inheriting its neighbour's rule."""
        for reg in ('beginner', 'seasoned'):
            v = P.TRIO['lime'][f'full_harvest_notes_{reg}']
            self.assertTrue(re.search(r'\bgreen\b', v, re.I), f'lime.{reg} loses pick-green')
            # The negative must match an INSTRUCTION to pick yellow, never the word. The first
            # version flagged the correct prose "once it turns yellow it is overripe" -- a
            # warning, not an instruction. Same trap as wave 1's cherry-thinning guard: a token
            # scan is not the check.
            self.assertIsNone(re.search(r'(?:pick|harvest)\b[^.]{0,70}\byellow\b', v, re.I),
                              f'lime.{reg} instructs the reader to pick yellow')

    def test_lemon_does_NOT_inherit_the_lime_rule(self):
        for reg in ('beginner', 'seasoned'):
            self.assertIsNone(re.search(r'pick lemons green|harvest green',
                                        P.TRIO['lemon'][f'full_harvest_notes_{reg}'], re.I))

    def test_lime_is_never_told_to_store_like_a_lemon(self):
        lime = ' '.join(P.TRIO['lime'].values()).lower()
        self.assertIn('50', lime)                       # held near 50F, not properly cold
        self.assertTrue(re.search(r'chilling-sensitive|damaged by cold|short-lived', lime))
        self.assertIsNone(re.search(r'the tree is (?:your|the) stor', lime))

    def test_lemon_and_navel_and_grapefruit_DO_hold_on_the_tree(self):
        for slug in ('lemon', 'orange-navel', 'grapefruit'):
            joined = ' '.join(P.TRIO[slug].values()).lower()
            self.assertTrue(re.search(r'hold[s]? (?:on|well on) the (?:tree|branch)|stor(?:es|ing) themselves|'
                                      r'the tree is the store|the tree functions as the store|'
                                      r'use the tree as your storage', joined), slug)

    def test_mandarin_does_NOT_hold_in_BOTH_full_harvest_registers(self):
        """PER-FIELD for the same reason as lime. Mandarin puffs and dries on the branch, so
        inheriting navel's leave-it-on-the-tree advice loses the crop to waiting."""
        for reg in ('beginner', 'seasoned'):
            v = P.TRIO['mandarin-clementine'][f'full_harvest_notes_{reg}']
            self.assertTrue(re.search(r'do not hold|does not hold|puff', v, re.I),
                            f'mandarin.{reg} loses the does-not-hold rule')
            self.assertTrue(re.search(r'pick promptly|harvest promptly', v, re.I),
                            f'mandarin.{reg} loses the pick-promptly instruction')
            self.assertIsNone(re.search(r'leave ripe fruit on the tree|stores itself outdoors', v, re.I),
                              f'mandarin.{reg} inherited navel holding advice')

    def test_hang_lengths_match_each_crops_own_record(self):
        HANG = {'orange-navel': 'ten to twelve', 'grapefruit': 'nine to thirteen'}
        for slug, phrase in HANG.items():
            self.assertIn(phrase, ' '.join(P.TRIO[slug].values()), slug)

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

    def test_graft_union_depth_agrees_across_every_crop_and_register(self):
        # v1.3 sec9.2 across FIVE crops: the same physical instruction must not drift.
        for slug in P.TRIO:
            for reg in ('beginner', 'seasoned'):
                v = P.TRIO[slug][f'year_one_notes_{reg}']
                self.assertIn('two to three inches', v, f'{slug}.{reg}')

    def test_the_graft_union_is_GLOSSED_in_every_beginner_half(self):
        # v1.3 sec9.3: a beginner meets "graft union" on a nursery tag, so it is named and
        # explained in the field where it appears, not three fields away.
        for slug in P.TRIO:
            v = P.TRIO[slug]['year_one_notes_beginner']
            self.assertIn('graft union', v, slug)
            self.assertTrue(re.search(r'knobby joint|the joint|where .* joined', v), f'{slug} unglossed')



if __name__ == '__main__':
    unittest.main(verbosity=2)
