# PLA-8 BATCH 18 (acid citrus) -- HANDOFF: staged, read, dry-run green, NOT applied

**Written 2026-08-31 at the end of a long session. Read this before touching batch 18.**

Canonical is `2cde361b` (the `ant_exclusion` mint). Batch 18 is authored, merged, READ, and its
promote passes `--dry-run`. **Nothing is applied.** What remains is the mechanical half.

---

## 1. Where things actually stand

| item | state |
|---|---|
| batch 17 (stone fruit) | committed **and PUSHED** (`b196251`, `365898d`) |
| batch 17 TYPE_TARGETS fix | committed, **not pushed** (`b509928`) |
| `ant_exclusion` mint | committed, **not pushed** (`9e46e0a`, `715b735`) |
| batch 18 | **staged only.** `tools/staging/pla8_batch18_acid_citrus/` |
| canonical | `2cde361b`, working tree clean |
| unpushed | 3 commits |

`crops_data_final.json` sha256 must read `2cde361bb3b8571576f94637e65d86f557a44e7807d97b2a94c02eb7c3715198`.
If it does not, STOP and reconcile before doing anything else.

## 2. What is DONE for batch 18

* **Authored** by two agents (lemon 36 rungs, lime 42; 24 problems, 78 rungs total).
* **Merged** -- `python3 tools/ladder_batch.py merge --out tools/staging/pla8_batch18_acid_citrus`.
* **Verified** -- gate_all PASS, control_ladder_gate 0, register_completeness PASS, copy hygiene
  clean on all 156 new strings, 0 temperature figures, 0 ladder vocabulary.
* **READ.** All six `ant_exclusion` rungs read against the method's MEANS; the shared-id divergence
  map produced and adjudicated; the oil-temperature conflict ruled and applied.
* **Promote written** -- `tools/promote_pla8_batch18.py`, dry-run green, post SHA
  `514903dbaa59fa66d550fc88525d56dcdfe7150398f6f639e5b5905f1ddf85e4`.

## 3. What REMAINS, in order

1. `tools/test_promote_pla8_batch18.py` -- copy `test_promote_pla8_batch17.py` as the template.
2. `tools/mutate_pla8_batch18_suite.py` -- copy `mutate_pla8_batch17_suite.py`.
3. Run both. **Expect the harness to find guard branches with no driver** -- it did on both promotes
   built this session, three times on batch 17 and once on the mint, every time a branch nothing
   exercised rather than a wrong assertion.
4. `python3 tools/promote_pla8_batch18.py --apply`
5. Gauntlet: `gate_all`, `control_ladder_gate`, `register_completeness_gate`, `whole_crop_gate` on
   lemon and lime, `release_verify`.
6. State trio (LATEST.txt + STATE_HISTORY prepend + CURRENT_STATE Current-SHA line), then
   `test_gen_current_state.py`.
7. `npm run build:guides` in `~/plant-app` -- **the E1 pre-commit check in THIS repo blocks the
   commit until you do**, and re-run it AFTER the commit so the provenance stamp points at a
   commit that exists.
8. Commit, then register the new SHA in `promote_fixture.COMMIT_FOR`.

**Commit the state trio WITH the data.** The pre-commit roster-claim check reads `LATEST.txt` from
the INDEX, so canonical and its pointer must move in the same commit. Batch 16 split them across
three commits; that shape no longer passes.

## 4. Batch-18-specific guards already written, and why each exists

Do not treat these as boilerplate; each encodes a ruling made during the read.

* **`check_sooty_mold_is_laddered`** -- THE guard this batch exists for. `sooty-mold` shipped
  `control_ladder: null` on the previous base because a `fungal` type could name no insect method.
  If it is unladdered again, or loses its `ant_exclusion` rung, the mint accomplished nothing.
* **`check_ant_exclusion_precedes_predators`** -- the mechanism asserted on the data. The sources
  say exclude ants SO THAT natural enemies can work, so wherever both rungs appear the exclusion
  must come first.
* **`PERMITTED_DIVERGENCE`** -- `citrus-aphids` is the ONLY shared id whose ladders may differ, and
  only by the `ant_exclusion` rung. See section 5.
* **`check_no_temperature_figures`** -- see section 6.
* **`check_no_ladder_vocabulary`** -- carried from batch 17; here it also catches cross-problem
  pointers ("the same limits as the scale rung").
* **`EXPECTED_TYPE_UPGRADES`** -- citrus `type` is MIXED, unlike stone fruit. 21 of 24 problems
  already carry a fine type and must be PRESERVED EXACTLY; only 3 are coarse upgrades, pinned by
  name. (Roster-wide, unladdered problems are messier still: 129 carry no type at all.)

## 5. The shared-id divergence rule, settled this session

**A shared id MAY carry different ladders where the RECORDS differ. It may NOT carry different
SHAPES for the same asserted content.**

