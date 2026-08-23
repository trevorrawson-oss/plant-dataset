# Control-method catalog extension -- spec + provenance (PLA-8, ahead of the ladder rollout)

**Date:** 2026-08-22
**Canonical:** `98ea96c4` (unchanged by this document; nothing promoted yet)
**Why now:** the pilot batch of five crops proved the 37-method catalog is under-powered for the
roster it is about to be rolled out across. Extending it AFTER 23 batches would bake the loss into
861 problems.

---

## 1. The measured gap

The catalog was built for the 7-crop ladder pilot. Measured against `TYPE_TARGETS`, how many of the
37 methods are legal for each problem type:

| problem type | legal methods | note |
| -- | --: | -- |
| insect | 25 | fine |
| mite | 22 | but the 22 exclude the water spray, soap and watering the source leads with |
| fungal | 12 | |
| bacterial | 10 | |
| viral | 10 | **every one of them is a generic disease method; none targets `viral`** |
| mollusk | 6 | |
| vertebrate | 6 | |
| physiological | 5 | |
| **nematode** | **4** | **all four are the `any` methods; nothing targets `nematode`** |

**`nematode` and `viral` are declared in `TYPE_TARGETS` but used by ZERO of the 37 methods.** They
are dead branches: a problem typed either way can only ever reach `crop_rotation`,
`garden_sanitation`, `resistant_varieties` and `floating_row_cover`.

This is not a theoretical gap. Five independent authoring bots, run in parallel on unrelated crops,
each hit it and each reported it unprompted:

- **heirloom-tomato / spider mites** -- the crop's own prose calls a water blast and consistent
  watering its primary controls. Both were blocked. The ladder that would have shipped omits exactly
  what the source emphasizes most.
- **swiss-chard / slugs** -- night hand-picking, the entry's first-line treatment, was blocked.
- **swiss-chard + fig / root-knot nematode** -- the whole organic-matter and vigor program had no
  legal home.
- **jalapeno / bacterial spot** -- "water at the soil to keep foliage dry" was blocked.
- **basil / fusarium, jalapeno / phytophthora, heirloom-tomato / wilt** -- soil drainage, named as
  the core control in all three, has no method at all.

---

## 2. What ships in this round -- 3 new methods, 4 corrections

Every claim below is quoted from a document **fetched and read on 2026-08-22**, not cited from
memory. Where a source hedges, the hedge is recorded here so it cannot be lost in compression.

### 2a. NEW: `soil_solarization` (tier `physical`)

`applies_to`: `nematode`, `fungal_soilborne`, `bacterial`, `disease_general`
**Anchor:** UC IPM Pest Notes 74145, *Soil Solarization for Gardens & Landscapes*
`https://ipm.ucanr.edu/PMG/PESTNOTES/pn74145.html` (fetched 2026-08-22, 59,467 bytes)

> "Solarization controls many soilborne fungi and bacteria, nematodes, and some weeds."
> "The method involves heating the soil by covering it with clear plastic for four to six weeks
> during a hot period of the year"
> "heating the top 12 to 18 inches to temperatures lethal to a wide range of soilborne pests"
> "the top layers of soil will heat up to as high as 140°F"
> "Four to six weeks of soil heating during the warmest time of the year is usually sufficient to
> control most soil pests."

**THE HEDGE, WHICH MUST RIDE IN `cons` AND IN THE SEASONED REGISTER:**

> "soil solarization is not always as effective against nematodes as it is against fungal disease
> and weeds. This is because nematodes are relatively mobile and can move deeper in the soil profile
> to escape the heat"

Corroborated by UC IPM Pest Notes 7489 (*Nematodes*, fetched 2026-08-22), which independently
bounds the claim:

> "You can reduce existing infestations through fallowing, crop rotation, and soil solarization.
> However, these methods reduce nematodes primarily in the top foot or so of the soil, so they are
> effective only for about a year. They are suitable primarily for annual plants or to help young
> woody plants establish."

This is the method that ends `nematode`'s dead branch, and it must ship carrying its own limits.

### 2b. NEW: `improve_drainage` (tier `cultural`)

`applies_to`: `fungal_soilborne`, `disease_general`
**Anchor:** UC IPM Pest Notes 74133, *Phytophthora Root and Crown Rot*
`https://ipm.ucanr.edu/PMG/PESTNOTES/pn74133.html` (fetched 2026-08-22, 59,946 bytes)

> "The most important way to prevent Phytophthora root and crown rot is proper irrigation."
> "Provide good soil drainage. Raised beds can be a good solution for vegetables where drainage is
> a problem."
> "Avoid prolonged soil saturation or standing water around tree bases."
> "Phytophthora diseases can develop in as little to 4 to 8 hours of soil saturation"
> "Soils should be well-drained to the rooting depth of the plants ... 1 to 2 feet for bedding plants"

The 4-to-8-hour figure is worth carrying into the seasoned register: it is the fact that makes
drainage feel urgent rather than tidy.

### 2c. NEW: `reflective_mulch` (tier `cultural`)

`applies_to`: `insect_soft_bodied`, `viral`
**Anchor:** UC IPM Pest Notes 7404, *Aphids*
`https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html` (fetched 2026-08-22, 68,447 bytes)

