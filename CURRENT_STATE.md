# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS/enums). Then PROMOTE.

---


**6 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple) of a ~18 target. **LEMON arc** (anchor 7, first evergreen): Steps 1-3 + 3.5 + 4-5 + **6A (the 6 biology surfaces) done**. Pre-cert. NEXT = claude.ai lemon Step 6B (the 65 register/care fields).

## Canonical pointer
- **Current SHA:** `7df91190edabaa57d1067e28989ae59348db48e4e399a4019e000befb5982095`. `LATEST.txt` session: `lemon_6A` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `6c9b9a54` -- feat(lemon): Steps 4-5 -- the evergreen region biology (10 regions live)
  - `3a094769` -- feat(lemon): Step 3.5 -- the evergreen region/calendar model (test-first)
  - `08556e21` -- feat(lemon): Steps 1-3 -- anchor 7, the FIRST evergreen / first citrus
  - `d228ed7b` -- feat(peach): register-fill backfill -- register-complete
  - `a821d6d4` -- feat(apple): CERTIFIED -- anchor 6, the second tree (Steps 9-11)
  - `0711aa99` -- feat(apple): Steps 6-8B -- register prose complete (anchor 6)
  - `3c8ac5e9` -- feat(apple): Steps 6-8A -- bulk care prose + key-shape reconcile (anchor 6)

## What just happened (session `lemon_6A`)
- **LEMON Step 6A -- the 6 biology surfaces** (`6c9b9a54`->`7df91190`). claude.ai authored 6 ops (clean apply, crop SHA matched the claimed `fb3e0bea` pre-reconcile): `pests` (6; ACP at high w/ regional-honesty prose), `diseases` (6; Phytophthora headline + canker/HLB regionally scoped, HLB<->ACP cross-ref), `growth_stages` (6; apple shape -- single `timing`, no `day_range_from_sow`), `failure_diagnostics` (5), `notifications` (4), `weather_triggers` (3). All dual-register; `growth_stages_annual`/`_year_one` left empty/null (N/A for a tree).
- **ENUM RECONCILIATION (Claude Code; the flagged open question):** claude.ai had no enum examples in the slice. **Remapped 53 values to canonical** (audience both->core, severity moderate->medium, condition temp->FROST_WARNING/HEAT_STRESS, trigger_type/stage/offset_from/action/year_phase/type synonyms). **ADDED 7 new citrus enum values (Trevor-blessed):** notification action `fertilize`; weather actions `protect_from_frost`/`guard_against_heat_stress`/`avoid_oil_in_heat`; offset anchors `fruit_set`/`spring_growth_start`; stage `mature_bearing`. **iOS-app forward dependency -- see OWED.**
- **Protocol #6:** whole_crop_gate lemon = 2 (carried pre-cert anchoring; A3=0, A4=0, dual-voice coverage complete [148 CP pairs, null_values 0], dash 0); register_completeness PASS; **register_fill_gate = 65 UNCHANGED** (6A is biology, not register -- confirms scope); release_verify only-lemon/no-catalog/no-new-violations/lettuce byte-identical; pre-commit clean. Verbatim DEFERRED to cert.

## Active work + next step
- **NEXT = claude.ai lemon Step 6B (the 65 register/care fields):** watering (19), fertilizer (14, w/ the high-pH iron/zinc micros), container_notes (21 -- lemon's OWN container-as-STRENGTH story, NOT peach's "not recommended"), storage (10 -- store-on-the-tree advantage), yield (9), tips (9), harvest_ready_beginner. `register_fill_gate lemon` (currently 65) is the worklist driver -> must approach 0.
- **Then lemon 9-11 (cert):** the Step-11 verbatim scan, close the 2 anchoring gaps (`varieties/sources` + `hawaii.11`), the variety-attribution call, the flip.
- **Anchor 8 = orange-navel** -- the heat-accumulation gate, built test-first at orange's Step 3.5.

## OWED
- **iOS-app: support the 7 new citrus enum values** (notification action `fertilize`; weather actions `protect_from_frost`/`guard_against_heat_stress`/`avoid_oil_in_heat`; offset anchors `fruit_set`/`spring_growth_start`; stage `mature_bearing`) -- the app track must handle them for citrus notifications to fire correctly.
- lemon cert items: the 2 pre-cert anchoring gaps (`varieties/sources` + `hawaii.11 ucanr_ext`); the variety-attribution decision; the Step-11 verbatim scan.
- Carried: apple's 4 open_findings; `peach_rotation_shape_finding`; perennial-aware `rotation` shape; fold the region-meta auto-populate into `_build_tree_shells` for future trees; Appendix A growth_stages `timing_*` reconcile (the peach/apple fork lemon sidestepped by matching apple); `apply_patch` reject-bare-slash hardening.

## Gate record (generated 2026-06-12, on canonical `7df91190`)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- **lemon: 2 (pre-cert anchoring gaps only; A3=0, A4=0, dual-voice complete, dashes 0; 6 biology surfaces live; 6B register + cert remain)**

## Region fill state (generated)
- **6 certified anchors: 10/10 filled.**
- **lemon: 10/10 evergreen regions FILLED + 6 biology surfaces LIVE** (pests/diseases/growth_stages/failure_diagnostics/notifications/weather_triggers). 6B register prose + cert remain.

## Flip gates (generated)
- **6 anchors:** launch_ready true/true status=`verified_gs_arc`
- **lemon:** launch_ready False/False status=`None` (pre-cert; 1-3 + 3.5 + 4-5 + 6A done)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes) -->
- **EVERGREEN model (built + region-proven + biology-proven 2026-06-12):** `perennial_evergreen` calendar_basis + `gating_factors`; cold-gated climate = `min_winter_temp_f`; calendars DERIVED via `derive_evergreen_calendar` (A4-gated); z9 per-region by frost; survives_no_fruit = honest empty; tropical year-round = `year_round:true` + harvest fill (A4 skips). The 6 biology surfaces = apple shape (single `timing`). Evergreen = 2 anchors (lemon 7, orange-navel 8).
- **Enum vocab grows per crop** but REUSE the canonical value for an existing concept (Claude Code reconciles claude.ai's assumed enums at release); genuinely-new app-affecting values (citrus frost/heat/feed actions, citrus phenology anchors) are added with Trevor's bless + flagged as an iOS-app forward dependency.
- **variety-delta descriptors = USER-FACING-CATEGORICAL**; register-fill is a cert dimension; **patch paths = leading-slash/dot**; **claude.ai self-dash + self-enum checks are unreliable** -- Claude Code re-scans + reconciles, the gates are the defense.
- **pre-cert anchoring is admission state** (`drop_precert_anchoring`).
