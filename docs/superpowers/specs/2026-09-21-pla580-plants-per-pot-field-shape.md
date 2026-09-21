# `container_notes.plants_per_pot`: field-shape spec (PLA-580, PLA-7 Plan C)

**Date:** 2026-09-21. **Canonical:** `1721208e` (unchanged by this document; no promote, no data
change). **Branch:** `worktree-pla580`, spec commits only.
**Supersedes, in part:** the two-paragraph sketch in
`docs/superpowers/specs/2026-09-06-pla7-container-field-shape-design.md` section 4 item 2. Where
this document and that one disagree, the disagreement is named in section 2 and the measurement is
given. **Read with:** PLA-580, PLA-7 (D3), PLA-409, PLA-533, PLA-539, PLA-586, PLA-10.

**Amendment history.** First draft 2026-09-21. **Amendment 1** (same day, Trevor's read): one
correction he caught (section 4.1) and six rulings, listed in 3.1. **Amendment 2** (same day, his
read of amendment 1): four further amendments, listed in 3.2, of which the largest is that the
planner's extrapolation beyond a reading's own pot size is **modeled, not sourced**, and is written
down as such.

**The headline.** The 2026-09-06 sketch assumed a count could be bound to `min_pot_gallons`. It
cannot. Measured against raw bytes, the dataset's `min_pot_gallons` disagrees with the pot size
Illinois states its counts against on **9 of 10** counted rows, by factors from 1.5x to 5x. The one
row that agrees is leaf lettuce, which is the row the sketch worked its example on. A count carried
without its own pot size is not a datum, and the consumer that would read it is already built and
would already render the error.

**The second headline.** Switching the planner to the new field is **not** direction-neutral.
Measured, **every one of the ten Illinois readings is more permissive than `min_pot_gallons`**, by
2.0x to 10.0x, with no exceptions. That is the dangerous direction, and it is why ruling 3 holds the
switch to `count > 1` rows. Section 5.2 records what that unbroken pattern may mean, as a hypothesis
for PLA-533 rather than a conclusion.

---

## 1. What this adds, in one table

| field | where | shape | who authors | who reads |
|---|---|---|---|---|
| `plants_per_pot` | `container_notes` | object `{readings: [{count: [min, max], at_gallons: [lo, hi], sources, anchoring_urls}, ...]}`, or `null` | PLA-580 promote, roster-wide, null where no T1 count exists | plant-app planner (`plantingGallons`) + the "In a pot" chapter row; plant-astro ContainerCard (PLA-586) |

No other field is added. `min_pot_gallons` and `recommended_pot_gallons` are not touched, not
re-read and not re-derived by this arc. PLA-533 owns the audit of the former.

---

## 2. The reads, from raw bytes (found / absent / undetermined)

All four sources fetched 2026-09-21. Byte counts, sha256 digests and the exact fetch results are in
section 13. Every quotation below is copied from those bytes.

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

**Note the four spacing rows are the same signal as amendment 2's first point.** Where Illinois
declines to give a count it gives a spacing, which is an area measure. That is consistent with
capacity in a pot being governed by surface area and spacing rather than by volume, and it is part
of why section 4.4 refuses to treat the volume scaling as sourced.

### 2.2 University of Maryland: FOUND, contradicting the 2026-09-06 sketch

The sketch says UMD publishes "only narrative counts". It does not. `types-containers-growing-
vegetables` (HTTP 200, 34,659 bytes) states a count against a stated size, verbatim:

> For Large Vegetables-one plant per container. Minimum 8-10 gallons of growing media, with a depth
> of 12-16 inches Examples: tomatoes, pepper, eggplant, cucumber, Winter squash

This is a **size-class** count, not a per-crop one: one count, one size band, five named crop
groups. The two other classes on the same page carry a volume and a depth but **no count** ("Medium
Vegetables or Flowering Plants Minimum 4-6 gallons... Small Vegetables or Flowering Plant Minimum
1-3 gallons..."). `maintaining-container-grown-vegetables` (HTTP 200, 36,871 bytes) carries no count.

**UMD contradicts Illinois on the crops they share.** Pepper: Illinois 2 plants at 2 gallons; UMD 1
plant at 8-10 gallons. Cucumber: Illinois 2 at 1 gallon; UMD 1 at 8-10. Same crop, different count,
different size. Neither is wrong; they are different pots. Under ruling 1 the field holds both.

UMD's "Minimum 8-10 gallons" is the only genuinely banded size in either source; under amendment 3
it is encoded `[8, 10]` and every Illinois point size is encoded `[n, n]`.

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
  pot". A fourth unit, and another area signal.
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

Every Illinois count maps to at least one dataset slug. **No count matches no crop.** But three
Illinois rows map ambiguously, and **four of UMD's five named groups are category names, not crop
names**, which is the same ambiguity:

| source row | maps to | ruling |
|---|---|---|
| IL parsley, cabbages, green beans, leaf lettuce, Swiss chard, eggplant | `parsley`, `cabbage`, `green-beans-bush`, `lettuce-leaf`, `swiss-chard`, `eggplant` | 1:1, authored |
| IL cherry and patio tomatoes | `cherry-tomato` | authored; `grape-tomato` is a separate slug the row does not name |
| IL cucumbers | `cucumber`, `english-cucumber`, `pickling-cucumber`, `slicing-cucumber` | **HELD** (ruling 5) |
| IL pepper | `bell-pepper` + 4 others; varieties span sweet and hot | **HELD** (ruling 5) |
| IL Standard tomatoes | names no slug | **UNAUTHORED** (ruling 5) |
| UMD eggplant | `eggplant` | 1:1, authored |
| UMD tomatoes, pepper, cucumber, Winter squash | 5 / 5 / 4 / 3-4 slugs each | **HELD**, same rule |

**Certified crops with no count anywhere: 86** of the 110 that are `container_ok: true` (full list in
section 13). Among them are `beet`, `carrot`, `radish` and `spinach`, which Illinois *does* have a
row for but gives a thinning spacing rather than a count. They get null, and the reason is recorded:
a thinning spacing is not a capacity.

---

## 3. D1, unit binding: carry the source's own gallons. RULED

**Measured.** Per-plant gallons under each candidate binding, for the counted rows:

| Illinois row | IL size | count | slug | `min_pot_gallons` | `rec_pot_gallons` | source says per plant | min-bound says | rec-bound says |
|---|---|---|---|---|---|---|---|---|
| parsley | 0.5 | 1 | parsley | 1 | 2 | 0.50 | 1.00 | 2.00 |
| cabbages | 1 | 1 | cabbage | 5 | 10 | 1.00 | 5.00 | 10.00 |
| cucumbers | 1 | 2 | cucumber | 5 | 10 | 0.50 | 2.50 | 5.00 |
| green beans | 1 | 2-3 | green-beans-bush | 5 | 5 | 0.50 | 2.50 | 2.50 |
| leaf lettuce | 1 | 4-6 | lettuce-leaf | 1 | **None** | 0.25 | 0.25 | n/a |
| Swiss chard | 1 | 1 | swiss-chard | 3 | 5 | 1.00 | 3.00 | 5.00 |
| cherry/patio tomatoes | 1 | 1 | cherry-tomato | 5 | 10 | 1.00 | 5.00 | 10.00 |
| eggplant | 2 | 1 | eggplant | 5 | 7 | 2.00 | 5.00 | 7.00 |
| pepper | 2 | 2 | bell-pepper | 3 | 5 | 1.00 | 1.50 | 2.50 |
| Standard tomatoes | 3 | 1 | beefsteak-tomato | 15 | 20 | 3.00 | 15.00 | 20.00 |

(Per amendment 4, every figure here divides by `count[min]`, the conservative end.)

**Bind to `min_pot_gallons`: rejected.** It reproduces the source on exactly one row (leaf lettuce,
and only because 1 gallon happens to equal its minimum). Everywhere else it invents a per-plant
volume neither the source nor the dataset states. Worse, it is not merely an internal number:
plant-app renders `${count} in a ${minGallons} gallon pot` (`src/lib/container-model.ts:256`), so
the binding becomes a **printed sentence**. Green beans would read "2 to 3 in a 5 gallon pot".
Illinois said 2-3 in a **one**-gallon pot. That sentence would be this project's own invention,
presented to a grower as a sourced fact.

**Bind to `recommended_pot_gallons`: rejected, harder.** 95 of 121 certified crops carry it, and the
7 that carry `min_pot_gallons` without it include **`lettuce-leaf`** -- the flagship count crop, the
one worked example in the 2026-09-06 sketch and the reason PLA-580 exists. A binding that strands
its own motivating case is not a binding. (The other six: orange-navel, mandarin-clementine,
mulberry, grapefruit, cherry-sweet, cherry-sour.)

**Carry the source's own gallons: RULED (ruling 1).** The count and the size it was measured at are
one datum and travel together, and a crop may hold more than one such datum:

```jsonc
"plants_per_pot": {
  "readings": [
    {
      "count": [4, 6],
      "at_gallons": [1, 1],
      "sources": ["uiuc_ext"],
      "anchoring_urls": {
        "uiuc_ext": {
          "url": "https://extension.illinois.edu/container-gardens/growing-vegetables-containers",
          "verified": "2026-09-21"
        }
      }
    }
  ]
}
```

Four properties earn it:

1. **It is the only shape that can hold the conflict.** Illinois' pepper (2 at 2 gal) and UMD's
   pepper (1 at 8-10 gal) are both true and are different pots. A bare `[min, max]` has to pick one
   and cannot say which it picked. The `readings` array holds both, which ruling 1 requires as a
   shape the field must carry before PLA-12 starts adding sources.
2. **It fails safe into today's behavior.** plant-app's parser
   (`plantsPerPotOf`, `container-model.ts:98`) opens with
   `if (!Array.isArray(v) || v.length !== 2) return null;` at line 100. An object literal fails
   `Array.isArray`, so the already-deployed app reads **null**, which means one plant per pot:
   **exactly the behavior it has now**. Ship a bare array and the same code silently divides
   `min_pot_gallons` and starts printing the invented sentence the day the data lands. The object
   shape makes the ordering error impossible; the array shape makes it the default. This is the
   decisive argument.
   *Confirmed by reading the guard, not by executing it.* The existing table test
   (`container-model.test.ts:109-117`) covers a string and `undefined` but **not an object**; the
   regression test that closes this is noted on PLA-539.
3. **It carries its own sources.** Measured: the Illinois table page is **not** an anchoring URL
   anywhere in `container_notes` today (the three `uiuc_ext` container anchors are the drainage
   page, asparagus and lemongrass). Adding it to the block-level `sources` would assert it sourced
   the whole block, which it did not. The sibling-field pattern that `critical_warnings` uses in the
   2026-09-06 spec applies unchanged, and per-reading sources are what let two readings cite
   different institutions.
4. **It keeps `min_pot_gallons` meaning what it already means.** No re-reading of 102 pot figures,
   no retroactive redefinition, and PLA-533's audit of that field stays independent of this one.

**Sub-rule, one unit only.** `at_gallons` is gallons. A count published only against a diameter
(strawberry's "up to four plants fit in a 12-inch pot") is **not authored in this field**; it stays
in prose. One unit, no converter, no inferred volume from a diameter.

### 3.1 Trevor's rulings, amendment 1

| # | ruling | applied in |
|---|---|---|
| 1 | Shape is `{readings: [...]}`; author UMD alongside Illinois where both exist, not as a recorded second reading | 1, 3, 6, 9 |
| 2 | On conflicting readings the planner uses the **most conservative** (largest gallons per plant) | 4.3, 5 |
| 3 | The planner switches **only where `count > 1`**; count-1 rows keep `min_pot_gallons` until PLA-533 audits it | 4.2, 5 |
| 4 | Display renders a reading's own `at_gallons` with its count, never `min_pot_gallons` | 7.1 |
| 5 | The three ambiguous rows stay held; "Standard tomatoes" stays unauthored | 2.6, 9 |
| 6 | plant-astro's card is PLA-586; state what it must read, matching the app card's contract | 7.3 |

### 3.2 Trevor's amendments, amendment 2

| # | amendment | applied in |
|---|---|---|
| 1 | Extrapolation beyond `at_gallons` is a **MODELED app rule**, stated in the consumer contract and never implied to be sourced; no rendered sentence states a count at a pot size no source named; capacity-by-area routed to PLA-10 | 4.4, 5.1, 7.1, 7.2, 11 |
| 2 | The unbroken permissive direction is recorded as a **hypothesis for PLA-533**, not a conclusion: it is consistent with `min_pot_gallons` being a minimum pot for the crop rather than a per-plant volume, which would make PLA-409's per-plant reading the original error | 5.2 |
| 3 | `at_gallons` is **always `[lo, hi]`**, `lo == hi` for a single size. One type per field. The conservative reader takes `hi` | 1, 3, 6, 8 |
| 4 | The planner divides by **`count[min]`**, the conservative end. This is the contract; the first draft's `count[max]` is superseded | 4.2, 8 |

---

## 4. D2, meaning: a per-pot capacity at a stated size. RULED

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

Its input is **one number: gallons drunk per plant.**

**Correcting the sketch's arithmetic, since PLA-580 quotes it.** The 2026-09-06 spec says the field
"changes a 2-gallon-per-plant charge to roughly a third of a gallon". Measured: `lettuce-leaf`'s
`min_pot_gallons` is **1**, not 2, so today's charge is 1 gallon; and the conservative result is
**0.25**, not 0.33. Neither end of that sentence matches the dataset or the source. The likely
origin of the "2" is Wisconsin's "at least two gallons" for small plants, which is not the figure
the dataset carries. The app's own fixture repeats the error
(`catalog.container.test.ts:52` builds lettuce with `containerMinGallons: 2`).

### 4.1 CORRECTION: "dividing by 1 changes nothing" was wrong

The first draft of this spec, and the session summary that went with it, said six of the ten
Illinois counts are 1 and that "dividing by 1 changes nothing". **That is false under this spec's
own D2.** It is true only under the rejected `min_pot_gallons` binding, where a count of 1 returns
`min_pot_gallons` unchanged. Once the planner reads `at_gallons / count`, a count-1 row returns
**`at_gallons`**, which is a different number from `min_pot_gallons` on 9 of 10 rows, by the same
1.5x to 5x this spec was written to expose. A count of 1 changes the planner as much as any other
count. Section 5 measures every row.

### 4.2 The formula, and the switch predicate (rulings 3 and 4, amendment 4)

**The contract, stated once and unambiguously:**

```
conservative gallons per plant for one reading = at_gallons[hi] / count[min]
```

`at_gallons[hi]` is the roomier end of a banded size; `count[min]` is the smaller capacity claim. A
pot Illinois says holds "4-6" lettuce is therefore priced as if it holds **4**, not 6. **Amendment 4
makes `count[min]` the contract**; the first draft's `count[max]` is superseded, and the app's
current `containerPlantsPerPot[1]` at `rootstock.ts:112` is on the wrong end and must change.

The planner uses the field **only when a crop has at least one reading whose `count` is not
`[1, 1]`**. Otherwise it keeps `min_pot_gallons`, exactly as today. A reading of `[1, 2]` is not a
count-1 row and does switch.

The reason is ruling 3's: on a count-1 row the field carries no capacity information the planner did
not already have (one plant, one pot), so the only thing switching would do is **replace an
unaudited number with a different unaudited number, in the more permissive direction**. PLA-533
owns the audit of `min_pot_gallons`; until it reports, this arc does not quietly overwrite its
output. Section 5 shows the switch would be more permissive on **all seven** unambiguous count-1
readings, which is what makes the hold worth having.

### 4.3 Conflicting readings (ruling 2)

Where a crop carries more than one reading, the planner takes the **largest** conservative per-plant
figure across all of them, count-1 readings included. Count-1 readings do not trigger the switch
(4.2) but they do participate in the maximum once some other reading has triggered it. That ordering
matters: it is what lets UMD's cautious 10 gallons per plant restrain Illinois' 1.00 on pepper,
rather than being ignored because its count happens to be 1.

**Honest note: ruling 2 is currently inert.** Measured, the only crop carrying two unambiguous
readings after ruling 5's holds is **eggplant**, and both of its readings are count-1, so ruling 3
keeps `min_pot_gallons` and the maximum is never taken. The rule is correct and it is what PLA-12
will need; it changes no number in this pass. The harness therefore exercises it on a **synthetic
fixture** (section 8), since no authored crop does.

### 4.4 Extrapolation beyond `at_gallons` is MODELED, not sourced (amendment 1)

A source states a capacity **at the pot it names**. Illinois says a one-gallon pot holds 4-6 leaf
lettuce. It does not say what a five-gallon pot holds. When the planner prices a five-gallon pot at
`at_gallons[hi] / count[min]` per plant and concludes it holds twenty lettuces, **that conclusion is
this project's model, not Illinois' claim.** The model assumes capacity is linear in root volume.

**That assumption is probably wrong for multi-plant crops.** For plants grown several to a pot the
binding constraint is usually **surface area and spacing**, not volume: a pot twice as deep does not
hold twice as many lettuces. The dataset's own sources point the same way. Illinois declines to give
a count on exactly the four crops where it gives a **thinning spacing** instead (spinach, beets,
carrots, radishes), Wisconsin's only per-plant number for root crops is a **spacing** ("two to four
inches apart"), and strawberry's prose count is bound to a **diameter**. Three sources reach for an
area measure the moment the question becomes "how many".

**Therefore:**

- The extrapolation is **an app rule, recorded as modeled** in the consumer contract (7.2). It is
  not a dataset claim, it is not sourced, and no document in this arc may present it as either.
- **No rendered sentence may state a count at a pot size no source named** (7.1). The card shows the
  reading at its own size, attributed. The planner may still price an arbitrary pot, because that is
  what a planner does, but it does so as a model and never as a quotation.
- **Capacity-by-area is routed to PLA-10** (ground spacing and layout methods), recorded there as a
  question for that arc's field shape: whether a per-plant area, which PLA-10 is already modeling
  for beds and rows, is the correct governing constraint for multi-plant pots as well. It is not
  this field's question and this field does not pre-empt the answer. `spacing_inches` already exists
  and is what such a rule would read.

This field remains worth shipping: it fixes the *stated* case, which is that a one-gallon pot holds
several lettuces and today's planner charges a whole gallon for one. What it does not do is license
a linear volume model, and section 5.1 no longer implies one.

---

## 5. Where `min_pot_gallons` and the new field disagree, measured

Every counted row, with the conservative per-plant figure the new field would give
(`at_gallons[hi] / count[min]`) against the per-plant figure the planner uses today
(`min_pot_gallons`). **"More permissive" means the new field charges a plant less, so more plants
fit a pot.** Measured on canonical `1721208e`.

| slug | source | count | `at_gallons` | new g/plant | `min_pot_gallons` | factor | direction | status |
|---|---|---|---|---|---|---|---|---|
| parsley | uiuc | `[1,1]` | `[0.5,0.5]` | 0.50 | 1 | 2.0x | **more permissive** | authored, count-1: no switch |
| cabbage | uiuc | `[1,1]` | `[1,1]` | 1.00 | 5 | 5.0x | **more permissive** | authored, count-1: no switch |
| swiss-chard | uiuc | `[1,1]` | `[1,1]` | 1.00 | 3 | 3.0x | **more permissive** | authored, count-1: no switch |
| cherry-tomato | uiuc | `[1,1]` | `[1,1]` | 1.00 | 5 | 5.0x | **more permissive** | authored, count-1: no switch |
| eggplant | uiuc | `[1,1]` | `[2,2]` | 2.00 | 5 | 2.5x | **more permissive** | authored, count-1: no switch |
| eggplant | umd | `[1,1]` | `[8,10]` | 10.00 | 5 | 0.5x | less permissive | authored, count-1: no switch |
| **green-beans-bush** | uiuc | `[2,3]` | `[1,1]` | **0.50** | 5 | **10.0x** | **more permissive** | **SWITCHES** |
| **lettuce-leaf** | uiuc | `[4,6]` | `[1,1]` | **0.25** | 1 | **4.0x** | **more permissive** | **SWITCHES** |
| cucumber | uiuc | `[2,2]` | `[1,1]` | 0.50 | 5 | 10.0x | more permissive | HELD (ruling 5) |
| cucumber | umd | `[1,1]` | `[8,10]` | 10.00 | 5 | 0.5x | less permissive | HELD |
| bell-pepper | uiuc | `[2,2]` | `[2,2]` | 1.00 | 3 | 3.0x | more permissive | HELD |
| bell-pepper | umd | `[1,1]` | `[8,10]` | 10.00 | 3 | 0.3x | less permissive | HELD |
| beefsteak-tomato | uiuc | `[1,1]` | `[3,3]` | 3.00 | 15 | 5.0x | more permissive | UNAUTHORED (ruling 5) |
| beefsteak-tomato | umd | `[1,1]` | `[8,10]` | 10.00 | 15 | 1.5x | more permissive | HELD |
| butternut-squash | umd | `[1,1]` | `[8,10]` | 10.00 | 10 | 1.0x | same | HELD |

### 5.1 What the rulings leave standing

**Every Illinois reading, without exception, is more permissive than `min_pot_gallons`** (2.0x to
10.0x). UMD runs the other way on the crops it names, because its 8-10 gallon class is larger than
most of our minimums. Trevor's read was right: the unguarded switch moves in the dangerous
direction, and UMD is the only thing that pushes back.

After rulings 3 and 5, **exactly two crops switch**:

| crop | today | after | change |
|---|---|---|---|
| `green-beans-bush` | 5.00 gal/plant | 0.50 | 10x more permissive |
| `lettuce-leaf` | 1.00 gal/plant | 0.25 | 4x more permissive |

**Both are more permissive, and neither has a reading that restrains it.** Measured: green beans sit
in UMD's "Medium Vegetables" class and lettuce in "Small Vegetables or Flowering Plant", and
**neither class publishes a count**. Ruling 2's conservative maximum has nothing to choose from, and
ruling 3's hold does not apply because both counts exceed 1. So the guards work where the field is
inert and do not reach the two rows where it acts.

**What this does and does not claim.** What the sources state is that a **one-gallon** pot holds 2-3
bush beans or 4-6 leaf lettuce, and that today's planner charging 5 gallons per bean and 1 per
lettuce is wrong at that size. What follows for a **five-gallon** pot is the app's linear model, not
Illinois' claim, and section 4.4 says so: the earlier draft's "roughly 10 bean plants or 20
lettuces" was stated as though it were a consequence of the data, and it is a consequence of the
model. Those numbers should be read as what the current model would say, and as the reason
capacity-by-area is now a live question on PLA-10.

**Recommendation:** ship the two, and put them in front of Trevor by name at the promote rather than
inside a roster count. If either reads wrong in the app, the honest lever is a second T1 reading that
restrains it, or PLA-10's area model, not a fudge factor on the first.

### 5.2 A hypothesis for PLA-533, not a conclusion (amendment 2)

**Ten of ten Illinois readings are more permissive than `min_pot_gallons`, by 2.0x to 10.0x, with no
exceptions.** A pattern that unbroken is unlikely to be ten independent authoring differences.

**The hypothesis:** `min_pot_gallons` is, and was authored as, *the minimum pot for the crop* --
a whole-container figure -- rather than *a per-plant root volume*. Illinois' sizes are also
whole-container figures but for smaller pots, so the gap would be a mixture of genuinely different
pots and a semantic mismatch. If that is right, then **PLA-409's per-plant reading of
`min_pot_gallons` is the original error**, and this field is exposing it rather than introducing it.
PLA-7's own kickoff records the same tension from the other side: it says the app consumes
`min_pot_gallons` "PER PLANT" and that "that per-plant semantics is written nowhere in the dataset
and must be", while the 2026-09-06 spec section 4 defines the field as the pot holding
`plants_per_pot` plants. Two documents, two meanings, and no source read.

**This is offered as a hypothesis for PLA-533 to test, not as a finding.** This session did not read
the provenance of a single `min_pot_gallons` figure, and PLA-533 owns exactly that. Recorded here
and as a comment on PLA-533 so the audit has a specific thing to look for: whether the authored
figures behave like whole-container minimums or like per-plant volumes, and whether any source was
ever read per-plant. Nothing in this spec depends on the answer, which is the point of ruling 3.

---

## 6. D3, presence-or-null. CONFIRMED against A39 and the register

**The rule:** `container_notes.plants_per_pot` is present on all **121 certified** crops, `null`
where no T1 count exists. The **7 shells carry no key** and stay byte-identical.

**Confirmed, not assumed.** Measured on `1721208e`: the 7 shells (avocado, olive, and the five
mushrooms) carry a `container_notes` block of 22-24 keys but **`'container_path' in cn` is `False`**
on all 7. A39 (`register_coverage_gate`, wired as whole_crop_gate A39) exempts uncertified crops by
**key absence**, which is how the A1 promote left the shells byte-identical. `plants_per_pot`
follows the identical pattern, and the register row for `container_path` (row **29**) is its
precedent. Row **30** is PLA-465's plant dimensions; this field takes row **31**.

**Encoding `at_gallons` (amendment 3).** Always `[lo, hi]`, both numbers, `lo == hi` for a single
stated size. **One type per field**: no consumer, gate or test ever branches on whether the value is
a scalar or a pair, and the conservative reader is unconditionally `at_gallons[1]`. Only UMD's
"Minimum 8-10 gallons" is a genuine band; every Illinois row is authored `[n, n]`. The rejected
alternatives were a bare scalar with an optional band (two types, a branch at every read site) and
authoring UMD at its low end (discards a figure the source states, and makes the cautious source
look less cautious than it is).

---

## 7. D4 and D5: display and consumers

### 7.1 What the card shows, and what it shows when the two figures disagree (ruling 4, amendment 1)

- Each reading renders as **its own line, attributed to its source**, carrying that reading's own
  `count` and `at_gallons`: "Illinois Extension: 4 to 6 plants in a 1 gallon pot."
- **No rendered sentence may state a count at a pot size no source named.** The card never scales a
  reading to the grower's actual pot, never to `min_pot_gallons`, and never to a round number. If a
  source did not say it, the card does not print it. This is amendment 1's display half and it binds
  both consumers.
- **No consumer ever computes or prints `min_pot_gallons / count`.** The existing string at
  `container-model.ts:256` is the thing being removed.
- The **Pot size row is unchanged** and keeps showing `min_pot_gallons`. When `at_gallons` is smaller
  than it (7 of the 10 Illinois rows), the two rows sit on the same card saying different things,
  and **the attribution is what resolves it**: the pot-size row is this project's recommended
  minimum, the plants-per-pot row is a named institution's observed capacity at a pot it chose. A
  reading is never phrased as advice to use a smaller pot.
- With two readings that disagree, **both render, both attributed**, in the order authored. The card
  does not pick a winner; only the planner does, by ruling 2.
- Copy rule, per the project convention: no em dashes in any rendered string.

### 7.2 The planner contract, including what is modeled

Stated for PLA-539 to implement:

1. Parse `container_notes.plants_per_pot.readings`. Absent, `null`, and an empty list all mean the
   same thing: **no readings, behave exactly as today.**
2. Per reading, conservative gallons per plant = `at_gallons[1] / count[0]` (4.2).
3. **Switch predicate:** use the field only if some reading has `count != [1, 1]`. Otherwise keep
   `min_pot_gallons` (4.2, ruling 3).
4. Once switched, take the **maximum** conservative figure across all readings, count-1 readings
   included (4.3, ruling 2).
5. **MODELED, and labeled as such in the code:** applying that per-plant figure to a pot of any size
   other than the reading's own `at_gallons` assumes capacity is linear in root volume. It is an app
   rule, not a dataset claim and not a sourced one. The comment at the call site says so, names
   section 4.4, and names PLA-10 as where the area alternative lives. A planner must price arbitrary
   pots, so the rule stays; what changes is that it stops being invisible.
6. The existing `containerPlantsPerPot[1]` at `rootstock.ts:112` divides by the wrong end and must
   become `[0]` (amendment 4).
7. Regression test owed, noted on PLA-539: an **object** value at `container-model.ts:100` reads as
   `null`. The current table test covers a string and `undefined` but not an object, and that guard
   is what makes the whole ordering safe.

### 7.3 The two consumers

**plant-app: already built, and that is the hazard.** Wired end to end today on
`feat/community-foundation` at `a7f6288c`:

| file | what it does now |
|---|---|
| `src/lib/container-model.ts:98-100` | `plantsPerPotOf` requires a 2-element integer array; anything else is `null` |
| `src/lib/container-model.ts:198` | sets `plantsPerPot` on `ContainerFacts` |
| `src/lib/container-model.ts:250-267` | renders the seasoned-only row "Plants per pot", text `"${count} in a ${f.minGallons} gallon pot"` |
| `src/lib/planner/catalog.ts:151` | maps it to `containerPlantsPerPot` |
| `src/lib/planner/rootstock.ts:112` | `share = containerPlantsPerPot[1]`, divides `min_pot_gallons` |

A code comment at `container-model.ts:253` already says "latent today -- no crop ships
plants_per_pot yet". **This field's consumer ships before its data**, so the frontend-first rule is
already satisfied in form but the built frontend implements the binding this spec rejects. Under
`{readings: [...]}` it reads `null` and holds today's behavior until changed deliberately. The work
is PLA-539's, contract in 7.2.

**plant-astro: filed as PLA-586.** There is no ContainerCard and `plants_per_pot` appears nowhere in
`src/`; `container_notes` is read only by `CareGuideCard.astro:101`, `HeroCard.astro:165-167` and
`lib/containers.ts`. PLA-586 mirrors plant-app's "In a pot" card (PLA-539) rather than designing a
new one, so **this field's astro contract is the app's contract**, restated here so PLA-586 can be
built against it without reading this whole spec:

- Read `container_notes.plants_per_pot`; treat **absent, `null`, and `{readings: []}` as the same
  thing: render no row.**
- For each reading render one attributed line per 7.1, using that reading's own `count` and
  `at_gallons`. **Never `min_pot_gallons`, and never a pot size no source named.**
- Dual register: the row is seasoned-only in the app card; astro matches unless PLA-480's design
  pass says otherwise.
- Astro renders; it does **not** compute per-plant gallons. Steps 2 through 6 of 7.2 are planner
  logic and have no astro equivalent, because astro has no planner. In particular astro never
  performs the modeled extrapolation at all, which makes its contract the simpler of the two.
- Note the pre-existing headline disagreement PLA-586 inherits: astro's HeroCard leads with
  `recommended_pot_gallons` while the app's planner computes from `min_pot_gallons`. This field is
  bound to neither, so it does not deepen the split, but PLA-586 should not accidentally resolve it
  by using `plants_per_pot` as a tiebreak.
- PLA-586 is blocked on PLA-535 (the astro submodule is 72+ revisions behind); nothing renders there
  until that bump lands.

**Export allowlist: confirmed, no change needed.** `container_notes` is present in `SHIP_TOP_LEVEL`
(`scripts/export-projection.mjs:44`), so a new subkey ships with no projection change. PLA-580's
item 4 is closed.

---

## 8. D4 armor

- **Shape gate, whole_crop_gate `A60`** (A58 is `container_path`, A59 is `plant_dimensions`; A60 is
  the next free id, measured). New `tools/plants_per_pot_gate.py` + tests, TDD, wired the way A58
  was: shape armed on the tooling commit, the **presence floor behind `A60_PRESENCE_ARMED = False`
  until the commit that writes canonical**.
  Rules: value is `null` or an object whose only key is `readings`; `readings` is a **non-empty**
  list (an empty list is not a legitimate value -- absence is spelled `null`); each reading's keys
  are exactly `{count, at_gallons, sources, anchoring_urls}`; `count` is `[min, max]` integers with
  `1 <= min <= max`; **`at_gallons` is always a 2-element list `[lo, hi]` of positive numbers with
  `lo <= hi`** and a scalar is a violation, not a shorthand (amendment 3); `sources` non-empty and
  every key present in `anchoring_urls` with a `url` and a `verified` date; **no two readings in one
  crop share a source key**; **`plants_per_pot` non-null requires `container_ok: true`**; and the
  key is **absent** on every uncertified shell.
- **`numeric_sanity_gate`:** `count[max] <= 30`; `at_gallons[hi]` in `[0.5, 100]`. The 0.5 floor is
  deliberate and differs from the `1..100` that `min_pot_gallons` and `recommended_pot_gallons` use
  at `numeric_sanity_gate.py:66-67`, because Illinois publishes a half-gallon row. A comment says so
  at the bound, or a later reader will "fix" it.
- **Cross-field coherence, fails LOUD:** `at_gallons` is **not** required to equal or exceed
  `min_pot_gallons`, and the gate must not assert it. Measured, that assertion would fail on 9 of 10
  authored rows -- it is the very confusion this spec exists to prevent. What the gate *does* check
  is that `at_gallons` is present whenever `count` is.
- **`register_completeness`:** `plants_per_pot` is structured, not prose; no register pair.
- **`field_additions` provenance:** one record per authored **reading**, carrying URL, fetch date,
  sha256 and the **verbatim row or sentence** the count was copied from. The EVIDENCE_HASHES guard
  from PLA-465 applies: no 64-hex token in the promote spec that is not a measured digest.
- **Suite + mutation harness, PLA-215:** one mutation per guard family, MUTATION-APPLIED marker +
  sentinel, `set(pre) == set(post)` before value comparison, refusal-spec passes for good input,
  suite replay-pinned via `promote_fixture.COMMIT_FOR`. **Positive control runs the whole suite.**
  Guards that cannot be shown reachable are removed, not shipped as coverage.
  **Two controls are owed by name**, because no authored crop exercises either path:
  1. **The two-reading conservative maximum (ruling 2), on a synthetic fixture.** Section 4.3
     records that eggplant is the only two-reading crop and that both its readings are count-1, so
     the maximum is never taken on real data. The fixture carries one count-1 reading and one
     count>1 reading on the same crop and asserts the larger per-plant figure wins.
  2. **The `count[min]` divisor (amendment 4).** A fixture whose `count` is `[2, 6]` distinguishes
     `count[0]` from `count[1]`; a `[4, 4]` fixture would pass under either and is not a control.
- **Release:** gate_all 121/121, A60 presence 0 violations, `register_completeness` +
  `register_coverage` PASS, `release_verify` clean in every section, collision gate holding.

---

## 9. The authorable population under the rulings

**Authored (8 readings across 7 crops):**

| crop | readings |
|---|---|
| `parsley` | uiuc `count [1,1]` @ `[0.5, 0.5]` |
| `cabbage` | uiuc `count [1,1]` @ `[1, 1]` |
| `green-beans-bush` | uiuc `count [2,3]` @ `[1, 1]` |
| `lettuce-leaf` | uiuc `count [4,6]` @ `[1, 1]` |
| `swiss-chard` | uiuc `count [1,1]` @ `[1, 1]` |
| `cherry-tomato` | uiuc `count [1,1]` @ `[1, 1]` |
| `eggplant` | uiuc `count [1,1]` @ `[2, 2]` **and** umd `count [1,1]` @ `[8, 10]` |

**Held (ruling 5):** Illinois' cucumbers and pepper rows, and UMD's tomatoes / pepper / cucumber /
Winter squash groups, all because one row names several slugs. **Unauthored:** Illinois' "Standard
tomatoes", which names no slug at all.

**Null:** the other 114 certified crops, including the 4 Illinois rows that give a thinning spacing.

The 18 prose crops are **not** authorable from the prose (2.5). Each would need its own T1 read
against the source the block already cites, which is a separate pass.

---

## 10. Sequencing

1. **Now:** this spec, amended twice, held for Trevor's read. No promote.
2. **Promote:** A60 gate (shape armed, presence floor disarmed), suite, harness with both named
   positive controls, the 8 readings in section 9, `field_additions` records, gauntlet on a scratch
   post-state, HOLD for approval, then the canonical write with `--expect-sha` and
   `A60_PRESENCE_ARMED = True` in the same commit.
3. **plant-app (PLA-539):** the contract in 7.2, including the `count[0]` divisor, the modeled-rule
   comment, and the object-reads-null regression test. Safe before or after the data lands, because
   the object shape reads null until then.
4. **plant-astro (PLA-586):** 7.3, itself blocked on PLA-535's submodule bump.
5. **PLA-533** may move `min_pot_gallons` under the count-1 rows, and 5.2 gives it a hypothesis to
   test. Nothing in this field depends on its outcome, which is the point of ruling 3.
6. **PLA-10** carries the capacity-by-area question from 4.4.
7. **Close PLA-580** with the record: the binding, the 8 readings, section 5's finding that the
   measured effect is two crops both loosened, and 4.4's line between what is sourced and what is
   modeled.

---

## 11. Out of scope, by name

`min_pot_gallons` semantics and PLA-533's provenance audit of the 102 figures (5.2 hands it a
hypothesis, not an answer); **capacity-by-area as the governing constraint for multi-plant pots,
which is PLA-10's** (4.4); the strawberry diameter count and any diameter-to-volume conversion; the
18 prose counts as an authoring source; `critical_warnings` (PLA-581, Plan D); the 88 unmatched
cultivar names (Plan B); the astro card itself (PLA-586); the app changes themselves (PLA-539).

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
dataset-wide. `container_ok: true`: **110** of 121 certified. `min_pot_gallons` present: **102**;
`recommended_pot_gallons` present: **95**; both: **95**; min without recommended: **7**
(`lettuce-leaf`, `orange-navel`, `mandarin-clementine`, `mulberry`, `grapefruit`, `cherry-sweet`,
`cherry-sour`). `'container_path' in container_notes` is `False` on all 7 shells. Certified crops
that are `container_ok: true` with no count in any source read: **86**. Certified but not
`container_ok`: **11** (apricot, asparagus, field-corn, flint-corn, nectarine, pawpaw, peach,
persimmon, plum, popcorn, sweet-corn).

**`min_pot_gallons` for the crops in section 5:** parsley 1, cabbage 5, swiss-chard 3, cherry-tomato
5, eggplant 5, green-beans-bush 5, lettuce-leaf 1, cucumber 5 (and english-/pickling-/slicing- all
5), bell-pepper 3, beefsteak-tomato 15, heirloom-tomato 15, butternut-/acorn-/spaghetti-squash and
pumpkin 10.

**Register / gates.** `docs/field_addition_register.md` holds 30 rows; 29 is `container_path`, 30 is
plant dimensions; this field is 31. Highest whole_crop_gate id in `tools/whole_crop_gate.py` is
**A59**; A60 is free. `numeric_sanity_gate.py:66-67` bounds `min_pot_gallons` and
`recommended_pot_gallons` at `1..100`.

**Consumers.** plant-app `feat/community-foundation` @ `a7f6288c`: `container-model.ts` lines 98-100
(guard `if (!Array.isArray(v) || v.length !== 2) return null;` at 100), 198, 250-267; test table at
`container-model.test.ts:109-117` (no object case); `planner/catalog.ts:151`;
`planner/rootstock.ts:103-118`; `planner/types.ts:39`; `container_notes` in `SHIP_TOP_LEVEL` at
`export-projection.mjs:44`. plant-astro @ `aa17dff`: no ContainerCard, no `plants_per_pot`
reference; `container_notes` read in `CareGuideCard.astro:101`, `HeroCard.astro:165-167`,
`lib/containers.ts`.

**Discrepancies recorded against the 2026-09-06 spec.** (a) UMD publishes a count against a stated
size; the spec says it carries narrative counts only. (b) The prose-count population is 18, not 13.
(c) The lettuce worked example's arithmetic matches neither the dataset (`min_pot_gallons` is 1, not
2) nor the source (0.25 conservative, not 0.33). (d) PLA-580's summary line renders
`min_pot_gallons` semantics as "per plant"; the spec's own section 4 says a pot holding
`plants_per_pot` plants. The app implements the spec, not the summary. 5.2 records that this
disagreement may be the arc's original error rather than a wording slip.

**Corrections recorded against this document's own drafts.** (i) "Dividing by 1 changes nothing" was
false under D2; see 4.1. (ii) The first draft divided by `count[max]`; amendment 4 makes `count[min]`
the contract, and the section 3 and 5 tables are recomputed accordingly (green beans 0.33 -> 0.50,
lettuce 0.17 -> 0.25). (iii) The amendment-1 draft presented "roughly 10 bean plants or 20 lettuces"
as a consequence of the data; it is a consequence of the linear-volume model, and 4.4 and 5.1 now
say so.
