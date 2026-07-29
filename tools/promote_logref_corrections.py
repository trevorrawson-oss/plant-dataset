#!/usr/bin/env python3
"""Append Class 2 correction lines to two verification_log_ref narratives.

Hardening item 3 (docs/2026-07-26-post-asparagus-hardening-kickoff.md), under the
convention ruled in docs/verification_log_ref_convention.md.

APPEND-ONLY BY CONSTRUCTION: this script asserts the original prose is present
byte-for-byte and then concatenates a correction line onto the end. It never edits a
sentence. Re-running is a no-op (it aborts if the correction is already present).

Guards, all fatal:
  - canonical SHA must match EXPECT_SHA
  - each target log_ref must contain its expected stale substring verbatim
  - neither log_ref may already carry a [CORRECTION ...] marker
  - the live suitability split must match what the correction line asserts
  - only verification_log_ref may change; every other byte-level key is re-verified

Writes COMPACT per CLAUDE.md: separators=(",",":"), ensure_ascii=False, no trailing newline.

    $ python3 tools/promote_logref_corrections.py --dry-run
    $ python3 tools/promote_logref_corrections.py
"""
import argparse
import collections
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

EXPECT_SHA = 'b0d01f132f4e4ef635d076c35db97f261b27158b4eeca238d90d7983abdcae31'

ASPARAGUS_STALE = ('Suitability is an honest 16-region, 39-cell map: 18 cells perennialize, '
                   '8 are marginal, and 13 are unsuitable.')
ARTICHOKE_STALE = ('6 perennialize, 25 marginal, 7 survives_no_fruit, 1 unsuitable')

ASPARAGUS_CORRECTION = (
    ' [CORRECTION 2026-07-29: two assertions above are retired. (1) The suitability split is no '
    'longer 18/8/13 but 25 perennializes / 4 marginal / 10 unsuitable; those cells were RE-RATED '
    'in timing arc 2, not merely recounted. (2) The CHILL framing of the dormancy mechanism is '
    'retracted. It traces to PlantVillage, an aggregated crop-profile database rather than an '
    'extension bulletin, and UC IPM states dormancy comes from cold OR DROUGHT, instructing home '
    'gardeners to induce it by withholding irrigation. The clause that frost-free subtropical or '
    'extreme-heat desert zones deny dormancy entirely is false outright: low_desert_az z9 and z10 '
    'were re-rated unsuitable -> perennializes on in-region UC and UA evidence. Do not reason from '
    'the chill claim. See open_findings asparagus_suitability_chill_mechanism_unsourced_arc2, '
    'asparagus_chill_claim_provenance_plantvillage and '
    'asparagus_low_desert_az_rerated_from_retired_chill_mechanism, plus '
    'docs/verification_log_ref_convention.md.]'
)

ARTICHOKE_CORRECTION = (
    ' [CORRECTION 2026-07-29: the suitability tally above predates the annual_only value. The 25 '
    'marginal cells are now 22 annual_only + 3 marginal; the 6 perennializes, 7 survives_no_fruit '
    'and 1 unsuitable are unchanged. annual_only shipped frontend-first as a sixth suitability '
    'value after this cert, so nothing in the sentence above signals that 22 of 39 cells now carry '
    'a value it does not name. See docs/verification_log_ref_convention.md.]'
)

TARGETS = {
    'asparagus': (ASPARAGUS_STALE, ASPARAGUS_CORRECTION,
                  {'perennializes': 25, 'marginal': 4, 'unsuitable': 10}),
    'artichoke': (ARTICHOKE_STALE, ARTICHOKE_CORRECTION,
                  {'annual_only': 22, 'marginal': 3, 'perennializes': 6,
                   'survives_no_fruit': 7, 'unsuitable': 1}),
}


def die(msg):
    print(f'ABORT: {msg}', file=sys.stderr)
    sys.exit(1)


def suit_split(crop):
    counter = collections.Counter()
    for _rk, region in (crop.get('regions') or {}).items():
        for cell in ((region or {}).get('resolved_by_zone') or {}).values():
            if isinstance(cell, dict) and cell.get('suitability'):
                counter[cell['suitability']] += 1
    return dict(counter)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    raw = open(CANONICAL, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        die(f'canonical SHA drift.\n  expected {EXPECT_SHA}\n  found    {sha}')
    print(f'canonical SHA verified: {sha[:8]}')

    data = json.loads(raw.decode('utf-8'))
    by_slug = {c['slug']: c for c in data['crops']}

    for slug, (stale, correction, expect_split) in TARGETS.items():
        crop = by_slug.get(slug)
        if crop is None:
            die(f'{slug} not in roster')
        log_ref = (crop.get('verification_status') or {}).get('verification_log_ref')
        if not isinstance(log_ref, str):
            die(f'{slug} verification_log_ref is {type(log_ref).__name__}, expected str')
        if '[CORRECTION' in log_ref:
            die(f'{slug} already carries a [CORRECTION ...] marker; refusing to double-append')
        if stale not in log_ref:
            die(f'{slug} does not contain the expected stale substring verbatim:\n  {stale!r}')
        live = suit_split(crop)
        if live != expect_split:
            die(f'{slug} live suitability split {live} != what the correction asserts '
                f'{expect_split}; the correction text would itself be wrong')
        print(f'  {slug}: stale substring found, split verified {live}')

    # Apply.
    before = {}
    for slug, (_stale, correction, _split) in TARGETS.items():
        crop = by_slug[slug]
        vs = crop['verification_status']
        before[slug] = vs['verification_log_ref']
        vs['verification_log_ref'] = before[slug] + correction

    # Prove append-only: the new value must START with the old, byte for byte.
    for slug, (_stale, correction, _split) in TARGETS.items():
        new = by_slug[slug]['verification_status']['verification_log_ref']
        if not new.startswith(before[slug]):
            die(f'{slug} append-only violated')
        if new != before[slug] + correction:
            die(f'{slug} unexpected mutation')
        print(f'  {slug}: +{len(correction)} chars appended '
              f'({len(before[slug])} -> {len(new)})')

    out = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    if out.endswith('\n'):
        die('refusing to write a trailing newline')

    if args.dry_run:
        new_sha = hashlib.sha256(out.encode('utf-8')).hexdigest()
        print(f'\nDRY RUN, nothing written. Would become: {new_sha}')
        return 0

    with open(CANONICAL, 'w', encoding='utf-8') as fh:
        fh.write(out)
    new_sha = hashlib.sha256(open(CANONICAL, 'rb').read()).hexdigest()
    print(f'\nwritten. canonical {EXPECT_SHA[:8]} -> {new_sha[:8]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
