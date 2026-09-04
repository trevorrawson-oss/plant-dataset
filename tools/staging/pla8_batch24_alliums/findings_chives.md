# chives -- batch 24 r4 findings (2026-09-03)

## 1. validate_out.py could not reach PASS for any crop but onion -- FIXED (one line, in this directory)
With `P.CROPS = (crop,)` the promote's `check_no_precedent_copy` still asserted
`declared_seen == set(DECLARED_IDENTITIES)`, and the only declared identity is
`('onion','onion-thrips','water_spray')`. So a chives, leek or shallot run refused with
"declared identities [...] were not found in the batch" no matter what the prose said (confirmed on
the baseline run of the previous out_chives.json). Added one line after `P.CROPS = (crop,)` that
scopes `P.DECLARED_IDENTITIES` to the crop being validated. The promote itself is untouched; it runs
all four crops together and onion's pin is present there.

Second validator observation, NOT fixed: a length mismatch (`pests: 3 in record, 4 in out`) makes
the shape loop `continue`, so every pest rung was skipped on the baseline run and the two
false-attribution devices in the old spinosad seasoned notes went unreported. Anyone reading a
partial-failure run as "only N defects" should know the count is a floor.

## 2. Promote pins that chives now changes (for the orchestrator, not for me to edit)
- `EXPECTED_PROBLEMS["chives"]` 8 -> 7 and `EXPECTED_RUNGS["chives"]` 30 -> 27 (pests 5+4+3,
  diseases 4+4+3+4); `TOTAL_RUNGS` moves by -3.
- `EXPECTED_TEMP_FIGURES`: chives contributed 3 figures before (75°F downy mildew; 90°F in the
  thrips soap note; 90°F in the retired aphids soap note) and contributes 2 now.

## 3. Record claims with no legal method (catalog gaps; claims left in the record)
- **onion-thrips: tolerance through watering** -- "keep plants watered in hot spells", "avoid
  drought stress", "keeping plants unstressed and watered blunts outbreaks" (three fields). The
  only key is `even_watering`, whose applies_to is physiological/mite/bacterial and does not reach
  insect. Same gap the batch findings file already logs (#2); not forced.
- **onion-thrips: spatial separation** -- "avoid siting chives beside heavily thrips-pressured
  onion or garlic plantings". Not crop_rotation (no self-history claim) and not airflow_spacing
  (disease-only). Batch findings #3. Consequence stands: the thrips ladder has no cultural
  bed-choice rung; garden_sanitation (the shear) is its only cultural entry.
- **allium-leafminer: azadirachtin** -- the record names "spinosad or azadirachtin can help where
  pressure is high". The catalog's `neem_oil` is the clarified oil for soft-bodied pests, not the
  azadirachtin extract, and its MEANS does not describe a leafminer, so mapping it would be a
  mis-key. Spinosad carries the rung; azadirachtin stays in the record only.
- **allium-leafminer: separation** -- "separate new plantings from pressured allium beds" is the
  same separation gap as thrips; the crop_rotation rung carries only the record's carryover claim.
- **chives' shear-and-regrow reset** -- carried inside garden_sanitation on 5 of 7 problems per
  the brief's instruction; still a distinct cultural action from end-of-season cleanup (batch
  findings #4). Nothing new to add, logging that it is now 5/7 rather than 5/8.

## 4. Doubts about record claims (not acted on; recorded so they are not silently trusted)
- **botrytis name vs content**: the corrected record is wholly FOLIAR (Botrytis squamosa leaf
  blight from UC IPM / PNW handbook) and its symptoms_seasoned itself says "It is documented on
  onion, and chives are a related host." The pinned id `botrytis-leaf-blight-neck-rot` and the name
  "Botrytis (leaf blight and neck rot)" still promise a neck rot no field describes. Batch findings
  #6.1 already flags this; the r3 correction made the record MORE foliar, not less. The ladder
  follows the record.
- **botrytis crop_rotation, three years**: prevention_seasoned gives "three years"; no other field
  repeats it and the beginner registers do not carry it. I used it in both registers of the new rung
  because the record states it. Worth a source-truth glance since it is the one hard number in the
  ladder that appears in a single field.
- **onion-maggot beginner registers say "flies"/"fly" for both the pest and its adult**; the seasoned
  registers name Delia antiqua. No conflict, noting only that the beginner never says "maggot fly"
  as a name, which is how the record's cause_beginner introduces it.
- **rust host framing**: symptoms_seasoned says "Allium rust (Puccinia species)"; osu_ext anchor
  is the garlic page of the PNW handbook. The chives-specific claim rests on uc_ipm's onion/garlic
  rust page; neither anchor is a chives document. Stated because the crop-scoped id was minted on
  the strength of "chives' prose names Puccinia rust fungi".

## 5. Style calls made while authoring (so a reviewer can disagree in one place)
- The bee warning on both spinosad rungs uses the method's caution only; the previous "chive blooms
  draw bees and hoverflies" was dropped as unsourced in the record and the catalog.
- "Culls" is defined in-line in the beginner register wherever it appears; "pupae" is defined the
  first time it appears in a beginner note ("its resting stage").
- Beginner registers name no binomial; the only technical nouns kept in beginner copy are
  "pustules" (record's own beginner term, explained as orange spots) and "row cover" (defined).
