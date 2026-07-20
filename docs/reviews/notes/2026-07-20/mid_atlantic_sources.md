# Mid-Atlantic region -- T1 sourcing table (Task 3)

**Arc:** `docs/superpowers/plans/2026-07-20-mid-atlantic-region.md`, Task 3.
**Region:** `mid_atlantic`, `zone_span ["7","8"]`, frost-anchored.
**Sources (both T1, both already in `source_catalog`):** `vce_426_331` (Virginia Cooperative
Extension Pub. 426-331, "Virginia's Home Garden Vegetable Planting Guide"), `ncsu_ext` (NC State
Extension). All fetched/verified 2026-07-20 in the controller env.

---

## 1. Frost anchors (`resolved_from`) -- the deriver inputs

From **VCE 426-331 Table 1** (per-zone frost dates, the SAME document the planting tables are built
on -- internally consistent) cross-checked with **NC State Extension** frost normals.

VCE Table 1 verbatim: z7a "April 15-25 / Oct 15-25", z7b "April 5-15 / Oct 25-Nov 5",
z8a "April 1-15 / Nov 1-15", z8b "March 15-April 1 / Nov 15-25".

**Anchors adopted (representative of the belt's center of mass):**

| Zone | last_frost | first_frost | Basis |
|---|---|---|---|
| **7** | **Apr 15** | **Oct 25** | VCE Table 1 z7a/z7b midpoint. Belt z7 = northern VA / central MD / most NJ / eastern PA / western NC Piedmont. |
| **8** | **Apr 8** | **Oct 30** | Raleigh/Wake Co. marquee (NC State Extension, the ruling's z8 anchor). Sits inside VCE z8a's Apr 1-15 range; VCE z8a first frost (Nov 1-15) is ~1 week later, so this anchor is mildly conservative on the fall end. |

**Modeling note (important):** the belt's z7 must NOT be anchored to NC Piedmont z7 stations
(Greensboro last frost Apr 3, Winston-Salem Apr 1, Charlotte Apr 1) -- those run *warmer* than
Raleigh z8 because they sit at a southern latitude, which would invert the z7-vs-z8 gradient. The
belt's z7 is dominated by northern VA / MD / NJ / PA, genuinely cooler than NC's Piedmont; VCE
Table 1's Virginia z7 dates (last frost mid-to-late April) are the representative anchor. Adopted
anchors give z7 a ~12-day-shorter frost-free season than z8, matching the VCE z7 planting tables'
2-3 week later windows.

---

## 2. VCE 426-331 planting windows -- z8 (Coastal Plain, DC, VA Tidewater)

Full Table 4 (z8a shown; z8b generally 5-10 days earlier spring / later fall). Superscript-3 crops
are transplant dates. **"Fall" column = the documented second (fall) planting cycle the naive
single-cycle deriver omits -- the reason this region exists.**

| VCE crop | Spring (z8a) | Fall (z8a) |
|---|---|---|
| Asparagus | Feb 15-Apr 1 | -- |
| Beans, lima | Apr 20-Jul 1 | Jul 1-Aug 20 |
| Beans, pole | Apr 10-Jul 1 | Jul 1-Jul 20 |
| Beans, snap | Apr 1-Jul 1 | Jul 1-Aug 20 |
| Beets | Feb 20-Apr 10 | Sep 1-Oct 1 |
| Broccoli (T) | Mar 1-Apr 10 | Aug 20-Sep 20 |
| Brussels sprouts (T) | -- | Aug 20-Sep 1 |
| Cabbage (T) | Mar 1-Apr 10 | Aug 20-Sep 10 |
| Cabbage, Chinese | Mar 1-Apr 10 | Aug 20-Sep 20 |
| Carrots | Feb 20-Apr 1 | Aug 1-Sep 10 |
| Cauliflower (T) | Mar 1-Mar 20 | Aug 20-Sep 10 |
| Chard, Swiss | Feb 20-Apr 10 | Aug 20-Oct 1 |
| Collards, kale | Feb 10-Apr 1 | Aug 20-Oct 1 |
| Corn, sweet | Apr 1-Aug 10 | -- |
| Cucumbers | Apr 10-Jul 1 | Jul 1-Aug 10 |
| Eggplant (T) | Apr 10-Aug 10 | -- |
| Garlic | -- | Oct 15-Nov 15 |
| Kohlrabi | Feb 20-Apr 1 | Sep 1-Oct 1 |
| Leeks | Mar 1-Apr 1 | -- |
| Lettuce, baby salad | Mar 10-May 1 | Sep 1-Oct 20 |
| Lettuce, head | Mar 1-Apr 20 | Sep 1-Oct 10 |
| Muskmelon | Apr 10-Jul 20 | -- |
| Mustard | Feb 10-Apr 1 | Sep 1-Oct 20 |
| Okra | Apr 15-Aug 10 | -- |
| Onion (bulbing) | Feb 20-Apr 20 | -- |
| Peas, garden | Feb 20-Apr 1 | -- |
| Peas, southern | Apr 20-Aug 20 | -- |
| Peppers (T) | Apr 10-Aug 10 | -- |
| Potatoes | Feb 20-Apr 10 | -- |
| Pumpkin | Apr 10-Jul 20 | -- |
| Radish | Feb 10-Apr 10 | Sep 10-Oct 20 |
| Rutabaga | -- | Aug 20-Sep 10 |
| Spinach | Feb 10-Mar 20 | Sep 20-Nov 1 |
| Squash, summer | Apr 10-Jul 1 | Jul 1-Sep 10 |
| Squash, winter | Apr 10-Aug 10 | -- |
| Sweet potato | Apr 20-Jul 20 | -- |
| Tomatoes (T) | Apr 10-Jul 1 | Jul 1-Aug 10 |
| Turnips | Feb 20-Apr 1 | Sep 1-Oct 1 |
| Watermelon | Apr 10-Aug 1 | -- |

## 3. VCE 426-331 planting windows -- z7 (Piedmont, MD, NJ, eastern PA) -- z7a shown

| VCE crop | Spring (z7a) | Fall (z7a) |
|---|---|---|
| Asparagus | Mar 20-Apr 20 | -- |
| Beans, lima | May 1-Jun 20 | Jun 20-Jul 20 |
| Beans, pole | Apr 20-Jun 20 | Jun 20-Jul 10 |
| Beans, snap | Apr 20-Jun 10 | Jun 10-Aug 1 |
| Beets | Mar 10-May 1 | Aug 10-Sep 10 |
| Broccoli (T) | Mar 20-May 1 | Aug 1-Sep 1 |
| Brussels sprouts (T) | -- | Aug 1-Aug 10 |
| Cabbage (T) | Mar 20-May 1 | Aug 1-Sep 1 |
| Cabbage, Chinese | Mar 20-May 1 | Aug 1-Sep 1 |
| Carrots | Mar 10-Apr 20 | Jul 10-Aug 20 |
| Cauliflower (T) | Mar 10-Apr 10 | Aug 1-Aug 20 |
| Chard, Swiss | Mar 10-May 1 | Aug 1-Sep 10 |
| Collards, kale | Mar 1-Apr 20 | Aug 1-Sep 10 |
| Corn, sweet | Apr 10-Jul 20 | -- |
| Cucumbers | Apr 20-Jun 20 | Jun 20-Jul 20 |
| Eggplant (T) | Apr 20-Jul 20 | -- |
| Garlic | -- | Oct 1-Oct 30 |
| Kohlrabi | Mar 10-Apr 20 | Aug 10-Sep 10 |
| Leeks (T) | Mar 20-Apr 20 | -- |
| Lettuce, baby salad | Mar 20-May 10 | Aug 20-Oct 1 |
| Lettuce, head (T) | Mar 20-May 10 | Aug 10-Sep 20 |
| Muskmelon | Apr 20-Jul 1 | -- |
| Mustard | Mar 1-Apr 20 | Aug 10-Oct 1 |
| Okra | May 1-Jul 20 | -- |
| Onion (bulbing) | Mar 1-May 1 | -- |
| Peas, garden | Mar 1-Apr 1 | -- |
| Peas, southern | May 10-Aug 1 | -- |
| Peppers (T) | Apr 20-Jul 20 | -- |
| Potatoes | Mar 10-May 20 | -- |
| Pumpkin | May 1-Jul 1 | -- |
| Radish | Mar 1-May 1 | Aug 20-Oct 1 |
| Rutabaga | -- | Aug 1-Aug 20 |
| Spinach | Mar 1-Apr 10 | Sep 1-Oct 10 |
| Squash, summer | Apr 20-Jun 20 | Jun 20-Aug 20 |
| Squash, winter | Apr 20-Jul 10 | -- |
| Sweet potato | May 1-Jul 10 | -- |
| Tomatoes (T) | Apr 20-Jun 20 | Jun 20-Aug 1 |
| Turnips (T) | Mar 10-May 1 | Aug 10-Sep 20 |
| Watermelon | May 1-Jul 10 | -- |

## 4. The fall-cycle crop map (drives Task 4's warm/cool split + which crops get `second_planting`)

**Crops with a DOCUMENTED fall window (get a `second_planting` cycle where our roster carries the crop):**
beans (lima/pole/snap), beets, broccoli, brussels sprouts, cabbage, chinese cabbage, carrots,
cauliflower, chard, collards, kale, cucumbers, garlic, kohlrabi, lettuce (leaf/head), mustard,
radish, rutabaga, spinach, **summer squash**, **tomatoes**, turnips.

**Warm-season crops WITH a real fall cycle (the headline finding -- these are what the naive
single-cycle deriver was omitting):** tomatoes (fall Jul 1-Aug 10 z8 / Jun 20-Aug 1 z7), cucumbers,
summer squash, snap/pole/lima beans.

**Warm-season crops with NO fall cycle (VCE "not recommended" fall) -- author spring-only, honestly:**
peppers, eggplant, okra, sweet corn, muskmelon, watermelon, winter squash, pumpkin, sweet potato,
southern peas. (Their long DTM does not finish a fall planting before frost in this belt.)

**Cool-season crops:** the fall column IS their strong season here; author the long spring + fall
shoulders. No `heat_pause`.

## 5. Chill (trees) -- NC State Extension

- **Statewide accumulation, verbatim:** "Typically, throughout North Carolina, gardens receive in
  excess of 1,000 chilling hours annually, so insufficient chilling rarely occurs."
- **Variety recommendation, verbatim:** "plant varieties with a chilling requirement of 750 hours or
  greater... varieties with chilling requirements of less than 750 hours suffer frequent crop losses."
  The belt's real risk is **premature bloom in warm winter spells (too little chill), then a killing
  frost** -- NOT chill deficit. This nuance goes in apple's `suitability_note_seasoned`.
- **Consequence for A3:** the delivered band (below) clears every canonical apple variety (max 900,
  McIntosh) with margin -> all 14 chill-gated trees resolve `fruits_reliably` on real evidence.

**Tree harvest windows (NC State Extension), verbatim harvest months:** apple Aug-Nov, peach Jun-Aug,
pear (European) Aug-Oct, plum Jun-Aug, fig Jun-Aug, persimmon Sep-Nov. (Pawpaw is NATIVE to this
belt -- a genuine strength; source its Aug-Oct ripening in Task 5.)

### Chill band adopted (`region_chill_delivered.mid_atlantic`) -- FLAGGED for Trevor at check-in

| Zone | band | reasoning |
|---|---|---|
| 7 | **[1100, 1500]** | cooler Piedmont/mid-Atlantic winters bank proportionally more |
| 8 | **[1000, 1350]** | NC State ">1,000" statewide; Coastal Plain is the warm edge |

Both clear the 900 apple max, so all trees fruit. **This is the one interpolated number in the arc:**
NC State gives a single statewide ">1,000" figure, not a per-zone measurement. The band reads higher
than some existing z8 neighbors (`se_gulf` z8 [650,1000], `ca_interior` z8 [500,1100]) because NC's
z8 winters genuinely deliver more chill than the Gulf coast or CA Central Valley -- but it is a
judgment call on a user-displayed number, so surface it at the check-in and let Trevor decide whether
to keep the ">1,000"-anchored band or moderate it toward the neighbors for display comparability.

## 6. Berries -- NC State blueberry variety steer (`recommended_type`)

NC State "Growing Blueberries in the Home Garden," by region (verbatim quotes):
- **Coastal Plain (z8, high-organic soils):** highbush (Duke, Jersey) + southern highbush (O'Neal,
  New Hanover, Legacy). "Highbush varieties begin ripening in mid-May in the southeastern Coastal Plain."
- **Piedmont / Foothills / drier upland (z7-8):** rabbiteye (Climax, Premier, Powderblue, Tifblue,
  Centurion) + southern highbush. "rabbiteye blueberries are the best choice for most soils below
  2,500 ft elevation in NC."
- Use `recommended_type` = `rabbiteye` for the belt's dominant upland z7-8 with a
  highbush/southern-highbush note for the Coastal Plain, per the existing blueberry `northern_tier`
  `recommended_type` idiom. Duke/Jersey/Premier are already on the canonical variety list.

## 7. Coverage gaps -- crops NOT in VCE's vegetable table (author conservatively, flag)

The VCE table covers vegetables. Our 82-crop roster also includes **culinary herbs** (basil,
cilantro, dill, parsley, etc.) and a few crops without a VCE row. These get authored from NC State
herb/crop guidance where it exists, or a conservative frost-anchored spring window mirroring the
crop's existing `northern_tier` z7 cell, flagged in `notes`, never invented. Enumerate the exact
gap list against the live roster at the start of Task 4.

**T1-or-it-doesn't-ship holds:** where no VCE/NC State window exists for a crop, author a conservative
cell and flag it; do not fabricate a fall cycle a source does not document.

## 8. FALL-CYCLE CALENDAR PROCEDURE -- a plan correction (found in Task 3, blocks Task 4)

**The plan's Task 4 Step 2 is wrong as written.** It says "derive the `calendar[]` via
`annual_calendar.py`; the deriver picks up `second_planting`." It does NOT. Verified empirically:
`derive_annual_calendar` reads only the TOP-LEVEL `plant_out`/`harvest`/`start_indoors`; it never
reads `second_planting.*`. And a roster-wide check confirms **all 272 existing `second_planting`
cells have a stored `calendar[]` that does NOT re-derive from their (split) storage form** -- the
two-cycle calendars were built from COMBINED windows, then the windows were split into primary +
`second_planting` by the 2026-07-09 demux migration, which preserved the pre-built calendar.

**A43 forbids the shortcut of just storing comma windows:** a cell carrying `second_planting` must be
single-span in the top-level `plant_out`/`harvest`/`start_indoors`, with the fall cycle nested in
`second_planting` (and the top-level `harvest_end`/`last_plant_date` must sit inside the FIRST/spring
span -- the dedup invariant).

**Correct authoring procedure for each fall-cycle crop (Task 4):**
1. Author the COMBINED two-cycle windows in a scratch cell: `plant_out` = `"<spring span>, <fall
   span>"`, `harvest` = `"<spring span>, <fall span>"`, `start_indoors` = spring indoor span (the
   deriver's `parse_months` handles the comma; verified: `"Mar 25 - Apr 15, Jul 6 - Jul 20"` -> months
   {3,4,7}).
2. Derive `calendar[]` from that scratch combined cell -> it renders BOTH cycles (spring
   plant/harvest, a `growing` lull, fall plant/harvest, `cold_pause` winter). Verified against the
   stored `se_gulf` cherry-tomato calendar: byte-match except a one-month plant/growing boundary,
   which authored windows resolve.
3. SPLIT for storage (A43): top-level `plant_out`/`harvest`/`harvest_start`/`harvest_end`/
   `first_plant_date`/`last_plant_date` carry ONLY the spring (primary) single span; `second_planting`
   = `{start_indoors, plant_out, harvest_start, harvest_end}` for the fall cycle (mirror the
   `se_gulf` cherry-tomato `second_planting` shape). Store the split windows + the step-2 derived
   `calendar[]`.
4. Gate: `region_harness` runs A43 -> the split cell + preserved calendar must pass.

**Recommendation to raise at the check-in:** add a small helper to Task 2's tooling --
`build_second_cycle_cell(spring, fall)` that does combined-derive-then-split deterministically -- so 30
authoring subagents don't each re-implement the split by hand (error-prone; the A43 envelope is the
main gate-churn source). Alternatively, correct Task 4 Step 2's text to the 4-step procedure above and
have each subagent follow it. Either way, `derive_annual_calendar` alone is NOT sufficient for
fall-cycle crops -- that is the load-bearing correction.

Cool-season and spring-only crops are UNAFFECTED: they have single-cycle top-level windows, and
`derive_annual_calendar` renders them correctly as the plan states.
