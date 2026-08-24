# The IPM ladder rollout -- batch playbook

**If you are a session picking this up cold, this file is the procedure. You do not need the chat
transcript it came from.**

Status as of 2026-08-23: canonical `75b3c0f0`, catalog **43 methods**, **7 of 121** certified crops
laddered, **114 remaining (861 problems), ~23 batches of 5**. Run `python3 tools/ladder_batch.py
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
`python3 tools/ladder_batch.py families` and take a TWIN GROUP off the top.

This is a correction, made 2026-08-24 after batch 1. `status` used to recommend "fewest problems
first", which optimised batch SIZE and destroyed batch COHERENCE -- it is exactly what produced
batch 1 as heirloom-tomato + jalapeno + swiss-chard + basil + fig: five unrelated crops, 38
problems, and **zero shared prose**, so five separate source sets had to be read from scratch.
Measured across the 114 remaining crops, **295 of 861 problem-instances (34%) are BYTE-IDENTICAL to
a problem on another unladdered crop**, and 11 twin groups cover 32 crops. Distinct problems left
to read: ~540, against 861 instances.

A twin group collapses the expensive step: you read ONE problem set and then verify its siblings are
byte-identical, which is mechanical. It also makes the "fix one member of a template family, check
its siblings" rule automatic instead of something to remember -- the rule that was violated twice in
one session when `arugula`/`bok-choy` turned out byte-identical and an iron-phosphate safety claim
spanned six crops.

**Size is still real**: ~38 problems -> ~143 rungs -> **~290 register strings** is readable in one
sitting; at ~470 reading becomes skimming, and `prepare` warns past ~400. But a twin group of 7
microgreens at 2 problems each is 14 problems, and a twin group of 3 cucumbers at 9 each is 27 --
both well under the ceiling, so family and size rarely conflict. When they do, family wins and the
batch gets smaller.

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

Then the gauntlet, the state trio (`LATEST.txt`, `STATE_HISTORY.md` prepend, `CURRENT_STATE.md`
Current-SHA pointer -- and `test_gen_current_state.py` will catch you if you only do two of three),
`npm run build:guides` in plant-app to clear the E1 pre-commit check, commit, and register the new
SHA in `promote_fixture.COMMIT_FOR`.

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
- **The coverage floor is NOT armed.** `control_ladder_gate`'s integrity half is wired in as
  `whole_crop_gate` A56; the "a certified crop must HAVE a ladder" floor is deliberately held back,
  because arming it today takes `gate_all` from 121/121 to 7/121. Arm it when coverage lands.
- Content defects found and NOT fixed: swiss-chard's slug prose calls iron-phosphate bait "safe
  around pets and wildlife" (unhedged absolute); basil's slug entry recommends tighter spacing while
  its downy-mildew entry recommends spacing for airflow (real contradiction, mildew is the
  higher-severity threat); fig's souring and endosepsis entries look like one problem split across
  `pests[]` and `diseases[]`.
- ~535 spaced `°F` instances roster-wide against 4,834 unspaced -- a real minority defect, worth its
  own sweep, not this arc's job.
