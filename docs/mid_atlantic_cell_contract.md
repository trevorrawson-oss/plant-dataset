# Mid-Atlantic cell contract -- per-archetype `regions.mid_atlantic` template (v0)

**Status:** LOCKED for authoring (Task 1 of 12, Mid-Atlantic region arc, roadmap item 8)
**Date:** 2026-07-20
**Origin:** `docs/superpowers/specs/2026-07-20-mid-atlantic-region-design.md` (read that first for the
product/scope rationale; this doc expands its section 4 "data model" into a verbatim,
copy-from template) + `docs/kickoffs/31-mid-atlantic-region.md` + the ruling that queued the whole
arc, `docs/reviews/notes/2026-07-15/tier2_mid_atlantic_ruling.md`.
**Precedent:** `docs/pnw_cell_contract.md` (the maritime-PNW region's sibling doc, shipped
2026-07-14). This doc mirrors its structure and method deliberately, but the emphasis inverts:
PNW's headline was a chill/heat archetype flip across many crop classes; **Mid-Atlantic's headline
is narrower and sharper -- one real gap, in one crop class, that this dataset already models and
already gates.** Tree fruit and berries need essentially no correction here (real NC chill clears
the whole canonical apple range with margin; NC State's own blueberry picks are already canonical
varieties). The one real gap is that warm-season annuals are missing an entire documented fall
planting cycle. Read the ruling note for the receipts; read THIS doc for the actual field shapes
every archetype writes against.
**Consumed by:** Tasks 4-7 (cool-season annuals / warm-season annuals / trees / citrus+berries+herbs
authoring batches). Each of those tasks writes one `regions.mid_atlantic` object per crop; this doc
is the shape they write against.
**Getting a key wrong here fails `whole_crop_gate` across dozens of crops at the single atomic
promote, not one crop** -- treat every key below as load-bearing.
**Method:** column GS-arc (`docs/gs_cross_crop_field_addition_v0.md`) -- a region is a column added
roster-wide (Option A, full 111-crop roster, forced by A31; Trevor decided the exact span 2026-07-20).
This is that column's field contract, locked before any crop is touched.

---

## 0. How to read this doc

- Every JSON block below is **pretty-printed for readability**. The canonical `crops_data_final.json`
  is written compact (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline) -- when a
  `regions.mid_atlantic` object is spliced into a real crop, it is compact, byte for byte, like every
  other region cell. Never hand-indent the real splice.
- The prose fields in the worked examples (`region_notes_*`, `suitability_note_*`, `chill_basis_*`,
  `cold_basis_*`, `type_note_*`) are **illustrative placeholders** demonstrating shape and register,
  not authored, final sourced content. Tasks 4-7 replace them with real NC State / VCE-sourced (T1)
  prose. The placeholders still follow house consumer-copy style so they double as a style example: no
  em dashes (commas, colons, semicolons, periods only), American English, temperatures as `°F`,
  "plant" lowercase outside sentence-start.
- **Two different honesty tiers apply to the absolute values in this doc, and they are marked
  explicitly wherever they differ:**
  - **Already real, T1-sourced, safe to use verbatim:** z8 frost dates (Raleigh/Wake County COOP,
    1944-2019, State Climate Office of NC via NC State Extension: **last frost April 8, first frost
    October 30**), the VCE 426-331 zone-8 tomato fall window (**July 1 - August 10**, Table 4,
    explicit fall column), NC State's ">1,000 chilling hours annually" statewide chill floor, and the
    real canonical blueberry-variety-to-`recommended_type` mapping (Duke/Jersey/Bluecrop/Patriot/
    Northblue/Northland = `northern_highbush`; Emerald/Jewel/Sharpblue = `southern_highbush`;
    Premier/Powderblue/Brightwell/Tifblue = `rabbiteye`). These come straight from the ruling note
    and the live canonical; every worked example below uses them where relevant rather than
    inventing a placeholder on top of already-real evidence.
  - **Genuinely NOT yet sourced, clearly-plausible placeholders only:** every z7 frost date, the exact
    per-zone chill-hour band split (only the real >1,000 hr statewide floor is sourced; the z7-vs-z8
    split is a plausible illustration), the exact `heat_pause` month list for any specific crop, and
    which crops beyond tomato actually carry a VCE-documented fall window. Task 3 (the T1 sourcing
    pass named in the kickoff) resolves these; do not treat this doc's z7 numbers as authoritative.
- **Every `calendar[]` array in every worked example below was checked against the actual live
  gate/deriver functions in this repo, not just eyeballed**, in the same spirit as the PNW contract's
  own verification callout: `tools/annual_calendar.py` (`annual_coherence_violations`,
  `annual_calendar_violations`, `heat_pause_backing_violations`), `tools/second_planting_gate.py`
  (`check_crop`, rules A+B), `tools/tree_calendar.py` (`derive_tree_calendar`,
  `tree_calendar_violations`), and `tools/berry_woody_calendar.py`
  (`berry_woody_calendar_violations`). Every worked example's calendar in this doc returned **zero
  violations** from the relevant function(s) when checked in a scratch script against these exact
  field values (not against the real canonical -- no canonical bytes were read-write touched). See
  each section's inline callout for which function(s) certified that section's example.
- Reference cells inspected to build this contract (exact key sets + resolution methods captured
  2026-07-20 against canonical `e1e01c47`): `broccoli.regions.northern_tier` (all zones, esp. z7),
  `cherry-tomato.regions.se_gulf` (all zones, esp. z8), `apple.regions.northern_tier` (esp. z7),
  `orange-navel.regions.se_gulf` (z8) and `.regions.northern_tier` (the empty/unsuitable reference
  shape), `blueberry.regions.northern_tier` (z7) and `.regions.se_gulf` (z8, the rabbiteye/evergreen
  reference shape), plus the gate/deriver source of truth (`tools/annual_calendar.py`,
  `tools/second_planting_gate.py`, `tools/tree_calendar.py`, `tools/berries_woody_gate.py`,
  `tools/berry_woody_calendar.py`, `tools/perennial_gate.py`, `tools/whole_crop_gate.py`,
  `tools/region_cell_audit.py`). See the Appendix for the exact captured key lists.

---

## 1. Invariants that apply to every `mid_atlantic` cell, all 4 archetypes

- `region_id`: `"mid_atlantic"`
- `region_label`: **`"Mid-Atlantic: Piedmont and Coastal Plain"`** (verbatim; no em dash; use this
  exact string, do not paraphrase -- `region_label` renders verbatim on the frontend). This is the
  final, Trevor-approved wording from the design spec section 4.1; do not use the ruling note's own
  ad hoc label ("mid-Atlantic z8") anywhere in a real cell.
- `zone_span`: `["7", "8"]` -- **DECIDED** (design spec section 4.2, Trevor 2026-07-20). Every
  `mid_atlantic` cell's `resolved_by_zone` carries **exactly** the keys `"7"` and `"8"`, no more, no
  fewer. This will be gate-enforced once Task 2 adds `mid_atlantic: ["7", "8"]` to
  `zone_span_gate.EXPECTED_SPANS` (A45, span<->key parity) -- **not done by Task 1**; this doc only
  fixes the value every later task authors against. z7 holds 2.2x more ZIPs than z8 in this belt
  (3,131 vs 1,444) and is the same continuous Piedmont-and-coastal-plain climate a shade cooler --
  it is NOT a throwaway edge zone the way a donor-cloned extra zone sometimes is elsewhere; author
  both zones as distinctly as the sources support, the same discipline PNW applied to its own z8/z9
  split.
- **Frost-ANCHORED discipline, non-negotiable across every archetype that carries it:**
  `resolution_method = "frost_anchored_resolved"` for annuals/herbs/berries/strawberry (the ordinary
  shape almost every other region in this dataset already uses -- Mid-Atlantic is NOT a bespoke
  `_month_resolution` region the way `se_gulf` is, and it is NOT frost-free the way `rgv` is);
  `resolved_from` carries **real** `{"last_frost": <date>, "first_frost": <date>}`, never null.
  `cold_pause` is a legitimate, expected winter token here (this belt has a real winter, unlike
  `se_gulf`'s balmy z8-10 span) -- `tools/region_cell_audit.py`'s `frost_model: "anchored"` branch
  (the same branch PNW uses) is the one Task 2 will register for `mid_atlantic`.
- **A trap to avoid: do not literally clone `se_gulf`'s cherry-tomato cell wholesale.** The brief's
  own worked-template pointer (`cherry-tomato.regions.se_gulf.z8`) is the right SHAPE reference for
  "`heat_pause` + `second_planting` coexisting" but the WRONG WIRING reference: `se_gulf` uses its own
  bespoke `resolution_method: "se_gulf_month_resolution"` and its `plantings[]` rule-layer entries
  anchor off se_gulf-only synthetic tokens (`"plant_out_start"`, `"heat_pause_start"`,
  `"heat_pause_end"`) that do not exist in the standard frost-anchored vocabulary. Mid-Atlantic is
  `frost_anchored_resolved`, so its `plantings[]` entries anchor off the ORDINARY vocabulary every
  other frost-anchored region already uses: `"last_frost"` (spring), `"first_frost"` (fall,
  negative offsets counting back), or `"plant_out"` (harvest, positive offsets off the crop's own
  set-out) -- exactly the vocabulary `broccoli.regions.northern_tier` already uses, including its own
  fall/`second_planting` succession. **`broccoli.regions.northern_tier.z7` is the correct WIRING
  template; `cherry-tomato.regions.se_gulf.z8` is the correct CONTENT-SHAPE template** (a real crop
  that carries both `heat_pause` and `second_planting` together, and specifically demonstrates the
  "action-over-passive" flip where a declared heat month renders as `plant` because the fall
  transplant is the actual activity that month -- see section 2.6). Do not confuse the two roles.
- **A genuine, useful coincidence: the wiring template is not just climate-analogous, it is partly
  the SAME geography.** `broccoli.regions.northern_tier`'s real `z7` row cites
  `umd_ext_broccoli` -- University of Maryland Extension -- whose catalogued `citable_for` field
  literally reads *"broccoli spring/fall windows; fall-often-better-than-spring (**mid-Atlantic**)"*.
  Maryland is one of this region's own seven states. That z7 row's two-cycle, `heat_pause`-bearing
  shape is not merely a plausible analog borrowed from a colder climate zone the way PNW had to
  reach for RGV/se_gulf precedent; it is real Extension content for a Mid-Atlantic state that is
  simply filed under the wrong region tag today. This is useful context for Task 4, not license to
  skip real Mid-Atlantic-specific sourcing (`ncsu_ext` / `vce_426_331`) for the crop actually being
  authored -- but it means the SHAPE is trustworthy, not just plausible.
- **The fall cycle is the differentiator -- restated explicitly, because it is the entire reason
  this region exists.** Nothing in this belt is misclassified today; the generic zone dates are
  simply conservative. VCE 426-331's zone-8 table carries an explicit separate fall tomato window
  (Jul 1 - Aug 10) and NC State's own central-NC planting calendar shows continuous transplanting
  through July 1, while the naive single-cycle deriver closes the season in mid-July and shows flat
  `cold_pause` from August through December against a real October 30 first frost. **Warm-season
  annuals carry a T1-sourced `heat_pause` (real midsummer set-failure months) plus a real fall
  `second_planting`; cool-season annuals get long spring-and-fall shoulders and carry NO
  `heat_pause`** unless a specific crop's own T1 evidence says otherwise (brassicas in this belt
  plausibly do carry one -- see section 2.4). This is the opposite emphasis from PNW (which had to
  argue AGAINST inventing a `heat_pause` almost everywhere); here a real, sourced `heat_pause` is
  expected and common, it just must be sourced per crop, never assumed.
