# Onion photoperiod (day-length) model -- design

**Date:** 2026-06-16
**Author:** Claude Code (structural lane)
**Status:** Approved design (Trevor, 2026-06-16). Implementation plan next.
**Milestone:** Onion gold-standard arc (anchor 12). Onion is the FIRST photoperiod-gated crop -- its schema stress-test.
**Reads against:** gold-standard arc checklist v2.0 (Steps 2 / 3.5 / 4 / 5.5 / 6-8 / 11); `tools/whole_crop_gate.py` (the A-section gate pattern); `tools/build_region_shells.py`; `tools/perennial_gate.py` (the `gating_factors` precedent); the evergreen `gating_factors` amendment.
**Start SHA:** `f89a1b7af025513eab4ec11dc0cbd54a15ab49a9f18999db14d69396f347bb65` (canonical content SHA; must equal `LATEST.txt` at apply time -- Step 0 preflight).

---

## 1. Problem

Every certified anchor so far resolves its region behavior on a CLIMATE axis: frost (annuals), heat (warm crops), chill (deciduous trees), cold/heat accumulation (evergreen citrus). Onion is the first crop where the deciding axis is **photoperiod**: a bulb onion only bulbs when day length crosses a cultivar-specific threshold, so WHICH variety bulbs at all depends on the grower's latitude.

- **Long-day** onions need ~14-16 h of daylight to bulb -- they work in the northern tier.
- **Short-day** onions bulb at ~10-12 h -- they work in the South.
- **Intermediate-day** (a.k.a. day-neutral for guidance purposes) bulb at ~12-14 h -- the broad middle, and the safe "works most places" pick.

There is **zero day-length modeling anywhere in the dataset today**. Plant the wrong type for your latitude and you get no bulb (a long-day onion in Florida stays a scallion; a short-day onion in Minnesota bulbs tiny and early). This is exactly the failure a region-resolved guide should prevent, and exactly why onion is a gold-standard anchor.

**Product decision (Trevor, 2026-06-16): region-resolved.** The guide should tell a grower, per region/zone, which day-length type to grow, and tag each recommended variety with its type so the grower can pick a matching one. This runs day-length guidance through the same region engine that already resolves frost, chill, and suitability -- the competitive moat over uncited apps that give a generic "match your latitude" line.

**Approach decision (Trevor, 2026-06-16): two-layer (variety-tagged + region-resolved).** A variety-only model leaves the grower to self-map latitude to type; a region-only model says "grow short-day" without telling the grower which listed variety IS short-day. Only the two-layer model delivers the resolved experience, and it reuses the variety + region-cell patterns already certified on 11 anchors.

---

## 2. Decisions

**D1 -- Photoperiod is an added VARIETY-SELECTION axis, not a calendar change.** Onion's `calendar_basis` stays `frost_anchored`. Its sowing/harvest windows are resolved by frost exactly like every other annual. Photoperiod gates which CULTIVAR bulbs at a latitude; it never moves a planting date. Step 5.5 (calendar coherence) is unchanged.

**D2 -- The suitability axis is the existing `gating_factors` list.** Onion carries crop-level `gating_factors: ["photoperiod"]`, the same field citrus uses for `["cold_hardiness"]`. This is **non-breaking**: `perennial_gate.perennial_cert_violations` no-ops for any non-perennial `calendar_basis` (returns `[]` before reading `gating_factors`), and `build_region_shells` only tests for `"heat_accumulation"` membership. So `"photoperiod"` is inert to all existing code; only the new photoperiod gate (D5) reads it. No decoupling or refactor of `gating_factors` is required.

**D3 -- Day-length type is a 3-token enum.** `day_length_type` and `recommended_day_length_type` both draw from `{long_day, intermediate_day, short_day}`. "Day-neutral" folds into `intermediate_day` (the two are interchangeable for region guidance); any cultivar-level nuance rides that variety's `recommended_note`.

