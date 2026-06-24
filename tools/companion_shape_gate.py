#!/usr/bin/env python3
"""Companion-shape cert-gate branch (Phase B, audit F4/F6, 2026-06-24). Imported + run by
whole_crop_gate.py. A no-op for any crop carrying no `companions` dict.

WHY: two render defects the audit found across the GS anchors --

  F4  BARE-STRING ENTRIES. A companion stored as a bare string ("marigolds") instead of
      the certified object {name, ...} is silently DROPPED by CompanionsCard.normCompanions
      (it spreads the string, finds no .name, filters it out) -- the row renders as NOTHING.
      Hit lemon, orange-navel, basil, green-beans-bush.

  F6  GOODS HIDDEN FROM SEASONED MODE. The card maps the buckets to registers:
        good_seasoned + good_beginner_seasoned -> rendered in SEASONED mode
        good_beginner                          -> rendered in BEGINNER mode only
      so companions placed ONLY in good_beginner / bad_beginner never appear for a seasoned
      reader. Hit apple (all its goods + bads in the beginner-only bucket).

This makes both un-shippable at scale: every entry must be a well-formed object with a name,
and a crop's goods/bads must be reachable from a seasoned-readable bucket. The per-entry `why`
copy is policed elsewhere (the dual-voice gate B flags a null `why_beginner` sibling); this gate
is the RENDERABILITY structure -- the entry exists, has a name, and lands where it will show.
"""

GOOD_BUCKETS = ("good_seasoned", "good_beginner_seasoned", "good_beginner")
BAD_BUCKETS = ("bad_seasoned", "bad_beginner_seasoned", "bad_beginner")
# The buckets the card renders in seasoned mode (good_beginner / bad_beginner are beginner-only).
SEASONED_READABLE_GOOD = ("good_seasoned", "good_beginner_seasoned")
SEASONED_READABLE_BAD = ("bad_seasoned", "bad_beginner_seasoned")


def _entries(companions, bucket):
    v = companions.get(bucket)
    return v if isinstance(v, list) else []


def _nonempty_name(entry):
    return isinstance(entry, dict) and isinstance(entry.get("name"), str) and bool(entry["name"].strip())


def companion_shape_violations(crop):
    """Return a list of violation strings ([] = clean). No-op when the crop has no
    companions dict (indoor microgreens carry none)."""
    companions = crop.get("companions")
    if not isinstance(companions, dict):
        return []
    V = []
    # 1+2. every entry in every bucket is a well-formed object with a non-empty name.
    for bucket in GOOD_BUCKETS + BAD_BUCKETS:
        for i, entry in enumerate(_entries(companions, bucket)):
            if not isinstance(entry, dict):
                V.append(f"companions.{bucket}[{i}]: bare {type(entry).__name__} {entry!r} -- "
                         f"must be the certified object shape {{name, ...}} (a bare string is "
                         f"silently dropped by the card)")
            elif not _nonempty_name(entry):
                V.append(f"companions.{bucket}[{i}]: object has no non-empty `name` "
                         f"(keys={sorted(entry)}) -- the card renders by `name`, so a legacy "
                         f"`plant`-keyed or nameless entry never shows")
    # 3. goods/bads must be reachable in seasoned mode (not beginner-only).
    def _has(buckets):
        return any(_entries(companions, b) for b in buckets)
    if _has(GOOD_BUCKETS) and not _has(SEASONED_READABLE_GOOD):
        V.append("companions: good entries exist only in the beginner-only bucket "
                 "(good_beginner) -- seasoned mode shows no good companions. Move them into "
                 "good_seasoned or good_beginner_seasoned.")
    if _has(BAD_BUCKETS) and not _has(SEASONED_READABLE_BAD):
        V.append("companions: bad entries exist only in the beginner-only bucket "
                 "(bad_beginner) -- seasoned mode shows no 'keep apart from' rows. Move them "
                 "into bad_seasoned or bad_beginner_seasoned.")
    return V


if __name__ == "__main__":
    import json, sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path))
    total = 0
    for c in data["crops"]:
        for v in companion_shape_violations(c):
            print(f"  {c.get('slug')}: {v}")
            total += 1
    print(f"companion_shape gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
