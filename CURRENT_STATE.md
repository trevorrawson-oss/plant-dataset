# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.4.1**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list (6c, 6d, and now Steps 7/8 all proved this: the kickoff's named scope can differ from the live denominator -- Steps 7/8 caught `thinning.tip` that no roster named).
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push). Data change and state-only change both end with this ritual; never leave git behind.

---

## Canonical pointer
- **Current SHA:** `7e9eeceb1bf15852c8a1e7a6a7a76ebaaa4b3955aa86b1b89104777f7d45886c` (M15 lettuce Steps 7/8 -- the `_beginner` siblings + the dual-voice coverage gate that flipped M13. **97 `_beginner` fields authored**: 30 top-level/dict CP + 66 per-entry compound CP + 1 flagged-CP gap (`thinning.tip`) that the structural gate caught and no roster named. Three corrected `_seasoned` fields (root-aphid treatment/prevention, downy-mildew cause) had their beginners authored against the CORRECTED biology. claude.ai authored + applied; collateral-audited. Lettuce-only; 122 other crops + all non-crop top-level keys byte-identical; **0 `_seasoned` changes** this session. Dual-voice coverage gate PASS whole-crop: 0 missing AND 0 null over a derived denominator of 130 CP fields.)
- **Predecessor chain:** `5224e13a` (Step 6d seven compounds) <- `0dfd835a` (6c top-level/identity/yield/succession) <- `1e19948c` (6b container) <- `61cddea3` (6a core-biology) <- `e27eec14` (freezer micro-addendum) <- `815efe62` (register-conversion completion) <- `8a1d8a50` (bolting) <- `ed495666` (Pass 2) <- `20f9fc2b` (Pass 1b) <- `327a2d5c` (Pass 1a) <- `582dbbad` (northern_tier).
- Every promote re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## Active work + exact next step
- **Crop in flight:** `lettuce-leaf` (crops index 33). **Top-level is a dict of 55 keys**; the register-bearing sibling surface is what matters here.
- **Done:** region-cell STRUCTURAL slice. Phase-0 register-conversion gap-fixes. Checklist synced to v1.4.1. **Step 6a/6b/6c/6d** (the seasoned depth-lift, complete). **Steps 7/8** (all `_beginner` siblings + the dual-voice coverage gate). The hole that flipped M13 would now return non-zero -- verified live (the gate caught `thinning.tip`).
- **NEXT: Step 9 (dash gate).** Whole-crop user-facing `--`/`°F`/en/em resolution. **This is a coordinated Claude Code sweep** bundled with FINDING 6c-4 (temperature-form normalization) + FINDING F-6d-2 (dataset-wide `--` → common-form) -- NOT a per-crop hand pass. Lettuce's untouched fields + ~122 other crops still carry `--`; the region `tip_overrides` `text_seasoned` carry legacy `°F`/"degree F" notation in scope for this sweep.
- ⚠️ **The lettuce flag-flip is the LAST act of Step 11, ONLY on 0 violations. It is NOT next.** Step 9 → Step 11 (whole-crop validation) precede any flip.

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- one crop becomes gold-standard / goes live. **Gate:** that crop's Step 11 returns 0 violations. Flags + status live under `verification_status` (NOT top level): `verification_status.launch_ready_core` / `launch_ready_seasoned` / `status`. (Steps 7/8 held these: both False, status `unverified`.)
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce done; cherry + beefsteak still owe M16); shipped with a `zones{}` fallback.
3. **Authoring-model flip** -- carrots and every later crop authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`, perennial support) -- a FUTURE bump, **2.9+ (NOT 2.8)**. LATER milestone, after carrots. **Decoupled** from #2.

**Schema version lineage:** 2.7.5 (additive region scaffolding, done) -> **2.8 = register-suffix conversion (DONE; current `schema_version`)** -> future bumps re-number off 2.8. Region read-layer flip (#2) + perennial extension (#4) are **2.9+**. The region-primary spec's "2.8 breaking flip" label is stale; re-number to 2.9 when built.

## Live locked decisions / guardrails
- **Governing checklist: v1.4.1.** When checklist text and live dataset shape disagree, the **dataset is authoritative for what is true** -- flag the doc lag, do not author against fields that don't exist. The auto-derived denominator (Appendix A + register inventory) is authority over a kickoff's named list. **Steps 7/8 is the strongest demonstration yet:** the dual-voice gate MUST be a STRUCTURAL crop walk, not a hand-built field list. The first gate version (a hand list) silently omitted `thinning.tip` + region `tip_overrides` -- the exact M13 failure mode. The reusable gate is `dual_voice_gate_v2.py`.
- **Lane split.** Dataset STRUCTURAL work = **Claude Code**. Biology windows from T1 sources + consumer copy (Steps 6/7/8) = **claude.ai**.
- **Per-crop pipeline (target):** Claude Code shell pass -> claude.ai fills biology gaps + copy -> Claude Code certifies (Step 11) -> Claude Code gated deletion.
- **Lettuce authors into `regions{}` this arc;** keep `zones{}` coherent until Phase C.
- **Inheritance is candidate, not verified (v1.4.1 §4).** Prior-phase attribution carries forward as candidate; verification status does NOT inherit; side-by-side check vs live T1 always required.
- **Pest/disease = highest-scrutiny cluster (full cherry-anchor rigor).** Beginner siblings for the 3 corrected pest/disease fields were authored against the CORRECTED `_seasoned` text (cultural-control-not-spray; resistance-not-"LR"; oomycete-not-fungus).
- **Micro-strings are at-bar-by-nature (depth-exempt) for the SEASONED lift, but DO take a `_beginner` sibling.** `log_prompt`, `failure_diagnostics.label`, notification/weather `title` were PASS (not lifted) at 6d -- but Steps 7/8 still author their `_beginner` siblings (they are CORE-PROSE-NEEDS-SIBLING, just short). The depth-exemption is about the seasoned-lift tally, not the sibling requirement.
- **`cause_beginner` ruling (Trevor 2026-05-30):** register transform, same biological content, plainer grammar. May be byte-identical to `_seasoned` where the seasoned carries no jargon. Lettuce authored all 5; for cherry/beefsteak this is M16 `gs_exemplar_finding_004`.
- **`thinning.tip` / `indoor_cycle.tip` flagged-CP (register inventory §7):** `thinning.tip` flag now CONFIRMED-CP -- the lettuce anchor authored a clean beginner sibling. `indoor_cycle.tip` confirms at its archetype anchor.
- **Region `tip_overrides` shape (registered, v1.4 pre-commit honored):** `regions.<id>.tip_overrides.<stage>[]` each with `text_seasoned` + `text_beginner` + `overrides_tip_id` + `sources` + `anchoring_urls` + `added_in` + `evidence_tier`. CORE-PROSE-NEEDS-SIBLING; covered by the structural dual-voice gate; in Step 9's dash scope.
- **Succession-shape rule (spec §3b-i):** succession RULE lives ONCE in region-constant `plantings[]` (`track:"succession"`); app recomputes from `plantings[]` + live frost, IGNORES `resolved_by_zone`.
- **`year_round` encoding** for pauseless cells (declare-one-outcome).
- **`track` semantics:** `beginner` = shared MAIN calendar; `succession` = seasoned-only.
- **Register-conversion convention.** Register-bearing prose is `X_seasoned` + (`X_beginner` for CP, absent for SP); presence IS the visibility declaration. Canonical roster: `register_bearing_field_inventory_v1_0.md`. Bare-null-of-ruled-stem = ruled-empty PASS.
- **Temperature notation (6c):** author user-facing prose in **"degrees F"**. Three competing forms exist dataset-wide -- canonical normalization deferred to a Claude Code sweep (FINDING 6c-4). Do not introduce a fourth style.
- **Dash convention (6d):** the project is moving OFF the `--` literal to **common form** (commas / restructure) for user-facing copy -- Trevor ratified. Fields authored/rewritten in a session use common form immediately (Steps 7/8: 0 `--` in 97 authored fields). The **dataset-wide** `--` → common-form conversion is a mechanical Claude Code sweep (**FINDING F-6d-2**), bundled with FINDING 6c-4 + Step 9.
- **Deletion gate (legacy `zones{}`):** delete ONLY at Phase C, per crop, AFTER region cell carries everything zones held + all consumers read region-first + round-trip + frost-input independence. `safe_sowing_note` precondition not yet met (FINDING 6c-2).

## Open items owed
- **Register-completeness / dual-voice gate -- BUILT + REFINED (now structural, `dual_voice_gate_v2.py`); standalone today.** STILL OWED (WORRY 3): wire into the per-crop shell pass as an admission HALT + re-run at Step 11. Shell pass built at cherry/beefsteak M16. Keep stop-and-ask (WORRY 4). **NEW emphasis:** the gate must be the STRUCTURAL walk, not a field list -- ship `dual_voice_gate_v2.py`'s walk logic into the pipeline `rubric.md`, not a transcribed roster.
- **Gold-standard arc checklist amendments** (claude.ai's authoring lane): (1) per-step lane tags; (2) shell-pass-first structuring of Steps 4-5; (3) Step 11 flip-disambiguation guardrail; (4) generalized per-crop deletion gate. **NEW (5):** Step 8 gate wording must mandate a structural crop walk and explicitly name `thinning.tip` + region `tip_overrides` as fields a hand list drops.
- **Pipeline / operating-model doc -- TO BE DESIGNED.** Own session after lettuce is gold-standard.
- **Step 11 Appendix-A registration:** bolting register keys + ~26 register-conversion field rulings + succession strings + se_gulf_month_resolution + 6b container conversion key-pairs + **the Steps 7/8 `_beginner` keys (97 new populated; see registration delta deliverable)** + region `tip_overrides` leaf-keys (now registered).
- **Temperature-form normalization sweep** (FINDING 6c-4): single canonical form, Claude Code.
- **Dataset-wide `--` → common-form sweep** (FINDING F-6d-2): Claude Code; bundle with 6c-4 + Step 9 = the Step 9 work.
- **`safe_sowing_note` migration decision** (FINDING 6c-2): Phase C, Claude Code.
- **Deferred vocabulary session:** dataset-wide rename of `track` value `beginner` -> `main`.
- **Companions reconciliation session (§5):** the array-level register split (`good_beginner_seasoned`/`good_seasoned`/`bad_seasoned`, `why` fields). Lettuce carries 3 populated `why_seasoned` with null `why_beginner` -- correctly OUT OF SCOPE until this session runs.

## Inherited findings (unchanged)
- `finding_001` -- warm `zones{}` 8-11 SE-mis-sourced (legacy layer, own pass).
- na3d-na3g sourcing-sibling findings; `na3d_finding_003` cosmetic.
- **`rotation.note` 6a citation -- verify** (FINDING 6c-3): may reference uncatalogued `pnw_handbook`; re-confirm against catalog T1 at cross-anchor audit.
- Two-field predicate: `blocks_launch AND status != "resolved"` (never a bare count). **0 unresolved blockers** post-Steps78.

## Step 6 progress
- **79 of 119 lifted** -- UNCHANGED by Steps 7/8 (the seasoned-lift tally does not move when authoring `_beginner` siblings).
- Remaining Step 6: any residual top-level CP not yet at-bar (`companions.*` deferred to §5 reconciliation; `det_indet.detail` does not exist on lettuce). Then Step 9 → Step 11.

## Steps 7/8 result (this session)
- **97 `_beginner` authored** (30 top-level/dict + 66 compound per-entry + 1 `thinning.tip` flagged-CP gap the structural gate caught).
- **Dual-voice coverage gate PASS:** denominator 130 CP fields w/ seasoned prose, populated 130, missing_keys 0, null_values 0. SP-no-sibling 158, ruled-empty 10, out-of-scope (companions split) 7.
- **5 lettuce `_beginner` still null, all correct:** 3 `companions.*.why_beginner` (§5 deferred), 1 `start_method.hardening_off` (boolean stem), 1 `container_notes.overwintering.approach` (ruled-empty).

## Note on dataset size
Dataset is **~10.6 MB minified** (10,632,328 bytes at `7e9eeceb`). This **exceeds the project-knowledge upload limit** -- dataset + `LATEST.txt` stay out-of-band (upload from `~/plant-dataset/` at chat start), never in project knowledge.

## Pointers
- **History (append-only recovery log):** `STATE_HISTORY.md`.
- **Checklist:** gold-standard arc checklist **v1.4.1** (+ 5 amendments owed above).
- **Specs:** region-primary schema shape spec v1.0 (§3b-i), `register_bearing_field_inventory_v1_0.md`, per_crop_verification_methodology v1.4(.1), v1.5 cold-zone fall-heat-floor, calendar-model spec, region-tip override spec + validator, tip-region authoring standard v1.1.
- **Reusable gate:** `dual_voice_gate_v2.py` (structural whole-crop dual-voice coverage -- ship this logic into the pipeline rubric, not a hand roster).
- **Findings (recent):** `phase_3_lettuce_m15_steps78_findings.md` (this session) + `m15_steps78_dual_voice_coverage_report.md` + `m15_steps78_appendix_a_registration_delta.md`; `phase_3_lettuce_m15_step6d_findings.md`; `phase_3_lettuce_m15_step6c_findings.md`.
