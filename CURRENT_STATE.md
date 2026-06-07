# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list. **Kickoffs SUMMARIZE; they are not authority on arc position -- re-derive the next unowned step from the live crop + the checklist.**
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches; a corrected header on a stale body is worse than a uniformly-stale file). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push).

---

## 🥬 LETTUCE FLIPPED (M15) · 🍅 CHERRY Step 4 IN PROGRESS -- 8 of 10 REGION CELLS SOURCED (M16, 2026-06-06)
`lettuce-leaf` is the FIRST flipped anchor (1 of 9): `launch_ready_core=True` + `launch_ready_seasoned=True` (`status` stays `"unverified"` pending the M16 vocab decision). **M16 is in flight on `cherry-tomato`, CHERRY FIRST then beefsteak.** Cherry has completed **Step 3.5** (region shells, Claude Code), **Step 9** (residual source-name dash), **Step 10** (`harvest_to_table` T2-as-evidence ruling), and **Step 4 is in progress: 8 of 10 region cells sourced -- `se_gulf`, `ca_interior`, `ca_north_coast`, `ca_south_coast`, `ca_desert`, `low_desert_az`, `warm_arid`, `fl_peninsula`.** **NEXT = `hawaii_tropical`, then `northern_tier` calendar work**, then Steps 5-8, then Claude Code Step 11. **Lettuce was NOT touched -- byte-identical, still certified.** **(Operating model: claude.ai authors, Claude Code releases -- now 2 clean runs; see STATE_HISTORY.)**

## Canonical pointer
- **Current SHA:** `7d4bf50cc56801017ed30d027343c55378a4ffe7631a736dd93284b2ade48140` (M16 cherry Step 4 -- `fl_peninsula` cell: claude.ai authored, Claude Code released CLEAN, no merge/normalization). `LATEST.txt` session line: `m16_cherry_step4_fl_peninsula`.
- **claude.ai: preflight the next cell (`hawaii_tropical`) against `7d4bf50c`.**
- **Predecessor chain:** `7d4bf50c` (fl_peninsula) <- `842ee139` (warm_arid) <- `bf96d1d1` (catalog +nmsu_donaana_mg) <- `9d8784f7` (4 coastal+desert cells) <- `813bade9` (catalog +ucanr_san_diego_mg) <- `349fb7af` (ca_interior) <- `339933f2` (se_gulf) <- `f916e8fe` (Steps 9+10) <- `1b4fea68` (north `lifted_from_zone` strip) <- `a65c7175` (Step 3.5 region shells + `second_planting`) <- `29b3aaa9` (M15 lettuce flip) <- ... (full chain in STATE_HISTORY).
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## What just happened (2026-06-06, session `m16_cherry_step4_fl_peninsula`) -- SECOND RUN OF THE NEW MODEL, CLEAN
- **`fl_peninsula` (zones 10-11, South Florida) released CLEAN** -- no merge, no normalization. claude.ai applied every warm_arid lesson: authored on the CORRECT base (`842ee139`); cited already-catalogued `uf_ifas_vh021` + `uf_ifas_south_cal` (NOT the `ufifas_ext` scout ID) so NO admit needed; cleared its own stale pending markers; used `°F`.
- **Encoding rulings (Trevor + Claude Code):** **Q1 = B** -- cherry-narrowed soft `heat_pause` `[7,8]` (the two peak >78°F-night months), honoring BOTH the source's cherry-summer-tolerant signal AND the new-fruit-set-stop (vs A's cool-season-only or C's `year_round`). **Q2 = two distinct zone resolutions** (z10 + z11, source-decided per VH021/EP452, not legacy-carried).
- **Gate: residual 25 -> 24** (fl_peninsula region_notes cleared; the 24 all downstream: 2 region_notes-null + 21 dual-voice + 1 cornell_ext). Only `cherry-tomato` changed; catalog 82 unchanged; §A2 shape 0; §E 0 uncatalogued; §F only the pre-existing cornell gap; lettuce byte-identical `GATE: PASS`. Owed-to-claude.ai (Step 5/5.5): confirm `[7,8]` cherry-narrow + the z10/z11 split at side-by-side.
- **Operating model (now 2 clean runs):** claude.ai outputs ONLY the updated JSON + a STATE_HISTORY entry snippet (never the whole HISTORY, never LATEST/CURRENT/SHA). Claude Code verifies, computes the SHA, re-pins LATEST, regenerates THIS file, appends the entry, syncs `00-current`, commits + pushes. Cell-by-cell Step-4 detail lives in STATE_HISTORY.
- **Standing Step-11 item (flagged by claude.ai):** cherry's `launch_ready_core/seasoned: true` are stale M10 per-zone-standard artifacts and CONFLICT with the Step-11 entry guard (which expects both-false at entry, as lettuce did). Claude Code reconciles at the flip (reset to false, then flip under arc rigor). Left untouched mid-arc; parked.


