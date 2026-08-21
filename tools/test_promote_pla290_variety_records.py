#!/usr/bin/env python3
"""Guards for the PLA-290 variety-record promote.

REPLAY-PINNED BOTH ENDS: the PRE state is rebuilt from git by hash and the POST state by
REPLAYING this promote on that fixture, so the suite never reads live canonical. It therefore
cannot go vacuous when canonical moves on ([[promote-guards-went-vacuous-on-sha-skip]] -- never
skip on a SHA mismatch, rebuild), and cannot redden on somebody else's later promote
([[promote-suite-post-must-be-replayed-not-live]]).

The blast-radius guard asserts KEY-SET EQUALITY BEFORE comparing any value, in both directions
([[blast-radius-guards-iterate-pre-only]]). This promote REPLACES list elements and ADDS dict
keys where there were bare strings, so a pre-only walk would be blind to exactly the thing most
worth watching -- an eleventh crop quietly converted, or a record gaining a fabricated field.

THE GUARD THAT MATTERS MOST is test_every_id_prefixes_its_stored_legacy_slug. plant-app's
PLA-291 shim bridges an already-planted variety id by dashed-prefix match, so an id that fails
that check does not merely look wrong -- it silently unplants a user's garden record.

Mutation evidence: tools/mutate_pla290_variety_suite.py
"""
import copy
import json
import os
import re
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import promote_fixture  # noqa: E402
import promote_pla290_variety_records as P  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'promote_pla290_variety_records.py')

_post = {}


def post_bytes():
    """The bytes THIS promote produces, by replaying it on the rebuilt pre-state -- never
    live canonical. A suite whose `post` is live canonical reddens on every FUTURE promote
    and stops testing its own ([[promote-suite-post-must-be-replayed-not-live]]); the PLA-253
    nematode suite was red for exactly that reason when this promote landed."""
    if 'raw' not in _post:
        path, sha = promote_fixture.scratch(P.BASE_SHA)
        assert sha == P.BASE_SHA
        r = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
        assert r.returncode == 0, f'replay failed: {(r.stdout + r.stderr)[-800:]}'
        _post['raw'] = open(path, 'rb').read()
    return _post['raw']

# beet[6] "Monogerm types (such as Moneta)" -> "Moneta is a common example." The two function
# words are the only tokens in all 59 entries that do not survive verbatim; enumerated here so
# the preservation guard stays exact instead of being loosened to a threshold.
ALLOWED_TOKEN_LOSS = {('beet', 6): {'such', 'as'}}


@pytest.fixture(scope='module')
def pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


@pytest.fixture(scope='module')
def post():
    return json.loads(post_bytes())


def recs(data, slug):
    return {c['slug']: c for c in data['crops']}[slug]['varieties']['recommended']


def all_records(data):
    for slug in P.CROPS:
        for i, r in enumerate(recs(data, slug)):
            yield slug, i, r


# --- the shape ------------------------------------------------------------------------------

def test_no_prose_string_survives_in_any_in_scope_crop(post):
    """The defect itself: a bare string in one of the ten crops means the app's legacy branch
    still runs and a sentence still reaches a card title."""
    for slug in P.CROPS:
        for i, entry in enumerate(recs(post, slug)):
            assert isinstance(entry, dict), f'{slug}[{i}] is still a {type(entry).__name__}'


def test_every_record_carries_exactly_id_name_note(post):
    """Minimally {id, name, note} -- and no more. A fabricated days_to_maturity would be
    invisible to a shape check that only asserted the three keys were PRESENT."""
    for slug, i, r in all_records(post):
        assert set(r) == {'id', 'name', 'note'}, f'{slug}[{i}] keys are {sorted(r)}'


def test_no_name_is_a_sentence(post):
    """The rendered symptom. A colon in a name is the exact shape that produced
    "Golden Self-Blanching: a compact, pale-stalked ..." on the Garden On Deck card."""
    for slug, i, r in all_records(post):
        assert ':' not in r['name'], f'{slug}[{i}] name still carries a colon: {r["name"]!r}'
        assert len(r['name']) <= 60, f'{slug}[{i}] name is {len(r["name"])} chars'


def test_the_celery_card_reads_as_a_name(post):
    """The reported screenshot, pinned as its own case."""
    golden = [r for r in recs(post, 'celery') if r['id'] == 'golden-self-blanching']
    assert len(golden) == 1
    assert golden[0]['name'] == 'Golden Self-Blanching'
    assert golden[0]['note'].startswith('A compact, pale-stalked')


# --- the id, which is a compatibility constraint --------------------------------------------

