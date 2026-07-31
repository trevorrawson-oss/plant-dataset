#!/usr/bin/env python3
"""Adversarially test the guards on promote_mid_south_corrected_repoint.py.

The guard that carries this promote is the one that refuses to attach a document to a cell that
has NOT been corrected -- these three cells were held back from the earlier repoint precisely
because their documents contradicted them, so a regression here would publish the contradiction
the whole arc exists to prevent. It is tested by reverting each correction in turn.

Runs under pytest AND as a script; the skip guard is in the TEST BODY.

    $ python3 -m pytest tools/test_promote_mid_south_corrected_repoint.py -q
    $ python3 tools/test_promote_mid_south_corrected_repoint.py
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
SCRIPT = os.path.join(REPO, 'tools', 'promote_mid_south_corrected_repoint.py')
BASE_SHA = 'd1b441c27f9d1cfe243977e794fc9207ed58361e87ea402af0a37e0845f0f65a'
BARE = 'https://www.uaex.uada.edu'




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
    """The pinned PRE-promote state, rebuilt -- never a copy of live canonical.

    Copying canonical only worked while it still sat on BASE_SHA. Once it moved past, the old
    `if not _canonical_is_base(): return` skip made this whole suite pass while running ZERO
    checks. promote_fixture rebuilds the pinned state (from a commit, or by replaying the
    promote chain for hunt 1's never-committed intermediates) and hash-verifies it, so these
    guards keep testing forever and FAIL LOUDLY if the state cannot be rebuilt.
    """
    return _fixture.scratch(BASE_SHA, mutate)


def _cell(crops, slug, z):
    return crops[slug]['regions']['mid_south']['resolved_by_zone'][z]


def test_guards():
    results = []

    def check(name, ok, detail=''):
        results.append((name, ok, detail))
        print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))

    path, sha = _scratch()
    rc, out = _run(path, sha)
    check('clean dry-run succeeds', rc == 0)
    check('repoints exactly 10 nodes', 'repointed 10 nodes' in out)

    path, sha = _scratch()
    rc, out = _run(path, '0' * 64)
    check('SHA drift aborts', rc == 2 and 'drifted' in out)

    # THE CENTRAL GUARD: revert each correction, confirm the repoint refuses.
    for slug, z, field, bad in (
            ('fig', '7', 'plant_out', 'Dec - Feb (dormant plant)'),
            ('raspberry', '8', 'plant_out', 'December to March'),
            ('blueberry', '7', 'plant_out', 'December to March')):
        def revert(crops, _d, s=slug, zz=z, f=field, b=bad):
            _cell(crops, s, zz)[f] = b
        path, sha = _scratch(revert)
        rc, out = _run(path, sha)
        check('%s reverted -> refuses to publish the contradiction' % slug,
              rc == 2 and 'would publish a contradiction' in out)

    # blueberry type reverted -> abort even though plant_out is fine
    def revert_type(crops, _d):
        _cell(crops, 'blueberry', '7')['recommended_type'] = 'rabbiteye'
    path, sha = _scratch(revert_type)
    rc, out = _run(path, sha)
    check('blueberry type reverted -> abort',
          rc == 2 and 'has not had its corrected type applied' in out)

    # catalog id already present
    def preadd(_crops, data):
        data['source_catalog']['uada_ext_fsa6104'] = {'id': 'uada_ext_fsa6104'}
    path, sha = _scratch(preadd)
    rc, out = _run(path, sha)
    check('catalog id already present -> abort', rc == 2 and 'already holds' in out)

    # the prerequisite promote never ran
    def drop_ft(_crops, data):
        data['source_catalog'].pop('uada_ext_fruit_trees', None)
    path, sha = _scratch(drop_ft)
    rc, out = _run(path, sha)
    check('missing prerequisite catalog id -> abort',
          rc == 2 and 'run the fruit-tree repoint first' in out)

    # partially repointed -> count guard
    def prerepoint(crops, _d):
        _cell(crops, 'fig', '7')['anchoring_urls'] = {
            'uada_ext_fruit_trees': {'url': 'x', 'verified': 'y'}}
    path, sha = _scratch(prerepoint)
    rc, out = _run(path, sha)
    check('partially repointed -> abort on count', rc == 2 and 'expected exactly 10' in out)

    # APPLY
    path, sha = _scratch()
    with open(path, 'rb') as fh:
        before = json.loads(fh.read())
    rc, out = _run(path, sha, apply_=True)
    with open(path, 'rb') as fh:
        raw_after = fh.read()
    after = json.loads(raw_after)
    check('apply succeeds', rc == 0 and '10 citations repointed' in out)
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
    for slug, want in (('fig', 'uada_ext_fruit_trees'), ('raspberry', 'uada_ext_fsa6107'),
                       ('blueberry', 'uada_ext_fsa6104')):
        check('%s now cites %s' % (slug, want),
              want in json.dumps(aa[slug]['regions']['mid_south']))

    def bare_nodes(slug):
        found = []

        def walk(n, path):
            if isinstance(n, dict):
                au = n.get('anchoring_urls')
                if isinstance(au, dict):
                    for k, v in au.items():
                        if isinstance(v, dict) and v.get('url') == BARE:
                            found.append(path)
                for k, v in n.items():
                    if k != 'anchoring_urls':
                        walk(v, path + '.' + k)
            elif isinstance(n, list):
                for i, v in enumerate(n):
                    walk(v, '%s[%d]' % (path, i))
        walk(aa[slug]['regions']['mid_south'], '')
        return sorted(found)

    # raspberry and blueberry clear completely; fig keeps EXACTLY the three arms whose claims no
    # UAEX document makes -- bloom (no bloom dates are published for any fruit crop) and fig
    # harvest (the fruit-trees page gives ripening spans for pawpaw and persimmon, not fig).
    check('raspberry fully cleared of bare hosts', bare_nodes('raspberry') == [], str(bare_nodes('raspberry')))
    check('blueberry fully cleared of bare hosts', bare_nodes('blueberry') == [], str(bare_nodes('blueberry')))
    check('fig keeps exactly its 3 undocumented arms bare',
          bare_nodes('fig') == ['.plantings[0].bloom[0]',
                                '.plantings[0].harvest_end[0]',
                                '.plantings[0].harvest_start[0]'],
          str(bare_nodes('fig')))

    check('catalog gained exactly the 2 new entries',
          set(after['source_catalog']) - set(before['source_catalog'])
          == {'uada_ext_fsa6107', 'uada_ext_fsa6104'})

    rc, out = _run(path, hashlib.sha256(raw_after).hexdigest(), apply_=True)
    check('re-apply refused', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'guard checks failed: %s' % [r[0] for r in failed]


if __name__ == '__main__':
    test_guards()
