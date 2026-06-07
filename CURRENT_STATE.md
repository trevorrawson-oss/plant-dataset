# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If your MEMORY conflicts with them, the files win and your memory is STALE -- the dataset advances through sessions (including Claude-Code-only catalog admits) faster than any memory refreshes, so memory is always a lagging snapshot. Re-derive arc position from the files, never from memory. Memory may hold stable facts (lanes, methodology, file locations), never the moving SHA/count/next-cell.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list. **Kickoffs SUMMARIZE; they are not authority on arc position -- re-derive the next unowned step from the live crop + the checklist.**
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches; a corrected header on a stale body is worse than a uniformly-stale file). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai-authored cell -- a green gate is NOT a clean release).** Run, in order, and BLOCK on any concern: (a) `python3 tools/whole_crop_gate.py <slug>` (the shape FLOOR); (b) `python3 tools/release_verify.py <candidate.json> --base crops_data_final.json --slug <slug>` (collateral, violation-diff, calendar coherence, user-facing dash/temp scan, exemplar key-diff, region_notes presence -- exits 1 on hard concerns; pause-legibility/biology surface as non-blocking Step-5.5 notes); (c) **cross-check the cell against claude.ai's own STATE_HISTORY entry claims** (exact months/dates/keys changed -- did the bytes match what it said? did the COUNTS add up?). Only then PROMOTE (#5). Biology correctness is NOT this step -- that is the Step-5 4-round side-by-side. The cross-check has caught real drift each session (a vestigial key the gate can't see; an 8-vs-7 verified-count in 5.C; an "8-cells" overcount in 5.D).

---

## 🥬 LETTUCE FLIPPED (M15) · 🍅 CHERRY -- Step 5/5.5 verification COMPLETE (9/10; warm_arid HELD); NEXT = Steps 6/7/8 (M16, 2026-06-07)
`lettuce-leaf` is the FIRST flipped anchor (1 of 9): `launch_ready_core=True` + `launch_ready_seasoned=True` (`status` stays `"unverified"` pending the M16 vocab decision). **M16 is in flight on `cherry-tomato`, CHERRY FIRST then beefsteak.** Steps 3.5 + 9 + 10 done; all 10 region cells authored; **the whole-crop Step 5/5.5 verification pass (4-round side-by-side + calendar coherence) is COMPLETE across sub-sessions 5.A-5.D -- 9 of 10 region cells 4-round-VERIFIED.** The 10th, **`warm_arid`, is HELD**: its two-window structure is now CONFIRMED (Trevor read the Dona Ana MG chart, Claude Code verified the screenshot) but a date-correction + region_note re-authoring is owed to claude.ai before it flips. **NEXT = Steps 6/7/8** (seasoned depth-lift + beginner siblings + dual-voice gate to 0), then Step 2 rider, then Claude Code Step 11 + the `launch_ready` flip. **Lettuce was NOT touched -- byte-identical, still certified.** **(Operating model: claude.ai authors, Claude Code releases -- now 8 releases, 7 clean + 1 merge.)**

