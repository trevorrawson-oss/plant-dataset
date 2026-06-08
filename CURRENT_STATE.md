# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---

## 🥬 LETTUCE + 🍅 CHERRY CERTIFIED (`verified_gs_arc`). 🍅 BEEFSTEAK (anchor 2/9) arc: Steps 3.5 + 4 + 5 + 5.5 DONE, NEXT = Steps 6/7/8
**2 of 9 anchors certified.** `cherry-tomato` + `lettuce-leaf`, both `status="verified_gs_arc"`, both `GATE: PASS`. **M16 `beefsteak-tomato` (anchor 2 of 9) in flight:** **Steps 3.5 (shells) + 4 (warm sourcing) + 5 (side-by-side verification) + 5.5 (NT `cold_pause` + calendar coherence) all DONE.** All 9 warm cells VERIFIED TRUE against T1 (zero corrections; the wider-than-cherry heat pause is now doubly-T1-confirmed). `northern_tier` winter `cold_pause` derived. **NEXT = beefsteak Steps 6/7/8 (the 30 dual-voice `_beginner` siblings).** **(Operating model: claude.ai authors, Claude Code releases.)**

## Canonical pointer
- **Current SHA:** `8fdb3ee66c6866ed690949e03d59b90c006f4231d759a2222ecfa1b20ce63f54` (beefsteak Step 5.5: NT 22 `wait`->`cold_pause` token edits; ONLY `beefsteak-tomato.regions.northern_tier.resolved_by_zone.{3-7}.calendar` changed -- 9 warm cells + NT non-calendar fields + lettuce + cherry + catalog byte-identical). `LATEST.txt` session: `m16_beefsteak_step5_5_nt_cold_pause`.
- **NEXT: beefsteak Steps 6/7/8 (dual-voice beginner siblings) -- preflight against `8fdb3ee6`.**
- **Predecessor chain:** `8fdb3ee6` (Step 5.5 NT cold_pause; Step 5 verified warm cells, 0 corrections) <- `3a482908` (Step 4 warm regions) <- `006cd0af` (Step 3.5 shells) <- `87c8e0a1` <- `b6777ef6` (cherry CERTIFIED) <- ... (full chain in STATE_HISTORY).

