# fig -- author-fresh perennial fill NOTES (2026-06-30)

**Output:** `fig_crop.json` (compact, 152,264 bytes, 86 top-level keys) modeled on certified **peach**
(deciduous_fruit_tree structure), heavily refit for *Ficus carica* (Moraceae).
Status `author_fresh_pilot`; `launch_ready_core`/`launch_ready_seasoned` both false.
Canonical `crops_data_final.json` was **READ-ONLY** the whole session (SHA `84321950...` unchanged).

## The four refits (how fig departs from peach)

### 1. Pollination = NONE (parthenocarpic)
- `self_fertile: true`; `pollination.needs_pollinizer: false`; `pollinizer_distance_ft: null`.
- All prose leads with parthenocarpy: common home figs set + ripen fruit with **no pollination at
  all** (female-only flowers hidden inside the fruit -> a fig shows no visible bloom). Smyrna /
  San Pedro / caprifig types need the fig wasp (*Blastophaga psenes*) and are called out as an aside
  as NOT for home gardens. Recommended varieties are all common types: Celeste, Brown Turkey,
  Chicago Hardy, Black Mission, Kadota, LSU Purple.
- The "bloom" token in the derived calendar is honestly framed as **leaf-out / breba set**, not a
  showy bloom (`bloom_time_*` prose says so explicitly). The deciduous_fruit_tree calendar model
  requires a bloom-month anchor to derive `calendar[]`; that anchor is leaf-out here.

### 2. LOW chill (~100h) -- warm regions WELL-SUITED (the OPPOSITE of cherry)
- `chill_hours_range: [100, 300]`; every variety `chill_hours_required: 100` (UF/IFAS: figs "do not
  require more than 100 hours" below 45F). Crop-level `chill_hours_required: null` (variety-level
  carries the numbers, matching peach).
- Kept `calendar_basis: "perennial_chill_gated"` per the task; `gating_factors` left UNSET so
  perennial_gate defaults to `[chill_hours, cold_hardiness]` (A3 C2 requires chill_hours present for
  this basis). Because fig's chill floor (100) is met almost everywhere, I **avoided
  `survives_no_fruit` cells entirely** -> the chill-Goldilocks split never bites. Cells are only
  `fruits_reliably` / `marginal` (carry calendars) or `unsuitable` (empty).
- Showcase of the refit: **ca_desert z9/z10 and low_desert_az z9 = `fruits_reliably`** for fig,
  exactly where certified peach is chill-limited `survives_no_fruit` / `marginal`. The chill_basis
  prose in every region states chill is a non-issue and cold/heat is the real story.

### 3. Own-root, from cuttings (no rootstock system)
- `recommended_rootstock: "Own-root (from cuttings)"`; `rootstock_selection_basis: "own_root"`;
  `recommended_rootstock_note` explains figs are not grafted, so there is no graft union and no
  rootstock size/disease selection.
- `rootstock_options` carries ONE honest own-root entry (container_suitable true, 20 gal) whose
  traits prose explains size is managed by pruning/variety/container, and that the one soil-pest
  caveat (root-knot nematode) has **no resistant rootstock to fall back on** -- a nematode-free,
  well-drained site is the substitute for rootstock choice.
- `start_method.notes` refit: no graft union to keep above grade; you can plant slightly DEEPER to
  build a multi-stem bush (the dieback-recovery form).

### 4. COLD-tender -- hardiness prose LEADS with it
- `hardiness_notes_*` open on cold: dormant wood hardy only to ~**15°F to 20°F**; sustained lows
  below that kill the top (roots hardier, usually resprout). The in-ground map: **z7-10 in ground,
  z6 with heavy mulch/wrap, z3-5 container-overwintered-indoors.**
- `hardiness_zone_min: 6`, `hardiness_zone_max: 11`, `reliable_fruit_zone_min: 7`,
  `reliable_fruit_zone_max: 10`.
- Suitability map: northern_tier z3/z4 = **unsuitable** (empty calendar), z5 = marginal (heavy
  protection / container), z6 = marginal (protected, cold-hardy varieties), z7 = fruits_reliably
  (cool edge). All z8-z10 = fruits_reliably. z11 (fl_peninsula + hawaii) = **marginal** (humid-tropic
  fig rust / souring / nematodes + weak dormancy).
- Container culture is elevated (cold-tender -> containers): `container_ok: true`,
  `min_pot_gallons: 15` (UMD), `overwintering.applicable: true`, approach = unheated garage/shed.

