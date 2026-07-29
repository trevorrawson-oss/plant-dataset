# 44 - `early_years`: the perennial establishment arc

**Date:** 2026-07-29
**Type:** cross-crop field addition. Run under `docs/gs_cross_crop_field_addition_v0.md` (the column
GS-arc method) and register it in `docs/field_addition_register.md` before authoring.
**Scope:** 26 certified perennials, **70 per-year entries, 140 dual-register strings.**
**Sequenced:** after the hardening pass and the citation cleanup arc. Not before.

---

## 0. This is a FIND, not a defect

The three-state perennial calendar (`establishing` / `first` / `full`) is new and it works. Building
it is what exposed a datapoint the dataset never had. Trevor's framing, and it is the right one:
perennial guidance being thin is a **standing complaint against competing apps**, so this is a
differentiator to build, not a hole to patch.

Nothing below is a criticism of the app. The app is doing the only honest thing available to it.

---

## 1. What is actually happening on screen

`plant-app`'s guide screen resolves three establishment states but branches the copy **two ways**
(`src/app/(tabs)/learn/[slug].tsx`):

```js
const establishmentCopy =
  establishmentState === 'full'
    ? firstSentence(registerNote(guide, 'harvest_ready', level))   // full bearing
    : establishmentTip && registerNote(establishmentTip, 'text', level);  // BOTH earlier states
```

So the **establishing** pill and the **first harvest** pill render identical prose. Apple shows its
blossom-pinching line on both. Blueberry and lime do the same. Pawpaw (`[4, 7]`) shows one sentence
for three consecutive years.

**Measured: 21 crops** where both early states are reachable.

Two things are NOT wrong and must not be "fixed":
- The **calendar tokens are correct**. `applyEstablishment` rewrites harvest months to
  `no_harvest_yet` vs `light_harvest` per state. Only the prose repeats.
- The app is not missing a field it could have read. **There is no field for the middle years.**
  `year_one_notes_*` covers year 1, `harvest_ready_*` covers full bearing, nothing covers between.

That absence is ours. This arc closes it.

---

## 2. The field

```jsonc
"early_years": [
  { "year": 1,
    "note_beginner": "...", "note_seasoned": "...",
    "sources": ["..."], "anchoring_urls": { ... },
    "education_ref": null }        // optional; null until the education section exists
]
```

**RULED (Trevor, 2026-07-29):**

1. **PER YEAR, not per named phase.** Per-phase ("formative pruning", "first thinning") is how the
   extension literature writes it and was considered, but the consumer surface is a year pill and a
   grower knows what year their tree is in, not what phase it is in.
2. **The key is `year`, NOT `bed_year`.** Most of these are trees. `harvest_ramp_weeks` keeps
   `bed_year` because it is herbaceous-perennial-only (asparagus, artichoke) where "bed" is
   literally correct. Two scopes, two words, each accurate. Do not unify them.
3. **The field is `early_years`**, chosen over `establishment_steps` for reading like something a
   person would say. It also implies an end: the period before full bearing.

**Ordered, sparse-tailed.** Entries run `year: 1` through `year: high - 1` where `high` is
`years_to_first_harvest[1]`, i.e. every year before the first that reads `full`. Apple `[2,5]` gets
4 entries; strawberry `[1,2]` gets 1; pawpaw `[4,7]` gets 6.

**Scope, measured on canonical `b0d01f13`:** the 26 certified perennials carrying
`years_to_first_harvest`. Distribution of entries per crop: 1×5 crops, 2×8, 3×6, 4×5, 5×1, 6×1.

**Explicitly OUT of scope:** the 5 woody herbs (lavender, oregano, rosemary, sage, thyme) carry
`year_one_notes` but NO `years_to_first_harvest`, so they have no establishment lag and the year
pills are meaningless for them. Do not author `early_years` there, and settle with the frontend
lanes that the pill row keys on `years_to_first_harvest` presence.

---

## 3. What each entry has to say

The content Trevor asked for is the **steps along the way**, not a restatement of "be patient":

