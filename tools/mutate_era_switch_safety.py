#!/usr/bin/env python3
"""mutate_era_switch_safety -- mutation harness for the era-switch WIRING (2026-10-06, PLA-673 B2 go-condition 2).

  whole_crop_gate.py / gate_all.py / precommit_release_verify.py  <- test_era_switch_safety.py

(The binding itself, sourced_block_ratchet_gate.bind_era / _default_known, is mutation-tested by
mutate_citation_ratchet_gates.py, family "era".) One mutation per guard; the named driver must redden. Liveness (PLA-215
bar): anchor preflight (each anchor exactly once, else HARNESS DEAD), MUTATION-APPLIED marker checked on disk, a
sentinel that must redden, the WHOLE unmutated suite green first. Grading: rc 1 = caught; rc 0 = SURVIVED; anything else
(rc 5 nothing collected, rc 2 collection error) = BROKEN.
Usage: mutate_era_switch_safety.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
SU = "test_era_switch_safety.py"

MUTATIONS = [  # (name, target file, anchor, replacement, driver)
    ("wcg_bind_removed", "whole_crop_gate.py", "    _sbr_era.bind_era(PATH)\n", "    pass\n",
     "whole_crop_gate_refuses"),
    ("wcg_refusal_exits_0", "whole_crop_gate.py", '    print(f"ERA SWITCH REFUSED: {_e}")\n    sys.exit(2)\n',
     '    print(f"ERA SWITCH REFUSED: {_e}")\n    sys.exit(0)\n', "whole_crop_gate_refuses"),
    ("gate_all_bind_removed", "gate_all.py", "        _sbr_era.bind_era(path)\n", "        pass\n",
     "gate_all_refuses"),
    ("hook_env_strip_removed", "precommit_release_verify.py",
     "    env = {k: v for k, v in os.environ.items() if k != ERA_ENV}\n", "    env = dict(os.environ)\n",
     "hook_strips"),
    ("hook_verdict_check_removed", "precommit_release_verify.py",
     '    if not any(l.startswith("GATE:") for l in out.splitlines()):\n', "    if False:\n",
     "hook_refuses_a_gate_run_with_no_verdict"),
]
SENTINEL = (SU, '    rc, out = _run("gate_all.py", CANON, env_value=value)\n    assert rc == 2',
            '    rc, out = _run("gate_all.py", CANON, env_value=value)\n    assert rc == 7', "gate_all_refuses")


def run_driver(tools, sel):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    env.pop("SBR_KNOWN_AT_ARMING", None)
    cmd = [sys.executable, "-B", "-m", "pytest", os.path.join(tools, SU), "-q", "-x", "--no-header",
           "-p", "no:cacheprovider"] + (["-k", sel] if sel else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode, r.stdout + r.stderr


def apply(tools, target, old, new):
    p = os.path.join(tools, target)
    clean = open(p, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times"
    with open(p, "w", encoding="utf-8") as f:
        f.write(clean.replace(old, new, 1) + "\n" + MARKER + "\n")
    if MARKER not in open(p, encoding="utf-8").read():
        return None, "mutation not on disk"
    return clean, None


def main(argv):
    only = argv[1] if len(argv) > 1 else None
    muts = [m for m in MUTATIONS if not only or only in m[0]]
    tmp = tempfile.mkdtemp(prefix="mut_era_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    try:
        for f in os.listdir(HERE):
            src = os.path.join(HERE, f)
            if f.endswith((".py", ".json")) and os.path.isfile(src):
                shutil.copy2(src, os.path.join(tools, f))
        for d in (".evidence_cache", ".doc_cache", "staging", "batches"):
            if os.path.isdir(os.path.join(HERE, d)):
                os.symlink(os.path.join(HERE, d), os.path.join(tools, d))
        for name in ("crops_data_final.json", ".git", "CLAUDE.md", "LATEST.txt"):
            if os.path.exists(os.path.join(REPO, name)):
                os.symlink(os.path.join(REPO, name), os.path.join(tmp, name))
        bad = [m[0] for m in muts if open(os.path.join(tools, m[1]), encoding="utf-8").read().count(m[2]) != 1]
        if bad:
            sys.exit(f"HARNESS DEAD: anchor preflight failed for {bad}")
        print(f"anchor preflight: {len(muts)}/{len(muts)} anchors match exactly once")
        rc, out = run_driver(tools, None)
        if rc != 0:
            print(out[-2000:])
            sys.exit(f"HARNESS DEAD: the unmutated suite is already failing (rc {rc})")
        print("positive control: the WHOLE suite, unmutated, is GREEN")
        f, old, new, sel = SENTINEL
        clean, err = apply(tools, f, old, new)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel {err}")
        rc, _ = run_driver(tools, sel)
        open(os.path.join(tools, f), "w", encoding="utf-8").write(clean)
        if rc != 1:
            sys.exit(f"HARNESS DEAD: the sentinel did not redden as a test failure (rc {rc})")
        print("sentinel: reddened as required\n")
        caught, survived, broken = [], [], []
        for name, target, old, new, sel in muts:
            clean, err = apply(tools, target, old, new)
            if err:
                broken.append(name); print(f"  BROKEN   {name}: {err}"); continue
            rc, out = run_driver(tools, sel)
            open(os.path.join(tools, target), "w", encoding="utf-8").write(clean)
            if rc == 1:
                caught.append(name); print(f"  caught   {name}")
            elif rc == 0:
                survived.append(name); print(f"  SURVIVED {name}  (-k {sel})")
            else:
                broken.append(name); print(f"  BROKEN   {name}: rc {rc} (-k {sel})\n{out[-600:]}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
