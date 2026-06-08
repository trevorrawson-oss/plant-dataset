#!/usr/bin/env python3
"""Author-fresh wipe: reset the 120 non-GS crops to honest authoring-ready shells.

Contract: docs/reset_to_shell_policy_v1_0.md. Keep identity/classification +
sources_summary (candidate pool); reset verification_status to the pre-arc shell;
blank every other per-crop CLAIM (dict keeps keys + recurse; list -> []; scalar -> null).
The 3 GS crops + all sibling top-level keys are untouched.

Tested by tools/test_reset_to_shell.py (TDD). Destructive -- run --apply only after
the dry-run audit is clean; base SHA is preserved in git for recovery.

Usage:
  python3 tools/reset_to_shell.py crops_data_final.json --out crops_data_final.scratch.json
  (add --apply to write; without --out it only audits and prints the footprint)
"""
import os, sys, json, copy, argparse, hashlib

KEEP_TOP = {"slug", "name", "botanical_name", "family", "category", "type",
            "archetype", "calendar_basis", "lifecycle", "perennial", "difficulty"}
KEEP_VERBATIM = {"sources_summary"}
PRE_ARC_VSTATUS = {"launch_ready_core": False, "launch_ready_seasoned": False,
                   "status": None, "last_audited": None}
GS_KEEP = {"cherry-tomato", "beefsteak-tomato", "lettuce-leaf"}


def blank_recursive(value):
    """dict -> keep keys, recurse; list -> []; scalar -> None."""
    if isinstance(value, dict):
        return {k: blank_recursive(v) for k, v in value.items()}
    if isinstance(value, list):
        return []
    return None


def reset_crop(crop):
    """Return a NEW shell dict for one crop per the policy (does not mutate input)."""
    out = {}
    for k, v in crop.items():
        if k in KEEP_TOP or k in KEEP_VERBATIM:
            out[k] = copy.deepcopy(v)
        elif k == "verification_status":
            out[k] = dict(PRE_ARC_VSTATUS)
        else:
            out[k] = blank_recursive(v)
    return out


def reset_dataset(data, gs_keep=GS_KEEP):
    """Reset every non-GS crop in place; return (data, stats)."""
    wiped = kept = 0
    for i, crop in enumerate(data.get("crops", [])):
        if crop.get("slug") in gs_keep:
            kept += 1
            continue
        data["crops"][i] = reset_crop(crop)
        wiped += 1
    return data, {"wiped": wiped, "kept_gs": kept, "total": wiped + kept}


def _leaves(value, path=""):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from _leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(value, list):
        for idx, v in enumerate(value):
            yield from _leaves(v, f"{path}[{idx}]")
    else:
        yield path, value


def assert_blanked(crop):
    """Safety invariant: every leaf NOT under an identity key / sources_summary /
    verification_status is None. Raises AssertionError on any surviving content."""
    skip = KEEP_TOP | KEEP_VERBATIM | {"verification_status"}
    for k, v in crop.items():
        if k in skip:
            continue
        for path, leaf in _leaves(v, k):
            assert leaf is None, f"content survived the wipe at {path!r} = {leaf!r}"


def _audit(pristine, reset, gs_keep):
    """Full pre/post audit; returns list of problems (empty == clean)."""
    problems = []
    # 2. sibling top-level keys byte-identical; crop count + slugs unchanged
    for k in pristine:
        if k == "crops":
            continue
        if json.dumps(pristine[k], sort_keys=True, ensure_ascii=False) != \
           json.dumps(reset[k], sort_keys=True, ensure_ascii=False):
            problems.append(f"sibling top-level key changed: {k}")
    p_slugs = [c.get("slug") for c in pristine["crops"]]
    r_slugs = [c.get("slug") for c in reset["crops"]]
    if p_slugs != r_slugs:
        problems.append("crop slug list/order changed")
    p_by = {c["slug"]: c for c in pristine["crops"]}
    for c in reset["crops"]:
        slug = c["slug"]
        pc = p_by[slug]
        if slug in gs_keep:
            # 1. GS crops byte-identical
            if json.dumps(pc, sort_keys=True, ensure_ascii=False) != \
               json.dumps(c, sort_keys=True, ensure_ascii=False):
                problems.append(f"GS crop mutated: {slug}")
            continue
        # 3. identity + sources_summary byte-identical; vstatus == shell
        for k in (KEEP_TOP | KEEP_VERBATIM):
            if k in pc and json.dumps(pc[k], sort_keys=True, ensure_ascii=False) != \
                          json.dumps(c.get(k), sort_keys=True, ensure_ascii=False):
                problems.append(f"{slug}: kept key {k} changed")
        if c.get("verification_status") != PRE_ARC_VSTATUS:
            problems.append(f"{slug}: verification_status not the pre-arc shell")
        # 4. safety invariant
        try:
            assert_blanked(c)
        except AssertionError as e:
            problems.append(f"{slug}: {e}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("--out")
    ap.add_argument("--apply", action="store_true",
                    help="write --out (otherwise audit-only/dry-run)")
    args = ap.parse_args()

    data = json.load(open(args.infile))
    pristine = copy.deepcopy(data)
    reset, stats = reset_dataset(data)
    problems = _audit(pristine, reset, GS_KEEP)

    print(f"crops: {stats['total']} | wiped: {stats['wiped']} | kept GS: {stats['kept_gs']}")
    if problems:
        print(f"AUDIT FAILED -- {len(problems)} problem(s):")
        for p in problems[:40]:
            print("  -", p)
        sys.exit(1)
    print("AUDIT CLEAN: GS + siblings byte-identical; identity/sources kept; "
          "verification_status reset; no content leaf survived.")
    if args.out and args.apply:
        # CANONICAL serialization: compact, no trailing newline (matches apply_patch.py)
        text = json.dumps(reset, separators=(",", ":"), ensure_ascii=False)
        open(args.out, "w").write(text)
        new_sha = hashlib.sha256(text.encode()).hexdigest()
        print(f"[written {args.out}] OUT_SHA={new_sha}")
    elif args.out:
        print("(dry-run; pass --apply to write --out)")


if __name__ == "__main__":
    main()
