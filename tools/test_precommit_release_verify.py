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
from precommit_release_verify import drop_shell_build_unmasks

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
