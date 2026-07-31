"""Adversarial guards for promote_lettuce_verified_dates.py.

The risk in a "normalize the field" promote is that it becomes a rubber stamp: writing a date
that asserts a check nobody performed. So the guard that matters most is that the script refuses
to stamp a link whose url is not the one that was actually fetched.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SCRIPT = os.path.join(HERE, 'promote_lettuce_verified_dates.py')

import promote_fixture as F                # noqa: E402
import promote_lettuce_verified_dates as P  # noqa: E402

results = []


def check(name, ok, detail=''):
    results.append((name, ok))
    print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))


def run(path, sha, apply_=False):
    p = subprocess.run([sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
                        '--canonical', path, '--expect-sha', sha],
                       capture_output=True, text=True, cwd=ROOT)
    return p.returncode, p.stdout + p.stderr


def crop_of(path):
    with open(path, encoding='utf-8') as fh:
        return next(c for c in json.load(fh)['crops'] if c['slug'] == P.SLUG)


def bools(crop):
    return [(sub, i, sid) for sub in P.SUBTREES
            for i, item in enumerate(crop.get(sub) or []) if isinstance(item, dict)
            for sid, e in (item.get('anchoring_urls') or {}).items()
            if isinstance(e, dict) and isinstance(e.get('verified'), bool)]


def main():
    path, sha = F.scratch(P.BASE_SHA)
    check('fixture is the pinned pre-state', sha == P.BASE_SHA)
    pre = crop_of(path)
    check('fixture really has 11 boolean flags', len(bools(pre)) == 11, str(len(bools(pre))))

    rc, out = run(path, sha)
    check('clean dry-run succeeds', rc == 0, out[-300:])
    check('asserts the urls match what was fetched', 'actually fetched' in out)

    rc, _ = run(path, '0' * 64)
    check('SHA drift aborts', rc == 2)

    rc, out = run(path, sha, apply_=True)
    check('apply succeeds', rc == 0, out[-300:])
    post = crop_of(path)

    check('no boolean flags remain', bools(post) == [])
    stamped = [e.get('verified') for sub in P.SUBTREES for item in (post.get(sub) or [])
               if isinstance(item, dict)
               for e in (item.get('anchoring_urls') or {}).values()
               if isinstance(e, dict) and e.get('verified') == P.CHECK_DATE]
    check('exactly 11 carry the new date', len(stamped) == 11, str(len(stamped)))
    check('the date is a real ISO date, not a boolean',
          isinstance(stamped[0], str) and len(stamped[0]) == 10)

    # urls must be untouched
    def urlmap(c):
        return {(sub, i, sid): e.get('url') for sub in P.SUBTREES
                for i, item in enumerate(c.get(sub) or []) if isinstance(item, dict)
                for sid, e in (item.get('anchoring_urls') or {}).items() if isinstance(e, dict)}
    check('every url unchanged', urlmap(pre) == urlmap(post))

    with open(path, 'rb') as fh:
        raw = fh.read()
    check('COMPACT preserved', b'": ' not in raw[:200000])
    check('no trailing newline', not raw.endswith(b'\n'))

    rc, _ = run(path, hashlib.sha256(raw).hexdigest(), apply_=True)
    check('re-apply refused (no booleans left)', rc == 2)

    # THE ONE THAT MATTERS: a url that differs from what was checked must abort,
    # otherwise this promote becomes a rubber stamp for a verification never performed.
    def swap_url(crops, _d):
        au = crops[P.SLUG]['pests'][0]['anchoring_urls']
        au['clemson_hgic']['url'] = 'https://hgic.clemson.edu/factsheet/some-other-page/'

    p2, s2 = F.scratch(P.BASE_SHA, swap_url)
    rc, out = run(p2, s2, apply_=True)
    check('REFUSES to stamp a url that was not the one fetched',
          rc == 2 and 'what was checked' in out, out[-200:])

    # an unexpected extra boolean must abort rather than be stamped blind
    def add_bool(crops, _d):
        crops[P.SLUG]['pests'][0]['anchoring_urls']['made_up'] = {
            'url': 'https://example.invalid/x', 'verified': True}

    p3, s3 = F.scratch(P.BASE_SHA, add_bool)
    rc, out = run(p3, s3, apply_=True)
    check('aborts on an unexpected boolean rather than stamping it',
          rc == 2, out[-200:])

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


def test_guards():
    main()


if __name__ == '__main__':
    main()
