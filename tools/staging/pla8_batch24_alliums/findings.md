# Batch 24 (alliums) -- findings

## 0. THE PREMISE I GAVE THE AGENTS WAS WRONG, AND TWO OF THEM REFUSED IT

`pinned_ids.json` claimed 3 template twins against spring-onion and instructed the onion and shallot
agents to copy spring-onion's shipped ladders BYTE-FOR-BYTE for them. **There are zero template
twins.** My scan compared the 8 FULL-schema fields (`symptoms_*`, `organic_treatment_*`,
`prevention_*`) on crops that do not carry them: leek, onion and shallot use
`identification_*`/`management_*`, so **6 of the 8 compared fields were `None` on both sides and the
tuples matched on ABSENCE.** Re-measured on the fields these crops actually have, all three share
only `cause_beginner`/`cause_seasoned` and **differ on both `management_*` fields**, which is where a
ladder comes from.

**Both agents measured instead of complying, and the copy would have shipped two defects:**
* `onion`/`onion-thrips` -- onion's `management_seasoned` names **reflective mulch** and
  spring-onion's does not, which is exactly why spring-onion's shipped ladder has one rung fewer.
  A verbatim copy DROPS a sourced control.
* `onion`/`fusarium-basal-rot` -- spring-onion's `resistant_varieties` note says "Not every
  **scallion** is offered that way." A verbatim copy puts "scallion" inside the onion record.

**The real management relative is GARLIC, not spring-onion**: onion/`onion-thrips`'s
`management_seasoned` is byte-identical to garlic's, and both onion and shallot found this
independently. Any divergence guard for this batch must be re-derived per schema and on a garlic
axis, not inherited.

This is the same defect class as an optional-field gate going vacuous: a comparison over fields that
do not exist reports identity where there is only absence. **In a schema-split batch, every
cross-crop prose comparison must use the field set the crop actually carries.**

## 1. ONE DECLARED PROPAGATION, to be PINNED in the promote

`onion`/`onion-thrips`/`water_spray` is **byte-identical to spring-onion's shipped rung**, and this
is deliberate and correct rather than a copy defect. The water-spray CLAIM is word-for-word shared
between the two records ("hose off light infestations" / "spray them off with water if thrips are
light"); only the surrounding field differs (onion adds reflective mulch, and says "onions" where
spring-onion says "alliums"). Where the sourced claim is identical, a cosmetic divergence is the
batch-3 defect. It must be ASSERTED in the promote as a declared identity, not left to chance --
and a batch-23-style precedent-copy guard would refuse it at 1.000 unless the pin is honoured.

The agent could NOT do the same for `onion-maggot`/`floating_row_cover`, whose sourced clauses are
also identical, because **spring-onion's shipped note contains "Pair it with the rotation rung"** --
internal vocabulary in live consumer copy. It wrote a clean equivalent instead.

## 2. THE STRONGEST CATALOG SIGNAL IN THE ARC SO FAR: `even_watering` reaches neither insect nor fungal

`applies_to = ['physiological', 'mite', 'bacterial']`. **All FOUR agents reported it independently**,
on at least six problems:

| crop | problem | the blocked instruction |
|---|---|---|
| chives | onion-thrips | "Keeping plants unstressed and watered blunts outbreaks" (in three separate fields) |
| leek | onion-thrips | "Keep plants vigorous and evenly watered" |
| leek | pink-root | "keep plants unstressed and evenly watered" -- **unrepresented in any rung** |
| onion | onion-thrips | "Keep plants vigorous and watered" |
| onion | pink-root | "Keep plants unstressed" |
| shallot | onion-thrips, pink-root | same shape |

Roots reported the same gap three times (potato x2, sweet-potato x1) and it was already on the r10
queue as "general plant vigor". Four independent reports in one batch is the playbook's own trigger.
Note the method's MEANS **already** describes holding spider mites down on plants "left dry and
stressed", so the vigor-against-a-pest mechanism is in the text; only the target set excludes insects.

## 3. NEW GAP: spatial separation from a pressured neighbouring allium planting

chives reports it on **3 of its 4 pests** ("avoid siting chives beside heavily thrips-pressured onion
or garlic plantings"; "separate new plantings from pressured allium beds"; "do not crowd alliums
together"). It is neither `crop_rotation` (moves a planting in time, off its own history) nor
`airflow_spacing` (disease-only, and its rationale is humidity, not host concentration).
**Consequence: chives/`onion-thrips` has no cultural bed-choice rung at all**, because its thrips
prose carries separation advice and no rotation advice.

## 4. NEW GAP: the perennial "shear the clump and let it regrow clean" reset

chives' signature move, carried on 5 of its 8 problems inside `garden_sanitation`, whose MEANS is
end-of-season cleanup plus pulling first affected leaves. Chives' action is a whole-plant hard
cutback of a perennial clump used as an in-season reset that also re-times regrowth into drier
weather. Closest legal key, but a distinct cultural action and a candidate for its own method.

## 5. `reflective_mulch`'s MEANS has not caught up with its use

Scoped entirely to *aphid-transmitted virus on squash, melon and cucumber*; it now carries THRIPS
rungs on garlic (shipped), onion and shallot. Reported independently by two agents. The key is right
and the crops' prose names it directly; the catalog's explanation text is what is out of date.

## 6. Pre-existing prose defects found while reading. NOT fixed.

1. **chives' `Botrytis (leaf blight and neck rot)` never describes a neck rot.** Every field is
   foliar: sunken leaf spots, dense canopies, splashing water, leaf wetness. There is no curing,
   storage or neck content anywhere, and chives is a cut-leaf crop that is not lifted. **The NAME
   over-promises against its own record**, which is why the pinned id `botrytis-leaf-blight-neck-rot`
   is right for the entry as named and wrong for the entry as written. Either rename the problem to
   "Botrytis leaf blight" or add the neck-rot content the name claims.
2. **"bin" as a verb in live consumer copy** -- leek rust `management_beginner`, "pull off and bin
   badly spotted leaves". British; the American-English rule is a hard rule.
3. **UK flight dates presented as general** -- leek's allium leaf miner gives "about March to April
   and September to November", which is RHS (UK) timing, while the record also cites `umd_ext`
   (mid-Atlantic US) whose windows differ. The hedges are intact but the geography is not stated.
4. **leek moth register mismatch**: `identification_seasoned` says the two generations run "roughly
   May to June and August to October"; both beginner registers say "late spring and late summer",
   which under-covers the second flight by about two months.
5. **chives thrips registers offer different materials**: `organic_treatment_beginner` names only
   insecticidal soap, `organic_treatment_seasoned` adds spinosad, so the spinosad rung necessarily
   introduces that material into the beginner register for the first time.
6. **shallot's pink root is anchored solely to `tamu_agrilife` `onion1.pdf`**, an ONION publication
   cited for a shallot claim. Cross-crop anchor; flagged, not adjudicated.
7. **`autumn` / `fall` split inside leek's record**, seasoned vs beginner, not a designed register
   difference.
8. **152 roster-wide style hits** (internal vocabulary plus absolute words) across ~50 crops,
   measured by the onion agent; spring-onion contributes 3 and garlic 2. Upper bound on candidates,
   NOT on defects -- the absolute half is unadjudicated and several are legitimate ("never move
   infested soil"). The internal-vocabulary half is unambiguous and is consistent with the 130
   measured during batch 23. It is why "copy the sibling verbatim" is unsafe as a general policy.
