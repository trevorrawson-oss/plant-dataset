#!/usr/bin/env python3
"""Instrumented mutation harness for the PLA-253 bee-hedge suite. PLA-215 convention.

Same three self-checks as the first pass's harness, for the same reason (PLA-138's run
reported false vacuity because its harness silently ran the CLEAN fixture):

  MUTATION-APPLIED MARKER  every mutated copy carries `# MUTATION-APPLIED: <name>`, asserted
                           present in the file about to execute, and asserted to differ from
                           the original. A mutation whose anchor failed to match is a hard
                           error, never a survivor.
  SENTINEL                 one guaranteed-fatal mutation must redden, or the run exits
                           HARNESS DEAD and reports nothing else.
  POSITIVE CONTROL         one guaranteed-invisible mutation must stay green, so "the guard
                           is blind" is distinguishable from "the injection was a no-op".

TWO MUTATION FAMILIES ARE SPECIFIC TO A SECOND PASS and do not exist in the first pass's
harness: mutations that UNDO pass one (revert to the "harmless" text, drop the precaution),
and mutations that EDIT MORE THAN THE CLAUSE (reflow the surrounding sentence). Those are
the two ways a small wording fix on freshly-rewritten prose goes wrong.

Run: python3 tools/mutate_pla253_bee_hedge_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPT = os.path.join(HERE, 'promote_pla253_bt_bee_hedge.py')
SUITE = os.path.join(HERE, 'test_promote_pla253_bt_bee_hedge.py')

SEASONED = ("Bt kurstaki produces crystal proteins that, once eaten, are activated in the "
            "caterpillar's alkaline gut and destroy the gut lining; it is selective to "
            "caterpillars and practically nontoxic to people, pets, bees, and wildlife, "
            "but it must be ingested and breaks down in a few days.")
PASS_ONE_OLD = ("Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with "
                "it, the Bt proteins wreck its gut and it stops feeding and dies. It is "
                "harmless to people, pets, and bees.")

WRITE = "    entry[FIELD] = NEW\n"

MUTATIONS = [
    ("no-op: the un-hedged clause is kept",
     WRITE, "    entry[FIELD] = PREV\n",
     "test_new_text_is_exactly_the_authored_delivery"),

    ("still absolute: a different absolute swapped in ('so bees are safe')",
     WRITE, "    entry[FIELD] = PREV.replace(CLAUSE_OLD, 'so bees are safe')\n",
     "test_the_hedge_matches_npics_register_for_the_active_ingredient"),

    ("absolute survives elsewhere in the field",
     WRITE, "    entry[FIELD] = NEW + ' Bees are not at risk.'\n",
     "test_the_absolute_is_gone_and_the_hedge_is_present"),

    # --- second-pass family 1: edits more than the clause ---
    ("reflow: the sentence AFTER the clause is quietly re-punctuated",
     WRITE, "    entry[FIELD] = NEW.replace('Two things to watch.', 'Two things to watch:')\n",
     "test_the_change_is_exactly_one_clause_and_every_other_byte_is_identical"),

    ("reflow: the sentence BEFORE the clause is quietly reworded",
     WRITE, "    entry[FIELD] = NEW.replace('a natural soil bacterium', 'a common soil bacterium')\n",
     "test_the_change_is_exactly_one_clause_and_every_other_byte_is_identical"),

    # --- second-pass family 2: undoes pass one ---
    ("UNDO: the field reverted to the pre-PLA-253 'harmless' text",
     WRITE, f"    entry[FIELD] = {PASS_ONE_OLD!r}\n",
     "test_pass_one_gains_all_survive"),

    ("UNDO: hedged, but the eye-and-skin precaution dropped",
     WRITE,
     "    entry[FIELD] = NEW.replace(' The spray itself can irritate eyes and skin, so wear "
     "gloves and keep it away from your face.', '')\n",
     "test_pass_one_gains_all_survive"),

    ("UNDO: hedged, but the non-target caterpillar limit dropped",
     WRITE, "    entry[FIELD] = NEW.split(' And it does not tell')[0]\n",
     "test_pass_one_gains_all_survive"),

    ("register collapsed: the seasoned string copied into the beginner field",
     WRITE, f"    entry[FIELD] = {SEASONED!r}\n",
     "test_register_is_not_collapsed"),

    ("house style: an em dash in consumer copy",
     WRITE, "    entry[FIELD] = NEW.replace('Two things to watch.', 'Two things to watch \\u2014')\n",
     "test_new_copy_meets_house_style"),

    ("blast radius, CHANGE: a second control method edited too",
     WRITE, "    entry[FIELD] = NEW\n    data['control_methods']['neem_oil']['best_use'] = 'x'\n",
     "test_exactly_one_leaf_changed_and_it_is_the_named_field"),

    ("blast radius, ADD: a new leaf appended",
     WRITE, "    entry[FIELD] = NEW\n    entry['sneaked_in'] = 'x'\n",
     "test_key_sets_are_identical_before_any_value_comparison"),

    ("blast radius, DROP: an existing leaf removed",
     WRITE, "    entry[FIELD] = NEW\n    entry.pop('best_use')\n",
     "test_key_sets_are_identical_before_any_value_comparison"),

    ("blast radius, CROP: a crop edited by a top-level-only promote",
     WRITE, "    entry[FIELD] = NEW\n    data['crops'][0]['description'] = 'x'\n",
     "test_no_other_crop_or_top_level_key_moved"),

    ("SHA guard removed",
     "    if sha != args.expect_sha:\n", "    if False:\n",
     "test_refusal_spec_promote_refuses_a_wrong_base_sha"),

    ("already-hedged refusal removed",
     "    if current == NEW:\n", "    if False:\n",
     "test_refusal_spec_promote_refuses_when_already_hedged"),

    ("unknown-text refusal removed: would half-apply a hedge to the 'harmless' sentence",
     "    if current != PREV:\n", "    if False:\n",
     "test_refusal_spec_promote_refuses_text_it_was_not_written_against"),

    ("compact formatting broken: indent=2",
     "    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')\n",
     "    out = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')\n",
     "test_compact_formatting_preserved"),

    ("CONTROL (must stay green): a print string the suite never reads",
     "    print(f'hedged control_methods.{METHOD}.{FIELD}')\n",
     "    print('a message no guard inspects')\n",
     None),
]

SENTINEL = ("SENTINEL (must redden): the promote writes an empty document",
            "    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')\n",
            "    out = json.dumps({}, ensure_ascii=False, separators=(',', ':')).encode('utf-8')\n",
            "test_new_text_is_exactly_the_authored_delivery")

ORIG = open(SCRIPT, encoding='utf-8').read()


def apply_mutation(name, anchor, repl):
    if ORIG.count(anchor) != 1:
        raise SystemExit(f'HARNESS DEAD: anchor for {name!r} matches {ORIG.count(anchor)} '
                         f'times, expected exactly 1.')
    mutated = ORIG.replace(anchor, repl + f'    # MUTATION-APPLIED: {name}\n', 1)
    if mutated == ORIG:
        raise SystemExit(f'HARNESS DEAD: mutation {name!r} produced an identical file.')
    with open(SCRIPT, 'w', encoding='utf-8') as fh:
        fh.write(mutated)
    on_disk = open(SCRIPT, encoding='utf-8').read()
    if f'# MUTATION-APPLIED: {name}' not in on_disk or on_disk == ORIG:
        raise SystemExit(f'HARNESS DEAD: marker missing from the file about to run ({name!r}).')


def run(test):
    r = subprocess.run([sys.executable, '-m', 'pytest', SUITE, '-q', '-x', '-k', test],
                       cwd=REPO, capture_output=True, text=True)
    return r.returncode != 0, r.stdout


def restore():
    with open(SCRIPT, 'w', encoding='utf-8') as fh:
        fh.write(ORIG)


def main():
    backup = os.path.join(tempfile.mkdtemp(prefix='pla253_hedge_mut_'), 'orig.py')
    shutil.copy(SCRIPT, backup)
    results, control_ok = [], None
    try:
        name, anchor, repl, test = SENTINEL
        apply_mutation(name, anchor, repl)
        red, _ = run(test)
        restore()
        if not red:
            print('HARNESS DEAD: the sentinel mutation did not redden the suite. No survivor '
                  'verdict from this run is trustworthy.')
            return 2
        print(f'  LIVENESS OK   {name} -> reddened {test}')

        for name, anchor, repl, test in MUTATIONS:
            apply_mutation(name, anchor, repl)
            if test is None:
                red, out = run('not test_base_is_the_first and not test_pre_state and '
                               'not test_the_hedge_matches')
                restore()
                control_ok = not red
                print(f'  {"CONTROL OK" if control_ok else "CONTROL FAILED"}    {name}')
                if not control_ok:
                    print(out[-1500:])
                continue
            red, out = run(test)
            restore()
            results.append((name, test, red))
            print(f'  {"CAUGHT  " if red else "SURVIVED"}  {name}  -> {test}')
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
        print('POSITIVE CONTROL FAILED.')
        return 1
    print('ALL MUTATIONS CAUGHT, control green, sentinel red -- PLA-215 items 1-3 met.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
