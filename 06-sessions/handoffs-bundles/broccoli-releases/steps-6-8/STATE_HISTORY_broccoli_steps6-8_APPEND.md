## 2026-06-23 — session `broccoli_steps6-8` (claude.ai lane)

**Start (slice crop) SHA:** `a68e13add84abfc2d7cf6431b7e3959e5202134c4367e11aa672c46120d9f21c` (preflight CLEAN vs `SLICE_INTEGRITY.md`; full-file `78ef87cd` per LATEST.txt).
**Post-author crop SHA:** `8f93303ace8535f9723e3619417ad2399aed7e9cbd23d30c3580e3f06f8761cf`. claude.ai authored DATA values + this entry only; **Claude Code applies (SHA-gated atomic write), runs `whole_crop_gate` + `register_completeness` + `register_fill` + `release_verify`, re-pins SHA, regenerates CURRENT_STATE, syncs, commits.**
**Gate:** not run this session. Expected residual after apply: **17 → 0** (the 10 region_notes-null + 6 empty compounds + 1 tips, all the deferred-zero from the Steps 4-5.5 release, now filled). Confirm 0 with `whole_crop_gate broccoli` at promote.

### What this pass was
Gold-standard arc v2.0 **Steps 6-8** (consumer prose + the 7 compounds) for **broccoli** — the FINAL authoring leg before cert. Step 6 was mostly a VERIFY pass (broccoli authored most of its 1-3 prose fresh to the GS bar); the core work was the new 6-8 surface. The cool-season analog of the zucchini 6-8 leg.

### What happened
- **36 register-prose pairs authored:** 10 `region_notes_*` (the spring/fall cool-season structure, derived from the windows authored at 4-5.5: 6 split with `second_planting` + 4 continuous; northern_tier `cold_pause` frost-bracketed both ends with NO heat exclusion, interior/south-coast/warm_arid `heat_pause` midsummer, deserts/FL/HI `season_over`; fall-out-yields-spring noted for the mid-Atlantic), `storage` (perishable head: ~1 wk fridge unwashed, freezes after blanching), `yield_expectations` (central head 4-8 in THEN side shoots; De Cicco/Calabrese side-shoot-heavy; `factors_seasoned` 4-item single-register list), `container_notes.shape_requirements` (re-authored as a CP PAIR — scalar dropped at 1-3, see decision below).
- **`moon_phase_preference` → N/A prose** (carrot precedent; `phase: none`, `evidence_tier: none`, honest `source_note_seasoned`; never null).
- **All 7 compounds populated:** `growth_stages` (6, ids = the live `tips_by_stage` keys), `pests` (4: cabbageworm complex / aphids / flea beetles / cabbage root maggot, each with `cause_beginner`), `diseases` (3: clubroot / black rot / downy mildew, each with `cause_beginner`), `failure_diagnostics` (4: buttoning / bolting / no-head-or-loose / hollow stem, 4-slot `what_happened`), `notifications` (3: harvest-before-open / side-dress-N / heat-watch), `weather_triggers` (2: heat-threatens-heading / hard-freeze, CP title+body + bare machinery), `tips_by_stage` (12 tips across the 6 stages, `text_seasoned`/`text_beginner`, A12-conformant).

### Structural decisions (both surfaced to Trevor pre-authoring; adjudicated)
1. **`growth_stages` ids = the 6 live `tips_by_stage` keys** (`germination, seedling, established, head_forming, harvest, side_shoots`), NOT the kickoff DRAFT's 7-stage list. The certified rule: `growth_stages` ids equal `tips_by_stage` keys exactly, the stage set is crop-specific, there is no universal set and no mandatory `end_of_season`/`vegetative` (`established` covers the leafy-frame stage; season-end is the calendar token, not a stage). **A12 EXACT MATCH — zero orphan-key risk.**
2. **`weather_triggers` title/body = CP pairs; machinery (condition/action/severity/active_stages/audience) = bare enums.** The renderer shows the body; the compound is not all machinery. Matches certified cherry/lettuce.
3. **`container_notes.shape_requirements` re-authored as a CP PAIR** (`_seasoned`+`_beginner`) per the green-beans CP ruling. Renames the scalar null to the pair (collateral `-1 / +2`) — a structured-null closure flagged for the release review, not a novel key.
4. **`moon_phase_preference` N/A prose** (register_fill rejects null).

