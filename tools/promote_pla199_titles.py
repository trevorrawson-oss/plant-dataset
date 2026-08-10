#!/usr/bin/env python3
"""PLA-199: source_catalog titles -- the field, the backfill, nothing else. Base 060b91b8.

WHAT THIS DOES (rulings D1+D2 of docs/2026-08-10-source-catalog-title-decision.md, as
OVERRIDDEN/confirmed by the PLA-199 issue -- D1 is (a), a new optional `title` field, NOT the
spec's recommended name-parenthetical convention):

  1. Adds an optional `title` field to document-scoped source_catalog entries. The value is the
     document's OWN title, read from the cached body in tools/.doc_cache (sha1(url).txt), never
     inferred from the id, the URL, or the pub number -- inferring a title from an identifier is
     exactly the defect PLA-199 exists to fix. 101 of the 153 document-scoped ids are filled.
  2. Migrates the two PLA-155 precedent entries (vce_426_840, vce_spes_455) OFF the
     "Pub ID (Title)" name convention: the parenthetical moves to `title`, `name` keeps the id
     restatement. No other `name` changes (scope: "no renaming of existing ids").
  3. Records the other 52 document-scoped ids UNFILLED, with reasons: 50 have no cached
     document, unr_sp2007's cache is an extraction with no usable text layer, and
     lsu_agcenter_3363's cached text layer carries body prose but NO title line (its cover is an
     image; titling it would be URL/pub-number inference). These 52 are the mint-time gate's
     frozen exemption list (tools/source_catalog_title_gate.py, A54).

WHAT IT DELIBERATELY DOES NOT DO: no title on any institution-root (bare-url) id -- a bare
anchor honestly labeled beats a decorated one (D2). No subject/genre tagging (D4 deferred:
titles buy authoring-time visibility, costs #1+#2; they do NOT make genre detection mechanical).
Nothing outside source_catalog moves -- not one crop byte, not one finding, no consumer string.

TRANSCRIPTION NOTES (all read 2026-08-10 from the cached bodies):
  - All-caps PDF covers are transcribed in title case (ucce_imperial_artichoke,
    uc_costs_strawberry_sjv, nws_vef, uhawaii_ctahr_b91); layout dashes become commas.
  - vce_426_331 keeps the document's own U+2019 apostrophe ("Virginia's").
  - Four cached bodies DIVERGE from what their catalog name/id claims; the title records what
    the document actually is, which is the feature, not a bug (see the close-out): wsu_em051e
    serves EM057E; ufifas_ae588 serves a carrot nitrogen guideline; uariz_ext_az1005 serves the
    Maricopa vegetable calendar (name says onions); uc_costs_strawberry_sjv serves the 2005
    study (name says 2004).

Usage: python3 tools/promote_pla199_titles.py [--dry-run] [canonical.json]
"""
import argparse
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '060b91b807f7988d3d22ebbae77e90d285ee5f7dfe6a18a11c4de37cf6debbbd'

BARE = re.compile(r'https?://[^/]+/?\Z')

# The two PLA-155 precedent entries: parenthetical OUT of name, INTO title (D1).
NAME_MIGRATIONS = {
    'vce_426_840': 'Virginia Cooperative Extension Publication 426-840',
    'vce_spes_455': 'Virginia Cooperative Extension Publication SPES-455',
}

