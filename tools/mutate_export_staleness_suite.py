#!/usr/bin/env python3
"""Instrumented mutation harness for the PLA-258 export-staleness gate. PLA-215 convention.

The suite under test claims to catch a defect that is invisible to every other instrument
in this repo: an export whose BYTES ARE CORRECT and whose SOURCE IS OLD. That claim is
worth exactly as much as a run like this one, so each guard family gets a defect sneaked
at it, injected into a SCRATCH COPY of the gate, never the working file.

The three self-checks the convention requires (PLA-138's harness dedented an already-
indented template, silently ran the CLEAN fixture, and reported every mutation as
surviving -- confident garbage, in the wrong direction):

  MUTATION-APPLIED MARKER  every mutated copy carries `# MUTATION-APPLIED: <name>`, asserted
                           present in the file about to execute AND asserted to differ from
                           the original. An anchor that failed to match is a HARD ERROR, not
                           a survivor -- that distinction is the whole point.
  SENTINEL                 one guaranteed-fatal mutation must redden, or the run prints
                           HARNESS DEAD and reports nothing else.
  POSITIVE CONTROL         one guaranteed-invisible mutation must stay GREEN, so "the guard
                           is blind" stays distinguishable from "the injection was a no-op".

Run: python3 tools/mutate_export_staleness_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "export_staleness_gate.py")
SUITE = os.path.join(HERE, "test_export_staleness_gate.py")

# (name, anchor, replacement, the guard that MUST redden)
# `None` as the expected guard means "no guard should redden" (the positive control).
MUTATIONS = [
    # ---- E1: provenance ----
    ("E1 blind: a stale stamp is accepted as current",
     "    elif stamped != canonical_sha:",
     "    elif False:",
     "TestE1AppProvenance::test_a_stale_stamp_is_caught"),

    ("E1 blind: a missing stamp is treated as nothing-to-report",
     "    if not os.path.exists(mpath):",
     "    if False:",
     "TestE1AppProvenance::test_a_missing_manifest_is_caught_not_skipped"),

    ("E1 blind: an unparseable stamp is swallowed and the export passes",
     "    except (ValueError, OSError) as e:",
     "    except (ValueError, OSError) as e:\n        return [], []\n    except SyntaxError as e:",
     "TestE1AppProvenance::test_an_unparseable_manifest_is_caught_not_swallowed"),

    # ---- E2: integrity. The key-set family is PLA-162's defect at a new boundary. ----
    ("E2 blind: iterate only what the stamp RECORDS (PLA-162's one-directional shape)",
     "    for missing in sorted(expected - got):",
     "    for missing in sorted(set()):",
     "TestE2AppIntegrity::test_an_artifact_the_manifest_forgot_is_caught"),

    ("E2 blind: an artifact the stamp invented is ignored",
     "    for extra in sorted(got - expected):",
     "    for extra in sorted(set()):",
     "TestE2AppIntegrity::test_an_artifact_the_manifest_invented_is_caught"),

    ("E2 blind: the artifact hash is never compared (a hand edit ships)",
     "        if actual != recorded[rel]:",
     "        if False:",
     "TestE2AppIntegrity::test_a_hand_edited_artifact_is_caught"),

    ("E2 blind: a stamped artifact missing from disk is skipped quietly",
     "        if not os.path.exists(full):",
     "        if False and not os.path.exists(full):",
     "TestE2AppIntegrity::test_a_missing_artifact_is_caught"),

    # ---- E3: the website pin ----
    ("E3 blind: a stale submodule pin is accepted",
     "    if pinned_sha != canonical_sha:",
     "    if False:",
     "TestE3AstroPin::test_a_stale_submodule_pin_is_caught"),

    ("E3 blind: a pin this repo cannot resolve is treated as fine",
     "    if blob is None:",
     "    if False:",
     "TestE3AstroPin::test_a_pin_at_a_commit_the_dataset_does_not_have_is_caught"),

    ("E3 blind: a repo with no submodule entry passes",
     "    if not entry:",
     "    if False:",
     "TestE3AstroPin::test_a_repo_with_no_submodule_entry_is_caught"),

    # ---- the unmeasured channel: an instrument that cannot justify its zero ----
    ("UNMEASURED erased: an absent app repo reports a clean zero",
     '        return [], [f"UNMEASURED app: no repo at {app_root} -- export currency NOT checked"]',
     "        return [], []",
     "TestUnmeasuredIsNotGreen::test_an_absent_app_repo_reports_unmeasured_not_clean"),

    ("UNMEASURED erased: an absent astro repo reports a clean zero",
     '        return [], [f"UNMEASURED astro: no repo at {astro_root} -- site currency NOT checked"]',
     "        return [], []",
     "TestUnmeasuredIsNotGreen::test_an_absent_astro_repo_reports_unmeasured_not_clean"),

    ("UNMEASURED collapsed into violations (the two become indistinguishable)",
     '        "violations": av + sv,\n        "unmeasured": au + su,',
     '        "violations": av + sv + au + su,\n        "unmeasured": [],',
     "TestUnmeasuredIsNotGreen::test_unmeasured_is_distinguishable_from_a_violation"),

    # ---- SENTINEL: guaranteed fatal. If this survives, the harness is not running. ----
    ("SENTINEL: the gate never reports anything at all",
     "def all_violations(canonical_path=None, app_root=None, astro_root=None, dataset_root=None):",
     "def all_violations(canonical_path=None, app_root=None, astro_root=None, dataset_root=None):\n    return []",
     "__SENTINEL__"),

    # ---- POSITIVE CONTROL: guaranteed invisible. If this reddens, the suite is
    #      asserting on prose it should not be asserting on. ----
    ("POSITIVE CONTROL: a violation message's advisory tail is reworded",
     "run `npm run build:guides` in {app_root}.\")",
     "rebuild the export in {app_root}.\")",
     None),
]


def run_suite(workdir):
    """(passed, failing_test_ids). Runs the suite against whatever gate sits in workdir."""
    r = subprocess.run([sys.executable, "-m", "pytest", "test_export_staleness_gate.py",
                        "-q", "--no-header", "-p", "no:cacheprovider"],
                       cwd=workdir, capture_output=True, text=True)
    failing = set()
    for line in (r.stdout + r.stderr).splitlines():
        if line.startswith("FAILED "):
            failing.add(line.split(" ", 1)[1].split(" ")[0])
    return r.returncode == 0, failing


def main():
    original = open(GATE).read()

    # Baseline: the CLEAN gate must be green, or nothing below means anything.
    base = tempfile.mkdtemp()
    shutil.copy(GATE, base)
    shutil.copy(SUITE, base)
    ok, failing = run_suite(base)
    shutil.rmtree(base, ignore_errors=True)
    if not ok:
        print("HARNESS DEAD: the CLEAN suite is not green; mutation results would be noise.")
        print(f"  failing: {sorted(failing)}")
        return 1
    print("baseline: CLEAN suite green\n")

    results = []
    for name, anchor, replacement, expect in MUTATIONS:
        if anchor not in original:
            print(f"HARNESS DEAD: anchor for {name!r} did not match the gate source.")
            print("  A mutation that cannot be applied is a HARD ERROR, never a survivor.")
            return 1
        mutated = original.replace(anchor, replacement, 1)
        marker = f"# MUTATION-APPLIED: {name}\n"
        mutated = marker + mutated

        work = tempfile.mkdtemp()
        try:
            gate_copy = os.path.join(work, "export_staleness_gate.py")
            with open(gate_copy, "w") as f:
                f.write(mutated)
            shutil.copy(SUITE, work)

            # liveness: the file about to execute carries the marker AND differs from clean
            on_disk = open(gate_copy).read()
            assert marker in on_disk, f"MUTATION-APPLIED marker absent for {name!r}"
            assert on_disk.replace(marker, "", 1) != original, \
                f"mutated copy is byte-identical to the original for {name!r}"

            ok, failing = run_suite(work)
        finally:
            shutil.rmtree(work, ignore_errors=True)

        if expect is None:                      # positive control
            verdict = "GREEN (as required)" if ok else f"REDDENED -- {sorted(failing)}"
            results.append(("CONTROL", name, ok, verdict))
        else:
            hit = any(expect.split("::")[-1] in f for f in failing)
            results.append(("SENTINEL" if expect == "__SENTINEL__" else "MUTATION",
                            name, hit or (expect == "__SENTINEL__" and not ok),
                            f"caught by {sorted(failing)[:3]}" if failing else "SURVIVED"))

    sentinel = [r for r in results if r[0] == "SENTINEL"]
    if not sentinel or not sentinel[0][2]:
        print("HARNESS DEAD: the sentinel mutation did not redden the suite.")
        print("  Every other result in this run is untrustworthy and is not reported.")
        return 1

    control = [r for r in results if r[0] == "CONTROL"]
    control_ok = all(r[2] for r in control)

    caught = sum(1 for r in results if r[0] == "MUTATION" and r[2])
    total = sum(1 for r in results if r[0] == "MUTATION")
    survivors = [r for r in results if r[0] == "MUTATION" and not r[2]]

    for kind, name, good, detail in results:
        flag = "OK  " if good else "FAIL"
        print(f"  [{flag}] {kind:<8} {name}\n           -> {detail}")

    print(f"\nsentinel: reddened (harness live)")
    print(f"positive control: {'held green' if control_ok else 'REDDENED -- suite over-asserts'}")
    print(f"mutations: {caught}/{total} CAUGHT, {len(survivors)} survivor(s)")
    for _, name, _, _ in survivors:
        print(f"  SURVIVOR: {name}")
    return 0 if (caught == total and control_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
