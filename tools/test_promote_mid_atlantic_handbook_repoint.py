#!/usr/bin/env python3
"""Adversarially test the guards on promote_mid_atlantic_handbook_repoint.py.

The load-bearing guards, both of which encode a lesson this arc paid for:
  * refuse to cite the handbook if a cell's plant_out drifts off the Dec-Feb dormant window it
    actually backs (pointing a cell at a document that disagrees CREATES a visible defect);
  * refuse to repoint a bloom arm, because the handbook publishes no bloom dates and repointing
    cannot fix an absent quantity.

Skip guard is in the TEST BODY so pytest sees it.

    $ python3 -m pytest tools/test_promote_mid_atlantic_handbook_repoint.py -q
    $ python3 tools/test_promote_mid_atlantic_handbook_repoint.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promote_fixture as _fixture  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
SCRIPT = os.path.join(REPO, 'tools', 'promote_mid_atlantic_handbook_repoint.py')
BASE_SHA = 'eb5926edf5e1d75c56ef2f1469bfd1c5cd484c388cb94fc71eb18f9fa8669516'
NEW_ID = 'ncsu_ext_handbook_tree_fruit'
VEG = 'https://www.pubs.ext.vt.edu/426/426-331/426-331.html'




def _scratch(mutate=None):
    """The pinned PRE-promote state, rebuilt -- never a copy of live canonical.

    Copying canonical only worked while it still sat on BASE_SHA. Once it moved past, the old
    `if not _canonical_is_base(): return` skip made this whole suite pass while running ZERO
    checks. promote_fixture rebuilds the pinned state (from a commit, or by replaying the
    promote chain for hunt 1's never-committed intermediates) and hash-verifies it, so these
    guards keep testing forever and FAIL LOUDLY if the state cannot be rebuilt.
    """
    return _fixture.scratch(BASE_SHA, mutate)


def _run(path, sha, apply_=False):
    p = subprocess.run([sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
                        '--canonical', path, '--expect-sha', sha], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def test_guards():
    results = []

    def check(name, ok, detail=''):
        results.append((name, ok))
        print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))

    path, sha = _scratch()
    rc, out = _run(path, sha)
    check('clean dry-run succeeds', rc == 0)
    check('repoints exactly 54 nodes / 12 findings', 'repointed 54 nodes, 12 findings' in out)
    check('exactly the 10 intended crops', 'exactly the 10 intended crops' in out)
    check('asserts no bloom arm repointed', 'no bloom arm repointed' in out)

    rc, out = _run(path, '0' * 64)
    check('SHA drift aborts', rc == 2 and 'drifted' in out)

    # central guard: plant_out drifts off the window the handbook backs
    def move(crops, _d):
        crops['plum']['regions']['mid_atlantic']['resolved_by_zone']['7']['plant_out'] = \
            'Mar - Apr (spring)'
    path, sha = _scratch(move)
    rc, out = _run(path, sha)
    check('plant_out off the documented window -> abort',
          rc == 2 and 'late fall/early winter' in out)

    def preadd(_crops, data):
        data['source_catalog'][NEW_ID] = {'id': NEW_ID}
    path, sha = _scratch(preadd)
    rc, out = _run(path, sha)
    check('catalog id already present -> abort', rc == 2 and 'already holds' in out)

    def drop(_crops, data):
        data['crops'] = [c for c in data['crops'] if c['slug'] != 'plum']
    path, sha = _scratch(drop)
    rc, out = _run(path, sha)
    check('missing crop -> abort', rc == 2 and 'absent' in out)

    # apply and inspect
    path, sha = _scratch()
    before = json.loads(open(path).read())
    rc, out = _run(path, sha, apply_=True)
    raw_after = open(path, 'rb').read()
    after = json.loads(raw_after)
    check('apply succeeds', rc == 0 and '54 citations repointed' in out)
    check('no trailing newline', not raw_after.endswith(b'\n'))

    bb = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in after['crops']}

    def strip(d):
        c = json.loads(json.dumps(d))

        def walk(n):
            if isinstance(n, dict):
                n.pop('anchoring_urls', None)
                n.pop('sources', None)
                (n.get('verification_status') or {}).pop('open_findings', None)
                for v in n.values():
                    walk(v)
            elif isinstance(n, list):
                for v in n:
                    walk(v)
        walk(c['crops'])
        c.pop('source_catalog', None)
        return c
    check('zero value changes', strip(before) == strip(after))

    # the vegetable guide must be GONE from every repointed crop's mid_atlantic block
    veg_left = [s for s in ('apple', 'fig', 'peach', 'plum', 'persimmon', 'pawpaw')
                if VEG in json.dumps(aa[s]['regions']['mid_atlantic'])]
    check('vegetable guide gone from repointed crops', not veg_left, str(veg_left))

    # bloom arms must still NOT cite the handbook
    bloom_ok = True
    for s in ('fig', 'peach', 'plum', 'persimmon'):
        for arm in aa[s]['regions']['mid_atlantic'].get('plantings') or []:
            for b in arm.get('bloom') or []:
                if NEW_ID in (b.get('anchoring_urls') or {}):
                    bloom_ok = False
    check('bloom arms still not citing the handbook', bloom_ok)

    # excluded crops untouched -- handbook does not name them
    untouched = all(bb[s] == aa[s] for s in
                    ('apricot', 'cherry-sour', 'cherry-sweet', 'pomegranate'))
    check('apricot/cherries/pomegranate deliberately untouched', untouched)

    # mid_south must not be collateral
    ms_ok = all(json.dumps(bb[s].get('regions', {}).get('mid_south'), sort_keys=True)
                == json.dumps(aa[s].get('regions', {}).get('mid_south'), sort_keys=True)
                for s in ('apple', 'fig', 'peach', 'plum', 'mulberry'))
    check('mid_south untouched', ms_ok)

    # the two nuance findings landed on the right crops
    def fids(s):
        return [f.get('id') for f in aa[s]['verification_status']['open_findings']]
    check('nectarine divergence finding present',
          'mid_atlantic_nectarine_harvest_divergent' in fids('nectarine'))
    check('mulberry species-scope finding present',
          'mid_atlantic_mulberry_table_row_species_scoped' in fids('mulberry'))
    check('bloom finding on all 10',
          all('mid_atlantic_bloom_offset_undocumented' in fids(s) for s in
              ('apple', 'fig', 'mulberry', 'nectarine', 'pawpaw', 'peach',
               'pear-asian', 'pear-european', 'persimmon', 'plum')))

    rc, out = _run(path, hashlib.sha256(raw_after).hexdigest(), apply_=True)
    check('re-apply refused', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


if __name__ == '__main__':
    test_guards()
