#!/usr/bin/env python3
"""mutate_pla464_rootstock_array_suite -- mutation harness for the PLA-464 Option A promote suite.

BUILT TO THE PLA-215 BAR. One defect per guard family injected into a SCRATCH COPY of the promote
source; the suite's own driver for that guard must go RED. A survivor is a guard the suite does not
actually test.

THE LIVENESS DEFENSE: anchor preflight (every anchor matches EXACTLY ONCE), a MUTATION-APPLIED marker
asserted on disk, a sentinel that MUST redden, a positive control that must be GREEN, bytecode
disabled with __pycache__ cleared before every run, and pytest rc 5 (nothing collected) graded BROKEN.

NOT COUNTED AS COVERAGE (removed from the promote rather than left to read as coverage): a post-state
name-net check (implied by entry count + survivor byte identity), a fold-in count==1 check (implied
by equality with pre + sentence), a verify_post gallons assertion (container_notes is outside the
declared keys, so the generic loop refuses first; the pin lives in check_pre_state), a change-count
refusal (every per-key check implies it).

Usage:
    mutate_pla464_rootstock_array_suite.py             # all families
    mutate_pla464_rootstock_array_suite.py --family X  # one family
    mutate_pla464_rootstock_array_suite.py --list
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
PROMOTE = "promote_pla464_rootstock_array.py"
SUITE = "test_promote_pla464_rootstock_array.py"
STAGING = "pla464_rootstock_array"
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5


def off(line):
    """Replace a guard's `if <cond>:` (or `elif`) with a never-true branch, keeping indentation."""
    m = re.match(r"^(\s*)(if|elif) (.*):$", line)
    assert m, line
    return f"{m.group(1)}{m.group(2)} False:  {MARKER}"


