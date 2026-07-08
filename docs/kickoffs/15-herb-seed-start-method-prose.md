# Kickoff: Seed-start METHOD prose for the seed-startable non-seed crops (register #6 follow-on)

**Created 2026-07-07** (register #6 seedling-light follow-on (b); flagged again after register #9/#10
wrapped the structured seed->harvest spine). Method: `docs/gs_cross_crop_field_addition_v0.md` is the
template for STRUCTURED fields; **this task is PROSE enrichment, not a new field**, so it is a lighter,
audit-first authoring pass (closer to the watering/register-5 per-crop authoring than a gated column pass).

## 0. The gap (register #6, verified in the data 2026-07-07)

Register #6 gave 10 non-seed crops a real `germination_light` value because they are realistically
home-seed-startable (the "no-home-seed-path" N/A rule SET them despite a transplant/division propagule).
But #6 was LIGHT-only by design: it recorded whether the seed needs light/dark to germinate, and left the
fuller "here is how to actually start it from seed" method (depth, temp, timing, weeks to transplant size,
the tricky bits) OUT of scope. So today these crops can tell a user the seed's light need without telling
them how to sow it.

**The target set (germination_light SET, propagule != seed):**

| crop | propagule | germination_light | germination_temp_f | weeks_indoors | sow_depth_inches |
|---|---|---|---|---|---|
| lavender | transplant | light_required | [70,70] | -- | none |
| rosemary | transplant | light_required | [70,70] | -- | none |
| oregano | transplant | light_required | [65,70] | -- | none |
| sage | transplant | neutral | [60,70] | -- | none |
| thyme | transplant | neutral | [70,70] | -- | none |
| mint | division | light_required | [60,70] | 6 | none |
| chives | division | neutral | [60,70] | 6 | none |
| bee-balm | division | neutral | [65,75] | 8 | none |
| echinacea | division | light_required | [65,70] | 8 | none |
| pawpaw | transplant | neutral | [] (empty) | -- | none |

All 10 have `germination_light` (and, except pawpaw, `germination_temp_f`) SET, but **`sow_depth_inches`
is `none` for all 10** and none carry a structured from-seed method.

## 1. BUT the gap is NOT uniform -- AUDIT FIRST (the leek/rollout lesson)

A prose scan already shows several of these are partly or fully covered, so **step 1 is a per-crop audit
of `start_method.notes` + germination `growth_stages` prose; author ONLY the genuine gaps.** Do not blanket-
author. What the scan found (confirm + extend it):
- **chives** -- ALREADY carries the actionable from-seed method ("grow readily from seed... slow, 2 to 3
  weeks... start indoors 6 to 8 weeks before last frost"). Likely NO fill needed.
- **lavender / rosemary** -- ALREADY explain the from-seed REALITY and steer to transplants ("does not come
  true from seed, 100 to 200 days" / "can take about three years, cultivars do not come true from seed").
  The honest question is whether to add any actionable how-to at all (see design Q2).
- **pawpaw** -- NO from-seed prose (the notes are the taproot/transplant narrative); and pawpaw seed-start
  is genuinely different (recalcitrant seed needing ~90 to 120 days cold-moist stratification). The hardest
  case; may deserve its own stratification paragraph or a scope decision (Q3).
- **oregano / sage / thyme / mint / bee-balm / echinacea** -- audit each; the division herbs
  (mint/bee-balm/echinacea) carry a `weeks_indoors`, so they have an indoor-start path already implied.

## 2. Design questions for the brainstorm (settle BEFORE authoring)

1. **Prose-only, or add a structured `sow_depth_inches` for the from-seed path?** `sow_depth_inches` is
   currently `none` for all 10 and A39 treats it as legit-N/A for a non-seed propagule (so adding it is
   NOT required and could muddy the propagule archetype). Recommendation: keep it PROSE (a from-seed
   sentence in `start_method.notes`, both registers), aligned to the existing `germination_light` (surface-
   sow for light_required; barely cover for neutral) + `germination_temp_f`. Do not add the structured
   field. Confirm.
2. **How much method for crops we deliberately steer AWAY from seed (lavender/rosemary/oregano)?** These
   are authored to recommend transplants because seed is slow/erratic/off-type. Adding a full "here is how
   to grow from seed" could undercut the honest steer. Recommendation: a SHORT, honest "if you do start
   from seed" clause (surface-sow because light aids germination, keep at ~70F, expect slow/erratic
   germination, grow on N weeks) that makes `germination_light` actionable WITHOUT overselling the seed
   path. Confirm the tone.
3. **pawpaw -- in scope, and how?** Its from-seed method is stratification-heavy (a different beast from
   the herbs). Options: (a) author a proper cold-moist-stratification paragraph; (b) keep it a transplant-
   only story and note seed is impractical (which would argue its `germination_light=neutral` is close to
   a no-home-seed-path case). Recommendation: (a) a short stratification note, since #6 SET it as
   seed-startable -- but confirm, and source it carefully (pawpaw seed is recalcitrant).
4. **Sourcing tier.** Per-crop T1 (extension `.edu` seed-starting pages + RHS) for the depth/temp/timing;
   own certified germination prose where it already states the method. Accuracy over cost (the #6 bar).
5. **Register-tracking.** This is a prose enrichment on 10 crops, not a cross-crop STRUCTURED field, so it
   is not a true register-# field. Track as a standalone authoring task, or add a `field_addition_register`
   candidate row (#11) for visibility. Confirm.

## 3. Method (audit-first authoring pass; amend-not-recert)

1. **superpowers:brainstorming FIRST** -- lock scope with Trevor (Q1-Q5: prose-only, the steer-away tone,
   pawpaw, sourcing, tracking). Write a short contract or fold the decisions into this kickoff.
2. **Per-crop audit** of all 10 (`start_method.notes_*` + germination-stage prose) -> a table of
   COVERED / PARTIAL / GAP. Only PARTIAL + GAP get authored.
3. **Author the gaps** from each crop's own prose + T1, dual-register (beginner + seasoned), aligned to
   the crop's existing `germination_light` + `germination_temp_f` + `weeks_indoors`. No em-dashes in
   consumer copy; American English; temps render `°F`. COMPACT canonical, SHA-guard EXACTLY the changed crops.
4. **Gate each batch:** `whole_crop_gate` on changed (dual-register completeness + dash/temp) +
   `register_completeness` + `seed_tray_gate`/`register_coverage`/`gate_all` (regression) + `release_verify`
   (source-truth + dash/degrees). No new structured field, so no new gate to build.
5. **State trio** at release (LATEST SHA+session; prepend STATE_HISTORY; SURGICAL CURRENT_STATE -- do NOT
   run gen_current_state.py, memory `current-state-md-drift`).
6. Trevor confirms every push. Commit each verified batch; hold the push.

## 4. Start here
- Confirm state: `shasum -a 256 crops_data_final.json` == `LATEST.txt` (currently `00e0b6b1`, register #10);
  `git log -1`; `git status -sb`.
- Read register #6's contract (`docs/seedling_light_contract.md`, esp. the N/A rule + follow-on (b)) and
  this file.
- Run the per-crop audit (step 2) to size the REAL gap before brainstorming tone/scope, then
  `superpowers:brainstorming` to lock it.

## Note
This is the LAST acknowledged narrative gap in the seed->harvest arc; the STRUCTURED spine + fills (#4-#10)
are complete + gate-locked (A39) on all 114 certified crops. This task is optional polish, not a spine hole.
