# Second-planting structure + shape-complete region shells -- design

**Date:** 2026-06-05
**Author:** Claude Code (structural lane)
**Status:** Approved design (Trevor, 2026-06-05). Implementation plan next.
**Milestone:** M16, cherry-tomato Step 3.5 (region shell build) + a net-new resolved-layer structure.
**Reads against:** gold-standard arc checklist v1.5 (Step 3.5); region-primary shape spec v1.0; calendar-model schema addendum (session 4c, the `track` enum); `tools/whole_crop_gate.py`.
**Start SHA:** `29b3aaa904a62487960c5dc53b4282538454076f696ffec039ac4ab87937801a` (must equal `LATEST.txt` at apply time).

---

## 1. Problem

M16 brings `cherry-tomato` to region-primary gold-standard. Step 3.5 (Claude Code lane) builds all 10 region cells to the reference shape. While scoping that build, two things surfaced that the kickoff did not pre-decide:

1. **Cherry is the first crop to need a "second planting."** Tomato is not a succession crop (`succession_policy.suitable=false, successions=1`), but it is plantable a second time for a longer harvest -- cold zones 6-7 ("two crops possible") and warm zones 9+ (a late-summer batch for fall/winter). Today that option lives only as prose (`succession_policy.tip_*`, `zone_notes`); the calendar cannot render it or notify on it. Trevor's decision: make it **structured** (computed dates, a second calendar band, notifications) and **own its representation in the Claude Code lane**, because the same person builds the app/website that consumes it.

2. **Shell thickness.** The Step 3.5 shells can be thin (track only, Step 4 builds the window structure) or shape-complete (the archetype-correct skeleton scaffolded with null values, Step 4 fills only values). Trevor's criteria: accuracy and scale, time is not a constraint.

This design settles both, plus the resolved-layer model that second planting and succession imply.

---

## 2. Decisions

**D1 -- Second planting is structured, not prose.** It gets computed per-zone dates so the calendar draws a second `plant -> harvest` band and the app can fire "time to start your fall batch" notifications. Default-visible (not hidden behind an affordance).

**D2 -- Shells are shape-complete, not thin.** The accurate-and-scalable choice. A thin shell pushes window-structure *building* into 121 independent Step-4 passes -- 121 chances to drift. A shape-complete shell scaffolds the archetype-correct skeleton with null values, so Step 4 fills *values* into a fixed shape the renderer can rely on. Empty `windows`/window arrays still let each source decide one-vs-two windows, so per-source accuracy is preserved. Null is not data, so this respects "do not carry warm-zone defaults as if verified."

**D3 -- Two honest resolved-layer patterns, not one forced shape and not three messy ones.** Second planting and succession are different *kinds* of thing and must read differently:
- **Discrete planting** (`beginner`, `second_planting`): one `plant -> harvest` window. The main planting and a second planting are genuinely alike -- same shape, just different times of year.
- **Succession** (`succession`): a *cadence* -- keep sowing every N days across a span. Not a window, a rhythm. Its own shape.

**D4 -- Each crop carries only the structures for what it actually is; each concept has one fixed shape across crops.** A crop is not forced to carry slots for concepts it does not use. Consistency means *a given concept always has the same shape wherever it appears*, not *every crop has every concept*.

**D5 -- Lettuce is NOT touched.** `lettuce-leaf` already correctly represents what it is: a flat main planting + succession (`succession_spring`/`succession_fall`). It is not a second-planting crop. We **ratify lettuce's existing shapes as the standard** (main-flat, succession-cadence) rather than reshape lettuce to match a new model. Lettuce stays byte-identical and certified; no migration, no re-gate, no reopening the reference crop. Its reference shape does not move, so claude.ai's methodology references to it stay valid.

---

## 3. The resolved-layer model

Each `regions[r].resolved_by_zone[z]` cell. **Bold = new or formalized in this design; everything else is unchanged from lettuce's proven shape.**

```
resolved_by_zone["7"] = {
  calendar: [12 month-states],                 // combined across all bands -- unchanged
  first_plant_date, last_plant_date,           // overall envelope -- unchanged
  harvest, notes, zone_notes, planting_note,   // zone display -- unchanged
  resolution_method,                           // unchanged
  sources: [...], anchoring_urls: {...},        // zone-level provenance -- unchanged

  // ---- MAIN PLANTING (track: beginner) -- flat, universal, unchanged ----
  plant_out, start_indoors, harvest_start, harvest_end,

  // ---- SECOND PLANTING (track: second_planting) -- NEW discrete-window structure,
  //      present ONLY on zones that have one ----
  second_planting: {
    plant_out, start_indoors, harvest_start, harvest_end,
    sources: [...], anchoring_urls: {...}
  },

  // ---- SUCCESSION (track: succession) -- cadence, succession crops only,
  //      ratified from lettuce; cherry never has this ----
  succession_spring: "Apr 15, Apr 29, May 13, ...",
  succession_fall:   "Jul 1, Jul 15, ..."
}
```

