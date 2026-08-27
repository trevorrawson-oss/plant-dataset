# PLA-8 batch 9 (THE ROOTS) -- authored, read, adjudicated; promote BLOCKED on the batch 8 commit

turnip, radish, carrot, beet. 29 problems, **134 rungs staged** in `tools/staging/pla8_batch9_roots/`.
Base would be `043a7272` (batch 8's output, applied but UNCOMMITTED), so the replay-pinned suite
cannot be built until that commit lands and registers in `COMMIT_FOR`. Everything up to the
promote is done.

## The authoring run died mid-flight and the outputs survived

All four agents were killed by a monthly spend limit **after** writing their output files. Files
verified complete against source: problem counts match (9/7/6/7), families in order, every
problem carries a type and a non-empty ladder, every rung both registers. **No relaunch was
needed.** What was lost is the four self-reports (loose fits, gaps, prose oddities), so this
read did that work directly rather than starting from the bots' flags.

## Adjudications

1. **beet's `handpick` rung DROPPED from the leafminer ladder (the real catch).** Its note said
   "pick off any leaf with a pale winding trail" -- the same action as its own
   `garden_sanitation` rung two places above ("pull off the first tunneled leaves"). `handpick`
   MEANS catching free-living insects on a scouting walk ("big enough to spot and slow enough to
   catch"); a maggot sealed between leaf surfaces is not handpickable, and spinach put the same
   advice under sanitation. A legal-but-wrong-meaning duplicate: the `bottom_watering` shape,
   found only by reading. Ladder 6 -> 5 rungs, batch total 135 -> 134.
2. **beet's `flea-beetle` (singular) converged to `flea-beetles`.** The agent followed
   swiss-chard, which ships the lone singular id; 14 crops ship the plural, including turnip and
   radish in this same batch. Beet is at FIRST authoring so the id was free to choose.
   **swiss-chard stays the outlier** -- its id is a shipped join key and re-deriving it is
   forbidden; that remains the batch-8 finding.

## Prose-driven divergences, each verified against the source and pinned

| split | verdict |
| -- | -- |
| copper on **alternaria leaf spot** | turnip YES (its prose names copper), radish NO ("radishes usually grow faster than the disease") |
| copper on **downy mildew** | turnip + beet YES -- both prose say "a copper fungicide is a last resort", unlike spinach's "limited efficacy" undercut in batch 8 |
| spinosad on **flea beetles** | turnip + radish YES (prose names it), beet NO (stops at kaolin clay, which is where its prose stops) |
| `garden_sanitation` on **aphids** | turnip YES, beet NO -- 6 of 7 prose fields differ between the two entries |
| **damping-off** rung count | radish 2 rungs, no sanitation: its prose says re-sow the bare spots and never says remove collapsed seedlings, unlike spinach/arugula/carrot/beet |

## `prompt_harvest` on three problems, and why it transfers

The catalog's documented cases are fruit crops, but its MEANS is "taking the crop you do want,
sooner", and each use restates the crop's own sentence: radish wireworms ("harvest promptly so
roots spend less time exposed"), carrot rust fly ("harvesting promptly rather than leaving roots
in the ground"), carrot cavity spot ("harvest promptly rather than holding mature roots in wet
ground"). Same shape as kaolin_clay and reflective_mulch: documented cases narrower than the
action. KEPT on all three, flagged here so a later pass can re-argue it.

## Ids: 29 minted, all with roster precedent or genuinely new

Reused: `flea-beetles`, `cabbage-root-maggot`, `aphids`, `harlequin-bug`, `clubroot`,
`white-rust`, `downy-mildew`, `alternaria-leaf-spot`, `black-rot`, `damping-off`,
`beet-spinach-leafminer`, `root-knot-nematode`, `cercospora-leaf-spot`, `carrot-rust-fly`
(celery's). Genuinely new, no precedent: `wireworms`, `common-scab`, `aster-yellows`,
`carrot-leaf-blight`, `cavity-spot`.

## Structural state

`ladder_batch verify`: **structural checks PASS**, 68 method-meaning pairs read, cross-sibling
conflicts 2 (both beet-vs-turnip, both adjudicated above as prose-driven). NO mint needed.

## What the promote needs (after the batch 8 commit)

Base `043a7272` registered in `COMMIT_FOR`; guards pinning each divergence above in BOTH
directions, the handpick-off-leafminer refusal as a refusal-spec, the `flea-beetles` convergence,
and the standing batch-wide refusals (no DE anywhere, no neem/soap on flea beetles).
Roster would go 37 -> 41.
