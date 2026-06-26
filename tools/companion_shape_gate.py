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


# Which buckets render in which register (the card's bucket->mode map). A both-bucket
# (*_beginner_seasoned) entry renders in BOTH, so it needs BOTH whys.
SEASONED_RENDER_BUCKETS = ("good_seasoned", "good_beginner_seasoned",
                           "bad_seasoned", "bad_beginner_seasoned")
BEGINNER_RENDER_BUCKETS = ("good_beginner", "good_beginner_seasoned",
                           "bad_beginner", "bad_beginner_seasoned")


def companion_why_fill_violations(crop):
    """Return a list of bare-name render gaps ([] = clean). A companion that RENDERS in a
    register must carry that register's `why`: a seasoned-readable entry needs `why_seasoned`,
    a beginner-readable entry needs `why_beginner`, a both-bucket (*_beginner_seasoned) entry
    needs both. Otherwise the card shows the companion name with no reason. Skips non-dict /
    nameless entries (the shape gate owns those). No-op when the crop has no companions dict.

    This does NOT enforce reachability -- a beginner-only companion is legitimate curation
    (Trevor 2026-06-25); it only must carry its register's `why`. Separate from the wired
    `companion_shape_violations` (so the existing A19 stays green); wired after the why
    back-fill lands."""
    companions = crop.get("companions")
    if not isinstance(companions, dict):
        return []
    V = []

    def _missing(entry, key):
        v = entry.get(key)
        return not (isinstance(v, str) and v.strip())

    for bucket in GOOD_BUCKETS + BAD_BUCKETS:
        for i, entry in enumerate(_entries(companions, bucket)):
            if not _nonempty_name(entry):
                continue  # shape gate (A19) owns bare-string / nameless entries
            if bucket in SEASONED_RENDER_BUCKETS and _missing(entry, "why_seasoned"):
                V.append(f"companions.{bucket}[{i}] ({entry['name']!r}): renders in seasoned "
                         f"mode but why_seasoned is null/empty (bare-name companion)")
            if bucket in BEGINNER_RENDER_BUCKETS and _missing(entry, "why_beginner"):
                V.append(f"companions.{bucket}[{i}] ({entry['name']!r}): renders in beginner "
                         f"mode but why_beginner is null/empty (bare-name companion)")
    return V


# Ruled evidence vocab (register_bearing_field_inventory v1_0 §ENUM: evidence_label +
# confidence are categorical). `disputed` is valid at the label level for honesty even
# though only provenance.label carries it today.
EVIDENCE_LABELS = {"traditional", "extension_backed", "research_backed",
                   "likely", "mechanistic", "disputed"}
EVIDENCE_CONFIDENCE = {"low", "medium", "high"}


def companion_evidence_violations(crop):
    """Return a list of companions lacking honest evidence ([] = clean). Decision (a),
    Trevor 2026-06-25: every companion (good OR bad) must declare an `evidence_label` in
    the ruled enum AND a `confidence` in {low,medium,high}. A speculative-but-LABELED
    pairing (e.g. mechanistic/low) is allowed -- the bar is transparency, not only T1 --
    so beginners keep folk-wisdom companions while a seasoned reader can see the evidence
    weight. Skips non-dict / nameless entries (the shape gate A19 owns those). No-op when
    the crop has no companions dict. Separate from the wired `companion_shape_violations`;
    wired after the evidence-label back-fill lands."""
    companions = crop.get("companions")
    if not isinstance(companions, dict):
        return []
    V = []
    for bucket in GOOD_BUCKETS + BAD_BUCKETS:
        for i, entry in enumerate(_entries(companions, bucket)):
            if not _nonempty_name(entry):
                continue  # shape gate (A19) owns bare-string / nameless entries
            label = entry.get("evidence_label")
            if label not in EVIDENCE_LABELS:
                V.append(f"companions.{bucket}[{i}] ({entry['name']!r}): evidence_label "
                         f"{label!r} not in {sorted(EVIDENCE_LABELS)} (every companion must "
                         f"declare its evidence honestly)")
            conf = entry.get("confidence")
            if conf not in EVIDENCE_CONFIDENCE:
                V.append(f"companions.{bucket}[{i}] ({entry['name']!r}): confidence {conf!r} "
                         f"not in {sorted(EVIDENCE_CONFIDENCE)}")
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
