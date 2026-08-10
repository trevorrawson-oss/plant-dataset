"""Adversarial guard tests for promote_apple_mid_atlantic_bloom_reason.py.

The promote reworks the STATED REASON of apple's `mid_atlantic_bloom_offset_undocumented`
finding and keeps its conclusion (Trevor-ruled 2026-07-30). It is documentation-only: no
value, date, calendar or citation may move, and the nine sibling crops carrying the same
finding must come through byte-for-byte.

Every test drives the real script against a SCRATCH copy. The defect classes injected are
the ones that would actually do damage:

  * canonical drifting under the pinned SHA
  * the prior text not being what we think it is (someone else already edited it)
  * the blast radius exceeding one crop / one finding / two keys
  * a value field riding along with a documentation change
  * THE GUARD THAT MATTERS: writing a reason that names a document the arm does not cite.
    That is precisely the defect being corrected, and the script must refuse to reintroduce
    it -- so the test reverts apple's citation to the handbook and demands an abort.
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
SCRIPT = os.path.join(HERE, 'promote_apple_mid_atlantic_bloom_reason.py')
FINDING_ID = 'mid_atlantic_bloom_offset_undocumented'

import promote_apple_mid_atlantic_bloom_reason as P  # noqa: E402

# The fixture is SYNTHESIZED, never "whatever canonical happens to be". Once the promote has
# been applied, a fixture copied straight from canonical no longer carries the prior text and
# every happy-path guard would silently stop testing anything. The sibling cherry-sour suite
# guards that with `if not _is_base(): return`, which passes vacuously the moment canonical
# moves on. Rebuilding the pre-state keeps these guards live forever instead.
ALL_TEN = ('apple',) + P.SIBLINGS

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
    """Rebuild the exact pre-promote state, whatever canonical currently holds."""
    data = load(CANON)
    for slug in ALL_TEN:
        crop = next(c for c in data['crops'] if c['slug'] == slug)
        f = next(x for x in crop['verification_status']['open_findings']
                 if x.get('id') == FINDING_ID)
        f['summary'] = P.PRIOR_SUMMARY
        f['basis'] = P.PRIOR_BASIS
    if mutate is not None:
        mutate(data)
    return data, write_compact(scratch, data)


def main(tmp):
    scratch = os.path.join(tmp, 'scratch.json')

    # ---- 0. the fixture itself must really be the pre-state -----------------
    pre, base = make_pre_state(scratch)
    check('synthesized fixture carries the prior text on all ten crops',
          all(finding_of(pre, s)['summary'] == P.PRIOR_SUMMARY for s in ALL_TEN))

    # ---- 1. happy path ------------------------------------------------------
    r = run(scratch, base, '--apply')
    check('applies cleanly against a pinned, undrifted copy', r.returncode == 0,
          r.stdout[-400:] + r.stderr[-400:])
    after = load(scratch)
    before = pre

    new = finding_of(after, 'apple')
    old = finding_of(before, 'apple')
    check('the finding still exists (reworded, not deleted)', new is not None)
    check('conclusion preserved: status still accepted_modeled',
          new['status'] == 'accepted_modeled', new.get('status'))
    check('id unchanged', new['id'] == FINDING_ID)
    check('severity and blocks_launch unchanged',
          new['severity'] == old['severity'] and new['blocks_launch'] == old['blocks_launch'])
    check('the summary actually changed', new['summary'] != old['summary'])
    check('new reason names the document the arm really cites',
          'ext_org_apples' in new['summary'])
    check('new reason does NOT repeat the falsified absence claim',
          'publishes NO bloom date for any fruit crop' not in new['summary'])
    check('new reason carries the geography argument',
          'estern' in new['summary'] and 'Piedmont' in new['summary'])

    # blast radius
    bb = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in after['crops']}
    # key-set first: iterating bb alone cannot see a crop APPENDED by the promote (PLA-162)
    check('no crop appeared or vanished', set(bb) == set(aa), str(sorted(set(bb) ^ set(aa))))
    changed = sorted(s for s in bb if bb[s] != aa[s])
    check('exactly one crop changed', changed == ['apple'], changed)
    siblings = ['fig', 'mulberry', 'nectarine', 'pawpaw', 'peach',
                'pear-asian', 'pear-european', 'persimmon', 'plum']
    untouched = [s for s in siblings
                 if json.dumps(finding_of(before, s), sort_keys=True) ==
                 json.dumps(finding_of(after, s), sort_keys=True)]
    check('all 9 sibling findings byte-for-byte unchanged',
          len(untouched) == 9, sorted(set(siblings) - set(untouched)))

    ap_b, ap_a = bb['apple'], aa['apple']
    diffkeys = [k for k in ap_b if ap_b[k] != ap_a.get(k)]
    check('only verification_status changed on apple', diffkeys == ['verification_status'], diffkeys)
    check('apple regions untouched (no value, date or citation moved)',
          ap_b['regions'] == ap_a['regions'])
    fb, fa = finding_of(before, 'apple'), finding_of(after, 'apple')
    check('exactly two keys changed in the finding',
          sorted(k for k in set(fb) | set(fa) if fb.get(k) != fa.get(k)) == ['basis', 'summary'],
          sorted(k for k in set(fb) | set(fa) if fb.get(k) != fa.get(k)))

    # compactness
    raw = open(scratch, 'rb').read()
    check('output stays COMPACT', b', "' not in raw[:200000] and b'": ' not in raw[:200000])
    check('no trailing newline', not raw.endswith(b'\n'))

    # ---- 2. rerun must refuse (not silently double-apply) -------------------
    r2 = run(scratch, sha_of(scratch), '--apply')
    check('refuses to re-apply an already-corrected finding', r2.returncode != 0,
          r2.stdout[-300:])

    # ---- 3. drifted canonical -> abort --------------------------------------
    _, s3 = make_pre_state(scratch)
    r3 = run(scratch, 'deadbeef' * 8, '--apply')
    check('aborts when the pinned SHA does not match', r3.returncode != 0)
    check('drifted run wrote nothing', sha_of(scratch) == s3)

    # ---- 4. prior text is not what we expect -> abort -----------------------
    def scramble(d):
        finding_of(d, 'apple')['summary'] = 'someone else already rewrote this'

    _, s4 = make_pre_state(scratch, scramble)
    r4 = run(scratch, s4, '--apply')
    check('aborts when the prior summary is not the expected text', r4.returncode != 0,
          r4.stdout[-300:])

    # ---- 5. THE ONE THAT MATTERS -------------------------------------------
    # Revert apple's bloom citation to the handbook. The new reason names
    # ext_org_apples, so writing it would credit a document the arm does not cite --
    # the exact defect this promote exists to remove. It must refuse.
    def recite_handbook(d):
        apple = next(c for c in d['crops'] if c['slug'] == 'apple')
        for p in apple['regions']['mid_atlantic']['plantings']:
            for arm in (p.get('bloom') or []):
                if isinstance(arm, dict):
                    arm['sources'] = ['ncsu_ext']
                    arm['anchoring_urls'] = {'ncsu_ext': {'url': 'https://content.ces.ncsu.edu',
                                                          'verified': '2026-06-10'}}

    _, s5 = make_pre_state(scratch, recite_handbook)
    r5 = run(scratch, s5, '--apply')
    check('REFUSES to name a document the bloom arm does not cite', r5.returncode != 0,
          r5.stdout[-300:])

    # ---- 6. dry-run writes nothing -----------------------------------------
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
