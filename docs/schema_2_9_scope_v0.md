# Schema 2.9 -- Scope / Design-Lock Plan (v0 DRAFT)

**Status:** v0.1 DRAFT. Incorporates Trevor's product decisions (2026-06-10): structured rootstock w/ choose-by delineators, variety-level bloom-overlap calendar (per the `apple-zone-6.html` sample), app-ready by-stage watering/drip, and level + how-often + how-much vocab. NOT ratified. No dataset write until ratified + migration spec'd. Remaining open items are engineering defaults (Section 7).
**Lane:** Claude Code (structural shape design + deterministic migration + gates). claude.ai authors the per-crop BIOLOGY into the shape LATER, during each perennial/tree anchor arc -- NOT here.
**Roadmap:** this is Milestone 18 ("Schema perennial extension"), the structural design-lock gated BEFORE the first perennial/tree anchor. Carrot (M17) was the gate and is now CERTIFIED, so this is unblocked. The roadmap leaves the version label open ("2.8, 2.9, or a sub-point, pinned when the session opens"); this doc proposes **2.9**.
**Base:** schema_version `2.8`, canonical SHA `b34bd6fc` (2026-06-10).
**Designs against / siblings:** `region_primary_schema_shape_spec_v1_0`, `second_planting_structure_spec_v1_1`, `schema_2_7_specification_v1_0`, `heat_anchor_proposal_v0` (the v0-proposal-then-ratify precedent).

---

## 0. What 2.9 is, and what it is NOT

**2.9 bundles three threads into one structural bump** (one design-lock, one migration, so we touch the 123-crop file once):

- **Thread A -- Perennial / tree extension.** Formalize the partial perennial surface that ALREADY exists in the dataset (scaffolded null), complete it with the missing fields, and add the relationship modeling (pollination partners, region lifecycle override).
- **Thread B -- Containers, watering, and irrigation/drip.** The areas flagged weak. `container_notes` is already rich; `watering` is thin; irrigation/drip has zero structured surface.
- **Thread C -- Normalization sweeps.** The structural-debt items parked under "2.9" across the carrot arc.

**2.9 does NOT:**
- Author any biology values (chill hours for apple, bloom windows for peach, drip schedules). Those are per-crop, authored by claude.ai during each anchor arc. 2.9 builds the empty, gated shape only.
- Flip any crop or change any consumer copy.
- Touch the 4 certified anchors' content (cherry/beefsteak/carrot/lettuce stay byte-identical except where a normalization sweep is universal and additive).

**Migration discipline (same flavor as 2.7.5):** additive, null-scaffolded, no-retrofit. New fields land present-but-null on the archetypes that carry them, absent on those that do not. A green `whole_crop_gate` after migration means the SHAPE is correct, never that biology is filled.

---

## 1. Current state (what the probe found, 2026-06-10)

The dataset is NOT a blank slate for perennials. A partial surface was scaffolded in an earlier pass and never populated or spec'd:

**Already present (all NULL), on 26 woody-perennial crops** (deciduous_fruit_tree 14 + evergreen_fruit_tree 7 + berries_woody 4 + 1):
- Top-level: `chill_hours_required` (scalar), `chill_hours_range` (list), `chill_hours_note_seasoned`/`_beginner`, `bloom_time_seasoned`/`_beginner`, `bloom_duration_days`, `pollinator_notes_seasoned`/`_beginner`.
- `tips_by_stage` perennial stages: `dormancy`, `dormant_prune`, `establishment` (on ~25-32 crops).

**Crop population (123 total):** lifecycle = annual 79 / permanent 26 / perennial 13 / biennial 5; `perennial:true` on 38. Archetypes: deciduous_fruit_tree 14, evergreen_fruit_tree 7, berries_woody 4, berries_herbaceous 1, culinary_herb 11, plus the annual/flower/mushroom set. Perennial categories: Stone Fruit 6, Citrus 5, Berries & Shrubs 4, Fig & Subtropical 4, Pome Fruit 3, Herbs 7, etc. Tree/woody slugs include peach, apple, lemon, plum, apricot, pear-european/asian, lime, orange-navel, fig, pomegranate, persimmon, avocado, blueberry, raspberry, blackberry, elderberry.

