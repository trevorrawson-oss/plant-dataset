#!/usr/bin/env python3
"""Integration test: the register VALUE-shape gates are wired into the always-on whole_crop_gate.

A39 (register_coverage_gate) enforces the register fields are PRESENT-or-null. This test locks the
companion guarantee -- that their VALUE shape is validated by the always-on suite, not only on-demand:
  A40 timing_spine_gate.timing_spine_violations  (enum / [min,max] / ladder / provenance)
  A41 climate_threshold_gate.check_crop           (range / enum / frost<chilling<heat coherence)
  A42 seedling_light_gate.check_crop              (enum / cap_hours <=> photoperiod_capped)

Method (CLAUDE.md TDD): inject ONE bad VALUE per register into a SCRATCH COPY of the REAL canonical on
a certified crop and confirm whole_crop_gate now BOUNCES with that A-number's tag; confirm the clean
crop is green on these dimensions. Before the wiring this test is RED (whole_crop_gate passed a garbage
register value); after wiring it is GREEN. Run: python3 tools/test_whole_crop_gate_register_shape.py
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
_WHOLE = os.path.join(HERE, "whole_crop_gate.py")
_CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")
SLUG = "cherry-tomato"   # a fully-green certified crop that carries all four register sets


def _run_whole(path):
    r = subprocess.run([sys.executable, _WHOLE, SLUG, path], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def _scratch_with(mutate):
    """Deep-copy the real canonical, mutate the target crop, write to a temp file, return its path."""
    data = json.load(open(_CANON, encoding="utf-8"))
    crop = next(c for c in data["crops"] if c.get("slug") == SLUG)
    mutate(crop)
    fd, p = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return p


# ---- baseline: the clean crop is green on all three register-shape dimensions ----
rc, out = _run_whole(_CANON)
assert rc == 0 and "GATE: PASS" in out, ("clean canonical crop should PASS", rc, out[-400:])
for tag in ("VIOLATION: timing-spine", "VIOLATION: climate-shape", "VIOLATION: seedling-light"):
    assert tag not in out, (f"clean crop unexpectedly flagged {tag}", out)


# ---- one bad VALUE per register -> the matching A-number must fire ----
CASES = [
    # (label, mutate, expected VIOLATION tag)
    ("timing: sow_depth_inches min>max",
     lambda c: c.__setitem__("sow_depth_inches", [5, 2]),
     "VIOLATION: timing-spine"),
    ("timing: propagule bad enum",
     lambda c: c.__setitem__("propagule", "banana"),
     "VIOLATION: timing-spine"),
    ("climate: heat_threshold_f out of range",
     lambda c: c.__setitem__("heat_threshold_f", 200),
     "VIOLATION: climate-shape"),
    ("climate: frost above heat (coherence)",
     lambda c: c.__setitem__("frost_tolerance_f", 99),
     "VIOLATION: climate-shape"),
    ("seedling: seedling_light bad enum",
     lambda c: c.__setitem__("seedling_light", "full_sun"),
     "VIOLATION: seedling-light"),
    ("seedling: orphan cap_hours",
     lambda c: c.__setitem__("seedling_light_cap_hours", 11),
     "VIOLATION: seedling-light"),
]

for label, mutate, tag in CASES:
    p = _scratch_with(mutate)
    try:
        rc, out = _run_whole(p)
        assert rc == 1 and tag in out, (f"[{label}] whole_crop_gate should bounce with {tag}", rc,
                                        [l for l in out.splitlines() if "VIOLATION" in l][-8:])
    finally:
        os.unlink(p)

print("whole_crop_gate register-shape wiring tests: OK")
