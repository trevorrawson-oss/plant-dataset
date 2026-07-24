# Asparagus Gold-Standard Arc -- the `herbaceous_perennial` Archetype (Design-First)

**Date:** 2026-07-23
**Base canonical:** `ccf5e890` (origin/main `7923579`, after the variety-resistance pilot + ladybug sweep; local synced via `git pull --ff-only`)
**Scope of THIS arc:** DESIGN-FIRST. Mint + TDD-gate the `herbaceous_perennial` archetype and land a
staged, newest-standard reference asparagus that proves the shape end to end. **Stop before** the full
16-region / full-field authoring + certification, which becomes a separate follow-on arc.

---

## 1. Problem & context

Asparagus is one of the 9 honest shells (empty `days_to_maturity`, null `sunlight`, empty `varieties`,
`verification_status` all false/null). It is an **herbaceous perennial vegetable**: crowns planted once,
a 2--3 year establishment lag before first harvest, then a spring spear-harvest window (6--8 weeks)
followed by ferning-out, fall dieback, and winter dormancy, over a 15--20 year bed life. It fits none of
the existing archetypes cleanly -- not a culinary herb, not a flower, not a berry, not a tree.

The roadmap (`docs/kickoffs/07-remaining-gs-anchors.md`) flags artichoke + asparagus as the
"herbaceous-perennial crop archetype -- design-then-author" case, and Trevor **ratified the name
`herbaceous_perennial`** on 2026-07-05 (roadmap ruling #2). This arc is the design half of that: it
delivers the archetype + its armor, piloted on asparagus, so the follow-on arc (and later artichoke)
authors against a proven, gated template instead of inventing as it goes.

### Load-bearing facts established during brainstorming

- **A herbaceous perennial certifies cleanly on `calendar_basis = frost_anchored`.** `A3`
  (`perennial_cert_violations`) hard-returns `[]` for any basis not in `PERENNIAL_BASES`, and
  `frost_anchored` is not one -- so asparagus never triggers tree invariants (chill/bloom). **Proof by
  precedent:** chives, mint, lemongrass, bee-balm, echinacea are all `perennial:true` + `frost_anchored`
  + certified (`verification_status.status == "verified_gs_arc"`).
- **The 16-region roster is a HARD cert floor**, not optional. `A31` requires
  `CANONICAL_REGIONS = set(zone_span_gate.EXPECTED_SPANS)`; certified crops (chives, strawberry) already
  carry all 16 including the six new authored regions (rgv/pnw/mid_atlantic/mid_south/nevada/utah_dixie).
  Asparagus's shell has only the old 10, all empty. Certification therefore requires authoring **all 16**
  region cells -- deferred to the authoring arc, but the archetype must define how they behave.
- **The new IPM `control_ladder` is NOT yet a hard cert requirement** -- its `A39` hard-flip was deferred
  to the roster-wide rollout (~897 problems). So asparagus *could* certify on the legacy `pests`/`diseases`
  shape. Per Trevor's "author to newest standards now" call, the reference nonetheless demonstrates the
  ladder shape so the follow-on arc has no retrofit.
- **Next free structural-gate number is `A46`** (A45 is the current max; SE-Alaska's reserved A46/A47 were
  spec'd but never built, so those numbers are free).

### Decisions ruled by Trevor (2026-07-23 brainstorm)

1. **Scope = design-first**, author + certify later.
2. **Depth = design to the newest-standard bar** (the reference includes a `control_ladder` and a
   variety-resistance `resists:` map), even though we stop before cert.
3. **Unsuitable regions = suitability marker + honest calendar** (option A of the fork): reuse the
   existing `suitability` field with a perennial-appropriate vocabulary, keep a minimal honest calendar so
   `A32` stays satisfied, and let the new gate validate the marker's presence + coherence. **No `A32`
   carve-out.**

---

## 2. The archetype: `herbaceous_perennial -> frost_anchored`

- **Register** `"herbaceous_perennial": "frost_anchored"` in `tools/calendar_basis_gate.py::ARCHETYPE_BASIS`.
  `VALID_CALENDAR_BASES` is **unchanged** (`frost_anchored` already valid). This mirrors exactly how
  `warm_season_grass` (sweet-corn) was added: a meaningful new archetype label riding the existing
  frost-anchored calendar machinery, with **no new calendar deriver** and **no new dispatch in the
  A3/A4/A5 calendar layer**.
- **The establishment lifecycle rides the perennial FIELDS, not the calendar.** The per-zone `calendar`
  renders the *established-bed steady state* (dormant -> spring spear harvest -> summer fern -> fall
  dieback), exactly the frost-anchored annual token machinery A5/A24/A28 already validate. The multi-year
  establishment (2--3 yr to first harvest) lives in:
  - `perennial: true`
  - `lifecycle`: **`"perennial"`** (recommended, matching the chives/mint herbaceous lane; the shell
    currently says `"permanent"` -- the gate will accept either, but we standardize on `perennial` for the
    herbaceous lane and reserve `permanent` for woody/tree. Final value confirmed at authoring.)
  - `years_to_first_harvest`, `years_to_full_production`, `productive_lifespan_years`
  - `succession_policy.suitable: false` (+ a `reason_seasoned`: a permanent bed is never succession-planted)
  - `year_one_notes_beginner` / `year_one_notes_seasoned` (the establishment-year deviation from the
    steady-state calendar)
  - `start_method` = crowns (primary) with a seed-start alternative note

**Blast radius:** the archetype label is applied only to crops we explicitly set it on (asparagus in the
reference; later artichoke). The existing herbaceous-perennial *herbs* stay `culinary_herb` /
`companion_and_ornamental_flower` per the 2026-07-05 ruling -- untouched.

---

## 3. The new structural cert gate `A46`

A small TDD gate (`tools/herbaceous_perennial_gate.py`, wired into `whole_crop_gate.py` as `A46` and into
`tools/gate_all.py`), **scoped to `archetype == "herbaceous_perennial"`** (no-op for every other crop, so
zero effect on the 119 certified). It armors the invariants unique to a no-replant perennial vegetable --
the analog of how berries_woody / woody_ornamental / berries_herbaceous each got their own structural gate.

### Invariant contract (the crop must satisfy all)

1. `perennial == true`.
2. `lifecycle in {"perennial", "permanent"}` (a permanent-bed lifecycle, not annual/biennial).
3. `succession_policy.suitable == false` **and** carries a non-null `reason_seasoned` (you do not
   succession-plant a permanent bed).
4. Establishment fields present + sane: `years_to_first_harvest` non-empty with min >= 1;
   `years_to_full_production` non-empty; `productive_lifespan_years` a positive int.
5. No `succession` / `second_planting` planting **tracks** in any region cell (a permanent bed has a
   single establishment planting -- the lighter herbaceous analog of A3's "exactly 1 perennial
   establishment entry" tree rule; herbaceous beds allow a fill/gapping planting so we forbid the
   *succession/second_planting tracks* rather than mandating exactly one entry).
6. **Suitability coherence** (see section 4): every region cell carries a `suitability` value from the
   herbaceous-perennial vocabulary; an `unsuitable`/`marginal` cell's `region_notes_*` states the
   dormancy/chill reason; a `suitable` cell renders a real spear-harvest calendar.
7. `rotation` reflects a permanent/no-rotate bed (present, and not a standard annual rotation cycle).

### RED proof (TDD, before the gate is trusted)

Inject each defect class into a **scratch copy** of the reference asparagus and confirm the gate bounces
it, per the CLAUDE.md hard rule ("a gate isn't done until a defect has been sneaked at it and caught"):

- `perennial: false` on a herbaceous_perennial crop -> bounce
- `lifecycle: "annual"` -> bounce
- `succession_policy.suitable: true` (or null reason) -> bounce
- empty `years_to_first_harvest` / null `productive_lifespan_years` / `years_to_first_harvest` min 0 -> bounce
- a `succession` or `second_planting` planting track injected into a cell -> bounce
- a region cell missing `suitability`, or an `unsuitable` cell with a full thriving calendar + no reason
  note -> bounce
- **negative control:** the clean reference asparagus passes; and a *non*-herbaceous_perennial crop
  carrying any of these shapes is untouched (scope proof).

---

## 4. Suitability convention for chill-dependent regions

Asparagus needs winter dormancy, so of the mandatory 16 regions several are genuine poor fits
(hawaii_tropical, fl_peninsula, low_desert_az, rgv, and the mild-winter edges of the CA coast). The
frost-anchored lane's `A32` requires a **non-empty calendar in every region cell**, and only the
tree/woody perennials use the `suitability` enum today (values `fruits_reliably` / `marginal` /
`unsuitable` / `survives_no_fruit`, which are fruiting-specific and do not fit a spear crop).

**Resolution (Trevor-ruled):** herbaceous_perennial cells **reuse the existing `suitability` field** with a
perennial-vegetable-appropriate vocabulary, and **still carry a minimal honest calendar** so `A32` is
satisfied with no carve-out. Honesty about a poor region lives in the `suitability` value + the
`region_notes_*` prose, not in an empty calendar.

- **Proposed vocabulary** (finalized at authoring): `perennializes` (thrives -- a full spring
  spear-harvest calendar), `marginal` (grows but the dormancy/heat is imperfect -- calendar present,
  notes caveat), `unsuitable` (won't reliably perennialize -- a minimal "if you must, treat as a poor
  annual / grow elsewhere" calendar + an explicit dormancy-reason note).
- `suitability` is an **already-known key** (used by 292+ tree cells) so `register_completeness` /
  `A25` should already rule it; the gate task must **confirm** it is ruled for the frost-anchored
  herbaceous_perennial path and rule it if a novel path surfaces (do not assume).
- `A46` invariant #6 validates the marker's presence + coherence with the calendar/notes.
- The reference proves both ends: `northern_tier` = `perennializes`; `hawaii_tropical` = `unsuitable`.

---

## 5. The reference asparagus (staged, newest-standard bar)

Authored to demonstrate the archetype end to end, then **kept in staging (`tools/staging/`), NOT promoted
into the canonical** -- asparagus stays a shell on `main` until the follow-on cert arc. (CLAUDE.md
READ-ONLY-on-canonical rule: the design-first deliverable is the archetype + gate + a proven template, not
a canonical splice.) Contents:

- **Structural spine:** `archetype`, `calendar_basis`, the perennial fields (section 2), `start_method`
  (crowns + seed alt), `planting_layout` (trench/row -> `A44` shape), core agronomy stubs sufficient to
  exercise the gate (soil/pH/sun/spacing/germination need not be fully T1-authored in the reference; they
  are the authoring arc's job -- the reference authors what the gate + archetype need).
- **Two contrasting region cells** proving the suitability convention:
  - `northern_tier` -- `suitability: perennializes`, a real established-bed spear-harvest calendar
    (dormant -> spring harvest window -> summer fern -> fall dieback), `year_one_notes` for the
    establishment deviation.
  - `hawaii_tropical` -- `suitability: unsuitable`, a minimal honest calendar + a `region_notes_*`
    dormancy-reason caveat.
- **IPM `control_ladder`** for the signature problems, referencing the existing `control_methods` catalog
  (all present): asparagus beetle (`handpick` -> `floating_row_cover` -> `garden_sanitation` [fall fern
  removal, the overwintering site] -> `beneficial_predators` -> `spinosad`/`neem_oil` -> `pyrethroid`
  rescue), rust (`resistant_varieties` -> `airflow_spacing` -> `garden_sanitation` -> `sulfur`). Stable
  kebab problem `id` + `type`, monotonic-tier, applies_to-coherent -- validated by the existing
  `control_ladder_gate`. Add asparagus-specific catalog methods only if a rung has no existing home
  (e.g. a "no-replant-in-old-beds / well-drained site" cultural method for Fusarium) -- authored from a
  fetched T1 source, never broadened on an unsupported claim.
- **Varieties** to the common-core standard: `varieties.recommended` with `hero_description`s (REQUIRED on
  all variety work since the berry pilot) -- all-male hybrids (Millennium, Jersey Knight/Giant, Guelph
  Millennium), an open-pollinated heirloom (Mary/Martha Washington), and a purple (Sweet Purple / Purple
  Passion). Plus a **variety-resistance `resists:` map** on an all-male hybrid (e.g. Millennium ->
  rust / Fusarium, referencing the reference ladder's problem `id`s), proving the archetype accommodates
  the just-shipped variety-resistance standard.

---

## 6. Variety approach (this pilot vs. later)

- **This pilot:** the light path -- `varieties.recommended` + `hero_description` + a `resists:` map.
  This satisfies the common-core standard and demonstrates the newest resistance standard.
- **Deferred (documented, not built here):** a dedicated **sex-ratio / dioecious variety archetype**. The
  genuinely differentiating asparagus variety axis is sex (all-male F1 hybrids out-yield OP dioecious
  lines because males spend nothing on seed) and color (green vs. purple; white is a blanching technique,
  not a cultivar). Per the shallot-held lesson, build a per-variety schema only once the authoring arc
  confirms the datapoint is differentiating **and** T1-sourceable at variety granularity -- for all-male
  yield/resistance it likely is, so this is a probable follow-on variety arc, but it is out of scope for
  the archetype pilot.

---

## 7. Explicitly deferred to the follow-on authoring + cert arc

- Full T1 agronomy fan-out (soil texture/drainage/OM, pH range + prose, sun, water/watering schedule,
  spacing, germination temp, growth_stages + tips_by_stage, harvest_ready dual-register + sources,
  storage, fertilizer/NPK, descriptions, hardiness notes, failure_diagnostics, container_notes, recipes,
  tasks, notifications, weather_triggers, moon_phase, companions).
- **All 16 region cells** (the reference does 2), with zone tuning (asparagus realistically z3--8
  plantable; z9--11 marginal/unsuitable) and per-region frost-anchored calendars + suitability markers.
- Full `pests` / `diseases` coverage and the complete `control_ladder` set.
- Register-field completion (#4--#7) to satisfy `A39`/`A40`/`A41`/`A42` at cert.
- The full release gauntlet: `whole_crop_gate` all-A on asparagus + `gate_all` (roster -> **120/120**) +
  `release_verify` + the per-batch source-truth sample; the state trio; a field-addition register row.
- Then **artichoke** on the same archetype (fast follow), which also settles the sibling shell.

---

## 8. Verification plan (this session's deliverable)

- `A46` RED battery green (every defect class in section 3 bounces on the real reference shape; clean
  reference passes; scope negative-control passes).
- `gate_all` stays **119/119** -- the archetype registration + new gate must not perturb any certified
  crop (asparagus is not promoted, so it is not in the certified roster; the reference is exercised via a
  standalone/scratch run).
- The reference asparagus passes `control_ladder_gate` (ladder shape) and `variety_resistance_gate`
  (resistance-map shape) on a scratch run.
- Footprint discipline: canonical `crops_data_final.json` **untouched** (asparagus stays a shell);
  changes limited to new tooling (`herbaceous_perennial_gate.py` + test, the one-line `ARCHETYPE_BASIS`
  add, `whole_crop_gate`/`gate_all` wiring) + staged reference files + this spec/plan.

---

## 9. Risks & open items

- **`suitability` vocabulary + rule.** Confirm `suitability` is already ruled by `register_completeness`
  on the frost-anchored path before relying on it; finalize the `perennializes`/`marginal`/`unsuitable`
  vocab and check no existing gate assumes the tree-only `fruits_reliably` set. (Mitigation: a scratch
  `whole_crop_gate` run on the reference surfaces any unruled-key halt.)
- **`lifecycle` value** (`perennial` vs the shell's `permanent`) -- ruled `perennial` here; confirm the
  gate + any `A20`/display logic accept it for a frost-anchored crop.
- **Reference honesty on `hawaii_tropical`.** The "if you must" minimal calendar must not read as a
  genuine recommendation -- the `suitability: unsuitable` + notes must dominate. Content-review the two
  reference cells.
- **A46 vs. A32 interaction.** We deliberately avoid an A32 carve-out (Trevor's ruling); verify the
  minimal honest calendar in an `unsuitable` cell actually satisfies A32 (non-empty calendar) so the two
  gates are consistent.
- **Concurrency.** No region/variety arc is expected to run concurrently; if one starts, the archetype
  touches tooling + a staged shell only (path-disjoint from `regions.<slug>` / `varieties.*` splices).

---

## Appendix: precedent evidence

- Certified `perennial:true` + `frost_anchored` crops: chives, mint, lemongrass, bee-balm, echinacea
  (`verified_gs_arc`).
- `ARCHETYPE_BASIS` new-label-on-frost_anchored precedent: `warm_season_grass` (sweet-corn, kickoff #21).
- Per-archetype structural gates: A10/A11 (berries_herbaceous = strawberry), A13/A14 (woody_ornamental),
  A15/A16 (berries_woody) -- the pattern A46 follows.
- Region floor: `coverage_floor_gate.CANONICAL_REGIONS = set(zone_span_gate.EXPECTED_SPANS)` (16).
- Ladder standard: top-level `control_methods` (37 methods) + per-problem `control_ladder` +
  `control_ladder_gate`; variety-resistance: `variety_resistance_gate` + per-variety `resists:` map
  (both shipped in base `ccf5e890`).
