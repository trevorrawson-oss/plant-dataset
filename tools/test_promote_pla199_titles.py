#!/usr/bin/env python3
"""Promote guards for PLA-199 (source_catalog titles). Runs BOTH ways (pytest + direct).

Pre/post resolution: pre-state is promote_fixture.pre_state(BASE_SHA). Post-state is, in order:
$PLA199_CANONICAL (scratch artifact pre-GO), promote_fixture.pre_state(POST_SHA) once the
promote commit is registered in COMMIT_FOR, else the live canonical.

Expectations are HAND-WRITTEN (counts, names, spot titles) -- an expectation computed from the
promote's own tables is vacuous (the computed-guard rule, five instances in one day 2026-08-05).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.dirname(HERE)

import promote_fixture  # noqa: E402
from source_catalog_title_gate import LEGACY_UNFILLED, title_violations  # noqa: E402

BASE_SHA = '060b91b807f7988d3d22ebbae77e90d285ee5f7dfe6a18a11c4de37cf6debbbd'
POST_SHA = 'c16071bc34e3f41e0224264adc7d372061ce1b8de9fd2ab61ca5d232b63e4e3b'  # 46f143e

BARE = re.compile(r'https?://[^/]+/?\Z')

# Hand-audited 2026-08-10: 208 catalog entries; 153 document-scoped (pathed url), 55
# institution roots; 101 titles read off cached documents; 52 recorded unfilled.
N_ENTRIES, N_DOC_SCOPED, N_ROOTS, N_TITLED, N_UNFILLED = 208, 153, 55, 101, 52

# The two D1 migrations, old and new names WRITTEN DOWN.
MIGRATIONS = {
    'vce_426_840': (
        'Virginia Cooperative Extension Publication 426-840 (Small Fruit in the Home Garden)',
        'Virginia Cooperative Extension Publication 426-840',
        'Small Fruit in the Home Garden'),
    'vce_spes_455': (
        'Virginia Cooperative Extension Publication SPES-455 (Edamame in Virginia II: '
        'Producing a High-Quality Product)',
        'Virginia Cooperative Extension Publication SPES-455',
        'Edamame in Virginia II. Producing a High-Quality Product'),
}

# Six spot titles, transcribed AGAIN here from the doc-head notes, not imported from the
# promote script.
SPOT_TITLES = {
    'vce_426_331': 'Virginia’s Home Garden Vegetable Planting Guide: Recommended Planting '
                   'Dates and Amounts to Plant',
    'wsu_em051e': 'Home Vegetable Gardening in Washington',
    'uf_ifas_hs1153': 'Lemon Growing in the Florida Home Landscape',
    'nmsu_chart': 'Las Cruces Vegetable Planting Chart',
    'usu_washco_dates': 'Planting Dates (Spring)',
    'ufifas_ae588': 'Carrot (Daucus carota) Production in the Sandy Soils of North Florida: '
                    'Nitrogen Fertilization Guidelines',
}

_pre_raw = promote_fixture.pre_state(BASE_SHA)
_override = os.environ.get('PLA199_CANONICAL')
_live = open(os.path.join(REPO, 'crops_data_final.json'), 'rb').read()
SYNTHESIZED = False
if _override:
    _post_raw = open(_override, 'rb').read()
elif POST_SHA:
    _post_raw = promote_fixture.pre_state(POST_SHA)
elif 'title' not in json.loads(_live)['source_catalog']['vce_426_331']:
    # Pre-GO: the promote has not landed, so no post bytes exist on disk. Synthesize the
    # post-state by RUNNING the transform under test -- the guards' expectations stay
    # hand-written, so this validates the transform end-to-end rather than skipping
    # (a skipped promote suite is how guards go quietly vacuous; memory rule).
    import promote_pla199_titles as _promote
    _post_raw = json.dumps(_promote.apply(json.loads(_pre_raw)),
                           separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    SYNTHESIZED = True
else:
    _post_raw = _live
PRE = json.loads(_pre_raw)
POST = json.loads(_post_raw)
PRE_CAT, POST_CAT = PRE['source_catalog'], POST['source_catalog']
comp = lambda o: json.dumps(o, separators=(',', ':'), ensure_ascii=False)  # noqa: E731


def test_g1_everything_outside_the_catalog_is_byte_identical():
    assert set(PRE) == set(POST), 'top-level key set moved'
    for k in PRE:
        if k != 'source_catalog':
            assert comp(PRE[k]) == comp(POST[k]), f'top-level {k} moved'


def test_g2_catalog_census():
    assert set(PRE_CAT) == set(POST_CAT), 'catalog id set moved'
    assert len(POST_CAT) == N_ENTRIES
    doc = {c for c, e in POST_CAT.items() if not BARE.match(e['url'])}
    assert len(doc) == N_DOC_SCOPED and len(POST_CAT) - len(doc) == N_ROOTS


def test_g3_only_titles_and_the_two_names_moved():
    for cid in PRE_CAT:
        a = dict(PRE_CAT[cid])
        b = {k: v for k, v in POST_CAT[cid].items() if k != 'title'}
        if cid in MIGRATIONS:
            old, new, _ = MIGRATIONS[cid]
            assert a['name'] == old, f'{cid} pre name unexpectedly {a["name"]!r}'
            assert b['name'] == new, f'{cid} post name unexpectedly {b["name"]!r}'
            a['name'] = new
        assert comp(a) == comp(b), f'{cid}: something besides title/name moved'


def test_g4_title_counts_and_placement():
    assert sum('title' in e for e in PRE_CAT.values()) == 0, 'pre-state already had titles'
    titled = [c for c, e in POST_CAT.items() if 'title' in e]
    assert len(titled) == N_TITLED
    for cid in titled:
        e = POST_CAT[cid]
        assert not BARE.match(e['url']), f'{cid}: title on an institution root'
        t = e['title']
        assert isinstance(t, str) and t.strip() == t and t, f'{cid}: unclean title {t!r}'
        keys = list(e)
        assert keys.index('title') == keys.index('name') + 1, f'{cid}: title not after name'


def test_g5_migrated_titles_carry_the_parenthetical_content():
    for cid, (_, _, title) in MIGRATIONS.items():
        assert POST_CAT[cid]['title'] == title, f'{cid} title {POST_CAT[cid]["title"]!r}'


def test_g6_spot_titles_exact():
    for cid, t in SPOT_TITLES.items():
        assert POST_CAT[cid].get('title') == t, f'{cid}: {POST_CAT[cid].get("title")!r}'


def test_g7_unfilled_set_matches_the_gate_exemption_both_directions():
    untitled_doc = {c for c, e in POST_CAT.items()
                    if not BARE.match(e['url']) and 'title' not in e}
    assert len(untitled_doc) == N_UNFILLED
    assert untitled_doc == set(LEGACY_UNFILLED), (
        f'gate exemption drifted from the promote: '
        f'only-in-catalog={sorted(untitled_doc - set(LEGACY_UNFILLED))} '
        f'only-in-gate={sorted(set(LEGACY_UNFILLED) - untitled_doc)}')


def test_g8_a54_green_on_post():
    assert title_violations(POST_CAT) == []


def test_g9_compact_no_trailing_newline():
    if SYNTHESIZED:
        # No on-disk post bytes exist pre-GO; in synthesized mode this check would compare
        # the serializer to itself (trivially green = vacuous). It bites once the promote
        # lands and the suite reads real bytes (override / POST_SHA / live file).
        print('  g9: SYNTHESIZED mode -- on-disk byte check deferred to the landed promote')
        return
    assert not _post_raw.endswith(b'\n'), 'canonical grew a trailing newline'
    assert comp(POST).encode('utf-8') == _post_raw, 'post bytes are not canonical-compact'


TESTS = [v for k, v in sorted(globals().items()) if k.startswith('test_')]

if __name__ == '__main__':
    for t in TESTS:
        t()
        print(f'ok {t.__name__}')
    print(f'{len(TESTS)}/{len(TESTS)} green (direct runner)')
