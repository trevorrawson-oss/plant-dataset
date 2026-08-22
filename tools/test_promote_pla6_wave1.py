#!/usr/bin/env python3
"""Guard suite for tools/promote_pla6_wave1.py (PLA-6 Round 2, wave 1). Base 0cc37afe.

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
import promote_pla6_wave1 as P  # noqa: E402
from perennial_year_gate import renders_pills  # noqa: E402

POST_SHA = '647fe432076030a3bef240d953a31b04c8a4b31140b445d00b78f1b9a18f108f'

BASES = ('first_harvest_notes', 'full_harvest_notes')

# Thinning distances, named explicitly per crop so a future edit to either register reddens.
# Each is the figure the crop's OWN tips_by_stage.fruit_set already states.
THINNING = {'peach': '6 to 8', 'nectarine': '6 to 8', 'apricot': '4 to 6', 'plum': '4 to 6',
            'pear-asian': '6 inches'}
# Crops that must NOT tell the reader to thin: cherries size without it, and saying otherwise
# would send a grower stripping fruit for no reason.
NO_THINNING = ('cherry-sweet', 'cherry-sour')
ORDINAL = {4: 'fourth', 5: 'fifth', 6: 'sixth'}

# ENUMERATED, never derived from P.TRIO. The mutation harness caught the first version deriving
# `expected` from P.TRIO inside the test body, which made adding an unauthorised crop change both
# sides of the comparison identically -- the guard-derived-from-what-it-checks vacuity. A literal
# is the only shape that can fail.
WAVE_CROPS = ('apricot', 'cherry-sour', 'cherry-sweet', 'nectarine',
              'peach', 'pear-asian', 'pear-european', 'plum')


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

    def test_the_wave_is_exactly_the_enumerated_eight(self):
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

    def test_peach_and_nectarine_stay_apart(self):
        # The one the drafting check actually caught, at 0.837. Pinned by name so it cannot
        # quietly re-converge: they are the same species group and the pull is real.
        r = difflib.SequenceMatcher(None,
                                    P.TRIO['peach']['full_harvest_notes_beginner'].lower(),
                                    P.TRIO['nectarine']['full_harvest_notes_beginner'].lower()
                                    ).ratio()
        self.assertLess(r, 0.30, f'peach/nectarine re-converged at {r:.3f}')


class QuantityAgreement(unittest.TestCase):
    """v1.3 sec9.2: a figure stated in both registers must agree, and must agree with the crop's
    own record rather than with a remembered number."""

    def test_thinning_distance_matches_the_crops_own_fruit_set_tip(self):
        by = {c['slug']: c for c in _pre()['crops']}
        for slug, spacing in THINNING.items():
            tips = ' '.join(t.get('text_seasoned', '') + t.get('text_beginner', '')
                            for t in by[slug]['tips_by_stage']['fruit_set'])
            self.assertIn(spacing, tips, f'{slug}: {spacing} is not what the record states')
            for field, v in P.TRIO[slug].items():
                self.assertIn(spacing, v, f'{slug}.{field} omits the thinning distance')

    def test_the_cherries_are_told_NOT_to_thin_and_are_given_no_spacing(self):
        """The first version of this guard searched for the word "thin" and flagged
        cherry-sweet's "Do not thin cherries" -- the word in a NEGATIVE instruction, which is the
        correct advice. A token scan is not the check; the check is whether the crop is told to
        space fruit. So: the cherries must carry an explicit no-thinning instruction, and must
        carry no spacing figure at all."""
        SPACING = r'every\s+\d+\s+to\s+\d+\s+inches|\d+\s+inches apart'
        for slug in NO_THINNING:
            joined = ' '.join(P.TRIO[slug].values())
            self.assertTrue(re.search(r'no thinning|do not thin|without hand thinning|'
                                      r'there is no thinning', joined, re.I),
                            f'{slug} never tells the reader NOT to thin')
            for field, v in P.TRIO[slug].items():
                self.assertIsNone(re.search(SPACING, v, re.I),
                                  f'{slug}.{field} gives a thinning distance for a cherry')

    def test_the_thinning_crops_are_never_told_NOT_to_thin(self):
        # The inverse, so the guard above cannot be satisfied by saying both things everywhere.
        for slug in THINNING:
            joined = ' '.join(P.TRIO[slug].values())
            self.assertIsNone(re.search(r'do not thin|no thinning', joined, re.I), slug)

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


class BearingHabit(unittest.TestCase):
    """The wave's whole point: these crops differ in HOW they bear, and the prose must not
    flatten that. A grower told to prune a cherry like a peach loses the spurs that carry its
    crop."""

    def test_one_year_wood_crops_say_renewal_pruning_is_required(self):
        for slug in ('peach', 'nectarine'):
            joined = ' '.join(P.TRIO[slug].values()).lower()
            self.assertIn('one-year', joined.replace('previous summer', 'one-year')
                          if 'one-year' not in joined else joined)

    def test_spur_bearers_say_prune_LIGHTER_in_BOTH_registers(self):
        """Per-register, not joined. The harness caught the joined version: three of the four
        fields could lose the spur advice entirely and the guard still passed on the fourth,
        which is the whole point of a wave that authors eight similar crops at once."""
        for slug in ('apricot', 'plum', 'cherry-sweet', 'cherry-sour'):
            for reg in ('beginner', 'seasoned'):
                v = P.TRIO[slug][f'first_harvest_notes_{reg}'].lower()
                self.assertIn('spur', v, f'{slug}.{reg} never mentions spurs')
                self.assertTrue(re.search(r'light|gentl|conserv|preserv', v),
                                f'{slug}.{reg} never says prune lighter')

    def test_the_two_pears_invert_each_other_in_EVERY_field(self):
        """The inversion is the single most consequential fact about either crop -- a European
        pear left to ripen on the tree browns at the core -- so it must survive in every field,
        not just wherever the joined string happened to find it. The harness caught the joined
        version: replacing one whole field with tree-ripe advice fired NOTHING."""
        for field in P.NEW_FIELDS:
            self.assertIn('firm', P.TRIO['pear-european'][field].lower(),
                          f'pear-european.{field} loses the picked-firm rule')
            self.assertTrue(re.search(r'tree-ripe|on the tree',
                                      P.TRIO['pear-asian'][field], re.I),
                            f'pear-asian.{field} loses the ripens-on-tree rule')

    def test_european_pear_is_never_told_to_pick_tree_ripe(self):
        for field, v in P.TRIO['pear-european'].items():
            self.assertIsNone(re.search(r'pick (?:each pear |them )?tree-ripe', v, re.I),
                              f'pear-european.{field} says pick tree-ripe')


if __name__ == '__main__':
    unittest.main(verbosity=2)
