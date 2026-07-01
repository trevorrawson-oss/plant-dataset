# elderberry -- author-fresh PILOT notes (Claude Code lane, 2026-06-30)

Authored **elderberry** (slug `elderberry`, *Sambucus canadensis* / *S. nigra*) as a gold-standard
PERENNIAL by FILLING its shell, modeled STRUCTURALLY on the certified **blueberry** (archetype
`berries_woody`), refit for a large multi-stemmed SHRUB. READ-ONLY on canonical:
`crops_data_final.json` was never written (built by deep-copying the blueberry record from canonical
into scratch, then overwriting every value). The `berries_woody_gate.py` was NOT modified.

Output: `elderberry_crop.json` (compact, `separators=(",",":")`, `ensure_ascii=False`, no trailing
newline; byte-identical to a compact re-dump). 92 top-level keys, exact key parity with blueberry
(missing:[] extra:[]).

## THE HEADLINE: elderberry fits NEITHER berries_woody sub-form -- authored as the closest fit, mismatches SURFACED

`berries_woody_gate.py` A15 has two sub-forms, keyed on `cane_type`:
- **BUSH** (blueberry): `cane_type="not_applicable"`; `self_fertile` MUST be `False`; recommended_type
  enum `{northern_highbush, southern_highbush, rabbiteye}`.
- **CANE** (raspberry/blackberry): real `cane_type`; `self_fertile` a bool; enum `{summer_bearing, everbearing}`.

Elderberry is a large multi-stemmed **shrub** that is **partially self-fertile**, with cultivars
(Adams / York / Nova / Bob Gordon / Wyldewood / Ranch) that belong to NEITHER enum. It is closer to
BUSH (a crown-forming shrub, not a biennial-cane fruit), so it is authored as the **BUSH sub-form**
(`cane_type="not_applicable"`) with the honest biology left in place so the gate surfaces the gaps
rather than being tricked into silence.

### GATE RESULT
`python3 tools/whole_crop_gate.py elderberry <scratch>` -> **GATE: 21 VIOLATION(S)** (exit 1). ALL 21
are the two intended elderberry-sub-form gaps in **A15**; every other gate is clean. This is the
expected, honest outcome (the task said reaching GATE: PASS was NOT required; report the exact gaps).

The precise 21 remaining violations (A15 `berries_woody` structural cert):
1. **self_fertile (x1)** -- `self_fertile must be false (bush berry needs cross-pollination, the light
   model); got True`. Elderberry is authored `self_fertile=true` (the honest PARTIALLY-self-fertile
   biology; a lone plant sets some fruit, unlike self-incompatible rabbiteye). The BUSH branch demands
   `False`; the CANE branch would accept a bool. Elderberry sits BETWEEN the two, and the gate's binary
   bush=False / cane=bool model has no "partially self-fertile" state.
2. **recommended_type (x20, one per resolved cell)** -- `recommended_type 'american_elderberry' not in
   ['northern_highbush','rabbiteye','southern_highbush']`. Elderberry has ONE cultivated type
   (American elderberry) across all regions; it is NOT chill-type-gated the way blueberry is. No honest
   in-enum value exists, so `american_elderberry` is used and trips the enum on every cell. (The type
   COVERAGE invariant does NOT fire -- an out-of-enum type never enters the coverage set -- so these are
   clean enum-membership signals, not coverage noise.)

### A37 (calendar-coherence) -- reported separately, as instructed
```
A37. calendar coherence (growing-after-harvest + one-month harvest hole)
  calendar-coherence violations: 0
```
A37 is CLEAN (0). No harvest-hole (Bug-2) or impossible-growing (Bug-1) flagged; nothing hand-fixed.

## THE GATE-FIT MISMATCHES (elderberry sub-form gaps -- for a human to add an elderberry sub-form)
Three, exactly as the task called out, carried as non-blocking `open_findings` on the record:

1. **recommended_type enum** (HARD gate violation, x20). Fix: add an `american_elderberry` type (a
   BERRY_ELDER sub-form) to the A15 enum, or exempt a single-type berries_woody crop from the per-cell
   type-enum + coverage check.
2. **self_fertile expectation** (HARD gate violation, x1). Fix: the elderberry sub-form should accept a
   `self_fertile` that expresses PARTIAL self-fertility (true, with a strong cross-pollination
   recommendation) -- a third state between BUSH=False and CANE=bool-true.
