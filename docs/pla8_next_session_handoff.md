# PLA-8 IPM ladder rollout -- where to pick up

Written 2026-08-25 at the close of the batch-4 session. `docs/ladder_batch_playbook.md` is still THE
procedure; this file is only the position and the open items.

## Verify first (CLAUDE.md, before acting)

```
shasum -a 256 crops_data_final.json     # must match LATEST.txt
git log -1 && git status -sb
python3 tools/ladder_batch.py status
```

## Position

Roster **24 of 121 laddered**, 97 remaining (~700 problems). Catalog **51 methods**.

Five promotes landed 2026-08-24/25, all pushed:

| canonical | what |
|---|---|
| `decb944d` | batch 3, the three cucumbers, roster 16 -> 19 |
| `3ec673a7` | `best_use` widened on 10 methods (11 flagged, 1 correct as written) |
| `5696aead` | bt `pros[1]`, the "only" selectivity overclaim |
| `e40cd8ec` | catalog round: `borer_stem_surgery` minted, 50 -> 51 |
| `e794969f` | batch 4, the five squashes, roster 19 -> 24 |

## THE MOST IMPORTANT THING TO KNOW

**The family cut was measuring the wrong thing until 2026-08-25.** `cmd_families` grouped on problem
NAMES and printed "identical prose", so it advertised propagate-safe twin groups that were not. 0 of
10 reported groups were real. It is fixed (`c1cd161`) and now prints TWO groupings with two different
instructions:

- **TRUE TWINS** -- byte-identical prose. One authoring pass, propagate, promote asserts identity.
- **SHARED-NAME FAMILIES** -- same problems, different prose, percentage shown. **Every member needs
  its own authoring pass.**

**Consequence for planning: only ONE true twin remains on the roster.** Batches now cost roughly one
authoring pass per crop, not one per group. ~97 crops means ~95 authoring passes. Anyone planning
from the old numbers will be wrong by about 3x.

## What to run next

```
python3 tools/ladder_batch.py families
```

**Remaining true twin: `dry-bean` + `green-beans-bush`.** `pole-beans` diverges from both, so the
natural next batch is the three beans -- 2 authoring passes for 3 crops, 27 problems -- which is the
same hybrid shape batch 4 just proved. `tools/promote_pla8_batch4.py` is the template for that shape;
`promote_pla8_batch2.py` for a pure twin; `promote_pla8_batch3.py` for a pure non-twin.

After the beans, the shared-name families: 2+2 tomatoes, collards/kale, snow/sugar-snap peas,
cayenne/habanero, 4 microgreens (**different problem schema** -- `name_beginner` / `management_*`;
decide deliberately, do not walk into it). Then 80 singletons batched by category, the largest being
Companion & Pollinator (10) and Herbs (10).

## Use the cross-sibling check; it is the cheap half of the read

`ladder_batch.py verify` now reports **CROSS-SIBLING LADDER CONFLICTS**: siblings whose source prose
agrees but whose authored ladders do not. It found batch 3's defect retroactively and two of batch
4's three real findings. It REPORTS, never refuses -- a divergence is correct when the crops' prose
makes different claims. Read every row; a batch typically produces 3-6, of which 1-2 are real.

## Open, recorded with reasons -- do not silently close

**Catalog gaps, by how often they have now recurred:**
1. **No planting-date / succession-timing method.** NEW in batch 4 and the strongest candidate for
   the next catalog round. "Time a fall succession to crop after the borer's main flight" is a
   standard control named by three of five squashes with nowhere to go, and it will recur on
   watermelon, cantaloupe, honeydew and pumpkin.
2. **No plant-vigor method.** "Keep young plants vigorous so they grow past the vulnerable stage" --
   unplaced twice per crop across batches 3 AND 4.
3. **No disease-side nitrogen method.** `balance_nitrogen` is `insect_soft_bodied` only, so "avoid
   excess nitrogen" is gate-illegal on powdery mildew. Both batches.
4. **No biofungicide or potassium-bicarbonate key**, and `neem_oil` / `horticultural_oil` are
   insect/mite-scoped, so only the sulfur third of the powdery-mildew advice is expressible. Both
   batches.
5. No conventional FUNGICIDE key at all (`carbaryl`/`pyrethroid` are the only conventional entries,
   both insecticides), so chlorothalonil is unexpressible.
6. Older, from batch 1/2: `container_culture` (three negative source reads, still unanchored),
   `certified_clean_stock` stranded on 3+ crops, a generic trap-board key, `adjust_planting_date`,
   `oil_on_silks`, `preplant_weed_control`, `avoid_wounding`.

**Existing-prose defects found and NOT fixed** (each needs its own pass; none blocks a batch):
- `organic_treatment_seasoned` recommends **chlorothalonil, a conventional synthetic, inside a field
  named `organic_`** -- downy mildew and anthracnose, all three cucumbers.
- A **false conjunction** on acorn and spaghetti's borer treatment: burying vine joints does not
  reduce next year's brood; both T1 sources attribute that only to destroying infested vines.
- **Stale anchor**: yellow-summer-squash and zucchini cite `hortnews.extension.iastate.edu`, now a
  301 to `yardandgarden.extension.iastate.edu`. Document alive, URL moved. Repoint pending.
- `slicing-cucumber`'s angular leaf spot cites only `umn_ext` while its siblings carry
  `umn_ext + clemson_hgic`, yet it KEEPS the "75 to 82°F" figure they share.
- "Wilt-resistant practices" (ungrammatical) and "individual leaves or runners wilt" (squash has
  vines, not runners) on the summer-squash twins.
- Angular leaf spot's beginner register opens "There is no cure" then recommends a copper spray.

**`best_use` narrowness, an 11th instance**: `stem_collars` is cutworm-scoped but ships against
cabbage-fly egg-laying and now the squash-borer foil wrap. The other 10 were widened in `6671ecd`.

**PLA-393 (frost-anchor spread)** is filed and Trevor deferred it. Five annual pairs, not fourteen,
one a coherent ornamental cluster. Re-verify from canonical before acting; do not inherit the issue's
numbers.

## The coverage floor is the finish line, and it is NOT armed

`control_ladder_gate`'s integrity half is wired as `whole_crop_gate` A56. The "a certified crop must
HAVE a ladder" floor is deliberately held back: arming it today takes `gate_all` from 121/121 to
24/121. Arm it when coverage lands. That, not "121 laddered", is what closes this arc.

## Process notes worth carrying

- **The mutation harness earned its place five times this session.** Every promote needed 2-3 runs.
  Every survivor was a masking or unreachability defect invisible to a fully green suite: a guard
  shadowed by an earlier check, a guard whose test read a constant instead of driving the code, a
  guard reading a field the staged files do not carry, a guard whose only reachable state nothing
  constructed. **Assume a new guard is vacuous until an injection proves otherwise.**
- **When a gate fires on text you believe is correct, reword before you weaken the gate.** The
  hygiene check flagged "does not always work" -- a real hedge -- and rewording was right. The
  opposite also happened: a fuzzy contradiction test flagged approved copy, and there the TEST was
  wrong. Tell them apart by asking whether the rule or the instance is the thing you can defend.
- **A diff shows what DIFFERS, never what a record asserts.** Briefing agents on what a sibling does
  not claim, inferred from a diff, was wrong in batch 3 and cost a wrong instruction to three agents.
  Batch 4's briefs told each agent to read only its own file.
- **Trust the bots' self-flags.** Across batches 3 and 4 every flagged "loose fit" was worth reading,
  and the ones that turned out to be genuine gaps came from agents refusing to force a key.
