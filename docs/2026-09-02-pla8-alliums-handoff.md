# PLA-8 -- HANDOFF: batch 24 (alliums) is STAGED with a PASSING promote and NO suite yet

**Written 2026-09-02 at the end of a long session. Read this before doing anything.**

Canonical is `c24d7754` (catalog r10). **Verify first:**
`shasum -a 256 crops_data_final.json` must read
`c24d7754e9d708b09169b5b8979f1f63bdd35b14cd77e0adf86ba03b88870c6f` and match `LATEST.txt`.

`main` is **5 commits AHEAD of origin and UNPUSHED**. Trevor confirms every push; do not push unasked.

---

## 1. What shipped this session

| commit | what |
|---|---|
| `128e390` | **batch 23, the roots** -- parsnip, potato, sweet-potato; 22 problems / **87 rungs**; `b118f19d` -> `e6c986e3`; roster **94 -> 97** |
| `efb8cc5` | `COMMIT_FOR` for `e6c986e3` |
| `bf11fb5` | batch-23 suite fix: its `main()` driver read LIVE canonical and broke the moment the promote landed |
| `a1fc62a` | **catalog r10** -- `certified_clean_stock` widened to `insect_general` + prose generalized; `e6c986e3` -> `c24d7754`; methods steady at 64, `source_catalog` 218 -> 219 |
| `cdfbedc` | `COMMIT_FOR` for `c24d7754` |

Both arcs mutation-tested: batch 23 **64/64 zero survivors** (re-run post-land), r10 **50/50 zero survivors**.

## 2. START HERE: batch 24's guard suite and mutation harness

**Everything else about batch 24 is DONE.** `tools/promote_pla8_batch24.py` exists, passes, and
produces `c24d7754` -> **`3eefc4b8`**. 27 problems, **82 rungs**, roster 97 -> 101.
Staging is `tools/staging/pla8_batch24_alliums/` with `out_*.json`, `pinned_ids.json` and
`findings.md`. **Both the promote and the staging dir are UNTRACKED** -- commit them with the suite.

Gauntlet already run on a scratch candidate and green: `gate_all` **121/121**, all four crops PASS,
every standalone gate 0, `release_verify` clean but for its known single-crop CONCERN naming exactly
the 4 declared crops, `catalog +none -none`, reference byte-identical.

**What is missing is `tools/test_promote_pla8_batch24.py` and
`tools/mutate_pla8_batch24_suite.py`.** Per PLA-215 the promote does not ship without them. Copy
batch 23's pair as the template; the guard list below is what needs driving.

### The six guards that are NEW in batch 24, each already verified firing by hand

Do not assume any of these is covered by an inherited driver.

1. `check_schema_premise` -- **split by schema**, asserted in BOTH directions per crop, plus an
   INVERSE severity split. Needs drivers for: a FULL field appearing on an allium-schema crop, an
   allium field on chives, severity present on chives, severity missing on the other three, and the
   coverage count.
2. `check_type_set_from_nothing` -- `type` is ABSENT pre-state, not coarse. Drivers: a pre-existing
   type, a staged type off the pin, a staged type outside the gate's map, the coverage count.
3. `check_no_template_twins_premise` -- **schema-aware**. Drivers: a twin appearing on the fields
   both crops actually carry, AND the anti-vacuity branch.
4. `check_no_precedent_copy` -- **two passes plus a pin table**. Drivers needed for: pass A over
   threshold, **pass B over threshold** (a rung lifted onto a DIFFERENT problem), a declared identity
   that is not byte-identical, a declared identity naming a crop with no such rung, a declared
   identity missing from the batch, and BOTH anti-vacuity branches.
5. `verify_post` -- `type` is an ADDED key here, not a changed value. Drivers: unexpected added key,
   dropped key, the added-count (3 per problem), any pre-existing leaf changing, per-crop tally.
