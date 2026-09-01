# BATCH 22 (stragglers) -- read notes

26 problems, **135 rungs, unchanged by the read**. Full-schema crops with laddered siblings, so the
ladders are long and the hazard is not thin authoring but SILENT DIVERGENCE FROM A SIBLING.

All 135 rungs were read against their own record and against their method's `best_use`. **No rung
was changed.** Everything below is either a ruling that confirms what was authored, or a defect
filed against data this promote does not touch.

## R1. RULED: pumpkin/downy-mildew KEEPS `wet_foliage_discipline`, and the three squashes have the gap

The one template-twin divergence in the batch. pumpkin's downy-mildew source prose is **byte-
identical across all eight fields** to butternut, acorn and spaghetti squash, and pumpkin's ladder
carries one rung they do not.

The shared `prevention_seasoned` ends: "...and **avoid working among wet vines**."

`wet_foliage_discipline` means, verbatim from the catalog:

> "applied by choosing WHEN you work rather than what you apply. Distinct from watering at the base,
> which changes where the water goes; this one changes where you go, and it still applies after rain
> or dew, which no irrigation choice controls."

That is exactly the sentence's instruction, and pumpkin's rung note draws the method's own
distinction unprompted. **The rung is supported. The three squashes are the ones missing it.**

Measured roster-wide: **34 laddered problems carry an instruction to time work to dry foliage, and
13 of them have no such rung** (jalapeno/bacterial-spot; cucumber, slicing-cucumber and
pickling-cucumber at downy-mildew and angular-leaf-spot each; sugar-snap-peas and snow-peas at
powdery-mildew; swiss-chard, butternut-squash, acorn-squash, spaghetti-squash at downy-mildew).
**Filed, not fixed** -- editing shipped crops here would trip this promote's own bystander check.

Pinned as the single entry in `TEMPLATE_DIVERGENCE_PINS`, so neither the rung nor the reason can
drift silently.

## R2. RESOLVED: the handoff's pumpkin "template defect" is NOT a defect

The handoff recorded: "the three cucumbers' downy-mildew treatment reads 'apply a labeled fungicide
**such as copper or chlorothalonil**'; pumpkin's is byte-identical **with the product list
removed**. Adjudicate whether the products were lost or UGA C1206 names none."

Read: pumpkin's prose is byte-identical to the **SQUASHES**, not to the cucumbers. There are two
templates, not one stripped copy of another:

| family | treatment prose | ladder |
|---|---|---|
| cucumber, slicing-, pickling- | "...such as copper or chlorothalonil..." | + `copper_fungicide`, `chlorothalonil` |
| butternut, acorn, spaghetti, **pumpkin** | "...a labeled fungicide..." (no products) | no spray rung |

**Pumpkin honestly carries no spray rung and is consistent with its actual siblings.** Whether the
squash template *should* name products is a source-truth question about three shipped crops, not
about this batch.

## R3. CONFIRMED: `bacterial-wilt` on pumpkin -- batch 21's trap, mirrored

Batch 21 refused this id for nasturtium because nasturtium's wilt is *Ralstonia* (soilborne, rotate
away) while the roster id is *Erwinia tracheiphila* (survives inside cucumber beetles).

Pumpkin's record states the beetle-gut mechanism in both registers and makes **no soil-persistence
claim**, which is the exact tell. Pumpkin also carries `cucumber-beetles` as its own problem. The id
that was a trap one batch ago is the right reuse here. **The organism decides.**

## R4. RULED: two mints sit beside a SHORTER roster id that names a WIDER problem

Neither was in `PINNED_IDS.md`. Both were found by a substring scan of all 20 authored ids against
the roster, run because an exact-id check -- batch 21's own fix -- passes an id that merely
*resembles* a live one.

**`bacterial-blight` (mint) beside `bacterial-blights` (3 holders).** Not a singular/plural split.
The plural is plural because it names TWO organisms:

> *Xanthomonas campestris* pv. *phaseoli* (common blight) and *Pseudomonas syringae* pv.
> *phaseolicola* (halo blight)

on *Phaseolus* beans. Edamame's is *Pseudomonas savastanoi* pv. *glycinea* alone, on *Glycine max*.
Different disease, different id.

