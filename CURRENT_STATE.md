# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push).

---

## 🥬 LETTUCE FLIPPED (M15) · 🍅 CHERRY Step 3.5 region shells BUILT (M16, 2026-06-05)
`lettuce-leaf` is the FIRST flipped anchor (1 of 9): `launch_ready_core=True` + `launch_ready_seasoned=True` (`status` stays `"unverified"` pending the M16 vocab decision). **M16 is in flight on `cherry-tomato`, CHERRY FIRST then beefsteak.** This session completed cherry's **Step 3.5 (region shell build, Claude Code lane)**: all 10 region cells are now at the ratified reference shape (§A2 shape classes = 0; `gs_exemplar_finding_shell` closed). It also DEFINED the net-new `second_planting` structure (cherry is the first crop to need it). Cherry now hands to **claude.ai for Steps 4-8** (warm-window sourcing, the second-planting dates + which-zones, region_notes copy, dual-voice siblings, the T2 ruling). **Lettuce was NOT touched -- byte-identical, still certified.**

## Canonical pointer
- **Current SHA:** `1b4fea68e63ed63c02cc50aeb8bd55a761c6d6534fe037fba371eab7130df68a` (M16 cherry Step 3.5 -- `lifted_from_zone` north normalization, follow-up to the region shells). `LATEST.txt` session line: `m16_cherry_step3_5_lifted_from_zone_norm`.
- **Predecessor chain:** `1b4fea68` (north `lifted_from_zone` strip) <- `a65c7175` (cherry Step 3.5 region shells + `second_planting` structure) <- `29b3aaa9` (M15 lettuce flip) <- `6880ed37` (lettuce write-back) <- `37bfc12d` <- `cdcbf175` <- `df4d24c7` <- `da4b8bc5` <- `7e9eeceb` <- ... (full lettuce chain in STATE_HISTORY).
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## What just happened (2026-06-05, session `m16_cherry_step3_5_region_shells`)
- Ran the full superpowers flow: brainstorming -> spec (`docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`) -> plan (`docs/superpowers/plans/2026-06-05-cherry-region-shells.md`) -> subagent-driven execution (4 tasks, each implementer + spec + code-quality reviewed).
- **Built cherry's 10 region shells (Step 3.5):** `northern_tier` promoted from cold `zones{}` (track added, nested `plantings` stripped, `zone_promoted_verified`, provenance rewritten); 9 warm/CA regions -> shape-complete RULE skeletons (empty archetype window arrays); 4 `region_label` em-dashes resolved. NO biology values invented; NO warm zone data carried as verified.
- **Defined the `second_planting` structure** (the bigger design outcome -- see Live locked decisions). Tooling: `tools/build_region_shells.py` (pure transform) + `tools/apply_region_shells.py` (SHA-gated apply + collateral audit) + a `whole_crop_gate.py` §A2 validation block for `second_planting`.
- **Gate:** cherry §A2 shape classes = 0; total 42 -> 34 (residual = downstream claude.ai). Lettuce regression-guarded `GATE: PASS` byte-identical. Collateral audit clean (only `cherry.regions` changed).
- **Follow-up normalization (same session, SHA `a65c7175` -> `1b4fea68`):** a lettuce-vs-cherry north comparison surfaced one shape divergence -- cherry's north resolved cells kept the tautological `lifted_from_zone` key that lettuce's `northern_tier` sheds. Fixed in `build_region_shells.py` (strips it in the north promote; applies to all 121 crops) + re-applied to cherry (surgical: only `lifted_from_zone` removed from the 5 cold cells, gate unchanged at 34, lettuce still PASS). Cherry's north now has ZERO cherry-only cell keys vs lettuce (remaining lettuce-only keys = `heat_pause`/`succession_*` = correct biology differences). NOTE the still-deferred non-shape differences from lettuce (claude.ai's Steps 4-8, by design): `calendar[12]` not yet derived (cherry north carries `wait` in winter-gap months where lettuce has `cold_pause` -- Step 5.5 pause classification), `region_notes` null.

