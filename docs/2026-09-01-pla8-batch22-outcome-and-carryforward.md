# PLA-8 BATCH 22 (stragglers) -- OUTCOME, and the carry-forward for batch 23

**Written 2026-09-01. Supersedes `docs/2026-09-01-pla8-batch22-handoff.md`,** which described batch 22
as authored-but-not-merged. It is now merged, read, promoted and gauntleted.

Canonical is `919eabc4` (batch 22, the stragglers).
**Verify first:** `shasum -a 256 crops_data_final.json` must read
`919eabc4d2dae936e3f5b876c52799f5a3a3e3d1983c2c8ac324384ab986c073`.

---

## 1. What shipped

| item | value |
|---|---|
| promote | `tools/promote_pla8_batch22.py`, base `fabdaae1` -> `919eabc4` |
| crops | english-cucumber (9 problems / 50 rungs), edamame (9 / 43), pumpkin (8 / 42) |
| totals | **26 problems, 135 rungs, 4 mints**, catalog steady at 62, source_catalog steady at 218 |
| roster | laddered **91 -> 94** of 121 |
| suite | `tools/test_promote_pla8_batch22.py` -- 103/103, both runners |
| harness | `tools/mutate_pla8_batch22_suite.py` -- **72 injected / 0 survived**, 14 families |

Gauntlet: `gate_all` 121/121, `control_ladder_gate` 0, `register_completeness` PASS,
`whole_crop_gate` PASS x3, `variety_resistance_gate` 0, `variety_ladder_delta_gate` 0,
`release_verify` clean.

## 2. The premise, and why it had to be re-measured

**FULL schema** (`symptoms_*`, `cause_*`, `organic_treatment_*`, `prevention_*`, `sources`,
`anchoring_urls`) -- the batch 17-20 shape. Batch 21 was NOTE schema, so copying its
`check_note_schema_premise` would have refused this batch on its first guard.

**Type: SPLIT BY CROP, the fifth distinct rule in six batches.** english-cucumber and pumpkin set
from nothing; edamame upgraded from coarse (`pest` x5, `disease` x4). Measuring also found an
asymmetry the handoff did not record: **edamame's problems carry `severity`, the other two crops'
do not.** Both are pinned in both directions.

| batch | premise |
|---|---|
| 17 | uniformly coarse -> upgrade |
| 18 | mixed fine/coarse -> two-sided |
| 19 | uniformly fine -> preserve |
| 20, 21 | no type at all -> set from nothing |
| **22** | **split by crop: two set-from-nothing, one upgrade** |

## 3. THE GUARD THIS BATCH NEEDED, AND WHY BATCH 21'S ANSWER DOES NOT TRANSFER

Of 22 reused-id instances, 7 match a shipped sibling exactly and 15 diverge -- almost batch 21's
ratio. **Batch 21 concluded from that ratio that shape comparison is meaningless. That conclusion is
not portable**, because batch 21's crops were companion flowers converging on generic pests, while
these three are TEMPLATE SIBLINGS of laddered crops that share authored prose.

The measurement that decides is the cross-tab of SOURCE-PROSE identity against LADDER identity:

| | ladder matches | ladder differs |
|---|---|---|
| **prose byte-identical** | 6 | **3** (all one problem) |
| prose differs | 3 | 16 |

**9 template twins**, 6 agreeing, 3 diverging -- and all 3 are pumpkin/downy-mildew against
butternut, acorn and spaghetti squash. That is the batch 3 defect shape (cucumber and
slicing-cucumber shared a byte-identical `prevention_seasoned` while one keyed it to
`resistant_varieties` and the other refused), and it is invisible to every gate because it only
exists ACROSS crops. `check_template_sibling_divergence` is the result: where the prose is
identical the ladder must match, with the single adjudicated exception pinned.

Batch 20's "pin every divergence" would have been 15 pins of noise here. Batch 21's "no shape
comparison" would have seen none of it. **Re-measure this every batch; three batches have now
needed three different answers.**

`check_no_shipped_prose_echo` is carried from batch 21 unchanged, re-measured before adoption:
0 whole-note and 0 sentence echoes over 270 batch notes against a 5,351-note / 8,840-sentence
shipped corpus. A REFUSAL-SPEC pass, and worth most exactly where ladders converge.

## 4. Rulings made at the read

1. **pumpkin/downy-mildew's extra `wet_foliage_discipline` rung is CORRECT and the shipped siblings
   are the ones with the gap.** The shared `prevention_seasoned` says "avoid working among wet
   vines"; the method means choosing WHEN you work, explicitly distinct from watering at the base.