## Canonical pointer
- **Current SHA:** `45d5199f4e4adc335ef23bf510195815dea0b2dca6fe841610f90a7c3f26fee8` (M16 cherry Step 5.D -- tropical/peninsula verified + the consolidated winter-`wait`->`cold_pause` ruling; calendar-token + backend only, NO date moves). `LATEST.txt` session line: `m16_cherry_5d_tropical_winter`.
- **claude.ai next: warm_arid re-authoring (chart read done) OR Steps 6/7/8 -- preflight against `45d5199f`.**
- **Predecessor chain:** `45d5199f` (5.D tropical+winter) <- `9f61c52f` (5.C two-window/desert) <- `adf9dcb4` (5.B CA single-window) <- `dadd18d1` (5.A northern_tier) <- `eeaeae37` (northern_tier cells) <- `7dd2837e` (hawaii_tropical) <- `7d4bf50c` (fl_peninsula) <- `842ee139` (warm_arid) <- `bf96d1d1` (catalog +nmsu_donaana_mg) <- `9d8784f7` (4 coastal+desert cells) <- `813bade9` (catalog +ucanr_san_diego_mg) <- `349fb7af` (ca_interior) <- `339933f2` (se_gulf) <- `f916e8fe` (Steps 9+10) <- `1b4fea68` (north lifted_from_zone strip) <- `a65c7175` (Step 3.5 region shells) <- `29b3aaa9` (M15 lettuce flip) <- ... (full chain in STATE_HISTORY).
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## What just happened (2026-06-07, session `m16_cherry_5d_tropical_winter`) -- STEP 5/5.5 5.D (LAST Step-5 sub-session)
- **Sub-session 5.D released (PATCH, 19 edits: 15 calendar-token + 2 delete_key + 2 add_key).** Bytes changed on **7 cells** (the entry said 8 -- an overcount; cross-check corrected it); **NO planting/harvest date moved anywhere** (date guard confirmed).
- **PART 1 -- `fl_peninsula` + `hawaii_tropical` 4-round VERIFIED, both PASS** (UF/IFAS VH021/EP452 for FL; CTAHR HGV-5 for HI -- `year_round:true` + positive no-heat_pause confirmed at source). The vestigial empty `sources_pending_admission` key DROPPED on both; a `plantings_provenance.step5_verification` stamp added (records the this-arc side-by-side, not inherited).
- **PART 2 -- whole-crop NON-regional sourced fields: VERIFIED-AS-COVERED, zero edits by design.** Every crop-level sourced field already carries `verification_status=verified_retro_complete` from the cherry retro (the separate 10-session crop-level workstream); the region passes added/changed no crop-level field, so no gap remained for 5.D. Only genuinely arc-pending whole-crop item = the schema-touching `fruit_set_temp_f` (Trevor ruling).
- **PART 3 -- consolidated Step-5.5 WINTER ruling: 15 winter months `wait`->`cold_pause`** (calendar-token only, NO cold_pause object -- matches northern_tier 5.A precedent): se_gulf z8 Jan/Dec; ca_interior z8 Jan, z9 Jan/Dec; ca_north_coast z9 Jan/Feb/Nov/Dec; ca_south_coast z9 Jan/Feb/Dec; warm_arid z8 Jan/Feb/Dec. **7 counter-candidates KEPT as `wait`:** the two FROST-FREE z10 rows (ca_north_coast z10, ca_south_coast z10) + warm_arid z8 April (between-window gap). Summer-pause legibility was already cleared in 5.C.
- **Verified per protocol #6 + the 5 followups:** gate 21 (unchanged); release_verify clean exit 0 (check C now 3 wait-notes = exactly the kept counter-candidates; check E fully clean); claim cross-check byte-confirmed (15 tokens, 7 kept, 2 deleted, 2 stamped); followup-2 coherence (every new cold_pause month was previously `wait`).

