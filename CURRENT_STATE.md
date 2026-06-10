# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


## 🌳 SCHEMA 2.9 MIGRATED (2.8 -> 2.9): perennial/tree extension scaffolded **null-by-archetype** (chill / bloom / pollination / rootstock / dormancy+pruning windows / establishment / cane / renovation) + UNIVERSAL watering_method/schedule_by_stage/drought_tolerance/critical_periods + fertilizer.amount + container self-watering + sources plumbing. **STRICTLY ADDITIVE** (2439 leaves added, 0 changed, 0 removed); the 4 anchors stay certified. **Unblocks the perennial/tree anchors** (peach now eligible). 4 anchors certified (cherry/beefsteak/carrot/lettuce).

## Canonical pointer
- **Current SHA:** `0be2652ca00c878f0b8ecb975b521f09a8c81e7ac498679b9d16965fd4a19092`. `LATEST.txt` session: `schema_2_9_migration` (2026-06-10).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `b34bd6fc` -- feat(carrot): Steps 6-8 + CERTIFIED -- anchor 4 (first author-fresh, verified_gs_arc)
  - `ea16404c` -- feat(carrot): Step 5.5 -- per-zone calendars + pause tokens + succession shapes (v1.1)
  - `a9908c4a` -- feat(carrot): Step 4 CLOSED -- 9 warm regions + heat anchor live (air)
  - `12bb0572` -- feat(carrot): Step 4 partial -- northern_tier authored (from-scratch, anchor-relative)
  - `66b43bda` -- feat(carrot): Step 3.5 region shells (direct-sow) + extend build_region_shells
  - `ae2061ba` -- feat(carrot): Steps 1-3 author-fresh (anchor 4) + uga_c1232 mint + container dual-register
  - `aeb5c339` -- feat: author-fresh pivot -- reset 120 non-GS crops to honest shells

## What just happened (2026-06-10, session `schema_2_9_migration` -- Claude Code structural lane)
- **Schema 2.9 migration RELEASED.** `migrate_schema_2_9.py` (test-first, 10 assertions GREEN) null-scaffolds the perennial/tree extension per the archetype applicability matrix: chill block + bloom + pollination on 25 woody; rootstock on 21 grafted trees; cane on 4 brambles; renovation on strawberry; establishment on 26 (woody+strawberry). UNIVERSAL on all 123: `watering_method`/`schedule_by_stage`/`drought_tolerance`/`critical_periods`/`method_note`, `fertilizer.amount_*`, container `self_watering`, + `sources`/`anchoring_urls` plumbing on watering/fertilizer/thinning/varieties. `schema_version` 2.8 -> 2.9.
- **Strictly additive + idempotent + non-destructive:** 0 leaves removed, 0 values changed, 2439 added; re-run = identical SHA. The 4 certified anchors changed ONLY by additions -> `launch_ready` intact (additive nulls don't un-earn the 2.8 cert, same flavor as 2.7.5).
- **Gates:** register_completeness PASS (nulls aren't prose -> no halt), whole_crop_gate all 4 anchors PASS. Pre-ruled the 4 new universal-plain keys (`recommended_rootstock_note`/`establishment_note`/`what_to_ask_nursery`/`recommended_note`) in register EXCLUDED_KEYS so per-anchor authoring won't halt later. Promoted `0be2652c`.
- **Scope (locked, Trevor "build it"):** FLAT null-by-archetype, label 2.9, one bundled migration, plumbing-everywhere. Variety-object upgrade scoped to WOODY only (non-woody anchors' `recommended` string lists untouched). Spec: `docs/schema_2_9_scope_v0.md`.

## Active work + next step
- **2.9 design-lock DONE -> perennial/tree anchors UNBLOCKED.** NEXT = anchor 5 (roadmap call): **peach** (stone-fruit tree, now eligible -- first to exercise the new perennial surface) OR microgreen / an annual family hub (don't need 2.9).
- **2.9 per-anchor back-fill (non-blocking):** 2.9 fields are null everywhere; biology authored per anchor (each perennial/tree anchor populates its chill/bloom/pollination/rootstock; the 4 certified anchors get a small watering_method/fertilizer.amount back-fill when convenient).
- **Deferred off the additive migration:** C1 register-shape reshape (single->dual on universal keys; pre-existing debt) + C3 vocab value-reconcile (harvest_urgency/fertilizer.frequency level-vs-cadence). Variety×zone ROUTING (one-slug-per-varietal leaning) is plant-astro-side.
- **PARKED (unchanged):** WeatherKit; USCRN (uscrn null); v1.7 checklist amendment; register inventory; carrot region-tip override (`carrot_s68_finding_001`). **PK refresh owed:** `second_planting_structure_spec` v1.1 + `schema_2_9_specification_v1_0` (both in 05-methodology/current).

## Gate record (generated 2026-06-10, on canonical `0be2652c`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **4 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

## Live locked decisions / guardrails (carry into the perennial/tree anchors)
- **SCHEMA 2.9 model (locked):** crop = entity/guide/URL; **variety = DELTA overlay** (`{value,parent,changed}`, the apple-mock); Fuji is a VIEW of apple, never top-level. Three-tier info hierarchy keeps it scaling: universal education -> reference pages (`/guides/soil`+`/guides/ph` model; add chill-hours/pollination/pruning/watering); crop base -> hub; variety delta -> compact, distributes across page sections. Family tier = authoring (GS hubs + bots) + reference pages, NOT runtime inheritance -> renderer stays 2 levels. Perennial fields are FLAT null-by-archetype (not nested). Bloom calendar rides a structured `varieties.recommended[]` (curated recommended set, NO full Phase-5 dep). Beginner LEAN; depth -> seasoned.
- **MIGRATIONS are additive null-scaffold** (per 2.7.5 + 2.9): add fields null per the archetype matrix, never interpret/move values, never un-earn a cert; biology authored per anchor. `migrate_schema_2_9.py` is idempotent + non-destructive (test-first).
- **AUTHOR-FRESH model proven (carrot):** every value from the crop's own sources; "matches an anchor" is never a justification (A1). **CATALOG PRECISION = Claude Code's lane** (`ipm.ucanr.edu`->`uc_ipm`; claude.ai only sees the crop's source subset). **Step-11 verbatim_scan is flip-blocking** (reword, route to voice lane, don't self-dismiss).
- **SUCCESSION shape (spec v1.1):** `succession_continuous` (string) for continuous; `succession_spring`/`succession_fall` for split. **HEAT ANCHOR:** `heat_threshold_temp_f` = AIR (carrot 75°F).
- **Canonical JSON COMPACT** (`separators=(",",":")`, no trailing newline; never indent=2). GOTCHA: shell `>` truncates before read -> `gen_current_state` reads the old file for its header, so gen to a temp then `mv`. apply_patch accepts `ops` alias + APPENDS on `add` at list-index==len. Catalog IDs minted/re-pointed by Claude Code. Anchor target ~18.
- **Lane split:** claude.ai authors/verifies biology + copy; Claude Code releases (apply, gates + protocol #6, structural shapes/migrations, catalog mints, the flip) + owns data SHAPE/naming + builds the renderer. `zones{}` wiped on the 120 (kept on GS crops until Phase C).
