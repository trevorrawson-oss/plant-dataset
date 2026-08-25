#!/usr/bin/env python3
"""Mutation harness for tools/test_ladder_batch.py.

Per CLAUDE.md's PLA-215 bar: a guard is unverified until a defect has been sneaked at it. The
family cut is exactly the kind of check that reads as coverage while proving nothing -- its
predecessor grouped on problem NAMES and printed "identical prose", and no test existed to notice.

LIVENESS DEFENSE (PLA-138): every mutant is written with a MUTATION-APPLIED marker, an anchor
PREFLIGHT asserts each anchor matches exactly once before grading, and a SENTINEL mutation that
must redden proves the harness is running the mutated file at all. If the sentinel survives, the
harness is dead and the run exits HARNESS DEAD rather than reporting 'all caught'.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "ladder_batch.py")
TEST = os.path.join(HERE, "test_ladder_batch.py")
MARKER = "# MUTATION-APPLIED"

# (family, label, anchor, replacement)
MUTATIONS = [
    ("signature", "revert to the ORIGINAL defect: group on problem NAMES only",
     '''        for k in PROSE_FIELDS:
            v = p.get(k, _ABSENT)''',
     '''        for k in ():
            v = p.get(k, _ABSENT)'''),

    ("signature", "drop prevention_seasoned from PROSE_FIELDS (the County Fair field)",
     '"prevention_beginner", "prevention_seasoned",',
     '"prevention_beginner",'),

    ("signature", "drop the microgreens schema half of PROSE_FIELDS",
     '                "management_beginner", "management_seasoned",',
     '                '),

    ("signature", "collapse ABSENT and explicit-null onto the same token",
     '_ABSENT = "\\x00absent"   # distinct from an explicit null, which is distinct from ""',
     '_ABSENT = "\\x00null"   # distinct from an explicit null, which is distinct from ""'),

    ("order", "sort the signature, making problem ORDER invisible",
     "        sig.append(tuple(row))\n    return tuple(sig)",
     "        sig.append(tuple(row))\n    return tuple(sorted(sig))"),

    ("names", "drop the explicit name fields, falling back to problem_name()'s chain",
     '        for k in ("name", "name_beginner", "name_seasoned"):',
     '        for k in ():'),

    ("grouping", "never report a twin group (the vacuous-pass shape)",
     "    twins = sorted((v for v in groups.values() if len(v) > 1), key=len, reverse=True)",
     "    twins = []"),

    ("grouping", "report EVERY crop as a twin regardless of signature",
     "        groups[prose_signature(c)].append(c[\"slug\"])",
     "        groups[\"same\"].append(c[\"slug\"])"),
]

SENTINEL = ("SENTINEL", "break family_cut outright; MUST redden or the harness is dead",
            "def family_cut(todo):",
            "def family_cut(todo):\n    raise AssertionError('sentinel')")


def preflight():
    src = open(SRC).read()
    bad = []
    for fam, label, anchor, _rep in MUTATIONS + [SENTINEL]:
        n = src.count(anchor)
        if n != 1:
            bad.append(f"  [{fam}] {label}: anchor matches {n} times, expected exactly 1")
    if bad:
        print("PREFLIGHT FAILED -- anchors do not match exactly once:")
        print("\n".join(bad))
        raise SystemExit(2)
    print(f"preflight: {len(MUTATIONS) + 1}/{len(MUTATIONS) + 1} anchors match exactly once")


def run_suite(cwd):
    r = subprocess.run([sys.executable, "-m", "pytest", os.path.join(cwd, "test_ladder_batch.py"),
                        "-q", "--no-header", "-p", "no:cacheprovider"],
                       capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr


def apply_in(tmp, anchor, rep):
    p = os.path.join(tmp, "ladder_batch.py")
    src = open(p).read()
    assert src.count(anchor) == 1, "anchor drifted inside the sandbox"
    open(p, "w").write(src.replace(anchor, rep) + f"\n{MARKER}\n")
    assert MARKER in open(p).read(), "mutation marker absent: the mutant was not written"


def sandbox():
    """Mirror the repo LAYOUT, not just the files.

    `ladder_batch.REPO` is derived from the module's own path (`dirname(dirname(__file__))`), so a
    flat sandbox silently repoints CANON at a nonexistent file and every test errors out. That is
    not a caught mutation, it is a dead harness -- and it is what the positive control exists to
    catch. Keep the module at <sandbox>/tools/ and symlink the real canonical alongside it.
    """
    tmp = tempfile.mkdtemp(prefix="mut_ladder_batch_")
    tools = os.path.join(tmp, "tools")
    os.makedirs(tools)
    for f in ("ladder_batch.py", "test_ladder_batch.py", "control_ladder_gate.py"):
        s = os.path.join(HERE, f)
        if os.path.exists(s):
            shutil.copy(s, tools)
    os.symlink(os.path.join(os.path.dirname(HERE), "crops_data_final.json"),
               os.path.join(tmp, "crops_data_final.json"))
    return tools


def main():
    preflight()

    # POSITIVE CONTROL: the clean tree must be green, or every 'catch' below is meaningless
    tmp = sandbox()
    rc, out = run_suite(tmp)
    shutil.rmtree(tmp)
    if rc != 0:
        print("POSITIVE CONTROL FAILED -- the clean suite is not green:\n" + out[-2000:])
        raise SystemExit(2)
    print("positive control: clean suite GREEN")

    # SENTINEL
    tmp = sandbox()
    apply_in(tmp, SENTINEL[2], SENTINEL[3])
    rc, out = run_suite(tmp)
    shutil.rmtree(tmp)
    if rc == 0:
        print("HARNESS DEAD -- the sentinel mutation SURVIVED; the suite is not running the "
              "mutated module. Every result below would be a false 'caught'.")
        raise SystemExit(3)
    print("sentinel: RED (harness is live)\n")

    caught = survived = 0
    for fam, label, anchor, rep in MUTATIONS:
        tmp = sandbox()
        apply_in(tmp, anchor, rep)
        rc, out = run_suite(tmp)
        shutil.rmtree(tmp)
        if rc != 0:
            caught += 1
            first = next((l for l in out.splitlines() if l.startswith("FAILED")), "")
            print(f"  CAUGHT   [{fam}] {label}\n           {first[:110]}")
        else:
            survived += 1
            print(f"  SURVIVED [{fam}] {label}   <-- GUARD GAP")

    print(f"\n{caught} caught, {survived} survived, of {len(MUTATIONS)}")
    raise SystemExit(1 if survived else 0)


if __name__ == "__main__":
    main()
