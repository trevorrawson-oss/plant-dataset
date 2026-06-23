# Slice integrity -- how to preflight this SLICE (not the full file)

`LATEST.txt`'s SHA describes the **full `crops_data_final.json`**. It does NOT describe
`zucchini-courgette_current_slice.json`, a single-crop extract written pretty-printed
(`json.dump(crop, indent=2, ensure_ascii=False)`). The slice's raw FILE hash differs from the full-file hash
BY DESIGN -- not drift.

## The slice's integrity check = the CROP SHA (sorted-min, formatting-independent)
```
sha256(json.dumps(zucchini_crop, sort_keys=True, separators=(',',':'), ensure_ascii=False))
```
**NOTE `ensure_ascii=False`** -- keeps any `°F` literal as a UTF-8 char.

**Expected zucchini-courgette crop SHA at canonical `642f4890` (full-file `642f4890…`, the Steps 4-5.5 release):**
```
fd8174dec57ceb0d9e7ce66755902144e70e4f31d3f071e24fb2bc3ec8b1ba25
```
This is the **post-Step-4-5.5 shell** -- Steps 1-3 (biology/varieties/companions/succession_policy) + Step 3.5
(region shells) + Steps 4-5.5 (all 10 regions FILLED: windows + calendars + succession + the A8
`successions_realized`) authored. What remains NULL/empty is the Steps 6-8 surface: `region_notes_*` (all 10),
`description_*`, `harvest_ready_*`, the `fertilizer` block prose, the `watering` prose, the `container_notes`
deep prose, `rotation` prose, `storage`, `yield_expectations`, `moon_phase_preference.source_note_seasoned`, and
the 7 compounds (`growth_stages`, `notifications`, `weather_triggers`, `pests`, `diseases`,
`failure_diagnostics`, `tips_by_stage`). Steps 6-8 author INTO this shape.

## The two-callsite integrity chain
1. **AUTHORING base (claude.ai, on the slice):** compute the slice's crop SHA, confirm `== fd8174de…`.
2. **APPLY base (Claude Code, on the full file):** at release, preflight `sha256(crops_data_final.json) == LATEST.txt`
   (`642f4890…`) before applying. Paths are zucchini-crop-relative.
