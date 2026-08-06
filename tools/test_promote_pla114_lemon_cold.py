#!/usr/bin/env python3
"""Guards for the PLA-114 lemon cold promote (6b2dcb8e -> next).

RED BEFORE GREEN: every check here asserts the POST state, so the whole suite must FAIL on the
pre-state. It is run both ways and mutation-tested before the promote is trusted.

NO SKIP GUARD. [[promote-guards-went-vacuous-on-sha-skip]] -- six suites once reported green while
running zero checks. The pre-state is rebuilt from `promote_fixture`, hash-verified, so these
compare POST-canonical against a reconstructed PRE rather than against whatever canonical happens
to be.

THE TRIPWIRE IS ENUMERATED, NOT BLANKET. This promote moves NO consumer prose, and the fourteen
leaf-and-fruit strings are the ones a reader would most expect it to touch -- an earlier draft of
the disposition wanted to rewrite them, and that draft was wrong. So they are pinned BYTE-IDENTICAL
by path, and every other lemon string is pinned wholesale.
"""
import copy
import hashlib
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The mutation harness points this at a sabotaged copy to prove these guards are not vacuous.
CANONICAL = os.environ.get('PLA114_CANONICAL', os.path.join(REPO, 'crops_data_final.json'))

BASE_SHA = '6b2dcb8ed4f51c833fa4d44845b15e7f609079a24a544af025c067dfca45d4db'

CLEMSON_COLD = 'https://hgic.clemson.edu/cold-tolerance-in-citrus/'
TAMU_CITRUS = 'https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/'
IPM_FREEZE = 'https://ipm.ucanr.edu/home-and-landscape/freezing-and-frost-damage-to-citrus/'
UC8100_URL = 'https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf'

# The fourteen strings that assert the high-20s threshold for leaves AND fruit. ENUMERATED by
# path, because the claim "this promote moved no prose" is only checkable if the paths are named.
CONFLATION_PATHS = [
    ('crop', 'hardiness_notes_seasoned'),
    ('fd', 2, 'what_happened_seasoned'),
    ('fd', 2, 'what_happened_beginner'),
    ('region', 'northern_tier', 'cold_basis_seasoned'),
    ('zone', 'northern_tier', '3', 'frost_risk_note_seasoned'),
    ('zone', 'northern_tier', '4', 'frost_risk_note_seasoned'),
    ('zone', 'northern_tier', '5', 'frost_risk_note_seasoned'),
    ('zone', 'northern_tier', '6', 'frost_risk_note_seasoned'),
    ('zone', 'northern_tier', '7', 'frost_risk_note_seasoned'),
    ('zone', 'se_gulf', '9', 'frost_risk_note_seasoned'),
    ('zone', 'se_gulf', '10', 'frost_risk_note_seasoned'),
    ('region', 'rgv', 'cold_basis_seasoned'),
    ('region', 'pnw', 'cold_basis_seasoned'),
    ('zone', 'pnw', '8', 'suitability_note_seasoned'),
]

FINDING_IDS = {
    'lemon_cold_threshold_was_miscredited_now_uc8100': 'resolved',
    'lemon_ca_interior_uc_ipm_repointed_to_freeze_page': 'resolved',
    'lemon_warm_arid_plantings_no_citrus_document': 'open',
    'lemon_tamu_table_1_not_in_text_layer': 'open',
    'lemon_cold_threshold_single_source_divergence': 'resolved',
}


def _crop(data, slug='lemon'):
    return next(c for c in data['crops'] if c['slug'] == slug)


def _resolve(crop, path):
    kind = path[0]
    if kind == 'crop':
        return crop[path[1]]
    if kind == 'fd':
        return crop['failure_diagnostics'][path[1]][path[2]]
    if kind == 'region':
        return crop['regions'][path[1]][path[2]]
    if kind == 'zone':
        return crop['regions'][path[1]]['resolved_by_zone'][path[2]][path[3]]
    raise AssertionError(f'unknown path kind {kind!r}')


def _url(crop, region, zone, sid):
    cell = crop['regions'][region]['resolved_by_zone'][zone]
    return cell['anchoring_urls'][sid]['url']


# This suite validates the state THIS promote produced, `29b96b65` -- not whatever canonical
# happens to be later. Pinned 2026-08-06 when the §7 promote legitimately added seven catalog ids,
# three findings and four citations on top of it, which broke the "nothing else moved" guards.
# Re-baselining those each time a later promote lands would hollow them out; the mutation harness
# still overrides via PLA114_CANONICAL, so the guards stay falsifiable.
POST_SHA = '29b96b65a0969a8ad654762b5d84276bafbd2a8747706cb512ed1414305abf6f'


