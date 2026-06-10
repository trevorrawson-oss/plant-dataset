#!/usr/bin/env python3
"""Schema 2.9 migration -- additive null-scaffold per docs/schema_2_9_scope_v0.md.

DETERMINISTIC, IDEMPOTENT, NON-DESTRUCTIVE. Adds new fields (null/empty) per the
archetype applicability matrix; bumps schema_version 2.8 -> 2.9. Does NOT interpret
or move any existing value -- biology is authored per perennial/tree anchor later.

Three threads, all additive:
  A perennial/tree : chill / bloom / pollination / rootstock / windows / establishment
                     / cane (brambles) / renovation (matted) -- gated by archetype.
  B containers/watering : watering_method + schedule_by_stage + drought_tolerance
                     + critical_periods + fertilizer.amount + container self-watering -- UNIVERSAL.
  C normalization (additive slice) : sources/anchoring_urls plumbing on the four shells.
     (C1 register reshape + C3 vocab value-reconcile are deferred off this structural pass.)

Variety-object upgrade is scoped to WOODY archetypes (the bloom calendar); non-woody
crops' varieties.recommended string lists are left untouched, so the (non-woody)
certified anchors are not disturbed there. Universal null fields DO land on every crop
(uniform shape); additive nulls keep launch_ready (same as the 2.7.5 bump).

Usage:
  python3 tools/migrate_schema_2_9.py --in crops_data_final.json --out /tmp/scratch.json
  python3 tools/migrate_schema_2_9.py --in F --out F            # in place, idempotent
"""
import json
import argparse
import hashlib

# --- archetype sets (applicability matrix, doc Section 5) ---
WOODY = {"deciduous_fruit_tree", "evergreen_fruit_tree", "berries_woody"}
GRAFTED = {"deciduous_fruit_tree", "evergreen_fruit_tree"}   # rootstock
BRAMBLE = {"berries_woody"}                                  # cane mgmt (blueberry null-ok)
MATTED = {"berries_herbaceous"}                              # strawberry: renovation
PERENNIAL_FRUIT = WOODY | MATTED                            # establishment


def ensure(d, key, default):
    """Add key=default ONLY if absent. Never overwrite -> idempotent + non-destructive."""
    if key not in d:
        d[key] = default


def ensure_pair(d, base):
    ensure(d, base + "_seasoned", None)
    ensure(d, base + "_beginner", None)


def migrate_crop(c):
    arch = c.get("archetype")

    # ---------- B (UNIVERSAL) ----------
    w = c.setdefault("watering", {})
    ensure(w, "watering_method", None)            # base|drip|soaker|overhead_ok
    ensure(w, "schedule_by_stage", [])            # [{stage_id,system,rate,frequency,level,note_*}]
    ensure(w, "drought_tolerance", None)          # low|moderate|high
    ensure_pair(w, "method_note")                 # rot-avoidance / base-vs-overhead
    ensure_pair(w, "critical_periods")            # can't-miss watering windows

    f = c.setdefault("fertilizer", {})
    ensure_pair(f, "amount")                      # how MUCH per feeding (Trevor)

    cn = c.setdefault("container_notes", {})
    ensure(cn, "self_watering_ok", None)
    ensure_pair(cn, "self_watering_notes")

    # ---------- C (UNIVERSAL additive slice): sources/anchoring plumbing ----------
    for shell in ("watering", "fertilizer", "thinning", "varieties"):
        s = c.get(shell)
        if isinstance(s, dict):
            ensure(s, "sources", None)
            ensure(s, "anchoring_urls", None)

    # ---------- A: WOODY -- chill / bloom / pollination / windows ----------
    if arch in WOODY:
        ensure(c, "chill_hours_required", None)
        ensure(c, "chill_hours_range", [])
        ensure_pair(c, "chill_hours_note")
        ensure_pair(c, "bloom_time")
        ensure(c, "bloom_duration_days", None)
        ensure_pair(c, "pollinator_notes")
        poll = c.setdefault("pollination", {})
        ensure(poll, "self_fertile", None)
        ensure(poll, "needs_pollinizer", None)
        ensure(poll, "pollinizer_distance_ft", None)
        ensure_pair(poll, "notes")
        ensure(c, "dormancy_window", None)
        ensure(c, "pruning_window", None)
        ensure_pair(cn, "container_overwintering")
        # woody varieties.recommended is the bloom-calendar list (objects authored per-anchor)
        v = c.get("varieties")
        if isinstance(v, dict):
            v.setdefault("recommended", [])

    # ---------- A: PERENNIAL FRUIT (woody + matted) -- establishment ----------
    if arch in PERENNIAL_FRUIT:
        ensure(c, "establishment_years", None)
        ensure(c, "establishment_note", None)     # universal: "won't fruit for ~3 years"

    # ---------- A: GRAFTED trees -- rootstock ----------
    if arch in GRAFTED:
        ensure(c, "recommended_rootstock", None)
        ensure(c, "recommended_rootstock_note", None)  # universal plain
        ensure(c, "rootstock_options", [])             # [{name,size_class,mature_height_ft,...}]

    # ---------- A: BRAMBLES -- cane management ----------
    if arch in BRAMBLE:
        ensure(c, "cane_type", None)
        ensure_pair(c, "cane_management")

    # ---------- A: MATTED (strawberry) -- renovation + bloom ----------
    if arch in MATTED:
        ensure_pair(c, "renovation")
        ensure_pair(c, "bloom_time")
        ensure_pair(c, "pollinator_notes")

    return c


VERSIONING_2_9 = (" As of schema_version 2.9, the perennial/tree extension is "
                  "scaffolded (null-by-archetype): chill_hours_*, bloom_*, pollination, "
                  "rootstock_options, dormancy_window/pruning_window, cane_management, "
                  "renovation, establishment_years on woody/perennial archetypes; plus "
                  "universal watering_method + schedule_by_stage + drought_tolerance + "
                  "critical_periods + fertilizer.amount + container self-watering, and "
                  "sources/anchoring_urls plumbing on watering/fertilizer/thinning/varieties. "
                  "Values authored per anchor; this bump is additive scaffolding only.")


def migrate_dataset(d):
    for c in d.get("crops", []):
        migrate_crop(c)
    d["schema_version"] = "2.9"
    note = d.get("versioning_note") or ""
    if "2.9" not in note:
        d["versioning_note"] = note + VERSIONING_2_9
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    args = ap.parse_args()
    raw = open(args.inp, encoding="utf-8").read()
    before = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    d = json.loads(raw)
    migrate_dataset(d)
    out = json.dumps(d, separators=(",", ":"), ensure_ascii=False)
    open(args.out, "w", encoding="utf-8").write(out)
    after = hashlib.sha256(out.encode("utf-8")).hexdigest()
    print("schema_version:", d.get("schema_version"))
    print("crops:", len(d.get("crops", [])))
    print("before SHA:", before[:12], "-> after SHA:", after[:12])
    if before == after:
        print("(no change -- already migrated; idempotent)")


if __name__ == "__main__":
    main()
