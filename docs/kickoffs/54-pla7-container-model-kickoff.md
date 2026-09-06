# 54 - PLA-7, the container growing model: kickoff (dataset side)

**Written:** 2026-09-06, the session after the overnight cleanup. **Canonical measured:** `72371c02`
(HEAD `9a79e35`, pushed, in sync). **Linear:** PLA-7 (Todo -> In Progress with this document).
**Required reading, done:** PLA-429, PLA-409. **Sibling specs read:** PLA-426 (row spacing shape),
PLA-10 (layout), PLA-142 (critical_warnings), PLA-13 (the closing schema decisions), PLA-305.

> **Amended 2026-09-06 (later the same day):** Trevor ruled D4 and D5, delegated D1 and D2, and asked
> about D3; PLA-463 (rootstock selection axis) was filed against D1's `dwarf_rootstock` assumption. The
> rulings and the reconciled shapes live in
> `docs/superpowers/specs/2026-09-06-pla7-container-field-shape-design.md`; read that before §6 here.

> Every number below was MEASURED on `72371c02` with a key walk over `crops_data_final.json` and a
> grep over `~/plant-astro/src` and `~/plant-app/src` + `scripts`. Re-measure before believing any of
> them in a later session. Nothing in this document changes canonical.

---

## 0. What PLA-7 asks, and the one-sentence finding

PLA-7 proposes a **beginner** experience (pot size, drainage guidance, watering note, one compact
variety, a simple overwinter indicator), an **advanced** experience (root shape, full container
dimensions, material and heat, self-watering suitability, wind and support, multi-plant spacing,
yield reduction expectations, overwinter zone-shift logic), a **safety requirement** (balcony weight
warnings render regardless of experience mode), and closes when beginner and advanced behavior is
defined, the dataset fields are confirmed, container context is represented in the app, and critical
warnings are never hidden by mode. The PLA-14 sequence adds an arc deliverable: **a field-shape spec
naming what PLA-12 must author at variety level.**

**The finding: the container model is already AUTHORED and almost entirely UNRENDERED.**
`container_notes` exists on all 128 crops with roughly 35 leaf keys. On the 121 certified crops it
carries **3,068 non-null leaves, of which 644 are read by any consumer; 2,183 of those leaves are
prose strings, of which 222 are read, and those 222 are the bare variety-name chips.** Every
dual-register prose pair in the block (notes, watering, fertilizer, self-watering, soil mix, shape,
saucer practice, overwintering) renders nowhere on plant-astro and nowhere in plant-app, although
plant-app's export projection ships the whole object. This is the roadmap's standing item
("authored, exported, rendered nowhere") at its largest known scale, and it means PLA-7 is mostly a
**consumer contract + a handful of shape decisions**, not a column-authoring arc.

---

## 1. Start state -- VERIFY, DO NOT TRUST

