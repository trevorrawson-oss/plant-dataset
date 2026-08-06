#!/usr/bin/env python3
"""PLA-114 §7: the six, as scoped. Base bce8bcc7.

WHAT THIS DOES
  1. mints seven UC catalog ids, and admits Lazaneo under the EXISTING `ucanr_san_diego_mg`
  2. adds `ucce_placer_nevada_31_018c` to lemon's source_set (Trevor's 28-vs-29 ruling)
  3. amends F5 by APPEND -- a seventh document, and 26F is TWO institutions, not one
  4. repoints the `plant_out` arms of the four CA hunts onto the UC documents that publish the rule
  5. files three findings: two modeled declarations with their absences enumerated, and the
     held-back harvest finding as USER-FACING CONTENT

WHAT IT DELIBERATELY DOES NOT DO -- and this is the substance, not an omission.

`harvest_start` / `harvest_end` on `low_desert_az`, `ca_desert` and `ca_south_coast` stay BARE.
No repoint, no scoped-divergence note. The arms compute from `bloom_start + 240/+300`, and bloom
is itself MODELED, so the displayed value is produced by the model and not by any document.
Repointing would credit a document for a value it did not produce (F1 again). Converting the
documents' ABSOLUTE calendar windows into bloom-anchored offsets would be worse: it pushes a
sourced window through an unsourced anchor and then cites the document for the composite. Same
defect, more arithmetic. The finding below records that no citation is admissible for these arms
as currently structured, and flags the user-facing consequence.

`bloom` stays MODELED in every region including the Central Valley. UC IPM's chart is cited only
as the main bloom of Central Valley CITRUS GENERALLY, explicitly not as lemon's bloom: it is a
commercial Pest Management Guideline dominated by navels and mandarins, and four independent
sources describe lemon as ever-bearing.

Usage: python3 tools/promote_pla114_six.py [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'bce8bcc72aeebb42269b2d96310b427d9502a3670241ca7621e91810588f16cd'
SESSION = 'pla114_six_2026_08_06'

MAUK = 'https://ucanr.edu/sites/default/files/2013-12/178097.pdf'
MARIN = 'https://ucanr.edu/site/uc-marin-master-gardeners/document/citrus'
KERN = 'https://ucanr.edu/sites/default/files/2011-05/98580.pdf'
IPM_TIMINGS = ('https://ipm.ucanr.edu/agriculture/citrus/'
               'timings-for-key-cultural-and-management-practices/')
PLACER = 'https://ucanr.edu/sites/default/files/2020-10/63813.pdf'
SACRAMENTO = 'https://ucanr.edu/sites/default/files/2013-07/72239.pdf'
SANTA_CLARA = ('https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/'
               'growing-great-citrus')
LAZANEO = ('https://www.mastergardenersd.org/wp-content/uploads/2016/12/'
           'citrus-for-the-home-garden.pdf')
AZ1001 = 'https://extension.arizona.edu/sites/extension.arizona.edu/files/pubs/az1001.pdf'

_UC = 'university_extension'
_MG = 'extension_master_gardener_program'


def _entry(cid, name, publisher, url, cls, citable):
    return {'id': cid, 'name': name, 'publisher': publisher, 'url': url, 'source_class': cls,
            'trust_tier': 'high', 'tier': 'T1', 'accessed': '2026-08', 'citable_for': citable}


NEW_IDS = {
    'ucce_riverside_citrus_qa': _entry(
        'ucce_riverside_citrus_qa',
        'Mauk, P. & Shea, T., Questions and Answers to Citrus Management, 3rd ed., '
        'UC Cooperative Extension Riverside County',
        'UC Cooperative Extension, Riverside County', MAUK, _UC,
        'Home-citrus Q&A for Riverside County (Moreno Valley, Indio, Blythe). Cited for the '
        'PLANTING RULE: "The best planting time is after frost danger (after February 15 in the '
        'Riverside area) and before the onset of hot weather. Although fall planting can be '
        'successful it is generally better to wait until spring." Also publishes lemon bearing '
        'habit by district -- Eureka "bears year round on the coast, fall and winter in the low '
        'desert valleys, and winter to spring production in the inland Riverside areas" -- and '
        'carries SEPARATE irrigation tables for the Riverside area and the Desert area, which is '
        'independent evidence that UC treats inland and desert as distinct regimes. '
        'DO NOT count its 29F/30-minute frost figure (Q18) as a second institution: it is '
        'near-verbatim UC ANR 8100 and is the SAME LINEAGE.'),
    'uc_mg_marin_citrus': _entry(
        'uc_mg_marin_citrus', 'UC Marin Master Gardeners, "Citrus" grow sheet',
        'UC Master Gardeners of Marin County (UC ANR)', MARIN, _MG,
        'North-coast California home-citrus grow sheet, page updated 2026-06-19. Cited for the '
        'PLANTING RULE ("Citrus can be planted any time of the year in frost-free zones", '
        'otherwise spring) and for the ever-bearing habit statement "Lemons and limes are '
        'considered ever-bearing but produce most in winter and spring". It publishes NO bloom '
        'window and NO lemon-specific harvest dates.'),
    'ucce_kern_kc9382': _entry(
        'ucce_kern_kc9382',
        'Kallsen, C., Growing Backyard Citrus in Kern County, KC9382 (rev. July 2007)',
        'UC Cooperative Extension, Kern County', KERN, _UC,
        'San Joaquin Valley home-citrus guide -- the region-exact source for California interior '
        'valleys. Cited for the PLANTING RULE: "Generally, citrus should be planted after the '
        'danger of frost is passed, usually in late March through April." It is a cultural and '
        'troubleshooting guide and publishes NO harvest window for lemon.'),
    'uc_ipm_citrus_timings': _entry(
        'uc_ipm_citrus_timings',
        'UC IPM, "Timings for Key Cultural and Management Practices", Citrus (UC ANR Pub 3441)',
        'UC Statewide Integrated Pest Management Program (UC ANR)', IPM_TIMINGS, _UC,
        'Commercial Pest Management Guideline timing chart, explicitly scoped to California\'s '
        'Central Valley. Its month shading is a VISUAL BAR GRID: text extraction returns the row '
        'labels with empty cells, so it must be read from the HTML class attributes. Re-derived '
        'from raw HTML 2026-08-06: Prebloom Jan-Feb; BLOOM PERIOD March plus the FIRST HALF of '
        'April (the Bloom row carries a shaded cell spanning both half-months of March and '
        'exactly ONE shaded half-cell in April); Petal fall mid-April through May; Fruit '
        'development Jun-Sep; Fall Oct through mid-Dec. '
        'CITABLE ONLY FOR THE MAIN BLOOM OF CENTRAL VALLEY CITRUS GENERALLY, NEVER FOR LEMON\'S '
        'BLOOM: the guideline covers commercial citrus dominated by navels and mandarins, and '
        'lemon is repeatedly documented as ever-bearing. Its Harvest row is likewise GENERIC '
        'CITRUS (Jan-May plus mid-Nov-Dec) and must not be read as lemon\'s harvest.'),
    'ucce_placer_nevada_31_018c': _entry(
        'ucce_placer_nevada_31_018c',
        'Fake, C., Growing Citrus in the Sierra Nevada Foothills, UCCE Placer/Nevada 31-018C '
        '(2020)',
        'UC Cooperative Extension, Placer and Nevada Counties', PLACER, _UC,
        'County-advisor citrus guide for the Sierra Nevada foothills. Publishes a cold-hardiness '
        'LADDER naming cultivars: "kumquat (18F) is hardier than Satsuma mandarin (20F) > Meyer '
        'lemon (22F) > oranges: navel, blood, etc. (24F) > grapefruit (26F) > true lemons '
        '(Eureka, Lisbon) (28F) > lime (30F)". The document self-describes these as "guidelines '
        'to assist in selecting appropriate species" -- a SELECTION GUIDELINE, not a '
        'duration-qualified damage-onset threshold, which is why lemon stays at 29F on UC ANR '
        '8100 rather than moving to 28. NOT INDEPENDENT of the Meyer 22F figure already cited '
        '(Fake & Norton, 134971.pdf): same author, same ladder, ONE lineage. Also publishes a '
        'California planting window (spring after frost danger, March-April; fall not '
        'recommended) whose geographic scope is the FOOTHILLS, not the Interior Valleys.'),
    'uc_mg_sacramento_gn127': _entry(
        'uc_mg_sacramento_gn127',
        'UC Master Gardeners of Sacramento County, Growing Citrus in Sacramento, GN 127 '
        '(rev. Oct 2012, ed. Chuck Ingels)',
        'UC Master Gardeners of Sacramento County (UC ANR)', SACRAMENTO, _MG,
        'Central Valley home-citrus guide. Publishes a cold-damage ladder for leaf and branch '
        'damage: "Limes 29F, Lemons and grapefruit 26F, Meyer lemon 22F, Oranges and mandarins '
        '21F, Kumquat 19F", with its own caveat that "these are not hard and fast figures". This '
        'is the SECOND institution publishing 26F alongside LSU AgCenter, and it is '
        'category-level in the same way (lemon and grapefruit share one number). Its harvest '
        'statement is GENUS-LEVEL ONLY ("most citrus varieties ripen from late fall through '
        'winter") and its recommended home-garden varieties do NOT include Eureka or Lisbon, so '
        'it is not citable for a Central Valley true-lemon harvest window.'),
    'uc_mg_santa_clara_citrus': _entry(
        'uc_mg_santa_clara_citrus',
        'UC Master Gardeners of Santa Clara County, "Growing Great Citrus"',
        'UC Master Gardeners of Santa Clara County (UC ANR)', SANTA_CLARA, _MG,
        'Central-coast home-citrus guide. Cited as one of three UC counties that PLACE the spring '
        'bloom without publishing it, by timing work around it ("February or March before '
        'bloom"). Also states Eureka carries "some fruit year-round", one of the four independent '
        'descriptions of lemon as ever-bearing.'),
}

SAN_DIEGO_APPEND = (
    ' ADMITTED 2026-08-06 for a SECOND document on the Association domain: Lazaneo, V., "Citrus '
    'for the Home Garden" (Aug 2014, UCCE San Diego), '
    'https://www.mastergardenersd.org/wp-content/uploads/2016/12/citrus-for-the-home-garden.pdf '
    '-- UCCE-authored, so it clears the read-not-cited caveat above at cite-time. CITABLE FOR the '
    'San Diego planting rule (spring after danger of frost has passed; early planting especially '
    'desirable inland) and the San Diego harvest window (Eureka and Lisbon "Almost all year"), and '
    'for its independently-worded 29F figure ("Young trees can be injured or killed when winter '
    'temperatures drop below 29F... Fruit can also be damaged when temperatures drop below 29F"), '
    'which genuinely corroborates UC ANR 8100 rather than restating it. '
    'DO NOT CITE IT FOR THE COLD-HARDINESS RANKING: its ladder puts grapefruit MORE TENDER than '
    'true lemon, which is the reverse of UC ANR 8100 Table 1, UCCE 31-018C, LSU AgCenter, UA '
    'AZ1001, UC MG Sacramento GN 127 and Mauk & Shea Q18 -- an outlier 6 to 1. '
    'The SLO county page links this document as mastergardenerssandiego.org, which does not '
    'resolve; mastergardenersd.org is the live host.')

# (region, source id to ADD to the plant_out arm, url)
PLANT_OUT = [
    ('ca_interior', 'ucce_kern_kc9382', KERN),
    ('ca_north_coast', 'uc_mg_marin_citrus', MARIN),
    ('ca_south_coast', 'ucanr_san_diego_mg', LAZANEO),
    ('ca_south_coast', 'ucce_riverside_citrus_qa', MAUK),
    ('ca_desert', 'ucce_riverside_citrus_qa', MAUK),
]

F5_ID = 'lemon_cold_threshold_single_source_divergence'
F5_APPEND = (
    ' [AMENDMENT 2026-08-06: a SEVENTH document, never cited by lemon, publishes a figure for '
    'exactly this crop. UCCE Placer/Nevada 31-018C (Fake, 2020), "Growing Citrus in the Sierra '
    'Nevada Foothills", gives a cultivar-named ladder ending "grapefruit (26F) > true lemons '
    '(Eureka, Lisbon) (28F) > lime (30F)". It names Eureka and Lisbon, the cultivars this parent '
    'entry covers, and its 28 matches the value this dataset carried before ae15df4 moved it to '
    '29 -- and its lime 30 matches our lime exactly, two rungs on a seven-rung ladder, which is a '
    'strong inference that this ladder or its lineage is where our citrus numbers came from '
    'uncited. Trevor RULED KEEP 29 on 2026-08-06: UC ANR 8100 is a numbered, peer-reviewed '
    'publication giving a duration-qualified damage ONSET (29F sustained 30 minutes or longer) '
    'and is the warmer safety edge, whereas 31-018C self-describes its numbers as "guidelines to '
    'assist in selecting appropriate species" -- a selection guideline, not an onset threshold. '
    'Tier plus claim-type decides it; 31-018C\'s greater cultivar specificity does not override. '
    'CAUTION: 31-018C is NOT INDEPENDENT of the Meyer 22F figure this crop already cites (Fake & '
    'Norton, 134971.pdf) -- same author, same ladder, ONE lineage, the reprint trap in a new '
    'costume. AND THIS FINDING\'S OWN FRAMING OF 26F IS NOW UNDERSTATED: it presents LSU '
    'AgCenter\'s 26F as a lone category-level figure, but UC MG Sacramento GN 127 independently '
    'publishes "Lemons and grapefruit 26F" for leaf and branch damage. TWO institutions publish '
    '26F, not one. The ruling to keep 29 still holds -- 29 remains the only duration-qualified '
    'onset figure and the safety edge -- but the record must be honest about what sits on the '
    'other side.]')

FINDINGS = [
    {
        'id': 'lemon_ca_interior_harvest_modeled_no_uc_window',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'MODELED DECLARATION, scoped to the documents read. No UC document read for campaign '
            'D publishes a lemon-specific harvest window for California\'s Central Valley, so '
            'ca_interior harvest_start and harvest_end remain modeled rather than sourced. '
            'Enumerated per absence-findings-are-document-scoped: UC MG Sacramento GN 127 (Central '
            'Valley) gives GENUS-LEVEL harvest only, "most citrus varieties ripen from late fall '
            'through winter", and its recommended home-garden varieties are navel and Valencia '
            'oranges, Satsuma mandarin, Meyer lemon and Bearss lime -- no true lemon; UCCE Kern '
            'KC9382 (San Joaquin) is a cultural and troubleshooting guide and publishes none; UC '
            'IPM\'s citrus timing chart is explicitly Central Valley but its Harvest row is '
            'GENERIC CITRUS; UCCE Merced\'s only citrus resource is UCCE Placer/Nevada #15C, the '
            'Fake lineage already covered. WHY THE GENUS-LEVEL STATEMENTS ARE NOT USED even '
            'though the form is admissible: F5 accepts LSU\'s category-level "about 26F for all '
            'other citrus", so a "most varieties" claim is admissible in FORM -- but lemon is the '
            'documented EXCEPTION to genus-level citrus harvest patterns, described as '
            'ever-bearing or year-round by four independent sources, so applying a most-varieties '
            'window to the crop repeatedly named as the exception is the wrong instrument. '
            'PARTIAL EXPLANATION, stated as partial: Sacramento\'s variety list suggests UC does '
            'not publish a Central Valley true-lemon harvest window because it does not really '
            'recommend true lemon there for home gardens. EVIDENCE AGAINST THAT, recorded rather '
            'than omitted: the Crop Profile for Citrus in California (2003) states Lisbon lemons '
            'are better adapted to the Desert, Interior and San Joaquin Valley regions with fruit '
            'harvested over a nine-month period. Both can be true -- the Crop Profile is '
            'commercial and Sacramento is home-garden. The Crop Profile is a LEAD, NOT A SOURCE: '
            'it gives a duration with no anchor, so citing it for harvest_start or harvest_end '
            'would credit a document for a claim it does not make, and its authorship is a '
            'stakeholder panel rather than extension-authored or peer-reviewed despite the UC '
            'host. Tier undecided; not admitted. '
            'WHAT "MODELED" DOES AND DOES NOT CLAIM HERE. It is a PROVENANCE statement -- this '
            'value came from the model rather than from a document -- and it is NOT a statement '
            'that the value is correct. An unqualified declaration would read as '
            'modeled-and-therefore-fine. ca_interior\'s harvest span is 95 days, which sits '
            'inside the suspect group flagged by PLA-151 (evergreen_fruit_tree harvest arms model '
            'an ever-bearing habit through a bloom-anchored offset built for determinate fruit): '
            'all 478 tree harvest arms anchor on bloom_start, which is correct for a determinate '
            'deciduous fruit and the wrong instrument for an evergreen ever-bearing one, doubly '
            'so here because lemon\'s bloom is itself modeled. So this cell may be both UNSOURCED '
            'and TOO NARROW, and those are separate defects with separate fixes.'),
    },
    {
        'id': 'lemon_bloom_modeled_every_region',
        'severity': 'low', 'status': 'open', 'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'MODELED DECLARATION. lemon\'s bloom arm stays modeled in EVERY region, including the '
            'Central Valley where a chart does exist. No T1 publishes a lemon bloom window for '
            'ca_north_coast, ca_south_coast, ca_desert or low_desert_az at all. For ca_interior a '
            'chart exists and is deliberately NOT used as lemon\'s bloom: UC IPM\'s citrus timing '
            'chart (UC ANR Pub 3441), re-derived from raw HTML 2026-08-06 rather than from a '
            'rendered image, gives a Bloom period of March plus the first half of April and is '
            'explicitly scoped to California\'s Central Valley -- but it is a COMMERCIAL Pest '
            'Management Guideline covering citrus generally, and Central Valley commercial citrus '
            'is dominated by navels and mandarins. It is citable for the main bloom of Central '
            'Valley CITRUS GENERALLY and must not be written as lemon\'s bloom. THE DEEPER REASON '
            'and the ruling behind this declaration: lemon may not have a discrete bloom window '
            'at all. Four independent sources describe it as ever-bearing -- Mauk & Shea (Improved '
            'Meyer "bears year round"), UC MG Santa Clara (Eureka "some fruit year-round"), UC '
            'Marin MG ("lemons and limes are considered ever-bearing"), UCCE SLO (flowers and '
            'fruit in spring, summer and fall) -- so filling a single Mar to mid-Apr window would '
            'assert a discrete bloom for the crop repeatedly named as the exception, the same '
            'error as reading lemon off UC IPM\'s generic Harvest row or off Lazaneo\'s hardiness '
            'ranking. Three UC counties PLACE the spring bloom without publishing it, by timing '
            'work around it: Sacramento fertilizes "in March before bloom", Santa Clara "February '
            'or March before bloom", SLO notes maximum stored food "late February/early March just '
            'before spring bloom". Placing is not publishing.'),
    },
    {
        'id': 'lemon_harvest_arms_uncitable_as_structured_and_may_render_too_narrow',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'USER-FACING CONTENT FINDING, not citation hygiene. Documents were FOUND for the '
            'low_desert_az, ca_desert and ca_south_coast harvest arms and were deliberately NOT '
            'cited, because no citation is admissible for these arms as they are currently '
            'structured. The documents publish ABSOLUTE CALENDAR WINDOWS; the cells compute from '
            'bloom_start plus an offset; and bloom is itself MODELED (see '
            'lemon_bloom_modeled_every_region). So the displayed value is produced by the model, '
            'not by any document. Repointing would credit a document for a value it did not '
            'produce, which is the defect F1 exists to record. Converting the documents\' absolute '
            'windows into bloom-anchored offsets would be worse: it pushes a sourced window '
            'through an unsourced anchor and then cites the document for the composite. '
            'THE CONSEQUENCE, SCOPED HONESTLY AFTER THE SOURCE-TRUTH SAMPLE. There are TWO '
            'reader-facing harvest surfaces and they disagree with each other. The zone-level '
            'harvest STRING is separately authored and is broadly consistent with the sources, '
            'several cells carrying an explicit year-round caveat: ca_south_coast reads "Nov - Mar '
            '(and scattered year-round; heaviest late winter to spring)" against Mauk & Shea\'s '
            '"bears year round on the coast", and low_desert_az reads "Nov - Mar (Eureka bears '
            'year-round)". The OFFSET-COMPUTED arms are the narrower surface: low_desert_az '
            'computes about 60 days where UA AZ1001 marks Eureka and Lisbon across fourteen '
            'half-month cells, August through February inclusive. Both surfaces render -- '
            'harvest_start and harvest_end drive plant-astro\'s SuccessionCard, '
            'TodayCommunityCard and PlantingCalendarCard, while the zone string renders '
            'elsewhere. AN EARLIER DRAFT OF THIS FINDING SAID a first-season grower is shown a '
            'harvest season roughly five months too short. THE SOURCE-TRUTH SAMPLE REFUTED THAT '
            'before it shipped: the reader also sees the harvest string and its year-round '
            'caveat, so the alarming version was not established. What IS established is narrower '
            'and still worth fixing: the two surfaces disagree, the offset-derived one is '
            'narrower than every source read, and low_desert_az\'s string omits August through '
            'October entirely -- three months AZ1001 marks for both cultivars. '
            'INTERNAL CORROBORATION NEEDING NO DOCUMENT: lime shares all nine of lemon\'s regions '
            'and is described by the same sources as the same ever-bearing habit, yet lime is '
            'modeled at a 180-day span in eight of them while lemon runs 60 to 125. '
            'AZ1001 is reachable at '
            'https://extension.arizona.edu/sites/extension.arizona.edu/files/pubs/az1001.pdf ; '
            'the /publication/low-desert-citrus-varieties path 403s in both plain and browser '
            'user-agent modes while the host root returns 200, so the block is path-specific '
            'rather than a bot policy. NOT YET RESOLVED: whether this is lemon-specific or an '
            'evergreen_fruit_tree modelling issue is under separate diagnosis.'),
    },
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    raw = open(CANONICAL, 'rb').read()
    got = hashlib.sha256(raw).hexdigest()
    if got != BASE_SHA:
        print(f'ABORT: canonical is {got[:16]}, expected {BASE_SHA[:16]}', file=sys.stderr)
        return 1
    print(f'base SHA verified: {got[:16]}')

    data = json.loads(raw)
    lemon = next(c for c in data['crops'] if c['slug'] == 'lemon')
    cat = data['source_catalog']

    for cid, entry in NEW_IDS.items():
        if cid in cat:
            print(f'ABORT: {cid} already catalogued', file=sys.stderr)
            return 1
        cat[cid] = entry
    print(f'minted {len(NEW_IDS)} ids')

    sd = cat['ucanr_san_diego_mg']
    if 'Lazaneo' in sd['citable_for']:
        print('ABORT: San Diego entry already admits Lazaneo', file=sys.stderr)
        return 1
    sd['citable_for'] += SAN_DIEGO_APPEND
    print('admitted Lazaneo under existing ucanr_san_diego_mg')

    data['source_catalog'] = dict(sorted(cat.items()))

    ss = lemon['verification_status']['source_set']
    for cid in ('ucce_placer_nevada_31_018c', 'ucce_riverside_citrus_qa', 'uc_mg_marin_citrus',
                'ucce_kern_kc9382', 'ucanr_san_diego_mg'):
        if cid not in ss:
            ss.append(cid)
    ss.sort()
    print('source_set ->', ss)

    for region, sid, url in PLANT_OUT:
        arm = lemon['regions'][region]['plantings'][0]['plant_out'][0]
        if sid in arm['sources']:
            print(f'ABORT: {region}/{sid} already cited', file=sys.stderr)
            return 1
        arm['sources'].append(sid)
        arm.setdefault('anchoring_urls', {})[sid] = {'url': url, 'verified': '2026-08-06'}
        print(f'  plant_out {region:16s} += {sid}')

    f5 = next(f for f in lemon['verification_status']['open_findings'] if f['id'] == F5_ID)
    if 'AMENDMENT 2026-08-06' in f5['summary']:
        print('ABORT: F5 already amended', file=sys.stderr)
        return 1
    original = f5['summary']
    f5['summary'] = original + F5_APPEND
    assert f5['summary'].startswith(original)
    print('F5 amended by append')

    existing = {f['id'] for f in lemon['verification_status']['open_findings']}
    for f in FINDINGS:
        if f['id'] in existing:
            print(f'ABORT: {f["id"]} already filed', file=sys.stderr)
            return 1
        lemon['verification_status']['open_findings'].append(f)
    print(f'filed {len(FINDINGS)} findings')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN -- {len(out)} bytes, sha {new_sha}')
        return 0
    open(CANONICAL, 'wb').write(out)
    print(f'wrote {len(out)} bytes\nnew canonical SHA: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
