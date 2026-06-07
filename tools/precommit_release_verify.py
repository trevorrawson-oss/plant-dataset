#!/usr/bin/env python3
"""precommit_release_verify.py -- a pre-commit SAFETY NET for dataset commits.

Backstop for when releases scale to a pipeline. It does NOT replace the operator's
protocol #6 (gate + release_verify + claim cross-check); it catches the one thing a
tired/automated committer is most likely to ship: a REGRESSION.

Blocks a commit ONLY on:
  - a changed crop that gains a NEW gate violation vs HEAD, or
  - a dropped source_catalog entry.
It deliberately does NOT require gate == 0 -- mid-arc releases legitimately carry
violations (M16 5.A-5.D all sat at 21). The invariant is "don't make it worse,"
which is correct for every commit type below.

Commit-type aware (per the 2026-06-06 design):
  - crops_data_final.json NOT staged       -> SKIP   (doc / tool-only commit)
  - source_catalog changed, NO crop changed -> catalog admit: only a catalog DROP blocks
  - exactly 1 crop changed                  -> cell release: NEW violations on it block
  - >1 crop changed                         -> normalization: NEW violations on ANY block
Every crop-touching case also blocks on a source_catalog DROP.

FAIL-OPEN: any internal error prints a loud warning and ALLOWS the commit. A broken
safety net must never halt all work. Bypass anytime with `git commit --no-verify`.

Modes:
  (default)                 git: staged `:crops_data_final.json` vs `HEAD:crops_data_final.json`
  --base A --candidate B    offline test on two files (no git)
"""
import json, subprocess, sys, os, argparse, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "whole_crop_gate.py")


def gate_violations(path, slug):
    out = subprocess.run([sys.executable, GATE, slug, path],
                         capture_output=True, text=True).stdout
    return set(l.strip() for l in out.splitlines() if "VIOLATION:" in l)


def crops_map(d):
    return {c["slug"]: c for c in d["crops"]}


def _stub_regions(crop):
    """Regions whose plantings is still a PENDING stub / not a real rule dict."""
    out = set()
    for rk, r in (crop.get("regions") or {}).items():
        pl = r.get("plantings")
        if not (isinstance(pl, list) and pl and isinstance(pl[0], dict)):
            out.add(rk)
    return out


def drop_shell_build_unmasks(new, base_crop, cand_crop):
    """Step-3.5 shell-build allowance: drop `region_notes pair both null: R`
    violations that are new ONLY because region R graduated from a PENDING stub
    (base) to a shaped shell (candidate). The stub MASKED the null region_notes
    pair; building the shell un-masks it, and null region_notes is the explicitly
    accepted Step-3.5 admission state (Steps 6/7 fill it) -- not a regression. A
    region_notes-null that appears on a cell which was NOT a stub in base (a real
    blanking, or a Step-11 unfilled cell) is left in -- still a regression."""
    graduated = _stub_regions(base_crop) - _stub_regions(cand_crop)
    prefix = "VIOLATION: region_notes pair both null: "
    return {v for v in new
            if not (v.startswith(prefix) and v[len(prefix):] in graduated)}


def check(base_path, cand_path):
    base = json.load(open(base_path))
    cand = json.load(open(cand_path))
    bc, cc = crops_map(base), crops_map(cand)
    changed = sorted(s for s in cc if cc[s] != bc.get(s))
    concerns = []

    bcat = set(base.get("source_catalog", {}))
    ccat = set(cand.get("source_catalog", {}))
    dropped = sorted(bcat - ccat)
    added = sorted(ccat - bcat)
    if dropped:
        concerns.append(f"source_catalog entries DROPPED: {dropped}")

    if not changed:
        print(f"  catalog admit / no crop change (catalog +{added or 'none'})")
    else:
        kind = "cell release" if len(changed) == 1 else f"multi-crop normalization ({len(changed)} crops)"
        print(f"  {kind}: crops changed = {changed}")
        for slug in changed:
            vb = gate_violations(base_path, slug)
            vc = gate_violations(cand_path, slug)
            new = drop_shell_build_unmasks(vc - vb, bc.get(slug, {}), cc[slug])
            new = sorted(new)
            if new:
                concerns.append(f"{slug}: {len(new)} NEW gate violation(s): {new[:5]}")
            else:
                cleared = len(vb) - len(vc)
                tail = f", cleared {cleared}" if cleared > 0 else ""
                print(f"  ok {slug}: no new violations ({len(vc)} total{tail})")
    return concerns


def _blob(ref):
    r = subprocess.run(["git", "show", ref], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git show {ref}: {r.stderr.strip()}")
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    f.write(r.stdout); f.close()
    return f.name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base")
    ap.add_argument("--candidate")
    a = ap.parse_args()
    tmp = []
    try:
        if a.base and a.candidate:
            base_path, cand_path = a.base, a.candidate
        else:
            staged = subprocess.run(["git", "diff", "--cached", "--name-only"],
                                    capture_output=True, text=True).stdout.split()
            if "crops_data_final.json" not in staged:
                print("pre-commit release-verify: crops_data_final.json not staged -> skip")
                return 0
            cand_path = _blob(":./crops_data_final.json")    # staged (index)
            base_path = _blob("HEAD:./crops_data_final.json")  # last commit
            tmp = [cand_path, base_path]
        print("pre-commit release-verify (safety net -- NOT a substitute for protocol #6):")
        concerns = check(base_path, cand_path)
        if concerns:
            print("\nBLOCKED -- regression(s) detected:")
            for c in concerns:
                print("  CONCERN: " + c)
            print("Fix, run protocol #6, or bypass with: git commit --no-verify")
            return 1
        print("  OK -- no regression. (Backstop only; still run protocol #6 for a real release.)")
        return 0
    except SystemExit:
        raise
    except Exception as e:
        print(f"pre-commit release-verify ERRORED -> failing OPEN (commit ALLOWED): {e}",
              file=sys.stderr)
        return 0
    finally:
        for f in tmp:
            try:
                os.unlink(f)
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main())
