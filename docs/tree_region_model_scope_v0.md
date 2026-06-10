# Tree Region / Calendar Model -- Scope / Design-Lock Plan (v0 DRAFT)

**Status:** DESIGN + SPEC (proposal). No dataset writes yet. SHA unchanged (`621c79af`).
**Date:** 2026-06-10
**Lane:** Claude Code structural-design lane (same as schema 2.9). I design the shape + extend the deterministic builder + update the gate; claude.ai authors the per-region BIOLOGY later (Step 4+), per tree anchor.
**Roadmap slot:** peach Step 3.5 (FLAG 4) -- the tree region/calendar model. Peach is anchor 5, the first PERMANENT tree (Stone Fruit hub, archetype `deciduous_fruit_tree`, schema 2.9, canonical SHA `621c79af`).
**Designs against / siblings:** `region_primary_schema_shape_spec_v1_0` (the annual two-layer model this adapts), `schema_2_9_specification_v1_0` (§A4 perennial fields + the variety bloom calendar), `gold_standard_arc_checklist_v1_7` Step 5.5 (the `calendar_basis` branch + 13-state enum that gate this), `second_planting_structure_spec_v1_1`. Renderer target: `04-guides/apple-zone-6.html` (the 3-track tree Gantt + hardiness band + chill block + cross-pollination).

---

## 0. What this decides, and what it does NOT

**Decides this session (for Trevor to ratify, like 2.9):**
- What a region/zone cell MEANS for a permanent tree (Section 2-3), and why the annual `plantings[]` sowing-window model does not fit one.
- A new `calendar_basis` value and the gate branch behind it (Section 4).
- The tree region cell shape: the chill-adequacy layer, the suitability/hardiness verdict, the perennial phenology rule, and the zone-resolved render layer (Section 3 + 5).
- The `calendar[]` tree-state vocabulary and the one open enum question (`dormant`) (Section 6).
- How the shape feeds the apple-guide 3-track Gantt + hardiness band + chill block (Section 7).
- Ratification of the provisional `dormancy_window` / `pruning_window` month-band shape against this model (Section 8).
- What `build_region_shells.py` builds for a tree, test-first (Section 9).

**Does NOT do (out of scope, Phase 2 / per-anchor):**
- Author any biology: no chill-hours-delivered numbers, no suitability verdicts, no bloom/harvest dates, no `calendar[]` arrays. Step 3.5 builds the EMPTY, gated skeleton; Step 4+ (claude.ai) fills it from peach's own pomology sources.
- Touch the annual crops' region model. The 4 certified annual anchors (cherry/beefsteak/carrot/lettuce) stay byte-identical.
- Resolve FLAG 1 (rootstock `selection_basis`) -- deferred to apple (Section 10).
- Build the ZIP->region resolver, or the renderer itself.

---

## 1. Ground truth: the annual model, and why a tree breaks it

The annual region model (`region_primary_schema_shape_spec_v1_0`) is a **two-layer cut**:

- **Region-constant rule layer** -- `regions[r].plantings[]`: frost-anchored sowing rules, `{from: "last_frost", offset_days, window_days}`, authored once per region. "Transplant 7 days after last frost" holds for every zone in the region.
- **Zone-resolved render layer** -- `regions[r].resolved_by_zone[z]`: the rules materialized against each zone's frost date into human date strings + a 12-month `calendar[]` array.

This is correct for an annual because **an annual's defining event is a sowing window that recurs every year, anchored to frost.** The whole calendar is "when do I plant, when do I harvest, before the season closes."

**A permanent tree has no annual sowing window.** It is planted ONCE (bare-root, dormant, late winter), then it is permanent for 15-50 years. Running the annual model on peach produces a category error: the scaffold gave peach 10 region cells whose `plantings[]` expect a recurring `direct_sow`/`plant_out` frost window and whose `resolved_by_zone` cells expect per-season plant/harvest strings. Peach's `calendar_basis` is currently `frost_anchored` -- a wipe default that is simply wrong for a tree.

**What actually varies by region/zone for a permanent tree** is a different set of facts:

