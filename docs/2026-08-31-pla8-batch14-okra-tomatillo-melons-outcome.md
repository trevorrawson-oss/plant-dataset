# PLA-8 -- batch 14 (okra, tomatillo, the melons) + the mancozeb mint: outcome

Written 2026-08-31. Base `b6d36611`; mint output `4c5a79d3`; batch output `c76f14f1`.
Crops: okra, tomatillo, cantaloupe, honeydew-melon, watermelon. 48 problems, 232 rungs, roster
laddered 58 -> 63, catalog 60 -> 61. Sequencing per Trevor 2026-08-31: batch 14, then the
companions -- **the Companion & Pollinator deferral is LIFTED by Trevor's direct instruction**;
only the microgreens now sit at the back of the queue.

## 1. WHAT SHIPPED

| | promote | commit | effect |
| -- | -- | -- | -- |
| 1 | `tools/promote_pla8_mancozeb.py` | `f9cd212` | mints `mancozeb`, catalog 60 -> 61. Zero crops. |
| 2 | `tools/promote_pla8_batch14.py` | `b5c75c2` | 48 problems, 232 rungs on 5 crops. Catalog untouched. |
| + | `tools/ladder_batch.py` note schema | (fix commit) | the companions tooling gap, closed TDD-first. |

The mint ran FIRST so the key existed in the authoring brief -- agents may only name catalog keys.

## 2. THE MANCOZEB MINT

- Profile re-read through the tested instrument (`tools/ucipm_uaidb.py`, offline control 5/5 in
  the same pass) rather than trusted from the chem cohort's birth-time figures; matched figure for
  figure: water **H**, acute **L** (CAUTION band), **Prop 65 + EPA** carcinogen lists, bees low.
- The shelf test ran the carbaryl way: UC IPM's California survey lists NO home products; Clemson's
  cucurbit factsheet carries it in the HOME-GARDEN table (Southern Ag Dithane M-45, 5 day PHI,
  gummy stem blight), verified from RAW HTML per the column-shift lesson.
