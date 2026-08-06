#!/usr/bin/env python3
"""PLA-114 promote: lemon's cold anchor. Base 6b2dcb8e.

WHAT THIS DOES, and nothing else:

  1. mints `uc_anr_8100` (UC ANR Publication 8100, Frost Protection for Citrus and Other
     Subtropicals -- Geisel & Unruh 2003), recording that its URL is USER-AGENT GATED
  2. `lemon.frost_tolerance_f` 28 -> 29, and adds `uc_anr_8100` to lemon's source_set
  3. repoints nine bare citations onto the documents that support what those cells claim
  4. files five findings, F1-F5

IT MOVES NO CONSUMER PROSE. That is deliberate and it is the corrected disposition, not an
oversight. An earlier draft wanted to rewrite the fourteen strings that assert the high-20s
threshold for leaves AND fruit, on the theory that the leaf half was unsupported. That draft was
wrong twice over:

  * HS402's 22-24F is DEFOLIATION -- leaf drop, a severity ENDPOINT further along the same damage
    curve -- not a competing leaf-damage onset. 8100 frames the curve explicitly: "Greater damage
    occurs with colder temperatures, a longer duration of cold, or higher relative humidity."
  * 8100's 29F covers foliage, because it says PLANTS: "when temperatures fall to 29F for 30
    minutes or longer, some frost damage to tender citrus plants will occur", under a "Trees"
    heading that contrasts with a separate "Fruits" section.

The axis is ONSET vs ENDPOINT, not leaves vs trees. And none of the fourteen asserts leaf DEATH at
the threshold: all use "damaged"/"injured", and every lethality clause is scoped to a different
subject under a colder, separately-named condition. Counting lethality verbs per string flags 8 of
14; reading which noun each verb governs flags 0. `test_promote_pla114_lemon_cold.py` pins all
fourteen byte-identical so a later pass cannot quietly "fix" correct prose.

WHAT IT DELIBERATELY LEAVES BARE, because those hunts are still OPEN:
  * `se_gulf` z8 `clemson_hgic`      -- hunt #28
  * `ca_interior` z8/z9 `ucanr_ext`  -- hunt #3
  * `warm_arid` plantings + plant_out -- F3; hunt #31 covered 1 of its 3 nodes, not 3

Usage: python3 tools/promote_pla114_lemon_cold.py [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '6b2dcb8ed4f51c833fa4d44845b15e7f609079a24a544af025c067dfca45d4db'

CLEMSON_COLD = 'https://hgic.clemson.edu/cold-tolerance-in-citrus/'
TAMU_CITRUS = 'https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/'
IPM_FREEZE = 'https://ipm.ucanr.edu/home-and-landscape/freezing-and-frost-damage-to-citrus/'
UC8100_URL = 'https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf'

# (region, zone, source_id) -> new url. ENUMERATED, so the guard suite can assert COVERAGE rather
# than overlap ([[guard-derived-from-what-it-checks-is-vacuous]]).
REPOINTS = (
    [('northern_tier', z, 'clemson_hgic', CLEMSON_COLD) for z in ('3', '4', '5', '6', '7')]
    + [('northern_tier', z, 'tamu_agrilife', TAMU_CITRUS) for z in ('3', '4', '5', '6', '7')]
    + [('se_gulf', '8', 'tamu_agrilife', TAMU_CITRUS),
       ('warm_arid', '8', 'tamu_agrilife', TAMU_CITRUS),
       ('warm_arid', '8', 'clemson_hgic', CLEMSON_COLD),
       ('ca_interior', '8', 'uc_ipm', IPM_FREEZE),
       ('ca_interior', '9', 'uc_ipm', IPM_FREEZE)]
)

UC8100 = {
    'id': 'uc_anr_8100',
    'name': 'UC ANR Publication 8100, Frost Protection for Citrus and Other Subtropicals '
            '(Geisel & Unruh, 2003)',
    'publisher': 'University of California Agriculture and Natural Resources',
    'url': UC8100_URL,
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'tier': 'T1',
    'accessed': '2026-08',
    'citable_for': 'ANONYMOUSLY PEER-REVIEWED numbered UC ANR publication (DOI 10.3733/ucanr.8100), '
                   'the citrus frost anchor for this dataset. Publishes, under a "Trees" heading '
                   'kept separate from its "Fruits" section: damage ONSET for tender citrus at 29F '
                   '(-1.7C) sustained 30 minutes or longer. Table 1 (relative frost sensitivity, '
                   'no temperatures, H/M/L only): citron H, grapefruit M, kumquat L, lemon Citrus '
                   'limon H, lime H, mandarin M, orange M, Satsuma L. Table 2 (critical frost '
                   'damage temperatures, FRUIT): lemon buds and blossoms 27.0F; button lemons '
                   '<1/2in 29.5-30.5F; green lemons >1/2in 27.0-29.5F; tree-ripe lemons 26.0-30.5F. '
                   'It frames a damage CURVE, not a cliff: "Greater damage occurs with colder '
                   'temperatures, a longer duration of cold, or higher relative humidity." Table 1 '
                   'is TREES and Table 2 is FRUIT -- do NOT read the fruit table onto a foliage '
                   'field. FETCH TRAP: this URL is USER-AGENT GATED. A plain fetch returns HTTP 202 '
                   'with Content-Type text/html and ZERO bytes, a success status carrying no '
                   'document; send a browser user-agent and it returns HTTP 200 with the 245,883-'
                   'byte PDF. Read it from raw bytes via pypdf, never WebFetch. The anrcatalog.'
                   'ucanr.edu path for 8100 is DEAD -- it redirects to a generic ANR Publishing '
                   'landing page served as HTTP 200 text/html.',
}

SESSION = 'pla114_lemon_cold_2026_08_06'

FINDINGS = [
    {
        'id': 'lemon_cold_threshold_was_miscredited_now_uc8100',
        'severity': 'medium',
        'status': 'resolved',
        'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'lemon carried frost_tolerance_f = 28 and a "high-20s F" prose claim while '
            'hardiness_notes_seasoned credited "Clemson HGIC, Texas A&M AgriLife, UF/IFAS". Of '
            'those three, ONLY UF/IFAS publishes lemon cold figures: HS1153/HS402 "Lemon Growing '
            'in the Florida Home Landscape" (cited by this crop as uf_ifas_hs1153) gives '
            'defoliation at 22-24F, severe wood damage at 20F, flowers and young fruit killed at '
            '29F, and mature fruit damaged at 28F to 31F. Clemson\'s cold-tolerance page publishes '
            'satsuma and kumquat at 15F and no lemon number; TAMU\'s citrus fact sheet publishes '
            'satsuma 18F plus freeze-protection operating points (sprinkler 28F calm / 30F windy) '
            'and no lemon number. So the mis-credit is TWO of three, not three of three. RESOLVED '
            'by minting uc_anr_8100 (UC ANR 8100), which publishes the damage ONSET for tender '
            'citrus at 29F sustained 30 minutes or longer and whose Table 1 rates lemon Citrus '
            'limon H, and by moving frost_tolerance_f 28 -> 29 to match that onset. HISTORY WORTH '
            'KEEPING: an earlier pass reported this number appeared in 0 of the 17 readable '
            'documents lemon cites and nearly filed that as an absence. The zero was the '
            'instrument -- the scan required a temperature to be "lemon-adjacent", and in HS402 '
            'the nearest "lemon" is 333 characters from the figures because on a crop monograph '
            'the crop is the section subject and the passage\'s own subject noun is "trees". Any '
            'proximity window under ~333 chars returns a confident zero. tools/cited_claim_scan.py '
            'is the regression. STILL OWED, deliberately not done here because this promote moved '
            'no consumer prose: the hardiness_notes_seasoned credit parenthetical still reads '
            '"(Sources: Clemson HGIC, Texas A&M AgriLife, UF/IFAS.)" and should name UC ANR 8100 '
            'and UF/IFAS HS402 for the number.'),
    },
    {
        'id': 'lemon_ca_interior_uc_ipm_repointed_to_freeze_page',
        'severity': 'low',
        'status': 'resolved',
        'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'lemon ca_interior zone 8 and zone 9 cited uc_ipm at the bare host https://ipm.ucanr.edu. '
            'The two UC IPM citrus pages lemon cites elsewhere (agriculture/citrus/ and the home '
            'and landscape citrus page) are pest and disease documents carrying zero occurrences '
            'of "hardy", "cold hard" or any temperature, so the first read of this hunt called it '
            'CASE 2, a right-document-wrong-claim dead end. That was scoped to the two pages we '
            'cite and was wrong about the host: UC IPM publishes a freezing-and-frost-damage-to-'
            'citrus page we did NOT cite, verified live at HTTP 200, which states that "Eureka '
            'lemon and grapefruit are among the most cold-sensitive scions, whereas mandarin, '
            'Meyer lemon, and sweet orange are more cold hardy". Both cells are SUITABILITY cells '
            '(survives_no_fruit at z8, marginal at z9) and a sensitivity RANKING is exactly the '
            'right support for a suitability enum, so both are repointed. SCOPE IT: that page '
            'publishes a ranking and NO temperature -- it must not be cited for the numeric '
            'threshold. The ucanr_ext arm of these same two cells stays bare; that is hunt #3 and '
            'it is still open.'),
    },
    {
        'id': 'lemon_warm_arid_plantings_no_citrus_document',
        'severity': 'low',
        'status': 'open',
        'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'lemon warm_arid plantings[0] and its plant_out[0] arm cite bare uariz_ext '
            '(https://extension.arizona.edu) and bare clemson_hgic (https://hgic.clemson.edu), and '
            'NO sibling citrus crop cites a pathed document for either node. Arizona\'s dominant '
            'pathed document in this dataset is AZ1005, a VEGETABLE planting calendar, which is '
            'the campaign-A shape of a vegetable table standing as sole source on a tree crop. '
            'CASE 2: no document hunt remains, what is left is authoring. Recorded because the '
            'decision-level verdict masked it -- hunt #31 read SIBLING-PATHED on the strength of '
            'ONE zone cell while covering 1 of its 3 nodes, and the zone-8 cell (which does have a '
            'sibling document) is repointed in this same promote while these two are deliberately '
            'left bare.'),
    },
    {
        'id': 'lemon_tamu_table_1_not_in_text_layer',
        'severity': 'low',
        'status': 'open',
        'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'The TAMU citrus fact sheet (aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/) '
            'refers in prose to a "Table 1" of variety characteristics which may carry a cold-'
            'hardiness column, but that table is NOT present in the cached text layer of the page. '
            'UNDETERMINED, not an absence: the document is readable and is not a WAF block, so the '
            'table is either an image, a separate asset, or dropped by extraction. It is the one '
            'thing that could still change the answer on hunts #26 and #27, whose zone cells are '
            'repointed at this document in this promote on the strength of its cold-hardy-types '
            'list (which excludes lemon) rather than on any table.'),
    },
    {
        'id': 'lemon_cold_threshold_single_source_divergence',
        'severity': 'low',
        'status': 'resolved',
        'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'Six T1 citrus cold documents were read for a lemon-applicable damage temperature, and '
            'they do not agree. Recorded so the next reader does not re-hunt this. UC ANR 8100 '
            'publishes 29F as the damage ONSET for tender citrus, qualified "for 30 minutes or '
            'longer", under a "Trees" heading kept separate from its "Fruits" section, and it '
            'discriminates by sensitivity class: its Table 1 rates lemon Citrus limon H. LSU '
            'AgCenter publishes about 26F for leaf or wood damage, but as ONE category-level figure '
            'for "all other citrus" -- everything except satsumas and kumquats, which lumps M-rated '
            'grapefruit and orange in with H-rated lemon and lime. 8100 wins on SCOPE, not on being '
            'the warmer number: it is the more specific instrument for a crop its own table rates '
            'H. CRITICALLY, 8100 frames a damage CURVE and not a cliff ("Greater damage occurs with '
            'colder temperatures, a longer duration of cold, or higher relative humidity"), so a '
            'colder figure further along that curve is NOT a contradiction: UF/IFAS HS402 gives '
            'lemon-specific DEFOLIATION at 22-24F and severe wood damage at 20F, which are severity '
            'ENDPOINTS, never competing onsets. Fruit is a separate axis again: HS402 gives mature '
            'fruit damage at 28-31F and 8100 Table 2 gives buds and blossoms 27.0F and tree-ripe '
            'lemons 26.0-30.5F. Documents that publish NO lemon-applicable damage temperature at '
            'all: Clemson cold-tolerance (satsuma and kumquat 15F only), TAMU citrus fact sheet '
            '(satsuma 18F and freeze-protection operating points), UF/IFAS HS132 (cold annotations '
            'for calamondin, kumquat and Key lime, and none for lemon), UC IPM freeze page (a '
            'ranking, zero temperatures). Twelve of lemon\'s 29 cited URLs are uncached and remain '
            'UNDETERMINED rather than silent.'),
    },
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    raw = open(CANONICAL, 'rb').read()
    got = hashlib.sha256(raw).hexdigest()
    if got != BASE_SHA:
        print(f'ABORT: canonical is {got[:16]}, expected base {BASE_SHA[:16]}', file=sys.stderr)
        return 1
    print(f'base SHA verified: {got[:16]}')

    data = json.loads(raw)
    lemon = next(c for c in data['crops'] if c['slug'] == 'lemon')

    if 'uc_anr_8100' in data['source_catalog']:
        print('ABORT: uc_anr_8100 already in source_catalog', file=sys.stderr)
        return 1
    data['source_catalog']['uc_anr_8100'] = UC8100
    data['source_catalog'] = dict(sorted(data['source_catalog'].items()))
    print('minted uc_anr_8100')

    assert lemon['frost_tolerance_f'] == 28, lemon['frost_tolerance_f']
    assert lemon['frost_effect'] == 'foliage_damaged', lemon['frost_effect']
    lemon['frost_tolerance_f'] = 29
    print('frost_tolerance_f 28 -> 29')

    source_set = lemon['verification_status']['source_set']
    assert 'uc_anr_8100' not in source_set
    source_set.append('uc_anr_8100')
    source_set.sort()
    print('source_set += uc_anr_8100')

    for region, zone, sid, url in REPOINTS:
        cell = lemon['regions'][region]['resolved_by_zone'][zone]
        entry = cell['anchoring_urls'][sid]
        assert entry['url'] != url, f'{region}/{zone}/{sid} already repointed'
        print(f'  repoint {region}/z{zone}/{sid}: {entry["url"]} -> {url}')
        entry['url'] = url
        entry['verified'] = '2026-08-06'

    existing = {f['id'] for f in lemon['verification_status']['open_findings']}
    for finding in FINDINGS:
        assert finding['id'] not in existing, finding['id']
        lemon['verification_status']['open_findings'].append(finding)
    print(f'filed {len(FINDINGS)} findings')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN -- would write {len(out)} bytes, sha {new_sha}')
        return 0
    with open(CANONICAL, 'wb') as fh:
        fh.write(out)
    print(f'wrote {len(out)} bytes\nnew canonical SHA: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
