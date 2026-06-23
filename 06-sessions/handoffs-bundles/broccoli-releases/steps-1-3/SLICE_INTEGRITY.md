# Slice integrity -- how to preflight this SLICE (not the full file)

`LATEST.txt`'s SHA describes the **full `crops_data_final.json`** (`shasum -a 256 == LATEST.txt`). It does NOT
describe `broccoli_current_slice.json`, a single-crop extract written pretty-printed
(`json.dump(crop, indent=2, ensure_ascii=False)`). The slice's raw FILE hash differs BY DESIGN -- not drift.

## The slice's integrity check = the CROP SHA (sorted-min, formatting-independent)
```
sha256(json.dumps(broccoli_crop, sort_keys=True, separators=(',',':'), ensure_ascii=False))
```
**NOTE `ensure_ascii=False`** -- the dataset crop-SHA convention keeps any `°F` literal as a UTF-8 char.

**Expected broccoli crop SHA at canonical `0b767fc2` (full-file `0b767fc2…`, the blueberry cert):**
```
2f81cd13c3db2a74205d9caf85ef89ccda38d99909bfee7d8676b0d23691833c
```
This is the BLANK author-fresh shell (archetype `cool_season_annual`, `calendar_basis frost_anchored` wipe
default, 10 empty region shells, no scalars/varieties/companions yet). Steps 1-3 author INTO this shape.

## The two-callsite integrity chain
1. **AUTHORING base (claude.ai, on the slice):** compute the slice's crop SHA, confirm `== 2f81cd13…`.
2. **APPLY base (Claude Code, on the full file):** at release, preflight `sha256(crops_data_final.json) == LATEST.txt`
   (`0b767fc2…`) before applying. Paths are broccoli-crop-relative.

> **Parallel-authoring note:** zucchini Steps 1-3 is being authored in a SEPARATE claude.ai session against this
> same base (`0b767fc2`). That is fine -- both are independent author-lane slices. Claude Code releases them ONE
> AT A TIME (single session), re-preflighting against the live `LATEST.txt` before each apply, so the second
> release rebases on the first's new SHA. No collision.
