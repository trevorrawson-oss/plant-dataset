# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list. **Kickoffs SUMMARIZE; they are not authority on arc position -- re-derive the next unowned step from the live crop + the checklist.**
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches; a corrected header on a stale body is worse than a uniformly-stale file). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push).

---

## 🥬 LETTUCE FLIPPED (M15) · 🍅 CHERRY Step 4 IN PROGRESS -- 7 of 10 REGION CELLS SOURCED (M16, 2026-06-06)
`lettuce-leaf` is the FIRST flipped anchor (1 of 9): `launch_ready_core=True` + `launch_ready_seasoned=True` (`status` stays `"unverified"` pending the M16 vocab decision). **M16 is in flight on `cherry-tomato`, CHERRY FIRST then beefsteak.** Cherry has completed **Step 3.5** (region shells, Claude Code), **Step 9** (residual source-name dash), **Step 10** (`harvest_to_table` T2-as-evidence ruling), and **Step 4 is in progress: 7 of 10 region cells sourced -- `se_gulf`, `ca_interior`, `ca_north_coast`, `ca_south_coast`, `ca_desert`, `low_desert_az`, `warm_arid`.** **NEXT = `fl_peninsula`, `hawaii_tropical`, then `northern_tier` calendar work**, then Steps 5-8, then Claude Code Step 11. **Lettuce was NOT touched -- byte-identical, still certified.** **(New operating model now live: claude.ai authors, Claude Code releases -- see below + STATE_HISTORY.)**

