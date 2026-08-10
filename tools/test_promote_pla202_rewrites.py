#!/usr/bin/env python3
"""Guard suite for promote_pla202_rewrites.py (base c16071bc -> POST_SHA).

Fixture-pinned per tools/promote_fixture.py: the pre-state is rebuilt by hash, the post
state is rebuilt by REPLAYING the promote script on that fixture, so this suite never
reads live canonical and cannot go vacuous when canonical moves on.

Expectations are hand-written where they are load-bearing:
  * CLEARED_RUNS come from the adjudication ledger (docs/pla202_verbatim_adjudication_
    c16071bc.json), NOT from the staged replacement table -- the ledger is the
    independent record of what had to disappear.
  * SPOT_PHRASES are hand-picked distinctive sentences from the authored delivery, one
    per writing unit -- they catch a replacement applied to the wrong field or not at
    all, independently of comparing against the staged table the script itself reads.
Every guard is mutation-tested in this file: each sabotage test doctors the post state
and asserts the specific guard goes red.
"""
import copy
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402

BASE_SHA = 'c16071bc34e3f41e0224264adc7d372061ce1b8de9fd2ab61ca5d232b63e4e3b'
POST_SHA = '76f92a20faae0b8e5336ef8e7e1d9c852b9c734c93ae84fc6cccd65f49bcf3ce'

TOUCHED = {
    'asparagus': ['description_seasoned', 'hardiness_notes_seasoned',
                  'soil.preferred_description_seasoned'],
    'beet': ['regions.utah_dixie.region_notes_beginner'],
    'carrot': ['regions.utah_dixie.region_notes_beginner'],
    'turnip': ['regions.utah_dixie.region_notes_beginner'],
    'spring-onion': ['regions.utah_dixie.region_notes_seasoned'],
    'cabbage': ['regions.hawaii_tropical.resolved_by_zone.10.zone_notes',
                'regions.hawaii_tropical.resolved_by_zone.11.zone_notes',
                'regions.hawaii_tropical.resolved_by_zone.12.zone_notes',
                'regions.hawaii_tropical.resolved_by_zone.13.zone_notes',
                'regions.hawaii_tropical.region_notes_seasoned'],
    'cherry-sour': ['regions.mid_atlantic.resolved_by_zone.7.suitability_note_seasoned',
                    'regions.mid_atlantic.resolved_by_zone.8.suitability_note_seasoned'],
    'chives': ['regions.fl_peninsula.region_notes_beginner'],
    'echinacea': ['regions.fl_peninsula.region_notes_beginner'],
    'english-cucumber': ['diseases[1].symptoms_seasoned'],
    'fig': ['companions.bad_seasoned[0].why_seasoned'],
    'lime': ['diseases[5].cause_seasoned'],
    'pawpaw': ['pests[0].cause_seasoned'],
    'raspberry': ['regions.utah_dixie.region_notes_seasoned'],
    'strawberry': ['regions.ca_north_coast.region_notes_seasoned'],
}

