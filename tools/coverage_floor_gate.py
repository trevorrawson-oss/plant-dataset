#!/usr/bin/env python3
"""Coverage-floor cert gates -- the presence floors A2 never enforced (whole_crop_gate A31/A32).

incognito-redteam C3 + C4 (2026-06-27): the gates iterate whatever regions/cells exist and
validate each, but NEVER assert that ENOUGH exist. So a non-indoor crop could ship with
regions:{} (zero coverage) or a single region, and a frost_anchored annual could ship with the
calendar[] deleted on every cell -- both certify, because every per-region / per-cell gate just
`continue`s on the missing structure (A5/A24/A28 skip an absent calendar; A2 checks plantings,
never the calendar). These two floors close that:

  A31 region_roster_violations -- a non-indoor crop must carry the full 10-region roster.
  A32 calendar_presence_violations -- a frost_anchored cell must carry a non-empty calendar.

Both are archetype-aware: an indoor / zone_independent crop legitimately collapses regions to {}
(A31 exempts it), and tree empty cells are governed by A3's no-fruit split (A32 is frost_anchored
only).
"""

# The canonical 10-region roster -- identical across all 17 non-indoor certified anchors and the
# top-level `region_chill_delivered` table. THE coverage floor for a region-resolved crop.
CANONICAL_REGIONS = {
    "ca_desert", "ca_interior", "ca_north_coast", "ca_south_coast", "fl_peninsula",
    "hawaii_tropical", "low_desert_az", "northern_tier", "se_gulf", "warm_arid",
}

# re-audit #2 D7: the resolved_by_zone KEY roster -- USDA hardiness zones 3-11. A31 validated
# region keys but no zone roster existed, so a fictitious zone ("banana_zone") or a hollow
# resolved_by_zone (D2) certified. Every resolved cell in the 17 non-indoor anchors keys 3-11.
CANONICAL_ZONES = {"3", "4", "5", "6", "7", "8", "9", "10", "11"}

# re-audit #2 D3: the calendar-presence floor (A32) was frost_anchored-only, so the 3 NON-TREE
# perennial archetypes could ship every cell calendar:[]. Trees (perennial_chill_gated/evergreen)
# are EXCLUDED -- their empty cells are legitimate (unsuitable/chill-limited) and A3 governs them.
CALENDAR_PRESENCE_BASES = {
    "frost_anchored", "perennial_herbaceous", "berries_woody", "perennial_woody_ornamental",
}


def _is_indoor(crop):
    # re-audit #2 D1: key ONLY on calendar_basis (which A30 validates), NOT on the unvalidated
    # `zone_independent` flag -- trusting the flag let a frost_anchored crop set zone_independent:true
    # + regions:{} and exempt itself from the whole region/calendar floor. A30 now also asserts
    # zone_independent is consistent with the basis, so the flag is no longer a backdoor here.
    return crop.get("calendar_basis") == "non_seasonal_indoor"


def region_roster_violations(crop):
    """Return a list ([] = clean). A non-indoor crop must carry EXACTLY the canonical 10-region
    roster -- no missing region (regions:{} or a partial roster renders the crop for almost
    nowhere) and no unknown region key (a typo renders a region the model does not resolve). An
    indoor / zone_independent crop must collapse regions to {} (a non-empty regions there is
    off-model)."""
    regions = crop.get("regions") or {}
    if _is_indoor(crop):
        if regions:
            return [f"indoor/zone_independent crop must collapse regions to {{}} "
                    f"(got {len(regions)}: {sorted(regions)})"]
        return []
    have = set(regions)
    missing = sorted(CANONICAL_REGIONS - have)
    unknown = sorted(have - CANONICAL_REGIONS)
    V = []
    if missing:
        V.append(f"non-indoor crop is missing canonical region(s) {missing} "
                 f"(has {len(have)}/{len(CANONICAL_REGIONS)}); the 10-region roster is the coverage "
                 f"floor -- a partial/empty roster certifies a crop that renders for almost nowhere")
    if unknown:
        V.append(f"unknown region key(s) {unknown} not in the canonical 10-region roster "
                 f"(a typo'd region renders for a region the model never resolves)")
    # D2 + D7: validate the zone layer BELOW each region key -- A31 stopped at the region key, so a
    # hollow resolved_by_zone (D2) or a fictitious zone key (D7) certified.
    for rk in sorted(have & CANONICAL_REGIONS):
        rbz = (regions.get(rk) or {}).get("resolved_by_zone")
        if not (isinstance(rbz, dict) and rbz):
            V.append(f"{rk}: empty/absent resolved_by_zone -- a region key with no resolved zones "
                     f"below it renders no calendar (the region roster floor stops at the key)")
            continue
        bad_zones = sorted(set(rbz) - CANONICAL_ZONES)
        if bad_zones:
            V.append(f"{rk}: unknown zone key(s) {bad_zones} not in the USDA zone roster "
                     f"{sorted(CANONICAL_ZONES, key=int)} (a fictitious zone certifies a cell the "
                     f"model never resolves)")
    return V


def calendar_presence_violations(crop):
    """Return a list ([] = clean). For a frost_anchored crop, every resolved_by_zone cell must
    carry a NON-EMPTY calendar -- the calendar IS the page's core deliverable, and A5/A24/A28 all
    `continue` on an absent one, so a cell with calendar:[] (or no calendar key) silently ships a
    blank planner. No-op off the CALENDAR_PRESENCE_BASES (frost_anchored + the 3 non-tree perennials,
    D3): TREE empty cells are governed by A3's no-fruit split (unsuitable / chill-limited cells are
    legitimately empty), and indoor crops have no cells."""
    basis = crop.get("calendar_basis")
    if basis not in CALENDAR_PRESENCE_BASES:
        return []
    V = []
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            if not (cell.get("calendar") or []):
                V.append(f"{rk}.{z}: {basis} resolved cell has an empty/absent calendar "
                         f"-- this archetype's cells must render a non-empty month-strip calendar")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        vs = region_roster_violations(c) + calendar_presence_violations(c)
        if vs:
            print(f"  {c.get('slug')}:")
            for v in vs:
                print(f"     {v}")
            total += len(vs)
    print(f"coverage_floor gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
