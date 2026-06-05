#!/usr/bin/env python3
"""SHA-gated apply of build_region_shells to ONE crop, written to a scratch copy
with a collateral audit. Does NOT touch canonical -- promotion is a separate,
manual step after the gate verifies the scratch. Run from repo root:
    python3 tools/apply_region_shells.py [slug]
"""
import json, hashlib, copy, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_region_shells import build_region_shells

EXPECTED_SHA = "29b3aaa904a62487960c5dc53b4282538454076f696ffec039ac4ab87937801a"
PATH = "crops_data_final.json"
SCRATCH = "crops_data_final.scratch.json"
SLUG = sys.argv[1] if len(sys.argv) > 1 else "cherry-tomato"

raw = open(PATH, "rb").read()
actual = hashlib.sha256(raw).hexdigest()
if actual != EXPECTED_SHA:
    sys.exit(f"SHA mismatch: {actual} != {EXPECTED_SHA} -- STOP, reconcile against LATEST.txt")

data = json.loads(raw)
before = copy.deepcopy(data)
crop = next(c for c in data["crops"] if c["slug"] == SLUG)
build_region_shells(crop)

# collateral audit: every OTHER crop byte-identical (compared as parsed objects)
assert set(before) == set(data), "top-level key set changed"
for k in before:
    if k != "crops":
        assert before[k] == data[k], f"top-level key changed: {k}"
changed = [b["slug"] for b, a in zip(before["crops"], data["crops"]) if b != a]
assert changed == [SLUG], f"collateral change -- expected only {SLUG!r}, got {changed}"

with open(SCRATCH, "w") as f:
    json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
print(f"scratch written: {SCRATCH} (only {SLUG} changed)")
