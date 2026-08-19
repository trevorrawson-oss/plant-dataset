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

# --- export-currency arm (PLA-258) ---------------------------------------------
# The arm blocks a canonical commit whose downstream export was built from different
# bytes. Guarded here for the two ways it could go quietly wrong: firing on commits it
# has no business judging, and passing a stale export because it measured the wrong
# canonical.
import json as _json, shutil as _shutil, tempfile as _tempfile, hashlib as _hashlib
from precommit_release_verify import export_currency_concerns
import export_staleness_gate as _esg

_tmp = _tempfile.mkdtemp()

def _mk_app(root, stamped_sha):
    for rel in _esg.APP_ARTIFACTS:
        full = os.path.join(root, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(f"body-of-{rel}")
    m = {"canonical_sha256": stamped_sha, "artifacts":
         {r: _hashlib.sha256(f"body-of-{r}".encode()).hexdigest() for r in _esg.APP_ARTIFACTS}}
    p = os.path.join(root, _esg.APP_PROVENANCE)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    _json.dump(m, open(p, "w"))
    return root

# case 9: a commit that does NOT stage the canonical is none of this arm's business.
# (An arm that fires on doc-only commits gets bypassed by habit, and then never fires.)
assert export_currency_concerns(["docs/foo.md"], _mk_app(os.path.join(_tmp, "a1"), "x"*64)) == [], \
    "must not judge a commit that does not stage the canonical"

# case 10: canonical staged + export stamped with a DIFFERENT canonical -> blocks.
# The staged canonical is read from the git index, so this asserts against the real
# repo's staged/HEAD bytes rather than a synthetic hash.
_real = _esg.sha256_bytes(open(os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "crops_data_final.json"), "rb").read())
_stale = export_currency_concerns(["crops_data_final.json"],
                                  _mk_app(os.path.join(_tmp, "a2"), "0"*64))
assert _stale and any("E1" in c for c in _stale), \
    f"a stale stamp must block a canonical commit, got {_stale}"

# case 11: an absent plant-app SKIPS rather than blocks. This backstop must never make a
# dataset-only checkout uncommittable; the RELEASE gate is where unmeasured stays red.
assert export_currency_concerns(["crops_data_final.json"], os.path.join(_tmp, "nope")) == [], \
    "absent plant-app must fail open in the backstop"

_shutil.rmtree(_tmp, ignore_errors=True)
print("PASS precommit_release_verify export-currency arm")
