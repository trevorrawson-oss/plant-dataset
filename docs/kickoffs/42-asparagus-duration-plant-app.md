# 42 - Asparagus harvest-duration arc: plant-app handoff

**To:** the plant-app session (TestFlight build)
**From:** plant-dataset, 2026-07-28
**Dataset state:** `origin/main` **`65820b3`**, canonical **`27f14303c3c77e7ca34313bf137173bc3a83e76ff2626578916ddd40336c2a79`**, pushed.
**Action required from you:** `npm run build:guides`, then read §3 before you cut the build.

---

## 1. What you actually need to do

```bash
cd ~/plant-app
npm run build:guides      # reads ~/plant-dataset/crops_data_final.json directly
npm test
```

`scripts/build-guides-data.mjs` reads the plant-dataset working tree, which is now at the pushed
canonical, so a plain rebuild picks everything up. Your bundled `src/data/guides.json` was last
synced at plant-dataset `0c6c229` and is **four content releases behind**.

**Nothing in this arc breaks the app.** Verified against your code, not assumed:

- Two NEW fields ship (`harvest_stop_rule` crop-level, `harvest_duration_weeks` per-cell). Neither
  is read anywhere in `src`. `Guide` (`src/lib/guides.ts:20-110`) ends in an index signature
  `[k: string]: unknown` and the data is loaded via `data as unknown as Guide[]` (line 116), so
  unknown fields are harmlessly ignored. There is no ajv/zod/JSON-schema validation anywhere.
- `harvest_ready_sources` changed contents. It has **zero consumers** in `src`.
- `harvest_ready_anchoring_urls` lost its `msu_ext` key on asparagus. Its only consumer,
  `src/lib/herb/allowlist.ts:32`, iterates `Object.values()` with no key or index assumptions.
  **`src/lib/herb/allowlist.test.ts:20-25` still passes**: it asserts `EXTENSION_ALLOWLIST`
  contains `canr.msu.edu`, and five other crops (cayenne-pepper, habanero, chives, cherry-sour,
  celery) still cite that host in their own `harvest_ready_anchoring_urls`.

---

## 2. What changed that you DO render

**`harvest_ramp_weeks` year 5 widened `[8,10]` -> `[6,10]`.** Your `rampLine()`
(`src/lib/harvest-ramp.ts:58-63`) will now render **"Year 5. 6 to 10 weeks."** where it previously
said "Year 5. 8 to 10 weeks." Same for year 4, unchanged at `[6,8]`.

Why: the mature-bed figure is not one number. Across eight T1 documents it spans roughly five to
ten weeks (UMN 6-8, UGA C1026 6-8, MSU "up to 8", USU "up to 8", Illinois 8-10, UC ANR 7234 8-10,
UC MG statewide "6 to 10", NMSU max 10). `[8,10]` had collapsed that to its upper end. `[6,10]` is
the range actually carried, and UC Master Gardener statewide publishes that exact span verbatim.

**`harvest_ready_beginner` / `harvest_ready_seasoned` were rewritten.** You render these at
`src/lib/guide-chapters.ts:215` -> `GuideChapters.tsx:101` ("When to pick"), and the first sentence
becomes the "Full harvest" pill caption via `[slug].tsx:344`. They are now **bed-year aware** and
defer to the stop rule instead of stating a flat week count. Re-read the pill caption after the
rebuild: `firstSentence()` is now taking the first sentence of different prose than before.

**Four asparagus zone bands moved** (from the earlier duration pass, also in this sync):
`mid_south` z7 `Apr - Jun` -> `Apr - May`, `northern_tier` z7 `Apr - Jun` -> `Apr - May`,
`northern_tier` z5 `Apr - Jun` -> `May - Jun`, `utah_dixie` z8 `Mar - May` -> `Mar - Apr`, each with
its calendar token moved to match. Plus `ca_desert` z9 `Feb - Apr` -> `Mar - May` with `plant_out`
`Feb 1 - Apr 30` -> `Jan 1 - Mar 1`, which fixes a real defect your bundle still carries: the cooler
desert zone claimed harvest a month EARLIER than the warmer valley floor.

---

## 3. READ THIS BEFORE CUTTING THE BUILD

