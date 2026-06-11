# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


**5 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, peach, lettuce-leaf) of a ~18 roadmap target. **Anchor 6 = apple IN PROGRESS:** Step 4 (TREE region fill) released this session -- all 10 region cells now FILLED (17 calendars / 3 empty at the 100-hour no-fruit floor), gate PASS, but NOT yet certified. NEXT = apple Step 5 (verify).

## Canonical pointer
- **Current SHA:** `5cfe354eaaa7cc2714def0f9052615d8b013c0ca8f69c75fb918ecbbb32da848`. `LATEST.txt` session: `apple_step4` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `510edafe` -- feat(apple): Steps 1-3 + 3.5 -- anchor 6, the second tree (compressed)
  - `7345b944` -- feat(peach): CERTIFIED -- anchor 5, the FIRST tree (Steps 9-11: verbatim scan + perennial cert-gate + flip)
  - `0d3ed015` -- feat(peach): Steps 6-8c -- the events layer (notifications + weather_triggers); bulk prose COMPLETE
  - `59876b61` -- feat(peach): Steps 6-8b -- bulk care prose part 2 + mint clemson_peach_diseases
  - `4a3a4801` -- feat(peach): Steps 6-8a -- core biology compounds + the tree-stage journey (bulk prose, part 1 of 2)
  - `3e07c4e1` -- feat(peach): Step 4 -- the first tree's region biology fill + the no-fruit-calendar direction split
  - `e99001f2` -- feat(peach): Step 3.5 -- the TREE region/calendar model (anchor 5, first permanent tree)

## What just happened (session `apple_step4`)
- **apple's 10 TREE region shells FILLED** (`510edafe`->`5cfe354e`). claude.ai authored the region biology (chill bands + per-zone suitability + absolute bloom/harvest/dormant timing + 12-token tree calendars); slice-integrity matched its pre-reconcile SHA `9d86c815` (faithful apply, 5th match).
- **No-fruit DIRECTION SPLIT at apple's floor = 100** (vs peach's 400): 17 calendars / 3 empty. The 100-floor keeps ca_south_coast z10 + ca_desert z10 calendar-bearing where peach left them empty; fl z10 (chill < 100) + fl z11 + hawaii z11 are empty. perennial A3 = 0.
- **Claude Code reconciled an anchoring-convention drift inline** (Trevor-approved): claude.ai used broad source arrays + one mnemonic anchor per rule (145 §F violations). Re-keyed 12 mnemonics -> catalog IDs across 63 leaves, set each leaf's sources = its actual anchor(s) (broad set stays at the §F-exempt region rollup), minted 3 new T1 sources (catalog 89->92: `ucd_fruitnut`, `ext_org_apples`, `ucanr_slo_mg`). No biology touched, no fabricated URLs.
- **Gates green:** whole_crop_gate apple PASS (anchoring 0 gaps, source-tier 0 uncatalogued); register PASS; only apple changed; release_verify's 10 concerns all = the tree-model chill fields vs the annual exemplar (intentional, as for peach).

## Active work + next step
- **NEXT = apple Step 5 (verify)** -> 5.5 calendars -> 6-8 bulk prose -> cert (9-11). apple's region layer is filled + gate-clean; it is NOT in the Gate/Region/Flip tables below until it certifies.
- **OPEN decision (non-blocking) -- `reliable_fruit_zone_min`:** left at 4 (roster-honest); lowering to species-honest 3 needs adding ultra-hardy cultivars (Honeycrisp/Haralson/Honeygold) to the roster. Decide at Step 5 / a roster pass.
- **Trevor content question (fold into 6-8):** the establishment-year **blossom-removal / no-fruit-year-1** care note -- apple's bulk prose is unauthored (Steps 6-8); verify peach coverage and make the year-1 blossom-thinning note a standard part of the tree care prose.
- **Still owed (carried):** perennial-aware `rotation` shape (peach open_finding); `_build_tree_shells` auto-populate region_id/label/zone_span + stray-key sweep; Appendix A registration of growth_stages `timing_*`/`year_phase`.

## Gate record (generated 2026-06-11, on canonical `5cfe354e`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **5 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