Three named concepts, three clear homes:
- **Main** = flat fields. Renderer reads them as today. (Why flat and not nested: it is "the planting," universal, and keeping it flat is what makes lettuce zero-touch. The minor main-flat / second-nested asymmetry is the accepted cost of not reshaping a certified crop.)
- **`second_planting`** = a discrete-window object, same field set as the main window. Present only where the zone has a second planting.
- **Succession** = `succession_spring` / `succession_fall` cadence strings, exactly as `lettuce-leaf` established. Future succession crops (carrot) match lettuce; they do not invent a new shape.

Renderer model (the app Trevor builds):
```
drawBand(cell)                                  // main, always
if (cell.second_planting) drawBand(cell.second_planting)   // second discrete band
if (cell.succession_spring || cell.succession_fall) drawCadence(cell)  // repeating-sow pattern
```
Each branch matches a real distinction. They cannot be confused, which is the point.

### Rendering -- grounded in the existing app (Trevor 2026-06-05)

**The dataset shape is rendering-agnostic.** The structured `second_planting` object feeds either a separate seasoned card or a same-calendar band equally; we do not need to settle the rendering to do the dataset work. This section records what plant-astro already does so the dataset feeds it cleanly. These components currently read `zones{}`; they move to `regions{}.resolved_by_zone[z]` at the Phase C read-layer flip.

**Existing components:**
- **`PlantingCalendarCard`** (`src/components/guides/PlantingCalendarCard.astro`) -- the MAIN cycle, shown in BOTH beginner + seasoned. Two rows: a plant row (`start_indoors -> plant_out`) and a harvest row (`harvest_start -> harvest_end`). Deliberately MASKS the second planting (spring cycle only) so it never implies "what I plant in March produces through December."
- **`SuccessionCard`** (`src/components/guides/SuccessionCard.astro`) -- **seasoned-only** (`tone="seasoned"`; hidden in beginner mode by `.level-beginner .seasoned-only{display:none}`). Two render modes that map exactly onto this design's two structures:
  - *rhythm mode* (`succession_policy.suitable=true`, e.g. lettuce) -- the succession cadence.
  - *multi-track mode* (`suitable=false` + a second window, e.g. cherry z9) -- the second planting, rendered as its own two-row track (plant row + harvest row) with heat-pause cells.

**Per-track visibility (already built, keyed off `track` + the beginner/seasoned toggle):**

| Mode | Copy register | Planting surfaces shown |
|---|---|---|
| Beginner | `_beginner` copy | main cycle only (`PlantingCalendarCard`) |
| Seasoned | `_seasoned` copy | main cycle + `SuccessionCard` (second planting OR succession) |

**Why this design helps (the real win):** today both cards SYNTHESIZE the second planting fragilely -- parsing a comma-separated multi-window string (`plant_out: "Feb 7 - Feb 28, Jun 24 - Jul 8"`), detecting the second cycle from `calendar[12]` heuristics, and guessing harvest from a `days_to_maturity` midpoint. The structured `second_planting:{}` replaces all of that with explicit, sourced dates:
- The main window **de-multiplexes** back to a single window (the second window moves out of the comma-separated `plant_out` string into `second_planting.plant_out`).
- `SuccessionCard` multi-track mode reads `second_planting:{}` directly instead of synthesizing it.
- `SuccessionCard` rhythm mode reads `succession_spring`/`succession_fall` directly.

So the two-row layout, the seasoned-only visibility, and treating succession vs second-planting as different render modes are ALL already built -- this design just feeds them clean, explicit data instead of fragile synthesis.

**Same calendar vs separate card is the renderer's call, not the dataset's.** Current impl = a separate seasoned-only card (`SuccessionCard`). A same-calendar second band is an option the same structured data supports. Decide it at the plant-astro Phase-C read-layer rewrite; the dataset is identical either way. (`calendar[12]` stays the coarse single-state-per-month strip; the precise per-band two-row timeline is drawn from the window date fields, which are the source of truth.)

### Region-constant rule layer

The region-primary model has a rule layer (`regions[r].plantings[]`, tagged by `track`) and a resolved layer (`resolved_by_zone[z]`). Second planting mirrors how succession already works in lettuce: a region-constant rule entry plus a resolved representation.

- `regions[r].plantings[]` gains a `{succession_id:2, label:"second"/"fall", track:"second_planting", <window rule>}` entry on regions that have a second planting. (`track:"second_planting"` already exists in the 4c enum.)
- The window-rule shape inside it mirrors the `beginner` entry's (`start_indoors`/`plant_out`/`harvest_start`/`harvest_end` rule objects with `from`/`offset_days`/`window_days`).