> "Silver-colored reflective mulches have been successfully used to reduce transmission of
> aphid-borne viruses in summer squash, melon, and other susceptible vegetables. These mulches repel
> invading aphid populations, reducing their numbers on seedlings and small plants."

One sentence anchors BOTH targets, which is why this method ends `viral`'s dead branch as a
by-product of fixing an aphid gap. Note the scope: the source's claim is about **seedlings and small
plants**, so the prose must not imply it protects a mature planting.

### 2d. CORRECTIONS to `applies_to` on FOUR existing methods (three mite, one mollusk)

> **One candidate was dropped after checking:** `horticultural_oil` was listed here in the
> first draft, on the strength of the same "insecticidal oil or insecticidal soap" sentence.
> It already carries `mite`. The claim was true and the correction was a no-op, and a no-op
> row in a corrections table reads as coverage it does not provide.

These are corrections, not additions: the methods already exist and the omission looks like an
artifact of a 7-crop pilot rather than considered biology. Each is anchored.

**UC IPM Pest Notes 7405, *Spider Mites*** `https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html`
(fetched 2026-08-22, 55,187 bytes):

| method | add | supporting sentence |
| -- | -- | -- |
| `water_spray` | `mite` | "In gardens and on small fruit trees, regular, forceful spraying of plants with water often will reduce spider mite numbers adequately." |
| `insecticidal_soap` | `mite` | "If an insecticide is needed, use an insecticidal oil or insecticidal soap (or a combination of the two)." |
| `even_watering` | `mite` | "Water plants enough so they are not drought stressed, which increases mites and mite damage." |

**UC IPM Pest Notes 7427, *Snails and Slugs*** `https://ipm.ucanr.edu/PMG/PESTNOTES/pn7427.html`
(fetched 2026-08-22, 62,477 bytes):

| method | add | supporting sentence |
| -- | -- | -- |
| `handpick` | `mollusk` | "Handpick from plants at night or from fence ledges, undersides of decks, and meter boxes." and "Hand-picking can be very effective if done thoroughly on a regular basis." |

---

## 3. DELIBERATELY NOT IN THIS ROUND -- owed, with the reason

**No adequate T1 anchor was found, so nothing is minted.** A catalog entry's SHAPE will pull a
fabricated source out of an author who is trying to fill it; the honest output is a shorter list.

| owed method | why it is owed | why it is not here |
| -- | -- | -- |
| `container_culture` | PLA-8's own container ruling requires it (role (b): the remedy IS the container). Wanted by fig x2, swiss-chard, heirloom-tomato. | **Checked and refuted:** UC IPM's *Nematodes* note contains ZERO mentions of container, potting, pot, or organic matter. The UC IPM root-knot page returned a 10KB stub and a UMN container-growing URL 404'd. The crops' own prose asserts it, but crop prose is not a catalog anchor. |
| `certified_clean_stock` | The PRIMARY control for basil downy mildew, jalapeno anthracnose, fig mosaic. Repeatedly dropped by the bots. | Not yet sourced. Likely findable; not attempted this round. |
| `bottom_watering` += `bacterial` | jalapeno's bacterial-spot prose says "water at the soil to keep foliage dry". | Crop prose only. Needs its own T1 anchor before the widening is defensible. |
| `straw_mulch` += `physiological` | heirloom-tomato's blossom-end-rot and cracking prose call for mulch. | Same: crop prose only, not yet anchored. |
| generic pheromone / monitoring trap | jalapeno's pepper weevil. The only pheromone method is codling-moth-specific. | Not sourced. |
| trap cropping, diatomaceous earth | jalapeno flea beetles, heirloom-tomato flea beetles. | Not sourced. |

---

## 4. Consumer impact -- checked with the plant-app session, not assumed

- **No new tier.** All three new methods sit inside plant-app's hardcoded five (`TIER_ORDER`). A
  sixth tier would have made the methods render NOWHERE while only the test suite complained, and
  would have silently skipped the label/PHI/pollinator safety strip via `isSprayMethod()`.
- **None of the three is a spray**, so defaulting to non-spray is correct by intent here, not by
  accident.
- **Nothing enumerates method keys**; `methodFor()` is a keyed lookup and `humanizeMethodKey()`
  already degrades gracefully for a key the app's glossary lacks ("dataset authored ahead of the
  app: render a readable rung, never crash").
- **`applies_to` has NO consumer in plant-app.** The corrections are dataset-internal, affecting
  only which methods a gate will accept on a given problem type.
- plant-app's data test asserts `keys.length >= 24`, a floor, so catalog growth passes.

---

## 5. Gate consequences

`control_ladder_gate.catalog_violations` requires, for every entry: all of
`name / tier / applies_to / how_it_works_beginner / how_it_works_seasoned / best_use / pros / cons /
sources / anchoring_urls`, a valid tier, non-empty pros and cons, every source present in
`source_catalog` AND at tier T1, and `anchoring_urls` keys matching `sources` exactly.

All three new entries anchor to `ucanr_ext`, already catalogued T1 and already the anchor for 30 of
the 37 existing methods. Per A54, any document-scoped sub-id minted must be TITLED from the document
itself rather than inferred from its URL.

**The corrections widen what the gate ACCEPTS, so they cannot redden anything.** Re-running the five
pilot crops after this lands should show ladders GAINING the rungs their sources lead with, which is
the point.
