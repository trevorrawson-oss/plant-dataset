#!/usr/bin/env python3
"""mutate_container_citation_floor_suite -- mutation harness for the PLA-533 ratchet gate.

BUILT TO THE PLA-215 BAR: one defect per guard family injected into a SCRATCH COPY of the gate
source; the suite's own driver for that guard must go RED. Liveness: anchor preflight (each anchor
exactly once), MUTATION-APPLIED marker on disk, a sentinel that MUST redden, a positive control
that runs the WHOLE suite, bytecode off, pytest rc 5 graded BROKEN.

Trevor's two named proofs are drivers here by name:
  * adding a fifth must FAIL   -> test_PROOF_adding_a_fifth_FAILS
  * closing one must PASS      -> test_PROOF_closing_one_PASSES_at_the_lower_count

Usage: mutate_container_citation_floor_suite.py [--list]
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GATE = "container_citation_floor_gate.py"
SUITE = "test_container_citation_floor_gate.py"
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5


def off(line):
    m = re.match(r"^(\s*)(if|elif) (.*):$", line)
    assert m, line
    return f"{m.group(1)}{m.group(2)} False:  {MARKER}"


MUTATIONS = [
    # --- scope: who is in the population at all -------------------------------------------------
    ("scope", "shells_counted",
     "    if not _certified(crop):\n        return False",
     "    if False:  " + MARKER + "\n        return False",
     "test_an_uncertified_shell_is_exempt"),
    ("scope", "null_figure_counted",
     "    if cn.get(FIELD) is None:\n        return False",
     "    if False:  " + MARKER + "\n        return False",
     "test_a_null_min_pot_gallons_is_out_of_scope"),

    # --- the two halves of "uncited" -------------------------------------------------------------
    ("uncited", "missing_anchors_ignored",
     '    return not (cn.get("sources") or []) or not (cn.get("anchoring_urls") or {})',
     '    return not (cn.get("sources") or [])  ' + MARKER,
     "test_sources_without_anchors_is_uncited"),
    ("uncited", "missing_sources_ignored",
     '    return not (cn.get("sources") or []) or not (cn.get("anchoring_urls") or {})',
     '    return not (cn.get("anchoring_urls") or {})  ' + MARKER,
     "test_anchors_without_sources_is_uncited"),
    ("uncited", "nothing_is_ever_uncited",
     '    return not (cn.get("sources") or []) or not (cn.get("anchoring_urls") or {})',
     "    return False  " + MARKER,
     "test_live_canonical_is_exactly_the_known_four"),

    # --- THE RATCHET ITSELF ----------------------------------------------------------------------
    ("ratchet", "growth_and_substitution_invisible",
     "        if slug not in KNOWN:",
     "        if False:  " + MARKER,
     "test_PROOF_adding_a_fifth_FAILS or test_swapping_one_for_another_still_FAILS "
     "or test_giving_a_null_crop_a_figure_without_a_citation_FAILS"),
    ("ratchet", "ceiling_not_enforced",
     "    if len(live) > CEILING:",
     "    if False:  " + MARKER,
     "test_the_count_check_fires_on_a_KNOWN_CEILING_desync"),
    ("ratchet", "ratchet_inverted_shrinking_refused",
     "        if slug not in KNOWN:",
     "        if slug in KNOWN:  " + MARKER,
     "test_live_canonical_passes or test_PROOF_closing_one_PASSES_at_the_lower_count"),

    # --- the pins ---------------------------------------------------------------------------------
    ("pins", "ceiling_raised",
     "CEILING = 4",
     "CEILING = 99  " + MARKER,
     "test_ceiling_and_known_set_are_the_measured_four"),
    ("pins", "known_widened",
     '    "dry-bean",           # 5 gal (also recommended 5, depth 8) -- sibling of green-beans-bush',
     '    "dry-bean", "cabbage",  ' + MARKER,
     "test_ceiling_and_known_set_are_the_measured_four or test_the_two_pins_are_in_sync_as_shipped"),
]


def sentinel_for(tools_dir):
    src = open(os.path.join(tools_dir, SUITE), encoding="utf-8").read()
    m = re.search(r'^CITED_VICTIM = "cabbage"$', src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the CITED_VICTIM pin to build a sentinel from")
    return ("sentinel", "victim_pin_broken", m.group(0),
            'CITED_VICTIM = "no-such-crop"  ' + MARKER, "test_a_cited_crop_is_not_in_the_population",
            SUITE)


def preflight(tools_dir):
    src = open(os.path.join(tools_dir, GATE), encoding="utf-8").read()
    bad = [f"  {fam}/{name}: anchor matches {src.count(old)} times\n      {old[:90]!r}"
           for fam, name, old, _n, _s in MUTATIONS if src.count(old) != 1]
    if bad:
        sys.exit("HARNESS DEAD: anchor preflight failed.\n" + "\n".join(bad))
    print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")


def build_scratch():
    tmp = tempfile.mkdtemp(prefix="mut_ccf_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    for f in os.listdir(HERE):
        src = os.path.join(HERE, f)
        if os.path.isfile(src) and (f.endswith(".py") or f.endswith(".json")):
            shutil.copy2(src, os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"),
               os.path.join(tmp, "crops_data_final.json"))
    os.symlink(os.path.join(REPO, ".git"), os.path.join(tmp, ".git"))
    return tmp, tools


def run_suite(tools_dir, selector, suite=SUITE):
    shutil.rmtree(os.path.join(tools_dir, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", os.path.join(tools_dir, suite),
                        "-q", "-k", selector, "--no-header", "-p", "no:cacheprovider"],
                       capture_output=True, text=True, cwd=os.path.dirname(tools_dir), env=env)
    return r.returncode, r.stdout + r.stderr


def apply_mutation(tools_dir, old, new, target=GATE):
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
    ap = argparse.ArgumentParser(); ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        for fam, name, *_ in MUTATIONS:
            print(f"{fam}/{name}")
        print(f"\n{len(MUTATIONS)} mutations")
        return 0

    tmp, tools = build_scratch()
    print(f"scratch: {tools}\n")
    try:
        preflight(tools)
        rc, out = run_suite(tools, "test_")
        if rc != 0:
            print(out[-2000:])
            sys.exit("HARNESS DEAD: the UNMUTATED scratch copy is already failing; a red driver "
                     "would grade its mutation caught for the wrong reason.")
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

        caught, survived, broken = [], [], []
        for fam, name, old, new, sel in MUTATIONS:
            clean, err = apply_mutation(tools, old, new)
            if err:
                broken.append((fam, name, err)); print(f"  BROKEN   {fam}/{name}: {err}"); continue
            rc, out = run_suite(tools, sel)
            open(os.path.join(tools, GATE), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append((fam, name, f"driver {sel!r} collected NO TESTS"))
                print(f"  BROKEN   {fam}/{name}: collected no tests")
            elif rc == 0:
                survived.append((fam, name, sel)); print(f"  SURVIVED {fam}/{name}  (driver: {sel})")
            else:
                caught.append((fam, name)); print(f"  caught   {fam}/{name}")
        print(f"\n{len(MUTATIONS)} injected: {len(caught)} caught, {len(survived)} survived, "
              f"{len(broken)} broken")
        for f, n, e in broken:
            print(f"  BROKEN {f}/{n}: {e}")
        for f, n, s in survived:
            print(f"  SURVIVED {f}/{n}  (driver was: {s})")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
