#!/usr/bin/env python3
"""Guards for the PLA-157 promote (zinnia trigger register shift + the six titles).
Base ce9eb12f. RED before GREEN.

The load-bearing assertions are BYTE-IDENTITY ones: zinnia's rotated body prose must equal, byte
for byte, what sat one slot over at ce9eb12f (no re-authoring smuggled in), every crop outside
the two-crop footprint must be untouched, and both cert logs must be byte-identical (the fix owes
NO correction line per docs/verification_log_ref_convention.md -- so writing one would be a bug).

Every expected value here is RETYPED as a constant, never imported from the promote script or
computed from what it validates (the five-vacuous-guards-in-one-day lesson).

Run: python3 tools/test_promote_pla157_zinnia_triggers.py   (or pytest)
Override the post-state under test with PLA157_CANONICAL=<path> (scratch/mutation runs).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture  # noqa: E402
from trigger_prose_gate import identifier_prose_violations, title_length_violations  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Re-based 2026-08-10: PLA-155 promoted first (ce9eb12f -> 4f610318, disjoint footprint --
# zinnia/bee-balm/marigold byte-identical across the move, verified before re-pinning).
BASE_SHA = '4f6103183ac9c07475b3e0c2d3a71159d0662a10a61383e1d792c049957cac23'
# Pin to the state THIS promote produces once it lands + is registered in COMMIT_FOR.
# None = read live canonical (pre-pin bootstrap only).
POST_SHA = None

FOOTPRINT = {'zinnia', 'bee-balm'}
CLEMSON_URL = 'https://hgic.clemson.edu/factsheet/how-to-grow-zinnias-the-best-varieties-care-tips/'
UF_URL = 'https://gardeningsolutions.ifas.ufl.edu/plants/ornamentals/zinnia/'
UMN_URL = 'https://extension.umn.edu/flowers/zinnia'
UCIPM_URL = 'https://ipm.ucanr.edu/home-and-landscape/zinnia/'

ZINNIA_TITLES = ['Frost warning', 'Damp weather warning', 'Hot weather ahead']
BEEBALM_TITLES = ['Damp weather warning', 'Hot, dry weather', 'Frost and winter rest']
ZINNIA_STRAY = ['clemson_hgic_1149', 'clemson_hgic_1149', 'uf_ifas_zinnia']
ZINNIA_SOURCES = [['umn_ext', 'clemson_hgic_1149'],
                  ['uc_ipm', 'clemson_hgic_1149'],
                  ['clemson_hgic_1149', 'uf_ifas_zinnia']]
ZINNIA_ANCHORS = [
    {'umn_ext': {'url': UMN_URL, 'verified': '2026-06-15'},
     'clemson_hgic_1149': {'url': CLEMSON_URL, 'verified': '2026-08-10'}},
    {'uc_ipm': {'url': UCIPM_URL, 'verified': '2026-06-15'},
     'clemson_hgic_1149': {'url': CLEMSON_URL, 'verified': '2026-08-10'}},
    {'clemson_hgic_1149': {'url': CLEMSON_URL, 'verified': '2026-06-15'},
     'uf_ifas_zinnia': {'url': UF_URL, 'verified': '2026-08-10'}},
]
ZIN_FID = 'pla157_weather_trigger_register_shift'
BEE_FID = 'pla157_title_beginner_body_prose'

PRE = json.loads(promote_fixture.pre_state(BASE_SHA))
_override = os.environ.get('PLA157_CANONICAL')
if _override:
    _post_raw = open(_override, 'rb').read()
elif POST_SHA:
    _post_raw = promote_fixture.pre_state(POST_SHA)
else:
    _post_raw = open(os.path.join(REPO, 'crops_data_final.json'), 'rb').read()
POST = json.loads(_post_raw)


def crop(d, slug):
    return next(c for c in d['crops'] if c['slug'] == slug)


# G1. blast radius: same roster BOTH ways, same order, and every crop outside the two-crop
# footprint byte-identical (iterating PRE alone cannot see a ghost crop appended to POST --
# the set equality is the half that catches it)
assert {c['slug'] for c in PRE['crops']} == {c['slug'] for c in POST['crops']}, 'roster moved'
assert [c['slug'] for c in PRE['crops']] == [c['slug'] for c in POST['crops']], 'crop order moved'
for pre_c, post_c in zip(PRE['crops'], POST['crops']):
    if pre_c['slug'] not in FOOTPRINT:
        assert pre_c == post_c, f"{pre_c['slug']} moved outside the fix's footprint"
assert crop(PRE, 'zinnia') != crop(POST, 'zinnia'), 'zinnia unchanged: promote did not run'
assert crop(PRE, 'bee-balm') != crop(POST, 'bee-balm'), 'bee-balm unchanged: promote did not run'
assert PRE['source_catalog'] == POST['source_catalog'], 'source_catalog moved'

ZT_PRE = crop(PRE, 'zinnia')['weather_triggers']
ZT = crop(POST, 'zinnia')['weather_triggers']
BT_PRE = crop(PRE, 'bee-balm')['weather_triggers']
BT = crop(POST, 'bee-balm')['weather_triggers']
assert len(ZT) == 3 and len(BT) == 3, 'trigger counts moved'

# G2. THE ROTATION, byte-identical: each post body_seasoned is the pre title_beginner, each post
# body_beginner is the pre body_seasoned -- no re-authoring of cert-checked prose. Fixture
# sanity: the pre body_beginner really was the stray id.
for i in range(3):
    assert ZT_PRE[i]['body_beginner'] == ZINNIA_STRAY[i], f'fixture sanity: zinnia[{i}] stray id'
    assert ZT[i]['body_seasoned'] == ZT_PRE[i]['title_beginner'], \
        f'zinnia[{i}] body_seasoned is not the rotated pre title_beginner, byte for byte'
    assert ZT[i]['body_beginner'] == ZT_PRE[i]['body_seasoned'], \
        f'zinnia[{i}] body_beginner is not the rotated pre body_seasoned, byte for byte'

# G3. the six titles: exactly the authored constants -- short, capitalized, no em dash
assert [t['title_beginner'] for t in ZT] == ZINNIA_TITLES, 'zinnia titles wrong'
assert [t['title_beginner'] for t in BT] == BEEBALM_TITLES, 'bee-balm titles wrong'
for s in ZINNIA_TITLES + BEEBALM_TITLES:
    assert len(s) <= 60 and s[0].isupper() and '—' not in s and '--' not in s, s

# G4. the restored credits: exact sources lists (restored id appended, nothing dropped) and
# exact anchoring_urls -- old entries byte-identical, new entries read-verified 2026-08-10
for i in range(3):
    assert ZT[i]['sources'] == ZINNIA_SOURCES[i], f"zinnia[{i}] sources: {ZT[i]['sources']}"
    assert ZT[i]['anchoring_urls'] == ZINNIA_ANCHORS[i], \
        f"zinnia[{i}] anchors: {ZT[i]['anchoring_urls']}"

# G5. zinnia: every trigger key OUTSIDE the five touched (title_beginner, body_seasoned,
# body_beginner, sources, anchoring_urls) byte-identical; the rest of the crop untouched
TOUCHED = {'title_beginner', 'body_seasoned', 'body_beginner', 'sources', 'anchoring_urls'}
for i in range(3):
    assert set(ZT_PRE[i]) == set(ZT[i]), f'zinnia[{i}] keys moved'
    for k in set(ZT_PRE[i]) - TOUCHED:
        assert ZT_PRE[i][k] == ZT[i][k], f'zinnia[{i}].{k} moved'
zin_pre_rest = {k: v for k, v in crop(PRE, 'zinnia').items()
                if k not in ('weather_triggers', 'verification_status')}
zin_post_rest = {k: v for k, v in crop(POST, 'zinnia').items()
                 if k not in ('weather_triggers', 'verification_status')}
assert zin_pre_rest == zin_post_rest, 'zinnia moved outside triggers + findings'

# G6. bee-balm: ONLY title_beginner moved, per trigger; the rest of the crop untouched
for i in range(3):
    assert set(BT_PRE[i]) == set(BT[i]), f'bee-balm[{i}] keys moved'
    for k in set(BT_PRE[i]) - {'title_beginner'}:
        assert BT_PRE[i][k] == BT[i][k], f'bee-balm[{i}].{k} moved'
bee_pre_rest = {k: v for k, v in crop(PRE, 'bee-balm').items()
                if k not in ('weather_triggers', 'verification_status')}
bee_post_rest = {k: v for k, v in crop(POST, 'bee-balm').items()
                 if k not in ('weather_triggers', 'verification_status')}
assert bee_pre_rest == bee_post_rest, 'bee-balm moved outside triggers + findings'

# G7. the repair is RECORDED: one appended finding per crop, resolved, non-blocking, prior
# findings byte-identical and still in order
for slug, fid in (('zinnia', ZIN_FID), ('bee-balm', BEE_FID)):
    pre_of = crop(PRE, slug)['verification_status']['open_findings']
    post_of = crop(POST, slug)['verification_status']['open_findings']
    assert post_of[:len(pre_of)] == pre_of, f'{slug} prior findings rewritten'
    assert len(post_of) == len(pre_of) + 1, f'{slug} finding count: {len(post_of)}'
    new = post_of[-1]
    assert new['id'] == fid, f'{slug} new finding id: {new["id"]}'
    assert new['status'] == 'resolved' and new['blocks_launch'] is False, new
    assert 'PLA-157' in new['summary'] and '2026-08-10' in new['summary'], new['summary']

# G8. both cert logs BYTE-IDENTICAL -- this fix owes no correction line, so writing one (or
# rewriting the record) is a bug; the rest of verification_status moves only by the finding
for slug in FOOTPRINT:
    vs_pre = crop(PRE, slug)['verification_status']
    vs_post = crop(POST, slug)['verification_status']
    assert vs_pre['verification_log_ref'] == vs_post['verification_log_ref'], f'{slug} cert log moved'
    for k in set(vs_pre) - {'open_findings'}:
        assert vs_pre[k] == vs_post[k], f'{slug} verification_status.{k} moved'

# G9. the gate the fix ships closes on the fixed state and was RED on the base: A52/A53 report
# zero on POST for both crops, and the pinned pre-state still reproduces 3 identifier + 3 title
# hits on zinnia and 3 title hits on bee-balm
for slug in FOOTPRINT:
    assert identifier_prose_violations(crop(POST, slug)) == [], f'{slug} A52 still red'
    assert title_length_violations(crop(POST, slug)) == [], f'{slug} A53 still red'
assert len(identifier_prose_violations(crop(PRE, 'zinnia'))) == 3, 'RED proof lost (A52)'
assert len(title_length_violations(crop(PRE, 'zinnia'))) == 3, 'RED proof lost (A53 zinnia)'
assert len(title_length_violations(crop(PRE, 'bee-balm'))) == 3, 'RED proof lost (A53 bee-balm)'

# G10. COMPACT preserved; no em dash anywhere in either crop's triggers
assert b'\n' not in _post_raw, 'canonical is not compact'
for t in ZT + BT:
    for k, v in t.items():
        if isinstance(v, str):
            assert '—' not in v, f'em dash in {k}: {v!r}'

print('test_promote_pla157_zinnia_triggers: OK (10 guard groups)')
