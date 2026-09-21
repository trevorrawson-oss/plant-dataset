# `container_notes.plants_per_pot`: field-shape spec (PLA-580, PLA-7 Plan C)

**Date:** 2026-09-21. **Canonical:** `1721208e` (unchanged by this document; no promote, no data
change). **Branch:** `worktree-pla580`, spec commit only.
**Supersedes, in part:** the two-paragraph sketch in
`docs/superpowers/specs/2026-09-06-pla7-container-field-shape-design.md` section 4 item 2. Where
this document and that one disagree, the disagreement is named in section 2 and the measurement is
given. **Read with:** PLA-580, PLA-7 (D3), PLA-409.

**The headline.** The 2026-09-06 sketch assumed a count could be bound to `min_pot_gallons`. It
cannot. Measured against raw bytes, the dataset's `min_pot_gallons` disagrees with the pot size
Illinois states its counts against on **9 of 10** counted rows, by factors from 1.5x to 5x. The one
row that agrees is leaf lettuce, which is the row the sketch worked its example on. A count carried
without its own pot size is not a datum, and the consumer that would read it is already built and
would already render the error.

---

## 1. What this adds, in one table

| field | where | shape | who authors | who reads |
|---|---|---|---|---|
| `plants_per_pot` | `container_notes` | object `{count: [min, max], at_gallons: number, sources: [...], anchoring_urls: {...}}`, or `null` | PLA-580 promote, roster-wide, null where no T1 count exists | plant-app planner (`plantingGallons`) + container chapter row; plant-astro ContainerCard, once one exists |

No other field is added. `min_pot_gallons` and `recommended_pot_gallons` are not touched, not
re-read and not re-derived by this arc.

---

## 2. The reads, from raw bytes (found / absent / undetermined)

All four sources fetched 2026-09-21. Byte counts, sha256 digests and the exact fetch results are in
section 12. Every quotation below is copied from those bytes.

### 2.1 Illinois Extension: FOUND, and it is the only per-crop table

`https://extension.illinois.edu/container-gardens/growing-vegetables-containers`, HTTP 200, 28,754
bytes. One `<table>`, 14 data rows, captioned "Container sizes and varieties of vegetables suitable
for container gardening". No counts appear anywhere else on the page.

Every row, verbatim, with the container size each count is stated against:

| container size | plant type | spacing/planting | count? |
|---|---|---|---|
| Half-gallon | parsley | 1 plant | 1 |
| One gallon | cabbages | 1 plant | 1 |
| One gallon | cucumbers | 2 plants | 2 |
| One gallon | green beans | 2-3 plants | 2-3 |
| One gallon | leaf lettuce | 4-6 plants | 4-6 |
| One gallon | spinach | direct seed, thin to 1-2 inches apart | **no count** |
| One gallon | Swiss chard | 1 plant | 1 |
| One gallon | cherry and patio tomatoes | 1 plant | 1 |
| Two gallon | beets | thin to 2-3 inches apart | **no count** |
| Two gallon | carrots | thin to 2-3 inches apart | **no count** |
| Two gallon | eggplant | 1 plant | 1 |
| Two gallon | pepper | 2 plants | 2 |
| Two gallon | radishes | thin to 1-2 inches apart | **no count** |
| Three gallon | Standard tomatoes | 1 plant | 1 |

**10 of 14 rows carry a count. Four carry a thinning spacing instead**, which is a different datum
and is not a per-pot capacity. The container size is stated per row and **varies across four
values** (0.5, 1, 2, 3 gallons). This is the fact the field shape has to survive.

### 2.2 University of Maryland: FOUND, contradicting the 2026-09-06 sketch

The sketch says UMD publishes "only narrative counts". It does not. `types-containers-growing-
vegetables` (HTTP 200, 34,659 bytes) states a count against a stated size, verbatim:

> For Large Vegetables-one plant per container. Minimum 8-10 gallons of growing media, with a depth
> of 12-16 inches Examples: tomatoes, pepper, eggplant, cucumber, Winter squash