## Active work + exact next step
- **M16 cherry: Steps 3.5 + 9 + 10 DONE; Step 4 IN PROGRESS (8 of 10 cells done -- `fl_peninsula` released this session). NEXT = `hawaii_tropical` (claude.ai), then `northern_tier` calendar.** Per `region_source_map` anchors. **Preflight against `7d4bf50c`.**
  - **`hawaii_tropical` (CTAHR B-91, zone 11) -- crop-distributed timing; year-round encoding may apply** (lettuce Hawaii precedent: `year_round:true` + `calendar_basis` + 12-month all-active calendar). `uhawaii_ctahr` catalogued.
  - **`northern_tier` (zones 3-7)** -- promoted-verified (cold); owes `calendar[12]` cold_pause derivation (Step 5.5) + region_notes pair (Steps 6/7). Winter-gap months `wait`, owe `cold_pause` (frost-limited, NO midsummer heat_pause up north).
- **Then in sequence:** Step 5/5.5 (4-round side-by-side on every claim incl. all region windows authored; derive every region `calendar[12]`; classify north winter gaps as `cold_pause`; discover `cornell_ext` zone-6 URL). Steps 6/7/8 (seasoned depth-lift; beginner siblings incl. `cause_beginner`; remaining `region_notes_*` pairs; dual-voice coverage gate to 0 -- **author 27, gate displays 21**, see blind spot). Step 2 rider (`gs_exemplar_finding_003`). Then Claude Code **Step 11** + flip.
- **`status`-vocab decision still owed (Appendix B item 1) -- THREE-state unification.** Cherry `"verified_retro_complete"`; lettuce `"unverified"`. Successor (leaning `verified_arc`) decided at cherry's flip, back-applied. Do NOT set before decided + flip fires.
- **Blossom-drop `fruit_set_temp_f` -- T1 anchors in hand, ruling owed (claude.ai surfaces shape, Claude Code adds field).** Now includes the San Diego MG 65°F–90°F range (in `ca_south_coast` provenance) + VH021 + s1b_finding_006 (Clemson/PSU: >90°F day, <55°F night). Schema-touching → Trevor rules shape. Rule with s1b_finding_006 (deferred to family close).

## Gate record (2026-06-06, post-`fl_peninsula`, GATE-CONFIRMED on canonical)
- **`GATE: 24 VIOLATION(S)`** -- all downstream. Composition: **2** region_notes-null (`hawaii_tropical`, `northern_tier`), **21** dual-voice siblings (Steps 7/8; gate-counts 21, author ~27 -- see blind spot), **1** `cornell_ext` zone-6 URL (Step 5).
- **§A2 shape classes 0** (`stub:0 | null-track:0 | stale nested:0`); `second_planting` validates clean on the two-window cells (`ca_desert`, `low_desert_az`, `warm_arid`); §E 0 uncatalogued / 0 non-T1; §C/D 0 dash / 0 temp-form; §F only the pre-existing cornell gap. 8 of 10 region cells carry `region_notes`.


