#!/usr/bin/env python3
"""Guards for the PLA-290 follow-on echinacea record promote.

REPLAY-PINNED BOTH ENDS: the PRE state is rebuilt from git by hash and the POST state by
REPLAYING this promote on that fixture, so the suite never reads live canonical. It cannot go
vacuous when canonical moves on ([[promote-guards-went-vacuous-on-sha-skip]]) and cannot redden
on somebody else's later promote ([[promote-suite-post-must-be-replayed-not-live]] -- which
recurred in two suites born days before PLA-290 and is now checked at birth).

THE GUARD THAT MATTERS MOST is the dashed-prefix one: an id that fails it does not render
wrong, it silently unplants a real garden record.

THE ROSTER-WIDE CAP GUARD is the point of the whole change: after this, no variety's app
display name exceeds 70 characters and none contains a colon, across all 756 entries. It is
asserted over the WHOLE roster, not over echinacea, so a future regression anywhere reddens it.

Mutation evidence: tools/mutate_pla290b_echinacea_suite.py
"""
import copy
import json
import os
import re
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
import promote_pla290b_echinacea_record as P  # noqa: E402

SCRIPT = os.path.join(HERE, 'promote_pla290b_echinacea_record.py')

# plant-app's legacy string branch, transcribed: it splits ONLY a trailing parenthetical.
TRAILING_PAREN = re.compile(r'^(.+?)\s+\(([^)]+)\)$')
NAME_CAP = 70

_post = {}


def post_bytes():
    if 'raw' not in _post:
        path, sha = promote_fixture.scratch(P.BASE_SHA)
        assert sha == P.BASE_SHA
        r = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
        assert r.returncode == 0, f'replay failed: {(r.stdout + r.stderr)[-800:]}'
        _post['raw'] = open(path, 'rb').read()
    return _post['raw']


@pytest.fixture(scope='module')
def pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


@pytest.fixture(scope='module')
def post():
    return json.loads(post_bytes())


def recs(data, slug):
    return {c['slug']: c for c in data['crops']}[slug]['varieties']['recommended']


def display_name(entry):
    """What the app actually puts in the card title, for either entry shape."""
    if isinstance(entry, dict):
        return str(entry.get('name', ''))
    m = TRAILING_PAREN.match(entry)
    return m.group(1) if m else entry


def every_entry(data):
    for c in data['crops']:
        for i, e in enumerate((c.get('varieties') or {}).get('recommended') or []):
            yield c['slug'], i, e


# --- the entry ------------------------------------------------------------------------------

def test_the_entry_is_now_a_record(post):
    assert recs(post, P.CROP)[P.INDEX] == P.RECORD


def test_the_name_is_a_name_and_not_a_sentence(post):
    entry = recs(post, P.CROP)[P.INDEX]
    assert entry['name'] == 'Interspecific hybrid color series'
    assert len(entry['name']) <= NAME_CAP
    assert ';' not in entry['name'] and ':' not in entry['name']


def test_the_slug_rule_agrees_with_PLA290s_over_the_whole_corpus(post):
    """This promote defines its own `slugify_variety` rather than importing PLA-290's, so the
    two frozen records stay independent. That trade is only safe if they actually agree --
    asserted over every variety name and every legacy prose string in the live dataset, not
    over a handful of hand-picked examples."""
    import promote_pla290_variety_records as Q
    corpus = [e['name'] if isinstance(e, dict) else e for _s, _i, e in every_entry(post)]
    for entries in Q.PREV_ENTRIES.values():
        corpus.extend(entries)
    corpus.append(P.PREV_ENTRY)
    assert len(corpus) > 700, f'corpus suspiciously small ({len(corpus)})'
    for name in corpus:
        assert P.slugify_variety(name) == Q.slugify_variety(name), f'slug rules differ on {name!r}'


def test_the_id_prefixes_the_stored_legacy_slug(post):
    """The whole 228-char sentence is what a planting stores today, because the trailing-paren
    rule does not match it. The shim bridges it only by dashed prefix."""
    legacy = P.slugify_variety(P.PREV_ENTRY)
    assert legacy.startswith(recs(post, P.CROP)[P.INDEX]['id'] + '-')


def test_the_id_equals_slugify_of_its_name(post):
    entry = recs(post, P.CROP)[P.INDEX]
    assert entry['id'] == P.slugify_variety(entry['name'])


def test_the_legacy_stored_id_resolves_to_THIS_record(post):
    """plant-app's varietyFor() transcribed, over echinacea's whole array."""
    records = [e for e in recs(post, P.CROP) if isinstance(e, dict)]
    stored = P.slugify_variety(P.PREV_ENTRY)
    hit = None
    for v in records:
        if stored.startswith(v['id'] + '-') and len(v['id']) > (len(hit['id']) if hit else 0):
            hit = v
    assert hit is not None and hit['id'] == P.RECORD['id']


def test_no_word_of_the_original_was_dropped(post):
    """There is no colon to split on here -- the sentence runs THROUGH its parenthetical -- so
    the split is authored, and an authored split is exactly where words go missing."""
    entry = recs(post, P.CROP)[P.INDEX]
    was = set(re.findall(r'[a-z0-9]+', P.PREV_ENTRY.lower()))
    now = set(re.findall(r'[a-z0-9]+', (entry['name'] + ' ' + entry['note']).lower()))
    assert not (was - now), f'dropped {sorted(was - now)}'


