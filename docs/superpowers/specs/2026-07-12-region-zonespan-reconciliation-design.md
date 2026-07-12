# Region zone-span reconciliation + coverage roadmap -- design spec

**Date:** 2026-07-12
**Status:** DRAFT (pending Trevor review)
**Source report:** `docs/2026-07-12-region-zonespan-gaps.md` (plant-app session sweep)
**Sequencing:** ships BEFORE the leek variety pilot (leek's hardiness engine reads region
zones and leek is one of the 117 crops this touches; the leek plan rebases on top).

## 1. Product goal

A user types their ZIP and gets their proper, up-to-date zone AND region with correct
planting information. That runs through a four-link chain:

1. **ZIP -> zone** -- plant-app `zip-zones.json` (already on the 2023 USDA map)
2. **zone + state -> region** -- region `zone_span`s (THIS REPO; where 300+ ZIPs fall through)
3. **region + zone -> dates** -- per-crop `resolved_by_zone` rows (THIS REPO)
4. **no region -> generic zone dates** -- the fallback; fine for some states, misleading for others

This arc fixes link 2 (and the link-3 rows it requires) for every gap that is a stale
zone LABEL, and produces a roadmap covering the whole chain so the remaining gaps are
deliberate decisions, not accidents.

## 2. Diagnosis: stale labels, not wrong data

The spans encode 2012-era zone labels of the cities the regions were authored FOR.
The 2023 USDA map relabeled those cities; the climates and the calendars did not change.

- `low_desert_az` IS the Phoenix calendar (UA extension az2078, Maricopa az1005), but
  Phoenix relabeled 9b -> 10a, so span `[9]` no longer catches Phoenix (71 ZIPs).
- `hawaii_tropical` was authored for Honolulu (CTAHR, `ctahr_year_round_resolution`),
  but most of Honolulu is z12 under the ZIP table vs span `[11]` (119 + 2 + 1 ZIPs).
- Warmest coastal LA/SD pockets read z11 vs `ca_south_coast`/`ca_desert` span `[9,10]` (28 ZIPs).
- The New Orleans fringe reads z10 vs `se_gulf` span `[8,9]` (6 ZIPs).
- **The one real exception:** Rio Grande Valley TX z10 (95 ZIPs, McAllen/Brownsville) is a
  genuinely different climate (frost-free winter-vegetable region); se_gulf z8-9 Gulf-coast
  dates do not honestly stretch there. It needs its own authored region (roadmap item 3).

## 3. Data-model reality (verified 2026-07-12 against canonical e45bcf3c)

- Regions live PER-CROP: 117 of 125 crops carry a `regions` dict (10 region ids);
  106 are populated per region, 11 are empty shells (`zone_span` empty, no calendars).
- `zone_span` is uniform in value across crops per region; a widen touches ~106 copies.
- `resolved_by_zone` keys exactly match the span. Widening a span REQUIRES a row for the
  new zone in every populated crop, or span/key parity breaks.
- The per-zone date windows were authored at splice time (no per-zone resolver tool exists);
  only the 12-month `calendar[]` is computed (`tools/annual_calendar.py`).
- `zone_frost_data` covers zones 3-11 (+ half zones). No z12/z13 entries. Hawaii's
  `ctahr_year_round_resolution` does not read frost data (asserted at implementation, not assumed).
- NOTHING in `tools/` reads `zone_span` (grep across all tools, 2026-07-12) -- no gate
  guards it and no tool consumes it; the parity gate is new work.
- The app's `regions.json` is generated downstream of this dataset (nothing in this repo
  produces it); per the source report, span widens flow through as data with no app code change.

## 4. Deliverable 1: the widen (canonical dataset change)

| Region | Span change | New-zone row source (donor) | ZIPs fixed |
|---|---|---|---|
| `low_desert_az` | [9] -> [9,10] | clone z9 | 71 (Phoenix metro) |
| `hawaii_tropical` | [11] -> [10,11,12,13] | clone z11 (year-round) | 122 (Honolulu +) |
| `ca_south_coast` | [9,10] -> [9,10,11] | clone z10 | 28 (coastal LA/SD, |
| `ca_desert` | [9,10] -> [9,10,11] | clone z10 | app picks via ZIP3) |
| `se_gulf` | [8,9] -> [8,9,10] | clone z9 | 6 (New Orleans fringe) |

Total: ~227 ZIPs directly, plus the 95 RGV ZIPs on the interim ruling below (~320 total).

**Clone honesty.** Clone-adjacent-zone is honest here BECAUSE the calendars were already
written for the relabeled cities (provenance audit per region confirms; done for
low_desert_az and se_gulf, repeated for HI/CA before the transform runs). Each cloned row
is marked: a provenance note stating the row is 2023-map label reconciliation cloned from
the donor zone, so we never pretend z12 Honolulu was authored separately.

**Mechanics.** A new deterministic builder `tools/build_zonespan_widen_patch.py`
(existing patch-builder pattern): per region, deep-copy the donor zone's `resolved_by_zone`
row to the new zone key(s), update `zone_span` in every populated crop. Empty-span shells
stay byte-identical. Everything outside the five regions' `zone_span` + `resolved_by_zone`
is byte-identical. Canonical stays compact (protocol).

