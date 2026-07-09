# second_planting de-multiplexing migration -- design

**Date:** 2026-07-09
**Author:** Claude Code (kickoff #18 executing session)
**Status:** Approved design (Trevor, 2026-07-09: Decision A + edge rulings + Decisions B-E + approach all confirmed individually). Implementation plan next.
**Kickoff:** `docs/kickoffs/18-second-planting-demux-migration.md`
**Reads against:** `docs/2026-07-08-second-planting-demux-findings.md`; `docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md` (the second_planting model + Phase C read-layer flip); `tools/whole_crop_gate.py` (SECOND_PLANTING_KEYS, A-numbering); `tools/apply_patch.py`.
**Start SHA:** `1372c29991c03bd5b28d154003408d8c2cf1bf2c3ad2ac6b3cb41b3f5575952a` (== LATEST.txt at design time; every batch re-gates against the then-current LATEST).

---

## 1. Mission

Finish the partially-rolled-out `second_planting` split: a two-season cell's top-level
window fields carry the PRIMARY (spring) window only, with the fall planting in a
structured `second_planting{}` object -- as an EXTRACT-then-clean migration, never a
strip -- then gate the old comma-string shape out of existence so new crops are
authored correctly from the start. Runs BEFORE the new-crop work for that reason.

## 2. Rulings (Trevor, 2026-07-09 -- all resolved before design)

| # | Ruling |
|---|---|
| A | **suitable=true cells are EXEMPT** (297 cells / 38 crops). Two windows there are one continuous cool-season sow cadence; SuccessionCard renders them as a rhythm. Their multi-window top-level is the legitimate full sow window. |
| A-edge1 | **Woody herbs are EXEMPT** (59 cells / 5 crops: lavender, oregano, rosemary, sage, thyme). Their `"Oct - Nov or Feb - Mar"` is two alternative establishment windows for ONE perennial planting. The gate treats `" or "`-joined windows as one planting choice. |
| A-edge2 | **chives + mint are EXEMPT** (4 cells). Harvest-only doubling = two harvest flushes of one established perennial around a summer pause. No planting event; no second_planting. |
| B-reflush | **REFLUSH cells are EXEMPT** (8 cells: cayenne 4, habanero 3, jalapeno 1). One spring planting, harvest string doubled: the same plant pauses fruit set in summer heat (matches their `poor_fruit_set` heat_effect) and sets again in fall. Harvest-only doubling with single planting fields is a legitimate shape. |
| B-alt | **ALT_WINDOW cells get OR-NORMALIZED, not migrated** (11 cells: onion 4, shallot 2, swiss-chard 5). Two planting windows converging on ONE harvest ("plant sets in fall OR late winter") are alternatives, not a discrete second crop. Comma becomes `" or "`, matching the woody-herb precedent. onion `ca_interior` `start_indoors: "Sep, Dec"` -> `"Sep or Dec"` likewise. |
| B-fix | **onion `ca_north_coast` z9/z10 continuity fix:** `plant_out "Nov - Jan, Jan - March"` -> `"Nov - March"`. The chunks overlap at Jan and the cell's own zone_notes say "plant November through March". Logged as a zone_notes-backed correction inside the batch. |
| B-order | Primary = first comma-span. **Verified on all TWO_CROP cells: spans are date-ordered spring-first**, no 3+-window fields. (The only fall-first fields in the roster are ALT_WINDOW cells, which are not extracted.) |
| B-fava | **broad-beans-fava gets a REAL second_planting with the SHARED harvest window** (4 cells: ca_north_coast z9/z10, northern_tier z6, warm_arid z8; Trevor 2026-07-09). Fava is a true two-sowing crop ("sow in February... and again in September"): the fall sowing overwinters and harvests in the SAME spring window -- authored in the cell's own calendar[] tokens (two plant events, one harvest window) and zone_notes. Extraction: plant_out = the fall span, start_indoors null, harvest_start/end = the shared single harvest span's endpoints. NOT or-normalized ("or" would misstate "and again" as either/or). Honest imprecision logged: on the north coast the overwintered crop peaks EARLY in the shared window; month-granular data cannot slice that (future sourcing item, corrections log). Declarative SHARED_HARVEST ruling in the generator, like the onion continuity fix. |
| C | **Envelopes narrow to the primary window** on every cell with a second_planting, at the CLEAN stage: `first_plant_date`/`last_plant_date` = primary plant window ends; `harvest_start`/`harvest_end` = primary harvest window ends. The fall cycle's envelope lives entirely in `second_planting{}`. REFLUSH/ALT_WINDOW cells keep their full envelope (one crop cycle). |
| D | **Fixed four-key shape, `start_indoors: null` for direct-sown second plantings.** No `direct_sow` variant; top-level already expresses direct-sow as `plant_out` + null `start_indoors` on these crops and second_planting mirrors it. `SECOND_PLANTING_KEYS` unchanged. |
| E | **Provenance inherited:** each new `second_planting{}` copies the cell's `sources[]` + `anchoring_urls{}` verbatim (the cited pages cover both windows; Population-1 precedent). |
| Precision | **Authored granularity preserved.** Month-granular second windows stay month-granular (`harvest_start "Nov"`, `harvest_end "Dec"`); no invented day precision. Month-only envelope values already exist in canonical (shallot `harvest_start "Jun"`). |

## 3. Scope (measured at `1372c299` with the real window parser)

- **Population 1 -- DEDUP: 64 cells / 7 crops** (cherry/grape/roma/beefsteak/heirloom
  tomato, broccoli, kohlrabi). **NOT celery** -- celery has no second_planting anywhere;
  the kickoff's roster line was wrong. 116 still-doubled top-level fields
  (start_indoors 30, plant_out 38, harvest 48). CAVEAT: doubled *harvest* strings are
  month-granular while `second_planting.harvest_start/end` are day-granular (e.g.
  `"Sep - Nov"` vs `"Sep 6 - Nov 8"`, 40 such fields), so the clean drops the SECOND
  comma-span by position and asserts OVERLAP with the second_planting span -- never
  byte-equality.
- **Population 2 -- EXTRACT: 94 TWO_CROP cells / 18 crops:** acorn-squash 5,
  banana-pepper 8, bell-pepper 8, broad-beans-fava 4 (shared-harvest ruling, §2 B-fava),
  butternut-squash 5, cantaloupe 3, cayenne-pepper 3, eggplant 6, habanero 3,
  honeydew-melon 3, jalapeno 6, pole-beans 9, potato 4, pumpkin 5, spaghetti-squash 5,
  swiss-chard 8, tomatillo 6, watermelon 3. (Fava was invisible to the kickoff-era
  scans -- single-month windows + a target-list-limited iteration; the gate's
  roster-wide Rule B sweep surfaced it.)
- **OR-NORMALIZE: 11 ALT_WINDOW cells + the 2-cell onion continuity fix** (§2 B-alt/B-fix;
  the 2 fix cells are among the 11).
- **EXEMPT (the gate must never flag):** 297 suitable=true cells; 59 woody-herb "or"
  cells; 4 chives/mint bimodal-harvest cells; 8 pepper REFLUSH cells; parenthetical
  commas (~240 cells, e.g. peach `"Apr - May (dormant, bare-root)"`).
- `calendar[]` UNCHANGED everywhere (the hand-authored full-year both-cycles overview).
- Cells whose planting fields disagree on window count (e.g. jalapeno se_gulf z8
  `start_indoors` single + `plant_out` doubled) extract what exists: absent second
  spans become null in second_planting. Nothing is invented.

## 4. Shared window parser -- `tools/plant_windows.py` (new)

ONE parser used by the extractor AND the gate, so they cannot disagree.

- Strip parentheticals first.
- Split the string on top-level commas into SPANS; within a span, `" or "`-joined
  chunks are alternatives of ONE planting choice (the span counts once).
- A span matches `Mon [D] [- Mon [D]]`: full month names (March) and abbreviations,
  single-month windows (`"Aug"`), optional day-of-month.
- API (approximate): `spans(s) -> [Span]` with month/day endpoints + raw text;
  `count(s)`; helpers for date-ordering and overlap.
- Proven against the false-positive classes in §3 EXEMPT plus the single-month and
  full-month-name forms that broke the naive scan (potato `"Feb - Mar, Aug"`,
  onion `"Jan - March"`).

## 5. Extraction (deterministic, per TWO_CROP cell)

```
second_planting = {
  plant_out:     second span of plant_out,
  start_indoors: second span of start_indoors if doubled else null,
  harvest_start: second harvest span's start (authored granularity),
  harvest_end:   second harvest span's end   (authored granularity),
  sources:       cell.sources (verbatim),
  anchoring_urls: cell.anchoring_urls (verbatim),
}
```

Per-cell asserts (extraction aborts on any failure): every doubled field has exactly
2 spans; spans date-ordered spring-first; fall plant window precedes fall harvest
window; cell has no existing second_planting.

The extractor emits an `apply_patch.py` batch JSON (from-guarded `add` ops for
second_planting; `replace` ops for or-norm/fix cells). It NEVER writes the canonical;
apply_patch.py is the only writer, SHA-gated per batch.

## 6. The gate -- A43 (`tools/second_planting_gate.py`, new)

Standalone module in the A40-42 pattern (`check_crop(crop)` returning violations),
wired into `whole_crop_gate.py` as A43 and run roster-wide by `gate_all.py`. Both
rules are TDD'd upfront; each is WIRED when it becomes globally true:

- **Rule B -- no unstructured comma shape** (wired at Stage-1 close; blocks new crops):
  on a crop with `succession_policy.suitable != true`, a cell with >= 2 comma-joined
  window spans in `start_indoors` OR `plant_out` and NO `second_planting` is a
  violation. Harvest-only doubling allowed (reflush/bimodal). `" or "` allowed.
- **Rule A -- dedup invariant** (wired at Stage-3 close): a cell WITH `second_planting`
  must be single-span in all three top-level window fields, and its envelope must sit
  within the primary windows -- formulated as CONTAINMENT: `harvest_end` parses inside
  the FIRST harvest span, `last_plant_date` inside the FIRST plant_out span.
  (Containment rather than not-equal-to-the-fall-values: fava's legitimately SHARED
  harvest window passes naturally while both real envelope defect classes still fire.)
- The existing SECOND_PLANTING_KEYS presence check stays as-is.

**TDD, RED before GREEN, adversarially proven on scratch copies of the real canonical:**
1. Inject a re-doubled `plant_out` onto a second_planting cell -> Rule A bounces.
2. Inject a new-crop-style comma `plant_out` with no second_planting -> Rule B bounces.
3. peach parenthetical comma -> NO fire.
4. Woody-herb `" or "` -> NO fire.
5. suitable=true cadence (carrot/lettuce) -> NO fire.
6. Pepper reflush harvest doubling -> NO fire.
A defect class is only trusted once it has been sneaked at the gate and caught.

## 7. Staged rollout (the UI never loses the fall crop)

**Stage 1 -- plant-dataset: POPULATE (additive) + or-norm + Rule B.**
Three archetype batches via `tools/apply_patch.py` + `tools/batches/`:
- S1-B1 solanaceae: banana/bell/cayenne/habanero/jalapeno pepper, eggplant, tomatillo (40 cells).
- S1-B2 cucurbits: acorn/butternut/spaghetti squash, pumpkin, cantaloupe, honeydew, watermelon (29 cells).
- S1-B3 rest: pole-beans, potato, swiss-chard, broad-beans-fava TWO_CROP (25 cells,
  fava via the §2 B-fava shared-harvest ruling) + the 13 or-norm/fix replace ops
  (onion, shallot, swiss-chard ALT_WINDOW).
Each batch: SHA-guarded, footprint-exact byte-diff (ONLY the intended crops, ONLY the
intended keys), count 124, COMPACT, no escaped-unicode regression. After S1-B3: wire
Rule B as A43. Release: whole_crop_gate 18/18 + gate_all 114/114 + release_verify +
per-batch source-truth sample; state trio (CURRENT_STATE.md HAND-MAINTAINED surgically
per `current-state-md-drift` -- no gen_current_state regen); Trevor approves the commit
and the push. NOTE (flagged, accepted): or-norm means the CURRENT astro UI immediately
stops synthesizing a second track for onion/shallot/swiss-chard ALT_WINDOW cells --
that track was fabricated (harvest guessed from a DTM midpoint), so this is a
correction, not a loss.

**Stage 2 -- plant-astro: Phase C read-layer flip.**
`SuccessionCard.astro`, `PlantingCalendarCard.astro`, `today.ts`, `plant-window.ts`:
the fall track comes from `second_planting{}` (present -> render; absent -> none);
comma-split synthesis (`hasSecondPlanting` from chunk count, `synthesizedSecondTrack`)
removed. During Stage 2 the top-level strings are STILL doubled, so the flip must
prefer `second_planting` over the comma string when both exist (no double-render).
Submodule bump; `cd ~/plant-astro && npm run build` (the real end-to-end check --
vitest + astro check alone missed the last break); grep `src/` for residual
multi-window assumptions; visual spot-check broccoli `ca_interior` z9 (pop 1) +
bell-pepper `se_gulf` z8 (pop 2). Trevor gates the bump. Work happens in ~/plant-astro,
never in the embedded submodule copy.

**Stage 3 -- plant-dataset: CLEAN + Rule A.**
Batches: pop-1 dedup (116 fields across 64 cells / 7 crops) + pop-2 clean (94 cells:
window strings -> primary span; envelopes narrowed per Decision C). Sanity assert per
field: dropped second span OVERLAPS the cell's second_planting span. Wire Rule A into
A43. Full suite + state trio + Trevor-gated commit/push; then another astro submodule
bump + `npm run build`. After Stage 3 the old shape is extinct and A43 enforces the
whole invariant roster-wide.

## 8. New-crop convention

Add to the crop-authoring checklist: a suitable=false two-season crop is authored
with primary-only top-level windows + a populated `second_planting{}`; alternative
establishment windows use `" or "`; a same-plant split harvest is comma-joined in
`harvest` only. A43 Rule B enforces the planting-field side from Stage 1 on.

## 9. Write discipline

- READ-ONLY on `crops_data_final.json` except the explicit per-batch promotes.
- Every batch SHA-gated against the then-current LATEST; apply to scratch; byte-diff
  footprint audit; COMPACT (`separators=(",",":")`, `ensure_ascii=False`, no trailing
  newline); count 124.
- Trevor approves every commit; Trevor confirms every push.
- State trio at each content release (Stage 1 and Stage 3); STATE_HISTORY most-recent-first;
  LATEST.txt SHA + session bump.

## 10. Definition of done

1. 94 TWO_CROP cells carry a populated, provenance-bearing `second_planting{}`.
2. 11 ALT_WINDOW cells or-normalized; onion continuity fix in.
3. plant-astro reads `second_planting{}`; no comma-split second-track synthesis remains;
   `npm run build` green.
4. All 158 second_planting cells (64 + 94) primary-only at top level with narrowed
   envelopes; `calendar[]` byte-identical throughout.
5. A43 both rules wired, TDD-proven (6 defect classes), gate_all 114/114 green.
6. Authoring convention documented; kickoff #18 closeable; memory
   `second-planting-demux-followup` updated to COMPLETE.

## 11. Risks / open items

- **Astro flip semantics during the doubled interim (Stage 2):** prefer-second_planting
  ordering is load-bearing; a component that renders BOTH the structured object and the
  comma tail would double-draw the fall crop. Mitigated by the grep + visual spot-check.
- **Envelope narrowing touches fields the app reads** (`first/last_plant_date`) --
  covered by the Stage-3 astro build + `dataset-shape-change-breaks-frontends` grep.
- **Parser drift:** single shared module (§4) is the mitigation; the gate and the
  extractor must never re-implement window parsing separately.
- **plant-app (iOS) consumers** are out of this kickoff's scope but read the same
  canonical; flag the shape change in the state trio so the app lane knows
  (weeks_indoors repoint memory pattern).