## warm_arid -- chart READ done, two-window CONFIRMED; date correction + region_note AUTHORING OWED (claude.ai)
- **Path A read DONE 2026-06-07:** Trevor opened the Shillingburg / Dona Ana MG chart (`donaanamastergardeners.nmsu.edu/documents/foodgardenplantingchart-1.pdf`, catalogued T1 `nmsu_donaana_mg`); Claude Code confirmed the tomato row from a screenshot (archived `06-sessions/.../m16-cherry-releases/warm_arid_path_a_evidence/`). The chart STATES a genuine **two-window** structure. **Tomato row, verified:** 1st = start indoors ~mid-Jan -> **transplant early March**; 2nd = start ~mid-June -> **transplant ~mid-July** (planting/transplant timing only, not harvest).
- **THE CORRECTION:** the current cell was DESERT-ANALOGY-authored and is WRONG on the first planting -- it has spring `plant_out` **May 1-21** (start_indoors Mar 20), but the chart says **early March** (start indoors mid-Jan), ~2 months earlier. The SECOND planting is already ~right (current `plant_out` Jul 15-Aug 4 / `start_indoors` Jun 3-17 ≈ the chart's mid-July transplant / mid-June start). The first-planting shift cascades into harvests, the July heat treatment, and the calendar.
- **Trevor's product call:** KEEP the second planting; add an HONEST-PROVENANCE seasoned `region_note` disclosing it comes from the Dona Ana County MG (Las Cruces) chart -- a single regional MG source, not independently corroborated.
- **AUTHORING OWED (claude.ai lane):** re-author warm_arid z8 to the chart (1st transplant -> early March WITH frost/beginner-safety reconciliation as for low_desert_az's mid-March call; re-derive harvests; re-judge the July heat_pause; dual-register region_notes incl. the honesty note via the copywriting skill). Claude Code then releases -> warm_arid flips HELD->verified (10/10). A paste-ready relay sits at `~/Downloads/warm_arid_chart_read_RELAY_for_claude_ai.txt`. The winter cold_pause (Jan/Feb/Dec) + April-stays-wait already shipped in 5.D and are correct under the confirmed two-window shape.

## Active work + exact next step
- **Step 5/5.5 is COMPLETE (9/10 cells verified).** Two parallel threads now:
  - **(thread A) warm_arid re-authoring** (claude.ai; chart read done -- see above). Flips the last cell to 10/10. Independent of Steps 6-8.
  - **(thread B) Steps 6/7/8 = the main next step.** Seasoned depth-lift; beginner siblings incl. `cause_beginner`; **dual-voice coverage gate to 0 (author ~27, gate displays 21 -- see blind spot).** Then the **Step 2 rider** (`gs_exemplar_finding_003`). Then Claude Code **Step 11** + flip + the `launch_ready` reset.
- **`status`-vocab decision still owed (Appendix B item 1) -- THREE-state unification.** Cherry `"verified_retro_complete"`; lettuce `"unverified"`. Successor (leaning `verified_arc`) decided at cherry's flip, back-applied. Do NOT set before decided + flip fires.
- **Blossom-drop `fruit_set_temp_f` -- T1 anchors in hand, ruling owed.** az2078 (>55°F nights / >90°F pollen) + UC IPM (>95°F CA desert) + San Diego MG 65-90°F + VH021 + s1b_finding_006. Schema-touching -> Trevor rules shape. Deferred to family close.
- **OPTIONAL reversible item (5.D flag):** `ca_south_coast` z9 winter `cold_pause` is the SOFTEST call (region_notes bound the season by "the late OR ABSENT coastal frost"). Ruled cold_pause on the cooler-inland-edge read; reverts to `wait` if Trevor prefers the conservative reading. Non-blocking.

## Gate record (2026-06-07, post-5.D, GATE-CONFIRMED on canonical)
- **`GATE: 21 VIOLATION(S)`** -- all Steps 6/7/8. Composition: **21** dual-voice siblings (gate-counts 21, author ~27 -- see blind spot). **0** region_notes-null; **0** anchoring gaps; **0** uncatalogued. UNCHANGED across 5.D (calendar tokens + empty-key deletes + nested backend stamps are all gate-invisible).
- **§A2 shape classes 0**; `second_planting` validates clean on every two-window cell; §E 0 uncatalogued / 0 non-T1; §C/D 0; §F 0 gaps. ALL 10 region cells carry `region_notes` + coherent calendars.

## Region fill state (10 of 10 authored; 9/10 4-round-VERIFIED, warm_arid HELD)
| region | zones | status | window | heat_pause | second_planting |
|---|---|---|---|---|---|
| `northern_tier` | 3-7 | VERIFIED (5.A) | cold (frost-bracketed) | none (frost-limited) | yes, z6-7 (structured) |
| `ca_interior` | 8-9 | VERIFIED (5.B) | single | none | none |
| `ca_north_coast` | 9-10 | VERIFIED (5.B) | single (May) | none (COOL-limited) | none |
| `ca_south_coast` | 9-10 | VERIFIED (5.B) | single (long Apr-Jul15) | none (mild marine) | none |
| `se_gulf` | 8-9 | VERIFIED (5.C) | two-window | month 7 (cherry-narrowed) | yes |
| `ca_desert` | 9-10 | VERIFIED (5.C) | two-window | Jun-Aug (absolute) | yes (Sep) -- fall band on mechanism+az2078 |
| `low_desert_az` | 9 | VERIFIED (5.C) | two-window | Jul-Aug (absolute, corrected) | yes (Sep) |
| `fl_peninsula` | 10-11 | VERIFIED (5.D) | near-continuous (z10+z11 distinct) | Jul-Aug (cherry-narrowed) | none |
| `hawaii_tropical` | 11 | VERIFIED (5.D) | year_round (all-active) | none (oceanic-tropical) | none |
| `warm_arid` | 8 | **HELD** -- two-window CONFIRMED (chart); dates+note authoring owed | two-window (chart: Mar + Jul transplants) | July? (re-judge in re-author) | yes (start Jun -> transplant ~mid-Jul) |

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- ✅ lettuce DONE (1 of 9). Cherry mid-arc (Steps 3.5+9+10 done; all 10 cells authored; Step 5/5.5 done 9/10, warm_arid HELD; owes warm_arid re-author + Steps 6-8 + Step 11; the stale M10 `launch_ready=true` resets at the flip). Beefsteak after cherry.
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on 3 provers (lettuce ✅; cherry all 10 cells real-filled ✅; beefsteak owes both). Ships with `zones{}` fallback. **2.9+.** (The plant-astro renderer rewrite -- read `regions{}` + consume `second_planting`, and now render `cold_pause` calendar tokens -- is gated here.)
3. **Authoring-model flip** -- carrots onward authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, **2.9+.** After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial extension are **2.9+.**

## Live locked decisions / guardrails
- **CHERRY HEAT PAUSE is a PER-REGION judgment, NOT universal.** se_gulf: narrowed to month 7. ca_desert + low_desert_az: NOT narrowed (climatic-absolute; low_desert_az corrected to Jul-Aug). fl_peninsula: Jul-Aug cherry-narrowed. hawaii_tropical: none (year_round). Apply per region from the source. beefsteak re-derives.
- **WINTER COLD is the expected default, encoded as a `cold_pause` CALENDAR TOKEN with NO sibling object** (northern_tier 5.A + the 5.D winter ruling). A `cold_pause` token asserts a real frost trough outside every window; do NOT add it to frost-free zones (the z10 rows stay `wait`). `wait` = a legitimate non-cold, non-heat between-window/out-of-window gap.
- **`harvest_to_table` T2-as-evidence -- RULED (Trevor, 2026-06-05): T1-only as evidence, NO grandfathering.** Replace SOLE-backing T2 with a T1; DROP redundant T2. De-citation is whole-crop.
- **TEMPERATURE in user-facing copy -- canonical `°F`, NEVER spelled "degrees F" (M16-CA-INT-003).** User-facing strings use `°F`; §C/D enforces user-facing only. Spelled "N degrees F" is correct + dominant in BACKEND prose (`synthesis_note_seasoned`, `heat_pause.basis_seasoned`, `source_quote`, `step5_verification`) and is NOT policed. (Owed: add to `tip_region_authoring_standard`.)
- **WINDOW STRUCTURE is a SOURCE FINDING, not a default.** Single-window: ca_interior, ca_north_coast, ca_south_coast. Two-window (source-confirmed): se_gulf, ca_desert, low_desert_az, **warm_arid (chart-confirmed 2026-06-07 -- Mar + Jul transplant bands)**. fl_peninsula near-continuous; hawaii_tropical year_round. Never carry a multi-window shape on analogy -- warm_arid's was wrong until the chart was actually read.
- **CATALOG ADMISSION (county MG = UC ANR/NMSU = T1).** UC MG county programs + NMSU county MG are extension T1, admissible. statewide `uc_mg` IS the authoritative publisher of Table 13.2 (county MGs corroborate where they carry region-specific prose). LANE: discovery + verified-live-URL = claude.ai; catalog write = Claude Code. Opportunistic future admits: a CA desert FALL source (ca_desert, non-blocking); any new readable warm_arid corroborator.
- **`second_planting` structure (Claude Code lane) -- PROVEN on se_gulf + ca_desert + low_desert_az + northern_tier z6/z7; warm_arid pending re-author.** Shape: `resolved_by_zone[z].second_planting = {start_indoors, plant_out, harvest_start, harvest_end, sources, anchoring_urls}` + region-constant `plantings[]` `track:"second_planting"`. Cell dates = envelope across bands. Discrete (NOT succession). Seasoned-only. Spec: `docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`. DEFERRED UI question -> Phase C read-layer.
- **Resolved-layer shape standards RATIFIED (2026-06-05):** main = flat cell fields; succession = `succession_spring`/`succession_fall` (lettuce); `second_planting` = discrete-window object (cherry). Each crop carries ONLY its structures. **Lettuce is NOT reshaped.**
- **REGION SHELL-BUILD RULE:** every crop builds all 10 cells to the lettuce bar. North FROM legacy cold `zones{}` (promote + verify + hoist succession; strip nested `plantings`; re-stamp `zone_promoted_verified`; strip tautological `lifted_from_zone`). Warm/CA re-derive from T1. `whole_crop_gate.py` §A2 enforces structure. **Owed: claude.ai folds the lifted_from_zone-strip into checklist v1.5 Step 3.5 text.**
- **Governing checklist: v1.5.** Dataset is authoritative; flag doc lag.
- **Lane split.** STRUCTURAL/MECHANICAL = Claude Code (region shells, transforms, gates, audits, SHA re-pins, flips, `second_planting`, dual-voice-walker fix, catalog admission, envelope/coherence recompute). Biology + consumer copy + voice/IP + URL discovery + which-zones/dates + the T2 ruling = claude.ai.
- **Anchoring gate is LAYER-SCOPED (1A):** claim-bearing leaves only; legacy `zones{}` + the 10 `regions{}` root rollup `sources` arrays excluded; sibling `*_sources`/`*_anchoring_urls` pairs included; `bolting.*` inherit-class excluded.
- **Keep `zones{}` coherent until Phase C.** The current renderer still reads `zones{}`.

## Owed checklist amendments (claude.ai, OPEN)
- `lifted_from_zone`-strip into v1.5 Step 3.5 north sub-procedure text (tool already enforces it).
- dual-voice-walker blind-spot note (the 6 uncounted `why_beginner` companion siblings) for Claude Code.
- `°F`-in-user-facing-copy rule (M16-CA-INT-003) into `tip_region_authoring_standard`.
- Retire the "every region cell needs a county MG" framing (Note A, 5.B).
- Window-structure-is-a-source-finding precedent (5.C/warm_arid): NEVER carry a multi-window shape on analogy -- a readable source must STATE or SHOW the structure. Fold into Step 5.

## Owed (Claude Code lane, OPEN)
- **warm_arid re-authoring release** (after claude.ai authors the chart-corrected dates + honesty region_note) -- flips it to verified, 10/10.
- **`uc_mg` catalog-url nit (5.B):** legacy `https://mg.ucanr.edu` home vs `ucanr.edu/program/...` anchors. Catalog-hygiene, batched.
- **Pre-commit/promote-wrapper release-verify hook** -- enforce protocol #6 at the beefsteak/pipeline transition (3 commit types: cell release = full verify; catalog admit = source_catalog-only; doc-only = skip). Deferred from manual cherry phase.