## Active work + exact next step
- **M16 cherry is at Step 3.5-COMPLETE. NEXT = claude.ai Steps 4-8** on cherry: warm-region window sourcing into the shells; author which zones get a `second_planting` + the dates (the structure is defined + gate-validated, the data is biology); region_notes copy (Steps 6/7); dual-voice siblings incl. `cause_beginner` (`gs_exemplar_finding_004`, Steps 7/8); `harvest_to_table` T2 ruling (Step 10); extreme-zone computation record (`gs_exemplar_finding_003`, Step 2); `cornell_ext` zone-6 URL (Step 5). Then back to Claude Code for Step 11 certification + flip.
- **`status`-vocab decision still owed** (Appendix B item 1): the successor to `"unverified"` for `verification_status.status`, decided at cherry's flip and back-applied to lettuce + both tomatoes. Do NOT set `gold_standard` before it is decided.
- **Then beefsteak** repeats the SAME arc start-to-flip, INHERITING the cherry rulings but independently verifying its biology (v1.4.1 §4). Its Step 3.5 reuses `tools/build_region_shells.py` (parameterized by slug; the re-run guard makes it pipeline-safe).
- **Riders from the lettuce arc (non-gating, claude.ai lane, still open):** s11_finding_004.2 Option-A thermoinhibition-source package; the Appendix-A inventory merge.

## Step 3.5 gate record (2026-06-05, post-promote, on canonical)
- **§A2 shape classes: `stub:0 | null-track:0 | stale nested:0`** -- the Step-3.5 success condition; `gs_exemplar_finding_shell` closed. `both region_notes null: 10` REMAINS (admission-acceptable per the v1.5 two-callsite model; becomes a Step-11 cert violation; claude.ai authors region_notes at Steps 6/7).
- Residual gate count 34 (all downstream): 10 region_notes-null, 21 dual-voice siblings, 1 source-name dash, 1 `harvest_to_table` T2, 1 `cornell_ext` URL. §F anchoring 3->1; §C/D dash 5->1.
- Lettuce `GATE: PASS`, byte-identical. Collateral audit: only `cherry.regions` changed.

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- ✅ lettuce DONE (1 of 9). Cherry is mid-arc (Step 3.5 done, owes Steps 4-11). Beefsteak after cherry.
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce ✅; cherry shell ✅ this session, owes fill; beefsteak owes both). Ships with `zones{}` fallback. **2.9+.** (The plant-astro renderer rewrite -- read `regions{}` + consume `second_planting` instead of synthesizing from `zones{}` multi-window strings -- is gated here.)
3. **Authoring-model flip** -- carrots onward authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, **2.9+**. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial extension are **2.9+**.

