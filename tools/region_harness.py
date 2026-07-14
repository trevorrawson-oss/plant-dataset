#!/usr/bin/env python3
"""Region-GENERIC off-canonical per-crop gate harness.

Runs the REAL whole_crop_gate.py on a single crop whose region cell is staged, against a
SCRATCH canonical (real canonical + the crop's staged region cell merged) + a SCRATCH copy
of tools/ that has <region_id> patched into zone_span_gate.EXPECTED_SPANS. The real canonical
and the real tools/ are never touched -- this lets each region arc's per-crop authoring tasks
gate ONE crop's authored cell in isolation, long before the region is real (that only happens
at the atomic promote). Generalized from rgv_harness.py (region_id + span are now parameters
instead of RGV-hardcoded constants); rgv_harness.py itself is left byte-untouched.

Success signal (empirically confirmed against a real crop -- see docs/superpowers/sdd/
task-2-report.md -- and matching rgv_harness.py's own confirmed finding): whole_crop_gate.py
does `sys.exit(1)` iff its `violations` list is non-empty and otherwise falls off the end of
main (implicit exit 0), printing "GATE: PASS ..." only in the exit-0 case and
"GATE: N VIOLATION(S)" whenever it exits 1. The exit code is the sole authoritative signal;
the printed verdict line is redundant with it (never disagrees), so the predicate is just
`returncode == 0` -- no string-splitting on "PASS"/"FAIL" needed (those substrings can appear
inside per-gate diagnostic lines regardless of the final verdict, which is what makes
string-splitting fragile).

Usage as a library: region_harness.gate_crop(region_id, span, slug, staged_cells) -> (passed, output).
Usage as a smoke script: python3 tools/region_harness.py <region_id> <z1,z2> <staging.json> <slug>
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


def build_scratch_tools(dest, region_id, span):
    """Copy tools/*.py to dest, patching zone_span_gate.EXPECTED_SPANS to include region_id.
    Every other gate (A31 region roster, A45 zone_span parity) derives its region/zone
    universe from EXPECTED_SPANS, so this one patch is sufficient to make the whole suite
    region-aware without touching the real tools/ directory."""
    os.makedirs(dest, exist_ok=True)
    for fn in os.listdir(HERE):
        if fn.endswith(".py"):
            shutil.copy(os.path.join(HERE, fn), os.path.join(dest, fn))
    zsg = os.path.join(dest, "zone_span_gate.py")
    src = open(zsg, encoding="utf-8").read()
    # insert region_id into the EXPECTED_SPANS dict literal (first line after the opening
    # brace). Built from `span` (not a re-typed literal) so the patch and the caller's span
    # can never diverge.
    span_literal = json.dumps(list(span))
    patched, n = re.subn(r"(EXPECTED_SPANS = \{\n)",
                         rf'\1    "{region_id}": ' + span_literal + ',\n', src, count=1)
    assert n == 1, "could not patch EXPECTED_SPANS"
    open(zsg, "w", encoding="utf-8").write(patched)
    return dest


def scratch_canonical(region_id, staged_cells, path):
    """Write the real CANON + each staged region cell merged into its crop's regions, to
    `path`, COMPACT (matching the format whole_crop_gate and its sub-gates expect)."""
    data = json.load(open(CANON, encoding="utf-8"))
    by = {c["slug"]: c for c in data["crops"]}
    for slug, cell in staged_cells.items():
        by[slug].setdefault("regions", {})[region_id] = cell
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    return path


def gate_crop(region_id, span, slug, staged_cells):
    """Return (passed, output) from running the real whole_crop_gate.py on `slug` in a
    scratch env (scratch tools/ + scratch canonical), then discarded. `staged_cells` is
    `{slug: region_cell_dict}` -- crops not in it get no region cell (so a crop with no
    staged cell yet legitimately fails A31, the region-roster floor)."""
    with tempfile.TemporaryDirectory() as tmp:
        tools = build_scratch_tools(os.path.join(tmp, "tools"), region_id, span)
        canon = scratch_canonical(region_id, staged_cells, os.path.join(tmp, "canon.json"))
        try:
            r = subprocess.run([sys.executable, os.path.join(tools, "whole_crop_gate.py"), slug, canon],
                               capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired as e:
            return False, (f"whole_crop_gate.py timed out after 120s for {slug!r} -- "
                            f"partial output: {(e.stdout or b'')!r}{(e.stderr or b'')!r}")
        return r.returncode == 0, r.stdout + r.stderr


if __name__ == "__main__":
    # smoke: region_harness.py <region_id> <z1,z2> <staging.json> <slug>
    rid, span = sys.argv[1], sys.argv[2].split(",")
    staged = json.load(open(sys.argv[3], encoding="utf-8"))
    slug = sys.argv[4]
    ok, out = gate_crop(rid, span, slug, {slug: staged[slug]})
    print(out)
    sys.exit(0 if ok else 1)
