# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist v1.4) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push). Data change and state-only change both end with this ritual; never leave git behind (the hand-promote-uncommitted combination is what once turned a routine promote into a recovery).

---

## Canonical pointer
- **Current SHA:** `8a1d8a50ef41729f34caabf849da3b870e61975d1914e857d58a0420aebab056` (bolting register-conversion addendum -- 2.8 gap-fix; 9 crops' `bolting.note`/`prevention` -> `_seasoned` + null `_beginner`).
- **Predecessor chain:** `ed495666` (lettuce Pass 2 warm-cell consistency) <- `20f9fc2b` (Pass 1b succession hoist) <- `327a2d5c` (Pass 1a calendars) <- `582dbbad` (northern_tier reconciliation).
- Every promote re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## Active work + exact next step
- **Crop in flight:** `lettuce-leaf`.
- **Done:** the region-cell STRUCTURAL slice is complete -- Steps 4/5 + per-cell 5.5 gates, and the three Claude-Code structural passes (1a calendars, 1b succession-rule hoist, 2 warm-cell consistency). All 10 region cells populated + shape-correct. Plus the bolting register addendum (see Canonical pointer): a Phase-0 gap-fix orthogonal to the lettuce arc, surfaced by the Step 6 register read.
- **NEXT (claude.ai's lane):** **Step 6 -- seasoned depth-lift.** Then Steps 7/8 (beginner siblings), then Step 11 (whole-crop validation).
- ⚠️ **The lettuce flag-flip is the LAST act of Step 11, ONLY on 0 violations. It is NOT next.** (Region-cell work being done is necessary, not sufficient -- see Flip gates.)

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- one crop becomes gold-standard / goes live. **Gate:** that crop's Step 11 returns 0 violations. *(This is the one a session jumped to early off "northern_tier done"; it only closed Step 5.5.)*
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce done; cherry + beefsteak still owe M16); shipped with a `zones{}` fallback. Low-stakes because only gold-standard crops render, and those always have populated region cells -- a PENDING cell never reaches a user.
3. **Authoring-model flip** -- carrots and every later crop are authored region-first (no zones->regions retrofit). **Gate:** 3 provers done.
4. **Schema 2.8 perennial bump** (`lifecycle_override`, perennial support) -- a LATER milestone, after carrots. **Decoupled** from #2; do not bundle.

## Live locked decisions / guardrails (in force; superseded ones live in history)
- **Lane split.** Dataset STRUCTURAL work (region shell, calendar derivation, shape transforms, programmatic gates, gated deletion) = **Claude Code**. Biology windows from T1 sources (live web) + consumer copy (Steps 6/7/8) = **claude.ai**. Steps 4-5.5 split THROUGH this line: shell = Claude Code, window biology = claude.ai.
- **Per-crop pipeline (target):** Claude Code shell pass (scaffold + reshape existing `zones{}` data + derive calendars + set conventions + run gates + emit a precise PENDING-gap map) -> claude.ai fills the flagged biology gaps + writes copy -> Claude Code certifies (Step 11 structural re-walk) -> Claude Code gated deletion. The shell pass runs BEFORE the biology (fixes lettuce's retrofit-cleanup order).
- **Lettuce authors into `regions{}` this arc;** keep `zones{}` coherent until Phase C.
- **Succession-shape rule (spec-B, clarified 2026-06-03, codified as spec §3b-i):** the succession RULE (anchors/offset/interval/notes) lives ONCE in region-constant `plantings[]` (`track:"succession"`). `resolved_by_zone[z]` must NOT hold succession ARM OBJECTS (rule-bearing -- the NA-3h anti-pattern Pass 1b removed), but MAY hold materialized succession DATE-STRINGS (`succession_spring`/`succession_fall`), exactly as it holds the main `plant_out` strings -- static-consumer precompute, not a rule. Guardrail: the app recomputes succession from `plantings[]` + live frost and IGNORES `resolved_by_zone` entirely (main and succession alike). **Regenerable-vs-precompute (why warm != cold, asymmetric BY DESIGN):** store rule-ONLY when the cadence regenerates from STORED inputs (warm cells: regular continuous 2-week `succession_policy`); MATERIALIZE per-zone date-strings when it does NOT (northern_tier: the `soil_temp_40f` spring anchor is not a stored resolver input -- the whole northern resolved layer is precompute for the same reason -- plus per-zone Clause-C counts + the fall Jul-1 clamp).
- **`year_round` encoding** for genuinely pauseless cells (declare-one-outcome: each frost_anchored resolved cell declares exactly one of heat_pause / cold_pause / year_round).
- **`track` semantics:** single scalar naming the calendar -- `beginner` = the shared MAIN calendar BOTH audiences see (legacy misnomer for "main"); `succession` = seasoned-only. Renderer enforces visibility.
- **Register-conversion convention.** Register-bearing prose is `X_seasoned` + (`X_beginner` for CP, absent for SP); presence IS the visibility declaration. The canonical roster is `register_bearing_field_inventory_v1_0.md`. NEW crop datapoints must be checked against it -- an unruled prose field is a finding (the bolting class of bug; see the register-completeness gate below).
- **Deletion gate (legacy `zones{}`):** delete ONLY at Phase C, per crop, AFTER -- region cell carries everything zones held (incl. succession) + all consumers read region-first + round-trip returns a present verified value + frost-input independence. The shell pass READS zones; deletion REMOVES zones; opposite ends of the pipeline.

## Open items owed
- **Register-completeness gate -- BUILT (draft):** `plant-dataset/tools/register_completeness_gate.py` (roster-completeness inversion: any prose-shaped field with no ruling HALTS; stop-and-ask, no auto-fix). Ran dataset-wide; surfaced a LARGE bolting-class omission beyond bolting (see next item). **Refinement owed:** add the positive CP/SP roster so it auto-separates "ruled SP/CP but unconverted" from "genuinely unruled" (currently grouped by hand). **Home:** folds into the per-crop shell pass as an admission gate + Step 11. Candidate list handed to claude.ai: `06-sessions/register_completeness_gate_handoff_2026-06-03.md`.
- **Register-conversion completion addendum (Claude Code, AFTER claude.ai rules):** the 2.8 register conversion was incomplete -- its tomato-anchored walk missed nested + array-name prose. Pending claude.ai rulings: (A) SP evidence prose `synthesis_note` (~6.4k) / `source_quote` (~3k) / `design_note` (~1.8k) / `zone_coverage_note` in zones+regions planting rules -> `_seasoned` rename only (no beginner); (B) `growth_stages_annual`/`growth_stages_year_one` inner prose -> CP (`_seasoned` + null `_beginner`); (C) ~18 newly-surfaced fields need rulings. Byte-preserving rename + null scaffold, no copy authored (like bolting, larger).
- **Gold-standard arc checklist amendments** (claude.ai's authoring lane to apply): (1) per-step lane tags; (2) shell-pass-first structuring of Steps 4-5; (3) a Step 11 flip-disambiguation guardrail (this is the per-crop `launch_ready` flip ONLY); (4) the generalized per-crop deletion gate.
- **Pipeline / operating-model doc -- TO BE DESIGNED** (cross-crop machine + full flip taxonomy + the checklist-amendments list). Design as its own session after lettuce is gold-standard.
- **Step 11 Appendix-A registration:** the `succession_spring`/`succession_fall` resolved-cell keys (Pass 1b) + the `se_gulf_month_resolution` method label (Pass 2) + the `bolting.{note,prevention}_seasoned/_beginner` keys (this addendum).
- **Optional forward finding:** machine-readable fall heat-floor clamp field, dataset-wide, if the app resolver must reproduce the cold-zone Jul-1 clamp exactly. NOTE: this alone does NOT make the north regenerable (spring `soil_temp_40f` anchor is unstored); full symmetry would also need a `zone_soil_temp_40f` input table.
- **Deferred vocabulary session:** dataset-wide rename of the `track` value `beginner` -> `main`.

## Pointers
- **History (append-only recovery log):** `STATE_HISTORY.md`.
- **Checklist:** gold-standard arc checklist v1.4 (+ amendments owed above).
- **Specs:** region-primary schema shape spec v1.0 (now in `05-methodology/current/`, carries §3b-i), `register_bearing_field_inventory_v1_0.md` (register roster), per_crop_verification_methodology v1.4(.1), v1.5 cold-zone fall-heat-floor, calendar-model spec, region-tip override spec + validator, tip-region authoring standard v1.1.
- **Findings (recent):** `06-sessions/northern_tier_pass1a_findings.md`, `northern_tier_pass1b_findings.md`, `lettuce_warm_cell_pass2_findings.md`, `bolting_register_conversion_addendum_findings.md`.
