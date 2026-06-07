# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If your MEMORY conflicts with them, the files win and your memory is STALE -- the dataset advances through sessions faster than memory refreshes. Re-derive arc position from the files, never from memory.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. The checklist's auto-derived denominator is authority over any kickoff's named field list. **Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.**
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry at close, never rewrite it.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai-authored change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session (a vestigial key; an 8-vs-7 count in 5.C; an "8-cells" overcount in 5.D; a date-shape correction in 5e; an add-vs-replace op mislabel + a missing history entry in 6-8). **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---

## 🥬 LETTUCE FLIPPED (M15) · 🍅 CHERRY -- GATE = 0 / PASS, Steps 5-8 COMPLETE; NEXT = Step 2 rider -> Step 11 FLIP (M16, 2026-06-07)
`lettuce-leaf` is the FIRST flipped anchor (1 of 9): `launch_ready_core=True` + `launch_ready_seasoned=True` (`status` stays `"unverified"` pending the M16 vocab decision). **M16 cherry-tomato is nearly done:** Steps 3.5 + 9 + 10 done; all 10 region cells authored AND 4-round-verified (Step 5/5.5); **Steps 6/7/8 (dual-voice beginner siblings) COMPLETE -- the gate is now `0 / PASS`.** What remains is small: the **Step 2 rider** (`gs_exemplar_finding_003`), then **Claude Code Step 11** -- the `launch_ready` reset-then-set + the `status`-vocab three-state decision + certification. **That is the whole arc done -- the first of 9 anchors fully complete.** **Lettuce was NOT touched -- byte-identical, still certified.** **(Operating model: claude.ai authors, Claude Code releases -- now 10 releases, 9 clean + 1 merge.)**

## Canonical pointer
- **Current SHA:** `84b086f170bdf1184c96cb79bf4e1778da5cdfc33755898a56d9d2d9024fa23c` (M16 cherry Steps 6/7/8 -- 27 dual-voice `_beginner` siblings authored, gate 21->0/PASS). `LATEST.txt` session line: `m16_cherry_6_8_beginner_siblings`.
- **claude.ai next: Step 2 rider (`gs_exemplar_finding_003`), OR Claude Code proceeds to Step 11 -- preflight against `84b086f1`.**
- **Predecessor chain:** `84b086f1` (6/7/8 beginner siblings) <- `12348fa0` (5e warm_arid) <- `45d5199f` (5.D tropical+winter) <- `9f61c52f` (5.C two-window/desert) <- `adf9dcb4` (5.B CA single-window) <- `dadd18d1` (5.A northern_tier) <- `eeaeae37` <- `7dd2837e` <- `7d4bf50c` <- `842ee139` <- `bf96d1d1` (catalog +nmsu_donaana_mg) <- `9d8784f7` <- `813bade9` (catalog +ucanr_san_diego_mg) <- `349fb7af` <- `339933f2` <- `f916e8fe` (Steps 9+10) <- `1b4fea68` <- `a65c7175` (Step 3.5) <- `29b3aaa9` (M15 lettuce flip) <- ... (full chain in STATE_HISTORY).
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## What just happened (2026-06-07, session `m16_cherry_6_8_beginner_siblings`) -- GATE TO 0
- **27 dual-voice `_beginner` siblings authored** (claude.ai copy, from the Claude-Code punch list) for crop-level fields that had only a `_seasoned` phrasing. Consumer copy only -- regions byte-identical, no dates/structure touched.
- **21 gate-tracked** (pests/diseases causes, watering, container_notes, rotation, storage, yield_expectations, companions.note) + **6 walker-blind-spot** (`companions.{good,bad}_beginner_seasoned[0-2].why_beginner`).
- **GATE 21 -> 0 / PASS.** The dual-voice coverage gate is satisfied.
- **Two benign process deviations handled:** claude.ai labeled all ops `add` but the keys were present-as-null (applied as a from-guarded set, no clobber); and claude.ai omitted the STATE_HISTORY entry, so Claude Code authored it from the patch.
- **Verified per protocol #6:** gate PASS; release_verify clean (only cherry; lettuce byte-identical; cleared all 21 violations; no novel keys); claim cross-check (all 27 base=null -> authored string == patch value).

