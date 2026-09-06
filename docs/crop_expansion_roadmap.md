# Crop expansion roadmap -- new crops, and the cross-crop sequence they wait behind

**What this is:** the living queue of NEW CROPS planned for `crops_data_final.json`, beyond the
current **128** (121 certified gold-standard anchors + 7 honest shells: avocado, olive, the five
mushrooms), plus the cross-crop depth sequence that governs when new-crop work can run. **Live
state is `CURRENT_STATE.md`**, never this file. **The sequence of record is Linear PLA-14** ("The
sequence, as of 2026-09-06"); this file restates it so an outside reader finds it here.

The full family -> crop -> variety inventory lives in
`~/Documents/plant-project/08-reference/master_crop_list.pdf` (outside the repo). New-crop authoring
follows the §E GS-anchor checklist; a crop reuses an existing archetype where the biology allows (no
new gate) or pilots a new archetype first. Sequence new-crop arcs against a STABLE roster, never
mid-certification, and never ahead of the cross-crop sequence below.

## The cross-crop sequence (PLA-14, 2026-09-06)

**The rule:** all cross-crop depth work closes before variety expansion opens. PLA-12's title, PLA-13
and PLA-17 each encode it; this file and `ROADMAP.md` v7.0 now state it.

```
1. PLA-7    container growing model
2. PLA-10   ground spacing and layout methods
3. PLA-9    day-length and photoperiod calculator
4. PLA-11   yield and household planning
5.          cross-crop fields: PLA-142, PLA-143, PLA-137
6. PLA-231  variety surfacing: what a short variety list means
7. PLA-13   cross-crop schema decisions        } the closing
8. PLA-17   app-side schema review             } gates
9. PLA-12   variety expansion
```

Containers and spacing come first because dwarf and semi-dwarf rootstock, bush versus vining habit
and patio cultivars are variety-level data the container model needs; PLA-7 and PLA-10 each owe a
field-shape spec naming what PLA-12 must author, as an arc deliverable. Required kickoff reading:
PLA-7 reads PLA-429 and PLA-409; PLA-10 reads PLA-426 and PLA-429. PLA-13 batches PLA-452, PLA-326,
PLA-260, PLA-325 and the `establishment_years` shape ruling.

Closed since the last edit of this file: PLA-5 (cleanup), PLA-6 (perennial ramp; its go-live is
PLA-363, still In Progress on the plant-astro bump), PLA-8 (IPM ladder, 913/913 problem entries,
A57 armed), PLA-449, PLA-450 / PLA-451 (canonical `72371c02`).

Cleanup that rides in gaps and blocks nothing: PLA-457, PLA-462, PLA-453, PLA-448 s4d,
`monitor_and_tolerate`.

## A standing item: authored, exported, rendered nowhere

A recurring class, not a list of incidents: an arc authors into a field no consumer reads, and
nothing catches it because the gates check the dataset, not the render path. Known members:
`establishment_note` (26 crops), `harvest_stop_rule` (2), `harvest_ramp_na_*`,
`years_to_full_production`, `productive_lifespan_years`, the `region_notes_*` tier (PLA-260),
variety-level `resistance` and `ladder_delta`. **Check the render path before authoring, not
after:** every new field names its consumer in the arc kickoff, or is declared a dataset-side asset.

## Planned additions

| # | Crop(s) | Family / archetype | Pattern (reuse) | Status | Notes |
|---|---------|--------------------|-----------------|--------|-------|
| 1 | **Corn family** -- field/dent corn, popcorn, flint-corn | Zea mays, warm-season grass (`warm_season_grass` -> `frost_anchored`) | the sweet-corn pattern (block/row `planting_layout`, direct-sown) + the dry-bean dry-down harvest ladder (`dry_down` -> `harvest` -> `cure`), NOT sweet-corn's fresh milk-stage harvest | **SHIPPED 2026-07-15** (canonical `e1e01c47`; count 125 -> 128, 116 -> 119 certified; all 3 dry corns) | sweet-corn (certified 2026-07-10) established the block-planted warm-season-grass pattern expressly for these; NO new archetype gate (the `calendar_basis` dispatch already covers `warm_season_grass`). |
| 2 | **Grains & warm-season grasses** -- **sorghum** (grain + sweet/syrup), **millet** (pearl / proso / foxtail) | Poaceae, warm-season grass (`warm_season_grass` -> `frost_anchored`) | same mold as the corn family: frost-anchored, direct-sown warm-season grasses with a dry-down grain harvest; sweet sorghum adds a stalk/syrup harvest variant | QUEUED (added 2026-07-15, Trevor); **waits behind the cross-crop sequence above** | Sibling of the corn family, same build pattern, NO new gate for the grasses. Sorghum is the flagship of a grains lane. |
| 3 | **Pseudo-grains** -- **amaranth**, **quinoa**, **buckwheat** | broadleaf (Amaranthaceae / Polygonaceae), NOT grasses | frost-anchored annuals with a dry-down seed harvest (dry-bean-style ladder), but broadleaf, not grass | QUEUED (added 2026-07-15, Trevor); **waits behind the cross-crop sequence above** | Rounds out a "grains & pseudo-grains" arc alongside #1-#2. The one wrinkle: broadleaf habit, so confirm the archetype fit (they likely do NOT want `warm_season_grass`) before the roster pass; may want a light pilot. |

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
- Since PLA-8: every problem entry ships with an `id`, a `type` and a `control_ladder` against the
  shared catalog (A56/A57), and every minted id is run through `problem_id_collision_gate` at
  pinning time (`docs/ladder_batch_playbook.md`).

The pseudo-grains (amaranth / quinoa / buckwheat) share the frost-anchored + dry-down shape but are
broadleaf, not grasses -- confirm the archetype fit (they may not fit `warm_season_grass`) before the
roster pass.

## Also on the crop backlog (existing)
- The 7 honest shells (the 5 mushrooms + avocado/olive): design/retire decisions, not certification
  backlog. They carry `pests: []` / `diseases: []` and `verification_status.status = None` by intent.
- Full family -> crop -> variety inventory: `~/Documents/plant-project/08-reference/master_crop_list.pdf`
  (outside the repo).

---
*(Add a row when a new crop or crop-family is planned. Reuse an existing archetype/gate where the
biology allows; pilot a new archetype only when a crop genuinely does not fit one. Keep the
sequence section in step with Linear PLA-14; edit it there first.)*
