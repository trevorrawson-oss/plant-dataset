# Corn Family GS-Anchor Arc -- Design Spec (field-corn / popcorn / flint-corn)

**Status:** design, approved 2026-07-15 (Trevor).
**Arc:** certify the three DRY corns as new §E crops, the fast follow-on the sweet-corn arc set up.
All *Zea mays*, frost-anchored direct-sown annuals. **NO new gate, NO new field.**
**Workspace:** isolated worktree `.claude/worktrees/corn-family` (branch `worktree-corn-family`), so it
runs without colliding with the region Tier-2 arc active on `main`.
**Base:** canonical `c73d7fa` (125 crops, 116 certified); result 128 crops, 119 certified.

---

## 1. Context and goal

`sweet-corn` (certified 2026-07-10) established the corn pattern expressly so the family could follow:
`corn`/field-dent, `popcorn`, `flint-corn` are all *Zea mays*, frost-anchored, direct-sown, wind-
pollinated block-planted annuals (kickoff #21). This arc certifies all three at once. The pattern is
fully proven, so this is not an archetype pilot -- it is APPLYING two settled templates:
- **sweet-corn** -- the corn front half (block planting, the germination -> ... -> kernel_fill stages,
  frost-anchored annual calendar, `warm_season_grass` archetype, `planting_layout`).
- **dry-bean** -- the dry-down harvest tail (`dry_down -> harvest -> cure_thresh` ladder, the `harvest`-id
  A40 anchor, `harvest_window_days` omitted, single-crop `succession` off, humid-region Option C).

The only real delta from sweet-corn is the HARVEST: the dry corns dry down on the stalk (grain/pop/meal),
not a fresh milk-stage pick.

## 2. Governing principles (inherited, no new machinery)

Per kickoff #21's reframe (verified against the code): **the gate dispatch key is `calendar_basis`, NOT
`archetype`.** A frost-anchored direct-sown annual runs the STANDARD annual gate set; `dry-bean` is the
proof that a fresh warm-season annual certifies with A39/A40 native and ZERO new gate. Therefore:
- **NO new gate.** §E checklist is native: A39 (register coverage) + A40 (timing-spine value shape) fall
  out of clean authoring.
- **NO new field.** Block planting reuses the existing `planting_layout` (enum) + `pollination_block_min_rows`
  that sweet-corn already added; the archetype label `warm_season_grass` already exists.
- **Legacy variety shape.** These are new §E crops; their `varieties.recommended` use the LEGACY
  `{name, dtm, note, ...}` shape (like sweet-corn / dry-bean), NOT the flat `variety_detail` schema. The
  berry-arc `hero_description` common-core does NOT apply (variety_detail_gate is opt-in via
  `maturity_class`; these crops do not opt in). Variety migration is the deferred Spec-2 roster rollout.

## 3. The three crops + shared archetype

New §E crops (category `Corn`), each modeled field-by-field on sweet-corn + dry-bean:
- `field-corn` (dent) -- slug chosen over bare `corn` to stay unambiguous next to `sweet-corn` (confirm
  against the master crop list at authoring).
- `popcorn`
- `flint-corn`

Shared crop-level shape (copy sweet-corn's exact structure): `calendar_basis: "frost_anchored"`,
`archetype: "warm_season_grass"`, `weeks_indoors: 0` (direct-sown; `seedling_light`/`tray_sowing` = na),
`planting_layout: "block"` + `pollination_block_min_rows: 4`, frost-tender (`frost_effect: killed`,
germination/heat/chilling thresholds copied from sweet-corn's sourced values), `succession` single-crop
(suitable off, like dry-bean).

## 4. The dry-down harvest model (the delta)

`growth_stages` ladder = sweet-corn's corn front half + dry-bean's dry-down tail:
`germination -> seedling -> vegetative -> tasseling -> silking -> kernel_fill -> dry_down -> harvest -> cure_thresh`.
- `kernel_fill` -- kernels fill and dent/harden on the ear.
- `dry_down` -- kernels dry on the stalk to storage moisture.
- **`harvest`** -- the A40 LOAD-BEARING anchor (dry ears; kernels hard). A40 validates ladder
  monotonicity + the DTM band anchored on this id, exactly as dry-bean.
- `cure_thresh` -- finish drying + shell/thresh off the cob for storage.
- **`harvest_window_days` OMITTED** (one-shot dry harvest; you can leave ears on the stalk -- the dry-bean
  precedent, NOT sweet-corn's tight `[4,7]` milk window). Per-stage `day_range_from_sow` monotonic,
  windows overlapping per the green-beans/dry-bean convention.

## 5. Regions -- 12 each, Option C, dry-bean humid handling

Each crop is authored across all 12 canonical regions (the A31 coverage floor): `northern_tier`,
`se_gulf`, `ca_interior`, `ca_north_coast`, `ca_south_coast`, `ca_desert`, `warm_arid`, `low_desert_az`,
`fl_peninsula`, `hawaii_tropical`, `rgv`, `pnw`. T1-anchored sow -> dry-down calendars (extension
grain-corn guides: Iowa State, K-State, Purdue, Nebraska, UMN, plus the warm-region siblings already
cited for sweet-corn/dry-bean).

**Option C (all plantable, honest advisories) -- the dry-bean precedent, since the dry corns hit the
humid field-drying problem sweet-corn sidestepped:** in humid regions (`fl_peninsula`, `se_gulf`,
`hawaii_tropical`, `rgv`, maritime `pnw`) dry-down-on-the-stalk molds, so the calendars stay populated
but the prose advises harvesting at hard-dent and finishing the dry-down indoors. Short-season northern
zones carry honest DTM advisories (a long-season dent may not finish in the coldest zones). No region
needs `suitable:false` (the annual model's suitability enum is tree-only; honesty lives in prose, as
dry-bean established). `heat_pause` where a desert summer genuinely pauses set (sweet-corn precedent).

## 6. Per-crop identity, DTM, varieties, cross-pollination

DTM is a **Trevor-ratified synthesis band per crop** (inherently variety-dependent + maturity-class
spread; no single T1 species figure -- the sweet-corn/dry-bean precedent; the app works from windows):
- **field-corn/dent** -- grain, cornmeal, masa/hominy, animal feed; DTM ~`[95,120]` (the longest-season
  dry corn); varieties e.g. Reid's Yellow Dent, Wapsie Valley, hybrid grain dents.
- **popcorn** -- popping (hard-endosperm, pops on moisture flash); DTM ~`[90,110]`; varieties e.g. Robust,
  Japanese Hulless, Dakota Black, Strawberry (ornamental + pop).
- **flint-corn** -- cornmeal, polenta, hominy, decorative; DTM ~`[90,110]`; varieties e.g. Painted
  Mountain (short-season), Floriani Red Flint, Cascade Ruby-Gold, Glass Gem (ornamental).

**Cross-pollination (prose in each crop's planting/variety guidance, no schema):** the corn types cross-
pollinate readily and it shows in the kernel that season -- dent pollen on popcorn ruins popping, flint
x dent muddies both. Isolate by distance (~250+ ft between blocks) OR stagger tassel timing (~2 weeks),
and note this ALSO applies vs a neighbor's sweet-corn. Crop `description_beginner`/`description_seasoned`
name the representative variety spectrum (good practice, the leek/apple template) but stay legacy-shape.

## 7. Sourcing

T1 extension grain-corn guides (Iowa State, K-State Research & Extension, Purdue, University of Nebraska,
UMN, plus the warm-region sources already catalogued for sweet-corn/dry-bean). Per the DTM precedent,
the synthesis DTM band is Trevor-ratified (no single T1 figure); every regional calendar + threshold +
cultural claim is T1-anchored. `source_set` per crop reconciled to what is actually cited; new
`source_catalog` entries only if a genuinely new T1 source is needed (prefer the existing corn/grain
catalog ids).

## 8. Gates + footprint

- **NO new gate, NO new field.** `whole_crop_gate` (§3 A-gates) + A39 + A40 + `calendar_coherence` +
  `release_verify` validate each crop natively (the dry-bean greenfield proof).
- `calendar_basis_gate` already maps `warm_season_grass -> frost_anchored` (sweet-corn's ruling);
  `planting_layout` A44 already validates block + `pollination_block_min_rows` (sweet-corn's gate).
- **Adversarial RED proof per crop** (the CLAUDE.md bar): on a scratch copy, inject the §E defect classes
  (non-monotonic ladder, dropped germination_light, absurd DTM, em-dash, bad enum, missing region) and
  confirm each bounces before trusting the authoring.
- Footprint: EXACTLY the 3 new crops added; all 125 existing crops byte-identical; `source_catalog` +only
  genuinely-new ids; count 125 -> 128; COMPACT (no trailing newline). SHA-guarded splice via
  `tools/apply_patch.py` (per-crop or one batch -- decided in the plan).
- Release battery per protocol #6: `whole_crop_gate` each new crop PASS, `gate_all` 119/119,
  `calendar_coherence` 0, `timing_spine` 0, `release_verify` clean, source-truth sample.

## 9. Scope boundaries (explicitly OUT)

- **`broom-corn` (a *Sorghum*) and `sugar-cane` (*Saccharum*, perennial tropical)** -- different genera /
  basis, NOT part of this arc despite the "corn" name (kickoff #21). Sorghum + the other grains are the
  separate grains lane on `docs/crop_expansion_roadmap.md`.
- **No new gate, no new field, no new archetype.** Any temptation to build one is the over-engineering
  kickoff #21 already rejected.
- **No variety_detail flat schema / `hero_description`** on these crops (legacy variety shape; the
  Spec-2 roster rollout migrates varieties later).
- The garden-planner data-model arc (row_spacing / height / spread) is a separate arc.

## 10. Success criteria

- `field-corn`, `popcorn`, `flint-corn` each certified (`verified_gs_arc`): frost-anchored annual, direct-
  sown, `planting_layout: block` + `pollination_block_min_rows: 4`, the 9-stage dry-down `growth_stages`
  ladder with the `harvest`-id A40 anchor + `harvest_window_days` omitted, single-crop, 12 T1-anchored
  regional calendars (Option C humid advisories), legacy varieties naming the spectrum, all §E register
  fields present-or-null.
- Recorded adversarial RED proof per crop (defect classes bounce; canonical READ-ONLY during proofs).
- `whole_crop_gate` each PASS; `gate_all` 119/119; `calendar_coherence` 0; `timing_spine` 0;
  `release_verify` clean; footprint audit = exactly the 3 new crops, 125 others byte-identical, count 128.

## 11. Open items to confirm during authoring

- Final slugs (`field-corn` vs `corn` vs `dent-corn`; confirm against the master crop list).
- Final per-crop DTM synthesis bands (Trevor ratifies, as with sweet-corn/dry-bean).
- Final variety picks per crop (T1-sourced where possible; honest tier for seed-trade-only cultivars).
- Whether any region genuinely warrants a `heat_pause` (desert summers) vs a straight frost-anchored run.
