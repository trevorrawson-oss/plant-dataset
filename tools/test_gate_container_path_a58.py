#!/usr/bin/env python3
"""Integration test: whole_crop_gate A58 (container_path) fires on a scratch fixture and is a
no-op on today's canonical. Run: python3 tools/test_gate_container_path_a58.py"""
import copy, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json")))


def gate(slug, mutate):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == slug)
    mutate(c)
    tmp = os.path.join(HERE, "_tmp_a58_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        return subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
                              capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)


# The block is present and announced.
out = gate("cherry-tomato", lambda c: None)
assert "A58. container_path coherence" in out, "A58 block missing from whole_crop_gate"
# No key on live canonical: A58 is a no-op, the gate is still PASS for a passing crop.
assert "container-path:" not in out, out
# A rule-1 defect on a scratch copy bounces.
out = gate("cherry-tomato", lambda c: c["container_notes"].__setitem__("container_path", None))
assert "container-path:" in out and "rule 1" in out, out
# An unknown value bounces.
out = gate("cherry-tomato", lambda c: c["container_notes"].__setitem__("container_path", "dwarf_rootstock"))
assert "container-path:" in out and "not in" in out, out
# A good value on a good crop is clean.
out = gate("cherry-tomato", lambda c: c["container_notes"].__setitem__("container_path", "direct"))
assert "container-path:" not in out, out
# Presence is NOT armed yet: a certified crop without the key is not flagged.
src = open(os.path.join(HERE, "whole_crop_gate.py")).read()
assert "A58_PRESENCE_ARMED = False" in src, "presence floor must stay unarmed until the canonical carries the key (Task 8)"
print("PASS gate A58 container_path")
