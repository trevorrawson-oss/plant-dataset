

**9 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple, lemon, orange-navel, basil) of a ~18 target. **ZINNIA in flight -- anchor 10, the FIRST flower (`companion_and_ornamental_flower`). Steps 1-3 + 3.5 DONE 2026-06-14:** scalars + 2.9 universal + variety set + INVERTED companions + dual-register prose authored fresh, then the 10 region SHELLS built (skeleton + start normalized to `both`). **NEXT = zinnia Steps 4-5 (claude.ai handoff): region biology + per-zone windows.**

## Canonical pointer
- **Current SHA:** `5e7e5f66ace50109083c0b36a09a30801ce7b66359c0b35fe20cfe6886233ab2`. `LATEST.txt` session: `zinnia_steps3_5_region_shells` (2026-06-14).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `aff87ab3` -- feat(zinnia): Steps 1-3 -- anchor 10, the first flower
  - `94d647f8` -- feat(gate): always-on annual calendar coherence (A5) + fix tomato start_indoors token
  - `0678212e` -- fix(basil): citation hygiene -- remove dead UMaine link, confirm PSU URLs live
  - `c998b1cb` -- feat(basil): CERTIFIED -- anchor 9, the first herb
  - `de9f54bf` -- feat(basil): Step 11 verbatim reword + JB re-pin (flip HELD on AZ finding)
  - `83ed20e5` -- feat(basil): Steps 6-8 -- bulk prose; register-complete + gate-clean
  - `48c9580f` -- feat(basil): Steps 5C + 5.5 -- per-zone harvest resolution + derived calendars

## What just happened (session `zinnia_steps3_5_region_shells`)
- **ZINNIA Step 3.5 region shells BUILT** (`aff87ab3` -> `5e7e5f66`), Claude Code deterministic pass via `build_region_shells.py` (the ratified M16 builder). All 10 regions graduated from PENDING stubs to the shape-complete RULE skeleton: each carries a `plantings[]` main-arm skeleton + `region_notes_*` slots; the 4 `California -- X` region_label em-dashes resolved to `California: X`. No biology/dates invented (Steps 4-5 fill them).
- **Fixed an off-enum value the 1-3 gates missed:** `start_method.start` was `"direct_sow_or_transplant"` (non-canonical); normalized to **`both`** (the certified enum is {direct, both, indoors}; basil = `both`). The author's value literally meant both methods, so this is a faithful normalization. `both` -> the transplant region shape (`start_indoors` + `plant_out`), matching basil; direct-sowers read `plant_out` as their sow date (zinnia's hero method per `start_method.notes`).
- **Verification:** `whole_crop_gate zinnia` = 10 violations, now ALL `region_notes pair both null` (the regions have skeletons but no notes yet) -- the explicitly accepted Step-3.5 admission state (`precommit_release_verify.drop_shell_build_unmasks` exempts exactly these; Steps 4-7 fill region_notes). The 10 `plantings stub/missing` violations CLEARED. dash/temp 0/0; release_verify reviewed (the region_notes-null CONCERN is the known shell-build forward-state, not a regression).

## Active work + next step
- **zinnia 1-3 + 3.5 DONE.** Region shells built; regions carry skeletons + null notes (the 10 `region_notes both null` violations are the accepted Step-3.5 admission state, not a regression). 9 anchors certified + zinnia in flight (anchor 10).
- **NEXT = zinnia Steps 4-5 (claude.ai HANDOFF):** region biology + per-zone windows (warm-season frost-tender, last-frost -> first-frost; succession suitable; `both` start = transplant shape, direct-sowers use `plant_out`), then 5C/5.5 per-zone windows + DERIVED calendars (`annual_calendar.py`, summer-centered), 6-8 bulk prose, cert. Build the 4-5 handoff (runbook §8): orientation trio + zinnia slice + sources/catalog + `00_KICKOFF`. zinnia = the `Companion & Pollinator` family exemplar + the second go-live demand crop.
- **Rulings flagged by claude.ai (none block; sensible defaults, confirm at leisure):** vase-life-in-`storage.notes_*` as the canonical home (vs a future ruled `vase_life` field if cut-flower crops proliferate); no `sources_summary.secondary` T2 slot; `moon_phase_preference` left unset.
- **Separate track:** the tree GUIDE PAGE on plant-astro (apple-zone-6 mock; 4 certified trees to template from).

