#!/usr/bin/env python3
"""Adversarially test the guards on promote_mid_south_fruit_tree_repoint.py.

Each guard is proven by injecting the defect class it exists to catch into a SCRATCH COPY.
The two that matter most are the ones protecting against the arc's own named failure mode --
pointing a cell at a document that contradicts it:

  * if a repointed crop's plant_out drifts off the Dec-Feb dormant window the document backs,
    the promote must refuse rather than cite the page for a claim it no longer makes;
  * if pawpaw/persimmon harvest moves outside the page's stated ripening span, same.

Runs under pytest AND as a script; the skip guard is in the TEST BODY so pytest sees it.

    $ python3 -m pytest tools/test_promote_mid_south_fruit_tree_repoint.py -q
    $ python3 tools/test_promote_mid_south_fruit_tree_repoint.py
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
SCRIPT = os.path.join(REPO, 'tools', 'promote_mid_south_fruit_tree_repoint.py')
BASE_SHA = '14c8eab246859c63a3fc9bf68c8f8fcef9ee39f360661589d26245f5924504c3'

BARE = 'https://www.uaex.uada.edu'
NEW_URL = 'https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx'


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
    tmp = tempfile.mkdtemp(prefix='msrepoint_')
    path = os.path.join(tmp, 'crops.json')
    shutil.copy2(CANON, path)
    with open(path, 'rb') as fh:
        raw = fh.read()
    if mutate is None:
        return path, hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    mutate({c['slug']: c for c in data['crops']}, data)
    return path, _write(path, data)


def test_guards():
    if not _canonical_is_base():
        print('SKIP: canonical is not the pinned base SHA')
        return
    results = []

    def check(name, ok, detail=''):
        results.append((name, ok, detail))
        print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))

    # 1. clean dry-run, exactly 40 nodes
    path, sha = _scratch()
    rc, out = _run(path, sha)
    check('clean dry-run succeeds', rc == 0)
    check('repoints exactly 40 nodes', 'repointed 40 nodes' in out)

    # 2. SHA drift
    path, sha = _scratch()
    rc, out = _run(path, '0' * 64)
    check('SHA drift aborts', rc == 2 and 'drifted' in out)

    # 3. THE CENTRAL GUARD: a repointed crop's plant_out drifts off the documented window.
    #    Citing the page anyway would be the unr_fs0261 defect this whole arc exists to stop.
    def move_plum(crops, _d):
        crops['plum']['regions']['mid_south']['resolved_by_zone']['7']['plant_out'] = \
            'Mar - Apr (spring)'
    path, sha = _scratch(move_plum)
    rc, out = _run(path, sha)
    check('plant_out off the documented window -> abort',
          rc == 2 and 'backs a Dec-Feb dormant window' in out)

    # 4. pawpaw harvest drifts outside the page's mid-Aug..Oct ripening span
    def move_pawpaw(crops, _d):
        crops['pawpaw']['regions']['mid_south']['resolved_by_zone']['7']['harvest_start'] = 'Jul 1'
    path, sha = _scratch(move_pawpaw)
    rc, out = _run(path, sha)
    check('pawpaw harvest moved -> abort', rc == 2 and 'harvest moved' in out)

    # 5. persimmon harvest drift
    def move_persimmon(crops, _d):
        crops['persimmon']['regions']['mid_south']['resolved_by_zone']['8']['harvest_end'] = 'Dec 25'
    path, sha = _scratch(move_persimmon)
    rc, out = _run(path, sha)
    check('persimmon harvest moved -> abort', rc == 2 and 'harvest moved' in out)

    # 6. catalog id already present -> abort (idempotency)
    def preadd_cat(_crops, data):
        data['source_catalog']['uada_ext_fruit_trees'] = {'id': 'uada_ext_fruit_trees'}
    path, sha = _scratch(preadd_cat)
    rc, out = _run(path, sha)
    check('catalog id already present -> abort', rc == 2 and 'already holds' in out)

    # 7. a node already repointed -> count falls short -> abort
    def prerepoint(crops, _d):
        cell = crops['plum']['regions']['mid_south']['resolved_by_zone']['7']
        cell['anchoring_urls'] = {'uada_ext_fruit_trees': {'url': NEW_URL, 'verified': 'x'}}
    path, sha = _scratch(prerepoint)
    rc, out = _run(path, sha)
    check('partially-repointed input -> abort on count', rc == 2 and 'expected exactly 40' in out)

    # 8. an unexpected zone appears -> abort
    def add_zone(crops, _d):
        rbz = crops['peach']['regions']['mid_south']['resolved_by_zone']
        rbz['9'] = json.loads(json.dumps(rbz['8']))
    path, sha = _scratch(add_zone)
    rc, out = _run(path, sha)
    check('unexpected zone -> abort', rc == 2 and 'expected 7+8' in out)

    # 9. missing crop
    def drop(_crops, data):
        data['crops'] = [c for c in data['crops'] if c['slug'] != 'plum']
    path, sha = _scratch(drop)
    rc, out = _run(path, sha)
    check('missing crop -> abort', rc == 2 and 'absent' in out)

    # 10. APPLY on scratch: values untouched, excluded crops untouched, compact held
    path, sha = _scratch()
    with open(path, 'rb') as fh:
        before = json.loads(fh.read())
    rc, out = _run(path, sha, apply_=True)
    with open(path, 'rb') as fh:
        raw_after = fh.read()
    after = json.loads(raw_after)
    check('apply succeeds', rc == 0 and '40 citations repointed' in out)
    check('no trailing newline', not raw_after.endswith(b'\n'))

    def strip_cites(d):
        c = json.loads(json.dumps(d))

        def walk(n):
            if isinstance(n, dict):
                n.pop('anchoring_urls', None)
                n.pop('sources', None)
                for v in n.values():
                    walk(v)
            elif isinstance(n, list):
                for v in n:
                    walk(v)
        walk(c['crops'])
        c.pop('source_catalog', None)
        return c
    check('zero value changes outside citations', strip_cites(before) == strip_cites(after))

    aa = {c['slug']: c for c in after['crops']}
    # the excluded crops must still carry the bare host -- proving we did NOT mass-repoint
    for slug in ('fig', 'raspberry', 'blueberry'):
        ms = aa[slug]['regions']['mid_south']
        blob = json.dumps(ms)
        check('%s still bare (deliberately not repointed)' % slug,
              '"%s"' % BARE in blob and 'uada_ext_fruit_trees' not in blob)

    # pawpaw plant_out must NOT have been repointed (container claim, undocumented)
    pw = aa['pawpaw']['regions']['mid_south']['plantings'][0]['plant_out'][0]
    check('pawpaw plant_out left bare', 'uada_ext' in (pw.get('anchoring_urls') or {}))
    # ...while pawpaw harvest WAS
    ph = aa['pawpaw']['regions']['mid_south']['plantings'][0]['harvest_start'][0]
    check('pawpaw harvest repointed', 'uada_ext_fruit_trees' in (ph.get('anchoring_urls') or {}))

    # bloom arms must remain bare on every tree fruit (no UAEX bloom dates exist)
    bloom_bare = True
    for slug in ('apricot', 'peach', 'plum', 'persimmon'):
        for arm in aa[slug]['regions']['mid_south']['plantings']:
            for b in arm.get('bloom') or []:
                if 'uada_ext_fruit_trees' in (b.get('anchoring_urls') or {}):
                    bloom_bare = False
    check('bloom arms untouched', bloom_bare)

    check('catalog gained exactly 1 entry',
          set(after['source_catalog']) - set(before['source_catalog']) == {'uada_ext_fruit_trees'})

    # 11. re-apply refused
    sha2 = hashlib.sha256(raw_after).hexdigest()
    rc, out = _run(path, sha2, apply_=True)
    check('re-apply refused', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'guard checks failed: %s' % [r[0] for r in failed]


if __name__ == '__main__':
    test_guards()
