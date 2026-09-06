# The IPM ladder rollout -- batch playbook

**If you are a session picking this up cold, this file is the procedure. You do not need the chat
transcript it came from.**

Status as of 2026-08-24: canonical `c13ddea5`, catalog **50 methods**, **16 of 121** certified crops
laddered, **105 remaining (791 problems), ~21 batches of 5**. Run `python3 tools/ladder_batch.py
status` for the live figures rather than trusting this paragraph.

---

## 0. The one thing to understand before starting

Every gate in this repo checks **structure**. The two worst defects found while proving this process
both passed every gate and every mutation harness:

1. A generic consequence sentence that was **factually false on five of seven diseases** ("letting
   them slide shows up in the fruit" -- red stele and verticillium kill whole plants; fire blight
   kills wood).
2. `bottom_watering` **means** "water from below, in seed trays" and twelve authored rungs used it to
   mean "water at the base, outdoors". Different action. Same key.

Neither is findable by a gate. Both were found by reading. **The reading is not overhead on this
process; it is the process.** Everything else is arranged to make the reading affordable.

---

## 1. Prepare

```
python3 tools/ladder_batch.py status      # includes the family cut
python3 tools/ladder_batch.py families    # the family cut on its own
python3 tools/ladder_batch.py prepare --crops a,b,c,d,e --out /tmp/batchN
```

**GROUP BY FAMILY FIRST. Size is the second constraint, not the first.** Run
`python3 tools/ladder_batch.py families`. It reports **two different groupings, with two different
instructions.** Do not confuse them; they were one thing until 2026-08-24 and the conflation was
wrong.

- **TRUE TWINS** -- byte-identical problem prose, in order. This is the only group where you author
  ONE crop and propagate the ladders mechanically, with the promote asserting the copies are
  identical (`tools/promote_pla8_batch2.py`). The read is one problem set plus an equality check.
- **SHARED-NAME FAMILIES** -- the same problems by name, prose NOT identical. The read is still
  cheap, because the sourcing overlaps and the siblings compare side by side, but **every member
  needs its own authoring pass.** The percentage printed is the share of problem fields that match.

**WHY THIS SPLIT EXISTS.** The signature the tool grouped on was `sorted(problem_name(p))` --
problem NAMES ONLY. It never compared a character of prose, yet it printed "TWIN GROUPS ... one read
covers the group" and closed with "identical prose means the read is one problem set plus a
mechanical equality check on its siblings". Measured against canonical `c13ddea5`, **not one of the
ten reported twin groups was a true twin**: collards/kale shared 28.7% of their problem fields,
beefsteak/cherry-tomato 34.4%, the three cucumbers 72.2%.

**The corns of batch 2 are why nobody noticed.** They measured 96.2% with all twelve differences on
a single problem (Raccoons, which says "sweet corn" where the others say "corn", and carries the
same one-rung `exclusion_fencing` ladder on all four), so that shipped propagation was sound. The
group was selected for a reason that had nothing to do with prose and came out right anyway, so the
method read as proven. **A mechanical proxy standing in for reading is reproducible and wrong;
reproducibility is not validity.**

Applied to the cucumbers the same propagation would have been a content defect in both directions.
`pickling-cucumber`'s prose names wilt-tolerant varieties **such as County Fair** and asserts
**CMV-resistant** pickling varieties and resistant angular-leaf-spot varieties; `cucumber`'s and
`slicing-cucumber`'s name **non-bitter** varieties that attract fewer beetles and claim no
resistance at all. Copy either way and you erase a sourced control or invent one. Batch 3 was
authored three times instead.

The correction also finds propagate-safe SUBSETS the old cut could not: `dry-bean` +
`green-beans-bush` are true twins, while `pole-beans` diverges from both.

The earlier ordering was worse still. `status` used to recommend "fewest problems first", which
optimised batch SIZE and destroyed batch COHERENCE -- it is exactly what produced batch 1 as
heirloom-tomato + jalapeno + swiss-chard + basil + fig: five unrelated crops, 38 problems, and
**zero shared prose**, so five separate source sets had to be read from scratch.

Batching by family still makes the "fix one member of a template family, check its siblings" rule
automatic instead of something to remember -- the rule that was violated twice in one session when
`arugula`/`bok-choy` turned out byte-identical and an iron-phosphate safety claim spanned six crops.