## Gate record (generated 2026-06-14, on canonical `5e7e5f66`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **basil: `PASS` (0)**
- **peach: `PASS` (0)**
- **apple: `PASS` (0)**
- **lemon: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **orange-navel: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **basil: 10/10 region cells filled**
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lemon: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause
- **orange-navel: 10/10 region cells filled**

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **basil:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **apple:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lemon:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **orange-navel:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **9 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
- **`start_method.start` ENUM = {direct, both, indoors}** (carrot/lettuce=`direct`, basil/zinnia=`both`, tomatoes=`indoors`). `build_region_shells` reads it: `direct` -> `direct_sow` window shape; `both`/`indoors` -> transplant shape (`start_indoors` + `plant_out`, direct-sowers read `plant_out` as the sow date). A non-canonical value (zinnia shipped `direct_sow_or_transplant`, normalized to `both`) silently mis-shapes the region build -- author the ENUM value, not prose. **STEP-3.5 ADMISSION STATE:** after the shell build, regions legitimately carry skeletons + null `region_notes` (Steps 4-7 fill them); `precommit_release_verify.drop_shell_build_unmasks` EXEMPTS the `region_notes both null` violations of stub->shell graduated regions (not a regression). release_verify's cell-model flags them as a CONCERN -- that is the human-review hook, not a block. The ratified 3.5 skeleton carries `anchoring_urls:{}` per planting (cleaned/relocated at Steps 4-5).
- **FLOWER / ORNAMENTAL ARCHETYPE -- proven on zinnia (anchor 10, the FIRST flower):** frost-tender heat-lover on the basil annual rails (summer peak, NO heat_pause, `pause_in_heat:false`); grown for BLOOMS not food -> bloom-centric care (deadhead + cut drive cut-and-come-again; NO `bolting` field -- flowering is the goal). Flower slots live IN the shell: `flower_type` scalar, `deadheading_seasoned/_beginner` pair, `harvest_ready_*` repurposed for the cut-flower cut cue, vase life -> `storage.notes_*` (edible room_temp/fridge/freezer stay null). Disease = powdery mildew, resistance is VARIETY-led (Profusion/Zahara interspecific hybrids = the zinnia DMR analog). The template for the 5-crop `Companion & Pollinator` family (marigold/cosmos/sweet-alyssum/sweet-pea).
- **COMPANION ITEM SHAPE = the certified carrot rich-object shape (NOT a flat `why`).** `good_seasoned[]` = {name, category, timing, why_seasoned, notify_weeks_before, provenance:{label, confidence, reason, verified_against_sources, verified_date}, mirrored evidence_label/confidence/verified_against_sources, sources, anchoring_urls}; `good_beginner_seasoned[]` = {name, why_beginner}; `good_beginner`/`bad_beginner` empty; the bad-companion caution folds into `note_*`. **VOCAB = `research_backed` / `likely` / `traditional`** -- the cherry-era `extension_backed`/`mechanistic`/`disputed` are DEPRECATED (checklist v1.6 text is STALE on this; carrot certified with the new labels). `register_completeness_gate` HALTs on a flat `companions.*.why` key. For a pollinator crop the companion frame INVERTS: zinnia is the DRAW (good = the crops IT benefits), not the beneficiary.
- **SOURCE-TIER: certified crops carry ZERO non-T1.** `johnny_seeds` (and seed-company / almanac sources) = T2 -- usable as evidence-log corroboration, NEVER a dataset claim citation; `whole_crop_gate` E flags any non-T1 in scope.
- **HERB ARCHETYPE -- cert-proven on basil (anchor 9):** heat-LOVING (inverse of lettuce -- summer is peak, NO heat_pause, `pause_in_heat:false`); frost-limited both ends; `year_round` for frost-free hawaii; bolting herb-central; chilling-injury storage (no root-veg "refrigerate X weeks"); foliar-wetness disease nexus; DMR variety notation sweet-basil-specific (derive each herb fresh). The template for the other tender heat-loving annual herbs.
- **CERT VERBATIM GATE = SOURCE FIDELITY, not just lifts:** verify source CLAIMS against the LIVE source at cert; a self-contradicting source cannot sole-anchor a window; re-source (re-anchor to a cleaner catalog-named publication + demote the weak one to its supported scope), never quick-edit dates. "The findings said the source says X" is not proof. (basil low_desert_az: az2061 -> az1005 primary + az2061 care co-anchor.) CITATION HYGIENE: re-pin only after fetch+verify; unreachable URLs filed NOT-COVERED (blocks_launch:false), never hidden.
- **ANNUAL CALENDAR DERIVATION + COHERENCE (`tools/annual_calendar.py`):** the DERIVER computes simple summer-centered calendars from resolved windows (explicit plant_out authoritative; direct-sow = envelope minus harvest; `cold_pause` anchored at deep winter; `year_round` -> 12x growing; reproduces carrot NT z5 exactly). It is NOT used to re-derive complex multi-cycle (winter-wrap / heat-inverted) cells -- those are legitimately hand-authored and a clean deriver would degrade them. The always-on enforcement is `annual_coherence_violations` (whole_crop_gate A5): consistency, not re-derivation -- bad length / non-enum token (catches `start_indoors`) / heat_pause-object-vs-token mismatch are HARD; `wait` is a NOTE. So: derive the simple, hand-author the complex, gate BOTH for coherence.
- **PROCESS ATTESTATIONS -> STATE_HISTORY, not crop data** (basil 6-8: `region_tip_override_assessment` stripped). **`*_basis` evidence prose is BACKEND (A3):** bare `*_basis` keys EXCLUDED via `_basis_family`. **6-8 worklist is a COMPUTED SWEEP** (`register_fill_gate` + empty compounds; release re-runs to 0).
- **ANCHORING:** every `plantings[]` arm anchors to the SPECIFIC verified page (lettuce = B577 PDF / VH021), never the homepage; nested `{id:{url,verified:DATE}}`. A split sub-ID (`uariz_ext_az2061`, `uf_ifas_vh021`) scopes a multi-topic publisher to the specific bulletin.
- **TOOLING (basil-surfaced):** `apply_patch` `add` tolerates empty-equivalent shells; `sources_summary` subtree EXCLUDED.
- **EVERGREEN + HEAT model -- COMPLETE + cert-proven (lemon cold-only, orange cold+heat).** heat `marginal` -> suitability `marginal`. Ready to replicate to grapefruit.
- **CERT mechanics / THE FLIP:** source-verbatim (vs cited URLs) is the flip gate; sibling-crop echo is a separate voice call. The FLIP = `verification_status` block (status verified_gs_arc + phase + launch_ready x2 + last_audited + source_set + verification_log_ref + open_findings all blocks_launch:false) + top-level last_reviewed/_session.
- TREE per-variety schema = lemon's 11-key set incl. `delta`. claude.ai self-checks are advisory -- the gates are the defense.