## Canonical pointer
- **Current SHA:** `842ee139c711e533110e6dc3868d77676e85cefda4b98915570d644dbb2327bf` (M16 cherry Step 4 -- `warm_arid` cell: claude.ai authored, Claude Code released via merge). `LATEST.txt` session line: `m16_cherry_step4_warm_arid`.
- **claude.ai: preflight the next cell (`fl_peninsula`) against `842ee139`.**
- **Predecessor chain:** `842ee139` (warm_arid) <- `bf96d1d1` (catalog +nmsu_donaana_mg) <- `9d8784f7` (4 coastal+desert cells) <- `813bade9` (catalog +ucanr_san_diego_mg) <- `349fb7af` (ca_interior + temp fix) <- `339933f2` (se_gulf sourcing) <- `f916e8fe` (Steps 9+10) <- `1b4fea68` (north `lifted_from_zone` strip) <- `a65c7175` (cherry Step 3.5 region shells + `second_planting` structure) <- `29b3aaa9` (M15 lettuce flip) <- ... (full lettuce chain in STATE_HISTORY).
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## What just happened (2026-06-06, session `m16_cherry_step4_warm_arid`) -- FIRST RELEASE UNDER THE NEW AUTHOR/RELEASE MODEL
- **`warm_arid` (zone 8, Las Cruces / Mesilla Valley) released.** claude.ai AUTHORED the cell (two-window + `second_planting`; spring transplant ~May from CR457-B frost data, NOT the chart's March; fall transplant late-Jul/Aug from the Doña Ana chart; cherry-narrow `heat_pause` = [7] July-only, milder arid nights vs the zone-9 desert absolutes). Claude Code RELEASED it.
- **The release verification caught + fixed three things a wholesale promote would have shipped wrong** (the value of the new model's first run):
  1. claude.ai built on the PRE-admit base (`9d8784f7`, catalog 81) and cited `nmsu_donaana_mg` -> would have DROPPED the admission + shipped an uncatalogued citation. Fixed by MERGE onto `bf96d1d1` (kept the 82-entry catalog).
  2. Two stale `sources_pending_admission` markers cleared (donaana already admitted).
  3. Two mechanical deviations from the cell's own `low_desert_az` exemplar, normalized (CONTENT untouched): `plantings_provenance.sources` -> `verified_against`; `heat_pause.basis_seasoned` spelled "degrees F" -> `°F`.
- **Gate: residual 26 -> 25** (warm_arid region_notes cleared; the 25 are all downstream: 3 region_notes-null + 21 dual-voice + 1 cornell_ext). §A2 shape 0; §E 0 uncatalogued; lettuce byte-identical `GATE: PASS`. Owed-to-claude.ai (Step 5/5.5): the cherry-narrow [7] ruling + the fall-window maturation check.
- **NEW OPERATING MODEL now in force (see STATE_HISTORY for the full rule).** claude.ai outputs ONLY (a) the updated JSON + (b) a STATE_HISTORY entry snippet (never the whole HISTORY file, never LATEST/CURRENT/the SHA). Claude Code computes the verified SHA, re-pins LATEST, regenerates THIS file, appends the entry, syncs `00-current`, commits + pushes. One disciplined release per change; cell-by-cell Step-4 detail (se_gulf..warm_arid) lives in STATE_HISTORY.


## Active work + exact next step
- **M16 cherry: Steps 3.5 + 9 + 10 DONE; Step 4 IN PROGRESS (7 of 10 cells done -- `warm_arid` released this session). NEXT = `fl_peninsula` (claude.ai), then `hawaii_tropical`, then `northern_tier` calendar.** Per `region_source_map` anchors. **Preflight against `842ee139`.**
  - **`fl_peninsula` (UF/IFAS VH021, zones 10-11) -- inverted calendar; verify window count per source** (lettuce's was single-window). UF/IFAS family fully catalogued.
  - **`hawaii_tropical` (CTAHR B-91, zone 11) -- crop-distributed timing; year-round encoding may apply** (lettuce Hawaii precedent: `year_round:true` + `calendar_basis` + 12-month all-active calendar). `uhawaii_ctahr` catalogued.
  - **`northern_tier` (zones 3-7)** -- promoted-verified (cold); owes `calendar[12]` cold_pause derivation (Step 5.5) + region_notes pair (Steps 6/7). Winter-gap months `wait`, owe `cold_pause` (frost-limited, NO midsummer heat_pause up north).
- **Then in sequence:** Step 5/5.5 (4-round side-by-side on every claim incl. all region windows authored; derive every region `calendar[12]`; classify north winter gaps as `cold_pause`; discover `cornell_ext` zone-6 URL). Steps 6/7/8 (seasoned depth-lift; beginner siblings incl. `cause_beginner`; remaining `region_notes_*` pairs; dual-voice coverage gate to 0 -- **author 27, gate displays 21**, see blind spot). Step 2 rider (`gs_exemplar_finding_003`). Then Claude Code **Step 11** + flip.
- **`status`-vocab decision still owed (Appendix B item 1) -- THREE-state unification.** Cherry `"verified_retro_complete"`; lettuce `"unverified"`. Successor (leaning `verified_arc`) decided at cherry's flip, back-applied. Do NOT set before decided + flip fires.
- **Blossom-drop `fruit_set_temp_f` -- T1 anchors in hand, ruling owed (claude.ai surfaces shape, Claude Code adds field).** Now includes the San Diego MG 65°F–90°F range (in `ca_south_coast` provenance) + VH021 + s1b_finding_006 (Clemson/PSU: >90°F day, <55°F night). Schema-touching → Trevor rules shape. Rule with s1b_finding_006 (deferred to family close).

## Gate record (2026-06-06, post-4-cell, GATE-CONFIRMED on working copy)
- **`GATE: 26 VIOLATION(S)`** -- confirmed this session. Composition: **4** region_notes-null (`northern_tier`, `warm_arid`, `fl_peninsula`, `hawaii_tropical`), **21** dual-voice siblings (Steps 7/8; gate-counted 21, author 27 -- see blind spot), **1** `cornell_ext` zone-6 URL (Step 5).
- **30 → 26 this session** (4 region_notes pairs cleared by the 4 authored cells). No new violation of any kind introduced by the 4 cells.
- **§A2 shape classes remain 0** (`stub:0 | null-track:0 | stale nested:0`). **second_planting structure validated clean** on both two-window cells (`ca_desert`, `low_desert_az`) -- all 4 required window keys present.
- **§E source-tier: 0 uncatalogued / 0 non-T1** (42 distinct IDs, +2 this session: `ucanr_marin_mg`, `ucanr_san_diego_mg`). **§C/D: 0** dash, **0** temp forms (every region_notes authored with `°F` from first draft). **§F: 1** gap (the known `cornell_ext` zone-6 malformed entry).
- **Lettuce `GATE: PASS`, byte-identical.** Collateral audit clean (only `cherry-tomato` changed; all 122 others + lettuce + earlier cells byte-identical except the 4 newly-authored).

## Region fill state (6 of 10)
| region | zones | status | window | heat_pause | second_planting |
|---|---|---|---|---|---|
| `northern_tier` | 3-7 | promoted-verified; owes calendar+notes | (cold) | none (frost-limited) | (cold 6-7 TBD) |
| `se_gulf` | 8-9 | FILLED | two-window | month 7 (cherry-narrowed) | yes |
| `ca_interior` | 8-9 | FILLED | single | none | none |
| `ca_north_coast` | 9-10 | FILLED | single (May) | none (COOL-limited) | none |
| `ca_south_coast` | 9-10 | FILLED | single (long Apr-Jul15) | none (mild marine) | none |
| `ca_desert` | 9-10 | FILLED | two-window | Jun-Aug (absolute) | yes (Sep) |
| `warm_arid` | 8 | PENDING (window unresolved) | TBD | TBD | TBD |
| `low_desert_az` | 9 | FILLED | two-window | Jun-Aug (absolute) | yes (Sep) |
| `fl_peninsula` | 10-11 | PENDING | TBD (verify per VH021) | TBD | TBD |
| `hawaii_tropical` | 11 | PENDING | TBD (year-round?) | n/a | n/a |

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- ✅ lettuce DONE (1 of 9). Cherry is mid-arc (Steps 3.5 + 9 + 10 done; Step 4 in progress, 6 of 10 cells done; owes 3 warm regions + northern_tier calendar + Steps 5-8 + 11). Beefsteak after cherry.
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