6. `check_id_adjudications` -- scope variant, spelling variant, taxon reuse, stem variant. Each
   branch needs its own driver.

Also: `check_no_shipped_prose_echo` now EXEMPTS declared identities. Without that exemption two
guards contradict each other, one requiring what the other forbids, and the batch cannot pass either
way. That exemption needs its own driver.

### THREE HARNESS LESSONS THIS SESSION PAID FOR, IN ORDER OF COST

1. **A mutation harness proves a guard FIRES; it cannot prove the guard MEASURES THE RIGHT THING.**
   Batch 23's `check_no_precedent_copy` was reachable (243 comparisons), non-vacuous and
   mutation-tested 3/3, and it scored the batch's only real copy at **0.431** and passed it. Cause:
   `difflib` defaults plus a mean of two registers. `autojunk` engages at 200 characters and junks
   any character in over 1% of the sequence, which describes every seasoned register; the mean then
   dilutes one copied register against one independent one. Same pair with `autojunk=False` and a
   per-register max: **0.757**, sharing a 56-character verbatim run. **Every prose-similarity check
   in this repo must pass `autojunk=False` and take a per-field max.** A guard needs a POSITIVE
   CONTROL BUILT FROM THE REAL DEFECT, not only mutations of its own branches.
2. **A promote's guards do not cover the ROSTER gates that read what the promote writes.** r10
   shipped once, passed its own `check()`, a 67-test suite and a 49-mutation harness with zero
   survivors, and then took `gate_all` from **121/121 to 0/121**: the minted source carried `name`
   but no `title`, and A54 requires a title read off the document. It is catalog-level, so one
   titleless id reddens every crop. The promote now IMPORTS `source_catalog_title_gate.title_violations`
   and runs it against the post-state. **If a promote writes to `source_catalog` or
   `control_methods`, import and run the roster gate that reads it.**
3. **Assert the WHOLE sentence, never a shared fragment.** Three drivers this session asserted a
   fragment that appeared in two different messages, so disabling either branch left the other
   satisfying the test and the mutation SURVIVED. It is written in the previous handoff and I
   reproduced it three times anyway. The fragment always looks specific while you are looking at the
   one branch; the collision lives in the message you are not looking at.

## 3. Batch 24's premise, because every batch's is different and this one is the eighth shape

* **SCHEMA SPLIT.** chives is FULL-schema (`symptoms_*`/`cause_*`/`organic_treatment_*`/
  `prevention_*`) and carries **NO severity**. leek, onion, shallot use `identification_*` /
  `management_*` -- an **allium-only** schema held by exactly 5 crops (garlic, leek, onion, shallot,
  spring-onion), of which garlic and spring-onion are already laddered, so the shape is proven.
  Severity splits the other way: chives none, the other three all.
* **Type: SET FROM NOTHING.** All 27 carry no `type` key at all.
* **Zero template twins**, measured schema-aware.

**THE PREMISE I ASSERTED FIRST WAS FALSE AND TWO AGENTS CAUGHT IT.** `pinned_ids.json` originally
claimed 3 template twins against spring-onion and instructed the onion and shallot agents to copy
spring-onion's shipped ladders byte-for-byte. The scan had compared the 8 FULL-schema fields on
crops that do not carry them: **6 of 8 were `None` on both sides and the tuples matched on ABSENCE.**
Complying would have shipped two defects -- onion/`onion-thrips` would have DROPPED
`reflective_mulch` (a control onion's prose names and spring-onion's does not), and
onion/`fusarium-basal-rot` would have carried the word "scallion" into the onion record. **In a
schema-split batch every cross-crop prose comparison must use the field set the crop actually
carries.** The real management relative is GARLIC, not spring-onion.

## 4. The r10 backfill: 14 rungs, UNSTARTED, and the reason r10 exists

r10 widened `certified_clean_stock` to reach insect-typed problems and generalized its prose from
pathogens to planting-stock-borne pests. **Nothing has been authored against it yet.** 14 rungs are
now placeable, in two classes that need different treatment:

