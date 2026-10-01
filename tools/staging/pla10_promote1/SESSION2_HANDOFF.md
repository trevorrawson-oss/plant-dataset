# PLA-10 promote 1, session 2 hand-off (2026-10-01)

Canonical READ-ONLY throughout: `c5fc3d13` == LATEST.txt, unchanged. HEAD at session start `459704c` == origin/main.
Nothing landed: no promote, no canonical write, no gate arming. Two commits on Trevor's order, PUSHED 2026-10-01 (`459704c..cd1a96b`): A `58c485c` (tooling: the PDF reader through pypdf 6.14.2 + the 'a foot' idiom), B `cd1a96b` (data staging). The four rulings below are TAKEN and closed; session 3 does not reopen them.

Working-tree note: an untracked `.codex/` directory and an untracked `AGENTS.md` were present in the checkout during session 2. They are not this arc's; they were left untouched and are in no commit. Leave them out of session 3's commits too.

## What is staged
- **93 of the 113 crops** (every session-2 row of worklist 56 §4), one `row-none` entry each, in `crops/<slug>.json`.
- `EVIDENCE.tsv`: 145 rows; every numeric field on every staged entry has a row whose quote was checked as a substring of
  the HASHED bytes in `tools/.evidence_cache/` (`MANIFEST.tsv` now 211 rows; raw-byte fetches under two user agents, PLA-532 convention).
- `python3 tools/promote_pla10_planting_layout.py --check` -> `REFUSED: FIXED LIST ... missing [the 20 session-3 crops], extra []` (by design).
- `python3 tools/staging/pla10_promote1/validate_partial.py --only <the 86 HTML-backed crops>` -> OK on every per-crop guard
  (evidence, retired anchors, restatements, A44 armed, A62, A63, numeric_sanity, display_readiness). The 7 PDF-backed crops
  (below) refuse at guard 2 until the PDF ruling lands.
