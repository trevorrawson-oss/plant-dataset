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
Run: python3 -m pytest tools/test_run_test_tree_reporting.py -q
SHIPS MUTATION-TESTED via mutate_run_test_tree.py (M8-M11).
"""
import os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PASSING = "def test_ok():\n    assert True\n"
FAILING = "def test_bad():\n    assert False, 'PROBE: an unwaived failure'\n"
ERRORING = ("import pytest\n\n\n@pytest.fixture\ndef broken():\n    raise RuntimeError('PROBE: setup error')\n\n\n"
            "def test_uses_broken(broken):\n    assert True\n")
SKIPPING = "import pytest\n\n\ndef test_skips():\n    pytest.skip('PROBE: inputs gone')\n"

PROBE = """import re, sys
sys.path.insert(0, {tools!r})
import run_test_tree as R
R.WAIVERS = {{{tid!r}: {{"ticket": "PROBE", "reason": "probe", "character": re.compile(r"PROBE")}}}}
sys.argv = ["run_test_tree.py", "--files", *{files!r}]
sys.exit(R.main())
"""


class Reporting(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="_rtt_probe_", dir=ROOT)
        self.rel = os.path.relpath(self.dir, ROOT)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def file(self, name, body):
        with open(os.path.join(self.dir, name), "w", encoding="utf-8") as f:
            f.write(body)
        return os.path.join(self.rel, name)

    def runner(self, files, waived_tid):
        probe = os.path.join(self.dir, "probe_main.py")
        with open(probe, "w", encoding="utf-8") as f:
            f.write(PROBE.format(tools=HERE, tid=waived_tid, files=files))
        r = subprocess.run([sys.executable, probe], cwd=ROOT, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def verdict(self, out):
        return [l for l in out.splitlines() if l.startswith("VERDICT")][-1]

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


if __name__ == "__main__":
    unittest.main()
