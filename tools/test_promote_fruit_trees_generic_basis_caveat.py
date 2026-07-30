#!/usr/bin/env python3
"""Adversarially test the guards on promote_fruit_trees_generic_basis_caveat.py.

Small promote, so a focused suite -- but the load-bearing guard is real: the finding asserts
these crops CITE uada_ext_fruit_trees, so if that citation is ever removed or reverted the
finding would misdescribe the data and must not be written.

Skip guard is in the TEST BODY so pytest sees it.

    $ python3 -m pytest tools/test_promote_fruit_trees_generic_basis_caveat.py -q
    $ python3 tools/test_promote_fruit_trees_generic_basis_caveat.py
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
SCRIPT = os.path.join(REPO, 'tools', 'promote_fruit_trees_generic_basis_caveat.py')
BASE_SHA = '7ca9e487df51e9d6cd2882c7305c12f536b3733154ac5298bdbd4c0fb079bbe9'
FID = 'mid_south_fruit_trees_citation_generic_basis'


def _is_base():
    if not os.path.exists(CANON):
        return False
    with open(CANON, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest() == BASE_SHA


def _scratch(mutate=None):
    tmp = tempfile.mkdtemp(prefix='ftcav_')
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
    check('clean dry-run succeeds', rc == 0 and 'all 3 crops' in out)

    rc, out = _run(path, '0' * 64)
    check('SHA drift aborts', rc == 2 and 'drifted' in out)

    # THE load-bearing guard: the citation the finding describes must be present
    def unrepoint(crops, _d):
        for z, cell in crops['mulberry']['regions']['mid_south']['resolved_by_zone'].items():
            cell['anchoring_urls'].pop('uada_ext_fruit_trees', None)
    path, sha = _scratch(unrepoint)
    rc, out = _run(path, sha)
    check('citation absent -> abort', rc == 2 and 'does not cite' in out)

    def preadd(crops, _d):
        crops['apricot']['verification_status']['open_findings'].append(
            {'id': FID, 'status': 'accepted_modeled', 'blocks_launch': False, 'summary': 'x'})
    path, sha = _scratch(preadd)
    rc, out = _run(path, sha)
    check('duplicate finding -> abort', rc == 2 and 'already present' in out)

    def drop(_crops, data):
        data['crops'] = [c for c in data['crops'] if c['slug'] != 'mulberry']
    path, sha = _scratch(drop)
    rc, out = _run(path, sha)
    check('missing crop -> abort', rc == 2 and 'absent' in out)

    # apply and verify the footprint
    path, sha = _scratch()
    before = json.loads(open(path).read())
    rc, out = _run(path, sha, apply_=True)
    raw_after = open(path, 'rb').read()
    after = json.loads(raw_after)
    check('apply succeeds', rc == 0 and 'APPLIED: 3 findings' in out)
    check('no trailing newline', not raw_after.endswith(b'\n'))

    bb = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in after['crops']}
    check('exactly the 3 crops changed',
          sorted(s for s in bb if bb[s] != aa[s]) == ['apricot', 'mulberry', 'pomegranate'])

    def strip(d):
        c = json.loads(json.dumps(d))
        for crop in c['crops']:
            (crop.get('verification_status') or {}).pop('open_findings', None)
        return c
    check('zero value changes outside open_findings', strip(before) == strip(after))
    check('each crop got exactly one new finding',
          all(len(aa[s]['verification_status']['open_findings'])
              == len(bb[s]['verification_status']['open_findings']) + 1
              for s in ('apricot', 'mulberry', 'pomegranate')))

    rc, out = _run(path, hashlib.sha256(raw_after).hexdigest(), apply_=True)
    check('re-apply refused', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


if __name__ == '__main__':
    test_guards()
