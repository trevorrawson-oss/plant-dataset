#!/usr/bin/env python3
"""mutate_pla7_container_path_suite -- mutation harness for the PLA-7 promote A1 container_path suite.

BUILT TO THE PLA-215 BAR. It injects one defect per guard family into a SCRATCH COPY of the promote
source, runs the suite's own drivers against the mutated copy, and requires each to go RED. A
mutation that survives is a guard the suite does not actually test.

THE LIVENESS DEFENSE: anchor preflight (every anchor matches EXACTLY ONCE), a MUTATION-APPLIED
marker asserted on disk, a sentinel that MUST redden, a positive control that must be GREEN, and
bytecode disabled with __pycache__ cleared before every run. Any of those failing exits HARNESS
DEAD, which is the behaviour to expect from a working harness on a bad day.

WHY PER-MUTATION TEST SELECTION. Each mutation names the driver that SHOULD catch it, and only that
driver runs. The selection IS the assertion: a mutation counts as caught only if ITS OWN driver
reddens, not if some other test happens to fall over.

NOT COUNTED AS COVERAGE (forward assertions that cannot fire in isolation on this spec): the
kind/field/kebab shape checks in check_spec_shape, and apply_to's own match-count refusal, which
check_pre_state reaches first.

Usage:
    mutate_pla7_container_path_suite.py             # all families
    mutate_pla7_container_path_suite.py --family X  # one family
    mutate_pla7_container_path_suite.py --list
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_pla7_container_path.py"
SUITE = "test_promote_pla7_container_path.py"
STAGING = "pla7_container_path"
MARKER = "# MUTATION-APPLIED"
# pytest exits 5 when nothing was collected: a non-zero rc that is NOT a red driver. Grading it as
# "caught" would score a mistyped selector as coverage, so it is BROKEN (a harness failure).
NOTHING_COLLECTED = 5

# (family, name, old, new, pytest -k selector)
MUTATIONS = [
    ("entry", "base_sha_check_removed", "    if got != BASE_SHA:", "    if False:  " + MARKER,
     "test_refuses_a_canonical_that_is_not_the_base"),

    ("spec", "row_count_not_pinned", "    if len(rows) != EXPECTED_ROWS:", "    if False:  " + MARKER,
     "test_refuses_a_missing_crop"),
    ("spec", "duplicate_crop_accepted", '        if r["crop"] in seen:', "        if False:  " + MARKER,
     "test_refuses_a_duplicated_crop"),
    ("spec", "unknown_value_accepted", "        if v is not None and v not in VALUES:", "        if False:  " + MARKER,
     "test_refuses_an_unknown_value"),
    ("spec", "missing_evidence_accepted", '        if v in EVIDENCE_VALUES and not (r.get("evidence") or "").strip():', "        if False:  " + MARKER,
     "test_refuses_rootstock_without_evidence"),
    ("spec", "stray_evidence_accepted", '        if v not in EVIDENCE_VALUES and r.get("evidence"):', "        if False:  " + MARKER,
     "test_refuses_evidence_on_a_direct_row"),
    ("spec", "count_pins_not_compared", "        if counts[k] != pins[k]:", "        if False:  " + MARKER,
     "test_refuses_a_count_drift"),
    ("spec", "flip_count_not_pinned", "    if len(flips) != EXPECTED_FLIPS:", "    if False:  " + MARKER,
     "test_refuses_a_fourth_flip"),
    ("spec", "recommending_flip_accepted", '        if f["container_ok"] is not True or f["container_recommended"] is not False:', "        if False:  " + MARKER,
     "test_refuses_a_flip_that_recommends"),
    ("spec", "absurd_pot_accepted", '        if not (isinstance(f["min_pot_gallons"], int) and 1 <= f["min_pot_gallons"] <= 100):', "        if False:  " + MARKER,
     "test_refuses_a_flip_with_an_absurd_pot"),
    ("spec", "gravel_count_not_pinned", '    if len(spec["gravel_normalize"]) != EXPECTED_GRAVEL:', "    if False:  " + MARKER,
     "test_refuses_a_gravel_row_count_drift"),

    ("prestate", "existing_key_accepted", '        if "container_path" in cn:\n            raise SystemExit(f"REFUSED: {c[\'slug\']} already carries container_path")',
     '        if False:  ' + MARKER + '\n            raise SystemExit(f"REFUSED: {c[\'slug\']} already carries container_path")',
     "test_refuses_a_crop_already_carrying_the_key"),
    ("prestate", "existing_variety_key_accepted", '            if "container_suitable" in v or "container_min_gallons" in v:', "            if False:  " + MARKER,
     "test_refuses_a_variety_already_flagged"),
    ("prestate", "evidence_not_counted", "            if hits != 1:", "            if False:  " + MARKER,
     "test_refuses_evidence_that_does_not_match_the_crop"),
    ("prestate", "null_vs_ok_not_compared", '        if (r["container_path"] is not None) != ok_post:', "        if False:  " + MARKER,
     "test_refuses_a_row_whose_null_disagrees_with_container_ok"),
    ("prestate", "rootstock_join_not_checked", '            if not any(x.get("container_suitable") is True for x in (c.get("rootstock_options") or []) if isinstance(x, dict)):', "            if False:  " + MARKER,
     "test_refuses_rootstock_with_no_suitable_entry"),
    ("prestate", "flip_precondition_not_checked", '        if cn.get("container_ok") is not False or cn.get("min_pot_gallons") is not None:', "        if False:  " + MARKER,
     "test_refuses_a_flip_on_a_crop_already_true"),
    ("prestate", "gravel_set_not_compared", '    if set(spec["gravel_normalize"]) != want_gravel:', "    if False:  " + MARKER,
     "test_refuses_a_missed_gravel_crop"),
    ("prestate", "applicable_set_not_compared", '    if set(spec["overwinter_applicable_true"]) != want_app:', "    if False:  " + MARKER,
     "test_refuses_a_missed_applicable_crop"),
    ("prestate", "applicable_prose_not_required", '            if not (ow.get("approach_seasoned") or cn.get("container_overwintering_seasoned")):', "            if False:  " + MARKER,
     "test_refuses_applicable_with_no_prose"),
    ("prestate", "mechanical_count_not_pinned", "    if len(mech) != EXPECTED_FLAGS_MECHANICAL:", "    if False:  " + MARKER,
     "test_refuses_a_mechanical_count_drift"),
    ("prestate", "explicit_flag_entry_not_checked", "        if len(ent) != 1:", "        if False:  " + MARKER,
     "test_refuses_an_explicit_flag_naming_no_entry"),

    ("post", "gate_not_run_on_post", "    v = CPG.all_violations(post, presence=True)\n    if v:", "    v = CPG.all_violations(post, presence=True)\n    if False:  " + MARKER,
     "test_refuses_a_post_state_that_fails_the_gate"),
    ("post", "display_readiness_not_run_on_flips", "        if dv:", "        if False:  " + MARKER,
     "test_refuses_a_flip_that_fails_display_readiness"),

    ("blast", "top_level_change_invisible", '        if k != "crops" and _j(pre[k]) != _j(post[k]):', "        if False:  " + MARKER,
     "test_refuses_a_top_level_change"),
    ("blast", "roster_change_invisible", '    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):', "    if False:  " + MARKER,
     "test_refuses_a_roster_change"),
    ("blast", "shell_change_invisible", '            if _j(s) != _j(g):\n                raise SystemExit(f"REFUSED: shell {slug} changed")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: shell {slug} changed")',
     "test_refuses_a_shell_change"),
    ("blast", "outside_change_invisible", '            if _j(s[k]) != _j(g[k]):\n                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside container_notes/varieties")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside container_notes/varieties")',
     "test_refuses_a_change_outside_the_two_blocks"),
    ("blast", "extra_key_accepted", '        if set(gcn) - set(scn) != {"container_path"} or set(scn) - set(gcn):', "        if False:  " + MARKER,
     "test_refuses_an_extra_container_notes_key"),
    ("blast", "undeclared_cn_change_accepted", '                raise SystemExit(f"REFUSED: {slug} container_notes.{k} changed without a spec row")', "                leaves += 1  " + MARKER,
     "test_refuses_an_undeclared_container_notes_change"),
    ("blast", "unmatched_flag_accepted", "                if key not in allowed_flags:", "                if False:  " + MARKER,
     "test_refuses_a_variety_flag_without_a_match"),
    ("blast", "variety_value_change_invisible", "                    if _j(a[k]) != _j(b[k]):", "                    if False:  " + MARKER,
     "test_refuses_a_variety_prose_change"),
    ("blast", "leaf_count_not_pinned", "    if leaves != EXPECTED_LEAVES:", "    if False:  " + MARKER,
     "test_refuses_a_leaf_count_drift"),
    ("blast", "drainage_key_set_not_compared",
     '                if set(gcn[k]) != set(scn[k]):\n                    raise SystemExit(f"REFUSED: {slug} drainage key set changed")',
     '                if False:  ' + MARKER + '\n                    raise SystemExit(f"REFUSED: {slug} drainage key set changed")',
     "test_refuses_a_drainage_key_addition"),
    ("blast", "overwintering_key_set_not_compared",
     '                if set(gcn[k]) != set(scn[k]):\n                    raise SystemExit(f"REFUSED: {slug} overwintering key set changed")',
     '                if False:  ' + MARKER + '\n                    raise SystemExit(f"REFUSED: {slug} overwintering key set changed")',
     "test_refuses_an_overwintering_key_addition"),
    ("blast", "variety_min_gallons_not_compared",
     '                if key in explicit and b["container_min_gallons"] != explicit[key]["container_min_gallons"]:', "                if False:  " + MARKER,
     "test_refuses_a_variety_min_gallons_other_than_declared"),
    ("blast", "flag_not_rederived_from_list",
     '                if key not in explicit and (b.get("name") or "").strip().lower() not in csv_pre:', "                if False:  " + MARKER,
     "test_refuses_a_helper_that_flags_the_wrong_variety"),
    ("blast", "unflagged_match_invisible",
     '            if (b.get("name") or "").strip().lower() in csv_pre and b.get("container_suitable") is not True:', "            if False:  " + MARKER,
     "test_refuses_a_matching_variety_left_unflagged"),

    ("blast", "path_value_not_compared_to_spec",
     '        if gcn["container_path"] != row_by_crop[slug]["container_path"]:', "        if False:  " + MARKER,
     "test_refuses_a_path_value_other_than_the_spec_row"),
    ("blast", "varieties_prose_change_invisible",
     '                if k != "recommended" and _j(sva[k]) != _j(gva[k]):', "                if False:  " + MARKER,
     "test_refuses_a_varieties_prose_change"),
    ("blast", "string_entry_change_invisible",
     "                    if not isinstance(a, dict) and _j(a) != _j(b):", "                    if False:  " + MARKER,
     "test_refuses_a_string_variety_entry_change"),
    ("blast", "top_level_key_set_not_compared", "    if set(pre) != set(post):", "    if False:  " + MARKER,
     "test_refuses_a_top_level_key_addition"),
    ("blast", "crop_level_key_set_not_compared", "        if set(s) != set(g):", "        if False:  " + MARKER,
     "test_refuses_a_crop_level_key_addition"),

    ("serialize", "indent_reintroduced",
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_compact_no_trailing_newline"),
]


def sentinel_for(tools_dir):
    """Built from the CURRENT pin value, so a legitimate pin move does not permanently break the
    sentinel and invite someone to delete it."""
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_LEAVES = (\d+)$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_LEAVES pin to build a sentinel from")
    return ("sentinel", "leaf_count_pin_broken",
            m.group(0), f"N_LEAVES = {int(m.group(1)) + 99999}  " + MARKER,
            "test_pins_are_the_literals", SUITE)


def preflight(tools_dir):
    """EVERY ANCHOR MATCHES EXACTLY ONCE, checked before a single result is graded."""
    src = open(os.path.join(tools_dir, PROMOTE), encoding="utf-8").read()
    bad = []
    for fam, name, old, _new, _sel in MUTATIONS:
        n = src.count(old)
        if n != 1:
            bad.append(f"  {fam}/{name}: anchor matches {n} times, needs exactly 1\n"
                       f"      {old[:90]!r}")
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed. An anchor matching zero times edits "
                 "nothing and reports a FALSE SURVIVOR; one matching twice edits a site nobody "
                 "intended.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_pla7_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"),
               os.path.join(tmp, "crops_data_final.json"))
    # promote_fixture.pre_state shells out to `git show` with cwd=REPO, derived from its own path.
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    shutil.copytree(os.path.join(HERE, "staging", STAGING),
                    os.path.join(tools, "staging", STAGING))
    return tmp, tools


def run_suite(tools_dir, selector):
    """STALE BYTECODE IS A DEAD HARNESS: clear __pycache__ and disable writing it."""
    shutil.rmtree(os.path.join(tools_dir, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", os.path.join(tools_dir, SUITE), "-q", "-k", selector,
         "--no-header", "-p", "no:cacheprovider"],
        capture_output=True, text=True, cwd=os.path.dirname(tools_dir), env=env)
    return r.returncode, (r.stdout + r.stderr)


def apply_mutation(tools_dir, old, new, target=PROMOTE):
    path = os.path.join(tools_dir, target)
    clean = open(path, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times in {target}"
    mutated = clean.replace(old, new, 1)
    if mutated == clean:
        return None, "replacement produced identical bytes"
    open(path, "w", encoding="utf-8").write(mutated)
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

    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        preflight(tools)

        rc, out = run_suite(tools, "test_the_spec_is_the_shape_measured")
        if rc != 0:
            print(out[-2500:])
            sys.exit("HARNESS DEAD: the UNMUTATED scratch copy is already failing. Every 'caught' "
                     "below would be meaningless because the suite fails regardless of mutation.")
        print("positive control: unmutated scratch is GREEN")

        fam, name, old, new, sel, tgt = sentinel_for(tools)
        clean, err = apply_mutation(tools, old, new, tgt)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel)
        open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
        if rc == NOTHING_COLLECTED:
            sys.exit("HARNESS DEAD: the sentinel selected NO TESTS (pytest rc 5). A selector that "
                     "collects nothing reddens for the wrong reason and grades every mutation below "
                     "on an empty run.")
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED. The harness is not measuring "
                     "anything and no result below can be trusted.")
        print("sentinel: reddened as required\n")

        muts = [m for m in MUTATIONS if not args.family or m[0] == args.family]
        caught, survived, broken = [], [], []
        for fam, name, old, new, sel in muts:
            clean, err = apply_mutation(tools, old, new)
            if err:
                broken.append((fam, name, err))
                print(f"  BROKEN   {fam}/{name}: {err}")
                continue
            rc, out = run_suite(tools, sel)
            open(os.path.join(tools, PROMOTE), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append((fam, name, f"driver {sel!r} collected NO TESTS (pytest rc 5)"))
                print(f"  BROKEN   {fam}/{name}: driver {sel!r} collected no tests (pytest rc 5)")
            elif rc == 0:
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