# Hand-pinned from the PLA-202 adjudication ledger: the normalized shared runs that made
# each field a rewrite. After the promote, the field's normalized prose must contain NONE
# of its runs. Scoped per field -- several of these strings remain legitimately (benign)
# elsewhere in the roster.
CLEARED_RUNS = {
    ('asparagus', 'description_seasoned'): [
        'requires two distinct periods a growing period and a resting period'],
    ('asparagus', 'hardiness_notes_seasoned'): [
        'spring freezes will not harm the crowns or subsequent harvests but can damage emerging spears',
        'two distinct periods a growing period and a resting period'],
    ('asparagus', 'soil.preferred_description_seasoned'): [
        'in heavy medium or sandy soils as long as the',
        'does not pool water after rain'],
    ('beet', 'regions.utah_dixie.region_notes_beginner'): [
        'can be left in the ground quite late into'],
    ('carrot', 'regions.utah_dixie.region_notes_beginner'): [
        'can be left in the ground quite late into'],
    ('turnip', 'regions.utah_dixie.region_notes_beginner'): [
        'can be left in the ground quite late into'],
    ('spring-onion', 'regions.utah_dixie.region_notes_seasoned'): [
        'green onions can be planted spring or fall as they do not take long to mature'],
    ('cabbage', 'regions.hawaii_tropical.resolved_by_zone.10.zone_notes'): [
        'excellent garden crops at low elevations during winter and'],
    ('cabbage', 'regions.hawaii_tropical.resolved_by_zone.11.zone_notes'): [
        'excellent garden crops at low elevations during winter and'],
    ('cabbage', 'regions.hawaii_tropical.resolved_by_zone.12.zone_notes'): [
        'excellent garden crops at low elevations during winter and'],
    ('cabbage', 'regions.hawaii_tropical.resolved_by_zone.13.zone_notes'): [
        'excellent garden crops at low elevations during winter and'],
    ('cabbage', 'regions.hawaii_tropical.region_notes_seasoned'): [
        'excellent garden crops at low elevations during winter and'],
    ('cherry-sour', 'regions.mid_atlantic.resolved_by_zone.7.suitability_note_seasoned'): [
        'where the climate is favorable but need careful management and will not consistently bear fruit'],
    ('cherry-sour', 'regions.mid_atlantic.resolved_by_zone.8.suitability_note_seasoned'): [
        'where the climate is favorable but need careful management and will not consistently bear fruit'],
    ('chives', 'regions.fl_peninsula.region_notes_beginner'): [
        'a cool season herb that thrives in florida s fall and spring'],
    ('echinacea', 'regions.fl_peninsula.region_notes_beginner'): [
        'a year or two and then fizzle out though'],
    ('english-cucumber', 'diseases[1].symptoms_seasoned'): [
        'downy mildew is one of the most important leaf diseases of cucurbits'],
    ('fig', 'companions.bad_seasoned[0].why_seasoned'): [
        'root knot nematodes are the leading killer of'],
    ('lime', 'diseases[5].cause_seasoned'): [
        'is most prevalent during the rainy season when flowers are present'],
    ('pawpaw', 'pests[0].cause_seasoned'): [
        'into the fleshy tissues of the flower causing'],
    ('raspberry', 'regions.utah_dixie.region_notes_seasoned'): [
        'fruit ripens after the hottest part of the summer is over'],
    ('strawberry', 'regions.ca_north_coast.region_notes_seasoned'): [
        'highest in the first full season after planting and declines'],
}

# One distinctive hand-transcribed phrase per writing unit from the authored delivery.
SPOT_PHRASES = {
    ('asparagus', 'description_seasoned'):
        "ties the plant's longevity to getting a true dormant season each year",
    ('asparagus', 'hardiness_notes_seasoned'):
        'the crown does its rebuilding while the top is down',
    ('asparagus', 'soil.preferred_description_seasoned'):
        'Texture is not the real constraint here, drainage is.',
    ('beet', 'regions.utah_dixie.region_notes_beginner'):
        'There is no need to clear the whole row at once',
    ('carrot', 'regions.utah_dixie.region_notes_beginner'):
        'counts the winter bed as its own storage for carrots',
    ('turnip', 'regions.utah_dixie.region_notes_beginner'):
        'Frost does not end this one.',
    ('spring-onion', 'regions.utah_dixie.region_notes_seasoned'):
        'room for a sowing at each end of the season',
    ('cabbage', 'regions.hawaii_tropical.resolved_by_zone.10.zone_notes'):
        'CTAHR divides the state by elevation',
    ('cabbage', 'regions.hawaii_tropical.region_notes_seasoned'):
        'though leaf diseases become the main worry there',
    ('cherry-sour', 'regions.mid_atlantic.resolved_by_zone.7.suitability_note_seasoned'):
        'trees that skip crops in some years and that repay close management',
    ('chives', 'regions.fl_peninsula.region_notes_beginner'):
        'Summer is the hard part.',
    ('echinacea', 'regions.fl_peninsula.region_notes_beginner'):
        'may only be a two-season plant',
    ('english-cucumber', 'diseases[1].symptoms_seasoned'):
        'this is the one that costs growers the most',
    ('fig', 'companions.bad_seasoned[0].why_seasoned'):
        'nothing else takes down as many fig trees',
    ('lime', 'diseases[5].cause_seasoned'):
        'lands only where wet weather and open bloom coincide',
    ('pawpaw', 'pests[0].cause_seasoned'):
        'the feeding happens out of sight inside the flower itself',
    ('raspberry', 'regions.utah_dixie.region_notes_seasoned'):
        'comes in on the far side of the summer peak',
    ('strawberry', 'regions.ca_north_coast.region_notes_seasoned'):
        'the bed gets pulled and reset rather than carried forward',
}

