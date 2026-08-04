#!/usr/bin/env python3
"""GUARDED PROMOTE: campaign B closeout -- fig, strawberry, apple, elderberry, broad-beans-fava.

CITATIONS AND FINDINGS ONLY. Not one consumer-facing string, date, offset or suitability moves;
a guard proves it byte-for-byte.
Evidence: docs/2026-08-04-campaign-b-closeout-hunt.md.

THE REMAINDER, per tools/campaign_b_reprice.py: 2 decisions needing document work (fig mid_south,
strawberry mid_south) plus 3 region-anchor-only decisions (apple mid_south, elderberry mid_south,
broad-beans-fava mid_atlantic). 18 SOLE bare nodes. 4 repoint, 14 stay bare ON PURPOSE.

WHY SO FEW REPOINTS -- the answers differ per crop and are adjudicated one at a time:

  fig         UAEX publishes NO fig harvest date. Arkansas's own FRUIT HARVEST CALENDAR
              (FCS812A) lists 12 fruits and fig is NOT among them. Three other UAEX documents
              give only cultivar ripening ORDER ("Celeste ... ripens usually before Brown
              Turkey"; "Brown Turkey ... ripens a few weeks after Celeste") and crop structure
              (the breba crop "rarely" persists in Arkansas). Same shape as hunt 1's peach
              "days before Elberta" ladder: a relative order with no anchor date.
  strawberry  the z8 plasticulture plant_out is the block's last live claim arm, and the one
              UAEX datum CONTRADICTS ITS TAIL. See below.
  apple       CLEAN: its plantings[] container is the only bare node left, and its own
              plant_out arm and BOTH zone cells already cite uada_ext_fruit_trees. Repointing
              the container to the document its own children carry is bookkeeping, not a claim.
  elderberry  UAEX's home-garden berry guide does not mention elderberry AT ALL (0 hits). Its
              Plant of the Week article covers the right taxon (Sambucus canadensis) but gives
              seasons, not dates, and NO planting date -- and its "midsummer" flowering diverges
              from our May/June bloom. No UAEX document represents a planting model here.
  fava        the HEAT_PAUSE claim is directly supported by two documents and repoints; the zone
              cells' planting model is not, because neither mid_atlantic vegetable calendar
              lists the crop.

THE STRAWBERRY FIND. Our z8 window is "Sep 15 - Oct 5". UAEX's own three-year fall-planting-date
study reports the last two weeks of September as what was considered "on time", and the first
week of October as the LATE treatment, which "reduced strawberry yield 15-35 percent depending on
variety and test year". So the tail of our window sits inside the treatment UAEX measured as
costly. NOT changed here: it is consumer-facing, and it is coupled to the still-open
strawberry_mid_south_plasticulture_home_garden_tension -- FSA6103 says this annual system "is not
recommended for home garden strawberry production at this time", so trimming the window using
COMMERCIAL research would deepen a commitment to a system the home-garden fact sheet disrecommends
while that question is unresolved. Recorded, coupled, and left for a ruling.

THE SECOND HOST-VS-AUTHOR TRAP IN TWO DAYS. The only dated plasticulture planting calendar on the
UAEX server ("Third week of September - set your Sweet Charlies first") is An Introductory Guide to
Strawberry Plasticulture by E. Barclay Poling, NC STATE -- hosted by UAEX, authored elsewhere, and
calendared for North Carolina. Citing it as uada_ext would credit UAEX with NC State's
recommendations. A guard bans it.

WHAT WAS CHECKED AND IS *NOT* A DEFECT. elderberry's mid_south planting arms are month-name
strings (["March","April"]) rather than offset objects, so they carry no per-arm citation. That is
NOT a defect and NOT unique to elderberry: it is a supported variant used by 8 crops across all 16
regions (420 arms -- blackberry, blueberry, elderberry, raspberry, lavender, oregano, rosemary,
sage, thyme). For those crops ALL citation lives on the container, which is exactly why they price
as region-anchor-only. Measured before filing, because "these arms are uncited" would have been a
fabricated finding.

FOOTPRINT: 4 nodes repoint, 14 stay bare, 5 findings filed, 1 catalog id minted.

    $ python3 tools/promote_campaign_b_closeout.py --dry-run
    $ python3 tools/promote_campaign_b_closeout.py --apply
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
BASE_SHA = '370806b54252628b49502d3b85476504be24e461bb479445f056d02514f529b7'
SESSION = 'campaign_b_closeout_2026_08_04'
VERIFIED = '2026-08-04'

FRUIT_TREES = ('uada_ext_fruit_trees',
               'https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx')
FSA6103 = ('uada_ext_fsa6103', 'https://www.uaex.uada.edu/publications/pdf/FSA-6103.pdf')
TOOLBOX_FAVA = ('ncsu_ext_toolbox_vicia_faba', 'https://plants.ces.ncsu.edu/plants/vicia-faba/')

# path -> (crop, region, new id, new url). Paths are the bare_host_scan spelling, so the promote
# and the scan cannot drift apart on how a node is addressed.
REPOINTS = {
    ('apple', 'mid_south', 'regions.mid_south.plantings[0]'): FRUIT_TREES,
    ('strawberry', 'mid_south', 'regions.mid_south.plantings[0]'): FSA6103,
    ('broad-beans-fava', 'mid_atlantic',
     'regions.mid_atlantic.resolved_by_zone.7.heat_pause'): TOOLBOX_FAVA,
    ('broad-beans-fava', 'mid_atlantic',
     'regions.mid_atlantic.resolved_by_zone.8.heat_pause'): TOOLBOX_FAVA,
}

# The 14 deliberate CASE 2 nodes, ENUMERATED -- never derived from REPOINTS, which is the
# self-referential vacuity caught by mutation testing on 2026-08-03.
HELD = (
    ('fig', 'mid_south', 'regions.mid_south.plantings[0].bloom[0]'),
    ('fig', 'mid_south', 'regions.mid_south.plantings[0].harvest_start[0]'),
    ('fig', 'mid_south', 'regions.mid_south.plantings[0].harvest_end[0]'),
    ('strawberry', 'mid_south', 'regions.mid_south.plantings[0].bloom[0]'),
    ('strawberry', 'mid_south', 'regions.mid_south.plantings[1]'),
    ('strawberry', 'mid_south', 'regions.mid_south.plantings[1].plant_out[0]'),
    ('strawberry', 'mid_south', 'regions.mid_south.plantings[1].bloom[0]'),
    ('strawberry', 'mid_south', 'regions.mid_south.resolved_by_zone.7'),
    ('strawberry', 'mid_south', 'regions.mid_south.resolved_by_zone.8'),
    ('elderberry', 'mid_south', 'regions.mid_south.plantings[0]'),
    ('elderberry', 'mid_south', 'regions.mid_south.resolved_by_zone.7'),
    ('elderberry', 'mid_south', 'regions.mid_south.resolved_by_zone.8'),
    ('broad-beans-fava', 'mid_atlantic', 'regions.mid_atlantic.resolved_by_zone.7'),
    ('broad-beans-fava', 'mid_atlantic', 'regions.mid_atlantic.resolved_by_zone.8'),
)

CROPS = ('apple', 'broad-beans-fava', 'elderberry', 'fig', 'strawberry')

# The scope is a set of (crop, region) DECISIONS, not crop x region. fig also owns a SOLE bare
# node in mid_atlantic, and that is a DIFFERENT decision -- already CLOSED-BY-RULING under
# mid_atlantic_bloom_offset_undocumented. Scoping by crop would have swept it in. Caught by the
# coverage guard on the first dry run, which is the whole reason that guard compares against the
# scan instead of against this file.
DECISIONS = (('apple', 'mid_south'), ('broad-beans-fava', 'mid_atlantic'),
             ('elderberry', 'mid_south'), ('fig', 'mid_south'), ('strawberry', 'mid_south'))

# Hosted by UAEX, authored by NC State, calendared for North Carolina. Must never be credited to
# uada_ext, and must never appear on a mid_south strawberry node.
BANNED_URL_SUBSTR = 'Guide%20to%20Strawberry%20Plasticulture'

CATALOG_ENTRY = {
    'id': TOOLBOX_FAVA[0],
    'name': 'NC State Extension Gardener Plant Toolbox -- Vicia faba',
    'publisher': 'NC State Extension',
    'url': TOOLBOX_FAVA[1],
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': '2026-08',
    'tier': 'T1',
    'citable_for': (
        'NC State Extension Gardener Plant Toolbox entry for Vicia faba (fava / broad / faba '
        'bean). HEAT LIMIT, the load-bearing claim: "This cool season crop can be grown in most '
        'climates, however, temperatures in the 60\'s are ideal. In locations where the daytime '
        'temperatures exceed the mid 70\'s may result in poor yeild unless planted at a time when '
        'temperatures are milder" (sic, the source misspells "yield"). Backs the mid_atlantic '
        'heat_pause on both zones: a HEAT exclusion, not a frost gap. Also "Four to five months '
        'are needed between sowing seed and harvesting", "NC Region: Coastal, Mountains, '
        'Piedmont" (so both mid_atlantic zones are in range), "Flower Bloom Time: Spring, Summer" '
        'and "Display/Harvest Time: Fall, Summer" -- SEASONS ONLY, no dates, which is why the '
        'zone cells\' planting model does NOT cite this. Corroborated on the temperature claim by '
        'VCE SPES-590, "Faba Bean: A Multipurpose Specialty Crop for the Mid-Atlantic USA" '
        '(2024-03-26): "temperatures ranging from 60-65 degF are the best for its growth, faba '
        'bean can grow at temperatures ranging from 45-75 degF". Parent portal entry: ncsu_ext.'),
    '_admission_provenance': (
        'Minted 2026-08-04 (campaign B closeout). Page sub-id under a trusted T1 parent (tier '
        'inherited). Read from raw bytes 2026-08-04; taxon confirmed as Vicia faba, matching the '
        'crop, per the match-the-taxon-not-the-common-name rule.'),
}

_SCOPE = ('Absence is scoped to the documents named here, all read from raw bytes 2026-08-04 and '
          'listed in docs/2026-08-04-campaign-b-closeout-hunt.md.')

FINDINGS = [
    ('fig', {
        'id': 'mid_south_fig_harvest_undocumented',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': (
            'UAEX publishes no fig harvest date. Arkansas\'s own fruit harvest calendar (FCS812A, '
            '"Arkansas Local Produce Fruit & Vegetable Harvest Calendars") lists twelve fruits -- '
            'apples, blackberries, blueberries, cantaloupe, grapes, muscadines, nectarines, '
            'peaches, plums, raspberries, strawberries, watermelon -- and FIG IS NOT AMONG THEM. '
            'Three further UAEX documents (the Yard & Garden fig reference desk, the White County '
            'article, and the summer fruits page) give only cultivar ripening ORDER and crop '
            'structure: "Celeste ... ripens usually before Brown Turkey", "Brown Turkey (also '
            'called Texas Everbearing) ripens a few weeks after Celeste ... bears for a '
            'relatively long period of time", and the breba crop "rarely" persists in Arkansas so '
            'the current-season crop "is predominantly what we harvest". That is a relative '
            'ladder with no anchor date, the same shape hunt 1 recorded for peach ("days before '
            'Elberta"), which is why fig was not in hunt 1\'s stated exclusion list but reaches '
            'the same verdict on its own evidence. Our Jun 25 - Aug 10 (zone 7) / Jun 15 - Jul 30 '
            '(zone 8) window is modeled from bloom_start and is not contradicted by anything '
            'read. TRAP FOR THE NEXT READER: FCS812A\'s month columns are GRAPHICAL BARS with no '
            'text layer, so a text extraction returns crop names and no months. It cannot support '
            'a month claim for any crop, including the twelve it does list. ' + _SCOPE),
        'basis': 'UAEX FCS812A; uaex.uada.edu fig reference desk; UAEX White County "Fig Varieties '
                 'that Grow Well in AR"; UAEX summer fruits page. Read from raw bytes 2026-08-04.',
        'filed_in_session': SESSION,
    }),

    ('strawberry', {
        'id': 'mid_south_strawberry_z8_plant_out_late_tail',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'The zone 8 plasticulture plant_out window is "Sep 15 - Oct 5", and UAEX\'s own '
            'three-year fall-planting-date study places its TAIL inside the treatment it measured '
            'as costly. Per the University of Arkansas System Division of Agriculture report of '
            'that study, the plots planted on what was considered "on time" were "the last two '
            'weeks of September", and the late treatment was "a week later in the first week of '
            'October"; extension specialist Amanda McWhirt reports the "late-planted treatment '
            'reduced strawberry yield 15-35 percent depending on variety and test year", and that '
            'a row cover "will never make up for the loss of daylight that occurred due to the '
            'late planting, even in as short of a one-week delay". Sep 15-30 matches "on time". '
            'Oct 1-5 does not. A follow-on study begun in 2021 also indicates "planting too early '
            'could reduce yield potential", so the early bound is not settled either. NOT changed '
            'here, for two reasons. It is consumer-facing. And it is COUPLED to '
            'strawberry_mid_south_plasticulture_home_garden_tension, which is still open: FSA6103 '
            'says this annual system "is not recommended for home garden strawberry production at '
            'this time", so trimming the window on the strength of COMMERCIAL plasticulture '
            'research would deepen a commitment to a system the home-garden fact sheet '
            'disrecommends, while that question is unresolved. The two should be ruled together. '
            + _SCOPE),
        'basis': 'UAEX news release "Fall planting strawberries? When is too late, and too early, '
                 'to plant in Arkansas" (2022-05-24, John Lovett, quoting Amanda McWhirt), read '
                 'from raw bytes 2026-08-04; cross-read against uada_ext_fsa6103.',
        'filed_in_session': SESSION,
    }),
    ('strawberry', {
        'id': 'mid_south_strawberry_plasticulture_guide_is_ncsu_not_uaex',
        'severity': 'low', 'status': 'accepted', 'blocks_launch': False,
        'summary': (
            'The only document on the UAEX server carrying a dated plasticulture planting '
            'calendar is "An Introductory Guide to Strawberry Plasticulture" by E. Barclay '
            'Poling, Professor and Extension Specialist, Department of Horticultural Science, NC '
            'STATE. It is hosted by UAEX and authored elsewhere, and its calendar is North '
            'Carolina\'s ("Third week of September - set your Sweet Charlies first (we like to '
            'set these 5 days ahead of Chandler)"; "by the time growers in the southeastern '
            'Coastal Plain plant in mid-October"). Citing it as uada_ext would credit the '
            'University of Arkansas with NC State\'s recommendations, which is the '
            'template-inheritance attribution defect this arc has now hit twice in two days. It '
            'is also a COMMERCIAL guide (methyl bromide fumigation, 15,000-17,500 plants per '
            'acre, deer fencing) and not home-garden guidance. Recorded so a later pass does not '
            '"find" it and repoint at it; the promote bans its URL structurally. ' + _SCOPE),
        'basis': 'uaex.uada.edu/farm-ranch/crops-commercial-horticulture/docs/Guide to Strawberry '
                 'Plasticulture.pdf, read from raw bytes 2026-08-04; authorship and calendar '
                 'confirmed in the document header and section text.',
        'filed_in_session': SESSION,
    }),

    ('elderberry', {
        'id': 'mid_south_elderberry_no_uaex_planting_model',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'summary': (
            'No UAEX document represents a planting model for elderberry, so the three container '
            'nodes stay on the institution root. UAEX\'s home-garden berry guide, which is the '
            'document backing every other mid_south berry, DOES NOT MENTION ELDERBERRY AT ALL (0 '
            'occurrences of "elderberry" or "Sambucus"). UAEX\'s Plant of the Week article does '
            'cover the crop and the RIGHT TAXON (Sambucus canadensis, matching ours), but it '
            'publishes no planting date and only seasons for the rest: "Small white 5-petaled '
            'flowers are produced in midsummer", "Purple-black pea sized berries are produced in '
            'late summer in profusion, especially if two clones are planted to ensure '
            'pollination". Our arms say bloom May and June, which is EARLIER than "midsummer", '
            'and plant_out March and April, which the document does not speak to at all. Needs a '
            'ruling: either accept the months as modeled and say so, or revisit the bloom window '
            'against the one UAEX statement that exists. NOTE, checked and NOT a defect: this '
            'crop\'s planting arms are month-name strings rather than offset objects, so they '
            'carry no per-arm citation by design. That is a supported variant shared by 8 crops '
            'across all 16 regions (420 arms), not an elderberry fault, and it is why all of this '
            'crop\'s citation must live on the container. ' + _SCOPE),
        'basis': 'UAEX Yard & Garden berries page (word-searched, 0 hits); UAEX Plant of the Week '
                 '"Elderberry", Latin: Sambucus canadensis (Gerald Klingaman). Both read from raw '
                 'bytes 2026-08-04. Arm-shape census run over the full canonical the same day.',
        'filed_in_session': SESSION,
    }),

    ('broad-beans-fava', {
        'id': 'mid_atlantic_fava_absent_from_vegetable_calendars',
        'severity': 'low', 'status': 'accepted_modeled', 'blocks_launch': False,
        'summary': (
            'The heat_pause on both zones now cites the NC State Plant Toolbox entry for Vicia '
            'faba, which states the claim directly: "temperatures in the 60\'s are ideal. In '
            'locations where the daytime temperatures exceed the mid 70\'s may result in poor '
            'yeild" (sic). VCE SPES-590, "Faba Bean: A Multipurpose Specialty Crop for the '
            'Mid-Atlantic USA", corroborates it for this exact geography: "temperatures ranging '
            'from 60-65 degF are the best for its growth, faba bean can grow at temperatures '
            'ranging from 45-75 degF". The ZONE CELLS are a different question and stay bare: '
            'NEITHER mid_atlantic vegetable calendar lists this crop. NC State\'s central North '
            'Carolina planting calendar has rows for beans lima/bush, lima/pole, snap/bush and '
            'snap/pole and no fava; VCE 426-331 has beans lima, pole and snap and no fava. Zero '
            'occurrences of "fava", "broad bean" or "faba" in either. So the region publishes no '
            'planting date for the crop, and SPES-590 does not supply one -- it is a '
            'cropping-systems research publication about faba bean as a winter cover and seed '
            'crop, reporting variety trials, not a home-garden planting calendar. ' + _SCOPE),
        'basis': 'NC State Plant Toolbox, Vicia faba; VCE SPES-590 (2024-03-26); NC State central '
                 'North Carolina planting calendar; VCE 426-331. All read from raw bytes and '
                 'word-searched 2026-08-04.',
        'filed_in_session': SESSION,
    }),
]

EM_DASH = chr(8212)
INSTITUTION = re.compile(r'UAEX|University of Arkansas|NC State|Virginia|VCE|Arkansas')


def resolve(crop, region, path):
    """Resolve a bare_host_scan path to the dict carrying `sources`/`anchoring_urls`."""
    node = crop['regions'][region]
    tail = re.sub(r'^regions\.[a-z0-9_]+\.', '', path)
    for part in tail.split('.'):
        m = re.match(r'^([a-z_]+)\[(\d+)\]$', part)
        if m:
            node = node[m.group(1)][int(m.group(2))]
        else:
            node = node[part]
    return node


def cites_bare(node, sid, url):
    """Match bare_host_scan's OWN definition of SOLE, not a re-derivation of it.

    `sources` is OPTIONAL on these nodes: elderberry's mid_south container carries
    `anchoring_urls` and no `sources` key at all, and the scan still calls it SOLE because it
    unions the two and asks whether anything non-bare survives. A stricter check here would have
    aborted on a node the scan legitimately reports, which is how a promote and its own scan
    drift apart.
    """
    anchors = node.get('anchoring_urls') or {}
    if set(anchors) != {sid} or anchors[sid].get('url') != url:
        return False
    extra = {s for s in (node.get('sources') or []) if s != sid}
    return not extra


BARE = {'mid_south': ('uada_ext', 'https://www.uaex.uada.edu'),
        'mid_atlantic': ('ncsu_ext', 'https://content.ces.ncsu.edu')}


def prose_of(crop, region):
    out = {}
    for z, cell in crop['regions'][region]['resolved_by_zone'].items():
        for k, v in cell.items():
            if isinstance(v, str):
                out['%s.%s' % (z, k)] = v
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, str):
                        out['%s.%s.%s' % (z, k, k2)] = v2
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

    all_nodes = sorted(set(REPOINTS) | set(HELD))

    # PREFLIGHT 1 -- the premise: every node in scope is still SOLE on its region's bare host.
    for slug, region, path in all_nodes:
        sid, url = BARE[region]
        if not cites_bare(resolve(crops[slug], region, path), sid, url):
            print('ABORT: %s %s no longer cites the bare host SOLE -- premise changed'
                  % (slug, path))
            return 2
    print('preflight: all %d nodes still cite their bare host SOLE' % len(all_nodes))

    # PREFLIGHT 2 -- coverage. Every SOLE bare node these five crops own in these regions must be
    # accounted for by REPOINTS or HELD, so a node cannot be silently forgotten. This is what
    # makes the promote's footprint claim checkable against the scan rather than against itself.
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    from bare_host_scan import scan  # noqa: E402
    scoped = {(slug, path.split('.')[1], path)
              for _sid, slug, path, sole, _u in scan(data)
              if sole and path.startswith('regions.')
              and (slug, path.split('.')[1]) in DECISIONS}
    if scoped != set(all_nodes):
        print('ABORT: scan and promote disagree on scope.\n  scan-only: %s\n  promote-only: %s'
              % (sorted(scoped - set(all_nodes)), sorted(set(all_nodes) - scoped)))
        return 2
    print('preflight: promote scope == bare_host_scan scope (%d nodes)' % len(scoped))

    # PREFLIGHT 3 -- nothing already filed, nothing already catalogued.
    for slug, f in FINDINGS:
        if any(x.get('id') == f['id'] for x
               in ((crops[slug].get('verification_status') or {}).get('open_findings') or [])):
            print('ABORT: finding %s already filed on %s' % (f['id'], slug))
            return 2
    if CATALOG_ENTRY['id'] in data['source_catalog']:
        print('ABORT: catalog id %s already exists' % CATALOG_ENTRY['id'])
        return 2
    print('preflight: %d findings unfiled, catalog id unminted' % len(FINDINGS))

    # ---- edits -----------------------------------------------------------------------------
    applied = []
    data['source_catalog'][CATALOG_ENTRY['id']] = copy.deepcopy(CATALOG_ENTRY)
    applied.append('catalog + %s' % CATALOG_ENTRY['id'])

    for (slug, region, path), (sid, url) in sorted(REPOINTS.items()):
        node = resolve(crops[slug], region, path)
        # Preserve the node's existing SHAPE: only rewrite `sources` where the node already has
        # one. strawberry's mid_south plantings[0] carries anchoring_urls and no sources key, and
        # inventing one would be a shape change riding on a citation promote.
        if 'sources' in node:
            node['sources'] = [sid]
        node['anchoring_urls'] = {sid: {'url': url, 'verified': VERIFIED}}
        applied.append('%s %s -> %s' % (slug, path.replace('regions.', ''), sid))

    for slug, finding in FINDINGS:
        vs = crops[slug].setdefault('verification_status', {})
        vs.setdefault('open_findings', []).append(copy.deepcopy(finding))
        applied.append('%s finding %s' % (slug, finding['id']))

    # ---- guards ----------------------------------------------------------------------------
    # G1 every repoint agrees with the catalog and is T1.
    for (slug, region, path), (sid, url) in REPOINTS.items():
        entry = data['source_catalog'].get(sid)
        if not entry:
            print('ABORT: %s %s repoints at uncatalogued id %s' % (slug, path, sid))
            return 2
        if entry.get('url') != url:
            print('ABORT: %s %s url disagrees with catalog id %s (%r)'
                  % (slug, path, sid, entry.get('url')))
            return 2
        if entry.get('tier') != 'T1':
            print('ABORT: %s %s repoints at non-T1 id %s' % (slug, path, sid))
            return 2
    print('verified: %d repoints agree with the catalog and are all T1' % len(REPOINTS))

    # G2 -- LOAD-BEARING. The 14 held nodes must STILL be bare.
    for slug, region, path in HELD:
        sid, url = BARE[region]
        if not cites_bare(resolve(crops[slug], region, path), sid, url):
            print('ABORT: %s %s was repointed but is a deliberate CASE 2 node' % (slug, path))
            return 2
    print('verified: %d CASE 2 nodes still bare, as intended' % len(HELD))

    # G3 -- the Poling guide is NC State content on a UAEX host. It may not be CITED. It may of
    # course be NAMED in a finding, which is the whole point of the record it gets, so this walks
    # anchoring_urls and sources rather than the raw blob. The blob version fired on the finding's
    # own basis line.
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

    # Narrowed to the UAEX-HOSTED PDF specifically. A first cut also banned any URL containing
    # "strawberry-plasticulture" and immediately flagged
    # content.ces.ncsu.edu/strawberry-plasticulture-production-guide-for-north-carolina, which is
    # NC State's OWN guide cited as ncsu_ext on mid_atlantic crops and is entirely correct. The
    # defect is a UAEX host lending its name to NC State authorship, not the word.
    for sid, url in cited_urls(data, []):
        if BANNED_URL_SUBSTR in url:
            print('ABORT: the NC State plasticulture guide is cited as %s (%s)' % (sid, url))
            return 2
    print('verified: the UAEX-hosted NC State plasticulture guide is cited nowhere')

    # G4 -- NOT ONE CONSUMER STRING MOVES.
    bmap = {c['slug']: c for c in before['crops']}
    for slug in CROPS:
        for region in ('mid_south', 'mid_atlantic'):
            if region not in bmap[slug].get('regions', {}):
                continue
            if prose_of(bmap[slug], region) != prose_of(crops[slug], region):
                print('ABORT: %s %s consumer copy changed' % (slug, region))
                return 2
    print('verified: every consumer-facing string byte-identical across all 5 crops')

    # G5 findings are dated, sourced, em-dash free.
    for slug, f in FINDINGS:
        for field in ('summary', 'basis'):
            if EM_DASH in f[field]:
                print('ABORT: em dash in %s.%s' % (f['id'], field))
                return 2
        if not INSTITUTION.search(f['summary']):
            print('ABORT: finding %s names no institution' % f['id'])
            return 2
        if '2026-08-04' not in f['basis']:
            print('ABORT: finding %s basis carries no read date' % f['id'])
            return 2
    print('verified: %d findings dated, sourced, and free of em dashes' % len(FINDINGS))

    # G6 exact footprint.
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
    print('verified: exactly 5 crops changed, nothing else at top level')

    # G7 per crop, only the intended regions and keys moved.
    touched_regions = {}
    for slug, region, _p in all_nodes:
        touched_regions.setdefault(slug, set()).add(region)
    for slug in CROPS:
        b, a = bmap[slug], aa[slug]
        for reg in b.get('regions', {}):
            if b['regions'][reg] != a['regions'][reg] and reg not in touched_regions.get(slug, ()):
                print('ABORT: %s region %s changed and is not in this hunt' % (slug, reg))
                return 2
        moved = {k for k in b if k != 'regions' and b[k] != a.get(k)}
        if moved - {'verification_status'}:
            print('ABORT: %s crop-level keys changed: %s' % (slug, sorted(moved)))
            return 2
        nb = len((b.get('verification_status') or {}).get('open_findings') or [])
        na = len((a.get('verification_status') or {}).get('open_findings') or [])
        want = sum(1 for s, _f in FINDINGS if s == slug)
        if na - nb != want:
            print('ABORT: %s gained %d findings, expected %d' % (slug, na - nb, want))
            return 2
    print('verified: only the hunted regions and verification_status moved, per crop')

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