## Region fill state (8 of 10)
| region | zones | status | window | heat_pause | second_planting |
|---|---|---|---|---|---|
| `northern_tier` | 3-7 | promoted-verified; owes calendar+notes | (cold) | none (frost-limited) | (cold 6-7 TBD) |
| `se_gulf` | 8-9 | FILLED | two-window | month 7 (cherry-narrowed) | yes |
| `ca_interior` | 8-9 | FILLED | single | none | none |
| `ca_north_coast` | 9-10 | FILLED | single (May) | none (COOL-limited) | none |
| `ca_south_coast` | 9-10 | FILLED | single (long Apr-Jul15) | none (mild marine) | none |
| `ca_desert` | 9-10 | FILLED | two-window | Jun-Aug (absolute) | yes (Sep) |
| `warm_arid` | 8 | FILLED | two-window | month 7 (cherry-narrowed) | yes (fall) |
| `low_desert_az` | 9 | FILLED | two-window | Jun-Aug (absolute) | yes (Sep) |
| `fl_peninsula` | 10-11 | FILLED | near-continuous (z10+z11 distinct) | Jul-Aug (cherry-narrowed) | none |
| `hawaii_tropical` | 11 | PENDING | TBD (year-round?) | n/a | n/a |

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- ✅ lettuce DONE (1 of 9). Cherry is mid-arc (Steps 3.5 + 9 + 10 done; Step 4 in progress, 8 of 10 cells done; owes 3 warm regions + northern_tier calendar + Steps 5-8 + 11). Beefsteak after cherry.
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce ✅; cherry shell ✅ + 6 cells real-filled, owes 4 more; beefsteak owes both). Ships with `zones{}` fallback. **2.9+.** (The plant-astro renderer rewrite -- read `regions{}` + consume `second_planting` instead of synthesizing from `zones{}` multi-window strings -- is gated here.)
3. **Authoring-model flip** -- carrots onward authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, **2.9+.** After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial extension are **2.9+.**

