#!/usr/bin/env python3
"""Unit test for the pre-commit hook's Step-3.5 shell-build allowance.
Run from repo root: python3 tools/test_precommit_release_verify.py

The hook blocks a commit on a NEW gate violation for a changed crop. A Step-3.5
region-shell build legitimately trades stub/shape violations for `region_notes pair
both null` ones: the PENDING stub was MASKING the null region_notes pair, and
building the shell un-masks it. Null region_notes is the explicitly accepted Step-3.5
admission state (Steps 6/7 fill it), so that specific "new" violation is NOT a
regression. This pins that allowance -- and pins that a REAL region_notes-blanking
on an already-built cell is still caught.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precommit_release_verify import drop_shell_build_unmasks, drop_precert_anchoring

STUB = {"plantings": ["PENDING CORRECTION PHASE -- windows not yet pulled."]}
SHELL = {"plantings": [{"succession_id": 1, "track": "beginner"}]}
NULL_NOTES = "VIOLATION: region_notes pair both null: se_gulf"

# case 1: se_gulf stub (base) -> shell (candidate): the null-notes violation is the
# admission unmask, NOT a regression -> dropped from the blocking set.
base = {"regions": {"se_gulf": dict(STUB)}}
cand = {"regions": {"se_gulf": dict(SHELL)}}
assert drop_shell_build_unmasks({NULL_NOTES}, base, cand) == set(), "stub->shell unmask must be forgiven"

# case 2: se_gulf already a shell in base; its notes get blanked in candidate -> a
# real regression (the cell did NOT graduate from a stub) -> still blocks.
base2 = {"regions": {"se_gulf": dict(SHELL)}}
cand2 = {"regions": {"se_gulf": dict(SHELL)}}
assert drop_shell_build_unmasks({NULL_NOTES}, base2, cand2) == {NULL_NOTES}, "non-stub regression must NOT be forgiven"

# case 3: a non-region_notes new violation is never forgiven, even on a graduated cell.
other = "VIOLATION: dual-voice null sibling: pests[0].cause_beginner"
assert drop_shell_build_unmasks({other}, base, cand) == {other}, "unrelated violations must never be forgiven"

# case 4: mixed set -- only the graduated region_notes-null is dropped.
mixed = {NULL_NOTES, other, "VIOLATION: region_notes pair both null: ca_desert"}
# ca_desert did NOT graduate (absent from both) -> its null-notes violation stays.
assert drop_shell_build_unmasks(mixed, base, cand) == {other, "VIOLATION: region_notes pair both null: ca_desert"}

print("PASS precommit_release_verify shell-build allowance")

# --- pre-cert anchoring allowance ---
ANCH = "VIOLATION: anchoring: rootstock_options[0]: uf_ifas_hs1153 unanchored"
precert = {"verification_status": {"status": None}}          # lemon Steps 1-3 state
certified = {"verification_status": {"status": "verified_gs_arc"}}

# case 5: pre-cert crop gains an anchoring gap (sources authored, anchoring at Step 4+)
# -> accepted admission state, dropped from the blocking set.
assert drop_precert_anchoring({ANCH}, precert) == set(), "pre-cert anchoring gap must be forgiven"

# case 6: a CERTIFIED crop gains an anchoring gap -> real regression, still blocks.
assert drop_precert_anchoring({ANCH}, certified) == {ANCH}, "certified anchoring regression must NOT be forgiven"

# case 7: a non-anchoring new violation on a pre-cert crop is never forgiven by this filter.
assert drop_precert_anchoring({other}, precert) == {other}, "non-anchoring violations must never be forgiven here"

# case 8: mixed -- only the anchoring violation is dropped on a pre-cert crop.
assert drop_precert_anchoring({ANCH, other}, precert) == {other}, "only anchoring dropped, pre-cert"

print("PASS precommit_release_verify pre-cert anchoring allowance")

# --- no consumer coupling (PLA-713) ---------------------------------------------
# Consumers are pinned; a stale consumer export is the expected state and must never block a dataset
# commit. Behavioral, not textual: a real canonical commit is staged in a scratch repo while $HOME
# carries a plant-app whose export stamp names a DIFFERENT canonical -- exactly what the removed
# PLA-258 arm blocked on. The hook must let it through. The hook under test is HOOK_UNDER_TEST when
# set (the mutation harness points it at a scratch copy), else this tools/ dir's hook.
import json as _json, shutil as _shutil, subprocess as _sp, tempfile as _tempfile
import precommit_release_verify as _hook

_hook_path = os.environ.get("HOOK_UNDER_TEST") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "precommit_release_verify.py")
for _name in ("export_currency_concerns", "apply_export_waivers", "EXPORT_WAIVERS"):
    assert not hasattr(_hook, _name), f"the PLA-258 export arm is back: {_name}"

_tmp = _tempfile.mkdtemp()
try:
    _home = os.path.join(_tmp, "home")
    _app = os.path.join(_home, "plant-app")
    os.makedirs(os.path.join(_app, "assets", "data"))
    _json.dump({"canonical_sha256": "0" * 64, "artifacts": {}},
               open(os.path.join(_app, "assets", "data", "dataset-provenance.json"), "w"))
    _repo = os.path.join(_tmp, "repo")
    os.makedirs(_repo)
    def _g(*a):
        _sp.run(["git", "-C", _repo, *a], check=True, capture_output=True)
    _g("init", "-q"); _g("config", "user.email", "t@e.com"); _g("config", "user.name", "t")
    _canon = os.path.join(_repo, "crops_data_final.json")
    open(_canon, "w").write(_json.dumps({"crops": [], "source_catalog": {}}))
    _g("add", "crops_data_final.json"); _g("commit", "-qm", "base", "--no-verify")
    # a catalog admit: the canonical is staged, no crop changes, so no gate run is needed
    open(_canon, "w").write(_json.dumps({"crops": [], "source_catalog": {"new_src": {"name": "x"}}}))
    _g("add", "crops_data_final.json")
    _env = dict(os.environ, HOME=_home)
    _r = _sp.run([sys.executable, _hook_path], cwd=_repo, env=_env, capture_output=True, text=True)
    _out = _r.stdout + _r.stderr
    assert "ERRORED" not in _out, f"hook errored, so it failed OPEN and proves nothing: {_out}"
    assert "catalog admit" in _out, f"hook did not reach the canonical arm (vacuous): {_out}"
    assert _r.returncode == 0, f"a stale consumer export blocked a dataset commit (rc {_r.returncode}): {_out}"
    assert "plant-app" not in _out and "build:guides" not in _out, f"hook still talks about the app: {_out}"
finally:
    _shutil.rmtree(_tmp, ignore_errors=True)
print("PASS precommit_release_verify no consumer coupling (PLA-713)")
