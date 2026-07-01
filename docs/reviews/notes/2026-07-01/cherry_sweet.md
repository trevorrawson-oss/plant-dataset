# cherry-sweet -- PERENNIAL PILOT authoring notes (the bot's first tree)

Slug `cherry-sweet` (Prunus avium). Filled the shell modeled STRUCTURALLY on the certified
**peach** (same genus, archetype `deciduous_fruit_tree`, `calendar_basis perennial_chill_gated`),
refitting every value for sweet cherry. Built by deep-cloning peach's structure (guaranteeing
top-level key-parity for the register/completeness gates) and overwriting all content.

- Deliverable: `cherry_sweet_crop.json` (this scratch dir)
- Canonical: **READ-ONLY, untouched** (cherry-sweet is still a shell in the live canonical;
  `git status` confirms `crops_data_final.json` unmodified vs HEAD).
- Note on environment: HEAD advanced externally mid-session (canonical `ed8abc66` -> `1bc569dc`,
  a different lane). Re-validated the deliverable against the CURRENT canonical + CURRENT tools:
  key-parity vs current peach holds and the gate still passes.

## GATE RESULT
`python3 tools/whole_crop_gate.py cherry-sweet <scratch>` -> **GATE: PASS (exit 0)**, both against
the build snapshot and re-spliced into the current canonical. `tools/release_verify.py` -> clean,
no blocking concerns (its 2 `wait` review notes are pre-existing **cherry-tomato** cells, not
cherry-sweet). `register_fill_gate` -> PASS.

### Perennial gate branches that FIRED (non-trivially, on `perennial_chill_gated`)
- **A30** calendar_basis enum guard -> 0 (dispatch is honest: `perennial_chill_gated` + archetype match)
- **A2** region-fill completeness -> 0 (all 10 regions filled, plantings + region_notes present)
- **A3** perennial cert-gate -> 0 (one `track:"perennial"` establishment entry per region; suitability
  enum; the NO-FRUIT DIRECTION SPLIT vs the shared `region_chill_delivered` table at floor=250h)
- **A4** tree calendar coherence -> 0 (every filled cell's `calendar[]` DERIVED via
  `derive_tree_calendar(bloom,harvest)`, so it cannot drift)
- **A22** perennial variety-chill type lock -> 0 (all 8 varieties carry NUMERIC `chill_hours_required`)
- **A31** region roster floor -> 0 (full canonical 10-region roster, valid zone keys)
- **A33** numeric sanity -> 0 (tree-spacing ceiling 360in; spacing [180,300])
- **A34** cross-consistency -> 0 (pH prose "6.5 to 7.0" == `ph.preferred_range [6.5,7.0]`)

