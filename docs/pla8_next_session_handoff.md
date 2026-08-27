# PLA-8 -- handoff after the conventional-tier disclosure round (2026-08-26)

Run `python3 tools/ladder_batch.py status` for live figures rather than trusting any number here.
The procedure is `docs/ladder_batch_playbook.md`. Read it; this file covers only what changed.

Roster laddered **29 of 121**. Catalog **56 methods**. **No true twins left** -- every batch from
here costs one authoring pass per crop.

---

## THE NEXT TWO PIECES OF WORK, IN ORDER

> **UPDATE 2026-08-26 (evening): piece 1 is DONE.** The chemical-cohort round ran and promoted
> (`04b5aa69` -> `674fab25`, uncommitted pending Trevor): 4 methods changed (neem's invented
> low-bee rating fixed in THREE fields including a live strawberry rung; copper acute split
> named; soap's Moderate acute disclosed; hort oil's medium-band bee caution added), 3 verified
> byte-for-byte, harness 49/49 first run. **The catalog audit is DECLARED CLOSED.** Evidence:
> `docs/2026-08-26-pla8-chemical-cohort-closeout.md`. Next is the tomatoes (piece 2 below).

### 1. The chemical-cohort close-out round -- DONE (see update above; prep kept for the record)
`docs/2026-08-26-pla8-chemical-cohort-round-prep.md` has the whole thing: the seven methods, their
UC IPM uaiKeys, what to check on each, and which guard shapes to reuse.

Seven pilot-era (2026-07-22/23) chemical entries have never been re-read:
`copper_fungicide` `sulfur` `neem_oil` `spinosad` `insecticidal_soap` `horticultural_oil`
`iron_phosphate_slug_bait`

**This closes the catalog's safety-bearing surface.** Of 56 methods only 10 are a chemical a person
applies to food; three are now re-read and these are the other seven. After this round the catalog
audit is DECLARED CLOSED and batches run straight through, minting a method only when a batch
genuinely needs one (melons will need `mancozeb`, uaiKey=30 -- that is growth, not debt).

The instrument exists and is tested: `tools/ucipm_uaidb.py`, with `tools/test_ucipm_uaidb.py` as an
OFFLINE positive control against a cached page. **Run that control in the same pass as any reading.**

> **UPDATE 2026-08-26 (late evening): piece 2 is STAGED AND READ, not promoted.** 154 rungs
> across the 4 tomatoes sit in `tools/staging/pla8_batch7_tomatoes/` with the read done, two
> cross-sibling conflicts adjudicated, and ONE mint staged (`splash_barrier_mulch`, all four
> agents hit the same wall, UMN anchors read live). The promote waits on the chemical-cohort
> COMMIT so its suite can replay-pin from `674fab25`. Everything the promote session needs:
> `docs/2026-08-26-pla8-batch7-tomatoes-staging-read.md`.

### 2. Then the tomatoes
`beefsteak-tomato` `cherry-tomato` `grape-tomato` `roma-tomato` -- 4 crops, 34 problems. Highest
likely demand AND the best remaining family cut (grape+roma 68.1%), which will not always coincide.

---

## TREVOR'S ORDERING RULING, 2026-08-26: DEMAND BEATS READ-EFFICIENCY

> "the microgreens are last on my list as nobody has looked them on the website or asked about them"

The playbook batches by FAMILY because that makes the read cheap. That is now subordinate to what
people actually open. **Microgreens (7 crops / 14 problems) and Companion & Pollinator (10 / 65) go
LAST** -- 17 crops, about 18% of the remaining work, deferred. Peppers, leafy greens, roots and
brassicas move up. A cheap read of something nobody opens is still wasted.

Owed: a rough top-20 by page views would let the remaining 92 be ordered against real demand instead
of a guess. Ask for it.

---

## What landed this session

| commit | |
| -- | -- |
| `febf1af` | catalog **r7**: mint `biofungicide` + `weed_host_control`; a widening REFUSED after six T1 docs came back empty, and the refusal is itself a guard. |
| `603f4f8` | **THE TOOLING FIX.** `ladder_batch.cmd_prepare` emitted `best_use[:150]`, cutting the trailing "Distinct from X" clause that keeps two methods apart -- 37 of 55 fields ran past 150 chars, SIX lost the clause outright. And `cautions` reached the brief NOWHERE (41 strings, 29 of 55 methods). Brief 13.6KB -> 22.6KB. |
| `99a19c6` | r8: the powdery-mildew exception on `wet_foliage_discipline`. |
| `d925eb6` | **BATCH 6**: the two peas, 84 rungs, roster 27 -> 29. |
| `d096415` / `2e86279` | mint `chlorothalonil` + backfill 9 rungs onto 6 CERTIFIED crops. |
| (this round) | the conventional-tier disclosure round, below. |