**D4 -- Variety records become objects (peach-shaped).** Author-fresh onion authors `varieties.recommended[]` as objects, not bare strings (carrot/lettuce use strings; peach/microgreens already use objects). Shape: `{ name, use, day_length_type, recommended_note }`. `day_length_type` is the per-cultivar token; `recommended_note` is the universal-plain descriptor (peach precedent, EXCLUDED from register pairing).

**D5 -- A new gate with a coverage invariant.** `photoperiod_violations(crop)` (test-first), wired as `whole_crop_gate` section **A9**, no-op unless `"photoperiod" in gating_factors` -- the same off-branch-safe pattern A6/A8 used. It is the teeth of the model (see Section 4).

**D6 -- The per-cell type is a SOURCE finding per region (A5 discipline).** Each cell's `recommended_day_length_type` is read from a source for that region's latitude band, NOT inferred from latitude by analogy. The expected bands (north -> long, south -> short, middle -> intermediate) are a sanity check the source must corroborate, never the authority. This is the same "window structure is a source finding" rule that governs the frost windows.

---

## 3. Schema

### 3a. Crop level
```
"gating_factors": ["photoperiod"],
"photoperiod": {
  "explainer_seasoned": "<dual-register: what day length is, why it picks the variety>",
  "explainer_beginner": "<...>",
  "sources": [...],            // >= 2 T1
  "anchoring_urls": {...}      // per-source {url, verified}
}
```
`calendar_basis` stays `frost_anchored`. The `photoperiod` block is the crop-level concept explainer + provenance; it does NOT carry per-region data (that lives in the cells).

### 3b. Variety level (`varieties.recommended[]`, objects)
```
{ "name": "Walla Walla", "use": "sweet fresh", "day_length_type": "long_day",
  "recommended_note": "A mild long-day sweet onion for northern gardens; not a keeper." }
```
`day_length_type` in `{long_day, intermediate_day, short_day}`. The recommended set spans the types the dataset's regions need (see the coverage invariant, Section 4).

### 3c. Region/zone cell (`resolved_by_zone.<zone>`)
```
"recommended_day_length_type": "short_day",
"day_length_note_seasoned": "<At this latitude only short-day onions bulb...>",
"day_length_note_beginner": "<...>"
```
`recommended_day_length_type` is the resolved guidance token; `day_length_note_*` is the dual-register cell note. These sit alongside the frost windows the cell already resolves. (Where an entire region is one band, the value is constant across its zone cells; it is still authored per cell to mirror `suitability`, and a region-root note may summarize it.)

---

## 4. The gate -- `photoperiod_violations(crop)` (whole_crop_gate A9)

No-op unless `"photoperiod" in (crop.get("gating_factors") or [])`. Otherwise returns a list of violation strings (`[]` = pass). Asserts:

1. **Variety typing.** Every `varieties.recommended[]` entry is an object with `day_length_type in {long_day, intermediate_day, short_day}`.
2. **Cell typing.** Every resolved cell with a non-empty planting window carries `recommended_day_length_type` in the same enum.
3. **Coverage invariant (the teeth).** For every distinct `recommended_day_length_type` resolved across the region cells, at least one recommended variety carries that `day_length_type`. The guide may never say "grow short-day here" while listing zero short-day varieties. This mirrors the perennial `survives != fruits` invariant: a resolved verdict the rest of the page cannot honor is a defect.
4. **Register pairing.** `day_length_note_seasoned`/`_beginner` present as a pair on every cell that carries the type (enforced by the existing register gates; A9 asserts presence as a backstop).

Built test-first against FILLED onion data; run at Step 11 cert and on-demand. Added to the always-on `whole_crop_gate` as section A9 (no-op off-branch), consistent with how A6 (indoor cycle) and A8 (successions_realized) were added.

---

## 5. Arc integration (no new steps; fields land inside existing steps)

