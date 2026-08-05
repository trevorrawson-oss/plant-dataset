# USCRN soil-temperature validation (PLA-110) -- design pass + measured evidence

**Session 2026-08-04.** **PROMOTED: `4065e23b` -> `5a52a76c`.** Built in worktree
`~/plant-dataset-pla110`, branch `pla-110-uscrn`. **Uncommitted, awaiting Trevor.**

Five tools, 84 tests, a measured zone table and 228 records. Trevor ruled both open decisions
(§3 and §2 item #4) on 2026-08-04; §7 records what landed and what changed after the ruling.

---

## 1. What the issue asked for, and the three ways its framing was wrong

PLA-110 says "9 of 3,403 `uscrn_validation` slots populated ... complete or re-run that
integration." All three load-bearing numbers were re-verified before any code, per the repo's
re-verify rule. The 9 and the 3,403 are both exactly right as counts. What they mean is not.

**(a) 3,403 is the wrong denominator, by a factor of eight.** The field sits on 3,403 of 6,579
date entries, and two thirds of them cannot be soil-validated even in principle:

| where the slot sits | slots | can a 5cm spring soil crossing validate it? |
|---|---:|---|
| `harvest_start` / `harvest_end` | 1,940 | No. Harvest follows days-to-maturity from planting. |
| `start_indoors` | 326 | No. Indoors, heated house, tray. Not field soil. |
| `plant_out` / `transplant` | 712 | In principle yes, but this repo has no sourced number for it (see §4). |
| **`direct_sow`** | **425** | **Yes. This is the field's real universe.** |

Of the 425, **408** are on crops that are `propagule: seed` and carry `germination_temp_f`; the
only two excluded crops are potato (tuber) and one division-propagated crop. So the honest
denominator is 408, not 3,403, and the pilot's 9 is 2% of the target, not 0.3%.

This is the `citation-arc-repriced-by-decision-unit` shape: a count priced at the wrong unit.

**(b) "Re-run the integration" -- there is nothing to re-run.** Confirmed: no USCRN puller,
validator, or soil-temp integration exists anywhere in `tools/`. This was build-from-scratch.

**(c) The pilot is not a clean template to copy.** The issue says "Copy it rather than
redesigning." One of the 9 pilot records is wrong:

> `bok-choy` / `northern_tier` carries `stored_date: "03-18"`, `uscrn_median_date: "03-29"`,
> `station_count: 14`, `station_year_count: 198`, `anchor_threshold: "soil 40F reached at 5cm"`.
> Every one of those values is byte-identical to the `lettuce-leaf` / `northern_tier` record.
> Bok-choy has no Mar 18 date in any zone (z6 is Mar 22, z7 is Mar 1), and its own germination
> floor is **45F**, not lettuce's 40F.

It is a copied record asserting a validation of a date bok-choy does not store, against a
threshold that is not bok-choy's. The `template-inheritance-fabricates-attributions` shape,
inside our own file. The remaining 8 records are not reproducible either -- their station-year
counts (61 for zone 8) cannot be reconstructed from the archive by any method tried here, though
their `station_count` of 18 for zone 8 matches this pass exactly.

**Recommendation: the 9 pilot records are overwritten, not preserved.** They are unauditable, one
is demonstrably wrong, and the pilot's own note says the numbers "should not be auto-applied."

---

## 2. The four decisions the issue reserved

**#2 Station-to-zone method -- SETTLED, and it needed no external data.** The USDA hardiness zone
*is* the mean annual extreme minimum temperature, binned in 10F steps from -60F. USCRN publishes
`T_DAILY_MIN`. So every station is binned **from its own record** -- no raster, no lat/lon join, no
third-party table. A year only scores if it contains its own winter (300+ valid daily minima and
20+ in each of Dec/Jan/Feb), because a station that lost January reports a falsely warm minimum
and walks a zone or two south.

All 113 stations resolved, 0 dropped. Spot-checked against published placements: Fairhope AL 9a,
Gadsden AL 8a, Batesville AR 7a, Elgin AZ 8a, Tucson AZ 9b. Distribution:

| zone | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| stations | 5 | 12 | 18 | 23 | 17 | 18 | 14 | 6 |

**Coverage gap, stated rather than papered over: zones 11, 12 and 13 have no USCRN station** in
this archive. 103 cells were skipped for that reason and get no record at all.

**#3 Confidence floor -- SETTLED, keep 30 station-years, and never silently omit.** A cell under
the floor is written with `status: flagged_for_review` and a note naming its actual station-year
count. A second failure mode the pilot did not have a concept for is also caught: a threshold the
zone *misses* in more than 25% of watched years is `unreliable`, because its median describes only
the warm tail. Zone 3 and zone 4 at 70F are exactly that (35% and 31% never reached).

**#1 Per-crop thresholds -- PARTLY SETTLED. This is the open question. See §3.**

**#4 Field-addition register -- RECOMMEND NOT ADDING as a hard cert requirement.** Now that #1 and
#3 have real answers, the reason is concrete rather than abstract: the field is meaningful on 408
of 6,579 date entries, and it is meaningful on **zero** entries for all 31 tree, berry and mushroom
crops, none of which are ever seed-sown in the garden. An A39 presence-or-null hard requirement
would oblige every future crop -- including every fruit tree -- to carry a field that can never be
populated for it. That is a certification treadmill bought for nothing. **Recommend instead:** a
soft coverage scan over the direct-sow slice only, in the shape of `soil_temp_floor_scan.py`, with
the same hard-flip condition once the slice is fully populated. **Trevor's call; not actioned.**

---

## 3. THE OPEN QUESTION -- `germination_temp_f` is an optimal band, not a minimum

The threshold has two sources: the arm's own `from: soil_temp_40f` where it declares one (26
arms), and `germination_temp_f[0]` everywhere else. The second is where the problem is.

