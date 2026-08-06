#!/usr/bin/env python3
"""Guards for PLA-114 Task 2: the mis-credited parenthetical. Base 29b96b65.

RED BEFORE GREEN: every check asserts the POST state, so the suite fails on the pre-state.

THE DELICATE PART. `hardiness_notes_seasoned` is ONE OF THE FOURTEEN strings the previous promote
pinned byte-identical, and this promote edits it. That is not the pin being abandoned -- the pin's
stated purpose is "so a later pass cannot 'fix' correct copy", and the correct copy is the
stage-aware CLAIM, not the source credit appended after it. So the pin is NARROWED rather than
dropped: everything before " (Sources:" must still be byte-identical to `6b2dcb8e`, and the other
thirteen strings stay whole-string identical. A guard that simply stopped checking this field
would hand the next pass exactly the licence the pin exists to deny.
"""
import hashlib
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture  # noqa: E402
import test_promote_pla114_lemon_cold as prev  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.environ.get('PLA114B_CANONICAL', os.path.join(REPO, 'crops_data_final.json'))

BASE_SHA = '29b96b65a0969a8ad654762b5d84276bafbd2a8747706cb512ed1414305abf6f'
ORIGINAL_SHA = '6b2dcb8ed4f51c833fa4d44845b15e7f609079a24a544af025c067dfca45d4db'

OLD_TAIL = ' (Sources: Clemson HGIC, Texas A&M AgriLife, UF/IFAS.)'
NEW_TAIL = (' (Sources: cold-damage temperatures UC ANR 8100 and UF/IFAS HS1153; cold-hardiness '
            'ranking and freeze protection Clemson HGIC and Texas A&M AgriLife.)')

F1 = 'lemon_cold_threshold_was_miscredited_now_uc8100'
CORRECTION_TOKEN = '[CORRECTION 2026-08-06:'


def _crop(data, slug='lemon'):
    return next(c for c in data['crops'] if c['slug'] == slug)


def _f1(data):
    return next(f for f in _crop(data)['verification_status']['open_findings'] if f['id'] == F1)


# Pinned to the state THIS promote produced, `bce8bcc7`, for the same reason as its predecessor:
# the §7 promote landed on top of it and legitimately moved things these guards assert did not
# move. The mutation harness still overrides via PLA114B_CANONICAL.
POST_SHA = 'bce8bcc72aeebb42269b2d96310b427d9502a3670241ca7621e91810588f16cd'


@pytest.fixture(scope='module')
def post():
    override = os.environ.get('PLA114B_CANONICAL')
    if override:
        with open(override, 'rb') as fh:
            return json.loads(fh.read())
    return json.loads(promote_fixture.pre_state(POST_SHA))


@pytest.fixture(scope='module')
def pre():
    return json.loads(promote_fixture.pre_state(BASE_SHA))


@pytest.fixture(scope='module')
def original():
    """`6b2dcb8e` -- the state the fourteen strings were pinned against in the first place."""
    return json.loads(promote_fixture.pre_state(ORIGINAL_SHA))


# --- the credit itself --------------------------------------------------------------------------

def test_the_new_credit_is_exact(post):
    assert _crop(post)['hardiness_notes_seasoned'].endswith(NEW_TAIL)


def test_the_miscredit_is_gone(post):
    assert OLD_TAIL not in _crop(post)['hardiness_notes_seasoned']


def test_the_pre_state_carried_the_miscredit(pre):
    """Non-vacuity: if the pre-state did not carry it, the two checks above prove nothing."""
    assert _crop(pre)['hardiness_notes_seasoned'].endswith(OLD_TAIL)


def test_the_temperature_sources_are_named_for_the_temperature(post):
    """UC 8100 publishes the 29F onset; HS1153/HS402 publishes four lemon-specific figures."""
    tail = _crop(post)['hardiness_notes_seasoned'][-len(NEW_TAIL):]
    assert 'UC ANR 8100' in tail and 'UF/IFAS HS1153' in tail
    before_semicolon = tail.split(';')[0]
    assert 'Clemson' not in before_semicolon and 'Texas A&M' not in before_semicolon, (
        'Clemson and TAMU must not sit in the temperature clause -- neither publishes the number')


def test_clemson_and_tamu_are_KEPT_for_what_they_do_support(post):
    """[[never-blanket-a-reason-across-crops]] -- they support the ranking and the protection
    advice (TAMU's cold-hardy list excludes lemon; Clemson's 15F hardiest-citrus figure), so a
    blanket strip would have been its own mis-citation in the opposite direction."""
    tail = _crop(post)['hardiness_notes_seasoned'][-len(NEW_TAIL):]
    assert 'Clemson HGIC' in tail and 'Texas A&M AgriLife' in tail