**Seven crop-level asparagus strings you render still carry the superseded "six to eight weeks"
figure.** They are stale, not wrong (6-8 sits inside the new 6-10), and none of them is a crash. But
they sit on the SAME SCREEN as the ramp line, so a tester scrolling the asparagus guide can see
"Year 5. 6 to 10 weeks." in the phase ribbon and "six to eight weeks" in the body copy.

| field | your render site |
|---|---|
| `description_beginner` / `description_seasoned` | `[slug].tsx:270,697` - guide body copy |
| `growth_stages[1].user_action_beginner` / `_seasoned` | `GrowingJourney.tsx:75-79` "Do this"; also Garden tab `RightNowBlock.tsx:18,28` |
| `tips_by_stage.spear_emergence[0].text_beginner` / `_seasoned` | `GrowingJourney.tsx:95-100` tip callout |
| `watering.schedule_by_stage[1].note_seasoned` | `GrowingJourney.tsx:87-92` "Water"; also `RightNowBlock.tsx:19,29` |

Two more stale strings exist but you do NOT render them, so they cost you nothing:
`notifications[1].body_seasoned` (no code reads `guide.notifications`) and `year_one_notes_seasoned`
(zero references in `src`).

**This is a judgment call, not a blocker.** Options:

1. **Ship now.** The inconsistency is narrow-vs-wide, not right-vs-wrong, and only asparagus shows
   the ramp line at all. Nothing else on the roster is affected.
2. **Ask plant-dataset for the prose pass first.** It is bounded: seven strings, one crop, and the
   gate + promote machinery is already in place. It is registered as owed work in
   `docs/field_addition_register.md` rows 26/27 and in the state trio.

If you ship now, please note the inconsistency in the TestFlight notes so a tester reporting it is
not treated as a new bug.

---

## 4. What was wrapped, for context

Asparagus's harvest data is now internally coherent and mechanically enforced. Duration used to be
asserted in three layers that disagreed (the crop-level structured ramp, the crop-level prose, and
per-cell regional prose), and nothing checked across them.

- **Ruled and written into CLAUDE.md:** `harvest` strings are month-granular TOUCH-SETS, not
  day-precise spans. Decided by reading YOUR renderer and plant-astro's, not by preference:
  `succession.ts` `monthFromString` discards day numbers. A month may be named only if the cell's
  sourced duration can reach it.
- **New `harvest_stop_rule`** (crop-level): the pencil-diameter signal every source converges on,
  with `threshold_inches: [0.25, 0.5]` carried as a RANGE because three T1 institutions publish
  three different numbers (NMSU 1/4, MU G6405 3/8, UC MG Marin 1/2) while the signal is unanimous.
  Dual-register prose included. **Nothing renders it yet** - it is a candidate for the "or until
  spears thin to pencil width, whichever comes first" clause beside your ramp line.
- **New per-cell `harvest_duration_weeks`**, sparse: present only where a source states a regional
  duration. Exactly two cells today, `mid_south` z7 `[4,8]` and `utah_dixie` z8 `[6,8]`. Ten of
  twelve candidates correctly got NO override because no cited source states one. If you ever wire
  it: prefer the cell value, fall back to the crop ramp.
- **`tools/harvest_duration_gate.py`** now runs seven checks, 31 tests, with its RED git-pinned so
  the proof survives the session. Gauntlet green: `gate_all` 120/120, `release_verify` CLEAN.

Citation fidelity was independently verified at 35/35 quotes re-fetched raw and matched verbatim.

---

## 5. Still owed, on our side, not blocking you

- The seven-string prose pass in §3.
- No gate connects a per-cell override to the crop ramp (an injected `[30,40]` fired nothing).
- `harvest` string vs `calendar` token is ungated for the `herbaceous_perennial` archetype
  (A34/A37 are carved out), so band repairs are unverified paired edits.
- Citation cleanup arc, now with named instances: `msu_ext` is cited on five asparagus cells and is
  an 85-character JavaScript shell; six anchoring URLs point at extension portal roots with zero
  asparagus content.
- `se_gulf` z8 wants a `uga_c1026` catalog row so its stated duration can be honestly sourced.

**Unrelated but still open from before:** plant-astro's `PlantingCalendarCard` still mis-renders
asparagus zone rows (plant and harvest simultaneously, a "too late" summer). That is a website bug
with a written spec, owned by the astro lane, and it is why `plant-astro` `origin/main` is
deliberately still pinned to `7923579`. It does not affect this app.
