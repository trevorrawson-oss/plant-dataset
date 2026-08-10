#!/usr/bin/env python3
"""PLA-156 corn dispositions: the grain corns' harvest credits, corrected per claim. Base 72284f02.

WHAT THIS DOES (the five dispositions from the 2026-08-10 sourcing pass, recorded on PLA-156):
  1. popcorn se_gulf harvest arms REPOINT to UMN + Iowa State, the two T1 documents that publish
     the numbers (90-120 day range; 13-14 percent popping moisture, independently in both).
  2. popcorn's harvest_start DTM prose WIDENS from the unpublished narrowing "100 to 110 days" to
     UMN's published "90 to 120 days". The one consumer-facing string this promote moves.
  3. field-corn and flint-corn harvest arms go UNCITED (sources [], anchors {}), each with an
     open finding declaring the DTM MODELED, absence scoped to the six documents read, and a
     DO-NOT-REPOINT pin: B577's single Corn row reads 80-100 days (home-garden sweet corn), which
     CONTRADICTS all three grain-corn DTMs -- a future "fix" pointing these arms at it would
     write 80-100 into three crops and call it sourced.
  4. uga_b577 is RE-SCOPED, not dropped: it stays on every sow arm, plantings-level anchor and
     zone cell it genuinely supports (its Mar 15 spring opening; sowing is species-level).
  5. The Mar 15 - Apr 30 sow cutoff is recorded in provenance as OUR narrowing of B577's
     Mar 15 - Jun 1 window (conservative direction), per disposition 5.

WHAT IT DELIBERATELY DOES NOT DO: sweet-corn is untouched (B577 supports it to the day, including
the z9/z10 Mar 1 starts via the chart's own South-Georgia footnote). Crop-level days_to_maturity
on all three grain corns is untouched: a separate datum with separate provenance, out of PLA-156's
scope. Zone harvest strings are untouched: month-granular touch-sets that remain reachable under
both the modeled and the published DTM bands.

Usage: python3 tools/promote_pla156_corn.py [--dry-run] [canonical.json]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '72284f0291442919d005a8546f6cfbdcdf06502fe7842327fa77201e5c9c8571'

UMN_URL = 'https://extension.umn.edu/vegetables/growing-popcorn'
ISU_URL = 'https://yardandgarden.extension.iastate.edu/how-to/growing-and-harvesting-popcorn-home-garden'
VERIFIED = '2026-08-10'

# Every pre-state string this promote touches, pinned byte-for-byte. A mismatch means canonical
# is not the state this transform was written against -- abort, never fuzzy-match.
POPCORN_HS_OLD = ('The block reaches its dry-down harvest about 100 to 110 days after sowing, '
                  'when the husks are brown and papery and the kernels are hard and glossy; the '
                  'crop is then cured to the popping window (about 13 to 14 percent moisture).')
POPCORN_HS_NEW = ('The block reaches its dry-down harvest about 90 to 120 days after sowing, '
                  'when the husks are brown and papery and the kernels are hard and glossy; the '
                  'crop is then cured to the popping window (about 13 to 14 percent moisture).')
POPCORN_HE = ('Harvest ends when the dried ears are all in. Sound ears can field-dry on the '
              'stalk in good weather; in humid weather they are picked at hard-dry and finished '
              'drying under cover.')
FIELD_HS = ('The block reaches its dry-down grain harvest about 110 to 120 days after sowing, '
            'when the husks are brown and papery and the kernels are hard and dented.')
FIELD_HE = ('Harvest ends when the dried ears are all in. Sound ears can field-dry on the stalk '
            'in good weather; in humid weather they are pulled at hard dent and finished drying '
            'under cover.')
FLINT_HS = ('The block reaches its dry-down grain harvest when the husks are brown and papery '
            'and the kernels are hard and glassy: flint matures in about 90 to 110 days, then '
            'the ears field-dry for a week or two before they are pulled.')
FLINT_HE = ('Harvest ends when the dried ears are all in. Sound ears can field-dry on the stalk '
            'in good weather; in humid weather they are pulled once the kernels are hard and '
            'glassy and finished drying under cover.')

PROV_APPEND = {
    'popcorn': (' [PLA-156 2026-08-10: harvest arms repointed to UMN and Iowa State, which '
                'publish the 90 to 120 day range and the 13 to 14 percent popping moisture; the '
                'harvest_start DTM prose widened to the published range; uga_b577 re-scoped to '
                'the sow arms it supports. The Mar 15 - Apr 30 sow cutoff is our full-season '
                'narrowing of B577\'s Mar 15 - Jun 1 window.]'),
    'field-corn': (' [PLA-156 2026-08-10: uga_b577 re-scoped to the sow arms it supports; both '
                   'harvest arms now carry no citation because the 110 to 120 day figure is '
                   'MODELED (see open finding pla156_field_corn_harvest_dtm_modeled). The Mar 15 '
                   '- Apr 30 sow cutoff is our full-season narrowing of B577\'s Mar 15 - Jun 1 '
                   'window.]'),
    'flint-corn': (' [PLA-156 2026-08-10: uga_b577 re-scoped to the sow arms it supports; both '
                   'harvest arms now carry no citation because the 90 to 110 day figure is '
                   'MODELED (see open finding pla156_flint_corn_harvest_dtm_modeled). The Mar 15 '
                   '- Apr 30 sow cutoff is our full-season narrowing of B577\'s Mar 15 - Jun 1 '
                   'window.]'),
}

FINDINGS = {
    'popcorn': {
        'id': 'pla156_popcorn_dtm_widened_to_published_range',
        'summary': ('se_gulf harvest_start DTM prose widened from the unpublished narrowing '
                    '"about 100 to 110 days" to UMN Extension\'s published "90 to 120 days" '
                    '(read 2026-08-10). The 13 to 14 percent popping moisture is published '
                    'INDEPENDENTLY by UMN, Iowa State and WVU, each in its own wording. Both '
                    'harvest arms now cite documents that state their numbers. uga_b577 '
                    're-scoped to the sow claims: its single Corn row (80-100 days, home-garden '
                    'sweet corn) publishes no popcorn figure. Crop-level days_to_maturity '
                    '[90,110] deliberately untouched: separate datum, separate provenance.'),
        'blocks_launch': False,
        'status': 'accepted',
        'basis': ('PLA-156 sourcing pass 2026-08-10, six T1 documents read. UMN '
                  'extension.umn.edu/vegetables/growing-popcorn; Iowa State Y&G popcorn '
                  'home-garden page.'),
    },
    'field-corn': {
        'id': 'pla156_field_corn_harvest_dtm_modeled',
        'summary': ('The 110 to 120 day dry-down figure in se_gulf harvest prose, and the zone '
                    'harvest strings derived from it, are MODELED from variety-class norms. No '
                    'home-garden extension DTM for field corn was found; absence is scoped to '
                    'the six documents read 2026-08-10 (UMN, Iowa State x2, WVU, Utah State, '
                    'SDSU, plus Purdue Agronomy and Iowa State ICM, which treat field corn as '
                    'commercial agronomy: growth stages, black layer, drydown rate, harvest at '
                    'about 25 percent grain moisture -- none of which is a DTM). uga_b577 '
                    'removed from both harvest arms and retained on the sow arms it supports. '
                    'DO NOT repoint these arms at B577\'s Corn row: it reads 80-100 days '
                    '(home-garden sweet corn) and CONTRADICTS this crop\'s DTM. MU IPM '
                    'publishes hybrid RELATIVE MATURITY "typically between 98 and 120"; an RM '
                    'rating is not a calendar DTM and was not cited for this claim.'),
        'blocks_launch': False,
        'status': 'accepted',
        'basis': 'PLA-156 dispositions, claude.ai sourcing pass 2026-08-10.',
    },
    'flint-corn': {
        'id': 'pla156_flint_corn_harvest_dtm_modeled',
        'summary': ('The 90 to 110 day figure in se_gulf harvest prose (inherited from the '
                    'field-corn dry-down synthesis per plantings_provenance), and the zone '
                    'harvest strings derived from it, are MODELED from variety-class norms. '
                    'Extension covers flint corn as decoration: SDSU ("Indian Corn & Popcorn") '
                    'and Iowa State ("Growing and Harvesting Ornamental Corn") both cover the '
                    'crop and publish NO DTM at all, harvest cues only (husks dry, ears fully '
                    'mature); UMass NEVMG likewise. Absence scoped to the six documents read '
                    '2026-08-10. uga_b577 removed from both harvest arms and retained on the '
                    'sow arms it supports. DO NOT repoint these arms at B577\'s Corn row: it '
                    'reads 80-100 days (home-garden sweet corn) and CONTRADICTS this crop\'s '
                    'DTM.'),
        'blocks_launch': False,
        'status': 'accepted',
        'basis': 'PLA-156 dispositions, claude.ai sourcing pass 2026-08-10.',
    },
}


def _crop(data, slug):
    return next(c for c in data['crops'] if c['slug'] == slug)


def _arms(crop):
    pl = crop['regions']['se_gulf']['plantings'][0]
    return pl['harvest_start'][0], pl['harvest_end'][0]


def _pin(cond, msg):
    if not cond:
        print(f'ABORT (pre-state pin failed): {msg}', file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    args = ap.parse_args()

    raw = open(args.canonical, 'rb').read()
    got = hashlib.sha256(raw).hexdigest()
    _pin(got == BASE_SHA, f'canonical is {got[:8]}, transform written against {BASE_SHA[:8]}')
    data = json.loads(raw)

    # -- pre-state pins ---------------------------------------------------------------------
    pins = {'popcorn': (POPCORN_HS_OLD, POPCORN_HE), 'field-corn': (FIELD_HS, FIELD_HE),
            'flint-corn': (FLINT_HS, FLINT_HE)}
    for slug, (hs_txt, he_txt) in pins.items():
        hs, he = _arms(_crop(data, slug))
        _pin(hs['synthesis_note_seasoned'] == hs_txt, f'{slug} harvest_start prose moved')
        _pin(he['synthesis_note_seasoned'] == he_txt, f'{slug} harvest_end prose moved')
        for arm, name in ((hs, 'harvest_start'), (he, 'harvest_end')):
            _pin(arm['sources'] == ['uga_b577'], f'{slug} {name} sources are not sole-uga_b577')
            _pin(list(arm['anchoring_urls'].keys()) == ['uga_b577'], f'{slug} {name} anchors moved')
        _pin(_crop(data, slug)['verification_status']['open_findings'] == [],
             f'{slug} open_findings not empty')
        _pin('[PLA-156' not in _crop(data, slug)['regions']['se_gulf']['plantings_provenance'],
             f'{slug} provenance already amended')

    # -- disposition 1 + 2: popcorn repoints and widens -------------------------------------
    hs, he = _arms(_crop(data, 'popcorn'))
    hs['synthesis_note_seasoned'] = POPCORN_HS_NEW
    for arm in (hs, he):
        arm['sources'] = ['umn_ext', 'iastate_ext']
        arm['anchoring_urls'] = {'umn_ext': {'url': UMN_URL, 'verified': VERIFIED},
                                 'iastate_ext': {'url': ISU_URL, 'verified': VERIFIED}}

    # -- disposition 3 + 4: field/flint harvest arms go honestly uncited --------------------
    for slug in ('field-corn', 'flint-corn'):
        for arm in _arms(_crop(data, slug)):
            arm['sources'] = []
            arm['anchoring_urls'] = {}

    # -- findings + provenance appends (disposition 5 recorded in both) ---------------------
    for slug, finding in FINDINGS.items():
        crop = _crop(data, slug)
        crop['verification_status']['open_findings'].append(finding)
        crop['regions']['se_gulf']['plantings_provenance'] += PROV_APPEND[slug]

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN ok: {BASE_SHA[:8]} -> {new_sha[:8]} ({len(out)} bytes, not written)')
        return
    with open(args.canonical, 'wb') as f:
        f.write(out)
    print(f'PROMOTED: {BASE_SHA[:8]} -> {new_sha[:8]}')


if __name__ == '__main__':
    main()
