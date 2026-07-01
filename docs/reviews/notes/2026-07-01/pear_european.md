# pear-european -- PERENNIAL PILOT authoring notes

**Output:** `pear_european_crop.json` (compact, `separators=(",",":")`, `ensure_ascii=False`,
no trailing newline, 86 top-level keys -- matches apple's 86). Standalone crop object.
**Status:** `author_fresh_pilot`, `launch_ready_core=false`, `launch_ready_seasoned=false`,
`open_findings: []`. READ-ONLY on canonical (loaded apple as the structural template + the
shell + the shared `region_chill_delivered` table; never wrote `crops_data_final.json`).

## GATE RESULT

`python3 tools/whole_crop_gate.py pear-european <scratch>` -> **GATE: PASS (exit 0)**, all
branches 0 violations, on the first self-gate run. Scratch = a throwaway copy of canonical with
the pear-european shell replaced by this record. Key tallies: dual-voice 210 populated CP pairs /
**0 null siblings**; dash 0; non-canonical temp 0; source-tier **18 distinct IDs, all catalogued
T1, 0 non-T1**; anchoring 93 claim-leaves / **0 gaps**; numeric-sanity 0; cross-consistency 0.

## Mirrored ALL ~35 apple perennial fields (NONE omitted)

Built from a deep copy of the certified apple record, then refit every value. Confirmed present
and pear-refit: `calendar_basis`=`perennial_chill_gated`; `archetype`=`deciduous_fruit_tree`;
`chill_hours_required`(null)/`chill_hours_range`[200,800]/`chill_hours_note_{seasoned,beginner}`;
`bloom_time_{seasoned,beginner}`/`bloom_duration_days`(9); `pollination`{} /`self_fertile`(false)/
`pollinator_notes_{seasoned,beginner}`; `hardiness_zone_min`(4)/`max`(8)/`hardiness_notes_*`;
`reliable_fruit_zone_min`(5)/`max`(8); `rootstock_options`(5)/`recommended_rootstock`(OHxF 87)/
`recommended_rootstock_note`/`rootstock_selection_basis`(size); `establishment_years`(4)/
`establishment_note`; `years_to_first_harvest`[4,6]/`years_to_full_production`[6,10]/
`productive_lifespan_years`(50); `dormancy_window`{11,3}/`pruning_window`{2,3};
`growth_stages_year_one`[]/`growth_stages_annual`[]/`year_one_notes_*`; `tasks`[];
`varieties_detail`[]; `regions{}`/`resolved_by_zone{}` perennial-precompute calendar (NOT the
annual 12-token model); `description_*`/`harvest_ready_*`; `succession_policy.suitable`=false.

**`gating_factors`: mirrored apple exactly = the field is ABSENT.** Apple carries no explicit
`gating_factors` key, so `perennial_gate.gating_factors()` applies the
`["chill_hours","cold_hardiness"]` default; the gate's C2 guard confirms `chill_hours` is in the
effective set (it is). Adding an explicit list was unnecessary and would risk the C2 trap.

**One deliberate refit, not an omission:** `harvest_urgency` = `"medium"` (apple = `"low"`),
because European pears have a tighter pick window -- they must be caught mature-but-firm and
ripened off the tree.

## Key pear refits (apple = structure; every value refit for Pyrus communis)

- **Ripen OFF the tree (the signature):** threaded through `description_*`, `harvest_ready_*`,
  `storage.*`, the `harvest`/`post_harvest` growth stages, tips, and a dedicated
  `failure_diagnostics` entry (`mealy_rotten_core`). Pick mature-but-firm (upward-twist
  detachment, ground color lightening, corky lenticels) -> cool-store to satisfy post-harvest
  chilling (days for summer Bartlett, several weeks near freezing for winter Anjou/Bosc) ->
  ripen at room temperature. Tree-ripening -> internal browning + stone-cell grit at the core.
  Sourced: UC IPM pear harvest, OSU FS-147, WSU pear harvest, UMN.
- **Fire blight LEADS the disease list** (Erwinia amylovora): pear markedly more susceptible than
  apple; the binding constraint across the humid Southeast. Lean nitrogen, dry-weather pruning,
  resistant cultivars + OHxF rootstock. Pests refit to the pear set: codling moth, **pear psylla**
  (the signature pear pest + dormant-oil program + pear-decline vector), pear scab (Venturia
  pyrina), **Fabraea leaf spot** (Entomosporium). Diseases: fire blight, pear scab, Fabraea,
  pear decline.
- **Cross-pollination leads `pollinator_notes_*`:** mostly self-unfruitful, plant 2 compatible
  cultivars 50-100 ft apart; Bartlett/Anjou partially self-fruitful in mild climates but crop
  better with a pollinizer; **Bartlett x Seckel incompatible**; **Magness pollen-sterile** (the
  triploid-analog caution, mirroring apple's triploid note); pear nectar low -> bee activity
  matters more. `pollinizer_distance_ft`=100.
- **Rootstocks refit to OHxF + quince + seedling:** OHxF 87 (recommended), OHxF 97, OHxF 333
  (fire-blight + pear-decline tolerant, Old Home x Farmingdale); Quince (dwarfing/precocious but
  graft-incompatible with Bartlett/Bosc/Seckel without an Old Home interstem, and cold-tender);
  Bartlett/Winter Nelis seedling (standard). Sourced: WSU pear rootstocks.
- **Bare-root DORMANT winter planting**, spring bloom (a few days before apple -> more
  frost-exposed), late-summer to fall fruit. `years_to_first_harvest` 4-6 (later than apple);
  `productive_lifespan_years` 50 (very long-lived). Hardiness z4-8, reliable fruit z5-8.
- **12-variety roster** (Pyrus communis), bloom-sequenced very_early->very_late, chill 200-800:
  Hood(200), Kieffer(350), Orient(350), Seckel(500), Moonglow(600), Ayers(600), Warren(600),
  Bartlett(800), Comice(600), Bosc(600), Anjou(700), Magness(700). Fire-blight-resistant set
  flagged for the South; blight-susceptible dessert pears (Bartlett/Bosc/Comice) flagged for
  drier/cooler air.

## Perennial gate branches that FIRED (real work, not no-op)

- **A30** calendar_basis enum guard -> `perennial_chill_gated` accepted.
- **A3** perennial cert-gate: exactly-1 `track:"perennial"` establishment entry per region; the
  4-value suitability enum; and the **NO-FRUIT DIRECTION SPLIT** read against the shared
  `region_chill_delivered` table -> **0 violations across all 20 cells**.
- **A4** tree-calendar coherence: every non-empty calendar == `derive_tree_calendar(bloom,
  harvest)` -> 12 calendar-bearing cells recomputed, **0 incoherent** (calendars were generated
  by that exact deriver, so coherence is by construction).
- **A22** perennial variety-chill TYPE lock: numeric `chill_hours_required` on all 12 varieties,
  no legacy string -> 0.
- A2 region-fill (10 regions, perennial track), A17 npk, A19/A26/A27 companions, A20 display,
  A23 raw-display, A25/A29/A36 register, B/C/D/E/F/G all 0.
- Correctly NO-OP'd off perennial: A5/A9/A10/A11/A13/A14/A15/A16/A24/A28/A32 (annual / other
  archetypes), A8 (succession out-of-scope).

### The load-bearing modeling decision: chill floor = 200 (Hood)

The A3 no-fruit split compares the **shared-table low-end** for each region+zone against the
crop's `min_variety_chill` floor (the lowest recommended-variety `chill_hours_required`). I set
the roster minimum to **Hood at 200h** (documented 150-250h low-chill Southern European pear),
which yields the gate-consistent suitability map below (validated separately, 0 mismatches):

| outcome | region.zone (shared low-end) |
|---|---|
| fruits_reliably (+cal) | northern_tier 5/6/7, se_gulf 8, ca_interior 8/9, ca_north_coast 9, warm_arid 8 |
| marginal (+cal) | northern_tier 4, se_gulf 9, ca_south_coast 9 |
| survives_no_fruit **+cal** (chill met: lo>=200) | northern_tier 3 (lo 1000; cold/season-limited, not chill) |
| survives_no_fruit **empty** (lo<200) | ca_north_coast 10 (150), ca_south_coast 10 (50), ca_desert 9 (150)/10 (100), low_desert_az 9 (100), fl_peninsula 10 (50) |
| unsuitable empty | fl_peninsula 11, hawaii_tropical 11 |

I deliberately did NOT include the documented ~150h cultivars (Pineapple/Floridahome) in the
recommended[] roster: a 150 floor would force the low-desert and immediate-foggy-coast cells
(shared lo 150) to carry fruiting calendars, over-promising European pear where it genuinely
struggles (low chill + extreme heat / fog + fire blight). Floor 200 marks those honestly as
chill-limited (empty). European pear is correctly shown as MORE chill-demanding and less
warm-South-adapted than apple (whose floor was 100).

## Sources (18, all catalogued T1) -- verification status + FLAGS

Per the SOURCING RULE: existing source_catalog + WebFetch/WebSearch only; never curl/wget/pip/
pdftotext. All 18 cited IDs are catalogued T1; anchoring URLs are real http(s) + dated 2026-06-30.

**Text-verified live this session (content confirmed via WebFetch/WebSearch):**
- `umn_ext` -> extension.umn.edu/fruit/growing-pears (full pear content fetched)
- `uc_ipm` -> ipm.ucanr.edu/.../pearharvest.html (off-tree ripening, fetched)
- `wsu_ext` -> treefruit.wsu.edu/web-article/pear-rootstocks/ + /pear-pollination/ (fetched)
- `ucd_fruitnut` -> fruitsandnuts.ucdavis.edu/.../chilling-requirement (general chill page; live)
- `clemson_hgic` -> hgic.clemson.edu/factsheet/fire-blight-of-fruit-trees/ (confirmed exists;
  supports the fire-blight + resistant-variety + Fabraea claims)

**FLAGGED -- catalogued T1 + real-format URL, but the EXACT pear page was NOT text-verified this
session (owed at cert: WebFetch each and re-point if needed):**
- `osu_ext` FS-147 picking-storing-apples-pears -- WebFetch returned **403**; substance confirmed
  via search snippet, URL is a real OSU catalog page. Re-verify.
- `psu_ext` pear-production-in-home-fruit-plantings -- real PSU pear URL (search-confirmed), but
  my WebFetch returned a generic page (likely JS/redirect); content not text-confirmed.
- `clemson_hgic` -- the dedicated Clemson *pear* culture factsheet 404'd; I cite the fire-blight
  factsheet instead. A dedicated pear culture page (Clemson/UGA "Home Garden Pears") is a cleaner
  cite for the non-fire-blight pear facts.
- `uga_ext` (C740), `ncsu_ext` (growing-pears-in-the-home-garden), `uf_ifas`
  (gardeningsolutions/.../pears/), `uhawaii_ctahr`, `ucanr_ext`/`uc_mg` (homeorchard.ucanr.edu),
  `ucanr_marin_mg` (marinmg.ucanr.edu) -- plausible/real-domain pages reused or pattern-assumed
  from the apple template; NOT pear-text-verified.
- `uariz_ext` (az1269.pdf) + `nmsu_ext` (H-310) -- reused from apple's desert/arid cells; both are
  PDFs/pages I did NOT re-fetch (az1269 is a PDF -> no extraction per rule; cited as modeled). H-310
  may be apple-specific; re-point to a pear-specific NMSU/AZ deciduous-fruit page at cert.
- `ucanr_san_diego_mg`, `ucanr_slo_mg` -- reused from apple's CA-coast MG variety pages (real,
  general fruit/variety pages).

