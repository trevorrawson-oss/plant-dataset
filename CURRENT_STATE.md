# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If your MEMORY conflicts with them, the files win and your memory is STALE -- the dataset advances through sessions (including Claude-Code-only catalog admits) faster than any memory refreshes, so memory is always a lagging snapshot. Re-derive arc position from the files, never from memory. Memory may hold stable facts (lanes, methodology, file locations), never the moving SHA/count/next-cell.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list. **Kickoffs SUMMARIZE; they are not authority on arc position -- re-derive the next unowned step from the live crop + the checklist.**
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches; a corrected header on a stale body is worse than a uniformly-stale file). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai-authored cell -- a green gate is NOT a clean release).** Run, in order, and BLOCK on any concern: (a) `python3 tools/whole_crop_gate.py <slug>`; (b) `python3 tools/release_verify.py <candidate.json> --base crops_data_final.json --slug <slug>`; (c) **cross-check the cell against claude.ai's own STATE_HISTORY entry claims** (exact months/dates/keys changed -- did the bytes match what it said? did the COUNTS add up?). Only then PROMOTE (#5). Biology correctness is NOT this step -- that is the Step-5 4-round side-by-side. The cross-check has caught real drift every session (a vestigial key; an 8-vs-7 verified-count in 5.C; an "8-cells" overcount in 5.D; a date-shape correction in 5e).

---

## 🥬 LETTUCE FLIPPED (M15) · 🍅 CHERRY -- STEP 5/5.5 COMPLETE, 10/10 region cells VERIFIED; NEXT = Steps 6/7/8 (M16, 2026-06-07)
`lettuce-leaf` is the FIRST flipped anchor (1 of 9): `launch_ready_core=True` + `launch_ready_seasoned=True` (`status` stays `"unverified"` pending the M16 vocab decision). **M16 is in flight on `cherry-tomato`, CHERRY FIRST then beefsteak.** Steps 3.5 + 9 + 10 done; all 10 region cells authored; **the whole-crop Step 5/5.5 verification pass is COMPLETE -- all 10 region cells 4-round-VERIFIED** (warm_arid was the last, re-authored from the Path-A chart read + flipped this session). **NEXT = Steps 6/7/8** (seasoned depth-lift + beginner siblings incl. `cause_beginner` + the dual-voice coverage gate to 0), then the Step 2 rider (`gs_exemplar_finding_003`), then Claude Code **Step 11** + the `launch_ready` flip + the `status`-vocab decision. **Lettuce was NOT touched -- byte-identical, still certified.** **(Operating model: claude.ai authors, Claude Code releases -- now 9 releases, 8 clean + 1 merge.)**

