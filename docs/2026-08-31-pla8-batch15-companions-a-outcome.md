# PLA-8 -- batch 15, companions A: outcome

Written 2026-08-31. Base `c76f14f1`; output `098dd0b1`. Crops: marigold, zinnia, cosmos,
calendula, sweet-alyssum. 33 problems, 84 rungs, roster laddered 63 -> 68, catalog untouched
at 61. The first Companion & Pollinator batch under Trevor's deferral-lift ruling, and the first
batch on the note-shaped third schema.

## 1. THE SCHEMA, AND WHAT THE TOOLING FIX BOUGHT

All 33 problems carry `name`/`severity`/`audience`/`note_beginner`/`note_seasoned` only -- no
classic advice fields, no per-problem sources. The promote's `check_schema_premise` asserts the
note pair on every target so the alignment correspondence can never compare tuples of None. The
`ladder_batch` note-schema fix (shipped with batch 14) made the family cut honest here:
**measured, ZERO byte-identical note pairs exist across the five crops** -- before the fix all
five Aphids records would have collided as false twins. Every ladder was authored per-crop.

## 2. THE COMPANION INVERSION, GUARDED THREE WAYS

These are the crops other plantings use AS trap, banker and insectary stands. zinnia's
Japanese-beetle record is the trap-cropping round's pinned INVERTED exclusion ("part of their
trap-crop value"); calendula's aphid note describes the crop "sometimes grown as a deliberate
trap or banker plant". A trap rung on any of them tells the reader to destroy the crop they grow.

1. `trap_cropping` FORBIDDEN batch-wide.
2. Trap vocabulary ("trap crop", "trap-crop", "sacrificial", "banker") banned from every note --
   unplaced content must not creep back through an allusion. The suite proves the ban non-vacuous
   against the SOURCE notes, which genuinely carry the vocabulary.
3. The placeable half stays placed: alyssum/marigold/zinnia/cosmos/calendula recruit predators
   that suppress their OWN aphids, shipped as `beneficial_predators` conservation rungs -- the
   read distinguished own-aphid suppression (place) from protect-other-crops value (unplace) on
   every record.

The inversion cuts the other way once: both Japanese-beetle records advise AGAINST pheromone
traps (they concentrate beetles), and each handpick rung is REQUIRED to keep that
anti-recommendation, because a dropped do-not-do has no token to scan for once it is gone.

## 3. IDS

- **`zinnia-leaf-spots` minted species-scoped** (A. zinniae + Xanthomonas, both zinnia-scoped);
  the roster's `alternaria-leaf-spot` is the brassica organism on seven cole crops and is refused
  in both directions.
- **`gray-mold`** (marigold + cosmos, one string) reuses strawberry's id. FILED: the roster
  already carries a second Botrytis string, artichoke's `botrytis-gray-mold` -- a pre-existing
  id divergence for the same fungus, recorded here, not resolved.
- sweet-alyssum reuses **`cabbageworms`** (it is a brassica; same complex) and `flea-beetles`;
  the rot records reuse `root-and-stem-rots`/`damping-off` per the lead-name convention. New:
  `japanese-beetles`, `leaf-spots`, `zinnia-leaf-spots`, `aster-leafhoppers`, `stem-canker`,
  `cucumber-mosaic`. `aster-yellows` typed `bacterial` per the carrot precedent (a phytoplasma).

## 4. THE READ

- **Two introduced facts removed**: calendula's soap rungs said "hotter than 90°F" -- standard
  label advice, but the figure appears nowhere in this crop's notes.
- **A dubious source mechanism trimmed, not amplified**: the marigold/zinnia mite notes claim
  base watering "raises humidity around foliage"; the cosmos agent flagged the mechanism as
  backwards, and the rungs now keep only the well-supported drought-stress half. The source
  claim is FILED as a prose tension (it also appears in the cosmos and sweet-pea-family records).
- **The recurring PM pattern**: four companion PM records prescribe base watering; the catalog's
  own USU-backed caution says powdery mildews need no leaf wetness. Rungs restate the crop's
  action with the humidity framing and no splash claim (the melon-batch treatment). FILED with
  the same source-truth flag the agents raised on the notes themselves.
- One shipped-rung echo reworded. Divergent aster-yellows ladders (marigold 1 rung vs carrot's
  row-cover-bearing ladder) are legitimate: marigold's note never names covering, and the agent
  reported the gap rather than importing the precedent.

## 5. VERIFICATION

- Suite **58/58 both runners**. One verify_post branch was DELETED as unreachable rather than
  kept as phantom coverage: every new id doubles as a NO_MATERIAL or pheromone lookup key, so
  the generic did-not-ship branch could never fire on its own (the trap-round rule); the
  specific per-id "lost its <id> problem" messages are the real protection, and the suite
  asserts one of them directly.
- Harness **36/36, zero survivors, first full run** (inversion 7/7, materials 5/5, taxon 5/5,
  validate 6/6, blast 5/5, alignment 2/2, echo 2/2, ids 2/2, schema 1/1, mechanics 1/1).
- Gauntlet: gate_all **121/121**, control_ladder_gate **0**, register_completeness **PASS**,
  whole_crop_gate PASS on all five, release_verify **clean** vs `c76f14f1`.

## 6. NEXT

Batch 16 = companions B (echinacea, bee-balm, chamomile, borage, sweet-pea; 32 problems),
pre-mapped. Its sharp calls: bee-balm's "Rust" id should be organism-scoped if the record names
*Puccinia menthae* (shareable with the mint-family herbs later); sweet-pea's root rots choose
between the generic `root-and-stem-rots` and the peas' `root-rots-damping-off` on prose-twin
evidence (*Lathyrus* is Fabeae, the same kinship that let fava reuse it); echinacea brings the
roster's first `rabbits-and-deer` vertebrate ladder since the corns and a new `eriophyid-mites`
mite id. Sweet-pea carries no weevil problem, so the *Bruchus* trap does not arise. After 16:
~9 batches; microgreens last.
