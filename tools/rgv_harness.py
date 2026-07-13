#!/usr/bin/env python3
"""Off-canonical per-crop gate harness for the RGV (Rio Grande Valley) region column.

Runs the REAL whole_crop_gate.py on a single crop whose rgv cell is staged, against a
SCRATCH canonical (real canonical + the crop's staged rgv cell merged) + a SCRATCH copy
of tools/ that has rgv patched into zone_span_gate.EXPECTED_SPANS. The real canonical
and the real tools/ are never touched -- this lets Tasks 4-7 gate ONE crop's authored
rgv cell in isolation, long before rgv is a real region (that only happens at the
atomic promote, Task 8+).

Success signal (empirically confirmed, not assumed -- see docs/superpowers/sdd/
task-2-report.md): whole_crop_gate.py does `sys.exit(1)` iff its `violations` list is
non-empty and otherwise falls off the end of main (implicit exit 0), printing
"GATE: PASS ..." only in the exit-0 case and "GATE: N VIOLATION(S)" whenever it
exits 1. The exit code is the sole authoritative signal; the printed verdict line is
redundant with it (never disagrees), so the predicate is just `returncode == 0` --
no string-splitting on "PASS"/"FAIL" needed (those substrings can appear inside
per-gate diagnostic lines regardless of the final verdict, which is what makes
string-splitting fragile).

Usage as a library: rgv_harness.gate_crop(slug, staged_cells) -> (passed, output).
Usage as a smoke script: python3 tools/rgv_harness.py <staging.json> <slug>
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")
RGV_SPAN = ["9", "10"]


def build_scratch_tools(dest):
    """Copy tools/*.py to dest, patching zone_span_gate.EXPECTED_SPANS to include rgv.
    Every other gate (A31 region roster, A45 zone_span parity) derives its region/zone
    universe from EXPECTED_SPANS, so this one patch is sufficient to make the whole
    suite rgv-aware without touching the real tools/ directory."""
    os.makedirs(dest, exist_ok=True)
    for fn in os.listdir(HERE):
        if fn.endswith(".py"):
            shutil.copy(os.path.join(HERE, fn), os.path.join(dest, fn))
    zsg = os.path.join(dest, "zone_span_gate.py")
    src = open(zsg, encoding="utf-8").read()
    # insert rgv into the EXPECTED_SPANS dict literal (first line after the opening brace)
    patched, n = re.subn(r"(EXPECTED_SPANS = \{\n)",
                         r'\1    "rgv":            ["9", "10"],\n', src, count=1)
    assert n == 1, "could not patch EXPECTED_SPANS"
    open(zsg, "w", encoding="utf-8").write(patched)
    return dest


def scratch_canonical(staged_cells, path):
    """Write the real CANON + each staged rgv cell merged into its crop's regions, to
    `path`, COMPACT (matching the format whole_crop_gate and its sub-gates expect)."""
    data = json.load(open(CANON, encoding="utf-8"))
    by = {c["slug"]: c for c in data["crops"]}
    for slug, cell in staged_cells.items():
        by[slug].setdefault("regions", {})["rgv"] = cell
    # Splice the rgv chill band + provenance (a top-level promote-time addition). A3's perennial
    # no-fruit split reads region_chill_delivered["rgv"][zone] for a survives_no_fruit tree cell;
    # without it A3 flags "no delivered band -- cannot apply the no-fruit split". Injecting it here
    # (from the Task-3 staging file, keyed by dotted json path) makes the scratch canonical faithful
    # to the post-promote state so chill-gated trees gate correctly. No-op for annual cells.
    band_path = os.path.join(HERE, "staging", "rgv_chill_band.json")
    if os.path.exists(band_path):
        for k, v in json.load(open(band_path, encoding="utf-8")).items():
            parts = k.split(".")
            if len(parts) == 2:
                data.setdefault(parts[0], {})[parts[1]] = v
            else:
                data[parts[0]] = v
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    return path


def gate_crop(slug, staged_cells):
    """Return (passed, output) from running the real whole_crop_gate.py on `slug` in a
    scratch env (scratch tools/ + scratch canonical), then discarded. `staged_cells` is
    `{slug: rgv_cell_dict}` -- crops not in it get no rgv cell (so a crop with no staged
    cell yet legitimately fails A31, the region-roster floor)."""
    with tempfile.TemporaryDirectory() as tmp:
        tools = build_scratch_tools(os.path.join(tmp, "tools"))
        canon = scratch_canonical(staged_cells, os.path.join(tmp, "canon.json"))
        r = subprocess.run([sys.executable, os.path.join(tools, "whole_crop_gate.py"), slug, canon],
                           capture_output=True, text=True)
        return r.returncode == 0, r.stdout + r.stderr


if __name__ == "__main__":
    # smoke: gate one crop from a staging file: rgv_harness.py <staging.json> <slug>
    staged = json.load(open(sys.argv[1], encoding="utf-8"))
    ok, out = gate_crop(sys.argv[2], {sys.argv[2]: staged[sys.argv[2]]})
    print(out)
    sys.exit(0 if ok else 1)
