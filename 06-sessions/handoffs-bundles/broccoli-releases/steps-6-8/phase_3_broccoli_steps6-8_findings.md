# plant -- Broccoli Steps 6-8 Findings (consumer prose + the 7 compounds)

**Session:** `broccoli_steps6-8` (claude.ai author lane)
**Date:** 2026-06-23
**Crop:** `broccoli` (archetype `cool_season_annual`, `calendar_basis: frost_anchored`)
**Checklist:** gold-standard arc checklist v2.0, Steps 6 / 7 / 8 + Appendix A + dual-register v1.1.
**Start (slice crop) SHA:** `a68e13add84abfc2d7cf6431b7e3959e5202134c4367e11aa672c46120d9f21c` (preflight CLEAN vs `SLICE_INTEGRITY.md`; full-file `78ef87cd` per `LATEST.txt`).
**Post-author crop SHA:** `8f93303ace8535f9723e3619417ad2399aed7e9cbd23d30c3580e3f06f8761cf`
**Register scope:** both `_seasoned` and `_beginner` (Steps 6 verify + 7/8 siblings, in one leg).

---

## Scope delivered (the COMPUTED worklist, walked -- not hand-enumerated)

The raw null-walk of the slice surfaced 303 nulls; **265 are out of the 6-8 lane and correctly resting** (104 `uscrn_validation` sub-objects = Phase 1.1 pipeline; 81 legacy `zones{}` = the deferred re-source layer; 60 `resolved_by_zone` derived notes = resolved/CC layer; 10 companion `provenance.verified_date` = traditional->null by design; 2 `verification_status` = Step 11 cert flip; plus 4 z11 frost-free `resolved_from` nulls and a few CC structural flags). **The 6-8 lane is exactly:**

- **36 register-prose nulls authored as pairs:** 10 `region_notes_*` pairs (20) + `storage` 4 pairs (8) + `yield_expectations` 3 pairs (6) + `container_notes.shape_requirements` (re-authored as a CP pair, +2; see Decision 1).
- **`moon_phase_preference`** 3 sub-fields -> N/A prose (carrot precedent; never null).
- **7 compounds:** `growth_stages` (6), `pests` (4), `diseases` (3), `failure_diagnostics` (4), `notifications` (3), `weather_triggers` (2), `tips_by_stage` (12 tips across 6 stages).

**Collateral audit: only the 12 in-lane top-level blocks changed; 0 out-of-lane leaves touched** (`+372 / -1 / ~37`; the `-1` is the `shape_requirements` scalar renamed to the pair). zones{}, uscrn, verification_status, resolved_by_zone, plantings_provenance all byte-untouched.

---

## Step 6 (seasoned depth-lift) -- a VERIFY pass

Broccoli authored most of its 1-3 prose fresh to the GS bar, so Step 6 over the existing fields (`description`, `fertilizer`, `watering`, `rotation`, `container_notes.notes`, `start_method`, `soil`, `ph`, `varieties`, `succession_policy`) was a verify pass: each reads at the cherry seasoned-depth bar (mechanism + numeric specificity + regional/contextual nuance + honest-about-tradeoffs). No terse field required a lift. The NEW 6-8 `_seasoned` fields (region_notes, storage, yield, shape_requirements) were authored to that bar with T1 backing + anchoring.

## Step 7 (top-level/dict beginner siblings) -- pre-existing gap = 0

Every populated `_seasoned` CP field on the released base already carries its `_beginner`. The naive walk flagged 130 "owed" siblings; **all 130 are out-of-denominator** and were excluded against the certified contract (verified by matching the released, gate-passed base `a68e13ad`):
- `synthesis_note_seasoned` (region planting arms) and `*.basis_seasoned` (pause objects) are **single-register backend** evidence prose (A3 `_basis_family`; the source-synthesis audit layer). No `_beginner` twin on any certified crop.
- `soil.*_texture_seasoned` pairs with `*_texture_core` (USER-FACING-CATEGORICAL token), not a `_beginner`. SP, not CP.
- `companions.good_seasoned[]` / `bad_seasoned[]` are the **seasoned-only** arrays; beginner-visible siblings live in the separate populated `good_beginner_seasoned[]` / `bad_beginner_seasoned[]` arrays. Array membership encodes visibility (the three-array shape).

