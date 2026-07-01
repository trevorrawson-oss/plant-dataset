# pawpaw -- author-fresh gold-standard PERENNIAL (author notes)

**Crop:** pawpaw (*Asimina triloba*, Annonaceae) -- North America's largest native fruit.
**Model:** filled the shell against the certified **peach** `deciduous_fruit_tree` structure (exact
86-key parity), heavy family refit. `calendar_basis="perennial_chill_gated"`, `archetype="deciduous_fruit_tree"`.
**Status:** `author_fresh_pilot`; `launch_ready_core=false`, `launch_ready_seasoned=false`.
**Output:** `pawpaw_crop.json` (compact, 166,218 bytes, no trailing newline). Canonical READ-ONLY throughout
(SHA `84321950...` unchanged).

## The signature refits vs peach

### 1. Pollination -- apple-like-but-weirder, leads `pollinator_notes_*` + `pollination{}` + companions + failure_diagnostics
- **Self-INCOMPATIBLE** (`self_fertile=false`, `pollination.needs_pollinizer=true`, `pollinizer_distance_ft=30`).
  Needs **2 genetically DISTINCT trees** (two cultivars, or two+ seedlings) -- NOT two of the same clone.
  Encoded that a named cultivar + its own **root suckers are one genotype** and do not count (the `bad_seasoned`
  companion + the `pawpaw_fd_bloomed_no_fruit` diagnostic). Flowers are protogynous (female-first), further
  preventing selfing.
- **Fly/beetle pollinated, NOT bees** -- deep maroon, faintly carrion/fermentation-scented flowers evolved to
  draw blowflies + carrion beetles; these pollinators are inefficient/undependable, so natural set is poor.
- **Hand pollination** is the standard grower response (small brush, fresh pollen from one clone -> ripe sticky
  stigma of a distinct clone, repeated over bloom). Leads the `blossom` growth stage + the hand-pollinate
  notification + `pawpaw_blossom` tips.

### 2. Part-shade-when-young (unusual for a fruit tree)
Woodland understory native: young foliage is genuinely sun-sensitive and scorches in full sun. Encoded as
`sunlight="full sun (part shade the first year or two)"`, the `pawpaw_fd_scorched_young_leaves` diagnostic, the
`establishment` stage + shade notification + `HEAT_STRESS` weather trigger, and `start_method.hardening_off_*`
(shade acclimation). Full sun only once established (best fruit).

### 3. Other refits
- **Moderate chill** ~400h+ (`chill_hours_range=[400,1000]`, all varieties `chill_hours_required=400` -> gate
  floor 400). KSU: requirement not rigorously studied, ~400-1000, not cultivar-differentiated -> variety
  selection is by **cross-pollination**, not chill matching (unlike peach). Very cold-hardy z5-8 core
  (`hardiness_zone 4-9`, `reliable_fruit_zone 5-8`).
- **Very short shelf life** (`harvest_urgency="high"`): ripe fruit 2-3 days room temp, ~week fridge; unripe
  fruit ~2-3 wk fridge then ripen out; freeze the pulp. Why it is never in stores.
- **Taproot -> container spring planting** (`start_method.start="container_spring"`, not bare-root); the
  `pawpaw_fd_transplant_failed` diagnostic.
- **Clonal suckering** -> patches of 500+ stems, one genotype (ties back to the pollination trap).
- **Few pests** (honest, thin-by-design): pawpaw peduncle borer (*Talponia plummeriana*, medium), zebra
  swallowtail caterpillars (low -- pawpaw is the sole host; a feature), fruit-raiding wildlife (medium).
  **Deer avoid** the foliage (acetogenins). 1 disease: Phyllosticta leaf/fruit spot (low, cosmetic).
- **Rootstock handled honestly**: no dwarfing/clonal rootstock exists; cultivars are grafted onto pawpaw
  seedling rootstock; own-root seedlings also grown (variable, slower). Two `rootstock_options`;
  `rootstock_selection_basis="seedling_compatibility"`.
- **years_to_first_harvest [4,7]** (grafted ~4, seedling 5-8); slow. Container_ok=false (deep taproot);
  `self_watering_ok=true` (unusual for a tree -- pawpaw likes even moisture, so a sub-irrigated pot suits the
  young-tree phase, with a drainage caveat).

