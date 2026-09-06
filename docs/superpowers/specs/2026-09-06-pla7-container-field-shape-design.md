# PLA-7 container growing model: field-shape spec (dataset side)

**Date:** 2026-09-06. **Canonical:** `72371c02` (unchanged by this document). **Kickoff:**
`docs/kickoffs/54-pla7-container-model-kickoff.md` (the measurements this spec rests on).
**Rulings:** Trevor, 2026-09-06: D1 and D2 delegated ("whatever works best and gets accurate and
useful info into the hands of our users"); D4 approved on condition the container-safety slice of
PLA-142 is wrapped into the PLA-7 arc; D5 approved. D3 answered in section 4. D6 is a technical call.
**Constraint filed after the kickoff:** PLA-463 (Trevor, 2026-09-06 14:49): `rootstock_options[]`
assumes apple; a `rootstock_selection_axis` is proposed; PLA-7's container-path value must not
assume a size-controlling rootstock exists. This spec is written to survive PLA-463's outcome.

**This is the arc deliverable the PLA-14 sequence asked for:** it names what PLA-12 must author at
variety level, and the render contract every new or newly-rendered field carries.

---

## 1. What this spec adds, in one table

| field | where | shape | who authors | who reads |
|---|---|---|---|---|
| `container_path` | `container_notes` | enum `direct` / `rootstock` / `cultivar` / `tray`, or null | PLA-7 promote, roster-wide | astro CareGuideCard + HeroCard + beds tool; app planner catalog + guide chapter |
| `plants_per_pot` | `container_notes` | `[min, max]` integers, or null | PLA-7 promote where T1 publishes it | app planner (per-plant gallons); astro ContainerCard; app container chapter |
| `container_suitable` | `varieties.recommended[]` | `true` / `false` / null | PLA-7 migration on 63 crops; PLA-12 for every new variety | astro variety list + beds tool; app variety picker + planner |
| `container_min_gallons` | `varieties.recommended[]` | positive number, or absent | PLA-12, only where a source gives one | app planner (overrides crop `min_pot_gallons` for that cultivar) |
| `critical_warnings` | crop top level | list of warning objects, `[]` legitimate | PLA-7 authors the `safety` class; PLA-142 authors `harvest` | astro crop page hero block; app guide hero block; **renders in every mode** |

Everything else PLA-7 needs already exists and is unrendered; section 6 is the render contract for it.
No other field is added. Section 4 says why the rest of the advanced list is not fields.

---

## 2. `container_notes.container_path` (D1)

**Meaning.** The way a grower gets THIS crop into a pot. It names the JOIN the consumer should
follow, never the horticultural mechanism, so it does not depend on PLA-463's axis vocabulary:

| value | meaning | the consumer follows |
|---|---|---|
| `direct` | the crop as commonly sold grows in a pot; compact cultivars may do better but are not required | nothing; crop-level gallons apply |
| `rootstock` | a pot is viable only on a container-suitable rootstock | `rootstock_options[]` entries with `container_suitable: true` |
| `cultivar` | a pot is viable only with a compact / bush / patio / genetic-dwarf cultivar | `varieties.recommended[]` entries with `container_suitable: true` |
| `tray` | an indoor tray crop; depth governs, gallons do not | `depth_inches_min` |
| null | `container_ok` is `false` or undecided | nothing; the "No" line stands |

**Rules (each becomes a gate, section 7).**
1. `container_ok: true` requires a non-null `container_path`; `container_ok: false` requires null.
2. `rootstock` requires at least one `rootstock_options[]` entry with `container_suitable: true`, and,
   once PLA-463 lands, a crop whose `rootstock_selection_axis` permits it (`size_control` or
   `combined`). Until PLA-463 lands, no tree crop is flipped to `rootstock` by this arc except where
   the rootstock class is already T1 on the entry's own sources (apple, both pears, the citrus with a
   Flying Dragon entry, and both cherries on their WSU/OSU entries). Lemon and lime carry
   container-suitable trifoliate entries with no gallons: their `container_path` (`direct` or
   `rootstock`) is an authoring read of their own notes in session 2, after the D6 gallons fill.
   PLA-463 rules the rest crop by crop.
