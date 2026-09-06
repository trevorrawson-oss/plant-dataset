#!/usr/bin/env python3
"""mutate_pla450_option_b_scoped_ids_suite -- mutation harness for the PLA-450 Option B promote suite.

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
    mutate_pla450_option_b_scoped_ids_suite.py             # all families
    mutate_pla450_option_b_scoped_ids_suite.py --family X  # one family
    mutate_pla450_option_b_scoped_ids_suite.py --list
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
PROMOTE = "promote_pla450_option_b_scoped_ids.py"
SUITE = "test_promote_pla450_option_b_scoped_ids.py"
STAGING = "pla450_option_b_scoped_ids"
MARKER = "# MUTATION-APPLIED"

# (family, name, old, new, pytest -k selector)
MUTATIONS = [
    # ---- entry: the base pin
    ("entry", "base_sha_check_removed",
     "    if got != BASE_SHA:", "    if False:  " + MARKER,
     "test_main_refuses_a_moved_base"),

    # ---- spec shape: the ruling, frozen
    ("spec", "row_outside_the_ruling_accepted",
     '        if r["from"] not in RULED:', "        if False:  " + MARKER,
     "test_refuses_a_row_outside_the_ruling"),
    ("spec", "wrong_crop_accepted",
     '        if r["crop"] != crop:', "        if False:  " + MARKER,
     "test_refuses_the_wrong_crop_for_a_ruled_id"),
    ("spec", "wrong_diverges_from_accepted",
     '        if r["diverges_from"] != diverges:', "        if False:  " + MARKER,
     "test_refuses_the_wrong_diverges_from"),
    ("spec", "free_form_scoped_id_accepted",
     '        if r["to"] != f"{scope}-{r[\'from\']}":', "        if False:  " + MARKER,
     "test_refuses_a_free_form_scoped_id"),
    ("spec", "missing_ruled_row_accepted",
     "    if seen_from != set(RULED):", "    if False:  " + MARKER,
     "test_refuses_a_missing_ruled_row"),
    ("spec", "non_scope_kind_accepted",
     '        if r["kind"] != "scope":', "        if False:  " + MARKER,
     "test_refuses_a_kind_other_than_scope"),

    # ---- pre-state: the vacate premise
    ("prestate", "missing_target_accepted",
     "        if len(hits) != 1:\n            raise SystemExit(f\"REFUSED: {r['crop']}/{r['field']} matched {len(hits)} entries named \"",
     "        if False:  " + MARKER + "\n            raise SystemExit(f\"REFUSED: {r['crop']}/{r['field']} matched {len(hits)} entries named \"",
     "test_refuses_a_missing_target"),
    ("prestate", "id_drift_accepted",
     '        if e.get("id") != r["from"]:', "        if False:  " + MARKER,
     "test_refuses_an_id_drift"),
    ("prestate", "unladdered_target_accepted",
     '        if not isinstance(e.get("control_ladder"), list) or not e["control_ladder"]:',
     "        if False:  " + MARKER,
     "test_refuses_a_target_with_no_ladder"),
    ("prestate", "non_singleton_generic_accepted",
     '        if holders != {r["crop"]}:', "        if False:  " + MARKER,
     "test_refuses_a_generic_id_that_is_not_a_singleton"),
    ("prestate", "existing_scoped_id_accepted",
     '        if r["to"] in ids:', "        if False:  " + MARKER,
     "test_refuses_a_scoped_id_that_already_exists"),
    ("prestate", "dead_diverges_from_accepted",
     '        if not (ids.get(r["diverges_from"], set()) - {r["crop"]}):', "        if False:  " + MARKER,
     "test_refuses_a_diverges_from_that_is_not_live"),

    # ---- the variety join
    ("variety", "dangling_reference_accepted",
     "        if pid not in ids_on[slug]:", "        if False:  " + MARKER,
     "test_refuses_a_dangling_reference"),
    ("variety", "reference_on_touched_id_accepted",
     "        if pid in touched:", "        if False:  " + MARKER,
     "test_refuses_a_reference_on_a_touched_id"),
    ("variety", "vanished_surface_accepted",
     '    if n == 0:\n        raise SystemExit("REFUSED: found zero variety references;',
     "    if False:  " + MARKER + '\n        raise SystemExit("REFUSED: found zero variety references;',
     "test_refuses_a_vanished_join_surface"),

    # ---- registry, three ways
    ("registry", "missing_adjudication_accepted",
     '        if e is None:\n            raise SystemExit(f"REFUSED: registry has no entry',
     "        if False:  " + MARKER + '\n            raise SystemExit(f"REFUSED: registry has no entry',
     "test_refuses_a_missing_adjudication"),
    ("registry", "organism_not_required",
     '            if org not in e["reason"]:', "            if False:  " + MARKER,
     "test_refuses_a_reason_that_does_not_name_both_organisms"),
    ("registry", "anchor_not_required",
     '            if anc not in e["reason"]:', "            if False:  " + MARKER,
     "test_refuses_a_reason_that_does_not_cite_its_anchor"),
    ("registry", "stale_entry_accepted",
     "        if stale:", "        if False:  " + MARKER,
     "test_refuses_an_entry_naming_a_vacated_id"),
    ("registry", "moved_pair_not_required",
     "        if frozenset((a, b)) not in by_pair:", "        if False:  " + MARKER,
     "test_refuses_a_lost_moved_pair"),

    # ---- vacate + uniqueness
    ("vacate", "surviving_generic_accepted",
     '        if r["from"] in idx:\n            raise SystemExit(f"REFUSED: generic',
     "        if False:  " + MARKER + '\n            raise SystemExit(f"REFUSED: generic',
     "test_refuses_a_generic_id_that_survives"),
    ("vacate", "scoped_id_elsewhere_accepted",
     '        if idx.get(r["to"]) != {r["crop"]}:', "        if False:  " + MARKER,
     "test_refuses_a_scoped_id_that_lands_elsewhere"),
    ("vacate", "within_crop_duplicate_accepted",
     "        if dup:", "        if False:  " + MARKER,
     "test_refuses_a_within_crop_duplicate"),

    # ---- the prediction
    ("prediction", "snapshot_staleness_accepted",
     "    if a != b:\n        raise SystemExit(\"REFUSED: staged registry snapshot differs",
     "    if False:  " + MARKER + "\n        raise SystemExit(\"REFUSED: staged registry snapshot differs",
     "test_refuses_to_write_when_the_snapshot_is_stale"),
    ("prediction", "baseline_drift_accepted",
     "    if base != PREDICTED_BASELINE:", "    if False:  " + MARKER,
     "test_refuses_a_baseline_drift"),
    ("prediction", "post_figure_mismatch_accepted",
     "    if got != PREDICTED:", "    if False:  " + MARKER,
     "test_refuses_a_post_state_whose_figures_differ"),
    ("prediction", "prediction_retuned_after_the_fact",
     'PREDICTED = {"raw": 36, "registered": 24, "actionable": 12}',
     'PREDICTED = {"raw": 36, "registered": 21, "actionable": 15}  ' + MARKER,
     "test_prediction_constants_are_the_pinned_literals"),
    ("prediction", "baseline_read_from_the_working_registry",
     "    base = collision_figures(pre, baseline_registry())",
     "    base = collision_figures(pre)  " + MARKER,
     "test_post_state_matches_the_prediction"),
    ("prediction", "baseline_registry_commit_moved_to_head",
     'BASELINE_REGISTRY_COMMIT = "074f9e2"', 'BASELINE_REGISTRY_COMMIT = "HEAD"  ' + MARKER,
     "test_baseline_registry_is_pinned_to_a_commit_not_head"),

    # ---- blast radius
    ("blast", "roster_change_invisible",
     '    if {c["slug"] for c in pre["crops"]} != {c["slug"] for c in post["crops"]}:',
     "    if False:  " + MARKER, "test_refuses_a_roster_change"),
    ("blast", "top_level_change_invisible",
     '            raise SystemExit(f"REFUSED: top-level key {k!r} changed")', "            pass  " + MARKER,
     "test_refuses_a_touched_top_level_key"),
    ("blast", "untouched_crop_change_invisible",
     '            raise SystemExit(f"REFUSED: untouched crop {slug} changed")', "            pass  " + MARKER,
     "test_refuses_a_touched_untouched_crop"),
    ("blast", "crop_level_key_set_not_compared",
     "        if set(s_crop) != set(g_crop):", "        if False:  " + MARKER,
     "test_refuses_a_crop_level_addition"),
    ("blast", "entry_key_set_not_compared",
     "                if set(s) != set(g):", "                if False:  " + MARKER,
     "test_set_comparison_runs_before_value_comparison"),
    ("blast", "entry_count_not_compared",
     "            if len(src) != len(got):", "            if False:  " + MARKER,
     "test_refuses_a_dropped_entry"),
    ("blast", "entry_order_not_compared",
     '                if g.get("name") != s.get("name"):', "                if False:  " + MARKER,
     "test_refuses_an_entry_reorder"),
    ("blast", "carried_field_change_invisible",
     "                    if json.dumps(s[k], sort_keys=True) != json.dumps(g[k], sort_keys=True):\n                        raise SystemExit(f\"REFUSED: {slug}/{s.get('name')!r} field {k!r} changed; \"",
     "                    if False:  " + MARKER + "\n                        raise SystemExit(f\"REFUSED: {slug}/{s.get('name')!r} field {k!r} changed; \"",
     "test_refuses_a_touched_prose_field"),
    ("blast", "lost_ladder_invisible",
     '                if not isinstance(g.get("control_ladder"), list) or not g["control_ladder"]:',
     "                if False:  " + MARKER, "test_refuses_a_lost_ladder"),
    ("blast", "unspecified_id_change_invisible",
     "                    if g[\"id\"] != s[\"id\"]:\n                        raise SystemExit(f\"REFUSED: {slug}/{s.get('name')!r} id changed \"",
     "                    if False:  " + MARKER + "\n                        raise SystemExit(f\"REFUSED: {slug}/{s.get('name')!r} id changed \"",
     "test_refuses_an_id_change_without_a_spec_row"),
    ("blast", "row_mismatch_invisible",
     '                    if s["id"] != r["from"] or g["id"] != r["to"]:', "                    if False:  " + MARKER,
     "test_refuses_a_rewrite_not_matching_its_row"),
    ("blast", "leaf_count_not_compared",
     "    if changed != len(rows(spec)):", "    if False:  " + MARKER,
     "test_refuses_fewer_leaves_than_rows"),

    # ---- serializer
    ("serialize", "indent_reintroduced",
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_one_serializer_shared_with_the_suite"),
    ("serialize", "ascii_escaping_reintroduced",
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=True).encode("utf-8")  ' + MARKER,
     "test_one_serializer_shared_with_the_suite"),
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
            "test_apply_changes_exactly_the_two_id_leaves", SUITE)


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
    tmp = tempfile.mkdtemp(prefix="mut_pla450b_")
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