- **Which crops get a fall cycle is a per-crop T1 call, not an extrapolation from tomato.** VCE
  426-331's tables cover more than tomato; the ruling names pepper, squash, and bean as likely
  neighbors but explicitly did NOT verify them. Extract VCE's FULL crop coverage early (design spec
  section 6) and follow the tables crop by crop. Expect a real tail of spring-only warm-season crops
  where VCE simply does not carry a fall window; that is the honest answer, not a gap to paper over.
- `resolution_method` is free-text provenance, not a gate-enforced enum (60+ distinct strings already
  live in the canonical). Use `"frost_anchored_resolved"` for the annual archetype, `
  "perennial_precompute"` for chill-gated trees, `"perennial_evergreen_precompute"` for citrus,
  `"berries_woody_precompute"` for the berry archetype -- all four are already-live strings, not new
  ones.
- `sources` / `anchoring_urls`: every rule-layer entry (`plantings[]` sub-objects) and every zone-row
  carries its own `sources` (source-catalog ids) + `anchoring_urls` (id -> `{url, verified}`) pair.
  T1-or-it-doesn't-ship holds. `ncsu_ext` (NC State Extension) and `vce_426_331` (Virginia Cooperative
  Extension Publication 426-331) are **already catalogued** T1 sources (both `tier: "T1"`,
  `trust_tier: "high"`; `vce_426_331`'s own `citable_for` field already reads *"Mid-Atlantic regional
  coverage"*) -- use these ids in every worked example below. Expect few or no NEW `source_catalog`
  entries in this arc (design spec section 4.7); this is another way it is lighter than PNW, which
  had to add crop-class-specific WSU/OSU publication sub-ids from scratch.
- Compact-JSON rule: never write the real splice with `indent=2`. This doc's blocks are pretty for the
  human reader only.

---

## 2. Archetype 1 -- frost-anchored ANNUAL cell (82 crops, the flagship of this arc)

**Who gets this shape:** the 82 `frost_anchored` annuals. This is the biggest batch (Tasks 4 and 5,
split cool-season / warm-season) and the one carrying the entire reason this region exists.

### 2.1 Cell-level keys

Identical to every other frost-anchored region's annual cell shape -- Mid-Atlantic adds no new
top-level key:

| Key | Shape | Note |
|---|---|---|
| `region_id` | string | `"mid_atlantic"` |
| `region_label` | string | `"Mid-Atlantic: Piedmont and Coastal Plain"` |
| `zone_span` | `["7","8"]` | decided |
| `sources` | `[id, ...]` | region-level source list |
| `plantings` | `[{...}, ...]` | the **rule layer** -- offsets off named frost anchors, not absolute dates |
| `resolved_by_zone` | `{"7": {...}, "8": {...}}` | the **render layer** -- absolute dates + `calendar[]` |
| `plantings_provenance` | nullable | present (may be null), matches `broccoli.northern_tier`'s convention |
| `region_notes_beginner` | string \| null | dual-register prose |
| `region_notes_seasoned` | string \| null | dual-register prose |

### 2.2 `plantings[]` entries -- the STANDARD frost-anchored vocabulary, never `se_gulf`'s

Anchor `start_indoors` / `plant_out` off `"last_frost"` (spring) and `"first_frost"` (fall, the
`second_planting` succession's own entry), and anchor `harvest_start` / `harvest_end` off `"plant_out"`
(the crop's own set-out). Each entry carries its own `sources` + `anchoring_urls` + (seasoned
register) `synthesis_note_seasoned`. **Never** `"plant_out_start"`, `"heat_pause_start"`,
`"heat_pause_end"`, `"transplant_window"`, `"frost_free_spring"`, `"soil_workable"`,
`"heat_subsiding"`, or `"fall_open"` -- those are donor vocabulary from `se_gulf`/`rgv`/other bespoke
regions that does not apply to a standard `frost_anchored_resolved` region. A fall
(`second_planting`-track) `plantings[]` entry is its own array element (`track: "second_planting"`),
exactly the shape `broccoli.regions.northern_tier`'s real fall entry already uses.

### 2.3 `resolved_by_zone["7"|"8"]` keys

| Key | Required? | Note |
|---|---|---|
| `plant_out` | required | absolute month/date-range string, **spring cycle only** |
| `start_indoors` | conditional | present only if the crop is tray-started; **spring cycle only** |
| `harvest`, `harvest_start`, `harvest_end` | required | **spring cycle only** |
| `first_plant_date`, `last_plant_date` | required | mirror the SPRING/primary succession's window only, matching every existing frost-anchored cell's convention |
| `calendar` | required, 12 tokens | must be internally coherent with BOTH the top-level spring window fields AND the nested `second_planting` fields where present (see 2.6) -- never fabricated independent of the dates |
| `resolution_method` | required | `"frost_anchored_resolved"` |
| `resolved_from` | required | `{"last_frost": <real date>, "first_frost": <real date>}` -- never null |
| `second_planting` | conditional | author where a real fall cycle exists; shape = `{start_indoors, plant_out, harvest_start, harvest_end, sources, anchoring_urls}` -- these live ONLY inside this nested object, never merged into the top-level fields (see 2.6's A43 discussion) |
| `heat_pause` | conditional | author where the T1 evidence supports a real midsummer set-failure/bolt period -- **expected common here**, the opposite default from PNW, but still sourced per crop, never assumed (design spec section 4.5, risk item 3) |
| `succession_spring` / `succession_fall` | conditional | present only if the crop runs multiple succession sowings within a season |
| `successions_realized` | conditional | derived count; present only if the crop is in succession scope (`tools/derive_realized_successions.py`) |
| `sources`, `anchoring_urls` | required | zone-row citation |
| `notes`, `zone_notes`, `planting_note` | required key, null-able value | present (possibly `null`) unless there is a real per-zone caveat to author (matches `northern_tier`'s three-key convention, not `se_gulf`'s two-key one) |
| `lifted_from_zone` | conditional | only if this zone's row was donor-cloned from the other -- expected RARE here given the real z7/z8 sourcing split (VCE covers z7-native Virginia; NC State covers z8-native NC) |

### 2.4 Cool-season worked example -- brassica-style, spring + fall two-cycle (broccoli pattern)

Modeled directly on the real, currently-certified `broccoli.regions.northern_tier.z7` cell (the
"same-states-cooler-edge" template named in the task brief, and per the callout in section 1, a cell
that is already partly Mid-Atlantic-sourced via `umd_ext_broccoli`). z8 uses the ruling's real Raleigh
frost dates (last frost **Apr 8**, first frost **Oct 30**); z7 uses a clearly-plausible placeholder
(last frost Apr 18, first frost Oct 22 -- a shorter season than z8, directionally correct for a
cooler zone, but NOT sourced; Task 3 finds a real Richmond / central-MD / north-Piedmont anchor).
Illustrative placeholder crop, values NOT fully sourced except the frost dates and the general
existence of a summer heat constraint on brassica heading (a well-established horticultural fact,
not specific to this exact month list):

```json
{
  "region_id": "mid_atlantic",
  "region_label": "Mid-Atlantic: Piedmont and Coastal Plain",
  "zone_span": ["7", "8"],
  "sources": ["ncsu_ext", "vce_426_331"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "spring",
      "track": "beginner",
      "start_indoors": [
        {
          "from": "last_frost",
          "offset_days": -49,
          "window_days": 21,
          "synthesis_note_seasoned": "Start transplants indoors about 6 to 7 weeks before the last frost; the crop tolerates light frost, so it goes out ahead of the frost-free date (NC State / VCE calendars).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "plant_out": [
        {
          "from": "last_frost",
          "offset_days": -21,
          "window_days": 21,
          "synthesis_note_seasoned": "Set out spring transplants about 3 weeks before the last frost; established plants of this crop shrug off a light frost (NC State / VCE).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_start": [
        {
          "from": "plant_out",
          "offset_days": 60,
          "window_days": 0,
          "synthesis_note_seasoned": "Matures in roughly 60 days in the mild spring-into-early-summer window (NC State).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_end": [
        {
          "from": "plant_out",
          "offset_days": 80,
          "window_days": 0,
          "synthesis_note_seasoned": "End of the spring harvest window before the belt's hot, humid midsummer stalls head quality.",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "anchoring_urls": {}
    },
    {
      "succession_id": 2,
      "label": "fall",
      "track": "second_planting",
      "start_indoors": [
        {
          "from": "first_frost",
          "offset_days": -110,
          "window_days": 30,
          "synthesis_note_seasoned": "Fall crop: start the second planting in midsummer, timed to head as nights cool ahead of the belt's real fall frost (NC State).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "plant_out": [
        {
          "from": "first_frost",
          "offset_days": -75,
          "window_days": 21,
          "synthesis_note_seasoned": "Set out fall transplants in mid to late summer; heads finish as the weather cools and tolerate this belt's light early frosts (NC State / VCE).",
          "sources": ["ncsu_ext", "vce_426_331"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"},
            "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_start": [
        {
          "from": "plant_out",
          "offset_days": 65,
          "window_days": 0,
          "synthesis_note_seasoned": "Fall heads mature in cooling weather; often the better crop of the two in this belt (NC State).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_end": [
        {
          "from": "first_frost",
          "offset_days": 14,
          "window_days": 0,
          "synthesis_note_seasoned": "Fall harvest continues past the first light frost; this crop tolerates it (NC State).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "anchoring_urls": {}
    }
  ],
  "plantings_provenance": null,
  "resolved_by_zone": {
    "8": {
      "plant_out": "Mar 18 - Apr 8",
      "start_indoors": "Feb 18 - Mar 11",
      "harvest": "May 17 - Jun 6",
      "harvest_start": "May 17",
      "harvest_end": "Jun 6",
      "first_plant_date": "Mar 18",
      "last_plant_date": "Apr 8",
      "calendar": ["cold_pause", "indoors", "plant", "plant", "harvest", "harvest", "heat_pause", "indoors", "plant", "harvest", "harvest", "cold_pause"],
      "notes": null,
      "zone_notes": null,
      "planting_note": null,
      "sources": ["ncsu_ext"],
      "anchoring_urls": {
        "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
      },
      "resolution_method": "frost_anchored_resolved",
      "second_planting": {
        "start_indoors": "Jul 12 - Aug 11",
        "plant_out": "Aug 16 - Sep 6",
        "harvest_start": "Oct 20",
        "harvest_end": "Nov 13",
        "sources": ["ncsu_ext"],
        "anchoring_urls": {
          "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
        }
      },
      "resolved_from": {"last_frost": "Apr 8", "first_frost": "Oct 30"},
      "heat_pause": {
        "months": [7, 8],
        "classification": "heat_pause",
        "basis_seasoned": "Summer gap is a heat exclusion, not a frost gap: this brassica's developing heads lose quality in hot, humid Piedmont and Coastal Plain summers, and plants in the head-formation stage bolt as temperatures climb (NC State Extension).",
        "sources": ["ncsu_ext"],
        "anchoring_urls": {
          "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
        }
      }
    },
    "7": {
      "plant_out": "Mar 28 - Apr 18",
      "start_indoors": "Feb 28 - Mar 21",
      "harvest": "May 27 - Jun 16",
      "harvest_start": "May 27",
      "harvest_end": "Jun 16",
      "first_plant_date": "Mar 28",
      "last_plant_date": "Apr 18",
      "calendar": ["cold_pause", "indoors", "plant", "plant", "harvest", "harvest", "heat_pause", "indoors", "growing", "harvest", "harvest", "cold_pause"],
      "notes": null,
      "zone_notes": null,
      "planting_note": null,
      "sources": ["vce_426_331"],
      "anchoring_urls": {
        "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
      },
      "resolution_method": "frost_anchored_resolved",
      "second_planting": {
        "start_indoors": "Jul 4 - Aug 3",
        "plant_out": "Aug 8 - Aug 29",
        "harvest_start": "Oct 12",
        "harvest_end": "Nov 5",
        "sources": ["vce_426_331"],
        "anchoring_urls": {
          "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
        }
      },
      "resolved_from": {"last_frost": "Apr 18", "first_frost": "Oct 22"},
      "heat_pause": {
        "months": [7, 8],
        "classification": "heat_pause",
        "basis_seasoned": "Summer gap is a heat exclusion, not a frost gap: this brassica's developing heads lose quality in hot, humid Piedmont summers, and plants in the head-formation stage bolt as temperatures climb (VCE 426-331).",
        "sources": ["vce_426_331"],
        "anchoring_urls": {
          "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
        }
      }
    }
  },
  "region_notes_beginner": "In the Piedmont and Coastal Plain, grow this crop twice: once in spring and again in fall, with a summer break in between when the heat and humidity stall head formation. Set out transplants a few weeks before your last frost for an early-summer harvest, then plant again in midsummer for a fall crop that is often the better of the two.",
  "region_notes_seasoned": "The Mid-Atlantic runs this brassica as two frost-bracketed crops around a real midsummer heat gap. Set spring transplants out about 3 weeks ahead of the last frost for a harvest before the hot, humid Piedmont and Coastal Plain summer sets in; a second planting goes out in midsummer, timed to head as nights cool in fall, and often out-yields the spring crop. Watch for the same heat-driven bolt risk VCE and NC State both flag for this belt; the fall crop is the more forgiving of the two here."
}
```

**Verified clean** (scratch script, both zone rows): `annual_coherence_violations` (token enum,
length, `heat_pause.months` <-> calendar alignment, folding in the real "action-over-passive" flip on
z8's Aug row, where the fall `start_indoors` action legitimately overrides the passive pause), `
annual_calendar_violations` (A24 placement -- no pause on a top-level active window),
`heat_pause_backing_violations` (A25 -- `heat_pause` carries months + basis + sourced URL), and
`second_planting_gate.check_crop` (A43, both rules A and B) -- **zero violations across all four
checks, both zone rows.**

### 2.5 Warm-season worked example -- the fall-cycle flagship (cherry-tomato content, standard wiring)

This is the crop class the whole region exists for. **Content** modeled on
`cherry-tomato.regions.se_gulf.z8`'s real fields (`weeks_indoors: 6, days_to_maturity_mid: 62,
dtm_anchor: from_transplant, frost_tolerance_f: 32` -- the exact generic values the ruling already
confirmed for cherry-tomato); **wiring** is the standard `frost_anchored_resolved` vocabulary (section
2.2), NOT `se_gulf`'s bespoke anchors. The z8 fall window (`second_planting.plant_out: "Jul 1 - Aug
10"`) is the **real, verbatim VCE 426-331 Table 4 zone-8 tomato fall date range** -- use it as written,
not a rounded approximation. z7's fall window is a clearly-plausible placeholder (VCE and the State
Climate Office both publish zone-7 tables; Task 3 replaces this with the real dates):

```json
{
  "region_id": "mid_atlantic",
  "region_label": "Mid-Atlantic: Piedmont and Coastal Plain",
  "zone_span": ["7", "8"],
  "sources": ["ncsu_ext", "vce_426_331"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "spring",
      "track": "beginner",
      "start_indoors": [
        {
          "from": "last_frost",
          "offset_days": -35,
          "window_days": 14,
          "synthesis_note_seasoned": "Start seed indoors about 6 weeks before spring set-out (NC State / VCE).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "plant_out": [
        {
          "from": "last_frost",
          "offset_days": 7,
          "window_days": 21,
          "synthesis_note_seasoned": "Set transplants out about a week after the last frost, once soil has warmed (NC State / VCE 426-331 Table 4).",
          "sources": ["ncsu_ext", "vce_426_331"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"},
            "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_start": [
        {
          "from": "plant_out",
          "offset_days": 62,
          "window_days": 14,
          "synthesis_note_seasoned": "Cherry tomatoes begin ripening about 62 days after transplanting (NC State / VCE).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_end": [
        {
          "from": "plant_out",
          "offset_days": 76,
          "window_days": 0,
          "synthesis_note_seasoned": "The spring crop's harvest winds down as the hot, humid Piedmont and Coastal Plain midsummer sets in and fruit set stalls (NC State / VCE).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "anchoring_urls": {}
    },
    {
      "succession_id": 2,
      "label": "fall",
      "track": "second_planting",
      "start_indoors": [
        {
          "from": "plant_out",
          "offset_days": -60,
          "window_days": 40,
          "synthesis_note_seasoned": "For the fall crop, start seed indoors roughly 6 weeks ahead of the VCE-documented fall set-out window (VCE 426-331 Table 4).",
          "sources": ["vce_426_331"],
          "anchoring_urls": {
            "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "plant_out": [
        {
          "from": "first_frost",
          "offset_days": -105,
          "window_days": 40,
          "source_quote": "Zone 8a Fall: July 1-Aug 10 | Zone 8b Fall: July 1-Aug 10",
          "synthesis_note_seasoned": "Set the fall crop out from early July into mid-August, the explicit fall window VCE 426-331 Table 4 documents for zone 8 tomatoes; cherry and grape types suit this window well because of their shorter days to maturity (VCE 426-331).",
          "sources": ["vce_426_331"],
          "anchoring_urls": {
            "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_start": [
        {
          "from": "plant_out",
          "offset_days": 62,
          "window_days": 14,
          "synthesis_note_seasoned": "The fall crop begins ripening about 62 days after the late-summer transplant (NC State / VCE).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_end": [
        {
          "from": "first_frost",
          "offset_days": -2,
          "window_days": 0,
          "synthesis_note_seasoned": "The fall crop is harvested up to just ahead of the belt's real first frost, which kills tomato vines outright (NC State frost-date table).",
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          },
          "uscrn_validation": null
        }
      ],
      "anchoring_urls": {}
    }
  ],
  "plantings_provenance": null,
  "resolved_by_zone": {
    "8": {
      "plant_out": "Apr 15 - May 6",
      "start_indoors": "Mar 4 - Mar 18",
      "harvest": "Jun 16 - Jun 30",
      "harvest_start": "Jun 16",
      "harvest_end": "Jun 30",
      "first_plant_date": "Apr 15",
      "last_plant_date": "May 6",
      "calendar": ["cold_pause", "cold_pause", "indoors", "plant", "plant", "harvest", "plant", "plant", "harvest", "harvest", "cold_pause", "cold_pause"],
      "zone_notes": null,
      "planting_note": "multi_season",
      "sources": ["ncsu_ext"],
      "anchoring_urls": {
        "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
      },
      "resolution_method": "frost_anchored_resolved",
      "second_planting": {
        "start_indoors": "May 20 - Jun 29",
        "plant_out": "Jul 1 - Aug 10",
        "harvest_start": "Sep 1",
        "harvest_end": "Oct 28",
        "sources": ["vce_426_331"],
        "anchoring_urls": {
          "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
        }
      },
      "resolved_from": {"last_frost": "Apr 8", "first_frost": "Oct 30"},
      "heat_pause": {
        "months": [7, 8],
        "classification": "heat_pause",
        "basis_seasoned": "Summer sowing gap is a heat exclusion, not a frost gap: hot, humid Piedmont and Coastal Plain days and especially nights push tomato flowers to drop and fruit set to fail. Cherry types are heat resistant, so this pause is shorter for them than for large-fruited tomatoes, and the fall transplant window overlaps it directly (VCE 426-331; NC State Extension).",
        "sources": ["vce_426_331", "ncsu_ext"],
        "anchoring_urls": {
          "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"},
          "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
        }
      }
    },
    "7": {
      "plant_out": "Apr 25 - May 16",
      "start_indoors": "Mar 14 - Mar 28",
      "harvest": "Jun 26 - Jul 10",
      "harvest_start": "Jun 26",
      "harvest_end": "Jul 10",
      "first_plant_date": "Apr 25",
      "last_plant_date": "May 16",
      "calendar": ["cold_pause", "cold_pause", "indoors", "plant", "plant", "harvest", "harvest", "plant", "harvest", "harvest", "cold_pause", "cold_pause"],
      "zone_notes": null,
      "planting_note": "multi_season",
      "sources": ["vce_426_331"],
      "anchoring_urls": {
        "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
      },
      "resolution_method": "frost_anchored_resolved",
      "second_planting": {
        "start_indoors": "Jun 8 - Jul 8",
        "plant_out": "Jul 20 - Aug 10",
        "harvest_start": "Sep 20",
        "harvest_end": "Oct 20",
        "sources": ["vce_426_331"],
        "anchoring_urls": {
          "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
        }
      },
      "resolved_from": {"last_frost": "Apr 18", "first_frost": "Oct 22"},
      "heat_pause": {
        "months": [8],
        "classification": "heat_pause",
        "basis_seasoned": "Summer sowing gap is a heat exclusion, not a frost gap: hot Piedmont days and nights push tomato flowers to drop and fruit set to fail. Cherry types hold up better than large-fruited tomatoes, so the pause here is shorter than the Coastal Plain's (VCE 426-331).",
        "sources": ["vce_426_331"],
        "anchoring_urls": {
          "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
        }
      }
    }
  },
  "region_notes_beginner": "In the Piedmont and Coastal Plain you can grow cherry tomatoes twice a year, once in spring and again in fall, with a summer stretch in between when the heat and humidity make plants drop their flowers instead of setting fruit. Cherry tomatoes handle the heat better than big tomatoes, so plant your spring crop early enough to pick before the worst of it, then plant again in early to mid summer for a real fall crop, the reason this region has its own calendar at all.",
  "region_notes_seasoned": "The Piedmont and Coastal Plain run two cherry tomato seasons, spring and fall, split by a real midsummer heat window when high day and night temperatures cause blossom drop and fruit set to fail. Cherry types handle this better than large-fruited tomatoes: they are heat resistant and quick to mature, so a few varieties keep setting even as the pause begins. Virginia Cooperative Extension documents an explicit fall transplant window from early July into mid-August; NC State's own calendar shows continuous spring transplanting into early July. Time the spring crop to ripen before peak heat, then set the fall crop out in that same window for a harvest running up to the belt's real first frost. z7's shorter, cooler season narrows both windows slightly relative to z8's Coastal Plain. (NC State Extension; Virginia Cooperative Extension Pub. 426-331)"
}
```

**Verified clean** (scratch script, both zone rows): `annual_coherence_violations`,
`annual_calendar_violations` (A24), `heat_pause_backing_violations` (A25), and
`second_planting_gate.check_crop` (A43, rules A+B) all return **zero violations**. Note the z8 July
row: `heat_pause.months` includes 7, but the calendar shows `plant` for July, not `heat_pause` --
this is the legitimate "action-over-passive" flip (section 2.6), and it is not a placeholder
convenience -- it is exactly what `cherry-tomato.regions.se_gulf.z8`'s own real, certified calendar
already does for its own July row (`"plant"`, not `"heat_pause"`, even though `heat_pause.months`
there is `[7]`).

### 2.6 The `second_planting` shape, A43, and the action-over-passive flip

**A43's Rule A (the de-mux invariant), quoted from `tools/second_planting_gate.py`'s own docstring:**
*"a cell WITH `second_planting` must be single-span in `start_indoors`/`plant_out`/`harvest`, and its
envelope must sit INSIDE the primary windows: `harvest_end` must parse inside the FIRST harvest span,
`last_plant_date` inside the FIRST `plant_out` span (containment, not fall-value equality...)."* In
practice this means:

- The top-level `plant_out`, `start_indoors`, and `harvest` fields represent the **spring cycle
  only** -- a single date range each, never a comma-joined multi-span. The fall cycle's own
  `start_indoors` / `plant_out` / `harvest_start` / `harvest_end` live ONLY inside the nested
  `second_planting` object, exactly the shape `broccoli.regions.northern_tier`'s real z7 cell already
  uses (its top-level `harvest_end` is `"May 31"`, its `second_planting.harvest_end` is a completely
  separate `"Dec 4"` -- the two never merge).
  Because `harvest_end` and `last_plant_date` are themselves derived from those same top-level
  spring-only fields, the envelope-containment check is automatically satisfied as long as the cell
  is authored in this shape -- it is a structural guarantee, not something to hand-verify per crop.
- **A genuine open question for Task 4/5, flagged here rather than resolved:** VCE 426-331's own
  table literally labels its spring column `"April 10-July 1"` for zone 8a tomatoes -- a single
  continuous span running deep into what this doc's worked example treats as the pre-heat-pause
  window -- and NC State's own calendar shows continuous transplant markers through July 1. Read
  literally, this could mean VCE models tomato as one long CONTINUOUS succession-transplant window
  rather than a bounded spring cycle followed by a discrete gap. This doc's worked example takes the
  simpler, cleaner, gate-standard reading (a bounded spring cycle ending before the heat, then a
  discrete VCE-sourced fall window) because that is what the two-cycle `second_planting` shape is
  built for and what the brief's named templates (broccoli/cherry-tomato) both already do. If a
  future crop's real sourcing more strongly supports a genuine multi-wave succession model instead
  (the way `broccoli.regions.ca_north_coast`'s own five-wave continuous-succession shape differs from
  `northern_tier`'s simpler two-cycle one), that is a legitimate alternate shape already supported by
  the schema (a third `plantings[]` entry with `track: "succession"`, as `broccoli.northern_tier`
  itself already carries) -- but it is a per-crop call, not the default.
- **The action-over-passive flip, the single most important content-shape lesson from
  `cherry-tomato.regions.se_gulf.z8`'s real calendar:** a declared `heat_pause` month does not
  automatically render as the `heat_pause` token. If the SAME month is also genuinely when the fall
  transplant happens (backed by a real `plant_out` or `start_indoors` window touching that month),
  the calendar should show the backed action token (`plant` or `indoors`) instead, and
  `annual_coherence_violations`'s alignment check treats that as a legitimate "flip," not a mismatch
  (`flipped = hp & {months the stored calendar shows as indoors/plant}`; the required equality is
  `cal_hp == hp - flipped`). This is exactly why section 2.5's z8 July row shows `plant`, not
  `heat_pause`, even though July is a declared heat month -- the fall transplant genuinely starts
  then, per VCE's own dates, and showing the pause token instead would bury the more useful, more
  action-oriented signal.

### 2.7 Gates that bind this shape

A2 (region-fill completeness), A5/A5b/A5c (annual calendar coherence + indoors-run backing), A8
(`successions_realized`, if in scope), A24 (calendar-placement drift), A25 (`heat_pause` thermal
backing -- **the gate that matters most in THIS arc**, since an unsourced pause silently reshapes the
whole calendar, per design spec risk item 3), A31/A32 (region-roster + real-calendar floor -- A32
applies to `{frost_anchored, perennial_herbaceous, berries_woody, perennial_woody_ornamental}`, this
archetype's scope), **A43** (the de-mux/envelope invariant -- the gate most likely to see churn in
this arc per design spec risk item 4, since every authored fall cycle touches it), A45 (zone_span
exact-match, once `mid_atlantic` lands in `EXPECTED_SPANS`, Task 2). None of these are new gates for
Mid-Atlantic; they already run roster-wide.

---

## 3. Archetype 2 -- fruiting TREE cell

**Who gets this shape:** the chill-gated deciduous fruit -- apple, pear-european, pear-asian,
cherry-sweet, cherry-sour, plum, apricot, nectarine, peach, fig, mulberry, persimmon, and the two
warm-limited edge cases discussed below (14 crops total). **Tree fruit needs essentially no
correction in this belt** -- the ruling's own basket-crop check found real NC chill accumulation
clears the entire canonical apple variety range (max 900 hr, McIntosh) with margin, and no plausible
reading of "Mid-Atlantic z7/z8" predicts a chill deficit the way a bespoke region sometimes has to
correct for. The value here is in getting the REAL evidence into the dataset (a sourced
`region_chill_delivered` band, section 3.4's note), not in flipping any suitability class.

### 3.1 Cell-level keys

| Key | Shape | Note |
|---|---|---|
| `region_id` / `region_label` / `zone_span` / `sources` | as section 1 | |
| `plantings` | `[{...}]`, exactly ONE entry | `track: "perennial"`; no `start_indoors`, no `direct_sow`, no succession/`second_planting` (`perennial_gate.py` enforces a tree is planted once) |
| `resolved_by_zone` | `{"7": {...}, "8": {...}}` | |
| `region_notes_beginner` / `region_notes_seasoned` | string \| null | |
| `chill_basis_seasoned` / `chill_basis_beginner` | string | region-level chill narrative (chill-DELIVERED lives in the shared top-level `region_chill_delivered.mid_atlantic` table, not per-cell -- A18; this pair is the prose companion) |
| `plantings_provenance` | nullable | present, may be null |

### 3.2 `resolved_by_zone["7"|"8"]` keys

| Key | Note |
|---|---|
| `plant_out` | dormant-season bare-root/container window (absolute display string) |
| `resolution_method` | `"perennial_precompute"` |
| `suitability` | `"fruits_reliably"` for the mainstream set (the modal Mid-Atlantic verdict, per the ruling); `"marginal"` reserved for a genuine cool-summer-ripening or warm-limited caveat (see 3.4) |
| `suitability_note_seasoned` / `suitability_note_beginner` | dual-register honesty prose -- **the real nuance to carry here is NC State's own 750+-hour variety preference (3.4), not a chill-deficit caveat** |
| `bloom`, `harvest_start`, `harvest_end`, `harvest` | real display windows -- **`calendar[]` is DERIVED from these two fields** via `tools/tree_calendar.py:derive_tree_calendar(bloom, harvest)` (prune = month before bloom; bloom = bloom-open month; growing = bloom+1..harvest_start-1; harvest = the harvest span; care = the month after harvest end; dormant = the rest). Gate-enforced (`tree_calendar_violations`, A4): a stored calendar that does not equal the function's output on the cell's own `bloom`/`harvest` fields is a hard violation. **Do not hand-invent tree calendars; run the deriver (or its exact algorithm) against the authored bloom/harvest windows.** |
| `frost_risk_note_seasoned` | string |
| `resolved_from` | `{"last_frost": <date>, "first_frost": <date>, "chill_hours": [lo, hi]}` -- real frost dates AND a chill band (mirrors `apple.regions.northern_tier`'s shape exactly) |
| `sources`, `anchoring_urls` | required |

### 3.3 Full worked example -- `fruits_reliably` (apple pattern)

Modeled on `apple.regions.northern_tier.z7`'s real shape and offset method (`bloom` from
`last_frost` +7/window 21; `harvest_start` from `bloom_start` +120; `harvest_end` from `bloom_start`
+165), substituting Mid-Atlantic's frost dates. **The `>1,000 chilling hours annually` NC-wide floor
is real, sourced evidence** (NC State Extension Gardener Handbook ch. 15, quoted in the ruling); the
EXACT per-zone chill-band split below is an illustrative placeholder (z7 cooler/more chill than z8),
not yet sourced to a specific station -- Task 3 nails the real split, but the underlying floor is
already real and clears the entire canonical apple roster (max requirement 900 hr, McIntosh) either
way:

```json
{
  "region_id": "mid_atlantic",
  "region_label": "Mid-Atlantic: Piedmont and Coastal Plain",
  "zone_span": ["7", "8"],
  "sources": ["ncsu_ext", "vce_426_331"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "establishment",
      "track": "perennial",
      "plant_out": [
        {
          "label": "bare_root_dormant",
          "from": "last_frost",
          "offset_days": -60,
          "window_days": 45,
          "sources": ["ncsu_ext"],
          "anchoring_urls": {
            "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
          }
        }
      ],
      "bloom": [
        {
          "label": "primary",
          "from": "last_frost",
          "offset_days": 7,
          "window_days": 21,
          "sources": ["ext_org_apples"],
          "anchoring_urls": {
            "ext_org_apples": {"url": "https://apples.extension.org/timing-of-apple-tree-bloom/", "verified": "2026-07-20"}
          }
        }
      ],
      "harvest_start": [
        {"label": "primary", "from": "bloom_start", "offset_days": 120, "sources": ["ext_org_apples"],
         "anchoring_urls": {"ext_org_apples": {"url": "https://apples.extension.org/timing-of-apple-tree-bloom/", "verified": "2026-07-20"}}}
      ],
      "harvest_end": [
        {"label": "primary", "from": "bloom_start", "offset_days": 165, "sources": ["ext_org_apples"],
         "anchoring_urls": {"ext_org_apples": {"url": "https://apples.extension.org/timing-of-apple-tree-bloom/", "verified": "2026-07-20"}}}
      ],
      "anchoring_urls": {
        "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
      },
      "sources": ["ncsu_ext"]
    }
  ],
  "plantings_provenance": null,
  "resolved_by_zone": {
    "8": {
      "plant_out": "Dec - Feb (dormant, bare-root or container)",
      "resolution_method": "perennial_precompute",
      "suitability": "fruits_reliably",
      "suitability_note_seasoned": "Chill is never the limiter here: real accumulation exceeds 1,000 hours a year across the belt, clearing every variety in this guide with room to spare. NC State recommends favoring varieties needing 750 hours or more specifically because the real risk in a mild Coastal Plain winter is a warm spell pushing bloom too early, not a chill shortfall.",
      "suitability_note_beginner": "Apples do very well here. Winters are plenty cold for any variety; a warm spell in late winter is a bigger worry than not enough cold.",
      "bloom": "Apr 15 - May 6",
      "harvest_start": "Aug 13",
      "harvest_end": "Sep 27",
      "harvest": "Aug 13 - Sep 27",
      "calendar": ["dormant", "dormant", "prune", "bloom", "growing", "growing", "growing", "harvest", "harvest", "care", "dormant", "dormant"],
      "frost_risk_note_seasoned": "A late cold snap during an unusually early bloom is the real risk in this zone, not insufficient winter chill.",
      "resolved_from": {"last_frost": "Apr 8", "first_frost": "Oct 30", "chill_hours": [1000, 1300]},
      "sources": ["ncsu_ext"],
      "anchoring_urls": {
        "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
      }
    },
    "7": {
      "plant_out": "Dec - Feb (dormant, bare-root or container)",
      "resolution_method": "perennial_precompute",
      "suitability": "fruits_reliably",
      "suitability_note_seasoned": "The cooler Piedmont interior banks even more chill than the Coastal Plain, clearing the full canonical variety range with margin. The same NC State guidance applies: favor 750-hour-plus varieties to guard against premature bloom in a warm winter spell, not because chill is scarce.",
      "suitability_note_beginner": "Apples do very well here too, with an even colder, more reliable winter than the Coastal Plain.",
      "bloom": "Apr 25 - May 16",
      "harvest_start": "Aug 23",
      "harvest_end": "Oct 7",
      "harvest": "Aug 23 - Oct 7",
      "calendar": ["dormant", "dormant", "prune", "bloom", "growing", "growing", "growing", "harvest", "harvest", "harvest", "care", "dormant"],
      "frost_risk_note_seasoned": "Late frost during bloom is uncommon at this zone's typical bloom timing.",
      "resolved_from": {"last_frost": "Apr 18", "first_frost": "Oct 22", "chill_hours": [1200, 1500]},
      "sources": ["vce_426_331"],
      "anchoring_urls": {
        "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
      }
    }
  },
  "region_notes_beginner": "This is good apple country from the Piedmont to the coast. Winters bank plenty of cold for nearly any variety, so pick based on taste and use, not chill worries. Plant a bare-root or container tree while it is still dormant, sometime between late fall and late winter.",
  "region_notes_seasoned": "The Mid-Atlantic banks abundant winter chill, well over 1,000 hours a year across the belt, clearing the entire recommended variety range with margin. NC State's own guidance still favors varieties needing 750 hours or more, not because chill is short here but because the real risk in a mild winter spell is premature bloom, which a late freeze can then damage. Plant bare-root or container trees during the dormant season, from late fall through late winter, while the ground is workable.",
  "chill_basis_seasoned": "Mid-Atlantic winters bank abundant, reliable chill accumulation, in excess of 1,000 hours a year across the belt (NC State Extension), comfortably clearing the requirement of every variety in this guide. Chill is never the limiting factor here; the real risk NC State flags is a warm winter spell triggering premature bloom in a low-chill variety, ahead of a later hard freeze.",
  "chill_basis_beginner": "Winters here are plenty cold for this tree. Nearly any variety gets all the winter chill it needs; the bigger worry is an early warm spell tricking it into blooming too soon."
}
```

**Verified clean** (scratch script, both zone rows): `tree_calendar.derive_tree_calendar(bloom,
harvest)` run against each zone row's own `bloom`/`harvest` strings reproduces the stored `calendar[]`
array exactly, and `tree_calendar_violations` returns **zero violations** for both rows.

### 3.4 Notes on the other 13 chill-gated trees, pawpaw, and the 750-hour nuance

- **The 750-hour variety-preference nuance belongs in `suitability_note_seasoned`, not in a
  suitability downgrade.** NC State's real guidance (quoted in the ruling) is to plant varieties
  needing "750 hours or greater... to avoid premature bloom during warm winter spells" -- this is a
  cultivar-selection tip for a belt with AMPLE chill, the mirror image of a genuine chill-deficit
  caveat. Every `fruits_reliably` cell in this archetype should carry this nuance in prose (as
  section 3.3's worked example does), never render it as `"marginal"`.
- **Pawpaw is NATIVE here** -- a strength to state plainly in its own `suitability_note_beginner` /
  `_seasoned`, not an edge case requiring special handling. Do not import PNW's or another region's
  pawpaw framing (a heat/humidity-limited edge crop there); the Mid-Atlantic's real humid-continental
  climate is squarely inside pawpaw's native range.
- **Any genuinely heat/humidity-limited caveat for a Mid-Atlantic tree is source-driven, not
  assumed** (design spec section 5 explicitly expects none for the mainstream set). If Task 6's real
  sourcing pass finds one (a late-ripening variety struggling with humidity-driven disease pressure,
  for instance), author it the same way `docs/pnw_cell_contract.md` section 3.4 handles its own
  cool-summer-ripening delta: still `fruits_reliably` overall, the caveat lives in prose first,
  `suitability` enum second; reserve `"marginal"` for a genuine belt-wide fruiting-outcome concern, not
  a single late variety in the lineup being a stretch.

### 3.5 Gates that bind this shape

A3 (`perennial_gate.py` -- suitability enum membership, single perennial establishment entry,
`fruits_reliably`/`marginal` must carry a non-empty calendar), A4 (`tree_calendar_violations` --
`calendar[]` must equal `derive_tree_calendar(bloom, harvest)` exactly, not merely "close"), A18
(chill-delivered crop-invariance -- no per-crop `chill_hours_delivered`; the shared
`region_chill_delivered.mid_atlantic` table is Task 3's job, section 7), A31 (region-roster floor).
**A32 does NOT apply to trees** (`coverage_floor_gate.CALENDAR_PRESENCE_BASES` = `frost_anchored`,
`perennial_herbaceous`, `berries_woody`, `perennial_woody_ornamental` -- Archetype 1's scope, not the
tree archetypes; trees are exempt and governed by A3/A4 instead).

---

## 4. Archetype 3 -- cold-limited CITRUS cell (`perennial_evergreen`)

**Who gets this shape:** the 5 evergreen citrus (grapefruit, lemon, lime, mandarin-clementine,
orange-navel). Cold-limited, the same overall direction as `se_gulf`'s own citrus story (unlike
PNW's citrus, which is BOTH cold-limited and heat-poor) -- the Mid-Atlantic has ample summer heat for
the 3 heat-gated citrus, so cold alone decides the verdict here.

**Important, a correction to the shorthand used in the task brief:** `SUITABILITY_ENUM` in
`tools/perennial_gate.py` is exactly `{"fruits_reliably", "marginal", "survives_no_fruit",
"unsuitable"}` -- **there is no bare `"survives"` value.** Where the brief (or this doc's own prose
elsewhere) says "survives," the enum-correct value is **`"survives_no_fruit"`**. Using a literal
`"survives"` string fails A3 outright (not in the 4-value enum). This archetype's practical choices
are `"unsuitable"` (calendar MUST be empty -- the modal Mid-Atlantic verdict for most of this
roster) or `"survives_no_fruit"` (calendar optional -- for the z8 Tidewater container-culture case
discussed in 4.4).

### 4.1 Cell-level keys

| Key | Shape | Note |
|---|---|---|
| `region_id` / `region_label` / `zone_span` / `sources` | as section 1 | |
| `plantings` | `[{...}]`, exactly ONE entry, `track: "perennial"` | same tree-establishment constraint as Archetype 2 |
| `resolved_by_zone` | `{"7": {...}, "8": {...}}` | |
| `min_winter_temp_f` | `[lo, hi]` | region-level cold-damage band (the envelope across both zones) |
| `cold_basis_seasoned` / `cold_basis_beginner` | string | the region-level cold narrative -- **this is the primary honesty field for Mid-Atlantic citrus** |
| `heat_summer_basis` / `heat_basis_seasoned` / `heat_basis_beginner` | conditional | **only** for the 3 heat-gated citrus (grapefruit, mandarin-clementine, orange-navel -- crops carrying `"heat_accumulation"` in `gating_factors`), and **only required at the cell level when `suitability != "unsuitable"`**. Lemon/lime never carry these fields (`gating_factors: ["cold_hardiness"]` only). Unlike PNW (where heat is ALSO the limiter), the Mid-Atlantic's long, hot, humid summer is genuinely adequate heat for these crops -- cold is the sole reason the verdict stays low, so `heat_summer_basis` should read `"adequate"` or better wherever it is authored, never `"insufficient"`. |
| `plantings_provenance` | nullable | |

### 4.2 `resolved_by_zone["7"|"8"]` keys

| Key | Note |
|---|---|
| `plant_out` | display string, or `null` for the thin/`unsuitable` variant |
| `resolution_method` | `"perennial_evergreen_precompute"` |
| `suitability` | `"unsuitable"` is the modal verdict for this archetype in this belt |
| `suitability_note_seasoned` / `suitability_note_beginner` | dual-register honesty prose, cold-led |
| `min_winter_temp_f` | `[lo, hi]` per-zone (may mirror the region-level pair) |
| `heat_summer_basis` | conditional, heat-gated crops only, only when `suitability != "unsuitable"` |
| `bloom`, `harvest_start`, `harvest_end`, `harvest` | `null` for the `unsuitable` thin variant -- no calendar to derive from |
| `calendar` | `[]` for `unsuitable` -- **hard requirement**, `perennial_gate.py` lines 131-133 |
| `frost_risk_note_seasoned` | string |
| `resolved_from` | may be `{}` or omit frost/chill entirely (citrus is not chill-gated); cold is the only per-cell climate axis, living in `min_winter_temp_f`, not `resolved_from` |
| `sources`, `anchoring_urls` | required |

### 4.3 Full worked example -- `"unsuitable"`, cold-limited (orange-navel pattern)

Modeled on the real SHAPE of `orange-navel.regions.northern_tier` (the "too cold, empty calendar"
reference cell already in canonical: `suitability: "unsuitable"` all zones, `min_winter_temp_f: []`,
`calendar: []`) with the PROSE REGISTER of the real `orange-navel.regions.se_gulf.z8` cell (a genuine
cold/heat-honesty citrus cell one zone warmer than this one), substituting Mid-Atlantic's real
frost dates and a plausible, colder `min_winter_temp_f` band (illustrative, not yet sourced to a
specific NC/VA winter-extreme record):

```json
{
  "region_id": "mid_atlantic",
  "region_label": "Mid-Atlantic: Piedmont and Coastal Plain",
  "zone_span": ["7", "8"],
  "sources": ["ncsu_ext"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "establishment",
      "track": "perennial",
      "plant_out": [],
      "bloom": [],
      "harvest_start": [],
      "harvest_end": [],
      "anchoring_urls": {}
    }
  ],
  "resolved_by_zone": {
    "8": {
      "plant_out": null,
      "resolution_method": "perennial_evergreen_precompute",
      "suitability": "unsuitable",
      "suitability_note_seasoned": "Even the Coastal Plain's milder z8 pockets see occasional hard freezes into the teens and low 20s degrees Fahrenheit, well below this crop's wood-damage threshold, in a belt with a real, frost-anchored winter rather than the near-frost-free zone this crop actually needs. Ample summer heat is not the limiter; winter cold is. A container tree brought fully indoors for the coldest nights is the only realistic way to grow this here.",
      "suitability_note_beginner": "This will not survive outdoors here, even in the milder Coastal Plain. Our winters get too cold in a hard freeze. If you want this in the Mid-Atlantic, grow it in a container you bring fully indoors for winter.",
      "min_winter_temp_f": [15, 22],
      "bloom": null,
      "harvest_start": null,
      "harvest_end": null,
      "harvest": null,
      "calendar": [],
      "frost_risk_note_seasoned": "A hard freeze most winters, not just an occasional Arctic outbreak, is what rules this crop out outdoors here.",
      "resolved_from": {},
      "sources": ["ncsu_ext"],
      "anchoring_urls": {
        "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
      }
    },
    "7": {
      "plant_out": null,
      "resolution_method": "perennial_evergreen_precompute",
      "suitability": "unsuitable",
      "suitability_note_seasoned": "The cooler Piedmont interior is colder still than the Coastal Plain in winter, with hard freezes an every-winter event, well below this crop's wood-damage threshold. Not a viable outdoor planting anywhere in this zone.",
      "suitability_note_beginner": "This will not survive outdoors here. Winters are too cold, even more so than the Coastal Plain.",
      "min_winter_temp_f": [8, 18],
      "bloom": null,
      "harvest_start": null,
      "harvest_end": null,
      "harvest": null,
      "calendar": [],
      "frost_risk_note_seasoned": "A hard freeze every winter, not an occasional event, rules this crop out here.",
      "resolved_from": {},
      "sources": ["vce_426_331"],
      "anchoring_urls": {
        "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
      }
    }
  },
  "region_notes_beginner": "Skip this outdoors in the Mid-Atlantic, in both the Coastal Plain and the Piedmont. Winters get too cold in a hard freeze most years. Grow it in a container and bring it fully indoors for winter if you want to try.",
  "region_notes_seasoned": "The Mid-Atlantic has a real, frost-anchored winter this crop cannot tolerate outdoors, in either zone of this belt. Summer heat is ample; winter cold decides the case on its own. Container culture with full winter cover indoors is the only realistic path; some z8 Tidewater growers do attempt exactly this (section 4.4) -- but this is not outdoor citrus country.",
  "min_winter_temp_f": [8, 22],
  "cold_basis_seasoned": "Mid-Atlantic winters bring real hard freezes well below this crop's wood-damage threshold in both zones of the belt, the Piedmont colder and more consistently so than the Coastal Plain. This is a genuine frost-anchored winter, not an occasional-outbreak risk the way a warmer citrus-adjacent belt might see it.",
  "cold_basis_beginner": "Winters here get properly cold most years, cold enough to kill this tree if left outdoors.",
  "plantings_provenance": null
}
```

**Verification note:** an empty `calendar: []` needs no calendar-derivation check (both
`tree_calendar_violations` and A32 are no-ops on an empty calendar / non-annual basis); the binding
check for this shape is `perennial_gate.py`'s own `unsuitable -> calendar must be empty` rule, which
this worked example satisfies by construction.

### 4.4 The z8 Tidewater container-culture delta -- `"survives_no_fruit"`, source it rather than refusing flatly

Design spec section 5 and the design spec's own app-handoff section both flag that "some container
culture is real in z8 Tidewater" for citrus -- source it rather than defaulting the whole roster to
`"unsuitable"`. Since citrus is NOT chill-gated (`chill_hours` is not in a `perennial_evergreen`
crop's `gating_factors`), `perennial_gate.py`'s chill Goldilocks-band split never fires for
`"survives_no_fruit"` here, the same point PNW's own contract makes at its section 5.5: a cold-only
evergreen's `survives_no_fruit` verdict may legally carry either an empty calendar or a real, thin
bloom-only calendar, both honest. If Task 6's real NC/VA sourcing finds genuine container-culture
practice specific to the milder Tidewater z8 pockets (protected microclimates, active winter
protection), author that zone's cell `"survives_no_fruit"` instead of `"unsuitable"` rather than
flattening the whole roster to the simpler verdict -- follow the source, not the path of least
authoring effort.

### 4.5 Heat-gated delta -- grapefruit / mandarin-clementine / orange-navel vs lemon / lime

Orange-navel, grapefruit, and mandarin-clementine carry `"heat_accumulation"` in `gating_factors`;
lemon and lime do not. Per `perennial_gate.py`'s heat floor: a heat-gated crop's cell must carry
`heat_summer_basis` whenever `suitability != "unsuitable"`. Since section 4.3's worked example is
`"unsuitable"` throughout, the heat floor never triggers there and `heat_summer_basis`/`heat_basis_*`
are correctly omitted. **If Task 6 lands a `"survives_no_fruit"` verdict for any zone (4.4), that
cell (and the region-level pair) MUST add `heat_summer_basis`** (one of `HEAT_BASIS_ENUM = {"high",
"adequate", "marginal", "insufficient"}` -- almost certainly `"high"` or `"adequate"` for the
Mid-Atlantic's long, hot, humid summer, the opposite of PNW's own `"insufficient"` verdict) plus
`heat_basis_seasoned` + `heat_basis_beginner`. Lemon and lime never carry these fields regardless of
verdict.

### 4.6 Gates that bind this shape

A3 (`unsuitable` -> calendar MUST be empty; heat floor requires `heat_summer_basis` on the 3
heat-gated crops whenever `suitability != "unsuitable"`), A31 (region-roster floor -- present even
though `unsuitable`). A32 does not apply (trees/citrus exempt, per section 3.5). A4/
`tree_calendar_violations` is a no-op here because the calendar is empty.

---

## 5. Archetype 4 -- BERRY cell (blueberry, `berries_woody`)

**Who gets this shape:** blueberry, the sole `berries_woody` crop today (blackberry/raspberry are a
separate `cane_type`-routed sub-form of the same archetype but are not templated in this doc; see
section 7). **Berries are strong and well documented in this belt** -- NC is genuine native highbush
AND rabbiteye range, and this is the ONE archetype where the region-specific
`recommended_type` decision is genuinely two-way, unlike PNW (northern_highbush only) or `se_gulf`
(rabbiteye only).

### 5.1 Cell-level keys

Identical shape to `blueberry.regions.northern_tier`'s real cell: `region_id`, `region_label`,
`zone_span`, `sources`, `plantings` (one perennial establishment entry, list-of-month-name shape is
also legal per the real cell, see Appendix), `plantings_provenance`, `resolved_by_zone`,
`region_notes_beginner`, `region_notes_seasoned`.

### 5.2 `resolved_by_zone["7"|"8"]` keys

| Key | Note |
|---|---|
| `plant_out`, `harvest`, `harvest_start`, `harvest_end` | absolute display strings |
| `calendar` | required, 12 tokens -- **DERIVED, dispatched on `leaf_habit`** via `tools/berry_woody_calendar.py:derive_berry_woody_calendar(leaf_habit, cell)`. `leaf_habit == "deciduous"` reuses the tree cycle exactly (`derive_tree_calendar`: dormant/prune/bloom/growing/harvest/care); `leaf_habit == "evergreen"` uses a year-round `growing` filler with bloom/harvest/care, no `dormant`, no `season_over`. Gate-enforced (`berry_woody_calendar_violations`, A16): stored must equal derived for any non-empty calendar. |
| `resolution_method` | `"berries_woody_precompute"` |
| `recommended_type` | one of `{"northern_highbush", "southern_highbush", "rabbiteye"}` (the `BUSH_TYPE_ENUM`) -- **single value per cell**, not a list, even where the real regional guidance genuinely supports more than one type across different zones of the same region (5.3 below) |
| `leaf_habit` | one of `{"deciduous", "evergreen"}` -- **this is regional-winter-severity-dependent, NOT fixed by `recommended_type` alone** (5.3 below); it selects which derivation function runs |
| `type_note_seasoned` / `type_note_beginner` | the highbush-vs-rabbiteye steer prose |
| `bloom` | display string |
| `frost_risk_note_seasoned` | string |
| `resolved_from` | `{"last_frost": <date>, "first_frost": <date>}` |
| `grown_as_note_seasoned` / `grown_as_note_beginner` | the lifecycle-narrative prose pair (register_fill's own required set) |
| `sources`, `anchoring_urls` | required |

### 5.3 The highbush/rabbiteye per-zone decision -- real evidence, genuinely two-way, deferred to Task 6/7

**This is the one place this contract deliberately does NOT lock a single answer**, because the real
evidence supports different picks for the two zones and `recommended_type` is single-valued per cell
(the `berries_woody_gate.py` type-COVERAGE invariant requires every per-cell `recommended_type` to
have at least one matching variety, but a cell cannot declare two types at once):

- **The real, already-canonical variety-to-type mapping** (read directly off `blueberry`'s live
  `varieties.recommended` list): Duke, Bluecrop, Patriot, Jersey, Northblue, Northland =
  `northern_highbush`; Emerald, Jewel, Sharpblue = `southern_highbush`; Premier, Powderblue,
  Brightwell, Tifblue = `rabbiteye`.
- **NC State's real guidance** (quoted in the ruling): "Growing Blueberries in the Home Garden" names
  Duke and Jersey for the Coastal Plain highbush pick and Premier (among others) for Coastal
  Plain/Piedmont/Foothills rabbiteye, calling rabbiteye "the best choice for most soils below 2,500
  ft elevation in NC" -- essentially the whole belt. A second NC Cooperative Extension source
  (Brunswick County Center) gives rabbiteye a 400-600 chill-hour requirement and calls Coastal Plain
  cultivars in the 350-1,000 chill-hour range the ones that "do best."
- Since Duke and Jersey map to the ALREADY-canonical `northern_highbush` type (not
  `southern_highbush`), and Premier maps to `rabbiteye`, both real NC State picks are already
  representable in the existing `BUSH_TYPE_ENUM` -- **no new type value is needed.** The genuinely
  open call for Task 6/7 is which type to name as the SINGLE `recommended_type` per zone: a plausible
  split (not decided here) is `northern_highbush` for the cooler z7 Piedmont interior (closer to
  where `northern_tier`'s own real cell already recommends it) and `rabbiteye` for the warmer z8
  Coastal Plain (closer to where `se_gulf`'s own real cell recommends it, per the elevation-below-
  2,500-ft framing) -- but NC State's own source names Duke/Jersey for the Coastal Plain specifically
  too, so this is a real per-source judgment call, not a mechanical rule. Whichever type is NOT
  named as `recommended_type` for a given zone should still be discussed honestly in
  `type_note_seasoned` (the way a good steer names the runner-up), matching the register PNW and
  `se_gulf`'s own cells already use.
- **`leaf_habit` is regional-winter-severity-dependent, not fixed by botanical type.** The real,
  already-shipped `blueberry.regions.se_gulf.z8` cell tags `rabbiteye` as `leaf_habit: "evergreen"`
  specifically because that region's winter is mild enough for rabbiteye to hold its leaves nearly
  year-round; the real `blueberry.regions.northern_tier.z7` cell tags `northern_highbush` as
  `leaf_habit: "deciduous"` because that region has a genuine winter. **The Mid-Atlantic has a real,
  frost-anchored winter in both zones** (unlike `se_gulf`'s near-frost-free z8-10 span), so the
  expected default here is `leaf_habit: "deciduous"` regardless of which type wins the
  `recommended_type` call -- including for `rabbiteye`, which is botanically deciduous nearly
  everywhere except the mildest winters. A `rabbiteye` + `deciduous` cell is a genuinely new
  combination not yet present anywhere in the canonical roster (5.4's worked delta verifies it
  computes cleanly through the real deriver).

### 5.4 Worked examples

**z7 -- modeled directly on the real, currently-certified `blueberry.regions.northern_tier.z7` cell**
(`northern_highbush`, `deciduous`), frost dates swapped to this belt's own z7 placeholder:

```json
{
  "plant_out": "March to April",
  "harvest": "late June to August",
  "harvest_start": "late June",
  "harvest_end": "August",
  "calendar": ["dormant", "dormant", "prune", "bloom", "growing", "harvest", "harvest", "harvest", "care", "dormant", "dormant", "dormant"],
  "sources": ["vce_426_331"],
  "anchoring_urls": {
    "vce_426_331": {"url": "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "verified": "2026-07-20"}
  },
  "resolution_method": "berries_woody_precompute",
  "recommended_type": "northern_highbush",
  "leaf_habit": "deciduous",
  "type_note_seasoned": "Northern highbush is the classic pick for the cooler Piedmont interior. It needs real winter chill and a true dormancy, which this zone provides, and Duke and Jersey (both northern highbush) are among NC State's own named picks for this belt.",
  "type_note_beginner": "Northern highbush is a good match for the cooler part of this region. It wants a real cold winter rest, which it gets here.",
  "bloom": "April to May",
  "frost_risk_note_seasoned": "Blooms late enough to escape most spring frosts here; a hard late freeze on open bloom is an occasional risk, so good air drainage helps.",
  "resolved_from": {"last_frost": "Apr 18", "first_frost": "Oct 22"},
  "grown_as_note_seasoned": "Northern highbush is a permanent deciduous shrub here, planted once and productive for decades. It rests fully dormant through winter, then breaks bud and blooms in spring, when an open flower can still be caught by a late freeze. Fruit sets and ripens across summer. After leaf drop, prune late in the dormant season, just before bud break.",
  "grown_as_note_beginner": "Your blueberry bush is a long-lived planting you set once and keep for many years. It loses its leaves and rests all winter, then flowers in spring, where a late frost can still catch the open blooms in a cold year. Berries ripen through summer. Prune it in late winter, just before the buds open."
}
```

**z8 delta -- `rabbiteye`, still `deciduous`** (the genuinely new combination, NC Coastal Plain
pattern, real frost dates):

```json
{
  "plant_out": "March to April",
  "harvest": "June to mid-July",
  "harvest_start": "June",
  "harvest_end": "mid-July",
  "calendar": ["dormant", "prune", "bloom", "growing", "growing", "harvest", "harvest", "care", "dormant", "dormant", "dormant", "dormant"],
  "sources": ["ncsu_ext"],
  "anchoring_urls": {
    "ncsu_ext": {"url": "https://content.ces.ncsu.edu", "verified": "2026-07-20"}
  },
  "resolution_method": "berries_woody_precompute",
  "recommended_type": "rabbiteye",
  "leaf_habit": "deciduous",
  "type_note_seasoned": "Rabbiteye is NC State's own top pick for most of the Coastal Plain, including Premier among its named cultivars. Unlike the milder Deep South, this belt has a real winter, so rabbiteye drops its leaves and rests fully dormant here rather than holding them nearly year-round the way it can farther south.",
  "type_note_beginner": "Rabbiteye is the type NC State recommends for most of this area. Here it loses its leaves and rests over winter like a typical fruit bush, unlike in the much milder Deep South where it can stay nearly evergreen.",
  "bloom": "March",
  "frost_risk_note_seasoned": "Rabbiteye blooms later than highbush and usually escapes spring freezes; a warm late-winter spell can still push bloom early in a mild year.",
  "resolved_from": {"last_frost": "Apr 8", "first_frost": "Oct 30"},
  "grown_as_note_seasoned": "Rabbiteye is a permanent deciduous shrub in this belt's real winter, planted once and productive for decades. It rests dormant and leafless through winter, then blooms in early spring, sets fruit, and ripens across early summer. After leaf drop, prune late in the dormant season, just before bud break. It needs a second, different rabbiteye variety nearby to cross-pollinate and set a crop.",
  "grown_as_note_beginner": "Your rabbiteye blueberry is a long-lived bush you plant once and keep for many years. Here it loses its leaves and rests over winter like a typical fruit bush. It flowers early in spring and ripens berries by early summer. One key point: plant a second, different rabbiteye variety nearby so the two can pollinate each other and make fruit."
}
```

**Verified clean** (scratch script, both rows): `derive_tree_calendar(bloom, harvest)` (the SAME
function the deciduous branch of `derive_berry_woody_calendar` dispatches to) reproduces each stored
`calendar[]` exactly, and `berry_woody_calendar_violations` returns **zero violations** for both,
including the z8 `rabbiteye` + `deciduous` combination.

### 5.5 Gates that bind this shape

A15 (`berries_woody_gate.py` -- lifecycle scalars present, `gating_factors` retains `chill_hours`,
woody-specific prose pairs non-null, `self_fertile` false + no tree cross-pollination machinery,
no tree-only key (`suitability`) on the cell, `recommended_type`/`leaf_habit` typed against the
enum, the type-COVERAGE invariant -- every per-cell `recommended_type` must have >=1 matching
variety, which both `northern_highbush` and `rabbiteye` already do off the existing canonical
`blueberry.varieties.recommended` list), A16 (`berry_woody_calendar_violations` -- calendar ==
`derive_berry_woody_calendar(leaf_habit, cell)` exactly), A18 (chill-delivered crop-invariance, same
shared-table rule as trees), A31 (region-roster floor), **A32 applies** (`berries_woody` is in
`CALENDAR_PRESENCE_BASES` -- unlike trees, a `berries_woody` cell needs a real, non-empty calendar).

---

## 6. Cross-archetype pre-flight checklist (Tasks 4-7, before handoff)

- [ ] `region_id` = `"mid_atlantic"`, `region_label` = `"Mid-Atlantic: Piedmont and Coastal Plain"`
      verbatim, no em dash
- [ ] `zone_span` = `["7","8"]`; `resolved_by_zone` keys are exactly `{"7","8"}`
- [ ] Annual/herb/berry/strawberry archetype: `resolution_method = "frost_anchored_resolved"`,
      `resolved_from` carries REAL `last_frost`/`first_frost` dates (never null); `plantings[]`
      anchors to `last_frost`/`first_frost`/`plant_out`, **never** `se_gulf`'s bespoke
      `plant_out_start`/`heat_pause_start`/`heat_pause_end` vocabulary
- [ ] Cool-season crops get long spring-and-fall shoulders and carry NO `heat_pause` unless a
      specific crop's own T1 evidence says otherwise
- [ ] Warm-season crops: `heat_pause` where the T1 evidence genuinely supports a real midsummer
      set-failure period (expected common here -- source it per crop, never assume it), plus a real
      `second_planting` where VCE/NC State document one. **Which crops get a fall cycle is a per-crop
      T1 call** -- do not extrapolate from tomato to its neighbors without checking VCE's own tables
- [ ] `cold_pause` IS legitimate and expected on a Mid-Atlantic annual's winter months (this is a real
      frost-anchored belt, not `se_gulf`'s near-frost-free one)
- [ ] **A43 envelope invariant**: any cell carrying `second_planting` is single-span in its top-level
      `start_indoors`/`plant_out`/`harvest`; the fall cycle's OWN windows live only inside the nested
      `second_planting` object; `harvest_end`/`last_plant_date` sit inside the FIRST (spring) window
      by construction
- [ ] The "action-over-passive" flip: a declared `heat_pause` month backed by a real `plant`/`indoors`
      action that month shows the ACTION token, not the passive `heat_pause` token (section 2.6)
- [ ] `calendar[]` is internally coherent with the window fields: for a single-cycle annual, matches
      `tools/annual_calendar.py:derive_annual_calendar()`'s literal output; for a `second_planting`-
      bearing (multi-cycle) annual, hand-verified against `annual_coherence_violations` +
      `annual_calendar_violations` + `heat_pause_backing_violations` (the naive deriver does not fold
      `second_planting`'s own windows in -- section 2.6); for any tree/citrus/berry non-empty
      calendar, EQUALS `tools/tree_calendar.py:derive_tree_calendar()` (trees, and the deciduous
      branch of berries) or `tools/berry_woody_calendar.py`'s evergreen branch, run against the
      cell's own `bloom`/`harvest` fields -- never hand-typed independently of the dates
- [ ] Tree/citrus archetype: `plantings[]` has exactly one entry, `track: "perennial"`, no
      `start_indoors`/`direct_sow`/succession/`second_planting`
- [ ] Fruiting tree (Archetype 2): `suitability` = `"fruits_reliably"` (modal here -- real >1,000 hr
      chill clears the whole canonical variety range) or `"marginal"` (a genuinely sourced caveat,
      expected rare); the 750-hour NC State variety-preference nuance belongs in prose, never a
      suitability downgrade; pawpaw is framed as NATIVE, a strength
- [ ] Citrus (Archetype 3): `suitability` in `{"unsuitable", "survives_no_fruit"}` (modal:
      `"unsuitable"`) -- **never the bare word "survives"**, the enum-correct form is
      `"survives_no_fruit"`; `unsuitable` -> calendar MUST be `[]`; z8 Tidewater container culture is
      a real, sourceable `survives_no_fruit` case, not a default
- [ ] Heat-gated citrus only (grapefruit, mandarin-clementine, orange-navel): carries
      `heat_summer_basis` + `heat_basis_*` whenever `suitability != "unsuitable"`, and the verdict
      should read `"high"`/`"adequate"` here (ample summer heat), never `"insufficient"`; lemon/lime
      never carry these fields regardless of verdict
- [ ] Berry (Archetype 4): `recommended_type` is single-valued per cell from `{"northern_highbush",
      "southern_highbush", "rabbiteye"}`, backed by >=1 matching canonical variety; `leaf_habit` is
      `"deciduous"` by default here (this belt has a real winter in both zones), independent of which
      type is named -- do not import `se_gulf`'s evergreen-rabbiteye assumption
- [ ] Every rule entry and zone-row carries real `sources` + `anchoring_urls` (T1 -- `ncsu_ext` /
      `vce_426_331` are already catalogued; expect few or no new `source_catalog` entries)
- [ ] No em dashes in any `*_note_*`/`region_notes_*`/`chill_basis_*`/`cold_basis_*`/`type_note_*`
      prose; American English; `°F`; "plant" lowercase outside sentence-start
- [ ] Splice is compact JSON (no `indent=2`, no trailing newline) when it lands in the canonical

---

## 7. Out of scope (owned by a different task/session)

This doc is the **per-crop cell** contract for the 4 archetypes the brief named (annual, tree,
citrus, berry) only. It does NOT cover:

- `zone_span_gate.EXPECTED_SPANS["mid_atlantic"]` (the top-level span registration that makes A45
  accept `mid_atlantic` cells at all) and `region_cell_audit.py`'s `REGION_CONFIG["mid_atlantic"]`
  entry -- both Task 2 (`.superpowers/sdd/ma-task-2-brief.md` is already written for this).
- `region_chill_delivered.mid_atlantic` + `region_chill_delivered_provenance` (the shared chill-band
  table Archetype 2's fruiting calls are consistent with -- design spec section 4.6, Task 3). The
  real `>1,000 hr` NC-wide floor is already sourced (the ruling); the exact per-zone band split used
  in this doc's own apple worked example (section 3.3) is an illustrative placeholder pending that
  task.
- The 5 `perennial_woody_ornamental` crops (rosemary/oregano/sage/thyme/lavender) and the 1
  `perennial_herbaceous` crop (strawberry). Design spec section 5 flags that humidity, not cold, is
  their real Mid-Atlantic constraint (`se_gulf`'s own humidity-struggle framing is the closer analog
  than PNW's), but neither archetype was in the brief's named extraction list for this task, and
  neither has its own worked example here. A later task should pull `se_gulf`'s own real cells for
  these classes as its precedent, the same way this doc pulled `broccoli`/`cherry-tomato`/`apple`/
  `orange-navel`/`blueberry`.
- `region_source_map` (build-time authoring infrastructure, not a runtime-read field).
- The generalized `tools/region_harness.py` / `tools/region_cell_audit.py` /
  `tools/build_region_promote.py` (already region-generic per the design spec section 7; Task 2
  registers `mid_atlantic` in them, no rewrite needed) and the state-trio / footprint audit at
  promote (a later task).
- The z7 delivery dependency -- plant-app's `zones.ts:resolveFromZip` onboarding-assignment fix
  (`docs/kickoffs/32-plant-app-temperate-region-resolution.md`), a plant-app concern, not a dataset
  concern. The dataset should be correct ahead of the consumer, per precedent (RGV and PNW both
  shipped before their own app-side fences/fixes landed).
- Any plant-app `REGION_STATES`/`regions.json` wiring or plant-astro consumption.

See the design spec for all of the above.

---

## Appendix -- reference-cell key sets captured 2026-07-20 (canonical `e1e01c47`)

```
broccoli.regions.northern_tier
  cell keys: region_id, region_label, zone_span, sources, plantings, plantings_provenance,
             resolved_by_zone, region_notes_beginner, region_notes_seasoned
  plantings[]: THREE entries in the real cell -- succession_id 1 "spring" (track: beginner),
             2 "fall" (track: second_planting), 3 "succession" (track: succession, content
             duplicates the spring entry) -- the third entry is not required by this contract's
             simpler two-cycle shape; flagged as a real-cell oddity, not a pattern to copy blind.
  zone-row keys: plant_out, start_indoors, harvest, harvest_start, harvest_end, first_plant_date,
             last_plant_date, calendar, notes, zone_notes, planting_note, sources, anchoring_urls,
             resolution_method, second_planting, succession_spring, succession_fall, resolved_from,
             successions_realized, heat_pause (present z5-z7, absent z3-z4 -- the belt's warmer
             zones need it, the colder ones don't)
  resolution_method: frost_anchored_resolved; resolved_from real per zone (z7: last_frost "Mar 15",
             first_frost "Nov 15"); z7's real sources list includes umd_ext_broccoli (University of
             Maryland Extension) -- see section 1's callout, this is genuinely partial Mid-Atlantic
             content filed under a different region tag today.

cherry-tomato.regions.se_gulf
  cell keys: region_id, region_label, zone_span, sources, plantings, resolved_by_zone,
             region_notes_beginner, region_notes_seasoned, plantings_provenance
  zone-row keys (z8): plant_out, start_indoors, harvest, harvest_start, harvest_end,
             first_plant_date, last_plant_date, calendar, zone_notes, planting_note, sources,
             anchoring_urls, resolution_method, heat_pause, second_planting -- NOTE: no top-level
             `notes` key (unlike northern_tier's three-key notes/zone_notes/planting_note set) and
             a BESPOKE resolution_method ("se_gulf_month_resolution") with se_gulf-only plantings[]
             anchor tokens (plant_out_start, heat_pause_start, heat_pause_end) -- do not carry either
             of those two things into a mid_atlantic cell (section 1's callout); the real z8
             calendar's July token is "plant" (not "heat_pause"), the action-over-passive flip this
             contract's section 2.6 leans on.

apple.regions.northern_tier
  cell keys: region_id, region_label, zone_span, sources, plantings, plantings_provenance,
             resolved_by_zone, region_notes_beginner, region_notes_seasoned, chill_basis_seasoned,
             chill_basis_beginner
  zone-row keys: plant_out, resolution_method, suitability, suitability_note_seasoned,
             suitability_note_beginner, bloom, harvest_start, harvest_end, harvest, calendar,
             frost_risk_note_seasoned, resolved_from, sources, anchoring_urls
  resolution_method: perennial_precompute; resolved_from carries last_frost + first_frost +
             chill_hours together (z7: last_frost "Apr 5", first_frost "Oct 25", chill_hours
             [700,1100] -- this contract's apple worked example uses a HIGHER band, [1000,1300]/
             [1200,1500], reflecting the ruling's real >1,000 hr NC-wide evidence, deliberately not
             copied verbatim from northern_tier's own lower band).

orange-navel.regions.se_gulf
  cell keys: + min_winter_temp_f, heat_summer_basis (z8, heat-gated: this crop carries
             "heat_accumulation" in gating_factors), region-level + cold_basis_seasoned/beginner,
             heat_basis_seasoned/beginner, plantings_provenance
  suitability: "marginal" at z8 -- a COLD-limited marginal one zone warmer than this contract's own
             belt (frost-safe-ish but a hard freeze is a real risk); this contract's own worked
             example (section 4.3) goes one notch further to "unsuitable" for both mid_atlantic
             zones, since z7/z8 here are colder than se_gulf's own z8.

orange-navel.regions.northern_tier
  suitability: "unsuitable" all zones, min_winter_temp_f: [] every zone, calendar: [] every zone --
             the real "too cold, empty calendar" citrus reference cell; this contract's section 4.3
             worked example's SHAPE (null plant_out/bloom/harvest, empty calendar, empty
             plantings[] sub-lists) is modeled directly on this cell.

blueberry.regions.northern_tier
  cell keys: region_id, region_label, zone_span, sources, plantings, plantings_provenance,
             resolved_by_zone, region_notes_beginner, region_notes_seasoned
  plantings[]: ONE entry, track: perennial, but its sub-fields are LIST-OF-MONTH-NAME strings
             (e.g. plant_out: ["March","May"]) rather than the offset-object shape trees/citrus use
             -- both shapes are legal for this archetype's rule layer; the RESOLVED layer (below) is
             the load-bearing render layer either way.
  zone-row keys (z7): plant_out, harvest, harvest_start, harvest_end, calendar, sources,
             anchoring_urls, resolution_method, recommended_type, leaf_habit, type_note_seasoned,
             type_note_beginner, bloom, frost_risk_note_seasoned, resolved_from,
             grown_as_note_seasoned, grown_as_note_beginner
  resolution_method: berries_woody_precompute; recommended_type "northern_highbush", leaf_habit
             "deciduous"; resolved_from {last_frost "Mar 15", first_frost "Nov 15"}.

blueberry.regions.se_gulf
  zone-row keys (z8): SAME set as northern_tier's z7 row.
  resolution_method: berries_woody_precompute; recommended_type "rabbiteye", leaf_habit
             "evergreen" (that region's mild winter lets rabbiteye hold its leaves nearly year
             round -- this contract's own section 5.3/5.4 explicitly does NOT carry the
             rabbiteye-implies-evergreen assumption into mid_atlantic, since this belt has a real
             winter in both zones); calendar uses the year-round growing/bloom/harvest/care
             vocabulary, no dormant token, matching derive_evergreen_berry_woody_calendar's shape.
```

Gate logic cross-referenced: `tools/whole_crop_gate.py` (A2, A3, A4, A5/A5b/A5c, A8, A15, A16, A18,
A24, A25, A31/A32, A43, A45), `tools/annual_calendar.py` (`derive_annual_calendar`,
`annual_calendar_violations`, `annual_coherence_violations`, `heat_pause_backing_violations`),
`tools/second_planting_gate.py` (`check_crop`, the A43 de-mux + envelope invariant), `tools/
tree_calendar.py` (`derive_tree_calendar`, `tree_calendar_violations`), `tools/berries_woody_gate.py`
(`SUITABILITY_ENUM`-adjacent `BUSH_TYPE_ENUM`/`CANE_TYPE_ENUM`/`SHRUB_TYPE_ENUM`, the type-coverage
invariant), `tools/berry_woody_calendar.py` (`derive_berry_woody_calendar`,
`berry_woody_calendar_violations`), `tools/perennial_gate.py` (A3, `SUITABILITY_ENUM`,
`HEAT_BASIS_ENUM`, the no-fruit direction split, `gating_factors`, `min_variety_chill`),
`tools/region_cell_audit.py` (the `frost_model: "anchored"` branch Task 2 will register for
`mid_atlantic`). Every `calendar[]` array in this doc's worked examples (sections 2.4, 2.5, 3.3, 5.4)
was run through these exact functions in a scratch script during authoring (not eyeballed alone,
and no canonical bytes were read-write touched); each section's inline callout names which
function(s) certified it.