| | |
|---|---|
| canonical | `72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222` |
| HEAD | `9a79e35` on `main`, in sync with `origin/main` |
| held | PLA-457 promote prepared, NOT applied (`docs/2026-09-06-pla457-sulfur-oil-interval-prepared.md`) |
| known red | `test_bare_host_scan::test_self_pathed_population_at_this_canonical`, `test_cited_claim_scan::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass` (pre-existing, 2 failed / 5,347 passed) |

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json          # must equal LATEST.txt
git log --oneline -3 && git status -sb
```

---

## 2. What the required reading binds

**PLA-409 (container fullness).** Both halves SHIPPED in plant-app on 2026-08-27 (`e4ae9294`,
`17eb503c`, OTA group `9f238713`). A pot that knows its gallons now measures **root volume**:
`rootstock_options[].container_size_gallons` for a picked rootstock, else the crop's
`container_notes.min_pot_gallons`; a woody crop is one root system regardless of count, packers
drink **per plant**; a planting with no gallons figure consumes its area share converted to gallons.
The canopy-versus-floor question was dissolved, not answered. **Consequence for PLA-7:** the
dataset's container numerics are already load-bearing in the planner, and `min_pot_gallons` is
consumed as a PER-PLANT figure. That semantics is nowhere written in the dataset. It must be.

**PLA-429 (no footprint distinct from spacing).** A bed/row problem: trunk-or-rootball width as a
floor for the spacing solver, Low priority, a rider on PLA-426/PLA-10. **It does not bind PLA-7**:
root volume replaced surface area in pots, so "multi-plant spacing" in a container is a gallons
question (how many root systems fit the pot), not an inches question. PLA-7 should say so and hand
the footprint back to PLA-10.

---

## 3. The measured shape (121 certified; the 7 shells carry `container_ok: null` and nulls throughout)

**Decision and numerics**

| key | present | note |
|---|---|---|
| `container_ok` | 107 True / 14 False | False = peach, plum, apricot, nectarine, persimmon, mulberry, pawpaw, cherry-sweet, cherry-sour, asparagus, and the 4 corns |
| `container_recommended` | 103 bool / 4 null on True crops | null on lettuce-leaf, orange-navel, mandarin-clementine, grapefruit |
| `min_pot_gallons` | 99 | the 8 True crops without it are the 8 tray crops (depth governs; §3 gate) |
| `recommended_pot_gallons` | 95 | missing on 12 True crops: 8 trays + lettuce-leaf, orange-navel, mandarin-clementine, grapefruit |
| `depth_inches_min` | 99 | missing on 8 True crops: lemon, lime, orange-navel, mandarin-clementine, grapefruit, fig, pomegranate, lettuce-leaf |
| `self_watering_ok` | 99 bool | |
| `overwintering.applicable` | 38 True / 65 False / 18 null | the 18 null = 17 woody perennials + asparagus |
| `drainage.drainage_holes_required` | 98 bool | |
| `drainage.gravel_layer` | 64 `False` + 16 `'not_required'` + 41 null | **two encodings of one fact** |
| `container_suitable_varieties[]` | 63 crops, 222 names | bare strings; **162 match a `varieties.recommended[]` entry, 60 (on 26 crops) do not** |
| `container_specific_pests[]` | populated on 3 | **RULED retire 2026-08-22 (PLA-8 r1), not yet retired**; basil `spider_mites` exists nowhere else, a blind retire destroys it |
| `sources` / `anchoring_urls` | 109 / 109 | **12 certified crops have an empty `sources`**: the 4 corns, dry-bean, green-beans-bush, apricot, nectarine, peach, plum, grapefruit, orange-navel. Four of those are `container_ok: true` (dry-bean, green-beans-bush, grapefruit, orange-navel), a GS checklist Step 2 bar miss (">= 2 T1 + anchoring URLs") |

**Dual-register prose (pairs on certified crops)**

| pair | seasoned / beginner | note |
|---|---|---|
| `notes_*` | 121 / 121 | |
| `watering_adjustment_*` | 115 / 120 | thyme, rosemary, oregano, sage, lavender carry beginner ONLY |
| `fertilizer_adjustment_*` | 115 / 120 | same five |
| `self_watering_notes_*` | 120 / 120 | |
| `soil_mix.type_*` | 120 / 120 | `type_seasoned` is a bare enum `container_potting_mix` on 17 crops and free prose on ~100 (whole_crop_gate line ~805 already tolerates this) |
| `soil_mix.amendments_*` | 120 / 120 | |
| `shape_requirements_*` | 64 / 64 | prose "deep beats wide"; no enum |
| `drainage.saucer_practice_*` | 39 / 39, plus 45 bare `saucer_practice` | ruled USER-FACING-CATEGORICAL bare line (Trevor 2026-06-22) |
| `overwintering.approach_*` | 102 / 102 | |
| `container_overwintering_*` | 23 / 23 | woody only; **22 of the 23 ALSO carry `overwintering.approach_*`** -- two prose homes for one topic on the same crop (apple carries both, fully populated); persimmon is the one with `container_overwintering_*` alone |

**Rootstocks (19 woody crops, 66 entries):** `container_suitable` 66 bool (19 True);
`container_size_gallons` 16 numeric, null on 3 suitable entries (lemon's trifoliate and Carrizo/Swingle,
lime's Swingle), so the app falls back to the crop's 15 gal for those.

**Variety level:** no `container_suitable` / habit flag exists on any of the 756 variety entries.
`plant_habit` exists on 5 dry-bean entries as a descriptive trait. 111 entries on 60 crops mention a
container/compact/patio/dwarf/bush signal in prose.

**What does not exist at all:** container material/heat, wind/support (no crop-level support or
trellis field anywhere; 33 crops mention wind in container prose), plants-per-pot (24 crops say
"one plant per pot" in prose), container yield reduction (5 crops mention it; `yield_expectations`
has no container variant), pot width/diameter, a zone-shift number (`hardiness_zone_min/max` exist on
31 crops; apple's prose says a tree hardy to zone 4 in the ground may only take a milder pot winter).

---

## 4. The render path, measured (the standing item)

| reader | reads | renders as |
|---|---|---|
| plant-astro `CareGuideCard.astro` | `container_ok`, `min_pot_gallons` | the one-line stat "Yes · 15+ gal pot" / "No" |
| plant-astro `HeroCard.astro` | `container_ok`, `recommended_pot_gallons`, `min_pot_gallons` | the hero stat "20 gal / min 15 gal pot" |
| plant-astro `lib/containers.ts` -> `pages/guides/beds.astro` | `container_ok`, `container_recommended`, both gallons, `container_suitable_varieties` | the "what size pot" tool: 4 size bands, crops as chips, variety names as chips, "belongs in the ground" list |
| plant-astro `RootstockCard.astro`, `lib/planner/catalog.ts` | rootstock `container_suitable`, `container_size_gallons` | rootstock card + planner |
| plant-app `lib/planner/catalog.ts` `deriveContainerFacts` | `container_ok`, `min_pot_gallons`, `recommended_pot_gallons`, rootstock `container_suitable`/`container_size_gallons`/`spread_ft` | placeability, the pot rule, the FullnessMeter (PLA-409), the rootstock pick |
| plant-app `scripts/build-education-data.mjs` | the same five keys as astro's `containers.ts` | Learn > beds pot-size bands |
| plant-app `scripts/export-projection.mjs` | ships `container_notes` and `rootstock_options` whole | the app HAS every string and reads none of the prose |

**Read by NO consumer:** `depth_inches_min`, `drainage.*`, `soil_mix.*`, `watering_adjustment_*`,
`fertilizer_adjustment_*`, `self_watering_ok`, `self_watering_notes_*`, `shape_requirements_*`,
`overwintering.*`, `container_overwintering_*`, `notes_beginner` / `notes_seasoned`,
`container_specific_pests`. (The astro `notes_*` and `drainage` grep hits are StoringCard, FeedingCard,
TimingSpineCard and `soil.drainage_requirement`, not the container block.)

**PLA-7's proposed lists against this:**

| proposed | dataset today | rendered today |
|---|---|---|
| beginner: pot size | `min_pot_gallons` / `recommended_pot_gallons` | YES (both consumers) |
| beginner: drainage guidance | `drainage.*` + `saucer_practice_*` | no |
| beginner: watering note | `watering_adjustment_*` | no |
| beginner: one compact variety | `container_suitable_varieties[]` bare strings | as chips in the beds tool only; not on the crop page, not joined to the variety list |
| beginner: overwinter indicator | `overwintering.applicable` + `approach_*`; `container_overwintering_*` | no |
| advanced: root shape | `shape_requirements_*` prose, 64 crops; no enum | no |
| advanced: full dimensions | depth only (`depth_inches_min`); no width | no |
| advanced: material and heat | absent | n/a |
| advanced: self-watering suitability | `self_watering_ok` + notes | no |
| advanced: wind and support | absent as a field | n/a |
| advanced: multi-plant spacing | absent as a field; per-plant gallons implied | the planner already prices it in gallons (PLA-409) |
| advanced: yield reduction | absent; 5 crops in prose | n/a |
| advanced: overwinter zone-shift | prose only | no |
| safety: balcony weight | prose on 9 crops mentions balconies, 6 mention weight; no field | no |

---

## 5. Defects and tensions found while measuring (none fixed; canonical untouched)

1. **The two consumers give OPPOSITE container answers for plum, mulberry, cherry-sweet and cherry-sour.**
   Each carries `container_ok: false` while its own `notes_seasoned` says a container "can work" on
   St. Julien / Marianna, Dwarf Everbearing, Gisela 5, and each has a `rootstock_options[]` entry with
   `container_suitable: true` and a gallons figure (25, 15, 25, 25). plant-astro prints "No" on the
   crop page and lists all four under "belongs in the ground"; plant-app's planner computes
   `containerOk = container_ok || any suitable rootstock` and places them at 25 gal. Root cause: the
   crop-level boolean has no way to say "yes, but only on a size-limiting rootstock." Apple (`true`,
   "only on M9/M27") is the same fact encoded the other way round. This is PLA-13's first open
   decision, met in the data.
2. `container_specific_pests` is ruled retire (2026-08-22) and still present on 127 crops.
3. Five woody herbs carry `watering_adjustment_beginner` and `fertilizer_adjustment_beginner` with no
   `_seasoned` sibling (thyme, rosemary, oregano, sage, lavender).
4. Twelve certified crops have an empty `container_notes.sources`; four of them are `container_ok: true`.
5. `drainage.gravel_layer` mixes `False` and `'not_required'` for the same fact.
6. `soil_mix.type_seasoned` mixes a bare enum (17) with free prose (~100).
7. Sixty of the 222 `container_suitable_varieties` names have no variety entry to join to.
8. Twenty-two woody crops carry both `overwintering.approach_*` and `container_overwintering_*`; the
   17 woody perennials also have `overwintering.applicable: null` while their prose says winter is
   the hard part.
9. Three container-suitable citrus rootstocks carry no gallons, so the app silently substitutes the
   crop minimum.
10. `min_pot_gallons` is consumed per plant (PLA-409) and its semantics are documented nowhere.

---

## 6. Decisions for Trevor (product / content calls; one row each, with a recommendation)

**D1. How the dataset says "in a pot, but only on a dwarf rootstock or a compact cultivar."**
- (A) Keep the boolean; flip the four crops to `true` with the rootstock's gallons; let prose carry
  the condition. Cheapest; the consumers agree again; the crop-page stat then reads "Yes · 25+ gal
  pot" for a sweet cherry with the condition invisible.
- (B) **Recommended.** Keep `container_ok` as "some path exists" and add a sibling
  `container_path` enum, present-or-null: `direct` | `dwarf_rootstock` | `compact_cultivar` | `tray`.
  The four crops become `true` + `dwarf_rootstock`; apple, both pears, the citrus, fig, pomegranate
  and mulberry are declared the same way; the trays (`depth_inches_min` crops) get `tray`; bush
  tomatoes / peppers / cucurbits with a compact list get `compact_cultivar` where the prose says
  compact types are the container performers. The consumers render the qualifier ("Yes, on a dwarf
  rootstock · 25+ gal"). This is the variety-axis answer PLA-13 asks for: `dwarf_rootstock` points at
  `rootstock_options[].container_suitable`, `compact_cultivar` at the variety flag in D2.
- (C) Retire the crop-level boolean and derive it from rootstock/variety flags. Rejected: 88 crops
  have no rootstocks and no variety carries a flag; the roster would go null.
- **Trap either way:** `CareGuideCard` tests `container_ok === true` / `=== false` and blanks on
  anything else; the app tests `=== true`. Any new VALUE on `container_ok` itself would silently blank
  both. A new sibling key is invisible to both until they read it, which is safe. Frontend first.

**D2. The variety-level field PLA-12 must author (the arc deliverable).**
- (A) **Recommended.** `varieties.recommended[].container_suitable: true | false | null` mirroring the
  rootstock shape the app already reads, plus an optional `container_min_gallons` override where a
  source gives one. Migrate `container_suitable_varieties[]` into it: the 162 matched names become
  flags on existing entries; the 60 unmatched names either get entries (they are real cultivars,
  e.g. Tumbling Tom, Bush Early Girl, Top Hat, Spacemaster) or are dropped, per crop, in a source-read.
  Then retire the bare-string list. One shape for both axes; `deriveContainerFacts` extends by one
  branch.
- (B) `plant_habit` enum (`compact` | `bush` | `dwarf` | `patio` | `vining` | `standard`) as the
  biology, with suitability inferred by the app. Habit is descriptive under the variety contract and
  the inference is a rule the app would own; it does not answer "is THIS cultivar a pot plant" for a
  determinate tomato that still wants 15 gal.
- (C) Both. Only if PLA-10's height/spread override work wants `plant_habit` anyway; otherwise YAGNI.

**D3. Which of PLA-7's advanced items are dataset fields, and which are app rules or education pages.**
- Material and heat: **not a crop field** (a dark pot heats up for every crop). App-side education
  content, one page. Recommend declaring it so in PLA-7 and moving on.
- Wind and support: **not a container field**. Rides PLA-10's `height_inches` + `planting_layout`
  `vertical` entry; the container-specific sentence ("the pot must anchor a 6-foot support", pole
  beans) already lives in `notes_*`.
- Multi-plant spacing: **gallons per plant, already the app's model.** Recommend writing the
  PER-PLANT semantics of `min_pot_gallons` into the schema doc and the register, and authoring
  `plants_per_pot: [min, max] | null` ONLY if Trevor wants the "one plant per pot" instruction to be
  machine-readable (24 crops state it in prose today). Recommendation: not now; the notes carry it.
- Yield reduction: **not a number.** No extension publishes a per-crop container yield penalty
  (the "not a published datum" trap); the honest statement is prose and PLA-11 owns yield. Recommend
  no field; where a crop's notes already say "lighter crops than in the ground" that stands.
- Full container dimensions: recommend NO width field; depth + gallons is what the sources publish
  and the app consumes gallons. Fill the 8 missing `depth_inches_min` (citrus, fig, pomegranate,
  lettuce) in the promote if a source gives them.
- Root shape: keep `shape_requirements_*` as prose (64 crops); no enum. The advanced reader gets the
  sentence.
- Overwinter zone-shift: **an app rule, not a field**: read `hardiness_zone_min` (31 crops) and the
  container overwintering prose. Dataset-side the owed change is finding 8: one prose home, not two,
  and `overwintering.applicable` decided (true) on the 17 woody perennials.

**D4. Safety: balcony weight.** Recommend PLA-7 authors NO container safety field. PLA-142
(`critical_warnings`, sequence step 5) already lists "container safety: balcony weight limits" as a
known example and carries the "renders regardless of mode" rule as its own open design question.
PLA-7 closes its safety bullet by naming PLA-142 as the home and handing it the 9 balcony / 6 weight
mentions as candidates, not by authoring. Trevor's call whether that ordering is acceptable (safety
lands at step 5, not step 1).

**D5. Where the prose renders (the consumer contract).** Today: nowhere. Options: (A) a
dual-register ContainerCard on the plant-astro crop page (FeedingCard pattern) and a container
chapter in plant-app's GuideChapters, reading notes / watering / fertilizer / self-watering /
drainage / overwintering by register; or (B) declare the prose a dataset-side asset (Herb context
only). **Recommend (A)**: 2,183 authored strings exist because the GS checklist required them
(Steps 6-8 name `container_notes.*_beginner` as CORE-PROSE-NEEDS-SIBLING), and PLA-7's own
completion bullet says container context is represented in the app. Frontend-first sequencing
(the fail-open-renderer lesson).

**D6. Riders in the same promote (technical; I make the call unless overruled):** retire
`container_specific_pests` with the basil `spider_mites` migration into `pests[]`; normalize
`gravel_layer` to one encoding; author the five missing `_seasoned` siblings; fill the 3 citrus
rootstock gallons and the 4 empty `sources` on `container_ok: true` crops from T1 reads; leave
`soil_mix.type_seasoned`'s enum/prose mix alone (ruled tolerable, A23-adjacent, and the app does
not read it).

---

## 7. Arc plan (after D1-D5 are ruled)

1. **Session 2, dataset.** Write `docs/superpowers/specs/2026-09-xx-pla7-container-field-shape-spec.md`:
   the `container_path` enum (D1) and the variety `container_suitable` flag (D2) as the PLA-12
   authoring contract; the per-plant semantics of `min_pot_gallons`; the render contract per field
   for both consumers (D5); the register row in `docs/field_addition_register.md` per
   `gs_cross_crop_field_addition_v0.md`. Then the promote: `container_path` roster-wide
   (present-or-null, joins A39; shape gate A4x), the four-crop fix, the variety migration on the 63
   crops with a source-read on the 60 unmatched names, the D6 riders. Suite + mutation harness per
   PLA-215; gauntlet per protocol #6; state trio; hold for approval.
2. **Session 3, dataset.** Independent source-truth pass on the container numerics: kickoff 45
   recorded that the pot-size figures "were authored under varying discipline"; sample the 99
   `min_pot_gallons` and 16 rootstock gallons against their anchors before the planner leans harder
   on them.
3. **Consumer sessions (plant-astro, plant-app; not this repo).** Read `container_path` and the
   variety flag; render the qualifier on the crop stat; the ContainerCard / chapter; extend
   `deriveContainerFacts` with the variety branch; retire the `container_suitable_varieties` read once
   the flag lands. Ship before the data flips (frontend first). plant-astro submodule bump is the
   astro session's.
4. **Close.** PLA-7 close-out in Linear naming: the spec path, what PLA-12 authors, what PLA-142 owns,
   what PLA-10 owns (support/height), the app rules (zone shift, material) declared not-fields.

---

## 8. Traps

- **Do not add a value to `container_ok`.** Both consumers blank on a non-boolean (section 6, D1).
- **Frontend first** for anything the consumers read; the data flip is the last step.
- **Do not fill the 60 unmatched cultivar names from seed-vendor copy.** They enter as variety
  entries only through a T1 read (the PLA-426 "Herb's lookups are a feeder, not a source" rule).
- **The basil `spider_mites` entry** dies in a blind `container_specific_pests` retire.
- **PLA-429 does not bind this arc.** Do not author a footprint number for pots.
- **The 4-crop fix is a CONTENT change on `container_ok`** and moves what the astro beds tool lists;
  it holds for approval like any canonical write.
- **A guard that reads the live variety list or the live registry** goes red on replayed states;
  pin to a commit or a staged snapshot (the PLA-450 lesson).

## 9. Not in scope, by name

PLA-10 (height/spread/support), PLA-11 (yield), PLA-142 (the warnings field itself), PLA-409's
plot/bed surface-area models, kickoff 45's irrigation numbers (blocked on the tier arc), PLA-457,
PLA-462, PLA-453, PLA-448 s4d.
