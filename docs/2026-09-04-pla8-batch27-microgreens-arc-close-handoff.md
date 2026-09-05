# PLA-8 batch 27, the microgreens -- and the close of the arc

`ba61762a` -> `95e66f6d`. ONE promote, SEVEN crops: arugula-microgreens, broccoli-microgreens,
cilantro-microgreens, pea-shoots, radish-microgreens, sunflower-sprouts, wheatgrass.

**This closes PLA-8.** Nothing here is a next batch. Section 6 is the post-arc cleanup pass.

---

## 1. The arc-close arithmetic, stated explicitly

The completion test is **every problem entry laddered**, not every crop laddered. Both numbers are
computed from canonical, not asserted:

| figure | value |
|---|---|
| crops in roster | **128** |
| certified (`verified_gs_arc`) | **121** |
| certified crops with every problem laddered | **121** |
| shells (`pests: []` AND `diseases: []`) | **7** |
| **121 laddered + 7 shells** | **= 128** |
| problem entries on certified crops | **913** |
| problem entries carrying a ladder | **913** (was 899) |
| total rungs roster-wide | **3,637** (+43) |
| catalog methods | **64, UNCHANGED** |

The seven shells are `avocado`, `olive`, `oyster-mushroom`, `shiitake-mushroom`,
`lions-mane-mushroom`, `wine-cap-mushroom`, `button-mushroom`. Each carries `pests: []` and
`diseases: []` with `verification_status.status = None` -- present and empty by intent, per
CLAUDE.md. **They hold ZERO problem entries.** An instrument that counts laddered-versus-unladdered
by walking problem ids passes straight over them and will never report them as owed, which is
exactly why this arithmetic is written down rather than left to a tool. `doc_roster_claim_gate`
independently agrees: "128 crops, 121 certified, 7 shells (5 mushrooms + 2 named), 0 violations".

**`gate_all`: 121/121.**

---

## 2. What the batch actually changed

Purely additive. `id` + `type` + `control_ladder` onto 14 entries = **42 changed leaves**. Zero
prose edited, zero catalog change, zero top-level change. `release_verify` confirms exactly the
seven declared crops changed and the reference crop is byte-identical.

43 rungs, 85 register strings. Ladder shape: six crops carry gnats 2 / damping-off 4; cilantro
carries gnats **3**; sunflower's `airflow_spacing` rung is beginner-only, matching the precedent's.

**All 43 rungs are cultural or physical. No material rungs**, enforced as a safety refusal spec:
these crops are cut at cotyledon stage inside 7 to 28 days and eaten whole and raw (wheatgrass is
juiced raw), and no pre-harvest interval has been ruled for a crop on that timescale. Nothing in any
source or any crop's prose pushed toward a material rung; all seven authors independently reported
the prose asserting the opposite.

---

## 3. Zero ids minted, and the guard proved live BEFORE pinning

`fungus-gnats` and `damping-off` are both **REUSED**. `microgreens-mix` is laddered on this same
schema and carries both; `damping-off` is carried by 14 crops. `check_ids_are_reused` refuses any
pinned id that does not already exist outside the batch AND on the precedent crop.

PLA-449 ran **at id-pinning time, before fan-out, against POST-APPLY data**: **42 pairs -> 42, zero
introduced, zero removed.**

That zero is trustworthy only because the instrument was proved live on a DIFFERENCE first. A probe
stamped `damping-off-microgreens` / `fungus-gnats-microgreens` onto the seven:

| run | result |
|---|---|
| `DISPLAY_NAME_FIELDS = ("name", "name_seasoned", "name_beginner")` (the PLA-449 fallback) | **2 OPEN findings** -- FAMILY_MEMBER/NAME_SHARED and NAME_SHARED |
| narrowed to `("name",)` (pre-PLA-449) | **0 findings, both ids reported BLIND** |

`damping-off-microgreens` is edit distance **11** from `damping-off`, so check 1 never reaches it
either. The schema fallback is precisely what closes the hole, confirmed before pinning, not after.

---

## 4. The bundling rule was applied and ANSWERED, not waived

Four of the seven disease names bundle mold with damping-off. PLA-448 §4d and batch 26's pomegranate
precedent (an id-less bundle SPLITS rather than minting a new bundle) both pointed at a split.