Step 7's real work was authoring the `_beginner` siblings for the NEW 6-8 fields only.

## Step 8 (per-entry siblings + dual-voice coverage gate)

Every `audience:"core"` compound entry carries its required `_beginner` siblings, including `cause_beginner` on all pests and diseases. **Dual-voice coverage gate: PASS (0 missing keys / 0 null)** on the correct denominator.

---

## Structural decisions (both surfaced to Trevor pre-authoring; adjudicated)

### Decision 1 -- `growth_stages` ids = the 6 live `tips_by_stage` keys (Fork 1, Option A, confirmed)
The slice's `tips_by_stage` was pre-keyed at the shell stage with **6 ids**: `germination, seedling, established, head_forming, harvest, side_shoots`. Adopted these verbatim as the `growth_stages[].id` set rather than the kickoff DRAFT's 7-stage list. Rationale (Trevor-confirmed against the certified data): every certified crop's `growth_stages` ids equal its `tips_by_stage` keys exactly, and the stage set is crop-specific (carrot=4, lettuce ends with `bolting`, green-beans uses `pod_set_fill`, zucchini has `flowering`+`end_of_season`); there is NO universal stage set and NO mandatory `end_of_season`/`vegetative`. Broccoli's `head_forming`+`side_shoots` ARE its crop-specific beats; `established` covers the leafy-frame ("vegetative") stage; season-end is carried by the calendar `cold_pause`/`season_over`/`heat_pause` tokens, not a stage. **A12 id-coverage: EXACT MATCH** -- zero orphan-key risk into the gate.

### Decision 2 -- `weather_triggers` title/body = CP pairs; machinery = bare (Fork 2, confirmed)
Each `weather_triggers` entry carries `title_seasoned`/`title_beginner` + `body_seasoned`/`body_beginner` (user-facing, dual-register, like `notifications`); the trigger machinery (`condition`/`action`/`severity`/`active_stages`/`audience`) is bare enums, no siblings. The renderer shows the body text, so the compound is not all machinery. Matches the certified cherry/lettuce `weather_triggers` shape; CC will conform any minor machinery-key detail at release.

### Decision 3 -- `container_notes.shape_requirements` re-authored as a CP PAIR
Per the green-beans ruling (CURRENT_STATE locked decision): `shape_requirements` is ruled CP, so a populated `_seasoned` requires a populated `_beginner`. The scalar null `shape_requirements` was dropped at Steps 1-3 (deferred to 6-8 to avoid freehanding the beginner register); re-authored here as the pair `shape_requirements_seasoned` + `shape_requirements_beginner`. **Flag for release:** this renames a scalar key to a pair (the `-1 / +2` in the collateral count) -- a structured-null closure, surfaced here for the review.

### Decision 4 -- `moon_phase_preference` = N/A prose (never null)
No-evidence field (carrot precedent). Set `phase: "none"`, `evidence_tier: "none"`, and authored `source_note_seasoned` as honest N/A prose (no extension/peer-reviewed support for lunar timing; plant by soil temperature/frost/windows instead). `register_fill_gate` rejects null; N/A fields get N/A prose.

---

## Anchoring (REQUIRED cert work, closed in this pass)

Each touched block was anchored in the same pass (block-coherent authoring, scope A):
- **`storage`, `yield_expectations`:** `sources = [umn_ext_broccoli, umd_ext_broccoli]` + `anchoring_urls` (both already in the 133-entry catalog, T1).
- **`pests` (4) and `diseases` (3):** each entry anchored `sources = [umn_ext_broccoli, umd_ext_broccoli]` + `anchoring_urls`.
- **`tips_by_stage`:** per-tip `sources` ([umn/umd] or [ufifas_ext_broccoli]) + `evidence_tier: T1`.

