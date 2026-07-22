# Utah "Dixie" region -- COOL cells content review B (independent)

**Scope:** `tools/staging/utah_dixie_annuals_cool.json` -- 40 COOL cells (brassicas, roots/leafy,
cool legumes, alliums, cool herbs, cool flowers, perennial herbs). Read-only review against
`docs/reviews/notes/2026-07-22/utah_dixie_sources.md` (the bible) + the c1-c5 shard reports.
Reviewer did not edit the file; findings below are for the controller to apply.

## Overall verdict: **SHIP-WITH-FIXES**

No factual, sourcing, or calendar-coherence errors were found. Every spring date matches its USU
Group (A Feb 15 / B Mar 1), every fall `second_planting` traces to a USU-documented or
bible-sanctioned basis (no fabricated windows), the allium/A9 handling is sound (photoperiod
violations 0), and all 40 calendars are coherent (January cold_pause or the documented allium/
perennial overwinter pattern; no impossible growing months). The required fixes are prose/leak
cleanups, not data corrections. One is a genuine must-fix (a "Nevada" build-word leak in rendered
consumer copy); the rest are consistency/polish.

**Counts: Critical 1 | Important 3 | Minor 2**

Mechanical checks: em dashes 0, en dashes 0, `°F` glyph used (101x), British spellings 0.
Fall-cycle inventory = 20 crops, all bible-sanctioned (6 Group-E dated + broccoli/cauliflower/carrot
Heflebower analogy + arugula/bok-choy/collards/kohlrabi cole-greens analogy + borage/calendula/
cilantro/dill/parsley cool-herb two-window + spring-onion + leek). Frost anchor Mar 30 / Nov 1 on
every cell.

---

## CRITICAL (1)

### C1. "Nevada" build-word leak in leek's rendered consumer prose
- **crop:** leek -- **file:** `tools/staging/utah_dixie_annuals_cool.json`
- The internal sibling-region name **Nevada** leaks into user-facing copy:
  - `region_notes_seasoned`: "...structured on the same two-cycle pattern already used for this crop
    in **the Nevada region**."
  - `zone_notes` (`resolved_by_zone.8.notes`): "...structured on **the Nevada region's** own
    two-cycle leek pattern..."
  - (also `plantings_provenance`, see I1)
- The task's PROSE rule explicitly forbids the build word "Nevada" in consumer copy, and
  `region_notes_seasoned` is the primary rendered surface. This exposes build lineage to users.
- **Exact fix:** drop the region attribution. Replace "structured on the same two-cycle pattern
  already used for this crop in the Nevada region" with e.g. "structured on the same proven
  overwintering two-cycle pattern: a spring stand pushed out by summer heat plus a frost-hardy
  fall-transplanted stand." Same reword in `zone_notes`. Factual content unchanged.

---

## IMPORTANT (3)

### I1. Internal region-id build words in `plantings_provenance` (5 cells)
- **crops:** bee-balm, chamomile, echinacea, mint, chives, leek -- **file:** same
- `plantings_provenance` (and one `notes`) name internal region ids / sibling regions:
  - bee-balm / echinacea / mint / chamomile: "...its existing **nevada/low_desert_az/warm_arid**
    herbaceous-perennial cell shape..."
  - chives: "...matching **the Nevada region's** own convention for this crop."
  - echinacea: "...matching **the Nevada donor's** own divergence..."
  - leek `plantings_provenance`: "...structured on **the Nevada region's** own two-cycle leek pattern..."
- Same leak class as C1 but in the provenance/disclosure field. Whether or not this field renders,
  the tokens `Nevada`, `warm_arid`, `low_desert` must not appear (task PROSE rule).
- **Exact fix:** strip the internal id list; describe the lineage generically, e.g. "modeled on the
  established desert perennial-in-place archetype (fall-establish, cool-season harvest, summer heat
  pause), re-anchored to St. George's frost dates." Keep the honest "no USU Table 1 line" disclosure.

### I2. "Heflebower" author surname in consumer prose -- inconsistent, normalize (28 occurrences)
- **crops:** arugula, beet, bok-choy, broccoli, carrot, cauliflower, chamomile, collards, kohlrabi,
  radish, spring-onion, turnip (in `region_notes_seasoned` + `synthesis_note_seasoned`), plus
  onion/shallot `notes` -- **file:** same
- The brassicas/roots refer to the fall source as "USU('s) **Heflebower** fall-gardening guidance,"
  naming the bare extension-author surname. The cool-herb cells (borage/calendula/cilantro/dill)
  instead cite it cleanly by publication title: "USU's general fall-gardening guidance for
  restarting cool-season crops (**Fall Gardening in the St. George Area**)." A bare surname reads
  like an internal citation token to a lay reader and is inconsistent within the same batch. This is
  the same house concern as the forbidden "UNR/UNLV" institutional shorthands.
- **Exact fix:** normalize every consumer-prose "Heflebower" to the publication/agency form used by
  the cool-herb cells, e.g. "USU Extension's fall-gardening guidance for the St. George area" (or the
  pub title). Source basis unchanged. (The bible's instruction to "cite Heflebower" is about which
  source backs the window, not about printing the surname in consumer copy.)

