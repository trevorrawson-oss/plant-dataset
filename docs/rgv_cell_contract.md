# RGV cell contract -- per-archetype `regions.rgv` template (v0)

**Status:** LOCKED for authoring (Task 1 of 7, RGV / subtropical South Texas region arc)
**Date:** 2026-07-13
**Origin:** `docs/superpowers/specs/2026-07-13-rgv-subtropical-tx-region-design.md` (read that first for
the product/scope rationale; this doc is its Section 4.3 "per-crop RGV cell" expanded into a
verbatim, copy-from template).
**Consumed by:** Tasks 4-7 (the annuals / citrus / chill-gated-tree / woody-herb+berry authoring
batches). Each of those tasks writes one `regions.rgv` object per crop; this doc is the shape they
write against. **Getting a key wrong here fails `whole_crop_gate` across dozens of crops at the
single atomic promote (Section 7 of the design spec), not one crop** -- treat every key below as
load-bearing.
**Method:** column GS-arc (`docs/gs_cross_crop_field_addition_v0.md`) -- a region is a column added
roster-wide; this is that column's field contract, "locked before any crop is touched."

---

## 0. How to read this doc

- Every JSON block below is **pretty-printed for readability**. The canonical
  `crops_data_final.json` is written compact (`separators=(",",":")`, `ensure_ascii=False`, no
  trailing newline) -- when a `regions.rgv` object is spliced into a real crop, it is compact, byte
  for byte, like every other region cell. Never hand-indent the real splice.
- The prose fields in the worked examples (`region_notes_*`, `suitability_note_*`,
  `chill_basis_*`) are **illustrative placeholders** that demonstrate shape and register, not
  authored, sourced content. Tasks 4-7 replace them with real TAMU-AgriLife-sourced (T1) prose.
  The placeholders still follow the house consumer-copy style so they double as a style example:
  no em dashes (commas/colons/semicolons/periods only), American English, temperatures as `°F`,
  "plant" lowercase outside sentence-start.
- Reference cells inspected to build this contract (exact key sets captured 2026-07-13 against the
  canonical at commit `a32e5ed`): `broccoli.regions.hawaii_tropical`, `broccoli.regions.se_gulf`,
  `apple.regions.low_desert_az`, `pear-european.regions.low_desert_az`,
  `grapefruit.regions.se_gulf`, `lemon.regions.se_gulf`, `orange-navel.regions.warm_arid`, and the
  builder/gate source of truth (`tools/build_region_shells.py`, `tools/perennial_gate.py`,
  `tools/whole_crop_gate.py`). See the Appendix for the exact captured key lists.

---

## 1. Invariants that apply to every `rgv` cell, all 3 archetypes

- `region_id`: `"rgv"`
- `region_label`: `"Rio Grande Valley: Subtropical South Texas"` (design spec §4.3; use this exact
  string, do not paraphrase -- `region_label` renders verbatim on the frontend)
- `zone_span`: `["9", "10"]` -- **LOCKED** for this arc (design spec §4.1). Every rgv cell's
  `resolved_by_zone` carries **exactly** the keys `"9"` and `"10"`, no more, no fewer. This is
  gate-enforced: A45 (`zone_span_gate`) fails any cell whose `resolved_by_zone` keys don't match
  `EXPECTED_SPANS["rgv"]` exactly.
- **Frost-free discipline, non-negotiable across all 3 archetypes:** `resolved_from` carries
  `last_frost: null` and `first_frost: null` (annual cells) or omits frost dates entirely / carries
  only a chill/heat datum (tree cells -- see Sections 3-4). The RGV never authors a frost date. If a
  cell asserts a non-null frost date, that is a defect, not a stylistic choice -- the whole reason
  RGV exists as its own region is that the `se_gulf` donor cell it replaces wrongly asserts Gulf
  frost dates (design spec §2).
- `resolution_method` is **free-text provenance, not a gate-enforced enum** (confirmed: 60+ distinct
  strings already live in the canonical, e.g. `month_resolved_frost_free`,
  `ctahr_table2_month_resolution_frost_free`, `frost_free_no_anchor`). Use
  `"month_resolved_frost_free"` (the Hawaii/FL-z11 convention) unless a more specific RGV-sourced
  label is warranted -- but whatever string is used, it must clearly read as frost-free resolution,
  and the `resolved_from` nulls (not the string) are what the gates actually check.
- `zone_span` has only two rows (`"9"`, `"10"`), so the usual 3-11-region `lifted_from_zone` pattern
  (identical values, one zone donor-cloned from the other) is legal here too: if TAMU's LRGV table
  does not differentiate z9 (inland fringe) from z10 (Valley core) for a given crop, author z10
  fully and set z9 = clone + `"lifted_from_zone": "10"` (or vice versa) rather than inventing an
  unsourced difference. Prefer authoring both distinctly where the source supports it (RGV's design
  intent is a real z9/z10 distinction, not a copy-paste).
- `sources` / `anchoring_urls`: every rule-layer entry (`plantings[]` sub-objects) and every
  zone-row carries its own `sources` (source-catalog ids) + `anchoring_urls` (id → `{url, verified}`)
  pair. T1-or-it-doesn't-ship holds; `tamu_agrilife` is already catalogued (design spec §6) -- Tasks
  4-7 confirm/add the exact TAMU publication id(s) per crop class, not a generic placeholder.
- Compact-JSON rule: never write the real splice with `indent=2`. This doc's blocks are pretty for
  the human reader only.

---

## 2. Archetype 1 -- frost-free ANNUAL cell

**Who gets this shape:** the 79 `frost_anchored` annuals, plus the non-tree perennials that carry a
real seasonal calendar (`perennial_woody_ornamental` -- rosemary/oregano/sage/thyme/lavender;
`berries_woody` -- blackberry/blueberry/raspberry/elderberry; `perennial_herbaceous` -- strawberry).
~89 crops total. This is the biggest batch (Tasks 4 and part of 7).

