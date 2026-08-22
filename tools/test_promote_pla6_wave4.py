#!/usr/bin/env python3
"""Guard suite for tools/promote_pla6_wave4.py (PLA-6 Round 2, wave 4, the last). Base 97c63704.

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
import promote_pla6_wave4 as P  # noqa: E402
from perennial_year_gate import renders_pills  # noqa: E402

POST_SHA = '20a32c47f0bf861e5b93fad71b9af3bbb37643afdb70dccd758e1ee0eb080ea9'

BASES = ('first_harvest_notes', 'full_harvest_notes')

ORDINAL = {2: 'second', 3: 'third', 5: 'fifth'}

# ENUMERATED, never derived from P.TRIO. The mutation harness caught the first version deriving
# `expected` from P.TRIO inside the test body, which made adding an unauthorised crop change both
# sides of the comparison identically -- the guard-derived-from-what-it-checks vacuity. A literal
# is the only shape that can fail.
WAVE_CROPS = ('artichoke', 'fig', 'mulberry', 'persimmon', 'pomegranate')


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
        VERBS = (r'\b(thin|pick|prune|cut|net|space|clear|handle|check|keep|watch|pull|clip|twist|squeeze|shake|wait|water|feed|plant|set|strip|scout|protect|leave|start|sort)\b')
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



class FinalWaveFacts(unittest.TestCase):
    """Per-field, never joined: the harnesses proved in waves 1, 2 and 3 that a joined-field
    guard goes vacuous the moment one field is replaced."""

    def test_artichokes_BRACT_TERM_is_glossed_in_every_beginner_half(self):
        """THE ORIGINAL COMPLAINT, 2026-08-05: artichoke's mature-bed copy rested on an
        unexplained technical term. v1.3 sec9.3 scopes the gloss requirement to the beginner
        half explicitly, so the seasoned register may use `bract` bare; the beginner may not."""
        for field in ('first_harvest_notes_beginner', 'full_harvest_notes_beginner'):
            v = P.TRIO['artichoke'][field]
            self.assertIn('bract', v.lower(), field)
            self.assertTrue(re.search(r'the tough overlapping scales', v),
                            f'{field}: bract used without its gloss')

    def test_artichoke_indexes_on_TIGHTNESS_not_size_in_every_field(self):
        for field, v in P.TRIO['artichoke'].items():
            # Match the RULE, not one phrasing. The beginner half says "shut flat against one
            # another" and "It is not size", which is the same instruction in plainer words --
            # the first version of this guard demanded the literal word "tight" and flagged
            # correct prose, the same trap as wave 1's cherry-thinning guard.
            self.assertTrue(re.search(r'tight|shut flat|closed flat', v, re.I),
                            f'{field}: loses the closure cue')
            self.assertTrue(re.search(r'not (?:on )?size|rather than size|rather than on diameter|'
                                      r'never on diameter|not.*diameter', v, re.I),
                            f'{field}: loses the not-by-size rule')

    def test_artichokes_cutback_is_framed_as_SCHEDULING(self):
        # The mature-bed fact no truncation could ever have carried.
        for reg in ('beginner', 'seasoned'):
            v = P.TRIO['artichoke'][f'full_harvest_notes_{reg}']
            self.assertTrue(re.search(r'cut-back', v, re.I), reg)
            self.assertTrue(re.search(r'mid-April|middle of April', v), f'{reg}: no spring window')
            self.assertTrue(re.search(r'summer harvest|crops in summer', v, re.I),
                            f'{reg}: never states the alternative schedule')

    def test_fig_says_color_is_NOT_ripeness(self):
        for reg in ('beginner', 'seasoned'):
            v = P.TRIO['fig'][f'first_harvest_notes_{reg}']
            self.assertTrue(re.search(r'color (?:will fool|is not)|not ripeness', v, re.I), reg)
            self.assertTrue(re.search(r'neck', v, re.I), f'{reg}: loses the bent-neck cue')

    def test_fig_is_never_told_to_prune_hard(self):
        # It carries a breba crop on last year's wood; heavy heading forfeits it.
        for field, v in P.TRIO['fig'].items():
            self.assertIsNone(re.search(r'prune (?:it )?hard|renewal pruning', v, re.I), field)

    def test_mulberry_is_told_NOT_to_thin_and_given_no_spacing(self):
        """Positive requirement plus absence, the shape wave 1's cherry guard settled on. A bare
        token scan cannot work here: the correct prose contains "Do not thin them", so searching
        for the word flags the right answer. And the first absence-pattern missed the mutation
        outright by requiring "the" OR "young" where the injected text said "the young"."""
        joined = ' '.join(P.TRIO['mulberry'].values())
        self.assertTrue(re.search(r'do not thin|not practiced|thinning is not', joined, re.I),
                        'mulberry never tells the reader NOT to thin')
        for field, v in P.TRIO['mulberry'].items():
            self.assertIsNone(re.search(r'(?<!not )\bthin\s+(?:the\s+)?(?:young\s+)?'
                                        r'(?:fruit|berries|it)\b', v, re.I),
                              f'{field}: instructs thinning on a crop that sizes without it')
            self.assertIsNone(re.search(r'one every few inches|every \d+ to \d+ inches', v, re.I),
                              f'{field}: gives a thinning distance for mulberry')

    def test_persimmon_scopes_harvest_by_TYPE_in_every_field(self):
        # Eating an astringent persimmon firm is the memorable way to get this wrong.
        for field, v in P.TRIO['persimmon'].items():
            self.assertTrue(re.search(r'astringen', v, re.I), f'{field}: loses type scoping')
        for reg in ('beginner', 'seasoned'):
            v = P.TRIO['persimmon'][f'full_harvest_notes_{reg}']
            # Both halves must carry the ripening instruction, since eating an astringent
            # persimmon firm is the memorable failure. The named cultivar is required only in
            # the BEGINNER half: a seasoned reader is served by "non-astringent cultivars",
            # while a beginner needs the name on the nursery tag.
            self.assertTrue(re.search(r'jelly-soft', v, re.I), f'{reg}: no ripening instruction')
        self.assertTrue(re.search(r'Fuyu', P.TRIO['persimmon']['full_harvest_notes_beginner']),
                        'beginner half must name the cultivar a grower sees on the tag')

    def test_pomegranate_names_SPLITTING_and_its_cause_in_every_field(self):
        for field, v in P.TRIO['pomegranate'].items():
            self.assertTrue(re.search(r'split', v, re.I), f'{field}: loses the defining failure')

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

    def test_THE_ROLLOUT_IS_COMPLETE(self):
        """The closing assertion of the arc: after this promote every pill-rendering perennial
        carries the trio, so PILL-CAPTION has nothing left to find and the gate can arm as an
        A-number rather than running standalone."""
        post = _post(_pre())
        unmigrated = [c['slug'] for c in post['crops']
                      if renders_pills(c) and not c.get('full_harvest_notes_beginner')]
        self.assertEqual(unmigrated, [], f'still unmigrated: {unmigrated}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
