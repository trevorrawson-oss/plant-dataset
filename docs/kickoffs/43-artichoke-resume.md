# 43 - Artichoke GS #121: resume handoff

**To:** the artichoke session (paused 2026-07-27 mid-arc)
**From:** plant-dataset asparagus lane, 2026-07-28
**Dataset now:** `origin/main` **`c96e8df`**, canonical **`ea3636e7`**.
**You paused against canonical `34025ee3`.** That is **five content releases stale**.

---

## 0. Read this first, in this order

1. §1 -- your promote script will abort on sight, and your uncommitted work is at risk.
2. §4 -- the gate suite will report **4 findings on your staged cells that are NOT your bugs**.
   Do not edit your prose to appease them.
3. §2/§3 -- three new obligations artichoke picks up at cert.

Nothing about your cell layer has been invalidated. Your 39 cells were never written to the
canonical, and no asparagus work touched artichoke.

---

## 1. Two housekeeping things, both urgent

**Your `EXPECTED_SHA` is stale.** `tools/promote_artichoke.py:42` guards on
`34025ee3056d0173...`. The canonical has moved `34025ee3` -> `79862bc3` -> `0da1d234` ->
`9fe9e33e` -> `02fbb5e8` -> `a995333f` -> `27f14303` -> `ea3636e7`. Re-baseline to `ea3636e7`
(or whatever HEAD is when you run) and re-derive any pre-state assertions against the current
file. The guard working correctly means it will refuse to run, which is the good outcome.

**Your A48 is still uncommitted, and has been all through a long concurrent session.**
`tools/whole_crop_gate.py` carries it as an unstaged modification, alongside untracked
`perennial_harvest_gate.py`, `test_perennial_harvest_gate.py`, `carveout_dependency_audit.py`,
`promote_artichoke.py`, `tools/staging/artichoke/`, `tools/staging/shards/`. The asparagus lane
never staged any of them (explicit pathspecs throughout, verified after every commit), but a stray
`git checkout .` or `git clean -fdx` destroys A48, which is a working TDD-proven gate.

There is a second reason to land it early: because A48 lives only in the working tree, **every
gauntlet run this week exercised a stricter `whole_crop_gate` than the one at HEAD.** That turned
out harmless (a final review re-ran `whole_crop_gate` from git and asparagus still passed, and A48
is additive), but it means no recorded "gate PASS" was ever produced by committed code. Committing
A48 fixes that permanently. **Consider landing A48 as its own commit before you resume authoring.**

---

## 2. Artichoke now owes three things it did not owe when you paused

The asparagus arc shipped two new fields and a semantics ruling. Artichoke is the ONLY other
`herbaceous_perennial`, so the register deliberately routes both fields to you to author
**natively at cert** rather than as a later backfill column pass (the method doc's §2.5 branch;
column passes are forbidden mid-certification anyway, and you are the certification).

### 2a. `harvest_stop_rule` (crop-level, register **row 27**)

```jsonc
"harvest_stop_rule": {
  "signal": "<enum>",                  // the observable a grower watches
  "threshold_inches": [min, max],      // carry a RANGE where sources disagree
  "note_beginner": "...", "note_seasoned": "...",
  "sources": [...], "anchoring_urls": {...}
}
```

**`STOP_SIGNALS` in `tools/harvest_duration_gate.py` is currently a vocabulary of one
(`spear_diameter`), and artichoke almost certainly needs a second value.** Asparagus stops on spear
CALIBER; artichoke's stop signal is a bud-quality one (bracts beginning to open / loss of
tightness), which is a different observable, not a different threshold on the same one. Add the
enum value with the same TDD discipline the rest of the suite uses, and pick the name for what the
grower observes.

`threshold_inches` may legitimately be absent or shaped differently if artichoke's stop signal is
not a diameter. Do not force asparagus's shape onto it. If sources disagree on a number, carry the
range: that is this arc's standing rule, set when `harvest_ramp_weeks` year 2 was wrongly collapsed
to `[0,0]`, and applied again to the stop threshold (three T1 institutions publish 1/4, 3/8 and 1/2
inch for asparagus, so the field carries `[0.25, 0.5]`).

### 2b. `harvest_ramp_weeks` (crop-level, register **row 26**)

Ordered `[{bed_year, weeks: [min,max]}]`. Two hazards the row records, both learned expensively:

- **Year-counting conventions.** Sources use three incompatible ones ("year after planting crowns",
  "year the plants are in the garden", "harvest year") that all describe the same season. Ours counts
  **seasons in the ground**. Restate every sourced number into that convention before recording it.
- **Carry the range.** Asparagus year 2 shipped as `[0,0]`, collapsing a genuine UMN/Missouri vs
  MSU/UNH disagreement to its conservative end and presenting it as certainty in a brand-new field.
  A gate check now exists specifically for this: **RAMP-FIRST** requires the first `bed_year` whose
  `weeks` max is non-zero to **EQUAL the minimum** of `years_to_first_harvest`. Note that the
  register originally stated this check as "must fall INSIDE `years_to_first_harvest`" -- that
  formulation passes on the very defect it was written for, and was corrected.

