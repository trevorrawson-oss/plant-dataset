#!/usr/bin/env python3
"""Guard suite for promote_ca_uc_case2_findings.py.

Fixtures are REBUILT from the pinned pre-state via promote_fixture.scratch (which replays the
campaign-A repoint onto the last committed state), never copied from live canonical. No skip path.

Assertions pin ABORT MESSAGES, not exit codes -- the checks overlap, so an exit-code-only
assertion stays green with the interesting guard deleted.

Runs under pytest AND standalone; every guard lives in a test BODY, never under __main__.
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import promote_fixture  # noqa: E402

SCRIPT = os.path.join(REPO, 'tools', 'promote_ca_uc_case2_findings.py')
BASE = 'e65aa63ae6154371233edbf076d7f94003652dfbd64980eae3c20a2afb3c76cd'


def run(mutate=None, expect_sha=None):
    path, sha = promote_fixture.scratch(BASE, mutate)
    p = subprocess.run(
        [sys.executable, SCRIPT, '--canonical', path,
         '--expect-sha', expect_sha or sha, '--apply'],
        cwd=REPO, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def aborts(mutate, needle, expect_sha=None):
    rc, out = run(mutate, expect_sha=expect_sha)
    assert rc == 2, 'expected abort, got rc=%d\n%s' % (rc, out[-1500:])
    assert needle in out, 'expected %r in output:\n%s' % (needle, out[-1500:])


def _findings(crop):
    return (crop.get('verification_status') or {}).get('open_findings') or []


# --------------------------------------------------------------------------- happy path
def test_clean_pre_state_applies():
    rc, out = run()
    assert rc == 0, out[-2000:]
    assert 'filed: 5 findings' in out
    assert 'preflight: all 9 decisions still sole bare hosts' in out
    assert 'verified: nothing but open_findings moved' in out
    assert 'verified: each of the 5 crops gained exactly one finding' in out


def test_sha_drift_aborts():
    def mutate(crops, data):
        crops['okra']['regions']['ca_desert']['resolved_by_zone']['9']['plant_out'] = 'Apr 1 - Apr 2'
    aborts(mutate, 'ABORT: canonical drifted', expect_sha=BASE)


# --------------------------------------------------------------------------- premise guards
def test_a_repointed_decision_aborts():
    """If a cell has been repointed since, the finding would describe a state that is gone."""
    def mutate(crops, data):
        for node in _walk(crops['arugula']['regions']['ca_interior']):
            au = node.get('anchoring_urls') or {}
            if 'uc_mg' in au:
                au['uc_mg']['url'] = 'https://ucanr.edu/some/real/arugula/page'
    aborts(mutate, 'no longer cites https://mg.ucanr.edu as a sole bare host')


def test_the_pear_url_is_pinned_per_decision():
    """THE BUG THIS SUITE EXISTS FOR: the pears cite homeorchard, not the vegetable table.

    A global bare-host map would silently accept the wrong URL here and file a finding asserting
    something false about the citation. Flip the pears to the generic root and the pinned URL
    must refuse it.
    """
    def mutate(crops, data):
        for node in _walk(crops['pear-asian']['regions']['ca_interior']):
            au = node.get('anchoring_urls') or {}
            if 'ucanr_ext' in au:
                au['ucanr_ext']['url'] = 'https://ucanr.edu'
    aborts(mutate, 'no longer cites https://homeorchard.ucanr.edu/ as a sole bare host')


def test_okra_window_drift_aborts():
    """The okra ruling QUOTES its windows; if they move, the reasoning must be re-adjudicated."""
    def mutate(crops, data):
        crops['okra']['regions']['ca_desert']['resolved_by_zone']['10']['plant_out'] = 'May 1 - May 31'
    aborts(mutate, 'finding quotes')


def test_missing_crop_aborts():
    def mutate(crops, data):
        data['crops'] = [c for c in data['crops'] if c['slug'] != 'edamame']
    aborts(mutate, 'ABORT: crop edamame absent')


def test_missing_region_aborts():
    def mutate(crops, data):
        del crops['arugula']['regions']['ca_south_coast']
    aborts(mutate, 'has no ca_south_coast region')


def test_already_filed_aborts():
    def mutate(crops, data):
        _findings(crops['okra']).append(
            {'id': 'okra_ca_uc_row_lacks_regional_resolution', 'status': 'accepted'})
    aborts(mutate, 'already filed')


# --------------------------------------------------------------------------- shim-reached guards
def test_a_value_change_riding_along_aborts():
    """Findings-only: not one citation, window or prose byte may move."""
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
        '["harvest_start"] = "__doctored__"\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'something other than open_findings changed')


def test_an_extra_crop_in_the_footprint_aborts():
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
        '                c.setdefault("verification_status", {})'
        '.setdefault("open_findings", []).append({"id": "__doctored__"})\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'ABORT: crops changed =')


def test_a_finding_naming_an_outside_institution_aborts():
    """Only okra's ruling rests on AZ1005; no other finding may name an outside institution."""
    shim = (
        'import sys\n'
        'import importlib.util as _iu\n'
        '_spec = _iu.spec_from_file_location("prm", %r)\n'
        '_m = _iu.module_from_spec(_spec)\n' % SCRIPT +
        'sys.modules["prm"] = _m\n'
        '_spec.loader.exec_module(_m)\n'
        '_m.FINDINGS[0][1]["summary"] += " NC State also publishes an arugula date."\n')
    _run_module_with_shim(shim, 'which its ruling does not rest on')


def test_wrong_finding_count_aborts():
    shim = (
        'import sys\n'
        'import importlib.util as _iu\n'
        '_spec = _iu.spec_from_file_location("prm", %r)\n'
        '_m = _iu.module_from_spec(_spec)\n' % SCRIPT +
        'sys.modules["prm"] = _m\n'
        '_spec.loader.exec_module(_m)\n'
        '_m.FINDINGS = _m.FINDINGS[:3]\n')
    _run_module_with_shim(shim, 'filed 3 findings, expected 5')


def test_two_findings_on_one_crop_aborts():
    shim = (
        'import sys, copy\n'
        'import importlib.util as _iu\n'
        '_spec = _iu.spec_from_file_location("prm", %r)\n'
        '_m = _iu.module_from_spec(_spec)\n' % SCRIPT +
        'sys.modules["prm"] = _m\n'
        '_spec.loader.exec_module(_m)\n'
        '_extra = copy.deepcopy(_m.FINDINGS[0][1])\n'
        '_extra["id"] = "arugula_second_finding"\n'
        '_m.FINDINGS = _m.FINDINGS + [("arugula", _extra)]\n'
        '_m.EXPECT_FINDINGS = 6\n')
    _run_module_with_shim(shim, 'expected +1')


def test_trailing_newline_aborts():
    shim = (
        'import json\n'
        '_real = json.dumps\n'
        'json.dumps = lambda *a, **k: _real(*a, **k) + "\\n"\n')
    _run_with_shim(shim, 'trailing newline introduced')


def test_top_level_key_change_aborts():
    """Caught by the stripped() whole-document compare, which is why no separate
    top-level guard exists -- one was written, mutation-proven unreachable, and removed."""
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
    _run_with_shim(shim, 'something other than open_findings changed')


def _run_module_with_shim(shim, needle):
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
