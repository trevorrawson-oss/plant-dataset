#!/usr/bin/env python3
"""GUARDED PROMOTE: explain the July desert sowing in the four cucurbits' ca_desert region notes.

PROSE ONLY, and an EDIT to existing prose -- no field is added, no value moves, no citation moves,
no finding is filed. `region_notes_seasoned` / `region_notes_beginner` already exist on all 121
certified crops in every region they carry (1,808 of 1,878 region cells; the only 70 gaps are the
7 uncertified shells x 10 regions), so this is not a schema change and not a cross-crop field
addition.

WHAT IT ADDS AND WHY. These cells already say a midsummer sowing happens around July. They do not
say WHY, and the timing reads as a mistake to anyone who knows what an Imperial Valley July is.
Trevor ruled 2026-08-03 to keep the July window; this makes the reasoning legible to the reader
instead of leaving it only in an open_finding no user will ever see.

WHAT IT DELIBERATELY DOES NOT CLAIM. No temperature threshold and no fruit-set number. Cucurbit
pollen viability does collapse somewhere in the low 90s F, but that was NOT sourced this session,
and writing a number the record cannot support is the fill-the-shape-is-the-defect failure. The
copy stays qualitative: flowering and fruit set land in the milder weather of early fall. That is
a restatement of this crop's OWN calendar (sow July, harvest Oct 1 - Nov 1), not a new claim. The
quantitative version belongs to the fruit-set arc recorded in STATE_HISTORY.md 2026-08-03.

NO INSTITUTION IS NAMED. These ca_desert arms are the 8 decisions HELD on the accepted finding
ca_desert_fall_cycle_provenance_gap and still cite a bare host, so naming a source here is exactly
what promote_apple_mid_atlantic_bloom_reason.py refuses.

VISIBILITY, STATED HONESTLY. plant-astro renders NONE of region_notes_seasoned/beginner today
(nor planting_note, zone_notes or notes). This copy is correct and waiting, not live. It cannot
regress anything, because nothing reads it -- "ship the frontend first" guards against a consumer
failing OPEN on an unknown value, which is not this.

FOOTPRINT: 8 strings = 4 crops x ca_desert x 2 registers. Every other byte identical. COMPACT.

    $ python3 tools/promote_ca_desert_july_sowing_note.py --dry-run
    $ python3 tools/promote_ca_desert_july_sowing_note.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '3f6d6ce4430c23ab8b346017be3b9a8963f635fc1178767293d24e2a689eb6f3'

REGION = 'ca_desert'
CROPS = ('acorn-squash', 'butternut-squash', 'spaghetti-squash', 'pumpkin')

SEASONED_ADD = (
    ' The July timing looks punishing and is deliberate: it places flowering and fruit set in the '
    'milder weather of early fall rather than at peak summer temperatures. Keep water steady '
    'through establishment, when the seedbed is most exposed.')
BEGINNER_ADD = (
    ' Planting in July seems harsh, but it is on purpose: the plants flower and set fruit later, '
    'once the weather has cooled. Keep the soil damp while the seedlings get going.')

# Each cell's EXACT prior tail, asserted to occur exactly once before the sentence is appended.
# Pinned per crop rather than matched loosely: butternut and pumpkin carry different wording from
# acorn and spaghetti, and a loose match would silently accept the wrong cell.
TAILS = {
    ('acorn-squash', 'region_notes_seasoned'):
        'Steady irrigation is essential, and the fall timing is the reliable one.',
    ('acorn-squash', 'region_notes_beginner'):
        'and again around July for a fall crop. Water steadily.',
    ('butternut-squash', 'region_notes_seasoned'):
        'Steady irrigation is essential, and the fall timing is the reliable one.',
    ('butternut-squash', 'region_notes_beginner'):
        'for a fall crop that grows right through the summer heat. Water steadily.',
    ('spaghetti-squash', 'region_notes_seasoned'):
        'Steady irrigation is essential, and the fall timing is the reliable one.',
    ('spaghetti-squash', 'region_notes_beginner'):
        'and again around July for a fall crop. Water steadily.',
    ('pumpkin', 'region_notes_seasoned'):
        'Steady irrigation is essential, and the fall timing is the reliable one.',
    ('pumpkin', 'region_notes_beginner'):
        'for a fall crop that grows right through the summer heat. Water steadily.',
}

EXPECT_STRINGS = 8
ANY_INSTITUTION = re.compile(
    r'University|Extension|UC ANR|UCANR|Master Gardener|AZ1005|Arizona|NC State|NCSU|UAEX')
EM = chr(8212)


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

    # PREFLIGHT: the July window this copy explains must actually still be there. If the second
    # planting ever moves off July, this prose becomes a lie and must be re-authored, not carried.
    for slug in CROPS:
        rbz = ((crops.get(slug) or {}).get('regions', {}).get(REGION) or {}).get(
            'resolved_by_zone') or {}
        if not rbz:
            print('ABORT: %s has no %s resolved_by_zone' % (slug, REGION))
            return 2
        for z, cell in sorted(rbz.items()):
            sp = cell.get('second_planting')
            if not isinstance(sp, dict) or not str(sp.get('plant_out', '')).startswith('Jul'):
                print('ABORT: %s %s z%s second planting is %r, not a July sowing -- this copy '
                      'explains a July sowing and must be re-authored' % (
                          slug, REGION, z, (sp or {}).get('plant_out')))
                return 2
    print('preflight: all 4 crops still carry a July %s second planting' % REGION)

    # APPLY
    touched = []
    for slug in CROPS:
        r = crops[slug]['regions'][REGION]
        for field, add in (('region_notes_seasoned', SEASONED_ADD),
                           ('region_notes_beginner', BEGINNER_ADD)):
            cur = r.get(field)
            if not isinstance(cur, str) or not cur.strip():
                print('ABORT: %s %s is empty -- this promote EDITS existing prose, it does not '
                      'author a missing note' % (slug, field))
                return 2
            tail = TAILS[(slug, field)]
            if cur.count(tail) != 1 or not cur.endswith(tail):
                print('ABORT: %s %s does not END with its pinned tail exactly once' % (slug, field))
                return 2
            if add.strip() in cur:
                print('ABORT: %s %s already carries this sentence' % (slug, field))
                return 2
            r[field] = cur + add
            touched.append('%s %s' % (slug, field))

    if len(touched) != EXPECT_STRINGS:
        print('ABORT: rewrote %d strings, expected %d' % (len(touched), EXPECT_STRINGS))
        return 2
    print('applied: %d strings across %d crops' % (len(touched), len(CROPS)))

    # HOUSE STYLE + the no-source rule, on the rewritten strings.
    for slug in CROPS:
        r = crops[slug]['regions'][REGION]
        for field in ('region_notes_seasoned', 'region_notes_beginner'):
            v = r[field]
            if EM in v or '--' in v:
                print('ABORT: em dash or "--" in consumer copy: %s %s' % (slug, field))
                return 2
            if '  ' in v or ' ,' in v or ' .' in v:
                print('ABORT: whitespace/punctuation artifact: %s %s' % (slug, field))
                return 2
            m = ANY_INSTITUTION.search(v)
            if m:
                print('ABORT: %s %s names %r, but these arms cite a bare host and carry no such '
                      'source' % (slug, field, m.group(0)))
                return 2
            if re.search(r'\d+\s*(?:degrees|deg|F\b)', v):
                print('ABORT: %s %s states a temperature; this copy is deliberately qualitative '
                      'because no threshold was sourced' % (slug, field))
                return 2
    print('verified: house style clean, no institution named, no unsourced temperature')

    # FOOTPRINT
    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != sorted(CROPS):
        print('ABORT: crops changed = %s, expected %s' % (changed, sorted(CROPS)))
        return 2

    # Blank the 8 target strings in both trees; everything else must then be equal. This proves no
    # window, citation, other region or top-level key moved -- one check, always reachable.
    def blanked(doc):
        d = copy.deepcopy(doc)
        for crop in d['crops']:
            if crop['slug'] not in CROPS:
                continue
            r = (crop.get('regions') or {}).get(REGION) or {}
            for field in ('region_notes_seasoned', 'region_notes_beginner'):
                if field in r:
                    r[field] = '<blanked>'
        return d
    if blanked(before) != blanked(data):
        culprits = [s for s in changed
                    if blanked({'crops': [ba[s]]}) != blanked({'crops': [aa[s]]})]
        print('ABORT: changed outside the 8 region-note strings: %s'
              % (', '.join(culprits) or 'outside the crops list'))
        return 2
    print('verified: only the 8 region-note strings moved, and only in %s' % REGION)

    print('\n%d strings:' % len(touched))
    for t in touched:
        print('  ' + t)

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        print('\n--- resulting seasoned copy (pumpkin) ---')
        print(crops['pumpkin']['regions'][REGION]['region_notes_seasoned'])
        print('\n--- resulting beginner copy (pumpkin) ---')
        print(crops['pumpkin']['regions'][REGION]['region_notes_beginner'])
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d strings across %d crops' % (len(touched), len(changed)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