- Lane A (mechanical, 46 rows): 41 staged by `stage_lane_a.py` straight from the worklist TSV (quote overrides in
  `lane_a_overrides.json`: table rows quoted as their full row string, two UMN pages re-worded, onion's 'a foot' row withheld);
  5 moved to lane B (4 PDF pages, raspberry's changed page).
- Lane B (judgment, 47 flagged rows + the 5 hand-overs): every crop has a decision row in `lane_b_specs/<slug>.json`
  (the spec; `stage_lane_b.py --all` rebuilds the stage files and EVIDENCE rows from them and re-checks every quote).
- Lane C (hunts): `HUNTS.md`. **All seven W5 crops and all three W3 crops FOUND a citable page**, so the R5 migration
  waiver list stays EMPTY (`planting_layout_migration_known.WAIVERS` needs no entry from session 2). field-corn's result
  goes to session 3: Clemson 'Homegrown Grits' names dent corn with a conditional single value ('spaced a little further
  apart (2 ft)') and UGA B577's chart row is labelled just 'Corn' (3-3.5 ft rows, 12-18 in plants); neither is a clean
  field-corn range, so session 3 decides between them and the sweet-corn sibling page (W3).

## Rulings TAKEN by Trevor (2026-10-01, session 2 close-out review)
1. **PDF evidence: TAKEN.** The manifest keeps hashing the raw PDF bytes; `check_evidence` runs the quote check for a `.pdf`
   cache file against pypdf's text extraction of those bytes (`PDF_TEXT_EXTRACTOR = ("pypdf", "6.14.2")` pins the extractor;
   docstring guard 2). TDD: RED with a Flate-compressed fixture (`flate_pdf`) whose quote fails under the old reader, GREEN
   after; harness mutations `p_pdf_read_as_raw_bytes` + `p_foot_idiom_dropped`; affected set run. The 7 PDF-backed crops
   (bell-pepper, garlic, jalapeno, pickling-cucumber, persimmon, orange-navel, nectarine) now pass guard 2 as staged.
2. **'a foot' idiom: TAKEN.** `IDIOMS = (("a foot", 1.0),)` in the promote; 'two feet' and 'a foot or two' read through the
   word table; the test pins the table both ways. onion's row ([12,12], same sentence) and zinnia's row ([12,12], 'space the
   rows a foot apart') are restaged from it.
3. **W6 two-page entries: PERMISSIVE reading TAKEN.** W6 forbids one VALUE joined from two pages; in-row and row spacing are
   two values and the entry carries one anchoring_url per source. Condition honored: EVIDENCE.tsv has one row per (field,
   source), never a shared row (carrot: in_row <- umn_ext, row <- clemson_hgic; radish: in_row <- umd_ext, row <- clemson_hgic).
   Session 3 may add raspberry rows (UGA C766 'space the rows 12 feet apart') and mint rows under W2 (USU 'at least 2 feet'
   is a minimum: [24,24] with 'minimum' recorded, only if the sentence is a recommendation).
4. **VH021 row minimums as [x,x] with 'minimum' recorded: TAKEN** (beet, celery), consistent with W2 as refined.

After the rulings: `validate_partial.py` (no --only) -> all 93 staged crops pass every per-crop guard, 147 evidence rows,
147 (entry, field) figures covered; `promote --check` still refuses on the fixed list naming exactly the 20 session-3 crops.

## Independent source-truth review sample (session 3): named
Every DIFFERS / SCOPE / COMMERCIAL row of worklist 56 §4.1, plus **all 34 re-authored dill strings** (the largest restatement
edit in the promote), by path:
- `growth_stages[1].user_action_beginner`
- `growth_stages[1].user_action_seasoned`
- `notifications[0].body_seasoned`
- `start_method.notes_beginner`
- `start_method.notes_seasoned`
- `tips_by_stage.seedling[0].text_beginner`
- `tips_by_stage.seedling[0].text_seasoned`
- `regions.ca_desert.resolved_by_zone.10.notes`
- `regions.ca_desert.resolved_by_zone.11.notes`
- `regions.ca_desert.resolved_by_zone.9.notes`
- `regions.ca_interior.resolved_by_zone.8.notes`
- `regions.ca_interior.resolved_by_zone.9.notes`
- `regions.ca_north_coast.resolved_by_zone.10.notes`
- `regions.ca_north_coast.resolved_by_zone.9.notes`
- `regions.ca_south_coast.resolved_by_zone.10.notes`
- `regions.ca_south_coast.resolved_by_zone.11.notes`
- `regions.ca_south_coast.resolved_by_zone.9.notes`
- `regions.fl_peninsula.resolved_by_zone.10.notes`
- `regions.fl_peninsula.resolved_by_zone.11.notes`
- `regions.hawaii_tropical.resolved_by_zone.10.notes`
- `regions.hawaii_tropical.resolved_by_zone.11.notes`
- `regions.hawaii_tropical.resolved_by_zone.12.notes`
- `regions.hawaii_tropical.resolved_by_zone.13.notes`
- `regions.low_desert_az.resolved_by_zone.10.notes`
- `regions.low_desert_az.resolved_by_zone.9.notes`
- `regions.northern_tier.resolved_by_zone.3.notes`
- `regions.northern_tier.resolved_by_zone.4.notes`
- `regions.northern_tier.resolved_by_zone.5.notes`
- `regions.northern_tier.resolved_by_zone.6.notes`
- `regions.northern_tier.resolved_by_zone.7.notes`
- `regions.se_gulf.resolved_by_zone.10.notes`
- `regions.se_gulf.resolved_by_zone.8.notes`
- `regions.se_gulf.resolved_by_zone.9.notes`
- `regions.warm_arid.resolved_by_zone.8.notes`

## Crops whose figure MOVES (46; each carries its restatement adjudication in the stage file)
| crop | today | staged in_row | staged row | sources | restatements adjudicated | edits |
| -- | -- | -- | -- | -- | -- | -- |
| arugula | `[1,3]` | `[3,6]` | `null` | uwi_hort | 6 | 0 |
| banana-pepper | `[12,18]` | `[12,24]` | `[36,36]` | uga_ext | 5 | 4 |
| bee-balm | `[18,24]` | `[24,30]` | `null` | iastate_ext | 2 | 2 |
| blueberry | `[48,72]` | `[48,60]` | `[96,120]` | ncsu_ext | 2 | 0 |
| bok-choy | `[6,12]` | `[6,6]` | `null` | ncsu_ext | 8 | 0 |
| celery | `[6,10]` | `[6,12]` | `[18,18]` | uf_ifas_vh021 | 6 | 4 |
| chamomile | `[8,12]` | `[8,8]` | `[18,18]` | msu_bozeman | 8 | 7 |
| cherry-sour | `[180,300]` | `[180,240]` | `null` | unh_ext | 0 | 0 |
| cherry-sweet | `[180,300]` | `[180,240]` | `null` | unh_ext | 2 | 0 |
| chives | `[8,12]` | `[6,12]` | `null` | umn_ext | 7 | 7 |
| cilantro-coriander | `[2,4]` | `[2,2]` | `[15,15]` | usu_ext | 2 | 0 |
| collards | `[18,24]` | `[12,24]` | `[30,36]` | umd_ext | 8 | 5 |
| cosmos | `[12,18]` | `[12,24]` | `null` | usu_ext | 4 | 4 |
| cucumber | `[12,24]` | `[12,18]` | `[48,72]` | vce_426_331 | 1 | 0 |
| dill | `[8,12]` | `[9,9]` | `[12,12]` | usu_ext | 35 | 34 |
| dry-bean | `[2,4]` | `[2,3]` | `[18,24]` | usu_ext | 2 | 0 |
| elderberry | `[48,96]` | `[60,84]` | `null` | psu_ext | 3 | 2 |
| fig | `[120,240]` | `[120,192]` | `[156,240]` | uf_ifas_edis | 0 | 0 |
| grapefruit | `[216,360]` | `[180,180]` | `null` | uf_ifas_hs132 | 3 | 0 |
| habanero | `[18,24]` | `[12,24]` | `[30,36]` | umd_ext | 3 | 2 |
| kohlrabi | `[6,9]` | `[6,8]` | `[18,24]` | iastate_ext | 18 | 12 |
| lemongrass | `[24,36]` | `[36,36]` | `null` | usu_ext | 1 | 1 |
| lettuce-leaf | `[6,8]` | `[6,10]` | `[12,24]` | clemson_hgic | 1 | 0 |
| mandarin-clementine | `[120,216]` | `[180,180]` | `null` | uf_ifas_hs132 | 0 | 0 |
| mint | `[12,24]` | `[12,12]` | `null` | uf_ifas | 0 | 0 |
| mulberry | `[300,360]` | `[240,360]` | `null` | ncsu_ext_handbook_tree_fruit | 0 | 0 |
| nectarine (PDF) | `[216,240]` | `[144,180]` | `null` | unh_ext | 12 | 0 |
| orange-navel (PDF) | `[180,300]` | `[180,240]` | `null` | uhawaii_ctahr | 0 | 0 |
| parsnip | `[3,6]` | `[3,3]` | `[18,24]` | clemson_hgic | 13 | 10 |
| pawpaw | `[96,180]` | `[96,96]` | `null` | ksu_pawpaw | 2 | 0 |
| pear-asian | `[144,300]` | `[120,180]` | `null` | clemson_hgic | 16 | 0 |
| pear-european | `[180,300]` | `[240,240]` | `null` | uga_ext | 9 | 0 |
| persimmon (PDF) | `[180,240]` | `[180,216]` | `[240,240]` | tamu_agrilife | 2 | 0 |
| pickling-cucumber (PDF) | `[8,18]` | `[6,12]` | `[48,48]` | osu_ext | 1 | 0 |
| pomegranate | `[120,180]` | `[120,192]` | `[156,240]` | uf_ifas_edis | 0 | 0 |
| roma-tomato | `[24,30]` | `[18,24]` | `[48,48]` | iastate_ext | 2 | 0 |
| rosemary | `[24,36]` | `[24,24]` | `null` | psu_ext | 6 | 6 |
| shallot | `[6,8]` | `[3,6]` | `[12,18]` | usu_ext | 16 | 10 |
| slicing-cucumber | `[12,24]` | `[12,18]` | `[48,72]` | vce_426_331 | 2 | 0 |
| sweet-alyssum | `[4,8]` | `[8,10]` | `null` | psu_ext | 4 | 3 |
| sweet-pea | `[3,6]` | `[5,6]` | `null` | osu_ext | 1 | 0 |
| sweet-potato | `[12,18]` | `[12,14]` | `[36,36]` | uf_ifas | 8 | 4 |
| tomatillo | `[24,48]` | `[24,24]` | `[36,36]` | usu_ext | 3 | 0 |
| turnip | `[2,4]` | `[2,3]` | `[14,18]` | clemson_hgic | 18 | 11 |
| viola | `[6,10]` | `[6,12]` | `null` | clemson_hgic | 5 | 4 |
| zinnia | `[9,12]` | `[8,12]` | `null` | clemson_hgic_1149 | 4 | 4 |

Decision rows worth a second look (the biggest moves or the closest calls): nectarine 18-20 ft -> 12-15 ft (UNH names
nectarine; W3 hunt-first), pear-asian [144,300] -> [120,180] (Clemson minimum range), the three citrus to HS132's minimum
(orange-navel to CTAHR's 15-20 ft range, PDF), bok-choy [6,12] -> [6,6] (NCSU species page; UMN 12-18 is the full-head
regime), chamomile -> [8,8], cilantro -> [2,2] (USU leaf-crop seed spacing, no thin-to on the page), parsnip -> [3,3],
dill -> [9,9] (34 prose strings re-authored), cosmos [12,18] -> [12,24] (USU species page over UF's cultivar sheet),
sweet-alyssum [4,8] -> [8,10] (PSU sowing table), sweet-pea [3,6] -> [5,6] (OSU thin-to), dry-bean [2,4] -> [2,3] (USU names
dry beans), roma-tomato -> ISU's determinate range [18,24].

## Crops staged with today's figure unchanged (47)
apricot, basil, beefsteak-tomato, beet, bell-pepper (PDF), borage, broccoli, brussels-sprouts, cabbage, calendula, carrot, cauliflower, cherry-tomato, echinacea, edamame, eggplant, english-cucumber, garlic (PDF), grape-tomato, green-beans-bush, heirloom-tomato, jalapeno (PDF), kale, lavender, leek, lemon, lime, marigold, nasturtium, okra, onion, oregano, parsley, peach, plum, pole-beans, potato, radish, raspberry, sage, snow-peas, spinach, spring-onion, sugar-snap-peas, sunflower, swiss-chard, thyme

## Retired anchors (11 crops): all dispositions staged
carrot, cherry-tomato, grape-tomato, lemon (moved), lime, potato, radish (lane A, reasons in `lane_a_overrides.json`);
celery, roma-tomato, sweet-potato, tomatillo (lane B specs). tomatillo's four tomato pages dropped as 'a tomato page, not
tomatillo's'; lemon's anchor moved as-is (not mis-keyed, worklist §3).

## Fetch notes
- `fetch_evidence.py` (two UAs, gzip, optional Safari + Sec-Fetch headers via `FETCH_UA=safari`, `FETCH_DELAY`). hgic.clemson.edu's
  Cloudflare rule (error 1010) 403s the plain Python UA outright and the browser UA without Accept-Encoding + Sec-Fetch headers.
  ucanr.edu/site/... pages 403 under every header set tried (uc_mg garlic, UC MG citrus): read from `tools/.doc_cache` only.
- 13 cited URLs 301 to new URLs (UF edis -> ask.ifas; five UMN pages; UMD peas; UW parsley; MU g6461; CTAHR www3); each is a
  second MANIFEST row on the same bytes, so an entry may anchor either URL.
- UMN's raspberry page lost its between-rows sentence; Clemson's zinnia page lost its '12 to 18 inches' row sentence.

## Session 3 inherits
the 20 special-structure crops (hills, corn incl. field-corn's hunt result, the five D1 blend repairs + spaghetti's decision
row, apple's rootstock basis, artichoke, asparagus), the 8 microgreens (promote-written), the independent source-truth review
(sample must include every DIFFERS / SCOPE / COMMERCIAL row above), the gauntlet, the arming flips, the data commit
(worklist 56 §8), and the four rulings above.

## Helpers in this directory (session tooling, not gates)
`fetch_evidence.py`, `stage_lane_a.py` + `lane_a_overrides.json`, `stage_lane_b.py` + `lane_b_specs/`, `validate_partial.py`
(refuses on zero staged; reuses the promote's own functions; NOT a substitute for `--check`).

