# PLA-8 -- batch 16, companions B: outcome

Written 2026-08-31. Base `098dd0b1`; output `213cb110`. Crops: echinacea, bee-balm, chamomile,
borage, sweet-pea. 32 problems, 88 rungs, roster laddered 68 -> 73, catalog untouched at 61.
**This batch closes the Companion & Pollinator category** -- every crop in it is now laddered.

## 1. THE SWEET-PEA TAXON RULING

Sweet pea (*Lathyrus*) is Fabeae, the same kinship that let fava reuse the peas'
`root-rots-damping-off` -- but fava earned that reuse on near-verbatim prose-twin evidence, and
sweet-pea's rot prose is its own generic Rhizoctonia/Pythium/Fusarium complex. The batch pins
the refusal BOTH directions in `TAXON_REFUSED`: sweet-pea ships the ornamental
`root-and-stem-rots` (shared with echinacea and borage under the lead-name convention), and the
peas' id appearing anywhere is a hard abort. The Fabeae kinship still ships where the prose
carries it: the rotation rung restates "rotate off recent pea, bean, or sweet pea ground" from
the crop's own record. No weevil problem exists on the crop, so the *Bruchus* trap never arises.

## 2. IDS

- New to the roster (6): `eriophyid-mites`, `rabbits-and-deer` (the first vertebrate ladder
  since the corns), `stalk-borer`, `bee-balm-rust`, `mealybugs`, `caterpillars`.
- **`bee-balm-rust` is crop-scoped, not a generic `rust`**: the record names only *Puccinia
  spp.*, so a later organism-scoped mint for the mint-family *P. menthae* stays free. The suite
  asserts no bare `rust` id exists on the roster.
- Reused (14) including `japanese-beetles` (batch 15's mint), `gray-mold`, `aster-yellows`
  (typed bacterial per the carrot phytoplasma precedent), `damping-off`, `anthracnose`,
  `downy-mildew`, `leaf-spots`, `mosaic-viruses`.

## 3. THE INVERSION CARRIES OVER, PLUS TWO BATCH-SPECIFIC GUARDS

1. `trap_cropping` forbidden batch-wide; the trap vocabulary ban gained **"decoy"** -- borage's
   own aphid record describes banker AND decoy value (the suite proves the ban non-vacuous
   against those source notes). "insectary" stays legal: predators recruited against the crop's
   OWN pests are the placeable half.
2. **The lure-trap warning is REQUIRED** on echinacea's Japanese-beetle handpick rung (the
   mirror of batch 15's pheromone guard): the crop's notes advise against bag-style beetle
   traps, the first authoring pass dropped the warning, and the read restored it -- exactly the
   dropped-do-not-do class the guard family exists for.
3. **verify_post regained a new-id-shipped branch.** Batch 15 deleted its generic did-not-ship
   branch as unreachable because every new id doubled as a per-id lookup key; here only
   `japanese-beetles` does, so the branch is real protection again -- reachability decides,
   per-batch, never precedent. The batch-total rung check went the other way: deleted as
   unreachable (per-crop counts sum to it identically).

## 4. MATERIALS

`MATERIAL_OK` scopes every soft_chemical rung to the ladders whose own notes name the material
(12 ladders; soap widely, oil on the mite/aphid pairs, iron phosphate on sweet-pea slugs,
spinosad on sweet-pea thrips + caterpillars, bt biological on sweet-pea caterpillars); every
other ladder must carry none, and every disease ladder is cultural/physical only. **The
spinosad-on-a-pollinator-plant tension is resolved the chlorothalonil way**: the crop's notes
name the material, so the rungs ship WITH bee-timing framing in the seasoned register (asserted
by the suite), and the tension is filed here rather than silently dropping a named material.
FILED: chamomile's thrips/mealybugs records carry the agents' "not documented on chamomile
extension pages" sourcing admission; the companion PM base-watering vs USU no-leaf-wetness
tension recurs on four records (the batch-15 treatment applied).

## 5. THE READ

Nine introduced 90°F figures trimmed to number-free heat cautions (echinacea/bee-balm soap and
oil rungs; the crops' notes carry no figure), five real "never" tokens reworded, two trim seams
smoothed, and the echinacea lure-trap warning restored (then guarded). Echo scan: zero against
the 68-crop shipped corpus after one reword round during staging.

## 6. VERIFICATION

- Suite **71/71 both runners** (pytest + unittest), replay-pinned to post `213cb110`.
- Harness **52/52, zero survivors, first full run** (preflight 53 anchors exactly once,
  positive control GREEN, sentinel RED; inversion 9/9, validate 16/16, materials 6/6, taxon
  6/6, ids 3/3, alignment 3/3 -- including the identical-prose direction, driven for the first
  time this arc -- blast 5/5, echo 2/2, schema 1/1, mechanics 1/1).
- Gauntlet: gate_all **121/121**, control_ladder_gate **0**, register_completeness **PASS**,
  whole_crop_gate PASS on all five, release_verify **clean** vs `098dd0b1` (5-crop declared
  blast radius, catalog +none -none, lettuce-leaf byte-identical).

## 7. NEXT

The Companion & Pollinator category is DONE (roster 73/121 laddered). ~9 batches remain --
stone fruit, citrus, berries, remaining herbs/roots, pome; the 7 microgreens stay LAST per the
standing ruling. Batch 17 starts in a fresh session (Trevor, 2026-08-31).
