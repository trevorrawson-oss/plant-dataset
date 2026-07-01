# cherry-sour (Prunus cerasus) -- author-fresh perennial pilot NOTES

Authored 2026-06-30 by FILLING the `cherry-sour` shell, modeled structurally on the certified
**peach** (genus Prunus, `archetype: deciduous_fruit_tree`, `calendar_basis: perennial_chill_gated`)
and refit off the **cherry-sweet** pilot scaffold (`scratchpad/cherry_sweet_crop.json`), the closest
reference (same genus; shared cherry pests, diseases, rootstocks, cracking, storage, growth stages).
Output: `scratchpad/cherry_sour_crop.json`. **Canonical READ-ONLY** (SHA `84321950...` unchanged,
matches LATEST.txt). Status `author_fresh_pilot`, both launch flags `false`.

## All ~35 peach perennial fields mirrored + refit (none omitted)
`calendar_basis=perennial_chill_gated`, `archetype=deciduous_fruit_tree`, `perennial=true`;
`chill_hours_required=null` + `chill_hours_range`; `hardiness_zone_min/max` + `reliable_fruit_zone_min/max`;
`bloom_duration_days`; `dormancy_window {12,2}` + `pruning_window {2,3}`; `establishment_years` + note;
`pollination{}`; `self_fertile`; `recommended_rootstock` + note + `rootstock_selection_basis` +
`rootstock_options[]`; `years_to_first_harvest` / `years_to_full_production` / `productive_lifespan_years`;
dual-register prose `description_*`, `harvest_ready_*`, `bloom_time_*`, `hardiness_notes_*`,
`chill_hours_note_*`, `pollinator_notes_*`, `year_one_notes_*`; `varieties.recommended[]` (numeric chill);
`growth_stages[]` (8 stages) + `tasks:[]`; `notifications[]`, `weather_triggers[]`, `tips_by_stage{}`;
`yield_expectations{}`, `failure_diagnostics[]`, `moon_phase_preference{}`, `succession_policy{}`;
`regions{}` / `resolved_by_zone{}` perennial calendar-token model. Calendars DERIVED via
`tree_calendar.derive_tree_calendar(bloom, harvest)` so A4 is coherent by construction.

## Key sour-cherry refits vs peach / sweet cherry
- **POLLINATION = SELF-FRUITFUL** (`self_fertile=true`, `pollination.needs_pollinizer=false`,
  `pollinizer_distance_ft=null`). ONE tree crops on its own; Montmorency the classic. This is the KEY
  difference from **sweet cherry, which is self-STERILE** (most cultivars set no crop without a
  cross-compatible pollinizer of overlapping bloom). Grounded in Iowa State: "Sour or tart cherries
  are self-fruitful ... Only one sour cherry tree needs to be planted." Every pollinizer-dependent
  field (companions, growth_stages bloom/planting, notifications, tips, failure_diagnostics,
  start_method, container) rewritten to remove the sweet-cherry pollinizer requirement.
- **CHILL** `chill_hours_range=[700,1200]`; prose "roughly 700 to 1,000+ hours, Montmorency near
  1,000, NO low-chill option" (unlike peach/sweet, sour cherry has no low-chill cultivar). Variety
  chills: Montmorency 1000, Balaton 1000, Meteor 800, North Star 700, English Morello 700 -> A3
  no-fruit-split **floor = 700**.
