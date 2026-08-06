#!/usr/bin/env python3
"""Guards for PLA-114 §7 (the six), as scoped. Base bce8bcc7. RED before GREEN.

The load-bearing guards here are the NEGATIVE ones. This promote's substance is as much what it
refuses to write as what it writes: the three held-back harvest arms must stay bare, bloom must
stay modeled everywhere, and UC IPM must not end up cited on a bloom arm. A suite that only
checked the additions would pass on a promote that quietly did the wrong thing.
"""
import hashlib
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.environ.get('PLA114C_CANONICAL', os.path.join(REPO, 'crops_data_final.json'))
BASE_SHA = 'bce8bcc72aeebb42269b2d96310b427d9502a3670241ca7621e91810588f16cd'

NEW_IDS = ['ucce_riverside_citrus_qa', 'uc_mg_marin_citrus', 'ucce_kern_kc9382',
           'uc_ipm_citrus_timings', 'ucce_placer_nevada_31_018c', 'uc_mg_sacramento_gn127',
           'uc_mg_santa_clara_citrus']
HELD_BACK = [('low_desert_az', 'uariz_ext', 'https://extension.arizona.edu'),
             ('ca_desert', 'uariz_ext', 'https://extension.arizona.edu'),
             ('ca_south_coast', 'ucanr_ext', 'https://ucanr.edu')]
NEW_FINDINGS = ['lemon_ca_interior_harvest_modeled_no_uc_window',
                'lemon_bloom_modeled_every_region',
                'lemon_harvest_arms_uncitable_as_structured_and_may_render_too_narrow']


def _crop(d, slug='lemon'):
    return next(c for c in d['crops'] if c['slug'] == slug)


def _arm(d, region, arm):
    return _crop(d)['regions'][region]['plantings'][0][arm][0]


@pytest.fixture(scope='module')
def post():
    return json.loads(open(CANONICAL, 'rb').read())


@pytest.fixture(scope='module')
def pre():
    return json.loads(promote_fixture.pre_state(BASE_SHA))


# --- the mints ---------------------------------------------------------------------------------

@pytest.mark.parametrize('cid', NEW_IDS)
def test_id_is_minted(post, cid):
    e = post['source_catalog'][cid]
    assert e['tier'] == 'T1' and e['url'].startswith('https://')


def test_exactly_the_seven_were_minted(pre, post):
    assert sorted(set(post['source_catalog']) - set(pre['source_catalog'])) == sorted(NEW_IDS)
    assert set(pre['source_catalog']) - set(post['source_catalog']) == set()


def test_lazaneo_admitted_under_the_existing_san_diego_id(pre, post):
    """No new id: mastergardenersd.org is already `ucanr_san_diego_mg`'s host."""
    before = pre['source_catalog']['ucanr_san_diego_mg']['citable_for']
    after = post['source_catalog']['ucanr_san_diego_mg']['citable_for']
    assert after.startswith(before), 'the existing entry was rewritten rather than appended to'
    assert 'Lazaneo' in after and 'citrus-for-the-home-garden.pdf' in after
    assert 'lazaneo' not in {k.lower() for k in post['source_catalog']}


def test_lazaneo_is_barred_from_the_hardiness_ranking(post):
    """It puts grapefruit more tender than true lemon -- an outlier 6 to 1."""
    after = post['source_catalog']['ucanr_san_diego_mg']['citable_for']
    assert 'DO NOT CITE IT FOR THE COLD-HARDINESS RANKING' in after
    assert 'outlier 6 to 1' in after


def test_uc_ipm_timings_is_barred_from_being_lemons_bloom(post):
    """The whole point of the bloom ruling. If this text goes, the guard goes with it."""
    e = post['source_catalog']['uc_ipm_citrus_timings']['citable_for']
    assert 'NEVER FOR LEMON' in e.upper()
    assert 'Central Valley' in e
    assert 'first half' in e.lower(), 'the re-derived Mar-to-mid-Apr edge must be recorded'


def test_31_018c_records_the_shared_lineage(post):
    e = post['source_catalog']['ucce_placer_nevada_31_018c']['citable_for']
    assert 'NOT INDEPENDENT' in e and '134971' in e


# --- plant_out repoints ------------------------------------------------------------------------

@pytest.mark.parametrize('region,sid', [('ca_interior', 'ucce_kern_kc9382'),
                                        ('ca_north_coast', 'uc_mg_marin_citrus'),
                                        ('ca_south_coast', 'ucanr_san_diego_mg'),
                                        ('ca_south_coast', 'ucce_riverside_citrus_qa'),
                                        ('ca_desert', 'ucce_riverside_citrus_qa')])
def test_plant_out_now_cites_a_pathed_document(post, region, sid):
    arm = _arm(post, region, 'plant_out')
    assert sid in arm['sources']
    url = arm['anchoring_urls'][sid]['url']
    assert url.count('/') > 3, f'{url} is not pathed'


def test_low_desert_az_plant_out_STAYS_BARE(pre, post):
    """AZ1001 publishes no planting date -- hunt #14's plant_out is still OPEN."""
    a, b = _arm(pre, 'low_desert_az', 'plant_out'), _arm(post, 'low_desert_az', 'plant_out')
    assert b['sources'] == a['sources']
    assert b['anchoring_urls'] == a['anchoring_urls']


# --- what the promote REFUSES to do ------------------------------------------------------------

@pytest.mark.parametrize('region,sid,url', HELD_BACK)
def test_held_back_harvest_arms_stay_bare(post, region, sid, url):
    for arm in ('harvest_start', 'harvest_end'):
        e = _arm(post, region, arm)
        assert e['anchoring_urls'][sid]['url'] == url, f'{region}/{arm}/{sid} was repointed'


