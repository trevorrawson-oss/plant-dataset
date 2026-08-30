# PLA-8 batch 12 -- what the read found and did NOT fix

Written 2026-08-28 while laddering `broad-beans-fava`, `brussels-sprouts` and `parsley`.
Base 745e56cd (batch 11's output). **Everything here is FILED, not fixed.** The batch's job is
ladders; each item below is either out of its blast radius or wants a decision rather than an edit.

Items are ordered by how much they could cost, not by how easy they are.

---

## 1. `note_seasoned` IS UNGATED, AND 53 RUNGS DO NOT HAVE ONE

The dataset's dual-register standard is core to it, and `control_ladder_gate.py` **never mentions
`note_seasoned`**. Nothing checks that a rung has one. Measured over the whole roster:

| crop | rungs with no `note_seasoned` |
| -- | -- |
| broccoli | 19 of 30 |
| celery | 18 of 25 |
| artichoke | 8 of 30 |
| asparagus | 7 of 20 |
| microgreens-mix | 1 of 7 |
| **total** | **53 rungs, 5 crops** |

All five predate the discipline the batch promotes enforce (`validate_batch` refuses an empty note
and refuses identical registers, so nothing shipped since batch 1 can have this shape). broccoli is
the ladder PILOT, which is where the gap starts.

**Not yet established: what the renderer does with a missing seasoned note.** It may fall back to
the beginner register, or it may render nothing for that rung to a seasoned reader. That is a
plant-astro question and it decides whether this is cosmetic or 53 blank rungs in the live product.
**Answer it before pricing the backfill.**

**A GATE FOR THIS IS DELIBERATELY NOT ARMED.** A new roster-wide gate wired before its data lands
floods the parallel session's gauntlet, and the trap-cropping backfill touches broccoli's siblings
right now. This belongs after the fall block, gate and backfill together.

---

## 2. fava's root-rot record is a PEA record's twin anchored to BEAN documents

`broad-beans-fava` / "Root rots and seed decay":

- Its treatment prose is a near-verbatim twin of `snow-peas`' -- "There is no rescue for rotted seed
  or collapsed seedlings; replant... into warmer, better-drained conditions once the soil has
  dried", sentence for sentence.
- Its two anchors are both *Phaseolus* bean pages: `umn_ext`
  `extension.umn.edu/vegetables/growing-beans` and `umass_ext`
  `nevegetable.org/crops/bean-snap-lima-and-dry`.
- Fava is *Vicia faba*: not a pea, and not a *Phaseolus* bean.

So the prose appears templated from one crop while the citations point at a third. This is the
template-inheritance shape that has carried claims across crops before. **It did NOT affect this
batch's ladder** (all four rungs are generic legume root-rot culture that holds whichever document
you read), which is why it is filed rather than chased: repointing anchors is citation-campaign
work and should be priced as such, not done mid-batch.

Same crop, smaller version: "Bean seed fly" anchors to UC IPM's **dry-bean** seedcorn maggot page
(organism-correct, crop-wrong, and defensible) plus a generic UMN "growing beans" page that
supports none of the entry's specific claims.

---

## 3. The roster is SPLIT on whether downy mildew is a fungus

An authoring agent flagged fava's downy mildew for calling the pathogen "the downy mildew fungus"
when downy mildews are oomycetes, and noted that the root-rot entry in the same record correctly
says "fungi and water molds".

**Checked before filing, and the framing changes: of 28 `downy-mildew` records that name a causal
class, 15 say fungus/fungi and 13 say oomycete/water mold.** Fava is not an outlier; it is on the
larger side of a near-even roster split. This is one ruling to make once, not a crop to correct.
It is also a genuine consumer-copy question rather than a purely technical one: "fungus" is the
word a gardener knows.

Note the narrower point still stands on its own: within fava's single record, two entries use
different vocabulary for the same class of organism.

---

## 4. brussels sprouts' harlequin bug: the two registers disagree on the insect's COLOR

