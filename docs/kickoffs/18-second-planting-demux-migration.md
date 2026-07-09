# Kickoff #18 -- second_planting de-multiplexing migration

**For:** a fresh plant-dataset session (Trevor runs it before starting new crops).
**Lane:** plant-dataset (data + gate) + a coordinated plant-astro read-layer flip.
**Status at kickoff:** canonical `1372c299` (heat-gap flip live). READ-ONLY on
`crops_data_final.json` until this migration's explicit promote.

---

## 1. Mission

Finish the partially-rolled-out `second_planting` split so a two-season cell's
top-level per-zone window fields carry the **PRIMARY (spring) planting only**, with
the second (fall) planting in a structured `second_planting{}` object -- as an
**EXTRACT-then-clean migration, never a strip.** Then add a gate so the old
comma-string shape cannot regress or be re-introduced by new crops.

## 2. Why this BEFORE the new crops (Trevor, 2026-07-09)

Every new two-season crop authored in the old comma-string shape adds to the debt.
Landing the de-muxed convention **+ the gate** first means new crops are authored
correctly from the start and the gate enforces it. This is the stated reason to
sequence de-mux ahead of the new-crop work.

## 3. Read first

- **`docs/2026-07-08-second-planting-demux-findings.md`** -- the finding (esp. §7, true scope).
- **`docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`** --
  the `second_planting` model; §3 the rendering (PlantingCalendarCard MASKS the second
  planting, seasoned-only SuccessionCard reads `second_planting{}`); the explicit
  "the main window de-multiplexes back to a single window" intent.
- Memories: `second-planting-demux-followup`, `dataset-shape-change-breaks-frontends`,
  `current-state-md-drift`.

## 4. Scope (measured 2026-07-09, canonical `1372c299`)

- **Population 1 -- 64 cells already HAVE `second_planting`** (cherry/beefsteak/roma
  tomatoes + broccoli/kohlrabi/celery). Their still-doubled top-level windows are exact
  byte copies of the `second_planting` span -> de-mux = pure **DEDUP**, zero loss.
- **Population 2 -- 401 cells / 59 frost_anchored crops** have >=2 real date windows in
  a top-level field but NO `second_planting`. But that 401 splits sharply:

  | `succession_policy.suitable` | cells | crops | de-mux? |
  |---|---|---|---|
  | **false** (discrete spring+fall) | **106** | **21** | **YES -- the real targets** |
  | **true** (continuous cool-season cadence) | 295 | 38 | **likely NO -- see Decision A** |

  **suitable=false (the 21 real targets):** acorn-squash, banana-pepper, bell-pepper,
  butternut-squash, cantaloupe, cayenne-pepper, chives, eggplant, habanero,
  honeydew-melon, jalapeno, mint, onion, pole-beans, potato, pumpkin, shallot,
  spaghetti-squash, swiss-chard, tomatillo, watermelon. These mirror the cherry/beefsteak
  shape already in Population 1 -- a spring crop + a fall crop split by summer heat.

- **Perennials/trees are NOT in scope** (0 non-frost_anchored). A naive `split(',')`
  falsely counts ~15 trees (e.g. peach `plant_out: "Apr - May (dormant, bare-root)"` --
  the comma is inside a parenthetical, not a second window). **DETECTION MUST use a real
  date-window parser** (strip parentheticals; match `Mon D - Mon D` / `Mon - Mon` chunks),
  not a naive comma split. The naive count is ~641 (inflated); the parsed count is 401.

## 5. DECISIONS TO RESOLVE (brainstorm targets -- do NOT guess)

**Decision A (resolve FIRST -- it sizes the migration): are `suitable=true` cells exempt?**
The 295 `suitable=true` cells (carrot/lettuce/kale/spinach/radish/beet/...) have two
windows that are ONE continuous cool season (a sow *cadence*), not a discrete spring+fall
second planting. The SuccessionCard already renders `suitable=true` crops as a *rhythm*,
not two tracks. **Recommendation: EXEMPT them** -- their multi-window top-level is the
legitimate full sow window; do NOT create a `second_planting` for them. If confirmed, the
real de-mux target is **~106 cells / 21 crops**, tractable and well-precedented (same shape
as the 64 already done). CONFIRM with Trevor before proceeding.

**Decision B -- primary-window ordering.** The first comma-window is assumed spring
(primary), the second fall. VALIDATE every target cell's windows are date-ordered; flag any
that aren't (wrap-around, 3+ windows).

**Decision C -- `first_plant_date` / `last_plant_date`.** Today they span BOTH windows
(e.g. bell-pepper: `Mar 15` / `Sep 20`). Decide: narrow to the primary, or keep the full
envelope? The `calendar[]` (hand-authored, both cycles) STAYS regardless; but the astro
cards read these strings. Coordinate with the consumer (Decision E).

**Decision D -- direct-sow second plantings.** The 2026-06-05 `second_planting` shape
(`plant_out`, `start_indoors`, `harvest_start`, `harvest_end`) was designed for a TRANSPLANT
crop (cherry). Several targets are direct-sown (pole-beans, potato) with `start_indoors=null`.
The spec flagged a `direct_sow` variant as out-of-scope-for-cherry -- rule whether
`second_planting` needs it, or `start_indoors:null` suffices.

**Decision E -- sources/anchoring_urls inheritance.** The cell's `sources` cover both
windows -> inherit into `second_planting` (as Population 1 does). Confirm.

## 6. The principle: EXTRACT-then-clean, NEVER strip

A Population-2 second window has NO structural home, so:
1. **EXTRACT** -- build `second_planting{}` from the SECOND date window (+ inherit
   `sources`/`anchoring_urls`).
