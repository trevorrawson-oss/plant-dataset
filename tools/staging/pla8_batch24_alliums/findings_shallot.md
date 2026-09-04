# shallot -- PLA-8 batch 24 findings (claims not placed, catalog gaps, doubts)

## Record claims with NO method that reaches the type (left in the record, not forced)
1. **onion-thrips / straw mulch.** The record says "straw mulch on the bed deters thrips".
   `straw_mulch` applies_to is `['disease_general', 'fungal_foliar']`, which does not reach
   `insect`. No rung. The claim stays in management_* prose only.
2. **onion-thrips / watering for vigor.** "Water well: vigor buys tolerance of the feeding, not
   fewer thrips." `even_watering` applies_to is `['bacterial', 'mite', 'physiological']`, no reach
   to `insect`. No watering rung; the tolerance-not-fewer-thrips point is carried inside the
   `balance_nitrogen` notes (both registers), which is the same sentence in the record.
3. **pink-root / steady water and fertility.** "Keep plants vigorous with steady water and
   fertility, since weak roots are the ones it takes." `even_watering` does not reach `fungal`,
   and `balance_nitrogen` is a RESTRAINT method, the opposite of what the record asks. No rung;
   the vigor point is carried inside `improve_drainage` seasoned (drainage relieves the wet-soil
   stress the record ties it to).

## Catalog fit that is a stretch rather than a gap (placed, flagged)
4. **onion-thrips / weed_host_control.** The record's claim is SITING ("site shallots away from
   small grains, alfalfa or clover, which shed thrips into alliums when they dry down or are cut"),
   not removal. `weed_host_control`'s catalog text is about clearing host plants at the margins.
   I wrote the rung as siting-first, with the method's own host-specific caution, and did not
   claim the reader should clear a neighbor's clover or grain. If the reviewer reads this as a
   forced fit, the rung can be dropped without loss: the siting claim is also carried in the
   `garden_sanitation` seasoned note as "handled by siting rather than by sanitation".
5. **onion-maggot / planting_time_avoidance.** The record supports it ("where the season allows,
   planting after the first flight has passed reduces damage") and the applies_to reaches
   `insect` via `insect_chewing`. The catalog's MEANS names borers and bean beetle as the
   documented cases; onion maggot is a third shape (a fly whose first flight you plant behind).
   Placed; noting the catalog text does not yet mention a root-maggot case.

## Batch-level consequences for the promote
6. **Temperature figure count.** `pink-root/crop_rotation` seasoned states the record's "75 to
   85°F" soil-temperature band (the TEMP regex catches `85°F`; `85` is in the record). The
   promote pins `EXPECTED_TEMP_FIGURES = 3`; shallot previously contributed 0. Measured today the
   other staged outs carry 3 (all chives, one of them on the RETIRED aphids ladder), so the pin
   needs re-deriving after all four re-authorings land regardless. Drop the figure if the
   re-pin is unwelcome; the note reads fine without it.
7. **Rung count.** `EXPECTED_RUNGS["shallot"]` is pinned at 21; this authoring is 24
   (thrips 3->5, maggot 3->4, downy 5->5, pink root 2->2; leafminer/white rot/botrytis unchanged).
8. **Validator.** As first delivered, `validate_out.py` could not reach PASS on any crop but onion
   because `check_no_precedent_copy` demanded onion's DECLARED_IDENTITY from a batch scoped to
   one crop. It was fixed on disk mid-run (per-crop filtering of `P.DECLARED_IDENTITIES`); the
   PASS above is under the fixed version.

## Doubts worth a reviewer's eye
9. **onion-thrips / beneficial_predators seasoned** says a broad-spectrum spray "leaves the
   axil-sheltered survivors to rebuild through the next warm, dry spell". That joins two record
   sentences (thrips shelter in the axils where sprays miss them; they build through warm, dry
   spells) into one causal claim. I believe it is a fair synthesis, not an import, but it is a
   synthesis.
10. **allium-leafminer / spinosad seasoned** says "with a sealed cover in place it has no role".
    The record says spinosad is for when covers are not practical; "no role" is my reading of
    that, stated a shade more absolutely than the record does. Soften to "little role" if wanted.
11. **downy-mildew: the orchestrator's brief said "spores are airborne".** The record does not
    use that word (it says "spreads fast in crowded, poorly aired plantings" and "lingering leaf
    wetness"). I wrote to the record and did not assert airborne spread anywhere.
12. **white-rot / garden_sanitation beginner** keeps prev_out's "dig it out along with the soil
    that comes up on the roots". The record's soil claim is about INTRODUCING the fungus on soil;
    extending it to removal is a small step. Kept because the sclerotia are on the rotted base.
