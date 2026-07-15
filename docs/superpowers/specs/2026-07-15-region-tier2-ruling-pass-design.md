# Region Coverage Roadmap Item 5 -- Tier-2 Judged-Belt Ruling Pass -- Design Spec

**Status:** design, pending Trevor review 2026-07-15.
**Arc:** `docs/region_coverage_roadmap.md` item 5, the belt-by-belt ruling pass that follows RGV
(item 3, SHIPPED) and Maritime PNW (item 4, SHIPPED). **NOT a region-authoring arc.** No canonical
touch, no gate/code changes -- pure research + documentation.
**Runs in parallel with** the in-flight berry variety pilot (`docs/superpowers/plans/2026-07-15-berry-variety-pilot.md`).
Path-disjoint by construction: this arc never touches `crops_data_final.json`; the berry pilot's
only canonical touch is its own Trevor-gated Task 7 promote.
**Base canonical:** `8dd4ac4c` (read-only reference point; this arc does not re-stamp or splice).

---

## 1. Context and goal

The region program is a four-link chain (ZIP -> zone -> region -> dates). Items 1 (zone-span
widen), 3 (RGV), and 4 (PNW) shipped; item 2 (plant-app empty-ZIP cleanup) is plant-app's own
queue. Item 5 is next: five Tier-2 belts have zone-8+ ZIPs mapped to **no region at all**, so
`resolveFromZip` in plant-app can't offer one and those users see whatever the zone-only fallback
produces. The roadmap currently carries only unsourced "first reads" (mostly "probably ok") for
these belts. This arc replaces each with a cited ruling: **GENERIC-OK** (the zone-only fallback is
honestly close to what a real regional extension source says) or **NEW-REGION** (it materially
diverges, and the belt gets queued as its own future roadmap item -- a full spec/plan/build, not
built here).

## 2. What "generic zone dates" actually means (verified, not assumed)

Initial investigation suspected the per-crop `zones{}` field was the live no-region fallback --
it's populated for z8 on only 6 of 125 crops (the 5 tomato varieties + lettuce-leaf), and where
populated, its z8 sourcing is entirely Deep South (`uga_b577`, `uga_calendar`, `clemson_hgic`,
`tamu_agrilife`), not remotely representative of coastal Virginia or high-desert Nevada. That
looked alarming but is a dead end: `STATE_HISTORY.md` (the June cert sweep) records `zones{}` as
explicitly Trevor-ruled **"backend/UNRENDERED, LEAVE"** -- the app never shows it.

`tools/annual_calendar.py` itself only renders an already-resolved set of `plant_out`/`start_indoors`/
`harvest` windows into the 12-month `calendar[]` token array -- it does not take frost dates directly.
PNW's own arc hand-authored those windows from real WSU/OSU sources per crop/class; the deriver just
computed the display tokens from them. There is no verifiable, dataset-side record of exactly what
plant-app renders for a ZIP with no matching region (`zones{}` being dead rules that field out as an
answer for every zone, not just 8+). Rather than reverse-engineer unverifiable app internals, **this
arc's comparison baseline is a deliberately naive, region-blind construction**: build `plant_out`/
`start_indoors` windows for a crop directly from ITS OWN generic biology fields (`weeks_indoors`,
`days_to_maturity`, `frost_tolerance_f`) anchored to the belt's real frost dates, exactly the kind of
zone-only assumption a region-less experience embodies, run it through `tools/annual_calendar.py`,
and compare the result against the belt's real T1 regional guidance. This mirrors the framing PNW's
own writeup used ("generic zone dates that assume a hot summer the maritime PNW does not have") without
claiming to reproduce plant-app's private client logic byte-for-byte.

## 3. Scope: the 5 belts

| Belt | States (ZIP counts, z8 unless noted) | Roadmap first read |
|---|---|---|
| Mid-Atlantic | NC 793 (+20 z9), VA 258, MD 117, DC 215, DE/NJ/PA (small) | "probably ok (humid continental-lite)" |
| Mid-South | AR 460, OK 106, TN 122 (+1 z9), MO 6 | "probably ok" |
| Nevada | z8 15, z9 94, z10 1 | "probably ok (warm_arid adjacency)" |
| Utah | z8 15 | "probably ok (warm_arid adjacency)" |
| Alaska | z8 13 | "probably ok at this scale" |

Order (largest population impact first, so the highest-value belt is also where the method gets
its first real-world workout): **mid-Atlantic -> mid-South -> Nevada -> Utah -> Alaska.**

Puerto Rico (item 6) is explicitly out of scope -- it's a Trevor product-scope call, not a dataset
ruling.

## 4. Method: per-belt spot-check

For each belt, in order:

1. **Pick the marquee anchor.** The highest-ZIP-count state/city in the belt (e.g. Raleigh/Norfolk
   NC for mid-Atlantic). Get its real last/first frost dates (NOAA or the state extension's own
   figures, same standard PNW used for Sea-Tac/Astoria).
