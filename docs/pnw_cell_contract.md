# PNW cell contract -- per-archetype `regions.pnw` template (v0)

**Status:** LOCKED for authoring (Task 1 of 12, maritime Pacific Northwest region arc, roadmap item 4)
**Date:** 2026-07-14
**Origin:** `docs/superpowers/specs/2026-07-14-maritime-pnw-region-design.md` (read that first for the
product/scope rationale; this doc expands its section 4.3 "per-crop PNW cell" into a verbatim,
copy-from template) + `docs/kickoffs/27-maritime-pnw-region.md`.
**Precedent:** `docs/rgv_cell_contract.md` (the RGV region's sibling doc, shipped 2026-07-13). This
doc mirrors its structure and method deliberately -- **but flips the frost model everywhere.** RGV is
frost-FREE (`month_resolved_frost_free`, null `resolved_from`, no `cold_pause`, transplant-window
anchors). PNW is frost-ANCHORED, the ordinary shape every other pre-existing region already uses
(`ca_north_coast`, `northern_tier`, etc.): `frost_anchored_resolved`, real `resolved_from` frost
dates, `cold_pause` winters, `last_frost`/`first_frost`-anchored `plantings[]`. Read RGV's doc for the
overall METHOD (column GS-arc, per-archetype key tables, worked-example convention); read THIS doc
for PNW's actual field values -- do not copy RGV's frost-free conventions into a `pnw` cell.
**Consumed by:** Tasks 4-7 (annuals / trees / citrus / other perennials authoring batches). Each of
those tasks writes one `regions.pnw` object per crop; this doc is the shape they write against.
**Getting a key wrong here fails `whole_crop_gate` across dozens of crops at the single atomic
promote, not one crop** -- treat every key below as load-bearing.
**Method:** column GS-arc (`docs/gs_cross_crop_field_addition_v0.md`) -- a region is a column added
roster-wide (Option A, full 108-crop roster, Trevor-approved 2026-07-14); this is that column's
field contract, locked before any crop is touched.

---

## 0. How to read this doc

- Every JSON block below is **pretty-printed for readability**. The canonical `crops_data_final.json`
  is written compact (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline) -- when a
  `regions.pnw` object is spliced into a real crop, it is compact, byte for byte, like every other
  region cell. Never hand-indent the real splice.
- The prose fields in the worked examples (`region_notes_*`, `suitability_note_*`, `chill_basis_*`,
  `cold_basis_*`) are **illustrative placeholders** demonstrating shape and register, not authored,
  sourced content. Tasks 4-7 replace them with real WSU/OSU-sourced (T1) prose. The placeholders still
  follow house consumer-copy style so they double as a style example: no em dashes (commas, colons,
  semicolons, periods only), American English, temperatures as `°F`, "plant" lowercase outside
  sentence-start.
- **The absolute dates in every worked example below (frost dates, plant/bloom/harvest windows, chill
  bands, `min_winter_temp_f`) are clearly-plausible maritime placeholders, NOT sourced.** Real
  Puget-Sound/Willamette-Valley last-frost dates run roughly mid-April (z8, colder inland/higher
  pockets) to earlier/milder (z9, coastal and protected lowlands); first frost runs roughly early
  November (z8) to mid-to-late November (z9 milder). This doc uses **z8: last frost Apr 15, first
  frost Nov 1** and **z9: last frost Apr 1, first frost Nov 15** throughout, for internal consistency
  across every worked example. Task 3 (WSU/OSU/NWS T1 sourcing pass) replaces these with real
  station-sourced windows per crop and per zone; do not treat the numbers here as authoritative,
  only as an internally-consistent shape to author against.
- **Every `calendar[]` array below was verified against the actual live derivation/gate code in this
  repo** (`tools/tree_calendar.py` for the tree archetypes, hand-checked against
  `tools/annual_calendar.py`'s placement/coherence/backing gates for the annual archetype -- see the
  callout in §2.4). This is stronger than "plausible": these specific arrays are known to satisfy the
  gates that will actually run against Task 4-7's real cells. The absolute dates feeding them are
  still placeholders (see above); only the token-shape/coherence is load-bearing here.
- Reference cells inspected to build this contract (exact key sets + resolution methods captured
  2026-07-14 against canonical `d0832254`): `broccoli.regions.ca_north_coast`,
  `broccoli.regions.northern_tier`, `apple.regions.northern_tier`, `orange-navel.regions.ca_north_coast`,
  `orange-navel.regions.northern_tier`, plus the gate/deriver source of truth
  (`tools/annual_calendar.py`, `tools/tree_calendar.py`, `tools/perennial_gate.py`,
  `tools/whole_crop_gate.py`). See the Appendix for the exact captured key lists.

---

## 1. Invariants that apply to every `pnw` cell, all 4 archetypes

- `region_id`: `"pnw"`
- `region_label`: `"Maritime Pacific Northwest: Puget Sound and Willamette Valley"` (verbatim; no
  em dash; use this exact string, do not paraphrase -- `region_label` renders verbatim on the
  frontend)
- `zone_span`: `["8", "9"]` -- **LOCKED** (design spec §4.1). Every pnw cell's `resolved_by_zone`
  carries **exactly** the keys `"8"` and `"9"`, no more, no fewer. This will be gate-enforced once a
  later task adds `pnw: ["8", "9"]` to `zone_span_gate.EXPECTED_SPANS` (A45, span<->key parity) --
  **not done by Task 1**; this doc only fixes the value every later task authors against.
- **Frost-ANCHORED discipline, non-negotiable across all archetypes that carry it:**
  `resolution_method = "frost_anchored_resolved"` for annuals/herbs/berries/strawberry;
  `resolved_from` carries **real** `{"last_frost": <date>, "first_frost": <date>}` (never null --
  this is the opposite of RGV's `{null, null}` invariant). `cold_pause` is a **legitimate, expected**
  winter token for a pnw annual calendar (RGV's auditor forbids `cold_pause`; a generalized
  `tools/region_cell_audit.py` for PNW must NOT carry that forbidding rule over -- flagged for Task
  2). Tree cells (`perennial_precompute`/`perennial_evergreen_precompute`) carry `resolved_from` with
  the real frost dates too (chill-gated trees) or omit frost entirely for the citrus's per-cell
  climate axis (cold, not chill -- see §5).
- **No summer `heat_pause` for cool-season crops, full stop.** Summer IS the growing window in the
  maritime PNW (design spec §2, §5) -- the opposite framing from RGV, where summer was the heat-driven
  planting gap. A cool-season crop's mid-summer months render `growing` (an in-season lull if any),
  never `heat_pause`. A **warm-season** crop MAY carry a T1-backed `heat_pause` only if a genuine
  summer heat gap is sourced -- this will be rare to nonexistent in the maritime PNW (the region
  *rations* heat, it does not have too much of it); default to no pause and handle warm-crop honesty
  through calendar shape + `region_notes_*` instead (§2.6).
- `resolution_method` is free-text provenance, not a gate-enforced enum (60+ distinct strings already
  live in the canonical). Use `"frost_anchored_resolved"` for the annual archetype (matches every
  other frost-anchored region exactly -- this is not a new string), `"perennial_precompute"` for
  chill-gated trees, `"perennial_evergreen_precompute"` for citrus.
- `sources` / `anchoring_urls`: every rule-layer entry (`plantings[]` sub-objects) and every zone-row
  carries its own `sources` (source-catalog ids) + `anchoring_urls` (id -> `{url, verified}`) pair.
  T1-or-it-doesn't-ship holds. `wsu_ext` (Washington State University Extension) and `osu_ext` (Oregon
  State University Extension) are **already catalogued** T1 sources
  (`source_catalog.wsu_ext`/`.osu_ext`, both `tier: "T1"`, `trust_tier: "high"`) -- use these ids in
  every worked example below; Tasks 3-7 add the exact WSU/OSU publication id(s) per crop class, not a
  generic placeholder, the same way the RGV arc added specific TAMU publication ids on top of the
  generic `tamu_agrilife` catalog entry.
- Unlike RGV (which had no z8-appropriate zone to borrow and so authored both zones distinctly by
  default), PNW's z8/z9 split is real and load-bearing (z8 = colder Puget/Willamette lowlands
  interior, z9 = milder coastal/protected pockets) -- author both zones distinctly wherever the
  source differentiates them. The `lifted_from_zone` donor-clone pattern remains legal (per the usual
  2-zone-span convention) only where WSU/OSU genuinely does not differentiate z8 from z9 for a given
  crop.
