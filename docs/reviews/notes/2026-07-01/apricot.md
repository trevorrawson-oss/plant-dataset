# apricot -- author-fresh perennial pilot NOTES

**Output:** `apricot_crop.json` (this scratchpad). Built off the certified **peach**
(`deciduous_fruit_tree`, `perennial_chill_gated`) template; every value refit for
**Prunus armeniaca**. `status="author_fresh_pilot"`, `launch_ready_core/seasoned=false`.
Canonical `crops_data_final.json` was READ-ONLY (peach + apricot shell read; nothing written to it).

## Field mirror
All **86 top-level keys** match peach exactly (`missing vs peach: []`, `extra vs peach: []`).
Every ~35 perennial field is present and refit: `calendar_basis="perennial_chill_gated"`,
`chill_hours_range`, per-variety `chill_hours_required`, `bloom_time_*`, `bloom_duration_days`,
`pollination`/`self_fertile`/`pollinator_notes_*`, `hardiness_zone_*` + `reliable_fruit_zone_*`,
`rootstock_options`/`recommended_rootstock*`/`rootstock_selection_basis`, `establishment_years`/
`establishment_note`, `years_to_first_harvest`/`years_to_full_production`/`productive_lifespan_years`,
`dormancy_window`/`pruning_window`, `growth_stages` (9-stage tree cycle, `growth_stages_year_one`/
`_annual`=null), `tasks`, `varieties`/`varieties_detail`, `regions{}` (10) + `resolved_by_zone{}`.
Region calendars were DERIVED with the gate's own `tree_calendar.derive_tree_calendar(bloom, harvest)`
so A4 is coherent by construction.

## Apricot refits vs peach (biology)
- **Pollination: SELF-FRUITFUL.** `self_fertile=true`, `pollination.needs_pollinizer=false`. A second
  variety is an OPTIONAL bonus for the few cultivars that respond (Moorpark called out by name);
  one tree fruits. (Peach is also self-fertile, but the exception flips: peach = J.H. Hale;
  apricot = Moorpark benefits, none require.)
- **SIGNATURE RISK = very early bloom -> late-frost crop loss.** This leads the hardiness, region,
  bloom, failure-diagnostic, notification, and weather-trigger prose. Blooms earlier than peach/plum/
  apple; warm-winter-then-frost regions marginal.
- **Chill:** `chill_hours_range=[350,900]` (USU/UC IPM: most 600-900h, low-chill ~350h). Variety span
  350 (Katy) -> 700 (Chinese/Goldrich). **No-fruit-split floor = min variety chill = 350** (> the
  200 low end of the warm survives_no_fruit cells, so those stay correctly empty; A3 passes).
- **Bare-root dormant** planting (`start.start="bare_root_dormant"`).
- **Rootstocks (4):** Apricot seedling, Myrobalan (plum), Marianna 2624 (plum), Lovell (peach
  seedling). `recommended_rootstock="Myrobalan 29C"`. Plum stocks tolerate heavier/wetter soil but
  are canker-prone; peach seedling is more canker-tolerant (UC IPM).
