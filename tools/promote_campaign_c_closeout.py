#!/usr/bin/env python3
"""GUARDED PROMOTE: campaign C closeout -- arid + Texas.

CITATIONS AND FINDINGS ONLY. Not one consumer-facing string, date, offset or suitability moves;
a guard proves it byte-for-byte.
Evidence: docs/2026-08-05-campaign-c-reprice-and-arid-document-read.md.

THE REMAINDER, per tools/campaign_c_reprice.py: after the lemon/lime re-scope campaign C held 30
decisions, of which 6 were honestly open. All four governing documents have now been read, so
NOTHING here is a document hunt -- every node below is adjudicated against a document that was
opened and word-searched or, where the windows are drawn as graphics, read visually.

5 NODES REPOINT. 29 STAY BARE ON PURPOSE. 8 FINDINGS FILED. NO CATALOG ID MINTED.

WHY EACH REPOINT, one at a time:

  carrot      A WRONG-INSTITUTION CITATION, not a bare host needing a document. Source id
              `nmsu_chart` -- New Mexico State -- carries the url `https://desert.tamu.edu/`, a
              bare TEXAS A&M host, on the zone 8 cell and its heat_pause. The catalog already
              holds the right document for that id, carrot's OTHER nodes already cite it
              correctly, and the cell's own prose credits "NMSU Dona Ana Master Gardeners". Only
              the heat_pause is SOLE; the zone cell is corroborated by a live TAMU url. BOTH are
              fixed anyway, because a fabricated attribution left standing in a second field is
              exactly the defect this arc keeps re-finding.
  tomatoes    beefsteak and heirloom both cite `nmsu_donaana_mg` at its bare root, and both
              cells' basis prose NAMES the document: "Dona Ana County Master Gardener Las Cruces
              planting chart". That is the same chart carrot needs. Repointing to it is the CASE 1
              definition verbatim: the real document is nameable from the cell's own prose.
  garlic      the ONE rgv arm with a real document behind it. See below.

THE DONA ANA CHART HAS NO TEXT LAYER. Its planting windows are drawn as graphical bars: a text
extraction returns crop names, month headers and ZERO dates. This is the AZ1005 rotated-grid trap
in a second document, and here it does not yield a wrong grid, it yields an empty one. Read
visually instead. Carrots: mid-January through February, second bar August into early September --
our cell says "Jan - Feb, Aug", first_plant_date Jan 15, last_plant_date Aug 31. Tomatoes: start
around January/February, transplant March into early April; second start June, transplant mid-July
into early August -- our cells say start_indoors Feb 5-19, plant_out Mar 19 - Apr 8, then Jun 3-17
and Jul 15 - Aug 4. Both claims are CORROBORATED by the document their own prose names.

HUNT #13 IS CASE 2 FOR ALL SIX CROPS, AND IT IS MEASURED, NOT ASSUMED. The RGV Homeowner Vegetable
Guide 2022 sat in tools/.doc_cache as an HTTP 403 that both scans had read as ABSENCE. Refetched
and parsed: 5 pages, 11,097 characters, ~25 crop rows, and ZERO occurrences of arugula, fava,
broad bean, garlic, shallot, snow pea or sugar snap. Two further RGV documents were read for the
same six crops. The guide is cited on 468 nodes and by 51 crops inside regions.rgv, which is the
sibling-precedent trap at 51-to-6: the pressure to make the last six match their neighbours is
precisely the pressure to be wrong.

ITS ONLY PEA IS COWPEA. "Cowpeas, Texas Pinkeye, Dolico" is Vigna unguiculata, a warm-season
southern pea and a different genus from Pisum sativum. The Lower Rio Grande Valley table's
"Peas (sweet)" row is Pisum and is cool-season, but it names neither snow nor sugar snap and
carries a single 70-80 day figure that cannot distinguish them. Both facts are recorded on the pea
findings so a later pass does not "find" the Cowpea row and repoint at it.

THE SIX CROPS ALREADY SAID THIS. Every one declares the absence in its own
plantings[0].plant_out[0].synthesis_note_seasoned ("No RGV-specific table row exists for garlic").
The document read confirms every declaration is TRUE. What was missing is that the declaration
lived only in cell prose, where no scan looks -- a third adjudication vocabulary alongside
region-named findings and source-id-named findings. These findings move it into the ledger.

GARLIC IS THE ONE EXCEPTION AND IT IS NOT A BLANKET. Two documents carry a garlic row:

  - the Cameron County Master Gardener fall guide (txmg.org) says plant October through
    mid-November, harvest 90-120 days later. Its planting window agrees with ours. Its HARVEST
    figure does not survive contact with the crop: 90-120 days is not a bulbing-garlic figure.
    That guide also names its own primary source as the LRGV table, which has no garlic row, and
    txmg.org holds no source_catalog id. DECLINED -- swapping a sound derivation for a weaker
    uncatalogued source that contradicts it is the trap kickoff 53 s6 lesson 5 names.
  - TAMU AgriLife Bexar County's garlic page, which garlic's OWN se_gulf and warm_arid regions
    ALREADY cite under this same source id. It states the planting claim directly: garlic "can be
    planted in the late fall", and "if planted in October, may have tops showing above the soil
    and be well rooted by November". Our rgv plant_out is Oct 15 - Nov 15. REPOINTED.

So garlic's PLANT_OUT gets a real document and its HARVEST does not, because the same page says
"The crop will mature in June" while our harvest_start is Apr 13 -- derived arithmetic
(plant_out + 180 days) that runs ahead of every document we hold AND ahead of our own se_gulf rows
(May) for the same mild-winter class. That tension is FILED, not silently retuned: fixing it means
re-deriving a consumer-facing date, which needs its own evidence and is not a citation promote's
work.

NO CATALOG ID IS MINTED. The Bexar url is cited under `tamu_agrilife` because that is what
garlic's own se_gulf and warm_arid regions already do for this exact document. Minting a sub-id
used by one region while two others cite the parent would trade a citation gap for an
inconsistency. A guard requires the url to be already present on this crop under this id.

WHAT IS DELIBERATELY *NOT* DONE. Hunt #14's cantaloupe, honeydew-melon and watermelon are
MODELED-ONLY -- their windows are declared derived but their `uariz_ext` anchor is not
adjudicated. No finding is filed for them here, because AZ1005 is a live lead: it is Arizona's
vegetable planting calendar, it is catalogued as `uariz_ext_az1005`, other crops cite it, and it
plausibly carries cucurbit rows. Filing an absence finding without reading it would be exactly the
document-scoped-absence error this arc has already made once. Left open and recorded.

    $ python3 tools/promote_campaign_c_closeout.py --dry-run
    $ python3 tools/promote_campaign_c_closeout.py --apply
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
BASE_SHA = '5a52a76cabb5ca34dcda7756220fcc34db05f408722e27562bdfd96cd4b0b160'
SESSION = 'campaign_c_closeout_2026_08_05'
VERIFIED = '2026-08-05'

DONAANA_CHART = 'https://donaanamastergardeners.nmsu.edu/documents/foodgardenplantingchart-1.pdf'
BEXAR_GARLIC = ('https://bexar-tx.tamu.edu/homehort/'
                'archives-of-weekly-articles-davids-plant-of-the-week/garlic/')

# The wrong-institution url. Must be extinct after this promote; a guard proves it.
WRONG_URL = 'https://desert.tamu.edu/'

# bare_host_scan's own definition, so the promote and the scan cannot drift on what "root" means.
BARE_URL = re.compile(r'https?://[^/]+/?$')

# (slug, region, path) -> (source id, url BEFORE, url AFTER). The BEFORE is pinned so the promote
# aborts rather than overwriting a value that moved under it.
REPOINTS = {
    ('carrot', 'warm_arid', 'regions.warm_arid.resolved_by_zone.8'):
        ('nmsu_chart', WRONG_URL, DONAANA_CHART),
    ('carrot', 'warm_arid', 'regions.warm_arid.resolved_by_zone.8.heat_pause'):
        ('nmsu_chart', WRONG_URL, DONAANA_CHART),
    ('beefsteak-tomato', 'warm_arid', 'regions.warm_arid.resolved_by_zone.8'):
        ('nmsu_donaana_mg', 'https://donaanamastergardeners.nmsu.edu/', DONAANA_CHART),
    ('heirloom-tomato', 'warm_arid', 'regions.warm_arid.resolved_by_zone.8'):
        ('nmsu_donaana_mg', 'https://donaanamastergardeners.nmsu.edu/', DONAANA_CHART),
    ('garlic', 'rgv', 'regions.rgv.plantings[0].plant_out[0]'):
        ('tamu_agrilife', 'https://agrilifeextension.tamu.edu', BEXAR_GARLIC),
}

# The 29 deliberate CASE 2 nodes, ENUMERATED -- never derived from the hunt roster, which is the
# self-referential vacuity mutation testing caught on 2026-08-03.
RGV_BARE = ('https://agrilifeextension.tamu.edu', 'tamu_agrilife')
HELD = tuple(
    ('garlic', 'rgv', 'regions.rgv.%s' % p) for p in (
        'plantings[0].harvest_start[0]', 'plantings[0].harvest_end[0]',
        'resolved_by_zone.9', 'resolved_by_zone.10')
) + tuple(
    (slug, 'rgv', 'regions.rgv.%s' % p)
    for slug in ('arugula', 'broad-beans-fava', 'shallot', 'snow-peas', 'sugar-snap-peas')
    for p in ('plantings[0].plant_out[0]', 'plantings[0].harvest_start[0]',
              'plantings[0].harvest_end[0]', 'resolved_by_zone.9', 'resolved_by_zone.10')
)

CROPS = ('arugula', 'beefsteak-tomato', 'broad-beans-fava', 'carrot', 'garlic',
         'heirloom-tomato', 'pumpkin', 'shallot', 'snow-peas', 'sugar-snap-peas')

# ENUMERATED BY HAND, never derived from REPOINTS/HELD/FINDINGS. A first cut computed both of
# these from those tables, which made G8 incapable of failing: the expected set and the thing it
# validated came from the same place ([[guard-derived-from-what-it-checks-is-vacuous]]). Caught
# by mutation testing on the first run of the guard suite. G8 now checks the DATA against these
# constants and, separately, these constants against the tables, so either drifting is an abort.
TOUCHED_REGIONS = {
    'arugula': {'rgv'}, 'beefsteak-tomato': {'warm_arid'}, 'broad-beans-fava': {'rgv'},
    'carrot': {'warm_arid'}, 'garlic': {'rgv'}, 'heirloom-tomato': {'warm_arid'},
    'pumpkin': set(), 'shallot': {'rgv'}, 'snow-peas': {'rgv'}, 'sugar-snap-peas': {'rgv'},
}
FINDINGS_PER_CROP = {
    'arugula': 1, 'beefsteak-tomato': 0, 'broad-beans-fava': 1, 'carrot': 1, 'garlic': 1,
    'heirloom-tomato': 0, 'pumpkin': 1, 'shallot': 1, 'snow-peas': 1, 'sugar-snap-peas': 1,
}

_RGV_SCOPE = ('Absence is scoped to the three Rio Grande Valley documents named here, all read '
              'from raw bytes 2026-08-05 and listed in '
              'docs/2026-08-05-campaign-c-reprice-and-arid-document-read.md.')

_GUIDE = ('The RGV Homeowner Vegetable Guide 2022 (Texas A&M AgriLife, Cameron County) is the '
          'document 51 crops cite for this region. It was cached as an HTTP 403 and both scans '
          'had read that as absence; refetched and parsed 2026-08-05 (5 pages, 11,097 '
          'characters). Its roster is about 25 rows: green bean bush and pole, sweet corn, '
          'pepper, potato, tomato, cantaloupe, zucchini, butternut squash, broccoli, cabbage, '
          'collards, cauliflower, kale, kohlrabi, spinach, swiss chard, beets, carrot, turnip, '
          'cowpeas, cilantro, dill, onion bulbing and bunching, leek, sweet potato. ')

_COWPEA = ('TRAP FOR THE NEXT READER: the guide DOES carry a pea row, "Cowpeas, Texas Pinkeye, '
           'Dolico". That is Vigna unguiculata, a warm-season southern pea and a different genus '
           'from Pisum sativum. It cannot source this crop. The Lower Rio Grande Valley table '
           'does carry a cool-season "Peas (sweet)" row (Pisum, 9-1 thru 9-30, 70-80 days), but '
           'it names neither snow nor sugar snap and its single maturity figure cannot '
           'distinguish them. ')


def _absent(crop_label, terms):
    return (_GUIDE + 'Word-searched for %s: ZERO occurrences. The Lower Rio Grande Valley table '
            '(texaslocalproduce.tamu.edu) and the Cameron County Master Gardener fall guide '
            '(txmg.org) were read for the same crop and also carry no row. So no Rio Grande '
            'Valley planting table publishes a window for %s, and this cell\'s own '
            'synthesis_note_seasoned already said so before the documents were read. The windows '
            'stay as authored, modeled on the region\'s cool-season fall and winter calendar. '
            % (terms, crop_label)) + _RGV_SCOPE


FINDINGS = [
    ('arugula', {
        'id': 'rgv_arugula_absent_from_rgv_planting_tables',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': _absent('arugula', '"arugula", "rocket" and "eruca"'),
        'basis': 'RGV Homeowner Vegetable Guide 2022 (Texas A&M AgriLife, Cameron County); '
                 'Vegetable Crops of the Lower Rio Grande Valley (Texas A&M AgriLife); Vegetable '
                 'Gardens for the Rio Grande Valley, Fall Planted or Cool Season Crops (Cameron '
                 'County Master Gardeners). All read from raw bytes and word-searched 2026-08-05.',
        'filed_in_session': SESSION,
    }),
    ('broad-beans-fava', {
        'id': 'rgv_fava_absent_from_rgv_planting_tables',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': _absent('fava beans', '"fava", "broad bean" and "vicia"') + (
            ' The Cameron County guide\'s bean row reads "Beans (green, snap, lima & butter)", '
            'which does not reach Vicia faba. Its page 1 failed the PDF font parse and was '
            'recovered from the raw content stream rather than skipped, so this absence is '
            'measured across the whole document and not inferred from the pages that happened '
            'to be readable.'),
        'basis': 'RGV Homeowner Vegetable Guide 2022; Vegetable Crops of the Lower Rio Grande '
                 'Valley; Vegetable Gardens for the Rio Grande Valley (Cameron County Master '
                 'Gardeners), page 1 recovered from the raw content stream. Read 2026-08-05.',
        'filed_in_session': SESSION,
    }),
    ('shallot', {
        'id': 'rgv_shallot_absent_from_rgv_planting_tables',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': _absent('shallots', '"shallot"') + (
            ' Checked and NOT a substitute: all three documents carry onion rows and the first '
            'two carry leek rows. Onion timing is not shallot timing, and this crop already '
            'carries shallot_calendar_modeled_on_onion recording where its calendar does come '
            'from. Also NOT a substitute: shallot_pink_root_tamu_pdf cites this same institution, '
            'but that is a DISEASE anchor and says nothing about a planting window.'),
        'basis': 'RGV Homeowner Vegetable Guide 2022; Vegetable Crops of the Lower Rio Grande '
                 'Valley; Vegetable Gardens for the Rio Grande Valley (Cameron County Master '
                 'Gardeners). All read from raw bytes and word-searched 2026-08-05.',
        'filed_in_session': SESSION,
    }),
    ('snow-peas', {
        'id': 'rgv_snow_peas_absent_from_rgv_planting_tables',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': _absent('snow peas', '"snow pea" and "snowpea"') + ' ' + _COWPEA,
        'basis': 'RGV Homeowner Vegetable Guide 2022; Vegetable Crops of the Lower Rio Grande '
                 'Valley (the "Peas (sweet)" and "Peas (southern)" rows read directly); Vegetable '
                 'Gardens for the Rio Grande Valley (Cameron County Master Gardeners). Read '
                 '2026-08-05.',
        'filed_in_session': SESSION,
    }),
    ('sugar-snap-peas', {
        'id': 'rgv_sugar_snap_peas_absent_from_rgv_planting_tables',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': _absent('sugar snap peas', '"sugar snap" and "snap pea"') + ' ' + _COWPEA + (
            'This crop already records that TAMU AgriLife\'s own sugar snap factsheet (EHT-015) '
            'is a scanned PDF that could not be converted, so it was never cited; that remains '
            'true and is a separate matter from the RGV tables having no row.'),
        'basis': 'RGV Homeowner Vegetable Guide 2022; Vegetable Crops of the Lower Rio Grande '
                 'Valley (the "Peas (sweet)" and "Peas (southern)" rows read directly); Vegetable '
                 'Gardens for the Rio Grande Valley (Cameron County Master Gardeners). Read '
                 '2026-08-05.',
        'filed_in_session': SESSION,
    }),
    ('garlic', {
        'id': 'rgv_garlic_harvest_start_runs_ahead_of_every_source',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'Garlic is the one hunt 13 crop with a real document behind part of its window, so '
            'its arms split. PLANT_OUT is now anchored to Texas A&M AgriLife Bexar County\'s '
            'garlic page, which garlic\'s own se_gulf and warm_arid regions already cite: garlic '
            '"can be planted in the late fall", and "if planted in October, may have tops showing '
            'above the soil and be well rooted by November". Our Oct 15 to Nov 15 sits inside '
            'that, and the Cameron County Master Gardener fall guide independently says October '
            'through mid-November. HARVEST does NOT follow it. The same page says "The crop will '
            'mature in June", while our harvest_start is Apr 13, which is derived arithmetic '
            '(plant_out plus 180 days) and not a published date. It also runs ahead of our OWN '
            'se_gulf rows, which give May for zones 9 and 10 in the same mild-winter class off '
            'the same document. The Rio Grande Valley is warmer than both Bexar County and the '
            'se_gulf belt, so an earlier harvest is plausible and this is NOT being called an '
            'error. It is unsourced, and it is early in the direction that costs a reader most: '
            'sending them to lift bulbs before the tops go down. NOT retuned here, because '
            'changing it means re-deriving a consumer-facing date and that needs a South Texas '
            'garlic maturity source, which no document read this session supplies. DECLINED, and '
            'recorded so it is not re-proposed: the Cameron County guide\'s "harvest 90 to 120 '
            'days later" is not a bulbing-garlic figure, that guide names the Lower Rio Grande '
            'Valley table as its own primary source and that table has no garlic row, and '
            'txmg.org holds no source_catalog id. ' + _RGV_SCOPE),
        'basis': 'Texas A&M AgriLife Extension, Bexar County, "Garlic" (David Rodriguez, County '
                 'Extension Agent-Horticulture); Vegetable Gardens for the Rio Grande Valley '
                 '(Cameron County Master Gardeners); RGV Homeowner Vegetable Guide 2022; '
                 'Vegetable Crops of the Lower Rio Grande Valley. All read 2026-08-05. Compared '
                 'against this crop\'s own se_gulf and warm_arid resolved cells.',
        'filed_in_session': SESSION,
    }),
    ('carrot', {
        'id': 'warm_arid_carrot_chart_url_was_a_texas_host_under_a_new_mexico_id',
        'severity': 'medium', 'status': 'resolved', 'blocks_launch': False,
        'summary': (
            'The warm_arid zone 8 cell and its heat_pause cited source id nmsu_chart, New Mexico '
            'State, at the url https://desert.tamu.edu/ , a bare TEXAS A&M host. The catalog has '
            'always held the right document for that id, the Dona Ana County Master Gardener Las '
            'Cruces vegetable planting chart, and this crop\'s OTHER nodes already cited it '
            'correctly, so this was a transcription defect and not a second document. Both nodes '
            'are repointed. The claim itself is CORROBORATED by the chart: its carrot row runs '
            'mid-January through February with a second bar from August into early September, '
            'and this cell says "Jan - Feb, Aug" with first_plant_date Jan 15 and last_plant_date '
            'Aug 31. TRAP FOR THE NEXT READER: that chart\'s windows are drawn as GRAPHICAL BARS '
            'and its text layer contains crop names, month headers and no dates at all, so a text '
            'extraction returns an empty grid rather than a wrong one. It must be read visually. '
            'CLASS, not an isolated row: nmsu_chart carries three different urls across 15 nodes '
            'and 5 crops, and the third is lowwaterplants.nmsu.edu on lavender, an ornamental '
            'page standing in for a food garden planting chart. That one is outside this '
            'campaign and is left open. No existing check can see this shape: bare_host_scan '
            'never consults source_catalog, and every one of these urls returns HTTP 200.'),
        'basis': 'Dona Ana County Master Gardeners, Las Cruces Vegetable Planting Chart, read '
                 'visually 2026-08-05; source_catalog entry for nmsu_chart; roster-wide '
                 'comparison of node anchoring_urls against catalog urls, 29,390 entries, run '
                 '2026-08-05.',
        'filed_in_session': SESSION,
    }),
    ('pumpkin', {
        'id': 'pumpkin_pilot_regional_source_anchors_general',
        'severity': 'low', 'status': 'accepted', 'blocks_launch': False,
        'summary': (
            'Several regional planting-window cells anchor to institution-level extension portals '
            '(nmsu, tamu) rather than a pumpkin-specific regional planting-date page read this '
            'session. The core agronomy and the representative dates are verified against UGA '
            'C1206, UMN and UF/IFAS, as recorded in pumpkin_pilot_regional_calendars_modeled; the '
            'regional date portals back the MODELED windows. Filed 2026-08-05 to match the '
            'finding its five sibling cucurbits and peppers already carry: acorn-squash, '
            'butternut-squash, spaghetti-squash, bell-pepper and eggplant each hold a '
            'regional_source_anchors_general record naming these same two portals, and pumpkin '
            'was the only crop in that set without one, which is why the citation arc read it as '
            'unadjudicated when the identical citation shape on its siblings read as declared. '
            'This records the existing state; it changes no citation and no window.'),
        'basis': 'Measured against the crop\'s own warm_arid nodes 2026-08-05: '
                 'plantings[0] and resolved_by_zone.8 each cite nmsu_ext at '
                 'https://pubs.nmsu.edu and tamu_agrilife at https://agrilifeextension.tamu.edu, '
                 'both institution roots. Sibling findings compared directly.',
        'filed_in_session': SESSION,
    }),
]

EM_DASH = chr(8212)
INSTITUTION = re.compile(r'AgriLife|Texas A&M|NMSU|New Mexico|Dona Ana|Cameron County|UGA|UMN'
                         r'|UF/IFAS|Master Gardener')


def resolve(crop, region, path):
    """Resolve a bare_host_scan path to the dict carrying `sources`/`anchoring_urls`."""
    node = crop['regions'][region]
    tail = re.sub(r'^regions\.[a-z0-9_]+\.', '', path)
    for part in tail.split('.'):
        m = re.match(r'^([a-z_]+)\[(\d+)\]$', part)
        node = node[m.group(1)][int(m.group(2))] if m else node[part]
    return node


def cites_bare(node, sid, url):
    """Match bare_host_scan's OWN definition of SOLE, not a re-derivation of it."""
    anchors = node.get('anchoring_urls') or {}
    if set(anchors) != {sid} or anchors[sid].get('url') != url:
        return False
    return not {s for s in (node.get('sources') or []) if s != sid}


