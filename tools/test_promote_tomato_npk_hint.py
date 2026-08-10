"""Adversarial guards for promote_tomato_npk_hint.py.

The failure mode for a "fix the wording" promote is that it makes the text self-consistent while
leaving the claim wrong. Here the claim WAS the problem: neither cited source recommends high
potassium, and UMN explicitly advises a low- or no-phosphorus feed while we pointed readers at
8-32-16. So the guards check the CONTENT of the replacement, not just that it changed.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SCRIPT = os.path.join(HERE, 'promote_tomato_npk_hint.py')

import promote_fixture as F        # noqa: E402
import promote_tomato_npk_hint as P  # noqa: E402

results = []


def check(name, ok, detail=''):
    results.append((name, ok))
    print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))


def run(path, sha, apply_=False):
    p = subprocess.run([sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
                        '--canonical', path, '--expect-sha', sha],
                       capture_output=True, text=True, cwd=ROOT)
    return p.returncode, p.stdout + p.stderr


def fert(path, slug):
    with open(path, encoding='utf-8') as fh:
        return next(c for c in json.load(fh)['crops'] if c['slug'] == slug)['fertilizer']


def main():
    path, sha = F.scratch(P.BASE_SHA)
    check('fixture is the pinned pre-state', sha == P.BASE_SHA)
    check('fixture still carries 8-32-16 on the trio',
          all('8-32-16' in fert(path, s)['npk_hint_beginner'] for s in P.TRIO))
    check('fixture carries the subtler tied-number claim on the pair',
          all('higher third number' in fert(path, s)['npk_hint_beginner'] for s in P.PAIR))

    rc, out = run(path, sha)
    check('clean dry-run succeeds', rc == 0, out[-300:])

    rc, _ = run(path, '0' * 64)
    check('SHA drift aborts', rc == 2)

    rc, out = run(path, sha, apply_=True)
    check('apply succeeds', rc == 0, out[-300:])

    for s in P.SLUGS:
        f = fert(path, s)
        b, sz = f['npk_hint_beginner'], f['npk_hint_seasoned']
        check('%s no longer recommends 8-32-16' % s, '8-32-16' not in b and '8-32-16' not in sz)
        check('%s no longer claims the third number should be highest' % s,
              not ('third number' in b and 'highest' in b))
        check('%s no longer asserts high potassium as the rule' % s,
              'high-potassium formula' not in b and not sz.lower().startswith('high k'))
        check('%s leads with the soil test, which is what both sources say' % s,
              'soil test' in b.lower() and 'soil test' in sz.lower())
        check('%s keeps the SOURCED nitrogen warning' % s,
              'nitrogen' in b.lower() and 'nitrogen' in sz.lower())
        check('%s carries UMN\'s low-or-no-phosphorus guidance' % s,
              'phosphorus' in sz.lower())
        check('%s npk_ratio untouched (value change is a separate promote)' % s,
              f.get('npk_ratio') == '5-10-10', str(f.get('npk_ratio')))
        check('%s no em dash in consumer copy' % s,
              chr(8212) not in b and '--' not in b and chr(8212) not in sz and '--' not in sz)

    # collateral
    with open(path, encoding='utf-8') as fh:
        post = json.load(fh)
    pre = json.loads(F.pre_state(P.BASE_SHA))
    bb = {c['slug']: c for c in pre['crops']}
    aa = {c['slug']: c for c in post['crops']}
    # key-set first: iterating bb alone cannot see a crop APPENDED by the promote (PLA-162)
    check('no crop appeared or vanished', set(bb) == set(aa), str(sorted(set(bb) ^ set(aa))))
    check('exactly the 5 tomatoes changed',
          sorted(s for s in bb if bb[s] != aa[s]) == sorted(P.SLUGS))
    check('only the fertilizer subtree moved',
          all(sorted(k for k in set(bb[s]) | set(aa[s]) if bb[s].get(k) != aa[s].get(k))
              == ['fertilizer'] for s in P.SLUGS))
    check('cadence fields from the previous promote survived untouched',
          all(aa[s]['fertilizer']['frequency'] == 'every 3 to 4 weeks'
              and aa[s]['fertilizer']['notify_days_after'] == 21 for s in P.SLUGS))

    with open(path, 'rb') as fh:
        raw = fh.read()
    check('COMPACT preserved', b'": ' not in raw[:200000])
    check('no trailing newline', not raw.endswith(b'\n'))

    rc, _ = run(path, hashlib.sha256(raw).hexdigest(), apply_=True)
    check('re-apply refused', rc == 2)

    # a script that tried to keep 8-32-16 must be caught by its own content guard
    def already_fixed(crops, _d):
        crops['cherry-tomato']['fertilizer']['npk_hint_beginner'] = 'something else entirely'

    p2, s2 = F.scratch(P.BASE_SHA, already_fixed)
    rc, _ = run(p2, s2, apply_=True)
    check('drifted prior text aborts', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


def test_guards():
    main()


if __name__ == '__main__':
    main()
