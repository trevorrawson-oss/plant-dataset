#!/usr/bin/env python3
"""Instrumented mutation harness for the PLA-253 nematode-anchor suite. PLA-215 convention.

Mutations are injected into a SCRATCH COPY of the promote script, and the suite is run against
a canonical rebuilt by replaying that mutated script from the pinned base -- never against the
live canonical, and never by editing the live script. That is the only arrangement in which a
guard is shown to catch a defect it would actually have faced.

The three self-checks the convention requires (PLA-138's harness dedented an already-indented
template, silently ran the CLEAN fixture, and reported every mutation as surviving):

  MUTATION-APPLIED MARKER  every mutated copy carries `# MUTATION-APPLIED: <name>`, asserted
                           present in the file about to execute and asserted to differ from
                           the original. An anchor that did not match is a HARD ERROR, never
                           a survivor.
  SENTINEL                 one guaranteed-fatal mutation must redden, or the run exits
                           HARNESS DEAD and reports nothing else.
  POSITIVE CONTROL         one guaranteed-invisible mutation must stay GREEN, so "the guard is
                           blind" stays distinguishable from "the injection was a no-op".

THE FAMILY THIS PASS NEEDS THAT THE Bt PASSES DID NOT: this promote ADDS things -- a catalog
id and a source id. Additions are exactly what a blast-radius guard that walks only the PRE
state cannot see (all four PLA-162 defects). Four mutations below plant additions and drops on
purpose to prove the key-set assertions are load-bearing.

Run: python3 tools/mutate_pla253_nematode_suite.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPT = os.path.join(HERE, 'promote_pla253_nematode_anchor.py')
SUITE = os.path.join(HERE, 'test_promote_pla253_nematode_anchor.py')

sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla253_nematode_anchor as P  # noqa: E402

APPLY_ANCHOR = "    entry['pros'][1] = NEW_PRO_1\n"
CATALOG_ANCHOR = "    catalog[NEW_SOURCE_ID] = json.loads(json.dumps(NEW_CATALOG_ENTRY))\n"
SOURCES_ANCHOR = ("    if NEW_SOURCE_ID not in entry['sources']:\n"
                  "        entry['sources'].append(NEW_SOURCE_ID)\n")

# (name, anchor, replacement, guard that MUST redden; None = positive control)
MUTATIONS = [
    ("the pro is left in its unanchored wording",
     APPLY_ANCHOR, "    entry['pros'][1] = PREV_PRO_1\n",
     "test_the_pro_is_exactly_the_authored_delivery"),

    ("the beginner line narrows back to people-and-pets, dropping plants",
     "    entry['how_it_works_beginner'] = NEW_BEGINNER\n",
     "    entry['how_it_works_beginner'] = NEW_BEGINNER.replace(' people, pets, or plants', ' people or pets')\n",
     "test_the_claim_names_all_three_protected_classes"),

    ("the EPA exemption sentence is dropped from the beginner line",
     "    entry['how_it_works_beginner'] = NEW_BEGINNER\n",
     "    entry['how_it_works_beginner'] = NEW_BEGINNER.split(' The EPA considers')[0]\n",
     "test_the_beginner_line_is_exactly_the_authored_delivery"),

    ("an em dash reaches the consumer copy",
     "    entry['how_it_works_beginner'] = NEW_BEGINNER\n",
     "    entry['how_it_works_beginner'] = NEW_BEGINNER.replace('. The EPA', ' \\u2014 the EPA')\n",
     "test_no_em_dash_in_the_consumer_copy"),

    # --- the anchor itself ---
    ("the catalog entry is minted WITHOUT a title (A54's mint-time defect)",
     CATALOG_ANCHOR,
     "    _e = json.loads(json.dumps(NEW_CATALOG_ENTRY)); _e.pop('title', None)\n"
     "    catalog[NEW_SOURCE_ID] = _e\n",
     "test_the_new_catalog_entry_is_titled_at_mint_time"),

    ("the catalog entry is minted at the wrong tier",
     CATALOG_ANCHOR,
     "    _e = json.loads(json.dumps(NEW_CATALOG_ENTRY)); _e['tier'] = 'T2'\n"
     "    catalog[NEW_SOURCE_ID] = _e\n",
     "test_the_new_source_is_in_the_catalog_as_t1"),

    ("the prose is rewritten but the source is never cited (the unanchored claim survives)",
     SOURCES_ANCHOR, "    pass\n",
     "test_the_method_cites_the_new_source_and_still_cites_uc_ipm"),

    ("the safety source REPLACES the efficacy source instead of joining it",
     SOURCES_ANCHOR, "    entry['sources'] = [NEW_SOURCE_ID]\n",
     "test_the_method_cites_the_new_source_and_still_cites_uc_ipm"),

    ("anchoring_urls drifts out of step with sources",
     "    entry['anchoring_urls'][NEW_SOURCE_ID] = {\n"
     "        'url': NEW_CATALOG_ENTRY['url'],\n"
     "        'verified': VERIFIED,\n"
     "    }\n",
     "    pass\n",
     "test_anchoring_urls_match_sources_exactly"),

    ("the UC IPM efficacy anchor is silently re-verified to today",
     "    entry['anchoring_urls'][NEW_SOURCE_ID] = {\n",
     "    entry['anchoring_urls'][KEPT_SOURCE_ID]['verified'] = VERIFIED\n"
     "    entry['anchoring_urls'][NEW_SOURCE_ID] = {\n",
     "test_the_uc_ipm_anchor_is_untouched"),

    # --- ADDITIONS AND DROPS: the PLA-162 family this promote is exposed to ---
    ("a SECOND catalog id rides along on the mint (an addition)",
     CATALOG_ANCHOR,
     CATALOG_ANCHOR + "    catalog['ghost_source'] = {'id': 'ghost_source', 'tier': 'T1'}\n",
     "test_nothing_else_in_the_dataset_moved"),

    ("an unrelated catalog entry is DROPPED",
     CATALOG_ANCHOR, CATALOG_ANCHOR + "    catalog.pop('clemson_hgic', None)\n",
     "test_nothing_else_in_the_dataset_moved"),

    ("a new key is ADDED to the method (a pre-only walk cannot see this)",
     APPLY_ANCHOR, APPLY_ANCHOR + "    entry['internal_note'] = 'lane assignment'\n",
     "test_nothing_else_in_the_dataset_moved"),

    ("pros gains a third entry instead of pros[1] being rewritten",
     APPLY_ANCHOR, "    entry['pros'].append(NEW_PRO_1)\n",
     "test_the_pros_list_kept_its_length_and_its_other_entry"),

    ("another control method is edited in passing",
     APPLY_ANCHOR,
     APPLY_ANCHOR + "    data['control_methods']['bt']['best_use'] = 'drifted'\n",
     "test_no_other_control_method_was_touched"),

    ("a crop is edited in passing",
     APPLY_ANCHOR,
     APPLY_ANCHOR + "    data['crops'][0]['description_beginner'] = 'drifted'\n",
     "test_no_crop_was_touched"),

    # --- SENTINEL ---
    ("SENTINEL: the transform does nothing at all",
     "def apply_to(data):\n", "def apply_to(data):\n    return data\n",
     "__SENTINEL__"),

    # --- POSITIVE CONTROL ---
    ("POSITIVE CONTROL: a comment inside the transform is reworded",
     "    entry = data['control_methods'][METHOD]\n",
     "    # reworded comment, no behavior change\n    entry = data['control_methods'][METHOD]\n",
     None),
]


def build_canonical(script_path, workdir):
    """Replay the (possibly mutated) promote from the pinned base into a scratch canonical."""
    base = promote_fixture.pre_state(P.BASE_SHA)
    canon = os.path.join(workdir, 'crops_data_final.json')
    with open(canon, 'wb') as fh:
        fh.write(base if isinstance(base, bytes) else base.encode('utf-8'))
    r = subprocess.run([sys.executable, script_path, '--canonical', canon,
                        '--expect-sha', P.BASE_SHA, '--apply'],
                       capture_output=True, text=True)
    return canon, r


def run_suite(workdir, canon_path):
    """Run the COPY of the suite that lives in the scratch tree, so its own
    `REPO = dirname(dirname(__file__))` resolves to the scratch root and `post` is the MUTATED
    canonical. Passing the real suite path instead makes every run read the live canonical and
    report a clean sweep -- which is precisely what the sentinel caught on the first run of
    this harness, and precisely the PLA-138 failure the sentinel exists for.

    PYTHONPATH points at the REAL tools dir so `promote_fixture` (which resolves its own REPO
    from its own file location and shells out to git) still finds the git repo. The scratch
    tools dir is searched FIRST by the suite, so `promote_pla253_nematode_anchor` resolves to
    the mutated copy while `promote_fixture` falls through to the real one."""
    scratch_suite = os.path.join(workdir, 'tools', os.path.basename(SUITE))
    env = dict(os.environ)
    env['PYTHONPATH'] = HERE
    r = subprocess.run([sys.executable, '-m', 'pytest', scratch_suite, '-q', '--no-header',
                        '-p', 'no:cacheprovider', '--rootdir', workdir],
                       capture_output=True, text=True, env=env, cwd=workdir)
    failing = set()
    for line in (r.stdout + r.stderr).splitlines():
        if line.startswith('FAILED '):
            failing.add(line.split(' ', 1)[1].split(' ')[0].split('::')[-1])
    return r.returncode == 0, failing, r.stdout + r.stderr


def main():
    original = open(SCRIPT).read()

    # The suite reads CANONICAL from its own module constant, so the scratch tree must BE a
    # repo-shaped directory: tools/ + crops_data_final.json at its root.
    def make_tree():
        w = tempfile.mkdtemp()
        os.makedirs(os.path.join(w, 'tools'), exist_ok=True)
        # promote_fixture is deliberately NOT copied: it resolves its own REPO from its
        # file location and shells out to git, so a copy in a non-git scratch tree cannot
        # rebuild the pre-state. It is reached through PYTHONPATH instead.
        shutil.copy(os.path.join(HERE, 'test_promote_pla253_nematode_anchor.py'),
                    os.path.join(w, 'tools', 'test_promote_pla253_nematode_anchor.py'))
        return w

    # ---- baseline: the CLEAN replay must be green ----
    w = make_tree()
    try:
        shutil.copy(SCRIPT, os.path.join(w, 'tools', 'promote_pla253_nematode_anchor.py'))
        canon, r = build_canonical(os.path.join(w, 'tools', 'promote_pla253_nematode_anchor.py'), w)
        if r.returncode != 0:
            print('HARNESS DEAD: the CLEAN replay did not apply.')
            print(r.stdout, r.stderr)
            return 1
        ok, failing, out = run_suite(w, canon)
        if not ok:
            print('HARNESS DEAD: the CLEAN replay does not pass its own suite; mutation '
                  'results would be noise.')
            print(f'  failing: {sorted(failing)}')
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
            mpath = os.path.join(w, 'tools', 'promote_pla253_nematode_anchor.py')
            with open(mpath, 'w') as fh:
                fh.write(mutated)
            on_disk = open(mpath).read()
            assert marker in on_disk, f'MUTATION-APPLIED marker absent for {name!r}'
            assert on_disk.replace(marker, '', 1) != original, \
                f'mutated copy is byte-identical to the original for {name!r}'

            canon, r = build_canonical(mpath, w)
            if r.returncode != 0:
                # A mutation the promote's own preconditions reject never reaches the suite.
                # That is a REFUSAL-SPEC pass, not a survivor -- record it as such.
                results.append(('REFUSED', name, True, f'promote refused it: {r.stderr.strip().splitlines()[0][:90]}'))
                continue
            ok, failing, out = run_suite(w, canon)
        finally:
            shutil.rmtree(w, ignore_errors=True)

        if expect is None:
            results.append(('CONTROL', name, ok,
                            'GREEN (as required)' if ok else f'REDDENED -- {sorted(failing)}'))
        elif expect == '__SENTINEL__':
            results.append(('SENTINEL', name, not ok,
                            f'caught by {sorted(failing)[:3]}' if failing else 'SURVIVED'))
        else:
            hit = expect in failing
            results.append(('MUTATION', name, hit,
                            f'caught by {sorted(failing)[:3]}' if failing else 'SURVIVED'))

    sentinel = [r for r in results if r[0] == 'SENTINEL']
    if not sentinel or not sentinel[0][2]:
        print('HARNESS DEAD: the sentinel mutation did not redden the suite.')
        print('  Every other result in this run is untrustworthy and is not reported.')
        return 1
    control = [r for r in results if r[0] == 'CONTROL']
    control_ok = all(r[2] for r in control)

    real = [r for r in results if r[0] in ('MUTATION', 'REFUSED')]
    caught = [r for r in real if r[2]]
    survivors = [r for r in real if not r[2]]

    for kind, name, good, detail in results:
        print(f"  [{'OK  ' if good else 'FAIL'}] {kind:<8} {name}\n           -> {detail}")

    print('\nsentinel: reddened (harness live)')
    print(f"positive control: {'held green' if control_ok else 'REDDENED -- suite over-asserts'}")
    print(f'mutations: {len(caught)}/{len(real)} CAUGHT, {len(survivors)} survivor(s)')
    for _, name, _, _ in survivors:
        print(f'  SURVIVOR: {name}')
    return 0 if (len(caught) == len(real) and control_ok) else 1


if __name__ == '__main__':
    sys.exit(main())