Artichoke's dual-mode life (perennial in mild winters, grown as an ANNUAL in cold regions) makes
this interesting: a ramp is a perennial-crown concept. If the annual-mode regions have no meaningful
bed-age ramp, say so explicitly rather than authoring a fake one. Absence is a legitimate answer;
the honest-N/A branch is required by the column-arc template.

### 2c. Per-cell `harvest_duration_weeks` (sparse, row 26 amendment)

`[min, max]` on a region cell, **present only where a source states a regional duration**. Absence
inherits the crop ramp. Override-by-absence, matching the row-12 variety contract. On asparagus this
landed on exactly 2 of 12 checked cells; the other 10 correctly inherit, which is the honest outcome
of a real check, not a gap. Do not invent regional differentiation you cannot source.

---

## 3. One ruling that binds your cell layer

**`harvest` strings are month-granular TOUCH-SETS**, now a CLAUDE.md hard rule
(`docs/2026-07-27-harvest-window-semantics-ruling.md`). `"Jul - Oct"` means harvest occurs somewhere
within those months, not "July 1 to October 31". This was settled by reading the plant-astro and
plant-app renderers, both of which discard day numbers and paint whole touched months.

**With a constraint:** a painted month is a promise, so a month may be NAMED only if the cell's
sourced duration can REACH it. Under the mid-month convention, the 15th of the first named month
plus the duration's top end must land on or after the 1st of the last named month; explicit source
dates govern over that arithmetic. That is what REACH enforces.

---

## 4. The gate suite will report 4 findings on your staged cells. ALL FOUR ARE FALSE POSITIVES.

I ran the new checks against `tools/staging/artichoke/cells.py` (39 cells, 16 regions) before
writing this. Results: `zone_order` **0**, `ramp` **0**, `ramp_prose` **0**, `stop_rule` **0**, and
`duration` **4**. I read all four. **None is a defect in your data.** They are parser defects in
MY gate, which artichoke is the first crop to expose.

| cell | reported | why it is wrong |
|---|---|---|
| `northern_tier` z5 | REACH: 3 wk cannot reach October from mid-August | the "about three weeks" is the **seedling vernalization chill** ("seedlings chilled about three weeks near 40°F"), not a harvest duration |
| `northern_tier` z6 | END: note ends July, field ends October | the note says "pulls first harvest forward **into July** and lets picking **run into October**". The parser takes the FIRST `into <month>` match, which here is the START |
| `low_desert_az` z9 | END: note ends March, field ends June | "transplanting from mid January **through March**" is a **planting** window, read as a harvest end |
| `low_desert_az` z10 | END: note ends October, field ends June | "puts artichoke in from September **through October**" is again the **planting** window |

Two underlying defects, both mine:

1. **`harvest_clauses` splits only on `.` and `;`.** Artichoke's prose runs long comma-chained
   sentences that carry the planting window AND the harvest window in one "clause", so a planting
   month or a vernalization week-count gets attributed to harvest. Asparagus prose happens to use
   shorter sentences, which is why this never surfaced.
2. **`stated_end` returns the first `into|until|through <month>` match**, not the last, so a
   start-of-harvest phrase beats the actual end.

**DO NOT edit your prose to make these go quiet, and do not add per-crop exemptions.** Both would be
the "gate floods, so weaken the gate" trade this suite exists to refuse, and both would damage
genuinely good prose. **The asparagus lane owns this fix and is doing it.** Coordinate before you
run a promote so you are not gating against a parser that is mid-repair.

This is also a correction to a claim in the gate's own header: its "measured zero false flood
roster-wide" was measured when asparagus was the only crop with parseable prose. Artichoke is the
first real test, and the honest result is 4 false positives out of 39 cells.

---

## 5. What is already green for you

- **`zone_order_gate`** (archetype-scoped to `herbaceous_perennial`): **0** on your staged cells.
  You will be its SECOND member, which is also the trigger to hard-flip it from soft/standalone into
  the always-on suite. Worth doing at your cert.
- **A24/A34 carve-outs**: your own `carveout_dependency_audit.py` already proved they are no-ops for
  artichoke. Nothing in the asparagus work changed that.
- Your 39 cells all carry both `plant_out` and `harvest`, so A47 and your A48 are both satisfied.

---

## 6. Still to do on artichoke, per your own pause note

Cell layer is done and gate-clean. **Prose, IPM, and cultivars remain.** Resume via your
design-decisions Part C.

Two additions from the asparagus arc worth folding in while you author:

- **Region-level prose is a separate layer from cell ratings and NO GATE cross-checks them.** The
  asparagus arc reproduced that defect within an hour of documenting it, while watching for it.
  Hardening item 1 is a coherence gate for exactly this, and the recommendation is to build it
  **during** your arc rather than after, so your 39 cells are the first thing it checks instead of a
  fresh audit surface. Your call whether to take it on.
- **`category`**: register row 25 records that artichoke should move Fruiting Veg -> **Perennial
  Vegetables** at cert (the new value asparagus introduced, UC Master Gardener's classification).

---

## 7. Things NOT to worry about

- No asparagus change touched artichoke data, `source_catalog`, or any shared catalog.
- `signal` is already ruled into `register_completeness_gate`'s `EXCLUDED_KEYS`, so authoring
  `harvest_stop_rule` will not HALT that gate.
- `release_verify` §E does not flag `harvest_duration_weeks` as a novel region key (measured).
