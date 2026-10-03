# Utah "Dixie" region — cross-region-city consumer-prose leak fix

**Status:** COMPLETE. All cross-region-city references removed from consumer prose in the three
utah_dixie staging shards; every touched crop re-gated PASS and re-audited 0 issues. Mirrors the
Nevada "colder than Phoenix" -> absolute-framing fix. crops_data_final.json untouched; no git commit.

## Crops fixed, per file

### tools/staging/utah_dixie_annuals_warm.json — 8 crops (Las Vegas leak)
cucumber, slicing-cucumber, pickling-cucumber, english-cucumber, yellow-summer-squash,
zucchini-courgette, green-beans-bush, edamame

- Field: `region_notes_seasoned` (each).
- Reworded the clause `"so unlike the Las Vegas Valley just across the state line, there is no
  second cycle here"` -> `"so there is no second cycle here"`. Meaning preserved: USU documents
  no fall/summer replant window for these crops here.

### tools/staging/utah_dixie_citrus.json — 5 crops (Phoenix leak)
grapefruit, lemon, lime, mandarin-clementine, orange-navel

- Fields touched (each crop, 5 Phoenix mentions apiece = 25 total): `region_notes_beginner`,
  `region_notes_seasoned`, `cold_basis_seasoned`, `cold_basis_beginner`, and
  `resolved_by_zone.8.suitability_note_beginner`.
- Every `"colder than Phoenix"` / `"colder than the Phoenix low desert"` /
  `"colder than the lower Phoenix desert"` reworded to absolute framing keyed to the real z8b
  figure already in the prose (ordinary winter lows around 15 to 20°F, USU Extension Washington
  County frost/elevation data), e.g.:
  - seasoned openers: `"...run roughly 15 to 20°F on an ordinary cold night, colder than the
    Phoenix low desert, and USU's..."` -> `"...run roughly 15 to 20°F on an ordinary cold night,
    and USU's..."`
  - cold_basis_seasoned tail: dropped the trailing `", colder than the lower Phoenix desert."`
  - beginner: `"Winters here get colder than Phoenix, with ordinary lows around 15 to 20°F"` ->
    `"Winters here bring ordinary lows around 15 to 20°F"`; comparative clauses like
    `"winters here, colder than Phoenix, regularly..."` -> `"winters here, with ordinary lows
    around 15 to 20°F, regularly..."`.
- Every suitability verdict (survives_no_fruit / unsuitable) and cold-limit meaning left intact.

### tools/staging/utah_dixie_perennials.json — strawberry: NO edit (false positive)
See finding below.

## Re-gate + re-audit result
- **14/14 re-gated PASS** (8 warm + 5 citrus + strawberry), each ending `GATE: PASS`.
- **Audit 0 issues:** annuals_warm 0/42 cells, citrus 0/5 cells, perennials 0/10 cells.

## strawberry finding
FALSE POSITIVE. The flag was a substring hit on `"Renovate"` (capital R at sentence start:
"Renovate right after harvest...") inside `strawberry.region_notes_seasoned` — the June-bearing
matted-row **renovation** step, not the city Reno. The string names no region city (no Las Vegas /
Phoenix / Reno / Las Cruces / Clark County / Mesilla). Left unchanged.

## City-term confirmation
Word-boundary grep across all three files for `Las Vegas | Phoenix | Las Cruces | \bReno\b |
Clark County | Mesilla`: **0 matches.** The only remaining raw `Reno` substring is the single
`Renovate` in strawberry (documented false positive above). All three files parse as valid JSON.
