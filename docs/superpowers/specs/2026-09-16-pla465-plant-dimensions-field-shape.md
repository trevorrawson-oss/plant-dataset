# Plant dimensions: crop-level `mature_height_ft`, `mature_spread_ft`, and the `footprint_inches` slot (PLA-465 + PLA-429 shape)

**Date:** 2026-09-16. **Canonical:** `a98b6cfd`. **Status:** DRAFT for Trevor's read. Rulings R2 through R7 and the D3 re-rule approved as recommended on the PLA-465 measurement comment; R1 CHANGED by Trevor the same day: define the fields for all 121 certified crops, author only the 30 tree and woody crops, presence-or-null carries the rest. This spec is the shape half of the field-addition method (`docs/gs_cross_crop_field_addition_v0.md`); the authoring and promote session follows on approval.

## 1. What this adds, in one table

| field | where | type | meaning | authored now on | null means |
| -- | -- | -- | -- | -- | -- |
| `mature_height_ft` | crop top level | `[lo, hi]` feet, numbers | the height a grower should expect the plant to reach as grown by the crop's method: on its recommended rootstock, or on its own roots where the rootstock basis is `not_applicable`; for a staked, trellised or trained crop, the trained height | the 30 tree and woody crops | not yet authored (91 certified crops), or a shell |
| `mature_spread_ft` | crop top level | `[lo, hi]` feet, numbers | the canopy width at maturity on the same basis | the 30 | same |
| `footprint_inches` | crop top level | number, inches | the width of the plant's own body at the ground: trunk diameter for a woody crop, mature crown or rootball width for a herbaceous one. Explicitly NOT canopy and NOT a recommendation; the physical floor, always below `spacing_inches[0]` | nobody (PLA-429's slot; it rides PLA-426) | not yet authored, roster-wide |

Every plant has a height, so no N/A value exists for the first two: null is "not authored" and nothing else. The seven uncertified shells are not touched (A39 exempts them until their own certification), so `release_verify --ref avocado` stays byte-identical.

## 2. The meaning, ruled (R2, R5, R7)

The crop-level figure is a **rootstock-plus-scion** figure by construction: it names the size on the recommended rootstock, which is what both consumers already lift as the recommended pick. On the 17 crops with rootstock rows, the recommended row carries a height and spread on 13 (measured 2026-09-16); on apricot, lime, pawpaw and plum the `recommended_rootstock` string matches no row, and on lemon the rows carry null, so those five are read from T1 like every other crop, not seeded. The standard size stays reachable through `rootstock_options[]` on `size_control` crops.

Shrubs and subshrubs (blueberry, the brambles, elderberry, lavender, rosemary, sage, thyme, oregano) use the same field; extension publishes a mature height and spread for them the same way, and the variety delta-overlay already carries the upright-rosemary case. The three cross-crop rootstock inconsistencies (Marianna 2624, Swingle citrumelo, trifoliate orange) are scion-dependent values under this meaning and are not edited.

For the 91 certified crops not authored here, the definition still holds when a later column pass fills them: mature above-ground height as grown by the crop's method (corn and sunflower at tasseling or bloom; an indeterminate tomato at its stake or cage height; a microgreen at cut height). That later pass is a consumer concern beyond D3: corn, sunflower and staked tomatoes shade neighbours, which is the planner's and PLA-534's.

## 3. Presence, the register row, and the population (R1 as changed, R6)

Register row **30**: `mature_height_ft` + `mature_spread_ft` + `footprint_inches`, three crop-level numerics, presence-or-null on every certified crop under the A39 register-coverage floor. Widening the definition to 121 costs nothing beyond this paragraph: A39's floor is roster-wide by default, and a woody-only field would have needed its own N/A predicate on top.

The authored population is the 30 tree and woody crops by archetype: 14 `deciduous_fruit_tree`, 7 `evergreen_fruit_tree` (5 certified + the avocado and olive shells, which take values only when they certify), 4 `berries_woody`, 5 `woody_ornamental`. Measured 2026-09-16: 19 of the 30 carry no height sentence anywhere in their prose, and the six genuine mature-height statements that exist are rootstock- or variety-conditional. This is new sourcing, not a lift.

## 4. The armor: A59, numeric bounds, provenance

- **A59 plant-dimensions shape**, wired into `whole_crop_gate` and run by `gate_all`, fires only when a field is non-null (A39 owns presence): each of `mature_height_ft` and `mature_spread_ft` is a two-number list with `0 < lo <= hi`; `footprint_inches` is a positive number and, when `spacing_inches` is present, strictly below `spacing_inches[0]`. Shape only; it does not judge the biology.
- **`numeric_sanity_gate`** gains the three checks with the basis-aware ceiling spacing already uses: height `[0.1, 120]` ft and spread `[0.1, 80]` ft on `_TREE_BASES` (`perennial_chill_gated`, `perennial_evergreen`, `berries_woody`); height `[0.1, 20]` ft and spread `[0.1, 20]` ft elsewhere (a rosemary at 6 ft, a sunflower at 12 ft, pole beans on a trellis at 10 ft all fit; a 60 ft basil does not); `footprint_inches` `[0.5, 60]`.
- **Provenance**: an authored value on a certified crop is an amend-not-recert addition, so each authored crop appends one `verification_status.field_additions[]` entry `{field: "plant_dimensions", date, sources, note}` naming the T1 page and what it states, the convention the pet_safe and timing_spine passes use and that A40 already checks for the spine. The promote refuses a non-null value on a crop with no such entry.
- **The promote** ships under the PLA-215 bar: a generated spec, a replay-pinned suite, a mutation harness with a liveness defense, set-before-value blast radius, pinned counts (121 keys written, 30 authored, 91 null, 7 shells byte-identical).

