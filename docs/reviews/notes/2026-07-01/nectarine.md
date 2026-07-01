# nectarine -- author-fresh pilot (perennial_chill_gated refit off certified peach)

Output: `nectarine_crop.json` (compact, canonical style: `separators=(",",":")`, `ensure_ascii=False`,
no trailing newline). Modeled cell-for-cell on certified **peach** (nectarine = Prunus persica var.
nucipersica, a smooth-skinned peach -- the closest refit). Canonical `crops_data_final.json` was
READ-ONLY throughout; SHA `84321950...` unchanged.

## Method
Deep-copied the peach record, applied a proper-noun-protected `peach -> nectarine` swap over rendered
prose only, then hand-overrode the fields that genuinely differ. All ~35 peach perennial fields are
mirrored and refit (none omitted): `calendar_basis="perennial_chill_gated"`, `chill_hours_required`
/`chill_hours_range`, bloom/pollination/`self_fertile`/pollinator_notes, hardiness + reliable-fruit
zones, rootstock_* (options + note + `rootstock_selection_basis`), establishment_years/note,
years_to_first_harvest/full_production, dormancy_window/pruning_window, growth_stages (year_one +
annual are null on peach, kept null), tasks, varieties_detail (`[]`, as peach),
`regions{}`/`resolved_by_zone{}` (all 10 canonical regions), notifications, weather_triggers,
tips_by_stage, failure_diagnostics.

Protected proper nouns (kept, since they are the recognized names even on nectarine): peachtree
borer / lesser peachtree borer, peach tree short life, peach leaf curl.

## What changed vs peach

### Skin (the defining difference)
- **Smooth, fuzzless skin** woven into `description_*`, `harvest_ready_*` (color reads clean, no fuzz;
  bare skin bruises/marks more, handle gently). Botanical name -> `Prunus persica var. nucipersica`.

### Pollination
- Peach is already self-fertile, so `self_fertile=true` is unchanged, BUT peach's **J.H. Hale
  self-sterile exception was dropped** everywhere (nectarines are reliably self-fruitful, one tree).
  Refit: `pollination.notes_*`, `pollinator_notes_*`, `companions.note_*`, the bloom notification body,
  and the blossom self-fertility tip. `needs_pollinizer=false`.

### Disease / pest susceptibility (fuzzless = more vulnerable)
- **Brown rot** (`diseases[Brown rot]`): now framed as the most damaging nectarine disease; the bare
  skin gives the fungus easier entry than a peach's down, so it rots faster/harder; sanitation +
  generous thinning stressed. Sources -> clemson_hgic (peach-diseases) + mu_ext.
- **Bacterial spot**: nectarines "generally more susceptible than peaches" (MSU), smooth-skin pitting
  more conspicuous, variety choice is the main lever (Fantasia tolerant, Hardired bred for tolerance).
  Sources -> clemson_hgic + msu_ext.
- **Catfacing insects (stink bugs / plant bugs)**: scarring far more visible on smooth skin; severity
  bumped low -> medium.
- **Western flower thrips** ADDED as a 6th pest (nectarine-specific fruit scarring; smooth skin shows
  every mark). Sources -> ucanr_ext (UC IPM nectarine WFT) + mu_ext.
- **Peach leaf curl** kept unchanged in substance (still applies to nectarine).

### Varieties (re-pointed to self-fruitful nectarine cultivars)
Arctic Star (300h, low-chill white -- the no-fruit-split floor), Fantasia (500), Flavortop (650),
Roseprincess (750 white), Redgold (750), Independence (700), Hardired (800, disease-tolerant),
Mericrest (850, cold-hardy to ~-28°F). `chill_hours_range` -> [300, 900]. All self-fruitful; note_*
now leads with disease tolerance (nectarines run more disease-prone than peaches).

