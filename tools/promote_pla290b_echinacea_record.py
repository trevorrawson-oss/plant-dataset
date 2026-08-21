#!/usr/bin/env python3
"""PLA-290 follow-on: echinacea's interspecific-hybrid entry becomes a record. Base 2d496da5.

THE SAME DEFECT FAMILY AS PLA-290, THE OTHER VARIANT. PLA-290 converted the ten crops whose
entries were colon-format prose. This is the one remaining entry whose PARENTHETICAL sits
MID-STRING, so plant-app's legacy branch -- which splits only a TRAILING parenthetical,
`^(.+?)\\s+\\(([^)]+)\\)$` -- does not match it either, and all 228 characters become the
variety's display name.

Found by plant-app's new dataset-shape tripwire (PLA-291 Part B) once PLA-290's regenerated
data let it run. Measured here before acting, not taken from the report: of **756 variety
entries roster-wide, this is the ONLY one whose app display name exceeds 70 characters** --
the next longest is 59 -- and **0** display names still contain a colon. So the cap holds at
70 with zero exceptions after this, with real headroom.

WHAT THIS DOES. One leaf: `echinacea.varieties.recommended[6]`, string -> `{id, name, note}`.

THE ID IS THE SAME COMPATIBILITY CONSTRAINT PLA-290 ESTABLISHED. plant-app's `varietyFor()`
bridges an already-planted record by DASHED-PREFIX match on the stored slug, and today's
stored slug is the whole 228-char sentence slugified. `interspecific-hybrid-color-series`
prefixes it, so any existing planting still resolves; and `id == slugify(name)` keeps
`varieties.ts` and `build-guides-data.mjs` agreeing.

THE SPLIT IS AUTHORED, NOT MECHANICAL, because there is no colon to split on: the sentence
runs THROUGH its parenthetical and out the other side ("...'Tiki Torch') in orange, red,
yellow, and doubles; showy but..."). The cultivar list and the color list both belong in the
note. A token guard asserts every word of the original survives into name+note.

ECHINACEA'S OTHER SIX ENTRIES ARE DELIBERATELY LEFT AS STRINGS. Each is a clean trailing
parenthetical that the app parses correctly, and PLA-290 ruled that family out of scope. The
crop is therefore left with a MIXED array -- one record, six strings -- which all three
consumers handle per-entry (`plant-app varieties.ts`, `build-guides-data.mjs`, and
plant-astro's `parseVariety` each branch on the type of each element). Converting the other
six would be shim-safe, because their slugs already come from the paren-head and would not
move; it is simply not this change.

Guard suite: tools/test_promote_pla290b_echinacea_record.py
Mutation harness: tools/mutate_pla290b_echinacea_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla290b_echinacea_record.py [--canonical PATH] [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')


def slugify_variety(name):
    """plant-app's rule, character for character (varieties.ts + build-guides-data.mjs).

    Defined here rather than imported from `promote_pla290_variety_records`, deliberately. A
    promote script is a pinned historical artifact; one importing another couples two frozen
    records so that editing the older one silently changes what the newer one did. The guard
    suite asserts this function and PLA-290's agree over the whole live corpus, which catches
    drift without creating the coupling.
    """
    s = re.sub(r"['’!.]", '', name.lower())
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

BASE_SHA = '2d496da51b37c68a60402b82cc30a5252d07e45474b6b98edaf299afbc5c69c4'

CROP = 'echinacea'
INDEX = 6

PREV_ENTRY = ("Interspecific hybrid color series (for example Big Sky, Conefections, Sombrero, "
              "'Hot Papaya', 'Tiki Torch') in orange, red, yellow, and doubles; showy but often "
              "shorter-lived and less reliably perennial than the straight species")

RECORD = {
    'id': 'interspecific-hybrid-color-series',
    'name': 'Interspecific hybrid color series',
    'note': ("For example Big Sky, Conefections, Sombrero, 'Hot Papaya', and 'Tiki Torch', in "
             "orange, red, yellow, and doubles. Showy but often shorter-lived and less reliably "
             "perennial than the straight species."),
}


def apply_to(data):
    """The whole transform, as one function, so the guard suite exercises the code the promote
    runs rather than a re-implementation of it."""
    by = {c['slug']: c for c in data['crops']}
    by[CROP]['varieties']['recommended'][INDEX] = dict(RECORD)
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    ap.add_argument('--canonical', dest='canonical_flag', default=None)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    canonical = args.canonical_flag or args.canonical

    raw = open(canonical, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        print(f'ABORT: base SHA mismatch\n  expected {args.expect_sha}\n  found    {sha}',
              file=sys.stderr)
        return 1

    data = json.loads(raw.decode('utf-8'))
    by = {c['slug']: c for c in data['crops']}
    crop = by.get(CROP)
    if crop is None:
        print(f'ABORT: no crop {CROP!r}', file=sys.stderr)
        return 1
    rec = (crop.get('varieties') or {}).get('recommended') or []
    if len(rec) <= INDEX or rec[INDEX] != PREV_ENTRY:
        print(f'ABORT: {CROP}.varieties.recommended[{INDEX}] is not the entry this promote was '
              f'written against\n  found: {rec[INDEX] if len(rec) > INDEX else "(missing)"!r}',
              file=sys.stderr)
        return 1

    # The compatibility constraint, re-checked at run time rather than trusted from authoring.
    legacy = slugify_variety(PREV_ENTRY)
    if not legacy.startswith(RECORD['id'] + '-'):
        print(f'ABORT: {RECORD["id"]!r} would strand the stored id {legacy!r}', file=sys.stderr)
        return 1
    if RECORD['id'] != slugify_variety(RECORD['name']):
        print(f'ABORT: id != slugify({RECORD["name"]!r})', file=sys.stderr)
        return 1

    apply_to(data)
    print(f'{CROP}.varieties.recommended[{INDEX}]: {len(PREV_ENTRY)}-char prose string -> '
          f'{{id, name, note}}')
    print(f'  name: {RECORD["name"]!r} ({len(RECORD["name"])} chars)')
    print(f'  id:   {RECORD["id"]!r}')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN -- would write {len(out)} bytes, sha {new_sha}')
        return 0
    with open(canonical, 'wb') as fh:
        fh.write(out)
    print(f'wrote {len(out)} bytes\nnew canonical SHA: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