# id -> the document's own title, read from tools/.doc_cache. HAND-TRANSCRIBED, not extracted
# by tooling -- a first-line heuristic is the mechanical proxy this whole arc bans.
TITLES = {
    'clemson_hgic_1149': 'How to Grow Zinnias: The Best Varieties & Care Tips',
    'clemson_hgic_1322_sweet_potato': 'Sweetpotato',
    'clemson_peach_diseases': 'Peach Diseases',
    'cornell_ext': 'Cornell Cooperative Extension',
    'csu_ext_lavender_07245': 'Growing Lavender in Colorado',
    'iastate_ext_colecrops': 'Cole Crops',
    'illinois_ext': 'Asparagus',
    'ksu_pawpaw': 'Pawpaw',
    'lsu_agcenter': 'Lawn & Garden',
    'lsu_agcenter_3634': 'Vegetable Gardening Tips: Artichokes',
    'msstate_ext': 'Lawn and Garden',
    'ncsu_ext_handbook_tree_fruit': '15. Tree Fruit and Nuts',
    'ncsu_ext_lavandula_angustifolia':
        'Lavandula angustifolia (Common Lavender, English Lavender, Lavender, '
        'Narrow-Leaved Lavender)',
    'ncsu_ext_toolbox_punica_granatum': 'Punica granatum (Pomegranate)',
    'ncsu_ext_toolbox_vicia_faba':
        'Vicia faba (Bell Bean, Broad Bean, English Bean, Faba Bean, Fava Bean, Field Bean, '
        'Horse Bean, Pidgeon Bean, Tick Bean, Windsor Bean)',
    'ndsu_ext': 'Extension',
    'nmsu_chart': 'Las Cruces Vegetable Planting Chart',
    'nmsu_ext_cr457b':
        'Growing Zones and Planting Information for Home Vegetable Gardens in New Mexico',
    'nmsu_ext_h324': 'Home Garden Strawberry Production in New Mexico',
    'nws_vef': 'Climate of Las Vegas, Nevada',
    'osu_ext_prune_lavender': 'When is the best time to prune lavender?',
    'osu_oregon_veg': 'Artichoke, Globe',
    'tamu_agrilife_fall_veg': 'Fall Vegetable Gardening Guide',
    'tamu_eht065': 'Easy Gardening: Artichoke',
    'ua_az1005': 'Vegetable Planting Calendar for Maricopa County',
    'ua_az1615': 'Planting and Harvesting Calendar for Gardeners in Yuma County',
    'uada_ext_berries': 'Arkansas Berries - Home Garden',
    'uada_ext_chill': 'Chilling Hour Reports',
    'uada_ext_fall_veg': 'Fall Planting Dates',
    'uada_ext_fruit_trees': 'Arkansas Fruit Tree Production Tips',
    'uada_ext_fsa6104': 'Blueberry Production in the Home Garden',
    'uada_ext_fsa6105': 'Blackberry Production in the Home Garden',
    'uada_ext_fsa6107': 'Raspberry Production in the Home Garden',
    'uada_ext_spring_veg': 'Arkansas spring and summer vegetable planting dates',
    'uariz_ext_az1005': 'Vegetable Planting Calendar for Maricopa County',
    'uariz_ext_az1615': 'Planting and Harvesting Calendar for Gardeners in Yuma County',
    'uariz_ext_az1667': 'Growing Strawberries in Home Gardens',
    'uariz_ext_az2061': 'Growing Herbs In Tucson',
    'uc_anr_7221': 'Artichoke Production in California',
    'uc_costs_strawberry_sjv': '2005 Sample Costs to Produce Strawberries, San Joaquin Valley',
    'uc_mg_santa_clara_citrus': 'Growing Great Citrus',
    'uc_mg_t132': 'Time of planting',
    'ucanr_ext_mg_timeplanting': 'Time of planting',
    'ucanr_mg_monterey_santacruz': 'Growing Strawberries in the Home Garden',
    'ucanr_pub7234': 'Asparagus Production in California',
    'ucanr_san_diego_mg': 'UC Master Gardeners of San Diego County',
    'ucce_imperial_artichoke':
        'Sample Cost to Establish and Produce Artichokes, Imperial County, 2000',
    'ucce_imperial_lowdesert': 'Asparagus in the Low Desert',
    'uf_ifas_central_cal': 'Central Florida Gardening Calendar',
    'uf_ifas_gs': 'Onions and Shallots',
    'uf_ifas_hs1153': 'Lemon Growing in the Florida Home Landscape',
    'uf_ifas_hs1289': 'Production Guidelines for Globe Artichoke in Florida',
    'uf_ifas_hs132': 'Citrus Culture in the Home Landscape',
    'uf_ifas_hs403': 'Growing Strawberries in the Florida Home Garden',
    'uf_ifas_north_cal': 'North Florida Gardening Calendar',
    'uf_ifas_south_cal': 'South Florida Gardening Calendar',
    'uf_ifas_vh021': 'Florida Vegetable Gardening Guide',
    'uf_ifas_zinnia': 'Zinnia',
    'ufifas_ae588':
        'Carrot (Daucus carota) Production in the Sandy Soils of North Florida: '
        'Nitrogen Fertilization Guidelines',
    'ufifas_ext_broccoli': 'Broccoli',
    'ufifas_ext_vh021': 'Florida Vegetable Gardening Guide',
    'uga_c1206_homegrown_pumpkins': 'Homegrown Pumpkins',
    'uga_c1258_fall': 'Fall Vegetable Gardening',
    'uga_c963_vegetable_gardening': 'Vegetable Gardening in Georgia',
    'uga_caes_collards': 'Cultivating Collards: a Step-by-step Guide',
    'uga_calendar': 'Vegetable Garden Calendar',
    'uga_ext_c943_calendar': 'Vegetable Garden Calendar',
    'uga_ext_c963_chart': 'Vegetable Planting Chart',
    'uhawaii_ctahr': 'Information Central',
    'uhawaii_ctahr_b91': 'Home Gardening in Hawaii',
    'uhawaii_ctahr_hawaii_county': 'Plants',
    'uhawaii_ctahr_hgv1': 'Carrots',
    'umaine_2075': 'Bulletin #2075, Growing Globe Artichokes (Cynara scolymus L.) in Maine',
    'umaine_highmoor': '2023 Research Report: Artichokes for the Northeast',
    'umass_nevmg': 'Globe Artichoke',
    'umd_ext_broccoli': 'Growing Broccoli in a Home Garden',
    'umn_ext_broccoli': 'Growing broccoli in home gardens',
    'unlv_mg_svn': 'Vegetable Planting Guide for Southern Nevada',
    'unr_ext_fs1305':
        'Fruit, Flower and Seed Vegetable Varieties for the Moapa and Virgin Valleys',
    'unr_fs0261': 'Home Vegetable Production in Southern Nevada',
    'unr_sp0115': 'Becoming a Desert Gardener',
    'unr_sp9911': 'Growing Tomatoes in Southern Nevada',
    'usu_ext': 'Yard & Garden',
    'usu_ext_artichoke': 'How to Grow Artichoke in Your Garden',
    'usu_ext_english_lavender': 'How to Grow English Lavender in Your Garden',
    'usu_ext_fall_veg': 'Fall Gardening in the St. George Area',
    'usu_ext_garlic': 'How to Grow Garlic in Your Garden',
    'usu_ext_peaches': 'How to Grow Peaches in Your Garden',
    'usu_ext_raspberry': 'Raspberry Management for Utah',
    'usu_ext_tomato': 'How to Grow Tomatoes in Your Garden',
    'usu_ext_veg_dates': 'Suggested Vegetable Planting Dates for Utah',
    'usu_ext_wash_frost': 'Elevations for Washington County',
    'usu_ext_wash_fruits': 'Fruits',
    'usu_washco_dates': 'Planting Dates (Spring)',
    'vce_426_331':
        'Virginia’s Home Garden Vegetable Planting Guide: Recommended Planting Dates '
        'and Amounts to Plant',
    'vce_426_840': 'Small Fruit in the Home Garden',
    'vce_438_108': 'Specialty Crop Profile: Globe Artichoke',
    'vce_spes_455': 'Edamame in Virginia II. Producing a High-Quality Product',
    'wsu_em051e': 'Home Vegetable Gardening in Washington',
    'wsu_em057e': 'Home Vegetable Gardening in Washington',
    'wsu_ext_lavender_prcr': 'Lavender Research',
}