- `symptoms_beginner`: "Shield-shaped **black-and-orange** (or black-and-red) bugs"
- `symptoms_seasoned`: "brightly **black-and-yellow** or black-and-red"

This is an identification detail, which is the half of a pest entry a reader acts on before
anything else. The ladder was authored around it (the beginner note says "brightly marked" and
takes no side, the seasoned note follows the seasoned register), but the source should pick one.

---

## 5. parsley's `carrot-rust-fly` entry fuses TWO organisms under one id

The record is named "Carrot rust fly and carrot weevil" and covers *Psila rosae* plus the carrot
weevil. The id `carrot-rust-fly` names only the first, and `planting_time_avoidance` was sourced
against the **fly's** generations specifically -- the timing advice may not transfer to the weevil.
Both rung registers say "flies" rather than implying weevil coverage, which is the honest reading
of the source, but the entry is arguably two problems.

**Not split in this batch**: a ladder batch places controls, it does not restructure a crop's
problem set, and splitting would mint an id (`carrot-weevil`) whose ladder nobody has authored.
Precedent exists both ways -- `cabbageworms` also covers two organisms under one id.

---

## 6. brussels sprouts' cabbage root maggot is framed spring-shaped for a fall crop

The entry says "worst in cool, wet soil" and "most active in cool, damp weather" without naming a
season. Brussels sprouts is normally set out in summer for a fall harvest, so the risk window as
written may not be the one this crop's readers face. The rungs deliberately say "cool, wet
establishment" rather than importing the shipped siblings' "cool, wet spring establishment". The
source may want a brussels-specific timing sentence.

---

## 7. Two catalog entries whose `best_use` is narrower than their shipped use

Neither blocked this batch; both are the pattern first recorded in batch 3 (`best_use` narrower
than shipped use on 11 of 49 methods).

- **`reflective_mulch`**: `best_use` scopes it to "vegetables with a local history of
  aphid-transmitted virus", with squash/melon/cucumber as the documented cases. It is live on **17
  rungs**, most of them plain aphids, thrips and whiteflies with no virus named (green-beans-bush,
  both peas, three squashes). Used again here on brussels sprouts and fava, both prose-sourced.
  The mechanism (disorienting alighting aphids) is the same; the stated reason is narrower than the
  practice.
- **`prompt_harvest`**: its `best_use` is fruit-crop shaped ("over-ripe or fallen fruit feeds the
  problem"), but dill, cilantro and now parsley all use it for taking a leaf crop off ahead of
  foliar lesions. Three crops is a convention forming; rule it once rather than per crop.

---

## 8. Advice with no catalog home, recorded so the next catalog round can price it

Written up separately and in full in `docs/2026-08-28-pla8-disease-escape-sowing-gap.md`:
**disease-escape sowing** (7 instances on 7 crops, 6 of them already shipped).

Also unplaced by this batch, and NOT yet measured:

- **"Sow into warm soil so the seedlings outrun the pest"** -- a vigor / grow-through concept, not a
  calendar one. Present on corn cutworms (x4), corn flea beetles (x4), jalapeno, okra and fava's
  bean seed fly. Currently carried inside adjacent rungs' notes on the shipped ladders. Needs its
  own measurement pass before anyone prices it.
- **"Grow summer savory nearby"** (fava aphid) -- companion planting. Explicitly NOT trap cropping;
  no key, and no rung was authored either way.
- **"Relocate the larvae to a sacrificial plant" / "grow extra parsley as a swallowtail host"** --
  conservation, the caterpillars end alive. A documented exclusion from the trap-cropping round,
  guarded against in this promote so no later pass "finishes the job".
- **"Pinch out the growing tip once the lower pods have set"** (fava aphid) -- PLACED, under
  `garden_sanitation`, whose `best_use` covers pulling affected tissue in season. Recorded because
  it is the crop's primary control resting on a general-purpose key.
