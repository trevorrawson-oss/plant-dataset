# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.4.1**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push). Data change and state-only change both end with this ritual; never leave git behind (the hand-promote-uncommitted combination is what once turned a routine promote into a recovery).

---

## Canonical pointer
- **Current SHA:** `1e19948cc7afe2c1e498d3d28e514b134cefc1170a299c18f5650bfbbd6e2a9c` (M15 lettuce Step 6b -- container cluster: 6 `_seasoned` container fields authored (2 of them bare-null->`_seasoned`+null `_beginner` conversions: `shape_requirements`, `drainage.saucer_practice`) + `notes_seasoned` light-lift/dash-fix + container `sources`/`anchoring_urls` (umd/osu/uiuc/iastate/wvu, all admitted). claude.ai authored; Claude Code validated (dry-run all gates) + promoted. Lettuce-only; 122 other crops + 13 siblings byte-identical.)
- **Predecessor chain:** `61cddea3` (Step 6a core-biology depth-lift) <- `e27eec14` (freezer micro-addendum + gate refinement) <- `815efe62` (register-conversion completion) <- `8a1d8a50` (bolting) <- `ed495666` (Pass 2) <- `20f9fc2b` (Pass 1b) <- `327a2d5c` (Pass 1a) <- `582dbbad` (northern_tier).
- Every promote re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## Active work + exact next step
- **Crop in flight:** `lettuce-leaf` (crops index 33).
- **Done:** region-cell STRUCTURAL slice complete (Steps 4/5 + per-cell 5.5 gates; all 10 region cells populated + shape-correct). Phase-0 register-conversion gap-fixes complete (bolting `8a1d8a50` + register-conversion completion `815efe62` + freezer batch `e27eec14`). **Checklist synced to v1.4.1** (register-naming sync; resolved the pre-Phase-0 "no `_seasoned` suffix" language that contradicted the live explicit-suffix dataset -- dataset did not move). **Step 6a complete:** 15 core-biology `_seasoned` fields lifted (15/15 Appendix-A marked, 0 fail). **Step 6b complete:** 7 container-cluster `_seasoned` fields authored (incl. 2 bare-null->`_seasoned` conversions + null `_beginner` scaffolds; container sources/URLs set, all 5 admitted; dry-run-validated then promoted).
- **NEXT (claude.ai's lane):** **Step 6c** -- top-level/identity/yield/succession `_seasoned` + `safe_sowing_note_seasoned` ×5. Then 6d (compounds, ~76 fields). Step 6 progress: **22 of 119.**
- ⚠️ **The lettuce flag-flip is the LAST act of Step 11, ONLY on 0 violations. It is NOT next.** Steps 6 (remaining) -> 7/8 (beginner siblings) -> 11 (whole-crop validation) all precede any flip.

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- one crop becomes gold-standard / goes live. **Gate:** that crop's Step 11 returns 0 violations. *(The one a session jumped to early off "northern_tier done"; it only closed Step 5.5.)*
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce done; cherry + beefsteak still owe M16); shipped with a `zones{}` fallback.
3. **Authoring-model flip** -- carrots and every later crop authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`, perennial support) -- a FUTURE bump, **2.9+ (NOT 2.8)**. LATER milestone, after carrots. **Decoupled** from #2.

**Schema version lineage (so "2.8" isn't read two ways):** 2.7.5 = additive region scaffolding (Phase A, done) -> **2.8 = register-suffix conversion (DONE; current `schema_version`)** -> future bumps **re-number off 2.8** per the register inventory §9.1 ("the region-primary flip and perennial extension re-number; neither has shipped a schema artifact"). So the **region read-layer flip** (#2) and the **perennial extension** (#4) are **2.9+**, exact numbers pinned when each lands. NOTE: the region-primary spec's "## 4 Versioning: 2.7.5 -> 2.8 breaking flip" still labels the region flip "2.8" -- that label is stale (2.8 is taken); re-number to 2.9 when that flip is built (claude.ai's methodology lane).

## Live locked decisions / guardrails (in force; superseded ones live in history)
- **Governing checklist: v1.4.1** (register-naming sync of v1.4; field examples now `_seasoned`; denominator mechanism + Appendix A + gates + F5 register-vs-entry distinction all unchanged). When checklist text and live dataset shape disagree, the **dataset is authoritative for what is true** -- flag the doc lag, do not author against fields that don't exist.
- **Lane split.** Dataset STRUCTURAL work (region shell, calendar derivation, shape transforms, programmatic gates, gated deletion) = **Claude Code**. Biology windows from T1 sources (live web) + consumer copy (Steps 6/7/8) = **claude.ai**. *Note: checklist text edits are claude.ai's lane (doc authoring); the v1.4.1 sync was correctly Claude Code's because it touched no biology -- lane-by-content, not lane-by-filetype.*
- **Per-crop pipeline (target):** Claude Code shell pass (scaffold + reshape `zones{}` data + derive calendars + set conventions + run gates + emit PENDING-gap map) -> claude.ai fills biology gaps + writes copy -> Claude Code certifies (Step 11 re-walk) -> Claude Code gated deletion. Shell pass runs BEFORE biology.
- **Lettuce authors into `regions{}` this arc;** keep `zones{}` coherent until Phase C.
- **Succession-shape rule (spec §3b-i):** succession RULE lives ONCE in region-constant `plantings[]` (`track:"succession"`); `resolved_by_zone[z]` may hold materialized date-strings but NOT rule-bearing arm objects. App recomputes from `plantings[]` + live frost, IGNORES `resolved_by_zone`. Warm cells store rule-only (regenerable); northern_tier materializes per-zone (unstored `soil_temp_40f` anchor).
- **`year_round` encoding** for pauseless cells (declare-one-outcome: heat_pause / cold_pause / year_round).
- **`track` semantics:** `beginner` = shared MAIN calendar both audiences see (legacy misnomer for "main"); `succession` = seasoned-only.
- **Register-conversion convention.** Register-bearing prose is `X_seasoned` + (`X_beginner` for CP, absent for SP); presence IS the visibility declaration. Canonical roster: `register_bearing_field_inventory_v1_0.md`. NEW datapoints checked against it; an unruled prose field is a finding (bolting class). Bare-null-of-ruled-stem = ruled-empty PASS.
- **Deletion gate (legacy `zones{}`):** delete ONLY at Phase C, per crop, AFTER region cell carries everything zones held + all consumers read region-first + round-trip returns present verified value + frost-input independence.

## Open items owed
- **Register-completeness gate -- BUILT + REFINED; standalone today.** `plant-dataset/tools/register_completeness_gate.py` returns 0 unruled prose fields on the dataset (modulo 4 deferred §5 companions). **STILL OWED (WORRY 3):** wire it into the per-crop shell pass as an admission HALT + re-run at Step 11. Shell pass doesn't exist yet (built at cherry/beefsteak M16); wiring is a non-negotiable clause of that build. Keep stop-and-ask (WORRY 4).
- **Gold-standard arc checklist amendments** (claude.ai's authoring lane): (1) per-step lane tags; (2) shell-pass-first structuring of Steps 4-5; (3) Step 11 flip-disambiguation guardrail; (4) generalized per-crop deletion gate. *(v1.4.1 register-naming sync is DONE; these four remain.)*
- **Pipeline / operating-model doc -- TO BE DESIGNED** (cross-crop machine + full flip taxonomy + checklist-amendments list). Own session after lettuce is gold-standard.
- **Step 11 Appendix-A registration:** `succession_spring`/`succession_fall` (Pass 1b) + `se_gulf_month_resolution` (Pass 2) + `bolting.{note,prevention}` register keys + the ~26 register-conversion field rulings + the 6b container conversions (`container_notes.shape_requirements_*`, `drainage.saucer_practice_*`). *(6a added no new keys; 6b added 2 conversion key-pairs.)*
- **Optional forward finding:** machine-readable fall heat-floor clamp field (does NOT alone make north regenerable -- spring `soil_temp_40f` anchor unstored).
- **Deferred vocabulary session:** dataset-wide rename of `track` value `beginner` -> `main`.

## Inherited findings (unchanged)
- `finding_001` -- warm `zones{}` 8-11 SE-mis-sourced (legacy layer, own pass).
- na3d-na3g sourcing-sibling findings; `na3d_finding_003` cosmetic.
- Two-field predicate: `blocks_launch AND status != "resolved"` (never a bare count).

## Pointers
- **History (append-only recovery log):** `STATE_HISTORY.md`.
- **Checklist:** gold-standard arc checklist **v1.4.1** (+ 4 amendments owed above).
- **Specs:** region-primary schema shape spec v1.0 (§3b-i), `register_bearing_field_inventory_v1_0.md`, per_crop_verification_methodology v1.4(.1), v1.5 cold-zone fall-heat-floor, calendar-model spec, region-tip override spec + validator, tip-region authoring standard v1.1.
- **Findings (recent):** `phase_3_lettuce_m15_step6a_findings.md` (this session); `northern_tier_pass1a/1b_findings.md`; `lettuce_warm_cell_pass2_findings.md`; `bolting_register_conversion_addendum_findings.md`.
