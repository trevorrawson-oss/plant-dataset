#!/usr/bin/env python3
"""What run_test_tree REPORTS for the outcomes a green-looking verdict can hide (housekeeping kickoff 60,
2026-10-03: PLA-653, the rc-0 STALE gap, the ERROR gap, and "Fix 0").

Each test builds throwaway test files in a temp dir INSIDE the repo root (outside tools/, so whole-tree
discovery and the tools/ harness copies never see them), then drives the REAL run_test_tree.main() over them
through a subprocess probe that swaps in a test-only WAIVERS table. The runner's output is the thing asserted.

  1. A waived test that now PASSES, on a run where pytest exits 0, is reported STALE, and the VERDICT says so.
     (Until 2026-10-03 the STALE check ran only when something else failed.)
  2. A waived test whose file was NOT in this run's population is "not in population (not run)", never STALE,
     on a green run AND on a run where another test fails (PLA-653's measured case).
  3. A test that ERRORS (fixture / setup error) FAILS the tree. (Until 2026-10-03 only FAILED lines were read:
     pytest "rc=1 | 1 error" produced "VERDICT: PASS".) An error is never waivable.
  4. A pytest.skip is counted in the VERDICT ("Fix 0"); it is not a pass and not a failure.
  5-7. (PLA-625, 2026-10-29) The pytest population runs under xdist `-n auto` by default and `--serial` restores the
     single-process run; a red test or a red script still fails the parallel default, a waiver fires in both modes,
     and the parallel default REFUSES (BROKEN) when pytest-xdist is not installed.
Run: python3 -m pytest tools/test_run_test_tree_reporting.py -q
SHIPS MUTATION-TESTED via mutate_run_test_tree.py (M8-M15).
"""
import os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PASSING = "def test_ok():\n    assert True\n"
FAILING = "def test_bad():\n    assert False, 'PROBE: an unwaived failure'\n"
ERRORING = ("import pytest\n\n\n@pytest.fixture\ndef broken():\n    raise RuntimeError('PROBE: setup error')\n\n\n"
            "def test_uses_broken(broken):\n    assert True\n")
SKIPPING = "import pytest\n\n\ndef test_skips():\n    pytest.skip('PROBE: inputs gone')\n"

SCRIPT_FAILING = "assert False, 'PROBE: a script-style failure'\n"
# Passes only inside an xdist worker / only outside one, so the MODE the runner chose is read off the test result,
# not off the runner's own say-so.
IN_WORKER = "import os\n\n\ndef test_in_worker():\n    assert os.environ.get('PYTEST_XDIST_WORKER'), 'not in an xdist worker'\n"
NOT_IN_WORKER = "import os\n\n\ndef test_not_in_worker():\n    assert not os.environ.get('PYTEST_XDIST_WORKER'), 'in an xdist worker'\n"

PROBE = """import re, sys
sys.path.insert(0, {tools!r})
import run_test_tree as R
R.WAIVERS = {{{tid!r}: {{"ticket": "PROBE", "reason": "probe", "character": re.compile(r"PROBE")}}}}
if {no_xdist!r}:
    R.xdist_available = lambda: False
sys.argv = ["run_test_tree.py", "--files", *{files!r}, *{extra!r}]
sys.exit(R.main())
"""


