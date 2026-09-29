#!/usr/bin/env python3
"""Mutation harness for test_promote_pla533_blockers (PLA-215 convention).

One defect per guard family is injected into a SCRATCH COPY of the promote source, and the WHOLE suite
is rerun against it; the suite must go RED. The real promote file is never modified.

LIVENESS DEFENCE:
  1. MUTATION-APPLIED MARKER. The old text must occur exactly once and the mutant must differ from the
     original, or the run exits HARNESS DEAD rather than recording a survivor.
  2. SENTINEL. A mutation that breaks the happy path outright runs first; if it survives, the harness is
     not running the suite against the mutant and the run exits HARNESS DEAD.
  3. POSITIVE CONTROL. The unmutated scratch copy must be fully GREEN before any mutation, and pytest
     rc 5 (nothing collected) is graded BROKEN, never green.

Usage:  python3 tools/mutate_pla533_blockers_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = "promote_pla533_blockers.py"
SUITE = "test_promote_pla533_blockers.py"

MUTATIONS = [
    ("SENTINEL", "never append the findings",
     '        bycrop[x["crop"]]["verification_status"]["open_findings"].append(copy.deepcopy(x["finding"]))',
     '        pass'),
    ("pre/base-sha", "accept any base",
     "    if got != BASE_SHA:", "    if False:"),
    ("pre/flags", "stop checking the launch_ready pre-state",
     "        if any(vs.get(k) is not True for k in FLAGS):", "        if False:"),
    ("pre/live-blocker", "stop refusing a pre-existing live blocker",
     "        if live:", "        if False:"),
    ("pre/id-collision", "stop refusing an id already in the dataset",
     '        if x["finding"]["id"] in existing:', "        if False:"),
    ("pre/field-quote", "stop checking the quoted dataset strings",
     "            if not isinstance(val, str) or fragment not in val:", "            if False:"),
    ("evidence/quote", "stop checking quotes against the cached bytes",
     "            if re.sub(r\"\\s+\", \" \", quote) not in _page_text(sha):", "            if False:"),
    ("evidence/digest", "stop checking the cached file hashes to its name",
     "    if hashlib.sha256(raw).hexdigest() != sha:", "    if False:"),
    ("spec/count", "stop pinning the finding count",
     "    if len(fs) != EXPECTED_FINDINGS:", "    if False:"),
    ("spec/held", "let a HELD id land",
     '        if f.get("id") in HELD_IDS:', "        if False:"),
    ("spec/crop-set", "let a finding target another crop",
     '        if x["crop"] not in CROPS:', "        if False:"),
    ("spec/blocks", "let a non-blocking finding through",
     '        if f.get("blocks_launch") is not True or f.get("status") != "open":', "        if False:"),
    ("spec/close", "drop the close-condition requirement",
     '        if not all(m in f.get("summary", "") for m in CLOSE_MARKERS):', "        if False:"),
    ("apply/flags", "leave the launch flags true",
     "            bycrop[slug][\"verification_status\"][k] = False", "            pass"),
    ("post/crop-set", "stop comparing the crop SET before values",
     "    if set(P) != set(Q) or P != Q:", "    if False:"),
    ("post/top-level", "stop checking top-level keys",
     '        if k != "crops" and pre[k] != post[k]:', "        if False:"),
    ("post/collateral", "stop checking other crops",
     "            if a != b:", "            if False:"),
    ("post/in-crop", "stop checking keys inside a target crop",
     '            if k != "verification_status" and a[k] != b[k]:', "            if False:"),
    ("post/vs-keys", "stop checking undeclared verification_status keys (status)",
     "            if k not in DECLARED_VS_KEYS and va[k] != vb[k]:", "            if False:"),
    ("post/flags", "stop requiring both flags false",
     "        if any(vb[k] is not False for k in FLAGS):", "        if False:"),
]


def run_suite(workdir):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", os.path.join("tools", SUITE)],
                       cwd=workdir, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)[-400:]


def main():
    src = open(os.path.join(HERE, TARGET), encoding="utf-8").read()
    tmp = tempfile.mkdtemp(prefix="mut_pla533_")
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
