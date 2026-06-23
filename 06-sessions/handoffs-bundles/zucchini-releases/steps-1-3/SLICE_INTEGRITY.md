# Slice integrity -- how to preflight this SLICE (not the full file)

`LATEST.txt`'s SHA describes the **full `crops_data_final.json`** (`shasum -a 256 == LATEST.txt`). It does NOT
describe `zucchini-courgette_current_slice.json`, a single-crop extract written pretty-printed
(`json.dump(crop, indent=2, ensure_ascii=False)`). The slice's raw FILE hash differs from the full-file hash
BY DESIGN -- not drift.

## The slice's integrity check = the CROP SHA (sorted-min, formatting-independent)
```
sha256(json.dumps(zucchini_crop, sort_keys=True, separators=(',',':'), ensure_ascii=False))
```
**NOTE `ensure_ascii=False`** -- the dataset crop-SHA convention keeps any `°F` literal as a UTF-8 char.

**Expected zucchini-courgette crop SHA at canonical `0b767fc2` (full-file `0b767fc2…`, the blueberry cert):**
```
8e3faa1f2968515f7ec0d490c7613af79a1f46633de01cd81e4f7a3e68a5512f
```
This is the BLANK author-fresh shell (archetype `warm_season_fruiting`, `calendar_basis frost_anchored` wipe
default, 10 empty region shells, no scalars/varieties/companions yet). Steps 1-3 author INTO this shape.

## The two-callsite integrity chain
1. **AUTHORING base (claude.ai, on the slice):** compute the slice's crop SHA, confirm `== 8e3faa1f…`.
2. **APPLY base (Claude Code, on the full file):** at release, preflight `sha256(crops_data_final.json) == LATEST.txt`
   (`0b767fc2…`) before applying the handback. Paths are zucchini-crop-relative.
