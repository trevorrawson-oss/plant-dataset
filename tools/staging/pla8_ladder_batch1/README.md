# PLA-8 ladder rollout -- BATCH 1, authored and gate-clean, NOT PROMOTED

5 crops: heirloom-tomato, jalapeno, swiss-chard, basil, fig.
38 problems, 165 rungs, ~330 register strings. Canonical at authoring time: `75b3c0f0`.

## Why this is staged rather than promoted

The READ is unfinished. Covered so far: the 6 newest rungs (all verified faithful to the crops'
own sourced prose) and the 4 method-meaning calls the bots self-flagged (all 4 were genuine
mismatches -- see below). Roughly 150 rungs remain unread.

Do NOT promote this without finishing section 4 of `docs/ladder_batch_playbook.md`. The two worst
defects found while proving this process both passed every gate and every mutation harness.

## What is already known about this content

- **Gate-clean**: control_ladder_gate 0, gate_all 121/121 with the batch merged, copy hygiene clean
  across all 330 strings (0 em dashes, 0 absolutes, 0 British spellings, 0 spaced degF).
- **ids are STABLE** and were carried across two authoring passes unchanged; they are join keys.
  Reuse them, never regenerate. See CLAUDE.md's hard rule.
- **All 12 base-watering rungs point at `water_at_the_base`**, not `bottom_watering`. That split
  (canonical `75b3c0f0`) exists because those twelve rungs used a method that means "water from
  below, in seed trays".

## Method-meaning mismatches still OPEN in this content

Found by reading; each is a method key whose catalog meaning differs from what the rung says.
`bottom_watering` was the fourth and was fixed by minting `water_at_the_base`. These three remain:

| method | used on | catalog says | the rung says |
| -- | -- | -- | -- |
| `sensible_seeding_rate` | swiss-chard/damping-off | do not sow seeds too thickly (DENSITY) | sow fresh seed at the right DEPTH, presoak the seedball |
| `yellow_sticky_traps` | jalapeno/pepper-weevil | bright YELLOW cards attract flying insects | sticky traps baited with the weevil's SCENT LURE |
| `garden_sanitation` | jalapeno/hornworms | clear away old plants and DEBRIS | TURN THE SOIL OVER to break up overwintering pupae |

Each is the same class as the `bottom_watering` defect. The likely fixes are the same shape: mint
a method whose prose matches the action (seed-quality-at-sowing, a generic pheromone/monitoring
trap, off-season tillage), rather than stretching an existing key. See playbook section 6.

## Content defects found in CANONICAL prose, recorded not fixed

- swiss-chard slug `organic_treatment_beginner`: "an iron-phosphate slug bait, **which is safe
  around pets and wildlife**" -- unhedged absolute, the PLA-253 class. The ladder already hedges it
  correctly; only the source entry is wrong.
- basil: slug `prevention_seasoned` recommends TIGHTER spacing to dry the soil, while downy mildew
  `prevention_seasoned` recommends spacing FOR AIR CIRCULATION. Real contradiction, and asymmetric:
  downy mildew is severity `high` and basil's dominant threat, slugs are `medium`.
- fig: the souring (`pests[]`) and endosepsis (`diseases[]`) entries describe substantially the same
  field observation with near-identical controls; endosepsis' own text says "control it the same way
  as souring". Possible merge candidate.
