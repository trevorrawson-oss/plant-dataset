"""Adversarial guard tests for promote_pawpaw_mid_atlantic_bloom_reason.py.

Same shape as the apple promote, one crop later, and the difference is the point: apple's
conclusion survived on GEOGRAPHY (its source publishes bloom timing, for the wrong part of NC),
while pawpaw's survives on genuine ABSENCE (Penn State's pawpaw page is 15,361 characters, names
pawpaw 15 times, and mentions bloom zero times). Two crops, one wrong reason each, two different
correct reasons -- which is exactly why this is reworded per crop and never blanket-applied.

The fixture is SYNTHESIZED rather than copied from canonical, so these guards keep testing after
the promote has been applied.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
CANON = os.path.join(ROOT, 'crops_data_final.json')
SCRIPT = os.path.join(HERE, 'promote_pawpaw_mid_atlantic_bloom_reason.py')
FINDING_ID = 'mid_atlantic_bloom_offset_undocumented'

import promote_pawpaw_mid_atlantic_bloom_reason as P  # noqa: E402

results = []


def check(name, ok, detail=''):
    results.append((name, ok, detail))
    print('%s %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else '  <- ' + str(detail)))


def sha_of(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def write_compact(path, data):
    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    with open(path, 'wb') as fh:
        fh.write(out)
    return hashlib.sha256(out).hexdigest()


def run(scratch, sha, *extra):
    return subprocess.run(
        [sys.executable, SCRIPT, '--canonical', scratch, '--expect-sha', sha] + list(extra),
        capture_output=True, text=True, cwd=ROOT)


def load(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def finding_of(data, slug):
    crop = next(c for c in data['crops'] if c['slug'] == slug)
    return next(f for f in crop['verification_status']['open_findings']
                if f.get('id') == FINDING_ID)


def make_pre_state(scratch, mutate=None):
    """Rebuild the pre-promote state: pawpaw + the 8 handbook crops on the prior text."""
    data = load(CANON)
    for slug in ('pawpaw',) + P.SIBLINGS:
        f = finding_of(data, slug)
        f['summary'] = P.PRIOR_SUMMARY
        f['basis'] = P.PRIOR_BASIS
    if mutate is not None:
        mutate(data)
    return data, write_compact(scratch, data)


def main(tmp):
    scratch = os.path.join(tmp, 'scratch.json')

    pre, base = make_pre_state(scratch)
    check('fixture carries the prior text on pawpaw and all 8 handbook siblings',
          all(finding_of(pre, s)['summary'] == P.PRIOR_SUMMARY
              for s in ('pawpaw',) + P.SIBLINGS))

    r = run(scratch, base, '--apply')
    check('applies cleanly against a pinned, undrifted copy', r.returncode == 0,
          r.stdout[-500:] + r.stderr[-400:])
    after = load(scratch)

    new, old = finding_of(after, 'pawpaw'), finding_of(pre, 'pawpaw')
    check('finding still exists (reworded, not deleted)', new is not None)
    check('conclusion preserved: status still accepted_modeled',
          new['status'] == 'accepted_modeled', new.get('status'))
    check('id/severity/blocks_launch unchanged',
          new['id'] == FINDING_ID and new['severity'] == old['severity']
          and new['blocks_launch'] == old['blocks_launch'])
    check('summary actually changed', new['summary'] != old['summary'])
    check('new reason names the source the arm really cites', 'psu_ext' in new['summary'])
    # It may still NAME the handbook -- it has to, to say the old wording credited it wrongly.
    # What it must not do is keep ASSERTING the handbook as this cell's basis.
    check('new reason no longer asserts the handbook as the basis',
          'publishes NO bloom date for any fruit crop' not in new['summary'])
    check('new reason states the handbook is not what this arm cites',
          'does not cite the handbook' in new['summary'])
    check('new reason rests on ABSENCE, not apple\'s geography argument',
          'Piedmont' not in new['summary'])

    bb = {c['slug']: c for c in pre['crops']}
    aa = {c['slug']: c for c in after['crops']}
    # key-set first: iterating bb alone cannot see a crop APPENDED by the promote (PLA-162)
    check('no crop appeared or vanished', set(bb) == set(aa), str(sorted(set(bb) ^ set(aa))))
    changed = sorted(s for s in bb if bb[s] != aa[s])
    check('exactly one crop changed', changed == ['pawpaw'], changed)
    untouched = [s for s in P.SIBLINGS
                 if json.dumps(finding_of(pre, s), sort_keys=True) ==
                 json.dumps(finding_of(after, s), sort_keys=True)]
    check('all 8 handbook siblings byte-for-byte unchanged',
          len(untouched) == len(P.SIBLINGS), sorted(set(P.SIBLINGS) - set(untouched)))
    check('apple untouched (it was corrected in its own promote)',
          bb['apple'] == aa['apple'])

    pb, pa = bb['pawpaw'], aa['pawpaw']
    check('only verification_status changed on pawpaw',
          sorted(k for k in set(pb) | set(pa) if pb.get(k) != pa.get(k)) == ['verification_status'])
    check('pawpaw regions untouched (no value, date or citation moved)',
          pb['regions'] == pa['regions'])
    fb, fa = finding_of(pre, 'pawpaw'), finding_of(after, 'pawpaw')
    check('exactly two keys changed in the finding',
          sorted(k for k in set(fb) | set(fa) if fb.get(k) != fa.get(k)) == ['basis', 'summary'])

    raw = open(scratch, 'rb').read()
    check('output stays COMPACT', b'": ' not in raw[:200000])
    check('no trailing newline', not raw.endswith(b'\n'))

    r2 = run(scratch, sha_of(scratch), '--apply')
    check('refuses to re-apply an already-corrected finding', r2.returncode != 0)

    _, s3 = make_pre_state(scratch)
    r3 = run(scratch, 'deadbeef' * 8, '--apply')
    check('aborts when the pinned SHA does not match', r3.returncode != 0)
    check('drifted run wrote nothing', sha_of(scratch) == s3)

    def scramble(d):
        finding_of(d, 'pawpaw')['summary'] = 'someone else already rewrote this'

    _, s4 = make_pre_state(scratch, scramble)
    check('aborts when the prior summary is not the expected text',
          run(scratch, s4, '--apply').returncode != 0)

    # THE ONE THAT MATTERS, same guard as apple's: the reason may only name a source the arm
    # actually carries. Repoint pawpaw at the handbook and the new psu_ext reason must refuse.
    def recite_handbook(d):
        crop = next(c for c in d['crops'] if c['slug'] == 'pawpaw')
        for p in crop['regions']['mid_atlantic']['plantings']:
            for arm in (p.get('bloom') or []):
                if isinstance(arm, dict):
                    arm['sources'] = ['ncsu_ext']
                    arm['anchoring_urls'] = {'ncsu_ext': {'url': 'https://content.ces.ncsu.edu',
                                                          'verified': '2026-06-10'}}

    _, s5 = make_pre_state(scratch, recite_handbook)
    r5 = run(scratch, s5, '--apply')
    check('REFUSES to name a source the bloom arm does not cite', r5.returncode != 0,
          r5.stdout[-300:])

    _, s6 = make_pre_state(scratch)
    r6 = run(scratch, s6, '--dry-run')
    check('dry-run succeeds', r6.returncode == 0, r6.stdout[-300:])
    check('dry-run wrote nothing', sha_of(scratch) == s6)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


def test_promote_guards():
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        main(tmp)


if __name__ == '__main__':
    test_promote_guards()