PATH_TOKEN = re.compile(r'([^.\[\]]+)|\[(\d+)\]')


def _resolve(crop, path):
    node = crop
    for m in PATH_TOKEN.finditer(path):
        k, i = m.group(1), m.group(2)
        node = node[k] if k is not None else node[int(i)]
    return node


def _set(crop, path, value):
    toks = [(m.group(1), m.group(2)) for m in PATH_TOKEN.finditer(path)]
    node = crop
    for k, i in toks[:-1]:
        node = node[k] if k is not None else node[int(i)]
    k, i = toks[-1]
    node[k if k is not None else int(i)] = value


def _norm(text):
    return ' '.join(re.sub(r'[^a-z0-9°\s]', ' ', text.lower()).split())


_post_cache = {}


def post_bytes():
    """Replay the promote script on the rebuilt pre-state fixture; cache the result."""
    if 'raw' not in _post_cache:
        path, sha = promote_fixture.scratch(BASE_SHA)
        assert sha == BASE_SHA
        r = subprocess.run(
            [sys.executable, os.path.join(HERE, 'promote_pla202_rewrites.py'), path],
            capture_output=True, text=True)
        assert r.returncode == 0, f'replay failed: {(r.stdout + r.stderr)[-500:]}'
        _post_cache['raw'] = open(path, 'rb').read()
    return _post_cache['raw']


def _pre_data():
    return json.loads(promote_fixture.pre_state(BASE_SHA))


def _post_data():
    return json.loads(post_bytes())


# ---- assertion cores (called by tests AND by the sabotage tests on doctored states) ----

def assert_cleared_runs_absent(post):
    crops = {c['slug']: c for c in post['crops']}
    for (slug, path), runs in CLEARED_RUNS.items():
        text = _norm(_resolve(crops[slug], path))
        for run in runs:
            assert run not in text, f'{slug}:{path} still carries the cleared run "{run[:50]}..."'


def assert_spot_phrases_present(post):
    crops = {c['slug']: c for c in post['crops']}
    for (slug, path), phrase in SPOT_PHRASES.items():
        val = _resolve(crops[slug], path)
        assert phrase in val, f'{slug}:{path} lacks the authored phrase "{phrase[:50]}..."'


def assert_blast_radius(pre, post):
    pre_crops = {c['slug']: c for c in pre['crops']}
    post_crops = {c['slug']: c for c in post['crops']}
    assert set(pre_crops) == set(post_crops), 'crop roster changed'
    assert [c['slug'] for c in pre['crops']] == [c['slug'] for c in post['crops']], \
        'crop order changed'
    assert set(pre) == set(post), 'top-level keys changed'
    for key in pre:
        if key != 'crops':
            assert pre[key] == post[key], f'top-level {key!r} moved'
    for slug in pre_crops:
        a, b = copy.deepcopy(pre_crops[slug]), copy.deepcopy(post_crops[slug])
        for path in TOUCHED.get(slug, []):
            _set(a, path, None)
            _set(b, path, None)
        assert a == b, f'{slug}: a field outside the enumerated 22 moved'
    for slug, paths in TOUCHED.items():
        for path in paths:
            assert _resolve(pre_crops[slug], path) != _resolve(post_crops[slug], path), \
                f'{slug}:{path} was enumerated as touched but did not change'


def assert_conventions(post):
    crops = {c['slug']: c for c in post['crops']}
    for slug, paths in TOUCHED.items():
        for path in paths:
            val = _resolve(crops[slug], path)
            for ch in ('—', '–', '--'):
                assert ch not in val, f'{slug}:{path} carries {ch!r}'
    for slug in ('beet', 'carrot', 'turnip'):
        assert '100°F' in _resolve(crops[slug], TOUCHED[slug][0]), f'{slug}: 100°F lost'
    assert '100°F' in _resolve(crops['spring-onion'], TOUCHED['spring-onion'][0])


# ---- tests ------------------------------------------------------------------------------

def test_replay_reaches_pinned_post_sha():
    assert hashlib.sha256(post_bytes()).hexdigest() == POST_SHA


def test_compact_preserved():
    raw = post_bytes()
    assert b'\n' not in raw, 'canonical must be single-line COMPACT with no trailing newline'
    data = json.loads(raw)
    assert json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8') == raw