- **Step 0 (preflight):** SHA == `LATEST.txt`.
- **Steps 1-2 (claude.ai authors):** source set; `start_method.start = "both"` (onion is grown from sets/transplants AND direct seed); scalars; `gating_factors: ["photoperiod"]`; the `photoperiod` explainer block; `varieties.recommended[]` objects with `day_length_type`. Display-readiness DoD: SOURCED `days_to_maturity` + `spacing_inches` (both empty on the shell today).
- **Step 3 (companions):** standard v2.0 companion walk.
- **Step 3.5 (Claude Code lane -- me):** rebuild onion's region shells with `build_region_shells.py`. Onion's cells are in the STALE pre-3.5 shape (they still carry `start_indoors`, `first_plant_date`, `last_plant_date`, `notes`, `zone_notes`, `planting_note`, nested `plantings`, `lifted_from_zone`); the builder strips those to the reference shape. EXTEND the builder: when `"photoperiod" in gating_factors`, scaffold the per-cell `recommended_day_length_type` (null) + `day_length_note_seasoned`/`_beginner` (null) slots. Test-first, idempotent, no-clobber.
- **Step 4 (claude.ai sources):** fill each cell's `recommended_day_length_type` as a per-region SOURCE finding (D6) plus the frost windows.
- **Step 5.5 (calendar):** unchanged. Onion is a normal frost-anchored annual; succession/heat-pause coherence applies as usual; photoperiod is not a calendar token.
- **Steps 6-8 (prose):** author `photoperiod.explainer_*`, the cell `day_length_note_*`, and variety `recommended_note`, all dual-register, swept by `register_fill_gate`. Bolting/vernalization biology is authored into the normal prose surfaces (`failure_diagnostics`, `tips_by_stage`) -- NO new schema field for it (Section 6).
- **Step 11 (cert):** A9 + `register_fill_gate` (0 null register fields) + the standard flip (`verification_status` block + top-level `last_reviewed`/`_session`).

---

## 6. Register classification (Appendix A)

- **Tokens / enums -- categorical, EXCLUDED (no `_seasoned`/`_beginner`):** `gating_factors`, `day_length_type`, `recommended_day_length_type`.
- **CP pairs (suffix-ruled, dual-voice auto-covered):** `day_length_note_seasoned`/`_beginner`, `photoperiod.explainer_seasoned`/`_beginner`.
- **Universal-plain, EXCLUDED (peach precedent):** `varieties.recommended[].recommended_note`.

`recommended_day_length_type` and `day_length_type` are added to `register_completeness_gate.EXCLUDED_KEYS` / the categorical matcher; the `*_note_*` keys are auto-covered by the suffix rule. Confirm at the Step 3.5 / first-authoring gate run.

---

## 7. Boundaries (out of scope)

- **Scallion / spring-onion is a separate crop and a separate, simpler later arc.** It is harvested green before bulbing, so photoperiod is largely moot for it. Not part of onion's arc.
- **The region-filtering variety CHOOSER UI** (actively filtering/grouping recommended varieties by the grower's region) is a plant-astro render feature gated on app dev. This design produces all the DATA that UI will need; it does not build the UI.
- **Bulb onion only.** Garlic, shallots, leeks (other photoperiod-relevant alliums) are downstream; the `gating_factors: ["photoperiod"]` model is reusable for them, but they are not in scope here.

---

## 8. Bolting / vernalization (noted, not a schema change)

A bulb onion is a biennial grown as an annual; a cold spell after early planting (or oversized sets/transplants) can vernalize it into bolting (flowering) instead of bulbing. This is real onion biology a gold-standard guide must surface, but it is covered by the existing prose surfaces (`failure_diagnostics`, `tips_by_stage`, the cold-zone planting-window guidance) -- it does NOT need a new schema field. Flagged here so claude.ai authors it; not a structural item.

---

## 9. Lane split

- **Claude Code (me), structural:** the `build_region_shells` extension (per-cell day-length slots) + the stale-shape rebuild; the A9 gate (`photoperiod_violations`) test-first; the `register_completeness_gate` exclusions; all release-time gate runs; the Step 1-2 / Step 4 kickoff bundles.
- **claude.ai, authoring:** the `photoperiod` explainer copy; the variety set + `day_length_type` tags + `recommended_note`; each cell's `recommended_day_length_type` (sourced) + `day_length_note_*`; bolting prose; all biology/values.
- **Trevor:** ratifies this design (done) and reviews each release before push.
