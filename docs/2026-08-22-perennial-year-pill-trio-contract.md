# Contract: the perennial year-pill trio (`year_one_notes_*` / `first_harvest_notes_*` / `full_harvest_notes_*`)

**Status:** CONTRACT, ruled 2026-08-22 (Trevor). Field-addition register **row 28**.
**Arc:** PLA-6 Round 2. **Method:** `docs/gs_cross_crop_field_addition_v0.md` (column GS arc).
**Consumer wiring:** PLA-362 landed 2026-08-22 (plant-app). Authoring is UNBLOCKED.

---

## The defect this closes

plant-app renders three year-pills on every perennial guide -- **Establishing / First harvests /
Full harvest** -- and composes their captions from prose authored for other purposes
(`src/app/(tabs)/learn/[slug].tsx`, `establishmentCopy`):

```
Establishing    -> tips_by_stage.establishment[0].text_{level}
First harvests  -> tips_by_stage.establishment[0].text_{level}   <-- THE SAME STRING
Full harvest    -> firstSentence(harvest_ready_{level})
```

Measured on canonical `fe26f783`:

* **Establishing and First harvests are byte-identical on 36 of 38 perennials** (72 of 76
  crop x register slots; the 4 exceptions are the avocado/olive shells, which are empty).
* **22 of the 26 pill-rendering crops** put text explicitly scoped to year 1 into the
  First-harvests pill. Apple's First-harvests state covers **bed years 2, 3 and 4** and its only
  content is *"Pinch off all the flowers the first spring."* Pawpaw's covers **years 4, 5 and 6**
  and says *"Give the young tree shade for its first year or two."* The remaining 4 (blackberry,
  grapefruit, orange-navel, persimmon) inherit generic establishment text, which is not wrong,
  just not about the year the grower is in.
* The pill sits directly beneath a ribbon reading **LIGHT HARVEST**. That is the PLA-327 pattern
  one layer up: two parts of one screen disagreeing.
* The strings are **thin** for the load: median establishment tip is **149 chars beginner / 169
  seasoned**. Apple's seasoned register is 96 characters, and it is currently doing the work of
  two entire pills.
* **The Full-harvest caption is a truncation**, and `harvest_ready_*` is *also* rendered in full
  further down the same page by `guide-chapters.ts`'s Harvest chapter. So the caption is
  simultaneously too short to stand alone (artichoke beginner: `"Squeeze the bud."`, 3 words) and
  a duplicate of content already on the page. Un-shearing it would worsen the duplication; the
  pill needs its own string.

**Register coverage is NOT part of this defect.** Measured: 0 half-pairs across 873 register pairs
on perennial `growth_stages`; the pill-feeding fields are complete except on the two known shells.
Do not spend arc time on it.

---

## The contract

Two new crop-level register pairs, symmetric with the existing `year_one_notes_*`:

| field | type | applies to |
| -- | -- | -- |
| `year_one_notes_beginner` / `_seasoned` | string | EXISTS on 26 crops. Repurposed as the **Establishing** caption. |
| `first_harvest_notes_beginner` / `_seasoned` | string \| null | **NEW.** The **First harvests** caption. |
| `full_harvest_notes_beginner` / `_seasoned` | string \| null | **NEW.** The **Full harvest** caption. |

### Presence rule

**Present-or-null on all 38 `perennial: true` crops**, so an A39-style presence floor can gate it
and a new perennial cannot certify without a ruling. Non-null is REQUIRED on the crops that render
pills; null is the correct value elsewhere.

"Renders pills" is defined by plant-app and reproduced in `tools/perennial_year_gate.py::renders_pills`:
a well-formed `years_to_first_harvest: [lo, hi]`. **26 of 38 today.** The 12 that render none are
the 5 woody-ornamental herbs (lavender, oregano, rosemary, sage, thyme), the 3 culinary herbs
(chives, lemongrass, mint), the 2 flowers (bee-balm, echinacea), and the avocado/olive shells.
Those 12 take `null` in all six slots -- **a legitimately-N/A case, which the method requires the
pilot to include.**