def test_cleared_runs_absent():
    assert_cleared_runs_absent(_post_data())


def test_spot_phrases_present():
    assert_spot_phrases_present(_post_data())


def test_blast_radius():
    assert_blast_radius(_pre_data(), _post_data())


def test_conventions():
    assert_conventions(_post_data())


def test_cherry_sour_zone_variants_stay_parallel():
    crops = {c['slug']: c for c in _post_data()['crops']}
    z7 = _resolve(crops['cherry-sour'], TOUCHED['cherry-sour'][0])
    z8 = _resolve(crops['cherry-sour'], TOUCHED['cherry-sour'][1])
    assert z7.replace('1100 to 1500', '1000 to 1350').replace('zone 7', 'zone 8') == z8


def test_cabbage_zone_notes_stay_identical_across_zones():
    crops = {c['slug']: c for c in _post_data()['crops']}
    vals = {_resolve(crops['cabbage'], p)
            for p in TOUCHED['cabbage'] if p.endswith('zone_notes')}
    assert len(vals) == 1


def test_script_aborts_on_wrong_base():
    path, _ = promote_fixture.scratch(BASE_SHA, mutate=lambda crops, data: _set(
        crops['asparagus'], 'description_seasoned', 'tampered'))
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, 'promote_pla202_rewrites.py'), path],
        capture_output=True, text=True)
    assert r.returncode != 0 and 'pre-state pin failed' in r.stderr


# ---- mutation tests: every guard above must catch its sabotage --------------------------

def _expect_red(fn, *args):
    try:
        fn(*args)
    except AssertionError:
        return
    raise AssertionError(f'{fn.__name__} stayed GREEN under sabotage -- vacuous guard')


def test_sabotage_reintroduced_run_is_caught():
    post = _post_data()
    crops = {c['slug']: c for c in post['crops']}
    _set(crops['lime'], 'diseases[5].cause_seasoned',
         _resolve(crops['lime'], 'diseases[5].cause_seasoned')
         + ' It is most prevalent during the rainy season when flowers are present.')
    _expect_red(assert_cleared_runs_absent, post)


def test_sabotage_skipped_field_is_caught():
    pre, post = _pre_data(), _post_data()
    pre_fig = next(c for c in pre['crops'] if c['slug'] == 'fig')
    post_fig = next(c for c in post['crops'] if c['slug'] == 'fig')
    original = _resolve(pre_fig, 'companions.bad_seasoned[0].why_seasoned')
    _set(post_fig, 'companions.bad_seasoned[0].why_seasoned', original)
    _expect_red(assert_spot_phrases_present, post)          # authored phrase now missing
    _expect_red(assert_blast_radius, pre, post)             # enumerated field did not change


def test_sabotage_out_of_footprint_edit_is_caught():
    pre, post = _pre_data(), _post_data()
    kale = next(c for c in post['crops'] if c['slug'] == 'kale')
    kale['description_seasoned'] = kale.get('description_seasoned', '') + ' tampered'
    _expect_red(assert_blast_radius, pre, post)


def test_sabotage_in_crop_out_of_field_edit_is_caught():
    pre, post = _pre_data(), _post_data()
    fig = next(c for c in post['crops'] if c['slug'] == 'fig')
    fig['watering']['frequency_seasoned'] = fig['watering']['frequency_seasoned'] + ' tampered'
    _expect_red(assert_blast_radius, pre, post)


def test_sabotage_catalog_edit_is_caught():
    pre, post = _pre_data(), _post_data()
    key = next(k for k in post if k != 'crops')
    post[key] = copy.deepcopy(post[key])
    if isinstance(post[key], dict):
        post[key]['__tampered__'] = True
    else:
        post[key] = 'tampered'
    _expect_red(assert_blast_radius, pre, post)


def test_sabotage_dash_is_caught():
    post = _post_data()
    crops = {c['slug']: c for c in post['crops']}
    _set(crops['chives'], 'regions.fl_peninsula.region_notes_beginner',
         _resolve(crops['chives'], 'regions.fl_peninsula.region_notes_beginner')
         + ' — tampered')
    _expect_red(assert_conventions, post)


if __name__ == '__main__':
    fns = [(n, f) for n, f in sorted(globals().items())
           if n.startswith('test_') and callable(f)]
    for name, fn in fns:
        fn()
        print(f'PASS {name}')
    print(f'{len(fns)} checks passed (direct runner)')