- **COLD-HARDIER + a NORTHERN crop** `hardiness_zone_min/max = 4/8`, `reliable_fruit = z4-6`
  (matches task "z4-6"); survives to z3 with North Star/Meteor/Mesabi. Warm-winter regions are
  chill-limited/unsuitable. `difficulty=medium` (easier than sweet's `hard`: self-fruitful + hardy).
- **Smaller bush-tree, tart pie/processing fruit** description/harvest_ready/storage rewritten for
  tart, pick-soft, pies/juice/freezer fruit (not fresh dessert); storage shorter fridge life,
  freezing emphasized. `productive_lifespan_years=25` (ISU: sour 20-25 yrs vs sweet <10).
- **Bare-root dormant** (`start_method.start` inherited `bare_root_dormant`).
- **Rootstocks** `recommended_rootstock=Mahaleb` (traditional sour-cherry stock, precocious,
  cold-hardy, well-drained-only); options Mahaleb / Mazzard / Gisela 5 / Gisela 6 / own-root genetic
  dwarf (North Star, Meteor). Dropped sweet's Colt (mild-winter, not cold-hardy).
- **Pests** (task list) Cherry fruit fly (eastern R. cingulata + black R. fausta, western noted) /
  Spotted wing drosophila / Black cherry aphid / Birds. Dropped peach/sweet borers.
- **Diseases** (task list) **Cherry leaf spot ELEVATED to severity `high` = the signature tart-cherry
  disease** (MSU: most important disease of tart cherry; Montmorency highly susceptible, drops leaves
  after a few lesions, premature defoliation) / Brown rot (high) / Bacterial canker (medium, sour
  more tolerant than sweet). Dropped sweet's X-disease (and its rotation reference).
- `years_to_first_harvest=[3,4]` (task).

## Region model (A3 no-fruit chill split; `region_chill_delivered` is the crop-invariant table)
Sour cherry is a NORTHERN, high-chill crop, so the map is shifted colder than sweet cherry.
- **northern_tier**: z3 `marginal`, z4/z5/z6 `fruits_reliably`, z7 `marginal` -- ALL carry derived
  calendars (Great Lakes tart-cherry belt is z5-6). z3 is the cold bonus edge (hardiest dwarfs),
  z7 the warm/low-chill/humid edge.
- **All warm regions empty (chill-limited / unsuitable)**: se_gulf z8/z9 `unsuitable`; ca_interior,
  ca_north_coast, ca_south_coast, warm_arid `survives_no_fruit` (tree lives, chill short); ca_desert,
  low_desert_az, fl_peninsula, hawaii `unsuitable` (no chill + heat). Every survives_no_fruit cell has
  delivered `chill_lo < 700 floor` -> empty calendar (A3 over-promise rule satisfied). 5 filled +
  15 empty cells across the full canonical 10-region roster.

## Gate result -- whole_crop_gate cherry-sour: **PASS (exit 0), 0 violations**
Clean on every branch incl. the perennial ones: A30 (calendar_basis), A31/A32 (coverage floors),
A3 (perennial no-fruit split), A4 (tree calendar coherence), A22 (variety-chill numeric), A25/A29/A36
(register), A19/A26/A27 (companion), B dual-voice (0 null siblings), C/D (0 user-facing dashes,
0 non-canonical temps, `°F` x8), E (16 T1 sources, 0 uncatalogued/non-T1), F (100 claim leaves, 0 gaps).
`release_verify`: chill table well-formed, reference crops PASS.

### A37 (calendar-coherence, the NEW gate) -- reported separately per instruction
**A37 flagged NOTHING for cherry-sour (0 lines, both bug1 + bug2 clean).** Trees are exempt from the
frost_anchored growing-after-harvest rule; the harvest-hole rule found no holes (tree harvest spans
are single contiguous windows, calendars derived by `derive_tree_calendar`). No hand-fix was needed.

## Sources (existing catalog T1 only; verified via WebFetch/WebSearch 2026-06-30; no curl/wget)
16 distinct T1 IDs: iastate_ext (growing-cherries, covers sour -- self-fruitful + cultivars + lifespan),
msu_ext (cherry leaf spot 101 + netting), umn_ext (SWD), usu_ext, ucanr_ext (cherry IPM), psu_ext
(bacterial canker + cherry leaf spot), wsu_ext (cherry rootstocks), cornell_ext, plus the region cells'
inherited ucanr_santa_clara_mg, clemson_hgic, uga_ext, uf_ifas, uariz_ext, tamu_agrilife, uhawaii_ctahr.

## Flags / open findings (all blocks_launch=false, status=open)
`author_fresh_pilot`; launch_ready_core/seasoned = false/false. Open findings: perennial-pilot needs
daily biology-fidelity review + source-truth sample; warm-region verdicts rest on the shared chill
table + iastate/msu sour-cherry sourcing (region-local pages not separately fetched per zone);
bloom/harvest windows are generally-safe structural fits (sour ripens a touch later than sweet,
late June to July in the north) to refine at the variety-delta pass.
