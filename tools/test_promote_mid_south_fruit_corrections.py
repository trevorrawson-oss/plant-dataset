#!/usr/bin/env python3
"""Adversarially test the guards on promote_mid_south_fruit_corrections.py.

This one edits VALUES on certified crops, so the guards that matter are the ones proving we
changed only what we meant to and nothing drifted underneath us. Each is exercised by injecting
the failure into a SCRATCH COPY.

Runs under pytest AND as a script; the skip guard is in the TEST BODY so pytest sees it.

    $ python3 -m pytest tools/test_promote_mid_south_fruit_corrections.py -q
    $ python3 tools/test_promote_mid_south_fruit_corrections.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
SCRIPT = os.path.join(REPO, 'tools', 'promote_mid_south_fruit_corrections.py')
BASE_SHA = '5f58654b1fceb057a37cfaec7c77ef5c5d6e3a8de69847781cf237da89121b20'


def _canonical_is_base():
    if not os.path.exists(CANON):
        return False
    with open(CANON, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest() == BASE_SHA


def _write(path, data):
    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    with open(path, 'wb') as fh:
        fh.write(out)
    return hashlib.sha256(out).hexdigest()


def _run(path, sha, apply_=False):
    p = subprocess.run([sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
                        '--canonical', path, '--expect-sha', sha],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def _scratch(mutate=None):
    tmp = tempfile.mkdtemp(prefix='msfix_')
    path = os.path.join(tmp, 'crops.json')
    shutil.copy2(CANON, path)
    with open(path, 'rb') as fh:
        raw = fh.read()
    if mutate is None:
        return path, hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    mutate({c['slug']: c for c in data['crops']}, data)
    return path, _write(path, data)


def _cell(crops, slug, z):
    return crops[slug]['regions']['mid_south']['resolved_by_zone'][z]


def test_guards():
    if not _canonical_is_base():
        print('SKIP: canonical is not the pinned base SHA')
        return
    results = []

    def check(name, ok, detail=''):
        results.append((name, ok, detail))
        print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))

    # 1. clean dry-run, exactly 28 edits over exactly 5 crops
    path, sha = _scratch()
    rc, out = _run(path, sha)
    check('clean dry-run succeeds', rc == 0)
    check('28 edits planned', '28 edits' in out)
    check('exactly 5 crops changed', 'exactly 5 crops changed' in out)

    # 2. SHA drift
    path, sha = _scratch()
    rc, out = _run(path, '0' * 64)
    check('SHA drift aborts', rc == 2 and 'drifted' in out)

    # 3. a prior value drifted -> abort rather than overwrite silently
    def drift(crops, _d):
        _cell(crops, 'fig', '7')['plant_out'] = 'Jan - Feb (dormant plant)'
    path, sha = _scratch(drift)
    rc, out = _run(path, sha)
    check('changed prior value -> abort', rc == 2 and 'expected' in out)

    # 4. the SUB target text is gone (someone reworded it) -> abort
    def reword(crops, _d):
        c = _cell(crops, 'cherry-sweet', '8')
        c['suitability_note_seasoned'] = c['suitability_note_seasoned'].replace(
            'University of Arkansas Cooperative Extension steers', 'NC State Extension steers')
    path, sha = _scratch(reword)
    rc, out = _run(path, sha)
    check('SUB text absent -> abort', rc == 2 and 'exactly once' in out)

    # 5. arm shape drifted -> abort
    def arm_drift(crops, _d):
        crops['fig']['regions']['mid_south']['plantings'][0]['plant_out'][0]['offset_days'] = -30
    path, sha = _scratch(arm_drift)
    rc, out = _run(path, sha)
    check('fig arm drifted -> abort', rc == 2 and 'not the expected last_frost -60d' in out)

    def rasp_drift(crops, _d):
        crops['raspberry']['regions']['mid_south']['plantings'][0]['plant_out'] = ['January', 'March']
    path, sha = _scratch(rasp_drift)
    rc, out = _run(path, sha)
    check('raspberry arm drifted -> abort', rc == 2 and 'not ["December","March"]' in out)

    # 6. finding missing (never filed, or already resolved) -> abort
    def unresolve(crops, _d):
        ofs = crops['fig']['verification_status']['open_findings']
        for f in ofs:
            if f.get('id') == 'mid_south_fig_dormant_planting_contradicted':
                f['status'] = 'resolved'
    path, sha = _scratch(unresolve)
    rc, out = _run(path, sha)
    check('finding already resolved -> abort', rc == 2 and 'already resolved' in out)

    # 7. idempotency: re-running against already-corrected data aborts
    def precorrect(crops, _d):
        _cell(crops, 'blueberry', '7')['recommended_type'] = 'northern_highbush'
    path, sha = _scratch(precorrect)
    rc, out = _run(path, sha)
    check('already-corrected input -> abort', rc == 2)

    # 8. APPLY on scratch and verify the result in detail
    path, sha = _scratch()
    with open(path, 'rb') as fh:
        before = json.loads(fh.read())
    rc, out = _run(path, sha, apply_=True)
    with open(path, 'rb') as fh:
        raw_after = fh.read()
    after = json.loads(raw_after)
    check('apply succeeds', rc == 0 and 'APPLIED: 28 edits' in out)
    check('no trailing newline', not raw_after.endswith(b'\n'))

    bb = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in after['crops']}
    changed = sorted(s for s in bb if bb[s] != aa[s])
    check('exactly the 5 intended crops',
          changed == ['blueberry', 'cherry-sour', 'cherry-sweet', 'fig', 'raspberry'], str(changed))

    def cell(d, slug, z):
        return d[slug]['regions']['mid_south']['resolved_by_zone'][z]

    check('blueberry z7 -> northern_highbush',
          cell(aa, 'blueberry', '7')['recommended_type'] == 'northern_highbush')
    check('blueberry z8 stays rabbiteye',
          cell(aa, 'blueberry', '8')['recommended_type'] == 'rabbiteye')
    check('blueberry z7 prose no longer recommends rabbiteye',
          'Rabbiteye is the University of Arkansas' not in cell(aa, 'blueberry', '7')['type_note_seasoned'])
    check('blueberry z8 false exclusion gone',
          'too heat-stressed to recommend here' not in cell(aa, 'blueberry', '8')['type_note_seasoned'])
    check('fig plant_out -> Mar - Apr, both zones',
          all(cell(aa, 'fig', z)['plant_out'] == 'Mar - Apr (dormant plant)' for z in ('7', '8')))
    check('fig arm -> -21d',
          aa['fig']['regions']['mid_south']['plantings'][0]['plant_out'][0]['offset_days'] == -21)
    check('raspberry plant_out -> March to April, both zones',
          all(cell(aa, 'raspberry', z)['plant_out'] == 'March to April' for z in ('7', '8')))
    check('raspberry arm -> March/April',
          aa['raspberry']['regions']['mid_south']['plantings'][0]['plant_out'] == ['March', 'April'])
    check('cherry-sour -> marginal, both zones',
          all(cell(aa, 'cherry-sour', z)['suitability'] == 'marginal' for z in ('7', '8')))

    # the fabricated attribution must be gone from BOTH registers
    sweet = cell(aa, 'cherry-sweet', '8')
    check('fabricated UAEX sour-cherry steer removed (both registers)',
          'steers zone 8 growers toward sour cherry' not in sweet['suitability_note_seasoned']
          and 'points zone 8 growers toward pie' not in sweet['suitability_note_beginner'])

    # mid_atlantic must be untouched -- its calls are correctly sourced to NC State
    ma_same = all(
        json.dumps(bb[s]['regions']['mid_atlantic'], sort_keys=True)
        == json.dumps(aa[s]['regions']['mid_atlantic'], sort_keys=True)
        for s in ('blueberry', 'cherry-sour', 'cherry-sweet', 'fig', 'raspberry'))
    check('mid_atlantic completely untouched', ma_same)

    # every other region of the 5 crops untouched
    other_same = True
    for s in ('blueberry', 'cherry-sour', 'cherry-sweet', 'fig', 'raspberry'):
        for rid in bb[s].get('regions', {}):
            if rid == 'mid_south':
                continue
            if bb[s]['regions'][rid] != aa[s]['regions'][rid]:
                other_same = False
    check('no region but mid_south touched', other_same)

    # calendars frozen
    cal_same = all(
        cell(bb, s, z).get('calendar') == cell(aa, s, z).get('calendar')
        for s in ('blueberry', 'cherry-sour', 'cherry-sweet', 'fig', 'raspberry')
        for z in ('7', '8'))
    check('calendars unchanged', cal_same)

    # findings resolved
    resolved = 0
    for s, fid in (('blueberry', 'mid_south_blueberry_recommended_type_inverted'),
                   ('fig', 'mid_south_fig_dormant_planting_contradicted'),
                   ('raspberry', 'mid_south_raspberry_dormant_planting_contradicted'),
                   ('cherry-sour', 'mid_south_cherry_sour_suitability_ruling_needed')):
        for f in aa[s]['verification_status']['open_findings']:
            if f.get('id') == fid and f.get('status') == 'resolved' and f.get('resolution'):
                resolved += 1
    check('all 4 findings resolved with a resolution', resolved == 4)

    # 9. re-apply refused
    rc, out = _run(path, hashlib.sha256(raw_after).hexdigest(), apply_=True)
    check('re-apply refused', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'guard checks failed: %s' % [r[0] for r in failed]


if __name__ == '__main__':
    test_guards()
