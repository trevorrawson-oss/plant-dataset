#!/usr/bin/env python3
"""Tests for trigger_prose_gate (PLA-157): identifier-shaped consumer prose + title length.

RED-fixture cases pin to ce9eb12f, the canonical where the zinnia defect is LIVE, via
promote_fixture -- so this suite keeps proving the gate catches the real defect class after the
promote moves canonical on. Synthetic cases inject the defect into other slots (body_seasoned,
title_seasoned) so the checks are shown to fire beyond the exact live instance -- the
guard-reachability lesson: a check that has only ever been argued from its docstring has fired
zero times.

Run: python3 tools/test_trigger_prose_gate.py   (or pytest)
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture  # noqa: E402
from trigger_prose_gate import (  # noqa: E402
    TITLE_MAX,
    identifier_prose_violations,
    title_length_violations,
)

BASE_SHA = 'ce9eb12fb85abf9f592ee8bc6621102a5dd785327a74befe2b0e7ddc8146bff5'
DATA = json.loads(promote_fixture.pre_state(BASE_SHA))


def crop(slug):
    return next(c for c in DATA['crops'] if c['slug'] == slug)


# T1. the LIVE defect: zinnia at ce9eb12f carries exactly 3 identifier-shaped body_beginner
# values, and the messages name the stray ids
v = identifier_prose_violations(crop('zinnia'))
assert len(v) == 3, f'zinnia identifier violations: {v}'
assert all('body_beginner' in m for m in v), v
assert sum('clemson_hgic_1149' in m for m in v) == 2, v
assert sum('uf_ifas_zinnia' in m for m in v) == 1, v

# T2. the LIVE title defect: zinnia and bee-balm each carry exactly 3 body-length
# title_beginner values; marigold (the healthy sibling ornamental) is clean on both checks
assert len(title_length_violations(crop('zinnia'))) == 3
assert len(title_length_violations(crop('bee-balm'))) == 3
assert all('title_beginner' in m for m in title_length_violations(crop('bee-balm')))
assert identifier_prose_violations(crop('bee-balm')) == []
assert identifier_prose_violations(crop('marigold')) == []
assert title_length_violations(crop('marigold')) == []

# T3. SCOPE: the gate reads only weather_triggers prose slots. carrot carries the legitimate
# enum container_notes.soil_mix.type_seasoned = 'container_potting_mix' (identifier-shaped by
# construction, on ~17 crops) -- a wider scan floods on it; this gate must not
carrot = crop('carrot')
assert carrot['container_notes']['soil_mix']['type_seasoned'] == 'container_potting_mix', \
    'fixture sanity: the enum this scope decision was measured against moved'
assert identifier_prose_violations(carrot) == []

# T4. synthetic injections: the identifier check fires on ANY of the four prose slots, not just
# the slot the live defect happens to occupy
HEALTHY = {
    'weather_triggers': [{
        'condition': 'high', 'severity': 'protect', 'action': 'Frost warning',
        'title_seasoned': 'Frost warning', 'title_beginner': 'Frost warning',
        'body_seasoned': 'Real prose, written for a reader.',
        'body_beginner': 'Real prose, written for a beginner.',
        'sources': ['some_src'], 'anchoring_urls': {},
    }],
}
assert identifier_prose_violations(HEALTHY) == []
assert title_length_violations(HEALTHY) == []
for slot in ('title_seasoned', 'title_beginner', 'body_seasoned', 'body_beginner'):
    mut = copy.deepcopy(HEALTHY)
    mut['weather_triggers'][0][slot] = 'clemson_hgic_9999'
    got = identifier_prose_violations(mut)
    assert len(got) == 1 and slot in got[0], f'{slot} injection missed: {got}'

# T5. title length boundary: TITLE_MAX passes, TITLE_MAX+1 fails, and the check reads BOTH
# title slots but neither body slot (bodies are legitimately long)
mut = copy.deepcopy(HEALTHY)
mut['weather_triggers'][0]['title_seasoned'] = 'x' * TITLE_MAX
assert title_length_violations(mut) == []
for slot in ('title_seasoned', 'title_beginner'):
    mut = copy.deepcopy(HEALTHY)
    mut['weather_triggers'][0][slot] = 'Cover plants before a cold night arrives. ' * 4
    got = title_length_violations(mut)
    assert len(got) == 1 and slot in got[0], f'{slot} length injection missed: {got}'
mut = copy.deepcopy(HEALTHY)
mut['weather_triggers'][0]['body_beginner'] = 'A perfectly legitimate long body sentence. ' * 5
assert title_length_violations(mut) == []

# T6. absent / null / non-list weather_triggers never crash (indoor crops carry none)
assert identifier_prose_violations({}) == []
assert title_length_violations({}) == []
assert identifier_prose_violations({'weather_triggers': None}) == []
assert title_length_violations({'weather_triggers': None}) == []

print('test_trigger_prose_gate: OK (6 groups)')