## Unclear modeling / open questions for the daily review

1. **Chill floor (200 via Hood)** is the single load-bearing call -- it sets the whole
   suitability map. If the review prefers a higher, "standard European pear" floor (e.g. 400-600,
   dropping the low-chill Southern cultivars from recommended[]), the warm-edge cells
   (ca_south_coast 9, ca_interior 9, ca_north_coast 9) flip toward survives_no_fruit/empty, which
   contradicts real CA pear production. The current floor keeps CA pear country fruiting while
   honestly emptying the desert/immediate-coast -- the apple-consistent choice.
2. **se_gulf 8 = fruits_reliably** leans on the fire-blight-resistant set (Kieffer/Orient/etc.);
   the prose is explicit that the dessert pears fail there. Some reviewers might prefer `marginal`
   to foreground the disease pressure. Defensible either way; I chose fruits_reliably because
   Southern extensions treat resistant pears as one of the easier Southern tree fruits.
3. **Bloom/harvest display dates** are reasonable-regional (the GENERALLY-SAFE-NOW bar), shifted
   ~1 week earlier than apple for pear's earlier bloom; exact days are a variety-delta-pass refit.
4. `disease.type` for pear decline = `"other"` (a phytoplasma; not fungal/bacterial). No gate
   enums on `disease.type`, so harmless, but flagging the choice.
