# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---

## 🥬 LETTUCE + 🍅 CHERRY CERTIFIED (`verified_gs_arc`). 🍅 BEEFSTEAK (anchor 2/9) arc: Steps 3.5 + 4 DONE, NEXT = Step 5
**2 of 9 anchors certified.** `cherry-tomato` (first full v1.5 arc) + `lettuce-leaf` (M15), both `status="verified_gs_arc"`, both `GATE: PASS`. **M16 `beefsteak-tomato` (anchor 2 of 9) in flight:** **Step 3.5 (region shells) + Step 4 (warm-region sourcing) both DONE.** All 9 warm region cells are now sourced + dual-register `region_notes` authored, every source T1; `northern_tier` shell built (owes only `calendar` `cold_pause` + `region_notes`). **NEXT = beefsteak Step 5 (per-cell side-by-side verification) + Step 5.5 (NT calendar `cold_pause`).** **(Operating model: claude.ai authors, Claude Code releases.)**

## Canonical pointer
- **Current SHA:** `3a482908b610d81824f2151cc2aa95ecb9ca50e925077085d4ba293bfbec1994` (beefsteak Step 4: 9 warm cells sourced; ONLY `beefsteak-tomato.regions` changed -- `zones{}`, lettuce, cherry, catalog byte-identical). `LATEST.txt` session: `m16_beefsteak_step4_warm_regions`.
- **NEXT: beefsteak Step 5 (verification side-by-side) + Step 5.5 (NT `cold_pause`) -- preflight against `3a482908`.**
- **Predecessor chain:** `3a482908` (Step 4 warm regions; = claude.ai `a87932cd` + 1 Claude-Code °F normalization) <- `006cd0af` (Step 3.5 shells) <- `87c8e0a1` (status vocab + lettuce gaps) <- `b6777ef6` (cherry CERTIFIED) <- ... <- `a65c7175` (cherry Step 3.5) <- `29b3aaa9` (M15 lettuce flip) <- ... (full chain in STATE_HISTORY).