## Active work + exact next step -- THE FLIP IS NEXT
- **Step 2 rider (small):** `gs_exemplar_finding_003` extreme-zone record. claude.ai's lane if it needs authored content; otherwise a structural note.
- **THEN Claude Code Step 11 -- the per-crop flip (the finish line for cherry):**
  1. **`launch_ready` reset-then-set:** clear the stale M10 `launch_ready=true` artifact, then set `launch_ready_core=True` + `launch_ready_seasoned=True` on the now-fully-verified cherry (gate=0, 10/10 cells, dual-voice complete) -- matching the lettuce flip pattern.
  2. **`status`-vocab THREE-state decision (Appendix B item 1):** cherry is `"verified_retro_complete"`, lettuce `"unverified"`. Decide the unified successor (leaning `verified_arc`) AT this flip and back-apply to lettuce. Do NOT set before decided.
  3. **Certify.** After the flip, cherry is the first FULLY-complete gold-standard anchor (1 of 9), the template every later crop follows. Then beefsteak.
- **Parked Trevor items (non-blocking):** `fruit_set_temp_f` schema shape (T1 anchors in hand: az2078 / UC IPM / CR457 / San Diego MG / VH021 / s1b_finding_006 -- schema-touching, Trevor rules); optional ca_south_coast z9 soft-`cold_pause` revert to `wait`.

## Gate record (2026-06-07, post-6/7/8, GATE-CONFIRMED on canonical)
- **`GATE: PASS` (0 VIOLATIONS).** Dual-voice coverage complete: 0 null siblings; 0 region_notes-null; 0 anchoring gaps; 0 uncatalogued; §A2 shape classes 0; §C/D 0; §F 0. All 10 region cells verified with coherent calendars.
- **NOTE -- the gate's dual-voice walker still has the blind spot** (it counted 21, the real total was 27; the 6 `companions.*.why_beginner` were filled but never gate-visible). For cherry this is now moot (all 27 filled). **OWED: fix the walker so it auto-counts the companions `why_beginner` siblings before beefsteak**, else beefsteak could pass the gate with 6 hidden nulls.

## Region fill state (10 of 10 authored AND 4-round-VERIFIED -- Step 5 COMPLETE)
| region | zones | status | window | heat_pause | second_planting |
|---|---|---|---|---|---|
| `northern_tier` | 3-7 | VERIFIED (5.A) | cold (frost-bracketed) | none (frost-limited) | yes, z6-7 |
| `ca_interior` | 8-9 | VERIFIED (5.B) | single | none | none |
| `ca_north_coast` | 9-10 | VERIFIED (5.B) | single (May) | none (COOL-limited) | none |
| `ca_south_coast` | 9-10 | VERIFIED (5.B) | single (long Apr-Jul15) | none (mild marine) | none |
| `se_gulf` | 8-9 | VERIFIED (5.C) | two-window | month 7 (cherry-narrowed) | yes |
| `ca_desert` | 9-10 | VERIFIED (5.C) | two-window | Jun-Aug (absolute) | yes (Sep) |
| `low_desert_az` | 9 | VERIFIED (5.C) | two-window | Jul-Aug (absolute) | yes (Sep) |
| `fl_peninsula` | 10-11 | VERIFIED (5.D) | near-continuous | Jul-Aug (cherry-narrowed) | none |
| `hawaii_tropical` | 11 | VERIFIED (5.D) | year_round | none (oceanic-tropical) | none |
| `warm_arid` | 8 | VERIFIED (5e) | two-window (Mar + Jul transplants) | month 7 (cherry-narrowed, mirror se_gulf) | yes |

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- ✅ lettuce DONE (1 of 9). **Cherry is READY: gate=0, 10/10 cells verified, dual-voice complete -- only the Step 11 flip remains** (reset-then-set + status vocab + cert). Beefsteak after cherry.
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on 3 provers (lettuce ✅; cherry all 10 cells real-filled + verified ✅; beefsteak owes both). Ships with `zones{}` fallback. **2.9+.** (The plant-astro renderer rewrite -- read `regions{}`, consume `second_planting`, render `cold_pause`/`heat_pause` tokens -- is gated here.)
3. **Authoring-model flip** -- carrots onward authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, **2.9+.** After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial extension are **2.9+.**