**Never amend any of them** -- `promote_fixture.COMMIT_FOR` pins them.

---

## The conventional-tier disclosure round, and what it should teach the next one

**THE DEFECT WAS WRONG ADVICE, NOT A MISSING CAUTION.** Both conventional insecticides told readers
to "spray at dusk when bees are not foraging". That sunset-to-midnight allowance is UC IPM's MIDDLE
bee band. Carbaryl and all nine common pyrethroids sit in the STRICTEST band, which grants no time
window at all. Ten live rungs across apple, strawberry, asparagus and broccoli.

**A CLASS KEY HIDES INGREDIENT-LEVEL DISAGREEMENT.** `pyrethroid` covers nine ingredients whose
chronic ratings SPLIT four to five. `copper_fungicide` is the same shape and is in the next round.
Where a class key's members disagree, the caution names which.

**AN ABSENCE WAS DOCUMENT-SCOPED, AGAIN.** UC IPM lists no home-garden product for carbaryl, no Pest
Note mentions it, and it appears only as a professional product -- three signals from one
institution. NPIC overturns it nationally: 190+ registered products, "home gardens" named. Carbaryl
stays. A California shelf survey is not the world.

**AND ONE DEFECT WAS SIX HOURS OLD AND MINE.** "Bee rating II" on chlorothalonil was a numeral the
page does not carry; it renders three CSS bands and the four-numeral scheme lives in a footnote about
a different database. Caught by the very next pass over the same source, which is the argument for
re-reading a cohort rather than trusting recency.

### Guard lessons, and the one that cost two harness runs

1. **WRITE THE `VerifyPostIsDriven` CLASS FIRST.** Eight of twelve first-run survivors were
   `verify_post` guards with no driver: `check()` refuses every input that could reach them, so the
   whole post-state half sat untested while green. Fifth time this arc.
2. **A coverage assertion must not derive its expectation from the table it validates.** Emptying
   `DISCLOSURE_AXES` made the loop body never run AND the expected set empty, so the test passed
   having tested nothing. Freeze the axis list as a LITERAL in the test.
3. **A guard below a stronger neighbour is dead code.** The post-side split check sat under an
   exact-equality check that subsumed it. Made reachable rather than deleted.
4. **Order matters between two guards that fire on the same input.** A method with no bee caution
   trips both the band guard and the `bees` axis; the band message is the specific one, so the band
   check runs first and the test asserts THAT message.
5. **Token scans flag correct prose.** The authored caution said "materials one band softer carry a
   sunset to midnight exception; this one does not" -- correct, and refused, because the scan cannot
   read a negation. Simplify the prose, do not outsmart the guard.
6. **Piping a harness through `tail` masks its exit code.** The run reported exit 0 while printing
   FAIL. Redirect to a file instead.

---

## The `[:150]` defect had a SECOND instance, and it was in the checking tool

`603f4f8` fixed `cmd_prepare`, which builds the AUTHORING brief. It did not fix `cmd_verify`, which
builds the READ brief -- the pass that holds each shipped rung against what its method means -- and
that was still cutting `best_use` at **104** characters. Measured on `04b5aa69`: **53 of 56 methods
run past that cut and 13 lose their trailing "Distinct from <neighbour>" clause outright**,
including `off_season_tillage` and `planting_time_avoidance`, two of the methods this arc has
actually confused. **The tool that exists to catch method-meaning mismatches was comparing rungs
against truncated meanings.** Fixed, with `ReadBriefCarriesTheWholeMeaning` in
`tools/test_ladder_batch.py` (verified RED with the slice reintroduced, then GREEN).

**Generalize: when you fix a defect in one command, grep for the same shape in its siblings before
closing.** One fix, two commands, twelve hours apart, and the second one was found only by a
throwaway probe.

## Owed, and NOT done here

- **plant-app owes its `data(guides)` commit.** Regenerate `build:guides` AFTER this round lands;
  the WIP export sitting in that tree carries the OLD wrong bee cautions. The plant-app session was
  told this directly and is publishing its OTA from the clean committed tree instead.
- **`mancozeb`** (uaiKey=30, already read: water H, bees low, acute L, Prop 65 + EPA) is named with
  chlorothalonil on watermelon and cantaloupe. Mint it when the melons batch needs it.
- **Chlorothalonil sits inside `organic_treatment_seasoned`** on 11 problems -- a conventional
  synthetic in a field named `organic_`. Flagged by batch 3, still live, still not fixed.
- Existing-prose findings recorded but not fixed: the peas' unsourced timing claim; Pediobius
  credited to `clemson_hgic`; bush beans advised to clean stakes; the sulfur register interval
  disagreement.
