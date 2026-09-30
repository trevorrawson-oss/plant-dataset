#!/usr/bin/env python3
"""Mutation harness for test_promote_pla626_delete_first (PLA-215 convention). Cloned from the PLA-533 subtractive harness.

One defect per guard family is injected into a SCRATCH COPY of the promote source, and the WHOLE suite
is rerun against it; the suite must go RED. The real promote file is never modified.

LIVENESS DEFENCE:
  1. MUTATION-APPLIED MARKER. The old text must occur exactly once and the mutant must differ from the
     original, or the run exits HARNESS DEAD rather than recording a survivor.
  2. SENTINEL. A mutation that breaks the happy path outright runs first; if it survives, the harness is
     not running the suite against the mutant and the run exits HARNESS DEAD.
  3. POSITIVE CONTROL. The unmutated scratch copy must be fully GREEN before any mutation, and pytest
     rc 5 (nothing collected) is graded BROKEN, never green.

Usage:  python3 tools/mutate_pla626_delete_first_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = "promote_pla626_delete_first.py"
SUITE = "test_promote_pla626_delete_first.py"

MUTATIONS = [
    ("SENTINEL", "never write the edited text back",
     '        _set(crop, e["path"], cur.replace(e["before"], e["after"], 1))', '        pass'),
    ("pre/base-sha", "accept any base", "    if got != BASE_SHA:", "    if False:"),
    ("spec/change-set", "allow an edit outside apricot and plum", '        if e["crop"] not in CHANGED:', "        if False:"),
    ("spec/no-number", "allow an added number or citation token",
     '        if any(re.search(r"\\d", w) for w in added) or re.search(r"https?://|www\\.|_ext\\b|\\bsources?\\b", e["after"]):',
     "        if False:"),
    ("spec/retraction-pin", "allow a retraction on any field",
     '        if (r["crop"], r["path"], r["before"]) != RETRACTION or r["after"] is not None:', "        if False:"),
    ("pre/marianna-row", "stop pinning apricot rootstock_options[2]",
     '    if at(apricot, "/rootstock_options/2").get("name") != MARIANNA:', "    if False:"),
    ("pre/exact-once", "accept a target found 0 or 2+ times", "        if n != 1:", "        if False:"),
    ("pre/retraction-state", "stop pinning recommended_rootstock's pre-state",
     '        if at(crop, r["path"]) != r["before"]:', "        if False:"),
    ("apply/retraction", "leave recommended_rootstock in place", '        _set(crop, r["path"], None)', "        pass"),
    ("post/crop-set", "stop comparing the crop SET before values",
     "    if set(P) != set(Q) or P != Q:", "    if False:"),
    ("post/top-level", "stop checking top-level keys",
     '    if set(pre) != set(post) or any(pre[k] != post[k] for k in pre if k != "crops"):', "    if False:"),
    ("post/collateral", "stop checking crops outside the set", "            if a != b:", "            if False:"),
    ("post/reversal", "stop the undeclared-change reversal check", "        if _revert(a, b, spec) != a:", "        if False:"),
    ("post/st-julien", "stop the St. Julien purpose guard",
     '    if left:\n        refuse(f"St. Julien', '    if False:\n        refuse(f"St. Julien'),
    ("post/brownline", "stop the brownline purpose guard",
     '    if left:\n        refuse(f"prune brownline', '    if False:\n        refuse(f"prune brownline'),
    ("post/history-exempt", "stop exempting verification_status (purpose guard reads history as live)",
     '                if p == "" and k == "verification_status":', "                if False:"),
    ("serialize/compact", "reintroduce indent",
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")'),
]


def run_suite(workdir):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", os.path.join("tools", SUITE)],
                       cwd=workdir, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)[-400:]


def main():
    src = open(os.path.join(HERE, TARGET), encoding="utf-8").read()
    tmp = tempfile.mkdtemp(prefix="mut_pla626_")
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