**`container_notes` (already ~20 fields):** container_ok, container_recommended, depth_inches_min, min_pot_gallons, recommended_pot_gallons, drainage, soil_mix, overwintering, watering_adjustment_*, fertilizer_adjustment_*, shape_requirements_*, container_specific_pests, container_suitable_varieties, notes_*, sources, anchoring_urls. **Structurally rich already.**

**`watering` (thin):** frequency_*, amount_*, method_*, signs_overwater_*, signs_underwater_*, anchoring_urls. No system/method modeling, no by-stage needs, no drought tolerance.

**Irrigation/drip:** ZERO structured fields. "drip" appears 10x, "irrigation" 16x, "soaker" 6x -- all buried in free prose, none queryable.

**Implication:** Thread A is "formalize + complete + populate-later," NOT "invent." Thread B-watering and B-drip are the genuinely new design. Thread B-containers is mostly already shaped (gap-fill only).

---

## 2. Thread A -- Perennial / tree extension

### A1. Formalize the existing surface
Lock the shapes already scaffolded (so they stop being undocumented null):
- `chill_hours_required` (int, null where N/A), `chill_hours_range` (`[low, high]` ints), `chill_hours_note_seasoned`/`_beginner` (prose; the dual-register explainer Trevor flagged we are weak on).
- `bloom_time_seasoned`/`_beginner` (prose), `bloom_duration_days` (int). (The `bloom` calendar-state already exists per cell; this is the crop-level descriptor.)
- `pollinator_notes_seasoned`/`_beginner` (prose).

