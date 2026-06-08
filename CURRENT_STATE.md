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
- **Current SHA:** `ab389f72136f6d8f6576da6f93b62c8eb1cf2e3cf765041276a6ac746c4f5e4b` (register normalization: `source_quote_seasoned` un-renamed to bare `source_quote` dataset-wide -- 794 keys across 32 crops, value + position preserving; backend evidence, no longer rendered to seasoned mode. Only `source_quote*` keys changed; all other content byte-identical). `LATEST.txt` session: `register_source_quote_excluded_normalization`.
- **NEXT: anchor 4 of 9 (carrots, region-first) -- preflight against `ab389f72`.**
- **Predecessor chain:** `ab389f72` (source_quote->EXCLUDED normalization) <- `973632ea` (beefsteak CERTIFIED) <- `e8b46da5` (Steps 6/7/8) <- `8fdb3ee6` (Step 5.5) <- `3a482908` (Step 4) <- `006cd0af` (Step 3.5) <- `b6777ef6` (cherry CERTIFIED) <- ... (full chain in STATE_HISTORY).

## What just happened (2026-06-08, session `register_source_quote_excluded_normalization` -- Claude Code lane)
- **`source_quote` reclassified SP -> EXCLUDED + dataset normalized** (per claude.ai register-inventory addendum 2026-06-08, Trevor-ratified). `source_quote` is *verbatim* third-party extension text; as a `_seasoned` field it would RENDER unparaphrased source quotes to seasoned-mode users -- the IP/verbatim posture the project's paraphrase discipline + `verbatim_scan` forbid. Reclassified to backend evidence (§4 AUDIT_LEAF, same class as `source`/`source_id`/`source_note`). Reverses a 2026-05-30 "SP" call (which weighed the quotes as content, not the verbatim-display IP posture).
- **Apply (Claude Code mechanical):** un-renamed all **794** `source_quote_seasoned` -> bare `source_quote` across **32 crops** (value + position preserving; 0 collisions; the 2265 region-fill instances were already bare). `synthesis_note_seasoned` (own-voice reasoning) UNCHANGED -- the seasoned "show your work" still renders. Added `source_quote` to `register_completeness_gate.py` `EXCLUDED_KEYS` to match the inventory + `whole_crop_gate`.
- **This RESOLVES the 24-pattern roster HALT** (the prior parked dataset-wide register item). The 4 `companions.*.provenance.reason` remain DEFERRED-by-design.
- *(Prior session: beefsteak CERTIFIED via Steps 9/10/11 -- the 3rd anchor; full detail in STATE_HISTORY.)*

## Verification (this release -- dataset-wide backend normalization)
- **In-transform audits:** only `source_quote*` keys changed -- every other key+value byte-identical (independent strip-and-compare); all `source_quote*` VALUES preserved (multiset equal); 0 `source_quote_seasoned` remain; `source_quote` count 2265 -> 3059. **register_completeness_gate: HALT(24) -> PASS(0).** **whole_crop_gate: lettuce + cherry + beefsteak all `GATE: PASS`** (un-rename is backend; no violation change; the 3 anchors stay certified). Multi-crop change (32 crops) -> targeted collateral (the strip-compare), not the single-crop release_verify model.

## Active work + parked decisions
- **NEXT MILESTONE: anchor 4 of 9 -- carrots (region-first authoring, the authoring-model-flip prover 3 is now MET by beefsteak; carrots onward is full region-first).** 6 anchors remain.
- **PARKED -- Trevor / claude.ai dataset-wide (NOT blocking any per-crop cert):**
  1. **Register inventory `source_quote` -- ✅ RESOLVED 2026-06-08.** Ruled EXCLUDED (claude.ai addendum, Trevor); 794 `source_quote_seasoned` un-renamed to bare dataset-wide; gate `EXCLUDED_KEYS` synced; roster HALT(24) -> PASS. **Open follow-up:** the inventory doc (`register_bearing_field_inventory_v1_0.md`) itself lives only in claude.ai PK -- consider promoting it on-disk (like the checklist) since the gate enforces it; the addendum is archived under `06-sessions/`.
  2. **`fruit_set_temp_f` schema shape** (warm_arid Aug structural set; surfaced at Steps 4/5).
- **PARKED -- Trevor (minor):** optional `ca_south_coast` z9 soft-`cold_pause` revert; lettuce `why_beginner` copy (3 fields) sanity-check; the `sources_summary[19].name` comma-vs-colon one-char copy call (cherry used comma; beefsteak matches).
- **RESOLVED 2026-06-08 (tooling-hardening pass, commits `c1055cf..c7448f0`):** the three parked Claude-Code-lane tooling items are closed. `apply_patch` now ABSORBS claude.ai's patch one-offs (`_meta`/`corrections` wrapper, crop-relative paths, ascii-escaped proposed SHA -- validated against all 3 archived beefsteak patches); `field_classification.py` is the ONE shared backend predicate, so `whole_crop_gate` + `release_verify` + the roster gate agree on `basis_seasoned`/`source_quote` and §D no longer over-flags legacy `zones{}` dashes. (Plus `gen_current_state.py` skeleton generator + `rotate_state_history.py`; Fix 3 -- roster per-crop-vs-standing -- deferred, moot after source_quote.) Tools-only; canonical SHA unchanged. Reviewed clean (all tests green, 3 anchors PASS, history-replay reproduces the chain).

## Gate record (2026-06-08, on canonical `ab389f72`)
- **lettuce `PASS` (0); cherry `PASS` (0); beefsteak `PASS` (0)**; all three `verified_gs_arc`, launch_ready true. **register_completeness_gate: PASS (0)** -- the 24-pattern `source_quote` HALT is resolved dataset-wide.

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
