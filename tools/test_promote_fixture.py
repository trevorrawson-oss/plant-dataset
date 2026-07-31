"""Tests for the promote-guard fixture resolver.

The resolver's whole job is to make promote guards impossible to silence. So the properties that
matter are: every reconstruction is hash-verified, a chained (never-committed) state rebuilds
byte-exactly, and an unresolvable SHA RAISES rather than skipping.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import promote_fixture as F  # noqa: E402

COMMITTED = '45409cee243da4196e983198c33505701d44f50842ffb208a224d0b22ddd817b'
CHAINED = '5f58654b1fceb057a37cfaec7c77ef5c5d6e3a8de69847781cf237da89121b20'


def test_committed_state_rebuilds_and_verifies():
    raw = F.pre_state(COMMITTED)
    assert hashlib.sha256(raw).hexdigest() == COMMITTED


def test_never_committed_intermediate_rebuilds_by_replay():
    """5f58654b was an intermediate state inside hunt 1 and is in no commit."""
    assert COMMITTED not in F.CHAIN, 'sanity: this one should come from a commit'
    assert CHAINED in F.CHAIN and CHAINED not in F.COMMIT_FOR
    raw = F.pre_state(CHAINED)
    assert hashlib.sha256(raw).hexdigest() == CHAINED


def test_rebuilt_state_is_real_canonical_not_a_stub():
    data = json.loads(F.pre_state(CHAINED))
    assert len(data['crops']) == 128
    assert any(c['slug'] == 'blueberry' for c in data['crops'])


def test_unknown_sha_raises_and_never_returns_a_substitute():
    try:
        F.pre_state('0' * 64)
    except AssertionError as e:
        assert 'never skip' in str(e)
    else:
        raise AssertionError('an unresolvable SHA must raise, not return a fixture')


def test_scratch_writes_the_pre_state_and_reports_its_sha():
    path, sha = F.scratch(COMMITTED)
    assert sha == COMMITTED
    with open(path, 'rb') as fh:
        assert hashlib.sha256(fh.read()).hexdigest() == COMMITTED


def test_scratch_mutation_changes_the_sha_so_defects_are_injectable():
    def drop_a_crop(_crops, data):
        data['crops'] = [c for c in data['crops'] if c['slug'] != 'blueberry']

    path, sha = F.scratch(COMMITTED, drop_a_crop)
    assert sha != COMMITTED
    with open(path, encoding='utf-8') as fh:
        assert not any(c['slug'] == 'blueberry' for c in json.load(fh)['crops'])


def test_output_stays_compact_after_mutation():
    path, _ = F.scratch(COMMITTED, lambda _c, _d: None)
    with open(path, 'rb') as fh:
        raw = fh.read()
    assert not raw.endswith(b'\n')
