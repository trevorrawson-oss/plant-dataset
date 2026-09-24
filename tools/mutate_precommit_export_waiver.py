#!/usr/bin/env python3
"""mutate_precommit_export_waiver -- mutation harness for the pre-commit hook's EXPORT_WAIVERS
(PLA-581, ruled 2026-09-24: waive the exact known E1 case, fail on everything else).

PLA-215 bar: one defect per guard injected into a SCRATCH COPY of precommit_release_verify.py; its
driver in test_precommit_export_waiver.py must go RED. Liveness: anchor preflight, MUTATION-APPLIED
marker on disk, a sentinel that MUST redden, a positive control that runs the WHOLE waiver suite AND
the existing script-style hook test (as a script, never under pytest), bytecode off, pytest rc 5
graded BROKEN.

Usage: mutate_precommit_export_waiver.py
"""
import os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TARGET = "precommit_release_verify.py"
SUITE = "test_precommit_export_waiver.py"
SCRIPT = "test_precommit_release_verify.py"
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5

CHAR = '        "character": re.compile(r"^E1 app-provenance: export was built from canonical d7b33682f992 "'
MATCH = '        hit = next((name for name, w in waivers.items() if w["character"].search(v)), None)'
STALE = '    return unwaived, waived, [n for n in waivers if n not in fired]'
WIRE_BLOCK = '            stale_export = unwaived'
WIRE_APPLY = '            unwaived, waived, stale_waivers = apply_export_waivers(export_currency_concerns(staged))'

MUTATIONS = [
    ("waiver_never_matches", CHAR, CHAR.replace("d7b33682f992", "NEVERMATCHES") + "  " + MARKER,
     "test_the_known_stale_export_is_waived"),
    ("character_dropped_any_stale_sha_waived", CHAR, CHAR.replace("d7b33682f992", "[0-9a-f]{12}") + "  " + MARKER,
     "test_a_different_stale_sha_is_not_waived"),
    ("frozen_prefix_shortened", CHAR, CHAR.replace("d7b33682f992", "d7b33682[0-9a-f]{4}") + "  " + MARKER,
     "test_the_character_needs_the_whole_frozen_prefix"),
    ("every_violation_waived_including_e2", MATCH,
     "        hit = next(iter(waivers), None)  " + MARKER, "test_e2_is_never_waived"),
    ("stale_waiver_never_reported", STALE, "    return unwaived, waived, []  " + MARKER,
     "test_a_current_export_has_nothing_to_waive_and_the_waiver_reads_stale"),
    ("unwaived_violations_do_not_block", WIRE_BLOCK, "            stale_export = []  " + MARKER,
     "test_main_blocks_on_an_unwaived_export"),
    ("waiver_not_consulted_by_the_hook", WIRE_APPLY,
     "            unwaived, waived, stale_waivers = export_currency_concerns(staged), [], []  " + MARKER,
     "test_main_passes_on_the_waived_export"),
]


def run(tools, selector=None, script=False):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if script:
        r = subprocess.run([sys.executable, "-B", os.path.join(tools, SCRIPT)],
                           capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    else:
        r = subprocess.run([sys.executable, "-B", "-m", "pytest", os.path.join(tools, SUITE), "-q",
                            "-k", selector or "test_", "--no-header", "-p", "no:cacheprovider"],
                           capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode, r.stdout + r.stderr


def apply(tools, old, new):
    p = os.path.join(tools, TARGET)
    clean = open(p, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times"
    open(p, "w", encoding="utf-8").write(clean.replace(old, new, 1))
    if MARKER not in open(p, encoding="utf-8").read():
        return None, "mutation not on disk"
    return clean, None


def main():
    tmp = tempfile.mkdtemp(prefix="mut_exportwaiver_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    try:
        for f in os.listdir(HERE):
            if f.endswith(".py") and os.path.isfile(os.path.join(HERE, f)):
                shutil.copy2(os.path.join(HERE, f), os.path.join(tools, f))
        for name in ("crops_data_final.json", ".git", "CLAUDE.md"):
            os.symlink(os.path.join(REPO, name), os.path.join(tmp, name))
        src = open(os.path.join(tools, TARGET), encoding="utf-8").read()
        bad = [n for n, old, _, _ in MUTATIONS if src.count(old) != 1]
        if bad:
            sys.exit(f"HARNESS DEAD: anchor preflight failed for {bad}")
        print(f"anchor preflight: {len(MUTATIONS)}/{len(MUTATIONS)} anchors match exactly once")
        for script in (False, True):
            rc, out = run(tools, script=script)
            if rc != 0:
                print(out[-2000:])
                sys.exit(f"HARNESS DEAD: the unmutated {'script' if script else 'suite'} is already failing")
        print(f"positive control: the WHOLE unmutated {SUITE} AND {SCRIPT} (as a script) are GREEN")
        # sentinel: break the suite's own FROZEN pin; the waived-export driver must redden
        sp = os.path.join(tools, SUITE)
        clean = open(sp, encoding="utf-8").read()
        m = re.search(r'^FROZEN = "[0-9a-f]{64}"', clean, re.M)
        if not m:
            sys.exit("HARNESS DEAD: cannot locate the FROZEN pin for the sentinel")
        open(sp, "w", encoding="utf-8").write(clean.replace(m.group(0), 'FROZEN = "' + "0" * 64 + '"  ' + MARKER, 1))
        rc, _ = run(tools, "test_the_known_stale_export_is_waived")
        open(sp, "w", encoding="utf-8").write(clean)
        if rc == NOTHING_COLLECTED:
            sys.exit("HARNESS DEAD: the sentinel selected NO TESTS")
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel mutation SURVIVED")
        print("sentinel: reddened as required\n")
        caught, survived, broken = [], [], []
        for name, old, new, sel in MUTATIONS:
            clean_t, err = apply(tools, old, new)
            if err:
                broken.append((name, err)); print(f"  BROKEN   {name}: {err}"); continue
            rc, _ = run(tools, sel)
            open(os.path.join(tools, TARGET), "w", encoding="utf-8").write(clean_t)
            if rc == NOTHING_COLLECTED:
                broken.append((name, "collected no tests")); print(f"  BROKEN   {name}: no tests")
            elif rc == 0:
                survived.append(name); print(f"  SURVIVED {name}  (driver {sel})")
            else:
                caught.append(name); print(f"  caught   {name}")
        print(f"\n{len(MUTATIONS)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
