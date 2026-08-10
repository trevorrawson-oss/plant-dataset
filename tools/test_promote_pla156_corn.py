#!/usr/bin/env python3
"""Guards for the PLA-156 corn dispositions. Base 72284f02. RED before GREEN.

The load-bearing guards are the RETENTION ones: uga_b577 must SURVIVE on every sow arm, plantings
anchor and zone cell of all three grain corns (re-scope, not drop), and sweet-corn must be
byte-identical (B577 supports it to the day). A suite that only checked the removals would pass
on a promote that stripped B577 everywhere -- which is exactly what the corrupt ledger almost
commissioned and what PLA-156 exists to prevent.

Run: python3 tools/test_promote_pla156_corn.py   (or pytest)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_SHA = '72284f0291442919d005a8546f6cfbdcdf06502fe7842327fa77201e5c9c8571'
# Pinned to the state THIS promote produced (registered in COMMIT_FOR as 8d00f8a), so the suite
# keeps protecting after canonical moves on. None = read live canonical (pre-pin bootstrap only).
POST_SHA = 'db853c4b20e889a93d8946e947b31a2c7a00f49042e8774a04dc7386bca9e7a5'

UMN_URL = 'https://extension.umn.edu/vegetables/growing-popcorn'
ISU_URL = 'https://yardandgarden.extension.iastate.edu/how-to/growing-and-harvesting-popcorn-home-garden'
B577_URL = 'https://secure.caes.uga.edu/extension/publications/files/html/B577/B577PlantingChart.pdf'
GRAIN = ('field-corn', 'popcorn', 'flint-corn')
TOUCHED = set(GRAIN)
NEW_FINDING_IDS = {
    'popcorn': 'pla156_popcorn_dtm_widened_to_published_range',
    'field-corn': 'pla156_field_corn_harvest_dtm_modeled',
    'flint-corn': 'pla156_flint_corn_harvest_dtm_modeled',
}

_pre_raw = promote_fixture.pre_state(BASE_SHA)
_override = os.environ.get('PLA156_CANONICAL')
if _override:
    _post_raw = open(_override, 'rb').read()
elif POST_SHA:
    _post_raw = promote_fixture.pre_state(POST_SHA)
else:
    _post_raw = open(os.path.join(REPO, 'crops_data_final.json'), 'rb').read()
PRE = json.loads(_pre_raw)
POST = json.loads(_post_raw)


def crop(d, slug):
    return next(c for c in d['crops'] if c['slug'] == slug)


def arms(d, slug):
    pl = crop(d, slug)['regions']['se_gulf']['plantings'][0]
    return pl['harvest_start'][0], pl['harvest_end'][0]


def b577_live_nodes(c):
    """Count live-layer anchoring entries citing the B577 url (zones{} excluded)."""
    hits = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                p = f'{path}.{k}' if path else k
                if k == 'anchoring_urls' and isinstance(v, dict) and 'zones' not in p.split('.'):
                    for src, rec in v.items():
                        if isinstance(rec, dict) and rec.get('url') == B577_URL:
                            hits.append(p)
                walk(v, p)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f'{path}[{i}]')

    walk(c, '')
    return hits


# G1. roster identical PRE vs POST -- no crop appears or vanishes (blast-radius, both directions)
assert {c['slug'] for c in PRE['crops']} == {c['slug'] for c in POST['crops']}, 'roster moved'

# G2. every crop OUTSIDE the three grain corns is byte-identical, sweet-corn EXPLICITLY among them
for pre_c, post_c in zip(PRE['crops'], POST['crops']):
    assert pre_c['slug'] == post_c['slug'], 'crop order moved'
    if pre_c['slug'] not in TOUCHED:
        assert pre_c == post_c, f"{pre_c['slug']} moved but is outside the promote's footprint"
assert crop(PRE, 'sweet-corn') == crop(POST, 'sweet-corn'), 'sweet-corn moved'

# G3. PRE pins: all six grain-corn harvest arms were sole-uga_b577 before the promote
for slug in GRAIN:
    for arm in arms(PRE, slug):
        assert arm['sources'] == ['uga_b577'], f'{slug} pre-state not sole-b577'

# G4. popcorn harvest_start prose: the ONE consumer string this promote moves. Hand-written
# expected values, not computed from the promote script (computed-guard-expectations lesson).
hs_pre, he_pre = arms(PRE, 'popcorn')
hs_post, he_post = arms(POST, 'popcorn')
assert 'about 100 to 110 days after sowing' in hs_pre['synthesis_note_seasoned']
assert 'about 90 to 120 days after sowing' in hs_post['synthesis_note_seasoned'], \
    'popcorn DTM prose not widened to the published range'
assert 'about 100 to 110' not in hs_post['synthesis_note_seasoned'], 'old narrowing survives'
assert 'about 13 to 14 percent moisture' in hs_post['synthesis_note_seasoned'], \
    'the sourced moisture claim must survive the widen'
assert he_post['synthesis_note_seasoned'] == he_pre['synthesis_note_seasoned'], \
    'popcorn harvest_end prose must not move'

# G5. popcorn harvest arms cite EXACTLY the two documents that publish the numbers
for arm in (hs_post, he_post):
    assert arm['sources'] == ['umn_ext', 'iastate_ext'], f"popcorn sources: {arm['sources']}"
    assert arm['anchoring_urls'] == {
        'umn_ext': {'url': UMN_URL, 'verified': '2026-08-10'},
        'iastate_ext': {'url': ISU_URL, 'verified': '2026-08-10'},
    }, 'popcorn anchors are not the two pinned documents'

# G6. field/flint harvest arms are honestly uncited: no sources, no anchors, and NOT repointed
# at B577's contradicting Corn row (the do-not-do this suite pins for future sessions)
for slug in ('field-corn', 'flint-corn'):
    for arm in arms(POST, slug):
        assert arm['sources'] == [], f'{slug} harvest arm still carries a credit'
        assert arm['anchoring_urls'] == {}, f'{slug} harvest arm still carries an anchor'

# G7. field/flint harvest PROSE is byte-identical -- the values stand, only the credit moves
for slug in ('field-corn', 'flint-corn'):
    for a_pre, a_post in zip(arms(PRE, slug), arms(POST, slug)):
        assert a_pre['synthesis_note_seasoned'] == a_post['synthesis_note_seasoned'], \
            f'{slug} harvest prose moved in a citation-scope promote'

# G8. RE-SCOPE, NOT DROP: each grain corn keeps B577 on exactly 5 live-layer nodes
# (direct_sow arm, plantings-level anchor, zone cells 8/9/10) -- 7 pre minus the 2 harvest arms.
# Sweet-corn keeps all 11. Hand-counted constants from the pre-promote gate output.
for slug in GRAIN:
    pre_n, post_n = len(b577_live_nodes(crop(PRE, slug))), len(b577_live_nodes(crop(POST, slug)))
    assert pre_n == 7, f'{slug} pre b577 nodes {pre_n} != 7 (pin from 2026-08-10 gate output)'
    assert post_n == 5, f'{slug} post b577 nodes {post_n} != 5 -- re-scope must keep the sow layer'
assert len(b577_live_nodes(crop(POST, 'sweet-corn'))) == 11, 'sweet-corn b577 nodes moved'

# G9. each grain corn's direct_sow arm still cites b577 BY NAME (the retention that matters most)
for slug in GRAIN:
    ds = crop(POST, slug)['regions']['se_gulf']['plantings'][0]['direct_sow'][0]
    assert 'uga_b577' in ds['sources'], f'{slug} direct_sow lost its supported citation'
    assert ds['anchoring_urls']['uga_b577']['url'] == B577_URL

# G10. the three findings exist, carry the pinned ids, and the two modeled ones pin the
# do-not-repoint warning naming B577's contradicting figure
for slug, fid in NEW_FINDING_IDS.items():
    of = crop(POST, slug)['verification_status']['open_findings']
    assert [f['id'] for f in of] == [fid], f'{slug} findings: {[f["id"] for f in of]}'
    f = of[0]
    assert f['blocks_launch'] is False and f['status'] == 'accepted'
for slug in ('field-corn', 'flint-corn'):
    f = crop(POST, slug)['verification_status']['open_findings'][0]
    assert 'DO NOT repoint' in f['summary'] and '80-100' in f['summary'], \
        f'{slug} finding lacks the do-not-repoint pin'

# G11. provenance AMENDED BY APPEND: the original text survives byte-for-byte as a prefix
for slug in GRAIN:
    prov_pre = crop(PRE, slug)['regions']['se_gulf']['plantings_provenance']
    prov_post = crop(POST, slug)['regions']['se_gulf']['plantings_provenance']
    assert prov_post.startswith(prov_pre), f'{slug} provenance was rewritten, not appended'
    assert '[PLA-156 2026-08-10:' in prov_post, f'{slug} provenance lacks the dated append'
    assert 'Mar 15 - Apr 30' in prov_post and 'Mar 15 - Jun 1' in prov_post, \
        f'{slug} provenance does not record the narrowing (disposition 5)'

# G12. COMPACT preserved and the consumer-copy rules hold in the one new consumer string
assert b'\n' not in _post_raw, 'canonical is not compact'
assert '—' not in hs_post['synthesis_note_seasoned'], 'em dash in consumer copy'

print('test_promote_pla156_corn: OK (12 guard groups)')