3. **cane_type** (CONCEPTUAL, no gate violation). `cane_type="not_applicable"` routes elderberry to the
   closest (BUSH) branch, but it UNDERSTATES elderberry's real management: a perennial multi-stem shrub
   renewed by removing canes older than ~3 years (or cutting the whole clump to the ground). Neither
   `not_applicable` (bush crown, no canes) nor the biennial-cane enum `{summer_bearing, everbearing}`
   captures "perennial multi-stem cane renewal." An elderberry sub-form wants a third `cane_type`.

### Secondary conceptual mismatches (also carried as open_findings; NOT the 3 headline flags)
4. **chill-gating is a poor conceptual fit.** A15 mandates `gating_factors` contain `chill_hours` +
   `chill_hours_required` set, and A21 mandates a numeric per-variety `chill_hours_required`. Elderberry
   is NOT chill-type-gated -- one type everywhere, cultivars chosen by yield/season, not chill. It is
   authored with `gating_factors=["chill_hours"]`, crop `chill_hours_required=400`, and a **uniform
   nominal 400** on every variety (`chill_hours_range=null`) purely to satisfy the shape; chill is
   retained only as the real winter-dormancy requirement. This passes A15/A21 but is a modeling
   compromise flagged for the human sub-form (an elderberry sub-form could drop the chill signature).
5. **deciduous warm-cell artifact.** `leaf_habit="deciduous"` on EVERY cell (elderberry has no
   evergreen form), so the A16 deciduous deriver fills `dormant` months on the near-frost-free warm
   cells (fl z11, hawaii z11, warm CA z10). Biologically these are low-activity/semi-evergreen; a known
   artifact, identical class to the raspberry pilot's warm-cell dormancy. A16 is clean (stored==derived).
6. **warm-region marginality.** A31/A32 force all 10 regions with populated calendars, but elderberry is
   genuinely marginal in the hot low deserts and far tropics (z10-z11). Those cells carry best-effort
   windows with strong marginality language in the region prose; honest biology, not a fudge.