### All three pills are always rendered

`YEAR_PILLS` in `PhaseRibbonCalendar.tsx` is a fixed three-element array; every pill is present and
tappable on every pill-rendering crop. `establishmentState()` only decides which one is **selected
on open**. So a crop whose `years_to_first_harvest[0] <= 1` (artichoke, blackberry, fig, raspberry,
strawberry -- `bedYear()` is 1-based, so those never *open* on Establishing) still needs all three
strings, because a grower can tap any pill. **All 26 crops need all 6 slots. No partial rows.**

---

## What each string must say

The governing test, from copy architecture v1.3 §9.1 applied on the **year axis**:

> What does a grower in *this* state now know, or now be able to do, that a grower in the previous
> state does not?

| pill | the question it answers | asparagus | apple |
| -- | -- | -- | -- |
| **Establishing** | the plant is in the ground and gives you nothing. What are you building, and what must you not do? | Cut nothing at all. The fern is the crown's only way to build reserves. | Pinch every blossom off. A fruitless year 1 buys decades of tree. |
| **First harvests** | you may take some, and taking too much costs you the planting. How much, and how do you know when to stop? | A light two-week pick *only if the bed came through strong*. Over-cutting a two-year crown is how home plantings fail. | The tree may hold a few fruit now. Thin hard and stake or support the limbs; a young tree can break under its first real crop. |
| **Full harvest** | the planting is mature. What does a full season look like, and what keeps it productive for its lifespan? | Six to ten weeks, ending on spear calibre, not on the calendar. | A full crop every year, with annual dormant pruning and thinning to prevent biennial bearing. |

**Three rules, all load-bearing:**

1. **The biology of the stage, not general care.** "Water deeply" belongs in `watering`. These
   fields exist to say what is true *of this year and not the next one*.
2. **The beginner register carries the ACTION, not just the caution.** Per the v1.2 §9
   actionability floor, and it matters most here: getting asparagus year 2 wrong costs the grower
   the bed. A beginner given a risk and denied its remedy is worse off than one given neither.
