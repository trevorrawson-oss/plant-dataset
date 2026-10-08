#!/usr/bin/env python3
"""Instrumented mutation harness for export_staleness_gate, the informational consumer-pin report
(PLA-713; rewritten from the PLA-258 blocking gate). PLA-215 convention.

The suite claims the report counts how far behind each consumer's ORIGIN pin is, reports a pin it
cannot read as UNMEASURED, and never fails a run -- a stale pin produces a report and exit 0. Each
guard family gets a defect sneaked at it, injected into a SCRATCH COPY of the gate, never the
working file.

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
    # ---- the count: how far behind ----
    ("behind blind: the commit range is reversed (counts what the pin has, not what it lacks)",
     '    behind = _git(dataset_root, "rev-list", "--count", f"{pinned}..{head}")',
     '    behind = _git(dataset_root, "rev-list", "--count", f"{head}..{pinned}")',
     "TestBehindCount::test_a_pin_two_commits_back_is_two_behind_with_a_different_canonical"),

    ("canonical blind: every pin reads as serving origin/main's bytes",
     "               canonical_same=pin_canon == head_canon,",
     "               canonical_same=True,",
     "TestBehindCount::test_a_pin_two_commits_back_is_two_behind_with_a_different_canonical"),

    ("off-main blind: a pin carrying commits main lacks is reported as merely behind",
     '    if row["ahead"]:',
     "    if False:",
     "TestBehindCount::test_a_pin_off_origin_main_is_flagged"),

    # ---- where the pin is read from ----
    ("wrong ref: the origin's default HEAD is read instead of the consumer's shipping branch",
     '                f"refs/heads/{branch}") is None:',
     '                "HEAD") is None:',
     "TestReadsOriginNotCheckout::test_the_branch_named_is_the_branch_read"),

    ("consumer table: the app's gitlink path drifts",
     '     "feat/community-foundation", "vendor/plant-dataset"),',
     '     "feat/community-foundation", "plant-dataset"),',
     "TestConsumerTable::test_the_consumers_are_the_ruled_pins"),

    ("population: a consumer row is silently dropped",
     "    rows = [pin_status(*c, dataset_root=dataset_root, dataset_ref=dataset_ref) for c in consumers]",
     "    rows = [pin_status(*c, dataset_root=dataset_root, dataset_ref=dataset_ref) for c in consumers][:1]",
     "TestConsumerTable::test_every_consumer_is_reported"),

    # ---- NEVER BLOCKS (ruling item 5): a stale pin must report and exit 0 ----
    ("blocking restored: a stale or unmeasured pin fails the run",
     '    return 0\n\n\nif __name__ == "__main__":',
     '    return 1 if r["unmeasured"] or any(x["behind"] for x in r["consumers"]) else 0\n\n\nif __name__ == "__main__":',
     "TestStalePinReportsAndNeverFails::test_a_stale_pin_exits_zero_and_says_how_far_behind"),

    # ---- the unmeasured channel: an instrument that cannot justify its zero ----
    ("unresolvable pin: the history check is skipped",
     '    if _git(dataset_root, "cat-file", "-e", f"{pinned}^{{commit}}") is None:',
     "    if False:",
     "TestUnmeasured::test_a_pin_this_repo_cannot_resolve_is_unmeasured"),

    ("gitlink shape: any tree entry is accepted as a pin",
     '        if len(parts) < 3 or parts[0] != "160000":',
     "        if len(parts) < 3:",
     "TestUnmeasured::test_a_path_that_is_not_a_gitlink_is_unmeasured"),

    ("missing entry: an absent gitlink is not reported as such",
     "        if not entry:",
     "        if False:",
     "TestUnmeasured::test_a_branch_without_the_gitlink_is_unmeasured"),

    ("unmeasured erased: the count of unread pins is always zero",
     '            "unmeasured": sum(not r["measured"] for r in rows)}',
     '            "unmeasured": 0}',
     "TestUnmeasured::test_unmeasured_is_counted_apart_from_measured"),

    # ---- SENTINEL: guaranteed fatal. If this survives, the harness is not running. ----
    ("SENTINEL: every row raises",
     '    row = {"check": check, "consumer": label,',
     '    raise RuntimeError("sentinel")\n    row = {"check": check, "consumer": label,',
     "__SENTINEL__"),

    # ---- POSITIVE CONTROL: guaranteed invisible. If this reddens, the suite is
    #      asserting on prose it should not be asserting on. ----
    ("POSITIVE CONTROL: the summary's advisory tail is reworded",
     'happen only on Trevor\'s call (PLA-713). Never blocks.")',
     'happen only on Trevor\'s call (PLA-713). Does not block.")',
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
