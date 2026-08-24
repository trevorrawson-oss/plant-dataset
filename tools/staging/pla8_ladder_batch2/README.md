# PLA-8 ladder rollout -- BATCH 2, the four corns. READ COMPLETE, 22/22 verified.

4 crops: sweet-corn, field-corn, popcorn, flint-corn. 8 problems each, 22 rungs each, 88 total.
Canonical at authoring time: `0754031d`.

## This is the FIRST batch cut by FAMILY rather than by size

Batch 1 was five unrelated crops chosen "fewest problems first", which produced 38 problems with
ZERO shared prose and five separate source sets to read. `ladder_batch.py` was corrected in `c0915d0`
to group by shared prose instead.

**The payoff, measured field by field: 276 of 288 field instances across the three siblings are
BYTE-IDENTICAL to sweet-corn.** The only divergence is Raccoons, and only its symptoms/cause/
prevention -- the treatment text matches even there, and the differences are cosmetic ("sweet corn"
-> "corn", "milk stage" -> "fill out").

So the read was **8 problems, not 32**, and the four `out_*.json` files are byte-identical by
construction: one crop was authored and the ladders were propagated mechanically. The promote's
guard suite asserts that identity, because it is the claim the family batching rests on.

## What the read found

**ZERO method-meaning mismatches**, against 22 of 165 (13%) in batch 1. Two reasons, neither luck:
the catalog grew 43 -> 50 across four rounds between the batches, and the authoring agent refused to
stretch a key four separate times rather than paper over a gap.

Full read: `FINDINGS_B2.md` in the session scratchpad. The two findings worth carrying forward:

1. **`off_season_tillage`'s gloss is too narrow, and it is one batch old.** Minted in r2 the same
   session, glossed around the hornworms that motivated it ("soil-pupating Lepidoptera"). European
   corn borer overwinters INSIDE THE STALK. The action is identical and correct; the stated
   MECHANISM names a life stage this pest does not have. A mint glossed around its motivating case
   is narrower than its own action. Prose fix, deferred arc.
2. **The `bt` CATALOG method still carries the absolute swept from nine crops in `9116050`** --
   "It only affects caterpillars ... a treated vegetable is safe to eat". Less severe than the crop
   version was, because the same field self-corrects two sentences later and `cautions` names
   swallowtails and monarchs. But it is the exact INVERSE of this arc's three earlier cases, where
   the catalog was right and the crops were wrong. Check both directions. OWED.

## Raccoons required a new method and exposed a gate hole

The authoring agent found no expressible rung for the crop's highest-severity problem and correctly
refused to pad, emitting `"control_ladder": []`. That refusal produced BOTH:
  * `exclusion_fencing`, minted in r4 (`0754031d`) and anchored to two T1 sources that disagree on
    the second wire height, with both named in the prose; and
  * a gate hole -- `control_ladder_gate` skipped `None` correctly but `[]` is not `None`, so an
    empty ladder passed every gate. Fixed in `a256211`; `null` and `[]` are now distinct.

## Structural limit found, not a gap

Stewart's wilt names a treatment aimed at its flea-beetle VECTOR. That is inexpressible: spinosad's
applies_to is insect-only and therefore illegal under a `bacterial` problem, and the model has no
cross-reference from a disease to its vector's own ladder. `floating_row_cover` carries the
exclusion half only. Expect this to recur on other vector-borne diseases.

## Gaps recorded, deliberately not minted

`adjust_planting_date` is the highest-frequency: unplaceable in FOUR of eight entries (earworm,
cutworms, flea beetles, rust), in two directions but one control. Plus `oil_on_silks`,
`preplant_weed_control`, `avoid_wounding`. All recorded in
`tools/build_pla8_catalog_r4_content.py:NOT_MINTED` and guarded so the record cannot be dropped.
