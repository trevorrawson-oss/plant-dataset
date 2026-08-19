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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_roster_claim_gate as roster

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "whole_crop_gate.py")

# Live docs whose roster claims must track the canonical (see doc_roster_claim_gate).
ROSTER_DOCS = sorted(set(roster.DOCS_WITH_COUNT_SENTENCE) | set(roster.DOCS_WITH_SHELL_ENUMERATION))
ROSTER_TRIGGERS = set(ROSTER_DOCS) | {"crops_data_final.json", "LATEST.txt"}


def _index_bytes(path):
    """The bytes of `path` as they will be COMMITTED (the index), or None if absent.
    Not the working tree: an unstaged fix must not buy a green commit."""
    r = subprocess.run(["git", "show", f":./{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def roster_claim_concerns(staged_names):
    """Block a commit that would leave a LIVE doc's roster claim contradicting the canonical.

    Runs ONLY when the commit touches the canonical, LATEST.txt, or a gated doc -- a commit that
    touches none of them cannot make a claim go stale, and a net that fires on unrelated commits
    gets bypassed by habit. Complements the regression arm below, which SKIPS doc-only commits."""
    if not ROSTER_TRIGGERS & set(staged_names):
        return []
    canon = _index_bytes("crops_data_final.json")
    if canon is None:
        return []
    facts = roster.roster_facts(json.loads(canon.decode("utf-8")))
    concerns = []
    for rel in ROSTER_DOCS:
        blob = _index_bytes(rel)
        if blob is None:
            continue          # doc absent from the index: not this net's business
        concerns += roster.doc_claim_violations(blob.decode("utf-8"), rel, facts)
    latest = _index_bytes("LATEST.txt")
    if latest is not None:
        concerns += roster.latest_sha_violations(latest.decode("utf-8"), canon)
    return concerns


def export_currency_concerns(staged_names, app_root=None):
    """Block a canonical commit whose downstream EXPORT was built from a different canonical.

    PLA-258: for three weeks the app shipped a byte-exact projection of a canonical that was
    three promotes old, and the only reason it went unnoticed is that a faithful projection
    of stale bytes is indistinguishable from a faithful projection of current ones. The fix
    is to make the two states unable to coexist across a commit boundary, which is what this
    arm does.

    Measured against the STAGED canonical, not the working tree: the export must have been
    built from the bytes about to be committed. `npm run build:guides` reads the working
    tree, so the intended order is promote -> build:guides -> commit, and a commit that
    reorders those is exactly what this catches.

    ONLY the app arm (E1/E2). The astro submodule pin is deliberately excluded: it can only
    ever point at an ALREADY-COMMITTED dataset commit, so at pre-commit time a current pin
    is not merely absent, it is impossible. The site's currency is the release gate's
    question (`tools/export_staleness_gate.py`), not this hook's.

    SKIPS when plant-app is not on this disk. That is a deliberate departure from the gate's
    "unmeasured is not green" rule, and it is safe only because this is the fail-open
    backstop: a dataset-only checkout must stay committable. The release gate still refuses
    to call an unmeasured surface clean."""
    if "crops_data_final.json" not in set(staged_names):
        return []
    sys.path.insert(0, HERE)
    import export_staleness_gate as esg
    root = app_root or esg.DEFAULT_APP_ROOT
    if not os.path.isdir(root):
        print(f"  export-currency: no plant-app at {root} -> skip (backstop fails open)")
        return []
    staged = _index_bytes("crops_data_final.json")
    if staged is None:
        return []
    violations, _ = esg.app_violations(root, esg.sha256_bytes(staged))
    return violations


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


def drop_precert_anchoring(new, cand_crop):
    """Pre-cert anchoring allowance. A crop that is NOT yet certified
    (verification_status.status != 'verified_gs_arc') legitimately carries authored
    `sources[]` without per-field `anchoring_urls` -- those fill progressively at
    Step 4+, and anchoring COMPLETENESS is a Step-11 cert requirement (whole_crop_gate
    section F), not a between-commit invariant. So a NEW `anchoring: ... unanchored`
    violation on a pre-cert crop is the accepted admission state (e.g. every tree /
    perennial / annual-hub Steps 1-3, which author sourced rootstock/varieties/
    companions before the anchoring pass), not a regression. A CERTIFIED crop gaining
    an anchoring gap IS a regression (it must keep its anchoring) -- left in to block."""
    status = (cand_crop.get("verification_status") or {}).get("status")
    if status == "verified_gs_arc":
        return new
    return {v for v in new if "VIOLATION: anchoring:" not in v}


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
            new = drop_precert_anchoring(new, cc[slug])
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
            # The roster-claim arm runs FIRST and independently: a doc-only commit skips the
            # regression arm below, and that is exactly where a stale roster claim ships.
            stale = roster_claim_concerns(staged)
            if stale:
                print("pre-commit roster-claim: BLOCKED -- a live doc contradicts the canonical:")
                for c in stale:
                    print("  VIOLATION: " + c)
                print("Fix the doc (or bypass with: git commit --no-verify)")
                return 1
            if "crops_data_final.json" not in staged:
                print("pre-commit release-verify: crops_data_final.json not staged -> skip")
                return 0
            cand_path = _blob(":./crops_data_final.json")    # staged (index)
            base_path = _blob("HEAD:./crops_data_final.json")  # last commit
            tmp = [cand_path, base_path]
        print("pre-commit release-verify (safety net -- NOT a substitute for protocol #6):")
        concerns = check(base_path, cand_path)
        if not (a.base and a.candidate):
            stale_export = export_currency_concerns(staged)
            if stale_export:
                print("\nBLOCKED -- the shipped export does not match the canonical being committed:")
                for c in stale_export:
                    print("  VIOLATION: " + c)
                print("Fix: run `npm run build:guides` in ~/plant-app, then commit again.")
                print("(Or bypass with: git commit --no-verify)")
                return 1
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