**`cucumber-mosaic-virus` (mint) beside `cucumber-mosaic` (calendula).** calendula's record is the
COMPOUND "Cucumber mosaic **and aster yellows**" -- an aphid-vectored virus and a leafhopper-
vectored phytoplasma under one id. english-cucumber's problem is the single virus. Since an id is
the join key a `varieties[].resistance` grade hangs off, merging them would assert that resistance
to CMV is resistance to aster yellows.

**These are the OPPOSITE of the singular/plural class**: there the two ids name the same problem;
here the shorter id names a wider one. `check_scope_variant_ids_not_merged` pins both on the
organism and the compound scope, not on the id strings.

## R5. FOUND: a FOURTH lone-crop minority-id variant

The same substring scan flagged **artichoke's `botrytis-gray-mold` (1 holder)** against the majority
`gray-mold` (5 holders) -- the same organism, *Botrytis cinerea*. english-cucumber correctly takes
the majority id.

The filed "three one-token repoints would retire the class" is **four**: asparagus `cutworm`,
swiss-chard `flea-beetle`, basil `japanese-beetle`, artichoke `botrytis-gray-mold`.

## R6. FILED: THREE banned absolutes are live in shipped consumer prose, not one

The handoff recorded only edamame's. A scan of all pre-state prose on the three crops found three,
one per crop:

| crop | field | text |
|---|---|---|
| english-cucumber | Downy mildew `organic_treatment_seasoned` | "Water at the soil line, **never** overhead" |
| edamame | SCN `prevention_beginner` | "**never** grow soybeans in the same spot every year" |
| pumpkin | Phytophthora blight `organic_treatment_seasoned` | "**never** let water stand" |

**None is carried into any rung.** The reason the batch tooling did not surface them:
`ladder_batch verify`'s absolute scan checks always/guaranteed/completely/totally/harmless and
**omits "never"**, while the promote's own `hygiene()` includes it. Two checks that read as the same
check are not. Worth reconciling before batch 23.

## R7. FILED: english-cucumber powdery mildew has an inverted register pair

`prevention_beginner` names the cultivar Tyria; `prevention_seasoned` generalizes to "tolerant
varieties". The seasoned register should be the more specific one. The authored rung follows the
record but adds a genuinely seasoned framing ("resistance varies across the English types, so check
the specific variety rather than the class"), so the ladder is sound and the record is what should
change.

## R8. Notes on placement, all accepted

* **english-cucumber CMV's weed-reservoir advice sits inside `garden_sanitation`** because
  `weed_host_control` cannot reach `viral` (`applies_to` is `insect_soft_bodied`, `fungal_foliar`).
  The rung's primary action -- roguing a plant that cannot be saved -- IS `garden_sanitation` by the
  catalog's own contrast clause in `prune_out_infection`. An aphid-vectored virus with a named weed
  reservoir is the textbook case for the method that cannot take it; filed as the strongest instance
  of that catalog gap.
* **pumpkin's squash-bug board trap sits inside `handpick`.** The board concentrates the bugs; the
  action is still hand-collection. Correct placement, not a gap.
* **pumpkin's preventive vine-burying has no method.** The reactive version is inside
  `borer_stem_surgery` ("bank damp soil over that joint"); the standing practice "bury vines at the
  joints as they run" is unplaced. Filed.
* **Several methods' `best_use` prose is narrower than their `applies_to`** -- `spinosad` names no
  beetles but admits `insect_chewing`; `yellow_sticky_traps` names no beetles; `water_spray` names
  aphids but admits `mite`; `straw_mulch` is strawberry-scoped. Every such rung here is
  record-supported and gate-legal. But the prose is what an author reads when deciding whether a
  rung fits, which is the batch-1 `bottom_watering` failure mode. Filed.

## R9. What the read did NOT change

Zero rungs added, removed or reworded. The authoring was strong: every divergence from a sibling
traces to the crop's own record, and several rungs explicitly explain their own divergence in prose
(english-cucumber's downy mildew: "This crop's guidance names copper and stops there, so nothing
heavier is offered for it on this crop"). Copy hygiene was clean on all 270 strings under the
promote's stricter `hygiene()`, and the prose-echo scan found 0 whole-note and 0 sentence echoes
against a 5,351-note shipped corpus.
