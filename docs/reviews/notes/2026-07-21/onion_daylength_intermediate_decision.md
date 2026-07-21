# Onion + shallot day-length correction (mid_south / mid_atlantic z8, mid_south z7) -- decision + sources

**Date:** 2026-07-21. **Scope:** onion + shallot, regions `mid_south` and `mid_atlantic`.
**Change:** `recommended_day_length_type` `long_day` -> `intermediate_day` at the latitudes where
long-day onions do not bulb, plus a spring planting-window trim (April tail dropped). **Canonical
base:** `931c1653`. **Patch:** `tools/batches/onion_daylength_intermediate.json` (builder
`tools/build_onion_daylength_patch.py`). No new field, no new gate.

## Why (the finding)
The mid-South and mid-Atlantic region builds shipped `long_day` for onion/shallot across their whole
z7-z8 span. That is wrong for the zone-8 cores, which sit at ~34-36°N (Little Rock 34.7°N, Pine
Bluff 34.2°N; Wilmington NC 34.2°N, New Bern 35.1°N). Long-day onions need 14-16 hr days to bulb;
at ~34°N the longest summer day only reaches ~14 hr, so a long-day onion triggers too late and too
briefly to size up. The operative extension line is **36°N** (Univ. of Maryland, Texas A&M):
short-day below it, long-day above. Every T1 source rules out long-day for this belt; two say so
outright ("Long-day onions are not recommended for our area," NC Onslow County; "Long day onions
cannot be successfully grown in the South," Clemson).

## What each authority recommends (T1)
| State / source | Day-length rec | Planting window | Tier |
|---|---|---|---|
| Arkansas -- UAEX FSA6014 | short-day statewide; intermediate adapted to the **northern half**; long-day not listed | spring transplant **Feb-April** | T1 |
| Oklahoma -- OSU (HLA-6004 + Candy production) | **intermediate** ("Candy") | **Feb 15 - Mar 10** | T1 |
| Tennessee -- UT D127 | **intermediate** for dry bulbs; "long-day types may not produce bulbs well in more southern locations" | late-Feb **through March** | T1 |
| Missouri -- MU G6201 | defaults **long-day** (northernmost; z8 = thin Bootheel sliver ~36.5°N; list still includes intermediate Candy) | spring | T1 |
| NC coastal -- NC State "Bulb Onions" + Onslow/Pender Co. | **short-day**; long-day "not recommended" | fall direct-seed Sep-Oct **or** late-winter transplant Feb-Mar | T1 |
| Virginia -- VCE 426-411 | **day-neutral / intermediate** | spring; VCE 426-331 table **Feb 20 - Apr 20** (z8) | T1 |
| framework -- UMD, TAMU, UGA, Nebraska, Iowa State | 36°N line; triggers SD 10-12h / ID 12-14h / LD 14-16h | -- | T1 |

**Convergence variety:** intermediate-day **'Candy'** is recommended by Arkansas (as SD/ID,
"adaptable to a wide range of latitudes"), Oklahoma (flagship), Tennessee, Missouri (list), and
Maryland -- the single best belt-wide pick.

**Shallot:** same species (*Allium cepa* Aggregatum group), same photoperiod response. There is no
separate T1 shallot latitude map (OSU's shallot page is written for the long-day Pacific NW), so
shallot honestly **follows onion** by species analogy; the cells say so.

## The decision: Path A (flip + tighten window)
- **Type:** `intermediate_day` is the single value best supported across the belt (the Candy
  convergence), keeps us internally consistent (`ca_interior` / `warm_arid` z8 are already
  intermediate), and is honest to note short-day types also succeed in the warm south.
- **Zones:** flip mid_south z7 **and** z8 (both ~34-37°N, below solid long-day country: TN + N.
  Arkansas both recommend intermediate); flip mid_atlantic z8 only. **mid_atlantic z7 stays
  `long_day`** -- its Piedmont runs to ~40°N (PA/NJ/MD), genuine long-day territory.

## The gate coupling and the source split (why the window was trimmed)
The A9 photoperiod gate (`photoperiod_gate.py`, whole_crop_gate A9) enforces a WINDOW-FIT rule: an
`intermediate_day` cell's `plant_out` must avoid April onward, because intermediate-day onions are
set early to build leaf area before their (shorter, earlier) day-length trigger. All six cells
planted into **mid-to-late April** ("Feb 15 - Apr 15" etc.), so flipping the label alone would have
left the gate RED.

**The sources split on the April tail:**
- END BY MID-MARCH (support the trim): **OSU** Feb 15-Mar 10; **Tennessee** through March; **NC
  coastal** Feb 10-Mar 10.
- INTO APRIL: **Arkansas FSA6014** "February through April"; **VCE** Feb 20-Apr 20 -- but both are
  **generic all-type windows**, not intermediate-specific.

**We went Path A** (trim the window to end late March) over refining the gate, because: (1) it keeps
the validated gate armor untouched; (2) it is the more accurate window for intermediate-day
varieties specifically (which want to go in early -- the April tail is really a long-day-onion
pattern); (3) 3 of the belt's 5 states already end by mid-March; (4) harvest is day-length-anchored
(May-June) and does **not** move. Trimmed windows: mid_south z8 "Feb 15 - Mar 25", z7 "Feb 24 - Mar
31"; mid_atlantic z8 "Feb 20 - Mar 31". April flips `plant` -> `growing` in the calendar strip.

The region-level `plantings[]` offset/window is left unchanged (it is the general provenance and,
for mid_atlantic, is shared with the still-long_day z7); the resolved cells are authoritative.

## What changed (footprint)
56 patches: 6 resolved cells (recommended_day_length_type, both day_length notes, plant_out,
last_plant_date, calendar[3], zone_notes) + 4 region cells (region_notes_beginner/seasoned +
`sources` gain the onion day-length authority) + **2 new T1 source_catalog entries**
(`uada_ext_fsa6014` UAEX Onions; `ncsu_ext_bulb_onions` NC State Bulb Onions). Only onion + shallot
changed; only their mid_south / mid_atlantic cells; 27 changed leaves per crop, all intended; 0
other crops; compact preserved (0 escaped-unicode).

## Gates (on the scratch)
`gate_all` 119/119 PASS; A9 photoperiod onion+shallot 0; calendar_coherence 0; prose_window_sweep 0;
release_verify B-H clean (the 1 concern = the documented single-crop-pilot collateral false positive,
run expected only onion but this is a deliberate 2-crop change). Em-dash guard clean.

## Source URLs (T1)
- UMD onions & day length (36°N line): https://marylandgrows.umd.edu/2018/04/06/onions-and-day-length/
- Texas A&M / Aggie Hort Growing Onions: https://aggie-hort.tamu.edu/archives/parsons/publications/onions/ONIONGRO.html
- UAEX FSA6014 Onions: https://www.uaex.uada.edu/publications/PDF/FSA-6014.pdf
- OSU HLA-6004 (OK planting dates) + Candy production fact sheet (extension.okstate.edu)
- UT D127 Onions/Leeks/Shallots: https://uthort.tennessee.edu/wp-content/uploads/sites/228/2023/11/D127.pdf
- MU G6201 vegetable planting calendar (extension.missouri.edu)
- NC State Bulb Onions: https://content.ces.ncsu.edu/bulb-onions
- NC Onslow County growing onions: https://onslow.ces.ncsu.edu/news/growing-onions/
- VCE 426-411 Onions, Garlic, Shallots: https://www.pubs.ext.vt.edu/426/426-411/426-411.html
- Clemson HGIC onion/leek/shallot/garlic: https://hgic.clemson.edu/factsheet/onion-leek-shallot-garlic/
- Bulbing-hour corroboration: UGA B1198, Nebraska (Lancaster Co.), Iowa State Extension

## Open follow-on (not this change)
Two pre-existing shallot per-variety `day_length_type` tensions remain uncorroborated (Southern
multiplier `short_day`; the set varieties `intermediate_day`) -- see memory `shallot-variety-dtm-held`.
Out of scope here (this change is the region-level recommendation, not per-variety typing).
