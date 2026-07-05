# Remaining GS anchors -- roadmap (walk through next week)

**Created 2026-07-02.** A standing list of what is still needed to keep scaling gold-standard (GS)
certified anchors, so nothing is forgotten between sessions. Read alongside CURRENT_STATE.md (live
state) and each batch's MORNING_REPORT (per-crop detail).

## Position snapshot (2026-07-02, canonical `f7ab0ac2`)
- **80 certified anchors.**
- **34 drafts staged, awaiting the certify session** (the near-term anchor pipeline):
  - 20 in `_handoff/batch_2026-07-02/` (edibles + herbs).
  - 14 in the same batch dir (7 microgreens + 7 companion flowers, authored 2026-07-02 evening).
- **After those 34 certify -> ~114 certified.** Then **11 shells remain** (10 design-cases + 1 to retire).

---

## RULINGS 2026-07-05 (Trevor, from the CROP_REVIEW_2026-07-05 walk-through)

**Strategic direction (drives sequencing):** get the app up for TESTERS by AUGUST. Focus = fall/winter
crops. Priority order: (1) certify these 34 -> 114, (2) add new DATAPOINTS / fields to the 114 (Trevor
has new fields to add BEFORE more crops), (3) THEN the new archetypes. Most archetypes WAIT until the
114 is finalized -- the Tier-2 design work below is explicitly deferred behind certify + field-addition.

1. **Cucumbers -> keep `cucumber` as the generic parent** alongside slicing/pickling/english (the
   tomato-split precedent). Certify all four. At the VARIETY pass, flag every questionable parent-vs-type
   crop for a how-to-organize review (see Variety-pass flags).
2. **Herbaceous-perennial lane -> RATIFIED now.** mint/chives/lemongrass + bee-balm/echinacea certify in
   their current lanes as-is (they model cleanly on existing tokens; "divide" / crown-maintenance is
   prose today, NOT a calendar token, so nothing blocks certifying). ALSO add `herbaceous_perennial` to
   the new-archetypes list (Tier 2A) -- that archetype is where divide / cut-back / crown-rejuvenation
   calendar semantics get designed.
3. **`collard-greens` -> RETIRE the shell** at a certify promote, AND give certified `collards` the
   display alias `name = "Collards (Collard Greens)"` (the exact `lettuce-leaf` = "Lettuce (Leaf)" pattern).
4. **artichoke + asparagus + the other design-cases -> stay DEFERRED** and go on the new-archetypes list
   (they are popular crops; get them right, not fast). = Tier 2A/2B/2C/2D below.
5. **Roster-wide spelled-degrees cleanup + gate hardening -> AFTER certifying to 114**, not now.
   (heirloom-tomato already normalized; the certified tomatoes + `green-beans-bush` still owe it.)

**Heirloom-tomato (Decision 5):** KEEP as a parent now; "heirloom" spans many types, so the specific
heirlooms become a VARIETY picker under the parent (same parent-vs-type shape as the cucumbers). The
parent record's numbers are an honest representative composite (OP, indeterminate, diverse) -- flag it
for the variety pass.

**New-archetypes list (deferred behind certify + field-addition):**
- `herbaceous_perennial` (Ruling 2 + artichoke/asparagus) -- Tier 2A
- `cultivated_fungus` (5 mushrooms) -- Tier 2D
- subtropical-evergreen-tree stretch refits (avocado A/B flowering; olive chill-flowering) -- Tier 2B
- warm-season block-planted grass (sweet-corn) -- Tier 2C

**Variety-pass flags (revisit when we break into varieties):**
- the cucumbers (parent `cucumber` vs slicing/pickling/english market-types)
- heirloom-tomato (many heirloom types -> variety picker)
- PRINCIPLE: at the variety break, flag ALL questionable parent-vs-type / many-variety crops for a
  how-to-organize review before expanding them.

---

## TIER 1 -- Certify the 34 staged drafts (fastest path to +34 anchors, NO new authoring)

These are already authored, gate-clean, and byte-spliceable. They just need the certify pass
(per-crop source-truth review -> ruling -> promote), in family waves, exactly as 50 -> 80 went. The
watch-items are enumerated in the two MORNING_REPORTs; the load-bearing ones:

- **Spelled-degrees cleanup (batch 20):** the certified tomatoes + `green-beans-bush` carry spelled
  "degrees F" in consumer prose the gate C/D scan misses; heirloom-tomato was normalized, the certified
  crops still owe it. Fold a roster-wide `degrees F`->`°F` pass + gate hardening into the certify work.
- **Perennial-herb lane ratify:** mint / chives / lemongrass are hardy perennials modeled in the
  `frost_anchored culinary_herb` lane (perennial=true, succession suitable=false). Each filed an
  open_finding asking Trevor to ratify the lane (or trigger the Tier-2A archetype below).
- **Cucumber parent-vs-type:** slicing/pickling/english-cucumber vs the generic certified `cucumber`
  (same species) -- rule whether the generic stays a parent alongside the market types.
- **Citrus:** re-verify against `--ref orange-navel` (not the default annual `lettuce-leaf`) to clear
  the benign tree-vs-annual-reference release_verify artifact.
- **Honesty boundaries to sample:** grapefruit-drug interaction (flagged, not asserted), fava favism
  (T1-sourced), habanero Scoville (triple-sourced), sweet-potato correctly dropped nightshade
  greening/solanine. `rhs` (UK) is catalogued T1 and used by sage + fava -- consider a source sample.
