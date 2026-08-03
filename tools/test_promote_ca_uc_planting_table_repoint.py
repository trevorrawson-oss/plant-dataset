#!/usr/bin/env python3
"""Guard suite for promote_ca_uc_planting_table_repoint.py.

Every fixture is REBUILT from the pinned pre-state via promote_fixture.scratch -- never copied
from live canonical, which is how six suites in this repo went silently vacuous while green.
There is no skip path: an unresolvable base SHA raises.

Assertions pin the ABORT MESSAGE, not just the exit code. The checks in this promote overlap
heavily (a contradicted window and a changed footprint both exit 2), so exit-code-only assertions
would stay green with the interesting guard deleted.

Runs under pytest AND standalone -- every guard lives in a test BODY, never under __main__.
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import promote_fixture  # noqa: E402

SCRIPT = os.path.join(REPO, 'tools', 'promote_ca_uc_planting_table_repoint.py')
BASE = '38a579d4c3e92e470892c9c992215de750f14f5bad02107d6cfc790ebdecc93a'


def run(mutate=None, expect_sha=None, apply_=True):
    """Rebuild the pre-state (optionally doctored), run the promote, return (rc, output)."""
    path, sha = promote_fixture.scratch(BASE, mutate)
    p = subprocess.run(
        [sys.executable, SCRIPT, '--canonical', path,
         '--expect-sha', expect_sha or sha, '--apply' if apply_ else '--dry-run'],
        cwd=REPO, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def aborts(mutate, needle, expect_sha=None):
    rc, out = run(mutate, expect_sha=expect_sha)
    assert rc == 2, 'expected abort, got rc=%d\n%s' % (rc, out[-1500:])
    assert needle in out, 'expected %r in output:\n%s' % (needle, out[-1500:])


# --------------------------------------------------------------------------- happy path
def test_clean_pre_state_applies():
    rc, out = run()
    assert rc == 0, out[-2000:]
    assert 'applied: 178 anchoring_urls entries / 89 nodes / 52 decisions' in out
    assert 'verified: 0 bare UC hosts remain in the 26 repointed pairs' in out
    assert 'verified: all 6 held pairs byte-identical' in out
    assert 'verified: exactly 8 crops changed, no top-level key moved' in out


def test_dry_run_writes_nothing():
    path, sha = promote_fixture.scratch(BASE, None)
    import hashlib
    p = subprocess.run([sys.executable, SCRIPT, '--canonical', path,
                        '--expect-sha', sha, '--dry-run'],
                       cwd=REPO, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    with open(path, 'rb') as fh:
        assert hashlib.sha256(fh.read()).hexdigest() == sha, 'dry run mutated the file'


# --------------------------------------------------------------------------- SHA pin
def test_sha_drift_aborts():
    def mutate(crops, data):
        crops['okra']['regions']['ca_interior']['resolved_by_zone']['9']['plant_out'] = 'May 2 - May 3'
    aborts(mutate, 'ABORT: canonical drifted', expect_sha=BASE)


# --------------------------------------------------------------------------- THE load-bearing guard
def test_contradicted_window_aborts():
    """A window with no overlap against Table 13.2 must never be repointed at it."""
    def mutate(crops, data):
        # UC gives Interior Valleys winter squash "April-June"; December overlaps nothing.
        crops['acorn-squash']['regions']['ca_interior']['resolved_by_zone']['9']['plant_out'] = \
            'Dec 1 - Dec 20'
    aborts(mutate, 'is CONTRADICTED by the table')


def test_contradicted_second_planting_aborts():
    """The second planting is adjudicated too, not just the main window."""
    def mutate(crops, data):
        cell = crops['watermelon']['regions']['ca_south_coast']['resolved_by_zone']['9']
        cell['second_planting'] = {'plant_out': 'Nov 1 - Nov 30'}
    aborts(mutate, 'is CONTRADICTED by the table')


def test_unparseable_window_aborts():
    def mutate(crops, data):
        crops['okra']['regions']['ca_interior']['resolved_by_zone']['9']['plant_out'] = 'whenever'
    aborts(mutate, 'cannot parse window')


def test_missing_window_aborts():
    def mutate(crops, data):
        crops['okra']['regions']['ca_interior']['resolved_by_zone']['9']['plant_out'] = ''
    aborts(mutate, 'states no planting window')


def test_missing_resolved_by_zone_aborts():
    def mutate(crops, data):
        crops['okra']['regions']['ca_interior']['resolved_by_zone'] = {}
    aborts(mutate, 'has no resolved_by_zone')


# --------------------------------------------------------------------------- premise guards
def test_missing_region_aborts():
    def mutate(crops, data):
        del crops['okra']['regions']['ca_interior']
    aborts(mutate, 'has no ca_interior region')


def test_missing_crop_aborts():
    def mutate(crops, data):
        data['crops'] = [c for c in data['crops'] if c['slug'] != 'okra']
    aborts(mutate, 'ABORT: crop okra absent')


def test_held_pair_already_repointed_aborts():
    """If the excluded pairs are no longer bare, the ruling this promote rests on is overtaken."""
    def mutate(crops, data):
        for reg in ('ca_desert',):
            for node in _walk(crops['okra']['regions'][reg]):
                au = node.get('anchoring_urls') or {}
                for sid in au:
                    if sid in ('ucanr_ext', 'uc_mg'):
                        au[sid]['url'] = 'https://ucanr.edu/some/real/page'
        for node in _walk(crops['okra']['regions']['ca_north_coast']):
            au = node.get('anchoring_urls') or {}
            for sid in au:
                if sid in ('ucanr_ext', 'uc_mg'):
                    au[sid]['url'] = 'https://ucanr.edu/some/real/page'
    aborts(mutate, 'exclusion list is stale')


# --------------------------------------------------------------------------- footprint guards
def test_extra_bare_anchor_changes_the_count_and_aborts():
    def mutate(crops, data):
        # a NEW bare-UC node inside a repointed pair -- not seen when the footprint was measured
        crops['okra']['regions']['ca_interior']['anchoring_urls'] = {
            'ucanr_ext': {'url': 'https://ucanr.edu', 'verified': '2026-06-29'}}
    aborts(mutate, 'anchor entries, expected 178')


def test_removed_bare_anchor_changes_the_count_and_aborts():
    def mutate(crops, data):
        au = crops['okra']['regions']['ca_interior']['resolved_by_zone']['9']['anchoring_urls']
        au.pop('uc_mg', None)
    aborts(mutate, 'anchor entries, expected 178')


def test_unexpected_anchor_keys_abort():
    def mutate(crops, data):
        au = crops['okra']['regions']['ca_interior']['resolved_by_zone']['9']['anchoring_urls']
        au['ucanr_ext']['note'] = 'something new the footprint never accounted for'
    aborts(mutate, 'carries unexpected keys')


# --------------------------------------------------------------------------- shim-reached guards
def test_a_value_change_riding_along_aborts():
    """Simulate the edit loop moving a planting window. Only url/verified may move.

    Unreachable by fixture mutation alone -- the pre-state doctoring would be re-read as the
    pre-state. So doctor the BEFORE snapshot instead: patch copy.deepcopy so the first call (the
    `before` capture) returns a tree whose window differs from what gets written.
    """
    shim = (
        'import copy, json\n'
        '_real = copy.deepcopy\n'
        '_n = {"i": 0}\n'
        'def _fake(x, *a, **k):\n'
        '    out = _real(x, *a, **k)\n'
        '    _n["i"] += 1\n'
        '    if _n["i"] == 1:\n'
        '        for c in out["crops"]:\n'
        '            if c["slug"] == "okra":\n'
        '                c["regions"]["ca_interior"]["resolved_by_zone"]["9"]'
        '["plant_out"] = "May 3 - May 4"\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'changed somewhere other than a UC url/verified pair')


def test_trailing_newline_aborts():
    """Write-time guard: COMPACT canonical must never gain a trailing newline."""
    shim = (
        'import json\n'
        '_real = json.dumps\n'
        'json.dumps = lambda *a, **k: _real(*a, **k) + "\\n"\n')
    _run_with_shim(shim, 'trailing newline introduced')


def test_top_level_key_change_aborts():
    shim = (
        'import copy\n'
        '_real = copy.deepcopy\n'
        '_n = {"i": 0}\n'
        'def _fake(x, *a, **k):\n'
        '    out = _real(x, *a, **k)\n'
        '    _n["i"] += 1\n'
        '    if _n["i"] == 1:\n'
        '        out["version"] = "__doctored__"\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'top-level version changed')


# --------------------------------------------------------------------------- guards that mutation
# testing proved unreachable by fixture doctoring alone. Each needed a shim; without one they were
# green and VACUOUS. 8 of 21 were in that state on the first pass -- the fifth occurrence in the
# repo's history of a guard test passing because it could not reach its guard.
def test_a_held_pair_inside_the_repoint_set_aborts():
    """The constant-vs-constant check: the exclusion list must not overlap the worklist."""
    shim = (
        'import runpy, sys, types\n'
        'import importlib.util as _iu\n'
        '_spec = _iu.spec_from_file_location("prm", %r)\n'
        '_m = _iu.module_from_spec(_spec)\n' % SCRIPT +
        'sys.modules["prm"] = _m\n'
        '_spec.loader.exec_module(_m)\n'
        '_m.REPOINT_PAIRS = _m.REPOINT_PAIRS + [("okra", "ca_desert")]\n')
    _run_module_with_shim(shim, 'a held pair appears in the repoint set')


def test_unparseable_uc_row_aborts():
    """If the transcribed table row stops yielding months, we must not repoint blind."""
    shim = (
        'import sys\n'
        'import importlib.util as _iu\n'
        '_spec = _iu.spec_from_file_location("prm", %r)\n'
        '_m = _iu.module_from_spec(_spec)\n' % SCRIPT +
        'sys.modules["prm"] = _m\n'
        '_spec.loader.exec_module(_m)\n'
        '_m.UC_TABLE = dict(_m.UC_TABLE)\n'
        '_m.UC_TABLE["okra"] = ("May", "April-May", "n/a", "May")\n')
    _run_module_with_shim(shim, 'no UC months parsed')


def test_node_count_drift_aborts_even_when_entry_count_holds():
    """Move one anchor to a NEW node: entries stay 178, nodes become 90."""
    def mutate(crops, data):
        reg = crops['okra']['regions']['ca_interior']
        au = reg['resolved_by_zone']['9']['anchoring_urls']
        moved = au.pop('uc_mg')
        reg['anchoring_urls'] = {'uc_mg': moved}
    aborts(mutate, 'touched 90 nodes, expected 89')


def test_a_typoed_target_url_that_is_still_bare_aborts():
    """The post-condition that a repoint actually left the domain root behind."""
    shim = (
        'import sys\n'
        'import importlib.util as _iu\n'
        '_spec = _iu.spec_from_file_location("prm", %r)\n'
        '_m = _iu.module_from_spec(_spec)\n' % SCRIPT +
        'sys.modules["prm"] = _m\n'
        '_spec.loader.exec_module(_m)\n'
        '_m.NEW_URL = "https://ucanr.edu"\n')
    _run_module_with_shim(shim, 'still carries the bare ucanr_ext host')


def test_a_held_pair_mutating_under_us_aborts():
    """Doctor the `before` snapshot so a held pair differs -- the edit loop never touches them."""
    shim = (
        'import copy\n'
        '_real = copy.deepcopy\n'
        '_n = {"i": 0}\n'
        'def _fake(x, *a, **k):\n'
        '    out = _real(x, *a, **k)\n'
        '    _n["i"] += 1\n'
        '    if _n["i"] == 1:\n'
        '        for c in out["crops"]:\n'
        '            if c["slug"] == "okra":\n'
        '                c["regions"]["ca_desert"]["resolved_by_zone"]["9"]'
        '["plant_out"] = "__doctored__"\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'held pair okra/ca_desert was modified')


def test_an_extra_crop_in_the_footprint_aborts():
    """Doctor `before` on a crop this promote must never touch."""
    shim = (
        'import copy\n'
        '_real = copy.deepcopy\n'
        '_n = {"i": 0}\n'
        'def _fake(x, *a, **k):\n'
        '    out = _real(x, *a, **k)\n'
        '    _n["i"] += 1\n'
        '    if _n["i"] == 1:\n'
        '        for c in out["crops"]:\n'
        '            if c["slug"] == "carrot":\n'
        '                c["__doctored__"] = True\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'ABORT: crops changed =')


def _run_module_with_shim(shim, needle):
    """Load the promote as a module, let the shim patch its CONSTANTS, then call main()."""
    import tempfile
    path, sha = promote_fixture.scratch(BASE, None)
    driver = os.path.join(tempfile.mkdtemp(prefix='shimmod_'), 'drive.py')
    with open(driver, 'w') as fh:
        fh.write(shim + (
            'sys.argv = ["promote", "--canonical", %r, "--expect-sha", %r, "--apply"]\n'
            'sys.exit(_m.main())\n' % (path, sha)))
    p = subprocess.run([sys.executable, driver], cwd=REPO, capture_output=True, text=True)
    out = p.stdout + p.stderr
    assert needle in out, 'expected %r in output:\n%s' % (needle, out[-1500:])


def _run_with_shim(shim, needle):
    import tempfile
    path, sha = promote_fixture.scratch(BASE, None)
    driver = os.path.join(tempfile.mkdtemp(prefix='shim_'), 'drive.py')
    with open(driver, 'w') as fh:
        fh.write(shim + (
            'import runpy, sys\n'
            'sys.argv = ["promote", "--canonical", %r, "--expect-sha", %r, "--apply"]\n'
            'runpy.run_path(%r, run_name="__main__")\n' % (path, sha, SCRIPT)))
    p = subprocess.run([sys.executable, driver], cwd=REPO, capture_output=True, text=True)
    out = p.stdout + p.stderr
    assert needle in out, 'expected %r in output:\n%s' % (needle, out[-1500:])


def _walk(node):
    out = []

    def go(n):
        if isinstance(n, dict):
            if isinstance(n.get('anchoring_urls'), dict):
                out.append(n)
            for k, v in n.items():
                if k != 'anchoring_urls':
                    go(v)
        elif isinstance(n, list):
            for v in n:
                go(v)
    go(node)
    return out


def main():
    fns = [(n, f) for n, f in sorted(globals().items())
           if n.startswith('test_') and callable(f)]
    bad = 0
    for name, fn in fns:
        try:
            fn()
            print('  PASS  %s' % name)
        except AssertionError as e:
            bad += 1
            print('  FAIL  %s\n        %s' % (name, str(e)[:300]))
    print('\n%d/%d passed' % (len(fns) - bad, len(fns)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
