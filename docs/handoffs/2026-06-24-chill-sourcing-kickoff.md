# Chill-sourcing kickoff (claude.ai authoring lane)

**Created:** 2026-06-24 (Claude Code, audit Phase A / F2)
**Lane:** claude.ai SOURCES the numbers; Claude Code RELEASES (verify -> promote).
**Depends on:** dataset `9739e373` (the F2 chill refactor must be in -- it created the table).

## The mission, in one line

Replace the PLACEHOLDER values in the shared top-level `region_chill_delivered` table
with ONE T1-sourced winter chill-DELIVERED band per region+zone. This is a
reconcile-to-a-sourced-value pass, not fresh authoring: the magnitudes are already
realistic, they are just not independently sourced.

## Why this exists

`chill_hours_delivered` (how much winter chill a climate banks) used to be authored
per-crop, so peach/apple/blueberry disagreed at the same region+zone and blueberry
stored it as a string. The F2 refactor moved it into ONE shared, crop-invariant table
`region_chill_delivered` (region -> {zone -> [lo, hi]}). The numbers currently in it
were SEEDED as the union of the old per-crop bands -- realistic but NOT sourced. See
`region_chill_delivered_provenance` in `crops_data_final.json`.

This is a CLIMATE datum (chill the AREA banks), the inverse of the per-variety
chill-REQUIRED (`chill_hours_required` / `chill_hours_range`), which is already correct
and is NOT in scope here.

## What to deliver

A patch (per `docs/handoff_patch_format_v1_0.md`) that sets each
`region_chill_delivered[<region>][<zone>]` to a sourced `[lo, hi]` integer band, plus
a refreshed `region_chill_delivered_provenance` string naming the model + the sources,
plus the source-catalog mints for any new T1 IDs.

### Hard requirements
- **T1 sources only** (university extension / UC IPM chill maps / state climatologist
  chill-accumulation data). No seed companies, no almanacs.
- **Per region+zone, not per zone.** Chill depends on the whole winter temperature
  profile, not the USDA winter-low zone -- zone 9 in humid se_gulf, CA interior, and
  CA desert bank very different chill. NEVER derive the band from the USDA zone.
- **Name the model.** Chill is counted differently by different sources: the Utah model
  (hours 32-45 degrees F), hours below 45 degrees F, or chill portions (Dynamic model).
  Pick the model the cited source uses and state it in the provenance; keep the table
  internally consistent (one model across all cells, or note per-cell which model).
- **`[lo, hi]` integers, `0 <= lo <= hi`.** The gate (`chill_table_violations`, run in
  `release_verify` H) rejects anything else. No open-ended "or more" strings.
- **Reconcile the prose.** The per-crop `regions.<r>.chill_basis_seasoned/beginner` on
  peach/apple references specific delivered numbers ("bank roughly 700 to 1,600 chill
  hours"). After the table is sourced, update any basis prose whose numbers now diverge.

## The 20 cells to source (current PLACEHOLDER union -- replace each)

| region | zone: [lo, hi] |
|---|---|
| northern_tier | z3: [1100,1600]  z4: [1000,1500]  z5: [900,1400]  z6: [800,1300]  z7: [700,1200] |
| se_gulf | z8: [450,1000]  z9: [350,650] |
| ca_interior | z8: [500,1100]  z9: [300,950] |
| ca_north_coast | z9: [300,800]  z10: [150,600] |
| ca_south_coast | z9: [200,550]  z10: [100,350] |
| ca_desert | z9: [150,400]  z10: [100,300] |
| warm_arid | z8: [400,850] |
| low_desert_az | z9: [100,400] |
| fl_peninsula | z10: [50,350]  z11: [0,150] |
| hawaii_tropical | z11: [0,150] |

These are the region+zone cells the three certified chill crops (peach/apple/blueberry)
resolve to. If a future chill crop needs a region+zone not listed, add the cell.

## Release path (Claude Code, after you deliver)

Apply the patch -> `chill_table_violations` (shape) + `whole_crop_gate` on peach/apple/
blueberry (the A3 no-fruit split now reads the table) + the prose reconcile -> promote
with the full ceremony. The plant-astro chill cards already read this table and show
"your area banks ~X; these varieties need ~Y", so a sourced value renders immediately
on the next submodule bump.