> apple year 1: pinch off blossoms, water steadily, stake a dwarf
> apple year 2: prune to scaffold branches, still remove fruit
> apple year 3: allow a light crop, thin it hard
> apple year 4: normal bearing begins, switch to the mature routine

Each entry must earn its place by saying something the previous year did not. **An entry that
restates its predecessor is the defect this arc exists to remove**, and the gate below checks for
exactly that.

---

## 4. Pruning is a dependency, and it is half-built

Measured across 36 certified perennials:

| surface | coverage |
|---|---|
| `pruning_window` | 24/36 |
| `tips_by_stage.dormant_prune` | 18/36 |
| `tips_by_stage.formative_pruning` | **1/36** |

`formative_pruning` is *precisely* the establishment-year pruning concept and it exists on exactly
one crop. Establishment pruning (scaffold selection, central leader vs open centre) is a real,
T1-sourceable body of extension material and it is the single most valuable thing `early_years` can
carry for a tree.

**A pruning education section is owed.** `plant-app` already has an `education.json` surface to
hold it. `education_ref` on each entry is the hook, and it stays `null` until that section exists,
so this arc is NOT blocked on it. Do not inline a pruning tutorial into a year note.

---

## 5. Gate work

New gate, TDD RED before GREEN, adversarially injected on a scratch copy per CLAUDE.md.

- **SHAPE** — ordered, `year` a positive int, no duplicates, contiguous from 1, both registers
  non-empty, sources non-empty and T1-catalogued.
- **SPAN** — the last `year` equals `years_to_first_harvest[1] - 1`. A crop whose range widens
  later must gain entries; this is the coherence check that stops the field going stale the way
  region prose did.
- **NO-REPEAT** — consecutive entries must not be near-identical. This is the whole point of the
  arc; without it, the field can reproduce the current duplication in a new shape.
- **HONEST N/A** — absence is legitimate where no establishment guidance is sourceable, but it must
  be recorded in `open_findings`, never left as a silent gap. See §7.

Scope it to `years_to_first_harvest` presence, measure the flood before wiring, and ship SOFT with a
stated hard-flip trigger. Precedent: A47/A48/A49/A50/A51.

---

## 6. Consumer contract

The frontends decide how it looks; the dataset decides what is true. Both need to know it exists:

- **plant-app** — `establishmentCopy` currently branches two ways over three states. With
  `early_years` it should read the entry for the grower's actual `bedYear`, falling back to the
  nearest earlier entry. Note `suitabilityDisplay` fails OPEN, so verify what a missing entry
  renders BEFORE shipping the data ([[fail-open-renderer-hides-new-values]] — the trap that made
  `annual_only` a frontend-first change).
- **plant-astro** — the `Year 1 / Year 2 / established` panel row currently derives Year 2 from
  component microcopy precisely because no dataset field existed. That microcopy can retire.

---

## 7. Traps this arc will hit, from arcs that already hit them

1. **Do not invent a year's guidance to fill the shape.** 70 entries is 70 chances to write a
   plausible sentence with no source. The artichoke arc authored a whole three-year
   `harvest_ramp_weeks` ramp with every number invented and retracted it before promote. Ask per
   entry: *which document says this, for this crop, for this year?*
2. **Absence is an answer.** Some crops will not have four sourced distinct years. Author what is
   sourced, mark the rest N/A in `open_findings`, and do NOT pad.
3. **A gate finding is a hypothesis until read.** The region-prose gate produced 38 findings that
   were reported as real; exactly one was. Read a sample before reporting counts.
4. **Watch the year-counting convention.** Register row 26 records three incompatible ones in the
   establishment literature ("year after planting", "year in the garden", "harvest year"). Ours
   counts **years since planting, 1-based**, matching `bedYear()`. Restate every sourced number into
   it before recording.

---

## 8. Follow-on, not part of this arc

**Container irrigation numbers** ride this same per-year spine. See
`docs/kickoffs/45-container-irrigation-numbers.md`, which depends on this field existing AND on the
source-tier renumbering. Do not start it inside this arc.
