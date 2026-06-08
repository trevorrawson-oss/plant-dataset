# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.6**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---

## 🥬 LETTUCE + 🍅 CHERRY + 🍅 BEEFSTEAK CERTIFIED (`verified_gs_arc`). 3 OF 9 ANCHORS DONE.
**3 of 9 anchors certified.** `lettuce-leaf` (M15), `cherry-tomato` (M16, first full v1.5/1.6 arc), and **`beefsteak-tomato` (M16 anchor 2, CERTIFIED 2026-06-08)** -- all three `launch_ready_core/seasoned=true`, `status="verified_gs_arc"`, `GATE: PASS`. **Beefsteak completed the full arc** (Steps 3.5 -> 11) including its own independently-sourced (wider-than-cherry) heat biology. **NEXT = anchor 4 of 9** (6 remain; carrots is the next region-first authoring-model prover). **(Operating model: claude.ai authors, Claude Code releases; Steps 9/10/11 were the Claude Code mechanical + flip lane.)**

## Canonical pointer
- **Current SHA:** `973632ea0549b77d1d4810b34d2c81f86f5ebd39dbffb6cfabd07c5162b10a63` (beefsteak Steps 9/10/11 -> CERTIFIED; ONLY `beefsteak-tomato` changed -- 5 keys: sources_summary, tips_by_stage, harvest_urgency_anchoring_urls, diseases, verification_status; cherry + lettuce + catalog byte-identical). `LATEST.txt` session: `m16_beefsteak_steps9_10_11_certification`.
- **NEXT: anchor 4 of 9 (carrots, region-first) -- preflight against `973632ea`.**
- **Predecessor chain:** `973632ea` (beefsteak CERTIFIED) <- `e8b46da5` (Steps 6/7/8) <- `8fdb3ee6` (Step 5.5) <- `3a482908` (Step 4) <- `006cd0af` (Step 3.5) <- `87c8e0a1` <- `b6777ef6` (cherry CERTIFIED) <- ... (full chain in STATE_HISTORY).

