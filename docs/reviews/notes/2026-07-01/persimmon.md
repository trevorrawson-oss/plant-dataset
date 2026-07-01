# persimmon -- author-fresh pilot NOTES

Authored by FILLING the persimmon shell, modeled on certified **peach** for the
`deciduous_fruit_tree` / `perennial_chill_gated` STRUCTURE (different family -- heavy refit).
READ-ONLY on canonical throughout; built in scratch, spliced into a scratch copy, gated to PASS.

- **Output:** `persimmon_crop.json` (compact, no trailing newline, 86 top-level keys == peach's 86;
  adds `year_one_notes_{seasoned,beginner}` + `rootstock_selection_basis` the shell lacked).
- **Status:** `author_fresh_pilot`; `launch_ready_core`/`launch_ready_seasoned` both `false`.
- **calendar_basis:** changed shell's `frost_anchored` -> `perennial_chill_gated` (required by A30,
  since archetype is `deciduous_fruit_tree`).

## The pollination model (the headline refit: Diospyros, Ebenaceae)

Pollination is TYPE-DEPENDENT and is the story that drives the biology:

- **Asian / Oriental (D. kaki)** -- Fuyu (non-astringent, eaten firm), Hachiya (astringent, ripened
  jelly-soft): **self-fruitful**, and the commercial cultivars are **parthenocarpic** (set seedless
  fruit with no pollen). One tree crops alone.
- **American (D. virginiana)**: typically **dioecious** -- male and female flowers on separate trees,
  so a female needs a **male** within ~50-200 ft. Exception: **self-fruitful female selections
  (Meader)** set seedless fruit with no male.
- The two species do **not** cross-pollinate each other.

Encoding: `self_fertile: true` and `pollination.self_fertile: true` reflect the **dominant home
case** (a single self-fruitful Asian Fuyu). BOTH `pollinator_notes_{seasoned,beginner}` and
`pollination.notes_*` explicitly explain the **Asian-self vs American-dioecious split**, including
the Meader exception and the "no cross-pollination between species" rule.

## Chill + hardiness (much broader, lower-chill than peach)

- **Low chill.** Asian ~100-200 h below 45°F (UF HS1389, UC); American modest. `chill_hours_range`
  [100, 700]; per-variety chill (A22 numeric): Izu 100, Fuyu 200, Hachiya 200, Great Wall 200,
  Meader 400, Prok 400 -> **no-fruit-split floor = 100** (Izu).
- **Hardiness split.** American to ~-20 to -25°F (z4-9, MUCH cold-hardier); Asian killed below ~10°F
  (z7-10). Combined: `hardiness_zone` 4-10, `reliable_fruit_zone` 5-10. Bloom is **late (May-June)**,
  so persimmon largely escapes spring frost -- the limiter is midwinter COLD at the cold edge and
  insufficient CHILL / summer sunburn at the warm/desert edge.

### Regional roster (honest, gate-consistent with the shared chill table)

American covers the cold end, Asian the warm; both overlap z7-9.
- **northern_tier:** z3 unsuitable (empty; ~-40°F kills American); z4 marginal; z5-7 fruits_reliably.
- **se_gulf, ca_interior, ca_north_coast, warm_arid:** fruits_reliably (both types; classic country).
- **ca_south_coast:** z9 fruits_reliably; z10 marginal (low coastal chill).
- **ca_desert (z9,z10), low_desert_az (z9):** marginal -- chill barely met, **summer heat/sunburn**
  is the binding limit (UC: persimmon does poorly in desert; UA: Fuyu "practically pest free").
- **fl_peninsula:** z10 marginal (low-chill Asian; astringent types do better deep south); z11
  survives_no_fruit -> **empty** (chill_lo 0 < floor 100).
- **hawaii_tropical:** z11 survives_no_fruit -> **empty** (lowland ~0 chill; note that cooler upland
  HI, outside this region, does grow persimmon).

Every fruiting cell carries a 12-token calendar **derived deterministically** from its bloom+harvest
display windows (`tree_calendar.derive_tree_calendar`), so A4 tree-calendar coherence is 0 by
construction. Empty cells: unsuitable (z3) and the two zero-chill survives_no_fruit cells.

## Other refits vs peach

- **Low-pest / ornamental:** `difficulty: easy`; pests are few (scale, mealybug, persimmon psyllid,
  and the one that can be serious -- persimmon borer); diseases minor. `harvest_urgency: low` (fruit
  holds on the tree into cool weather; Fuyu stores well).