- **Hardiness z5-8** (`hardiness_zone_min=5`, `_max=8`; `reliable_fruit_zone` 5-8). Region cells span
  z3-11 like peach (cells legitimately extend past the headline band, same as peach's z10/z11 cells).
- **Pests:** plum curculio, peachtree borer, aphids (green peach / mealy plum), San Jose scale,
  catfacing insects. **Diseases:** brown rot (Monilinia, *the* signature -- apricot is among the most
  susceptible of all fruit), bacterial canker, bacterial spot, shot hole (Coryneum blight).
- **Distinctive apricot touches:** iron chlorosis on alkaline western soils (soil/ph/fertilizer prose
  + a failure_diagnostic); thin closer (one fruit every **4-6 in**, vs peach 6-8) and curb biennial
  bearing; prune **more lightly than peach** (bears on multi-year spurs + one-year wood); ripens
  earlier than peach; dries/freezes exceptionally well; `years_to_first_harvest=[2,4]`.
- **Suitability map** (honest apricot geography, not a peach copy): fruits_reliably = **ca_interior
  z8/z9 + warm_arid z8** (dry-summer, chill-adequate, frost-dodgeable -- apricot's real homes);
  marginal across the humid/variable-spring north + SE + coastal/low-chill CA + low desert;
  survives_no_fruit (empty) at the warm low-chill edges (ca_south_coast z10, ca_desert z10,
  fl_peninsula z10); survives_no_fruit WITH calendar at cold northern_tier z4 (chill abundant, bloom
  frozen); unsuitable (empty) z3 north / fl z11 / hawaii z11.

## Gate result -- whole_crop_gate apricot: **PASS (exit 0)**
Spliced into a scratch canonical copy; every branch A2-A37 + B/C/D/E/F/G = **0 violations**.
- **A37 (calendar-coherence): 0** -- Bug 1 (growing-after-harvest) is no-op for perennials (trees
  legitimately regrow), Bug 2 (harvest-hole) finds none (all harvest windows are single spans).
  **No A37-only lines to report** -- the crop is gate-clean including A37.
- A3 perennial (no-fruit split), A4 tree-calendar coherence, A22 variety-chill, A20 display,
  A25/A29/A36 register, A19/A26/A27 companions, A33/A34 truth-layer: all 0.
- Separate release checks: `verbatim_scan` = 0 hard / 0 borderline; `register_completeness_gate` =
  PASS (0 unruled); `contamination_scan` = **21%** overall (BELOW peach's own 22%, far below the
  certified vegetables at 30-47%). The byte-identical strings shared with peach are generic tree
  phenology, short UI titles, and genuinely shared stone-fruit biology (e.g. catfacing insects) --
  no apricot-specific fact carries peach content. Every "peach" mention in apricot prose is a
  legitimate cross-reference (comparison, peach-seedling rootstock, peachtree-borer/green-peach-aphid
  names, Florida regional context).

## Sources (existing-catalog **T1 only**; 11 IDs, all catalogued + admitted)
usu_ext, ucanr_ext, iastate_ext, umn_ext, ncsu_ext, clemson_hgic, tamu_agrilife, uariz_ext,
uf_ifas_edis, uhawaii_ctahr, ucanr_santa_clara_mg. Gate E: 0 uncatalogued, 0 non-T1.

Core apricot biology is anchored to pages I confirmed live via WebSearch/WebFetch:
- usu_ext -> extension.usu.edu/yardandgarden/research/apricots-in-the-home-garden (CONFIRMED)
- ucanr_ext -> ipm.ucanr.edu/home-and-landscape/cultural-tips-for-growing-apricot/ (CONFIRMED)
- iastate_ext -> yardandgarden.extension.iastate.edu/how-to/pollination-requirements-tree-and-small-fruits (CONFIRMED)
- umn_ext -> extension.umn.edu/fruit/growing-stone-fruits-home-garden (CONFIRMED)
- ncsu_ext -> plants.ces.ncsu.edu/plants/prunus-armeniaca/ (CONFIRMED)

## FLAGS (per the READ-only / no-curl / pilot-precision rules)
1. **uariz_ext anchored to az1269 "Deciduous Fruit & Nuts for the Low Desert" -- PDF-ONLY.** The page
   was confirmed to exist via WebSearch but NOT opened (the no-`pdftotext`/no-`curl` rule). Treated as
   modeled; the low-desert facts (low-chill <400h, Jan/Feb bare-root, Katy/Royal Rosa very-early May
   harvest) were corroborated in the search snippet.
2. **clemson_hgic anchored to the peach-diseases factsheet.** Clemson has no dedicated apricot page;
   the SE brown-rot/disease context is modeled from its stone-fruit guidance (brown rot biology is
   genus-shared). Flagged as modeled.
3. **tamu_agrilife, uf_ifas_edis, uhawaii_ctahr, ucanr_santa_clara_mg** URLs are the region's
   extension stone-fruit/deciduous-fruit guidance, cited at **pilot precision** (region cells), not
   individually opened. Per-claim URL sampling (WebFetch each cited page, confirm it backs the
   number) is the **certification** step (source-truth sample), not the author-fresh pilot -- this is
   the documented citation-honesty gap between author_fresh_pilot and certified.
4. Gate F only checks URL shape + `verified` presence (not liveness/support); no fabricated hosts were
   used -- every URL is a real extension domain path.

## Next steps (not done here -- future cert)
Source-truth URL sampling per claim; family-bleed audit sign-off; then the launch flip (status ->
verified_gs_arc, launch flags true) once Trevor rules. Splice-into-canonical + state-trio are a
separate promote task (canonical stayed READ-ONLY this session).
