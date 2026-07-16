# Crop expansion roadmap -- planned new crops for the roster

**What this is:** the living queue of NEW CROPS planned for `crops_data_final.json`, beyond the
current **125** (116 certified + 9 shells). The full family -> crop -> variety inventory lives in
`~/Documents/plant-project/08-reference/master_crop_list.pdf` (the Phase 4 variety-expansion
inventory, outside the repo); this doc tracks the near-term, method-ready additions and their build
pattern. New-crop authoring follows the §E GS-anchor checklist; a crop reuses an existing archetype
where the biology allows (no new gate) or pilots a new archetype first. Sequence new-crop arcs against
a STABLE roster, never mid-certification.

## Planned additions

| # | Crop(s) | Family / archetype | Pattern (reuse) | Status | Notes |
|---|---------|--------------------|-----------------|--------|-------|
| 1 | **Corn family** -- field/dent corn, popcorn, flint-corn | Zea mays, warm-season grass (`warm_season_grass` -> `frost_anchored`) | the sweet-corn pattern (block/row `planting_layout`, direct-sown) + the dry-bean dry-down harvest ladder (`dry_down` -> `harvest` -> `cure`), NOT sweet-corn's fresh milk-stage harvest | **SHIPPED 2026-07-15** (canonical `e1e01c47`; count 125 -> 128, 116 -> 119 certified; all 3 dry corns) | sweet-corn (certified 2026-07-10) established the block-planted warm-season-grass pattern expressly for these; NO new archetype gate (the `calendar_basis` dispatch already covers `warm_season_grass`). |
| 2 | **Grains & warm-season grasses** -- **sorghum** (grain + sweet/syrup), **millet** (pearl / proso / foxtail) | Poaceae, warm-season grass (`warm_season_grass` -> `frost_anchored`) | same mold as the corn family: frost-anchored, direct-sown warm-season grasses with a dry-down grain harvest; sweet sorghum adds a stalk/syrup harvest variant | QUEUED (added 2026-07-15, Trevor) | Sibling of the corn family, same build pattern, NO new gate for the grasses. Sorghum is the flagship of a grains lane. |
| 3 | **Pseudo-grains** -- **amaranth**, **quinoa**, **buckwheat** | broadleaf (Amaranthaceae / Polygonaceae), NOT grasses | frost-anchored annuals with a dry-down seed harvest (dry-bean-style ladder), but broadleaf, not grass | QUEUED (added 2026-07-15, Trevor) | Rounds out a "grains & pseudo-grains" arc alongside #1-#2. The one wrinkle: broadleaf habit, so confirm the archetype fit (they likely do NOT want `warm_season_grass`) before the roster pass; may want a light pilot. |

## The build pattern (grains & warm-season grasses)

The sweet-corn arc (2026-07-10) already paved this for the grass members:
- `calendar_basis: frost_anchored`, with the sanctioned `warm_season_grass` archetype in
  `calendar_basis_gate` ARCHETYPE_BASIS (its "extend when a new archetype is certified" mechanism) --
  so a new warm-season grass needs NO new dispatch gate.
- Direct-sown (`weeks_indoors 0`), block/row `planting_layout`.
- Dry-down grain harvest reuses the dry-bean `dry_down` -> `harvest` -> `cure` ladder (the `harvest`
  stage id is the A40 anchor; one-shot harvest, `harvest_window_days` omitted).
- All the §E register fields + T1 sourcing (extension grain guides: e.g. K-State, Texas A&M AgriLife,
  Nebraska, Purdue for grain sorghum + the millets).

The pseudo-grains (amaranth / quinoa / buckwheat) share the frost-anchored + dry-down shape but are
broadleaf, not grasses -- confirm the archetype fit (they may not fit `warm_season_grass`) before the
roster pass.

## Also on the crop backlog (existing)
- The GS-anchor certification backlog: staged §E draft crops + the design/retire shells (the 5
  mushrooms + avocado/olive/artichoke/asparagus). See memory `remaining-gs-anchors-roadmap`.
- Full family -> crop -> variety inventory: `~/Documents/plant-project/08-reference/master_crop_list.pdf`
  (outside the repo).

---
*(Add a row when a new crop or crop-family is planned. Reuse an existing archetype/gate where the
biology allows; pilot a new archetype only when a crop genuinely does not fit one.)*