`docs/climate_thresholds_contract.md` states it plainly: "`germination_temp_f` is a band because
it is an *optimal range*." Checked against the standard extension germination table, the roster's
values behave as a mix -- near-minimum for cool crops, optimal-floor for warm ones:

| crop | `germination_temp_f[0]` | published *minimum* germination |
|---|---:|---:|
| lettuce | 35 | 32-35 -- floor is the minimum |
| radish | 45 | 40-45 -- close |
| carrot | 55 | ~40 -- floor is well above minimum |
| cucumber | 70 | ~60 -- floor is the optimal bottom |
| okra | 70 | ~60 -- floor is the optimal bottom |

The pilot itself shows the gap: lettuce's floor is 35F but the pilot's sourced anchor, from UMN
Extension prose, is **40F**.

**Why it matters.** Using the optimal floor as a hard "soil must reach" gate reads systematically
early, and it drives most of what is currently flagged. The six utah_dixie cucurbit cells flagged
at 70F sit 45 days ahead of the measured crossing; at cucumber's true minimum of 60F the same
zone's median is 03-23 against a stored 03-15, which is fine. Same data, opposite verdict, purely
from which number is called the threshold.

**Three options, with a recommendation:**

1. **Author a `sowing_soil_temp_f` field** -- the real "sow when soil reaches" number, sourced per
   crop. Correct, and a column GS-arc in its own right (~97 crops). Recommended if this is going
   to carry app-facing notification claims, which is PLA-110's stated reason for existing.
2. **Use the optimal floor and label it honestly.** Every record already carries
   `anchor_threshold_basis: "germination_temp_f floor for this crop"`, so nothing is passed off as
   a sourced sowing gate. Cheap, ships today, and the flagged set is a review surface rather than
   a defect list.
3. **Restrict to the 26 declared-anchor arms.** Fully sourced, and far too small to be worth the
   machinery.

**Recommendation: (2) now, (1) as the follow-on arc**, because (2) is already built and its output
is honest about its own provenance, while (1) is the thing that actually justifies a paid-tier
notification claim.

---

## 4. What was built, and two methods that were measured and rejected

`tools/uscrn_ingest.py` (19 tests) parses 1,802 station-years in 4s. `tools/uscrn_zone_table.py`
(12 tests) aggregates to zone x threshold. `tools/uscrn_validate.py` (28 tests) joins to the
roster. Two readings were built, measured on the real roster, and thrown away -- recorded here so
they are not rebuilt:

* **The Phase 1.1 fixed-day bands** (+/-3 aligned, 4-10 drift, >10 misaligned) returned **170 of
  228 cells "misaligned"**, including 16 of the 29 whose arm declares its own soil anchor. A
  zone's own crossing swings 30-90 days between p10 and p90, so a 3-day band is finer than the
  quantity it measures and reports variance as error. The bands were specified for a comparison
  against a single station, not a zone aggregate. **Retained as the reported `offset_band`, since
  the methodology named it, but it is not the verdict.**
* **Comparing the window's OPENING date to the median crossing** returned 67 cells "often too
  cold". A sowing window is a range a gardener picks a day inside, so its opening precedes the
  typical crossing by construction. That is a property of windows, not a defect.

**What survived** compares the sowing **window** against the measured distribution:
`window_too_early` (window closes before even p10 -- follow it and every day is cold soil, the
desert-cucurbit shape), `opens_early` (closes before the median), `brackets_crossing` (healthy),
`opens_late` (soil long ready; a choice, never flagged), `not_soil_limited` (zone is above the
threshold when the year opens).

Result on 228 records: **167 brackets_crossing, 45 not_soil_limited, 12 opens_early, 3 opens_late,
1 window_too_early.** 28 cells carry directional risk. That is a readable review surface.

Measured 50F crossing, the headline evidence -- monotonic across zones, as it must be:

| zone | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| median | 05-11 | 05-09 | 04-27 | 04-15 | 03-12 | 02-02 | 01-06 | 01-01 |
| station-years | 72 | 170 | 257 | 330 | 257 | 261 | 199 | 88 |

---

