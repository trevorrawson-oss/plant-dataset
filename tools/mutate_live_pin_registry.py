#!/usr/bin/env python3
"""mutate_live_pin_registry -- mutation harness for the live-pin registry and its detector (kickoff 60 B6,
2026-10-04). One defect per guard family, injected into a SCRATCH COPY of tools/, each driving
test_live_pin_registry.py: every detector arm (canonical SHA, integer equality, integer floor, population string,
the live-read gate), the A44 omission (the ruled positive control), an exemption with no reason, and a ruled file
moved to EXEMPT. Liveness: anchor preflight, MUTATION-APPLIED marker, sentinel, positive control (the runner is
mutate_pla10_promote2.py's, copied unchanged).
Usage: mutate_live_pin_registry.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5
SCRIPTS = set()
REG = "live_pin_registry.py"
T = "test_live_pin_registry.py"

MUTATIONS = [
    ("a44_omitted", REG, "    'test_gate_planting_layout_a44.py': [", "    'test_gate_planting_layout_a44_GONE.py': [",
     T, "every_detected_file_is_registered"),
    ("sha_arm_blind", REG, '    sha = sorted({x[:8] for x in re.findall(r"\\b[0-9a-f]{8,64}\\b", src) if x[:8] in prefixes})',
     "    sha = []", T, "detector_sees_each_pin_shape"),
    ("equality_arm_blind", REG, "            if any(isinstance(o, ast.Eq) for o in x.ops):", "            if False:",
     T, "detector_sees_each_pin_shape"),
    ("floor_arm_blind", REG, "            if any(isinstance(o, (ast.GtE, ast.Gt, ast.LtE, ast.Lt)) for o in x.ops):",
     "            if False:", T, "detector_sees_each_pin_shape"),
    ("population_string_arm_blind", REG,
     "                if isinstance(c, ast.Constant) and isinstance(c.value, str) and POPSTR.search(c.value):",
     "                if False:", T, "detector_sees_each_pin_shape"),
    ("live_read_gate_blind", REG, "        if not LIVE.search(src):", "        if True:", T, "the_registry_population"),
    ("exemption_without_reason", REG,
     "    'test_live_pin_registry.py': 'DOC_ONLY: the registry\\'s own test;",
     "    'test_live_pin_registry.py': '' and 'DOC_ONLY: the registry\\'s own test;",
     T, "every_exemption_says_why"),
    ("ruled_entry_exempted", T, '    "test_annual_calendar.py", "test_perennial_year_gate.py",',
     '    "test_annual_calendar_GONE.py", "test_perennial_year_gate.py",', T, "ruled_files_are_live_pins"),
]
SENTINEL = (T, "(61, 25, 60, 43)", "(61, 25, 60, 44)", "the_registry_population")

def run_driver(tools, f, sel):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if f in SCRIPTS:
        cmd = [sys.executable, "-B", os.path.join(tools, f)]
    else:
        cmd = [sys.executable, "-B", "-m", "pytest", os.path.join(tools, f), "-q", "-x", "--no-header",
               "-p", "no:cacheprovider"] + (["-k", sel] if sel else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode, r.stdout + r.stderr


def apply(tools, target, old, new):
    p = os.path.join(tools, target)
    clean = open(p, encoding="utf-8").read()
    if clean.count(old) != 1:
        return None, f"anchor matches {clean.count(old)} times"
    open(p, "w", encoding="utf-8").write(clean.replace(old, new + "  " + MARKER if "\n" not in new
                                                       else new.replace("\n", "  " + MARKER + "\n", 1), 1))
    if MARKER not in open(p, encoding="utf-8").read():
        return None, "mutation not on disk"
    return clean, None


def main(argv):
    only = argv[1] if len(argv) > 1 else None
    muts = [m for m in MUTATIONS if not only or only in m[0]]
    tmp = tempfile.mkdtemp(prefix="mut_lpr_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    try:
        for f in os.listdir(HERE):
            src = os.path.join(HERE, f)
            if f.endswith((".py", ".json")) and os.path.isfile(src):
                shutil.copy2(src, os.path.join(tools, f))
        for d in (".evidence_cache", ".doc_cache", "staging"):
            if os.path.isdir(os.path.join(HERE, d)):
                os.symlink(os.path.join(HERE, d), os.path.join(tools, d))
        for name in ("crops_data_final.json", ".git", "CLAUDE.md"):
            os.symlink(os.path.join(REPO, name), os.path.join(tmp, name))
        bad = [n for n, t, old, *_ in muts if open(os.path.join(tools, t), encoding="utf-8").read().count(old) != 1]
        if bad:
            sys.exit(f"HARNESS DEAD: anchor preflight failed for {bad}")
        print(f"anchor preflight: {len(muts)}/{len(muts)} anchors match exactly once")
        for f in sorted({m[4] for m in muts}):
            rc, out = run_driver(tools, f, None)
            if rc != 0:
                print(out[-2000:])
                sys.exit(f"HARNESS DEAD: the unmutated driver {f} is already failing (rc {rc})")
        print(f"positive control: every driver file WHOLE and unmutated is GREEN "
              f"({len({m[4] for m in muts})} files)")
        f, old, new, sel = SENTINEL
        clean, err = apply(tools, f, old, new)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel {err}")
        rc, _ = run_driver(tools, f, sel)
        open(os.path.join(tools, f), "w", encoding="utf-8").write(clean)
        if rc in (0, NOTHING_COLLECTED):
            sys.exit(f"HARNESS DEAD: the sentinel did not redden (rc {rc})")
        print("sentinel: reddened as required\n")
        caught, survived, broken = [], [], []
        for name, target, old, new, drv, sel in muts:
            clean, err = apply(tools, target, old, new)
            if err:
                broken.append(name); print(f"  BROKEN   {name}: {err}"); continue
            rc, _ = run_driver(tools, drv, sel)
            open(os.path.join(tools, target), "w", encoding="utf-8").write(clean)
            if rc == NOTHING_COLLECTED:
                broken.append(name); print(f"  BROKEN   {name}: driver collected nothing")
            elif rc == 0:
                survived.append(name); print(f"  SURVIVED {name}  ({drv} {sel or '(script)'})")
            else:
                caught.append(name); print(f"  caught   {name}")
        print(f"\n{len(muts)} injected: {len(caught)} caught, {len(survived)} survived, {len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
