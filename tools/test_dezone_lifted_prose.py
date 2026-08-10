#!/usr/bin/env python3
"""RED-first tests for the lifted-zone prose de-zoning pass.

THE DEFECT. `tools/build_zonespan_widen_patch.py` widened five warm regions by
`copy.deepcopy`-ing a donor zone's `resolved_by_zone` row onto the new zone label and
stamping `lifted_from_zone`. The DATA is right -- the 2023 USDA map moved the cities the
regions were authored for, so the row genuinely is that city's data. The PROSE was never
rewritten, so 66 cells tell the reader they are in the DONOR zone: a `ca_south_coast` z11
gardener reads "Zone 10 on the south coast almost never freezes".

THE FIX IS DE-ZONING, NOT RENUMBERING, and that is a correctness decision not a style one:
  * Every donor->lifted pair carries an IDENTICAL `region_chill_delivered` band
    (low_desert_az 9/10 both [100,400]; ca_south_coast 10/11 both [50,350]; ca_desert 10/11
    both [100,300]; hawaii_tropical 10-13 all [0,150]; se_gulf 9/10 both [350,650]),
    so every chill figure in the prose transfers verbatim and must SURVIVE the edit.
  * Renumbering would assert new zone-specific claims we cannot source. The clearest case:
    mandarin's ca_south_coast cell names the Ojai Pixie, and Ojai is not zone 11.
De-zoning removes a false statement and adds no new one.
"""
import copy
import json
import os
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import dezone_lifted_prose as dz  # noqa: E402
import promote_fixture  # noqa: E402

CANONICAL = os.path.join(REPO, 'crops_data_final.json')

# The state these rules were authored against. REBUILT from the pinned SHA, never read from live
# canonical: canonical moves after every promote, and a suite pointed at it would start measuring
# a different file. Six suites in this repo went silently vacuous exactly that way -- and the
# first version of THIS suite read live canonical and broke the moment its own promote landed.
BASE_SHA = '8d2b1a91eea725e66cd6317a4a5a395f0db3b3302fb93e4994262c3e6d42b289'

# Measured on canonical 8d2b1a91 before any edit.
EXPECTED_CELLS = 66
EXPECTED_STRINGS = 106
# 15, not 16: the naive regex also hits pawpaw ca_interior z9, whose "As in interior zone 8,
# pawpaw is marginal here" is CORRECT comparative prose on a non-lifted row.
EXPECTED_CROPS = 15

# The rule-tables FROZEN BY VALUE as of the measurement (PLA-162). RULES, SELF_REF and
# COMPARATIVE are RULES, not rows: nothing in the fixture can scope them, and they are applied
# at run time, so editing the live module changes what this suite measures over a fixture that
# never moved. Measured 2026-08-10 before the freeze: pruning one 'apparently dead' RULES pair
# (every pair looks dead against clean live canonical) turned TWELVE pinned tests red. The
# pinned classes below measure with these frozen copies via PinnedRulesCase;
# TestShippedState.test_live_rule_tables_match_the_frozen_pin is the unpinned tripwire.
RULES_AT_PIN = [
    ('Zone 11 in tropical Hawaii', 'Tropical Hawaii'),
    ('Tropical zone 11 in Hawaii', 'Tropical Hawaii'),
    ('Zone 11 tropical Hawaii', 'Tropical Hawaii'),
    ('Zone 11 in Hawaii', 'Tropical Hawaii'),
    ('Tropical zone 11', 'Tropical Hawaii'),
    ('Zone 11 Hawaii', 'Tropical Hawaii'),
    ('Zone 10 on the South Coast', 'The South Coast'),
    ('Zone 10 on the south coast', 'The south coast'),
    ('The warmest coastal zone 10', 'The warmest coastal ground'),
    ('The immediate coast in zone 10', 'The immediate coast'),
    ('South-coast zone 10', 'The south coast'),
    ('Zone 10 South Coast', 'The South Coast'),
    ('Zone 10 south coast', 'The south coast'),
    ('Zone 10 in the California desert', 'The California desert'),
    ('The hottest desert zone 10', 'The hottest desert'),
    ('Zone 10 in the low desert', 'The low desert'),
    ('Zone 10 in the desert', 'The desert'),
    ('Zone 10 low desert', 'The low desert'),
    ('Zone 10 desert', 'The desert'),
    ('Zone 9 in the Arizona low desert', 'The Arizona low desert'),
    ('The zone 9 Arizona low desert', 'The Arizona low desert'),
    ('Zone 9 in the Arizona desert', 'The Arizona desert'),
    ('Zone 9 Arizona low desert', 'The Arizona low desert'),
    ('Zone 9 across the Gulf region', 'The Gulf coast'),
    ('Zone 9 across the Gulf', 'The Gulf coast'),
    ('Zone 9 in the Southeast', 'The Gulf coast'),
    ('Zone 9 on the Gulf', 'The Gulf coast'),
    ('Zone 9 Gulf', 'The Gulf coast'),
    ('Zone 9 grows', 'The Gulf coast grows'),
    ('Low-desert zone 10', 'The low desert'),
    ('Low-desert zone 9', 'The low desert'),
    ('Thyme can persist in zone 9', 'Thyme can persist here'),
    ('Thyme takes zone 10 heat', 'Thyme takes the heat'),
    ("Zone 10's mild", 'The mild'),
    ('In zone 10, sage', 'Sage'),
    ('In zone 11, sage', 'Sage'),
    ('In zone 9, sage', 'Sage'),
    ('In zone 9, heat and humidity', 'Heat and humidity'),
]
RULES_AT_PIN.sort(key=lambda r: -len(r[0]))  # mirror the module's longest-first ordering

