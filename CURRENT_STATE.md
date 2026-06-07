# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---

## 🥬 LETTUCE + 🍅 CHERRY CERTIFIED (`verified_gs_arc`). 🍅 BEEFSTEAK (anchor 2/9) ARC OPEN -- Step 3.5 DONE, NEXT = Step 4
**2 of 9 anchors certified.** `cherry-tomato` (first full v1.5 arc) + `lettuce-leaf` (M15) both carry `status="verified_gs_arc"`, both `GATE: PASS`. **M16 `beefsteak-tomato` (anchor 2 of 9) has STARTED:** **Step 3.5 (Region shell build, Claude Code lane) is COMPLETE** -- all 10 region cells built to cherry's reference shape, §A2 SHAPE gate = 0 (`gs_exemplar_finding_shell` closed for beefsteak). **NEXT = beefsteak Step 4 (warm-region sourcing, claude.ai lane)** -- handoff prepared. The post-cert **tooling-hardening batch is now COMPLETE** (#1 patch applier, #2 walker fix, #3 pre-commit hook, runbook v1.0), and the region-shell toolchain was generalized for all 9 anchors this session. **(Operating model: claude.ai authors, Claude Code releases.)**

## Canonical pointer
- **Current SHA:** `006cd0afbab0d3b9fab8909a870c3ac98909b3f066c5d6c0f8f4457693ec0071` (beefsteak Step 3.5: 9 warm region shells + `northern_tier` promote-from-zones; ONLY `beefsteak-tomato.regions` changed -- `zones{}`, lettuce, cherry, catalog all byte-identical). `LATEST.txt` session: `m16_beefsteak_step3_5_region_shells`.
- **NEXT: beefsteak Step 4 warm-region sourcing (claude.ai) -- preflight against `006cd0af`.**
- **Predecessor chain:** `006cd0af` (beefsteak Step 3.5) <- `87c8e0a1` (status vocab + lettuce gaps) <- `b6777ef6` (cherry Step 11 CERTIFIED) <- `84b086f1` (cherry 6/7/8, gate->0) <- `12348fa0` (cherry 5e warm_arid) <- ... <- `a65c7175` (cherry Step 3.5) <- `29b3aaa9` (M15 lettuce flip) <- ... (full chain in STATE_HISTORY).

## What just happened (2026-06-07, session `m16_beefsteak_step3_5_region_shells`)
- **Beefsteak Step 3.5 region shells BUILT (Claude Code structural lane).** All 10 `regions{}` cells brought to cherry's ratified reference shape via `tools/apply_region_shells.py beefsteak-tomato`:
  - **9 warm cells** (se_gulf, ca_interior, ca_north_coast, ca_south_coast, ca_desert, warm_arid, low_desert_az, fl_peninsula, hawaii_tropical): `PENDING` stub string -> shape-complete RULE skeleton (`track:"beginner"`, empty archetype window arrays, empty `anchoring_urls`, `region_notes_*` keys). The 4 `California -- X` `region_label` em-dashes resolved to `California: X`.
  - **`northern_tier`** promoted from the verified cold `zones{}`: `plantings[0].track` None->`beginner`; 5 `resolved_by_zone` cells stripped of the forbidden nested `plantings` (§3b-i) + the tautological `lifted_from_zone`, restamped `static_precompute`->`zone_promoted_verified`; `plantings_provenance` rewritten to the beefsteak promotion record. NT key structure now byte-identical to cherry's reference.
  - **Beefsteak is `succession_policy.suitable=false`** (a `second_planting` crop like cherry, NOT a succession crop) -- so NO succession hoist is needed; the `track:"beginner"` default is complete and correct.
  - **Gate:** §A2 SHAPE classes all **0** (`stub:0 | null-track:0 | stale-nested:0`) -- closes `gs_exemplar_finding_shell` for beefsteak. Total **49 -> 43**; the residual 43 is ALL DOWNSTREAM claude.ai work (10 region_notes-null Steps 6/7; 30 dual-voice incl. `cause_beginner` + 6 `growth_stages.log_prompt_beginner` Steps 6/7/8; 1 `sources_summary` dash Step 9; 1 `harvest_to_table` T2 Step 10; 1 `harvest_urgency` anchoring Step 4/5/10). Beefsteak has MORE dual-voice siblings than cherry (the corrected walker counts `growth_stages.log_prompt_beginner` etc.).