def test_the_note_keeps_every_named_cultivar(post):
    """The cultivar list is the entry's substance; a tidier note that quietly dropped two of
    them would still read fine."""
    note = recs(post, P.CROP)[P.INDEX]['note']
    for cultivar in ('Big Sky', 'Conefections', 'Sombrero', 'Hot Papaya', 'Tiki Torch'):
        assert cultivar in note, f'{cultivar} dropped'
    for color in ('orange', 'red', 'yellow', 'doubles'):
        assert color in note, f'{color} dropped'


def test_the_note_is_a_finished_sentence_without_an_em_dash(post):
    note = recs(post, P.CROP)[P.INDEX]['note']
    assert note[0].isupper() and note.endswith('.')
    assert '—' not in note and '–' not in note


def test_no_days_to_maturity_was_invented(post):
    assert set(recs(post, P.CROP)[P.INDEX]) == {'id', 'name', 'note'}


# --- the roster-wide property this change exists to establish -------------------------------

def test_no_variety_display_name_exceeds_the_cap_ANYWHERE(post):
    """The point of the change, asserted over all 756 entries rather than over echinacea, so a
    regression introduced by any future crop reddens here."""
    over = [(s, i, display_name(e)) for s, i, e in every_entry(post)
            if len(display_name(e)) > NAME_CAP]
    assert not over, f'{len(over)} display name(s) over {NAME_CAP}: ' \
                     f'{[(s, i, n[:60]) for s, i, n in over]}'


def test_no_variety_display_name_contains_a_colon_ANYWHERE(post):
    """PLA-290's property, re-asserted here so the two halves of the defect family cannot
    regress independently."""
    bad = [(s, i, display_name(e)) for s, i, e in every_entry(post) if ':' in display_name(e)]
    assert not bad, f'{bad[:5]}'


def test_the_cap_guard_was_actually_reachable_before_this_promote(pre):
    """REACHABILITY: prove the roster-wide guard above is not green-by-vacuity. Against the PRE
    state it must find exactly this one offender -- a guard that never had anything to catch
    reads as coverage while providing none ([[guard-reachability-must-be-measured]])."""
    over = [(s, i) for s, i, e in every_entry(pre) if len(display_name(e)) > NAME_CAP]
    assert over == [(P.CROP, P.INDEX)], f'expected exactly the echinacea offender, got {over}'


# --- blast radius ---------------------------------------------------------------------------

def test_echinaceas_other_six_entries_are_untouched_strings(pre, post):
    """They are clean trailing parentheticals the app parses correctly, and PLA-290 ruled that
    family out of scope. Converting them would be shim-safe but is not this change."""
    a, b = recs(pre, P.CROP), recs(post, P.CROP)
    assert len(a) == len(b) == 7
    for i in range(7):
        if i == P.INDEX:
            continue
        assert isinstance(b[i], str), f'echinacea[{i}] was converted'
        assert a[i] == b[i], f'echinacea[{i}] changed'


def test_nothing_outside_that_one_leaf_moved(pre, post):
    """Key sets FIRST, both directions, then values."""
    a, b = copy.deepcopy(pre), copy.deepcopy(post)
    ca = {c['slug']: c for c in a['crops']}
    cb = {c['slug']: c for c in b['crops']}
    assert set(ca) == set(cb), 'the crop roster changed'
    for slug in ca:
        if slug != P.CROP:
            assert ca[slug] == cb[slug], f'{slug} changed'
    assert set(ca[P.CROP]) == set(cb[P.CROP]), 'echinacea gained or lost a top-level key'
    assert set(ca[P.CROP]['varieties']) == set(cb[P.CROP]['varieties']), \
        'echinacea.varieties gained or lost a key'
    ca[P.CROP]['varieties']['recommended'] = cb[P.CROP]['varieties']['recommended']
    assert ca[P.CROP] == cb[P.CROP], 'echinacea changed outside varieties.recommended'
    assert set(a) == set(b), 'a top-level dataset key was added or dropped'
    assert a == b, 'the promote changed something outside the one leaf'


def test_canonical_is_still_compact(post):
    raw = post_bytes()
    assert b'\n' not in raw, 'canonical gained a newline; it must stay COMPACT'
    assert raw == json.dumps(post, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


# --- non-vacuity ----------------------------------------------------------------------------

def test_MUTATION_the_cap_guard_catches_a_planted_long_name(post):
    b = copy.deepcopy(post)
    {c['slug']: c for c in b['crops']}['zinnia']['varieties']['recommended'][0] = 'x' * 120
    with pytest.raises(AssertionError):
        over = [(s, i) for s, i, e in every_entry(b) if len(display_name(e)) > NAME_CAP]
        assert not over


def test_MUTATION_the_blast_radius_guard_catches_a_stray_edit(pre, post):
    a, b = copy.deepcopy(pre), copy.deepcopy(post)
    {c['slug']: c for c in b['crops']}['tomatillo']['_drift'] = 1
    ca = {c['slug']: c for c in a['crops']}
    cb = {c['slug']: c for c in b['crops']}
    with pytest.raises(AssertionError):
        for slug in ca:
            if slug != P.CROP:
                assert ca[slug] == cb[slug], f'{slug} changed'


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