## What just happened (2026-06-07, session `m16_beefsteak_step4_warm_regions`)
- **Beefsteak Step 4 RELEASED -- all 9 warm cells sourced (claude.ai authored, Claude Code released).** Each warm shell filled with verified region-appropriate windows + dual-register `region_notes` + heat biology, independently re-derived (NOT analogized from cherry). Headline biology: **beefsteak holds a WIDER summer heat pause than cherry** (large-fruited, less heat-tolerant) -- se_gulf/ca_desert/low_desert_az Jun-Aug `[6,7,8]`, fl_peninsula Jun-Sep `[6,7,8,9]`, warm_arid `[7]`-for-legibility; the cool CA coast + Hawaii hold no pause (hawaii `year_round:true`). second_planting on se_gulf/ca_desert/warm_arid/low_desert_az. All `sources_pending_admission` cleared; orphaned cold (UMN/MSU) prose dropped (`gs_exemplar_finding_001`). No catalog mints.
- **`northern_tier` untouched** (its `calendar` `cold_pause` + `region_notes` are Steps 5.5/6/7).
- **Patch-format reconciliation + 1 °F normalization (Claude Code lane).** claude.ai's patch deviated from `handoff_patch_format_v1_0.md` (it used a `_meta`+`corrections[].changes[]`/`set_value`/`before`/`after` variant); reconciled to canonical `{base_sha, patches[]}` and applied via `apply_patch.py` -- triangulated to claude.ai's proposed `a87932cd` exactly (== the zip's full JSON). Then the claim cross-check caught one real drift: `warm_arid.heat_pause.basis_seasoned` spelled "95 degrees F" where cherry's certified cell uses `°F`; normalized `95 degrees F -> 95°F` (Claude Code notation lane). Promoted SHA `3a482908` = `a87932cd` + that 1-field fix.

## Verification (protocol #6, this release)
- **(a) gate:** beefsteak `43 -> 34` (§A2 SHAPE 0; region_notes-null = 1 = NT only; temp-form 0 after the °F fix); cherry + lettuce `GATE: PASS`. **(b) release_verify:** collateral clean (only `beefsteak.regions`; zones/lettuce/cherry/catalog byte-identical); §B **no new violations**; §E/F ok; §C `wait` notes (NT + 2 cool-CA-coast z10 shoulders = Step 5.5, non-blocking); §D 6 dashes = SAME pre-existing legacy `zones{}` backend strings (untouched). **(c) claim cross-check:** all 9 cells' window_structure / heat_pause months / second_planting zones / pending-cleared / `year_round` verified TRUE; orphan-drop genuine (exact per-cell source IDs 100% region-appropriate, zero cold citations, zero whole-word Minnesota/Michigan prose).

## Active work + parked decisions
- **NEXT MILESTONE: beefsteak Step 5 (per-cell side-by-side verification, claude.ai) + Step 5.5** (`northern_tier` `calendar` `cold_pause` derivation -- token-only, no sibling object, the move cherry's NT got -- plus whole-calendar coherence on the 9 new warm cells). Then **Steps 6/7/8** (the 30 dual-voice `_beginner` siblings incl. `cause_beginner` x8 + `growth_stages.log_prompt_beginner` x6), **Step 9** (1 `sources_summary[19].name` dash), **Step 10** (1 `harvest_to_table` T2 + 1 `harvest_urgency` anchoring gap), **Step 11** (validation + `launch_ready` reset-then-flip + `status`->`verified_gs_arc`).
- **PARKED -- beefsteak stale-flag reset (Step 11, NOT now):** still carries `launch_ready_core/seasoned=true` + `status="verified_complete"` (M11 artifacts). Reset-then-re-earn at its OWN Step 11.
- **PARKED -- Trevor decisions:** (1) **`fruit_set_temp_f` schema shape** -- would let `warm_arid`'s August large-fruited poor-set be STRUCTURAL rather than prose-only (claude.ai flagged it again this session); schema-touching -> Trevor rules shape, Claude Code adds field. (2) optional `ca_south_coast` z9 soft-`cold_pause` revert. (3) lettuce `why_beginner` copy (Radishes/Carrots/Chives) Claude-Code-drafted -- sanity-check.
- **PARKED -- Claude Code lane (non-blocking):**
  1. **Patch-format drift:** claude.ai's Step 4 patch used a non-canonical `_meta`+`corrections[].changes[]` variant. Flag to claude.ai for Step 5: emit `handoff_patch_format_v1_0.md` exactly (`base_sha` + `patches[]` with `json_path`/`value`). Reconciled by hand this session; if it recurs, extend `apply_patch.py` to tolerate it.
  2. **Gate/release_verify `basis_seasoned` classification mismatch:** `whole_crop_gate` §D temp-scan exempts `synthesis_note_seasoned` but NOT `basis_seasoned`; `release_verify` §D exempts both. Align them, and settle whether `*_basis`/`basis_seasoned` is user-facing (must be `°F`) or backend (may spell) -- this governs whether the spelled-degrees `synthesis_note_seasoned` temps need a dataset-wide °F pass.
  3. `release_verify` §D over-flags pre-existing legacy `zones{}` anchoring-note dashes (narrower backend filter than the gate's `is_backend`).
- **PARKED -- claude.ai checklist amendments:** `lifted_from_zone`-strip into Step 3.5 text; °F-in-user-facing rule; retire "every cell needs a county MG"; window-structure-is-a-source-finding (Path A fallback); heat-set-failure-month = heat_pause token + second_planting action.

## Gate record (2026-06-07, on canonical `3a482908`)
- **cherry `GATE: PASS` (0); lettuce `GATE: PASS` (0).** Both: launch_ready core+seasoned=true, `status="verified_gs_arc"`.
- **beefsteak `GATE: 34`** -- mid-arc (Steps 4 done). §A2 SHAPE 0; the 34 = 1 NT region_notes-null + 30 dual-voice siblings + 1 `sources_summary` dash + 1 `harvest_to_table` T2 + 1 `harvest_urgency` anchoring gap. All downstream Steps 5.5/6/7/8/9/10.

## Region fill state
**cherry-tomato -- 10/10 verified, CERTIFIED (the reference exemplar).** (Full per-cell table in prior CURRENT_STATE revisions / STATE_HISTORY.)

**beefsteak-tomato -- 9/10 warm cells SOURCED (Step 4); `northern_tier` shell-built (owes `calendar` `cold_pause` + `region_notes` at 5.5/6/7).** Independent heat biology, WIDER pause than cherry:
| region | zones | window | heat_pause | second_planting |
|---|---|---|---|---|
| `se_gulf` | 8,9 | two_window | **Jun-Aug [6,7,8]** (wider than cherry) | yes (z8,z9) |
| `ca_interior` | 8,9 | single | none (production-tail) | none |
| `ca_north_coast` | 9,10 | single (May) | none (cool-limited) | none |
| `ca_south_coast` | 9,10 | single (long Apr-Jul15) | none (mild marine) | none |
| `ca_desert` | 9,10 | two_window | Jun-Aug [6,7,8] (absolute, = cherry) | yes (z9,z10) |
| `warm_arid` | 8 | two_window | [7] legibility (Aug poor-set in prose) | yes (z8) |
| `low_desert_az` | 9 | two_window | **Jun-Aug [6,7,8]** (wider than cherry) | yes (z9) |
| `fl_peninsula` | 10,11 | near_continuous_inverted | **Jun-Sep [6,7,8,9]** (widest) | none |
| `hawaii_tropical` | 11 | year_round | none (oceanic-tropical) | none |
| `northern_tier` | 3-7 | cold (frost-bracketed) | none (frost-limited) | (Step 3.5; owes cold_pause+notes) |

## Flip gates (the four distinct "flips")
1. **Per-crop `launch_ready` flip** -- ✅ lettuce (1), ✅ cherry (2). **Beefsteak in flight (Steps 3.5+4 done; 5/5.5/6/7/8/9/10/11 remain).** Then 6 more anchors.
2. **Region read-layer flip** -- renderer reads `regions{}` first. Shape proven on lettuce + cherry; beefsteak 9/10 cells now filled (owes NT + Steps 5-11). Ships with `zones{}` fallback. **2.9+.**
3. **Authoring-model flip** -- carrots onward region-first. Gate: 3 provers (cherry done; beefsteak prover 2, in flight).
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, 2.9+. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial = **2.9+.**

## Live locked decisions / guardrails (carry into beefsteak Step 5)
- **Reference gold-standard crop = `cherry-tomato`** (Step 3.5 shape + the convention reference). Dataset is authoritative; flag doc lag.
- **BEEFSTEAK HOLDS A WIDER HEAT PAUSE than cherry -- now SOURCED, not assumed** (Step 4 re-derived it from Alabama Coop Ext + U.Missouri IPM: large-fruited abort at day >85 / night >72 °F, below cherry's threshold). Step 5 confirms each window/pause side-by-side against its T1.
- **Heat-set-failure month that is ALSO a planting month = `heat_pause` token + the plant on a `second_planting{}` track** (warm_arid Jul). **WINTER COLD = `cold_pause` token, NO sibling object** (not on frost-free z10).
- **DUAL-VOICE: every in-scope `_seasoned` field needs a plain `_beginner` sibling.** Backend prose (`synthesis_note`, `*_basis`, `source_quote`) is seasoned-only by design. (See the parked `basis_seasoned` classification item -- the gate currently temp-scans `basis_seasoned`; user-facing temps render `°F`.)
- **WINDOW STRUCTURE is a SOURCE FINDING; NEVER carry a multi-window shape on analogy** (Path A is the fallback for visual-chart sources -- warm_arid's two-window rests on the Dona Ana MG Las Cruces chart).
- **`harvest_to_table` T2-as-evidence: T1-only, NO grandfathering.** **TEMPERATURE user-facing = `°F` not "degrees F"** (backend prose may spell it).
- **CATALOG ADMISSION (county MG = UC ANR/NMSU = T1):** discovery+verified-URL = claude.ai; catalog write = Claude Code (mint the ID). Step 4 needed no mints.
- **`second_planting` = discrete-window object (seasoned-only); succession = `succession_spring/fall`; main = flat cell fields.** Each crop carries ONLY its structures. **Lettuce NOT reshaped.**
- **HANDOFF PATCHES must conform to `handoff_patch_format_v1_0.md`** (`base_sha` + `patches[]`). claude.ai's Step 4 patch drifted; reconciled by hand. Flag in the Step 5 handoff.
- **Lane split:** STRUCTURAL/MECHANICAL/notation = Claude Code; biology + consumer copy + voice/IP + URL discovery + dates = claude.ai.
- **Keep `zones{}` coherent until Phase C** (renderer still reads it).
- **Release sequence:** `docs/release_runbook_v1_0.md`; protocol #6 before every promote.