- **Region-shell toolchain generalized for reuse (Claude Code lane, commit `653234d`):** the cherry-pinned one-shots made reusable for all 9 anchors -- `build_region_shells` session/date params (NT provenance records THIS crop, not cherry); `apply_region_shells` reads the start-SHA gate from `LATEST.txt` (the cherry constant could not match any later base); the pre-commit hook is now **Step-3.5-aware** (forgives the stub->shell `region_notes`-null unmask, still blocks real region_notes-blanking); `test_build_region_shells` decoupled from canonical fill-state (synthetic stub fixture + cherry idempotency smoke). All tool unit tests PASS.

## Verification (protocol #6, this release -- a green gate is NOT a clean release)
- **§A2 SHAPE gate = 0** (admission pass). **Collateral:** only `beefsteak-tomato.regions` changed; `zones{}`, lettuce, cherry, `source_catalog` byte-identical. **release_verify:** the only NEW gate violations = the 9 expected `region_notes`-null unmasks (stub->shell); its §D flags 9 `--` strings that are ALL **pre-existing** legacy `zones{}`/Phase-B backend records (byte-confirmed unchanged base->scratch), correctly backend-exempt in `whole_crop_gate`. **Claim cross-check:** every byte change is an intended transform op (region_label dash, stub->skeleton, NT strip/restamp/provenance) -- zero unexpected field changes. **Pre-commit hook (Step-3.5-aware):** no regression, cleared 6.

## Active work + parked decisions
- **NEXT MILESTONE: beefsteak Step 4 (warm-region sourcing, claude.ai lane).** Source the 9 warm shells from the `region_source_map` T1 anchors (`se_gulf`->`uga_ext`/`ufifas_ext`; `ca_*`->`ucanr_ext`; `warm_arid`->`nmsu_ext`; `low_desert_az`->`uariz_ext`; `fl_peninsula`->`ufifas_ext`; `hawaii_tropical`->`uhawaii_ctahr`); drop orphaned cold (UMN) prose from any warm cell (the cherry `gs_exemplar_finding_001` pattern -- beefsteak carries the identical defect); clear `sources_pending_admission` per cell as it is sourced; `northern_tier` owes `calendar[12]` `cold_pause` derivation + `region_notes` (Steps 5.5/6/7). **Beefsteak re-derives ALL heat biology INDEPENDENTLY -- likely a WIDER pause than cherry** (less heat-resistant). Handoff at `~/Downloads/HANDOFF_beefsteak_step4/`.
- **PARKED -- beefsteak stale-flag reset (Step 11, NOT now):** beefsteak still carries `launch_ready_core/seasoned=true` + `status="verified_complete"` -- M11 pre-arc artifacts, NOT v1.5-arc-verified. Reset-then-re-earn at beefsteak's OWN Step 11 (exactly as cherry's stale M10 flags were). Do NOT treat beefsteak as arc-done.
- **PARKED -- Trevor decisions (none block beefsteak Step 4):** (1) `fruit_set_temp_f` schema shape (T1 anchors in hand; schema-touching -> Trevor rules shape, Claude Code adds field). (2) optional `ca_south_coast` z9 soft-`cold_pause` revert to `wait`. (3) lettuce `why_beginner` copy (Radishes/Carrots/Chives) is Claude-Code-drafted -- Trevor sanity-check.
- **PARKED -- Claude Code tooling note (non-blocking):** `release_verify.py` §D user-facing scan has a NARROWER backend filter than `whole_crop_gate.py`'s `is_backend` (it lacks the `anchoring_urls` + `zone_\d+_` exemptions), so it over-flags pre-existing legacy `zones{}`/Phase-B backend strings as user-facing dashes. `whole_crop_gate` is the authoritative cert gate; align the two filters in a future tooling pass.
- **PARKED -- claude.ai checklist amendments:** `lifted_from_zone`-strip into Step 3.5 text; °F-in-user-facing rule; retire "every cell needs a county MG"; window-structure-is-a-source-finding (Path A fallback); heat-set-failure-month = heat_pause token + second_planting action.

## Gate record (2026-06-07, on canonical `006cd0af`, CORRECTED walker)
- **cherry `GATE: PASS` (0); lettuce `GATE: PASS` (0).** Both: launch_ready core+seasoned=true, `status="verified_gs_arc"`.
- **beefsteak `GATE: 43`** -- the Step-3.5 admission state, NOT a failure. §A2 SHAPE = 0 (shells built); the 43 residual is all downstream Steps 4-10 (region_notes copy, dual-voice siblings, the 1 source-name dash, the 1 T2, the 1 anchoring gap). The arc is mid-flight.

