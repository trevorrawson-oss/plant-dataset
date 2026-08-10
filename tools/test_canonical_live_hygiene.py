#!/usr/bin/env python3
"""LIVE canonical hygiene -- the checks the pinned suites can no longer make.

Three promote suites once asserted "canonical is still compact" against live canonical. When
their `post` fixtures were repointed to pinned SHAs (correctly -- later promotes had moved
things), those assertions collapsed into comparing hash-verified literals to themselves and
were deleted (PLA-162). This file is where the LIVE claim now lives, once, falsifiably:
whatever canonical currently is, it obeys the serialization contract in CLAUDE.md.
"""
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')


def _raw():
    with open(CANONICAL, 'rb') as fh:
        return fh.read()


def test_live_canonical_is_single_line_compact_with_no_trailing_newline():
    raw = _raw()
    assert b'\n' not in raw, 'canonical must be single-line compact'
    assert not raw.endswith(b'\n'), 'canonical must have no trailing newline'


def test_live_canonical_round_trips_through_the_ruled_serializer():
    """COMPACT means byte-reproducible: json.dumps with the ruled separators and
    ensure_ascii=False must reproduce the file exactly. This is the check that catches
    `indent=2`, ascii-escaping, and separator drift in one comparison."""
    raw = _raw()
    data = json.loads(raw)
    assert json.dumps(data, ensure_ascii=False,
                      separators=(',', ':')).encode('utf-8') == raw
