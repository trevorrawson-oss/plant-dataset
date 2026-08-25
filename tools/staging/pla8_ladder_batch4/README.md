# PLA-8 ladder rollout -- BATCH 4, the five squashes. READ COMPLETE.

5 crops: yellow-summer-squash, zucchini-courgette, acorn-squash, butternut-squash,
spaghetti-squash. 31 problems, **139 rungs** (23 + 23 + 31 + 31 + 31). Canonical at authoring time:
`5696aead`; promoted onto `e40cd8ec` after the catalog round that minted `borer_stem_surgery`.

## The first HYBRID batch: a true twin AND a shared-name family in one cut

The corrected family cut (`c1cd161`) makes this possible to see. Verified field by field BEFORE
authoring, not assumed:

| group | identity | handling |
|---|---|---|
| yellow-summer-squash + zucchini-courgette | **40/40 = 100%** | ONE authoring pass, propagated, identity ASSERTED |
| acorn + butternut + spaghetti | 73.2 / 80.4 / 73.2% | THREE authoring passes, distinctness ASSERTED |

So the promote holds both premises at once, in opposite directions: batch 2's promote refuses if its
corns DIVERGE, batch 3's refuses if its cucumbers CONVERGE, and this one does both. **4 authoring
passes for 5 crops.**

### Distinctness here is about PROSE, not method keys

The trio converges on IDENTICAL method sequences, and that is correct: same seven problems, mostly
shared prose, and none of the crop-distinct variety claims that made batch 3's cucumbers diverge in
methods. Every note differs. Comparing method keys refused this batch on its first dry run, so
`verify_post` compares full ladder CONTENT and a test pins the ruling so re-tightening it fails loud.

## THE CROSS-SIBLING CHECK PAID FOR ITSELF ON ITS FIRST REAL BATCH

`ladder_batch.cross_sibling_conflicts` (built in `07ddc0a` from batch 3's hand-found defect) reported
**3 rows**, and two were real defects:

1. **Downy mildew, acorn vs butternut AND acorn vs spaghetti -- ALL EIGHT prose fields identical**,
   yet butternut and spaghetti authored a `copper_fungicide` rung and acorn refused. **Acorn was
   right.** These crops' prose says only *"a labeled fungicide"* and names no material; certified
   cucumber's says *"a labeled fungicide such as copper or chlorothalonil"* and NAMES copper. Putting
   a product in front of a reader that the crop's own prose does not carry is what the
   restate-from-own-prose rule forbids. **Copper removed from two ladders.** The mirror of batch 3,
   where the same check's finding was resolved by ADDING a rung.
2. **Squash vine borer, acorn vs spaghetti** -- spaghetti carried a `handpick` rung where acorn
   refused entirely, with both `organic_treatment_*` fields identical. Resolved by the catalog mint
   below.

After the fixes the check reports **none**. That is the check confirming its own corrections.

## The catalog was the gap, and three agents said so independently

acorn, butternut and spaghetti ALL reported the borer's stem surgery unplaceable, and **two rejected
`handpick` by name**, citing that method's own con: *"Misses hidden eggs and tiny larvae."* A larva
inside a stem is the case handpicking is documented to MISS. yellow-summer-squash used `handpick` and
called it *"not literal"* in the same breath. That is the `bottom_watering` trap.

It mattered because stem surgery is the crop's ONLY in-season remedy: five ladders otherwise carried
no action at all for the treatment their own prose leads with. **`borer_stem_surgery` was minted in a
separate catalog round (`cadaa6c`, 50 -> 51 methods)**, scoped to `insect_boring` and nothing else so
the gate can tell it apart from `handpick`, and sourced from two T1 documents fetched and read (UMN,
Iowa State) with both hedges enforced by the promote.

Nine crops carry Squash vine borer. Five are here; watermelon, cantaloupe, pumpkin and honeydew-melon
are not laddered yet, so they get the method during their own authoring rather than through a
backfill promote over shipped crops.

## Third fix: a join-key defect

The summer-squash pair minted `cucumber-beetle` (singular) where the trio and three shipped cucumbers
use `cucumber-beetles`. Ids are join keys for `varieties[].resistance` and `ladder_delta`, and two
independent passes producing different ids for the same problem is exactly what CLAUDE.md's
pin-at-first-authoring rule exists to prevent. Normalized, and the promote now refuses any id that
disagrees with the roster's shipped spelling.

## Rulings made during the read

- **`stem_collars` for the foil wrap KEPT.** yellow-summer-squash's prose says "Wrap the lower stem
  with foil"; the catalog's `best_use` is cutworm-scoped, but shipped broccoli precedent is exact --
  "a disk laid flat on the soil around each transplant blocks the cabbage fly from LAYING EGGS AT THE
  STEM BASE". Same action class. (`stem_collars.best_use` is an 11th instance of the narrow-`best_use`
  class fixed in `6671ecd`.)