def test_no_harvest_arm_anywhere_gained_a_citation(pre, post):
    """COVERAGE, not a spot check: no harvest arm on any region may have changed."""
    for region in _crop(post)['regions']:
        for arm in ('harvest_start', 'harvest_end'):
            a = (_crop(pre)['regions'][region]['plantings'][0].get(arm) or [])
            b = (_crop(post)['regions'][region]['plantings'][0].get(arm) or [])
            assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), region


def test_no_bloom_arm_anywhere_changed(pre, post):
    """Bloom stays MODELED everywhere, so no bloom arm may gain a source."""
    for region in _crop(post)['regions']:
        a = (_crop(pre)['regions'][region]['plantings'][0].get('bloom') or [])
        b = (_crop(post)['regions'][region]['plantings'][0].get('bloom') or [])
        assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), region


def test_uc_ipm_timings_is_cited_by_NO_cell(post):
    """It is admitted to the catalog as evidence for a finding, never onto a cell."""
    blob = json.dumps(_crop(post)['regions'], ensure_ascii=False)
    assert 'uc_ipm_citrus_timings' not in blob
    assert 'timings-for-key-cultural' not in blob


def test_the_held_back_finding_states_the_user_facing_consequence(post):
    filed = {f['id']: f for f in _crop(post)['verification_status']['open_findings']}
    s = filed['lemon_harvest_arms_uncitable_as_structured_and_may_render_too_narrow']['summary']
    assert 'about 60 days' in s
    assert 'August through February' in s, 'the AZ1001 reading, not the half-month version'
    assert 'Feb 15' not in s, "the work order's bar-edge misread must not survive"
    # the source-truth sample refuted the alarming version; the record must say so rather than
    # quietly drop it, and must not re-assert it
    assert 'TWO' in s and 'reader-facing harvest surfaces' in s
    assert 'scattered year-round' in s, 'the mitigating string must be quoted, not omitted'
    assert 'SOURCE-TRUTH SAMPLE REFUTED THAT' in s
    assert s.count('five months too short') == 1, 'named only as the refuted earlier draft'


# --- findings ----------------------------------------------------------------------------------

def test_ca_interior_modeled_declaration_cross_references_pla151(post):
    """"Modeled" is a PROVENANCE statement, not a correctness claim.

    ca_interior's span is 95 days, inside the suspect group. An unqualified declaration would read
    as modeled-and-therefore-fine, so the cell must say it may be BOTH unsourced and too narrow.
    """
    filed = {f['id']: f for f in _crop(post)['verification_status']['open_findings']}
    s = filed['lemon_ca_interior_harvest_modeled_no_uc_window']['summary']
    assert 'PLA-151' in s, 'the archetype finding must be cross-referenced'
    assert 'PROVENANCE statement' in s and 'NOT a statement' in s
    assert '95 days' in s
    assert 'UNSOURCED and TOO NARROW' in s


@pytest.mark.parametrize('fid', NEW_FINDINGS)
def test_finding_filed(post, fid):
    filed = {f['id']: f for f in _crop(post)['verification_status']['open_findings']}
    assert fid in filed and filed[fid]['status'] == 'open'


def test_f5_amended_by_append_not_rewrite(pre, post):
    def f5(d):
        return next(f for f in _crop(d)['verification_status']['open_findings']
                    if f['id'] == 'lemon_cold_threshold_single_source_divergence')['summary']
    assert f5(post).startswith(f5(pre))
    tail = f5(post)[len(f5(pre)):]
    assert 'seventh' in tail.lower()
    assert 'TWO institutions publish 26F' in tail
    assert 'Sacramento' in tail
    assert 'NOT INDEPENDENT' in tail


def test_earlier_findings_survive(pre, post):
    before = {f['id'] for f in _crop(pre)['verification_status']['open_findings']}
    after = {f['id'] for f in _crop(post)['verification_status']['open_findings']}
    assert before <= after
    assert after - before == set(NEW_FINDINGS)


# --- blast radius ------------------------------------------------------------------------------

def test_no_other_crop_changed(pre, post):
    pre_by = {c['slug']: c for c in pre['crops']}
    post_by = {c['slug']: c for c in post['crops']}
    changed = [s for s in pre_by
               if json.dumps(pre_by[s], ensure_ascii=False, sort_keys=True)
               != json.dumps(post_by[s], ensure_ascii=False, sort_keys=True)]
    assert changed == ['lemon'], changed


def test_no_consumer_prose_moved(pre, post):
    """This promote is citations and findings only. Every consumer string must be identical."""
    def strings(node, out, trail=''):
        if isinstance(node, dict):
            for k, v in node.items():
                # `open_findings` and `source_set` are the structured records this promote is
                # SUPPOSED to add to; `anchoring_urls` holds the citations it repoints. Everything
                # else a reader could see must be byte-identical.
                if k in ('open_findings', 'source_set', 'anchoring_urls'):
                    continue
                strings(v, out, f'{trail}.{k}')
        elif isinstance(node, list):
            for i, v in enumerate(node):
                strings(v, out, f'{trail}[{i}]')
        elif isinstance(node, str):
            out[trail] = node
    a, b = {}, {}
    strings(_crop(pre), a)
    strings(_crop(post), b)
    moved = {k for k in a if a.get(k) != b.get(k)}
    assert moved == set(), sorted(moved)


def test_frost_tolerance_still_29(post):
    assert _crop(post)['frost_tolerance_f'] == 29


def test_canonical_is_still_compact():
    raw = open(CANONICAL, 'rb').read()
    assert b'\n' not in raw and not raw.endswith(b'\n')


def test_the_promote_actually_ran():
    assert hashlib.sha256(open(CANONICAL, 'rb').read()).hexdigest() != BASE_SHA


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
