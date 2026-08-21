#!/usr/bin/env python3
"""Instrumented mutation harness for the PLA-290 variety-record suite. PLA-215 convention.

Mutations are injected into a SCRATCH COPY of the promote script, and the suite runs against a
canonical rebuilt by replaying that mutated script from the pinned base -- never against live
canonical, never by editing the live script.

The three self-checks the convention requires (PLA-138's harness dedented an already-indented
template, silently ran the CLEAN fixture, and reported every mutation as surviving):

  MUTATION-APPLIED MARKER  every mutated copy carries `# MUTATION-APPLIED: <name>`, asserted
                           present in the file about to execute and asserted to differ from the
                           original. A non-matching anchor is a HARD ERROR, never a survivor.
  SENTINEL                 one guaranteed-fatal mutation must redden, or the run exits
                           HARNESS DEAD and reports nothing else.
  POSITIVE CONTROL         one guaranteed-invisible mutation must stay GREEN, so "the guard is
                           blind" stays distinguishable from "the injection was a no-op".

WHY EVERY MUTATION IS INJECTED INSIDE apply_to() AND NOT INTO THE TABLES. The promote re-checks
the shim constraint and the id rule against RECORDS before it writes anything, so a corrupted
TABLE is refused at the door and the guard suite never sees it. That refusal is real protection,
but it is not evidence that the GUARDS work. Mutating the transform after the precondition gate
is the only injection point at which a defect actually reaches canonical, which is the defect
the suite exists to catch.

Run: python3 tools/mutate_pla290_variety_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPT_NAME = 'promote_pla290_variety_records.py'
SUITE_NAME = 'test_promote_pla290_variety_records.py'
SCRIPT = os.path.join(HERE, SCRIPT_NAME)
SUITE = os.path.join(HERE, SUITE_NAME)

sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla290_variety_records as P  # noqa: E402

APPLY = "        by[slug]['varieties']['recommended'] = [dict(r) for r in RECORDS[slug]]\n"
NAST = "    by[NASTURTIUM]['varieties']['recommended'][NAST_INDEX] = NAST_NEW\n"
DUMP = "    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')\n"


def block(*lines):
    """A replacement for APPLY: build the record list, tamper, then assign."""
    body = "        _rs = [dict(r) for r in RECORDS[slug]]\n"
    for ln in lines:
        body += "        " + ln + "\n"
    return body + "        by[slug]['varieties']['recommended'] = _rs\n"


# (name, anchor, replacement, guard that MUST redden; None = positive control)
MUTATIONS = [
    # --- the defect itself ---
    ("a crop is left in its prose-string shape",
     APPLY,
     "        by[slug]['varieties']['recommended'] = (\n"
     "            list(PREV_ENTRIES[slug]) if slug == 'turnip'\n"
     "            else [dict(r) for r in RECORDS[slug]])\n",
     "test_no_prose_string_survives_in_any_in_scope_crop"),

    ("the whole sentence is kept as the variety name (the reported symptom)",
     APPLY,
     block("for _i, _r in enumerate(_rs):",
           "    _r['name'] = PREV_ENTRIES[slug][_i]"),
     "test_no_name_is_a_sentence"),

    ("celery's Golden Self-Blanching is renamed to a stub",
     APPLY,
     block("if slug == 'celery':",
           "    _rs[3]['name'] = 'Golden'",
           "    _rs[3]['id'] = 'golden'"),
     "test_the_celery_card_reads_as_a_name"),

    # --- the id, which is the compatibility constraint ---
    ("an id is re-keyed to a cultivar named inside the parenthetical, stranding plantings",
     APPLY,
     block("if slug == 'carrot':", "    _rs[0]['id'] = 'scarlet-nantes'"),
     "test_every_id_prefixes_its_stored_legacy_slug"),

    ("an id drifts from slugify(name), desyncing varieties.ts from build-guides-data.mjs",
     APPLY,
     block("if slug == 'carrot':", "    _rs[1]['name'] = 'Danvers Half Long'"),
     "test_every_id_equals_slugify_of_its_own_name"),

    ("two records in one crop share an id",
     APPLY,
     block("if slug == 'potato':", "    _rs[1]['id'] = _rs[0]['id']"),
     "test_ids_are_unique_within_each_crop"),

    ("two records in one crop have their ids swapped (each resolves to the other's entry)",
     APPLY,
     block("if slug == 'potato':",
           "    _rs[0]['id'], _rs[1]['id'] = _rs[1]['id'], _rs[0]['id']"),
     "test_every_legacy_stored_id_still_resolves_to_its_OWN_record"),

    ("an id also claims a DIFFERENT entry's stored slug (longest-prefix ambiguity)",
     APPLY,
     block("if slug == 'carrot':", "    _rs[1]['id'] = 'nantes'"),
     "test_no_id_prefixes_a_DIFFERENT_entrys_legacy_slug"),

    # --- fabricated and lost content ---
    ("a days_to_maturity is invented on every crop's first record",
     APPLY, block("_rs[0]['days_to_maturity'] = 90"),
     "test_every_record_carries_exactly_id_name_note"),

    ("a note is truncated at its first comma, dropping sourced words",
     APPLY, block("_rs[0]['note'] = _rs[0]['note'].split(',')[0] + '.'"),
     "test_no_word_of_the_original_prose_was_dropped"),

    ("a note loses its terminal period",
     APPLY, block("_rs[0]['note'] = _rs[0]['note'].rstrip('.')"),
     "test_every_note_is_a_finished_sentence"),

    ("an em dash reaches the consumer copy",
     APPLY, block("_rs[0]['note'] = _rs[0]['note'].replace(', ', ' \\u2014 ', 1)"),
     "test_no_em_dash_in_the_consumer_copy"),

    ("a record is dropped, merging two entries into one",
     APPLY,
     "        by[slug]['varieties']['recommended'] = [dict(r) for r in RECORDS[slug]][:-1]\n",
     "test_no_entry_count_changed"),

    # --- nasturtium, the out-of-scope crop ---
    ("the marigold copy-paste artifact is left in place",
     NAST, "    pass\n",
     "test_the_marigold_artifact_is_gone_from_nasturtium"),

    ("the nasturtium edit moves the name half, changing a stored variety slug",
     NAST,
     "    by[NASTURTIUM]['varieties']['recommended'][NAST_INDEX] = NAST_NEW.replace(\n"
     "        'Jewel series', 'Jewel series mix')\n",
     "test_the_nasturtium_edit_did_not_move_its_variety_slug"),

    ("nasturtium is converted too, silently re-keying six varieties",
     NAST,
     "    by[NASTURTIUM]['varieties']['recommended'] = [\n"
     "        {'id': 'jewel-series', 'name': 'Jewel series', 'note': 'Converted.'}\n"
     "        for _ in range(6)]\n",
     "test_nasturtium_stays_a_string_crop"),

    # --- blast radius: the PLA-162 family ---
    ("an eleventh string-shape crop is converted in passing",
     NAST,
     "    by['basil']['varieties']['recommended'] = [\n"
     "        {'id': 'genovese', 'name': 'Genovese', 'note': 'Converted.'}]\n" + NAST,
     "test_the_other_string_shape_crops_were_not_converted"),

    ("an unrelated crop gains a key (a pre-only walk cannot see this)",
     NAST, "    by['tomatillo']['_lane_note'] = 'drifted'\n" + NAST,
     "test_nothing_outside_the_eleven_crops_moved"),

    ("the canonical is written pretty-printed instead of COMPACT",
     DUMP, "    out = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')\n",
     "test_canonical_is_still_compact"),

    # --- SENTINEL ---
    ("SENTINEL: the transform does nothing at all",
     "def apply_to(data):\n", "def apply_to(data):\n    return data\n",
     "__SENTINEL__"),

    # --- POSITIVE CONTROL ---
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
                        '--expect-sha', P.BASE_SHA, '--apply'],
                       capture_output=True, text=True)
    return canon, r


def run_suite(workdir):
    """Run the COPY of the suite in the scratch tree so its own REPO resolves to the scratch
    root and `post` is the MUTATED canonical. Pointing at the real suite makes every run read
    live canonical and report a clean sweep -- the PLA-138 failure the sentinel exists for.
    PYTHONPATH reaches the REAL tools dir so promote_fixture still finds the git repo."""
    scratch_suite = os.path.join(workdir, 'tools', SUITE_NAME)
    env = dict(os.environ)
    env['PYTHONPATH'] = HERE
    r = subprocess.run([sys.executable, '-m', 'pytest', scratch_suite, '-q', '--no-header',
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
    # promote_fixture is deliberately NOT copied: it resolves its own REPO from its file
    # location and shells out to git, so a copy in a non-git scratch tree cannot rebuild the
    # pre-state. It is reached through PYTHONPATH instead.
    shutil.copy(SUITE, os.path.join(w, 'tools', SUITE_NAME))
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
            print('HARNESS DEAD: the CLEAN replay does not pass its own suite; mutation '
                  f'results would be noise.\n  failing: {sorted(failing)}')
            return 1
    finally:
        shutil.rmtree(w, ignore_errors=True)
    print('baseline: CLEAN replay green\n')

    results = []
    for name, anchor, replacement, expect in MUTATIONS:
        if anchor not in original:
            print(f'HARNESS DEAD: anchor for {name!r} did not match the promote source.')
            print('  A mutation that cannot be applied is a HARD ERROR, never a survivor.')
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
        print('  Every other result in this run is untrustworthy and is not reported.')
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