2. **CLEAN** -- set the top-level window fields to the PRIMARY (first) window only.

A naive "remove the second span" DELETES the fall planting. (Population 1 is the safe dedup;
Population 2 is the real migration.)

### Worked example (bell-pepper `se_gulf` z8)
```
BEFORE                                      AFTER
plant_out: "Mar 15 - Apr 15, Sep 1 - Sep 20"   plant_out: "Mar 15 - Apr 15"
harvest:   "May 15 - Jun 30, Nov 1 - Nov 30"   harvest:   "May 15 - Jun 30"
harvest_start/end: "May 15" / "Nov 30"         harvest_start/end: "May 15" / "Jun 30"
                                               second_planting: {
                                                 plant_out: "Sep 1 - Sep 20",
                                                 start_indoors: null,
                                                 harvest_start: "Nov 1", harvest_end: "Nov 30",
                                                 sources: [...], anchoring_urls: {...}
                                               }
calendar: UNCHANGED (the full-year both-cycles overview stays)
```

## 7. The gate (TDD, RED before GREEN, adversarially proven on a scratch canonical)

Add a de-mux invariant to `tools/whole_crop_gate.py`:
- If a cell HAS `second_planting`: none of top-level `start_indoors`/`plant_out`/`harvest`
  may contain the `second_planting` window as a comma-span (the dedup invariant).
- A cell with >=2 real date windows AND no `second_planting` AND
  `succession_policy.suitable != true` is a VIOLATION (blocks the old shape + new crops
  re-introducing it). `suitable=true` cells are EXEMPT (Decision A).
Inject a still-doubled cell into a scratch copy of the real canonical; confirm it bounces
before trusting the gate.

## 8. Staged rollout (so the UI never loses the fall crop)

The clean phase REMOVES the fall window from the top-level strings the astro cards read
today, so it must not ship before the cards read `second_planting{}`. Recommended staging:

1. **plant-dataset -- POPULATE `second_planting{}` (ADDITIVE; top-level unchanged).** Safe:
   nothing breaks; `second_planting` becomes the complete structured home. SHA-guarded,
   archetype-batched, footprint-exact, gate-clean.
2. **plant-astro -- flip `SuccessionCard` + `PlantingCalendarCard` to read
   `second_planting{}`** for the fall cycle (the "Phase C read-layer flip"). Today they
   synthesize it from the comma-string (`hasSecondPlanting` = plant_out comma count) /
   `calendar[]` (`synthesizedSecondTrack`). Known consumers: `PlantingCalendarCard.astro`,
   `SuccessionCard.astro`, `today.ts`.
3. **plant-dataset -- CLEAN top-level to primary-only.** Now safe.

Per `dataset-shape-change-breaks-frontends`: after ANY submodule bump,
`cd ~/plant-astro && npm run build` (a full build is the real end-to-end check; vitest +
astro check alone missed the last break). Grep plant-astro `src/` for the old multi-window
assumptions before/after each stage.

## 9. New-crops relationship

Once the gate lands, a new `suitable=false` two-season crop MUST author `second_planting{}`
+ primary-only top-level (the gate blocks the old comma shape). Add the convention to the
crop-authoring checklist so new crops comply from the start. (This is the reason to run
de-mux before the new crops.)

## 10. Recommended flow for the executing session

1. Read §3 docs + this kickoff.
2. **Resolve Decision A first** (suitable=true exempt?) -- it sizes the real population
   (~106 vs 401).
3. superpowers: brainstorm (Decisions A-E + gate + staging) -> spec -> plan -> execute
   (TDD, SHA-guarded per-archetype batches via `tools/apply_patch.py`, footprint-exact,
   full gate suite + state trio each release).
4. Coordinate the plant-astro read-layer flip; `npm run build` plant-astro.

## 11. References

- `docs/2026-07-08-second-planting-demux-findings.md`
- `docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`
- `tools/whole_crop_gate.py` (`SECOND_PLANTING_KEYS` validation) · `tools/apply_patch.py`
  (SHA-guarded splice) · `tools/annual_calendar.py` (calendar deriver; `calendar[]` stays)
- plant-astro: `src/components/guides/{PlantingCalendarCard,SuccessionCard}.astro`
- memories: `second-planting-demux-followup`, `dataset-shape-change-breaks-frontends`,
  `current-state-md-drift`

---

## 12. CLOSED (2026-07-09) + the new-crop authoring convention

Migration complete: `1372c299 -> 50288c02` (3 populate + 2 clean batches, A43 both
rules live). Final scope: 94 extracted / 18 crops (kickoff's 106/21 was re-ruled:
reflush + chives/mint exempt, fava ADDED with a shared-harvest ruling; Population 1
= 5 tomatoes + broccoli + kohlrabi, NOT celery). Full record:
`docs/superpowers/specs/2026-07-09-second-planting-demux-migration-design.md` + the
2026-07-09 STATE_HISTORY entries.

**AUTHORING CONVENTION (enforced by whole_crop_gate A43 -- a new crop cannot certify
otherwise):** a suitable=false two-season crop is authored with primary-only
top-level windows + a populated `second_planting{}` (four keys: plant_out,
start_indoors (null if direct-sown), harvest_start, harvest_end + inherited
sources/anchoring_urls). Alternative establishment windows are `" or "`-joined,
never comma-joined. A same-plant split harvest (reflush) is comma-joined in
`harvest` ONLY, with single-window planting fields. Envelope fields
(first/last_plant_date, harvest_start/end) describe the PRIMARY cycle only.
