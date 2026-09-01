# BATCH 21 (flowers) -- read notes

26 problems, 65 -> **64 rungs** after the read. Note-schema crops, so ladders are short by design.

## R1. RULED: `bt` DROPPED from viola's caterpillar ladder. The safety call of this batch.

The catalog's `bt` caution, verbatim:

> "Bt kurstaki kills the caterpillars of moths and butterflies as a group, including desirable
> species such as swallowtails and monarchs; spray only plants with a pest problem, **never butterfly
> host plants**"

**Viola IS a butterfly host plant.** Fritillary larvae depend on violets; viola's own note says so.

The author kept the rung, conditioned heavily ("leave native fritillary larvae unsprayed where
butterflies are wanted"), reasoning that the crop's note names Bt and that dropping it would discard
sourced advice. That reasoning was careful and it is the right instinct in general. It fails here on
a specific point the author itself supplied: **Bt "does not sort a pest larva from a fritillary."**
Applied to a leaf, it kills whatever caterpillar eats that leaf.

So the conditioning asks the reader to do something the material cannot do. That is not a hedge, it
is an **incoherent recommendation**, published on a plant the catalog explicitly excludes.

**Dropped.** The ladder is now `handpick` alone, which is honest and is what the note actually asks
for: handpicking DOES let you sort fritillaries from pests, which is the whole point of the
qualification.

**FILED as a prose defect:** viola's own note recommends Bt on a butterfly host, contradicting the
catalog's own caution. The note is what should change. **Flagged for Trevor to overrule if he
disagrees -- this is a content call, not a mechanical one.**

## R2. RULED: `whiteflies-and-mites` -> reuse `whiteflies`

See `PINNED_IDS.md` section H. The composite driver test from batch 20, applied consistently.

## R3. CORRECTED: `cutworm` -> `cutworms`, and the split is a CLASS

My pin said reuse the singular "to avoid creating a split". Measured, the split already exists and
the singular is the minority:

| singular | holders | plural | holders |
|---|---|---|---|
| `cutworm` | 1 (asparagus) | `cutworms` | 8 |
| `flea-beetle` | 1 (swiss-chard) | `flea-beetles` | 31 |
| `japanese-beetle` | 1 (basil) | `japanese-beetles` | 6 |

**Three splits, all 1-versus-many.** Batch 20 found the Japanese beetle case and treated it as a
one-off; it is a systematic class. Sunflower takes the plural. Three one-token repoints (asparagus,
swiss-chard, basil) would retire the class; FILED, not fixed.

## R4. The inversion held, and nasturtium's aphid rung is the evidence

No `trap_cropping`, no "trap"/"decoy" token anywhere in 128 new strings. The aphid ladder is scoped
to "a planting you are keeping" and states the inversion outright:

> "Aphids finding this plant is normal rather than a sign that something has gone wrong, so aim for a
> planting you are happy to look at instead of an empty one."

Two pieces of trap-crop content are consequently UNPLACED and that is correct: the trap-stand tending
obligation ("pull or destroy the planting once heavily loaded") and the trap-stand siting advice.
Both concern the trap USE, which is why you grow the plant, not a control of its own problem.

## R5. Gaps and structural walls

1. **A composite spanning TWO TYPES is structurally unrepresentable.** Whiteflies are `insect`,
   spider mites are not, and one problem carries one type. Typing it `insect` (correctly, whiteflies
   drive) makes `even_watering` illegal, so "raise humidity with base watering" -- which four shipped
   flower crops carry on that exact key -- has no home here. Not fixable without splitting a record
   that is one note.
2. **Soil pH has no method.** Viola's crown rot names high pH as a driver; `raise_soil_ph` exists but
   is the OPPOSITE action (liming for clubroot). No lowering or soil-test method exists.
3. **"Restrained watering" (how MUCH) has no method.** `water_at_the_base` is about WHERE,
   `even_watering` is mite/physiological, `bottom_watering` is trays. Third batch running that a
   watering-quantity lever has no home.
4. **A conceded chemical with no material named.** Sunflower's rust note says "fungicides exist for
   severe pressure but are seldom needed" without naming one, so no legal rung exists. Same for its
   defoliators ("spot-treat at high densities"). The schema cannot represent "a chemical exists and
   we decline to name it."
5. **Aster yellows: leafhopper vector management is illegal on a `bacterial` type**, and nasturtium
   has no leafhopper record to carry it. Cosmos solved this by having a separate `aster-leafhoppers`
   insect problem; nasturtium cannot.
6. **Head/fruit covering has no key.** Sunflower's paper-sack-over-one-head technique used
   `bird_netting`, whose MEANS is a hoop frame sealed to the ground. Flagged by its author.

## R6. Register asymmetries -- SEVEN, all the same shape (hedged seasoned, flat beginner)

nasturtium: flea beetles (beginner gives NO control at all), whiteflies, aphids.
sunflower: rust (beginner never learns a chemical exists), downy mildew, sclerotinia.
viola: **caterpillars -- the beginner note says "pick them off or use Bt" with NO butterfly caveat at
all**, which is the same defect class as R1 and arguably its source.

Every rung was written to the HEDGED version. The crops' own beginner notes are what should change.

## R7. Two severity/prose tensions on sunflower, filed

`Birds and squirrels` is `severity: high` on a problem its own note calls "a feature, not a problem"
for growers who want the seed, and `Sunflower moth` is `severity: medium` while the note prescribes
tolerance. A renderer sorting by severity puts a one-rung opt-in problem at the top of sunflower's
list.