- **Catalog admissions:** several crop-specific T1 pubs were folded onto existing catalog ids
  (habanero CV130/CR706, mandarin CH116/CH159, lime CH092/CH093, sweet-potato Clemson-1322/UGA-C1014);
  admit dedicated ids at promote if wanted.

---

## TIER 2 -- Design-then-author (the 10 remaining shells; each needs a decision BEFORE a template fill)

### 2A. Herbaceous-perennial crops (2): `artichoke`, `asparagus`
- **Blocker:** no clean template. Strawberry is the only certified herbaceous perennial, but its
  `berries_herbaceous` gate (A10/A11) is fruit-fitted (grown_as + renovation tokens).
- **Work:** design a herbaceous-perennial-CROP treatment -- either additively generalize
  `perennial_herbaceous` for a leafy/spear/bud crop, or a small new archetype. Refit crown biology:
  asparagus = long-lived crown bed (15-20 yr), spear harvest window then fern, dioecious/all-male
  hybrids; artichoke = vernalization-to-bud, crown division, annual-vs-perennial by region.
- **Ties to:** the mint/chives/lemongrass "perennial-in-lane" decision (Tier-1). Settle the archetype
  question once for all hardy herbaceous perennials. Same "2nd archetype member over-fits the single
  certified example's gate" pattern that elderberry surfaced -- expect additive gate generalization.

### 2B. Subtropical evergreen trees (2): `avocado`, `olive`
- **Blocker:** deliberate stretch refits, not clean fills (evergreen-tree structure exists via
  orange-navel/lemon, but the reproductive biology is novel).
- **avocado** <- orange-navel (evergreen tree) + a NEW pollination model: A/B flowering-type
  (synchronous dichogamy, plant complementary types), strong alternate/biennial bearing, more
  cold-tender than citrus, high-fat fruit that ripens off-tree. The A/B flowering is the design crux.
- **olive** <- fig / orange-navel: chill-INFLUENCED flowering (needs winter cool to flower -- unusual
  for an evergreen), biennial bearing, oil-vs-table use split, very long-lived, self-fertile-ish but
  better with a pollenizer. Pin pollination under A38.

### 2C. Warm-season block-planted grass (1): `sweet-corn`
- **Blocker:** no close template. Wind-pollinated so it must be BLOCK-planted (not rows) for kernel
  fill; heavy nitrogen feeder; ear-fill timing; su/se/sh2 sugary-gene types affect isolation +
  harvest; relay/succession planting for continuous harvest.
- **Approach:** warm-season `frost_anchored`; likely a fresh archetype or a heavy refit off a warm
  annual. Decide the template/archetype first.

### 2D. Cultivated mushrooms (5): `button-mushroom`, `oyster-mushroom`, `shiitake-mushroom`, `lions-mane-mushroom`, `wine-cap-mushroom`
- **Blocker (biggest single design lift):** needs a WHOLE NEW archetype. Fungi are not plants -- no
  planting calendar, no sun/soil/frost, no seed. The model is spawn + substrate + colonization ->
  fruiting/flush cycle driven by temperature / humidity / fresh-air (CO2) / light triggers, on
  different substrates per species (button = composted manure/casing; oyster = straw/sawdust; shiitake
  + lions-mane = supplemented hardwood sawdust or logs; wine-cap = wood chips outdoors).
- **Work:** design a "cultivated fungus" archetype (fields: substrate, spawn type, colonization time,
  fruiting conditions, flush cadence, indoor/log/outdoor-bed method) + its gate (TDD, RED-before-GREEN),
  the way `berries_woody` / `woody_ornamental` / `non_seasonal_indoor` were built. THEN author all 5
  off it in one fan-out. `microgreens-mix` is indoor but a totally different (seed->greens) model, not
  a usable template.
- Note the FOOD-SAFETY honesty bar (wild-lookalike cautions, cook-before-eating) like elderberry's.

---

## TIER 3 -- Cleanup (not new anchors)
- **`collard-greens`: RETIRE** (Ruling 3, 2026-07-05). Empty shell duplicating certified `collards`
  (same species, no distinction) -- the `beetroot`->`beet` precedent. A canonical edit (drop the slug)
  AND set certified `collards` `name = "Collards (Collard Greens)"` (the `lettuce-leaf` = "Lettuce
  (Leaf)" alias pattern, so the common name is still searchable). Gated on Trevor, done at a certify
  promote. Not an anchor to build.

## Also owed (quality, tracked elsewhere -- not new anchors)
- URL-liveness sweep (post-123): tomato B577 / null-URL sdsu, yellow iastate /encyclopedia 404,
  honeydew log 404, celery tamu http/https redirect loop, etc.
- D8 backed `heat_pause` for melons/peppers at the variety-delta pass.
- Cross-crop field-addition arc (deferred to a stable/complete roster -- never mid-cert).

---

## Suggested sequence for next week
1. **Certify the 34 staged drafts** in family waves (biggest, fastest anchor gain: 80 -> ~114). Roll
   the spelled-degrees cleanup + gate hardening into it.
2. **Retire collard-greens** during one of those promotes.
3. **Design pass 2A** (herbaceous-perennial archetype) -- unlocks artichoke + asparagus AND settles the
   mint/chives/lemongrass lane question in one go.
4. **Design pass 2D** (cultivated-fungus archetype) -- unlocks all 5 mushrooms.
5. **Author 2B + 2C** (avocado, olive, sweet-corn) as deliberate stretch refits once their
   pollination/planting models are decided.