- **Diseases:** authored **anthracnose** (UF-confirmed) + **root/crown rot** (Phytophthora; Asian
  persimmon is root-rot-prone, hence native rootstock) + **leaf spot** (NC State: "no serious
  disease problems"). NOTE: the brief named "crown gall"; I substituted **sourced** root/crown rot +
  canker instead, since T1 sources named Phytophthora crown rot / Botryosphaeria canker / anthracnose,
  not crown gall (source-honesty call -- flag for review if crown gall is specifically wanted).
- **Fertilizer:** light feeder; **excess nitrogen drops fruit** (UGA/UF) -- npk 10-10-10, split
  late-dormancy/summer, ~2 oz per year of age.
- **Rootstock:** D. virginiana (native, cold/wet-tolerant, the default), D. lotus (date-plum), and
  D. kaki seedling (warm CA only). `rootstock_selection_basis: soil_pest_tolerance`.
- **Astringency handling** is the #1 consumer failure mode: authored into storage + harvest_ready +
  failure_diagnostics (astringent Hachiya must ripen jelly-soft; non-astringent Fuyu eaten firm).

## Gate result

`python3 tools/whole_crop_gate.py persimmon <scratch_canonical>` -> **GATE: PASS (exit 0)**.
All A-numbered gates 0 violations (A30/A31/A32/A33/A34, A2-A29, A35/A36/A37), plus B (dual-voice
null_values 0), C/D (0 dash, 0 non-canonical temp), E (9 source IDs, 0 uncatalogued, 0 non-T1),
F (97 claim-leaves, 0 anchoring gaps), G (flip state clean).

### A37 (new calendar-coherence gate) -- reported separately

**A37 = 0 violations (clean).** No hand-fix needed and none applied. Rationale: Bug 1
(growing-after-harvest) is a **no-op off frost_anchored**, so it never fires for a
`perennial_chill_gated` tree; Bug 2 (one-month harvest hole) checks the `harvest` DISPLAY window for
a single month punched between two spans -- every persimmon cell uses a **single continuous** fall
harvest window, so no hole exists. A37 required no normalizer intervention here.

`release_verify.py` -> **clean, exit 0** (2 NON-BLOCKING Step-5.5 `wait`-legibility review notes on
ca_north_coast.z10 / ca_south_coast.z10 -- the annual-oriented pause heuristic mis-firing on
mild-coastal TREE cells that legitimately carry only 1-2 dormant months; A4 governs tree calendars
authoritatively and passed 0).

## Sources (all catalog T1) + flags

Used 9 T1 source IDs, all catalogued: `clemson_hgic`, `uga_ext`, `uf_ifas_edis`, `ncsu_ext`,
`uc_ipm`, `ucd_fruitnut`, `uariz_ext`, `tamu_agrilife`, `uhawaii_ctahr`. Confirmed live + read via
WebFetch/WebSearch (NEVER curl/wget/pdftotext):
- **clemson_hgic** https://hgic.clemson.edu/factsheet/persimmon/ -- READ (types, astringency,
  pollination split, cold hardiness).
- **uga_ext** https://fieldreport.caes.uga.edu/publications/C784/ -- READ (native -20 to -25°F,
  Asian <10°F, dioecious vs parthenocarpic, 10-10-10 rate, excess-N drop, borer).
- **uf_ifas_edis** https://ask.ifas.ufl.edu/publication/HS1389 -- READ (chill 100-200h, pH 6-7,
  15ft spacing, split fertilizer, anthracnose, harvest Aug-Dec).
- **ncsu_ext** https://plants.ces.ncsu.edu/plants/diospyros-kaki/ (+ .../diospyros-virginiana/ for
  American cells) -- READ (z7-10b Asian, <10°F, "no serious insect or disease problems", 4-6 yr).
- **uc_ipm** https://ipm.ucanr.edu/PMG/GARDEN/PLANTS/persimmon.html -- READ (scale, mealybug, borers,
  Phytophthora root/crown rot, leaf spot).
- **ucd_fruitnut** https://fruitandnuteducation.ucanr.edu/fruitnutproduction/Persimmon/ -- read via
  search aggregation (chill <100h, parthenocarpy, 3-5 yr / ~60 yr life, Fuyu/Hachiya harvest, desert
  sunburn). FLAG: the direct URL 301-redirects to a UC ANR page that returned 403 on WebFetch; content
  confirmed via search snippet, not a clean single-page fetch.
- **uariz_ext** https://extension.arizona.edu/.../az1269_...pdf -- **PDF (not extracted, per the
  no-pdftotext rule)**; persimmon content (Fuyu 200h self-fruitful "practically pest free"; Izu 100h;
  Shinseiki 350-400h) read via search snippet. Same PDF peach cites. FLAGGED as modeled-from-snippet.
- **tamu_agrilife** https://aggie-horticulture.tamu.edu/.../persimmons_2015.pdf -- **PDF (not
  extracted)**; content (Oriental persimmon widely adapted in TX, low-pest, root-rot-prone, native
  used as rootstock, Fuyu/Izu firm-eaten) read via search snippet. FLAGGED as modeled-from-snippet.
- **uhawaii_ctahr** https://www.ctahr.hawaii.edu/oc/freepubs/pdf/ -- generic CTAHR pubs directory URL
  (same as peach's hawaii anchor); used only for the zero-chill lowland-HI survives_no_fruit cell.
  FLAGGED as a directory-level anchor, not a specific persimmon page.

### Flags summary
1. `ucd_fruitnut`, `uariz_ext`, `tamu_agrilife` content confirmed via search snippet, not clean full
   fetch (PDF or redirect/403); NOT shelled out to extract. Cite-honesty: the numbers used are the
   ones those pages state.
2. Substituted **root/crown rot + canker** (T1-sourced) for the brief's "crown gall" (unsourced in
   T1) -- flag if crown gall specifically is required.
3. `uhawaii_ctahr` anchor is a directory URL, not a specific persimmon factsheet.
4. Region establishment `plantings` offsets are plausible perennial-precompute placeholders
   (informational; the load-bearing display windows are the per-cell bloom/harvest strings, which
   drive the A4-coherent calendars).
