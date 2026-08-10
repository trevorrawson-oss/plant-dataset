"""Adversarial guards for promote_tomato_fertilizer_cadence.py.

A cadence change on five certified crops that drives an APP NOTIFICATION, so the guards that
matter are the ones proving nothing else moved and that the new stage the reminder points at
actually exists on every crop. Fixture is rebuilt from the pinned pre-state, never copied from
live canonical, so these keep testing after the promote is applied.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SCRIPT = os.path.join(HERE, 'promote_tomato_fertilizer_cadence.py')

import promote_fixture as F           # noqa: E402
import promote_tomato_fertilizer_cadence as P  # noqa: E402

results = []


def check(name, ok, detail=''):
    results.append((name, ok))
    print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))


def run(path, sha, apply_=False):
    p = subprocess.run([sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
                        '--canonical', path, '--expect-sha', sha],
                       capture_output=True, text=True, cwd=ROOT)
    return p.returncode, p.stdout + p.stderr


def fert(data, slug):
    return next(c for c in data['crops'] if c['slug'] == slug)['fertilizer']


def main():
    path, sha = F.scratch(P.BASE_SHA)
    check('fixture is the pinned pre-state', sha == P.BASE_SHA, sha[:16])
    pre = json.load(open(path, encoding='utf-8'))
    check('fixture really carries the OLD cadence',
          all(fert(pre, s)['frequency'] == 'every 2 weeks' for s in P.SLUGS))

    rc, out = run(path, sha)
    check('clean dry-run succeeds', rc == 0, out[-300:])
    check('asserts the stage it points at exists', 'stage we point at' in out)

    rc, out = run(path, '0' * 64)
    check('SHA drift aborts', rc == 2 and 'drifted' in out)

    rc, out = run(path, sha, apply_=True)
    check('apply succeeds', rc == 0, out[-300:])
    post = json.load(open(path, encoding='utf-8'))

    for s in P.SLUGS:
        f = fert(post, s)
        check('%s cadence is Clemson\'s' % s, f['frequency'] == 'every 3 to 4 weeks')
        check('%s reminder no longer fires at 14 days' % s, f['notify_days_after'] == 21)
        check('%s points at an EXISTING stage' % s,
              f['stage_id'] in {g.get('id') for g in
                                next(c for c in post['crops'] if c['slug'] == s)['growth_stages']})
        check('%s UGA attribution dropped' % s, 'UGA' not in f['amount_seasoned'])
        check('%s prose no longer uses the first-fruit trigger' % s,
              'size of a quarter' not in f['amount_seasoned'])
        check('%s keeps the high-potassium switch at flowering' % s,
              'flower' in f['notify_message_beginner'].lower())
        check('%s rate survived (this promote changes timing, not the rate)' % s,
              '1 pound of 10-10-10' in f['amount_seasoned'])

    # no collateral
    bb = {c['slug']: c for c in pre['crops']}
    aa = {c['slug']: c for c in post['crops']}
    # key-set first: iterating bb alone cannot see a crop APPENDED by the promote (PLA-162)
    check('no crop appeared or vanished', set(bb) == set(aa), str(sorted(set(bb) ^ set(aa))))
    check('exactly the 5 tomatoes changed',
          sorted(s for s in bb if bb[s] != aa[s]) == sorted(P.SLUGS))
    check('no other tomato field moved',
          all(sorted(k for k in set(bb[s]) | set(aa[s]) if bb[s].get(k) != aa[s].get(k))
              == ['fertilizer'] for s in P.SLUGS))
    check('citations frozen',
          all(json.dumps({k: fert(pre, s).get(k) for k in ('sources', 'anchoring_urls')},
                         sort_keys=True) ==
              json.dumps({k: fert(post, s).get(k) for k in ('sources', 'anchoring_urls')},
                         sort_keys=True) for s in P.SLUGS))
    check('npk_ratio untouched (the NPK wording defect is a SEPARATE promote)',
          all(fert(pre, s).get('npk_ratio') == fert(post, s).get('npk_ratio') for s in P.SLUGS))

    raw = open(path, 'rb').read()
    check('COMPACT preserved', b'": ' not in raw[:200000])
    check('no trailing newline', not raw.endswith(b'\n'))
    check('no em dash in the rewritten copy',
          all(chr(8212) not in fert(post, s)[k] and '--' not in fert(post, s)[k]
              for s in P.SLUGS
              for k in ('amount_beginner', 'amount_seasoned', 'notify_message_beginner',
                        'notify_message_seasoned', 'timing', 'frequency')))

    rc, _ = run(path, hashlib.sha256(raw).hexdigest(), apply_=True)
    check('re-apply refused', rc == 2)

    # a crop missing the target stage must abort rather than point the app at nothing
    def drop_stage(crops, _d):
        crops['roma-tomato']['growth_stages'] = [
            g for g in crops['roma-tomato']['growth_stages'] if g.get('id') != 'established']

    p2, s2 = F.scratch(P.BASE_SHA, drop_stage)
    rc, out = run(p2, s2, apply_=True)
    check('aborts if a crop lacks the stage the reminder would point at',
          rc == 2 and 'growth stage' in out, out[-200:])

    # prior value drift
    def drift(crops, _d):
        crops['grape-tomato']['fertilizer']['frequency'] = 'every 3 to 4 weeks'

    p3, s3 = F.scratch(P.BASE_SHA, drift)
    rc, _ = run(p3, s3, apply_=True)
    check('already-corrected input aborts', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


def test_guards():
    main()


if __name__ == '__main__':
    main()