## What just happened (2026-06-08, session `m16_beefsteak_steps9_10_11_certification` -- Claude Code lane)
- **Step 9 (dash):** `sources_summary[19].name` "...Center -- Produce Facts Sheets" -> ", Produce Facts Sheets" (publisher-publication apposition, cherry's resolution).
- **Step 10 (T2 + anchoring):** de-cited the T2 `harvest_to_table` from `tips_by_stage.germination[0]` (4 T1 sources remain; matches cherry's 0-citation state); added `harvest_urgency_anchoring_urls` (umn_ext + ncsu_ext, cherry's verified template).
- **Verbatim/copyright scan (Step 11 gate) -- RAN FULL (69 URLs, 56 covered), caught 2 HARD hits, BOTH adjudicated:** (1) `diseases[0].cause_seasoned` (depth-lifted at Step 6) shared an 8-word run with an Arkansas Septoria description -> **REWORDED** "starts at the bottom of the plant and moves upward" -> "starts low on the plant and moves upward" (Trevor's call: reword-then-certify; meaning/voice preserved, run broken). (2) `failure_diagnostics[3].next_season_tip_beginner` "1 to 2 inches of water" -> **RULED BENIGN** (universal numeric horticultural convention, the `s11_finding_003`-class precedent; Trevor 2026-06-08).
- **Step 11 (the flip):** reset the stale M11 `launch_ready_core/seasoned=true` -> false (entry guard `both==false` held), confirmed all gates green, atomically re-flipped -> true (EARNED); `status` `verified_complete` -> `verified_gs_arc`; `phase` `phase_3_m11_cleanup` -> `phase_3_m16_gold_standard_arc`; `date`/`last_audited` -> 2026-06-08. **BEEFSTEAK CERTIFIED.**

## Verification (protocol #6 + full Step-11 gate suite, this release)
- **whole_crop_gate beefsteak `GATE: PASS` (0)**; cherry + lettuce `GATE: PASS`. **release_verify:** only beefsteak changed (5 intended keys); §B no new violations; §D 6 = the SAME pre-existing legacy `zones{}` backend dashes. **verbatim scan:** hit 1 reworded (gone), hit 2 ruled benign (1 residual benign-adjudicated HARD hit, the water convention -- consistent with lettuce's benign-numeric precedent). **roster gate (register_completeness):** dataset-wide HALT (24 unruled `source_quote` patterns + 4 deferred companions) -- **PRE-EXISTING on the base; cherry + lettuce certified under the identical HALT, so it is NOT a per-crop flip blocker** (it gates the future register-conversion / new-crop-admission, a different operation). Collateral: only beefsteak's 5 intended keys; reset-then-flip provenance-honest.

## Active work + parked decisions
- **NEXT MILESTONE: anchor 4 of 9 -- carrots (region-first authoring, the authoring-model-flip prover 3 is now MET by beefsteak; carrots onward is full region-first).** 6 anchors remain.
- **PARKED -- Trevor / claude.ai dataset-wide (NOT blocking any per-crop cert):**
  1. **Register inventory: the 24 unruled `source_quote` patterns.** All 24 are `regions.*.plantings[].{start_indoors,plant_out,harvest_start,harvest_end}[].source_quote` (the backend verbatim date-verification quotes) -- they emerged when the region-fill layer added `source_quote` into region `plantings[]`. They need ONE ruling in `register_bearing_field_inventory_v1_0.md`: region-cell `source_quote` = **EXCLUDED** (backend, never user-facing -- same class as the already-excluded top-level `source_quote`/`synthesis_note`). The 4 `companions.*.provenance.reason` are already DEFERRED-by-design (inventory §5, not an open gap). This is a claude.ai/Trevor inventory task, not a per-crop blocker.
  2. **`fruit_set_temp_f` schema shape** (warm_arid Aug structural set; surfaced at Steps 4/5).
- **PARKED -- Trevor (minor):** optional `ca_south_coast` z9 soft-`cold_pause` revert; lettuce `why_beginner` copy (3 fields) sanity-check; the `sources_summary[19].name` comma-vs-colon one-char copy call (cherry used comma; beefsteak matches).
- **PARKED -- Claude Code lane (non-blocking):** claude.ai patch one-offs to keep flagging (full `$.crops[...]` paths; `ensure_ascii=False` SHA -- both hit once, now in CURRENT_STATE guardrails); gate/release_verify `basis_seasoned` §D classification alignment; release_verify §D over-flags pre-existing legacy `zones{}` dashes.

## Gate record (2026-06-08, on canonical `973632ea`)
- **lettuce `PASS` (0); cherry `PASS` (0); beefsteak `PASS` (0).** All three `verified_gs_arc`, launch_ready core+seasoned=true.

## Region fill state
**lettuce-leaf, cherry-tomato, beefsteak-tomato -- all 10/10 region cells filled + verified + CERTIFIED.** Beefsteak's heat biology is independently T1-sourced (wider-than-cherry pauses), NT is single-crop (not cherry's z6-7 second-crop) with winter `cold_pause`. Cherry remains the Step-3.5 shape + convention reference exemplar.

## Flip gates (the four distinct "flips")
1. **Per-crop `launch_ready` flip** -- ✅ lettuce, ✅ cherry, ✅ **beefsteak (3 of 9).** 6 anchors remain.
2. **Region read-layer flip** -- shape + fill + verification + flip proven on 3 crops now. The plant-astro renderer rewrite (read `regions{}`, consume `second_planting`, render `cold_pause`/`heat_pause`) is data-side unblocked. Ships with `zones{}` fallback. **2.9+.**
3. **Authoring-model flip** -- carrots onward region-first. **Gate: 3 provers MET (lettuce, cherry, beefsteak).** Carrots is the first post-flip region-first authoring.
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, 2.9+. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial = **2.9+.**

## Live locked decisions / guardrails (carry into anchor 4 / carrots)
- **Reference gold-standard crop = `cherry-tomato`** (shape + convention) -- but derive each crop's biology + STRUCTURE from its OWN sources; "matches cherry" is not a justification (v1.6 A1).
- **Step 11 = reset-then-flip:** stale `launch_ready=true` reset to false (entry guard), gates green, re-flip earned, `status` -> `verified_gs_arc`. The verbatim scan is a flip gate -- run it FULL (fetch URLs to cache, scan); HARD hits are flip-blocking until adjudicated (reword a real lift; rule generic/numeric conventions benign with a note -- do NOT self-dismiss, route the ruling to the voice lane / Trevor).
- **HANDOFF PATCHES: `base_sha` + `patches[]`, FULL `$.crops[?(@.slug=='...')]...` paths, `from`=current value, proposed end-SHA `ensure_ascii=False`.**
- **Lane split:** STRUCTURAL/MECHANICAL/notation/dash/de-cite/anchoring-fill/the-flip = Claude Code; biology + consumer copy + voice/IP + dates = claude.ai.
- **Keep `zones{}` coherent until Phase C.** **Release sequence:** `docs/release_runbook_v1_0.md`; protocol #6 before every promote.