### Region map -- kept intact, prose refit
All 10 regions, zones, calendars, suitabilities, dates, and the shared chill-delivered bands are
peach-identical (nectarine shares peach's chill/cold physiology). Prose refit peach cultivars ->
nectarine: Florida King -> Arctic Star (and its floor ~400h -> ~300h across ca_north_coast z10,
ca_south_coast z9/z10 + region/chill notes, ca_desert z9 + region/chill notes, warm_arid z8,
low_desert_az z9 + region/chill notes, fl_peninsula z10 + region/chill notes); Reliance/Contender/
Intrepid -> Mericrest/Hardired (northern_tier z4/z5). The A3 no-fruit split still holds: floor 300 is
in (100, 1000], so the three warm survives_no_fruit cells (chill_lo 50/100/50) stay empty and
northern_tier z4 (chill_lo 1000) keeps its calendar -- byte-consistent with peach.

### Hardiness
Zone fields mirror peach (min 4, max 9, reliable 5-9) to stay consistent with the kept region map;
nectarine's marginally lower cold-hardiness ("not quite as cold-hardy as peach," MU) and best-in-5-to-8
reality are carried in `hardiness_notes_*` and the northern_tier z4/z5 cell prose (hardiest cultivar
Mericrest ~-28°F).

## Gate result -- `whole_crop_gate.py nectarine` on a spliced scratch copy: **PASS (exit 0)**
All A-gates 0 violations (A30-A37 + B/C/D/E/F/G). Cross-checks: register_completeness_gate exit 0;
peach re-gated on the same spliced dataset still exit 0 (shared table undisturbed).

**A37 (calendar-coherence) lines, reported separately per instructions: NONE.**
A37 Bug 1 (growing-after-harvest) is frost_anchored-only, so a tree is exempt; Bug 2 (harvest-hole)
runs on all crops but the peach-derived harvest windows are already normalizer-clean, so A37 = 0. No
hand-fixes were needed or made.

(verbatim_scan is fetch-based and could not reach the network in this sandbox, so its source-vs-prose
comparison did not run; all nectarine prose is originally authored, not copied verbatim.)

## Status / flags
`verification_status.status = "author_fresh_pilot"`; `launch_ready_core=false`,
`launch_ready_seasoned=false`; `open_findings=[]`. Not launch-eligible (a draft), as intended.

## Sources (existing catalog T1 only -- no new source IDs minted)
Nectarine-specific claims lean on: **mu_ext** (Univ. of Missouri "Nectarine: The Fuzzless Peach" --
self-fruitful, fuzzless = more disease/insect-prone, brown rot most devastating, not quite as
cold-hardy, varieties Fantasia/Flavortop/Redgold/Sunglo); **clemson_hgic** (peaches-nectarines +
peach-diseases -- "nectarines are fuzzless peaches, culture same," self-fruitful); **msu_ext**
(bacterial spot on peaches and nectarines -- "nectarines are generally more susceptible than
peaches"); **ucanr_ext** (UC IPM nectarine western flower thrips -- fruit scarring). Region/culture
sources carried from peach: ncsu_ext, umd_ext, umaine_ext, uga_ext, ucanr_santa_clara_mg, uariz_ext,
tamu_agrilife, uf_ifas, uf_ifas_edis, uhawaii_ctahr, iastate_ext, clemson_peach_diseases. All catalog
T1 (source-tier gate E: 0 uncatalogued, 0 non-T1).

## Honest flags for the review lane
- Backend `companions.*.provenance.reason` still cite the peach replant-disease literature (the 1941
  California peach-after-peach study, etc.) verbatim -- left as-is because that IS the evidence base
  for the Prunus replant claim (same species) and the field is backend own-voice, not rendered
  register prose. Grep for "peach" in the record surfaces these plus deliberate nectarine-vs-peach
  comparisons in consumer prose (all intentional).
- Variety `chill_hours_required` values are reasonable cultivar figures (nursery/extension-grounded),
  not individually cited -- same convention as peach (block-level extension citation). Nursery chill
  figures vary; the load-bearing constraint is that the low-chill floor (Arctic Star 300h) keeps the
  A3 no-fruit split byte-consistent with peach, which it does.
- Hardiness kept at peach's 4-9 / 5-9 for map consistency despite MU's "not quite as cold-hardy";
  the nuance lives in prose. If the review lane prefers a hardened z5 floor, northern_tier z4 would
  flip survives_no_fruit -> unsuitable (empty calendar) to match -- a one-cell change, flagged here
  rather than made.