def test_every_id_prefixes_its_stored_legacy_slug(post):
    """plant-app PLA-291 Part A bridges a stored sentence-slug to the variety whose slug is a
    DASHED PREFIX of it. An id failing this does not render wrong, it unplants a real garden
    record -- so it is checked against the pre-promote prose, entry by entry."""
    for slug in P.CROPS:
        for prev_entry, r in zip(P.PREV_ENTRIES[slug], recs(post, slug)):
            legacy = P.slugify_variety(prev_entry)
            assert legacy.startswith(r['id'] + '-'), \
                f'{slug}/{r["id"]!r} strands the stored id {legacy!r}'


def test_every_id_equals_slugify_of_its_own_name(post):
    """plant-app resolves a variety slug two different ways: varieties.ts prefers v.id,
    build-guides-data.mjs slugifies v.name and never reads v.id. They agree only while this
    invariant holds; all 53 pre-existing records with an id satisfy it."""
    for slug, i, r in all_records(post):
        assert r['id'] == P.slugify_variety(r['name']), \
            f'{slug}[{i}] id {r["id"]!r} != slugify({r["name"]!r})'


def test_ids_are_unique_within_each_crop(post):
    """Identity is the (cropSlug, slug) pair -- build-guides-data.mjs throws on a duplicate."""
    for slug in P.CROPS:
        ids = [r['id'] for r in recs(post, slug)]
        assert len(set(ids)) == len(ids), f'{slug} has duplicate ids'
        assert all(ids), f'{slug} has an empty id'


def test_every_legacy_stored_id_still_resolves_to_its_OWN_record(post):
    """The end-to-end contract, not just the invariant behind it: plant-app's varietyFor()
    transcribed, run over every id a pre-PLA-290 planting could have stored, asserting it
    lands on THAT entry's record and not merely on some record. A prefix check alone cannot
    see an id swap between two entries of the same crop."""
    def variety_for(records, stored):
        for v in records:
            if v['id'] == stored:
                return v
        best = None
        for v in records:
            if stored.startswith(v['id'] + '-') and len(v['id']) > (len(best['id']) if best else 0):
                best = v
        return best

    for slug in P.CROPS:
        records = recs(post, slug)
        for i, prose in enumerate(P.PREV_ENTRIES[slug]):
            stored = P.slugify_variety(prose)
            hit = variety_for(records, stored)
            assert hit is not None, f'{slug}[{i}] stored id {stored!r} resolves to nothing'
            assert hit['id'] == records[i]['id'], \
                f'{slug}[{i}] stored id resolves to {hit["id"]!r}, not {records[i]["id"]!r}'


def test_no_id_prefixes_a_DIFFERENT_entrys_legacy_slug(post):
    """The shim takes the LONGEST dashed-prefix match. If one record's id also prefixed another
    record's stored id, a planting could silently resolve to the wrong variety."""
    for slug in P.CROPS:
        legacy = [P.slugify_variety(e) for e in P.PREV_ENTRIES[slug]]
        ids = [r['id'] for r in recs(post, slug)]
        for a, vid in enumerate(ids):
            for b, leg in enumerate(legacy):
                if a != b:
                    assert not leg.startswith(vid + '-'), \
                        f'{slug}: id {vid!r} also claims entry {b}'


# --- the note -------------------------------------------------------------------------------

def test_every_note_is_a_finished_sentence(post):
    for slug, i, r in all_records(post):
        assert r['note'], f'{slug}[{i}] has an empty note'
        assert r['note'][0].isupper(), f'{slug}[{i}] note is not capitalized'
        assert r['note'].endswith('.'), f'{slug}[{i}] note has no terminal period'


def test_no_em_dash_in_the_consumer_copy(post):
    for slug, i, r in all_records(post):
        assert '—' not in r['name'] and '—' not in r['note'], f'{slug}[{i}] has an em dash'


def test_no_word_of_the_original_prose_was_dropped(post):
    """A restructure must not become a rewrite. Every alphanumeric token of all 59 originals
    has to survive into name+note, with the one enumerated exception."""
    for slug in P.CROPS:
        for i, (prev_entry, r) in enumerate(zip(P.PREV_ENTRIES[slug], recs(post, slug))):
            was = set(re.findall(r'[a-z0-9]+', prev_entry.lower()))
            now = set(re.findall(r'[a-z0-9]+', (r['name'] + ' ' + r['note']).lower()))
            lost = was - now - ALLOWED_TOKEN_LOSS.get((slug, i), set())
            assert not lost, f'{slug}[{i}] dropped {sorted(lost)}'


def test_no_days_to_maturity_was_invented(post):
    """Ten notes carry a DTM as prose ("about 90 to 100 days"). None of these entries was ever
    sourced for one, and a range cannot be narrowed to the integer the field takes without
    inventing precision."""
    for slug, i, r in all_records(post):
        assert 'days_to_maturity' not in r, f'{slug}[{i}] gained a days_to_maturity'


