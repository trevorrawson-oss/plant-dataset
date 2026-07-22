# Utah "Dixie" region -- FINAL whole-arc review (cross-cutting)

Reviewer: independent final holistic pass (Claude Code). Date: 2026-07-22. READ-ONLY.
Scope: the shipped `utah_dixie` region (canonical `d8e0a98e`, committed UNPUSHED) via the 5 class
staging files `tools/staging/utah_dixie_{annuals_warm,annuals_cool,trees,citrus,perennials}.json`
(identical to what shipped -- verified against `crops_data_final.json`), the spec
`docs/superpowers/specs/2026-07-22-utah-dixie-region-design.md`, the sourcing bible
`docs/reviews/notes/2026-07-22/utah_dixie_sources.md`, prior reviews A/B, kickoff #39,
`CURRENT_STATE.md`, `LATEST.txt`. This is the holistic pass the two per-class reviews (A = fruiting/
suitability, B = cool) could each miss at their scope seam.

---

## OVERALL VERDICT: FIX-FIRST

The build is factually clean and every spec delta is executed exactly. There are **zero** data,
sourcing, calendar-coherence, or delta-fidelity defects. Every issue below is a **prose/provenance
leak**, and the most important one is a residual instance of the *exact* sibling-region-token class
the controller's own leak-sweep + Review B already chose to remediate -- left in 8 cells that fell in
the seam between reviews A and B (the woody-herb + corn/bean `plantings_provenance` fields, one of them
carrying the forbidden name "Nevada"). Because the dataset is committed but UNPUSHED and the fix is a
fast, mechanical consistency sweep matching the standard the project already applied, this should be
swept before Trevor pushes rather than shipped with a known inconsistency. Nothing here is a factual
regression; a reviewer could reasonably call it READY-TO-PUSH-after-sweep.

**Counts: Critical 0 | Important 2 | Minor 4**

---

## CRITICAL (0)
None. No zero-harvest cell (habanero C1 from Review A is fixed), no fabricated source or window, no
delta contradiction, no calendar defect.

---

## IMPORTANT (2)