Guards: `tools/test_ladder_batch.py` (9 tests), mutation-verified by
`tools/mutate_ladder_batch_suite.py` -- 8 injections, 8 caught, preflight 9/9, positive control
green, sentinel red.

**Size is still real**: ~38 problems -> ~143 rungs -> **~290 register strings** is readable in one
sitting; at ~470 reading becomes skimming, and `prepare` warns past ~400. But a family of 4
microgreens at 2 problems each is 8 problems, and a family of 3 cucumbers at 9 each is 27 -- both
well under the ceiling, so family and size rarely conflict. When they do, family wins and the batch
gets smaller. Note a shared-name family costs one authoring pass PER CROP, not one per group; only
a true twin collapses that.

`prepare` regenerates the brief FROM CANONICAL every time. Never reuse an old brief: batch 1 was
authored against a 37-method catalog that grew to 43 mid-batch, and a stale brief silently produces
ladders that omit controls the crop's own prose names.

---

## 2. Author -- one agent per crop, in parallel

Launch five agents at once. Substitute the crop slug and the batch dir. Roughly 5 minutes wall clock
and ~80k tokens per crop.

> TARGETED AUTHORING of IPM control ladders for ONE crop. Work only in the scratchpad; do NOT modify
> anything in /Users/trevorrawson/plant-dataset.
>
> CROP: `<slug>`
>
> INPUTS: read all three first.
> 1. `<BATCH>/<slug>_source.json` -- the crop's existing pests[]/diseases[] WITH their sourced prose
> 2. `<BATCH>/brief_catalog.md` -- the ONLY methods you may name, their tiers, what each one MEANS,
>    and the problem.type -> applies_to compatibility map
> 3. any already-certified ladder as a shape exemplar (apple's is the most complete)
>
> Per problem: mint a stable kebab `id`, set `type` (insect / mite / mollusk / fungal / bacterial /
> viral / physiological / nematode / vertebrate), and author an ORDERED `control_ladder`,
> least-invasive first. Rung shape:
> `{"method": "<catalog key>", "note_beginner": "...", "note_seasoned": "..."}`
>
> HARD RULES (a gate enforces each):
> - `method` MUST be a catalog key. Never invent one.
> - Rungs non-decreasing by tier: cultural < physical < biological < soft_chemical < conventional.
> - A method is legal only if its applies_to includes "any" OR overlaps the type's target set.
> - **Short ladders are CORRECT.** A cultural-only ladder is fine. NEVER pad a ladder to reach a
>   spray. Not every problem needs a chemical rung.
>
> CONTENT RULES, the most important instruction:
> - **RESTATE FROM THE CROP'S OWN PROSE.** Build every rung from what that entry already asserts.
>   Introduce no facts, numbers, thresholds or product claims that are not already there.
> - **CHECK WHAT THE METHOD MEANS, not just that it is legal.** The brief gives each method's
>   meaning. If the crop's advice is a different ACTION that merely sounds similar, do NOT use that
>   key; report it as a gap instead.
> - If the prose does not support a rung, do not author it. Fewer honest rungs beat a complete-looking
>   ladder.
> - Dual register, materially different: beginner plain/second-person/actionable, seasoned denser and
>   mechanism-aware. Never the same sentence reworded.
> - Gloss any technical term on FIRST USE in the beginner register ("frass, the sawdust-like
>   droppings"; "the microscopic worms in the soil called root-knot nematodes"). Seasoned may use it
>   bare.
> - No em dashes or en dashes. American English. `85°F` unspaced. Lowercase "plant" mid-sentence.
> - **No absolute claims** (always / never / completely / harmless / guaranteed). **If a source
>   hedges, KEEP the hedge** -- a dropped qualifier is a defect with no term to scan for.
> - Do not copy a sentence verbatim from the crop's prose.
>
> OUTPUT: valid JSON to `<BATCH>/out_<slug>.json`, SAME ORDER as the input arrays:
> `{"pests":[{"id","type","control_ladder"},...],"diseases":[...]}`
>
> Then report: problems handled, total rungs, **every ladder you deliberately kept short and why**,
> **every piece of crop advice you could NOT place in a rung and why**, any method key you used that
> is a loose fit for what the prose means, and anything in the existing prose that looks wrong or
> contradictory. Be specific about what you could not place rather than papering over it.

**Trust the bots' self-flags.** In batch 1 every single flagged "loose fit" turned out to be a
genuine method-meaning mismatch. Read the flagged ones first.

---

## 3. Merge and verify

```
python3 tools/ladder_batch.py merge  --out /tmp/batchN
python3 tools/ladder_batch.py verify --out /tmp/batchN
```

`merge` enforces the **id-stability rule** (CLAUDE.md): if a problem already has an `id`, the bot's
proposal is discarded and the existing one kept, because ids are join keys for
`varieties[].resistance` and `ladder_delta`. It prints any disagreement.

`verify` runs the real gates -- never a bot's own self-validation script -- plus copy hygiene, and
then prints the **method-meaning pairs** for you to read.

---

## 4. READ. This is the step that finds real defects.

In priority order:

1. **Every method-meaning pair `verify` prints.** For each: does the RUNG describe the ACTION the
   METHOD describes, or a different action that sounds similar? This is where `bottom_watering` was
   caught.
2. **Every "loose fit" and "could not place" the bots flagged.** ~30 per batch. 4 of 4 were real.
3. **Every rung on a problem whose prose you have not otherwise read**, checking the rung restates
   the crop's own assertions and invents nothing.
4. **Consequence and outcome clauses**, per problem: does the stated cost match this disease? A root
   rot kills plants; fire blight kills wood; a fruit rot shows in the fruit. One generic clause
   across several diseases is almost always wrong somewhere.
5. **Hedges**: where the source qualifies a claim, does the rung keep the qualifier?

Record what you CHECKED, not only what you fixed. That list is the denominator, and without it
"cleanup rode the arcs" reads as coverage it never had.

---

## 5. Promote

Copy the most recent batch promote as a template; they are deliberately near-identical:
`tools/promote_pla8_*.py` + its `test_promote_pla8_*.py` + its `mutate_pla8_*_suite.py`.

Non-negotiables, each of which exists because it was violated once:

- **One `serialize()`**, used by both the promote and the suite. A suite doing its own `json.dumps`
  grades itself, and an `indent=1` mutation survives.
- **`post` is the promote's OWN output**, replayed from `promote_fixture.pre_state(BASE_SHA)`. Never
  live canonical, or the suite reddens on every future promote.
- **Blast radius at LEAF level**, with `set(pre) == set(post)` compared BEFORE any value comparison.
  Iterating `pre` alone makes every addition invisible.
- **Mutation harness with an anchor PREFLIGHT** validating every anchor matches exactly once before
  grading. Anchors spanning Python implicit string concatenation match zero times; anchors matching
  twice edit a site you did not intend and report a catch for the wrong reason.
- **A guard that cannot fire in isolation is documented as a forward assertion and NOT counted as
  coverage.** Two exist already; copy that treatment rather than padding a total.
- **A cross-rung duplicate scan must compare a rung against OTHER rungs only.** Batch 12's compared
  each rung's `note_seasoned` against its own `note_beginner`, so a rung with identical registers
  was reported as a duplicate note and MASKED `validate_batch`'s identical-registers refusal, which
  says it in far clearer words. Found only because a driver asserted on the message it expected and
  got a different one: assert the message you mean, not merely that something refused.
- **If a later batch must chain through your promote, it needs `--canonical`.** `promote_fixture.
  _from_chain` rebuilds an uncommitted intermediate by invoking its producing script as
  `<script> --canonical PATH --expect-sha SHA --apply`. Most promotes in `tools/` accept a
  POSITIONAL canonical only and will die with "unrecognized arguments: --canonical". Add
  `ap.add_argument("--canonical", dest="canonical_flag", default=None)` and
  `a.canonical = a.canonical_flag or a.canonical`. Needed whenever a batch's base is another
  batch's output rather than a commit -- batch 12 on batch 11 (for a REUSED id that batch 11
  mints), and the trap-cropping mint/backfill pair.

Then the gauntlet, the state trio (`LATEST.txt`, `STATE_HISTORY.md` prepend, `CURRENT_STATE.md`
Current-SHA pointer -- and `test_gen_current_state.py` will catch you if you only do two of three),
`npm run build:guides` in plant-app to clear the E1 pre-commit check, commit, and register the new
SHA in `promote_fixture.COMMIT_FOR`.

### 5a. REQUIRED CLOSE STEP: re-measure the collision gate suite

`tools/test_problem_id_collision_gate.py` reads LIVE canonical and pins the canonical SHA plus the
gate's `raw` / `registered` / `actionable` counts and the pair list. **It reddens on every promote
by design.** It sat red through batches 26 and 27 because nothing in this playbook named the
re-measure as a step (PLA-461). So, at every close that moves canonical:

1. Run `python3 tools/problem_id_collision_gate.py` on the new canonical and record the three
   figures. Run `--show-registered` and diff the pair list against the previous state.
2. Re-measure the suite: `PINNED_SHA`, the three counts, and any pair the promote added, retired or
   registered. **Re-measure, never retune** -- a count edited to match a surprise is a guard turned
   off. The docstring on `test_audit_output_is_exactly_pinned` carries the running ledger; append
   the move there (what changed, why, which ticket).
3. Report the three figures in the Linear close-out as a named deliverable, not a note.

The standing assertion is that **a batch may add registered pairs and never open ones**, so
`actionable` holding is the pass condition for a ladder batch. When a promote is SUPPOSED to move
`actionable` (a merge or a split, PLA-450/451), **pin the predicted figures before the run** and
refuse on any other result; a number read off afterward is not evidence.

---

## 6. When the catalog is the problem, not the crop

If several bots independently report the same control blocked, that is the catalog, not the authors.
Batch 1 produced this on five unrelated crops in one afternoon and it was the most valuable output of
the pilot.

Before widening a method's `applies_to`, ask the question that was got wrong once:

> **Does the method's own PROSE describe the action this crop needs?**

`applies_to` governs what the gate ACCEPTS and does nothing to what a reader sees. Widening
`balance_nitrogen` to cover blossom-end rot would have put "the soft, sappy new growth that too much
nitrogen pushes out is exactly what aphids multiply on" onto a calcium-disorder ladder. **If the
prose does not fit, mint a new method instead of widening.** That is how `water_at_the_base`,
`moisture_buffering_mulch` and `avoid_ammoniacal_nitrogen` exist.

Every new method needs a real T1 document, fetched and READ. Do not mint one you cannot anchor:
`container_culture` is still owed precisely because UC IPM's nematode note turns out to say nothing
about containers, which was only discoverable by reading it.

---

## 7. Known-owed, carried forward

- `container_culture` (PLA-8's container ruling needs it; no anchor found yet),
  `certified_clean_stock` (stranded on 3+ crops), a generic pheromone/monitoring trap, trap cropping,
  diatomaceous earth.
- Refused deliberately, do not "finish the job" without re-arguing the biology: `even_watering`+insect,
  `even_watering`+nematode, `straw_mulch`+nematode, `airflow_spacing`+insect (all tolerance, not
  control) and `beneficial_predators`+viral (predators control the vector, not the virus).
- ~~**The coverage floor is NOT armed.**~~ **ARMED 2026-09-05**, at the arc's close, as
  `whole_crop_gate` **A57** (`control_ladder_gate.coverage_violations`). Coverage landed at 913 of
  913 problem entries, so the condition this row was waiting on is met and `gate_all` stayed
  121/121. **The unit is the problem ENTRY, not the crop** -- "every certified crop carries a
  ladder" would sit red at 121 of 128 forever, because the seven shells carry `pests: []` /
  `diseases: []` and hold nothing to ladder. Entry-scoped, they pass with no carve-out at any
  certification status. `[]` stays A56's defect ("laddered and left blank"); A57 owns absence only.
  Proof it fires: `tools/mutate_a57_coverage_floor.py` -- 7 injected / 7 caught, on both problem
  schemas, graded through `whole_crop_gate`, `gate_all` AND the pre-commit hook.
- Content defects found and NOT fixed: swiss-chard's slug prose calls iron-phosphate bait "safe
  around pets and wildlife" (unhedged absolute); basil's slug entry recommends tighter spacing while
  its downy-mildew entry recommends spacing for airflow (real contradiction, mildew is the
  higher-severity threat); fig's souring and endosepsis entries look like one problem split across
  `pests[]` and `diseases[]`.
- ~535 spaced `°F` instances roster-wide against 4,834 unspaced -- a real minority defect, worth its
  own sweep, not this arc's job.
