#!/usr/bin/env python3
"""Instrumented mutation harness for the PLA-253 promote suite. PLA-215 convention.

WHY A HARNESS AND NOT A LIST OF SABOTAGE TESTS. PLA-138's original mutation run reported
false vacuity because its harness dedented an already-indented template and silently ran
the CLEAN fixture: every mutation "survived", and the conclusion drawn from that was
exactly backwards. A mutation run that cannot detect its own failure to mutate produces
confident garbage in whichever direction the bug happens to point.

So this harness proves three things about itself before any verdict is trusted:

  MUTATION-APPLIED MARKER (item 2). Every mutated copy gets a literal
  `# MUTATION-APPLIED: <name>` line injected, and the harness asserts BOTH that the marker
  is present in the file it is about to execute AND that the file's bytes differ from the
  original. A mutation whose anchor silently failed to match is a hard error, never a
  survivor.

  SENTINEL (item 2). One mutation is guaranteed-fatal: the promote writes an empty
  document. If the suite does NOT redden on that, the harness is not running what it thinks
  it is running, and it exits `HARNESS DEAD` without reporting any other result.

  POSITIVE CONTROL (item 3). One mutation is guaranteed-invisible: it edits a print string
  the suite never reads. It MUST stay green. That is what separates "the guard is blind"
  from "the injection was a no-op" -- PLA-162's own first injection was invisible for
  exactly this reason and only its control caught it.

Each mutation names the test expected to redden and is run against THAT test in isolation,
so a different test failing elsewhere in the suite cannot be mistaken for the guard working.

Run: python3 tools/mutate_pla253_suite.py
Exit 0 = every mutation caught, control green, sentinel red. Anything else is a failure.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPT = os.path.join(HERE, 'promote_pla253_bt_safety.py')
SUITE = os.path.join(HERE, 'test_promote_pla253_bt_safety.py')

SEASONED = ("Bt kurstaki produces crystal proteins that, once eaten, are activated in the "
            "caterpillar's alkaline gut and destroy the gut lining; it is selective to "
            "caterpillars and practically nontoxic to people, pets, bees, and wildlife, "
            "but it must be ingested and breaks down in a few days.")

WRITE_ANCHOR = "    entry[FIELD] = NEW\n"

# (name, anchor, replacement, test expected to redden or None for the control)
MUTATIONS = [
    ("no-op: the old text is kept",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = OLD\n",
     "test_new_text_is_exactly_the_authored_delivery"),

    ("absolute survives: 'harmless' put back into the replacement",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = NEW + ' It is harmless.'\n",
     "test_defect_a_the_absolute_claim_is_gone_from_the_whole_entry"),

    ("register collapsed: the seasoned string copied into the beginner field",
     "    entry[FIELD] = NEW\n",
     f"    entry[FIELD] = {SEASONED!r}\n",
     "test_register_is_not_collapsed"),

    ("defect (b) unfixed: the non-target caterpillar limit dropped",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = NEW.split(' And it does not tell')[0]\n",
     "test_defect_b_the_butterfly_silence_is_broken"),

    ("precaution dropped: no eye and skin irritation warning",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = NEW.replace(' The spray itself can irritate eyes and skin, so wear "
     "gloves and keep it away from your face.', '')\n",
     "test_the_handling_precaution_the_old_line_omitted_is_present"),

    ("house style: an em dash in consumer copy",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = NEW.replace('Two things to watch.', 'Two things to watch \\u2014')\n",
     "test_new_copy_meets_house_style"),

    ("blast radius, CHANGE: a second control method edited too",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = NEW\n    data['control_methods']['neem_oil']['best_use'] = 'x'\n",
     "test_exactly_one_leaf_changed_and_it_is_the_named_field"),

    ("blast radius, ADD: a new leaf appended (invisible to a pre-only walk)",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = NEW\n    entry['sneaked_in'] = 'x'\n",
     "test_key_sets_are_identical_before_any_value_comparison"),

    ("blast radius, DROP: an existing leaf removed",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = NEW\n    entry.pop('best_use')\n",
     "test_key_sets_are_identical_before_any_value_comparison"),

    ("blast radius, CROP: a crop edited by a top-level-only promote",
     "    entry[FIELD] = NEW\n",
     "    entry[FIELD] = NEW\n    data['crops'][0]['description'] = 'x'\n",
     "test_no_other_crop_or_top_level_key_moved"),

    ("SHA guard removed",
     "    if sha != args.expect_sha:\n",
     "    if False:\n",
     "test_refusal_spec_promote_refuses_a_wrong_base_sha"),

    ("idempotence refusal removed",
     "    if current == NEW:\n",
     "    if False:\n",
     "test_refusal_spec_promote_refuses_when_the_defect_is_already_gone"),

    ("unknown-text refusal removed: overwrites prose it never read",
     "    if current != OLD:\n",
     "    if False:\n",
     "test_refusal_spec_promote_refuses_text_it_was_not_written_against"),

    ("compact formatting broken: indent=2",
     "    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')\n",
     "    out = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')\n",
     "test_compact_formatting_preserved"),

    # POSITIVE CONTROL -- must stay GREEN.
    ("CONTROL (must stay green): a print string the suite never reads",
     "    print(f'replaced control_methods.{METHOD}.{FIELD}')\n",
     "    print('a message no guard inspects')\n",
     None),
]

SENTINEL = ("SENTINEL (must redden): the promote writes an empty document",
            "    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')\n",
            "    out = json.dumps({}, ensure_ascii=False, separators=(',', ':')).encode('utf-8')\n",
            "test_new_text_is_exactly_the_authored_delivery")

ORIG = open(SCRIPT, encoding='utf-8').read()


def apply_mutation(name, anchor, repl):
    """Write the mutated script. Hard-errors unless the mutation demonstrably landed."""
    if ORIG.count(anchor) != 1:
        raise SystemExit(f'HARNESS DEAD: anchor for {name!r} matches {ORIG.count(anchor)} '
                         f'times, expected exactly 1. Refusing to report survivors from a '
                         f'run whose mutations may never have been applied.')
    marked = repl + f'    # MUTATION-APPLIED: {name}\n'
    mutated = ORIG.replace(anchor, marked, 1)
    if mutated == ORIG:
        raise SystemExit(f'HARNESS DEAD: mutation {name!r} produced an identical file.')
    with open(SCRIPT, 'w', encoding='utf-8') as fh:
        fh.write(mutated)
    on_disk = open(SCRIPT, encoding='utf-8').read()
    if f'# MUTATION-APPLIED: {name}' not in on_disk or on_disk == ORIG:
        raise SystemExit(f'HARNESS DEAD: marker missing from the file about to be executed '
                         f'({name!r}).')
    return True


def run(test):
    r = subprocess.run([sys.executable, '-m', 'pytest', SUITE, '-q', '-x', '-k', test],
                       cwd=REPO, capture_output=True, text=True)
    return r.returncode != 0, r.stdout


def restore():
    with open(SCRIPT, 'w', encoding='utf-8') as fh:
        fh.write(ORIG)


def main():
    backup = os.path.join(tempfile.mkdtemp(prefix='pla253_mut_'), 'orig.py')
    shutil.copy(SCRIPT, backup)
    results, control_ok = [], None
    try:
        # ---- liveness first: if the sentinel does not redden, report nothing else ----
        name, anchor, repl, test = SENTINEL
        apply_mutation(name, anchor, repl)
        red, _ = run(test)
        restore()
        if not red:
            print('HARNESS DEAD: the sentinel mutation did not redden the suite. '
                  'The harness is not running the code it thinks it is; no survivor '
                  'verdict from this run is trustworthy.')
            return 2
        print(f'  LIVENESS OK   {name} -> reddened {test}')

        for name, anchor, repl, test in MUTATIONS:
            apply_mutation(name, anchor, repl)
            if test is None:  # positive control
                red, out = run('not test_pre_state and not test_claims_are_supported')
                restore()
                control_ok = not red
                print(f'  {"CONTROL OK" if control_ok else "CONTROL FAILED"}    {name}')
                if not control_ok:
                    print(out[-1500:])
                continue
            red, out = run(test)
            restore()
            results.append((name, test, red))
            print(f'  {"CAUGHT  " if red else "SURVIVED"}  {name}  -> {test}")'[:-2])
            if not red:
                print(out[-1200:])
    finally:
        shutil.copy(backup, SCRIPT)

    assert open(SCRIPT, encoding='utf-8').read() == ORIG, 'restore failed'
    survivors = [n for n, _, red in results if not red]
    print()
    print(f'mutations: {len(results)} | caught: {len(results) - len(survivors)} | '
          f'survivors: {len(survivors)}')
    print(f'positive control green: {control_ok}')
    if survivors:
        print('SURVIVORS:')
        for s in survivors:
            print('  -', s)
        return 1
    if not control_ok:
        print('POSITIVE CONTROL FAILED -- the suite reddens on an injection it should not '
              'see, so a "caught" verdict elsewhere may be noise.')
        return 1
    print('ALL MUTATIONS CAUGHT, control green, sentinel red -- PLA-215 items 1-3 met.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