# --- nasturtium, which is NOT converted -----------------------------------------------------

def test_the_marigold_artifact_is_gone_from_nasturtium(post):
    entry = recs(post, P.NASTURTIUM)[P.NAST_INDEX]
    assert 'Tagetes' not in entry, 'the copy-paste genus is still there'
    assert entry == P.NAST_NEW


def test_nasturtium_stays_a_string_crop(pre, post):
    """Its trailing-paren shape parses correctly today; converting it was not in scope, and
    converting it silently would change every nasturtium variety slug."""
    for i, entry in enumerate(recs(post, P.NASTURTIUM)):
        assert isinstance(entry, str), f'nasturtium[{i}] was converted'
    assert recs(post, P.NASTURTIUM)[1:] == recs(pre, P.NASTURTIUM)[1:]


def test_the_nasturtium_edit_did_not_move_its_variety_slug(pre, post):
    """The app slugs a string entry from the name BEFORE the parenthetical. Editing inside the
    parens must leave that name, and therefore every stored planting id, untouched."""
    def head(s):
        m = re.match(r'^(.+?)\s+\(([^)]+)\)$', s)
        return m.group(1) if m else s
    a = head(recs(pre, P.NASTURTIUM)[P.NAST_INDEX])
    b = head(recs(post, P.NASTURTIUM)[P.NAST_INDEX])
    assert a == b == 'Jewel series'
    assert P.slugify_variety(a) == P.slugify_variety(b)


# --- blast radius ---------------------------------------------------------------------------

def test_the_other_string_shape_crops_were_not_converted(pre, post):
    """basil, the tomatoes and the flowers carry trailing-paren strings the app parses fine.
    Converting them would be a different decision with its own id migration."""
    a = {c['slug']: c for c in pre['crops']}
    b = {c['slug']: c for c in post['crops']}
    for slug in a:
        if slug in P.CROPS or slug == P.NASTURTIUM:
            continue
        assert (a[slug].get('varieties') or {}).get('recommended') == \
            (b[slug].get('varieties') or {}).get('recommended'), f'{slug} varieties moved'


def test_nothing_outside_the_eleven_crops_moved(pre, post):
    """Key sets FIRST, both directions, then values."""
    a, b = copy.deepcopy(pre), copy.deepcopy(post)
    ca = {c['slug']: c for c in a['crops']}
    cb = {c['slug']: c for c in b['crops']}
    assert set(ca) == set(cb), 'the crop roster changed'
    touched = set(P.CROPS) | {P.NASTURTIUM}
    for slug in ca:
        if slug not in touched:
            assert ca[slug] == cb[slug], f'{slug} changed'

    # the touched crops: only varieties.recommended may differ
    for slug in touched:
        assert set(ca[slug]) == set(cb[slug]), f'{slug} gained or lost a top-level key'
        assert set(ca[slug]['varieties']) == set(cb[slug]['varieties']), \
            f'{slug}.varieties gained or lost a key'
        ca[slug]['varieties']['recommended'] = cb[slug]['varieties']['recommended']
        assert ca[slug] == cb[slug], f'{slug} changed outside varieties.recommended'

    assert set(a) == set(b), 'a top-level dataset key was added or dropped'
    assert a == b, 'the promote changed something outside the eleven crops'


def test_no_entry_count_changed(pre, post):
    """One record per entry -- the shim's prefix rule cannot survive a split or a merge."""
    for slug in set(P.CROPS) | {P.NASTURTIUM}:
        assert len(recs(pre, slug)) == len(recs(post, slug)), f'{slug} changed entry count'


def test_canonical_is_still_compact(post):
    raw = post_bytes()
    assert b'\n' not in raw, 'canonical gained a newline; it must stay COMPACT'
    assert raw == json.dumps(post, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


# --- non-vacuity ----------------------------------------------------------------------------

def test_MUTATION_the_blast_radius_guard_catches_a_stray_edit(pre, post):
    a, b = copy.deepcopy(pre), copy.deepcopy(post)
    cb = {c['slug']: c for c in b['crops']}
    cb['tomatillo']['description_beginner'] = 'SABOTAGE'
    ca = {c['slug']: c for c in a['crops']}
    with pytest.raises(AssertionError):
        for slug in ca:
            if slug not in set(P.CROPS) | {P.NASTURTIUM}:
                assert ca[slug] == cb[slug], f'{slug} changed'


def test_MUTATION_the_shim_guard_catches_a_stranded_id(post):
    """A plausible-looking id that would unplant a garden record must redden the prefix check."""
    with pytest.raises(AssertionError):
        legacy = P.slugify_variety(P.PREV_ENTRIES['carrot'][0])
        assert legacy.startswith('scarlet-nantes' + '-')


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