**It does not split, because the documents refuse the distinction:**

* Penn State, *Growing Microgreens*: "Damping-off is the only disease or pest issue we have
  encountered", with a figure captioned "Damping-off possibly caused by *Rhizoctonia* or *Botrytis*
  species in a microgreens tray."
* Virginia Tech SPES-756: damping-off caused by *Pythium* or *Phytophthora*, plus mildews. The word
  "mold" does not appear in the publication.
* No readable .edu/.gov document attributes seed-mat fuzz to *Rhizopus*, *Mucor*, *Aspergillus* or
  *Penicillium*. The word "saprophytic" appears in none of them.

Minting a `surface-mold` id would have asserted an organism-level distinction the two most
authoritative sources contradict -- the shape of the rule pulling a fabricated entry out of the
batch. So: **one complex, one id.** The bundled NAMES are PLA-453 and were carried byte-for-byte.

Grey literature does list mold as its own management item (Purdue Extension; Missouri State's
"Diseases" slide carries separate "damping off" and "mold" bullets). That is what a future scope
ruling has to weigh. Recorded, not acted on.

---

## 5. Instrument liveness: the seven crops' pre-batch green was VACUOUS

Measured, not inferred. `control_ladder_gate`'s identity, type and `applies_to` checks all `continue`
on any problem whose `control_ladder` is `None` -- which all 14 of these entries were. So
`whole_crop_gate` reported PASS on all seven while checking nothing at all about their problems.