## Region / suitability model (10 regions; calendars DERIVED via tools/tree_calendar.py)
Pawpaw is a humid-eastern understory tree; the West/desert/tropics are a genuine poor fit.
- **fruits_reliably** (calendar): northern_tier z5/z6/z7, se_gulf z8 (native range core).
- **marginal** (calendar): northern_tier z4 (season-limited edge), se_gulf z9 (hot low-chill ~350h edge),
  ca_interior z8/z9 (chill OK but hot/dry/alkaline -> high-care, honest hedge).
- **survives_no_fruit** (empty; chill_lo < 400 floor satisfies the A3 no-fruit split): ca_north_coast z9/z10,
  ca_south_coast z9 (cool summers / low chill -> tree lives, no crop).
- **unsuitable** (empty): northern_tier z3, ca_south_coast z10, ca_desert z9/z10, warm_arid z8, low_desert_az
  z9, fl_peninsula z10/z11, hawaii_tropical z11.
Bloom/harvest shift by region (S->N): bloom Mar (se_gulf z8) to May (northern z4); harvest Aug (S) to Oct (N),
matching pawpaw's late, ~150-180-day ripening. All harvest strings are single contiguous spans -> no A37 holes.

## Gate result (`whole_crop_gate.py pawpaw`, spliced into a scratch canonical) -- **PASS, exit 0**
All A-numbered gates 0 (A2-A37), dual-voice null_values 0, dash 0, temp-form 0, source-tier clean (5 T1),
anchoring gaps 0, flip-state clean.
- **A37 (calendar-coherence): 0 violations.** Bug 1 (growing-after-harvest) is a no-op for trees
  (frost_anchored only); Bug 2 (harvest-hole) reads the harvest DISPLAY string -- all cells use single
  contiguous spans, so nothing flagged. **No A37 lines to report / hand-fix.**

## Sources (T1 catalog only; all verified live 2026-06-30)
- `ksu_pawpaw` -- Kentucky State University Pawpaw Program (the premier authority): planting guide + FAQ.
  Hardiness z5-8, chill 400-1000, self-incompatibility, fly/beetle + hand pollination, spacing 8 ft, pH 5.5-7,
  spring/container planting, taproot, years-to-fruit, mature 25 ft, fertilizer, suckering, peduncle borer.
- `psu_ext` -- Penn State (The Native Pawpaw Tree; Pawpaw in the Garden and the Kitchen): sun, fruit
  6-12 oz, ripening late Aug-Sep, shelf life, ~4 yr to bear, deer resistance, storage/freezing, cultivars.
- `uiuc_ext` -- Illinois Extension (Pawpaw: America's tropical treasure): flavor, ripening, shelf life,
  maroon carrion-scented flowers, no serious pests/disease, deer, zebra swallowtail sole host, 10-30 ft.
- `wvu_ext` -- WVU Extension: understory/best in full sun, young trees need shade 2 yr, fly pollination,
  self-incompatible, ripen Aug-Sep, potted-not-bare-root transplants.
- `umd_ext` -- Maryland Extension (Native Trees of MD: Pawpaw): clonal colonies via runners, beetle/fly
  pollination + self-incompatibility, ripen Aug-Oct, deer-unpalatable (bark/foliage chemicals), swallowtail host.

## Flags
- **No unreadable sources.** All five T1 pages fetched cleanly (no curl/wget/pdftotext used; WebFetch/WebSearch
  only). One nav-hub page (KSU "pawpaw-growing-information") carried no specifics; used the KSU planting guide +
  FAQ instead. KSU has deeper PDFs (Layne96, RVT, PawPaw Foundation) left unread per the no-PDF-extract rule --
  not needed; the HTML T1 set fully backs the record.
- **Chill values are estimates**, not measured (KSU states this); all varieties set to 400 (the moderate floor)
  and flagged in `chill_hours_note_*` + variety notes as approximate and not cultivar-differentiated.
- **Peduncle borer / peach analogs**: no replant-disease complex documented for pawpaw (unlike peach); rotation
  authored honestly around site (drainage/frost-pocket/shade), not a rotation interval.
- **Refine-at-variety-expansion**: region bloom/harvest windows are generally-safe regional brackets, not
  fine-tuned dates (per the scale-phase rule); exact days are a variety-delta-pass concern.