2. **Build the naive-baseline comparison** for a small representative crop basket spanning the
   classes that actually matter -- not one bellwether:
   - **one `frost_anchored` annual** (a widely-grown, well-documented crop): construct naive
     `plant_out`/`start_indoors` windows from the crop's own generic `weeks_indoors` /
     `days_to_maturity` / `frost_tolerance_f` fields anchored to the marquee city's real frost
     dates, run through `tools/annual_calendar.py`, and compare the resulting `calendar[]` and
     windows against the belt's real T1 planting calendar for that crop.
   - **one chill-gated tree fruit** (every one of these 5 belts genuinely grows tree fruit, and
     PNW's biggest surprise -- the A3 chill/fruit-set flip -- was exactly this class): there is no
     chill data at all today for a no-region ZIP (`region_chill_delivered` is a per-region table;
     a belt with no region has zero entries), so the comparison is finding a real published
     chill-hour estimate for the marquee city (a university extension chill map/tool) and checking
     whether it would classify the crop `fruits_reliably` / `marginal` / `survives_no_fruit`
     against its `chill_hours_required` floor -- i.e. whether the missing chill data is
     consequential (the verdict would clearly differ from a naive same-zone assumption) or moot
     (the belt's chill so clearly clears or fails the floor that a bespoke region would not change
     the story).
   - plus a berry or cool-season crop where regionally relevant, using the annual method above.
3. **Find the belt's real T1 extension calendar** for the same crops. Reuse already-catalogued
   sources where they exist (`vce_426_331`/`ncsu_ext` for mid-Atlantic, `usu_ext` for Utah,
   `unr_ext` for Nevada). **Where no T1 source is yet catalogued -- mid-South (AR/OK/TN/MO) and
   Alaska -- actively research and find the real land-grant extension source** (University of
   Arkansas, Oklahoma State, University of Tennessee, University of Missouri, UAF Cooperative
   Extension Service). A missing catalog entry is a research task, not a blocker and not license
   to cite a weaker T2 source instead. **`source_catalog` itself lives inside
   `crops_data_final.json`, so it is NOT written in this arc** (that would be a canonical touch);
   newly found sources are cited by institution + URL directly in the belt's research note.
   Formal `source_catalog` registration happens only if/when a belt is later built as a real
   region (the same point RGV/PNW formally added their sources).
4. **Compare directionally**, using the same GO / CONDITIONAL-GO / mismatch framing as the
   zone-span reconciliation's "clone honesty record" and RGV/PNW's own provenance audits: do the
   deriver's frost-anchored dates and the real T1 calendar's timing and class behavior (does the
   tree fruit actually fruit reliably there, per the T1 source) line up? A genuine divergence --
   especially a chill/fruit-set class mismatch -- is a NEW-REGION signal.

## 5. Ruling framework

Each belt gets exactly one of:

- **GENERIC-OK** -- the zone-only deriver output is honestly close to the real T1 calendar for the
  representative basket. Ruling stands with the citation as evidence; no further action.
- **CONDITIONAL-GO** -- directionally fine with a specific caveat (e.g. one crop class is a bit
  generous/conservative but not misleading) -- recorded, not treated as blocking.
- **NEW-REGION** -- material divergence found. The belt is **not built here**; it's added to the
  roadmap as a new numbered item (its own future spec/plan/build, same as items 3/4 were spun out
  after item 1's reconciliation surfaced the need).

## 6. Sequencing: 5 independent, checkpointed passes

The 5 belts are researched and ruled **one at a time, sequentially**, each ending in a checkpoint
with Trevor before the next begins -- not one combined pass. This lets the method (marquee-city
choice, basket composition, sourcing depth) get adjusted after the first belt if something about
mid-Atlantic's result calls for it, before the same approach is repeated four more times.

## 7. Artifacts (per belt)

- A research note `docs/reviews/notes/2026-07-15/tier2_<belt>_ruling.md` (or the date the belt is
  actually run): marquee anchor + frost dates, the crop basket, deriver output, T1 source(s) with
  URLs, the directional comparison, and the verdict.
- An update to `docs/region_coverage_roadmap.md`'s "Tier-2 rulings pending (item 5 detail)" section
  -- that belt's row moves from an unsourced "first read" to a cited ruling, mirroring how item 1's
  "Clone honesty record" subsection reads.

No `crops_data_final.json` change of any kind -- including `source_catalog`, which lives inside the
canonical file (see §4 step 3) -- and no `LATEST.txt`/`CURRENT_STATE.md`/`STATE_HISTORY.md`
state-trio update, since this arc produces no content release and the state trio is for canonical
content releases only.

## 8. Scope boundaries (explicitly OUT)

- Authoring any NEW-REGION finding -- queued as its own future roadmap item, not built in this arc.
- Any gate or code change (no new gate needed; nothing here is enforced roster-wide).
- Item 2 (plant-app empty-state ZIP cleanup) and item 6 (Puerto Rico, product-scope) -- untouched,
  different owners.
- Re-litigating items 1/3/4 (already shipped and ruled).

## 9. Success criteria

- All 5 belts carry a cited GENERIC-OK / CONDITIONAL-GO / NEW-REGION ruling with real T1 evidence,
  replacing the roadmap's unsourced first reads.
- Any belt ruled NEW-REGION is recorded as a new queued roadmap item, not built.
- Zero canonical bytes changed; zero gate/tooling code changed.
- `docs/region_coverage_roadmap.md` item 5 section reads as a settled record (mirroring item 1's
  "Clone honesty record"), not a to-do list.

## 10. Open items to confirm during authoring

- Exact marquee city per belt (a specific pick within e.g. "mid-Atlantic" -- Raleigh vs. Norfolk vs.
  Richmond) -- settled at research time against where the best T1 source and frost-date data exist.
- Whether mid-South's TN z9 sliver (1 ZIP) or NV's z10 sliver (1 ZIP) need their own note or can
  ride the belt's general verdict -- likely the latter given the scale, confirmed per-belt.
- Which specific crop fills the "annual" and "berry/cool-season" basket slots per belt -- picked at
  research time for whichever has the strongest T1 documentation in that belt.
