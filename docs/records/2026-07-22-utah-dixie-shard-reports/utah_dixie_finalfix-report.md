# Utah Dixie -- final-review (F1/F2/M1/M2/M3) provenance-leak fixes

**Status: DONE**

Source: `docs/reviews/notes/2026-07-22/utah_dixie_final_review.md` (FIX-FIRST verdict, Important 2 /
Minor 4). Files edited only:
- `tools/staging/utah_dixie_perennials.json`
- `tools/staging/utah_dixie_annuals_warm.json`
- `tools/staging/utah_dixie_annuals_cool.json`

`crops_data_final.json` confirmed byte-unchanged (`git diff --stat -- crops_data_final.json` empty,
SHA still `d8e0a98e...`, matches `LATEST.txt`). No git commit created (per instructions).

## Crops fixed per file

**`utah_dixie_perennials.json` (5 crops) -- F1**, sibling-region ids stripped from
`plantings_provenance.note`: lavender, oregano, rosemary, sage, thyme. Removed "closer to the
warm_arid / low_desert_az / nevada desert-thrives framing than to" -> "suiting this crop far
better than" / "far better than" (rosemary's sentence shape differs slightly). Factual content
(hardiness-zone clause, frost-date anchor, sourcing line) unchanged.

**`utah_dixie_annuals_warm.json` (6 crops) -- F2 + M1 + general-rule sweep**, `plantings_provenance`
rewritten for dry-bean, pole-beans, sweet-corn, field-corn, flint-corn, popcorn: dropped "Nevada"
donor-cell attribution and "UNLV" (dry-bean, sweet-corn, pole-beans), dropped the "Shape C" build
label (all 6), and reworded the literal snake_case tokens `heat_pause`/`second_planting` to plain
English ("no summer heat pause and no fall replant") in all 6 -- these three corn-cells (field-corn/
flint-corn/popcorn) weren't individually named in F2 but shared the identical leak pattern, so the
general rule's "rewrite any you find, not just the ones listed" applied.

**`utah_dixie_annuals_cool.json` (5 crops) -- M2 + M3 + general-rule sweep**:
- garlic (M3): `resolved_by_zone.8.notes` "(not a true cold_pause)" -> "(it never goes fully
  dormant the way a true winter cold pause implies)".
- echinacea (M2): `synthesis_note_seasoned` "summer heat_pause" -> "summer heat pause".
- echinacea, bee-balm, mint, chamomile: their `plantings_provenance` strings also carried the raw
  `heat_pause`/`cold_pause` tokens (missed by both per-class reviews, same root cause as F1/F2 --
  `plantings_provenance` was never in the leak-sweep scope). Reworded to plain English throughout
  ("summer heat pause", "renders as true winter dormancy").

**16 crops touched total.** No other crop/field in any of the 3 files was modified -- confirmed by
a JSON-string-value walk (below) that separates genuine prose from the schema/vocabulary fields
that legitimately store these exact tokens (calendar-array elements, the `track` enum, and the
`heat_pause.classification` field -- required data shape, not a leak, per the review's own
cross-cutting confirmation that these are pre-existing and clean).

## Re-gate result

`python3 tools/region_harness.py utah_dixie 8 <file> <slug>` on all 16 touched crops:

| file | slug | result |
|---|---|---|
| perennials | lavender | GATE: PASS |
| perennials | oregano | GATE: PASS |
| perennials | rosemary | GATE: PASS |
| perennials | sage | GATE: PASS |
| perennials | thyme | GATE: PASS |
| warm | dry-bean | GATE: PASS |
| warm | pole-beans | GATE: PASS |
| warm | sweet-corn | GATE: PASS |
| warm | field-corn | GATE: PASS |
| warm | flint-corn | GATE: PASS |
| warm | popcorn | GATE: PASS |
| cool | echinacea | GATE: PASS |
| cool | garlic | GATE: PASS |
| cool | bee-balm | GATE: PASS |
| cool | mint | GATE: PASS |
| cool | chamomile | GATE: PASS |

**16/16 re-gated PASS.** Spot-checked 7 untouched crops across the 3 files (raspberry, strawberry,
cherry-tomato, habanero, leek, onion, arugula) -- all still GATE: PASS, no collateral breakage from
the shared-file rewrites.

`python3 tools/region_cell_audit.py utah_dixie <file>`:
- perennials: `0 issue(s) across 10 cell(s) in 1 file(s)`
- warm: `0 issue(s) across 42 cell(s) in 1 file(s)`
- cool: `0 issue(s) across 40 cell(s) in 1 file(s)`

## Grep confirmation

A literal byte-grep of `nevada|warm_arid|low_desert|UNR|UNLV|unr_|unlv_|Las Vegas|Phoenix|heat_pause|
cold_pause|second_planting|Shape [A-F]|shard` (case-insensitive) over the raw compact-JSON files
necessarily still returns hits (299 in the warm file, 299 in the cool file) -- these are the JSON
*key names* `"heat_pause":{...}` and the schema-required *enum/vocabulary values* (`calendar` array
tokens `"heat_pause"`/`"cold_pause"`, the `track` field's `"second_planting"` value, and the
`heat_pause.classification` field's `"heat_pause"` value). Those are structural data, not prose, and
the review's own cross-cutting section already confirmed them clean/expected roster-wide.

A JSON-aware walk of every **string value** in the 3 files' utah_dixie cells (excluding only those
same schema/vocabulary fields) confirms: **0 remaining matches in any prose field** (perennials,
warm, cool -- all zero). This is the check that maps to the task's own phrasing, "in any string
value" (i.e. genuine prose, not JSON structure/enum data).

JSON validity: all 3 files parse clean (`json.load`). Re-serialized compact
(`separators=(",",":")`, `ensure_ascii=False`, no trailing newline), matching prior format;
`git diff --stat` on each shows a single-line change (expected for single-line compact files).

## Confirmation

Grep clean: **YES** (0 genuine prose-field leaks across all 3 staging files; the raw-byte grep's
non-zero count is fully accounted for by legitimate schema keys/enum values, not build-provenance
or sibling-region leaks).