## 5. The rootstock override rule and its order (R3)

`rootstock_options[].mature_height_ft` and `spread_ft` become **overrides** of the crop-level figure on `size_control` crops and are **nulled on `soil_and_pest` crops** (PLA-463 D-B), where every row today carries the same placeholder (15 entries on peach, nectarine, apricot, persimmon). Order, ruled: **the crop-level field lands first, in this promote; the nulling follows in PLA-463's Plan E promote**, which carries the locked vocabulary that says which crops are `soil_and_pest`, so a consumer falls back to the crop level and never to nothing.

The consumer check that precedes the nulling, measured: plant-astro `RootstockCard.astro` renders "Mature height" per row; plant-app `TreeRootstockCard.tsx` and `RootstockRow.tsx` render height and spread per row; the app planner's `cropOnRootstock` substitutes a picked rootstock's `spread_ft` for the crop's spacing, so nulling those rows changes planner behaviour on the four crops (a picked Lovell stops supplying a 15 to 20 ft spread) until the planner falls back to `mature_spread_ft`. Plan E must land after the consumer sessions in section 8, or the planner change ships with it.

## 6. PLA-429's slot (R4)

`footprint_inches` is defined here and authored nowhere. Measured: `spacing_inches` is a range on all 121 certified crops and `thin_to_inches` exists on 41, both spacings; 42 crops mention trunk diameter, caliper, rootball or crown width in prose, all as handling instructions, never as a published width at the ground. The planner keeps its 6-inch floor constant until PLA-426 runs and this slot is filled as its rider. Defining it now means the split into per-crop files (PLA-537) does not have to add a key later.

## 7. D3 re-ruled

PLA-7 D3 routed wind and support to a PLA-10 height that did not exist. With `mature_height_ft` and `container_path` present, wind and support become an **app rule**, no new dataset field: a tall crop in a pot on a `rootstock` or `cultivar` path, or any crop above a height threshold the app sets, gets the support and wind copy. The dataset owes the number; the rule is the consumer's.

## 8. Consumers, frontend first

- **plant-app** `scripts/export-projection.mjs` SHIP allowlist gains the three keys (top-level keys do not ship otherwise); `catalog.ts` gains crop-level `heightFt` and `spreadFt`; the planner's `cropOnRootstock` falls back to `mature_spread_ft` before the crop's spacing; `TreeRootstockCard` shows the crop-level size above the per-row overrides.
- **plant-astro** `HeroCard.astro` gains a mature-size stat; `RootstockCard.astro` leads with the crop-level size and shows row figures as the overrides they are; the empty-array guard from PLA-464 stays.
- Neither consumer reads a crop-level dimension today, so nothing breaks before they change; the fields are inert until read.

## 9. Sourcing

T1 per crop: the crop's existing extension anchors usually publish mature height and spread on the same page as the rootstock or planting guidance (UC ANR fruit and nut pages, Clemson HGIC, UF/IFAS, NC State). Where only a nursery catalog states a size, the value is recorded as T2-only in the `field_additions` note, per the PLA-463 sourcing rule, or left null. No number is copied from `rootstock_options[]`; a row's figure that agrees with the T1 read is corroboration, not a source.

## 10. Sequencing

1. This spec, Trevor's read.
2. Authoring and promote session: 30 crops, two numbers each, from T1; the register row; A59; the `numeric_sanity` lines; the promote with suite and harness; the gauntlet; the state trio. Held for approval, then written with `--expect-sha`.
3. Consumer sessions (section 8), frontend first; the app allowlist line first of all.
4. PLA-463 Plan E: the basis remap and the `soil_and_pest` row nulling, after step 3.
5. A later column pass fills the 91 herbaceous crops when a consumer needs them (planner shading, PLA-534).

## 11. Out of scope, by name

Herbaceous authoring (step 5); the D-B nulling itself (Plan E); PLA-426 row spacing and the footprint fill; PLA-10 layout methods; PLA-11 yield; any edit to `rootstock_options[]` values.

## 12. Measured facts this rests on (2026-09-16, canonical `a98b6cfd`)

Two dimension keys roster-wide, both on rootstock rows (60 entries each). Population 30 by archetype as in section 3. 19 of 30 with no height sentence anywhere. Recommended-row height present on 13 of 17 rootstock crops; sharp recommended-versus-standard gaps on apple ([10, 14] vs [25, 35]), both pears ([12, 16] vs [25, 40]), cherry-sweet ([15, 20] vs [25, 40]). 15 placeholder rootstock heights on the four `soil_and_pest` crops. Roster-wide, 42 of 121 certified crops carry some foot-height sentence, mostly in `description_*` and `soil_prep_*`.
