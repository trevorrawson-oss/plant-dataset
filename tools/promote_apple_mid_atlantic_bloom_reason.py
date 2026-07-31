#!/usr/bin/env python3
"""GUARDED PROMOTE: fix the STATED REASON of apple's mid_atlantic bloom finding, keep its conclusion.

Trevor-ruled 2026-07-30, by the precedent he set the same day on mid_atlantic cherry-sour.

WHAT WAS WRONG. `mid_atlantic_bloom_offset_undocumented` is carried identically by ten crops. Its
reason says the NC State Extension Gardener Handbook ch. 15 "publishes NO bloom date for any fruit
crop", so the quantity is absent and the offset must be declared. For eight of the ten that is
exactly right -- their bloom arms cite `ncsu_ext`. **Apple's does not.** Apple's mid_atlantic bloom
arm cites `ext_org_apples`, and that page publishes apple bloom timing outright:

    "in western North Carolina apple trees will generally bloom in mid-April whereas apple trees
     in Minnesota do not bloom until a month later, generally in mid-May"

So the finding's stated reason describes a document this cell never cited, and asserts an absence
its actual source contradicts.

WHY THE CONCLUSION SURVIVES ANYWAY -- and this is Trevor's ruling, not an inference. The page's
North Carolina figure is explicitly WESTERN North Carolina. `mid_atlantic` is explicitly "Piedmont
and Coastal Plain", which excludes the mountains. A western-mountains source does not govern this
belt. That is the identical geography test Trevor applied to mid_atlantic sour cherry hours
earlier, where the single pro-sour-cherry recommendation came from Macon County. Apple bloom timing
IS published; it is not published for THIS region. The offset stays modeled, and repointing at the
mid-April figure would import the wrong geography.

REWORD, DO NOT DELETE. The conclusion (`accepted_modeled`), the id, the severity and the launch
flag are all unchanged. Only `summary` and `basis` move.

THE GUARD THAT MATTERS is a generalization of hunt 1's best one ("refuse to cite a document at a
cell that contradicts it"): **refuse to write a reason that names a source the arm does not
actually carry.** That is the defect being removed, so the script must be unable to reintroduce it.
Tested by reverting apple's citation to the handbook and confirming the abort.

FOOTPRINT: 1 crop, 1 finding, 2 keys. Documentation only -- no value, date, calendar or citation
moves anywhere in the roster. Nine sibling findings come through byte-for-byte.

    $ python3 tools/promote_apple_mid_atlantic_bloom_reason.py --dry-run
    $ python3 tools/promote_apple_mid_atlantic_bloom_reason.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'd5f8307395d681d908857953c13ef51be0e680c6532794a2fb3c6e3aae0925d9'

SLUG = 'apple'
REGION = 'mid_atlantic'
FINDING_ID = 'mid_atlantic_bloom_offset_undocumented'

# The source id the new reason names. It MUST be the one the bloom arm actually carries.
NAMED_SOURCE = 'ext_org_apples'

SIBLINGS = ('fig', 'mulberry', 'nectarine', 'pawpaw', 'peach',
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
    'datum. REASON CORRECTED 2026-07-30 (Trevor-ruled); the conclusion is unchanged. The earlier '
    'wording credited this to the NC State Extension Gardener Handbook chapter 15 publishing no '
    'bloom date, but THIS crop\'s bloom arm does not cite the handbook at all: it cites '
    'ext_org_apples (apples.extension.org/timing-of-apple-tree-bloom/), and that page DOES publish '
    'apple bloom timing -- "in western North Carolina apple trees will generally bloom in mid-April '
    'whereas apple trees in Minnesota do not bloom until a month later, generally in mid-May". The '
    'declaration therefore rests on GEOGRAPHY, not on absence. That figure is explicitly WESTERN '
    'North Carolina, and mid_atlantic is explicitly "Piedmont and Coastal Plain", which excludes '
    'the mountains, so a western-mountains source does not govern this belt: the same test Trevor '
    'applied the same day to mid_atlantic cherry-sour, where the one pro-sour-cherry '
    'recommendation came from Macon County. Apple bloom timing IS published, just not for this '
    'region, so the offset stays modeled here and repointing at the mid-April figure would import '
    'the wrong geography. The eight sibling crops whose arms DO cite ncsu_ext keep the original '
    'handbook rationale, which is accurate for them.')

NEW_BASIS = (
    'tools/bloom_datum_scan.py (per-document bloom-timing classification) + raw-bytes read of '
    'apples.extension.org, 2026-07-30. See docs/2026-07-30-bloom-declaration-premise-falsified.md '
    'section 4. Supersedes the handbook rationale in the original wording; the accepted_modeled '
    'conclusion is Trevor-ruled and unchanged.')


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

    # THE LOAD-BEARING GUARD: the reason may only name a source this arm actually carries.
    srcs = _bloom_sources(crops[SLUG])
    if NAMED_SOURCE not in srcs:
        print('ABORT: the new reason names %r but the %s/%s bloom arm cites %s.\n'
              '       Refusing to describe a document this cell does not cite -- that is the very '
              'defect this promote removes.' % (NAMED_SOURCE, SLUG, REGION, srcs))
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

    # the nine siblings must be sitting on the prior text too, so "unchanged" is provable
    sib_before = {}
    for s in SIBLINGS:
        sf = [f for f in ((crops[s].get('verification_status') or {}).get('open_findings') or [])
              if isinstance(f, dict) and f.get('id') == FINDING_ID]
        if len(sf) != 1 or sf[0].get('summary') != PRIOR_SUMMARY:
            print('ABORT: sibling %s does not carry the expected prior finding' % s)
            return 2
        sib_before[s] = json.dumps(sf[0], sort_keys=True, ensure_ascii=False)
    print('verified: all 9 siblings carry the identical prior finding')

    status_before = finding.get('status')
    finding['summary'] = NEW_SUMMARY
    finding['basis'] = NEW_BASIS

    if finding.get('status') != status_before:
        print('ABORT: status moved -- this promote may not change the conclusion')
        return 2

    # ---- blast radius ------------------------------------------------------
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
        print('ABORT: apple keys changed = %s, expected only verification_status' % diffkeys)
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
    print('verified: 1 crop / 1 finding / 2 keys; 9 siblings byte-for-byte')

    if args.dry_run:
        print('\n  summary: %d -> %d chars' % (len(PRIOR_SUMMARY), len(NEW_SUMMARY)))
        print('  basis:   %d -> %d chars' % (len(PRIOR_BASIS), len(NEW_BASIS)))
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
