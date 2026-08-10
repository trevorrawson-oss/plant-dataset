#!/usr/bin/env python3
"""trigger_prose_gate -- weather_triggers consumer-prose sanity (PLA-157, A52/A53).

The defect class (found by the PLA-138 instrument audit, filed as PLA-157): certified zinnia
shipped raw source ids ('clemson_hgic_1149') as `body_beginner`, a consumer-facing field, and
whole_crop_gate PASSED -- A29 checks the register is non-null and the compound gate checks it is
non-empty, and an identifier satisfies both. The gate validated the field's SHAPE and could not
see that the string is an id rather than prose.

Two checks, both measured against ce9eb12f before wiring:

  A52 identifier_prose_violations: a title_*/body_* value matching ^[a-z0-9_]+$ (no whitespace)
      is never valid consumer copy. Roster-wide the only hits are the 3 zinnia defects.
      SCOPE IS DELIBERATELY weather_triggers ONLY: a wider sweep over all *_seasoned/_beginner
      strings floods on legitimate enum fields (container_notes.soil_mix.type_seasoned =
      'container_potting_mix' on ~17 crops).

  A53 title_length_violations: a title slot holding body-length prose. Measured gap: the longest
      legitimate title roster-wide is 60 chars (grapefruit); the 6 defect values (zinnia 3,
      bee-balm 3) run 117-147. TITLE_MAX = 80 sits in the gap with headroom on both sides.
"""
import re

PROSE_KEYS = ('title_seasoned', 'title_beginner', 'body_seasoned', 'body_beginner')
TITLE_KEYS = ('title_seasoned', 'title_beginner')
TITLE_MAX = 80
_IDENT = re.compile(r'[a-z0-9_]+\Z')


def _triggers(crop):
    wt = crop.get('weather_triggers')
    if not isinstance(wt, list):
        return []
    return [(i, t) for i, t in enumerate(wt) if isinstance(t, dict)]


def identifier_prose_violations(crop):
    out = []
    for i, t in _triggers(crop):
        for k in PROSE_KEYS:
            v = t.get(k)
            if isinstance(v, str) and _IDENT.fullmatch(v):
                out.append(f'weather_triggers[{i}].{k} is identifier-shaped, not prose: {v!r}'
                           ' (PLA-157 defect class: a source id shipped as consumer copy)')
    return out


def title_length_violations(crop):
    out = []
    for i, t in _triggers(crop):
        for k in TITLE_KEYS:
            v = t.get(k)
            if isinstance(v, str) and len(v) > TITLE_MAX:
                out.append(f'weather_triggers[{i}].{k} is {len(v)} chars (max {TITLE_MAX}):'
                           f' body-length prose in a title slot: {v[:60]!r}...')
    return out