@pytest.fixture(scope='module')
def post():
    override = os.environ.get('PLA114_CANONICAL')
    if override:
        with open(override, 'rb') as fh:
            return json.loads(fh.read())
    return json.loads(promote_fixture.pre_state(POST_SHA))


@pytest.fixture(scope='module')
def pre():
    return json.loads(promote_fixture.pre_state(BASE_SHA))


# --- the value ---------------------------------------------------------------------------------

def test_frost_tolerance_is_29(post):
    """UC 8100: 29F/30min is the damage ONSET for tender citrus, and Table 1 rates lemon H."""
    assert _crop(post)['frost_tolerance_f'] == 29


def test_frost_effect_is_unchanged(pre, post):
    """The field means 'the temperature at which frost_effect occurs' -- the effect must not move."""
    assert _crop(post)['frost_effect'] == _crop(pre)['frost_effect'] == 'foliage_damaged'


def test_the_value_actually_moved(pre, post):
    """Non-vacuity: the pre-state must differ, or test_frost_tolerance_is_29 proves nothing."""
    assert _crop(pre)['frost_tolerance_f'] == 28
    assert _crop(post)['frost_tolerance_f'] != _crop(pre)['frost_tolerance_f']


def test_sibling_citrus_values_are_untouched(pre, post):
    """[[never-blanket-a-reason-across-crops]] -- grapefruit/orange/mandarin are a SEPARATE pass."""
    for slug in ('lime', 'grapefruit', 'orange-navel', 'mandarin-clementine'):
        assert _crop(post, slug)['frost_tolerance_f'] == _crop(pre, slug)['frost_tolerance_f']


def test_the_sibling_ordering_is_now_correct(post):
    """lime > lemon > grapefruit, matching 8100 Table 1 (lemon H, grapefruit M) and LSU's ranking."""
    lime = _crop(post, 'lime')['frost_tolerance_f']
    lemon = _crop(post)['frost_tolerance_f']
    grapefruit = _crop(post, 'grapefruit')['frost_tolerance_f']
    assert lime > lemon > grapefruit, (lime, lemon, grapefruit)


# --- the new catalog id ------------------------------------------------------------------------

def test_uc_anr_8100_is_minted(post):
    entry = post['source_catalog']['uc_anr_8100']
    assert entry['url'] == UC8100_URL
    assert entry['tier'] == 'T1'


def test_uc_anr_8100_records_the_user_agent_gate(post):
    """A plain fetch returns HTTP 202 + zero bytes. Unrecorded, a later session calls it dead.

    Assert the DISTINCTIVE tokens. A first cut checked `'202' in blob`, which a mutation could not
    falsify because the accessed date "2026-08" contains "202" -- the guard was green on the year.
    """
    entry = post['source_catalog']['uc_anr_8100']
    assert 'HTTP 202' in entry['citable_for']
    assert 'USER-AGENT GATED' in entry['citable_for']
    assert 'ZERO bytes' in entry['citable_for']


def test_uc_anr_8100_is_in_lemons_source_set(post):
    assert 'uc_anr_8100' in _crop(post)['verification_status']['source_set']


def test_no_other_catalog_id_was_added_or_removed(pre, post):
    assert set(post['source_catalog']) - set(pre['source_catalog']) == {'uc_anr_8100'}
    assert set(pre['source_catalog']) - set(post['source_catalog']) == set()


# --- the repoints ------------------------------------------------------------------------------

@pytest.mark.parametrize('zone', ['3', '4', '5', '6', '7'])
def test_northern_tier_repointed_to_both_documents(post, zone):
    assert _url(_crop(post), 'northern_tier', zone, 'clemson_hgic') == CLEMSON_COLD
    assert _url(_crop(post), 'northern_tier', zone, 'tamu_agrilife') == TAMU_CITRUS


def test_se_gulf_z8_tamu_repointed(post):
    assert _url(_crop(post), 'se_gulf', '8', 'tamu_agrilife') == TAMU_CITRUS


def test_se_gulf_z8_clemson_STAYS_BARE(pre, post):
    """Hunt #28 is OPEN and must not be swept along. Over-repointing is the failure mode here."""
    assert _url(_crop(post), 'se_gulf', '8', 'clemson_hgic') == 'https://hgic.clemson.edu'
    assert _url(_crop(post), 'se_gulf', '8', 'clemson_hgic') == \
        _url(_crop(pre), 'se_gulf', '8', 'clemson_hgic')