2. **The handoff's pumpkin "template defect" was not one.** Pumpkin's downy-mildew treatment is
   byte-identical to the SQUASHES (which name no product and ship no spray rung), not a stripped
   copy of the cucumbers' "such as copper or chlorothalonil". Pumpkin honestly carries no spray
   rung and is consistent with its actual siblings. Whether the squash template *should* name
   products is a source-truth question about three shipped crops, not about pumpkin.
3. **`bacterial-blight` is a correct mint, and it is NOT a fourth singular/plural split.**
   `bacterial-blights` is plural because it names TWO organisms (*Xanthomonas campestris* pv.
   *phaseoli*, *Pseudomonas syringae* pv. *phaseolicola*) on *Phaseolus* beans; edamame's is
   *Pseudomonas savastanoi* pv. *glycinea* alone.
4. **`cucumber-mosaic-virus` is a correct mint.** calendula's `cucumber-mosaic` is the COMPOUND
   record "Cucumber mosaic **and aster yellows**" -- a virus plus a leafhopper-vectored phytoplasma
   under one id. Merging would make a `varieties[].resistance` grade assert that CMV resistance is
   aster-yellows resistance.
5. **`bacterial-wilt` on pumpkin is confirmed correct** (the batch 21 trap, mirrored): the record
   states the beetle-gut mechanism in both registers and makes no soil-persistence claim.

**3 and 4 are the OPPOSITE of the singular/plural class**: there the two ids name the SAME problem,
here the shorter id names a WIDER one. `check_scope_variant_ids_not_merged` pins both on the
organism and the compound scope rather than on the id strings.

## 5. THE PINNING METHOD, AGAIN -- batch 21's fix is necessary but NOT sufficient

Batch 21 earned the rule "check every intended MINT against the roster BY ID, not by problem name."
That rule was followed here and it still missed two, because **an exact-id check passes an id that
merely RESEMBLES a live one**. `cucumber-mosaic-virus` is not `cucumber-mosaic`, so the check was
satisfied.

