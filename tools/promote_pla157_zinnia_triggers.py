#!/usr/bin/env python3
"""PLA-157: zinnia's shifted weather_triggers register block + the six body-length titles.
Base ce9eb12f.

The defect (PLA-138 phase-1 instrument audit §5b): certified zinnia's three weather_triggers
shipped with the dual-register block SHIFTED ONE SLOT -- title_beginner held the seasoned body
prose, body_seasoned held the beginner prose, and body_beginner held a raw source id
(clemson_hgic_1149 x2, uf_ifas_zinnia), a consumer-facing field. whole_crop_gate passed: an
identifier satisfies both A29 (non-null) and the compound population check (non-empty).
Second instance: bee-balm's three title_beginner slots carried body-length prose (117-147 chars)
over correct bodies.

The fix is deliberately BYTE-PRESERVING on zinnia's prose: the two body strings per trigger are
ROTATED BACK, not re-authored (they passed the cert verbatim gate at zinnia_step11_cert and the
register comparison against marigold's healthy templates confirms which slot each belongs in).
The only newly authored prose is six short beginner titles. The stray ids return to their
triggers' `sources` -- both documents re-read 2026-08-10 and support the claims they anchor:
Clemson HGIC 1149 publishes the airflow / base-watering / spacing powdery-mildew guidance
(trigger 1) and the last-frost sowing that establishes frost-tenderness (trigger 0); UF/IFAS
Gardening Solutions publishes "zinnias can handle Florida's hot summers ... bloom throughout the
summer, often until the first frost" (trigger 2). Both are T1 in source_catalog (admission
zinnia_steps4_5_se_gulf). Neither crop's cert log is touched: per
docs/verification_log_ref_convention.md this fix retires nothing the logs assert (no correction
line owed); the record lands in open_findings instead, status resolved.

Gates added alongside (measured before wiring): A52 identifier-shaped consumer prose, A53 title
length -- tools/trigger_prose_gate.py.

Usage: python3 tools/promote_pla157_zinnia_triggers.py [--dry-run] [canonical.json]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
# Re-based 2026-08-10: PLA-155 promoted first (ce9eb12f -> 4f610318, disjoint footprint --
# zinnia/bee-balm/marigold byte-identical across the move, verified before re-pinning).
BASE_SHA = '4f6103183ac9c07475b3e0c2d3a71159d0662a10a61383e1d792c049957cac23'

CLEMSON_ID = 'clemson_hgic_1149'
CLEMSON_URL = 'https://hgic.clemson.edu/factsheet/how-to-grow-zinnias-the-best-varieties-care-tips/'
UF_ID = 'uf_ifas_zinnia'
UF_URL = 'https://gardeningsolutions.ifas.ufl.edu/plants/ornamentals/zinnia/'
VERIFIED = '2026-08-10'

# per zinnia trigger: (stray id expected in body_beginner, new short beginner title)
ZINNIA_FIX = [
    (CLEMSON_ID, 'Frost warning'),
    (CLEMSON_ID, 'Damp weather warning'),
    (UF_ID, 'Hot weather ahead'),
]
RESTORED_URL = {CLEMSON_ID: CLEMSON_URL, UF_ID: UF_URL}

BEEBALM_TITLES = ['Damp weather warning', 'Hot, dry weather', 'Frost and winter rest']

ZINNIA_FINDING = {
    'id': 'pla157_weather_trigger_register_shift',
    'type': 'consumer_copy_structural',
    'severity': 'high',
    'status': 'resolved',
    'blocks_launch': False,
    'summary': (
        'All three weather_triggers shipped with the dual-register block shifted one slot: '
        'title_beginner held the seasoned body prose, body_seasoned held the beginner prose, and '
        'body_beginner, a consumer-facing field, held a raw source id (clemson_hgic_1149 x2, '
        'uf_ifas_zinnia). whole_crop_gate passed: an identifier satisfies both A29 (non-null '
        'register) and the compound population check (non-empty). Fixed 2026-08-10 (PLA-157): '
        'the two body strings per trigger rotated back byte-identical (cert-verbatim-checked '
        'prose, not re-authored), three short beginner titles authored, and the stray ids '
        'restored to their triggers\' sources with both documents re-read the same day (Clemson '
        'HGIC 1149: airflow, base watering, and spacing against powdery mildew, plus last-frost '
        'sowing; UF/IFAS zinnia: blooms through summer heat until first frost). A52 '
        '(identifier-shaped consumer prose) and A53 (title length) added to whole_crop_gate; '
        'measured roster-wide before wiring, these values were the only hits.'),
    'basis': ('PLA-138 phase-1 instrument audit (docs/2026-08-06-pla138-phase1-instrument-audit.md '
              '§5b), filed as PLA-157. Register placement adjudicated against marigold\'s healthy '
              'trigger templates. Cert log untouched per '
              'docs/verification_log_ref_convention.md (nothing it asserts is retired).'),
}
BEEBALM_FINDING = {
    'id': 'pla157_title_beginner_body_prose',
    'type': 'consumer_copy_structural',
    'severity': 'medium',
    'status': 'resolved',
    'blocks_launch': False,
    'summary': (
        'All three weather_triggers\' title_beginner slots carried body-length prose (117-147 '
        'chars) restating the body content instead of a short title; both body_* registers were '
        'correct prose. Replaced 2026-08-10 (PLA-157) with short beginner titles; no body prose, '
        'sourcing, or other field touched. A53 now gates the class (max 80 chars, measured '
        'against a 60-char legitimate roster maximum).'),
    'basis': 'PLA-138 phase-1 instrument audit §5b, filed as PLA-157.',
}


def _crop(data, slug):
    return next(c for c in data['crops'] if c['slug'] == slug)


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

    zin = _crop(data, 'zinnia')
    bee = _crop(data, 'bee-balm')

    # -- pre-state pins ---------------------------------------------------------------------
    zt = zin['weather_triggers']
    bt = bee['weather_triggers']
    _pin(len(zt) == 3 and len(bt) == 3, 'trigger counts moved')
    for i, (stray_id, _) in enumerate(ZINNIA_FIX):
        _pin(zt[i]['body_beginner'] == stray_id, f'zinnia[{i}] body_beginner is not the stray id')
        _pin(len(zt[i]['title_beginner']) > 80, f'zinnia[{i}] title_beginner is not body-length')
        _pin(stray_id not in zt[i]['sources'], f'zinnia[{i}] already cites {stray_id}')
    _pin(zt[0]['sources'] == ['umn_ext'], 'zinnia[0] sources moved')
    _pin(zt[1]['sources'] == ['uc_ipm'], 'zinnia[1] sources moved')
    _pin(zt[2]['sources'] == [CLEMSON_ID], 'zinnia[2] sources moved')
    for i in range(3):
        _pin(len(bt[i]['title_beginner']) > 80, f'bee-balm[{i}] title_beginner is not body-length')
    for c, f in ((zin, ZINNIA_FINDING), (bee, BEEBALM_FINDING)):
        ids = [x.get('id') for x in c['verification_status']['open_findings']]
        _pin(f['id'] not in ids, f"{c['slug']} already carries {f['id']}")

    # -- zinnia: rotate the block back; author the title; restore the id -------------------
    for i, (stray_id, title) in enumerate(ZINNIA_FIX):
        t = zt[i]
        t['body_beginner'] = t['body_seasoned']
        t['body_seasoned'] = t['title_beginner']
        t['title_beginner'] = title
        t['sources'] = t['sources'] + [stray_id]
        t['anchoring_urls'][stray_id] = {'url': RESTORED_URL[stray_id], 'verified': VERIFIED}

    # -- bee-balm: titles only --------------------------------------------------------------
    for i, title in enumerate(BEEBALM_TITLES):
        bt[i]['title_beginner'] = title

    # -- record the repair in open_findings (cert logs untouched) ---------------------------
    zin['verification_status']['open_findings'].append(ZINNIA_FINDING)
    bee['verification_status']['open_findings'].append(BEEBALM_FINDING)

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
