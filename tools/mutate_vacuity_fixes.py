#!/usr/bin/env python3
"""mutate_vacuity_fixes -- mutation harness for the kickoff-60 B5 vacuity fixes (2026-10-03/04).

Each of these tests used to RETURN EARLY and PASS having inspected nothing (PLA-544 side finding). Each mutation
here is a defect that early-returning version could never have seen; the fixed test must now redden on it, which
is the proof that it reaches its entry point:
  test_source_catalog_title_gate  (two tests, replayed from 060b91b8): the A54 flood count; the DORMANT marker
  test_build_rgv_promote          (replayed from 7e29f4f4): one patch changed -> not the committed batch
  test_rgv_harness::a31           (injection on broccoli): the A31 region-roster floor switched off
  test_bare_host_scan             (SOLE pinned by identity): the SOLE predicate inverted
(test_build_corn_family_patch's honest pytest.skip carries no assertion to mutate; run_test_tree's VERDICT counts it.)
Liveness: anchor preflight, MUTATION-APPLIED marker, sentinel, positive control (runner copied unchanged).
Usage: mutate_vacuity_fixes.py [name-substring]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = "# MUTATION-APPLIED"
NOTHING_COLLECTED = 5
SCRIPTS = set()
SC, RB, RH, BH = ("test_source_catalog_title_gate.py", "test_build_rgv_promote.py", "test_rgv_harness.py",
                  "test_bare_host_scan.py")

MUTATIONS = [
    ("sc_untitled_doc_ids_unflagged", "source_catalog_title_gate.py", "            elif cid not in LEGACY_UNFILLED:",
     "            elif False:", SC, "pre_state_floods_at_exactly_101"),
    ("sc_dormancy_unmarked", "whole_crop_gate.py",
     '    print("  DORMANT: catalog carries no titles (PLA-199 backfill not yet promoted)")',
     '    print("  catalog carries no titles (PLA-199 backfill not yet promoted)")', SC, "a54_dormant"),
    ("rgv_batch_patch_changed", "build_rgv_promote.py", '            patches.append({"op": "add",',
     '            patches.append({"op": "add", "mutated": True,', RB, "batch_shape"),
    ("rgv_region_roster_floor_off", "whole_crop_gate.py", "for m in _rrv:\n    fail(f\"region-roster: {m}\")",
     "for m in []:\n    fail(f\"region-roster: {m}\")", RH, "missing_rgv_fails_a31"),
    ("bare_host_sole_inverted", "bare_host_scan.py", "rows.append((sid, slug, path or '<crop>', not has_real, url))",
     "rows.append((sid, slug, path or '<crop>', has_real, url))", BH, "sole_split_is_pinned_by_identity"),
]
SENTINEL = (BH, "assert (len(sole_known), doc['sole_count']) == (161, 161)",
            "assert (len(sole_known), doc['sole_count']) == (162, 161)", "sole_split_is_pinned_by_identity")

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
    tmp = tempfile.mkdtemp(prefix="mut_b5_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    try:
        for f in os.listdir(HERE):
            src = os.path.join(HERE, f)
            if f.endswith((".py", ".json")) and os.path.isfile(src):
                shutil.copy2(src, os.path.join(tools, f))
        for d in (".evidence_cache", ".doc_cache", "staging", "batches"):
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