3. **Gloss in the field, not three fields away.** `bract tightness`, `crown`, `rootstock`, `cane`,
   `spur`, `primocane`, `renovation`. The gloss usually already exists on a neighbouring crop --
   borrow it rather than inventing. See PLA-6's cleanup slice, and the corrected measurement in
   its Round 1 close-out (`crown` is 95 bare on perennials, not 147, and glossed instances do
   exist -- strawberry's `hardening_off_beginner` is the model).

**Length floor:** these replace strings whose median is 149/169 chars and which were judged thin
for the job. Target the range `year_one_notes_*` already occupies (asparagus 306/423, artichoke
255/403), not the establishment tip's.

---

## Sequencing -- FRONTEND FIRST, and why it is not optional here

`year_one_notes_*` is the cautionary tale and it is already in this dataset: 26 crops of
well-sourced establishment prose, authored, carried through the export projection, and **read by no
component in either consumer repo.** Nobody has ever seen a word of it. Authoring 104 more strings
into the same condition is the failure this arc exists to stop.

Strictly, adding optional prose fields is inert rather than dangerous -- this is not the
`fail-open-renderer-hides-new-values` enum hazard, where a consumer degrades on an unknown value.
Nothing breaks if the app never reads them. But nothing *works* either, and that is the whole point.

**Order:**

1. ~~**plant-app rewires the three pills to the three fields**~~ **DONE 2026-08-22 (PLA-362).**
   Each pill falls back to today's source when its field is null, so a half-migrated roster renders
   correctly throughout. **It was NOT a no-op, and that was measured rather than assumed:**
   `year_one_notes_*` is already in the shipped bundle on 26 crops, so wiring Establishing to it
   changed **52 captions on day one with zero authoring**, and
   **Establishing == First harvests fell from 36 crops to 10.** Of those 10, five render no pills
   at all; the live remainder is the **five citrus** (grapefruit, lemon, lime, mandarin-clementine,
   orange-navel), the only pill-rendering crops with no `year_one_notes_*`. Diffed old-vs-new over
   all 121 shipped guides x 3 states x 2 registers: 52 differences, all on `establishing`, none on
   `first` or `full`.
2. **Pilot 4 crops** per the column-GS-arc method -- apple (the deblossom class, 3-year First
   harvests), pawpaw (longest establishment, 4..6), asparagus (herbaceous, has a real ramp), and
   **sage** (the legitimately-N/A case: no `years_to_first_harvest`, all six slots null).
3. **Roll out** to the remaining 22, then null-fill the other 11 N/A crops.
4. **Gate.** `tools/perennial_year_gate.py` gains a TRIO family (presence-or-null, non-null on
   pill-rendering crops, no two of the three byte-identical within a crop) and arms as an
   A-number once the 4 PILL-CAPTION findings are cleared. Per the no-backfill-treadmill rule, a
   new perennial then cannot certify without the trio.

## Consumers

**plant-app** is the only consumer today, and PLA-362 wired it 2026-08-22.

**plant-astro does NOT render the year-pills at all** -- measured, not assumed: it reads
`years_to_first_harvest` in exactly two places (`HeroCard.astro`, `guides/index.astro`) and only as
a number, for a "first harvest in N years" line. `year_one_notes` appears **zero** times. There is
no Establishing / First harvests / Full harvest UI on the website.

**That is by plan, not by oversight** (Trevor, 2026-08-22: "We haven't added the perennial feature
to the website. Once this is done we will"). So the website is a **follow-on consumer**, and when it
picks the feature up it inherits two requirements from this contract:

1. Read the trio, one field per pill -- not the legacy `tips_by_stage.establishment[0].text_*`,
   which is what put year-one advice on the First-harvests pill in the app.
2. **Collapse the caption with a "Read more."** `year_one_notes_*` was authored as an explainer,
   not a caption: median 449 characters against the 166 the establishment tip ran, 19 of 52
   registers over 500, and a 1190-character maximum on artichoke's seasoned. Unclamped it pushes
   the calendar out of view. The app's clamp is `src/components/guides/ClampedCaption.tsx`
   (six lines, width-aware threshold); the website needs its own, since none of that code is shared.

## The caption clamp (app, shipped with PLA-362)

Trevor's call: *"I like read more."* The depth is wanted -- he had asked for exactly it
(*"they are also a little thin on info"*) -- so every word is kept and the reader opens it, rather
than trimming the prose back to caption length.

`ClampedCaption` clamps to 6 lines and offers Read more / Read less only when the text is long
enough to need it. The overflow test is a **width-aware character threshold** (400 phone / 700
iPad), not a measurement, because React Native's `onTextLayout` reports only the VISIBLE lines once
`numberOfLines` is set -- a clamped `Text` cannot tell you it was clamped. The usual workaround
renders unclamped for one frame to measure and then clamps, which pops the layout on every guide
open. The thresholds sit deliberately ABOVE the true wrap point at each width, because a
"Read more" that expands nothing is a worse defect than a slightly long caption.

## What this does NOT resolve

* **`establishment_years` still ships in three shapes** -- 27 int, 4 `[lo, hi]` (exactly the
  `berries_woody` archetype), 2 null, 5 absent. Deliberately ungated pending its own ruling;
  it drives Herb's coaching gate and `establishment.ts` states it is *meant* to disagree with
  `years_to_first_harvest`. Separate decision.
* **The other unrendered fields.** `establishment_note` (26), `harvest_stop_rule` (2, including
  asparagus's bed-saving pencil-thickness rule), `harvest_ramp_na_*`, `years_to_full_production`,
  `productive_lifespan_years` all still render nowhere. This arc rescues `year_one_notes_*` only.
