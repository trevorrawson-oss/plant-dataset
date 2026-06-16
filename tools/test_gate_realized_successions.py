#!/usr/bin/env python3
"""Integration test: whole_crop_gate A8 validates successions_realized coherence.

Builds a back-filled (coherent) carrot fixture, then injects each failure mode and
runs the gate as a subprocess, checking the specific violation string. Mirrors
test_gate_second_planting.py. Run from repo root:
  python3 tools/test_gate_realized_successions.py
"""
import json, copy, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from derive_realized_successions import backfill_crop

base = json.load(open("crops_data_final.json"))
# back-fill ALL in-scope succession crops so the fixture is internally coherent
for c in base["crops"]:
    backfill_crop(c)


def run_gate(slug, mutate=None):
    d = copy.deepcopy(base)
    if mutate:
        mutate(next(x for x in d["crops"] if x["slug"] == slug))
    tmp = os.path.join(HERE, "_tmp_succ_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
                           capture_output=True, text=True)
    finally:
        os.remove(tmp)
    return r.stdout, r.returncode


# coherent back-filled carrot -> no A8 violation, whole gate PASS (additive, cert intact)
out, rc = run_gate("carrot")
assert "successions_realized" not in out or "VIOLATION" not in out.split("A8")[1].split("\n")[0], out
assert "GATE: PASS" in out, f"coherent carrot should pass the whole gate:\n{out}"
print("PASS coherent carrot -> gate clean")

# stale value -> 'stale' violation
def corrupt_value(c):
    c["regions"]["northern_tier"]["resolved_by_zone"]["3"]["successions_realized"] = 99
out, rc = run_gate("carrot", corrupt_value)
assert "successions_realized stale" in out, f"expected stale violation:\n{out}"
assert rc == 1
print("PASS stale value -> flagged")

# missing field -> 'missing' violation
def drop_value(c):
    del c["regions"]["se_gulf"]["resolved_by_zone"]["8"]["successions_realized"]
out, rc = run_gate("carrot", drop_value)
assert "successions_realized missing" in out, f"expected missing violation:\n{out}"
print("PASS missing field -> flagged")

# crop-level cap not equal to max(realized) -> reconciliation violation
def break_reconcile(c):
    c["succession_policy"]["successions"] = 3
out, rc = run_gate("carrot", break_reconcile)
assert "succession_policy.successions" in out and "!= max(realized)" in out, f"expected reconcile violation:\n{out}"
print("PASS broken reconciliation -> flagged")

# out-of-scope crop (cherry, suitable=False, second_planting) carrying the field -> violation
def inject_into_cherry(c):
    c["regions"]["northern_tier"]["resolved_by_zone"]["6"]["successions_realized"] = 5
out, rc = run_gate("cherry-tomato", inject_into_cherry)
assert "successions_realized on out-of-scope crop" in out, f"expected out-of-scope violation:\n{out}"
print("PASS out-of-scope field -> flagged")

print("\nALL PASS test_gate_realized_successions")
