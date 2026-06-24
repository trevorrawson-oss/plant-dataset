#!/usr/bin/env python3
"""migrate_npk_ratio.py -- one-time deterministic NPK pill migration (Phase A, audit F3).

Adds a render-ready `fertilizer.npk_ratio` to every crop carrying an npk_hint:
  - RATIO crops: the FIRST N-P-K pattern (\\d+-\\d+-\\d+) lifted verbatim from the
    already-source-verified `npk_hint_seasoned` (fallback `npk_hint_beginner`).
    "high K, e.g. 5-10-10 or 8-32-16" -> "5-10-10". Deterministic; no new authoring.
  - RATIO-LESS crops (citrus / allium / lavender / blueberry): explicit `npk_ratio:
    null` + a short qualitative `npk_tag` the pill degrades to. These 4 are enumerated
    (their hints carry no single ratio by design); the tag compresses the verified hint.
Indoor microgreens (no npk_hint) is untouched. Strictly additive; idempotent.

Run: python3 tools/migrate_npk_ratio.py [crops_data_final.json]
Canonical write: json.dumps(separators=(",",":"), ensure_ascii=False), no trailing newline.
"""
import json, re, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
RATIO_RE = re.compile(r"\d{1,3}-\d{1,3}-\d{1,3}")

# The crops whose feeding guidance is genuinely ratio-less (audit F3). The tag is a
# terse, source-faithful compression of the verified npk_hint -- a USER-FACING-
# CATEGORICAL label (single form, read by both registers), NOT new persuasive copy.
RATIOLESS_TAGS = {
    "lemon": "Nitrogen-forward",
    "onion": "Nitrogen-forward early",
    "lavender": "Lean soil, minimal feed",
    "blueberry": "Acid-forming, ammonium N",
}


def insert_after(d, anchor_key, new_pairs):
    """Return a new dict with new_pairs inserted immediately after anchor_key (or
    appended if anchor_key is absent). Skips keys already present (idempotent)."""
    out = {}
    inserted = False
    for k, v in d.items():
        if k in new_pairs:
            continue  # drop any stale copy so we re-place it in the canonical spot
        out[k] = v
        if k == anchor_key:
            for nk, nv in new_pairs.items():
                out[nk] = nv
            inserted = True
    if not inserted:
        for nk, nv in new_pairs.items():
            out[nk] = nv
    return out


def migrate():
    data = json.load(open(PATH, encoding="utf-8"))
    touched, skipped_no_hint = [], []
    for c in data["crops"]:
        fert = c.get("fertilizer")
        if not isinstance(fert, dict):
            continue
        hint_s = fert.get("npk_hint_seasoned")
        hint_b = fert.get("npk_hint_beginner")
        if not (hint_s or hint_b):
            skipped_no_hint.append(c["slug"])
            continue
        slug = c["slug"]
        if slug in RATIOLESS_TAGS:
            pairs = {"npk_ratio": None, "npk_tag": RATIOLESS_TAGS[slug]}
            shown = f"null + tag={RATIOLESS_TAGS[slug]!r}"
        else:
            m = RATIO_RE.search(hint_s or "") or RATIO_RE.search(hint_b or "")
            if not m:
                sys.exit(f"ERROR {slug}: npk_hint present but no parseable ratio and not "
                         f"in the ratio-less roster -- add it to RATIOLESS_TAGS with a tag.\n"
                         f"  hint: {hint_s or hint_b!r}")
            pairs = {"npk_ratio": m.group(0)}
            shown = m.group(0)
        anchor = "npk_hint_seasoned" if "npk_hint_seasoned" in fert else "npk_hint_beginner"
        c["fertilizer"] = insert_after(fert, anchor, pairs)
        touched.append((slug, shown))

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False))

    print("migrate_npk_ratio -- touched %d crop(s):" % len(touched))
    for slug, shown in sorted(touched):
        print("  %-18s npk_ratio = %s" % (slug, shown))
    print("skipped (no npk_hint surface): %d -- %s" % (
        len(skipped_no_hint),
        ", ".join(sorted(skipped_no_hint)[:6]) + (" ..." if len(skipped_no_hint) > 6 else "")))


if __name__ == "__main__":
    migrate()