## POLLINATION MODEL (load-bearing)
**Partially self-fertile, plant 2 for good yield.** Authored `self_fertile=true`,
`pollination.self_fertile=true`, `pollination.needs_pollinizer=false`, `pollinizer_distance_ft=60`.
A single elderberry sets SOME fruit on its own, but yields are far higher with a second, DIFFERENT
cultivar blooming nearby (within ~60 ft) for cross-pollination. The flowers are wind-pollinated and
insect-visited. Every consumer surface (description, pollinator_notes, varieties note, notifications,
tips, failure_diagnostics "little or no fruit") drives the "plant 2 different cultivars" message. This
is the single biggest lever on yield. (Source: PSU "planting at least two will increase
cross-pollination... no more than 60 feet"; MU af1017.)

## COOK-BEFORE-EATING SAFETY (load-bearing)
Handled prominently and repeatedly, never buried:
- `description_*` leads with "always COOK the berries, because raw or unripe fruit, leaves, and stems
  are mildly toxic."
- `harvest_ready_*`, `storage.*`, the harvest growth_stage, the `harvest_and_cook` notification, and the
  harvest tip all repeat: cut whole ripe (deep purple-black) clusters, discard green/red unripe berries
  and ALL stems, and COOK (or freeze/dry) before eating.
- A dedicated `failure_diagnostics` entry, **"Feeling sick after eating the berries"**, explains the
  cyanogenic compounds in raw/unripe berries, leaves, stems, and seeds and the cook-to-destroy fix.
- `harvest_urgency="high"`. Elderflowers are noted as edible/usable (cordials, fritters).
(Source: PSU "Elderberries must not be consumed raw. Elderberry leaves, stems, and seeds contain a
cyanogenic glycoside called sambunigrin... Cooking the berries destroys the toxins.")

## OTHER KEY REFITS vs blueberry
- **NOT acid-loving.** pH preferred [5.5, 6.5], tolerated [5.5, 7.5]; no sulfur/peat/ericaceous/azalea
  content. Fertilizer is a balanced `10-10-10` (npk_ratio, npk_tag null), not acid/ammonium.
- **Wet-tolerant, moisture-loving, drought-SENSITIVE.** Streambank plant; tolerates clay and wet ground
  (rain-garden use); `drought_tolerance="low"`; the waterlogging weather-trigger is downgraded to LOW.
- **Fast + vigorous.** `years_to_first_harvest=[2,3]`, `years_to_full_production=[3,4]` (quicker than
  blueberry); `establishment_years=[1,2]`; yield ~10-15 lb per mature bush.
- **Very cold-hardy, native.** `hardiness_zone_min=3`; reliable temperate range z3-9
  (`reliable_fruit_zone` 3-9); `hardiness_zone_max=11` to cover the FL-native / tropical-highland edge
  (marginal, flagged).
- **Cane renewal is central** -- full `cane_management_*` prose (remove canes >~3 yr; cut clump to the
  ground to renew), plus the `dormant_prune` stage/tip/notification.
- **Pests few / easy** -- birds (high; inverting-cyme cultivars like Bob Gordon help), SWD + sap beetles,
  elder shoot/stem borers, aphids, Japanese beetles. **Diseases few** -- elderberry rust (alternate host
  sedges), powdery mildew, cane canker/dieback.
- **Varieties (6, all american_elderberry)** -- Adams, York, Nova, Bob Gordon, Wyldewood, Ranch; note
  drives "plant two DIFFERENT cultivars" (Adams+York, or Bob Gordon+Wyldewood).
- **Container** -- `container_ok=true` but `container_recommended=false`: a big suckering shrub best in
  the ground; only compact cultivars (Ranch) in a 20-25 gal pot.

## CALENDAR (A16) -- clean
Every cell's `calendar[]` is `derive_berry_woody_calendar("deciduous", {bloom, harvest})` from the
authored bloom/harvest windows (June-July bloom + late-summer ripening in the core, earlier in the
South). A16 = 0 (stored == derived). Bloom/harvest shift by region; northern_tier spreads across z3-7.

## SOURCES (catalogued T1 only, read live via WebFetch/WebSearch 2026-06-30 -- 3 ids)
- `psu_ext` -- Penn State "Elderberry in the Garden and the Kitchen" (culture, cross-pollination within
  60 ft, harvest, and the load-bearing cook-before-eating / cyanogenic-glycoside safety).
- `mu_ext` -- University of Missouri AF1017 "Growing and Marketing Elderberries in Missouri" (cultivars,
  ~4 ft in-row spacing, year-2 bearing, mid-to-late-summer harvest).
- `msu_ext` -- Michigan State "Growing elderberry in the garden" (6-12 ft habit, hardy to ~z4a, pH
  5.5-6.5, wet/clay tolerance, late-August ripening, annual/biannual cane pruning, SWD/borers/Japanese
  beetle, elderberry rust, no-fertilizer-at-planting).
All three are in `source_catalog` at `tier=T1` (gate E: 3 distinct ids, 0 uncatalogued, 0 non-T1; gate
F: 74 claim-bearing leaves, 0 anchoring gaps). Draft sourcing is intentionally narrow for a pilot.

### FLAGGED UNREADABLE (per instruction)
- **MSU E-2747 "Unusual Fruit Plants for Gardens in the North Central Region"**
  (`canr.msu.edu/uploads/files/e2747.pdf`) -- the PDF was binary-unparseable at WebFetch (same class as
  the raspberry-pilot OSU EC-1306 and blueberry AZ1585). NOT cited; cultivar detail leaned on the
  readable MU/PSU/MSU pages plus well-established cultivar facts.
- **NCSU** `content.ces.ncsu.edu/growing-elderberries-in-the-home-garden` -- HTTP 404 at fetch. NOT cited.
- **MU G6461** turned out to be tomatoes (mis-hit), and **MU G6005** HTML 404'd -- neither cited.

## VERIFICATION POSTURE
`verification_status.status="author_fresh_pilot"`, `launch_ready_core=false`,
`launch_ready_seasoned=false` (a DRAFT, not a cert). 6 `open_findings`, all `blocks_launch:false`
(the 3 headline gate-fit gaps + the 3 secondary conceptual mismatches). No em dashes / non-canonical
temps in consumer copy (gate C/D: 0/0). Canonical untouched; the gate is unmodified. Promoting into
canonical + adding the elderberry sub-form to `berries_woody_gate.py` are separate, Trevor-gated tasks.

## SCRATCH ARTIFACTS
- `elderberry_crop.json` -- the deliverable (compact).
- `elderberry_NOTES.md` -- this file.
- `build_elderberry*.py` (parts 1-4), `_eb_part{1,2,3}.json` (intermediate), `scratch_canon.json`
  (current canonical with elderberry spliced, for gating), `blueberry_full.json` (template dump).