## Region fill state
**cherry-tomato -- 10/10 authored, verified, CERTIFIED (the reference exemplar):**
| region | zones | status | window | heat_pause | second_planting |
|---|---|---|---|---|---|
| `northern_tier` | 3-7 | VERIFIED | cold (frost-bracketed) | none (frost-limited) | yes, z6-7 |
| `ca_interior` | 8-9 | VERIFIED | single | none | none |
| `ca_north_coast` | 9-10 | VERIFIED | single (May) | none (COOL-limited) | none |
| `ca_south_coast` | 9-10 | VERIFIED | single (long Apr-Jul15) | none (mild marine) | none |
| `se_gulf` | 8-9 | VERIFIED | two-window | month 7 (cherry-narrowed) | yes |
| `ca_desert` | 9-10 | VERIFIED | two-window | Jun-Aug (absolute) | yes |
| `low_desert_az` | 9 | VERIFIED | two-window | Jul-Aug (absolute) | yes |
| `fl_peninsula` | 10-11 | VERIFIED | near-continuous | Jul-Aug (cherry-narrowed) | none |
| `hawaii_tropical` | 11 | VERIFIED | year_round | none (oceanic-tropical) | none |
| `warm_arid` | 8 | VERIFIED | two-window (Mar + Jul) | month 7 (cherry-narrowed) | yes |

**beefsteak-tomato -- 10/10 SHELLS BUILT (Step 3.5), 0/10 sourced (Step 4 pending).** Every cell at cherry's reference shape: warm cells = `track:"beginner"` skeletons with empty windows + null `region_notes` (await Step 4 sourcing + Steps 6/7 copy); `northern_tier` = promoted + verified from `zones{}` (windows real; owes `calendar` `cold_pause` + `region_notes`). Beefsteak re-derives its OWN warm windows + heat biology at Step 4/5 (likely wider pause than cherry).

## Flip gates (the four distinct "flips")
1. **Per-crop `launch_ready` flip** -- ✅ lettuce (1), ✅ cherry (2, first FULL arc). **Beefsteak in progress (Step 3.5 done, Steps 4-11 remain).** Then 6 more anchors.
2. **Region read-layer flip** -- renderer reads `regions{}` first. Gate: shape proven on lettuce + cherry; beefsteak shells now built (owes Step 4-11 fill). Ships with `zones{}` fallback. **2.9+.**
3. **Authoring-model flip** -- carrots onward region-first. Gate: 3 provers (cherry done; beefsteak is prover 2, in flight).
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, 2.9+. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial = **2.9+.**

## Live locked decisions / guardrails (carry into beefsteak Step 4)
- **Reference gold-standard crop (Step 3.5 shape) = `cherry-tomato`** (cleanest fully-arced exemplar; repointed from lettuce). Dataset is authoritative; flag doc lag.
- **BEEFSTEAK RE-DERIVES ITS OWN HEAT BIOLOGY -- likely a WIDER pause than cherry** (less heat-resistant). Do NOT carry cherry's per-region pause widths onto beefsteak by analogy. Cherry's rule: narrow the pause only where heat is marginal (se_gulf z8, warm_arid z8 = single-month Jul), NOT where absolute (z9 deserts = Jun-Aug). Beefsteak sources its own.
- **Heat-set-failure month that is ALSO a planting month = `heat_pause` calendar token + the plant carried by `second_planting{}`** (Trevor 2026-06-07). **WINTER COLD = `cold_pause` token, NO sibling object** (not on frost-free z10, which stays `wait`).
- **DUAL-VOICE: every in-scope `_seasoned` field needs a plain `_beginner` sibling.** Backend prose (synthesis_note, *_basis, source_quote) is seasoned-only by design. Companions `why_beginner` is in-scope (walker fixed `ac5f49f`).
- **WINDOW STRUCTURE is a SOURCE FINDING; NEVER carry a multi-window shape on analogy** (Path A is the fallback for visual-chart sources).
- **`harvest_to_table` T2-as-evidence: T1-only, NO grandfathering.** **TEMPERATURE user-facing = `°F` not "degrees F"** (backend prose may spell it).
- **CATALOG ADMISSION (county MG = UC ANR/NMSU = T1):** discovery+verified-URL = claude.ai; catalog write = Claude Code (mint the ID).
- **`second_planting` = discrete-window object (Claude Code lane), seasoned-only; succession = `succession_spring/fall`; main = flat cell fields.** Each crop carries ONLY its structures. **Lettuce NOT reshaped.** Spec in `docs/superpowers/specs/`.
- **Lane split:** STRUCTURAL/MECHANICAL = Claude Code; biology + consumer copy + voice/IP + URL discovery + dates = claude.ai.
- **Keep `zones{}` coherent until Phase C** (renderer still reads it).
- **Release sequence:** `docs/release_runbook_v1_0.md` (the full how); protocol #6 before every promote.