# (family, name, old, new, pytest -k selector)
MUTATIONS = [
    ("entry", "base_sha_check_removed", "    if got != BASE_SHA:", off("    if got != BASE_SHA:"),
     "test_refuses_a_canonical_that_is_not_the_base"),

    ("spec", "spec_base_not_checked", '    if spec.get("base_sha") != BASE_SHA:', off('    if spec.get("base_sha") != BASE_SHA:'),
     "test_refuses_a_spec_on_another_base"),
    ("spec", "retire_count_not_pinned", "    if len(rows) != EXPECTED_RETIRE:", off("    if len(rows) != EXPECTED_RETIRE:"),
     "test_refuses_a_retire_count_drift"),
    ("spec", "duplicate_row_accepted", "        if key in seen:", off("        if key in seen:"),
     "test_refuses_a_duplicated_retire_row"),
    ("spec", "unknown_concept_accepted", '        if r["concept"] not in CONCEPTS:', off('        if r["concept"] not in CONCEPTS:'),
     "test_refuses_an_unknown_concept"),
    ("spec", "nameless_row_accepted", '        if not (r.get("name") or "").strip():', off('        if not (r.get("name") or "").strip():'),
     "test_refuses_a_nameless_retire_row"),
    ("spec", "crop_count_not_pinned", "    if len(retire_crops) != EXPECTED_CROPS:", off("    if len(retire_crops) != EXPECTED_CROPS:"),
     "test_refuses_a_retire_set_spanning_the_wrong_crop_count"),
    ("spec", "foldin_count_not_pinned", "    if len(folds) != EXPECTED_FOLDINS:", off("    if len(folds) != EXPECTED_FOLDINS:"),
     "test_refuses_a_foldin_count_drift"),
    ("spec", "foldin_crop_not_checked", "    if len(set(fold_crops)) != len(fold_crops) or not set(fold_crops) <= retire_crops:",
     off("    if len(set(fold_crops)) != len(fold_crops) or not set(fold_crops) <= retire_crops:"),
     "test_refuses_a_foldin_on_a_crop_with_no_retired_row"),
    ("spec", "unterminated_foldin_accepted", '        if not s.strip() or not s.endswith("."):', off('        if not s.strip() or not s.endswith("."):'),
     "test_refuses_a_foldin_without_a_period"),
    ("spec", "em_dash_accepted", "        if _bad_copy(s):", off("        if _bad_copy(s):"),
     "test_refuses_a_foldin_with_an_em_dash"),
    ("spec", "sourceless_foldin_accepted", '        if not f.get("sources"):', off('        if not f.get("sources"):'),
     "test_refuses_a_foldin_without_sources"),
    ("spec", "rr_count_not_pinned", "    if len(rr) != EXPECTED_RR:", off("    if len(rr) != EXPECTED_RR:"),
     "test_refuses_a_recommended_rootstock_count_drift"),
    ("spec", "rr_noop_accepted", '        if r["crop"] not in retire_crops or r["from"] == r["to"]:', off('        if r["crop"] not in retire_crops or r["from"] == r["to"]:'),
     "test_refuses_a_recommended_rootstock_no_op"),
    ("spec", "gallons_not_kept_accepted",
     '    if mg.get("kept") is not True or mg.get("min_pot_gallons") != MULBERRY_GALLONS or mg.get("container_min_gallons") != MULBERRY_GALLONS:',
     off('    if mg.get("kept") is not True or mg.get("min_pot_gallons") != MULBERRY_GALLONS or mg.get("container_min_gallons") != MULBERRY_GALLONS:'),
     "test_refuses_mulberry_gallons_not_kept"),
    ("spec", "fa_count_not_pinned", "    if len(fas) != EXPECTED_FA:", off("    if len(fas) != EXPECTED_FA:"),
     "test_refuses_a_field_additions_count_drift"),
    ("spec", "fa_shape_not_checked", '        if set(e) != set(FA_KEYS) or e["field"] != "recommended_rootstock_note":',
     off('        if set(e) != set(FA_KEYS) or e["field"] != "recommended_rootstock_note":'),
     "test_refuses_a_field_additions_shape"),
    ("spec", "fa_sources_not_tied_to_foldin", '        if fa["crop"] not in by_fold or list(e["sources"]) != list(by_fold[fa["crop"]]["sources"]):',
     off('        if fa["crop"] not in by_fold or list(e["sources"]) != list(by_fold[fa["crop"]]["sources"]):'),
     "test_refuses_a_field_additions_whose_sources_differ_from_its_foldin"),
    ("spec", "findings_count_not_pinned", "    if len(ofs) != EXPECTED_FINDINGS:", off("    if len(ofs) != EXPECTED_FINDINGS:"),
     "test_refuses_a_findings_count_drift"),
    ("spec", "finding_shape_not_checked", "        if set(e) != set(RECORD_KEYS):", off("        if set(e) != set(RECORD_KEYS):"),
     "test_refuses_a_finding_shape"),
    ("spec", "blocking_finding_accepted", '        if e["status"] != "deferred" or e["blocks_launch"] is not False or e["filed_in_session"] != SESSION:',
     off('        if e["status"] != "deferred" or e["blocks_launch"] is not False or e["filed_in_session"] != SESSION:'),
     "test_refuses_a_finding_that_blocks_launch"),
    ("spec", "duplicate_finding_id_accepted", '        if e["id"] in ids or of["crop"] not in retire_crops:', off('        if e["id"] in ids or of["crop"] not in retire_crops:'),
     "test_refuses_a_duplicated_finding_id"),
    ("spec", "expected_block_not_compared", '    if spec["expected"] != want_expected:', off('    if spec["expected"] != want_expected:'),
     "test_refuses_an_expected_block_drift"),

    ("prestate", "roster_not_pinned", '    if len(data["crops"]) != ROSTER:', off('    if len(data["crops"]) != ROSTER:'),
     "test_refuses_a_roster_drift"),
    ("prestate", "missing_crop_accepted", "        if c is None:", off("        if c is None:"),
     "test_refuses_a_retire_crop_off_the_roster"),
    ("prestate", "index_name_not_checked", '        if r["index"] >= len(rows) or (rows[r["index"]].get("name") or "") != r["name"]:',
     off('        if r["index"] >= len(rows) or (rows[r["index"]].get("name") or "") != r["name"]:'),
     "test_refuses_an_index_naming_another_row"),
    ("prestate", "net_not_compared", "    if got != want:", off("    if got != want:"),
     "test_refuses_a_net_disagreement_missed_row or test_refuses_a_net_disagreement_unflagged_spec_row"),
    ("prestate", "missing_note_accepted", "        if not isinstance(note, str) or not note.strip():", off("        if not isinstance(note, str) or not note.strip():"),
     "test_refuses_a_crop_with_no_note"),
    ("prestate", "present_foldin_accepted", '        if note.count(f["sentence"]) != 0:', off('        if note.count(f["sentence"]) != 0:'),
     "test_refuses_a_foldin_already_present"),
    ("prestate", "catalog_not_checked", "            if s not in catalog:", off("            if s not in catalog:"),
     "test_refuses_a_foldin_source_not_in_catalog"),
    ("prestate", "sibling_from_not_checked", '        if idx[r["crop"]].get("recommended_rootstock") != r["from"]:',
     off('        if idx[r["crop"]].get("recommended_rootstock") != r["from"]:'),
     "test_refuses_a_sibling_from_mismatch"),
    ("prestate", "crop_gallons_not_pinned", '    if (m.get("container_notes") or {}).get("min_pot_gallons") != mg["min_pot_gallons"]:',
     off('    if (m.get("container_notes") or {}).get("min_pot_gallons") != mg["min_pot_gallons"]:'),
     "test_refuses_mulberry_gallons_not_pinned_on_base"),
    ("prestate", "variety_gallons_not_pinned", '    if len(dv) != 1 or dv[0].get("container_min_gallons") != mg["container_min_gallons"]:',
     off('    if len(dv) != 1 or dv[0].get("container_min_gallons") != mg["container_min_gallons"]:'),
     "test_refuses_dwarf_everbearing_gallons_not_pinned_on_base"),
    ("prestate", "fa_list_not_checked", '        if not isinstance(vs.get("field_additions"), list):', off('        if not isinstance(vs.get("field_additions"), list):'),
     "test_refuses_field_additions_not_a_list"),
    ("prestate", "prior_fa_record_accepted", '        if any(x.get("field") == "recommended_rootstock_note" for x in vs["field_additions"]):',
     off('        if any(x.get("field") == "recommended_rootstock_note" for x in vs["field_additions"]):'),
     "test_refuses_a_recorded_note_addition_already_present"),
    ("prestate", "of_list_not_checked", '        if not isinstance(vs.get("open_findings"), list):', off('        if not isinstance(vs.get("open_findings"), list):'),
     "test_refuses_open_findings_not_a_list"),
    ("prestate", "prior_finding_id_accepted", '        if any(x.get("id") == of["entry"]["id"] for x in vs["open_findings"]):',
     off('        if any(x.get("id") == of["entry"]["id"] for x in vs["open_findings"]):'),
     "test_refuses_a_finding_id_already_present"),

    ("post", "gate_not_run_on_post", "    v = CPG.all_violations(post, presence=True)\n    if v:",
     "    v = CPG.all_violations(post, presence=True)\n    if False:  " + MARKER,
     "test_refuses_a_post_state_that_fails_the_gate"),
    ("post", "display_readiness_not_run", "        if dv:", off("        if dv:"),
     "test_refuses_a_touched_crop_that_fails_display_readiness"),
    ("post", "numeric_sanity_not_run", "        if nv:", off("        if nv:"),
     "test_refuses_a_touched_crop_that_fails_numeric_sanity"),

    ("blast", "top_level_key_set_not_compared", "    if set(pre) != set(post):", off("    if set(pre) != set(post):"),
     "test_refuses_a_top_level_key_addition"),
    ("blast", "top_level_change_invisible", '        if k != "crops" and _j(pre[k]) != _j(post[k]):', off('        if k != "crops" and _j(pre[k]) != _j(post[k]):'),
     "test_refuses_a_top_level_change"),
    ("blast", "roster_change_invisible", '    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):',
     off('    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):'),
     "test_refuses_a_roster_change"),
    ("blast", "untouched_crop_change_invisible",
     '            if _j(s) != _j(g):\n                raise SystemExit(f"REFUSED: untouched crop {slug} changed")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: untouched crop {slug} changed")',
     "test_refuses_an_untouched_crop_change"),
    ("blast", "crop_level_key_set_not_compared", "        if set(s) != set(g):", off("        if set(s) != set(g):"),
     "test_refuses_a_crop_level_key_addition"),
    ("blast", "outside_change_invisible",
     '            if _j(s[k]) != _j(g[k]):\n                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside the declared keys")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside the declared keys")',
     "test_refuses_a_change_outside_the_declared_keys or test_refuses_a_gallons_move_on_mulberry or test_refuses_a_gallons_move_on_dwarf_everbearing"),
    ("blast", "entry_count_not_compared", '        if len(g["rootstock_options"]) != len(kept):', off('        if len(g["rootstock_options"]) != len(kept):'),
     "test_refuses_an_entry_count_drift"),
    ("blast", "survivor_change_invisible",
     '            if _j(a) != _j(b):\n                raise SystemExit(f"REFUSED: {slug} surviving rootstock entry {a.get(\'name\')!r} changed")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: {slug} surviving rootstock entry {a.get(\'name\')!r} changed")',
     "test_refuses_a_surviving_entry_change"),
    ("blast", "note_not_compared_to_pre_plus_foldin", '            if g["recommended_rootstock_note"] != want:', off('            if g["recommended_rootstock_note"] != want:'),
     "test_refuses_a_note_other_than_pre_plus_foldin"),
    ("blast", "undeclared_note_change_invisible", '        elif _j(s["recommended_rootstock_note"]) != _j(g["recommended_rootstock_note"]):',
     off('        elif _j(s["recommended_rootstock_note"]) != _j(g["recommended_rootstock_note"]):'),
     "test_refuses_a_note_change_without_a_foldin"),
    ("blast", "sibling_value_not_compared", '            if g["recommended_rootstock"] != rr[slug]["to"]:', off('            if g["recommended_rootstock"] != rr[slug]["to"]:'),
     "test_refuses_a_sibling_value_other_than_declared"),
    ("blast", "undeclared_sibling_change_invisible", '        elif _j(s["recommended_rootstock"]) != _j(g["recommended_rootstock"]):',
     off('        elif _j(s["recommended_rootstock"]) != _j(g["recommended_rootstock"]):'),
     "test_refuses_a_sibling_change_without_a_row"),
    ("blast", "vs_key_set_not_compared", "        if set(sv) != set(gv):", off("        if set(sv) != set(gv):"),
     "test_refuses_a_verification_status_key_addition"),
    ("blast", "vs_value_change_invisible",
     '            if _j(sv[k]) != _j(gv[k]):\n                raise SystemExit(f"REFUSED: {slug} verification_status.{k} changed")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: {slug} verification_status.{k} changed")',
     "test_refuses_a_verification_status_value_change"),
    ("blast", "list_type_not_checked", "            if not isinstance(a, list) or not isinstance(b, list):", off("            if not isinstance(a, list) or not isinstance(b, list):"),
     "test_refuses_a_list_that_is_not_a_list"),
    ("blast", "prefix_not_compared", "            if _j(b[:len(a)]) != _j(a):", off("            if _j(b[:len(a)]) != _j(a):"),
     "test_refuses_a_rewritten_prefix"),
    ("blast", "tail_not_compared_to_spec", "            if _j(tail) != _j(want_tail):", off("            if _j(tail) != _j(want_tail):"),
     "test_refuses_a_record_other_than_the_spec or test_refuses_an_extra_appended_record"),

    ("serialize", "indent_reintroduced",
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_compact_no_trailing_newline"),
]


def sentinel_for(tools_dir):
    """Built from the CURRENT pin value, so a legitimate pin move does not permanently break it."""
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_CHANGES = (\d+)$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_CHANGES pin to build a sentinel from")
    return ("sentinel", "change_count_pin_broken",
            m.group(0), f"N_CHANGES = {int(m.group(1)) + 99999}  " + MARKER,
            "test_pins_are_the_literals", SUITE)


def preflight(tools_dir):
    """EVERY ANCHOR MATCHES EXACTLY ONCE, checked before a single result is graded."""
    src = open(os.path.join(tools_dir, PROMOTE), encoding="utf-8").read()
    bad = []
    for fam, name, old, _new, _sel in MUTATIONS:
        n = src.count(old)
        if n != 1:
            bad.append(f"  {fam}/{name}: anchor matches {n} times, needs exactly 1\n      {old[:90]!r}")
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed. An anchor matching zero times edits nothing and "
                 "reports a FALSE SURVIVOR; one matching twice edits a site nobody intended.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_pla464_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"), os.path.join(tmp, "crops_data_final.json"))
    # promote_fixture.pre_state shells out to `git show` with cwd=REPO, derived from its own path.
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    shutil.copytree(os.path.join(HERE, "staging", STAGING), os.path.join(tools, "staging", STAGING))
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

        rc, out = run_suite(tools, "test_the_spec_is_the_shape_measured or test_apply_changes_exactly_the_declared_changes")
        if rc != 0:
            print(out[-2500:])
            sys.exit("HARNESS DEAD: the UNMUTATED scratch copy is already failing. Every 'caught' below "
                     "would be meaningless because the suite fails regardless of mutation.")
        print("positive control: unmutated scratch is GREEN")

        fam, name, old, new, sel, tgt = sentinel_for(tools)
        clean, err = apply_mutation(tools, old, new, tgt)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel)
        open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
        if rc == NOTHING_COLLECTED:
            sys.exit("HARNESS DEAD: the sentinel selected NO TESTS (pytest rc 5).")
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED. The harness is not measuring anything.")
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

        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
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
