# PLA-8 -- disease-escape sowing has no catalog key: the measurement

Written 2026-08-28 against canonical `be444e25`, during batch 12 (broad-beans-fava,
brussels-sprouts, parsley). This is a measurement and a ruling, not a handoff: it records a gap
found while authoring, so the next catalog round can price it without re-deriving it.

**This is the second gap of the trap-cropping shape**, found the same way (an authoring agent
reporting advice it could not legally place) and measured the same way. Read
`docs/2026-08-28-trap-cropping-mint-handoff.md` first; that round is the model for this one.

---

## 1. THE GAP

Six shipped ladders and one crop in batch 12 carry the same recommendation in their source prose:
**sow early so the crop reaches maturity before a weather-driven disease builds.** There is no
catalog key for it, so all six shipped without it.

The near neighbor is `planting_time_avoidance`, and it is illegal here rather than merely loose:

```
planting_time_avoidance | tier: cultural | applies_to: ['insect_chewing', 'insect_boring']
best_use: A pest whose damage falls in a predictable, locally published stretch of the season,
  on a crop quick enough to finish before it or start after it. The two documented cases differ
  in shape: the squash vine borer has a single flight to get behind, while the Mexican bean
  beetle runs several generations a year whose damage still concentrates in July and August.
  Distinct from crop rotation, which moves the planting in space; this one moves it in time.
```

`applies_to` carries no disease target, so the gate refuses it on a fungal problem. That refusal
is correct and should not be worked around by a bare `applies_to` edit -- see the ruling in §4.

| near-miss | why it is not this |
| -- | -- |
| `planting_time_avoidance` | dodges a pest's *flight window*, a locally published biological calendar; escape sowing races a *weather-driven epidemic* that has no published start date |
| `resistant_varieties` | already on all six ladders, and genuinely different: it changes WHAT you plant, not WHEN |
| `crop_rotation` | moves the planting in space |
| `prompt_harvest` | acts at the END of the season on fruit that feeds the problem; this is a decision made at sowing |
| `sound_sowing_practice` | about seed quality, depth, soil warmth and restrained watering against damping-off; says nothing about the calendar |

---

## 2. THE MEASUREMENT

Scan over every `_beginner` / `_seasoned` prose field of every problem on all 128 crops for a
sowing-date shift, restricted to problems whose `type` is a disease class. **Hits were READ, not
counted.** 8 raw hits, 1 discarded, **7 real instances on 7 crops.**

### 2a. BACKFILL -- 6 rungs onto ladders that ALREADY SHIPPED

All six open with `resistant_varieties`, so the new rung belongs at the FRONT of each ladder
beside it: both are decisions made before anything is in the ground.

| crop | problem id | the prose | current ladder |
| -- | -- | -- | -- |
| sweet-corn | `common-rust` | "plant early so the crop matures before rust builds late in the season" | resistant_varieties > water_at_the_base > garden_sanitation |
| field-corn | `common-rust` | same sentence | same |
| popcorn | `common-rust` | same sentence | same |
| flint-corn | `common-rust` | same sentence | same |
| sugar-snap-peas | `powdery-mildew` | "sow early so the crop finishes pod fill before the late-season mildew weather" | resistant_varieties > airflow_spacing > garden_sanitation > biofungicide > sulfur |
| snow-peas | `powdery-mildew` | same sentence | same |

The four corn instances are one sentence repeated across a template family, and the two pea
instances are another. **That is two authoring decisions, not six** -- price the round that way.
(`citation-arc-repriced-by-decision-unit`: a count at the wrong unit inflated an arc 4-20x.)

### 2b. AUTHORING -- 1 crop, live in batch 12

