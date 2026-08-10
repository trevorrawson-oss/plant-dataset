#!/usr/bin/env python3
"""Guards for the PLA-155 vce_426_331 credit corrections. Base ce9eb12f. RED before GREEN.

The load-bearing guards are RETENTION and BLAST-RADIUS: vce_426_331 must SURVIVE on the ~55
in-document vegetables, the declared borrows, the frost-anchored perennials, northern_tier and
zones{} (a suite that only checked the removals would pass on a promote that stripped the id
everywhere -- the exact over-fix the classification argues against). Every expected value below
is WRITTEN DOWN, never computed from the artifact it validates
([[computed-guard-expectations-are-vacuous]]); the changed-path walk iterates BOTH directions
([[blast-radius-guards-iterate-pre-only]]).

Mutation log (RED before GREEN, each run against a sabotaged scratch copy, 2026-08-10). The
first sweep had TWO invalid guards, both caught by mutations: G5/G6 used substring-in-json
checks that fired on legitimate prose mentions ([[guard-tests-pass-because-an-earlier-check-fires]]
inverted -- a broken earlier check masked every later guard), and the first GREEN run exposed
five container-level anchors the promote itself had missed. Final sweep:
  m1 catalog mint skipped            -> G2 fired
  m2 consumer value also edited      -> G8 fired (sweet-pea z7 plant_out)
  m3 elderberry finding dropped      -> G7 fired
  m4 one edamame anchor left behind  -> G6 fired
  m5 8th crop touched                -> G8 fired (lettuce-leaf cell)
  m6 wrong URL in vce_426_840        -> G2 fired
  m7 berry container anchor left     -> G5 fired
  m8 in-doc vegetable stripped       -> G8 fired (broccoli retention, both-direction diff)
  m9 strawberry note reverted        -> G4 fired

Run: python3 tools/test_promote_pla155_vce.py   (or pytest)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_SHA = 'ce9eb12fb85abf9f592ee8bc6621102a5dd785327a74befe2b0e7ddc8146bff5'
# Pinned to the state THIS promote produced (registered in COMMIT_FOR as 503c29f), so the
# suite keeps protecting after canonical moves on. None = read live canonical (bootstrap only).
POST_SHA = '4f6103183ac9c07475b3e0c2d3a71159d0662a10a61383e1d792c049957cac23'

URL_331 = 'https://www.pubs.ext.vt.edu/426/426-331/426-331.html'
URL_840 = 'https://www.pubs.ext.vt.edu/426/426-840/426-840.html'
URL_455 = 'https://www.pubs.ext.vt.edu/SPES/spes-455/spes-455.html'
URL_LATHYRUS = 'https://plants.ces.ncsu.edu/plants/lathyrus-odoratus/'

TOUCHED = {'sweet-pea', 'strawberry', 'blueberry', 'raspberry', 'blackberry', 'elderberry',
           'edamame'}
NEW_FINDING_IDS = {
    'sweet-pea': 'sweet_pea_mid_atlantic_vce_pea_row_analog',
    'strawberry': 'mid_atlantic_strawberry_vce_pub_number_corrected',
    'blueberry': 'mid_atlantic_blueberry_vce_credit_repointed_426_840',
    'raspberry': 'mid_atlantic_raspberry_vce_credit_repointed_426_840',
    'blackberry': 'mid_atlantic_blackberry_vce_credit_repointed_426_840',
    'elderberry': 'mid_atlantic_elderberry_no_vce_planting_model',
    'edamame': 'edamame_vce_pub_id_divergence_corrected',
}
# Raw-substring counts in the POST bytes, hand-audited 2026-08-10 (delta reconciliation in
# docs/2026-08-10-pla155-vce-promote.md): 1281 - 49 removals (strawberry 12, blueberry 6,
# raspberry 6, blackberry 6, elderberry 6, edamame 13) + 15 finding-text mentions
# (7 filed_in_session substrings + 8 summary mentions) = 1247.
POST_COUNTS = {'vce_426_331': 1247, 'vce_426_840': 36, 'vce_spes_455': 16,
               'VCE 426-331': 225, 'VCE 426-840': 5}

_pre_raw = promote_fixture.pre_state(BASE_SHA)
_override = os.environ.get('PLA155_CANONICAL')
if _override:
    _post_raw = open(_override, 'rb').read()
elif POST_SHA:
    _post_raw = promote_fixture.pre_state(POST_SHA)
else:
    _post_raw = open(os.path.join(REPO, 'crops_data_final.json'), 'rb').read()
PRE = json.loads(_pre_raw)
POST = json.loads(_post_raw)
POST_TEXT = _post_raw.decode('utf-8') if isinstance(_post_raw, bytes) else _post_raw


def crop(d, slug):
    return next(c for c in d['crops'] if c['slug'] == slug)


# G1. roster identical, both directions
assert {c['slug'] for c in PRE['crops']} == {c['slug'] for c in POST['crops']}, 'roster moved'

# G2. catalog: exactly two new ids, at the written-down URLs; nothing else moved
pre_cat, post_cat = set(PRE['source_catalog']), set(POST['source_catalog'])
assert post_cat - pre_cat == {'vce_426_840', 'vce_spes_455'}, f'catalog delta {post_cat - pre_cat}'
assert pre_cat - post_cat == set(), 'a catalog id vanished'
assert POST['source_catalog']['vce_426_840']['url'] == URL_840
assert POST['source_catalog']['vce_spes_455']['url'] == URL_455
assert POST['source_catalog']['vce_426_840']['tier'] == 'T1'
assert POST['source_catalog']['vce_spes_455']['tier'] == 'T1'
for cid in pre_cat:
    assert PRE['source_catalog'][cid] == POST['source_catalog'][cid], f'catalog {cid} moved'

# G3. sweet-pea: ncsu_ext JOINS, vce_426_331 SURVIVES, values byte-identical
sp_pre, sp_post = crop(PRE, 'sweet-pea'), crop(POST, 'sweet-pea')
assert sp_pre['regions']['mid_atlantic']['sources'] == ['vce_426_331']
assert sp_post['regions']['mid_atlantic']['sources'] == ['ncsu_ext', 'vce_426_331']
for z in ('7', '8'):
    pre_c = sp_pre['regions']['mid_atlantic']['resolved_by_zone'][z]
    post_c = sp_post['regions']['mid_atlantic']['resolved_by_zone'][z]
    assert pre_c['sources'] == ['vce_426_331']
    assert post_c['sources'] == ['ncsu_ext', 'vce_426_331']
    assert post_c['anchoring_urls']['ncsu_ext']['url'] == URL_LATHYRUS
    assert post_c['anchoring_urls']['vce_426_331']['url'] == URL_331, 'vce anchor must survive'
assert sp_post['regions']['mid_atlantic']['resolved_by_zone']['7']['plant_out'] == 'Mar 1 - Apr 1'
assert sp_post['regions']['mid_atlantic']['resolved_by_zone']['7']['harvest'] == 'Apr 13 - May 14'
assert sp_post['regions']['mid_atlantic']['resolved_by_zone']['8']['plant_out'] == 'Feb 20 - Apr 1'

# G4. strawberry: id + pub-number strings move together; nothing else in the arms moves
st_post = crop(POST, 'strawberry')
ma = st_post['regions']['mid_atlantic']
assert ma['sources'] == ['vce_426_840', 'ncsu_ext']
z7 = ma['resolved_by_zone']['7']
assert z7['sources'] == ['vce_426_840']
assert z7['anchoring_urls']['vce_426_840']['url'] == URL_840
assert 'vce_426_331' not in z7['anchoring_urls']
assert z7['plant_out'] == 'Apr 1 - Apr 22' and z7['harvest'] == 'May 27 - Jun 24'
entry = ma['plantings'][0]
assert set(entry['anchoring_urls']) == {'vce_426_840'}, 'strawberry container anchor'
assert entry['anchoring_urls']['vce_426_840']['url'] == URL_840
EXPECT_NOTE_PLANT = ('Set dormant bare-root crowns about two weeks before the last spring frost, '
                     'as soon as the soil can be worked; the crowns are dormant stock, so there '
                     'is no need to wait out frost danger (VCE 426-840 home garden matted-row '
                     'guidance).')
assert entry['plant_out'][0]['synthesis_note'] == EXPECT_NOTE_PLANT
for fld in ('plant_out', 'bloom', 'harvest_start', 'harvest_end'):
    arm = entry[fld][0]
    assert arm['sources'] == ['vce_426_840'], f'strawberry {fld} arm sources {arm["sources"]}'
    assert arm['anchoring_urls']['vce_426_840']['url'] == URL_840
    assert 'VCE 426-331' not in arm['synthesis_note']
    assert 'VCE 426-840' in arm['synthesis_note']
# z8 untouched, byte-identical
assert crop(PRE, 'strawberry')['regions']['mid_atlantic']['resolved_by_zone']['8'] == \
    ma['resolved_by_zone']['8'], 'strawberry z8 must not move'

# G5. berry trio swap + elderberry removal
for slug in ('blueberry', 'raspberry', 'blackberry'):
    c = crop(POST, slug)
    ma = c['regions']['mid_atlantic']
    assert ma['sources'] == ['ncsu_ext', 'vce_426_840'], f'{slug} region {ma["sources"]}'
    cont = ma['plantings'][0]['anchoring_urls']
    assert set(cont) == {'ncsu_ext', 'vce_426_840'}, f'{slug} container anchor {sorted(cont)}'
    assert cont['vce_426_840']['url'] == URL_840
    for z in ('7', '8'):
        cell = ma['resolved_by_zone'][z]
        assert cell['sources'] == ['ncsu_ext', 'vce_426_840'], f'{slug} z{z}'
        assert cell['anchoring_urls']['vce_426_840']['url'] == URL_840
        assert 'vce_426_331' not in cell['anchoring_urls']
el = crop(POST, 'elderberry')
assert 'vce' not in json.dumps(el['regions']['mid_atlantic']), 'elderberry must carry NO vce id'
assert el['regions']['mid_atlantic']['sources'] == ['ncsu_ext']
for z in ('7', '8'):
    cell = el['regions']['mid_atlantic']['resolved_by_zone'][z]
    assert cell['sources'] == ['ncsu_ext']
    assert cell['plant_out'] == 'March to April', 'elderberry values must not move'

# G6. edamame: complete repoint -- the wrong id survives in NO sources list and NO anchor key
# (the new finding's prose legitimately names it; prose is exempt, citation layer is not)
ed = crop(POST, 'edamame')


def cites(node, ident, out, path=''):
    if isinstance(node, dict):
        if ident in (node.get('sources') or []):
            out.append(f'{path}.sources')
        if isinstance(node.get('anchoring_urls'), dict) and ident in node['anchoring_urls']:
            out.append(f'{path}.anchoring_urls')
        for k, v in node.items():
            cites(v, ident, out, f'{path}.{k}')
    elif isinstance(node, list):
        for i, x in enumerate(node):
            cites(x, ident, out, f'{path}[{i}]')


bad = []
cites(ed, 'vce_426_331', bad)
assert not bad, f'edamame still cites the wrong id at {bad}'
assert 'vce_426_331' not in ed['verification_status']['source_set']
six = [ed['fertilizer'], ed['varieties'], ed['tips_by_stage']['germination'][1],
       ed['tips_by_stage']['pod_fill'][0], ed['failure_diagnostics'][0],
       ed['failure_diagnostics'][2]]
for node in six:
    assert 'vce_spes_455' in node['sources'], f'node missing vce_spes_455: {node.get("sources")}'
    assert node['anchoring_urls']['vce_spes_455']['url'] == URL_455
assert 'vce_spes_455' in ed['verification_status']['source_set']
assert ed['verification_status']['source_set'] == sorted(ed['verification_status']['source_set'])

# G7. findings: each new id exactly once in POST, absent in PRE
for slug, fid in NEW_FINDING_IDS.items():
    pre_ids = [f.get('id') for f in crop(PRE, slug)['verification_status']['open_findings']]
    post_ids = [f.get('id') for f in crop(POST, slug)['verification_status']['open_findings']]
    assert fid not in pre_ids, f'{fid} pre-existed'
    assert post_ids.count(fid) == 1, f'{fid} count {post_ids.count(fid)}'
    assert post_ids[:len(pre_ids)] == pre_ids, f'{slug} findings reordered or dropped'

# G8. blast radius: the ONLY changed paths are citation-layer, in the 7 named crops (+ catalog)


def leaf_diff(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                out.append(f'{path}.{k}')
            else:
                leaf_diff(a[k], b[k], f'{path}.{k}', out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(path)
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                leaf_diff(x, y, f'{path}[{i}]', out)
    elif a != b:
        out.append(path)


ALLOWED_SUFFIXES = ('.sources', '.anchoring_urls', '.open_findings', '.source_set',
                    '.synthesis_note')
changed = []
leaf_diff(PRE, POST, '', changed)
assert changed, 'no diff at all -- guard suite is vacuous'
pre_slugs = [c['slug'] for c in PRE['crops']]
for p in changed:
    if p.startswith('.source_catalog'):
        continue
    assert p.startswith('.crops['), f'unexpected top-level change {p}'
    idx = int(p.split('[', 1)[1].split(']', 1)[0])
    slug = pre_slugs[idx]
    assert slug in TOUCHED, f'untouched crop {slug} changed: {p}'
    assert any(s in p for s in ALLOWED_SUFFIXES), f'non-citation-layer change: {p}'
    if '.synthesis_note' in p:
        assert slug == 'strawberry' and '.plantings[0].' in p, f'synthesis_note outside straw arms: {p}'

# G9. retention: the id survives everywhere it is legitimately doing work (written-down spots)
for slug, z, expect in [('broccoli', '7', True), ('cucumber', '8', True), ('thyme', '7', True),
                        ('shallot', '7', True), ('popcorn', '8', True), ('bok-choy', '7', True)]:
    cell = crop(POST, slug)['regions']['mid_atlantic']['resolved_by_zone'][z]
    assert ('vce_426_331' in cell['sources']) is expect, f'{slug} z{z} retention broke'
nt = crop(POST, 'cherry-tomato')['regions']['northern_tier']['resolved_by_zone']['6']
assert 'vce_426_331' in nt['sources'], 'northern_tier must be untouched here (PLA-195 block d)'

# G10. raw-substring counts at the hand-audited literals
for ident, n in POST_COUNTS.items():
    assert POST_TEXT.count(ident) == n, f'{ident}: {POST_TEXT.count(ident)} != {n}'

# G11. compact JSON survived: no indent artifacts, no trailing newline
assert not POST_TEXT.endswith('\n'), 'trailing newline'
assert '",\n' not in POST_TEXT[:2000], 'looks indented'

print('PLA-155 promote guards: ALL GREEN '
      f'({len(changed)} changed leaf paths, all citation-layer, crops={sorted(TOUCHED)})')
