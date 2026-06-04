# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.4.1**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list (6c, 6d, Steps 7/8, and now Step 9 all proved this: the kickoff's named scope can differ from the live denominator -- Step 9 derived its user-facing set by a structural walk because the authority docs are claude.ai-side only).
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push). Data change and state-only change both end with this ritual; never leave git behind.

---

## Canonical pointer
- **Current SHA:** `da4b8bc51dc935b0efce115a6405cb7fb82e3e927e520767757fff2e8062dec2` (M15 lettuce Step 9 -- the dash gate + dataset-wide temperature normalization. **286 user-facing leaves changed: 269 temperature conversions across 56 crops + 17 lettuce dash conversions.** Pure mechanical/structural normalization -- NO biology, NO new copy. Temperature is now the **degree symbol `°F`** dataset-wide (Trevor reversed FINDING 6c-4); lettuce's 17 user-facing `--` resolved per-sense (comma/colon/semicolon, punctuation-only). Backend leaves changed 0; value-preservation 0 failures; dual-voice regression PASS (lettuce 130 `_beginner` present, unchanged); flip-guard holds. Lettuce-only for dashes; temperature dataset-wide.)
- **Predecessor chain:** `7e9eeceb` (Steps 7/8 -- 97 `_beginner` siblings + dual-voice gate) <- `5224e13a` (Step 6d seven compounds) <- `0dfd835a` (6c top-level/identity/yield/succession) <- `1e19948c` (6b container) <- `61cddea3` (6a core-biology) <- `e27eec14` (freezer micro-addendum) <- `815efe62` (register-conversion completion) <- `8a1d8a50` (bolting) <- `ed495666` (Pass 2) <- `20f9fc2b` (Pass 1b) <- `327a2d5c` (Pass 1a) <- `582dbbad` (northern_tier).
- Every promote re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## Active work + exact next step
- **Crop in flight:** `lettuce-leaf` (crops index 33). **Top-level is a dict of 14 keys** (the 14th is `region_source_map`).
- **Done:** region-cell STRUCTURAL slice. Phase-0 register-conversion gap-fixes. Checklist synced to v1.4.1. **Step 6a/6b/6c/6d** (seasoned depth-lift). **Steps 7/8** (`_beginner` siblings + dual-voice coverage gate). **Step 9** (dash gate -- lettuce user-facing `--` = 0; temperature-form gate -- dataset-wide `degrees F`/bare-F = 0, `°F` sole form).
- **NEXT: Step 10** (cross-field consistency + copyright/attribution audit), **then Step 11** (whole-crop validation; re-runs every prior gate independently against live data).
- ⚠️ **The lettuce flag-flip is the LAST act of Step 11, ONLY on 0 violations. It is NOT next.** Step 10 -> Step 11 precede any flip.

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- one crop becomes gold-standard / goes live. **Gate:** that crop's Step 11 returns 0 violations. Flags + status live under `verification_status` (NOT top level): `verification_status.launch_ready_core` / `launch_ready_seasoned` / `status`. (Step 9 held these: both False, status `unverified`.)
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce done; cherry + beefsteak still owe M16); shipped with a `zones{}` fallback.
3. **Authoring-model flip** -- carrots and every later crop authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`, perennial support) -- a FUTURE bump, **2.9+ (NOT 2.8)**. LATER milestone, after carrots. **Decoupled** from #2.

**Schema version lineage:** 2.7.5 (additive region scaffolding, done) -> **2.8 = register-suffix conversion (DONE; current `schema_version`)** -> future bumps re-number off 2.8. Region read-layer flip (#2) + perennial extension (#4) are **2.9+**. The region-primary spec's "2.8 breaking flip" label is stale; re-number to 2.9 when built.

## Live locked decisions / guardrails
- **Governing checklist: v1.4.1.** When checklist text and live dataset shape disagree, the **dataset is authoritative for what is true** -- flag the doc lag, do not author against fields that don't exist. The auto-derived denominator (Appendix A + register inventory) is authority over a kickoff's named list. **Step 9 demonstration:** the checklist + register inventory live ONLY in claude.ai project knowledge (not on local disk), so Step 9's user-facing field set was derived by a STRUCTURAL walk of the dataset -- classifying every token-carrying leaf -- exactly the "derive, don't transcribe" principle.
- **Lane split.** Dataset STRUCTURAL/MECHANICAL work = **Claude Code** (Step 9 was here). Biology windows from T1 sources + consumer copy authoring (Steps 6/7/8) = **claude.ai**. Per-sense dash resolution is editorial judgment on EXISTING copy (punctuation-only), done here for lettuce; full per-crop dash work rides with each crop's arc.
- **Per-crop pipeline (target):** Claude Code shell pass -> claude.ai fills biology gaps + copy -> Claude Code certifies (Step 11) -> Claude Code gated deletion.
- **Lettuce authors into `regions{}` this arc;** keep `zones{}` coherent until Phase C.
- **Inheritance is candidate, not verified (v1.4.1 §4).** Prior-phase attribution carries forward as candidate; verification status does NOT inherit; side-by-side check vs live T1 always required.
- **Pest/disease = highest-scrutiny cluster (full cherry-anchor rigor).**
- **Micro-strings are at-bar-by-nature (depth-exempt) for the SEASONED lift, but DO take a `_beginner` sibling.**
- **`cause_beginner` ruling (Trevor 2026-05-30):** register transform, same biological content, plainer grammar. May be byte-identical to `_seasoned` where the seasoned carries no jargon.
- **TEMPERATURE NOTATION -- CANONICAL `°F` (Trevor 2026-06-04, reverses 6c-4).** User-facing temperature renders as the **degree symbol `°F`** (e.g. `75°F`, `70-85°F`), no space before the symbol. Step 9 converted `degrees F`/`degree F`/bare-F INTO `°F` dataset-wide in user-facing leaves; FINDING 6c-4 RESOLVED. 6c-4 had picked spelled-out "degrees F" only as the then-dominant form; Trevor prefers the symbol. **Do NOT re-author copy in "degrees F".** Backend `synthesis_note`/`design_note`/`uscrn_validation` retain whatever form (not user-facing). See memory `temp_form_degree_symbol`.
- **DASH CONVENTION -- per-sense, per-crop (F-6d-2 re-scoped 2026-06-04).** User-facing `--` resolves to common form by SENSE: aside -> comma; label/title -> colon; joined independent clauses -> semicolon; restructure avoided in mechanical passes (it breaks value-preservation). **This is editorial judgment, done per-crop with the crop's arc** -- NOT a blind dataset-wide find-replace. Lettuce's 17 done at Step 9 (punctuation-only). The other 122 crops still carry `--` (5,360 user-facing occurrences) -- **FINDING F-6d-2 STILL OPEN**, executed as each crop is arc'd.
- **Deletion gate (legacy `zones{}`):** delete ONLY at Phase C, per crop, AFTER region cell carries everything zones held + all consumers read region-first + round-trip + frost-input independence. `safe_sowing_note` precondition not yet met (FINDING 6c-2).
- **Succession-shape rule (spec §3b-i):** succession RULE lives ONCE in region-constant `plantings[]` (`track:"succession"`); app recomputes from `plantings[]` + live frost, IGNORES `resolved_by_zone`.
- **`year_round` encoding** for pauseless cells (declare-one-outcome).
- **`track` semantics:** `beginner` = shared MAIN calendar; `succession` = seasoned-only.
- **Register-conversion convention.** Register-bearing prose is `X_seasoned` + (`X_beginner` for CP, absent for SP); presence IS the visibility declaration. Bare-null-of-ruled-stem = ruled-empty PASS.

## Step 9 result (this session)
- **286 user-facing leaves changed** = 269 temperature conversions (56 crops) + 17 lettuce dash conversions.
- **Gates:** lettuce dash residual 0 (PASS); temperature-form residual `degrees F`=0 / bare-F=0, `°F` sole form (PASS dataset-wide); dual-voice regression lettuce 130 `_beginner` present unchanged (PASS); flip-guard `(False,False,unverified)` (PASS).
- **103 dataset-wide bare-F conversions** all hand-vetted as genuine temperatures (negatives, ranges, `60F+`); 0 false positives.
- **Backend untouched:** 0 backend/exempt leaves changed; value-preservation 0 failures (temp notation-only; dash single-`--`->punctuation swap, no word/case change).

## Open items owed
- **FINDING F-6d-2 (OPEN, re-scoped):** dataset-wide `--` -> common form is per-crop per-sense editorial work, NOT a blind sweep. Lettuce done; 122 crops (~5,360 user-facing `--`) pending their arcs.
- **FINDING S9-1 (NEW):** `bolting.triggers` (4 crops) has NO Appendix-A ruling -- register it (treated user-facing this pass). Same class of safeguard the `thinning.tip` catch exercised.
- **Register-completeness / dual-voice gate -- BUILT (`dual_voice_gate_v2.py`, claude.ai-side).** STILL OWED (WORRY 3): wire into the per-crop shell pass as an admission HALT + re-run at Step 11. Ship the STRUCTURAL walk logic into the pipeline `rubric.md`, not a transcribed roster.
- **Gold-standard arc checklist amendments** (claude.ai's authoring lane): (1) per-step lane tags; (2) shell-pass-first Steps 4-5; (3) Step 11 flip-disambiguation guardrail; (4) generalized per-crop deletion gate; (5) Step 8 gate wording must mandate a structural crop walk and name `thinning.tip` + region `tip_overrides`; **(6) NEW -- Step 9 wording: derive the user-facing leaf set by a structural walk (the authority docs are claude.ai-side), and the dash resolution is per-sense per-crop, not a dataset-wide find-replace.**
- **Pipeline / operating-model doc -- TO BE DESIGNED.** Own session after lettuce is gold-standard.
- **Step 11 Appendix-A registration:** bolting register keys + ~26 register-conversion field rulings + succession strings + se_gulf_month_resolution + 6b container conversion key-pairs + the Steps 7/8 `_beginner` keys (97) + region `tip_overrides` leaf-keys + **the `bolting.triggers` ruling (FINDING S9-1)**.
- **`safe_sowing_note` migration decision** (FINDING 6c-2): Phase C, Claude Code.
- **Deferred vocabulary session:** dataset-wide rename of `track` value `beginner` -> `main`.
- **Companions reconciliation session (§5):** the array-level register split (`good_beginner_seasoned`/`good_seasoned`/`bad_seasoned`, `why` fields). Lettuce carries 3 populated `why_seasoned` with null `why_beginner` -- correctly OUT OF SCOPE until this session runs.

## Inherited findings (unchanged)
- `finding_001` -- warm `zones{}` 8-11 SE-mis-sourced (legacy layer, own pass).
- na3d-na3g sourcing-sibling findings; `na3d_finding_003` cosmetic.
- **`rotation.note` 6a citation -- verify** (FINDING 6c-3): may reference uncatalogued `pnw_handbook`; re-confirm against catalog T1 at cross-anchor audit.
- Two-field predicate: `blocks_launch AND status != "resolved"` (never a bare count). **0 unresolved blockers.**

## Resolved findings (recent)
- **FINDING 6c-4 -- RESOLVED 2026-06-04 (Step 9):** temperature-form normalization complete dataset-wide; canonical user-facing form is `°F` (Trevor reversed the original "degrees F" choice).
- **FINDING Steps78-2 (`tip_overrides` notation carry) -- CLEARED for lettuce:** the 4 bolting `tip_overrides` carried no `degrees F`/bare-F needing change; `low_desert_az`'s "100 degree F" converted to `100°F` in the dataset-wide temp pass.

## Step 6 progress
- **79 of 119 lifted** -- UNCHANGED by Step 9 (a notation/punctuation sweep does not move the seasoned-lift tally).
- Remaining Step 6: any residual top-level CP not yet at-bar (`companions.*` deferred to §5; `det_indet.detail` does not exist on lettuce).

## Note on dataset size
Dataset is **~10.6 MB minified** (10,631,118 bytes at `da4b8bc5`; slightly smaller than `7e9eeceb`'s 10,632,328 because `°F` is shorter than "degrees F"). This **exceeds the project-knowledge upload limit** -- dataset + `LATEST.txt` stay out-of-band (upload from `~/plant-dataset/` at chat start), never in project knowledge.

## Pointers
- **History (append-only recovery log):** `STATE_HISTORY.md`.
- **Checklist:** gold-standard arc checklist **v1.4.1** (+ 6 amendments owed above).
- **Specs:** region-primary schema shape spec v1.0 (§3b-i), `register_bearing_field_inventory_v1_0.md`, per_crop_verification_methodology v1.4(.1), v1.5 cold-zone fall-heat-floor, calendar-model spec, region-tip override spec + validator, tip-region authoring standard v1.1.
- **Reusable gate:** `dual_voice_gate_v2.py` (structural whole-crop dual-voice coverage -- ship this logic into the pipeline rubric, not a hand roster).
- **Findings (recent):** `phase_3_lettuce_m15_step9_findings.md` (this session) + the Steps78 set (`phase_3_lettuce_m15_steps78_findings.md`, `m15_steps78_dual_voice_coverage_report.md`, `m15_steps78_appendix_a_registration_delta.md`); `phase_3_lettuce_m15_step6d_findings.md`; `phase_3_lettuce_m15_step6c_findings.md`.
