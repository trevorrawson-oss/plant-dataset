#!/usr/bin/env python3
"""Guard suite for tools/promote_pla6_year_trio.py (PLA-6 Round 2 pilot). Base fe26f783.

Run: python3 tools/test_promote_pla6_year_trio.py   (also collected by pytest)

REPLAY-PINNED, SO THERE IS NO RED PHASE AND THIS SUITE DOES NOT CLAIM ONE. `pre` is
reconstructed from the pinned base SHA via promote_fixture, never read from live canonical, and
`post` is the promote's OWN output rather than a future canonical -- so this stays green across
every later promote instead of reddening on all of them. That construction also means the guards
are green from birth and cannot be observed failing first, which is exactly why two other things
carry the non-vacuity evidence instead:

  * a REACHABILITY guard proving the base really contained what the promote was written against
    (the four trio fields ABSENT on all four crops, each edit's find-string present exactly once),
    so a guard cannot pass by operating on nothing; and
  * tools/mutate_pla6_year_trio_suite.py, the PLA-215 mutation harness, which is the only
    evidence any of these families can actually fail.

BLAST RADIUS uses `assert set(pre) == set(post)` BEFORE any value comparison, at both the crop
level and the per-crop key level. Iterating `pre` alone makes ADDITIONS in `post` invisible, which
was all four PLA-162 defects -- and this promote's whole purpose is additions, so that failure
mode would hide the entire change.
"""
import copy
import difflib
import hashlib
import json
import os
import re
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, 'tools')
sys.path.insert(0, TOOLS)

import promote_fixture  # noqa: E402
import promote_pla6_year_trio as P  # noqa: E402
from perennial_year_gate import pill_caption_violations, renders_pills  # noqa: E402

POST_SHA = '0cc37afe6597d43eac4e867b5eefa625aed5002dfc20628e4a5fbac80215e66b'

BASES = ('first_harvest_notes', 'full_harvest_notes')

# Fields this promote is ALLOWED to touch. Anything else changing is a blast-radius failure.
EXPECTED_TOUCHED = {
    (slug, field) for slug, fields in P.TRIO.items() for field in fields
} | set(P.EDITS)


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre):
    return P.apply_to(copy.deepcopy(pre))


