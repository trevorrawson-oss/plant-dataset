# plant -- CURRENT STATE (live surface)

> **⚠️ SESSION PROTOCOL -- read before acting.**
> 1. **Confirm canonical FIRST:** `shasum -a 256 crops_data_final.json` == `LATEST.txt`; also `git -C ~/plant-dataset log --oneline -1` + `git status -sb` (the working tree can sit AHEAD of HEAD -- an uncommitted hand-promote). Locate the active step on the gold-standard arc checklist (v2.0) before acting -- never infer "next" from "a cell is done".
> 2. **CURRENT_STATE.md = LIVE STATE ONLY.** Never delta-edit; FULLY REGENERATE at close via `tools/gen_current_state.py`, then carry the prose slots forward + amend. The mechanical sections are generated from true state.
> 3. **STATE_HISTORY.md = APPEND-ONLY** -- a dated entry most-recent-first below its header; never rewrite. It is the recovery log that caught the premature-flip near-miss.
> 4. **RELEASE VERIFICATION before any promote** (protocol #6): `whole_crop_gate` + `tools/release_verify.py` + cross-check vs claude.ai's STATE_HISTORY claims. A green gate is NOT a clean release.
> 5. **Four flips are distinct, never conflated:** per-crop `launch_ready` (that crop's Step 11 == 0), region read-layer, authoring-model, schema bump.

---


**18/18 GS-arc anchors GREEN -- the audit's last two loose-end classes CLOSED (`c0c1c666`, 2026-06-25).** WI3: a new `whole_crop_gate` branch **A21** (`berries_woody_variety_chill_violations`) locks the WI4 string->numeric chill migration so a future berry crop can't reship the legacy `chill_hours` STRING -- test-first (12 tests), blueberry conforms, 18/18 holds. WI4: the three claude.ai Layer-2 flags source-VERIFIED against live T1 -- **onion northern_tier z3** harvest CONFIRMED wrong and corrected (`Jul 30 - Aug 29` -> `Aug 15 - Sep 15`); **carrot z4/z5** spring-harvest flags verified MINOR and LEFT; **peach se_gulf** chill prose confirmed non-contradicting and LEFT (Trevor's lean). **whole_crop_gate 18/18 + A21 green, register PASS, release_verify C-H clean (H chill_table 0), 34/34 tool tests, precommit no-regression (onion 0 total).** **Then `b39f1453` (2026-06-25): the #2 blueberry calendar copy landed** -- `grown_as_note_seasoned/beginner` authored on all 20 blueberry cells (claude.ai lane; Option B per-leaf-habit, regionally tuned; season-relative prune; evergreen carries no dormancy/prune language); release_verify clean, only blueberry changed, 18/18 holds. The plant-astro submodule bump (now 96dc6603 -> `b39f1453`, batching the onion z3 window + the blueberry copy; calendars re-render automatically, no UI change beyond the prior batch) is GATED on Trevor and batches with `fix/calendar-harvest-two-row` + the Expo port.

## Canonical pointer
- **Current SHA:** `b39f1453664c257f07f9a6f03ca3ed2dca34dc22e7ff5bdf7a14e4a2cf0d9bf7`. `LATEST.txt` session: `blueberry_grown_as_note` (2026-06-25).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `b39f1453` -- feat(blueberry): #2 berries_woody calendar copy -- grown_as_note on all 20 cells (claude.ai author lane)
  - `c0c1c666` -- feat(onion): WI4 source-truth -- northern_tier z3 harvest -> Aug 15 - Sep 15 (T1)
  - `96dc6603` -- feat(release): final batch -- Phase B to 18/18 + chill T1 + source-truth corrections + WI4
  - `3009a3fc` -- feat(gates): Phase B -- companion-shape (A19) + display-readiness (A20) + tips coverage (A12) + companion reshape (F4/F6)
  - `9739e373` -- feat(schema): Phase A -- npk_ratio field + chill shared-delivered table (audit F2/F3)
  - `6e9538e1` -- feat(broccoli): CERTIFIED -- anchor 18 (Step 11 flip); the LAST GS anchor, the roster is DONE (~18)
  - `956fc987` -- feat(broccoli): Steps 6-8 -- consumer prose + the 7 compounds (whole_crop_gate -> 0, structurally cert-ready)
  - `b0ccdd2d` -- feat(zucchini-courgette): CERTIFIED -- anchor 17 (Step 11 flip); the warm-season rail-rider

## What just happened (session `wi3_variety_chill_gate_wi4_onion_z3_harvest`, 2026-06-25)

**A small post-final-release pass closing the audit's last two loose-end classes -- base `96dc6603` -> `c0c1c666`; ONE data cell + one new gate branch.**

- **WI3 -- berries_woody variety-chill PRESENCE gate (tooling, commit `fc6e5cd`):** new `whole_crop_gate` branch **A21** (`berries_woody_variety_chill_violations` in `tools/berries_woody_gate.py`). For a `berries_woody` crop, every `varieties.recommended` entry must carry a NUMERIC `chill_hours_required` + a `chill_hours_range` (null for a single-value cultivar, else a valid `[lo,hi]` pair with `lo == required`), and NO string `chill_hours`. No-op off `berries_woody`. **Test-first: 12 new tests** (`test_berries_woody_gate.py` ALL PASS). A15 polices the CROP-level chill gate basis; A21 polices the per-VARIETY shape `chillBuckets`/`tree.ts` reads -- it locks the WI4 migration so a future berry crop can't reship the STRING that broke blueberry's gauge (audit F2). blueberry's 13 cultivars conform (A21 0 violations); 18/18 stays green.
- **WI4 -- the three Layer-2 flags source-VERIFIED against live T1 (data, commit `14f54c4`):**
  - **onion northern_tier z3 -- CONFIRMED + APPLIED.** A zone-3 long-day storage onion transplanted May 1-22 cannot finish harvest by the stored `Jul 30 - Aug 29` (long-day bulbs initiate only post-solstice, then size up). T1: SDSU ("Bulbs can be harvested August through October" for mid-Apr-mid-May planting) + USU (100-120 day DTM -> early Aug to mid-Sept from a May transplant). The cell's OWN `zone_notes` ("harvest late summer before the mid-September frost") + `resolved_from.first_frost` Sep 15 corroborate -- the old window undershot its own framing. `harvest` -> `Aug 15 - Sep 15` (start Aug 15, end Sep 15); `calendar` Jul `harvest`->`growing` (still bulbing), Sep `season_over`->`harvest`. **NO plant-token change; onion is out of succession scope -> ZERO `successions_realized` cascade.** CC-lane harvest correction (the carrot z3 precedent).
  - **carrot northern_tier z4 + z5 -- verified MINOR, LEFT.** The Jun (z4) / May (z5) spring first-harvest is reachable from the earliest sow at the published **50-60-day fast-variety floor** (Iowa State, UW A3686, USU) -- the optimistic edge, not a wrong-season error. Within the ~1-month tolerance; no live T1 source contradicts the current value. (DOCUMENT items; revisit only if the carrot cells are next touched.)
  - **peach se_gulf chill prose -- confirmed non-contradicting, LEFT.** `chill_basis_seasoned` "roughly 600 to 1,000 chill hours inland" loosely brackets the T1 table cell `se_gulf.8 [650,1000]` ("roughly" + bank-vs-cultivar-requirement framing); the prose's own second clause already uses 650. Trevor's lean is leave-it; the only available tweak is the 3-char "600"->"650" for full internal consistency, recorded for his discretion.
- **Verification:** whole_crop_gate 18/18 + A21 green; register_completeness_gate PASS; release_verify C-H clean (H chill_table 0; 2 pre-existing non-blocking z10 `wait`-month review notes, NOT mine); 34/34 tool tests; precommit no-regression (onion 0 total). Collateral audit: exactly onion `northern_tier.z3` changed, 123 crops intact, no top-level key drift, JSON stays compact (1 line, no trailing newline).

## Active work + next step -- dataset SHIPPED 18/18; plant-astro bump GATED on Trevor

- **plant-astro submodule bump = GATED on Trevor.** Branch `fix/calendar-harvest-two-row` already carries F1 (green-beans two-row calendar) + Phase A card UI (npk/chill) + Phase B companion hardening + the WI3 app port + the blueberry BerryChillCard. This pass adds NO UI change -- the onion z3 corrected calendar re-renders automatically from the bumped data. Bump `96dc6603` -> `c0c1c666` + merge/push held for Trevor's single signoff (push auto-deploys Netlify); batch it with the prior UI work + the Expo port.
- **Deferred list (updated):** (1) ~~a `berries_woody` variety-chill presence gate~~ **SHIPPED this session (A21).** (2) peach `se_gulf.chill_basis_seasoned` "600"->"650" -- confirmed-leave; available 3-char tweak if Trevor wants the prose's first clause to match the table exactly. (3) carrot z4/z5 spring-harvest MINOR + the Hawaii year-round-window product call -- DOCUMENT items (verified MINOR / a modeling-product call, not defects).
- **The real Expo app (~/plant-app) still needs the same two-row harvest + chill-card port** the app-preview got (flagged for Trevor; NOT in this batch).

## Gate record (generated 2026-06-25, on canonical `c0c1c666`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **basil: `PASS` (0)**
- **zucchini-courgette: `PASS` (0)**
- **green-beans-bush: `PASS` (0)**
- **broccoli: `PASS` (0)**
- **peach: `PASS` (0)**
- **apple: `PASS` (0)**
- **lemon: `PASS` (0)**
- **blueberry: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **onion: `PASS` (0)**
- **strawberry: `PASS` (0)**
- **orange-navel: `PASS` (0)**
- **microgreens-mix: `PASS` (0)**
- **lavender: `PASS` (0)**
- **zinnia: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **basil: 10/10 region cells filled**
- **zucchini-courgette: 10/10 region cells filled**
- **green-beans-bush: 10/10 region cells filled**
- **broccoli: 10/10 region cells filled**; 7 heat_pause, 14 second_planting
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lemon: 10/10 region cells filled**
- **blueberry: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause
- **onion: 10/10 region cells filled**
- **strawberry: 10/10 region cells filled**
- **orange-navel: 10/10 region cells filled**
- **microgreens-mix: 0/0 region cells filled**
- **lavender: 10/10 region cells filled**
- **zinnia: 10/10 region cells filled**

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **basil:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **zucchini-courgette:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **green-beans-bush:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **broccoli:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **apple:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lemon:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **blueberry:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **onion:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **strawberry:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **orange-navel:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **microgreens-mix:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lavender:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **zinnia:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **18 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

## Live locked decisions / guardrails
- **BERRIES_WOODY VARIETY-CHILL PRESENCE = GATED at A21 (WI3, 2026-06-25, test-first):** `berries_woody_variety_chill_violations` (in `tools/berries_woody_gate.py`, wired as `whole_crop_gate` **A21**) locks the WI4 string->numeric migration. For a `berries_woody` crop, every `varieties.recommended` entry must carry a NUMERIC `chill_hours_required` (the chill-gating threshold `chillBuckets`/`tree.ts` reads) + a `chill_hours_range` key that is null (single-value cultivar) OR a valid `[lo,hi]` pair with `lo <= hi` AND `lo == chill_hours_required` (the scalar IS the range low end); a STRING `chill_hours` (the dropped legacy form) is a violation. **This is the per-VARIETY analog of A15's CROP-level chill gate** -- A15 = the gate BASIS (gating_factors + crop `chill_hours_required`), A21 = the variety shape the cards consume. No-op off `berries_woody`. blueberry's 13 cultivars conform. Template for the raspberry/blackberry/currant/gooseberry/grape berry family.
- **HARVEST-ONLY SOURCE-TRUTH CORRECTIONS STAY IN THE CC LANE when no plant-token/succession cascade (onion z3, WI4, 2026-06-25):** the routing rule (source_truth_sampling_qa_v1_0 Step 4) sends a WINDOW-SHAPE change (plant tokens move -> calendar + `successions_realized` recompute) to the claude.ai authoring lane, but a HARVEST-window correction that moves only harvest tokens -- NO plant-token change, and the crop is out of succession scope -- is a bounded deterministic edit CC applies directly (the carrot z3 precedent generalized). onion `northern_tier.z3` harvest `Jul 30 - Aug 29` -> `Aug 15 - Sep 15`: T1-confirmed (SDSU Aug-Oct + USU 100-120d DTM + post-solstice long-day bulbing), CORROBORATED by the cell's own `zone_notes`/`first_frost` Sep 15; calendar Jul `harvest`->`growing` + Sep `season_over`->`harvest`; onion `succession_policy.suitable=False` so A8 has nothing to recompute. **The DOCUMENT-bucket flags from the parent QA (carrot z4/z5 spring harvest) re-verified MINOR and LEFT** -- a Jun/May first-harvest is reachable at the published 50-60-day fast-variety floor; "optimistic edge" != "wrong-season", and the conservative rule is leave-within-1-month. Source-verify EVERY claude.ai flag against live T1 before acting; "apply only if confirmed" means a live T1 source must contradict the current value beyond ~1 month.
- **CHILL NO-FRUIT DIRECTION-SPLIT is the gate's job, and `survives_no_fruit` must be EMPTY when chill-limited (apple `ca_south_coast.10`, 2026-06-25, Trevor-approved).** A `perennial_chill_gated` cell's calendar is decided by the DELIVERED band `[lo,hi]` (the shared table) vs the crop's min-variety chill FLOOR: `lo >= floor` -> chill met, MUST carry a calendar; `lo < floor` -> chill-limited, MUST be EMPTY (over-promise). When Stream A's T1 chill drop moved `ca_south_coast.10` to `[50,350]`, apple's lo (50) fell below its 100h floor, so its `survives_no_fruit` cell flipped chill-limited and its 12-token calendar became an over-promise -> emptied (matches apple's own `fl_peninsula.10`, identical [50,350]/survives_no_fruit/empty, + peach's 3 identical cells). Prose ("blooms most years, treat any harvest as a bonus") KEPT. **A `marginal` cell, NOT a third calendar tier, is the "fruits in good years" representation** -- the band STRADDLING the floor (`lo<floor<=hi`) is NOT a signal (7 peach marginal/reliable cells straddle it and correctly fruit); the SUITABILITY ENUM (fruits_reliably > marginal > survives_no_fruit > unsuitable) already encodes the gradient, so no model change is needed.
- **BLUEBERRY VARIETY CHILL = numeric, tree-consistent (WI4 rider 1, 2026-06-25):** the 13 `varieties.recommended` carry `chill_hours_required` (numeric SCALAR = the LOW end of the old `~lo-hi` string, the chill-gating threshold that `chillBuckets`/tree.ts reads directly) + `chill_hours_range` `[lo,hi]` for genuine-range cultivars (single-value strings -> range null); the `chill_hours` STRING is DROPPED (matches the trees, which carry null `chill_hours`). Deterministic migration. **NOW GATED at A21 (WI3, above)** -- the deferred presence gate shipped. `npk_tag` is USER-FACING-CATEGORICAL: onion -> "High nitrogen early", blueberry -> "Acidic, ammonium-based".
- **PHASE B GATES (audit F4-F7, 2026-06-24, `3009a3fc`) -- three new whole_crop_gate branches, each test-first + fix-the-structure-to-green:** **A19 `companion_shape_gate`** -- every companion entry must be an OBJECT with a non-empty `name` (a bare STRING is silently dropped by the card -> F4); a crop's goods/bads must be reachable from a SEASONED-READABLE bucket `good_seasoned`|`good_beginner_seasoned` (beginner-only = invisible to seasoned -> F6). **A20 `display_readiness_gate`** -- ARCHETYPE-AWARE field PRESENCE for the Hero/Ph/Feeding cards: universal sunlight/water; non-indoor adds sunlight_hours / ph.preferred_range / spacing_inches / fertilizer{type,timing,frequency} / a real container_ok bool. Indoor (IndoorCycleCard) + in-ground container_ok==False are legitimate N/A. **A12 tips COVERAGE** -- every growth_stage id has a non-empty renderable tip (`text_*`). Indoor exempt. **GATE-AS-WORKLIST:** wiring these made 4 already-certified anchors go RED until the Phase B content landed (the audit's intended outcome).
- **COMPANION ENTRY RENDER RULE (RegisterText, plant-astro):** a both-mode (`*_beginner_seasoned`) entry carrying ONLY `why_beginner` BLANKS seasoned mode (RegisterText falls back the other way). So a register-neutral companion `why` goes in `why_seasoned` (renders both via fallback), or use the carrot two-bucket pattern (same `name` in `good_seasoned`+`good_beginner_seasoned`, reconciled by the card). apple's reshape used `why_seasoned` for exactly this reason.
- **NPK PILL = a dedicated `fertilizer.npk_ratio` (Phase A, audit F3, 2026-06-24):** a render-ready bare "N-P-K" string (e.g. `5-10-10`) is the SINGLE SOURCE OF TRUTH for the feeding pill -- derived DETERMINISTICALLY (first `\d+-\d+-\d+`) from the verified `npk_hint_seasoned`, never re-derived at render. Ratio-less crops (citrus/allium/lavender/blueberry) carry explicit `npk_ratio: null` + a short `npk_tag`. GATE **A17** = present-or-explicit-null (no-op off the npk_hint surface). The pill renders the ratio OR the tag; the npk_hint PROSE still renders as a dual-register paragraph.
- **CHILL-DELIVERED = ONE shared crop-invariant `region_chill_delivered` table (Phase A, audit F2, 2026-06-24):** chill-DELIVERED is a CLIMATE datum (region+zone -> [lo,hi]), authored ONCE at the dataset top level, NEVER per-crop. chill-REQUIRED stays per-variety (`chill_hours_required` / `chill_hours_range`). NO crop may carry `chill_hours_delivered` (GATE **A18**); `perennial_gate` A3's no-fruit split + the plant-astro chill cards both READ the shared table; `release_verify` H validates its [lo,hi] shape. Numbers are **T1-SOURCED** (2026-06-25; Utah / modified-Weinberger chill model, accumulated hours 32-45 degrees F, per-region extension chill data); the gate enforces SHAPE + crop-invariance, never the values.
- **BERRIES_WOODY ARCHETYPE -- CERTIFIED (anchor 18, the FIRST + only `berries_woody`; design spec `2026-06-22-blueberry-berries-woody-model-design.md`, D1-D8; cert 2026-06-23 `0b767fc2`):** a woody fruiting SHRUB whose growable TYPE is CHILL-GATED by region and whose calendar SHAPE splits by per-cell `leaf_habit` (deciduous/evergreen); `calendar_basis:"berries_woody"`, frost resolution ON; planted ONCE 20-50 yrs; acid soil pH 4.5-5.5; `type` top-level=`"berry"`. **TOOLSET (test-first):** `berry_woody_calendar` deriver + A16; `berries_woody_gate` A15 (the chill signature -- chill_hours_required IS the gate basis, the INVERSE of woody_ornamental; the type COVERAGE invariant; leaf_habit<->token placement) + **A21 (variety-chill presence, WI3 2026-06-25)**; `_build_berry_woody_shells`; `derive_berry_woody_calendars`. **leaf_habit = OPTION B (region-biology binary):** SHB reads deciduous in cool CA, evergreen in the warm South. Template for raspberry/blackberry/currant/gooseberry/grape.
- **WARM-SEASON-ANNUAL OFF-SEASON TOKEN = `cold_pause`, NEVER `wait`:** a frost-tender annual's frost-killed WINTER off-season months render `cold_pause` (the frost-bracketed dormant period); every certified warm-season annual carries `cold_pause` with ZERO `wait`. `wait` is the ILLEGIBLE token Step 5.5 pause-legibility resolves; it is NOT a valid resting state for a populated calendar. The A5 gate flags wait-tokens as ADVISORY NOTES (not blocking), so this needs the CC eye at release. **`region_label` = the certified COLON convention (`California: Interior Valleys`), never ` -- `.** **SUCCESSION MIXED-GEOMETRY: geometry is keyed PER-REGION by continuous-vs-split (second_planting spec v1.1 §4), NOT warm-vs-cold -- continuous -> `succession_continuous` + split -> `succession_spring`/`succession_fall` comma-lists. `successions_realized` is CC-DERIVED at A8, never authored; `succession_policy.successions` reconciles to max-over-zones.**
- **RAIL-RIDER RELEASE = conform claude.ai's field SHAPES to the certified contract in the Claude Code lane:** an annual on the proven `warm_season_fruiting` rails needs NO new archetype/tooling, but a fresh-authored slice can DRIFT, and `register_completeness_gate` HALTs on novel/unruled prose. carrot/onion are the TEMPLATES: companion `provenance` = the rich `{label, confidence, reason, verified_against_sources, verified_date}`; `soil.organic_matter_preference` = a USER-FACING-CATEGORICAL token; `container_notes.shape_requirements` is CP (populated_seasoned REQUIRES populated_beginner). `successions_realized` stays OUT-OF-SCOPE at Steps 1-3.
- **WOODY-ORNAMENTAL ARCHETYPE -- CERTIFIED (anchor 14, lavender):** a woody perennial SUBSHRUB grown for BLOOMS whose LIFECYCLE is region-dependent -- per-cell `grown_as` in {perennial, annual}. Tokens `dormant`/`growing`/`bloom` + `prune`; NO `harvest`/`renovation`. **GATES** `woody_ornamental_violations` (**A13**) + `woody_ornamental_calendar_violations` (**A14**). `gating_factors` EMPTY, NO A9. **FIRST-RUN TRIGGER GOTCHA: claude.ai must SET `archetype = "woody_ornamental"` at Step 1-2.** Template for rosemary/sage/thyme/butterfly-bush/Russian-sage.
- **TIPS RENDERING-CONFORMANCE (`tips_by_stage`) is GATED at A12:** the renderer does `tipsByStage[stage.id].text_seasoned`, so a tip renders only if (a) its list is non-empty, (b) it uses `text_seasoned`/`text_beginner` (NOT `tip_*`), (c) its KEY is a real `growth_stages` id. INDOOR crops are EXEMPT (their tip surface is `indoor_cycle.tip_*`, gated A6). When `growth_stages` ids change, re-key `tips_by_stage`.
- **PER-ZONE `successions_realized` = a DERIVED integer, NOT sourced:** `resolved_by_zone.<z>.successions_realized` = the realized sowing count a zone's season supports. Deriver `tools/derive_realized_successions.py`, gap-aware; **Cap 12 GLOBAL**. Scope = `succession_policy.suitable==True` + region-filled + non-indoor. `whole_crop_gate` **A8** re-derives-and-asserts-equality + presence + reconciliation + out-of-scope absence.
- **BERRIES_HERBACEOUS ARCHETYPE -- CERT-PROVEN on strawberry (anchor 13):** a herbaceous perennial whose LIFECYCLE is region-dependent. `calendar_basis: perennial_herbaceous` (frost resolution ON). Per-cell `grown_as` in {perennial, annual}. Tokens `dormant` + `renovation` (June-bearing perennial cells). **GATES:** `berry_herbaceous_violations` (**A10**) + `berry_calendar_violations` (**A11**). Photoperiod is the deliberate INVERSE of onion. chill INFORMATIONAL.
- **PHOTOPERIOD / DAY-LENGTH ARCHETYPE -- cert-proven on onion (anchor 12):** day length gates which CULTIVAR bulbs by latitude, NOT the calendar -- onion STAYS `calendar_basis:frost_anchored`. Crop-level `gating_factors:["photoperiod"]`; variety `day_length_type`; per-cell `recommended_day_length_type`. **A9 gate (`photoperiod_violations`):** every variety + resolved cell has a valid type + the COVERAGE invariant. **BOLTING is VERNALIZATION, NOT photoperiod.** hawaii_tropical = short_day.
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven (lemon cold-only, orange cold+heat).** heat `marginal` -> suitability `marginal`. TREE per-variety schema = lemon's 11-key set incl. `delta`. The perennial no-fruit split (A3) is gating_factor-keyed. Chill-delivered for the deciduous branch comes from the shared `region_chill_delivered` table.
- **INDOOR / `non_seasonal_indoor` ARCHETYPE -- proven on microgreens-mix (anchor 11):** grown INDOORS year-round; NO frost/season/hardiness zone. **`regions{}` AND `zones{}` COLLAPSED to `{}`.** Self-describes via `zone_independent:true` + `indoor_cycle{}` + `calendar_basis:non_seasonal_indoor`. EXEMPT from the npk pill, tips A12, weather_triggers.
- **COMPANION ITEM SHAPE = the certified carrot rich-object shape (NOT a flat `why`).** `good_seasoned[]` = {name, category, timing, why_seasoned, notify_weeks_before, provenance:{...}, sources, anchoring_urls}; `good_beginner_seasoned[]` = {name, why_beginner}. **VOCAB = `research_backed` / `likely` / `traditional`.**
- **SOURCE-TIER: certified crops carry ZERO non-T1.** `johnny_seeds` / seed-company / almanac = T2 (evidence-log corroboration only); `whole_crop_gate` E flags any non-T1.
- **DISPLAY-READINESS FIELDS ARE A SEPARATE BAR FROM CERT (garden-calculator-surfaced):** the calculator gates PLACEABILITY on `spacing_inches` (+ `companions`) and CONTAINER on `container_ok==true` AND `min_pot_gallons != null`; cert validates BIOLOGY/sources and does NOT require them. **Audit display-readiness PER consuming surface.**
- **CERT mechanics / THE FLIP:** source-verbatim (vs cited URLs) is the flip gate; `verification_status` block (status verified_gs_arc + phase + launch_ready x2 + last_audited + source_set + verification_log_ref + open_findings all blocks_launch:false). CERT RE-VERIFICATION = an INDEPENDENT SOURCE FETCH FOR FIDELITY (WebFetch a sample of cited URLs, check the NUMBERS).
- **GOTCHA: canonical JSON is COMPACT** (`json.dumps(separators=(",",":"), ensure_ascii=False)`, no trailing newline, never indent=2). **Dataset commits go in `~/plant-dataset` on `main`** (the submodule is detached-HEAD); push is AUTONOMOUS (announce-then-execute). The plant-astro merge/push stays GATED on Trevor.
</content>
</invoke>
