# KICKOFF -- Zucchini / Courgette Steps 6-8 (consumer prose + the 7 compounds)

You are picking up **zucchini-courgette** for its FINAL authoring leg before certification. Steps 1-3 (biology /
varieties / companions / succession_policy), Step 3.5 (region shells), and Steps 4-5.5 (all 10 regions filled:
windows + calendars + succession + the A8 `successions_realized`) are DONE and released. Your lane is **Steps
6-8: the consumer prose + the 7 compounds** -- the depth-lifted seasoned prose, every beginner sibling, and the
pest/disease/growth-stage/tip/notification surfaces. When the gate residual reaches the deferred-zero, zucchini
hands back to Claude Code for Step 9 (dash/temp sweep) + Step 11 (cert flip). `lettuce-leaf` is the reference GS
crop; the cherry / green-beans seasoned-depth bar is the quality target.

Operating model unchanged: you AUTHOR, Claude Code RELEASES (gates + promote). Don't introduce a claim with no T1
page behind it.

> **DRAFT for Trevor to voice + send.** Structural frame + the COMPUTED worklist assembled by Claude Code; the
> final prompt is yours.
> **SCOPE: Steps 6-8 ONLY.** Region WINDOWS/calendars/succession are DONE (Steps 4-5.5) -- do NOT touch them.
> The cert flip (`verification_status`) is Step 11 (Claude Code). Do NOT set it.

---