## What just happened (2026-06-08, session `m16_beefsteak_step5_5_nt_cold_pause`)
- **Step 5 -- verification side-by-side, all 9 warm cells (claude.ai authored, Claude Code released).** Every Step-4 biological value (windows, harvest offsets, second_planting dates, heat_pause months) checked side-by-side against its cited T1, live-fetched. **ALL 9 warm cells VERIFIED TRUE -- ZERO corrections.** The wider-than-cherry heat pause STANDS, now DOUBLY T1-confirmed (UF/IFAS VH021 + CTAHR Field Production Guide for the type-differential; Missouri IPM / Maryland / Yavapai for thresholds; the widest case fl_peninsula Jun-Sep checked vs Miami NCEI night-temp normals). Cultivar-type PASS (DTM 75-90, +90d offsets, not cherry's). Template-copy CLEARED (0 heat_pause-basis/region_notes byte-identical to cherry; the 8 species-level spring windows match cherry but were re-verified, not pasted).
- **Step 5.5 -- the only dataset CHANGE: NT `cold_pause` (22 tokens).** `northern_tier` z3-z7 winter shoulder `wait` -> `cold_pause` (token-only, no sibling, the move cherry's NT got). Inventory: z3 6 / z4 6 / z5 4 / z6 4 / z7 2 = 22. Cool-coast z10 `wait` shoulders (ca_north_coast, ca_south_coast) CLASSIFIED + KEPT `wait` (frost-free-cool, byte-identical to cherry's certified z10). Coherence invariants clean.
- **Patch format: CANONICAL this session** (`base_sha` + `patches[]`) -- the Step-4 `_meta`/`corrections` drift is corrected; the project-knowledge spec landed.

## Verification (protocol #6, this release)
- **(a) gate:** beefsteak **34 (unchanged** -- Step 5.5 is coherence, not violation-clearing); cherry + lettuce `GATE: PASS`. **(b) release_verify:** collateral clean (only `beefsteak.regions.northern_tier`; 9 warm cells + NT non-calendar + lettuce + cherry + catalog byte-identical); §B **no new violations**; §C the 5 NT `wait`-notes CLEARED (now cold_pause), only the 2 legit cool-coast z10 waits remain; §E/F ok; §D 6 dashes = SAME pre-existing legacy `zones{}` backend strings. **(c) claim cross-check:** exactly 22 `wait`->`cold_pause` on the manifest paths, 0 non-conforming; 9 warm cells byte-identical; warm-cell corrections 0.
- **Serialization note (benign):** claude.ai's proposed end-SHA `5e09ef33` was computed `ensure_ascii=True` (°-symbols escaped); the canonical convention is `ensure_ascii=False`, so the promoted SHA is `8fdb3ee6`. CONTENT verified identical (the ascii-escaped re-serialization of the promoted file reproduces `5e09ef33` exactly). Flag claude.ai to compute the proposed end-SHA with `ensure_ascii=False`.

## Active work + parked decisions
- **NEXT MILESTONE: beefsteak Steps 6/7/8 (dual-voice beginner siblings, claude.ai).** The 30 crop-level `_beginner` siblings: `cause_beginner` x8 (pests/diseases), `growth_stages.log_prompt_beginner` x6, watering x3, container x2, rotation x1, storage x3, yield x2, companions `why_beginner` x5. (The 9 region_notes are already dual-register from Step 4.) Then **Step 9** (1 `sources_summary[19].name` dash), **Step 10** (1 `harvest_to_table` T2 + 1 `harvest_urgency` anchoring gap), **Step 11** (validation + `launch_ready` reset-then-flip + `status`->`verified_gs_arc`).
- **PARKED -- beefsteak stale-flag reset (Step 11, NOT now):** still carries `launch_ready_core/seasoned=true` + `status="verified_complete"` (M11 artifacts). Reset-then-re-earn at its OWN Step 11.
- **PARKED -- Trevor decisions:** (1) **`fruit_set_temp_f` schema shape** (re-surfaced AGAIN at Step 5) -- would make `warm_arid`'s August large-fruited poor-set STRUCTURAL not prose-only; schema-touching -> Trevor rules shape, Claude Code adds field. (2) optional `ca_south_coast` z9 soft-`cold_pause` revert. (3) lettuce `why_beginner` copy (Radishes/Carrots/Chives) Claude-Code-drafted -- sanity-check.
- **PARKED -- Claude Code lane (non-blocking):**
  1. **claude.ai serialization:** compute the proposed end-SHA with `ensure_ascii=False` (it used `True` this session; content was fine, SHA differed). Flag in the Step 6/7/8 handoff.
  2. **Gate/release_verify `basis_seasoned` classification:** `whole_crop_gate` §D temp-scans `basis_seasoned` but exempts `synthesis_note_seasoned`; `release_verify` §D exempts both. Align them; settle user-facing-vs-backend for `*_basis`.
  3. `release_verify` §D over-flags pre-existing legacy `zones{}` anchoring-note dashes (narrower backend filter than the gate's).
  - **RESOLVED this session:** the Step-4 patch-format drift (claude.ai now emits canonical `{base_sha, patches[]}`).
- **RESOLVED:** the six previously-owed checklist amendments are SHIPPED in **v1.6** (governing checklist is now v1.6, synced on disk `05-methodology/current/` + `00-current/` + PK) -- no longer owed; do not re-flag.

## Gate record (2026-06-08, on canonical `8fdb3ee6`)
- **cherry `GATE: PASS` (0); lettuce `GATE: PASS` (0).** Both: launch_ready core+seasoned=true, `status="verified_gs_arc"`.
- **beefsteak `GATE: 34`** -- mid-arc (Steps 4 + 5 + 5.5 done). §A2 SHAPE 0; the 34 = 1 NT region_notes-null + 30 dual-voice siblings + 1 `sources_summary` dash + 1 `harvest_to_table` T2 + 1 `harvest_urgency` anchoring gap. All downstream Steps 6/7/8/9/10. (Step 5.5 left the total unchanged by design -- it cleared `wait`-legibility review notes, not gate violations.)

## Region fill state
**cherry-tomato -- 10/10 verified, CERTIFIED (the reference exemplar).**

**beefsteak-tomato -- 9/10 warm cells SOURCED (Step 4) + VERIFIED side-by-side (Step 5); `northern_tier` promoted + `cold_pause`-derived (Step 5.5).** Owes only the crop-level dual-voice siblings (6/7/8) + NT `region_notes` (6/7). Independent heat biology, WIDER pause than cherry, now T1-verified:
| region | zones | window | heat_pause (VERIFIED) | second_planting |
|---|---|---|---|---|
| `se_gulf` | 8,9 | two_window | Jun-Aug [6,7,8] (wider than cherry) | yes (z8,z9) |
| `ca_interior` | 8,9 | single | none (production-tail) | none |
| `ca_north_coast` | 9,10 | single (May) | none (cool-limited; z10 `wait` shoulders) | none |
| `ca_south_coast` | 9,10 | single (long Apr-Jul15) | none (mild marine; z10 `wait` shoulders) | none |
| `ca_desert` | 9,10 | two_window | Jun-Aug [6,7,8] (absolute, = cherry) | yes (z9,z10) |
| `warm_arid` | 8 | two_window | [7] legibility (Aug poor-set in prose) | yes (z8) |
| `low_desert_az` | 9 | two_window | Jun-Aug [6,7,8] (wider than cherry) | yes (z9) |
| `fl_peninsula` | 10,11 | near_continuous_inverted | Jun-Sep [6,7,8,9] (widest) | none |
| `hawaii_tropical` | 11 | year_round | none (oceanic-tropical) | none |
| `northern_tier` | 3-7 | cold (frost-bracketed) | none; winter `cold_pause` DERIVED (22 tokens) | (owes region_notes at 6/7) |

## Flip gates (the four distinct "flips")
1. **Per-crop `launch_ready` flip** -- ✅ lettuce (1), ✅ cherry (2). **Beefsteak in flight (3.5+4+5+5.5 done; 6/7/8/9/10/11 remain).** Then 6 more anchors.
2. **Region read-layer flip** -- shape + fill proven on lettuce + cherry; beefsteak 9/10 cells filled + verified (owes NT notes + Steps 6-11). Ships with `zones{}` fallback. **2.9+.**
3. **Authoring-model flip** -- carrots onward region-first. 3 provers (cherry done; beefsteak prover 2, in flight).
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, 2.9+. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial = **2.9+.**

## Live locked decisions / guardrails (carry into beefsteak Steps 6/7/8)
- **Reference gold-standard crop = `cherry-tomato`** (shape + convention reference). Dataset is authoritative; flag doc lag.
- **BEEFSTEAK'S WIDER HEAT PAUSE is now T1-VERIFIED** (Step 5 side-by-side: VH021 + CTAHR + thresholds + regional night-temp normals). Do NOT re-litigate; it is doubly-sourced.
- **DUAL-VOICE (Steps 6/7/8 focus): every in-scope `_seasoned` field needs a plain `_beginner` sibling** per dual-register v1.1's five rules (failure-diagnostics 4-slot, range-to-target safety-edge, contextual qualifiers, voice w/ bio-accuracy carve-out, gloss-then-use). `cause_beginner` = same content, plainer phrasing (may be byte-identical to its `_seasoned` if no jargon). Backend prose (`synthesis_note`, `*_basis`, `source_quote`) is seasoned-only.
- **`harvest_to_table` T2-as-evidence: T1-only, NO grandfathering** (Step 10). **TEMPERATURE user-facing = `°F` not "degrees F"** (backend prose may spell it).
- **HANDOFF PATCHES conform to `handoff_patch_format_v1_0.md`** (`base_sha` + `patches[]`) -- claude.ai conformed this session. Compute the proposed end-SHA `ensure_ascii=False`.
- **`second_planting` = discrete-window object (seasoned-only); each crop carries ONLY its structures; lettuce NOT reshaped.**
- **Lane split:** STRUCTURAL/MECHANICAL/notation = Claude Code; biology + consumer copy + voice/IP + URL discovery + dates = claude.ai.
- **Keep `zones{}` coherent until Phase C.** **Release sequence:** `docs/release_runbook_v1_0.md`; protocol #6 before every promote.
