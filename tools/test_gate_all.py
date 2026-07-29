#!/usr/bin/env python3
"""Tests for gate_all -- the run-all floor that runs whole_crop_gate on EVERY certified crop.

whole_crop_gate validates ONE crop; release_verify runs it on target+reference; the pre-commit hook is
a regression net on CHANGED crops. Nothing asserted the WHOLE certified roster passes the suite, so a
regression on an untouched crop (or a newly-certified crop nobody re-gated) could sit green. gate_all
closes that. This test confirms: the clean canonical is green (all certified PASS), an uncertified §E
shell is EXCLUDED from the run (unfilled shells legitimately fail the suite), and a defect injected into
a SCRATCH COPY of the real canonical is caught (that crop shows up FAILED, CLI exits 1).
Run: python3 tools/test_gate_all.py
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gate_all import run

HERE = os.path.dirname(os.path.abspath(__file__))
_TOOL = os.path.join(HERE, "gate_all.py")
_CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")


def _run_cli(path):
    r = subprocess.run([sys.executable, _TOOL, path], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


# ---- clean canonical: every certified crop passes; shells excluded from the run ----
cert, failed = run(_CANON)
# DERIVED, not hardcoded (2026-07-29): this said `== 114` and rotted at every cert, reading as a
# suite failure when nothing was wrong (114 -> 121 by the artichoke arc). The intent is that the
# run covers EXACTLY the certified set, so compute that set from the canonical instead.
with open(_CANON, encoding="utf-8") as _fh:
    _expected = {c["slug"] for c in json.load(_fh)["crops"]
                 if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"}
assert set(cert) == _expected, (
    "gate_all's run must cover exactly the verified_gs_arc set",
    sorted(_expected - set(cert)), sorted(set(cert) - _expected))
assert len(cert) >= 114, ("the certified roster must never shrink below its 2026 floor", len(cert))
assert failed == [], ("clean canonical: no certified crop should fail whole_crop_gate", failed)
assert "olive" not in cert and "button-mushroom" not in cert, ("uncertified §E shells must be excluded", cert)

rc, out = _run_cli(_CANON)
assert rc == 0 and "PASS" in out, ("clean canonical CLI should exit 0", rc, out)


# ---- scratch copy: inject a defect into a certified crop -> that crop FAILS, CLI exits 1 ----
data = json.load(open(_CANON, encoding="utf-8"))
scratch = copy.deepcopy(data)
tc = next(c for c in scratch["crops"] if c.get("slug") == "cherry-tomato")
del tc["germination_light"]   # A39 register-coverage will bounce this certified crop
fd, p = tempfile.mkstemp(suffix=".json")
os.close(fd)
with open(p, "w", encoding="utf-8") as fh:
    json.dump(scratch, fh)
try:
    cert2, failed2 = run(p)
    assert any(slug == "cherry-tomato" for slug, _ in failed2), ("defect crop must be reported FAILED", failed2)
    rc, out = _run_cli(p)
    assert rc == 1 and "cherry-tomato" in out, ("scratch-defect CLI should exit 1 naming the crop", rc, out)
finally:
    os.unlink(p)

print("gate_all tests: OK")