---

## 4. The `second_planting` structure -- the one net-new thing

This is the structure Claude Code owns (the representation). claude.ai owns the *data* that fills it (which zones, what dates -- biology).

**Resolved (per applicable zone):** `resolved_by_zone[z].second_planting = {plant_out, start_indoors, harvest_start, harvest_end, sources, anchoring_urls}`. Same field set as the main window. Absent on zones with no second planting.

**Rule (region-constant):** a `plantings[]` entry with `track:"second_planting"`.

**Which zones get it:** a biological determination (claude.ai, Step 4/5). Step 3.5 establishes the *structure exists and is defined*; it does not decide per-zone presence or fill dates.

**Calendar:** the existing `calendar[12]` array encodes the combined month-states for both bands (the second band's `plant`/`growing`/`harvest` months appear in the same array). No second calendar array.

---

## 5. Cherry Step 3.5 build (Claude Code)

Cherry-tomato only. Build all 10 region cells to the ratified reference shape.

**northern_tier (zones 3-7) -- promote FROM legacy `zones{}`:**
- Add `track:"beginner"` to the single region-constant `plantings[0]` (clears the null-track violation).
- Strip the nested `plantings` key from each `resolved_by_zone.{3..7}` cell (clears the §3b-i stale-shape violation; also clears the 2 nested `mu_ext` anchoring gaps as a side effect).
- Re-stamp `resolution_method: static_precompute -> zone_promoted_verified` on each cold cell (semantic truth; lettuce parity; the checklist requires it though the tool does not yet enforce it).
- Replace the `plantings_provenance` "LIFTED VERBATIM" string with a `zone_promoted_verified` provenance object.
- `region_notes_*` keys stay null (admission-acceptable at 3.5; claude.ai authors at Steps 6/7).
- **No succession hoist** (cherry is not succession-suitable).
- **Second planting:** zones 6-7 carry "two crops possible" prose. Step 3.5 does NOT author the second-planting dates (biology). It leaves the structure defined for claude.ai to populate at Step 4/5. The `cornell_ext` null-URL in zone 6 stays (Step 5 URL-discovery, claude.ai).

**9 warm/CA regions -- shape-complete RULE skeleton; resolved cells stay PENDING:**
- **Shape-completeness (D2) applies to the rule layer.** Convert `plantings:["PENDING ..."]` to a region-constant rule object `[{succession_id:1, label:"main", track:"beginner", <archetype window-rule keys present, arrays empty>, anchoring_urls:{}}]`. This is the fixed skeleton Step 4 fills values into.
- **The `resolved_by_zone` cells are derived output**, not rule shape. They stay as PENDING fill-targets (the existing minimal cells: a PENDING marker + `resolution_method`), populated by Step 4 when windows are sourced. The only Step-3.5 requirement on them: no nested `plantings` key (none exist on the warm stubs). Do not scaffold null resolved values -- there is nothing to resolve until Step 4 sources windows.
- Keep the existing seeded `sources`.
- Fix the 4 `region_label` em-dashes (`California -- Interior Valleys` -> `California: Interior Valleys`). Mechanical, in lane, clears 4 of 5 §C/D dash hits.
- `region_notes_*` keys present, null.
- Do NOT carry warm `zones{}` data into the cells as if verified (climate-contamination guard). Shape only; claude.ai sources windows at Step 4.

**Archetype window-rule skeleton (warm_season_fruiting, transplant):** the region-constant `plantings[0]` rule object carries `start_indoors`, `plant_out`, `harvest_start`, `harvest_end` as present-but-empty arrays. (Greens use `direct_sow` instead of `start_indoors`+`plant_out`; that branch is archetype-derived and out of scope for cherry.)

**No `second_planting` data is written at Step 3.5.** Step 3.5 produces the *representation* (this spec) and the *gate's awareness* of `second_planting`; cherry's actual second-planting rule entries and resolved windows are authored by claude.ai at Step 4/5 (which zones + dates = biology). At the end of Step 3.5, cherry carries main-band shells only.

---

## 6. Gate changes (`tools/whole_crop_gate.py`)

The gate is the Step 11 certification suite and must learn the new structure so it neither false-flags it nor misses it.

- **Recognize `second_planting` as a known resolved-layer structure**, not a stray. Its `sources`/`anchoring_urls` are walked by §E (source-tier) and §F (anchoring) the same as any claim-bearing leaf -- the recursive walkers already descend into it, so confirm they treat it correctly (it carries `sources` + `anchoring_urls`, so §F's `check_pair` should fire on it when populated).
- **§A2 stale-shape check** looks for a nested `plantings` key in `resolved_by_zone` cells. `second_planting` is a *different* key, so it is not mistaken for the forbidden nested `plantings` -- confirm by name, not by "any nested dict."
- **Optional shape validation:** when `second_planting` is present, assert it carries the discrete-window field set (`plant_out`/`start_indoors`/`harvest_start`/`harvest_end`). Keep this lenient at admission (null values acceptable), strict at certification (populated), mirroring the region_notes admission/certification split.
- **No change to §A2's region_notes-null check.** After the shell build, cherry's region_notes are null (claude.ai authors them). Per checklist v1.5 these are admission-acceptable at Step 3.5 and become violations only at Step 11 certification. Step 3.5 "done" = the three §A2 *shape* classes at 0 (`stub/missing: 0 | null-track: 0 | stale nested: 0`), read directly off the gate's own A2 line. We do not author placeholder copy to zero the count, and we do not add an admission-mode flag -- the cert tool stays pristine.

**Lettuce regression guard:** after every gate edit, re-run `whole_crop_gate.py lettuce-leaf` and confirm it still returns 0. The gate must not start flagging the untouched, certified crop.

---

## 7. Lane split

**Claude Code (this work):**
- This spec; the `second_planting` representation; ratifying main-flat and succession shapes as standards.
- Cherry's 10 region shells (north promoted, warm shape-complete null).
- The `region_label` dash fixes (4).
- Gate updates + the lettuce regression guard.
- Write discipline (Section 8); the PROMOTE close ritual.

**claude.ai (downstream, Steps 4-8):**
- Which zones get a second planting + the second-planting *dates* (Step 4/5 biology).
- Warm-region window sourcing into the shells.
- `region_notes_*` copy (Steps 6/7).
- `cause_beginner` + the other dual-voice siblings (§B, finding `_004`).
- The `harvest_to_table` T2-as-evidence ruling (§E, Step 10).
- The extreme-zone computation record (Step 2, finding `_003`).
- `cornell_ext` (zone 6) URL discovery (Step 5).

**Not in scope (explicitly):** reshaping lettuce; a `windows{}` wrapper; an admission-mode gate flag; authoring any second-planting or warm-window date values; **the plant-astro renderer rewrite** to read `regions{}` and consume `second_planting:{}` instead of synthesizing from `zones{}` multi-window strings (future, gated to the Phase C read-layer flip -- `zones{}` stays coherent as the fallback the current UI reads until then, so nothing breaks now).

---

## 8. Write discipline + definition of done

**Write discipline (same as the lettuce arc):**
- SHA-gate the apply against `29b3aaa9...` == `LATEST.txt`; `sys.exit(1)` on mismatch.
- Operate on a scratch copy; minified output `json.dump(data, f, separators=(',',':'), ensure_ascii=False)`.
- Collateral audit: every crop other than `cherry-tomato` byte-identical; every top-level key on cherry unchanged except the intended `regions{}` edits. **`lettuce-leaf` in particular byte-identical.**
- Independent post-write re-verification reading the output only.

**Definition of done (this Step-3.5 + structure work):**
- `whole_crop_gate.py cherry-tomato`: §A2 shape classes = 0 (`stub: 0 | null-track: 0 | stale nested: 0`). Residual gate count is the documented downstream claude.ai work (region_notes-null, dual-voice siblings, source-tier, dash on the source name).
- `whole_crop_gate.py lettuce-leaf`: still 0 (regression guard).
- Collateral audit clean.
- PROMOTE: write canonical, re-pin `LATEST.txt` (new SHA + date + session), regenerate `CURRENT_STATE.md`, append `STATE_HISTORY.md`, sync `00-current/`, commit + push (dataset push is autonomous, announce-then-execute). plant-astro stays gated.

---

## 9. Risks / open items

- **Gate edits touching a certified crop's result.** Mitigated by the lettuce regression guard (re-run after every gate change; must stay 0).
- **Warm-shell window-key choice (transplant vs direct-sow).** Cherry is transplant (`start_indoors`+`plant_out`). A warm region that direct-sows tomatoes would swap to `direct_sow` -- a rare per-source Step-4 override, not a Step-3.5 default. Flagged for claude.ai.
- **Succession shape is ratified from a single exemplar (lettuce).** When carrot (the next succession crop) runs, confirm `succession_spring`/`succession_fall` still fits; revise the standard then if not.
- **`second_planting` is exercised by one crop at first (cherry).** Beefsteak repeats it; the structure is provisional until both pass, like every other M16 ruling.
- **claude.ai awareness.** This introduces a new resolved-layer structure (`second_planting`) and ratifies two existing shapes as standards. Flag in `CURRENT_STATE.md` / `STATE_HISTORY.md` at close so claude.ai's Step 4/5 authoring follows the spec.