### Step 7 pre-existing gap = 0 (the denominator call)
Every populated `_seasoned` CP field on the released base already carries its `_beginner`. The naive walk flagged 130 "owed"; **all 130 are out-of-denominator**, verified by matching the released gate-passed base `a68e13ad`: `synthesis_note_seasoned`/`*.basis_seasoned` are single-register backend (A3 `_basis_family`); `soil.*_texture_seasoned` pairs with `*_texture_core` (categorical, no `_beginner`); `companions.good_seasoned[]`/`bad_seasoned[]` are seasoned-only arrays (beginner siblings live in the populated `*_beginner_seasoned[]` arrays — membership encodes visibility). Step 7's real work was siblings for the NEW 6-8 fields only.

### Anchoring + sourcing (cert work closed this pass)
- Each touched block anchored in the same pass: `storage`/`yield_expectations`/`pests`(×4)/`diseases`(×3) → `sources [umn_ext_broccoli, umd_ext_broccoli]` + `anchoring_urls`; per-tip sources [umn/umd] or [ufifas_ext_broccoli], `evidence_tier: T1`.
- **No new source mints** — all three IDs are existing T1 catalog parents (minted at 4-5.5). Whole-guide parents legitimately cover the claims; release lane MAY mint finer page sub-ids if preferred (surfaced as a choice).

### Verification done (claude.ai lane — read-only on the slice)
- **Preflight slice crop SHA PASS** (`a68e13ad`).
- **Collateral audit:** only the 12 in-lane top-level blocks changed; **0 out-of-lane leaves touched** (zones{}, uscrn_validation, verification_status, resolved_by_zone, plantings_provenance all byte-untouched).
- **Dual-voice coverage gate PASS (0 missing / 0 null)** on the correct denominator.
- **A12 conformance:** `tips_by_stage` keys == `growth_stages` ids; all lists non-empty; all tips `text_seasoned`/`text_beginner` (no `tip_*` prose).
- **8-gram source-verbatim scan: 0 overlaps** vs the live source snippets (all paraphrased).
- **Numeric fidelity:** all quantitative claims internally consistent with verified scalars; live T1 corroboration captured (UMN 86/77°F heading-stall verbatim, UMD 3-8 in head, USU buttoning + 4-6 leaves, WVU cabbageworm complex + 3yr rotation, MSU De Cicco). **Yield expressed as HEAD SIZE not lb/10ft** — avoids the green-beans yield-weight contradiction class.
- **Copy rules:** 0 em-dash / 0 `--` / 0 "degrees F" across the authored user-facing surface; `°F` symbol; broccoli lowercase.

### Flag for Claude Code (release lane)
1. Apply the slice; confirm only `broccoli` changes; **confirm the `shape_requirements` scalar→pair rename is a clean structured-null closure (Decision 3), not a novel key.**
2. `whole_crop_gate` residual **17 → 0**; register + A12 compound gates; `release_verify` (lettuce-leaf byte-identical).
3. Then **Step 9** (dash/temp sweep) → **Step 11 cert** (source-fidelity WebFetch + the flip; resolves the 4-5.5 carry-forwards F-broc-h11-001 / F-broc-warmarid-001 / se_gulf z9 heat_pause attestation / F-broc-001 rotation / F-broc-005 PK vocab sync). **Do NOT set `verification_status` — Step 11, Claude Code.**

### Residual after this session (broccoli)
**All authoring is DONE.** Broccoli's entire prose + compound surface is filled and dual-voiced; the only remaining work is the Claude Code release + Step 9 + Step 11 cert. **The arc is one release-lane pass from broccoli's cert (anchor ~18).**

**Claude Code release note (2026-06-23, session `broccoli_steps6-8`):** _pending apply._
