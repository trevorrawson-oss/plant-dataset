#!/usr/bin/env python3
"""GUARDED PROMOTE: the AZ1005 melon read, the catalog-divergence fixes, and lavender.

CITATIONS AND FINDINGS ONLY. Not one consumer-facing string, date, offset or suitability moves;
a guard proves it byte-for-byte. Evidence: docs/2026-08-05-az1005-and-divergence-followups.md.

Three follow-ups left open by the campaign C closeout, worked together because they are one class
of question. 20 nodes repoint, 3 stay bare on purpose, 6 findings filed, no catalog id minted.

AZ1005 WAS READ, AND IT DOES NOT SAY WHAT SIBLING PRECEDENT SUGGESTED. The campaign C closeout
deliberately filed NO absence finding for cantaloupe, honeydew-melon and watermelon, because
AZ1005 was a live lead rather than a measured absence. Reading it proves that was the right call
twice over: it HAS both melon rows, so an absence finding would have been false -- and it does NOT
support every window we publish, so a blanket repoint would have been false too.

  Its grid is the documented 90-degree-rotated one, and this promote's evidence was reconstructed
  from CHARACTER COORDINATES rather than read by eye: month headers share an x and vary in y, so
  months run down the page and crops across it. The method was validated against a control before
  any melon was touched -- pumpkin reads Mar 1, Mar 15 then Jul 1, Jul 15, Aug 1 off the grid, and
  our pumpkin cell says plant_out Mar 1 - Mar 15 with a second planting Jul 1 - Jul 31. It
  reproduces a value we already hold, so the reading is trustworthy.

  Melons, Cantaloupe/Honeydews, etc.   S at Feb 15 through Jul 15, continuous
  Melons, Watermelon                   S at Feb 15, Mar 1, Mar 15 -- AND NOTHING ELSE ALL YEAR

  honeydew   opens Feb 15. The document opens Feb 15. Clean, all 5 nodes repoint.
  cantaloupe opens Feb 1, two weeks AHEAD of the document, and its second planting runs to
             Aug 15 where the document stops at Jul 15. Repointed, divergence FILED.
  watermelon opens Feb 1, and its Jul 15 - Aug 15 second planting has NO support at all: AZ1005
             gives watermelon a spring sowing window only. Its 3 spring nodes repoint; its TWO
             second_planting nodes STAY BARE with a filed reason.

  Note honeydew has no row of its OWN -- it rides a combined "Cantaloupe/Honeydews, etc." row, so
  the document cannot distinguish the two crops' timing. Recorded rather than glossed.

THE DIVERGENCE FIXES come from tools/catalog_divergence_scan.py, built this session at the one
definition that does not flood. turnip's 7 nodes cite `ucanr_san_diego_mg` at the bare
mastergardenersd.org root while eight sibling crops cite per-crop pages on that same host.

  THE OBVIOUS TARGET WAS WRONG. `/turnips/` -- the plural, matching `/beets/` -- returns HTTP 404.
  The real page is `/turnip/`, singular. Pattern-matching a sibling's url shape would have cited a
  dead link, which is the sibling-precedent trap in its cheapest possible form.

  edamame's one node STAYS BARE: no Cornell edamame VARIETY document exists to repoint at. The
  gardener-facing Vegetable Varieties database requires authentication, the only Cornell edamame
  publication is a 2014 conference proceedings PDF, and the Cornell field-crops soybean varieties
  page is agronomic soybean rather than edamame cultivars.

LAVENDER TURNED OUT NOT TO BE A RELABEL. It was queued as cosmetic -- an id pointing at the wrong
document. Reading all three of its NMSU sources shows something else: NONE of them publishes a
lavender planting date, so its `warm_arid` plant_out window is unsourced. No repoint is possible
and none is invented; the finding records it. The node is NOT bare and NOT sole, so no scan in the
repo would ever have surfaced this.

    $ python3 tools/promote_az1005_and_divergence.py --dry-run
    $ python3 tools/promote_az1005_and_divergence.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import re
import sys
from urllib.parse import urlsplit

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '754c51a0de23daceff87c081cd84c6d60274e416fc19639bd2ee2520f5f309f5'
SESSION = 'az1005_and_divergence_2026_08_05'
VERIFIED = '2026-08-05'

AZ_BARE = ('uariz_ext', 'https://extension.arizona.edu')
AZ1005 = 'uariz_ext_az1005'
# Written out as a CONSTANT rather than read from the catalog at edit time. A first version did
# `az_url = catalog[AZ1005]['url']` and then guarded `if az_url != catalog[AZ1005]['url']`, which
# compares a value to itself and can never fire -- the vacuous-guard shape, caught by the test
# sweep. Pinning it here makes the guard a real assertion: this promote believes AZ1005 lives at
# this address, and aborts if the catalog disagrees.
AZ1005_URL = 'https://www.extension.arizona.edu/sites/default/files/2024-08/az1005-2018.pdf'
SD_BARE = ('ucanr_san_diego_mg', 'https://www.mastergardenersd.org/')
SD_TURNIP = 'https://www.mastergardenersd.org/turnip/'

# (slug, region, path): the source ID CHANGES from the portal to the specific document, so both
# `sources` and `anchoring_urls` move. This is what the region's other 24 crops already do.
REPOINT_ID = [
    (s, 'low_desert_az', 'regions.low_desert_az.' + p)
    for s in ('cantaloupe', 'honeydew-melon')
    for p in ('plantings[0]', 'resolved_by_zone.9', 'resolved_by_zone.9.second_planting',
              'resolved_by_zone.10', 'resolved_by_zone.10.second_planting')
] + [
    ('watermelon', 'low_desert_az', 'regions.low_desert_az.' + p)
    for p in ('plantings[0]', 'resolved_by_zone.9', 'resolved_by_zone.10')
]

# Only the URL moves; the id stays, because the id is right and the document is on its own site.
REPOINT_URL = [
    ('turnip', 'ca_south_coast', 'regions.ca_south_coast.' + p)
    for p in ('plantings[0].direct_sow[0]', 'resolved_by_zone.9', 'resolved_by_zone.9.heat_pause',
              'resolved_by_zone.10', 'resolved_by_zone.10.heat_pause', 'resolved_by_zone.11',
              'resolved_by_zone.11.heat_pause')
]

# ENUMERATED, never derived. watermelon's summer nodes and edamame's varieties block.
HELD = (
    ('watermelon', 'low_desert_az',
     'regions.low_desert_az.resolved_by_zone.9.second_planting', AZ_BARE),
    ('watermelon', 'low_desert_az',
     'regions.low_desert_az.resolved_by_zone.10.second_planting', AZ_BARE),
    ('edamame', None, 'varieties', ('cornell_ext', 'https://www.vegetables.cornell.edu/')),
)

CROPS = ('cantaloupe', 'edamame', 'honeydew-melon', 'lavender', 'turnip', 'watermelon')

# Hand-written; G8 checks the DATA against these and these against the edit tables.
TOUCHED_REGIONS = {
    'cantaloupe': {'low_desert_az'}, 'honeydew-melon': {'low_desert_az'},
    'watermelon': {'low_desert_az'}, 'turnip': {'ca_south_coast'},
    'edamame': set(), 'lavender': set(),
}
FINDINGS_PER_CROP = {
    'cantaloupe': 1, 'edamame': 1, 'honeydew-melon': 1, 'lavender': 1, 'turnip': 1,
    'watermelon': 1,
}

_AZ = ('AZ1005, the University of Arizona Cooperative Extension Vegetable Planting Calendar for '
       'Maricopa County (Kai Umeda, revised 9/18), read 2026-08-05. Its grid is rotated 90 '
       'degrees, so the windows were reconstructed from character coordinates rather than read by '
       'eye, and the method was validated first against pumpkin, whose grid row (Mar 1, Mar 15, '
       'then Jul 1, Jul 15, Aug 1) reproduces our existing cell. ')

FINDINGS = [
    ('honeydew-melon', {
        'id': 'low_desert_az_honeydew_rides_a_combined_melon_row',
        'severity': 'low', 'status': 'accepted', 'blocks_launch': False,
        'summary': (_AZ + 'The low_desert_az cells now cite AZ1005 directly, and its sowing '
                    'window opens Feb 15, exactly matching this crop\'s Feb 15 - Mar 15 '
                    'plant_out. RECORDED SO IT IS NOT MISREAD LATER: honeydew has no row of its '
                    'own in that document. It rides a combined row headed "Melons, Cantaloupe '
                    'Honeydews, etc.", which runs Feb 15 through Jul 15, so the document cannot '
                    'distinguish honeydew timing from cantaloupe timing. It supports the window '
                    'we publish; it does not independently confirm that honeydew and cantaloupe '
                    'should differ, and this crop\'s later opening relative to cantaloupe remains '
                    'a modeled judgment recorded in honeydew_pilot_regional_calendars_modeled.'),
        'basis': _AZ + 'Compared against this crop\'s own low_desert_az resolved cells.',
        'filed_in_session': SESSION,
    }),
    ('cantaloupe', {
        'id': 'low_desert_az_cantaloupe_window_runs_past_az1005_at_both_ends',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'summary': (_AZ + 'The combined "Melons, Cantaloupe Honeydews, etc." row carries S '
                    '(direct seed) marks from Feb 15 continuously through Jul 15. Our cells now '
                    'cite that document and diverge from it at BOTH ends. Our spring plant_out '
                    'opens Feb 1, two weeks ahead of the document\'s first mark, and our second '
                    'planting runs Jul 15 - Aug 15 where the document\'s last mark is Jul 15. '
                    'Neither end is called an error here: Maricopa County is one part of the low '
                    'desert and our region spans more, and a fortnight at the front of a '
                    'direct-sown cucurbit window is within the range where soil temperature '
                    'rather than the calendar governs. But neither end is SOURCED, and the early '
                    'opening is the one that can cost a reader a planting, since seed going into '
                    'cold February soil rots rather than germinating. NOT retuned here, because '
                    'changing it means moving a consumer-facing date and that needs its own '
                    'evidence; the honest options are to trim to the document or to declare the '
                    'shoulders modeled. Compare the soil-temperature evidence in this crop\'s '
                    'uscrn_validation record before ruling.'),
        'basis': _AZ + 'Compared against this crop\'s own low_desert_az resolved cells and its '
                 'uscrn_validation record.',
        'filed_in_session': SESSION,
    }),
    ('watermelon', {
        'id': 'low_desert_az_watermelon_summer_planting_absent_from_az1005',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'summary': (_AZ + 'Watermelon has its OWN row in that document, separate from the '
                    'combined cantaloupe/honeydew one, and it is strikingly short: S marks at '
                    'Feb 15, Mar 1 and Mar 15, and NOTHING for the rest of the year. AZ1005 gives '
                    'low-desert watermelon a spring sowing window only. Our cells carry a second '
                    'planting at Jul 15 - Aug 15, which that document does not support at all, so '
                    'those two second_planting nodes STAY on the institution root rather than '
                    'being repointed at a document that contradicts them. The three spring nodes '
                    'are repointed. Our spring opening of Feb 1 also sits two weeks ahead of the '
                    'document, the same divergence recorded for cantaloupe. Worth noting the '
                    'asymmetry, because it is evidence rather than an oversight: the same '
                    'document gives cantaloupe and honeydew a continuous Feb-to-July window and '
                    'gives watermelon six weeks, which is a real horticultural claim about a '
                    'longer-season crop in a hot desert, not a gap in the table. Needs a ruling: '
                    'either source the summer planting elsewhere, or declare it modeled.'),
        'basis': _AZ + 'Compared against this crop\'s own low_desert_az resolved cells, and '
                 'against the cantaloupe and honeydew rows in the same table.',
        'filed_in_session': SESSION,
    }),
    ('turnip', {
        'id': 'ca_south_coast_turnip_source_supports_a_wider_window_than_we_publish',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'The seven ca_south_coast nodes cited the UC Master Gardeners San Diego County site '
            'at its bare root while eight sibling crops cited per-crop pages on that same host. '
            'They now cite the turnip page directly. TRAP WORTH RECORDING: the obvious target, '
            '/turnips/ plural to match /beets/, returns HTTP 404. The real page is /turnip/, '
            'singular, and pattern-matching a sibling url would have installed a dead link. WHAT '
            'THE PAGE ACTUALLY SAYS is wider than what we publish: "Seeds can be planted from '
            'September to May" for coastal San Diego and "September to April" inland, against our '
            'plant_out of Sep - Oct. Our window is a conservative SUBSET, so nothing here is '
            'wrong and no date is changed, but a reader in this region is being shown a shorter '
            'planting season than the cited source describes. Flagged for a content pass to '
            'decide whether to widen.'),
        'basis': 'UC Master Gardener Association of San Diego County, "Turnip" '
                 '(mastergardenersd.org/turnip/), read 2026-08-05; the /turnips/ 404 confirmed '
                 'the same day. Surfaced by tools/catalog_divergence_scan.py.',
        'filed_in_session': SESSION,
    }),
    ('edamame', {
        'id': 'edamame_varieties_no_cornell_edamame_document_exists',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': (
            'The varieties block cites cornell_ext at the bare vegetables.cornell.edu root, and '
            'it STAYS bare because no Cornell edamame variety document exists to repoint at. '
            'Searched 2026-08-05: the gardener-facing "Vegetable Varieties for Gardeners" '
            'database at vegvariety.cce.cornell.edu requires authentication and cannot be cited; '
            'the only Cornell edamame publication located is a 2014 Empire State Fruit and '
            'Vegetable Expo proceedings PDF, which is a production overview rather than a '
            'cultivar recommendation list; and the Cornell CALS soybean varieties page covers '
            'AGRONOMIC soybean by maturity group, which is a different use of the same species '
            'and cannot recommend edamame cultivars. The five cultivars listed here are '
            'corroborated by the two other sources already on this node (University of Missouri '
            'Extension and Virginia Cooperative Extension SPES-455). Surfaced by '
            'tools/catalog_divergence_scan.py as one of its eight rows; recorded so a later pass '
            'does not repoint it at the agronomic soybean page.'),
        'basis': 'vegvariety.cce.cornell.edu (authentication required); hort.cornell.edu 2014 '
                 'Expo proceedings; cals.cornell.edu field-crops soybean varieties. All checked '
                 '2026-08-05.',
        'filed_in_session': SESSION,
    }),
    ('lavender', {
        'id': 'warm_arid_lavender_plant_out_window_is_unsourced',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'The warm_arid zone 8 cell publishes plant_out "Apr - May or Sep - Oct" and cites '
            'three NMSU sources. NONE of them publishes a lavender planting date. NMSU Guide '
            'H-221 "Spices and Herbs for the Home Garden" gives lavender seed-germination '
            'guidance only (moist refrigerated storage for three days; 30 days to germinate at 65 '
            'degrees F or higher) and no planting month or season. NMSU RR-770 is "Lavender '
            'Cultivar Trial Results for North-Central New Mexico, 2003 through 2005", a research '
            'report whose only date is when the trial plot was established (June 24, 2002) and '
            'whose geography is north-central New Mexico, not the southern warm_arid band this '
            'cell describes. The NMSU low-water-plants herbaceous list covers the right taxon '
            '(Lavandula angustifolia) and gives water need, mature height and sun exposure, but '
            'states no planting time and no hardiness zone. So the window is modeled and says so '
            'nowhere. TWO CITATIONS ARE ALSO MISLABELLED, which is how this stayed invisible: '
            'the low-water list is cited under nmsu_chart, whose catalog entry is the Dona Ana '
            'Food Garden Planting Chart, and RR-770 is cited under nmsu_donaana_mg, whose catalog '
            'entry is the Dona Ana Master Gardeners site. Both are real NMSU documents cited for '
            'a claim they do not make, under ids naming documents they are not. NOT REACHABLE BY '
            'ANY SCAN IN THE REPO: this node is neither bare nor sole, so bare_host_scan and '
            'catalog_divergence_scan both pass it, and every mechanical widening of the '
            'divergence check floods.'),
        'basis': 'NMSU Guide H-221; NMSU RR-770; NMSU low-water plants herbaceous perennials and '
                 'annuals list. All three read 2026-08-05 against this crop\'s own warm_arid '
                 'zone 8 cell.',
        'filed_in_session': SESSION,
    }),
]

EM_DASH = chr(8212)
INSTITUTION = re.compile(r'Arizona|AZ1005|NMSU|Cornell|Master Gardener|UC |Missouri|Virginia')


def resolve(crop, region, path):
    node = crop['regions'][region] if region else crop
    tail = re.sub(r'^regions\.[a-z0-9_]+\.', '', path) if region else path
    for part in tail.split('.'):
        m = re.match(r'^([a-z_]+)\[(\d+)\]$', part)
        node = node[m.group(1)][int(m.group(2))] if m else node[part]
    return node


def cites(node, sid, url):
    meta = (node.get('anchoring_urls') or {}).get(sid)
    return bool(meta) and meta.get('url') == url


def reg_host(u):
    h = (urlsplit(u).hostname or '').lower()
    h = h[4:] if h.startswith('www.') else h
    p = h.split('.')
    return '.'.join(p[-2:]) if len(p) >= 2 else h


def all_urls(node, out):
    if isinstance(node, dict):
        for sid, m in (node.get('anchoring_urls') or {}).items():
            if isinstance(m, dict) and m.get('url'):
                out.append((sid, m['url']))
        for k, v in node.items():
            if k != 'anchoring_urls':
                all_urls(v, out)
    elif isinstance(node, list):
        for v in node:
            all_urls(v, out)
    return out


def prose_of(crop):
    out = {}

    def rec(n, path):
        if isinstance(n, dict):
            for k, v in n.items():
                if k == 'anchoring_urls':
                    continue
                if isinstance(v, str):
                    out['%s.%s' % (path, k)] = v
                else:
                    rec(v, '%s.%s' % (path, k))
        elif isinstance(n, list):
            for i, v in enumerate(n):
                rec(v, '%s[%d]' % (path, i))

    rec(crop.get('regions') or {}, '')
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
    catalog = data['source_catalog']

    # PREFLIGHT 1 -- every target still carries the citation this promote expects.
    for slug, region, path in REPOINT_ID:
        if not cites(resolve(crops[slug], region, path), *AZ_BARE):
            print('ABORT: %s %s no longer cites %s at %s' % (slug, path, *AZ_BARE))
            return 2
    for slug, region, path in REPOINT_URL:
        if not cites(resolve(crops[slug], region, path), *SD_BARE):
            print('ABORT: %s %s no longer cites %s at %s' % (slug, path, *SD_BARE))
            return 2
    for slug, region, path, (sid, url) in HELD:
        if not cites(resolve(crops[slug], region, path), sid, url):
            print('ABORT: held node %s %s no longer cites %s' % (slug, path, sid))
            return 2
    print('preflight: %d repoints + %d held nodes carry their pinned pre-state citation'
          % (len(REPOINT_ID) + len(REPOINT_URL), len(HELD)))

    # PREFLIGHT 2 -- coverage against the SCAN, not against this file. Every node the divergence
    # scan reports must be either repointed or explicitly held.
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    from catalog_divergence_scan import divergences  # noqa: E402
    scan_nodes = {n for v in divergences(data).values() for n in v}
    accounted = {'%s:%s' % (s, p) for s, _r, p in REPOINT_URL} | \
                {'%s:%s' % (s, p) for s, _r, p, _c in HELD if s == 'edamame'}
    if scan_nodes != accounted:
        print('ABORT: divergence scan and promote disagree.\n  scan-only: %s\n  promote-only: %s'
              % (sorted(scan_nodes - accounted), sorted(accounted - scan_nodes)))
        return 2
    print('preflight: promote covers all %d catalog_divergence_scan rows' % len(scan_nodes))

    # PREFLIGHT 3 -- nothing already filed.
    for slug, f in FINDINGS:
        if any(x.get('id') == f['id'] for x
               in ((crops[slug].get('verification_status') or {}).get('open_findings') or [])):
            print('ABORT: finding %s already filed on %s' % (f['id'], slug))
            return 2
    print('preflight: %d findings unfiled' % len(FINDINGS))

    # ---- edits -----------------------------------------------------------------------------
    applied = []
    az_url = AZ1005_URL
    for slug, region, path in REPOINT_ID:
        node = resolve(crops[slug], region, path)
        node['anchoring_urls'].pop(AZ_BARE[0])
        node['anchoring_urls'][AZ1005] = {'url': az_url, 'verified': VERIFIED}
        if isinstance(node.get('sources'), list):
            node['sources'] = [AZ1005 if s == AZ_BARE[0] else s for s in node['sources']]
        applied.append('%s %s  uariz_ext -> %s' % (slug, path.replace('regions.', ''), AZ1005))
    for slug, region, path in REPOINT_URL:
        node = resolve(crops[slug], region, path)
        node['anchoring_urls'][SD_BARE[0]] = {'url': SD_TURNIP, 'verified': VERIFIED}
        applied.append('%s %s  -> /turnip/' % (slug, path.replace('regions.', '')))
    for slug, finding in FINDINGS:
        vs = crops[slug].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(copy.deepcopy(finding))
        applied.append('%s finding %s' % (slug, finding['id']))

    # ---- guards ----------------------------------------------------------------------------
    # G1 both repoint targets are catalogued and T1.
    for sid in (AZ1005, SD_BARE[0]):
        entry = catalog.get(sid)
        if not entry or entry.get('tier') != 'T1':
            print('ABORT: %s is uncatalogued or not T1' % sid)
            return 2
    print('verified: both repoint targets are catalogued and T1')

    # G2 -- LOAD-BEARING, and the reason no catalog id is minted. Every repoint url must be
    # vouched for by evidence already in the repo, by one of two rules:
    #
    #   (a) the url IS the id's catalog url                       -- AZ1005
    #   (b) the url sits on a host this id ALREADY uses in the pre-state, on other crops
    #                                                              -- the San Diego turnip page
    #
    # A REGISTRABLE-DOMAIN match against the catalog url was tried here first and is the WRONG
    # test: `ucanr_san_diego_mg`'s catalog url is on ucanr.edu, while the county Master Gardener
    # association runs mastergardenersd.org, where eight sibling crops (beet, cabbage, spinach,
    # swiss-chard, brussels-sprouts, collards, kale and the pears) already cite per-crop pages.
    # County MG programs routinely run a separate .org alongside their university program page, so
    # a domain match rejects correct citations. Rule (b) is both looser on domain and STRICTER in
    # substance, because it demands the repo already vouch for that host under that exact id
    # rather than trusting a string comparison.
    if AZ1005_URL != catalog[AZ1005]['url']:
        print('ABORT: AZ1005_URL disagrees with the catalog entry for %s' % AZ1005)
        return 2
    # Evidence must come from OTHER crops. Computing this over the whole pre-state let the very
    # nodes being repointed vouch for their own target -- turnip's seven bare
    # `https://www.mastergardenersd.org/` citations put that host in the set, so the check could
    # never fail. Same self-referential shape as the G8 constants, caught by the same test sweep.
    bmap_pre = {c['slug']: c for c in before['crops']}
    sd_hosts = {reg_host(u)
                for slug, crop in bmap_pre.items() if slug != 'turnip'
                for sid, u in all_urls(crop, []) if sid == SD_BARE[0]}
    if reg_host(SD_TURNIP) not in sd_hosts:
        print('ABORT: %s is on a host %s never used by %s (%s)'
              % (SD_TURNIP, reg_host(SD_TURNIP), SD_BARE[0], sorted(sd_hosts)))
        return 2
    print('verified: AZ1005 is its catalog url; the turnip page is on a host this id already uses'
          ' (%s)' % ', '.join(sorted(sd_hosts)))

    # G3 -- the bare roots must be EXTINCT on every crop this promote touched.
    for slug in ('cantaloupe', 'honeydew-melon', 'turnip'):
        for sid, url in all_urls(crops[slug], []):
            if (sid, url) in (AZ_BARE, SD_BARE):
                print('ABORT: %s still cites the bare root %s' % (slug, url))
                return 2
    print('verified: the bare roots are gone from cantaloupe, honeydew-melon and turnip')

    # G4 -- the 3 held nodes must STILL be exactly as they were.
    for slug, region, path, (sid, url) in HELD:
        if not cites(resolve(crops[slug], region, path), sid, url):
            print('ABORT: %s %s was repointed but is a deliberate hold' % (slug, path))
            return 2
    print('verified: %d held nodes untouched, as intended' % len(HELD))

    # G5 -- NOT ONE CONSUMER STRING MOVES.
    bmap = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    for slug in CROPS:
        if prose_of(bmap[slug]) != prose_of(aa[slug]):
            print('ABORT: %s consumer copy changed' % slug)
            return 2
    print('verified: every consumer-facing string byte-identical across all %d crops' % len(CROPS))

    # G6 finding hygiene.
    for slug, f in FINDINGS:
        for field in ('summary', 'basis'):
            if EM_DASH in f[field]:
                print('ABORT: em dash in %s.%s' % (f['id'], field))
                return 2
        if not INSTITUTION.search(f['summary']):
            print('ABORT: finding %s names no institution' % f['id'])
            return 2
        if VERIFIED not in f['basis']:
            print('ABORT: finding %s basis carries no read date' % f['id'])
            return 2
    print('verified: %d findings dated, sourced, and free of em dashes' % len(FINDINGS))

    # G7 exact footprint.
    changed = sorted(s for s in bmap if bmap[s] != aa[s])
    if changed != sorted(CROPS):
        print('ABORT: crops changed = %s, expected %s' % (changed, sorted(CROPS)))
        return 2
    for k in before:
        if k == 'crops':
            continue
        if before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    print('verified: exactly %d crops changed, nothing else at top level' % len(CROPS))

    # G8 hand-written constants, checked against the data AND against the edit tables.
    if sorted(TOUCHED_REGIONS) != sorted(CROPS) or sorted(FINDINGS_PER_CROP) != sorted(CROPS):
        print('ABORT: the hand-written G8 constants do not cover exactly CROPS')
        return 2
    from_tables = {}
    for slug, region, _p in REPOINT_ID + REPOINT_URL:
        from_tables.setdefault(slug, set()).add(region)
    for slug in CROPS:
        if TOUCHED_REGIONS[slug] != from_tables.get(slug, set()):
            print('ABORT: TOUCHED_REGIONS[%s] = %s but the edit tables say %s'
                  % (slug, sorted(TOUCHED_REGIONS[slug]), sorted(from_tables.get(slug, set()))))
            return 2
        if FINDINGS_PER_CROP[slug] != sum(1 for s, _f in FINDINGS if s == slug):
            print('ABORT: FINDINGS_PER_CROP[%s] disagrees with FINDINGS' % slug)
            return 2
        b, a = bmap[slug], aa[slug]
        for reg in b.get('regions', {}):
            if b['regions'][reg] != a['regions'][reg] and reg not in TOUCHED_REGIONS[slug]:
                print('ABORT: %s region %s changed and is not in this pass' % (slug, reg))
                return 2
        moved = {k for k in b if k != 'regions' and b[k] != a.get(k)}
        if moved - {'verification_status'}:
            print('ABORT: %s crop-level keys changed: %s' % (slug, sorted(moved)))
            return 2
        nb = len((b.get('verification_status') or {}).get('open_findings') or [])
        na = len((a.get('verification_status') or {}).get('open_findings') or [])
        if na - nb != FINDINGS_PER_CROP[slug]:
            print('ABORT: %s gained %d findings, expected %d'
                  % (slug, na - nb, FINDINGS_PER_CROP[slug]))
            return 2
    print('verified: only the intended regions and verification_status moved, per crop')

    print('\n%d edits:' % len(applied))
    for a in applied:
        print('  ' + a)

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d edits across %d crops' % (len(applied), len(changed)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