# id -> why it stays unfilled. These 52 become source_catalog_title_gate.LEGACY_UNFILLED.
UNFILLED = {
    'almanac': 'uncached', 'aspca': 'uncached', 'auburn_aces': 'uncached',
    'cornell_ext_apple_disease': 'uncached', 'cornell_ext_apple_fireblight': 'uncached',
    'cornell_ext_apple_scab': 'uncached', 'cornell_ext_strawberry_redstele': 'uncached',
    'johnny_seeds': 'uncached', 'mo_ext_g6201': 'uncached', 'mo_ext_g6461': 'uncached',
    'msu_bozeman': 'uncached', 'msu_ext': 'uncached', 'msu_radical_roots': 'uncached',
    'ncsu_ext_bulb_onions': 'uncached', 'ncsu_ext_strawberry_anthracnose': 'uncached',
    'nws_lzk': 'uncached', 'ohio_state_ext': 'uncached', 'psu_microgreens': 'uncached',
    'purdue_ext_bp132w': 'uncached', 'purdue_ext_foodlink_lavender': 'uncached',
    'rutgers_fs044': 'uncached', 'tamu_agrilife_aggie_spring': 'uncached',
    'uada_ext_fsa6001': 'uncached', 'uada_ext_fsa6014': 'uncached',
    'uada_ext_fsa6103': 'uncached', 'uc_anr_8100': 'uncached',
    'uc_ipm_citrus_timings': 'uncached', 'uc_mg_marin_citrus': 'uncached',
    'uc_mg_sacramento_gn127': 'uncached', 'ucanr_ext_8256': 'uncached',
    'ucanr_ext_woolly_apple_aphid': 'uncached', 'ucanr_slo_mg': 'uncached',
    'ucce_kern_kc9382': 'uncached', 'ucce_placer_nevada_31_018c': 'uncached',
    'ucce_riverside_citrus_qa': 'uncached', 'ucd_postharvest': 'uncached',
    'uf_ifas_hs764': 'uncached', 'uf_ifas_leon': 'uncached', 'uf_ifas_nwdistrict': 'uncached',
    'uga_b577': 'uncached', 'uga_c1014_sweet_potato': 'uncached', 'uga_c1232': 'uncached',
    'uiuc_ext': 'uncached', 'umaine_ext_2184': 'uncached', 'umass_ext': 'uncached',
    'umn_ext': 'uncached', 'umn_ext_apple_scab': 'uncached',
    'umn_ext_edible_flowers': 'uncached', 'uscrn': 'uncached', 'weatherkit': 'uncached',
    'unr_sp2007': 'cache unreadable: extraction has no usable text layer',
    'lsu_agcenter_3363': 'cached text layer has NO title line (image cover); '
                         'titling it would be URL/pub-number inference',
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def with_title(entry, title):
    """Rebuild the entry dict with `title` inserted directly after `name` (key order is
    meaningful in the compact canonical; append-at-end would scatter the field)."""
    out = {}
    for k, v in entry.items():
        out[k] = v
        if k == 'name':
            out['title'] = title
    assert 'title' in out, 'entry had no name key'
    return out


def apply(d):
    cat = d['source_catalog']

    doc_scoped = {c for c, e in cat.items() if not BARE.match(e['url'])}
    # Coverage, both directions, against the HAND-WRITTEN lists (a computed expectation
    # would be vacuous): every document-scoped id is either titled or recorded unfilled.
    assert set(TITLES) | set(UNFILLED) == doc_scoped, (
        'fill+unfilled lists do not cover the document-scoped set: '
        f'missing={sorted(doc_scoped - set(TITLES) - set(UNFILLED))} '
        f'stray={sorted((set(TITLES) | set(UNFILLED)) - doc_scoped)}')
    assert not set(TITLES) & set(UNFILLED), 'an id is both filled and unfilled'
    assert len(TITLES) == 101 and len(UNFILLED) == 52 and len(doc_scoped) == 153

    for cid in cat:
        assert 'title' not in cat[cid], f'{cid} already carries a title'

    for cid, new_name in NAME_MIGRATIONS.items():
        old = cat[cid]['name']
        assert old.startswith(new_name + ' ('), f'{cid} name unexpectedly {old!r}'
        cat[cid]['name'] = new_name

    for cid, title in TITLES.items():
        assert title.strip() == title and title, f'{cid} title not a clean string'
        cat[cid] = with_title(cat[cid], title)

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