**CLASS A (10) -- the reason is a PATHOGEN the stock carries; the insect is only the vector.** The
existing disease-framed prose is already correct for these.
* asian-citrus-psyllid on grapefruit, lemon, lime, mandarin-clementine, orange-navel ("certified
  disease-free trees", huanglongbing)
* aphids on strawberry, raspberry, blackberry ("certified virus-free plants")
* potato/`aphids-virus-vectors`, sweet-potato/`whiteflies-virus-vectors`

**CLASS B (4) -- the reason is THE PEST ITSELF riding inside the planting material.**
* sweet-potato/`sweet-potato-weevil` ("certified weevil-free slips")
* raspberry and blackberry /`raspberry-crown-borer` ("certified, borer-free stock")
* strawberry/`root-crown-weevils` ("clean stock")

This is a thin-ladder-backfill-shaped promote (`tools/promote_pla8_thin_ladder_backfill.py` is the
template): `expect_before` pins each ladder's exact current sequence, every pre-existing rung must be
byte-identical after, and `check_warrants` requires a declared phrase from each problem's own prose.

## 5. The r11 queue, in evidence order

1. **`even_watering` reaches neither `insect` nor `fungal`** -- `applies_to = ['physiological',
   'mite', 'bacterial']`. **SEVEN independent reports across two batches**: roots 3 (potato x2,
   sweet-potato x1), alliums 4 (all four agents). The blocked instruction is always the same shape:
   "keep plants vigorous and evenly watered", "keep plants unstressed". On leek/`pink-root` it is
   **unrepresented in any rung**. The method's own MEANS already describes holding spider mites down
   on plants "left dry and stressed", so the mechanism is in the text and only the target set
   excludes it. **Strongest catalog signal in the arc.**
2. **Spatial separation from a pressured neighbouring allium planting** -- NEW. chives reports it on
   3 of its 4 pests. Neither `crop_rotation` (moves a planting in time, off its own history) nor
   `airflow_spacing` (disease-only, rationale is humidity not host concentration). Consequence:
   chives/`onion-thrips` has no cultural bed-choice rung at all.
3. **The perennial "shear the clump and let it regrow clean" reset** -- NEW. chives' signature move,
   carried on 5 of its 8 problems inside `garden_sanitation`, whose MEANS is end-of-season cleanup.
4. **`reflective_mulch`'s MEANS is out of date** -- scoped to aphid-transmitted virus on squash,
   melon and cucumber; now carries THRIPS rungs on garlic (shipped), onion and shallot.
5. **`prompt_harvest`'s MEANS and `how_it_works_*` are fruit-only** -- now carrying **8** root-lifting
   rungs across carrot, radish, parsnip, potato and sweet-potato. Counted, not estimated.
6. **`off_season_tillage`'s `how_it_works_*` is written around pupal cells of soil-pupating
   Lepidoptera** and now carries wireworm rungs (click beetle larvae persisting years).
7. Carried from the roots handoff and still open: in-season mounding (blocked on a document for the
   barrier reading), `horticultural_oil` cannot reach `fungal`, humidity/venting under cover,
   `weed_host_control` cannot reach `viral`/`nematode`/**`bacterial`** (roots added the third).

## 6. Open, filed, NOT fixed

1. **A mis-pointed source key on sweet-potato's weevil entry.** It says "Buy **certified**,
   weevil-free slips" and cites `clemson_hgic_1322_sweet_potato` and `uf_ifas_edis` IN154.
   **Clemson HGIC 1322 does not mention the weevil at all**; IN154 says only "should be free of
   weevils". The claim IS supportable -- NCDA&CS states "Purchase only certified and tagged
   sweetpotato weevil-free plants from known sources" -- so this is the right claim under the wrong
   key, the `vce_426_331` shape. Belongs to the citation cleanup arc.
2. **chives' `Botrytis (leaf blight and neck rot)` never describes a neck rot.** Every field is
   foliar. The NAME over-promises against its own record, which is why the pinned id
   `botrytis-leaf-blight-neck-rot` is right for the entry as named and wrong for it as written.
   Either rename the problem or add the missing content.
3. **"bin" as a verb in live consumer copy** -- leek rust `management_beginner`. British; hard rule.
4. **UK flight dates presented as general** -- leek's allium leaf miner gives RHS timing while the
   record also cites `umd_ext` (mid-Atlantic US).
5. **leek moth register mismatch** -- seasoned says "May to June and August to October", both
   beginner registers say "late spring and late summer", under-covering the second flight.
6. **~130-152 roster-wide style hits** (internal vocabulary "rung"/"ladder"/"tier", plus absolutes)
   across ~50 crops. The vocabulary half is unambiguous and is legacy: batches 21/22/23/24 crops all
   carry ZERO, so the guard has been enforced since batch 21. **spring-onion's shipped
   `floating_row_cover` note contains "Pair it with the rotation rung"** -- which is why "copy the
   sibling verbatim" is unsafe as a general policy. Bounded cleanup: mechanical find, hand rewrite,
   no sourcing.
7. **shallot's pink root is anchored solely to `tamu_agrilife` `onion1.pdf`**, an onion publication.
8. Carried forward: four one-token id repoints (asparagus `cutworm`, swiss-chard `flea-beetle`,
   basil `japanese-beetle`, artichoke `botrytis-gray-mold`); `wet_foliage_discipline` missing from 13
   laddered problems; `beneficial_nematodes` owes a T1 read; the chard bolting contradiction; the
   dropped-hedge inverse sweep has never been run.

## 7. Method notes worth carrying

* **Pin ids AND types before fan-out.** 22/22 and 27/27 came back with zero drift across two batches.
* **Give agents the schema explicitly per crop.** In a split batch the brief must name the fields
  that crop actually carries, or an agent goes looking for `prevention_*` that does not exist.
* **Tell agents to VERIFY the premise, not just follow it.** Two agents refused a wrong instruction
  and measured instead; that is the single highest-value thing that happened this session.
* **The independent source-truth pass is not optional.** It ran on batch 23 when every gate, an
  82-test suite and a 64/64 harness were green, and found **eleven defects**, including a rung that
  contradicted its own crop's storage data and a copper hazard band softened from "highly to very
  highly toxic to fish and aquatic life" to "toxic to fish".
* **A search summary is not evidence.** A search attributed a sentence to NC State that the document
  does not contain; the real sentence was weaker and conditional. Fetch and read.
* **E1 pre-commit always needs `--no-verify`**, and the reason goes in the message. Structural.
* **plant-app owes `npm run build:guides`** covering seven dataset revisions now.

## 8. Roster position

**101 / 121 laddered once batch 24 lands** (97 today). Remaining after it: **20 crops / 89 problems /
5 batches**, computed from canonical:

| batch | crops | n | problems |
|---|---|---|---|
| **24 alliums (STAGED, needs suite)** | chives, leek, onion, shallot | 4 | 27 |
| 25 other trees | mulberry, pawpaw, persimmon, pomegranate | 4 | 24 |
| 26 woody herbs | lavender, rosemary, sage, thyme | 4 | 20 |
| 27 soft herbs | lemongrass, mint, oregano | 3 | 16 |
| 28 pome fruit | pear-asian, pear-european | 2 | 15 |
| 29 microgreens (**LAST**, standing ruling) | 7 microgreens crops | 7 | 14 |

**MEASURE BATCH 25's SCHEMA BEFORE AUTHORING.** The microgreens 7 use a FOURTH shape,
`description_*` / `management_*`, with **zero laddered anywhere**, so batch 29 has no proven
precedent. Batch 25's four crops have not been checked at all.
