#!/usr/bin/env python3
"""mutate_pla8_batch27_suite -- mutation harness for the PLA-8 batch 27 promote suite.

BUILT TO THE PLA-215 BAR. It injects one defect per guard family into a SCRATCH COPY of the promote
source, runs the suite's own drivers against the mutated copy, and requires each to go RED. A
mutation that survives is a guard the suite does not actually test.

THE LIVENESS DEFENSE, and why it is not optional. PLA-138's harness dedented an already-indented
template, silently ran the CLEAN fixture, and reported every mutation as surviving. Batch 25's
harness reported 34/34 while dead. Batch 26's exited HARNESS DEAD on its first run, which is the
behaviour to expect from a working one. So this harness:

  1. ANCHOR PREFLIGHT. Every anchor must match EXACTLY ONCE in the clean source before anything is
     graded. An anchor matching zero times edits nothing and reports a false survivor; an anchor
     matching twice edits a site nobody intended and reports a catch for the wrong reason.
  2. Writes a MUTATION-APPLIED marker and asserts it is on disk, and that the bytes changed.
  3. Runs a SENTINEL that MUST redden, or exits HARNESS DEAD.
  4. Runs a POSITIVE CONTROL: the unmutated copy must be GREEN.
  5. Disables bytecode and clears __pycache__ before every run. Stale bytecode silently imports the
     CLEAN module and reports every mutation as surviving.

WHY PER-MUTATION TEST SELECTION. Each mutation names the driver that SHOULD catch it, and only that
driver runs. The selection IS the assertion: a mutation counts as caught only if ITS OWN driver
reddens, not if some other test happens to fall over.

Usage:
    mutate_pla8_batch27_suite.py             # all families
    mutate_pla8_batch27_suite.py --family X  # one family
    mutate_pla8_batch27_suite.py --list
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
PROMOTE = "promote_pla8_batch27.py"
SUITE = "test_promote_pla8_batch27.py"
STAGING = "pla8_batch27_microgreens"
MARKER = "# MUTATION-APPLIED"

# (family, name, old, new, pytest -k selector)
MUTATIONS = [
    # ---- rule 1: the schema pin
    ("schema", "name_key_no_longer_refused",
     'if "name" in e:\n            raise SystemExit(f"REFUSED: {crop}/{field} entry carries a \'name\' key',
     'if False:\n            raise SystemExit(f"REFUSED: {crop}/{field} entry carries a \'name\' key  ' + MARKER,
     "test_refuses_when_a_name_key_appears"),
    ("schema", "existing_id_silently_overwritten",
     "for k in PINNED_FIELDS:\n            if k in e:",
     "for k in PINNED_FIELDS:\n            if False:  " + MARKER,
     "test_refuses_when_an_entry_already_has_an_id"),
    ("schema", "name_seasoned_drift_ignored",
     "if entry_name(e) != row[\"name_seasoned\"]:",
     "if False:  " + MARKER,
     "test_refuses_a_name_seasoned_drift"),

    # ---- rule 2: ids are reused, never minted
    ("ids", "minted_id_accepted",
     "if pid not in outside:",
     "if False:  " + MARKER,
     "test_refuses_a_minted_id"),
    ("ids", "precedent_link_not_required",
     "if PRECEDENT not in outside[pid]:",
     "if False:  " + MARKER,
     "test_refuses_an_id_the_precedent_does_not_carry"),

    # ---- ladder integrity
    ("ladders", "unknown_method_accepted",
     "if m is None:\n                        raise SystemExit(f\"REFUSED: {crop}/{e['id']} names unknown method {mid!r}\")",
     "if m is None:\n                        continue  " + MARKER,
     "test_refuses_an_unknown_method"),
    ("ladders", "tier_inversion_accepted",
     "if any(ranks[i] > ranks[i + 1] for i in range(len(ranks) - 1)):",
     "if any(ranks[i] > ranks[i + 1] for i in range(0)):  " + MARKER,
     "test_refuses_a_tier_inversion"),
    ("ladders", "applies_to_incoherence_accepted",
     "if UNIVERSAL_TARGET not in targets and not (targets & TYPE_TARGETS[ptype]):",
     "if False:  " + MARKER,
     "test_refuses_an_applies_to_mismatch"),
    ("ladders", "empty_ladder_accepted",
     "if not isinstance(ladder, list) or not ladder:",
     "if not isinstance(ladder, list):  " + MARKER,
     "test_refuses_an_empty_ladder"),
    ("ladders", "repeated_method_accepted",
     "if mid in seen:",
     "if False:  " + MARKER,
     "test_refuses_a_repeated_method"),

    # ---- rule 4: the raw-crop safety refusal
    ("safety", "material_rung_admitted",
     "if TIER_RANK[tier] > MAX_TIER_RANK:",
     "if False:  " + MARKER,
     "test_refuses_a_soft_chemical_rung"),
    ("safety", "max_tier_raised_to_conventional",
     'MAX_TIER_RANK = TIER_RANK["physical"]',
     'MAX_TIER_RANK = TIER_RANK["conventional"]  ' + MARKER,
     "test_refuses_a_soft_chemical_rung"),

    # ---- rule 5: the unsourced root-hair claim
    ("root_hair", "claim_no_longer_refused",
     "if ROOT_HAIR.search(text):",
     "if False:  " + MARKER,
     "test_refuses_the_root_hair_claim"),
    ("root_hair", "regex_cannot_match",
     'ROOT_HAIR = re.compile(r"root\\s*hairs?", re.I)',
     'ROOT_HAIR = re.compile(r"zzzznevermatches")  ' + MARKER,
     "test_refuses_the_root_hair_claim"),

    # ---- PLA-457
    ("pla457", "sulfur_oil_interval_admitted",
     "if SULFUR.search(s) and OIL.search(s) and DURATION.search(s):",
     "if False:  " + MARKER,
     "test_refuses_a_sulfur_oil_interval"),

    # ---- copy guards
    ("copy", "ratio_threshold_disabled",
     "COPY_THRESHOLD = 0.70",
     "COPY_THRESHOLD = 2.00  " + MARKER,
     "test_refuses_a_lift_from_the_precedent_ladder"),
    ("copy", "ngram_run_check_disabled",
     "shared = {g for g in (tg & dg) if not _is_figure_run(g)}",
     "shared = set()  " + MARKER,
     "test_refuses_a_short_run_lifted_from_the_crops_own_prose"),
    ("copy", "figure_exemption_swallows_everything",
     "return any(ch.isdigit() for ch in gram)",
     "return True  " + MARKER,
     "test_figure_runs_are_exempt"),
    ("copy", "similarity_made_asymmetric",
     "return max(difflib.SequenceMatcher(None, a, b).ratio(),\n               difflib.SequenceMatcher(None, b, a).ratio())",
     "return difflib.SequenceMatcher(None, a, b).ratio()  " + MARKER,
     "test_similarity_is_symmetric"),
    ("copy", "precedent_dropped_from_the_donor_set",
     "for slug in CROPS + (PRECEDENT,):",
     "for slug in CROPS:  " + MARKER,
     "test_refuses_a_lift_from_the_precedent_ladder"),
    ("copy", "intra_batch_twin_accepted",
     "if r >= TWIN_THRESHOLD:",
     "if False:  " + MARKER,
     "test_refuses_a_propagated_note"),

    # ---- registers and house style
    ("registers", "identical_registers_accepted",
     "if b.strip() == s.strip():",
     "if False:  " + MARKER,
     "test_refuses_identical_registers"),
    ("registers", "reword_accepted",
     "if _sym(b, s) >= 0.90:",
     "if False:  " + MARKER,
     "test_refuses_a_reworded_register"),
    ("hygiene", "em_dash_accepted",
     "if DASHES.search(text):",
     "if False:  " + MARKER,
     "test_refuses_an_em_dash"),
    ("hygiene", "absolute_accepted",
     "if ABSOLUTES.search(text):",
     "if False:  " + MARKER,
     "test_refuses_an_absolute"),
    ("hygiene", "ladder_vocabulary_accepted",
     "if LADDER_VOCAB.search(text):",
     "if False:  " + MARKER,
     "test_refuses_ladder_vocabulary"),
    ("hygiene", "spaced_degree_accepted",
     "if SPACED_F.search(text):",
     "if False:  " + MARKER,
     "test_refuses_a_spaced_degree"),

    # ---- blast radius
    ("blast", "set_comparison_removed",
     "if added != set(PINNED_FIELDS):",
     "if False:  " + MARKER,
     "test_set_comparison_runs_before_value_comparison"),
    ("blast", "roster_change_invisible",
     'if {c["slug"] for c in pre["crops"]} != {c["slug"] for c in post["crops"]}:',
     "if False:  " + MARKER,
     "test_refuses_a_roster_change"),
    ("blast", "untouched_crop_change_invisible",
     'if json.dumps(pre_i[slug], sort_keys=True) != json.dumps(post_i[slug], sort_keys=True):\n            raise SystemExit(f"REFUSED: untouched crop {slug} changed")',
     "if False:\n            raise SystemExit(f\"REFUSED: untouched crop {slug} changed\")  " + MARKER,
     "test_refuses_a_touched_untouched_crop"),
    ("blast", "top_level_change_invisible",
     'raise SystemExit(f"REFUSED: top-level key {k!r} changed")',
     'pass  ' + MARKER,
     "test_refuses_a_touched_top_level_key"),
    ("blast", "carried_prose_change_invisible",
     'if json.dumps(g[k], sort_keys=True) != json.dumps(s[k], sort_keys=True):\n                        raise SystemExit(f"REFUSED: {crop}/{entry_name(g)!r} carried field {k!r} "',
     'if False:\n                        raise SystemExit(f"REFUSED: {crop}/{entry_name(g)!r} carried field {k!r} "  ' + MARKER,
     "test_refuses_a_touched_prose_field"),
    ("blast", "ladder_mismatch_invisible",
     'if g["control_ladder"] != authored[row["id"]]["control_ladder"]:',
     "if False:  " + MARKER,
     "test_refuses_a_ladder_that_does_not_match_the_authored_output"),

    # ---- serializer and base-SHA entry point
    ("serialize", "indent_reintroduced",
     'return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     'return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_one_serializer_shared_with_the_suite"),
    ("serialize", "ascii_escaping_reintroduced",
     'return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     'return json.dumps(data, separators=(",", ":"), ensure_ascii=True).encode("utf-8")  ' + MARKER,
     "test_one_serializer_shared_with_the_suite"),
    ("entry", "base_sha_check_removed",
     "if got != BASE_SHA:",
     "if False:  " + MARKER,
     "test_main_refuses_a_moved_base"),
]


def sentinel_for(tools_dir):
    """Built from the CURRENT pin value, so a legitimate pin move does not permanently break the
    sentinel and invite someone to delete it."""
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r"^N_RUNGS = (\d+)$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_RUNGS pin to build a sentinel from")
    return ("sentinel", "rung_count_pin_broken",
            m.group(0), f"N_RUNGS = {int(m.group(1)) + 99999}  " + MARKER,
            "test_the_batch_is_the_shape_measured", SUITE)


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
    tmp = tempfile.mkdtemp(prefix="mut_b27_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"),
               os.path.join(tmp, "crops_data_final.json"))
    # promote_fixture.pre_state shells out to `git show` with cwd=REPO, and REPO is derived from
    # the fixture's own path. Without a .git the fixture raises, the positive control fails, and
    # the harness dies -- correctly, but for the wrong reason. Link the real object store in.
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    shutil.copytree(os.path.join(HERE, "staging", STAGING),
                    os.path.join(tools, "staging", STAGING))
    return tmp, tools


def run_suite(tools_dir, selector, target_file=PROMOTE):
    """STALE BYTECODE IS A DEAD HARNESS: CPython's source-mtime cache has one-second granularity,
    so a rapid rewrite can leave a __pycache__ entry that still looks current and the suite
    silently imports the CLEAN module."""
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

        rc, out = run_suite(tools, "test_the_batch_is_the_shape_measured")
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
