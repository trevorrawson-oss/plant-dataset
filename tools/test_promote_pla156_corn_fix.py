#!/usr/bin/env python3
"""Guards for the PLA-156 verification pass (the two held dispositions, corrected).
Base db853c4b. RED before GREEN.

The load-bearing assertion is the REVERT: popcorn's se_gulf harvest_start prose must be
byte-identical to what it was at 72284f02 -- the true original, fetched from the fixture, not a
constant computed from either promote script. And the corrected findings must still carry the
do-not-repoint-at-B577 pin, which survives every version of this story.

Run: python3 tools/test_promote_pla156_corn_fix.py   (or pytest)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG_SHA = '72284f0291442919d005a8546f6cfbdcdf06502fe7842327fa77201e5c9c8571'
BASE_SHA = 'db853c4b20e889a93d8946e947b31a2c7a00f49042e8774a04dc7386bca9e7a5'
POST_SHA = None  # pinned after the fix commit registers in COMMIT_FOR

CLEMSON_URL = 'https://hgic.clemson.edu/homegrown-grits/'
ISU_ORN_URL = 'https://yardandgarden.extension.iastate.edu/how-to/growing-and-harvesting-ornamental-corn'
UMN_URL = 'https://extension.umn.edu/vegetables/growing-popcorn'
ISU_POP_URL = 'https://yardandgarden.extension.iastate.edu/how-to/growing-and-harvesting-popcorn-home-garden'
B577_URL = 'https://secure.caes.uga.edu/extension/publications/files/html/B577/B577PlantingChart.pdf'
GRAIN = ('field-corn', 'popcorn', 'flint-corn')

ORIG = json.loads(promote_fixture.pre_state(ORIG_SHA))
PRE = json.loads(promote_fixture.pre_state(BASE_SHA))
_override = os.environ.get('PLA156F_CANONICAL')
if _override:
    _post_raw = open(_override, 'rb').read()
elif POST_SHA:
    _post_raw = promote_fixture.pre_state(POST_SHA)
else:
    _post_raw = open(os.path.join(REPO, 'crops_data_final.json'), 'rb').read()
POST = json.loads(_post_raw)


def crop(d, slug):
    return next(c for c in d['crops'] if c['slug'] == slug)


def arms(d, slug):
    pl = crop(d, slug)['regions']['se_gulf']['plantings'][0]
    return pl['harvest_start'][0], pl['harvest_end'][0]


def b577_live_nodes(c):
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


# G1. roster identical, and every crop outside the three is byte-identical to db853c4b
assert {c['slug'] for c in PRE['crops']} == {c['slug'] for c in POST['crops']}, 'roster moved'
for pre_c, post_c in zip(PRE['crops'], POST['crops']):
    assert pre_c['slug'] == post_c['slug'], 'crop order moved'
    if pre_c['slug'] not in set(GRAIN):
        assert pre_c == post_c, f"{pre_c['slug']} moved outside the fix's footprint"
assert crop(PRE, 'sweet-corn') == crop(POST, 'sweet-corn'), 'sweet-corn moved'

# G2. THE REVERT: popcorn's harvest_start prose is byte-identical to the TRUE ORIGINAL at
# 72284f02, and the widened text is gone
orig_hs = arms(ORIG, 'popcorn')[0]['synthesis_note_seasoned']
post_hs = arms(POST, 'popcorn')[0]['synthesis_note_seasoned']
assert 'about 100 to 110 days' in orig_hs, 'fixture sanity: original prose is the narrowing'
assert post_hs == orig_hs, 'popcorn prose is not byte-identical to the 72284f02 original'
assert 'about 90 to 120 days' in arms(PRE, 'popcorn')[0]['synthesis_note_seasoned'], \
    'fixture sanity: db853c4b carries the widened text'

# G3. the repoint SURVIVES the revert: popcorn arms still cite exactly UMN + Iowa State
for arm in arms(POST, 'popcorn'):
    assert arm['sources'] == ['umn_ext', 'iastate_ext'], f"popcorn sources: {arm['sources']}"
    assert arm['anchoring_urls'] == {
        'umn_ext': {'url': UMN_URL, 'verified': '2026-08-10'},
        'iastate_ext': {'url': ISU_POP_URL, 'verified': '2026-08-10'},
    }, 'popcorn anchors moved off the two pinned documents'

# G4. field-corn harvest arms cite exactly Clemson's Grits page; flint exactly ISU ornamental
for arm in arms(POST, 'field-corn'):
    assert arm['sources'] == ['clemson_hgic'], f"field-corn sources: {arm['sources']}"
    assert arm['anchoring_urls'] == {'clemson_hgic': {'url': CLEMSON_URL, 'verified': '2026-08-10'}}
for arm in arms(POST, 'flint-corn'):
    assert arm['sources'] == ['iastate_ext'], f"flint-corn sources: {arm['sources']}"
    assert arm['anchoring_urls'] == {'iastate_ext': {'url': ISU_ORN_URL, 'verified': '2026-08-10'}}

# G5. field/flint harvest PROSE still byte-identical to the ORIGINAL -- neither promote may
# move the values, only the credits
for slug in ('field-corn', 'flint-corn'):
    for a_orig, a_post in zip(arms(ORIG, slug), arms(POST, slug)):
        assert a_orig['synthesis_note_seasoned'] == a_post['synthesis_note_seasoned'], \
            f'{slug} harvest prose moved'

# G6. B577 still absent from all six harvest arms, and its retention footprint unmoved:
# 5 live-layer nodes per grain corn, 11 on sweet-corn
for slug in GRAIN:
    for arm in arms(POST, slug):
        assert 'uga_b577' not in arm['sources'] and 'uga_b577' not in arm['anchoring_urls'], \
            f'{slug} harvest arm regained the B577 credit'
    assert len(b577_live_nodes(crop(POST, slug))) == 5, f'{slug} b577 footprint moved'
assert len(b577_live_nodes(crop(POST, 'sweet-corn'))) == 11, 'sweet-corn b577 footprint moved'

# G7. findings corrected IN PLACE: same single id per crop, correction acknowledged, the
# cert-log basis named, and the do-not-repoint pin retained
FIDS = {'popcorn': 'pla156_popcorn_dtm_widened_to_published_range',
        'field-corn': 'pla156_field_corn_harvest_dtm_modeled',
        'flint-corn': 'pla156_flint_corn_harvest_dtm_modeled'}
for slug, fid in FIDS.items():
    of = crop(POST, slug)['verification_status']['open_findings']
    assert [f['id'] for f in of] == [fid], f'{slug} findings: {[f["id"] for f in of]}'
    s = of[0]['summary']
    assert s.startswith('[CORRECTED same day, 2026-08-10:'), f'{slug} finding not marked corrected'
    assert 'verification_log' in s and 'SYNTHESIS' in s, f'{slug} finding lacks the cert-log basis'
for slug in ('field-corn', 'flint-corn'):
    s = crop(POST, slug)['verification_status']['open_findings'][0]['summary']
    assert 'DO NOT repoint' in s and '80-100' in s, f'{slug} lost the do-not-repoint pin'

# G8. cert verification_log untouched on all three (append-only historical record)
for slug in GRAIN:
    assert crop(PRE, slug)['verification_status']['verification_log'] == \
        crop(POST, slug)['verification_status']['verification_log'], f'{slug} cert log moved'

# G9. provenance: the db853c4b text (original + first append) survives byte-for-byte as a
# prefix, with the verification append after it
for slug in GRAIN:
    prov_pre = crop(PRE, slug)['regions']['se_gulf']['plantings_provenance']
    prov_post = crop(POST, slug)['regions']['se_gulf']['plantings_provenance']
    assert prov_post.startswith(prov_pre), f'{slug} provenance history rewritten'
    assert '[PLA-156 verification 2026-08-10:' in prov_post[len(prov_pre):], \
        f'{slug} provenance lacks the verification append'

# G10. COMPACT preserved; no em dash in the restored consumer string
assert b'\n' not in _post_raw, 'canonical is not compact'
assert '—' not in post_hs, 'em dash in consumer copy'

print('test_promote_pla156_corn_fix: OK (10 guard groups)')
