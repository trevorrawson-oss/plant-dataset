"""Adversarial guards for promote_zone_null_anchor_note.py.

A note-only rewrite, so the guards exist to prove it is note-only: no url appears, no source id
moves, no value changes, and the live `zones{}` subtree around these anchors is untouched.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SCRIPT = os.path.join(HERE, 'promote_zone_null_anchor_note.py')

import promote_fixture as F              # noqa: E402
import promote_zone_null_anchor_note as P  # noqa: E402

results = []


def check(name, ok, detail=''):
    results.append((name, ok))
    print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))


def run(path, sha, apply_=False):
    p = subprocess.run([sys.executable, SCRIPT, '--apply' if apply_ else '--dry-run',
                        '--canonical', path, '--expect-sha', sha],
                       capture_output=True, text=True, cwd=ROOT)
    return p.returncode, p.stdout + p.stderr


def nulls(path):
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    return [(c['slug'], sid, e) for c in data['crops'] for sid, e in P._null_anchors(c)]


def main():
    path, sha = F.scratch(P.BASE_SHA)
    check('fixture is the pinned pre-state', sha == P.BASE_SHA)
    pre = nulls(path)
    check('fixture has exactly 57 null anchors', len(pre) == 57, str(len(pre)))
    check('all carry the old to-do note', all(e.get('note') in P.OLD_NOTES for _s, _i, e in pre))

    rc, out = run(path, sha)
    check('clean dry-run succeeds', rc == 0, out[-300:])
    rc, _ = run(path, '0' * 64)
    check('SHA drift aborts', rc == 2)

    rc, out = run(path, sha, apply_=True)
    check('apply succeeds', rc == 0, out[-300:])
    post = nulls(path)

    check('still exactly 57 null anchors (none deleted)', len(post) == 57, str(len(post)))
    check('every one carries the new decision note',
          all(e.get('note') == P.NEW_NOTE for _s, _i, e in post))
    check('none gained a url', all(e.get('url') is None for _s, _i, e in post))
    check('none gained a verified value', all(e.get('verified') is None for _s, _i, e in post))
    check('the new note no longer reads as a pending task',
          'needs manual lookup' not in P.NEW_NOTE and 'not a pending task' in P.NEW_NOTE)

    # the source ids must survive -- deleting them was the option we rejected
    with open(path, encoding='utf-8') as fh:
        after = json.load(fh)
    prej = json.loads(F.pre_state(P.BASE_SHA))

    def ids(d):
        return sorted((c['slug'], sid) for c in d['crops'] for sid, _e in P._null_anchors(c))
    check('every null anchor source id survives', ids(prej) == ids(after))

    bb = {c['slug']: c for c in prej['crops']}
    aa = {c['slug']: c for c in after['crops']}
    # key-set first: iterating bb alone cannot see a crop APPENDED by the promote (PLA-162)
    check('no crop appeared or vanished', set(bb) == set(aa), str(sorted(set(bb) ^ set(aa))))
    changed = sorted(s for s in bb if bb[s] != aa[s])
    check('exactly the 4 tomatoes changed', len(changed) == 4, str(changed))
    check('only the zones subtree moved on those crops',
          all(sorted(k for k in set(bb[s]) | set(aa[s]) if bb[s].get(k) != aa[s].get(k)) == ['zones']
              for s in changed), str(changed))

    # the live planting data inside zones{} must be byte-identical.
    # anchoring_urls nest at every depth, so they have to be stripped RECURSIVELY --
    # comparing only the top level of each zone silently included the nested notes.
    def strip_anchors(node):
        if isinstance(node, dict):
            return {k: strip_anchors(v) for k, v in node.items() if k != 'anchoring_urls'}
        if isinstance(node, list):
            return [strip_anchors(v) for v in node]
        return node

    def planting(d, slug):
        z = {c['slug']: c for c in d['crops']}[slug].get('zones') or {}
        return json.dumps(strip_anchors(z), sort_keys=True)

    check('live zone planting data untouched (today.ts reads this)',
          all(planting(prej, s) == planting(after, s) for s in changed))

    with open(path, 'rb') as fh:
        raw = fh.read()
    check('COMPACT preserved', b'": ' not in raw[:200000])
    check('no trailing newline', not raw.endswith(b'\n'))

    rc, _ = run(path, hashlib.sha256(raw).hexdigest(), apply_=True)
    check('re-apply refused', rc == 2)

    def unexpected(crops, _d):
        crops['cherry-tomato']['zones']['3']['anchoring_urls']['made_up'] = {
            'url': None, 'verified': None, 'note': 'something else'}
    p2, s2 = F.scratch(P.BASE_SHA, unexpected)
    rc, out = run(p2, s2, apply_=True)
    check('aborts on an unexpected null anchor rather than rewriting it blind', rc == 2)

    failed = [r for r in results if not r[1]]
    print('\n%d/%d guard checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


def test_guards():
    main()


if __name__ == '__main__':
    main()