* `citrus-aphids` DIFFERS and that is allowed: lemon carries `ant_exclusion`, lime does not. Both
  aphid entries only OBSERVE ants, but lemon's own sooty mold entry says "Managing ants, which
  protect those insects, is part of the same fix" and names those insects as "aphids, scale,
  mealybugs, or whitefly". lime has no sooty mold entry, so that sentence exists nowhere in its
  record.
* `citrus-canker` was COLLAPSED: lemon used `prune_out_infection`, lime `garden_sanitation`, on
  sentences differing by one comma. `garden_sanitation` won because `prune_out_infection` means
  "taking the cut well beyond the visible margin, back into clean tissue" and implies a curative
  excision the entry explicitly denies ("There is no cure for an infected tree").
* Precedent both ways: batch 17's `brown-rot` spans six crops with 3 to 5 rungs (records differ);
  `plum-curculio` had to collapse (same content, three organizations).

## 6. OPEN adjudications, carried forward -- these are NOT done

1. **Oil temperature, 95°F vs 90°F.** The crops' scale entries say oil is unsafe above 95°F; the
   catalog's `horticultural_oil` caution says 90°F. Ruled for the RUNGS ONLY: no rung states a
   figure, so the method's caution carries it and the stricter number governs by construction.
   **This does NOT resolve the conflict.** The crops' 95°F still renders from their own
   `organic_treatment_*` fields, beside the 90°F caution, on the same page. Needs a real sourcing
   pass against the citrus documents.
2. **lemon's phytophthora entry contradicts itself on the mulch setback**: `prevention_seasoned`
   says "a foot", `prevention_beginner` says "a hand's width". Roughly 3x apart in one record.
3. **lime anthracnose's BEGINNER register carries a flat absolute** ("Persian limes are not
   affected") where its SEASONED register hedges ("appears to be immune"). The authored rungs keep
   the hedge in both registers, so the ladder and the existing beginner prose now disagree. The
   existing prose is the thing that should change.
4. **Phytophthora is typed `fungal` while its own prose says "water molds, not true fungi".** No
   oomycete type exists; `fungal` is the only bucket reaching `improve_drainage` and
   `resistant_rootstock`, so it is correct-by-necessity, but the record contradicts its own field.
5. **The mis-pointed-key defect**: lemon's mealybug and sooty-mold entries make ant claims citing
   only `ipm.ucanr.edu/PMG/GARDEN/FRUIT/citrus.html`, which was READ and is an INDEX PAGE with no
   ant content. Needs a repoint to `ucanr_ext_ants` / `ucanr_ext_sooty_mold`, both now in the
   catalog. Same class as plum's San Jose scale citing a mealy plum aphid page (batch 17).

## 7. The largest remaining CATALOG gap on citrus

**Nutrient supplementation has no method at all.** lemon's `iron-zinc-deficiency` ladder is a single
`even_watering` rung, and the entire actual treatment -- citrus micronutrient fertilizer, chelated
iron and zinc, EDDHA on high-pH soil, foliar micronutrient spray -- is unplaceable. Compounded by
`improve_drainage` being illegal on `physiological`. This is bigger than ant exclusion was; it
affects every physiological disorder on the roster, not just citrus.

Other gaps both citrus authors hit: quarantine/reporting requirements (no key), nursery-stock
inspection on insect types (`certified_clean_stock` is pathogen-scoped), "keep trees unstressed and
not dusty" on insect types (`even_watering` is mite/physiological only -- note the same advice IS
placeable on citrus-mites, which is an `applies_to` artifact rather than biology), and a generic
pheromone monitoring trap (only `codling_moth_pheromone_trap` exists).

## 8. Two lessons from this session that will save a new session time

* **IMPORT A GATE'S TABLE, NEVER RETYPE IT.** Two bugs in one session from re-implementing gate
  logic: the mint asserted its own idea of a valid source entry and shipped `name` without `title`
  (gate_all 121/121 FAILED until it called A54's own checker, which then immediately exposed that
  `title_violations` takes the catalog dict and not `data`); and both promotes hand-copied
  `TYPE_TARGETS` with `mite: {"mite"}` where the gate has `mite: {"mite", "insect_general"}`, which
  would have refused correct content. Both now import. Fixed in `b509928`.
* **A HANDED-OUT RULE BEATS A HANDED-OUT REGEX.** Twice, an authoring agent found instances my scan
  missed by applying the RULE instead of the pattern: cherry-sour found a sixth ladder-position
  claim in batch 17, and lime found a fourth oil cross-reference here that carried no figure and so
  slipped a figure-based scan. When briefing, give the rule and treat any pattern as a hint.

## 9. Roster position

Laddered **79 / 121** after batch 17. Batch 18 takes it to **81**. Remaining after that: ~7 batches
-- sweet citrus (grapefruit, mandarin-clementine, orange-navel, 32 problems), berries, woody herbs,
soft herbs, flowers, alliums, roots, other trees, and three stragglers (english-cucumber, edamame,
pumpkin). Microgreens stay LAST per the standing ruling.

Citrus was SPLIT on size: all five citrus measured 56 problems / **414 register strings**, past the
~400 threshold `prepare` warns at. Sweet citrus is the other half and is not yet prepared.