import re  # noqa: E402

SELF_REF_AT_PIN = re.compile(
    r'(?:^|(?<=[.;] ))(?:[A-Z][a-z-]+(?:[ -][a-z]+){0,3} )?[Zz]ones? (\d{1,2})\b'
    r'(?![^.]*\b(?:hardy|rated|than|compared|colder|warmer|below|above|south of|north of)\b)'
    r'[^.]*?\b(?:is|are|sits|fruits|banks|has|have|does|gets|stays|runs|ripens|grows)\b')
COMPARATIVE_AT_PIN = re.compile(r'(?i)^\s*(?:as in|like|unlike|compared with|versus)\b')


def load():
    """The pinned pre-state. Hash-verified by promote_fixture; an unknown SHA raises."""
    return json.loads(promote_fixture.pre_state(BASE_SHA))


def load_live():
    with open(CANONICAL, encoding='utf-8') as fh:
        return json.load(fh)


class PinnedRulesCase(unittest.TestCase):
    """Base for the pinned-measurement classes: evaluate the fixture through the rule-tables
    AS OF the measurement, restored after every test so TestShippedState still sees live."""

    def setUp(self):
        ctx = promote_fixture.tables_frozen(dz, {
            'RULES': RULES_AT_PIN,
            'SELF_REF': SELF_REF_AT_PIN,
            'COMPARATIVE': COMPARATIVE_AT_PIN,
        })
        ctx.__enter__()
        self.addCleanup(ctx.__exit__, None, None, None)
        self.data = load()


class TestShippedState(unittest.TestCase):
    """The pass has landed, so live canonical must stay clean. This is the regression guard
    the pinned-fixture tests above cannot provide -- they describe the transformation, this
    describes what is actually shipping to readers."""

    def test_live_canonical_has_no_lifted_row_naming_the_wrong_zone(self):
        self.assertEqual(dz.find_defects(load_live()), [])

    def test_live_rule_tables_match_the_frozen_pin(self):
        """The unpinned equality tripwire. This class does NOT inherit PinnedRulesCase, so
        dz.* here is the live module state. A deliberate rule change fails THIS test, once
        and loudly, instead of silently re-shaping the pinned measurement -- update the
        frozen copies only with the change spelled out in the diff."""
        self.assertEqual(dz.RULES, RULES_AT_PIN)
        self.assertEqual(dz.SELF_REF.pattern, SELF_REF_AT_PIN.pattern)
        self.assertEqual(dz.COMPARATIVE.pattern, COMPARATIVE_AT_PIN.pattern)