3. `cultivar` requires at least one `varieties.recommended[]` entry with `container_suitable: true`.
4. `tray` requires `depth_inches_min` non-null and matches the `microgreen` archetype.
5. The key is present-or-null on every CERTIFIED crop; the 7 uncertified shells carry no key (A39
   exempts them), so a roster promote leaves a shell byte-identical as its reference crop.
6. `container_ok` stays a boolean. **No new value is ever added to it**: plant-astro's CareGuideCard
   and the app's planner both test strict equality and blank on anything else.

**The four defect crops resolve three ways, not one.**
- cherry-sweet, cherry-sour: `container_ok: true`, `container_path: rootstock`. The Gisela 5 entries
  are sourced to WSU and OSU on the entries themselves and PLA-463 names those classes T1-citable.
  `min_pot_gallons` becomes the rootstock figure (25) so the crop-level stat has a number.
- mulberry: `container_ok: true`, `container_path: cultivar`. Its "Genetic dwarf (Dwarf Everbearing)"
  is a cultivar mis-homed as a rootstock entry (PLA-463's own point; the same name already exists in
  `varieties.recommended[]`). The variety entry takes `container_suitable: true` and
  `container_min_gallons: 15`, and `min_pot_gallons` becomes 15. The mis-homed rootstock entry is
  NOT removed by this arc: `rootstock_options[]` is PLA-463's shape to rule, so its retirement rides
  that ticket's follow-on (amended 2026-09-06 after the plan's feasibility pass).
- plum: **held**. PLA-463 records that plum's size-control claims are T2-heavy. It flips only after
  PLA-463's T1 read on Marianna 2624 / St. Julien A; until then it stays `false` with its prose,
  and the consumer disagreement on plum is accepted as known and logged on PLA-463.

**Consumer changes before the data flips (frontend first).** CareGuideCard: "Yes, on a dwarf
rootstock · 25+ gal" / "Yes, compact types · 5+ gal" / "Yes · 5+ gal" / "Tray, 2 in deep". HeroCard
the same qualifier as its sub-line. beds tool: a `rootstock` or `cultivar` crop shows its qualifier
on the chip. App `deriveContainerFacts`: `containerOk` reads `container_ok` alone (the
`|| suitable.length > 0` branch is what produced the disagreement); the qualifier is a new field
on the planner crop; a `cultivar` crop lists its `container_suitable` varieties in the picker the
way rootstocks are listed today.

---

## 3. The variety-level contract PLA-12 must author (D2)

`varieties.recommended[].container_suitable: true | false | null`
`varieties.recommended[].container_min_gallons: number` (optional key; present only when a source
gives a cultivar-specific pot size)

**Why this shape.** It mirrors `rootstock_options[].container_suitable` +
`container_size_gallons`, which the app already reads; one shape for both axes means
`deriveContainerFacts` grows one branch, not a second model. `plant_habit` stays a descriptive
trait under the variety contract; suitability is the load-bearing claim and is authored, not inferred.

**Null rules.** null = not assessed. `false` = assessed and not a pot plant (a vining zucchini, a
standard apple scion sold on seedling stock). PLA-12 authors a value on every entry of a crop whose
`container_path` is `cultivar`; elsewhere null is legitimate.

**Migration of `container_suitable_varieties[]` (63 crops, 222 names).**
1. The 162 names that match an existing entry become `container_suitable: true` on that entry.
2. The 60 that match nothing get a T1 read per crop: a real cultivar named in an extension container
   list (Illinois' table names Pixie, Patio, Salad Bush, Bush Champion, Spacemaster, Topcrop) becomes
   a new `{id, name, note, container_suitable: true}` entry; a name found only in vendor copy is
   dropped and the drop is logged in the crop's `verification_log`. No name enters from seed-catalog
   text (the PLA-426 "feeder, not a source" rule).
3. `container_suitable_varieties[]` is retired AFTER the astro beds tool and the app's
   `build-education-data.mjs` read the flag instead. Both are one-function changes.

---

## 4. D3 answered: what the advanced reader gets, and what does not become a field

Trevor asked whether "no new fields" means advanced users get nothing new. No. The advanced reader
gets more than the beginner from three sources:

1. **Everything already authored in the seasoned register, rendered for the first time** (D5):
   `notes_seasoned`, `watering_adjustment_seasoned`, `fertilizer_adjustment_seasoned`,
   `self_watering_ok` + `self_watering_notes_seasoned`, `soil_mix.type_seasoned` +
   `amendments_seasoned`, `shape_requirements_seasoned` (64 crops), `drainage.*`,
   `depth_inches_min`, `overwintering.approach_seasoned`, `container_overwintering_seasoned`.
   That is five of PLA-7's eight advanced items (root shape, dimensions, self-watering,
   overwintering, and the watering/feeding adjustments the issue folded into the watering note).
