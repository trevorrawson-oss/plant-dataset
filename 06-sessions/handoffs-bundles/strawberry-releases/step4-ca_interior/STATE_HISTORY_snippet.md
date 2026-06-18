## 2026-06-18 — session `strawberry_step4_ca_interior` (ANNUAL proof cell)

**Start-SHA (expected):** `f880a63c6325125b0017b713dd13ac80c801d8d3699ae9a6cd5f0612d7412725` (`strawberry_step4_northern_tier`; full-file, Claude Code preflights at apply).
**Lane:** claude.ai authored the cell (grown_as + month-resolved windows + resolved_from:null + per-rule-entry anchoring + prose); `calendar[]` left `[]` for the deriver. Patch = 38 ops, `regions.ca_interior` z8+z9 ONLY.
**Gate:** not run this session (claude.ai authored JSON + this entry). Claude Code applies, runs the annual-branch deriver on z8/z9, then A10/A11 + whole_crop_gate + register_completeness_gate, re-pins SHA, regenerates CURRENT_STATE, commits. Expected residual after this cell: one region_notes-null gap clears (`ca_interior`); 8 warm regions remain.

### What happened — and the SOURCE finding that overturned the kickoff sketch
`ca_interior` (z8, z9) authored end-to-end as the ANNUAL proof cell. **The kickoff sketched a fall-plant (Oct–Nov) winter-annual window; the live UC IPM home-garden authority overrode it.** UC's recommended-planting-dates table (Time to Plant / Cultural Tips, both fetched + verified 2026-06-18) gives, for **short-day cultivars in the San Joaquin Valley: summer planting Jul 20–Aug 5; winter planting "not grown."** The Oct–Nov fall-plant window is the **coastal** pattern (Central Coast / Santa Maria / Oxnard / South Coast), NOT the hot interior. Authoring fall-plant here would have been the Reedley-reads-Florida / anti-cross-region (A5) defect. Trevor ratified authoring to source (option A).

- **grown_as = annual** (SOURCED, not inferred): UC — "replace your plantings with new plants from a nursery every 2 to 3 years"; "fruit production is usually highest in the first full season after planting and declines afterwards." Summer heat + soilborne pest buildup drive the replant cadence.
- **Windows (month-resolved, absolute; `resolved_from: null`; `resolution_method: absolute_month_uc_planting_table`):** plant_out **Jul 20–Aug 5**; a **small fall crop** (~Oct) the planting year; main flush the **following spring, peak May–Jun**. Cell `harvest` display = "Oct, then May - Jun". The decision this proof cell was scoped to settle — **how a frost-BEARING annual anchors — HELD: month-resolved + resolved_from:null**, exactly as predicted; only the month values differ from the sketch (a sourcing correction, not a scope change).
- **frost_risk_note_seasoned** authored per cell (valley winters mild-but-not-frost-free; a hard/late freeze injures open blossoms on the overwintering crop) even though windows are month-resolved — frost is a risk, not the anchor.
- **Per-rule-entry anchoring** authored on each arm (plant_out/bloom/harvest_start/harvest_end) and per cell, one entry per source ID — the northern_tier conformance lesson applied from the start; no release fix needed.
- **Source:** `uc_ipm` (catalogued, already in-slice). Two specific verified pages: `…/time-to-plant` (the dated table) and `…/cultural-tips-for-growing-strawberry` (annual culture, replant cadence, harvest). Chill (100–300 hr, informational) + self-pollinating corroborated on `…/strawberry`. No new parent source; no sub-ID minted (Claude Code's release-lane call if a page-specific sub-ID under uc_ipm is wanted, mirroring the clemson_hgic_1149 pattern).

### THE CLEANER MAP (B's insight, folded in) — two annual sub-shapes, not one
- **Interior summer-plant annual** — `ca_interior` is the template for **ca_desert / low_desert_az / warm_arid** (shared hot-summer, summer-or-spring-plant reality).
- **Frost-free fall-plant annual (true plasticulture)** — a DISTINCT sub-shape still UNPROVEN; `fl_peninsula` (z10/z11, genuine Oct–Nov winter annual) is its proof cell; coastal-CA TBD.
- **A5 in BOTH directions:** do NOT template the interior summer-plant window onto coastal/FL cells, and do NOT template the coastal fall-plant window onto the interior deserts. Recorded in `plantings_provenance`.

### Calendar — deferred to the deriver (Claude Code lane), with a flagged shape question
`calendar[]` left `[]` for `berry_herbaceous_calendar` (annual branch). **Claude Code flagged (its note, carried here):** the valley summer-plant arc (plant summer → small fall crop → main spring flush → bed persists 2–3 yr, no winter dormancy) is a third shape vs both branches built; A10 doesn't require `season_over` and A11 only checks coherence, so the gates won't reject it, but the generated calendar should be validated against these authored windows at release and the deriver refined if the summer-stress / no-off-season shape needs it. **Open structural question for Claude Code:** whether the annual valley cell carries `season_over` at all (the bed is carried over, not pulled at year end) — likely NO season_over, no dormant; resolve at the deriver run.

### Deferred (correctly, per Trevor)
- **Day-neutral-in-the-valley note** (UC: day-neutral isn't tabled for San Joaquin; Santa-Maria-style Feb 15–Jun 15 is the day-neutral coastal window): deferred to the centralized `type_selection_*` section at Steps 6–8. Cell notes stay about the cell's short-day lifecycle; the type story lives in ONE place.

### Verification done (dry-run, SHA-gated discipline)
- All 38 from-guards matched on a dry-run apply against the slice; applied clean.
- Collateral: ONLY `regions.ca_interior` changed; all 9 other regions + non-region top-level byte-identical.
- D9-intent structural checks CLEAN: grown_as typed=annual both cells; calendar=[] (deriver handoff); resolved_from null; resolution_method set; per-cell + per-arm anchoring one-per-source-ID; no tree keys (suitability/chill_hours_delivered); track flipped perennial→annual; arm entries carry `from:null` (month-resolved, not frost-relative).
- User-facing copy guard CLEAN: 0 `--`, 0 em/en-dash, 0 spelled-degrees, American spellings (region_notes + grown_as_note + frost_risk_note). `90F` written with the degree sign in the dataset string.

### Carried flags (unchanged)
1. `grown_as` per region remains a per-region SOURCE call for the remaining 8 (ca_desert/low_desert_az/warm_arid expected interior-annual on THIS template; fl_peninsula fall-plant annual = separate proof; se_gulf/hawaii_tropical + the 2 coastal-CA perennial-vs-annual calls genuinely open).
2. `reliable_fruit_zone` 4-9 warm-edge refinement (this cell carried the flag; no UC figure refined it — left for the warm pass / Step 5).
3. Per-rule-entry anchoring placement — authored correctly from the start.
