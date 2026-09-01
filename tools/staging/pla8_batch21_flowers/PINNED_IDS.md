# BATCH 21 (flowers & edible flowers) -- PINNED PROBLEM IDS

**Settled BEFORE fan-out. Use the id in this table. Never derive one from the problem name.**

Base `5409c0ce`. 3 crops, 26 problems. Fourth consecutive batch pinned in advance.

## 0. TWO THINGS THAT MAKE THIS BATCH DIFFERENT FROM 17-20

1. **These are NOTE-SCHEMA records.** Each problem carries only `note_beginner` / `note_seasoned`,
   `name`, `audience` and `severity`. There is **no** `symptoms_*`, `cause_*`,
   `organic_treatment_*` or `prevention_*`, and **no `sources` or `anchoring_urls`**. That is the
   companion-flower schema from batches 15 and 16, not the batch 17-20 schema. Copying batch 20's
   promote would have refused the whole batch on its premise check.
2. **All 26 carry NO `type`**, so every type is SET from nothing (the batch 20 form, not 19's).

## A. REUSE an existing roster id

| problem | crop | id | why the reuse is safe |
|---|---|---|---|
| Aphids | all three | `aphids` | the broad generic; 54 holders |
| Cabbage white caterpillars (imported cabbageworm) | nasturtium | `cabbageworms` | *Pieris rapae*, the same insect the five brassicas carry. The note even gives the reason: nasturtium "shares the mustard-oil chemistry of brassicas" |
| Flea beetles | nasturtium | `flea-beetles` | 31 holders |
| Slugs and snails | nasturtium, viola | `slugs-and-snails` | 9 holders |
| Aster yellows | nasturtium | `aster-yellows` | a phytoplasma with a wide host range; 4 holders |
| Cutworms | sunflower | `cutworm` | **SINGULAR, deliberately.** See section D |
| Sclerotinia (white mold) head and stalk rot | sunflower | `white-mold` | **same organism**: the beans' `white-mold` is *Sclerotinia sclerotiorum* and so is this |
| Downy mildew | sunflower, viola | `downy-mildew` | 27 holders |
| Spider mites | viola | `spider-mites` | 15 holders |
| Foliage-feeding caterpillars | viola | `caterpillars` | generic name, generic record |
| Crown and root rot | viola | `crown-and-root-rot` | see section C |
| Powdery mildew | viola | `powdery-mildew` | 29 holders |
| Gray mold (Botrytis blight) | viola | `gray-mold` | **same organism**: *Botrytis cinerea*, as on strawberry, marigold and cosmos |

## B. MINT NEW -- including FOUR traps

| problem | crop | id |
|---|---|---|
| Bacterial wilt | nasturtium | `southern-bacterial-wilt` |
| Rust | sunflower | `sunflower-rust` |
| Septoria leaf spot and powdery mildew | sunflower | `sunflower-foliar-diseases` |
| Leaf spots and anthracnose | viola | `viola-leaf-spots` |
| Whiteflies and spider mites | nasturtium | `whiteflies-and-mites` |
| Mosaic and aphid-borne viruses | nasturtium | `aphid-borne-viruses` |
| Birds and squirrels | sunflower | `birds-and-squirrels` |
| Sunflower moth and head-clipping weevil | sunflower | `sunflower-head-insects` |
| Leaf-feeding caterpillars and beetles | sunflower | `sunflower-defoliators` |

### TRAP 1 -- `bacterial-wilt` is the WRONG ORGANISM AND THE WRONG CONTROL

The roster's `bacterial-wilt` (10 cucurbit crops) is ***Erwinia tracheiphila***, and cantaloupe's own
record says it "has no soil or seed stage that matters here: it survives the winter inside cucumber
beetles". Nasturtium's note says **"Southern bacterial wilt (Ralstonia) can collapse plants in hot,
humid soils... remove infected plants and rotate away from the site."**

Different genus, different reservoir, and **opposite management** -- beetle control versus soil
rotation. This is the most dangerous trap in the batch, because reusing it would attach
beetle-vectoring advice to a soilborne disease. Ships `southern-bacterial-wilt`.

### TRAP 2 -- "Rust" name-matches a CROP-SCOPED id

Sunflower's problem is named `Rust`, and bee-balm has a problem named `Rust` whose id is
**`bee-balm-rust`** -- already crop-scoped by whoever authored it. Sunflower rust is a different
species. Batch 20 minted `orange-rust` and `elderberry-rust` on the same principle. Ships
`sunflower-rust`.

### TRAP 3 -- `septoria-leaf-spot` is a different Septoria

The roster's `septoria-leaf-spot` (6 holders) is ***Septoria lycopersici***, a tomato disease.
Sunflower's note names ***Septoria helianthi***. Different species -- and the sunflower record is a
COMPOSITE with powdery mildew besides, so neither existing id covers it.

### TRAP 4 -- viola's `anthracnose` is not the vegetable generic

Viola's note is "Foliar spotting (including pansy leaf spot **and** anthracnose)" -- a composite of
leaf spots, not the *Colletotrichum orbiculare* the roster's `anthracnose` (14 crops) carries. Batch
20 already split cane anthracnose and blueberry ripe rot away from that same generic; this is the
third crop family to need it.

## C. Two judgment calls, stated so they can be overruled

**`crown-and-root-rot` IS reused** (parsley, 1 holder). Parsley's record names "Pythium,
Phytophthora, Rhizoctonia"; viola's names "black root rot from Thielaviopsis, plus Pythium and
Phytophthora". Both are COMPLEXES of soilborne rots sharing two genera and the same cultural
management, and the id is generically named. Viola's *Thielaviopsis* is an addition within the
complex, not a replacement. Same reasoning that kept acid citrus's composite `citrus-mites` intact.
**The author should carry the black-root-rot and high-pH detail in the rung prose.**

**Composites get composite ids, and the test is whether ONE organism is the DRIVER.** Batch 20 kept
elderberry's SWD reuse because SWD creates the damage and the whole control is the SWD program. Here
none of the composites has a driver: whiteflies and mites are both called "secondary"; birds and
squirrels both "raid ripening heads" under one covering control; the moth and the weevil are "the
classic head-infesting pair". Co-equal subjects with one shared control get one composite id.

## D. CORRECTED -- `cutworms` PLURAL, and the split is a MEASURED ROSTER DEFECT CLASS

**The first draft of this section was WRONG and said the opposite.** It claimed asparagus's
`cutworm` was the only holder, so reusing the singular would avoid *creating* a split. That rested
on a broken scan (see section G). The measurement:

| singular | holders | plural | holders |
|---|---|---|---|
| `cutworm` | **1** (asparagus) | `cutworms` | **8** |
| `flea-beetle` | **1** (swiss-chard) | `flea-beetles` | **31** |
| `japanese-beetle` | **1** (basil) | `japanese-beetles` | **6** |

**Three splits, all the same 1-versus-many shape**: exactly one early crop holds the singular and
everything authored since uses the plural. Batch 20 found the Japanese beetle instance and treated it
as a one-off; it is a class.

**RULED: sunflower takes `cutworms` (plural)**, matching the majority and the batch 20 decision.
nasturtium's `flea-beetles` is already the majority id and is correct as pinned.

**FILED, not fixed:** three repoints (asparagus, swiss-chard, basil) would retire the class entirely.
Each is one token, but a repoint is its own change with its own blast radius.

(`bacterial-leaf-spot` on cilantro versus `bacterial-spot` on five peppers also appears in the
multi-id list but is probably a LEGITIMATE distinction rather than a split -- different organisms --
and is not part of this class.)

## E. THE COMPANION INVERSION IS LIVE, AND NASTURTIUM IS ITS SHARPEST CASE

Batches 15 and 16 established it: on a companion planting a "pest" can be the POINT of the plant.
Nasturtium's own aphid note says **"Aphids love nasturtiums, which is exactly why gardeners use the
plant as a trap to lure them away from vegetables"**, and its virus note adds "because nasturtium
concentrates aphids...".

So, carried forward from batch 16:
* **`trap_cropping` is FORBIDDEN batch-wide.** The trap-crop USE is why you grow the plant; it is not
  a control of the plant's own problem.
* **Trap/decoy vocabulary is banned from every rung note**, so unplaced trap content cannot creep
  back in through prose.
* A nasturtium aphid ladder must not read as "eliminate the aphids". The note distinguishes a TRAP
  stand (monitor, pull and destroy once loaded) from an ORNAMENTAL one. The rungs must respect that.

## F. Count check -- CORRECTED TWICE. Computed, never hand-added.

| bucket | instances | distinct ids |
|---|---|---|
| A reuse | 20 | 16 |
| B mint | 6 | 6 |
| **total** | **26** | **22** |

**The first draft said 17 reuse / 9 mint.** Three ids I classified as MINTS were already live, and I
found them only because two authoring agents flagged one each and an audit then caught the rest:

| id | actually lives on | how it was missed |
|---|---|---|
| `southern-bacterial-wilt` | eggplant | see section G |
| `birds-and-squirrels` | fig | fig's problem is NAMED "Birds (and squirrels)", so a by-name scan misses it |
| `whiteflies` | roma-tomato, grape-tomato, calendula | I planned to mint a composite; see section H |

## G. THE METHOD BUG THAT CAUSED THIS, so it is not repeated

My reuse scan built `name -> {ids}` and then displayed `sorted(ids)[0]`. **Eight problem names on
this roster carry MORE THAN ONE id**, so for every one of them the scan silently showed only the
alphabetically-first and hid the rest. "Bacterial wilt" maps to BOTH `bacterial-wilt` (cucurbit
*Erwinia*) and `southern-bacterial-wilt` (eggplant *Ralstonia*); `bacterial-wilt` sorts first, so I
concluded the correct organism needed a NEW id when the roster already had exactly the right one.

**Two rules for the next batch's pinning step:**
1. Never collapse a name to one id. Print every id a name carries.
2. **Check each id you intend to MINT against the roster directly**, not only its problem name. A
   name-based scan cannot see an id whose holder names the problem differently.

(The promote's `check_ids` would have caught all three at `if i in existing`, so this was never going
to ship -- but it would have refused the batch after the authoring was done.)

## H. `whiteflies`, and applying the composite DRIVER test consistently

Batch 20 kept elderberry's `spotted-wing-drosophila` reuse for a problem NAMED as a composite
("Spotted-wing drosophila and sap beetles") because ONE organism drove the damage and the whole
control was that organism's program.

Nasturtium's "Whiteflies and spider mites" has the same shape and the note says so: whiteflies are
unconditional, while spider mites appear only "in hot dry conditions", and both take the same two
controls. **Whiteflies drive. So it REUSES `whiteflies`** rather than minting a composite, and the
type is `insect`, matching all three existing holders.

The author had independently typed it `insect` on the same reasoning and explicitly noted it did not
choose the type to unlock a method -- correct, and the reason its choice stands. The cost is real
and is filed: "raise humidity with base watering" has no legal home, because `even_watering` is
`[mite, physiological]`.