### I3. "37 degrees N" should render "37°N" (onion + shallot)
- **crops:** onion, shallot -- **file:** same
- `region_notes_seasoned` and `day_length_note_seasoned` both spell "about 37 **degrees** N" /
  "roughly 37 **degrees** N." The style rule is to avoid the word "degrees" (glyph form). Latitude,
  not temperature, but it is the only spelled "degrees" in the batch and trivially fixable.
- **Exact fix:** replace "37 degrees N" with "37°N" in both fields of both crops (4 spots).

---

## MINOR (2)

### M1. chamomile `plantings_provenance` reads as internal build notes
- **crop:** chamomile -- **file:** same
- "...any USU vegetable-only planting chart). **Shape re-anchored** to the St. George frost dates and
  heat_pause..." The truncated, capitalized "Shape" sentence plus build phrasing reads like a build
  log. (Not the forbidden "Shape E" token, but the same register slip.) Tidy to plain wording, or
  confirm `plantings_provenance` is not user-rendered. Folds naturally into the I1 reword.

### M2. lettuce-leaf + spinach fall `harvest_end` extends ~2.5 weeks past first frost
- **crops:** lettuce-leaf (fall harvest_end Nov 19), spinach (Nov 17) -- **file:** same
- Both fall stands are carried ~17-18 days past the Nov 1 average first frost on general
  cold-tolerance, cited only to the frost-date source (`usu_ext_wash_frost`). Heflebower's explicit
  "left in the ground quite late into winter" line names only beet/carrot/turnip, not the greens.
  The shard report (c2) discloses this honestly, but the in-cell prose does not. Low severity (both
  are genuinely cold-hardy and survive light frost). Optional: either add a one-clause in-prose note
  that the greens hold under row cover past frost, or trim to `first_frost` to be conservative.

---

## Adjudicated flags (rulings)

- **onion/shallot plant_out Sep 26-Oct 5 (Aug 1-10 read as seed-start):** **HONEST / DEFENSIBLE --
  keep as-is.** The `zone_notes` transparently frames Aug 1-10 as "when to start seed or source
  sets," with the outdoor transplant ~8 weeks later; early-Aug seed to late-Sep/early-Oct transplant
  is standard fall-onion establishment, and the later `plant_out` is what A9 checks (photoperiod
  violations 0, window fully outside the forbidden Apr-Aug band). Not an overclaim -- the note says
  "this cell reads that as," it does not assert USU labeled it a seed-start. (Only the I3 "37°N"
  style fix rides along.)

- **radish + swiss-chard spring-only:** **CORRECT -- keep.** Neither is on USU's Group E dated fall
  list, and Heflebower names neither with a fall date (radish is called "large-seeded/easy" but
  undated). Authoring a fall window would be fabricated; the bible rules both spring-only. radish
  additionally states its spring-only status in its own `region_notes_seasoned` (transparent).

- **radish heat_pause widened to [5,6,7,8,9]:** **ACCEPTABLE -- keep.** A legitimate A37
  stale-`growing` coherence fix (26-day DTM finishes harvest by mid-April, leaving May-Sep genuinely
  idle in a spring-only crop). The `basis_seasoned` was honestly reworded to frame May as the lead-up
  and not claim May independently hits 100°F (only Jun/Jul/Aug are USU-sourced). Matches the
  spring-only-cool-crop summer-idle convention. Not a content distortion.

- **cool legumes (fava / snow-peas / sugar-snap-peas) spring-only:** **CORRECT -- keep.** The bible
  explicitly places "peas (snow/sugar-snap/fava)" in the no-USU-fall-window bucket; USU's Group E
  list has no peas. Nevada's donor carries two windows, but the bible's source-grounded ruling
  overrides -- authoring a fall pea window would be a fabricated citation. fava's Group A placement
  is disclosed as a "peas"-line analogy in its `notes`.

---

## What is clean (verified, no action)
- Spring Group dates: all Group A (Feb 15) and Group B (Mar 1) assignments correct; Table-1-absent
  crops (celery Group B; borage/calendula/cilantro/dill Group A) disclose the analogy in
  `region_notes_seasoned`.
- Fall windows: all 20 trace to Group E dated, the named Heflebower analogies, or bible-sanctioned
  cool-herb/spring-onion/leek two-window shapes. cabbage's wide May 1-Jul 15 window correctly
  narrowed to Jun 15-Jul 15 to clear the spring harvest; carrot/turnip/beet "held late" past frost
  correctly cited to Heflebower.
- Allium / A9: onion + shallot `intermediate_day`, fall-set, plant_out outside Apr-Aug (0 A9
  violations); garlic fall clove Sep 20-Oct 25 within usu_ext_garlic's late-Sep-Nov range;
  spring-onion two-window, harvested green, no day-length gating; overwinter calendars (garlic/onion/
  shallot: winter `growing` + `season_over` gap, no false cold_pause) are the documented pattern.
- Dual-register prose is distinct per crop (beginner = plain how-to; seasoned = USU-chart/Group
  citations), not restatements. No em dashes, American English, `°F` glyph throughout.
