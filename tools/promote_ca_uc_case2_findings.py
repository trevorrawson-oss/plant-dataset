#!/usr/bin/env python3
"""GUARDED PROMOTE: campaign A closeout -- 5 CASE 2 findings on 5 crops.

FINDINGS ONLY. Not one value moves, not one citation moves, not one source id changes.
Evidence: docs/2026-08-03-campaign-a-count-reconciliation-and-readjudication.md.

Campaign A's first promote repointed the 52 decisions the UC planting-date table can support.
This closes the part it CANNOT, by ruling rather than by edit -- the cells keep their bare host
by design, which is what the hunt ledger exists to record.

TWO DISTINCT REASONS, and they are filed separately because they are not the same defect.
Blanketing one reason over crops that need different ones is a documented failure of this arc.

  A. THE DOCUMENT HAS NO ROW FOR THIS CROP (4 findings / 4 crops / 5 decisions).
     https://ucanr.edu/program/uc-master-gardener-program/time-planting is California Master
     Gardener Handbook TABLE 13.2, a VEGETABLE table. Read from raw bytes this session and parsed
     by HTML structure: 33 rows, artichoke -> watermelons, asserted rectangular at 33x6. It has
     no arugula row; its only bean row is "beans, snap", which is Phaseolus and not edamame's
     Glycine max; and it carries no tree fruit at all, so neither pear is in it. A vegetable
     planting guide standing as sole source on a tree fruit is the vce_426_331 shape this arc has
     already caught once, on 19 fruit nodes.

  B. THE ROW EXISTS BUT HAS NO REGIONAL RESOLUTION (1 finding / okra / 4 decisions).
     Okra IS in the table, and that is why it needs the opposite ruling from A. Its row reads
     "May" for North & North Coast, "April-May" for South Coast, "May" for Interior Valleys and
     "May" for Desert Valleys. Three of four regions are the same single month, and the two the
     table gives identically -- Monterey-north and the Imperial Valley -- are the coldest and the
     hottest summer climates in the state. A row that cannot separate those two cannot adjudicate
     a per-region window, so our ca_desert March opening and ca_north_coast June opening are not
     CONTRADICTED by it in any meaningful sense; they are simply not addressed by it. Recording
     that is honest; trimming our dates to a state-wide single month would be a real regression.

WHY NO CITATION IS REPOINTED AND NO VALUE MOVES. CASE 2 means the claim is unsourced. The fix is
a content finding, not a URL swap at a plausible-looking page -- and not a date change either,
since nothing here shows a date is wrong.

DELIBERATELY OUT OF SCOPE: lemon (4) and lime (3), whose 7 decisions are the same "no UC row"
shape but belong with campaign D's lemon cluster, where one crop-centric read of lemon's
citations serves seven hunts at once. Filing them here would do the work twice.

FOOTPRINT: 5 findings appended to 5 crops' verification_status.open_findings. Every other byte
identical -- no anchoring_urls, no sources array, no window, no prose. COMPACT preserved.

    $ python3 tools/promote_ca_uc_case2_findings.py --dry-run
    $ python3 tools/promote_ca_uc_case2_findings.py --apply
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
BASE_SHA = 'e65aa63ae6154371233edbf076d7f94003652dfbd64980eae3c20a2afb3c76cd'
SESSION = 'ca_uc_case2_findings_2026_08_03'

BARE = {'ucanr_ext': 'https://ucanr.edu', 'uc_mg': 'https://mg.ucanr.edu'}
TABLE_URL = 'https://ucanr.edu/program/uc-master-gardener-program/time-planting'

# (crop, region, source_id, EXACT bare url) each finding rules on. The url is pinned per decision,
# not taken from a global map, because that assumption was WRONG and this guard caught it: both
# pears cite https://homeorchard.ucanr.edu/, the UC Home Orchard root, NOT the vegetable table.
# Filing the no-row reason on them would have asserted something false about their citation.
COVERED = {
    'arugula': [('ca_interior', 'uc_mg', 'https://mg.ucanr.edu'),
                ('ca_south_coast', 'uc_mg', 'https://mg.ucanr.edu')],
    'edamame': [('ca_north_coast', 'uc_mg', 'https://mg.ucanr.edu')],
    'pear-asian': [('ca_interior', 'ucanr_ext', 'https://homeorchard.ucanr.edu/')],
    'pear-european': [('ca_interior', 'ucanr_ext', 'https://homeorchard.ucanr.edu/')],
    'okra': [('ca_desert', 'uc_mg', 'https://mg.ucanr.edu'),
             ('ca_desert', 'ucanr_ext', 'https://ucanr.edu'),
             ('ca_north_coast', 'uc_mg', 'https://mg.ucanr.edu'),
             ('ca_north_coast', 'ucanr_ext', 'https://ucanr.edu')],
}
HOMEORCHARD = 'https://homeorchard.ucanr.edu/'

# okra's windows as they must still read for finding B's reasoning to hold.
OKRA_WINDOWS = {
    'ca_desert': {'9': 'Mar 15 - Apr 30', '10': 'Mar 1 - Apr 30', '11': 'Mar 1 - Apr 30'},
    'ca_north_coast': {'9': 'Jun 1 - Jun 30', '10': 'May 15 - Jun 30'},
}

_NOROW = (
    'The cited UC page cannot source this cell because it has no row for this crop. '
    '%s is the California Master Gardener Handbook Table 13.2, a VEGETABLE planting-date table; '
    'read from raw bytes 2026-08-03 and parsed by HTML structure (33 rows, artichoke through '
    'watermelons, asserted rectangular at 33x6), %s CASE 2: the claim is unsourced, so this is '
    'recorded as a content finding rather than repointed at a plausible-looking page, and no '
    'date is changed because nothing here shows a date is wrong. The cell keeps its bare host by '
    'design; the hunt ledger records it as ruled rather than open.') % (TABLE_URL, '%s')

_ORCHARD = (
    'This cell cites ' + HOMEORCHARD + ', a domain root, as its sole source -- but that root is '
    'the UC HOME ORCHARD site, not the UC vegetable planting-date table, and the distinction '
    'changes the ruling. The Home Orchard site is the RIGHT CLASS of document for %s: it is UC '
    "ANR's home fruit-tree resource, so unlike a vegetable table standing on a tree fruit, "
    'nothing here is mis-classed. What is missing is the specific page, which was never '
    'recorded. That makes this a CASE 1 REPOINT CANDIDATE rather than a CASE 2 unsourced claim, '
    'and it is deliberately NOT answered in campaign A, whose document is the vegetable table '
    'and cannot speak to a pear. It belongs with the UC fruit-tree read that also owes the '
    'ca_north_coast/ucanr_marin_mg pear decisions -- the same two crops -- so one pass settles '
    'both rather than two passes settling one each. Left OPEN, not accepted: there is a live '
    'document to go find, and this should not read as a closed decision.')

FINDINGS = [
    ('arugula', {
        'id': 'arugula_ca_uc_table_has_no_row',
        'summary': _NOROW % ('and it contains no arugula row at all. Arugula (Eruca vesicaria) '
                             'is absent from the table, which carries no salad-green row beyond '
                             'lettuce and spinach.'),
        'basis': ('Campaign A, 2026-08-03. Covers ca_interior/uc_mg and ca_south_coast/uc_mg, '
                  'both of which cite https://mg.ucanr.edu, a domain root, as their sole source. '
                  'The table was located, fetched and read in full this session -- this is a '
                  'document-scoped absence over one document, not a claim about what UC ANR '
                  'publishes anywhere. A UC arugula planting date may well exist elsewhere in '
                  'UC ANR material; it is simply not in the page these cells point at.'),
        'severity': 'low', 'blocks_launch': False,
        'filed_in_session': SESSION, 'status': 'accepted',
    }),
    ('edamame', {
        'id': 'edamame_ca_north_coast_uc_table_has_no_row',
        'summary': _NOROW % ('and its only bean row is "beans, snap", which is Phaseolus '
                             'vulgaris. Edamame is Glycine max, a different genus with a '
                             'different daylength response and a different season, so the snap '
                             'bean row does not transfer to it. Matching the row by the word '
                             '"beans" would be the match-the-taxon-not-the-common-name trap.'),
        'basis': ('Campaign A, 2026-08-03. Covers ca_north_coast/uc_mg, citing '
                  'https://mg.ucanr.edu, a domain root, as its sole source. Note edamame ALSO '
                  'carries a separate ca_north_coast/ucanr_marin_mg bare host, which is ledger '
                  'hunt #16 and out of this campaign; the Marin MG vegetable planting calendar '
                  'already identified there is a genuinely better candidate for edamame than '
                  'this table, and is left to that hunt.'),
        'severity': 'low', 'blocks_launch': False,
        'filed_in_session': SESSION, 'status': 'accepted',
    }),
    ('pear-asian', {
        'id': 'pear_asian_ca_interior_homeorchard_root_repoint_candidate',
        'summary': _ORCHARD % 'pear-asian',
        'basis': ('Campaign A, 2026-08-03. Covers ca_interior/ucanr_ext. This crop was initially '
                  'grouped with the crops the UC vegetable table omits, and that grouping was '
                  'WRONG: a guard pinning the exact bare URL per decision caught that these '
                  'cells never cited the vegetable table at all. The reason had to be measured '
                  'per cell rather than blanketed across the group, which is a documented '
                  'failure mode of this arc.'),
        'severity': 'low', 'blocks_launch': False,
        'filed_in_session': SESSION, 'status': 'open',
    }),
    ('pear-european', {
        'id': 'pear_european_ca_interior_homeorchard_root_repoint_candidate',
        'summary': _ORCHARD % 'pear-european',
        'basis': ('Campaign A, 2026-08-03. Covers ca_interior/ucanr_ext. Same disposition as '
                  'pear-asian and filed separately because each crop carries its own ruling, '
                  'but note the two are NOT automatically the same answer: Pyrus pyrifolia and '
                  'Pyrus communis have different chill and harvest behavior, so whichever Home '
                  'Orchard page is located must be checked to cover the specific species before '
                  'either citation is repointed at it.'),
        'severity': 'low', 'blocks_launch': False,
        'filed_in_session': SESSION, 'status': 'open',
    }),
    ('okra', {
        'id': 'okra_ca_uc_row_lacks_regional_resolution',
        'summary': (
            'Okra IS in the UC planting-date table, and it still cannot adjudicate these cells, '
            'which is why this is ruled differently from the crops the table simply omits. Read '
            'from raw bytes 2026-08-03, the okra row of ' + TABLE_URL + ' gives "May" for North '
            '& North Coast, "April-May" for South Coast, "May" for Interior Valleys and "May" '
            'for Desert Valleys. Three of the four regions are the same single month, and the '
            'two it treats identically -- Monterey County north, and the Imperial and Coachella '
            'Valleys -- are the coldest and the hottest summer climates in the state. A row that '
            'does not separate those two carries no regional resolution, and the page says as '
            'much itself: "Because the areas shown here are large, planting dates are only '
            'approximate, as the climate may vary even in small sections of the state." So our '
            'ca_desert opening (Mar 1 or Mar 15) and our ca_north_coast z9 opening (Jun 1) are '
            'not meaningfully contradicted by this document; they are not addressed by it. NO '
            'DATE IS CHANGED: trimming a per-region window to a state-wide single month would '
            'lose real regional information, and the desert March opening is independently '
            'consistent with U of A AZ1005, whose low-desert okra marks run Mar 15 to May 15.'),
        'basis': ('Campaign A, 2026-08-03. Covers ca_desert/uc_mg, ca_desert/ucanr_ext, '
                  'ca_north_coast/uc_mg and ca_north_coast/ucanr_ext -- 4 decisions, all citing '
                  'a domain root as their sole source. These were the two live authoring '
                  'decisions kickoff 50 identified in the California block; the adjudication is '
                  'that they are a SOURCE-GRANULARITY finding, not a value defect. AZ1005 is '
                  'named here as a consistency check on the desert window only, explicitly NOT '
                  'as a California source -- trimming a Californian window to an Arizona '
                  "document's marks is the geography stretch this arc warns about, and is the "
                  'same restraint ca_desert_fall_cycle_provenance_gap applied.'),
        'severity': 'low', 'blocks_launch': False,
        'filed_in_session': SESSION, 'status': 'accepted',
    }),
]

EXPECT_FINDINGS = 5
EXPECT_CROPS = sorted(COVERED)
INSTITUTION = re.compile(r'Arizona|AZ1005|NC State|NCSU|Clemson|Texas A&M|TAMU')


def _nodes(root):
    out = []

    def walk(n):
        if isinstance(n, dict):
            if isinstance(n.get('anchoring_urls'), dict):
                out.append(n)
            for k, v in n.items():
                if k != 'anchoring_urls':
                    walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(root)
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

    # PREFLIGHT 1: every decision this rules on must STILL be a sole bare host. If one has been
    # repointed since, the finding would describe a state that no longer exists.
    for slug, pairs in sorted(COVERED.items()):
        crop = crops.get(slug)
        if crop is None:
            print('ABORT: crop %s absent' % slug)
            return 2
        for reg, sid, want_url in pairs:
            r = ((crop.get('regions') or {}).get(reg))
            if not isinstance(r, dict):
                print('ABORT: %s has no %s region' % (slug, reg))
                return 2
            found = False
            for node in _nodes(r):
                au = node.get('anchoring_urls') or {}
                meta = au.get(sid)
                if not isinstance(meta, dict) or meta.get('url') != want_url:
                    continue
                cited = set(au) | {s for s in (node.get('sources') or []) if isinstance(s, str)}
                allbare = {s for s, m in au.items()
                           if isinstance(m, dict) and m.get('url')
                           and re.fullmatch(r'https?://[^/]+/?', m['url'])}
                if not (cited - allbare):
                    found = True
            if not found:
                print('ABORT: %s %s/%s no longer cites %s as a sole bare host -- premise moved'
                      % (slug, reg, sid, want_url))
                return 2
    print('preflight: all %d decisions still sole bare hosts'
          % sum(len(v) for v in COVERED.values()))

    # PREFLIGHT 2: okra's windows must still read as finding B's reasoning quotes them.
    for reg, zones in sorted(OKRA_WINDOWS.items()):
        rbz = crops['okra']['regions'][reg]['resolved_by_zone']
        for z, want in sorted(zones.items()):
            got = (rbz.get(z) or {}).get('plant_out')
            if got != want:
                print('ABORT: okra %s z%s plant_out is %r, finding quotes %r -- re-adjudicate'
                      % (reg, z, got, want))
                return 2
    print('preflight: okra windows match the text of the ruling')

    # FILE
    filed = []
    for slug, finding in FINDINGS:
        vs = crops[slug].setdefault('verification_status', {})
        ofs = vs.setdefault('open_findings', [])
        if any(isinstance(f, dict) and f.get('id') == finding['id'] for f in ofs):
            print('ABORT: finding %s already filed' % finding['id'])
            return 2
        ofs.append(copy.deepcopy(finding))
        filed.append('%s <- %s' % (slug, finding['id']))
    if len(filed) != EXPECT_FINDINGS:
        print('ABORT: filed %d findings, expected %d' % (len(filed), EXPECT_FINDINGS))
        return 2
    print('filed: %d findings' % len(filed))

    # A finding may not name an institution the ruling does not rest on. AZ1005 appears in okra's
    # basis as a deliberate, explained consistency check -- nowhere else.
    for slug, finding in FINDINGS:
        if slug == 'okra':
            continue
        blob = json.dumps(finding, ensure_ascii=False)
        m = INSTITUTION.search(blob)
        if m:
            print('ABORT: %s finding names %r, which its ruling does not rest on'
                  % (slug, m.group(0)))
            return 2
    print('verified: no finding names an institution outside its own ruling')

    # NOT ONE citation, window or prose byte may move. Strip open_findings from both trees and
    # they must be equal.
    def stripped(doc):
        d = copy.deepcopy(doc)
        for crop in d['crops']:
            (crop.get('verification_status') or {}).pop('open_findings', None)
        return d
    if stripped(before) != stripped(data):
        print('ABORT: something other than open_findings changed')
        return 2
    print('verified: nothing but open_findings moved -- no citation, window or prose touched')

    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if changed != EXPECT_CROPS:
        print('ABORT: crops changed = %s, expected %s' % (changed, EXPECT_CROPS))
        return 2
    # NOTE: no separate top-level-key guard. The stripped() equality above compares the WHOLE
    # document with only open_findings removed, so it already catches any top-level change and a
    # second check there was mutation-proven unreachable. A check that cannot fail is not a guard.
    print('verified: exactly %d crops changed' % len(changed))

    # each touched crop gained exactly ONE finding
    for slug in EXPECT_CROPS:
        b = len(((ba[slug].get('verification_status') or {}).get('open_findings')) or [])
        a = len(((aa[slug].get('verification_status') or {}).get('open_findings')) or [])
        if a - b != 1:
            print('ABORT: %s findings went %d -> %d, expected +1' % (slug, b, a))
            return 2
    print('verified: each of the %d crops gained exactly one finding' % len(EXPECT_CROPS))

    print('\n%d findings:' % len(filed))
    for f in filed:
        print('  ' + f)

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d findings across %d crops' % (len(filed), len(changed)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
