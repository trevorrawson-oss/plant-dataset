#!/usr/bin/env python3
"""mutate_pla465_null_rulings_suite -- mutation harness for PLA-465 promote 2 (the twelve nulls, recorded).
PLA-215 bar: one defect per guard family into a SCRATCH COPY; the driver for that guard must go RED.
Liveness: anchor preflight, MUTATION-APPLIED marker, sentinel that must redden, positive control = the WHOLE
suite (a driver red on the clean copy would grade its mutation caught for the wrong reason), bytecode off,
pytest rc 5 graded BROKEN. NOT COUNTED: the addenda-count total (implied by the per-entry summary check;
removed from the promote)."""
import argparse, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_pla465_null_rulings.py"
SUITE = "test_promote_pla465_null_rulings.py"
STAGING = "pla465_null_rulings"
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5


def off(line):
    m = re.match(r"^(\s*)(if|elif) (.*):$", line)
    assert m, line
    return f"{m.group(1)}{m.group(2)} False:  {MARKER}"


def off1of2(two):
    a, b = two.split("\n")
    return off(a) + "\n" + b


A = {
 "entry": "    if got != BASE_SHA:",
 "spec_base": '    if spec.get("base_sha") != BASE_SHA:',
 "appends_count": "    if len(rows) != EXPECTED_APPENDS:",
 "record_keys": "        if set(e) != set(RECORD_KEYS):",
 "dup_id": '        if e["id"] in ids:',
 "blocking": '        if e["blocks_launch"] is not False or e["filed_in_session"] != SESSION:',
 "status_vocab": '        if e["status"] not in STATUSES:',
 "route_iff": '        if (e["status"] == "deferred") != (e["deferred_to"] is not None):',
 "empty_text": '        if not (e["summary"] or "").strip() or not (e["resolution_note"] or "").strip():',
 "em_dash_record": '        if _bad_copy(e["summary"]) or _bad_copy(e["resolution_note"]):',
 "addendum_shape": '    if set(a) != {"crop", "id", "original_summary", "suffix"}:',
 "addendum_marker": '    if not a["suffix"].startswith(ADDENDUM_MARK) or not a["suffix"].endswith("]"):',
 "em_dash_addendum": '    if _bad_copy(a["suffix"]):',
 "crop_count": "    if len(crops) != EXPECTED_CROPS:",
 "expected": '    if spec["expected"] != want:',
 "roster": '    if len(data["crops"]) != ROSTER:',
 "off_roster": "        if c is None:",
 "not_certified": '        if not _certified(c):\n            raise SystemExit(f"REFUSED: ruling crop {crop} is not certified")',
 "carries_value": "        if any(c.get(k) is not None for k in PDG.FIELDS):",
 "of_list": '        if not isinstance((c.get("verification_status") or {}).get("open_findings"), list):',
 "id_present": '        if any(x.get("id") == r["entry"]["id"] for x in of):',
 "target_once": "    if len(hits) != 1:",
 "target_moved": '    if hits[0].get("summary") != a["original_summary"]:',
 "already_applied": '    if ADDENDUM_MARK in hits[0]["summary"]:',
 "gate_post": "    v = PDG.all_violations(post, presence=True)\n    if v:",
 "blocker_post": "        if blockers:",
 "top_keys": "    if set(pre) != set(post):",
 "top_change": '        if k != "crops" and _j(pre[k]) != _j(post[k]):',
 "roster_change": '    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):',
 "untouched": '            if _j(s) != _j(g):\n                raise SystemExit(f"REFUSED: untouched crop {slug} changed")',
 "crop_keys": "        if set(s) != set(g):",
 "outside": '            if k != "verification_status" and _j(s[k]) != _j(g[k]):',
 "vs_keys": "        if set(sv) != set(gv):",
 "vs_change": '            if k != "open_findings" and _j(sv[k]) != _j(gv[k]):',
 "shrank": "        if len(pb) < len(pa):",
 "prefix": "            elif _j(x) != _j(y):",
 "target_keys": "                if set(x) != set(y):",
 "target_summary": '                        if y[k] != x[k] + a["suffix"]:',
 "target_field": "                    elif _j(x[k]) != _j(y[k]):",
 "tail": "        if _j(pb[len(pa):]) != _j(want_tail):",
}
MUTATIONS = [
 ("entry", "base_sha_check_removed", A["entry"], off(A["entry"]), "test_refuses_a_canonical_that_is_not_the_base"),
 ("spec", "spec_base_not_checked", A["spec_base"], off(A["spec_base"]), "test_refuses_a_spec_on_another_base"),
 ("spec", "appends_count_not_pinned", A["appends_count"], off(A["appends_count"]), "test_refuses_an_appends_count_drift"),
 ("spec", "record_keys_not_checked", A["record_keys"], off(A["record_keys"]), "test_refuses_a_record_with_the_wrong_keys"),
 ("spec", "duplicate_id_accepted", A["dup_id"], off(A["dup_id"]), "test_refuses_a_duplicated_id"),
 ("spec", "blocking_record_accepted", A["blocking"], off(A["blocking"]), "test_refuses_a_blocking_record"),
 ("spec", "status_vocab_not_checked", A["status_vocab"], off(A["status_vocab"]), "test_refuses_a_status_outside_the_vocabulary"),
 ("spec", "route_iff_not_checked", A["route_iff"], off(A["route_iff"]), "test_refuses_deferred_without_a_route_and_accepted_with_one"),
 ("spec", "empty_text_accepted", A["empty_text"], off(A["empty_text"]), "test_refuses_an_empty_summary"),
 ("spec", "em_dash_record_accepted", A["em_dash_record"], off(A["em_dash_record"]), "test_refuses_an_em_dash_in_a_record"),
 ("spec", "addendum_shape_not_checked", A["addendum_shape"], off(A["addendum_shape"]), "test_refuses_an_addendum_shape"),
 ("spec", "addendum_marker_not_checked", A["addendum_marker"], off(A["addendum_marker"]), "test_refuses_an_addendum_without_the_dated_marker"),
 ("spec", "em_dash_addendum_accepted", A["em_dash_addendum"], off(A["em_dash_addendum"]), "test_refuses_an_em_dash_in_the_addendum"),
 ("spec", "crop_count_not_pinned", A["crop_count"], off(A["crop_count"]), "test_refuses_a_crop_count_drift"),
 ("spec", "expected_block_not_compared", A["expected"], off(A["expected"]), "test_refuses_an_expected_block_drift"),
 ("prestate", "roster_not_pinned", A["roster"], off(A["roster"]), "test_refuses_a_roster_drift"),
 ("prestate", "off_roster_accepted", A["off_roster"], off(A["off_roster"]), "test_refuses_a_crop_off_the_roster"),
 ("prestate", "uncertified_accepted", A["not_certified"], off1of2(A["not_certified"]), "test_refuses_an_uncertified_crop"),
 ("prestate", "valued_crop_accepted", A["carries_value"], off(A["carries_value"]), "test_refuses_a_crop_that_carries_a_dimension"),
 ("prestate", "of_list_not_checked", A["of_list"], off(A["of_list"]), "test_refuses_open_findings_not_a_list"),
 ("prestate", "present_id_accepted", A["id_present"], off(A["id_present"]), "test_refuses_an_id_already_present"),
 ("prestate", "target_count_not_checked", A["target_once"], off(A["target_once"]), "test_refuses_an_addendum_target_that_is_not_found_once"),
 ("prestate", "moved_target_accepted", A["target_moved"], off(A["target_moved"]), "test_refuses_an_addendum_target_whose_summary_moved"),
 ("prestate", "applied_addendum_accepted", A["already_applied"], off(A["already_applied"]), "test_refuses_an_addendum_already_applied"),
 ("post", "gate_not_run_on_post", A["gate_post"], "    v = PDG.all_violations(post, presence=True)\n    if False:  " + MARKER, "test_refuses_a_post_state_that_fails_the_gate"),
 ("post", "blocker_not_checked", A["blocker_post"], off(A["blocker_post"]), "test_refuses_a_launch_blocker_after_the_write"),
 ("blast", "top_level_key_set_not_compared", A["top_keys"], off(A["top_keys"]), "test_refuses_a_top_level_key_addition"),
 ("blast", "top_level_change_invisible", A["top_change"], off(A["top_change"]), "test_refuses_a_top_level_change"),
 ("blast", "roster_change_invisible", A["roster_change"], off(A["roster_change"]), "test_refuses_a_roster_change"),
 ("blast", "untouched_change_invisible", A["untouched"], off1of2(A["untouched"]), "test_refuses_an_untouched_crop_change"),
 ("blast", "crop_key_set_not_compared", A["crop_keys"], off(A["crop_keys"]), "test_refuses_a_crop_level_key_addition"),
 ("blast", "outside_change_invisible", A["outside"], off(A["outside"]), "test_refuses_a_change_outside_verification_status"),
 ("blast", "vs_key_set_not_compared", A["vs_keys"], off(A["vs_keys"]), "test_refuses_a_verification_status_key_addition"),
 ("blast", "vs_change_invisible", A["vs_change"], off(A["vs_change"]), "test_refuses_a_verification_status_value_change"),
 ("blast", "shrink_invisible", A["shrank"], off(A["shrank"]), "test_refuses_a_shrunk_list"),
 ("blast", "prefix_not_compared", A["prefix"], off(A["prefix"]), "test_refuses_a_rewritten_prefix"),
 ("blast", "target_key_set_not_compared", A["target_keys"], off(A["target_keys"]), "test_refuses_an_addendum_target_key_addition"),
 ("blast", "target_summary_not_compared", A["target_summary"], off(A["target_summary"]), "test_refuses_an_addendum_summary_other_than_original_plus_suffix"),
 ("blast", "target_field_change_invisible", A["target_field"], off(A["target_field"]), "test_refuses_an_addendum_target_field_change"),
 ("blast", "tail_not_compared", A["tail"], off(A["tail"]), "test_refuses_a_tail_other_than_the_spec or test_refuses_an_extra_appended_record"),
 ("serialize", "indent_reintroduced", '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
  '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER, "test_compact_no_trailing_newline"),
]


def sentinel_for(tools_dir):
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_APPENDS = (\d+)$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_APPENDS pin")
    return ("sentinel", "appends_pin_broken", m.group(0), f"N_APPENDS = {int(m.group(1)) + 99999}  " + MARKER, "test_pins_are_the_literals", SUITE)


def preflight(tools_dir):
    src = open(os.path.join(tools_dir, PROMOTE), encoding="utf-8").read()
    bad = [f"  {fam}/{name}: anchor matches {src.count(old)} times\n      {old[:90]!r}" for fam, name, old, _n, _s in MUTATIONS if src.count(old) != 1]
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_pla465b_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"), os.path.join(tmp, "crops_data_final.json"))
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    shutil.copytree(os.path.join(HERE, "staging", STAGING), os.path.join(tools, "staging", STAGING))
    return tmp, tools


def run_suite(tools_dir, selector):
    shutil.rmtree(os.path.join(tools_dir, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", os.path.join(tools_dir, SUITE), "-q", "-k", selector, "--no-header", "-p", "no:cacheprovider"],
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
    if MARKER not in back or back == clean:
        return None, "mutation not on disk"
    return clean, None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--family"); ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        fams = {}
        for fam, name, *_ in MUTATIONS:
            fams.setdefault(fam, []).append(name)
        for f, names in fams.items():
            print(f"{f} ({len(names)})"); [print(f"    {n}") for n in names]
        return 0
    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        preflight(tools)
        rc, out = run_suite(tools, "test_")
        if rc != 0:
            print(out[-2500:]); sys.exit("HARNESS DEAD: the UNMUTATED scratch copy is already failing; a red driver would grade its mutation caught for the wrong reason.")
        print("positive control: the WHOLE unmutated suite is GREEN")
        fam, name, old, new, sel, tgt = sentinel_for(tools)
        clean, err = apply_mutation(tools, old, new, tgt)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc, _ = run_suite(tools, sel)
        open(os.path.join(tools, tgt), "w", encoding="utf-8").write(clean)
        if rc == NOTHING_COLLECTED:
            sys.exit("HARNESS DEAD: the sentinel selected NO TESTS (pytest rc 5).")
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED.")
        print("sentinel: reddened as required\n")
        muts = [m for m in MUTATIONS if not args.family or m[0] == args.family]
        caught, survived, broken = [], [], []
        for fam, name, old, new, sel in muts:
            clean, err = apply_mutation(tools, old, new)
            if err:
                broken.append((fam, name, err)); print(f"  BROKEN   {fam}/{name}: {err}"); continue
            rc, out = run_suite(tools, sel)
            open(os.path.join(tools, PROMOTE), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append((fam, name, "collected no tests")); print(f"  BROKEN   {fam}/{name}: collected no tests")
            elif rc == 0:
                survived.append((fam, name, sel)); print(f"  SURVIVED {fam}/{name}   (driver: {sel})")
            else:
                caught.append((fam, name)); print(f"  caught   {fam}/{name}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        for f, n, e in broken: print(f"  BROKEN {f}/{n}: {e}")
        for f, n, s in survived: print(f"  SURVIVED {f}/{n}  (driver was: {s})")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