1. **Hardiness / suitability** -- does the tree *survive winter* here, and does it *fruit reliably* here? These are two different ranges (the apple guide's two-band hardiness strip: "Survives 3a-9b / Fruits reliably 3b-9a"). For peach the reliable-fruit band is narrow and bounded at BOTH ends: too cold = bud/wood kill + late-frost loss of the early blooms; too warm = not enough winter chill to break dormancy.
2. **Chill adequacy** -- does the region bank enough winter chill to set fruit, and *which varieties*? Peach's 8 recommended varieties span 400 chill hours (Florida King, very-early bloom) to 1,050 (Contender, late bloom). A region delivering ~400 chill hours fruits Florida King but never Contender; a region delivering ~1,000 fruits the high-chill set but a 400-hour variety planted there blooms too early and is frosted. **Region chill band -> which varieties fruit** is the single most tree-specific datum, and it has no analogue in the annual model.
3. **Phenology timing (absolute dates)** -- bloom, fruit development, harvest, dormancy, and dormant-pruning shift by region/latitude (a peach blooms in February on the Gulf, April in Michigan). The bloom ORDER (very-early -> very-late) is variety-intrinsic and region-stable; the absolute calendar position shifts by region. This is the one place the annual frost-resolution machinery still applies.
4. **The recurring cycle, once established** -- bloom -> fruit set -> harvest -> leaf drop -> winter dormancy/chill -> dormant prune, every year. This is the tree's `calendar[]`, and its states are bloom/growing/harvest/prune/dormant, not plant/indoors/heat-pause.

**The scaffold already anticipates this (the 2.9 pattern repeats).** Peach already carries, scaffolded-null at the crop level:
`hardiness_zone_min`, `hardiness_zone_max`, `reliable_fruit_zone_min`, `reliable_fruit_zone_max`, `hardiness_notes_seasoned`/`_beginner` -- exactly the apple two-band hardiness data. Plus the 2.9 perennial block (`chill_hours_range [200,1050]`, `pollination{self_fertile:true}`, `dormancy_window`, `pruning_window`, `establishment_years 3`, `rootstock_options[]`) and the 8-variety bloom calendar (`bloom_group`/`bloom_window_relative`/`chill_hours_required` per variety). **So this work is formalize + complete + populate-later, NOT invent** -- the same finding 2.9 made. What is missing is the REGION layer that turns crop hardiness + variety chill into a per-place verdict and a per-place calendar.

---

## 2. The core design: what a tree region cell means

A tree region cell keeps the annual model's **two-layer discipline** (region-constant rules vs zone-resolved render) and its **outer container** (region_id, region_label, zone_span, sources, region_notes_*) unchanged -- so the ZIP->region resolver, the region grid, and the gate's region walk all keep working. What changes is the INNER calendar model: the annual sowing-rule semantics are replaced by three tree sub-models.

| Layer | Annual | Tree |
|---|---|---|
| **Region-constant rule** (`plantings[]`) | recurring frost-anchored sowing windows + succession tracks | a SINGLE one-time establishment plant window (`track:"perennial"`) -- when to set a bare-root tree here |
| **Region-constant climate** (NEW) | n/a | `chill_hours_delivered [low,high]` -- the region's typical banked winter chill, which gates the variety set |
| **Zone-resolved render** (`resolved_by_zone[z]`) | plant/harvest date strings + 12-month `calendar[]` | a per-zone **suitability verdict** + per-zone **chill adequacy** + absolute **bloom / harvest / prune** dates + the tree `calendar[]` |

The cleanest framing: **for a tree, "region" answers *can I grow it here and which varieties*, and "zone" answers *exactly when it blooms, fruits, and goes dormant*.** That maps onto the existing region/zone split with no structural violence -- chill adequacy and suitability are region-grained (refined per zone), and the phenology dates are zone-resolved, exactly as frost-anchored dates are today.

A decisive property this buys us: **honest "does-not-grow-here" cells.** The annual model had to invent a planting window for every region; the `year_round` flag was a special-case patch for genuinely pauseless cells. The tree `suitability` verdict instead lets a cell say plainly `unsuitable` (Hawaii peach: zero chill, never fruits) or `survives_no_fruit` (zone 3 peach: the tree lives but the crop fails) without fabricating a calendar. The region grid stays truthful end to end.

---

## 3. The tree region cell shape (full)

Worked on peach `se_gulf`, with the cold-end `northern_tier` shown after. **Skeleton built at Step 3.5 (empty); values authored Step 4+.**

```jsonc
"se_gulf": {
  "region_id": "se_gulf",
  "region_label": "Southeast: Gulf",
  "zone_span": ["7b","8a","8b","9a"],
  "sources": ["clemson_hgic","ncsu_ext"],
  "anchoring_urls": { "clemson_hgic": {"url":"...","verified":"2026-06-10"} },

  // --- TREE region-constant climate layer (NEW; replaces nothing, adds the chill gate) ---
  "chill_hours_delivered": [650, 950],          // region's typical banked winter chill (NOAA/extension)
  "chill_basis_seasoned": "Piedmont/Gulf winters bank ~650-950 chill hours; high-chill varieties fruit reliably, very-low-chill types bloom too early and frost.",
  "chill_basis_beginner": "Winters here are cold enough for most peach varieties.",

  // --- TREE region-constant RULE layer (the establishment plant window; one entry, no succession) ---
  "plantings": [
    {
      "succession_id": 1,
      "label": "establishment",
      "track": "perennial",
      "plant_out": [                            // one-time, bare-root dormant, frost-relative
        { "label": "bare_root_dormant", "from": "last_frost", "offset_days": -42, "window_days": 42,
          "synthesis_note": null, "sources": [], "anchoring_urls": {}, "uscrn_validation": null }
      ],
      "bloom":   [ { "label": "primary", "from": "last_frost", "offset_days": -7,  "window_days": 21,
                     "sources": [], "anchoring_urls": {} } ],   // bloom ~ around last frost (frost RISK lives here)
      "harvest_start": [ { "label": "primary", "from": "bloom_start", "offset_days": 90,  "sources": [], "anchoring_urls": {} } ],
      "harvest_end":   [ { "label": "primary", "from": "bloom_start", "offset_days": 135, "sources": [], "anchoring_urls": {} } ],
      "anchoring_urls": {}
    }
  ],
  "plantings_provenance": null,

  // --- zone-resolved render layer ---
  "resolved_by_zone": {
    "8a": {
      "suitability": "fruits_reliably",         // fruits_reliably | marginal | survives_no_fruit | unsuitable
      "suitability_note_seasoned": "Reliable peach country; choose 600-900 chill-hour varieties.",
      "suitability_note_beginner": "Peaches grow well here.",
      "chill_hours_delivered": [700, 900],      // zone refinement of the region band
      "plant_dates": "Dec - Feb (dormant, bare-root)",
      "bloom_dates": "Mar 1 - Mar 20",          // absolute, resolved from frost
      "harvest_dates": "Jun 1 - Jul 15",
      "calendar": ["dormant","dormant","prune","bloom","growing","harvest","harvest","growing","care","dormant","dormant","dormant"],
      "frost_risk_note_seasoned": "Late-frost loss possible on very-early bloomers; favor mid-to-late bloom groups.",
      "resolved_from": { "last_frost": "Mar 8", "first_frost": "Nov 20", "chill_hours": [700,900] },
      "resolution_method": "perennial_precompute"
    }
  },
  "region_notes_seasoned": null,
  "region_notes_beginner": null
}
```

`northern_tier` (cold half) is the same shape, and is where `suitability` earns its keep:

```jsonc
"northern_tier": {
  "region_id": "northern_tier", "region_label": "Northern Tier",
  "zone_span": ["4b","5","6","7"],
  "chill_hours_delivered": [1000, 1500],
  "plantings": [ { "track":"perennial", "label":"establishment", "plant_out":[{"from":"last_frost","offset_days":-30,"window_days":30, ...}], "bloom":[...], "harvest_start":[...], "harvest_end":[...] } ],
  "resolved_by_zone": {
    "4":  { "suitability": "survives_no_fruit", "suitability_note_seasoned": "Hardy varieties (Reliance, Contender) survive, but late frost and -20F bud kill make a crop unreliable.", "calendar": ["dormant","dormant","dormant","prune","bloom","growing","growing","harvest","care","dormant","dormant","dormant"], ... },
    "5":  { "suitability": "marginal",         ... },
    "6":  { "suitability": "fruits_reliably",  ... },
    "7":  { "suitability": "fruits_reliably",  ... }
  },
  ...
}
```

(And the cleanest demonstration of the model's honesty: `hawaii_tropical` resolves to `suitability: "unsuitable"`, `chill_hours_delivered: [0,150]`, empty `calendar`, `suitability_note_beginner: "Peaches need a cold winter to fruit; they will not produce in Hawaii."` -- no fabricated window, no `year_round` patch.)

### 3a. The three new sub-models, precisely

1. **Chill adequacy** -- `chill_hours_delivered [low,high]` at region level, refined per zone. The RENDERER (not the cell) intersects this band with each variety's `chill_hours_required` to produce the "which varieties fruit here" answer + the apple-guide chill note ("low-chill varieties wasted here"). The cell stays a *data source*, not precomputed analysis -- same discipline as `resolved_by_zone` holding render strings, not logic. A short `chill_basis_*` prose pair carries the human explanation.

2. **Suitability / hardiness verdict** -- a per-zone `suitability` enum + `suitability_note_*`. Derived (by the author at Step 4, attested to sources) from: the crop-level `hardiness_zone_min/max` (survives) and `reliable_fruit_zone_min/max` (fruits) -- *which already exist scaffolded-null* -- intersected with the zone and the chill verdict. Four states:
   - `fruits_reliably` -- survives + chill met + low frost risk.
   - `marginal` -- fruits in good years; chill borderline or late-frost-exposed.
   - `survives_no_fruit` -- tree lives but the crop is unreliable (too cold, or too warm/no-chill at the warm edge).
   - `unsuitable` -- does not survive or never sets fruit (Hawaii).

3. **Phenology rule + resolution** -- the recurring cycle. The region-constant `plantings[0]` carries the establishment plant window + a `bloom[]` rule + `harvest_start/end[]` rules. Two new `from` anchors extend the existing offset vocabulary:
   - `bloom` anchored to `last_frost` (bloom near last frost is the frost-risk story, and it is what the resolver already has frost dates for).
   - `harvest_start/end` anchored to a NEW `bloom_start` anchor (fruit develops ~90-135 days after bloom). This keeps harvest tied to the biological driver (bloom), not to a sowing date the tree does not have.
   The zone layer resolves these to absolute `bloom_dates` / `harvest_dates` / `plant_dates` + the `calendar[]`, with `resolved_from` recording the frost dates AND chill band used (auditable, re-derivable -- same contract as the annual `resolved_from`).

### 3b. Why reuse `plantings[]` for the one-time plant window

It would be tempting to drop `plantings[]` entirely for a tree. Keeping a single `track:"perennial"` establishment entry instead is deliberate:
- It feeds the **"Plant" track** of the 3-track Gantt with the same field the annual renderer already reads -- the renderer does not special-case trees for the plant row.
- It gives the gate's region walk a non-null `plantings` rule layer to check (the walk currently fails a stub/missing/null-track `plantings`); the perennial entry satisfies it structurally.
- `bloom[]` + `harvest_start/end[]` on the same entry feed the **Bloom** and **Harvest** tracks, so all three Gantt rows come from one uniform place for both annual and tree.

What is PROHIBITED on a tree's `plantings[]`: any `track:"succession"` / `track:"second_planting"` entry, any `start_indoors`/`direct_sow` (a bare-root tree is neither). Exactly one establishment entry. The gate enforces this (Section 5).

---

## 4. `calendar_basis` -- new value `perennial_chill_gated`

`calendar_basis` is a CROP-level field; the Step 5.5 gate branches on it to decide which calendar criteria apply. Today's three values: `frost_anchored` (109 crops), `non_seasonal_indoor` (13), `generic_placeholder` (1). Peach is wrongly `frost_anchored` (wipe default).

**Recommendation: add `perennial_chill_gated`, and set peach to it.** It is the structural marker that makes the gate stop demanding a recurring sowing window and start demanding the tree shape (suitability + chill + the perennial establishment entry). Rationale for a new basis rather than overloading `frost_anchored`:
- The frost-anchored branch *requires* `plantings length >= 1` of recurring sowing windows, succession-track coherence, and heat/cold-pause-as-season-gap semantics. None hold for a tree.
- Frost resolution is still ON (bloom/harvest/plant ARE frost-anchored), unlike `non_seasonal_indoor` which suppresses it -- so a tree is genuinely a third mode, not either existing one.

**Scope of the name (Trevor decision, Section 10):** `perennial_chill_gated` is accurate for peach and the entire near-term tree set -- all deciduous Stone Fruit + Pome + most woody berries are chill-requiring. Evergreen/citrus (lemon, orange) is perennial but *hardiness-gated, not chill-gated* (chill ~ 0; frost-tenderness is the limiter). I recommend we introduce `perennial_chill_gated` now and DEFER the evergreen variant to the citrus anchor (it will be either a sibling `perennial_tender` basis or a `suitability.gating_factor` field) -- the same "defer until the second data point" discipline as FLAG 1. This keeps peach moving without over-designing for a crop we have not reached.

---

## 5. Gate updates (`whole_crop_gate.py` + Step 5.5)

The gate gains a `perennial_chill_gated` branch, parallel to the existing `non_seasonal_indoor` branch:

- **`plantings[]` rule:** exactly ONE entry, `track:"perennial"`, `label:"establishment"`; no succession/second_planting entries; no `start_indoors`/`direct_sow`. (Replaces the frost-anchored ">=1 sowing window + succession coherence" requirement.) Add `"perennial"` to the recognized `track` vocabulary so the null-track check passes it.
- **`calendar[]` vocabulary:** tree states only (Section 6). Succession/heat-pause coherence checks are N/A.
- **NEW required on each resolved cell:** `suitability` in the 4-value enum, and `chill_hours_delivered` present (may be `[0,n]` for unsuitable). A `frost_anchored`-style plant/harvest-window check is replaced by a bloom/harvest-date presence check at fill time (Step 11), not shape time (Step 3.5).
- **Frost resolution:** stays ON (not suppressed).
- `register_completeness_gate`: rule the new prose fields -- `chill_basis_*`, `suitability_note_*`, `frost_risk_note_seasoned` as CORE-PROSE pairs (seasoned + beginner where a beginner line is warranted; `frost_risk_note` is seasoned-only). These follow the existing `_seasoned`/`_beginner` suffix machinery, so the dual-voice coverage gate auto-covers them.

At Step 3.5 (shape) the gate asserts the skeleton is present-and-empty in the right shape; at Step 11 (fill) the same gate asserts the values are populated -- the two-callsite model from v1.5.

---

## 6. The `calendar[]` tree vocabulary -- the one open enum question

The 13-state enum (checklist Step 5.5) is: `wait, indoors, plant, growing, harvest, late, bloom, start, prune, care, cold_pause, heat_pause, season_over`. It already reserves **`bloom`, `prune`, `care`** -- these were put there for exactly this tree case. A peach year uses: `bloom` (spring), `growing` (fruit development), `harvest`, `prune` (dormant prune), `care` (post-harvest), and the winter dormant months.

**The gap: there is no `dormant` state.** A deciduous tree's winter dormancy is a real, meaningful, multi-month state (leafless, banking chill -- the chill it needs for *next* year's fruit). The nearest existing token is `cold_pause`, but that means "a growing crop paused by cold between two sowing windows, will resume the same season" -- semantically wrong for tree dormancy, and the renderer draws them differently (a dormancy band with a prune marker vs a gap between annual windows).

**Recommendation: add `dormant` (14-state enum).** It is additive (no existing crop uses it), it lets the tree `calendar[]` render winter honestly, and it keeps `cold_pause` meaning what it means for annuals. Month-collision rule (one state per month): a dormant month that is also the prune window renders `prune` (the actionable state); other dormant months render `dormant`. *Alternative if Trevor prefers no enum change: reuse `cold_pause` for dormant months* -- cheaper, but conflates two genuinely different renderer states and muddies the gate. I recommend `dormant`.

---

## 7. How it feeds the apple-guide renderer (the consumer is the spec)

`04-guides/apple-zone-6.html` is the 3-track tree guide this model exists to feed. Field-by-field:

| Renderer element (apple guide) | Fed by |
|---|---|
| **Hardiness band** ("Survives 3a-9b / Fruits reliably 3b-9a", zone marker) | crop-level `hardiness_zone_min/max` + `reliable_fruit_zone_min/max`; the user's zone cell's `suitability` colors the marker |
| **Chill block** ("Varies by variety 200-1,200 hrs" + "Zone 6 delivers 1,000+" + "low-chill wasted here") | crop `chill_hours_range` (the headline) + the region/zone `chill_hours_delivered` (the "your winters deliver X") + `chill_basis_*` (the note); renderer intersects delivered-band x variety `chill_hours_required` for the per-variety lines |
| **Bloom timing & cross-pollination Gantt** (per-variety very-early->very-late bars; "Apr 10-20" legend; best pairs) | variety `bloom_group`/`bloom_window_relative`/`bloom_duration_days` (intrinsic, already authored) positioned into the region/zone `bloom_dates` absolute window (the scale); crop `pollination` block (peach self_fertile -> the section degrades to "no second tree needed", the inverse of apple) |
| **Planting calendar** (3-track Plant / Bloom / Harvest Gantt) | the zone cell `calendar[]` (Plant from `plantings[0].plant_out`, Bloom from `bloom_dates`, Harvest from `harvest_dates`) |
| **Subzone table** (last frost / first fall / min temp per a/b) | `resolved_from` frost dates + the chill band; the renderer's existing subzone machinery |
| **Growing journey** (Planting -> Y1 establishment -> Scaffold -> Annual winter prune -> First harvest) | `tips_by_stage` (dormancy/dormant_prune/establishment, 2.9) + `dormancy_window`/`pruning_window` + `establishment_years` |

The crop self_fertility flips one section: apple's whole cross-pollination requirement becomes, for peach, "self-fertile -- a single tree fruits" with the bloom Gantt retained only as a variety-comparison/spread view. The `pollination` block already drives this (peach `self_fertile:true, needs_pollinizer:false`).

---

## 8. Ratifying `dormancy_window` / `pruning_window` (the fold-in item)

claude.ai authored these provisionally as month-bands: `dormancy_window {start_month:12, end_month:2}`, `pruning_window {start_month:2, end_month:3}`.

**Ratification verdict: keep the month-band SHAPE at the crop level; the region `calendar[]` resolves the actual months per place.** Reasoning:
- They are correct as a **coarse crop-level descriptor** -- the at-a-glance "dormant in winter, prune in late winter," the same altitude as crop-level `bloom_duration_days: 10`. A beginner line ("prune every winter while the tree is bare") reads off this directly.
- The PER-PLACE truth (a Gulf peach prunes in Dec-Jan; a Michigan peach in Mar) lives in the zone `calendar[]` `prune`/`dormant` months, resolved from frost -- *not* in the crop band. So the crop band is a default/summary; the calendar is the resolved layer. This mirrors crop `bloom_duration_days` (default) vs region `bloom_dates` (resolved).
- No reshape to frost-relative offsets is needed: pruning timing is forgiving (anywhere in late dormancy), the month-band is faithful to how extension sources state it, and claude.ai already authored it. Reshaping would be churn for no rendering gain. **Shape STANDS.**

One amendment to record: tag both as northern-hemisphere defaults (a `hemisphere` assumption note), since the resolved calendar is what localizes them. Low-friction; can ride the Step 4 fill.

---

## 9. What Step 3.5 builds: `build_region_shells.py` tree branch (test-first)

Phase 2 (AFTER Trevor ratifies this doc). A pure transform, mutating the crop dict in place, no biology invented -- same contract as the annual builder.

- **Detection:** branch to the tree path when `calendar_basis == "perennial_chill_gated"` OR (`lifecycle == "permanent"` and archetype is woody). (The builder also SETS `calendar_basis` from the `frost_anchored` wipe-default to `perennial_chill_gated` -- the one crop-level flip that makes the gate branch.)
- **Per region cell:** keep the container keys; resolve the `California -- X` -> `California: X` dash (existing logic); build the perennial RULE skeleton -- one `{succession_id:1, label:"establishment", track:"perennial", plant_out:[], bloom:[], harvest_start:[], harvest_end:[], anchoring_urls:{}}` entry; add `chill_hours_delivered: []`, `chill_basis_seasoned/_beginner: null`; ensure `region_notes_seasoned/_beginner` keys present (null OK).
- **Per resolved_by_zone cell:** replace the annual cell keys with the tree cell keys -- `suitability:null`, `suitability_note_seasoned/_beginner:null`, `chill_hours_delivered:[]`, `plant_dates/bloom_dates/harvest_dates:null`, `calendar:[]`, `frost_risk_note_seasoned:null`, `resolved_from:{}`, `resolution_method:null`. Strip the annual-only leftovers (`start_indoors`, `succession_*`, `heat_pause`, `lifted_from_zone`, nested `plantings`).
- **northern_tier:** peach is author-fresh (wiped shell, empty `zones{}`), so `_north_should_promote` already returns False -> NT goes through the from-scratch path like any region. The tree branch treats NT identically (it is just the cold-zone cell); zone keys stay as scaffolded -- the per-zone `suitability` verdict, not zone-trimming, carries "no reliable crop in zone 3-4." (Zone-span trimming is a Step 4 biology call, deliberately NOT a shape call.)
- **Idempotent + COMPACT** serialization; tests first in `test_build_region_shells.py` (extend the existing harness): tree-detection, one-establishment-entry invariant, tree cell key-set, no annual leftovers, NT-from-scratch, re-run stability.

Output: peach's 10 region cells at tree shape, EMPTY, gate-green for shape, PENDING fill. Released exactly like the annual Step 3.5 (apply wrapper owns SHA; promote; regenerate CURRENT_STATE; append STATE_HISTORY).

---

## 10. Decisions (for Trevor to ratify) + Deferred

**Decisions this doc asks Trevor to ratify (like 2.9's "go ahead and build it"):**
1. **`calendar_basis = perennial_chill_gated`** (new value), peach set to it; evergreen/citrus variant DEFERRED to the lemon anchor. *(Recommend yes.)*
2. **Add `dormant` to the calendar enum (13 -> 14 states).** *(Recommend yes; alternative is reuse `cold_pause`.)*
3. **Tree region cell shape** as Section 3 -- the chill-adequacy layer (`chill_hours_delivered` + `chill_basis_*`), the 4-value `suitability` verdict, the single `track:"perennial"` establishment entry with `bloom`/`harvest` rules, and the `bloom_start` harvest anchor. *(Recommend as specified.)*
4. **`dormancy_window`/`pruning_window` month-band shape STANDS** at crop level; calendar resolves per place (Section 8). *(Recommend yes.)*

**Deferred / folded (tracked, not built here):**
- **FLAG 1 (rootstock `selection_basis`):** per-archetype enum (`size` for pome / `soil_pest_tolerance` for stone). Peach rootstocks do NOT control size; chosen for soil/nematode tolerance. Accepted claude.ai's pragmatic shape (size_class="standard" x4, choose-by axis in `what_to_ask_nursery`). DEFER until apple supplies the pome data point + a renderer consumer. Untouched by this region model.
- **Evergreen/citrus `calendar_basis`** variant -- decided at the lemon anchor.
- **ZIP->region resolver, renderer build** -- engineering items, unblocked by this shape but separate.

---

## 11. Sequencing

1. **Ratify this doc** (Trevor) -> promote to `05-methodology/current/tree_region_model_spec_v1_0.md` + PK; fold the `calendar_basis` value + `dormant` state + the perennial gate branch into the v1.7 checklist Step 5.5 (a v1.8 amendment) + the calendar-model enum.
2. **Build (Phase 2):** extend `build_region_shells.py` (test-first) + the `whole_crop_gate.py` perennial branch + `register_completeness_gate` rulings; set peach `calendar_basis`; run the shells; release per protocol #6 (whole_crop_gate, release_verify, cross-check, promote, regenerate state, append history).
3. **Then Step 4+ (claude.ai):** author peach's per-region `chill_hours_delivered`, `suitability` verdicts, bloom/harvest dates, `calendar[]` arrays, and the prose pairs from peach's pomology sources; fill the crop-level `hardiness_zone_*`/`reliable_fruit_zone_*`/`hardiness_notes_*`. The shape this doc locks is what they fill.

---

*End of tree region / calendar model scope v0. Adapts `region_primary_schema_shape_spec_v1_0` for the permanent-tree case; locks the shape Step 4 fills; the build + gate are Phase 2, SHA-gated, after ratification.*
