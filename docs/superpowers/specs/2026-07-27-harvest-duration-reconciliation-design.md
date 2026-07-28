# Harvest-duration reconciliation + `harvest_stop_rule` -- design (asparagus pilot)

**Date:** 2026-07-27
**Arc type:** cross-crop field addition. NEW **row 27** (`harvest_stop_rule`) + an **amendment to row
26** (`harvest_ramp_weeks`, whose scope note records the bed-age axis but never noticed the regional
one).
**Canonical at design:** `a995333f` (`main` `0b0165f`, committed, UNPUSHED).
**Scope decision:** asparagus-only **pilot**. Artichoke inherits the contract **natively at its
cert**, not by backfill.
**Origin:** surfaced by the harvest-duration pass
(`docs/2026-07-27-harvest-window-semantics-ruling.md`) when plant-app shipped a bed-age ramp line
rendered beside the per-cell calendar, making a latent three-layer contradiction visible on screen.
**North-star fit:** accuracy + honesty about limits. The stop rule is the single most-sourced,
most-portable datum in the asparagus literature, and it is the thing that makes every week-count
safe. [[trevor-north-star-accuracy-authority]]

---

## 1. The problem

Harvest duration is asserted in **three layers that disagree**, and nothing checks across them.

| layer | where | asparagus value |
|---|---|---|
| structured, bed-age axis | crop `harvest_ramp_weeks` | year 5+ = **8 to 10 weeks** |
| prose, crop level | `harvest_ready_beginner` / `_seasoned` | "on an established bed ... **about six to eight weeks**" |
| prose, regional | per-cell `notes` | **4-6** (Ozarks), **6** (z3), **8-10** (CA/NV), **10** (NM) |

The crop-level pair contradict each other *before region enters*: an "established bed" is year 5+,
where the ramp promises 8-10 and the prose promises 6-8. The regional layer then disagrees with both
in the cells where a source states a real regional duration.

**This is not a rendering bug.** It is the same defect class the 2026-07-27 duration pass closed one
layer down (field vs cell prose), reappearing between crop-level layers. The pass's own gate cannot
see it: `harvest_duration_gate` compares a cell's note to that cell's `harvest` band and never reads
`harvest_ramp_weeks` or `harvest_ready_*` at all.

**It is now user-visible.** plant-app's `src/lib/harvest-ramp.ts` (shipped 2026-07-27) renders
`rampLine()` -- literally *"Year 5. 8 to 10 weeks."* -- beside the zone calendar. An Ozarks grower
reads "8 to 10 weeks" next to cell prose sourced to MU G6405, which states April 14 to May 30 for
southern Missouri, about 6.5 weeks. Measured today: **2 cells** where the crop ramp overstates the
cell's own sourced duration (`mid_south` z7 at 4-6 weeks, `northern_tier` z3 at 6).

**And the rule that reconciles them is already in the dataset, unstructured.** Both registers of
`harvest_ready_*` carry it:

> *"stop when the new spears thin down to about pencil width"* (beginner)
> *"end the season when the majority thin to about pencil diameter, under 3/8 inch"* (seasoned)

Every source that says anything about ending the harvest converges on this signal, independently,
across eight states. It is what actually protects the crown, it is what makes the week counts safe,
and it works in every region without a start date -- including the 20 cells whose start is honestly
modeled rather than sourced
(`docs/2026-07-27-asparagus-harvest-start-sourcing-sweep.md` §3.2). It is not machine-readable and
not linked to any number.

---

## 2. The ruled model

**Bed-year x region, with the stop rule as governor** (Trevor, 2026-07-27). Rejected alternatives:
collapsing to one crop-level number (discards MU G6405's sourced Ozark dates -- real data thrown
away), and demoting all week counts to advisory (a calendar band still needs a number, so the app
would silently derive one, which is how the original artifact happened).

What a grower reads:

> **Ozarks, year 5:** "Cut for about 4 to 6 weeks in your area, or until spears thin to pencil
> width, whichever comes first."
> **California Delta, year 5:** "Cut for about 8 to 10 weeks, or until spears thin to pencil width,
> whichever comes first."

The regional clause appears only where a source states one. Everywhere else the crop ramp is the
default and the sentence is identical minus "in your area."

---

## 3. Field contracts

### 3.1 `harvest_stop_rule` -- crop-level, NEW (register row 27)

```jsonc
"harvest_stop_rule": {
  "signal": "spears thin to pencil diameter",   // the observable, source-unanimous
  "threshold_inches": [0.25, 0.5],              // RANGE: sources disagree on the number
  "note_beginner": "...",                       // dual-register consumer prose
  "note_seasoned": "...",
  // sources: exactly the documents confirmed by raw read to carry the rule.
  // `uada_ext` is confirmed; the rest of the set is settled during authoring (see below).
  "sources": ["uada_ext"],
  "anchoring_urls": { "uada_ext": { "url": "<FSA-6002>", "verified": "2026-07-27" } }
}
```

