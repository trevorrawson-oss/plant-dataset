# Kickoff #16 -- plant-app: pull the migrated microgreens growth_stages

**For:** a plant-app session (this is a WEBSITE/app concern, done in that repo).
**Trigger:** the dataset change below lands via the plant-astro submodule bump (gated on Trevor).
**Owner of the data change:** plant-dataset, canonical `86ccf8c3` -> `9d1193eb` (2026-07-08).

## What changed in the dataset

The 8 microgreens-family crops from the 2026-07-02 indoor batch had their `growth_stages`
migrated from an older non-standard per-stage shape to the standard shape every other
certified crop already uses.

Crops: `arugula-microgreens`, `broccoli-microgreens`, `cilantro-microgreens`,
`microgreens-mix`, `pea-shoots`, `radish-microgreens`, `sunflower-sprouts`, `wheatgrass`.

- **Old per-stage keys:** `stage_id`, `name_seasoned`, `name_beginner`,
  `description_seasoned`, `description_beginner`, `day_range_from_sow`.
- **New per-stage keys (standard, matches cherry-tomato/beefsteak):** `id`, `name`,
  `day_range_from_sow`, `audience`, `user_action_beginner`, `what_to_look_for_beginner`,
  `log_prompt_beginner`, `user_action_seasoned`, `what_to_look_for_seasoned`,
  `log_prompt_seasoned`.
- **Unchanged:** every stage `id` value (`sow`/`germination`/`blackout`/`light`/`harvest`)
  and every `day_range_from_sow` value. Only the copy/title fields changed shape.
- **Card title** (`name`) is a single, non-toggling label: `Sow`, `Germination`,
  `Blackout`, `Light`, `Harvest` (uniform across all 8).

## Why this exists

Before the migration these 8 rendered journey cards with **blank titles and empty
"Do this"/"Look for" sections**, because the renderer reads the standard keys (`name`,
`user_action_*`, `what_to_look_for_*`) which the old shape lacked. plant-app patched
around it on 2026-07-07 (**commit `a3a0145`**). With the real data in place, that
workaround can be **reverted** so the cards render authored titles + copy.

## What the plant-app session must do

1. Update the embedded dataset (plant-astro submodule bump to `9d1193eb`, per Trevor).
2. `npm run build:guides` -- regenerate the guide/journey artifacts from the new data.
3. Re-check the **promotion checklist's count assertions** (stage/field counts for these
   8 crops now match the standard shape; update any hard-coded expectations if needed).
4. `npx jest` -- confirm the suite is green against the rebuilt guides.
5. Revert / retire the `a3a0145` blank-title workaround once real titles + copy render.

## Verification already done on the dataset side

`gate_all` PASS (114/114), `whole_crop_gate` PASS x8, `register_completeness` PASS,
`timing_spine` 0/0, `temp_scan` 0, `release_verify` clean, 0 em-dashes in the new copy.
Footprint: EXACTLY the 8 crops' `growth_stages`; all else byte-identical; count 124; COMPACT.
Patch: `tools/batches/microgreens_growth_stages_migration.json`.
