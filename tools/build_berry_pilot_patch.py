#!/usr/bin/env python3
"""Emit the SHA-guarded COMPACT patch enriching strawberry's varieties to the flat BERRY schema
(spec: berry variety pilot, 2026-07-15; the 5th archetype). The 9 varieties fold in the common core
(id/name/maturity_class/confidence_tier/hero_description/note_beginner/note_seasoned/sources +
anchoring_urls) plus the berry-specific block (bearing_habit/use), replacing the legacy
name/type/days_or_season/use/recommended_note shape. New crop-level `variety_archetype: "berry"` +
`berry_group: "strawberry"` (strawberry is the FIRST live berry_group; cane/bush are reserved,
0 live). ALSO folds in the Task-5 hero_description backfill for the 4 prior variety pilots
(dry-bean/apple/onion/leek, 33 varieties) into the SAME atomic batch, per the Task 6 brief.

DESIGN (staged inputs, controller-authored + gate-verified 2026-07-15):
- Per-variety `sources`/`anchoring_urls` carry T1 ONLY (see
  docs/reviews/notes/2026-07-15/strawberry_variety_sourcing.md). All 9 varieties are T1.
- Strawberry is berry_group=strawberry (no chill_hours_required -- the herbaceous berry has no
  chill trait; chill_hours_required is a cane/bush-only field per variety_detail_gate).
- days_to_maturity is NOT part of the berry archetype (berry is not in variety_detail_gate's
  DTM_ARCHETYPES) -- strawberry stays season-only, unaffected.
- exactly ONE is_reference:true => Albion (the day-neutral benchmark, "good first choice").
- verification_status.source_set: strawberry's existing set already catalogues every T1 id the 9
  varieties cite (cornell_ext/osu_ext/umd_ext/umn_ext), so the replace op is emitted ONLY IF the
  computed union actually introduces a new id -- computed, never hardcoded, so a future re-run
  with different sourcing still resolves correctly.
- The 33 hero_description adds (Task 5) are folded into this SAME atomic batch; each is an `add`
  onto the currently-empty/absent slot on the matching prior-pilot variety object.

All `from`/`value` are computed from the LOADED canonical (never hand-typed), so the apply_patch
from-guards cannot drift. Every authored string is asserted em-dash-free.

Prints the COMPACT-indent patch JSON to STDOUT only (diagnostics go to stderr) so the caller can
redirect straight to the batch file:
  python3 tools/build_berry_pilot_patch.py > tools/batches/berry_strawberry_pilot.json
"""
import hashlib
import json
import os
import sys

CANON = "crops_data_final.json"
OUT = "tools/batches/berry_strawberry_pilot.json"
STRAWBERRY_VARIETIES = "/private/tmp/strawberry_varieties.json"
HERO_BACKFILL = "/private/tmp/hero_backfill.json"

BERRY_COMMON_CORE = ("id", "name", "maturity_class", "confidence_tier",
                      "hero_description", "note_beginner", "note_seasoned", "sources")
BERRY_TRAITS = ("bearing_habit", "use")


def crop(data, slug):
    return next(c for c in data["crops"] if c.get("slug") == slug)


def assert_no_em_dash(s, where):
    assert "—" not in s, f"em dash in {where}: {s!r}"


def build_variety(vd):
    """Validate a staged variety object against the flat berry schema (fail loudly on drift) and
    assert no em dash in any authored string field. Returns a shallow copy, key order preserved."""
    for f in BERRY_COMMON_CORE + BERRY_TRAITS:
        assert f in vd and vd[f] not in (None, "", []), f"strawberry variety {vd.get('id')}: missing {f!r}"
    assert isinstance(vd.get("is_reference"), bool), f"strawberry variety {vd.get('id')}: is_reference not bool"
    assert isinstance(vd.get("anchoring_urls"), dict) and vd["anchoring_urls"], \
        f"strawberry variety {vd.get('id')}: missing anchoring_urls"
    for f in ("name", "hero_description", "note_beginner", "note_seasoned", "use"):
        assert_no_em_dash(vd[f], f"strawberry/{vd.get('id')}.{f}")
    return dict(vd)