2. **One new number, `plants_per_pot`**, because it IS published at T1. Checked 2026-09-06:
   University of Illinois Extension's "Growing Vegetables in Containers" table carries
   `Container Size | Plant Type | Spacing/Planting | Recommended Varieties` with rows such as
   "Two gallon containers | pepper | 2 plants", "One gallon containers | leaf lettuce | 4-6 plants",
   "One gallon containers | green beans | 2-3 plants". Wisconsin, Clemson and UMD, which anchor 82
   of the block's crops, publish only narrative counts; Texas A&M E-545 is a PDF to read at
   authoring. So the field is authored where a T1 table or sentence gives it and is null elsewhere;
   13 crops already state a count in prose and are the first candidates.
   - Shape: `container_notes.plants_per_pot: [min, max]` integers `>= 1`, or null.
   - Semantics: the number of plants a pot of `min_pot_gallons` supports at maturity.
   - Consequence for the planner: per-plant root volume = `min_pot_gallons / plants_per_pot[max]`;
     null keeps today's behaviour (one plant per `min_pot_gallons`), so the field is purely additive.
     For leaf lettuce that changes a 2-gallon-per-plant charge to roughly a third of a gallon, which is
     the difference between "a 5-gallon pot holds two lettuces" and "holds twelve".
   - `min_pot_gallons` semantics, written down for the first time: **the smallest pot the sources
     recommend for this crop**, holding `plants_per_pot` plants (one when null). This goes into the
     schema doc and the register row.
3. **App rules with one T1 constant each**, which are not per-crop facts and would be fabricated if
   authored per crop:
   - Material and heat: a dark pot heats the root zone for every crop; education page, not a field.
   - Wind and support: a height question; rides PLA-10's `height_inches` and the `vertical` layout
     entry. Where a crop's pot must anchor a support (pole beans), the sentence already lives in
     `notes_seasoned`.
   - Yield reduction: no extension publishes a per-crop container yield penalty; PLA-11 owns yield;
     the honest sentence ("expect lighter crops than in the ground") stays in prose where a source
     says it.
   - Overwinter zone-shift: an app rule over `hardiness_zone_min` and the overwintering prose.
     Measured: of the 56 crops where container overwintering is relevant (38 `applicable: true` +
     the 17 woody perennials + persimmon), 30 carry `hardiness_zone_min` and 26 do not, and the 26
     are the herbs, alliums, brassicas and biennials whose overwintering is a "cover or bring in"
     instruction rather than a zone number. The app rule applies where the zone exists; the prose
     covers the rest. No field.
   - Pot width / diameter: not published per crop; depth + gallons are what the sources give.
   - Root shape enum: PLA-13's "whether root shape becomes a universal crop field" is answered NO by
     this spec: `depth_inches_min` is the number and `shape_requirements_*` the sentence.

**Dataset-side fixes riding with this** (D6): `overwintering.applicable` set `true` on the 17 woody
perennials whose prose says winter is the hard part; the two prose homes stay as they are (both are
sourced and both render under D5, `overwintering.approach_*` as the general instruction and
`container_overwintering_*` as the trunk-and-graft-union specifics) but the spec records that a
future pass may merge them; the 8 missing `depth_inches_min` filled from T1 where given.

---

## 5. `critical_warnings[]` with the safety class authored in PLA-7 (D4, Trevor's condition)

