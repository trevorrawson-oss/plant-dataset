# Berry Variety Pilot (strawberry) -- Design Spec (the BERRY bearing-habit archetype)

**Status:** design, approved 2026-07-15 (Trevor).
**Arc:** the 5th variety archetype after annual_dtm (dry-bean), tree_fruit (apple),
photoperiod_annual (onion), hardiness_annual (leek). Field-addition register row 18.
**Pilot crop:** `strawberry` only (single-crop, the established pilot discipline).
**Base canonical:** `8dd4ac4c` (re-stamp `base_sha` from the live canonical at build time; the
SHA-guarded splice fails closed on drift).

---

## 1. Context and goal

Berries are the last big variety-archetype gap. The full roster maps into five archetype buckets:
`annual_dtm` / `tree_fruit` / `photoperiod_annual` / `hardiness_annual` (all piloted) plus **berry**
(strawberry, raspberry, blackberry, blueberry, elderberry -- 57 varieties, unpiloted). Their variety
content already exists in the legacy shape; the arc is a shape migration + T1 sourcing, not greenfield.

This pilot designs the `berry` archetype and proves it on **strawberry** (9 varieties). The `berry`
schema is designed to GENERALIZE to the cane/bush groups (which carry chill + their own habit vocab),
exactly as apple's `tree_fruit` was built to cover every deciduous tree -- but only the strawberry
slice is populated + validated here; the cane/bush branches are designed, adversarially RED-tested,
and RESERVED (0 live members), like `photoperiod_capped` / `multisow_clump` were.

**Why strawberry is isolated as its own pass (Trevor):** strawberry is the one berry whose LIFECYCLE
is region-dependent -- a herbaceous perennial in cold/temperate zones, but grown as a replanted ANNUAL
in warm regions (Southeast plasticulture). Bearing-habit is the variety datapoint regardless of
lifecycle, and variety CHOICE interacts with the annual system (short-day southern types like
Chandler / Camarosa suit plasticulture; June-bearers suit matted-row perennial). The perennial-vs-annual
lifecycle itself stays a crop/region concern, NOT variety schema; the variety records the habit and,
where relevant, an optional `regional_fit` note.

## 2. The honest framing (the accuracy crux)

The load-bearing per-variety fact for a berry is its **bearing habit / cultivar group** -- the thing
that decides how and when it fruits and, for the woody berries, whether it will fruit in a given
climate at all. For strawberry the three habits are genuinely different products:

- **june_bearing** -- one concentrated early-summer flush (the matted-row backbone of US backyard
  growing).
- **day_neutral** -- fruits through the season, compact, container-friendly.
- **everbearing** -- two lighter flushes.

This is exactly the choice a grower makes ("one big batch for jam" vs "a few berries all summer"), so
it must be a first-class, validated field, not buried in prose. Strawberry carries no chill requirement
(unlike the cane/bush groups), so the archetype's chill field is a cane/bush concern, absent for
strawberry.

## 3. Governing principles (the contract -- inherited)

