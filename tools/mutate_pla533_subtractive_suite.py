#!/usr/bin/env python3
"""Mutation harness for test_promote_pla533_subtractive (PLA-215 convention). Cloned from the PLA-533 blockers harness.

One defect per guard family is injected into a SCRATCH COPY of the promote source, and the WHOLE suite
is rerun against it; the suite must go RED. The real promote file is never modified.

LIVENESS DEFENCE:
  1. MUTATION-APPLIED MARKER. The old text must occur exactly once and the mutant must differ from the
     original, or the run exits HARNESS DEAD rather than recording a survivor.
  2. SENTINEL. A mutation that breaks the happy path outright runs first; if it survives, the harness is
     not running the suite against the mutant and the run exits HARNESS DEAD.
  3. POSITIVE CONTROL. The unmutated scratch copy must be fully GREEN before any mutation, and pytest
     rc 5 (nothing collected) is graded BROKEN, never green.

Usage:  python3 tools/mutate_pla533_subtractive_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = "promote_pla533_subtractive.py"
SUITE = "test_promote_pla533_subtractive.py"

MUTATIONS = [
    ("SENTINEL", "never write the edited text back",
     '        _set(crop, e["path"], new.strip())', '        pass'),
    ("pre/base-sha", "accept any base", "    if got != BASE_SHA:", "    if False:"),
    ("pre/exact-once", "accept a target found 0 or 2+ times", "        if n != 1:", "        if False:"),
    ("spec/change-set", "allow an edit outside the five crops", '        if e["crop"] not in CHANGED:', "        if False:"),
    ("spec/no-number", "allow an added number or citation token",
     '        if any(re.search(r"\\d", w) for w in added) or re.search(r"https?://|_ext\\b|uf_ifas|\\bsources?\\b", e["after"]):',
     "        if False:"),
    ("pre/fd-state", "stop pinning Flying Dragon's pre-state",
     '        if row.get("name") != FD_NAME or row.get("container_size_gallons") != r["before"] or row.get("container_suitable") is not True:',
     "        if False:"),
    ("apply/fd-null", "leave the 25 gal in place", '        row["container_size_gallons"] = None', "        pass"),
    ("pre/lime-row", "stop pinning lime's sour orange row",
     '    if not rows or rows[0].get("name") != LIME_ROW or sum(1 for x in rows if x.get("name") == LIME_ROW) != 1:',
     "    if False:"),
    ("pre/lime-rec", "stop pinning lime's recommended_rootstock pre-state",
     '    if lime.get("recommended_rootstock") != LIME_REC:', "    if False:"),
    ("apply/lime-row", "keep the sour orange row", "    rows.pop(0)", "    pass"),
    ("apply/lime-rec", "leave recommended_rootstock in place", '    lime["recommended_rootstock"] = None', "    pass"),
    ("post/crop-set", "stop comparing the crop SET before values",
     "    if set(P) != set(Q) or P != Q:", "    if False:"),
    ("post/top-level", "stop checking top-level keys",
     '    if set(pre) != set(post) or any(pre[k] != post[k] for k in pre if k != "crops"):', "    if False:"),
    ("post/collateral", "stop checking crops outside the set", "            if a != b:", "            if False:"),
    ("post/reversal", "stop the undeclared-change reversal check", "        if _revert(a, b, spec) != a:", "        if False:"),
]


def run_suite(workdir):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", os.path.join("tools", SUITE)],
                       cwd=workdir, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)[-400:]


def main():
    src = open(os.path.join(HERE, TARGET), encoding="utf-8").read()
    tmp = tempfile.mkdtemp(prefix="mut_pla533sub_")
    try:
        # A tools/ scratch copy has no .git, and promote_fixture rebuilds the pinned pre-state FROM git
        # (REPO = parent of tools/). Mirror the repo layout: tmp/tools/ holds the copies, and .git,
        # canonical, docs, the staged spec and the evidence cache are linked in (PLA-581 precedent).
        tools = os.path.join(tmp, "tools"); os.mkdir(tools)
        for name in (SUITE, "promote_fixture.py"):
            shutil.copy(os.path.join(HERE, name), tools)
        for name in (".git", "crops_data_final.json", "docs"):
            os.symlink(os.path.join(os.path.dirname(HERE), name), os.path.join(tmp, name))
        for name in ("staging", ".evidence_cache"):
            os.symlink(os.path.join(HERE, name), os.path.join(tools, name))
        tgt = os.path.join(tools, TARGET)

        open(tgt, "w", encoding="utf-8").write(src)
        rc, out = run_suite(tmp)
        if rc == 5:
            print("HARNESS DEAD: positive control collected nothing (rc 5)"); sys.exit(2)
        if rc != 0:
            print("HARNESS DEAD: positive control is not green\n" + out); sys.exit(2)
        print("positive control: GREEN")

        caught, survived = [], []
        for fam, desc, old, new in MUTATIONS:
            n = src.count(old)
            if n != 1:
                print(f"HARNESS DEAD: [{fam}] target found {n} times (need exactly 1)"); sys.exit(2)
            mutant = src.replace(old, new, 1)
            if mutant == src:
                print(f"HARNESS DEAD: [{fam}] mutant identical to source"); sys.exit(2)
            open(tgt, "w", encoding="utf-8").write(mutant)
            print(f"MUTATION-APPLIED [{fam}] {desc}")
            rc, out = run_suite(tmp)
            if rc == 5:
                print(f"HARNESS DEAD: [{fam}] suite collected nothing"); sys.exit(2)
            (caught if rc != 0 else survived).append(fam)
            print(f"   -> {'CAUGHT' if rc != 0 else 'SURVIVED'}")
            if fam == "SENTINEL" and rc == 0:
                print("HARNESS DEAD: sentinel survived"); sys.exit(2)
        open(tgt, "w", encoding="utf-8").write(src)
        rc, out = run_suite(tmp)
        if rc != 0:
            print("HARNESS DEAD: restored copy is not green"); sys.exit(2)
        print(f"\n{len(MUTATIONS)} injected, {len(caught)} caught, {len(survived)} survived: {survived}")
        sys.exit(1 if survived else 0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