class _Probe(unittest.TestCase):
    """Throwaway files + the probe driver; no tests of its own."""
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="_rtt_probe_", dir=ROOT)
        self.rel = os.path.relpath(self.dir, ROOT)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def file(self, name, body):
        with open(os.path.join(self.dir, name), "w", encoding="utf-8") as f:
            f.write(body)
        return os.path.join(self.rel, name)

    def runner(self, files, waived_tid, extra=(), no_xdist=False):
        probe = os.path.join(self.dir, "probe_main.py")
        with open(probe, "w", encoding="utf-8") as f:
            f.write(PROBE.format(tools=HERE, tid=waived_tid, files=files, extra=list(extra), no_xdist=no_xdist))
        r = subprocess.run([sys.executable, probe], cwd=ROOT, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def verdict(self, out):
        return [l for l in out.splitlines() if l.startswith("VERDICT")][-1]


class Reporting(_Probe):
    # 1 -------------------------------------------------------------------------------------------
    def test_a_waived_test_that_now_passes_is_STALE_on_an_rc0_run(self):
        f = self.file("test_now_passes.py", PASSING)
        rc, out = self.runner([f], f"{f}::test_ok")
        self.assertEqual(rc, 0, out)
        self.assertIn("STALE WAIVER", out)
        self.assertIn("STALE WAIVER(S)", self.verdict(out), "a green run must not pass a stale waiver silently")

    # 2 -------------------------------------------------------------------------------------------
    def test_a_waived_test_not_collected_is_not_STALE_on_a_green_run(self):
        f = self.file("test_green.py", PASSING)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived")
        self.assertEqual(rc, 0, out)
        self.assertNotIn("STALE WAIVER", out)
        self.assertIn("waived test not in population (not run): tools/test_elsewhere.py::test_waived", out)

    def test_a_waived_test_not_collected_is_not_STALE_when_another_test_fails(self):
        f = self.file("test_red.py", FAILING)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived")
        self.assertNotEqual(rc, 0, out)
        self.assertNotIn("STALE WAIVER", out)
        self.assertIn("waived test not in population (not run): tools/test_elsewhere.py::test_waived", out)

    # 3 -------------------------------------------------------------------------------------------
    def test_a_test_that_ERRORS_fails_the_tree(self):
        f = self.file("test_errors.py", ERRORING)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived")
        self.assertNotEqual(rc, 0, out)
        self.assertTrue(self.verdict(out).startswith("VERDICT: FAIL"), out)
        self.assertIn(f"test error: {f}::test_uses_broken", out)

    def test_an_ERROR_is_never_waived(self):
        f = self.file("test_errors.py", ERRORING)
        rc, out = self.runner([f], f"{f}::test_uses_broken")
        self.assertNotEqual(rc, 0, out)
        self.assertNotIn("WAIVED:", out)

    # 4 -------------------------------------------------------------------------------------------
    def test_a_pytest_skip_is_counted_in_the_verdict(self):
        f = self.file("test_skips.py", SKIPPING)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived")
        self.assertEqual(rc, 0, out)
        self.assertIn("1 pytest test(s) SKIPPED (ran nothing)", self.verdict(out))
        self.assertIn("PROBE: inputs gone", out)


class Mode(_Probe):
    """PLA-625 ruling 09d4844d (2026-10-29): the pytest population runs under pytest-xdist `-n auto` by default, and
    `--serial` gives the pre-ruling behavior exactly. The mode is pinned by what the TESTS saw (PYTEST_XDIST_WORKER),
    not only by what the runner prints; the positive controls prove the parallel default still fails a red tree."""

    # 5 -------------------------------------------------------------------------------------------
    def test_the_default_runs_pytest_in_xdist_workers(self):
        f = self.file("test_mode.py", IN_WORKER)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived")
        self.assertEqual(rc, 0, out)
        self.assertIn("(parallel, -n auto)", out)

    def test_serial_runs_pytest_in_one_process(self):
        f = self.file("test_mode.py", NOT_IN_WORKER)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived", extra=["--serial"])
        self.assertEqual(rc, 0, out)
        self.assertIn("(serial)", out)

    def test_serial_is_not_the_default(self):
        f = self.file("test_mode.py", NOT_IN_WORKER)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived")
        self.assertNotEqual(rc, 0, out)
        self.assertTrue(self.verdict(out).startswith("VERDICT: FAIL"), out)

    # 6 positive controls under the parallel default ----------------------------------------------
    def test_parallel_a_failing_test_fails_the_tree(self):
        f = self.file("test_red.py", FAILING)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived")
        self.assertEqual(rc, 1, out)
        self.assertTrue(self.verdict(out).startswith("VERDICT: FAIL"), out)
        self.assertIn(f"unwaived test failure: {f}::test_bad", out)

    def test_parallel_a_failing_script_style_file_fails_the_tree(self):
        f = self.file("test_script_red.py", SCRIPT_FAILING)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived")
        self.assertEqual(rc, 1, out)
        self.assertTrue(self.verdict(out).startswith("VERDICT: FAIL"), out)
        self.assertIn(f"{f}: rc=1", out)

    def test_a_waiver_fires_in_both_modes(self):
        f = self.file("test_red.py", FAILING)
        for extra in ([], ["--serial"]):
            rc, out = self.runner([f], f"{f}::test_bad", extra=extra)
            self.assertEqual(rc, 0, (extra, out))
            self.assertIn(f"WAIVED: {f}::test_bad [PROBE]", out)
            self.assertIn("1 waived failure(s)", self.verdict(out))

    # 7 refusal spec ------------------------------------------------------------------------------
    def test_the_parallel_default_REFUSES_without_xdist(self):
        f = self.file("test_green.py", PASSING)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived", no_xdist=True)
        self.assertEqual(rc, 3, out)
        self.assertIn("pytest-xdist", out)
        self.assertTrue(self.verdict(out).startswith("VERDICT: BROKEN"), out)

    def test_serial_needs_no_xdist(self):
        f = self.file("test_green.py", PASSING)
        rc, out = self.runner([f], "tools/test_elsewhere.py::test_waived", extra=["--serial"], no_xdist=True)
        self.assertEqual(rc, 0, out)


if __name__ == "__main__":
    unittest.main()