This is a **size-class** count, not a per-crop one: one count, one size, five named crop groups. The
two other classes on the same page carry a volume and a depth but **no count** ("Medium Vegetables
or Flowering Plants Minimum 4-6 gallons... Small Vegetables or Flowering Plant Minimum 1-3
gallons..."). `maintaining-container-grown-vegetables` (HTTP 200, 36,871 bytes) carries no count.

**UMD contradicts Illinois on the crops they share.** Pepper: Illinois 2 plants at 2 gallons; UMD 1
plant at 8-10 gallons. Cucumber: Illinois 2 at 1 gallon; UMD 1 at 8-10. Same crop, different count,
different size. Neither is wrong; they are different pots. A field that carries a count without the
size it was measured at cannot represent both, and cannot tell a later reader which one it holds.

### 2.3 Wisconsin Horticulture: ABSENT

`hort.extension.wisc.edu/articles/growing-vegetables-containers/`, HTTP 200, 147,888 bytes, no
`<table>`. Full text read. It publishes **volumes and a spacing, and no plant count at all**:
"smaller plants like leaf lettuce, spinach, peas, radishes, cilantro, and green onions require
containers with a volume of at least two gallons and that are at least four to six inches deep";
"Larger plants like tomatoes, peppers, broccoli, eggplants, squash, cucumbers and bush beans require
a container with a minimum volume of five gallons"; and for root vegetables, "be sure to space
plants two to four inches apart". A spacing is not a count. Absent, confirmed from bytes.

### 2.4 Clemson HGIC: UNDETERMINED live, ABSENT on the archived bytes

The live page refuses automated fetches: HTTP **403**, 1,486-byte nginx/Cloudflare body, on two
attempts with different browser headers. That is undetermined, not absent, and it is recorded as
undetermined.

A Wayback snapshot of the same URL was fetched instead (HTTP 200, 204,582 bytes, snapshot
`20250214051543`) and read in full: factsheet HGIC 1251, "Published: Mar 1, 1999". It contains **no
`<table>`, zero occurrences of "gallon", and no plant count**. Its only sizing sentence is "Most
plants need containers at least 6 to 8 inches deep for adequate rooting."

**Absent on the archived bytes; the live page is undetermined.** If the promote wants to rely on
Clemson for anything, it must be fetched by a route that is not blocked, and the snapshot date
recorded. Nothing in this spec depends on Clemson.

### 2.5 The dataset's own prose: 18 crops, and the sketch said 13

Measured on canonical `1721208e`: **18** certified crops carry a count-shaped phrase in
`container_notes` prose, not 13. They matter because they are the tempting shortcut, and three of
them show why the shortcut is unsafe:

- **15 are capacity counts stated with a gallons figure in the same sentence**, e.g. bell-pepper
  "Use at least a 3-gallon pot (5 is better), 12 inches deep, one plant per pot"; kale "a pot of at
  least 3 gallons that is 10 inches or more deep, one or two plants per pot".
- **strawberry binds its count to a diameter, not a volume**: "up to four plants fit in a 12-inch
  pot". A fourth unit.
- **tomatillo's count is not a capacity at all**: "you need at least two plants for them to set
  fruit, so you will need two pots placed close together." That is a pollination *minimum*, the
  semantic opposite of a per-pot *maximum*. A planner that divided by it would be wrong in the
  dangerous direction. **edamame** is a third meaning again: "one plant gives only a handful of
  pods" is a yield note.

And the prose disagrees with Illinois wherever both speak: bell-pepper prose says 1 plant at 3
gallons, Illinois says 2 at 2; swiss-chard prose says 1 at 5 gallons, Illinois says 1 at 1.

**Rule that follows:** our own prose is not a source. A count lifted from `notes_seasoned` is a
number this project wrote, not a number it read, and authoring it into a structured field would
launder authored prose into a cited datum. Every authored value is re-read from the source's bytes
or it is null.

### 2.6 Mapping the counts to slugs

Every Illinois count maps to at least one dataset slug. **No count matches no crop.** But three rows
map ambiguously, and the promote must rule them rather than fan the number out:

| Illinois row | maps to | note |
|---|---|---|
| parsley, cabbages, green beans, leaf lettuce, Swiss chard, eggplant | `parsley`, `cabbage`, `green-beans-bush`, `lettuce-leaf`, `swiss-chard`, `eggplant` | 1:1, unambiguous |
| cherry and patio tomatoes | `cherry-tomato` | `grape-tomato` is a separate slug the row does not name |
| cucumbers | `cucumber`, `english-cucumber`, `pickling-cucumber`, `slicing-cucumber` | **4 slugs.** The row's varieties (Salad Bush, Bush Champion, Spacemaster) are bush slicing types |
| pepper | `bell-pepper` + 4 others | the row's varieties span sweet (Lady Bell, New Ace, Gypsy) and hot (Red Chilli) |
| Standard tomatoes | `beefsteak-tomato`, `heirloom-tomato`, `roma-tomato`? | "Standard" names no slug; Jetstar/Celebrity/Super Bush are slicers, roma is paste |

**Certified crops with no count anywhere: 86** of the 110 that are `container_ok: true` (full list in
section 12). Among them are `beet`, `carrot`, `radish` and `spinach`, which Illinois *does* have a
row for but gives a thinning spacing rather than a count. They get null, and the reason is recorded:
a thinning spacing is not a capacity.

---

## 3. D1, unit binding: carry the source's own gallons. RECOMMENDED

**Measured.** Per-plant gallons under each candidate binding, for the counted rows:

| Illinois row | IL size | count | slug | `min_pot_gallons` | `rec_pot_gallons` | source says per plant | min-bound says | rec-bound says |
|---|---|---|---|---|---|---|---|---|
| parsley | 0.5 | 1 | parsley | 1 | 2 | 0.50 | 1.00 | 2.00 |
| cabbages | 1 | 1 | cabbage | 5 | 10 | 1.00 | 5.00 | 10.00 |
| cucumbers | 1 | 2 | cucumber | 5 | 10 | 0.50 | 2.50 | 5.00 |
| green beans | 1 | 2-3 | green-beans-bush | 5 | 5 | 0.33 | 1.67 | 1.67 |
| leaf lettuce | 1 | 4-6 | lettuce-leaf | 1 | **None** | 0.17 | 0.17 | n/a |
| Swiss chard | 1 | 1 | swiss-chard | 3 | 5 | 1.00 | 3.00 | 5.00 |
| cherry/patio tomatoes | 1 | 1 | cherry-tomato | 5 | 10 | 1.00 | 5.00 | 10.00 |
| eggplant | 2 | 1 | eggplant | 5 | 7 | 2.00 | 5.00 | 7.00 |
| pepper | 2 | 2 | bell-pepper | 3 | 5 | 1.00 | 1.50 | 2.50 |
| Standard tomatoes | 3 | 1 | beefsteak-tomato | 15 | 20 | 3.00 | 15.00 | 20.00 |

**Bind to `min_pot_gallons`: rejected.** It reproduces the source on exactly one row (leaf lettuce,
and only because 1 gallon happens to equal its minimum). Everywhere else it invents a per-plant
volume neither the source nor the dataset states, off by 1.5x to 5x. Worse, it is not merely an
internal number: plant-app renders `${count} in a ${minGallons} gallon pot`
(`src/lib/container-model.ts:256`), so the binding becomes a **printed sentence**. Green beans would
read "2 to 3 in a 5 gallon pot". Illinois said 2-3 in a **one**-gallon pot. That sentence would be
this project's own invention, presented to a grower as a sourced fact.

**Bind to `recommended_pot_gallons`: rejected, harder.** 95 of 121 certified crops carry it, and the
7 that carry `min_pot_gallons` without it include **`lettuce-leaf`** -- the flagship count crop, the
one worked example in the 2026-09-06 sketch and the reason PLA-580 exists. A binding that strands
its own motivating case is not a binding. (The other six: orange-navel, mandarin-clementine,
mulberry, grapefruit, cherry-sweet, cherry-sour.)

**Carry the source's own gallons: RECOMMENDED.** The count and the size it was measured at are one
datum and travel together:

```jsonc
"plants_per_pot": {
  "count": [4, 6],
  "at_gallons": 1,
  "sources": ["uiuc_ext"],
  "anchoring_urls": {
    "uiuc_ext": {
      "url": "https://extension.illinois.edu/container-gardens/growing-vegetables-containers",
      "verified": "2026-09-21"
    }
  }
}
```

Four properties earn it:

1. **It is the only shape that can hold the conflict.** Illinois' pepper (2 at 2 gal) and UMD's
   pepper (1 at 8-10 gal) are both true and are different pots. A bare `[min, max]` has to pick one
   and cannot say which it picked.
2. **It fails safe into today's behavior.** plant-app's parser
   (`plantsPerPotOf`, `container-model.ts:98`) returns `null` for anything that is not a 2-element
   integer array. Ship an object and the existing app reads `null`, which means one plant per pot:
   **exactly the behavior it has now**. Ship a bare array, and the same already-deployed code
   silently divides `min_pot_gallons` and starts printing the invented sentence the day the data
   lands. The object shape makes the ordering error impossible; the array shape makes it the
   default. This is the decisive argument.
3. **It carries its own sources.** Measured: the Illinois table page is **not** an anchoring URL
   anywhere in `container_notes` today (the three `uiuc_ext` container anchors are the drainage
   page, asparagus and lemongrass). Adding it to the block-level `sources` would assert it sourced
   the whole block, which it did not. The sibling-field pattern that `critical_warnings` uses in the
   2026-09-06 spec applies unchanged.
4. **It keeps `min_pot_gallons` meaning what it already means.** No re-reading of 102 pot figures,
   no retroactive redefinition, and PLA-533's audit of that field stays independent of this one.

**Sub-rule, one unit only.** `at_gallons` is gallons. A count published only against a diameter
(strawberry's "up to four plants fit in a 12-inch pot") is **not authored in this field**; it stays
in prose. One unit, no converter, no inferred volume from a diameter.

**Bounds note.** `at_gallons` must admit **0.5** (Illinois' parsley row). The existing
`numeric_sanity` bounds for `min_pot_gallons` / `recommended_pot_gallons` are `1..100`
(`tools/numeric_sanity_gate.py:66-67`); this field's floor is lower on purpose, and section 6 says so.

---

## 4. D2, meaning: a per-pot capacity at a stated size. RECOMMENDED

**The meaning.** `count` is the number of plants of this crop that the cited source says a pot of
`at_gallons` holds to maturity. It is a **capacity at a stated size**, not a density, not a minimum,
not a yield note. Explicitly excluded, with the measured examples that forced each exclusion:

- a **pollination minimum** (tomatillo, "you need at least two plants"): not a capacity, opposite
  sign;
- a **yield note** (edamame, "one plant gives only a handful of pods");
- a **thinning spacing** (Illinois' spinach, beets, carrots, radishes rows);
- a count bound to a **diameter** (strawberry).

**What the PLA-409 planner needs, read from the code rather than assumed.** plant-app
`src/lib/planner/rootstock.ts:103-118`:

```ts
const perPot = rs?.containerGallons ?? crop.containerMinGallons;
if (perPot == null) return null;
const share = crop.containerPlantsPerPot ? crop.containerPlantsPerPot[1] : 1;
const per = perPot / share;
return crop.isWoody ? per : per * planting.count;
```

Its input is **one number: gallons drunk per plant.** It gets there today by dividing
`min_pot_gallons` by the count's upper bound. Under this spec it should instead read
`at_gallons / count[max]` directly and **not touch `min_pot_gallons` at all**. For leaf lettuce that
is `1 / 6 = 0.17` gallons per plant, and a 5-gallon pot stops charging 5 gallons for one lettuce.

**Correcting the sketch's arithmetic, since PLA-580 quotes it.** The 2026-09-06 spec says the field
"changes a 2-gallon-per-plant charge to roughly a third of a gallon". Measured: `lettuce-leaf`'s
`min_pot_gallons` is **1**, not 2, so today's charge is 1 gallon; and the result is **0.17**, not
0.33. Neither end of that sentence matches the dataset or the source. The likely origin of the "2"
is Wisconsin's "at least two gallons" for small plants, which is not the figure the dataset carries.
The app's own fixture repeats the error (`catalog.container.test.ts:52` builds lettuce with
`containerMinGallons: 2`).

**How much this actually moves, stated plainly.** A count of 1 divides by 1 and changes nothing.
**Six of the ten** Illinois counts are 1. Across every source read, the crops where this field
changes a planner number at all are: cucumber (2), green beans (2-3), leaf lettuce (4-6), pepper (2)
from Illinois, and kale (1-2) from prose if it is ever re-read at T1. That is **four to five crops
of 121**. The field is still worth having -- it is published, it is true, it renders as a row, and
leaf lettuce alone is a 6x error today -- but nobody should expect the planner to transform. If the
arc wants a broader effect, the lever is not this field.

**Extrapolation is the consumer's inference, not the dataset's.** The source says 4-6 lettuce in a
1-gallon pot. It does not say 30 in a 5-gallon pot. The dataset records the datum at its stated
size; any scaling beyond that is the planner's, and the planner should say so rather than the
dataset implying it.

---

## 5. D3, presence-or-null. CONFIRMED against A39 and the register

**The rule:** `container_notes.plants_per_pot` is present on all **121 certified** crops, `null`
where no T1 count exists. The **7 shells carry no key** and stay byte-identical.

**Confirmed, not assumed.** Measured on `1721208e`: the 7 shells (avocado, olive, and the five
mushrooms) carry a `container_notes` block of 22-24 keys but **`'container_path' in cn` is `False`**
on all 7. A39 (`register_coverage_gate`, wired as whole_crop_gate A39) exempts uncertified
`verified_gs_arc` misses by **key absence**, which is how the A1 promote left the shells
byte-identical. `plants_per_pot` follows the identical pattern, and the register row for
`container_path` (row **29**) is its precedent. Row **30** is PLA-465's plant dimensions; this field
takes row **31**.

Population at land: 121 keys written, of which the authorable set is section 8's, and the rest null.

---

## 6. D4, armor

- **Shape gate, whole_crop_gate `A60`** (A58 is `container_path`, A59 is `plant_dimensions`; A60 is
  the next free id, measured). New `tools/plants_per_pot_gate.py` + tests, TDD, wired the way A58
  was: shape armed on the tooling commit, the **presence floor behind `A60_PRESENCE_ARMED = False`
  until the commit that writes canonical**.
  Rules: value is `null` or an object; object keys exactly
  `{count, at_gallons, sources, anchoring_urls}`; `count` is `[min, max]` integers with
  `1 <= min <= max`; `at_gallons` is a positive number; `sources` non-empty and every key present in
  `anchoring_urls` with a `url` and a `verified` date; **`plants_per_pot` non-null requires
  `container_ok: true`** (a crop that cannot go in a pot has no per-pot capacity); and the key is
  **absent** on every uncertified shell.
- **`numeric_sanity_gate`:** `count[max] <= 30`; `at_gallons` in `[0.5, 100]`. The 0.5 floor is
  deliberate and differs from the `1..100` that `min_pot_gallons` and `recommended_pot_gallons` use
  at `numeric_sanity_gate.py:66-67`, because Illinois publishes a half-gallon row. A comment says so
  at the bound, or a later reader will "fix" it.
- **Cross-field coherence, fails LOUD:** `at_gallons` is **not** required to equal or exceed
  `min_pot_gallons`, and the gate must not assert it. Measured, that assertion would fail on 9 of 10
  authored rows -- it is the very confusion this spec exists to prevent. What the gate *does* check
  is that `at_gallons` is present whenever `count` is.
- **`register_completeness`:** `plants_per_pot` is structured, not prose; no register pair.
- **`field_additions` provenance:** one record per authored value, carrying the source's raw bytes
  evidence -- URL, fetch date, sha256 and the **verbatim row or sentence** the count was copied
  from. The EVIDENCE_HASHES guard from PLA-465 applies: no 64-hex token in the promote spec that is
  not a measured digest.
- **Suite + mutation harness, PLA-215:** one mutation per guard family, MUTATION-APPLIED marker +
  sentinel, `set(pre) == set(post)` before value comparison, refusal-spec passes for good input,
  suite replay-pinned via `promote_fixture.COMMIT_FOR`. **Positive control runs the whole suite.**
  Guards that cannot be shown reachable are removed, not shipped as coverage.
- **Release:** gate_all 121/121, A60 presence 0 violations, `register_completeness` +
  `register_coverage` PASS, `release_verify` clean in every section, collision gate holding.

---

## 7. D5, consumers. CONFIRMED by reading both repos, not assumed

**plant-app: already built, and that is the hazard.** The consumer is wired end to end today, on
`feat/community-foundation` at `a7f6288c`:

| file | what it does now |
|---|---|
| `src/lib/container-model.ts:98` | `plantsPerPotOf` parses `cn.plants_per_pot`, requiring a 2-element integer array; anything else is `null` |
| `src/lib/container-model.ts:198` | sets `plantsPerPot` on `ContainerFacts` |
| `src/lib/container-model.ts:250-267` | renders a seasoned-only row, "Plants per pot", text `"${count} in a ${f.minGallons} gallon pot"` |
| `src/lib/planner/catalog.ts:151` | maps it to `containerPlantsPerPot` |
| `src/lib/planner/rootstock.ts:112` | `share = containerPlantsPerPot[1]`, divides `min_pot_gallons` |

A code comment at `container-model.ts:253` already says "latent today -- no crop ships
plants_per_pot yet". **This field's consumer therefore ships before its data, which inverts the
usual risk**: the frontend-first rule is already satisfied, but the built frontend implements the
binding this spec rejects. Under the recommended object shape it reads `null` and keeps today's
behavior until it is changed deliberately. Under a bare array it would be wrong on day one. The app
changes owed: read `at_gallons` for the divisor, and render the source's size in the row rather than
`minGallons`.

**plant-astro: not built.** Measured: **no ContainerCard exists** and `plants_per_pot` /
`plantsPerPot` appear **nowhere** in `src/`. `container_notes` is read only by
`CareGuideCard.astro` (`${min_pot_gallons}+ gal pot`), `HeroCard.astro` (value
`${recommended_pot_gallons} gal`, sub `min ${min_pot_gallons} gal pot`) and `lib/containers.ts` for
the beds tool. Worth flagging for the arc: the two consumers already disagree about which pot figure
is the headline -- astro's hero leads with `recommended_pot_gallons`, the app's planner computes
from `min_pot_gallons`. A count bound to either would inherit that disagreement, which is a third
argument for carrying its own.

**Export allowlist: confirmed, no change needed.** `container_notes` is present in `SHIP_TOP_LEVEL`
(`scripts/export-projection.mjs:44`), so a new subkey ships with no projection change. PLA-580's
item 4 is closed.

---

## 8. The authorable population, and what the promote still has to rule

From Illinois, unambiguous and ready to author (7 crops): `parsley` 1 @ 0.5; `cabbage` 1 @ 1;
`green-beans-bush` 2-3 @ 1; `lettuce-leaf` 4-6 @ 1; `swiss-chard` 1 @ 1; `cherry-tomato` 1 @ 1;
`eggplant` 1 @ 2.

Held for an authoring read in the promote, each with its ambiguity named in section 2.6:
`cucumber` and its three siblings; `bell-pepper` and the four other pepper slugs; the "Standard
tomatoes" row against `beefsteak-tomato` / `heirloom-tomato` / `roma-tomato`.

UMD's size-class row is authorable in principle (1 @ 8-10 gallons for tomatoes, pepper, eggplant,
cucumber, winter squash) but `at_gallons` is a **range** there, not a point, and it conflicts with
Illinois on two crops. Recommendation: **do not author from UMD in this pass**. Take the per-crop
table where it speaks, leave the rest null, and record UMD's row in the promote document as a known
second reading rather than silently preferring one source over the other.

The 18 prose crops are **not** authorable from the prose (section 2.5). If the arc wants them, each
needs its own T1 read against the source the block already cites, which is a separate pass.

---

## 9. Sequencing, and the one ordering hazard

1. **Now:** this spec, held for Trevor's read. No promote.
2. **plant-app first**, if a bare array is ever chosen over the object: the divisor and the rendered
   sentence must change *before* any data lands. Under the recommended object shape this ordering is
   enforced by the shape itself and the app can be changed at leisure.
3. **Promote:** A60 gate (shape armed, presence floor disarmed), suite, harness, the authoring reads
   in section 8, `field_additions` records, gauntlet on a scratch post-state, HOLD for approval, then
   the canonical write with `--expect-sha` and `A60_PRESENCE_ARMED = True` in the same commit.
4. **plant-astro:** a ContainerCard has to exist before this renders there at all. That is the
   2026-09-06 spec's section 6 work, unstarted.
5. **Close PLA-580** with the record: the binding, the population, and the four-to-five-crop honest
   scope of the planner effect.

---

## 10. Out of scope, by name

`min_pot_gallons` semantics and PLA-533's provenance audit of the 102 figures; the strawberry
diameter count and any diameter-to-volume conversion; the 18 prose counts as an authoring source;
UMD's size-class model as a dataset shape; `critical_warnings` (PLA-7 Plan D); the 88 unmatched
cultivar names (Plan B); whether the planner should extrapolate a density beyond `at_gallons`.

---

## 11. The open question for Trevor

Section 8 recommends taking Illinois where it is unambiguous and leaving UMD's conflicting size-class
row unauthored. The alternative is to carry both, which the object shape *can* hold (a list of
readings rather than one), at the cost of a consumer that has to choose. **Recommendation: one
reading per crop for now**, because no consumer is built to choose and a list would ship a decision
nobody has made. Raised here rather than decided because it is a product call about how much
disagreement to show a grower.

---

## 12. Measured facts this rests on (2026-09-21, canonical `1721208e`)

**Preflight.** `shasum -a 256 crops_data_final.json` =
`1721208ee0cbe4249ecf32ca3bd47a786f8a689cadcb7bb300d8d8ada4d82054`, matching LATEST.txt.
`origin/main` = `21a43f0e29e946dd4d956be2bd331ea9d81dff3c`.

**Source fetches.** All 2026-09-21.

| source | URL | result | bytes | sha256 |
|---|---|---|---|---|
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/growing-vegetables-containers` | 200 | 28,754 | `f9f336d5eb33a1dc0833f53d98b2e909cf2d6ce920795dc8913fab94de393119` |
| `uwi_hort` | `https://hort.extension.wisc.edu/articles/growing-vegetables-containers/` | 200 | 147,888 | `7847f46653318ae5d12ca24f8595e3b6ab056e8cf15252e301b95bc63ccf8c33` |
| `umd_ext` | `https://extension.umd.edu/resource/types-containers-growing-vegetables` | 200 | 34,659 | `96521c5d0cf8860e7895a8c6da426ac48a372894c531431c64666bda8151f407` |
| `umd_ext` | `https://extension.umd.edu/resource/maintaining-container-grown-vegetables` | 200 | 36,871 | `e2ad3acfec22c992888eaabbd7185d86f241ab8cae3b63aae35bf95cd62963ac` |
| `clemson_hgic` | `https://hgic.clemson.edu/factsheet/container-vegetable-gardening/` | **403** (2 attempts) | 1,486 (error body) | n/a |
| `clemson_hgic` | `https://web.archive.org/web/20250214051543/https://hgic.clemson.edu/factsheet/container-vegetable-gardening/` | 200 | 204,582 | `4b4dd8d59860c6ffeef2745c2f72ac886a3f03f98e1225ea050fbd6fdc211f01` |

**Dataset.** 128 crops; **121** `verified_gs_arc`, **7** with `verification_status: null` (avocado,
olive, oyster-/shiitake-/lions-mane-/wine-cap-/button-mushroom). `plants_per_pot`: **0** occurrences
dataset-wide (byte count on the canonical file). `container_ok: true`: **110** of 121 certified.
`min_pot_gallons` present: **102**; `recommended_pot_gallons` present: **95**; both: **95**; min
without recommended: **7** (`lettuce-leaf`, `orange-navel`, `mandarin-clementine`, `mulberry`,
`grapefruit`, `cherry-sweet`, `cherry-sour`). `'container_path' in container_notes` is `False` on
all 7 shells. Certified crops that are `container_ok: true` with no count in any source read: **86**.
Certified but not `container_ok`: **11** (apricot, asparagus, field-corn, flint-corn, nectarine,
pawpaw, peach, persimmon, plum, popcorn, sweet-corn).

**Register / gates.** `docs/field_addition_register.md` holds 30 rows; 29 is `container_path`, 30 is
plant dimensions; this field is 31. Highest whole_crop_gate id in `tools/whole_crop_gate.py` is
**A59**; A60 is free. `numeric_sanity_gate.py:66-67` bounds `min_pot_gallons` and
`recommended_pot_gallons` at `1..100`.

**Consumers.** plant-app `feat/community-foundation` @ `a7f6288c`: `container-model.ts` lines 98,
198, 250-267; `planner/catalog.ts:151`; `planner/rootstock.ts:103-118`; `planner/types.ts:39`;
`container_notes` in `SHIP_TOP_LEVEL` at `export-projection.mjs:44`. plant-astro @ `aa17dff`: no
ContainerCard, no `plants_per_pot` reference; `container_notes` read in `CareGuideCard.astro:101`,
`HeroCard.astro:165-167`, `lib/containers.ts`.

**Discrepancies recorded against the 2026-09-06 spec.** (a) UMD publishes a count against a stated
size; the spec says it carries narrative counts only. (b) The prose-count population is 18, not 13.
(c) The lettuce worked example's arithmetic matches neither the dataset (`min_pot_gallons` is 1, not
2) nor the source (0.17, not 0.33). (d) PLA-580's summary line renders `min_pot_gallons` semantics as
"per plant"; the spec's own section 4 says a pot holding `plants_per_pot` plants. The app implements
the spec, not the summary.