PLA-142 proposed `{title, body, stage, severity}` and left four questions open. To wrap the
container-safety slice into PLA-7 without leaving PLA-142 a migration, this spec settles the shape;
PLA-142 later authors the `harvest` class into the same field.

```jsonc
"critical_warnings": [
  {
    "id": "balcony-load",                 // kebab, unique within the crop
    "class": "safety",                    // safety | harvest
    "severity": "critical",               // critical | high
    "stage": null,                        // a growth_stages id, or null = always
    "title": "A full pot is heavy",
    "body_seasoned": "...",               // dual register, CORE-PROSE-NEEDS-SIBLING
    "body_beginner": "...",
    "sources": ["uiuc_ext"],              // sibling-field pattern: its own T1 sources
    "anchoring_urls": { "uiuc_ext": { "url": "https://extension.illinois.edu/container-gardens/growing-vegetables-containers", "verified": "2026-09-06" } }
  }
]
```

- Presence-or-null per A39: every crop carries the key; `[]` is the common, legitimate value.
- **Render rule, both consumers: `class: safety` renders in every experience mode and above the fold;
  `class: harvest` follows the mode.** This is PLA-7's "critical warnings are not hidden by
  experience mode" completion bullet, made a schema property instead of a UI convention.
- `severity` orders within a class; it does not change rendering. Two values only (YAGNI).
- The `safety` class in PLA-7 covers the container hazards the block's prose already raises on 9
  crops (balcony load, a tall staked vine in a light pot in wind, a saucer-flooded pot as a root-rot
  and mosquito source where a source says so). Each entry needs its own T1 source; where extension
  publishes the weight of wet potting mix per gallon, that is the citable figure. **No entry ships
  unsourced**: an unsourced safety warning is exactly the class of confident copy this dataset
  refuses.
- **Consumer prerequisite:** `critical_warnings` is a top-level key, and plant-app's
  `scripts/export-projection.mjs` ships top-level keys from an allowlist (`SHIP_TOP_LEVEL`). The key
  must be added there or the app never sees it. `container_notes` subkeys need no projection change.

---

## 6. The render contract (D5, approved)

**Frontend first**: each consumer ships its reader before the data changes that reader would
misrender. Data that is only newly READ (the prose) can render as soon as the card exists.

| field | plant-astro | plant-app |
|---|---|---|
| `container_ok` + `container_path` + gallons | CareGuideCard line and HeroCard stat carry the qualifier (section 2) | planner crop sheet + container placeability; `deriveContainerFacts` reads `container_ok` alone |
| `notes_*`, `watering_adjustment_*`, `fertilizer_adjustment_*` | new ContainerCard on the crop page, dual register via `RegisterText`, FeedingCard pattern | new "In a pot" chapter in `guide-chapters.ts` / `GuideChapters.tsx`, `reg(level, beginner, seasoned)` |
| `self_watering_ok` + notes | ContainerCard row "Self-watering pot: yes/no" + sentence | same chapter |
| `soil_mix.type_*` + `amendments_*` | ContainerCard "Mix" row; the 17 bare-enum `type_seasoned` values humanize via the A23 map | same chapter |
| `drainage.*`, `saucer_practice*` | ContainerCard "Drainage" row | same chapter |
| `depth_inches_min`, `shape_requirements_*` | ContainerCard "Pot shape" row | same chapter |
| `plants_per_pot` | ContainerCard "Plants per pot" | planner per-plant gallons (section 4) + chapter |
| `overwintering.*`, `container_overwintering_*` | ContainerCard "Winter" row, shown when `applicable` is true or the woody prose exists | chapter + a My Garden container nudge (PLA-7 label "My Garden") |
| variety `container_suitable` | variety list badge; beds tool chips read the flag | variety picker badge; planner cultivar pick |
| `critical_warnings[]` `safety` | hero block above the fold, every mode | hero block above the fold, every mode |
| `container_specific_pests` | retired (D6) | retired |

**Fail-open checks owed before each consumer ships** (the `annual_only` lesson): what each card
renders when the field is null, when the enum value is unknown, and when `container_ok` is `false`.

---

## 7. Gates and register (the armor)

