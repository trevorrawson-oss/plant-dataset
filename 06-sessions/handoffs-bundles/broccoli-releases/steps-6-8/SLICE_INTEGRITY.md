# Slice integrity -- how to preflight this SLICE (not the full file)

`LATEST.txt`'s SHA describes the **full `crops_data_final.json`**. It does NOT describe
`broccoli_current_slice.json`, a single-crop extract written pretty-printed
(`json.dump(crop, indent=2, ensure_ascii=False)`). The slice's raw FILE hash differs from the full-file hash
BY DESIGN -- not drift.

## The slice's integrity check = the CROP SHA (sorted-min, formatting-independent)
```
sha256(json.dumps(broccoli_crop, sort_keys=True, separators=(',',':'), ensure_ascii=False))
```
**NOTE `ensure_ascii=False`** -- keeps any `°F` literal as a UTF-8 char.

**Expected broccoli crop SHA at canonical `78ef87cd` (full-file `78ef87cd…`, the Steps 4-5.5 release):**
```
a68e13add84abfc2d7cf6431b7e3959e5202134c4367e11aa672c46120d9f21c
```
This is the **post-Step-4-5.5 shell** -- Steps 1-3 (biology/varieties/companions/succession_policy, PLUS the
fertilizer block, watering prose, container core, rotation, description, harvest_ready -- broccoli authored more
at 1-3 than zucchini) + Step 3.5 + Steps 4-5.5 (all 10 regions FILLED: windows + calendars + succession + the A8
`successions_realized`). What remains NULL/empty is a LEANER Steps 6-8 surface than zucchini's:
`region_notes_*` (all 10), `storage`, `yield_expectations`, `moon_phase_preference.source_note_seasoned`,
`container_notes.shape_requirements` (dropped at 1-3, re-author here), and the 7 compounds (`growth_stages`,
`notifications`, `weather_triggers`, `pests`, `diseases`, `failure_diagnostics`, `tips_by_stage`). Steps 6-8
author INTO this shape (plus the Step-6 seasoned depth-lift pass over the already-authored prose).

## The two-callsite integrity chain
1. **AUTHORING base (claude.ai, on the slice):** compute the slice's crop SHA, confirm `== a68e13ad…`.
2. **APPLY base (Claude Code, on the full file):** at release, preflight `sha256(crops_data_final.json) == LATEST.txt`
   (`78ef87cd…`) before applying. Paths are broccoli-crop-relative.
