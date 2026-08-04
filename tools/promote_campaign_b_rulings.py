#!/usr/bin/env python3
"""GUARDED PROMOTE: Trevor's rulings on campaign B's 7 open decisions.

CONSUMER PROSE + FINDING STATUS ONLY. Not one date, offset, suitability value or citation moves;
guards prove each of those separately.
Evidence: docs/2026-08-03-mid-atlantic-ncsu-ext-citation-hunt.md,
docs/2026-08-04-campaign-b-closeout-hunt.md.

THREE PROSE EDITS, six strings, all in fields VERIFIED to render in plant-astro before writing
(`suitability_note_*` in HardinessFruitingCard.astro, `grown_as_note_*` in
BerryYearCalendarCard.astro). A note in an unrendered field informs nobody.

  1. cherry-sweet mid_atlantic z8 -- REMOVE A CREDIT NC STATE DOES NOT SUPPORT. The cell told
     readers, in both registers, that "NC State Extension steers zone 8 growers toward sour cherry
     instead, which tolerates this humidity far better". No NC State document makes a zone-8 cherry
     recommendation; the handbook's eastern/central NC list contains no cherry of either kind; and
     the advantages NC State DOES publish are COLD HARDINESS and SELF-POLLINATION, not humidity.
     The fix is not deletion but RESTATEMENT: credit the two real claims, move the humidity
     sentence outside the attribution. That is exactly the shape cherry-sour's own z8 cell already
     uses, so the siblings stop contradicting each other.

  2. strawberry mid_south z8 -- TWO JOBS IN ONE STRING.
     (a) A SECOND LIVE INSTANCE OF A KNOWN FABRICATED CREDIT. `grown_as_note_seasoned` called the
         plasticulture system one "the University of Arkansas recommends". FSA6103 says it "is not
         recommended for home garden strawberry production at this time". The 2026-08-03 pass
         corrected this exact claim in `plantings_provenance` -- which RENDERS NOWHERE -- and did
         not reach this field, which renders TODAY. Removed subtractively: the credit goes, the
         horticultural fact stays (the herb-pass precedent).
     (b) THE TIMING GRADIENT. Trevor's ruling: KEEP the Sep 15 - Oct 5 window rather than trim it.
         The mechanism UAEX describes is continuous (fewer days -> fewer crowns -> fewer flowers),
         not a cliff, and no source claims a survival risk, so a late home planting still crops.
         Trimming would have had the WORSE failure mode: UAEX's own article notes growers delay
         when ground is too wet and that fall hurricanes push wet weather up from the Gulf, so a
         gardener who cannot plant until October 2 would read a Sep 30 cutoff, conclude the window
         had closed, and possibly not plant at all -- trading a lighter crop for none. The defect
         was never the tail; it was that a flat date range presents Sep 20 and Oct 3 as equivalent
         when UAEX measured that they are not. So the range stays and the GRADIENT goes in the copy.

  3. apricot mid_atlantic z8 -- ADD THE GEOGRAPHY THE CELL OMITTED. `marginal` is RETAINED (see
     below), but the note explained the limits as early bloom and brown rot and never mentioned
     that NC State's own plant database places apricot in the Mountains and Piedmont, zones 5a-7b,
     rather than the Coastal Plain, nor that its Pender County office reports apricots there are
     hard to keep alive beyond a few years. A reader deciding whether to plant one wants that.

EIGHT FINDING RECORDS CLOSED, and the two suitability tensions are closed as RECORDED-NOT-ACTIONED
on evidence that came in against the tightening. Cross-region calibration is what settled it:
apricot is `marginal` in se_gulf zones 8, 9 and 10, which are hotter and MORE humid than the
mid_atlantic Coastal Plain, so flipping mid_atlantic z8 to `unsuitable` would assert apricot does
better on the Gulf Coast than in Virginia and North Carolina, which is backwards. In every other
hot-humid region apricot is `survives_no_fruit`, never `unsuitable`. The cherries are weaker still:
their Toolbox range is 3a-8b, so zone 8 is INSIDE NC State's published range, and only one county
sentence pushes against -- a sentence that lumps cherries, bunch grapes, raspberries and apricots
under a single reason, which is the shape that turns out partly wrong when split by crop.

STAYS OPEN, deliberately: `strawberry_mid_south_plasticulture_home_garden_tension`. Two T1
documents from one institution genuinely disagree about whether the annual system belongs in a home
garden, and neither is wrong. Now that the false "UAEX recommends" credit is gone from the copy,
the remaining question is purely whether to present the system at all, which is Trevor's to rule.

    $ python3 tools/promote_campaign_b_rulings.py --dry-run
    $ python3 tools/promote_campaign_b_rulings.py --apply
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
BASE_SHA = '47a502afd95a8248c790ee005e7970672a62434cf4f1cc76dd3e7edac9b62286'
SESSION = 'campaign_b_rulings_2026_08_04'

CROPS = ('apricot', 'cherry-sour', 'cherry-sweet', 'elderberry', 'pomegranate', 'strawberry')

# (slug, region, zone, field, exact old substring, new substring, tokens that must survive)
EDITS = [
    ('cherry-sweet', 'mid_atlantic', '8', 'suitability_note_seasoned',
     'NC State Extension steers zone 8 growers toward sour cherry instead, which tolerates this '
     'humidity far better.',
     'If you want a cherry here, sour cherry is the better choice: NC State notes it is the '
     'hardier of the two, and unlike sweet cherry it is self fertile, so a single tree can set a '
     'crop on its own. It also carries this belt\'s humidity better.',
     ('sour cherry', 'self fertile')),
    ('cherry-sweet', 'mid_atlantic', '8', 'suitability_note_beginner',
     'NC State Extension actually points zone 8 growers toward pie (sour) cherry instead, since '
     'it handles the humidity much better.',
     'If you want a cherry, pie (sour) cherry is the easier one: NC State says it is the hardier '
     'of the two, and it is self fertile, so one tree can set fruit without a partner. It also '
     'handles humid summers better.',
     ('pie (sour) cherry', 'self fertile')),

    ('strawberry', 'mid_south', '8', 'grown_as_note_seasoned',
     'the plasticulture (annual-hill) system the University of Arkansas recommends, not a '
     'perennial bed: set plug transplants in mid-September through early October on raised, '
     'plastic-mulched rows with drip irrigation,',
     'the plasticulture (annual-hill) system, not a perennial bed: set plug transplants in '
     'mid-September through early October on raised, plastic-mulched rows with drip irrigation, '
     'as early in that window as your ground allows, since University of Arkansas trials measured '
     'a 15 to 35 percent yield loss when planting slipped from late September into the first week '
     'of October,',
     ('plasticulture', 'plastic-mulched rows', 'drip irrigation')),
    ('strawberry', 'mid_south', '8', 'grown_as_note_beginner',
     'Set transplants in September or early October on a raised, plastic-covered row.',
     'Set transplants in September or early October on a raised, plastic-covered row, and plant '
     'as early as you can manage: a planting that slips into October will still give you berries, '
     'just noticeably fewer.',
     ('plastic-covered row',)),

    ('apricot', 'mid_atlantic', '8', 'suitability_note_seasoned',
     'site it on a slope or high ground with good cold-air drainage to improve the odds.',
     'site it on a slope or high ground with good cold-air drainage to improve the odds. Be aware '
     'too that NC State\'s plant database places apricot in the Mountains and Piedmont, zones 5a '
     'to 7b, rather than on the Coastal Plain, and its Pender County office reports apricots '
     'there are hard to keep alive beyond a few years, so treat a Coastal Plain planting as a '
     'trial rather than a dependable fruit tree.',
     ('cold-air drainage', 'Coastal Plain')),
    ('apricot', 'mid_atlantic', '8', 'suitability_note_beginner',
     'Plant it on a slope, not a low spot where cold air pools, to improve your odds.',
     'Plant it on a slope, not a low spot where cold air pools, to improve your odds. Worth '
     'knowing: NC State lists apricot for the mountains and piedmont rather than the coastal '
     'plain, and its Pender County office says apricots are hard to keep alive here for more than '
     'a few years, so treat it as an experiment.',
     ('cold air pools',)),
]

# Claims that must NOT survive anywhere in these crops' prose after the edits.
BANNED = (
    'steers zone 8 growers toward sour cherry',
    'points zone 8 growers toward pie (sour) cherry',
    'the University of Arkansas recommends',
)

# finding id -> (slug, new status, resolution text)
RULINGS = {
    'mid_atlantic_cherry_sweet_sour_steer_attribution_unsupported': (
        'cherry-sweet', 'resolved',
        'RULED 2026-08-04 by Trevor: RESTATE, do not delete. The credit now names only what NC '
        'State publishes about sour cherry (it is the hardier of the two, and it is self fertile '
        'while sweet cherry needs a second variety), and the humidity claim moved OUTSIDE the '
        'attribution as our own assessment. That matches cherry-sour\'s own zone 8 cell, which '
        'had it right all along, so the two siblings no longer contradict each other. Deletion '
        'was rejected because NC State does support two real advantages and the steer toward sour '
        'cherry genuinely helps a reader; what was wrong was the zone-8 scope and the humidity '
        'rationale, not the recommendation itself. Applied in both registers.'),
    'mid_south_strawberry_z8_plant_out_late_tail': (
        'strawberry', 'resolved',
        'RULED 2026-08-04 by Trevor: KEEP the Sep 15 - Oct 5 window, express the gradient in the '
        'copy instead. The reasoning, which reversed the proposal to trim to Sep 15 - Sep 30: the '
        'mechanism UAEX describes is continuous rather than a threshold (fewer days before '
        'dormancy give fewer branch crowns, hence fewer flowers), no source claims a survival '
        'risk, and 15 to 35 percent of a home planting is a couple of quarts rather than a lost '
        'season. Trimming carried the worse failure mode: UAEX\'s own article notes growers must '
        'delay when ground is too wet and that fall hurricanes push wet weather up from the Gulf, '
        'so a gardener who cannot plant until October 2 would read a September 30 cutoff, '
        'conclude the window had closed and possibly not plant at all, trading a lighter crop for '
        'none. UAEX never says do not plant in October; it says every week of delay costs yield, '
        'which is advice to plant early, not a deadline. The real defect was that a flat date '
        'range presents September 20 and October 3 as equivalent, and that is now fixed in '
        'grown_as_note_seasoned and grown_as_note_beginner, both of which render in '
        'BerryYearCalendarCard.astro.'),
    'mid_atlantic_apricot_harvest_divergent': (
        'apricot', 'accepted_modeled',
        'RULED 2026-08-04: DECLARE MODELED, keep the values. The Plant Toolbox\'s "ripens in late '
        'June to July" is a species-level description of Prunus armeniaca with no regional '
        'harvest table behind it, while our window is derived from bloom plus 95 and 140 days and '
        'the bloom offset is itself unsourced. Retuning harvest to match would force changing '
        'bloom too, which is swapping one unsourced model for another -- the same call Trevor '
        'made on strawberry\'s bloom offset on 2026-08-03. The divergence stays recorded so a '
        'later pass does not "fix" it.'),
    'mid_atlantic_pomegranate_bloom_window_narrower_than_source': (
        'pomegranate', 'accepted_modeled',
        'RULED 2026-08-04: DECLARE MODELED. The two are not the same quantity. Beaufort County '
        'describes an ORNAMENTAL long-bloom habit running from April well into fall; our field '
        'models the fruit-setting bloom that the harvest window derives from. Taking the source '
        'literally would produce a bloom band covering most of the year, which renders as noise '
        'and tells a gardener nothing. Noted for the record: zone 8\'s Apr 29 start does touch '
        'April as the source says, and zone 7\'s May 6 does not.'),
    'mid_south_elderberry_no_uaex_planting_model': (
        'elderberry', 'accepted_modeled',
        'RULED 2026-08-04: DECLARE MODELED. "Midsummer" in a Plant of the Week garden column is a '
        'season word, not a phenology observation, and it is weaker evidence than the model it '
        'would overturn; zone 7\'s August to September harvest already matches the same page\'s '
        '"late summer" berries. This crop has never had a gold-standard pass, and that is when to '
        'source its months properly rather than on the strength of one adjective. The absence of '
        'elderberry from UAEX\'s home-garden berry guide stays recorded.'),
    'mid_atlantic_apricot_coastal_plain_suitability_tension': (
        'apricot', 'accepted',
        'RULED 2026-08-04: RECORDED, NOT ACTIONED. `marginal` is RETAINED. Cross-region '
        'calibration settled it against the tightening: apricot is `marginal` in se_gulf zones 8, '
        '9 and 10, which are hotter and MORE humid than the mid_atlantic Coastal Plain, so '
        'flipping this cell to `unsuitable` would assert the crop does better on the Gulf Coast '
        'than in Virginia and North Carolina, which is backwards. In every other hot-humid region '
        'apricot is `survives_no_fruit`, never `unsuitable`. What the evidence DID justify is '
        'prose: the zone 8 note now tells the reader that NC State places apricot in the '
        'Mountains and Piedmont, zones 5a to 7b, rather than the Coastal Plain, and that its '
        'Pender County office reports trees there are hard to keep alive beyond a few years.'),
    'mid_atlantic_cherry_coastal_plain_suitability_tension': (
        None, 'accepted',      # filed on BOTH cherries; slug resolved per-crop below
        'RULED 2026-08-04: RECORDED, NOT ACTIONED. `marginal` is RETAINED on both cherries. The '
        'case is weaker than apricot\'s: the Plant Toolbox gives both Prunus cerasus and Prunus '
        'avium as 3a-8b, so zone 8 sits INSIDE NC State\'s published range, and the only evidence '
        'pushing against is a single Pender County sentence that lumps cherries, bunch grapes, '
        'raspberries and apricots under one reason -- the shape that repeatedly turns out partly '
        'wrong when split by crop. No prose change either, since the cherry cells already tell '
        'the reader not to count on an annual crop.'),
}

NEW_FINDING = ('strawberry', {
    'id': 'mid_south_strawberry_grown_as_note_uaex_credit_removed',
    'severity': 'medium', 'status': 'resolved', 'blocks_launch': False,
    'summary': (
        'A SECOND, STILL-LIVE instance of the fabricated UAEX credit corrected on 2026-08-03. '
        'That pass found `plantings_provenance` claiming the University of Arkansas "pioneered '
        'and RECOMMENDS" the zone 8 annual plasticulture system when FSA6103 says it "is not '
        'recommended for home garden strawberry production at this time", and corrected it by '
        'appending a dated CORRECTION. The same claim also sat in '
        '`grown_as_note_seasoned` as "the plasticulture (annual-hill) system the University of '
        'Arkansas recommends", and was missed. The distinction that matters: `plantings_provenance` '
        'RENDERS NOWHERE, while `grown_as_note_seasoned` renders TODAY in '
        'BerryYearCalendarCard.astro, so the corrected record was invisible to readers and the '
        'uncorrected one was not. Removed subtractively here per the herb-pass precedent: the '
        'credit goes, the horticultural fact stays. Lesson for the next attribution fix: correct '
        'EVERY field carrying the claim, and check the rendering ones first.'),
    'basis': 'UAEX FSA6103; strawberry mid_south z8 grown_as_note_seasoned as of 47a502af; '
             'plant-astro BerryYearCalendarCard.astro field read, verified 2026-08-04.',
    'filed_in_session': SESSION,
})

EM_DASH = chr(8212)


def cell_of(crops, slug, region, zone):
    return crops[slug]['regions'][region]['resolved_by_zone'][zone]


def findings_of(crop):
    return (crop.get('verification_status') or {}).get('open_findings') or []


def all_prose(crop):
    out = {}
    for reg, r in (crop.get('regions') or {}).items():
        for z, cell in ((r or {}).get('resolved_by_zone') or {}).items():
            for k, v in cell.items():
                if isinstance(v, str):
                    out['%s.%s.%s' % (reg, z, k)] = v
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

    # PREFLIGHT -- every ruling must land on a finding that EXISTS and is still open.
    targets = []
    for fid, (slug, status, _res) in RULINGS.items():
        holders = [s for s in CROPS
                   for f in findings_of(crops[s]) if f.get('id') == fid]
        if not holders:
            print('ABORT: ruling names %s but no crop carries it' % fid)
            return 2
        if slug is not None and holders != [slug]:
            print('ABORT: %s expected on %s, found on %s' % (fid, slug, holders))
            return 2
        for s in holders:
            f = next(x for x in findings_of(crops[s]) if x.get('id') == fid)
            if f.get('status') != 'open':
                print('ABORT: %s on %s is %r, not open -- already ruled?'
                      % (fid, s, f.get('status')))
                return 2
            targets.append((s, fid, status))
    print('preflight: %d finding records open and ready to rule' % len(targets))

    if any(f.get('id') == NEW_FINDING[1]['id'] for f in findings_of(crops[NEW_FINDING[0]])):
        print('ABORT: finding %s already filed' % NEW_FINDING[1]['id'])
        return 2

    # PREFLIGHT -- the tension Trevor ruled to LEAVE OPEN must still be open, and stay that way.
    KEEP_OPEN = 'strawberry_mid_south_plasticulture_home_garden_tension'
    keep = next((f for f in findings_of(crops['strawberry']) if f.get('id') == KEEP_OPEN), None)
    if keep is None or keep.get('status') != 'open':
        print('ABORT: %s is not open; its premise changed' % KEEP_OPEN)
        return 2
    print('preflight: the plasticulture tension is open and will be left that way')

    # ---- edits -----------------------------------------------------------------------------
    applied = []
    for slug, region, zone, field, old, new, keep_toks in EDITS:
        cell = cell_of(crops, slug, region, zone)
        cur = cell.get(field)
        if not isinstance(cur, str) or cur.count(old) != 1:
            print('ABORT: %s %s z%s %s does not contain the expected text exactly once'
                  % (slug, region, zone, field))
            return 2
        cell[field] = cur.replace(old, new)
        for tok in keep_toks:
            if tok not in cell[field]:
                print('ABORT: %s %s lost the fact %r' % (slug, field, tok))
                return 2
        applied.append('%s %s z%s %s' % (slug, region, zone, field))

    for slug, fid, status in targets:
        f = next(x for x in findings_of(crops[slug]) if x.get('id') == fid)
        f['status'] = status
        f['resolution'] = RULINGS[fid][2]
        f['resolved_in_session'] = SESSION
        applied.append('%s %s -> %s' % (slug, fid, status))

    findings_of(crops[NEW_FINDING[0]]).append(copy.deepcopy(NEW_FINDING[1]))
    applied.append('%s finding %s' % (NEW_FINDING[0], NEW_FINDING[1]['id']))

    # ---- guards ----------------------------------------------------------------------------
    # G1 -- LOAD-BEARING. Not one banned claim may survive in ANY prose on these crops.
    for slug in CROPS:
        for path, v in all_prose(crops[slug]).items():
            for b in BANNED:
                if b in v:
                    print('ABORT: %s %s still carries the banned claim %r' % (slug, path, b))
                    return 2
    print('verified: 0 banned claims remain in any of the %d crops\' prose' % len(CROPS))

    # G2 house style on every rewritten string.
    for slug, region, zone, field, _o, _n, _k in EDITS:
        v = cell_of(crops, slug, region, zone)[field]
        if EM_DASH in v or '--' in v:
            print('ABORT: em dash or "--" in consumer copy: %s %s' % (slug, field))
            return 2
        if '  ' in v or ' ,' in v or ' .' in v or '..' in v:
            print('ABORT: whitespace/punctuation artifact: %s %s' % (slug, field))
            return 2
    print('verified: no em dash, doubled space, or orphaned punctuation in the 6 strings')

    # G3 -- LOAD-BEARING. This promote may not move a single datum. Suitability values, dates and
    # citations are all asserted UNCHANGED, separately, because the whole ruling turned on
    # retaining them.
    bmap = {c['slug']: c for c in before['crops']}
    DATA_KEYS = ('suitability', 'plant_out', 'bloom', 'harvest', 'harvest_start', 'harvest_end',
                 'calendar', 'resolved_from', 'sources', 'anchoring_urls', 'heat_pause')
    for slug in CROPS:
        for reg, r in (bmap[slug].get('regions') or {}).items():
            for z, bcell in ((r or {}).get('resolved_by_zone') or {}).items():
                acell = crops[slug]['regions'][reg]['resolved_by_zone'][z]
                for k in DATA_KEYS:
                    if bcell.get(k) != acell.get(k):
                        print('ABORT: %s %s z%s %s changed; this promote is prose only'
                              % (slug, reg, z, k))
                        return 2
            if (r or {}).get('plantings') != crops[slug]['regions'][reg].get('plantings'):
                print('ABORT: %s %s plantings changed; this promote is prose only' % (slug, reg))
                return 2
    print('verified: no suitability, date, calendar or citation moved anywhere')

    # G4 exactly the 6 intended strings moved, and nothing else in prose.
    for slug in CROPS:
        b, a = all_prose(bmap[slug]), all_prose(crops[slug])
        moved = {k for k in b if b[k] != a.get(k)}
        expect = {'%s.%s.%s' % (reg, z, f) for s, reg, z, f, _o, _n, _k in EDITS if s == slug}
        if moved != expect:
            print('ABORT: %s prose moved %s, expected %s' % (slug, sorted(moved), sorted(expect)))
            return 2
    print('verified: exactly %d strings moved, all intended' % len(EDITS))

    # G5 the plasticulture tension must STILL be open -- Trevor ruled to leave it.
    after = next(f for f in findings_of(crops['strawberry']) if f.get('id') == KEEP_OPEN)
    if after.get('status') != 'open':
        print('ABORT: %s was closed; Trevor ruled to leave it open' % KEEP_OPEN)
        return 2
    print('verified: the plasticulture tension is still open, as ruled')

    # G6 no finding was dropped, and every ruled one carries a dated resolution.
    for slug in CROPS:
        bids = [f.get('id') for f in findings_of(bmap[slug])]
        aids = [f.get('id') for f in findings_of(crops[slug])]
        if bids != aids[:len(bids)]:
            print('ABORT: %s findings were reordered or dropped' % slug)
            return 2
    for slug, fid, _st in targets:
        f = next(x for x in findings_of(crops[slug]) if x.get('id') == fid)
        if '2026-08-04' not in f.get('resolution', ''):
            print('ABORT: %s resolution carries no ruling date' % fid)
            return 2
    print('verified: no finding dropped; every ruling dated')

    # G7 exact footprint.
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in bmap if bmap[s] != aa[s])
    if changed != sorted(CROPS):
        print('ABORT: crops changed = %s, expected %s' % (changed, sorted(CROPS)))
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