- Two axes diverge from chlorothalonil and the entry refuses its sibling's sentences: acute
  L/CAUTION is a PRO stated honestly, and natural enemies is **UNRATED** -- disclosed as
  unrated-is-not-low and guarded by an invented-rating detector (the neem shape). The detector's
  first draft only caught one word order; the suite caught that ("Rated Low risk to natural
  enemies" puts Low FIRST) and it now checks sentence-wise in both orders.
- Suite 49/49 both runners; harness **28/28, zero survivors, first run**.

## 3. THE BATCH'S SPINE: CONVENTIONAL SCOPING

chlorothalonil + mancozeb land on exactly two ladders (cantaloupe/`alternaria-leaf-blight`,
watermelon/`anthracnose`), where the prose names BOTH -- and both are REQUIRED there, because
shipping one silently un-names the other. Nowhere else: every other spray mention in the batch is
"a labeled fungicide", unnamed. Copper lands once (tomatillo/`early-blight`, named). 23 ladders
carry no material rung at all, each on its own prose.

## 4. THE BACTERIAL-WILT MIRROR

Batch 13 refused `bacterial-wilt` for eggplant (Ralstonia vs the roster's Erwinia). The melons
REUSE it because theirs IS the Erwinia -- both cause-prose records name *Erwinia tracheiphila*,
beetle-carried -- and `check_bacterial_wilt_premise` asserts that in canonical so the reuse cannot
outlive its evidence. Watermelon carries no bacterial-wilt problem, which its own prose explains.
Other joins: `tomato-hornworm` (the tomatoes'), `corn-earworm`, cucurbit ids from the
cucumbers/squashes; new: `stink-bugs` (lead-organism convention), `three-lined-potato-beetle`,
`root-and-stem-rots`, `gummy-stem-blight`, `alternaria-leaf-blight`.

## 5. THE MELON TWIN STRUCTURE AND THE CROP-NEUTRALITY RULE

Six problems are byte-identical in advice prose on all three melons and ship ONE text set each,
both directions pinned. The batch's new subtlety: **the symptom prose is crop-named where the
advice prose is shared**, so a donor set may carry only claims backed on every member and no
single crop's name -- `check_melon_neutrality` enforces it. Every donor claim was fact-checked
against the records (one-generation-South squash bug, PM's fruit-size/sugar/sunscald, DM's
10-to-14-day leaf kill, GSB's Didymella: all BACKED).

## 6. READ RULINGS

- okra's stink bugs earn the batch's one trap rung WITH the removal attribution ("concentrates
  them for removal", the turnip precedent) plus the cautions pointer for the unstated deadline.
- Pre-plant cultivation stays refused (tomatillo's cutworm agent refused it unprompted -- the
  batch-13 ruling is now the house instinct); hornworm fall tillage and the melons' late-winter
  vine-borer bed work earn `off_season_tillage`.
- Ten shipped-rung echoes rewritten (the cucumber ladybug sentence caught its third batch of
  independent agents converging on it).
- Divergent wilt ladders across the melons are LEGITIMATE: honeydew's prose says "choose more
  tolerant varieties" (rung, hedged as tolerance-not-immunity); cantaloupe's says few varieties
  resist (no rung).

## 7. VERIFICATION

- Batch suite **68/68 both runners**; harness **38/38 (run 3)**. Run 2's FOUR survivors were all
  real: the wilt premise had no honeydew-only driver (stripping both melons let a narrowed loop
  pass on cantaloupe's evidence), and three check-side branches had only post-side drivers.
  Preflight also caught a duplicate anchor before run 2 (the check/verify_post twin pattern).
- Gauntlet: gate_all **121/121**, control_ladder_gate **0**, register_completeness **PASS**,
  whole_crop_gate PASS on all five, release_verify **clean** vs `b6d36611`.

## 8. THE COMPANIONS TOOLING FIX (shipped with this round)

The 10 Companion & Pollinator crops carry prose in `note_beginner`/`note_seasoned` ONLY.
`ladder_batch.prose_key` reduced such problems to `(name, None, None)`: same-named problems on
different companion crops collided as FALSE TWINS -- the microgreens blind spot in a third
schema. Fixed TDD-first (the false-twin test was RED on the shipped tool), with the load-bearing
test's coverage floor forcing fixtures for the new fields. 27/27; tool harness 10/10.

## 9. FILED, NOT FIXED

- **honeydew's fusarium-wilt AND gummy-stem-blight `ncsu_ext` anchors both point at the
  downy-mildew URL** (agent-found; the mis-pointed-key class, third and fourth instances this
  week alongside eggplant's hornworm anchor).
- Catalog gaps re-confirmed: horticultural oil is named for powdery mildew by okra AND all three
  melons' prose but the key is insect/mite-scoped (now a measured WIDENING candidate, 4+ crops);
  weed-host control vs nematodes; neighbor-crop separation (okra beside corn); DE dust; potassium
  bicarbonate; reflective mulch vs cucumber beetles (bacterial applies_to gap).
- okra root-knot filed under `diseases[]` with source `type: "disease"`; shipped `nematode` per
  the type vocabulary.

## 10. NEXT

Batch 15 = the first companions batch (marigold, zinnia, cosmos, calendula, sweet-alyssum; 33
problems). Standing hazards: zinnia/Japanese beetles is a pinned INVERTED trap-cropping exclusion;
all 65 companion problems need `type` minted; no per-problem source anchors exist on these crops,
so the read leans on crop-level sourcing. Batch 16 = echinacea, bee-balm, chamomile, borage,
sweet-pea (sweet-pea is *Lathyrus*, NOT *Pisum*: no pea-organism id may be reused without a taxon
check). Then ~9 batches remain; microgreens last.