### F1. Sibling-region tokens survive in 5 woody-herb `plantings_provenance.note` fields
- **crops/file:** lavender, oregano, rosemary, sage, thyme -- `utah_dixie_perennials.json`
- Each `plantings_provenance.note` contains: "...closer to the **warm_arid / low_desert_az / nevada**
  desert-thrives framing than to any humid belt." That is the sibling-region NAME **Nevada** plus the
  internal region-ids **warm_arid** and **low_desert_az** -- the identical leak class Review B flagged
  as I1 for the OTHER perennials (bee-balm/echinacea/mint/chamomile/chives) and that the controller
  fixed there (those cells now carry no region-id in `plantings_provenance`). These 5 were missed
  because they live in the perennials file (Review A's scope), and Review A explicitly deemed the
  woody-herb provenance language "out of scope / canonical pattern" -- so no one swept them. **Confirmed
  present in the shipped canonical** (`d8e0a98e`) on all 5 slugs. Review B's own ruling is that these
  tokens "must not appear whether or not the field renders," and the project acted on it, so leaving
  these ships an inconsistency: identical archetype cells disagree on the same field.
- **Fix:** strip the region-id list; describe the lineage generically, exactly as the cool-file
  perennials were reworded (e.g. "...suit this crop far better than any humid belt: arid heat, intense
  sun, and alkaline well-drained soil."). Factual content unchanged. (5 cells.)

### F2. "Nevada" / "UNLV" survive in 3 corn/bean `plantings_provenance` strings
- **crops/file:** dry-bean, pole-beans, sweet-corn -- `utah_dixie_annuals_warm.json`
- `plantings_provenance` narrates the donor lineage in user-adjacent prose:
  - dry-bean: "...**the Nevada donor** cell's structure carried across but its **UNLV** window was
    replaced with USU's own date."
  - sweet-corn: "...This DROPS **the Nevada donor's UNLV**-sourced spring-plus-fall two-cycle
    structure..."
  - pole-beans: "...mirroring **the Nevada donor** cell's own bearing-window length."
- Same forbidden-token class as F1 (and as Review B's leek C1 "Nevada" leak, which was fixed). The
  build-lineage attribution should not name the sibling region or "UNLV" in a stored prose field.
- **Fix:** drop the donor attribution -- state the fact without the region/institution name (e.g.
  "single spring block per USU's one Group C date; harvest re-anchored to the crop's own dry-down").
  (3 cells.)

*(F1 + F2 together = 8 cells sharing one root cause: the `plantings_provenance` field was never
included in the leak-sweep that cleaned the consumer `region_notes` / `zone_notes` surfaces.)*

---

## MINOR (4)

### M1. "Shape C" build-label in 6 corn/bean `plantings_provenance`
- dry-bean, pole-beans, sweet-corn, field-corn, flint-corn, popcorn (`utah_dixie_annuals_warm.json`):
  each opens "Utah Dixie **Shape C** ... cell". "Shape C" is an internal authoring label (Review A M1
  called the analogous "Shape A" leak Minor). Scrub to plain wording ("single full-season cell") if the
  F2 sweep touches these anyway.

### M2. `heat_pause` snake_case token in a rendered consumer field (echinacea)
- echinacea `plantings[0].transplant[0].synthesis_note_seasoned` (`utah_dixie_annuals_cool.json`):
  "...it does not need a summer **heat_pause** in St. George's Dixie...". This is a *rendered* consumer
  field (Review A M2 class), and both prior reviews missed this instance. **Fix:** "a summer heat
  pause" (plain English).

### M3. `cold_pause` snake_case token in consumer zone notes (garlic)
- garlic `resolved_by_zone.8.notes` (`utah_dixie_annuals_cool.json`): "...keeps growing through the mild
  St. George winter (not a true **cold_pause**)...". Same class as M2, in the zone-notes surface.
  **Fix:** "not a true winter dormancy / not a true cold pause".

### M4. Kickoff #39 cites a stale canonical SHA
- `docs/kickoffs/39-utah-dixie-plant-app.md` states "Canonical `b1045e04` -> **`f7e3afe3`**
  (commit `d215415`)". That is the pre-city-fix promote SHA; the actual shipped canonical is
  **`d8e0a98e`** (after the `0ff05a2b` city-reference consumer-prose fix). The app-wiring instructions
  (`REGION_STATES.utah_dixie=['UT']`, the 847xx-only ZIP3 fence, NO isWarm #32 dep) are all correct and
  SHA-independent; only the informational SHA is one commit stale. `LATEST.txt` and `CURRENT_STATE.md`
  are both correct. **Fix:** update the kickoff's SHA to `d8e0a98e` (optional -- informational only).

---

## CROSS-CUTTING CONFIRMATIONS (passed)

**Delta fidelity (all 5 classes, verified against `crops_data_final.json`):**
- Trees: apple / pear-asian / pear-european = `marginal`; cherry-sour = `marginal` (Review A I1
  applied); cherry-sweet = `fruits_reliably`; pawpaw = `unsuitable`; apricot / nectarine / peach /
  plum / fig / mulberry / persimmon / pomegranate = `fruits_reliably`. Exact spec match.
- Citrus: mandarin-clementine + lemon = `survives_no_fruit`; orange-navel + lime + grapefruit =
  `unsuitable`. NO `fruits_reliably` (cold-limited). Exact spec match.
- Berries carry no suitability field; honesty lives in prose -- raspberry marginal fall-bearing/
  primocane steer (Caroline/Josephine/Polana/Joan J/Polka + Bababerry/Dorman Red, iron-chlorosis,
  "Utah's Dixie" ripens-after-heat), blackberry marginal (higher-elevation column), blueberry
  very-marginal (alkaline, container-only), elderberry marginal (moisture), **strawberry a
  low-elevation thriver** (perennial matted row, USU low-elev list). Exact spec match.
- ALL 42 warm crops single-spring: zero `second_planting` track in the warm file (delta 4a load-bearing
  rule holds). The R2 hot-chile fix is an extended bearing window, not a replant.
- onion + shallot = `intermediate_day` (delta 4d).
- Frost anchor Mar 30 / Nov 1 uniform across all 111 cells. (The lone "Feb 28" token is parsley's
  overwintered fall `harvest_end`, not a Nevada frost-date leak.)

**Honesty / no fabrication:**
- Every cited source id across all 5 files is one of the 8 registered USU T1 sub-ids
  (`usu_ext_veg_dates/tomato/wash_fruits/raspberry/garlic/fall_veg/wash_frost/peaches`); all 8 exist in
  the canonical `source_catalog`, all `tier=T1`, URLs matching the sourcing bible exactly. No invented
  source, no non-USU aggregator cited.
- Non-USU-table crops disclose the analogy: edamame (Review A I4 fix present -- "snap bean" by-analogy
  grouping), okra + sweet-potato ("outside USU Table 1 ... heat-lover biology"), mulberry + pomegranate
  ("USU ... does not name ... judged from low-desert biology + neighbor regions"), borage (Group A
  analogy). No uncited USU date attributed to an unlisted crop.
- Chill band `[250,450]` is honestly flagged in `region_chill_delivered_provenance.utah_dixie` as
  "elevation-bracketed INFERENCE, not a measured figure" (Phoenix `[100,400]` below, Las Cruces
  `[450,850]` above), documenting the empty chill-hunt. No false precision.

**Consumer-string leak sweep (all 5 files, all string values):**
- em dashes: 0. en dashes: 0. spelled "degrees": 0 (Review B I3 "37 degrees N" -> "37°N" applied).
  `°F` glyph used throughout.
- Phoenix / Las Vegas / Las Cruces / UNR / UNLV / Heflebower in **consumer** fields: 0 (the controller
  leak-sweep + Review B I2 Heflebower normalization applied). "Nevada" / "warm_arid" / "low_desert_az"
  survive **only** in the 8 `plantings_provenance` cells above (F1/F2). `heat_pause`/`cold_pause`
  snake_case in a rendered consumer field: only M2/M3.

**Consistency:**
- Dual-register real hooks: 0 of 111 cells have `region_notes_beginner == region_notes_seasoned`; 0
  share even the first 60 chars; beginner is consistently the plainer register (verified on the berry/
  strawberry set). No cross-crop pasted-identical `region_notes_beginner` or `_seasoned`.
- heat_pause months honest per crop (Shape A `[7,8,9]` deliberate to preserve the June harvest token,
  per Review A M3; hot chiles re-authored heat-lover per Review A R2).

**Doc accuracy:**
- `CURRENT_STATE.md` top block: SHA `d8e0a98e`, 111 cells, 128/119 certified, single zone `["8"]`,
  Mar 30/Nov 1, and every delta (apple/pear/cherry-sour marginal, pawpaw unsuitable, citrus split,
  berries, 847xx-only fence, NO isWarm #32 dep) match reality.
- `LATEST.txt`: SHA `d8e0a98e` matches `shasum -a 256 crops_data_final.json`. Accurate.
- Kickoff #39: instructions correct; only the informational canonical SHA is stale (M4).

---

## HONESTY ATTESTATION
No fabricated sources and no fabricated windows found. Every authored window/verdict traces to one of
the 8 registered USU T1 sub-ids (all present in the canonical `source_catalog`, URLs matching the
bible); every non-USU-table crop discloses its by-analogy/biology basis; and the `[250,450]` chill band
is explicitly labeled elevation-bracketed inference, not a measured figure.
