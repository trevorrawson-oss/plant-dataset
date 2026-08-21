#!/usr/bin/env python3
"""Instrumented mutation harness for the PLA-290 follow-on echinacea suite. PLA-215 convention.

THIS HARNESS CARRIES MORE WEIGHT HERE THAN IT DID FOR PLA-290, and the reason is worth stating.
A replay-pinned suite has NO RED PHASE by construction: its `post` IS the promote's own output,
so it goes green the moment the promote is written and can never be observed failing first.
PLA-290's suite only had a RED phase because it initially (wrongly) read live canonical. So for
this suite the mutation run is not corroborating evidence of non-vacuity -- it is the ONLY
evidence, alongside the reachability guard that proves the PRE state really did contain the
offender the cap check exists to catch.

The three self-checks the convention requires:

  MUTATION-APPLIED MARKER  every mutated copy carries `# MUTATION-APPLIED: <name>`, asserted
                           present and asserted to differ from the original. A non-matching
                           anchor is a HARD ERROR, never a survivor.
  SENTINEL                 one guaranteed-fatal mutation must redden, or HARNESS DEAD.
  POSITIVE CONTROL         one guaranteed-invisible mutation must stay GREEN.

Run: python3 tools/mutate_pla290b_echinacea_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME = 'promote_pla290b_echinacea_record.py'
SUITE_NAME = 'test_promote_pla290b_echinacea_record.py'
SCRIPT = os.path.join(HERE, SCRIPT_NAME)
SUITE = os.path.join(HERE, SUITE_NAME)

sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla290b_echinacea_record as P  # noqa: E402

APPLY = "    by[CROP]['varieties']['recommended'][INDEX] = dict(RECORD)\n"


def mut(*lines):
    body = "    _r = dict(RECORD)\n"
    for ln in lines:
        body += "    " + ln + "\n"
    return body + "    by[CROP]['varieties']['recommended'][INDEX] = _r\n"


MUTATIONS = [
    ("the entry is left as the 228-char prose string (the defect survives)",
     APPLY, "    pass\n",
     "test_no_variety_display_name_exceeds_the_cap_ANYWHERE"),

    ("the whole sentence is kept as the name",
     APPLY, mut("_r['name'] = PREV_ENTRY", "_r['id'] = slugify_variety(PREV_ENTRY)"),
     "test_the_name_is_a_name_and_not_a_sentence"),

    ("the id is re-keyed to a cultivar from inside the parenthetical, stranding plantings",
     APPLY, mut("_r['id'] = 'big-sky'"),
     "test_the_id_prefixes_the_stored_legacy_slug"),

    ("the id drifts from slugify(name)",
     APPLY, mut("_r['name'] = 'Interspecific hybrid series'"),
     "test_the_id_equals_slugify_of_its_name"),

    ("two named cultivars are quietly dropped from the note",
     APPLY, mut("_r['note'] = _r['note'].replace(\"Sombrero, 'Hot Papaya', and \", '')"),
     "test_the_note_keeps_every_named_cultivar"),

    ("the note is truncated at its first period, dropping the color and habit clauses",
     APPLY, mut("_r['note'] = _r['note'].split('. ')[0] + '.'"),
     "test_no_word_of_the_original_was_dropped"),

    ("the note loses its terminal period",
     APPLY, mut("_r['note'] = _r['note'].rstrip('.')"),
     "test_the_note_is_a_finished_sentence_without_an_em_dash"),

    ("an em dash reaches the consumer copy",
     APPLY, mut("_r['note'] = _r['note'].replace('. Showy', ' \\u2014 showy')"),
     "test_the_note_is_a_finished_sentence_without_an_em_dash"),

    ("a days_to_maturity is invented",
     APPLY, mut("_r['days_to_maturity'] = 90"),
     "test_no_days_to_maturity_was_invented"),

    ("one of echinacea's six untouched strings is converted in passing",
     APPLY,
     APPLY + "    by[CROP]['varieties']['recommended'][0] = {\n"
             "        'id': 'magnus', 'name': 'Magnus', 'note': 'Converted.'}\n",
     "test_echinaceas_other_six_entries_are_untouched_strings"),

    ("an unrelated crop gains a key (a pre-only walk cannot see this)",
     APPLY, APPLY + "    by['tomatillo']['_lane_note'] = 'drifted'\n",
     "test_nothing_outside_that_one_leaf_moved"),

    ("a DIFFERENT crop's variety is given an over-long name (roster-wide reach)",
     APPLY, APPLY + "    by['zinnia']['varieties']['recommended'][0] = 'z' * 120\n",
     "test_no_variety_display_name_exceeds_the_cap_ANYWHERE"),

    ("a colon-format prose entry is reintroduced elsewhere (PLA-290 regression)",
     APPLY,
     APPLY + "    by['zinnia']['varieties']['recommended'][0] = 'Benary: a big double zinnia'\n",
     "test_no_variety_display_name_contains_a_colon_ANYWHERE"),

    ("the canonical is written pretty-printed instead of COMPACT",
     "    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')\n",
     "    out = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')\n",
     "test_canonical_is_still_compact"),

    ("SENTINEL: the transform does nothing at all",
     "def apply_to(data):\n", "def apply_to(data):\n    return data\n",
     "__SENTINEL__"),

    ("POSITIVE CONTROL: a comment is added inside the transform",
     "    by = {c['slug']: c for c in data['crops']}\n",
     "    # reworded comment, no behavior change\n"
     "    by = {c['slug']: c for c in data['crops']}\n",
     None),
]


def build_canonical(script_path, workdir):
    base = promote_fixture.pre_state(P.BASE_SHA)
    canon = os.path.join(workdir, 'crops_data_final.json')
    with open(canon, 'wb') as fh:
        fh.write(base if isinstance(base, bytes) else base.encode('utf-8'))
    r = subprocess.run([sys.executable, script_path, '--canonical', canon,
                        '--expect-sha', P.BASE_SHA, '--apply'], capture_output=True, text=True)
    return canon, r


def run_suite(workdir):
    """Run the COPY of the suite in the scratch tree, so its own REPO/HERE resolve there and it
    replays the MUTATED promote. Pointing pytest at the real suite makes every run read the real
    script and report a clean sweep -- the PLA-138 failure the sentinel exists for."""
    env = dict(os.environ)
    env['PYTHONPATH'] = HERE
    r = subprocess.run([sys.executable, '-m', 'pytest',
                        os.path.join(workdir, 'tools', SUITE_NAME), '-q', '--no-header',
                        '-p', 'no:cacheprovider', '--rootdir', workdir],
                       capture_output=True, text=True, env=env, cwd=workdir)
    failing = set()
    for line in (r.stdout + r.stderr).splitlines():
        if line.startswith('FAILED '):
            failing.add(line.split(' ', 1)[1].split(' ')[0].split('::')[-1])
    return r.returncode == 0, failing


def make_tree():
    w = tempfile.mkdtemp()
    os.makedirs(os.path.join(w, 'tools'), exist_ok=True)
    shutil.copy(SUITE, os.path.join(w, 'tools', SUITE_NAME))
    # the suite's drift guard imports PLA-290's module to compare slug rules; the
    # PROMOTE no longer does. Copied, never mutated -- it is not under test here.
    shutil.copy(os.path.join(HERE, 'promote_pla290_variety_records.py'),
                os.path.join(w, 'tools', 'promote_pla290_variety_records.py'))
    return w


def main():
    original = open(SCRIPT).read()

    w = make_tree()
    try:
        shutil.copy(SCRIPT, os.path.join(w, 'tools', SCRIPT_NAME))
        _, r = build_canonical(os.path.join(w, 'tools', SCRIPT_NAME), w)
        if r.returncode != 0:
            print('HARNESS DEAD: the CLEAN replay did not apply.')
            print(r.stdout, r.stderr)
            return 1
        ok, failing = run_suite(w)
        if not ok:
            print('HARNESS DEAD: the CLEAN replay does not pass its own suite; mutation results '
                  f'would be noise.\n  failing: {sorted(failing)}')
            return 1
    finally:
        shutil.rmtree(w, ignore_errors=True)
    print('baseline: CLEAN replay green\n')

    results = []
    for name, anchor, replacement, expect in MUTATIONS:
        if anchor not in original:
            print(f'HARNESS DEAD: anchor for {name!r} did not match the promote source.')
            return 1
        marker = f'# MUTATION-APPLIED: {name}\n'
        mutated = marker + original.replace(anchor, replacement, 1)
        w = make_tree()
        try:
            mpath = os.path.join(w, 'tools', SCRIPT_NAME)
            with open(mpath, 'w') as fh:
                fh.write(mutated)
            on_disk = open(mpath).read()
            assert marker in on_disk, f'MUTATION-APPLIED marker absent for {name!r}'
            assert on_disk.replace(marker, '', 1) != original, \
                f'mutated copy is byte-identical to the original for {name!r}'
            _, r = build_canonical(mpath, w)
            if r.returncode != 0:
                head = (r.stderr.strip().splitlines() or ['(no stderr)'])[0][:90]
                results.append(('REFUSED', name, True, f'promote refused it: {head}'))
                continue
            ok, failing = run_suite(w)
        finally:
            shutil.rmtree(w, ignore_errors=True)

        if expect is None:
            results.append(('CONTROL', name, ok,
                            'GREEN (as required)' if ok else f'REDDENED -- {sorted(failing)}'))
        elif expect == '__SENTINEL__':
            results.append(('SENTINEL', name, not ok,
                            f'caught by {len(failing)} guards' if failing else 'SURVIVED'))
        else:
            results.append(('MUTATION', name, expect in failing,
                            f'caught by {sorted(failing)[:3]}' if failing else 'SURVIVED'))

    sentinel = [x for x in results if x[0] == 'SENTINEL']
    if not sentinel or not sentinel[0][2]:
        print('HARNESS DEAD: the sentinel mutation did not redden the suite.')
        return 1

    print(f'{"KIND":<9} {"OK":<4} NAME')
    print('-' * 100)
    bad = 0
    for kind, name, ok, detail in results:
        if not ok:
            bad += 1
        print(f'{kind:<9} {"PASS" if ok else "FAIL":<4} {name}\n{"":9} {"":4} {detail}')
    print('-' * 100)
    print(f'{len(results)} injections, {bad} unsatisfactory')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
