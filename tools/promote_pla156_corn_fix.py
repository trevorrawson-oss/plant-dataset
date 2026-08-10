#!/usr/bin/env python3
"""PLA-156 verification pass: the two held dispositions, corrected. Base db853c4b.

The claude.ai lane held two of its own five dispositions and asked this session to VERIFY rather
than accept. Both failed verification, in the same direction: the sourcing pass did not know the
crops' own certification records, and neither did the morning promote.

  * popcorn's cert verification_log records days_to_maturity [90,110] as a SYNTHESIS Trevor
    ratified at promote "from convergent extension figures -- Iowa State variety table 85-112d,
    UMN 'most varieties require 90 to 120 days'; no single T1 quotes the exact band." The widen
    of one se_gulf prose string to UMN's 90-120 re-adjudicated that settled band and left the
    crop carrying THREE values (90-120 in se_gulf, 100-110 in eleven sibling regions, [90,110]
    at crop level). REVERTED here; the repoint to UMN + Iowa State stays (they publish the
    moisture figure and are the ratified band's own named inputs).
  * field-corn's cert log records [95,120] as a ratified synthesis whose FIRST named input is
    "Clemson HGIC 'from 90 to 120 days after planting for most varieties'" -- a home-garden
    extension DTM the sourcing pass reported not finding. Re-found independently and READ
    2026-08-10 (hgic.clemson.edu/homegrown-grits/): it publishes the 90-120 band, the husk cue
    ("Harvest when the husks are dry, brown and papery") and the drying guidance. flint-corn's
    log likewise records [90,110] as a ratified synthesis from Cornell and NCSU variety figures.
    So the morning findings calling these DTMs "MODELED" mischaracterize the crops' own records.
    Both findings are CORRECTED in place (same ids, correction acknowledged inline); the
    harvest arms gain the citation their non-DTM claims support: clemson_hgic on field-corn,
    iastate_ext (ornamental-corn page, read 2026-08-10, harvest cues + drying) on flint-corn.

What stays: the do-not-repoint-at-B577 pin (B577's 80-100 Corn row still contradicts all three
bands); uga_b577 on every sow arm and zone cell; sweet-corn untouched.

Usage: python3 tools/promote_pla156_corn_fix.py [--dry-run] [canonical.json]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'db853c4b20e889a93d8946e947b31a2c7a00f49042e8774a04dc7386bca9e7a5'

CLEMSON_URL = 'https://hgic.clemson.edu/homegrown-grits/'
ISU_ORN_URL = 'https://yardandgarden.extension.iastate.edu/how-to/growing-and-harvesting-ornamental-corn'
VERIFIED = '2026-08-10'

POPCORN_HS_WIDENED = ('The block reaches its dry-down harvest about 90 to 120 days after sowing, '
                      'when the husks are brown and papery and the kernels are hard and glossy; '
                      'the crop is then cured to the popping window (about 13 to 14 percent '
                      'moisture).')
POPCORN_HS_RESTORED = ('The block reaches its dry-down harvest about 100 to 110 days after '
                       'sowing, when the husks are brown and papery and the kernels are hard and '
                       'glossy; the crop is then cured to the popping window (about 13 to 14 '
                       'percent moisture).')

FINDINGS = {
    'popcorn': {
        'id': 'pla156_popcorn_dtm_widened_to_published_range',
        'summary': ('[CORRECTED same day, 2026-08-10: the widen this finding first recorded was '
                    'REVERTED on the dependency check the claude.ai lane asked for.] se_gulf '
                    'harvest arms repointed to UMN + Iowa State, which publish the 13 to 14 '
                    'percent popping moisture independently and are the two named inputs of the '
                    'crop\'s ratified DTM band. The harvest_start prose was briefly widened to '
                    'UMN\'s "90 to 120 days"; verification found the crop\'s own '
                    'verification_log records days_to_maturity [90,110] as a SYNTHESIS Trevor '
                    'ratified at certification (ISU variety table 85-112d + UMN 90-120, "no '
                    'single T1 quotes the exact band"), and eleven sibling regions carry the '
                    'same "about 100 to 110 days" prose. The widen re-adjudicated a settled '
                    'band and created a third value, so it was reverted: the prose narrowing '
                    'rests on the cert-ratified synthesis, not on the cell\'s citations, which '
                    'anchor the moisture and drying claims they publish. uga_b577 re-scoped to '
                    'the sow claims (its Corn row, 80-100, is sweet corn and publishes no '
                    'popcorn figure).'),
        'blocks_launch': False,
        'status': 'accepted',
        'basis': ('PLA-156 dispositions 1+4 applied; disposition 2 (widen) held by the '
                  'claude.ai lane, verified here, and reverted. Cert record: '
                  'popcorn.verification_status.verification_log, PROVISIONAL band synthesis.'),
    },
    'field-corn': {
        'id': 'pla156_field_corn_harvest_dtm_modeled',
        'summary': ('[CORRECTED same day, 2026-08-10: this finding first called the DTM MODELED; '
                    'that mischaracterized the crop\'s own records.] The 110 to 120 day '
                    'dry-down figure in se_gulf harvest prose is a narrowing WITHIN the '
                    'cert-ratified days_to_maturity [95,120], which the crop\'s '
                    'verification_log records as a SYNTHESIS Trevor ratified at certification '
                    'from convergent extension figures, first among them Clemson HGIC "from 90 '
                    'to 120 days after planting for most varieties". That document '
                    '(hgic.clemson.edu/homegrown-grits/, home-garden register, dent corn) was '
                    're-found and READ 2026-08-10: it publishes the 90-120 band, the husk cue '
                    'and the drying guidance, and now anchors both harvest arms for the claims '
                    'it publishes; the exact 110-120 sentence rests on the ratified synthesis. '
                    'uga_b577 removed from the harvest arms and retained on the sow arms. DO '
                    'NOT repoint these arms at B577\'s Corn row: it reads 80-100 days '
                    '(home-garden sweet corn) and CONTRADICTS this crop\'s band. MU IPM\'s '
                    'relative-maturity 98-120 read and not cited (an RM rating is not a '
                    'calendar DTM).'),
        'blocks_launch': False,
        'status': 'accepted',
        'basis': ('PLA-156 dispositions; the modeled call was held by the claude.ai lane, '
                  'verified here, and corrected. Cert record: '
                  'field-corn.verification_status.verification_log, PROVISIONAL band synthesis.'),
    },
    'flint-corn': {
        'id': 'pla156_flint_corn_harvest_dtm_modeled',
        'summary': ('[CORRECTED same day, 2026-08-10: this finding first called the DTM MODELED; '
                    'that mischaracterized the crop\'s own records.] The 90 to 110 day figure '
                    'in se_gulf harvest prose IS the cert-ratified days_to_maturity [90,110], '
                    'which the crop\'s verification_log records as a SYNTHESIS Trevor ratified '
                    'at certification from convergent variety figures (Painted Mountain ~85 per '
                    'cornell_ext, Floriani ~100, Glass Gem 105-110 per ncsu_ext; "no single T1 '
                    'quotes the exact band"). Iowa State\'s ornamental-corn page (READ '
                    '2026-08-10) publishes the harvest cues and drying guidance and now anchors '
                    'both harvest arms for those claims; the band sentence rests on the '
                    'ratified synthesis. uga_b577 removed from the harvest arms and retained on '
                    'the sow arms. DO NOT repoint these arms at B577\'s Corn row: it reads '
                    '80-100 days (home-garden sweet corn) and CONTRADICTS this crop\'s band.'),
        'blocks_launch': False,
        'status': 'accepted',
        'basis': ('PLA-156 dispositions; the modeled call was held by the claude.ai lane, '
                  'verified here, and corrected. Cert record: '
                  'flint-corn.verification_status.verification_log, PROVISIONAL band synthesis.'),
    },
}

PROV_APPEND = {
    'popcorn': (' [PLA-156 verification 2026-08-10: the prose widen recorded above was REVERTED '
                'the same day. The crop\'s cert log ratifies [90,110] as a convergent synthesis '
                'and eleven sibling regions carry "100 to 110"; the se_gulf prose returns to '
                'that narrowing, whose basis is the ratified band, while UMN + Iowa State stay '
                'cited for the moisture and drying claims they publish.]'),
    'field-corn': (' [PLA-156 verification 2026-08-10: the "no citation" state recorded above '
                   'was superseded the same day. The cert log ratifies [95,120] as a convergent '
                   'synthesis whose first input is Clemson HGIC\'s published "90 to 120 days"; '
                   'that document was read and now anchors both harvest arms for the husk-cue '
                   'and drying claims it publishes. The 110-120 sentence rests on the ratified '
                   'synthesis.]'),
    'flint-corn': (' [PLA-156 verification 2026-08-10: the "no citation" state recorded above '
                   'was superseded the same day. The cert log ratifies [90,110] as a convergent '
                   'synthesis from Cornell and NCSU variety figures; Iowa State\'s '
                   'ornamental-corn page was read and now anchors both harvest arms for the '
                   'harvest-cue and drying claims it publishes. The band sentence rests on the '
                   'ratified synthesis.]'),
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

    # -- pre-state pins: exactly the morning promote's output ------------------------------
    hs, he = _arms(_crop(data, 'popcorn'))
    _pin(hs['synthesis_note_seasoned'] == POPCORN_HS_WIDENED, 'popcorn prose is not the widened text')
    _pin(hs['sources'] == ['umn_ext', 'iastate_ext'], 'popcorn hs sources moved')
    for slug in ('field-corn', 'flint-corn'):
        for arm in _arms(_crop(data, slug)):
            _pin(arm['sources'] == [] and arm['anchoring_urls'] == {}, f'{slug} arm not uncited')
    for slug, f in FINDINGS.items():
        of = _crop(data, slug)['verification_status']['open_findings']
        _pin(len(of) == 1 and of[0]['id'] == f['id'], f'{slug} findings moved')
        _pin('[CORRECTED' not in of[0]['summary'], f'{slug} finding already corrected')

    # -- popcorn: revert the widen, keep the repoint ---------------------------------------
    hs['synthesis_note_seasoned'] = POPCORN_HS_RESTORED

    # -- field/flint: cite the documents their non-DTM claims support ----------------------
    for arm in _arms(_crop(data, 'field-corn')):
        arm['sources'] = ['clemson_hgic']
        arm['anchoring_urls'] = {'clemson_hgic': {'url': CLEMSON_URL, 'verified': VERIFIED}}
    for arm in _arms(_crop(data, 'flint-corn')):
        arm['sources'] = ['iastate_ext']
        arm['anchoring_urls'] = {'iastate_ext': {'url': ISU_ORN_URL, 'verified': VERIFIED}}

    # -- findings corrected in place; provenance amended by second append ------------------
    for slug, finding in FINDINGS.items():
        crop = _crop(data, slug)
        crop['verification_status']['open_findings'][0] = finding
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
