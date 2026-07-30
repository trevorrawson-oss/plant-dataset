#!/usr/bin/env python3
"""GUARDED PROMOTE: the three mid_south fruit corrections the UAEX document hunt found.

VALUE CHANGES. Trevor-approved 2026-07-30. Evidence:
docs/2026-07-30-mid-south-uada-ext-citation-hunt.md. Scope is mid_south ONLY -- mid_atlantic is
deliberately untouched, because its rabbiteye/sour-cherry calls are correctly sourced to NC State
for the Piedmont and Coastal Plain, which is its stated geography.

1. blueberry z7  rabbiteye -> northern_highbush (+ 4 prose fields), z8 keeps rabbiteye but loses
   its false exclusion of northern highbush.

   THREE University of Arkansas documents place the types opposite to our cell:
     FSA6104  "The northern highbush type is better adapted to the northern part of the state";
              northern highbush at HIGHER elevations, rabbiteye at LOWER, in central Arkansas.
     FSA6130  section headers "Northern Highbush (Northern and Central Ark.)" vs
              "Rabbiteye (Central and Southern Ark.)".
     berries  "In Arkansas, northern highbush blueberries are grown in the northern counties, and
              rabbiteyes are grown in more central and southern areas."
   z7 IS the northern/upland belt (the region's own note: "NW AR Ozarks (Fayetteville)").

   WHERE OUR VALUE CAME FROM: the phrase "below 2,500 feet" still sitting in the provenance is NC
   State's threshold for the NORTH CAROLINA PIEDMONT. mid_south was built from the mid_atlantic
   cell as a structural template (mid_south_sources.md section 7 directs exactly that) and the
   Piedmont steer came across relabeled as an Arkansas steer.

   WHY IT MATTERS MORE THAN A CITATION: rabbiteye is the southern species -- less cold hardy, and
   low-chill (350-600 h), so an upland warm spell pushes it into bloom ahead of a killing freeze.
   Northern highbush needs 800-1,000 h, which z7's 1,000-1,300 h supplies, and blooms later. The
   shipped value pointed a z7 gardener at the bush most likely to grow well and then fruit nothing.
   Corroborated internally: our own northern_tier z7 already uses northern_highbush, and mid_south
   z7 banks MORE chill than northern_tier z7.

   Pollination advice changes with the type and this is a real correction, not a reword: rabbiteye
   is self-INfertile (the old note demanded a second rabbiteye "to set a crop"), while FSA6130 says
   "Southern and Northern highbush cultivars are generally self-fertile but benefit from planting
   two or more cultivars which can improve fruit size and number."

2. fig + raspberry  dormant winter planting -> early spring.
     fig        "Dec - Feb (dormant plant)"  -> "Mar - Apr (dormant plant)", arm -60d -> -21d
     raspberry  "December to March"          -> "March to April",            arm months likewise
   UAEX, Home Garden Fruit Trees: "Fig trees should not be planted until early spring", and the
   sentence licensing every other tree fruit explicitly carves figs out ("Fruit trees OTHER THAN
   FIGS, could be planted in the fall"). FSA6107: "Planting should occur in the spring as soon as
   the soil can be properly prepared."

   Dates DERIVED from UAEX's statement against Arkansas's own frost anchors (z7 last_frost Apr 10,
   z8 Apr 3), NOT copied from northern_tier -- whose sources (UMaine/UNH/UMass/Rutgers, and for fig
   umd_ext/clemson_hgic) do not cover Arkansas. last_frost - 21d lands Mar 20 (z7) / Mar 13 (z8),
   both inside "Mar - Apr", and matches the house encoding northern_tier already uses for fig.
   SCOPE: mid_south only. The Dec-Feb window is a roster-wide convention and is plausibly correct
   in the mild-winter regions; UAEX governs Arkansas and nothing else.

3. cherry-sour  fruits_reliably -> marginal, both zones, + a FABRICATED ATTRIBUTION removed from
   cherry-sweet z8.
   FSA6129: "Given the climate in Arkansas, both apricots and cherries trees can be grown but will
   not reliably set fruit." It says "cherries" unqualified and gives NO cherry cultivar table at
   all, while listing cultivars for apples, pears, peaches and nectarines. That same sentence is
   what already supports apricot and cherry-sweet at `marginal`.
   THE FABRICATION: cherry-sweet z8 currently reads "University of Arkansas Cooperative Extension
   steers zone 8 growers toward sour cherry instead" -- that is the mid_atlantic sentence with
   "NC State Extension" swapped out. NC State does make that steer and it is the sound basis of
   Trevor's 2026-07-20 ruling FOR MID_ATLANTIC. UAEX does not make it. Removed in both registers.

Also resolves the four open_findings filed for these defects at 14c8eab2.

FOOTPRINT: every edit asserts its exact prior value and aborts on any drift. Calendars are NOT
touched -- these are woody-perennial calendars with no `plant` token, so a planting-window change
does not move them (asserted). COMPACT preserved.

    $ python3 tools/promote_mid_south_fruit_corrections.py --dry-run
    $ python3 tools/promote_mid_south_fruit_corrections.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '5f58654b1fceb057a37cfaec7c77ef5c5d6e3a8de69847781cf237da89121b20'
SESSION = 'mid_south_uada_hunt_corrections_2026_07_30'

BB7_TYPE_S = (
    "Northern highbush is the type the University of Arkansas recommends for the northern part of "
    "the state, and that covers the Ozark uplands: Duke and Bluecrop are the dependable defaults, "
    "both named by the University of Arkansas as long adapted in Arkansas. The belt's winter "
    "chill, roughly 1,000 to 1,300 hours, comfortably meets their 800 to 1,000 hour requirement. "
    "Rabbiteye belongs to central and southern Arkansas rather than these uplands: it is the less "
    "cold hardy type, and its low chill requirement, about 350 to 600 hours, lets a warm "
    "late-winter spell push it into bloom ahead of a killing freeze. Northern highbush drops its "
    "leaves and rests fully dormant through the belt's real winter.")

BB7_TYPE_B = (
    "Northern highbush, such as Duke or Bluecrop, is the type the University of Arkansas "
    "recommends for this part of the state. Your winters are cold enough to give these bushes the "
    "chilling they need, and they bloom late enough to dodge most spring freezes. Rabbiteye is the "
    "type for central and southern Arkansas: up here it is more likely to be hurt by winter cold, "
    "or tricked into blooming early by a warm spell and then caught by a freeze. Your bush will "
    "lose its leaves and rest each winter.")

BB7_FROST = (
    "Northern highbush will not break bud until it has taken its full chilling, so it blooms late "
    "here and usually escapes spring freezes; Duke is specifically noted for blooming relatively "
    "late. A warm late-winter spell moves it far less than it moves the low-chill southern types.")

BB7_GROWN = (
    "Northern highbush is a permanent deciduous shrub in the Ozark uplands' real winter, planted "
    "once and productive for decades. It rests dormant and leafless through winter, then blooms in "
    "spring, sets fruit, and ripens across early summer. After leaf drop, prune late in the dormant "
    "season, just before bud break. Plant at least two different northern highbush cultivars with "
    "overlapping bloom: this type is self fertile, but the University of Arkansas notes that two or "
    "more cultivars improve fruit size and number. The belt's winter chill, roughly 1,000 to 1,300 "
    "hours, comfortably covers this type's 800 to 1,000 hour requirement.")

CS_SEASONED = (
    "Chill is never the limiter here: the belt delivers roughly {chill} chilling hours a year in "
    "zone {z}, clearing this crop's variety range with margin (University of Arkansas Cooperative "
    "Extension Chilling Hour Reports). Bloom and harvest weather is what limits it. The University "
    "of Arkansas groups cherries with apricots as trees that can be grown in the state but will "
    "not reliably set fruit: both bloom early enough to meet a frost or freeze, and the heavy "
    "rainfall common here during ripening splits the fruit. Sour cherry is the more forgiving of "
    "the two cherries and handles the humidity better than sweet, so it is the one to choose if "
    "you want a cherry, but expect a crop in good years rather than every year.")

CS_BEGINNER = (
    "Winters here are cold enough for this tree, so chilling is not the problem. Spring and summer "
    "weather is: it blooms early and can lose its flowers to a late freeze, and heavy rain right "
    "at ripening splits the fruit. The University of Arkansas says cherries can be grown in the "
    "state but will not set fruit reliably. Sour cherry is the better of the two cherries here, so "
    "choose it over sweet, but expect fruit in good years rather than every year.")

# (slug, kind, path, old, new)  kind: SET | SUB | ARM
EDITS = [
    ('blueberry', 'SET', ('7', 'recommended_type'), 'rabbiteye', 'northern_highbush'),
    ('blueberry', 'SET', ('7', 'type_note_seasoned'), None, BB7_TYPE_S),
    ('blueberry', 'SET', ('7', 'type_note_beginner'), None, BB7_TYPE_B),
    ('blueberry', 'SET', ('7', 'frost_risk_note_seasoned'), None, BB7_FROST),
    ('blueberry', 'SET', ('7', 'grown_as_note_seasoned'), None, BB7_GROWN),
    ('blueberry', 'SUB', ('8', 'type_note_seasoned'),
     'while northern highbush is too heat-stressed to recommend here.',
     'while the University of Arkansas also lists northern highbush as adapted to central '
     "Arkansas, so it is a workable second choice toward the belt's cooler, upland edge."),

    ('fig', 'SET', ('7', 'plant_out'), 'Dec - Feb (dormant plant)', 'Mar - Apr (dormant plant)'),
    ('fig', 'SET', ('8', 'plant_out'), 'Dec - Feb (dormant plant)', 'Mar - Apr (dormant plant)'),

    ('raspberry', 'SET', ('7', 'plant_out'), 'December to March', 'March to April'),
    ('raspberry', 'SET', ('8', 'plant_out'), 'December to March', 'March to April'),
    ('raspberry', 'SUB', ('7', 'grown_as_note_seasoned'),
     'Set dormant bare-root canes over winter into early spring, plant',
     'Set dormant bare-root canes in early spring, as soon as the soil can be worked, plant'),
    ('raspberry', 'SUB', ('7', 'grown_as_note_beginner'),
     'Plant dormant canes in winter or early spring on a raised, well-drained bed',
     'Plant dormant canes in early spring, as soon as the soil can be worked, on a raised, '
     'well-drained bed'),
    ('raspberry', 'SUB', ('8', 'grown_as_note_seasoned'),
     'Set dormant canes over winter, trellis',
     'Set dormant canes in early spring, trellis'),

    ('cherry-sour', 'SET', ('7', 'suitability'), 'fruits_reliably', 'marginal'),
    ('cherry-sour', 'SET', ('8', 'suitability'), 'fruits_reliably', 'marginal'),
    ('cherry-sour', 'SET', ('7', 'suitability_note_seasoned'), None,
     CS_SEASONED.format(chill='1,000 to 1,300', z='7')),
    ('cherry-sour', 'SET', ('8', 'suitability_note_seasoned'), None,
     CS_SEASONED.format(chill='900 to 1,100', z='8')),
    ('cherry-sour', 'SET', ('7', 'suitability_note_beginner'), None, CS_BEGINNER),
    ('cherry-sour', 'SET', ('8', 'suitability_note_beginner'), None, CS_BEGINNER),

    ('cherry-sweet', 'SUB', ('8', 'suitability_note_seasoned'),
     'University of Arkansas Cooperative Extension steers zone 8 growers toward sour cherry '
     'instead, which tolerates this humidity far better.',
     'Sour cherry tolerates this humidity better and is the safer choice of the two, though the '
     'University of Arkansas cautions that neither cherry sets fruit reliably in the state.'),
    ('cherry-sweet', 'SUB', ('8', 'suitability_note_beginner'),
     'University of Arkansas Cooperative Extension actually points zone 8 growers toward pie '
     '(sour) cherry instead, since it handles the humidity much better.',
     'Pie (sour) cherry handles the humidity better and is the safer choice of the two, though the '
     'University of Arkansas cautions that no cherry fruits reliably in the state.'),
]

PROVENANCE_SUB = (
    'blueberry',
    "recommended_type is rabbiteye in BOTH zones per the sourcing note's the University of "
    "Arkansas steer (docs/reviews/notes/2026-07-20/mid_south_sources.md section 6): rabbiteye is "
    "the best choice for most upland soils below 2,500 feet (Premier/Powderblue/Climax), with "
    "highbush (Duke/Jersey) named specifically as the lowland South alternative on higher-organic "
    "soils.",
    "recommended_type CORRECTED 2026-07-30: z7 northern_highbush, z8 rabbiteye. The original fill "
    "set rabbiteye in BOTH zones from the 2026-07-20 sourcing note, whose 'below 2,500 feet' steer "
    "is NC State's claim about the NORTH CAROLINA PIEDMONT, carried across when this region was "
    "built from the mid_atlantic template and relabeled as a University of Arkansas steer; no "
    "Arkansas document supports it for the uplands. THREE University of Arkansas documents place "
    "the types the other way: FSA6104 ('the northern highbush type is better adapted to the "
    "northern part of the state'), FSA6130 (headers 'Northern Highbush (Northern and Central "
    "Ark.)' vs 'Rabbiteye (Central and Southern Ark.)'), and the Arkansas Berries page ('northern "
    "highbush blueberries are grown in the northern counties, and rabbiteyes are grown in more "
    "central and southern areas'). z7 is the Ozark upland/northern belt and takes northern "
    "highbush; z8 is central Arkansas, where rabbiteye is correct and stays.")

# findings closed by this promote
RESOLVE = {
    'blueberry': 'mid_south_blueberry_recommended_type_inverted',
    'fig': 'mid_south_fig_dormant_planting_contradicted',
    'raspberry': 'mid_south_raspberry_dormant_planting_contradicted',
    'cherry-sour': 'mid_south_cherry_sour_suitability_ruling_needed',
}
RESOLUTIONS = {
    'blueberry': 'FIXED 2026-07-30 (Trevor-approved): z7 -> northern_highbush; z8 keeps rabbiteye '
                 'and loses its false exclusion of northern highbush. mid_atlantic deliberately '
                 'untouched, its rabbiteye call being correctly sourced to NC State for the '
                 'Piedmont.',
    'fig': 'FIXED 2026-07-30 (Trevor-approved): plant_out -> "Mar - Apr (dormant plant)" in both '
           'zones, arm offset last_frost -60d -> -21d, derived from UAEX\'s "early spring" against '
           "Arkansas's own frost anchors rather than copied from a region whose sources do not "
           'cover Arkansas.',
    'raspberry': 'FIXED 2026-07-30 (Trevor-approved): plant_out -> "March to April" in both zones, '
                 'arm months likewise, and the three prose strings that stated winter planting '
                 'moved to early spring.',
    'cherry-sour': 'RULED 2026-07-30 (Trevor): mid_south -> marginal, matching apricot and '
                   'cherry-sweet, which the same FSA6129 sentence supports. Trevor\'s 2026-07-20 '
                   'fruits_reliably ruling stands for mid_atlantic on NC State evidence and is '
                   'NOT disturbed. The UAEX-attributed sour-cherry steer on cherry-sweet z8 was a '
                   'find-and-replace of the NC State sentence and has been removed.',
}


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

    def cell(slug, z):
        return crops[slug]['regions']['mid_south']['resolved_by_zone'][z]

    # snapshot calendars: a planting-window change must NOT move a woody-perennial calendar
    cal_before = {(s, z): list(cell(s, z).get('calendar') or [])
                  for s in ('fig', 'raspberry', 'blueberry', 'cherry-sour', 'cherry-sweet')
                  for z in ('7', '8')}

    applied = []
    for slug, kind, (z, field), old, new in EDITS:
        c = cell(slug, z)
        cur = c.get(field)
        if kind == 'SET':
            if old is not None and cur != old:
                print('ABORT: %s z%s %s expected %r, found %r' % (slug, z, field, old, cur))
                return 2
            if cur == new:
                print('ABORT: %s z%s %s already at the new value' % (slug, z, field))
                return 2
            c[field] = new
        elif kind == 'SUB':
            if not isinstance(cur, str) or cur.count(old) != 1:
                print('ABORT: %s z%s %s does not contain the expected text exactly once'
                      % (slug, z, field))
                return 2
            c[field] = cur.replace(old, new)
        applied.append('%s z%s %s' % (slug, z, field))

    # structural arms
    fig_arm = crops['fig']['regions']['mid_south']['plantings'][0]['plant_out'][0]
    if fig_arm.get('offset_days') != -60 or fig_arm.get('from') != 'last_frost':
        print('ABORT: fig arm is not the expected last_frost -60d shape')
        return 2
    fig_arm['offset_days'] = -21
    applied.append('fig plantings[0].plant_out[0].offset_days -60 -> -21')

    rasp_arm = crops['raspberry']['regions']['mid_south']['plantings'][0]
    if rasp_arm.get('plant_out') != ['December', 'March']:
        print('ABORT: raspberry arm is not ["December","March"], found %r'
              % (rasp_arm.get('plant_out'),))
        return 2
    rasp_arm['plant_out'] = ['March', 'April']
    applied.append('raspberry plantings[0].plant_out -> ["March","April"]')

    # provenance
    slug, old, new = PROVENANCE_SUB
    ms = crops[slug]['regions']['mid_south']
    if (ms.get('plantings_provenance') or '').count(old) != 1:
        print('ABORT: %s plantings_provenance does not contain the expected text once' % slug)
        return 2
    ms['plantings_provenance'] = ms['plantings_provenance'].replace(old, new)
    applied.append('blueberry plantings_provenance')

    # calendars must be untouched
    for key, cal in cal_before.items():
        if list(cell(key[0], key[1]).get('calendar') or []) != cal:
            print('ABORT: calendar moved for %s z%s' % key)
            return 2
    print('verified: no calendar moved')

    # resolve the findings this promote closes
    for slug, fid in RESOLVE.items():
        ofs = (crops[slug].get('verification_status') or {}).get('open_findings') or []
        hit = [f for f in ofs if isinstance(f, dict) and f.get('id') == fid]
        if len(hit) != 1:
            print('ABORT: expected exactly 1 finding %s on %s, found %d' % (fid, slug, len(hit)))
            return 2
        if hit[0].get('status') == 'resolved':
            print('ABORT: finding %s already resolved' % fid)
            return 2
        hit[0]['status'] = 'resolved'
        hit[0]['resolution'] = RESOLUTIONS[slug]
        hit[0]['resolved_in'] = SESSION
        applied.append('%s finding %s -> resolved' % (slug, fid))

    # house style: no em dash / "--" in any consumer string we wrote
    EM = chr(8212)
    for _slug, kind, (z, field), _o, _n in EDITS:
        v = cell(_slug, z).get(field)
        if isinstance(v, str) and (EM in v or '--' in v):
            print('ABORT: em dash or "--" in consumer copy: %s z%s %s' % (_slug, z, field))
            return 2
    print('verified: no em dash or "--" in the rewritten consumer copy')

    # exact footprint: only the crops we intend, only the fields we intend
    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    EXPECT = ['blueberry', 'cherry-sour', 'cherry-sweet', 'fig', 'raspberry']
    if changed != EXPECT:
        print('ABORT: crops changed = %s, expected %s' % (changed, EXPECT))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    print('verified: exactly %d crops changed, nothing else' % len(changed))

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
