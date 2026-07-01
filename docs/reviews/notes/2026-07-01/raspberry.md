# raspberry -- PERENNIAL PILOT authoring notes (Claude Code lane, 2026-06-30)

Authored **raspberry** (slug `raspberry`, *Rubus idaeus* red / *R. occidentalis* black) as a
gold-standard PERENNIAL by FILLING its shell, modeled STRUCTURALLY on the certified **blueberry**
(archetype `berries_woody`), refit for CANE biology. READ-ONLY on canonical: `crops_data_final.json`
was never written (git confirms only `tools/berries_woody_gate.py` is modified).

Output: `raspberry_crop.json` (compact, `separators=(",",":")`, `ensure_ascii=False`, no trailing
newline -- byte-identical to a compact re-dump). 92 top-level keys.

## GATE RESULT
`python3 tools/whole_crop_gate.py raspberry <scratch>` -> **GATE: PASS** (exit 0), verified against
BOTH the canonical I read at start (`ed8abc66`) AND the current canonical (`1bc569dc`, see "Canonical
moved" below). Blueberry regression: still PASS (byte-identical path). Also green: `release_verify`
(clean, 2 non-blocking pause-legibility notes), `register_completeness_gate` (0 unruled prose).

### berries_woody gate branches that fired (and passed)
- **A15 berries_woody structural cert** -- the cane-fruit sub-form (lifecycle scalars, chill-gate
  signature `gating_factors=["chill_hours"]` + `chill_hours_required=800`, prose-pair backstop,
  self_fertile, no tree/cross-pollination machinery, per-cell `recommended_type`+`leaf_habit`
  typing, type COVERAGE, leaf_habit<->token placement). **This is the branch that required the gate
  generalization (below).**
- **A16 berries_woody calendar coherence** -- all 20 resolved cells: stored `calendar[]` ==
  `derive_berry_woody_calendar(leaf_habit, bloom, harvest)`. Clean.
- **A21 berries_woody variety-chill presence** -- all 14 varieties carry numeric
  `chill_hours_required` + valid `chill_hours_range`. Clean.
- **A31/A32 coverage floors** -- full 10-region roster, every cell carries a non-empty calendar.
- Plus the universal roster A2-A36, B (dual-voice 221 CP / 26 SP / 0 nulls), C/D (0 dash / 0 temp),
  E (8 sources, all catalogued T1), F (85 claim leaves, 0 anchoring gaps).

## MIRRORED ALL BLUEBERRY PERENNIAL FIELDS -- 0 omitted
Symmetric key-diff vs blueberry = **EMPTY** (raspberry has every one of blueberry's 92 keys, no
extras). The berries_woody perennial field set is all present and refit:
`calendar_basis="berries_woody"`, `archetype="berries_woody"`, `gating_factors=["chill_hours"]`,
`chill_hours_required`/`chill_hours_range`/`chill_hours_note_*`, `bloom_time_*`/`bloom_duration_days`,
`pollination{}`/`self_fertile`/`pollinator_notes_*`, `hardiness_zone_min/max`/`hardiness_notes_*`,
`reliable_fruit_zone_min/max`, **`cane_type` + `cane_management_*`** (the CENTRAL raspberry refit),
`planting_method_notes_*`, `type_selection_*`, `establishment_years`/`establishment_note`,
`years_to_first_harvest`/`years_to_full_production`/`productive_lifespan_years`, `dormancy_window`
(null, as blueberry), `pruning_window` (null, as blueberry), `growth_stages` (9, same ids) +
`growth_stages_year_one`/`growth_stages_annual` (empty, as blueberry), `year_one_notes_*`, `tasks`
(empty), `varieties`/`varieties_detail`, and blueberry's `regions{}`/`resolved_by_zone{}` perennial
calendar structure (10 regions, 20 cells). `soil_prep_*`, `type_selection_*`, and `gating_factors`
were ADDED (the shell lacked them; blueberry carries them).

## KEY RASPBERRY REFITS (blueberry = structure; CANE biology = the big refit)
- **`cane_type="both_summer_and_everbearing"`** (blueberry: `"not_applicable"`). The biennial cane is
  the signature: crown perennial, each cane lives 2 years.
- **`cane_management_*` is now CENTRAL** -- full prose on SUMMER-BEARING (floricane: primocane year 1,
  fruits year 2, then dies; remove spent floricanes + thin to 4-6/ft) vs EVERBEARING/FALL-BEARING
  (primocane: fruits on first-year cane tips, MOW ALL CANES TO THE GROUND each winter for one clean
  fall crop, or double-crop). Both registers.
- **`self_fertile=true`** (blueberry false) -- raspberry is self-fertile, no pollinizer needed.
  `pollination.needs_pollinizer=false`.
- **Bare-root DORMANT canes** (`start_method.start="nursery_transplant"`, planting prose = dormant
  bare-root, late winter/early spring) + **certified virus-free stock** emphasis.
- **Aggressive SUCKERING + TRELLIS** -- containment-to-a-narrow-row and support are recurring themes
  (notifications, growth_stages, tips, cane_management).
- **`years_to_first_harvest=[1,2]`** -- fall-bearing planted in spring fruits THAT fall (year 1);
  summer-bearing fruits year 2. `years_to_full_production=[3,4]`, `productive_lifespan_years=[10,15]`.
- **Very cold-hardy** `hardiness_zone_min=3` (reds to z3-4); **heat-limited** `reliable_fruit_zone=3..8`
  (`hardiness_zone_max=11` only marginally). `chill_hours_required=800`, range `[250,1600]`.
- **Soil/pH refit** -- well-drained loam, pH 5.6-6.5 (NOT blueberry's acid 4.5-5.5); no
  sulfur/azalea/peat/ericaceous content. `fertilizer.npk_ratio="10-10-10"` balanced.
- **Pests** -- SPOTTED-WING DROSOPHILA (high, the major modern pest), raspberry cane borer, raspberry
  crown borer, Japanese beetle, aphids (virus vectors). **Diseases** -- Phytophthora root rot (high),
  anthracnose, cane+spur blight, orange rust (high), raspberry mosaic virus complex (high).
- **Companions** -- light model: bad_seasoned = nightshades+strawberry (Verticillium wilt) and wild
  brambles (virus/SWD reservoir); good = traditional allium edge + legume row-middle (honest
  traditional/likely provenance, low confidence).
- **recommended_type axis (per cell) = the CANE type** {`summer_bearing`, `everbearing`}; cold north
  z3-4 = everbearing (mow-to-ground reliability + fast fall crop), z5-7 = summer-bearing; cool CA
  coast = summer-bearing; hot/low-chill regions = everbearing (Dorman Red / Bababerry, marginal).
  **`leaf_habit="deciduous"` on EVERY cell** (raspberry has no evergreen form, unlike blueberry's
  warm-South evergreen rabbiteye/SHB).

## SOURCES (catalogued + T1 + read live via WebFetch/WebSearch 2026-06-30 -- 8 ids)
`umn_ext` (Minnesota types + home-garden), `cornell_ext` (Fruit Resources / SWD hosts),
`psu_ext` (raspberry production), `ncsu_ext` (SE caneberry guide), `usu_ext` (Utah raspberry
management), `uga_ext` (C766 home-garden raspberries/blackberries -- Dormanred), `tamu_agrilife`
(TX Master Gardener Dormanred), `ucanr_ext` (UC backyard berries). Every cited source is in
`source_catalog` with `tier=T1` (gate E: 0 uncatalogued, 0 non-T1). Each was opened and read
live (not curl/wget). The OSU EC-1306 and a couple of PSU/NCSU URLs 403'd/404'd at fetch and were
NOT used (FLAGGED rather than cited blind).

## THE PILOT FINDING -- the berries_woody gate is blueberry-specific; I generalized it (TDD)
The whole point of the pilot surfaced cleanly: against the UNMODIFIED gate, honest raspberry bounced
with exactly **22 violations**, ALL from two blueberry-specific hardcodes in **A15**
(`tools/berries_woody_gate.py`), plus my own documenting open-finding:
1. `self_fertile must be False` -- but raspberry IS self-fertile (the task specifies `self_fertile=true`).
2. `recommended_type in {northern_highbush, southern_highbush, rabbiteye}` -- blueberry chill classes;
   raspberry's cane types are `summer_bearing`/`everbearing` (20 cells).
Everything else passed first try (calendar coherence, coverage, dual-voice, sourcing, anchoring,
tips, display-readiness). There is NO honest way to pass the unmodified gate (setting
`self_fertile=false` or `recommended_type="rabbiteye"` would be biologically false).

**Resolution (the pilot's tooling deliverable):** I generalized A15 ADDITIVELY into two sub-forms,
keyed on `cane_type`:
- **BUSH** (blueberry, `cane_type="not_applicable"`): UNCHANGED -- self_fertile must be False,
  blueberry chill-class type enum.
- **CANE** (raspberry/blackberry, real `cane_type`): self_fertile must be a bool (True correct),
  type enum `{summer_bearing, everbearing}`.
Every blueberry invariant is preserved (coverage, no-tree-machinery, leaf_habit token placement);
blueberry still passes byte-identically; the whole-dataset berries_woody sweep is 0 violations.

**TDD (RED-before-GREEN, per the hard rule):** RED baseline = raspberry bounced (21 structural).
After the change, 9 adversarial defect classes were sneaked at the gate and ALL caught (>0):
bogus blueberry-type on a cane cell; type typo; non-bool self_fertile on cane; self_fertile=True on a
BUSH (blueberry, still bounces); cross-pollination machinery on a cane variety; evergreen+dormant token
mismatch; deciduous-missing-dormant; everbearing-variety-removed coverage break; rootstock machinery.
Baseline raspberry + blueberry = 0.

**ACTION REQUIRED (Trevor):** `tools/berries_woody_gate.py` is modified in the working tree,
UNCOMMITTED. It needs your TDD sign-off before any commit. Do NOT trust it until reviewed. (CC lane
writes gates, but the armor change is yours to approve.)

## MODELING DECISIONS / FLAGS (carried as open_findings on the record, all non-blocking)
1. **Deriver prune-placement for fall-bearing** -- the shared `berry_woody_calendar` deriver (A16)
   places the dormant `prune` token the month before bloom. That fits spring/summer-blooming cells,
   but for the cold-north fall-bearing cells (`northern_tier` z3/z4) the real management is a
   late-winter MOW-to-the-ground, so the derived prune month reads ~1-2 months later than the actual
   cut. Calendars are stored as derived (A16 requires it); `cane_management` prose carries the
   accurate timing. A deriver refinement for the primocane fall-bearing shape is a future tooling item.
2. **Hot-region marginality** -- A32/coverage forces a calendar on every cell, but raspberries are
   genuinely marginal-to-unsuitable in `ca_desert`, `low_desert_az`, `fl_peninsula` (z10/z11),
   `hawaii_tropical` (z11). Those cells carry best-effort low-chill/heat-tolerant (Dorman Red /
   Bababerry) windows with STRONG marginality language in the prose ("essentially unsuitable",
   "treat as an experiment"). Unlike blueberry (rabbiteye/SHB for the South), raspberry has no good
   warm-climate type -- this is honest biology, not a fudge.
3. **release_verify pause-legibility notes (2, NON-blocking)** -- `ca_north_coast.z10` and
   `ca_south_coast.z10` (nearly frost-free) show 4-5 `dormant` months, which release_verify flags for
   a human glance ("legit gap vs cold/heat_pause?"). The dormancy is biologically real (raspberries
   are deciduous everywhere, dormant in winter regardless of frost), a direct consequence of the
   correct "deciduous on every cell" modeling. Benign; release_verify verdict is CLEAN.

## VERIFICATION POSTURE
`verification_status.status="author_fresh_pilot"`, `launch_ready_core=false`,
`launch_ready_seasoned=false` (a DRAFT, not a cert). 3 open_findings (all non-blocking; the
gate-generalization finding was set non-blocking once the gate was generalized).

## CANONICAL MOVED MID-SESSION (external, not me)
At session start the canonical was `ed8abc66` (22 certified + 28 drafts). Mid-session it advanced via
EXTERNAL concurrent commits to `1bc569dc` ("bok-choy -> ALL 50 CERTIFIED"). I never wrote
`crops_data_final.json` (git confirms). Blueberry (my template) is structurally unchanged (92 keys,
berries_woody) and the raspberry shell is still unfilled in canonical. I re-spliced + re-gated against
the CURRENT canonical: raspberry GATE: PASS, key-isomorphic to current blueberry, blueberry regression
clean. Promoting raspberry into canonical is a separate authoring/promote task (Trevor-gated); this
deliverable is the authored record + the gate generalization, in scratch.

## SCRATCH ARTIFACTS
- `raspberry_crop.json` -- the deliverable (compact).
- `raspberry_NOTES.md` -- this file.
- `build_raspberry*.py` (parts 1-4), `_rasp_*.json` (intermediate), `scratch_canon.json` (current
  canonical with raspberry spliced, for gating), `bb_scaffold.json`, `blueberry_full.json`,
  `raspberry_shell.json` -- working files.
