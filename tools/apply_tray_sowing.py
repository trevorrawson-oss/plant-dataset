#!/usr/bin/env python3
"""apply_tray_sowing.py -- reusable splicer for register #9 (tray_sowing + pot_up).

Reads a BATCH file: a JSON object { "<slug>": {"tray_sowing": <enum>, "pot_up": <enum>?}, ... }.
  - tray_sowing is REQUIRED per entry.
  - pot_up (enum {recommended,optional,not_needed}) is REQUIRED iff tray_sowing is a real tray value
    (multi_sow_thin_to_one/single_sow/multisow_clump); it MUST be OMITTED when tray_sowing == 'na'.

Guards (all HARD -- abort on any breach, canonical left untouched):
  - each slug must exist and NOT already carry tray_sowing (never overwrite an authored crop).
  - the resulting crop must PASS seed_tray_gate.check_crop (enum + na<->seedling_light coherence +
    pot_up present-iff-real-value) BEFORE it is written -- a bad batch never reaches disk.
  - crop count stays 124; output is COMPACT (separators=(',',':'), ensure_ascii=False, no trailing
    newline); EXACTLY the batch slugs change (per-crop byte diff), every other crop byte-identical.

Usage:
  apply_tray_sowing.py BATCH.json [--path crops_data_final.json] [--dry-run]
See docs/seed_tray_protocol_contract.md.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed_tray_gate import check_crop, POT_UP, REAL_TRAY, TRAY_SOWING


def compact(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def slug_of(c):
    return c.get("slug") or c.get("id")


def main():
    args = list(sys.argv[1:])
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    path = "crops_data_final.json"
    if "--path" in args:
        i = args.index("--path")
        path = args[i + 1]
        del args[i:i + 2]
    if not args:
        sys.exit("usage: apply_tray_sowing.py BATCH.json [--path P] [--dry-run]")
    batch = json.load(open(args[0], encoding="utf-8"))

    raw = open(path, encoding="utf-8").read()
    data = json.loads(raw)
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data
    by = {slug_of(c): c for c in crops}
    n_before = len(crops)
    pre = {slug_of(c): compact(c) for c in crops}

    intended = set(batch)
    for s, spec in batch.items():
        if s not in by:
            sys.exit(f"ABORT: unknown slug {s!r}")
        c = by[s]
        if "tray_sowing" in c:
            sys.exit(f"ABORT: {s} already carries tray_sowing (never overwrite)")
        ts = spec.get("tray_sowing")
        if ts not in TRAY_SOWING:
            sys.exit(f"ABORT: {s} tray_sowing {ts!r} not in {sorted(TRAY_SOWING)}")
        has_pu = "pot_up" in spec
        if ts in REAL_TRAY and not has_pu:
            sys.exit(f"ABORT: {s} real tray value {ts!r} requires pot_up in the batch")
        if ts == "na" and has_pu:
            sys.exit(f"ABORT: {s} tray_sowing 'na' must OMIT pot_up in the batch")
        c["tray_sowing"] = ts
        if has_pu:
            if spec["pot_up"] not in POT_UP:
                sys.exit(f"ABORT: {s} pot_up {spec['pot_up']!r} not in {sorted(POT_UP)}")
            c["pot_up"] = spec["pot_up"]
        # coherence pre-check on the finished crop -- a bad shape never reaches disk
        viol = check_crop(c)
        if viol:
            sys.exit("ABORT: gate would fail after splice:\n  " + "\n  ".join(viol))

    if len(crops) != n_before:
        sys.exit(f"ABORT: crop count changed {n_before} -> {len(crops)}")

    post = {slug_of(c): compact(c) for c in crops}
    changed = {s for s in post if post[s] != pre.get(s)}
    if changed != intended:
        sys.exit(f"ABORT: changed set {sorted(changed)} != intended {sorted(intended)}")

    out = compact(data)
    if dry:
        print(f"DRY-RUN ok: would change EXACTLY {len(intended)} crops: {sorted(intended)}")
        print(f"  count {n_before} -> {len(crops)}; bytes {len(raw)} -> {len(out)}")
        return
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(out)  # COMPACT, no trailing newline
    print(f"WROTE {path}: {len(intended)} crops spliced: {sorted(intended)}")
    print(f"  count {n_before} -> {len(crops)}; bytes {len(raw)} -> {len(out)}")


if __name__ == "__main__":
    main()