Inherited verbatim from the variety-detail contract (register #12; dry-bean/apple/onion/leek):

- **3.1 Flat, sparse override-by-ABSENCE.** A variety records a field only where meaningful; no
  `delta{value,parent,changed}` overlay.
- **3.2 Source-authoritative, T1-or-it-does-not-ship.** A T1 source is the authority; per-variety
  `sources` are T1-ONLY so cert gate E (source-tier) stays green. Honesty about weaker data lives in
  `confidence_tier` + prose, never a fabricated citation.
- **3.3 Common core + dispatched archetype block.** A crop declares `variety_archetype`; the gate
  selects the required trait/enum block. Absence still defaults to `annual_dtm` (dry-bean untouched).
- **3.4 Season-only, no DTM.** Strawberry's crop `days_to_maturity` is `[]`, so berry varieties carry
  NO `days_to_maturity` (the `dtm_empty` season-only predicate, shared with tree_fruit).
- **3.5 Soft-gate lifecycle.** The berry checks ship SOFT/standalone in `variety_detail_gate`, NOT
  wired into `whole_crop_gate` / A39. The hard-flip (INV-1) remains the Spec-2 roster-rollout trigger.

## 4. The `berry` archetype + `berry_group` discriminator (new)

- New `variety_archetype: "berry"` added to the dispatch (a 5th archetype).
- New crop-level `berry_group ∈ {strawberry, cane, bush}` -- the real-world axis that decides both the
  valid `bearing_habit` vocabulary and whether chill applies. Strawberry declares `berry_group:
  "strawberry"`.
- The gate's berry block **sub-dispatches on `berry_group`**:
  - `strawberry` -> `bearing_habit ∈ {june_bearing, everbearing, day_neutral}`; NO chill.
  - `cane` -> `bearing_habit ∈ {summer_bearing, fall_bearing}` + `chill_hours_required` (RESERVED).
  - `bush` -> `bearing_habit ∈ {northern_highbush, southern_highbush, rabbiteye, half_high}` +
    `chill_hours_required` (RESERVED).

One `berry` archetype models the family as one thing (which it biologically is) and keeps the
top-level dispatch at 5 entries; the group sub-key carries the within-family variation.

## 5. Per-variety schema (common core + `berry` block)

### 5.1 Universal common core (with one addition -- see §7)
`id` (stable slug), `name`, `maturity_class ∈ {early, mid, late}`, `confidence_tier ∈ {T1..T4}`,
`is_reference` (exactly one true per crop), `hero_description` (NEW, §7), `note_beginner`,
`note_seasoned`, `sources` (T1-only), `anchoring_urls`.

**`maturity_class` = ripening ONSET season.** This resolves the continuous-bearer wrinkle: a
day_neutral / everbearing strawberry has no single ripening class, so `maturity_class` records when
fruiting BEGINS (its onset), while `bearing_habit` already carries the continuous-vs-flush truth. Every
variety therefore has a well-defined `maturity_class`.

### 5.2 The `berry` block (strawberry slice populated)
- `bearing_habit` -- LOAD-BEARING, group-dispatched enum (strawberry values above).
- `use` -- required free string (e.g. "fresh, freezing, jam"), matches the tree/onion/leek `use`.
- `regional_fit` -- OPTIONAL prose, carries the annual/plasticulture suitability nuance where relevant
  (short-day southern types for warm-region annual systems). Absent where not meaningful.
- NO `days_to_maturity` (season-only), NO chill for strawberry.

### 5.3 Reserved cane/bush (designed, not populated)
`chill_hours_required` (positive int) is a cane/bush field; the gate validates it when
`berry_group ∈ {cane, bush}` and REJECTS it (or a cane/bush `bearing_habit`) appearing under
`berry_group: "strawberry"`. Zero live cane/bush members in this pilot; the branches exist to be
RED-tested so the archetype is proven end-to-end.

## 6. The gate (shape-only)

Extend `tools/variety_detail_gate.py` with a `berry` trait/enum block + a `_berry_checks(slug, nm, x,
group)` helper (mirrors `_tree_checks` / `_hardiness_checks`), dispatched by `berry_group`.

- **SHAPE-ONLY: no standalone honesty engine this pilot.** Strawberry has no chill, so the
  chill-vs-region honesty axis does not apply; it becomes relevant only when cane/bush land and will
  fold into the existing `chill_gate` then. This mirrors onion (reused the existing engine) rather than
  leek (built one). Explicitly OUT of scope here.
- VIOLATIONS (in-scope crops only): common-core presence incl. `hero_description`; `bearing_habit`
  membership in the group's enum; `maturity_class`/`confidence_tier` enums; exactly-one `is_reference`;
  slug-shaped + unique `id`; a cane/bush value under `berry_group: strawberry` bounces.
- **TDD, RED-before-GREEN, adversarially proven** on a SCRATCH copy of real strawberry (canonical
  READ-ONLY throughout): green baseline, then each defect bounces -- bad `bearing_habit` for the group,
  missing `hero_description`, wrong `maturity_class`, two `is_reference`, dup `id`, a reserved
  cane/bush value on the strawberry crop, `chill_hours_required` present under `berry_group:
  strawberry`.
- Soft/standalone; off-scope crops silent (the un-migrated roster stays green).

## 7. The `hero_description` common-core standard + backfill (bundled)

- New per-variety `hero_description` -- a single-register MARQUEE line (a hook that leads the variety
  card), distinct from and additive to the dual-register `note_beginner`/`note_seasoned` detail. Added
  to the **universal common core**, so it is required on EVERY in-scope variety going forward, not just
  berries (Trevor: "make it normal going forward").
- **Backfill BUNDLED into this arc (Trevor-approved).** The 4 shipped pilots (dry-bean/apple/onion/leek
  = 33 varieties) currently lack it, so this arc authors one `hero_description` marquee line per
  variety for those 33 too, in a paired batch -- exactly like the crop-description fold-in was
  backfilled. This keeps the soft gate green (no crop left non-conforming to the new common-core field)
  and makes the standard real immediately. American English, no em dashes, `°F` where temps appear.

## 8. `register_completeness` ruling

Rule the new string keys `bearing_habit`, `berry_group`, and `hero_description` into
`register_completeness` EXCLUDED_KEYS (path-scoped to `varieties`), TDD like `day_length_type` /
`cold_hardiness_class`. A25 must read 0 unruled on the release battery.

## 9. Sourcing

T1 per-variety for `bearing_habit` + `maturity_class` from extension strawberry guides (Cornell CALS,
UMN Extension, NC State, Ohio State, UMD Extension). Bearing habit is well-documented, so a clean T1
pass is expected; anything thin is honestly recorded in `confidence_tier` + prose, never laundered.
Per-variety `sources` T1-ONLY (cert E.source-tier holds). New source ids added to `source_catalog` only
if genuinely needed; `verification_status.source_set` updated to what is actually cited.

**Flagship (`is_reference`) = one, the "good first choice if unsure":** leaning a widely-adaptable
day_neutral (e.g. Albion) or a classic reliable performer (e.g. Earliglow / Honeoye); settled at
authoring against which is best-sourced + most broadly recommended.

## 10. Rollout (amend-not-recert) + footprint

SHA-guarded COMPACT splice via `tools/apply_patch.py` (`tools/batches/berry_strawberry_pilot.json`
for strawberry + `tools/batches/variety_hero_backfill.json` for the 4-pilot hero backfill, or one
combined batch). Footprint EXACT:
- strawberry: `varieties` + `variety_archetype` + `berry_group` + `verification_status.source_set`.
- hero backfill: `varieties` on dry-bean/apple/onion/leek only (one `hero_description` per variety).
- ALL other crops byte-identical; `source_catalog` touched only if a new source is genuinely added;
  count 125 unchanged; strawberry + the 4 pilots stay certified (116 certified unchanged); COMPACT
  (no trailing newline); 0 escaped unicode.

## 11. Field-addition register entry

Row 18: the `berry` archetype (bearing-habit) + the `hero_description` common-core standard. HARD-FLIP
(INV-1): fold the berry-block checks into the A39 register-coverage hard floor + `gate_all` when the
Spec-2 rollout column pass reaches full-roster coverage. Soft is a stage, not a resting state.

## 12. Scope boundaries (explicitly OUT)

- Cane/bush POPULATION (raspberry/blackberry/blueberry/elderberry) -- designed + reserved here, authored
  in the fast-follow.
- Any standalone berry honesty engine / chill-vs-region viability gate (a cane/bush-era concern).
- Strawberry's perennial-vs-annual LIFECYCLE model (a crop/region concern, not variety schema).
- The A39 hard-flip (INV-1, Spec-2).
- plant-astro/plant-app consumption (INV-2: do not consume variety `bearing_habit` as load-bearing
  until the crop is gate-clean).

## 13. Success criteria

- `strawberry` carries `variety_archetype: "berry"` + `berry_group: "strawberry"` + 9 varieties on the
  flat berry schema, each with `bearing_habit`, `maturity_class` (onset), `use`, `hero_description`,
  dual-register notes, T1 `sources`; exactly one `is_reference`.
- `hero_description` present on all 9 strawberry varieties AND backfilled onto all 33 varieties of the
  4 prior pilots.
- `variety_detail_gate` strawberry 0 viol / 0 warn (berry in scope, 5 archetypes); the recorded
  adversarial RED proof bounces every injected defect class incl. the reserved cane/bush branches.
- `whole_crop_gate` strawberry PASS; `gate_all` 116/116; `register_completeness` A25 = 0 unruled;
  `release_verify` clean (0 em dashes in any user-facing string, incl. every new `hero_description`).
- Footprint audit: exactly strawberry (+ the 4-pilot hero backfill); all other crops byte-identical;
  count 125; compact.

## 14. Open items to confirm during authoring

- Final `is_reference` flagship choice (day_neutral Albion vs a classic June-bearer) -- pick the
  best-sourced, most broadly recommended.
- Exact `hero_description` voice length target (a single crisp marquee line; keep it a hook, not a
  restatement of the note).
- Whether any strawberry variety genuinely warrants a `regional_fit` note (short-day southern/annual
  types) vs leaving it absent.
- Field name confirmation: `hero_description` (self-documenting) vs a shorter `hero`.