def test_bare_uf_ifas_became_specific(post):
    """"UF/IFAS" alone does not disambiguate -- the crop cites HS1153 AND HS132."""
    tail = _crop(post)['hardiness_notes_seasoned'][-len(NEW_TAIL):]
    assert 'UF/IFAS HS1153' in tail
    assert 'UF/IFAS.' not in tail and 'UF/IFAS,' not in tail


# --- the narrowed pin: the CLAIM text may not move ----------------------------------------------

def test_the_claim_text_is_byte_identical_to_the_ORIGINAL_pin(original, post):
    """Everything before the credit must match `6b2dcb8e`, not merely the previous promote."""
    def claim(data):
        return _crop(data)['hardiness_notes_seasoned'].split(' (Sources:')[0]
    assert claim(post) == claim(original)


def test_the_claim_text_still_carries_the_stage_aware_wording(post):
    """The wording an earlier draft wanted to rewrite. It was correct; it must survive verbatim."""
    claim = _crop(post)['hardiness_notes_seasoned']
    assert 'leaves and fruit are damaged when temperatures fall into the high 20s F' in claim
    assert 'a hard freeze can kill an unprotected young tree to the ground' in claim


@pytest.mark.parametrize('path', [p for p in prev.CONFLATION_PATHS
                                  if p != ('crop', 'hardiness_notes_seasoned')],
                         ids=lambda p: '.'.join(map(str, p)))
def test_the_other_THIRTEEN_strings_are_whole_string_identical(original, post, path):
    assert prev._resolve(_crop(post), path) == prev._resolve(_crop(original), path)


def test_exactly_thirteen_others_are_covered():
    """Non-vacuity: if the exclusion filter silently emptied, the parametrize above would vanish."""
    others = [p for p in prev.CONFLATION_PATHS if p != ('crop', 'hardiness_notes_seasoned')]
    assert len(others) == 13, others


# --- F1 gets a correction APPENDED, never a rewrite ----------------------------------------------

def test_f1_carries_a_dated_correction(post):
    assert CORRECTION_TOKEN in _f1(post)['summary']


def test_f1s_original_text_survives_byte_for_byte(pre, post):
    """Append-don't-rewrite: the record of what was believed must not be edited into current tense."""
    before = _f1(pre)['summary']
    after = _f1(post)['summary']
    assert after.startswith(before), 'F1 was rewritten rather than appended to'


def test_the_correction_names_what_is_no_longer_true(post):
    """A correction that does not say what changed is decoration."""
    correction = _f1(post)['summary'][len(_f1(post)['summary'].split(CORRECTION_TOKEN)[0]):]
    assert 'UC ANR 8100' in correction
    assert 'Clemson' in correction and 'Texas A&M' in correction


# --- nothing else moved --------------------------------------------------------------------------

def test_the_previous_promote_still_holds(post):
    """Regression: value, catalog id and every repoint from `ae15df4` must survive untouched."""
    assert _crop(post)['frost_tolerance_f'] == 29
    assert 'uc_anr_8100' in post['source_catalog']
    cells = _crop(post)['regions']
    assert cells['northern_tier']['resolved_by_zone']['3']['anchoring_urls']['clemson_hgic']['url'] \
        == 'https://hgic.clemson.edu/cold-tolerance-in-citrus/'
    assert cells['ca_interior']['resolved_by_zone']['8']['anchoring_urls']['uc_ipm']['url'] \
        == 'https://ipm.ucanr.edu/home-and-landscape/freezing-and-frost-damage-to-citrus/'


def test_only_two_strings_moved_on_lemon(pre, post):
    """COVERAGE: enumerate every changed string on lemon; exactly two are permitted."""
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
    strings(_crop(pre), before)
    strings(_crop(post), after)
    moved = {k for k in before if before.get(k) != after.get(k)}
    assert moved == {'.hardiness_notes_seasoned',
                     '.verification_status.open_findings[4].summary'}, sorted(moved)


def test_no_other_crop_changed(pre, post):
    pre_by = {c['slug']: c for c in pre['crops']}
    post_by = {c['slug']: c for c in post['crops']}
    changed = [s for s in pre_by
               if json.dumps(pre_by[s], ensure_ascii=False, sort_keys=True)
               != json.dumps(post_by[s], ensure_ascii=False, sort_keys=True)]
    assert changed == ['lemon'], changed


def test_top_level_is_untouched(pre, post):
    for key in pre:
        if key == 'crops':
            continue
        assert json.dumps(pre[key], sort_keys=True) == json.dumps(post[key], sort_keys=True), key


def test_canonical_is_still_compact():
    raw = promote_fixture.pre_state(POST_SHA)
    assert b'\n' not in raw and not raw.endswith(b'\n')


def test_the_promote_actually_ran():
    got = hashlib.sha256(promote_fixture.pre_state(POST_SHA)).hexdigest()
    assert got != BASE_SHA, 'the post state is the pre-state'


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
