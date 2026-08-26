# PLA-8 BATCH 5 -- the three beans

**Canonical `acf33780` -> `7c3e5d71`.** 3 crops, 27 problems, **131 rungs** (44 + 44 + 43), 262
register strings. Roster laddered **24 -> 27** of 121. No control_method, no source, no crop outside
the three.

| crop | problems | rungs | how it was authored |
| -- | -- | -- | -- |
| `green-beans-bush` | 9 | 44 | authored |
| `dry-bean` | 9 | 44 | **propagated** from green-beans-bush (true twin) |
| `pole-beans` | 9 | 43 | authored independently (75.7% shared prose) |

**Two authoring passes for three crops.** The last true twin on the roster.

---

## The premise, and where it is checked

`dry-bean` and `green-beans-bush` carry **byte-identical problem prose in order**, which is the only
thing that licenses copying one crop's ladders onto the other. Batch 4 asserted that premise by
comparing the two STAGED files, which proves a propagation happened and says nothing about whether
it was allowed.

**This promote checks it in canonical.** `check_twin_premise` compares eleven prose fields across
all nine problems straight out of the dataset, and refuses in both directions: the twin must match,
and `pole-beans` must NOT, because a sibling that had quietly become identical would mean the batch
is authoring the same crop twice and calling it two passes. Measured at promote time: the twin is
identical, and pole-beans differs on **35 field pairs**.

`control_ladder` is deliberately excluded from the compared fields. Including it would make the
premise self-referential: true by construction after the promote and worthless before it. A test
pins that exclusion.

---

## The read found four defects. Each is fixed and pinned.

Applied by `apply_read_fixes.py` (kept here so the fixes are reproducible rather than hand-edits),
and re-asserted by the promote in both `check_read_fixes` and `verify_post`.

**1. `pole-beans` / Mexican bean beetle: `off_season_tillage` -> `garden_sanitation`.**
The batch-1 defect class, and the one no gate can see. The seasoned clause is BYTE-IDENTICAL on both
siblings -- *"Work crop debris into the soil promptly after harvest to remove overwintering
shelter"* -- and the two authoring passes filed it under different keys. `off_season_tillage` MEANS
destroying soil-pupating stages; its own text says *"the pupal cells of soil-pupating Lepidoptera
such as the hornworms"*. Mexican bean beetle overwinters as ADULTS near woodland edges, which both
crops' own `cause` field states. Same-sounding action, wrong mechanism.

**The pole-beans pass flagged this itself and used the key anyway**, writing that "the catalog's
mechanism is soil-pupating larvae, whereas this crop says MBB adults overwinter near woodland
edges." Third batch running where a self-flagged loose fit was a real mismatch.

**2 + 3. `green-beans-bush` ordering**, on Anthracnose and Bean root rots. The cross-sibling check
flagged both: same method SET, different order, and the prevention prose the differing rungs are
built from is byte-identical across the two crops. Its own rule is that a divergence is a defect
"when the prose they share is the prose the differing rung would be built from." Same-tier moves, so
nothing is added or removed. Direction taken from the SOURCE's order, not the sibling's.

**4. The root-injury clause leaves `sound_sowing_practice`.** That method's `best_use` ENUMERATES
its scope -- "seed quality, depth, soil warmth and restrained watering" -- and handling damage at
planting is outside the list. The crop's prose does say *"Avoid damaging the roots when planting"*,
so it is a real sourced control with no catalog home: **recorded as a gap, not stretched onto the
nearest key.** The pole-beans pass refused it for the same reason.

**After the fixes, cross-sibling conflicts went 3 -> 1**, and the survivor is adjudicated correct
(Bean rust: the two crops' prevention prose genuinely differs, "stakes" vs "poles and trellis").

---

## One divergence that is CORRECT, pinned in both directions

`augmentative_release` appears on the twin's Mexican bean beetle ladder and **not** on pole-beans'.
The twin's prose names the wasp in both registers (*"a tiny helper wasp is sold to control them"* /
*"the parasitic wasp Pediobius foveolatus is sold for biological control"*); pole-beans' prose names
it in neither. Pinned both ways, so a later pass can neither propagate the claim across the family
nor drop it from the crop that earns it.

---

## The batch found a defect in the catalog round that preceded it

This is the first batch authored against the r5 catalog round, and it repaid it immediately.
`planting_time_avoidance.best_use` demanded "one main generation" while naming Mexican bean beetle
as a documented case; Clemson, the cited document, says three generations. **The two passes
disagreed about the fit, each correctly quoting a different half of the sheet**, which is the
signature of a sheet that says two things. Closed separately in `22d176c` before this batch landed.

The promote requires the r5 round to actually be reachable here -- `planting_time_avoidance` on
Mexican bean beetle, `wet_foliage_discipline` on the bacterial blights, `balance_nitrogen` on white
mold, on all three crops. Minting a method the batch then does not use would mean the round was not
needed.

---

## Fidelity check