## Live locked decisions / guardrails
- **CHERRY HEAT PAUSE is a PER-REGION judgment, NOT universal (reaffirmed across se_gulf vs the deserts, 2026-06-06).** se_gulf: cherry's heat resistance narrowed the summer pause to a single month (month 7). `ca_desert` + `low_desert_az`: the pause is NOT narrowed -- peak desert summer (>95-110°F) is climatic-absolute and stops fruit set even for heat-tolerant cherry. Apply per region from the source; do NOT universalize either direction. beefsteak re-derives (wider).
- **`harvest_to_table` T2-as-evidence -- RULED (Trevor, 2026-06-05): T1-only as evidence, NO grandfathering.** Precedent for every pre-arc-built crop. Where a T2 is the SOLE backing, replace with a T1; where the claim is already T1-anchored and the T2 is redundant, DROP it. De-citation is whole-crop (evidence fields AND registry).
- **TEMPERATURE in user-facing copy -- canonical `°F`, NEVER spelled "degrees F" (M16-CA-INT-003).** region_notes + all user-facing strings use degree-sign `°F`; §C/D enforces on user-facing fields only. Spelled "N degrees F" is correct + dominant in BACKEND prose (`synthesis_note_seasoned`, `heat_pause.basis_seasoned`) and is NOT policed. **All 4 cells this session authored region_notes with `°F` from first draft -- §C/D stayed 0.** (Owed: add to `tip_region_authoring_standard`.)
- **WINDOW STRUCTURE is a SOURCE FINDING, not a default.** One-vs-two windows decided by reading the source. Single-window so far: ca_interior, ca_north_coast, ca_south_coast. Two-window: se_gulf, ca_desert, low_desert_az. **`warm_arid` is held PENDING precisely because its structure is not yet source-confirmed** -- do NOT mirror the desert shape onto it by analogy. Confirm absence of a second window with a second source before authoring single-window.
- **CATALOG ADMISSION (county MG = UC ANR = T1) -- precedent set 2026-06-06.** UC Master Gardener county programs are UC ANR extension, T1, admissible (precedent: `ucanr_marin_mg`, `ucanr_santa_clara_mg`, now `ucanr_san_diego_mg`). LANE: source discovery + verified-live-URL handoff = claude.ai; the catalog write (mint ID, 9-field shape, SHA-gated apply) = Claude Code. claude.ai hands a batch {proposed source, confirmed-live URL, why T1, what it corroborates}; Claude Code admits the T1 ones in one promote, rejects non-T1. Uncatalogued county MGs surfacing mid-arc → flag to a batch, do not introduce inline (§E would fail). UC ANR program URL convention is `ucanr.edu/site/uc-master-gardener-program-{county}-county` (NOT `{county}mg.ucanr.edu`); Master Gardener *Association* `.org` domains are separate -- point catalog `url` at the ucanr.edu program home, treat Association-domain prose as read-not-cited unless independently T1-anchored.
- **`second_planting` structure (Claude Code lane) -- PROVEN on se_gulf + ca_desert + low_desert_az; ABSENT on ca_interior/ca_north_coast/ca_south_coast (single-season).** Shape: `resolved_by_zone[z].second_planting = {start_indoors, plant_out, harvest_start, harvest_end, sources, anchoring_urls}` on applicable zones only, + region-constant `plantings[]` entry `succession_id:2, label:"second", track:"second_planting"`. Cell-level `first_plant_date`/`last_plant_date`/`harvest`/`calendar` = envelope across both bands. Discrete (NOT succession). Seasoned-only visibility. Spec: `docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`. **DEFERRED UI question:** structured single-season flag placement -- decide at Phase C read-layer rewrite.
- **Resolved-layer shape standards RATIFIED (2026-06-05):** main = flat cell fields (universal); succession = `succession_spring`/`succession_fall` (lettuce's shape); `second_planting` = discrete-window object (cherry's shape). Each crop carries ONLY its structures; each concept has ONE fixed shape. **Lettuce is NOT reshaped.**
- **REGION SHELL-BUILD RULE (Trevor 2026-06-05):** every crop's arc builds ALL 10 region cells to the lettuce bar. North (`northern_tier`) builds FROM legacy cold `zones{}` (promote + verify + hoist succession; strip nested cell `plantings`; re-stamp `zone_promoted_verified`; strip the tautological `lifted_from_zone` key). Warm/CA re-derive from T1 (zone data may be climate-contaminated). `whole_crop_gate.py` §A2 enforces the structural side. **Owed: claude.ai folds the `lifted_from_zone`-strip into checklist v1.5 Step 3.5 north sub-procedure text.**
- **Governing checklist: v1.5** (Step 3.5 Region shell build; reference-GS-crop = `lettuce-leaf`; two-callsite admission/certification -- null `region_notes` / empty `anchoring_urls` accepted at Step 3.5, violations at Step 11). Dataset is authoritative; flag doc lag.
- **Lane split.** STRUCTURAL/MECHANICAL = Claude Code (region shells, transforms, gates, audits, SHA re-pins, flips, `second_planting` representation, dual-voice-walker fix, catalog admission). Biology + consumer copy + voice/IP + URL discovery + which-zones/dates for second_planting + the T2 ruling + Appendix-A = claude.ai.
- **Anchoring gate is LAYER-SCOPED (1A):** claim-bearing leaves only; legacy `zones{}` + the 10 `regions{}` root rollup `sources` arrays excluded; sibling-named `*_sources`/`*_anchoring_urls` pairs included; `bolting.*` inherit-class excluded.
- **Keep `zones{}` coherent until Phase C** (deletion gate: region carries everything + consumers read region-first + round-trip + frost-input independence). The current renderer still reads `zones{}`.

## Owed checklist amendments (claude.ai, OPEN)
- `lifted_from_zone`-strip into v1.5 Step 3.5 north sub-procedure text (tool already enforces it).
- dual-voice-walker blind-spot note (the 6 uncounted `why_beginner` companions siblings) for Claude Code.
- `°F`-in-user-facing-copy rule (M16-CA-INT-003) into `tip_region_authoring_standard`.