- **`resistant_varieties` on the borer KEPT**, with hedges. The claim is species-level (*C. moschata*
  vs *pepo*) or recovery-based ("some growers find they recover better"), not cultivar disease
  resistance. Within the precedent set by cucumber's non-bitter varieties, corn husk cover and apple
  rootstock, and every agent kept the source's hedge explicit.
- **`handpick` DROPPED from the borer ladders entirely.** Egg scouting is stated in yellow's prose but
  egg REMOVAL is not, and scouting is a trigger, not a control. It lives in the surgery rung's note.

## Catalog gaps hit, recorded not forced

Recurring from batch 3, now on their second and third batch: **no plant-vigor method** ("keep young
plants vigorous so they grow past the vulnerable stage", unplaced twice per crop); **no disease-side
nitrogen method** (`balance_nitrogen` is `insect_soft_bodied` only, so "avoid excess nitrogen" is
illegal on powdery mildew); **no biofungicide or potassium-bicarbonate key**, and `neem_oil` /
`horticultural_oil` are insect/mite-scoped, so only the sulfur third of the powdery-mildew advice is
expressible.

New here: **no planting-date / succession-timing method.** "Time a fall succession to crop after the
borer's main flight" is a standard, prominent SVB control named by three of the five crops and it has
no home at all. Strongest candidate for the next catalog round.

## Existing-prose defects found, NOT fixed

1. **A false conjunction on acorn and spaghetti's borer `organic_treatment_seasoned`**: *"Burying vine
   joints ... and removing and destroying infested vines at season's end, BOTH reduce next year's
   brood."* Burying joints is a plant-survival tactic; keeping an infested plant alive arguably
   sustains the larva. Both T1 sources attribute brood reduction only to destroying infested vines.
   The rung encodes the correct attribution rather than repeating the error.
2. **A stale anchor**: yellow-summer-squash and zucchini cite `hortnews.extension.iastate.edu`, which
   now 301-redirects. The document is alive; only the URL moved. The mint anchors the live URL; the
   crop repoint is a separate pass.
3. **"Wilt-resistant practices"** (yellow's beetle prevention) is not grammatical -- a practice is not
   wilt-resistant. The ambiguity is what blocked a `resistant_varieties` rung there.
4. **"Individual leaves or runners wilt"** (bacterial wilt symptoms, both twin crops): squash produces
   vines, not runners. Reads as template language carried from a strawberry-shaped crop.
5. Powdery mildew's cause says it does not need leaf wetness while its prevention prescribes base
   watering, on all five crops. Same tension certified cucumber carries; the rungs say so explicitly.

## Harness and gauntlet

**29 injections, 29 caught, 0 survivors**, preflight 30/30, positive control GREEN, sentinel RED. Six
families: hybrid 7, readfix 9, reach 6, blast 4, mechanics 2, ids 1.

**TWO RUNS: 2 survivors, then 0.** The cross-family collision guard was unreachable until a test
copied the twin file over a trio file -- a state where both other grouping checks pass and only it can
object. And `verify_post`'s copper guard is a second line whose first line always fires.

The suite also caught a guard of mine that was **dead from birth**: `check_read_fixes` read
`p.get("name")` off the staged files, which carry only `{id, type, control_ladder}`, so the lookup
always returned None and the id convention was never once enforced. It now resolves the name from
canonical by index.

GATES: `control_ladder_gate` 0; `variety_resistance_gate` 0; `variety_ladder_delta_gate` 0;
`register_completeness` PASS; `gate_all` PASS; copy hygiene 0 across all five checks; cross-sibling
conflicts 0.
