# BATCH 20 (berries) -- read notes

## R1. RULED: elderberry's `Spotted-wing drosophila and sap beetles` KEEPS the reuse

The elderberry author was asked to judge whether sap beetles are co-equal or secondary, and answered
**co-equal**, on structural grounds: all four descriptive fields give the two organisms parallel
grammatical billing, in both registers. That evidence is real and correctly gathered.

**I read the record and ruled the other way.** The grammar is parallel; the biology and the control
are not.

* `cause_seasoned`: *"Spotted-wing drosophila (an invasive vinegar fly) lays eggs in **healthy ripe
  fruit**; sap beetles are drawn to **overripe and split** berries."* SWD CREATES the damage; sap
  beetles EXPLOIT it. That is a primary and a secondary colonizer, which is what the agent's own
  quotation shows even as it argued for equal billing.
* `organic_treatment_seasoned` is the SWD program verbatim: *"Harvest ripe clusters frequently and
  completely, and remove fallen or overripe fruit... Monitor with apple-cider-vinegar traps."*
  Nothing in it is a sap-beetle-specific action. Removing overripe fruit is what denies the beetles
  their substrate, so the one program covers both.

**The ladder encodes the CONTROL, and the control is SWD's.** The join is therefore honest. Minting
a composite would also drop elderberry out of the joins for a marquee invasive whose management is
identical across six crops (strawberry, cherry-sour, cherry-sweet, blackberry, blueberry, raspberry).

**Where the agent's finding DOES land: the problem NAME over-promises relative to its own cause and
treatment fields.** The cleaner fix is on the PROSE side, not the id side. Filed as a naming
observation, not actioned.

### The agent's secondary observation is correct but is not a problem

It noted that this id already spans very different response levels: strawberry's ladder reaches
`spinosad` and `pyrethroid`, elderberry's stops at monitoring. **That is exactly what batch 18's
divergence rule permits** -- a shared id MAY carry different ladders where the RECORDS differ, and
elderberry's record names no chemistry at all while strawberry's does. Not a defect.

## R2. Cross-batch divergence applies again, and is WIDER than batch 19's

Six ids in this batch already live on already-shipped crops:

| id | existing holders |
|---|---|
| `spotted-wing-drosophila` | strawberry, cherry-sour, cherry-sweet |
| `birds` | strawberry, cherry-sour, cherry-sweet |
| `aphids` | ~50 vegetable crops |
| `scale-insects` | the five citrus |
| `japanese-beetles` | marigold, zinnia, echinacea |
| `powdery-mildew` | many |

The batch 19 guard shape (`check_cross_batch_divergence`, comparing against CANONICAL rather than
only the staging directory) is REQUIRED here too. Note `aphids` and `powdery-mildew` are broad
generics with many holders and many existing ladder shapes, so the guard must be scoped to permit
that rather than demanding one shape across 50 crops. **Design the guard for this batch before
writing it; do not copy batch 19's assumption that a shared id has one shape.**

## R3. Gaps reported by the elderberry author, carried forward

1. **"Keep the plant vigorous" has NO catalog method**, and it appears in THREE elderberry records
   (`elder-borers`, `japanese-beetles`, `cane-canker-dieback`). The near-misses are wrong:
   `even_watering` is `[mite, physiological]` and means steady moisture against calcium disorders;
   `water_at_the_base` means splash suppression. Silently dropped from three ladders. This is the
   same class as the citrus "keep trees unstressed and not dusty" gap, now seen on a second crop
   family -- **two families independently blocked on general plant vigor.**
2. **Turf grub management** (Japanese beetles) has no method. The author correctly REFUSED
   `beneficial_nematodes`, whose MEANS is soil-stage larvae drenched into trays, and which the
   record never names. That refusal is the `bottom_watering` discipline applied correctly.
3. **Wound avoidance** (cane canker) has no method; carried inside a `prune_out_infection` note,
   which has shipped precedent on apricot and cherry-sour bacterial canker.
4. **Fruit cooling after harvest** (SWD) has no method; carried inside `prompt_harvest`, matching
   the shipped cherry ladders.

## R4. Loose fits flagged by the author, to check at the read

* `resistant_varieties` for the Bob Gordon cyme droop on `birds`. The mechanism is FRUIT
  PRESENTATION (an inverted cyme hides berries), not genetic resistance or pest preference. The
  catalog does extend the key to "varieties a pest is less drawn to, like a tight corn husk against
  earworm", which is the same shape. Judged in scope, but if `varieties[].resistance` ever grades
  elderberry against `birds`, the grade would be about cyme orientation.
* `weed_host_control` for the rust's alternate host. Right key, but the catalog frames it around
  ANNUAL BEDS while this is an obligate alternate host for a host-alternating *Puccinia* on a
  perennial shrub. Correct, under-described by the catalog text.
* `garden_sanitation` does three jobs in this one crop (in-season cane removal, dormant renewal
  pruning, excision of rusted shoots) and appears five times.

## R5. Register asymmetries found by the author (hedged seasoned, flat beginner)

Three instances, all the same shape and all written to the HEDGE in the rungs:

* `birds`: seasoned *"widely the number-one competitor"*; beginner drops "widely".
* `powdery-mildew`: seasoned *"rarely harm an **established** shrub"*; beginner drops "established".
* `japanese-beetles`: beginner *"A strong elderberry handles a few beetles fine"* is stronger than
  seasoned *"usually outgrows the damage"*.

Same class as lime anthracnose's beginner absolute in batch 18. The existing prose is what should
change; the rungs already carry the hedge.

---