def test_warm_arid_z8_repointed_to_both(post):
    assert _url(_crop(post), 'warm_arid', '8', 'tamu_agrilife') == TAMU_CITRUS
    assert _url(_crop(post), 'warm_arid', '8', 'clemson_hgic') == CLEMSON_COLD


def test_warm_arid_plantings_STAY_BARE(pre, post):
    """F3's two uncovered nodes have NO sibling document -- #31 covered 1 of 3 nodes, not 3."""
    for crop in (pre, post):
        planting = _crop(crop)['regions']['warm_arid']['plantings'][0]
        assert planting['anchoring_urls']['clemson_hgic']['url'] == 'https://hgic.clemson.edu'


@pytest.mark.parametrize('zone', ['8', '9'])
def test_ca_interior_uc_ipm_repointed_to_freeze_page(post, zone):
    assert _url(_crop(post), 'ca_interior', zone, 'uc_ipm') == IPM_FREEZE


@pytest.mark.parametrize('zone', ['8', '9'])
def test_ca_interior_ucanr_ext_STAYS_BARE(pre, post, zone):
    """Hunt #3 is OPEN -- the cell is SPLIT and only the uc_ipm arm has a document."""
    assert _url(_crop(post), 'ca_interior', zone, 'ucanr_ext') == 'https://ucanr.edu'
    assert _url(_crop(post), 'ca_interior', zone, 'ucanr_ext') == \
        _url(_crop(pre), 'ca_interior', zone, 'ucanr_ext')


def test_exactly_the_intended_urls_moved(pre, post):
    """COVERAGE, not overlap: enumerate every (region, zone, sid) whose url changed."""
    moved = set()
    for region, rdata in _crop(post)['regions'].items():
        for zone, cell in (rdata.get('resolved_by_zone') or {}).items():
            for sid, entry in (cell.get('anchoring_urls') or {}).items():
                before = _crop(pre)['regions'][region]['resolved_by_zone'][zone][
                    'anchoring_urls'][sid]['url']
                if entry['url'] != before:
                    moved.add((region, zone, sid))
    expected = {('northern_tier', z, s) for z in '34567'
                for s in ('clemson_hgic', 'tamu_agrilife')}
    expected |= {('se_gulf', '8', 'tamu_agrilife'), ('warm_arid', '8', 'tamu_agrilife'),
                 ('warm_arid', '8', 'clemson_hgic'),
                 ('ca_interior', '8', 'uc_ipm'), ('ca_interior', '9', 'uc_ipm')}
    assert moved == expected


# --- the findings ------------------------------------------------------------------------------

def test_all_five_findings_filed(post):
    filed = {f['id']: f for f in _crop(post)['verification_status']['open_findings']}
    for fid, status in FINDING_IDS.items():
        assert fid in filed, f'{fid} not filed'
        assert filed[fid]['status'] == status, f'{fid} status {filed[fid]["status"]!r}'


def test_the_pre_existing_findings_survive(pre, post):
    """Append-only: filing five must not drop the four already there."""
    before = {f['id'] for f in _crop(pre)['verification_status']['open_findings']}
    after = {f['id'] for f in _crop(post)['verification_status']['open_findings']}
    assert before <= after
    assert after - before == set(FINDING_IDS)


def test_f1_records_the_miscredit_as_two_of_three(post):
    """UF/IFAS IS correctly credited -- HS402 publishes lemon figures. Only Clemson and TAMU are not."""
    filed = {f['id']: f for f in _crop(post)['verification_status']['open_findings']}
    blob = json.dumps(filed['lemon_cold_threshold_was_miscredited_now_uc8100'], ensure_ascii=False)
    assert 'HS402' in blob
    assert 'uf_ifas_hs1153' in blob or 'UF/IFAS' in blob


def test_f5_states_scope_and_the_duration_qualifier(post):
    """Why 29 beats 26 is SCOPE (8100 discriminates by class, LSU lumps), not '29 > 26'."""
    filed = {f['id']: f for f in _crop(post)['verification_status']['open_findings']}
    blob = json.dumps(filed['lemon_cold_threshold_single_source_divergence'], ensure_ascii=False)
    assert '30 minutes' in blob, 'the duration qualifier makes a colder figure non-contradictory'
    # The LSU scope must be stated as a CATEGORY that lumps sensitivity classes -- not merely by
    # mentioning satsuma, which F5 also does when listing Clemson's figures. A first cut checked
    # for the bare words and was green on the wrong sentence.
    assert 'all other citrus' in blob, 'LSU category scope'
    assert 'category-level' in blob, 'why 29 wins is SCOPE, not that 29 > 26'
    assert 'sensitivity class' in blob, '8100 discriminates where LSU lumps'
    assert 'DEFOLIATION at 22-24F' in blob, 'HS402 endpoint recorded as an endpoint'
    assert 'ENDPOINTS, never competing onsets' in blob, 'onset vs endpoint must be explicit'