**`signal` leads, and `threshold_inches` carries a range, because that is what the sources support.**
The *signal* is unanimous (UADA states it three times verbatim: *"When the diameter of the spears is
less than the size of a pencil, cease harvesting"*; also MSU State, UGA C1026, UC MG, Sonoma). The
*number* is not: **NMSU H-227 = 1/4 in**, **our own current prose = under 3/8 in**, **UC MG Sonoma =
less than one-half inch**. Three T1 institutions, three thresholds. Per this arc's standing rule --
set when `harvest_ramp_weeks` year 2 was wrongly collapsed to `[0,0]` -- **where sources disagree the
data carries the range, it does not pick a side.** A point value here would be false precision in a
brand-new field, the exact error already made once on this crop.

**Sourcing discipline (tier C).** `harvest_ready_sources` today lists `umn_ext`, `msu_ext`, `mu_ext`,
`clemson_hgic`. The pencil rule was **not found** in the UMN text fetched raw this session, and the
MSU page returns an 83-character JS shell with zero asparagus content when fetched raw, so it cannot
be verified that way. `harvest_stop_rule.sources` cites **only documents confirmed to carry the
claim** -- `uada_ext` is confirmed by direct raw read; every other candidate must be re-read raw
before it is cited. This crop has produced five confirmed instances of a real T1 document cited for a
claim it does not make; this field will not add a sixth.

**Legitimately-N/A branch (required by the column-arc template).** Crops with no repeated-cutting
season have no stop rule: the field is absent, never a fabricated one. On the pilot the N/A case is
proven by the field being absent everywhere except asparagus.

### 3.2 `harvest_duration_weeks` -- per-cell, sparse override (amends register row 26)

```jsonc
// inside regions.<slug>.resolved_by_zone.<zone>
"harvest_duration_weeks": [4, 6]
```

- `[min, max]` integer weeks, the mature-bed duration **for that cell's geography**.
- **Present only where a source states a regional duration.** Absence inherits the crop-level ramp.
  Override-by-**absence**, matching the row-12 variety contract -- explicitly NOT a
  `{value, parent, changed}` diff, which stores drift-prone cached parents.
- **No new sources field.** The duration comes from a source already cited on the cell (MU G6405 on
  `mid_south` z7); the cell's existing `sources` / `anchoring_urls` carry it.
- **Do not invent differentiation.** A cell gets an override only where a document states a regional
  duration. Making cells *look* differentiated without a source is the failure this whole arc exists
  to prevent, and `nevada` z8/z9/z10 plus `ca_interior` z8/z9 are already honest-as-labeled
  identical values that must stay that way.

### 3.3 Repair `harvest_ready_beginner` / `_seasoned`

The flat "about six to eight weeks" is rewritten to be bed-year aware and to defer to the stop rule,
so the crop prose stops contradicting `harvest_ramp_weeks` year 5. Consumer-copy rules apply: no em
dashes, American English, "plant" lowercase.

---

## 4. The gate

**Extend `tools/harvest_duration_gate.py`; do not add a sixth gate.** Same defect class (a duration
claim that another layer contradicts), and extending keeps the existing 12 tests guarding while the
new checks land. The file is already soft/standalone and roster-wide with measured-zero flood.

New cross-layer checks, each firing only where the data gives it something to compare:

| check | rule |
|---|---|
| **RAMP-FIRST** | the first `bed_year` whose `weeks` max is non-zero must **equal the MINIMUM** of `years_to_first_harvest`. |
| **RAMP-PROSE** | where `harvest_ready_*` states a bare established-bed week count, it must equal the ramp's mature entry. |
| **OVERRIDE-REACH** (a design-time name; folded into `REACH` as shipped) | a cell's `harvest_duration_weeks` must be reachable within that cell's `harvest` band -- reuses the existing REACH machinery and the mid-month convention from the touch-set ruling. A structured override takes **precedence over the note parse** as REACH's input. **AS SHIPPED THE CODE EMITS NO DISTINCT `OVERRIDE-REACH` STRING:** `tools/harvest_duration_gate.py::duration_violations` selects `dur = tuple(ov) if has_ov else note_dur` and emits one `REACH` message either way, so override-driven reachability failures surface as `REACH`. The label names the input-precedence RULE, not an emitted verdict; the tests pin the emitted strings. |
| **OVERRIDE-PROSE** | where a cell carries both an override and a note-stated duration, they must agree. |
| **STOP-SHAPE** | `harvest_stop_rule`, where present, has a non-empty `signal`, a 2-element ascending `threshold_inches`, both registers, and at least one source. |

**RAMP-FIRST is "equals the minimum", not "falls inside the range", and the distinction is the whole
point.** Row 26 states the check loosely as "must fall inside `years_to_first_harvest`" -- **that
formulation would not have caught the defect it was written for.** With the historical year-2 `[0,0]`,
the first non-zero entry is year 3, and 3 *is* inside `[2,3]`, so a range-containment check passes on
the defect. The real error was that `years_to_first_harvest: [2,3]` encodes a genuine source
disagreement (UMN/Missouri permit a light second-spring cut; MSU/UNH say wait for year three), and
collapsing year 2 to `[0,0]` silently picked the year-three side. Requiring the first non-zero bed
year to equal the range's **minimum** forces the ramp to keep the door open in year 2, which is what
`[0, 2]` now honestly encodes. Under that rule the historical value goes RED (first non-zero 3 != min
2) and the corrected value goes GREEN (2 == 2).

**RAMP-PROSE compares ranges for equality, not overlap.** The live contradiction is prose `[6, 8]`
against ramp mature `[8, 10]`: those *overlap* at 8, so a disjointness test would miss it. They are
still two different claims about the same bed. Parsing reuses `stated_duration()`, already built and
test-pinned. After the §3.3 repair the shipped prose is bed-year aware and states no bare flat count,
so the check finds nothing to compare and stays silent -- which is the intended end state, not a
gap.

**TDD, RED before GREEN**, per CLAUDE.md: each check gets a test that fails first, plus adversarial
defect-injection into a scratch copy of the live canonical. Both REDs are **already verified against
real history**, not asserted:

- **RAMP-FIRST** goes RED on commit **`6f2b379`** (canonical `79862bc3`, the pilot before the
  `0c6c229` year-2 fix), where the ramp was `[{1,[0,0]},{2,[0,0]},{3,[2,3]},...]`: first non-zero bed
  year 3 != min(`years_to_first_harvest`) 2. Confirmed by running the arithmetic against that commit.
  The same value passes row 26's loose "falls inside" formulation, which is why §4 tightened it.
- **RAMP-PROSE** is RED on the **live** canonical: `stated_duration(harvest_ready_beginner)` returns
  `(6, 8)` against ramp mature `[8, 10]`. Confirmed by running the shipped parser.

Both git-pinned the way the duration gate's RED is pinned to commit `7870051`, so the proof outlives
this session.

**One honest parser limit, recorded rather than papered over.** `stated_duration` returns `None` for
`harvest_ready_seasoned`, whose "roughly six-to-eight-week spring window" hyphenates the compound
adjective and does not match the `N to M weeks` pattern. So RAMP-PROSE fires on the beginner register
only until the parser learns that form. Implementation should extend it and add the seasoned string
as a test case; if that proves noisy, the check stays beginner-only and the limit is documented in the
gate header. Either way it is a known gap, not an assumed win.

**Soft, and soft is a stage not a resting state.** Hard-flip into `whole_crop_gate` A39 when
artichoke certifies and the archetype has two members. Precedent: `control_ladder_gate`,
`variety_resistance_gate`, `zone_order_gate`.

---

## 5. Scope and sequencing

**Pilot = asparagus only.** The honest candidate set for both fields is the `herbaceous_perennial`
archetype, whose only current member is asparagus; artichoke is the only other. Row 26's own scope
note establishes this: the field means *weeks of repeated cutting a persistent crown can fund*, which
does not generalize to the 19 fruit trees, 4 woody berries, or 5 cut-as-needed woody herbs.

**No column pass runs in this arc, and that is deliberate.** `field_addition_register.md`'s standing
principle and CLAUDE.md both forbid column passes mid-certification, and artichoke (#121) is mid-cert
and paused. Because the archetype has exactly one other member, the correct branch is the method
doc's own **§2.5 fold-into-the-per-crop-checklist**, not a backfill sweep: artichoke authors both
fields at its cert and the treadmill never starts.

**Order of work:**

1. `harvest_stop_rule` contract + asparagus authoring (raw-read its sources first; cite only carriers).
2. `harvest_duration_weeks` overrides on the cells whose sources state a regional duration.
3. `harvest_ready_*` prose repair.
4. Gate extension, TDD, driven to 0.
5. Register row 27 + row 26 amendment.
6. Gauntlet, state trio, Trevor approves the commit.

**Definition of done, same standard as the pass that produced this arc:** a check that returns zero,
not fields that look filled.

---

## 6. Consumer impact

**plant-app** (`src/lib/harvest-ramp.ts`, shipped today) reads `harvest_ramp_weeks` and renders
`rampLine()`. Once cell overrides exist it can prefer the cell value and fall back to the crop ramp,
and it can append the stop-rule clause. Both fields must be read **gracefully** -- present-or-omitted,
never fabricated -- per the column-arc template §4, so nothing breaks before the app wires them.

**Note the app's guides.json is currently stale** (synced at plant-dataset `0c6c229`, three content
releases back) and still carries the `ca_desert` z9 defect. `npm run build:guides` reads this
checkout directly.

**INV-2 (standing):** do not consume these as load-bearing until the crop is gate-clean.

---

## 7. Risks

- **Fabricating regional differentiation.** Mitigated by the source-stated-only rule in §3.2 and by
  the override being sparse; a cell with no sourced duration keeps inheriting.
- **Citing a document that does not carry the stop rule.** Mitigated by the tier-C discipline in
  §3.1: raw-read every candidate, cite only confirmed carriers. Five prior instances on this crop.
- **False precision on the threshold.** Mitigated by carrying the range.
- **Scope creep into a column pass.** Mitigated by §5: asparagus only, artichoke at cert.