def reg_host(u):
    h = (urlsplit(u).hostname or '').lower()
    h = h[4:] if h.startswith('www.') else h
    p = h.split('.')
    return '.'.join(p[-2:]) if len(p) >= 2 else h


def cited_urls(node, out):
    if isinstance(node, dict):
        for sid, m in (node.get('anchoring_urls') or {}).items():
            if isinstance(m, dict) and m.get('url'):
                out.append((sid, m['url']))
        for k, v in node.items():
            if k != 'anchoring_urls':
                cited_urls(v, out)
    elif isinstance(node, list):
        for v in node:
            cited_urls(v, out)
    return out


def prose_of(crop):
    """Every string anywhere under regions, keyed by path. The consumer-copy tripwire."""
    out = {}

    def walk(n, path):
        if isinstance(n, dict):
            for k, v in n.items():
                if k == 'anchoring_urls':
                    continue
                if isinstance(v, str):
                    out['%s.%s' % (path, k)] = v
                else:
                    walk(v, '%s.%s' % (path, k))
        elif isinstance(n, list):
            for i, v in enumerate(n):
                walk(v, '%s[%d]' % (path, i))

    walk(crop.get('regions') or {}, '')
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

    # PREFLIGHT 1 -- the premise: every repointed node still carries the url this promote expects.
    for (slug, region, path), (sid, old, _new) in sorted(REPOINTS.items()):
        node = resolve(crops[slug], region, path)
        got = ((node.get('anchoring_urls') or {}).get(sid) or {}).get('url')
        if got != old:
            print('ABORT: %s %s expected %s at %r, found %r' % (slug, path, sid, old, got))
            return 2
    print('preflight: all %d repoint targets carry their pinned pre-state url' % len(REPOINTS))

    # PREFLIGHT 2 -- the held nodes are still SOLE on the RGV bare host.
    for slug, region, path in HELD:
        if not cites_bare(resolve(crops[slug], region, path), RGV_BARE[1], RGV_BARE[0]):
            print('ABORT: %s %s no longer cites the bare host SOLE -- premise changed'
                  % (slug, path))
            return 2
    print('preflight: all %d held nodes still cite the bare host SOLE' % len(HELD))

    # PREFLIGHT 3 -- coverage against the SCAN, not against this file. Every SOLE bare node the
    # six rgv crops own in rgv must be accounted for by REPOINTS or HELD, so a node cannot be
    # silently forgotten.
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    from bare_host_scan import scan  # noqa: E402
    rgv_crops = {s for s, r, _p in HELD} | {'garlic'}
    scoped = {(slug, 'rgv', path) for _sid, slug, path, sole, _u in scan(data)
              if sole and path.startswith('regions.rgv.') and slug in rgv_crops}
    accounted = {(s, r, p) for s, r, p in HELD} | {
        (s, r, p) for (s, r, p) in REPOINTS if r == 'rgv'}
    if scoped != accounted:
        print('ABORT: scan and promote disagree on rgv scope.\n  scan-only: %s\n  promote-only: %s'
              % (sorted(scoped - accounted), sorted(accounted - scoped)))
        return 2
    print('preflight: promote rgv scope == bare_host_scan rgv scope (%d nodes)' % len(scoped))

    # PREFLIGHT 4 -- nothing already filed.
    for slug, f in FINDINGS:
        if any(x.get('id') == f['id'] for x
               in ((crops[slug].get('verification_status') or {}).get('open_findings') or [])):
            print('ABORT: finding %s already filed on %s' % (f['id'], slug))
            return 2
    print('preflight: %d findings unfiled' % len(FINDINGS))

    # ---- edits -----------------------------------------------------------------------------
    applied = []
    for (slug, region, path), (sid, _old, new) in sorted(REPOINTS.items()):
        node = resolve(crops[slug], region, path)
        node['anchoring_urls'][sid]['url'] = new
        node['anchoring_urls'][sid]['verified'] = VERIFIED
        applied.append('%s %s  %s -> %s' % (slug, path.replace('regions.', ''), sid, new[:58]))

    for slug, finding in FINDINGS:
        vs = crops[slug].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(copy.deepcopy(finding))
        applied.append('%s finding %s' % (slug, finding['id']))

    # ---- guards ----------------------------------------------------------------------------
    # G1 every repoint is T1 and stays within its catalog entry's own institution.
    for (slug, region, path), (sid, _old, new) in REPOINTS.items():
        entry = data['source_catalog'].get(sid)
        if not entry:
            print('ABORT: %s %s repoints at uncatalogued id %s' % (slug, path, sid))
            return 2
        if entry.get('tier') != 'T1':
            print('ABORT: %s %s repoints at non-T1 id %s' % (slug, path, sid))
            return 2
        if reg_host(new) != reg_host(entry['url']):
            print('ABORT: %s %s repoints %s at %s, a different institution from its catalog url %s'
                  % (slug, path, sid, reg_host(new), reg_host(entry['url'])))
            return 2
    print('verified: %d repoints are T1 and match their catalog institution' % len(REPOINTS))

    # G2 -- LOAD-BEARING, and the reason no catalog id is minted. Every repoint url must be
    # vouched for by something already in the repo. Three rules, and each of the three repoints
    # needs a DIFFERENT one, which is what stops this from being a rubber stamp:
    #
    #   (a) the url IS the catalog url for that id            -- carrot / nmsu_chart
    #   (b) the catalog url is a bare ROOT and the url is a document on THAT SAME HOST, which is
    #       the repo's normal shape (nmsu_ext's root is pubs.nmsu.edu and its nodes cite
    #       pubs.nmsu.edu/_circulars/...)                     -- tomatoes / nmsu_donaana_mg
    #   (c) THIS CROP already cites that exact url under that exact id somewhere else
    #                                                          -- garlic / tamu_agrilife (Bexar)
    #
    # (b) deliberately requires the same HOST, not the same registrable domain. That is what
    # keeps the Bexar page out of rule (b): bexar-tx.tamu.edu is not agrilifeextension.tamu.edu,
    # so it has to earn its citation through (c) by being a document this crop already trusts.
    host = lambda u: (urlsplit(u).hostname or '').lower().removeprefix('www.')  # noqa: E731
    rules = {}
    for (slug, region, path), (sid, _old, new) in sorted(REPOINTS.items()):
        entry = data['source_catalog'].get(sid) or {}
        cu = entry.get('url') or ''
        if new == cu:
            rules[(slug, path)] = 'a: is the catalog url'
        elif BARE_URL.fullmatch(cu) and host(new) == host(cu):
            rules[(slug, path)] = 'b: document on the catalog root host %s' % host(cu)
        elif any(s == sid and u == new
                 for s, u in cited_urls(before_crop(before, slug), [])):
            rules[(slug, path)] = 'c: this crop already cites it under %s' % sid
        else:
            print('ABORT: %s %s cites %s at %s, a url neither the catalog nor this crop vouches '
                  'for' % (slug, path, sid, new))
            return 2
    print('verified: every repoint url is vouched for, by rule:')
    for (slug, path), why in sorted(rules.items()):
        print('   %-18s %-46s %s' % (slug, path.replace('regions.', ''), why))
    if len({w[0] for w in rules.values()}) != 3:
        print('ABORT: expected all three vouching rules to be exercised, saw %s'
              % sorted({w[0] for w in rules.values()}))
        return 2

    # G3 -- the wrong-institution url must be EXTINCT.
    for sid, url in cited_urls(data, []):
        if url == WRONG_URL:
            print('ABORT: the wrong-institution url survives, cited as %s' % sid)
            return 2
    print('verified: %s is cited nowhere in the dataset' % WRONG_URL)

    # G4 -- the 29 held nodes must STILL be bare.
    for slug, region, path in HELD:
        if not cites_bare(resolve(crops[slug], region, path), RGV_BARE[1], RGV_BARE[0]):
            print('ABORT: %s %s was repointed but is a deliberate CASE 2 node' % (slug, path))
            return 2
    print('verified: %d CASE 2 nodes still bare, as intended' % len(HELD))

    # G5 -- NOT ONE CONSUMER STRING MOVES, across every region of every touched crop.
    bmap = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    for slug in CROPS:
        if prose_of(bmap[slug]) != prose_of(aa[slug]):
            print('ABORT: %s consumer copy changed' % slug)
            return 2
    print('verified: every consumer-facing string byte-identical across all %d crops' % len(CROPS))

    # G6 findings are dated, sourced, em-dash free.
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

    # G8 per crop, only the intended regions and keys moved -- checked against the HAND-WRITTEN
    # constants, not against the edit tables. Both directions are asserted so the constants
    # cannot quietly stop describing the promote.
    if sorted(TOUCHED_REGIONS) != sorted(CROPS) or sorted(FINDINGS_PER_CROP) != sorted(CROPS):
        print('ABORT: the hand-written G8 constants do not cover exactly CROPS')
        return 2
    from_tables = {}
    for slug, region, _p in list(REPOINTS) + list(HELD):
        from_tables.setdefault(slug, set()).add(region)
    for slug in CROPS:
        if TOUCHED_REGIONS[slug] != from_tables.get(slug, set()):
            print('ABORT: TOUCHED_REGIONS[%s] = %s but the edit tables say %s'
                  % (slug, sorted(TOUCHED_REGIONS[slug]), sorted(from_tables.get(slug, set()))))
            return 2
        if FINDINGS_PER_CROP[slug] != sum(1 for s, _f in FINDINGS if s == slug):
            print('ABORT: FINDINGS_PER_CROP[%s] = %d but FINDINGS holds %d'
                  % (slug, FINDINGS_PER_CROP[slug], sum(1 for s, _f in FINDINGS if s == slug)))
            return 2
    for slug in CROPS:
        b, a = bmap[slug], aa[slug]
        for reg in b.get('regions', {}):
            if b['regions'][reg] != a['regions'][reg] and reg not in TOUCHED_REGIONS[slug]:
                print('ABORT: %s region %s changed and is not in this campaign' % (slug, reg))
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
    print('verified: only the campaign regions and verification_status moved, per crop')

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


def before_crop(before, slug):
    for c in before['crops']:
        if c['slug'] == slug:
            return c
    raise KeyError(slug)


if __name__ == '__main__':
    sys.exit(main())