## R6. SIX MIS-POINTED SOURCE KEYS, FOUND BY TWO INDEPENDENT AUTHORS AND VERIFIED

Both reports were checked against the data and both are **exactly right**.

**raspberry** -- `cornell_ext` resolves to `https://fruit.cornell.edu/spottedwing/hosts/` on FIVE of
its ten problems:

| problem | plausible? |
|---|---|
| Spotted-wing drosophila (SWD) | YES, this is the correct anchor |
| Raspberry cane borer | NO -- a longhorn beetle that girdles canes |
| Raspberry crown borer | NO -- a clearwing moth in the crown |
| Aphids | NO |
| Raspberry mosaic virus complex | NO |

**blueberry** -- `umaine_ext` resolves to
`https://extension.umaine.edu/blueberries/factsheets/insects/210-spotted-wing-drosophila/` on BOTH
its SWD problem (correct) and its **blueberry maggot** problem (wrong: *Rhagoletis mendax* is a
different fly, and the record's maggot-specific claims -- banded-wing adult, June-August flight, one
egg per berry, pupae surviving composting -- cannot come from an SWD factsheet).

### This is now a MEASURED, RECURRING defect class, not three anecdotes

| batch | instance |
|---|---|
| 17 | plum's San Jose scale citing a mealy plum aphid page |
| 18 | lemon's mealybug and sooty-mold ant claims citing an INDEX PAGE with no ant content |
| 20 | these six |

**The shape is consistent: a crop's problems share ONE source id whose URL is specific to ONE of
them.** That is mechanically detectable -- flag any node whose cited URL contains a pest/disease
term that does not appear in that problem's own name or prose. Worth building as a scan; NOT built
here, and deliberately not scoped into this batch.

**Not fixed in batch 20.** A repoint is its own change with its own blast radius, and these citations
are not what this batch writes. Filed.

## R7. RULED: `resistant_varieties` may NOT carry PHENOLOGICAL ESCAPE

Two authors hit the same sentence ("choose early-ripening cultivars to dodge peak fly pressure" on
SWD) and made OPPOSITE calls:

* **blueberry REFUSED it**, reasoning that the catalog calls `resistant_varieties` "the natural
  handoff to variety-level resistance data", so using it for escape-by-timing would seed a FALSE
  RESISTANCE SIGNAL on a live join key.
* **raspberry USED it**, and flagged it as the loosest of its four loose fits.

**blueberry is right, and this is the same shape as the batch 19 `garden_sanitation` call: two
authors split, and the refuser was correct.** The key feeds `varieties[].resistance`. An early
cultivar is not a resistant cultivar; it escapes exposure. Recording a grade against it would assert
susceptibility data the source never gave.

**APPLIED: dropped the `resistant_varieties` rung from BOTH raspberry's and blackberry's
`spotted-wing-drosophila` ladders** (6 -> 5 rungs each; batch total 142 -> 140).

Blackberry hit the same sentence independently, used the key, flagged it, and added the
decisive datapoint: it searched the roster and found **ZERO shipped precedent** for
earliness-escape under `resistant_varieties`. So the tally was 2 used / 1 refused, and the
refuser was still right -- a majority of authors reaching for a key is not evidence the key
means what they need. Both users had flagged it as their loosest fit, which is the signal.
Elderberry's `birds` use of the same key for the Bob Gordon cyme droop is a SEPARATE question and
survives, because the catalog explicitly extends the key to "varieties a pest is less drawn to, like
a tight corn husk against earworm" -- non-preference IS a varietal trait of the plant, whereas
ripening date is a calendar accident. Noted so the two decisions are not read as inconsistent.

## R8. CATALOG GAPS, now with a THIRD independent confirmation

1. **"Keep the plant vigorous" has no method** -- reported by elderberry (3 records), raspberry
   (2 records) and blueberry (scale). **Three crops, three independent authors, one batch**, on top
   of citrus's "keep trees unstressed and not dusty". The playbook's own rule is that several bots
   blocked on the same control means the CATALOG. This is now the best-evidenced mint candidate on
   the board.
2. **Burying overwintering inoculum has no method, and the nearest key CONTRADICTS it.** Blueberry's
   mummy berry control is *"shallowly cultivate or mulch under bushes in late winter to bury
   overwintering mummies before their spore cups form"* -- half the two-stage cycle. Every mulch key
   is a splash/contact barrier laid at planting, `off_season_tillage` is insect-only, and
   `garden_sanitation`'s own CAUTION reads *"Destroy diseased debris rather than leaving or BURYING
   it."* Folding it in would have contradicted the method it sat under. Sharp catch; strong mint
   candidate.
3. **Dormant lime sulfur has no key.** Raspberry and blackberry both name it for cane anthracnose,
   and "lime sulfur" appears in exactly those two crops corpus-wide. The catalog's `sulfur` is an
   in-season wettable protectant with an in-season heat caution; delayed-dormant calcium polysulfide
   on bare canes is a different material, timing and caution set. ONE mint would cover both crops.
4. **Exclusion netting on a non-SWD fly has no key.** `bird_netting` is vertebrate-only,
   `swd_exclusion_netting` is used on exactly three problems roster-wide and all three are SWD, and
   `floating_row_cover` means bed-level transplant fabric. Blueberry maggot's "netting also excludes
   the adult fly" is unplaceable.
5. **`airflow_spacing` cannot reach an insect type**, so the airflow half of blueberry's scale advice
   and raspberry's "open the canopy" SWD advice are both structurally unplaceable. This is an
   `applies_to` artifact rather than biology, same class as the citrus `even_watering` note.
