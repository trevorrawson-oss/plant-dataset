#!/usr/bin/env python3
"""Register-FILL cert gate: every ruled `_seasoned`/`_beginner` register field must be
AUTHORED (not null/empty) before a crop flips.

This is the systemic fix for the gap that let apple ship 30 null register fields and
CERTIFIED peach ship 46: the always-on whole_crop_gate TOLERATES null register prose
(`null_values: 0` does not catch an unauthored `_seasoned`/`_beginner` field). This gate
catches them. It is the FILL half; `register_completeness_gate.py` is the RULED half.

Deliberately a STANDALONE cert/Step-11 gate (NOT wired into the always-on whole_crop_gate),
so an in-progress crop -- or a certified crop still awaiting a backfill (peach 6-8C) -- is
not red-flagged in the routine gate record. Run it at the flip, and on-demand to derive a
6-8 worklist or audit a certified crop.

Allowlist (legitimately null, never a violation):
  - `frost_risk_note_*`  -- seasoned-only, authored per-cell only where late frost is a risk.
  - the legacy `zones{}` layer -- deprecated (regions{} is the live layer).
Empty arrays (e.g. the companions array-split awaiting its reshape session) are not strings,
so are never counted. An N/A field is AUTHORED as N/A prose ("Not applicable. ..."), never
left null -- so a null "reason"/"hardening_off" IS a violation (author the N/A).

Run: python3 tools/register_fill_gate.py <crop-slug> [crops_data_final.json]
Exit 1 on any violation.
"""
import json
import sys


def _allowlisted(path):
    # frost_risk_note (optional per-cell) + legacy zones{} layer
    leaf = path.rsplit("/", 1)[-1]
    if leaf.startswith("frost_risk_note"):
        return True
    if "/zones/" in path or path.startswith("zones/"):
        return True
    return False


def register_fill_violations(crop):
    """Return null/empty `_seasoned`/`_beginner` register fields that must be authored
    before this crop flips ([] = complete). Allowlisted paths are excluded.

    Structured N/A: a dict carrying `applicable: false` IS the authored N/A form, so its
    null `_seasoned`/`_beginner` children are not violations (the overwintering N/A on
    cherry/beefsteak/carrot). `applicable: null` (undecided) or `applicable: true` does
    NOT excuse them -- a null child still violates (decide + author, or set false)."""
    V = []

    def walk(o, path, na):
        if isinstance(o, dict):
            # entering an {applicable: false} subtree marks its register children as N/A.
            child_na = na or (o.get("applicable") is False)
            for k, v in o.items():
                walk(v, path + "/" + k, child_na)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, "%s/%d" % (path, i), na)
        elif isinstance(o, str) or o is None:
            if path.endswith(("_seasoned", "_beginner")) and (o is None or o == ""):
                if not na and not _allowlisted(path):
                    V.append(path.lstrip("/"))

    walk(crop, "", False)
    return V


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    slug = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    crop = next((c for c in data.get("crops", []) if c.get("slug") == slug), None)
    if crop is None:
        print("register-fill gate: crop %r not found in %s" % (slug, path))
        sys.exit(2)
    viol = register_fill_violations(crop)
    print("register-fill cert gate -- unauthored register fields for %r:" % slug)
    for p in viol:
        print("  NULL  " + p)
    if viol:
        print("\nGATE: %d unauthored register field(s). Author them (an N/A field = N/A prose,"
              " not null) before the flip." % len(viol))
        sys.exit(1)
    print("\nGATE: PASS -- every ruled register field is authored (modulo the frost_risk_note /"
          " legacy-zones allowlist). Flip-eligible on this dimension.")
    sys.exit(0)