## Canonical pointer
- **Current SHA:** `12348fa008e88b75e5c8052def049bf44e06f8b099561825c5fd298d3d858508` (M16 cherry Step 5e -- warm_arid re-authored to the Dona Ana MG chart: 1st planting May->Mar, frost basis -> arid_highland, July heat_pause retained (mirror se_gulf), honest-provenance seasoned note. warm_arid HELD->VERIFIED, 10/10). `LATEST.txt` session line: `m16_cherry_5e_warm_arid`.
- **claude.ai next: Steps 6/7/8 (dual-voice depth-lift + beginner siblings) -- preflight against `12348fa0`.**
- **Predecessor chain:** `12348fa0` (5e warm_arid re-author) <- `45d5199f` (5.D tropical+winter) <- `9f61c52f` (5.C two-window/desert) <- `adf9dcb4` (5.B CA single-window) <- `dadd18d1` (5.A northern_tier) <- `eeaeae37` (northern_tier cells) <- `7dd2837e` (hawaii_tropical) <- `7d4bf50c` (fl_peninsula) <- `842ee139` (warm_arid shell) <- `bf96d1d1` (catalog +nmsu_donaana_mg) <- `9d8784f7` (4 coastal+desert cells) <- `813bade9` (catalog +ucanr_san_diego_mg) <- `349fb7af` (ca_interior) <- `339933f2` (se_gulf) <- `f916e8fe` (Steps 9+10) <- `1b4fea68` (north lifted_from_zone strip) <- `a65c7175` (Step 3.5 region shells) <- `29b3aaa9` (M15 lettuce flip) <- ... (full chain in STATE_HISTORY).
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## What just happened (2026-06-07, session `m16_cherry_5e_warm_arid`) -- warm_arid re-author, the LAST cell
- **warm_arid (zone 8, S. NM / Las Cruces) re-authored to the Path-A chart read and FLIPPED HELD->VERIFIED.** 25 edits, only warm_arid changed, gate held at 21.
- **First planting corrected (the core fix):** was spring transplant **May 1-21** (desert-analogy error), now **Mar 19 - Apr 8** (start_indoors Feb 5-19); rule offset 14->0 from `last_frost`; harvest_start Jul 1->May 18; harvest_end Oct 21->Nov 5; harvest envelope "May-Jun, Sep-Nov".
- **Frost basis switched** generic zone-8 -> `arid_highland` variant (last_spring Mar 19, first_fall Nov 12), NOAA-cross-checked; new nested `plantings_provenance.frost_basis`.
- **Second planting kept** (start_indoors Jun 3-17, plant_out Jul 15-Aug 4 = the chart's mid-July transplant); harvests re-derived (Sep 13 / Nov 5).
- **July encoding = heat_pause (Option 2, Trevor's call):** the fall crop transplants IN July, but July is the peak fruit-set-failure window -> calendar token `heat_pause` with the plant carried by the `second_planting{}` object on its own track. Calendar is now BYTE-IDENTICAL to se_gulf z8; harvest_start-Sep / calendar-Sep-growing mirrors se_gulf's identical convention (verified parity).
- **Honest-provenance seasoned region_note** authored (Trevor's ask): discloses the second planting rests on the single Dona Ana MG Las Cruces chart, uncorroborated; beginner stays plain.
- **Verified per protocol #6:** gate 21 (held); release_verify clean exit 0 (only warm_arid; no novel keys; warm_arid off the wait-list); claim cross-check byte-confirmed. **SUPERSEDED two 5.D warm_arid tokens** (Feb cold_pause->start_indoors; Apr wait->growing) -- legitimate, 5.D worked the pre-correction shape.

## Active work + exact next step
- **Step 5/5.5 is COMPLETE (10/10 cells verified). The next step is STEPS 6/7/8 (claude.ai):** seasoned depth-lift; beginner siblings incl. `cause_beginner`; **dual-voice coverage gate to 0 (author ~27, gate displays 21 -- see blind spot).** Then the **Step 2 rider** (`gs_exemplar_finding_003` extreme-zone record). Then Claude Code **Step 11** + flip + the `launch_ready` reset.
- **`status`-vocab decision owed (Appendix B item 1) -- THREE-state unification.** Cherry `"verified_retro_complete"`; lettuce `"unverified"`. Successor (leaning `verified_arc`) decided at cherry's flip, back-applied. Do NOT set before decided + flip fires.
- **Blossom-drop `fruit_set_temp_f` -- T1 anchors in hand, ruling owed (claude.ai surfaces shape, Claude Code adds field).** az2078 (>55°F nights / >90°F pollen) + UC IPM (>95°F CA desert) + CR457 (>95°F day / <55°F night) + San Diego MG 65-90°F + VH021 + s1b_finding_006. Schema-touching -> Trevor rules shape. Deferred to family close.
- **OPTIONAL reversible item (5.D flag, still open):** `ca_south_coast` z9 winter `cold_pause` is the SOFTEST call (region_notes say "late OR absent" coastal frost). Reverts to `wait` if Trevor prefers conservative. Non-blocking.

## Gate record (2026-06-07, post-5e, GATE-CONFIRMED on canonical)
- **`GATE: 21 VIOLATION(S)`** -- all Steps 6/7/8. Composition: **21** dual-voice siblings (gate-counts 21, author ~27 -- see blind spot). **0** region_notes-null; **0** anchoring gaps; **0** uncatalogued. HELD across 5e (warm_arid was a correction of an already-populated cell, not a new fill).
- **§A2 shape classes 0**; `second_planting` validates clean on every two-window cell (se_gulf, ca_desert, low_desert_az, warm_arid, + northern_tier z6/z7); §E 0; §C/D 0; §F 0. ALL 10 region cells carry `region_notes` + coherent calendars.

## Region fill state (10 of 10 authored AND 4-round-VERIFIED -- Step 5 COMPLETE)
| region | zones | status | window | heat_pause | second_planting |
|---|---|---|---|---|---|
| `northern_tier` | 3-7 | VERIFIED (5.A) | cold (frost-bracketed) | none (frost-limited) | yes, z6-7 (structured) |
| `ca_interior` | 8-9 | VERIFIED (5.B) | single | none | none |
| `ca_north_coast` | 9-10 | VERIFIED (5.B) | single (May) | none (COOL-limited) | none |
| `ca_south_coast` | 9-10 | VERIFIED (5.B) | single (long Apr-Jul15) | none (mild marine) | none |
| `se_gulf` | 8-9 | VERIFIED (5.C) | two-window | month 7 (cherry-narrowed) | yes |
| `ca_desert` | 9-10 | VERIFIED (5.C) | two-window | Jun-Aug (absolute) | yes (Sep) |
| `low_desert_az` | 9 | VERIFIED (5.C) | two-window | Jul-Aug (absolute) | yes (Sep) |
| `fl_peninsula` | 10-11 | VERIFIED (5.D) | near-continuous | Jul-Aug (cherry-narrowed) | none |
| `hawaii_tropical` | 11 | VERIFIED (5.D) | year_round | none (oceanic-tropical) | none |
| `warm_arid` | 8 | VERIFIED (5e) | two-window (Mar + Jul transplants) | month 7 (cherry-narrowed, mirror se_gulf) | yes (Jul transplant) |

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- ✅ lettuce DONE (1 of 9). Cherry: Steps 3.5+9+10 done; all 10 cells authored AND Step-5-verified; owes Steps 6-8 + Step 11; the stale M10 `launch_ready=true` resets at the flip. Beefsteak after cherry.
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on 3 provers (lettuce ✅; cherry all 10 cells real-filled + verified ✅; beefsteak owes both). Ships with `zones{}` fallback. **2.9+.** (The plant-astro renderer rewrite -- read `regions{}` + consume `second_planting` + render `cold_pause`/`heat_pause` tokens -- is gated here.)
3. **Authoring-model flip** -- carrots onward authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, **2.9+.** After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial extension are **2.9+.**

## Live locked decisions / guardrails
- **CHERRY HEAT PAUSE is a PER-REGION judgment, NOT universal.** Cherry NARROWS the pause only where heat is marginal, NOT where it is absolute: se_gulf z8 + **warm_arid z8** = a cherry-narrowed single-month (Jul) set-dip (arid nights recover); ca_desert + low_desert_az (z9) = climatic-absolute Jun-Aug, NOT narrowed. fl_peninsula Jul-Aug cherry-narrowed; hawaii_tropical none. **warm_arid sits with se_gulf (narrow), not the z9 deserts (wide)** -- precedent recorded 5e. beefsteak re-derives (likely wider).
- **A heat-set-failure month that is ALSO a planting month is encoded `heat_pause` in the calendar token, with the plant carried by the `second_planting{}` object** (se_gulf z8 + warm_arid z8, Trevor's call 2026-06-07). Pause > plant in the token precedence; the dedicated second-planting track surfaces the action. Keeps `heat_pause.months` ↔ `calendar[month]` coherent for release_verify.
- **WINTER COLD is the default, encoded as a `cold_pause` CALENDAR TOKEN with NO sibling object.** Do NOT add it to frost-free zones (the z10 rows stay `wait`). `wait` = a legitimate non-cold, non-heat out-of-window gap.
- **`harvest_to_table` T2-as-evidence -- RULED (Trevor, 2026-06-05): T1-only as evidence, NO grandfathering.** Replace SOLE-backing T2 with a T1; DROP redundant T2.
- **TEMPERATURE in user-facing copy -- canonical `°F`, NEVER spelled "degrees F" (M16-CA-INT-003).** User-facing strings use `°F`; spelled "N degrees F" is correct + dominant in BACKEND prose (`synthesis_note_seasoned`, `*_basis`, `source_quote`, `step5_verification`) and is NOT policed. (Owed: add to `tip_region_authoring_standard`.)
- **WINDOW STRUCTURE is a SOURCE FINDING, not a default.** Single-window: ca_interior, ca_north_coast, ca_south_coast. Two-window (source-confirmed): se_gulf, ca_desert, low_desert_az, warm_arid (chart-confirmed). fl_peninsula near-continuous; hawaii_tropical year_round. **NEVER carry a multi-window shape on analogy** -- warm_arid's desert-analogy shape was WRONG (1st planting off by 2 months) until the Dona Ana chart was actually read (Path A). The chart is the window-count authority; frost data is the date authority; they are sourced separately and the single-source fall window is disclosed in the seasoned note.
- **CATALOG ADMISSION (county MG = UC ANR/NMSU = T1).** UC MG + NMSU county MG are extension T1, admissible. statewide `uc_mg` IS the authoritative publisher of Table 13.2. LANE: discovery + verified-live-URL = claude.ai; catalog write = Claude Code. Opportunistic future admits: a CA desert FALL source (ca_desert, non-blocking); an independent warm_arid fall-window corroborator (would strengthen the currently-single-source note).
- **`second_planting` structure (Claude Code lane) -- PROVEN on se_gulf, ca_desert, low_desert_az, warm_arid, northern_tier z6/z7.** Shape: `resolved_by_zone[z].second_planting = {start_indoors, plant_out, harvest_start, harvest_end, sources, anchoring_urls}` + region-constant `plantings[]` `track:"second_planting"`. Cell dates = envelope across bands. Discrete (NOT succession). Seasoned-only. Spec: `docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`. DEFERRED UI question -> Phase C.
- **Resolved-layer shape standards RATIFIED (2026-06-05):** main = flat cell fields; succession = `succession_spring`/`succession_fall` (lettuce); `second_planting` = discrete-window object (cherry). **Lettuce is NOT reshaped.**
- **REGION SHELL-BUILD RULE:** every crop builds all 10 cells to the lettuce bar. North FROM legacy cold `zones{}`; warm/CA re-derive from T1. `whole_crop_gate.py` §A2 enforces structure. **Owed: claude.ai folds the lifted_from_zone-strip into checklist v1.5 Step 3.5 text.**
- **Governing checklist: v1.5.** Dataset is authoritative; flag doc lag.
- **Lane split.** STRUCTURAL/MECHANICAL = Claude Code. Biology + consumer copy + voice/IP + URL discovery + which-zones/dates + the T2 ruling = claude.ai.
- **Anchoring gate is LAYER-SCOPED (1A);** **keep `zones{}` coherent until Phase C** (the renderer still reads it).

## Owed checklist amendments (claude.ai, OPEN)
- `lifted_from_zone`-strip into v1.5 Step 3.5 north sub-procedure text (tool already enforces it).
- dual-voice-walker blind-spot note (the 6 uncounted `why_beginner` companion siblings) for Claude Code.
- `°F`-in-user-facing-copy rule (M16-CA-INT-003) into `tip_region_authoring_standard`.
- Retire the "every region cell needs a county MG" framing (Note A, 5.B).
- Window-structure-is-a-source-finding precedent (5.C/5e/warm_arid): NEVER carry a multi-window shape on analogy -- a readable source must STATE or SHOW the structure (Path A is the fallback when the source is a visual chart). Fold into Step 5.
- Heat-set-failure-month-that-is-also-a-plant-month = `heat_pause` token + `second_planting{}` action (5e precedent). Fold into the calendar-token rules.

## Owed (Claude Code lane, OPEN)
- **`uc_mg` catalog-url nit (5.B):** legacy `https://mg.ucanr.edu` home vs `ucanr.edu/program/...` anchors. Catalog-hygiene, batched.
- **Pre-commit/promote-wrapper release-verify hook** -- enforce protocol #6 at the beefsteak/pipeline transition (3 commit types: cell release = full verify; catalog admit = source_catalog-only; doc-only = skip). Deferred from manual cherry phase.