- Compact-JSON rule: never write the real splice with `indent=2`. This doc's blocks are pretty for the
  human reader only.

---

## 2. Archetype 1 -- frost-anchored ANNUAL cell

**Who gets this shape:** the 79 `frost_anchored` annuals, plus the non-tree perennials that carry a
real seasonal calendar (`perennial_woody_ornamental` -- rosemary/oregano/sage/thyme/lavender;
`berries_woody` -- blackberry/blueberry/raspberry/elderberry; `perennial_herbaceous` -- strawberry).
~89 crops total (design spec §3). This is the biggest batch (Task 4 + part of Task 7).

### 2.1 Cell-level keys

Identical to every other region's annual cell shape -- PNW adds no new top-level key:

| Key | Shape | Note |
|---|---|---|
| `region_id` | string | `"pnw"` |
| `region_label` | string | `"Maritime Pacific Northwest: Puget Sound and Willamette Valley"` |
| `zone_span` | `["8","9"]` | locked |
| `sources` | `[id, ...]` | region-level source list |
| `plantings` | `[{...}, ...]` | the **rule layer** -- offsets off named frost anchors, not absolute dates |
| `resolved_by_zone` | `{"8": {...}, "9": {...}}` | the **render layer** -- absolute dates + `calendar[]` |
| `region_notes_beginner` | string \| null | dual-register prose |
| `region_notes_seasoned` | string \| null | dual-register prose |

### 2.2 `plantings[]` entries -- anchor to `last_frost` / `first_frost`, the STANDARD vocabulary