## 5. Other decisions worth recording

* **Records are keyed to the CELL (crop x zone), not to an arm index.** Measured: arms align
  positionally with resolved window segments only **51%** of the time, so an index-based write
  would attach half its verdicts to the wrong window.
* **Region records carry `by_zone`.** A region spanning zones 3-7 has crossing dates ~90 days
  apart; a single flat record cannot describe it, which is structurally why the pilot's region
  records went wrong. Every scalar comes from one `representative_zone` so the record cannot
  contradict its own arithmetic.
* **A missing daily reading breaks the 5-day sustain run** rather than being interpolated, and an
  unwatched year is never counted as "the soil never got there" -- the
  `waf-block-pages-cached-as-absence` shape.
* **Feb 29 folds to Feb 28.** The dataset stores month-day strings with no year; an emitted
  `02-29` is a date that does not exist three years in four.
* **Warm-zone saturation is not a spring event.** Zone 8 is already at/above 40F on Jan 1 in 67%
  of years, zone 9 in 79%. Those carry `year_round: true` and `status: not_soil_limited`.

---

## 6. Trevor's rulings, 2026-08-04

**§3 threshold basis: ship on the optimal floor.** Option (2). `anchor_threshold_basis` names the
provenance on every record, and a guard pins it there so the ruling cannot erode. Explicitly not
the finish line: **PLA-118** carries the real germination-minimum field, and **no app-facing
USCRN-validation claim is made until that lands**, not on this one.

**§2 item #4 register row: not added.** A soft coverage scan replaces it, built as
`tools/uscrn_coverage_scan.py` in the shape of `soil_temp_floor_scan.py`. It reports **0
unexplained gaps**: 532 cell-zones covered, 89 fall-only, 59 in zones 11-13 where USCRN has no
station. Every uncovered cell carries a named reason or the scan exits 1.

---

## 7. What landed, and the three things that changed after the ruling

**PROMOTED `4065e23b` -> `5a52a76c`.** Two writes: the top-level `uscrn_soil_temp` table and 228
`uscrn_validation` records. Nothing else moved, and that is proven twice over -- by a structural
before/after comparison with the field blanked, and by **14 standalone roster gates coming out
byte-identical** to the pre-promote base.

**(a) A correction to §1, made by re-reading the data rather than the inference.** This doc first
said bok-choy's 40F threshold was lettuce's number leaking across. It is not. The anchor is
declared on bok-choy's own planting arm and sourced to bok-choy's own MSU Extension prose ("bok
choy ... germinates once soil reaches about 40 degrees F"), so it legitimately overrides the 45F
optimal-band floor. What was copied was the record PAYLOAD, the date and the station counts, not
the threshold. A guard written to demand 45F there was asserting an inference against the
evidence; it was replaced by one that re-derives every record's `stored_date` from its own cell,
which catches the real defect and generalizes to any mis-targeted write.

**(b) A29 caught a real mistake mid-pass.** The records first used the pilot's field name
`zone_coverage_note_seasoned`. The `_seasoned` suffix is a **contract**, not a label:
`register_fill_gate` requires every `_seasoned`/`_beginner` field to be authored prose with a
register twin, and it **bounced 34 of 121 certified crops** until the field was renamed to
`zone_coverage_note`. These are machine-generated methodology annotations on a field that renders
nowhere, not the expert half of a dual-register consumer pair.

**(c) One guard was built and removed, and one guard order was wrong.** A "no two crops share an
identical record" check looked like the right fingerprint for the pilot's copy defect and is not:
six cucurbits legitimately produce byte-identical utah_dixie records (same 70F floor, same
`Mar 15 - Mar 29` window, same zone). The first version compared whole germination *bands* and
false-positived on a 90-vs-95 upper bound that has no bearing on the threshold; corrected to
compare floors, it could not fail at all, because two earlier guards already covered it. Removed
rather than shipped. Separately the slot-count guard sat *behind* the structural comparison and
was therefore unreachable -- its mutation test passed only because an earlier guard fired, the
`guard-tests-pass-because-an-earlier-check-fires` shape, hit again. Reordered.

**Gauntlet:** `gate_all` 121/121, `whole_crop_gate` PASS, `release_verify` clean (its 4 review
notes are pre-existing Step 5/5.5 items), 14 standalone gates byte-identical, 118/118 test files
green on the direct runner and under pytest (the single pytest abort,
`test_build_berry_pilot_patch.py`, is a pre-existing documented SKIP for session-scoped staging
inputs and is identical on the base). Compact preserved, no trailing newline.

**State trio done:** CURRENT_STATE.md amended surgically (release entry prepended, canonical
pointer advanced, locked-decisions block and SESSION PROTOCOL header verified intact),
STATE_HISTORY.md appended most-recent-first, LATEST.txt bumped.

**Uncommitted, awaiting Trevor.** On commit, register `5a52a76c` -> `<commit>` in
`promote_fixture.COMMIT_FOR`. No plant-astro bump.