def build_strawberry_ops(data, staged):
    """The strawberry-side ops: variety_archetype, berry_group, varieties.recommended replace, and
    the conditional source_set replace. Returns (ops, source_set_op) where source_set_op is
    'emitted' or 'skipped'."""
    sb = crop(data, "strawberry")
    assert len(staged) == 9, f"expected 9 staged strawberry varieties, got {len(staged)}"

    varieties = [build_variety(vd) for vd in staged]
    ref_ids = [v["id"] for v in varieties if v["is_reference"]]
    assert ref_ids == ["albion"], f"exactly one flagship expected (albion), got {ref_ids}"
    ids = [v["id"] for v in varieties]
    assert len(ids) == len(set(ids)), f"duplicate variety id(s) in staged input: {ids}"

    current_varieties = sb["varieties"]
    current_recommended = current_varieties["recommended"]
    assert isinstance(current_recommended, list) and current_recommended, \
        "strawberry.varieties.recommended: expected a populated legacy list to replace"

    ops = []

    assert sb.get("variety_archetype") is None, "strawberry already carries variety_archetype"
    assert sb.get("berry_group") is None, "strawberry already carries berry_group"
    ops.append({"op": "add", "json_path": "$.crops[?(@.slug=='strawberry')].variety_archetype",
                "value": "berry"})
    ops.append({"op": "add", "json_path": "$.crops[?(@.slug=='strawberry')].berry_group",
                "value": "strawberry"})

    # Only recommended[] moves; the varieties-level note_beginner/note_seasoned/sources/
    # anchoring_urls carry forward unchanged (not touched by this op).
    ops.append({"op": "replace", "json_path": "$.crops[?(@.slug=='strawberry')].varieties.recommended",
                "from": current_recommended, "value": varieties})

    cited = sorted({i for v in varieties for i in v["sources"]})
    current_ss = sb["verification_status"]["source_set"]
    new_ids = sorted(set(cited) - set(current_ss))
    if new_ids:
        new_ss = sorted(set(current_ss) | set(cited))
        ops.append({"op": "replace",
                     "json_path": "$.crops[?(@.slug=='strawberry')].verification_status.source_set",
                     "from": current_ss, "value": new_ss})
        return ops, "emitted"
    return ops, "skipped"


def build_hero_ops(data, hero_rows):
    """`add` ops folding in the Task-5 hero_description backfill (dry-bean/apple/onion/leek). Each
    targets the exact variety by slug+id read from the loaded canonical, and refuses to clobber an
    already-present hero_description. Generic over the row count (the real run's 33-row invariant
    is asserted in build_patch, the atomic-batch assembly point)."""
    ops = []
    seen = set()
    for row in hero_rows:
        slug, vid, hero = row["slug"], row["id"], row["hero_description"]
        key = (slug, vid)
        assert key not in seen, f"duplicate hero row {key}"
        seen.add(key)
        assert_no_em_dash(hero, f"{slug}/{vid}.hero_description")
        c = crop(data, slug)
        rec = c["varieties"]["recommended"]
        target = next((x for x in rec if x.get("id") == vid), None)
        assert target is not None, f"{slug}: no variety with id={vid!r} found in canonical"
        assert target.get("hero_description") in (None, ""), \
            (f"{slug}/{vid}: hero_description already present "
             f"({target.get('hero_description')!r}); refusing to clobber")
        ops.append({"op": "add",
                     "json_path": (f"$.crops[?(@.slug=='{slug}')].varieties.recommended"
                                   f"[?(@.id=='{vid}')].hero_description"),
                     "value": hero})
    return ops


def build_patch(data, staged_varieties, hero_rows, sha):
    """Assembles the full atomic batch dict {base_sha, patches}. Pure function of its inputs so
    the test can drive it against synthetic fixtures without touching disk."""
    assert len(hero_rows) == 33, f"expected 33 staged hero rows, got {len(hero_rows)}"
    sb_ops, source_set_op = build_strawberry_ops(data, staged_varieties)
    hero_ops = build_hero_ops(data, hero_rows)
    ops = sb_ops + hero_ops
    expected = 2 + 1 + (1 if source_set_op == "emitted" else 0) + len(hero_rows)
    assert len(ops) == expected, f"op count mismatch: {len(ops)} != {expected}"
    return {"base_sha": sha, "patches": ops}, source_set_op


def main():
    raw = open(CANON, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)

    staged = json.load(open(STRAWBERRY_VARIETIES, encoding="utf-8"))
    hero_rows = json.load(open(HERO_BACKFILL, encoding="utf-8"))

    patch, source_set_op = build_patch(data, staged, hero_rows, sha)

    text = json.dumps(patch, ensure_ascii=False, indent=1)
    print(text)
    print(f"wrote {len(patch['patches'])} ops (base_sha {sha[:12]}, source_set {source_set_op}) "
          f"-- redirect stdout to {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
