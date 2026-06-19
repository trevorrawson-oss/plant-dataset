# Re-scope note -- strawberry Step 4 after fl_peninsula (z10-11)

**From:** claude.ai (authoring lane) · **To:** Claude Code (structural/release lane) · **Date:** 2026-06-18

## What this hand-back contains
- `strawberry_step4_fl_peninsula_patch_v1.json` -- 14-op canonical patch, `fl_peninsula` z10 + z11 ONLY. `calendar[]` left `[]`.
- `STATE_HISTORY_snippet_fl_peninsula.md` -- append-only entry (most-recent-first).
- This re-scope note.

## Release steps (your lane)
1. **Step-0 preflight:** `sha256(crops_data_final.json) == LATEST.txt` (`adf6f86f`). Patch `start_sha` matches.
2. **Apply** v1 (drift guards on every op; `sys.exit(1)` on mismatch).
3. **Run the deriver** (`tools/derive_berry_calendars` / the `berry_herbaceous_calendar` path) for the two new cells. **VALIDATE: this is the FIRST strawberry cell expected to emit `season_over`** (pulled annual, summer off-season). Confirm the derived `calendar[]` contains `season_over` and contains NO `dormant` and NO `renovation` (annual cell -- A11 / D9 check 3 + check 4). Contrast ca_interior, whose carried bed correctly has no `season_over`.
4. **Gates:** `whole_crop_gate.py strawberry` (A2 region-fill now 8 gaps -> 6; A10 structural; A11 calendar coherence post-deriver; D9 `berries_herbaceous_violations`) + `register_completeness_gate.py`. A green gate is not a clean release -- also `release_verify.py` + cross-check this snippet's claims.
5. **Source sub-id mint (your autonomous release lane):** `uf_ifas_hs403` under parent `uf_ifas` (EDIS HS1154/HS403, T1 inherited, record `_admission_provenance`), mirroring `uf_ifas_vh021` / `clemson_hgic_1149`. The patch cites bare `uf_ifas`; re-point the cited entries to the minted sub-id if that is the house convention at write-back, OR admit `uf_ifas` as the parent + keep the page in `anchoring_urls` (lettuce carries the page sub-id -- match it). `uf_ifas_ep452` (South FL Gardening Calendar) is an optional corroboration admit.
6. **Collateral audit:** only `fl_peninsula` changed; all other crops + strawberry top-level byte-identical (my local check passed; re-confirm against canonical).
7. **Re-pin** `LATEST.txt` + regenerate `CURRENT_STATE.md` (full, via `tools/gen_current_state.py`) + commit.

Independently reproduced post-apply crop-object SHA (fl_peninsula filled): `0f3c3898bd9116cfd24467774ed1fed569f3dd77eb25eae44821837be5e43f24` (computed on the slice; canonical content SHA will differ since canonical holds all 123 crops -- this is the strawberry object hash for your cross-check).

## The remaining 7 warm regions (NOT in this patch)
Three templates are now proven; scale on them with per-region A5 sourcing (read a source for each; do not analogize from a neighbor):
- **Interior deserts -- `ca_desert`, `low_desert_az`, `warm_arid`:** the ca_interior **interior summer-plant annual** template. Likely a shifted (earlier/later) summer window -- re-source; deserts are not the valley.
- **Coastal CA -- `ca_north_coast`, `ca_south_coast`:** **genuinely source-decided** perennial-vs-annual. Coastal CA is the one US region HS403 itself flags as sharing FL-like conditions; mild summers may support either a perennial day-neutral bed or a long day-neutral annual. Read the source, do not infer.
- **`se_gulf`:** open `grown_as` call (humid-summer decline -- likely annual, but source it).
- **`hawaii_tropical` (z11):** open call; strawberries are an **elevation/niche** crop there. **Do NOT assume `year_round`** despite frost-free z11 -- mirror the onion hawaii lesson (a day-length / climate-gated crop's frost-free cell is not automatically year_round). Source the actual island practice or carry an honest informational note.

## Step-5 boundary flag -- YOUR CALL, Trevor (NOT resolved here)
Authoring the z11 cell surfaced a crop-level scalar question:
- Current: `hardiness_zone_min/max = 3 / 10`, `reliable_fruit_zone_min/max = 4 / 9`.
- But `fl_peninsula` now has a **z11 cell that fruits well -- as a pulled annual.**

The tension is real because the two scalars mean different things, and the annual reality does not map cleanly onto either:
- `hardiness_zone` = where the plant *survives* (a perennial-bed concept). A z11 winter annual does not "survive" z11 summer -- it is pulled. So z11 arguably does not belong in a *survival* range even though we grow it there.
- `reliable_fruit_zone` = where it *fruits well*. It demonstrably fruits well in z10 and z11 as an annual, so a literal reading says extend the max to 11 (and 10 is already authored as fruiting).

**Options (I recommend surfacing, not auto-applying):**
1. **Leave both scalars as-is; let the region cells carry the annual reality.** Cleanest semantically -- the scalars stay "perennial-bed survival / reliable perennial fruiting," and the `grown_as: annual` cells already say "grown here as a yearly crop." Matches how ca_interior z8-9 (annual, also above the reliable_fruit_zone max of 9 at z9) was handled: the region cell carried it, the scalar was not stretched. **This is the consistent precedent.**
2. **Extend `reliable_fruit_zone_max` to 10 or 11 with an explicit "fruits well as a fall-planted annual in z10-11" qualifier in `hardiness_notes_*`.** More literally accurate to "fruits well," but risks implying perennial reliability where the truth is annual.
3. **Extend `hardiness_zone_max` to 11.** I'd advise AGAINST -- it conflates survival with annual culture and is the least defensible reading.

My lean is **Option 1** (consistency with the ca_interior precedent + the cleanest scalar semantics; the annual reality is fully carried by the region cells and `grown_as`), but this is a definition call on what the two scalars are *for*, so it is yours. Flagging now so the remaining warm-region fill (several more annual cells at z9-11) applies one consistent rule rather than deciding ad hoc per region. Whatever you choose, it should be applied once, globally, at the Step-5 verification pass -- not per-cell.

## Carried flags (unchanged, for Steps 6-8 consumer prose)
- The day-neutral type story + the ca_interior small fall crop -> centralized `type_selection_*`.
- `bloom_duration_days` (currently null) -- author at 6-8 only if it informs the frost-on-blossom guidance.
