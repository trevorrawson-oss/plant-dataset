# Slice integrity -- how to preflight this SLICE (not the full file)

`LATEST.txt`'s SHA describes the **full `crops_data_final.json`** (`shasum -a 256 == LATEST.txt`). It does NOT
describe `broccoli_current_slice.json`, a single-crop extract written pretty-printed
(`json.dump(crop, indent=2, ensure_ascii=False)`). The slice's raw FILE hash differs from the full-file hash
BY DESIGN -- not drift.

## The slice's integrity check = the CROP SHA (sorted-min, formatting-independent)
```
sha256(json.dumps(broccoli_crop, sort_keys=True, separators=(',',':'), ensure_ascii=False))
```
**NOTE `ensure_ascii=False`** -- the dataset crop-SHA convention keeps any `°F` literal as a UTF-8 char.

**Expected broccoli crop SHA at canonical `20a34223` (full-file `20a34223…`, the Step 3.5 release):**
```
04698276600f1b6a49c4761f8a5df66353290411911d4e972561769e2a66b935
```
This is the **post-Step-3.5 shell** -- Steps 1-3 authored (scalars / biology / varieties / companions /
succession_policy) PLUS the 10 region cells built to the transplant-shape RULE skeleton (`plantings[0]` =
`{track:"beginner", start_indoors:[], plant_out:[], harvest_start:[], harvest_end:[], anchoring_urls:{}}`,
`region_notes_*` null, `resolved_by_zone` cells PENDING). `calendar_basis` = `frost_anchored`. Steps 4-5.5
author the region WINDOWS + calendars INTO this shape.

## The two-callsite integrity chain
1. **AUTHORING base (claude.ai, on the slice):** compute the slice's crop SHA, confirm `== 04698276…`.
2. **APPLY base (Claude Code, on the full file):** at release, preflight `sha256(crops_data_final.json) == LATEST.txt`
   (`20a34223…`) before applying the handback. Paths are broccoli-crop-relative.