- **A39 presence-or-null** joins: `container_notes.container_path`, `container_notes.plants_per_pot`,
  top-level `critical_warnings`. Register rows added to `docs/field_addition_register.md` with the
  consumer named per row (this spec, section 6).
- **Shape gate** (A40-style): `container_path` enum membership; `plants_per_pot` `[min, max]` ints,
  `1 <= min <= max <= 30`; `critical_warnings[]` object keys, `class`/`severity` enums, unique ids,
  `body_beginner` present when `body_seasoned` is (CORE-PROSE-NEEDS-SIBLING), sources non-empty.
- **Coherence gate**, fails LOUD like the variety join gates: rules 1-4 of section 2; `rootstock`
  additionally checks PLA-463's axis once that field exists; variety `container_min_gallons` present
  only on entries with `container_suitable: true`.
- **numeric_sanity_gate**: `plants_per_pot` bounds; `container_min_gallons` `[1, 100]` like its crop
  sibling.
- **register_completeness**: `critical_warnings[].body_*` ruled as a compound register pair;
  `container_path` and `plants_per_pot` are structured, not prose.
- **Promote suite + mutation harness** per PLA-215: one mutation per guard family, MUTATION-APPLIED
  marker + sentinel, positive controls where an injection could be invisible (the coherence gate on
  a crop with `container_path: rootstock` and no suitable rootstock), `set(pre) == set(post)` before
  value comparison, refusal-spec passes for good input. The suite pins its pre-state via
  `promote_fixture.COMMIT_FOR` and reads NO live registry or live variety list.
- **Release**: whole_crop_gate 18/18, gate_all, release_verify with the declared crops, the
  source-truth sample on every new numeric and every new variety entry.

---

## 8. Sequencing

1. **Now (PLA-463 in flight in claude.ai):** this spec; PLA-463 receives the rootstock extraction it
   asked for (delivered 2026-09-06). The non-tree half of the roster does not wait on PLA-463.
2. **Session 2, dataset promote (held for approval):** `container_path` roster-wide for the 107
   `container_ok: true` crops as `direct` / `cultivar` / `tray`, and `rootstock` only for apple, both
   pears, and the citrus whose container entry is Flying Dragon; the cherry and mulberry fixes
   (section 2) and the plum hold; the variety migration (section 3); `plants_per_pot` where T1 gives
   it; `critical_warnings` `safety` entries with T1 sources; `overwintering.applicable` on the 17
   woody; the D6 riders (retire `container_specific_pests` with basil `spider_mites` migrated into
   `pests[]`, one `gravel_layer` encoding, the 5 herb `_seasoned` siblings, the 3 citrus rootstock
   gallons and the 4 empty `sources` from T1 reads, the 8 `depth_inches_min`). Suite, harness,
   gauntlet, state trio.
3. **Consumer sessions (plant-astro, plant-app):** section 6, frontend first; the projection
   allowlist; the `deriveContainerFacts` change. Astro submodule bump is the astro session's.
4. **PLA-463 lands its axis and per-crop T1 pass:** the remaining tree crops (plum, apricot,
   nectarine, peach, persimmon, pawpaw) get their `container_path` and any `container_ok` flip in a
   small follow-on promote under PLA-463, reusing this suite.
5. **Session 3, dataset:** independent source-truth sample on the 99 `min_pot_gallons`, the 16
   rootstock gallons and every new `plants_per_pot`, per kickoff 45's warning that the pot figures
   were authored under varying discipline.
6. **Close PLA-7** with the record: what PLA-12 authors (section 3), what PLA-142 inherits
   (section 5), what PLA-10 and PLA-11 own (section 4), the app rules declared not-fields, the
   PLA-13 answers (container suitability sits on the variety axis via `container_suitable`; root
   shape is not a universal field).

## 9. Out of scope, by name

PLA-463's axis vocabulary and null rules for `size_class` / `mature_height_ft` (that ticket rules
them; this spec only consumes them); PLA-10 height/spread/support; PLA-11 yield; PLA-142's
`harvest` class; kickoff 45's irrigation numbers; the plot/bed surface-area models; merging the two
overwintering prose homes.
