# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.4.1**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list (6c proved this: the kickoff's named scope differed from the live denominator -- see `phase_3_lettuce_m15_step6c_findings.md` FINDING 6c-1).
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push). Data change and state-only change both end with this ritual; never leave git behind.

---

## Canonical pointer
- **Current SHA:** `0dfd835a29636868fce6e4b180ec8ca5bbf3b654523636c4354c52d160ef23c8` (M15 lettuce Step 6c -- top-level/identity/yield/succession: 10 `_seasoned` fields lifted to cherry seasoned-depth (9 CP + 1 SP) + source/anchoring_url attachments. Two of three yield numbers corrected against T1 (peak_production 1-2wk->2-4wk regrowth; per_plant reframed bolt-bounded). claude.ai authored + applied; collateral-audited. Lettuce-only; 122 other crops + 13 sibling top-level keys byte-identical.)
- **Predecessor chain:** `1e19948c` (Step 6b container cluster) <- `61cddea3` (Step 6a core-biology depth-lift) <- `e27eec14` (freezer micro-addendum + gate refinement) <- `815efe62` (register-conversion completion) <- `8a1d8a50` (bolting) <- `ed495666` (Pass 2) <- `20f9fc2b` (Pass 1b) <- `327a2d5c` (Pass 1a) <- `582dbbad` (northern_tier).
- Every promote re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## Active work + exact next step
- **Crop in flight:** `lettuce-leaf` (crops index 33).
- **Done:** region-cell STRUCTURAL slice complete (all 10 region cells populated + shape-correct). Phase-0 register-conversion gap-fixes complete. Checklist synced to v1.4.1. **Step 6a complete** (15 core-biology `_seasoned`). **Step 6b complete** (7 container-cluster `_seasoned`). **Step 6c complete** (10 top-level/identity/yield/succession `_seasoned`: 9 CP + 1 SP; sources/URLs attached; yield numbers T1-corrected).
- **NEXT (claude.ai's lane):** **Step 6d** -- the seven compounds (`pests`, `diseases`, `growth_stages`, `notifications`, `weather_triggers`, `failure_diagnostics`, `tips_by_stage`), ~76 `_seasoned` prose fields. NOTE: `tips_by_stage.*.text_seasoned` already carry authored `_beginner` siblings (do not clobber); the other six compounds carry NULL `_beginner` (siblings come in Steps 7/8). Re-walk the LIVE Appendix-A denominator for 6d before authoring -- some compound `_seasoned` may already be near-bar.
- ⚠️ **The lettuce flag-flip is the LAST act of Step 11, ONLY on 0 violations. It is NOT next.** Steps 6d -> 7/8 (beginner siblings) -> 9 (dash gate) -> 11 (whole-crop validation) all precede any flip.

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- one crop becomes gold-standard / goes live. **Gate:** that crop's Step 11 returns 0 violations. Flags + status live under `verification_status` (NOT top level): `verification_status.launch_ready_core` / `launch_ready_seasoned` / `status`.
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce done; cherry + beefsteak still owe M16); shipped with a `zones{}` fallback.
3. **Authoring-model flip** -- carrots and every later crop authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`, perennial support) -- a FUTURE bump, **2.9+ (NOT 2.8)**. LATER milestone, after carrots. **Decoupled** from #2.

**Schema version lineage:** 2.7.5 (additive region scaffolding, done) -> **2.8 = register-suffix conversion (DONE; current `schema_version`)** -> future bumps re-number off 2.8. Region read-layer flip (#2) + perennial extension (#4) are **2.9+**. The region-primary spec's "2.8 breaking flip" label is stale; re-number to 2.9 when built.

## Live locked decisions / guardrails
- **Governing checklist: v1.4.1.** When checklist text and live dataset shape disagree, the **dataset is authoritative for what is true** -- flag the doc lag, do not author against fields that don't exist. The auto-derived denominator (Appendix A + register inventory) is authority over a kickoff's named list.
- **Lane split.** Dataset STRUCTURAL work = **Claude Code**. Biology windows from T1 sources + consumer copy (Steps 6/7/8) = **claude.ai**.
- **Per-crop pipeline (target):** Claude Code shell pass -> claude.ai fills biology gaps + copy -> Claude Code certifies (Step 11) -> Claude Code gated deletion.
- **Lettuce authors into `regions{}` this arc;** keep `zones{}` coherent until Phase C.
- **Inheritance is candidate, not verified (v1.4.1 §4).** Prior-phase attribution carries forward as candidate; verification status does NOT inherit; Step 4 / depth-lift side-by-side check vs live T1 always required. 6c is a fresh demonstration: the inherited `peak_production` "1-2 weeks" was unsourced and wrong (cut-cycle is 2-4 wk per umd/unl); corrected.
- **Succession-shape rule (spec §3b-i):** succession RULE lives ONCE in region-constant `plantings[]` (`track:"succession"`); app recomputes from `plantings[]` + live frost, IGNORES `resolved_by_zone`.
- **`year_round` encoding** for pauseless cells (declare-one-outcome).
- **`track` semantics:** `beginner` = shared MAIN calendar; `succession` = seasoned-only.
- **Register-conversion convention.** Register-bearing prose is `X_seasoned` + (`X_beginner` for CP, absent for SP); presence IS the visibility declaration. Canonical roster: `register_bearing_field_inventory_v1_0.md`. Bare-null-of-ruled-stem = ruled-empty PASS.
- **Temperature notation (NEW, 6c):** author user-facing prose in **"degrees F"** (matches the dominant 62 instances). Three competing forms exist dataset-wide (62 "degrees F" / 10 bare F / 5 °F) -- canonical normalization deferred to a Claude Code sweep (FINDING 6c-4). Do not introduce a fourth style.
- **Deletion gate (legacy `zones{}`):** delete ONLY at Phase C, per crop, AFTER region cell carries everything zones held + all consumers read region-first + round-trip + frost-input independence. **NEW (6c) precondition not yet met for `safe_sowing_note`:** it lives in `zones{}` only; `regions{}` carries none (it uses `plantings[].direct_sow[]`). Real migration item, not confirm-and-delete (FINDING 6c-2).

## Open items owed
- **Register-completeness gate -- BUILT + REFINED; standalone today.** STILL OWED (WORRY 3): wire into the per-crop shell pass as an admission HALT + re-run at Step 11. Shell pass built at cherry/beefsteak M16. Keep stop-and-ask (WORRY 4).
- **Gold-standard arc checklist amendments** (claude.ai's authoring lane): (1) per-step lane tags; (2) shell-pass-first structuring of Steps 4-5; (3) Step 11 flip-disambiguation guardrail; (4) generalized per-crop deletion gate.
- **Pipeline / operating-model doc -- TO BE DESIGNED.** Own session after lettuce is gold-standard.
- **Step 11 Appendix-A registration:** bolting register keys + ~26 register-conversion field rulings + (Pass 1b) succession strings + (Pass 2) se_gulf_month_resolution + 6b container conversion key-pairs. 6c added no new keys (edited existing `_seasoned` + attached sources/URLs).
- **Temperature-form normalization sweep** (FINDING 6c-4): single canonical form, Claude Code.
- **`safe_sowing_note` migration decision** (FINDING 6c-2): Phase C, Claude Code -- migrate verbatim into a regions field, or retire in favor of `plantings[].direct_sow[]`.
- **Deferred vocabulary session:** dataset-wide rename of `track` value `beginner` -> `main`.

## Inherited findings (unchanged)
- `finding_001` -- warm `zones{}` 8-11 SE-mis-sourced (legacy layer, own pass).
- na3d-na3g sourcing-sibling findings; `na3d_finding_003` cosmetic.
- **`rotation.note` 6a citation -- verify** (FINDING 6c-3): may reference uncatalogued `pnw_handbook`; re-confirm against catalog T1 at cross-anchor audit. `rotation.anchoring_urls` was `{}`; 6c attached `umn_ext`.
- Two-field predicate: `blocks_launch AND status != "resolved"` (never a bare count).

## Note on dataset size
Dataset is now **~10.6 MB minified** (grown with the regions layer; the old "4.6 MB minified" note is stale). This **exceeds the project-knowledge upload limit** -- dataset + `LATEST.txt` stay out-of-band (upload from `~/plant-dataset/` at chat start), never in project knowledge.

## Pointers
- **History (append-only recovery log):** `STATE_HISTORY.md`.
- **Checklist:** gold-standard arc checklist **v1.4.1** (+ 4 amendments owed above).
- **Specs:** region-primary schema shape spec v1.0 (§3b-i), `register_bearing_field_inventory_v1_0.md`, per_crop_verification_methodology v1.4(.1), v1.5 cold-zone fall-heat-floor, calendar-model spec, region-tip override spec + validator, tip-region authoring standard v1.1.
- **Findings (recent):** `phase_3_lettuce_m15_step6c_findings.md` (this session); `phase_3_lettuce_m15_step6a_findings.md`; northern_tier pass findings; bolting register-conversion addendum.
