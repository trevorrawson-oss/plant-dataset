# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0** -- one self-contained doc; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8) so the plant-project top level shows only numbered folders + the single active handoff.
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session.

---


**6 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple) of a ~18 roadmap target. **LEMON arc STARTED** -- anchor 7, the FIRST evergreen / first citrus; **Steps 1-3 released** (biology + 5 varieties + sourced rootstock/companions). Lemon is NOT certified (pre-cert, status null). NEXT = lemon Step 3.5 = Claude Code builds the evergreen region/calendar model.

## Canonical pointer
- **Current SHA:** `08556e215da0155225ada8c68160f016948030a577280b65f7b2c5018b67d191`. `LATEST.txt` session: `lemon_steps1_3` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `d228ed7b` -- feat(peach): register-fill backfill -- 42 null register fields; register-complete
  - `a821d6d4` -- feat(apple): CERTIFIED -- anchor 6, the second tree (Steps 9-11)
  - `0711aa99` -- feat(apple): Steps 6-8B -- register prose complete (anchor 6)
  - `3c8ac5e9` -- feat(apple): Steps 6-8A -- bulk care prose + key-shape reconcile (anchor 6)
  - `09538e31` -- fix(trees): derive calendars from dates + A4 coherence gate; apple Step 5 + peach backfill
  - `5cfe354e` -- feat(apple): Step 4 -- tree region fill + anchoring reconcile (anchor 6)
  - `510edafe` -- feat(apple): Steps 1-3 + 3.5 -- anchor 6, the second tree (compressed)

## What just happened (session `lemon_steps1_3`)
- **LEMON Steps 1-3 RELEASED** (`d228ed7b`->`08556e21`), anchor 7, the first evergreen. claude.ai authored (48-op patch, leading-slash -- clean apply, lemon-crop SHA matched the claimed `badeedb1...` exactly): source set (citrus T1), the 2.9 EVERGREEN block (chill=0 honest, dormancy null, self-fertile pollination, REAL grafted rootstocks selected by disease/cold/soil NOT size, establishment), `gating_factors:["cold_hardiness"]`, survives-vs-fruits hardiness (8b/11 survives, 9b/11 fruits), 5 structured varieties w/ bloom data (Eureka/Lisbon/Improved Meyer/Ponderosa/Variegated Pink), companions. NO region cells, NO calendars, calendar_basis left `frost_anchored` (Claude Code flips -> `perennial_evergreen` at Step 3.5). **No flip** (pre-cert).
- **Claude Code release-lane corrections + rulings:**
  - **Catalog mint (92->94):** `uf_ifas_hs1153` (live URL is HS402, not the 404 HS1153 slug) + `ucr_citrus`. §E now clean.
  - **Dash hygiene:** claude.ai's prose carried `--` in **20 fields** despite its "no --" claim (cross-check caught it); swapped each for context-appropriate punctuation, wording untouched; §D dash=0. **claude.ai's self-dash-check is unreliable -- reinforce in every kickoff.**
  - **Delta ruling (Trevor 2026-06-12):** `varieties.recommended[].delta.*.value`/`.parent` ruled USER-FACING-CATEGORICAL (terse attribute/diff descriptors, no register sibling) -- sets the register treatment for the WHOLE variety-delta model. Wired into `register_completeness_gate` + recorded in `register_bearing_field_inventory_v1_0` (variety-delta addendum).
  - **Pre-cert anchoring hook allowance (test-first):** `precommit_release_verify.drop_precert_anchoring` -- a pre-cert crop (status != verified_gs_arc) legitimately carries sources without per-field anchoring (Step 4+ fills it); a CERTIFIED crop gaining an anchoring gap still blocks. Stops the false-block that every tree/perennial/hub Steps 1-3 would otherwise hit.