### 2.1 Cell-level keys

Identical to every other region's annual cell shape -- RGV adds no new top-level key here:

| Key | Shape | Note |
|---|---|---|
| `region_id` | string | `"rgv"` |
| `region_label` | string | `"Rio Grande Valley: Subtropical South Texas"` |
| `zone_span` | `["9","10"]` | locked |
| `sources` | `[id, ...]` | region-level source list |
| `plantings` | `[{...}, ...]` | the **rule layer** -- offsets, not absolute dates |
| `resolved_by_zone` | `{"9": {...}, "10": {...}}` | the **render layer** -- absolute dates + `calendar[]` |
| `region_notes_beginner` | string \| null | dual-register prose |
| `region_notes_seasoned` | string \| null | dual-register prose |

### 2.2 `plantings[]` entries -- anchor to `transplant_window` / `plant_out`, NOT frost

This is the one rule the frost-free convention changes: every `plantings[].plant_out` (and
`start_indoors`, when tray-started) entry's `"from"` field is **`"transplant_window"`** (direct
literal, offset `0`) or an offset off `plant_out`/`transplant_window` for `start_indoors` and
`harvest_start`/`harvest_end` -- **never** `"frost_free_spring"`, `"soil_workable"`,
`"heat_subsiding"`, `"fall_open"`, or any `*frost*` anchor name (those are the se_gulf/donor
vocabulary this arc retires for RGV). Each entry carries its own `sources` + `anchoring_urls` +
(seasoned register) `synthesis_note_seasoned`.

### 2.3 `resolved_by_zone["9"|"10"]` keys