## 0. Preflight (Step 0) -- do first, STOP on mismatch
- `shasum -a 256 ~/plant-dataset/crops_data_final.json` MUST equal `LATEST.txt` == `642f48903eed2754c9d8f2bda2cfe32ce48dd46436d4d764d7100ffd6d98d8b7`. Mismatch => STOP and reconcile.
- Confirm the slice's crop SHA per `SLICE_INTEGRITY.md`: `fd8174de…`.
- Read, in order: `CURRENT_STATE.md` + `STATE_HISTORY.md` (the two newest entries are this crop's Steps 4-5.5 release + Step 3.5); the **v2.0 checklist** Steps 6 / 7 / 8 + Appendix A (the auto-derived prose-field denominator) + the dual-register v1.1 five rules. **Re-derive your arc position from the checklist, not this prose.**

## 1. Files (the bundle)
**Upload:** this doc; `zucchini-courgette_current_slice.json` (the post-4-5.5 base -- regions FILLED, the 6-8 prose surface NULL); `SLICE_INTEGRITY.md`; `zucchini_sources_and_catalog.json` (the 122-parent catalog + zucchini's `sources_summary` -- reuse parents, mint specific-page sub-ids under a trusted parent); `LATEST.txt` / `CURRENT_STATE.md` / `STATE_HISTORY.md`. (No `zone_frost_data` -- 6-8 is prose, the windows are already authored in the slice.)
**Project knowledge:** the v2.0 checklist + dual-register v1.1 + voice methodology are already loaded. No design spec needed.

## 2. What these steps own (the checklist bars)
- **Step 6 -- Seasoned depth-lift:** every `X_seasoned` prose field meets the cherry seasoned-depth bar -- **mechanism explained**, **regional variation acknowledged where it exists**, **numeric specificity where biology supports it**, **honest about complexity/tradeoffs**. New claims carry T1 backing + anchoring URLs.
- **Step 7 -- Beginner siblings (top-level + dict-sub-field):** the `_beginner` sibling for every top-level / dict CP prose field, DERIVED FROM the depth-lifted `_seasoned` (so siblings don't drift against not-yet-final seasoned text). Dual-register v1.1's five rules. Pair `_beginner`/`_seasoned` only where the divergence is substantive; a single-term gloss makes the string universal-plain.
- **Step 8 -- Beginner siblings (per-entry on the 7 compounds) + THE DUAL-VOICE COVERAGE GATE:** every `audience:"core"` compound entry has all its required `_beginner` siblings populated + non-null; `audience:"seasoned"` entries carry prose but no beginner sibling. **The gate (Claude Code re-runs at release): for every core-prose-needs-sibling field across the WHOLE crop, the sibling is present AND non-null -- 0 missing keys AND 0 null.**

## 3. THE COMPUTED WORKLIST (walk the crop -- do NOT hand-enumerate; peach/apple shipped CERTIFIED with null fields from a hand list)
**78 register-prose fields currently NULL** + **7 empty compounds**. The release-lane sweep (`register_fill_gate` + the A12 compound gate) re-runs this to 0; author the FULL set, not a remembered subset.

**Register-prose nulls, by block (each is a `_seasoned`/`_beginner` pair unless noted):**
- **`region_notes_*` -- all 10 regions** (northern_tier, se_gulf, ca_interior, ca_north_coast, ca_south_coast, ca_desert, warm_arid, low_desert_az, fl_peninsula, hawaii_tropical): the region-specific growing guidance, DERIVED from the windows/calendars already authored at 4-5.5 (the spring-vs-spring+fall structure, the inverted FL season, the desert mid-summer `heat_pause` gap, the hawaii bounded-continuous).
- **`fertilizer`** -- `amount` / `notes` / `notify_message` / `npk_hint` pairs. **Author against the MODERATE-feeder profile** locked at Steps 1-3 (UMD "Medium requirement for nutrients"; NOT heavy -- the legume green-beans contrast is to a LIGHT feeder, zucchini sits in the middle): incorporate at planting + side-dress as vines run / at flowering; the "consistent moisture + don't over-N" nexus. Wire `fertilizer.stage_id` to a real `growth_stages` id.
- **`watering`** -- `frequency` / `amount` / `method` / `signs_overwater` / `signs_underwater` / `method_note` / `critical_periods` pairs. Keep the **base-water / dry-foliage / powdery-mildew nexus** (the `watering_method:base` + `drought_tolerance:low` enums are already set); ~1 in/week, critical at flowering/fruit-set; the misshapen-fruit-from-inadequate-water beat.
- **`container_notes` deep prose** -- `notes` / `soil_mix.type` / `soil_mix.amendments` / `watering_adjustment` / `fertilizer_adjustment` / `self_watering_notes` pairs + `overwintering.approach` + `shape_requirements`. **`overwintering.applicable:false`** (zucchini is `lifecycle:annual`, frost-killed) -> N/A PROSE, never null. `shape_requirements` was DROPPED at Steps 1-3 -> author it now as a REAL dual-voice pair (a big sprawling plant needs a wide/deep container).
- **`rotation`** -- `rotation_years` (int) + `avoid_after` + `note` pairs. Cucurbitaceae; squash bug / vine borer / soilborne disease buildup -> a 2-3 yr return; avoid following other cucurbits (cucumber/melon/squash). Source the years.
- **`storage`** -- `room_temp` / `fridge` / `freezer` / `notes` pairs. Summer squash is tender, NOT a keeper: a few days at room temp, ~1 week fridge in a perforated bag, freezes shredded/blanched for cooking.
- **`yield_expectations`** -- `per_plant` / `peak_production` / `first_year_note` pairs + `factors_seasoned` (single-register list). The prolific "pick young, pick every 1-2 days at peak" beat; a couple plants feed a household.
- **`description_*`**, **`harvest_ready_*`** (the harvest cue: 6-8 in, glossy, before seeds harden / it turns to a marrow), **`moon_phase_preference.source_note_seasoned`** (N/A prose -- no-evidence field, like carrot; never null).

## 4. The 7 compounds (Step 8 + A12 rendering-conformance)
Author each with `audience` tags + the dual-register per-entry siblings. **A12 HARD constraint:** `tips_by_stage` is a **dict keyed by `growth_stages[].id`**, each value a LIST of tip objects using **`text_seasoned`/`text_beginner`** (NOT `tip_*`); a tip renders ONLY if its key is a real stage id + the field is `text_*` + the list is non-empty. Define `growth_stages[].id` FIRST, then key `tips_by_stage` + `fertilizer.stage_id` + `notifications` to those ids.
- **`growth_stages`** -- the zucchini arc: germination -> seedling -> established/vining -> flowering (the monoecious male-then-female beat) -> harvest (pick-young, pick-often) -> end_of_season. Each: `what_to_look_for` / `user_action` / `log_prompt` (+ `_beginner`). The ids are the load-bearing keys for tips + fertilizer + notifications.
- **`pests`** -- LEAD **squash vine borer** (the signature killer -- wilting + frass at the base; the mid-season borer is WHY the fall succession exists), then **squash bug**, **cucumber beetle** (+ aphids if T1-supported). Each: `symptoms` / `cause` / `organic_treatment` / `prevention` (+ `_beginner` incl. **`cause_beginner`**).
- **`diseases`** -- LEAD **powdery mildew** (the base-water nexus; resistant varieties; airflow), then **bacterial wilt** (cucumber-beetle-vectored -- ties to the pest entry). Same 4 fields + `cause_beginner`.
- **`failure_diagnostics`** -- the 4-slot template (`label` / `what_happened` / `next_season_tip` + the cause): **poor pollination** (small fruit yellowing/rotting at the blossom end -- ties to the `self_fertile:true` + `pollinator_notes` already authored), **fruit hidden until oversized** (the marrow), **borer collapse**, **mildew defoliation**.
- **`notifications`** + **`weather_triggers`** -- `title` / `body` (+ `_beginner`); machinery (`action`/`condition`/`severity`/`trigger_type`/`offset_from`) carries no sibling. Load-bearing: the borer-watch + succession-sow reminders; a frost-warning trigger.

## 5. Block-coherent authoring + anchoring (the cert-ready bot template)
Author each TOUCHED block as a UNIT -- the `_seasoned`/`_beginner` pairs + close its structured nulls + **ANCHOR the block** (`sources` + `anchoring_urls`) in ONE pass. Anchoring is REQUIRED `launch_ready_core` cert work (Step 11), not optional polish -- close it now while the sources are open. **N/A fields get N/A PROSE, never null** (`register_fill_gate` rejects null). Surface any beyond-prose change (retro-anchoring, structured nulls closed) as a LABELED sub-section for the release review.

## 6. Copy + sourcing rules
T1 only (seed-company / almanac = T2, evidence-log only). **No em dashes / no `--` in any consumer string; `°F` symbol (never "degrees F"); American English; "zucchini" / "squash" lowercase.** Backend prose (`*_basis`, `source_quote`, provenance) MAY spell "degrees F." CP fields are suffixed siblings (`parent.X_seasoned` / `parent.X_beginner`, never a nested `parent.X.{X_seasoned}`).

## 7. Deliverable
Hand back the authored slice (or a patch) + the post-author crop SHA + a LABELED list of any new source mints / retro-anchoring + a note of any N/A-prose ruling. Claude Code preflights vs `LATEST.txt` (`642f4890`), applies, runs `whole_crop_gate` (the residual should fall to **0** -- region_notes filled, all 7 compounds populated, dual-voice 0 missing / 0 null, A12 tips rendering-conformant) + `register_completeness` + `register_fill` + `release_verify`, and promotes. Then **Step 9** (whole-crop dash/temp sweep) -> **Step 11 cert** (the independent T1 source-fidelity WebFetch -- which also resolves the 3 Steps-4-5.5 carry-forwards: the hawaii `year_round` upgrade vs CTAHR B-91, the warm_arid z8 NMSU CR457 confirm, the desert `heat_pause` already A5-confirmed -- then the flip).
