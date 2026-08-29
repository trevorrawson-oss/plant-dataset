# brussels-sprouts / `harlequin-bug` -- the `trap_cropping` rung

Recorded 2026-08-28 from `plant-dataset-e3`, the session running the trap-cropping catalog round.

> **EXECUTED 2026-08-28.** The mint and backfill landed first (`be444e25` -> `86c5396a` ->
> `96cbc68c`), so the condition below was met and the rung IS in batch 12. That kept e3's backfill
> at 10 rather than 11 and shipped this crop correct the first time. The contract was followed in
> full; what changed in the promote is recorded at the bottom. Kept as the record of why the rung
> reads the way it does.

## The condition

**Only author this rung if `trap_cropping` exists in batch 12's BASE canonical.** If the mint has
not landed, the ladder gate rejects the unknown method key and the promote is burned. If batch 12
promotes first, brussels-sprouts stays unplaced and becomes an 11th rung in e3's backfill, which
e3 has explicitly accepted ("I would rather eat 45 minutes").

## Why it earns a rung at all

brussels-sprouts' harlequin bug prose is a textbook instance WITH the safety-bearing timing:
"deploy an early trap crop of cleome or mustard to divert overwintering adults, then destroy it
before the main crop is set out." Both registers carry it. It is one of the 6 unladdered crops in
section 2b of `docs/2026-08-28-trap-cropping-mint-handoff.md`.

## The contract, so this rung matches the other ten

1. **Group `DESTROY_STATED`.** This crop's prose carries the removal step, so the rung SHOULD
   restate it, and SHOULD carry the attribution phrase **"this crop's guidance"**. e3's three
   `DIVERT_ONLY` rungs are forbidden that phrase; this one is not.
2. **Name cleome or mustard, and nothing else.** Both appear in this crop's own prose. e3 carries
   a species guard because jalapeno's prose names nasturtium, and a copied rung would have put
   mustard on a non-brassica.
3. **Point at the method's `cautions` for the removal deadline rather than restating it.** That
   sheet carries the UMass "before eggs hatch" line. Do not paraphrase a timing deadline into a
   rung note.
4. **Placement: index 1**, cultural tier, at the END of the cultural run. The shipped ladder is
   `garden_sanitation > floating_row_cover > handpick > insecticidal_soap > neem_oil > pyrethrin`,
   so the rung goes between `garden_sanitation` and `floating_row_cover`. Not the front, not
   appended last.

## If it is added at rebase time

It is one rung on one problem. Re-pin `BASE_SHA`, re-run the promote for a fresh `POST_SHA`,
update the suite's expected rung count for brussels-sprouts (48 -> 49) and the batch total
(104 -> 105), and **re-run the mutation harness**, not just the tests.


---

## What executing it changed in the promote (2026-08-28)

Adding the rung inverted one guard and scoped two others. Recorded because "add a rung" understates
it:

- **`check_base_premises` INVERTED.** It used to refuse a base CONTAINING `trap_cropping` (the batch
  carried no rung, so brussels would have shipped silently wrong). It now refuses a base LACKING it,
  because the rung would fail the ladder gate as an unknown method.
- **The batch-wide `trap_cropping` refusal became SCOPED** to `TRAP_OK = ("brussels-sprouts",
  "harlequin-bug")`, in both `check_read_fixes` and `verify_post`. Every other problem still refuses
  it, and parsley's parsleyworm is the one where a rung actively reverses the advice.
- **`TRAP_INDEX = 1` is pinned in `verify_post`.** Moving the rung leaves the ladder tier-legal, so
  nothing else would notice a wrong placement.
- **`NOTE_BAN_EXEMPT`** exempts that one rung from the `"trap crop"` / `"sacrificial"` note-word ban.
  The ban exists to keep parsley's conservation language from being written up as a control;
  applying it to a legitimate trap-crop note would be a scope error.
- **Counts:** brussels-sprouts 48 -> 49 rungs, batch total 104 -> 105.
- **New `trap` mutation family** covering presence, placement and scope in both directions.
