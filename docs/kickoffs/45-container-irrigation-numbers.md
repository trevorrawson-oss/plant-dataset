# 45 - Container irrigation numbers: drip, emitters, and gallons by year

**Date:** 2026-07-29
**Origin:** Trevor, 2026-07-29 — *"one good thing for containers, especially for tree perennials, is
drip system and what nozzles/water amounts you use for the different stages of the tree."*
**Type:** an extension of `early_years` (kickoff 44), not a standalone column.
**BLOCKED ON TWO THINGS.** Read §3 before scoping. This cannot start until both clear.

---

## 0. Why this matters

Trevor names **container growing as the second standing complaint against competing apps**, after
thin perennial guidance. Kickoff 44 addresses the first. This addresses the second, for the hardest
case: a fruit tree in a pot, where getting water wrong is the usual reason it dies.

---

## 1. The gap, measured on canonical `b0d01f13`

The structure exists. The numbers do not.

| surface | state |
|---|---|
| `watering.schedule_by_stage` on fruit trees | **19/19** — present everywhere |
| what those entries actually say | `rate: "deep soak"`, `frequency: "1-2x per week"` |
| `watering.watering_method` | already `drip` on apple and others |
| `container_notes.watering_adjustment_*` | 120/121, but **prose only** |

Apple's container guidance today: *"check it every day when it is warm… water until water runs out
the holes in the bottom."* Good coaching. Useless for sizing a system. Nothing anywhere answers
**how many emitters, at what flow rate, for how long, at what age.**

**Existing base to audit, not a blank page:** 75/121 certified crops already carry *some*
gallons/GPH/inches-per-week number somewhere in `watering` or `container_notes`. Audit those first
— they were authored under varying discipline and some will not survive a source check.

Related container coverage, for the broader container arc later: the prose sub-fields are ~99%
filled and `container_ok` is 100% (107 yes / 14 no), so shape is not the gap. The thin spots are
`container_specific_pests` **3/121** and the pot-size numerics (`min_pot_gallons` 81%,
`recommended_pot_gallons` 78%, `depth_inches_min` 81%).

---

## 2. Why it rides `early_years` instead of being its own column

A tree's water demand is a function of **age and canopy size**. That is the exact axis `early_years`
already keys on. A newly planted container apple and a fourth-year bearing one want different
emitter counts on the same schedule.

Two parallel per-year structures would drift apart, and we already have a live instance of that
failure: register row 26 records that **no gate connects a per-cell `harvest_duration_weeks` to the
crop-level `harvest_ramp_weeks`**, so an override of `[30,40]` fires nothing. Do not create a second
one. Add an optional numeric block to the existing `early_years` entry rather than a new column.

Sketch, to be settled at scoping:

```jsonc
{ "year": 2,
  "note_beginner": "...", "note_seasoned": "...",
  "irrigation": {                     // optional; absent is the honest default
    "gallons_per_week": [min, max],   // the AGRONOMIC claim -> T1 only
    "emitters": 2, "emitter_gph": 1.0,// the PRODUCT arithmetic -> see the tier ruling
    "sources": [...] } }
```

---

## 3. THE TIER RULING, and the blocker it creates

Trevor: *"we can use trade content for the nozzles as a tier 2 source."* The intent is right and the
mechanics do not work today. Both problems are real and both are sequencing, not disagreement.

**Problem 1 — gate E denies every non-T1 citation, right now.**

```python
not_t1 = sorted(s for s in cited if s in cat and cat[s].get("tier") != "T1")
for s in not_t1: fail(f"source-tier: {s} tier={cat[s].get('tier')}")
```

Any T2 citation fails the gate outright. (The 9 current T2 entries are catalogued but effectively
unusable; the only two appearing in crops, `johnny_seeds` on zinnia and `harvest_to_table` on
beefsteak-tomato, sit in `sources_summary`, the never-rendered backend rollup gate E excludes —
verified 2026-07-29, not a live violation.)

**Problem 2 — under the PLANNED renumbering, trade content is T3, which is explicitly denied.**
`docs/2026-07-27-source-tier-model-kickoff.md` §3.1 defines the new bands as T1 peer-reviewed /
numbered extension, **T2 extension-PUBLISHED but not peer-reviewed**, T3 common practice, folklore,
**seed trade** → deny. An irrigation manufacturer is not extension-published, so it lands in T3.

### The resolution: separate the PLANT claim from the PRODUCT fact

These are different kinds of assertion and conflating them is what the tier model exists to prevent.

- **"This tree needs 12 to 18 gallons a week in July"** is an AGRONOMIC claim about a living thing.
  **T1 extension only, no exceptions.** Extension publishes exactly this, usually as gallons per
  week by canopy diameter or tree age.
- **"This emitter delivers 1.0 GPH"** is a PRODUCT SPECIFICATION. It is a verifiable fact about a
  manufactured object, not a claim about a plant, and the manufacturer is its most authoritative
  source. The grower-facing number ("two 1-GPH emitters, 90 minutes, twice a week") is then
  **arithmetic** on a T1 agronomic figure and a product spec.

**Proposal for the tier arc to rule on:** admit these as `source_class:
manufacturer_specification` at the new T2 band, with a written rule — *may back a product fact
only, never an agronomic one* — and a gate that enforces the split rather than trusting it. That
keeps trade content permanently unable to make a claim about a plant, which is the line this
dataset has held everywhere else.

### Consequence for sequencing

**This arc runs AFTER the source-tier renumbering**, which itself must land gate E's T2 acceptance
BEFORE any T1→T2 demotion (that kickoff's §3.1 sequencing hazard: demoting `unlv_mg_svn` while
gate E still denies non-T1 would instantly fail 67 crops). Order:

1. source-tier renumbering + gate E accepts T2 (its own arc)
2. `early_years` ships (kickoff 44)
3. this arc

If the tier arc slips, this one can still ship **T1-only**: extension gallons-per-week by age,
with emitter arithmetic omitted. That is a smaller but entirely honest product.

---

## 4. Traps

1. **The container-specific numbers will be thinner than the in-ground ones.** Extension publishes
   tree irrigation well; container emitter counts for a dwarf apple are much more often vendor
   content. Expect an honest-N/A branch from the start rather than backfilling plausible catalog
   figures — the exact shape of the artichoke chill-hours trap, where a widely-copied seed-company
   number was contradicted by the peer-reviewed trial.
2. **Do not let arithmetic launder a missing source.** If the gallons-per-week figure is not
   sourced, the emitter maths has nothing to stand on and the whole entry is fiction with units.
3. **Audit the 75 crops that already carry numbers before adding more.**
4. **Verify the renderer before shipping the data.** `annual_only` nearly deleted a note because
   `suitabilityDisplay` fails open; check what a missing `irrigation` block renders first.
