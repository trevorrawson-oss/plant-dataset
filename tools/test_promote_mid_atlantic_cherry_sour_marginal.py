#!/usr/bin/env python3
"""Adversarially test the guards on promote_mid_atlantic_cherry_sour_marginal.py.

A suitability downgrade on a certified crop, so the guards worth testing are the ones proving
NOTHING ELSE moved -- and the consistency guard, since the ruling's stated argument is that
apricot and cherry-sweet are already marginal in this region. If that stops being true, the
argument for this change no longer holds and the promote must refuse.

Skip guard is in the TEST BODY so pytest sees it.

    $ python3 -m pytest tools/test_promote_mid_atlantic_cherry_sour_marginal.py -q
    $ python3 tools/test_promote_mid_atlantic_cherry_sour_marginal.py
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
SCRIPT = os.path.join(REPO, 'tools', 'promote_mid_atlantic_cherry_sour_marginal.py')
BASE_SHA = '45409cee243da4196e983198c33505701d44f50842ffb208a224d0b22ddd817b'


def _is_base():
    if not os.path.exists(CANON):
        return False
    with open(CANON, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest() == BASE_SHA


def _scratch(mutate=None):
    tmp = tempfile.mkdtemp(prefix='chsour_')
    path = os.path.join(tmp, 'crops.json')
    shutil.copy2(CANON, path)
    raw = open(path, 'rb').read()
    if mutate is None:
        return path, hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    mutate({c['slug']: c for c in data['crops']}, data)
    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    open(path, 'wb').write(out)
    return path, hashlib.sha256(out).hexdigest()


def _run(path, sha, apply_=False):
    p = subprocess.run([sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
                        '--canonical', path, '--expect-sha', sha], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def _cell(crops, slug, z):
    return crops[slug]['regions']['mid_atlantic']['resolved_by_zone'][z]


def test_guards():
    if not _is_base():
        print('SKIP: canonical is not the pinned base SHA')
        return
    results = []

    def check(name, ok, detail=''):
        results.append((name, ok))
        print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))

    path, sha = _scratch()
    rc, out = _run(path, sha)
    check('clean dry-run succeeds', rc == 0)
    check('asserts siblings already marginal', 'already marginal here' in out)
    check('asserts no calendar/date/citation moved', 'no calendar, date or citation moved' in out)

    rc, out = _run(path, '0' * 64)
    check('SHA drift aborts', rc == 2 and 'drifted' in out)

    # the consistency argument is load-bearing: if a sibling stops being marginal, refuse
    def unmarginal(crops, _d):
        _cell(crops, 'cherry-sweet', '8')['suitability'] = 'fruits_reliably'
    path, sha = _scratch(unmarginal)
    rc, out = _run(path, sha)
    check('sibling no longer marginal -> abort',
          rc == 2 and 'consistency argument for this ruling no longer holds' in out)

    # prior value drifted
    def drift(crops, _d):
        _cell(crops, 'cherry-sour', '7')['suitability'] = 'marginal'
    path, sha = _scratch(drift)
    rc, out = _run(path, sha)
    check('already-ruled input -> abort', rc == 2)

    def drop(_crops, data):
        data['crops'] = [c for c in data['crops'] if c['slug'] != 'cherry-sour']
    path, sha = _scratch(drop)
    rc, out = _run(path, sha)
    check('missing crop -> abort', rc == 2 and 'absent' in out)

    # apply and inspect
    path, sha = _scratch()
    before = json.loads(open(path).read())
    rc, out = _run(path, sha, apply_=True)
    raw_after = open(path, 'rb').read()
    after = json.loads(raw_after)
    check('apply succeeds', rc == 0 and 'APPLIED: 6 edits' in out)
    check('no trailing newline', not raw_after.endswith(b'\n'))

    bb = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in after['crops']}
    check('exactly one crop changed', sorted(s for s in bb if bb[s] != aa[s]) == ['cherry-sour'])
    check('both zones now marginal',
          all(_cell(aa, 'cherry-sour', z)['suitability'] == 'marginal' for z in ('7', '8')))

    # mid_south must NOT be collateral -- it was ruled separately earlier the same day
    check('mid_south cherry-sour untouched',
          json.dumps(bb['cherry-sour']['regions']['mid_south'], sort_keys=True)
          == json.dumps(aa['cherry-sour']['regions']['mid_south'], sort_keys=True))

    # dates, calendars and citations frozen
    frozen = True
    for z in ('7', '8'):
        b, a = _cell(bb, 'cherry-sour', z), _cell(aa, 'cherry-sour', z)
        for k in ('plant_out', 'harvest', 'harvest_start', 'harvest_end', 'bloom',
                  'calendar', 'anchoring_urls', 'sources'):
            if b.get(k) != a.get(k):
                frozen = False
    check('dates, calendar and citations all frozen', frozen)

    # Trevor's framing: marginal must NOT read as discouragement
    for z in ('7', '8'):
        a = _cell(aa, 'cherry-sour', z)
        both = a['suitability_note_seasoned'] + ' ' + a['suitability_note_beginner']
        check('z%s note keeps the pro-fruiting characteristics' % z,
              'self fertile' in both and 'hardier' in both)
        check('z%s note is honest about the limit' % z,
              'not' in both.lower() and 'every year' in both.lower())

    check('no em dash in the new copy',
          all(chr(8212) not in _cell(aa, 'cherry-sour', z)[k] and '--' not in _cell(aa, 'cherry-sour', z)[k]
              for z in ('7', '8')
              for k in ('suitability_note_seasoned', 'suitability_note_beginner')))

    rc, out = _run(path, hashlib.sha256(raw_after).hexdigest(), apply_=True)
    check('re-apply refused', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


if __name__ == '__main__':
    test_guards()