The same sabotage (`type: 'not-a-real-type'` on wheatgrass's disease entry), run against both states:

| state | result |
|---|---|
| pre-promote (`ba61762a`) | **GATE: PASS** -- the gate cannot see it |
| post-promote (`95e66f6d`) | **GATE: 1 VIOLATION** |

**Landing the ladders armed the gate on seven crops it could not previously see.** A shape gate
cannot notice absence unless absence is spelled out, and here absence was the entire population.

### The suite and its harness

Suite **53/53**. Harness **36 injected / 36 caught / 0 survived / 0 broken**, anchor preflight 36/36
matching exactly once, positive control green, sentinel reddened.

**The harness earned its keep on the first run**, with one survivor:
`copy/similarity_made_asymmetric`. `test_similarity_is_symmetric` had used a synthetic string pair
that was symmetric anyway, so deleting the both-orders `max()` changed nothing -- a vacuous test
reading as coverage. It is repinned on a real pair (arugula's and broccoli's fungus-gnat
`management_seasoned`) that difflib scores **0.288 one way and 0.828 the other**, and the test now
asserts that a one-order guard MISSES it while the correct guard catches it, so the mutation is
detectable by construction.

---

## 6. THE POST-ARC CLEANUP PASS -- this is what comes next

Ordered by consequence. Each row is a decision or a task, with its own evidence.

### 6a. Arm the coverage floor. This is the headline item and the arc unlocks it. **DONE 2026-09-05.**

> **CLOSED 2026-09-05 -- armed as `whole_crop_gate` A57.** Outcome, evidence and the two defects the
> arming turned up: `docs/2026-09-05-pla8-coverage-floor-armed.md`. In short: the floor is
> ENTRY-scoped (`control_ladder_gate.coverage_violations`), so the seven shells pass with no
> carve-out and the question this row left open -- may a crop certify carrying zero problems? --
> is answered YES, in the guard's tests, exactly where the correction below said it belonged.
> `gate_all` stayed 121/121; `tools/mutate_a57_coverage_floor.py` 7 injected / 7 caught, graded
> through `whole_crop_gate`, `gate_all` and the pre-commit hook. Row 6a-bis item 5 is also closed:
> `test_ladder_batch`'s 1 failure + 6 errors are repaired, not skipped.


`docs/ladder_batch_playbook.md` §7 states it exactly: "`control_ladder_gate`'s integrity half is
wired in as `whole_crop_gate` A56; the 'a certified crop must HAVE a ladder' floor is **deliberately
held back**, because arming it today takes `gate_all` from 121/121 to 7/121. **Arm it when coverage
lands.**" Coverage has now landed: 913/913. Arming it makes an unladdered problem un-certifiable and
ends the deferral. It is a new guard, so it ships mutation-tested per PLA-215.

**CORRECTION (2026-09-05), measured after this handoff was first written: NO SHELL CARVE-OUT IS
NEEDED.** An earlier draft of this section said the carve-out "must be explicit ... or the floor
takes the seven shells down." That is wrong. The seven shells carry
`verification_status.status = None`, so they are **not** `verified_gs_arc` and sit outside the
certified population a floor would run over -- `gate_all` runs `whole_crop_gate` on the 121
certified crops, and the shells are not among them. Measured on `95e66f6d`:

    certified: 121   shells: 7   fully laddered: 121
    shells that are CERTIFIED (would the floor see them?): NONE
    certified set == fully-laddered set: True
    certified crops lacking a ladder: NONE

So arming the floor is a **no-op on today's data by construction**: the set it would police is
exactly the set that already satisfies it. The real design question is not a carve-out but what
happens if a shell ever certifies while still carrying `pests: []` / `diseases: []` -- that is when
the floor has to decide whether "certified with zero problems" is legal. Worth answering in the
guard's tests rather than discovering later.

### 6a-bis. THE FULL-TREE REGRESSION: 5 failures + 6 errors, NONE attributable to this batch

`python3 -m pytest tools/` after the promote: **5,141 passed, 1 skipped, 5 failed, 6 errors**
(43 min). Every one was run down to a cause rather than counted. **Four predate batch 27 and one is
the arc finishing.** Zero are dataset defects.

| # | test | cause | batch 27's contribution |
|---|---|---|---|
| 1 | `test_bare_host_scan::test_self_pathed_population_at_this_canonical` | Pins `(315, 155)`. **Measures `(321, 161)` BOTH before and after this promote.** | **Zero.** 0 self-pathed rows on the seven crops before AND after. Already red at `ba61762a`. |
| 2 | `test_cited_claim_scan::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass` | `UnreportableAbsence: 8 of 28 cited URLs are uncached`, and the named URLs are ALLIUM ones (leek/shallot thrips, onion downy mildew, onion maggots). A URL-cache completeness problem. | **Zero.** Batch 27 added and removed **0** anchoring URLs (1,369 distinct before, 1,369 after, empty symmetric difference). |
| 3 | `test_problem_id_collision_gate::Preflight::test_canonical_is_the_pinned_sha` | `PINNED_SHA = ce98b0a6` (batch 25 + rosemary) while canonical was **already `ba61762a`** at HEAD. | **Zero.** Already red before this session began. |
| 4 | `test_problem_id_collision_gate::AuditFixture::test_audit_output_is_exactly_pinned` | Same stale pin. | **Zero.** |
| 5 | `test_ladder_batch::TheRosterHasRunOutOfTrueTwins::test_there_are_unladdered_crops_left_to_measure` **+ the 6 `BriefCarriesTheWholeMeaning` ERRORS** | **The arc is complete.** | This batch, by design. **FIXED 2026-09-05**, both on the class's own written instruction: the emptied reachability guard is retired and inverted into the arc-complete invariant (cross-walked against the A57 floor, because `laddered` is the weaker any-entry predicate), and the brief suite now builds its own unladdered scratch target instead of being skipped. 27/27. |

A first run of this regression overlapped the state-trio rewrite, which raised the possibility that
some failures were a mid-write race. **They were not**: a clean re-run after the trio settled
reproduced the identical five. Recorded because the wrong explanation was the more comfortable one.

**Read before acting: four predate this batch entirely, and the fifth is the arc completing.**

**(i) `test_problem_id_collision_gate.py` -- 2 failures, ALREADY RED BEFORE THIS BATCH.**
`PINNED_SHA = ce98b0a6`, which is batch 25 + the rosemary correction. Canonical was already
`ba61762a` at HEAD when this session started, so the pin was one full promote stale before batch 27
touched anything. Measured:

| | |
|---|---|
| `PINNED_SHA` in the suite | `ce98b0a6` |
| canonical BEFORE batch 27 | `ba61762a` |
| canonical AFTER batch 27 | `95e66f6d` |
| already red before batch 27 | **True** |

`test_canonical_is_the_pinned_sha` and `test_audit_output_is_exactly_pinned` both key off it. PLA-449
shipped on 2026-09-04 and its suite went stale on the very next promote (batch 26), which did not
re-pin it. **This is the pattern `promote_fixture` exists to end** -- a suite pinned to live
canonical rather than rebuilt from a committed base -- and PLA-449's audit fixture did not adopt it.
The fix is to move it onto `promote_fixture.pre_state` like the promote suites, not to keep
re-pinning a SHA after every promote.

**(ii) `test_ladder_batch.py` -- 1 failure + 6 errors, ALL ONE ROOT CAUSE: THE ARC IS COMPLETE.**
The suite was written assuming unladdered crops always exist. They no longer do.

* `TheRosterHasRunOutOfTrueTwins::test_there_are_unladdered_crops_left_to_measure` asserts
  `len(todo) > 0`. `todo` is now empty, permanently. The assertion is simply false from here on.
* The six `BriefCarriesTheWholeMeaning` ERRORS are `RuntimeError: generator raised StopIteration`,
  from `setUpClass`:
  `target = next(c["slug"] for c in d["crops"] if ...verified_gs_arc and not lb.laddered(c))`.
  With zero unladdered crops the `next()` has nothing to return.

Neither is a data defect and neither should be "fixed" by weakening an assertion. The decision is
what these tests should say now that the thing they measured is finished: retire the twin-hunt
class, or invert it to assert the arc stays complete; and point `BriefCarriesTheWholeMeaning` at any
certified crop, since the brief it checks is about the CATALOG and does not depend on which crop is
prepared. Both are small, but both change what a test means, so they are Trevor's call rather than
a mid-close edit. **Completing an arc breaks the arc's own tooling; that is expected, and it is
better surfaced loudly here than discovered as ambient red later.**

### 6b. Sourcing findings filed by this batch, not fixed by it

| # | finding | scope | evidence |
|---|---|---|---|
| 1 | The **root-hair-versus-mold diagnostic is unsourced**. Its only cited source, `psu_microgreens`, is silent on root hairs. It is sourceable at Purdue Extension and Missouri State, both grey literature. | radish-microgreens, sunflower-sprouts, wheatgrass | The claim sits in **BOTH** `management_seasoned` and `management_beginner`, so a fix touching one sentence leaves it live. Radish's beginner "usually harmless" is the same claim class again and would also survive such a fix. Highest consequence of the set: it tells a beginner a tray is safe to eat. |
| 2 | All seven **fungus-gnat entries cite only `uc_ipm` PN 7448**, a general pest note, while asserting crop-specific tray practice and cycle-length claims (arugula's "6 to 8 day cycle", broccoli's "8 to 12 days"). | 7 crops | The precedent `microgreens-mix` cites `psu_microgreens` + `unr_ext` for the same pest. Flagged independently by five of seven authors. |
| 3 | **`microgreens-mix` carries a `yellow_sticky_traps` rung its own prose never asserts.** | the precedent crop | A scan of all eight microgreens crops found cilantro is the ONLY one whose prose asserts traps. The precedent has an unprosed rung. |
| 4 | **`unr_ext`'s catalogued URL 302-redirects** to `naes.unr.edu/dfi/publication.aspx?PubID=3468`. | source catalog | The page is alive; the catalogued URL is stale. |
| 5 | **"Soil-borne fungi (Rhizoctonia, Botrytis, ...)"** overreaches. PSU's caption names those organisms but never calls them soil-borne, and *Botrytis* is conventionally airborne. | 4+ crops | The organism NAMING tracks the document; the "soil-borne" framing is the part that does not. Three authors flagged the organism list as wrong; reading the source showed the naming is right and the framing is the defect. |

### 6c. Four catalog gaps, each reported independently by multiple authors

Playbook §6: several authors reporting the same blocked control makes it the catalog's problem, not
the authors'.

1. **No tray / equipment sanitation method.** All seven leaned `garden_sanitation` past its written
   definition (end-of-season garden debris, pulling affected leaves) to mean washing trays and using
   fresh medium between indoor cycles. The precedent already does this. If a key is ever minted, all
   microgreens-family rungs using it should be repointed together.
2. **No pre-sow seed handling method.** pea-shoots' "drain the soaked seed well before sowing" and
   wheatgrass's "do not over-soak the seed" are both now unplaced.
3. **No method meaning "rinse the mat"** (wheatgrass) **or hull removal** (sunflower's un-shed seed
   hulls). `water_spray` is both illegal on a fungal type and a different action.
4. **No cultural airflow method legal on insects.** `airflow_spacing`+insect is a deliberate refusal
   (tolerance, not control), so every crop's "keep air moving" gnat advice survives only as prose
   inside a `bottom_watering` note, invisible to any method-key-level analysis. Also note
   `airflow_spacing`'s written meaning is layout and spacing, while every rung here is a fan.

### 6d. Open decisions carried in from earlier batches

* **Batch 26's four no-control entries** ship one honest anchored rung each and are still a decision
  for Trevor; the catalog has no tolerate-and-monitor method.
* **PLA-457** (sulfur/oil interval) is roster-wide and still awaiting a ruling. It did not touch this
  batch (no materials), and the held-guard passed as a refusal spec.
* **PLA-452** (the microgreens schema: `name_seasoned`/`name_beginner`, no `name`, on 8 crops) and
  **PLA-453** (the four-way damping-off naming variant set) were both explicitly out of scope here.
  This promote PINS the schema: if PLA-452 normalizes it, `check_pre_state_schema` refuses rather
  than mis-joining.
* **22 open collision pairs** on live canonical (the pre-existing set; this batch added none).
* Carried from batch 24: four one-token id repoints; `wet_foliage_discipline` missing from 13
  laddered problems; `beneficial_nematodes` owes a T1 read; the dropped-hedge inverse sweep never
  run; the 8 duplicate-id pairs / 39 name groups to adjudicate.
* **~535 spaced `°F` instances** roster-wide against 4,834 unspaced -- its own sweep.

### 6e. plant-app `npm run build:guides` -- the number, re-measured

The kickoff carried forward that the E1 bypass had been accumulating since batch 24. **That premise
is stale.** `export_staleness_gate` reports the shipped export is built from **`ce98b0a6`**:

* **ONE** dataset revision behind before this promote; **TWO** after it. Not the ~15 the records
  imply.
* `npm run build:guides` **did** run mid-arc, after the rosemary cert-log correction.
* Batch 24's "eleven dataset revisions behind" and `dfd8d85`'s "built from `c24d7754`" were both
  true when written and are both stale now.
* Four dataset commits since batch 24 carry a recorded `--no-verify: E1 app-provenance only`. This
  batch's commit will be the fifth.

---

## 7. Authoring notes worth keeping

**15 of 85 notes were rewritten after the copy guard fired.** Three were lifted from the
**precedent's own rung notes** -- `microgreens-mix` is a shape exemplar, not a donor -- and one was a
**0.776 similarity against TWO different precedent rungs with no shared six-word run at all**, the
multi-donor recombination a run-length check cannot see. That is why the guard runs a both-orders
ratio alongside the n-gram check. Every author's own self-check had come back clean, because each
compared only against its own crop's prose.

A narrow exemption was added for runs containing a **number**: "7 to 10 day grow-out" has no honest
paraphrase, and demanding one would be a guard refusing correct input. The exemption frees only runs
with a digit, so prose runs still fail.

**5 more notes were rewritten after the house-style guard caught internal machinery vocabulary
leaking into consumer prose**: "so the ladder stops at the cultural rungs by design", "this rung
earns more on cilantro", "this rung is doing more work than it would". A reader of the app has no
concept of a rung. (The regex is word-bounded, so "a sponge you have wrung out" is untouched --
verified, because one author asked.)

**Two divergences adjudicated on evidence, one kept and one cut:**

* **KEPT** -- cilantro's `yellow_sticky_traps`, which six other authors declined. Verified rather
  than accepted: cilantro's `management_seasoned` is the only prose in the family that asserts traps
  ("sticky cards help you catch a building population early"). The other apparent matches in a scan
  were "sticky-when-wet seed" and "traps moisture".
* **CUT** -- wheatgrass's `sound_sowing_practice` for "do not over-soak the seed", taking it 5 rungs
  to 4. The pea-shoots author read the same catalog entry and refused materially the same advice
  ("drain the soaked seed well") as unplaceable. Two authors reaching opposite conclusions on one
  question is exactly where a batch invents a difference with no source behind it, so both crops now
  refuse it and the gap is filed once, in 6c.
