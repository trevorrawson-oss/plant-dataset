#!/usr/bin/env python3
"""Adversarially test the guards on promote_mid_south_uada_citation_findings.py.

Every guard is proven by INJECTING the defect class it is supposed to catch into a SCRATCH COPY
and confirming the promote refuses. A guard that has never bounced anything is not a guard.

Runs under pytest AND as a script. The skip guard lives in the TEST BODY, not under
`if __name__ == "__main__"`, so pytest sees it too (the 456422c lesson).

    $ python3 -m pytest tools/test_promote_mid_south_uada_citation_findings.py -q
    $ python3 tools/test_promote_mid_south_uada_citation_findings.py
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
SCRIPT = os.path.join(REPO, 'tools', 'promote_mid_south_uada_citation_findings.py')
BASE_SHA = '13d42f95413034636325ff14abb5346d6e044f61ddf313948ff49cdfb82fcda7'




def _write(path, data):
    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    with open(path, 'wb') as fh:
        fh.write(out)
    return hashlib.sha256(out).hexdigest()


def _run(path, sha, apply_=False):
    cmd = [sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
           '--canonical', path, '--expect-sha', sha]
    p = subprocess.run(cmd, capture_output=True, text=True)
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


def _cell(crops, slug, zone):
    return crops[slug]['regions']['mid_south']['resolved_by_zone'][zone]


def test_guards():
    results = []

    def check(name, ok, detail=''):
        results.append((name, ok, detail))
        print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))

    # 1. clean dry-run succeeds and plans exactly 17 findings (4 adjudicated + 13 bloom)
    path, sha = _scratch()
    rc, out = _run(path, sha)
    check('clean dry-run succeeds', rc == 0, out.strip().splitlines()[-1] if out else '')
    check('plans exactly 17 findings', '17 findings planned' in out)

    # 2. SHA drift aborts
    path, sha = _scratch()
    rc, out = _run(path, '0' * 64)
    check('SHA drift aborts', rc == 2 and 'drifted' in out)

    # 3. blueberry no longer inverted -> abort (RE-VERIFY guard)
    def unfix_blueberry(crops, _d):
        _cell(crops, 'blueberry', '7')['recommended_type'] = 'northern_highbush'
    path, sha = _scratch(unfix_blueberry)
    rc, out = _run(path, sha)
    check('blueberry defect already fixed -> abort',
          rc == 2 and 'NO LONGER carries the defect' in out)

    # 4. fig plant_out already moved to spring -> abort
    def fix_fig(crops, _d):
        for z in ('7', '8'):
            _cell(crops, 'fig', z)['plant_out'] = 'Mar - Apr (early spring)'
    path, sha = _scratch(fix_fig)
    rc, out = _run(path, sha)
    check('fig already corrected -> abort', rc == 2 and 'NO LONGER carries the defect' in out)

    # 5. raspberry already corrected -> abort
    def fix_rasp(crops, _d):
        for z in ('7', '8'):
            _cell(crops, 'raspberry', z)['plant_out'] = 'March to April'
    path, sha = _scratch(fix_rasp)
    rc, out = _run(path, sha)
    check('raspberry already corrected -> abort', rc == 2 and 'NO LONGER carries the defect' in out)

    # 6. cherry-sour already ruled to marginal -> abort
    def rule_cherry(crops, _d):
        for z in ('7', '8'):
            _cell(crops, 'cherry-sour', z)['suitability'] = 'marginal'
    path, sha = _scratch(rule_cherry)
    rc, out = _run(path, sha)
    check('cherry-sour already ruled -> abort', rc == 2 and 'NO LONGER carries the defect' in out)

    # 7. a bloom arm already repointed -> abort (the finding would misdescribe it)
    def repoint_bloom(crops, _d):
        ms = crops['peach']['regions']['mid_south']
        for arm in ms['plantings']:
            for b in arm.get('bloom') or []:
                b['anchoring_urls'] = {'uada_ext_fsa6129': {
                    'url': 'https://www.uaex.uada.edu/publications/pdf/FSA-6129.pdf',
                    'verified': '2026-07-30'}}
    path, sha = _scratch(repoint_bloom)
    rc, out = _run(path, sha)
    check('bloom arm already repointed -> abort',
          rc == 2 and 'not a SOLE bare uada_ext host' in out)

    # 8. idempotency: finding already present -> abort
    def preadd(crops, _d):
        crops['fig']['verification_status']['open_findings'].append(
            {'id': 'mid_south_fig_dormant_planting_contradicted', 'status': 'open',
             'blocks_launch': False, 'summary': 'x'})
    path, sha = _scratch(preadd)
    rc, out = _run(path, sha)
    check('duplicate finding -> abort', rc == 2 and 'already present' in out)

    # 9. missing crop -> abort
    def drop_fig(_crops, data):
        data['crops'] = [c for c in data['crops'] if c['slug'] != 'fig']
    path, sha = _scratch(drop_fig)
    rc, out = _run(path, sha)
    check('missing crop -> abort', rc == 2 and 'absent' in out)

    # 10. APPLY on a scratch copy: exactly 17 findings land, zero values move, COMPACT held
    path, sha = _scratch()
    with open(path, 'rb') as fh:
        before = json.loads(fh.read())
    rc, out = _run(path, sha, apply_=True)
    with open(path, 'rb') as fh:
        raw_after = fh.read()
    after = json.loads(raw_after)
    check('apply succeeds', rc == 0 and 'APPLIED: 17 findings' in out)
    check('no trailing newline', not raw_after.endswith(b'\n'))
    check('compact separators', b'", "' not in raw_after[:200000])

    bb = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in after['crops']}
    added = {}
    for slug in bb:
        b_of = (bb[slug].get('verification_status') or {}).get('open_findings') or []
        a_of = (aa[slug].get('verification_status') or {}).get('open_findings') or []
        if len(a_of) != len(b_of):
            added[slug] = [f['id'] for f in a_of[len(b_of):]]
    # 17 findings land on 15 crops: fig and cherry-sour appear in BOTH groups
    # (their own contradiction/ruling finding AND the shared bloom finding).
    check('exactly 15 crops touched', len(added) == 15, str(sorted(added)))
    check('17 findings across 15 crops', sum(len(v) for v in added.values()) == 17)
    check('blueberry got the type finding',
          added.get('blueberry') == ['mid_south_blueberry_recommended_type_inverted'])
    check('fig got 2 findings (contradiction + bloom)', len(added.get('fig', [])) == 2)
    check('apple untouched', 'apple' not in added)
    check('strawberry untouched', 'strawberry' not in added)

    # prove values identical outside open_findings
    def strip(d):
        c = json.loads(json.dumps(d))
        for crop in c['crops']:
            (crop.get('verification_status') or {}).pop('open_findings', None)
        return c
    check('zero value changes outside open_findings', strip(before) == strip(after))

    # 11. re-running APPLY on the already-applied copy aborts (no double-append)
    sha2 = hashlib.sha256(raw_after).hexdigest()
    rc, out = _run(path, sha2, apply_=True)
    check('re-apply is refused', rc == 2 and 'already present' in out)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'guard checks failed: %s' % [r[0] for r in failed]


if __name__ == '__main__':
    test_guards()