**This is the load-bearing flip from RGV's contract.** RGV forced every `plant_out`/`start_indoors`
entry to anchor off a synthetic `"transplant_window"` token (offset 0) because RGV has no frost to
anchor to. PNW has a real winter, so its `plantings[]` entries use the **ordinary** frost-anchored
vocabulary every pre-existing frost-anchored region already uses:
`"from": "last_frost"` (spring establishment/set-out, negative or small offsets -- transplants often
go out a couple weeks *before* last frost for frost-tolerant crops like brassicas) and
`"from": "first_frost"` (fall/second-planting entries, negative offsets counting back from the first
fall frost) or `"from": "plant_out"` (harvest entries, positive offsets off the crop's own set-out).
**Never** `"transplant_window"`, `"frost_free_spring"`, `"soil_workable"`, `"heat_subsiding"`, or
`"fall_open"` -- those are the RGV/se_gulf-donor vocabulary that does not apply here. Each entry
carries its own `sources` + `anchoring_urls` + (seasoned register) `synthesis_note_seasoned`.

### 2.3 `resolved_by_zone["8"|"9"]` keys

| Key | Required? | Note |
|---|---|---|
| `plant_out` | required | absolute month/date-range string |
| `start_indoors` | conditional | present only if the crop is tray-started |
| `harvest`, `harvest_start`, `harvest_end` | required | |
| `first_plant_date`, `last_plant_date` | required | mirror the SPRING/primary succession's window only (not the fall second_planting's) -- matches every existing frost-anchored cell's convention |
| `calendar` | required, 12 tokens | must be internally coherent with the window fields (see §2.4's derivation note) -- never fabricated independent of the dates. Token enum: `plant, harvest, indoors, growing, heat_pause, cold_pause, season_over, wait` |
| `resolution_method` | required | `"frost_anchored_resolved"` -- see §1 |
| `resolved_from` | required | `{"last_frost": <real date>, "first_frost": <real date>}` -- hard invariant, never null (the exact opposite of RGV, see §1) |
| `second_planting` | conditional | author where a real fall cycle exists (common for PNW's long cool season -- many cool-season crops genuinely run a spring + fall cycle here); shape = `{plant_out, start_indoors, harvest_start, harvest_end, sources, anchoring_urls}` -- all four window keys required if the object is present at all |
| `heat_pause` | conditional, EXPECTED RARE | only if a genuine T1-backed summer heat gap is sourced -- see §2.6. The maritime PNW's default posture is "no heat_pause" for the vast majority of crops, cool- and warm-season alike |
| `succession_spring` / `succession_fall` | conditional | present only if the crop runs multiple succession sowings within a season |
| `successions_realized` | conditional | derived count; present only if the crop is in succession scope (`tools/derive_realized_successions.py`) |
| `sources`, `anchoring_urls` | required | zone-row citation |
| `notes`, `zone_notes`, `planting_note` | required key, null-able value | present (possibly `null`) unless there is a real per-zone caveat to author |
| `lifted_from_zone` | conditional | only if this zone's row was donor-cloned from the other (§1) |

### 2.4 Full worked example -- cool-season, spring + fall two-cycle (broccoli-style)

This is the dominant PNW annual pattern: a cool-season crop (brassica, leafy green, root, cool herb,
pea) runs a spring cycle, a long mild summer (the growing/harvest window, not a pause), and often a
real second fall cycle behind it. Modeled directly on the shape of
`broccoli.regions.northern_tier` (the closest already-shipped **frost-anchored, two-cycle** analog --
picked over `ca_north_coast`'s continuous-succession shape because it is the simpler, more common
single-plus-second-planting pattern most of the 79 annuals will actually use). Illustrative
placeholder crop, values NOT sourced (frost dates per §0's fixed placeholders: z8 last frost Apr 15 /
first frost Nov 1; z9 last frost Apr 1 / first frost Nov 15):

```json
{
  "region_id": "pnw",
  "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
  "zone_span": ["8", "9"],
  "sources": ["wsu_ext", "osu_ext"],
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
          "synthesis_note_seasoned": "Start transplants indoors about 6 to 7 weeks before the last frost; the crop tolerates light frost, so it goes out ahead of the frost-free date (WSU / OSU west-side planting guides).",
          "sources": ["wsu_ext"],
          "anchoring_urls": {
            "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
          },
          "uscrn_validation": null
        }
      ],
      "plant_out": [
        {
          "from": "last_frost",
          "offset_days": -21,
          "window_days": 21,
          "synthesis_note_seasoned": "Set out spring transplants about 3 weeks before the last frost; a light frost does not damage established plants of this crop (WSU / OSU).",
          "sources": ["wsu_ext"],
          "anchoring_urls": {
            "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_start": [
        {
          "from": "plant_out",
          "offset_days": 60,
          "window_days": 0,
          "synthesis_note_seasoned": "Matures in roughly 60 days in the mild, cool spring-into-summer window (WSU / OSU).",
          "sources": ["wsu_ext"],
          "anchoring_urls": {
            "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_end": [
        {
          "from": "plant_out",
          "offset_days": 80,
          "window_days": 0,
          "synthesis_note_seasoned": "End of the spring harvest window before the crop is replaced by the fall planting.",
          "sources": ["wsu_ext"],
          "anchoring_urls": {
            "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
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
          "synthesis_note_seasoned": "Fall crop: start or sow the second planting in midsummer for a harvest that runs into fall behind the mild first frost (OSU / WSU).",
          "sources": ["osu_ext"],
          "anchoring_urls": {
            "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
          },
          "uscrn_validation": null
        }
      ],
      "plant_out": [
        {
          "from": "first_frost",
          "offset_days": -75,
          "window_days": 21,
          "synthesis_note_seasoned": "Set out fall transplants in mid to late summer; heads or roots finish as the weather cools and tolerate the region's light early frosts (OSU / WSU).",
          "sources": ["osu_ext"],
          "anchoring_urls": {
            "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_start": [
        {
          "from": "plant_out",
          "offset_days": 65,
          "window_days": 0,
          "synthesis_note_seasoned": "Fall crop matures in cooling weather; the maritime PNW's mild fall lets it finish slowly without a hard cutoff (OSU).",
          "sources": ["osu_ext"],
          "anchoring_urls": {
            "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
          },
          "uscrn_validation": null
        }
      ],
      "harvest_end": [
        {
          "from": "first_frost",
          "offset_days": 14,
          "window_days": 0,
          "synthesis_note_seasoned": "Fall harvest continues past the first light frost; this crop tolerates it (WSU / OSU).",
          "sources": ["wsu_ext"],
          "anchoring_urls": {
            "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
          },
          "uscrn_validation": null
        }
      ],
      "anchoring_urls": {}
    }
  ],
  "resolved_by_zone": {
    "8": {
      "plant_out": "Mar 25 - Apr 15",
      "start_indoors": "Feb 25 - Mar 18",
      "harvest": "May 24 - Nov 15",
      "harvest_start": "May 24",
      "harvest_end": "Nov 15",
      "first_plant_date": "Mar 25",
      "last_plant_date": "Apr 15",
      "calendar": ["cold_pause", "indoors", "plant", "plant", "harvest", "harvest", "indoors", "plant", "plant", "harvest", "harvest", "cold_pause"],
      "notes": null,
      "zone_notes": null,
      "planting_note": null,
      "sources": ["wsu_ext"],
      "anchoring_urls": {
        "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
      },
      "resolution_method": "frost_anchored_resolved",
      "second_planting": {
        "start_indoors": "Jul 14 - Aug 13",
        "plant_out": "Aug 18 - Sep 8",
        "harvest_start": "Oct 22",
        "harvest_end": "Nov 15",
        "sources": ["osu_ext"],
        "anchoring_urls": {
          "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
        }
      },
      "succession_spring": "Mar 25, Apr 15",
      "succession_fall": "Aug 18, Sep 8",
      "resolved_from": {"last_frost": "Apr 15", "first_frost": "Nov 1"},
      "successions_realized": 4
    },
    "9": {
      "plant_out": "Mar 11 - Apr 1",
      "start_indoors": "Feb 11 - Mar 4",
      "harvest": "May 10 - Nov 29",
      "harvest_start": "May 10",
      "harvest_end": "Nov 29",
      "first_plant_date": "Mar 11",
      "last_plant_date": "Apr 1",
      "calendar": ["cold_pause", "indoors", "plant", "plant", "harvest", "growing", "indoors", "indoors", "plant", "growing", "harvest", "cold_pause"],
      "notes": null,
      "zone_notes": null,
      "planting_note": null,
      "sources": ["wsu_ext"],
      "anchoring_urls": {
        "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
      },
      "resolution_method": "frost_anchored_resolved",
      "second_planting": {
        "start_indoors": "Jul 28 - Aug 27",
        "plant_out": "Sep 1 - Sep 22",
        "harvest_start": "Nov 5",
        "harvest_end": "Nov 29",
        "sources": ["osu_ext"],
        "anchoring_urls": {
          "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
        }
      },
      "succession_spring": "Mar 11, Apr 1",
      "succession_fall": "Sep 1, Sep 22",
      "resolved_from": {"last_frost": "Apr 1", "first_frost": "Nov 15"},
      "successions_realized": 4
    }
  },
  "region_notes_beginner": "West of the Cascades, this crop gets one of the best growing seasons anywhere in the country: long, cool, and mild. Start transplants indoors in late winter and set them out in early spring for a first crop by early summer. Set out a second round of transplants in midsummer for a fall harvest that often runs into November. There is no need to dodge summer heat here: summer is simply the growing season, not a pause.",
  "region_notes_seasoned": "The maritime Pacific Northwest's cool, marine-tempered summer is this crop's strong axis, not a heat problem to plan around. Set spring transplants out about three weeks ahead of the last frost for an early-summer harvest, then run a second, fall-directed planting from midsummer transplants for a harvest that often carries into November behind the season's first frost. Winters here are mild enough that the calendar shows only a short cold pause rather than a long dormant stretch. Watch for slugs and downy mildew in the wet season; summer heat is not a limiting factor for this crop here."
}
```

**Calendar-derivation callout (read before authoring Task 4's real cells).** The `calendar[]` arrays
above were built by hand-tracing each window's touched months (spring `start_indoors`/`plant_out`,
spring `harvest`, fall `second_planting.start_indoors`/`plant_out`/`harvest`) with the priority
`plant > harvest > indoors`, then verified to produce **zero violations** against the actual live
gate functions in this repo: `annual_calendar_violations` (A24, placement), `annual_coherence_violations`
(A5, token-enum + heat_pause alignment), and `indoors_run_backing_violations` (every `indoors` run
overlaps a real start-indoors window). **A concrete finding for Task 4:** running the literal
`tools/annual_calendar.py:derive_annual_calendar()` function against this same cell (top-level
`plant_out`/`harvest_start`/`harvest_end` only, the way the function reads it) produces a WRONG
calendar -- it does not fold `second_planting`'s own windows into the derivation, so it over-extends
`harvest` across Jul-Oct even though the fall cycle is actually re-planting (indoors, then plant) in
those months. This matches the tool's own docstring caveat: it "cannot reproduce ~190/200 certified
annual cells" and multi-cycle (second_planting-bearing) cells are "legitimately hand-authored." **For
any PNW annual with a `second_planting`, hand-verify the calendar against the true activity per month
(not the naive single-window deriver output), and confirm zero violations from the three gate
functions above before shipping the cell.** Single-cycle cells (no fall reset -- e.g. a crop harvested
once and done) should still literally match `derive_annual_calendar()`'s output.

### 2.5 Warm-season delta -- transplant-led, honest-marginality framing

Warm-season crops (tomato, pepper, eggplant, melon, sweet corn, squash, cucumber, okra, sweet potato)
run a **single**, transplant-led, often-compressed cycle rather than the cool-season two-cycle
pattern -- the maritime PNW's mild, short-on-heat summer does not give these crops a second window,
and unlike RGV there is no viable fall reset for most of them. The delta from §2.4 lives entirely in
`resolved_by_zone[z]`:

```json
{
  "plant_out": "May 15 - Jun 5",
  "start_indoors": "Mar 25 - Apr 15",
  "harvest_start": "Aug 10",
  "harvest_end": "Oct 1",
  "resolution_method": "frost_anchored_resolved",
  "resolved_from": {"last_frost": "Apr 15", "first_frost": "Nov 1"}
}
```

No `second_planting`, no `heat_pause` (there is no heat to pause for -- see §1). The honesty for a
genuinely heat-hungry crop (melon, okra, sweet potato, a long-season pepper) lives in **the calendar
shape itself** (a late, short plant-out-to-harvest window, often clipped tight against the first
frost) plus `region_notes_*` prose that plainly states the marginality and steers toward early or
short-season cultivars, warmest-microsite siting, and cloche/row-cover framing where the T1 source
supports it -- **never** a `suitability` field (the annual archetype carries none; only trees and
citrus have `suitability`). This is the PNW analog of RGV's per-crop honesty calls for its own
marginal cases, just aimed at the opposite climate axis (heat, not cold/frost).

### 2.6 The summer rule (binding on every annual cell, both variants) -- restated explicitly

**Cool-season crops: summer renders `growing` (or `harvest`), never `heat_pause`.** This is the single
most important inversion from RGV, where summer was the default planting gap
(`season_over`/`heat_pause`). In the maritime PNW, summer is cool, dry, and long -- it is the season,
not an obstacle. **Warm-season crops: also no `heat_pause` by default** -- their honesty lives in a
compressed, transplant-anchored calendar and prose (§2.5), not a declared pause, because the PNW's
problem is a *shortage* of summer heat, not an excess of it; a `heat_pause` object asserts "too hot,"
which is never the PNW's story. Author a `heat_pause` object only in the rare case a T1 source states
a genuine mid-summer heat-driven stop for a specific crop (this is expected to be at or near zero
occurrences across the 79 annuals) -- never invent one to "fill in" what is actually just an
in-season lull (`growing`) or, off the growing window entirely, `cold_pause`.

### 2.7 Gates that bind this shape

A2 (region-fill completeness), A5/A5b/A5c (annual calendar coherence + indoors-run backing), A8
(successions_realized, if in scope), A24 (calendar-placement drift), A31/A32 (region-roster + real-
calendar floor -- A32 applies to `{frost_anchored, perennial_herbaceous, berries_woody,
perennial_woody_ornamental}`, this archetype's scope), A45 (zone_span exact-match, once `pnw` lands in
`EXPECTED_SPANS`). None of these are new gates for PNW; they already run roster-wide.

---

## 3. Archetype 2 -- fruiting TREE cell (the flagship)

**Who gets this shape:** the chill-gated deciduous fruit that DO fruit here -- apple, pear-european,
pear-asian, cherry-sweet, cherry-sour, plum, apricot, nectarine, peach, fig, mulberry, persimmon
(design spec §5). The maritime PNW banks ample winter chill (~700-1,300 hours, comparable to the
existing `northern_tier` z5-z7 band), clearing the fruiting threshold for nearly the whole chill-gated
roster. **This is the region's flagship archetype, the inverse of RGV's citrus flagship** -- most of
the 14 chill-gated trees FRUIT here, honestly and reliably.

### 3.1 Cell-level keys

| Key | Shape | Note |
|---|---|---|
| `region_id` / `region_label` / `zone_span` / `sources` | as §1 | |
| `plantings` | `[{...}]`, exactly ONE entry | `track: "perennial"`; no `start_indoors`, no `direct_sow`, no succession/second_planting (`perennial_gate.py` enforces this -- a tree is planted once) |
| `resolved_by_zone` | `{"8": {...}, "9": {...}}` | |
| `region_notes_beginner` / `region_notes_seasoned` | string \| null | |
| `chill_basis_seasoned` / `chill_basis_beginner` | string | region-level chill narrative (chill-delivered lives in the shared top-level `region_chill_delivered.pnw` table, not per-cell -- A18; this pair is the prose companion) |
| `plantings_provenance` | nullable | present, may be null |

### 3.2 `resolved_by_zone["8"|"9"]` keys

| Key | Note |
|---|---|
| `plant_out` | dormant-season bare-root/container window (absolute display string) |
| `resolution_method` | `"perennial_precompute"` |
| `suitability` | `"fruits_reliably"` for the flagship set (the modal PNW verdict); `"marginal"` for a cooler-summer-ripening caveat crop |
| `suitability_note_seasoned` / `suitability_note_beginner` | dual-register honesty prose |
| `bloom`, `harvest_start`, `harvest_end`, `harvest` | real display windows -- **`calendar[]` is DERIVED from these two fields** via `tools/tree_calendar.py:derive_tree_calendar(bloom, harvest)` (prune = month before bloom; bloom = bloom-open month; growing = bloom+1..harvest_start-1; harvest = the harvest span; care = the month after harvest end; dormant = the rest). This is gate-enforced (`tree_calendar_violations`, A4): a stored calendar that does not equal the function's output on the cell's own `bloom`/`harvest` fields is a hard violation. **Do not hand-invent tree calendars; run the deriver (or its exact algorithm) against the authored bloom/harvest windows.** |
| `frost_risk_note_seasoned` | string |
| `resolved_from` | `{"last_frost": <date>, "first_frost": <date>, "chill_hours": [lo, hi]}` -- real frost dates AND a chill band (mirrors `apple.regions.northern_tier`'s shape exactly) |
| `sources`, `anchoring_urls` | required |

### 3.3 Full worked example -- fruits_reliably (apple/pear/cherry/plum pattern)

Modeled on `apple.regions.northern_tier` (z5-z7 rows, its "prime apple country" fruiting band),
substituting PNW's frost dates and a comparable substantial chill band. Illustrative placeholder crop,
values NOT sourced. `calendar[]` below is the **actual, verified output** of
`tree_calendar.derive_tree_calendar(bloom, harvest)` run against this example's own `bloom`/`harvest`
strings -- not hand-typed:

```json
{
  "region_id": "pnw",
  "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
  "zone_span": ["8", "9"],
  "sources": ["wsu_ext", "osu_ext"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "establishment",
      "track": "perennial",
      "plant_out": [
        {
          "label": "bare_root_dormant",
          "from": "last_frost",
          "offset_days": -90,
          "window_days": 75,
          "sources": ["wsu_ext"],
          "anchoring_urls": {
            "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
          }
        }
      ],
      "bloom": [
        {
          "label": "primary",
          "from": "last_frost",
          "offset_days": 7,
          "window_days": 21,
          "sources": ["osu_ext"],
          "anchoring_urls": {
            "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
          }
        }
      ],
      "harvest_start": [
        {"label": "primary", "from": "bloom_start", "offset_days": 120, "sources": ["osu_ext"],
         "anchoring_urls": {"osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}}}
      ],
      "harvest_end": [
        {"label": "primary", "from": "bloom_start", "offset_days": 165, "sources": ["osu_ext"],
         "anchoring_urls": {"osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}}}
      ],
      "anchoring_urls": {
        "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
      },
      "sources": ["wsu_ext"]
    }
  ],
  "plantings_provenance": null,
  "resolved_by_zone": {
    "8": {
      "plant_out": "Dec - Feb (dormant, bare-root or container)",
      "resolution_method": "perennial_precompute",
      "suitability": "fruits_reliably",
      "suitability_note_seasoned": "Ample winter chill and a long, mild growing season let early to mid-season varieties fruit dependably here. The latest-ripening keeper varieties can run marginal in the coolest, wettest sites, where a shorter effective summer limits full ripening (WSU / OSU home orchard guidance).",
      "suitability_note_beginner": "This fruits well here. Choose an early to midseason variety for the most dependable results.",
      "bloom": "Apr 22 - May 13",
      "harvest_start": "Aug 20",
      "harvest_end": "Oct 4",
      "harvest": "Aug 20 - Oct 4",
      "calendar": ["dormant", "dormant", "prune", "bloom", "growing", "growing", "growing", "harvest", "harvest", "harvest", "care", "dormant"],
      "frost_risk_note_seasoned": "Bloom occurs safely after the typical last frost in most years; an unusually late cold snap during bloom is an occasional, not typical, risk here.",
      "resolved_from": {"last_frost": "Apr 15", "first_frost": "Nov 1", "chill_hours": [900, 1300]},
      "sources": ["wsu_ext"],
      "anchoring_urls": {
        "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
      }
    },
    "9": {
      "plant_out": "Nov - Feb (dormant, bare-root or container)",
      "resolution_method": "perennial_precompute",
      "suitability": "fruits_reliably",
      "suitability_note_seasoned": "The mildest coastal and protected-lowland sites still bank enough winter chill for the full recommended-variety roster, with an even longer frost-free shoulder than the interior lowlands. Chill is not the limiter here; a cooler, shorter effective summer near the immediate coast can still pinch the latest-ripening keepers (WSU / OSU).",
      "suitability_note_beginner": "This fruits well here too, and the season starts a bit earlier than the colder inland pockets.",
      "bloom": "Apr 8 - Apr 29",
      "harvest_start": "Aug 6",
      "harvest_end": "Sep 20",
      "harvest": "Aug 6 - Sep 20",
      "calendar": ["dormant", "dormant", "prune", "bloom", "growing", "growing", "growing", "harvest", "harvest", "care", "dormant", "dormant"],
      "frost_risk_note_seasoned": "Bloom occurs even earlier here than the colder interior lowlands and safely clears the milder last-frost date in most years.",
      "resolved_from": {"last_frost": "Apr 1", "first_frost": "Nov 15", "chill_hours": [700, 1100]},
      "sources": ["osu_ext"],
      "anchoring_urls": {
        "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
      }
    }
  },
  "region_notes_beginner": "This is prime fruit-tree country. Ample winter chill and a long, mild growing season let most varieties fruit reliably from Puget Sound to the Willamette Valley. Plant a bare-root or container tree while it is still dormant, from late fall through late winter.",
  "region_notes_seasoned": "The maritime Pacific Northwest banks abundant winter chill and offers a long, cool growing season, the region's tree-fruit flagship. Early to mid-season varieties ripen reliably across both zones; the latest-ripening keeper varieties can be marginal in the coolest, wettest sites closer to the coast or at the region's cooler margins, where a shorter effective summer limits full ripening. Plant bare-root or container trees during the dormant season, from late fall through late winter, while the ground is workable.",
  "chill_basis_seasoned": "Maritime Pacific Northwest winters bank a substantial, reliable chill accumulation, roughly 700 to 1,300 hours depending on zone and site, comfortably clearing the requirement of nearly every variety in this guide. Chill is never the limiting factor here; growing-season warmth for the latest-ripening varieties is the real variable.",
  "chill_basis_beginner": "Winters here are plenty cold for this tree. Nearly any variety gets all the winter chill it needs."
}
```

### 3.4 Delta -- the cool-summer ripening caveat (still `fruits_reliably`, honest prose)

Design spec §5 flags that some fruiting-set crops (late-ripening peach/fig variants, for example) may
carry a genuine cool-summer ripening caveat even while still classified `fruits_reliably` overall
(the tree fruits; specific late varieties are the caveat, not the whole crop). Where the T1 source
supports it, note this honestly in `suitability_note_*` (as §3.3's worked example already does for
apple's latest keepers) rather than downgrading the whole cell to `marginal` -- reserve `marginal` for
a crop/site combination where the source genuinely calls the *overall* fruiting outcome marginal, not
merely "the latest variety in the lineup is a stretch." This mirrors RGV's own pattern of per-crop
honesty living in prose first, `suitability` enum second.

### 3.5 Gates that bind this shape

A3 (`perennial_gate.py` -- suitability enum membership, single perennial establishment entry,
`fruits_reliably`/`marginal` must carry a non-empty calendar), A4 (`tree_calendar_violations` --
`calendar[]` must equal `derive_tree_calendar(bloom, harvest)` exactly, not merely "close"), A31
(region-roster floor). **A32 does NOT apply to trees** (`coverage_floor_gate.CALENDAR_PRESENCE_BASES`
= `frost_anchored`, `perennial_herbaceous`, `berries_woody`, `perennial_woody_ornamental` --
Archetype 1's scope, not the tree archetypes; trees are exempt and governed by A3/A4 instead).

---

## 4. Archetype 3 -- edge/heat-limited TREE cell

**Who gets this shape:** the chill-gated tree fruit whose PNW limiter is **cool summers, not chill** --
pomegranate and pawpaw are design spec §5's named edge cases (pomegranate wants more sustained summer
heat than the maritime PNW gives; pawpaw wants summer heat plus humidity). Any other late-ripening
caveat crop belongs in §3.4 instead (still `fruits_reliably`, honest prose) unless the T1 evidence is
severe enough to warrant a genuine `marginal` (or, rarely, `unsuitable`) verdict.

**Important, a correction to the shorthand in the task brief:** `SUITABILITY_ENUM` in
`tools/perennial_gate.py` is exactly `{"fruits_reliably", "marginal", "survives_no_fruit",
"unsuitable"}` -- there is **no bare `"survives"` value**. Where this doc (or the task brief) says
"survives," the enum-correct value is **`"survives_no_fruit"`**. Using a literal `"survives"` string
will fail A3 outright (not in the 4-value enum). This archetype's practical choices are
**`"marginal"`** (calendar REQUIRED, non-empty -- the tree blooms and sometimes sets fruit, but
ripening is a genuine coin flip) or **`"survives_no_fruit"`** (calendar optional -- for a
chill-gated tree, `perennial_gate.py`'s no-fruit direction split is **chill-driven only**; since
pomegranate/pawpaw's PNW limiter is heat, not chill, `survives_no_fruit` here may legally carry either
an empty or a real calendar, both honest -- the chill Goldilocks-band check simply does not gate this
crop's case one way or the other) or **`"unsuitable"`** (calendar MUST be empty -- reserve for a crop
whose T1 evidence says it cannot even reliably survive/establish, not merely fails to ripen).

### 4.1 Full worked example (`marginal`, pomegranate/pawpaw pattern)

`calendar[]` below is again the actual, verified output of `derive_tree_calendar(bloom, harvest)` --
a late bloom (needs real warmth to start) and a narrow, late harvest window that a cool PNW summer
frequently fails to fully deliver on. Illustrative placeholder crop, values NOT sourced:

```json
{
  "region_id": "pnw",
  "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
  "zone_span": ["8", "9"],
  "sources": ["wsu_ext", "osu_ext"],
  "plantings": [
    {
      "succession_id": 1,
      "label": "establishment",
      "track": "perennial",
      "plant_out": [
        {"label": "container_spring", "from": "last_frost", "offset_days": 14, "window_days": 45,
         "sources": ["osu_ext"],
         "anchoring_urls": {"osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}}}
      ],
      "bloom": [
        {"label": "primary", "from": "last_frost", "offset_days": 50, "window_days": 30,
         "sources": ["osu_ext"],
         "anchoring_urls": {"osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}}}
      ],
      "harvest_start": [
        {"label": "primary", "from": "bloom_start", "offset_days": 140, "sources": ["osu_ext"],
         "anchoring_urls": {"osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}}}
      ],
      "harvest_end": [
        {"label": "primary", "from": "bloom_start", "offset_days": 175, "sources": ["osu_ext"],
         "anchoring_urls": {"osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}}}
      ],
      "anchoring_urls": {
        "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
      },
      "sources": ["osu_ext"]
    }
  ],
  "plantings_provenance": null,
  "resolved_by_zone": {
    "8": {
      "plant_out": "Apr - Jun (container, warmest available site)",
      "resolution_method": "perennial_precompute",
      "suitability": "marginal",
      "suitability_note_seasoned": "The tree survives and often blooms in the maritime PNW's mild winters, but our cool, marine-tempered summers rarely deliver the sustained heat this crop needs to size and fully ripen its fruit. Site it in the single warmest, most reflected-heat spot in the garden (a south-facing wall is ideal); expect a bonus crop in a hot year, not a dependable annual harvest (WSU / OSU).",
      "suitability_note_beginner": "This tree can live and even flower here, but our summers usually are not hot enough to ripen the fruit well. Treat any fruit as a bonus, not a sure thing, and give it the warmest spot you have.",
      "bloom": "Jun 5 - Jul 5",
      "harvest_start": "Oct 20",
      "harvest_end": "Nov 10",
      "harvest": "Oct 20 - Nov 10",
      "calendar": ["dormant", "dormant", "dormant", "dormant", "prune", "bloom", "growing", "growing", "growing", "harvest", "harvest", "care"],
      "frost_risk_note_seasoned": "Frost is not the limiting factor for this crop here; insufficient sustained summer heat is the binding constraint on a full, sweet harvest.",
      "resolved_from": {"last_frost": "Apr 15", "first_frost": "Nov 1", "chill_hours": [900, 1300]},
      "sources": ["osu_ext"],
      "anchoring_urls": {
        "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
      }
    },
    "9": {
      "plant_out": "Apr - Jun (container, warmest available site)",
      "resolution_method": "perennial_precompute",
      "suitability": "marginal",
      "suitability_note_seasoned": "As with zone 8, winter is not the obstacle: this tree survives and blooms in the mild maritime winter. The limiter is the same cool, short summer, slightly earlier here but not meaningfully warmer. Expect fruit only in the warmest microsites in a hot year (WSU / OSU).",
      "suitability_note_beginner": "Same story as the colder zone here: the tree lives fine, but our cool summers rarely ripen the fruit well.",
      "bloom": "May 25 - Jun 25",
      "harvest_start": "Oct 10",
      "harvest_end": "Nov 5",
      "harvest": "Oct 10 - Nov 5",
      "calendar": ["dormant", "dormant", "dormant", "prune", "bloom", "growing", "growing", "growing", "growing", "harvest", "harvest", "care"],
      "frost_risk_note_seasoned": "Frost is not the limiting factor for this crop here; insufficient sustained summer heat is the binding constraint on a full, sweet harvest.",
      "resolved_from": {"last_frost": "Apr 1", "first_frost": "Nov 15", "chill_hours": [700, 1100]},
      "sources": ["osu_ext"],
      "anchoring_urls": {
        "osu_ext": {"url": "https://extension.oregonstate.edu", "verified": "2026-07-14"}
      }
    }
  },
  "region_notes_beginner": "This is a gamble crop here, not a sure thing. Winters are mild enough for the tree to live and flower, but our summers usually are not hot enough to ripen a full crop. Plant it only if you have the warmest, most sheltered spot in the garden and are growing it for the challenge.",
  "region_notes_seasoned": "Winter is not this crop's obstacle in the maritime Pacific Northwest; the tree survives and blooms reliably in the mild, chill-abundant winter here. The limiter is the region's defining trait working against it: a cool, marine-tempered summer that rarely delivers the sustained heat this crop needs to size and sweeten fruit. Treat it as a warmest-microsite specialty planting, not a dependable orchard crop."
}
```

### 4.2 Note on the `"unsuitable"` (empty-calendar) alternative

If Task 5's actual WSU/OSU sourcing pass finds a crop in this class where the T1 evidence is more
severe than "ripens poorly" -- genuinely cannot establish or reliably survive the maritime PNW's
combination of cool summers and wet winters -- author it `"unsuitable"` instead, mirroring RGV's own
"thin/null variant" (§4.2 of the RGV doc, modeled on `peach.regions.fl_peninsula`): `plant_out`,
`bloom`, `harvest_start`, `harvest_end`, `harvest` all `null`, `calendar: []`, and a
`suitability_note_*` that closes with an honest redirect. Do not default every edge case to
`"unsuitable"` just because it is the simpler shape -- `perennial_gate.py` requires the calendar to
match the declared verdict (`unsuitable` -> calendar MUST be empty; `marginal` -> calendar MUST be
non-empty), so the shape follows the sourced verdict, never the reverse.

### 4.3 Gates that bind this shape

A3 (`marginal` requires a non-empty calendar; `unsuitable` requires an empty one -- `perennial_gate.py`
lines 131-148), A4 (any non-empty calendar must equal `derive_tree_calendar(bloom, harvest)`), A31
(region-roster floor -- present even if the eventual verdict is `unsuitable`/empty). A32 does not
apply (trees are exempt, per §3.5).

---

## 5. Archetype 4 -- cold-limited CITRUS cell (`perennial_evergreen`)

**Who gets this shape:** the 5 evergreen citrus (grapefruit, lemon, lime, mandarin-clementine,
orange-navel). **This is the exact mirror-flip of RGV's citrus flagship.** RGV's citrus is the
region's premier tree fruit (frost-free, heat-abundant, `fruits_reliably`). PNW's citrus is the
opposite: cold-limited and heat-poor, honestly `unsuitable` (or, at best, `survives_no_fruit`) for
essentially the whole roster, in the ground or even as a container plant left outdoors (design spec
§5).

### 5.1 Cell-level keys

| Key | Shape | Note |
|---|---|---|
| `region_id` / `region_label` / `zone_span` / `sources` | as §1 | |
| `plantings` | `[{...}]`, exactly ONE entry, `track: "perennial"` | same tree-establishment constraint as Archetype 2/3 |
| `resolved_by_zone` | `{"8": {...}, "9": {...}}` | |
| `min_winter_temp_f` | `[lo, hi]` | region-level cold-damage band (the envelope across both zones) |
| `cold_basis_seasoned` / `cold_basis_beginner` | string | the region-level cold narrative -- **this is the primary honesty field for PNW citrus** (the mirror of RGV's `heat_basis_*` being its primary honesty field) |
| `heat_summer_basis` / `heat_basis_seasoned` / `heat_basis_beginner` | conditional | **only** for the 3 heat-gated citrus (grapefruit, mandarin-clementine, orange-navel -- crops carrying `"heat_accumulation"` in `gating_factors`), and **only required at the cell level when `suitability != "unsuitable"`** (`perennial_gate.py`'s heat floor skips entirely when the cell is `unsuitable` -- cold has already decided the case, so the heat datum would be moot). Lemon/lime never carry these fields (they are not heat-gated). |
| `plantings_provenance` | nullable | |

### 5.2 `resolved_by_zone["8"|"9"]` keys

| Key | Note |
|---|---|
| `plant_out` | display string, or `null` for the thin/`unsuitable` variant |
| `resolution_method` | `"perennial_evergreen_precompute"` |
| `suitability` | `"unsuitable"` is the modal PNW verdict for this archetype (see §5.3's enum-correction callout, same issue as §4) |
| `suitability_note_seasoned` / `suitability_note_beginner` | dual-register honesty prose, cold-led |
| `min_winter_temp_f` | `[lo, hi]` per-zone (may mirror the region-level pair) |
| `bloom`, `harvest_start`, `harvest_end`, `harvest` | `null` for the `unsuitable` thin variant (no calendar to derive from -- `calendar: []`, and `tree_calendar_violations`/`derive_evergreen_calendar` are skipped entirely for an empty calendar) |
| `calendar` | `[]` for `unsuitable` -- **hard requirement**, `perennial_gate.py` line 131-133 |
| `frost_risk_note_seasoned` | string |
| `resolved_from` | may be `{}` or omit frost/chill entirely (citrus is not chill-gated); cold is the only per-cell climate axis, and PNW's cold datum lives in `min_winter_temp_f`, not `resolved_from` |
| `sources`, `anchoring_urls` | required |

### 5.3 Full worked example -- `"unsuitable"`, cold-limited (orange-navel pattern)

Modeled on the SHAPE of `orange-navel.regions.northern_tier` (the existing "too cold, empty
calendar" reference cell) with the PROSE register of `orange-navel.regions.ca_north_coast` (a real
cold/heat-honesty citrus cell), substituting PNW's cold-limited framing. Illustrative placeholder
crop, values NOT sourced. **Enum-correction callout:** the task brief's shorthand
`suitability="survives"` is not a real value -- see §4's identical correction; the enum-correct
choices here are `"unsuitable"` (this worked example) or `"survives_no_fruit"` (§5.4):

```json
{
  "region_id": "pnw",
  "region_label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
  "zone_span": ["8", "9"],
  "sources": ["wsu_ext"],
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
      "suitability_note_seasoned": "Winters west of the Cascades bring periodic hard freezes into the teens and single digits Fahrenheit during Arctic outbreaks, well below the mid-20s°F wood-damage threshold for this crop, even though the average winter is much milder. Summers here also lack the sustained heat this crop needs to ripen sweet. Even a container tree brought under full cover for the coldest nights is a marginal proposition; this is not citrus country, in the ground or in a pot left outdoors (WSU).",
      "suitability_note_beginner": "This will not survive outdoors here. Our winters get too cold in a hard freeze and our summers do not get hot enough. If you want this in the maritime Pacific Northwest, grow it in a container you bring fully indoors for winter.",
      "min_winter_temp_f": [10, 20],
      "bloom": null,
      "harvest_start": null,
      "harvest_end": null,
      "harvest": null,
      "calendar": [],
      "frost_risk_note_seasoned": "An occasional deep Arctic-outbreak freeze, not the typical winter, is what makes this crop unviable outdoors here; even a mild-winter year does not deliver the summer heat to ripen it.",
      "resolved_from": {},
      "sources": ["wsu_ext"],
      "anchoring_urls": {
        "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
      }
    },
    "9": {
      "plant_out": null,
      "resolution_method": "perennial_evergreen_precompute",
      "suitability": "unsuitable",
      "suitability_note_seasoned": "The milder coastal and protected-lowland pockets still see an occasional hard freeze cold enough to kill this crop's wood, and even a mild winter here does not deliver the summer heat needed to ripen fruit sweet. Marginally less risky than the colder interior lowlands, but still not a viable outdoor planting (WSU).",
      "suitability_note_beginner": "A bit milder here than the colder spots, but still not safe outdoors long term, and summers still are not hot enough to ripen the fruit.",
      "min_winter_temp_f": [20, 30],
      "bloom": null,
      "harvest_start": null,
      "harvest_end": null,
      "harvest": null,
      "calendar": [],
      "frost_risk_note_seasoned": "Milder than the colder interior lowlands, but an occasional deep freeze still puts this crop at real risk outdoors.",
      "resolved_from": {},
      "sources": ["wsu_ext"],
      "anchoring_urls": {
        "wsu_ext": {"url": "https://extension.wsu.edu", "verified": "2026-07-14"}
      }
    }
  },
  "region_notes_beginner": "Skip this outdoors in the maritime Pacific Northwest. Winters get too cold in a hard freeze and summers do not get hot enough to ripen the fruit. Grow it in a container and bring it fully indoors for winter if you want to try.",
  "region_notes_seasoned": "This is the maritime Pacific Northwest's honest citrus story, the mirror of its role as a Gulf Coast or California flagship: winters here are mild in an average year but bring periodic hard freezes well below this crop's wood-damage threshold, and summers lack the sustained heat to ripen fruit sweet even where winter cold is not the limiter. Even container culture with full winter cover indoors is a marginal, high-effort proposition. This is not citrus country.",
  "min_winter_temp_f": [10, 30],
  "cold_basis_seasoned": "Puget Sound and Willamette Valley winters bring occasional Arctic-outbreak hard freezes into the teens and single digits Fahrenheit, well below the mid-20s°F point that damages or kills citrus wood, even though the typical winter low in most years is far milder. The risk is the severe, infrequent event, not the average winter (WSU).",
  "cold_basis_beginner": "Winters here look mild most years, but a hard freeze does happen from time to time, and it gets cold enough to kill this tree if left outdoors.",
  "plantings_provenance": null
}
```

### 5.4 Delta -- heat-gated citrus (grapefruit / mandarin-clementine / orange-navel) vs non-heat-gated (lemon / lime)

Orange-navel, grapefruit, and mandarin-clementine carry `"heat_accumulation"` in `gating_factors`;
lemon and lime do not (`gating_factors: ["cold_hardiness"]` only). Per `perennial_gate.py`'s heat
floor (lines 149-161): a heat-gated crop's cell must carry `heat_summer_basis` whenever
`suitability != "unsuitable"`. Since §5.3's worked example is `"unsuitable"` throughout, the heat
floor never triggers and `heat_summer_basis`/`heat_basis_*` are correctly omitted. **If Task 6's real
WSU/OSU sourcing lands a milder verdict for any zone** (e.g. a sheltered z9 pocket authored as
`"survives_no_fruit"` -- see §5.5 below), that cell (and the region-level pair) MUST add
`heat_summer_basis` (one of `HEAT_BASIS_ENUM = {"high", "adequate", "marginal", "insufficient"}` --
almost certainly `"insufficient"` for the maritime PNW) + `heat_basis_seasoned` + `heat_basis_beginner`
for the 3 heat-gated crops. Lemon and lime never carry these fields regardless of verdict -- adding
them "for consistency" is itself a violation-adjacent inconsistency (stray heat machinery on a
non-heat-gated crop), the same rule RGV's contract documented at its own §3.4.

### 5.5 Note on the `"survives_no_fruit"` alternative

Unlike Archetype 3's chill-gated trees, citrus is **not** chill-gated (`chill_hours` is not in a
`perennial_evergreen` crop's `gating_factors`), so `perennial_gate.py`'s chill Goldilocks-band split
never fires for `survives_no_fruit` here -- "a cold-only evergreen has no such [chill] band, so
`survives_no_fruit` may carry a calendar (blooms in mild years) or be empty (no dependable crop),
both honest" (`perennial_gate.py:134-138`). If Task 6's sourcing finds a genuinely milder verdict
for a sheltered z9 microclimate (the tree can survive and occasionally flower but not reliably fruit,
rather than being flatly unviable), author `"survives_no_fruit"` instead of `"unsuitable"` -- with
either an empty calendar (if the source does not support even an occasional bloom claim) or a real
bloom-only/thin calendar (if it does), plus the heat-gated delta from §5.4 if applicable. Do not
default the whole roster to `"unsuitable"` if the real T1 evidence supports a lesser verdict for
either zone -- follow the source, the same T1-over-template discipline every other archetype in this
doc follows.

### 5.6 Gates that bind this shape

A3 (`unsuitable` -> calendar MUST be empty; heat floor requires `heat_summer_basis` on the 3
heat-gated crops whenever `suitability != "unsuitable"`), A31 (region-roster floor -- present even
though `unsuitable`). A32 does not apply (trees/citrus exempt, per §3.5). A4/`tree_calendar_violations`
is a no-op here because the calendar is empty (the function only checks non-empty calendars).

---

## 6. Cross-archetype pre-flight checklist (Tasks 4-7, before handoff)

- [ ] `region_id` = `"pnw"`, `region_label` = `"Maritime Pacific Northwest: Puget Sound and Willamette Valley"` verbatim, no em dash
- [ ] `zone_span` = `["8","9"]`; `resolved_by_zone` keys are exactly `{"8","9"}`
- [ ] Annual/herb/berry/strawberry archetype: `resolution_method = "frost_anchored_resolved"`,
      `resolved_from` carries REAL `last_frost`/`first_frost` dates (never null -- the opposite of
      RGV); `plantings[]` anchors to `last_frost`/`first_frost`/`plant_out`, never
      `transplant_window`/`frost_free_spring`/`soil_workable`/`heat_subsiding`/`fall_open`
- [ ] No summer `heat_pause` on a cool-season crop's calendar (summer renders `growing`/`harvest`);
      a warm-season crop's honesty lives in calendar shape + prose, not a declared pause (rare
      exception: a genuinely T1-sourced summer heat gap, expected near-zero across the 79 annuals)
- [ ] `cold_pause` IS legitimate and expected on a PNW annual's winter months -- do not strip it the
      way RGV's auditor would
- [ ] `calendar[]` is internally coherent with the window fields: for a single-cycle annual, matches
      `tools/annual_calendar.py:derive_annual_calendar()`'s literal output; for a `second_planting`-
      bearing (multi-cycle) annual, hand-verified against `annual_calendar_violations` +
      `annual_coherence_violations` + `indoors_run_backing_violations` (the naive deriver
      over-extends `harvest` through a fall reset -- see §2.4's callout); for any tree/citrus
      non-empty calendar, EQUALS `tools/tree_calendar.py:derive_tree_calendar()` (or
      `derive_evergreen_calendar()` for citrus) run against the cell's own `bloom`/`harvest` fields --
      never hand-typed independently of the dates
- [ ] Tree/citrus archetype: `plantings[]` has exactly one entry, `track: "perennial"`, no
      `start_indoors`/`direct_sow`/succession/second_planting
- [ ] Fruiting tree (Archetype 2): `suitability` = `"fruits_reliably"` (modal) or `"marginal"`
      (cool-summer ripening caveat), non-empty calendar
- [ ] Edge/heat-limited tree (Archetype 3): `suitability` ∈
      `{"marginal", "survives_no_fruit", "unsuitable"}` -- **never the bare word "survives"** (not a
      real enum value; the enum-correct form is `"survives_no_fruit"`); `marginal` requires a
      non-empty calendar, `unsuitable` requires an empty one, `survives_no_fruit` may be either (no
      chill Goldilocks split applies to a heat-limited case)
- [ ] Citrus (Archetype 4): `suitability` ∈ `{"unsuitable", "survives_no_fruit"}` (modal:
      `"unsuitable"`) -- same enum correction as above; `unsuitable` -> calendar MUST be `[]`
- [ ] Heat-gated citrus only (grapefruit, mandarin-clementine, orange-navel): carries
      `heat_summer_basis` + `heat_basis_*` whenever `suitability != "unsuitable"`; lemon/lime never
      carry these fields regardless of verdict
- [ ] Every rule entry and zone-row carries real `sources` + `anchoring_urls` (T1 -- `wsu_ext` /
      `osu_ext` are already catalogued; add crop-class-specific WSU/OSU publication ids as Task 3's
      sourcing pass finds them, never leave this doc's placeholder URLs in a shipped cell)
- [ ] No em dashes in any `*_note_*`/`region_notes_*`/`chill_basis_*`/`cold_basis_*` prose; American
      English; `°F`; "plant" lowercase outside sentence-start
- [ ] Splice is compact JSON (no `indent=2`, no trailing newline) when it lands in the canonical

---

## 7. Out of scope (owned by a different task/session)

This doc is the **per-crop cell** contract only. It does NOT cover:

- `zone_span_gate.EXPECTED_SPANS["pnw"]` (the top-level span registration that makes A45 accept `pnw`
  cells at all -- design spec §4.4, a later task)
- `region_chill_delivered.pnw` + `region_chill_delivered_provenance` (the shared chill-band table
  Archetype 2/3's fruiting calls are consistent with -- design spec §4.5, Task 3)
- `region_source_map` (build-time authoring infrastructure, not a runtime-read field)
- The generalized `tools/region_cell_audit.py` / `tools/region_harness.py` / atomic-promote emitter
  (Task 2, 8-9) and the state-trio / footprint audit at promote (Task 10)
- The east-side wrinkle -- hot, dry east-of-the-Cascades z8 pockets (Spokane basin, Columbia Basin)
  that should NOT resolve to this maritime calendar; that is a plant-app ZIP3-fence concern (Task 11),
  not a dataset-build concern (design spec §4.1)
- Any plant-app ZIP3-fencing or plant-astro consumption

See the design spec for all of the above.

---

## Appendix -- reference-cell key sets captured 2026-07-14 (canonical `d0832254`)

```
broccoli.regions.ca_north_coast
  cell keys: region_id, region_label, zone_span, sources, plantings, resolved_by_zone,
             region_notes_beginner, zone_8_presence, region_notes_seasoned
  zone-row keys (z9/z10): plant_out, start_indoors, harvest, harvest_start, harvest_end,
             first_plant_date, last_plant_date, calendar, notes, zone_notes, planting_note,
             sources, anchoring_urls, resolution_method, second_planting, succession_spring,
             succession_fall, resolved_from, successions_realized
  resolution_method: frost_anchored_resolved; resolved_from real (e.g. z10 {"last_frost":"Jan 15",
             "first_frost":"Dec 31"}) -- note this region's own successions are continuous (5-wave),
             a more complex pattern than the northern_tier 2-cycle template this contract mirrors

broccoli.regions.northern_tier
  cell keys: region_id, region_label, zone_span, sources, plantings, plantings_provenance,
             resolved_by_zone, region_notes_beginner, region_notes_seasoned
  zone-row keys: same as ca_north_coast's zone-row set
  resolution_method: frost_anchored_resolved; resolved_from real (e.g. z3 {"last_frost":"May 15",
             "first_frost":"Sep 15"}) -- THE closest existing frost-anchored, 2-cycle (spring +
             second_planting fall) analog; this contract's §2.4 worked example mirrors ITS shape,
             not ca_north_coast's more complex continuous-succession shape

apple.regions.northern_tier
  cell keys: region_id, region_label, zone_span, sources, plantings, plantings_provenance,
             resolved_by_zone, region_notes_beginner, region_notes_seasoned, chill_basis_seasoned,
             chill_basis_beginner
  zone-row keys: plant_out, resolution_method, suitability, suitability_note_seasoned,
             suitability_note_beginner, bloom, harvest_start, harvest_end, harvest, calendar,
             frost_risk_note_seasoned, resolved_from, sources, anchoring_urls
  resolution_method: perennial_precompute; resolved_from carries last_frost + first_frost +
             chill_hours together (e.g. z5 [900,1300], z6 [800,1200], z7 [700,1100] -- this
             contract's §3.3 worked example's chill numbers are lifted directly from this real
             cell's z5/z7 rows, the closest real-world analog to PNW's expected substantial band)

orange-navel.regions.ca_north_coast
  cell keys: + min_winter_temp_f, cold_basis_seasoned, cold_basis_beginner, heat_summer_basis,
             heat_basis_seasoned, heat_basis_beginner, plantings_provenance
  zone-row keys: + min_winter_temp_f, heat_summer_basis (heat-gated: this crop carries
             "heat_accumulation" in gating_factors)
  suitability: "marginal" both zones -- but this is a HEAT-limited marginal (frost-safe, too cool
             to sweeten), the opposite direction from PNW's COLD-limited case; this contract's §5.3
             worked example borrows this cell's PROSE REGISTER (cold_basis_*/heat_basis_* framing
             style) but not its verdict or its heat-story content

orange-navel.regions.northern_tier
  suitability: "unsuitable" all 5 zones (z3-z7), min_winter_temp_f: [] every zone, calendar: []
             every zone -- the real "too cold, empty calendar" citrus reference cell; this contract's
             §5.3 worked example's SHAPE (null plant_out/bloom/harvest, empty calendar, empty
             plantings[] sub-lists) is modeled directly on this cell
```

Gate logic cross-referenced: `tools/whole_crop_gate.py` (A2, A5/A5b/A5c, A8, A24, A31/A32, A45),
`tools/annual_calendar.py` (`derive_annual_calendar`, `annual_calendar_violations`,
`annual_coherence_violations`, `indoors_run_backing_violations`, `heat_pause_backing_violations`,
`heat_flip_backing_violations`), `tools/tree_calendar.py` (`derive_tree_calendar`,
`derive_evergreen_calendar`, `tree_calendar_violations`), `tools/perennial_gate.py` (A3,
`SUITABILITY_ENUM`, `HEAT_BASIS_ENUM`, the no-fruit direction split, `gating_factors`,
`min_variety_chill`). Every `calendar[]` array in this doc's worked examples (§2.4, §2.5-omitted,
§3.3, §4.1) was checked against these functions directly (not by inspection alone) during authoring;
see each section's inline callout for the specific check run.