**RGV interim ruling (Trevor-approved 2026-07-12).** Widening se_gulf to z10 means the 95
TX RGV z10 ZIPs auto-match se_gulf (TX is in the app's se_gulf state mapping). Ships as an
EXPLICITLY INTERIM answer: Gulf-coast winter-garden dates are directionally right for RGV
and better than a bare zone label, and se_gulf's source set already includes tamu_agrilife.
The real fix is roadmap item 3; the interim is recorded in the roadmap doc, not hidden.

## 5. Deliverable 2: the roadmap doc

`docs/region_coverage_roadmap.md` -- one ordered program covering the whole chain, with an
**owner column** (dataset session / plant-app session / product call). Every gap from the
sweep gets one of four rulings: *stale-label widen (fixed by this arc)* / *needs a new
authored region (queued, prioritized)* / *generic zone dates are the deliberate answer
(ruled fine, with rationale)* / *different owner (first-class entry, not a footnote)*.

| # | Item | Owner | Notes |
|---|---|---|---|
| 1 | Zone-span widen (this arc) | dataset | ~320 ZIPs fixed |
| 2 | App-side cleanup | plant-app | ~285 empty-state ZIP rows (load-bearing: those ZIPs stay broken even with perfect spans); verify regions.json sync path; TX z10 ZIP3 fencing decision |
| 3 | RGV / subtropical TX region | dataset | 95 ZIPs off the interim; TAMU AgriLife RGV calendars are strong T1 |
| 4 | Maritime PNW region | dataset | ~750 ZIPs (WA/OR z8-9); generic frost-anchored dates most misleading here (cool summers); WSU/OSU extension = strong T1 |
| 5 | Judged later: mid-Atlantic z8 belt (NC/VA/MD/DC/DE/NJ/PA, ~1,400 ZIPs), mid-South (AR/OK/TN/MO), NV/UT/AK | dataset | each gets an explicit ruling; "generic is fine" is a legitimate outcome where honest |
| 6 | Puerto Rico (z11-13, ~175 ZIPs) | product call (Trevor) | market-scope question before a data question; also needs z12/13 support end to end |

Items 3+ are their own future arcs (spec -> plan -> build), NOT started in this one.

## 6. Verification (TDD, per session protocol)

1. **New gate FIRST, RED before GREEN.** Next free A-number (A45 expected):
   span <-> `resolved_by_zone` key parity + cross-crop `zone_span` uniformity per region
   (empty-span shells exempt). Adversarially proven on a SCRATCH copy -- inject (a) a
   span/key mismatch, (b) a divergent span in one crop -- confirm both bounce before the
   transform runs. Wired into `gate_all.py` roster-wide.
2. **Biology/provenance audit per region (not per crop).** The clone claim is
   "this region's calendars were already written for the relabeled city." Verify via
   `plantings_provenance` + source audit for HI and both CA regions (AZ and se_gulf done);
   spot-check that no donor row encodes anything zone-label-dependent; assert Hawaii's
   resolution path never reads `zone_frost_data` (z12/13 have no entries).
3. **Acceptance test = the sweep.** Re-run the source report's repro (zip-zones zones >= 8
   vs widened spans + state mapping): the Tier-1 gap table goes to zero except the ruled
   items (RGV rides se_gulf interim; Tier-2 states unchanged by design).
4. **Full release ceremony:** `whole_crop_gate` 18/18, `gate_all.py` roster-wide,
   `release_verify.py`, per-batch source-truth sample, state trio
   (CURRENT_STATE.md surgical update per drift memory, STATE_HISTORY.md, LATEST.txt).

## 7. Non-goals

- No new region is authored in this arc (RGV, PNW, etc. are queued arcs).
- No Tier-2 state gets a region mapping; no ruling is silently implied -- the roadmap
  doc records each explicitly.
- No app-side edits (zip-zones empty-state rows, regions.json sync, ZIP3 hints) from this
  session -- two-session collision rule; they are roadmap item 2 with plant-app as owner.
- No `zone_frost_data` z12/13 backfill (only needed if PR gets green-lit, item 6).
- No plant-astro submodule bump from this session (owned by the astro session).

## 8. Risks / open items

- **regions.json sync path unverified.** If the app's `zoneSpan` turns out NOT to derive
  from this dataset, the widen still stands (link-3 truth) but link 2 needs an app-side
  mirror edit -- roadmap item 2 verifies this before the app consumes anything.
- **Donor-row edge cases.** A crop whose donor row is degenerate (e.g. `suitable`-adjacent
  advisories, second-planting bands) must clone cleanly; the builder diff-audits a sample
  and the source-truth sample covers it.
- **ZIP counts are point-in-time** (2026-07-12 sweep); the acceptance re-run recounts.

## 9. Acceptance criteria

1. New parity gate live, adversarially RED-proven, green roster-wide.
2. Canonical updated: five regions' spans widened, cloned rows marked, footprint exactly
   the five regions' `zone_span` + new `resolved_by_zone` keys across populated crops;
   all else byte-identical; compact format preserved.
3. Sweep re-run: zero unruled Tier-1 gaps.
4. `docs/region_coverage_roadmap.md` committed with all six items + owner column + the
   four-way ruling for every gap in the source report.
5. Full release ceremony green; state trio updated; commit awaits Trevor's push confirm.