- **EVERGREEN MODEL ratified this session** (Trevor): two axes (`calendar_basis: perennial_evergreen` + crop-level `gating_factors`); spec = `tree_region_model_evergreen_amendment_v1_0` (in PK); evergreen gets 2 anchors (lemon cold-only = 7, orange-navel heat = 8; avocado parked). FLAG 1 resolved (lemon's `rootstock_selection_basis:"disease_cold_soil_tolerance"` is a legit new enum value; key matches peach/apple).
- Footprint: only `lemon` + `source_catalog` changed; 6 anchors byte-identical, all PASS; lettuce byte-identical. whole_crop_gate lemon = 19 (10 region-unfilled + 9 anchoring-deferred -- ALL expected Steps-1-3 admission state).

## Active work + next step
- **NEXT = lemon Step 3.5 (Claude Code, the evergreen model BUILD), test-first against lemon's authored dates** (per evergreen amendment §5): `build_region_shells` evergreen branch (set `calendar_basis -> perennial_evergreen`; gating-keyed climate layer `min_winter_temp_f` for cold_hardiness; reuse perennial establishment entry + render keys); `perennial_gate` generalize to `PERENNIAL_BASES` + default gating_factors + cold-only no-fruit branch; `derive_evergreen_calendar` (no `dormant` token, `growing` filler, wrap/multi-bloom aware); `whole_crop_gate` A3/A4 recognize the evergreen basis. **Regression: peach + apple must stay byte-identical / PASS.**
- **Then lemon Steps 4-5** (region biology + the suitability verdicts + anchoring URLs populated), **6-8** (care prose), **9-11** (cert + the Step-11 verbatim scan, which defers from Steps 1-3 since anchoring URLs are empty now).
- **Anchor 8 = orange-navel** (heat-accumulation gate -- first builds the `heat_summer_basis` climate datum + the heat no-fruit branch).

## OWED
- lemon's 9 anchoring gaps (Step 4+); the Step-11 verbatim scan (deferred -- 0 URLs at Steps 1-3).
- Carried: apple's 4 open_findings (dead-anchor repair, rotation shape, companions array-split, reliable_fruit_zone roster); `peach_rotation_shape_finding`; perennial-aware `rotation` shape; `_build_tree_shells` auto-populate region_id/label/zone_span; Appendix A reg of growth_stages `timing_*`/`year_phase`; `apply_patch` reject-bare-slash hardening; repoint `gen_current_state` checklist ref -> v2.0.

## Gate record (generated 2026-06-12, on canonical `08556e21`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **apple: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- **lemon: 19 (10 region-unfilled + 9 anchoring-deferred -- expected Steps-1-3 admission state, NOT cert-eligible yet)**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause
- **lemon: 0/10 (annual-shape shells; rebuilt to evergreen tree shells at Step 3.5)**

## Flip gates (generated)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lemon:** launch_ready_core=False launch_ready_seasoned=False status=`None` (pre-cert, Steps 1-3 done)
- **6 anchors certified.** (Target denominator is a roadmap call -- see the headline slot.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
- **EVERGREEN two-axis model (2026-06-12):** `calendar_basis: perennial_evergreen` (shape: no dormancy, `growing` off-season filler, wrap/multi-bloom) + crop-level `gating_factors` list `{cold_hardiness, heat_accumulation, chill_hours}` (suitability gate). Gates use `PERENNIAL_BASES`; chill-gated crops w/o gating_factors default `["chill_hours","cold_hardiness"]` (peach/apple byte-identical). Spec = `tree_region_model_evergreen_amendment_v1_0`. Evergreen = 2 anchors (lemon 7 cold-only, orange-navel 8 heat).
- **variety-delta descriptors (`delta.*.value`/`.parent`) = USER-FACING-CATEGORICAL** (no register sibling). Sets the variety-delta model's register treatment dataset-wide.
- **register-fill is a cert dimension** (`register_fill_gate`); tree calendars are DERIVED + A4-gated; **patch paths = leading-slash RFC-6901 or dot-form** (bare-slash mis-applies silently).
- **claude.ai's self-checks for dashes are unreliable** -- Claude Code re-scans + the §D gate is the real defense; reinforce the no-`--` rule in every kickoff.
