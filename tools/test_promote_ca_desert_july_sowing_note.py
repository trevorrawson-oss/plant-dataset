#!/usr/bin/env python3
"""Guard suite for promote_ca_desert_july_sowing_note.py.

Fixtures REBUILT from the pinned pre-state via promote_fixture.scratch (replaying campaign A's two
promotes onto the last committed state), never copied from live canonical. No skip path.

Assertions pin ABORT MESSAGES, not exit codes. Runs under pytest AND standalone; every guard lives
in a test BODY, never under __main__.
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import promote_fixture  # noqa: E402

SCRIPT = os.path.join(REPO, 'tools', 'promote_ca_desert_july_sowing_note.py')
BASE = '3f6d6ce4430c23ab8b346017be3b9a8963f635fc1178767293d24e2a689eb6f3'
CROPS = ('acorn-squash', 'butternut-squash', 'spaghetti-squash', 'pumpkin')


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


def _note(crops, slug, field):
    return crops[slug]['regions']['ca_desert'][field]


# --------------------------------------------------------------------------- happy path
def test_clean_pre_state_applies():
    rc, out = run()
    assert rc == 0, out[-2000:]
    assert 'applied: 8 strings across 4 crops' in out
    assert 'preflight: all 4 crops still carry a July ca_desert second planting' in out
    assert 'verified: house style clean, no institution named, no unsourced temperature' in out
    assert 'verified: only the 8 region-note strings moved, and only in ca_desert' in out


def test_sha_drift_aborts():
    def mutate(crops, data):
        crops['pumpkin']['regions']['ca_desert']['region_notes_beginner'] += ' x'
    aborts(mutate, 'ABORT: canonical drifted', expect_sha=BASE)


# --------------------------------------------------------------------------- premise guards
def test_july_window_gone_aborts():
    """THE PREMISE: this copy explains a July sowing. If the window moves, it becomes a lie."""
    def mutate(crops, data):
        crops['pumpkin']['regions']['ca_desert']['resolved_by_zone']['10'][
            'second_planting']['plant_out'] = 'Aug 1 - Aug 31'
    aborts(mutate, 'not a July sowing')


def test_second_planting_removed_aborts():
    def mutate(crops, data):
        del crops['acorn-squash']['regions']['ca_desert']['resolved_by_zone']['9']['second_planting']
    aborts(mutate, 'not a July sowing')


def test_drifted_tail_aborts():
    """The pinned tail must still END the note; a reworded note needs re-authoring, not appending."""
    def mutate(crops, data):
        r = crops['butternut-squash']['regions']['ca_desert']
        r['region_notes_seasoned'] = r['region_notes_seasoned'].replace(
            'the fall timing is the reliable one.', 'the fall timing is dependable.')
    aborts(mutate, 'does not END with its pinned tail exactly once')


def test_note_no_longer_last_sentence_aborts():
    """Appending blind would bury the new sentence mid-note. It must still be the tail."""
    def mutate(crops, data):
        r = crops['pumpkin']['regions']['ca_desert']
        r['region_notes_seasoned'] += ' Shade cloth helps.'
    aborts(mutate, 'does not END with its pinned tail exactly once')


def test_empty_note_aborts():
    """This promote EDITS existing prose; it must refuse to author a missing note."""
    def mutate(crops, data):
        crops['spaghetti-squash']['regions']['ca_desert']['region_notes_beginner'] = ''
    aborts(mutate, 'does not author a missing note')


def test_reapplied_after_the_tail_aborts():
    """Re-running on an already-edited note: the tail is no longer last, so the tail guard bites."""
    def mutate(crops, data):
        r = crops['acorn-squash']['regions']['ca_desert']
        r['region_notes_seasoned'] += (
            ' The July timing looks punishing and is deliberate: it places flowering and fruit '
            'set in the milder weather of early fall rather than at peak summer temperatures. '
            'Keep water steady through establishment, when the seedbed is most exposed.')
    aborts(mutate, 'does not END with its pinned tail exactly once')


def test_sentence_already_present_before_the_tail_aborts():
    """The case the tail guard CANNOT see: the sentence was inserted mid-note, so the note still
    ends with its pinned tail. Without this, the duplicate-sentence guard was vacuous."""
    def mutate(crops, data):
        r = crops['acorn-squash']['regions']['ca_desert']
        tail = 'Steady irrigation is essential, and the fall timing is the reliable one.'
        add = ('The July timing looks punishing and is deliberate: it places flowering and fruit '
               'set in the milder weather of early fall rather than at peak summer temperatures. '
               'Keep water steady through establishment, when the seedbed is most exposed.')
        r['region_notes_seasoned'] = r['region_notes_seasoned'].replace(tail, add + ' ' + tail)
    aborts(mutate, 'already carries this sentence')


def test_doubled_space_in_copy_aborts():
    """Whitespace artifact guard: without a shim producing one, it could never fire."""
    shim = _mod_shim('_m.SEASONED_ADD = "  Two spaces open this sentence."')
    _run_module_with_shim(shim, 'whitespace/punctuation artifact')


def test_missing_region_aborts():
    def mutate(crops, data):
        del crops['pumpkin']['regions']['ca_desert']
    aborts(mutate, 'has no ca_desert resolved_by_zone')


# --------------------------------------------------------------------------- shim-reached guards
def test_copy_naming_an_institution_aborts():
    """These arms cite a bare host; naming a source they do not carry must abort."""
    shim = _mod_shim('_m.SEASONED_ADD = " The University of Arizona marks July 1 for this crop."')
    _run_module_with_shim(shim, 'names')


def test_copy_stating_a_temperature_aborts():
    """Deliberately qualitative: no threshold was sourced, so none may be written."""
    shim = _mod_shim(
        '_m.SEASONED_ADD = " Fruit set fails above 95 degrees F, so July works."')
    _run_module_with_shim(shim, 'states a temperature')


def test_em_dash_in_copy_aborts():
    shim = _mod_shim('_m.BEGINNER_ADD = " Plant in July ' + chr(8212) + ' it is on purpose."')
    _run_module_with_shim(shim, 'em dash')


def test_double_hyphen_in_copy_aborts():
    shim = _mod_shim('_m.BEGINNER_ADD = " Plant in July -- it is on purpose."')
    _run_module_with_shim(shim, 'em dash or')


def test_wrong_string_count_aborts():
    shim = _mod_shim('_m.CROPS = ("acorn-squash", "pumpkin")')
    _run_module_with_shim(shim, 'rewrote 4 strings, expected 8')


def test_a_value_change_riding_along_aborts():
    """Prose only: no window, citation or other region may move."""
    shim = (
        'import copy\n'
        '_real = copy.deepcopy\n'
        '_n = {"i": 0}\n'
        'def _fake(x, *a, **k):\n'
        '    out = _real(x, *a, **k)\n'
        '    _n["i"] += 1\n'
        '    if _n["i"] == 1:\n'
        '        for c in out["crops"]:\n'
        '            if c["slug"] == "pumpkin":\n'
        '                c["regions"]["ca_desert"]["resolved_by_zone"]["9"]'
        '["harvest_start"] = "__doctored__"\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'changed outside the 8 region-note strings')


def test_another_region_changing_aborts():
    shim = (
        'import copy\n'
        '_real = copy.deepcopy\n'
        '_n = {"i": 0}\n'
        'def _fake(x, *a, **k):\n'
        '    out = _real(x, *a, **k)\n'
        '    _n["i"] += 1\n'
        '    if _n["i"] == 1:\n'
        '        for c in out["crops"]:\n'
        '            if c["slug"] == "pumpkin":\n'
        '                c["regions"]["rgv"]["region_notes_seasoned"] = "__doctored__"\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'changed outside the 8 region-note strings')


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
        '                c["__doctored__"] = True\n'
        '    return out\n'
        'copy.deepcopy = _fake\n')
    _run_with_shim(shim, 'ABORT: crops changed =')


def test_trailing_newline_aborts():
    shim = (
        'import json\n'
        '_real = json.dumps\n'
        'json.dumps = lambda *a, **k: _real(*a, **k) + "\\n"\n')
    _run_with_shim(shim, 'trailing newline introduced')


def _mod_shim(patch):
    return (
        'import sys\n'
        'import importlib.util as _iu\n'
        '_spec = _iu.spec_from_file_location("prm", %r)\n'
        '_m = _iu.module_from_spec(_spec)\n' % SCRIPT +
        'sys.modules["prm"] = _m\n'
        '_spec.loader.exec_module(_m)\n' + patch + '\n')


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