## Live locked decisions / guardrails
- **CHERRY HEAT PAUSE is a PER-REGION judgment.** Cherry NARROWS the pause only where heat is marginal: se_gulf z8 + warm_arid z8 = cherry-narrowed single-month (Jul) set-dip; ca_desert + low_desert_az (z9) = climatic-absolute Jun-Aug, NOT narrowed. beefsteak re-derives (likely wider).
- **A heat-set-failure month that is ALSO a planting month = `heat_pause` calendar token + the plant carried by `second_planting{}`** (se_gulf + warm_arid z8, Trevor 2026-06-07). Pause > plant in token precedence; the dedicated second-planting track surfaces the action.
- **WINTER COLD = `cold_pause` calendar token, NO sibling object.** Do NOT add to frost-free zones (z10 rows stay `wait`).
- **DUAL-VOICE: every `_seasoned` data field that is in-scope needs a plain-language `_beginner` sibling** (Steps 6/7/8). Beginner = no jargon/Latin/mechanism-for-its-own-sake; say what it is + what to do. Backend `_seasoned` prose (synthesis_note, *_basis, source_quote) is seasoned-ONLY by design (no beginner sibling). The companions `why_beginner` fields are in-scope but gate-invisible (walker blind spot -- fix owed).
- **`harvest_to_table` T2-as-evidence -- RULED (Trevor 2026-06-05): T1-only, NO grandfathering.**
- **TEMPERATURE in user-facing copy -- canonical `°F`, NEVER spelled "degrees F."** Backend prose may spell it; not policed.
- **WINDOW STRUCTURE is a SOURCE FINDING, not a default.** NEVER carry a multi-window shape on analogy (warm_arid's desert-analogy shape was wrong until the chart was read). The chart is the window-count authority; frost data the date authority; single-source windows disclosed in the seasoned note.
- **CATALOG ADMISSION (county MG = UC ANR/NMSU = T1).** Discovery + verified-URL = claude.ai; catalog write = Claude Code. Opportunistic future admits: a CA desert FALL source; an independent warm_arid fall-window corroborator.
- **`second_planting` structure (Claude Code lane) -- PROVEN on se_gulf, ca_desert, low_desert_az, warm_arid, northern_tier z6/z7.** Discrete (NOT succession). Seasoned-only. Spec in `docs/superpowers/specs/`.
- **Resolved-layer shape standards RATIFIED (2026-06-05):** main = flat cell fields; succession = `succession_spring`/`succession_fall` (lettuce); `second_planting` = discrete-window object (cherry). **Lettuce is NOT reshaped.**
- **REGION SHELL-BUILD RULE + Governing checklist v1.5.** Dataset is authoritative; flag doc lag.
- **Lane split.** STRUCTURAL/MECHANICAL = Claude Code. Biology + consumer copy + voice/IP + URL discovery + dates = claude.ai.
- **Anchoring gate LAYER-SCOPED (1A); keep `zones{}` coherent until Phase C** (renderer still reads it).

## Owed checklist amendments (claude.ai, OPEN)
- `lifted_from_zone`-strip into v1.5 Step 3.5 north text (tool already enforces it).
- `°F`-in-user-facing rule (M16-CA-INT-003) into `tip_region_authoring_standard`.
- Retire the "every region cell needs a county MG" framing (Note A, 5.B).
- Window-structure-is-a-source-finding precedent (Path A is the fallback for visual-chart sources). Fold into Step 5.
- Heat-set-failure-month-that-is-also-a-plant-month = `heat_pause` token + `second_planting{}` action (5e). Fold into calendar-token rules.

## Owed (Claude Code lane, OPEN)
- **Dual-voice-walker blind-spot FIX (now higher priority -- before beefsteak):** make the gate's walker auto-count the `companions.{good,bad}_beginner_seasoned[*].why_beginner` siblings, so a future crop cannot pass with hidden nulls. Cherry's 6 are filled, but the walker still can't see them.
- **`uc_mg` catalog-url nit (5.B):** legacy `mg.ucanr.edu` home vs `ucanr.edu/program/...` anchors. Catalog-hygiene, batched.
- **Pre-commit/promote-wrapper release-verify hook** at the beefsteak/pipeline transition (3 commit types: cell release = full verify; catalog admit = source_catalog-only; doc-only = skip).
