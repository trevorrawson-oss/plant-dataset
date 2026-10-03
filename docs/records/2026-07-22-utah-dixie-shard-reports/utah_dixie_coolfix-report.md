# Utah Dixie COOL cells -- content-review B fixes

**Status: DONE**

File edited: `tools/staging/utah_dixie_annuals_cool.json` (all 40 COOL cells). No other file
touched -- `crops_data_final.json` confirmed unmodified via `git status -sb` (silent/clean), and
no git commit was created (HEAD unchanged at `fd47140`).

Source: `docs/reviews/notes/2026-07-22/utah_dixie_content_review_B.md` (Critical 1 / Important 3 /
Minor 2). All six findings applied.

## Fixes applied

1. **CRITICAL C1 -- "Nevada" build-word leak in leek.** Reworded `plantings_provenance`,
   `resolved_by_zone.8.notes`, and `region_notes_seasoned` to drop the sibling-region name and
   describe the two-cycle shape generically ("the same proven overwintering two-cycle pattern: a
   spring stand pushed out by summer heat plus a frost-hardy fall-transplanted stand"). Meaning
   unchanged, no other region named.

2. **IMPORTANT I1 -- region-id tokens in `plantings_provenance`.** Stripped `Nevada` /
   `nevada/low_desert_az/warm_arid` from bee-balm, echinacea, mint, chamomile, chives, and leek's
   provenance text; reworded to generic archetype language ("the established desert
   herbaceous-perennial cell shape", "consistent with how this crop is handled in other desert
   regions in this dataset" / "other warm-desert cells"). No field was nulled -- each retained a
   real, honest provenance note (source-tabled or archetype-analogy basis), so null was not needed.

3. **IMPORTANT I2 -- "Heflebower" surname (28 occurrences).** Normalized every instance across
   arugula, bok-choy, broccoli, cauliflower, collards, kohlrabi, beet, carrot (2 in one field),
   turnip, radish, onion, shallot, spring-onion, and chamomile (3 fields, one shared with fix 2/5)
   to the publication/agency form already used by the cool-herb cells: "USU('s) fall-gardening
   guidance for the St. George area" (or "USU's Fall Gardening in the St. George Area guidance"
   where the pub title was already being named). Source basis unchanged.

4. **IMPORTANT I3 -- "37 degrees N" -> "37°N".** Fixed all 4 spots (onion
   `day_length_note_seasoned` + `region_notes_seasoned`, shallot same two fields).

5. **MINOR M1 -- chamomile `plantings_provenance` build-log register.** Folded into the fix 2
   rewrite of the same field: dropped the truncated "Shape re-anchored..." fragment and the
   Nevada/Heflebower tokens together, replaced with a single clean sentence describing the
   structural donor, the spring/fall citation basis, and the heat_pause/cold_pause sourcing.

6. **MINOR M2 -- lettuce-leaf + spinach fall `harvest_end` past frost.** Chose the honesty-note
   route (not date trimming, so no calendar re-derive was needed). Added a `zone_notes` sentence
   to both (field was `null`) stating the Nov 19 / Nov 17 finish rests on the crop's own general
   cold tolerance past the Nov 1 average first frost, not a USU-dated fall-harvest line specific
   to that crop.

## Re-gate results

`python3 tools/region_harness.py utah_dixie 8 tools/staging/utah_dixie_annuals_cool.json <slug>`
run on every touched crop:

| slug | result |
|---|---|
| leek | GATE: PASS |
| onion | GATE: PASS |
| shallot | GATE: PASS |
| bee-balm | GATE: PASS |
| chamomile | GATE: PASS |
| echinacea | GATE: PASS |
| mint | GATE: PASS |
| chives | GATE: PASS |
| lettuce-leaf | GATE: PASS |
| spinach | GATE: PASS |

**10/10 re-gated PASS.**

Whole-file audit: `python3 tools/region_cell_audit.py utah_dixie tools/staging/utah_dixie_annuals_cool.json`
-> `region_cell_audit[utah_dixie]: 0 issue(s) across 40 cell(s) in 1 file(s)`.

Spot-checked 4 untouched crops (arugula, broccoli, beet, carrot) still GATE: PASS post-edit (no
collateral breakage from the shared file rewrite).

## Leak confirmation (grep, whole file)

- `Heflebower`: 0
- `Nevada` / `nevada` (case-insensitive): 0
- `degrees N`: 0
- `warm_arid`, `low_desert` (any case): 0
- em dash `—` / literal `--`: 0 (unchanged from baseline; new prose stayed within house style)

JSON validity confirmed (`json.load` succeeds); file re-written compact
(`separators=(",",":")`, `ensure_ascii=False`), matching the existing format.