Nine specifics that looked importable were checked against the crop's own prose: an eight-day mite
generation, *Rhizoctonia*/*Pythium*/*Fusarium* by name, two-year debris survival, mosaic viruses,
the Mid-Atlantic range claim, honeydew and sooty mold, the 10-day copper schedule. **All nine are in
green-beans-bush's own record.** And pole-beans' rungs claim nothing its prose lacks: every term its
record drops (the wasp, pyrethrin, the range claim) is absent from its rungs too.

---

## Catalog gaps, hit independently by BOTH passes

Neither pass forced a key for any of these; all were reported as unplaceable.

- **No botanical pyrethrin key.** The prose names "a pyrethrin"; `pyrethroid` is a synthetic
  conventional. Different material, different tier. Both refused it.
- **No conventional FUNGICIDE key at all** -- both conventional entries are insecticides -- so
  chlorothalonil, named in anthracnose's seasoned register, is unexpressible.
- **No weed-host control.** "Control nearby weeds that harbor them" (aphids) has no home;
  `garden_sanitation` means debris cleanup, a different action.
- **No dust-suppression key.** "Avoid the dusty conditions mites thrive in."
- **No general scouting key.** The monitoring keys are all pest-specific. Both passes folded the
  scouting cue into `water_spray`'s note and flagged that they had.
- **No equipment/tool hygiene key.** "Clean or replace stakes between years" was folded into
  `garden_sanitation` by both passes, both flagging the fit. Third instance; `tool_and_hand_hygiene`
  has been owed since batch 1.

---

## Existing-prose findings, RECORDED NOT FIXED

Read-only on canonical outside this batch's own fields.

1. **Bean rust advises cleaning reused STAKES on a BUSH bean record.** Bush beans are not staked; it
   reads as boilerplate shared across the bean trio. Same template-carryover class as batch 4's
   "runners" on squash.
2. **The sulfur schedule disagrees between registers.** Seasoned says "a 10-to-14-day schedule";
   beginner says "every week or two", which is 7 to 14. The rungs carry the seasoned figure.
3. **Bean root rots: the beginner register drops the measurement depth.** Seasoned says "about 69°F
   at a 4-inch depth"; beginner says only "about 69°F", which the reader cannot reproduce.
4. **Mexican bean beetle's cause and prevention are not reconciled.** `cause` says adults overwinter
   near woodland edges; `prevention` says working debris in removes overwintering shelter. Both are
   in the source; as written the record implies the bed is the whole source.
5. **Anthracnose: the beginner register silently drops chlorothalonil** while the seasoned keeps it.
   A register asymmetry in a PRODUCT claim, not tone.
6. **Neither the sulfur 90°F heat caution nor the copper aquatic-toxicity caution appears in the
   crop prose**, though the catalog method sheets carry both. Not imported (they are not in the
   crop's prose), but worth a corrections-log line.
7. **The Pediobius wasp is credited to `clemson_hgic`** on all three beans, and **neither of
   Clemson's two bean factsheets contains it** (both fetched and read 2026-08-25). UMD publishes it.
   True claim, wrong attribution.

**Also recorded, and NOT a defect:** the roster carries three spellings for spider mites
(`spider-mites` 4x, `two-spotted-spider-mite` 1x, `twospotted-spider-mite` 1x) and two for flea
beetles. Every one faithfully slugs its OWN crop's problem name, so the ids are internally correct
and the divergence is in the NAMES across crops. Nothing joins across crops today, so it costs
nothing yet; a cross-crop query on spider mites would miss two of six. This batch's
`two-spotted-spider-mite` matches strawberry's shipped id exactly.

---

## Verification

`gate_all` **121/121** · `control_ladder_gate` **0** · `variety_resistance_gate` **0** ·
`variety_ladder_delta_gate` **0** · `register_completeness` PASS · `register_coverage` PASS ·
`whole_crop_gate` PASS on all three · `release_verify` **clean** (blast radius declared exactly:
only the three crops changed) · COMPACT preserved · copy hygiene **0 of 262 strings**.

**Guard suite** `tools/test_promote_pla8_batch5.py` -- 55 tests.
**Mutation harness** `tools/mutate_pla8_batch5_suite.py` -- **40 injections, 40 caught, 0
survivors**, preflight 41/41, positive control GREEN, sentinel RED. Eight families: readfix 12,
blast 7, premise 5, grouping 4, shape 6, r5 3, mechanics 2, ids 1.

**THREE RUNS: 6 survivors, then 1, then 0.** The harness twice refused to run at all
(`HARNESS DEAD`) rather than mutate the wrong occurrence: two guards exist in both `check` and
`verify_post` and differ only by indentation, so a bare anchor matched twice. Of the survivors,
five were `verify_post` guards that no test drove -- `check` sees only the staged batch, so a post
state had to be doctored directly to reach them -- and one was a masked refusal: the
sanitation-present branch was unreachable because swapping the key for tillage trips the tillage
branch first, so it needed a test that DELETES the rung instead. The last survivor was fix 3, which
had only a POST-state assertion; that stays green with the guard disabled because the staged data is
already in the right order.
