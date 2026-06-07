#!/usr/bin/env python3
"""SHA-gated apply of build_region_shells to ONE crop, written to a scratch copy
with a collateral audit. Does NOT touch canonical -- promotion is a separate,
manual step after the gate verifies the scratch. Run from repo root:

    python3 tools/apply_region_shells.py <slug> [session] [date]

The SHA gate reads the expected start-SHA from LATEST.txt (the canonical pointer),
so this wrapper is reusable across every anchor without hand-editing a constant --
the cherry-pinned constant was a one-shot that could not run against any later base.
`session`/`date` stamp THIS crop's northern_tier promotion provenance; they default
to a slug-derived session + today, but pass them explicitly for the release record.
"""
import json, hashlib, copy, sys, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_region_shells import build_region_shells

PATH = "crops_data_final.json"
SCRATCH = "crops_data_final.scratch.json"


def latest_sha(path="LATEST.txt"):
    for line in open(path):
        if line.strip().startswith("SHA:"):
            return line.split(":", 1)[1].strip()
    sys.exit("LATEST.txt has no SHA: line -- cannot establish the start-SHA gate")


if len(sys.argv) < 2:
    sys.exit("usage: apply_region_shells.py <slug> [session] [date]")
SLUG = sys.argv[1]
SESSION = sys.argv[2] if len(sys.argv) > 2 else f"m16_{SLUG.split('-')[0]}_step3_5_region_shells"
DATE = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().isoformat()

EXPECTED_SHA = latest_sha()
raw = open(PATH, "rb").read()
actual = hashlib.sha256(raw).hexdigest()
if actual != EXPECTED_SHA:
    sys.exit(f"SHA mismatch: {actual} != {EXPECTED_SHA} (LATEST.txt) -- STOP, reconcile")

data = json.loads(raw)
before = copy.deepcopy(data)
crop = next(c for c in data["crops"] if c["slug"] == SLUG)
build_region_shells(crop, session=SESSION, date=DATE)

# collateral audit: every OTHER crop + every top-level key byte-identical (as objects)
assert set(before) == set(data), "top-level key set changed"
for k in before:
    if k != "crops":
        assert before[k] == data[k], f"top-level key changed: {k}"
changed = [b["slug"] for b, a in zip(before["crops"], data["crops"]) if b != a]
assert changed == [SLUG], f"collateral change -- expected only {SLUG!r}, got {changed}"

with open(SCRATCH, "w") as f:
    json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
print(f"scratch written: {SCRATCH} (only {SLUG} changed; session={SESSION} date={DATE})")