# --- the tripwire: NO prose moved ---------------------------------------------------------------

@pytest.mark.parametrize('path', CONFLATION_PATHS, ids=lambda p: '.'.join(map(str, p)))
def test_the_fourteen_conflation_strings_are_byte_identical(pre, post, path):
    """The disposition ruled NO edit is owed to these. Pinned so a later pass cannot drift them.

    NARROWED 2026-08-06 for `hardiness_notes_seasoned` ONLY, by the Task 2 credit-line promote.
    That promote rewrote the source parenthetical appended to this string -- the mis-credit F1
    exists to record -- and touched nothing else. The pin's purpose, stated when it was written,
    is "so a later pass cannot 'fix' correct copy", and the correct copy is the stage-aware CLAIM,
    not the credit. So the CLAIM text is still pinned byte-identical here; the credit is asserted
    separately, per claim, in test_promote_pla114_credit_line.py. Dropping the check for this
    field outright would have handed the next pass exactly the licence the pin denies.
    """
    before, after = _resolve(_crop(pre), path), _resolve(_crop(post), path)
    if path == ('crop', 'hardiness_notes_seasoned'):
        before, after = before.split(' (Sources:')[0], after.split(' (Sources:')[0]
        assert before, 'the split found no claim text -- the field shape changed'
    assert after == before


def test_the_fourteen_paths_all_resolve_and_asserted_the_threshold(pre):
    """Non-vacuity: a typo'd path would make the tripwire above pass by comparing None to None."""
    for path in CONFLATION_PATHS:
        value = _resolve(_crop(pre), path)
        assert isinstance(value, str) and 'high' in value.lower(), path


def test_no_lemon_string_moved_at_all(pre, post):
    """Wholesale: every string on lemon, not just the fourteen. Only non-string fields may move.

    The Task 2 credit-line promote later rewrote ONE credit parenthetical, so that single string is
    compared on its claim text here and per claim in test_promote_pla114_credit_line.py. Every
    other string on the crop is still compared whole, which is what makes this a coverage check
    rather than a spot check.
    """
    def strings(node, out, trail=''):
        if isinstance(node, dict):
            for k, v in node.items():
                strings(v, out, f'{trail}.{k}')
        elif isinstance(node, list):
            for i, v in enumerate(node):
                strings(v, out, f'{trail}[{i}]')
        elif isinstance(node, str):
            out[trail] = node

    before, after = {}, {}
    pre_crop, post_crop = copy.deepcopy(_crop(pre)), copy.deepcopy(_crop(post))
    # the promote intentionally adds citations and findings; exclude only those subtrees
    for crop in (pre_crop, post_crop):
        crop['verification_status'] = {k: v for k, v in crop['verification_status'].items()
                                       if k not in ('open_findings', 'source_set')}
        for rdata in crop['regions'].values():
            for cell in (rdata.get('resolved_by_zone') or {}).values():
                cell.pop('anchoring_urls', None)
    strings(pre_crop, before)
    strings(post_crop, after)
    key = '.hardiness_notes_seasoned'
    for bag in (before, after):
        bag[key] = bag[key].split(' (Sources:')[0]
    assert before[key], 'the split found no claim text -- the field shape changed'
    assert before == after


def test_no_other_crop_changed(pre, post):
    """127 of 128 crops must be byte-identical."""
    pre_by = {c['slug']: c for c in pre['crops']}
    post_by = {c['slug']: c for c in post['crops']}
    assert set(pre_by) == set(post_by)
    changed = [s for s in pre_by
               if json.dumps(pre_by[s], ensure_ascii=False, sort_keys=True)
               != json.dumps(post_by[s], ensure_ascii=False, sort_keys=True)]
    assert changed == ['lemon'], changed


def test_canonical_is_still_compact():
    raw = promote_fixture.pre_state(POST_SHA)
    assert b'\n' not in raw, 'canonical must be single-line compact'
    assert not raw.endswith(b'\n'), 'canonical must have no trailing newline'


def test_the_promote_actually_changed_canonical():
    """If the post state hashes to the base, every check above compares a file to itself."""
    got = hashlib.sha256(promote_fixture.pre_state(POST_SHA)).hexdigest()
    assert got != BASE_SHA, 'the post state is the pre-state -- the promote did not run'


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