**broad-beans-fava / `broad-bean-rust`**: "Sow early so the crop matures before the warm midsummer
weather that drives rust." Batch 12 ships this ladder as `airflow_spacing > crop_rotation >
garden_sanitation`, with the escape-sowing advice recorded as unplaced. **If the key is minted
before batch 12 promotes, fava takes the rung and the backfill stays at 6; if not, the backfill
becomes 7.** Unlike the trap-cropping round, this is not a deadline worth reordering for: one
rung, one crop.

### 2c. DISCARDED -- 1 false positive

**jalapeno / `mosaic-viruses`**: matched on "remove infected plants early," which is roguing, not
a sowing date. Recorded so the next scan does not re-flag it.

---

## 3. NOTHING IS CURRENTLY WRONG, AND THAT WAS VERIFIED

Before treating this as a defect, I checked whether the six shipped ladders had smuggled the
advice into an illegal or ill-fitting rung. They had not.

- Walked **every rung in canonical** against its method's `applies_to` and its problem's
  `TYPE_TARGETS` entry: **0 illegal rungs live.**
- All **13 live `planting_time_avoidance` rungs sit on `type: insect`** problems (carrot,
  green-beans-bush, sugar-snap-peas, pole-beans, snow-peas, arugula, radish x2, kohlrabi,
  turnip x2, beet, dry-bean).

So this is a gap to fill, not a mess to clean up. The six ladders are honestly short: they
dropped advice they could not place rather than mis-placing it, which is the behavior the arc
asks for.

---

## 4. THE RULING: MINT, DO NOT WIDEN

A bare `applies_to` widening of `planting_time_avoidance` is **refused**, on three grounds:

1. **The mechanisms differ.** `planting_time_avoidance` gets a crop behind or ahead of a pest's
   flight, which extension services publish as local degree-day or calendar windows. Escape
   sowing races a weather-driven epidemic with no published start date. Its own `best_use` says
   "a pest whose damage falls in a predictable, locally published stretch of the season" -- a
   sentence that is simply false for late-season rust.
2. **The prose would have to be rewritten, not extended.** The G5 rule from the catalog r5 round
   is that a widening moves its PROSE with its target. Here `best_use` names two documented insect
   cases and defines the method by pest phenology; covering both mechanisms means writing a
   different entry. When a widening requires a rewrite, it is two methods.
3. **Precedent.** `trap_cropping` is being minted rather than folded into `weed_host_control` for
   the same reason: a distinct action earns its own key. `pyrethrin` was minted rather than mapped
   onto `pyrethroid` because a near neighbor with the wrong meaning is worse than a missing key.

Proposed key: **`disease_escape_timing`**, tier `cultural`, `applies_to: ['fungal_foliar']` --
tight, since all seven instances are foliar fungal. Widening later is cheap; over-widening at
mint time is what put `certified_clean_stock` and `reflective_mulch` out of step with their own
`best_use`. Alternative name considered: `early_maturity_escape`.

**This ruling is a starting position, not a conclusion.** Re-test it against the T1 documents: if
the extension literature frames corn rust and pea mildew escape as one practice with insect
timing under a single "planting date" heading, the widen case gets stronger and should win.

---

## 5. WHAT THE T1 READ MUST ANCHOR

Not "early planting is good." The claim that carries the risk is **the escape is a race the
grower can lose**: sowing early trades one exposure for another (a cold, wet seedbed, and on
favas the seed-decay and bean-seed-fly window that batch 12 documents on the same crop). An
entry that says "sow early to beat rust" without the counter-exposure is advice that can cost a
stand. State it in the cautions, the way the trap-cropping entry must state destroy-before-
dispersal.

Do not mint a method you cannot anchor (`container_culture` is still owed for exactly that
reason). Candidate T1 sources already admitted in `source_catalog`: `umn_ext`, `ncsu_ext`,
`clemson_hgic`, `usu_ext`, `wsu_ext`.

---

## 6. SEQUENCING

Do NOT run this concurrently with the `trap_cropping` round. Two catalog mints plus batch 11's
`certified_clean_stock` widening already put three mutations against one catalog subtree in
flight; a fourth is how a rebase gets skipped. This round should follow trap-cropping, and its
backfill is small enough to ride along with whatever batch is promoting when it is ready.

A related, larger gap was measured at the same time and is NOT written up here because reading
its hits split it into two different claims rather than one: **"sow into warm soil so the
seedlings outrun the pest"** (corn cutworms x4, corn flea beetles x4, jalapeno, okra, and fava's
bean seed fly). That is a vigor / grow-through concept, not a calendar one, and it is currently
carried inside adjacent rungs' notes on the shipped corn and brassica ladders. It needs its own
measurement pass before anyone prices it. Four further raw hits were my scan catching the word
"seedbed" inside row-cover sentences on swiss-chard, radish, turnip and beet; they are not
instances.
