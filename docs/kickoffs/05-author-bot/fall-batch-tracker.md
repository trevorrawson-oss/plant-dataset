# Fall/winter crop batch — tracker

Seasonal priority (Trevor, 2026-06-29): get cool-season crops live for the late-summer/fall planting
window. Authored via `05-author-bot/KICKOFF.md`; each is a normal full GS record whose calendar is
fall/winter-weighted. Templates are the 4 live cool-season anchors (broccoli, carrot, lettuce-leaf,
onion).

| target | template | archetype/basis | status | notes (key refit) |
|---|---|---|---|---|
| **radish** | carrot | cool_season_annual / frost_anchored | **PILOT — package built** (`~/Downloads/pilot-radish-from-carrot/`) | ~22-30 day maturity (not 70), Brassicaceae (family CHANGES from carrot's Apiaceae), flea beetles/root maggots, succession sowings |
| kale | broccoli | cool_season_annual / frost_anchored | queued | leafy non-heading, very cold-hardy, no head-formation calendar |
| spinach | lettuce-leaf | cool_season_annual / frost_anchored | queued | very cold-hardy, bolts in heat, fall/overwinter emphasis |
| beet | carrot | cool_season_annual / frost_anchored | queued | taproot + edible greens, different pests/DTM |
| cabbage | broccoli | cool_season_annual / frost_anchored | queued | heading brassica, longer DTM, storage |
| brussels-sprouts | broccoli | cool_season_annual / frost_anchored | queued | long season (~90-180d), sprouts up the stalk, frost-sweetened, progressive harvest |

## Loop per crop
author (claude.ai + web) -> handoff patch -> Claude Code applies (`apply_patch.py`) + gates (A2-A36)
+ release_verify -> daily biology review (`04-daily-review/`) -> correct + re-gate -> counts. Then a
plant-astro submodule bump (Trevor's call) puts the batch live.

## Pilot-first
Prove the pipeline on radish (the refit is glaring, so it tests the discipline) before running the
other 5. Watch: authoring quality, sourcing honesty (spot-check URLs), Trevor's per-crop review cost
(sets the sustainable daily batch size).
