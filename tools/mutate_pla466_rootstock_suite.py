#!/usr/bin/env python3
"""Mutation harness for test_promote_pla466_rootstock.

A guard suite that has never been shown to FAIL is not coverage, it is decoration. This harness
injects one defect per guard family into the PROMOTE SOURCE, reruns the suite, and requires the
suite to go RED. A mutation that survives is reported loudly.

LIVENESS DEFENCE (PLA-138 dedented an already-indented template, silently ran the CLEAN fixture,
and reported every mutation as surviving):

  1. MUTATION-APPLIED MARKER. Every mutation must change the file. If the old text is not found,
     or the file is byte-identical after substitution, the run exits HARNESS DEAD rather than
     recording a survivor.
  2. SENTINEL. A mutation that MUST redden (it breaks the happy path outright) runs first. If the
     sentinel survives, the harness is not actually running the suite against the mutant, so every
     other result is meaningless and the run exits HARNESS DEAD.
  3. POSITIVE CONTROL. The unmutated suite must be fully GREEN before any mutation runs, and again
     after the file is restored. A suite that is already red cannot prove anything.

The whole suite is the control: every mutation runs `pytest tools/test_promote_pla466_rootstock.py`
in full rather than a hand-picked selector, so a mutation that reddens some unrelated test still
counts as caught, and a mutation nothing catches is unambiguous.

Usage:  python3 tools/mutate_pla466_rootstock_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TARGET = os.path.join(HERE, "promote_pla466_rootstock.py")
SUITE = os.path.join(HERE, "test_promote_pla466_rootstock.py")

# (family, name, old, new). One per guard family in the promote.
MUTATIONS = [
    # --- SENTINEL: must redden, or the harness is not running the mutant at all ---
    ("SENTINEL", "drop the St. Julien removal entirely",
     '    idx = next(i for i, e in enumerate(rows) if e["name"] == DROP_ROW)\n    rows[idx] = copy.deepcopy(CITATION_ROW)',
     '    pass'),

    # --- pre-state guards ---
    ("pre/roster", "stop checking the roster count",
     'if len(data["crops"]) != ROSTER:',
     'if False:'),
    ("pre/catalog", "stop checking citable_for pre-state",
     'if cat.get("citable_for") != UCD_CITABLE_FOR_OLD:',
     'if False:'),
    ("pre/plum-names", "stop checking the plum row names",
     "if names != PLUM_PRE_NAMES:",
     "if False:"),
    ("pre/marianna", "stop checking Marianna's container pre-state",
     'if mari["container_suitable"] is not True or mari["container_size_gallons"] != 25:',
     'if False:'),
    ("pre/varieties", "stop checking the varieties credit exists",
     'if "ucanr_ext" not in (v.get("sources") or []):',
     'if False:'),
    ("pre/launch", "stop checking launch_ready pre-state",
     'if vs.get("launch_ready_core") is not True or vs.get("launch_ready_seasoned") is not True:',
     'if False:'),
    ("pre/blocker", "stop refusing a pre-existing live blocker",
     "        if live:\n            raise SystemExit(f\"REFUSED: {slug} already carries a live blocking finding\")",
     "        if False:\n            raise SystemExit(f\"REFUSED: {slug} already carries a live blocking finding\")"),
    ("pre/chill-counts", "stop checking the pinned chill cell counts",
     "if (s_n, c_n) != (sole, co):",
     "if False:"),
    ("pre/container-null", "stop refusing a pre-existing container null",
     "    if nulls:\n        raise SystemExit(f\"REFUSED: container_suitable is already null on {nulls}\")",
     "    if False:\n        raise SystemExit(f\"REFUSED: container_suitable is already null on {nulls}\")"),

    # --- exact-once prose replacement ---
    ("prose/replace-once", "allow a target that is not unique",
     "    if n != 1:\n        raise SystemExit(f\"REFUSED: {where}: target found {n} times, expected exactly 1\")",
     "    if False:\n        raise SystemExit(f\"REFUSED: {where}: target found {n} times, expected exactly 1\")"),
    ("prose/last-sentence", "stop checking the traits target is the last sentence",
     'if not row_of(lem, SOUR_ORANGE)["traits_seasoned"].rstrip().endswith(SOUR_ORANGE_TRAITS_OLD):',
     'if False:'),

    # --- post-state guards ---
    ("post/crop-set", "stop comparing the crop SET before values",
     "    if set(P) != set(Q):",
     "    if False:"),
    ("post/changed-crops", "stop pinning which crops changed",
     "if changed != EXPECTED_CHANGED_CROPS:",
     "if False:"),
    ("post/other-catalog", "stop checking collateral catalog damage",
     "    if other != {k: v for k, v in pre[\"source_catalog\"].items() if k != \"ucd_fruitnut\"}:",
     "    if False:"),
    ("post/repoint-url", "stop checking the repointed url",
     'if au["ucd_fruitnut"]["url"] != NEW_PLUM_URL:',
     'if False:'),
    ("post/verified-date", "stop checking the verified date moved with the url",
     'if au["ucd_fruitnut"]["verified"] != VERIFIED:',
     'if False:'),
    ("post/citation-row", "stop byte-comparing the Citation row to its spec",
     "    if cit != CITATION_ROW:",
     "    if False:"),
    ("post/varieties-drop", "stop checking the varieties credit was dropped",
     'if "ucanr_ext" in plum["varieties"]["sources"]:',
     'if False:'),
    ("post/region-credit", "stop pinning the 48 surviving region credits",
     "    if still != 48:",
     "    if False:"),
    ("post/null-container", "stop pinning the null container row count",
     "if len(nulls) != EXPECTED_NULL_CONTAINER_ROWS:",
     "if False:"),
    ("post/null-size", "stop pinning the null size_class row count",
     "if len(sizenulls) != EXPECTED_NULL_SIZE_ROWS:",
     "if False:"),
    ("post/basis-held", "stop checking rootstock_selection_basis is held",
     'if Q[slug]["rootstock_selection_basis"] != P[slug]["rootstock_selection_basis"]:',
     'if False:'),
    ("post/container-path", "stop checking lemon/lime container_path held",
     'if cn["container_path"] != "direct" or cn["container_ok"] is not True:',
     'if False:'),
    ("post/lime-source", "stop checking lime gained uf_ifas_edis",
     'if "uf_ifas_edis" not in lso["sources"]:',
     'if False:'),
    ("post/findings-count", "stop pinning the new findings count",
     "if new_f != EXPECTED_NEW_FINDINGS:",
     "if False:"),
    ("post/lost-finding", "stop checking no existing finding id is lost",
     "        if not a <= b:",
     "        if False:"),
    ("post/blocker-launch", "stop coupling a live blocker to launch_ready false",
     'if vs.get("launch_ready_core") is not False or vs.get("launch_ready_seasoned") is not False:',
     'if False:'),
    ("post/status-frozen", "stop checking status never moves",
     'if vs.get("status") != P[c["slug"]]["verification_status"].get("status"):',
     'if False:'),
    # These two corrupt the VALUE, not the guard. Disabling the guard alone left the suite green,
    # because apply() still wrote a correct note and the suite's own assertion caught nothing new.
    # A guard is only meaningful against a bad value, so that is what gets injected.
    ("post/anchor-note-title", "write an anchor note with the expected page title MISSING",
     'title at this URL: \\"" + EXPECTED_PLUM_TITLE + "\\".',
     'title at this URL: unstated.'),
    ("post/anchor-note-fragility", "write an anchor note with the generic-path fragility MISSING",
     "site-wide GENERIC path",
     "site-wide path"),
    ("post/blocker-count", "stop pinning the blocker count",
     "if blockers != EXPECTED_BLOCKERS_AFTER:",
     "if False:"),
]


def run_suite():
    """Return (ok, tail). ok is True when the suite is fully green."""
    p = subprocess.run([sys.executable, "-m", "pytest", SUITE, "-q", "--no-header", "-x"],
                       cwd=REPO, capture_output=True, text=True)
    tail = (p.stdout or "").strip().splitlines()
    return p.returncode == 0, (tail[-1] if tail else "")


def main():
    with open(TARGET, "r", encoding="utf-8") as f:
        original = f.read()
    backup = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
    backup.write(original)
    backup.close()

    print("POSITIVE CONTROL: the unmutated suite must be GREEN")
    ok, tail = run_suite()
    if not ok:
        print(f"  HARNESS DEAD: the clean suite is already RED -- {tail}")
        sys.exit(2)
    print(f"  clean: {tail}\n")

    caught = survived = 0
    survivors = []
    try:
        for i, (family, name, old, new) in enumerate(MUTATIONS):
            if old not in original:
                print(f"  HARNESS DEAD: mutation {family!r} ({name}) -- old text NOT FOUND in the "
                      f"promote. The harness would have recorded a false survivor.")
                sys.exit(2)
            mutated = original.replace(old, new, 1)
            if mutated == original:
                print(f"  HARNESS DEAD: mutation {family!r} changed nothing (MUTATION-APPLIED marker).")
                sys.exit(2)
            with open(TARGET, "w", encoding="utf-8") as f:
                f.write(mutated)

            ok, tail = run_suite()
            if ok:
                survived += 1
                survivors.append((family, name))
                print(f"  SURVIVED  {family:<22} {name}")
                if family == "SENTINEL":
                    print("  HARNESS DEAD: the SENTINEL survived. The suite is not running against "
                          "the mutant, so every other result in this run is meaningless.")
                    sys.exit(2)
            else:
                caught += 1
                print(f"  caught    {family:<22} {name}")
    finally:
        with open(TARGET, "w", encoding="utf-8") as f:
            f.write(original)

    print("\nRESTORED. Re-running the clean suite as the closing control.")
    ok, tail = run_suite()
    if not ok:
        print(f"  HARNESS DEAD: the suite is RED after restore -- the file was not restored cleanly: {tail}")
        sys.exit(2)
    print(f"  clean: {tail}")

    total = caught + survived
    print(f"\n{caught}/{total} injected / caught, {survived} survived, 0 broken")
    if survivors:
        print("SURVIVORS (each is an unguarded defect class, not a pass):")
        for fam, nm in survivors:
            print(f"  - {fam}: {nm}")
        sys.exit(1)
    print("ALL MUTATIONS CAUGHT")


if __name__ == "__main__":
    main()