## Peach perennial fields MIRRORED (all present, refit) -- nothing omitted
`calendar_basis=perennial_chill_gated`; `archetype=deciduous_fruit_tree`; `perennial=true`;
`chill_hours_required` (null, crop-level, like peach), `chill_hours_range=[200,1100]`,
`chill_hours_note_seasoned/_beginner`; `bloom_time_seasoned/_beginner`, `bloom_duration_days=9`;
`pollination{self_fertile,needs_pollinizer,pollinizer_distance_ft,notes_*}`, `self_fertile=false`,
`pollinator_notes_seasoned/_beginner`; `hardiness_zone_min/max=5/9`, `hardiness_notes_seasoned/_beginner`,
`reliable_fruit_zone_min/max=5/8`; `rootstock_options[5]`, `recommended_rootstock`,
`recommended_rootstock_note`, `rootstock_selection_basis`; `establishment_years=4`,
`establishment_note`; `years_to_first_harvest=[3,5]`, `years_to_full_production=[6,7]`,
`productive_lifespan_years=30`; `dormancy_window`, `pruning_window`; `growth_stages_year_one=null`,
`growth_stages_annual=null`, `growth_stages[8]` (incl. `year_phase`), `year_one_notes_seasoned/_beginner`;
`tasks=[]`; `varieties.recommended[8]` + `varieties_detail=[]`; `tips_by_stage` keyed to the 8 stage ids;
`succession_policy{suitable:null, reason_seasoned}`; `harvest_urgency=high`; `failure_diagnostics[4]`;
the peach `regions{}`/`resolved_by_zone{}` PERENNIAL calendar token model (perennial establishment
planting per region + `perennial_precompute` cells with bloom/harvest display + derived `calendar[]` +
suitability enum + `frost_risk_note_seasoned` + `chill_basis_*`). `gating_factors`: NOT present (peach
carries none; chill rides in `chill_hours_*` + the gate's default, mirrored exactly). **No peach
perennial field could not be mirrored.**

## Key cherry refits (peach = structure; every value refit)
- **Self-sterile pollination (the signature):** `self_fertile=false`, `pollination.needs_pollinizer=true`.
  Every consumer pollination field LEADS with "plant a second compatible variety unless you pick a
  self-fertile one." Incompatibility (S-allele) groups noted; the Bing/Lambert/Royal Ann
  cross-incompatible trap called out. Self-fertile cultivars (Stella, Lapins, Sweetheart, Compact
  Stella, Skeena, Black Gold) named as the single-tree path + universal pollinizers. The decisive
  `companions.good_seasoned` entry is "a compatible pollinizer (or a self-fertile variety)."
- **Chill:** most cultivars ~700-1000h (high-chill tree); low-chill **Royal Lee + Minnie Royal**
  (~250h, a mutually-pollinizing pair) for mild-winter zones. Variety chills: Bing 800; Stella/Lapins/
  Sweetheart/Rainier/Black Tartarian 700; Royal Lee/Minnie Royal 250. Floor = 250 (drives the A3 split).
- **Cracking (signature failure):** rain/dew on ripe fruit splits it; built into watering (EVEN
  moisture rule), HEAVY_RAIN weather trigger (high), a dedicated failure_diagnostic, harvest_ready,
  brown rot, and the harvest-rain notification.
- **Birds (major pest):** a dedicated `pests` entry (netting the only reliable control) + the
  "keep it small enough to net" thread tying to dwarfing rootstock + a netting notification.
- **Rootstocks:** Mazzard (standard), Mahaleb (semi-dwarf, drainage-fussy), Gisela 5 (dwarf,
  precocious, hardy, container-capable), Gisela 6 (semi-dwarf, the recommended default), Colt
  (vigorous, NOT cold-hardy). `rootstock_selection_basis=vigor_precocity_and_soil` (cherry rootstocks
  DO control size -- the explicit INVERSE of peach's note).
- **Hardiness:** z5-9 (reliable 5-8); injury near -10F; less hardy than peach (z4) or sour cherry.
  Bare-root DORMANT winter planting; early-spring frost-sensitive bloom; late-spring/early-summer harvest.
- **Pests (5):** western cherry fruit fly (signature), spotted wing drosophila, black cherry aphid,
  birds, borers. **Diseases (4):** brown rot, bacterial canker (most serious on sweet cherry),
  cherry leaf spot, X-disease (cherry buckskin). Training = CENTRAL LEADER (not peach's open vase);
  cherries are NOT thinned (peach is) -- both refit honestly in growth_stages/tips.

## Region suitability map (the honest narrowing vs peach)
Sweet cherry's range is NARROWER than peach -- 7 calendar-bearing cells vs peach's ~13. The shared
crop-invariant `region_chill_delivered` table + floor 250h govern the A3 no-fruit split:
- **northern_tier:** z3 unsuitable (too cold); z4 survives_no_fruit WITH calendar (chill 1000>=250,
  cold-edge blooms, frost takes the crop -- the one survives_no_fruit-with-calendar cell); z5 marginal;
  z6/z7 fruits_reliably.
- **ca_interior:** z8 fruits_reliably (the real CA cherry district, dry air), z9 marginal (lower chill).
- **ca_north_coast:** z9 marginal; z10 survives_no_fruit-EMPTY (chill 150<250, chill-limited).
- **ca_south_coast / ca_desert:** all survives_no_fruit-EMPTY (chill 50-200 < 250).
- **se_gulf / warm_arid / low_desert_az / fl_peninsula / hawaii:** UNSUITABLE-empty.

## Source ids (existing catalog, T1 only; verified via WebFetch/WebSearch 2026-06-30)
Used: `usu_ext` (Utah State -- hardiness -10F/z5, self-fertile list, western cherry fruit fly),
`wsu_ext` (WSU TreeFruit -- rootstocks, pollination/S-alleles, chill), `osu_ext` (OSU -- cracking),
`iastate_ext` (ISU -- growing cherries: soil/sun/pH/planting/birds/brown rot/leaf spot),
`msu_ext` (MSU -- netting vs birds + SWD), `umn_ext` (SWD), `psu_ext` (bacterial canker),
`ucanr_ext` (UC IPM cherry -- brown rot/bacterial canker/X-disease/SWD/black cherry aphid/borers),
`ucanr_santa_clara_mg` (CA chill), `cornell_ext`. Region-root attribution also cites (catalogued T1,
no URL needed at region root): `clemson_hgic`, `uga_ext`, `uariz_ext`, `tamu_agrilife`, `uf_ifas`,
`uhawaii_ctahr`. **0 uncatalogued, 0 non-T1.** NEVER used curl/wget/pip/pdftotext.

## FLAGS / where annual->perennial modeling was unclear (also filed in `open_findings`, blocks_launch:false)
1. **Heat/humidity-limited zones don't fit the chill-keyed no-fruit split.** The A3 split is CHILL-keyed
   (survives_no_fruit + chill-met => MUST carry a calendar). For sweet cherry the limiter in se_gulf and
   warm_arid is HEAT/HUMIDITY/DISEASE, not chill or cold, even though chill is adequate (650h, 450h). To
   honestly show NO reliable crop with an empty calendar there, I classified those cells **`unsuitable`**
   (which the gate allows to be empty unconditionally) rather than survives_no_fruit. This is defensible
   (sweet cherry genuinely is not adapted to the humid Southeast or hot Texas), but it is a MODELING CHOICE
   the daily review should ratify: the perennial model has no "heat/humidity/disease-limited but chill-OK"
   suitability tier for a deciduous tree. Candidate enhancement: a heat/humidity gating factor for
   deciduous trees (analogous to the evergreen heat_accumulation floor).
2. **Region unsuitability sourcing for the warm zones** rests on (a) the crop-invariant region chill
   climate (shared table) and (b) sweet cherry's chill/hardiness/heat/humidity limits documented by
   usu/wsu/iastate; dedicated sweet-cherry pages from each warm-region extension (Clemson/UGA/UF/UAZ/
   TAMU/Hawaii) were NOT separately fetched. Verify region-local at the cert pass.
3. **Dates are GENERALLY-SAFE, not fine-precise** (per the standing scale-phase rule). Bloom/harvest
   windows and per-region calendars are structural fits refit from peach with cherry's earlier, shorter
   (~60-85 day) harvest; refine exact days at the variety-delta pass.
4. **Floor = 250h** (Royal Lee/Minnie Royal). Including the low-chill pair is biologically honest and is
   sweet cherry's low-chill frontier, but it lowers the chill-met threshold; I reserved `marginal`/
   `survives_no_fruit-empty` deliberately so warm-winter cells read honestly rather than over-promising.
5. **status=`author_fresh_pilot`, launch flags false.** Not certified -- this is the pilot artifact for
   the daily biology-fidelity review + source-truth sample.
