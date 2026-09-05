#!/usr/bin/env python3
"""mutate_pla8_batch26_suite -- mutation harness for the PLA-8 batch 26 promote suite.

BUILT TO THE PLA-215 BAR. It injects one defect per guard family into a SCRATCH COPY of the promote
source, runs the suite's own drivers against the mutated copy, and requires each to go RED. A
mutation that survives is a guard the suite does not actually test.

THE LIVENESS DEFENSE, and why it is not optional. PLA-138's harness dedented an already-indented
template, silently ran the CLEAN fixture, and reported every mutation as surviving -- a completely
dead harness producing a confident, wrong report. So this one:

  1. Writes a `MUTATION-APPLIED` marker into the mutated file and asserts it is present before
     running anything. A mutation that did not textually apply is a HARNESS failure, not a survivor.
  2. Asserts the mutated bytes actually differ from the clean bytes.
  3. Runs a SENTINEL mutation that MUST redden. If the sentinel survives, the harness is not
     measuring anything and the run exits `HARNESS DEAD` rather than reporting results.
  4. Runs a POSITIVE CONTROL: the unmutated copy must go GREEN. A harness where everything reddens
     is as useless as one where nothing does, and it is the likelier failure when the scratch tree
     is wired up wrong.

WHY PER-MUTATION TEST SELECTION. The full suite takes about three minutes, mostly in the precedent
copy walk over ~28000 comparisons. Each mutation names the driver that SHOULD catch it and only that
driver is run, which keeps the harness usable. The selection is also the assertion: a mutation is
caught only if ITS OWN driver reddens, not if some other test happens to fall over. That is the
"assert the whole sentence, not a shared fragment" rule applied at the harness level.

Usage:
    mutate_pla8_batch26_suite.py             # all families
    mutate_pla8_batch26_suite.py --family X  # one family
    mutate_pla8_batch26_suite.py --list
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_pla8_batch26.py"
SUITE = "test_promote_pla8_batch26.py"
MARKER = "# MUTATION-APPLIED"

# (family, name, old, new, pytest -k selector)
MUTATIONS = [
    # ---- reconcile -------------------------------------------------------------------------
    ("reconcile", "unaccounted_canonical_problem_ignored",
     'for key in sorted(canon - set(consumed)):',
     'for key in sorted(set()):  ' + MARKER,
     "test_unaccounted_canonical_problem_is_refused"),
    ("reconcile", "phantom_source_ignored",
     'if key not in canon:\n            bad.append(f"PHANTOM SOURCE:',
     'if False:  ' + MARKER + '\n            bad.append(f"PHANTOM SOURCE:',
     "test_phantom_source_is_refused"),
    ("reconcile", "retire_and_use_contradiction_ignored",
     'if key in consumed:\n            bad.append(f"CONTRADICTION:',
     'if False:  ' + MARKER + '\n            bad.append(f"CONTRADICTION:',
     "test_retiring_something_also_used_is_refused"),

    # ---- spec match ------------------------------------------------------------------------
    ("spec", "pinned_type_and_severity_unchecked",
     'for k in ("name", "id", "type", "severity"):',
     'for k in ("name", "id"):  ' + MARKER,
     "test_reverted_type_is_refused"),
    ("spec", "entry_count_unchecked",
     'if len(want) != len(got):',
     'if False:  ' + MARKER + ' len(want) != len(got):',
     "test_dropped_entry_is_refused or test_appended_ghost_entry_is_refused"),

    # ---- ladder ----------------------------------------------------------------------------
    ("ladder", "empty_ladder_allowed",
     'if not isinstance(ladder, list) or not ladder:',
     'if not isinstance(ladder, list) and False:  ' + MARKER,
     "test_empty_ladder_is_refused"),
    ("ladder", "tier_inversion_allowed",
     'if rank < last:',
     'if False:  ' + MARKER + ' rank < last:',
     "test_tier_inversion_is_refused"),
    ("ladder", "applies_to_incoherence_allowed",
     'if not (applies & TYPE_TARGETS[t]):',
     'if False:  ' + MARKER + ' not (applies & TYPE_TARGETS[t]):',
     "test_method_not_reaching_type_is_refused"),
    ("ladder", "em_dash_allowed",
     'if "—" in v or "–" in v:',
     'if False:  ' + MARKER,
     "test_em_dash_is_refused"),
    ("ladder", "machinery_vocabulary_allowed",
     'if LADDER_VOCAB.search(v):',
     'if False:  ' + MARKER + ' LADDER_VOCAB.search(v):',
     "test_machinery_vocabulary_in_a_note_is_refused"),
    ("ladder", "identical_registers_allowed",
     'if r["note_beginner"].strip() == r["note_seasoned"].strip():',
     'if False:  ' + MARKER,
     "test_identical_registers_are_refused"),
    ("ladder", "repeated_method_allowed",
     'if r["method"] in seen:',
     'if False:  ' + MARKER + ' r["method"] in seen:',
     "test_repeated_method_is_refused"),

    # ---- corrections -----------------------------------------------------------------------
    ("corrections", "split_limb_may_inherit_bundle_prose",
     'missing = [f for f in PROSE_FIELDS if f not in declared]',
     'missing = []  ' + MARKER,
     "test_split_limb_inheriting_bundle_prose_is_refused"),
    ("corrections", "correction_anchor_not_required",
     'for k in ("new", "why", "anchor"):',
     'for k in ("new",):  ' + MARKER,
     "test_correction_without_anchor_is_refused or test_correction_without_reason_is_refused"),
    ("corrections", "name_correction_may_disagree_with_pin",
     'if (corr or {}).get("new") != p["name"]:',
     'if False:  ' + MARKER,
     "test_name_correction_disagreeing_with_the_pin_is_refused"),
    ("corrections", "machinery_vocabulary_allowed_in_corrections",
     'if LADDER_VOCAB.search(corr["new"]):',
     'if False:  ' + MARKER + ' LADDER_VOCAB.search(corr["new"]):',
     "test_machinery_vocabulary_in_a_correction_is_refused"),

    # ---- sources ---------------------------------------------------------------------------
    ("sources", "unadmitted_source_key_allowed",
     'if s not in cat:',
     'if False:  ' + MARKER + ' s not in cat:',
     "test_unadmitted_source_key_is_refused"),
    ("sources", "anchor_without_source_allowed",
     'if k not in srcs:',
     'if False:  ' + MARKER + ' k not in srcs:',
     "test_anchor_without_a_matching_source_is_refused"),

    # ---- copy / echo -----------------------------------------------------------------------
    ("copy", "threshold_raised_out_of_reach",
     'COPY_THRESHOLD = 0.70',
     'COPY_THRESHOLD = 1.01  ' + MARKER,
     "test_verbatim_lift_from_a_shipped_note_is_refused"),
    ("copy", "metric_made_one_directional",
     'return max(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(),\n               difflib.SequenceMatcher(None, b, a, autojunk=False).ratio())',
     'return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()  ' + MARKER,
     "test_symmetric_metric_is_actually_symmetric"),
    # BOTH ORDERS, and pointed at the driver that can actually see it. The first version mutated
    # only the forward order and named the verbatim-lift driver, so `_sym` still returned an
    # undeflated score from the untouched reverse order AND a verbatim copy scores 1.0 either way.
    # It survived for two independent reasons, neither of which was a real gap in the guard.
    ("copy", "autojunk_re_enabled",
     'return max(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(),\n               difflib.SequenceMatcher(None, b, a, autojunk=False).ratio())',
     'return max(difflib.SequenceMatcher(None, a, b).ratio(),  ' + MARKER + '\n               difflib.SequenceMatcher(None, b, a).ratio())',
     "test_autojunk_is_disabled_and_it_matters"),
    ("echo", "house_exemption_swallows_everything",
     'house = {s for s, n in donors.items() if n > 1}',
     'house = set(donors)  ' + MARKER,
     "test_house_phrasing_is_exempt_but_a_single_donor_lift_is_not"),
    ("echo", "whole_note_echo_allowed",
     'if v in whole:',
     'if False:  ' + MARKER + ' v in whole:',
     "test_whole_note_echo_is_never_exempt"),
    ("echo", "intra_batch_twins_allowed",
     'if key in seen and seen[key] != crop:',
     'if False:  ' + MARKER,
     "test_cross_crop_twin_note_is_refused"),

    ("echo", "recombination_run_threshold_raised",
     'MIN_RUN_GRAMS = 3',
     'MIN_RUN_GRAMS = 999  ' + MARKER,
     "test_two_donor_recombination_is_refused"),
    ("echo", "recombination_overlap_brake_removed",
     'if a0 < b1 and b0 < a1:',
     'if False:  ' + MARKER + ' a0 < b1 and b0 < a1:',
     "test_nested_donor_runs_are_not_recombination"),

    # ---- temperature -----------------------------------------------------------------------
    ("temperature", "unwarranted_figure_allowed",
     'if num not in re.sub(r"\\s+", "", blob) and num not in re.sub(r"\\s+", "", meth):',
     'if False:  ' + MARKER,
     "test_unwarranted_temperature_figure_is_refused"),

    # ---- retirements (NEW: array duplicates) ----------------------------------------------
    ("retire", "undeclared_duplicate_shape_allowed",
     'if r["field"] != "pests" or dup.get("field") != "diseases" or dup.get("name") != r["name"]:',
     'if False:  ' + MARKER,
     "test_retirement_not_declared_as_duplicate_is_refused"),
    ("retire", "missing_diseases_twin_allowed",
     'if twin is None:\n            raise SystemExit(f"REFUSED: retirement {r[\'crop\']}/{r[\'name\']!r} names a diseases[] "',
     'if False:  ' + MARKER + '\n            raise SystemExit(f"REFUSED: retirement {r[\'crop\']}/{r[\'name\']!r} names a diseases[] "',
     "test_retirement_with_no_diseases_twin_is_refused"),
    ("retire", "uncarried_twin_allowed",
     'if (r["crop"], "diseases", r["name"]) not in carried:',
     'if False:  ' + MARKER,
     "test_retirement_whose_twin_is_not_carried_is_refused"),
    ("retire", "real_pest_retirement_allowed",
     'if gone.get("type") not in ("fungal", "bacterial", "viral", "disease"):',
     'if False:  ' + MARKER,
     "test_retirement_of_a_real_pest_is_refused"),

    # ---- types (NEW: mixed situation, pinned per row) -------------------------------------
    ("types", "pre_type_unchecked",
     'if src.get("type") != pre:',
     'if False:  ' + MARKER + ' src.get("type") != pre:',
     "test_pre_type_mismatch_is_refused"),
    ("types", "coarse_not_upgraded_allowed",
     'if post == pre:\n                raise SystemExit(f"REFUSED: {crop}/{row[\'name\']!r} type was not upgraded off "',
     'if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: {crop}/{row[\'name\']!r} type was not upgraded off "',
     "test_coarse_type_not_upgraded_is_refused"),
    ("types", "silent_retype_allowed",
     'if post != pre and not row.get("retype_reason"):',
     'if False:  ' + MARKER,
     "test_fine_type_retyped_without_reason_is_refused"),
    ("types", "mixed_premise_removed",
     'if upgraded == 0 or carried == 0:',
     'if False:  ' + MARKER,
     "test_type_situation_must_be_mixed"),

    # ---- PLA-457 hold (NEW) --------------------------------------------------------------
    ("hold", "interval_predicate_disabled",
     'if SULFUR.search(s) and OIL.search(s) and DURATION.search(s):',
     'if False:  ' + MARKER,
     "test_sulfur_oil_interval_is_refused"),
    ("hold", "sulfur_misspelled_in_regex",
     'SULFUR = re.compile(r"\\bsul(?:f|ph)ur\\b", re.I)',
     'SULFUR = re.compile(r"\\bsulph?ur\\b", re.I)  ' + MARKER,
     "test_sulfur_oil_interval_is_refused"),

    # ---- pear twins (NEW) ----------------------------------------------------------------
    ("twins", "id_mismatch_allowed",
     'if out_a[key]["id"] != out_e[key]["id"]:',
     'if False:  ' + MARKER,
     "test_pear_twin_id_mismatch_is_refused"),
    ("twins", "unpinned_divergence_allowed",
     'if pin is None:\n            raise SystemExit(f"REFUSED: pear twin {name!r} has byte-identical source prose but "',
     'if False:  ' + MARKER + '\n            raise SystemExit(f"REFUSED: pear twin {name!r} has byte-identical source prose but "',
     "test_unpinned_pear_divergence_is_refused"),
    ("twins", "mispinned_divergence_allowed",
     'if (extra_a, extra_e) != (tuple(pin[0]), tuple(pin[1])):',
     'if False:  ' + MARKER,
     "test_mispinned_pear_divergence_is_refused"),
    ("twins", "vacuity_brake_removed",
     'if twins == 0:\n        raise SystemExit("REFUSED: no pear template twins found;',
     'if False:  ' + MARKER + '\n        raise SystemExit("REFUSED: no pear template twins found;',
     "test_pear_twin_guard_refuses_when_no_twins_reach_it"),

    # ---- verify_post -----------------------------------------------------------------------
    ("verify", "undeclared_prose_change_allowed",
     'if k not in corr:\n                            raise SystemExit(f"REFUSED: {crop}/{g[\'name\']!r} prose field {k!r} "',
     'if False:  ' + MARKER + '\n                            raise SystemExit(f"REFUSED: {crop}/{g[\'name\']!r} prose field {k!r} "',
     "test_undeclared_prose_change_is_refused"),
    ("verify", "correction_value_not_compared",
     'if g[k] != corr[k]["new"]:',
     'if False:  ' + MARKER + ' g[k] != corr[k]["new"]:',
     "test_correction_not_matching_its_declaration_is_refused"),
    ("verify", "untouched_crops_unchecked",
     'if json.dumps(pre_i[slug], sort_keys=True) != json.dumps(post_i[slug], sort_keys=True):',
     'if False:  ' + MARKER,
     "test_untouched_crop_mutation_is_refused"),
    ("verify", "top_level_keys_unchecked",
     'if json.dumps(pre[k], sort_keys=True) != json.dumps(post[k], sort_keys=True):',
     'if False:  ' + MARKER,
     "test_top_level_key_mutation_is_refused"),
    ("verify", "removed_keys_unchecked",
     'if removed:',
     'if False:  ' + MARKER + ' removed:',
     "test_lost_key_is_refused"),

    # ---- mechanics -------------------------------------------------------------------------
    ("mechanics", "canonical_written_indented",
     'return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     'return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_serialize_is_compact"),
    ("mechanics", "base_sha_unchecked",
     'if got != BASE_SHA:',
     'if False:  ' + MARKER + ' got != BASE_SHA:',
     "test_load_canonical_refuses_a_moved_base"),
]

# The SENTINEL must redden. If it survives, nothing here is measuring anything.
#
# ITS ANCHOR IS DERIVED, NOT HARDCODED, and that is a lesson this harness paid for on its first run.
# The sentinel originally hardcoded `N_RUNGS = 138`. The suite's pins were then re-measured to 141
# after the last authoring round, the anchor stopped matching, and the harness correctly exited
# HARNESS DEAD instead of reporting a run. That is the liveness defense doing its job -- a mutation
# that did not apply is a HARNESS failure and not a survivor -- but a sentinel that breaks every time
# a pin legitimately moves will eventually be "fixed" by someone deleting it. So it reads the current
# value out of the suite and corrupts THAT.
def sentinel_for(tools_dir):
    import re as _re
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = _re.search(r"^N_RUNGS = (\d+)$", src, _re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_RUNGS pin to build a sentinel from")
    return ("sentinel", "rung_count_pin_broken",
            m.group(0), f"N_RUNGS = {int(m.group(1)) + 99999}  " + MARKER,
            "test_ladders_pass_and_rung_count_is_pinned", SUITE)


def build_scratch():
    """A scratch tools/ tree that imports cleanly. The promote resolves REPO as three levels up
    from its own file, so the scratch must sit at <tmp>/tools/ with the repo root above it."""
    tmp = tempfile.mkdtemp(prefix="mut_b26_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in os.listdir(HERE):
        if f.endswith(".py") or f.endswith(".json"):
            src = os.path.join(HERE, f)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(tools, f))
    # the promote and suite read canonical and the staging dir out of REPO
    os.symlink(os.path.join(REPO, "crops_data_final.json"),
               os.path.join(tmp, "crops_data_final.json"))
    # THE SUITE REBUILDS ITS PRE-STATE FROM THE COMMITTED BASE (promote_fixture.pre_state runs
    # `git show` with cwd=REPO, and REPO is derived from the fixture's own file path). In a scratch
    # tree that is a temp dir with no .git, so the fixture raised, the positive control failed, and
    # the harness correctly exited HARNESS DEAD on its first run. Batch 25's harness was measured
    # BEFORE its suite moved onto the fixture (818bd6b) and would die the same way today. Linking
    # the real .git in makes the scratch a worktree of the same object store.
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    shutil.copytree(os.path.join(HERE, "staging", "pla8_batch26_trees"),
                    os.path.join(tools, "staging", "pla8_batch26_trees"))
    return tmp, tools


def run_suite(tools_dir, selector, target_file=PROMOTE):
    """STALE BYTECODE IS A DEAD HARNESS. Each mutation rewrites the same .py, and CPython's
    source-mtime cache has one-second granularity, so a rapid rewrite can leave a __pycache__ entry
    that still looks current and the suite silently imports the CLEAN module. Every mutation then
    reports as SURVIVED with no sign anything is wrong -- the exact shape of PLA-138's dead harness.
    Bytecode writing is disabled in the child and any existing cache is removed before each run."""
    cache = os.path.join(tools_dir, "__pycache__")
    shutil.rmtree(cache, ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", os.path.join(tools_dir, SUITE), "-q", "-k", selector,
         "--no-header", "-p", "no:cacheprovider"],
        capture_output=True, text=True, cwd=os.path.dirname(tools_dir), env=env)
    return r.returncode, (r.stdout + r.stderr)


def apply_mutation(tools_dir, old, new, target=PROMOTE):
    path = os.path.join(tools_dir, target)
    clean = open(path, encoding="utf-8").read()
    if old not in clean:
        return None, f"ANCHOR NOT FOUND in {target}: {old[:70]!r}"
    mutated = clean.replace(old, new, 1)
    if mutated == clean:
        return None, "replacement produced identical bytes"
    open(path, "w", encoding="utf-8").write(mutated)
    # LIVENESS: the marker must be present on disk, or the mutation did not apply.
    back = open(path, encoding="utf-8").read()
    if MARKER not in back:
        return None, "MUTATION-APPLIED marker absent after write"
    if back == clean:
        return None, "file on disk is byte-identical to clean"
    return clean, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        fams = {}
        for fam, name, *_ in MUTATIONS:
            fams.setdefault(fam, []).append(name)
        for f, names in fams.items():
            print(f"{f} ({len(names)})")
            for n in names:
                print(f"    {n}")
        return 0

    muts = [m for m in MUTATIONS if not args.family or m[0] == args.family]
    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")

    try:
        # ---- POSITIVE CONTROL: the unmutated scratch must be GREEN on a cheap driver.
        rc, out = run_suite(tools, "test_spec_match_passes")
        if rc != 0:
            print(out[-2500:])
            sys.exit("HARNESS DEAD: the UNMUTATED scratch copy is already failing. Every 'caught' "
                     "below would be meaningless because the suite fails regardless of mutation.")
        print("positive control: unmutated scratch is GREEN\n")

        # ---- SENTINEL: a mutation that must redden.
        fam, name, old, new, sel, tgt = sentinel_for(tools)
        clean, err = apply_mutation(tools, old, new, tgt)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel)
        open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED. The harness is not measuring "
                     "anything and no result below can be trusted.")
        print("sentinel: reddened as required\n")

        caught, survived, broken = [], [], []
        for fam, name, old, new, sel in muts:
            clean, err = apply_mutation(tools, old, new)
            if err:
                broken.append((fam, name, err))
                print(f"  BROKEN   {fam}/{name}: {err}")
                continue
            rc, out = run_suite(tools, sel)
            open(os.path.join(tools, PROMOTE), "w", encoding="utf-8").write(clean)
            if rc == 0:
                survived.append((fam, name, sel))
                print(f"  SURVIVED {fam}/{name}   (driver: {sel})")
            else:
                caught.append((fam, name))
                print(f"  caught   {fam}/{name}")

        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, "
              f"{len(broken)} broken")
        if broken:
            print("\nBROKEN mutations are HARNESS failures, not survivors. Fix the anchors:")
            for f, n, e in broken:
                print(f"  {f}/{n}: {e}")
        if survived:
            print("\nSURVIVORS are guards the suite does not actually test:")
            for f, n, s in survived:
                print(f"  {f}/{n}  (driver was: {s})")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
