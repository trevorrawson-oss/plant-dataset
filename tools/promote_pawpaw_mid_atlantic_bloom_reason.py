#!/usr/bin/env python3
"""GUARDED PROMOTE: fix the STATED REASON of pawpaw's mid_atlantic bloom finding.

Trevor-approved 2026-07-30, following the apple ruling the same day.

THE SHARED DEFECT. `mid_atlantic_bloom_offset_undocumented` was authored once and attached to ten
crops, crediting NC State's Extension Gardener Handbook ch.15 with publishing no bloom date. Eight
of the ten cite `ncsu_ext` and that reason is accurate for them. Two do not: apple (corrected in
its own promote) and pawpaw, whose arm cites `psu_ext`.

WHY PAWPAW'S CORRECT REASON IS NOT APPLE'S. Apple's conclusion survived on GEOGRAPHY -- its source
does publish bloom timing, but for WESTERN North Carolina, which `mid_atlantic` excludes. Pawpaw's
survives on genuine ABSENCE. Penn State's "The Native Pawpaw Tree" was fetched and read from raw
bytes: 15,361 characters, names pawpaw 15 times, and contains ZERO occurrences of bloom, blossom or
flowering. So the quantity really is unpublished there, and the declaration is sound -- it was
simply crediting the wrong document.

That is the whole reason this is done per crop. One finding text over ten crops looked economical
and quietly asserted three different things, two of them false. **Never blanket a reason across
crops whose citations differ.**

FOOTPRINT: 1 crop, 1 finding, 2 keys. Documentation only. The 8 handbook siblings and the
already-corrected apple all come through byte-for-byte.

    $ python3 tools/promote_pawpaw_mid_atlantic_bloom_reason.py --dry-run
    $ python3 tools/promote_pawpaw_mid_atlantic_bloom_reason.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '8116484c0254efcb4a7de0fc3c398a1404e2b7836db84031e04c0a9d9de4805f'

SLUG = 'pawpaw'
REGION = 'mid_atlantic'
FINDING_ID = 'mid_atlantic_bloom_offset_undocumented'
NAMED_SOURCE = 'psu_ext'

# the crops whose arms DO cite ncsu_ext, for which the original wording is accurate
SIBLINGS = ('fig', 'mulberry', 'nectarine', 'peach',
            'pear-asian', 'pear-european', 'persimmon', 'plum')

PRIOR_SUMMARY = (
    'The mid_atlantic bloom window is a MODELED offset from the zone last-frost date, not a quoted '
    'datum. The NC State Extension Gardener Handbook chapter 15 was located and read in full this '
    'session and publishes NO bloom date for any fruit crop: it carries 31 mentions of bloom, all '
    'of them risk or management language ("any warm period during the remainder of the winter will '
    'cause the tree to bloom prematurely"), and the only month appearing near bloom refers to '
    'pruning in February. This independently reproduces the same finding at a second institution '
    'after UAEX, so the quantity appears simply not to be published for this geography -- the '
    'harvest-start-is-not-a-published-datum shape. Repointing cannot fix an absent quantity; the '
    'derivation is declared instead.')

PRIOR_BASIS = ('tools/doc_mentions_crop_scan.py + full read of the handbook, 2026-07-30. See '
               'docs/2026-07-30-mid-south-uada-ext-citation-hunt.md.')

NEW_SUMMARY = (
    'The mid_atlantic bloom window is a MODELED offset from the zone last-frost date, not a quoted '
    'datum. REASON CORRECTED 2026-07-30; the conclusion is unchanged and remains sound. The earlier '
    'wording credited this to the NC State Extension Gardener Handbook chapter 15, but THIS crop\'s '
    'bloom arm does not cite the handbook: it cites psu_ext (extension.psu.edu/the-native-pawpaw-'
    'tree). That document was fetched and read from raw bytes and genuinely publishes no bloom '
    'date: 15,361 characters, pawpaw named 15 times, and ZERO occurrences of bloom, blossom or '
    'flowering anywhere in it. So the declaration stands on real ABSENCE at the cited source, which '
    'is the harvest-start-is-not-a-published-datum shape; only the document being credited was '
    'wrong. Note this is NOT apple\'s correction: apple\'s source does publish bloom timing and its '
    'declaration rests on geography instead. One finding text was authored once and attached to ten '
    'crops whose citations differ, which is how a single wrong reason reached three different '
    'cells; the eight crops whose arms do cite ncsu_ext keep the original handbook rationale, which '
    'is accurate for them.')

NEW_BASIS = (
    'tools/bloom_datum_scan.py (per-document bloom-timing classification, verdict NO_MENTION) + '
    'raw-bytes read of extension.psu.edu/the-native-pawpaw-tree, 2026-07-30. See '
    'docs/2026-07-30-bloom-declaration-premise-falsified.md. Supersedes the handbook rationale in '
    'the original wording; the accepted_modeled conclusion is unchanged.')


def _bloom_sources(crop):
    out = []
    for planting in (crop['regions'][REGION].get('plantings') or []):
        for arm in (planting.get('bloom') or []):
            if isinstance(arm, dict):
                out.extend(arm.get('sources') or [])
    return out


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
        print('ABORT: canonical drifted.\n  expected %s\n  found    %s' % (args.expect_sha, sha))
        return 2
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    before = copy.deepcopy(data)
    crops = {c['slug']: c for c in data['crops']}
    if SLUG not in crops:
        print('ABORT: %s absent' % SLUG)
        return 2

    srcs = _bloom_sources(crops[SLUG])
    if NAMED_SOURCE not in srcs:
        print('ABORT: the new reason names %r but the %s/%s bloom arm cites %s.\n'
              '       Refusing to describe a document this cell does not cite.'
              % (NAMED_SOURCE, SLUG, REGION, srcs))
        return 2
    print('verified: bloom arm really cites %s (%s)' % (NAMED_SOURCE, srcs))

    ofs = (crops[SLUG].get('verification_status') or {}).get('open_findings') or []
    target = [f for f in ofs if isinstance(f, dict) and f.get('id') == FINDING_ID]
    if len(target) != 1:
        print('ABORT: expected exactly 1 %r on %s, found %d' % (FINDING_ID, SLUG, len(target)))
        return 2
    finding = target[0]

    if finding.get('summary') != PRIOR_SUMMARY:
        print('ABORT: prior summary is not the expected text (already edited?).')
        return 2
    if finding.get('basis') != PRIOR_BASIS:
        print('ABORT: prior basis is not the expected text (already edited?).')
        return 2
    if finding.get('status') != 'accepted_modeled':
        print('ABORT: status is %r, expected accepted_modeled' % finding.get('status'))
        return 2
    print('verified: prior summary, basis and status are exactly as pinned')

    sib_before = {}
    for s in SIBLINGS:
        sf = [f for f in ((crops[s].get('verification_status') or {}).get('open_findings') or [])
              if isinstance(f, dict) and f.get('id') == FINDING_ID]
        if len(sf) != 1 or sf[0].get('summary') != PRIOR_SUMMARY:
            print('ABORT: sibling %s does not carry the expected prior finding' % s)
            return 2
        sib_before[s] = json.dumps(sf[0], sort_keys=True, ensure_ascii=False)
    print('verified: all %d handbook siblings carry the identical prior finding' % len(SIBLINGS))

    status_before = finding.get('status')
    finding['summary'] = NEW_SUMMARY
    finding['basis'] = NEW_BASIS
    if finding.get('status') != status_before:
        print('ABORT: status moved -- this promote may not change the conclusion')
        return 2

    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != [SLUG]:
        print('ABORT: crops changed = %s, expected only [%s]' % (changed, SLUG))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    if ba[SLUG]['regions'] != aa[SLUG]['regions']:
        print('ABORT: a region moved -- this promote is documentation only')
        return 2
    diffkeys = sorted(k for k in set(ba[SLUG]) | set(aa[SLUG])
                      if ba[SLUG].get(k) != aa[SLUG].get(k))
    if diffkeys != ['verification_status']:
        print('ABORT: %s keys changed = %s, expected only verification_status' % (SLUG, diffkeys))
        return 2
    fb = next(f for f in ba[SLUG]['verification_status']['open_findings']
              if f.get('id') == FINDING_ID)
    fa = next(f for f in aa[SLUG]['verification_status']['open_findings']
              if f.get('id') == FINDING_ID)
    fdiff = sorted(k for k in set(fb) | set(fa) if fb.get(k) != fa.get(k))
    if fdiff != ['basis', 'summary']:
        print('ABORT: finding keys changed = %s, expected exactly [basis, summary]' % fdiff)
        return 2
    for s in SIBLINGS:
        sf = next(f for f in aa[s]['verification_status']['open_findings']
                  if f.get('id') == FINDING_ID)
        if json.dumps(sf, sort_keys=True, ensure_ascii=False) != sib_before[s]:
            print('ABORT: sibling %s finding moved' % s)
            return 2
    print('verified: 1 crop / 1 finding / 2 keys; %d siblings byte-for-byte' % len(SIBLINGS))

    if args.dry_run:
        print('\n  summary: %d -> %d chars' % (len(PRIOR_SUMMARY), len(NEW_SUMMARY)))
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: reworded %s on %s (reason only; conclusion kept)' % (FINDING_ID, SLUG))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
