#!/usr/bin/env python3
"""GUARDED PROMOTE: artichoke's open_findings sit at the top level, where nothing reads them.

Trevor-ruled 2026-07-31 (the "unblocked and cheap" cleanup batch).

THE DEFECT. Artichoke is the ONLY crop of 128 that stores findings as `crop["open_findings"]`.
120 crops use `verification_status.open_findings`; the other 7 are uncertified shells with
neither. Every gate and scan reads the nested key -- `whole_crop_gate` line 1062 is
`vs.get("open_findings") or []` -- so artichoke's 12 findings are invisible, and every
roster-wide finding count in this repo is short by one crop. The external blind audit's
768-findings figure and the 62-crops-with-unfinished-findings figure both exclude artichoke.

ORIGIN, found in source rather than inferred: `tools/promote_artichoke.py` line 340 writes
`crop["open_findings"] = copy.deepcopy(prose.OPEN_FINDINGS)`. The cert promote wrote the wrong
path. A bug, not an archetype choice -- asparagus, the other herbaceous perennial, uses the
nested key.

NOT AN EMERGENCY, and the guard says so out loud: all 12 findings are `status: accepted` with
`blocks_launch: false`, so nothing that would have blocked certification was being hidden. The
cost is measurement integrity, not a shipped defect.

SCOPE IS RELOCATION ONLY. Artichoke's entries also use `title` + `note_internal` where the
roster uses `summary`. That divergence is REAL but is NOT fixed here: `summary` is read by no
gate and no general scan (only by one-off promote scripts pinned to a named finding, and
`promote_hardening_item2` already falls back to another key), so normalizing it is a separate
ruling. The 12 entries move byte-for-byte; the guard fails if a single character changes.

    $ python3 tools/promote_artichoke_findings_key.py --dry-run
    $ python3 tools/promote_artichoke_findings_key.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '172e4e7af950f0b98bf7883f5386c2b701a9d88f4d4347fc30d520cce7e91298'

SLUG = 'artichoke'
EXPECTED_FINDINGS = 12
EXPECTED_NESTED_BEFORE = 120


def _fail(msg):
    print('ABORT: %s' % msg)
    return 2


def relocate(data):
    """Move the top-level findings list under verification_status. Returns `data`."""
    for crop in data['crops']:
        if crop.get('slug') != SLUG:
            continue
        vs = crop.get('verification_status')
        if not isinstance(vs, dict):
            raise SystemExit('ABORT: %s has no verification_status dict' % SLUG)
        vs['open_findings'] = crop.pop('open_findings')
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--canonical', default=CANON)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error('pass --dry-run or --apply')

    with open(args.canonical, 'rb') as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        return _fail('canonical drifted.\n  expected %s\n  found    %s' % (args.expect_sha, sha))
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    before = copy.deepcopy(data)

    # ---- preflight -----------------------------------------------------------
    top = [c for c in data['crops'] if 'open_findings' in c]
    if len(top) != 1 or top[0]['slug'] != SLUG:
        return _fail('expected exactly one crop with a top-level open_findings (%s), got %s'
                     % (SLUG, [c['slug'] for c in top]))
    art = top[0]
    if len(art['open_findings']) != EXPECTED_FINDINGS:
        return _fail('expected %d findings, found %d'
                     % (EXPECTED_FINDINGS, len(art['open_findings'])))
    vs = art.get('verification_status')
    if not isinstance(vs, dict):
        return _fail('%s has no verification_status dict to move into' % SLUG)
    if 'open_findings' in vs:
        return _fail('%s ALREADY has verification_status.open_findings -- refusing to merge '
                     'or clobber' % SLUG)
    nested_before = sum(1 for c in data['crops']
                        if 'open_findings' in (c.get('verification_status') or {}))
    if nested_before != EXPECTED_NESTED_BEFORE:
        return _fail('expected %d crops with the nested key, found %d'
                     % (EXPECTED_NESTED_BEFORE, nested_before))
    blockers = [f for f in art['open_findings'] if f.get('blocks_launch')]
    print('verified: %d findings, all top-level, %d blocks_launch (nested key absent)'
          % (len(art['open_findings']), len(blockers)))

    # ---- apply ---------------------------------------------------------------
    relocate(data)

    # ---- the move is byte-for-byte -------------------------------------------
    b_art = next(c for c in before['crops'] if c['slug'] == SLUG)
    a_art = next(c for c in data['crops'] if c['slug'] == SLUG)
    if 'open_findings' in a_art:
        return _fail('top-level key survived the move')
    moved = (a_art.get('verification_status') or {}).get('open_findings')
    if moved != b_art['open_findings']:
        return _fail('findings were MODIFIED during relocation; this pass only moves them')
    nested_after = sum(1 for c in data['crops']
                       if 'open_findings' in (c.get('verification_status') or {}))
    if nested_after != EXPECTED_NESTED_BEFORE + 1:
        return _fail('expected %d crops with the nested key after, found %d'
                     % (EXPECTED_NESTED_BEFORE + 1, nested_after))

    # ---- footprint: artichoke only, and only this one key --------------------
    b = {c['slug']: c for c in before['crops']}
    a = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in b if b[s] != a[s])
    if changed != [SLUG]:
        return _fail('crops changed = %s, expected [%s]' % (changed, SLUG))
    if set(b_art) - {'open_findings'} != set(a_art):
        return _fail('artichoke top-level key set changed beyond the removal')
    for k in set(a_art) - {'verification_status'}:
        if b_art[k] != a_art[k]:
            return _fail('artichoke.%s moved' % k)
    b_vs, a_vs = b_art['verification_status'], a_art['verification_status']
    if set(b_vs) | {'open_findings'} != set(a_vs):
        return _fail('verification_status key set changed beyond the addition')
    for k in b_vs:
        if b_vs[k] != a_vs[k]:
            return _fail('verification_status.%s moved' % k)
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            return _fail('top-level %s changed' % k)
    print('verified: footprint is artichoke only; 12 findings byte-identical; '
          'nested crops %d -> %d' % (nested_before, nested_after))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        return _fail('trailing newline introduced')
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d findings relocated under verification_status' % EXPECTED_FINDINGS)
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