Other biology: `years_to_first_harvest [1,2]`, full [3,5], `establishment_years 2`;
`harvest_urgency "high"` (figs do NOT ripen off the plant, spoil in 1-2 days). Two crops
(breba on old wood early summer + main on new wood late summer/fall) described across
description/bloom_time/harvest_ready/growth_stages; warm-zone harvest windows span both.
Pests: root-knot nematode (high; the leading fig killer, no resistant rootstock), dried-fruit
beetle + fig souring, birds+squirrels (high). Diseases: fig rust, fig mosaic (virus, fig-mite
spread), fig endosepsis. Fertilizer refit: LIGHT feeding, `npk_ratio "10-10-10"`, over-N warning
(leaves-not-fruit + poor cold hardiness). pH `preferred [6.0,6.5]`, `tolerated [6.0,7.8]`.

## Gate result -- whole_crop_gate fig: **PASS (0 violations), exit 0**
Every A-gate 0. Highlights: A3 perennial 0, A4 tree-calendar 0 (all calendars derived via
`tree_calendar.derive_tree_calendar` so calendar == derive(bloom,harvest)), A22 variety-chill 0,
A25/A29/A36 register 0, A20 display 0, A23 raw-display 0, B dual-voice null_values 0
(186 CP / 7 SP), C/D 0 dashes/temps, E 5 sources all catalogued+T1, F anchoring 0 gaps.

**A37 (calendar-coherence): 0 violations** -- nothing to report separately.
- Bug 1 (growing-after-harvest) is frost_anchored-only -> no-op for a perennial tree (trees exempt,
  as noted in the task).
- Bug 2 (one-month harvest hole) applies to all crops but all fig harvest windows are single
  contiguous summer/fall spans (Jun-Oct etc.), so there is no Oct-May single-month punch-out.
- Confirmed standalone: `calendar_coherence_gate.py` on the spliced scratch canonical =
  `0 growing-after-harvest + 0 harvest-hole` across all 125 crops.
Also confirmed dataset-wide `register_completeness_gate.py` = PASS (0 unruled prose; the 6 deferred
are pre-existing companion §5 entries, not fig).

## Sources (all existing catalog T1, verified 2026-06-30 via WebFetch)
- `clemson_hgic` -- https://hgic.clemson.edu/factsheet/fig/ (parthenocarpy, breba+main, varieties,
  15F cold event, 1"/wk water, 8-8-8/10-10-10, prune after coldest, nematodes/rust/souring, 3-4 yr)
- `uga_ext` -- https://fieldreport.caes.uga.edu/publications/C945/home-garden-figs/ (pH 5.5-6.5,
  spacing 10-20 ft, fertilizer 1/2 lb/ft to 5 lb, halve in north, 1-1.5"/wk, nematode = leading killer)
- `umd_ext` -- https://extension.umd.edu/resource/growing-figs-maryland (parthenocarpic, dieback
  below 20F + roots hardy, 15-gal container + garage overwinter, spacing 10 ft, bear yr 2-3,
  breba lower quality, main Aug-frost, cold-hardy varieties, winter-protection methods, birds)
- `ucanr_ext` -- https://ucanr.edu/site/uc-marin-master-gardeners/document/fig (CA: no pollination
  needed, breba+main, 8h+ full sun, 20-30 ft size, Black Mission/Desert King/Osborne, fig beetle/mite)
- `uf_ifas_edis` -- https://edis.ifas.ufl.edu/publication/MG214 (chill "not more than 100 hours"
  <=45F; parthenocarpic vs Smyrna/San Pedro-need-Blastophaga; dormant wood hardy ~15-20F; FL
  varieties; spacing 10-16 ft; 1/2 to 2-4 lb 10-10-10 Feb-Aug; fig rust control)

## FLAGS
- **Texas A&M (tamu_agrilife) fig = UNREADABLE, NOT cited.** The aggie-horticulture crop-guide URL
  404'd, and the agrilifeextension asset page only exposes a topic summary with full content behind
  the AgriLife Learn paywall (`figs_2015.pdf` is PDF-only). Per the no-shell-out rule I did not
  extract it; fig is sourced from the 5 readable T1 pages above instead.
- Suitability calls (z5 marginal vs unsuitable; z6 marginal; z11 marginal) are reasoned edge
  judgments leading with cold-tenderness + humid-tropic disease -- fine for the scale-phase
  "generally-safe" bar; a cert audit may refine exact zone edges and per-zone harvest windows.
- The calendar `bloom` token = leaf-out/breba-set anchor (figs have no showy bloom); flagged in
  prose. This is inherent to fitting a parthenocarpic species onto the deciduous_fruit_tree model.
