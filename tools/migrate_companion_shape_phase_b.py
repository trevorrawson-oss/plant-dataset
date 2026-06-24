#!/usr/bin/env python3
"""Phase B companion-shape conversion (audit F4/F6, 2026-06-24).

The STRUCTURAL half of the F4/F6 fix (Claude Code lane). Converts the bare-string and
beginner-only-bucket companions on the 5 offenders to the certified object shape so the
companion_shape_gate (A19) goes green; the per-entry `why` COPY for the newly-objectified
entries is the claude.ai authoring lane (handoff). Apple keeps its already-authored `why`.

Idempotent: re-running is a no-op (every entry already an object in a seasoned-readable bucket).

Per crop:
  green-beans-bush -- EMPTY the redundant legacy good_beginner/bad_beginner (pure dups of the
                      object *_beginner_seasoned buckets). Pure dedup, no copy.
  apple            -- MOVE good_beginner/bad_beginner -> *_beginner_seasoned (the seasoned-
                      readable both-mode bucket, fixes F6); rename plant->name, why->why_seasoned
                      (a register-neutral string renders in BOTH modes via RegisterText's
                      fallback; why_beginner would blank seasoned mode). Existing copy preserved.
  lemon            -- objectify the bare-string bad_* buckets to {name}; EMPTY the bad_beginner
                      dup of bad_beginner_seasoned. why -> claude.ai.
  orange-navel     -- objectify the bare-string good_*/bad_* buckets in place (register
                      placement preserved). why -> claude.ai.
  basil            -- objectify; MOVE the bucket-inverted good_beginner (tomatoes/peppers, the
                      strongest pairing) + bad_beginner (fennel) into the both-mode *_beginner_
                      seasoned bucket so seasoned readers see them (the basil F6). why -> claude.ai.

Canonical write: json.dumps(separators=(",",":"), ensure_ascii=False), no trailing newline.
"""
import json
import os
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"


def cap(s):
    s = s.strip()
    return s if not s else (s[0].upper() + s[1:])


def to_obj(x):
    """Bare string -> {name}. An already-shaped object passes through unchanged (idempotent)."""
    if isinstance(x, str):
        return {"name": cap(x)}
    return x


def objectify(bucket):
    return [to_obj(x) for x in (bucket or [])]


def dedup_names(beginner_only, both_bucket):
    """Drop entries from a legacy *_beginner list whose name already appears (objectified) in the
    *_beginner_seasoned both-mode list -- they are pure render duplicates."""
    both_names = {(_name(e)).lower() for e in objectify(both_bucket)}
    return [e for e in objectify(beginner_only) if _name(e).lower() not in both_names]


def _name(e):
    return e.get("name", "") if isinstance(e, dict) else cap(e)


def main():
    data = json.load(open(PATH, encoding="utf-8"))
    crops = {c.get("slug"): c for c in data["crops"]}

    # ---- green-beans-bush: empty the redundant legacy beginner-only buckets ----
    co = crops["green-beans-bush"]["companions"]
    co["good_beginner"] = dedup_names(co.get("good_beginner"), co.get("good_beginner_seasoned"))
    co["bad_beginner"] = dedup_names(co.get("bad_beginner"), co.get("bad_beginner_seasoned"))

    # ---- apple: move beginner-only -> both-mode bucket; plant->name, why->why_seasoned ----
    co = crops["apple"]["companions"]

    def apple_reshape(entry):
        if not isinstance(entry, dict):
            return entry
        e = dict(entry)
        if "plant" in e and "name" not in e:
            e["name"] = e.pop("plant")
        if "why" in e and "why_seasoned" not in e:
            e["why_seasoned"] = e.pop("why")
        return e

    co["good_beginner_seasoned"] = (objectify(co.get("good_beginner_seasoned"))
                                    + [apple_reshape(e) for e in (co.get("good_beginner") or [])])
    co["good_beginner"] = []
    co["bad_beginner_seasoned"] = (objectify(co.get("bad_beginner_seasoned"))
                                   + [apple_reshape(e) for e in (co.get("bad_beginner") or [])])
    co["bad_beginner"] = []

    # ---- lemon: objectify bad_* in place; drop the bad_beginner dup ----
    co = crops["lemon"]["companions"]
    co["bad_seasoned"] = objectify(co.get("bad_seasoned"))
    co["bad_beginner_seasoned"] = objectify(co.get("bad_beginner_seasoned"))
    co["bad_beginner"] = dedup_names(co.get("bad_beginner"), co.get("bad_beginner_seasoned"))

    # ---- orange-navel: objectify good_*/bad_* in place (register placement preserved) ----
    co = crops["orange-navel"]["companions"]
    for b in ("good_seasoned", "good_beginner_seasoned", "good_beginner",
              "bad_seasoned", "bad_beginner_seasoned", "bad_beginner"):
        co[b] = objectify(co.get(b))

    # ---- basil: objectify + un-invert (goods + the fennel caution -> both-mode bucket) ----
    co = crops["basil"]["companions"]
    co["good_beginner_seasoned"] = (objectify(co.get("good_beginner_seasoned"))
                                    + objectify(co.get("good_beginner")))
    co["good_beginner"] = []
    co["bad_beginner_seasoned"] = (objectify(co.get("bad_beginner_seasoned"))
                                   + objectify(co.get("bad_beginner")))
    co["bad_beginner"] = []

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False))

    # ---- self-verify: the gate must be clean on all 5 after the reshape ----
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from companion_shape_gate import companion_shape_violations
    bad = []
    for slug in ("green-beans-bush", "apple", "lemon", "orange-navel", "basil"):
        v = companion_shape_violations(crops[slug])
        print(f"  {slug}: {len(v)} companion-shape violation(s)")
        bad += v
    print("MIGRATION OK -- all 5 clean" if not bad else f"FAIL: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