| Key | Required? | Note |
|---|---|---|
| `plant_out` | required | absolute month/date-range string |
| `start_indoors` | conditional | present only if the crop is tray-started |
| `harvest`, `harvest_start`, `harvest_end` | required | |
| `first_plant_date`, `last_plant_date` | required | |
| `calendar` | required, 12 tokens | **DERIVED**, never hand-authored -- run `tools/annual_calendar.py` (or the crop's existing deriver invocation) after the window fields are set. Token enum: `plant, harvest, indoors, growing, heat_pause, cold_pause, season_over, wait` |
| `resolution_method` | required | see §1 |
| `resolved_from` | required | `{"last_frost": null, "first_frost": null}` -- hard invariant, see §1 |
| `second_planting` | conditional | only for a warm-season crop with a real spring+fall split around a heat_pause (§2.5 Variant B); shape = `{plant_out, start_indoors, harvest_start, harvest_end, sources, anchoring_urls}` -- all four window keys required if the object is present at all |
| `heat_pause` | conditional | only if a T1-backed summer heat pause is authored -- see the summer-gap rule, §2.5 |
| `season_over` (object) | conditional/RARE | not the `season_over` **calendar token** (common, §2.6) -- this is a structured object, shape `{"months":[...], "classification":..., "basis_seasoned":..., "sources":[...], "anchoring_urls":{...}}`, seen in the §2.4 worked example. Mirror the `heat_pause` discipline: author it only when a real T1 source states the *why* behind the summer planting gap. MOST cells omit it -- only 11 zone-rows in the whole canonical carry it (all on `broccoli`, across its `ca_desert`/`low_desert_az`/`fl_peninsula`/`hawaii_tropical` regions), so treat authoring it as the exception, not the default |
| `succession_continuous` / `succession_spring` / `succession_fall` | conditional | present only if the crop runs succession sowings (crop-dependent, not RGV-specific) |
| `successions_realized` | conditional | derived count; present only if the crop is in succession scope (`tools/derive_realized_successions.py`); absent entirely for an out-of-scope crop |
| `sources`, `anchoring_urls` | required | zone-row citation |
| `notes`, `zone_notes`, `planting_note` | required key, null-able value | present (possibly `null`) unless there is a real per-zone caveat to author |
| `lifted_from_zone` | conditional | only if this zone's row was donor-cloned from the other (§1) |

### 2.4 Full worked example -- cool-season, single-window (Hawaii-style)

This is the dominant new RGV pattern the design spec calls the "winter-garden inversion": a
cool-season crop (lettuce, spinach, brassica, root, cool herb) plants in the Oct-Mar window and the
brutal Valley summer is a planting gap. Modeled directly on `broccoli.regions.hawaii_tropical`
(illustrative placeholder crop `"leafy-example"`, values are NOT sourced):

```json
{
  "region_id": "rgv",
  "region_label": "Rio Grande Valley: Subtropical South Texas",
  "zone_span": ["9", "10"],
  "sources": ["tamu_agrilife"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "main",
      "track": "beginner",
      "start_indoors": [
        {
          "from": "transplant_window",
          "offset_days": -28,
          "window_days": 0,
          "synthesis_note_seasoned": "The Valley's winter vegetable window runs cool and frost-free; start transplants about 4 weeks before the October set-out (TAMU AgriLife LRGV planting guide).",
          "sources": ["tamu_agrilife"],
          "anchoring_urls": {
            "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
          },
          "uscrn_validation": null
        }
      ],
      "plant_out": [
        {
          "from": "transplant_window",
          "offset_days": 0,
          "window_days": 0,
          "synthesis_note_seasoned": "Set out in October as the summer heat breaks; the Valley rarely frosts, so this is a heat-driven start, not a frost-driven one (TAMU AgriLife LRGV planting guide).",
          "sources": ["tamu_agrilife"],
          "anchoring_urls": {
            "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_start": [
        {
          "from": "plant_out",
          "offset_days": 55,
          "window_days": 0,
          "synthesis_note_seasoned": "Matures in the mild Valley winter.",
          "sources": ["tamu_agrilife"],
          "anchoring_urls": {
            "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_end": [
        {
          "from": "plant_out",
          "offset_days": 150,
          "window_days": 0,
          "synthesis_note_seasoned": "End of the cool-season harvest before spring heat returns.",
          "sources": ["tamu_agrilife"],
          "anchoring_urls": {
            "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
          },
          "uscrn_validation": null
        }
      ],
      "anchoring_urls": {}
    }
  ],
  "resolved_by_zone": {
    "9": {
      "plant_out": "Oct 1 - Oct 22",
      "start_indoors": "Sep 3 - Sep 24",
      "harvest": "Nov 25 - Mar 1",
      "harvest_start": "Nov 25",
      "harvest_end": "Mar 1",
      "first_plant_date": "Oct 1",
      "last_plant_date": "Oct 22",
      "calendar": ["season_over", "season_over", "season_over", "season_over", "season_over", "season_over", "season_over", "season_over", "indoors", "plant", "harvest", "harvest"],
      "notes": null,
      "zone_notes": null,
      "planting_note": null,
      "sources": ["tamu_agrilife"],
      "anchoring_urls": {
        "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
      },
      "resolution_method": "month_resolved_frost_free",
      "resolved_from": {"last_frost": null, "first_frost": null},
      "season_over": {
        "months": [3, 4, 5, 6, 7, 8, 9],
        "classification": "heat_off_season",
        "basis_seasoned": "The Valley's long, humid summer is well outside this crop's heat tolerance, so the warm months are a planting gap, not a slow season (TAMU AgriLife).",
        "sources": ["tamu_agrilife"],
        "anchoring_urls": {
          "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
        }
      }
    },
    "10": {
      "plant_out": "Oct 1 - Oct 22",
      "start_indoors": "Sep 3 - Sep 24",
      "harvest": "Nov 25 - Mar 1",
      "harvest_start": "Nov 25",
      "harvest_end": "Mar 1",
      "first_plant_date": "Oct 1",
      "last_plant_date": "Oct 22",
      "calendar": ["season_over", "season_over", "season_over", "season_over", "season_over", "season_over", "season_over", "season_over", "indoors", "plant", "harvest", "harvest"],
      "notes": null,
      "zone_notes": null,
      "planting_note": null,
      "sources": ["tamu_agrilife"],
      "anchoring_urls": {
        "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
      },
      "resolution_method": "month_resolved_frost_free",
      "resolved_from": {"last_frost": null, "first_frost": null},
      "season_over": {
        "months": [3, 4, 5, 6, 7, 8, 9],
        "classification": "heat_off_season",
        "basis_seasoned": "The Valley's long, humid summer is well outside this crop's heat tolerance, so the warm months are a planting gap, not a slow season (TAMU AgriLife).",
        "sources": ["tamu_agrilife"],
        "anchoring_urls": {
          "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
        }
      },
      "lifted_from_zone": "9"
    }
  },
  "region_notes_beginner": "In the Rio Grande Valley, grow this crop in the cool season, not summer. Plant transplants in October and harvest from late November into early spring; it rarely if ever frosts here, so the challenge is heat, not cold. Skip planting from spring through summer: the Valley heat keeps this crop from growing well.",
  "region_notes_seasoned": "In the RGV this is a true winter crop, not a warm-season one. Transplants go out in October as the summer heat breaks, and harvest runs from late November into early spring while temperatures stay mild. Frost is essentially absent here, so timing is heat-driven rather than cold-driven: plant late enough to dodge lingering heat but early enough to finish before spring warmth returns. The long, humid Valley summer is a genuine planting gap for this crop, not a slow season."
}
```

### 2.5 Variant B -- warm-season, spring + fall split around a `heat_pause` (se_gulf-style)

Warm-season crops (tomato, pepper, bean, squash, melon, warm herb) run the design spec's other
pattern: a long spring-to-fall season split by a mid-summer pause, modeled on
`broccoli.regions.se_gulf`'s two-succession + `heat_pause` shape -- but **frost-free**: `plant_out`
still anchors to `transplant_window`, never `frost_free_spring`/`heat_subsiding`. The delta from
§2.4 is entirely inside `resolved_by_zone[z]`:

```json
{
  "plant_out": "Feb 1 - Mar 1",
  "harvest": "Apr 15 - Jun 15",
  "second_planting": {
    "start_indoors": "Jul 21 - Aug 11",
    "plant_out": "Aug 15 - Sep 15",
    "harvest_start": "Oct 20",
    "harvest_end": "Dec 1",
    "sources": ["tamu_agrilife"],
    "anchoring_urls": {
      "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
    }
  },
  "succession_spring": "Feb 1, Feb 22, Mar 15",
  "succession_fall": "Aug 15, Sep 5, Sep 26",
  "heat_pause": {
    "months": [6, 7, 8],
    "classification": "heat_stop_setting",
    "basis_seasoned": "Valley summer heat above the crop's fruit-set threshold stops production, so no crop is grown between the spring and fall windows (TAMU AgriLife).",
    "sources": ["tamu_agrilife"],
    "anchoring_urls": {
      "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
    }
  },
  "resolution_method": "month_resolved_frost_free",
  "resolved_from": {"last_frost": null, "first_frost": null}
}
```

`second_planting` requires all four of `plant_out`/`start_indoors`/`harvest_start`/`harvest_end`
present if the key is present at all (`whole_crop_gate`'s `SECOND_PLANTING_KEYS` check). `plantings[]`
carries a matching second `succession_id` entry with `track: "second_planting"` **always** --
`"fall"` is the entry's `label`, not its `track` (confirmed against
`broccoli.regions.se_gulf.plantings[1]`, which carries `label: "fall"`, `track: "second_planting"`),
same `transplant_window`-anchored shape as §2.2 -- see that cell for the exact rule-layer pattern to
mirror (frost anchors swapped for transplant-window anchors).

### 2.6 The summer-gap rule (binding on every annual cell, both variants)

**Default to `season_over`** for a cool-crop's summer gap (§2.4) or an out-of-window month
generally. Author a `heat_pause` object **only when a T1-backed heat pause is being asserted**
(a real warm-season mid-summer stop, §2.5) -- never invent a `heat_pause` to "fill in" a gap that
is actually just season-over. This is the heat_pause-at-variety-pass discipline already governing
the rest of the roster (see the `d8-heat-pause-variety-pass-commitment` memory): a `heat_pause`
carries `months` + `classification` + `basis_seasoned` + `sources`, i.e. it is a sourced claim, not
a placeholder. If TAMU doesn't specify a heat-stop for a crop, that crop's off-window months render
`season_over`, full stop.

### 2.7 Gates that bind this shape

A2 (region-fill completeness), A5/A5b/A5c (annual calendar coherence + indoors-run backing -- the
`calendar[]` must be the deriver's output, not hand-typed), A8 (successions_realized, if in scope),
A31/A32 (region-roster + calendar-presence floor), A45 (zone_span exact-match). None of these are
new gates for RGV -- they already run roster-wide; RGV cells must simply satisfy them like every
other region's.

---

## 3. Archetype 2 -- tree-fruiting cell

**Who gets this shape:** the 5 citrus (`perennial_evergreen`: grapefruit, lemon, lime,
mandarin-clementine, orange-navel -- RGV's signature crop, full flagship calendars per design spec
§3) and the low-chill subset of the 14 chill-gated trees that DO fruit in near-zero-chill RGV
(`perennial_chill_gated`: fig, mulberry, persimmon, pomegranate -- the fruit-vs-no-fruit call is
itself a sourced TAMU decision per crop, design spec §11).

**Important: this archetype has two sub-shapes, keyed off the crop's existing `calendar_basis` /
`gating_factors` -- RGV does not change either.** Get the wrong sub-shape and A3 (`perennial_gate.py`)
fails immediately.

### 3.1 Sub-shape by `calendar_basis` / `gating_factors`

| | `perennial_chill_gated` (fig, mulberry, persimmon, pomegranate) | `perennial_evergreen` (all 5 citrus) |
|---|---|---|
| Region-level climate keys | `chill_basis_seasoned`, `chill_basis_beginner` | `min_winter_temp_f` (`[lo,hi]`), `cold_basis_seasoned`, `cold_basis_beginner`; **+ if `"heat_accumulation" in gating_factors"`** (grapefruit, mandarin-clementine, orange-navel -- NOT lemon/lime): `heat_summer_basis`, `heat_basis_seasoned`, `heat_basis_beginner` |
| Cell-level climate keys | none (chill-delivered lives ONLY in the shared top-level `region_chill_delivered.rgv` table, not per-cell -- A18) | `min_winter_temp_f` (`[lo,hi]`); **+ if heat-gated:** `heat_summer_basis` |
| `resolved_from` | `{"last_frost": null, "first_frost": null}` (chill band is not per-cell; RGV is frost-free so no frost dates either way) | for RGV specifically: no frost dates (frost-free); may be `{}` or omit -- evergreen cells don't carry a chill datum at all, cold is the only per-cell climate axis and RGV has essentially none of it |
| Shared cell keys | `suitability`, `suitability_note_seasoned`, `suitability_note_beginner`, `plant_out`, `bloom`, `harvest_start`, `harvest_end`, `harvest`, `calendar`, `frost_risk_note_seasoned`, `resolution_method`, `sources`, `anchoring_urls` | same |
| `plantings[]` | exactly ONE entry, `track: "perennial"`, keys `plant_out`/`bloom`/`harvest_start`/`harvest_end`/`anchoring_urls`/`sources` -- no `start_indoors`, no `direct_sow`, no succession/second_planting | same |
| `suitability` value (fruiting archetype) | `"fruits_reliably"` or `"marginal"` (never `survives_no_fruit`/`unsuitable` -- that's Archetype 3) | same |
| `calendar[]` vocabulary | `prune, bloom, growing, harvest, care, dormant` (deciduous -- RGV winters are so mild that `dormant`/`prune` windows will be short; author from the source, don't force a temperate-length dormancy) | `bloom, growing, harvest, care` (no true dormancy for evergreen citrus; `dormant` should not appear) |

Region-level `plantings_provenance` (present, nullable) applies to both.

### 3.2 Full worked example -- `perennial_chill_gated` fruiting (fig/mulberry/persimmon/pomegranate pattern)

Modeled on `apple.regions.low_desert_az` (a `fruits_reliably`/`marginal` chill-gated tree cell),
substituting RGV's near-zero chill band. Illustrative placeholder crop, values NOT sourced:

```json
{
  "region_id": "rgv",
  "region_label": "Rio Grande Valley: Subtropical South Texas",
  "zone_span": ["9", "10"],
  "sources": ["tamu_agrilife"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "establishment",
      "track": "perennial",
      "plant_out": [
        {
          "label": "bare_root_or_container",
          "from": "last_frost",
          "offset_days": -21,
          "window_days": 45,
          "sources": ["tamu_agrilife"],
          "anchoring_urls": {
            "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
          }
        }
      ],
      "bloom": [
        {
          "label": "primary",
          "from": "last_frost",
          "offset_days": 21,
          "window_days": 21,
          "sources": ["tamu_agrilife"],
          "anchoring_urls": {
            "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
          }
        }
      ],
      "harvest_start": [
        {"label": "primary", "from": "bloom_start", "offset_days": 90, "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "harvest_end": [
        {"label": "primary", "from": "bloom_start", "offset_days": 140, "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "anchoring_urls": {
        "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
      },
      "sources": ["tamu_agrilife"]
    }
  ],
  "resolved_by_zone": {
    "9": {
      "plant_out": "Dec - Jan (dormant, bare-root or container)",
      "resolution_method": "perennial_precompute",
      "suitability": "fruits_reliably",
      "suitability_note_seasoned": "Valley winters deliver enough chill for low-chill cultivars, per Texas A&M AgriLife Extension. Heat and humidity, not cold, are the season's real hazards.",
      "suitability_note_beginner": "Low-chill varieties fruit well in the Rio Grande Valley. Choose a variety bred for low winter chill.",
      "bloom": "Feb 10 - Mar 3",
      "harvest_start": "May 10",
      "harvest_end": "Jun 30",
      "harvest": "May - Jun",
      "calendar": ["prune", "bloom", "growing", "growing", "harvest", "harvest", "care", "care", "care", "care", "dormant", "dormant"],
      "frost_risk_note_seasoned": "Frost is not a practical concern in the Valley; heat and humidity management matter more than cold protection.",
      "resolved_from": {"last_frost": null, "first_frost": null},
      "sources": ["tamu_agrilife"],
      "anchoring_urls": {
        "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
      }
    },
    "10": {
      "plant_out": "Dec - Jan (dormant, bare-root or container)",
      "resolution_method": "perennial_precompute",
      "suitability": "fruits_reliably",
      "suitability_note_seasoned": "Valley winters deliver enough chill for low-chill cultivars, per Texas A&M AgriLife Extension. Heat and humidity, not cold, are the season's real hazards.",
      "suitability_note_beginner": "Low-chill varieties fruit well in the Rio Grande Valley. Choose a variety bred for low winter chill.",
      "bloom": "Feb 10 - Mar 3",
      "harvest_start": "May 10",
      "harvest_end": "Jun 30",
      "harvest": "May - Jun",
      "calendar": ["prune", "bloom", "growing", "growing", "harvest", "harvest", "care", "care", "care", "care", "dormant", "dormant"],
      "frost_risk_note_seasoned": "Frost is not a practical concern in the Valley; heat and humidity management matter more than cold protection.",
      "resolved_from": {"last_frost": null, "first_frost": null},
      "sources": ["tamu_agrilife"],
      "anchoring_urls": {
        "tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}
      },
      "lifted_from_zone": "9"
    }
  },
  "region_notes_beginner": "This fruits well in the Rio Grande Valley if you choose a low-chill variety. Winters are mild enough for chill needs and summers are long and hot, so plant a variety bred for warm climates.",
  "region_notes_seasoned": "The Valley's near-zero-chill winters meet the requirement of low-chill cultivars, and the long hot growing season carries fruit through to a reliable harvest. Choose varieties bred for low winter chill and warm, humid summers; heat and humidity management, not cold protection, are the season's real work.",
  "chill_basis_seasoned": "Rio Grande Valley winters bank roughly 0 to 300 chill hours (order-of-magnitude, TAMU AgriLife), meeting the requirement of low-chill cultivars bred for this range.",
  "chill_basis_beginner": "Valley winters give a small amount of winter cold, enough for varieties bred to need very little.",
  "plantings_provenance": null
}
```

### 3.3 Full worked example -- `perennial_evergreen` citrus, heat-gated (grapefruit / mandarin-clementine / orange-navel pattern)

RGV is frost-free and heat-abundant -- its citrus cells should trend toward `"fruits_reliably"` with
`heat_summer_basis: "high"` (the design spec calls RGV citrus the flagship: "the authoritative
answer for RGV's signature crop", §5). Modeled on `grapefruit.regions.se_gulf` (`fruits_reliably`
zones) with `orange-navel.regions.warm_arid`'s `heat_summer_basis`/`heat_basis_*` fields folded in.
Illustrative placeholder crop, values NOT sourced:

```json
{
  "region_id": "rgv",
  "region_label": "Rio Grande Valley: Subtropical South Texas",
  "zone_span": ["9", "10"],
  "sources": ["tamu_agrilife"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "establishment",
      "track": "perennial",
      "plant_out": [
        {"label": "container_or_balled_spring", "from": "last_frost", "offset_days": 0, "window_days": 45,
         "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "bloom": [
        {"label": "primary", "from": "last_frost", "offset_days": 0, "window_days": 45,
         "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "harvest_start": [
        {"label": "primary", "from": "bloom_start", "offset_days": 240, "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "harvest_end": [
        {"label": "primary", "from": "bloom_start", "offset_days": 360, "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}},
      "sources": ["tamu_agrilife"]
    }
  ],
  "resolved_by_zone": {
    "9": {
      "plant_out": "Most of the year (container or balled; spring ideal)",
      "resolution_method": "perennial_evergreen_precompute",
      "suitability": "fruits_reliably",
      "suitability_note_seasoned": "The Valley is essentially frost-free, and its long hot summers bank ample heat to sweeten fruit over a long hang, per Texas A&M AgriLife Extension citrus guidance. This is the Valley's premier tree fruit.",
      "suitability_note_beginner": "This citrus does very well in the Rio Grande Valley: winters are mild and summers are long and hot, exactly what it needs.",
      "min_winter_temp_f": [32, 40],
      "heat_summer_basis": "high",
      "bloom": "Feb - Mar",
      "harvest_start": "Nov",
      "harvest_end": "Apr",
      "harvest": "Nov - Apr (holds and sweetens on the tree)",
      "calendar": ["harvest", "harvest", "bloom", "bloom", "growing", "growing", "growing", "growing", "growing", "growing", "harvest", "harvest"],
      "frost_risk_note_seasoned": "Frost is essentially absent in the Valley; an occasional hard freeze is the only cold risk, and it is rare.",
      "resolved_from": {"last_frost": null, "first_frost": null},
      "sources": ["tamu_agrilife"],
      "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}
    },
    "10": {
      "plant_out": "Most of the year (container or balled; spring ideal)",
      "resolution_method": "perennial_evergreen_precompute",
      "suitability": "fruits_reliably",
      "suitability_note_seasoned": "The Valley is essentially frost-free, and its long hot summers bank ample heat to sweeten fruit over a long hang, per Texas A&M AgriLife Extension citrus guidance. This is the Valley's premier tree fruit.",
      "suitability_note_beginner": "This citrus does very well in the Rio Grande Valley: winters are mild and summers are long and hot, exactly what it needs.",
      "min_winter_temp_f": [34, 42],
      "heat_summer_basis": "high",
      "bloom": "Feb - Mar",
      "harvest_start": "Nov",
      "harvest_end": "Apr",
      "harvest": "Nov - Apr (holds and sweetens on the tree)",
      "calendar": ["harvest", "harvest", "bloom", "bloom", "growing", "growing", "growing", "growing", "growing", "growing", "harvest", "harvest"],
      "frost_risk_note_seasoned": "Frost is essentially absent at the Valley core; a hard freeze is rare and brief when it occurs.",
      "resolved_from": {"last_frost": null, "first_frost": null},
      "sources": ["tamu_agrilife"],
      "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}
    }
  },
  "region_notes_beginner": "This citrus is a signature Rio Grande Valley crop. Winters are mild, almost frost-free, and summers are long and hot, ideal conditions for sweet, reliable fruit from November into spring.",
  "region_notes_seasoned": "The Rio Grande Valley is this citrus's most authoritative U.S. home outside peninsular Florida: essentially frost-free winters and long, intensely hot summers combine to bank ample heat for full sugar development over a long hang, from November into spring. Cold protection is rarely if ever needed here.",
  "min_winter_temp_f": [32, 42],
  "cold_basis_seasoned": "Valley winters rarely reach freezing and a hard freeze is a rare, short-lived event, well above this crop's damage thresholds in nearly all years, per Texas A&M AgriLife Extension.",
  "cold_basis_beginner": "Winters here are mild and almost never freeze long enough to hurt the tree or fruit.",
  "heat_summer_basis": "high",
  "heat_basis_seasoned": "Long, intensely hot Valley summers bank abundant heat, more than enough to sweeten fruit fully; heat is never the limiting factor here. Humidity favors cosmetic rind issues, a cosmetic concern rather than a yield one.",
  "heat_basis_beginner": "Summers here are long and very hot, plenty for sweet, well-ripened fruit.",
  "plantings_provenance": null
}
```

### 3.4 Delta -- evergreen, NOT heat-gated (lemon / lime pattern)

Lemon and lime carry `gating_factors: ["cold_hardiness"]` only (no `"heat_accumulation"`) -- per
`tools/build_region_shells.py`'s `heat_gated` branch, **omit** `heat_summer_basis` /
`heat_basis_seasoned` / `heat_basis_beginner` entirely (region- and cell-level) for these two crops.
Do not add heat fields "for consistency" -- `perennial_gate.py`'s A3 check flags a heat-gated
inference from stray `heat_summer_basis` cells against a crop whose `gating_factors` doesn't carry
the token, and the inverse (heat fields present on a non-heat-gated crop) is simply unnecessary
per-crop-constant field bloat inconsistent with every other region's lemon/lime cells. Everything
else in §3.3 applies unchanged (`min_winter_temp_f`, `cold_basis_*`, `suitability`, calendar
vocabulary).

### 3.5 Gates that bind this shape

A3 (`perennial_gate.py` -- suitability enum membership, single perennial establishment entry,
`fruits_reliably`/`marginal` must carry a non-empty calendar, the heat-gated floor when
`heat_accumulation` is in `gating_factors`), A4 (tree-calendar coherence -- `calendar[]` must be
*derivable* from `bloom`+`harvest` dates, not hand-typed independently), A31 (region-roster floor).
A32 does **not** apply to trees (`coverage_floor_gate.CALENDAR_PRESENCE_BASES` = `frost_anchored`,
`perennial_herbaceous`, `berries_woody`, `perennial_woody_ornamental` -- Archetype 1's scope, §2 --
not the tree archetypes; trees are exempt and governed by A3 instead).

---

## 4. Archetype 3 -- tree, NO-FRUIT cell

**Who gets this shape:** the high-chill subset of the 14 chill-gated trees, in near-zero-chill RGV:
apple, apricot, cherry-sour, cherry-sweet, nectarine, peach, pear-asian, pear-european, plum,
pawpaw (design spec §5, "Chill-gated fruit"). All `calendar_basis: "perennial_chill_gated"`. This is
the lightest-weight archetype (A32-exempt, only A3 governs) but still requires a correctly-shaped,
honest verdict cell -- not an empty stub.

### 4.1 The A3 no-fruit DIRECTION SPLIT -- the load-bearing rule

`tools/perennial_gate.py` enforces this exactly (read the violations, they are the spec):

- `suitability: "unsuitable"` → `calendar` **MUST be empty** (`[]`). Always.
- `suitability: "survives_no_fruit"` → the gate reads the shared top-level
  `region_chill_delivered.rgv[z]` band (added in a different task -- see §5) and the crop's lowest
  recommended-variety `chill_hours_required` (`min_variety_chill`, default 400 if the crop has none
  stated):
  - if the delivered chill **meets** the variety floor (`chill_lo >= floor`) → the cell **MUST**
    carry a real calendar (an empty one would under-report -- the tree can bloom some years).
  - if the delivered chill is **below** the floor (`chill_lo < floor`, RGV's near-zero-chill
    reality for every crop in this list) → the cell **MUST have an empty calendar** (a calendar
    would over-promise fruit that will not set).
- `fruits_reliably` / `marginal` → must carry a calendar (that's Archetype 2, not this one).
- A **null** `suitability` on a **filled** cell (one that already carries a calendar) is itself a
  violation -- a filled cell must declare its verdict.

Given RGV's order-of-magnitude `[0, 300]` chill band (design spec §4.5) against these ten crops'
several-hundred-to-thousand-hour chill requirements, expect **`survives_no_fruit` with an empty
calendar** to be the modal verdict -- the crop can physically live in the Valley (heat and humidity
permitting) but will not reliably set fruit. Reserve `"unsuitable"` for a crop that additionally
cannot even survive RGV's climate (extreme heat intolerance, e.g. a crop needing real winter
dormancy just to avoid decline, not only to fruit) -- check the per-crop TAMU guidance rather than
defaulting everything to `unsuitable`.

Two authored variants both appear in the existing canonical and either is acceptable depending on
how much the source publication commits to:

- **Thin/null variant** (`peach.regions.fl_peninsula`'s pattern): `plant_out`, `bloom`,
  `harvest_start`, `harvest_end`, `harvest` all `null`; `resolved_from` carries only the chill
  datum (or is empty for RGV, since RGV's chill lives in the shared table, not per-cell); the
  suitability note explains the chill gap and closes with a redirect ("choose a low-chill
  alternative instead").
- **Thicker variant** (`pear-european.regions.low_desert_az`'s pattern): `bloom`, `harvest_start`,
  `harvest_end`, `harvest` are still authored/computed (the tree may still leaf out and bloom on
  schedule even though it won't set fruit) while `calendar` stays `[]`.

Either is gate-clean as long as `calendar` is empty and the suitability note is honest about *why*
(chill gap, explicitly, not just "not recommended").

### 4.2 Full worked example (thicker variant, modeled on `pear-european.regions.low_desert_az`)

Illustrative placeholder crop, values NOT sourced:

```json
{
  "region_id": "rgv",
  "region_label": "Rio Grande Valley: Subtropical South Texas",
  "zone_span": ["9", "10"],
  "sources": ["tamu_agrilife"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "establishment",
      "track": "perennial",
      "plant_out": [
        {"label": "bare_root_dormant", "from": "last_frost", "offset_days": -35, "window_days": 35,
         "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "bloom": [
        {"label": "primary", "from": "last_frost", "offset_days": -3, "window_days": 21,
         "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "harvest_start": [
        {"label": "primary", "from": "bloom_start", "offset_days": 110, "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "harvest_end": [
        {"label": "primary", "from": "bloom_start", "offset_days": 140, "sources": ["tamu_agrilife"],
         "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}}
      ],
      "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}},
      "sources": ["tamu_agrilife"]
    }
  ],
  "plantings_provenance": null,
  "resolved_by_zone": {
    "9": {
      "plant_out": "Dec - Jan (dormant, bare-root)",
      "resolution_method": "perennial_precompute",
      "suitability": "survives_no_fruit",
      "suitability_note_seasoned": "The Rio Grande Valley banks only about 0 to 300 chill hours, far below even the lowest-chill cultivars of this crop, and extreme summer heat adds further stress. Trees may survive but will not reliably set fruit; choose a citrus or other low-chill crop for this climate instead.",
      "suitability_note_beginner": "This crop rarely fruits in the Rio Grande Valley: winters are too mild for the cold it needs and summers are too hot. Grow a citrus or another low-chill fruit here instead.",
      "bloom": "Jan 25 - Feb 15",
      "harvest_start": "May 15",
      "harvest_end": "Jun 15",
      "harvest": "May - Jun",
      "calendar": [],
      "frost_risk_note_seasoned": "Frost is not the limiting factor here; insufficient winter chill is the binding constraint on fruiting.",
      "resolved_from": {"last_frost": null, "first_frost": null},
      "sources": ["tamu_agrilife"],
      "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}
    },
    "10": {
      "plant_out": "Dec - Jan (dormant, bare-root)",
      "resolution_method": "perennial_precompute",
      "suitability": "survives_no_fruit",
      "suitability_note_seasoned": "The Rio Grande Valley banks only about 0 to 300 chill hours, far below even the lowest-chill cultivars of this crop, and extreme summer heat adds further stress. Trees may survive but will not reliably set fruit; choose a citrus or other low-chill crop for this climate instead.",
      "suitability_note_beginner": "This crop rarely fruits in the Rio Grande Valley: winters are too mild for the cold it needs and summers are too hot. Grow a citrus or another low-chill fruit here instead.",
      "bloom": "Jan 20 - Feb 10",
      "harvest_start": "May 10",
      "harvest_end": "Jun 10",
      "harvest": "May - Jun",
      "calendar": [],
      "frost_risk_note_seasoned": "Frost is not the limiting factor here; insufficient winter chill is the binding constraint on fruiting.",
      "resolved_from": {"last_frost": null, "first_frost": null},
      "sources": ["tamu_agrilife"],
      "anchoring_urls": {"tamu_agrilife": {"url": "https://agrilifeextension.tamu.edu", "verified": "2026-07-13"}}
    }
  },
  "region_notes_beginner": "This crop is a poor choice for the Rio Grande Valley. Winters are too mild to give it the cold it needs and summers are too hot, so trees rarely fruit here.",
  "region_notes_seasoned": "This crop does not fruit dependably in the Rio Grande Valley: winter chill (roughly 0 to 300 hours) falls far below its requirement even in the lowest-chill cultivars, and extreme summer heat compounds the problem. Trees may survive but rarely crop; the Valley is far better suited to citrus or other low-chill fruit."
}
```

Note this archetype's cell has **no `chill_basis_*` region-level pair** in the worked example above,
unlike Archetype 2's chill-gated fruiting cell (§3.2), which does carry `chill_basis_*`. Both are
legal on a `perennial_chill_gated` crop (the key is `setdefault`-scaffolded null-able at shell
stage regardless of eventual suitability); author it wherever there's a real chill claim to make.
Since `region_chill_delivered.rgv` is a shared, crop-invariant table, the same near-zero band
applies to every crop in this archetype, so a `chill_basis_*` pair authored once and reused
verbatim across the ten no-fruit crops is legitimate and expected.

### 4.3 Gates that bind this shape

A3 (the direction split above -- this is the entire gate for this archetype), A31 (region-roster
floor -- a no-fruit crop still needs the `rgv` cell present, just with an empty calendar; A31 does
not require a non-empty calendar, only A32 does and A32 skips trees). If `region_chill_delivered.rgv`
is not yet populated when a `survives_no_fruit` cell is authored, A3 fails with "no delivered band";
confirm that top-level table lands (a different task, §5) before or atomically with these cells,
per the design spec's ordering-pincer discipline (§7).

---

## 5. Cross-archetype pre-flight checklist (Tasks 4-7, before handoff)

- [ ] `region_id` = `"rgv"`, `region_label` = `"Rio Grande Valley: Subtropical South Texas"` verbatim
- [ ] `zone_span` = `["9","10"]`; `resolved_by_zone` keys are exactly `{"9","10"}`
- [ ] No `resolved_from.last_frost` / `.first_frost` is non-null anywhere in this crop's rgv cell
- [ ] No `plant_out`/`start_indoors` rule entry anchors to `frost_free_spring`, `soil_workable`,
      `heat_subsiding`, `fall_open`, or any other frost-relative anchor (annual archetype)
- [ ] `calendar[]` was DERIVED (`tools/annual_calendar.py` for annuals) or is coherent with
      `bloom`+`harvest` (tree archetypes) -- never hand-typed independently of the dates
- [ ] Summer/off-season gap defaults `season_over`; `heat_pause` present only where T1-backed
- [ ] Tree archetype: `plantings[]` has exactly one entry, `track: "perennial"`, no
      `start_indoors`/`direct_sow`/succession/second_planting
- [ ] Fruiting tree: `suitability` ∈ `{"fruits_reliably","marginal"}`, non-empty `calendar`
- [ ] No-fruit tree: `suitability` ∈ `{"survives_no_fruit","unsuitable"}`; `unsuitable` → empty
      calendar always; `survives_no_fruit` → empty calendar (RGV's chill-limited case, the
      expected default) unless the delivered/floor math says otherwise
- [ ] Heat-gated evergreen (grapefruit, mandarin-clementine, orange-navel only) carries
      `heat_summer_basis` + `heat_basis_*`; lemon/lime do NOT
- [ ] Every rule entry and zone-row carries real `sources` + `anchoring_urls` (T1, e.g.
      `tamu_agrilife` or a newly-catalogued TAMU publication id -- never left as this doc's
      placeholder text)
- [ ] No em dashes in any `*_note_*`/`region_notes_*` prose; American English; `°F`; "plant"
      lowercase outside sentence-start
- [ ] Splice is compact JSON (no `indent=2`, no trailing newline) when it lands in the canonical

---

## 6. Out of scope (owned by a different task/session)

This doc is the **per-crop cell** contract only. It does NOT cover:

- `zone_span_gate.EXPECTED_SPANS["rgv"]` (the top-level span registration that makes A45 accept
  `rgv` cells at all -- design spec §4.4, §7's "ordering pincer")
- `region_chill_delivered.rgv` + `region_chill_delivered_provenance` (the shared chill-band table
  Archetype 3's direction split reads -- design spec §4.5)
- `region_source_map` (build-time authoring infrastructure, not a runtime-read field)
- The atomic-promote assembly mechanics (design spec §7) and the state-trio / footprint audit
  (design spec §12)
- Any plant-app ZIP3-fencing or plant-astro consumption (design spec §9 -- explicitly a different
  session's work)

See the design spec for all of the above.

---

## Appendix -- reference-cell key sets captured 2026-07-13 (canonical `a32e5ed`)

```
broccoli.regions.hawaii_tropical
  cell keys: region_id, region_label, zone_span, sources, plantings, resolved_by_zone,
             region_notes_beginner, region_notes_seasoned
  zone-row keys: plant_out, start_indoors, harvest, harvest_start, harvest_end,
             first_plant_date, last_plant_date, calendar, notes, zone_notes, planting_note,
             sources, anchoring_urls, resolution_method, succession_continuous,
             resolved_from, season_over, successions_realized, lifted_from_zone (z10 only)

broccoli.regions.se_gulf
  zone-row keys: (as above, minus succession_continuous/season_over) plus second_planting,
             succession_spring, succession_fall, heat_pause

apple.regions.low_desert_az
  cell keys: + chill_basis_seasoned, chill_basis_beginner, plantings_provenance
  zone-row keys: plant_out, resolution_method, suitability, suitability_note_seasoned,
             suitability_note_beginner, bloom, harvest_start, harvest_end, harvest,
             calendar, frost_risk_note_seasoned, resolved_from, sources, anchoring_urls,
             lifted_from_zone (z10 only)

pear-european.regions.low_desert_az  (survives_no_fruit reference, same zone_span as rgv)
  same zone-row key set as apple; calendar: [] on both zones

grapefruit.regions.se_gulf / orange-navel.regions.warm_arid  (heat-gated evergreen reference)
  region + cell keys add: min_winter_temp_f, cold_basis_seasoned, cold_basis_beginner,
             heat_summer_basis, heat_basis_seasoned, heat_basis_beginner

lemon.regions.se_gulf  (non-heat-gated evergreen reference)
  same as above MINUS heat_summer_basis / heat_basis_seasoned / heat_basis_beginner
```

Gate logic cross-referenced: `tools/whole_crop_gate.py` (A2, A5/A5b/A5c, A8, A31/A32, A45),
`tools/perennial_gate.py` (A3, `SUITABILITY_ENUM`, the no-fruit direction split,
`min_variety_chill`), `tools/build_region_shells.py` (`_build_tree_cell`/`_build_tree_region` -- the
authoritative per-archetype shell shape this contract mirrors).
