#!/usr/bin/env python3
"""GUARDED PROMOTE: campaign B's mid_atlantic/ncsu_ext hunt -- apricot, cherry-sour,
cherry-sweet, pomegranate.

CITATIONS AND FINDINGS ONLY. Not one consumer-facing string, date, offset or suitability moves
with this promote; a guard below proves it byte-for-byte.
Evidence: docs/2026-08-03-mid-atlantic-ncsu-ext-citation-hunt.md.

THE BLOCK. `tools/campaign_b_reprice.py` leaves these four crops as the only `mid_atlantic`
decisions still needing document work: 24 SOLE nodes, six per crop, every one citing `ncsu_ext`
at the bare host https://content.ces.ncsu.edu. They survived the re-price because, alone among
the region's 13 decisions, they carry no `mid_atlantic` finding at all.

WHAT 11 NC STATE DOCUMENTS ACTUALLY SAY -- the answers differ per crop, which is why they are
adjudicated one at a time rather than blanketed:

  apricot       ch. 15 NAMES it ("Apricot and cherry trees grow in certain areas where the
                climate is favorable, but need careful management and will not consistently bear
                fruit") and gives the planting sentence, so planting + suitability repoint.
                Table 15-6 has NO apricot row. The Toolbox says "ripens in late June to July",
                which DIVERGES from our Jul 12 - Aug 26, so harvest stays bare and is filed.
  cherry-sour   same sentence names it; same repoints. No Table 15-6 cherry row; the Toolbox
                gives only the season "Summer".
  cherry-sweet  same, EXCEPT its zone 8 cell credits NC State with a zone-8 steer toward sour
                cherry on humidity grounds that no NC State document makes (see below), so that
                one node is HELD bare rather than repointed.
  pomegranate   ch. 15 NEVER MENTIONS IT -- 0 occurrences of "pomegranate" or "punica" in the
                whole chapter. Repointing its planting nodes at the handbook would manufacture
                the exact `vce_426_331` defect `doc_mentions_crop_scan.py` exists to catch. Only
                its zone 8 cell repoints, and to the TOOLBOX (`NC Region: Coastal`, USDA 8a-10b),
                which is the one NC State document that names the plant.

Absence is document-scoped: 11 documents read, 10 readable. `producing-tree-fruit-for-home-use`
returns HTTP 403 to every agent tried while the same host served ch. 15, `bulb-onions` and its own
index at 200 in the same run -- recorded UNDETERMINED, never absence.

FOOTPRINT: 9 nodes repoint, 15 stay bare ON PURPOSE, 13 findings are filed, 1 catalog id is
minted. Nothing else in the dataset may move.

    $ python3 tools/promote_mid_atlantic_ncsu_fruit_repoint.py --dry-run
    $ python3 tools/promote_mid_atlantic_ncsu_fruit_repoint.py --apply
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
BASE_SHA = '78e5d8e3b649151e4f049aa02cf6de23f05592448942c234e1016802f5652d19'
SESSION = 'mid_atlantic_ncsu_fruit_repoint_2026_08_03'
VERIFIED = '2026-08-03'

CROPS = ('apricot', 'cherry-sour', 'cherry-sweet', 'pomegranate')
REGION = 'mid_atlantic'
BARE_ID = 'ncsu_ext'
BARE_URL = 'https://content.ces.ncsu.edu'

HANDBOOK = ('ncsu_ext_handbook_tree_fruit',
            'https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts')
TOOLBOX_POM = ('ncsu_ext_toolbox_punica_granatum',
               'https://plants.ces.ncsu.edu/plants/punica-granatum/')

# Every node in scope, addressed structurally. 'held' entries are the deliberate CASE 2 set and
# must still be citing the bare host when this promote finishes.
ROOT, PLANT_OUT, BLOOM, H_START, H_END, ZONE8 = (
    'root', 'plant_out', 'bloom', 'harvest_start', 'harvest_end', 'zone8')
ALL_NODES = (ROOT, PLANT_OUT, BLOOM, H_START, H_END, ZONE8)

REPOINTS = {
    ('apricot', ROOT): HANDBOOK,
    ('apricot', PLANT_OUT): HANDBOOK,
    ('apricot', ZONE8): HANDBOOK,
    ('cherry-sour', ROOT): HANDBOOK,
    ('cherry-sour', PLANT_OUT): HANDBOOK,
    ('cherry-sour', ZONE8): HANDBOOK,
    ('cherry-sweet', ROOT): HANDBOOK,
    ('cherry-sweet', PLANT_OUT): HANDBOOK,
    ('pomegranate', ZONE8): TOOLBOX_POM,
}

# The 15 deliberate CASE 2 nodes, enumerated rather than derived as "everything not in REPOINTS".
# Derivation made the guard self-referential and therefore VACUOUS: adding a stray entry to
# REPOINTS also removed it from the held set, so the check could not fail. Caught by mutation
# testing, which is the fifth time a guard in this arc has been green and unfailable.
HELD = tuple(sorted(
    [('apricot', BLOOM), ('apricot', H_START), ('apricot', H_END),
     ('cherry-sour', BLOOM), ('cherry-sour', H_START), ('cherry-sour', H_END),
     ('cherry-sweet', BLOOM), ('cherry-sweet', H_START), ('cherry-sweet', H_END),
     ('cherry-sweet', ZONE8),
     ('pomegranate', ROOT), ('pomegranate', PLANT_OUT), ('pomegranate', BLOOM),
     ('pomegranate', H_START), ('pomegranate', H_END)]))

# ch. 15 never names pomegranate. Citing it there is the defect this arc exists to catch, so it
# is banned structurally rather than merely left undone.
BANNED = {'pomegranate': HANDBOOK[0]}

CATALOG_ENTRY = {
    'id': TOOLBOX_POM[0],
    'name': 'NC State Extension Gardener Plant Toolbox -- Punica granatum',
    'publisher': 'NC State Extension',
    'url': TOOLBOX_POM[1],
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': '2026-08',
    'tier': 'T1',
    'citable_for': (
        'NC State Extension Gardener Plant Toolbox entry for Punica granatum. SUITABILITY: '
        '"NC Region: Coastal" and "USDA Plant Hardiness Zone: 8a, 8b, 9a, 9b, 10a, 10b"; '
        '"Although this plant prefers warm, arid regions, it can be grown in some parts of North '
        'Carolina, preferably the coastal region"; "The plant usually survives the winter but '
        'will be killed to the ground at temperatures below 10 degrees F"; "Plants grown in North '
        'Carolina may need to be planted in a protected area or in a container that can be '
        'brought indoors for the winter." SEASONS ONLY, NO DATES: "Display/Harvest Time: Fall" '
        'and "Flower Bloom Time: Fall, Spring, Summer". Publishes NO planting date and NO harvest '
        'or bloom date, which is why only the zone 8 suitability cell cites it. Backs the '
        'mid_atlantic zone 8 `marginal` call, where the stated limiter is humidity capping fruit '
        'quality rather than winter cold. The NC State PUBLICATIONS host is a different property '
        'and its Extension Gardener Handbook ch. 15 never mentions this crop at all. '
        'Parent portal entry: ncsu_ext.'),
    '_admission_provenance': (
        'Minted 2026-08-03 (campaign B, mid_atlantic/ncsu_ext hunt). Page sub-id under a trusted '
        'T1 parent (tier inherited). Read from raw bytes 2026-08-03.'),
}

_DOCSCOPE = ('Absence is scoped to the 11 NC State documents read 2026-08-03 and listed in '
             'docs/2026-08-03-mid-atlantic-ncsu-ext-citation-hunt.md, of which 10 were readable; '
             'producing-tree-fruit-for-home-use returned HTTP 403 and is recorded UNDETERMINED, '
             'not absent.')

_BLOOM = (
    'The mid_atlantic bloom window is a MODELED offset from the zone last-frost date, not a '
    'quoted datum. This crop sits outside the 10-crop roster covered by '
    'mid_atlantic_bloom_offset_undocumented, so the same absence is recorded here on its own '
    'evidence: NC State Extension Gardener Handbook ch. 15 was re-read from live bytes '
    '2026-08-03 and publishes no bloom date for any fruit crop (its bloom content is ordering '
    'and bud-kill-threshold language only), and this crop\'s Plant Toolbox entry gives the '
    'season "Spring" with no date. Repointing cannot fix an absent quantity; the derivation is '
    'declared instead. ' + _DOCSCOPE)

FINDINGS = [
    ('apricot', {
        'id': 'mid_atlantic_apricot_bloom_offset_undocumented',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': _BLOOM,
        'basis': 'Full read of NC State Extension Gardener Handbook ch. 15 and the Plant Toolbox '
                 'entry for Prunus armeniaca, from raw bytes, 2026-08-03.',
        'filed_in_session': SESSION,
    }),
    ('apricot', {
        'id': 'mid_atlantic_apricot_harvest_divergent',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'Table 15-6 of the NC State handbook ("Fruit and nut harvesting guidelines", the '
            'table earlier findings call "Table 5") has 13 fruit and nut rows and NO apricot row. '
            'The one NC State statement of apricot ripening anywhere in the documents read is the '
            'Plant Toolbox prose "The fruit is yellow to reddish in color which ripens in late '
            'June to July". Our window is Jul 12 - Aug 26 in zone 7 and Jul 5 - Aug 19 in zone 8: '
            'it reaches a full month past that source and excludes its late-June start. This is '
            'NOT the mid_atlantic_nectarine_harvest_divergent shape -- nectarine\'s overrun into '
            'August was defensible because the SAME table gives peaches "June to August" and '
            'nectarine is botanically a peach, and nothing plays that corroborating role here. '
            'The harvest arms are therefore left citing the bare host rather than repointed at a '
            'document they contradict. Needs a ruling: trim the window toward the source, or '
            'declare it modeled and say so. ' + _DOCSCOPE),
        'basis': 'NC State Plant Toolbox, Prunus armeniaca; handbook ch. 15 Table 15-6 row list '
                 'enumerated from live bytes 2026-08-03.',
        'filed_in_session': SESSION,
    }),
    ('apricot', {
        'id': 'mid_atlantic_apricot_coastal_plain_suitability_tension',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'Zone 8 (Coastal Plain) carries apricot as `marginal`, but two NC State documents '
            'place the crop outside this belt entirely. The Plant Toolbox gives Prunus armeniaca '
            '"USDA Plant Hardiness Zone: 5a, 5b, 6a, 6b, 7a, 7b" and "NC Region: Mountains, '
            'Piedmont" -- zone 8 and the Coastal Plain are both absent. Pender County, writing '
            'about southeastern North Carolina, is blunter: apricots "are nearly impossible to '
            'keep alive for more than a few years because of our hot summers and erratic '
            'springs". That is a claim about the PLANT SURVIVING, not about the crop failing to '
            'fruit, which is the stronger of the two negatives and the distinction `marginal` is '
            'meant to encode. Not changed here: a suitability flip is consumer-facing and rides '
            'on its own ruling, and the zone 7 (Piedmont) cell is not in question. ' + _DOCSCOPE),
        'basis': 'NC State Plant Toolbox, Prunus armeniaca; Pender County Extension, "Fruits and '
                 'Berries You Can Grow"; both read from raw bytes 2026-08-03.',
        'filed_in_session': SESSION,
    }),

    ('cherry-sour', {
        'id': 'mid_atlantic_cherry_sour_bloom_offset_undocumented',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': _BLOOM,
        'basis': 'Full read of NC State Extension Gardener Handbook ch. 15 and the Plant Toolbox '
                 'entry for Prunus cerasus, from raw bytes, 2026-08-03.',
        'filed_in_session': SESSION,
    }),
    ('cherry-sour', {
        'id': 'mid_atlantic_cherry_sour_harvest_undocumented',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': (
            'Table 15-6 of the NC State handbook has NO cherry row of either kind, and the Plant '
            'Toolbox entry for Prunus cerasus gives only the season "Display/Harvest Time: '
            'Summer" with no date. Our Jun 11 - Jul 6 (zone 7) / Jun 4 - Jun 29 (zone 8) window '
            'is inside that season and is not contradicted by anything read -- it is simply not '
            'published. The harvest arms stay on the bare host: repointing them at ch. 15 would '
            'cite a document for a row it does not contain. ' + _DOCSCOPE),
        'basis': 'Handbook ch. 15 Table 15-6 row list enumerated from live bytes; NC State Plant '
                 'Toolbox, Prunus cerasus; 2026-08-03.',
        'filed_in_session': SESSION,
    }),
    ('cherry-sour', {
        'id': 'mid_atlantic_cherry_coastal_plain_suitability_tension',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'Pender County, writing about southeastern North Carolina, says "Cherries, bunch '
            'grapes, raspberries, and apricots are nearly impossible to keep alive for more than '
            'a few years because of our hot summers and erratic springs" -- a claim about the '
            'PLANT SURVIVING in the Coastal Plain, stronger than the fruiting-reliability '
            'negative that mid_atlantic_cherry_sour_marginal_ruling weighed. Filed per crop, and '
            'deliberately NOT as one blanket record with apricot: the cherries do not share '
            'apricot\'s zone problem, since the Plant Toolbox gives both Prunus cerasus and '
            'Prunus avium as 3a-8b, so zone 8 is inside their published range and only the county '
            'sentence pushes against `marginal`. Needs a ruling alongside apricot\'s, not merged '
            'into it. ' + _DOCSCOPE),
        'basis': 'Pender County Extension, "Fruits and Berries You Can Grow"; NC State Plant '
                 'Toolbox, Prunus cerasus and Prunus avium; read from raw bytes 2026-08-03.',
        'filed_in_session': SESSION,
    }),

    ('cherry-sweet', {
        'id': 'mid_atlantic_cherry_sweet_bloom_offset_undocumented',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': _BLOOM,
        'basis': 'Full read of NC State Extension Gardener Handbook ch. 15 and the Plant Toolbox '
                 'entry for Prunus avium, from raw bytes, 2026-08-03.',
        'filed_in_session': SESSION,
    }),
    ('cherry-sweet', {
        'id': 'mid_atlantic_cherry_sweet_harvest_undocumented',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': (
            'Table 15-6 of the NC State handbook has NO cherry row, and the Plant Toolbox entry '
            'for Prunus avium carries NO "Display/Harvest Time" field at all -- a stricter '
            'absence than sour cherry\'s, whose entry at least gives the season "Summer". Our '
            'Jun 11 - Jul 6 (zone 7) / Jun 4 - Jun 29 (zone 8) window is therefore unpublished '
            'rather than contradicted. Recorded separately from the sour cherry finding because '
            'the two documents fail in different ways, and a shared reason would misstate one of '
            'them. ' + _DOCSCOPE),
        'basis': 'Handbook ch. 15 Table 15-6 row list enumerated from live bytes; NC State Plant '
                 'Toolbox, Prunus avium; 2026-08-03.',
        'filed_in_session': SESSION,
    }),
    ('cherry-sweet', {
        'id': 'mid_atlantic_cherry_coastal_plain_suitability_tension',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'Pender County, writing about southeastern North Carolina, says "Cherries, bunch '
            'grapes, raspberries, and apricots are nearly impossible to keep alive for more than '
            'a few years because of our hot summers and erratic springs" -- a claim about the '
            'PLANT SURVIVING in the Coastal Plain, stronger than the fruiting-reliability '
            'negative this zone 8 cell currently carries. Filed per crop, and deliberately NOT as '
            'one blanket record with apricot: the cherries do not share apricot\'s zone problem, '
            'since the Plant Toolbox gives both Prunus cerasus and Prunus avium as 3a-8b, so zone '
            '8 is inside their published range and only the county sentence pushes against '
            '`marginal`. ' + _DOCSCOPE),
        'basis': 'Pender County Extension, "Fruits and Berries You Can Grow"; NC State Plant '
                 'Toolbox, Prunus cerasus and Prunus avium; read from raw bytes 2026-08-03.',
        'filed_in_session': SESSION,
    }),
    ('cherry-sweet', {
        'id': 'mid_atlantic_cherry_sweet_sour_steer_attribution_unsupported',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'The zone 8 cell credits NC State, in BOTH consumer registers, with a recommendation '
            'it does not make: "NC State Extension steers zone 8 growers toward sour cherry '
            'instead, which tolerates this humidity far better" (seasoned) and "NC State '
            'Extension actually points zone 8 growers toward pie (sour) cherry instead, since it '
            'handles the humidity much better" (beginner). Two things are wrong with the credit, '
            'and neither is the horticultural fact. THE SCOPE: no NC State document makes a '
            'zone-8 or Coastal-Plain cherry recommendation, and the handbook\'s list of crops '
            'recommended for eastern and central North Carolina contains no cherry of either '
            'kind; the only NC State steer toward sour cherry comes from Macon County in the '
            'far-western mountains, geography this region explicitly excludes, as '
            'mid_atlantic_cherry_sour_marginal_ruling itself records. THE REASON: NC State\'s '
            'stated advantages for sour cherry are COLD HARDINESS and SELF-POLLINATION (Plant '
            'Toolbox: "much more cold hardy than sweet cherry trees and is self-pollinating"; '
            'Henderson County: sour is self fertile while sweet needs two varieties), not '
            'humidity tolerance. The tell is this crop\'s own sibling: cherry-sour\'s zone 8 cell '
            'attributes the hardiness and self-fertility facts to NC State and leaves the '
            'humidity sentence UNATTRIBUTED. cherry-sweet\'s version moved the humidity claim '
            'inside the attribution and added a zone-8 scope -- same content, shifted attribution '
            'boundary. NOT fixed here: it is consumer copy in both registers, so the rewrite is a '
            'content ruling. The zone 8 node was also HELD on the bare host rather than repointed '
            'at the handbook with the other three crops, so this promote does not make a wrong '
            'credit look better sourced. ' + _DOCSCOPE),
        'basis': 'NC State Extension Gardener Handbook ch. 15; Plant Toolbox entries for Prunus '
                 'cerasus and Prunus avium; Henderson County Extension, "Cherry Trees for Fruit"; '
                 'all read from raw bytes 2026-08-03. Cross-read against '
                 'mid_atlantic_cherry_sour_marginal_ruling.',
        'filed_in_session': SESSION,
    }),

    ('pomegranate', {
        'id': 'mid_atlantic_pomegranate_not_covered_by_ncsu_publications',
        'severity': 'low', 'status': 'accepted', 'blocks_launch': False,
        'summary': (
            'The NC State Extension Gardener Handbook ch. 15 -- the document backing the planting '
            'model for every other mid_atlantic tree fruit -- NEVER MENTIONS POMEGRANATE: 0 '
            'occurrences of "pomegranate" and 0 of "punica" in the full chapter, and no row in '
            'Table 15-1, 15-2, 15-5 or 15-6. Its plantings container and plant_out arm are '
            'therefore LEFT ON THE BARE HOST on purpose. Repointing them at ch. 15 to match the '
            'sibling crops would cite a document for a crop it does not contain, which is exactly '
            'the vce_426_331 defect tools/doc_mentions_crop_scan.py exists to catch. The one NC '
            'State document that names the plant is the Plant Toolbox entry, which publishes no '
            'planting date, so the zone 8 suitability cell repoints there and nothing else does. '
            + _DOCSCOPE),
        'basis': 'Handbook ch. 15 re-read from live bytes 2026-08-03 and word-searched; NC State '
                 'Plant Toolbox, Punica granatum.',
        'filed_in_session': SESSION,
    }),
    ('pomegranate', {
        'id': 'mid_atlantic_pomegranate_bloom_window_narrower_than_source',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'Unlike the other three crops in this hunt, pomegranate\'s bloom is not simply '
            'undocumented -- a datum exists and our window does not match its extent. NC State '
            'Beaufort County publishes "The bloom season is incredibly long, beginning in April '
            'and lasting well into the fall", and the Plant Toolbox gives "Flower Bloom Time: '
            'Fall, Spring, Summer" with a flower description of clusters "in early summer to '
            'fall". Our cell models a 30-day window: Apr 29 - May 29 in zone 8, May 6 - Jun 5 in '
            'zone 7. The April start is consistent for zone 8 and not for zone 7, and neither '
            'zone reflects a season the source describes as running into fall. Recorded rather '
            'than resolved: widening a bloom window changes what the calendar renders, and the '
            'source is month-granular outreach prose, not a dated table. Filed SEPARATELY from '
            'the three bloom_offset_undocumented records for this reason -- blanketing them would '
            'assert absence where a datum exists. ' + _DOCSCOPE),
        'basis': 'NC State Beaufort County Extension, "Have You Ever Had a Pomegranate Martini?"; '
                 'NC State Plant Toolbox, Punica granatum; read from raw bytes 2026-08-03.',
        'filed_in_session': SESSION,
    }),
    ('pomegranate', {
        'id': 'mid_atlantic_pomegranate_harvest_season_only',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': (
            'The Plant Toolbox gives "Display/Harvest Time: Fall" and describes edible fruit "in '
            'fall". The SEASON is supported and our Sep 13 - Oct 18 (zone 7) / Sep 6 - Oct 11 '
            '(zone 8) window sits inside it, but no NC State document publishes a pomegranate '
            'harvest DATE, so the arms stay on the bare host. NOTE FOR THE NEXT READER, because '
            'it is a trap: NC State Brunswick County\'s "Try a Pomegranate" does contain the '
            'sentence "They are usually readily available from October through December", but '
            'that is a nutrition and recipe column about SUPERMARKET AVAILABILITY OF CALIFORNIA '
            'FRUIT, not a North Carolina harvest window. It must not be cited here. ' + _DOCSCOPE),
        'basis': 'NC State Plant Toolbox, Punica granatum; NC State Brunswick County Extension, '
                 '"Try a Pomegranate", read and rejected; 2026-08-03.',
        'filed_in_session': SESSION,
    }),
]

EM_DASH = chr(8212)
INSTITUTION = re.compile(r'NC State|NCSU|North Carolina State|Plant Toolbox|'
                         r'University of Arkansas|UAEX|Virginia')


def nodes_of(crop):
    """-> {node key: the dict carrying `sources` / `anchoring_urls`}."""
    reg = crop['regions'][REGION]
    p = reg['plantings'][0]
    return {
        ROOT: p,
        PLANT_OUT: p['plant_out'][0],
        BLOOM: p['bloom'][0],
        H_START: p['harvest_start'][0],
        H_END: p['harvest_end'][0],
        ZONE8: reg['resolved_by_zone']['8'],
    }


def cites_bare(node):
    return (node.get('sources') == [BARE_ID]
            and (node.get('anchoring_urls') or {}).get(BARE_ID, {}).get('url') == BARE_URL)


def prose_of(crop):
    """Every consumer-facing string in this crop's mid_atlantic cells, for the no-copy-moved guard."""
    out = {}
    for z, cell in crop['regions'][REGION]['resolved_by_zone'].items():
        for k, v in cell.items():
            if isinstance(v, str):
                out['%s.%s' % (z, k)] = v
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

    # PREFLIGHT 1 -- the premise. All 24 nodes must still be SOLE on the bare host. If a repoint
    # landed in the meantime this promote's evidence is stale and it must not run.
    for slug in CROPS:
        for key, node in nodes_of(crops[slug]).items():
            if not cites_bare(node):
                print('ABORT: %s %s no longer cites the bare host SOLE -- premise changed'
                      % (slug, key))
                return 2
    print('preflight: all %d nodes still cite %s SOLE at the bare host'
          % (len(CROPS) * len(ALL_NODES), BARE_ID))

    # Campaign A's pear lesson (never inherit the bare URL from a global map) is satisfied by the
    # check above, which compares each node's url to BARE_URL individually. A separate
    # "do all four decisions share one url" pass was written here and REMOVED as unfailable:
    # cites_bare already pins the exact URL per node, so the set check could never see a second
    # value that preflight 1 had not already rejected.

    # PREFLIGHT 2 -- nothing already filed, nothing already catalogued.
    for slug, f in FINDINGS:
        existing = [x.get('id') for x
                    in ((crops[slug].get('verification_status') or {}).get('open_findings') or [])]
        if f['id'] in existing:
            print('ABORT: finding %s already filed on %s' % (f['id'], slug))
            return 2
    if CATALOG_ENTRY['id'] in data['source_catalog']:
        print('ABORT: catalog id %s already exists' % CATALOG_ENTRY['id'])
        return 2
    print('preflight: %d findings unfiled, catalog id unminted' % len(FINDINGS))

    # ---- the edits -------------------------------------------------------------------------
    applied = []
    data['source_catalog'][CATALOG_ENTRY['id']] = copy.deepcopy(CATALOG_ENTRY)
    applied.append('catalog + %s' % CATALOG_ENTRY['id'])

    for (slug, key), (sid, url) in sorted(REPOINTS.items()):
        node = nodes_of(crops[slug])[key]
        node['sources'] = [sid]
        node['anchoring_urls'] = {sid: {'url': url, 'verified': VERIFIED}}
        applied.append('%s %s -> %s' % (slug, key, sid))

    for slug, finding in FINDINGS:
        vs = crops[slug].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(copy.deepcopy(finding))
        applied.append('%s finding %s' % (slug, finding['id']))

    # ---- guards ----------------------------------------------------------------------------
    # G1 every repointed node's URL must match what the CATALOG says that id resolves to.
    # NOTE: a pair of checks re-reading `sources` and `anchoring_urls` stood here and were REMOVED
    # as unfailable -- they read back the two lines that had just written them. This version is a
    # real cross-check between two independently authored structures, and mutation testing
    # confirms it fails when they disagree.
    for (slug, key), (sid, url) in REPOINTS.items():
        entry = data['source_catalog'].get(sid)
        if not entry:
            print('ABORT: %s %s repoints at uncatalogued id %s' % (slug, key, sid))
            return 2
        if entry.get('url') != url:
            print('ABORT: %s %s url %r disagrees with catalog id %s (%r)'
                  % (slug, key, url, sid, entry.get('url')))
            return 2
        if entry.get('tier') != 'T1':
            print('ABORT: %s %s repoints at non-T1 id %s' % (slug, key, sid))
            return 2
    print('verified: %d repoints agree with the catalog and are all T1' % len(REPOINTS))

    # G2 -- LOAD-BEARING. The 15 held nodes are the point of the hunt as much as the 9 repointed
    # ones. Each must STILL be on the bare host: a "helpful" extra repoint is a defect here.
    # COVERAGE, deliberately not an overlap check. Every node in scope must be accounted for by
    # one list or the other, so a node cannot be silently forgotten. Overlap is NOT rejected
    # here on purpose: if a node is wrongly added to REPOINTS it stays in HELD too, and the
    # data check below is then the thing that fires -- which is the stronger statement, because
    # it reads what was actually written rather than what was configured. An overlap check here
    # would preempt it and make the real guard unfailable.
    if set(HELD) | set(REPOINTS) != {(s, k) for s in CROPS for k in ALL_NODES}:
        print('ABORT: HELD + REPOINTS do not cover all %d nodes in scope'
              % (len(CROPS) * len(ALL_NODES)))
        return 2
    for slug, key in HELD:
        if not cites_bare(nodes_of(crops[slug])[key]):
            print('ABORT: %s %s was repointed but is a deliberate CASE 2 node' % (slug, key))
            return 2
    print('verified: %d CASE 2 nodes still bare, as intended' % len(HELD))

    # G3 -- LOAD-BEARING. ch. 15 never names pomegranate; it may not appear anywhere on that crop.
    for slug, banned_id in BANNED.items():
        blob = json.dumps(crops[slug], ensure_ascii=False)
        for node in nodes_of(crops[slug]).values():
            if banned_id in (node.get('sources') or []) or banned_id in (node.get('anchoring_urls') or {}):
                print('ABORT: %s cites %s, a document that never mentions the crop'
                      % (slug, banned_id))
                return 2
        if HANDBOOK[1] in blob:
            print('ABORT: %s references the handbook URL, which never mentions the crop' % slug)
            return 2
    print('verified: pomegranate cites no document that does not name it')

    # G4 -- NOT ONE CONSUMER STRING MOVES. This promote is citations and findings only.
    bmap = {c['slug']: c for c in before['crops']}
    for slug in CROPS:
        b, a = prose_of(bmap[slug]), prose_of(crops[slug])
        if b != a:
            diff = sorted(k for k in b if b.get(k) != a.get(k))
            print('ABORT: %s consumer copy changed: %s' % (slug, diff))
            return 2
    print('verified: every consumer-facing string byte-identical across all 4 crops')

    # G5 no finding text may carry an em dash, and every one must name its documents.
    for slug, f in FINDINGS:
        for field in ('summary', 'basis'):
            if EM_DASH in f[field]:
                print('ABORT: em dash in %s.%s' % (f['id'], field))
                return 2
        if not INSTITUTION.search(f['summary']):
            print('ABORT: finding %s names no institution' % f['id'])
            return 2
        if '2026-08-03' not in f['basis']:
            print('ABORT: finding %s basis carries no read date' % f['id'])
            return 2
    print('verified: %d findings dated, sourced, and free of em dashes' % len(FINDINGS))

    # G6 zone 7 is not in this hunt and must be untouched on all four crops.
    for slug in CROPS:
        if (bmap[slug]['regions'][REGION]['resolved_by_zone']['7']
                != crops[slug]['regions'][REGION]['resolved_by_zone']['7']):
            print('ABORT: %s zone 7 changed, it is not in this hunt' % slug)
            return 2
    print('verified: zone 7 untouched on all 4 crops')

    # G7 exact footprint -- only these crops, only source_catalog beside them.
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in bmap if bmap[s] != aa[s])
    if changed != sorted(CROPS):
        print('ABORT: crops changed = %s, expected %s' % (changed, sorted(CROPS)))
        return 2
    for k in before:
        if k in ('crops', 'source_catalog'):
            continue
        if before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    # Two catalog checks stood here -- "exactly one id was added" and "no existing entry was
    # modified" -- and both were REMOVED as unfailable: this promote writes exactly one new key
    # and never touches an existing one, so neither could fail whatever was injected. The
    # preflight collision check is the reachable version of the same guarantee.
    print('verified: exactly 4 crops changed, nothing else at top level')

    # G8 within each crop, only the intended regions/keys moved.
    for slug in CROPS:
        b, a = bmap[slug], aa[slug]
        for reg in b.get('regions', {}):
            if reg != REGION and b['regions'][reg] != a['regions'][reg]:
                print('ABORT: %s region %s changed' % (slug, reg))
                return 2
        moved = {k for k in b if k != 'regions' and b[k] != a.get(k)}
        if moved != {'verification_status'}:
            print('ABORT: %s crop-level keys changed: %s' % (slug, sorted(moved)))
            return 2
        nb = len((b.get('verification_status') or {}).get('open_findings') or [])
        na = len((a.get('verification_status') or {}).get('open_findings') or [])
        want = sum(1 for s, _f in FINDINGS if s == slug)
        if na - nb != want:
            print('ABORT: %s gained %d findings, expected %d' % (slug, na - nb, want))
            return 2
    print('verified: only mid_atlantic and verification_status moved, per crop')

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
