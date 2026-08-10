#!/usr/bin/env python3
"""PLA-155: vce_426_331 -- the confirmed wrong credits, corrected per claim. Base ce9eb12f.

WHAT THIS DOES (from docs/2026-08-10-pla155-vce-426-331-classification.md; citations, anchors,
findings and four synthesis-note pub-number strings only -- ZERO consumer-facing values move):

  1. Mints two catalog ids for documents read in full 2026-08-10 and now cached:
     vce_426_840 (Small Fruit in the Home Garden) and vce_spes_455 (Edamame in Virginia II).
  2. sweet-pea mid_atlantic z7/z8 + region list: ncsu_ext (Lathyrus odoratus Plant Toolbox,
     cached, right taxon) joins the SOLE vce_426_331 credit; the declared Peas-garden analog is
     registered as an accepted_modeled finding. vce_426_331 SURVIVES here on purpose: the cell
     notes have always declared the analog, the doc's zone frost table and its "no fall sowing"
     for garden peas are claim-true, and harvest = start_indoors + 85d is the crop's own
     certified mid days-to-bloom (cert finding_004) -- the values are NOT wrong, the sole credit
     was.
  3. strawberry mid_atlantic z7 cell + 4 rule-layer arms + region list: WRONG PUB NUMBER
     corrected, 426-331 -> 426-840 (the matted-row/renovation/frost-sensitivity content the
     synthesis notes attribute is IN 426-840 and absent from 426-331). Two divergences filed
     open, values NOT moved (plant offset 2wk vs the doc's 3-4wk; ripening/flush offsets
     unpublished).
  4. blueberry / raspberry / blackberry mid_atlantic cells + region lists: ride-along
     vce_426_331 credit (zero berry content) swaps to vce_426_840 (real planting-season
     statements for both crop groups). NCSU pathed anchors untouched.
  5. elderberry mid_atlantic: vce credit REMOVED (0 elderberry in 426-331 AND 426-840); cells
     stay on institution-root ncsu_ext, mirroring the accepted mid_south finding.
  6. edamame crop-level (6 nodes + anchors + source_set): id/document divergence corrected to
     vce_spes_455 -- the claims (B. japonicum inoculant, 7-10 day harvest window, low N) are
     verbatim in SPES-455 and absent from 426-331; two anchors already pointed at the SPES-455
     URL under the wrong id.

WHAT IT DELIBERATELY DOES NOT DO: the ~55 in-document vegetables (values spot-checked EXACT
against the doc's 7a/8a rows) are untouched. The declared borrows (shallot, arugula, bok-choy,
grain corns) are untouched -- grain-corn bands are Trevor-ratified (PLA-156). The frost-anchored
perennials (herbs, tree fruit) keep vce_426_331: Table 1 is zone-scoped and carries their
declared frost anchors. northern_tier divergences are PLA-195 block (d), recorded there, not
touched. Legacy zones{} untouched (ruled LEAVE). No consumer string, date, calendar or
suitability value moves.

Usage: python3 tools/promote_pla155_vce.py [--dry-run] [canonical.json]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'ce9eb12fb85abf9f592ee8bc6621102a5dd785327a74befe2b0e7ddc8146bff5'

URL_331 = 'https://www.pubs.ext.vt.edu/426/426-331/426-331.html'
URL_840 = 'https://www.pubs.ext.vt.edu/426/426-840/426-840.html'
URL_455 = 'https://www.pubs.ext.vt.edu/SPES/spes-455/spes-455.html'
URL_LATHYRUS = 'https://plants.ces.ncsu.edu/plants/lathyrus-odoratus/'
VERIFIED = '2026-08-10'

CAT_840 = {
    'id': 'vce_426_840',
    'name': 'Virginia Cooperative Extension Publication 426-840 (Small Fruit in the Home Garden)',
    'publisher': 'Virginia Tech',
    'url': URL_840,
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': '2026-08',
    'tier': 'T1',
    'citable_for': 'Small fruit culture for Virginia home gardens: strawberries (matted row, '
                   'renovation, planting 3-4 weeks pre-frost), blueberries, caneberries, grapes. '
                   'Mid-Atlantic regional coverage. NO elderberry content.',
}
CAT_455 = {
    'id': 'vce_spes_455',
    'name': 'Virginia Cooperative Extension Publication SPES-455 (Edamame in Virginia II: '
            'Producing a High-Quality Product)',
    'publisher': 'Virginia Tech',
    'url': URL_455,
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': '2026-08',
    'tier': 'T1',
    'citable_for': 'Edamame (vegetable soybean) production for Virginia: variety selection, '
                   'Bradyrhizobium japonicum inoculation, nitrogen management, 7-10 day harvest '
                   'window.',
}

# Pre-state strings this promote touches, pinned byte-for-byte. A mismatch means canonical is not
# the state this transform was written against -- abort, never fuzzy-match.
STRAW_NOTES_OLD = {
    'plant_out': 'Set dormant bare-root crowns about two weeks before the last spring frost, as '
                 'soon as the soil can be worked; the crowns are dormant stock, so there is no '
                 'need to wait out frost danger (VCE 426-331 home garden matted-row guidance).',
    'bloom': 'On an established matted-row bed, June-bearing plants begin flowering in the weeks '
             'after the last frost; open blossoms are frost-sensitive (VCE 426-331).',
    'harvest_start': "June-bearing strawberries ripen roughly six weeks after the last frost in "
                     "the Piedmont's matted-row system (VCE 426-331).",
    'harvest_end': 'The June-bearing flush runs about four weeks. Renovate the matted row within '
                   'two weeks of the last picking: mow the leaves above the crowns, narrow the '
                   'row, and fertilize (VCE 426-331).',
}
STRAW_NOTES_NEW = {k: v.replace('VCE 426-331', 'VCE 426-840') for k, v in STRAW_NOTES_OLD.items()}

FINDINGS = {
    'sweet-pea': {
        'id': 'sweet_pea_mid_atlantic_vce_pea_row_analog',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'filed_in_session': 'pla155_vce_426_331_classification',
        'summary': (
            "mid_atlantic z7/z8 windows are the declared Peas-garden ANALOG. vce_426_331 "
            "(Virginia's Home Garden Vegetable Planting Guide, read in full 2026-08-10) contains "
            "0 occurrences of 'sweet pea' and 0 of 'Lathyrus'; the set-out window is its Pisum "
            "sativum 'Peas, garden' row (z7a Mar 1 - Apr 1; z8a Feb 20 - Apr 1) applied to this "
            "ornamental as the belt's cool-season pea-timing analog, exactly as the cell notes "
            "have always declared. start_indoors applies the crop's own weeks_indoors=6, and "
            "harvest is start_indoors + 85 days -- the crop's own certified mid days-to-bloom "
            "(sweet-pea_pilot_finding_004) -- so the values are internally coherent with the "
            "certified biology and with the crop-wide modeled-windows declaration "
            "(sweet-pea_pilot_finding_001). Two claims ARE document-true: the zone frost table "
            "(Table 1, zone-scoped) and 'no fall sowing listed' for garden peas. ncsu_ext "
            "(Lathyrus odoratus Plant Toolbox, cached, right taxon) added 2026-08-10 to carry "
            "the biology claims (cool-season annual, frost-tolerant seedlings, toxic seed). "
            "Absence scoped to the documents read 2026-08-10."),
    },
    'strawberry': {
        'id': 'mid_atlantic_strawberry_vce_pub_number_corrected',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'filed_in_session': 'pla155_vce_426_331_classification',
        'summary': (
            "The z7 cell and all four rule-layer arms credited 'VCE 426-331 home garden "
            "matted-row guidance' -- a publication with NO strawberry row and no matted-row "
            "content (read in full 2026-08-10). The attributed content is in VCE 426-840, Small "
            "Fruit in the Home Garden (fetched live 2026-08-10, now cached): matted-row system, "
            "renovation soon after harvest, blossoms 'easily killed by frost', and 'dormant "
            "crowns in early spring, about three or four weeks before the average date of the "
            "last frost'. Citations and synthesis-note pub numbers repointed 2026-08-10; date "
            "values NOT moved. Residual divergences kept open: (1) the z7 plant_out opens Apr 1, "
            "about two weeks before the Apr 15 frost anchor, vs the document's 'three or four "
            "weeks before' (roughly Mar 18-25); (2) the 'ripen roughly six weeks after last "
            "frost' and 'flush runs about four weeks' offsets are NOT published by 426-840, "
            "which prints no strawberry harvest dates -- they are MODELED. A value change is "
            "consumer-facing and rides on its own ruling."),
    },
    'blueberry': {
        'id': 'mid_atlantic_blueberry_vce_credit_repointed_426_840',
        'severity': 'low', 'status': 'accepted', 'blocks_launch': False,
        'filed_in_session': 'pla155_vce_426_331_classification',
        'summary': (
            "The mid_atlantic ride-along vce credit moves from vce_426_331 (a vegetable planting "
            "guide with zero blueberry content; read in full 2026-08-10) to vce_426_840, Small "
            "Fruit in the Home Garden (read 2026-08-10): 'Set them in early spring about three "
            "or four weeks before the average date of the last frost' -- consistent with the "
            "March-to-April window at this belt's Apr 15 / Apr 8 frost anchors. The pathed NCSU "
            "home blueberry guide anchor is untouched."),
    },
    'raspberry': {
        'id': 'mid_atlantic_raspberry_vce_credit_repointed_426_840',
        'severity': 'low', 'status': 'accepted', 'blocks_launch': False,
        'filed_in_session': 'pla155_vce_426_331_classification',
        'summary': (
            "The mid_atlantic ride-along vce credit moves from vce_426_331 (zero caneberry "
            "content; read in full 2026-08-10) to vce_426_840, Small Fruit in the Home Garden "
            "(read 2026-08-10): 'Caneberries should be planted in late fall or early in spring, "
            "about four weeks before the average date of the last frost.' The December opening "
            "of our December-to-March window is the dormant-season reading of that guidance plus "
            "the co-cited NCSU Southeast caneberry guide; 426-840 does not state December "
            "explicitly."),
    },
    'blackberry': {
        'id': 'mid_atlantic_blackberry_vce_credit_repointed_426_840',
        'severity': 'low', 'status': 'accepted', 'blocks_launch': False,
        'filed_in_session': 'pla155_vce_426_331_classification',
        'summary': (
            "The mid_atlantic ride-along vce credit moves from vce_426_331 (zero caneberry "
            "content; read in full 2026-08-10) to vce_426_840, Small Fruit in the Home Garden "
            "(read 2026-08-10): 'Caneberries should be planted in late fall or early in spring, "
            "about four weeks before the average date of the last frost.' The December opening "
            "of our December-to-March window is the dormant-season reading of that guidance plus "
            "the co-cited NCSU Southeast caneberry guide; 426-840 does not state December "
            "explicitly."),
    },
    'elderberry': {
        'id': 'mid_atlantic_elderberry_no_vce_planting_model',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'filed_in_session': 'pla155_vce_426_331_classification',
        'summary': (
            "No VCE document read represents a planting model for elderberry, so the "
            "mid_atlantic region list and both zone cells DROP the vce_426_331 credit and stay "
            "on the institution root (ncsu_ext), mirroring "
            "mid_south_elderberry_no_uaex_planting_model. vce_426_331 read in full 2026-08-10: "
            "0 occurrences of 'elderberry' or 'Sambucus'. vce_426_840 (Small Fruit in the Home "
            "Garden) read 2026-08-10: covers strawberry, blueberry, caneberries and grapes, 0 "
            "elderberry. The March-to-April window remains MODELED (frost-anchored bare-root "
            "spring planting). One role vce_426_331 genuinely played survives on the record: the "
            "region's frost dates come from its zone-scoped Table 1, as plantings_provenance "
            "('Windows frost-reconciled against real VCE/NC State frost dates') already "
            "declares -- the credit removed here is the crop-scoped one the document cannot "
            "carry. Absence is scoped to those two documents read 2026-08-10; no claim about "
            "other VCE publications."),
    },
    'edamame': {
        'id': 'edamame_vce_pub_id_divergence_corrected',
        'severity': 'low', 'status': 'resolved', 'blocks_launch': False,
        'filed_in_session': 'pla155_vce_426_331_classification',
        'summary': (
            "Six crop-level nodes (fertilizer, varieties, germination and pod_fill tips, two "
            "failure diagnostics) cited vce_426_331 -- the vegetable planting guide, which "
            "contains no soybean or edamame content -- while the fertilizer and varieties "
            "anchoring entries already pointed at the SPES-455 URL under that wrong id. The "
            "claims belong to VCE SPES-455, 'Edamame in Virginia II: Producing a High-Quality "
            "Product' (fetched live 2026-08-10, now cached): Bradyrhizobium japonicum "
            "inoculation, the 'seven to 10 days' harvest window (our 'four to ten' brackets it "
            "via the co-cited mu_ext), and low nitrogen need are all stated. Catalog id "
            "vce_spes_455 minted; all six nodes, their anchors, and source_set repointed "
            "2026-08-10. The variety-latitude/photoperiod claim is NOT in SPES-455; it remains "
            "carried by the co-cited mu_ext and cornell_ext entries (not adjudicated here)."),
    },
}


def crop(d, slug):
    return next(c for c in d['crops'] if c['slug'] == slug)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def swap_id(lst, old, new):
    assert lst.count(old) == 1, f'expected exactly one {old} in {lst}'
    return [new if s == old else s for s in lst]


def swap_anchor(node, old, new, url):
    au = node['anchoring_urls']
    assert old in au, f'missing anchor {old}'
    del au[old]
    au[new] = {'url': url, 'verified': VERIFIED}


def apply(d):
    # 1. catalog
    cat = d['source_catalog']
    for entry in (CAT_840, CAT_455):
        assert entry['id'] not in cat, f"{entry['id']} already minted"
        cat[entry['id']] = entry

    # 2. sweet-pea: ncsu_ext joins the sole credit; analog registered as a finding
    sp = crop(d, 'sweet-pea')
    ma = sp['regions']['mid_atlantic']
    assert ma['sources'] == ['vce_426_331']
    ma['sources'] = ['ncsu_ext', 'vce_426_331']
    for z in ('7', '8'):
        cell = ma['resolved_by_zone'][z]
        assert cell['sources'] == ['vce_426_331']
        cell['sources'] = ['ncsu_ext', 'vce_426_331']
        au = cell['anchoring_urls']
        assert set(au) == {'vce_426_331'} and au['vce_426_331']['url'] == URL_331
        au['ncsu_ext'] = {'url': URL_LATHYRUS, 'verified': VERIFIED}

    # 3. strawberry: wrong pub number -> 426-840
    st = crop(d, 'strawberry')
    ma = st['regions']['mid_atlantic']
    assert ma['sources'] == ['vce_426_331', 'ncsu_ext']
    ma['sources'] = ['vce_426_840', 'ncsu_ext']
    cell = ma['resolved_by_zone']['7']
    assert cell['sources'] == ['vce_426_331']
    cell['sources'] = ['vce_426_840']
    swap_anchor(cell, 'vce_426_331', 'vce_426_840', URL_840)
    entry = ma['plantings'][0]
    assert set(entry['anchoring_urls']) == {'vce_426_331'}
    swap_anchor(entry, 'vce_426_331', 'vce_426_840', URL_840)
    for fld, old_note in STRAW_NOTES_OLD.items():
        arm = entry[fld][0]
        assert arm['synthesis_note'] == old_note, f'strawberry {fld} note drifted'
        arm['synthesis_note'] = STRAW_NOTES_NEW[fld]
        assert arm['sources'] == ['vce_426_331']
        arm['sources'] = ['vce_426_840']
        swap_anchor(arm, 'vce_426_331', 'vce_426_840', URL_840)

    # 4. blueberry / raspberry / blackberry: ride-along credit swaps to the small-fruit pub
    for slug in ('blueberry', 'raspberry', 'blackberry'):
        c = crop(d, slug)
        ma = c['regions']['mid_atlantic']
        assert ma['sources'] == ['ncsu_ext', 'vce_426_331'], f'{slug} region list drifted'
        ma['sources'] = ['ncsu_ext', 'vce_426_840']
        container = ma['plantings'][0]
        assert set(container['anchoring_urls']) == {'ncsu_ext', 'vce_426_331'}, f'{slug} container'
        swap_anchor(container, 'vce_426_331', 'vce_426_840', URL_840)
        for z in ('7', '8'):
            cell = ma['resolved_by_zone'][z]
            assert cell['sources'] == ['ncsu_ext', 'vce_426_331'], f'{slug} z{z} drifted'
            cell['sources'] = ['ncsu_ext', 'vce_426_840']
            swap_anchor(cell, 'vce_426_331', 'vce_426_840', URL_840)

    # 5. elderberry: false credit removed, institution root stays
    el = crop(d, 'elderberry')
    ma = el['regions']['mid_atlantic']
    assert ma['sources'] == ['ncsu_ext', 'vce_426_331']
    ma['sources'] = ['ncsu_ext']
    container = ma['plantings'][0]
    assert set(container['anchoring_urls']) == {'ncsu_ext', 'vce_426_331'}
    del container['anchoring_urls']['vce_426_331']
    for z in ('7', '8'):
        cell = ma['resolved_by_zone'][z]
        assert cell['sources'] == ['ncsu_ext', 'vce_426_331']
        cell['sources'] = ['ncsu_ext']
        au = cell['anchoring_urls']
        assert au['vce_426_331']['url'] == URL_331
        del au['vce_426_331']

    # 6. edamame: id/document divergence -> vce_spes_455
    ed = crop(d, 'edamame')
    six = [
        ed['fertilizer'],
        ed['varieties'],
        ed['tips_by_stage']['germination'][1],
        ed['tips_by_stage']['pod_fill'][0],
        ed['failure_diagnostics'][0],
        ed['failure_diagnostics'][2],
    ]
    for node in six:
        node['sources'] = swap_id(node['sources'], 'vce_426_331', 'vce_spes_455')
        swap_anchor(node, 'vce_426_331', 'vce_spes_455', URL_455)
    ss = ed['verification_status']['source_set']
    assert ss == sorted(ss), 'edamame source_set no longer sorted -- re-check convention'
    ss.remove('vce_426_331')
    ss.append('vce_spes_455')
    ss.sort()

    # 7. findings
    for slug, finding in FINDINGS.items():
        of = crop(d, slug)['verification_status']['open_findings']
        assert all(f.get('id') != finding['id'] for f in of), f"{finding['id']} already filed"
        of.append(finding)

    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('path', nargs='?', default=CANONICAL)
    args = ap.parse_args()

    raw = open(args.path, 'rb').read()
    if args.path == CANONICAL and sha(raw) != BASE_SHA:
        print(f'ABORT: canonical is {sha(raw)[:8]}, expected base {BASE_SHA[:8]}')
        sys.exit(1)

    d = apply(json.loads(raw))
    out = json.dumps(d, separators=(',', ':'), ensure_ascii=False)
    if args.dry_run:
        print(f'dry-run OK: {len(out)} bytes, sha {hashlib.sha256(out.encode()).hexdigest()[:8]}')
        return
    with open(args.path, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'promoted: {args.path} -> sha {hashlib.sha256(out.encode()).hexdigest()[:8]}')


if __name__ == '__main__':
    main()