class TestDetection(PinnedRulesCase):

    def test_finds_the_measured_defect_set(self):
        d = dz.find_defects(self.data)
        cells = {(r.slug, r.region, r.zone) for r in d}
        self.assertEqual(len(cells), EXPECTED_CELLS)
        self.assertEqual(len(d), EXPECTED_STRINGS)
        self.assertEqual(len({r.slug for r in d}), EXPECTED_CROPS)

    def test_every_defect_sits_on_a_lifted_row(self):
        """The widen pass is the whole mechanism; anything else is a different bug."""
        for r in dz.find_defects(self.data):
            cell = (self.data['crops'][r.crop_index]['regions'][r.region]
                    ['resolved_by_zone'][r.zone])
            self.assertIn('lifted_from_zone', cell,
                          f'{r.slug}/{r.region}/z{r.zone} is not a lifted row')

    def test_comparative_prose_is_not_flagged(self):
        """'As in interior zone 8, pawpaw is marginal here' is CORRECT prose.

        A check that cannot tell a self-reference from a comparison would rewrite
        legitimate copy. This is the known false positive of the naive regex.
        """
        d = dz.find_defects(self.data)
        self.assertEqual(
            [r for r in d if r.slug == 'pawpaw'], [],
            'pawpaw ca_interior z9 compares itself to zone 8; it must not be flagged')

    def test_comparative_prose_on_a_LIFTED_row_is_not_flagged(self):
        """The test above passes even with COMPARATIVE deleted, because pawpaw's row is not
        lifted and the lifted filter already excludes it. Mutation-testing caught that: the
        guard was vacuous. Put the comparison where the filter cannot save it."""
        data = copy.deepcopy(self.data)
        after = dz.apply(data)
        crop = next(c for c in after['crops'] if c['slug'] == 'lime')
        cell = crop['regions']['ca_south_coast']['resolved_by_zone']['11']
        cell['suitability_note_seasoned'] = (
            'As in zone 10, lime is dependable here and fruits through a long season.')
        self.assertEqual(
            [r for r in dz.find_defects(after)
             if r.slug == 'lime' and r.zone == '11'], [],
            'a comparison on a lifted row was mistaken for a self-reference')

    def test_donor_rows_themselves_are_never_flagged(self):
        """A donor row naming its own zone is correct and must be left alone."""
        for r in dz.find_defects(self.data):
            self.assertNotEqual(str(r.named_zone), str(r.zone))


class TestRules(PinnedRulesCase):

    def test_every_defect_string_is_covered_by_a_rule(self):
        """No silent skips: a string we detect but cannot rewrite is a failure, not a pass."""
        uncovered = [r for r in dz.find_defects(self.data)
                     if dz.rewrite(r.text) is None]
        self.assertEqual(uncovered, [], f'{len(uncovered)} strings have no rule')

    def test_rewrite_changes_only_the_zone_phrase(self):
        """The tail must be byte-identical -- this pass corrects a label, not content."""
        for r in dz.find_defects(self.data):
            new = dz.rewrite(r.text)
            old_phrase, new_phrase = dz.rule_for(r.text)
            self.assertEqual(new, r.text.replace(old_phrase, new_phrase, 1))
            self.assertEqual(r.text.count(old_phrase), 1,
                             f'phrase {old_phrase!r} is not unique in the string')

    def test_chill_figures_survive_verbatim(self):
        """The numbers are the reason de-zoning is safe; losing one would invert that."""
        checks = [
            ('plum', 'ca_desert', '11', 'about 100 to 300 hours'),
            ('plum', 'ca_south_coast', '11', 'roughly 50 to 350 hours'),
            ('plum', 'hawaii_tropical', '12', '0 to 150 hours'),
            ('persimmon', 'ca_south_coast', '11', 'about 50 to 350 hours'),
            ('persimmon', 'low_desert_az', '10', 'roughly 100 to 400 chill hours'),
            ('nectarine', 'low_desert_az', '10', 'about 300 to 400 chill hours'),
        ]
        after = dz.apply(copy.deepcopy(self.data))
        for slug, region, zone, figure in checks:
            crop = next(c for c in after['crops'] if c['slug'] == slug)
            cell = crop['regions'][region]['resolved_by_zone'][zone]
            blob = ' '.join(v for k, v in cell.items()
                            if isinstance(v, str) and k.endswith(('_seasoned', '_beginner')))
            self.assertIn(figure, blob, f'{slug}/{region}/z{zone} lost {figure!r}')

    def test_replacements_obey_consumer_copy_rules(self):
        """CLAUDE.md: no em dashes, no '--', temps render as degrees-F."""
        for old, new in dz.RULES:
            self.assertNotIn('—', new)
            self.assertNotIn('--', new)
            self.assertNotIn('degrees', new.lower())
            self.assertNotEqual(old, new)

    def test_no_rule_reintroduces_a_zone_number(self):
        for _old, new in dz.RULES:
            self.assertNotRegex(new, r'(?i)\bzones?\s*\d')