class Fixture(unittest.TestCase):
    """The fixture itself, before any guard trusts it."""

    def test_base_reconstructs_to_the_pinned_sha(self):
        raw = promote_fixture.pre_state(P.BASE_SHA)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), P.BASE_SHA)

    def test_post_serializes_to_the_pinned_post_sha(self):
        out = json.dumps(_post(_pre()), ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        self.assertEqual(hashlib.sha256(out).hexdigest(), POST_SHA)

    def test_output_is_compact(self):
        out = json.dumps(_post(_pre()), ensure_ascii=False, separators=(',', ':'))
        self.assertNotIn(', "', out)
        self.assertNotIn('\n', out)


class Reachability(unittest.TestCase):
    """The non-vacuity evidence for a suite with no RED phase: prove the base actually held
    what the promote claims to change, so no guard can pass by operating on nothing."""

    def test_all_four_trio_fields_were_absent_on_every_pilot_crop(self):
        by = {c['slug']: c for c in _pre()['crops']}
        for slug, fields in P.TRIO.items():
            for field in fields:
                self.assertNotIn(field, by[slug],
                                 f'{slug}.{field} already existed; the promote would overwrite')

    def test_every_edit_find_string_is_present_exactly_once_in_the_base(self):
        by = {c['slug']: c for c in _pre()['crops']}
        for (slug, field), (find, _r) in P.EDITS.items():
            self.assertEqual(by[slug][field].count(find), 1,
                             f'{slug}.{field}: find-string not uniquely reachable')

    def test_the_pilot_set_really_is_diverse(self):
        by = {c['slug']: c for c in _pre()['crops']}
        # three pill-rendering crops with materially different spans, plus one N/A case
        spans = {s: by[s]['years_to_first_harvest'] for s in P.PILL_CROPS}
        self.assertEqual(spans['apple'], [2, 5])
        self.assertEqual(spans['pawpaw'], [4, 7])
        self.assertEqual(spans['asparagus'], [2, 3])
        self.assertFalse(renders_pills(by['sage']), 'sage must be the legitimately-N/A case')


class BlastRadius(unittest.TestCase):
    """Nothing outside EXPECTED_TOUCHED may move."""

    def test_the_crop_roster_is_unchanged(self):
        pre, post = _pre(), None
        post = _post(pre)
        pre_slugs = {c['slug'] for c in pre['crops']}
        post_slugs = {c['slug'] for c in post['crops']}
        assert pre_slugs == post_slugs, 'roster changed'   # SET EQUALITY BEFORE value comparison
        self.assertEqual(len(pre['crops']), len(post['crops']))

    def test_top_level_keys_are_unchanged(self):
        pre = _pre()
        post = _post(copy.deepcopy(pre))
        assert set(pre) == set(post)
        for k in pre:
            if k == 'crops':
                continue
            self.assertEqual(pre[k], post[k], f'top-level {k} changed')

    def test_only_the_expected_crop_fields_differ(self):
        pre = _pre()
        post = _post(copy.deepcopy(pre))
        pre_by = {c['slug']: c for c in pre['crops']}
        post_by = {c['slug']: c for c in post['crops']}
        assert set(pre_by) == set(post_by)
        touched = set()
        for slug in post_by:
            a, b = pre_by[slug], post_by[slug]
            assert set(a) | set(b) == set(b), f'{slug}: a key disappeared'
            for field in set(a) | set(b):
                if a.get(field, '\0ABSENT') != b.get(field, '\0ABSENT'):
                    touched.add((slug, field))
        self.assertEqual(touched, EXPECTED_TOUCHED,
                         f'unexpected: {touched - EXPECTED_TOUCHED}; '
                         f'missing: {EXPECTED_TOUCHED - touched}')

    def test_exactly_four_crops_are_touched(self):
        self.assertEqual({s for s, _ in EXPECTED_TOUCHED},
                         {'apple', 'pawpaw', 'asparagus', 'cherry-sweet'})


class TrioShape(unittest.TestCase):
    def test_pill_crops_carry_all_four_fields_non_null(self):
        by = {c['slug']: c for c in _post(_pre())['crops']}
        for slug in P.PILL_CROPS:
            for field in P.NEW_FIELDS:
                self.assertTrue(by[slug].get(field), f'{slug}.{field} empty')

    def test_the_na_crop_is_a_deliberate_NON_target(self):
        """sage renders no pills, so it takes the trio by ABSENCE. The contract originally said
        null; A29 register-fill overruled that, because a `_beginner`/`_seasoned` field that
        EXISTS must be authored. Asserted by name so the omission is a recorded decision rather
        than a crop someone forgot."""
        by = {c['slug']: c for c in _post(_pre())['crops']}
        self.assertFalse(renders_pills(by['sage']))
        for field in P.NEW_FIELDS:
            self.assertNotIn(field, by['sage'],
                             f'sage renders no pills; {field} must be absent, not null')
        self.assertNotIn('sage', P.TRIO)

    def test_the_na_crops_existing_year_one_notes_survive_byte_identical(self):
        # Nulling real authored prose would be destructive and gains nothing, since sage's
        # Establishing pill is suppressed anyway.
        pre_by = {c['slug']: c for c in _pre()['crops']}
        post_by = {c['slug']: c for c in _post(_pre())['crops']}
        for r in ('year_one_notes_beginner', 'year_one_notes_seasoned'):
            self.assertTrue(pre_by['sage'][r])
            self.assertEqual(pre_by['sage'][r], post_by['sage'][r])

    def test_every_authored_crop_actually_renders_pills(self):
        """The presence floor, keyed on the crops where the caption is actually shown. A crop
        that renders none has nothing for the trio to caption, and authoring one would put prose
        somewhere no reader can reach -- the year_one_notes_* failure this arc exists to end."""
        by = {c['slug']: c for c in _post(_pre())['crops']}
        for slug in P.TRIO:
            self.assertTrue(renders_pills(by[slug]), f'{slug} renders no pills')
            for field in P.NEW_FIELDS:
                self.assertTrue(by[slug][field], f'{slug}.{field} empty')

    def test_no_trio_field_is_ever_null(self):
        """A29 register-fill forbids a null _beginner/_seasoned field that exists. This is the
        guard that keeps the corrected contract from drifting back."""
        by = {c['slug']: c for c in _post(_pre())['crops']}
        for crop in by.values():
            for field in P.NEW_FIELDS:
                if field in crop:
                    self.assertIsNotNone(crop[field], f"{crop['slug']}.{field} is null")


class Mechanics(unittest.TestCase):
    """language_and_copy_architecture v1.1 over every string this promote writes."""

    def _written(self):
        out = []
        for slug, fields in P.TRIO.items():
            for field, v in fields.items():
                if v:
                    out.append((f'{slug}.{field}', v))
        for (slug, field), (_f, replace) in P.EDITS.items():
            out.append((f'{slug}.{field}(edit)', replace))
        return out

    def test_no_em_dash_en_dash_or_double_hyphen(self):
        for where, v in self._written():
            for bad in ('—', '–', '--'):
                self.assertNotIn(bad, v, f'{where} contains {bad!r}')

    def test_american_english(self):
        for where, v in self._written():
            self.assertIsNone(re.search(r'\b(colour|fibre|centre|metre|grey|programme|internalise|realise|organise|recognise|emphasise|minimise|maximise|analyse|defence|labour|favour|behaviour)\b', v, re.I), where)

    def test_brand_name_is_lowercase_mid_sentence(self):
        for where, v in self._written():
            for m in re.finditer(r'(?<=[a-z,;] )Plant\b', v):
                self.fail(f'{where}: capitalized brand mid-sentence at {m.start()}')

    def test_temperatures_render_with_the_degree_symbol(self):
        for where, v in self._written():
            self.assertIsNone(re.search(r'\b\d+\s*(?:degrees?\s*F\b|F\b(?!\w))', v), where)


class RegisterIntegrity(unittest.TestCase):
    """v1.2 sec9 actionability floor and v1.3 sec9.1 differentiation."""

    def test_every_authored_pair_has_both_registers(self):
        for slug, fields in P.TRIO.items():
            for base in ('first_harvest_notes', 'full_harvest_notes'):
                b, s = fields[base + '_beginner'], fields[base + '_seasoned']
                self.assertEqual(b is None, s is None, f'{slug}.{base}: half a pair')

    def test_no_pair_is_byte_identical(self):
        for slug, fields in P.TRIO.items():
            for base in ('first_harvest_notes', 'full_harvest_notes'):
                b, s = fields[base + '_beginner'], fields[base + '_seasoned']
                if b and s:
                    self.assertNotEqual(b.strip().lower(), s.strip().lower(), f'{slug}.{base}')

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
        # The actionability floor: the beginner register must carry the ACTION, not only the
        # caution. Asparagus year 2 is the case that matters -- over-cutting costs the bed.
        VERBS = r'\b(cut|take|thin|pick|prune|plant|move|check|leave|stop|pull|keep|rake|water)\b'
        for slug, fields in P.TRIO.items():
            for field, v in fields.items():
                if v and field.endswith('_beginner'):
                    self.assertIsNotNone(re.search(VERBS, v, re.I), f'{slug}.{field}')


class QuantityAgreement(unittest.TestCase):
    """v1.3 sec9.2: where both registers state a quantity, they must AGREE. A register may omit
    a number or round one; it may not give a different one. These are the load-bearing figures,
    named explicitly rather than inferred, so a future edit to either half reddens."""

    def _t(self, slug, field):
        return P.TRIO[slug][field]

    def test_asparagus_year_two_ceiling_agrees(self):
        b = self._t('asparagus', 'first_harvest_notes_beginner')
        s = self._t('asparagus', 'first_harvest_notes_seasoned')
        for half in (b, s):
            self.assertIn('two weeks', half)
            self.assertIn('6 to 8 inches', half)

    def test_asparagus_bed_age_ramp_agrees_across_registers_and_with_the_dataset(self):
        b = self._t('asparagus', 'full_harvest_notes_beginner')
        s = self._t('asparagus', 'full_harvest_notes_seasoned')
        for half in (b, s):
            self.assertIn('two to four weeks', half)
            self.assertIn('six to eight', half)
            self.assertIn('six to ten', half)
        # and they must match the crop's own harvest_ramp_weeks, not a remembered figure
        by = {c['slug']: c for c in _pre()['crops']}
        ramp = {e['bed_year']: e['weeks'] for e in by['asparagus']['harvest_ramp_weeks']}
        self.assertEqual(ramp[3], [2, 4])
        self.assertEqual(ramp[4], [6, 8])
        self.assertEqual(ramp[5], [6, 10])

    def test_asparagus_harvest_cadence_agrees(self):
        # The divergence found during drafting: certified asparagus says "every day or two"
        # (beginner) against "every one to three days" (seasoned) in two other field families.
        # The new fields must NOT inherit it.
        b = self._t('asparagus', 'full_harvest_notes_beginner')
        s = self._t('asparagus', 'full_harvest_notes_seasoned')
        self.assertIn('every day or two', b)
        self.assertIn('every day or two', s)
        self.assertNotIn('one to three days', b)
        self.assertNotIn('one to three days', s)

    def test_pawpaw_pollinizer_distance_is_in_BOTH_registers(self):
        # Trevor's call: without the figure a beginner plants one tree in the front yard and one
        # in the back. That makes it an ACTIONABILITY item, not a precision one.
        for field in ('first_harvest_notes_beginner', 'first_harvest_notes_seasoned'):
            self.assertIn('30 feet', self._t('pawpaw', field), field)

    def test_pawpaw_bearing_ages_agree(self):
        b = self._t('pawpaw', 'first_harvest_notes_beginner')
        s = self._t('pawpaw', 'first_harvest_notes_seasoned')
        self.assertIn('five to eight', b)
        self.assertIn('five to eight', s)

    def test_apple_thinning_figure_agrees(self):
        for field in ('first_harvest_notes_beginner', 'first_harvest_notes_seasoned',
                      'full_harvest_notes_beginner', 'full_harvest_notes_seasoned'):
            self.assertIn('one per cluster' if field.endswith('beginner') else 'one fruit per cluster',
                          self._t('apple', field), field)


class RenderedFieldRepairs(unittest.TestCase):
    """The two pollinizer-distance repairs, and the reason they exist: TreePollinationCard reads
    the CROP-LEVEL pollinator_notes_*, while the distance lived only in the nested
    pollination.notes_beginner that no consumer reads."""

    def test_each_edit_removed_its_find_and_installed_its_replacement(self):
        pre_by = {c['slug']: c for c in _pre()['crops']}
        post_by = {c['slug']: c for c in _post(_pre())['crops']}
        for (slug, field), (find, replace) in P.EDITS.items():
            self.assertIn(find, pre_by[slug][field])
            self.assertNotIn(find, post_by[slug][field], f'{slug}.{field}: edit was a no-op')
            self.assertIn(replace, post_by[slug][field])

    def test_the_distance_now_reaches_the_RENDERED_field(self):
        post_by = {c['slug']: c for c in _post(_pre())['crops']}
        for slug, feet in (('pawpaw', '30 feet'), ('cherry-sweet', '100 feet')):
            self.assertIn(feet, post_by[slug]['pollinator_notes_beginner'],
                          f'{slug}: distance still absent from the field the card renders')

    def test_the_distance_matches_the_structured_field_it_restates(self):
        post_by = {c['slug']: c for c in _post(_pre())['crops']}
        for slug, feet in (('pawpaw', 30), ('cherry-sweet', 100)):
            self.assertEqual(post_by[slug]['pollination']['pollinizer_distance_ft'], feet)
            self.assertIn(f'{feet} feet', post_by[slug]['pollinator_notes_beginner'])

    def test_the_close_together_phrasing_is_gone_from_pawpaw(self):
        post_by = {c['slug']: c for c in _post(_pre())['crops']}
        self.assertNotIn('close together', post_by['pawpaw']['pollinator_notes_beginner'])

    def test_pawpaws_establishing_pill_also_carries_the_figure(self):
        # The siting decision is made in year one, so the Establishing pill is where a
        # first-year owner needs it.
        post_by = {c['slug']: c for c in _post(_pre())['crops']}
        self.assertIn('30 feet', post_by['pawpaw']['year_one_notes_beginner'])


class GateStability(unittest.TestCase):
    """This promote does not touch harvest_ready_*, so perennial_year_gate's PILL-CAPTION
    findings must be exactly unchanged. If they move, something was edited that should not be."""

    def test_pill_caption_findings_are_identical_pre_and_post(self):
        pre, post = _pre(), None
        post = _post(copy.deepcopy(pre))
        def ids(data):
            return sorted(f"{c['slug']}:{v.split(':')[1].strip()}"
                          for c in data['crops'] if c.get('perennial') is True
                          for v in pill_caption_violations(c))
        self.assertEqual(ids(pre), ids(post))
        self.assertEqual(ids(post), ['artichoke:beginner', 'artichoke:seasoned',
                                     'mandarin-clementine:seasoned', 'orange-navel:seasoned'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
