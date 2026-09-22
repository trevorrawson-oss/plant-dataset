#!/usr/bin/env python3
"""Refusal spec for whole_crop_gate section G, narrowed 2026-09-21 (PLA-466).

CONTRACT UNDER TEST. "certified" (verification_status.status) and "launch-ready"
(launch_ready_core / launch_ready_seasoned) are distinct states. A blocking finding drives the
FLAGS, never the status. So a live blocker is a violation only while the crop still CLAIMS
readiness on either flag; a live blocker with both flags false is the coherent state.

Before the narrowing the gate read "certified implies no live blocker". That rule was never
exercised: all 12 blocking findings in the dataset were status:resolved, so PLA-466's four were
the first live ones and the contradiction surfaced only at the gauntlet.

Each case runs the REAL gate as a subprocess against a scratch canonical, so nothing here can
pass by mocking the predicate it is meant to test.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GATE = os.path.join(HERE, "whole_crop_gate.py")
CANON = os.path.join(REPO, "crops_data_final.json")

SUBJECT = "plum"
BLOCKER_ID = "test_g_predicate_synthetic_blocker"


def _normalize(crop):
    """Put the subject in a KNOWN baseline before any injection: both launch flags true and NO
    blocking findings of any status.

    Without this the tests silently depend on whatever the live canonical happens to hold for
    SUBJECT. They were written when plum carried no blocker, and PLA-466's own landing then gave
    plum a live one -- which broke three of them. That is precisely the PLA-544 class (a test
    pinned to a state the next promote invalidates), committed by the very session that filed it.
    Normalizing makes each case measure ONLY what it injects.
    """
    vs = crop["verification_status"]
    vs["open_findings"] = [f for f in (vs.get("open_findings") or [])
                           if not (isinstance(f, dict) and f.get("blocks_launch"))]
    vs["launch_ready_core"] = True
    vs["launch_ready_seasoned"] = True


def run_gate(mutate):
    """Apply `mutate(crop)` to a NORMALIZED scratch canonical and return (passed, stdout)."""
    with open(CANON, encoding="utf-8") as f:
        data = json.load(f)
    crop = next(c for c in data["crops"] if c["slug"] == SUBJECT)
    _normalize(crop)
    mutate(crop)
    tmp = tempfile.mkdtemp(prefix="gate_g_")
    path = os.path.join(tmp, "crops.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    r = subprocess.run([sys.executable, GATE, SUBJECT, path], capture_output=True, text=True)
    return any(l.startswith("GATE: PASS") for l in r.stdout.splitlines()), r.stdout


def add_blocker(crop, status="open"):
    crop["verification_status"].setdefault("open_findings", []).append(
        {"id": BLOCKER_ID, "severity": "high", "status": status, "blocks_launch": True,
         "summary": "synthetic", "basis": "synthetic"})


def set_flags(crop, core, seasoned):
    crop["verification_status"]["launch_ready_core"] = core
    crop["verification_status"]["launch_ready_seasoned"] = seasoned


class TestSectionGPredicate(unittest.TestCase):

    def test_control_normalized_subject_passes(self):
        """POSITIVE CONTROL. If the normalized subject already fails, nothing below means anything."""
        ok, out = run_gate(lambda c: None)
        self.assertTrue(ok, f"{SUBJECT} does not pass the gate unmutated:\n{out[-2000:]}")

    def test_live_blocker_with_core_true_REDDENS(self):
        def m(c):
            set_flags(c, True, True)
            add_blocker(c)
        ok, out = run_gate(m)
        self.assertFalse(ok, "a live blocker while launch_ready_core is true must fail")
        self.assertIn("blocks launch while launch_ready is still true", out)
        self.assertIn(BLOCKER_ID, out)

    def test_live_blocker_with_only_seasoned_true_REDDENS(self):
        """Either flag alone is still a claim of readiness."""
        def m(c):
            set_flags(c, False, True)
            add_blocker(c)
        ok, out = run_gate(m)
        self.assertFalse(ok, "a live blocker while launch_ready_seasoned is true must fail")
        self.assertIn("blocks launch while launch_ready is still true", out)

    def test_live_blocker_with_both_flags_false_STAYS_GREEN(self):
        """The PLA-466 coherent state: the crop has honestly de-flagged itself."""
        def m(c):
            set_flags(c, False, False)
            add_blocker(c)
        ok, out = run_gate(m)
        self.assertTrue(ok, f"a live blocker with both flags false must PASS:\n{out[-2000:]}")
        self.assertIn("which is the coherent state", out)
        self.assertIn("open_findings blockers (blocks_launch AND status!=resolved): 1", out)

    def test_resolved_blocker_with_flags_true_STAYS_GREEN(self):
        """Unchanged behaviour: all 12 pre-PLA-466 blockers are resolved and must not redden."""
        def m(c):
            set_flags(c, True, True)
            add_blocker(c, status="resolved")
        ok, out = run_gate(m)
        self.assertTrue(ok, f"a RESOLVED blocker must not fail:\n{out[-2000:]}")
        self.assertIn("open_findings blockers (blocks_launch AND status!=resolved): 0", out)

    def test_the_blocker_is_still_counted_and_printed_when_green(self):
        """The narrowing must not make a live blocker invisible in the gauntlet output."""
        def m(c):
            set_flags(c, False, False)
            add_blocker(c)
        ok, out = run_gate(m)
        self.assertTrue(ok)
        self.assertIn("1 live blocker(s) recorded", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
