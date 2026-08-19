#!/usr/bin/env python3
"""Instrumented mutation harness for the PLA-161 suite's corrected pre/post wiring. PLA-215.

WHAT IS BEING VERIFIED. On 2026-08-19 the suite's `post` fixture was changed from LIVE canonical
to the promote's own output (`394bb8bd`, rebuilt and hash-verified). That change makes the
blast-radius guard durable -- but a change that makes a guard stop failing is exactly the change
most likely to make it stop TESTING, so it does not ship on the claim that it looks right.

Three things must hold, and each gets a defect sneaked at it:

  1. The blast-radius guard still CATCHES a stray edit (it did not go vacuous).
  2. The fixture pin still catches `post` being repointed at live canonical -- the precise
     regression this correction exists to prevent.
  3. The suite is GREEN while live canonical sits two promotes ahead of POST_SHA. That is the
     property the old wiring could not have, and it is asserted as the positive control rather
     than assumed.

Mutations are injected into a SCRATCH COPY of the suite, never the working file.

  MUTATION-APPLIED MARKER  every mutated copy carries the marker, asserted present in the file
                           about to execute and asserted to differ from the original. An anchor
                           that did not match is a HARD ERROR, never a survivor.
  SENTINEL                 one guaranteed-fatal mutation must redden, or the run exits HARNESS
                           DEAD and reports nothing else.
  POSITIVE CONTROL         the unmutated suite must stay green against a live canonical that has
                           MOVED, which is the whole point of the fix.

Run: python3 tools/mutate_pla161_post_fixture.py
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, 'test_promote_pla161_hunt28_declaration.py')
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

sys.path.insert(0, HERE)
import promote_pla161_hunt28_declaration as P  # noqa: E402

LIVE_POST_FIXTURE = """@pytest.fixture(scope='module')
def post():
    with open(CANONICAL, encoding='utf-8') as fh:
        return json.load(fh)"""

PINNED_POST_ANCHOR = "    return json.loads(promote_fixture.pre_state(P.POST_SHA))"

# (name, anchor, replacement, guard that MUST redden; None = positive control)
MUTATIONS = [
    ("THE REGRESSION ITSELF: `post` repointed back at live canonical",
     PINNED_POST_ANCHOR,
     "    with open(CANONICAL, encoding='utf-8') as fh:\n        return json.load(fh)",
     "test_the_post_fixture_is_pinned_to_this_promotes_output"),

    ("`post` pinned to the BASE state instead of the promote's output",
     PINNED_POST_ANCHOR,
     "    return json.loads(promote_fixture.pre_state(P.BASE_SHA))",
     "test_the_post_fixture_is_pinned_to_this_promotes_output"),

    # --- DATA-LEVEL defects. The first version of this harness mutated the GUARDS instead
    # (replacing an assertion with `assert True`) and scored three survivors -- but weakening a
    # test can never redden a test suite, so those mutations could not have been caught by
    # anything and proved nothing either way. A guard is shown non-vacuous by planting the
    # defect it exists to catch IN THE SUBJECT, then checking it fires.
    ("a stray edit lands on an unrelated crop in the post state",
     PINNED_POST_ANCHOR,
     "    _d = json.loads(promote_fixture.pre_state(P.POST_SHA))\n"
     "    _d['crops'][0]['description_beginner'] = 'SABOTAGE'\n"
     "    return _d",
     "test_nothing_else_in_the_dataset_moved"),

    ("an EXTRA finding is ADDED in post (the direction a pre-only walk cannot see)",
     PINNED_POST_ANCHOR,
     "    _d = json.loads(promote_fixture.pre_state(P.POST_SHA))\n"
     "    next(c for c in _d['crops'] if c['slug'] == 'lemon')"
     "['verification_status']['open_findings'].append({'id': 'ghost_finding'})\n"
     "    return _d",
     "test_nothing_else_in_the_dataset_moved"),

    ("a pre-existing finding is DROPPED in post",
     PINNED_POST_ANCHOR,
     "    _d = json.loads(promote_fixture.pre_state(P.POST_SHA))\n"
     "    _f = next(c for c in _d['crops'] if c['slug'] == 'lemon')"
     "['verification_status']['open_findings']\n"
     "    del _f[0]\n"
     "    return _d",
     "test_nothing_else_in_the_dataset_moved"),

    # SENTINEL: guaranteed fatal.
    ("SENTINEL: POST_SHA corrupted, so the pinned fixture cannot rebuild at all",
     "import promote_pla161_hunt28_declaration as P  # noqa: E402",
     "import promote_pla161_hunt28_declaration as P  # noqa: E402\nP.POST_SHA = '0' * 64",
     "__SENTINEL__"),
]


def run_suite(suite_path):
    """(green, failing_test_names, collected).

    `collected` is False when pytest never ran a test -- an import/collection error. That case
    must NEVER be scored as a catch: it exits non-zero for a reason that has nothing to do with
    the guard under test, which is how a harness reports confident garbage. The first run of
    this harness did exactly that: the mutated copy was written to a temp dir OUTSIDE the repo,
    so the suite's own `REPO = dirname(dirname(__file__))` misresolved, `import promote_fixture`
    failed, and all five mutations 'survived' with zero tests executed."""
    r = subprocess.run([sys.executable, '-m', 'pytest', suite_path, '-q', '--no-header',
                        '-p', 'no:cacheprovider'],
                       cwd=REPO, capture_output=True, text=True)
    out = r.stdout + r.stderr
    # FAILED *and* ERROR. A mutation that breaks a FIXTURE (a corrupted POST_SHA, an
    # unrebuildable pre-state) makes pytest report ERROR, not FAILED -- and that is a
    # legitimate catch: the suite refusing to run beats the suite running vacuously. Scoring
    # only FAILED lines made the sentinel read as a survivor.
    failing = set()
    for line in out.splitlines():
        for tag in ('FAILED ', 'ERROR '):
            if line.startswith(tag):
                failing.add(line.split(' ', 1)[1].split(' ')[0].split('::')[-1])
    # Count-based, NOT keyword-based. The first version of this check looked for 'error' in
    # the output tail and matched the word 'AssertionError' inside a legitimately caught
    # mutation -- scoring a working guard as a dead harness. If pytest reports a passed/failed
    # count, tests ran.
    collected = bool(re.search(r'\d+ (passed|failed|error)', out))
    return r.returncode == 0, failing, collected


def main():
    original = open(SUITE).read()

    # --- POSITIVE CONTROL, and it is the fix's whole claim ---
    live_sha = hashlib.sha256(open(CANONICAL, 'rb').read()).hexdigest()
    moved = live_sha != P.POST_SHA
    ok, failing, collected = run_suite(SUITE)
    if not ok:
        print('HARNESS DEAD: the CLEAN suite is not green; mutation results would be noise.')
        print(f'  failing: {sorted(failing)}')
        return 1
    print(f'baseline: CLEAN suite green')
    print(f'positive control: live canonical is {live_sha[:12]}, POST_SHA is {P.POST_SHA[:12]} '
          f'-- {"MOVED (the fix is being exercised)" if moved else "NOT YET MOVED"}')
    if not moved:
        print('HARNESS DEAD: live canonical has not moved past POST_SHA, so this run cannot')
        print('  distinguish the corrected wiring from the broken one. Nothing is proven.')
        return 1
    print()

    results = []
    for name, anchor, replacement, expect in MUTATIONS:
        if anchor not in original:
            print(f'HARNESS DEAD: anchor for {name!r} did not match the suite source.')
            print('  A mutation that cannot be applied is a HARD ERROR, never a survivor.')
            return 1
        marker = f'# MUTATION-APPLIED: {name}\n'
        mutated = marker + original.replace(anchor, replacement, 1)

        # INSIDE tools/, because the suite resolves REPO from its own __file__ and needs the
        # real repo to rebuild fixtures from git. Removed in `finally` on every path.
        mpath = os.path.join(HERE, '_test_mutated_pla161_tmp.py')
        try:
            with open(mpath, 'w') as fh:
                fh.write(mutated)
            on_disk = open(mpath).read()
            assert marker in on_disk, f'MUTATION-APPLIED marker absent for {name!r}'
            assert on_disk.replace(marker, '', 1) != original, \
                f'mutated copy is byte-identical to the original for {name!r}'
            ok, failing, collected = run_suite(mpath)
        finally:
            if os.path.exists(mpath):
                os.remove(mpath)

        if not collected:
            print(f'HARNESS DEAD: the mutated suite for {name!r} never ran a test '
                  f'(import/collection error). A run that executed nothing cannot distinguish '
                  f'a surviving mutation from a broken harness.')
            return 1

        if expect in ('__SENTINEL__', '__SENTINEL_SOFT__'):
            # `bool(failing)`, not `not ok`: a non-zero exit with zero failing tests is a broken
            # run, not a caught mutation.
            results.append(('SENTINEL' if expect == '__SENTINEL__' else 'MUTATION', name,
                            bool(failing), f'caught by {sorted(failing)[:3]}' if failing else 'SURVIVED'))
        else:
            hit = expect in failing
            results.append(('MUTATION', name, hit,
                            f'caught by {sorted(failing)[:3]}' if failing else 'SURVIVED'))

    sentinel = [r for r in results if r[0] == 'SENTINEL']
    if not sentinel or not sentinel[0][2]:
        print('HARNESS DEAD: the sentinel mutation did not redden the suite.')
        return 1

    real = [r for r in results if r[0] == 'MUTATION']
    caught = [r for r in real if r[2]]
    for kind, name, good, detail in results:
        print(f"  [{'OK  ' if good else 'FAIL'}] {kind:<8} {name}\n           -> {detail}")
    print('\nsentinel: reddened (harness live)')
    print(f'positive control: suite green with live {live_sha[:12]} != POST {P.POST_SHA[:12]}')
    print(f'mutations: {len(caught)}/{len(real)} CAUGHT, {len(real) - len(caught)} survivor(s)')
    for _, name, good, _ in real:
        if not good:
            print(f'  SURVIVOR: {name}')
    return 0 if len(caught) == len(real) else 1


if __name__ == '__main__':
    sys.exit(main())