## Live locked decisions / guardrails
- **`second_planting` structure (Claude Code lane, Trevor 2026-06-05) -- NEW.** Cherry is the first crop to need a discrete second planting. Representation OWNED by Claude Code (the renderer is ours). Resolved shape: `resolved_by_zone[z].second_planting = {plant_out, start_indoors, harvest_start, harvest_end, sources, anchoring_urls}` on applicable zones only, + a region-constant `plantings[]` entry `track:"second_planting"`. Discrete plantings (`beginner` + `second_planting`) share one window shape; SUCCESSION is a SEPARATE cadence -- two honest patterns, not one forced shape. Seasoned-only visibility (like succession). The gate validates the structure when present. Full spec: `docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`.
- **Resolved-layer shape standards RATIFIED (2026-06-05):** main planting = flat cell fields (universal); succession = `succession_spring`/`succession_fall` cadence (lettuce's shape, ratified -- carrot matches it, no new shape); `second_planting` = the discrete-window object above. Each crop carries ONLY the structures for what it is; each concept has ONE fixed shape across crops. **Lettuce is NOT reshaped** -- it already represents what it is.
- **Shape-complete shells, not thin (2026-06-05):** Step 3.5 builds the archetype-correct RULE skeleton (window-rule keys present, arrays empty) so Step 4 fills VALUES, not 121 passes each building shape. Resolved cells stay PENDING fill-targets (derived output).
- **Rendering is the app's call; the dataset is rendering-agnostic.** Built UI already handles cherry's second planting: `PlantingCalendarCard` (main, both modes) + `SuccessionCard` (seasoned-only, two render modes = discrete-window vs cadence). The structured `second_planting` replaces those cards' fragile synthesis. Same-calendar-band vs separate-card decided at the Phase C renderer rewrite; `zones{}` stays coherent until then so the current UI keeps working.
- **REGION SHELL-BUILD RULE (Trevor 2026-06-05):** every crop's arc builds ALL 10 region cells to the lettuce bar. North (`northern_tier`, zones 3-7) builds FROM legacy cold `zones{}` (promote + verify + hoist succession into region-constant `plantings[]` where applicable; strip nested cell `plantings`; re-stamp `static_precompute -> zone_promoted_verified`; **strip the tautological `lifted_from_zone` key** -- in the north it always equals the cell's own zone, and the reference crop lettuce sheds it; added to `build_region_shells.py` 2026-06-05, applies to all 121 crops' north). Warm/CA re-derive from T1 (zone data may be climate-contaminated). `whole_crop_gate.py` §A2 enforces the structural side (stub + null-track + §3b-i nested-cell catcher). Cherry's Step 3.5 this session is the first execution. **Owed: claude.ai folds the `lifted_from_zone`-strip into the checklist v1.5 Step 3.5 north sub-procedure text** (the tool already enforces it).
- **Governing checklist: v1.5** (Step 3.5 Region shell build; reference-GS-crop = `lettuce-leaf`; two-callsite admission/certification model -- null `region_notes` / empty `anchoring_urls` accepted at Step 3.5, violations at Step 11). Dataset is authoritative; flag doc lag.
- **Lane split.** STRUCTURAL/MECHANICAL = Claude Code (region shells, transforms, gates, audits, SHA re-pins, flips, the `second_planting` representation). Biology + consumer copy + voice/IP + URL discovery + which-zones/dates for second_planting + Appendix-A = claude.ai.
- **Anchoring gate is LAYER-SCOPED (1A):** claim-bearing leaves only; legacy `zones{}` + the 10 `regions{}` root rollup `sources` arrays excluded; sibling-named `*_sources`/`*_anchoring_urls` pairs included; `bolting.*` inherit-class excluded.
- **Keep `zones{}` coherent until Phase C** (deletion gate: region carries everything + consumers read region-first + round-trip + frost-input independence). The current renderer still reads `zones{}`.
- **Inheritance is candidate, not verified (v1.4.1 §4).** Pest/disease = highest-scrutiny cluster. Verify cherry AND beefsteak independently even where biology overlaps.
- **TEMPERATURE -- canonical `°F`** user-facing. **DASH -- per-sense, per-crop**, executed by each crop's arc (cherry's 4 region_label dashes resolved this session; 1 source-name dash remains, downstream).
- **Two-field readiness predicate, never a bare count:** `blocks_launch AND status != "resolved"`.
- **Dataset push autonomous (announce-then-execute); plant-astro stays gated.**

## Open items owed
- **M16 cherry Steps 4-8 (claude.ai):** warm-window sourcing; the `second_planting` data (which zones + dates) authored against the defined structure; region_notes copy; dual-voice siblings incl. `cause_beginner`; the `harvest_to_table` T2 ruling; the extreme-zone computation record; `cornell_ext` zone-6 URL. Then Claude Code Step 11 + flip.
- **`status`-vocab decision (Appendix B item 1):** successor to `"unverified"`; decided at cherry's flip, back-applied to lettuce + tomatoes.
- **Lettuce riders (claude.ai):** s11_finding_004.2 Option-A thermoinhibition source; Appendix-A inventory merge.
- **Beefsteak:** full arc after cherry flips (Step 3.5 reuses `tools/build_region_shells.py`).
- **The 5 Appendix-C findings on cherry:** `_shell` CLOSED this session; `_001` (warm sourcing + `cornell_ext` URL + orphan UMN text), `_002` (dashes -- region_labels done, source-name remains), `_003` (extreme-zone record), `_004` (`cause_beginner`) remain for claude.ai's Steps 4-8.
- **Gate tooling note:** `tools/whole_crop_gate.py` now knows `second_planting`; `build_region_shells.py` + `apply_region_shells.py` are committed + reusable for beefsteak/pipeline (slug-parameterized, re-run-safe).
- **Checklist amendments + archetype-driven biology checklist + dual-voice gate v2 ship-into-tools** (claude.ai/Claude Code, unchanged).
- **Pipeline / operating-model doc; `safe_sowing_note` migration (Phase C); `track` `beginner` -> `main` rename; companions reconciliation (§5)** -- all unchanged, deferred.

## Inherited findings (unchanged)
- `finding_001` -- warm `zones{}` 8-11 SE-mis-sourced (legacy layer, own pass); excluded from the anchoring gate by 1A definition.
- na3d-na3g sourcing-sibling findings; `na3d_finding_003` cosmetic.
- Two-field predicate returns 0 unresolved blockers (s11_finding_004 open but non-blocking).

*Update this file at each session close.*
