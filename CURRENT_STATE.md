# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v2.0**; the evergreen branch is in `tree_region_model_evergreen_amendment_v1_0`) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push). At each new handoff, ARCHIVE the prior handoff + consumed PK folders (runbook §7-8).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's STATE_HISTORY claims** (counts/keys/enums; if the crop-SHA method diverges, fall back to the collateral leaf-diff). Then PROMOTE.

---


**6 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple) of a ~18 target. **LEMON arc** (anchor 7, first evergreen): Steps 1-3 + 3.5 + 4-5 + 6A + **6B done -- lemon is now REGISTER-COMPLETE** (`register_fill_gate` 0). Pre-cert. **NEXT = lemon CERT (Steps 9-11)** -- the last step before anchor 7 certifies.

## Canonical pointer
- **Current SHA:** `f1fce7472ccaa07bd5f99952775e9d817ac7d1273dd885863b9cac6525543ece`. `LATEST.txt` session: `lemon_6B` (2026-06-12).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `7df91190` -- feat(lemon): Step 6A -- the 6 biology surfaces
  - `6c9b9a54` -- feat(lemon): Steps 4-5 -- the evergreen region biology (10 regions live)
  - `3a094769` -- feat(lemon): Step 3.5 -- the evergreen region/calendar model (test-first)
  - `08556e21` -- feat(lemon): Steps 1-3 -- anchor 7, the FIRST evergreen / first citrus
  - `d228ed7b` -- feat(peach): register-fill backfill -- register-complete
  - `a821d6d4` -- feat(apple): CERTIFIED -- anchor 6, the second tree (Steps 9-11)
  - `0711aa99` -- feat(apple): Steps 6-8B -- register prose complete (anchor 6)

## What just happened (session `lemon_6B`)
- **LEMON Step 6B -- the 65 register/care fields** (`7df91190`->`f1fce747`). claude.ai authored 80 ops (65 prose + 15 citation/anchoring): watering (14), container_notes (16, the citrus-STRENGTH story), fertilizer (6), storage (8, store-on-the-tree), soil (2), start_method (4), yield (6), rotation (4, N/A perennial + replant caveat), description (2), harvest_ready (2), moon source_note (1). **`register_fill_gate lemon` 65 -> 0** -- lemon is register-complete.
- **Crop-SHA cross-check diverged (claude.ai method artifact, NOT a data error):** its pre+post SHAs both differ from the canonical sort-keys crop-SHA (it hashed a different serialization). **Dispositive collateral check used:** 118 leaves changed, ALL within the 6B register surfaces; zero stray; verification_status / regions / 6A biology byte-untouched. (Process note passed back: use the canonical `json.dumps(...,separators=(',',':'),sort_keys=True)` crop-SHA.)
- **Protocol #6:** whole_crop_gate lemon = 4 (ALL pre-cert anchoring, forgiven; A3=0, **dual-voice coverage complete -- 180 CP pairs, null_values 0**, dash 0, sources 9/0/0); register_completeness PASS; release_verify only-lemon / no-catalog / lettuce byte-identical; pre-commit clean. Verbatim DEFERRED to cert.

## Active work + next step
- **NEXT = lemon CERT (Steps 9-11), Claude Code lane:**
  1. **Close the 4 pre-cert anchoring gaps** (all have cited catalog sources -> populate anchoring from the catalog): `varieties/sources` (ucr_citrus/uf_ifas_hs1153/tamu_agrilife/ucanr_ext), `regions.hawaii_tropical.11` (ucanr_ext), `harvest_ready_anchoring_urls` (uf_ifas_hs1153/ucd_postharvest -- sources listed, dict left `{}`).
  2. **Step-11 verbatim scan** (anchoring URLs now exist; fetch + compare; flip-blocking on >=8-word HARD hits).
  3. **Variety-attribution decision** (claude.ai flagged `varieties.recommended[]` carry no per-variety sources surface -- decide if needed).
  4. **The flip:** set `verification_status.status = verified_gs_arc` + both `launch_ready`. Run A3/A4 + the perennial cert gate + register_fill (0) as the flip gates.
- **Then anchor 8 = orange-navel** -- the heat-accumulation gate, test-first at orange's Step 3.5.

## OWED
- **iOS-app forward dependency:** support the 7 new citrus enum values from 6A (notification action `fertilize`; weather actions `protect_from_frost`/`guard_against_heat_stress`/`avoid_oil_in_heat`; offset anchors `fruit_set`/`spring_growth_start`; stage `mature_bearing`).
- **start_method sources slot** (schema question, claude.ai flagged): add a structured sources slot to slot-less containers (start_method, moon_phase_preference) vs accept inline citation. Non-blocking; decide at/after cert.
- Carried: apple's 4 open_findings; `peach_rotation_shape_finding`; perennial-aware `rotation` shape; fold region-meta auto-populate into `_build_tree_shells`; Appendix A growth_stages `timing_*` reconcile (peach/apple fork; lemon matched apple); `apply_patch` reject-bare-slash hardening.

## Gate record (generated 2026-06-12, on canonical `f1fce747`)
- **cherry-tomato / beefsteak-tomato / carrot / peach / apple / lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**
- **lemon: 4 (pre-cert anchoring gaps only; A3=0, A4=0, register_fill=0, dual-voice complete, dashes 0; ALL authoring done; cert 9-11 is next)**

## Region fill state (generated)
- **6 certified anchors: 10/10 filled.**
- **lemon: COMPLETE through 6B** -- 10/10 evergreen regions filled, 6 biology surfaces live, 65 register fields authored (register_fill 0). Only cert (9-11) remains.

## Flip gates (generated)
- **6 anchors:** launch_ready true/true status=`verified_gs_arc`
- **lemon:** launch_ready False/False status=`None` (pre-cert; ALL authoring done; cert is the last step)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes) -->
- **EVERGREEN model (fully proven on lemon 2026-06-12):** `perennial_evergreen` + `gating_factors`; `min_winter_temp_f` climate; calendars DERIVED (`derive_evergreen_calendar`, A4-gated); z9 per-region; survives_no_fruit honest-empty; tropical = `year_round:true` + harvest fill; 6 biology surfaces = apple shape (single `timing`). Evergreen = 2 anchors (lemon 7, orange-navel 8).
- **Enum vocab grows per crop** -- REUSE canonical for existing concepts (Claude Code reconciles claude.ai's assumed enums at release); genuinely-new app-affecting values added w/ Trevor's bless + flagged as an iOS-app forward dependency.
- **Crop-SHA cross-check:** if claude.ai's method diverges, fall back to the collateral leaf-diff (only intended paths changed; verification_status/regions/prior-surfaces untouched) -- that's the real correctness check.
- variety-delta = CATEGORICAL; register-fill is a cert dimension; patch paths = leading-slash/dot; claude.ai self-dash + self-enum + self-SHA checks are advisory -- Claude Code re-verifies. pre-cert anchoring = admission state (`drop_precert_anchoring`).