**No new source mints required.** All cited IDs (`umn_ext_broccoli`, `umd_ext_broccoli`, `ufifas_ext_broccoli`) are existing T1 catalog parents (minted at Steps 4-5.5). These are whole-guide parents that legitimately cover the storage/yield/pest/disease claims. **Release-lane option:** if the release lane prefers finer granularity, it may mint page-specific sub-ids under these parents (e.g. a postharvest sub-page), but the parents are claim-bearing as-is. Surfaced as a choice, not a defect.

---

## Source-fidelity (author-side; the independent fetch is Step 11)

Live T1 corroboration captured this session (2026-06-23) for the cert-sensitive numerics:
- **Heat threshold 86°F day / 77°F night** stops heading -- UMN broccoli guide, exact (drives `bolting`, the region `heat_pause` bases, and the heat-watch trigger).
- **Head size 4 to 8 inches** -- UMD ("mature heads measure 3 to 8 inches across"); my 4-8 is the heading-type figure inside that range.
- **Transplant at 4 to 6 true leaves; oversized starts -> buttoning** -- USU (verbatim on the buttoning mechanism).
- **Cabbageworm complex = cabbage looper / imported cabbageworm / diamondback moth; row cover control** -- WVU + UMN.
- **3-year brassica rotation** -- WVU; ties to the already-authored `rotation` block + clubroot.
- **1 to 1.5 in/week, even moisture for non-bitter heads** -- USU + UMN.
- **De Cicco side-shoot-heavy** -- MSU.
- **Germination 5 to 10 days; optimal 60 to 75°F** -- multiple T1; prose set to `60 to 75°F` (a valid optimal sub-range of the verified `germination_temp_f [40,86]`).

**8-gram source-verbatim scan: 0 overlaps** against the retrieved source snippets -- all prose paraphrased in own voice.
**Numeric fidelity: all quantitative claims internally consistent** with the slice's already-verified scalars (`spacing_inches [12,24]`, `weeks_indoors 5`, `min_pot 5 gal`, `depth 12 in`, `germination_temp_f`, `bolting.triggers 86/77°F`, `rotation 3yr`).
**Yield deliberately expressed as HEAD SIZE (4-8 in) + side-shoot narrative, NOT lb/10ft** -- avoids the green-beans yield-weight contradiction class (the recurring cert-fetch failure mode).

---

## Copy rules (user-facing surface) -- clean

Whole authored surface swept: **0 em-dashes, 0 `--`, 0 "degrees F"** (backend `synthesis_note`/`basis` excluded as backend prose). `°F` symbol throughout; American English; "broccoli" lowercase. CP fields are suffixed siblings (`parent.X_seasoned` / `parent.X_beginner`), never nested.

---

## Handback to Claude Code (release lane)

1. Preflight `sha256(crops_data_final.json) == LATEST.txt` (`78ef87cd`); apply the authored slice (or derive a patch); confirm only `broccoli` changes.
2. Run `whole_crop_gate` (expect residual -> **0**: region_notes filled 10/10, all 7 compounds populated, dual-voice 0 missing / 0 null, A12 tips rendering-conformant) + `register_completeness` + `register_fill` + `release_verify` (lettuce-leaf must stay byte-identical).
3. **Confirm the `shape_requirements` scalar->pair rename** (Decision 3) is a clean structured-null closure, not a novel key.
4. Then **Step 9** (whole-crop dash/temp sweep) -> **Step 11 cert** (the independent T1 source-fidelity WebFetch + the flip), which also resolves broccoli's Steps-4-5.5 carry-forwards: F-broc-h11-001 (hawaii window), F-broc-warmarid-001 (Dona Ana Path-A), the se_gulf z9 heat_pause attestation, F-broc-001 (rotation_years=3), F-broc-005 (PK companion-vocab sync).

**Do NOT set `verification_status` (status / last_audited / launch_ready) -- that is Step 11, Claude Code.**
