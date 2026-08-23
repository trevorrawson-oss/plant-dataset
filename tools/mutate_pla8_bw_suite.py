#!/usr/bin/env python3
"""Mutation harness for the bottom_watering applies_to correction (PLA-215).

WHY. The suite is replay-pinned and green from birth. The families that most need proving here are
SCOPE ones: this promote's real risk is not breakage (a widening cannot redden anything) but
over-widening -- adding a target the biology does not support, or quietly reinstating one of the
five graded REFUSALS. Those refusals are a judgment, and a judgment with no guard is a preference.

LIVENESS DEFENSE: positive control, sentinel, and a MUTATION-APPLIED marker asserted in the staged
file. Anchors are checked for uniqueness before mutating -- an anchor matching twice edits a site
you did not intend and reports a catch for the wrong reason, which is worse than a miss.

Usage: python3 tools/mutate_pla8_bw_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_bottom_watering_targets.py")
PROMOTE = os.path.join(HERE, "promote_pla8_bottom_watering_targets.py")
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    # ---- scope: over-widening, the actual risk of this promote --------------------------
    # NOT MUTATION-TESTED, DELIBERATELY, and this is the honest reason rather than an omission.
    # `test_the_five_refused_widenings_did_NOT_happen` asserts that even_watering, straw_mulch,
    # airflow_spacing and beneficial_predators did not gain the targets graded as tolerance-not-
    # control. There is NO mutation of THIS promote that can trip it in isolation: this promote only
    # touches `bottom_watering`, so any mutation that widens another method is caught FIRST by
    # `test_only_bottom_watering_changed`. A "caught" verdict there would be the earlier-check-masks-
    # guard vacuity wearing a green badge. The REFUSED test is a FORWARD assertion -- it guards a
    # future promote that might quietly finish the job -- and is kept for that, not counted as
    # coverage here. The first version of this harness pretended to test it with a mutation that
    # appended an unused import and changed nothing; it survived, correctly.
    ("a third target is added to bottom_watering", "scope",
     '        m["applies_to"].append(target)',
     '        m["applies_to"].append(target)\n    m["applies_to"].append("viral")'),
    ("a target is dropped instead of added", "scope",
     '        m["applies_to"].append(target)',
     '        m["applies_to"] = [target]'),
    # ---- sourcing -------------------------------------------------------------------------
    ("the new source loses its document title (A54)", "sourcing",
     '"title": "Bacterial Speck / Tomato / Agriculture: Pest Management Guidelines / UC Statewide "\n                 "IPM Program (UC IPM)",', ""),
    ("the new source drops to T2", "sourcing",
     '"accessed": "2026-08",\n        "tier": "T1",', '"accessed": "2026-08",\n        "tier": "T2",'),
    ("the mollusk anchor is re-minted instead of reused", "sourcing",
     '"mollusk": "ucanr_ext_snails_slugs"}', '"mollusk": "ucanr_ext_bacterial_speck"}'),
    ("a correction REPLACES the existing sources", "sourcing",
     '        if src not in m["sources"]:\n            m["sources"].append(src)',
     '        if True:\n            m["sources"] = [src]'),
    # ---- blast radius ----------------------------------------------------------------------
    ("a crop is touched as collateral", "blast",
     '    data["source_catalog"].update(json.loads(json.dumps(NEW_SOURCE)))',
     '    data["crops"][0]["name"] = "MUTATED"\n    data["source_catalog"].update(json.loads(json.dumps(NEW_SOURCE)))'),
    ("another control method is edited", "blast",
     '    m = data["control_methods"][METHOD]',
     '    data["control_methods"]["sulfur"]["applies_to"].append("mollusk")\n    m = data["control_methods"][METHOD]'),
    # ---- refusals ---------------------------------------------------------------------------
    ("the no-op refusal is disabled", "refusal",
     '        if target in cm[METHOD]["applies_to"]:', "        if False:"),
    ("the source-exists refusal is disabled", "refusal",
     "        if k in sc:\n            return f\"source_catalog.{k} already exists\"",
     "        if False:\n            return \"\""),
    # ---- mechanics ---------------------------------------------------------------------------
    ("output is no longer COMPACT", "mechanics",
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", "def apply_to(data):",
            "def apply_to(data):\n    return 0")


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0, (r.stdout + r.stderr)[-300:]


def stage(old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_pla8bw_")
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    s = open(PROMOTE).read()
    if old is not None:
        n = s.count(old)
        if n != 1:
            shutil.rmtree(wd)
            raise SystemExit(f"HARNESS DEAD: anchor matches {n}x (need exactly 1): {old[:70]!r}")
        s = s.replace(old, new + ("  " + MARKER if new else MARKER), 1)
    open(os.path.join(wd, os.path.basename(PROMOTE)), "w").write(s)
    if old is not None and MARKER not in open(os.path.join(wd, os.path.basename(PROMOTE))).read():
        shutil.rmtree(wd)
        raise SystemExit("HARNESS DEAD: MUTATION-APPLIED marker absent from the staged file")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- bottom_watering applies_to correction")
    print("=" * 78)
    wd = stage(); ok, out = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails.\n" + out); return 1
    print("positive control : GREEN\n")

    label, old, new = SENTINEL
    wd = stage(old, new); ok, _ = run(wd); shutil.rmtree(wd)
    if ok:
        print(f"HARNESS DEAD: {label} SURVIVED."); return 1
    print(f"sentinel         : RED as required ({label})\n")

    caught = survived = 0
    fam = {}
    for label, family, old, new in MUTATIONS:
        try:
            wd = stage(old, new)
        except SystemExit as e:
            print(f"  {e}"); return 1
        ok, _ = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1; print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1; print(f"  caught    [{family}] {label}")

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print(f"  {k:10s} {c} caught / {c + s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL -- a guard family is unreachable or its test is vacuous."); return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