**Added for batch 23: run a SUBSTRING / TOKEN-SUBSET scan of every authored id against the whole
roster, not just an equality check.** Over 20 authored ids it flagged 7 pairs; 2 were the real
adjudications above, 1 was the already-known `bacterial-wilt` trap, 3 were correct generic-vs-
crop-scoped aphid ids, and 1 (`gummy-stem-blight` vs blueberry's `stem-blight`) was a false
positive resolved by reading. A plural-only variant scan does NOT find these -- it was the first
thing tried and it saw only `japanese-beetle(s)`.

## 6. Filed, NOT fixed -- the carry-forward

1. **FOUR one-token repoints would retire the lone-crop minority-id class**, not three. The known
   three are asparagus `cutworm`, swiss-chard `flea-beetle`, basil `japanese-beetle`. **New:
   artichoke `botrytis-gray-mold`**, alone on a variant of the same *Botrytis cinerea* that the
   majority id `gray-mold` names on five crops. Batch 21's and batch 22's
   `check_singular_variants_not_taken` both refuse once the three are repaired -- retire the guard
   in the same change.
2. **`wet_foliage_discipline` is missing from 13 laddered problems whose own prose tells you to
   time your work to dry foliage.** Measured: 34 such problems, 21 carry the rung. The 13 are
   jalapeno/bacterial-spot; slicing-cucumber, pickling-cucumber and cucumber (downy-mildew and
   angular-leaf-spot each); sugar-snap-peas and snow-peas (powdery-mildew); swiss-chard,
   butternut-squash, acorn-squash and spaghetti-squash (downy-mildew).
3. **The absolutes are a CAMPAIGN, not three defects. MEASURED 2026-09-01 after the batch shipped.**
   The three found in these crops (english-cucumber downy mildew "Water at the soil line, **never**
   overhead"; edamame SCN "**never** grow soybeans in the same spot every year"; pumpkin
   phytophthora "**never** let water stand") are typical members of a large live population, not
   outliers:

   | measure | count |
   |---|---|
   | absolute-word hits in problem prose, roster-wide | **171** |
   | of which "never" | 136 (134 distinct clauses) |
   | "never" clauses that INSTRUCT the reader | **85** |
   | "never" clauses that are descriptive ("seeds that never come up") | ~45 |
   | absolutes in shipped RUNG notes | 22 |
   | absolutes in batch 22's 270 new rung strings | **0** |

   `"Water at the base of the plant, never from above"` (beefsteak-tomato) is the same shape as
   english-cucumber's. **Fixing three of eighty-five would make the dataset less consistent, not
   more.** Scope it as a prose pass with a real unit of decision, and note that most of the ~45
   descriptive uses are correct English that must NOT be touched -- this is a read-then-adjudicate
   campaign, not a find-and-replace. The §9 language standard bans absolute SAFETY and EFFICACY
   claims; a flat prescriptive "never" is a weaker offence than "harmless", so the priority order
   inside the campaign is worth setting before starting.

   **The tooling half IS fixed** (`ad571e6`): `ladder_batch verify`'s absolute vocabulary omitted
   "never" while every batch-17-to-22 promote's `hygiene()` included it, which is why the step
   whose job is to report copy hygiene reported zero. `tools/test_ladder_batch_absolutes.py` now
   re-derives every promote's list from source and fails if `verify` stops covering it; on its
   first run it found a second gap, `eliminates?`, in 18 promotes.

4. **english-cucumber powdery mildew has an inverted register pair**: `prevention_beginner` names
   the cultivar Tyria and `prevention_seasoned` generalizes. The seasoned register should be the
   more specific one.
5. **Mis-pointed / unstable source keys, re-measured on these three crops**: english-cucumber
   `clemson_hgic` -> 2 documents and `umn_ext` -> 2; edamame `iastate_ext` -> 2 and `mu_ext` -> 2;
   pumpkin `umn_ext` -> 3. Each problem's own `anchoring_urls` entry is correct; the KEY is not
   stable. Mechanically detectable; the scan is still worth building and still has not been.
6. **Catalog gaps, best-evidenced first**: general plant vigor (four berry authors + citrus +
   edamame + pumpkin); `horticultural_oil` unable to reach `fungal` (three batches); humidity /
   venting under cover (**the most-repeated instruction in english-cucumber's record, 5 problems,
   and it has no method at all**); `weed_host_control` unable to reach `viral` (english-cucumber's
   CMV is the textbook case -- an aphid-vectored virus with a named weed reservoir) or `nematode`;
   potassium bicarbonate absent entirely; lawn/grub management (edamame Japanese beetle);
   preventive vine-burying at the joints (pumpkin); "keep young plants vigorous"; a
   lift-fruit-onto-a-board method (`straw_mulch` covers only the mulch half); burying overwintering
   inoculum; dormant lime sulfur; watering QUANTITY; soil pH.
7. **Several methods' `best_use` prose enumerates fewer pests than their `applies_to` admits** --
   `spinosad` (no beetles named, admits `insect_chewing`), `yellow_sticky_traps` (no beetles),
   `water_spray` (aphids only, admits `mite`), `straw_mulch` (strawberry-scoped). The gate governs
   on `applies_to`, so nothing is wrong in the data; but the prose is what an author reads when
   deciding whether a rung fits, which is the batch-1 `bottom_watering` failure mode.
8. **viola's own note still recommends Bt on a butterfly host** (batch 21). The ladder already omits
   it; the note is what should change.
9. **The oil temperature ruling from batch 18 was OVERTURNED** by reading (batch 19 outcome doc
   §8). Specified but not actioned.

## 7. After batch 22

Roster **94 / 121**. Remaining **27 crops / 138 problems / 7 batches** (crop and problem counts
COMPUTED from canonical, not carried over -- the handoff's herb and allium splits differ):

| batch | crops | n | problems |
|---|---|---|---|
| **roots (NEXT, per Trevor)** | parsnip, potato, sweet-potato | 3 | 22 |
| alliums | chives, leek, onion, shallot | 4 | 27 |
| other trees | mulberry, pawpaw, persimmon, pomegranate | 4 | 24 |
| woody herbs | lavender, rosemary, sage, thyme | 4 | 20 |
| soft herbs | lemongrass, mint, oregano | 3 | 16 |
| pome fruit | pear-asian, pear-european | 2 | 15 |
| microgreens (**LAST**, standing ruling) | arugula-, broccoli-, cilantro-microgreens, pea-shoots, radish-microgreens, sunflower-sprouts, wheatgrass | 7 | 14 |

**Note for the roots batch:** potato and sweet-potato have laddered siblings only loosely (no other
solanaceous root, no other storage root), so the template-twin measurement of section 3 may come
back empty. If it does, `check_template_sibling_divergence` would be VACUOUS and must be replaced
rather than carried -- its own anti-vacuity branch will say so by refusing. Measure before writing.