### A2. Add the missing perennial fields (roadmap list not yet present)
- **`rootstock`** (DECIDED structured -- Trevor 2026-06-10): a `recommended_rootstock` (string) PLUS a `rootstock_options[]` so the user can CHOOSE by rootstock. Each option carries the delineators that actually drive the choice (from Trevor's clementine-dwarf nursery experience -- he needed to know how tall it grows, what pot, and what to ask the nursery for):
  `{name, size_class: dwarf|semi_dwarf|standard, mature_height_ft, spread_ft, container_suitable: bool, container_size_gallons, bearing_age_years, what_to_ask_nursery, traits_seasoned, traits_beginner, sources, anchoring_urls}`.
  `mature_height_ft` + `container_size_gallons` + `what_to_ask_nursery` are the three that made his decision. `traits_*` carries the size-control / disease-and-soil-tolerance / anchorage delineators in dual register. (Apple's variety chooser in the sample is the precedent for a "choose your X" rail.)
- **`dormancy_window`** + **`pruning_window`** -- STRUCTURED windows (offset_from / month band), distinct from the `tips_by_stage.dormancy`/`dormant_prune` PROSE stages, so the calendar/notifier can fire on them. (Mirrors how `plantings[]` is the rule layer behind the calendar.)
- **`cane_management`** -- for brambles (raspberry/blackberry/elderberry): floricane-vs-primocane, cut-back regime. Prose dual-register + an optional `cane_type` enum.
- **`renovation`** -- for matted-row perennials (strawberry): post-harvest renovation practice. Prose dual-register.
- **`establishment_years`** -- int (years to first real harvest / bearing age). Distinct from the `tips_by_stage.establishment` prose stage.
- **`pollination`** -- the relationship model (A4 below).

### A3. Field-applicability (sub-typing decision) -- *Open decision A-2*
The existing surface is **flat: present-but-null on applicable archetypes, absent on others** (chill fields on 26 woody crops, not on annuals). **Recommendation: keep flat, gated by archetype**, NOT a nested `perennial:{...}` sub-object. Rationale: matches what is already deployed (no retrofit of the 26 crops); the renderer branches on archetype/lifecycle it already reads; avoids a breaking nest. Document a **field-applicability matrix** (Section 5) so the migration knows which group each archetype carries. (Sub-typed groups are the alternative; cleaner namespacing but a breaking move on already-scaffolded crops.)

### A4. Pollination + bloom-overlap calendar -- DECIDED (Trevor 2026-06-10): variety-level bloom calendar
Trevor wants the cross-pollination feature his apple sample already mocks up (`04-guides/apple-zone-6.html`, "Bloom timing & cross-pollination", line ~510): a per-VARIETY bloom Gantt where each variety is a bar on a `very_early -> very_late` scale (bar width = bloom duration 6-14 days), and **overlapping bars = compatible pollinizers**. His Pink Lady case: you must buy a second apple that blooms at the same time, or it never sets fruit. So the model is VARIETY-level, not just crop-level.

**Crop-level `pollination`:**
```
"pollination": {
  "self_fertile": true|false|"partial",
  "needs_pollinizer": true|false,
  "pollinizer_distance_ft": 50,
  "notes_seasoned": "...", "notes_beginner": "..."
}
```
(apple: self_fertile=false, needs_pollinizer=true, distance=50.)

**Variety-level bloom (on a structured `varieties.recommended[]` -- the apple-mock way, NO full-expansion dependency):**
```
"bloom_group": "very_early|early|mid|late|very_late",
"bloom_window_relative": [start, end],   // 0-1 on the season scale -> drives the bar left/width
"bloom_duration_days": 6-14,
"chill_hours_required": int               // chill is ALSO per-variety (apple 200-1,200)
```
The sample renders exactly this: `bloom_group` -> color band, `bloom_window_relative` -> bar position. **Chill hours are variety-level** (the sample shows per-variety values + a crop-level `chill_hours_range` spread), so chill lives on the variety record too.

**Region resolution:** bloom GROUP / relative-position is variety-intrinsic (bloom ORDER is stable across regions); the ABSOLUTE bloom dates (the sample's "Apr 10-20") shift by region and resolve in the region layer, same pattern as `resolved_by_zone` calendars. 2.9 defines the relative shape; absolute-date resolution lands when region bloom anchors are populated.

**No Phase 5 dependency (Trevor's concern, resolved 2026-06-10):** the apple sample did this with ~13 RECOMMENDED varieties + their bloom data, not the full varietal catalog. So 2.9 upgrades `varieties.recommended` from a plain string list into a structured object list:
```
"recommended": [
  {"name": "Honeycrisp", "bloom_group": "mid", "bloom_window_relative": [0.40,0.55],
   "bloom_duration_days": 9, "chill_hours_required": 800, "recommended_note": "..."},
  ...
]
```
Each tree anchor authors its curated recommended set (the 8-13 the sample shows) and the bloom calendar runs on THAT -- it does NOT wait for the ~800-varietal Phase 5 expansion (which later adds the non-recommended long tail). The crop-level `pollination` block populates immediately. **Migration:** upgrade existing string `recommended` lists -> objects dataset-wide (deterministic: `"Nantes types..."` -> `{name, recommended_note}`); tree crops add the bloom fields, non-tree crops just carry `{name, recommended_note}`. Cross-references [[variety_chip_selector_pattern]] + the tree-blossom-calendar note.

### A4b. Crop-base + variety-delta architecture (the model the apple mock already uses)
**The crop is the entity, the guide, and the URL; a variety is a DELTA OVERLAY, never a top-level entity.** You land on "apple" (shared sections + crop defaults + the recommended-variety bloom calendar + pollination rule + rootstock options). A chip selector overlays a chosen variety's delta. Apple stays "apple"; Fuji is a VIEW of apple, not a sibling crop.

The mock's variety record is the canonical shape -- a variety carries only divergent fields, each as `{value, parent, changed}`:
```
"recommended": [{
  "name": "Honeycrisp", "subtitle": "...", "use": "fresh eating", "difficulty": "medium",
  "notes_seasoned": "...", "recommended_note": "...",
  "bloom_group": "mid", "chill_hours_required": 1000,        // machine values -> calendar
  "bloom_window_relative": [0.40,0.55], "bloom_duration_days": 9,
  "delta": {                                                  // what differs from the crop base
    "chill":   {"value":"1,000 hrs", "parent":"varies",  "changed": false},
    "harvest": {"value":"Sep early-mid", "parent":"Jul-Oct", "changed": false},
    "zone":    {"value":"4a-7a reliable", "parent":"3b-9a", "changed": true}
  }
}]
```
**Divergence-weighted, same architecture for every crop:** carrot's varieties diverge LIGHTLY (root shape, soil-depth fit, DTM) -> a thin delta, varieties optional ("grow a carrot" is fine). Apple's diverge HEAVILY and the divergence DRIVES THE PURCHASE (bloom for pollination, chill for climate, flavor/use, disease resistance) -> a rich delta, variety selection near-mandatory ("you buy a Fuji on M9, not an apple tree"). The schema does not force either; each crop's varieties carry their real deltas.

**This is largely a SEASONED surface** (reinforces Trevor's "more depth for seasoned" goal): the beginner sees the ONE recommended variety + its plain note; the seasoned gardener gets the full variety-delta comparison (chill/bloom/disease/storage across varieties) -- the stuff that actually drives a seasoned buyer. So the variety drill-down deepens seasoned without touching the beginner default.

**Open routing question (Trevor):** whether each variety also gets its own URL (`/guides/apple/fuji`, SEO + deep-link, delta pre-selected) or stays an on-page chip overlay only. The mock carries `data-slug`/`data-url` on varieties, anticipating per-variety routes. Decision pending; it adds a `slug` to the variety record if yes.

### A4c. Information hierarchy -- why the soil-page layout scales to varieties (Trevor 2026-06-10)
Trevor's concern: a soil type is a small card, a variety carries far more -- does the pattern hold? It does, because content lives at THREE tiers and no single tier is heavy:
- **Universal education (reference pages, the `/guides/soil` + `/guides/ph` model):** the heavy *conceptual* content -- how chill hours work, how cross-pollination works, how to prune a fruit tree. Authored ONCE, dual-register, T1-cited, shared by every crop/variety, never repeated. New universal reference pages this enables: `/guides/chill-hours`, `/guides/pollination`, `/guides/pruning`, `/guides/watering` (the drip/base-vs-overhead education). **The bulk of the "amount of information" lives here, out of the variety.**
- **Crop base (the crop hub):** the shared structure -- care sections + the pollination RULE + the bloom-calendar FRAME + rootstock options + the variety browser. Authored once per crop.
- **Variety delta (the overlay):** compact -- only what differs (its chill number, bloom slot, harvest window, flavor/use, disease resistance). Card-sized, like a soil type.

**Layout mechanics:** the soil-page pill/swiper maps to the variety SELECTOR (scales to 13+ chips fine). But a variety is NOT one swiper card -- its delta DISTRIBUTES across the page (chill block shows its number, bloom calendar highlights its bar, harvest timeline shifts, a small delta-summary panel gives the at-a-glance diff). The apple mock already renders a rich variety exactly this way (delta grid + zone note + bloom bar + per-variety plant/harvest arrays), so it is proven.

**Family tier (above crop):** family-shared biology (stone-fruit pruning, brassica pests, pome fireblight) is handled at AUTHORING time -- the GS family-hub anchors + bot derivation carry it into each crop's record -- plus the universal reference pages. NOT runtime inheritance. So the RENDERER stays two clean levels (crop base + variety delta); family is a reference-page + authoring layer above it. This keeps the renderer simple while honoring the real family -> crop -> variety biology hierarchy.

### A5. `lifecycle_override` (region-scoped) -- carried from the roadmap
Region-scoped annual-vs-perennial (strawberry grown as an annual in CA Interior Valleys; coastal CA keeps it perennial). **Region-scoped, NOT zone-scoped** (the roadmap's explicit correction). Lands in the region layer: `regions[r].lifecycle_override` (e.g. `"annual"`). Renderer/resolver reads it to swap the calendar + care model per region. Strawberry is the driver/first user (M19).

---

## 3. Thread B -- Containers, watering, irrigation/drip

### B1. Containers (gap-fill only -- already rich)
`container_notes` is structurally strong. Gaps to consider, additive:
- `self_watering_ok` (bool) + `self_watering_notes_*` -- self-watering/sub-irrigated containers are a real beginner win and currently unmodeled.
- `overwintering` exists but is a single field; for container PERENNIALS (potted citrus/fig), a `container_overwintering_seasoned`/`_beginner` with the move-indoors / wrap / chill-protection logic. Ties to Thread A.
- `fabric_pot_ok` / material guidance -- *optional, low priority.*

### B2. Watering -- DECIDED (Trevor 2026-06-10): build the structured by-stage model, app-ready
Trevor wants this built so the app (or the growing journey) can drive it -- e.g. a container tree advised **0.5 gpm at transplant, switching to 2 gpm when first flowers show**; or lettuce told to water at the **base, not overhead, to avoid rot**. So watering becomes a stage-keyed schedule, not flat prose:
- **`watering_method`** -- `base | drip | soaker | overhead_ok`, with `method_note_seasoned`/`_beginner` carrying the rot-avoidance / keep-foliage-dry logic. This is the "water at the base, not a sprinkler" case (lettuce: base only; many crops: avoid wetting leaves).
- **`schedule_by_stage[]`** -- the app-ready core, keyed to `growth_stages` ids:
  `{stage_id, system: hand|drip|soaker|self_watering, rate, frequency, level: low|moderate|high, note_seasoned, note_beginner}`
  `rate` carries the volume/flow Trevor described ("0.5 gpm", "2 gph", "1 inch/week", "deep soak"). The app reads `(stage_id, system, rate, frequency)` to schedule; the growing journey reads `note_*` for the human version. This is the transplant-0.5gpm -> flower-2gpm progression as data.
- **`drought_tolerance`** -- `low|moderate|high` + note (drives region/heat advice).
- **`critical_periods_*`** -- prose: the can't-miss windows (fruit sizing, head formation).
- Keep the existing flat frequency/amount/method/signs as the at-a-glance summary.

### B3. Drip / irrigation -- DECIDED (Trevor 2026-06-10): build it app-ready now (not deferred)
Resolved toward the structured build. The `schedule_by_stage` `(system, rate, frequency)` triple above IS the drip-ready surface -- the app can turn it into a drip schedule directly, and `watering_method` carries the base-vs-overhead rot logic. For drip specifically, `rate` holds flow (gph/gpm) plus an optional `emitter_note_*`. **What we are NOT putting in the dataset:** zones, emitter layout, soil-hydraulics run-times -- that stays an app-layer concern (the app computes a schedule from soil + climate + these per-crop targets). The dataset's job is the per-crop, per-stage TARGET; the app's job is the hydraulics. If the app scheduler is not built yet, the growing journey consumes the same `note_*` strings -- so it is "ready" either way.

---

## 4. Thread C -- Normalization sweeps (deterministic, no biology)

Bundle the structural-debt items so the one migration clears them:
- **C1. Shell-shape register normalization.** The 120 wiped crops carry pre-arc single-register shape on some universal keys (single `container_notes.shape_requirements` / `drainage.saucer_practice`) vs the GS crops' dual `_seasoned`/`_beginner`. Conform the 120 to the canonical UNIVERSAL key-shape (empty shape only, never values; single -> dual). Scoped to universal keys, not crop-specific ones. (Carried from the author-fresh pivot memory.)
- **C2. Dict-shell sources/anchoring_urls plumbing.** `watering`/`fertilizer`/`thinning`/`varieties` inconsistently carry `sources`/`anchoring_urls` across crops (carrot/beefsteak lack them; lettuce/cherry partial). Decide ONE policy (recommend: every claim-bearing dict-shell carries `sources` + `anchoring_urls`; add the keys null where missing) and sweep dataset-wide. Improves the Exeter-moat citation surface uniformly.
- **C3. Value-vocab -- DECIDED (Trevor 2026-06-10): carry BOTH a level AND the how-often / how-much, not either/or.** Context: today the field is inconsistent -- tomatoes say `harvest_urgency:"daily"` (a cadence) while carrot says `"low"` (a level), same for `fertilizer.frequency`. Trevor wants the level kept AND the cadence/amount surfaced, "especially for fertilizing." Resolution:
  - **`harvest_urgency`** -> a controlled **`level`** (`low|medium|high`, how time-sensitive) + a short **`cadence_*`** descriptor (how often to check/pick: "holds for weeks" vs "pick every day"). Renderer shows level as the badge, cadence as the human line.
  - **`fertilizer`** -> keep **`frequency`** as a cadence (how OFTEN), and ADD an explicit **`amount_seasoned`/`amount_beginner`** (how MUCH per feeding -- the dimension Trevor specifically wants), alongside the existing `type`/`npk_hint`/`example_product`. Optionally a `level` (light/moderate/heavy feeder). So fertilizer answers how often + how much + what.
  - Reconcile the existing values dataset-wide into these fields (carrot's `"low"` -> `level:"low"` + an authored cadence/amount; tomatoes' `"daily"`/"every 2 weeks" -> the cadence fields).

---

## 5. Field-applicability matrix (drives the migration)

Which archetypes carry which new/formalized field group (present-but-null; absent elsewhere):

| Field group | deciduous_fruit_tree | evergreen_fruit_tree | berries_woody | berries_herbaceous | culinary_herb (perennial) | annual / cool_season / warm_season | mushrooms / microgreen |
|---|---|---|---|---|---|---|---|
| chill_hours_* | yes | yes (often 0/null) | yes | -- | -- | -- | -- |
| bloom_*, pollination | yes | yes | yes | partial | -- | -- | -- |
| rootstock | yes | yes | -- | -- | -- | -- | -- |
| dormancy/pruning_window | yes | partial | yes | -- | partial | -- | -- |
| cane_management | -- | -- | brambles only | -- | -- | -- | -- |
| renovation | -- | -- | -- | strawberry/matted | -- | -- | -- |
| establishment_years | yes | yes | yes | yes | yes | -- | -- |
| lifecycle_override (region) | rare | rare | rare | strawberry | some herbs | -- | -- |
| watering_system / drought | yes | yes | yes | yes | yes | yes | n/a (mushroom) |
| container self_watering | yes (potted) | yes (potted citrus) | yes | yes | yes | yes | -- |

(Authoritative matrix finalized during the design-lock against the live archetype list; this is the v0 draft.)

---

## 6. Migration + gates

1. **Spec-lock** this doc (ratify; promote to `05-methodology/current/schema_2_9_specification_v1_0.md` + PK).
2. **`migrate_schema_2_9.py`** (test-first): additive null-scaffold per the applicability matrix; conform C1 register shape; add C2 plumbing keys null; reconcile C3 vocab. Deterministic, idempotent, re-run-safe. COMPACT serialization. Bump `schema_version -> 2.9` + extend `versioning_note`.
3. **Gate updates:** `register_completeness_gate` rulings for every new prose field (`chill_hours_note_*`, `bloom_*`, `pollinator_notes_*`, rootstock/cane/renovation prose, watering_system notes); `whole_crop_gate` applicability check (right groups present-null on right archetypes, absent elsewhere); the dual-voice coverage gate auto-covers the new `_seasoned`/`_beginner` pairs.
4. **Verification bars (methodology addendum):** what counts as T1 for chill hours (university pomology / extension variety tables), bloom windows, rootstock, drought tolerance. (Structural bar = Claude Code; the voice/copy bar for the new explainer prose = claude.ai, since "chill hours" is a hard beginner concept needing a gloss-then-use treatment.)
5. **No flips.** Migration leaves every crop's verification_status untouched; the perennial biology + flip happen per-anchor in M19.

---

## 7. Decisions

**RESOLVED (Trevor, 2026-06-10):**
- **A-1 rootstock:** ✅ structured `recommended_rootstock` + `rootstock_options[]` with the choose-by delineators (mature_height_ft, container_size_gallons, what_to_ask_nursery, size_class, traits_*). See A2.
- **A-3 pollination:** ✅ go deeper -- variety-level bloom-overlap calendar (the apple sample), not just crop-level. Crop-level `pollination` block + variety-level `bloom_group`/`bloom_window_relative`/`bloom_duration_days`/`chill_hours_required`. See A4.
- **B-1 drip/watering:** ✅ build the structured, app-ready by-stage model now (`watering_method` + `schedule_by_stage[{stage_id,system,rate,frequency,level,note_*}]`). Dataset supplies per-stage targets; app owns hydraulics. See B2/B3.
- **C-1 vocab:** ✅ carry BOTH level AND how-often/how-much. `harvest_urgency` = level + cadence; `fertilizer` = frequency + amount + type. See C3.

**STILL OPEN (engineering calls -- I will default these unless you say otherwise):**
- **A-2 sub-typing:** flat null-by-archetype (default -- matches the 26 already-scaffolded crops, no breaking retrofit) vs a nested `perennial:{...}` object. *Leaning flat.*
- **Version label:** 2.9 (default) vs a 2.8 sub-point.
- **Bundling:** one 2.9 migration for all three threads (default -- touch the 123-crop file once) vs separate bumps.
- **C2 plumbing policy:** every claim-bearing dict-shell carries `sources`+`anchoring_urls` (default) vs leave as-is.

## 8. Sequencing

2.9 gates the perennial/tree anchors. Of the anchor-5 candidates, **peach (stone-fruit tree)** needs 2.9 FIRST; microgreen and the annual family hubs (broccoli/bell-pepper/zucchini/onion/green-beans) do not. So either: run 2.9 now (unblocks peach + all tree/perennial anchors), or take an annual/indoor anchor-5 first and run 2.9 just before the first tree. Recommendation: **2.9 next** -- it is a ~4-5h design-lock + a deterministic migration, it clears the normalization debt for the whole dataset, and it unblocks the entire perennial/tree half of the anchor set at once.

---

## 9. Register breakdown (beginner vs seasoned) -- keeping the beginner lean

Principle (pair-vs-universal test): a field is **PAIRED** only when the beginner genuinely needs an actionable plain version; depth/comparison stays **SEASONED-ONLY**; single facts are **UNIVERSAL** (one plain line, everyone); numbers/enums are **MACHINERY** (no words). The beginner only ever sees the PAIRED + UNIVERSAL rows.

### PAIRED -- the only new prose a beginner sees (each = one plain sentence)
| Field | Beginner version (plain) | Seasoned version (depth) |
|---|---|---|
| `chill_hours_note_*` | "Your winters are cold enough for most apples." | the 700-1,000 hr requirement + low-chill-wasted-here mechanism |
| `pollination.notes_*` | "Plant a second apple nearby that blooms at the same time, or you get little fruit." | bee range, bloom-overlap, self-incompatibility |
| `watering_method_note_*` | "Water at the base, not over the leaves, to avoid rot." | foliar-disease pressure, canopy drying |
| `schedule_by_stage[].note_*` | "Now that it is flowering, water more often." | ET / root-depth / stage water demand |
| `fertilizer.amount_*` | "A small handful per plant." | "1 lb of 10-10-10 per 100 sq ft" |
| `self_watering_notes_*` | "A self-watering pot holds water in a reservoir, so you water less often." | sub-irrigation wicking, reservoir sizing |
| `container_overwintering_*` | "Bring your potted lemon inside before the first frost." | dormancy temps, chill-vs-freeze protection |
| `cane_management_*` | "After a cane has fruited, cut it to the ground." | floricane vs primocane, renewal ratio |
| `renovation_*` | "After harvest, mow the strawberry bed back." | matted-row renewal timing + thinning |
| `critical_periods_*` | "Do not let it dry out while the fruit is sizing up." | cell-division/expansion windows |

### UNIVERSAL -- one plain line, shown to everyone (beginner-safe, no split)
- `recommended_rootstock` + `recommended_rootstock_note` -- "A dwarf rootstock keeps it small enough for a pot."
- `rootstock_options[].what_to_ask_nursery` -- "Ask for it on a dwarf rootstock (e.g. M9)." (the nursery cheat-sheet)
- `establishment_years` + plain line -- "Won't fruit for about 3 years."
- `harvest_urgency` cadence line -- "Pick every few days." (paired with the `level` badge)

### SEASONED-ONLY -- beginner never sees these
- `rootstock_options[].traits_seasoned` (disease/soil-tolerance/anchorage comparison -- the beginner gets height + container + what-to-ask instead)
- `bloom_time_seasoned` (crop-level bloom prose -- the calendar covers the beginner)
- `drought_tolerance_note_seasoned`

### MACHINERY -- numbers / enums / bools, no register at all
chill_hours_required, chill_hours_range, bloom_group, bloom_window_relative, bloom_duration_days; pollination.self_fertile, needs_pollinizer, pollinizer_distance_ft; rootstock size_class, mature_height_ft, spread_ft, container_suitable, container_size_gallons, bearing_age_years; dormancy_window, pruning_window, lifecycle_override; watering_method, schedule_by_stage{stage_id, system, rate, frequency, level}, drought_tolerance; harvest_urgency.level, fertilizer.frequency, fertilizer.level, cane_type, self_watering_ok.

**Net beginner addition: ~14 short plain lines** (10 paired + 4 universal), each one sentence. Everything technical (rootstock comparison, bloom mechanics, all the numbers) is seasoned-only or machinery, so the beginner view stays a clean "what do I do" surface.
