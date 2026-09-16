#!/usr/bin/env python3
"""mutate_pla465_plant_dimensions_suite -- mutation harness for the PLA-465 plant-dimensions promote suite.

BUILT TO THE PLA-215 BAR: one defect per guard family injected into a SCRATCH COPY of the promote source;
the suite's own driver for that guard must go RED. Liveness: anchor preflight (each anchor exactly once),
MUTATION-APPLIED marker on disk, a sentinel that MUST redden, a positive control that must be GREEN,
bytecode off, pytest rc 5 graded BROKEN.

NOT COUNTED (removed from the promote rather than shipped unreachable): the shell count (ROSTER minus
the pinned certified count), the closing key/authored/null totals (implied by the per-crop checks), and
pair validity in check_spec_shape (the imported gate owns it, run on a synthetic in check_pre_state).

Usage: mutate_pla465_plant_dimensions_suite.py [--family X] [--list]
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_pla465_plant_dimensions.py"
SUITE = "test_promote_pla465_plant_dimensions.py"
STAGING = "pla465_plant_dimensions"
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5


def off(line):
    m = re.match(r"^(\s*)(if|elif) (.*):$", line)
    assert m, line
    return f"{m.group(1)}{m.group(2)} False:  {MARKER}"


def off2(two):
    """A two-line anchor whose SECOND line is the guard (the first disambiguates a repeated `if`)."""
    a, b = two.split("\n")
    return a + "\n" + off(b)


def off1of2(two):
    """A two-line anchor whose FIRST line is the guard and the second is its raise/continue."""
    a, b = two.split("\n")
    return off(a) + "\n" + b


A = {
 "entry": "    if got != BASE_SHA:",
 "spec_base": '    if spec.get("base_sha") != BASE_SHA:',
 "authored_count": "    if expected_authored is None or len(rows) != expected_authored:",
 "dup_crop": '        if r["crop"] in seen:',
 "row_keys": '        if set(r) != {"crop", "mature_height_ft", "mature_spread_ft", "field_addition"}:',
 "no_height": '        if r["mature_height_ft"] is None:',
 "fa_shape": '        if set(fa) != set(FA_KEYS) or fa["field"] != FA_FIELD:',
 "fa_date": '        if fa["date"] != FA_DATE:',
 "fa_sources": '        if not fa["sources"]:',
 "fa_note": '        if not (fa["note"] or "").strip() or "http" not in fa["note"]:',
 "expected": '    if spec["expected"] != {"keys": EXPECTED_KEYS, "authored": expected_authored, "null": EXPECTED_KEYS - expected_authored, "shells": EXPECTED_SHELLS}:',
 "roster": '    if len(data["crops"]) != ROSTER:',
 "certified_count": "    if len(certified) != EXPECTED_KEYS:",
 "existing_key": '            if f in c:\n                raise SystemExit(f"REFUSED: {c[\'slug\']} already carries {f}")',
 "fa_list": "        if _certified(c) and not isinstance(fa, list):",
 "prior_record": '        if any(isinstance(x, dict) and x.get("field") == FA_FIELD for x in (fa or [])):',
 "off_roster": "        if c is None:",
 "not_certified": '        if not _certified(c):\n            raise SystemExit(f"REFUSED: authored crop {r[\'crop\']} is not certified")',
 "not_woody": '        if c.get("archetype") not in WOODY:',
 "catalog": "            if s not in catalog:",
 "gate_on_row": "        v = PDG.shape_violations(syn)\n        if v:",
 "bounds_on_row": "        nv = numeric_sanity_violations(syn)\n        if nv:",
 "gate_on_post": "    v = PDG.all_violations(post, presence=True)\n    if v:",
 "bounds_on_post": '        nv = numeric_sanity_violations(idx[r["crop"]])\n        if nv:',
 "display_on_post": "        if dv:",
 "top_keys": "    if set(pre) != set(post):",
 "top_change": '        if k != "crops" and _j(pre[k]) != _j(post[k]):',
 "roster_change": '    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):',
 "shell_change": '            if _j(s) != _j(g):\n                raise SystemExit(f"REFUSED: shell {slug} changed")',
 "crop_keys": "        if set(g) != set(s) | set(FIELDS):",
 "outside_change": '            if _j(s[k]) != _j(g[k]):\n                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside the declared keys")',
 "footprint": '        if g["footprint_inches"] is not None:',
 "value_vs_spec": '            if _j(g["mature_height_ft"]) != _j(r["mature_height_ft"]) or _j(g["mature_spread_ft"]) != _j(r["mature_spread_ft"]):',
 "value_no_row": '            if g["mature_height_ft"] is not None or g["mature_spread_ft"] is not None:',
 "vs_keys": "        if set(sv) != set(gv):",
 "vs_change": '            if k != "field_additions" and _j(sv[k]) != _j(gv[k]):',
 "prefix": "        if _j(b[:len(a)]) != _j(a):",
 "tail": "        if _j(b[len(a):]) != _j(want_tail):",
}
MUTATIONS = [
 ("entry", "base_sha_check_removed", A["entry"], off(A["entry"]), "test_refuses_a_canonical_that_is_not_the_base"),
 ("spec", "spec_base_not_checked", A["spec_base"], off(A["spec_base"]), "test_refuses_a_spec_on_another_base"),
 ("spec", "authored_count_not_pinned", A["authored_count"], off(A["authored_count"]), "test_refuses_an_authored_count_drift"),
 ("spec", "duplicate_crop_accepted", A["dup_crop"], off(A["dup_crop"]), "test_refuses_a_duplicated_crop"),
 ("spec", "row_keys_not_checked", A["row_keys"], off(A["row_keys"]), "test_refuses_a_row_with_the_wrong_keys"),
 ("spec", "heightless_row_accepted", A["no_height"], off(A["no_height"]), "test_refuses_an_authored_row_with_no_height"),
 ("spec", "fa_shape_not_checked", A["fa_shape"], off(A["fa_shape"]), "test_refuses_a_field_addition_shape"),
 ("spec", "fa_date_not_pinned", A["fa_date"], off(A["fa_date"]), "test_refuses_a_field_addition_date"),
 ("spec", "sourceless_fa_accepted", A["fa_sources"], off(A["fa_sources"]), "test_refuses_a_field_addition_without_sources"),
 ("spec", "pageless_note_accepted", A["fa_note"], off(A["fa_note"]), "test_refuses_a_note_that_names_no_page"),
 ("spec", "expected_block_not_compared", A["expected"], off(A["expected"]), "test_refuses_an_expected_block_drift"),
 ("prestate", "roster_not_pinned", A["roster"], off(A["roster"]), "test_refuses_a_roster_drift"),
 ("prestate", "certified_count_not_pinned", A["certified_count"], off(A["certified_count"]), "test_refuses_a_certified_count_drift"),
 ("prestate", "existing_key_accepted", A["existing_key"], off1of2(A["existing_key"]), "test_refuses_a_crop_already_carrying_a_key"),
 ("prestate", "fa_list_not_checked", A["fa_list"], off(A["fa_list"]), "test_refuses_field_additions_not_a_list"),
 ("prestate", "prior_record_accepted", A["prior_record"], off(A["prior_record"]), "test_refuses_a_prior_plant_dimensions_record"),
 ("prestate", "off_roster_accepted", A["off_roster"], off(A["off_roster"]), "test_refuses_an_authored_crop_off_the_roster"),
 ("prestate", "shell_authoring_accepted", A["not_certified"], off1of2(A["not_certified"]), "test_refuses_an_authored_shell"),
 ("prestate", "herbaceous_authoring_accepted", A["not_woody"], off(A["not_woody"]), "test_refuses_an_authored_herbaceous_crop"),
 ("prestate", "catalog_not_checked", A["catalog"], off(A["catalog"]), "test_refuses_a_source_not_in_catalog"),
 ("prestate", "gate_not_run_on_row", A["gate_on_row"], off2(A["gate_on_row"]), "test_refuses_a_row_the_gate_rejects"),
 ("prestate", "bounds_not_run_on_row", A["bounds_on_row"], off2(A["bounds_on_row"]), "test_refuses_a_row_the_bounds_reject"),
 ("post", "gate_not_run_on_post", A["gate_on_post"], off2(A["gate_on_post"]), "test_refuses_a_post_state_that_fails_the_gate"),
 ("post", "bounds_not_run_on_post", A["bounds_on_post"], off2(A["bounds_on_post"]), "test_refuses_an_authored_crop_that_fails_the_bounds"),
 ("post", "display_not_run_on_post", A["display_on_post"], off(A["display_on_post"]), "test_refuses_an_authored_crop_that_fails_display_readiness"),
 ("blast", "top_level_key_set_not_compared", A["top_keys"], off(A["top_keys"]), "test_refuses_a_top_level_key_addition"),
 ("blast", "top_level_change_invisible", A["top_change"], off(A["top_change"]), "test_refuses_a_top_level_change"),
 ("blast", "roster_change_invisible", A["roster_change"], off(A["roster_change"]), "test_refuses_a_roster_change"),
 ("blast", "shell_change_invisible", A["shell_change"], off1of2(A["shell_change"]), "test_refuses_a_shell_change"),
 ("blast", "crop_key_set_not_compared", A["crop_keys"], off(A["crop_keys"]), "test_refuses_a_crop_level_key_set_drift"),
 ("blast", "outside_change_invisible", A["outside_change"], off1of2(A["outside_change"]), "test_refuses_a_change_outside_the_declared_keys"),
 ("blast", "footprint_not_checked", A["footprint"], off(A["footprint"]), "test_refuses_a_non_null_footprint"),
 ("blast", "value_not_compared_to_spec", A["value_vs_spec"], off(A["value_vs_spec"]), "test_refuses_a_written_value_other_than_the_spec_row"),
 ("blast", "rowless_value_accepted", A["value_no_row"], off(A["value_no_row"]), "test_refuses_a_dimension_on_a_crop_with_no_row"),
 ("blast", "vs_key_set_not_compared", A["vs_keys"], off(A["vs_keys"]), "test_refuses_a_verification_status_key_addition"),
 ("blast", "vs_change_invisible", A["vs_change"], off(A["vs_change"]), "test_refuses_a_verification_status_value_change"),
 ("blast", "prefix_not_compared", A["prefix"], off(A["prefix"]), "test_refuses_a_rewritten_field_additions_prefix"),
 ("blast", "tail_not_compared", A["tail"], off(A["tail"]), "test_refuses_a_record_other_than_the_spec or test_refuses_an_extra_appended_record"),
 ("serialize", "indent_reintroduced",
  '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
  '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER, "test_compact_no_trailing_newline"),
]


def sentinel_for(tools_dir):
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_KEYS = (\d+)$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_KEYS pin to build a sentinel from")
    return ("sentinel", "keys_pin_broken", m.group(0), f"N_KEYS = {int(m.group(1)) + 99999}  " + MARKER, "test_pins_are_the_literals", SUITE)


def preflight(tools_dir):
    src = open(os.path.join(tools_dir, PROMOTE), encoding="utf-8").read()
    bad = [f"  {fam}/{name}: anchor matches {src.count(old)} times\n      {old[:90]!r}" for fam, name, old, _n, _s in MUTATIONS if src.count(old) != 1]
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_pla465_")
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
        # THE POSITIVE CONTROL IS THE WHOLE SUITE, not two tests: a driver that is red on the CLEAN copy would
        # otherwise grade its mutation "caught" for the wrong reason (found here 2026-09-16: a display_readiness
        # driver nulled the gallons on a crop that also carried a tray depth and was red before any mutation).
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
                broken.append((fam, name, f"driver {sel!r} collected NO TESTS")); print(f"  BROKEN   {fam}/{name}: collected no tests")
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