class TestApply(PinnedRulesCase):

    def test_apply_clears_every_defect(self):
        after = dz.apply(copy.deepcopy(self.data))
        self.assertEqual(dz.find_defects(after), [])

    def test_apply_is_idempotent(self):
        once = dz.apply(copy.deepcopy(self.data))
        twice = dz.apply(copy.deepcopy(once))
        self.assertEqual(once, twice)

    def test_footprint_is_exactly_the_expected_strings(self):
        """Prove the blast radius: nothing outside the 106 target strings may move."""
        before = self.data
        after = dz.apply(copy.deepcopy(before))
        moved = []

        def walk(a, b, path):
            if isinstance(a, dict):
                self.assertEqual(set(a), set(b), f'key set changed at {path}')
                for k in a:
                    walk(a[k], b[k], f'{path}.{k}')
            elif isinstance(a, list):
                self.assertEqual(len(a), len(b), f'list length changed at {path}')
                for i, (x, y) in enumerate(zip(a, b)):
                    walk(x, y, f'{path}[{i}]')
            elif a != b:
                moved.append(path)

        walk(before, after, '$')
        self.assertEqual(len(moved), EXPECTED_STRINGS,
                         f'expected {EXPECTED_STRINGS} changed strings, got {len(moved)}')
        for p in moved:
            self.assertIn('.resolved_by_zone.', p)
            self.assertTrue(p.endswith(('_seasoned', '_beginner')), p)

    def test_non_lifted_cells_are_byte_identical(self):
        before = self.data
        after = dz.apply(copy.deepcopy(before))
        for i, crop in enumerate(before['crops']):
            for region, rv in (crop.get('regions') or {}).items():
                for zone, cell in (rv.get('resolved_by_zone') or {}).items():
                    if isinstance(cell, dict) and 'lifted_from_zone' in cell:
                        continue
                    self.assertEqual(
                        cell,
                        after['crops'][i]['regions'][region]['resolved_by_zone'][zone],
                        f'non-lifted {crop["slug"]}/{region}/z{zone} moved')

    def test_lifted_marker_and_all_non_prose_keys_are_preserved(self):
        """Only prose moves: suitability, dates, calendar and the lift marker stay put."""
        before = self.data
        after = dz.apply(copy.deepcopy(before))
        for i, crop in enumerate(before['crops']):
            for region, rv in (crop.get('regions') or {}).items():
                for zone, cell in (rv.get('resolved_by_zone') or {}).items():
                    if not isinstance(cell, dict):
                        continue
                    new = after['crops'][i]['regions'][region]['resolved_by_zone'][zone]
                    for k, v in cell.items():
                        if k.endswith(('_seasoned', '_beginner')):
                            continue
                        self.assertEqual(v, new[k], f'{crop["slug"]}/{region}/z{zone}.{k}')


class TestAdversarial(PinnedRulesCase):
    """CLAUDE.md: a gate is not done until a defect has been sneaked at it."""


    def test_detects_an_injected_wrong_zone_on_a_clean_lifted_cell(self):
        data = copy.deepcopy(self.data)
        after = dz.apply(data)
        crop = next(c for c in after['crops'] if c['slug'] == 'lemon')
        cell = crop['regions']['hawaii_tropical']['resolved_by_zone']['12']
        cell['suitability_note_seasoned'] = (
            'Zone 11 in Hawaii is frost-free, so lemon bears year-round.')
        self.assertTrue([r for r in dz.find_defects(after)
                         if r.slug == 'lemon' and r.zone == '12'],
                        'an injected donor-zone label was not detected')

    def test_does_not_fire_when_the_named_zone_is_the_cells_own(self):
        data = copy.deepcopy(self.data)
        after = dz.apply(data)
        crop = next(c for c in after['crops'] if c['slug'] == 'lemon')
        cell = crop['regions']['hawaii_tropical']['resolved_by_zone']['12']
        cell['suitability_note_seasoned'] = (
            'Zone 12 in Hawaii is frost-free, so lemon bears year-round.')
        self.assertEqual([r for r in dz.find_defects(after)
                          if r.slug == 'lemon' and r.zone == '12'], [])

    def test_rewrite_refuses_a_string_it_has_no_rule_for(self):
        """Never silently pass through text the pass does not understand."""
        self.assertIsNone(dz.rewrite('Zone 4 in Narnia is pleasant and grows turkish delight.'))

    def test_apply_leaves_a_wrong_zone_on_a_NON_lifted_row_untouched(self):
        """This promote is scoped to the widen artifact. A wrong zone on a row the widen
        never touched is a DIFFERENT defect needing its own ruling, so it must not be
        swept up here. Without this, dropping the lifted_from_zone filter passes silently."""
        data = copy.deepcopy(self.data)
        crop = next(c for c in data['crops'] if c['slug'] == 'lemon')
        cell = crop['regions']['ca_interior']['resolved_by_zone']['9']
        self.assertNotIn('lifted_from_zone', cell)
        planted = 'Zone 8 in the valley is marginal and fruits only in mild winters.'
        cell['suitability_note_seasoned'] = planted
        after = dz.apply(data)
        self.assertEqual(
            after['crops'][[c['slug'] for c in after['crops']].index('lemon')]
            ['regions']['ca_interior']['resolved_by_zone']['9']['suitability_note_seasoned'],
            planted, 'apply() rewrote a row the zone-span widen never lifted')


if __name__ == '__main__':
    unittest.main()
